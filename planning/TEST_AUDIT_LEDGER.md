# Test audit ledger

*Generated 10 October 2026 from the line-by-line audit. Every test that is not plain KEEP is listed; the other 872 are sound as they stand. Verdicts were made by a model reading each test, then spot-checked; treat each as a proposal, not a ruling.*

See [`TEST_AUDIT.md`](TEST_AUDIT.md) for what the audit found and what was changed.

## Retire (45)

Retire. Pins an authorial choice or an implementation detail, duplicates another test, or guards something no longer in the product.

### `tests/build/test_blocks.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 99 | `test_no_word_in_the_markup_judges` | Forbids verdict words (correct, wrong, pass, fail) in markup: a voice rule HOW_DEWLAB_THINKS says is not checked; substring "pass" is crude. | Delete; leave voice to the style guide checklist. |
| 254 | `test_a_page_without_solutions_runs_nothing` | Asserts subprocess.run is never called when no solutions exist: an implementation detail and speed concern, not a reader-visible behaviour. | Delete, or fold into a timing-free check that the build succeeds without python. |

### `tests/build/test_context.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 92 | `test_a_context_page_for_one_tutorial_says_that_tutorial` | Only checks single-tutorial wording ('that tutorial'); the back-link itself is covered by the two-tutorial test. Pins house copy. | Delete. |

### `tests/build/test_courses.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 169 | `test_a_moved_frontmatter_field_stops_the_build_and_says_to_delete_it` | Guards a finished frontmatter migration; the stale field is ignored harmlessly and no reader page breaks. Field names are hand-listed. Five parametrized cases. | Delete, or fold into one generic unknown-frontmatter-field test. |

### `tests/build/test_curriculum.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 54 | `test_a_series_too_short_to_have_a_shape_gets_none` | Pins the design choice that a short series gets no map, and passes vacuously when tree.html is missing. | Delete; the four-tutorial test covers map building. |
| 88 | `test_the_tutorial_just_before_does_not_get_a_second_arrow` | Pins an authorial choice (no duplicate arrow for the previous tutorial) and passes vacuously if no map is built. | Delete. |

### `tests/build/test_downloads.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 214 | `test_a_series_of_one_is_offered_in_the_singular` | Pins the singular wording "Download this one as a single file"; the count is right either way, so it guards copy, not function. | Fold into the series test as an assertion that no wrong count appears. |

### `tests/build/test_predict_build.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 95 | `test_no_word_in_the_block_judges` | Pins voice: verdict words are explicitly not checked by the machine (HOW_DEWLAB_THINKS). Tests build.py's own UI strings against a house habit. | Delete; leave to the style guide checklist. |

### `tests/build/test_reference_index.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 240 | `test_the_shipped_files_are_themselves_well_formed` | Loads the real shipped basics files and asserts only truthiness (corrected from content-independent). Any full build loads them anyway, so it duplicates. | Delete; the build already fails on malformed shipped basics. |
| 511 | `test_the_bands_are_the_ones_chosen_against_the_real_spread` | Pins a tuning choice: the tier-to-band mapping. Any retune fails it by design, and the corpus figures are only a comment. No reader breakage. | Delete; the level test above covers the mechanism. |

### `tests/build/test_templates.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 44 | `test_every_template_is_one_the_test_knows` | Hard-codes today's template slugs; a bookkeeping list that must be edited whenever a template is added. Tests nothing about the machinery. | Delete; install whatever templates exist. |

### `tests/build/test_toolkit_build.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 65 | `test_the_cell_and_its_reference_are_read_off_the_source` | Asserts internal attributes (toolkit_reference); the same facts are checked through the built manifest in the later-page tests. Implementation detail and duplicate. | Delete; rely on manifest-level entry assertions. |

### `tests/build/test_tutorial.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 909 | `test_report_doors_links_marks_only_the_issue_links` | Counts a class string and pins Discussions link ahead of issue links; an implementation detail of how the runtime finds links, which a browser test would cover. | Delete; cover runtime link injection in a browser test if wanted. |

### `tests/e2e/test_autocomplete.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 204 | `test_live_answer_is_still_used_once_the_cell_has_run` | Docstring says it confirms hoverDoc calls docFor rather than the Jedi fallback: an implementation path, calling an internal function; reader-visible result is covered by the hover docstring test. | Delete; the run-then-hover docstring test covers the behaviour. |
| 348 | `test_hover_help_waits_two_seconds_unless_changed` | Pins the default delay of two seconds, a design choice with a 1.5 s sleep; the delay setting tests cover the mechanism. | Delete, or assert only that default differs from 0. |

### `tests/e2e/test_cell_run_menu.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 150 | `test_escape_closes_the_menu_and_returns_focus` | Duplicates the cell-run-menu case in test_dismissible_panels, which asserts Escape and focus return for the same menu. | Delete; keep the parametrized case. |
| 270 | `test_declining_leaves_it_running` | Near-duplicate of the decline test in restart-and-run-all; same confirm gate and same weak True substring. | Merge into one parametrized decline test. |

### `tests/e2e/test_compare.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 125 | `test_no_word_on_the_table_judges` | Blocklist of 'right', 'pass', 'fail' enforces house voice (never judge); substring match is also fragile. Nothing breaks for a reader. | Delete; leave to the style guide checklist. |

### `tests/e2e/test_custom_cells.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 137 | `test_a_rendered_text_cells_chrome_is_invisible_until_touched` | Pins a hover-reveal opacity design choice with timing sleeps; touch-screen test covers the real break. | Delete; keep the touch-screen test. |

### `tests/e2e/test_dewmini_workbench.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 349 | `test_the_toolbar_offers_openings_not_a_second_way_to_add_a_cell` | Pins an authorial toolbar design (no add-python or add-text button); blank-cell seam is covered by the empty-notebook test. Imports button check is the only unique part. | Drop; keep a small test that Start-with-imports adds an import cell. |
| 585 | `test_a_web_cells_two_editors_are_both_always_visible` | Pins layout decision (two editors, no preview toggle icon); render and persistence are covered elsewhere. | Drop, or assert only that the HTML area is hidden until rendered. |
| 658 | `test_a_web_cells_chrome_is_also_quiet_until_touched` | Duplicates the text-cell chrome test for opacity on hover; a styling choice, touch reachability is tested separately. | Fold into a parametrised hover-chrome test or drop. |
| 738 | `test_a_run_cell_types_chrome_is_never_hidden` | Pins a styling choice (opacity 1 at rest, no preview icon) rather than something a reader cannot do. | Drop, or assert the run button is clickable on each cell type. |
| 1637 | `test_the_project_is_on_the_left_and_the_reference_on_the_right` | Pins which side each panel sits on, a layout preference; conflict rules and docking are tested separately. | Drop, or assert only that the two panels do not overlap. |
| 1773 | `test_web_defaults_off_sql_and_javascript_default_on` | Pins which cell types ship on by default, an authorial product choice; toggling itself is tested separately. | Drop; the toggle tests already seed state explicitly. |

### `tests/e2e/test_dewminiweb.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 86 | `test_renaming_updates_the_download_filename` | Asserts only a dataset attribute; the actual download filename is covered by the download test. | Fold into the download test or delete. |

### `tests/e2e/test_highlight_colors_and_list.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 130 | `test_a_fresh_highlight_is_amber_with_no_data_attribute` | Default colour is real, but 'no data-highlight-color attribute' pins a CSS implementation detail; the amber state check overlaps other tests. | Keep only the state assertion, folded into the list test; drop the attribute check. |

### `tests/e2e/test_highlight_schema.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 188 | `test_two_dropped_highlights_use_the_plural_wording` | Pins runtime copy verbatim; breaks on a wording edit and guards a house wording choice. The dropped-count behaviour is covered by the single-drop test. |  |

