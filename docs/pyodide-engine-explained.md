# `assets/pyodide-engine.js`, explained

This file is Mini IDE's connection to Python. It doesn't draw anything on
the page — that's [`assets/mini-ide.js`](mini-ide-js-explained.md)'s job —
and it doesn't decide where files are stored — that's
[`assets/mini-ide-fs.js`](mini-ide-fs-explained.md)'s job. What it does is
answer three questions for the rest of the app: "start Python," "run this
code," and "what does this name mean," without the caller needing to know
*how* Python is actually running underneath.

That "how" turns out to have two real answers, and understanding that is
the key to reading this whole file.

---

## The big idea: two engines wearing one interface

Mini IDE tries to run Python inside a **Web Worker** — a separate thread,
so a runaway loop in a student's code never freezes the page, and a real
Stop button can interrupt it. But a Worker can't always be created (most
notably when Mini IDE is opened straight from a `file://` path on disk,
which some browsers restrict). When that happens, this file falls back to
running Pyodide directly **on the main thread** instead — the same Python,
the same `tutorial_tools.py`, just without a genuine Stop button, since a
loop running on the same thread as everything else blocks that thread
completely.

Both paths exist side by side in this file:

- Everything under **"Worker path"** talks to the worker via
  `postMessage`/`onmessage`, using `workerRequest()` as the one function
  that turns "send a message" into "get a Promise back for the reply."
- Everything under **"Main-thread fallback"** (functions with an `MT`
  suffix) calls Pyodide's own APIs directly, since Python is running right
  there in the same JavaScript context.

Near the bottom, under **"the dispatcher,"** `boot()` tries the worker
first and falls back to the main thread only if that fails, recording
which one won in a module-level `mode` variable. Every exported function
after that — `runCell()`, `hoverDoc()`, `mountNative()`, and so on — is a
tiny `if (mode === "main-thread") ... else ...` that picks the matching
function from whichever section actually booted. That's the whole shape
of the file: two engines, one dispatcher, one shared public interface.

---

## Reading order

1. **Module docstring and config** — what this file is for, and
   `DEFAULT_PACKAGES`, the Pyodide packages loaded at boot.
2. **`configure()` and status/output plumbing** — how mini-ide.js hands
   this module a way to find a cell's output element and show status
   text, and `applyOutputEvent()`, which turns one "something happened in
   Python" event into real DOM, shared by both engines.
3. **Worker path** — `workerRequest()` (the request/reply pattern over
   `postMessage`), `ensureWorker()` (creates the worker, and is the *one*
   place this file listens for messages from it), `bootWorker()`,
   `requestInterrupt()` (how Stop actually stops something), and
   `runCellWorker()`.
4. **Main-thread fallback** — the Jedi-based autocomplete helpers, the
   filesystem mirror functions (`fs*MT`), and `bootMainThread()`/
   `runCellMainThread()`.
5. **The dispatcher** — `boot()`, `ensureBooted()`, `restart()`,
   `engineMode()`, `canStop()`.
6. **The exported API** — `runCell()`, `hoverDoc()`, `signatureHelp()`,
   `pageNamesCompletion()`, then the filesystem functions
   (`mountNative()` through `mkdir()`) that `mini-ide-fs.js` calls.

---

## Two patterns worth understanding on their own

**The request/reply pattern over `postMessage`.** A Worker is a genuinely
separate thread — the only way to talk to it is by sending plain messages,
and there's no built-in way to say "send this and wait for the answer."
`workerRequest()` builds that: it invents a unique id, remembers a
`{resolve, reject}` pair for that id, sends the message, and lets
`ensureWorker()`'s `onmessage` handler resolve the right pair once a
matching `"response"` message comes back. Every single thing the worker
can be asked to do — boot, run a cell, look up a hover doc, touch the
filesystem — goes through this one function.

**The interrupt buffer.** Stopping a *running* loop is a different problem
from sending it a message, because a tight loop in Python isn't checking
for new messages — it's just running. `SharedArrayBuffer` is memory both
threads can see and write to instantly, with no message needed at all;
Pyodide checks it periodically while code runs. `requestInterrupt()`
writes the number Pyodide treats as "this means Ctrl-C" into that shared
memory, and that alone is enough to stop even a `while True: pass` cell.
This only works when the browser actually handed out a
`SharedArrayBuffer` in the first place (see `canStop()`), which needs
cross-origin isolation — the reason Mini IDE registers a COI service
worker at all.

---

## Where to look for something specific

- **"Why doesn't Stop do anything?"** — `canStop()`; it's only true on the
  worker path with a real interrupt buffer. The main-thread fallback can
  never be interrupted mid-run.
- **"How does hover/autocomplete know what a name means?"** — two
  different techniques, tried in order on the main-thread path:
  `docForMT()`/`signatureForMT()` look up a name that's *already run* and
  ask Python's own `inspect` module about it; `jediDocMT()`/
  `jediSignatureMT()` fall back to Jedi's static analysis for names in
  code that hasn't run yet. The worker path does the same two-step lookup
  inside `pyodide-worker.js` and just returns the answer.
- **"How does a folder actually get connected to Python?"** — the
  `mount*` functions at the bottom, and their `fs*MT` counterparts
  earlier in the file. `mini-ide-fs.js` decides *which* backend (native
  folder, OPFS, or IDBFS) and calls these once it has decided; this file
  never picks a backend on its own.
- **"What happens when Restart is used?"** — `restart()`. It tears down
  whichever engine was running (terminating the worker, or just dropping
  the main-thread references) and resets `mode`/`bootPromise` so the next
  `ensureBooted()` starts a genuinely fresh interpreter.
