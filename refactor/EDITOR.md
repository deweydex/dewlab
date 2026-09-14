# The editors

Two editors write dewlab tutorials: `assets/editor.js` here, which talks to
GitHub's API from a browser tab, and dewnote, a separate repository that
opens a folder or a repository and knows dewlab as one of three dialects.
Both encode the current layout. This lists what changes in each.

## 1. assets/editor.js (this repository, step 4)

What it does today, in the parts that matter here: lists every path under
`tutorials/` from the GitHub tree; reads each `*.order.yaml` into
`state.series` (module from the path's second segment, name from the file
name, title from `series:`); reads each tutorial's frontmatter for `module`
and `slug`; marks a tutorial "off" when its frontmatter names a series that
does not list it; builds new paths as `tutorials/<module>/<slug>/<slug>.md`;
creates a tutorial from `TEMPLATE` with `module`, `module_title` (copied
from a sibling) and `series` filled in; moves a slug between order files;
resolves `tutorial:` links module-first.

Changes, by function:

- `TEMPLATE` (l. 329) — remove `slug`, `module`, `module_title`, `series`.
  Keep `title`, `year`, `version`.
- `load()` (l. 397) — read `courses/*.yaml` and `courses/index.yaml` instead
  of order files; `state.courses` = `{path, id, title, contents:
  [{title, tutorials: [...]}, …], mixed}`; a tutorial is "off" when no
  course lists its id.
- `newPathOf`, `releasesOf`, `pathOf`, `titleOf` (l. 445–470) — take an id;
  paths are `tutorials/<id>/…`.
- The tutorial index (l. 478–490) — key by id (folder name), not
  `module/slug`.
- `move()` (l. 496) — moves an id between series in a course file, or
  between course files; rewrites the YAML list in place (the order files
  were written with a regex today; course files nest one level deeper, so
  use a small YAML list rewriter that preserves comments).
- New tutorial (the sibling copy at l. 512–518) — no sibling lookup for
  `module_title`; instead ask which course and series to list it on (a
  picker over `state.courses`), and add the id to that list in the same
  commit as the file. Offer "none yet" — the file builds, on no course.
- `resolveTutorialLink`, `tutorialLinkProblems` (l. 151–170) — ids are
  site-wide; "ambiguous across modules" cannot happen; drop that branch.
- The search box (l. 193) — match on id and title; show the course(s) the
  tutorial is on.
- Uniqueness: on the new-tutorial form, as the id is typed, check
  `state.files` for `tutorials/<id>/` and say "taken — 'First Steps' in
  Programming and Maths, Integrated"; on the title, check the index for the
  same title and show a warning line that does not block.
- `STATUS_MEANS` (l. 320) — "On the course, in the reading order" → "Listed
  on at least one course"; "beta" → "Published but on no course".
- The commit/PR path (l. 300) — unchanged.

Done when the four checks in `PLAN.md` step 4 pass by hand.

## 2. dewnote (separate repository, step 8)

dewnote decides a file's dialect from its frontmatter alone
(`src/dialect.ts`: `year` present → dewlab), so migrated files are still
recognised as dewlab. Everything else that touches placement:

| File | Today | Change |
|---|---|---|
| `src/frontmatter-fields.ts` | dewlab's required list: `title, slug, module, module_title, year, series, version`; `module`/`series` rows indexed as pickers (decision 11) | Required: `title, year, version`. Remove the `slug`, `module`, `module_title`, `series` rows. `practice_for` stays, indexed over ids. |
| `src/file-index.ts` | indexes `slug`, `module`, `series` from frontmatter; "the one file among several sharing a slug" logic for versions | Index the id from the path (`tutorials/<id>/`), and the courses that list it from `courses/*.yaml`; drop `module`/`series`; the shared-slug disambiguation goes (ids are unique). |
| `src/series.ts`, `src/series-panel.ts` | reads `<series>.order.yaml` under `tutorials/<module>/` into `{module, slug, title, order}`; the panel's "Module (leave blank if already inside one)" input | Read `courses/*.yaml`; a course has titled series with ordered ids; the panel groups by course, then series, and reorders by rewriting the list in the course file. The module input goes. |
| `src/folder-store.ts`, `src/github.ts`, `src/repo-panel.ts` | walk for `.order.yaml`; the new-file placeholder `tutorials/module/new-tutorial.md` | Walk for `courses/*.yaml`; placeholder `tutorials/new-tutorial/new-tutorial.md`; on create, offer a course and series to list it on. |
| `src/link-check.ts`, `src/link-picker.ts` | `tutorial:`, `module:`, `series:` link kinds checked against the index's module/series values | `tutorial:` checks against ids; `module:` becomes `course:` (or stays, as an alias, pointing at `courses/<id>.html`); `series:` links need a course to be meaningful — drop, or resolve to the first course that has a series of that title. |
| `src/dialect-convert.ts` | `DEWLAB_ONLY_FIELDS = ["year", "covers", "practice_for", "practice_across"]`; dewstack → dewlab adds `module`/`series` | Remove any code that adds `module`/`series`/`module_title`/`slug` when converting to dewlab; `year` stays. |
| `src/full-corpus.test.ts`, `fixtures/` | round-trips `../dewlab` tutorials byte for byte | Passes as is (round-trip is byte-level); fixtures gain one migrated file. |
| `planning/DIALECTS.md` §1 | "File layout … `tutorials/<module>/<slug>/<slug>.md` … Required: `title, slug, module, module_title, year, series, version`" | Rewrite the layout and the required list; describe `courses/`. |
| `DECISIONS.md` | decision 11 (module and series pickers over the index) | A new decision: placement is read from course files, and the form has no placement fields; the picker survives as "list on course / series" at create time. |
| `planning/PLAN.md` §8 | dewlab's 2026-09 changes | Add this change and the order of work above. |

What does not change in dewnote: cells and their header grammar, the
block model, the round-trip guarantee, exports, the Mac app, GitHub
authentication. The change is confined to how it finds and places files.

A dewlab PR that lands steps 1–7 breaks dewnote's ability to *place* a
dewlab file (it will show every tutorial as "off" and offer module/series
rows that the build ignores) but not its ability to open, edit, run or
round-trip one. That is acceptable for a few days; the dewnote PR is the
fix.
