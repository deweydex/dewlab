# Writing a tutorial

A dewlab tutorial is one markdown file. The build turns it into a web page with
runnable Python in it. This document covers the format: what goes in the file,
what the build checks, and what to run before you open a pull request.

Two other documents go with this one. Read
[`../planning/PEDAGOGICAL_STYLE_GUIDE.md`](../planning/PEDAGOGICAL_STYLE_GUIDE.md)
before you write prose — it is short, and it settles questions that are easy to
guess wrong on. This page governs how a tutorial is built; that one governs how
it is written.

---

## The file and its frontmatter

A tutorial lives at `tutorials/<module>/<slug>.md` and opens with frontmatter,
then ordinary prose and code.

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
| `module_title` | The readable name for the module, shown on the contents page. |
| `year` | An academic year like `2026-2027`, since the programme is scoped a year at a time. |
| `series` | Groups tutorials that are meant to be worked through in order. |
| `version` | A dated version like `2026.08.24.1`. Bump it when you change the code in a cell, so a student's saved progress knows the page moved on. Prose fixes do not need it. See [Releasing a new version](#releasing-a-new-version) for when a bump needs a full versioned release instead. |
| `status` | Optional. `live` (the default) or `archived`. An archived tutorial keeps its built page, so old links still resolve, but drops out of the reading order and the contents page. |

