# Writing a tutorial

A dewlab tutorial is one markdown file. The build turns it into a web page with
runnable Python in it. This document covers the format: what goes in the file,
what the build checks, and what to run before you open a pull request.

If you only want to add or change one tutorial, `python3 check.py
tutorials/<id>` checks it in a second and says in plain words what to fix.
[`CHECK_YOUR_WORK.md`](CHECK_YOUR_WORK.md) explains that tool, and how it can
open the pull request for you.

Two other documents go with this one. Read
[`../planning/PEDAGOGICAL_STYLE_GUIDE.md`](../planning/PEDAGOGICAL_STYLE_GUIDE.md)
before you write prose — it is short, and it settles questions that are easy to
guess wrong on. This page governs how a tutorial is built; that one governs how
it is written.

---

## The file and its frontmatter

A tutorial is a folder, at `tutorials/<id>/`, holding everything that
belongs to it. The folder name is the tutorial's id: the address of its
page, how other tutorials link to it, and the key its readers' saved work
lives under. It is unique across the whole site and it never changes.

```text
tutorials/working-with-tables/
    working-with-tables.md              the tutorial
    working-with-tables-practice.md     its page of problems
    working-with-tables.glossary.yaml   what it teaches, for the reference
    v2026.08.24.1.md                    a frozen past release, if any
    a-sorted-table.png                  any picture or recording it uses
```

The tutorial itself is `<id>.md`, and it opens with frontmatter, then
ordinary prose and code. Nothing in the file says which course or series
it is in — that is written in `courses/`, described in the next section.

Only the first of those is required. A tutorial with no practice page, no
glossary, one release and no pictures is a folder with a single file in it,
and that is the normal case rather than an awkward one — it means a tutorial
never has to be rearranged later to make room for its own material.

```markdown
---
title: "Working With a Table"
year: "2026-2027"
version: 2026.08.24.1
---
```

| Field | What it does |
|---|---|
| `title` | Shown in the browser tab and at the top of the page. |
| `year` | An academic year like `2026-2027`, since the programme is scoped a year at a time. |
| `version` | A dated version like `2026.08.24.1`. Bump it when you change the code in a cell, so a student's saved progress knows the page moved on. Prose fixes do not need it. See [Releasing a new version](#releasing-a-new-version) for when a bump needs a full versioned release instead. |
| `status` | Optional, `live` by default. See the table below. |

| `status` | Built as a page? | In the reading order? | What it means |
|---|---|---|---|
| `draft` | No | No | Work in progress — visible only in a local build or the authoring editor. |
| `beta` | Yes | No | Reachable by direct URL, for testing or preview — never the default route. |
| `live` | Yes | Yes | The active, canonical release — the one a plain URL serves. |
| `archived` | Yes | No | Retired — still built, at its old URL, so old links and past students' saved work still have somewhere to land, but out of the reading order. |

