# `compose/dewmini.js`, explained

This file is everything that makes dewmini work: creating and deleting
cells, running Python, the file manager, drag-to-reorder, downloads and
notebook import, Settings, and the practice-problem picker. It does
**not** run Python itself — that's
[`assets/pyodide-engine.js`](pyodide-engine-explained.md)'s job — and it
does **not** decide where files are stored — that's
`compose/dewmini-fs.js`'s job. This file is the "glue": a `cells` array
as the source of truth, a save-then-render pattern for every change, the
drag-and-drop mechanics, and the Run-becomes-Stop button pattern.

---

## The big idea: `cells` is the source of truth

Almost everything in this file changes the module-level `cells` array
first, then calls `saveState()` and `renderCells()` to catch the page
up. A cell object here is `{ id, type, content, output, error }`, plus
`lastRunMs` and (for a Python cell that has run at least once)
`ranContent` — the content as it looked at that run, compared against
the cell's current content to show the "Edited since last run" badge
(DECISIONS_LOG.md 7.105) — and, once it's actually drawn on the page, a
few DOM-referencing properties (`.outputEl`, `.runBtn`, `.staleEl`) —
the rule is: change the data, then make the page match it, never the
other way around. `ranContent` is deliberately *not* one of the fields
`saveState()`/`readCells()` carry to and from `localStorage`: it
describes a live Python session, and no live session survives a reload,
so neither should the claim that one is stale.

`ranContent` is also the groundwork a not-yet-built feature would sit
on: `planning/CELL_IDENTITY.md` designs an execution counter and a
per-type cell header (numbered pill, run order, duration) that would
read this same field rather than add a new one.

### …and `cells` belongs to a notebook

Since tabs, `cells` is not the only notebook — it is the *active* one.
`notebooks` holds `{ id, name, cells }` for each open tab, and `cells`
points at whichever is active.

The important word is *points*: `cells` is the same array object the
active notebook holds, not a copy. That is what let tabs arrive without
rewriting every function in this file — they all still work on `cells`
and neither know nor care that there are others. Switching tabs
re-points one variable and re-renders.

The cost of that trick is one hazard worth knowing about, and it is why
`setCells()` exists. Assigning `cells = something` on its own would
leave the notebook still holding the *old* array, so edits would land in
an array attached to nothing — visible on screen, and silently gone the
moment you switched tabs and back. Any code replacing a notebook's cells
wholesale (loading the example, clearing, importing) has to go through
`setCells()`. `tests/e2e/test_dewmini_workbench.py` covers exactly that
round trip, because it is the kind of mistake that looks fine until it
doesn't.

Cell *execution* and cell *filesystem access* both go through
`assets/pyodide-engine.js` and `compose/dewmini-fs.js` respectively,
imported at the top of this file (`import * as engine ...`, `import *
as dfs ...`) — this file never talks to Pyodide or the filesystem
directly. `engine.configure({...})`, called once near the top, is what
wires the shared engine up to this specific page: how to find a cell's
output element, where to show status text, which Pyodide packages to
load, and `dataBase` (dewmini lives one directory below the site root,
so it needs a different base path to reach the shared `data/` folder
for `load_csv()`).

---

## Reading order

1. **Config and state** at the top — the `engine`/`dfs` imports,
   `DM_PACKAGES` (dewmini's wider package list — it adds `sqlite3` and
   `Pillow` beyond a tutorial page's baseline, since it isn't tied to
   one curriculum), the `engine.configure({...})` call, and the
   module-level variables that hold the whole notebook's state
   (`cells`, `running`, `runningCellId`).
