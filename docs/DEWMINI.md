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
inside the cell runs it and then moves you to the next one. That lets
you work down a notebook without reaching for the mouse. **Ctrl+Enter**, or
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
note appears next to its label. The output still showing underneath
belongs to the *old* code. Run the cell again and the note goes away.

The **⋯** button next to a cell's Run arrow opens two more ways to run
it. **Run above** starts from a clean slate and runs every cell from the
top down to this one. That is what you want once an earlier cell's
output has gone stale. **Run below** runs this cell and everything after
it, and keeps whatever the cells above it already defined. That lets you
redo the rest of a notebook without paying again for a slow first step.

Settings' **Restart & run all** goes further. It throws Python away
completely, then reruns every cell from a fresh start. This is the real test of whether a notebook works for somebody opening
it new, rather than only in the order you built it up.

While you type, dewmini offers the same completion, hover documentation
and function-signature help that a tutorial page's cells do. It offers
them on code that has not run yet, as well as on names an earlier cell
already defined.

A text cell is for notes next to your code. It might hold a heading, a
reminder of what a section does, or a record of what you tried. Click away from it
and it turns into formatted text. `# a heading`, `**bold**`, `*italic*`,
`` `code` `` and `- a bullet list` all format themselves.

Maths formats itself too. `$x^2 + 3x$` renders as a real equation, and
`$$...$$` on its own line puts the equation on its own centered line.
This is the same maths a tutorial page shows, now available for working
through a problem in your own words.

