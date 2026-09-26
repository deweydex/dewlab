# `assets/tutorial-runtime.js`, explained

This is the biggest single file in dewlab's frontend, and it's the one
loaded on every tutorial page. It's what turns build.py's static HTML
into an actually-working page: the settings panel, the reference, the
series navigation, saving a student's work, version switching, and
booting and running Python. If you've read
[`docs/dewmini-js-explained.md`](dewmini-js-explained.md) or
[`docs/pyodide-engine-explained.md`](pyodide-engine-explained.md), a
good chunk of this file will look familiar — the shared
`pyodide-engine.js` (dewmini's own Python engine) was originally ported
from this file's own Pyodide-handling code, and both solve the same
"worker vs. main thread" problem the same way.

---

## The big idea: one file, several independent jobs

Unlike dewmini (which splits cell management, the Python engine, and the
filesystem into three separate files), this file does all of its jobs in
one place. That's a deliberate difference, not an oversight — a tutorial
page is simpler than dewmini in scope (no file manager, no SQL, no
uploads), so splitting it further would add file-hopping without buying
much. Instead, this file is organized into clearly labeled sections (look
for the `/* ---- section name ---- */` comments), and each section is
close to self-contained:

- **Settings, reference, and series navigation** — three panels that
  open and close, coordinated so only one is ever open at once.
- **Texture** — the reader's theme/font/size preferences, shared across
  every dewlab page via `localStorage`.
- **Cells** — building each cell's editor and wiring up its buttons.
- **Custom cells** — a reader's own cells, created at runtime rather than
  authored in the tutorial's Markdown, kept deliberately separate from
  everything above.
- **Export** — printing (or saving as PDF) and saving the page's cells as
  a Jupyter notebook, alongside the "Download to keep" section
  `build.py` writes.
- **Pyodide** — booting Python and running a cell's code, with the same
  worker/main-thread split `pyodide-engine.js` uses.
- **Illustrative code and maths** — syntax highlighting for read-only code
  blocks, and KaTeX for rendered maths.
- **Saved work** — autosaving a student's cells, notes and highlights, and
  restoring them.
- **Highlights and margin notes** — marking a passage of prose, in one of
  four colours, with an optional note attached; a live list of them in
  the Notes panel (`refreshHighlightsList()`), and a cross-page summary
  at `all-notes.html` built from the same saved records by a separate
  file, `assets/my-notes.js`.
- **Progress** — the "3 of 8 cells run" summary and the contents-page
  badges.
- **Versions** — for a tutorial with more than one release: which one a
  reader is on, and moving between them without losing saved answers.
- **Start** — the one block of top-level code that actually calls
  everything above, in order, when the page loads.

---

## Reading order

Honestly, the section labels already in the file *are* the reading
order — read the module docstring at the very top first, then go section
by section, top to bottom. A few sections are worth calling out
specifically:

1. **Config** (`PYODIDE_VERSION`, `DEFAULT_PACKAGES`, `TEXTURE_DEFAULTS`,
   and so on) — the constants nearly every other section depends on.
2. **Pyodide** — the largest section, and the one with the most going on.
   It has the exact same worker/main-thread split as
   `pyodide-engine.js`; if a function here (`bootWorker`, `docForMT`,
   `workerRequest`, etc.) moves too fast, that file's own explanation
   goes into more detail on the identical pattern.
3. **Start**, at the very bottom — this is genuinely where execution
   begins. Everything above it is function definitions; nothing happens
   on the page until this section runs, top to bottom, in the order
   written.

---

## Custom cells: a second, deliberately separate cell system

A reader can add their own Python cell to a page — not one the tutorial's
author wrote, one the
reader typed themselves, for trying something out or writing a practice
problem of their own. The whole "custom cells" section (roughly
`CUSTOM_CELLS_PREFIX` through `initCustomCellsSection()`) exists to do
that, and its central design choice is worth stating plainly: **a custom
cell is never added to `cells`, and never touches `saveNow()`,
`restoreSaved()`, or the progress summary.** It gets its own array
(`customCells`), its own `localStorage` key
(`dewlab:custom-cells:<id>`), and its own save/restore
functions (`loadCustomCells()`/`saveCustomCells()`/
`scheduleCustomSave()`) that mirror the real ones in shape but never call
them or get called by them.

That separation isn't laziness — it's the simplest way to guarantee two
things this feature requires: a custom cell can't collide
with a real cell's id (its id always starts with `custom-`, which no
tutorial author would ever write), and a custom cell survives a tutorial
version change completely untouched (it was never part of the versioned
record to begin with, so there's nothing for a version-mismatch check to
even notice). The one thing a *python*-type custom cell shares with a
real cell is the shared `runCell()` function: its cell object has the
exact same shape a real cell's does (`{id, editor, outputEl, runBtn,
getCode, element}`), so `runCell()` runs one without any special-casing
— `mountCustomCellAfter()`'s own comment points this out. A *text*-type
custom cell has no run step at all, so its object is smaller
(`{id, type, element, getCode, focus}`) and never reaches `runCell()`.

The whole feature only appears on a page that already has real cells
(`cells.length > 0`) — see `initCustomCellsSection()`'s own comment for
why: a prose-only tutorial never boots Pyodide at all, and offering "add
your own cell" there would force it to, which is exactly the cost that
page is supposed to avoid.

One easy-to-miss detail: a real cell's Run button always starts
`disabled` in the HTML `build.py` generates, because at the moment that
markup is written nothing yet knows whether Python will boot quickly or
slowly — `setRunnable(true, "Run")` is what enables it later, once boot
actually finishes. A custom cell has no such luxury of a fixed starting
point: a reader might add one *before* boot finishes (one restored from
storage while the page is still loading) or long *after* it already has
(adding one ten minutes into a session). That's what the small
`pyodideReady` flag near the top of the Pyodide section is for —
`createCustomCellElement()` reads it to decide whether a brand-new
cell's Run button should start enabled or not, rather than assuming.

**Cell types, and a seam after every cell on the page.** A custom cell
can be `"python"` or `"sql"` (an editor, an output area, Run — `"sql"`
only ever arrives by duplicating an authored `sql exec` cell, since there
is no "+SQL" button of its own yet) or `"text"` (a
textarea that turns into rendered notes — a small, hand-written markdown,
`renderDocMarkdown()`, ported from `compose/dewmini.js`'s own text cells
rather than reinvented). Blurring the textarea renders it, and clicking
the rendered view edits it again — both still work, but neither is the
*only* way in: a text cell's bar also carries an explicit "view"/"edit"
button, because a mouse gesture (click away, click back) has no
equivalent affordance on a touch device with no hover to reveal that the
rendered text is clickable at all. One easy-to-miss detail in
`mountCustomCellAfter()`'s wiring: the button listens on `mousedown`
with `preventDefault()`, not `click` — clicking it while the textarea is
still focused would otherwise blur the textarea *first* (which
auto-renders), so by the time the button's own click handler ran it
would see the already-rendered state and toggle straight back to
editing instead of landing on rendered. Every dewlab surface with a text
cell (this file, `compose/dewmini.js`) uses the
same fix, for the same reason.

And a reader isn't limited to one button at the bottom of the page:
`initCustomCellsSection()` lays a
divider (`createCustomInsertDivider()`, `.dl-insert` in
`tutorial-style.css`) after *every* real cell, wherever it sits in the
tutorial's own prose, as well as inside the trailing "Try something of
your own" section — so a reader can try something immediately below
whatever prompted the idea, not scroll away from it first.

Each custom cell carries an `anchor`: the id of the real cell it was
added after, or the sentinel `TRAILING_ANCHOR` for one added in the
general section. Cells sharing an anchor stack in save order, each with
its own trailing divider so that seam stays usable for another insert.
`mountCustomCellAfter()` is the one function that actually places a cell
in the DOM — `insertAdjacentElement("afterend", ...)` twice, divider then
cell, so whichever divider was clicked stays exactly where it was and
the new cell lands right after it, with a fresh divider of its own
appended beyond that. Order is never tracked in a separate array that
could drift out of sync with the page — `saveCustomCells()` reads it
straight back out of the DOM (`document.querySelectorAll(".dl-cell-custom")`,
in document order), and `lastDividerFor(anchor)` (used by
`addCustomCell()` and `importCustomCell()`, which always append rather
than insert at a specific clicked seam) is the last `.dl-insert` element
carrying that anchor, also read straight from the DOM.

If a saved cell's anchor no longer matches any real cell — the tutorial
was updated and that particular cell is gone — `initCustomCellsSection()`
falls back to `TRAILING_ANCHOR` rather than dropping the custom cell.
This fallback is the concrete mechanics behind a custom cell surviving a
version change untouched: the cell and its code are never at
risk, only its position can degrade to the general section.

---

## Export: Print/PDF and a Jupyter notebook, alongside Download to keep

`#dl-settings-export` (`assets/shell.html`, wired by `initExportSection()`)
sits right after the existing "Download to keep" section, but is
deliberately its own section rather than folded into it: `build.py`'s
standalone/offline export strips `#dl-settings-download`'s entire content
out of the page it bakes (its own comment — "the offer to download it is
already taken, this is the download"), and Print and Jupyter export are
just as useful *inside* an already-downloaded copy, so they can't live
somewhere that vanishes from it.

Print calls nothing more than `window.print()` — the actual work is
`tutorial-style.css`'s `@media print` block, which hides the chrome,
panels, and insert seams and forces light ink on cells regardless of the
reader's theme (ported from `compose/dewmini-style.css`'s own, longer-
established print block). "Save as a Jupyter notebook"
(`downloadAsIpynb()`) walks every `.dl-cell` on the page — real and
custom alike — in document order (the same order printing shows them
in), turning a python cell into a `"code"` cell and a custom text cell
into `"markdown"`. It deliberately does not try to turn the tutorial's
own *prose* into markdown cells: by the time this runs, the reading only
exists as built HTML, not the original Markdown source, so a faithful
conversion back is a separate, much larger job — Print and Download to
keep already cover the full page, and the Settings panel note says so.

