
import { importPathSource, importedModuleTimesSource, reloadModulesSource, workingDirectorySource } from "./module-watch.js";

const DEFAULT_PACKAGES = ["numpy", "pandas", "matplotlib", "sqlite3"];

const RESEED_GLOBALS_SOURCE = `
import tutorial_tools
tutorial_tools._page_globals.update({
    name: getattr(tutorial_tools, name)
    for name in tutorial_tools.__all__
})
tutorial_tools._page_globals["__name__"] = "__dewlab__"

import sqlite3
_dewmini_previous_db = tutorial_tools._page_globals.get("db")
if _dewmini_previous_db is not None:
    _dewmini_previous_db.close()
tutorial_tools._page_globals["db"] = sqlite3.connect(":memory:")
`;

const NETWORK_PATCH_SOURCE = `
try:
    import pyodide_http
    pyodide_http.patch_all()
except Exception:
    pass
`;

function assetUrl(relativePath) {
  return new URL(relativePath, import.meta.url).href;
}

let getOutputEl = null; // (cellId) => that cell's output <div>, or null
let onStatus = null; // (text, kind?) => show a status message on the page
let packages = DEFAULT_PACKAGES; // which Pyodide packages to load at boot
// The base URL tutorial_tools.py's own load_csv() resolves a dataset name
// against — empty by default (right for a page at the site root),
// overridable per page since dewmini lives one directory deeper
// (compose/) and needs "../data/" to reach the same repo-root data/
// folder the tutorial pages already share.
let dataBase = "";

export function configure(options) {
  getOutputEl = options.getOutputEl;
  onStatus = options.onStatus || (() => {});
  if (options.packages && options.packages.length) packages = options.packages;
  if (typeof options.dataBase === "string") dataBase = options.dataBase;
}

function setStatus(text, kind) {
  onStatus(text, kind);
}

const openStreams = new Map(); // cellId -> {el, cssClass}

