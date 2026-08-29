# Mini IDE Redesign — Plan

> Working plan for the Mini IDE overhaul (file uploads, file manager, SQLite,
> three-pane-ish layout, Jupyter/.py import, an expanded settings panel).
> Kept here rather than in `docs/MINI_IDE.md` because that file documents
> current, shipped behavior for students; this one tracks in-progress design
> decisions and phase status for whoever (human or Claude) picks the work up
> next. Fold the relevant parts into `docs/MINI_IDE.md` as each phase ships
> (see Phase 8 below).

## Context

Mini IDE (`assets/mini-ide.html`/`.js`/`.css` in the dewlab repo) is a
browser-based Python notebook built on Pyodide. The goal is to push it
toward parity with the basics of Jupyter, with dewlab's own design
language, plus several genuinely new capabilities: file uploads, an
in-browser file manager, SQL/SQLite support, a richer pane layout (file
tree | editor/cells), and Jupyter `.ipynb`/`.py` import — under the
assumption that a student downloads Mini IDE once and works locally after
Python starts up. This is explicitly a step up from **dewmini**
(`compose/dewmini.html`/`.js`), a deliberately smaller/quieter sibling
notebook that stays as-is; new features are scoped to Mini IDE only. The
settings panel also needs to be meaningfully expanded to cover the new
subsystems.

Research (three parallel codebase surveys + one design pass, plus two live
checks against current Pyodide docs) surfaced two things that reshape the
plan:

1. **Mini IDE's execution engine is already behind the rest of the
   codebase.** It runs Pyodide on the main thread with no Stop button, and
   its "Jedi autocomplete" is a hardcoded stub — while `assets/pyodide-worker.js`
   (built for the tutorial pages) already solves all of this: real Worker
   execution, real Jedi, a genuine Stop button, streaming output, and the
   *real* `tutorial_tools.py` instead of Mini IDE's weaker inlined
   duplicate. **Decision: adopt this as the foundation before layering new
   features on top**, since SQL queries and file operations would otherwise
   freeze the tab.
2. **"Download mini-ide.html and it just works offline" isn't true today**
   — the file pulls in several sibling assets and loads Pyodide from a CDN
   at runtime. **Decision: embrace this explicitly** — ship Mini IDE as a
   folder (distribution/build output, not a source-tree restructure), and
   use the File System Access API (`pyodide.mountNativeFS`) to give it a
   real local working directory once granted — with an OPFS/IDBFS fallback
   for browsers that don't support it (Firefox/Safari), so the same file
   manager UI works everywhere, just backed by browser-private storage
   instead of a visible folder.

Two additional open questions were resolved directly with the project
owner:

- **SQL helper placement**: `run_query()` goes into the shared
  `assets/tutorial_tools.py` (reusable by future tutorial content, reuses
  existing table-rendering internals for free) rather than a
  Mini-IDE-exclusive shim.
- **Output layout**: cell output stays **inline per-cell** (two-pane
  layout: file tree | editor+cells), not a third dedicated
  console/terminal pane — this matches actual Jupyter notebook behavior
  more closely than a shared REPL-style output strip.

---

## Phase 1 — Engine migration (foundation; everything else depends on this)

Replace Mini IDE's main-thread Pyodide implementation with the
Worker-based one that already exists and is proven on tutorial pages.

- **Reuse `assets/pyodide-worker.js` unmodified** (generic `{type,id,...}`
  protocol, already page-agnostic — only additive change later is adding
  `'sqlite3'` to its `packages` list, Phase 4).
