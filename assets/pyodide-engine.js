/* dewlab's shared Pyodide engine — dewmini's worker *client*
 * (DECISIONS_LOG.md 7.89).
 *
 * Runs Pyodide off the main thread by reusing assets/pyodide-worker.js —
 * the same file the hosted tutorial pages already boot through
 * (assets/tutorial-runtime.js). This module handles booting, running a
 * cell, hover/signature-help lookups, Stop support, filesystem mounting,
 * and streaming a cell's output back into its own output element. The
 * page that configures it owns the cell array and the DOM; this module
 * never touches either directly, only through the accessors passed to
 * configure() — which is what keeps it independent of any one page's
 * markup.
 *
 * A separate module rather than part of dewmini.js because 700 lines of
 * genuinely tricky Worker/interrupt/postMessage logic deserve their own
 * file with their own seams (DECISIONS_LOG.md 7.89 for the history) —
 * note that tutorial-runtime.js still runs its own copy of the
 * worker-communication logic rather than importing this, per that
 * file's own "each page owns a thin copy" convention.
 *
 * A page opened over file:// (a downloadable, offline copy) can run into
 * real restrictions constructing a module Worker at all, so boot() falls
 * back to running Pyodide on the main thread — same interpreter, same
 * tutorial_tools.py, just no genuine Stop button, exactly like the
 * tutorial pages' own standalone export (DECISIONS_LOG.md 7.77).
 */

/* sqlite3 was unvendored from Pyodide's default stdlib bundle as of
 * Pyodide 0.28 — it's now just another entry in loadPackage's list, not
 * the vendoring problem planning/DECISIONS.md's older "core libraries"
 * note was about. */
const DEFAULT_PACKAGES = ["numpy", "pandas", "matplotlib", "sqlite3"];

/* Puts every name in tutorial_tools.__all__ into the shared namespace,
 * plus __name__ — run once at the end of boot, and again by
 * resetPageStateMT()/the worker's own "reset-page-state" handler after
 * reset_page_state() clears that namespace out, so the always-available
 * names come right back without needing a full re-boot. */
const RESEED_GLOBALS_SOURCE = `
import tutorial_tools
tutorial_tools._page_globals.update({
    name: getattr(tutorial_tools, name)
    for name in tutorial_tools.__all__
})
tutorial_tools._page_globals["__name__"] = "__dewlab__"
`;

/* Lets ordinary Python HTTP code work here, by pointing it at the browser's
 * own fetching.
 *
 * Python in a page has no network connection of its own, so `urllib` — which
 * is what `pandas.read_csv("https://…")` uses underneath — fails before it
 * even tries, with "unknown url type: https". That message is accurate and
 * useless: it means urllib has no HTTPS *handler* registered, because it has
 * no TLS library to register one with. It does not mean the page cannot
 * reach an HTTPS site. The browser does that constantly.
 *
 * `pyodide_http.patch_all()` bridges the two, rerouting urllib (and requests,
 * if a reader installs it) through the browser's own fetch. The browser then
 * performs the TLS itself, with its own certificate checks and its own trust
 * store — so `https://` stays fully encrypted and verified; the encryption
 * simply happens one layer out from Python.
 *
 * 9.6 KB, which is the whole reason this is on by default rather than an
 * option: every pandas tutorial ever written reads a URL this way, and a
 * student copying one should not have to know any of the above.
 *
 * Wrapped in try/except because a vendored Pyodide built before this was
 * added will not have the package (dev/fetch_pyodide.py's --packages list),
 * and an offline bundle must still boot without it — just without the
 * convenience. tutorial_tools.py's own error hints then explain the manual
 * route, so the failure stays informative rather than silent. */
const NETWORK_PATCH_SOURCE = `
try:
    import pyodide_http
    pyodide_http.patch_all()
except Exception:
    pass
`;

/* Resolved against *this module's own location* (assets/pyodide-engine.js),
 * not the page importing it: a relative fetch from inside the worker
 * resolves against the worker script's own location, not the page's, so
 * every URL handed to the worker (or read by the main-thread fallback) has
 * to be absolute first — and resolving against this module rather than
 * document.baseURI is what makes that absolute URL come out right no
 * matter how deep the importing page sits (dewmini's own
 * compose/dewmini.html one directory below the site root, in
 * particular). */
function assetUrl(relativePath) {
  return new URL(relativePath, import.meta.url).href;
}

/* These variables are this module's entire "connection" to the page
 * that's using it. They start out empty (or default) and get filled in
 * by configure() below, once, when the page first sets things up.
 * Keeping them as plain module-level variables (rather than passing them
 * around as arguments to every function) is a deliberate simplification:
 * everything in this file needs getOutputEl and setStatus, so it's less
 * noisy to set them once than to thread them through every function
 * signature. */
let getOutputEl = null; // (cellId) => that cell's output <div>, or null
let onStatus = null; // (text, kind?) => show a status message on the page
let packages = DEFAULT_PACKAGES; // which Pyodide packages to load at boot
// The base URL tutorial_tools.py's own load_csv() resolves a dataset name
// against — empty by default (right for a page at the site root),
// overridable per page since dewmini lives one directory deeper
// (compose/) and needs "../data/" to reach the same repo-root data/
// folder the tutorial pages already share.
let dataBase = "";

