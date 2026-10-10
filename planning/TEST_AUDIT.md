# Test audit

*10 October 2026. Planning document, not student-facing.*

The question put to every check: **if it fails, does something break for a
reader or for the build, or has an author only done something we would not
have chosen?** A second test came from Josh: if every content file were
deleted and someone else's put in their place, the number of checks worth
running should barely change.

Every test in `tests/` (1,143 functions in 79 files) was read, along with
the 293 places where `build.py` and `check.py` stop an author. A small model
recorded what each test asserts and what it reads; a stronger model ruled on
each, reading the code where the facts were thin. Verdicts are proposals. The
full list of everything that is not plain KEEP is in
[`TEST_AUDIT_LEDGER.md`](TEST_AUDIT_LEDGER.md).

## What was found

**The tests themselves are in better shape than feared.** Of 1,073 tests ruled
on in the main pass, 872 (81%) are sound as they stand. Only 63 (6%) are tied
to today's content. The rest of the picture is a short list of problems, most
of them somewhere other than where it looked like they would be.

| Verdict | Tests | Meaning |
|---|---:|---|
| Keep | 872 | Guards a reader, an id contract or a real feature, independent of content |
| Wire up | 89 | Guards saved work, ids, data or safety, but never runs in CI |
| Re-home | 47 | Sound aim; reads real content or source text, so rewrite against a fixture or behaviour |
| Retire | 45 | Pins an authorial choice or an implementation detail, or duplicates another test |
| Advisory | 19 | Guards a house preference or a planning file the build does not read |
| Question | 1 | Needs Josh |

