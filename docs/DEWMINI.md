# dewmini

dewmini is a small notebook for writing and running Python in your
browser. It uses the same Python as dewlab's tutorials, so there is
nothing to install. No tutorial is attached to it. Open it at
`compose/dewmini.html` and you get a blank page, ready for you to add a
cell.

Use it when a tutorial does not quite cover what you want to try. It
suits four things in particular:

- testing an idea before you decide whether it belongs in a lesson
- working on a practice problem away from the tutorial it came from
- keeping a small project going across sessions, with its own files
- running a few lines of Python that are not tied to any one topic

A tutorial page is mostly reading, with some code mixed in. dewmini is
mostly code, with room for a few notes.

---

## What you see

dewmini is a plain page. Cells sit directly on the background rather
than in bordered boxes. Each cell has a thin colored line down its left
side, and that line is invisible most of the time. It turns orange for
the cell you touched last. It turns red if that cell's last run gave an
error.

You can add a cell between any two cells, before the first one, or after
the last one. The spot is easy to miss until you hover over it or tap
it. It offers you a blank Python cell or a text cell.

A Python cell runs when you press its **Run** arrow. **Shift+Enter**
inside the cell runs it and then moves you to the next one, so you can
work down a notebook without reaching for the mouse. **Ctrl+Enter**, or
**Cmd+Enter**, runs the cell and leaves you where you are.
**Ctrl/Cmd+F** opens find-and-replace inside the cell you are in. Cells
share one set of variables from top to bottom, the way a notebook does.
Something an earlier cell defines, a later cell can use. **Run all**
first clears every cell's output, then reruns the whole page in order,
so what is on screen matches what the code did. Drag a cell by its
header to move it anywhere on the page.

Each Python cell also has a small **↺** button next to Run. It clears
that one cell's output and keeps its code, which gives you a clean slate
on a single cell without rerunning everything else. The toolbar's
**Clear output** does the same for every cell at once, and it also keeps
every cell and its code. **Clear** is the destructive one: it deletes
the cells themselves.

A small line under a cell's output shows how long the cell took to run.
You can turn that off in Settings.

A cell's own **×** needs two clicks. The first click arms the button and
turns it solid red. The second click, straight after, deletes the cell.
Click anything else, or wait a few seconds, and the button disarms
again.

If you edit a cell after running it, a small **"Edited since last run"**
note appears next to its label — a reminder that the output still
showing underneath belongs to the *old* code, not what's there now. Run
the cell again and the note goes away. The **⋯** button next to a cell's
Run arrow opens two more ways to run it: **Run above** runs every cell
from the top through this one, from a clean start — the fix once an
earlier cell's output has gone stale; **Run below** runs this cell and
everything after it, keeping whatever the cells above it already
defined, for redoing the rest of a notebook without paying to redo a slow
first step. Settings' **Restart & run all** goes further still: it
throws Python away completely and reruns every cell from a genuinely
fresh start — the real test of whether a notebook actually works, not
just whether it happened to work the way you built it up.

While you type, dewmini offers the same completion, hover documentation,
and function-signature help a tutorial page's cells do — on code that
hasn't run yet, not only on names already defined in a cell you've
already run.

