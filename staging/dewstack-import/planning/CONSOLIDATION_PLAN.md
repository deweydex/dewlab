# Consolidation plan

How the web authoring and database materials come together in this
repository, in what order, and what "done" means for each step. Written so
that a later session can pick it up without rediscovering the reasoning.

Last updated: 2026-09-03, late evening, after the front page, the reading
settings and the interim copies landed (section 7). The ledger in section 7
says what has moved and what has not.

---

## 1. The shape we are aiming for

**One home.** `dewadaba` becomes the single place a student is sent to for
the web authoring and database course. Everything else either feeds into it
or is linked from it.

**The main page is the README, and `index.html` is its published twin.**
GitHub renders the README, so it needs no build step, no hosting and no
styling to go wrong. `HTML-CSS-SQL-JS` already works this way and its README
is the model for the layout. The text itself is rewritten to the house style
(section 3). Josh also asked for the front page as a web page in the idiom
of the `HTML-CSS-SQL-JS` page, with dewlab's reading settings, so
`index.html` carries the same stages and links as the README, in the same
order, using a copy of the playground's stylesheet. When one changes, the
other changes to match; the README is the text of record.

**The README is a course map, in stages.** Each stage names what the student
will be able to do at the end of it, and links to where the work happens.

| Stage | Where the work happens | What the student ends up with |
|---|---|---|
| 1. Build a site | [`deweydex/portfolio_wad`](https://github.com/deweydex/portfolio_wad), forked or templated by the student | A personal site with a real address, published on GitHub Pages. From nothing to a portfolio. |
| 2. Work with data | Tutorials in this repository (section 5) | A database they built and queried in the browser, and the words to talk about it. |
| 3. Put the two together | Tutorials in this repository, later | A page that shows data from a database. Scope still open (section 8). |

Stage 1 links to the repository on GitHub, not to a Pages address. The
student's first act is to fork it, so the repository page is the right
front door.

**The tutorials live in a content component here.** A build step turns
markdown into pages with a shared shell, so every page carries the same
navigation, search and settings. Section 5 says why a build step and not
hand-written HTML.

**Where each existing repository ends up.**

| Repository | Fate |
|---|---|
| `portfolio_wad` (renamed from `web`) | Stays. Linked from the README as stage 1. The one tutorial we edit now (section 4). |
| `HTML-CSS-SQL-JS` | Stays untouched until its SQL section and teacher notes have moved here. Then archived. Meanwhile a verbatim copy sits at `databases/playground/` here, so the course has one address. |
| `WADB_Tutorials` | Stays untouched until its content has moved here, piece by piece. Then archived. Its Pages site stays live throughout. Meanwhile a verbatim copy sits at `tutorials/` here as an interim shelf; it inherits every defect in section 9 and is replaced page by page as section 7 proceeds. |
| `dewlab` | Stays. The source of the shell, settings and search we port. Not edited from here. |
| `project_wad` (renamed from `portfoliotest`) | No longer personal or left alone: this is the second starter, section 15's Arc 2 door. Its old README (Josh's own, a photograph and a résumé link) is replaced by the five-page skeleton, kept in git history rather than deleted. |
| `aiml-web-authoring`, `webauthoringdemo` | Already removed. |

---

## 2. Ground rules

**Nothing is deleted or rewritten at its source.** Content is copied here,
improved here, and the original stays where it was until the new version
has been in front of a class. The interim copies under `tutorials/` and
`databases/playground/` are byte-identical to their sources apart from one
addition, made at Josh's request so the pages link together: a course bar
at the top of each page with a link to the front page and its stages.
`tools/add_course_bar.py` inserts it, after the skip-to-content link where
there is one, and can insert it again after a copy is refreshed. Templates
and examples do not get it, because students copy those files. Archiving a repository is Josh's action, taken
after the links have moved. `web` is the one exception, because it is the
introduction and it is worth fixing in place.

**One piece per pull request.** A section of the README, one tutorial, one
resource page. Each pull request carries screenshots at desktop and phone
widths and the result of an accessibility run (section 3). Small pull
requests are how the source stays safe: a mistake is one revert, not a
rebuild.

**The designated branch for this session is
`claude/repo-consolidation-strategy-8m3miy`.** Later sessions use their own.

**Cell ids and exercise numbers are a contract once a class has seen
them.** Renaming a cell id throws away saved work. Renumbering an exercise
breaks the way students refer to it. Both are decided once and left alone.

---

## 3. The bar every student-facing word has to clear

The style guide is `planning/PEDAGOGICAL_STYLE_GUIDE.md` in `dewlab`,
section 4, including its "Plain language" and "Vocabulary" subsections. It
applies to the README here, to every tutorial, and to `web` once we edit it.
The plain-language checks, run over anything before it is committed:

1. Every sentence has a verb.
2. Every clause earns its place. Read the sentence back, then try a
   shorter version; if it still says the same thing, the clause that
   vanished was never necessary.
3. The meaning comes before the dash, never after it. One dash to a
   paragraph at most.
4. Say what a thing is before what it is not.
5. Mark a sequence: first, then, then.
6. A metaphor follows a plain statement. It never replaces one.
7. No idiom that assumes Irish or British English.
8. Hedge what is not a binary.
9. No idiom from any dialect, and no rare word where a common one works —
   pitched at a reader with about two thousand English words.

Two more that are easy to get wrong. Use "we" for the learning and "you"
for what is the student's own. Explore first, then the principle, then the
name, with a sentence on what the name is for. No emoji in student text.

**The accessibility bar** for every page that is not a README:

- The axe engine reports no serious or critical violations.
- No sideways scrolling at a 390 pixel viewport.
- Every page has a `main` landmark and a labelled `nav`.
- The menu opens and closes from the keyboard, moves focus into itself when
  it opens, and closes on Escape.
- Text contrast of at least 4.5 to 1, including links and code spans.

These are the bars the audit of `WADB_Tutorials` on 2026-09-03 found unmet.
Section 9 has the findings.

**Skills to use.** `josh-register` for any prose. `argument-signposting` as
a review pass on the README once it has more than three sections. Once the
build step exists, `tutorial-glossary` for each tutorial's glossary file and
`cell-code-review` for its code cells. Both assume dewlab's folder layout,
which section 5 keeps.

---

## 4. Phase 1: the main page

**What.** Replace the two-line README with the course map from section 1.

**Contents, in the order a student meets them.**

1. What this course is and who it is for. Two short paragraphs.
2. The three stages, each with a heading, what the student will be able to
   do at the end, and one link to where the work happens.
3. What they need: a GitHub account, a browser, a text editor. Nothing
   installed.
4. How to use the materials: work in order, or jump to what they need.
   Where their work is saved, once section 5 exists.
5. Every link in one table: repository and published site for each of
   `web`, `WADB_Tutorials`, `HTML-CSS-SQL-JS` and this repository's own
   tutorials.
6. A short line for teachers pointing at `planning/`.

**Links to verify before the README ships.** The Pages address for
`WADB_Tutorials` is confirmed live. The Pages addresses for
`HTML-CSS-SQL-JS` and `dewlab` are assumed and have not been fetched from
this environment. A link that does not resolve is a bug, not a note.

**Done when** the plain-language checks pass, every link resolves, the old name
"databaseL5" is gone, and Josh has read it.

*2026-09-03, evening.* The README has the three stages as drafted, plus the
stage 2 links now that the playground is here, a section for the interim
tutorials shelf, and the published twin `index.html` with reading settings
(theme, typeface with Atkinson Hyperlegible and OpenDyslexic self-hosted,
text size, line width, high contrast; `assets/`). The Pages addresses for
`HTML-CSS-SQL-JS`, `WADB_Tutorials` and this repository could not be
fetched from the session that wrote this note either; they stay unverified.

---

## 5. Phase 2: `web`, the one tutorial we edit

`web` is a fork-and-edit tutorial. The README is the teaching text, twenty
five exercises long, and `index.html`, `about.html` and `styles.css` are the
files the student changes. `CONCEPTS.md` is optional depth. The shape is
right and stays. The work is on the sentences and on the code files'
accessibility.

**Step 1. Audit before editing.** Render the three files at desktop and
phone widths, run axe, and read the README against the plain-language checks. Record
what is found in the ledger before changing anything.

*Done 2026-09-03. What the audit found:*

- Both pages have a `main` landmark, one `h1`, headings in order, a focus
  style on every link, and no sideways scroll at 390 pixels. This is a
  better starting point than any page in `WADB_Tutorials`.
