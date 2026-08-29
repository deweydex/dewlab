# dewmini

dewmini is a small notebook for writing and running Python in the browser —
the same zero-installation Python dewlab's tutorials use, without a tutorial
attached to it. Open it at `compose/dewmini.html`, or from the **dewmini**
link on the Mini IDE page, and you get a blank page with nothing on it but an
invitation to add a cell.

It exists for the moment a tutorial doesn't quite cover: trying something out
before deciding whether it belongs in a lesson, working through a practice
problem away from the material it came from, or just wanting somewhere to
run a few lines of Python that isn't tied to any one topic. Where a tutorial
page is a reading with code inside it, dewmini is closer to the reverse — a
sheet of code with room for notes beside it.

dewlab's other Python workspace, the [Mini IDE](../assets/mini-ide.html), is
the larger tool of the two — a fuller toolbar and export set for a project
meant to stand on its own outside any one tutorial. dewmini stays deliberately
smaller: reach for it for the quick, disposable session; reach for the Mini
IDE once a project outgrows one.

---

## What you see

A page, not an application chrome. Cells sit directly on the background with
a thin coloured line down the left rather than a bordered box — navy for a
Python cell, muted grey for a documentation cell, orange for whichever one
you last touched. Between every pair of cells, and before the first and
after the last, a seam sits ready to insert exactly there: a blank Python
cell or a documentation cell. The seam is faint until you rest a cursor or a
finger on it, not invisible — run down the page and you'll find every one.

A Python cell runs when you press its **Run** arrow, or press
**Shift+Enter** from inside it. Cells share one namespace top to bottom, the
notebook way: something an earlier cell defines, a later one can use.
**Run all** clears every cell's output and reruns the whole page in order,
so what's on screen always matches what the code above it actually did.
Drag a cell by its header to move it anywhere in the page.

A documentation cell is for notes beside the code — a heading, a reminder of
what a section is doing, a place to write down what you tried. Click away
from it and it renders: `# a heading`, `**bold**`, `*italic*`, `` `code` ``,
and `- a bullet list` all format themselves. Click back into the rendered
text to return to plain words underneath. Its picture-frame icon attaches an
image from your device — kept with the cell itself, never uploaded anywhere.

---

## Getting started

The empty page offers two ways in. **See an example** loads four cells — a
line of output, a small numpy calculation, a documentation cell showing what
one looks like rendered, and a plot — and runs them immediately, so the
first thing you see is dewmini actually doing something rather than an
explanation of what it could do. **Start with imports** begins instead with
a single cell carrying the imports most sessions reach for
(`numpy`, `pandas`, `matplotlib.pyplot`) and leaves the rest to you.
Either way, the toolbar's **Python**, **Text**, and **Practice** buttons —
and every seam between cells once there are some — add more.

---

## What a cell can call

A Python cell has the same eight functions a tutorial's cells do, because it
runs the same underlying module a tutorial page runs, fetched fresh rather
than reimplemented:

| Function | What it does |
|---|---|
| `show(*values, label=None)` | Render one or more values mid-cell, not only at the end |
| `show_table(frame, max_rows=20, caption=None)` | Render a DataFrame or Series as a table |
| `check(actual, expected, tolerance=None, label=None)` | A quick right / not-yet, with floats compared to a tolerance |
| `text_input(label="", value="", id=None)` | A text box; read what was typed with `.value` |
| `dropdown(label="", options=(), value=None, id=None)` | A menu; read the choice with `.value` |
| `button(label="Go", on_click=None, id=None)` | A button that calls a function when pressed |
| `image_input(label="Choose an image", id=None)` | A file picker for an image; read the picked file with `.value` |
| `await load_csv(name, **read_csv_kwargs)` | Load a CSV from dewlab's shared data folder, if one is there |

`numpy`, `pandas`, and `matplotlib` are available without importing them,
though a cell is free to `import` them anyway — dewmini keeps that import
visible rather than hiding it, since a cell copied out to somewhere else
should still make sense on its own. Two more sit a step beyond a tutorial
page's own defaults: `sqlite3`, a genuine Python database on the page with
nothing to install (`import sqlite3` and go), and Pillow, what
`image_input()` decodes a picked file into — a Pillow `Image` when Pillow
has loaded, the file's raw bytes on the rare page where it hasn't. A cell
that raises an error shows the traceback trimmed to its own line, the same
trimming a tutorial page's cell gets, so what's left on screen is the
mistake actually worth reading.

---

## Practice

The **Practice** button adds one problem from dewlab's own practice bank — a
documentation cell naming the problem, and a Python cell holding the
function stub exactly as it's written in the source bank, docstring and all,
ready to fill in. Settings has an **Order** switch: **in order** works
through the bank sequentially and remembers where a session left off;
**random** deals problems out of sequence without repeating one until every
problem in the bank has come up once. Filling in the stub and running the
cell is the whole exercise — there's no separate answer key to submit to,
only the docstring's own worked example to check a result against.

---

## Settings

One button in the masthead opens everything a page can change or a session
can take with it, in sections:

**Your notes** — a place to jot anything worth remembering as a session goes,
saved alongside the cells.

**Keep a copy** — a name for the session, used across every download below
and shown in the browser tab, so "print to PDF" and file downloads alike
suggest something more useful than a default. Below it: download as a
Python file, a standalone HTML page, or a Jupyter notebook; print — or save
as PDF — with the code and its output and none of the page's own chrome;
and load a `.ipynb` back in, from here or anywhere else, to continue working
on it.

**Practice** — the order switch described above.

**Texture** — the same reading preferences every dewlab page carries: theme,
font, text size, page width, link colour. A choice made here follows a
reader to the tutorials, and a choice made on a tutorial page follows them
back here.

**Editor** — the settings unique to a page about writing code rather than
reading it: how large the code is, how much room a cell gives itself
(compact, cozy, or relaxed), how heavy the cursor is, and whether line
numbers and the active line's highlight show at all. Nothing here touches
how the code runs, only how it sits on screen.

---

## Keeping your work

Everything typed into dewmini saves to the browser it was typed in, as it's
typed — nothing is sent anywhere, and nothing is scored. That also means the
work stays on that one browser and that one device; carrying it somewhere
else means taking one of the copies Settings offers along.

- **`.py`** joins every Python cell with a separator, and turns each
  documentation cell into a comment block, so the whole session reads as one
  ordinary Python file.
- **`.html`** is a single file that opens by double-clicking, carrying its
  own copy of the notebook tools and running its cells the moment it opens.
  Like a tutorial's own downloadable copy, it needs an internet connection
  the first time — Python itself is fetched then — and works without one
  after that.
- **`.ipynb`** is a real Jupyter notebook file: Python cells become code
  cells, documentation cells become markdown cells, openable in Jupyter,
  JupyterLab, or Colab. The same format loads back into dewmini from
  Settings.

---

## What's different from a tutorial page

A tutorial page can genuinely stop a cell that's run away — an accidental
infinite loop, say — because it runs Python in a background worker built for
exactly that. dewmini runs Python in the page itself, the simpler and older
of the two approaches, which means a cell that never finishes has to be
waited out or the page reloaded rather than interrupted. The shared data
folder `load_csv` reads from is real, but currently empty, so a name that
isn't there yet will say so rather than pretend otherwise. Widgets —
`text_input`, `dropdown`, `button`, `image_input` — work here exactly as
they do on a tutorial page, since dewmini keeps Python on the main thread
precisely where that live DOM connection is available.
