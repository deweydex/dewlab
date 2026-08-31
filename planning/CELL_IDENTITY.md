# Cell identity and the execution counter: a design note

Not built yet. This is the settled shape of one proposed feature — a
notebook cell that tells you, at a glance, what it is, whether it has
run, and whether its output still matches its code — kept here as the
record of *why* it looks the way it does, before any of it is wired into
`compose/dewmini.js`. Two static pages sit alongside this file, neither
needing a server or a build step to open:

- [`mockups/cell-identity.html`](./mockups/cell-identity.html) — a
  working mockup of every cell type in this design (Python, SQL, HTML,
  CSS, Text), including the live run-status timer.
- [`mockups/cell-identity-explained.html`](./mockups/cell-identity-explained.html)
  — the same design, explained in plain language for a reader new to the
  project. This document (below) assumes more context and is written for
  maintainers; that one is written to stand alone.

Four related, smaller features from the same proposal shipped already
(`DECISIONS_LOG.md` 7.105–7.108): the "edited since last run" marker,
Run above/below, Restart & run all, and maths rendering in text cells.
This document covers the one piece that was deliberately held back —
execution counters — because unlike the other four, it does not fit as a
small addition to the existing cell markup. It touches the same header
every cell already has, so it was worth designing properly rather than
bolting a number onto the side.

---

## 1. Why number a cell at all