- Two colour choices fail contrast. The accent blue `#3498db` under white
  button text measures 3.15 to 1 on both pages. The muted grey `#7f8c8d` on
  the light background measures 3.29 to 1 on three elements of the About
  page. Both are variables in `styles.css`, so each is a one-line change.
  Exercise 13 asks the student to change these colours, which is a chance
  to say what contrast is and why the defaults were chosen.
- The `nav` has no label and there is no skip link. Both are small
  additions, and the comment beside each is a chance to teach them.
- `README.md` averages eleven words a sentence, which is well inside the
  target. It has twenty-six em dashes, most of them carrying the sense of
  the sentence, and one reversal ("that's not failure, that's
  information"). Idioms to replace: "sit with it", "wander off the path",
  "click" in the sense of understanding, "kick in", "comfort with
  indeterminacy", "feel free".
- `CONCEPTS.md` averages eleven and a half words a sentence. Eight em
  dashes, one reversal, and "boxes all the way down".
- No emoji in either file.

**Step 2. The plain-language pass on `README.md` and `CONCEPTS.md`.** What a
first read already shows:

- Em dashes carry the meaning in many sentences ("a real site with a real
  URL", "that's not failure, that's information"). Rule 3.
- Idioms a second-language reader cannot see: "sit with it", "wander off
  the path", "won't click", "kick in", "boxes all the way down", "comfort
  with indeterminacy". Rules 6 and 7.
- Definitions that arrive as contrast: "not failure, that's information".
  Rule 4.
- The "Explore" prompts are the best part of the tutorial and stay. They
  are invitational in exactly the way the style guide asks for.

Exercise numbers, headings and file names do not change. Students' forks
and the exercises they refer to depend on them.

**Step 3. The code files.** `index.html` and `about.html` are what the
student publishes, so they should pass the accessibility bar as shipped.
Check landmarks, heading order, focus styles, contrast of the default
colours, and the comment text, which is student-facing too.

**Step 4. Decide whether `web` gets a Pages site of its own.** It would let
the README link to a live example. It is not needed for the tutorial to
work.

**Step 5. The gap against the assessment brief.** Assignment 1 asks for
`index.html`, `about.html`, `contact.html`, `styles.css`, `planning.md`,
`readme.md` and an `images/` folder. The starter has the first two and the
stylesheet. Add `contact.html` in the same commented style, with two or
three exercises of its own after exercise 12, and an `images/` folder with
a note in it. Point at the planning and README templates on the course
site rather than copying them, so the brief stays the one source. Done
when a student can go from fork to the brief's file list by following the
README alone.

**Step 6. Say where the tutorial fits.** A short section after the welcome
naming this tutorial as stage 1 of the course, with links to the front
page, the tutorials and the GitHub guides. Drafted as
[deweydex/web#2](https://github.com/deweydex/web/pull/2) and closed
unmerged, because it touches the paragraph #1 rewrites; the text is in that
PR and goes in on top of #1 once #1 has merged.

**Needs before starting.** `web` is attached to this session for reading
only. Editing it needs it attached with push access, and its own branch and
pull request.

**Done when** the audit findings are closed, the plain-language checks pass on both
markdown files, and a fresh fork renders cleanly at both widths.

---

## 6. Phase 3: the tutorial component

**The decision: a build step, modelled on dewlab.** Markdown in
`tutorials/`, a shell template, a script that writes `site/`, and a
workflow that publishes it on every push to `main`.

**Why not hand-written HTML, as `WADB_Tutorials` is.** Every defect the
audit found there is a drift defect. Six of forty-two pages have search.
Twenty-one lack the theme switcher. Three pages overflow a phone screen for
three different reasons. The pages were correct once and stopped agreeing
with each other as features were added one file at a time. A template
removes the whole class.

**What to port from dewlab, and what not to.**

| Port | Leave |
|---|---|
| `assets/shell.html`: the masthead, the three sidebars, the settings panel with theme, typeface, size and line width | The Pyodide runtime, for now (see the open question in section 8) |
| The colour and type tokens in `assets/tutorial-style.css`, and its dark theme | The authoring editor |
| `assets/search.js` and the way the build writes its index | The topic tree and browse-by-topic pages |
| The folder layout: `tutorials/<module>/<slug>/<slug>.md`, order files, glossary files | The maths handling |
| The build's checks: a dead link fails the build, an image without alt text fails the build | |
| The deploy workflow | |

*Decision, 2026-09-04.* The plan first said to copy dewlab's `build.py`
and trim it. Measured, that script is over four thousand lines and bound
to Pyodide, the authoring editor, the topic tree, zips and the dewmini
bundle. Trimming it would take longer than writing the part a reading
site needs. So the build here is a new script of a few hundred lines that
borrows the design and not the code: the same layout of `tutorials/`,
the same frontmatter fields, the same strict checks, and dewlab's shell,
tokens, Settings panel and search script carried over as files. What is
left out on purpose, for now: a resizable panel, the reference sidebar,
versioned releases, and downloadable copies. Each can come later without
changing a page's address.

*Reconciled, 2026-09-04, dewstack#5.* The build, shell and settings panel
above were written in [dewadaba#3](https://github.com/deweydex/dewadaba/pull/3)
while section 8's question 9 was being answered the other way, as "a copy
of dewlab's build and runtime". Josh chose to take #3's build as the
platform. Question 9 now reads: dewlab's design, not its code, for the
reading site; the Pyodide engine and `tutorial_tools.py` are copied in
from dewlab when data Arc 1 needs a SQL cell, and not before. The build
owns `tutorials/`, so the interim copies moved to `sources/`, and the
front page is `README.md` rendered by the build rather than a hand-made
`index.html`. The reading settings from dewadaba#2 gave way to the shell's
panel, which has the same choices and more.

**The runtime question.** A SQL cell needs an engine in the browser.
`HTML-CSS-SQL-JS` uses sql.js, which is light. dewlab chose Python's own
`sqlite3` through Pyodide, which is heavy but lets a SQL table and a pandas
table see each other. For a database course that never touches Python,
sql.js is the smaller thing to carry. This is Josh's call; section 8.

**First deliverable.** One page that says hello, built and published, with
the shell working at both widths and the accessibility bar met. The
pipeline is proven before any content moves.

**Done when** `python3 build.py` writes `site/` from a hello page, the
workflow publishes it, and the hello page passes the bar in section 3.

---

## 7. Phase 4: moving content, one piece at a time

Order of movement. Each item is one pull request and one ledger row.

**First, the database material**, because it is the reason this repository
exists and it has no home elsewhere.

1. The SQL section of `HTML-CSS-SQL-JS/index.html` becomes the first
   tutorial in a "Databases" module: what a table is, select, where, order
   by, insert, update, delete, with the students-and-courses sample data.
2. The exercises from the same page become its practice page.
3. `teacher.html` holds solutions and teaching notes. Decision needed on
   whether solutions stay public (section 8). The teaching notes go to
   `planning/`.
4. The quiz in `WADB_Tutorials/tentacular-plushies-quiz-final.html` is
   rebuilt as a page in the shell. Its five tasks and its reference panel
   are good. Its fixed three-panel layout is not, and does not survive a
   phone.

**Then the resource pages from `WADB_Tutorials`**, which are useful to
both stages: the quick reference, troubleshooting, project ideas and design
resources.

**Then the lessons from `WADB_Tutorials`.** Lessons 1 to 8 cover ground
that `web` now covers by doing. Lessons 9 to 13 and the seven GitHub guides
add things `web` does not. Which of the first eight survive is a decision
for Josh (section 8), taken after `web` has been through its pass.

**Not moved.** `Educational_Reference_Document.md`,
`GIT_PUSH_INSTRUCTIONS.md`, `recent_chat_ideas.md`,
`session_plan_advanced_content.md` and `.DS_Store`. These are session notes
and a prompt, not course material.

**For every piece that moves:**

1. Copy the source into `tutorials/`, converting HTML to markdown.
2. The plain-language pass, against the plain-language checks.
3. A glossary file, with the `tutorial-glossary` skill.
4. If it has code cells, the `cell-code-review` skill.
5. Screenshots at both widths and an axe run.
6. A ledger row.

The source file is not touched.

### The ledger

| Item | From | To | Status |
|---|---|---|---|
| README course map | this plan, section 4 | `README.md` | drafted 2026-09-03, awaiting Josh's read; the `HTML-CSS-SQL-JS` Pages link is unverified |
| `web` audit | `deweydex/web` | section 5, step 1 | done 2026-09-03 |
| `web` plain-language pass, colour fixes, skip link and nav label | `deweydex/web` | in place | done 2026-09-03, open as [deweydex/web#1](https://github.com/deweydex/web/pull/1), awaiting Josh's read |
| Front page as a web page, in the playground's idiom; rewritten to the five parts of section 10 | this plan, sections 1, 4 and 10 | `README.md`, rendered by `build.py` as the site's front page | done 2026-09-04, [dewadaba#2](https://github.com/deweydex/dewadaba/pull/2); the hand-made `index.html` and `styles.css` went in dewstack#5 |
| Reading settings: theme, typeface, size, width, high contrast | `dewlab/assets/tutorial-runtime.js`, `tutorial-style.css`, `vendor/fonts` | the shell's Settings panel, `assets/settings.js`, `assets/site.css`, `assets/fonts/` | done 2026-09-03, dewadaba#2; superseded by dewadaba#3's panel, dewstack#5 |
| Interim shelf: `WADB_Tutorials` verbatim | `deweydex/WADB_Tutorials` | `sources/wadb/` | done 2026-09-03, dewadaba#2; moved out of `tutorials/` in dewstack#5; coverage material, not published |
| Interim copy of the playground | `deweydex/HTML-CSS-SQL-JS` | `sources/playground/` | done 2026-09-03, dewadaba#2; moved in dewstack#5; coverage material, not published |
| SQLite notebook | course site assets | `databases/sqlite_tutorial.ipynb` | done 2026-09-03, dewadaba#2 |
| Course bar on every copied page | this plan, section 2 | `tools/add_course_bar.py` | done 2026-09-03, dewadaba#2; now aimed at `sources/`, where the bar's links are moot because the copies are not published |
| Page-by-page assessment of the three sources, with the order of rewrites | this plan, section 10 | `planning/PAGE_BY_PAGE.md` | done 2026-09-04, dewadaba#2 |
| `web` "Where this fits" section | section 5, step 6 | `deweydex/web` README | drafted as web#2, closed; lands after web#1 merges |
| Build step and hello page | `dewlab`, by design | `build.py`, `assets/`, `tutorials/` | done 2026-09-04, dewadaba#3, reconciled with `main` in dewstack#5; awaiting the first publish run to turn Pages on |
| Getting started, A0 to A6 (hello folded into A0, its slug retired) | `sources/wadb/github-guides/`, `lessons/01-html-basics.html` (first third) | `tutorials/getting-started/`, series `welcome` | done 2026-09-04; `NEXT_STEPS.md` step 3 |
| Reconciliation of dewadaba#3 with `main`: build as the platform, copies to `sources/`, README as the built front page, dewstack throughout | dewadaba#3, dewadaba#4 | this repository | done 2026-09-04, dewstack#5 |
| Site editor component for web pages | dewmini's Site tab (`dewlab/compose/dewmini.js`) | `build.py`, `assets/site-editor.js`, `assets/site.css` | done 2026-09-04; `NEXT_STEPS.md` step 4; textareas, not CodeMirror |
| Flexbox first steps, the first page to use it | `web/CONCEPTS.md`, `sources/wadb/lessons/04-css-layout.html` | `tutorials/web/flexbox-first-steps/`, module `web`, series `first-site` | done 2026-09-04; section 13's "done when"; repositioned to the close of the series once B1 to B4 existed |
| Web Arc 1, B1 to B4 (a page is files; the skeleton; headings, paragraphs and emphasis; sections and semantic tags) | `deweydex/web` exercises 3 to 8, `web/CONCEPTS.md`'s semantic section | `tutorials/web/`, module `web`, series `first-site` | done 2026-09-04; `NEXT_STEPS.md` step 5, in progress |
| Web Arc 1, B5 to B7 (images and alt text; three kinds of link; navigation) | `deweydex/web` exercises 9 to 12 | `tutorials/web/`, module `web`, series `first-site` | done 2026-09-04; `NEXT_STEPS.md` step 5, in progress; found and fixed a site-editor bug (`about:srcdoc` base tag) along the way |
| Web Arc 1, C1 to C3 (a rule and where it lives; variables and colour; the box) | `deweydex/web` exercises 13 to 16, `web/CONCEPTS.md`'s box section | `tutorials/web/`, module `web`, series `first-site` | done 2026-09-04; `NEXT_STEPS.md` step 5, in progress |
| Web Arc 1, C4 and C5 (text and units; selectors and classes) | `deweydex/web` exercises 17, 18, `web/CONCEPTS.md`'s units and selectors sections | `tutorials/web/`, module `web`, series `first-site` | done 2026-09-04; `NEXT_STEPS.md` step 5, in progress; C6 (specificity, optional depth) left for later |
| Web Arc 1, C7 to C9 (the container; position and the sticky header; hover and focus) | `deweydex/web` exercises 19 to 23 | `tutorials/web/`, module `web`, series `first-site` | done 2026-09-04; `NEXT_STEPS.md` step 5, in progress |
| Web Arc 1, C10 to C12 (transitions and transforms; media queries; flexible images) | `deweydex/web` exercises 22, 24; `sources/wadb/lessons/05-responsive-design.html`, `09-images.html` | `tutorials/web/`, module `web`, series `first-site` | done 2026-09-04; `NEXT_STEPS.md` step 5; all of Arc 1's C rows now written bar C6 (optional depth) |
| Second starter, `project_wad` | Josh's `portfoliotest`, repurposed; the brief's file list | `deweydex/project_wad`: five HTML pages, `styles.css`, `planning.md`/`readme.md`/`maintenance.md` | done 2026-09-05; `NEXT_STEPS.md` step 6; the three templates written fresh rather than adapted from the ML-specific ones in `sources/teaching-materials/` |
| Web Arc 2, D1 to D8, all eight pages (planning a site; pages and navigation; cards in a row; a grid gallery; navigation on a phone; a form; images and file size; documenting what you built) | `project_wad`'s own files; `sources/wadb/lessons/11-flexbox-grid-advanced.html` for flex-grow/shrink/basis and `minmax()` | `tutorials/web/`, module `web`, new series `several-pages` | done 2026-09-05; `NEXT_STEPS.md` step 6 done; each "your turn" points at `project_wad`'s real code, not new code written for the tutorial; `images-and-file-size` has no site editor, since file size is not a live-preview concept |
| Handover: where things stand, the order of work, open questions | this plan, sections 8, 14, 15 | `planning/NEXT_STEPS.md` | done 2026-09-04; the document a session opens first |
| More database content from Josh | `everlearning`'s `Teaching materials/` | `sources/teaching-materials/` | arrived and copied 2026-09-04; assessed in `PAGE_BY_PAGE.md` section 6 |
| Level 6 (`Web Development 6N1277`) coverage assessment | module descriptor Josh attached, 2026-09-04 | `planning/LEVEL6_COVERAGE.md` | done 2026-09-04; a coverage map, not new pages — nothing scheduled |
| SQL cell runtime: Pyodide boot, `run_sql()`, the `` ```sql cell=name `` block | dewlab's `pyodide-engine.js`/`pyodide-worker.js`/`tutorial_tools.py`, ported in shape rather than copied (`NEXT_STEPS.md` step 7's decision record) | `assets/sql-cell.js`, `assets/sql_tools.py`, `assets/site.css`, `build.py`, `tools/fetch_pyodide.py` | done 2026-09-05; `NEXT_STEPS.md` step 7, runtime only; verified live against a real, trimmed, self-hosted Pyodide, since this sandbox's egress proxy blocks the CDN `sql-cell.js` defaults to |
| Data Arc 1, four pages (a table is a list of rows; asking questions of a table; changing what is in it; a second table and a join) | `databases/sqlite_tutorial.ipynb` (the dinosaur notebook)'s sequence and seed data; the playground's SELECT/WHERE/ORDER BY/INSERT/UPDATE/DELETE command cards | `tutorials/data/`, module `data`, new series `first-database` | done 2026-09-05; `NEXT_STEPS.md` step 7 item 3; the join page is new rather than ported, since the notebook itself only `UNION`s its two tables |
| SQL cell persistence: a `persist` cell saves to `localStorage` and restores itself | conversation about the arc's own continuity, superseding the Download/Load-only design above | `assets/sql-cell.js`, `build.py`, `assets/site.css`, all four Data Arc 1 pages | done 2026-09-05; `NEXT_STEPS.md` step 7's persistence note; verified live across a real page navigation, not just within one page |
| SQL practice page | `HTML-CSS-SQL-JS/index.html`'s five exercises and command cards | `tutorials/data/sql-practice/`, module `data`, new series `practice` | done 2026-09-05; `NEXT_STEPS.md` step 7 item 4; students/courses seed data kept distinct from Arc 1's dinosaurs on purpose, so the exercises test transfer; hints per exercise, solutions collected at the foot |
| Teaching notes | `HTML-CSS-SQL-JS/teacher.html` | `planning/` | not started |
| Plushies quiz | `WADB_Tutorials/tentacular-plushies-quiz-final.html` | `tutorials/data/the-tentacular-plushies-quiz/`, module `data`, series `practice` | done 2026-09-05; `NEXT_STEPS.md` step 7 item 4; rebuilt as an instant, ungraded self-check (`` ```sql-check `` blocks, new `check_*` functions in `sql_tools.py`) rather than a score, since `README.md` already promises the tutorials aren't graded; a worked solution at the foot satisfies section 8 decision 2's "shows its solutions" |
| Quick reference | `WADB_Tutorials/reference.html`, the plushies quiz's reference panel, `uu_reference.md` | `tutorials/reference/quick-reference/` | done 2026-09-04, in two halves (HTML/CSS, then SQL) rather than the three originally planned; two-column tables, no cards |
| Troubleshooting | `WADB_Tutorials/troubleshooting.html` | `tutorials/reference/troubleshooting/` | done 2026-09-04, condensed to the checks that matter; adds the Settings panel and search as dewstack-specific problems |
| Project ideas | `WADB_Tutorials/project-ideas.html`, `design-resources.html`, `examples/hello-world.html`, `first-page.html`, `resume-template.html` | `tutorials/reference/project-ideas/` | done 2026-09-04, re-keyed to the starter, Flexbox/Grid, a database of your own, and the full-stack page; three small examples bundled as downloads, the larger templates (accordion, tabbed, modal, cube, spiral, blog, landing page, portfolio, photo gallery) left for when the page that teaches each pattern is written |
| Design resources | `WADB_Tutorials/design-resources.html` | folded into `project-ideas.md`'s "Making any of them easy to read" | done 2026-09-04, condensed to three checks (typeface and size, line height, contrast) rather than kept as its own page |
| GitHub guides 1 to 7 | `WADB_Tutorials/github-guides/` | `tutorials/` | not started |
| Lessons 9 to 13 | `WADB_Tutorials/lessons/` | `tutorials/` | not started |
| Lessons 1 to 8 | `WADB_Tutorials/lessons/` | decision pending | not started |
| Templates and examples | `WADB_Tutorials/templates/`, `examples/` | decision pending | not started |
| Data Arc 2, page 1 of 6 (designing a table before you build it) | fresh, per `NEXT_STEPS.md` step 8's page-by-page breakdown | `tutorials/data/`, module `data`, new series `several-tables` | done 2026-09-05; no code cell, a planning page in `planning-a-site`'s idiom; the "your turn" has the reader choose the arc's own project topic on paper, to build on the following pages |
| Data Arc 2, pages 2 to 6 (loading a real dataset; joining two real tables; charting a query's result; exporting a query to a file; a form that writes a row) | Josh's own Database Methods project brief (a sample-solution notebook), which teaches this same dataset via `pd.read_csv` against OWID's grapher CSV API | `tutorials/data/`, series `several-tables`; `assets/python_tools.py` gains `load_csv()` and `download_csv()` | done 2026-09-06; the dataset is the World Inequality Database's "income share of the top 1%" series (CC BY, via Our World in Data), the same one Josh's own project brief uses, rather than the population/life-expectancy placeholder `NEXT_STEPS.md` question 8 had named — `load_csv()` is ported from dewlab's `tutorial_tools.load_csv()` (`pyodide.http.pyfetch`, since plain `pandas.read_csv(url)` fails inside Pyodide with a message that explains nothing); `download_csv()` is new, using `js.Blob`/`URL.createObjectURL` the way `sql-cell.js`'s own Download button does, verified live against a scratch page (real download, correct filename and contents). Page 3's "messy" join is a small hand-authored `country_regions` table with one deliberately mismatched country name, not a second live fetch — controllable and reliable where a second real dataset would not be. This sandbox's egress proxy blocks `ourworldindata.org` (as it already did for the Python/pandas engine row above), so every page's own `load_csv()` cell was verified to fail as a caught, rendered `ConnectionError` rather than a raw crash — not yet verified against a real, successful fetch, which needs an environment with a route to Our World in Data |
| Python/pandas cell engine (`` ```py cell=name `` blocks) | dewlab's `tutorial_tools.py`, ported in shape (its rendering and streaming logic only, none of its widget/check machinery) | `assets/python_tools.py`, `assets/sql-cell.js`, `build.py`, `assets/site.css` | done 2026-09-05; `NEXT_STEPS.md` step 8's engine note; built ahead of Data Arc 2 page 4 actually needing it, since page 2's real dataset is still blocked on Josh; verified live against a self-hosted Pyodide with `sqlite3`/`pandas`/`matplotlib` |

---

## 8. Open questions for Josh

1. **The SQL engine.** Decided 2026-09-04: **Pyodide with sqlite3**, as
   dewlab does. The data track, the full-stack track and the Python half
   share one engine, and a SQL table and a pandas table see each other.
   The cost is a load of about ten megabytes and a few seconds on first
   open, which dewlab already pays and mitigates by caching. The port in
   section 6 therefore takes dewlab's `pyodide-engine.js`, its worker,
   `tutorial_tools.py` (`run_query()`, `load_csv()`) and dewmini's SQL
   cell, not SQL.js. The playground and the quiz keep SQL.js until they
   are rewritten.
2. **Public solutions.** Decided 2026-09-04: solutions are linked at the
   bottom of the page they belong to, after the exercises, not hidden and
   not on a separate teacher page. The quiz is ungraded, so it shows its
   solutions after the student submits. Teaching notes move to
   `planning/`.
3. **Which of lessons 1 to 8 survive** beside `web`. Decided 2026-09-04:
   all eight are rewritten as short pages, so a student who wants the
   explanation before the exercise has it. Lessons 6 to 8 and guides 1 to
   5 cover the same ground; the rewrite makes one page per step, not two.
4. **Templates and examples.** Decided 2026-09-04: fold into the project
   ideas page. Each idea links the template that fits it; no separate
   templates page. `portfolio-starter` and `basic` go, since the starter
   covers them.
5. **Attribution.** Decided 2026-09-04: `deweydex` everywhere. One
   account name on every page and link; the front page's footer now links
   `github.com/deweydex` rather than a personal site.
6. **A Pages site for `web`**, so the README can show a live example.
7. **The name.** Decided 2026-09-03: **dewstack**, beside dewlab, dewmini
   and dewmark. Every page, link and document already says dewstack; the
   GitHub repository still needs renaming to match, and GitHub redirects
   the old name. The alternatives considered: `dewsite` for the combined
   site; `dewbase`, `dewsql`, `dewquery`, `dewtable` for a database-only
   home if the halves ever split; `dewpage` or `dewfolio` for the starter,
   though `web` stays, because a student's fork keeps the name and
   `username.github.io/web/` is the better address for a portfolio.
8. **The interim shelf.** Decided 2026-09-04: the site is not yet sent to
   anyone, so the copies are not a student-facing problem. They stay as
   the material to check coverage against, and the deliverable is new
   pages that meet every criterion in section 11. As each new page lands,
   the front page links to it and the copy it replaces can go.
9. **Build and home.** Decided 2026-09-04: dewstack, one course site,
   tutorials as markdown in dewlab's shape. Revised the same day when
   dewadaba#3 landed (section 6): the build is a short script that
   borrows dewlab's design, and the shell and settings panel are
   dewlab's files carried over. The Pyodide engine, its worker and
   `tutorial_tools.py` are copied in when data Arc 1 needs a SQL cell.
   The ledger notes the dewlab commit each copy was taken from so a later
   sync is possible.
10. **Page length.** Decided 2026-09-04: shorter than dewlab, 30 to 50
   sentences, one idea, one live example, one "your turn", ten to fifteen
   minutes. The thirteen WADB lessons become thirty or so pages, and that
   is the intended outcome, not a cost.
11. **The live element on a web page.** Decided 2026-09-04: not a cell. A
   web tutorial page carries a small site editor with files (an HTML pane,
   a CSS pane, a JavaScript pane) and a live preview, the way dewmini's
   Site tab already works (dewlab DECISIONS_LOG 7.121) and the way
   `WADB_Tutorials/js/code-playground.js` did on four lessons. Exercises
   are not on the page at all: they are in the student's own fork,
   published on their own GitHub Pages, in the `web` starter's model of
   change one thing, save, look. The data track keeps cells, and a cell
   there is a query. Section 13 has the component.
12. **Practice.** Decided 2026-09-04: one "your turn" on the page and a
   separate practice page beside it, solutions at the foot (question 2).
13. **More database content is coming** (Josh, 2026-09-04): to be added
   to the sources later today. The data track's plan in section 7 is
   revised once it is in.
14. **The outcomes map.** First pass done 2026-09-04, once Josh sent the
   Level 6 `Web Development 6N1277` descriptor and asked for a coverage
   plan rather than pages yet: `planning/LEVEL6_COVERAGE.md`. Eleven of
   seventeen outcomes already fit or adapt onto Arc 1, Arc 2 and the
   accessibility bar; three (multi-tier architecture, an installed CMS,
   FTP/domain hosting) don't fit a static, no-backend site at all and are
   flagged rather than silently dropped. Nothing is scheduled from it yet.
15. **The web track's order.** Josh asked for the three trajectories to
   be compared and a hybrid proposed rather than one picked. Section 14;
   superseded in part by 16.
16. **The design.** Decided 2026-09-04: three arcs and two starters, as
   section 15 lays out. `web` stays the door to web Arc 1; a second
   forkable starter, working name `site`, is the door to Arc 2, the
   project's shape. Every arc ends in something a student can show.
17. **The front page.** Decided 2026-09-04, evening: the README and the
   front page are two texts for two readers. The README is the map for
   people who read the repository. The front page is for the student, in
   dewlab's shape: an opening under two hundred words, two doors that open
   onto pages here, the search box, then the list by module, with unwritten
   modules shown as a heading and one line. `tutorials/front.md` holds the
   opening and the doors; `modules.yaml` holds the planned modules and
   the one-line notes. This revises the first paragraph of section 1.
18. **The two starters' real names.** Decided 2026-09-05, by Josh: `web`
   renamed to `portfolio_wad`; the second starter, working name `site` in
   section 15, is `project_wad`. `_wad` is Web Authoring and Development,
   the two Level 5/6 modules likely to use these starters, though only
   Web Authoring assesses against them today (see question 14). The pair
   names what each ends in, a portfolio and a project, rather than reusing
   near-synonyms (`web`, `site`) that would not tell the two apart on a
   student's own GitHub profile. Both are GitHub template repositories, at
   Josh's choice: this leaves the ordinary **Fork** button in place while
   adding **Use this template**, which gives a copy with no visible link
   back to the course repository and no shared history, suiting a
   portfolio a student may carry past the course under a plainer name.
   This revises section 1's table; the dated ledger entries in section 7
   and in `PAGE_BY_PAGE.md` keep the old name, since they record what was
   true at the time.

---

## 9. What the audit of `WADB_Tutorials` found, 2026-09-03

Kept here so the bar in section 3 has its reasons attached. Ten pages were
rendered at 1280 and 390 pixels and run through axe.

One defect is worth a line of its own because it is on the page students
meet first in stage 2. The playground's "Choose Your Learning Path" box
sits inside the header and inherits the header's white text, on a
near-white background, so it is illegible at every width. The fix is one
rule, `.learning-paths { color: #333; }`, made in the source and copied, or
made here when the SQL section moves.

- Seven of ten pages scroll sideways on a phone. The home page hero clips
  its heading. Every lesson page overflows on one bibliography link whose
  text is its full address. The reference page's cards have a fixed width.
- Six of forty-two pages have the search box. Twenty-one lack the theme
  switcher, including seven of thirteen lessons.
- The menu sets its expanded state but does not move focus into itself and
  does not close on Escape. There is no close control inside it.
- Lesson pages, the reference, troubleshooting, the quiz and the templates
  have no `main` landmark. The header's `nav` has no label.
- The green example links on the home page measure 2.5 to 1 against white.
  The troubleshooting page has sixty-eight contrast failures. The
  attribution links in every masthead differ from the surrounding text only
  by colour.
- A sliver of the skip link shows at the top left of every page.
- Lessons load their syntax highlighter from a CDN, so they lose it where
  the network is restricted.
- The quiz disables body scrolling and fixes three panels at set
  percentages. On a phone the task panel is one word wide.

Almost all of these are drift defects, which is the case for section 5.

---

## 10. The page structure, proposed 2026-09-03, late

Josh's steer, in his words: web authoring and databases exist as separate
tutorials, with combined projects and tutorials as a third option; two
"getting started" links, then tutorial links for each subject, then
combined full-stack tutorials. That replaces the strictly sequential three
stages in sections 1 and 4 with two parallel tracks and a third that joins
them. A student can start on either track, and the college's timetable
(web authoring in the autumn, databases from January) is one order among
several rather than the only one.

The front page and README would then have five parts, in this order:

1. **Getting started**, two doors side by side. *Start with a website*:
   fork `web`, the exercises, a published portfolio. *Start with data*: the
   SQL playground, a first query in a minute. Each door says what the
   student will have at the end of it, and neither assumes the other.
2. **Web authoring tutorials**: the lessons, the GitHub guides, the
   templates and examples, the reference and troubleshooting, in the order
   a student who has done the starter needs them (project-facing lessons
   11 to 13 first).
3. **Database tutorials**: the playground, the quiz, the notebook, then
   the five tutorials in section 7 as they are written (a table is a list
   of rows; asking questions of a table; two tables; designing before
   typing; a real dataset).
4. **Full stack: putting the two together**. Combined tutorials and
   projects: a page that shows rows from a database, a form that adds a
   row, a chart drawn from a query. This is the former stage 3, now a
   track of its own rather than a finish line. Nothing exists here yet.
5. **Projects and the exam**: what the college sets, and which track each
   project draws on.

The course bar on every copied page then carries: front page, Start with
a website, Start with data, Web tutorials, Database tutorials.

Applied on 2026-09-04: `README.md`, `index.html` and the course bar now follow this structure. `PAGE_BY_PAGE.md` is the page-by-page assessment (b). Sections 11 and 12 below are (c) and (d).

What the next session should do with this, in order: (a) settle the
structure with Josh and rewrite the README and `index.html` to it; (b) go
through every page on each of the three source sites and say, page by
page, what is good, what should change, and whether it belongs in track 2,
3 or 4, extending the ledger in section 7 with a row per page; (c) write
down the style considerations for the rewrites: one shell and one set of
reading settings across all tracks, the plain-language bar, the
accessibility bar in section 3, the SQL engine decision, and how the
`web` starter's deliberately student-changeable design sits beside the
fixed design of the tutorials; (d) begin the full-stack track with one
small worked example, because it is the part with nothing behind it.

---

## 11. Style considerations for the rewrites

Written 2026-09-04, after measuring every source page (`PAGE_BY_PAGE.md`). These are the decisions a rewrite should not have to make again.

**One shell.** Every rewritten page, on every track, uses the front page's stylesheet, its reading settings (`assets/settings.css`, `assets/settings.js`, the two self-hosted typefaces) and the course bar. Until the build step in section 6 exists, a rewritten page is one HTML file that links those three things by relative path; when `build.py` arrives, its shell template absorbs exactly those three, and the pages are converted to markdown without changing what a student sees. Nothing is styled twice.

**The shape of a page, from dewlab's style guide, section 3.** Open with the question: what is this for, where would somebody meet it. Give them something to try before anything is explained: an HTML and CSS pane with a live preview for the web track, a SQL editor for the data track. Then the explanation, connecting what they saw to the idea. Then their turn, with a hint that scaffolds rather than answers. Close by looking back. No "learning outcomes" preamble: the outcome is one sentence at the end, "what you can now do". No "why this matters" section: if the opening question does not say why, the page has the wrong opening. The bibliography becomes one line, "where this came from".

**Size.** One idea per page. Under 60 sentences of prose, a mean under 18 words, at most six second-level headings, and every sentence surviving its own trim test (section 3, check 2) rather than a fixed ceiling. Where a source lesson has twelve to eighteen headings, that is three or four pages, and `PAGE_BY_PAGE.md` says where the cuts fall. Splitting is the main work; trimming a sentence is the easy part.

**Discover first, name afterwards.** The source lessons define, then show. The rewrites show, then define, then say what the name is for. A student who has dragged a window narrower and watched a Flexbox row wrap has met `flex-wrap`; the word comes after, with the sentence that says it is the word to search for.

**Two bars, both mechanical.** The plain-language bar is the plain-language checks in dewlab's `CLAUDE.md`, run over every sentence before a commit; the sentence-length measure in `PAGE_BY_PAGE.md` is the script that catches most of it. The accessibility bar is section 3 of this plan: no serious axe violation, no sideways scroll at 390 pixels, a `main` landmark, a labelled `nav`, 4.5 to 1 contrast. Every page is rendered at 1200 and 390 pixels and looked at before it is pushed. Code blocks scroll inside themselves; nothing on a page has a fixed width in pixels.

**Live examples, one engine per track.** The web track needs an "edit and see" widget: two editors (HTML, CSS) and an iframe whose `srcdoc` is rebuilt on each change. dewmini in dewlab already has this as its Web cell (DECISIONS_LOG 7.116, 7.120); port the pattern, not Pyodide. The data track needs a SQL editor and a result table; the playground's `tutorial.js` is sixty lines that do this with SQL.js. The full-stack track uses both. The data engine is Pyodide's `sqlite3`, decided in section 8, question 1: dewlab's engine, worker and `tutorial_tools.py` are ported as they are, and a SQL cell on a page is dewmini's SQL cell. The playground's sixty lines of SQL.js stay only until the playground is rewritten.

**The starter's design is the student's.** `web` is navy and blue on purpose: it is the one design a student is meant to change, and exercise 13 changes it. The tutorials never restyle it, never show a re-skinned copy of it, and when they refer to the student's site they show it as it is, in an iframe or a screenshot. The tutorials' own look (the purple gradient, white cards) is fixed and is the course's, not the student's.

**Names and numbers.** The starter's exercise numbers are a contract; they never change. New tutorial pages are named with words, not numbers (`flexbox-first-steps`, not `11a`), as dewlab does, so that inserting a page never renumbers its neighbours. The old lesson numbers appear only in `PAGE_BY_PAGE.md`, as provenance.

**Practice apart from reading.** As in dewlab (style guide, section 6): the reading page ends with one "your turn"; the practice page beside it holds the rest of the problems with answers behind folds. For the data track, the playground's five exercises and the quiz's five tasks become practice pages. Whether solutions stay public is question 2.

**Terms.** A rewritten page introduces at most three new terms and lists them at its end with one-line meanings. The quick reference is assembled from those lists, by hand until the build step does it, the way dewlab's reference panel is assembled from glossary files.

**What stays out.** Practice exams and anything the college marks. Teaching notes go to `planning/`, not to a page a student can reach.

---

## 12. The first full-stack tutorial, outlined

Working title: *A page that shows rows from a table*. It is the smallest page that deserves the name full stack: HTML and CSS a student already understands, a database they already queried, and a dozen lines of Python and JavaScript joining them.

**Where it sits.** After the starter's exercise 12 (the student has a page with sections and navigation) and after the first two data tutorials (they have made a table and asked it questions). It uses the same Pyodide engine as every other page here, so nothing new is installed; the first open of the day takes a few seconds while the engine loads, as dewlab's pages do.

**What the student does, in order.**

1. Open a page whose first cell has already made a `products` table in `sqlite3`, the same three columns as the playground's exercises, and whose web cell holds a `<table>` element with a heading row and no body. Press Run. The rows appear. That is the whole idea, seen before it is explained: the page asked the database a question and drew the answer.
2. Read the dozen lines that did it: a Python function that runs the query and returns the rows, and the few lines of JavaScript in the web cell that call it (Pyodide exposes a Python function to the page) and make a `<tr>` for each row. Change the query to `WHERE price < 10`. The table changes.
3. Add a search box. Its value goes into the `WHERE`. Now the visitor asks the question.
4. Add a small form with two fields. Its submit runs an `INSERT`, then redraws the table. Now the visitor changes the data.
5. Look back at where the work went: the database starts again on reload, as the playground does. Two buttons, "download my database" and "load a database file", save and restore the `.db` file through the browser's file system, as dewmini's Files section already does, and the student now has a file that is theirs. This is the same "where your work is saved" question the front page raises, answered in code.

**What it names, at the end.** Three terms: query, result set, and the idea that a page is HTML plus data plus the code between them. That is what "full stack" means here, and the word is given last.

**What it deliberately leaves out.** Servers, accounts, anything that sends data anywhere. A second tutorial can put a chart beside the table using the marks example from the front page; a third can draw the page from an Our World in Data extract. The projects page lists these as combined projects once the first tutorial exists.

**Done when** the page passes both bars in section 11, a student who has done the prerequisites can complete steps 1 to 5 without help, and the front page's full-stack section links to it instead of saying "being written".

**Built 2026-09-06, steps 1 to 3, as its own new cell type rather than the site editor.** Before any of this could be built, a real gap in the outline above needed resolving: step 2's "Pyodide exposes a Python function to the page" assumes the web cell's JavaScript can reach this page's own Pyodide instance, but the site editor's preview (section 13) is deliberately sandboxed to `allow-scripts` with no `allow-same-origin`, precisely so a reader's script *cannot* reach anything else on the page — the exact channel this needs. Three ways through it were put to Josh: bridge the sandbox with a `postMessage` protocol (keeps the sandbox intact, but layers a second new concept — cross-document messaging — onto a page whose whole point is one concept, "a query becomes a row"); open a real hole in it by adding `allow-same-origin` (matches the outline's "a dozen lines" simplicity exactly, at the cost of reopening the escape-the-sandbox risk that comment in `site-editor.js` exists to prevent); or give this cell type no iframe at all, rendering straight into the page the way a SQL or Python cell's own output already does, since there is then no separate document to sandbox in the first place. Josh's call, for teaching reasons as much as architectural ones: the third, since every other example of "one cell reaching another" on this site (`read_sql()`, `download_csv()`) is already direct, and postMessage would be the one place a student meets indirection with no in-story reason for it.

`build.py`'s `extract_app_cells()`/`render_app_cell()` add a third cell kind alongside `sql cell=` and `py cell=`: consecutive ` ```html app=name `/` ```css app=name `/` ```js app=name ` blocks (grouped the same way `site=` blocks are) become one `.dl-app-cell`, HTML and CSS panes rendered straight into a preview `<div>` (CSS wrapped in `@scope` so a reader's selectors reach only that cell's own preview — the encapsulation an iframe would have given for free, kept without one), JavaScript run as a freshly created `<script>` element on every Run (an `innerHTML` assignment never executes a script tag, which is why one is built each time rather than reused) wrapped in an async IIFE so `root` (this cell's own preview element) and `dlQuery` reach the reader's code as plain parameters, nothing added to the page's global scope. `assets/sql_tools.py` gained `query_rows(db_name, sql, params=None)`, the Python half of the bridge — a plain list of dicts, not `run_sql()`'s HTML, since the reader's own JavaScript decides what the page does with a result; `assets/sql-cell.js`'s `boot()` exposes it as `window.dlQuery` only when the page actually has an app cell, the same "no page pays for what it doesn't use" rule the package-list gathering already follows.

`params` was added to `query_rows()`/`dlQuery()` beyond what the outline's step 3 asked for, once step 3 was actually being written: a search box's typed text going straight into the SQL text (string concatenation) is a real anti-pattern worth not teaching even once, and a placeholder (`?`, filled in separately) is the correct, real-world fix — and a natural place to name it, since the page is already teaching "query" and "result set" at this exact moment. The tutorial (`tutorials/full-stack/a-page-that-reads-from-a-database/`) now names four terms at the end, not three: query, result set, full stack, and placeholder.

Steps 1 to 3 shipped as this one page. Step 4 (a form's `INSERT`) is deliberately the next page, not folded into this one — Data Arc 2's own `a-form-that-writes-a-row` (`NEXT_STEPS.md`) already promised that wiring as "a full-stack page still being written," so building it as page two closes that promise rather than pre-empting it here. Step 5 (Download/Load buttons for the whole database file) is superseded before it was ever built the same way Data Arc 1's own Download/Load-only design was: `persist` (a SQL cell's own localStorage auto-save) is the pattern this site actually converged on for "where your work is saved," so page two or a later page should reach for that first, Download/Load only as the secondary "take a copy out of the browser" action it already is elsewhere.

An app cell's Reset does *not* call `sql_tools.reset()` the way a SQL or Python cell's does — caught live, not just reasoned through: an app cell owns no connection or namespace of its own the way those cells do, only ever reading one through whatever name its own `dlQuery()` calls happen to pass, often a SQL cell's, elsewhere on the same page, that other cells still depend on. Verified live (a real self-hosted Pyodide, Playwright): the read cell, edited to `WHERE price < 10` and rerun, showed three rows becoming two correctly; the search cell's placeholder-bound `LIKE` query matched "Tote bag" on "bag" and nothing else; resetting the read cell cleared only its own preview, confirmed by the search cell still returning all five rows afterward; a bad query (`not_a_real_table`) and a bad JavaScript reference (`.querySelector` on nothing) both rendered in the cell's own error box with zero page or console errors, rather than crashing. `python3 -m pytest -q`: 169 tests (10 new in `tests/test_build.py`'s `TestAppCell`, 6 new in `tests/test_sql_tools.py`'s `TestQueryRows`, 4 new e2e in `tests/e2e/test_full_stack_cell.py`).

---

## 13. The site editor for web pages

Decided in section 8, question 11. What a web authoring tutorial page needs is not a cell but a small site: files a student can see all at once, and the page those files make, updating as they type. Three things already do most of this and are the sources for the component.

**dewmini's Site tab** (dewlab, `compose/dewmini.js`, `openSiteFile()` and the `SITE` view; DECISIONS_LOG 7.121). An `.html` file opens with its same-name `.css` and `.js` beside it: three editors on one side, a sandboxed iframe (`sandbox="allow-scripts"`, no same-origin) on the other, redrawn on every keystroke. The editors are CodeMirror, the same build dewlab vendors. It is the most complete of the three and the one to port; it already runs against a mounted folder, which the tutorial page does not need.

**WADB's code playground** (`tutorials/js/code-playground.js`, used on lessons 01, 09, 10 and 13). An HTML pane and a CSS pane seeded from `data-html` and `data-css` attributes, a preview, a reset, and a `data-solution-html` pair that shows a solution. The seeding-from-attributes and the solution pair are worth keeping; the rest the Site tab does better.

**The playground's interactive demo** (`databases/playground/index.html`, "Interactive Demo"): a CSS textarea applied live to a sample block. The smallest possible version, and a reminder that a demo can be one pane when the idea is one property.

**What the component is.** A block a tutorial's markdown can place, seeded with an HTML, a CSS and, when the page needs it, a JavaScript file, showing the three as tabs or panes beside a live preview at a width the reader can drag (so responsive pages can be tried). Buttons: reset to the tutorial's version, and "download these files", so a student can drop them into their fork. No saving on the page: the student's fork is where work is kept, and the page says so. In the build, a fenced block with a tag (as `python exec` marks a cell) marks a site file, and consecutive site-file blocks with matching base names form one editor.

**Where exercises go instead.** Every web tutorial ends with one "your turn" that is done in the student's fork: open this file, change this, save, refresh, look. The practice page beside it lists more of the same. That is the `web` starter's model, and it is why the tutorials never need to save a student's HTML.

**Done when** one rewritten page (lesson 11's first half, Flexbox) ships with the component, renders at both widths, passes both bars, and a student can drag the preview narrower and watch a row wrap.

**Added 2026-09-06: a console, and Run for JavaScript.** The component gained a console under the preview and a Run button on the JavaScript pane; HTML and CSS stay live, JavaScript runs when asked. `planning/CONSOLE_AND_WORKSPACE.md` is the design, and it also plans the dewstack workspace, a page of the site's own where the same component keeps several named sites in the browser.

---

## 14. The web track's order: three trajectories and a hybrid

Three orders exist for the same material. They differ in where GitHub comes, where CSS starts, and whether layout is taught at all.

**The starter's exercises** (`deweydex/web`, 25 exercises). Fork and publish first (1, 2), so the site is live before anything is learned. Then the home page's HTML, top to bottom: title, heading, a paragraph, emphasis, a section, an image, a link, a contact section, navigation (3 to 12). Then the stylesheet: variables and colour, backgrounds, the box, borders, text, classes (13 to 18). Then layout: the container, a sticky header, the footer (19 to 21). Then states and polish: hover, focus, a media query, a favicon (22 to 25). The trajectory is *one real page, top to bottom, then its stylesheet, top to bottom*. It never teaches Flexbox or Grid, though its stylesheet uses Flexbox in five places and exercise 21 leans on it; the project brief requires both.

**`CONCEPTS.md`** (ten sections). The box; how the browser builds a page; semantic HTML; selectors; specificity; units; Flexbox; responsive design; variables; transitions. The trajectory is *from the smallest idea to the largest, concept before use*. It puts variables ninth, though the starter uses them at exercise 13, and Flexbox seventh, though the starter never asks for it.

**WADB's lessons** (thirteen). HTML basics; semantics; CSS basics; layout (box, display, Flexbox, positioning); responsive design; then GitHub setup, workflow and Pages (6 to 8); then images and links (9, 10); then the three project lessons. The trajectory is *a textbook's*: all of HTML, then all of CSS, then publishing in the middle, then two topics that arrived later. Publishing in the middle is its weakest choice; the starter's first-minute publish is better, and there are no returning students to keep the old order for.

**The hybrid.** A getting-started strand first, before either door, because the starter relies on a GitHub account, an editor and a fork, and today it says "clone it" without saying how (Josh, 2026-09-04: "an overview of everything with steps to get up and running before the practice"). Then the starter's spine, because each tutorial page should be "the explanation behind the exercise you just did", with concept pages placed where the starter first touches the concept, and WADB's project material as a fourth strand after exercise 25. Thirty-six pages, in four strands a student can also read across. The front page gains a "Before you begin" part above the two doors that says the same in five sentences and links strand A.

| # | Page (working title) | Starter exercise | Source |
|---|---|---|---|
| A0 | How the pieces fit: editor, GitHub, Pages, browser, this site | before 1 | new; one picture and a paragraph |
| A1 | A GitHub account | before 1 | guide 01, lesson 06 |
| A2 | An editor: VS Code, or the editor inside GitHub | before 1 | new; the course site's "Programs to Install" page is empty today |
| A3 | Your copy of the starter: fork, then clone, download, or edit in the browser | 1 | guide 02, guide 06 (fork section); the starter says "clone" without saying how |
| A4 | Publish it: GitHub Pages, and why your address looks like that | 2 | guide 05, lesson 08 |
| A5 | The two loops: save and refresh on your computer; commit and wait on GitHub | 3 | lesson 01 (first third), guide 03, lesson 07 |
| A6 | Seeing under the page: the inspector | 3 onward | guide 07 (first third) |
| B1 | A page is files; save, refresh | 3 | lesson 01 (first third) |
| B2 | The skeleton: head, body, title | 3, 4 | lesson 01 |
| B3 | Headings, paragraphs, emphasis | 4 to 6 | lesson 01 |
| B4 | Sections, and the tags that mean something | 7, 8 | lesson 02, CONCEPTS semantic |
| B5 | Images, paths and alt text | 9 | lesson 09 |
| B6 | Three kinds of link | 10, 11 | lesson 10 |
| B7 | Navigation | 12 | lesson 10; a pointer to D1, because the starter's nav is a flex row |
| B8 | How the browser builds a page | after 12 | CONCEPTS DOM (optional depth) |
| C1 | A rule, and where it lives | 13 | lesson 03 |
| C2 | Variables and colour | 13, 14 | CONCEPTS variables, lesson 12 |
| C3 | The box | 15, 16 | CONCEPTS box, lesson 04 |
| C4 | Text and units | 17 | CONCEPTS units, lesson 03 |
| C5 | Selectors and classes | 18 | CONCEPTS selectors, lesson 03 |
| C6 | When rules conflict | 18 | CONCEPTS specificity (optional depth) |
| C7 | The container: width and centring | 19 | lesson 04 |
| C8 | Position, and the sticky header | 20, 21 | lesson 04 |
| C9 | States: hover and focus | 22, 23 | lesson 10 |
| C10 | Transitions | 22 | CONCEPTS transitions, lesson 13 |
| C11 | Media queries | 24 | CONCEPTS responsive, lesson 05 |
| C12 | Flexible images | 24 | lessons 05, 09 |
| D1 | Flexbox first steps | after 25 | CONCEPTS Flexbox, lesson 04 |
| D2 | Flexbox properties | project | lesson 11 (first half) |
| D3 | Grid areas and minmax | project | lesson 11 (second half) |
| D4 | A navigation that works on a phone | project | lessons 05, 10 |
| D5 | Components and a theme switch | project | lesson 12 |
| D6 | Keyframes and transforms | project | lesson 13 |
| D7 | Branches and pull requests | team project | guide 04, lesson 07 |
| D8 | Working with others on GitHub | team project | guide 06 |
| E | Troubleshooting; quick reference; project ideas with the templates folded in | any | resource pages |

**Where the starter diverges from this track, and the two warnings it needs.** First, the starter reaches the end of exercise 25 with a site that uses Flexbox without ever having named it, and the project brief requires Flexbox and Grid; the starter's closing section (plan, section 5, step 3) should say so and point at D1 to D3. Second, exercise 12's navigation is a flex row, so a student who asks "why does this line up" at B7 needs a pointer forward to D1 rather than an answer on the spot; B7 carries that pointer. Everywhere else the hybrid follows the starter exactly, so a student reading the tutorials in order and doing the exercises in order never meets a page that assumes an exercise they have not done.

**What the hybrid gives up.** CONCEPTS's small-to-large order has a logic of its own, and a student who likes theory first loses it; B8 and C6 are kept as optional depth so that reader has somewhere to go. WADB's all-HTML-then-all-CSS order is gone, and with it the sense that HTML is finished before CSS begins, which the starter's exercises 8 and 11 (adding sections after the stylesheet is in use) already contradict.

Thirty-six pages plus three reference pages, at 30 to 50 sentences each, is the "thirty-something shorter tutorials" outcome.

Josh's reply to this section (2026-09-04): the past structure of the source pages need not be kept; think it through from scratch, and say where an existing thing is upgraded and where something starts fresh. Section 15 does that, and where it differs from the hybrid above, section 15 wins. The table above stays as the inventory of where each source page's material goes. The order of writing them stays as `PAGE_BY_PAGE.md` section 5 has it: reference pages first, then D2 and D3, then the data track, then A1 to A3, then B5 to B7, then the rest.

---

## 15. From scratch: three arcs, two starters, and what to upgrade or begin fresh

If nothing existed and the brief were "adults, first time, nothing installed, two modules assessed by a web project, a database project and a practical exam", this is the course.

### The spine is a thing the student builds, not a syllabus

The starter's one insight is worth the whole design: the student's own artefact grows, and the teaching hangs off its growth. Fork, publish, change one thing, look. Generalised, every track is an artefact that grows in arcs, and each arc ends in something the student can show. The tutorial pages are not a parallel syllabus to read through; each is the explanation behind one step of the artefact, thirty to fifty sentences, with something to try in place and a "your turn" done on the artefact itself.

**The web track, three arcs.**

*Arc 1, your first site.* The `web` starter as it is: a three-page portfolio, twenty-five exercises, live from exercise 2. Beside it, one short concept page per idea the exercises touch, in the order they touch it: the page as files, the skeleton, headings and emphasis, sections and meaning, images and paths, links, navigation, then a rule, variables and colour, the box, text and units, selectors, the container, position, states, transitions, media queries. Sixteen pages. Ends with a published portfolio.

*Arc 2, a site with several pages.* This is the assessed project's shape: five pages, a shared navigation, Flexbox and Grid layouts, responsive, images, a form, and the planning and documentation the brief marks. The brief says the topic must differ from the portfolio, so this arc starts from a second starter, a five-page skeleton with `planning.md`, `readme.md` and `maintenance.md` templates inside it, forked the same way. Beside it: planning a site (audience, site map, wireframes); several pages and one navigation; a Flexbox row of cards; a Grid gallery; a navigation that works on a phone; a form; an images folder and file size; documenting what you built. Eight pages. Ends with the project. The live brief and the four template files it ships with are now in `sources/teaching-materials/Web Authoring Briefs/`; `PAGE_BY_PAGE.md` section 6 says what to adapt from them.

*Arc 3, a site with data.* The full-stack track: the site shows the student's database. Three pages, section 12. Ends with a page that reads, searches and adds rows.

**The data track, two arcs, meeting the third.**

*Arc 1, your first table.* The student's own database, on a topic they choose, kept as a file they download and load (dewmini's Files). Four pages: a table is a list of rows; asking questions of a table; changing what is in it; a second table and a join. The dinosaurs are the worked example on every page; the "your turn" is the student's own table. Cells are queries.

*Arc 2, a database with several tables.* The database project's shape, revised by `NEXT_STEPS.md` step 8's page-by-page breakdown (2026-09-05): designing a table before you build it (what goes in which table, keys, one-to-many); loading a real dataset, from Our World in Data; joining two real tables; charting a query's result, where pandas and matplotlib arrive; exporting a query to a file; a form that writes a row, linked to the web track's own form page rather than rebuilt here. Six pages. Ends with the project's database and the queries the practical exam asks for.

**Getting started, before both tracks.** Six pages (section 14, A0 to A6): how the pieces fit; an account; an editor, VS Code installed with GitHub's own editor as the fallback (decided 2026-09-04); your copy of the starter; publishing it and the address; the two loops; the inspector. The data track needs only the first and the last.

**Reference, beside everything.** Troubleshooting as problem-shaped cards; a quick reference in two halves, HTML and CSS, and SQL; project ideas with the templates folded in. Three pages.

Getting started 6, web 16 + 8 + 3, data 4 + 6, reference 3: forty-six short pages. More than thirty-six, and each one shorter, because Arc 2 of both tracks is material none of the sources has and the brief marks.

### Upgrade or fresh, piece by piece

| Piece | Verdict | Why |
|---|---|---|
| `web`, the starter | **Upgrade, lightly.** web#1's pass, the assessment file gap, the closing section. Keep every exercise number. | The shape is the design. Its one gap, Flexbox used without being named, is closed by the concept pages, not by more exercises. |
| A second starter for the project | **Fresh.** A five-page skeleton with the brief's file list, planning and README templates inside, fork-able. Working name `site`. | The brief wants a different topic from the portfolio and marks planning; nothing existing gives a student that starting point. |
| `CONCEPTS.md` | **Upgrade into the Arc 1 concept pages.** Its ten sections, in the starter's order rather than its own, each with a site editor. | Already the right register and length; only the order and the live element are missing. |
| WADB lessons 1 to 10 | **Quarry, do not upgrade.** Take the file-and-refresh insight, the paths section, alt text, link states, the box model prose; leave the shape. | Their shape (outcomes, why-it-matters, definitions, then examples) is the reverse of the one we want, and reversing a page is more work than writing it from the concept pages. |
| WADB lessons 11 to 13 | **Quarry the examples, write Arc 2 fresh.** The holy-grail, dashboard, card and gallery examples become the live editors' seeds. | The examples are good and project-shaped; the prose around them is a reference manual. |
| WADB GitHub guides | **Upgrade into getting started.** Shorten by half, keep the steps, merge each with its lesson twin. | Procedural pages survive being shortened; nothing about them needs rethinking. |
| Troubleshooting, quick reference, project ideas | **Upgrade.** Keep the structure, rewrite the prose, add the SQL half and the dewstack-specific problems. | The structures are right; the sentences and the phone layout are wrong. |
| WADB templates and examples | **Fold** into project ideas (decided). | |
| The playground | **Quarry and rebuild.** The six command cards and five exercises seed data Arc 1; the page is rebuilt in the shell with Pyodide. | The engine changes, the parts 1 and 2 duplicate the web track, and the page is one long scroll. |
| The quiz | **Rebuild, keep the tasks.** One column in the shell, the same five tasks, its reference panel into the quick reference, solutions after submission. | The three-panel layout is unusable on a phone and "check my work" was reported broken. |
| The dinosaur notebook | **Keep the narrative, rebuild as pages.** Its create, insert, select, second table, join sequence is data Arc 1's order. | It needs Jupyter and a pip install; the course has removed installs. |
| Data Arc 2 and the full-stack arc | **Fresh.** | Nothing in the sources covers design, a real dataset, or a page that shows data. The database content Josh is adding today may change this row. |
| The site editor | **Port dewmini's Site tab** (section 13). | It exists, is sandboxed, and updates on every keystroke. |
| The shell and build | **Done**, dewadaba#3: dewlab's shell and panel as files, a short build of its own (section 6). | The Pyodide runtime is copied in when data Arc 1 needs it. |
| Reading settings, course bar | **Done.** | |

### What this changes on the front page

Nothing in the five parts; the parts stay. Inside "Web authoring tutorials" and "Database tutorials", pages are listed by arc rather than by source, and each arc names what a student has at its end. The second starter joins the "Begin" part when it exists, as the door to Arc 2.

### The order of writing, revised

1. The three reference pages (every track, fail on a phone today).
2. Getting started A0 to A6, because the starter depends on it and the term has begun.
3. Web Arc 1's sixteen concept pages, in the starter's order, each a small pull request with its site editor.
4. The second starter and web Arc 2, before the project brief is issued in January.
5. Data Arc 1 as soon as the build step and Pyodide are in place; the playground and quiz rebuilt as part of it.
6. Data Arc 2, then the full-stack arc.
