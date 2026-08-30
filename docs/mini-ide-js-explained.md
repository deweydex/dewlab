# `assets/mini-ide.js`, explained

This file is the heart of Mini IDE. It owns the array of cells, draws
them on the page, wires up every button, and handles saving your work.
It does **not** run Python itself — that's a different file's job (see
[`docs/mini-ide-engine-explained.md`](mini-ide-engine-explained.md)) —
and it does **not** know how files are actually stored (that's
[`docs/mini-ide-fs-explained.md`](mini-ide-fs-explained.md)). This file
is the "glue": it owns the page, and asks those other two files to do
the parts it isn't responsible for.

If you're reading this to understand the code, not just to use Mini
IDE, this doc is your map. The inline comments in the file itself go
into detail on any one function; this doc is about how the pieces fit
together.

---

## The big idea: `cells` is the source of truth

Almost everything in this file revolves around one array, called
`cells`. Each entry is a plain JavaScript object that looks like this:

```js
{
  id: "cell-1234567890-abc123def",
  type: "python",      // or "text"
  content: "print('hi')",
  output: "",           // what the cell showed last time it ran
  hasError: false,
  isSample: false
}
```

The rule this file follows almost everywhere is: **change `cells`
first, then tell the page to catch up.** "Catching up" usually means two
things: `saveState()` (write `cells` to `localStorage`, so it survives
a reload) and `renderCells()` (rebuild the on-screen cells to match).
If you're reading a function and it changes `cells` but doesn't call
those two afterward, that's worth a second look — it usually means
something.

A cell object also grows a few more properties once it's actually drawn
on the page: `.editor` (the CodeMirror instance for a Python cell),
`.textarea` (for a text cell), `.outputEl` (the DOM element its output
goes into), and `.runBtn` (its Run/Stop button). These are convenient —
any code holding a `cell` object can reach its own DOM elements — but
they're also what caused a real bug this session found and fixed: those
live objects contain their own internal circular references (a DOM
node points back to its own parent, which points back to it), and
`JSON.stringify(cells)` — which is what saving to `localStorage`
needs — throws an error the moment it hits a real cycle. The fix,
in `saveState()`, is to build a fresh, plain object with only the
fields worth saving, rather than trying to serialize `cells` directly.
It's a good example of a bug that's easy to introduce (mixing "data"
and "live objects" on the same object feels harmless) and confusing to
debug later (the error shows up in `JSON.stringify`, nowhere near where
the mixing actually happened).

---

## Reading order

The file is organized top to bottom roughly in the order you'd want to
read it:

1. **Configuration Constants and Global State** — the `localStorage`
   keys this file uses, and the handful of module-level variables
   (`cells`, `hasSampleCells`, `runningCellId`, and so on) that make up
   this page's entire state. There's no framework here managing state
   for you; these plain variables *are* the state.
2. **DOM Elements** — every element this file talks to gets looked up
   once, in `init()`, and stored in a variable here. Nothing re-queries
   the DOM for the same element twice.
3. **Settings Functions** — the shared "texture" settings (theme, font,
   size) copied from the tutorial pages, plus Mini-IDE-specific
   sections (Python engine status, file storage status, import
   behavior) added on top of the same settings panel.
4. **Initialization** (`init()`) — runs once, when the page loads. Wires
   up the engine, loads saved cells (a genuinely empty notebook stays
   empty — nothing auto-seeds it), and calls all the `setup*()`/`init*()`
   functions that make the rest of the page interactive.
5. **Event Listeners** (`setupEventListeners()`) — one big function that
   attaches a click handler to every toolbar button, upload input, and
   so on. It's long, but each handler follows the same
   change-then-catch-up pattern described above.
6. **Cell Management** — creating cells, giving them IDs, and turning
   the `cells` array into actual DOM elements (`renderCells()` and
   `createCellElement()`). This is "cells as data and as pixels," not
   "cells as running code."
7. **Cell Execution** — running cells as code. This is where
   `mini-ide-engine.js` gets called. `runCell()` handles one cell,
   `runAllCells()` loops over all of them.
8. **File Tree** — the file manager panel: listing what's in the
   mounted filesystem, uploading, and deleting. All of this talks to
   `mini-ide-fs.js`, never to the filesystem directly.
9. **Notebook Import** — turning a `.ipynb` or `.py` file into cells.
10. **Download Functions** — the reverse direction: turning cells into a
    `.py`, `.html`, or `.ipynb` file you can save.
11. **Drag and Drop** — reordering cells by dragging their headers,
    using the browser's built-in HTML5 Drag and Drop API.
12. **Utility Functions** and the bottom-of-file **bootstrap** — small
    helpers, and the two lines that actually call `init()` when the
    page is ready.

