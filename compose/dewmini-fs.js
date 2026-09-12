
import * as engine from "../assets/pyodide-engine.js";

const MOUNT_POINT = "/mnt/dewmini";
const SYNC_DEBOUNCE_MS = 1500;

const DB_NAME = "dewmini-fs";
const DB_VERSION = 1;
const STORE_NAME = "kv";
const HANDLE_KEY = "native-dir-handle";

// An OPFS mount could hand navigator.storage.getDirectory() straight to
// engine.mountNative() — mapping Pyodide's mounted view directly onto
// the origin's one shared OPFS root. Two tools doing that on the same
// origin would see and could overwrite each other's files, invisibly,
// the moment both existed. dewmini mounts its own named subdirectory of
// that shared root instead (see mountOpfs() below) before handing
// *that* handle to the same engine.mountNative() real-folder mounting
// already uses — OPFS mounting and real-folder mounting are the same
// operation as far as the engine is concerned, just with a different
// handle source, so this needs no engine change at all.
const OPFS_SUBDIR = "dewmini";

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

/** Where the workspace is mounted inside Python — the directory a
 * student's own .py files are imported from. */
export function mountPoint() {
  return MOUNT_POINT;
}

export function configure(options = {}) {
  onBackendChange = options.onBackendChange || (() => {});
}

async function mountOpfsIfSupported() {
  if (!("storage" in navigator) || typeof navigator.storage.getDirectory !== "function") return false;
  try {
    const opfsRoot = await navigator.storage.getDirectory();
    const dewminiDir = await opfsRoot.getDirectoryHandle(OPFS_SUBDIR, { create: true });
    await engine.mountNative(MOUNT_POINT, dewminiDir);
    setBackend("opfs");
    return true;
  } catch (err) {
    console.warn("dewmini: OPFS mount failed, falling back to IndexedDB storage", err);
    return false;
  }
}

let initPromise = null;

export function init() {
  if (!initPromise) initPromise = doInit();
  return initPromise;
}

async function doInit() {
  await engine.ensureBooted();

  // Before any backend is chosen: the mount point goes on Python's import
  // search list whichever backend ends up behind it, and the path itself
  // is the same in all three cases. Without this a student can write two
  // Python files in the workspace and have no way to use one from the
  // other, which is the whole difficulty this workspace exists to teach
  // them through.
  await engine.addImportPath(MOUNT_POINT);

  await mountBestBackend();

  // Only now, and not beside addImportPath above. sys.path takes a string
  // and does not care whether the directory exists yet; chdir does, and
  // fails on a path nothing is mounted at. Done too early it therefore did
  // nothing at all, quietly, and a student's own open("notes.txt", "w")
  // went on landing outside the workspace.
  await engine.setWorkingDirectory(MOUNT_POINT);
}

async function mountBestBackend() {
  const storedHandle = await idbGet(HANDLE_KEY).catch(() => null);
  if (storedHandle) {
    try {
      const permission = await storedHandle.queryPermission({ mode: "readwrite" });
      if (permission === "granted") {
        await engine.mountNative(MOUNT_POINT, storedHandle);
        setBackend("native");
        return;
      }
    } catch (err) {
      console.warn("dewmini: a previously chosen folder is no longer usable", err);
      await idbDelete(HANDLE_KEY).catch(() => {});
    }
  }

  if (await mountOpfsIfSupported()) return;
  await engine.mountIdbfs(MOUNT_POINT);
  setBackend("idbfs");
}

export function reset() {
  initPromise = null;
  backend = null;
}

/** Whether a real folder was chosen before, so Settings can offer
 * "Reconnect" instead of "Choose folder". */
export async function hasStoredFolder() {
  return Boolean(await idbGet(HANDLE_KEY).catch(() => null));
}

export async function chooseFolder() {
  if (typeof window.showDirectoryPicker !== "function") {
    throw new Error("This browser can't grant access to a real folder — try Chrome or Edge.");
  }
  const handle = await window.showDirectoryPicker({ mode: "readwrite" });
  if (backend) await engine.unmount(MOUNT_POINT);
  await engine.mountNative(MOUNT_POINT, handle);
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
  if (backend) await engine.unmount(MOUNT_POINT);
  await engine.mountNative(MOUNT_POINT, storedHandle);
  setBackend("native");
}

/** Forgets a chosen folder (does not touch its contents). */
export async function forgetFolder() {
  await idbDelete(HANDLE_KEY).catch(() => {});
}

function resolvePath(relativePath) {
  const clean = String(relativePath || "").replace(/^\/+/, "").replace(/\/+$/, "");
  return clean ? `${MOUNT_POINT}/${clean}` : MOUNT_POINT;
}

export async function listDir(relativePath = "") {
  const entries = await engine.listDir(resolvePath(relativePath));
  return entries.sort((a, b) => {
    if (a.isDir !== b.isDir) return a.isDir ? -1 : 1;
    return a.name.localeCompare(b.name);
  });
}

export async function readFile(relativePath, encoding) {
  return engine.readFile(resolvePath(relativePath), encoding);
}

export async function writeFile(relativePath, data) {
  await engine.writeFile(resolvePath(relativePath), data);
  scheduleSync();
}

export async function deleteFile(relativePath) {
  await engine.deleteFile(resolvePath(relativePath));
  scheduleSync();
}

export async function mkdir(relativePath) {
  await engine.mkdir(resolvePath(relativePath));
  scheduleSync();
}

export async function sync() {
  if (backend) await engine.syncFs();
}

let syncTimer = null;

function scheduleSync() {
  clearTimeout(syncTimer);
  syncTimer = setTimeout(() => {
    engine.syncFs().catch((err) => console.warn("dewmini: filesystem sync failed", err));
  }, SYNC_DEBOUNCE_MS);
}

function flushSyncNow() {
  clearTimeout(syncTimer);
  engine.syncFs().catch(() => {}); // best-effort; nothing to do if it's too late
}

window.addEventListener("beforeunload", flushSyncNow);
document.addEventListener("visibilitychange", () => {
  if (document.visibilityState === "hidden") flushSyncNow();
});
