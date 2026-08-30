/* dewmini's filesystem — ported from assets/mini-ide-fs.js
 * (planning/MINI_IDE_REDESIGN.md Phase 2, DECISIONS_LOG.md 7.88), trimmed
 * to match dewmini's own single-threaded engine: Mini IDE's version sits
 * behind mini-ide-engine.js's Worker/main-thread dispatch, since Pyodide
 * there might be running in either place; dewmini only ever runs Pyodide
 * on the main thread, so the filesystem calls below talk to `pyodide.FS`
 * directly rather than through a second dispatching layer that would
 * only ever have one path to dispatch to.
 *
 * One small interface (init, listDir, readFile, writeFile, deleteFile,
 * mkdir) sitting between a mounted Pyodide filesystem and dewmini's own
 * Settings "Files" section — the same three backends, tried in the same
 * order, for the same reasons mini-ide-fs.js already explains in full:
 *   1. A real local folder, via the File System Access API. Chromium
 *      only, and only ever entered on an explicit click (chooseFolder()),
 *      never silently.
 *   2. OPFS — persistent, no picker, no permission prompt, broadly
 *      supported. What init() mounts by default.
 *   3. IDBFS — the universal fallback.
 *
 * getPyodide() is injected via configure() rather than imported directly
 * from dewmini.js: dewmini.js needs to call *into* this module (to mount
 * a filesystem once Pyodide boots) and this module needs to call *into*
 * dewmini.js (to get the live Pyodide instance, booting it if it hasn't
 * started yet) — a genuine two-way dependency between the two files, and
 * dependency injection avoids the circular-import tangle that having
 * each file `import` the other by name would create.
 */

const MOUNT_POINT = "/mnt/dewmini";
const SYNC_DEBOUNCE_MS = 1500;

const DB_NAME = "dewmini-fs";
const DB_VERSION = 1;
const STORE_NAME = "kv";
const HANDLE_KEY = "native-dir-handle";

// The subdirectory name mini-ide-fs.js's own OPFS mount does *not* use —
// it mounts navigator.storage.getDirectory() itself directly at its own
// mount point, which maps Pyodide's mounted view straight onto the
// origin's one shared OPFS root. Two tools doing that on the same origin
// would see and could overwrite each other's files, invisibly, the
// moment both existed — not a problem when Mini IDE was the only one
// mounting OPFS, but a real one now that dewmini does too. dewmini gets
// its own named subdirectory of that shared root instead (see
// mountOpfs() below), so its files stay separate from Mini IDE's
// (whose own mount is left as-is here — retiring it, not fixing it in
// place, is the plan per planning/MINI_IDE_AND_DEWMINI_NEXT.md §6).
const OPFS_SUBDIR = "dewmini";

/* ------------------------------------------------------------- IndexedDB
 * A FileSystemDirectoryHandle is structured-cloneable, so it can be
 * stored as an IndexedDB value directly — the standard way to persist
 * File System Access API access across reloads. Kept under its own
 * database name (not mini-ide-fs.js's), so choosing a folder in one tool
 * never silently reconnects it in the other — each remembers its own
 * choice, even if a student happens to pick the same real folder in
 * both. */

function idbOpen() {
  return new Promise((resolve, reject) => {
    const req = indexedDB.open(DB_NAME, DB_VERSION);
    req.onupgradeneeded = () => {
      req.result.createObjectStore(STORE_NAME);
    };
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}

async function idbGet(key) {
  const db = await idbOpen();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORE_NAME, "readonly");
    const req = tx.objectStore(STORE_NAME).get(key);
    req.onsuccess = () => resolve(req.result ?? null);
    req.onerror = () => reject(req.error);
  });
}

async function idbSet(key, value) {
  const db = await idbOpen();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORE_NAME, "readwrite");
    tx.objectStore(STORE_NAME).put(value, key);
    tx.oncomplete = () => resolve();
    tx.onerror = () => reject(tx.error);
  });
}

async function idbDelete(key) {
  const db = await idbOpen();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORE_NAME, "readwrite");
    tx.objectStore(STORE_NAME).delete(key);
    tx.oncomplete = () => resolve();
    tx.onerror = () => reject(tx.error);
  });
}

/* --------------------------------------------------------- FS primitives
 * The direct pyodide.FS calls mini-ide-engine.js's own fs*MT() functions
 * wrap — copied here in the same shape, since dewmini's Pyodide instance
 * lives on the main thread the same way theirs does when a Worker isn't
 * available. `getPyodide` (set by configure()) is called fresh each
 * time rather than cached, since the instance can change across a page
 * reload (nothing else here persists it either). */

