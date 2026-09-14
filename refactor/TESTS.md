# Tests

Two things here. First, a tool for one person adding one thing —
`check.py` and its page `docs/CHECK_YOUR_WORK.md`, both in this folder until
step 2 moves them. Second, what happens to the test suite: not "add tests
for the new thing" but a re-cut of the suite around the objects the new
architecture has, with every test that survives, changes or arrives
justified by the mistake it catches.

## 1. What the suite is today

- `tests/test_build.py`: 407 tests in 53 classes, one 4,300-line file,
  organised by the order features were added. About 200 of its lines
  write `tutorials/<module>/<slug>/` fixtures through three helpers
  (`write`, `tutorial_path`, `set_order`).
- Five smaller unit files for the tools (`tutorial_tools`, `from_notebook`,
  `curriculum_map`, `pair_results`, `report_patterns`): 198 tests, none
  about layout except `test_curriculum_map` (URLs from module and slug).
- `tests/e2e/`: 28 browser files, about 470 tests. One fixture site
  (`tests/e2e/fixture/`, copied into a temporary `tutorials/<module>/`).
  `test_reference.py` writes its own prose-only site per test.
- CI runs the unit tests only. The e2e suite needs a 30 MB Pyodide
  download and a browser. That is why the phone identity-row regression
  in #230 reached `main` with CI green: the browser test that would have
  caught it never ran there.

## 2. The re-cut

### 2.1 One file per object, fixtures that speak the new layout

`tests/test_build.py` splits into `tests/build/`, one file per thing the
build reads or writes, with one `conftest.py` holding three helpers:

- `tutorial(repo, id, body, **fields)` writes `tutorials/<id>/<id>.md`
  with `title`, `year`, `version` filled in unless overridden.
- `practice(repo, id, body)` writes `tutorials/<id>/<id>-practice.md` with
  `practice_for: <id>`.
- `course(repo, id, series)` writes `courses/<id>.yaml` from
  `{"Series title": ["id", …]}` and adds the id to `courses/index.yaml`.
  `repo` itself writes one course listing whatever `tutorial()` has
  written, so the common one-tutorial test needs no course at all.

| File | From today's classes | Changes |
|---|---|---|
| `test_tutorial.py` | TheHappyPath, Cells, SqlCells, SiteEditors, Includes, AltText, TutorialAssets, Frontmatter, Maths, IllustrativeCode, ListsWrittenTightAgainstProse, Folds, Notes, Datasets, StagedHints, CellReportPanel, TwoReleasesOnOneDay | Fixture helper only. Frontmatter's required-field test lists `title, year, version`. HappyPath's "builds to its module folder" becomes "builds to `tutorials/<id>.html`". |
| `test_links.py` | CrossLinks | `test_two_modules_may_each_have_the_same_slug` and `test_a_link_prefers_a_slug_in_its_own_module` are deleted — both are now impossible by construction — and replaced by one test: a second folder with an existing id stops the build and the message names the other tutorial and its course. |
| `test_practice.py` | PagesOfProblems, PracticeIsReachable | "same module" rule goes; a practice page follows its tutorial onto every course (new); a mixed set is listed under `mixed:` and refused if it is not a `practice_across` page (new). |
| `test_courses.py` | Navigation, TheSeriesRung, AllTutorialsPage, TheCrumbTrail, ArchivedTutorials (order-file half), CrossSeriesGlossary, TopicGroupsMatchRealTutorials | Rewritten against course files — see §3 for each test and why. The five borrowed-form and module-title tests are deleted. |
| `test_site.py` | TheFrontPage, PageCardsAndSections, TheAboutPage, TheStickyChrome, TheContentsOfAPage, TheSettingsPanel, FeedbackFooter, AssetVersions, TheExportFailsLoudly, BuildingNothing | Front-page cards generated from course files (new, replaces the hand-written-card test); `[[course-cards]]` in `read_page`. |
| `test_downloads.py` | TheDownloadableCopy, TheSeriesArchive, TheModuleArchive, DownloadsDoNotCollide | Per course; "a copy sits under the module its page does" becomes "under `tutorials/`, by id"; numbering across a course's series. |
| `test_versions.py` | VersionsOfATutorial, TheVersionListInTheManifest, TheManifestIdentifiesThePage | Manifest carries `id`, `courses`, `legacy` (new). |
| `test_reference.py` | TheReference, MathBasics, PythonBasics, TheCrossTutorialReference, WhatTheReferenceCanBeFilteredBy | Accumulation follows the course file's order (rewrite of CrossSeriesGlossary's four tests). |
| `test_curriculum.py` | TheKnowledgeMap, TheTopicTree, BrowseByTopicPage, NoDuplicateKeysInCurriculumData | `topic-groups.yaml` names ids, not module/slug pairs. |
| `test_redirects.py` | — | New: every line of `courses/redirects.yaml` becomes a stub page that points at a page that exists. |
| `test_check.py` | — | New: `check.py`'s own promises (§4). |