### `tests/e2e/test_map.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 144 | `test_the_message_names_the_first_dozen_problems_and_counts_the_rest` | Name promises a dozen shown, but asserts only loose substrings 'and ' and 'more'. Pins error-message formatting. | Delete, or assert twelve named plus a count. |
| 155 | `test_every_topic_landmark_and_section_exists` | Duplicates the real build, which calls map_data and refuses mismatches. Reads real tutorials and map/graph.json. Body compares counts only, not sections as the docstring says. | Delete; the real build in CI is the check. |
| 170 | `test_the_committed_layout_places_exactly_the_graphs_topics` | build.py map_data already refuses missing and extra layout entries for topics and landmarks, tested in the sandbox tests above. This re-checks real content. | Delete. |
| 206 | `test_a_bridge_is_as_wide_as_the_roads_it_carries` | Stroke width as a cue is a visual design choice; parses title text; nothing breaks if widths are equal. |  |

### `tests/e2e/test_phase0_golden_path.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 37 | `test_the_page_loads_its_shared_assets_rather_than_inlining_them` | Pins an implementation detail (asset filenames linked, not inlined); background check is weak; cites nonexistent DECISIONS.md. A missing stylesheet is caught by smoke tests. | Delete; page_smoke covers load and layout. |

### `tests/e2e/test_reference_panel.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 375 | `test_clicking_outside_does_not_close_a_right_panel_either` | Subsumed by the both-docks click-away test, which covers the right dock as well. | Delete; keep test_both_docks_stay_open_after_a_click_away. |
| 485 | `test_a_note_and_a_glossary_both_appear_with_their_own_headings` | Exact heading list duplicates the grouping test and the Notes case of the panel-heading test. | Fold the Notes ordering into the grouping test. |
| 651 | `test_the_toggle_is_visible_on_a_phone_sized_viewport` | Name says visible but checks hidden attribute only, same as the toggle-shows test; the real phone path is the launcher test. | Delete; launcher tests cover phones. |

### `tests/e2e/test_saved_progress.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 238 | `test_a_short_note_gets_no_marker` | Pins the 120-character threshold, a UX choice; the absence case is already exercised by the write-more-after-export test. |  |
| 245 | `test_a_long_note_gets_a_marker` | Pins the threshold number; presence of the marker is already asserted inside the export-clears and settings-toggle tests. |  |

### `tests/e2e/test_versions.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 236 | `test_the_page_says_which_release_it_is_before_it_talks_about_your_work` | Pins order of two notices (first child block), an authorial layout choice; nothing breaks for a reader if swapped. |  |

### `tests/test_erd_graphics.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 222 | `test_the_marked_amount_appears_more_than_once_in_the_drawing` | Requires the marked amount to repeat so the picture "argues" something: an authorial and pedagogical choice. | Retire. |
| 287 | `test_it_draws_the_numbers_the_page_multiplies` | Asserts the two-aces picture shows 4/52 and 3/51, today's arithmetic copied from a page. | Retire; test_sibling_branches_summing_wrong_stops_generation covers the real invariant. |
| 291 | `test_both_second_draws_are_out_of_the_same_smaller_deck` | Pins denominators 51 and numerators 3 and 4 of one example; duplicates the previous test. | Retire. |
| 349 | `test_the_chosen_target_actually_halves` | Pins which target and list the author picked for the binary search picture; authorial choice copied from the page. | Drop it; keep a generic binary-search step test if wanted. |
| 493 | `test_every_picture_is_placed_on_its_page_with_alt_text` | The build already enforces alt on img tags; the added full-sentence rule is a house style and it reads every real page. | Retire; rely on the build's alt check. |

### `tests/test_tutorial_tools.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 605 | `test_a_bad_query_raises_the_sqlite_error` | Third bad-query test; _query_rows only lets sqlite's own error propagate, already covered by the run_query and _run_sql_cell error tests. Pins nothing a reader sees. | Drop it, or fold into the _query_rows missing-table test. |

## Rehome (47)

Re-home. The aim is sound, but the test reads real content, names today's content, or reads source text. Rewrite it against a synthetic fixture or against behaviour.

### `tests/build/test_courses.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 417 | `test_archived_tutorials_are_built_off_the_route_and_listed_under_archive` | Archiving preserves saved-work addresses (real feature), but the map check needs the real node MIT-1.4 in topics.yaml. Six claims in one test. | Stub TOPIC_DATA with a fixture node and split into archive, listing and map tests. |
| 520 | `test_every_real_tutorial_is_reachable_from_some_group` | Reaching every tutorial from the topics page is sound, but it reads the real tutorials tree and planning yaml; corrected, this is content-dependent. Fails when authors add tutorials. | Test write_topics_page on a fixture; run the real-tree check in check.py or the build. |
| 527 | `test_every_reference_names_a_tutorial_that_actually_exists` | Dangling topic-group reference is a real broken link, but it reads real tutorials and real topic-groups.yaml (corrected from content-independent). Stops at first bad reference. | Move to a fixture test of the loader; keep the real-tree check in the build. |
| 534 | `test_every_group_has_a_key_a_name_an_intro_and_something_in_it` | Key/name/non-blank intro on groups is loader validation, but it reads the real topic-groups.yaml (corrected: content-tied); non-blank intro is partly style. | Run the same validation on a fixture groups file; validate in the loader. |

### `tests/build/test_curriculum.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 121 | `test_a_tutorial_claiming_nothing_gives_a_vertical_tree_of_every_topic_with_none_taught` | Aim sound (needs sit above, bands do not overlap, tree taller than wide) but reads real topics.yaml and names MIT-1.4, MIT-3.6, PRE-1, band labels and copy. | Build a synthetic topics fixture and assert the invariants over it; drop topic codes, labels and colour-key copy. |
| 228 | `test_a_topic_takes_its_strand_and_coverage_from_the_outcome_it_serves` | Real feature (split topic inherits outcome strand and state) but uses real load_topics and outcome MIT-1.4. | Monkeypatch both topics and outcomes to a synthetic set, then assert inheritance. |
| 257 | `test_three_tutorials_one_claiming_a_topic_put_the_map_on_the_tree_page_and_link_the_topic_to_its_section` | Topic-to-section link from covers: is real, but depends on real topics.yaml code MIT-1.4 and the 'How the tutorials relate' copy. | Use a synthetic topics fixture; assert the link and map node count, not the heading text. |
| 291 | `test_a_group_appears_once_its_own_tutorial_is_in_this_build` | Group-appears logic is real but the test reads groups[0] of the real topic-groups.yaml; docstring says real-file checks live elsewhere (corrected: contentDependent). | Write a synthetic topic-groups file and tutorial; assert the group name appears. |
| 332 | `test_ordinary_yaml_and_the_real_curriculum_files_load` | Ordinary-load half is sound; real-file half reads today's planning YAML and duplicates what the build already refuses when it loads them. | Keep the ordinary-YAML assertion; drop the real-file loop or move it to an advisory data check. |

### `tests/build/test_old_addresses.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 66 | `test_the_notebook_and_the_workspace_keep_their_old_addresses` | Aim is sound (old bookmarks keep working) but it greps literal location.replace and meta strings and pins historical filenames, copying real assets. Source-text check. | Follow the stubs: assert each old stub's target file exists, and the offline bundle has no stubs. |

### `tests/build/test_predict_build.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 59 | `test_the_three_ways_of_being_sure_and_the_route_when_not` | data-sure keys feed the runtime; the button wording asserts (curly apostrophe, 'Run it and see') pin copy. | Keep the data-sure asserts; drop the label strings. |

### `tests/build/test_reference_index.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 435 | `test_the_outcomes_claimed_decide_the_subjects_a_term_is_filed_under` | Subject filter is a real feature, but the test names real outcome codes (MIT-1.4, PDP-LO9) and runs against the real tree; comments cite real-corpus counts. Corrected to content-tied. | Stub TOPIC_DATA and use fixture codes; test the prefix-to-subject map directly. |

