# `assets/pyodide-worker.js`, explained

This file is the *inside* of the Web Worker every hosted dewlab page (and
dewmini, through `pyodide-engine.js`) runs Python in. It never touches
the page directly — it can't, a Worker has no access to the DOM — it only
ever talks back and forth over `postMessage`. If you've already read
[`pyodide-engine-explained.md`](pyodide-engine-explained.md), a lot of
this will look familiar: this file is the other end of that
conversation, the side that actually has Pyodide running in it.

---

## The big idea: this is where Python actually lives

Every page that uses this file — a tutorial page via `tutorial-runtime.js`,
or dewmini via `pyodide-engine.js` — creates exactly one Worker running
this file, and from that point on, Python only exists here. The page
itself never imports Pyodide or touches a Python object directly; it
sends a message describing what it wants (`"run-cell"`, `"hover-doc"`,
`"fs-write"`, and so on) and gets a message back with the answer. That
separation is what makes a genuine Stop button possible in the first
place: even if a student's code runs forever, it's only blocking *this*
thread, and the page stays completely responsive.

The one thing that *does* cross the thread boundary without going through
a message is the interrupt buffer — a small piece of `SharedArrayBuffer`
memory both sides can see at once, which is how Stop actually works (see
`self.onmessage`'s `"set-interrupt-buffer"` handler, and its own comment,
for how that's wired up).

---

## Reading order

1. **The module comment at the top** explains why this file exists at all
   and what changed by moving Pyodide off the main thread — read that
   first.
2. **Module state** — `pyodide`, `tools`, `inspectModule`,
   `builtinsModule`, `jediHoverFn`, `jediSignatureFn`: everything this
   worker keeps alive between messages.
3. **Code intelligence** — `lookupLiveName`, `docFor`, `signatureFor`
   (looking things up that have already run), `jediDoc`/`jediSignature`
   (looking things up in code that hasn't run yet), and `hoverDoc`/
   `signatureHelp`, which combine the two — live always wins, Jedi only
   fills the gap live can't reach.
4. **`pageNames`** — the list behind autocomplete.
5. **Jedi setup** — `JEDI_HELPER_SOURCE` (real Python source defining two
   small helpers) and `loadJedi()`, which runs it.
6. **`boot()`** — starts Pyodide, loads packages, loads
   `tutorial_tools.py`, sets up the shared namespace (`RESEED_GLOBALS_SOURCE`),
   and, only if the boot message set `msg.seedDb` (dewmini only —
   `assets/pyodide-engine.js`'s `bootWorker()` is the only caller that
   ever sets it), seeds the dewmini-only `db` global too
   (`SEED_DEWMINI_DB_SOURCE`, DECISIONS_LOG.md 7.118 — a fresh, in-memory
   `sqlite3` connection a SQL cell runs against and an ordinary Python
   cell can read under the same name). `resetPageState()` further down
   re-seeds both the same way, reading the `seedDewminiDb` flag `boot()`
   set rather than needing the caller to say so again on every reset.
   This file is shared with the hosted tutorial pages
   (`assets/tutorial-runtime.js` boots through it too), which is exactly
   why `db` is gated behind a flag rather than always created — a
   tutorial page's own boot message never sets `seedDb`, so it never gets
   one.
7. **`runCell()`** — runs one cell and streams its output back as it
   happens. What it actually runs is whatever code the calling page
   handed it — for a dewmini SQL cell, that's already been turned into a
   generated `tutorial_tools._run_sql_cell(db, …)` call before it ever
   reaches this file (`compose/dewmini.js`'s `buildSqlCellCode()`); this
   worker has no idea a SQL cell exists, which is deliberate — see
   [`dewmini-js-explained.md`](dewmini-js-explained.md).
8. **Filesystem** (dewmini only — a
   tutorial page has no filesystem to mount) — `fsMountNative`/`fsMountOpfs`/
   `fsMountIdbfs` (the three storage backends), `fsSync`, `fsUnmount`,
   and the plain file operations `fsList`/`fsRead`/`fsWrite`/`fsDelete`/
   `fsMkdir`. `db`-seeding above follows the same "purely additive,
   gated on who actually asks" shape this section already established.
9. **`self.onmessage`** at the bottom — the one entry point tying
   everything above together: reads a message's `type`, calls the
   matching function, and posts a `"response"` back (or an `"error"` if
   something threw).

---

## Two patterns worth understanding on their own

**The request/response protocol.** Every message this worker answers
follows the same shape: `{type, id, ...}` in, `{type: "response", id,
result}` (or `{type: "response", id, error}`) back. The `id` is what lets
the page side (`workerRequest()` in `pyodide-engine.js`, or its
equivalent in `tutorial-runtime.js`) match a reply to the specific
request that asked for it — since several requests could be in flight at
once, there's no other way to know which answer belongs to which
question. A few message types (`"status"`, `"jedi-ready"`, `"output"`)
are the exception: one-way pushes posted directly from `boot()`/
`runCell()`, with no `id` and no reply expected, since nothing on the
page side is waiting for them specifically.

**Live-then-static lookup.** Both `hoverDoc()` and `signatureHelp()`
combine two genuinely different techniques. "Live" (`docFor`/
`signatureFor`) means asking Python's own `inspect` module about an
object that has actually run and exists right now — accurate, but only
works for code that already executed. "Static" (`jediDoc`/
`jediSignature`) means asking Jedi to read the *text* of the code and
guess what a name probably means, without running anything — works on
code that hasn't run yet, but is necessarily a guess. Trying live first
and falling back to Jedi (`docFor(name) || jediDoc(...)`) gives the best
answer available in either case.

---

## Where to look for something specific

- **"How does Stop actually stop a `while True: pass`?"** — the
  `"set-interrupt-buffer"` case in `self.onmessage`, and
  `pyodide-engine.js`'s `requestInterrupt()` for the other half.
- **"Why can a page mount a real folder here, if this worker has no
  window to show a picker from?"** — `fsMountNative`'s comment: the
  folder picker (`window.showDirectoryPicker()`) has to run on the main
  thread, but the resulting `FileSystemDirectoryHandle` is
  structured-cloneable, so it's obtained on the page and then sent here
  over `postMessage` like any other message payload.
- **"What happens if a cell's code raises an error?"** — nothing special
  here: `tutorial_tools.py`'s own `run_cell()` catches it, renders it,
  and returns normally. A `throw` reaching this file's `runCell()` means
  something broke in the plumbing itself, not in the student's code, and
  is left to propagate to `self.onmessage`'s own `catch`/`fail()`.