/**
 * Wire the engine up to the page that owns it.
 *
 * @param {Object} options
 * @param {(cellId: string) => (HTMLElement|null)} options.getOutputEl -
 *   looks up a cell's live output element by id, the same way
 *   applyOutputEvent below needs to.
 * @param {(text: string, kind?: string) => void} [options.onStatus] -
 *   forwarded boot/package-loading progress text.
 * @param {string[]} [options.packages] - Pyodide packages to load at boot.
 * @param {string} [options.dataBase] - base URL load_csv() resolves a
 *   dataset name against; empty unless overridden.
 */
export function configure(options) {
  getOutputEl = options.getOutputEl;
  onStatus = options.onStatus || (() => {});
  if (options.packages && options.packages.length) packages = options.packages;
  if (typeof options.dataBase === "string") dataBase = options.dataBase;
}

/* A tiny wrapper so the rest of this file can just call setStatus(...)
 * instead of checking every time whether onStatus was ever configured.
 * (configure() above already guarantees onStatus is at least a no-op
 * function, so this never has to check for null.) */
function setStatus(text, kind) {
  onStatus(text, kind);
}

/* Mirrors _DomSink's own create-or-append logic (assets/tutorial_tools.py)
 * exactly — one open <pre> per contiguous run of the same stream class.
 * Shared by both the worker and main-thread paths, since tutorial_tools.py
 * emits the identical event shape either way (tools.run_cell's
 * output_target is a callable on the worker path, a DOM element on the
 * main-thread one — see tutorial_tools.py:601-638 — so this module always
 * hands it a callable and normalises here). */
const openStreams = new Map(); // cellId -> {el, cssClass}

/**
 * Takes one "output event" from Python (whether it arrived from the
 * Worker via postMessage, or was produced right here on the main thread)
 * and turns it into real DOM changes in a cell's output area.
 *
 * There are three kinds of event, matching what a running cell can do:
 *   - "stream": more text was printed (e.g. print(), or stderr). This is
 *     appended to the *currently open* <pre> for this cell if there is
 *     one with the same cssClass, or a new <pre> is started. That's what
 *     lets several print() calls in a row show up as one growing block of
 *     text instead of one <pre> per call.
 *   - "append": a finished, self-contained piece of output (a table, an
 *     image, a widget) arrives as ready-made HTML and gets inserted as-is.
 *     This also closes off any open stream, since whatever comes next is
 *     a new thing, not more of the same printed text.
 *   - "clear": wipe the cell's output area completely (used when a cell
 *     starts running again).
 */
function applyOutputEvent(cellId, kind, cssClass, text, markup) {
  const el = getOutputEl ? getOutputEl(cellId) : null;
  if (!el) return;
  if (kind === "stream") {
    let open = openStreams.get(cellId);
    /* `el` is looked up fresh above, but the open <pre> is cached — and a
     * re-render mid-run (reordering cells, inserting one) replaces the
     * output area under it, leaving this node detached. Appending to a
     * detached node loses the rest of the cell's output silently, so a <pre>
     * that is no longer inside the current output area is treated as no open
     * stream at all and a fresh one is started. Reachable since Python moved
     * off the main thread: the page stays responsive while a cell runs. */
    if (!open || open.cssClass !== cssClass || !el.contains(open.el)) {
      const pre = document.createElement("pre");
      pre.className = cssClass;
      el.appendChild(pre);
      open = { el: pre, cssClass };
      openStreams.set(cellId, open);
    }
    /* textContent, never innerHTML: printed output is data, not markup. */
    open.el.textContent += text;
  } else if (kind === "append") {
    openStreams.delete(cellId);
    const template = document.createElement("template");
    template.innerHTML = markup;
    el.appendChild(template.content);
  } else if (kind === "clear") {
    openStreams.delete(cellId);
    el.replaceChildren();
  }
}

/* Clears a cell's own output area for a fresh run, and forgets any open
 * stream <pre> for it so the next output event starts a new one rather
 * than appending to a node that no longer exists post-render. */
export function clearOutput(cellId) {
  openStreams.delete(cellId);
  const el = getOutputEl ? getOutputEl(cellId) : null;
  if (el) el.replaceChildren();
}

/* ---------------------------------------------------------- Worker path */

let worker = null; // the Worker object itself, once created
let interruptBuffer = null; // shared memory used to signal "stop running" (see requestInterrupt below)
let jediReadyWorker = false; // has the worker finished loading Jedi (autocomplete) yet?
let nextRequestId = 1; // counts up so every request gets a unique id
const pendingRequests = new Map(); // id -> {resolve, reject}

/**
 * Sends one message to the worker and returns a Promise for its reply.
 *
 * A Web Worker is a separate thread with its own memory — the only way to
 * talk to it is by sending plain messages back and forth with
 * postMessage(), and there's no built-in way to say "send this message
 * and give me back the answer" the way a normal function call would. This
 * function builds that on top of postMessage: it invents a unique `id`
 * for the request, remembers a {resolve, reject} pair for that id in
 * pendingRequests, and sends the message. Later, when the worker's
 * onmessage handler (in ensureWorker below) sees a "response" message
 * with a matching id, it looks up that same pair and calls resolve() or
 * reject() — which is what actually fulfills the Promise this function
 * returned. Every request the worker understands (booting, running a
 * cell, autocomplete lookups, filesystem operations) goes through this
 * one function.
 */