### `tests/build/test_site.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 56 | `test_the_site_s_pages_and_chrome_are_all_there` | About ten concerns in one test; pins the real home.md byline (names, institutions), dock layout, tab order and retired-feature absences like dewstack. | Split into small tests on a synthetic home.md; keep pages exist and settings panel present; drop byline, dock-order and absence pins. |
| 486 | `test_three_sections_give_the_page_its_own_closed_rung_and_one_section_gets_none` | Contents links to sections are real, but 'starts closed', the '3 sections' label and the one-section rule pin UI design choices. | Keep: rung links resolve to existing heading ids. Drop closed-state, count-label and single-section assertions. |
| 512 | `test_sub_headings_nest_and_a_repeated_one_is_left_out_while_a_distinct_one_is_kept` | Nesting is real, but omitting a repeated 'Your turn' heading encodes a house heading habit; docstring says five entries, body has two (corrected). | Test nesting and de-duplication using generic repeated headings; drop the 'Your turn' wording. |

### `tests/e2e/test_contrast.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 225 | `test_a_cell_type_pill` | Compares pill text to the page background but reads and ignores the pill own background, so wrong pairing. | Measure pill text against the pill own background colour. |

### `tests/e2e/test_dewmini_workbench.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 272 | `test_the_reference_offers_subject_and_level_up_front` | Asserts chip labels Maths and Computing, which come from the real planning/curriculum outcomes.yaml. Curriculum edits would fail it, not the filter. | Copy a synthetic curriculum into the fixture site and assert its own subject names. |

### `tests/e2e/test_editor.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 206 | `test_a_new_tutorial_starts_from_the_house_template_and_carries_only_what_is_its_own` | Real aim (new tutorial has only its own fields, course line added) but pins '## Reflection' and the year from today's house template, and absent retired fields. | Assert template parity with the editor's template constant, and keep the course-order and no-extra-field checks. |

### `tests/e2e/test_highlight_anchoring.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 143 | `test_lists_the_fixtures_paragraphs_in_reading_order` | Order check is sound but the fixed total of 15 blocks pins runtime chrome (feedback paragraph, practice heading) and breaks when chrome changes. | Drop the length assertion; assert fixture paragraphs appear in order. |

### `tests/e2e/test_loading_data.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 65 | `test_a_live_source_that_answers_is_used_and_shaped` | Live fetch with mocked network is sound, but it copies the real data/ dir and pins the snapshot date '26 September 2026' and Our World in Data wording. | Use a synthetic dataset and recipe in the fixture with its own snapshot date, or read the date from its yaml. |
| 73 | `test_a_live_source_that_fails_gives_the_saved_copy` | Fallback-to-saved-copy behaviour is real, but it pins the real data file's date and note wording; a data refresh breaks it. | Fixture dataset with fixed date; derive expected date from the dataset yaml. |
| 82 | `test_a_dataset_with_no_live_source_says_which_copy` | Says which copy loaded is a real feature; asserts the exact note with the real book's snapshot date. | Use a fixture dataset; compare against the date in its yaml instead of a literal. |

### `tests/e2e/test_map.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 162 | `test_every_region_is_on_exactly_one_continent_and_every_district_in_a_region` | Graph shape rules are sound, but this reads the real map/graph.json. Facts record corrected: reads graph only, not tutorials. | Run the same assertions on the fixture graph, or move into map_data as a refusal. |

### `tests/e2e/test_page_smoke.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 155 | `test_a_page_loads_with_no_console_errors` | Sound smoke check, but the fixture builds from the real pages/ directory and real planning data, and lists real page names. Facts record was wrong: not purely synthetic. | Build from a synthetic pages directory and topics data; derive the page list from the build output. |
| 172 | `test_a_page_never_scrolls_sideways_on_a_phone` | Phone overflow is a real reader break, but it measures real pages/ content and hard-coded real page names. Facts record was wrong: not purely synthetic. | Use synthetic pages with long words and wide elements; take the page list from the build. |

### `tests/e2e/test_panel_resize_drag.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 150 | `test_the_other_two_panels_share_the_width_mid_drag` | Compares inline style strings, so two empty strings pass; never asserts the drag changed anything. Real feature, vacuous check. | Assert measured widths of the opened panels are equal and larger than before the drag. |

### `tests/e2e/test_reference_panel.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 189 | `test_no_glossary_anywhere_in_the_series_still_shows_the_basics_tabs` | Feature is real, but basics panes read the real planning/curriculum yaml; only count>0 is asserted, so it depends on content tree existing. | Point basics data at a tiny fixture yaml via monkeypatch and assert its entries render. |

### `tests/e2e/test_saved_progress.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 77 | `test_the_record_carries_the_page_version_and_slug` | Pins literal fixture slug and version and the legacy tutorial-slug key; reader sees nothing. Real aim is that the record carries id and version the page declares. | Compare record tutorial-id and tutorial-version with the page meta values instead of literals. |
| 149 | `test_it_says_so_rather_than_claiming_a_normal_save` | Aim is a truthful status on quota failure, but asserts two exact wording fragments, so rewording fails it with no behaviour change. | Assert the state element changed to a warning class or differs from the normal-save text. |
| 160 | `test_a_reload_shows_no_output_for_the_dropped_cell` | Empty output passes for any reason, including the cell never saved; does not prove the dropped-output path. | Also assert the cell's code restored on reload, so the save is shown to have happened. |
| 325 | `test_the_summary_line_tracks_runs_as_they_happen` | A stated count must be right, but asserts are weak substrings ('of', 'cells run') and rely on a fixture traceback cell and Pyodide. | Assert exact '1 of N cells run' text computed from the page's cell count. |
| 619 | `test_it_never_starts_python` | Performance property invisible to a reader, checked with a fixed 1500 ms wait that can pass before a late request. | Wait for network idle, then assert no pyodide request. |
| 630 | `test_its_mathematics_still_renders` | Real reader concern (equations render) but misfiled in a saved-progress file and satisfied by any one formula. | Move to a rendering test file; check every dl-math block rendered. |
| 706 | `test_a_mismatched_file_leaves_the_existing_record_alone` | Tautological: the guarded write lives inside the test's own evaluate, not the app's import path, so it passes even if real import overwrites. | Drive the real import control with a mismatched file and assert the stored record is unchanged. |

### `tests/e2e/test_slider.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 95 | `test_reset_empties_the_strip_with_the_output` | Skips if no reset button, and asserts .dl-slider inside the strip, which the first test shows is never there, so it passes vacuously. | Assert the strip has no input[type=range] after reset; fail rather than skip when the button is missing. |

### `tests/test_curriculum_map.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 262 | `test_the_map_says_how_many_gaps_nobody_has_planned` | Aim is sound (unplanned_line wording) but it computes inputs from real planning data and has an early return that skips assertions. | Call unplanned_line with fixture states and proposals; assert the count appears. |
| 279 | `test_unplanned_line_edge_cases` | Tests unplanned_line behaviour but takes its outcome codes from real outcomes.yaml. | Use the fixture repo outcomes instead of load_outcomes on the real tree. |
| 360 | `test_prerequisites_are_real_and_not_self_referential` | Sound aim, but build.py drops unknown needs silently, so only self-reference matters; it reads real topics.yaml. | Move the check into a topics validator, tested with a fixture file. |
| 368 | `test_the_prerequisites_have_no_cycles` | A cycle could break the topic tree tiers, a real fault; but it walks the real topics.yaml, passing trivially if emptied. | Extract the walk into a function; test it on a fixture with and without a cycle. |
| 385 | `test_every_topic_has_a_name_and_a_description` | The topic tree displays both fields, so blank ones show; but it reads real topics.yaml only. | Test the topic loader against a fixture with a missing name or plain. |

