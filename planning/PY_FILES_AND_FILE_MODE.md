# Python files in dewmini

Students who are learning to program eventually have to stop writing code in
cells and start writing it in files, and then to spread one program across
several files that call each other. dewmini supports the first of those
activities. It does not yet support the second.

This document describes the work that is left: showing a notebook as a file,
turning the Files panel into a file manager, and moving notebooks out of
browser storage into the workspace. It also settles a related question that
comes up as soon as files are involved: whether the tutorials themselves
should be written as Python files rather than as markdown documents.

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

## Where this starts from

Three things are already in place, and the work below assumes them.

A notebook can be written out as a Python file and read back, using the
percent format: `# %%` before a code cell, `# %% [markdown]` before a text
cell. The workspace is on Python's import search list, so one file in it can
import another. A `.ipynb` file written or read by dewmini carries the outputs
of its cells.

Two things are not in place. Notebooks live in `localStorage`, the browser's
own small key-value store, and not in the workspace. And there is no way to
see a notebook as a file, or to manage the files in the workspace beyond
uploading and deleting them.

---

## Part 1: Showing a notebook as a file

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

---

## Part 2: The file manager, and where the panels go

To work with more than one file, a student needs to see which files exist and
open one of them.

The Workbench panel on the right of the screen already has a Files section,
but it is an inventory rather than a browser. It lists names and sizes, and
offers to upload a file or delete one. It has no way to open a file for
editing, create a new one, or rename one. Those three additions are most of
the work.

**The file manager belongs on the left**, and this decision changes what each
side of the screen is for.

`DEWMINI_WORKBENCH.md` §2 divided the two panels by ownership: the right-hand
panel held a student's own work and the left-hand panel held things they
consulted. That division put files on the right and the variable list on the
right, and put the reference glossary on the left.

The division that replaces it is by subject. **The left-hand panel describes
the project the student is working on: where they are in it, what files it
contains, and what values its code has produced. The right-hand panel holds
what is outside the project: reference material and settings.** So the left
holds the table of contents, the file manager and the variable list, and the
right holds the glossary and the settings.

Three things recommend this arrangement. Nearly every code editor a student
will meet afterwards puts a file tree on the left, so the habit transfers.
Files and the table of contents answer the same question — what is in this
piece of work — and belong beside each other rather than on opposite sides.
And the variable list is read while looking at the code that produced it,
which makes it part of the project rather than a thing consulted about it.

The cost is that the variable list and the glossary each move to the other
side, which invalidates the parts of `DEWMINI_WORKBENCH.md` §2 and of the
existing browser tests that name a panel's side. The move is worth doing as
part of building the file manager rather than on its own, because on its own
it rearranges the screen without adding anything a student can use.

---

## Part 3: Notebooks become files in the workspace

A notebook is saved as a Jupyter notebook file, a `.ipynb`, in the workspace.

That format is chosen over a format designed here because a format designed
here could be read only by software written here. A student who wanted to hand
a notebook to a teacher, open it on a university machine or put it in a
repository would find that nothing else opened it. dewlab would also have to
write and maintain a reader, a writer and a set of round-trip tests for a
format offering nothing the published one does not.

The reason to want a format of our own is to store things nbformat does not
describe: how long a cell took to run, whether its output is older than its
code, the name shown on its tab. nbformat already provides for this. Every
notebook and every cell carries a metadata object, and the specification
requires a tool to preserve metadata keys it does not recognise rather than
discard them. **dewmini keeps its own information under a `dewmini` key inside
that object**, and the file remains a valid Jupyter notebook that other
programs open normally. There is nothing left for a new format to do.

### Both formats stay, doing different jobs

A `.ipynb` file is a notebook: cells, and the outputs they produced. A `.py`
file in percent format is a program: code that another file can import, with
no outputs in it. A student writing a module they will import writes a `.py`
file. A student keeping a piece of work together with its results keeps a
`.ipynb` file.

Saving a notebook as a `.py` file remains available and remains useful, and
dewmini says in one line, at the moment it writes the file, that the outputs
are not in it. The message belongs there rather than in a dialogue box asking
for confirmation, because the student has not made a mistake and does not need
to be stopped.

