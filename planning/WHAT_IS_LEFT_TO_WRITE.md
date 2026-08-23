# Curriculum Writing Backlog & Coverage Roadmap

Status of existing curriculum coverage, outstanding syllabus outcomes, and the phased writing roadmap for dewlab tutorials.

---

## 1. Summary of Current Coverage

For exact outcome counts, refer to [`planning/CURRICULUM_MAP.md`](./CURRICULUM_MAP.md), generated automatically from `curriculum/outcomes.yaml`, `curriculum/out-of-scope.yaml`, `curriculum/proposed.yaml`, and tutorial `covers:` frontmatter.

- **Existing Published Tutorials**: 20 tutorials (17 in *Maths and Programming*, 1 in *Reflections and Review*, 2 in *Computational Methods*).
- **Curriculum Outcomes Active**: 41 covered across Mathematics for IT (5N18396) and Programming and Design Principles (5N21493).
- **Outstanding Outcomes to Author**: 26 outcomes (22 unaddressed outcomes + 4 prerequisites previously used without formal introduction).
- **Proposals in Place**: All 26 outstanding outcomes have dedicated module proposals and structured outlines in [`planning/outlines/`](./outlines/).

---

## 2. Outstanding Modules by Domain

### Functions & Calculus (7 Outcomes)
- **`drawing-functions`** (*Drawing Functions*): Cartesian coordinates, function evaluation, polynomial plotting ($y = mx + c$, $y = ax^2 + bx + c$, higher degree), domain/range.
- **`parabolas`** (*Parabolas*): Vertex form, completing the square, axis of symmetry, roots and discriminants.
- **`approaching-a-limit`** (*Approaching a Limit*): Intuitive and computational limits, secant lines tending to tangent lines, numerical convergence.
- **`rates-of-change`** (*Rates of Change*): Power rule differentiation, polynomial integration, constant of integration, rates of change in computing contexts.

### Geometry & Trigonometry (10 Outcomes)
- **`lines-and-distances`** (*Lines and Distances*): Slope, midpoint, Euclidean distance, Pythagorean theorem gateway.
- **`the-unit-circle`** (*The Unit Circle*): Radians, unit circle definitions of sine and cosine, exact trigonometric ratios in surd form.
- **`sine-and-cosine-waves`** (*Sine and Cosine Waves*): Circular motion unrolled into wave functions, amplitude, period, frequency, phase shift.
- **`solving-triangles`** (*Solving Triangles*): Right-angled triangle trigonometry, angles of elevation/depression, Sine Rule, Cosine Rule, non-right triangle area.

### Logic, Sets & Synthesis (5 Outcomes)
- **`logic-and-truth`** (*Logic and Truth*): Truth tables, Boolean operations (`and`, `or`, `not`), De Morgan's laws.
- **`venn-diagrams`** (*Drawing Sets*): Visualizing set intersections, unions, and complements via Matplotlib.
- **`rearranging-formulae`** (*Rearranging Formulae*): Systematic formula transposition and algebraic balancing.
- **`complex-roots`** (*When There Is No Answer*): Complex numbers, imaginary unit $i$, representation of non-real roots.

### Programming & Design Principles (4 Outcomes)
- **`history-and-paradigms`** (*How We Got Here*): Evolution of programming languages, imperative vs. declarative vs. object-oriented paradigms.
- **`testing-and-debugging`** (*When It Goes Wrong*): Systematic debugging workflows, defensive programming, assertion testing.
- **`team-project`** (*Working Together*): Collaborative development workflows, task estimation, version control teamwork.

---

## 3. Recommended Implementation Roadmap

1. **Foundational Visual Mathematics**:
   - *Drawing Functions* → *Lines and Distances* → *The Unit Circle*.
   - Establishes coordinate geometry and functional foundations required by subsequent modules.
2. **Calculus & Wave Dynamics**:
   - *Approaching a Limit* → *Rates of Change*.
   - *Sine and Cosine Waves* → *Solving Triangles*.
3. **Discrete Mathematics & Structural Tools**:
   - *Logic and Truth*, *Drawing Sets*, *Rearranging Formulae*, *When There Is No Answer*.
4. **Notebook & Coursework Conversions**:
   - Adapt PDP modules (*How We Got Here*, *When It Goes Wrong*) from existing coursework notebooks.
5. **Practice Problem Sets**:
   - Convert upstream worksheets from `deweydex/Mathematics` to accompany completed modules following [`planning/EXERCISES.md`](./EXERCISES.md).