### `tests/test_erd_graphics.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 212 | `test_counts_are_taken_over_the_drawn_depth_not_the_whole_recursion` | Counting logic is sound, but uses the make-change 6 with coins 1,3,4 example from a page. | Use a small synthetic recursion tree as input. |
| 266 | `test_the_matrix_is_read_from_the_tutorial_not_restated` | Reads the where-chains-lead page and pins its weather matrix; fails when the author edits numbers, not when the reader-facing code breaks. | Test _matrix_from_cell on a fixture page; leave the picture-staleness check to the committed-picture test. |
| 324 | `test_it_draws_the_matrices_the_tutorial_defines` | Reads multiplying-grids cell and pins its A and B; the fixture constants duplicate the content. | Test _matrices_from_cell on a fixture page. |
| 375 | `test_the_list_comes_from_the_tutorial` | Reads the finding-things page and pins its sorted list to a copy in the test. | Test _search_case on a fixture page. |
| 387 | `test_the_sets_come_from_the_tutorial` | Reads the sets page and pins its two lists to a copy in the test. | Test _sets_from_cell on a fixture page. |
| 393 | `test_every_comparison_case_appears` | Merge picture should show each comparison case, but it uses the page's own sets. | Use a tiny synthetic pair of lists that hit all three cases. |

### `tests/test_tutorial_tools.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 1485 | `test_its_three_cases` | Real behaviour (three provenance cases, days-ago count) but asserts four whole sentences of reader copy, so any rewording fails it. | Assert source name, snapshot date and days-ago figure appear, not the exact sentences. |

## Advisory (19)

Advisory. A house preference or a planning or generated file the build does not consume. Report it; never block on it.

### `tests/build/test_courses.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 316 | `test_a_repeated_title_is_warned_about_naming_both_and_their_courses` | Duplicate-title warning is console-only authoring hygiene, never fails the build, and asserts exact stderr wording and paths. | Mark advisory; assert only that a warning is printed and the build succeeds. |
| 326 | `test_tutorials_covering_the_same_outcomes_are_reported` | Outcome-overlap note is a planning report for authors that no reader sees; asserts exact stderr text and a weak 'three' check. | Mark advisory; assert on the reported pair, not wording. |

### `tests/build/test_templates.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 52 | `test_every_template_builds` | Templates are never published and the build does not consume them in production; failure hurts authors, not readers. Names real template slugs. | Mark advisory; derive slugs from the templates folder rather than a hard-coded list. |
| 60 | `test_every_world_variant_has_its_own_cell_id` | Checks template source text for the world-suffix id rule; the build already enforces that for real pages, so this guards only docs examples. | Mark advisory, or drop since build already refuses it. |
| 76 | `test_the_templates_readme_names_every_template` | Documentation index check on a planning-style file the build does not consume. | Mark advisory. |

### `tests/build/test_tutorial.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 783 | `test_the_stylesheet_defines_both` | Reads real tutorial-style.css; a missing fold rule leaves a plain browser triangle that still opens (7.295 made that non-blocking). Docstring says both, loop covers all four classes. | Move to advisory marker; or check the built site's css selectors instead of substring-matching source. |

### `tests/test_curriculum_map.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 108 | `test_every_declared_section_in_the_real_tutorials_exists` | Reads every real tutorial to check the planning map anchors; a stale map misleads nobody reading the site. | Mark advisory; test the anchor check with the fixture repo already used above. |
| 226 | `test_it_is_committed_current` | Generated planning file compared with the real tutorials; already marked advisory, correctly. |  |
| 230 | `test_every_out_of_scope_code_is_a_real_outcome` | Cross-checks two planning yaml files; no page reads it. Unmarked, so it blocks a PR over housekeeping. | Add pytest.mark.advisory. |
| 236 | `test_every_proposal_is_well_formed` | Planning proposals and outlines are not consumed by the build; a dangling reference is tidying, yet this is unmarked. | Add pytest.mark.advisory. |
| 247 | `test_a_proposal_never_claims_something_already_taught` | Planning housekeeping against real tutorials; already marked advisory. |  |
| 296 | `test_the_outlines_index_lists_every_outline` | Housekeeping on planning/outlines that no page reads; already advisory. |  |
| 317 | `test_every_outcome_has_a_topic` | Completeness of the plan in real planning data; already advisory. |  |
| 326 | `test_no_topic_invents_an_outcome` | Cross-references two real planning files. The build ignores unknown claims, so no reader breaks. Unmarked. | Add pytest.mark.advisory, or rehome as a validator test on a fixture topics file. |
| 340 | `test_a_groundwork_code_never_collides_with_an_outcome` | Naming convention check on real topics.yaml and outcomes; nothing a reader sees breaks. | Add pytest.mark.advisory. |
| 351 | `test_groundwork_is_written_up_like_a_topic` | Editorial completeness of real topics; already advisory. Also pins that a PRE- topic must exist. |  |
| 393 | `test_every_topic_says_what_it_is_and_where_it_is_used` | Description length and style are editorial; already advisory. |  |
| 414 | `test_the_sequence_graph_has_no_repeated_node` | Checks the committed generated map for repeated nodes; a regression test for a bug in render(), unmarked. Planning file only. | Assert on render() output from a fixture with two series; mark advisory meanwhile. |
| 430 | `test_no_tutorial_mentions_a_skills_demo` | House preference about prose, greps every real tutorial; already advisory. Candidate for outright retirement as an unchecked habit. | Consider retiring; style is meant to be unchecked. |

## Wire Up (89)

Wire up. Guards something a reader depends on (saved work, ids, data, safety) but does not run in CI.

### `tests/e2e/test_app_cell_live.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 115 | `test_saved_progress_restores_the_edited_panes_and_reruns_if_it_had_run` | Edited app panes restored from saved work and re-run; saved-work behaviour readers depend on, but local-only. | Run test_app_cell_live.py in CI or add a saved-progress app case to a CI file. |

### `tests/e2e/test_cell_hints_staged.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 91 | `test_a_reload_keeps_what_was_shown` | Revealed hints and counters persist in saved work across reload; a real saved-state contract, but local-only. | Run test_cell_hints_staged.py in CI, or move this one into a CI file. |

### `tests/e2e/test_cell_report.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 75 | `test_links_carry_page_version_and_this_cell` | Report links must carry page, cell and template or reports reach nobody useful; reader-facing door, but local-only. Names 'rendering-tour' fixture slug. | Add test_cell_report.py to CI; use the fixture slug from a constant. |

### `tests/e2e/test_cell_run_menu.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 112 | `test_run_above_runs_this_cell_and_everything_before_it_only` | Run above is a core run-control; asserts earlier cells ran and later did not. Fixture cell ids and output strings. | Add to CI browser job. |
| 124 | `test_run_below_keeps_earlier_state_and_does_not_reset_the_namespace` | Run below must keep namespace; losing variables breaks later cells. Waits on tools-widgets but asserts only numpy output. | Assert the plain-python marker survives; run in CI. |
| 201 | `test_restart_and_run_all_from_settings` | Restart & run all is a core control; failure leaves stale or missing outputs. Fixture cells and strings. | Add to CI browser job. |

### `tests/e2e/test_compare.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 156 | `test_a_guess_is_saved_with_the_cell_and_comes_back` | Typed guesses are saved student work; asserts the saved-state shape; local-only. | Include test_compare.py in the CI browser job. |

### `tests/e2e/test_contrast.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 187 | `test_the_link_colour` | Real readability failure on fixture, both schemes; never runs in CI. | Add test_contrast.py to the CI browser job. |
| 201 | `test_a_heading` | Heading contrast is reader-visible; measures only the first h2. Local only. | Add test_contrast.py to the CI browser job. |
| 211 | `test_the_crumbs_label` | Docstring promises course and tree pages too, but only all-tutorials is measured. Local only. | Measure the crumbs on course and tree pages too; run in CI. |
| 245 | `test_a_highlight_colour` | Mark text against its own mark background for four colours and both schemes; real readability. Local only. | Run in CI browser job. |