function workerRequest(type, payload) {
  const id = nextRequestId++;
  return new Promise((resolve, reject) => {
    pendingRequests.set(id, { resolve, reject });
    worker.postMessage({ type, id, ...payload });
  });
}

/**
 * Creates the Worker the first time it's needed, and does nothing on
 * later calls (that's the "ensure" in the name — make sure it exists,
 * don't recreate it). Also sets up the *one* place this file listens for
 * messages coming back from the worker; every kind of message the worker
 * can send is handled right here:
 *   - "status": a plain progress message ("Loading numpy…") to show the
 *     user while Python is booting.
 *   - "jedi-ready": the worker finished loading the autocomplete library
 *     in the background; nothing needs to happen except remembering it.
 *   - "output": a cell printed something or produced a result — handed
 *     straight to applyOutputEvent to turn into DOM.
 *   - "response": the answer to a specific workerRequest() call, matched
 *     up by its id and used to resolve (or reject, if the worker reports
 *     an error) that call's Promise.
 */
function ensureWorker() {
  if (worker) return;
  worker = new Worker(new URL("./pyodide-worker.js", import.meta.url), { type: "module" });
  worker.onmessage = (ev) => {
    const msg = ev.data;
    if (msg.type === "status") {
      setStatus(msg.text);
    } else if (msg.type === "jedi-ready") {
      jediReadyWorker = true;
    } else if (msg.type === "output") {
      applyOutputEvent(msg.cellId, msg.kind, msg.cssClass, msg.text, msg.markup);
    } else if (msg.type === "response") {
      const pending = pendingRequests.get(msg.id);
      if (!pending) return;
      pendingRequests.delete(msg.id);
      if ("error" in msg) pending.reject(new Error(msg.error));
      else pending.resolve(msg.result);
    }
  };
}

/* Creates the worker (if needed) and asks it to actually boot Python:
 * download Pyodide, load the packages this page wants, and load
 * tutorial_tools.py so cells have show()/show_table()/etc. available.
 * Once that resolves, Python is ready and the worker can run cells. */
async function bootWorker() {
  ensureWorker();
  await workerRequest("boot", {
    pyodideBase: pyodideBase(),
    packages,
    toolsSourceUrl: assetUrl("tutorial_tools.py"),
    dataBase,
  });

  if (globalThis.crossOriginIsolated && typeof SharedArrayBuffer !== "undefined") {
    interruptBuffer = new SharedArrayBuffer(4);
    worker.postMessage({ type: "set-interrupt-buffer", buffer: interruptBuffer });
  }
}

/* This is how the Stop button actually stops a running cell. Normally,
 * two threads (the main page and the worker) can only talk by sending
 * whole messages back and forth — but a *running* Python loop isn't
 * checking for new messages, it's just running. SharedArrayBuffer is
 * special: it's a block of memory both threads can see and write to
 * instantly, with no message-passing needed. Pyodide checks this buffer
 * periodically while Python code runs, so setting byte 0 to 2 (Pyodide's
 * own convention for "this means SIGINT / Ctrl-C") is enough to make a
 * runaway `while True: pass` cell stop on its own, without waiting for it
 * to finish. If the browser never handed out a SharedArrayBuffer in the
 * first place (see bootWorker above — that needs cross-origin isolation),
 * interruptBuffer stays null and there's simply no way to interrupt; the
 * Stop button won't offer to in that case (see canStop() further down). */
function requestInterrupt() {
  if (!interruptBuffer) return;
  /* 2 is SIGINT in Pyodide's own interrupt-buffer convention. */
  new Int32Array(interruptBuffer)[0] = 2;
}

/* Asks the worker to run one cell's code and waits for the result. All of
 * the actual output (prints, tables, images) arrives separately as
 * "output" messages handled in ensureWorker's onmessage above — this
 * Promise only resolves once the cell has finished (or raised), the same
 * way tutorial_tools.py's run_cell always does. */
async function runCellWorker(cellId, code) {
  return workerRequest("run-cell", { cellId, code });
}

/* The worker counterpart of resetPageStateMT() — asks pyodide-worker.js's
 * own "reset-page-state" handler to clear and re-seed the shared
 * namespace inside the worker, the same two steps done there since the
 * worker owns Pyodide entirely on this path. */
async function resetPageStateWorker() {
  await workerRequest("reset-page-state", {});
}

/* -------------------------------------------------- Main-thread fallback */

/* Everything with an "MT" suffix below belongs to the main-thread fallback
 * path — these hold the live Python objects Pyodide gives back once it's
 * running directly in the page (as opposed to the worker path above,
 * where Python only exists inside the worker and this file never touches
 * it directly, only through postMessage). */
let pyodideMT = null; // the Pyodide interpreter itself
let toolsMT = null; // the imported tutorial_tools Python module
let inspectModuleMT = null; // Python's own `inspect` module, for hover docs
let builtinsModuleMT = null; // Python's `builtins` module, for looking up e.g. `len`
let jediHoverFnMT = null; // the _dewlab_hover_doc Python function defined below
let jediSignatureFnMT = null; // the _dewlab_signature Python function defined below

