# The test suite, explained

Three directories, and each one earns its split by a different real
question, not by convention:

- **`tests/`** (root) — does this standalone Python module work, on its
  own, with no build and no browser? `tutorial_tools.py`, `from_notebook.py`,
  `report_patterns.py`/`label_report.py`, `pair_results.py`,
  `curriculum_map.py`. Each imports its subject directly and never touches
  `build.py`.
- **`tests/build/`** — does `build.py` turn source into the right static
  output? Every file here calls `b.build()` (via the shared `repo` fixture
  in `helpers.py`) and inspects what landed in `site/`. No browser, ever.
  `tests/build/test_check.py` is the one file here that isn't testing
  `build.py`'s own output — it's testing `check.py`, a standalone tool
  like the root five — but it lives here because it deliberately
  cross-checks its own Problems against real `BuildError`s, which needs a
  real build to compare against.
- **`tests/e2e/`** — does this work in a real browser? Playwright drives a
  real Chromium against a real served site, sometimes against a real
  self-hosted Pyodide. Slower, and the only place JavaScript-only behavior
  (a click, a keypress, `localStorage`) can be proven at all.

If you're not sure which one a new test belongs in, ask "does this call
`build.build()`?" and "does this need a browser?" — the answers place it.

---

## What's in each directory

**`tests/` (root) — one file per standalone tool:**

| File | Tests |
|---|---|
| `test_tutorial_tools.py` | `assets/tutorial_tools.py` — the cell-execution helpers (`show`, `check`, `run_query`, tracebacks, widgets…) injected into every cell's namespace |
| `test_from_notebook.py` | `from_notebook.py` — the `.ipynb` → tutorial-markdown converter |
| `test_report_patterns.py` | `report_patterns.py`/`label_report.py` — pattern-matching over report-doors issues |
| `test_pair_results.py` | `pair_results.py` — the pair-game judgement report generator |
| `test_curriculum_map.py` | `curriculum_map.py` — the topic-tree/curriculum-map data generator |
| `test_glossary_python.py` | `dev/glossary_python.py` — every glossary entry naming Python exists and its example fits the real signature; the signatures file is current; the build attaches signatures |

**`tests/build/` — one file per slice of `build.py`'s output:**

| File | Tests |
|---|---|
| `test_tutorial.py` | The core page engine: cells, site editors, hints, folds, notes, frontmatter — the biggest file here by a wide margin |
| `test_site.py` | Non-tutorial site content: cards, `[[marker]]` sections, wrapped-section markdown |
| `test_questions.py` | `​```question` fence markup: multiple-choice and fill-in-the-blank generation |
| `test_app_cell_markup.py` | `app`-fence markup generation (the build-time half; live behavior is `tests/e2e/test_app_cell_live.py`) |
| `test_reference_index.py` | The cross-tutorial glossary/reference index `build.py` assembles (`write_reference_index()`) — the data a panel shows, not the panel itself |
| `test_curriculum.py` | Series shape and knowledge-map data from course files |
| `test_courses.py` | Course-file processing: listings, moved-frontmatter migrations |
| `test_releases.py` | Version/release numbering and manifest fields |
| `test_downloads.py` | Standalone/zip export generation |
| `test_practice.py` | Practice-page linking rules |
| `test_context.py` | Context-page linking rules and the build errors a bad `context_for:` gets |
| `test_links.py` | Cross-page link resolution and validation |
| `test_old_addresses.py` | Legacy-URL redirect stub generation |
| `test_check.py` | `check.py`'s own Problems, cross-checked against real `BuildError`s |

**`tests/e2e/` — grouped by what's actually being exercised, not always one file per feature:**

*Core reading/execution smoke:* `test_phase0_golden_path.py` — real cell
execution (numpy, pandas, matplotlib, SQL), site editors, settings, the
contents/tree pages, all in one real browser + real Pyodide pass.

*Cell chrome:* `test_cell_run_menu.py`, `test_cell_collapse_duplicate.py`,
`test_cell_report.py` (also covers the hint icon, which shares the same
disclosure code as the report icon), `test_cell_hints_staged.py`,
`test_autocomplete.py`, `test_stop_button.py`, `test_custom_cells.py`,
`test_app_cell_live.py` — things that happen on or around one cell.

*Save/restore:* `test_saved_progress.py` (the core save/restore mechanism,
plus the live run-summary and the site-wide progress badges as their own
test classes) and `test_versions.py` (the same mechanism once a tutorial
has more than one release).

*Highlight feature:* `test_highlight_anchoring.py` (locating a passage),
`test_highlight_creation.py` (making a mark), `test_highlight_wrapping.py`
(the DOM mechanics of wrapping/restoring one), `test_highlight_popover.py`
(the edit/remove UI), `test_highlight_schema.py` (what survives a save),
`test_highlight_colors_and_list.py` (colour choice, the Notes panel's own
list). Five-going-on-six real sub-mechanisms, not accretion — each is
substantial on its own.

*Reference/glossary UI:* `test_reference_panel.py` — the live panel
(open/close, search, mobile launcher). Its build-time counterpart is
`tests/build/test_reference_index.py`.

*Authoring tool:* `test_editor.py` — the editor's own UI. Its build-time
counterpart, what the tutorials it writes actually build into, is
`tests/build/test_tutorial.py`.

*dewmini (the standalone tool):* `test_dewminiweb.py`, `test_dewmini_workbench.py`.

*My Notes:* `test_my_notes.py` — the cross-tutorial notes/highlights page.

*Everything else:* `test_multi_course_pages.py`, `test_student_notes_prose_only.py`.

*Cross-cutting properties, each owning one thing completely rather than
being scattered across whichever file happened to touch it first:*

| File | Owns |
|---|---|
| `test_contrast.py` | Every text/background colour pairing the design system defines, against the real WCAG AA 4.5:1 minimum, in every theme |
| `test_dismissible_panels.py` | The "opens from a toggle; Escape, an outside click, and its own close button all close it again" contract, for every one of the seven places it's wired |
| `test_page_smoke.py` | Every real page template: loads with no console errors, never scrolls sideways on a phone |
| `test_question_interaction.py` | Live grading of a `​```question` fence — selecting an option, filling a gap, and what survives a reload |

