# Editing a page where it stands

*A plan, October 2026. Nothing here is built. It is written to be argued with.*

## The proposal

A teacher opens any tutorial, practice page or hand-written page, chooses
**Edit this page** in Settings, and the page becomes typeable. Nothing moves.
The text is in the same font at the same width, the cells are the cells, and
the only visible differences are a caret and an outline on the block being
edited. When they are done, one button in Settings turns their changes into a
draft pull request, exactly as `editor.html` does now.

That is the whole feature. The rest of this document is about three things
that make it harder than it sounds, and one that makes it easier:

1. The page is generated from the markdown, so there is no document in the
   browser to edit. Something has to say which piece of the page came from
   which piece of the source.
2. Several planning documents, `CLAUDE.md`, and a few of the build's own
   refusals describe the old arrangement and would now be wrong or in the way.
3. Some of the test suite checks house style rather than function.
4. The easier thing: the repository already has a GitHub client, a block
   editor that writes the project's markdown, and a tier of "advisory" checks
   that never block a merge. Most of the machinery exists. The work is joining
   it to the rendered page.

---

## What exists

`assets/editor.js` (1,071 lines) is a GitHub client plus an editor UI, served
as `editor.html` and linked from nowhere a student goes. It fetches every file
under `tutorials/`, edits one body at a time with Milkdown's Crepe preset
(`vendor-src/milkdown-entry.js`), checks the result (`problems()`), and opens
a draft PR with a fine-grained token the author pastes in. The token is the
access model: GitHub decides who may have one.

Three details of that code matter here.

- Crepe reads its document once and cannot swap it in place, so every change
  of document destroys and rebuilds the editor (`ARCHITECTURE.md` §3).
- Crepe keeps only the first word of a fence's info string, so `python exec`
  loses its `exec`. `restoreExecTag()` puts it back on the way out.
- `milkdown.bundle.js` is 2.9 MB. It must load when a teacher presses Edit and
  never before. A student's page must not get heavier.

The editor also does things an in-page editor does not obviously replace:
reordering a series, changing frontmatter and status, releasing a version,
searching tutorials to insert a link, creating a page. Those are a later
question (see *Order of work*), not a reason to hold up the first one.

---

## The hard part: the page is not the document

I built the site and compared, for each of the 494 tutorial pages, the number
of blank-line-separated blocks in the markdown with the number of top-level
elements in the rendered `<main id="dl-body">`. They agree on 36. The median
page has 91 markdown blocks and 57 rendered ones. So the obvious plan, walk
the page's children alongside the source's blocks and pair them off, fails
on nearly every page. The causes are ordinary: a hint or solution fence
belongs to the cell above it and renders inside it, a `{{include: …}}` expands
into text that is not in the file, a world variant wraps its blocks, a list
with blank lines in it is one element, a `<details>` fold is raw HTML that
the build treats as opaque.

My splitter was crude, so read the number as "positional matching is not
viable", not as a measurement of anything finer.

Three ways to make the page editable:

**A. Make the rendered DOM `contenteditable` and convert it back to
markdown.** This gives the best "no visual change" and the worst fidelity.
HTML to markdown loses what the build added (placeholders, ids, wrappers,
`markdown="1"` marks) and cannot recover what it consumed (includes, fence
headers). Every save would be a guess. Rejected.

**B. Keep the rendered page and, for the block being edited, swap the
rendered HTML for an editor seeded with that block's markdown.** The rest of
the page is untouched. The swapped block is styled to look the same as the
page it replaced. When the teacher leaves the block, its new markdown is
spliced into the source at the block's byte range, and the block is
re-rendered. This needs the build to say which source range each rendered
block came from.

**C. Overlay a separate editor on top of the page.** No fidelity problem, but
it is the existing `editor.html` with extra steps. It does not meet the
"nothing changes" requirement. Rejected.

**Recommendation: B, with a source map emitted by the build.** The rest of
this plan assumes it.

### The source map

