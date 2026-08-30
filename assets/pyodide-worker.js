/* Pyodide, off the main thread — planning/CELL_CONTROLS.md §2, "Run"
 * becoming "Stop" while a cell runs.
 *
 * Everything that used to call `pyodide`/`tools`/`inspectModule` directly
 * from tutorial-runtime.js lives here instead: booting the interpreter,
 * running a cell, and the code-intelligence lookups (hover docs, signature
 * help, live-namespace completion) tutorial-runtime.js's CodeMirror
 * extensions ask for. tutorial-runtime.js now only ever talks to this file
 * through postMessage — see its own `WORKER_MODE` section for the client
 * half of this protocol.
 *
 * Only the hosted site runs this way. The standalone/offline export keeps
 * the pre-Worker, main-thread path unchanged: a `file://`-opened page can
 * run into real restrictions loading a module Worker at all, and nothing
 * about working offline needs a genuine Stop button on top of solving that
 * problem too (DECISIONS_LOG.md 7.77).
 *
 * Absolute URLs throughout, never the page-relative ones the manifest
 * itself carries: a relative fetch from *this* file resolves against this
 * file's own location, not the tutorial page's, so tutorial-runtime.js
 * resolves everything to an absolute URL before it ever reaches a message
 * here.
 */

/* This whole file runs inside a Web Worker, not on the page itself — a
 * separate thread with its own memory, created by `new Worker(...)` on
 * the page side (see pyodide-engine.js's ensureWorker(), or
 * tutorial-runtime.js's own equivalent). That's what makes a genuine
 * Stop button possible: even if Python code here runs forever, the page
 * itself stays responsive, since it's a different thread entirely. The
 * only way in or out is postMessage()/onmessage — there's no shared
 * memory to just reach into (SharedArrayBuffer, used for Stop further
 * down, is the one deliberate exception). */

let pyodide = null; // the Pyodide interpreter, once boot() finishes
let tools = null; // the imported tutorial_tools Python module
let inspectModule = null; // Python's `inspect` module, for hover docs
let builtinsModule = null; // Python's `builtins` module, for e.g. `len`

let jediHoverFn = null; // the _dewlab_hover_doc Python function, defined below
let jediSignatureFn = null; // the _dewlab_signature Python function, defined below

/* A tiny wrapper around the Worker's own global postMessage() — just
 * gives the rest of this file one consistent name to call. */
function post(message) {
  postMessage(message);
}

/* A name from the page's own live namespace first, a Python builtin second
 * — never shadowing a student's own name of the same spelling. Ported
 * unchanged from the pre-Worker tutorial-runtime.js (DECISIONS_LOG.md
 * 7.76); only where it runs has moved. */
function lookupLiveName(name) {
  /* The regex check guards against handing an arbitrary string straight
   * into a dict/attribute lookup below — only something that could
   * actually be a Python identifier (letters, digits, underscores, not
   * starting with a digit) is worth looking up at all. */
  if (!tools || !/^[A-Za-z_]\w*$/.test(name)) return undefined;
  try {
    const local = tools._page_globals.get(name);
    if (local !== undefined) return local;
  } catch {
    /* fall through to builtins */
  }
  if (!builtinsModule) return undefined;
  try {
    return builtinsModule[name];
  } catch {
    return undefined;
  }
}

/* Gets the docstring for a name that has already run (e.g. hovering over
 * "numpy" once `import numpy` has actually executed), using Python's own
 * inspect.getdoc — the same thing behind Python's built-in help(). The
 * `finally` block's `.destroy()` calls matter: Pyodide hands JavaScript a
 * *proxy* standing in for the real Python object, and a proxy has to be
 * destroyed explicitly once it's no longer needed, or Pyodide has no way
 * to know it can free the memory — otherwise a small leak on every hover. */
function docFor(name) {
  if (!tools || !inspectModule) return null;
  const obj = lookupLiveName(name);
  if (obj === undefined || obj === null) return null;
  try {
    return inspectModule.getdoc(obj) || null;
  } catch {
    return null;
  } finally {
    if (obj && typeof obj.destroy === "function") obj.destroy();
  }
}

