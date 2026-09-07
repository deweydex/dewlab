# Hints that know what the cell has done: a design note

Written 2026-09-06, in response to Josh asking, for dewlab and dewstack
together, "what type of infrastructure would be necessary for the text to
be at least somewhat aware of what the student has run or done to a given
cell on the page" — so that after an error has appeared some number of
times, or a cell has run some number of times without reaching a result,
the page can offer a "pause and ponder" fold with a question, then steps,
then perhaps pseudocode, and a while later another; "kind of like Khan
Academy's hints but a bit more engaged and pedagogically more open,
inviting the learner to form certain habits that we can specify."

**Built on dewlab, 2026-09-06 — see §12 at the end for what was decided
and how it differs from the design below.** The rest of this note is the
design as it was written before Josh answered its questions; §9's list is
kept as the record of what was asked. The note says what already exists in both
repositories to build on, what a page can observe without any new
plumbing, what the authoring surface could look like in markdown, how the
same idea lands on dewstack's three cell kinds, where to try it first, and
what the notebook grading systems do that is worth borrowing or avoiding.
Section 9 is the list of choices that are Josh's to make; section 10 is
the rollout once they are made. A companion note in dewstack,
`planning/CELL_HINTS.md`, covers only what differs there and points back
here for the rest.

---

## 1. The request, restated as behaviour

A reader is working on a cell. They run it and get an error. They change
something, run again, same error. A third time. Today the page does
nothing new: the same traceback, the same `?` hint they may or may not have
opened. The request is that on the third identical error a fold appears
under the cell, closed, with a summary like *pause and ponder*, and inside
it a question — not the answer — that points at the habit a stuck reader
most needs right then: read the last line of the error first; change one
thing and run again; print the value you are unsure of. If they are still
stuck after several more runs, a second fold with more concrete steps. If
the tutorial has an answer fold already, that stays where it is: the last
resort, not the second.

Two things the request is not. It is not grading: nothing is scored,
nothing leaves the browser, and section 11 of the style guide (struggle and
self-worth) says a count of failed attempts must never be shown to the
reader, since a number on a cell is a verdict whatever the caption says.
And it is not an answer engine: the hints are written by the author, per
cell, in the tutorial's own voice, the same way `hint:` and the `dl-hint`
fold already are. The infrastructure decides *when* a hint appears. The
author still decides *what* it says.

---

## 2. What already exists to build on

Most of the signal is already in the page. The list below is what a
reader of `tutorial-runtime.js` and `tutorial_tools.py` finds today, with
the dewstack equivalent where there is one.

**A per-cell `hint:` in the cell header** (`build.py` `HEADER_RE`,
`render_cell()`), shown behind a `?` toggle as `.dl-hint-text`, a plain
block in normal flow below the cell's bar — DECISIONS_LOG.md 7.67 turned it
from a hover popover into a click toggle, and that push-down shape is the
one a staged hint should reuse. Its text is one line, escaped, no
markdown, no maths.

**The two folds** (`docs/WRITING_TUTORIALS.md` "Answers and hints",
DECISIONS_LOG.md 7.52): `<details class="dl-hint">` holding numbered steps
that end in a **Think about** and a **Try this next**, and
`<details class="dl-answer">`. Both take markdown and maths inside them,
because the build pulls code and `$…$` out before markdown runs. The build
fails on a `<details>` with neither class. This is already the house shape
for "a route when stuck", and Josh's own description of the new thing —
"a dropdown which might include text (or pseudocode…)" — is this fold.

**`check()`** (`tutorial_tools.py`): pass or not-yet feedback, tolerant of
floats, and it records `cell.last_check = (position, passed)` on the cell
context for the duration of the run — today only so a trailing `check(...)`
does not also print `True`. That tuple is a per-run "did the check pass"
signal that already exists in Python and is thrown away at the end of the
run. dewstack's equivalent is the `sql-check` block, a separate
"Check my work" button per task calling a `check_*` function in
`dewstack/assets/sql_tools.py`, not something a cell's own run reports.

**`run_cell()` returns a boolean**: True if the code raised nothing. The
Worker path (`pyodide-worker.js`) carries that back as the `result` of a
`response` message. So the JavaScript side already learns, per run,
whether the run errored — and independently reads `.dl-error` out of the
output to set `errored` in the saved record. Two sources for the same
fact; either will do.

**`_ERROR_HINTS` and `render_error()`**: a short table of error messages
that get a plain-English note under the traceback. This is the only
place today where the page reacts to *what* went wrong rather than *that*
something went wrong. It is deliberately tiny (the comment above it says
why) and it is keyed on message text. A staged-hint system should not
grow this table; it is a different thing, author-written per cell rather
than site-wide per message. But it shows the seam: `render_error()` is
where the exception type and message are in hand.