`build.py` already pulls fences out before markdown sees them
(`extract_blocks()`) and puts them back afterwards. It would also record, for
each top-level block of the body, a start and end offset into the file as
committed, and write them onto the rendered element as `data-src="1204:1388"`
(with a block kind where it helps: `prose`, `cell`, `fold`, `include`,
`html`). Anything the build expands or wraps keeps the range of the source it
came from: an include is one block whose range covers the `{{include: …}}`
line and which is marked not editable in place; a cell's hint, solution,
inputs and predict fences share the cell's range and are edited with it.

Two properties the spike has to prove before anything else is built:

- **Every range round-trips.** For all pages, splicing a block's own text back
  over its own range changes nothing. This is a pytest in `tests/build/`,
  runs without a browser, and is the first test to write.
- **The offsets are for the source the page was built from.** A page on the
  live site may be a day behind `main`. The build therefore also writes the
  file's git blob sha onto `<main>`, and the editor fetches that blob by sha
  (the Git Data API serves any blob by sha), so the offsets are always valid.
  At save time, if `main` has moved on for that file, the first version stops
  and says so rather than trying to merge. A later version can re-find blocks
  by content.

The attribute costs bytes on every page. I have not measured the cost. The alternative, a separate `.map.json` per page fetched only on Edit, is
available if the cost matters. I would start with the attribute because it is
easier to test and debug.

---

## What is on a page

Before deciding what to edit in place, I counted what the 494 tutorial pages
contain. Counts are of uses across all pages, and of pages that have at least
one. (Earlier release files, `v<version>.md`, are left out.)

| Block | Uses | Pages |
|---|---|---|
| Headings, bullet and numbered lists | thousands | 384 to 494 |
| Python cell (`python exec`) | 3,003 | 370 |
| `<details>` fold (the hint and answer folds) | 3,388 | 360 |
| Inline maths (`$…$`) | 11,379 | 283 |
| Illustrative code (a Python fence that does not run) | 943 | 207 |
| World variant (`<div class="dl-world">`) | 1,090 | 201 |
| Solution fence | 825 | 200 |
| Predict fence | 385 | 195 |
| Inputs fence (the comparison table) | 638 | 179 |
| Hint fence (staged hints) | 653 | 172 |
| Table | 2,331 rows | 182 |
| Question fence | 1,121 | 148 |
| Display maths (`$$`) | 521 | 147 |
| Note (`<aside>`) | 124 | 106 |
| Site editor (`html`/`css`/`js` site) | 404 panes | 86 |
| Image | 60 | 56 |
| `{{include: …}}` | 193 | 69 |
| Toolkit reference | 50 | 38 |
| SQL cell | 54 | 17 |
| Full-stack app cell | 8 panes | 2 |
| Typed fence, project div | 1 and 5 | 1 each |

Two conclusions. First, the blocks my first draft left to "later" (folds,
hints, solutions, predictions, questions, world variants) are not
decoration. They are on a third to a half of all pages, and a teacher fixing
a page will meet them as often as a paragraph. They belong in the first
version, at least as editable source text. Second, the bottom of the table
(app cells, typed fences, projects) is on one or two pages each and can stay
source-only for as long as that is convenient.

**What an include is for.** It is not a way of including other tutorial pages.
It pastes a file from `setup/` into the page before the markdown is read. It
has two uses, and they are different problems:

- **Shared setup code, about 120 of the 193.** A cell loads the same dataset
  or defines the same helper (`setup/matrices/transform.py`, `setup/cube.py`)
  and the file sits in `setup/` so that a dozen pages do not each carry a copy.
- **Shared prose, 71 of the 193.** Almost all of them are one file,
  `setup/zen-calm-check.md`, the "A calm check" box that appears on 69 pages.
  Two more pages include a short note on what to do when a cell does not do
  what you expect.

Either way, the included text is not in the page's own file, and editing it
changes every page that includes it. That is usually what the author wants
(change the calm check once, not 69 times), but it means an in-place edit
would reach well beyond the page the teacher is looking at.

---

## What a teacher sees