/* Jedi is a Python library that can look at a piece of source code and
 * figure out what a name refers to — the same kind of analysis an IDE
 * uses for "go to definition" or a tooltip showing a function's
 * docstring, but done statically (by reading the code) rather than by
 * actually running it. This string is real Python source code, defining
 * two small helper functions that wrap Jedi's API in a simpler shape:
 * "given this source text and a line/column position, give me back a doc
 * string (or a signature string), or None if there isn't one." It gets
 * run once, in loadJediMT() below, and the two functions it defines are
 * then grabbed and kept as jediHoverFnMT/jediSignatureFnMT so JavaScript
 * can call them directly without re-parsing this string every time. */
const JEDI_HELPER_SOURCE = `
import jedi

def _dewlab_hover_doc(source, line, col):
    try:
        for d in jedi.Script(source).help(line, col):
            doc = d.docstring()
            if doc:
                return doc
    except Exception:
        pass
    return None

def _dewlab_signature(source, line, col):
    try:
        sigs = jedi.Script(source).get_signatures(line, col)
        if sigs:
            return sigs[0].to_string()
    except Exception:
        pass
    return None
`;

/* Loads Jedi and parso (the parsing library Jedi depends on) and runs the
 * helper source above. This is called from bootMainThread() but
 * deliberately *not* awaited there — Jedi is only needed for tooltips on
 * code that hasn't run yet, so there's no reason to make the student wait
 * for it before they can run their first cell. If it fails (a network
 * hiccup, an unsupported browser), autocomplete just falls back to only
 * showing names that already exist in the live namespace — see
 * lookupLiveNameMT below — rather than breaking anything. */
async function loadJediMT() {
  try {
    await pyodideMT.loadPackage(["jedi", "parso"]);
    await pyodideMT.runPythonAsync(JEDI_HELPER_SOURCE);
    jediHoverFnMT = pyodideMT.globals.get("_dewlab_hover_doc");
    jediSignatureFnMT = pyodideMT.globals.get("_dewlab_signature");
  } catch (err) {
    console.warn("pyodide-engine: Jedi failed to load; pre-run tooltips stay live-only", err);
  }
}

/* Looks up a name (like "numpy" or a variable a student defined) among
 * things that actually exist right now — first in the shared page
 * namespace (tutorial_tools._page_globals, the same dict every cell runs
 * against), then in Python's builtins (len, print, and so on) if it
 * wasn't a page-level name. This only finds names for things that have
 * *already run* — it's the "live" counterpart to Jedi's static analysis,
 * which can guess at names in code that hasn't executed yet. */
function lookupLiveNameMT(name) {
  if (!toolsMT || !/^[A-Za-z_]\w*$/.test(name)) return undefined;
  try {
    const local = toolsMT._page_globals.get(name);
    if (local !== undefined) return local;
  } catch {
    /* fall through to builtins */
  }
  if (!builtinsModuleMT) return undefined;
  try {
    return builtinsModuleMT[name];
  } catch {
    return undefined;
  }
}

/* Gets the docstring for a name that already exists (e.g. hovering over
 * "numpy" after `import numpy` has actually run) using Python's own
 * inspect.getdoc — the exact same thing Python's built-in help() uses
 * under the hood. The `finally` block calling .destroy() matters here:
 * Pyodide hands JavaScript a *proxy* object standing in for the real
 * Python object, and proxies need to be destroyed explicitly when done
 * with them, or Pyodide has no way to know the reference is no longer
 * needed and can't free it — a small but real memory leak if skipped. */
function docForMT(name) {
  if (!toolsMT || !inspectModuleMT) return null;
  const obj = lookupLiveNameMT(name);
  if (obj === undefined || obj === null) return null;
  try {
    return inspectModuleMT.getdoc(obj) || null;
  } catch {
    return null;
  } finally {
    if (obj && typeof obj.destroy === "function") obj.destroy();
  }
}

/* Same idea as docForMT, but for a function's *signature* (its name and
 * parameter list, e.g. "sorted(iterable, key=None, reverse=False)")
 * rather than its docstring — used for the little popup that shows while
 * typing inside a function call's parentheses. */
function signatureForMT(name) {
  if (!toolsMT || !inspectModuleMT) return null;
  const obj = lookupLiveNameMT(name);
  if (obj === undefined || obj === null) return null;
  let sig;
  try {
    sig = inspectModuleMT.signature(obj);
    return name + sig.toString();
  } catch {
    return null;
  } finally {
    if (sig && typeof sig.destroy === "function") sig.destroy();
    if (obj && typeof obj.destroy === "function") obj.destroy();
  }
}

/* The Jedi counterpart to docForMT: works on code that hasn't run yet, by
 * reading the source text itself rather than looking up a live object.
 * This is what makes hovering over `numpy.arr` (before `arr` has been
 * defined, or even before the cell has run) still able to show something
 * useful, as long as Jedi can figure it out from the code alone. */
function jediDocMT(source, line, col) {
  if (!jediHoverFnMT) return null;
  try {
    return jediHoverFnMT(source, line, col) || null;
  } catch {
    return null;
  }
}

/* The Jedi counterpart to signatureForMT — same idea, for a function
 * signature instead of a docstring. */
