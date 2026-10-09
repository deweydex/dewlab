# Test audit

*Working document, started 9 October 2026. Planning, not student-facing.*

The question put to every test: **if this fails, does something break for a
reader or for the build, or has an author only done something we would not
have chosen?** Judged on what the repository does today. No history.

Verdicts:

- **Keep** — a reader's page breaks, a contract (ids, saved work) is at stake,
  or it tests a real feature.
- **Advisory** — a house preference or a check on a planning file. Report it,
  never fail a run.
- **Re-home** — the aim is sound but the test reads one page's content, or
  greps source text, so it fails for reasons that are not the aim. Rewrite it
  against a fixture or against behaviour.
- **Retire** — it pins an authorial choice or an implementation detail and
  guards no reader.
- **Wire up** — it guards something real but never runs where it matters.

## Coverage so far

Read in full: `test_check_doc_links`, `test_video_links`,
`test_map_layout_script`, `test_picture_patterns`, `test_report_patterns`,
`test_term_uses`, `test_glossary_python`, `test_handwritten_classes`.

Read in part (names, headers and the content-coupled bodies): `test_pair_results`,
`test_from_notebook`, `test_curriculum_map`, `test_erd_graphics`,
`test_tutorial_tools`.

Not yet read: `tests/build/` (24 files), `tests/e2e/` (about 50 files), and the
230 refusals in `build.py`.

---

## tests/test_handwritten_classes.py — the clearest case

The docstring promises one thing: every hand-written `dl-` class has a CSS
rule. The file holds twelve tests, and eleven of them are about something else.
They pin numbers, strings and layout details in four individual tutorials
(`when-it-goes-wrong`, `flexbox-first-steps`, `named-grid-areas`, `the-box`),
plus source text in `build.py`, `tutorial-runtime.js` and `tutorial-style.css`.
Someone opening it to learn why a CSS check failed finds a tutorial's
arithmetic.

| Test | Verdict | Why |
|---|---|---|
| `every_hand_written_dl_class_is_styled` | **Keep** | An unstyled class gives a page of unstyled boxes, and nothing else notices. |
| `the_scan_finds_the_markup_built_diagrams` | **Re-home** | Guards the scanner, but by naming one real page (`the-box`). Use a fixture page. |
| `annotated_traceback_quotes_the_cell_it_describes` | **Keep, re-home** | "Every number is run" (HOW_DEWLAB_THINKS) makes prose-and-code agreement a real rule. But it is hard-wired to one page and one cell id. |
| `annotated_traceback_names_the_error_the_cell_raises` | **Keep, re-home** | Same. |
| `wrap_threshold_matches_the_tutorials_own_css` | **Keep, re-home** | Same: the 366px on the page must follow from its CSS. |
| `flexbox_preview_measures_the_row_and_not_the_frame` | **Keep, re-home** | Same: the prose names 366, which holds only with a zero body margin. |
| `grid_map_flips_at_the_tutorials_own_breakpoint` | **Keep, re-home** | Same: a picture and a slider must agree with the page's media query. |
| `preview_width_readout_can_land_on_a_threshold` | **Retire** | Greps `build.py` and the runtime for `step="1"` and a method name. It tests how the code is written. The slider's behaviour belongs to a browser test. |
| `grid_maps_queried_width_is_the_width_it_draws` | **Retire or move to e2e** | Greps a CSS rule for the absence of `padding`. A layout bug should be caught by measuring, not by reading the stylesheet. |
| `the_box_demo_has_something_for_a_margin_to_push` | **Retire** | Demands exactly two `.box` elements. That is an authorial choice about a demo. |
| `flexbox_cards_stay_narrower_than_their_flex_basis` | **Re-home** | Ten characters stands in for a measured pixel width. Measure in the browser or drop it. |
| `preview_width_control_does_not_resize_while_dragged` | **Retire** | Greps the stylesheet for `min-width` and the runtime for `requestAnimationFrame(apply)`. |

The shape of the fix is one general mechanism, not eight page-specific tests:
a page that states a number derived from its own code declares so, and a single
check re-derives it. That keeps the rule HOW_DEWLAB_THINKS endorses and frees
authors to rewrite those pages.