---

## The pill, the run line, collapse, Duplicate, the "⋯" run menu, and Restart & run all

Several pieces ported from `compose/dewmini.js`, once that file had
already proven them out: a numbered, coloured identity pill (`Cell N`
plus its type); a single merged run line reporting order, duration, and
staleness together; "Run above"/"Run below"; and Settings' "Restart &
run all". They didn't move wholesale — dewmini's `cells` array holds a
plain `.content` string kept
in sync by hand, while this file's cells only ever ask their own
CodeMirror editor for its current value (`getCode()`), so `isStale()`
here compares against that instead of a mirrored field; and dewmini's
pill number is live-recomputed on every reorder (cells can be dragged),
while `build.py`'s is a static, build-time position (`render_cell()`'s
`number` argument) since authored cells never move. The functions are
otherwise a close, deliberate copy, including the reasoning in their own
comments — `runCellBatch()`'s `reset` parameter, in particular, is worth
reading there rather than here, since it explains why "Run below" is the
one caller that must *not* reset the namespace first.

The run line (`.dl-cell-runline`, `renderCellRunLine()`) replaced what
used to be two separate elements — a `.dl-cell-stats` span ("Ran in
340 ms") and a `.dl-cell-stale-badge` ("edited since last run") shown or
hidden independently. They're folded into one line here because a
reader reads them together anyway: "Ran 1st in 340 ms", or with the
edit flag, "Ran 1st in 340 ms — edited since". The run order
(`ranOrder`, from a module-level `runSequenceCounter`) is new here —
tutorial pages previously had no notion of *when*, relative to other
cells, a given cell last ran, only whether its output matched its
current code. The counter resets to 0, and every cell's `ranOrder` along
with it, on any full namespace reset: "Restart & run all" and a
standalone "Restart Python" both call `resetRunSequence()`, and
"Run above"/"Run below" already reset the namespace first when their own
`reset: true` applies. A cell mid-run shows a live "Running… 1.6 s" via
`startRunLineTicker()`, a plain 100 ms timer rather than an `aria-live`
region (announcing a number changing ten times a second would be noise,
not information, for anyone using a screen reader); the very next cell
queued in a batch shows "Running next" via `setRunLineQueued()`.

`executeCell()` is the seam this needed that didn't already exist: the
old `runCell()` inlined "time it, run it, save it" directly, which is
fine for a single cell's own Stop-capable button but has nothing to say
about *loops over several cells*, wanting each one to get that same
Stop-button treatment as its own turn comes up. `runCell()` now just
wraps `executeCell()` with the single-cell Run/Stop button dance;
`runCellBatch()` wraps it with the same dance run once per cell in a
list, plus the batch-level status line. Neither duplicates the actual
running-and-timing logic.

Restarting Python is a heavier version of the same idea already used for
"Run all"/"Run above": `resetPageState()` (worker message type
`reset-page-state`, already in `assets/pyodide-worker.js` for dewmini's
own use) clears and re-seeds the shared namespace without throwing
anything away; `restartPython()` throws the whole interpreter away —
terminating the Worker, or dropping every main-thread Pyodide reference,
depending on which path this page is on — so a later `ensureBooted()`
boots a genuinely fresh one. That's a strictly stronger reproducibility
check than a reset (Jedi's completion cache and anything else only a
real restart clears go with it too), which is why Settings offers both
"Restart Python" alone and "Restart & run all" together, mirroring
dewmini's own two buttons.

`setCellCollapsed(cell, collapsed)` hides a cell's editable content
(`.dl-cell-content` — the CodeMirror editor for a python cell, or both
the textarea and rendered view for a custom text cell) behind a
one-line summary, leaving the output and the bar beneath it visible.
It's one standalone function rather than a per-cell closure the way
dewmini's own `setCollapsed()` is, because it has to serve both
`buildCells()` (authored cells) and `mountCustomCellAfter()` (custom
cells) the same way — it reads `cell.collapseBtn`/`contentRegion`/
`collapsedSummary`, set once when each cell is built, rather than
closing over element references of its own. Saving after a toggle is
immediate (`saveNow()`/`saveCustomCells()`), not the debounced
`scheduleSave()`/`scheduleCustomSave()` every keystroke goes through —
a discrete click has nothing to coalesce, and debouncing it risks
losing the state to a reload that beats the timer (a real bug an e2e
test caught during 7.114, before it shipped).

Duplicate (`.dl-btn-duplicate`, `duplicateAsCustomCell(cell, type)`)
means something narrower here than in dewmini, because an authored cell
isn't the reader's own the way every dewmini cell is — it's the
tutorial's own fixed content. Clicking it doesn't touch the original; it
drops a new *custom* cell, seeded with the original's current code,
immediately after it. This rides entirely on insertion machinery that
already existed for an unrelated reason: every cell this file mounts,
real or custom, gets its own trailing `.dl-insert` divider right after
it (`initCustomCellsSection()`/`mountCustomCellAfter()`) — the same
seam "+Code"/"+Text" already use for "Try something of your own" —
and `duplicateAsCustomCell()` just calls the same `insertCustomCell()`
those buttons call, finding its divider via `cell.element.nextElementSibling`
rather than searching for it, so the copy lands right after *this*
cell even if a reader has since added their own cells further down the
same chain. Custom cells got a Duplicate button too, `type` carried
through so a text cell's own copy stays text.

A rendered custom text cell goes quiet until touched (`.dl-cell-text`,
`assets/tutorial-style.css`, DECISIONS_LOG.md 7.115): its `.dl-cell-head`
and `.dl-cell-collapse-col` sit at `opacity: 0; pointer-events: none`
until a reader hovers or focuses the cell, so a rendered note reads like
part of the page rather than a code widget sitting open among cells that
are meant to be run. Pure CSS, ported from `compose/dewmini-style.css`'s
own `.dm-cell-text` rule — `:focus-within` already covers "actively
editing" (focusing the textarea puts the whole cell in that state), so
no JS class-toggling was needed on either side.

## Head, body row, footbar: the last gap with dewmini's own cells

Everything above ported dewmini's *content* (the pill, the run line,
collapse, Duplicate) onto `build.py`'s existing `.dl-cell-head`/
`.dl-cell-bar` shape without moving anything — that shape had Run sitting
*after* both the editor and the output, where dewmini's own footbar sits
*between* them. A reader who had just learned "Run is under the code" in
dewmini found it somewhere else entirely on a tutorial page — one of a
short list of small, real mismatches now closed. `render_cell()` now
emits three rows in the order dewmini's own cells already use —
`.dl-cell-head` (identity: the pill, an optional `.dl-cell-name`, then
Duplicate), `.dl-cell-body-row` (the
collapse triangle and the editor), `.dl-cell-footbar` (Run, Reset, Clear,
the run menu, the run line) — with `.dl-output` last. `createCustomCellElement()`
here builds the same three rows by hand for a reader's own cells, since
nothing in this file generates markup from `render_cell()` directly.