Add `packages: [sympy]` if a tutorial needs a library beyond `numpy`, `pandas`
and `matplotlib`, which load with every page. You can add any other field you
find useful — nothing validates against a fixed list, except `covers:`, which
is described under [Curriculum coverage](#curriculum-coverage).

---

## Where a tutorial sits in its series

Not in the frontmatter. Each series has one file beside its tutorials listing
them in reading order:

```yaml
# tutorials/computational-methods/python-fundamentals.order.yaml
series: Python fundamentals
order:
  - first-steps
  - working-with-tables
```

Moving a tutorial is moving a line, and inserting one is adding a line. Nothing
else changes: no renumbering, no editing every file after it. That is the whole
reason reading order is not a field on each tutorial.

The build checks it both ways. A tutorial the file forgets stops the build, and
so does a slug with no tutorial behind it. The second check is the one worth
having, because a file that looks complete beside a series that is quietly short
is a mistake nobody notices.

Slugs are unique within a module, not across the site — the built path already
carries the module, so two modules may each have a `first-steps`. A `tutorial:`
link looks in its own module first.

---

## Cells students can run

A fenced code block tagged `exec` becomes a live cell. It needs an `id`, and it
can carry a `hint`:

````markdown
```python exec
id: filter-evening
hint: Try printing readings["evening"] > 14 on its own first.
readings[readings["evening"] > 14]
```
````

`id` is how saved progress finds this cell again. It must be unique within the
tutorial, and it should stay the same when you edit the cell. That is what lets
you fix a typo without wiping what students have written.

`hint` is optional. It appears behind a small **?** on the cell, so it is
available without being in the way.

---

## Code students only read

An untagged fence is illustrative code. It gets the same syntax highlighting,
but no Run button and no editing:

````markdown
```python
total = 0
for value in [1, 2, 3]:
    total = total + value
```
````

The difference is visible at a glance: if there is no Run button, it is there to
be read.

---

## Mathematics

Write LaTeX between dollar signs — `$a_i + b_j$` inline, `$$…$$` on its own line
for display. It renders with KaTeX. Prices survive unharmed: `$5 or $6` is left
alone, and `\$99` is an escaped literal.

---

## Checking an answer

`check()` compares what a student produced against what you expected and shows a
pass or a not-yet:

```python
check(readings["morning"].mean(), 10.85)
```

It is forgiving in the ways that matter for beginners. Floats compare with a
tolerance, so `check(0.1 + 0.2, 0.3)` passes — a student meeting floating point
for the first time should not be told their correct answer is wrong. Arrays and
DataFrames compare element by element instead of raising. Lists report which
position differs. And `True` is not equal to `1`, whatever Python thinks,
because it is not the answer they meant.

Nothing is scored, recorded or sent anywhere. `check` exists so that a student
working alone at eleven at night gets an answer to "did I get that right?".

---

## Sharing setup code between tutorials

Boilerplate that several tutorials need — loading the same dataset, usually —
lives once in `setup/` and is pulled in where it is needed:

````markdown
```python exec
id: setup
{{include: setup/load_readings.py}}
```
````

The build pastes the file in. Worth being clear about what that does and does
not buy you: it removes the duplication from your source, not from the student's
browser. Every page is its own Python session, so an included setup cell runs
again on every page.

---

## Linking between tutorials

```markdown
See [working with a table](tutorial:working-with-tables#the-shared-table).
```

The build turns that into a real relative link. If the slug or the anchor does
not exist, the build fails rather than shipping a dead link for a student to
find. Headings and cell ids both count as anchors.

---

## Images

Every `<img>` needs an `alt` attribute or the build stops. An explicit `alt=""`
is accepted, and is how you mark an image as decorative.

---

## Practice pages

Every tutorial has a practice page beside it, at `<slug>-practice.md`, declared
with `practice_for:` in its frontmatter:

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

The contents page links a tutorial to its own practice page, and the tutorial
links forward to it too, so practice is always one click from the material it is
practising.

A **mixed problem set** draws on several tutorials at once, declared with
`practice_across:` instead:

```yaml
title: "Mixed Problems — Algebra and Functions"
slug: mixed-algebra
practice_across:
  - numbers-and-their-families
  - expressions-come-alive
  - cracking-equations
```

A mixed set is listed on the contents page under its module, and every tutorial
it draws on links to it in turn — so a student working through
`cracking-equations` sees the mixed set waiting, without it displacing that
tutorial's own practice page.

### Answers and hints

Answers go behind a fold beside the problem, not in a key at the end:

```html
<details class="dl-answer"><summary>answer</summary>

The answer, with the working.

</details>
```

The `dl-answer` class is what the styling and the fold marker come from, so it
is not decoration you can drop. The site is public, so an answer that exists can
be read and no arrangement changes that. What is worth protecting is the moment
before looking, and a fold is that moment made into a click.

Hints go in a fold of their own, before the answer, for problems where a student
can get stuck:

```html
<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The first thing to work out.
2. What that lets you do next.
3. The step people usually miss.

**Think about:** the question that makes the method make sense.

**Try this next:** a related problem the same steps solve.

</details>
```

Two folds, opened in order, so a stuck student gets a route rather than an
answer. The reflection and the follow-on question at the end matter as much as
the steps: a hint that ends at the answer teaches the answer, and one that ends
in a related question teaches the method. The build fails if a `<details>`
appears without one of these two classes, so a fold cannot be added without the
styling that makes it work.

Write toward a few tools per section rather than a cell per problem — one
`python exec` cell holding the helpers a section needs, rather than sixty
editors on a page. **Every number in an answer gets run before it is published**,
not reasoned about. See
[`../planning/PEDAGOGICAL_STYLE_GUIDE.md`](../planning/PEDAGOGICAL_STYLE_GUIDE.md#6-practice-pages)
for the full shape of a good practice page.

---

## The Reference panel and glossary files

Each tutorial has a `<slug>.glossary.yaml` beside it listing the terms,
functions, operators and formulas that tutorial introduces for the first time in
its series:

```yaml
entries:
  - term: matrix
    kind: concept
    definition: A grid of numbers, arranged in rows and columns.
```

The build assembles a tutorial's Reference panel from its own glossary plus
every earlier one in its series, so a reader never sees a term they have not
been taught. A practice page gets no glossary of its own; its reference is the
union of the tutorials it names.

The rules for what belongs in one are in
[`.claude/skills/tutorial-glossary/SKILL.md`](../.claude/skills/tutorial-glossary/SKILL.md),
and the design behind it is in
[`../planning/REFERENCE_PANEL.md`](../planning/REFERENCE_PANEL.md). Write or
regenerate the glossary whenever you add or remove something a tutorial
introduces.

---

## Curriculum coverage

dewlab tracks which QQI learning outcomes each tutorial teaches, against the
real module descriptors, so the site can say plainly what is covered and what is
not.

A tutorial's frontmatter declares, per section heading, what it teaches or
merely touches on:

```yaml
covers:
  the-dot-product-first:
    covers: [PDP-LO4]
    touches: [MIT-6.3]
```

`covers:` under a code means the outcome is taught there. `touches:` means the
section uses the idea without teaching it as its own outcome. The build fails if
a section named here is not a real heading in the tutorial, so this list cannot
drift from the page it describes.

The outcomes live in `planning/curriculum/outcomes.yaml`, one entry per learning
outcome, transcribed from the QQI descriptors under
`planning/curriculum/descriptors/`. **The outcome text is what coverage is
measured against.** The descriptor's own "e.g." examples are suggested content
only, and belong in a topic's `uses:` in `planning/curriculum/topics.yaml`, never
folded into the outcome itself. That distinction is what keeps coverage meaning
something rather than meaning whatever example a tutorial happened to use.

`planning/curriculum/topics.yaml` is the glossary behind the topic tree: one
entry per topic, with what it is in plain language, where it is used, and what it
needs first (`needs:`), which is what lays the tree out.

Run `python3 dev/curriculum_map.py` after touching any curriculum file. It
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

Widgets keep their values when a cell is re-run, so a student can type an answer,
press Run, and still see what they typed.

`numpy`, `pandas` and `matplotlib` are available in every tutorial without
importing anything special — they load with the page.

---

## Releasing a new version

Most edits — fixing a typo, clarifying a sentence, correcting a bibliography
entry — are just a commit. Bump `version:` only when you change what a cell
does, so a student's saved progress can tell the page moved on.

Where a change is substantial enough that students already partway through the
old version deserve to keep working in it undisturbed — a rewritten explanation,
cells replaced rather than tweaked — publish it as a release instead of editing
in place:

1. Turn the tutorial into a folder: `tutorials/<module>/<slug>/`.
2. Freeze the old file as `v<old-version>.md` inside it, unchanged.
3. Write the new version as `<slug>.md` in the same folder, with `version:`
   bumped.

The build serves the newest release under the tutorial's plain, unversioned
address, and every past release stays reachable at its own
`<slug>/v<version>.html`, frozen as it was. A reader sees a small version picker
wherever more than one release exists, and the contents page, the topic tree and
every `tutorial:` link always resolve to the current one. Frozen releases get no
downloadable copy of their own, since a downloadable snapshot of superseded
material is not worth shipping.

`TestVersionsOfATutorial` and `TestTheVersionListInTheManifest` in
`tests/test_build.py` pin down the exact behaviour.

---

## Adding a new module

Make a folder under `tutorials/` and put tutorials in it whose `module` field
matches the folder name. That is the whole procedure. Nothing keeps a list of
modules that needs updating.

---

## The authoring editor

A browser-based editor at `/editor.html` reads and writes tutorials through the
GitHub API, for changes that do not need a local checkout: reordering a series,
editing frontmatter, renaming a slug with the cell-id warnings that protect
saved student work, and opening a pull request with the result. It sits on top
of the same markdown files described here — nothing about a tutorial's format is
different because it went through the editor. For substantial writing, a local
checkout and an ordinary text editor is still the more comfortable tool.

The editor reports a `tutorial:slug#anchor` link that does not resolve, checked
against every other tutorial's real slugs and headings, before you commit rather
than after. A "Link to another tutorial" toggle above the prose editor searches
every tutorial by title, slug or module and inserts a real link at the cursor,
so you reach for a tutorial that exists rather than typing a slug from memory.
Its code cells offer keyword and locally-typed-name completion as you write. Open
the same tutorial as a student and their cell offers the same completion plus a
hover docstring, read off whatever the setup cell imported and whatever the
student has defined so far.

---

## Before you open a pull request

Run `python3 build.py` and fix anything it fails on — a dead link, a missing
`alt`, an unstyled fold, a `covers:` section that does not exist.

Run `python3 dev/curriculum_map.py` if you touched `covers:`, `outcomes.yaml` or
`topics.yaml`, and check that the coverage gaps it reports are the ones you
expect.

Run `python3 -m pytest` and make sure it is green.

If you added or changed a code cell, run it. Every number a tutorial or practice
page states as an answer should have been executed, not reasoned about. Open the
page in a browser and click through it.

Record a real decision — something somebody could reasonably have done
differently — as a new numbered entry in [`../DECISIONS_LOG.md`](../DECISIONS_LOG.md),
with what it would cost to change your mind later.
[`../QUESTIONS.md`](../QUESTIONS.md) is where anything still waiting on a
decision belongs.
