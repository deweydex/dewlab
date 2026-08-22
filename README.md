# dewlab

dewlab turns a markdown file into a web page where students read an
explanation, edit the Python underneath it, and run it — in the browser, with
nothing installed and nothing submitted anywhere.

It exists because of a familiar first week. You want a class writing Python in
the first hour, and instead the hour goes on installing an interpreter, an
editor, and a package or two, on four operating systems, several of which are
locked down. dewlab moves that cost to zero: a student opens a link. The Python
that runs is real Python, running on their own machine inside the browser tab,
so nothing they write is sent anywhere and nothing you host has to execute
their code.

This README is a walkthrough. It covers what a student sees, how you write a
tutorial, what tools your tutorials can call, and how to install and run the
build. If you are deciding whether to write your next set of materials in
dewlab, this is the document to read.

---

## What a student sees

Open a built tutorial and you get a reading page — serif prose, generous
margins, no toolbars. Interleaved with the prose are **cells**: small editable
boxes of Python with a **Run** button. Pressing Run (or Ctrl-Enter) executes
that cell and renders the result directly beneath it.

What comes back is what they would expect from a notebook, if they have used
one:

- anything the code printed;
- the value of the last line, if it is an expression;
- a `DataFrame` as a real table, not as text;
- a matplotlib figure as a picture;
- and if it goes wrong, a traceback trimmed down to *their* line, without the
  machinery underneath it.

Some things are deliberately different from a notebook, because a notebook was
built for researchers and this is built for people meeting Python for the first
time:

- `plt.plot(...)` does not print `[<matplotlib.lines.Line2D object …>]` above
  the figure. That line is noise that looks like an error.
- Every cell has a **reset** button that restores the version you wrote, so a
  student who has edited a cell into rubble can recover without losing the rest
  of the page.
- Cells on one page share a namespace in the order they appear, so cell three
  can use what cell one defined. Pages do **not** share anything with each
  other — each page starts clean.

Every page carries a **Settings** button in the masthead, and the masthead
follows the reader down the page, so it is always one tap away. Everything a
student can change or take away lives behind it, in three sections:

- **Your work** — whether the page is saving, and the buttons to export a copy,
  load one back, or start the tutorial again.
- **This tutorial** — **Download to keep**, which is described below.
- **Texture** — theme (auto, light, dark), serif or sans or mono, text size,
  line width as **narrow / medium / wide** with a slider behind them for
  anything in between, and link colour. Also **Header: full or minimal**, which
  tightens the masthead and puts the previous/next row on one line — worth
  knowing about if a class is reading on phones.

One button rather than a row of them, because a student who has found Settings
once has found all of it. Texture choices persist across pages and across
visits; a reading surface a student can adjust is a reading surface more
students can actually use.

That leaves the previous / **All tutorials** / next row carrying nothing but
navigation, which is what makes it work on a phone: two long tutorial titles
side by side, the way back to the contents beneath them. It sticks along with
the masthead, so moving on to the next tutorial never means scrolling to one end
of the page to find the link.

Under that, every tutorial with more than one section carries a **Contents**
list, closed by default. Open, it is the whole page's headings, with
sub-headings nested underneath — the fastest way back to a section a student
half-remembers. Sub-headings that repeat, like the several *Your turn* prompts in
a long tutorial, are left out of the listing: a contents entry a reader cannot
choose between is noise.

**Download to keep** gives the student one HTML file — on a memory stick, in
their downloads folder, anywhere — that they open by double-clicking. It
carries the reading, the cells, the editor and the mathematics inside it, and
looks and behaves like the page they downloaded it from.

One caveat worth passing on to a class: the file needs an internet connection
the *first* time it is opened, because Python itself is fetched then. Without
one, the reading works and the cells say so plainly rather than failing
silently.

The contents page carries the same offer for a whole series at once: **Download
all 18 as single files**, which is a zip of exactly those files. That is the one
to reach for when you are setting up a room, filling a memory stick, or handing
a class something to take home — rather than clicking through eighteen pages.