### `tests/e2e/test_custom_cells.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 104 | `test_typing_autosaves_under_its_own_key_not_the_tutorials` | Custom cell autosave and separate storage key protect reader work; custom cells only tested in this local file. | Run custom-cell persistence tests in CI. |
| 201 | `test_inserting_editing_running_and_reloading_all_stick` | Full custom-cell lifecycle including reload and anchor; reader work at stake. Local only. | Run in CI. |
| 252 | `test_an_orphaned_anchor_falls_back_to_the_trailing_section` | Custom cell must not be dropped when anchor vanishes; reader work preserved. Local only. | Run in CI. |
| 329 | `test_loading_a_shared_cell_always_gets_a_fresh_id_and_keeps_its_type` | Fresh id on import protects id keys and avoids collisions; saved-work contract. Local only. | Run in CI. |
| 396 | `test_ipynb_export_includes_real_and_custom_cells_in_document_order` | Export of notebook is a reader deliverable; despite name, no document-order assertion, only any code cell present. | Assert order, or rename; run in CI. |
| 487 | `test_neither_the_section_nor_the_settings_entry_appear` | Builds its own prose-only site and needs no Pyodide boot, so it could run in CI; guards custom-cells UI absence. | Move to a CI-run file. |

### `tests/e2e/test_dewmini_workbench.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 105 | `test_notebooks_survive_a_reload` | Saved notebooks are students' work; test only counts tabs after reload, not cell contents. Never runs in CI. | Assert cell text survives reload, and run one dewmini persistence test in the browser job. |
| 115 | `test_work_saved_before_tabs_is_migrated` | Legacy-save migration protects work already saved in readers' browsers; losing it is silent data loss. Not run in CI. | Add to a CI-run browser file or a small dewmini smoke job. |
| 595 | `test_a_web_cells_html_renders_in_a_sandboxed_iframe` | Asserts the iframe sandbox is exactly allow-scripts: a security contract for shared notebooks, yet never runs in CI. | Run this and the parent-escape test in the browser job. |
| 604 | `test_a_web_cells_script_cannot_reach_the_parent_page` | Real security boundary, but assertion is weak: a 300ms wait then a title check, so a slow escape would pass. Local only. | Probe with a postMessage or localStorage read and wait for the frame; run in CI. |
| 944 | `test_a_full_storage_keeps_the_code_and_says_what_it_dropped` | Full-storage handling stops silent loss of student work and pins the message; important enough to run in CI. | Run in CI; assert the notice is visible rather than matching its wording. |
| 1346 | `test_html_output_from_an_imported_notebook_cannot_bring_anything_active` | Imported ipynb HTML must be inert (no script, img, anchor); protects readers opening foreign files. Never run in CI. | Run in the browser job with the other sandbox tests. |

### `tests/e2e/test_dewminiweb.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 94 | `test_switching_sites_keeps_each_ones_own_edits` | Per-site edits lost on switch is data loss for the reader; source-tree page, not content. | Add Workspace tests to CI browser job. |
| 167 | `test_undo_after_switching_sites_cannot_bring_back_the_other_sites_code` | Ctrl+Z restoring another site leaks code between sites: data corruption. Careful timing in the test. | Add to CI browser job. |
| 231 | `test_delete_removes_the_site_on_screen_even_if_the_saved_open_id_is_stale` | Deleting the wrong site loses work; exercises a stale-state recovery path with raw localStorage seeding. | Add to CI browser job. |
| 253 | `test_a_downloaded_page_links_its_css_and_js_and_loads_back` | Download and round-trip are the Workspace output readers keep; real feature, only starter h1 text is incidental. | Add to CI browser job. |

### `tests/e2e/test_dismissible_panels.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 261 | `test_escape_closes_it` | Keyboard dismissal of ten panels is an accessibility feature on a synthetic site; focus-return cases pin current wiring, not necessarily intent. | Run in CI; keep focus asserts only where contract is stated. |

### `tests/e2e/test_editor.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 257 | `test_renaming_a_cell_id_warns_that_student_work_is_orphaned_and_that_releasing_is_the_way_not_to` | Cell-id rename warning guards the saved-work id contract and nothing else in the editor does; local-only, so a regression ships silently. | Run test_editor.py's id-warning and report tests in the browser CI job, or move to a unit test of the editor module. |
| 278 | `test_the_report_surfaces_a_problem_before_it_reaches_the_build` | Editor report must draw cell and fence lines where build.py does (unclosed, duplicate, missing id); catches ids problems before a PR. Not run in CI. | Add test_editor.py to the CI browser job, or test the report function directly in Node. |
| 510 | `test_a_reorder_commits_the_course_file_opens_a_pr_on_a_new_branch_and_goes_quiet` | Committing only the course file, on an editor/ branch, never main, with other lines intact; a wrong commit damages the repo. Not run in CI. | Run in CI, or test the commit-building function with a fake client in Node. |
| 531 | `test_an_insertion_commits_both_the_tutorial_and_the_course_file` | Insert must commit tutorial and course file together or the repo describes a course that does not exist. Not run in CI. | Run in CI, or unit-test the commit builder. |
| 723 | `test_releasing_adds_a_frozen_copy_of_what_students_have_and_a_new_release_of_the_edits` | Release must freeze the version students have and write the edits as a new version; this protects saved-work ids. Not run in CI. | Run in CI, or unit-test the release builder on a fake client. |
| 752 | `test_releasing_a_folder_writes_only_the_new_release` | Release of a versioned folder must write one new file and touch no frozen file; guards students' frozen versions. Not run in CI. | Run in CI, or unit-test the release builder. |

### `tests/e2e/test_highlight_anchoring.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 192 | `test_locates_the_anchor_at_the_right_occurrence` | Highlights are readers saved work; wrong occurrence moves them. Expected index recomputed with same indexOf logic. Local only. | Run in CI browser job; hard-code expected offsets. |
| 217 | `test_search_window_follows_a_moved_paragraph_until_the_move_is_too_big` | Highlights surviving tutorial edits matters to readers; hard-codes the plus-or-minus-five window, but window is the stated contract. Local only. | Run in CI browser job. |
| 262 | `test_gives_up_when_the_quote_itself_is_gone` | Prevents highlight attaching to unrelated text; local only. Replaces textContent so markup-preserving rewrite untested. | Run in CI browser job. |

### `tests/e2e/test_highlight_colors_and_list.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 148 | `test_the_choice_is_saved_and_survives_a_reload` | Highlight colour persistence is saved-work behaviour on a synthetic fixture; CI never runs it. | Include the highlight file in the CI browser job. |
| 306 | `test_every_new_colour_meets_aa_against_its_own_background` | Real contrast check on computed styles, six combos; a reader-facing accessibility fault, but local only. | Run in CI browser job; keep the WCAG maths as is. |

### `tests/e2e/test_highlight_creation.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 190 | `test_click_creates_saves_and_the_mark_survives_a_reload` | Student highlights lost on reload is lost saved work, yet this never runs in CI. Fixture-based and sound. | Add test_highlight_creation.py to the CI browser job. |

### `tests/e2e/test_highlight_popover.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 145 | `test_typing_a_note_and_saving_persists_it_and_shows_it_on_reopen` | Highlights and notes are saved student work; no Pyodide needed, so cheap, yet never runs in CI. | Add test_highlight_popover.py to the CI browser job. |
| 178 | `test_confirmation_gates_removal_of_a_highlight_with_a_note` | Guards against losing a student's note; fast, content-free, but local-only. | Add test_highlight_popover.py to the CI browser job. |

