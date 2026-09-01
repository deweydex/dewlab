# Cell identity and the execution counter: a design note

**Built in `compose/dewmini.js` (7.110).** This is the settled shape of
a notebook cell that tells you, at a glance, what it is, whether it has
run, and whether its output still matches its code — kept here as the
record of *why* it looks the way it does. `compose/dewmini.js` is now
the source of truth for what actually ships, not the two static mockups
below — they capture the original proposal and have not been redrawn to
match; §4 and §7 note the real, small differences 7.110 settled on while
building it:

- [`mockups/cell-identity.html`](./mockups/cell-identity.html) — a
  working mockup of every cell type in this design (Python, SQL, HTML,
  CSS, Text), including the live run-status timer.
- [`mockups/cell-identity-explained.html`](./mockups/cell-identity-explained.html)
  — the same design, explained in plain language for a reader new to the
  project. This document (below) assumes more context and is written for
  maintainers; that one is written to stand alone.

Four related, smaller features from the same proposal shipped first
(`DECISIONS_LOG.md` 7.105–7.108): the "edited since last run" marker,
Run above/below, Restart & run all, and maths rendering in text cells —
and per 7.109, three of those four (everything but maths, which needed
nothing extra there) now also run on tutorial and practice pages'
`.dl-cell`. This document's own subject — execution counters, the
numbered identity pill — held back at first because unlike the other
four, it didn't fit as a small addition to the existing cell markup; it
touched the same header every cell already had, so it was worth
designing properly before building it, which 7.110 then did, in
dewmini first. 7.113 carried the pill and the merged run-line on to
tutorial and practice pages too, once dewmini had settled their shape,
and 7.114 followed with collapse and Duplicate — see §7 for exactly
what did and didn't come along with them, and what Duplicate ended up
meaning on a page whose cells aren't all the reader's own.

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

| | Python | SQL | HTML | CSS | JavaScript | Text |
|---|---|---|---|---|---|---|
| Numbered, coloured pill | yes | yes | yes | yes | yes | yes |
| Drag target | yes | yes | yes | yes | yes | yes |
| Header-end: Duplicate, Delete | yes | yes | yes | yes | yes | yes |
| Run line (order/duration/stale) | yes | yes | — | — | yes | — |
| Collapse triangle | yes | yes | **yes** | **yes** | yes | yes |
| Edit / View toggle | — | — | yes | yes | — | yes |
| Quiet until touched | — | — | yes | yes | — | yes |

Collapse settled as "every type" once Text actually shipped it (§4's own
amendment, just below); §8 settles the rest, including JavaScript, which
this table never covered until it existed to design against.

**Header-end** is Duplicate and Delete, on every cell, plus an Edit
toggle for Text and HTML only — settled on while building 7.110, not
fully spelled out when this table was first written. Duplicate inserts
a copy of the cell right after itself, same type and code, no run
history: a starting point for a variation, not a claim that the copy
already ran.

**Collapse, amended: every cell type gets it, code-bearing or not (built
this way in dewmini, 7.110).** The reasoning below explains why HTML
doesn't need it — a rendered form already exists to shrink to — but a
Text cell caught in *edit* mode has no such fallback, and "shrink this
out of the way without deleting it" is exactly as true for a long note
as for a long function. HTML may still turn out not to need one, once it
exists; Text does.

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

**One rotated chevron, not two swapped triangles (7.110).** The mockups
use ▾/▸, filled triangles swapped between expanded and collapsed. Once
actually built, with the footer's own ▶ Run button sitting only a line
or two below it, two different filled triangles in the same corner of
the cell read as confusingly similar. dewmini instead rotates a single
`›` 90° between states — the same glyph throughout, its orientation
carrying the state rather than its shape.

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

- **Implementation: done in dewmini, for the two cell types that exist
  there (7.110).** The numbered, coloured pill; the merged run-line,
  including the live "Running…"/"Running next" states and the run-order
  counter (`runSequenceCounter`, reset on any namespace reset, not only a
  full restart); the collapse triangle, on every cell type per this
  document's own amendment above; and the header-end group, Duplicate —
  a genuinely new feature — included. `ranContent`/staleness (7.105),
  `runCellBatch()`/`runAbove()`/`runBelow()` (7.106), and
  `restartPython()` (7.108) turned out to be exactly the groundwork this
  needed, unchanged.
- **SQL, HTML, CSS, JavaScript: designed in §8, being built from there
  outward, in dewmini only, one type at a time (starting with HTML).**
  This document's own multi-type table was a design for when they
  exist, not a claim that they do — §8 is where "when they exist" turns
  into an actual execution model per type, since the table alone only
  ever answered *what chrome a cell gets*, never *what running one
  does*. `--dl-type-python`/`--dl-type-text` were the only colour tokens
  defined until §8 added four more.
