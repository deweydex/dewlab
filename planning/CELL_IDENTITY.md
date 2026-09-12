# Cell identity and the execution counter: a design note

**Built in `compose/dewmini.js` (7.110).** This document describes the
settled shape of a notebook cell: what it is, whether it has run, and
whether its output still matches its code. `compose/dewmini.js` is the
source of truth for what actually ships, not the two static mockups
below — they capture the original proposal and have not been redrawn to
match; §4 and §7 note the small differences 7.110 settled on while
building it:

- [`mockups/cell-identity.html`](./mockups/cell-identity.html) — a
  working mockup of every cell type in this design (Python, SQL, HTML,
  CSS, Text), including the live run-status timer.
- [`mockups/cell-identity-explained.html`](./mockups/cell-identity-explained.html)
  — the same design, explained in plain language for a reader new to the
  project. This document assumes more context and is written for
  maintainers; that one is written to stand alone.

Four related, smaller features from the same proposal shipped first
(`DECISIONS_LOG.md` 7.105–7.108): the "edited since last run" marker,
Run above/below, Restart & run all, and maths rendering in text cells —
per 7.109, three of those four (everything but maths) also run on
tutorial and practice pages' `.dl-cell`. This document's own subject —
execution counters, the numbered identity pill — came later (7.110),
because unlike the other four it touched the header every cell already
had rather than adding a small piece to it, so it was worth designing
properly before building it. 7.113 carried the pill and the merged
run-line to tutorial and practice pages too, and 7.114 followed with
collapse and Duplicate — see §7 for exactly what did and didn't come
along with them, and what Duplicate ended up meaning on a page whose
cells aren't all the reader's own.

---

## 1. Why number a cell at all

A dewmini notebook shares one Python namespace across every cell, top to
bottom, but a reader is free to run them in any order, any number of
times, or not at all. That freedom is the whole point of a notebook —
but it means a cell's position on the page stops being a reliable guide
to what state the notebook is actually in. Two problems follow:

- **Which cell produced this output?** If a reader has run cell 3, then
  cell 1, then edited cell 2 without re-running it, the order things
  actually happened in is no longer the order they appear on the page.
  A plain running count — "this was the 1st cell to run, this the 2nd" —
  answers that directly, and is exactly the piece of information a
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

**The whole pill is the drag target, not just the handle.** A small,
precise handle would be a worse touch target than the wide, inviting pill
around it. Since the pill already shows exactly what would be picked up
("Cell 3, Python"), there is no reason to make the target smaller than
the thing labelling it.

**The pill's tooltip says only what the pill can't say for itself: that
it drags.** Its own number and type are already visible as plain text
once, on every cell, and which cell types run against the shared session
is explained once, in the rules table further down, rather than repeated
on every hover.

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

Cell types that never run against the session — Text, and Web (§8's
merged HTML+CSS type) — have nothing to report here and show no run line
at all (`RUNS_AGAINST_SESSION = {python, sql, javascript}`). A cell that
cannot be stale should not have a line implying it could.

## 4. What differs by cell type, and why

Not every cell needs every affordance, and giving one to a cell that
can't use it is worse than simply leaving it off — it invites a reader
to wonder what it does. Four things vary by type:

| | Python | SQL | Web | JavaScript | Text |
|---|---|---|---|---|---|
| Numbered, coloured pill | yes | yes | yes | yes | yes |
| Drag target | yes | yes | yes | yes | yes |
| Header-end: Duplicate, Delete | yes | yes | yes | yes | yes |
| Run line (order/duration/stale) | yes | yes | — | yes | — |
| Collapse triangle | yes | yes | yes | yes | yes |
| Edit / View toggle | — | — | — | — | yes |
| Render button | — | — | yes | — | — |
| Quiet until touched | — | — | yes | — | yes |

Five columns, not six: HTML and CSS shipped as separate types first
(7.116, 7.117) and were later merged into one, Web (7.120) — read §8's
own "Two types become one" note for why.

**Header-end** is Duplicate and Delete, on every cell, plus an Edit
toggle for Text only, and a Render button for Web only. Duplicate inserts
a copy of the cell right after itself, same type and code, no run
history: a starting point for a variation, not a claim that the copy
already ran.

**Every cell type gets Collapse, code-bearing or not.** A read-not-run
type doesn't strictly need it — a rendered form already exists to shrink
to — but a Text cell caught in *edit* mode has no such fallback, and
"shrink this out of the way without deleting it" is exactly as true for a
long note as for a long function.