Two things rode along with the move rather than needing one of their own:

- **A cell now has two buttons where it once had one double-duty Reset.**
  `.dl-btn-reset` clears a cell's *output* only, touching no code — the
  same action, and the same counterclockwise ↺ icon, as dewmini's own
  footbar button. `.dl-btn-clear` puts the cell's *code* back to its
  starter and throws away whatever a reader typed, behind a confirmation
  dialog; it keeps the clockwise ↻ icon and resting red-ish border
  (`tutorial-style.css`) the old single button carried, since it is the
  one still doing something a reader can't undo.
- **A cell can carry a name.** `name:` is a fourth header line beside
  `id:`/`hint:`/`expect:` (`HEADER_RE`, `Cell.name`, `build.py`), shown
  in `.dl-cell-name` next to the pill — "a handle to hold on to" when a
  reader wants to talk about a specific cell by something more than its
  number. It also replaces the cell's own id in a traceback's file line
  once given (`run_cell()`'s new `label` parameter, threaded through
  `run_cell_report()`/`runCellMainThread()`/`runCellWorker()` here down
  to `tutorial_tools.cell_filename()`), the same reasoning dewmini's own
  `executeCell()` uses for its `Cell N` fallback.

Every button built by `icon_button()` (`build.py`) or `iconButtonHtml()`
(here) now carries a nested `.dl-btn-icon`/`.dl-btn-label` pair rather
than bare text — not for its own sake, but so Settings' new "Cell
buttons" row (`data-texture="buttons"`, `TEXTURE_DEFAULTS.buttons`,
`applyTexture()`) can show icon, label, or both by toggling one
`[data-button-labels]` attribute on `<html>` (`tutorial-style.css`) with
no markup rewrite per mode. It rides the same generic `initTexture()`
machinery every other Texture row already uses, so no new Settings
wiring function was needed — only the row itself
(`assets/shell.html#dl-settings-code-texture`) and the two lines in
`applyTexture()` that set or clear the attribute. `setBtnLabel()`/
`getBtnLabel()` here read or write a button's `.dl-btn-label` span
directly, since setting `.textContent` on the button itself would erase
its icon along with whatever text was there — every place that used to
set a Run/Preview button's `.textContent` (`setRunnable()`,
`setCellRunning()`/`clearCellRunning()`, the text cell's own
`syncPreviewBtn()`) goes through one of these two now instead. The small,
fixed-size badge buttons — the hint and report toggles, the collapse
triangle — deliberately were not given this treatment: they have no
dewmini counterpart to stay consistent with, and a text label would not
fit their compact, circular shape.

