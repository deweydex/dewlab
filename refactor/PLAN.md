# The plan

## 1. What is decided

These came out of the planning conversation on 2026-09-14 and are fixed for
this piece of work. Anything not listed here is open.

**A tutorial carries only what is its own.** Its id, which is its folder
name; its title; its version and status; what it covers; what packages and
datasets it needs; optionally what it assumes. It does not say which module
or series it is in. `module:`, `module_title:`, `series:` and `slug:` leave
the frontmatter. `year:` stays, for now, because dewnote recognises a dewlab
file by it.

**Placement lives in `courses/`.** One YAML file per course (what the site
calls a module today), listing its series as headings and each series'
tutorials as an ordered list of ids. One `courses/index.yaml` gives the order
courses appear in. There is no `series/` folder: a series is a heading in a
course file, and a series wanted in two courses is written in both.

**Every link is generated.** Previous and next, the where-you-are tree, the
course page, the contents page, downloads, "also part of" — from the course
files, at build. None of it is stored.

**Ids are site-wide and never change.** `tutorials/` is flat; the filesystem
refuses a second folder with the same name, and the build refuses it again
with a message that names the other tutorial and its course. Exactly one id
collides today: `first-steps` in the integrated module and in Computational
Methods. The Computational Methods one is renamed to `first-steps-cm`. Its
old address redirects; its saved work is carried over.

**Titles may repeat, but are never shown bare and are flagged.** Two courses
may each have a "Joins". The build warns when titles repeat (naming both and
their courses); every list on the site shows a title with its course beneath
it, as it already does; the editor says "taken" while an author types. Two
tutorials that cover the same outcomes are reported at build whatever they
are called.

**One page per tutorial, at one address.** Not one per course. The page
draws its chrome — tree, previous and next, the reference panel's
accumulation — for the course the reader is following, which the front-page
card sets and the browser remembers, defaulting to the first course that
lists the tutorial. The tree's module rung becomes the switch on a tutorial
that sits in more than one course. The build still writes the default
course's chrome into the HTML so the page is right before any script runs.

**Addresses.** `tutorials/<id>.html` for a tutorial, `tutorials/<id>-practice.html`
for its practice page, `tutorials/<id>/v<version>.html` for an earlier
release, `courses/<course>.html` for a course page. Every address the site
has today gets a redirect stub, generated from `courses/redirects.yaml`.

**Practice pages.** A practice page stays `<id>-practice.md` beside its
tutorial and keeps `practice_for:`; a mixed page keeps `practice_across:` and
is listed in the course file under `mixed:`. (The "practice.md by convention"
variant is a possible later simplification; it is not part of this change,
because it renames files for no gain in the model.)

**What a reader sees.** On the courses we have, the same pages and the same
trees; every old address still opens the same page. New: a tutorial in two
courses says so under its heading, and its tree can be switched between
them.

## 2. The target shape

```
tutorials/
  first-steps/
    first-steps.md              title, year, version, covers …
    first-steps-practice.md     title, year, version, practice_for
    first-steps.glossary.yaml
    v2026.08.23.1.md
  first-steps-cm/               ← renamed from computational-methods/first-steps
  storing-and-computing/
  …                             121 folders, flat
courses/
  index.yaml                    order: [maths-and-programming, computational-methods, …]
  maths-and-programming.yaml    title, code, status, card, description, contents, mixed
  programming-design-principles.yaml
  computational-methods.yaml
  fundamentals-of-oop.yaml
  database-methods.yaml
  web-authoring.yaml
  redirects.yaml                old path → new path, one line each
```

A course file:

```yaml
title: Programming and Design Principles
code: 5N2927 · QQI Level 5
status: beta
card: |
  This is the programming half of the integrated course, on its own. It runs
  from a first cell to reusable tools, then a project built in a team.
description: |
  This module is Programming and Design Principles (5N2927) on its own …
contents:
  - title: Programming Foundations
    tutorials: [first-steps, storing-and-computing, how-we-got-here, …]
  - title: Working in a Team
    tutorials: [critique-and-reflection, the-team-project]
mixed: [mixed-problems-programming]
```

A tutorial's frontmatter after migration:

```yaml
---
title: "First Steps"
year: "2026-2027"
version: 2026.08.23.2
covers:
  what-is-an-algorithm:
    covers: [MIT-6.1, PDP-LO2]
---
```

## 3. The steps, in order

Each step is its own commit on one branch, and each has a check that says
it is done. Steps 1–3 can land together as one pull request if the day
allows; 4–7 can follow in the same PR or the next. Step 8 is a different
repository. Step 9 deletes this folder.

### Step 0 — branch and freeze

- Branch `claude/courses` from `main`.
- No tutorial content changes are merged to `main` while the branch is open
  (a content PR would have to be re-migrated). Say so in the PR title.

Done when: the branch exists and the PR is open as a draft.

### Step 1 — migrate the files and swap the documents (this folder's scripts)