/* Same idea as docFor, but for a function's signature (its name and
 * parameter list) rather than its docstring. */
function signatureFor(name) {
  if (!tools || !inspectModule) return null;
  const obj = lookupLiveName(name);
  if (obj === undefined || obj === null) return null;
  let sig;
  try {
    sig = inspectModule.signature(obj);
    return name + sig.toString();
  } catch {
    return null;
  } finally {
    if (sig && typeof sig.destroy === "function") sig.destroy();
    if (obj && typeof obj.destroy === "function") obj.destroy();
  }
}

/* The Jedi counterpart to docFor: works on code that hasn't run yet, by
 * reading the source text itself (via the _dewlab_hover_doc Python
 * helper defined in JEDI_HELPER_SOURCE below) rather than looking up a
 * live object. */
function jediDoc(source, line, col) {
  if (!jediHoverFn) return null;
  try {
    return jediHoverFn(source, line, col) || null;
  } catch {
    return null;
  }
}

/* The Jedi counterpart to signatureFor. */
function jediSignature(source, line, col) {
  if (!jediSignatureFn) return null;
  try {
    return jediSignatureFn(source, line, col) || null;
  } catch {
    return null;
  }
}

/* Live always wins; Jedi only fills the gap live cannot reach — the same
 * composition tutorial-runtime.js's hoverDoc()/signatureHelp() used to do
 * on the main thread. Done here, worker-side, in one message round trip
 * rather than two, since both halves now live on the same side of the
 * postMessage boundary anyway. */
function hoverDoc(name, source, line, col) {
  return docFor(name) || jediDoc(source, line, col);
}

function signatureHelp(name, source, line, col) {
  return signatureFor(name) || jediSignature(source, line, col);
}

/* Lists every name currently defined in the shared page namespace, for
 * autocomplete — names starting with "_" (Python's own convention for
 * "private, internal") are filtered out so autocomplete only offers
 * things a student would actually want to type. */
function pageNames() {
  if (!tools) return [];
  try {
    return [...tools._page_globals.keys()].filter((name) => !name.startsWith("_"));
  } catch {
    return [];
  }
}

/* What is defined in the shared namespace, with each value's type and a
 * one-line summary — dewmini's variable inspector. The work happens in
 * Python (tutorial_tools.describe_globals(), which is where _page_globals
 * lives and which is unit-testable under plain CPython); this only
 * converts the result across the language boundary.
 *
 * `.toJs()` with a Map converter, because Pyodide hands back a list of
 * Python dicts, and a dict becomes a JS Map by default rather than a
 * plain object — which structured-clones fine but reads as empty from
 * the other side of postMessage once JSON-shaped code expects `.name`.
 * `destroy()` releases the proxy: a describe on every run would
 * otherwise leak one proxy per call for the life of the worker. */
function describeGlobals() {
  if (!tools) return [];
  try {
    const proxy = tools.describe_globals();
    const described = proxy.toJs({ dict_converter: Object.fromEntries });
    proxy.destroy();
    return described;
  } catch {
    return [];
  }
}

/* Real Python source code, defining two small helper functions on top of
 * Jedi — the library that does static analysis of Python source (working
 * out what a name probably refers to by reading the code, without
 * running it). This string gets run once, in loadJedi() below, and the
 * two functions it defines are then grabbed and kept in jediHoverFn/
 * jediSignatureFn so JavaScript can call them directly afterward. */
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

/* Loads Jedi and parso (the parser Jedi depends on) and runs the helper
 * source above. Called from boot() below, but deliberately not awaited
 * there — Jedi is only needed for tooltips on code that hasn't run yet,
 * so a student shouldn't have to wait for it before running their first
 * cell. If it fails, autocomplete simply falls back to only offering
 * names that already exist in the live namespace (lookupLiveName above),
 * rather than breaking anything. */