**Where the button is.** At the very bottom of the Settings panel, below
everything else, a small **Edit this page** button. It is visible to
everyone and meant to be seen by few: nobody scrolls that far unless they are
looking for it, and a student who finds it loses nothing. Settings has three
tabs (Appearance, Behavior, Imports & Exports), so it sits at the foot of
whichever tab is open, or in a short footer row the panel already has room
for; the choice is a layout detail for the build. Once editing, the same
spot shows what is pending (three blocks changed), a **Discard** button and an
**Open pull request** button. All the new chrome stays in the panel the page
already has and the page itself is left alone, which is the requirement.

**How a teacher finds out how to use it.** Next to the button is a collapsed
**How editing works** fold, in the style the Settings panel already uses for
its other details, and a link to a page in the repository that says the
same at more length. Both cover: what the button does, that it opens a draft
pull request and never changes the live site by itself, what a GitHub token
is and the exact permissions it needs (contents and pull requests, write,
this repository only), how to get one, and that adding `#edit` to any page's
address switches editing on directly. That link target is a new document,
written for a teacher who has never used GitHub, and is part of the first
version, not a follow-up. The `#edit` address and the button do the same
thing; the address exists so a teacher can bookmark or send it.

Because students can see the button, its label and the fold's wording count
as student-facing and follow `PEDAGOGICAL_STYLE_GUIDE.md#voice`. Pressing it
without a token shows the token prompt and the same explanation, never an
error.

**What editing looks like.** Pressing Edit does not rebuild the page. Click
into any block and that block becomes live: caret, normal typing, the same
typography. The block the caret is in gets a one-pixel outline in an existing
accent token, drawn with `outline` so it takes no space and nothing reflows.
Moving the caret to another block commits the first and opens the next.
Escape leaves editing.

**What can be edited, and how.** Not every block should be a rich-text field.

| Block | First version |
|---|---|
| Paragraphs, headings, lists, links, emphasis, inline code, tables | In place, Crepe styled as the page |
| Code cell (`python exec` and the other kinds) | In place, using the CodeMirror editor the cell already has. Saving writes the fence back with its header lines (`id:`, `hint:`, `toolkit:`) untouched |
| A new cell | A slash command inserts one. The editor generates its id from the nearest heading and a counter; the teacher never types one |
| Maths (`$…$`) | Click shows the TeX source in a small field; the rendered maths stays on the page. Whether the vendored Crepe build includes its maths feature is part of the spike |
| Image | Replace text and alt in place. An alt is asked for when an image is inserted |
| Hint fence, solution, predict, inputs, question, note, `<details>` fold, world variant | Hint, solution, predict, inputs and question: edited as their source text in a plain box under the block, then re-rendered. A `<details>` fold and a note: the prose inside is edited in place like any prose; the fold's open/closed state and class are not touched. A world variant: its wrapper is untouched and the blocks inside are edited as their own kind. Rich editing of the fences (a form for a question's options, say) follows once the box has been used |
| `{{include: …}}` | Shows a small link to the included file on GitHub (see below). Not editable in the page |
| Generated blocks (`[[search-box]]`), the glossary, the page chrome | Not editable here. The outline does not appear, and a tooltip says why |
| A frozen `v<version>.md` page | Not editable. The button says it is a past release |
| Generated pages (contents, tree, map, all-notes) | The button does not appear |

Cell ids deserve a line. With the rename warning no longer the main concern
(see *Assumptions*), the in-page editor handles ids by never showing them for
existing cells and generating them for new ones. That costs nothing and keeps
the ids that do functional work (hints and solutions find their cell by id;
two cells with one id break a page) correct without anyone thinking about
them.

**Fidelity of what Crepe writes back.** Crepe re-serializes markdown in its
own style: `*` bullets become `-`, a line wrapped at 80 columns may come back
on one, escapes appear. If the whole file went through it, every save would be
a diff across hundreds of lines nobody touched. Because B splices only the
edited block's range, untouched text is byte-identical and the review diff is
the teacher's change. Within an edited block some normalisation will remain.
The spike measures how much by loading every prose block of every tutorial
into Crepe and serializing it unchanged; I expect a minority of blocks to
differ and I want the number before choosing between tolerating it and
tuning Crepe's serializer.