### `tests/e2e/test_highlight_schema.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 125 | `test_a_highlight_round_trips_and_a_successful_restore_stays_silent` | Round trip of highlight id and note through saved progress is a saved-work contract. Never runs in CI. | Add test_highlight_schema.py to the CI browser job. |
| 152 | `test_a_dropped_highlight_keeps_its_note_and_is_reported_in_the_restore_summary` | Note surviving a dropped anchor protects saved work; restore notice is reader-visible. Local only. Pins 'could not be put back' substring. | Add to CI; assert the notice exists without matching wording. |

### `tests/e2e/test_highlight_wrapping.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 165 | `test_builds_a_range_that_wraps_the_same_text_describe_quote_saw` | Wrong offsets-to-range mapping puts a restored highlight on the wrong words. Real, fixture-based, never run in CI. | Add test_highlight_wrapping.py to the CI browser job. |
| 182 | `test_a_restored_highlight_appears_as_a_visible_mark` | Saved highlight must reappear after reload; name says visible but only checks existence and text. Local only. | Add to CI; assert the mark has nonzero size. |

### `tests/e2e/test_input.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 64 | `test_the_box_appears_after_the_prompt_and_enter_sends_the_line` | input() answer box is core to running cells; needs Pyodide and isolation, so only local, and a regression leaves cells hanging. | Run test_input.py in the CI browser job, or its hosted-input tests. |
| 99 | `test_stop_ends_the_wait` | A reader stuck on an input wait must be able to Stop and rerun; real contract, local-only. | Include in CI browser job with the other input tests. |

### `tests/e2e/test_loading_data.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 119 | `test_a_downloaded_copy_with_no_network_uses_what_it_carries` | Offline download must carry its data: a reader's page breaks otherwise. Local-only, and pins the real data files and dates. | Use fixture datasets, and run in CI if the download is a supported route. |

### `tests/e2e/test_my_notes.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 137 | `test_highlights_from_two_tutorials_both_appear` | All-notes page gathers readers own highlights across tutorials; local only. Pages not closed on failure. | Run in CI browser job; close pages in try/finally. |
| 226 | `test_the_download_button_offers_a_text_file` | Download is a reader backup of their own notes; checks filename and three substrings. Local only. | Run in CI browser job. |

### `tests/e2e/test_my_words.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 268 | `test_the_list_survives_a_reload` | Saved words vanishing on reload loses reader data; fixture-based, but local only. | Include test_my_words.py in the CI browser job. |
| 354 | `test_imported_text_is_never_read_as_markup` | Escaping of imported text is a script-injection guard on a real feature; runs on a synthetic fixture, but CI never runs this file. | Add test_my_words.py (prose-only, no Pyodide) to the CI browser job, or move this test into a CI file. |

### `tests/e2e/test_old_compose_addresses.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 44 | `test_an_old_address_opens_the_new_page_keeping_its_query_and_hash` | Teacher bookmarks to moved Notebook/Workspace pages must work; reads compose/ source not content, but file never runs in CI. Parametrised, 2 cases. | Add the file to the CI browser job. |
| 65 | `test_an_old_address_still_opens_the_new_page_without_javascript` | No-JS meta-refresh fallback for old bookmarks is real reader behaviour, but local-only. Parametrised, 2 cases. | Add the file to the CI browser job. |

### `tests/e2e/test_phase0_golden_path.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 64 | `test_python_started_with_no_console_errors` | Pyodide boot with no errors is what a reader depends on; CI smoke only checks page loads without errors, not boot in this file. | Run the golden-path file, or one boot test, in the browser job. |
| 70 | `test_plain_cell_prints_and_shows_its_last_expression` | Core promise: a cell runs and shows output. Uses synthetic fixture. Never runs in CI. | Include the cell-run basics in a CI browser job. |
| 83 | `test_a_sql_cells_select_renders_as_a_table_and_a_python_cell_can_read_it` | SQL cell rendering and shared db with Python is a real runtime feature; only runs locally. | Run in CI with the cell-run basics. |
| 197 | `test_a_site_editors_edit_survives_a_reload` | Reader's typed work surviving reload is saved-work behaviour; local-only. | Run in CI alongside saved-progress tests. |
| 217 | `test_matplotlib_renders_a_figure_without_leaking_its_repr` | Figure must render as a real image; reader sees broken plot otherwise. Local only. | Include in CI cell-run job. |
| 261 | `test_an_error_shows_the_students_line_and_does_not_stop_the_page` | Error display and page survival is core reader experience; asserts internal frame names absent. Local only. | Run in CI cell-run job. |

### `tests/e2e/test_predict.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 128 | `test_a_prediction_is_saved_with_its_cell_and_comes_back` | Prediction persisted in saved work and restored on reload: reader data at stake, yet file never runs in CI. | Add test_predict.py to the CI browser job, or fold this save/restore check into test_page_smoke. |

### `tests/e2e/test_question_interaction.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 154 | `test_a_choice_and_the_asking_survive_a_reload` | Reader's saved answers must survive reload; saved-work behaviour, fast, no Pyodide, but local-only. | Run test_question_interaction.py in the CI browser job. |

### `tests/e2e/test_saved_progress.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 66 | `test_typing_is_saved_without_being_asked` | Core saved-work promise: typed code reaches storage. Losing it costs a student their work; only runs locally, never in CI. | Run in the CI browser job, or fold into a short saved-work smoke test there. |
| 85 | `test_work_comes_back_after_a_reload` | Restore after reload is the saved-work feature itself; failure silently loses a reader's code. Not run in CI. | Include in the CI browser job. |
| 184 | `test_a_note_comes_back_after_a_reload` | A student's notes vanishing on reload is reader harm, and nothing in CI would catch it. | Include in the CI browser job. |
| 507 | `test_an_edited_tutorial_restores_anyway_and_says_so` | Restoring after a tutorial edit is a core saved-work path; seeds legacy slug key, literal versions are fixture values. Not in CI. | Seed tutorial-id too, and run in CI. |
| 536 | `test_a_saved_cell_that_no_longer_exists_is_reported_not_discarded` | Orphaned saved cells being reported is what protects students when ids change; the id contract depends on it. Not in CI. | Run in CI; assert the orphan survives in the record. |
| 639 | `test_saved_work_is_keyed_on_the_tutorials_id` | The progress key is the id contract students' work lives under; it runs nowhere in CI. Hard-codes the prefix, which is the point. | Run in CI; also assert the key against the fixture's known folder name. |

### `tests/e2e/test_stop_button.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 31 | `test_stopping_an_infinite_loop_then_running_the_cell_again` | A reader stuck in an infinite loop needs Stop to work and the cell to run again; fixture-based but never runs in CI. Cell id is a fixture's. | Run in CI, or add to the browser job's file list. |

### `tests/e2e/test_student_notes_prose_only.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 85 | `test_the_work_section_notes_field_and_autosave_survive_zero_cells` | Notes on a cell-less tutorial must show and autosave or students lose notes. Uses a synthetic build, content independent; local-only. | Run test_student_notes_prose_only.py in the CI browser job. |

### `tests/e2e/test_toolkit.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 222 | `test_with_nothing_saved_the_reference_is_loaded` | Real toolkit fallback on a synthetic course; wrong function version or stray print reaches the reader. Not run in CI, needs Pyodide. | Run in a CI job with dev/pyodide cached. |
| 238 | `test_the_readers_saved_version_is_loaded_function_by_function` | Per-function choice between reader code and reference decides what runs; synthetic fixture, real feature. | Add to CI browser job. |
| 247 | `test_an_untouched_stub_counts_as_not_written` | Untouched stub must not count as reader work; otherwise reader gets empty functions. Synthetic fixture. | Add to CI browser job. |
| 257 | `test_a_saved_version_that_raises_falls_back_and_the_line_says_so` | Fallback on raising saved code is real behaviour; exact error wording is copy, assert only that a message appears. | Loosen exact sentence match; run in CI. |
| 264 | `test_switching_to_reference_loads_the_reference_at_once` | Mode switch changes what runs: real feature. The localStorage key assertion is an implementation detail. | Drop the key check or assert via reload; run in CI. |
| 280 | `test_the_toolkit_survives_run_all_and_a_restart` | Toolkit must survive Run above and Restart & run all, or reader code vanishes mid-session. Synthetic fixture. | Add to CI browser job. |

