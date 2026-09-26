# Practice problems

Every tutorial has a page of problems beside it, and every series and course
has a mixed set. How to write one is in `docs/WRITING_TUTORIALS.md`: start
from the templates in `docs/templates/`
([`running-totals-practice.md`](../docs/templates/running-totals-practice.md)
for a practice page,
[`mixed-running-totals.md`](../docs/templates/mixed-running-totals.md) for a
mixed set). Why they are shaped that way is in the style guide's
[page shapes](PEDAGOGICAL_STYLE_GUIDE.md#page-shapes) and
[nothing is taught once](PEDAGOGICAL_STYLE_GUIDE.md#nothing-taught-once).

This file keeps what those do not: where the first problems came from, and
what is still to do.

---

## Where the material came from

### `deweydex/Mathematics`

Twenty-six worksheets under `markdown/`, written for *AIML Foundations
Mathematics* at Dublin and Dún Laoghaire ETB. Each is 200–600 lines and holds
roughly 60 problems.

**Twenty of the twenty-six end in an answer key in the markdown.** The other six
— `04e_optimisation`, `07a_matrix_operations`, `07c_eigenvalues`,
`07d_markov_chains`, `08a_bayes` and `08b_distributions` — have answers only as
PDFs under `pdfs/solutions/`, so every number on a page they fed was worked
afresh (`DECISIONS_LOG.md` 7.56).

Which worksheet fed which page:

| Worksheet | Practice page |
|---|---|
| `01_fractions`, `01a`, `01b` | `numbers-and-their-families-practice` |
| `02a_lines_coordinates_vectors` | `lines-and-distances-practice` |
| `02b_linear_thinking_data_curves` | `drawing-functions-practice` |
| `03a_foil_expanding` | `expressions-come-alive-practice` |
| `03b_factoring_solving`, `03c_applications` | `cracking-equations-practice` |
| `03d_graphing` | `parabolas-practice` |
| `04a_derivatives_integrals_inverse` | `approaching-a-limit-practice` |
| `04b_what_they_tell_us` | `rates-of-change-practice` |
| `05a_angles_radians_unit_circle` | `the-unit-circle-practice` |
| `05b_right_triangle_trig`, `05e_laws_sines_cosines` | `solving-triangles-practice` |
| `05c_graphs_sine_cosine` | `sine-and-cosine-waves-practice` |
| `06a_statistics_probability` | `what-are-the-chances-practice`, `making-sense-of-data-practice` |
| `07a_matrix_operations` | `grid-of-numbers-practice`, `multiplying-grids-practice`, `undoing-it-practice` |
| `07b_linear_systems` | `solving-systems-practice` |
| `07d_markov_chains` | `where-chains-lead-practice` |
| `07c_eigenvalues`, `08a_bayes`, `08b_distributions` | not yet — the material is not taught yet |

### `deweydex/everlearning`

`PDP_MIT_2026_2027_Integrated/PracticeProblems/PDP-Practice-Problem-Bank.py`
holds thirty-eight programming problems as **blank stubs with docstrings and no
answers**. They gave the questions for the programming spine's practice pages;
every answer was written here.

### The tutorials themselves

The largest source. Every "your turn" prompt in a tutorial is a problem that was
already set and never answered, and those now have answers to compare against.

---

## What is left

- **A worksheet converter**, which would live in `dev/` and does not exist
  yet. It would convert the Mathematics worksheets, and the two conditions for
  writing it are now met: the build supports practice pages, and several have
  been done by hand so the shape is known. But the remaining worksheets are
  for material not taught yet, so the converter would have nothing to convert
  until those tutorials exist — worth writing only once that changes.
- **Practice for the remaining 5N0554 strands**, once they are written. `07a`,
  `07b`, and `07d` fed the matrices strand's six pages; `07c` (eigenvalues),
  `08a` (Bayes) and `08b` (distributions) are still waiting, and their answers
  are in PDFs too.
- **Student-authored problems**, which is a runtime feature rather than a
  content one — a reader's own cells, described in
  `docs/tutorial-runtime-explained.md`.
