# Practice problems

Every tutorial has a page of problems beside it, and four more sets draw on
several tutorials at once. This file records where the material came from, how
the pages are built, and what is still worth doing.

---

## 1. What exists

| | Count |
|---|---:|
| Tutorials | 41 |
| Practice pages, one per tutorial | 38 |
| Mixed sets, drawing on several | 4 |

Six of the tutorials and six of the practice pages are the first 5N0554
strand — `computational-methods`'s `matrices` series — and unlike the other
thirty-two, their worksheets (`07a`, `07b`, `07d`) have no answer key in the
markdown, only a PDF. Every number on those six practice pages was worked
fresh rather than transcribed; see DECISIONS_LOG 7.56.

Three tutorials have no practice page, on purpose. *Bringing It All Together*
is already a set of integrative problems, and *Looking Back Before Moving
Forward* and *The Team Project* ask for reflection rather than answers.

The mixed sets are on the programming spine, on algebra and functions, on
trigonometry and geometry, and on data, chance and logic.

## 2. Where the material came from

### `deweydex/Mathematics`

Twenty-six worksheets under `markdown/`, written for *AIML Foundations
Mathematics* at Dublin and Dún Laoghaire ETB. Each is 200–600 lines and holds
roughly 60 problems.

**Twenty of the twenty-six end in an answer key in the markdown.** The other six
— `04e_optimisation`, `07a_matrix_operations`, `07c_eigenvalues`,
`07d_markov_chains`, `08a_bayes` and `08b_distributions` — have answers only as
PDFs under `pdfs/solutions/`. Those six are also the ones whose material is not
yet taught here, so nothing has been lost yet; when the 5N0554 strands are
written, their answers will have to come out of the PDFs or be worked afresh.

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

## 3. How a practice page is built

**Frontmatter.** One line beyond an ordinary tutorial:

```yaml
title: "The Unit Circle — Practice"
slug: the-unit-circle-practice
practice_for: the-unit-circle
```

`build.py` checks both directions: the tutorial has to exist, be in the same
module, and not be a practice page itself, and no two pages may claim the same
tutorial. A practice page declares no `covers:` — it sets problems on what its
tutorial taught, and saying so twice would report one outcome as taught by two
pages.

A mixed set uses `practice_across:` with a list of slugs instead. It links to
each of them and none links back; see `DECISIONS_LOG.md` 7.49 for why.

**Answers behind folds.**

```html
<details class="dl-answer"><summary>answer</summary>

The answer, with the working.

</details>
```

The site is public, so an answer that exists can be read. What is worth
protecting is not the answer but the moment before looking, and a fold is that
moment made physical. A key at the bottom of the page is one scroll away, which
is the same as being on it.

**A few checking tools, not a cell per problem.** One `python exec` cell per
section, holding the helpers that section's problems need. Sixty CodeMirror
instances on a page is a slow page, and a cell under every question invites
running it instead of thinking.

**Every number gets run.** Twenty-one wrong numbers were caught this way while
these pages were written, and none of them would have failed a test — no test
asserts on prose. See `DECISIONS_LOG.md` 7.50.

## 4. What is left

- **`dev/from_worksheet.py`.** A converter for the Mathematics worksheets. The
  two conditions for writing it are now met: the build supports practice pages,
  and several have been done by hand so the shape is known. Whether it is worth
  writing at all is a fair question — the remaining worksheets are the ones for
  material that is not taught yet, so the converter would have nothing to
  convert until those tutorials exist.
- **Practice for the remaining 5N0554 strands**, once they are written. `07a`,
  `07b`, and `07d` fed the matrices strand's six pages; `07c` (eigenvalues),
  `08a` (Bayes) and `08b` (distributions) are still waiting, and their answers
  are in PDFs too.
- **Student-authored problems**, which is a runtime feature rather than a
  content one. See `planning/PRACTICE.md`.