**The run-line** (`renderCellRunLine()`, planning/CELL_IDENTITY.md §3):
`cell.ranOrder`, `cell.lastRunMs`, and `cell.ranContent` — the code as it
was when it last ran, kept so the line can say "edited since". That last
one gives a signal nobody asked for but which matters more than the error
count: *the reader ran the same code again without changing it*. Three
identical errors on three identical runs is someone hoping; three
different errors on three edits is someone working. The hints those two
readers need are different, and the page can already tell them apart.

**The saved-work record** (`saveNow()`, keyed
`dewlab:progress:<module>:<slug>`): per cell, `task_id`, `student_code`,
`output_html`, `errored`, `collapsed`. Written after every run. Exported
and imported as a file, read by the contents page's progress badge and by
Settings. Its shape is a contract with those readers and with the
export/import tests, but it is additive: a new per-cell field is ignored
by every existing reader.

**The notes nudge** (`updateNotesNudge()`, planning/STUDENT_NOTES.md §4):
a small dot on the export button once notes have grown past a threshold
since the last export. The precedent for "the page changes because of
what the reader has done, quietly, without a count on screen", and for
keeping the state that drives it in its own small key rather than
widening the save record.

**Custom cells** (planning/PRACTICE.md §5): a reader can add a runnable
cell at runtime on any page that has cells. So a hint that contains a
runnable cell is not out of reach; the engine to mount one exists. It is
a later stage, not the first.

**On dewstack**, `dewstack/assets/sql-cell.js` runs all three cell kinds on one
Pyodide, main thread: `run_sql()` and `run_python()` each return an HTML
string, and an error is a `.dl-sql-error` or `.dl-error` element inside
it. Only a persisted SQL cell saves anything to `localStorage`. The web
track's site editor (`dewstack/assets/site-editor.js`) has no Run for HTML and CSS — they
are live — and a Run for the JavaScript pane, whose errors arrive on the
console relay with a line number. `sql-check` blocks report pass or fail
per click. There is no run-line and no per-cell save record, so a
counter there starts from nothing rather than from a field that exists.

---

## 3. What a page can observe, without a server

This is the part Josh pointed at: a Jupyter grader sees a notebook file
after the fact; this page watches every run as it happens, from inside the
interpreter the reader is using, with the reader's own storage under it.
The ladder below runs from what costs nothing to what costs a real change.
Each rung is a possible trigger for a hint.

| Signal | Where it comes from today | Cost to expose |
|---|---|---|
| The cell ran | `executeCell()` | none |
| It raised | `run_cell()`'s boolean; `.dl-error` in the output | none |
| Ran again with the code unchanged | `cell.ranContent === cell.getCode()` at the moment of the click | none |
| The same error as last time | first line of the `.dl-error` text, or the exception's type and message | small: keep the previous one on the cell |
| Which kind of error | exception class name (`NameError`, `IndexError`, `SyntaxError`) | small: return it from `run_cell()` alongside the boolean, or parse the traceback's last line |
| A `check()` failed or passed | `cell.last_check` in Python, thrown away today; `.dl-check-fail` in the output | none via the DOM; small via Python |
| The namespace holds a value the author expected | nothing today | medium: an author-written predicate evaluated against `_page_globals` after each run |
| The output contains something | `outputEl.innerText` | none, but fragile as a trigger |
| Time between runs; time since the first run | `performance.now()` at each click | none |
| The reader opened the `?` hint, or a fold | click handlers exist | none |
| Runs across a reload | the saved record | small, if counters are persisted |

Three of these matter for a first version. **Errored**, because it is the
case Josh named. **Unchanged**, because it separates the two kinds of
stuck. And **check failed**, because on a practice page it is the only
thing that says "this ran fine and is still wrong". Everything below the
line in the table is real and worth having, and none of it should be in
the first build.

The **namespace predicate** deserves its own paragraph, because it is the
one thing on the ladder that no notebook grader offers cheaply and that
Pyodide makes nearly free. A cell header line like

```
expect: len(readings) == 4 and readings["morning"].mean() > 10
```