---

## How a change reaches the repository

Reuse `githubClient()`. Move it, `splitFrontmatter()` and the other pure
helpers out of `editor.js` into a module both the old editor and the new one
import, so there is one GitHub client, not two. The new editor adds a
`splice(source, edits)` function: given the blob text and a list of
`{start, end, text}`, apply them from the end backwards.

Saving works as now. One branch per editing session, one commit per save,
a draft PR against `main`. Further saves in the same session add commits to
the same branch. No token reaches any server of ours, because there is none.

One security note, to be accurate rather than alarming. `localStorage` is
per origin, not per path, so the token `editor.html` stores is already
readable by script on any page of the site, including the app cells that run
author-written JavaScript in the page itself. The in-page editor does not
widen that. It does make it worth saying in the docs that the token is
fine-grained, scoped to this repository, and cannot merge.

**Where the code lives.** A new module, inpage-editor.js in `assets/` (not yet written), imported
dynamically when Edit is pressed. The Settings section is markup in
`assets/shell.html`, and the handler that loads the module can live in a
small separate script. The reason is the trap in `CLAUDE.md`: any edit to
`assets/tutorial-runtime.js` means rebuilding the standalone bundle with Node
or CI fails. The in-page editor should not need to touch the runtime, and
a downloaded copy of a page ("Download to keep") must not contain the editor
at all, since a downloaded page has no repository to write to.

---

## Documents and checks that will disagree

These say things the new arrangement makes untrue. Each needs a change in the
same pull request that makes it untrue, per `CONTRIBUTING.md`.

| Where | What it says | What changes |
|---|---|---|
| `ARCHITECTURE.md` intro and §3 | Three programs; the authoring editor "is never linked from a student page" and runs in its own tab | The editor now has two surfaces. The "never linked" claim goes; the section describes the source map, the swap, and the splice |
| `assets/editor.js`, the token gate text | "This page is never linked from anywhere students go" | Reworded once the entry point changes |
| `docs/WRITING_TUTORIALS.md`, "The authoring editor" | A tab at `/editor.html`, for changes "that do not need a local checkout", and "believe" the rename warning | Describe editing a page in place as the main route; keep a short line on `editor.html` for what only it does until that is retired |
| `docs/WRITING_TUTORIALS.md`, cell ids | "The editor warns about this; believe it." | See *Assumptions* |
| `CLAUDE.md`, "Two traps" | Renaming a cell id or a tutorial id throws away saved work | See *Assumptions*. The second trap (rebuild the vendor bundle) stays true |
| `docs/HOW_DEWLAB_THINKS.md`, "What the machine holds you to" | The first tier, "ids are contracts", is a list of blocking rules | Rewritten against the new list of what blocks (below). The doc already says advice and enforcement are different kinds of thing, so this is an edit, not a reversal |
| `docs/CHECK_YOUR_WORK.md`, `check.py` | Problem / Note output a contributor reads in a terminal | `check.py` is the same logic the editor needs in the browser. Decide whether the editor calls a JavaScript port (`problems()` today) or whether the two are generated from one list |
| `planning/PEDAGOGICAL_STYLE_GUIDE.md`, "Before a page ships" | A checklist for a person | Unchanged in content. Its role changes: it is now also what the editor links to from a warning, and what the LLM review reads (below). Worth one sentence at the top saying so |
| `DECISIONS_LOG.md` | Entries on the editor, the cell-id contract (7.23), the structural fold rule (7.52), advisory tests (7.291) | One new entry for this decision. The entries it supersedes get a pointer forward, not a deletion |

One more constraint comes from `CLAUDE.md` itself. The words on the Edit
button and in its Settings section appear on every page a student opens, so
they count as student-facing and follow `PEDAGOGICAL_STYLE_GUIDE.md#voice`.
The editor's own warnings are for teachers, not for the course's reader, and
I would write them in plain words by the same standard but not hold them to
the rules about predictions or verdicts. That distinction should be written
down once, in the style guide's opening, because the next person will ask.

---