### `tests/e2e/test_versions.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 117 | `test_it_counts_the_answers_that_carry_over_and_says_where_the_rest_went` | Carry-over count tells readers what happens to saved work; wording exact-match, fixture-based. Local only, never in CI. | Add test_versions.py to the CI browser job. |
| 133 | `test_an_untouched_starter_is_not_an_answer` | Wrong counts mislead readers about saved work; fixture-based but never runs in CI. | Add to CI browser job with the rest of test_versions.py. |
| 157 | `test_choosing_a_release_takes_them_there_and_that_is_where_the_plain_url_takes_them_next_time` | Redirect to the release a reader chose; wrong release means wrong cells and saved work. Local only. | Run test_versions.py in the CI browser job. |
| 170 | `test_work_saved_against_a_release_is_enough_on_its_own` | Saved-record redirect keeps returning readers on the release their work belongs to. Never runs in CI. | Run test_versions.py in the CI browser job. |
| 178 | `test_it_never_sends_them_away_from_a_release_they_asked_for` | Explicit release links must not be overridden; real reader breakage, fixture-based, local only. | Run test_versions.py in the CI browser job. |
| 225 | `test_an_answer_with_nowhere_to_go_is_not_called_lost` | Telling a reader saved work is lost when it is not is a real harm; copy-matching but fixture-based. Local only. | Run in CI browser job; match on the notice element, not its wording. |

### `tests/e2e/test_worlds.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 64 | `test_choosing_swaps_the_variants_and_is_remembered_for_the_page` | World choice and persistence govern which cell ids hold saved work; id contract; local-only. | Add test_worlds.py to the CI browser job. |
| 86 | `test_each_world_keeps_its_own_work` | Work per world variant is saved under world-suffixed ids, the id contract; local-only. | Add test_worlds.py to the CI browser job. |

### `tests/test_erd_graphics.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 434 | `test_the_committed_picture_is_what_the_generator_draws` | Guards that pictures on pages match the page cells; real reader risk (picture disagrees with numbers), yet skipped in CI without svgwrite. | Install svgwrite in CI or compare against the generator in a separate job. |
| 440 | `test_colours_are_theme_tokens_and_nothing_has_an_id` | Literal colours break dark mode and duplicate ids collide when inlined; it only reads committed SVGs, yet is skipped in CI via the module gate. | Remove the svgwrite gate from this check so it runs in CI. |
| 472 | `test_the_committed_picture_is_what_the_generator_draws` | Guards that pictures on pages match the page cells; real reader risk (picture disagrees with numbers), yet skipped in CI without svgwrite. | Install svgwrite in CI or compare against the generator in a separate job. |
| 478 | `test_colours_are_theme_tokens_and_nothing_has_an_id` | Literal colours break dark mode and duplicate ids collide when inlined; it only reads committed SVGs, yet is skipped in CI via the module gate. | Remove the svgwrite gate from this check so it runs in CI. |

## Question (1)

Question. Cannot be decided from the code; the owner decides.

### `tests/build/test_courses.py`

| Line | Test | Why | Fix |
|---|---|---|---|
| 152 | `test_a_practice_page_listed_in_a_course_stops_the_build` | Listing a practice page in a course still yields a working page; the refusal enforces an authorial structure. Owner must say whether it should block or warn. | If it need not block, turn it into a warning and test the warning. |

## Refusals that should be notes (51)

Places where `build.py` or `check.py` stops an author although the page would load and work. `check.py` must agree with the build (`tests/build/test_check.py`), so each pair changes together.