### What has to be answered before this is built

Of the three storage backends the workspace filesystem can use, one of them,
IDBFS, writes to permanent storage only when it is explicitly told to. A
notebook lost because that step did not happen would be a worse failure than
any problem this change solves. Before notebooks move out of `localStorage`,
the check recorded in `tests/MANUAL_CHECKLIST.md` — that a file written to the
workspace survives a reload on each backend — has to pass on a real machine.

---

## Part 4: Tutorials stay markdown documents

The tutorials are markdown files that `build.py` turns into pages. A
reasonable question, once dewmini can work in Python files, is whether they
should be Python files too, in the same percent format the workspace uses.

They should not, and the reason is what the files mostly contain. Across 91
tutorial files there are 6,076 lines of code and 17,306 lines of prose. A
tutorial is a piece of writing with code set into it, not a program with
comments. Storing it as a Python file would put three lines out of every four
inside a comment block, where no editor helps with them and the structure of
the document disappears.

The people who would pay for the change are the ones writing tutorials, and
they are writing prose. What is wanted instead is a way to move a piece of
work in either direction: a notebook a teacher has made becomes the starting
point for a tutorial, and a tutorial's cells open in dewmini as a notebook.
`dev/from_notebook.py` does the first of those already.

---

## Part 5: The work, in order

Each step is useful on its own, so the work can stop after any of them.

| Step | What it does | Rough size |
|---|---|---|
| 1 | Add the file view, extend the Files panel into a file manager, and move the panels to the sides Part 2 settles | One to two weeks |
| 2 | Let a tutorial carry a `workspace` folder, opened automatically | Small |
| 3 | Store notebooks in the workspace as `.ipynb` files | Medium, and blocked on the manual check in Part 3 |
| 4 | Write the tutorials that use all of it | Content work |

Step 2 does not depend on the others and can be done at any point. A
tutorial's `workspace` folder opens in dewmini by itself, which is a
deliberate exception to the rule in `DEWMINI_WORKBENCH.md` §1 that nothing
opens on a first visit. That rule exists so a student is not met with panels
they did not ask for. A workspace folder is not a panel: it is the material
the tutorial's own instructions refer to, and a student who has to find and
open it before the first instruction makes sense has been given a task that
teaches nothing.

Step 4 should follow the database module's learning outcomes being written,
since those determine what the tutorials need to demonstrate.

**Step 1 is much larger than the rest, and most of its cost is not the visible
interface.** It is that a tab currently holds a notebook, and would have to
hold either a notebook or a file. Anything reading or writing a tab's contents
would be affected. Before starting, someone should write down what a tab
holds. If that is described as a document with storage behind an interface,
rather than as JSON in `localStorage`, then step 3 becomes a change in one
place instead of everywhere.

The project view is designed after all of the above is in place, not alongside
it, because what a project view should show depends on what a project turns
out to be.

### Code that can be deleted

`migrateLegacyCells()` and `LEGACY_CELLS_KEY` in `compose/dewmini.js` convert
saved work from an earlier version of dewmini into the current format. dewlab
has not been released, so no saved work in that earlier format exists. The
function, the storage key it reads, and the test
`test_work_saved_before_tabs_is_migrated` can all be removed without losing
anything.

---

## What this document does not settle

**Whether the workspace filesystem is reliable enough to hold a student's
notebooks.** Part 3 explains why this has to be answered before notebooks
leave `localStorage`, and what test answers it.

**What a tab holds.** Part 5 argues that this should be written down before
the file view is built. It is a design question rather than an open choice,
but nothing else in Part 5 is safe to start until someone has answered it.

---

*Figures in Part 4 were measured from the repository, not estimated: 91
tutorial files, 646 executable code blocks, 211 non-executable code blocks,
6,076 lines of code, 17,306 lines of prose.*

*Names such as shapes.py refer to files a student would create. They are
written without backticks because `dev/check_doc_links.py` treats a backticked
filename as a claim that the file exists in this repository.*