async function loadJedi() {
  try {
    await pyodide.loadPackage(["jedi", "parso"]);
    await pyodide.runPythonAsync(JEDI_HELPER_SOURCE);
    jediHoverFn = pyodide.globals.get("_dewlab_hover_doc");
    jediSignatureFn = pyodide.globals.get("_dewlab_signature");
    post({ type: "jedi-ready" });
  } catch (err) {
    console.warn("dewlab worker: Jedi failed to load; pre-run tooltips stay live-only", err);
  }
}

/* Puts every name in tutorial_tools.__all__ into the shared namespace,
 * plus __name__ — run once at the end of boot() below, and again by
 * resetPageState() further down after tools.reset_page_state() clears
 * that namespace out, so the always-available names come right back
 * without needing a full re-boot. */
const RESEED_GLOBALS_SOURCE = `
import tutorial_tools
tutorial_tools._page_globals.update({
    name: getattr(tutorial_tools, name)
    for name in tutorial_tools.__all__
})
tutorial_tools._page_globals["__name__"] = "__dewlab__"
`;

/* Starts Python from scratch: downloads and initializes Pyodide, loads
 * the requested packages, loads tutorial_tools.py (giving cells access to
 * show()/show_table()/check()/etc.), and sets up the shared page
 * namespace every cell in this worker will run against. `msg` is the
 * "boot" message from the page — see the fields it reads below for what
 * the page side has to provide. Status updates are posted along the way
 * so the page can show real progress rather than one long silent wait. */
async function boot(msg) {
  post({ type: "status", text: "Starting Python…" });
  const { loadPyodide } = await import(/* @vite-ignore */ msg.pyodideBase + "pyodide.mjs");
  pyodide = await loadPyodide({ indexURL: msg.pyodideBase });

  post({ type: "status", text: `Loading ${msg.packages.join(", ")}…` });
  await pyodide.loadPackage(msg.packages);

  post({ type: "status", text: "Preparing the notebook tools…" });
  const source = await fetch(msg.toolsSourceUrl).then((r) => {
    if (!r.ok) throw new Error(`tutorial_tools.py: HTTP ${r.status}`);
    return r.text();
  });
  pyodide.FS.writeFile("/home/pyodide/tutorial_tools.py", source, { encoding: "utf8" });
  tools = pyodide.pyimport("tutorial_tools");
  inspectModule = pyodide.pyimport("inspect");
  builtinsModule = pyodide.pyimport("builtins");
  tools.configure(msg.dataBase);

  await pyodide.runPythonAsync(RESEED_GLOBALS_SOURCE);

  post({ type: "status", text: "" });

  /* Deliberately not awaited: a slower or blocked Jedi download must never
   * delay the moment a student can click Run. */
  loadJedi();
}

/* Runs one cell's Python code. `emit` is the callback tutorial_tools.py's
 * run_cell() calls every time the cell produces something (printed text,
 * a table, an image) — each call here turns straight into an "output"
 * message posted back to the page, which is what makes output appear
 * *as the cell runs*, one piece at a time, rather than only after it
 * finishes. */
async function runCell(cellId, code) {
  const emit = (kind, cssClass, text, markup) => {
    post({ type: "output", cellId, kind, cssClass, text, markup });
  };
  /* tutorial_tools.run_cell already turns a student's own error into
   * rendered output and returns normally — a throw here would mean
   * something broke in the plumbing itself, not in code a reader wrote,
   * so it is deliberately left to propagate to the uniform error path in
   * onmessage below rather than caught twice. */
  const ok = await tools.run_cell(cellId, emit, code);
  return { ok };
}

/* Clears the shared namespace and re-seeds it with the always-available
 * names — the worker half of pyodide-engine.js's resetPageState(),
 * needed for a page's own "Run all" wanting every cell to run against
 * the same clean slate a fresh page load would give it. */
async function resetPageState() {
  tools.reset_page_state();
  await pyodide.runPythonAsync(RESEED_GLOBALS_SOURCE);
}