2. **Storage** — `generateId`, `loadSavedState`, `saveState`.
3. **Cells** — `insertCellAt`/`addCell`/`deleteCell`/`focusCell`, the
   text-cell markdown renderer (`escapeHtml`/`renderDocInline`/
   `extractDocMath`/`renderDocMathSpan`/`renderDocMarkdown`), the KaTeX
   lazy-loader (`loadKatexRenderMath`/`renderMathsIn`), the
   image-attachment picker, `renderCells`, `createRunMoreMenu` (the
   per-cell "⋯" Run-above/Run-below popover), and `createCellElement`
   (the big one — builds a cell's entire DOM tree, and wires
   `completeNames`/`getDoc`/`getSignature` straight to the shared
   engine's own `pageNamesCompletion`/`hoverDoc`/`signatureHelp`).
4. **Execution** — `ensurePyodide` (boots the shared engine, then mounts
   the filesystem — `dfs.init()` — once it has), `executeCell` (runs one
   cell through `engine.runCell()`, records `ranContent`, and syncs the
   filesystem afterward, in case the cell wrote to it directly),
   `setRunButtonRunning`/`resetRunButton` (the Run-becomes-Stop button),
   `runCell` (a second click on the currently-running cell sends
   `engine.requestInterrupt()` instead of starting a new run),
   `runCellBatch` (the shared batch runner behind `runAllCells`/
   `runAbove`/`runBelow` — see below), `restartPython` (factored out of
   "Restart Python", also the first half of "Restart & run all").
5. **Downloads** — `triggerDownload` (the shared Blob-download trick),
   then `downloadAsPython`/`downloadAsIpynb`/`downloadAsHtml`, the last
   of which builds an entire second, self-contained HTML page as a
   string (`buildStandaloneHtml`) — worth reading closely if you haven't
   seen this pattern before.
6. **Practice** — the practice-bank fetch, the sequential/random
   ordering logic (`shuffledRange`'s Fisher–Yates shuffle is a nice
   small example of a well-known algorithm), and `addPracticeProblem`.
7. **Import** — `handleImportFile`, `parseIpynbCells`/`parsePyCells`
   (a `.py` dewmini itself exported comes back cell-for-cell; an
   unmarked script becomes one cell), `scanPyodideCompatibility`
   (flagging things Pyodide's Python can't run before they cause a
   confusing error).
8. **Drag reorder** — `setupDragAndDrop`, using the browser's native
   HTML5 Drag and Drop API.
9. **Status, panels, execution status, storage, texture, editor prefs,
   notes** — `updateExecutionStatus`/`initExecutionSection` (the
   Settings "Python" section: which mode booted, Restart Python, and
   Restart & run all);
   `updateStorageStatus`/`renderFileList`/`deleteFsFile`/
   `uploadFsFiles`/`initStorageSection` (the Settings "Files" section,
   all going through `dfs`, never touching a filesystem directly);
   several smaller pieces close cousins of functions in
   [`tutorial-runtime.js`](tutorial-runtime-explained.md) doing the same
   job for the shared reading-preference settings.
10. **Start**, at the bottom — `init()` and the
    `DOMContentLoaded`-or-run-now guard against a module script's
    double-init problem.

---

## Two patterns worth understanding on their own

**A small line-based Markdown parser.** Text cells support a deliberately
small set of formatting (headings, bold, italic, code, bullets, images) —
not real Markdown, on purpose (see the section comment above
`escapeHtml`). `renderDocMarkdown` reads the text one line at a time,
tracking whether a paragraph or a bullet list is currently "open," and
decides what to output based on what kind of line it just saw. This is a
good small example of how a simple parser can be built without a parsing
library, for a format simple enough not to need one.

**Extract, then restore, for maths the same way as for cells and code
blocks.** `renderDocMarkdown` extracts `$…$`/`$$…$$` into placeholder
tokens (`extractDocMath`) *before* its line-by-line pass runs, and only
restores them to real `<span class="dl-math">` markup at the very end,
after `escapeHtml`/`renderDocInline` have already touched everything
else. This is a JavaScript port of `build.py`'s own
`extract_math`/`render_math`/`place_blocks` pattern, not a call into it —
dewmini's text cells never go through Python — but the reason is
identical: letting the line-based parser see raw TeX first means
`$a_i$`'s underscore gets read as `renderDocInline`'s emphasis marker
before anyone gets a chance to render it as maths. See
DECISIONS_LOG.md 7.107 for the rest of the maths decision, including why
this is deliberately a *second* implementation of the same idea rather
than a shared one with the tutorial pipeline.

**A button that has to listen on `mousedown`, not `click`.** A text
cell's header carries an explicit Edit/View button (`previewBtn` in
`createCellElement`) alongside the older gestures — blur the textarea to
render it, click the rendered view to edit it again — because neither
gesture has an equivalent on a touch device with no hover to reveal that
the rendered text is even clickable. The button can't just listen for
`click`, though: clicking it while the textarea is still focused blurs
the textarea *first* (which renders it), and only then reaches the
button's own handler — by which point the state it would read has
already flipped, so it would toggle straight back to editing instead of
landing on rendered. `previewBtn.addEventListener("mousedown", (e) =>
e.preventDefault())` is what stops that blur from happening at all,
so the click handler underneath still sees the state as it was when the
reader actually clicked. `assets/tutorial-runtime.js`'s own text cells
use the identical fix.