Click back into the formatted text to edit the plain words underneath.
The **Edit**/**View** button in the cell's header does the same thing,
and is there for anyone who would not think to click the rendered text.

The picture-frame icon attaches an image from your device. The image
stays with the cell and is never uploaded anywhere.

---

## Getting started

The toolbar offers three ways to begin, and they stay there once you
have cells.

**See an example** loads four cells and runs them straight away. One
prints something. One is a small numpy calculation. One is a text cell,
showing what a note looks like formatted. One is a plot. The first thing
you see is dewmini doing something, rather than an account of what it
could do.

**Start with imports** begins with one cell that imports the packages
most sessions need, which are `numpy`, `pandas` and `matplotlib.pyplot`.
The rest is left to you.

**Practice** adds a problem from dewlab's own practice bank.

To add a cell, use the seam. The thin line between any two cells, and
above the first, carries **Python** and **Text** buttons. That is the
only place those buttons live. A cell therefore arrives where you were
looking, rather than at the bottom of a page you then scroll back up.

---

## What a cell can call

A Python cell can use the same eight functions a tutorial's cells can.
It runs the same code a tutorial page runs, loaded fresh rather than
copied:

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
call one.** A widget attaches a listener to a live element on the page.
dewmini runs Python in a background worker, off the page's own thread,
and that is what lets the Stop button interrupt a runaway cell. On the
far side of that boundary there is no page to attach a listener to.
Calling a widget therefore raises a clear error, rather than drawing
something that quietly does nothing. A tutorial page makes the same
trade (`DECISIONS_LOG.md` 7.77). The widgets do work in a downloaded
copy, which runs Python on the page's own thread.

`numpy`, `pandas` and `matplotlib` are available without importing
them, and you can still `import` them if you want. dewmini keeps that
import visible on purpose, so a cell you copy somewhere else still makes
sense on its own.

Two more things go beyond what a tutorial page offers. `sqlite3` is a
real database built into Python with nothing to install, so `import
sqlite3` and go. Files below says where a `.db` file it creates lives.
Pillow is what `image_input()` uses to open a picked image. You get a
Pillow `Image` when Pillow has loaded, and the file's raw bytes on the
rare page where it has not.

If a cell raises an error, the traceback is trimmed down to your own
code, the same way a tutorial page trims it. What is left on screen is
the mistake worth reading.

---

## Practice

The **Practice** button adds one problem from dewlab's practice bank.
You get a text cell naming the problem, and a Python cell holding the
function to fill in. The function arrives docstring and all, exactly as
written in the bank.

Settings has an **Order** switch. **In order** works through the bank
one problem at a time and remembers where you left off. **Random** picks
problems out of order, and does not repeat one until every problem in
the bank has come up once.

Filling in the function and running the cell is the whole exercise.
There is no answer key to submit to. The docstring's own example is what
you check your result against.

---

## Cells, or one file

The toolbar has two buttons, **Cells** and **File**. They show the same
work two ways, and switching between them converts nothing.

Cells is what you have been reading about: a list of boxes, each with its
own output underneath it. File shows the whole notebook as one Python
document. It is the same one the `.py` download writes. The `# %%` lines
mark where one cell ends and the next begins.

The two behave differently when you run them, and that difference is the
point. In the cells view, Run works on one cell, and the output appears
under that cell. In the file view, **Run the file** works through
the whole thing from the top, the way running a file at a command line
does. The output appears in one place at the end.

A notebook runs in the order you press Run. A file runs in the order it
is written. Moving between the two views is how you find out whether your
work depends on the order you happened to press things in.

Which view a notebook is in is part of that notebook. It stays that way
when you come back, and the tab says so once you have more than one open.

## More than one notebook

**New** opens a second notebook in its own tab. Each notebook keeps its
own cells, its own name and its own downloads. A scratch calculation
therefore does not have to live in the middle of a project. Click a tab to switch
to it, double-click its name to rename it, and the **×** closes it. It
asks first if there is anything in it. The row of tabs appears once you
have more than one notebook, so a single notebook looks as it always
did.

One thing is worth knowing. **Every tab shares one Python session.** A
variable you make in one notebook is visible in another. That is
sometimes useful and sometimes surprising, and it is why the Workbench's
**Variables** list shows the one session that everything shares.

---

## The two side panels

Three buttons in the header open panels docked down the sides of the
screen. Nothing opens by itself. If you came to run three lines and
leave, you never need to touch any of them.

The two sides mean different things. The left is your project: the files
in it, and the values your code has made. The right is everything outside
your project: things you look up, and things you change.

**Workbench**, on the left, holds your files, your variables and your
notes. **Library**, on the right, is everything you look *up*.
**Settings** is what you change. The Workbench has the left edge to
itself, so you can keep a definition open beside your own files. Library
and Settings share the right-hand edge, so opening one closes the other.

Almost every code editor you meet after this one puts your files on the
left, so the habit carries over.

On a wide enough screen, opening a panel shrinks the working area rather
than covering it, so your cells stay visible. Drag a panel's inner edge
to resize it. Whatever you leave open is still open when you come back.
**Esc** closes a panel. Clicking your own code never closes one, so a
reference you opened to read while writing stays put.

On a phone, panels slide up from the bottom instead.

### Library

**Reference** holds every term, function and operator that any dewlab
tutorial introduces, in one searchable list. Each entry names the
tutorial that introduced it. This reference shows everything. A tutorial page's own reference shows
only what you have been taught so far. In a workspace with no tutorial
attached, there is no "so far" to go by.

Search it, or narrow it with the buttons above the list:

- **Maths** and **Computing**, from the modules a term's tutorial
  belongs to. A tutorial that covers both is filed under both.
- **Beginner**, **Intermediate** and **Advanced**, from how many layers
  of groundwork sit under what that tutorial teaches. Nothing here is
  labelled by hand. The level is read off the topic map, so it stays
  true to the map rather than to whoever last updated a label.
- **Topics** folds open for the broader groupings (trigonometry,
  matrices, simulation, and so on), and **kind** for concepts,
  functions, operators, formulas and keywords.

Each button says how many terms it would leave, so a button that would
empty the list tells you before you press it. Picking two in the same
row means *either* of them. A term from a tutorial that claims no
outcomes is filed under **Unfiled**, and is never hidden.

**Data** holds real datasets you can load. Each one says where it came
from and what licence it carries. Pick one and it writes a working cell
into your notebook.

Some datasets are already in dewlab. Others are fetched from the web
when you run the cell, which needs a connection and needs that site to
allow the request. If the site does not allow it, the error says so. It also tells you
what to do instead: download the file and add it through Files.

The rest of the Library is what used to be **Help**. It covers how
cells work, the keyboard shortcuts, what a cell can call, and how your
work is kept.

### Workbench

**Variables** shows what is in your Python session right now: every
name, its type, and a short summary of its value. The summary says how
many rows a table has, how many items a list holds, or what a number is.
It updates every time you run a cell, which answers "did that work?"
without printing everything twice. Functions and modules fold away under
their own line, so your own variables stay at the top.

**Your notes** is a place to write down anything worth remembering as
you work. It stays with this browser rather than with any one
notebook.

**Files** is a real filesystem a cell can read from and write to. Your
open notebooks list here too, so you can always see where they are. A
notebook lives in this browser, not as a file. "Keep a copy" in
Settings saves one as a real file.

By default it is private storage inside your browser, which you cannot
see from outside. **Use a folder on my computer** switches to a real
folder instead, in a browser that supports it, such as Chrome or Edge.
Files a cell writes then appear on your computer where you can find
them. That covers a `sqlite3` database a cell creates, a chart a cell
saves to disk, and anything else `open()` can write.

This is where a cell writes by default. `open("notes.txt", "w")` in a
cell puts the file here, beside everything else, with no path in front of
the name.

**New file…** starts an empty Python file and opens it. **Add a file…**
brings an existing file in from your device. The list below shows what is
there. Click a name to open it, use **Rename** to change it, and the
cross to delete it.

A `.py` opens as a file, so you see the thing you are learning to write.
A `.ipynb` opens as cells, because that format carries the results each
one produced. A `.html` opens as a small website. Its matching `.css` and
`.js` files open beside it, and the page updates as you type. Editing any
of these saves straight back to its file. Other kinds of file stay in the
list for a cell to read, since dewmini would have to guess how to show
them as code.

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

**Python** shows how Python is currently running. It usually runs in a
background worker, which is what lets a runaway cell be stopped without
freezing the page. On a browser or setting where a background worker is
not available, it runs directly in the page, and a runaway cell cannot
be stopped.

**Restart Python** starts over with a clean interpreter. Everything a
cell has defined so far is discarded, and your cells and their code are
untouched. **Restart & run all** next to it does both steps: first a
clean interpreter, then every cell run in order from the top. That is
how you check a notebook still works from scratch, rather than only from
wherever you left it.

Below those, the **Run time** switch turns the small "ran in…" line
under a cell's output on or off.

**Keep a copy** starts with the name of the notebook you are looking
at. That name is also its tab's name, and the name every download below
uses.

From here you can download the notebook as a Python file, a standalone
HTML page or a Jupyter notebook. You can print it, or save it as a PDF,
with the code and its output and none of the page's own header and
buttons. You can also load a `.ipynb` or `.py` file back in, whether it
came from here or from anywhere else, and carry on with it.

An import **opens in a new tab**, so it never lands on top of what you
were doing. A `.py` file that dewmini exported comes back exactly as it
was, cell by cell, text cells included. A plain `.py` script with no
markers comes back as one Python cell.

A notebook written outside dewmini can bring along things this Python
cannot run. A `tkinter` window, a Jupyter "magic" command and a `!pip
install` shell line are the common ones. A warning banner appears straight after the
import and names which imported cell each one is in.

Four ready-made examples sit below that import button. Each brings its
own real data and opens in its own tab:

- **SQL & Our World in Data**, using `sqlite3` and `run_query()` against
  real CO₂ emissions data
- **a mini data investigation**, asking whether life expectancy has
  converged worldwide since 1950
- **a fun math problem**, estimating π by throwing random darts
- **word frequency: usual or unusual?**, checking a real novel against
  Zipf's law

Each one is a runnable dewlab tutorial in miniature.

**Practice** holds the order switch described above.

**Texture** holds the same reading preferences every dewlab page has:
theme, font, text size, page width and link color. A choice you make
here follows you to the tutorials, and a choice you make on a tutorial
page follows you back here.

**Editor** holds the settings for a page you write code on rather than
read. You can set how large the code is and how much room a cell gives
itself. You can also set how heavy the cursor looks, and whether line
numbers and the current line's highlight appear. A cell's spacing can be
compact, cozy or relaxed. None of this changes how the code runs, only
how it looks.

---

## Keeping your work

Everything you type in dewmini saves to the browser you typed it in, as
you type it. Nothing you write leaves your browser, and nothing is
scored.

Your work therefore stays on that one browser and that one device. To
move it somewhere else, use one of the downloads in Settings. If what
you want to keep is a file a cell wrote, use the Workbench's Files
section and its "use a folder on my computer".

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
  internet connection the first time you open it, because that is when
  it fetches Python. After that it works without one.
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

The link under dewmini's own title, "downloadable copy of dewmini
itself", gets you the whole tool as a zip. Unzip it and it works the
same as it does online. The copy you download already includes Python,
so it needs no internet connection at all.

That suits a classroom with no reliable connection. It also suits
keeping a copy that will work the same next year, whatever the hosted
site looks like by then.

It needs one step the online version does not. After unzipping, open a
terminal in the folder and run `python3 serve.py`, rather than
double-clicking `index.html`. A modern browser will not let a page
opened straight off disk load its own JavaScript the way dewmini needs
to. *serve.py* starts a small local server and opens the right page for
you, and it needs nothing installed beyond the Python already running
it. Leave that terminal window open
while you use dewmini; closing it stops the server.