let getPyodide = null;
let mountedFs = null;

async function fsMountNative(mountpoint, handle) {
  const pyodide = await getPyodide();
  pyodide.FS.mkdirTree(mountpoint);
  mountedFs = await pyodide.mountNativeFS(mountpoint, handle);
}

async function fsMountOpfs(mountpoint) {
  const pyodide = await getPyodide();
  const opfsRoot = await navigator.storage.getDirectory();
  const dewminiDir = await opfsRoot.getDirectoryHandle(OPFS_SUBDIR, { create: true });
  pyodide.FS.mkdirTree(mountpoint);
  mountedFs = await pyodide.mountNativeFS(mountpoint, dewminiDir);
}

async function fsMountIdbfs(mountpoint) {
  const pyodide = await getPyodide();
  pyodide.FS.mkdirTree(mountpoint);
  pyodide.FS.mount(pyodide.FS.filesystems.IDBFS, {}, mountpoint);
  await new Promise((resolve, reject) => {
    pyodide.FS.syncfs(true, (err) => (err ? reject(err) : resolve()));
  });
  mountedFs = {
    syncfs: () =>
      new Promise((resolve, reject) => {
        pyodide.FS.syncfs(false, (err) => (err ? reject(err) : resolve()));
      }),
  };
}

async function fsSync() {
  if (mountedFs) await mountedFs.syncfs();
}

async function fsUnmount(path) {
  const pyodide = await getPyodide();
  pyodide.FS.unmount(path);
  mountedFs = null;
}

async function fsList(path) {
  const pyodide = await getPyodide();
  const names = pyodide.FS.readdir(path).filter((n) => n !== "." && n !== "..");
  return names.map((name) => {
    const stat = pyodide.FS.stat(`${path.replace(/\/$/, "")}/${name}`);
    return { name, isDir: pyodide.FS.isDir(stat.mode), size: stat.size };
  });
}

async function fsRead(path, encoding) {
  const pyodide = await getPyodide();
  return pyodide.FS.readFile(path, encoding ? { encoding } : undefined);
}

async function fsWrite(path, data) {
  const pyodide = await getPyodide();
  pyodide.FS.writeFile(path, data);
}

async function fsDelete(path) {
  const pyodide = await getPyodide();
  const stat = pyodide.FS.stat(path);
  if (pyodide.FS.isDir(stat.mode)) pyodide.FS.rmdir(path);
  else pyodide.FS.unlink(path);
}

async function fsMkdir(path) {
  const pyodide = await getPyodide();
  pyodide.FS.mkdirTree(path);
}

/* ------------------------------------------------------------- backend */

let backend = null;
let onBackendChange = () => {};

function setBackend(name) {
  backend = name;
  onBackendChange(name);
}

/** Current backend, or null before init() has resolved. */
export function getBackend() {
  return backend;
}

/**
 * @param {Object} options
 * @param {() => Promise<Object>} options.getPyodide - resolves to the
 *   live Pyodide instance, booting it first if it hasn't started (the
 *   same function dewmini.js's own Run button calls).
 * @param {(backend: string) => void} [options.onBackendChange] - called
 *   whenever the active backend changes.
 */
export function configure(options) {
  getPyodide = options.getPyodide;
  onBackendChange = options.onBackendChange || (() => {});
}

async function mountOpfsIfSupported() {
  if (!("storage" in navigator) || typeof navigator.storage.getDirectory !== "function") return false;
  try {
    await fsMountOpfs(MOUNT_POINT);
    setBackend("opfs");
    return true;
  } catch (err) {
    console.warn("dewmini: OPFS mount failed, falling back to IndexedDB storage", err);
    return false;
  }
}

let initPromise = null;

/**
 * Mounts a filesystem: a previously chosen and still-permitted real
 * folder if one is on file, otherwise OPFS, otherwise IDBFS. Requires
 * Pyodide to already be starting (getPyodide() drives that) — called
 * from dewmini.js right after Pyodide itself finishes booting, so
 * "Files" in Settings only ever shows real status once Python has
 * actually started, the same lazy-boot rule the rest of dewmini follows.
 * Idempotent: a second call returns the same in-flight/completed mount.
 */
export function init() {
  if (!initPromise) initPromise = doInit();
  return initPromise;
}

async function doInit() {
  const storedHandle = await idbGet(HANDLE_KEY).catch(() => null);
  if (storedHandle) {
    try {
      const permission = await storedHandle.queryPermission({ mode: "readwrite" });
      if (permission === "granted") {
        await fsMountNative(MOUNT_POINT, storedHandle);
        setBackend("native");
        return;
      }
    } catch (err) {
      console.warn("dewmini: a previously chosen folder is no longer usable", err);
      await idbDelete(HANDLE_KEY).catch(() => {});
    }
  }

  if (await mountOpfsIfSupported()) return;
  await fsMountIdbfs(MOUNT_POINT);
  setBackend("idbfs");
}

