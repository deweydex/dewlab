/* Mini IDE's filesystem — planning/MINI_IDE_REDESIGN.md Phase 2.
 *
 * One small interface (init, listDir, readFile, writeFile, deleteFile,
 * mkdir, sync) sitting between a mounted Pyodide filesystem and every
 * feature that touches files (the file manager UI, uploads, SQLite,
 * notebook import) — none of those need to know which backend is active.
 * All calls go through mini-ide-engine.js, since the mounted filesystem
 * lives wherever Pyodide itself lives (inside the Worker in worker mode).
 *
 * Three backends, tried in this order:
 *   1. A real local folder, via the File System Access API
 *      (window.showDirectoryPicker + pyodide.mountNativeFS). Chromium
 *      only, and only ever entered when a student explicitly asks for it
 *      (chooseFolder()) — never silently, since the picker needs a user
 *      gesture and showDirectoryPicker() throws without one.
 *   2. OPFS (navigator.storage.getDirectory()) — persistent, no picker,
 *      no permission prompt, broadly supported (Chrome/Edge/Safari/
 *      Firefox). This is what init() mounts by default, so the file
 *      manager, SQLite, and notebook import all work out of the box
 *      before a student ever opens Settings.
 *   3. IDBFS — the universal fallback for a browser with neither.
 *
 * A real folder is an upgrade a student opts into later (Settings, Phase
 * 6), not the default init() reaches for on its own — same reasoning as
 * the picker itself: no unprompted permission dialogs on page load.
 */

import * as engine from "./mini-ide-engine.js";

const MOUNT_POINT = "/mnt/mini-ide";
const SYNC_DEBOUNCE_MS = 1500;

const DB_NAME = "mini-ide-fs";
const DB_VERSION = 1;
const STORE_NAME = "kv";
const HANDLE_KEY = "native-dir-handle";

/* ------------------------------------------------------------- IndexedDB
 * A FileSystemDirectoryHandle is structured-cloneable, so it can be
 * stored as an IndexedDB value directly — the standard way to persist
 * File System Access API access across reloads. No IndexedDB helper
 * exists elsewhere in this codebase (dewlab has never needed one before
 * this), so this is a small purpose-built one, not a shared utility. */

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

/** @type {"native"|"opfs"|"idbfs"|null} null until init() resolves. */
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
 *   whenever the active backend changes (init, chooseFolder, reconnect).
 */
export function configure(options = {}) {
  onBackendChange = options.onBackendChange || (() => {});
}

async function mountOpfsIfSupported() {
  if (!("storage" in navigator) || typeof navigator.storage.getDirectory !== "function") return false;
  try {
    await engine.mountOpfs(MOUNT_POINT);
    setBackend("opfs");
    return true;
  } catch (err) {
    console.warn("mini-ide: OPFS mount failed, falling back to IndexedDB storage", err);
    return false;
  }
}

let initPromise = null;

/**
 * Boots the engine if needed, then mounts a filesystem: a previously
 * chosen and still-permitted real folder if one is on file, otherwise
 * OPFS, otherwise IDBFS. Safe to call with no user gesture — never
 * touches window.showDirectoryPicker() itself. Idempotent: a second call
 * returns the same in-flight/completed mount rather than mounting twice
 * (which Pyodide's FS would reject — a path can't be mounted over
 * itself).
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
      /* 'prompt' or 'denied': can't silently re-request permission without
       * a user gesture. Falls through to OPFS/IDBFS below; the Settings
       * storage section (Phase 6) offers reconnectFolder() for this. */
    } catch (err) {
      console.warn("mini-ide: a previously chosen folder is no longer usable", err);
      await idbDelete(HANDLE_KEY).catch(() => {});
    }
  }

  if (await mountOpfsIfSupported()) return;
  await engine.mountIdbfs(MOUNT_POINT);
  setBackend("idbfs");
}

/**
 * Whether a real folder was chosen before, so Settings can offer
 * "Reconnect" instead of "Choose folder".
 */
export async function hasStoredFolder() {
  return Boolean(await idbGet(HANDLE_KEY).catch(() => null));
}

/**
 * Lets a student opt into a real local folder. Must be called directly
 * inside a click handler — showDirectoryPicker() throws without a fresh
 * user gesture.
 */
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

/**
 * Re-grants permission on a previously chosen folder. Must also be
 * called inside a click handler, same as chooseFolder().
 */
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

/* --------------------------------------------------------- file access */

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

/**
 * @param {string} relativePath
 * @param {"utf8"} [encoding] - omit to get raw bytes back (a Uint8Array).
 */
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

/* ------------------------------------------------------------ syncing
 * mountNativeFS-backed filesystems (real folder or OPFS) and IDBFS alike
 * need an explicit flush to actually persist a write — debounced here so
 * a burst of writes (a cell running a loop of file.write() calls) costs
 * one sync, not one per call, plus a best-effort flush on the way out. */

let syncTimer = null;

function scheduleSync() {
  clearTimeout(syncTimer);
  syncTimer = setTimeout(() => {
    engine.syncFs().catch((err) => console.warn("mini-ide: filesystem sync failed", err));
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
