# `compose/js-cell-engine.js`, explained

This file is a JavaScript cell's whole execution model — one persistent
sandboxed session the entire notebook shares, created lazily on first run.
It plays the same role for a JavaScript cell that
[`assets/pyodide-engine.js`](pyodide-engine-explained.md) plays for a
Python one, but the two look very different inside: Python needs a Worker
and a downloaded interpreter; a JavaScript cell's own engine is already
sitting inside the browser, so the whole file is a few hundred lines
managing one `<iframe>` and a small `postMessage` protocol, not a
worker/main-thread split.

---

## The big idea: a sandboxed iframe is already a separate realm

`assets/pyodide-engine.js` needs a Worker to get Python off the main
thread and to isolate one page's Python from another's. A `<iframe
sandbox="allow-scripts">` with no `allow-same-origin` gets both of those
for free — an opaque-origin document that cannot reach this page's own
DOM, `localStorage`, or any other cell, the identical isolation
`compose/dewmini.js`'s own HTML cell preview already relies on. That is
why this file has no Worker of its own: there is no interpreter boundary
left for one to add.

What a Worker buys Python that this file cannot match: a genuine Stop
button. Pyodide's Worker checks a shared `SharedArrayBuffer` periodically
while running, so a runaway loop can be interrupted from outside. This
iframe still executes on the tab's own main thread — a runaway loop here
freezes the whole page exactly the way Pyodide's own main-thread fallback
does. `canStop()` is unconditionally `false` for that reason, not because
it was left unfinished.

---

## Reading order

1. **The file banner at the top** is the most important reading in this
   file — it explains the sandboxing choice above, and walks through the
   one genuinely subtle design decision here: why each cell's code runs
   through indirect `eval` rather than an inserted `<script>` tag, and
   what that trades away. Read it before anything else; the rest of this
   document assumes it.
2. **Module state** — `frame` (the iframe itself, once created),
   `readyPromise` (memoizes `ensureSession()` the same way
   `engine.ensureBooted()` memoizes Pyodide's own boot), `pendingRun`
   (the one cell currently running, if any — there is never more than
   one, the same one-session-at-a-time rule Python's own interpreter
   has).
3. **`RUNTIME_SRC`** — not JavaScript that runs in this file at all, but
   a string of HTML+JS that becomes the iframe's `srcdoc`. Read this as a
   small, separate program: everything inside it runs *inside the
   sandboxed iframe*, in its own realm, not here. It owns three jobs:
   relaying `console.log()` calls back to the parent as output,
   reporting an uncaught error or an unhandled promise rejection the same
   way, and running a cell's code on a `"run"` message via `(0,
   eval)(code)` wrapped in a `try`/`catch`.
4. **`handleMessage()`** — the one place this file listens for messages
   from the iframe: an `"output"` event goes straight to
   `applyOutputEvent()` (imported from `assets/pyodide-engine.js` — see
   "Two patterns" below for why that import is safe), a `"done"` event
   resolves whichever `runCell()` call is waiting on it.
5. **`ensureSession()`** — creates the iframe the first time a JavaScript
   cell actually runs, wires up `handleMessage`, and waits for the
   iframe's own runtime script to announce `{type: "ready"}` before
   resolving. `sessionReady()` beside it is just `frame !== null`, read by
   `compose/dewmini.js` to decide whether "JavaScript ready." (and a
   second line in Settings' own execution-status text) is worth showing.
6. **`runCell()`** — the exported entry point `compose/dewmini.js`'s
   `executeCell()` calls. Ensures the session, clears the cell's previous
   output (`clearOutput()`, also imported from `pyodide-engine.js`), then
   posts a `"run"` message and returns a Promise that `handleMessage()`'s
   `"done"` handling resolves.
7. **`canStop()`/`requestInterrupt()`** — always `false` and a no-op,
   respectively; see the file banner and "The big idea" above for why. They
   exist so `compose/dewmini.js` can ask either engine the same question
   through one dispatcher (`canStopFor(cell)`/`requestInterruptFor(cell)`)
   without a special case for this one.
8. **`restart()`** — tears the iframe down entirely: removes it, drops
   the message listener, resolves any pending run as failed. Called from
   `compose/dewmini.js`'s own `restartPython()`, and from `runCellBatch()`
   whenever a batch resets (`reset: true` — "Run all"/"Run above"), since
   there is no cheaper way to clear a JavaScript session the way
   `engine.resetPageState()` cheaply clears Pyodide's.

---

## Two patterns worth understanding on their own

**Indirect `eval`, and the bug it fixes.** The obvious way to run a
cell's text as JavaScript is to insert it as a `<script>` element. That
was the first version of this file, and it was wrong: a `<script>`
tag's own top-level `let`/`const` declarations join the realm's *one,
permanent* global lexical environment, so re-running an edited cell a
second time — an entirely ordinary thing to do — throws `SyntaxError:
Identifier 'x' has already been declared`. Indirect eval —
`(0, eval)(code)`, called rather than written as a bare `eval(code)`
(direct eval would run in the *caller's* scope and behave differently) —
sidesteps this: per spec, indirect eval's own top-level `let`/`const`
bindings live in a scope private to that one call, so a cell can always
be re-run safely. The trade-off is real and worth remembering when
reading this file: only `var` and `function` declarations persist across
separate cells (they still attach to the real global object, the same as
a `<script>` tag's would); a `let`/`const` from one cell is gone the
moment that cell's `eval()` call returns, invisible to a later cell even
though it worked fine within its own cell. `DECISIONS_LOG.md` 7.119 has
the full story, including how this was actually found (re-running a
`let`-declaring cell in a real browser during verification, not by
reading the code).

**Reusing `assets/pyodide-engine.js`'s own output plumbing.** This file
imports `applyOutputEvent`/`clearOutput` from `pyodide-engine.js` rather
than keeping a second copy of the same ~25 lines. That is safe because
both files run in the exact same JS realm as `compose/dewmini.js` itself
— unlike `assets/pyodide-worker.js`, which duplicates similar logic
because a *Worker* genuinely cannot reach a constant defined in another
file's module scope, there is no such boundary here. Both engines are
configured with the same cellId → output-element lookup
(`compose/dewmini.js`'s single `engine.configure({getOutputEl, ...})`
call wires it for both, since `js-cell-engine.js` reads the same
module-level `getOutputEl` `pyodide-engine.js` already has), and a given
cellId is never running through both engines at once — a cell has
exactly one type — so there is nothing for the two to actually contend
over.

---

## Where to look for something specific

- **"Why doesn't a JavaScript cell support `await` at its own top
  level?"** — the file banner's own closing paragraph: wrapping a cell's
  code in an `async` function to allow it would swallow its own top-level
  `var`/`function` declarations into that function's scope instead of the
  global one, losing the one persistence guarantee this design does keep.
- **"What happens to a `console.log()` call after the cell it came from
  has already finished?"** — it still reports, tagged with whichever
  cell last ran (`RUNTIME_SRC`'s own `currentCellId` is never cleared,
  only ever reassigned by the next `"run"` message) — late/async output
  is a known, accepted limitation, not a bug; see `DECISIONS_LOG.md`
  7.119.
- **"Why is the iframe never visible?"** — `frame.style.display = "none"`
  in `ensureSession()`. Unlike an HTML cell's own sandboxed preview
  iframe, this one is a headless execution session — its output is
  relayed back into a cell's ordinary `.dm-cell-output` area, not shown
  as a little page of its own.