**A downloadable file that builds another whole HTML page.**
`buildStandaloneHtml` is worth slowing down on: it returns a giant
template-literal string that *is* a complete HTML page, with its own
`<script>` tag containing real JavaScript that will run later, in a
different browser tab, possibly on a different day. The trick that makes
it self-contained is embedding data with `JSON.stringify(...)` directly
into that inner script as constants — there's no way for the downloaded
file to fetch anything from dewlab once it's been saved somewhere else on
a reader's computer, so everything it needs (the tools' Python source,
the cells' content) has to travel inside the file itself.

**Boot the engine before deciding what the Run button looks like.**
`runCell()` awaits `ensurePyodide()` *before* calling
`setRunButtonRunning()`, not after — `setRunButtonRunning()` reads
`engine.canStop()` to decide whether the button becomes a genuine Stop
or just a disabled "busy" indicator, and `canStop()` only knows worker-
vs-main-thread once `ensureBooted()` has actually resolved. Calling
`ensurePyodide()` after `setRunButtonRunning()` instead — reading
`canStop()`'s pre-boot default — was a real bug this file's own Worker
migration introduced and testing caught: the button never offered a
genuine Stop on a page's first-ever cell run, even in worker mode, since
the boot hadn't happened yet at the moment the button's state was
decided.

---

## Where to look for something specific

- **"Why doesn't Stop do anything?"** — `engine.canStop()`, read inside
  `setRunButtonRunning()`; it's only true on the Worker path with a real
  interrupt buffer (see [`docs/pyodide-engine-explained.md`](pyodide-engine-explained.md)).
  A page opened over `file://` where a module Worker can't be created
  falls back to the main thread, where nothing can interrupt a running
  cell.
- **"How does a file a cell writes actually get saved?"** —
  `executeCell()` calls `dfs.sync()` (fire-and-forget) after every run,
  independent of `dewmini-fs.js`'s own debounced sync — a cell writing
  straight to the mounted path with `open()` or `sqlite3.connect()`
  never touches `dfs.writeFile()` at all, so nothing else would
  otherwise know a write happened.
- **"How does drag-and-drop actually work?"** — `setupDragAndDrop()`'s own
  comment walks through all four Drag and Drop events in order.
- **"Why does Run All reset everything first?"** — `runCellBatch()`'s own
  comment: it calls `engine.resetPageState()` so a stale value from a
  previous run can never mask a genuine mistake. `runAbove()` does the
  same for the same reason; `runBelow()` deliberately does not, since its
  whole point is keeping what came before it (DECISIONS_LOG.md 7.106).
- **"How is 'Restart & run all' different from 'Run all'?"** — `runAllCells()`
  only calls `engine.resetPageState()` (clear and re-seed the same
  interpreter); "Restart & run all" calls `restartPython()` first, a real
  `engine.restart()` that also clears Jedi's cache and the mounted
  filesystem handle. See DECISIONS_LOG.md 7.108.
- **"How does an imported `.ipynb`'s source turn into a string?"** —
  `handleImportFile()`'s comment on why source can arrive as either a
  plain string or an array of lines, and `splitLines()` for the reverse
  direction (exporting).
