# Outline — Two conversions from everlearning

**Closes:** `PDP-LO1` (history of programming), `PDP-LO3` (differentiate
languages by characteristics), `PDP-LO9` (interpret compiler and linker
messages).

Neither of these needs writing. Both exist as finished notebooks in
`everlearning`, and `dev/from_notebook.py` already converts notebooks into
dewlab tutorials. The work is conversion and a teaching pass, not authorship.

## How We Got Here — `PDP-LO1`, `PDP-LO3`

**Source:** `everlearning`
`PDP_MIT_2026_2027_Integrated/LearningOutcomes/PDP/PDP-LO1_LO3_MIT-1.4_The-Computing-Time-Machine.ipynb`
**Goes after:** Tutorial 1.

Purpose-built for these two outcomes, framed around the binary and hexadecimal
work so that the history reinforces a skill rather than sitting beside it. Stop 4
(a table of languages and paradigms) and Stop 5 (the same small program in
several paradigms) are what carry `PDP-LO3`.

**What conversion needs:**

- Run `dev/from_notebook.py` and check the section headings became sensible cell
  ids.
- The notebook is a tour with numbered "stops". Those want to become `##`
  headings.
- Check the paradigm snippets: anything not Python will need to become an
  illustrative block rather than a runnable cell, since dewlab runs Python only.

## When It Goes Wrong — `PDP-LO9`

**Source:** `everlearning`
`PDP_MIT_2026_2027_Integrated/LearningOutcomes/PDP/PDP-LO9_LO10_Reading-Compiler-Errors-and-Debugging.ipynb`
**Goes after:** Tutorial 3.

Reading an error message is the most useful single thing a beginner can learn,
and dewlab currently teaches it only in passing. Early in the series, while the
errors are still small.

**What conversion needs:**

- This one gains from dewlab rather than merely surviving it: a cell that raises
  the error and shows the traceback in place is better than a printed screenshot
  of one. Check that the deliberate errors actually run and fail as intended.
- There is a `SOLUTION_` twin in the same folder. Decide what happens to
  solutions generally before converting — see `planning/OPEN_QUESTIONS.md`.
- LO10 (testing) is already covered by Tutorial 8, so this conversion should
  keep the LO9 half and hand the rest over rather than duplicating it.

## Note

These two are the cheapest items on the whole gap list — no new material, no new
mathematics, and a converter that already works. If the aim is to close outcomes
per hour spent, they come first.
