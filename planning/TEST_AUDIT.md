# Test audit

*October 2026. Planning document, not student-facing. The reasoning is
DECISIONS_LOG 7.298; the rule it produced is in `CONTRIBUTING.md`, "What a
test or a refusal may stop".*

The question put to every test and every refusal: **if it fails, does
something break for a reader, or has an author only done something we would
not have chosen?** And Josh's check on the whole: with every content file
deleted, the number of tests worth running should barely change.

## What was found

- **The build's tests were built on the real site.** `tests/build/helpers.py`
  read `pages/about.md` on import and copied every real page into each small
  test site, so with the content removed all 413 tests in `tests/build/`
  could not be collected.
- **The build refused things that break nothing.** About thirty refusals
  were about the shape of a page (card order, a heading, one option where
  two were expected, a field in the old place) and not about a page a
  reader could not use. One was a bug: the `{{` guard scanned the author's
  own words.
- **Some tests guarded content, not code**: numbers copied from a page,
  greps of the stylesheet, the committed pictures, the planning files'
  agreement with each other.
- **Most tests were sound.** About four in five guard a reader, an id
  contract or a feature, and do not care what the content says.

## What changed

- Every file under `pages/` is optional; a fork can drop About, Features or
  the helpers and still build. `tests/build/` writes no pages.
- The shape refusals are notes, printed once per build. `check.py` agrees.
- The `{{` guard checks the shell's own tokens.
- Planning and picture checks moved to `--check` on their scripts, reported
  by the house-style job and never blocking. Eighteen tests retired; four
  remain `advisory`.
- A recursion the relaxed rules exposed (two mixed sets naming each other)
  is fixed.

With the content removed, 16 of 715 blocking tests now fail, all because
their fixtures still read `planning/curriculum/`, the map layout, the
glossary signatures or the committed pictures.

## Still open

1. **The verdict-word checks** (`test_no_word_in_the_markup_judges` and two
   like it) scan the site's own interface strings, not authors' prose. Keep
   or retire is Josh's call.
2. **85 browser tests that guard saved work, ids and imported text run only
   locally.** Wiring them into CI is a cost decision.
3. **Path filtering in CI**, so a change to a planning file does not run the
   whole suite.
4. **The sixteen tests above** want fixtures of their own instead of the
   real curriculum data.
