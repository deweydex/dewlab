# Python files in dewmini

Students who are learning to program eventually have to stop writing code in
cells and start writing it in files, and then to spread one program across
several files that call each other. dewmini supports the first of those
activities well. It does not support the second at all.

This document explains what dewmini does today, what would have to change, and
in what order the work could be done. It also settles a related question that
comes up as soon as files are involved: whether the tutorials themselves
should be written as Python files rather than as markdown documents.

Nothing described here has been built.

---

## Terms used in this document

**dewmini** is dewlab's Python workspace: a page at `compose/dewmini.html`
where a student writes and runs Python in the browser. It is separate from the
tutorial pages, although the two share the code that runs Python.

A **cell** is one editable box of code or text. A student runs a code cell and
its output appears underneath it.

A **notebook** is an ordered list of cells that dewmini shows as one document.
A student can have several notebooks open at once, one per tab.

The **workspace** is a folder of files belonging to the student. dewmini
mounts it inside Python at the path `/mnt/dewmini`, so Python code can read
and write files there. Data files a student uploads go here.

To **import** a file means to load the Python code in another file so that the
functions defined there can be called. Python spells this `import shapes`,
where `shapes` is the name of a file called shapes.py.

---

## What dewmini does today

Four facts matter for everything below.

**Notebooks are stored as text in the browser, not as files.** They live in
`localStorage`, the browser's own small key-value store, under the key
`dewmini:notebooks:v1`. Each cell is saved with both its code and the output
it last produced.

**The workspace filesystem is complete.** `compose/dewmini-fs.js` can list a
directory, read a file, write a file, delete a file and create a folder. It
does this across three different storage backends, choosing whichever the
browser allows.

**A notebook can be exported as a Python file, and read back.** The exported
file separates cells with comment lines that dewmini invented:
`# ---- cell 1 ----` before a code cell and `# ---- note ----` before a text
cell. `downloadAsPython()` writes them and `parsePyCells()` reads them, both in
`compose/dewmini.js`.

**No file in the workspace can import another.** Python looks for importable
files in a list of directories called `sys.path`, and nothing adds the
workspace to that list. A student can therefore have two Python files and no
way to use one from the other.

---

## Part 1: How cells should be marked in a Python file

A Python file is a flat sequence of lines. A notebook is a list of separate
cells. To store a notebook as a Python file, the file needs some way of
recording where one cell ends and the next begins, and that marker has to be
something Python ignores. A comment is the only option.

dewmini's current markers work, and they explain themselves: a reader who has
never seen one can guess what `# ---- cell 1 ----` means. No other program
understands them.

### The percent format

There is an established convention for the same job, usually called the
percent format. A code cell begins with a line containing `# %%`. A text cell
begins with `# %% [markdown]`, and its prose follows as ordinary `#` comment
lines. A short example:

```python
# %% [markdown]
# Reading a file of marks, and averaging them.

# %%
marks = [72, 65, 88]
sum(marks) / len(marks)
```

Jupytext, Visual Studio Code, Spyder and PyCharm all read this convention.
A file written this way is ordinary Python, so `python thing.py` runs it, and
it is also a notebook, so those editors show it as a sequence of cells.

### Recommendation, and the cost of it

dewmini should adopt the percent format.

The reason is that a student who writes a file in dewmini can open the same
file, unchanged, in Visual Studio Code on a college machine, and see the same
cells. Teaching a student to work in files is only worth doing if the files
they produce are usable somewhere other than the tool they were taught in.

There is a real cost, which is that `# %%` explains nothing. A beginner
reading it has no way to work out what it means, where the current markers are
almost self-explanatory.

Two things reduce that cost. The first is that a student working inside
dewmini need never see the marker: when dewmini displays a Python file it can
draw the markers as dividing lines between cells, which is what Visual Studio
Code does. The marker is only visible if the student opens the file in a plain
text editor. The second is that an exported file can begin with a few lines of
explanation, written as a markdown cell, saying what the markers are for. A
student can delete those lines once they no longer need them.

### Prose belongs in comments, not in strings

Python has a second way to put text in a file that it will not execute: a
string on a line by itself, usually written with triple quotes. This is a
worse choice than a comment for two reasons. Such a string is a real value
that Python creates and discards, so it is not truly inert. And a string in
the first position in a file becomes that file's docstring, which is a
documented feature that would then be doing something the author did not
intend. Comment lines have neither problem.

### What the change involves

The writer, `downloadAsPython()`, emits the new markers. The reader,
`parsePyCells()`, matches them. Two comments describing the old format need
updating. That is the whole change.

One piece of work should come first. Neither `downloadAsPython()` nor
`parsePyCells()` has any test, in `tests/test_build.py` or in `tests/e2e/`, so
the behaviour being changed is currently unprotected. A test that builds a
notebook, exports it, imports it again and compares the result would establish
what the code does before anyone alters it.

---

## Part 2: Letting one file import another