## The tests

### The principle

You said a test should check only whether code runs and whether the interface
shows errors. `docs/tests-explained.md` already holds a rule close to that,
as its sixth question: *would a page still build and teach well if the test
failed? Then it checks a preference, not a fault; mark it advisory.* And
`DECISIONS_LOG.md` 7.291 did a first pass. So the starting point is better
than "tests enforce style everywhere". The job is to finish the pass, using a
sharper statement of the rule:

> A check blocks a merge only if its failure means a page does not load, a
> cell cannot run, a link or asset points at nothing, a number the page states
> is wrong, or the interface shows a console error or breaks its layout.
> Anything that depends on what the author meant is not a test.

### What I found, and what I did not

I read the unit and build tests' relationship to the real tutorials, the CI
workflow, and a sample of the build's refusals. I did not read all 177
`fail(…)` sites in `build.py` or every file in `tests/build/`. The first task
below is to do that properly. What I saw:

- Nearly all of the build's refusals I read are structural: frontmatter that
  does not parse, a fence that does not close, a hint naming a cell that does
  not exist, a toolkit fence with no target. Those stay.
- Only a few test files read the real `tutorials/` folder at all.
  `test_handwritten_classes.py` fails if a page uses a `dl-` class the
  stylesheet has no rule for. That is a visible fault (unstyled markup), so
  it stays, and it is a good example of the rule. `test_courses.py` checks
  that every real tutorial is reachable from a topic group. That is a
  planning-document check; it should be advisory. `test_curriculum_map.py`
  already is.
- Some refusals sit closer to convention than to breakage.
  `HOW_DEWLAB_THINKS.md` says so about the `<details>` fold rule. Alt text
  on images is the one I would argue for keeping as a blocking rule on its
  own merits, since it concerns a reader who cannot see the picture. In the
  editor it should be asked for at the moment an image goes in, so it is
  rarely a build failure. I would keep the build refusal as the backstop.
- `check.py` prints Notes. Those already do what you want: report, never
  block.

### Where a style signal goes instead of a test

Three places, in order of how early the author sees them.

1. **In the editor, as it happens.** A small marker beside the block, with a
   sentence and a link to the style-guide section. Examples: a cell with no
   hint position, a sentence containing a verdict word, a heading with a
   trailing colon. These can be cheap string checks because they are only
   suggestions and are wrong sometimes. They never prevent a save.
2. **In the pull request, as an LLM review.** See below.
3. **In `check.py` and the advisory CI job,** as now.

### What the editor itself needs tested

- `tests/build/`: the source map. Every range round-trips; includes, worlds,
  hints and folds keep the ranges described above. Pure Python, runs in CI.
- A new browser test file, test_inpage_editor.py in `tests/e2e/`, with the fake GitHub client the current
  `test_editor.py` already uses: open a page, edit a paragraph and a cell,
  confirm the commit body differs from the original only inside those two
  ranges, and that nothing about the page's layout box changed (compare
  bounding rectangles before and after pressing Edit, which is the "no visual
  change" requirement stated as an assertion). These do not run in CI today;
  `ARCHITECTURE.md` §6 says the e2e suite is a local step. I would add this
  file to the short list the CI `browser` job names, because it is the only
  place the round trip is proven end to end.
- `test_page_smoke.py` already checks for console errors on every template.
  Add one case with edit mode on.

---

## Checking the prose after the fact

Your example, a heading that runs on to the next line because a closing mark
did not close, is a good one. A pattern match would flag it on pages where the
author meant it and miss it on pages where the cause is different. A reader
can tell at a glance, and a language model can too. Two parts:

- **A skill**, page-review, in the shape of
  `cell-code-review` (a new folder under `.claude/skills/`). It reads a changed tutorial against the style guide and
  looks for what a script cannot: a heading that is really a sentence or has
  swallowed the line below, a list that stopped being a list, emphasis left
  open, a fold that opens and never closes, a verdict word that crept in. It
  reports with the line, the reason and a suggested fix, and changes nothing.
