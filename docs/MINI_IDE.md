# Mini IDE

The Mini IDE is a browser-based Python environment for dewlab that goes a
step beyond the basic notebook experience: cells and text documentation
like before, plus a file manager, file upload, SQLite, and Jupyter
(`.ipynb`)/`.py` import, backed by a real Worker-based Python engine with a
genuine Stop button. For something smaller and quieter, see
[dewmini](../compose/dewmini.html) — Mini IDE is deliberately the more
capable of the two.

This document was rewritten alongside the redesign tracked in
[`planning/MINI_IDE_REDESIGN.md`](../planning/MINI_IDE_REDESIGN.md); that
file has the phase-by-phase design rationale, this one is the reader-facing
reference.

---

## Overview

The Mini IDE provides:

- **Cell-based interface**: create and manage Python and Text cells, sharing
  one persistent Python interpreter (like Jupyter)
- **Real Worker execution**: cells run off the main thread, with a genuine
  Stop button, wherever the browser allows it — falling back to the main
  thread otherwise (see [Execution Engine](#execution-engine))
- **A file manager**: a file tree pane backed by a real mounted filesystem —
  a folder on your computer if you grant one, private browser storage
  otherwise (see [Files and Storage](#files-and-storage))
- **File upload and SQLite**: drop files into the file tree, or query a
  `.db` file with `run_query()`
- **Jupyter/.py import**: load a `.ipynb` or `.py` file as this notebook's
  cells
- **Autocomplete and hover docs**: real Jedi-backed completion and
  documentation, live-namespace-first
- **Persistence**: cells save to `localStorage`; files live in the mounted
  filesystem
- **Full `tutorial_tools.py` API**: everything the tutorials use, plus
  `run_query` for SQL
- **Download options**: export as `.py`, `.html`, or `.ipynb`, or download
  the whole Mini IDE as an offline-capable folder

---

## Quick Start

### Opening the Mini IDE

1. From the dewlab contents page, click the **Mini IDE** link in the introduction
2. Or navigate directly to `mini-ide.html`
3. The Mini IDE opens in a new tab

### Creating Your First Cell

1. Click **"Python Cell"** to add a code cell
2. Type some Python code, for example:
   ```python
   print("Hello, World!")
   x = 42
   x * 2
   ```
3. Click **Run** to execute the cell — the first Run of a session also
   starts Python, which takes a moment
4. The output appears below the cell, as it's produced

### Stopping a Cell

While a cell is running, its Run button becomes a **Stop** button. Clicking
it sends a real interrupt — available whenever the browser has granted
cross-origin isolation (it usually has; see
[Execution Engine](#execution-engine) if Stop isn't doing anything).

### Adding Documentation

1. Click **"Text Cell"** to add a text cell
2. Type documentation, comments, or explanations
3. Text cells are rendered as formatted text; they don't execute

### Running All Cells

Click **"Run All"** to execute all Python cells in order. Cells share a
single Python interpreter, so a name defined in one cell is already
available to a later one without anything special.

### Reordering Cells

Drag a cell by its header and drop it in a new position. The cells run in
the new order the next time you Run All.

### Using Files

Click **"Files"** (or just look at the pane beside your cells on a wide
enough screen) to open the file tree. Upload with the **+** button or by
dragging files onto the pane; delete a file with the × next to it. See
[Files and Storage](#files-and-storage) for what backs this and how to use
a real folder on your computer instead of the browser's own storage.

### Importing a Notebook

Click **"Import"** to load a `.ipynb` or `.py` file as this notebook's
cells — see [Import](#import-ipynb--py).

### Downloading Your Work

- **Download .py**: exports the Python cells as one file, separated by
  `# %%` markers (text cells are not included — see
  [Download Formats](#download-formats))
- **Download .html**: a static snapshot of your cells and their last output
  — not a runnable page (see [Download Formats](#download-formats))
- **Download .ipynb**: exports as a Jupyter Notebook

All downloads save directly; nothing opens in a new tab.

---

## User Interface

### Toolbar

| Button | Description |
|--------|-------------|
| Files | Show/hide the file tree pane (only does something on a narrow screen — it's always visible otherwise) |
| Python Cell | Add a new Python code cell |
| Text Cell | Add a new text/markdown cell |
| Run All | Execute all cells in order |
| Clear All | Remove all cells (with confirmation) |
| Import | Load a `.ipynb` or `.py` file as this notebook's cells |
| Download .py | Export as a Python file |
| Download .html | Export a static snapshot as HTML |
| Download .ipynb | Export as a Jupyter Notebook |

### Cell Types

#### Python Cells

- Executable Python code, syntax-highlighted via CodeMirror
- Autocomplete from the live shared namespace, with a Jedi-backed fallback
  before a cell has ever run
- Hover documentation for user-defined names, builtins, and imported module
  members — live namespace first, Jedi second
- Signature help while typing a call's arguments
- Run button becomes Stop while the cell is running

#### Text Cells

- Plain text documentation — comments, explanations, section headers
- No execution, just display

### Cell Header

Each cell has a header containing:
- **Cell type indicator**: "Python" or "Text"
- **Run/Stop button** (Python cells only)
- **Delete button**

The header is also the drag handle for reordering.

### Output Area

- Streams as the cell produces it, rather than appearing all at once when
  the cell finishes
- Printed output
- The value of the last expression
- DataFrames rendered as tables (including `run_query()` results)
- Matplotlib figures
- Formatted error tracebacks

### File Tree Pane

Beside the cells on a wide enough screen (a bottom sheet on a phone, opened
with the toolbar's **Files** button):

- Lists everything in the mounted filesystem's root — uploaded files,
  `.db` files, anything a cell wrote
- **+** uploads one or more files; dragging files onto the pane does the
  same
- **⟳** refreshes the list
- **×** next to an entry deletes it (with confirmation)
- Before Python has started, it shows a note saying so rather than an
  empty list — run any cell to start it

---

## Files and Storage

Uploads, SQLite `.db` files, and anything a cell writes with plain
`open()` live in a filesystem mounted at `/mnt/mini-ide` inside Python.
What actually backs that mount depends on what your browser supports and
whether you've opted into a real folder:

1. **A real folder on your computer** (Chrome/Edge, via the File System
   Access API) — opt in from Settings → Files → **Use a folder on my
   computer**. Files are real files, visible in your own file browser.
   Needs a one-time permission grant; on a later visit, Settings offers
   **Reconnect my folder** instead if the browser needs to re-confirm
   access.
2. **This browser's private storage (OPFS)** — what a fresh session mounts
   automatically if a real folder hasn't been chosen (or your browser
   doesn't support the picker). Fast and persistent, but not visible
   outside the browser, and specific to this one browser profile on this
   one device.
3. **This browser's private storage (compatibility mode / IndexedDB)** —
   the fallback if even OPFS isn't available.

Settings → **Files** shows which one is active and lets you switch. Nothing
is mounted, and the file tree stays empty, until Python has started (run
any cell).

---

## SQL / SQLite

`sqlite3` is part of Python's standard library and loads automatically —
`import sqlite3` just works, no setup needed.

For a quick query with a rendered result, `tutorial_tools` (already
available in every cell) provides:

```python
run_query(conn_or_path, sql, params=None, max_rows=20, caption=None)
```

`conn_or_path` is either an already-open `sqlite3.Connection`, or a path —
typically a file in the mounted filesystem — that gets opened and closed
around this one query:

```python
run_query("students.db", "create table grades (name text, score integer)")
run_query("students.db", "insert into grades values (?, ?)", ("Ana", 92))
run_query("students.db", "select * from grades where score > ?", (80,))
```

Every query commits, including a `CREATE TABLE`/`INSERT`/`UPDATE` — the
friendlier default for someone who doesn't yet know sqlite3 needs an
explicit `commit()`. The result always comes back as a DataFrame, whether
or not it also rendered a table (a statement with nothing to fetch renders
nothing). Without a mounted folder or OPFS (i.e. before Python has started,
or in a browser with neither), `sqlite3.connect()` still works against an
in-memory filesystem — it just doesn't survive a reload.

---

## Import (.ipynb / .py)

The toolbar's **Import** button loads a `.ipynb` or `.py` file, replacing
or appending to the current notebook's cells depending on Settings →
**Import** → *On import: replace/append*.

- **`.ipynb`**: each notebook cell becomes a Python or Text cell. A code
  cell's outputs are carried over best-effort — an image renders, an HTML
  output (e.g. a DataFrame's own table) renders as-is, plain text/stream
  output renders in a `<pre>`. Anything else (widgets, other MIME types) is
  skipped rather than attempting a full notebook renderer.
- **`.py`**: splits on `# %%` markers (the same convention Jupytext, VS
  Code, and Spyder use) — each section becomes its own cell. A file with no
  markers imports as a single cell. `Download .py` exports with the same
  `# %%` separator, so a downloaded file round-trips back through Import
  into the same cells it came from.

---

## Available Functions

The Mini IDE provides the same API as dewlab tutorials through the
`tutorial_tools.py` module:

### Display Functions

| Function | Description |
|----------|-------------|
| `show(*values, label=None)` | Render values mid-cell |
| `show_table(frame, max_rows=20, caption=None)` | Render a DataFrame as a table |

### SQL

| Function | Description |
|----------|-------------|
| `run_query(conn_or_path, sql, params=None, max_rows=20, caption=None)` | Run a query, render the results, and return them as a DataFrame |

### Verification

| Function | Description |
|----------|-------------|
| `check(actual, expected, tolerance=None, label=None)` | Verify an answer with instant feedback |

### Input Widgets

| Function | Description |
|----------|-------------|
| `text_input(label, value="", id=None)` | Create a text input box |
| `dropdown(label, options, value=None, id=None)` | Create a dropdown selector |
| `button(label, on_click)` | Create a clickable button |

### Data Loading

| Function | Description |
|----------|-------------|
| `await load_csv(name)` | Load a CSV from dewlab's shared data folder (a different thing than a file you've uploaded — see [Files and Storage](#files-and-storage) for your own files) |

### Example Usage

```python
# Display functions
show("The answer is:", 42)
show_table(my_dataframe, caption="My Data")

# SQL
run_query("students.db", "create table grades (name text, score integer)")
run_query("students.db", "select * from grades")

# Verification
check(my_answer, 100, label="Correct!")

# Widgets
temp = text_input("Enter temperature")
unit = dropdown("Unit", ["Celsius", "Fahrenheit"])

# Data loading
data = await load_csv("my-data.csv")
```

---

## Autocomplete and Documentation

### Live Autocomplete

Suggests names from the shared namespace — everything a cell could
actually reference right now, from an earlier cell or this session's own
setup.

### Hover Documentation and Signature Help

Hover a name, or start typing a call's arguments, to see documentation —
the live namespace answers first (so a name you just defined shows its own
docstring), Jedi fills in anything live lookup can't reach (standard
library functions, module members, names before the cell defining them has
run).

Jedi loads in the background right after Python starts, without blocking
the first Run click — hover/signature help for anything Jedi alone can
answer is briefly unavailable until it finishes.

---

## Execution Engine

Mini IDE runs Python in a Web Worker whenever the browser allows it — the
page stays responsive during a long-running cell, and Stop can genuinely
interrupt one via a `SharedArrayBuffer` (this needs cross-origin isolation,
which a small service worker registers automatically; the very first visit
to any dewlab page may reload once to pick it up).

If a Worker isn't available (for instance, a `file://`-opened copy in a
browser that restricts module Workers there), Mini IDE falls back to
running Python on the main thread instead — everything still works, Stop
just can't interrupt a running cell in that mode.

Settings → **Python** shows which mode is active, and offers **Restart
Python** — tears down the current interpreter and starts a fresh one, for
recovering from a corrupted namespace or a runaway loop Stop couldn't
reach. The mounted filesystem re-mounts automatically after a restart.

---

## Persistence

### Automatic Saving

- All cells are automatically saved to `localStorage` on every change
  (content edit, cell add/remove, reorder, run)
- No manual save required for cells

### What is Saved

- Cell type (Python or Text)
- Cell content
- Cell order and ID
- The last run's rendered output (so it's still there after a reload,
  without re-running anything)
- Whether a cell's last run raised an error

### What is NOT Saved

- Live Python state — the interpreter itself restarts each session; a
  reloaded cell's saved output is a snapshot, not something you can keep
  computing from without re-running
- Widget values (reset on reload)

### Files

Uploaded files, `.db` files, and anything a cell writes persist in
whichever backend is mounted (see [Files and Storage](#files-and-storage))
— independent of cell `localStorage` persistence, and not affected by
Clear All.

### LocalStorage Keys

| Key | Purpose |
|-----|---------|
| `mini-ide:cells:v1` | All cell data |
| `mini-ide:helper-visible` | Whether the welcome helper text is shown |
| `mini-ide:import-mode` | Whether Import replaces or appends cells |
| `dewlab:texture` | Theme/font/size preferences (shared with tutorial pages) |

A chosen real folder's permission handle is stored separately, in
IndexedDB (`mini-ide-fs`) — not `localStorage`, since a `FileSystemDirectoryHandle`
isn't a string.

---

## Download Formats

### Python File (.py)

```python
print("first cell")

# %%

print("second cell")
```

**Behavior:**
- Only Python cells are included — text cells are not exported to `.py`
- Cells are separated by `# %%` (the Jupytext/VS Code/Spyder convention),
  matching what Import's `.py` splitter expects, so a round trip through
  download-then-import lands back on the same cells

### HTML File (.html)

A static snapshot — each cell's source and its last output, as plain
markup. It is **not** a standalone, runnable page: there's no embedded
Pyodide, and nothing in it executes. Useful for sharing what a notebook
looked like, not for handing someone something they can keep running. (For
a Python runtime a student can actually run, see
[The Downloadable Mini IDE](#the-downloadable-mini-ide) instead.)

### Jupyter Notebook (.ipynb)

A valid Jupyter Notebook JSON file that:
- Can be opened in Jupyter Notebook, JupyterLab, or Google Colab
- Preserves cell types and order (Text cells → Markdown, Python cells → Code)
- Includes standard Jupyter metadata

---

## The Downloadable Mini IDE

Beyond exporting your *work*, the Mini IDE tool itself is downloadable as a
folder (and a matching zip) that runs without a server — save it, open
`mini-ide.html` from disk, and it works the same as the hosted page.

Whether that first run needs an internet connection depends on whether the
copy you downloaded has Pyodide bundled in:

- **With Pyodide bundled**: Python starts from the files right next to
  `mini-ide.html` — no network needed, ever.
- **Without it**: the first run still needs to fetch Python from a CDN,
  same as the hosted page; after that it behaves identically.

This is a build-time choice dewlab's maintainers make (`assets/vendor/pyodide/`,
fetched with `dev/fetch_pyodide.py` — see `planning/MINI_IDE_REDESIGN.md`
Phase 7), not something a student configures.

---

## Technical Details

### Architecture

```
mini-ide.html
  |
  +-- mini-ide.js .......... cell management, UI, settings
  |     |
  |     +-- mini-ide-engine.js ... boots & talks to the Python engine
  |     |     |
  |     |     +-- pyodide-worker.js (Worker) .. Pyodide, Jedi, run_cell
  |     |     +-- (main-thread fallback, same file)
  |     |
  |     +-- mini-ide-fs.js ....... mounts & reads/writes the filesystem
  |     +-- CodeMirror .......... editing, autocomplete UI
  |
  +-- localStorage ........... cell persistence
  +-- mounted filesystem ..... file persistence (folder / OPFS / IndexedDB)
```

`mini-ide-engine.js` is Mini IDE's own client for `pyodide-worker.js` — the
same file the hosted tutorial pages boot through — ported rather than
imported, following this codebase's convention of each page owning a thin
copy of shared logic rather than sharing a runtime module directly.

### Pyodide Configuration

- **Version**: 0.28.3 (matches the tutorial pages)
- **Source**: jsDelivr CDN by default, or a bundled local copy in the
  downloadable folder (see [The Downloadable Mini IDE](#the-downloadable-mini-ide))
- **Packages loaded at boot**: numpy, pandas, matplotlib, sqlite3
- **Loaded separately, in the background**: jedi, parso (for hover/completion)
- **Loading**: lazy — nothing loads until the first cell actually runs

### Shared Namespace

All Python cells share one interpreter, the same as Jupyter:

```python
# Cell 1
x = 10

# Cell 2
y = x * 2  # y = 20, x is available from Cell 1
```

The interpreter itself only resets when the page reloads, or when
**Restart Python** (Settings → Python) is used — not on every Run All.

### Execution Order

Cells are executed in the order they appear in the UI. When you:
- Click **Run** on a cell: only that cell executes (click it again, or
  click Stop, to interrupt it while it's running)
- Click **Run All**: all cells execute in order, top to bottom
- Drag to reorder: the new order is used for the next Run All

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Tab | Indent or accept completion |
| Shift+Tab | Outdent |
| Enter | Accept completion or insert newline |
| Escape | Close completion list or leave cell |
| Ctrl+Z | Undo (in editor) |
| Ctrl+Y | Redo (in editor) |
| Ctrl+A | Select all (in editor) |
| Ctrl+C | Copy (in editor) |
| Ctrl+V | Paste (in editor) |
| Ctrl+X | Cut (in editor) |

---

## Troubleshooting

### Pyodide Not Loading

**Symptom**: The status bar stays on "Starting Python…" or "Loading
numpy, pandas, matplotlib…"

**Causes**:
- No internet connection (unless using a fully offline downloaded copy —
  see [The Downloadable Mini IDE](#the-downloadable-mini-ide))
- CDN blocked by a firewall or proxy
- Browser security restrictions

**Solutions**:
- Check your internet connection
- Try a different browser or network
- Wait a moment — Pyodide plus its packages is a real download
- Try refreshing the page; Settings → Python → **Restart Python** if
  Python started once but seems stuck now

### Stop Doesn't Interrupt a Cell

**Cause**: the browser hasn't granted cross-origin isolation, or Python is
running on the main-thread fallback rather than a Worker — see
[Execution Engine](#execution-engine).

**Solutions**:
- Reload the page once (the isolation service worker sometimes needs a
  reload on the very first visit)
- Check Settings → Python for which engine mode is active
- Restart Python from the same section as a last resort for a stuck cell

### Cells Not Running

**Symptom**: Clicking Run does nothing, or shows an error immediately

**Causes**:
- Python hasn't finished starting yet
- A syntax error in the code
- A browser console error

**Solutions**:
- Wait for the status bar to clear
- Check the browser console (F12) for errors
- Fix syntax errors

### File Features Not Working

**Symptom**: the file tree stays on "Files appear here once Python
starts", or upload shows an error

**Cause**: nothing is mounted until Python has started at least once.

**Solution**: run any cell, then try again.

### Download Not Working

**Symptom**: Clicking a download button does nothing

**Causes**:
- Browser popup or download blocker
- No cells to download (for `.py`, specifically no *Python* cells)

**Solutions**:
- Allow downloads for this site
- Add at least one cell of the right type
- Try a different browser

---

## Browser Support

| Browser | Cells, Run, autocomplete | Real Stop button | Real folder for files |
|---------|:---:|:---:|:---:|
| Chrome / Edge | ✅ | ✅ | ✅ |
| Firefox | ✅ | ✅ | Falls back to private browser storage |
| Safari | ✅ | ✅ | Falls back to private browser storage |
| Mobile Chrome | ✅ | ✅ | ✅ |
| Mobile Safari | ✅ (limited testing) | ✅ | Falls back to private browser storage |

**Requirements:**
- ES6 module support
- WebAssembly support
- `localStorage` support
- Fetch API support

A real folder specifically needs the File System Access API
(`showDirectoryPicker`), which is Chromium-only today — every other
feature, including the file manager itself, works the same way on any
supported browser, just backed by that browser's own private storage
instead.

---

## Limitations

1. **A hosted or CDN-dependent copy needs internet the first time**: only a
   downloaded copy with Pyodide bundled in (see
   [The Downloadable Mini IDE](#the-downloadable-mini-ide)) is truly
   offline-capable from the start
2. **No persistence between devices**: cells and files are saved per
   browser/device (per real folder, if you've chosen one and it happens to
   be cloud-synced by something outside Mini IDE's control — not something
   Mini IDE itself provides)
3. **No collaboration**: cannot share a live session
4. **Widgets are static in the `.html` export**: that export has no
   embedded Python, so nothing in it is interactive
5. **No debugger**: cannot step through code
6. **Memory limits**: ordinary browser memory limits apply to both the
   Python interpreter and the mounted filesystem

---

## Comparison with Other Tools

| Feature | Mini IDE | Jupyter | Colab | VS Code |
|---------|----------|---------|-------|---------|
| Browser-based | ✅ | ❌ | ✅ | ❌ |
| Zero install | ✅ | ❌ | ❌ | ❌ |
| Offline support | ✅ (downloadable, Pyodide bundled) | ❌ | ❌ | ✅ |
| Cell-based | ✅ | ✅ | ✅ | ❌ |
| Autocomplete | ✅ | ✅ | ✅ | ✅ |
| File manager | ✅ | ✅ | ✅ (Drive) | ✅ |
| SQL support | ✅ (`sqlite3` + `run_query`) | via extension | via extension | via extension |
| Persistence | ✅ (`localStorage` + mounted files) | ⚠️ (server) | ✅ (Google Drive) | ✅ (local) |
| Download as .py | ✅ | ❌ | ✅ | ✅ |
| Download as .ipynb | ✅ | ✅ | ✅ | ❌ |
| Import .ipynb / .py | ✅ | ✅ | ✅ | ✅ |
| Shared namespace | ✅ | ✅ | ✅ | ❌ |
| `tutorial_tools.py` API | ✅ | ❌ | ❌ | ❌ |

---

## Future Enhancements

Considered for future versions, not yet built:

- **Code folding**: collapse/expand code blocks
- **Cell output folding**: hide/show output
- **Nested folders in the file tree**: currently a flat, root-only view
- **More keyboard shortcuts**: more IDE-like bindings
- **More themes**: additional color themes beyond the shared texture settings

---

## Contributing

To contribute to the Mini IDE:

1. **Report bugs**: open an issue on GitHub
2. **Suggest features**: open an issue or discussion
3. **Submit code**: open a pull request
4. **Test**: try the Mini IDE and report issues

### Development Setup

```bash
# Clone the repository
git clone https://github.com/deweydex/dewlab
cd dewlab

# Install build dependencies
pip install -r requirements-build.txt

# Build the site
python3 build.py

# For a fully offline downloadable bundle, first fetch Pyodide:
python3 dev/fetch_pyodide.py --out assets/vendor/pyodide \
    --packages numpy pandas matplotlib sqlite3 jedi
python3 build.py

# Start local server
python3 -m http.server -d site 8000

# Open Mini IDE
# http://localhost:8000/mini-ide.html
```

### File Structure

```
assets/
├── mini-ide.html          # Entry point
├── mini-ide.js             # Cell management, UI, settings
├── mini-ide-engine.js      # Worker client: boot, run, hover/signature help
├── mini-ide-fs.js          # Filesystem: backend selection, mount, read/write
├── mini-ide-style.css      # Styling
├── pyodide-worker.js       # Shared with tutorial pages — the Worker itself
├── tutorial_tools.py       # Shared with tutorial pages — the Python-side API
└── vendor/
    ├── codemirror.bundle.js  # CodeMirror (includes autocomplete plumbing)
    ├── coi-serviceworker.js  # Cross-origin isolation, for the Stop button
    └── pyodide/               # Not committed — see Development Setup above
```

### Code Style

The Mini IDE follows the same style guidelines as the rest of dewlab:

- **JavaScript**: ES6+ modules
- **Comments**: explain *why*, not *what* — a well-named function doesn't
  need a comment restating its name
- **Naming**: camelCase for variables and functions
- **Constants**: UPPER_CASE with underscores
- **Error handling**: try/catch with meaningful messages
- **Async**: async/await for clarity

---

## License

The Mini IDE is part of dewlab and is licensed under the same terms.
See [LICENSE.md](../LICENSE.md) for details.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-01-XX | Initial release |
| 2.0 | 2026-08-29 | Worker-based execution engine with a real Stop button and real Jedi; a mounted filesystem (real folder / OPFS / IndexedDB) with a file manager pane; file upload; SQLite via `run_query()`; `.ipynb`/`.py` import; expanded settings (engine status, storage, import behavior); a downloadable, optionally fully-offline Mini IDE folder |