```bash
python3 refactor/apply_docs.py --check                      # every old passage present
python3 refactor/migrate_tutorials.py                       # dry run: report only
python3 refactor/migrate_tutorials.py --rename computational-methods/first-steps=first-steps-cm --apply
python3 refactor/apply_docs.py --apply                      # the documents, same commit
```

The documents are swapped in the same commit as the files, so the tree is
never half-described (`DOCS.md` §3 has the exact order).

What it does, in order:

1. Reads every `tutorials/<module>/<slug>/*.md`, `*.order.yaml`,
   `series.yaml`, `modules.yaml`, and `MODULE_INFO` from `build.py`.
2. Finds id collisions across modules and refuses to apply until each has a
   rename (`--rename computational-methods/first-steps=first-steps-cm` is the
   one needed today; the script proposes it).
3. Rewrites every tutorial, practice and release file's frontmatter: drops
   `module`, `module_title`, `series`, `slug`; keeps everything else in the
   same order.
4. Moves each `tutorials/<module>/<slug>/` folder to `tutorials/<slug>/`
   (`git mv`, so history follows), applying the renames; renames the files
   inside a renamed folder to match.
5. Writes `courses/<module>.yaml` from the module's order files (in
   `series.yaml` order, then the unlisted ones), its `MODULE_INFO` entry,
   and the card text from `pages/home.md`; `courses/index.yaml` from
   `modules.yaml`; `courses/redirects.yaml` with one line per old address
   (tutorial, practice and release pages, and module pages).