A dewmini notebook shares one Python namespace across every cell, top to
bottom, but a reader is free to run them in any order, any number of
times, or not at all. That freedom is the whole point of a notebook —
but it means a cell's position on the page stops being a reliable guide
to what state the notebook is actually in. Two problems follow directly
from that, and both are common enough in real notebooks (dewmini's and
everyone else's) to be worth solving rather than shrugging off as
"advanced users will figure it out":

- **Which cell produced this output?** If a reader has run cell 3, then
  cell 1, then edited cell 2 without re-running it, the *order things
  actually happened in* is no longer the order they appear on the page.
  A plain running count — "this was the 1st cell to run, this the 2nd" —
  answers that directly, and it is exactly the piece of information a
  reader needs to explain a confusing result: an output that depends on
  a cell that has not, in fact, run yet.
- **Which cell is which, once cells are dragged around?** dewmini cells
  can already be reordered by drag-and-drop. Once that's possible, a
  cell needs a stable, printed identity — "cell 3" — that a reader can
  point to in conversation ("check cell 3") independent of whatever else
  is currently above or below it.

Both problems already have a *partial* answer in dewmini today —
`ranContent` (7.105) already knows whether a cell's output matches its
current code, and shows an "edited since last run" marker for it. What
it does not know is *when*, relative to the other cells, that run
happened. The execution counter is that missing half.

## 2. The identity pill: `⋮ Cell N  TYPE`

Every cell, of every type, carries a small pill in its header: a drag
handle, the word "Cell" and its number, and the cell's type in capitals.

**It says "Cell" rather than leaving the number to imply it.** A bare
number reads as decoration until you already know what it means; writing
the word costs four characters and removes the guessing.

**The type sits in the same pill as the number, not off on its own,**
because both answer the same kind of question — "what is this thing" —
before a reader has read a line of it. Splitting them into two separate
badges would ask a reader to piece two facts together that belong
together as one.

**The type gets its own colour, in addition to its own label**
(`--dl-type-python`, `--dl-type-sql`, `--dl-type-html`, `--dl-type-css`
— Python keeps the site's own orange, since it is the default and most
common type; the others each get one muted, distinguishable hue). This
is a scanning aid on top of the text, not a replacement for it — a
notebook mixing Python, SQL, and HTML cells becomes sortable by eye
without reading every label, and because the colour is layered onto a
real word rather than standing in for one, nothing is lost for a reader
who can't tell the colours apart.

**The whole pill is the drag target, not just the handle.** An earlier
version made only the three-dot handle draggable, which meant a precise,
small hit target on what was otherwise a wide, inviting-looking pill —
worse on a touchscreen than on a mouse. Since the pill already shows
exactly what would be picked up ("Cell 3, Python"), there was no reason
to make the target smaller than the thing labelling it.

**The pill's tooltip says only what the pill can't say for itself: that
it drags.** An earlier draft repeated the cell's own number and type in
the tooltip and added a sentence about which cell types run against the
shared session — both already visible as plain text once, on every cell,
and the run-order distinction is explained once for good in the rules
table further down rather than repeated on every hover.

## 3. The run line: order, duration, and staleness, folded into one

Below the code (see §5 for why it's below, not above), Python and SQL
cells — the two types that actually run against the shared session —
show a single line reporting what happened last:

- **Not yet run this session** — italic, in the muted colour, before a
  cell has ever run.
- **Ran 1st in 340 ms** — once it has, in the site's normal text colour.
  Order and duration share one line rather than two, because a reader
  reads them together anyway ("when, and how long").
- **Ran 1st in 340 ms — edited since** — the same line, once the code has
  changed since that run. This *is* `ranContent`'s existing stale check
  (7.105); the counter design folds its badge into the run line instead
  of giving it a separate one, since both are facts about the same run.
- **Running… 1.6 s**, ticking live while the cell is actually executing,
  and **Running next** for a cell about to run as part of a batch (Run
  above/below, Restart & run all). The live figure updates on a plain
  timer, not as an `aria-live` region — announcing a number changing ten
  times a second would be noise, not information, for anyone using a
  screen reader.

Cell types that never run against the session — Text, HTML, CSS-as-styling
— have nothing to report here and show no run line at all
(`RUNS_AGAINST_SESSION = {python, sql}` in the mockup). A cell that
cannot be stale should not have a line implying it could be.

## 4. What differs by cell type, and why

Not every cell needs every affordance, and giving one to a cell that
can't use it is worse than simply leaving it off — it invites a reader
to wonder what it does. Four things vary by type:

| | Python | SQL | HTML | CSS | Text |
|---|---|---|---|---|---|
| Numbered, coloured pill | yes | yes | yes | yes | yes |
| Drag target | yes | yes | yes | yes | yes |
| Run line (order/duration/stale) | yes | yes | — | — | — |
| Collapse triangle | yes | yes | — | yes | — |
| Edit / View toggle | — | — | yes | — | yes |
| Quiet until touched | — | — | yes | — | yes |

**Collapse** exists wherever there is code worth hiding — Python, SQL,
and CSS-as-source. HTML and Text don't get it because they already have
a rendered form to shrink down to (see next).

**Edit/View, and staying quiet until touched,** belong to Text and HTML
only — the two types meant to be *read*, not run. Like a Markdown cell in
any other notebook tool, they render by default and hide their source
until a reader deliberately asks for it (a click to reveal the chrome, a
double-click to edit) rather than sitting open and code-shaped among
cells that are. Their controls are not removed while quiet, only made
invisible — `opacity: 0; pointer-events: none`, not `display: none` — so
a keyboard user tabbing through the page can still reach and open them;
only a mouse user actually needs to hover first.

## 5. Where the controls sit

Run, reset, and the "run above/below" menu sit at the bottom-left of the
cell, under the code, not above it — the same place `build.py`'s
`render_cell()` already puts a tutorial page's own Run/Reset bar, and the
same reasoning applies here: a reader's cursor is at the bottom of what
they just wrote, not back at the top, so that is where the next action
should be waiting. The collapse triangle sits to the left of the code, its
own box top-aligned with the first line of code (or text) beside it,
achieved by making both siblings of the same flex row rather than
nudging one with a margin — the more reliable way to keep two things
level than hand-tuning spacing between two separate elements.

## 6. What this deliberately doesn't do

- **No execution-order graph or arrows between cells.** A plain ordinal
  ("Ran 1st", "Ran 2nd") answers "when did this run" without building a
  visualisation of dependencies dewmini has no way to actually know (it
  does not trace which cell's variables another cell reads).
- **No keyboard equivalent for drag-and-drop.** Reordering cells still
  has no non-mouse, non-touch path. Worth flagging honestly rather than
  leaving it to be discovered later — a future pass should give cells a
  "move up" / "move down" action reachable from the keyboard, independent
  of this design.

## 7. What's still open

- **Implementation.** Everything above is design, not code. The
  groundwork it would build on already exists — `ranContent` and the
  staleness check (7.105), `runCellBatch()`/`runAbove()`/`runBelow()`
  (7.106), `restartPython()` (7.108) — but the counter itself, the pill,
  and the per-type behaviour split are not wired into
  `compose/dewmini.js` yet.
- **Tutorial and practice pages.** This design is dewmini-only so far.
  Carrying it to the reading pages a tutorial builds (`build.py`'s
  `render_cell()`) is a larger piece of work on its own, and would need
  cell types dewmini doesn't have today — a tutorial page currently
  distinguishes only "has a Run button" from "does not," not Python from
  SQL from HTML. The same instinct that makes a Text cell go quiet until
  touched here should carry over directly: a tutorial's own prose-like
  cells (Markdown-shaped, non-executable) ought to fade their chrome away
  the same way, rather than looking like every other numbered, run-tracked
  cell around them.
