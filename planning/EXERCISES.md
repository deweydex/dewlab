# Practice Problems & Worksheet Conversion Specification

Architecture and conversion specification for practice problem sets paired with dewlab tutorials, derived from upstream worksheet materials in [`deweydex/Mathematics`](https://github.com/deweydex/Mathematics).

---

## 1. Upstream Source Materials & Curriculum Mapping

The upstream repository [`deweydex/Mathematics`](https://github.com/deweydex/Mathematics) contains **twenty-seven comprehensive, finished worksheets** under `markdown/`. Developed for *AIML Foundations Mathematics* at Dublin and Dún Laoghaire ETB, each worksheet spans 250–600 lines, includes roughly 60 structured practice problems, and concludes with a complete step-by-step answer key.

These worksheets align directly with the integrated mathematics and computing modules in dewlab:

| Upstream Worksheet (`deweydex/Mathematics`) | Target Tutorial Module | Practice Page Slug |
|---|---|---|
| `02a_lines_coordinates_vectors.md` | *Lines and Distances* | `lines-and-distances-practice.md` |
| `02b_linear_thinking_data_curves.md` | *Drawing Functions* | `drawing-functions-practice.md` |
| `03a_foil_expanding.md`, `03b_factoring_solving.md` | *Expressions Come Alive*, *Cracking Equations* | `expressions-come-alive-practice.md`, `cracking-equations-practice.md` |
| `03d_graphing.md` | *Parabolas* | `parabolas-practice.md` |
| `04a_derivatives_integrals_inverse.md`, `04b_what_they_tell_us.md` | *Approaching a Limit*, *Rates of Change* | `approaching-a-limit-practice.md`, `rates-of-change-practice.md` |
| `05a_angles_radians_unit_circle.md` | *The Unit Circle* | `the-unit-circle-practice.md` |
| `05b_right_triangle_trig.md`, `05e_laws_sines_cosines.md` | *Solving Triangles* | `solving-triangles-practice.md` |
| `05c_graphs_sine_cosine.md` | *Sine and Cosine Waves* | `sine-and-cosine-waves-practice.md` |
| `06a_statistics_probability.md`, `08a_bayes.md`, `08b_distributions.md` | *What Are the Chances*, *Making Sense of Data* | `what-are-the-chances-practice.md`, `making-sense-of-data-practice.md` |
| `07a`–`07d` Matrices & Markov Chains | The Matrices Strand (5N0554) | `matrices-practice.md`, `markov-chains-practice.md` |
| `01_fractions.md`, `01a`, `01b` Exponents & Logarithms | *Numbers and Their Families* | `numbers-and-their-families-practice.md` |

---

## 2. Pedagogical Architecture of Practice Pages

### A. Protecting the "Moment Before Looking"
In traditional paper worksheets, answer keys placed at the very end require awkward page flipping or encourage premature lookup. In dewlab, answers are embedded directly adjacent to each problem inside an accessible HTML collapsible fold (`<details><summary>Check solution</summary>...</details>`).

This design:
1. **Preserves the effortful retrieval attempt**: Students pause, formulate an answer, and mentally commit before revealing the solution.
2. **Provides immediate corrective feedback**: Students verify understanding instantly while their working steps are fresh in mind.
3. **Eliminates evaluation anxiety**: Practice remains completely formative and self-directed, free from punitive automated grading.

### B. Worked Conversion Example

#### Source Markdown in `deweydex/Mathematics/markdown/05a_angles_radians_unit_circle.md`:
```markdown
## Part A: Angle Conversions and Arc Length
1. Convert 45° to radians. Express your answer in terms of π.
2. Convert 5π/6 radians to degrees.

## Answer Key
1. 45° × (π/180°) = π/4 radians.
2. (5π/6) × (180°/π) = 150°.
```

#### Generated dewlab Practice Format (`the-unit-circle-practice.md`):
```markdown
## Part A: Angle Conversions and Arc Length

**Problem 1:** Convert $45^\circ$ to radians. Express your answer as an exact multiple of $\pi$.

<details>
<summary>Check solution</summary>

$$45^\circ \times \frac{\pi}{180^\circ} = \frac{\pi}{4}\text{ rad}$$
</details>

**Problem 2:** Convert $\frac{5\pi}{6}$ radians to degrees.

<details>
<summary>Check solution</summary>

$$\frac{5\pi}{6} \times \frac{180^\circ}{\pi} = 5 \times 30^\circ = 150^\circ$$
</details>
```

### C. Section-Level Interactive Verification Scratchpads
Instead of burdening the browser with 60 individual CodeMirror instances per page, each major section provides a single interactive Python verification tool.

*Example Section Scratchpad for Trigonometry Practice*:
```python exec
id: unit-circle-practice-checker
# Section A & B Verification Helper
import numpy as np

def angle_info(degrees):
    radians = np.deg2rad(degrees)
    print(f"Degrees: {degrees}°")
    print(f"Radians: {radians:.4f} rad ({degrees/180:.3f}π)")
    print(f"Coordinates on Unit Circle (x, y): ({np.cos(radians):.4f}, {np.sin(radians):.4f})")

# Try checking any problem angle:
angle_info(45)
```

---

## 3. Automated Converter Pipeline (`dev/from_worksheet.py`)

Worksheets across `deweydex/Mathematics` share a consistent structure:
- Frontmatter and title header.
- Section headings: `## Part A`, `## Part B`, etc.
- Numbered question lists: `1. ...`, `2. ...`.
- Trailing `## Answer Key` with matching numbered solution steps.

### Conversion Logic
1. **Parser**: Reads `markdown/<worksheet>.md`, separating question parts from `## Answer Key`.
2. **Pairing**: Matches question index `i` with answer key entry `i`.
3. **Folding**: Wraps each solution in a styled `<details><summary>Check solution</summary>...</details>` element.
4. **TeX Normalization**: Preserves LaTeX inline (`$...$`) and block (`$$...$$`) delimiters for client-side KaTeX rendering.
5. **Frontmatter Attachment**: Appends standard dewlab metadata linking the practice set to its parent tutorial:
   ```yaml
   ---
   title: "The Unit Circle — Practice"
   slug: the-unit-circle-practice
   module: mit-pdp-maths-prog-integration
   practice_for: the-unit-circle
   year: "2026-2027"
   ---
   ```

---

## 4. Implementation Status & Next Steps

- [x] **Prototypes Validated**: Handcrafted practice pages for *Lines and Distances*, *Drawing Functions*, *Parabolas*, and *The Unit Circle* created and verified in `tutorials/mit-pdp-maths-prog-integration/`.
- [ ] **Automated Conversion Utility (`dev/from_worksheet.py`)**: Implement the batch conversion script to ingest all 27 worksheets from `deweydex/Mathematics`.
- [ ] **Practice Navigation Integration**: Add subtle "Practice Problems" companion buttons in the tutorial mastheads and table of contents.