/* ---------------------------------------------------------------------
 * Filesystem — dewmini only (via assets/pyodide-engine.js).
 * Tutorial pages never send these message types, so this section is
 * purely additive: nothing here changes what boot()/runCell() above do.
 *
 * `pyodide.mountNativeFS(mountpoint, handle)` is the one Pyodide API that
 * covers both real tiers a dewmini-fs.js caller can ask for — a real
 * FileSystemDirectoryHandle from window.showDirectoryPicker() (obtained
 * on the main thread, since that API needs a window and a user gesture,
 * then handed to this worker over postMessage — a FileSystemHandle is
 * structured-cloneable) and OPFS's own root handle, which this worker can
 * get for itself via navigator.storage.getDirectory() since OPFS is fully
 * available inside a Worker. IDBFS is the last-resort fallback for a
 * browser with neither. Whichever one is mounted, `mountedFs` holds the
 * `{syncfs}` handle fs-sync needs to flush pending writes back out. */
let mountedFs = null; // whatever mount object the active backend gave back, for fsSync() to use

/* Connects a real folder on the student's computer (its handle was
 * obtained on the main thread, via the folder picker, then sent here
 * over postMessage — see the big comment above) to Pyodide's virtual
 * filesystem at `mountpoint`. mkdirTree creates the mount point itself
 * first, since Pyodide can't mount onto a path that doesn't exist yet. */
async function fsMountNative(mountpoint, handle) {
  pyodide.FS.mkdirTree(mountpoint);
  mountedFs = await pyodide.mountNativeFS(mountpoint, handle);
}

/* The fallback for browsers without real-folder support: OPFS (Origin
 * Private File System), storage the browser manages for this site alone.
 * Unlike the native-folder handle, this worker can get OPFS's root
 * directly for itself — no permission prompt, no main-thread round trip
 * needed. */
async function fsMountOpfs(mountpoint) {
  const opfsRoot = await navigator.storage.getDirectory();
  pyodide.FS.mkdirTree(mountpoint);
  mountedFs = await pyodide.mountNativeFS(mountpoint, opfsRoot);
}

/* The last-resort fallback: IDBFS, Pyodide's own filesystem backed by
 * IndexedDB. Unlike the two mounts above, it needs an explicit two-way
 * sync (FS.syncfs) rather than writing straight through — this mounts
 * and does one immediate sync to pull in anything already saved, then
 * hands back a matching syncfs function so fsSync() below knows how to
 * push future changes back out. */
async function fsMountIdbfs(mountpoint) {
  pyodide.FS.mkdirTree(mountpoint);
  pyodide.FS.mount(pyodide.FS.filesystems.IDBFS, {}, mountpoint);
  /* populate=true pulls whatever this origin already saved into the
   * in-memory FS; the mount is otherwise empty. */
  await new Promise((resolve, reject) => {
    pyodide.FS.syncfs(true, (err) => (err ? reject(err) : resolve()));
  });
  mountedFs = {
    syncfs: () =>
      new Promise((resolve, reject) => {
        /* populate=false: write the in-memory FS out to IndexedDB. */
        pyodide.FS.syncfs(false, (err) => (err ? reject(err) : resolve()));
      }),
  };
}

/* Flushes any pending filesystem changes out to real storage. A no-op
 * for native-folder and OPFS backends (they write through immediately);
 * essential for IDBFS, where a write only exists in Pyodide's in-memory
 * copy until this actually runs. */
async function fsSync() {
  if (mountedFs) await mountedFs.syncfs();
}

/* Required before mounting a different backend at the same mountpoint —
 * Emscripten's FS refuses to mount over an already-mounted path (e.g.
 * upgrading from the OPFS default to a student's chosen real folder). */
function fsUnmount(path) {
  pyodide.FS.unmount(path);
  mountedFs = null;
}

/* Lists a directory's contents for the file-tree UI: name, whether it's
 * a folder, and its size in bytes. "." and ".." (the filesystem's own
 * self/parent entries) are filtered out first — the file tree has no use
 * for them. */
function fsList(path) {
  const names = pyodide.FS.readdir(path).filter((n) => n !== "." && n !== "..");
  return names.map((name) => {
    const stat = pyodide.FS.stat(`${path.replace(/\/$/, "")}/${name}`);
    return { name, isDir: pyodide.FS.isDir(stat.mode), size: stat.size };
  });
}