`compose/dewmini.js` carries the same three changes on its own side —
`.dm-icon-reset-output` keeps its original counterclockwise icon rather
than drifting to this file's clockwise one, every `.dm-icon-btn` gained
the same `.dl-btn-icon`/`.dl-btn-label` pair via a `iconButton()` helper
there, and a cell gained an editable `.dm-cell-name`/`.dl-cell-name`
input beside its pill — see `docs/dewmini-js-explained.md` for that half.

---

## Two patterns worth understanding on their own

**Four panels, one rule; three of them a dock.** The four right-hand
panels (Notes, Python, Settings — Appearance/Behavior/Imports & Exports
behind one tablist-switched toggle — and Report, `RIGHT_PANELS`) are
separate, independent UI components — but opening any one of them always
closes the other three, since they share one edge of the screen. There's
no shared "panel manager" object making that happen; each panel's own
`setOpen(true)` just calls `closeRightPanels(itsOwnName)` directly. The
Reference panel on the left is not in that group: it has its own edge, so
it can stay open alongside any of the four.

Three of those four are rails, and `RIGHT_DOCK_PANELS` is that shorter
list. Notes, Python and Settings dock to the screen's edge full height,
share one saved width (`RIGHT_DOCK_WIDTH_KEY`, not each panel's own DOM
id) — dragging any one's edge applies the new width to the other two right
away, so a reader switching which tab is open never sees the dock, and the
reading column beside it, resize — are what the reading column's own
gutter is measured against (`watchPanelOverlap()`), and are what a reader's
saved open panel can name (`saveSidebarState()`). Report is none of those
things: it is a popover above its own fixed circle at the bottom-right
(`.dl-report-popover`), so it borrows only this group's one-open-at-a-time
rule and its Escape handling, closes on an outside click where a rail does
not, and is not remembered from one page to the next. Anywhere the code
says `RIGHT_DOCK_PANELS` rather than `RIGHT_PANELS`, that difference is
what it is saying.