Nothing about cells, maths, folds, notes, datasets, hints, reports or the
reference panel's content changes in substance: those tests prove things
about a tutorial's body, and the body is untouched. They change only in
how their fixture is written.

### 2.2 The browser suite

- `tests/e2e/fixture/` gains `courses/e2e.yaml`; `conftest.py` copies it and
  stops writing `tutorials/<module>/`. `test_reference.py`'s `_tutorial`,
  `_set_order` and `MODULE` become `_tutorial`, `_course`.
- New browser tests, each for a foreseen failure (§3): the course chooser
  on the tree; saved work surviving the key migration; an old address
  landing on the new page; "Also part of" visible only when it applies.
- **CI runs the prose-only browser files.** `test_reference.py`,
  `test_narrow_screen.py`, `test_link_contrast.py` and the new layout
  tests need a browser but not Pyodide; a second CI job installs Playwright
  and runs them. This is the change that would have caught #230's
  identity-row failure before merge, and it costs about two minutes.

### 2.3 What is deleted, and why that is safe

- The borrowed form (three tests, #234): superseded by ordinary listing.
- `module_title` shown / folder name shown when absent (two tests): a
  course's title is in its file; there is no fallback to test.
- "A series without a name falls back to its filename": a series is a
  heading in a course file and must have a title (a Problem in `check.py`,
  a build failure).
- "No module file falls back to alphabetical": `courses/index.yaml` is
  written by the migration and required after it.
- "Order left in the frontmatter stops the build": there is no order in
  frontmatter to leave. Its replacement is "a placement field left in the
  frontmatter stops the build, and the message says to delete it" — the
  mistake a contributor copying an old file will make.
- "`series.yaml` naming an unknown series fails": there is no `series.yaml`.

## 3. The charter: what we foresee, and the test that proves it

Each row is a thing that will go wrong, given how people work, and the one
test that shows it cannot reach `main`. "Why this proof" says what the test
does not rely on, which is what makes it the right one.

| We foresee | Test | Why this proof |
|---|---|---|
| Two people create `first-steps` on two branches; both merge. | `test_links.py::test_a_second_folder_with_an_existing_id_stops_the_build_and_names_the_other` | Runs on the merged tree, not on either branch. The message is asserted too, because the fix is choosing a better id and the message has to say so. |
| A contributor copies an old tutorial and keeps `module:` in it. | `test_tutorial.py::test_a_placement_field_in_the_frontmatter_stops_the_build_and_says_to_delete_it` | The build must refuse rather than ignore: an ignored field is a field someone will keep writing. |
| An id in a course file has a typo; the series is quietly one short. | `test_courses.py::test_an_id_with_no_tutorial_behind_it_stops_the_build_naming_the_course_and_line` | The dangerous direction. Asserts on the course file and line so the fix is one edit. |
| A tutorial is written and never listed; nobody can find it. | `test_courses.py::test_a_tutorial_on_no_course_builds_and_is_noted` and `test_check.py::test_an_unlisted_tutorial_gets_a_note_saying_how_to_list_it` | Not an error — a draft is legitimate — but never silent, in the build and in the contributor's own tool. |
| The Computational Methods `first-steps` is renamed and a student's saved answers vanish. | `e2e/test_saved_progress.py::test_work_saved_under_the_old_key_is_there_under_the_new_id` | Seeds `dewlab:progress:computational-methods:first-steps` before load and reads it back under `dewlab:progress:first-steps-cm`. Does not go through the migration script; tests the runtime alone. |
| A bookmark or an external link to `tutorials/<module>/<slug>.html` breaks. | `test_redirects.py::test_every_old_address_has_a_stub_that_points_at_a_page_that_exists` and `e2e/test_redirects.py::test_an_old_address_lands_on_the_new_page` | The unit test proves every line of `redirects.yaml`; the browser test proves one stub does what a browser needs. |
| A PDP reader opens First Steps and sees the integrated course's tree. | `e2e/test_course_chrome.py::test_arriving_from_a_course_card_draws_that_courses_tree` | Arrives via the course page, not by setting storage directly, so it proves the whole path. |
| A tutorial on two courses shows "Also part of" on one where it isn't. | `test_courses.py::test_also_part_of_lists_the_other_courses_and_nothing_when_there_are_none` | Both branches in one test: present with two courses, absent with one. |
| Two courses list the same series and one drifts (a tutorial added to one, not the other). | `test_courses.py::test_the_same_id_may_be_listed_in_two_courses` plus the build's coverage report | We chose not to share series by reference. This test proves listing twice works; the drift itself is a choice, and the report makes it visible rather than forbidden. |
| A practice page is added and appears on none of the courses its tutorial is on. | `test_practice.py::test_a_practice_page_follows_its_tutorial_onto_every_course` | Two courses, one tutorial, one practice page; both course pages link it. |
| The reference panel on the PDP route accumulates trigonometry. | `test_reference.py::test_accumulation_follows_the_course_file_order_and_not_another_course` | Two courses sharing a tutorial, one with a maths series before it; the tutorial's manifest, built for the first course, carries nothing from the other. |
| A front-page card's text disagrees with the course page. | `test_site.py::test_the_course_cards_come_from_the_course_files` | There is nothing hand-written left to disagree. |
| Two tutorials get the same title on two courses and a reader can't tell them apart in search. | `test_courses.py::test_a_repeated_title_is_warned_about_naming_both_and_their_courses` and `test_site.py::test_search_entries_carry_the_course` | A warning, never an error — the title may be right. The search index carries the course so the reader has the context. |
| Two contributors write much the same tutorial under different names. | `test_courses.py::test_tutorials_covering_the_same_outcomes_are_reported` | Coverage, not titles, is the signal; three shared outcomes is the threshold and the test pins it. |
| The migration is run twice, or on an already-migrated tree. | `refactor/test_migrate.py::test_a_migrated_tree_reports_nothing_to_do` (deleted with the folder) | Cheap insurance for the one day it matters. |
| The renamed tutorial's practice page still names the old id, and so points at the *other* First Steps. | `refactor/test_migrate.py::test_a_rename_carries_practice_for_and_links_with_it` | Found by `check.py` on the first real dry run of the migration, before any test existed for it — which is the argument for running the tool over the migrated tree as a step in itself. |
| `check.py` calls a picture inside a code example a missing image. | `test_check.py::test_an_image_inside_a_code_example_is_not_a_missing_image` | Three web-authoring tutorials teach `<img src="does-not-exist.jpg">` on purpose; the first run flagged all three. |
| `check.py` calls a tutorial whose id ends in `-practice` a practice page. | `test_check.py::test_a_practice_page_is_known_by_its_frontmatter_not_its_name` | `sql-practice` is a real tutorial; the first run refused it. A page is what its frontmatter says. |
| `check.py` says "No problems" about a tutorial the build then refuses. | `test_check.py::test_everything_check_calls_a_problem_the_build_also_refuses` | Runs both on the same fixtures: every Problem is a build failure and every build failure of the kinds `check.py` covers is a Problem. The tool's promise, proven. |
| `check.py` is run from the wrong folder, or on a file it doesn't know. | `test_check.py::test_an_unknown_path_gets_a_plain_sentence_not_a_traceback` | The audience is somebody's first day. |
| dewnote opens a migrated tutorial and treats it as plain markdown. | dewnote's `full-corpus.test.ts` (other repository) | Round-trip is byte-level and passes; dialect detection keys on `year`, which stays. Listed here so nobody deletes `year:` without checking. |

## 4. `check.py` — the contributor's tool

What it is: one file, standard library plus PyYAML, no build, one second.
`python3 check.py tutorials/<id>` checks a tutorial and its practice page;
`python3 check.py courses/<id>.yaml` checks a course; no argument checks
everything. Every line starts with `OK`, `Problem` or `Note`, and every
Problem says what to do. It exits 1 on any Problem so it can sit in a
pre-commit hook or a CI step.

What it checks, and where the same rule lives in the build:

| Problem it reports | Build check it mirrors |
|---|---|
| Folder name is not a valid id | `load_all()` id rule |
| No `<id>.md` in the folder | `load_all()` |
| Frontmatter missing, unclosed, not YAML, missing `title`/`year`/`version` | `split_frontmatter()` |
| `version:` not `YYYY.MM.DD.n` | `versions_of()` |
| Old placement fields present | new refusal in `load_all()` |
| A cell with no `id:`, or two cells with one id | `extract_blocks()` |
| An image not in the folder | `TestTutorialAssets`' rule |
| Practice page without `practice_for`, naming a missing tutorial, or with `covers:` | `practice_pairs()` |
| Glossary entries without term or definition | `own_glossary()` |
| Course file not YAML; no title; no contents; series without title or tutorials; id not found; id listed twice; `mixed:` naming a non-mixed page | `courses()` |

What it only notes: no practice page; no cells; a title another tutorial
also has; a tutorial no course lists; a course missing card, code or
description; a course absent from `index.yaml`.

Where it lives: repository root, next to `build.py`, so `python3 check.py`
works from a fresh clone with no path to remember. Its page is
`docs/CHECK_YOUR_WORK.md`, written to the plain-language rules in
`planning/PEDAGOGICAL_STYLE_GUIDE.md` §4 — short sentences, every sentence
with a verb, no idiom, a small vocabulary, and a "Words on this page" list
at the end. `docs/WRITING_TUTORIALS.md` gains one line at the top pointing
at it, and `CONTRIBUTING.md` one line under "Before you open a pull
request".

`tests/build/test_check.py` proves the tool: each Problem against a fixture
that the build also refuses, each Note against one the build accepts, and
the two promises in the charter above.

## 5. Order

- Step 2 of `PLAN.md` moves `check.py` to the root and `CHECK_YOUR_WORK.md`
  to `docs/`, since both describe the new layout.
- Step 5 of `PLAN.md` is this document's §2 and §3.
- The CI browser job (§2.2) can land before any of it; it is independent.
