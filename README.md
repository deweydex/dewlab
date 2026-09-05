# dewlab

dewlab brings explanations, maths, and Python code together on a web page.
Learners can read about an idea, change an example, and run it in their
browser. The tutorials need no account or software installation.

The [tutorials page](https://deweydex.github.io/dewlab/) is the place to
begin learning. This README is an overview for teachers and contributors.

We use small examples to explore an idea before naming it. Hints, worked
answers, and earlier explanations give learners ways to continue when a
step is unclear. Tutorial and practice answers are not graded by dewlab.

## Where to go next

| What you want to do | Where to read |
|---|---|
| Use a tutorial | [Using dewlab](docs/FOR_STUDENTS.md) |
| Find an answer about getting started | [Frequently asked questions](docs/FAQ.md) |
| Write or edit a tutorial | [Writing a tutorial](docs/WRITING_TUTORIALS.md) |
| Change the site's code | [Contributing](CONTRIBUTING.md), then [Architecture](ARCHITECTURE.md) |
| Report a mistake or unclear explanation | [Reporting a problem](docs/REPORTING_A_PROBLEM.md) |
| Run Python outside a tutorial | [dewmini](docs/DEWMINI.md) |
| Consider using dewlab in a class | This overview and the [licence](LICENSE.md) |

The [pedagogical style guide](planning/PEDAGOGICAL_STYLE_GUIDE.md)
explains how tutorials are written and why. The
[plain-language review record](planning/PLAIN_LANGUAGE_PASS.md) describes
the work completed and what still needs review. The
[planning index](planning/README.md) links to design notes and decisions.
[CLAUDE.md](CLAUDE.md) gives repository instructions for coding assistants.

## What dewlab offers

**Examples learners can change.** A cell is a code box with a Run button.
The result appears below it as text, a number, a table, or a chart.
An error message helps identify something that did not work. Cells on a
page share the values created by running code, in the order they run.
Each tutorial has its own Python session.

**Work saved in the browser.** Edits to the tutorial's cells, notes, and results
are saved when browser storage is available. Large results may be left
out if storage is full. A saved result does not restore Python's values;
the code needs to run again in a new session. Clearing browser data
removes the saved work.

**Reading settings.** Learners can change the colours, font, text size,
line width, and link colour. Reference, Series, and Settings open beside
the reading on a wide screen, or at the bottom on a phone.

**Practice with support.** Many tutorials have a practice page with
hints and worked answers. Learners can try an idea, open a hint, or read
an answer. Mixed practice sets bring several topics together.

**Ways to keep a copy.** Export a copy saves code, results, and notes
as a file. Load a copy opens that file in the same tutorial. Download
to keep provides the published reading and starter code, separately from
current edits. A page can also be printed or saved as PDF.

**Space for learners' own examples.** On pages with runnable cells,
learners can add Python cells or text notes. These are saved separately
from the tutorial's cells. Their Share control exports an individual
cell. The Jupyter notebook export keeps the code and text from all cells,
including added cells, without results or the tutorial's reading.

**Ways to find an explanation.** The tutorials page lists series in
teaching order and offers search. The topic tree shows which ideas build
on earlier ones and which topics are not taught here yet. Browse by topic
brings pages about one subject together.

**A workspace for independent work.** dewmini supports Python code,
notes, files, and SQL databases outside a tutorial. It can open notebooks
and Python files and has a Stop button for running code.

**A course coverage map.** Tutorials declare which learning outcomes
their sections teach. The build checks those section references. The
curriculum map shows outcomes that still need material.

## Sharing and saved work

Tutorials run Python in the browser and do not automatically submit
answers to a teacher. Learners can choose to export and share files.
A cell's report link can send its current code and result to a GitHub
form. Opening that form sends the details to GitHub; submitting posts
the report. Code a learner chooses to run may also make internet requests.

[Using dewlab](docs/FOR_STUDENTS.md) explains saving and reset controls.
[Reporting a problem](docs/REPORTING_A_PROBLEM.md) explains what reports
include and offers ways to ask for help.

---

## How the site is put together

`build.py` reads the markdown in `tutorials/`, renders each file into the page
template at `assets/shell.html`, and writes a plain static site into `site/`.
GitHub Pages hosts the built files. GitHub Actions runs the build on
pushes to `main` and publishes the result. Python runs on the learner's
device rather than on an application server.

In the browser, `assets/tutorial-runtime.js` starts Pyodide, a version of
Python built for browsers. CodeMirror provides the cell editors. On the
hosted site, Python runs in a Web Worker, separately from the page's
interface. This lets the page offer a Stop button. The tutorial helpers
are defined in `assets/tutorial_tools.py`.

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

[Architecture](ARCHITECTURE.md) explains the build stages, browser
behaviour, and how the authoring editor connects to GitHub. It also
suggests where to begin reading the code for different kinds of changes.

---

## Running it on your own machine

These steps are for authors and contributors who want a local copy of
the site. They need Python 3.12 or later. Learners can use the published
site without this setup.

```sh
git clone https://github.com/deweydex/dewlab
cd dewlab
pip install -r requirements-build.txt
python3 build.py --clean
python3 -m http.server -d site 8000
```

The local site is then available at `http://localhost:8000`. The build
writes `site/`, which is excluded from Git.

`python3 build.py --no-standalone` skips downloadable copies for a faster
content preview. The full build checks those copies too. The test command
is `python3 -m pytest`; [Contributing](CONTRIBUTING.md) explains test setup.

---

## Where the project stands

The site includes tutorials, practice pages, saved work, version choices,
and a topic tree. Content is still being written and reviewed.

[Status](planning/STATUS.md) records progress on content and features.
The [curriculum map](planning/CURRICULUM_MAP.md) shows which learning
outcomes the tutorials cover. [Questions](QUESTIONS.md) records decisions
that remain open.

---

## Licence

The [licence](LICENSE.md) explains personal learning, adaptation,
classroom use, and other uses. It includes how to contact the author.
