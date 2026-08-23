# Curriculum Pedagogical & Structural Analysis

Curriculum design notes, structural dependency analysis, pedagogical sequencing evaluations, and terminology consistency rules for dewlab.

---

## 1. Curriculum Information Architecture

| Specification File | Purpose & Contents |
|---|---|
| [`CURRICULUM_MAP.md`](./CURRICULUM_MAP.md) | Automated outcome coverage matrix mapping all descriptor outcomes to active/proposed tutorials. |
| [`curriculum/outcomes.yaml`](./curriculum/outcomes.yaml) | Comprehensive list of syllabus learning outcomes from accredited module descriptors. |
| [`curriculum/out-of-scope.yaml`](./curriculum/out-of-scope.yaml) | Explicitly excluded topics and rationale, with record of returned items. |
| [`curriculum/proposed.yaml`](./curriculum/proposed.yaml) | Proposed curriculum tutorial modules and designated syllabus mappings. |
| [`curriculum/DECISIONS_NEEDED.md`](./curriculum/DECISIONS_NEEDED.md) | Structured decision records on curriculum sequencing and scope boundaries. |
| [`outlines/`](./outlines/) | Pedagogical outlines for all proposed curriculum modules. |

---

## 2. Coverage Analysis & Structural Gaps

Initial coverage analysis of the 65 accredited learning outcomes identified clear structural clustering:

- **Comprehensive Coverage**: Algorithms (9 of 9), Probability (8 of 8), Statistics (5 of 5), Number sets.
- **Mathematics Extension Gaps**: Calculus (0 of 3), Trigonometry (0 of 6), Function graphing & analysis (0 of 3), Formal logic (0 of 2).
- **Partial Strands**: Geometry (2 of 6), Core programming (7 of 11), Algebra (6 of 8).

### Critical Unaddressed Prerequisites ("Quiet Gaps")
Certain concepts were frequently utilized in code examples before receiving formal instruction:
1. **Truth Tables (`MIT-2.4`)**: Logical operators (`and`, `or`, `not`) were introduced in early control-flow tutorials without truth tables or formal evaluation rules. Resolved by scheduling *Logic and Truth*.
2. **Complex Roots (`MIT-1.10`)**: Quadratic equation solving handled negative discriminants by declaring "no real solutions" without introducing the imaginary unit $i$. Resolved by scheduling *When There Is No Answer*.
3. **Inverse Functions (`MIT-3.1`)**: Function mappings referenced without formal definition of domain/range inversion.
4. **Formula Transposition (`MIT-1.7`)**: Equation rearrangement assumed across multiple scientific exercises. Resolved by scheduling *Rearranging Formulae*.

---

## 3. Modularization & Pedagogical Sequencing

### Structural Review of Existing Tutorials

#### *Numbers and Their Families*
Original analysis revealed multiple distinct conceptual areas combined in a single unit:
- Number Domains (`MIT-2.1`) — Set theory ($\mathbb{N} \subset \mathbb{Z} \subset \mathbb{Q} \subset \mathbb{R}$)
- Exponents and Logarithms (`MIT-1.1`) — Algebra and inverse operations
- Geometric Formulas (`MIT-1.2`, `MIT-1.3`) — Mensuration

**Pedagogical Re-alignment**:
- Number domains align directly with primitive data types (`int`, `float`) and are integrated early.
- Exponents and logarithms are established prior to combinatorial counting, standard deviation, and polynomial calculus.
- Geometric formulas serve as concrete applications of function definition.

#### *Expressions Come Alive*
Focuses strictly on polynomial representation, evaluation, and polynomial arithmetic (addition, multiplication, subtraction). Serves as the direct foundation for algebraic solving (*Cracking Equations*) and polynomial calculus (*Rates of Change*).

### Decoupling Sequence from Numbered Titles
Sequencing is decoupled from tutorial file basenames and headings. Tutorials utilize descriptive titles (e.g. *Expressions Come Alive* rather than *Tutorial 14*) and manage order via series order files (`<series>.order.yaml`). This avoids cascading renaming edits when inserting new instructional units.

---

## 4. Terminology Disambiguation & Style Rules

To avoid conceptual confusion across paired mathematics and programming curriculum, terminology must adhere to strict disambiguation rules:

| Term Candidate | Disambiguation Rule | Rationale |
|---|---|---|
| **Index / Indices** | Reserve exclusively for list/sequence positioning or summation bounds. Use **Power** or **Exponent** for exponentiation. | Prevents collision between sequence indexing (`list[i]`) and algebraic powers. |
| **Function** | Explicitly distinguish between Python callables (`def foo():`) and mathematical mappings ($f: X \to Y$). | Avoids conflating computational side effects with pure mathematical relations. |
| **Range** | Explicitly distinguish between Python generator `range(start, stop)` and statistical dispersion / functional codomain. | Contextual distinction between iteration tools and descriptive metrics. |
| **Set** | Distinguish Python `set` collections from mathematical sets and variable assignment. | Clarity in discrete math and database contexts. |
| **Expression** | Distinguish Python evaluable code expressions from algebraic symbolic expressions. | Clear boundaries in SymPy and computational modeling. |