**Edit/View belongs to Text alone.** HTML had it too, when HTML was
still its own type: a click revealing the source behind a rendered view.
Web, the type that replaced it, has no toggle at all, because it has
nothing to toggle *between* — both its editors (HTML, CSS) are always
visible and always editable at once, never swapped out for a rendered
view the way Text's editor is. **Quiet until touched belongs to both
Text and Web**: both render by default and hide their chrome until a
reader deliberately touches the cell, rather than sitting open and
code-shaped among cells that are. Controls are not removed while quiet,
only made invisible — `opacity: 0; pointer-events: none`, not `display:
none` — so a keyboard user tabbing through the page can still reach and
open them; only a mouse user actually needs to hover first.

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

The collapse control is a single `›` glyph, rotated 90° between expanded
and collapsed states, rather than two swapped filled triangles as the
mockups show. With the footer's own ▶ Run button sitting only a line or
two below it, two different filled triangles in the same corner of the
cell would read as confusingly similar — one glyph throughout, its
orientation carrying the state rather than its shape.

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

**dewmini, Python and SQL cells (7.110): done.** The numbered, coloured
pill; the merged run-line, including the live "Running…"/"Running next"
states and the run-order counter (`runSequenceCounter`, reset on any
namespace reset, not only a full restart); the collapse triangle, on
every cell type per §4; and the header-end group, Duplicate included.
`ranContent`/staleness (7.105), `runCellBatch()`/`runAbove()`/
`runBelow()` (7.106), and `restartPython()` (7.108) turned out to be
exactly the groundwork this needed, unchanged.

**SQL, HTML, CSS, JavaScript: designed in §8, built from there outward,
in dewmini only, one type at a time. All four shipped — HTML (7.116),
CSS (7.117), SQL (7.118), JavaScript (7.119) — and HTML and CSS were
then merged into one type, Web (7.120).** §8 is where the design turns
into an actual execution model per type, since §4's table only ever
answered *what chrome a cell gets*, never *what running one does*.
`--dl-type-python`/`--dl-type-text` were the only colour tokens until §8
added four more; Web kept HTML's own token rather than needing a fifth,
which is why §4's own table is five columns, not six.

**Tutorial and practice pages: the pill and the run line are ported too
(7.113).** 7.109 ported the run-line-adjacent pieces (staleness, run
above/below, restart & run all) onto `build.py`'s
`render_cell()`/`assets/tutorial-runtime.js`, keeping dewmini's and the
tutorial runtime's own engines and DOM separate rather than unifying
them. 7.113 carried the pill (`Cell N`, coloured "Python" type) and the
merged run-line (order, duration, staleness, live "Running…"/"Running
next") over the same way, replacing the plain `.dl-cell-id` text and the
separate stats/stale-badge pair 7.109 had used. The pill's number is
different in kind from dewmini's, though: a tutorial page's cells are
never reordered, so `build.py` gives each one its static, build-time
position rather than live-recomputing it the way dewmini must for a
draggable list — there is no drag handle here, because there is nothing
to drag. The colour token is always `--dl-type-python`, since every
authored cell on a tutorial page is Python; `--dl-type-text` and the
rest stay unused until a real second authored type exists.

**Tutorial and practice pages: collapse and Duplicate too (7.114).** The
collapse triangle applies to every cell that has editable content — an
authored cell's code, and both a custom Python cell's code and a custom
text cell's note-or-rendered-view — the same "every type gets it"
reasoning §4 already settles for dewmini. Collapsing hides only
`.dl-cell-content`; the output and the bar beneath it stay visible, same
as dewmini.

Duplicate means something different here than in dewmini, because an
authored cell isn't a reader's own the way a dewmini cell is — it's the
tutorial's own fixed content. Duplicate on an authored cell inserts a
copy of its code as a new *custom* cell immediately after it — the
reader's own copy to experiment with, the tutorial's own left untouched.
This reuses machinery that already existed for an unrelated reason:
`initCustomCellsSection()` already seeds a "+Code / +Text" insertion
point after every real cell (for "Try something of your own" placed
anywhere on the page), so Duplicate is just one more way of using that
same seam, not a new insertion mechanism. Custom cells got their own
Duplicate too, inserting the copy right after the original the same way.

**Quiet until touched, built for the first time anywhere (7.115).** A
rendered Text cell's chrome (dewmini's
`.dm-cell-head`/`.dm-cell-collapse-col`; a custom text cell's own
`.dl-cell-head`/`.dl-cell-collapse-col`) stays `opacity: 0;
pointer-events: none` until a reader hovers or focuses the cell, one CSS
rule with no JavaScript on either side — a reader focusing the textarea
to edit already puts the cell in `:focus-within`, which is exactly when
the chrome should reappear. Authored cells and custom Python cells keep
their chrome on always; only Text is quiet.