There is a **topic tree** on its own page: every topic both module descriptors
cover, laid out left to right by what has to come first and grouped top to
bottom by subject. Drag to move around it, scroll to zoom, and choose any topic
to read what it is, two or three places it turns up in computing, what it needs
first, and — if it is taught here — a link straight to the section that teaches
it. Topics dewlab does not teach yet are drawn but dashed, so the tree is honest
about its own gaps rather than quietly leaving them out.

Underneath it, a second and smaller map shows how the **tutorials** relate:
reading order in solid arrows, and a dashed arrow wherever a later tutorial
builds on an earlier one and says so in its own text. Those are found by reading
the tutorials, not by anybody maintaining a list, so they cannot go out of date.

The contents page itself is an introduction and a list, which is what somebody
arriving actually wants.

A tutorial with no code in it at all is a perfectly ordinary dewlab tutorial —
same format, same styling — and it never loads the Python runtime, so a page of
prose and mathematics opens instantly.

---

## Writing a tutorial

A tutorial is one markdown file in `tutorials/<module>/<slug>.md`. It opens with
frontmatter, then ordinary prose and code.

```markdown
---
title: "Working With a Table"
slug: working-with-tables
module: computational-methods
year: "2026-2027"
series: python-fundamentals
order: 2
version: 1
---
```

| Field | What it does |
|---|---|
| `title` | Shown in the browser tab and at the top of the page. |
| `slug` | The filename of the built page, and how other tutorials link to this one. |
| `module` | Which subject this belongs to. It is also the folder name. Any value you like — a new module is a new folder, not a code change. |
| `year` | An academic year like `2026-2027`, since the programme is scoped a year at a time. |
| `series` | Groups tutorials that are meant to be worked through in order. |
| `order` | Position within that series. |
| `version` | Bump this when you change the code in a cell, so a student's saved progress knows the page moved on. Prose fixes do not need it. |

You can add `packages: [sympy]` if a tutorial needs a library beyond the three
that always load, and any other field you find useful — nothing validates
against a fixed list.

### Cells students can run

A fenced code block tagged `exec` becomes a live cell. It needs an `id`, and it
can carry a `hint`:

````markdown
```python exec
id: filter-evening
hint: Try printing readings["evening"] > 14 on its own first.
readings[readings["evening"] > 14]
```
````

- **`id`** is how saved progress finds this cell again. It must be unique within
  the tutorial, and it should stay the same when you edit the cell — that is
  what lets you fix a typo without wiping what students have written.
- **`hint`** is optional. It appears behind a small **?** on the cell, so it is
  available without being in the way.

### Code students only read

An **untagged** fence is illustrative code. It gets the same syntax
highlighting, but no Run button and no editing:

````markdown
```python
total = 0
for value in [1, 2, 3]:
    total = total + value
```
````

The distinction is visible at a glance: if there is no Run button, it is there
to be read.

### Mathematics

Write LaTeX between dollar signs — `$a_i + b_j$` inline, `$$…$$` on its own
line for display. It renders with KaTeX. Prices survive unharmed: `$5 or $6`
is left alone, and `\$99` is an escaped literal.

### Checking an answer

`check()` compares what a student produced against what you expected and shows
a pass or a not-yet:

```python
check(readings["morning"].mean(), 10.85)
```

It is deliberately forgiving in the ways that matter for beginners:

- floats compare with a tolerance, so `check(0.1 + 0.2, 0.3)` passes — a
  student meeting floating point for the first time should not be told their
  correct answer is wrong;
- arrays and DataFrames compare element by element instead of raising;
- lists report *which* position differs;
- `True` is not equal to `1`, whatever Python thinks, because it is not the
  answer they meant.

Nothing is scored, recorded, or sent anywhere. `check` exists so a student
working alone at eleven at night gets an answer to "did I get that right?".

### Sharing setup code between tutorials

Boilerplate that several tutorials need — loading the same dataset, usually —
lives once in `setup/` and is pulled in where it is needed:

````markdown
```python exec
id: setup
{{include: setup/load_readings.py}}
```
````

The build pastes the file in. Worth being clear about what that does and does
not buy you: it removes the duplication from your *source*, not from the
student's browser. Every page is its own Python session, so an included setup
cell runs again on every page.

### Linking between tutorials

```markdown
See [working with a table](tutorial:working-with-tables#the-shared-table).
```