/* Reads one file. Passing `encoding` (e.g. "utf8") gets a string back;
 * omitting it gets raw bytes as a Uint8Array — what a binary/image file
 * needs, and also what's needed here specifically because a Uint8Array
 * is structured-cloneable, so it can travel back across postMessage to
 * the page without any extra encoding step. */
function fsRead(path, encoding) {
  return pyodide.FS.readFile(path, encoding ? { encoding } : undefined);
}

/* Writes (or overwrites) one file with `data` — a string or raw bytes. */
function fsWrite(path, data) {
  pyodide.FS.writeFile(path, data);
}

/* Deletes a file or empty directory — checking which one first, since
 * Pyodide's FS (like most filesystems) uses a different call for each,
 * and using the wrong one raises an error instead of working. */
function fsDelete(path) {
  const stat = pyodide.FS.stat(path);
  if (pyodide.FS.isDir(stat.mode)) pyodide.FS.rmdir(path);
  else pyodide.FS.unlink(path);
}

/* Creates a directory, including any missing parent directories along
 * the way. */
function fsMkdir(path) {
  pyodide.FS.mkdirTree(path);
}

/* One uniform request/response shape for everything that needs an answer:
 * `{type, id, ...}` in, `{type: "response", id, result}` or
 * `{type: "response", id, error}` back. `status`/`jedi-ready`/`output` are
 * the only one-way pushes, posted directly from boot()/runCell() above
 * rather than routed through here. */
self.onmessage = async (ev) => {
  const msg = ev.data;
  const respond = (result) => post({ type: "response", id: msg.id, result });
  const fail = (err) => post({ type: "response", id: msg.id, error: String(err && err.message ? err.message : err) });

  try {
    if (msg.type === "boot") {
      await boot(msg);
      respond("ok");
    } else if (msg.type === "set-interrupt-buffer") {
      /* Hands Pyodide the shared memory the page will write into to
       * request a Stop (see pyodide-engine.js's requestInterrupt() for
       * the page-side half of this). Pyodide checks this buffer
       * periodically while Python code runs, so this one call is what
       * makes the Stop button able to interrupt even a runaway loop —
       * no response needed, since there's nothing to report back yet. */
      pyodide.setInterruptBuffer(new Int32Array(msg.buffer));
    } else if (msg.type === "run-cell") {
      respond(await runCell(msg.cellId, msg.code));
    } else if (msg.type === "reset-page-state") {
      await resetPageState();
      respond("ok");
    } else if (msg.type === "hover-doc") {
      respond(hoverDoc(msg.name, msg.source, msg.line, msg.col));
    } else if (msg.type === "signature-help") {
      respond(signatureHelp(msg.name, msg.source, msg.line, msg.col));
    } else if (msg.type === "page-names") {
      respond(pageNames());
    } else if (msg.type === "describe-globals") {
      respond(describeGlobals());
    } else if (msg.type === "fs-mount-native") {
      await fsMountNative(msg.mountpoint, msg.handle);
      respond("ok");
    } else if (msg.type === "fs-mount-opfs") {
      await fsMountOpfs(msg.mountpoint);
      respond("ok");
    } else if (msg.type === "fs-mount-idbfs") {
      await fsMountIdbfs(msg.mountpoint);
      respond("ok");
    } else if (msg.type === "fs-sync") {
      await fsSync();
      respond("ok");
    } else if (msg.type === "fs-unmount") {
      fsUnmount(msg.mountpoint);
      respond("ok");
    } else if (msg.type === "fs-list") {
      respond(fsList(msg.path));
    } else if (msg.type === "fs-read") {
      respond(fsRead(msg.path, msg.encoding));
    } else if (msg.type === "fs-write") {
      fsWrite(msg.path, msg.data);
      respond("ok");
    } else if (msg.type === "fs-delete") {
      fsDelete(msg.path);
      respond("ok");
    } else if (msg.type === "fs-mkdir") {
      fsMkdir(msg.path);
      respond("ok");
    }
  } catch (err) {
    fail(err);
  }
};
