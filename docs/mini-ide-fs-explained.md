# `assets/mini-ide-fs.js`, explained

This file answers one question for the rest of Mini IDE: "where do files
actually live, and how do I read and write them?" Nothing else in the
codebase — the file-tree UI, uploads, SQLite, notebook import — talks to
a filesystem directly. They all go through this file instead, so none of
them need to know or care which of three very different storage systems
is actually backing things at the moment.

---

## The big idea: three backends, one interface

A browser can't just give a web page access to "the" filesystem the way a
desktop app can — for good reason, since a random web page having free run
of a visitor's hard drive would be a security disaster. So Mini IDE has to
choose from three real options, each with different tradeoffs, and this
file is what hides that choice from everything else:

1. **A real folder on the student's computer**, via the File System
   Access API (`window.showDirectoryPicker`). The best option — a real,
   visible folder — but it only works in Chromium-based browsers, and the
   student has to explicitly grant it (there's no way to ask for this
   permission without a fresh click).
2. **OPFS** (Origin Private File System) — storage the browser manages for
   this site alone. Not visible in a normal file browser, but it survives
   reloads and works without asking permission, so this is what `init()`
   reaches for by default.
3. **IDBFS** — Pyodide's own filesystem backed by IndexedDB, the fallback
   for a browser that supports neither of the above.

Every exported function in the second half of this file — `listDir()`,
`readFile()`, `writeFile()`, `deleteFile()`, `mkdir()` — works exactly the
same regardless of which of the three is active. They just turn a
friendly relative path like `"data/scores.csv"` into the real mount-point
path and hand off to `pyodide-engine.js`, which is the layer that
actually knows how to reach whichever backend booted (see
[`docs/pyodide-engine-explained.md`](pyodide-engine-explained.md)).

---

## Reading order

1. **The comment at the top of the file** lays out the three backends and
   the order they're tried in — read that first, it's the map for
   everything else.
2. **IndexedDB helpers** (`idbOpen`, `idbGet`, `idbSet`, `idbDelete`) — a
   small hand-built wrapper turning IndexedDB's callback API into
   `async`/`await`-friendly functions. Used only to remember a chosen
   folder's handle between visits — nothing else in this file (or
   elsewhere in dewlab) needs IndexedDB directly.
3. **Backend state and `init()`** — `backend`, `setBackend()`,
   `mountOpfsIfSupported()`, and `init()`/`doInit()`, which is what
   actually picks a backend when Mini IDE starts up.
4. **Choosing and reconnecting a folder** — `hasStoredFolder()`,
   `chooseFolder()`, `reconnectFolder()`, `forgetFolder()`: the functions
   behind Settings' "Choose folder" / "Reconnect" buttons (Phase 6 of the
   redesign).
5. **`reset()`** — for pairing with `pyodide-engine.js`'s `restart()`:
   after the Python interpreter restarts fresh, this file's own memory of
   "I already mounted something" has to be forgotten too.
6. **File access** (`resolvePath`, `listDir`, `readFile`, `writeFile`,
   `deleteFile`, `mkdir`) — the actual exported interface everything else
   in Mini IDE calls.
7. **Syncing** — `scheduleSync()`/`flushSyncNow()`, and the
   `beforeunload`/`visibilitychange` listeners at the bottom that make
   sure a write isn't lost if the student closes the tab right after it.

---

## Two patterns worth understanding on their own

**"Try the best option, then the next, then the last resort."** `init()`
never assumes a browser supports everything — it tries a previously
granted real folder first, falls through to OPFS if that's unavailable
or was never granted, and falls through again to IDBFS if OPFS isn't
supported either. Each backend attempt reports success or failure rather
than throwing, specifically so this fallback chain can just be a
straightforward sequence of `if` checks in `doInit()`, without a tangle
of try/catch around every step.

**Debounced syncing.** OPFS and a real folder write through to storage
immediately, but IDBFS needs an explicit sync step to actually persist
anything — and even for the backends that don't need it, calling
`syncFs()` after every single write would be wasteful if a cell is
writing many lines in a loop. `scheduleSync()` solves this the same way a
search box debounces "wait until the student stops typing" before
searching: each call resets a timer, so a burst of writes in quick
succession costs one real sync, not one per write. The tradeoff is that a
write could still be waiting in that timer when the student closes the
tab — which is exactly why `flushSyncNow()` exists and gets wired up to
`beforeunload` and `visibilitychange` at the bottom of the file.

---

## Where to look for something specific

- **"Why did my file disappear after reload?"** — check `getBackend()`
  (or Settings' storage-status section, which calls it). If it's
  `"idbfs"` and a sync never had a chance to run (tab closed very
  quickly, or `flushSyncNow()`'s listeners didn't fire for some reason),
  a very recent write can be lost — the tradeoff mentioned above.
- **"How does 'Reconnect folder' work?"** — `reconnectFolder()`. It's
  different from `chooseFolder()` in one important way: it re-requests
  permission on a folder the student *already* picked before (stored via
  `idbSet(HANDLE_KEY, handle)`), rather than opening the picker again.
- **"Why do some functions need to be called from a click handler?"** —
  `window.showDirectoryPicker()` and `handle.requestPermission()` both
  require a recent, genuine user gesture (a click) to work at all — a
  browser security rule stopping a page from silently asking for folder
  access whenever it wants. `chooseFolder()` and `reconnectFolder()`'s own
  comments flag this.
