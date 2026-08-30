/* dewmini's filesystem — ported from assets/mini-ide-fs.js
 * (planning/MINI_IDE_REDESIGN.md Phase 2, DECISIONS_LOG.md 7.88), now
 * routing through the same shared assets/pyodide-engine.js Mini IDE's
 * own copy already does (DECISIONS_LOG.md 7.89), rather than talking to
 * `pyodide.FS` directly the way this file's first version did — once
 * dewmini's own Pyodide could run inside a Worker, `pyodide.FS` stopped
 * being something this module (running on the main thread) could touch
 * directly at all.
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
 */

import * as engine from "../assets/pyodide-engine.js";

const MOUNT_POINT = "/mnt/dewmini";
const SYNC_DEBOUNCE_MS = 1500;

const DB_NAME = "dewmini-fs";
const DB_VERSION = 1;
const STORE_NAME = "kv";
const HANDLE_KEY = "native-dir-handle";

// mini-ide-fs.js's own OPFS mount hands navigator.storage.getDirectory()
// straight to engine.mountNative() — mapping Pyodide's mounted view
// directly onto the origin's one shared OPFS root. Two tools doing that
// on the same origin would see and could overwrite each other's files,
// invisibly, the moment both existed — not a problem when Mini IDE was
// the only one mounting OPFS, but a real one now that dewmini does too.
// dewmini gets its own named subdirectory of that shared root instead
// (see mountOpfs() below) before handing *that* handle to the same
// engine.mountNative() Mini IDE's own real-folder mounting already uses
// — OPFS mounting and real-folder mounting are the same operation as far
// as the engine is concerned, just with a different handle source, so
// this needs no engine change at all. (Mini IDE's own un-namespaced
// mount is left as-is here — retiring it, not fixing it in place, is the
// plan per planning/MINI_IDE_AND_DEWMINI_NEXT.md §6.)
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
 * @param {Object} [options]
 * @param {(backend: string) => void} [options.onBackendChange] - called
 *   whenever the active backend changes.
 */
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

/**
 * Mounts a filesystem: a previously chosen and still-permitted real
 * folder if one is on file, otherwise OPFS, otherwise IDBFS. Requires
 * Pyodide to already be starting — engine.ensureBooted() drives that,
 * same as mini-ide-fs.js's own init() calls it — so "Files" in Settings
 * only ever shows real status once Python has actually started, the same
 * lazy-boot rule the rest of dewmini follows. Idempotent: a second call
 * returns the same in-flight/completed mount rather than mounting twice.
 */
export function init() {
  if (!initPromise) initPromise = doInit();
  return initPromise;
}

async function doInit() {
  await engine.ensureBooted();

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

/**
 * Forgets that init() ever ran, so the next call re-mounts from scratch —
 * for pairing with engine.restart(), whose fresh interpreter has nothing
 * mounted into it yet. Doesn't touch the stored folder handle (or any
 * file) itself, just this module's own "already initialized" memo.
 */
export function reset() {
  initPromise = null;
  backend = null;
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
  if (backend) await engine.syncFs();
}

/* ------------------------------------------------------------ syncing */

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