evaluated after each run in the page's own globals, with any exception
treated as "not yet", gives an author a way to say what "reached the
result" means without a visible `check()` in the reader's cell and
without shaping the task around the checker (the style guide §3's worry).
The predicate lives in the manifest, so it is visible to anyone who reads
the page source, exactly as an answer fold is; the site is public and
nothing changes that. Its use here is not to grade but to *stop* hinting:
once it holds, pending hints are cancelled and, if the author wrote one, a
short "you got there" note can appear. That is the shape of otter's
`grader.check()` and okpy's tests, with the round trip removed and the
result never leaving the tab.

---

## 4. The authoring surface

Three ways to write a staged hint into a tutorial's markdown were
considered. The recommendation is the second.

**(A) Grow the cell header.** `HEADER_RE` reads `id:` and `hint:` lines
off the top of an exec fence. Adding `hint-after-3-errors:` lines would
put every stage on one line, inside a code fence, with no markdown, no
maths and no code inside — the existing `hint:` already suffers from
this, and it is why the fold exists for anything longer than a sentence.
Rejected for anything past a one-liner.

**(B) A fold that names its cell and its trigger.** The `dl-hint` fold
already exists, already takes markdown, maths and illustrative code, and
is already checked by the build. Two attributes tie it to a cell and say
when it appears:

````markdown
```python exec
id: two-grids-added-together-2
hint: Two nested loops. The outer one picks a row index, the inner one a column index.
# Your add(a, b)
```

<details class="dl-hint" data-cell="two-grids-added-together-2" data-after="errors:3">
<summary>pause and ponder</summary>

Read the last line of the error before anything else. It names the kind
of thing that went wrong and the line it went wrong on. Which line is it
pointing at, and what does that line expect `a[i]` to be?

**Try this:** put `print(len(a), len(a[0]))` on its own line at the top of
the cell and run it once.

</details>

<details class="dl-hint" data-cell="two-grids-added-together-2" data-after="errors:8">
<summary>some steps</summary>

1. The outer loop needs a row index, `i`, from `0` to `len(a) - 1`.
2. The inner loop needs a column index, `j`, from `0` to `len(a[0]) - 1`.
3. The result at position `[i][j]` is `a[i][j] + b[i][j]`.

$$c_{ij} = a_{ij} + b_{ij}$$

**Think about:** why the inner loop's range comes from `a[0]` and not from `a`.

**Try this next:** the same shape, with subtraction.

</details>
````

The build validates that `data-cell` names a cell in this tutorial (or a
cell in the tutorial a practice page is paired with, see §6), that
`data-after` parses, and — since a fold without `data-cell` is the
ordinary always-visible fold — that nothing else changes for the folds
already written. The runtime hides these folds at load and shows one, still
closed, when its trigger fires. Reuses everything; adds two attributes and
a grammar for one of them.

**(C) A new fence kind**, ```` ```hint for=cell-id after=errors:3 ````.
Cleaner to grep for, and how dewstack already spells `sql-check` and
`py cell=`. But it would be a third thing that means "hint", beside the
header line and the fold, for content that is the fold's content. Not
worth the third spelling. If (B) is chosen, dewstack should use the same
attributes on the same fold, not its fence style, so an author moving
between the two repositories writes one thing.

### The trigger grammar

Small on purpose. `data-after` is one or more comma-separated terms, all
of which must hold:

| Term | Fires when |
|---|---|
| `errors:N` | the cell has raised on N runs since the counter last reset |
| `same-error:N` | the last N runs raised, and the last line of the error text was the same each time |
| `unchanged:N` | the last N runs were of the same code, byte for byte |
| `runs:N` | the cell has run N times without `expect` holding (or, with no `expect`, without a `check()` passing) |
| `check-fails:N` | a `check()` in the cell has failed on N runs |
| `minutes:M` | at least M minutes have passed since the first run of the cell this session (a floor, never a trigger on its own) |

Reset means: the cell's Reset button, Restart & run all, and `expect`
holding. Reaching the result is what clears the hints; time and reloads
are questions for §9.

`errors:3` alone covers Josh's first case. `runs:5` with an `expect:` or
a `check()` covers the second. `same-error:3` is the one this note would
argue for as the default the documentation recommends, because it is the
signal that most reliably means "does not know what to change" rather
than "is working through it".

### What a staged hint should contain

The style guide already settles most of this (§3 "A hint scaffolds; it
does not answer", §6 the two folds, §11 "name the feeling, then hand over
the route"). What the staging adds is a house order for the stages, so an
author writing three folds for one cell knows what each is for:

1. **First fold: a question and one move.** What does the error say; what
   is the line pointing at; what is the value you are not sure of. One
   thing to try that produces information rather than an answer —
   usually a `print`. This is the stage that teaches the habit, and the
   habit is the point. A short list of the habits worth teaching, so an
   author can name which one a fold is for, belongs in the writing guide,
   not in code: *read the last line first; change one thing, then run;
   print what you are unsure of; make the input smaller; say what you
   expected before you run*.
2. **Second fold: steps.** The existing `dl-hint` shape, numbered, ending
   in **Think about** and **Try this next**.
3. **Third fold, if any: the shape of the code.** Pseudocode or an
   illustrative fence with a gap. Still not the answer. The `dl-answer`
   fold, where one exists, stays the reader's own choice to open and is
   never triggered.

A cell with one staged fold is fine. The guide's "ration this" rule
applies to the number of cells that carry them at all: a page where every
cell pops a fold on the third error teaches readers to ignore folds.

---

## 5. The runtime

What `tutorial-runtime.js` would need, in the order a run happens.

**Counters on the cell object.** `cell.attempts = { runs, errors,
sameErrors, unchanged, checkFails, firstRunAt, lastErrorLine }`,
alongside `ranOrder` and `ranContent`, which already live there. Updated
in `executeCell()` after `run_cell()` returns, from three inputs: the
boolean it returns, the code as run against the previous `ranContent`,
and the output element (`.dl-error` text's last non-empty line,
`.dl-check-fail` present). No Python change is needed for a first build;
§9 asks whether to make `run_cell()` return a small summary instead of a
boolean, which is the tidier long-term shape and lets the Worker path
report the exception class without parsing text.

**`expect:`**, if adopted, is one call into Python after the run:
`tools.holds(expr)` evaluating the expression in `_page_globals` and
returning a boolean, exceptions included as False. A new function in
`tutorial_tools.py`, four lines, unit-testable under CPython like the
rest of that file.

**Trigger evaluation** after the counters update: for each hidden fold
bound to this cell, in source order, parse `data-after` once at load,
test it, and reveal the first fold whose terms all hold and which has not
been revealed already. Reveal means: remove `hidden`, leave the fold
closed, move focus nowhere, and announce once through the existing
`runAnnouncerEl` live region ("Ran — error. A hint has appeared below.")
so a screen-reader user learns a thing changed. Never a modal, never a
scroll, never an auto-open: the reader's next action is theirs.

**Where the fold sits.** In source it is written after the cell; in the
built page it can stay exactly there, in flow, hidden. The build does not
need to move it into the cell's own markup. Keeping it in flow means an
author can put a sentence between the cell and its fold, and it keeps
`render_cell()` untouched.

**Persistence.** Counters are kept in memory for the first build.
Persisting them (in the saved record as `cell.attempts`, or in a sibling
key as the notes nudge does) is a §9 question, because it changes what a
reload means and what an exported file contains.

**Reset.** The cell's Reset, Restart & run all, `expect` holding, or a
`check()` passing clear the counters and re-hide any fold not yet opened
by the reader. A fold the reader has opened stays: hiding text somebody
is reading is worse than leaving a hint they no longer need.

**Settings.** One toggle beside "run stats" and "progress badges":
*Hints that appear as I work: on / off.* Off means the folds stay hidden;
the counters still run so switching it back on does the right thing.

**The standalone export** (`Download to keep`) runs the same
`tutorial-runtime.js` through `standalone.bundle.js`, so it gets this for
free as long as nothing here depends on the Worker path.

---

## 6. Tutorials and practice pages

In a **tutorial**, the fold follows its cell, as in §4. Most tutorial
cells should not carry one; the "your turn" cells and the stubs (`# Your
add(a, b)`) are the ones that earn it.

A **practice page** is where the idea lands best and where the existing
convention is already closest. Practice pages have few cells ("a few
tools per section, not a cell per problem", PRACTICE.md §5) and many
problems with `dl-hint`/`dl-answer` folds under them. So the trigger
there is rarely "this cell errored three times" and more often "the
reader has run the section's tool cell N times without `check()`
passing for problem 9". Two ways to bind that: the fold names the
section's cell and a `check-fails:3` term, and the cell's `check()` calls
carry `label=` so the fold can name which check (`check-fails:3@q9`); or
practice pages use `runs:N` on the tool cell, which is cruder but
needs nothing new. §9 asks.

A practice page's folds may also name a cell in the tutorial it is paired
with (`practice_for:`), for the case where the problem says "using your
`add` from the tutorial"; the build can resolve that the same way
`tutorial:` links resolve. A small thing; noted so the validation is
written with it in mind.

---

## 7. dewstack: the same fold, three engines

dewstack shares no code with dewlab, only shapes (its `dewstack/assets/sql-cell.js` is
"ported in shape" from `pyodide-engine.js`). So the runtime work is done
twice, once per repository, and the authoring surface is what should be
identical. The `dl-hint` fold exists there already, with the same class
and the same build check. The attributes and the grammar carry over
unchanged. What differs is what "a run" and "an error" are:

- **SQL cell.** Run is a click; an error is a `.dl-sql-error` in the
  returned HTML; `same-error` compares the SQLite message. `unchanged`
  compares the textarea. `expect` has no Python namespace to evaluate
  against, but has something better for SQL: a query. `expect: SELECT
  COUNT(*) FROM products >= 4` is what the plushies quiz's `check_*`
  functions already do by hand in `dewstack/assets/sql_tools.py`, and a general
  `expect:` on a SQL cell would let an author write such a check without
  a new Python function per task.
- **Python cell.** As dewlab, minus the Worker: `run_python()` returns
  HTML; the error class is in the string; counters live on the DOM
  element's dataset or a Map keyed by cell.
- **`sql-check` block.** Each click is an attempt; `check-fails:N` on the
  block's own id is the natural trigger for the quiz's tasks.
- **Site editor (web track).** HTML and CSS have no run. The JavaScript
  pane's Run is the only click, and the console relay already posts
  errors with line numbers, so `errors:N` and `same-error:N` are
  available there. `expect` on a web cell could be a DOM query against
  the preview (`expect: document.querySelector("nav a")`), which is what
  a checker for "add a link inside the nav" would want. Not for the
  first build; noted because it is the one place the web track could get
  the same treatment without inventing a grader.
- **App cell** (full-stack). Same as the site editor's JavaScript pane.

Where to start on dewstack: the data track's Python and SQL cells, and
the quiz. The web track waits.

---

## 8. Where to try it first

**dewlab.**

- `tests/e2e/fixture/rendering-tour.md` gets one cell with two staged
  folds and one `expect:`; a new test file beside `test_cell_hint.py` drives
  the runs in a real Chromium (the same fixture and server
  `test_cell_hint.py` uses): a fold is hidden on load, still hidden after
  two errors, visible and closed after the third, not re-revealed by a
  fourth, hidden again after Reset, never revealed once `expect` holds.
- `tests/test_build.py`: `data-cell` naming a missing cell fails the
  build; `data-after` with an unknown term fails; a fold without
  `data-cell` is unchanged.
- `tests/test_tutorial_tools.py`: `holds()` under CPython, including the
  exception-is-False case, if `expect:` is adopted.
- A real page: `finding-where-it-went-wrong` is the obvious first
  tutorial, since its subject is reading an error back to its line, and
  a fold that says "read the last line first" there is the tutorial's own
  lesson arriving at the moment it is needed. `grid-of-numbers` is the
  second, since its stubs already carry `hint:` lines and its practice
  page already has stepped folds to graduate into staged ones.

**dewstack.**

- `the-tentacular-plushies-quiz`, whose five `sql-check` blocks are the
  only checks on the site and whose tasks are exactly the "run it until
  the check passes" shape.
- One data-track page with a Python cell, `charting-a-querys-result` or
  `asking-questions-of-a-table`, for the Python-cell path.
- dewstack's `tests/e2e/` already drives its site editor, full-stack
  cell and workspace in a real Chromium, so a staged-hint test there has
  a fixture and a server to reuse; its `dewstack/tests/test_sql_tools.py` and
  `dewstack/tests/test_python_tools.py` cover the Python side under CPython.

---

## 9. Questions for Josh

Each is a real fork. Stated assumptions are what this note would build
if unanswered.

1. **Which signal is the default the docs recommend?** (a) `errors:3`,
   any error; (b) `same-error:3`; (c) `unchanged:2`, the reader ran the
   same thing again; (d) leave it entirely to the author per fold.
   *Assumed: (b), with (a) and (c) available.*
2. **Authoring surface.** (a) the `dl-hint` fold with `data-cell` and
   `data-after` (§4 B); (b) a new fence kind (§4 C); (c) lines in the
   cell header (§4 A), one-line hints only. *Assumed: (a).*
3. **Should `expect:` exist in the first build?** (a) yes, a Python
   expression on the cell header; (b) no, `check()` and `runs:N` are
   enough to start; (c) yes, and on dewstack as a SQL expression too.
   *Assumed: (b) first, (a) second.*
4. **What clears the counters?** (a) Reset and Restart & run all only;
   (b) those plus a check passing or `expect` holding; (c) those plus a
   page reload, i.e. never persisted. *Assumed: (b), with counters
   in memory only, so (c) also holds until persistence is decided.*
5. **Persist across reloads?** (a) no, a new visit is a fresh start; (b)
   yes, in the saved record, so it travels in the export file; (c) yes,
   in a sibling key that never travels. *Assumed: (a) for now.*
6. **What a revealed fold does.** (a) appears closed, one live-region
   announcement, nothing else; (b) appears closed and the cell's bar
   shows a small marker until it is opened; (c) appears open. *Assumed:
   (a).*
7. **Can a staged fold contain a runnable cell?** (a) not yet: text,
   maths, and illustrative code; (b) yes, using the custom-cell engine,
   in a later phase; (c) yes, from the start. *Assumed: (a), (b) later.*
8. **The house order for stages** (§4). (a) question and one move, then
   steps, then code shape, answer never triggered; (b) let the author
   choose freely, guide only says "not the answer"; (c) the same three
   stages, with the third allowed to be the answer for practice pages.
   *Assumed: (a).*
9. **The habits list.** Where should the short list of habits a first
   fold can name live? (a) `docs/WRITING_TUTORIALS.md`, beside the two
   folds; (b) a new subsection of the style guide under §6, without
   renumbering; (c) both, one line in the guide pointing at the docs.
   *Assumed: (c).*
10. **Practice pages.** (a) `runs:N` on the section's tool cell, nothing
    new; (b) `check-fails:N@label`, binding to a labelled `check()`; (c)
    a fold per problem is too many; only the mixed sets get them.
    *Assumed: (a) first.*
11. **A Settings toggle?** (a) yes, default on; (b) yes, default off for
    the pilot; (c) no toggle. *Assumed: (a).*
12. **dewstack order.** (a) data track and quiz first, web track waits;
    (b) all three at once; (c) dewlab only until it has been in front of
    a class. *Assumed: (a), after dewlab's first build.*
13. **Should `run_cell()` return a summary instead of a boolean?** (a)
    yes, `{ok, error_type, error_line, checks}`, a small contract change
    with the Worker; (b) no, read the output DOM as `errored` already
    does. *Assumed: (b) first; (a) when `same-error` needs to be more
    exact than the traceback's last line.*

---

## 10. Rollout sketch

Ordered so each step is useful on its own and none needs the one after.

1. **Build side.** `data-cell`/`data-after` on the `dl-hint` fold,
   validated; `expect:` parsed off the header if adopted; both carried in
   the manifest. Tests in `test_build.py`. Docs: `WRITING_TUTORIALS.md`
   gains a "Hints that appear as a reader works" section beside the two
   folds; the style guide §6 gains a subsection on the stages.
2. **Runtime side.** Counters, trigger evaluation, reveal, reset, the
   live-region line, the Settings toggle. One e2e test file.
   `docs/tutorial-runtime-explained.md` and `ARCHITECTURE.md` §2 updated
   in the same change, per `CONTRIBUTING.md`'s rule.
3. **Two pages.** `finding-where-it-went-wrong` and `grid-of-numbers`,
   the folds written against the style guide's checks and run in a real
   browser before merge. `PLAIN_LANGUAGE_PASS.md` notes the new surface.
4. **dewstack.** Same attributes, its own counters in `dewstack/assets/sql-cell.js`, the
   quiz and one data page. Its planning note's ledger updated.
5. **Later, each its own decision:** `expect:` on SQL and web cells;
   persistence; a runnable cell inside a fold; `run_cell()` returning a
   summary.

A DECISIONS_LOG.md entry when step 1 lands, recording whichever of §9's
answers it was built under.

---

## 11. What the notebook graders do, and what a tab can do that they cannot

A survey, read in one sitting on 2026-09-06 from each project's own
source and documentation, of the systems Josh named and their nearest
neighbours. The point of it is the last two paragraphs; the rest is the
evidence.

**nbgrader** keeps everything in cell metadata (`nbgrader: {grade,
solution, locked, points, grade_id, checksum}`) and comment markers inside
the cell: `### BEGIN SOLUTION` / `### END SOLUTION` is replaced by
`# YOUR CODE HERE` when the assignment is released, and
`### BEGIN HIDDEN TESTS` marks asserts removed from the student copy.
`nbgrader validate` runs the notebook and prints a pass line or the
traceback of each failing test cell. There is no hint field, no attempt
counter, and no per-test message beyond what the `assert` raises; a
"detailed feedback" extension has been an open issue since 2016. It is a
grading pipeline with a checker bolted on, and none of its shape helps
here.

**otter-grader** compiles one master notebook into a student notebook
plus a `tests/` directory. Markers are `# BEGIN QUESTION` with YAML
underneath, `# SOLUTION` on a line whose right-hand side becomes `...`,
and a test cell that opens with a config docstring:

```python
""" # BEGIN TEST CONFIG
points: 1
hidden: false
failure_message: Check that you are returning, not printing.
""" # END TEST CONFIG
assert square(3) == 9
```

The student calls `grader.check("q1")` and sees "All tests passed!" or
a doctest-style diff with that `failure_message`. So a check *can* carry
an author's sentence — but it is one sentence per case, shown on the
first failure, every time. Every check is appended to a local log for
audit; nothing reads the log to change what the student sees. This is
the shape to avoid: a hint with no delay is a hint the reader learns to
skip.

**okpy** (Berkeley's OK client) is the one attempt-aware system in the
set, and it is worth knowing in detail. Tests are the same
`test = {"suites": [{"cases": [...]}]}` dict otter inherited, with two
additions. A *locked* case has its expected output replaced by a hash,
and `ok -u` walks the student through it one prompt at a time, answering
"-- OK! --" or "-- Not quite. Try again! --" with no cap on tries. Around
that loop: `.ok_history` counts attempts per question; a `guidance`
protocol swaps "Not quite" for a misconception-specific message when a
wrong answer matches a known one and the student has hit it enough times;
a `rate_limit` protocol imposes a growing cooldown and prints a
reflection prompt ("Woah, you're working really fast!") instead of
running the test; and a `hinting` protocol offers `ok --hint` only after
`SMALL_EFFORT = 2` failed attempts, re-offering every `WAIT_ATTEMPTS =
5`. The hints themselves come from a server. Three of those four ideas
map straight onto this note: the two thresholds are §4's `errors:3` and
`errors:8`; the misconception match is `same-error:N`; the reflection
prompt is Josh's "pause and ponder". The fourth, refusing to run the code
until a cooldown passes, is the one this note rejects: the reader's next
action is theirs, and a Run button that will not run is a verdict.

**Khan Academy.** A Perseus item is `{question, hints: Hint[]}`; each
hint has a `replace` flag ("when false, the previous hint remains
visible, so hints can build on each other"), the button reads "Get
another hint (2/5)", and the old authoring wiki's rules were that hints
are never required, the last hint is always the answer, and a stuck
student should be able to read the trail of hints and do the next
problem. On practice the button is free but taking a hint marks the item
wrong for mastery; on quizzes it appears only after a wrong answer, which
staff describe as anti-abuse rather than pedagogy. Two things to borrow:
the cumulative array (folds that stay open as the next appears), and the
rule that the trail should teach the method, which is DECISIONS_LOG.md
7.52's "a hint that ends in a related question teaches the method" said
another way. Two to refuse: a hint that costs something, and a last hint
that is the answer — here the answer stays in `dl-answer`, opened by the
reader and never triggered.

**Runestone Academy** is the near twin: a static site, Python in the
page (Skulpt, now also Pyodide), tests inside the directive. `.. actex::`
takes `:autograde: unittest`, `~~~~` separates prose from starter code,
and `=====` marks a hidden suffix run after the student's code, usually
a `TestCaseGui` class whose table reads Result / Actual / Expected /
Notes and "You passed: 75% of the tests". `self.getOutput()` lets a test
regex the printed output, which is what an in-page check is reduced to
without namespace access. There is no `:hint:` option; hints are a
separate `.. reveal::` block, always available, or an always-open
`<hint>` in the PreTeXt edition. Every run is logged to a server where
there is one, and nothing in the page adapts to it. Exercism ships
`.docs/hints.md` with a section per task behind a "Stuck?" button, on
demand; Codecademy has "Get Unstuck" and a whole-answer button. Neither
gates on attempts. The several projects called *pygrade* are unrelated
unit-test runners for GitHub classrooms and grade books; nothing there
touches notebooks or hints.

**The literature behind delaying a hint.** Koedinger and Aleven, "Exploring
the Assistance Dilemma in Experiments with Cognitive Tutors",
*Educational Psychology Review* 19(3), 2007, name the trade: help early
saves time and frustration and shallows learning; help late deepens it
and wastes time; the optimum depends on prior knowledge, which argues
for gating on attempts rather than on a clock (§4's `minutes:M` is a
floor, never a trigger, for this reason). Kapur, "Productive Failure",
*Cognition and Instruction* 26(3), 2008, and Kapur and Bielaczyc,
"Designing for Productive Failure", *Journal of the Learning Sciences*
21(1), 2012: students who first struggled without support outperformed
the supported group on later problems; the design rule is generate,
then consolidate. Renkl and Atkinson, "Structuring the Transition From
Example Study to Problem Solving", *Educational Psychologist* 38(1),
2003: fade worked examples by removing steps, last step first. That is
the opposite direction from Khan's hints, and it is an argument for
§4's third stage being "the shape of the code with a gap" rather than
the code.

| System | Where checks live | What the student sees | Attempt-aware | Hints authored where |
|---|---|---|---|---|
| nbgrader | cell metadata, `### BEGIN` markers | validate: pass line or traceback | no | nowhere |
| otter | markers → a `q1` dict in its tests directory | `check("q1")`: pass, or diff plus `failure_message` | no (logs each check) | one message per case, shown on first failure |
| okpy | `.ok` config, `tests/*.py`, hashed locked answers | terminal unlock loop | yes: history, cooldowns, hint after 2, again every 5 | a server; misconception messages in `.ok_guidance` |
| Khan | Perseus item JSON | right/wrong, cumulative hint steps | on assessment only; hints cost mastery | `hints: [...]`, last is the answer |
| Runestone | `=====` suffix in the directive | pass/fail table, "You passed: N%" | no | a separate `reveal`, always open |
| Exercism | test file per exercise | test runner output | no | `.docs/hints.md`, on demand |

**What a tab can do that these cannot.** Every system above except
Runestone runs its check somewhere other than where the student is
typing, so its feedback is a message returned across a boundary: a
validate run, a terminal, a server comparing hashes. Here the check runs
in the interpreter the cell just ran in. Three things follow that none
of them have at once. The page can look at the namespace directly — the
function exists but takes the wrong number of arguments; the loop
variable was never used — rather than only at printed text, which is
what Runestone's `getOutput()` is reduced to; that is §3's `expect:`.
The page sees every run, not only the ones where the student chose to
press Check, so it can tell "ran once, NameError" from "ran six times,
unchanged" and gate a hint the way OK's two thresholds do, with no
server and no login; that is §4's grammar. And the rendered output is
DOM, so a check can read it live. What stays on the device is the cost:
counts live in `localStorage` under the cell id, which is why the
cell-id contract in `CLAUDE.md` matters more here than it does to any
system in the table.

**What to borrow, in one line each.** Khan's cumulative array, as folds
that stay open. OK's two thresholds and its misconception match, as
`errors:N`, `runs:N`, `same-error:N`. Otter's per-case message, as the
`label=` on `check()` that §6 would bind a fold to. Runestone's in-page
suffix, as `expect:`. And from all of them, the thing to refuse: a hint
that fires on the first failure, costs the reader anything, or ends at
the answer.

---

## 12. What was decided, and what was built

Josh answered §9 the same day, in two rounds. What changed from the design
above, then what shipped (DECISIONS_LOG.md 7.135).

**The authoring surface is a fence, not two HTML attributes.** Josh: "the
way you wrote that in markdown involves a lot of HTML, is there a nicer way
of doing that?" There is: a ```` ```hint ```` fence, with `for:`, `after:`
and `title:` as optional header lines in the shape the exec cell already
uses, defaulting to the cell above, `5 errors`, and *Let's slow down a
moment…*. It also survives the Milkdown editor, which §4's option (C)
would not have. Both trigger spellings are accepted — `5 errors` and
`errors:5` — and canonicalised to the second.

**The default is five errors, not three identical ones.** `same-errors`,
`unchanged`, `runs`, `check-fails` and `minutes` are all there for an
author to reach for.

**`expect:` shipped in the first build**, on the cell header, evaluated by
Python after each run and reported back; Josh: "even having text there
would be a win for a student", and the win costs four lines.

**Nothing is cleared by success.** Josh: "I don't see why success needs to
hide hints?" A shown hint stays. The cell's Reset keeps the counters. Two
Settings rows: hints on or off (default on), and whether Restart Python
hides them (default keep).

**Counters persist in the saved-work record**, so a reload and the
downloaded series keep them and the export carries them.

**A marker on the cell's bar** as well as the live-region sentence: a dot,
gone when the fold is opened.

**The first stage asks.** Not a habits list of commands; questions — what
did you expect, what does the last line name, which line is it pointing at,
what would the smallest input be. The style guide's §3 subsection and
`docs/WRITING_TUTORIALS.md` carry this.

**Practice pages are left as they are** for now; the labelled-check binding
(§6) is a later piece. The four first tutorials are the two computational
methods pages named in §8 and two FOOP pages, `the-moves-you-already-know`
and `testing-what-a-class-does`.

**One thing found on the way.** Python-Markdown treats a `<details>` block
as raw HTML to its closing tag, so the hand-written `dl-hint` and
`dl-answer` folds on the practice pages have been shipping their numbered
steps and backticks as literal text, not lists and `<code>`. The `hint`
fence converts its body on its own (`render_staged_hint()`), so it does
not share the problem; the existing folds do. A pass that converts fold
bodies at build time is a separate, small change worth making.

**dewstack** stays as designed in its own note, not yet built: Josh, "I am
more concerned about it for python cells, but yes a makes sense."

**What §13 asked about the run report** was decided (a): `run_cell_report()`
returns a JSON report; `run_cell()` keeps its boolean for dewmini.
