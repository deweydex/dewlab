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
   up the engine, loads saved cells (or creates sample ones if there
   aren't any), and calls all the `setup*()`/`init*()` functions that
   make the rest of the page interactive.
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

---

## Where to look for something specific

- **"Why doesn't this setting show up in Settings?"** — look at
  `initMiniIdeSettings()` and the "hide empty sections" loop inside
  `initSettings()`. A settings section with no visible content hides
  itself automatically.
- **"How does a `.ipynb` file become cells?"** — `parseIpynb()` and
  `renderIpynbOutputs()`.
- **"How does dragging actually work?"** — `setupDragAndDrop()` and
  `getDragAfterElement()`; the inline comments on both walk through the
  browser APIs involved in detail.
- **"What actually gets saved, and when?"** — `saveState()` for the
  what, and the "Event Listeners" section's shared comment for the
  when (short version: every time `cells` changes).
