# dewmini

dewmini is a small notebook for writing and running Python in your
browser. It uses the same Python as dewlab's tutorials — nothing to
install — but without a tutorial attached to it. Open it at
`compose/dewmini.html`, or from the **dewmini** link on the Mini IDE
page, and you get a blank page ready for you to add a cell.

Use it when a tutorial doesn't quite cover what you want to try: testing
an idea before deciding it belongs in a lesson, working on a practice
problem away from the tutorial it came from, or just wanting somewhere
to run a few lines of Python that isn't tied to one topic. A tutorial
page is mostly reading, with some code mixed in. dewmini is mostly code,
with room for a few notes.

dewlab's other Python tool, the [Mini IDE](../assets/mini-ide.html), is
the bigger of the two — it has a fuller toolbar and more export options,
built for a project that stands on its own outside any tutorial. dewmini
stays small on purpose: use it for something quick, and switch to Mini
IDE once a project grows past that.

---

## What you see

dewmini is a plain page, not a busy app. Cells sit directly on the
background with a thin colored line down the left instead of a bordered
box — navy for a Python cell, gray for a text cell, orange for whichever
cell you touched last. Between any two cells — and before the first one,
and after the last one — you can add a new cell right there: a blank
Python cell or a text cell. That spot is easy to miss until you hover
over it or tap it, but it's there between every pair of cells if you
look.

A Python cell runs when you press its **Run** arrow, or press
**Shift+Enter** inside it. Cells share one set of variables from top to
bottom, notebook-style: something an earlier cell defines, a later cell
can use. **Run all** clears every cell's output and reruns the whole
page in order, so what's on screen always matches what the code actually
did. Drag a cell by its header to move it anywhere on the page.

A text cell is for notes next to your code — a heading, a reminder of
what a section does, or notes on what you tried. Click away from it and
it turns into formatted text: `# a heading`, `**bold**`, `*italic*`,
`` `code` ``, and `- a bullet list` all format themselves. Click back
into the formatted text to edit the plain words underneath, or use the
**Edit**/**View** button in its header — the same switch, worth having
if clicking the rendered text isn't an option you'd think to try. Its
picture-frame icon attaches an image from your device — the image stays
with the cell, and is never uploaded anywhere.

---

## Getting started

An empty page offers two ways to begin. **See an example** loads four
cells — one that prints something, a small numpy calculation, a text
cell showing what one looks like once formatted, and a plot — and runs
them right away, so the first thing you see is dewmini actually doing
something, not an explanation of what it could do. **Start with
imports** instead begins with one cell that imports the packages most
sessions need (`numpy`, `pandas`, `matplotlib.pyplot`), and leaves the
rest to you. Either way, the toolbar's **Python**, **Text**, and
**Practice** buttons — and every gap between cells once you have some —
let you add more.

---

## What a cell can call

A Python cell can use the same eight functions a tutorial's cells can,
because it runs the exact same code a tutorial page runs, loaded fresh
rather than copied:

| Function | What it does |
|---|---|
| `show(*values, label=None)` | Show one or more values in the middle of a cell, not just at the end |
| `show_table(frame, max_rows=20, caption=None)` | Show a DataFrame or Series as a table |
| `check(actual, expected, tolerance=None, label=None)` | A quick right / not-yet check; floats are compared within a small tolerance |
| `text_input(label="", value="", id=None)` | A text box — read what was typed with `.value` |
| `dropdown(label="", options=(), value=None, id=None)` | A menu — read the choice with `.value` |
| `button(label="Go", on_click=None, id=None)` | A button that calls a function when pressed |
| `image_input(label="Choose an image", id=None)` | A file picker for an image — read the picked file with `.value` |
| `await load_csv(name, **read_csv_kwargs)` | Load a CSV from dewlab's shared data folder, if one is there |

`numpy`, `pandas`, and `matplotlib` are available without importing
them, though you can still `import` them if you want — dewmini keeps
that import visible on purpose, so a cell you copy somewhere else still
makes sense by itself. Two more things go beyond what a tutorial page
offers: `sqlite3`, a real database built into Python with nothing to
install (`import sqlite3` and go), and Pillow, which is what
`image_input()` uses to open a picked image — you get a Pillow `Image`
if Pillow has loaded, or the file's raw bytes on the rare page where it
hasn't. If a cell raises an error, you'll see the traceback trimmed down
to your own code — the same trimming a tutorial page's cells get — so
what's left on screen is the mistake actually worth reading.

---

## Practice

The **Practice** button adds one problem from dewlab's practice bank — a
text cell naming the problem, and a Python cell holding the function
you need to fill in, docstring and all, exactly as written in the source
bank. Settings has an **Order** switch: **in order** works through the
bank one problem at a time and remembers where you left off; **random**
picks problems out of order, without repeating one until every problem
in the bank has come up once. Filling in the function and running the
cell is the whole exercise — there's no separate answer key to submit
to, just the docstring's own example to check your result against.

---

## Settings

One button in the header opens everything you can change or take with
you, in sections:

**Your notes** — a place to jot down anything worth remembering as you
work, saved along with your cells.

**Keep a copy** — a name for your session, used in every download below
and shown in the browser tab, so "print to PDF" and file downloads
suggest something more useful than a default name. Below it: download
as a Python file, a standalone HTML page, or a Jupyter notebook; print —
or save as PDF — with just the code and its output, none of the page's
own header and buttons; and load a `.ipynb` file back in, from here or
anywhere else, to keep working on it.

**Practice** — the order switch described above.

**Texture** — the same reading preferences every dewlab page has: theme,
font, text size, page width, link color. A choice you make here follows
you to the tutorials, and a choice you make on a tutorial page follows
you back here.

**Editor** — settings specific to a page about writing code rather than
reading it: how large the code is, how much room a cell gives itself
(compact, cozy, or relaxed), how heavy the cursor looks, and whether
line numbers and the current line's highlight show at all. None of this
changes how the code runs — only how it looks.

---

## Keeping your work

Everything you type in dewmini saves to the browser you typed it in, as
you type it — nothing is sent anywhere, and nothing is scored. That also
means your work stays on that one browser and that one device; to move
it somewhere else, use one of the downloads in Settings.

- **`.py`** joins every Python cell together with a separator, and turns
  each text cell into a comment block, so the whole session reads as one
  ordinary Python file.
- **`.html`** is a single file you can open by double-clicking. It
  carries its own copy of the notebook tools and runs its cells the
  moment it opens. Like a tutorial's own downloadable copy, it needs an
  internet connection the first time you open it — that's when it
  actually fetches Python — and works without one after that.
- **`.ipynb`** is a real Jupyter notebook file: Python cells become code
  cells, text cells become markdown cells, and it opens in Jupyter,
  JupyterLab, or Colab. The same file loads back into dewmini from
  Settings.

---

## What's different from a tutorial page

A tutorial page can genuinely stop a cell that's run away — say, an
accidental infinite loop — because it runs Python in a background
worker built to allow that. dewmini runs Python directly in the page
instead, the simpler and older of the two approaches, so a cell that
never finishes has to be waited out, or the page reloaded, rather than
stopped with a button. The shared data folder `load_csv` reads from is
real but currently empty, so asking for a file that isn't there yet
tells you so rather than pretending it worked. Widgets — `text_input`,
`dropdown`, `button`, `image_input` — work here exactly as they do on a
tutorial page, since dewmini keeps Python in the main page, right where
that direct connection to the page is available.