function jediSignatureMT(source, line, col) {
  if (!jediSignatureFnMT) return null;
  try {
    return jediSignatureFnMT(source, line, col) || null;
  } catch {
    return null;
  }
}

/* Works out the URL Pyodide's own files should be loaded from. Normally
 * that's a CDN (the jsdelivr URL below) — but dewmini's downloadable,
 * offline copy ships its own vendored Pyodide instead
 * (write_dewmini_bundle() in build.py), and that copy sets
 * globalThis.DEWLAB_PYODIDE_BASE before this file ever runs, so the same
 * code works in both cases without needing to know which one it's in. */
function pyodideBase() {
  return new URL(
    globalThis.DEWLAB_PYODIDE_BASE || `https://cdn.jsdelivr.net/pyodide/v0.28.3/full/`,
    document.baseURI
  ).href;
}

/* The main-thread equivalent of bootWorker() above: downloads and starts
 * Pyodide, loads the requested packages, loads tutorial_tools.py, and
 * (unlike the worker path) sets up a plain Python dict, _page_globals,
 * that every cell shares — the closest main-thread equivalent of the
 * persistent interpreter state a worker naturally keeps between
 * run-cell calls. This path is only used when a real Worker can't be
 * created (see boot() further down), most commonly a page opened
 * directly from disk via file://. */
async function bootMainThread() {
  setStatus("Starting Python…");

  const base = pyodideBase();
  const loadPyodideFn = globalThis.loadPyodide || (await import(/* @vite-ignore */ base + "pyodide.mjs")).loadPyodide;
  pyodideMT = await loadPyodideFn({ indexURL: base });

  setStatus(`Loading ${packages.join(", ")}…`);
  await pyodideMT.loadPackage(packages);
  // Separately, and forgivingly: a Pyodide without this package must still
  // boot. See NETWORK_PATCH_SOURCE for what it buys.
  try {
    await pyodideMT.loadPackage(["pyodide-http"]);
    await pyodideMT.runPythonAsync(NETWORK_PATCH_SOURCE);
  } catch {
    /* no browser-backed urllib; tutorial_tools.py's hints cover it */
  }

  setStatus("Preparing the notebook tools…");
  const source = await fetch(assetUrl("tutorial_tools.py")).then((r) => {
    if (!r.ok) throw new Error(`tutorial_tools.py: HTTP ${r.status}`);
    return r.text();
  });
  pyodideMT.FS.writeFile("/home/pyodide/tutorial_tools.py", source, { encoding: "utf8" });
  toolsMT = pyodideMT.pyimport("tutorial_tools");
  inspectModuleMT = pyodideMT.pyimport("inspect");
  builtinsModuleMT = pyodideMT.pyimport("builtins");
  toolsMT.configure(dataBase);

  await pyodideMT.runPythonAsync(RESEED_GLOBALS_SOURCE);

  setStatus("");
  loadJediMT(); // deliberately not awaited — must not delay the first Run
}

/* Re-seeds the shared namespace exactly the way boot's own first pass
 * does — every name in tutorial_tools.__all__, plus __name__ — without
 * re-running the rest of boot(). Used by resetPageState() below, which
 * clears _page_globals first (reset_page_state() itself) and then needs
 * this to put the always-available names right back, the same as they
 * were right after boot but with none of a reader's own leftover state. */
async function resetPageStateMT() {
  toolsMT.reset_page_state();
  await pyodideMT.runPythonAsync(RESEED_GLOBALS_SOURCE);
}

/* Lists every name currently defined in the shared namespace, for
 * autocomplete — the main-thread counterpart of the worker's "page-names"
 * message. Names starting with "_" (Python's own convention for
 * "private, not meant to be used from outside") are filtered out so
 * autocomplete doesn't suggest internal bookkeeping names alongside a
 * student's own variables. */
function pageNamesMT() {
  if (!toolsMT) return [];
  return [...toolsMT._page_globals.keys()].filter((name) => !name.startsWith("_"));
}

/* The main-thread counterpart of the worker's "describe-globals" — see
 * that handler's own comment for why the proxy needs converting and
 * destroying. */
function describeGlobalsMT() {
  if (!toolsMT) return [];
  const proxy = toolsMT.describe_globals();
  const described = proxy.toJs({ dict_converter: Object.fromEntries });
  proxy.destroy();
  return described;
}

/* Runs one cell's code directly, on the main thread. tutorial_tools.py's
 * own run_cell() does essentially everything here — running the code,
 * capturing output, rendering it into `el` — so this function is mostly
 * just "find the right output element and hand off to Python." The
 * `{ ok }` return shape matches what runCellWorker's response looks like,
 * so the exported runCell() further down can treat both paths the same
 * way without caring which one actually ran. */
async function runCellMainThread(cellId, code) {
  const el = getOutputEl ? getOutputEl(cellId) : null;
  const ok = await toolsMT.run_cell(cellId, el, code);
  return { ok };
}

/* Filesystem, main-thread mirror of the worker's fs-* handlers in
 * pyodide-worker.js — same Pyodide FS calls, just made directly since
 * pyodideMT lives right here instead of across a postMessage boundary. */
let mountedFsMT = null; // whatever mount object the active backend gave back, so fsSyncMT knows how to sync it