**Live-then-static code intelligence, worker-or-main-thread.** Hover docs
and autocomplete work by trying two different techniques and taking
whichever answers first: a *live* lookup (asking Python's own `inspect`
module about an object that has actually run) and a *static* one (asking
the Jedi library to guess from the source text alone, for code that
hasn't run yet). This combination happens on whichever thread Python is
actually running on — inside the Worker for the hosted site, or right
here on the main thread for the offline export — which is why there are
two near-identical implementations of the same lookup functions
(`docFor`-style vs. `docForMT`-style) rather than one. Completion is the
one place Jedi goes first: `jediCompletions()` asks it for attributes and
names together, reading the live namespace as well as the text, and
`pageNamesCompletion()` answers only when Jedi is silent (see
`vendor-src/codemirror-entry.js`'s `pythonCompletion()`).

---

## The toolkit: earlier pages' functions, loaded before the first cell

A page whose manifest has a `toolkit` list (build.py's `toolkit_for()`:
every `toolkit: yes` cell on an earlier page of the course, in course
order, each with its reference code) loads those cells into the shared
namespace before any of its own run. `loadToolkit()` is the one entry
point, called from three places: both boot paths (`bootWorker()` and
`bootMainThread()`, before the page becomes runnable, so a Run click
that waits on `ensureBooted()` also waits for the toolkit), and
`resetPageState()`, which every namespace-clearing path goes through
("Run this cell and all above", "Restart & run all"'s run half). A
restart reboots, so it takes the boot path.

Which version of each cell runs is the one decision made here rather
than in Python. The mode is a site-wide setting, `dewlab:toolkit-mode`
(`readToolkitMode()`/`writeToolkitMode()`, `mine` unless it says
`reference`). In `mine`, `savedToolkitCode()` reads the reader's code for
that cell straight out of the other page's saved record
(`dewlab:progress:<tutorial id>`, the record `saveNow()` writes there),
and marks an entry with nothing saved as `unsaved`. On a downloaded page
(`manifest.standalone`) there is no other page's record to read, so it
always sends the reference. Everything else — running each entry with
its output thrown away, taking each function the reader left out or left
as a stub from the reference (`_functions_in()`/`_is_placeholder()`),
undoing a reader's version that raised and running the reference in its
place, running each entry in a namespace of its own and copying back
only the names it defines (never those its `import` lines bind), and
naming the functions and classes the toolkit defined — is
`tutorial_tools._load_toolkit()`,
reached through a `"load-toolkit"` worker message or `toolsMT` directly,
the same fork as every other dual-path call here.

The line above the first cell (`buildToolkitLine()`,
`renderToolkitLine()`, `.dl-toolkit` in `tutorial-style.css`) says what
will load before Python has booted, what did load afterwards, and which
functions came from the reference and why ("You have not written … yet",
"… your version raised an error"). Past `TOOLKIT_NAMES_INLINE` (eight)
functions it gives a count instead of naming each one, and a closed
`.dl-toolkit-list` under it lists them page by page
(`toolkitListHtml()`), marking the ones that came from the reference
when the reader wrote some of their own. Its two radio buttons write
the mode; if Python is running, the toolkit reloads straight away, or,
when a cell is running, as soon as it finishes
(`reloadToolkitIfPending()`).

---

## Highlights: colour, the Notes panel's own list, and My Notes

A highlight anchors to a passage of prose (`locateHighlightAnchor()`,
`describeQuote()`) rather than a build-time id — see `DECISIONS_LOG.md`
7.155–7.160 for why that turned out cheap. Everything past that base is
this file's own addition, built together rather than across six rollout
steps the way the base feature was:

- **Colour.** `HIGHLIGHT_COLORS` names four (amber the default, then
  green/blue/pink); a highlight's `color` field rides in the same saved
  record `note` already does. The popover's swatch row
  (`initHighlightPopover()`) recolours a mark immediately on click —
  `recolorHighlight()` sets or clears `[data-highlight-color]` on every
  `<mark>` sharing that id, since a highlight split across an inline
  element (`wrapRange()`'s own comment explains when) is more than one
  `<mark>`. A fresh highlight starts in whichever colour was used last,
  read back from `localStorage` (`readLastHighlightColor()`) — across
  every tutorial, not per page, since a reader's own colour scheme is a
  reader-wide choice.
- **The Notes panel's own list** (`refreshHighlightsList()`,
  `renderHighlightRow()`) turns the in-memory `highlights` array into
  something reviewable: one row per highlight, a colour dot, the quote,
  and a note preview if there is one. It's also the only place on the
  page that says highlighting exists at all — nothing about the
  selection toolbar itself hints at it — so its own copy carries that
  explanation. Clicking a row calls `jumpToHighlight()`: close the
  panels, scroll the mark into view, pulse it (`.dl-highlight-flash`,
  `tutorial-style.css`), and open its popover, the same three things
  clicking the mark directly does.
- **My Notes** (`all-notes.html`, `write_all_notes_page()` in `build.py`,
  `assets/my-notes.js`) is the same idea across every tutorial at once.
  The link to it is the first thing in the Notes panel, above this page's
  own notes; it sat under the wordmark until 7.204, where a reader looking
  for what they had written had no reason to look.
  `localStorage` is shared per origin, not per page, so this page reads
  every `dewlab:progress:*` record itself, client-side — nothing here
  needs a server or an account. The one thing storage can't supply is a
  human title for a bare slug, so the build bakes in a small
  `{slug: title}` map as a JSON data island (`#dewlab-titles`), the same
  pattern `tree.js` already uses for its own topic-graph data. A card's
  own highlight rows link to `tutorials/<slug>.html#dl-highlight-<id>`;
  landing on that hash (checked once, at boot, after `renderMaths()`
  settles the page's layout) calls `jumpToHighlight()` again, this time
  with `openPopover: false` — a reader arriving from a link is visiting a
  passage to re-read it, not asking to edit it.

---

## Where to look for something specific

- **"Why does the offline download work differently from the hosted
  site?"** — `manifest.standalone`, checked throughout the Pyodide
  section. A `file://`-opened page can't reliably create a module Worker,
  so the standalone export always uses the main-thread path — see the
  module's own top comment and `DECISIONS_LOG.md` 7.77 for the full
  reasoning.
- **"Why does the Reference panel's search find `loop` when I type
  `loops`?"** — `filterReferenceContent()`/`filterBasicsContent()` match
  through `textMatches()` in `assets/search-words.js`, the same stems,
  synonyms and prefixes every other search box on the site uses, with a
  raw substring still accepted so a fragment narrows the list.
- **"Where does a page's saved work live, and what happened to the old
  `module:slug` keys?"** — `pageKey()`: every key is `dewlab:<kind>:<id>`,
  the id being the tutorial's folder name. `migrateStorage()`, run before
  anything reads a key, renames the keys a page's manifest `legacy` names
  (its address before `courses/` existed) and never overwrites work saved
  under the new key since. `describeMismatch()` accepts an exported file
  that names the page by id, or by the module and slug `legacy` says.
- **"How does the tree know which course I am on?"** — `initCourse()`:
  a course page remembers itself in `dewlab:course`; a tutorial listed on
  more than one course fetches `assets/routes.json`, adds a chooser to the
  tree's course rung (`addCourseChooser()`), and `drawCourseChrome()`
  redraws the course and series rungs, previous/next and the "also part
  of" line for the chosen course. A page on one course does none of this.
- **"How does a reader's saved work survive a tutorial being updated?"**
  — the Versions section, especially `carryOver()`/`describeCarry()`:
  saved work is keyed by tutorial, not by release, and restoring matches
  cells by id, so an answer just... still applies, as long as the cell it
  belongs to still exists in the release being switched to.
- **"Why is there a `dl-nudge` class on the notes-export button?"** —
  `updateNotesNudge()`/`markNotesExported()`: a small, deliberately rough
  heuristic (has enough new text piled up since the last export?) rather
  than anything precise.
- **"What happens when I press Compare with a solution?"** —
  `initCompare()`, called from `buildCells()` for a cell whose manifest
  entry has `inputs` (and usually a `solution`, and a `tests` cell id).
  `compareCell()` runs the cell as it stands (`runCell()`), then calls
  `tutorial_tools.compare()` through a `"compare"` worker message or
  `toolsMT` directly (`compareMainThread()`), the usual fork on
  `manifest.standalone`. `renderComparison()` fills the table the build
  wrote (`.dl-compare`, build.py's `render_inputs()`) with plain text
  only, adds a "Your tests" section when the reader has a tests cell,
  and marks a row that differs with `.dl-compare-differ` and the word
  "different". A guess column's boxes save with the cell
  (`cellGuesses()`/`restoreGuesses()`, the record's `guesses`).
- **"What does the predict block above a cell do?"** — `initPredict()`,
  called from `buildCells()` for a cell whose `.dl-predict` the build drew
  above it (build.py's `render_predict()`). `setSure()` records how sure
  the reader is; "I'm not sure yet" reveals and opens the cell's first
  staged hint whatever the Settings toggle says, and counts an `unsure`
  signal. After every run, `executeCell()` calls `notePrediction()`, which
  compares the guess with the cell's printed output (`guessMatches()`:
  the last number within the tolerance, or the whole output or last line
  with spacing ignored and case kept), counts `guess differed`, and
  `renderPrediction()` shows the two side by side with the chosen option's
  note. `updateSurprises()` fills the page's `.dl-surprises` list. The
  record's `prediction` holds guess, sureness and outcome
  (`predictionRecord()`/`restorePrediction()`), and `downloadAsIpynb()`
  writes a guess as a markdown cell above its code.
- **"How does a hint decide to appear under a cell?"** — the staged-hints
  block after `executeCell()`: `noteAttempt()` updates a cell's counters
  from the run's report, `triggerHolds()` tests a fold's `data-after`
  terms against them, `maybeRevealHint()` shows at most one fold per run
  and none once `expect:` holds. The counters and which folds have shown
  travel in the saved record (`attempts`, `hints_shown`), and two Settings
  rows (`initStagedHintsToggles()`) decide whether they show at all and
  whether a restart hides them.
- **"Where does a function from an earlier page come from?"** —
  `loadToolkit()` and the section on the toolkit above; the list itself is
  build.py's `toolkit_for()`, and running it is
  `tutorial_tools._load_toolkit()`.
- **"What's actually exposed to the browser console / end-to-end tests?"**
  — the `globalThis.dewlab = {...}` object at the very end of the file.
- **"Why doesn't a shared custom cell run itself when I load it?"** —
  `importCustomCell()`'s own comment: a loaded cell is deliberately never
  auto-run, so the Settings trust note (`assets/shell.html`,
  `#dl-settings-custom-cells`) is read before anything from someone
  else's file actually executes, not after.
- **"A tutorial update removed a cell — what happens to a custom cell
  that was added right after it?"** — `initCustomCellsSection()`'s own
  comment on the anchor fallback: it moves to the trailing "Try
  something of your own" section rather than disappearing.
- **"Why doesn't 'Save as a Jupyter notebook' include the tutorial's own
  reading, only the cells?"** — `downloadAsIpynb()`'s own comment: the
  reading only exists as built HTML by the time that function runs, not
  the original Markdown, so turning it back into notebook markdown
  faithfully is out of scope here on purpose.