export function applyOutputEvent(cellId, kind, cssClass, text, markup) {
  const el = getOutputEl ? getOutputEl(cellId) : null;
  if (!el) return;
  if (kind === "stream") {
    let open = openStreams.get(cellId);
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

export function clearOutput(cellId) {
  openStreams.delete(cellId);
  const el = getOutputEl ? getOutputEl(cellId) : null;
  if (el) el.replaceChildren();
}

let worker = null; // the Worker object itself, once created
let interruptBuffer = null; // shared memory used to signal "stop running" (see requestInterrupt below)
let jediReadyWorker = false; // has the worker finished loading Jedi (autocomplete) yet?
let nextRequestId = 1; // counts up so every request gets a unique id
const pendingRequests = new Map(); // id -> {resolve, reject}

function workerRequest(type, payload) {
  const id = nextRequestId++;
  return new Promise((resolve, reject) => {
    pendingRequests.set(id, { resolve, reject });
    worker.postMessage({ type, id, ...payload });
  });
}

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

async function bootWorker() {
  ensureWorker();
  await workerRequest("boot", {
    pyodideBase: pyodideBase(),
    packages,
    toolsSourceUrl: assetUrl("tutorial_tools.py"),
    dataBase,
    // Always true: this module is dewmini's own worker client (see the
    // file banner above) — assets/pyodide-worker.js reads this to decide
    // whether to seed the dewmini-only `db` global, since it's the same
    // worker file the hosted tutorial pages boot through and they must
    // never get one.
    seedDb: true,
  });

  if (globalThis.crossOriginIsolated && typeof SharedArrayBuffer !== "undefined") {
    interruptBuffer = new SharedArrayBuffer(4);
    worker.postMessage({ type: "set-interrupt-buffer", buffer: interruptBuffer });
  }
}

function requestInterrupt() {
  if (!interruptBuffer) return;
  /* 2 is SIGINT in Pyodide's own interrupt-buffer convention. */
  new Int32Array(interruptBuffer)[0] = 2;
}

async function runCellWorker(cellId, code, label) {
  return workerRequest("run-cell", { cellId, code, label });
}

async function resetPageStateWorker() {
  await workerRequest("reset-page-state", {});
}

let pyodideMT = null; // the Pyodide interpreter itself
let toolsMT = null; // the imported tutorial_tools Python module
let inspectModuleMT = null; // Python's own `inspect` module, for hover docs
let builtinsModuleMT = null; // Python's `builtins` module, for looking up e.g. `len`
let jediHoverFnMT = null; // the _dewlab_hover_doc Python function defined below
let jediSignatureFnMT = null; // the _dewlab_signature Python function defined below

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

function pyodideBase() {
  return new URL(
    globalThis.DEWLAB_PYODIDE_BASE || `https://cdn.jsdelivr.net/pyodide/v0.28.3/full/`,
    document.baseURI
  ).href;
}

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

async function resetPageStateMT() {
  toolsMT.reset_page_state();
  await pyodideMT.runPythonAsync(RESEED_GLOBALS_SOURCE);
}

function pageNamesMT() {
  if (!toolsMT) return [];
  return [...toolsMT._page_globals.keys()].filter((name) => !name.startsWith("_"));
}

function describeGlobalsMT() {
  if (!toolsMT) return [];
  const proxy = toolsMT.describe_globals();
  const described = proxy.toJs({ dict_converter: Object.fromEntries });
  proxy.destroy();
  return described;
}

async function runCellMainThread(cellId, code, label) {
  const el = getOutputEl ? getOutputEl(cellId) : null;
  const ok = await toolsMT.run_cell(cellId, el, code, undefined, label);
  return { ok };
}

let mountedFsMT = null; // whatever mount object the active backend gave back, so fsSyncMT knows how to sync it

async function fsMountNativeMT(mountpoint, handle) {
  pyodideMT.FS.mkdirTree(mountpoint);
  mountedFsMT = await pyodideMT.mountNativeFS(mountpoint, handle);
}

async function fsMountOpfsMT(mountpoint) {
  const opfsRoot = await navigator.storage.getDirectory();
  pyodideMT.FS.mkdirTree(mountpoint);
  mountedFsMT = await pyodideMT.mountNativeFS(mountpoint, opfsRoot);
}

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

async function fsSyncMT() {
  if (mountedFsMT) await mountedFsMT.syncfs();
}

function fsUnmountMT(path) {
  pyodideMT.FS.unmount(path);
  mountedFsMT = null;
}

function fsListMT(path) {
  const names = pyodideMT.FS.readdir(path).filter((n) => n !== "." && n !== "..");
  return names.map((name) => {
    const stat = pyodideMT.FS.stat(`${path.replace(/\/$/, "")}/${name}`);
    return { name, isDir: pyodideMT.FS.isDir(stat.mode), size: stat.size };
  });
}

function fsReadMT(path, encoding) {
  return pyodideMT.FS.readFile(path, encoding ? { encoding } : undefined);
}

/* Writes (or overwrites) one file with `data`, which can be a string or
 * raw bytes. */
function fsWriteMT(path, data) {
  pyodideMT.FS.writeFile(path, data);
}

function fsDeleteMT(path) {
  const stat = pyodideMT.FS.stat(path);
  if (pyodideMT.FS.isDir(stat.mode)) pyodideMT.FS.rmdir(path);
  else pyodideMT.FS.unlink(path);
}

function fsMkdirMT(path) {
  pyodideMT.FS.mkdirTree(path);
}

let mode = null; // "worker" | "main-thread", set once boot() resolves
let bootPromise = null;

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

export function ensureBooted() {
  if (!bootPromise) {
    bootPromise = boot().catch((err) => {
      bootPromise = null; // let a retry (e.g. a later Run click) try again
      throw err;
    });
  }
  return bootPromise;
}

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

  for (const { reject } of pendingRequests.values()) {
    reject(new Error("Python was restarted before this finished."));
  }
  pendingRequests.clear();
  openStreams.clear();

  // A fresh interpreter has imported nothing, so every remembered file
  // time describes a module that no longer exists.
  seenModuleTimes.clear();

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

export function engineMode() {
  return mode;
}

export function canStop() {
  return mode === "worker" && interruptBuffer !== null;
}

export { requestInterrupt };

export async function runCell(cellId, code, label) {
  clearOutput(cellId);
  if (mode === "main-thread") return runCellMainThread(cellId, code, label);
  return runCellWorker(cellId, code, label);
}

export async function resetPageState() {
  if (mode === "main-thread") return resetPageStateMT();
  return resetPageStateWorker();
}

async function hoverDoc(name, source, line, col) {
  if (mode === "main-thread") return docForMT(name) || jediDocMT(source, line, col);
  if (!worker) return null;
  return workerRequest("hover-doc", { name, source, line, col });
}

async function signatureHelp(name, source, line, col, argIndex) {
  void argIndex; // CodeMirror bolds the argument itself; not needed here
  if (mode === "main-thread") return signatureForMT(name) || jediSignatureMT(source, line, col);
  if (!worker) return null;
  return workerRequest("signature-help", { name, source, line, col });
}

export { hoverDoc, signatureHelp };

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

export async function describeGlobals() {
  if (mode === "main-thread") return describeGlobalsMT();
  if (!worker) return [];
  return workerRequest("describe-globals", {});
}

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

export async function addImportPath(path) {
  if (mode === "main-thread") {
    pyodideMT.runPython(importPathSource(path));
    return;
  }
  await workerRequest("add-import-path", { path });
}

export async function setWorkingDirectory(path) {
  if (mode === "main-thread") {
    pyodideMT.runPython(workingDirectorySource(path));
    return;
  }
  await workerRequest("set-working-directory", { path });
}

const seenModuleTimes = new Map();

export async function changedImportedModules(path) {
  let current;
  try {
    const raw = mode === "main-thread"
      ? pyodideMT.runPython(importedModuleTimesSource(path))
      : worker ? await workerRequest("imported-module-times", { path }) : "[]";
    current = JSON.parse(raw || "[]");
  } catch (err) {
    // Never worth interrupting a run over: this only ever drives a
    // notice, and a page that cannot ask simply does not show one.
    console.warn("dewlab: could not check imported modules", err);
    return [];
  }

  const changed = [];
  const live = new Set();
  for (const { name, mtime } of current) {
    live.add(name);
    const seen = seenModuleTimes.get(name);
    if (seen !== undefined && mtime !== null && mtime !== seen) changed.push(name);
    if (mtime !== null) seenModuleTimes.set(name, mtime);
  }
  // A module no longer in sys.modules cannot go stale, and keeping its
  // time would make a re-import of the same name look like an edit.
  for (const name of [...seenModuleTimes.keys()]) {
    if (!live.has(name)) seenModuleTimes.delete(name);
  }
  return changed;
}

export async function reloadModules(names) {
  if (!names.length) return { reloaded: [], failed: [] };
  const raw = mode === "main-thread"
    ? pyodideMT.runPython(reloadModulesSource(names))
    : worker ? await workerRequest("reload-modules", { names }) : null;
  const result = raw ? JSON.parse(raw) : { reloaded: [], failed: [] };
  // A reloaded module has been read afresh, so whatever its file says now
  // is what Python holds — forget the old time rather than leave the next
  // check comparing against it.
  for (const name of result.reloaded) seenModuleTimes.delete(name);
  return result;
}