The build turns that into a real relative link. If the slug or the anchor does
not exist, **the build fails** rather than shipping a dead link for a student to
find. Headings and cell ids both count as anchors.

### Images

Every `<img>` needs an `alt` attribute or the build stops. An explicit
`alt=""` is accepted, and is how you mark an image as decorative.

---

## What your cells can call

Beyond ordinary Python, a cell can use:

| Function | What it does |
|---|---|
| `show(*values, label=None)` | Render something mid-cell, rather than only at the end. |
| `show_table(frame, max_rows=20, caption=None)` | Render a DataFrame as a table. Long frames are truncated, and say so. |
| `check(actual, expected, tolerance=None, label=None)` | Pass or not-yet feedback, as above. |
| `text_input(label, value="", id=None)` | A text box. Read what was typed with `.value`. |
| `dropdown(label, options, value=None, id=None)` | A menu. Also read with `.value`. |
| `button(label, on_click)` | A button that calls your function, appending output below itself. |
| `await load_csv(name)` | Load a CSV from `data/` into a DataFrame. |

Widgets keep their values when a cell is re-run, so a student can type an
answer, press Run, and still see what they typed.

`numpy`, `pandas` and `matplotlib` are available in every tutorial without
importing anything special — they load with the page.

---

## Installing and running it

You need Python 3.12 or later. Students need none of this; it is for authors.

```sh
git clone https://github.com/deweydex/dewlab
cd dewlab
pip install -r requirements-build.txt
```

Build the tutorials and read them:

```sh
python3 build.py --clean
python3 -m http.server -d site 8000
```

That writes the downloadable copies too, into `site/download/` — one HTML file
per tutorial, plus one zip per series holding that series' files. They are the
slow part of a build, so `python3 build.py --no-standalone` skips them while
you are working on content.

Then open `http://localhost:8000/tutorials/<module>/<slug>.html`. The built
site lives in `site/` and is never committed — it is regenerated on every push
and published from there, so the markdown and the published page cannot drift
apart.

Run the tests with:

```sh
python3 -m pytest
```

The unit tests are fast and need no browser. The end-to-end tests drive a real
browser against a real Python runtime; they need a local copy of that runtime
first (`python3 dev/fetch_pyodide.py`, about 30 MB) and skip with a message if
it is missing.

### Adding a new module

Make a folder under `tutorials/` and put tutorials in it whose `module` field
matches the folder name. That is the whole procedure — nothing keeps a list of
modules that needs updating.

---

## How the pieces fit together

```text
tutorials/            your markdown, one folder per module
setup/                shared setup snippets, pulled in with {{include: ...}}
data/                 shared CSV datasets
assets/
  shell.html          the page template every tutorial is rendered into
  tutorial-style.css  the house style and the settings panel
  tutorial-runtime.js starts Python, mounts the editors, runs a cell
  tutorial_tools.py   what a student's cell code can call
  vendor/             CodeMirror and KaTeX, built from vendor-src/
build.py              markdown in, site/ out
tests/                unit tests, browser tests, and a manual checklist
planning/             what was decided before the build, and why
DECISIONS_LOG.md      what was decided during it, and what changing it costs
QUESTIONS.md          decisions still open
```

`assets/vendor/` is committed on purpose, even though it is built output. It
means neither the build nor an author previewing locally needs a Node
toolchain. If you change a pinned version in `vendor-src/package.json`, rebuild
it with `npm install && npm run build` inside `vendor-src/` and commit the
result.

---

## Where this has got to

Working today: the whole reading and running experience described above — the
page, the cells, output rendering, mathematics, highlighting, the settings
panel, and the build that produces it all from markdown.

Not built yet:

- **Saved progress.** A student's work currently lives only as long as the tab
  does. Autosave and a version-aware restore are designed and specified in
  `planning/VERSIONING_AND_PROGRESS.md`.
- **Navigation.** There is no contents page and no previous/next yet, so pages
  are reachable only by their own address.
- **Publishing.** The automated build-and-publish step is designed but not
  switched on.
- **The authoring editor.** For now, tutorials are written in a text editor.

`QUESTIONS.md` holds anything currently waiting on a decision, and is the right
place to raise one.
