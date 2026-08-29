# `compose/dewmini.js`, explained

This file is everything that makes dewmini work: creating and deleting
cells, running Python, drag-to-reorder, downloads, Settings, and the
practice-problem picker. Unlike Mini IDE (split across
`mini-ide.js`/`mini-ide-engine.js`/`mini-ide-fs.js`), dewmini keeps
everything in one file — it's a smaller tool with a smaller scope (no
file manager, no SQL support beyond what `import sqlite3` gives for
free, no filesystem to mount), so one file stays manageable where Mini
IDE's would not have.

If you've already read
[`docs/mini-ide-js-explained.md`](mini-ide-js-explained.md), quite a lot
of this will feel familiar — dewmini and Mini IDE share the same basic
shape (a `cells` array as the source of truth, the same save-then-render
pattern, the same drag-and-drop mechanics) even though neither file
imports code from the other.

---

## The big idea: `cells` is the source of truth, same as Mini IDE

Exactly like `mini-ide.js`, almost everything in this file changes the
module-level `cells` array first, then calls `saveState()` and
`renderCells()` to catch the page up. A cell object here is simpler than
Mini IDE's — no filesystem-backed properties, just `{ id, type, content,
output, error }` — but the rule is identical: change the data, then make
the page match it, never the other way around.

Where dewmini genuinely differs from Mini IDE is how it runs Python:
dewmini runs Pyodide directly on the main thread (`ensurePyodide()`),
with **no Web Worker** and **no Stop button** — the simpler, older
approach. `docs/DEWMINI.md`'s own "What's different from a tutorial page"
section explains the tradeoff in plain language; the short technical
version is that a runaway cell here has to be waited out or the page
reloaded, since nothing is running on a separate thread that could be
interrupted.

---

## Reading order

1. **Config and state** at the top — `DM_PACKAGES` (dewmini's wider
   package list — it adds `sqlite3` and `Pillow` beyond a tutorial page's
   baseline, since it isn't tied to one curriculum), and the module-level
   variables that hold the whole notebook's state.
2. **Storage** — `generateId`, `loadSavedState`, `saveState`.
3. **Cells** — `insertCellAt`/`addCell`/`deleteCell`/`focusCell`, the
   text-cell markdown renderer (`escapeHtml`/`renderDocInline`/
   `renderDocMarkdown`), the image-attachment picker, `renderCells`, and
   `createCellElement` (the big one — builds a cell's entire DOM tree).
4. **Execution** — `ensurePyodide` (boot-lazily, same pattern as Mini
   IDE's engine), `getDocForName` (hover tooltips), `executeCell`/
   `runCell`/`runAllCells`.
5. **Downloads** — `triggerDownload` (the shared Blob-download trick),
   then `downloadAsPython`/`downloadAsIpynb`/`downloadAsHtml`, the last
   of which builds an entire second, self-contained HTML page as a string
   (`buildStandaloneHtml`) — worth reading closely if you haven't seen
   this pattern before.
6. **Practice** — the practice-bank fetch, the sequential/random ordering
   logic (`shuffledRange`'s Fisher–Yates shuffle is a nice small example
   of a well-known algorithm), and `addPracticeProblem`.
7. **Import** — `handleImportFile`, reading a `.ipynb` back in.
8. **Drag reorder** — `setupDragAndDrop`, using the browser's native HTML5
   Drag and Drop API.
9. **Status, panels, texture, editor prefs, notes** — smaller UI pieces,
   several of them close cousins of functions in
   [`tutorial-runtime.js`](tutorial-runtime-explained.md) doing the same
   job for the shared reading-preference settings.
10. **Start**, at the bottom — `init()` and the
    `DOMContentLoaded`-or-run-now guard, the same double-init problem and
    fix `mini-ide.js` had.

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

---

## Where to look for something specific

- **"Why can't I stop a cell that's stuck?"** — dewmini has no Worker and
  no interrupt mechanism; see `ensurePyodide()`'s comment and
  `docs/DEWMINI.md`.
- **"How does drag-and-drop actually work?"** — `setupDragAndDrop()`'s own
  comment walks through all four Drag and Drop events in order.
- **"Why does Run All reset everything first?"** — `runAllCells()`'s own
  comment: it calls `tools.reset_page_state()` so a stale value from a
  previous run can never mask a genuine mistake.
- **"How does an imported `.ipynb`'s source turn into a string?"** —
  `handleImportFile()`'s comment on why source can arrive as either a
  plain string or an array of lines, and `splitLines()` for the reverse
  direction (exporting).