- **New file `assets/mini-ide-engine.js`** — Mini IDE's own thin
  worker-client, ported from `tutorial-runtime.js`'s worker-communication
  block (`workerRequest`, `ensureWorker`/`bootWorker`, `runCellWorker`,
  `hoverDoc`/`signatureHelp`, interrupt/Stop handling, `applyOutputEvent`,
  and the `bootMainThread`/`runCellMainThread` fallback —
  `tutorial-runtime.js:705-978`). This follows the codebase's existing
  convention of not sharing JS modules between pages (mini-ide.js already
  duplicates rather than imports tutorial-runtime.js's texture code).
- In `mini-ide.js`: delete `ensurePyodide()` (`959-1005`),
  `loadTutorialTools()` (`1013-1025`), `getTutorialToolsCode()`
  (`1450-1452`), `updateSharedNamespace()` (`1033-1047`), and the three
  autocomplete stubs `getJediCompletions()`/`getJediDoc()`/`getDocForName()`
  (`1360-1438`). Replace with calls into `mini-ide-engine.js`.
- `toolsSourceUrl` now points at the **real** `assets/tutorial_tools.py`
  (absolute URL, matching `tutorial-runtime.js:841`) — this alone upgrades
  output fidelity (real matplotlib figure capture, DataFrame tables, error
  tracebacks, widgets) with no new Python code.
- `runCell()`/`runAllCells()` (`855-946`) route through
  `tools.run_cell(cellId, emit, code)` via the worker; adopt
  `applyOutputEvent()` (streaming output) in place of the current batch
  `innerHTML` render.
- Wire real autocomplete/hover (`hover-doc`, `signature-help`,
  `page-names` worker messages) into `createCodeEditor()`'s options in
  place of the deleted stubs.
- Add COI service-worker registration to `mini-ide.html` (site already
  ships `coi-serviceworker.js` via `build.py:2748-2750`; Mini IDE just
  never registers it) — required for the Stop button's `SharedArrayBuffer`
  interrupt path.
- Keep the `file://` / non-worker fallback (`bootMainThread` port) for
  when a module Worker isn't available.

**This phase is independently shippable** — real autocomplete, a working
Stop button, and correct `tutorial_tools.py` behavior land even before any
new feature work starts.

## Phase 2 — Filesystem layer

New file `assets/mini-ide-fs.js`: one small interface (`init()`,
`listDir()`, `readFile()`, `writeFile()`, `deleteFile()`, `sync()`,
`backend`) sitting between the mount and every feature that touches files
(file manager, uploads, SQLite, notebook import) — none of those should
know which backend is active.

- **Tier 1 (Chromium):** `window.showDirectoryPicker()` →
  `pyodide.mountNativeFS()`. The returned `FileSystemDirectoryHandle` is
  stored in IndexedDB (handles aren't localStorage-serializable) for
  reconnect on later visits; permission re-grant needs an explicit
  "Reconnect folder" action since silent re-grant isn't guaranteed by the
  browser.
- **Tier 2 (fallback, all modern browsers):** OPFS via
  `navigator.storage.getDirectory()` — persistent, no picker step, not
  visible in the OS file browser.
- **Tier 3 (belt-and-braces):** IDBFS (`pyodide.FS.mount(pyodide.FS.filesystems.IDBFS, {}, mountDir)`).
- Single mount point regardless of backend: `/mnt/mini-ide` (parallel to
  Pyodide's own `/home/pyodide` convention).
- Debounced sync (~1-2s after last FS-touching op, matching the codebase's
  existing autosave-delay idiom) plus a flush attempt on
  `beforeunload`/`visibilitychange`.
- Before any mount is granted, cell persistence stays on today's
  `localStorage["mini-ide:cells:v1"]` path — the filesystem layer is
  additive, not a hard requirement to keep using Mini IDE.

## Phase 3 — Pane layout + file manager UI

- New CSS Grid workspace in `mini-ide-style.css`, replacing the current
  single-column `.mini-ide-cells` flex stack: `file tree | editor+cells`.
  **Two panes, not three** — output stays inline per-cell (confirmed
  decision above). Reuse existing `--dl-cell-bg`/`--dl-cell-border`/etc.
  tokens; `.dl-tree-layout` (`tutorial-style.css:1301-1310`) is the
  closest existing grid precedent for proportions/spacing, though a true
  multi-pane layout is new CSS work either way.
- File tree lists everything in the mounted root: uploaded data files,
  `.db` files, imported/exported notebooks, and the current notebook's own
  file (once a mount exists, the notebook can live as a real file there
  instead of purely in localStorage). Cells stay the primary editing
  surface in the main pane; double-clicking a data/db file in the tree
  opens a lightweight preview rather than replacing the notebook view.
- Responsive collapse follows the site's existing phone-breakpoint
  convention exactly (`tutorial-style.css:1250-1285`, panels become bottom
  sheets under `max-width: 34rem`) rather than inventing a new mobile
  pattern.

## Phase 4 — SQLite/SQL support

- Add `'sqlite3'` to the worker boot's `packages` array — **always-on**
  rather than a settings toggle, since it's small relative to
  numpy/pandas/matplotlib and avoids a confusing "why doesn't
  `import sqlite3` work" gap.
- Once Phase 2's mount exists, a cell just does
  `import sqlite3; conn = sqlite3.connect('/mnt/mini-ide/students.db')` —
  no special plumbing. Without a mount (localStorage-only mode), sqlite3
  still works against Pyodide's in-memory FS, it just doesn't survive
  reload — surface that distinction in the storage-status settings section
  and the welcome helper text.
- Add a thin `run_query(conn_or_path, sql, params=None)` helper **in
  `assets/tutorial_tools.py`** (confirmed placement — see Context above)
  that renders results via the same table renderer `show_table` already
  uses.

## Phase 5 — Upload + Jupyter/.py import

- **Upload:** drag-and-drop onto the file-tree pane, plus a toolbar button
  opening `<input type="file" multiple>` as the no-drag fallback. Each
  file is written through `mini-ide-fs.js`'s `writeFile()` into the mount;
  tree re-renders, sync is scheduled. Mostly "wire Phase 2/3 together,"
  not new design.
- **`.ipynb` import:** port `handleImportFile()` from
  `compose/dewmini.js:791-816` (already working there — `cell_type:
  code→python`/else→text, `source` array joined) into Mini IDE's cell
  shape. Extend it to handle rich outputs best-effort: `image/png` →
  `<img src="data:...">`, `text/html`/`text/plain` output → rendered
  directly into `cell.output` (which is already rendered as `innerHTML`
  today) — skip anything else (widgets, other MIME types) rather than
  building a full nbformat renderer.
- **`.py` import:** split on `# %%` cell markers (the
  Jupytext/VS Code/Spyder convention); if none are found, import the whole
  file as one cell. Note: `downloadAsPython()`'s current export separator
  (`\n\n# ---\n\n`, `mini-ide.js:1059-1075`) won't round-trip through this
  splitter — switch the export separator to `# %%` too for round-trip
  symmetry (small fix, bundle with this phase).

## Phase 6 — Settings panel expansion

(threaded through Phases 1-5, not a single block at the end)

Follow the existing `dl-settings-section` / `dl-seg` /
load→apply→sync→commit pattern (`mini-ide.js:202-361`, and
`compose/dewmini.js:1018-1081`'s `initEditorSettings()` as the closest
working precedent for a non-texture section) and the "hide the section if
it has nothing to show" rule already enforced generically at
`mini-ide.js:252-257`.

New sections, added as their underlying feature lands:

- **`#dl-settings-execution`** — engine status (worker vs. main-thread
  fallback, Stop-button availability), a "restart Python" action.
- **`#dl-settings-storage`** — active backend (native folder / private
  browser storage), choose/reconnect-folder button, clear-stored-data
  action. Always has something to show, so it's never hidden.
- **`#dl-settings-import`** — replace-vs-append behavior for
  `.ipynb`/`.py` import.
- Fix the currently dead `settings-export-python/html/ipynb` buttons
  (`mini-ide.html:158-160` — confirmed unwired to any listener) by binding
  them exactly like the toolbar's own download buttons already are
  (`mini-ide.js:565-567`).

## Phase 7 — Distribution: vendored Pyodide + folder-based shipping

Sequenced **last**, since it's a packaging concern orthogonal to
correctness — building it before Phases 1-6 are proven against the
CDN-loaded path means re-testing packaging repeatedly.

- New vendor step (no existing precedent — `vendor-src/build-vendor.mjs`
  only bundles JS libraries like CodeMirror today, nothing Pyodide-shaped)
  that fetches the pinned Pyodide release's `full/` distribution into
  `assets/vendor/pyodide/`.
- `build.py` change to bundle `mini-ide.html` + its assets + vendored
  Pyodide + `tutorial_tools.py` into one downloadable folder/zip,
  replacing the current three-loose-files copy (`build.py:2728-2733`).
  This is the "own folder" distribution artifact — it does not require
  restructuring `assets/` in the source tree.
- This is what makes "download once, work locally" actually true — today
  it silently depends on a live CDN fetch.

## Phase 8 — Docs cleanup

`docs/MINI_IDE.md` has confirmed mismatches with current behavior
(real-Jedi claims, ".py export keeps text cells as comments" — it
doesn't, ".html export works offline" — it's an explicit stub). Correct
these as each phase lands the real behavior, then do one full doc pass at
the end rather than patching incrementally, since the gap is already
large enough that partial patches risk leaving new mismatches of the same
kind.

---

## Verification

- Phase 1: open Mini IDE, confirm Stop interrupts a running
  `while True: pass` cell (requires COI service worker registered — check
  `crossOriginIsolated` in devtools console); confirm autocomplete
  suggests real names from `numpy`/a defined variable, not the old fixed
  7-item list; confirm a `matplotlib` figure renders in cell output
  (impossible today with the stub `tutorial_tools`).
- Phase 2: grant a folder, write a file from a cell, reload the page,
  confirm the file is still there (Chromium) and confirm Firefox/Safari
  falls back gracefully to OPFS with the same UX.
- Phase 3: resize to a phone-width viewport, confirm the file tree
  collapses to a bottom sheet like the existing settings/nav panels.
- Phase 4: `import sqlite3`, create and query a `.db` file in the mounted
  folder, reload, confirm the `.db` file persisted and is openable again.
- Phase 5: import a real `.ipynb` exported from Jupyter/Colab (with at
  least one image output) and a `.py` file with `# %%` markers; confirm
  cells and (best-effort) rich output land correctly.
- Phase 6: open Settings, confirm each new section appears only when
  relevant and the three previously-dead export buttons now trigger
  downloads.
- Phase 7: download the built folder fresh, disconnect network, open
  `mini-ide.html` from disk, confirm Python still boots.

## Status

- [x] Phase 1 — Engine migration (assets/mini-ide-engine.js, commit 22c474a)
- [x] Phase 2 — Filesystem layer (assets/mini-ide-fs.js, commit 1415227)
- [x] Phase 3 — Pane layout + file manager UI (commit 3cb899b; also fixed two pre-existing bugs: a circular-JSON crash in saveState() and a double-init listener bug)
- [x] Phase 4 — SQLite/SQL support (run_query() in tutorial_tools.py, commit cb7f504)
- [ ] Phase 5 — Upload + Jupyter/.py import
- [ ] Phase 6 — Settings panel expansion
- [ ] Phase 7 — Vendored Pyodide + folder-based distribution
- [ ] Phase 8 — Docs cleanup