This is the smallest change that addresses the difficulty students actually
have, which is not writing a function but calling a function that lives in
another file.

The workspace is mounted at `/mnt/dewmini`, and Python only imports from
directories listed in `sys.path`. Adding that one path when Python starts
makes every Python file in the workspace importable. The change itself is a
single line.

### The problem that has to be solved alongside it

Python remembers every module it has already imported, in a record called
`sys.modules`. When a program imports the same module a second time, Python
finds it in that record and returns it without reading the file again. This
behaviour is deliberate: it stops a large program from reading the same file
dozens of times.

It also produces a specific and confusing failure for a student. Suppose a
student writes a file shapes.py containing a function that calculates an
area, imports it in a cell, and calls it. The answer is wrong. They open
shapes.py, find the mistake, correct it, and run the cell again. They get the
same wrong answer, because Python did not read the corrected file. Nothing on
screen has changed and nothing explains why.

There are three ways dewmini could handle this.

It could **tell the student**. When a file that has been imported changes on
disk, dewmini shows a message saying so and offers to reload it. This is the
recommended option. It is the only one of the three that leaves the student
knowing something true about how Python works, and module caching is a
behaviour they will meet in every other Python environment.

It could **reload silently**, re-importing any changed file before running a
cell. This removes the friction and teaches nothing, and the first time the
student uses Python outside dewmini the problem returns with no explanation.

It could **restart Python** whenever a file changes. This is correct and far
too slow for a one-character edit.

---

## Part 3: Showing a notebook as a file

A student who is learning to write Python files needs to see one. dewmini
should therefore be able to show the same document in two ways: as a notebook,
which is a list of cells, or as a file, which is one continuous piece of text.

### Why both views are needed

An empty file is harder to begin than an empty cell. Faced with a blank page,
a beginner has to decide what the whole program will be before writing
anything. A cell asks for one line. Much of why notebooks suit teaching comes
from that difference, so removing the notebook view in favour of the file view
would make dewmini harder to start with, not easier.

Keeping both means a student can begin in cells and move to a file when they
are ready, without changing tools or losing their work. Because a
percent-format file is both things at once, switching between the views does
not convert anything. It changes how the same text is displayed.

### Which view is showing should be visible

A tool that behaves differently depending on a setting the user cannot see is
a tool people get lost in. The current view should be shown on the tab itself,
where it is always in sight, rather than only in a menu.

### Running in each view

The Run action means something different in each view. That difference should
be made obvious to the student rather than hidden, because it is one of the
things the file view exists to teach.

In the notebook view, Run executes one cell, and the output appears under that
cell. This is what dewmini does now.

In the file view, Run executes the whole file from top to bottom, as running
`python thing.py` at a command line would, and the output appears in one place
for the file. This is the point of the view: a file always runs in the order it
is written, and a notebook does not.

### The file manager

To work with more than one file, a student needs to see which files exist and
open one of them.

The Workbench panel on the right of the screen already has a Files section,
but it is an inventory rather than a browser. It lists names and sizes, and
offers to upload a file or delete one. It has no way to open a file for
editing, create a new one, or rename one. Those three additions are most of
the work.

The panel could sit on either side of the screen. `DEWMINI_WORKBENCH.md` §2
established that the right-hand panel holds a student's own work and the
left-hand panel holds things they consult, which puts files on the right. Most
code editors put a file tree on the left. Keeping it on the right is the
smaller change and is consistent with the existing arrangement, and the tabs
already provide a way to move between open files, so a tree is only worth
adding once there are folders or a large number of files. Whoever teaches with
dewmini should make this call after watching students use it.

---

## Part 4: Where notebooks are stored

This part can be deferred, but the decision affects how Part 3 should be
built, so it should be made knowingly rather than by default.

At present a notebook is a block of JSON text in `localStorage`, and the
workspace is a separate filesystem. A notebook is therefore not a file, and
the list of notebooks and the list of files are two different lists of two
different kinds of thing.

An alternative is to store each notebook as a percent-format Python file in
the workspace. The consequences are substantial. The file manager and the tab
strip would show the same items. Switching to the file view would require no
conversion, because the notebook would already be a file. Importing one
notebook from another would work without further changes, because they would
be ordinary Python files in a directory Python can import from. A student's
work would be a folder of Python files they could hand to anyone.

Two things stand in the way.

The first is that a Python file has nowhere to record the output a cell
produced. dewmini currently saves outputs with the cells and restores them
when the page reloads. Storing notebooks as files would mean either keeping
outputs in a second file alongside each notebook, or accepting that they are
lost. Losing a student's outputs would make dewmini worse than it is now, so
this has to be settled first.

The second is reliability. Of the three storage backends the filesystem can
use, one of them, IDBFS, only writes to permanent storage when it is
explicitly told to. A notebook lost because that step did not happen would be
a more serious failure than any problem this change solves.

### A defect in the current storage worth fixing regardless

