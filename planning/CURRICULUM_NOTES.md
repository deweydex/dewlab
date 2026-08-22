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

---

## 2026-08-22 — Tutorials 13 and 14, and where the foundations sit

Josh's read: 13 and 14 are a mishmash and want expanding into a tutorial each,
and probably want to come earlier. Half agreed, and the half that is not is
worth saying.

### 13 is a mishmash. 14 is not.

**Tutorial 13, Numbers and Their Families** (254 lines, 12 cells) holds three
unrelated topics under one title:

| Section | Outcome | What it actually is |
|---|---|---|
| The Number Domains | `MIT-2.1` | Set theory |
| Indices (Powers) and Their Rules | `MIT-1.1` | Algebra |
| Logarithms: The Inverse of Powers | `MIT-1.1` | Algebra |
| Practical Geometry: Formulas as Functions | `MIT-1.2`, `MIT-1.3` | Mensuration |
| Putting It Together: A Number Explorer | — | Synthesis of all three |

Nothing links them except that all three appear in Section 1 of the descriptor.
A student cannot say what this tutorial was about.

**Tutorial 14, Expressions Come Alive** (268 lines, 14 cells) is the opposite:
representing, evaluating, displaying, adding, multiplying, subtracting and
scaling polynomials — one topic, done properly, in a sensible order. The only
outlier is the opening *Expressions versus Equations* section, which is
vocabulary rather than a topic, and which `out-of-scope.yaml` has already
decided not to assess.

So 14 does not need splitting. It may need *moving*, which is a different
argument, below.

### The duplication nobody noticed

Tutorial 2, at *Data Types*, already says this:

> **Integers** (`int`) … These correspond to the mathematical integers, which
> mathematicians call **Z** … **Floating-point numbers** (`float`) … These
> approximate the real numbers (**R**)

Tutorial 13, eleven tutorials later, teaches ℕ ⊂ ℤ ⊂ ℚ ⊂ ℝ as its own section
with a `classify_number` exercise. The shallow version arrives first and the
real one arrives when nobody is expecting it. That is the wrong way round.

### The foundations are taught after the things that use them

MIT Section 1 is *Basic Arithmetic and Algebra*. In dewlab it is taught at
positions 13 to 15 — after counting and probability (9, 10), after statistics
(11, 12). Two concrete consequences:

- Tutorial 9 works with factorials and Tutorial 11 with standard deviation.
  Both lean on powers and roots, which Tutorial 13 teaches four tutorials later.
- Tutorial 2 needs the number domains and settles for two sentences about them.

This is an artefact of the source notebooks' numbering, not a decision anybody
made.

### Proposal: split 13 three ways and place each piece where it is needed

- **Number domains → into Tutorial 2, or immediately after it.** It is the same
  idea as `int` versus `float`, and Tutorial 2 is already half-teaching it. This
  is the strongest of the three moves.
- **Indices and logarithms → before Tutorial 9.** Powers and roots are the
  arithmetic that counting, standard deviation and polynomials all assume.
  Expanded, this is a full tutorial: index laws, roots as fractional powers,
  logarithms as the inverse, and why a computer's `log` has a base.
- **Practical geometry → straight after functions are introduced** (Tutorial 5
  or 8). "A formula is a function" is the best first use of a function there is,
  and it currently sits eight tutorials past the point where it would land.

Tutorial 14 then follows indices naturally, and still precedes 15. Whether it
moves earlier depends on whether the indices tutorial moves, not on anything
about 14 itself.

### This is the argument for dropping the numbers

Every move above renumbers everything after it — 50 prose references, 17 titles,
17 slugs, and only three cross-links the build can check
(`curriculum/DECISIONS_NEEDED.md`, question 5). Doing this *and* inserting the
new maths tutorials means two renumberings.

Dropping the numbers from titles once makes both free, and this is the clearest
case yet for it: the reordering is worth doing on its own merits, and the
numbering is the only thing making it expensive.