Add `packages: [sympy]` if a tutorial needs a library beyond `numpy`, `pandas`
and `matplotlib`, which load with every page. You can add any other field you
find useful — nothing validates against a fixed list, except `covers:`, which
is described under [Curriculum coverage](#curriculum-coverage).

---

## Where a tutorial sits: courses and series

Not in the tutorial. A course (what the site calls a module) is one file under
`courses/`, and a series is a heading in it with the tutorials listed in
reading order:

```yaml
# courses/computational-methods.yaml
title: Computational Methods and Problem Solving
code: 5N0554 · QQI Level 5
status: beta
card: |
  We work through matrices, simulation, algorithms and debugging, in Python.
description: |
  This module is Computational Methods and Problem Solving (5N0554). …
contents:
  - title: Python fundamentals
    tutorials: [first-steps-cm, storing-and-computing, repeating-yourself]
  - title: Matrices
    tutorials: [grid-of-numbers, multiplying-grids, what-a-matrix-does-to-a-picture]
```

To put a tutorial on a course, add its id to a list. To move it, move the
line. To take it off, remove the line; the tutorial still builds at its own
address, and the build notes that nothing lists it. The same tutorial may be
listed in as many courses as want it — Programming and Design Principles is
the programming half of the integrated course, read on its own, and its
course file simply lists the same ids. The tutorial keeps its one page and
its one address; a reader following either course sees that course's tree
and previous and next.

The build refuses an id it cannot find, naming the course file and the line,
and refuses a second folder with an id that already exists, naming the
tutorial that has it. It warns, without stopping, when two tutorials share a
title, and when two tutorials cover much the same outcomes — both are worth
a look, neither is necessarily wrong.

`courses/index.yaml` lists the courses in the order they appear on the front
page and the contents page. A course's card on the front page is generated
from its `card:` text; nothing is written by hand in `pages/home.md`.

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

### Hints that wait for an attempt

A `hint:` line is there from the start. A `hint` fence is not: it stays
hidden until the cell above it has been run, and has failed, some number of
times. Write it straight after the cell, with nothing but the text a stuck
reader should see:

````markdown
```python exec
id: your-add
# Your add(a, b)
```

```hint
What does the last line of the error say Python could not do? Which line
of your cell is it pointing at, and what did you expect that line to
produce?
```

```hint
after: 12 errors
title: some steps
1. The outer loop picks a row index, `i`.
2. The inner loop picks a column index, `j`.
3. The result at `[i][j]` is `a[i][j] + b[i][j]`.

**Think about:** why the inner loop's range comes from `a[0]`, not `a`.
```
````

The first fold appears after the fifth run that raises an error. The
second appears after the twelfth. Each arrives closed, in normal flow under
the cell, with a small dot on the cell's bar until it is opened. Nothing is
counted on screen, and nothing leaves the browser. The reader can turn the
hints off in Settings.

Three optional header lines, in the same `key: value` shape as a cell's
own:

- `for:` names the cell the hint belongs to. Without it, the hint belongs
  to the exec cell just above it.
- `after:` says when the hint appears. The default is `5 errors`. The
  signals the page tracks, and how to write them:

  | Write | Appears once… |
  |---|---|
  | `5 errors` | five runs have raised, in total |
  | `3 identical errors` | three runs in a row have ended in the same error |
  | `2 unchanged runs` | the reader has run the very same code twice more |
  | `8 runs` | the cell has run eight times |
  | `3 failed checks` | a `check()` in the cell has failed on three runs in a row |
  | `2 empty results` | a `sql exec` cell's query has come back with no rows, two runs in a row |
  | `2 minutes` | two minutes have passed since the first run |

  Join several with a comma or `and`: `3 identical errors and 2 minutes`.
  Every term must hold. The `errors:5` spelling works too, if you prefer
  it. The build fails on a term it does not know.
- `title:` is the fold's summary line. The default is *Let's slow down a
  moment…*.

Inside the fence is markdown: lists, emphasis, inline code and `$…$`
maths all render. A code block inside a hint is indented four spaces
rather than fenced.

A cell may also carry an `expect:` line, a Python expression that is true
once the reader has got where the cell was leading:

````markdown
```python exec
id: your-add
expect: add([[1]], [[2]]) == [[3]]
# Your add(a, b)
```
````

It is evaluated after every run of that cell, in the page's own
namespace. Once it holds, no further hint appears for the cell. Anything
that goes wrong evaluating it counts as "not yet", so a name the reader
has not defined is fine. The reader never sees the expression, and it
never affects the run itself. A `check()` in the cell does the same job
for the `failed checks` signal.

A cell may also carry a `name:` line, a short label shown beside its
identity pill — a handle a reader can point at ("the `filter-evening`
cell") instead of its number, and what a traceback names the cell in
place of its own id, once given:

````markdown
```python exec
id: filter-evening
name: filter-evening
readings[readings["evening"] > 14]
```
````

Optional, and most cells don't need one. Keep it short — it sits beside
a small pill, not in a sentence — and give it no `=` in it: a line at
the top of a cell shaped like `word: value` is read as a header line,
the same way `id:`/`hint:`/`expect:` already are, so `name: str = "Ada"`
as a cell's own first line of code would be misread as a `name:` header
rather than run. Writing `=` in the label itself is what tells the build
this was never a header — a cell named `total = value` gets read as
code, not as a name, so keep the label to a plain phrase or a variable's
own bare name, the way `filter-evening` is above.

**What each stage is for.** The first fold asks. It is a question about
what the reader can see and what they expected, not an instruction: *What
did you expect this line to print? What does the last line of the error
name?* Its job is the habit, and the habit is asking that question before
changing anything. The second fold gives steps, in the shape of the
`dl-hint` fold below. A third, if there is one, gives the shape of the
code with a gap in it. None of them gives the answer: an answer belongs in
a `dl-answer` fold the reader opens for themselves, and is never triggered.
Not every cell earns a staged hint. A page where every cell produces one
teaches readers to ignore them. The style guide's section 3 has the
reasoning.

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

## Struck-out text, and task lists

Two markdown forms beyond the usual ones.

`~~like this~~` strikes text out. Use it to show what something used to say
before a change, beside what it says now.

A list item that starts with `[ ]` or `[x]` becomes a task with a tick box:

```markdown
- [x] Run the first cell
- [ ] Change the number and run it again
```

The box is there to be read, not ticked. Nothing saves what a reader clicks,
and the page records progress from the cells they run instead.

A single tilde is left alone, so `~1,000`, `about ~5 minutes` and a CSS
`:checked ~ .toggle` selector all reach the page as written.

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

## Questions

A quick check a student answers without writing any code — multiple choice, or a
sentence with a word or two missing. Write it as a ```` ```question ```` fence:

````markdown
```question
id: right-angle
type: multiple-choice
correct: 2

Which of these is a right angle?

- 45 degrees
- 90 degrees
- 180 degrees
```
````

`id:` is required, and is a contract on the same terms a cell id is — it is what
a student's saved answer matches on, so renaming it loses their answer the same
way renaming a cell's id would. `type:` is `multiple-choice` or
`fill-in-the-blank`, spelled out in full rather than abbreviated, so a question
is readable without a reference card. Everything after the header lines is
ordinary markdown, LaTeX included: for a multiple-choice question, the prose
before the list is the prompt and the list is the options, in the order a
student sees them.
`correct:` names the right one by its position in that list, starting at 1 —
that line, and only that line, is what a student's browser could read if they
opened the page's source, which is the trade this format makes: right for a
quick check, wrong for anything that has to keep its answer secret.

A fill-in-the-blank question has no `correct:` line. Write the sentence with
each missing word in curly brackets:

````markdown
```question
id: cell-basics
type: fill-in-the-blank

A cell's own {id} is the key its saved code is stored under.
```
````

That word becomes a typing box. Offer a short list instead, separated by `|`,
and it becomes a dropdown — the first item is the one a student is being
checked against:

````markdown
```question
id: angle-names
type: fill-in-the-blank

An angle of 90 degrees is a {right angle|straight angle|acute angle}.
```
````

A question with several gaps checks them all together, with one Check button
for the whole sentence.

Like `check()`, a question is formative: right or not-yet, no score, nothing
sent anywhere. Unlike a cell, it needs no Python and downloads nothing extra —
a page whose only interactive content is a question never loads Pyodide.

If a check calls for a picture in place of an option, or a graded, secret
answer, this is not that: see "Checking an answer" above for the first, and
dewmark (a separate program, for exams) for the second.

---

## Full-stack cells

A page whose own HTML shows a database's real rows, rather than a copy typed
in by hand. Write three fences with a shared `app:` name — `html app`,
`css app` and `js app` — the same `id:`/grouping shape a live HTML/CSS/JS
editor uses, `site:` swapped for `app:`:

````markdown
```sql exec
id: seed-products
CREATE TABLE product_tbl (product_id INTEGER PRIMARY KEY, product_name TEXT, price REAL);
INSERT INTO product_tbl (product_name, price) VALUES ('Mug', 8.5), ('Notebook', 3.0);
```

```html app
id: shop-html
app: shop
<table><tbody></tbody></table>
```

```css app
id: shop-css
app: shop
td { padding: 0.3rem 0.6rem; }
```

```js app
id: shop-js
app: shop
const rows = await dlQuery("SELECT product_name, price FROM product_tbl ORDER BY product_name");
root.querySelector("tbody").innerHTML =
  rows.map((r) => `<tr><td>${r.product_name}</td><td>€${r.price}</td></tr>`).join("");
```
````

Only the `js` pane is required — `html` and `css` are optional, and both are
live in the preview without pressing Run, the same rule a site editor's own
panes follow. Inside the JS pane, `root` is this cell's own piece of the
page (the same idea a site editor's own sandboxed preview has, without the
sandbox), and `dlQuery(sql, params)` runs one query against the page's
shared database — the same one every `sql exec` cell on the page reads and
writes — and returns its rows as an array of plain objects, one per row,
keyed by column name. `params` fills in any `?` placeholders in `sql`, so a
value that came from a reader — typed into a search box, say — is bound as
one value rather than pasted into the query's own text.

A full-stack cell is not a third site-editor pane language, on purpose: a
site editor (`html site`/`css site`/`js site`) previews inside a sandboxed
iframe specifically so a reader's script cannot reach anything else on the
page, and this cell's whole point is reaching the page's own database. Use
a site editor for a page that only needs live HTML/CSS/JS with no database
behind it, and a full-stack cell only where the point of the page is a
query's own result becoming part of it.

---

### Naming tables and keys

Every SQL table in a tutorial follows one convention, so a student meets
the same shape on every page and in every diagram:

- A table's name is singular and ends in `_tbl`: `product_tbl`,
  `book_author_tbl`.
- A primary key is named after its table: `product_id`, never a bare
  `id`. A foreign key takes the same name as the key it points at, so a
  join reads `ON product_tbl.product_id = sale_tbl.product_id`.
- Foreign-key columns sit directly under the primary key, before the
  other columns.

A table built straight from a published CSV keeps the CSV's own column
names; only its table name follows the convention. The reasoning is in
DECISIONS_LOG 7.212, and `dev/graphics/erd.py` draws every relationship
from the key's own row, which the convention makes readable.

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

### A toolkit the reader carries from page to page

An include shares *your* code. A toolkit cell shares the *reader's*: a
function they write on one page is there on every later page of the course,
before its first cell runs. Mark the cell with `toolkit: yes`, beside its
`id:`:

````markdown
```python exec
id: toolkit-binary
toolkit: yes
def to_binary(n):
    ...
```

```python toolkit-reference
for: toolkit-binary
def to_binary(n):
    return bin(n)[2:]
```
````

The second fence is the *reference*: the complete, working version, for a
cell that is a stub the reader fills in. It is never shown on the page. A
toolkit cell with no reference fence is its own reference, which suits a
cell that already works as written. `for:` must name a toolkit cell on the
same page, and a cell can have one reference fence; either mistake fails
the build. Only a Python cell can be a toolkit cell.

What a later page loads, and in what order:

- **Which pages count.** Every toolkit cell on a tutorial *before* this one
  in its course, across every series, in the course file's order — the same
  walk the Reference panel's glossary takes. A page's own toolkit cells are
  not loaded for it; the reader runs those themselves. A page on two courses
  uses the first course (in `courses/index.yaml` order) that has any toolkit
  cells before it. A practice page (`practice_for:`) is not in the
  course's order itself, so it loads the toolkit of its own tutorial *and*
  of every tutorial before that one. A mixed page (`practice_across:`)
  loads the toolkit of every tutorial it lists and of everything before
  the latest of them, in course order. A context page (`context_for:`)
  works the same way as a practice page.
- **Whose version.** By default, the reader's own: the code they saved in
  that cell on its own page, function by function. Each function your
  reference defines comes from the reference instead when the reader's
  code does not define it, or defines it with a body not yet written: only
  a docstring, `...`, `pass` or `raise NotImplementedError`. So a reader
  who wrote `to_binary` and left `to_hex` as your stub gets their
  `to_binary` and your `to_hex`. When their code raises an error, none of
  it is kept and the whole reference loads. The line at the top of the
  page's first cell names each function that came from the reference, and
  why. A reader can switch the whole site to the reference versions from
  that same line. A downloaded copy of a page cannot see the reader's work
  on other pages, so it always loads the references.
- **What runs.** The whole cell, not only its functions. Keep a toolkit
  cell to definitions: anything it prints or shows is thrown away when it
  loads on a later page, and a slow cell slows every page after it. Write
  a stub as a real `def` with a docstring and `...` in its body, so the
  reference can stand in for it until the reader writes it.
- **What the page gets.** Each toolkit cell runs in a space of its own,
  the way a module does: it sees the page's starting names and every
  toolkit cell loaded before it, and only the names it defines come back
  to the page. Its own `import` lines stay inside it, so one cell's
  `from itertools import product` cannot collide with a later cell's
  `def product(values)`, and a page cell that reuses a toolkit function's
  helper name (`RATE = ...`) does not change what the function sees. A
  page cell can still hide a toolkit function by giving its name to
  something else, as `total = 0` hides `total()`: pick cell names that
  leave the toolkit's alone.

The cell's `id:` and the tutorial's id are the key the reader's version is
found under, so the usual rule — never rename a cell id once students have
used it — matters twice over here: renaming one quietly swaps every later
page back to the reference.

---

## Linking between tutorials

```markdown
See [a table in Python](tutorial:working-with-tables#keeping-only-some-rows).
```

The build turns that into a real relative link. If the slug or the anchor does
not exist, the build fails rather than shipping a dead link for a student to
find. Headings and cell ids both count as anchors.

A tutorial can also link to a learning outcome directly, rather than to a
specific tutorial:

```markdown
As introduced in [Linear Functions](topic:MIT-3.2) ...
```

`build.py` resolves `MIT-X.Y` to whichever tutorial currently teaches that
outcome (`taught_where()`). If an outcome is removed or archived with
nothing left to take its place, the build fails rather than shipping a link
that points at nothing.

---

## Images, and other files a tutorial uses

Put the file in the tutorial's own folder and refer to it by its plain name:

```markdown
![A table sorted by date](a-sorted-table.png)
```

The build copies it to the site and makes that name resolve, from the current
release and from every frozen one. You never write a path — which matters,
because the current release and a frozen one are served from different depths,
so any path you wrote by hand would be right for one and wrong for the other.

The same holds for anything else a page loads by `src`: a recording, a short
video. A reference to a file that is not in the folder stops the build, for the
same reason a dead `tutorial:` link does — the alternative is a page that looks
finished to everyone except the student who opens it.

Every `<img>` needs an `alt` attribute or the build stops. An explicit `alt=""`
is accepted, and is how you mark an image as decorative.

---

## Practice pages

Every tutorial has a practice page beside it, at `<slug>-practice.md`, declared
with `practice_for:` in its frontmatter:

```yaml
title: "A Grid of Numbers — Practice"
practice_for: grid-of-numbers
year: "2026-2027"
version: 2026.08.24.1
```

A practice page is never listed in a course file: it follows its tutorial onto
every course that lists it.

The contents page links a tutorial to its own practice page, and the tutorial
links forward to it too, so practice is always one click from the material it is
practising.

A **mixed problem set** draws on several tutorials at once, declared with
`practice_across:` instead, and listed in the course file under `mixed:` so
the course page knows to show it:

```yaml
title: "Mixed problems: algebra and functions"
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
appears without one of these classes (or `dl-why`, below), so a fold cannot be
added without the styling that makes it work.

Write toward a few tools per section rather than a cell per problem — one
`python exec` cell holding the helpers a section needs, rather than sixty
editors on a page. **Every number in an answer gets run before it is published**,
not reasoned about. See
[`../planning/PEDAGOGICAL_STYLE_GUIDE.md`](../planning/PEDAGOGICAL_STYLE_GUIDE.md#6-practice-pages)
for the full shape of a good practice page.

### Why this way?

A tutorial can say why it teaches as it does, in a fold of a third kind:

```html
<details class="dl-why"><summary>Why this way?</summary>

The one choice this page made, the alternative it turned down and what
that alternative is good for, and what is at stake.

</details>
```

One choice, a few short paragraphs, closed until the reader opens it, so
a curious reader can see the reasoning and nobody has to read it to
finish the page. Plot Twist puts one on every tutorial, just before "Four
questions, looking back"; its plan's principle 10 has the reasoning.

---

## Context pages

A tutorial should be doable in about an hour. Background that a student does
not need to finish it — where the idea is used in the wild, why browsers
behave the way they do, a little history, the deeper detail — goes on a
**context page** beside it instead. Students can finish the tutorial without
ever opening it. (Common mistakes go on the practice page, not here; and a
tutorial that teaches two ideas is better split into two tutorials than
trimmed. `DECISIONS_LOG.md` 7.208 has the reasoning.)

A context page is an ordinary tutorial file in its own folder,
`tutorials/<id>/<id>.md`, like a mixed problem set. It names the tutorial it
gives background for with `context_for:`, as one id or a list:

```yaml
title: "Where Joins Show Up"
context_for: joins
year: "2026-2027"
version: 2026.09.22.1
```

```yaml
context_for:
  - joins
  - joining-two-real-tables
```

A tutorial can have more than one context page. It sits off the reading order
the way a practice page does: it has no previous or next, it is not a search
result, it sits in the tree under the first tutorial it names, and its
Reference panel holds everything those tutorials have taught, followed
by the terms it defines itself, from its own `<id>.glossary.yaml`.

**How it links.** Each tutorial it names gets a short block after its practice
link, naming the context page and saying that nothing in it is needed to
finish the tutorial. The context page opens with a line naming those
tutorials, again saying it is optional. The contents page lists it beside each
of its tutorials, after the Practice button, with a small "context" tag.

**What the build refuses**, each with a message naming the file:

- an id in `context_for:` with no tutorial behind it;
- naming a practice page or another context page — name the tutorial;
- naming itself, or naming one id twice;
- setting `practice_for:` or `practice_across:` as well — a page is
  background or problems, not both;
- declaring `covers:` — nothing on a context page is needed to finish a
  tutorial, so it is never where an outcome is taught;
- a course file listing it. It follows its tutorial onto every course, the
  same as a practice page.

---

## The Reference panel and glossary files

Each tutorial has a `<slug>.glossary.yaml` beside it listing the terms,
functions, operators and formulas that tutorial introduces for the first time in
its series:

```yaml
entries:
  - term: matrix
    kind: concept
    definition: A matrix is a grid of numbers, arranged in rows and columns.
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
| `image_input(label="Choose an image", id=None)` | A picker limited to image files. `.value` is a Pillow `Image`, or the raw bytes where Pillow is not loaded. |
| `await load_csv(name)` | Load a CSV from `data/` into a DataFrame. |
| `await load_text(name)` | Fetch a plain-text file — from `data/`, or a full URL — and return its contents as a string. |
| `run_query(conn_or_path, sql, params=None, max_rows=20, caption=None)` | Run a SQL query and render the result as a table. Takes an open `sqlite3` connection or a path to pass to `sqlite3.connect()`. |

Widgets keep their values when a cell is re-run, so a student can type an answer,
press Run, and still see what they typed.

**Two of the four widgets need Python on the page's own thread, and the
hosted site runs it in a Worker** (`DECISIONS_LOG.md` 7.77 — that Worker is
what makes a real Stop button possible). `text_input` and `dropdown` work on a
hosted page: the page watches the control and posts each change to the
Worker, and the next run reads the value. `button` and `image_input` have to
call Python the moment they are used, with no cell running, and there is no
DOM on the far side of a `postMessage` boundary to hand them one; they raise a
clear `RuntimeError` on a hosted page, and work in a downloaded **Download to
keep** copy, which runs on the main thread
(`tests/e2e/test_phase0_golden_path.py` shows both).

`numpy`, `pandas` and `matplotlib` are available in every tutorial without
importing anything special — they load with the page.

**A matplotlib animation renders as a moving picture.** Build one with
`FuncAnimation` and make it the cell's last expression, or pass it to
`show()`, and the page shows it as an animated PNG that loops: every frame
the animation would have drawn, at the frame rate its `interval` asks for,
with the same transparent background a still figure gets. The figure it was
drawn on is not shown again as a still. Keep animations short — a few dozen
frames of a small figure is a few hundred kilobytes in the page, and every
frame is rendered in the reader's browser when the cell runs. Pillow, which
does the encoding, is on every page already.

---

## Releasing a new version

Most edits — fixing a typo, clarifying a sentence, correcting a bibliography
entry — are just a commit. Bump `version:` only when you change what a cell
does, so a student's saved progress can tell the page moved on.

Where a change is substantial enough that students already partway through the
old version deserve to keep working in it undisturbed — a rewritten explanation,
cells replaced rather than tweaked — publish it as a release instead of editing
in place:

1. Copy the current `<slug>.md` to `v<old-version>.md` in the same folder,
   unchanged. That is the release students keep working in.
2. Bump `version:` in `<slug>.md` and write the new material there.

Nothing moves and nothing is renamed: `<slug>.md` is always the current
release, and a past one is always `v<version>.md` beside it. The authoring
editor's **Release** button does exactly these two steps.

The build serves the newest release under the tutorial's plain, unversioned
address, and every past release stays reachable at its own
`<id>/v<version>.html`, frozen as it was. A reader sees a small version picker
wherever more than one release exists, and the contents page, the topic tree and
every `tutorial:` link always resolve to the current one. Frozen releases get no
downloadable copy of their own, since a downloadable snapshot of superseded
material is not worth shipping.

`TestVersionsOfATutorial` in `tests/build/test_releases.py` pins down the
exact behaviour.

---

## Adding a new module

A module is a course file. Create `courses/<id>.yaml` with a `title`, a
`code`, a `status`, the `card` text for the front page, a `description` for
the course's own page, and `contents` — its series, each with its tutorials
in order — then add the id to `courses/index.yaml` where it should appear.
That is the whole procedure: nothing in `build.py`, nothing in any tutorial.
The tutorials it lists may already be on another course.

---

## The site's own pages

Three pages are written by hand rather than built from tutorials: the home
page, the About page and the features page. Each is one markdown file under
`pages/` — `home.md`, `about.md`, `features.md` — with a frontmatter of one
field, `title:`, and nothing else. The body is ordinary markdown, converted
the way a tutorial's prose is, and every word on it is student-facing, so
the plain-language rules in the style guide apply.

A page can hold three things ordinary prose cannot:

- A tile linking somewhere, as a ```card fence: header lines `url:` (the
  link), and optionally `status:` (a badge), `meta:` (small text under the
  heading) and `wide: true` (two columns wide), then a markdown heading and
  a paragraph. Tiles next to each other share one grid.
- `[[search-box]]`, the live search, and `[[course-cards]]`, one tile per
  course from the course files in `courses/index.yaml` order. Write the
  marker on a line of its own; the build fills it.
- A `<div class="dl-hero">`, `<div class="dl-audience">`,
  `<div class="dl-attribution">` or `<ul class="dl-feature-list">` wrapper,
  with a blank line after the opening tag and before the closing one, so
  the markdown inside it still converts.

To change what a page says, edit the file and run `python3 build.py`; the
page is `site/<name>.html` (`site/index.html` for the home page). Adding a
fourth page is one file plus one line in `SITE_PAGES` in `build.py`.

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
every tutorial by title, id or course and inserts a real link at the cursor,
so you reach for a tutorial that exists rather than typing a slug from memory.
Its code cells offer keyword and locally-typed-name completion as you write. Open
the same tutorial as a student and their cell offers the same completion plus a
hover docstring, read off whatever the setup cell imported and whatever the
student has defined so far.

---

## Before you open a pull request

Run `python3 check.py tutorials/<id>` (or `courses/<course>.yaml`) and fix
every line that starts with *Problem*. When it reports none, it offers to
open the pull request for you — [`CHECK_YOUR_WORK.md`](CHECK_YOUR_WORK.md).

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