`saveState()` writes every notebook, every cell and every saved output into
`localStorage` as a single block of JSON, inside a `try` with an empty
`catch`. Browsers limit `localStorage` to roughly five megabytes. A student
whose notebooks contain a few images or a large table can exceed that limit, at
which point the write fails, the failure is discarded without being reported,
and the student's work stops being saved with nothing on screen to indicate it.

This is a defect in code that is already running, independent of anything else
in this document.

---

## Part 5: Tutorials stay markdown documents

Once dewmini can show Python files, a reasonable question follows: should the
tutorials be written as Python files too, rather than as markdown documents
with code blocks in them?

They should not. The case rests on what the tutorials contain and on who does
the writing.

### What the tutorials contain

Across the 91 tutorial files there are 6,076 lines of code and 17,306 lines of
prose. Close to three quarters of the material is writing. Written as Python
files, those 17,306 lines would all become comments, which is a worse format to
write, review and compare versions of, for the majority of what a tutorial is.

The tutorials also contain 646 executable code blocks and 211 code blocks that
exist to be read rather than run. `first-steps.md` teaches this distinction
explicitly: "Not every piece of code on a page is meant to be run." A Python
file offers no way to keep it. Code in a Python file either runs or is
commented out, and neither corresponds to a block that is displayed as code but
never executed.

### Who would pay

Two people write the tutorials, and they would bear the entire cost. The
authoring editor, `assets/editor.js`, is 1,235 lines built on Milkdown for
editing markdown with live mathematics and code blocks. Written as Python
files, the tutorials could not be edited with it.

Students would gain nothing, because students never read the tutorial source.
They read the built HTML page.

### What is needed instead

The real requirement is not that tutorials be written in Python. It is that a
tutorial be able to hand a student a set of Python files, so that a lesson
about importing can ship the two files the lesson is about.

Each tutorial already lives in its own folder, alongside its practice page and
its glossary. One additional convention would be enough:

```
tutorials/database-methods/joining-tables/
    joining-tables.md
    joining-tables.glossary.yaml
    workspace/
```

`build.py` copies the `workspace` folder alongside the built page, and the page
offers to open those files in dewmini. The tutorial remains a document, written
in markdown by people who are writing mostly prose. The lesson about files
ships actual files, in the percent format, which the student opens and edits.

---

## Part 6: The work, in order

Each step below is useful on its own, so the work can stop after any of them.

| Step | What it does | Rough size |
|---|---|---|
| 1 | Adopt the percent format for exported and imported Python files | Half a day |
| 2 | Add the workspace to `sys.path` and handle module caching | One day |
| 3 | Add the file view and extend the Files panel into a file manager | One to two weeks |
| 4 | Let a tutorial carry a `workspace` folder | Small |
| 5 | Write the tutorials that use it | Content work |

Step 1 comes first because it is small, independent, and every later step
writes files in that format. Step 2 follows because it is the smallest change
that lets a student do the thing they currently cannot, and it does not require
any new interface.

Step 4 does not depend on the others and can be done at any point.

Step 3 is much larger than the rest, and most of its cost is not the visible
interface. It is that a tab currently holds a notebook, and would have to hold
either a notebook or a file. Anything reading or writing a tab's contents would
be affected. Before starting, someone should write down what a tab holds. If
that is described as a document with storage behind an interface, rather than
as JSON in `localStorage`, then the change described in Part 4 later becomes a
change in one place instead of everywhere.

Step 5 should follow the database module's learning outcomes being written,
since those determine what the tutorials need to demonstrate.

### Code that can be deleted

`migrateLegacyCells()` and `LEGACY_CELLS_KEY` in `compose/dewmini.js` convert
saved work from an earlier version of dewmini into the current format. dewlab
has not been released, so no saved work in that earlier format exists. The
function, the storage key it reads, and the test
`test_work_saved_before_tabs_is_migrated` can all be removed without losing
anything.

---

## Part 7: Decisions still open

**Where do cell outputs live if a notebook becomes a file?** They could be
kept in a second file stored beside each notebook, or they could be discarded
when the page reloads. This question determines whether the change described
in Part 4 is possible at all, and it should be answered before Step 3 is
designed.

**Should notebooks be stored as files at all?** Part 4 sets out what this
would simplify and what it risks. It cannot be decided until the previous
question has an answer.

**Should the file manager be on the left or the right?** Part 3 gives the
argument for each side. Whoever teaches with dewmini should decide this after
watching students use it.

**Should a tutorial's `workspace` folder open in dewmini automatically, or
when the student asks for it?** Opening it automatically is easier for the
student. Waiting until asked keeps the existing rule that nothing opens by
itself on a first visit, described in `DEWMINI_WORKBENCH.md` §1.

---

*Figures in Part 5 were measured from the repository, not estimated: 91
tutorial files, 646 executable code blocks, 211 non-executable code blocks,
6,076 lines of code, 17,306 lines of prose.*

*Names such as shapes.py refer to files a student would create. They are
written without backticks because `dev/check_doc_links.py` treats a backticked
filename as a claim that the file exists in this repository.*
