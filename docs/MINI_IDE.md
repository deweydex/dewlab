# Mini IDE

The Mini IDE is a Python workspace that runs right in your browser.
Like a dewlab tutorial, you write and run Python in cells, and you can
add notes in text cells. But Mini IDE also gives you a file manager, the
ability to upload your own files, a real SQL database (SQLite), and a
way to load in a Jupyter notebook or a `.py` file. It runs Python in the
background so the page never freezes, and it has a real Stop button
that can actually interrupt code that's stuck.

Want something smaller and quieter instead? Try
[dewmini](../compose/dewmini.html). Mini IDE is built to be the bigger,
more capable of the two.

---

## Overview

Mini IDE gives you:

- **Cells**: write Python code or notes in separate cells. All your
  Python cells share the same running program, the same way Jupyter
  works.
- **Runs in the background**: your code runs separately from the page,
  so the page stays responsive, and Stop can really interrupt it. See
  [Execution Engine](#execution-engine) for when this is and isn't true.
- **A file manager**: a panel that lists real files — a folder on your
  computer if you allow it, or private storage in your browser if not.
  See [Files and Storage](#files-and-storage).
- **File upload and SQLite**: drop files into the file manager, or run a
  SQL query against a `.db` file with `run_query()`.
- **Load a notebook**: bring in a `.ipynb` or `.py` file as this
  notebook's cells.
- **Autocomplete and hover help**: real suggestions and documentation as
  you type.
- **Saves your work**: cells save automatically in your browser; files
  live in whichever storage backs the file manager.
- **Everything the tutorials have**: the same functions dewlab
  tutorials use, plus `run_query` for SQL.
- **Download options**: save your work as `.py`, `.html`, or `.ipynb` —
  or download the whole Mini IDE tool as a folder you can run offline.

---

## Quick Start

### Opening the Mini IDE

1. From the dewlab home page, click the **Mini IDE** link in the intro
2. Or go straight to `mini-ide.html`
3. Mini IDE opens in a new tab

### Creating Your First Cell

1. Click **"Python Cell"** to add a code cell
2. Type some Python code, for example:
   ```python
   print("Hello, World!")
   x = 42
   x * 2
   ```
3. Click **Run** to run the cell. The first time you click Run in a
   session, Python also has to start up, so it takes a moment.
4. The output shows up below the cell as it happens

### Stopping a Cell

While a cell is running, its Run button turns into a **Stop** button.
Clicking it really does interrupt the code — this works in most
browsers (see [Execution Engine](#execution-engine) if Stop doesn't
seem to be doing anything).

### Adding Notes

1. Click **"Text Cell"** to add a text cell
2. Type notes, comments, or explanations — `# a heading`, `**bold**`,
   `*italic*`, `` `code` ``, and `- a bullet list` all format themselves
3. Click away and it turns into formatted text; click it again, or use
   the **Edit**/**View** button in its header, to get the plain words
   back and keep writing
4. Text cells never run any code — they just display

### Running All Cells

Click **"Run All"** to run every Python cell in order, top to bottom.
All your cells share one running program, so something you define in
one cell is already there for a later one to use.

### Reordering Cells

Drag a cell by its header to move it. The new order is used next time
you click Run All.

### Inserting a Cell Between Two Others

Hover the thin seam between any two cells — or before the first, or
after the last — and it grows into "+ Python" / "+ Text" buttons. This
is the fast way to build a notebook: adding exactly where you're
already looking, rather than always appending at the bottom and
dragging it up. On a touch device the seam stays visible without a
hover to reveal it.

### Keeping a Note

Settings has a "Your notes" box — free-text, saved alongside your
cells but not part of them, for anything worth writing down that isn't
code or a text cell of its own (a reminder, a link, a to-do).

### Using Files

Click **"Files"** (or just look at the panel next to your cells if your
screen is wide enough) to open the file manager. Upload with the **+**
button, or by dragging files onto the panel. Delete a file with the ×
next to it. See [Files and Storage](#files-and-storage) for what's
actually storing these files, and how to use a real folder on your
computer instead of your browser's own storage.

### Loading a Notebook

Click **"Import"** to load a `.ipynb` or `.py` file as this notebook's
cells — see [Import](#import-ipynb--py).

### Downloading Your Work

- **Download .py**: saves your Python cells as one file, with `# %%`
  between them (text cells aren't included — see
  [Download Formats](#download-formats))
- **Download .html**: a snapshot of your cells and their last output —
  you can look at it, but it won't run any code (see
  [Download Formats](#download-formats))
- **Download .ipynb**: saves your work as a Jupyter Notebook

All three save the file directly — nothing opens in a new tab. All
three, plus a **Print / Save as PDF** button, also live together in
Settings under "Keep a copy," alongside a file name field — set it once
and it's used for every download and shown in the browser tab, instead
of the generic `mini-ide-notebook` default.

---

## User Interface

### Masthead

The **?** button next to Settings opens a Help panel covering cells,
keyboard shortcuts, Files, the available functions, and how your work is
kept — the same reference, reopenable any time, that
[dewmini](DEWMINI.md) shows next to its own toolbar. Opening either Help
or Settings closes the other, since they share the same corner.

### Toolbar

| Button | What it does |
|--------|-------------|
| Files | Shows or hides the file manager (only matters on a narrow screen — it's always visible otherwise) |
| Python Cell | Adds a new Python code cell |
| Text Cell | Adds a new text cell |
| Load example | Replaces your cells with a short worked example (asks first, unless the notebook is already empty) |
| Run All | Runs every cell in order |
| Clear Output | Clears every cell's output, keeping the cells and their code (no confirmation — nothing is lost) |
| Clear All | Removes all cells (asks first) |

Importing a file and downloading your work live in Settings now, not the
toolbar — see below. A fresh notebook starts genuinely empty; nothing
auto-loads sample cells for you, which is what "Load example" is for.

### Settings Groups

Settings is organized into three collapsible groups so you're not
scrolling past everything at once: **Workspace** (Python status and a
Run time on/off switch, Files status, Import) and **Your work** (notes,
Keep a copy/download) open by default, and **Appearance** (texture,
editor) collapsed until you need it. Opening Settings or Help while your
screen is wide enough for both to fit shrinks the working area rather
than covering it — your cells stay fully visible and usable with a panel
open, the way a desktop code editor's side panels behave.

### Cell Types

#### Python Cells

- Code you can run, with syntax highlighting
- Autocomplete that suggests names you've already used, and falls back
  to general Python knowledge before you've run anything
- Hover over a name to see what it does
- Helpful hints while you're typing a function call
- Run button turns into Stop while the cell is running

#### Text Cells

- Notes, comments, or explanations — `# heading`, `**bold**`,
  `*italic*`, `` `code` ``, and `- a bullet list` all format themselves
- Never run any code, they just display

### Cell Header

Each cell has a small pill-shaped header with:
- **A label**: "Python" or "Text"
- **A Run/Stop button** (▶, Python cells only)
- **A Reset-output button** (↺, Python cells only) — clears just this
  cell's own output, keeping its code, for when you want a clean slate
  on one cell without touching the rest of the notebook
- **An Edit/View button** (text cells only) — switches between the
  plain words and the formatted view
- **A Delete button** (×) — the first click arms it (it turns solid red);
  a second click actually deletes. Click anything else, or wait a few
  seconds, and it quietly disarms itself instead

The buttons are faint until you hover the cell (or, on a touch device,
always visible). The coloured rail beside a cell is quiet by design too
— invisible for an ordinary cell, and only lighting up (orange while
focused, red if its last run errored) when there's actually something
worth flagging at a glance down a long notebook.

### Output Area

- Shows up as the cell runs, not all at once when it finishes
- Anything the code printed
- The value of the last line, if it's an expression
- DataFrames shown as tables (including `run_query()` results)
- Matplotlib plots
- A readable error message if something goes wrong
- How long the run took, in small text under the output — turn this off
  in Settings → Workspace → Python → **Run time**, if you'd rather not
  see it

### File Manager Panel

Next to your cells if your screen is wide enough (a panel that slides
up from the bottom on a phone, opened with the **Files** button):

- Lists everything in your files — uploads, `.db` files, anything a
  cell created
- **+** uploads one or more files; you can also drag files onto the
  panel
- **⟳** refreshes the list
- **×** next to a file deletes it (asks first)
- Before Python has started, it just says so instead of showing an
  empty list — run any cell to get things going

---

## Editor Appearance

Settings has an "Editor" section — code size, how much room a cell
gives itself (compact, cozy, or relaxed), how heavy the cursor looks,
and whether line numbers and the current line's highlight show at all.
None of it changes how code runs, only how it looks; every open cell
picks up a change immediately. The same idea [dewmini](DEWMINI.md) offers
under its own "Editor" section in Settings.

---

## Files and Storage

Uploads, SQLite `.db` files, and anything a cell writes with `open()`
all live in one place inside Python. What that place actually is
depends on your browser, and whether you've chosen a real folder:

1. **A real folder on your computer** (Chrome or Edge only, for now) —
   turn this on in Settings → Files → **Use a folder on my computer**.
   Your files are real files you can see in your own file browser. You
   need to allow access once; on a later visit, Settings offers
   **Reconnect my folder** if your browser needs you to confirm again.
2. **Your browser's own private storage (OPFS)** — what a new session
   uses automatically if you haven't chosen a real folder (or your
   browser doesn't support that). Fast, and it sticks around, but you
   can't see these files outside the browser, and they only exist on
   this one browser, on this one device.
3. **Your browser's own private storage, older style (IndexedDB)** — a
   backup option if even the one above isn't available.

Settings → **Files** shows which one is active, and lets you switch.
Nothing is stored, and the file manager stays empty, until Python has
started — run any cell first.

---

## SQL / SQLite

`sqlite3` is part of Python itself, so it's ready to use right away —
just write `import sqlite3` and go.

For a quick way to run a query and see the result, use `run_query`,
which is already available in every cell:

```python
run_query(conn_or_path, sql, params=None, max_rows=20, caption=None)
```

`conn_or_path` can be a database connection you already opened, or just
a path to a file — usually one in your file manager — which
`run_query` opens and closes for you around that one query:

```python
run_query("students.db", "create table grades (name text, score integer)")
run_query("students.db", "insert into grades values (?, ?)", ("Ana", 92))
run_query("students.db", "select * from grades where score > ?", (80,))
```

Every query saves itself right away, including a `CREATE TABLE`,
`INSERT`, or `UPDATE` — a friendlier default if you don't yet know that
sqlite3 usually needs you to call `commit()` yourself. Whatever comes
back is always a DataFrame, whether or not it also showed you a table
(a query with nothing to show, like a `CREATE TABLE`, just doesn't show
one). If you haven't chosen a folder and your browser doesn't support
OPFS — basically, before Python has started — `sqlite3.connect()` still
works, it just won't remember anything after you reload the page.

---

## Import (.ipynb / .py)

The **Import** button loads a `.ipynb` or `.py` file. Depending on your
choice in Settings → **Import** → *On import: replace/append*, it
either replaces your current cells or adds to them.

- **`.ipynb`**: each cell in the notebook becomes a Python or Text
  cell. Outputs come along too, as best we can manage — an image shows
  up, an HTML output (like a DataFrame's own table) shows up as-is, and
  plain text shows up too. A few kinds of output (interactive widgets,
  some rarer formats) don't come across — Mini IDE isn't trying to be a
  full Jupyter viewer, just to bring your code and its outputs over.
- **`.py`**: splits the file wherever it finds a `# %%` line (the same
  marker Jupytext, VS Code, and Spyder use) — each part becomes its own
  cell. If there are no `# %%` markers, the whole file becomes one
  cell. `Download .py` uses the same `# %%` marker, so a file you
  download can be loaded straight back in as the same cells.

Importing a notebook written outside Mini IDE can bring along things
Pyodide's Python genuinely can't run — a `tkinter` window, a Jupyter
"magic" command like `%matplotlib inline`, a `!pip install` shell line.
A warning banner names exactly which imported cell each one is in,
right after the import, rather than leaving you to work out later why a
cell you didn't even write yourself raised an error.

## Worked examples

Settings → **Import** also offers four ready-made notebooks, real data
included — the same import path as loading your own file, just fetched
from dewlab instead of picked from your device:

| Example | What it covers |
|---|---|
| SQL & Our World in Data | `sqlite3`, `run_query()`, and real national CO₂ emissions data |
| A mini data investigation | pandas, `groupby`, and whether life expectancy has converged worldwide since 1950 |
| A fun math problem | estimating π by throwing random darts — Monte Carlo simulation |
| Word frequency: usual or unusual? | counting words in a real novel and checking it against Zipf's law |

Each is a real, runnable dewlab tutorial in miniature — narration in
text cells, code that actually works in Python cells, and a "your turn"
prompt near the end rather than just something to read.

---

## Available Functions

Mini IDE gives every Python cell the same functions dewlab tutorials
use:

### Display Functions

| Function | What it does |
|----------|-------------|
| `show(*values, label=None)` | Show one or more values partway through a cell |
| `show_table(frame, max_rows=20, caption=None)` | Show a DataFrame as a table |

### SQL

| Function | What it does |
|----------|-------------|
| `run_query(conn_or_path, sql, params=None, max_rows=20, caption=None)` | Run a query, show the results, and return them as a DataFrame |

### Checking Your Work

| Function | What it does |
|----------|-------------|
| `check(actual, expected, tolerance=None, label=None)` | Compares your answer to the right one and tells you right away |

### Input Widgets

| Function | What it does |
|----------|-------------|
| `text_input(label, value="", id=None)` | A text box you can type into |
| `dropdown(label, options, value=None, id=None)` | A menu you can pick from |
| `button(label, on_click)` | A button you can click |
| `image_input(label, id=None)` | A file picker for an image, read with `.value` |

### Loading Data

| Function | What it does |
|----------|-------------|
| `await load_csv(name)` | Loads a CSV from dewlab's shared data folder — not the same as a file you've uploaded yourself; see [Files and Storage](#files-and-storage) for those |

### Example

```python
# Display functions
show("The answer is:", 42)
show_table(my_dataframe, caption="My Data")

# SQL
run_query("students.db", "create table grades (name text, score integer)")
run_query("students.db", "select * from grades")

# Checking your work
check(my_answer, 100, label="Correct!")

# Widgets
temp = text_input("Enter temperature")
unit = dropdown("Unit", ["Celsius", "Fahrenheit"])

# Loading data
data = await load_csv("my-data.csv")
```

---

## Autocomplete and Documentation

### Autocomplete

Suggests names you can actually use right now — anything from an
earlier cell, or from something this session already set up.

### Hover Help and Function Hints

Hover over a name, or start typing the arguments to a function call, to
see what it does. If you just defined it yourself, you'll see your own
notes about it first; otherwise Mini IDE looks it up for you (this
covers things like standard library functions, or names from a cell
that hasn't run yet).

This lookup tool loads in the background right after Python starts, so
it doesn't hold up your first Run click — it just might take it a
second or two to be ready.

---

## Execution Engine

Mini IDE runs Python in the background whenever your browser allows it
— the page stays responsive while a cell is running, and Stop can
really interrupt it. (This uses a browser feature that needs a small
one-time setup step, which happens automatically; the very first time
you visit any dewlab page, it might reload once to finish that setup.)

If your browser doesn't allow running Python in the background — for
example, if you opened a copy of Mini IDE straight from a file on your
computer, in a browser that restricts this — everything still works,
Stop just can't interrupt a cell that's already running.

Settings → **Python** shows which mode you're in, and offers
**Restart Python** — this shuts down the current Python and starts a
fresh one, which is useful if something gets stuck in a way Stop can't
fix. Your files come back automatically after a restart.

---

## Saving Your Work

### Cells Save Automatically

- Every cell saves in your browser automatically, every time you change
  anything — edit, add, remove, reorder, or run a cell
- Nothing to save manually

### What's Saved

- Whether a cell is Python or Text
- What's written in the cell
- The order of your cells
- What the cell showed the last time it ran (so you still see it after
  reloading the page, without running it again)
- Whether the cell's last run had an error

### What's Not Saved

- Python itself starts fresh every time you open the page — a saved
  cell shows you what it showed last time, but you'd need to run it
  again to actually compute anything new
- Anything typed into a widget resets when you reload

### Files

Uploaded files, `.db` files, and anything a cell writes stick around in
whichever storage is backing the file manager (see
[Files and Storage](#files-and-storage)) — separately from your cells,
and Clear All doesn't touch them.

### Browser Storage Keys

| Key | What it's for |
|-----|-----|
| `mini-ide:cells:v1` | All your cell data |
| `mini-ide:import-mode` | Whether Import replaces or adds to your cells |
| `mini-ide:notes` | The free-text "Your notes" box in Settings |
| `mini-ide:filename` | The file name Settings uses for downloads and the tab title |
| `mini-ide:editor` | Code size, cell spacing, cursor width, and the line-number/active-line toggles |
| `dewlab:texture` | Your theme/font/size choices (shared with the tutorials) |

If you've chosen a real folder, permission to use it is remembered
separately, in a different kind of browser storage (IndexedDB) — not
alongside the list above, since a folder permission isn't the kind of
thing that fits in a plain list of settings.

---

## Download Formats

### Python File (.py)

```python
print("first cell")

# %%

print("second cell")
```

**What you get:**
- Only Python cells — text cells aren't included
- Cells are separated by `# %%` (the same marker Jupytext, VS Code, and
  Spyder use), which matches what Import expects, so downloading and
  then importing a file gives you back the same cells

### HTML File (.html)

A snapshot — each cell's code and its last output, saved as plain
markup. It is **not** a page you can run: there's no Python in it, and
nothing in it does anything when you open it. Good for showing someone
what a notebook looked like, not for handing them something they can
keep working in. (For an actual runnable copy of Mini IDE, see
[The Downloadable Mini IDE](#the-downloadable-mini-ide).)

### Jupyter Notebook (.ipynb)

A real Jupyter Notebook file:
- Opens in Jupyter Notebook, JupyterLab, or Google Colab
- Keeps your cell types and their order (text cells become Markdown,
  Python cells become Code)
- Includes the usual Jupyter file details

### Print / Save as PDF

The **Print / Save as PDF** button in Settings ("Keep a copy") calls
the browser's own print dialog, from which "Save as PDF" is a printer
choice like any other. Chrome, the file manager, Settings, and the
faint insert seams between cells are all hidden on the printed page —
just the cells and their output remain, in light ink regardless of
which theme you were reading in.

All four — the three file downloads and the printed copy — use the
file name set in Settings.

---

## The Downloadable Mini IDE

Beyond saving your *work*, you can download the whole Mini IDE tool
itself, as a folder (or a matching zip file) that runs without needing
a server — save it, open `mini-ide.html` from your computer, and it
works the same as it does online.

Whether you need internet the first time you open it depends on
whether the copy you downloaded already includes Python:

- **If it includes Python**: it starts up from the files right there
  next to `mini-ide.html` — no internet needed, ever.
- **If it doesn't**: the first time you open it, it still needs to
  fetch Python from the internet, the same as the online version — but
  after that, it behaves exactly the same either way.

This is a choice dewlab's maintainers make when they build a copy to
share, not something you set up yourself.

---

## How It's Built

Mini IDE is made of a few pieces that work together: `mini-ide.js`
manages your cells and the page itself; `mini-ide-engine.js` starts
Python and talks to it; `mini-ide-fs.js` handles your files. If you
want to understand how the code actually works, each of those files has
its own explanation doc in `docs/` (for example,
`docs/mini-ide-js-explained.md`) that walks through it in more detail
than fits here.

If you want to build dewlab yourself, change the code, or contribute a
fix, [`CONTRIBUTING.md`](../CONTRIBUTING.md) at the top of the repo is
where to start.

---

## Keyboard Shortcuts

| Shortcut | What it does |
|----------|--------|
| Shift+Enter | Runs the cell |
| Tab | Indents, or accepts a suggestion |
| Shift+Tab | Un-indents |
| Enter | Accepts a suggestion, or starts a new line |
| Escape | Closes the suggestion list, or leaves the cell |
| Ctrl+Z | Undo |
| Ctrl+Y | Redo |
| Ctrl+A | Select all |
| Ctrl+C | Copy |
| Ctrl+V | Paste |
| Ctrl+X | Cut |

---

## Troubleshooting

### Python Won't Load

**What you'll see**: the status bar stays stuck on "Starting Python…"
or "Loading numpy, pandas, matplotlib…"

**Possible reasons**:
- No internet connection (unless you're using a fully offline
  downloaded copy — see [The Downloadable Mini IDE](#the-downloadable-mini-ide))
- A firewall or network is blocking the download
- Your browser is blocking something it shouldn't

**Try this**:
- Check your internet connection
- Try a different browser or network
- Wait a bit — this is a real download, and it takes a moment
- Refresh the page; if Python started once and now seems stuck, try
  Settings → Python → **Restart Python**

### Stop Doesn't Interrupt a Cell

**Why**: your browser hasn't finished the one-time setup Stop needs, or
Python is running in the fallback mode instead of the background — see
[Execution Engine](#execution-engine).

**Try this**:
- Reload the page once (this setup sometimes needs a reload the very
  first time)
- Check Settings → Python to see which mode you're in
- As a last resort, use Restart Python in that same section

### Cells Won't Run

**What you'll see**: clicking Run does nothing, or shows an error right
away

**Possible reasons**:
- Python hasn't finished starting yet
- There's a mistake in your code
- Something went wrong in the browser

**Try this**:
- Wait for the status bar to clear
- Open the browser console (press F12) to see if there's an error
- Fix any mistakes in your code

### Files Aren't Working

**What you'll see**: the file manager still says "Files appear here
once Python starts", or uploading shows an error

**Why**: nothing is stored anywhere until Python has started at least
once.

**Try this**: run any cell, then try again.

### Downloads Aren't Working

**What you'll see**: clicking a download button does nothing

**Possible reasons**:
- Your browser is blocking downloads or pop-ups
- There's nothing to download (for `.py`, specifically no Python cells)

**Try this**:
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
| Mobile Safari | ✅ (not tested as much) | ✅ | Falls back to private browser storage |

**You'll need:**
- A fairly modern browser (anything from the last few years works)
- JavaScript turned on

Choosing a real folder on your computer specifically needs a feature
that, right now, only Chrome and Edge support. Every other feature,
including the file manager itself, works the same way in any browser —
it just uses that browser's own private storage instead of a real
folder.

---

## Limitations

1. **A hosted copy needs internet the first time**: only a downloaded
   copy that already includes Python (see
   [The Downloadable Mini IDE](#the-downloadable-mini-ide)) can start up
   with no internet at all
2. **Your work doesn't follow you between devices**: cells and files
   are saved on the one browser and device you used — unless you've
   chosen a real folder that happens to sync itself through something
   outside Mini IDE, like a cloud backup tool you already use
3. **No working together live**: you can't share a session with someone
   else in real time
4. **The `.html` download isn't interactive**: it has no Python in it,
   so nothing in it responds to clicks
5. **No step-by-step debugger**: you can't pause code partway through
   and look around
6. **Normal browser memory limits apply**: to both Python and your
   files

---

## Comparison with Other Tools

| Feature | Mini IDE | Jupyter | Colab | VS Code |
|---------|----------|---------|-------|---------|
| Runs in your browser | ✅ | ❌ | ✅ | ❌ |
| Nothing to install | ✅ | ❌ | ❌ | ❌ |
| Works offline | ✅ (downloadable, Python included) | ❌ | ❌ | ✅ |
| Cell-based | ✅ | ✅ | ✅ | ❌ |
| Autocomplete | ✅ | ✅ | ✅ | ✅ |
| File manager | ✅ | ✅ | ✅ (Drive) | ✅ |
| SQL support | ✅ (`sqlite3` + `run_query`) | with an extension | with an extension | with an extension |
| Saves your work | ✅ (in-browser + files) | ⚠️ (needs a server) | ✅ (Google Drive) | ✅ (on your computer) |
| Download as .py | ✅ | ❌ | ✅ | ✅ |
| Download as .ipynb | ✅ | ✅ | ✅ | ❌ |
| Load .ipynb / .py | ✅ | ✅ | ✅ | ✅ |
| Cells share one program | ✅ | ✅ | ✅ | ❌ |
| dewlab's own functions | ✅ | ❌ | ❌ | ❌ |

---

## What Might Come Next

Not built yet, but on the list:

- **Folding code**: collapsing and expanding blocks of code
- **Folding output**: hiding and showing a cell's output
- **Folders inside the file manager**: right now it only shows one flat
  list
- **More keyboard shortcuts**
- **More color themes**

---

## License

Mini IDE is part of dewlab and uses the same license.
See [LICENSE.md](../LICENSE.md) for details.

---

## Version History

| Version | Date | What changed |
|---------|------|---------|
| 1.0 | 2025-01-XX | First release |
| 2.0 | 2026-08-29 | Runs Python in the background with a real Stop button; a file manager backed by a real folder or private browser storage; file upload; SQLite through `run_query()`; loading `.ipynb`/`.py` files; more settings; a downloadable, sometimes fully offline copy of Mini IDE itself |