/** Whether a real folder was chosen before, so Settings can offer
 * "Reconnect" instead of "Choose folder". */
export async function hasStoredFolder() {
  return Boolean(await idbGet(HANDLE_KEY).catch(() => null));
}

/** Lets a student opt into a real local folder. Must be called directly
 * inside a click handler — showDirectoryPicker() throws without a fresh
 * user gesture. */
export async function chooseFolder() {
  if (typeof window.showDirectoryPicker !== "function") {
    throw new Error("This browser can't grant access to a real folder — try Chrome or Edge.");
  }
  const handle = await window.showDirectoryPicker({ mode: "readwrite" });
  if (backend) await fsUnmount(MOUNT_POINT);
  await fsMountNative(MOUNT_POINT, handle);
  await idbSet(HANDLE_KEY, handle);
  setBackend("native");
  return handle;
}

/** Re-grants permission on a previously chosen folder. Must also be
 * called inside a click handler, same as chooseFolder(). */
export async function reconnectFolder() {
  const storedHandle = await idbGet(HANDLE_KEY);
  if (!storedHandle) throw new Error("No previously chosen folder to reconnect.");
  const permission = await storedHandle.requestPermission({ mode: "readwrite" });
  if (permission !== "granted") throw new Error("Folder access wasn't granted.");
  if (backend) await fsUnmount(MOUNT_POINT);
  await fsMountNative(MOUNT_POINT, storedHandle);
  setBackend("native");
}

/** Forgets a chosen folder (does not touch its contents). */
export async function forgetFolder() {
  await idbDelete(HANDLE_KEY).catch(() => {});
}

/* --------------------------------------------------------- file access */

function resolvePath(relativePath) {
  const clean = String(relativePath || "").replace(/^\/+/, "").replace(/\/+$/, "");
  return clean ? `${MOUNT_POINT}/${clean}` : MOUNT_POINT;
}

/** Lists one directory's contents, folders before files, alphabetically
 * within each group. dewmini's own Settings "Files" list only ever
 * browses the mount's root (a deliberate, smaller scope than Mini IDE's
 * full tree — see DECISIONS_LOG.md 7.88) but this itself stays general,
 * the same as mini-ide-fs.js's own listDir(). */
export async function listDir(relativePath = "") {
  const entries = await fsList(resolvePath(relativePath));
  return entries.sort((a, b) => {
    if (a.isDir !== b.isDir) return a.isDir ? -1 : 1;
    return a.name.localeCompare(b.name);
  });
}

export async function readFile(relativePath, encoding) {
  return fsRead(resolvePath(relativePath), encoding);
}

export async function writeFile(relativePath, data) {
  await fsWrite(resolvePath(relativePath), data);
  scheduleSync();
}

export async function deleteFile(relativePath) {
  await fsDelete(resolvePath(relativePath));
  scheduleSync();
}

export async function mkdir(relativePath) {
  await fsMkdir(resolvePath(relativePath));
  scheduleSync();
}

/**
 * Syncs the mounted filesystem right now, best-effort — for a caller
 * that already knows something might have changed but didn't go through
 * writeFile()/deleteFile()/mkdir() above, so scheduleSync() below was
 * never triggered. The one real case: a cell's own Python code writing
 * straight to the mount (`open("/mnt/dewmini/x.db", "w")`,
 * `sqlite3.connect(...)`) never touches this module's JS functions at
 * all, so nothing here would otherwise know a write happened — dewmini.js
 * calls this once after every cell finishes running, rather than relying
 * only on the beforeunload/visibilitychange flush further down, which
 * (being an async operation started from a synchronous unload event) a
 * browser makes no promise of actually letting finish before the page
 * goes away.
 */
export async function sync() {
  if (backend) await fsSync();
}

/* ------------------------------------------------------------ syncing */

let syncTimer = null;

function scheduleSync() {
  clearTimeout(syncTimer);
  syncTimer = setTimeout(() => {
    fsSync().catch((err) => console.warn("dewmini: filesystem sync failed", err));
  }, SYNC_DEBOUNCE_MS);
}

function flushSyncNow() {
  clearTimeout(syncTimer);
  fsSync().catch(() => {}); // best-effort; nothing to do if it's too late
}

window.addEventListener("beforeunload", flushSyncNow);
document.addEventListener("visibilitychange", () => {
  if (document.visibilityState === "hidden") flushSyncNow();
});