Eight top-level files (about 70 tests) were read by hand before the main
pass and are not in those numbers; their rulings are in
[First-pass files](#first-pass-files) below.

### 1. The content dependence is in the fixtures, and per-test reading missed it

Deleting `tutorials/`, `pages/`, `courses/`, `planning/` and `map/` from a
copy and running the 755 unit tests gave a sharper answer than any reading:

- **All 413 tests in `tests/build/` could not be collected.**
  `tests/build/helpers.py` reads `pages/about.md` when it is imported, and its
  `repo` fixture copies the real About, Home, Features and every other page
  into each synthetic site. The suite meant to test the build on small fake
  sites builds Josh's actual prose in every test.
- With one-line stub pages instead, 679 tests passed and 40 failed (5.6% of
  the 719 that ran). 23 of the 40 are top-level: the curriculum-map (11),
  handwritten-classes (8), glossary (2), picture and layout tests. The other
  17 are in `tests/build/` (curriculum 6, courses 5, map 3, and one each in
  site, releases and reference index): their fixtures still read the real
  `planning/curriculum/*.yaml` because the build's module-level paths for
  that data are not redirected into the temporary site.
- The same coupling sits in the browser suite: `test_page_smoke.py` builds
  against the real pages and curriculum data; `test_dewmini_workbench.py`
  copies the real `planning/curriculum` and `data/`; `test_loading_data.py`
  asserts literal snapshot dates ("26 September 2026"), so refreshing a
  dataset breaks four tests.

### 2. Most of the browser suite never runs in CI

CI's `browser` job names five of the 44 e2e files. The other 39 (488 tests) are
local-only. Most of those are fine to leave there, but 85 guard things a
reader depends on and have no other net: autosave and restore, the
progress-key contract, the orphaned-cell notice, custom cells and their ids,
version redirects, imported text never read as markup, the web-cell sandbox,
highlight anchoring, colour contrast. `test_erd_graphics.py` (36 tests)
skips in CI because `svgwrite` is not installed there.

Some of these need no Pyodide and are cheap to add: `test_my_words.py`,
`test_highlight_popover.py`, and the prose-only test in `test_custom_cells.py`.

### 3. The build refuses 51 things that should be notes

Of 293 refusals, 242 stop the build for good reason (missing ids, unclosed
fences, links to nothing, solutions that do not run). 51 stop an author
although the page would load and work. The largest group is house shape:

- a project body must open with a `##` heading; the author's own project must
  come last and be the only one; project divs must follow the order of
  `projects:`; every project needs all five card fields;
- `practice_across` with one name, a repeated name, a name that is a practice
  page or a context page; `covers:` on a practice, mixed or context page;
  `context_for` naming a practice or context page twice;
- stale placement keys in frontmatter (`module`, `series`, `slug`) that the
  build ignores;
- a one-option multiple-choice question; a tolerance on a non-number
  prediction; an empty series; a blank glossary entry.

`check.py` mirrors the build and a parity test requires them to agree, so each
is a pair of changes.

### 4. One refusal is a bug, not a preference

After the shell template is filled, the build raises if the finished page
contains `{{` anywhere. That scans the author's own words. A Python cell with
`print(f"{{literal}} {name}")`, or a sentence showing a template as
`{{ name }}`, stops the build with "shell template has tokens build.py does
not fill". Any tutorial about templating would hit it. Eight pages use this
guard. It should compare against the shell's own token names.

### 5. Tests that promise more than they check

Several tests pass whether or not the feature works. Examples: a reset test
that skips if there is no reset button; `test_a_mismatched_file_leaves_the_existing_record_alone`,
whose guard is written inside the test's own `page.evaluate`; two "declining
leaves it running" tests that pass on any output containing `True`;
`test_a_short_toolkit_has_no_list`, which passes when the element is missing;
absence checks for markup that was removed long ago (`#dl-panels`,
`#dl-seriesnav-toggle`) tucked inside otherwise real tests. They are listed in
the ledger as re-home, with the assertion that needs strengthening.

### 6. Tests that pin interface wording

Many e2e and unit tests assert whole interface sentences ("Compare with a
solution", "WHERE IT TURNS UP", "3 rows affected"). A reword fails them with
no reader impact. Where the wording is the feature (the SQL hints) they stay;
elsewhere the ledger suggests asserting structure or state.

### 7. Page-specific number checks need one mechanism

`test_handwritten_classes.py` promises one thing (every hand-written `dl-`
class has a rule) and holds twelve tests, eleven of them about four named
tutorials. Five are sound in aim: HOW_DEWLAB_THINKS says a number a page states
must follow from its own code. They should become one declared mechanism that
any page can use, not a test per page. Four others grep the stylesheet or
runtime for strings and should go.

## First-pass files

Read by hand. Verdicts as in the ledger's vocabulary.

| File | Ruling |
|---|---|
| `test_check_doc_links.py` | Keep. Unit tests of a documentation checker; the one real-repository test is already advisory. |
| `test_video_links.py` | Keep. Link-finding and status logic for a weekly workflow. |
| `test_map_layout_script.py` | Keep the determinism and fixture tests. "Reproduces the committed layout of the real map" is a freshness check on a file the build never recomputes: a CI `--check` step, not a test. |
| `test_picture_patterns.py` | Keep five (accessibility feature). `every_picture_script_adds_the_pattern_layer` greps source for a magic string and `len(writers) >= 14`: re-home to check output pictures. `no_two_pictures_share_a_pattern_id` guards a real collision: keep. |
| `test_report_patterns.py` | Keep. `issue()` has an unused `days_old` parameter; `label_report_uses_the_same_parser` exists only because the parser is duplicated, so deduplicating retires it. |
| `test_term_uses.py` | Advisory. Tests an author-only lister referenced only from WRITING_TUTORIALS; `after_its_start` encodes a teaching rule about when to mark a term. |
| `test_glossary_python.py` | Keep. The build uses it. `signatures_file_is_current` skips off the Python version it was written under: make it a `--check`. |
| `test_handwritten_classes.py` | See section 7. Keep the CSS-class check; one mechanism for the page-number checks; retire the source greps and the "exactly two boxes" demand. |

## Rulings that need Josh

1. **Verdict-word checks.** `test_no_word_in_the_markup_judges`
   (`test_blocks.py`), `test_no_word_in_the_block_judges`
   (`test_predict_build.py`) and `test_no_word_on_the_table_judges`
   (`test_compare.py`) scan the site's own interface strings for words like
   "wrong" and "pass". The audit ruled them retire, because HOW_DEWLAB_THINKS
   says nothing scans pages for verdict words. They scan the product's strings,
   not authors' prose, and "no verdicts" is a core principle. Keep or retire?
2. **A tutorial listed under two series** (`build.py` line 3237). The audit
   says the placement code tolerates it. It was not confirmed that breadcrumbs
   and the where-you-are tree stay sensible. Left as a refusal.
3. **Data files without a provenance yaml** (lines 5272, 5302). Provenance and
   snapshot dates are project policy. Left as a refusal unless you say
   otherwise.
4. **CI path filtering and wiring the local-only browser tests** are separate
   changes to the workflow. Neither is made here.

## How far to trust this

The extractor (a small model) was wrong in places; the judges corrected it
where they noticed (for instance, 15 saved-progress tests flagged as
content-tied turned out to use test-owned fixtures). The judges did *not*
notice the fixture-level coupling in section 1; the deletion experiment did.
Each section above rests on code that was read, but a ruling in the ledger is
a starting point for a person, not a replacement for one.

## What changed

*Filled in as the changes land.*
