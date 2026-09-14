# Touchpoints

Every place in this repository that reads a tutorial's module or series, or
builds a path or a key from them. Line numbers are from `main` at
`3b5b79a` (2026-09-14) and will drift; the function names will not.

## 1. build.py (step 2)

Identity and paths

- `Tutorial.module` (property, from `meta["module"]`), `Tutorial.series`,
  `Tutorial.module_title`, `Tutorial.slug` — `slug` becomes the folder
  name, the other three go.
- `Tutorial.out_path` — `OUT / "tutorials" / module / slug.html` → drop the
  module segment.
- `load_all()` — walks `tutorials/**`; becomes flat; adds the duplicate-id
  refusal.
- `versions_of()` — families keyed `(module, slug)` → keyed by id.
- `practice_pairs()` — "same module" check goes; a practice page's
  `practice_for` names an id.
- `glossary_path()` — beside the file; unchanged.

Placement

- `order_files()`, `series_titles()`, `module_order()`,
  `module_series_order()`, `check_series_order()`, `MODULE_INFO`,
  `module_titles()` → replaced by `courses()` reading `courses/*.yaml` and
  `courses/index.yaml`.
- `series_of()` — including the borrowed-entry block added in #234 →
  groups from course files; `member.order` becomes per-placement.

Rendering that takes a module or series

- `nav_for()` (previous/next, `dl-nav-up` to "All tutorials")
- `link_between()` — relative paths; unchanged in shape, fewer segments.
- `crumb_trail_html()` — the tree: courses list, this course's series,
  this series' members, own rung. Gains the course chooser markup when a
  tutorial has several placements.
- `practice_link()`
- `render_tutorials_list()` / `render_module_body()` → per course.
- `write_module_page()` → `write_course_page()`; description, code and card
  from the course file.
- `write_series_zip()`, `write_module_zip()` — per course; filenames from
  the placement's position.
- `standalone_html()` — strips the tree except the own rung; unchanged in
  shape.
- `site_footer()`, `report_doors_panel_html()` — take `(page, version)`;
  `page` was `module/slug`; becomes the id.
- `write_search_index()` — `moduleTitle`, `series`, `url` per entry →
  `courses: [...]` and the new url.
- `write_tree_page()`, `write_topics_page()` — link by id; the topic-groups
  file names `module`/`slug` pairs today → ids.
- `render_index()` — the hand-written card fences in `pages/home.md` are
  replaced by cards generated from course files.
- `write()` — the manifest gains `id`, `courses`, `legacy` (the old
  `module:slug` for storage migration); `{{MODULE}}`, `{{SERIES}}` tokens.
- New: `write_redirects()`, the duplicate-title warning, the
  coverage-overlap warning, `assets/routes.json`.

Data files the build reads that name modules

- `planning/curriculum/topic-groups.yaml` — `module`/`slug` pairs → ids.
- `planning/curriculum/outcomes.yaml` — unaffected (outcome codes).
- `tutorials/modules.yaml`, `*/series.yaml`, `*/*.order.yaml` — replaced.

## 2. assets/tutorial-runtime.js (step 3)

- Keys built as `${PREFIX}${manifest.module}:${manifest.slug}`:
  `customCellsKey()` (2212), `progressKey()` (3531), notes export
  (3825), version pin (4107); the list badge at 4026 reads
  `link.dataset.module`/`slug`.
- Export filenames from `[manifest.module, manifest.slug]` (2526, 2665).
- New: `migrateStorage()`, `currentCourse()`, `drawCourseChrome()`, the
  course chooser on the tree's course rung, "also part of".
- `initVersionsSection()` — unchanged; still finds the own rung by class.
- `vendor-src/` rebuild after any change here.

## 3. assets/editor.js (step 4) — see EDITOR.md §1

## 4. Tests (step 5)

- `tests/test_build.py` — ~200 lines use `tutorial_path(repo, slug,
  module)`, `set_order(repo, module, series, slugs)`, or a
  `computational-methods` path; the `write()` helper writes
  `tutorials/computational-methods/<slug>/<slug>.md` and an order file.
  Rewrite the three helpers to write `tutorials/<slug>/<slug>.md` and a
  course file, and most tests follow. Classes that assert on the layout
  itself: `TestFrontmatter` (module/series fields), `TestTheSeriesRung`,
  `TestAllTutorialsPage` (module order, borrowed entries),
  `TestTheCrumbTrail`, the practice-page tests ("same module"), the
  standalone/zip tests (filenames), `TestTheKnowledgeMap` (topic-groups
  pairs).
- `tests/e2e/conftest.py` — 7 module-path lines; `test_reference.py` — 40
  (`MODULE = "reference-fixtures"`, `_tutorial`, `_set_order`);
  `test_versions.py` — 7; `test_phase0_golden_path.py` — 0 (uses the real
  site). 17 e2e files name a module somewhere; most in a URL.
- `tests/e2e/test_progress_badges.py`, `test_progress_summary.py` — keyed
  storage; assert on the new keys.

## 5. Dev scripts (step 2, item 11)

- `dev/curriculum_map.py` — `MAIN_MODULE`, `MAIN_SERIES`, URL at line 111,
  "earlier in the module" at 301 → courses; regenerate
  `planning/CURRICULUM_MAP.md`.
- `dev/draw_topic_graph.py` — `tutorials/{module}/{slug}.html` at 386–387.
- `dev/from_notebook.py` — writes into `tutorials/<module>/`; takes an id.
- `dev/build_topic_editor.py`, `dev/build_topic_game.py` — check for
  module in their data; likely unaffected.

## 6. Documents (step 6)

- `docs/WRITING_TUTORIALS.md` — frontmatter table, "Where a tutorial sits
  in its series", "Linking between tutorials" (`tutorial:` looks in its own
  module first — no longer meaningful), "Adding a new module", "Releasing a
  new version" (paths).
- `ARCHITECTURE.md` §1 — "reads `tutorials/**/*.md`".
- `CONTRIBUTING.md`, `CLAUDE.md`, `docs/build-explained.md`,
  `docs/FOR_STUDENTS.md`.
- `DECISIONS_LOG.md` — 7.172; 7.171's borrowed form is superseded.
- `planning/PLAIN_LANGUAGE_PASS.md` — "Also part of …".

## 7. Elsewhere

- `.github/workflows/deploy.yml` — unchanged (Pages serves whatever
  `site/` holds; the redirect stubs are pages).
- `.github/workflows/tests.yml` — unchanged.
- `compose/dewmini.html` — shares the stylesheet only; unaffected.
- `staging/dewstack-import/` — imported tutorials in the old layout; run
  the migration over it too, or leave it as a record.
- `topic_editor/`, `topic_tree_game/`, `dewmark/` — separate tools; check
  `topic_tree_game` for tutorial links by module.
