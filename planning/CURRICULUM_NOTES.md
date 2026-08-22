# Curriculum notes

A running log of what we have decided about the curriculum, what we have
noticed, and what we are still arguing about. Newest at the top.

It exists because the decisions are the expensive part. Rebuilding the
[curriculum map](./CURRICULUM_MAP.md) takes a second; working out again why we
left Venn diagrams out takes a conversation. Anything settled here should end up
in `curriculum/out-of-scope.yaml` or the tutorials themselves — this is the
working surface, not the record.

## Where the pieces live

| File | What it is |
|---|---|
| [`CURRICULUM_MAP.md`](./CURRICULUM_MAP.md) | Generated. Every outcome, its state, and a link to where it is taught. |
| [`curriculum/outcomes.yaml`](./curriculum/outcomes.yaml) | Every learning outcome in the two module descriptors. |
| [`curriculum/out-of-scope.yaml`](./curriculum/out-of-scope.yaml) | What we have decided not to teach, and why. |
| [`curriculum/proposed.yaml`](./curriculum/proposed.yaml) | Tutorials that do not exist yet and where each would go. |
| [`curriculum/DECISIONS_NEEDED.md`](./curriculum/DECISIONS_NEEDED.md) | The six open questions, set out so they can be answered. |
| [`outlines/`](./outlines/) | One outline per proposed tutorial. |
| each tutorial's `covers:` frontmatter | Which outcome each section teaches, and which it only uses. |

---

## 2026-08-22 — The map exists, and it says what we thought it would

**41 of 65 outcomes in place** once the two ruled out are set aside. The
distribution is not even slightly even:

- **Complete:** algorithms (9 of 9), probability (8 of 8), statistics (5 of 5),
  number, sets. Everything the converted notebooks were already good at.
- **Empty:** calculus (0 of 3), trigonometry (0 of 6), functions (0 of 3), logic
  (0 of 2). Every one of these is mathematics rather than programming.
- **Partial:** geometry (2 of 6), programming (7 of 11), algebra (6 of 8).

Josh's read was right: polynomials are actually well covered — Tutorial 14 does
representation, evaluation, addition and multiplication properly — but polynomial
*graphing* is not, and neither is anything after it.

### Four quiet gaps worth more than their count

Four outcomes are used but never taught, and these are the dangerous ones,
because a coverage table built from filenames would call them covered:

- `MIT-2.4` truth tables — students write `and`/`or`/`not` from Tutorial 3
  onwards and never see one laid out.
- `MIT-1.10` complex roots — Tutorial 15 computes the discriminant, finds it
  negative, and stops at "no real solutions".
- `MIT-3.1` inverse functions — Tutorial 6 mentions functions as mappings in
  passing.
- `MIT-1.7` transposing formulae — nothing anywhere, and every other subject
  assumes it.

### What the back-reference arrows showed

The map draws an arrow wherever one tutorial names an earlier one in its own
text. Two things fell out:

- **Tutorial 17 refers back to five different tutorials.** It is doing its job as
  a synthesis, and it is the most expensive tutorial in the series to move.
- **Tutorials 2, 3, 5, 8, 11, 13 are named by nobody.** Not a problem in itself —
  a tutorial can be foundational without being cited — but 8 (Building Reusable
  Tools) being uncited is odd, since its whole point is producing tools for
  later use. Worth a look at whether later tutorials should be reaching back to
  it explicitly.

### Ordering

The proposals cluster after Tutorial 15, which is the honest place for them —
graphing needs polynomials and solving first. That does mean the maths half of
the course gets substantially longer at the end, and the two cheap PDP
conversions want to go near the *front* (after Tutorials 1 and 3). Slotting them
in renumbers everything after them, which is a real cost. Nothing in
`proposed.yaml` has been given an `order` for that reason.

---

## 2026-08-22 — everlearning has far more reusable material than expected

`PDP_MIT_2026_2027_Integrated/LearningOutcomes/MIT/` holds **seven finished
worksheets, 3,072 lines and 486 problems, every one with an answer key**, and
between them they cover almost exactly the gaps the map found: quadratic
graphing and completing the square, graphing sine and cosine, derivatives and
integrals, the differentiation rules, coordinate geometry, right-triangle
trigonometry, and radians.

This changes what Phase 6 is. It is not "write the mathematics half of the
course"; it is "convert seven worksheets, cut what is out of scope, and add the
cells that make dewlab worth using instead of a PDF".

Two things follow:

- **The scope decisions are now decisions about specific parts of specific
  files**, which is what made `DECISIONS_NEEDED.md` writable. The chain-rule
  exclusion, for instance, cuts 62 of the 74 problems in the `MIT-3.7`
  worksheet — a fact worth knowing before confirming it.
- **`MIT-3.6` is the best-matched source of the seven.** All 82 problems are
  within scope as written: power rule both directions, the constant of
  integration, sums, polynomials, and a Fundamental Theorem preview. Nothing
  needs cutting.

### Renumbering is a 50-place edit nothing checks

Measured while working out what inserting a tutorial would cost: **50 prose
references by number** ("your functions from Tutorial 11"), 17 numbered titles,
17 numbered slugs — and only **three** cross-links use the `tutorial:slug`
syntax the build validates. So the build would catch almost none of a
renumbering.

`order:` in the frontmatter is what actually sequences a series; the number in
the title is decoration the build never reads. Placement and numbering are
therefore separable, which is the argument for dropping the numbers once and
placing freely thereafter.

---

## Ideas not yet acted on

- **Coordinate geometry is homeless and cheap.** `MIT-4.1`–`4.3` (slope,
  midpoint, length) would cost half a section inside Drawing Functions and are
  the one part of Section 4 the programming half of the course can use directly.
  Awaiting a decision — listed under `undecided` in `out-of-scope.yaml`.
- **`plot_function` should be written once and reused.** Drawing Functions,
  Angles and Waves, Approaching a Limit and Rates of Change all need it. If it is
  written four times, the series is teaching the opposite of Tutorial 8.
- **The symbolic differentiate/integrate pair** over Tutorial 14's polynomial
  representation is the strongest argument in the whole plan for dewlab as a
  format rather than a worksheet. It should be the centrepiece of Rates of
  Change, not a closing exercise.
- **Tutorial 15 may want revising rather than extending.** Both the complex-roots
  outline and the completing-the-square section of Drawing Functions take
  material that arguably belongs in 15. Worth deciding once rather than twice.
- **A "used but not taught" state should be visible to students too.** The map
  knows which sections only touch an outcome. A tutorial could say so — "you have
  used this; here is where it gets taught properly" — which would make the series
  honest about its own gaps.