- **No workflow yet.** The skill is run by hand, on request, against a
  changed page. That is your choice: no secret, no cost, and the chance to tune
  what it flags on real pages before anything posts to a pull request. If
  teachers' PRs start merging unreviewed, a workflow that runs the skill and
  comments (never a failing check) is the next step. Whether it should use
  the Claude review the repository may already have, or a new workflow with its
  own secret, can wait until then.

The WYSIWYG itself catches many of these first. A heading that swallowed a
line is visible the moment it is typed. The review is for what the author did
not notice.

---

## Order of work

Each step is a pull request that stands alone.

1. **Audit and the test principle. Done (DECISIONS_LOG 7.295).** Most of the
   sorting had been done in 7.291. Running twenty-four plausible teacher edits
   through the real build found two refusals in the wrong place. A bare
   `<details>` now builds, with its markdown converted, and the build says
   so in a note. An unclosed code fence, which silently turned the rest of a
   page into code, is now refused by the build and by `check.py`. The block and
   advisory lists in `HOW_DEWLAB_THINKS.md` and `tests-explained.md` were
   rewritten around one rule, and the claim that an `<img>` without `alt` always
   fails was corrected.
2. **The spike.** The source map in `build.py` and its round-trip test. Then
   a throwaway page that swaps one prose block and one cell and splices them
   back. Measure Crepe's normalisation across the corpus. At the end of this
   step we know whether B works, and what it costs, before building the UI.
3. **Edit mode on prose and cells.** The button, the how-to fold and the
   teacher's guide it links to, the `#edit` address, the swap, the outline,
   save to a draft PR. `ARCHITECTURE.md` and
   `WRITING_TUTORIALS.md` updated in the same pull request.
4. **The other blocks,** as source-text boxes first, in the order of the
   counts above: `<details>` folds and solutions, then hints, predict and
   inputs, then questions and world variants, then notes. Rich forms for any
   of them after that.
5. **The review skill,** run by hand, which can start any time after step 1. A workflow is later, if wanted.
6. **Retire `editor.html`'s overlap.** Move series reordering, frontmatter,
   release and the link picker to wherever they should live (some may belong
   in the in-page editor, some in a small admin page that stays). Delete only
   what has a replacement.

The next step is 2.

---

## Assumptions I made, and questions I could not settle

**Decided: saved student work is out of scope.** I took your statement to mean
that nobody is relying on any cell id or tutorial id today, so the plan does
not design around them. I did not propose deleting the id rules, because ids
do two jobs. One is keying saved work, which you have set aside. The other is
letting a hint, solution or test find its cell and letting two cells on a page
be told apart, which stays. In the documents above I would reduce the
saved-work warning to a plain statement of fact and put one line in the
decisions log saying it was dropped as a priority in October 2026 and why, so
that the day a class starts relying on a page, the reason to restore it is
findable. You chose this over removing the rules entirely or keeping the full warning.

**Decided: the button is always there, at the foot of Settings, with a how-to fold and a link, and `#edit` also works.** See *Where the button is*.

**Decided: includes link out to GitHub.** You said you do not mind this, so the plan takes the cheapest option: an included
file is not editable in the page, and shows a small link that opens that file in
GitHub's own editor, with the path visible so the teacher can see it is shared.
That covers both uses, and it keeps an edit to one page from silently changing
69 of them. The cost is that a teacher changing a setup cell leaves the page
for that one block. Editing the included file in place, with a warning that
N pages use it, is possible later and needs the save to write two files.

**Decided: one pull request per editing session.** One branch and one draft
PR, each save adding a commit, so three typo fixes on three pages arrive as one
review. The cost is keeping the branch name between page loads, in
`localStorage`; a stale branch from an earlier session needs a sensible
message when a teacher returns to it.

**Decided: the hand-written pages are editable, prose only.** On `pages/*.md`
(home, about, features) paragraphs, headings and lists edit in place. Cards
and generated markers open as source text, like a hint does.

**Decided: phones get one real-device test in the spike, not a design.** Typing
into a block with the settings panel as the only chrome may be awkward, and the
spike will say how awkward before any effort goes into it.
