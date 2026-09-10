# Next steps and open questions

Written 2026-09-04, at the end of the session that reconciled the build
step with the front page. This is the document to open at the start of
the next session. It says where everything stands, what to do next and in
what order, what each step needs, and what is still undecided. The
reasoning behind the decisions is in `CONSOLIDATION_PLAN.md`; the
assessment of every source page is in `PAGE_BY_PAGE.md`. This document
repeats neither. It points.

---

## 1. Where things stand

**2026-09-06, the documentation and code-comments plan, closed —
every phase done.** `planning/DOCS_AND_COMMENTS_PLAN.md` is new: Josh
asked that every file in both repositories read as something a teacher
or a student could follow, dewlab having already run this exact
initiative once (its own `planning/DOCS_AND_COMMENTS_PASS.md`, closed
out complete) while dewstack had never had it. `ARCHITECTURE.md` and
`CONTRIBUTING.md` now exist — the build, the runtime's three cell kinds
and the site editor, the feedback pipeline, the settings panel and
search, and the standing "keep documentation current" rule — and
`CLAUDE.md` points at both (`DECISIONS_LOG.md` stays an open question,
flagged for Josh rather than decided). Seven `docs/<name>-explained.md`
files now exist, covering this session's newest runtime code
(`sql_tools.py`, `python_tools.py`, `sql-cell.js`), the shared runtime
underneath the whole site (`build.py`, `site-editor.js`,
`workspace.js`), and every `tools/*.py` script as one shared file —
every one read closely enough to write its walkthrough, and every one
already had accurate docstrings except one real bug:
`tools/fetch_pyodide.py`'s `BASELINE` was still `sqlite3` alone, stale
now that Data Arc 2 needs `pandas`/`matplotlib` too — found while
scoping Phase A, fixed while writing Phase D's doc for that file.
Phase F's whole-repo language pass turned out lighter, as the plan
itself predicted — a grep for the consulting-report register markers
dewlab's own Phase E actually found turned up nothing anywhere in
`planning/*.md`, `README.md` or `docs/*.md`, though it did catch one
real staleness gap in `README.md`'s "Database tutorials" section,
fixed. `.claude/skills/cell-code-review/SKILL.md` is new (Phase E):
dewstack's own equivalent of dewlab's skill by the same name, adapted
to four block kinds instead of one language, then run against every
tutorial in every module — 43 tutorials, `getting-started` through
`web`'s 30. The code was already clean everywhere: semantic names
throughout, deliberate teaching choices (a discover-first name, a
join mismatch used as the lesson) correctly left alone, no renames
needed anywhere. One more real bug turned up along the way, the same
shape as the `README.md` one: `data/a-form-that-writes-a-row` linked
to `tutorial:a-form` as an existing page while also describing it as
something that still needed to exist — the web track's own form
tutorial had shipped since that sentence was written. Fixed. Nothing
in this plan remains open.

**2026-09-06, the full-stack arc's first page, closing out step 8's
second half — steps 1 to 3 of section 12's outline.** Before any of it
could be built, section 12's own outline needed a real gap closed:
"Pyodide exposes a Python function to the page" assumes a web cell's
JavaScript can reach this page's Pyodide, but the site editor's preview
(section 13) is deliberately sandboxed with no route back to anything
else on the page — exactly the channel this needs. Three ways through
it went to Josh — bridge the sandbox with `postMessage`, open a real
hole in it with `allow-same-origin`, or give this cell type no iframe
at all — and his call was the third, for a teaching reason as much as
an architectural one: every other "cell reaches another" example on
this site (`read_sql()`, `download_csv()`) is already direct, and
`postMessage` would be the one place a student meets indirection with
no story reason for it.

`build.py` gained a third cell kind, `app=name` (consecutive
`html`/`css`/`js` blocks, grouped the way `site=` blocks are, rendered
straight into the page — no separate document to sandbox in the first
place). `assets/sql_tools.py`'s new `query_rows(db_name, sql, params)`
is the Python half of the bridge; `assets/sql-cell.js` exposes it as
`window.dlQuery` only on a page that actually has an app cell.
`params` was added once the search-box step was actually being
written: pasting a visitor's typed text into SQL text directly is a
real anti-pattern worth not teaching even once, and a `?` placeholder
is the natural, real fix to name at exactly that moment — the
tutorial's own closing terms are query, result set, full stack, and
placeholder.

