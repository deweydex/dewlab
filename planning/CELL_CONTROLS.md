# A cell's own controls: where they sit, and whether "Run" can become "Stop"

Design note covering a shipped change (the bar's position and the hint's
behaviour) and a finding that stopped a second one before it was built (a
genuine interrupt for a running cell).

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

## 2. "Run" becoming "Stop" while a cell runs: not built, and here is why

The request: while a cell is running, the Run button becomes a Stop
button, in case a cell runs long enough that a reader wants to give up on
it rather than wait.

**This cannot be built as asked, not "is hard to build" but genuinely
cannot, given how Pyodide runs here today.** `tutorial-runtime.js` loads
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

**What would actually make this possible**: running Pyodide inside a Web
Worker instead of the main thread, with `pyodide.setInterruptBuffer()`
pointed at a `SharedArrayBuffer` a "Stop" click writes an interrupt signal
into — Pyodide's own documented mechanism for exactly this, and the
reason it works from a Worker and not from the main thread is that writing
to the buffer and running the Python are then two different threads, so
the click can be handled and acted on regardless of what the Python side
is doing.

**Why this is a much bigger PR than a button**, not a detail to wave past:

- `SharedArrayBuffer` requires the page to be served with
  `Cross-Origin-Opener-Policy: same-origin` and
  `Cross-Origin-Embedder-Policy: require-corp` response headers — real HTTP
  headers, not something a static file or a `<meta>` tag can set. GitHub
  Pages, this project's actual host (`ARCHITECTURE.md`), does not let a
  repository configure response headers at all. The common workaround is a
  same-origin service-worker shim ("coi-serviceworker") that intercepts
  requests and adds the headers itself — a real piece of infrastructure to
  add and maintain, not a config flag.
- Every place `tutorial-runtime.js` currently talks to Pyodide directly —
  `_page_globals`, `docFor`, `pageNamesCompletion`, the widget bridge in
  `tutorial_tools.py`, autocomplete's live-namespace source — would need
  to cross a postMessage boundary instead of being an ordinary function
  call, since none of that state lives on the main thread anymore.
- This is the same category of option `planning/CELL_TOOLTIPS.md` already
  weighed and set aside for Jedi-in-Pyodide: real, documented,
  used elsewhere — and a genuinely larger architectural change than the
  feature it enables looks like it should cost.

**Recommendation: do not build this now.** The bar/hint change above ships
on its own; the interrupt question is real but belongs as its own tracked
decision — `QUESTIONS.md` has it — rather than attempted as a quick
addition to a UI-layout fix. Nothing about shipping the layout change
forecloses building the Worker migration later if it turns out to be worth
its real cost.

## 3. What a reader gets today, without the Worker migration

Worth stating plainly rather than leaving as a silent gap: a cell that
truly never returns still freezes the tab, same as before this document.
The browser's own "Page Unresponsive" handling is the only recourse, same
as it is for any other page running JavaScript (or, here, WASM) that never
yields. Nothing in this change makes that better or worse — it was already
true, and fixing it is exactly the Worker migration in §2, not something
achievable alongside it.