/* Connects a real folder on the student's own computer (chosen through
 * the browser's folder picker, handled by the page's own fs module — see
 * compose/dewmini-fs.js) to Pyodide's virtual
 * filesystem at `mountpoint`. mkdirTree makes sure the mount point itself
 * exists first — Pyodide can't mount onto a path that isn't there. After
 * this, Python code doing e.g. open(f'{mountpoint}/x.csv') is reading and
 * writing the real file on disk. */
async function fsMountNativeMT(mountpoint, handle) {
  pyodideMT.FS.mkdirTree(mountpoint);
  mountedFsMT = await pyodideMT.mountNativeFS(mountpoint, handle);
}

/* The fallback for browsers that don't support picking a real folder
 * (Firefox, Safari): OPFS (Origin Private File System) is storage the
 * browser manages for this site alone. It isn't visible in the normal
 * file browser, but it behaves like a real folder from Pyodide's point of
 * view and survives page reloads, so the same mountNativeFS() call used
 * for a real folder works here too — Pyodide can't tell the difference. */
async function fsMountOpfsMT(mountpoint) {
  const opfsRoot = await navigator.storage.getDirectory();
  pyodideMT.FS.mkdirTree(mountpoint);
  mountedFsMT = await pyodideMT.mountNativeFS(mountpoint, opfsRoot);
}

/* The last-resort fallback: IDBFS, Pyodide's own filesystem backed by
 * IndexedDB (a database the browser gives every site). Unlike the two
 * mounts above, IDBFS needs an explicit two-way sync step
 * (FS.syncfs) rather than writing straight through, so this function
 * does one sync immediately after mounting (the `true` argument means
 * "load from storage into memory") and hands back a matching syncfs
 * object so later saves (fsSyncMT) know how to push changes back out
 * (`false` there means "save from memory to storage"). */
async function fsMountIdbfsMT(mountpoint) {
  pyodideMT.FS.mkdirTree(mountpoint);
  pyodideMT.FS.mount(pyodideMT.FS.filesystems.IDBFS, {}, mountpoint);
  await new Promise((resolve, reject) => {
    pyodideMT.FS.syncfs(true, (err) => (err ? reject(err) : resolve()));
  });
  mountedFsMT = {
    syncfs: () =>
      new Promise((resolve, reject) => {
        pyodideMT.FS.syncfs(false, (err) => (err ? reject(err) : resolve()));
      }),
  };
}

/* Flushes any pending filesystem changes out to real storage. A no-op for
 * the native-folder and OPFS backends (they write through immediately),
 * but essential for IDBFS — without calling this, changes only exist in
 * Pyodide's in-memory copy and would be lost on reload. */
async function fsSyncMT() {
  if (mountedFsMT) await mountedFsMT.syncfs();
}

/* Detaches whatever's currently mounted at `path`, needed before mounting
 * a *different* backend at the same mount point (e.g. switching from
 * OPFS to a real folder once the student grants permission). */
function fsUnmountMT(path) {
  pyodideMT.FS.unmount(path);
  mountedFsMT = null;
}

/* Lists the contents of a directory in the mounted filesystem, in the
 * shape the file-tree UI wants: name, whether it's a folder, and its size
 * in bytes. "." and ".." (the filesystem's own self/parent entries) are
 * filtered out since the file tree has no use for them. */
function fsListMT(path) {
  const names = pyodideMT.FS.readdir(path).filter((n) => n !== "." && n !== "..");
  return names.map((name) => {
    const stat = pyodideMT.FS.stat(`${path.replace(/\/$/, "")}/${name}`);
    return { name, isDir: pyodideMT.FS.isDir(stat.mode), size: stat.size };
  });
}

/* Reads one file. Passing `encoding` (e.g. "utf8") gets a JavaScript
 * string back; omitting it gets the raw bytes as a Uint8Array, which is
 * what image/binary files need. */
function fsReadMT(path, encoding) {
  return pyodideMT.FS.readFile(path, encoding ? { encoding } : undefined);
}

/* Writes (or overwrites) one file with `data`, which can be a string or
 * raw bytes. */
function fsWriteMT(path, data) {
  pyodideMT.FS.writeFile(path, data);
}

/* Deletes a file or an empty directory. Has to check which one it's
 * looking at first: Pyodide's FS (like most filesystems) uses a different
 * call for removing a directory (rmdir) than for removing a file
 * (unlink), and using the wrong one raises an error instead of working. */
function fsDeleteMT(path) {
  const stat = pyodideMT.FS.stat(path);
  if (pyodideMT.FS.isDir(stat.mode)) pyodideMT.FS.rmdir(path);
  else pyodideMT.FS.unlink(path);
}

/* Creates a directory, including any missing parent directories along the
 * way (that's what "Tree" means in mkdirTree — mkdir alone would fail if
 * the parent folder didn't already exist). */
function fsMkdirMT(path) {
  pyodideMT.FS.mkdirTree(path);
}

/* ------------------------------------------------------- the dispatcher */

let mode = null; // "worker" | "main-thread", set once boot() resolves
let bootPromise = null;

