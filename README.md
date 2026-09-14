# dewlab

dewlab turns a markdown file into a web page where learners read an
explanation, edit the Python underneath it, and run it. The Python runs inside
the browser tab, on the learner's own machine. Nothing is installed, nothing is
submitted, and nothing is scored.

It exists to remove the first-week cost of teaching programming. Instead of an
hour spent installing an interpreter, an editor and a package or two across
four operating systems, a learner opens a link and starts writing Python.

The live site is at **[deweydex.github.io/dewlab](https://deweydex.github.io/dewlab)**.

---

## Where to go next

This page is an overview. The detail lives in one document per reader, so you
only have to read the one that matches what you are here to do.

| If you want to… | Read |
|---|---|
| Use a tutorial | [`docs/FOR_STUDENTS.md`](docs/FOR_STUDENTS.md) |
| Find an answer about getting started | [`docs/FAQ.md`](docs/FAQ.md) |
| Write or edit a tutorial | [`docs/WRITING_TUTORIALS.md`](docs/WRITING_TUTORIALS.md) |
| Change the code | [`CONTRIBUTING.md`](CONTRIBUTING.md), then [`ARCHITECTURE.md`](ARCHITECTURE.md) |
| Report a mistake or a bug | [`docs/REPORTING_A_PROBLEM.md`](docs/REPORTING_A_PROBLEM.md) |
| Use the standalone Python workspace | [`docs/DEWMINI.md`](docs/DEWMINI.md) |
| Decide whether to teach with dewlab | keep reading here |

---

## What dewlab does

**Tutorials that run.** A tutorial is prose with editable Python cells set into
it. A cell shows whatever the code printed, the value of its last line, a table
drawn as a table and a chart drawn as a picture — and if something goes wrong,
an error trimmed down to the learner's own line. Cells on one page share their
variables in order, the way a notebook does. Pages start fresh, and share
nothing with each other.

**Work saved in the browser.** Everything a learner writes is saved in their
own browser, keyed to the tutorial and its version. Close the tab, come back
next week, and the code and its last output are still there. Nothing is scored
and nothing leaves the machine. The work stays on that device — it will not
follow them to a different computer, and clearing browser data will clear it.

**A reading surface a learner can adjust.** A dock in each top corner holds
the page's controls. The left holds Reference and Where You Are, a trail
from every tutorial down to this page's own sections. The right holds five
panels — Notes, Report, Python, Appearance, and Imports & Exports — where
theme, typeface, text size, line width and link colour live. Panels are
resizable and stay open while a reader moves through a series; on a phone,
everything collapses into one launcher at the bottom of the screen.

**Practice beside every tutorial.** Each tutorial has a practice page of
problems, with hints and answers behind folds so a stuck learner gets a route
before an answer. Mixed problem sets draw on several tutorials at once.

**Ways to take it away.** A tutorial can be downloaded as one HTML file that
works by double-clicking it, printed or saved as PDF, or saved as a Jupyter
notebook. A whole series downloads as a zip.

**Cells a reader adds themselves.** On any page with cells, a reader can add
their own Python or a text note under any cell, and share one as a small file
someone else can load. Those stay separate from the tutorial's own saved work,
so a tutorial update leaves them alone.

**Three ways to find something.** Tutorials are listed in teaching order on the
contents page, which also has a search box. The topic tree maps every topic in
the course descriptors by what has to come first, and marks the ones dewlab
does not teach yet. Browse by topic gathers everything on one subject in one
place.

**A Python workspace with no tutorial attached.** dewmini is a blank page for
trying a few lines out, with a file manager, uploads, SQLite, notebook import,
and a Stop button that interrupts code that is stuck, all in its own smaller,
quieter shape.

**Coverage you can check.** Each tutorial declares which learning outcomes it
teaches, per section. The build refuses to accept a section that does not
exist, and a generated map reports every outcome nobody has written for yet.

---

## How the site is put together

`build.py` reads the markdown in `tutorials/`, renders each file into the page
template at `assets/shell.html`, and writes a plain static site into `site/`.
There is no server and no database. Publishing is a build: GitHub Actions runs
the same command on every push to `main` and deploys the result to GitHub
Pages, so a published page cannot drift from the markdown it came from.

In the browser, `assets/tutorial-runtime.js` starts Pyodide — a build of real
CPython compiled for the browser — mounts a CodeMirror editor into each cell,
and runs cells against it. On the hosted site Python runs in a Web Worker, off
the page's own thread, which is what makes a real Stop button possible.
Everything a learner's code can call beyond ordinary Python is defined in
`assets/tutorial_tools.py`.

```text
tutorials/       one folder per module, then one folder per tutorial
setup/           setup snippets tutorials pull in with {{include: ...}}
data/            shared CSV datasets
assets/          the page template, styles, runtime, editors, and vendored libraries
compose/         dewmini, the smaller Python workspace
dewmark/         the exam track — specifications for authoring, sitting, and marking exams
build.py         markdown in, site/ out
dev/             maintainer scripts, including the curriculum map generator
tests/           unit tests, browser tests, and a manual checklist
docs/            reader documentation, plus one <file>-explained.md per code file
planning/        design notes, decision records, and the curriculum data
```

[`ARCHITECTURE.md`](ARCHITECTURE.md) covers all of this properly: the build
stage by stage, what the browser does, how the authoring editor talks to
GitHub, and where to start reading for a given kind of change.

---

## Running it on your own machine

Learners need none of this. It is for authors and contributors. You need
Python 3.12 or later.

```sh
git clone https://github.com/deweydex/dewlab
cd dewlab
pip install -r requirements-build.txt
python3 build.py --clean
python3 -m http.server -d site 8000
```

Then open `http://localhost:8000`. The built site in `site/` is never
committed; it is regenerated on every push.

Downloadable copies are the slow part of a build, so
`python3 build.py --no-standalone` skips them while you are working on
content. Run the tests with `python3 -m pytest`.

---

## Where the project stands

The reading and running experience, practice pages, versioned releases,
curriculum coverage, the topic tree, both Python workspaces, the authoring
editor and the build-and-publish pipeline are all built and live.

The curriculum spans six accredited QQI modules — *Mathematics for IT*,
*Programming and Design Principles*, *Computational Methods and Problem
Solving*, *Fundamentals of Object-Oriented Programming*, *Database Methods*
and *Web Authoring* — across 116 tutorials and 60 practice pages, covering
every learning outcome that doesn't call for a tool outside the project.

---

## Get involved

dewlab is open to anyone who wants to learn from it, teach with it, or help
build it.

- **[Try a tutorial](https://deweydex.github.io/dewlab)** — no install, no
  account, just a browser.
- **Teach a class with it** — welcome; [`LICENSE.md`](LICENSE.md) has the one
  thing to do first.
- **Found a mistake, or something that doesn't work?**
  [`docs/REPORTING_A_PROBLEM.md`](docs/REPORTING_A_PROBLEM.md) covers the
  fastest way to flag it — every page has a link at the foot for exactly
  this.
- **Want to write or improve a tutorial?** Start with
  [`docs/WRITING_TUTORIALS.md`](docs/WRITING_TUTORIALS.md).
- **Want to work on the code?** [`CONTRIBUTING.md`](CONTRIBUTING.md) has the
  setup, then [`ARCHITECTURE.md`](ARCHITECTURE.md) for how it fits together.
- **Have a question, or a decision you'd make differently?** Raise it in
  [`QUESTIONS.md`](QUESTIONS.md), or open a GitHub Discussion.

---

## Licence

See [`LICENSE.md`](LICENSE.md). Reading and learning from the material is free;
adapting it asks for credit, and using it with a class asks that you get in
touch first.
