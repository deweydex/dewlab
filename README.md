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
tutorial, how practice and versioning and curriculum coverage work, what tools
your cells can call, how to install and run the build, and how the pieces of
the site fit together. If you are deciding whether to write your next set of
materials in dewlab, or you are about to write a tutorial for the first time,
this is the document to read. If you have not seen it yet, read
[`planning/PEDAGOGICAL_STYLE_GUIDE.md`](planning/PEDAGOGICAL_STYLE_GUIDE.md)
next — it governs how a tutorial is written, and this document governs how it
is built.

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

**Work is saved as you go**, in the browser's own storage, keyed to that exact
tutorial and its version — nothing is sent to a server, and nothing is scored.
A student who closes the tab and comes back a week later finds their code and
its last output waiting, and if a tutorial has since been revised, their work
carries over cell by cell wherever a cell's id has not changed. Where a
tutorial has more than one published release, a small picker on the page lets
a reader move between them, and a returning student stays pinned to the
release they were already working in rather than being moved without asking.

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
all N as single files**, which is a zip of exactly those files. That is the one
to reach for when you are setting up a room, filling a memory stick, or handing
a class something to take home — rather than clicking through every page by
hand.

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

**Every tutorial has a practice page**, and the contents page links to it
alongside the tutorial itself. See [Practice pages and mixed problem
sets](#practice-pages-and-mixed-problem-sets) below for how that is written.

---

## Writing a tutorial

A tutorial is one markdown file in `tutorials/<module>/<slug>.md`. It opens with
frontmatter, then ordinary prose and code.

```markdown
---
title: "Working With a Table"
slug: working-with-tables
module: computational-methods
module_title: "Computational Methods"
year: "2026-2027"
series: python-fundamentals
version: 2026.08.24.1
---
```

| Field | What it does |
|---|---|
| `title` | Shown in the browser tab and at the top of the page. |
| `slug` | The filename of the built page, and how other tutorials link to this one. |
| `module` | Which subject this belongs to. It is also the folder name. Any value you like — a new module is a new folder, not a code change. |
| `module_title` | The human-readable name for the module, shown on the contents page. |
| `year` | An academic year like `2026-2027`, since the programme is scoped a year at a time. |
| `series` | Groups tutorials that are meant to be worked through in order. |
| `version` | A dated version like `2026.08.24.1`. Bump it when you change the code in a cell, so a student's saved progress knows the page moved on. Prose fixes do not need it. See [Releasing a new version](#releasing-a-new-version-of-a-tutorial) for when a bump needs a full versioned release rather than an in-place edit. |
| `status` | Optional. `live` (the default) or `archived`. An archived tutorial keeps its built page, so old links still resolve, but drops out of the reading order and the contents page. |

You can add `packages: [sympy]` if a tutorial needs a library beyond the three
that always load, and any other field you find useful — nothing validates
against a fixed list, except `covers:`, described in [Curriculum
coverage](#curriculum-coverage) below.

### Where a tutorial sits in its series

Not in the frontmatter. Each series has one file beside its tutorials listing
them in reading order:

```yaml
# tutorials/computational-methods/python-fundamentals.order.yaml
series: Python fundamentals
order:
  - first-steps
  - working-with-tables
```

**Moving a tutorial is moving a line. Inserting one is adding a line**, and
nothing else changes — no renumbering, no editing every file after it. That is
the whole reason this is not a field on each tutorial.

The build checks it both ways: a tutorial the file forgets stops the build, and
so does a slug with no tutorial behind it. The second is the one worth having,
because a file that looks complete and a series that is quietly short is a
mistake nobody notices.

Slugs are unique **within a module**, not across the site — the built path
already carries the module, so two modules may each have a `first-steps`. A
`tutorial:` link looks in its own module first.

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

## Practice pages and mixed problem sets

Every tutorial has a practice page beside it, at `<slug>-practice.md`,
declared with `practice_for:` in its frontmatter:

```yaml
title: "A Grid of Numbers — Practice"
slug: grid-of-numbers-practice
practice_for: grid-of-numbers
module: computational-methods
module_title: "Computational Methods"
year: "2026-2027"
series: matrices
version: 2026.08.24.1
```

The contents page links a tutorial to its own practice page, and a tutorial's
own page links forward to it too, so practice is always one click from the
material it is practising.

Beyond one-tutorial practice, a **mixed problem set** draws on several
tutorials at once, declared with `practice_across:` instead of `practice_for:`:

```yaml
title: "Mixed Problems — Algebra and Functions"
slug: mixed-algebra
practice_across:
  - numbers-and-their-families
  - expressions-come-alive
  - cracking-equations
```

A mixed set is listed on the contents page under its module, and every
tutorial it draws on links to it in turn — so a student working through
`cracking-equations` sees the mixed set waiting, without it ever displacing the
tutorial's own practice page.

**Answers go behind a fold beside the problem**, not in a key at the end:

```html
<details class="dl-answer"><summary>answer</summary>

The answer, with the working.

</details>
```

The `dl-answer` class is load-bearing — the styling and the fold marker come
from it. The site is public, so an answer that exists can be read and no
arrangement changes that; what is worth protecting is the moment before
looking, and a fold is that moment made physical.

**Hints go in a fold of their own, before the answer**, for problems where a
student can get genuinely stuck:

```html
<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The first thing to work out.
2. What that lets you do next.
3. The step people usually miss.

**Think about:** the question that makes the method make sense.

**Try this next:** a related problem the same steps solve.

</details>
```

Two folds, opened in order, so a stuck student gets a route rather than the
answer. The reflection and the follow-on question at the end matter as much as
the steps — a hint that ends at the answer teaches the answer, and one that
ends in a related question teaches the method. The build fails if a `<details>`
appears without one of these two classes on it, so a fold cannot be added
without the styling that makes it work.

A few tools per section, not a cell per problem, is the shape to write toward —
one `python exec` cell holding the helpers a section needs, rather than sixty
editors on a page. **Every number in an answer gets run before it is
published**, not reasoned about; see
[`planning/PEDAGOGICAL_STYLE_GUIDE.md`](planning/PEDAGOGICAL_STYLE_GUIDE.md#6-practice-pages)
for the full shape of a good practice page.

---

## Releasing a new version of a tutorial

Most edits — fixing a typo, clarifying a sentence, correcting a bibliography
entry — are just a commit. Bump `version:` only when you change what a cell
*does*, so a student's saved progress can tell the page moved on.

Where a change is substantial enough that students already partway through the
old version deserve to keep working in it undisturbed — a rewritten
explanation, cells replaced rather than tweaked — publish it as a proper
release instead of editing in place:

1. Turn the tutorial into a folder: `tutorials/<module>/<slug>/`.
2. Freeze the old file as `v<old-version>.md` inside it, unchanged.
3. Write the new version as `<slug>.md` in the same folder, with `version:`
   bumped.

The build serves the newest release under the tutorial's plain, unversioned
address, and every past release stays reachable at its own
`<slug>/v<version>.html`, frozen exactly as it was. A reader sees a small
version picker wherever more than one release exists, and the contents page,
the topic tree, and every `tutorial:` link always resolve to the current one.
Frozen releases do not get a downloadable copy of their own — only the current
release does, since a downloadable snapshot of superseded material is not
worth shipping. See `tests/test_build.py`'s `TestVersionsOfATutorial` and
`TestTheVersionListInTheManifest` for the exact behaviour this guarantees.

---

## Curriculum coverage

dewlab tracks which QQI learning outcomes each tutorial actually teaches,
against the real module descriptors, so the site can say honestly what is
covered and what is not.

A tutorial's frontmatter declares, per section heading, what it teaches or
merely touches on:

```yaml
covers:
  the-dot-product-first:
    covers: [PDP-LO4]
    touches: [MIT-6.3]
```

`covers:` under a code means the outcome is genuinely taught there; `touches:`
means the section uses the idea without teaching it as its own outcome. The
build fails if a section named here is not a real heading in the tutorial, so
this list cannot drift from the page it describes.

The outcomes themselves live in `planning/curriculum/outcomes.yaml`, one entry
per learning outcome, transcribed from the QQI module descriptors under
`planning/curriculum/descriptors/`. **The outcome text is what coverage is
measured against — the descriptor's own "e.g." examples are suggested content
only, and belong in a topic's `uses:` in `planning/curriculum/topics.yaml`,
never folded into the outcome itself.** That distinction is load-bearing: it
is the difference between "coverage" meaning something and it meaning whatever
example a tutorial happened to use.

`planning/curriculum/topics.yaml` is the glossary behind the topic tree: one
entry per topic, with what it is in plain language, where it is used, and what
it needs first (`needs:`) — the edges that lay the tree out top to bottom. Run
`python3 dev/curriculum_map.py` after touching any curriculum file; it
regenerates `planning/CURRICULUM_MAP.md` and reports any outcome nobody has
written a tutorial for yet.

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

## The authoring editor

A browser-based editor at `/editor.html` reads and writes tutorials through
the GitHub API, for changes that do not need a local checkout: reordering a
series, editing frontmatter, renaming a slug with the cell-id warnings that
protects saved student work, and opening a pull request with the result. It is
a convenience layered on top of the same markdown files this README describes
— nothing about a tutorial's format is different because it went through the
editor rather than a text editor. For substantial writing, a local checkout and
an ordinary editor is still the more comfortable tool.

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

Three GitHub Actions workflows run on every push: `tests` runs the unit suite,
`standalone-bundle-is-current` fails if the vendored CodeMirror/KaTeX bundle
has drifted from `vendor-src/`, and `publish` (`.github/workflows/deploy.yml`)
builds the site and deploys it to GitHub Pages on a push to `main`.

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
  tutorial-style.css  the house style, the settings panel, and the fold styles
  tutorial-runtime.js starts Python, mounts the editors, runs a cell
  tutorial_tools.py   what a student's cell code can call
  tree.html, tree.js  the topic tree page
  editor.html, editor.js  the browser-based authoring editor
  vendor/             CodeMirror and KaTeX, built from vendor-src/
build.py              markdown in, site/ out
dev/curriculum_map.py generates planning/CURRICULUM_MAP.md from outcomes.yaml, topics.yaml and the tutorials
tests/                unit tests, browser tests, and a manual checklist
planning/
  PEDAGOGICAL_STYLE_GUIDE.md  how a tutorial is written, and why
  curriculum/          outcomes.yaml, topics.yaml, and the QQI descriptor PDFs coverage is measured against
  STATUS.md             what has actually been built, and what has not
DECISIONS_LOG.md      what was decided during the build, and what changing it costs
QUESTIONS.md           decisions still open, waiting on Josh
LICENSE.md             terms for reusing this material
```

`assets/vendor/` is committed on purpose, even though it is built output. It
means neither the build nor an author previewing locally needs a Node
toolchain. If you change a pinned version in `vendor-src/package.json`, rebuild
it with `npm install && npm run build` inside `vendor-src/` and commit the
result.

---

## Contributing a tutorial

Before writing prose, read
[`planning/PEDAGOGICAL_STYLE_GUIDE.md`](planning/PEDAGOGICAL_STYLE_GUIDE.md) —
it is short, and it settles questions ("is 'let's' allowed?", "what goes in a
bibliography?") that are easy to guess wrong on. The short version: invite the
reader in — "let's try", "what happens when", "how might you" — rather than
instructing them; prose over bullets for explanations; every technical term
defined where it first appears; every tutorial ends with a bibliography of
three or four genuinely useful, verified further-reading links.

Before opening a pull request:

- Run `python3 build.py` and fix anything it fails on — a dead link, a
  missing `alt`, an unstyled fold, a `covers:` section that does not exist.
- Run `python3 dev/curriculum_map.py` if you touched `covers:`, `outcomes.yaml`
  or `topics.yaml`, and check the coverage gaps it reports are the ones you
  expect.
- Run `python3 -m pytest` and make sure it is green.
- If you added or changed a code cell, run it — every number a tutorial or
  practice page states as an answer should have actually been executed, not
  reasoned about. Open the page in a browser and click through it.

Record a real decision — something somebody could reasonably have done
differently — as a new numbered entry in `DECISIONS_LOG.md`, with what it
would cost to change your mind later. `QUESTIONS.md` is where anything still
waiting on Josh belongs.

---

## Where this stands

The reading and running experience described above, practice pages and mixed
problem sets, versioned releases, the curriculum coverage system and the topic
tree, the authoring editor, and the CI/CD pipeline that builds and publishes
the site on every push — all of that is built and live.

Content is not finished. `planning/STATUS.md` has the exact count and the
active roadmap; in short, the *Mathematics for IT* and *Programming and Design
Principles* modules are fully written, and *Computational Methods and Problem
Solving (5N0554)* is partway through — its linear algebra strand is done, and
Monte Carlo methods, algorithmic complexity, and systems modelling are not yet
written.

`QUESTIONS.md` holds anything currently waiting on a decision, and is the
right place to raise one.