/* Decides which of the two paths above (worker or main-thread) this page
 * actually gets, and tries them in order of preference: a real Worker
 * first, since it gives a genuine Stop button and never freezes the page
 * even on a runaway loop, and only falls back to running Python directly
 * on the main thread if creating a Worker fails outright (which happens,
 * for example, on a page opened straight from disk via file://, where
 * some browsers restrict module Workers). Once one path succeeds, `mode`
 * records which one it was, and every other exported function in this
 * file checks `mode` to know which set of MT/worker functions to call. */
async function boot() {
  if (typeof Worker !== "undefined") {
    try {
      await bootWorker();
      mode = "worker";
      return;
    } catch (err) {
      console.warn("pyodide-engine: Worker boot failed, falling back to the main thread", err);
    }
  }
  await bootMainThread();
  mode = "main-thread";
}

/**
 * The single entry point a page calls to make sure Python is
 * running, before doing anything that needs it (running a cell, mounting
 * a filesystem). Booting is slow and should only ever happen once, so
 * this caches the *Promise* from the first call in bootPromise — a second
 * call while booting is still in progress gets back that same Promise
 * (and so just waits for the same boot to finish) rather than starting a
 * second, wasted boot. If booting fails, bootPromise is reset to null so
 * that the *next* call (e.g. after the student clicks Run again) gets a
 * fresh attempt instead of being stuck replaying the same failure
 * forever.
 */
export function ensureBooted() {
  if (!bootPromise) {
    bootPromise = boot().catch((err) => {
      bootPromise = null; // let a retry (e.g. a later Run click) try again
      throw err;
    });
  }
  return bootPromise;
}

/**
 * Tears down whatever's running — the Worker if one exists, or just the
 * main-thread references — so the next ensureBooted() starts a genuinely
 * fresh interpreter. For recovering from a corrupted namespace or a
 * runaway loop the Stop button couldn't reach. Anything mounted into the
 * old interpreter's filesystem (the page's own fs module) goes with it —
 * the caller is responsible for re-mounting after the restart resolves.
 */
export function restart() {
  if (worker) {
    try {
      worker.terminate();
    } catch {
      // already gone
    }
  }
  worker = null;
  interruptBuffer = null;
  jediReadyWorker = false;

  /* Reject what was in flight before dropping it. Terminating the worker
   * means no reply is ever coming for these, and a promise that neither
   * resolves nor rejects is not "cancelled" — it hangs forever, and so does
   * whatever awaited it. A caller's `finally` never runs, so a "running"
   * guard set before the await stays set, and every later Run is silently
   * ignored until the page is reloaded. That is precisely the state this
   * button exists to get someone out of. */
  for (const { reject } of pendingRequests.values()) {
    reject(new Error("Python was restarted before this finished."));
  }
  pendingRequests.clear();
  openStreams.clear();

  mountedFsMT = null;
  pyodideMT = null;
  toolsMT = null;
  inspectModuleMT = null;
  builtinsModuleMT = null;
  jediHoverFnMT = null;
  jediSignatureFnMT = null;

  mode = null;
  bootPromise = null;
}

/* Tells the caller which path booted successfully, so the UI (Settings'
 * engine-status section, for one) can show it honestly rather than
 * assuming the worker always wins. */
export function engineMode() {
  return mode;
}

/* True only when a Stop button would actually do something: the worker
 * path is active *and* the browser handed out a SharedArrayBuffer to
 * signal it with (see requestInterrupt above for why that's needed). The
 * main-thread path can never be stopped once a cell starts running — a
 * synchronous loop on the same thread as everything else blocks that
 * thread completely, with no opportunity for an interrupt request to even
 * be noticed. */
export function canStop() {
  return mode === "worker" && interruptBuffer !== null;
}

export { requestInterrupt };

/* The one function a page actually calls to run a cell — it doesn't
 * need to know or care whether Python is running in a worker or on the
 * main thread. Output from the *previous* run is cleared first so a
 * re-run doesn't show old results mixed in with new ones, then execution
 * is handed off to whichever path actually booted. */
export async function runCell(cellId, code) {
  clearOutput(cellId);
  if (mode === "main-thread") return runCellMainThread(cellId, code);
  return runCellWorker(cellId, code);
}

/* Clears the shared namespace and re-seeds it with the always-available
 * names, without a full restart()+re-boot — for a page's own "Run all"
 * wanting every cell to run against the same clean slate a reader would
 * get from a fresh page load, so a name an earlier cell defined and a
 * later cell still depends on (even though it's no longer in the
 * notebook) can't silently mask that kind of mistake. Cheaper than
 * restart(): the interpreter itself, and anything mounted into its
 * filesystem, stay exactly as they were. */
export async function resetPageState() {
  if (mode === "main-thread") return resetPageStateMT();
  return resetPageStateWorker();
}

/* ---- code intelligence: what vendor-src/codemirror-entry.js calls ---- */

/* Looks up documentation for the name under the cursor, for CodeMirror's
 * hover tooltip. Two different sources are tried depending on which path
 * booted: on the main thread, a *live* object is checked first (whatever
 * that name actually refers to right now, if the cell defining it has
 * already run) and Jedi's static analysis is used only as a fallback for
 * names that haven't run yet; on the worker path, both of those checks
 * happen inside pyodide-worker.js itself, so this just forwards the
 * request and waits for its answer. */
