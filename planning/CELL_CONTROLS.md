# A cell's own controls: where they sit, and whether "Run" can become "Stop"

Design note covering two shipped changes: the bar's position and the
hint's behaviour (§1), and — following the finding in §2 below that
stopped it from being built as a quick addition — the Worker migration
that made a genuine interrupt possible after all (§2, updated;
`DECISIONS_LOG.md` 7.77).

---

## 1. What changed: the bar moved, and the hint stopped floating

Two real usability problems, reported directly: the hint's "?" opened a
popover that floated over the editor or output below it rather than
making room for itself, and the cell's controls (slug, hint, reset, run)
sat above the code — read top to bottom, a reader met the controls for
code they had not read yet.

**The bar now sits below the editor and the output**, not above them —
`render_cell()`'s markup order changed, nothing about how the runtime
wires to it did, since every binding (`.dl-editor`, `.dl-output`,
`.dl-btn-run`, `.dl-btn-reset`) is a class lookup via `querySelector`, not
a DOM-position assumption.

**The hint is now a click toggle, not a hover popover.** The old
`.dl-hint-text` was `position: absolute`, shown on `:hover`/`:focus-within`
— which is exactly what could float over content below it, and gave a
touch reader no way to open it at all (`:hover` does not fire on touch).
It is now a plain block, `hidden` by default, opened by a real click on
`.dl-hint-icon` (`aria-expanded`, toggled in `tutorial-runtime.js` rather
than by pure CSS) — opening it grows `.dl-cell` and pushes whatever comes
after the cell down the page, the same "push down, cover nothing" shape
the prose-level `<details class="dl-hint">` fold already has, arrived at
by a different mechanism because a `<details>` element does not fit
naturally as one icon inside a horizontal control bar.

## 2. "Run" becoming "Stop" while a cell runs

The request: while a cell is running, the Run button becomes a Stop
button, in case a cell runs long enough that a reader wants to give up on
it rather than wait.

**Now built, on the hosted site — `DECISIONS_LOG.md` 7.77.** The finding
below, that this could not be built as a small addition, was correct at
the time and is kept as-written since the reasoning still explains *why*
the fix had to be the size it was: a full Worker migration
(`assets/pyodide-worker.js`), not a button. `dewlab.canStop()` reports
whether the current page actually has it — cross-origin isolation landed
and a `SharedArrayBuffer` was allocated — and the button only ever offers
Stop when that is true. The offline, downloadable export deliberately
keeps the old main-thread path below and has no Stop button: a `file://`
page cannot load a module Worker, and the export was never going to be
left running long enough to need one.

**This could not be built as asked, not "is hard to build" but genuinely
could not, given how Pyodide ran here at the time.** `tutorial-runtime.js` loads
and runs Pyodide directly on the page's own main thread — confirmed by
reading `boot()` and `runCell()`, and by there being no `Worker` anywhere
in the codebase (`grep -r Worker assets/` finds nothing). A single Python
statement executing inside Pyodide's WASM runtime is synchronous from the
browser's point of view: while it runs, the same thread that would need to
handle a "Stop" button's click event is the thread running the student's
Python. A genuine infinite loop does not yield back to the browser between
iterations, so there is no point at which a click handler could even fire
— the button would be visually present but the browser could not process
input on it until the loop ends on its own or the browser's own "page
unresponsive" mechanism intervenes (which already exists today, native to
every browser, and is the de facto stop button a reader already has for a
true runaway loop).

**What made this possible**: running Pyodide inside a Web Worker instead
of the main thread, with `pyodide.setInterruptBuffer()` pointed at a
`SharedArrayBuffer` a "Stop" click writes an interrupt signal into —
Pyodide's own documented mechanism for exactly this, and the reason it
works from a Worker and not from the main thread is that writing to the
buffer and running the Python are then two different threads, so the
click can be handled and acted on regardless of what the Python side is
doing.

**Why this was a much bigger PR than a button**, not a detail to wave past:

- `SharedArrayBuffer` requires the page to be served with
  `Cross-Origin-Opener-Policy: same-origin` and
  `Cross-Origin-Embedder-Policy: require-corp` response headers — real HTTP
  headers, not something a static file or a `<meta>` tag can set. GitHub
  Pages, this project's actual host (`ARCHITECTURE.md`), does not let a
  repository configure response headers at all. The workaround built:
  `coi-serviceworker`, a same-origin service-worker shim (vendored into
  `assets/vendor/`, registered from `shell.html`) that intercepts requests
  and adds the headers itself.
- Every place `tutorial-runtime.js` used to talk to Pyodide directly —
  `_page_globals`, `docFor`, `pageNamesCompletion`, the widget bridge in
  `tutorial_tools.py`, autocomplete's live-namespace source — now crosses
  a postMessage boundary (`assets/pyodide-worker.js`) instead of being an
  ordinary function call, since none of that state lives on the main
  thread on the hosted site anymore.
- This was the same category of option `planning/CELL_TOOLTIPS.md` had
  already weighed and set aside for Jedi-in-Pyodide: real, documented,
  used elsewhere — and it turned out to be worth its real cost, built
  alongside Jedi rather than instead of it.

**Built: `DECISIONS_LOG.md` 7.77.** The bar/hint change above shipped on
its own first; the interrupt question was tracked in `QUESTIONS.md` and
answered there once the Worker migration landed, rather than attempted as
a quick addition to the UI-layout fix.

## 3. What a reader gets today

**On the hosted site**, a Stop button actually works: `dewlab.canStop()`
gates it on cross-origin isolation having genuinely landed for the current
page, so a browser or first visit where `coi-serviceworker` has not yet
taken effect (it needs one reload after its first registration) never
shows a Stop button it could not honor — that page still behaves exactly
as described below until the reload happens.

**On the offline, downloadable export**, and on any hosted page before
isolation has landed, a cell that truly never returns still freezes the
tab. The browser's own "Page Unresponsive" handling is the only recourse,
same as it is for any other page running JavaScript (or, here, WASM) that
never yields. The export was left on the old main-thread path
deliberately — see §2 — not as a remaining gap.