| File | Line | Refuses when | Why a note | Covered by |
|---|---|---|---|---|
| build.py | 805 | A field that moved out of frontmatter is still present in it. | A stale moved field is ignored by the page; it loads and works. Tell the author to delete it, do not stop the build. | tests/build/test_courses.py::test_a_moved_frontmatter_field_stops_the_build_and_says_to_delete_it |
| build.py | 1002 | Choice prediction offers fewer than two options. | A one-option choice works; whether two or more are needed is the author's intent, not breakage. | tests/build/test_predict_build.py::TestMistakes::test_the_build_says_what_is_wrong |
| build.py | 1008 | A tolerance line appears on a prediction whose type is not number. | A tolerance on a non-number prediction is ignored; the page works, the author probably forgot type: number. | tests/build/test_predict_build.py::TestMistakes::test_the_build_says_what_is_wrong |
| build.py | 1174 | An after: term has a count below one. | A zero or negative count is odd but the page works; the runtime behaviour is a timing choice. |  |
| build.py | 1574 | A question's text has a closing brace with no opening brace before it. | A stray closing brace is just a literal character in prose; the question still answers. Note it, do not stop. | tests/build/test_questions.py::test_a_missing_or_unclosed_gap_fails_the_build |
| build.py | 1611 | A multiple-choice question has options but no prompt text above them. | Options with no prompt in the fence may be deliberate when the question is asked in prose above; still answerable. | tests/build/test_questions.py::test_a_broken_correct_line_or_option_count_fails_the_build |
| build.py | 1613 | A multiple-choice question has fewer than two options. | One option is a weak question but loads and works; whether it is a real choice is authorial intent. | tests/build/test_questions.py::test_a_broken_correct_line_or_option_count_fails_the_build |
| build.py | 1761 | A world's description line is missing or blank. | A world with no description line gets a blank label; page loads and switches. Label wording is an authoring choice. |  |
| build.py | 1844 | A project lacks one of title, question, make, maths or data. | A project missing maths or data (say a non-maths project) still loads; the card or table cell is just empty. Which fields to show is a house shape. | tests/build/test_projects_build.py::test_the_build_says_what_is_wrong |
| build.py | 1852 | More than one project is marked own: true. | Two own projects only changes how many wide cards the grid draws; page works. Layout preference. | tests/build/test_projects_build.py::test_the_build_says_what_is_wrong |
| build.py | 1854 | The own: true project is not the last one listed. | Own project not last just places a wide card out of order; a layout preference, not a break. | tests/build/test_projects_build.py::test_the_build_says_what_is_wrong |
| build.py | 1896 | Project divs are not in the same order that projects: lists them. | Project sections in a different order from the cards still load and link correctly; ordering is presentation. | tests/build/test_projects_build.py::test_the_build_says_what_is_wrong |
| build.py | 1900 | A project's body does not open with a ## heading. | Body without a ## heading still shows and converts; the heading only supplies the open-and-close label. Authorial shape. | tests/build/test_projects_build.py::test_the_build_says_what_is_wrong |
| build.py | 3193 | order lists a course id with no matching courses/<id>.yaml file. | Downstream code already skips unknown names in order (c in found), so nothing breaks; a typo just omits an ordering hint. Changing it means updating test_courses. | tests/build/test_courses.py::test_an_index_naming_a_course_with_no_file_stops_the_build |
| build.py | 3237 | The same tutorial id is listed under two series. | Placements already support several entries; a tutorial in two series still builds and navigates. House habit of one place per course. Parity: check.py and the twice test must change too. | tests/build/test_courses.py::test_an_id_listed_twice_in_one_course_stops_the_build; tests/build/test_check.py::test_everything_check_calls_a_problem_the_build_also_refuses[a course listing an id twice] |
| build.py | 3248 | A tutorial id is listed under mixed and also under a series. | Both placements are accepted by the placement code; whether the page then reads sensibly is an authorial question. Leaning house shape. |  |
| build.py | 3311 | (warning, not a refusal) A series lists a tutorial id that has a folder but is not in the registry (a draft). | Already a printed note that carries on; correct as is. |  |
| build.py | 3318 | A series lists a context page id instead of its tutorial. | practice_pairs later overwrites the page's placements from its owner tutorial, so listing a context page is harmless; the build can say so and carry on. |  |
| build.py | 3323 | A series lists a practice page id. | Practice placements are overwritten from the owner tutorial, so listing one is ignored, not broken. Parity: check.py also reports it as a Problem. | tests/build/test_courses.py::TestCourses::test_a_practice_page_listed_in_a_course_stops_the_build |
| build.py | 3333 | mixed: lists a tutorial that has no practice_across line. | A plain tutorial under mixed: only gets a course-level placement; no reader-visible break shown in code, but intent is unclear. Parity: check.py also errors. | tests/build/test_practice.py::test_a_broken_page_of_problems_fails_the_build[mixed: names a page that is not a mixed set] |
| build.py | 3407 | A practice page declares covers, which would count its outcome twice. | Page loads and works; double counting of coverage is an authoring choice, and the build could simply ignore covers here. | tests/build/test_practice.py::TestPagesOfProblems::test_a_broken_page_of_problems_fails_the_build |
| build.py | 3422 | practice_for names a context page instead of a tutorial. | A context page has placements, so the practice page loads and is placed fine; whether it belongs there is house shape. |  |
| build.py | 3459 | A mixed problem set declares covers, double-reporting outcomes across tutorials. | Page loads fine; double-counted coverage is an authoring matter. | tests/build/test_practice.py::TestPagesOfProblems::test_a_broken_page_of_problems_fails_the_build |
| build.py | 3464 | practice_across lists only one tutorial. | One-name practice_across works (placement from the first tutorial); it is only a second way to say practice_for. | tests/build/test_practice.py::TestPagesOfProblems::test_a_broken_page_of_problems_fails_the_build |
| build.py | 3468 | A tutorial id is repeated inside practice_across. | A repeated id only repeats a listing; the page still works. | tests/build/test_practice.py::TestPagesOfProblems::test_a_broken_page_of_problems_fails_the_build |
| build.py | 3472 | practice_across names the page's own slug. | A self-reference is harmless here because placement comes from the first named tutorial; the page loads. | tests/build/test_practice.py::TestPagesOfProblems::test_a_broken_page_of_problems_fails_the_build |
| build.py | 3479 | practice_across names a page that is itself a practice page. | The named page exists and the set is placed; drawing on problem sets is a shape preference. | tests/build/test_practice.py::TestPagesOfProblems::test_a_broken_page_of_problems_fails_the_build |
| build.py | 3482 | practice_across names a context page instead of a tutorial. | The named page exists and is placed; drawing on background reading is a shape preference. |  |
| build.py | 3525 | A context page declares covers, though nothing on it is required. | Page loads; whether optional reading may carry coverage is an authorial choice. | tests/build/test_context.py::TestContextPages::test_a_broken_context_page_fails_the_build |
| build.py | 3530 | context_for names the same tutorial more than once. | A repeated id only duplicates a listing line; page works. | tests/build/test_context.py::TestContextPages::test_a_broken_context_page_fails_the_build |
| build.py | 3540 | context_for names a practice page instead of a tutorial. | Context for a practice page is rendered on that page; placement works, only the shape is unusual. | tests/build/test_context.py::TestContextPages::test_a_broken_context_page_fails_the_build |
| build.py | 3544 | context_for names another context page. | Context pages render on any page by slug, so a nested one is reachable; it is a shape preference. | tests/build/test_context.py::TestContextPages::test_a_broken_context_page_fails_the_build |
| build.py | 4118 | A Math or Python Basics group has no entries. | An empty group is odd but builds; the tab is just empty. Carry on and say so. | tests/build/test_reference_index.py::TestBasicsValidation::test_a_group_with_no_entries_fails_the_build |
| build.py | 5272 | A data file in data/ has no matching yaml describing its source and snapshot. | A data file with no yaml still loads for readers; this is a provenance habit. It fails the whole build even for undeclared files. | tests/build/test_tutorial.py::test_every_data_file_needs_its_yaml_even_undeclared |
| build.py | 5302 | A tutorial declares a dataset whose data/ yaml description does not exist. | The data loads without its yaml; only the attribution and snapshot note go missing. Provenance preference, though the snapshot note would be absent. | tests/build/test_tutorial.py::TestDatasets::test_note_and_dataset_faults_fail_the_build |
| build.py | 6951 | Literal double braces survive token filling in the page shell, so an unfilled placeholder would remain. | Author text containing double braces is legal prose; the check really guards shell tokens and should look at the shell, not the filled page. |  |
| build.py | 7010 | Literal double braces survive filling on the all-tutorials page, so a placeholder would remain. | Same shell-token guard fed by author titles; a title with braces still loads and reads fine. |  |
| build.py | 7088 | Literal double braces survive filling on the My Notes page, typically from a tutorial title in its title map. | Same shell-token guard fed by author titles; page still works with literal braces. |  |
| build.py | 7205 | Literal double braces survive filling on a course page, from its title or description text. | Same shell-token guard fed by course text; page still works with literal braces. |  |
| build.py | 7478 | Literal double braces survive filling on the topic tree page, from topic or tutorial names in its data. | Same shell-token guard fed by topic and tutorial names; page works with literal braces. |  |
| build.py | 7541 | layout.json places a town whose code is not a topic in graph.json. | Extra entry in layout.json for a removed topic is ignored when drawing; harmless tidiness, not a broken page. | tests/build/test_map.py::TestTheBuildRefusesAMapThatDoesNotMatch.test_a_layout_that_places_a_topic_the_map_no_longer_has |
| build.py | 7731 | Literal double braces survive filling on the map page, from topic, step or landmark names in its data. | Same shell-token guard fed by topic and tutorial names; page works with literal braces. |  |
| build.py | 7840 | Literal double braces survive filling on the topics page, from group names, intros or tutorial titles. | Same shell-token guard fed by group names and intros; page works with literal braces. |  |
| check.py | 180 | Main file frontmatter still has module, module_title, series or slug lines from the old layout. | Leftover placement keys are ignored once courses/ places the tutorial; the page works, so this is clean-up, not breakage. | tests/build/test_check.py::test_everything_check_calls_a_problem_the_build_also_refuses[an old placement field] |
| check.py | 239 | A context page also has a covers: line in its frontmatter. | Covers on a context page is an authorial statement about outcomes; the page itself loads and works. |  |
| check.py | 266 | A practice page has a covers: line in its frontmatter. | Covers on a practice page is a bookkeeping preference about who teaches an outcome; the page works. |  |
| check.py | 269 | A practice page still has module, module_title, series or slug lines from the old layout. | Same as the tutorial case: stale placement keys are ignored; the page works. |  |
| check.py | 281 | The glossary file has entries missing a term or a definition. | A blank glossary entry is untidy but one half-written entry need not stop the page; skip it with a note. |  |
| check.py | 333 | A series lists no tutorials, or an empty tutorials list. | An empty series is a placeholder an author may reasonably keep; page loads, just shows a heading with nothing under it. |  |
| check.py | 339 | A series lists a practice page id, which has practice_for in its frontmatter. | A practice page in a course list still resolves; it shows as an extra item. Build may need it for series keys, so low confidence. | tests/build/test_check.py::test_a_context_page_is_not_a_problem_but_listing_one_in_a_course_is |
| check.py | 341 | A series lists a context page id, which has context_for in its frontmatter. | A context page in a course list still resolves and loads; it is a placement preference. | tests/build/test_check.py::test_a_context_page_is_not_a_problem_but_listing_one_in_a_course_is |
