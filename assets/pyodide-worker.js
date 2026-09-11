
import { importPathSource, importedModuleTimesSource, reloadModulesSource, workingDirectorySource } from "./module-watch.js";

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

const NETWORK_PATCH_SOURCE = `
try:
    import pyodide_http
    pyodide_http.patch_all()
except Exception:
    pass
`;

const RESEED_GLOBALS_SOURCE = `
import tutorial_tools
tutorial_tools._page_globals.update({
    name: getattr(tutorial_tools, name)
    for name in tutorial_tools.__all__
})
tutorial_tools._page_globals["__name__"] = "__dewlab__"
`;

const SEED_DEWMINI_DB_SOURCE = `
import sqlite3
_dewmini_previous_db = tutorial_tools._page_globals.get("db")
if _dewmini_previous_db is not None:
    _dewmini_previous_db.close()
tutorial_tools._page_globals["db"] = sqlite3.connect(":memory:")
`;

let seedDewminiDb = false;

async function boot(msg) {
  post({ type: "status", text: "Starting Python…" });
  const { loadPyodide } = await import(/* @vite-ignore */ msg.pyodideBase + "pyodide.mjs");
  pyodide = await loadPyodide({ indexURL: msg.pyodideBase });

  post({ type: "status", text: `Loading ${msg.packages.join(", ")}…` });
  await pyodide.loadPackage(msg.packages);
  // Separately, and forgivingly: a Pyodide without this package must still
  // boot. See NETWORK_PATCH_SOURCE for what it buys.
  try {
    await pyodide.loadPackage(["pyodide-http"]);
    await pyodide.runPythonAsync(NETWORK_PATCH_SOURCE);
  } catch {
    /* no browser-backed urllib; tutorial_tools.py's hints cover it */
  }

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

  seedDewminiDb = !!msg.seedDb;
  await pyodide.runPythonAsync(RESEED_GLOBALS_SOURCE);
  if (seedDewminiDb) await pyodide.runPythonAsync(SEED_DEWMINI_DB_SOURCE);

  post({ type: "status", text: "" });

  /* Deliberately not awaited: a slower or blocked Jedi download must never
   * delay the moment a student can click Run. */
  loadJedi();
}

async function runCell(cellId, code, expect, label) {
  const emit = (kind, cssClass, text, markup) => {
    post({ type: "output", cellId, kind, cssClass, text, markup });
  };
  const report = await tools.run_cell_report(cellId, emit, code, expect ?? null, label ?? null);
  return JSON.parse(report);
}

async function resetPageState() {
  tools.reset_page_state();
  await pyodide.runPythonAsync(RESEED_GLOBALS_SOURCE);
  if (seedDewminiDb) await pyodide.runPythonAsync(SEED_DEWMINI_DB_SOURCE);
}

let mountedFs = null; // whatever mount object the active backend gave back, for fsSync() to use

async function fsMountNative(mountpoint, handle) {
  pyodide.FS.mkdirTree(mountpoint);
  mountedFs = await pyodide.mountNativeFS(mountpoint, handle);
}

async function fsMountOpfs(mountpoint) {
  const opfsRoot = await navigator.storage.getDirectory();
  pyodide.FS.mkdirTree(mountpoint);
  mountedFs = await pyodide.mountNativeFS(mountpoint, opfsRoot);
}

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

async function fsSync() {
  if (mountedFs) await mountedFs.syncfs();
}

function fsUnmount(path) {
  pyodide.FS.unmount(path);
  mountedFs = null;
}

function fsList(path) {
  const names = pyodide.FS.readdir(path).filter((n) => n !== "." && n !== "..");
  return names.map((name) => {
    const stat = pyodide.FS.stat(`${path.replace(/\/$/, "")}/${name}`);
    return { name, isDir: pyodide.FS.isDir(stat.mode), size: stat.size };
  });
}

function fsRead(path, encoding) {
  return pyodide.FS.readFile(path, encoding ? { encoding } : undefined);
}

/* Writes (or overwrites) one file with `data` — a string or raw bytes. */
function fsWrite(path, data) {
  pyodide.FS.writeFile(path, data);
}

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
      respond(await runCell(msg.cellId, msg.code, msg.expect, msg.label));
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
    } else if (msg.type === "add-import-path") {
      pyodide.runPython(importPathSource(msg.path));
      respond("ok");
    } else if (msg.type === "set-working-directory") {
      pyodide.runPython(workingDirectorySource(msg.path));
      respond("ok");
    } else if (msg.type === "imported-module-times") {
      respond(pyodide.runPython(importedModuleTimesSource(msg.path)));
    } else if (msg.type === "reload-modules") {
      respond(pyodide.runPython(reloadModulesSource(msg.names)));
    }
  } catch (err) {
    fail(err);
  }
};