---

## Two patterns worth understanding on their own

**The "boot lazily, boot once" pattern.** Starting Python is expensive
(it's a real download), so nothing in this file starts it just because
the page loaded — only the first time a cell actually needs to run,
via `ensureEngineAndFsReady()`. That function is careful to only try
mounting the filesystem once (`if (!fsReady)`), even though it might be
called again on a later Run click; Phase 2's filesystem module has its
own, separate guard against mounting twice, but this file's own
`fsReady` flag means it doesn't even ask a second time.

**The Run-becomes-Stop pattern.** A cell's Run button isn't two
different buttons — it's one button whose label and behavior change
depending on `runningCellId`. Clicking it while nothing is running
starts the cell; clicking the *same* cell's button again while it's
running sends an interrupt instead. This is handled by a few small
functions working together: `runCell()` checks which case it's in,
`setRunButtonRunning()` relabels the button once a run starts, and
`resetRunButton()` puts it back once the run ends (successfully or
not) — all three exist as separate functions specifically so `runCell`
itself stays readable, rather than having all of that logic inline.

**Text cells render, and a button — not just a gesture — is what gets
you back to editing.** A text cell used to be a plain `<textarea>`; it's
now a `.dl-doc-editor`/`.dl-doc-render` pair (the same shape and the same
`renderDocMarkdown()` `compose/dewmini.js` and
`assets/tutorial-runtime.js`'s own text cells use — this file ported
rather than reinvented it), so a short note reads as formatted text
instead of raw markdown syntax. Blurring the textarea renders it;
clicking the rendered view edits it again — but the cell's header also
carries an explicit Edit/View button (`previewBtn` in
`createCellElement()`), because neither gesture has an equivalent
affordance on a touch device with no hover to reveal that the rendered
text is clickable at all. That button listens on `mousedown` with
`preventDefault()`, not `click` — a click while the textarea is still
focused would blur it first (auto-rendering it), so by the time a
`click` handler ran it would see the already-flipped state and toggle
straight back to editing instead of landing on rendered. One consequence
worth knowing: `getDefaultContent()`'s text case is genuinely empty, not
placeholder boilerplate, precisely because a freshly added cell with
non-empty starter text would immediately render — forcing an extra click
before a reader could even start typing over it.

**Shift+Enter has to intercept the keystroke before CodeMirror sees
it.** The listener that runs a Python cell on Shift+Enter is attached to
`editorEl` with a third argument of `true` — capture phase, not the
default bubble phase. CodeMirror's own keymap handles Enter first if the
event reaches it on the way down in the normal order, inserting a
newline instead of running anything; attaching in capture phase means
this file's handler sees the keydown before CodeMirror's editor does,
so it can call `e.stopPropagation()` and run the cell instead. Ported
from `compose/dewmini.js`, which needs the exact same ordering for the
exact same reason.

---

## Where to look for something specific

- **"Why doesn't this setting show up in Settings?"** — look at
  `initMiniIdeSettings()` and the "hide empty sections" loop inside
  `initSettings()`. A settings section with no visible content hides
  itself automatically.
- **"How does a `.ipynb` file become cells?"** — `parseIpynb()` and
  `renderIpynbOutputs()`.
- **"How does dragging actually work?"** — `setupDragAndDrop()`; the
  inline comment above it walks through the four HTML5 Drag and Drop
  events involved. Ported from `compose/dewmini.js`'s own id-based
  approach (rather than the DOM-child-index approach this file used
  before `renderCells()` started interleaving insert dividers between
  cells — see the next entry).
- **"How does inserting a cell between two others work?"** —
  `insertCellAt()` is what both the toolbar's "Python Cell"/"Text Cell"
  buttons and the seams between cells call, at `cells.length` for the
  former and any other index for the latter; `createInsertDivider()`
  builds one seam, and `renderCells()` puts one before the first cell,
  between every pair, and after the last. All three ported from
  `compose/dewmini.js`.
- **"What actually gets saved, and when?"** — `saveState()` for the
  what, and the "Event Listeners" section's shared comment for the
  when (short version: every time `cells` changes). Settings' own
  extras — notes, the editor-appearance section, the download file
  name — each save themselves independently, on their own input events,
  via `initMiniIdeNotes()`, `initMiniIdeEditorSettings()`, and
  `initFilename()`.
- **"Where's the Help panel wired up?"** — `initHelp()` and
  `closeHelpPanel()`, right after `initSettings()` since the two panels
  close each other on open. This replaced `mini-ide-helper`, the old
  banner that showed once and was gone for good the moment a reader had
  any cells — the same reopenable "?" panel `compose/dewmini.js` uses
  instead.