Step 4 (a form's `INSERT`) is deliberately not in this page — Data Arc
2's own `a-form-that-writes-a-row` already promised that wiring as "a
full-stack page still being written," so it becomes page two rather
than being pre-empted here. Step 5 (Download/Load for the whole
database) is superseded before being built, the same way Data Arc 1's
own version was: `persist` is the pattern this site actually converged
on for "where your work is saved."

Verified live against a real self-hosted Pyodide through Playwright: a
query edited from `WHERE price < 10` to `WHERE price > 10` and rerun
changed which rows drew; a search box's placeholder-bound query matched
"bag" against "Tote bag" and nothing else; resetting one app cell
cleared only its own preview, confirmed by a second, unrelated app cell
still reading the same shared table correctly afterward — this caught a
real bug (an app cell's Reset must not call `sql_tools.reset()`, since
it owns no connection of its own the way a SQL or Python cell does; an
earlier draft did, and would have silently dropped a table other cells
on the page still needed); a bad SQL query and a bad JavaScript
reference each rendered in the cell's own error box with zero page or
console errors, catching a second real bug on the way (the error box
had no `id`, so `document.getElementById()` returned null and the
handler meant to show an error crashed trying to write to it instead).
`python3 -m pytest -q`: 169 tests (10 new in `tests/test_build.py`, 6
in `tests/test_sql_tools.py`, 4 new e2e in
`tests/e2e/test_full_stack_cell.py`). `python3 build.py --clean`: 57
pages. `modules.yaml`'s `full-stack` entry is out of `planned:` now
that it has a real page; `README.md`'s "Full stack" section links it.

**2026-09-06, Data Arc 2, pages 2 to 6, closing out step 8's first half.**
The dataset question (open question 8, below) is resolved differently
than expected: rather than the population/life-expectancy placeholder,
the arc uses the World Inequality Database's "income share of the
top 1%" series (Our World in Data, CC BY) — the same dataset Josh's own
Database Methods project brief already teaches, via a sample-solution
notebook Josh shared mid-session. Building Data Arc 2 straight off that
notebook ties the tutorial directly to the real assessed project
students go on to do, rather than to an invented example.

`assets/python_tools.py` gained two functions, both now in every Python
cell's own namespace alongside `read_sql`: `load_csv(url)`, ported from
dewlab's `tutorial_tools.load_csv()` (`pyodide.http.pyfetch`, since
plain `pandas.read_csv(url)` fails inside Pyodide with a message —
`urlopen error unknown url type: https` — that explains nothing, the
same failure dewlab's own hint text was written for); and
`download_csv(dataframe, filename)`, new, using `js.Blob` and
`URL.createObjectURL` the way `sql-cell.js`'s own Download button
already does, for the one thing dewlab's tutorials never had to solve —
a query's result leaving the browser as a file.

Five pages, in the `several-tables` series after page 1:
`loading-a-real-dataset` (`load_csv` into a DataFrame, cleaning —
renaming columns, checking what is missing — then `to_sql` into a named
SQL connection); `joining-two-real-tables` (a small hand-authored
`country_regions` table, one country deliberately spelled differently
than the income dataset does, so an inner `JOIN` silently drops it and
a `LEFT JOIN` makes the gap visible — a controllable stand-in for "data
that is actually messy," rather than a second live fetch that would be
neither controllable nor reliable); `charting-a-querys-result`
(`read_sql` into a DataFrame, `groupby`, one `matplotlib` line per
country); `exporting-a-query-to-a-file` (`download_csv`); and
`a-form-that-writes-a-row` (not a real form — the `INSERT` a submission
to the web track's own `a-form` page would run, with the actual wiring
left to the full-stack arc, per Josh's own call recorded in the
page-by-page breakdown below).

This sandbox's egress proxy blocks `ourworldindata.org`, the same as it
already blocked it for the Python/pandas engine slice — so every page's
`load_csv()` cell is verified only up to the point of a real network
fetch: built a scratch page outside the tutorials tree and drove it
through a real, self-hosted Pyodide with Playwright, confirming a
blocked fetch fails as a caught, rendered `ConnectionError` rather than
a raw crash, and that every cell downstream of it fails cleanly too
(`NameError`, then a `sqlite3` "no such table" once nothing was ever
loaded) rather than doing something worse. `download_csv()` was
verified independently, since none of the five pages' own cells ever
reach it while the network call above them fails: a scratch page with a
small hand-built DataFrame, run through the same real Pyodide, produced
an actual browser download with the right filename and the right CSV
text inside it. `joining-two-real-tables`'s own `country_regions` table
(no network dependency) ran correctly end to end the same way. What
none of this confirms yet is a real, successful `load_csv()` fetch —
that needs an environment with a route to Our World in Data, which this
one does not have. `python3 -m pytest -q`: 117 passed (pandas and
matplotlib are not installed by default in this environment either;
installed alongside `requirements-build.txt` to match what CI already
does, the same gap noted on the Python/pandas engine slice below).
`python3 build.py --clean`: 55 pages.

**2026-09-05, student feedback pathway, sixth slice.** The cell-level
report icon dewlab already had (fourth slice) now exists here too, on
both the SQL cell and the Python cell built in step 7 and step 8's
Python/pandas engine: a small circle among a cell's own buttons opens the
same three doors, already carrying the cell's id, its current code, and
whatever it last showed, so a student reporting "it gives an error" from
a cell never has to copy either by hand. `build.py`'s
`cell_report_markup()` builds the icon and the panel's static shell for
both cell types; `assets/sql-cell.js`'s `updateCellReportLinks()` fills
in the live code and output at the moment the panel opens, ported in
shape from dewlab's `tutorial-runtime.js` equivalent. `.github/
ISSUE_TEMPLATE/report.yml` gained the matching `cell`, `code`, `output`
and `browser` fields, so `report_patterns.py`'s per-cell threshold — until
now dormant here, since no report ever carried a `Cell` field — can
actually fire.

Needed a real browser test harness this repository did not have yet:
`tests/e2e/conftest.py`, ported from dewlab's own, builds a small fixture
tutorial (`tests/e2e/fixture/rendering-tour.md`, one SQL cell and one
Python cell) with `build.py` and serves it against a self-hosted Pyodide
(`tools/fetch_pyodide.py --packages sqlite3 pandas matplotlib --out
tests/e2e/pyodide`), so `tests/e2e/test_cell_report.py`'s eight tests
open the panel, edit a cell live, run it, and check the report links
carry the edited code and the real output — not what a click no browser
ever making would only assume. `tests/test_build.py` gained a
`TestCellReportPanel` class covering the icon and panel markup itself,
switched on and off by `planning/feedback.yaml`.

**2026-09-05, student feedback pathway, fifth slice.** Two more
workflows, both calling small stdlib-only scripts in `tools/`:
`label-report` fires the moment a report issue opens and applies a
`page: <slug>`/`kind: <error|unclear|question>` label, creating either
the first time it is needed, so nobody has to make these labels by hand
in GitHub's settings. `report-patterns` runs weekly and opens or updates
one `pattern` issue per page with three or more open reports in the last
fortnight — the per-cell half of the same threshold had nothing to match
yet at the time, since this repository's report form carried no `Cell`
field; the sixth slice above is what gave it one. Both scripts are tested
in `tests/test_report_patterns.py`, paired with the identical pair in
`deweydex/dewlab`.

**2026-09-05, student feedback pathway, fourth slice.**
`.claude/skills/triage-report/SKILL.md`, so working the report inbox has
a written order rather than being reinvented each session: read before
acting, re-sort the student's guessed `kind`, dedupe, and the two hard
stops — a database or web-standards question is Josh's call, and
nothing closes without a person having looked. Paired with the same
skill in `deweydex/dewlab`, adapted for this repository's own content and
conventions (a slug is a contract, not a cell id; `sources/` is never
emptied by deletion).

Also `.github/workflows/auto-disable-feedback.yml`, a direct request:
the report doors stay on, but turn themselves off on Tuesday,
2026-09-08, without anyone needing to remember to. A genuine one-shot —
cron's day-of-month/month fields carry the date, not a recurring weekday
— and its last step deletes its own workflow file in the same commit
that flips `planning/feedback.yaml`, so nothing is left behind to
misfire on the same date next year. A manual run of the same workflow
(`workflow_dispatch`) turns the doors off early, on purpose, rather than
rehearsing it safely.

**2026-09-05, student feedback pathway, third slice.**
`getting-started/issues-and-pull-requests`, a new page between
`a-github-account` and `an-editor`: what this repository's own file
listing holds, an issue as the report the three doors already file (real
open issues linked, not invented ones), and a real merged pull request
(#35) as what a proposed change actually looks like. The debugging half
of this plan turned out differently on dewlab's side: the tutorial was
going to teach reading a traceback, but `when-it-goes-wrong.md` in
`mit-pdp-maths-prog-integration` already does, fully, so dewlab folded a
short "what to try first" section into `first-steps.md` instead of
writing a page that would have duplicated it. Both new/changed tutorials
are dewlab#153 (the cell-level report icon) and dewlab#154 (the
first-steps.md section) — see that repository's own `DECISIONS_LOG.md`
Phase 8 for the fuller account. This closes out the plan's two new
tutorials, in a different shape than first scoped.

**2026-09-05, student feedback pathway, second slice.** The footer's
report line, "Something wrong on this page? Tell us.", now opens three
doors rather than one link: "I have a question" (to Discussions, once it
is switched on), "It gives an error" and "The page is wrong, or I could
not follow it" (both to a prefilled GitHub issue, `kind` already picked
on the form). `report_doors_html()` in `build.py` renders it as a plain
`<details>` — no JavaScript, no runtime change. A question filed as a bug
report was the wrong container for it and for whoever answers it later;
this is the fix, worked out from an artifact Josh and Claude built
together.

**2026-09-05, first slice.** A report link at the foot of every page,
opening a prefilled GitHub issue on the tutorials' own template,
`.github/ISSUE_TEMPLATE/report.yml`. `planning/feedback.yaml` is a kill
switch: `enabled: false` turns the doors off everywhere without touching
a tutorial. `getting-started/a-github-account` gained two sections, on
the username being public beyond your own pages and on GitHub Education.
Not built yet, and part of the same plan: the cell-level report button
with code capture, and two new tutorials on debugging and on reading a
repository's issues and pull requests. Manual GitHub-side steps still
needed, none of them costing anything: switch Discussions on, create the
`kind:`/`source:`/`pattern` labels, and make a Project across this
repository and dewlab's.

**Merged into `main`, all on 2026-09-04.** dewadaba#2 (the front page,
the interim copies, the reading settings, the plan and the page-by-page
assessment), dewadaba#3 (the build step, dewlab's shell and settings
panel, the hello page, the two workflows), dewadaba#4 (the morning's
decisions and plan sections 13 to 15) and dewadaba#5 (the reconciliation
of #3 with the rest: the build as the platform, the README as the front
page, the copies moved to `sources/`, dewstack throughout).

**Live.** The publish workflow's first run succeeded on the merge of #5,
so GitHub Pages is on, published by Actions from `site/`. Until the
repository is renamed the address is `deweydex.github.io/dewadaba/`. The
front page is written for the student, from `tutorials/front.md`: an
opening, two doors, the search box, and the list of pages by module, with
the modules not yet written shown as a heading and one line (decided
2026-09-04, evening; see question 11 below). The README is the longer map
for people who read the repository, and the two are no longer one text.

**The repository is still called dewadaba.** Every page, link and
document says dewstack, including the README's own link to the site and
the Colab link to the notebook, so those two links are dead until the
rename. GitHub redirects the old name once it is done, for the repository
and for Pages.

**Open elsewhere.** [deweydex/web#1](https://github.com/deweydex/web/pull/1),
the plain-language and accessibility pass on the starter, is a draft
awaiting Josh's read. [deweydex/everlearning#6](https://github.com/deweydex/everlearning/pull/6),
the fifteen-repository analysis that started all this, is a draft with
green CI. Nothing else is open. dewlab#116 (the descriptors gathered) is
merged.

**Arrived and assessed.** The further database content, plus a Level 6
module descriptor for later. See step 0, item 5.

**What the repository holds now.**

| Path | What it is |
|---|---|
| `README.md` | The course map. GitHub shows it; the build renders it as the top of `site/index.html`. One text, two places. |
| `build.py`, `tests/`, `pytest.ini`, `requirements-build.txt` | The build and its checks. Fourteen tests. |
| `assets/` | dewlab's shell (`shell.html`), stylesheet (`site.css`), settings panel (`settings.js`), search (`search.js`), the two accessible typefaces and their CSS, a favicon. |
| `tutorials/` | The build's input. Today: `modules.yaml`, `getting-started/` (the `welcome` series: A0 to A6, how the pieces fit through the inspector), `reference/` (the `shelf` series: troubleshooting, quick reference, project ideas), and `web/` (the `first-site` series: Flexbox first steps, the site editor's first page). |
| `sources/wadb/`, `sources/playground/` | Verbatim copies of `WADB_Tutorials` and `HTML-CSS-SQL-JS`, with the course bar added. Coverage material for the rewrites. Not published. |
| `sources/teaching-materials/` | The web authoring and database subset of everlearning's `Teaching materials/` folder: the Database Methods notebook sequence and live project brief, the Web Authoring briefs and templates, Break and Make a Website, exam material, and the Level 6 module descriptor. Coverage material, not published. Assessed in `PAGE_BY_PAGE.md` section 6. |
| `databases/sqlite_tutorial.ipynb` | The dinosaur notebook, opened from the README in Colab. |
| `tools/add_course_bar.py` | Puts the course bar on the copies. Its links are moot now that the copies are unpublished. Keep or delete; see the questions. |
| `tools/measure_sentences.py` | Counts sentences in a markdown file and shows the longest few per file, as candidates for the trim test (plan section 3, check 2). Not a pass/fail gate. |
| `planning/` | The plan, the page-by-page assessment, this, and `LEVEL6_COVERAGE.md` (a coverage map against the Level 6 module descriptor, nothing scheduled from it yet). |
| `.github/workflows/` | `tests.yml` on every pull request; `deploy.yml` on every push to `main`. |

---

## 2. The design, in one paragraph

Section 15 of the plan, decided 2026-09-04. The course is three tracks,
and each track is an artefact the student builds in arcs, with a tutorial
page behind each step of the artefact. The web track: Arc 1 is the `web`
starter and sixteen concept pages beside it, ending in a published
portfolio; Arc 2 is a second forkable starter shaped like the assessed
project and eight pages beside it; Arc 3 is a site that shows the
student's data. The data track: Arc 1 is the student's own first table,
four pages, cells as queries; Arc 2 is a designed database with a real
dataset, four pages. Before both tracks, six getting-started pages.
Beside everything, three reference pages. Forty-four pages of thirty to
fifty sentences each. The decisions that shape a page are in section 8
of the plan (sixteen of them) and section 11 (the style bar).

---

## 3. The order of work

Each numbered step is a session or two. Within a step, every page is a
pull request of its own, per the plan's ground rules. The order is the
plan's section 15 order with the housekeeping in front and the build
work put where the pages need it.

### Step 0. Housekeeping, Josh's actions

1. Rename the repository dewadaba to dewstack. Then open
   `https://deweydex.github.io/dewstack/` and the Colab link on the README
   and confirm both resolve.
2. Read and merge web#1. Then, on top of it, add the "Where this fits"
   section to the starter's README. The text is in the closed web#2 and is
   reproduced in section 6 below, with its links corrected: the closed
   draft pointed at `dewstack/tutorials/`, which no longer exists.
3. Read everlearning#6 and merge or close it. It is history now; the
   plan here superseded it the same day.
4. Point the class pages at `deweydex.github.io/dewstack/` and
   `github.com/deweydex/web`.
5. Done 2026-09-04. The further database content arrived as a
   `Teaching materials/` folder pushed to `everlearning`'s `main`; the
   web authoring and database subset is copied to
   `sources/teaching-materials/` and assessed in `PAGE_BY_PAGE.md`
   section 6. It also carried the Level 6 `Web Development 6N1277`
   module descriptor, assessed on its own in `planning/LEVEL6_COVERAGE.md`
   (nothing scheduled from it yet).

### Step 1. Assess the new database content, revise the data track

Done 2026-09-04. `PAGE_BY_PAGE.md` section 6 assesses it. It fills the
four-plus-four shape rather than changing it: the real, currently-taught
notebook sequence (pandas, matplotlib, ipywidgets, files, SQL) and the
live 50% project brief confirm Data Arc 2 almost exactly as section 15
already had it, and the exam material confirms the multi-table,
keys-and-relationships half. Two calls were needed and are made: Data
Arc 1 stays SQL-only (pandas is not pulled forward from Arc 2), and the
ipywidgets-style interactive element stays a full-stack-arc idea rather
than moving into Arc 2. Steps 6 and 7 are no longer provisional.

### Step 2. The three reference pages

Done 2026-09-04. A new module, `reference`, with one series, `shelf`.

| Page | Slug | From | Notes |
|---|---|---|---|
| Troubleshooting | `troubleshooting` | `sources/wadb/troubleshooting.html` | Written as problem-shaped cards, with the Settings panel and the search added as dewstack-specific problems. |
| Quick reference | `quick-reference` | `sources/wadb/reference.html`; `uu_reference.md` from the teaching materials | Two halves, HTML/CSS then SQL, as two-column tables rather than fixed-width cards, so nothing overflows a phone. |
| Project ideas | `project-ideas` | `sources/wadb/project-ideas.html`, `design-resources.html`, `examples/` | Re-keyed to the starter, Flexbox/Grid, a database of your own, and the full-stack page. `hello-world.html`, `first-page.html` and `resume-template.html` are bundled as downloads; the larger templates wait for the page that teaches each pattern. |

Confirmed at 1200 and 390 pixels with a headless Chromium screenshot
through Playwright: no sideways scroll on either width, one `main`
landmark, one `h1`, a labelled `nav` on each page. `python -m pytest -q`
and `tools/measure_sentences.py` both pass on all three. The README's
Troubleshooting and Quick reference links now point here instead of the
old external copies, and a Project ideas link was added.

Done when each page passes both bars in plan section 11 and renders at
1200 and 390 pixels without sideways scroll.

### Step 3. Getting started, A0 to A6

Done 2026-09-04. Question 3 below is resolved: hello folded into A0 and
the `hello` slug is retired (it had been in front of no class), so the
`welcome` series is now these seven pages in order, replacing the single
hello page.

| Page | Slug | From |
|---|---|---|
| A0 How the pieces fit | `how-the-pieces-fit` | New, plus hello's explanation of the shell. The README's "Before you begin" is the seed; no illustration yet, described in words instead. |
| A1 A GitHub account | `a-github-account` | `sources/wadb/github-guides/01-getting-started.html` |
| A2 An editor | `an-editor` | New. VS Code, with GitHub's own web editor as the no-install fallback. |
| A3 Your copy of the starter | `your-copy-of-the-starter` | Guide 06's fork section, plus guide 02. Fork, then clone, download, or edit in the browser. |
| A4 Publish it | `publish-it` | Guide 05. GitHub Pages, and why the address looks like that. |
| A5 The two loops | `the-two-loops` | Lesson 01's first third, guide 03. Save and refresh; commit, push, and wait. |
| A6 Seeing under the page | `the-inspector` | Guide 07's first third. |

The data track note (only A0 and A6 needed) is in A6's opening; A0
applies to both tracks equally, so it needed no such note.

Confirmed at 1200 and 390 pixels with a headless Chromium screenshot:
no sideways scroll, one `main` landmark, one `h1`, a labelled `nav` on
each page. `python -m pytest -q`, `python build.py --clean` (every
`tutorial:` cross-link between these seven pages resolves) and
`tools/measure_sentences.py` all pass.

### Step 4. The site editor component

Done 2026-09-04. Question 4 decided: plain `textarea`s, per the
recommendation, since the pages are read on phones and CodeMirror is
heavy there. Nothing rules out CodeMirror later; the markdown contract
(`site=name` fenced blocks) does not change either way.

A fenced block tagged `` ```html site=name `` (or `css`, or `js`)
becomes a pane; consecutive blocks sharing a name form one editor.
`build.py`'s `extract_site_editors()` and `render_site_editor()` do the
work, ported in shape (not code) from dewmini's Site tab
(`dewlab/compose/dewmini.js`, `openSiteFile()`/`renderSiteView()`;
DECISIONS_LOG 7.121): a pane per file, a preview built from
`<style>{css}</style>{html}<script>{js}</script>`, redrawn on every
keystroke, in an iframe sandboxed to `allow-scripts` with no
`allow-same-origin`. `assets/site-editor.js` is the runtime; new rules in
`assets/site.css` under `.dl-site-editor` style it, stacked vertically
rather than side by side, since the reading column can be as narrow as
26rem.

Two things dewmini's version does not need here and does not have:
**reset** restores the block's original text, and **download these
files** saves each pane as `<site-name>.<ext>`, so a reader can drop the
result into their own fork. Nothing is saved on the page itself, since
the student's fork is where real work lives (plan, section 13).

The preview width control is a percentage, not a fixed pixel range: the
reading column itself is reader-adjustable (26rem to 60rem in Settings),
so a fixed width could overflow a narrow one where a percentage cannot.

Tests added to `tests/test_build.py`: a page with one site block builds
and its editor has `sandbox="allow-scripts"`; a block with a language
other than html/css/js stops the build; site blocks sharing a name that
are not consecutive stop the build; a page with no site block gets no
`site-editor.js` script tag. `python -m pytest -q` (18 tests) and
`tools/measure_sentences.py` both pass.

**Done when**, satisfied: `flexbox-first-steps`, a new module `web` with
series `first-site`, ships with the component. Checked in a real browser
(Playwright): all three cards share one row at 100% preview width, and
wrap across three rows at 30%, with no page-level sideways scroll at
1200 or 390 pixels either way.

Done when D1, Flexbox first steps, ships with it and a reader can drag
the preview narrower and watch a row wrap.

**Console and Run, added 2026-09-06** (`planning/CONSOLE_AND_WORKSPACE.md`,
step 1 of its section 8). A JavaScript pane now carries a Run button in
its header and runs only on Run or Ctrl/Cmd+Enter; HTML and CSS stay
live, and the preview keeps the last-run script while they change. A
console under the preview shows `console.log` output and every uncaught
error with the pane and line it came from, a Go to line button that
puts the caret there, and a plain-language second line for the four
errors a first term meets most (`FRIENDLY` in `assets/site-editor.js`,
data rather than code). The console is open from the start on an editor
with a JavaScript pane and hidden on an HTML/CSS-only one until
something arrives. `</script` typed into the pane no longer ends the
script element early. Fourteen Playwright tests in
`tests/e2e/test_site_console.py`, with their own fixture and no Pyodide,
cover the line arithmetic for a runtime error, a syntax error and an
error inside a click handler, the Run model, Reset, Go to line, and the
hidden console opening for an inline script. The markdown contract is
unchanged; no tutorial had a `js site=` block on the day this shipped,
so nothing a student sees today has moved.

### Step 5. Web Arc 1, sixteen concept pages

In the starter's order, each page the explanation behind the exercise a
student has just done. Plan section 14's table maps every page to its
exercise and its source; the B and C rows are Arc 1. `web/CONCEPTS.md`
is the register to match and is quarried first. A new module, `web`,
with one series per arc. Each page: open with the question, something to
try in the site editor, the explanation, one "your turn" done in the
student's fork, a look back, at most three new terms listed at the end.

In progress. B1 to B7 done 2026-09-04: `a-page-is-files` (ex 3), `the-skeleton`
(ex 3, 4), `headings-and-emphasis` (ex 4 to 6), `sections-that-mean-something`
(ex 7, 8), `images-and-alt-text` (ex 9), `three-kinds-of-link` (ex 10, 11),
`navigation` (ex 12). `first-site.order.yaml` lists all seven before
`flexbox-first-steps`, which moves to the close of the series: D1 belongs
after the B and C rows, not chronologically where its own exercise sits, per
plan section 14. Checked the same way as steps 2 to 4: `tools/measure_sentences.py`,
`python build.py --clean`, `python -m pytest -q` (19 tests), and Playwright
screenshots at 1200 and 390 pixels confirming the site editor renders and
the demonstrations land (title/heading duplication, identical-looking
div/section boxes, heading levels stepping down, a broken image falling
back to its `alt` text, an anchor link jumping inside the preview). B8
(optional depth, the DOM) is left for later, per the plan's own allowance
for optional-depth pages.

C1 to C12 done 2026-09-04, all of Arc 1's C rows bar the optional-depth C6:
`a-rule-and-where-it-lives` (ex 13), `variables-and-colour` (ex 13, 14),
`the-box` (ex 15, 16), `text-and-units` (ex 17), `selectors-and-classes`
(ex 18), `the-container` (ex 19), `position-and-the-sticky-header` (ex 20,
21, two separate site editors on one page for the two distinct
techniques), `hover-and-focus` (ex 22, 23), `transitions-and-transforms`
(ex 22, `transform`'s functions kept separate from `hover-and-focus`'s
triggers), `media-queries` (ex 24, demonstrated live by dragging the
preview width slider across the breakpoint), `flexible-images` (ex 24,
`img { max-width: 100%; height: auto; }` from WADB lesson 9, demonstrated
with a data-URI test image so the page needs no network). C6 (specificity,
optional depth) and B8 (the DOM, optional depth) are the only rows left
before D1. Same checks throughout: `tools/measure_sentences.py` over the
whole repository, `python build.py --clean` (30 pages), `python -m
pytest -q` (19 tests), Playwright at 1200 and 390 pixels, plus live checks
of each demo's actual computed styles: the rem/px padding split, the
descendant selector's colour, the container's width change, the sticky
header's position after a scroll, the footer's bottom edge against the
preview's own height, the button's hover transform and focus outline, the
three transform functions' matrices, the message's background colour
either side of the media query's breakpoint, and the two images' widths
at a narrow preview (one overflowing at its full 500px, the other capped
to the container).

Writing `navigation`'s anchor-link demonstration found a real bug in the
site editor: a `srcdoc` iframe with no `<base>` tag resolves a relative
address, a same-page `href="#id"` included, against the tutorial page's
own address rather than its own, so clicking such a link loaded a copy of
the real page into the preview instead of jumping within it. Fixed in
`assets/site-editor.js` by setting `<base href="about:srcdoc">` on the
generated document; a test in `tests/test_build.py` guards the fix.
Confirmed with a headless click through Playwright: the preview now
scrolls to the matching `id` and the outer page's own address never
changes. `flexbox-first-steps` re-checked after the fix: its cards still
share one row at 100% and wrap to three at 30%.

### Step 6. The second starter and web Arc 2

Before the project brief is issued (January, per the plan; confirm the
date). A new repository, working name `site` (question 2): a five-page
skeleton with the brief's file list, a `planning.md` and a `readme.md`
template inside, forked the same way as `web`. Then the eight Arc 2
pages (D rows in section 14, reshaped as section 15 says), quarrying
lessons 11 to 13's examples for the editors' seeds. The front page's
"Begin" part gains the second starter as the door to Arc 2.

In progress, 2026-09-05. Question 2 resolved, by Josh: `web` renamed to
`portfolio_wad`, and the second starter is `project_wad` rather than
working-name `site`. `_wad` names both for Web Authoring and Development,
the two modules likely to use these starters, though only Web Authoring
carries an assessment against them today. Both names are meant to be
readable on a student's own GitHub profile and to say clearly which is
which; `portfolio_wad` and `project_wad` name the artefact each ends in
(a personal portfolio; the assessed multi-page project) rather than
repeating "web" and "site," near-synonyms that would not distinguish the
two on sight. `web`'s rename left every file and its history intact;
GitHub redirects the old address. Every reference to `deweydex/web`
across dewstack is updated to `deweydex/portfolio_wad`; the historical
ledger entries in section 7 and `PAGE_BY_PAGE.md` keep the old name,
since they describe what was true at the time, the same way `dewadaba`
stays in earlier entries after that rename.

Both repositories are GitHub template repositories, at Josh's choice,
confirmed as the right call: a template repo still shows the ordinary
**Fork** button, so nothing already written about forking breaks, and
**Use this template** additionally gives a copy with no visible link back
and no shared history, which suits a portfolio a student may want to
carry past the course under a plainer name. `your-copy-of-the-starter.md`
now teaches both ways of copying `portfolio_wad` and says a student is
free to rename their own copy now or later.

`project_wad` was Josh's own `portfoliotest` repository, renamed rather
than created empty; its original README (a photograph and a résumé link)
was in git history, not deleted, and is now replaced by the five-page
skeleton (`index.html`, `about.html`, `gallery.html`, `contact.html`,
`resources.html`, `styles.css`, and `planning.md`/`readme.md`/
`maintenance.md`, written fresh rather than reusing the ML-specific
templates in `sources/teaching-materials/`), verified with Playwright and
axe: 0 violations, no overflow at 1200 or 390 pixels, every page linking
to every other, Flexbox and Grid both confirmed live.

All eight Arc 2 pages done 2026-09-05, in a new series `several-pages`:
`planning-a-site` (audience, site map, wireframe, sent to `project_wad`'s
`planning.md`), `pages-and-navigation` (`aria-current`, consistent
navigation, demonstrated live by moving the marker between two links and
watching the bold weight follow it), `cards-in-a-row` (the three numbers
behind `flex`: grow, shrink, basis), `a-grid-gallery`
(`repeat(auto-fit, minmax())`, demonstrated by narrowing the preview and
watching the tiles reflow from two rows to four with no media query),
`navigation-on-a-phone` (`flex-direction: column` inside a media query,
demonstrated the same way), `a-form` (`<label for>`, demonstrated by
clicking a label's text and watching focus land on its input),
`images-and-file-size` (an `images/` folder, JPEG/PNG/SVG, resizing
before adding a photo — no site editor, since file size is not a
live-preview concept), `documenting-what-you-built` (`readme.md` and
`maintenance.md`, closing the arc that `planning-a-site` opened). Each
page's "your turn" sends the student to the matching real code already
sitting in `project_wad`, not to new code written for the tutorial.
Step 6 is done; step 7 (Pyodide, the SQL cell, data Arc 1) is done bar
its practice pages (item 4).

### Step 7. Pyodide, the SQL cell, and data Arc 1

1. Copy dewlab's `pyodide-engine.js`, its worker and `tutorial_tools.py`
   (`run_query()`, `load_csv()`), and dewmini's SQL cell. Record the
   dewlab commit in the ledger. Decide where the Pyodide payload is served
   from (question 5).
2. In `build.py`, a fenced block tagged as a SQL cell becomes an editable
   cell with a result table. Tests as for the site editor.
3. Four pages in a new module, `data`: a table is a list of rows; asking
   questions of a table; changing what is in it; a second table and a
   join. The dinosaur notebook's sequence, the playground's six command
   cards and five exercises as seeds. The student's own table as the
   "your turn", kept as a file they download and load.
4. The playground's SQL section and the quiz's five tasks rebuilt as the
   practice pages beside these, solutions at the foot (decision 2), the
   quiz's after submission.

**The runtime is done, 2026-09-05; the four pages are next.** Item 1
above is not what actually happened, and the difference is worth
recording rather than papering over.

`pyodide-engine.js` and `pyodide-worker.js` (dewlab commit `811cc4d`)
turned out to be dewmini's own infrastructure more than Pyodide's: a
Worker thread with a genuine Stop button, Jedi-backed hover docs and
autocomplete, a whole mounted-filesystem layer (native folder, OPFS,
IDBFS) — none of it something a single, independent SQL cell on a
reading page needs, and copying it wholesale would have meant carrying
dead code paths dewstack's UI never exposes a way to reach. `run_query()`
and `_run_sql_cell()` in `tutorial_tools.py` turned out to depend on
dewmini's own cell-identity system (`_require_cell()`, needing an active
`_CellContext` a full notebook sets up) and on pandas, for
`_table_html()`'s `DataFrame.to_html()` — pandas that Data Arc 1 was
already decided (step 1) not to need.

So this ported in shape, the same choice already made for the site
editor rather than dewmini's Site tab: `assets/sql-cell.js` is a new,
much smaller file, quarrying dewlab's main-thread boot sequence (no
Worker at all — a SQL query on a student-sized table finishes fast
enough that this is a real simplification, not a corner cut) —
`loadPyodide()`, `pyodide.loadPackage()`, writing the tools module into
Pyodide's FS and `pyimport`-ing it, the same shape line for line.
`assets/sql_tools.py` is a new, much smaller module, not a port of
`tutorial_tools.py` at all: one function, `run_sql(db_name, script)`,
building an HTML table directly from a `sqlite3` cursor's columns and
rows, no pandas, no cell context, catching `sqlite3.Error` itself and
rendering it as a message rather than a traceback (nothing here runs a
reader's own Python, so a traceback pointing at this file's own code
would only confuse). One connection per `data-db` name, kept at module
level, so cells sharing a name see the same tables and cells with
different names never do; a Reset button drops the named connection so a
`CREATE TABLE` run twice does not just fail.

`build.py`: a fenced `` ```sql cell=name `` block becomes a `.dl-sql-cell`
— a labelled textarea, Run and Reset, a status line, and an output area.
Unlike a site editor's `site=` blocks, a name is allowed to recur
anywhere on the page, not just back to back: a table one cell creates is
exactly what a later cell, after some prose, is meant to keep querying.

**Question 5, decided:** a CDN by default (`cdn.jsdelivr.net`, the same
one dewlab defaults to), overridable per page via
`window.DEWSTACK_PYODIDE_BASE` before `sql-cell.js` runs. `tools/
fetch_pyodide.py`, adapted from dewlab's `dev/fetch_pyodide.py`, is the
self-hosting escape hatch, trimmed to dewstack's real need: `--packages
sqlite3` alone (dewlab's own default pulls in numpy/pandas/matplotlib/
jedi for dewmini's wider needs) brings the download to about 13 MB
against dewlab's roughly 32 MB. `assets/vendor/pyodide/` is gitignored,
the same as dewlab's equivalent, and not populated by default.

**Verified live**, not just built: this sandbox's own egress proxy
blocks `cdn.jsdelivr.net` outright, so verification used
`tools/fetch_pyodide.py`'s own logic to fetch a real, trimmed,
sqlite3-only Pyodide and serve it locally, with
`window.DEWSTACK_PYODIDE_BASE` pointed at it. A real `CREATE TABLE` /
`INSERT` / `SELECT` script ran through actual Pyodide and rendered a
real table with the actual inserted rows; a second run without Reset
failed with "table … already exists", rendered as a message rather than
a crash, with zero page or console errors; Reset restored the textarea
and dropped the table; a run after Reset worked cleanly again. `python -m
pytest -q`: 33 tests, 9 of them a new `tests/test_sql_tools.py` exercising
`run_sql()` directly under plain CPython, since it imports nothing
browser-only. Playwright and axe at 1200 and 390 pixels: 0 violations (a
first pass had one — the textarea had no `<label>` — fixed before this
was recorded), no sideways scroll.

**Done when**, satisfied: a real SQL script runs through real Pyodide
and renders a real table, Reset genuinely clears the named database, and
a page with no SQL cell carries none of this weight (no script tag, no
Pyodide download).

**Download and Load, added after the runtime above:** item 3's "kept as
a file they download and load" needed a mechanism, so every `.dl-sql-cell`
now also carries Download and Load buttons, the same idea as the site
editor's "Download these files" — Download saves the cell's current text
as `<db-name>.sql`; Load reads a chosen file straight into the textarea,
still waiting on Run before anything executes. Building this surfaced a
real bug, not a test artifact: `import()`'s relative specifier resolves
against `sql-cell.js`'s own URL, but Pyodide re-resolves `indexURL`
itself once running, against the page — so a relative
`DEWSTACK_PYODIDE_BASE` reached two different base URLs depending which
half of the boot sequence used it. Fixed by resolving it to an absolute
URL in `pyodideBase()` before either use, against `sql-cell.js`'s own
location, the same way `sql_tools.py`'s URL already was. Verified live
again after the fix: Run, Download (the downloaded file's text matched
the textarea), and Load (a loaded file's text ran correctly after Run)
all worked with zero console errors.

**Item 3, the four pages, done 2026-09-05:** module `data`, series
`first-database` — *a table is a list of rows*, *asking questions of a
table*, *changing what is in it*, *a second table and a join*. The
dinosaur notebook's own six-dinosaur seed runs as the demo table on
every page, rebuilt fresh each time since a page's Pyodide, and the
tables it holds, do not survive a reload; the running dinosaur example
is what "recurs non-consecutively" (question 2's own feature) is for.
The fourth page's join is new rather than ported from the notebook: the
notebook itself never joins its two tables, only `UNION`s them, so a
`sightings` table with a `dinosaur_id` foreign key was written instead,
to teach the join the title actually names. Each page's "your turn"
builds the reader's own table, carried from page to page automatically
(superseded below — this originally meant Download at the end of one
page and Load at the start of the next). `modules.yaml`'s `data` entry
moved out of `planned`; `front.md`'s "Start with data" door and the
README's own data section now point here instead of the old external
playground.

Verified live the same way as the runtime: every real demo cell across
all four pages, run in order in a real browser against a real, trimmed,
locally-served Pyodide, rendered the expected rows with zero console
errors; axe-core found 0 violations and no sideways scroll on all four
pages and the front page, at 1200 and 390 pixels. `python -m pytest -q`:
35 tests. `tools/measure_sentences.py` over the four pages and the
touched parts of `README.md`: every sentence at or under 25 words.

Item 4, the playground's SQL section and the quiz rebuilt as practice
pages, is done — see the note after the persistence entry below.

**Persistence, superseding the Download/Load framing above, 2026-09-05:**
raised in conversation — a reader who forgets to click Load, or picks
the wrong file, loses the thread of "your table" across the arc, and the
same problem would only get worse in a scored quiz. Since every
dewstack page shares one browser origin, `localStorage` already carries
state from page to page with no file dialog needed, so a `persist` flag
on a `` ```sql cell=name `` block now does that automatically:
`assets/sql-cell.js` saves the cell's script to `localStorage` on every
Run (and on Load), and restores and reruns it on its own the next time a
`persist` cell with that name loads — the reader does nothing extra, and
a page with no persisted table falls through to a plain placeholder
comment (`sql_tools.py`'s comment-stripping already renders that as
"Nothing to run" rather than a confusing error). `build.py` renders a
persisted cell's label as "Your table" instead of "SQL", plus a short
note under the box, so the behaviour is named rather than left to a
script the reader cannot see. Reset now clears the saved copy too, not
just the in-page connection. Download and Load are unchanged underneath
this and still work — taking a copy out of the browser, or bringing one
in from elsewhere — just no longer the thing continuity depends on.

All four Data Arc 1 "your turn" cells now carry `persist`, with their
prose rewritten to match ("your table is already here" rather than
"click Load"). Verified live: built a table on page 1 in a real browser
against a real Pyodide, navigated to page 2, and watched it restore and
rerun with no click and the same rows, zero console errors; Reset
confirmed to clear `localStorage`, not just the textarea; Download and a
subsequent Load both confirmed to still work, with Load's file becoming
the new saved copy. `python -m pytest -q`: 37 tests. axe-core: 0
violations, no sideways scroll, on all four pages at 1200 and 390
pixels.

**Item 4, done 2026-09-05:** module `data`, new series `practice` —
`sql-practice` and `the-tentacular-plushies-quiz`. A real conflict
surfaced first: this item's own wording calls the quiz "scored", but
`README.md` already promises "the tutorials and exercises here are not
graded." Rereading the original `WADB_Tutorials` quiz settled it: its
own "Check My Work" button was always an instant, private self-check —
closer to dewlab's `check()` (instant feedback, records nothing) than
to a grade — so that is what got built, worded carefully as a check,
never a score.

`sql-practice`: the playground's five exercises, against the same
students/courses seed data the playground itself used (deliberately not
the dinosaurs Arc 1 already used, so the exercises test transfer rather
than memory of one example). A hint per exercise (`<details
class="dl-hint">`), full solutions collected in one `## Solutions`
section at the foot, per this item's own wording — not interleaved
per-exercise the way dewlab's own `-practice.md` convention does it.

`the-tentacular-plushies-quiz`: five tasks building a small shop
database, one persisted `cell=quiz` box for the reader's own SQL, and a
new `` ```sql-check db=... task=... `` block type (`build.py`,
`assets/sql-cell.js`) rendering a "Check my work" button per task.
Clicking one calls a `check_*` function in `assets/sql_tools.py`
(`check_products_table`, `check_transactions_table`,
`check_products_rows`, `check_transactions_rows`, `check_quiz_queries`)
against the quiz's own connection and shows one line: what is missing,
or that the task's requirements are met. Task 5's check doesn't inspect
the reader's actual queries — there is more than one correct `SELECT` —
only whether the underlying data could answer them (a product over 30,
a product under 15 in stock).

A real, pre-existing accessibility gap turned up building this: axe-core
found `var(--dl-orange)` fails WCAG AA contrast as small text on the
light background (about 3.45:1, needs 4.5:1) — caught because
`.dl-hint`'s summary is always visible, unlike a conditionally-shown
error a normal crawl might never render. `.dl-hint`'s summary text
dropped the orange (kept it only as the left border) and `.dl-sql-error`
switched from orange text to `--dl-fg` text with an orange border. The
same pattern turned out to be pervasive and pre-existing across the rest
of `site.css` — every hover state that coloured its text orange, plus
`.dl-search-match`'s static highlight — so it was fixed properly rather
than piecemeal: a new theme-aware `--dl-orange-text` token (light
`#b04f1a`, dark `#d4692a`, mirroring `--dl-link-default`'s own existing
split for the identical reason) now backs every one of those nine rules,
leaving `--dl-orange` itself for borders, backgrounds and focus outlines,
which already passed the lower 3:1 non-text threshold. Verified live by
hovering each real element (the Settings toggle, a page's table of
contents, a door on the front page, the site editor's and SQL cell's own
buttons, the quiz's Check my work button) and running axe-core in both
themes at both widths — 0 contrast violations throughout.

Verified live: every check button confirmed to fail before the matching
SQL is run and pass after, across all five tasks, in a real browser
against a real Pyodide; the practice page's hints and solutions open and
close; zero console errors throughout. `python -m pytest -q`: 46 tests
(12 new: 7 for the `check_*` functions in `tests/test_sql_tools.py`, 2
for the `sql-check` block in `tests/test_build.py`, plus the persist
tests already counted above). axe-core: 0 violations, no sideways
scroll, on both new pages at 1200 and 390 pixels, after the contrast
fix.

**One Pyodide engine, packages loaded per page, decided 2026-09-05.**
Ahead of step 8: question 16 confirmed Data Arc 2 needs pandas and
matplotlib, not SQL alone (`PAGE_BY_PAGE.md`'s reading of the live
project brief and the pandas notebook sequence already said as much).
The question this raised — one shared Pyodide config for every page, or
a leaner one for Arc 1's SQL-only pages and a heavier one only where
pandas is used — is answered by not choosing: `build.py`'s
`render_body()` now gathers the exact packages a page's own fenced
blocks need (a SQL cell or check still means `sqlite3` alone) and writes
that page's real list into `window.DEWSTACK_SQL_PACKAGES`;
`assets/sql-cell.js` loads exactly that list, nothing assumed. One
engine, one code path, and a page that has not yet used pandas does not
pay to download it. `tools/fetch_pyodide.py`'s own `--packages` default
stays `sqlite3` until a page actually declares more. Verified live: the
existing SQL cell and check pages still boot and run correctly reading
their own declared list; `python -m pytest -q`: 47 tests (1 new).

### Step 8. Data Arc 2, then the full-stack arc

Revised by item 16 (2026-09-05), on top of step 1's earlier revision:
this is where the data track's six themes actually land. SQL is done
(Arc 1, step 7); this arc adds pandas, matplotlib, forms, exploring
data, and exporting/importing as its real content, not as pages tacked
on afterward. The shape step 1 already settled — design before typing;
a real dataset from Our World in Data, loaded, cleaned, queried;
questions that need two tables; a chart from a query — still covers the
SQL-and-design half; pandas and matplotlib are the natural home for
exploring-data-and-charting, and forms and export/import likely want a
page or two of their own beyond that original four. Formal database
theory (normal forms and the like) is explicitly not part of this arc —
deferred to Level 6, per item 16. The packages note just above is the
infrastructure this arc's pandas/matplotlib pages will lean on: whatever
Python/pandas cell type they end up using just needs to declare its own
packages the same way a SQL cell declares `sqlite3`, and only pages using
it pay for the download. Then the three full-stack pages, with plan
section 12 as the outline of the first.

**The page-by-page breakdown, decided 2026-09-05, all six now built —
see "Where things stand" above for the 2026-09-06 slice that finished
pages 2 to 6.** Six pages, not the
original four — more pages is fine where each one stays short, and each
title says what the page does rather than naming a theme:

1. *Designing a table before you build it.* Unchanged from step 1's
   shape: columns, keys, one table or two, no code yet.
2. *Loading a real dataset.* The Our World in Data set (open question 8;
   population and life expectancy by country is the front-runner) comes
   in as a CSV and becomes a SQL table. Where "loaded, cleaned, queried"
   starts.
3. *Joining two real tables.* The same join Arc 1's last page taught, on
   data that is actually messy: missing years, country names that do not
   line up.
4. *Charting a query's result.* Pandas and matplotlib arrive together
   here, not as their own intro page: a `SELECT` result becomes a
   DataFrame becomes a bar or line chart. This is the page the new
   Python/pandas cell type has to exist for.
5. *Exporting a query to a file.* A query's result leaves the browser as
   a CSV — the export half of "exporting/importing", and the one thing
   dewlab's own tutorials never had to solve, since dewstack's data lives
   only in the browser.
6. *A form that writes a row.* Not a new forms tutorial: it links to the
   web track's own form page and shows the query that submitting it would
   run. Josh's call (2026-09-05): the full wiring — a form whose submit
   actually inserts a row — is more interesting once the full-stack pages
   exist, so this page shows the shape and points at plan section 12 for
   where it becomes real.

**The Python/pandas cell engine, built 2026-09-05**, ahead of page 4
actually needing it — the OWID dataset for page 2 is still blocked on
Josh (this sandbox's egress proxy has no route to
`ourworldindata.org`, confirmed both via `curl` and `WebFetch`), but the
engine itself does not depend on which dataset eventually loads. A
fenced `` ```py cell=name `` block becomes a `.dl-py-cell`, the same way
`` ```sql cell=name `` becomes a `.dl-sql-cell`; `assets/python_tools.py`
is `sql_tools.py`'s sibling, ported in shape from dewlab's
`tutorial_tools.py` (its `_render_value()`/`_figure_html()`/
`_table_html()`, and its streaming sink that merges consecutive
`print()`s of the same kind into one block rather than one per write).
`read_sql(db_name, query)` is already in a cell's namespace, and calls
`sql_tools.get_connection()` — the one new public function on that
side — so a page can build a table in a `sql cell=` block and chart it
in a `py cell=` block below without an import, sharing the one Pyodide
both cell types now boot together. `build.py`'s `render_body()` adds
`pandas` and `matplotlib` to a page's declared packages exactly when it
has a `py cell=` block, on top of the `sqlite3` a Python cell also
needs for `read_sql()` to reach a connection. Verified live: a self-hosted
Pyodide (`tools/fetch_pyodide.py --packages sqlite3 pandas matplotlib`,
since the CDN default is blocked here too) served alongside a scratch
page mixing both cell types — the SQL cell built a table, the Python
cell read it back with `read_sql()`, printed a row count, and rendered
a matplotlib chart as its last expression, with no console errors and
no double-rendered figure. `python -m pytest -q`: 78 tests (28 new, all
of `python_tools.py`'s CPython-testable logic — `run_python()` itself
needs Pyodide's `eval_code_async`, so it is left to that live check, the
same split dewlab draws around its own `run_cell()`); CI now installs
`pandas`/`matplotlib` alongside `requirements-build.txt`, matching
dewlab's own `unit` job.

**The full-stack arc's first page, built 2026-09-06** — see "Where
things stand" above for the full account, and `CONSOLIDATION_PLAN.md`
section 12 for the architecture decision behind it (a new cell type,
not the site editor's sandboxed one) and what it changes about the
outline there. `tutorials/full-stack/putting-it-together.order.yaml` is
the arc's own series; `modules.yaml`'s `full-stack` entry is out of
`planned:` now that it has a real page.

### Ongoing, every step

- When a rewritten page lands, the front page links it and the ledger in
  plan section 7 gets its row. When every page a copy fed has landed,
  the copy goes from `sources/` and `PAGE_BY_PAGE.md` says so.
- `CLAUDE.md` says how to run things. Keep it true.

---

## 4. Open questions

The ones that block a step are marked. The rest can be answered when the
step arrives.

1. **Hello page or A0?** Decided 2026-09-04, per the recommendation:
   folded into one page. `how-the-pieces-fit` covers the course and the
   shell together; the `hello` slug is retired.
2. **The second starter's name and shape.** Decided 2026-09-05, by Josh:
   `project_wad`, alongside `web` renamed to `portfolio_wad`. Both are
   GitHub template repositories, so both the **Fork** button and
   **Use this template** are open to a student; getting-started page A3
   covers both. See step 6's note for the naming reasoning.
3. **Module and series slugs.** Settled for `reference` (module
   `reference`, series `shelf`) with step 2. Still open: `getting-started`
   (exists), `web` with series `first-site`, `several-pages`,
   `with-data`; `data` with series `first-table`, `several-tables`. A
   slug is a contract once a class has seen it, so these should be
   settled before the first page in each.
4. **The editor widget.** Decided 2026-09-04, per the recommendation:
   `textarea`s. CodeMirror stays an option later if a page needs
   highlighting or bracket matching; the markdown contract (`site=name`
   fenced blocks) would not change.
5. **Where Pyodide is served from** (blocks step 7). dewlab's arrangement
   is the one to check: a CDN or self-hosted under `assets/vendor/`.
   Self-hosting is a large commit and no surprises; a CDN is small and a
   dependency. Whichever dewlab does is the default.
6. **The student's database file.** Decided 2026-09-05: the browser's own
   storage. A `persist` SQL cell saves its script to `localStorage` and
   restores and re-runs it on the next visit, so the table is already
   there rather than something to download and load back in; Download
   stays as a secondary way to take a copy out of the browser. Settled by
   `NEXT_STEPS.md` step 7's persistence note, not by the `web` model's
   file-in-a-fork — there is no repository of the student's own on the
   data track to commit it to.
7. **A Pages site for `web`** (plan question 6, still open). It would let
   the starter's README show a live example. Not needed for the tutorial
   to work.
8. **The Our World in Data dataset** for data Arc 2. Resolved
   2026-09-06, by Josh's own content rather than the population/life-
   expectancy guess: the World Inequality Database's "income share of
   the top 1%" series, the same one his Database Methods project brief
   already teaches. Licence is CC BY; the pages credit it. See "Where
   things stand" above for what is and is not yet verified against it.
9. **The high-contrast fix.** dewlab#114, open, fixes elements the
   high-contrast mode silently skipped. The shell's CSS was copied before
   that fix. Check whether it applies here once #114 merges.
10. **`tools/add_course_bar.py`.** The copies are unpublished, so the bar
    on them links nowhere. Delete the tool and the bars, or keep them
    until the copies go? Keeping costs nothing and deleting is one
    commit either way.
11. **The README as front page.** Decided 2026-09-04, evening: no. The
    README rendered as the front page was 1,600 words and 28 outbound
    links before the list of this site's own pages, and a student had to
    scroll past "For teachers" to reach it. The front page now has its
    own shape, in dewlab's: `tutorials/front.md` gives an opening under
    two hundred words and two doors that open onto pages here, then the
    search box and the list. `modules.yaml` names the modules not yet
    written so the shape of the course shows. The README stays the
    GitHub-facing map. The default line width also came down from 34rem
    to 30rem at Josh's request, with the Settings presets to match.
12. **Dates.** Term start, the date the project brief is issued, and the
    exam window, so that steps 3, 6 and 7 have deadlines. The plan says
    January for the brief; confirm.
13. **Level 6 reuse** (plan question 14). First pass done:
    `planning/LEVEL6_COVERAGE.md`. Open within it: three outcomes (a
    multi-tier architecture with a database server, an installed CMS,
    FTP/domain hosting) don't fit a static, no-backend site at all, and
    whether this repository is meant to satisfy 6N1277 on its own or
    alongside a separate CMS/hosting unit is Josh's call, not something
    to resolve by writing a page that doesn't really cover it.
14. **Break and Make a Website's placement.** Josh wants to consider it
    on its own rather than as plain enrichment. `LEVEL6_COVERAGE.md`
    proposes it as the vehicle for a Level 6 client-side-scripting step
    (DOM manipulation, form validation, `localStorage`) sitting after
    web Arc 2 and before the full-stack arc; the Irish Tax Simulator
    artefact itself stays enrichment either way. Not decided.
15. **The web track's teaching order, decided 2026-09-05.** Regroup and
    resequence Arc 1 around four stages — Basic HTML, Basic CSS, merging
    the two, then modern HTML/CSS (Flexbox, Grid, the rest of Arc 1's C
    rows) — rather than replacing the arc structure. `portfolio_wad` and
    `project_wad` stay the artefacts; the existing B and C row pages are
    material to regroup, not rewrite from nothing. A JavaScript module is
    added to `modules.yaml`'s `planned:` section, the same mechanism
    already used for `data` and `full-stack`, marked coming soon. Also
    wanted, not yet scoped: GitHub tutorials (getting-started's A1, A3 to
    A5 may already cover most of this — check before writing new ones)
    and a concrete page on how the internet works and how these
    technologies fit together, with further-reading resources.
16. **The data track's themes, decided 2026-09-05.** SQL, pandas,
    matplotlib, forms, exploring data, and exporting/importing are the
    content of Data Arc 1 and Arc 2 themselves, not additional pages
    after them — Josh's reasoning: SQL alone does not cover the Database
    Methods learning outcomes, and formal database theory (normal forms
    and the like) belongs to Level 6, not here, so it is deferred rather
    than added. `everlearning`'s teaching materials (including the exam)
    and "the flowershow website" both have material covering this ground
    already — the flowershow link is still needed from Josh before either
    can be quarried.
17. **WADB_Tutorials, reframed 2026-09-05, then the reframing itself
    reversed the same day.** First move: rather than a legacy source
    being slowly superseded, it became its own named path — "Previous
    Web Authoring Path" — offered alongside the redesigned one rather
    than retired. Lessons 11 to 13 (Flexbox/Grid, component design, CSS
    animation) were rebuilt as native pages under that name. The SQL
    quiz was rebuilt too, independently and at nearly the same time, as
    the data track's own official practice page (step 7 item 4, below)
    — the two efforts collided, and the copy under the new module was
    removed once that became clear, rather than keeping two quizzes
    teaching the same five tasks. That left the module holding only the
    three layout/animation pages. Second move, once item 15's four
    web-authoring stages were decided: those three pages are exactly
    "modern HTML/CSS" by any reading, so they moved again, into `web`'s
    `first-site` series proper, right after `flexbox-first-steps`. With
    nothing left in it, Previous Web Authoring Path was retired rather
    than kept as an empty shell — `modules.yaml`'s entry and note, the
    front page's mention, and the module's own folder are all gone. The
    net effect: WADB_Tutorials' content is now fully absorbed into the
    redesign, and the "keep it as a separate path" idea did not survive
    contact with the four-stage plan — worth knowing if the same idea
    comes up again for the parts of WADB_Tutorials still not superseded
    (lessons 11 to 13's own originals stay live at their old address
    regardless, per the ground rules).
18. **The several-pages series does not need a name in the four-stage
    scheme, decided 2026-09-05.** `planning-a-site`, `pages-and-navigation`,
    `a-form`, `images-and-file-size`, `documenting-what-you-built` are not
    part of teaching HTML and CSS from basic to modern — they are Web Arc
    2's own already-established role, applying the language to a real
    multi-page site via the second starter, `project_wad`. Item 15's four
    stages describe Arc 1; Arc 2 stays Arc 2, under its own existing name
    (step 6), rather than being folded in or given a fifth stage name it
    was never asked to have.
19. **A console for the site editor, and a workspace page, designed
    2026-09-06.** `planning/CONSOLE_AND_WORKSPACE.md` is the design:
    a console under the site editor's preview (console output, every
    uncaught error, the exact JavaScript-pane line, a plain-language
    second line for the common errors), then a page of dewstack's own
    where a student keeps several named sites in the browser, with an
    "Open in the workspace" button on tutorial-page editors as the
    bridge. The console is the thing that unblocks the JavaScript
    track: today a script that throws just stops the preview changing.
    Decided 2026-09-06, all four of its section 9 calls: CodeMirror on
    the workspace page only, with textareas staying on tutorial pages;
    "port in shape" stays the only rule between the repositories, no
    twinned files; the console opens whenever an editor has a
    JavaScript pane; and the page is called the dewstack workspace.
    Josh's own addition, which replaced the design's debounce: a Run
    button for JavaScript, so a program runs when asked and a student
    takes time with their code, while HTML and CSS stay live. Step 1
    (the console and Run on tutorial pages) shipped the same day; see
    Step 6 above. Step 2, the workspace page, shipped the same day too:
    `workspace/index.html`, built by `write_workspace()`, the same
    component mounted by `assets/workspace.js` over CodeMirror panes
    (`vendor-src/` builds `assets/vendor/codemirror.bundle.js`, loaded
    on this page alone, with a CI job that fails if the committed bundle
    drifts from its inputs), several named sites saved under
    `dewstack:workspace:v1`, New, rename, a two-click Delete, Load files
    and Download. A door to it on the front page, in the shape of
    dewlab's own. Eleven Playwright tests in `tests/e2e/test_workspace.py`.
    One thing found on the way and fixed in the component for both pages:
    four synchronous `srcdoc` writes in one task loaded only the first,
    so `render()` now writes once per frame load and parks the newest
    document until then. Step 3, "Open in the workspace" under every
    tutorial-page editor, shipped the same day: the three panes go into
    a hand-off key (`dewstack:workspace:incoming`) and the workspace
    makes a site from them on arrival, named after the page and the
    editor, with the save flushed on `pagehide` so a tab closed at once
    keeps it. Step 4 (the editor) is done by the workspace's CodeMirror.
    Step 5, the console in dewmini's Site view, is dewlab's and remains.

20. **Hints that appear after a cell has errored or run some number of
    times.** Raised by Josh 2026-09-06 for both repositories; dewlab's
    half built the same day (its DECISIONS_LOG.md 7.135). Built here
    2026-09-07 for `sql-check` blocks only — this repository's
    `planning/CELL_HINTS.md` §6 records what shipped: the same
    ```` ```hint ```` fence, `for:` naming a check's `task=` value and
    always required (no "block above" to default to), `after:` reading
    `check-fails`/`runs`/`minutes` only, the runtime ported into
    `assets/sql-cell.js`, one Settings row (no page-wide restart action
    to hang a second one off), tried on the tentacular-plushies quiz's
    Tasks 1 and 3. SQL/Python cell hints, the web track, a generic SQL
    `expect`, and a browser end-to-end test are not built — §6 lists them
    as the next pieces. Blocks nothing.

---

## 5. How to start the next session

Read, in this order: `CLAUDE.md` (two minutes), this document, plan
sections 8, 11 and 15, and the part of `PAGE_BY_PAGE.md` for whichever
source the step quarries. Then:

```bash
pip install -r requirements-build.txt
python3 -m pytest
python3 build.py --clean
python3 tools/measure_sentences.py README.md tutorials/**/*.md
```

A new page is a folder `tutorials/<module>/<slug>/<slug>.md` with this
frontmatter, listed in `tutorials/<module>/<series>.order.yaml`, with
the module in `tutorials/modules.yaml`:

```yaml
---
title: "Flexbox first steps"
slug: flexbox-first-steps
module: web
module_title: "Web authoring"
series: first-site
version: 2026.09.10.1
---
```

`status: draft` builds the page and keeps it off the front page and out
of search, which is how a page is reviewed before it is listed. A link to
another page is `tutorial:<slug>`, and the build stops if the slug does
not exist. Every image needs alt text or the build stops.

Before a page is pushed: the eight checks in `CLAUDE.md`, the sentence
tool, and a look at the built page at 1200 and 390 pixels. In this
session that look was a headless Chromium screenshot through Playwright;
any browser's device mode does the same. Then one pull request per page,
draft, with what was checked in its description.

Conventions from the sessions so far that are not written anywhere else:
no pull request is watched or scheduled unless Josh asks; nothing is
deleted from a source repository, ever; the source copies in `sources/`
are never edited; and the register for anything a student reads is the
plain-language bar, while the register for the planning documents is
this one.

---

## 6. Text held for later

**The "Where this fits" section for `web`'s README**, to go in after
web#1 merges, after the welcome paragraph. Links corrected from the
closed draft: the original pointed at tutorial pages that lived under
dewstack for a day.

> ## Where this fits
>
> This tutorial is the first step of the Web Authoring and Databases
> course. The course front page is at
> [deweydex.github.io/dewstack](https://deweydex.github.io/dewstack/).
> It holds the plan for the whole course and every link you need. When
> an exercise here leaves you with a question, the tutorials listed there
> have the longer explanation. The
> [GitHub guides](https://deweydex.github.io/WADB_Tutorials/github-guides/01-getting-started.html)
> show each step of making an account, saving your work, and publishing
> a site.

Once the getting-started pages exist, the GitHub guides link moves to
them.