async function hoverDoc(name, source, line, col) {
  if (mode === "main-thread") return docForMT(name) || jediDocMT(source, line, col);
  if (!worker) return null;
  return workerRequest("hover-doc", { name, source, line, col });
}

/* Same live-then-static idea as hoverDoc, but for a function's signature
 * (used for the little "which argument am I on" popup while typing inside
 * a function call). */
async function signatureHelp(name, source, line, col, argIndex) {
  void argIndex; // CodeMirror bolds the argument itself; not needed here
  if (mode === "main-thread") return signatureForMT(name) || jediSignatureMT(source, line, col);
  if (!worker) return null;
  return workerRequest("signature-help", { name, source, line, col });
}

export { hoverDoc, signatureHelp };

/* Every name currently defined in the shared page namespace —
 * tutorial_tools._page_globals, the same dict every cell actually runs
 * against — so what's offered is exactly what a cell could reference
 * right now. Async because the Worker path is a real round trip;
 * CodeMirror's completion sources accept a Promise natively. */
export async function pageNamesCompletion(context) {
  const word = context.matchBefore(/\w+/);
  if (!word || (word.from === word.to && !context.explicit)) return null;
  const names = mode === "main-thread"
    ? pageNamesMT()
    : worker
      ? await workerRequest("page-names", {})
      : [];
  if (!names.length) return null;
  return { from: word.from, options: names.map((label) => ({ label, type: "variable" })) };
}

/* What is currently defined in the shared namespace, each with its type and
 * a one-line summary of its value — what dewmini's Workbench shows, so a
 * reader can see what their code actually made rather than only what they
 * remembered to print.
 *
 * Returns `[]` rather than throwing when Python has not booted: the panel
 * asking before the first run is an ordinary thing to happen, not an
 * error worth a message. */
export async function describeGlobals() {
  if (mode === "main-thread") return describeGlobalsMT();
  if (!worker) return [];
  return workerRequest("describe-globals", {});
}

/* ------------------------------------------------------------- filesystem
 *
 * The page's own fs module (compose/dewmini-fs.js) is the only caller
 * of everything below: it owns backend selection
 * (native folder vs. OPFS vs. IDBFS) and calls these once it has decided.
 * Every function here assumes ensureBooted() has already resolved —
 * Pyodide's FS doesn't exist before that. */

/* Every exported function from here down follows the exact same shape:
 * if the main-thread path is active, call the matching *MT function
 * directly (it's running right here, in the same thread); otherwise send
 * a matching request across to the worker and wait for its reply. This
 * mirrors runCell()'s dispatch above, and it's why every fs*MT function
 * earlier in this file and every "fs-*" message pyodide-worker.js
 * understands come in matching pairs — the page's own fs module (the
 * only caller of any of these) never needs to know which path is
 * active. */

/* Mounts a real folder the student picked (via the browser's folder
 * picker) at `mountpoint`. */
export async function mountNative(mountpoint, handle) {
  if (mode === "main-thread") return fsMountNativeMT(mountpoint, handle);
  return workerRequest("fs-mount-native", { mountpoint, handle });
}

/* Mounts the OPFS fallback (private browser storage) at `mountpoint`. */
export async function mountOpfs(mountpoint) {
  if (mode === "main-thread") return fsMountOpfsMT(mountpoint);
  return workerRequest("fs-mount-opfs", { mountpoint });
}

/* Mounts the IDBFS last-resort fallback at `mountpoint`. */
export async function mountIdbfs(mountpoint) {
  if (mode === "main-thread") return fsMountIdbfsMT(mountpoint);
  return workerRequest("fs-mount-idbfs", { mountpoint });
}

/* Flushes any pending writes out to real storage (only meaningfully does
 * anything for the IDBFS backend — see fsSyncMT above). */
export async function syncFs() {
  if (mode === "main-thread") return fsSyncMT();
  return workerRequest("fs-sync", {});
}

/* Required before mounting a different backend at the same mountpoint. */
export async function unmount(mountpoint) {
  if (mode === "main-thread") return fsUnmountMT(mountpoint);
  return workerRequest("fs-unmount", { mountpoint });
}

/* Lists a directory's contents for the file-tree UI. */
export async function listDir(path) {
  if (mode === "main-thread") return fsListMT(path);
  return workerRequest("fs-list", { path });
}

/**
 * @param {string} path
 * @param {"utf8"} [encoding] - omit for raw bytes (a Uint8Array comes
 *   back either way; Uint8Array is structured-cloneable, so the worker
 *   path needs no extra encoding step for binary files).
 */
export async function readFile(path, encoding) {
  if (mode === "main-thread") return fsReadMT(path, encoding);
  return workerRequest("fs-read", { path, encoding });
}

/* Writes (or overwrites) one file. */
export async function writeFile(path, data) {
  if (mode === "main-thread") return fsWriteMT(path, data);
  return workerRequest("fs-write", { path, data });
}

/* Deletes a file or empty directory. */
export async function deleteFile(path) {
  if (mode === "main-thread") return fsDeleteMT(path);
  return workerRequest("fs-delete", { path });
}

/* Creates a directory (and any missing parent directories). */
export async function mkdir(path) {
  if (mode === "main-thread") return fsMkdirMT(path);
  return workerRequest("fs-mkdir", { path });
}