## 8. SQL, HTML, CSS, JavaScript: what running one actually does

§4's table answers what chrome each type gets; this section answers what
happens when a reader presses Run, or when a rendered cell first appears.
dewmini only, for now: building four cell types into two engines at once
would be the same mistake 7.109 explicitly declined to make for Python.

**Colour tokens.** Four new hues, alongside `--dl-type-python`/
`--dl-type-text`, each defined for light and dark the same way
`--dl-error-fg`/`--dl-pass-fg` already are rather than as a single fixed
hex — a colour picked for legibility against the light cell background
is not automatically legible against the dark one. SQL teal, HTML
violet, CSS blue, JavaScript rose: four hues that read as distinct from
each other, from Python's orange, and from error red/pass green, in
either theme.

### Web (HTML + CSS)

A web cell has two editors, HTML and CSS, both always visible and both
always editable — never one swapped out for the other the way a Text
cell's rendered view swaps out for its editor. Rendering is the header's
own explicit Render button rather than something either editor triggers
on its own: two editors both auto-rendering on blur would fire the same
preview update twice for one edit, and would show a reader tabbing from
one editor to the other a half-finished render flash by in between.
Render combines both halves into one sandboxed `<iframe srcdoc="…"
sandbox="allow-scripts">` — no `allow-same-origin`, so anything inside
it, script included, cannot reach the rest of the page, this cell's own
`localStorage`, or any other cell, regardless of who wrote it (dewmini
already has an import path, Settings → Load a shared cell/notebook, that
can bring in a `<script>` a reader didn't write themselves). The iframe
gets a generous default height and `resize: vertical`.

One cell holding both halves gives "which HTML is this CSS for" an
unambiguous answer — its own HTML — where two separate cells never
could. An empty HTML half still falls back to `CSS_PREVIEW_MARKUP` (a
fixed little "page" the old standalone CSS cell always rendered
against), so a reader who has only written a rule still has something
real to see it styling.

Chrome: pill, Duplicate/Delete, Render, collapse, quiet until touched —
close to the full Text-shaped set §4's table gives HTML/CSS, minus the
Edit/View toggle: with nothing ever swapped out for anything else, there
is nothing for a toggle to switch between. No run line: rendering isn't
running against a session, and a cell that cannot go stale should not
have a line implying it could.

**Two types become one (DECISIONS_LOG.md 7.120).** HTML and CSS shipped
as separate types first (7.116, 7.117), then merged once both existed to
show that a CSS cell that could never style anything but a fixed sample
page, and an HTML cell with no CSS of its own at all, were each half of
one idea rather than two complete ones. A notebook saved under the old
two-type model still loads: each standalone `html`/`css` cell becomes its
own new web cell independently (an old HTML cell's markup becomes the
new cell's HTML half with an empty CSS half, and symmetrically for CSS)
— never merged into one cell, since guessing which HTML an old CSS cell
was written to style is exactly the ambiguity the merged design no
longer needs to guess at.

### SQL

The one type that genuinely runs, against a namespace as real as
Python's own — `RUNS_AGAINST_SESSION` gains `sql` alongside `python`,
and every piece of machinery that already exists for that reason
(`runCellBatch()`, Run above/below, Restart & run all, the run-line's
order/duration/staleness) applies to a SQL cell exactly as built,
unmodified.

**Built on Python's own `sqlite3`, not a second engine (7.118).** dewmini
already runs a real Python, and Python already ships `sqlite3`,
unvendored as an ordinary loadable Pyodide package rather than bundled
into core (`compose/dewmini.js`'s `DM_PACKAGES` already carried it, from
`run_query()`'s own earlier work, 7.78). One engine, with the shared `db`
global sqlite3 already gives it, means a SQL cell's `CREATE TABLE` is a
table `pd.read_sql("select * from t", db)` can already see from an
ordinary Python cell, with no plumbing of its own — friendlier for a
student who has never opened a terminal, and interoperable with the
pandas/numpy tooling every other cell already uses. Two engines booting
in the same tab would have meant two data models that don't talk to each
other — a SQL cell's own table invisible to a pandas DataFrame, and vice
versa, unless something bridged them by hand.

A SQL cell's own code is never handed to Pyodide as-is — a cell's raw
SQL is not Python. `executeCell()`'s `buildSqlCellCode()` wraps it into
one generated line, `tutorial_tools._run_sql_cell(db, <the SQL as a
JSON-encoded string literal>)`, and that line is what actually runs
through the same `engine.runCell()` a Python cell's own code goes
through — no second code path through the engine, only a different
string handed to the one that already exists. `db` is a fresh, in-memory
`sqlite3.connect(":memory:")` connection, created once at boot and again
on every reset — `CREATE TABLE` in one cell and `SELECT` from it in a
later one work exactly the way defining a variable in one Python cell
and reading it in a later one already does, and Restart Python discards
and recreates `db` the same way it discards and recreates the Pyodide
interpreter itself.

`tutorial_tools._run_sql_cell(conn, script)` — internal, not in
`__all__`, since a reader is never meant to call it by name; `run_query()`
stays the public, single-statement version of the same idea, for a
tutorial page. It splits `script` on a bare `;` (a plain split, not a
real SQL parser — good enough for what a teaching notebook's cell needs,
not for a semicolon buried inside a string literal) and runs every
statement but the last directly, so a cell reads as an ordinary SQL
script — `CREATE TABLE` here, `INSERT` there, `SELECT` at the end — the
way `run_query()`'s single-statement shape never could. Only the last
statement's own result renders: a `SELECT`'s rows as an HTML table,
reusing the exact markup and CSS `tutorial_tools.py`'s own
`_table_html()` already produces for a Python DataFrame, so a SQL result
and a pandas result look like the same kind of thing on the page,
because they are; anything else (`CREATE`/`INSERT`/`UPDATE`/`DELETE`)
reports how many rows it touched in a short line — "3 rows affected" —
the SQL equivalent of a Python statement that prints nothing. Every
statement commits at the end, the same friendlier default `run_query()`
already chose. The generated wrapper line assigns its own return value
(`_ = tutorial_tools._run_sql_cell(...)`) rather than leaving it as the
cell's last expression, on purpose: `_run_sql_cell()` already renders its
result directly, and letting it also be the auto-displayed last value
would render the same table twice.

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
on Restart Python exactly like the Pyodide interpreter is. `console.log`,
its arguments serialised the way `tutorial_tools.py` already serialises a
Python `print()`'s, and a thrown error, both `postMessage` back to the
parent as this cell's output — the same "emit as you go" shape
`run_cell()`'s own `emit` callback already uses for Python, just crossing
a `postMessage` boundary instead of a Pyodide one.

**Built on indirect `eval`, not a `<script>` tag, and only `var`/
`function` persist across cells — not `let`/`const` (7.119).** Each
cell's code runs through indirect eval — `(0, eval)(code)`, called from
the iframe's own top level. A `<script>` tag's own top-level `let`/
`const` declarations join the realm's *one, permanent* global lexical
environment, so re-running an edited cell a second time — an entirely
ordinary thing to do in a notebook — would throw `SyntaxError: Identifier
'x' has already been declared` the moment it tried to redeclare its own
`let`. Per spec, indirect eval's top-level `let`/`const` bindings live in
a fresh scope private to *that one call*, not the realm's shared global
lexical environment, so a cell can always be re-run safely. The cost is
that those bindings are gone once the call returns — a later cell can no
longer read a `let`/`const` from an earlier one, only `var` and
`function` declarations, which indirect eval still attaches to the real
global object exactly like a `<script>` tag would. A real fix (parsing
each cell to hoist its own top-level `let`/`const` onto the shared
session by hand) would need an actual JS parser vendored in for it — out
of scope here, the same way SQL's own multi-statement split is a plain
string split rather than a real SQL parser. Documented plainly in the
cell's own help text (`compose/dewmini.html`) rather than left for a
reader to discover the hard way.

One further consequence of indirect eval over a `<script>` tag: a
synchronous error is caught directly around the `eval()` call itself (an
ordinary `try`/`catch`, no `window.onerror` needed) — this is what
actually answers whether the run's own `ok` was true or false. An
*unhandled promise rejection* (async work a cell scheduled but didn't
itself catch) still needs
`window.addEventListener("unhandledrejection", …)`, since it can only
fire after the triggering `eval()` call has already returned; it is
reported into the cell's output the same way, but arrives too late to
change the `ok` that run already reported. Top-level `await` is not
supported for the same reason: wrapping a cell's code in an `async`
function to allow it would swallow its own top-level `var`/`function`
declarations into that function's scope instead of the global one,
losing the one form of cross-cell persistence this design does have.

Chrome: the Python-shaped set, same as SQL — pill, Duplicate/Delete,
collapse, run line, no Edit/View, no quiet-until-touched.

### Build order, and what stays out of scope for now

HTML first — no new runtime dependency, and the sandboxed-iframe pattern
CSS and JavaScript both reuse gets proven once, on the simplest case.
**Built (7.116).** One real, deliberate difference from Text despite the
shared shape: a click on Text's rendered view opens its editor; the same
gesture cannot work for HTML, because a click inside a cross-origin
sandboxed iframe never bubbles out to a listener in this document. The
header's own Edit/View toggle — already there, already revealed the same
way by quiet-until-touched — is the one way in.

CSS next, since it shares that same iframe pattern almost entirely.
**Built (7.117).** Styling the HTML cell above it — the obvious pairing
— was set aside: it would make a CSS cell's behaviour depend on cell
order and type, which nothing else here does. Its preview is
`CSS_PREVIEW_MARKUP`, a fixed little "page," with the reader's rule in a
`<style>` tag ahead of it.

SQL next. **Built (7.118)**, and — once sql.js (SQLite compiled to
WebAssembly, the obvious first guess for "SQL needs a database") was set
aside for Python's own `sqlite3` above — needing no genuinely new
execution engine after all, only a generated-code path through the one
Pyodide already booted for everything else.

JavaScript last. **Built (7.119)** — the one type that did need a
genuinely new engine, a persistent sandboxed session with no Pyodide
underneath it at all. The sandboxed-iframe pattern HTML/CSS already
proved carried over directly; what was new was everything about running
code inside it safely across repeated re-runs, above.

Fifth, after all four existed: HTML and CSS merged into one type, Web —
not part of the build order above, but the result of the "Two types
become one" note once both types existed to show it was the right call.

Not attempted here, on purpose: none of the four get a drag-and-drop
keyboard equivalent (§6 already flags this as owed to every cell type,
not something new these four add); SQL and JavaScript get no
autocomplete or hover-doc the way Python's Jedi-backed tooling does —
real, but a second project once the execution model itself is proven (a
SQL cell's CodeMirror editor uses `@codemirror/lang-sql` for syntax
highlighting only, the same "structure, not semantics" a Python cell's
editor would have with Jedi turned off); and tutorial/practice pages get
none of this in this pass — §7's own "dewmini only" scoping decisions
apply here for the same reason: these are genuinely new engines, not a
port of something dewmini already proved, and the tutorial runtime has
never needed anything but Python.

## 9. Closing the last gaps with tutorial pages (7.136)

A single Python cell's own chrome and behaviour should feel the same
wherever a student meets it — not the whole platform (dewmini's tabs,
its filesystem, its other cell types stay dewmini-only), just one cell.
Comparing a Python cell in a tutorial against one in dewmini turned up
four concrete mismatches, plus two further requests alongside them; all
six shipped together.

**Run moved from after the output to between the code and the output.**
§5 above states the rule — Run sits where a reader's hand already is,
right under what they just wrote. `.dl-cell-bar` had sat after
`.dl-output`, not before it, on tutorial pages; `render_cell()` now
emits `.dl-cell-head` (identity: pill, optional name, Duplicate),
`.dl-cell-body-row` (collapse triangle, editor), `.dl-cell-footbar` (Run,
Reset, the run menu, the run line), then `.dl-output` — the same order
dewmini's own `createCellElement()` already used. `assets/tutorial-
runtime.js`'s `createCustomCellElement()` (a reader's own cells, built
entirely client-side, never through `render_cell()`) got the same three
rows by hand, so a reader's own cell and the tutorial's stay one shape.

**A same-shaped button did two different things.** The tutorial's single
Reset put a cell's *code* back to its starter and threw the rest away;
dewmini's own footbar button only clears a cell's *output*, no code
touched. Both were reasonable choices on their own — a tutorial's cell
has starter code worth returning to, a dewmini cell doesn't — but
nothing about how the two buttons *looked* said so, and the more
dangerous of the two sat in the position a reader's muscle memory would
already trust from the other page. A tutorial cell now carries both:
`.dl-btn-reset` clears output only, sharing dewmini's own counterclockwise
↺ (`&#8634;`) icon and meaning; `.dl-btn-clear` is the one that still
touches code, kept behind a confirmation dialog, with its own clockwise
↻ (`&#8635;`) icon and resting red-ish border (`tutorial-style.css`).

**Icon-only on one page, text-only on the other.** A tutorial page's
buttons were plain words (`Run`, `Reset`, `duplicate`); dewmini's were
bare glyphs in small square buttons, meaning purely by tooltip. Every
cell-chrome button on both pages now carries both, in a nested
`.dl-btn-icon`/`.dl-btn-label` pair (`icon_button()` in `build.py`,
`iconButtonHtml()` in `tutorial-runtime.js`, `iconButton()` in
`compose/dewmini.js`) — the same two class names regardless of which
page built the button, so one CSS rule, `tutorial-style.css`'s
`[data-button-labels]`, shows or hides either span on both. A Settings
row, "Cell buttons" (`data-texture="buttons"`, alongside Theme/Font/
Contrast in the existing Texture panel — a display preference, not an
execution one, so it stays available even on a page with no Python
cells at all), offers icons/text/both and rides the exact same
`"dewlab:texture"` localStorage key and generic `initTexture()` machinery
every other Texture row already uses on both pages. The small,
fixed-size badge buttons (hint and report toggles, the collapse
triangle) were deliberately left out of this: no dewmini counterpart to
match, and no room in their compact circular shape for a label.
`setBtnLabel()`/`getBtnLabel()` (one small helper pair, defined
separately in each file, the project's usual "port in shape"
convention) read or write a button's `.dl-btn-label` span directly,
since `.textContent` on the button itself would erase its icon along
with whatever text was there.

**dewmini's own traceback showed its internal cell id.** `run_cell()`
(`tutorial_tools.py`) gained an optional `label`, threaded down through
`run_cell_report()`/`_begin()`/`_CellContext`/`cell_filename()` and, on
the JavaScript side, `assets/pyodide-engine.js`'s `runCell()` and
`assets/pyodide-worker.js`'s `"run-cell"` message. `label`, when given,
replaces the id entirely — in `linecache`'s own key as well as what a
reader reads in a traceback's file line, since `_is_user_frame`'s own
`"<cell "` prefix check only cares about the prefix, never what follows
it. Unlike an id, a label isn't guaranteed unique — two dewmini cells can
share a name — so two same-named cells do share one `linecache` entry;
harmless given how this module always formats a cell's traceback
immediately, never from a stored exception read back later. dewmini's
`executeCell()` passes `cell.name || \`Cell ${n}\``; a tutorial page
passes its author-given `name:` when a cell has one, and nothing (the
id, as before) when it doesn't.

**The pill's position, and a name beside it.** The pill's position was
already the same on both pages — both put it at the head of the cell.
What was new is the name. `name:` is a fourth header line on an authored
cell (`HEADER_RE`, `Cell.name`, `build.py`), shown in `.dl-cell-name`
next to the pill; dewmini's own cells get an *editable* one instead, a
plain `<input>` (`.dm-cell-name`/`.dl-cell-name`, styled to read as a
label rather than a form field), since every dewmini cell is already the
reader's own. Neither replaces the pill's number — the number still says
*where* a cell sits; the name is only ever a second, optional way to
point at it in conversation. A duplicate deliberately does not carry a
dewmini cell's name over to its copy, the same reasoning already covers
not carrying over run history: a name is a claim of identity, and a
fresh cell hasn't earned it yet.

Deliberately left for later: an editable name for a *tutorial* page's
own reader-added custom cells, which stayed at their existing plain
"Your cell"/"Your note" pill text rather than gaining the same input
dewmini's cells did.

*Cost to change: `render_cell()` (build.py) rewritten to three rows;
`createCustomCellElement()` (tutorial-runtime.js) to match by hand; one
new Settings row, shared verbatim by both pages' existing Texture
machinery; a `label` parameter through five functions across
`tutorial_tools.py`, `pyodide-engine.js`, `pyodide-worker.js`; a
`name`/`nameEl` field on both cell models. `tests/test_build.py`'s
`test_the_footbar_sits_between_the_editor_and_output` (renamed from an
assertion the old layout made permanently false) and five e2e tests'
button-label selectors, updated to read `.dl-btn-label` where they used
to read a button's own `.textContent`. `assets/vendor/standalone.bundle.js`
rebuilt for the `tutorial-runtime.js` change.*