6. Removes the borrowed-form order files of `programming-design-principles`
   (their content is now that course's file) and the empty module folders.
7. Fixes `tutorial:` links inside tutorials that named a renamed slug.

Done when: the dry run reports 121 tutorials, 1 rename, 6 courses, and
`--apply` leaves `git status` showing only moves, frontmatter diffs, and the
new `courses/` folder. `build.py` will not build yet — that is step 2.

### Step 2 — the build reads courses

`build.py`, in this order (see `TOUCHPOINTS.md` for line-level detail):

1. `Tutorial`: `module` and `series` stop being frontmatter; `id` is the
   folder name; `out_path` becomes `tutorials/<id>.html` (releases under
   `tutorials/<id>/`). A `placements` attribute — `[(course, series_title,
   position), …]` — is filled from the course files after loading.
2. `load_all` walks `tutorials/*/` (flat) and refuses duplicate ids with the
   message from §1.
3. `courses()` replaces `order_files()`, `series_titles()`,
   `module_order()`, `module_series_order()`, `check_series_order()` and
   `MODULE_INFO`: reads `courses/*.yaml` and `courses/index.yaml`, validates
   every id, and refuses a tutorial on no course only with a note (it still
   builds, at its address, with no tree below "All tutorials").
4. `series_of()` becomes `groups` keyed by `(course, series_title)`, built
   from the course files; the borrowed-entry code is deleted.
5. `nav_for`, `crumb_trail_html`, `practice_link`, `render_module_body`,
   `write_module_page` (→ `write_course_page`), `render_tutorials_list`,
   `write_series_zip`, `write_module_zip`, `write_search_index`,
   `write_tree_page`, `write_topics_page`, `site_footer`,
   `report_doors_panel_html`, `standalone_html`: take a course (the
   tutorial's default course, its first placement) instead of
   `tutorial.module`/`tutorial.series`.
6. Every tutorial page also carries `data-courses` and the page's manifest
   gains `id` and `courses: [...]`; the build writes `assets/routes.json`
   (every course's contents, by id) for step 3.
7. "Also part of …" line under the heading when a tutorial has more than
   one placement.
8. Redirect stubs from `courses/redirects.yaml`: a page at each old address
   with `<meta http-equiv="refresh">` and a link, written by a new
   `write_redirects()`.
9. The front-page cards come from the course files: a new generated block,
   `[[course-cards]]`, which `apply_docs.py` puts in `pages/home.md` in place
   of the six hand-written course-card fences; `read_page()` already handles
   `[[search-box]]` the same way. Pages need no other change — `DOCS.md` §1.
10. Warnings, not errors: duplicate titles (both files, both courses);
    coverage overlap (two tutorials sharing three or more outcomes).
11. `dev/curriculum_map.py`, `dev/draw_topic_graph.py`,
    `dev/from_notebook.py` — the three dev scripts that build URLs or paths
    from a module.
12. `refactor/check.py` moves to the repository root as `check.py`, and
    `refactor/docs/CHECK_YOUR_WORK.md` to `docs/`; `docs/WRITING_TUTORIALS.md`
    and `CONTRIBUTING.md` each gain one line pointing at it (`TESTS.md` §4).

Done when: `python3 build.py --clean` writes the site; `site/tutorials/`
has one page per id; every old address in `courses/redirects.yaml` exists
as a stub; `python3 -m pytest tests --ignore=tests/e2e` is green after
step 5.

### Step 3 — the runtime follows the course

`assets/tutorial-runtime.js`:

1. Storage keys: every `dewlab:<kind>:<module>:<slug>` key becomes
   `dewlab:<kind>:<id>`. On first load, `migrateStorage()`
   (`storage_migration.js` in this folder) scans `localStorage` for keys
   whose suffix is `:<module>:<slug>` for this page's old address (both are
   in the manifest as `legacy`) and renames them; the same for the one
   renamed id. Progress badges on lists (`link.dataset.module` at 4026)
   read the new key.
2. `manifest.module` disappears; export filenames (`from` at 2526, 2665)
   use `manifest.id`.
3. `currentCourse()`: `dewlab:course` in localStorage, set by the front-page
   cards and the course page links (`?course=` on arrival, then remembered),
   else the first entry of `manifest.courses`.
4. `drawCourseChrome(course)`: from `assets/routes.json`, rewrite the tree's
   course rung, series rung and siblings, the bottom previous/next, and the
   "also part of" line; the course rung becomes a `<select>`-like chooser
   when `manifest.courses.length > 1`. The HTML the build wrote is the
   default course's, so nothing moves unless the remembered course differs.
5. Reference panel accumulation: today built into the page for the home
   series chain. Keep that as the default; on a course switch, re-fetch the
   accumulation for the chosen course from a per-course JSON the build
   writes (`assets/reference/<course>/<id>.json`). This is the one part of
   step 3 that can be left for a later day without breaking anything: until
   it is done, the panel accumulates the default course's chain.
6. Rebuild `vendor-src` (`npm run build`) so `standalone.bundle.js` matches.

Done when: a saved answer on `computational-methods/first-steps` before the
change is still there on `first-steps-cm` after it; opening First Steps from
the PDP card shows the PDP tree and previous/next; the e2e files in
`TOUCHPOINTS.md` §3 pass.

### Step 4 — the authoring editor here

`assets/editor.js` — see `EDITOR.md` §1. In short: paths become
`tutorials/<id>/`, the new-tutorial template loses four fields, the series
panel reads and writes course files instead of order files, and "unlisted"
means "on no course".

Done when: `editor.html` opens the repository, lists every tutorial under
its courses, can move one between series in a course file, and can create a
tutorial that then appears on a chosen course — checked by hand against a
fork, since the editor talks to GitHub.

### Step 5 — tests

`TESTS.md` is this step. In short: `tests/test_build.py` is re-cut into
`tests/build/`, one file per object, with three fixture helpers that speak
the new layout; the browser fixture gains a course file; the tests that
asserted on module folders, order files, `module_title` or the borrowed
form are rewritten or deleted (`TESTS.md` §2.3 says which and why); the
charter in `TESTS.md` §3 names the new tests, each against a foreseen
mistake; `tests/build/test_check.py` proves `check.py`; and CI gains a
browser job for the prose-only e2e files.

Done when: the unit suite is green, every row of the charter has its test,
and the e2e files that passed before the branch pass again (the two
failures already present on `main` in this sandbox excepted).

### Step 6 — documents

Already done by step 1's `apply_docs.py`, which carries every edit in
`DOCS.md` §2 (the writing guide, `ARCHITECTURE.md`, `CLAUDE.md`, the runtime
explainer, the reference-panel spec, the three skills, and the course cards
in `pages/home.md`). What remains by hand: `DECISIONS_LOG.md` 7.172,
`planning/PLAIN_LANGUAGE_PASS.md` for "Also part of …", and regenerating
`planning/CURRICULUM_MAP.md` with `dev/curriculum_map.py` once step 2 builds.

Done when: `dev/check_doc_links.py` passes and `grep -rn "tutorials/<module>"
docs ARCHITECTURE.md CLAUDE.md .claude` finds nothing.

### Step 7 — deploy and redirects check

After the merge to `main`, open five old addresses on the published site
(a tutorial, a practice page, a release, a module page, and the renamed
Computational Methods First Steps) and confirm each lands on its new page.

### Step 8 — dewnote (separate repository, separate pull request)

See `EDITOR.md` §2. dewnote reads dewlab's layout in seven source files
and describes it in `planning/DIALECTS.md` §1. None of it blocks steps 1–7;
dewnote simply cannot open the new layout until it is done, and its
full-corpus round-trip test (which reads `../dewlab`) will fail on the
missing fields.

### Step 9 — delete this folder

In the same PR as step 7's confirmation, or the next: `git rm -r refactor/`,
with `DECISIONS_LOG.md` 7.172 pointing at the PR that carried the work.

## 4. Order of magnitude

From the inventory: about 90 placement reads in `build.py`, 6 in the
runtime, 25 in `editor.js`, 3 dev scripts, ~200 fixture and assertion lines
across the tests, 2 documents that describe the layout, and 7 source files
plus one document in dewnote. Steps 1–3 are a long day; 4–6 are another;
dewnote is a third. "Today" is steps 0–3 with the PR open and the tests
red at the end of it, or steps 0–2 with them green.