A text cell is for notes next to your code — a heading, a reminder of
what a section does, or notes on what you tried. Click away from it and
it turns into formatted text: `# a heading`, `**bold**`, `*italic*`,
`` `code` ``, and `- a bullet list` all format themselves. Maths formats
itself too: `$x^2 + 3x$` renders as a real equation, and `$$...$$` on its
own puts it on its own centered line — the same maths a tutorial page can
show you, now available for working through a problem in your own words.
Click back into the formatted text to edit the plain words underneath, or
use the **Edit**/**View** button in its header — the same switch, worth
having if clicking the rendered text isn't an option you'd think to try.
Its picture-frame icon attaches an image from your device — the image
stays with the cell, and is never uploaded anywhere.

---

## Getting started

The toolbar offers three ways to begin, and they stay there rather than
disappearing once you have cells. **See an example** loads four cells —
one that prints something, a small numpy calculation, a text cell
showing what one looks like once formatted, and a plot — and runs them
right away, so the first thing you see is dewmini actually doing
something, not an explanation of what it could do. **Start with
imports** begins with one cell that imports the packages most sessions
need (`numpy`, `pandas`, `matplotlib.pyplot`), and leaves the rest to
you. **Practice** adds a problem from dewlab's own practice bank.

To add a cell, use the seam: the thin line between any two cells, and
above the first, carries **Python** and **Text** buttons. That is the
only place they live, so a cell always arrives where you were looking
rather than at the bottom of a page you then have to scroll back up.

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
| `text_input(label="", value="", id=None)` | A text box — read what was typed with `.value`. **See the note below.** |
| `dropdown(label="", options=(), value=None, id=None)` | A menu — read the choice with `.value`. **See the note below.** |
| `button(label="Go", on_click=None, id=None)` | A button that calls a function when pressed. **See the note below.** |
| `image_input(label="Choose an image", id=None)` | A file picker for an image — read the picked file with `.value`. **See the note below.** |
| `await load_csv(name, **read_csv_kwargs)` | Load a CSV from dewlab's shared data folder, if one is there |

**The four widgets do not work here at the moment, and say so when you
call one.** A widget attaches a listener to a live element on the page,
and dewmini runs Python in a background worker — off the page's own
thread, which is exactly what lets the Stop button interrupt a runaway
cell. There is no page on the far side of that boundary to attach a
listener to, so calling one raises a clear error rather than drawing
something that quietly does nothing. A tutorial page makes the same trade
(`DECISIONS_LOG.md` 7.77). They work in a downloaded copy, which runs
Python on the page's own thread.

`numpy`, `pandas`, and `matplotlib` are available without importing
them, though you can still `import` them if you want — dewmini keeps
that import visible on purpose, so a cell you copy somewhere else still
makes sense by itself. Two more things go beyond what a tutorial page
offers: `sqlite3`, a real database built into Python with nothing to
install (`import sqlite3` and go — see Files below for where a `.db`
file it creates actually lives), and Pillow, which is what
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

## More than one notebook

**New** opens a second notebook in its own tab. Each keeps its own cells,
its own name, and its own downloads — so a scratch calculation doesn't
have to live in the middle of a project. Click a tab to switch,
double-click its name to rename it, and the **×** closes it (it asks
first, if there's anything in it). The row of tabs only appears once you
have more than one, so a single notebook looks exactly as it always did.

One thing worth knowing: **every tab shares one Python session.** A
variable you make in one notebook is visible in another. That is
sometimes useful and occasionally surprising, which is why the
Workbench's **Variables** list shows you the one session everything
shares.

---

## The two side panels

Three buttons in the header, opening panels docked down the sides of the
screen. Nothing opens by itself — if you came to run three lines and
leave, you never need to touch any of them.

**Library**, on the left, is everything you look *up*. **Workbench**, on
the right, is everything about the work in front of you. **Settings** is
what you change. Because the Library docks to the opposite side from the
other two, you can keep a definition open beside your own variables;
Workbench and Settings share the right-hand edge, so opening one closes
the other.

On a screen wide enough, opening a panel shrinks the working area rather
than covering it, so your cells stay fully visible. Drag a panel's inner
edge to resize it. Whatever you leave open is still open when you come
back, and **Esc** closes a panel — clicking your own code never does, so
a reference you opened to read while writing stays put.

On a phone, panels slide up from the bottom instead.

### Library

**Reference** — every term, function and operator any dewlab tutorial
introduces, in one searchable list, with the tutorial that introduced
each one named underneath it. Unlike a tutorial page's own reference,
which shows only what you have been taught so far, this one shows
everything — in a workspace with no tutorial attached there's no "so
far" to go by, and hiding two-thirds of it would just be unhelpful.

Search it, or narrow it with the buttons above the list:

- **Maths** and **Computing**, from the modules a term's tutorial
  belongs to. A tutorial that covers both is filed under both.
- **Beginner**, **Intermediate** and **Advanced**, from how many layers
  of groundwork sit under what that tutorial teaches. Nothing is
  labelled by hand — this is read off the topic map, so it stays true to
  the map rather than to whoever last remembered to update it.
- **Topics** folds open for the broader groupings (trigonometry,
  matrices, simulation, and so on), and **kind** for concepts,
  functions, operators, formulas and keywords.

Each button says how many terms it would leave, so one that would empty
the list tells you before you press it. Picking two in the same row
means *either*, not both. A term from a tutorial that claims no outcomes
is filed under **Unfiled** rather than hidden.

**Data** — real datasets you can load, each saying where it came from
and what licence it carries. Pick one and it writes a working cell into
your notebook. Some are already in dewlab; others are fetched from the
web when you run the cell, which needs a connection and needs that site
to allow it (if it doesn't, the error says so, and says what to do
instead — download the file and add it through Files).

The rest of the Library is what used to be **Help**: how cells work, the
keyboard shortcuts, what a cell can call, and how your work is kept.

### Workbench

**Variables** — what's actually in your Python session right now: every
name, its type, and a short summary of its value (how many rows a table
has, how many items a list holds, what a number is). It updates every
time you run a cell. This answers a question that was awkward before —
"did that actually work?" — without printing everything twice. Functions
and modules fold away under their own line, so your own variables stay
at the top.

**Your notes** — a place to jot down anything worth remembering as you
work. It stays with this browser rather than with any one notebook.

**Files** — a real filesystem a cell can read and write to, separate
from the notebook itself (that's "Keep a copy," in Settings). By default
it's private, invisible storage inside your browser; **Use a folder on
my computer** switches to a real folder instead, in a browser that
supports it (Chrome or Edge), so files a cell writes actually appear on
your computer where you can see them — a `sqlite3` database a cell
creates, a chart a cell saves to disk, anything `open()` can write.
**Add a file…** brings an existing file from your device into whichever
storage is active, for a cell to read back with a plain `open()`. The
list below shows what's there, with a way to delete anything you no
longer need.

**Your own Python files live here too, and you can import them.** Write
shapes.py into this storage. A cell can then say `import shapes` and
call `shapes.area(4)`. That is how a program spread across several files
works anywhere else, and it is the step from writing functions to using
them.

One thing about it surprises most people the first time. Python reads a
file once and remembers it. Editing that file after you have imported it
does not change what runs. You fix a mistake, run the cell again, and
get the same wrong answer. dewmini notices when this happens, names the
file that changed, and offers to re-read it. The behaviour is Python's
own, and you will meet it in every other Python you use. That is why
dewmini tells you about it rather than working around it quietly.

Re-reading a file replaces what is inside it. A name you imported with
`from shapes import area` still points at the old version, so run that
line again as well.

### Settings

**Python** — shows how Python is currently running (in a background
worker, so a runaway cell can be stopped without freezing the page; or
directly in the page, on a browser or setting where a background worker
isn't available, where it can't be) and a **Restart Python** button for
starting over with a clean interpreter — everything a cell has defined
so far is discarded, though your cells and their code are untouched.
Next to it, **Restart & run all** does both at once: a clean interpreter,
then every cell run in order from the top — the way to check a notebook
still works from scratch, not just from wherever you happened to leave
it. Below that, the **Run time** switch turns the small "ran in…" line
under a cell's output on or off.

**Keep a copy** — the name of the notebook you're looking at, which is
also its tab's name and the name every download below uses. Then:
download as a Python file, a standalone HTML page, or a Jupyter
notebook; print — or save as PDF — with just the code and its output,
none of the page's own header and buttons; and load a `.ipynb` or `.py`
file back in, from here or anywhere else, to keep working on it. An
import **opens in a new tab**, so it never lands on top of what you were
doing. A `.py` file dewmini itself exported comes back exactly as it
was, cell by cell, including its text cells; a plain, unmarked `.py`
script comes back as one Python cell. A notebook written outside dewmini
can bring along things Pyodide's Python genuinely can't run (a `tkinter`
window, a Jupyter "magic" command, a `!pip install` shell line); a
warning banner names exactly which imported cell each one is in, right
after the import.

Four ready-made examples sit right below that import button — real
data included, each opening in its own tab: **SQL & Our
World in Data** (`sqlite3` and `run_query()` against real CO₂ emissions
data), **a mini data investigation** (has life expectancy converged
worldwide since 1950?), **a fun math problem** (estimating π by
throwing random darts), and **word frequency: usual or unusual?**
(checking a real novel against Zipf's law). Each is a real, runnable
dewlab tutorial in miniature.

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
it somewhere else, use one of the downloads in Settings, or the
Workbench's Files section and its "use a folder on my computer" if what
you want to keep is a file a cell wrote, not the notebook itself.

A browser gives each site a limited amount of room, usually around five
megabytes. One chart takes up far more of that room than all your code
does. If you fill it, dewmini keeps your code and gives up the outputs
it cannot fit. It names the ones it dropped. Run those cells again after
a reload and the outputs come back. If even the code will not fit,
dewmini says so and asks you to download the notebook. A reload from
that point would lose your work.

- **`.py`** joins every Python cell together and turns each text cell
  into a comment block. The whole session then reads as one ordinary
  Python file, and it loads back in here exactly as it was.

  The cells are marked with `# %%` lines. A text cell is marked
  `# %% [markdown]`. Python ignores both, so the file still runs as an
  ordinary script. Visual Studio Code, Spyder, PyCharm and Jupytext all
  understand these markers, so the same file opens as the same cells on
  another machine. The file starts with a few comment lines saying so,
  and you can delete them without changing anything.

  A `.py` file has nowhere to keep what your cells printed. It holds
  the code, not the results.
- **`.html`** is a single file you can open by double-clicking. It
  carries its own copy of the notebook tools and runs its cells the
  moment it opens. Like a tutorial's own downloadable copy, it needs an
  internet connection the first time you open it — that's when it
  actually fetches Python — and works without one after that.
- **`.ipynb`** is a real Jupyter notebook file: Python cells become code
  cells, text cells become markdown cells, and it opens in Jupyter,
  JupyterLab, or Colab. The same file loads back into dewmini from
  Settings.

  This is the download that keeps your results. Printed text, tables
  and figures travel with the file. They are there when you open it
  again, here or anywhere else. A notebook someone else made shows you
  their results as soon as you load it, without running anything.

---

## The downloadable dewmini

Beyond saving your work, the link under dewmini's own title —
"downloadable copy of dewmini itself" — gets you the whole tool as a
zip: unzip it, and it works the same as it does online, with no internet
needed at all once you've unzipped it, once the copy you downloaded
already includes Python. Good for a classroom with no reliable
connection, or for keeping a copy that works the same next year
regardless of what the hosted site looks like by then.

It needs one extra step the online version doesn't: after unzipping,
run `python3 serve.py` from inside the folder (open a terminal there
first) rather than double-clicking `index.html` directly. A modern
browser won't let a page opened straight off disk load its own
JavaScript the way dewmini needs to — *serve.py* starts a small local
server and opens the right page for you, and needs nothing installed
beyond the Python already running it. Leave that terminal window open
while you use dewmini; closing it stops the server.