Confirm-dialog gaps (a destructive action gated behind a native
`confirm()`) didn't get a file of their own. Three of the eight sites
already had solid, feature-specific tests (`test_highlight_popover.py`'s
removal, `test_cell_run_menu.py`'s Clear, `test_custom_cells.py`'s clear-all)
checking real state, not just "the dialog appeared" — a shared contract
file would have meant rebuilding those assertions for no gain. The five
gaps that existed (declining wasn't proven to actually decline in three
places, and two sites had no test at all) were closed directly in the
files that already own that feature.

---

## Two terms, in case they're not familiar

**Smoke test.** The cheapest test that just proves a thing turns on, before
checking anything specific about how it behaves. "This page loads with no
console errors" is a smoke test; "this button does the right thing when
clicked" is not. (From testing physical hardware: power it on, see if
smoke comes out.)

**A confirm dialog.** A native browser `confirm("Are you sure?")` popup —
the kind Playwright's own API calls a `dialog`, which is where
`test_confirm_dialogs`-style naming comes from even where there's no file
by that name. Declining it should always leave things exactly as they
were; accepting it should do the destructive thing. Both halves are worth
proving — a test that only clicks "OK" never proves Cancel actually
cancels.

---

## Where does a new test go?

1. **Is it a standalone Python module `build.py` never touches?** `tests/`
   root, one file for the module.
2. **Are you checking what `build.py` writes to `site/`?** `tests/build/`,
   in the file that already owns that slice of output, or a new file if
   it's a genuinely new slice.
3. **Are you checking live browser behavior — a click, a keypress, state
   surviving a reload?** `tests/e2e/`, in the file for that feature.
4. **Is what you're checking a property that should hold in more than one
   place** — a contrast ratio, a dismissal contract, "does this page even
   load," a confirm-then-decline guarantee — **rather than one feature's
   own behavior?** Don't scatter one more instance into whichever file you
   happen to be in. Either it belongs in one of the four property files
   above, or (if it's a new kind of property) it's worth asking whether it
   deserves one of its own — enumerate every real instance of the property
   in the source first, the same way each of the four above did, rather
   than writing the one case you happened to be looking at.
5. **Are you adding a build-time and a live-behavior test for the same new
   feature?** Give them names that say so — a `_markup`/`_live` suffix
   pair the way `test_app_cell_markup.py`/`test_app_cell_live.py` read as
   a pair, or a shared root the way `test_tutorial.py`/`test_editor.py`
   and `test_reference_index.py`/`test_reference_panel.py` are meant to,
   even though neither of those two pairs shares a literal filename stem.
   Two files named one character apart for unrelated reasons — the build
   and live halves of app-cell coverage used to differ only by a plural
   `s`, easy to misread in a CI failure list — is exactly what this is
   trying to avoid.