## tests/test_erd_graphics.py — never runs in CI

`svgwrite` is not in `requirements-build.txt` and the workflow does not
install it, so every test in the file skips there. 505 lines pass silently.
**Wire up or move**, deliberately: either install `svgwrite` in the unit job,
or label these as local-only generator tests in `dev/graphics/`.

Inside the file, once it runs:

- **Keep.** Layout and renderer logic (arrow placement, cycles, tree
  overlap, crossing counts, "branches sum to 1").
- **Keep as freshness checks, ideally as CI `--check` steps.** "The committed
  picture is what the generator draws" (two parametrised tests).
- **Keep.** "Colours are theme tokens and nothing has an id" protects dark
  mode and duplicate ids on a page.
- **Advisory.** "Alt text is written in full sentences" (`endswith(".")`) is a
  style rule. The alt text's existence is the structural half, and the build
  already refuses a missing `alt`.
- **Re-home.** Tests that name particular tutorials and cell ids
  (`where-chains-lead` / `a-weather-machine-1`, `multiplying-grids`, and the
  `range-collapsing`, `merge-walk` ones).

## Smaller files

| File | Verdict | Notes |
|---|---|---|
| `test_check_doc_links.py` | **Keep** | Unit tests of a documentation checker. The one real-repository test is already advisory. |
| `test_video_links.py` | **Keep** | Link-finding and status logic for a weekly workflow. |
| `test_map_layout_script.py` | **Keep two, advisory one** | The determinism and fixture tests guard the script. "Reproduces the committed layout of the real map" checks a generated file is current, which the build never recomputes. Move to a CI `--check` like the topic game and editor graph. |
| `test_picture_patterns.py` | **Keep five, re-home one, keep one** | The generator's behaviour is a real accessibility feature. `every_picture_script_adds_the_pattern_layer` greps source for a magic string and `len(writers) >= 14`; test the output pictures instead. `no_two_pictures_share_a_pattern_id` guards a real collision. |
| `test_report_patterns.py` | **Keep** | Parsing and thresholds for the report workflows. Tidy: `issue()` takes an unused `days_old`; `label_report_uses_the_same_parser` exists only because the parser is duplicated, so deduplicating retires it. |
| `test_term_uses.py` | **Advisory (move to a house folder)** | Tests a lister for authors, referenced only from WRITING_TUTORIALS. Not in the build or CI. `after_its_start` encodes a teaching rule about when to mark a term. |
| `test_glossary_python.py` | **Keep** | The build uses `glossary_python`. `every_python_name_exists` protects the reference panel. `signatures_file_is_current` skips off the Python version it was written under; make it a `--check`. |
| `test_pair_results.py` | **Keep (tooling)** | CI regenerates the reports and diffs them. Bodies not fully read. |
| `test_from_notebook.py` | **Question** | Converts notebooks from another repository. Referenced only from docs and the decisions log. If nobody imports notebooks any more, retire the script and its 300 lines of tests. |
| `test_tutorial_tools.py` | **Keep** | The runtime library's pure logic, 1,499 lines. Bodies not yet read for wording rules. |

## test_curriculum_map.py

The advisory split already done (7.291) is right as far as it goes. Remaining
candidates, since `build.py` reads `topics.yaml`, `outcomes.yaml`,
`out-of-scope.yaml` and `topic-groups.yaml` for the topic tree and topics page:

- **Keep.** `no_topic_invents_an_outcome`, `prerequisites_are_real`, `have_no_cycles`, `every_topic_has_a_name_and_a_description` — the build and a reader's topic tree depend on them.
- **Advisory.** `sequence_graph_has_no_repeated_node` reads only `CURRICULUM_MAP.md`, a planning document. `groundwork_is_written_up_like_a_topic`, `a_groundwork_code_never_collides`, and `every_proposal_is_well_formed` check planning files the build does not use; confirm before moving.

## Decisions for you

1. `test_from_notebook.py`: do you still convert notebooks?
2. `test_erd_graphics.py`: run in CI, or label as local?
3. The prose-matches-code pages: do you want the one declared mechanism
   described above, replacing the page-specific tests?
