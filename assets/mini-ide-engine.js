/* Mini IDE's Pyodide engine.
 *
 * Runs Pyodide off the main thread by reusing assets/pyodide-worker.js —
 * the same file the hosted tutorial pages already boot through
 * (assets/tutorial-runtime.js). This module is mini-ide.js's worker
 * *client*: booting, running a cell, hover/signature-help lookups, Stop
 * support, and streaming a cell's output back into its own output
 * element. mini-ide.js owns the cell array and the DOM; this module never
 * touches either directly, only through the accessor passed to configure().
 *
 * Ported from tutorial-runtime.js's own worker-communication block rather
 * than imported from it — this codebase's existing convention (mini-ide.js
 * already duplicates tutorial-runtime.js's texture code rather than
 * sharing it) is that each page owns a thin copy rather than a shared
 * runtime module.
 *
 * A page opened over file:// (the downloadable, offline Mini IDE) can run
 * into real restrictions constructing a module Worker at all, so boot()
 * falls back to running Pyodide on the main thread — same interpreter,
 * same tutorial_tools.py, just no genuine Stop button, exactly like the
 * tutorial pages' own standalone export (DECISIONS_LOG.md 7.77).
 */

const DEFAULT_PACKAGES = ["numpy", "pandas", "matplotlib"];

/* Resolved against the *page*, not this module: a relative fetch from
 * inside the worker resolves against the worker script's own location,
 * not the page's, so every URL handed to the worker (or read by the
 * main-thread fallback) has to be absolute first. */
function pageUrl(relativePath) {
  return new URL(relativePath, document.baseURI).href;
}

let getOutputEl = null;
let onStatus = null;
let packages = DEFAULT_PACKAGES;

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
 */
export function configure(options) {
  getOutputEl = options.getOutputEl;
  onStatus = options.onStatus || (() => {});
  if (options.packages && options.packages.length) packages = options.packages;
}

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

function applyOutputEvent(cellId, kind, cssClass, text, markup) {
  const el = getOutputEl ? getOutputEl(cellId) : null;
  if (!el) return;
  if (kind === "stream") {
    let open = openStreams.get(cellId);
    if (!open || open.cssClass !== cssClass) {
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

let worker = null;
let interruptBuffer = null;
let jediReadyWorker = false;
let nextRequestId = 1;
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
    toolsSourceUrl: pageUrl("assets/tutorial_tools.py"),
    /* No data directory of its own yet (planning/MINI_IDE_REDESIGN.md
     * Phase 2 gives it a real mounted filesystem) — empty, matching the
     * pre-Worker implementation, so load_csv() fails informatively rather
     * than resolving against a folder that doesn't exist. */
    dataBase: "",
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

async function runCellWorker(cellId, code) {
  return workerRequest("run-cell", { cellId, code });
}

/* -------------------------------------------------- Main-thread fallback */

let pyodideMT = null;
let toolsMT = null;
let inspectModuleMT = null;
let builtinsModuleMT = null;
let jediHoverFnMT = null;
let jediSignatureFnMT = null;

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
    console.warn("mini-ide: Jedi failed to load; pre-run tooltips stay live-only", err);
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

  setStatus("Preparing the notebook tools…");
  const source = await fetch(pageUrl("assets/tutorial_tools.py")).then((r) => {
    if (!r.ok) throw new Error(`tutorial_tools.py: HTTP ${r.status}`);
    return r.text();
  });
  pyodideMT.FS.writeFile("/home/pyodide/tutorial_tools.py", source, { encoding: "utf8" });
  toolsMT = pyodideMT.pyimport("tutorial_tools");
  inspectModuleMT = pyodideMT.pyimport("inspect");
  builtinsModuleMT = pyodideMT.pyimport("builtins");
  toolsMT.configure(""); // see the matching note in bootWorker() above

  await pyodideMT.runPythonAsync(`
import tutorial_tools
tutorial_tools._page_globals.update({
    name: getattr(tutorial_tools, name)
    for name in tutorial_tools.__all__
})
tutorial_tools._page_globals["__name__"] = "__dewlab__"
`);

  setStatus("");
  loadJediMT(); // deliberately not awaited — must not delay the first Run
}

function pageNamesMT() {
  if (!toolsMT) return [];
  return [...toolsMT._page_globals.keys()].filter((name) => !name.startsWith("_"));
}

async function runCellMainThread(cellId, code) {
  const el = getOutputEl ? getOutputEl(cellId) : null;
  const ok = await toolsMT.run_cell(cellId, el, code);
  return { ok };
}

/* Filesystem, main-thread mirror of the worker's fs-* handlers in
 * pyodide-worker.js — same Pyodide FS calls, just made directly since
 * pyodideMT lives right here instead of across a postMessage boundary. */
let mountedFsMT = null;

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

/* ------------------------------------------------------- the dispatcher */

let mode = null; // "worker" | "main-thread", set once boot() resolves
let bootPromise = null;

async function boot() {
  if (typeof Worker !== "undefined") {
    try {
      await bootWorker();
      mode = "worker";
      return;
    } catch (err) {
      console.warn("mini-ide: Worker boot failed, falling back to the main thread", err);
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

export function engineMode() {
  return mode;
}

export function canStop() {
  return mode === "worker" && interruptBuffer !== null;
}

export { requestInterrupt };

export async function runCell(cellId, code) {
  clearOutput(cellId);
  if (mode === "main-thread") return runCellMainThread(cellId, code);
  return runCellWorker(cellId, code);
}

/* ---- code intelligence: what vendor-src/codemirror-entry.js calls ---- */

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

/* ------------------------------------------------------------- filesystem
 *
 * mini-ide-fs.js is the only caller of everything below: it owns backend
 * selection (native folder vs. OPFS vs. IDBFS) and calls these once it has
 * decided. Every function here assumes ensureBooted() has already
 * resolved — Pyodide's FS doesn't exist before that. */

export async function mountNative(mountpoint, handle) {
  if (mode === "main-thread") return fsMountNativeMT(mountpoint, handle);
  return workerRequest("fs-mount-native", { mountpoint, handle });
}

export async function mountOpfs(mountpoint) {
  if (mode === "main-thread") return fsMountOpfsMT(mountpoint);
  return workerRequest("fs-mount-opfs", { mountpoint });
}

export async function mountIdbfs(mountpoint) {
  if (mode === "main-thread") return fsMountIdbfsMT(mountpoint);
  return workerRequest("fs-mount-idbfs", { mountpoint });
}

export async function syncFs() {
  if (mode === "main-thread") return fsSyncMT();
  return workerRequest("fs-sync", {});
}

/* Required before mounting a different backend at the same mountpoint. */
export async function unmount(mountpoint) {
  if (mode === "main-thread") return fsUnmountMT(mountpoint);
  return workerRequest("fs-unmount", { mountpoint });
}

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

export async function writeFile(path, data) {
  if (mode === "main-thread") return fsWriteMT(path, data);
  return workerRequest("fs-write", { path, data });
}

export async function deleteFile(path) {
  if (mode === "main-thread") return fsDeleteMT(path);
  return workerRequest("fs-delete", { path });
}

export async function mkdir(path) {
  if (mode === "main-thread") return fsMkdirMT(path);
  return workerRequest("fs-mkdir", { path });
}
