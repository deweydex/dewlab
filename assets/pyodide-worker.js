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

let pyodide = null;
let tools = null;
let inspectModule = null;
let builtinsModule = null;

let jediHoverFn = null;
let jediSignatureFn = null;

function post(message) {
  postMessage(message);
}

/* A name from the page's own live namespace first, a Python builtin second
 * — never shadowing a student's own name of the same spelling. Ported
 * unchanged from the pre-Worker tutorial-runtime.js (DECISIONS_LOG.md
 * 7.76); only where it runs has moved. */
function lookupLiveName(name) {
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

function jediDoc(source, line, col) {
  if (!jediHoverFn) return null;
  try {
    return jediHoverFn(source, line, col) || null;
  } catch {
    return null;
  }
}

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

function pageNames() {
  if (!tools) return [];
  try {
    return [...tools._page_globals.keys()].filter((name) => !name.startsWith("_"));
  } catch {
    return [];
  }
}

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

  await pyodide.runPythonAsync(`
import tutorial_tools
tutorial_tools._page_globals.update({
    name: getattr(tutorial_tools, name)
    for name in tutorial_tools.__all__
})
tutorial_tools._page_globals["__name__"] = "__dewlab__"
`);

  post({ type: "status", text: "" });

  /* Deliberately not awaited: a slower or blocked Jedi download must never
   * delay the moment a student can click Run. */
  loadJedi();
}

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
      pyodide.setInterruptBuffer(new Int32Array(msg.buffer));
    } else if (msg.type === "run-cell") {
      respond(await runCell(msg.cellId, msg.code));
    } else if (msg.type === "hover-doc") {
      respond(hoverDoc(msg.name, msg.source, msg.line, msg.col));
    } else if (msg.type === "signature-help") {
      respond(signatureHelp(msg.name, msg.source, msg.line, msg.col));
    } else if (msg.type === "page-names") {
      respond(pageNames());
    }
  } catch (err) {
    fail(err);
  }
};
