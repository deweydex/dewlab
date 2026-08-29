# `assets/tutorial-runtime.js`, explained

This is the biggest single file in dewlab's frontend, and it's the one
loaded on every tutorial page. It's what turns build.py's static HTML
into an actually-working page: the settings panel, the cheat sheet, the
series navigation, saving a student's work, version switching, and
booting and running Python. If you've read
[`docs/mini-ide-js-explained.md`](mini-ide-js-explained.md) or
[`docs/mini-ide-engine-explained.md`](mini-ide-engine-explained.md), a
good chunk of this file will look familiar — Mini IDE's own engine file
was ported from this one's Pyodide-handling code, and both files solve
the same "worker vs. main thread" problem the same way.

---

## The big idea: one file, several independent jobs

Unlike Mini IDE (which splits cell management, the Python engine, and the
filesystem into three separate files), this file does all of its jobs in
one place. That's a deliberate difference, not an oversight — a tutorial
page is simpler than Mini IDE in scope (no file manager, no SQL, no
uploads), so splitting it further would add file-hopping without buying
much. Instead, this file is organized into clearly labeled sections (look
for the `/* ---- section name ---- */` comments), and each section is
close to self-contained:

- **Settings, cheat sheet, and series navigation** — three panels that
  open and close, coordinated so only one is ever open at once.
- **Texture** — the reader's theme/font/size preferences, shared across
  every dewlab page via `localStorage`.
- **Cells** — building each cell's editor and wiring up its buttons.
- **Custom cells** — a reader's own cells, created at runtime rather than
  authored in the tutorial's Markdown, kept deliberately separate from
  everything above.
- **Pyodide** — booting Python and running a cell's code, with the same
  worker/main-thread split Mini IDE's engine file uses.
- **Illustrative code and maths** — syntax highlighting for read-only code
  blocks, and KaTeX for rendered maths.
- **Saved work** — autosaving a student's cells and notes, and restoring
  them.
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
   `mini-ide-engine.js`; if a function here (`bootWorker`, `docForMT`,
   `workerRequest`, etc.) moves too fast, that file's own explanation
   goes into more detail on the identical pattern.
3. **Start**, at the very bottom — this is genuinely where execution
   begins. Everything above it is function definitions; nothing happens
   on the page until this section runs, top to bottom, in the order
   written.

---

## Custom cells: a second, deliberately separate cell system

`planning/PRACTICE.md` §3 asks for a way a reader can add their own
Python cell to a page — not one the tutorial's author wrote, one the
reader typed themselves, for trying something out or writing a practice
problem of their own. The whole "custom cells" section (roughly
`CUSTOM_CELLS_PREFIX` through `initCustomCellsSection()`) exists to do
that, and its central design choice is worth stating plainly: **a custom
cell is never added to `cells`, and never touches `saveNow()`,
`restoreSaved()`, or the progress summary.** It gets its own array
(`customCells`), its own `localStorage` key
(`dewlab:custom-cells:<module>:<slug>`), and its own save/restore
functions (`loadCustomCells()`/`saveCustomCells()`/
`scheduleCustomSave()`) that mirror the real ones in shape but never call
them or get called by them.

That separation isn't laziness — it's the simplest way to guarantee two
things `PRACTICE.md` explicitly requires: a custom cell can't collide
with a real cell's id (its id always starts with `custom-`, which no
tutorial author would ever write), and a custom cell survives a tutorial
version change completely untouched (it was never part of the versioned
record to begin with, so there's nothing for a version-mismatch check to
even notice). The one thing custom cells *do* share with real cells is
the shared `runCell()` function: a custom cell object has the exact same
shape a real cell does (`{id, editor, outputEl, runBtn, getCode,
element}`), so `runCell()` runs one without any special-casing —
`mountCustomCell()`'s own comment points this out.

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
(clicking "+ Add a cell" ten minutes into a session). That's what the
small `pyodideReady` flag near the top of the Pyodide section is for —
`createCustomCellElement()` reads it to decide whether a brand-new
cell's Run button should start enabled or not, rather than assuming.

---

## Two patterns worth understanding on their own

**Three panels, one rule.** Settings, the cheat sheet, and the series
navigation panel are three separate, independent UI components — but
opening any one of them always closes the other two. There's no shared
"panel manager" object making that happen; each panel's own `setOpen(true)`
just calls the other two panels' close functions directly. It's a small
enough amount of coordination that three plain function calls handles it
without needing anything more structured.

**Live-then-static code intelligence, worker-or-main-thread.** Hover docs
and autocomplete work by trying two different techniques and taking
whichever answers first: a *live* lookup (asking Python's own `inspect`
module about an object that has actually run) and a *static* one (asking
the Jedi library to guess from the source text alone, for code that
hasn't run yet). This combination happens on whichever thread Python is
actually running on — inside the Worker for the hosted site, or right
here on the main thread for the offline export — which is why there are
two near-identical implementations of the same lookup functions
(`docFor`-style vs. `docForMT`-style) rather than one.

---

## Where to look for something specific

- **"Why does the offline download work differently from the hosted
  site?"** — `manifest.standalone`, checked throughout the Pyodide
  section. A `file://`-opened page can't reliably create a module Worker,
  so the standalone export always uses the main-thread path — see the
  module's own top comment and `DECISIONS_LOG.md` 7.77 for the full
  reasoning.
- **"How does a reader's saved work survive a tutorial being updated?"**
  — the Versions section, especially `carryOver()`/`describeCarry()`:
  saved work is keyed by tutorial, not by release, and restoring matches
  cells by id, so an answer just... still applies, as long as the cell it
  belongs to still exists in the release being switched to.
- **"Why is there a `dl-nudge` class on the notes-export button?"** —
  `updateNotesNudge()`/`markNotesExported()`: a small, deliberately rough
  heuristic (has enough new text piled up since the last export?) rather
  than anything precise.
- **"What's actually exposed to the browser console / end-to-end tests?"**
  — the `globalThis.dewlab = {...}` object at the very end of the file.
- **"Why doesn't a shared custom cell run itself when I load it?"** —
  `importCustomCell()`'s own comment: a loaded cell is deliberately never
  auto-run, so the Settings trust note (`assets/shell.html`,
  `#dl-settings-custom-cells`) is read before anything from someone
  else's file actually executes, not after.