- **Tutorial and practice pages: the pill and the run line are now ported
  too (7.113).** 7.109 ported the run-line-adjacent pieces (staleness,
  run above/below, restart & run all) onto `build.py`'s
  `render_cell()`/`assets/tutorial-runtime.js`, keeping dewmini's and the
  tutorial runtime's own engines and DOM separate rather than unifying
  them — see that decision for why a full shared cell implementation was
  explicitly not the chosen path. 7.113 carried the pill (`Cell N`,
  coloured "Python" type) and the merged run-line (order, duration,
  staleness, live "Running…"/"Running next") over the same way, replacing
  the plain `.dl-cell-id` text and the separate stats/stale-badge pair
  7.109 had used. The pill's number is different in kind from dewmini's,
  though: a tutorial page's cells are never reordered, so `build.py`
  gives each one its static, build-time position rather than
  live-recomputing it the way dewmini must for a draggable list — there
  is no drag handle here, because there is nothing to drag. The colour
  token is always `--dl-type-python`, since every authored cell on a
  tutorial page is Python; `--dl-type-text` and the rest stay unused
  until a real second authored type exists.

  There was never a header→footer move to make on this side, unlike
  dewmini: `build.py`'s `.dl-cell-bar` sat below the editor and output
  from the start (§5 above notes this — it's the layout dewmini's own
  7.110 moved *to*), so nothing here needed relocating.

- **Tutorial and practice pages: collapse and Duplicate too (7.114).**
  The collapse triangle now applies to every cell that has editable
  content — an authored cell's code, and both a custom python cell's
  code and a custom text cell's note-or-rendered-view — the same "every
  type gets it" reasoning §4's amendment already settled for dewmini.
  Collapsing hides only `.dl-cell-content`; the output and the bar
  beneath it stay visible, same as dewmini.

  Duplicate turned out to mean something different here than in
  dewmini, because an authored cell isn't a reader's own the way a
  dewmini cell is — it's the tutorial's own fixed content. Rather than
  skip it, Duplicate on an authored cell inserts a copy of its code as a
  new *custom* cell immediately after it — the reader's own copy to
  experiment with, the tutorial's own left untouched. This reuses
  machinery that already existed for an unrelated reason:
  `initCustomCellsSection()` already seeds a "+Code / +Text" insertion
  point after every real cell (for "Try something of your own" placed
  anywhere on the page, not only at the bottom), so Duplicate is just
  one more way of using that same seam, not a new insertion mechanism.
  Custom cells got their own Duplicate too, inserting the copy right
  after the original the same way.

- **Quiet until touched, built for the first time anywhere (7.115).**
  This document described it from §2 onward, but it was never actually
  built — not in dewmini, not here — until now. A rendered Text cell's
  chrome (dewmini's `.dm-cell-head`/`.dm-cell-collapse-col`; a custom
  text cell's own `.dl-cell-bar`/`.dl-cell-collapse-col`) stays
  `opacity: 0; pointer-events: none` until a reader hovers or focuses
  the cell, one CSS rule with no JavaScript on either side — a reader
  focusing the textarea to edit already puts the cell in `:focus-within`,
  which is exactly when the chrome should reappear. Authored cells and
  custom python cells keep their chrome on always; only Text is quiet.

## 8. SQL, HTML, CSS, JavaScript: what running one actually does

§4's table answered what chrome each type gets. It never answered the
harder question: what happens when a reader presses Run, or when a
rendered cell first appears — because none of these types existed yet
to test that question against. This section answers it, type by type,
before any of it gets built. dewmini only, for now (see the closing note
below) — building four cell types into two engines at once would be the
same mistake 7.109 explicitly declined to make for Python.

**Colour tokens.** Four new hues, alongside `--dl-type-python`/
`--dl-type-text`, each defined for light and dark the same way
`--dl-error-fg`/`--dl-pass-fg` already are rather than as a single fixed
hex — a colour picked for legibility against the light cell background
is not automatically legible against the dark one. SQL teal, HTML
violet, CSS blue, JavaScript rose: four hues that read as distinct from
each other, from Python's orange, and from error red/pass green, in
either theme.

### HTML

Renders live, the way a Text cell renders Markdown — but raw HTML
cannot share Text's `innerHTML`-into-the-page approach safely, because
dewmini already has an import path (Settings → Load a shared cell/
notebook) that can bring in a `<script>` a reader didn't write
themselves. It renders inside a sandboxed `<iframe srcdoc="…">
sandbox="allow-scripts">` instead — no `allow-same-origin`, so anything
inside it, script included, cannot reach the rest of the page, this
cell's own `localStorage`, or any other cell, regardless of who wrote
it. The iframe gets a generous default height and `resize: vertical` so
a reader can drag it taller for content that needs it, rather than the
page reaching into a cross-origin frame to measure its content height
(which the same sandboxing that keeps it safe also makes impossible
without an explicit `postMessage` handshake — not worth the complexity
for a first version).

Chrome: pill, Duplicate/Delete, collapse, Edit/View, quiet until
touched — the same full Text-shaped set §4's table already gives HTML,
now that "once it exists" (§4's own hedge on HTML's collapse) is true.
No run line: rendering isn't running against a session, and a cell that
cannot go stale should not have a line implying it could.

### CSS

The obvious pairing — CSS styling an HTML cell right above it — was
considered and set aside: it would make a CSS cell's behaviour depend on
cell order and type in a way nothing else in dewmini's model does (a
Python cell reads the *shared namespace*, never "whatever cell happens
to sit above it"). Instead a CSS cell renders its own small, fixed
preview — a heading, a paragraph, a button, a list, a link — inside the
same kind of sandboxed iframe HTML uses, with the reader's CSS in a
`<style>` tag ahead of that markup. Self-contained, live-updated as the
reader types (debounced, the same rhythm autosave already uses), and
exactly as functional as a standalone "try CSS" tool needs to be.

Chrome: same as HTML — pill, Duplicate/Delete, collapse, Edit/View,
quiet until touched, no run line. A CSS cell is read (the rule) and seen
(the preview), never run against anything shared.

### SQL

The one type that genuinely runs, against a namespace as real as
Python's own — `RUNS_AGAINST_SESSION` gains `sql` alongside `python`,
and every piece of machinery that already exists for that reason
(`runCellBatch()`, Run above/below, Restart & run all, the run-line's
order/duration/staleness) applies to a SQL cell exactly as built,
unmodified. The database itself is *sql.js* (SQLite compiled to
WebAssembly) — the same category of choice Pyodide already made for
Python, a real interpreter running entirely in the reader's own tab, no
server. One shared, in-memory database for the whole notebook, created
lazily on the first SQL cell's first run; `CREATE TABLE` in one cell and
`SELECT` from it in a later one work exactly the way defining a variable
in one Python cell and reading it in a later one already does. Restart
Python (renamed, in spirit, to cover this) discards and recreates the
database the same way it discards and recreates the Pyodide interpreter.

Output: a `SELECT`'s rows render as an HTML table, reusing the exact
markup and CSS `tutorial_tools.py`'s own `show_table()` already produces
for a Python DataFrame, so a SQL result and a pandas result look like
the same kind of thing on the page, because they are. A statement with
no rows to return (`CREATE`/`INSERT`/`UPDATE`/`DELETE`) reports what it
did in a short line — "3 rows inserted," "Table created" — the SQL
equivalent of a Python statement that prints nothing.

Chrome: the Python-shaped set — pill, Duplicate/Delete, collapse, run
line. No Edit/View toggle, no quiet-until-touched: like Python, a SQL
cell is meant to be worked on, not read past.

### JavaScript

Also a real, shared session, on the same reasoning as SQL — closer in
kind to Python than to HTML/CSS's read-only rendering, so
`RUNS_AGAINST_SESSION` gains `javascript` too. The session lives in one
persistent sandboxed iframe for the whole notebook (`sandbox=
"allow-scripts"`, no `allow-same-origin`, the same isolation HTML's
preview uses), created lazily on first run and torn down and recreated
on Restart Python exactly like the Pyodide interpreter is. Each cell's
code is posted into that iframe and evaluated there, so a `var`/
function/`const` declared in one cell is still there for a later one to
read, the same persistent-namespace feel Python's own session already
has. `console.log`, its arguments serialised the way `tutorial_tools.py`
already serialises a Python `print()`'s, and a thrown error, both
`postMessage` back to the parent as this cell's output — the same
"emit as you go" shape `run_cell()`'s own `emit` callback already uses
for Python, just crossing a `postMessage` boundary instead of a Pyodide
one.

Chrome: the Python-shaped set, same as SQL — pill, Duplicate/Delete,
collapse, run line, no Edit/View, no quiet-until-touched.

### Build order, and what stays out of scope for now

HTML first — no new runtime dependency, and the sandboxed-iframe
pattern CSS and JavaScript both reuse gets proven once, on the simplest
case. CSS next, since it shares that same pattern almost entirely. SQL
and JavaScript both need a genuinely new execution engine (*sql.js*; the
persistent sandboxed session) and come after, in whichever order the
work actually lands.

Not attempted here, on purpose: none of the four get a drag-and-drop
keyboard equivalent (§6 already flags this as owed to every cell type,
not something new these four add to); SQL and JavaScript get no
autocomplete or hover-doc the way Python's Jedi-backed tooling does —
real, but a second project once the execution model itself is proven;
and tutorial/practice pages get none of this in this pass — §7's own
"dewmini only" scoping decisions for the pill/run-line/collapse/
Duplicate work apply here for the same reason: these are genuinely new
engines, not a port of something dewmini already proved, and the
tutorial runtime has never needed anything but Python.
