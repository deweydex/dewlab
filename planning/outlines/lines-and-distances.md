# Outline — Lines and Distances

**Closes:** `MIT-4.1` (linear equations as `ax + by + c = 0`), `MIT-4.2` (slope;
parallel and perpendicular), `MIT-4.3` (midpoint and length of a segment),
`MIT-4.4` (the Pythagorean theorem).
**Goes after:** Drawing Functions.
**Goes before:** Angles and Waves, which needs coordinates for the unit circle.
**Builds on:** Tutorial 12 (plotting), Drawing Functions (a function has a
picture).
**Size:** full.

## Why it is a tutorial rather than a section

`drawing-functions.md` currently carries a conditional: *"If coordinate geometry
is kept: `MIT-4.1`, `MIT-4.2`, `MIT-4.3`."* That was written when most of
Section 4 was out of scope, and it is no longer the right shape for two reasons.

Pythagoras is **one of the six gateways in the topic tree** — it unlocks seven
downstream topics, more than any other candidate, which is why it became a
Pythagoras serves as a critical gateway unlocking seven downstream topics in
the topic tree. A gateway requires a dedicated tutorial rather than an embedded
subsection within graphing.

Furthermore, downstream trigonometry (*The Unit Circle*, *Solving Triangles*)
assumes coordinate geometry: the unit circle is a coordinate-geometry object
(a locus of points at distance 1 from the origin). Having a dedicated tutorial
prevents trigonometry from having to introduce Cartesian coordinates in passing.

Drawing Functions focuses on plotting functions, while coordinate slope,
midpoint, and Euclidean distance are established here.

---

## Pedagogical & Terminology Architecture

The following pedagogical choices structure the tutorial:

### What to call it

**"Lines and Distances"**, and not "Coordinate Geometry".

The descriptor's phrase is the descriptor's business. For an adult learner
returning to education — which is most of this cohort — *geometry* is the name of
a thing they did at fifteen and possibly did badly. It carries theorems, proofs,
and a compass. Nothing in this tutorial is that.

"Lines and Distances" names the two things a student walks out with: how to
describe a line, and how far apart two things are. Both are answers to questions
somebody might already have.

### A line: three descriptions, in an order that earns each one

The students have been writing `def f(x): return 2*x + 1` since Tutorial 8. The
descriptor asks for `ax + by + c = 0`. Between those sit `y = mx + c`. Teaching
them in the descriptor's order means opening with the least familiar and least
motivated of the three.

The order that works is the reverse, and it makes the general form arrive as an
answer rather than a convention:

1. **A line is a function you have already written.** `slope * x + intercept`.
2. **`y = mx + c` is the same thing with the parts named.** No new idea, only
   vocabulary — and now the two numbers have jobs.
3. **`ax + by + c = 0` exists because of one line the other two cannot draw:
   a vertical one.** `x = 3` has no slope; the function form cannot express it
   and `y = mx + c` divides by zero trying. The general form can. That is the
   whole reason it is in the syllabus, and a student who sees the vertical line
   fail first will never need to memorise the form.

That third point is the tutorial's best moment and it should not be given away
early. Let them try to plot `x = 3` with the tools they have.

### Slope: name it as a rate of change from the start

"Rise over run" and "how much y changes when x goes up by one" are the same
number. The first is a mnemonic; the second is a sentence about the world, and it
is what Rates of Change needs three tutorials later.

Committing to the second here means the derivative arrives as *the slope of a
curve that keeps changing* rather than as a new idea with new vocabulary. The
cost is one phrase used consistently. Worth deciding now because it is a
commitment across Lines and Distances, Approaching a Limit, and Rates of Change.

"Rise over run" still gets said once, because students will meet it elsewhere and
should recognise it.

### Distance before Pythagoras, so the theorem is earned

The distance formula *is* Pythagoras, with the right-angled triangle drawn
between the two points rather than handed over. The order matters:

- Ask for the distance between two points. Let them find the horizontal gap and
  the vertical gap easily and then be stuck.
- Draw the triangle those two gaps make. The distance is the third side.
- **Then** name the theorem.

Taught the other way round, Pythagoras is a fact to accept and the distance
formula is an application of it. Taught this way, the theorem is the answer to a
question they were already asking, and the formula is not a separate thing to
remember. For a gateway topic, that difference is the point.

### Perpendicular slopes: draw it rather than state it

`m₁ × m₂ = −1` is easy to state and impossible to believe on sight. The
describable version is a picture: take the right triangle under a line, turn it a
quarter turn, and rise and run have swapped places with one of them changing
sign. The rule falls out of the swap.

This is a place where the runnable cell does something a textbook cannot — turn
the triangle and watch the numbers exchange.

### Where practical right-triangle trigonometry goes

`MIT-4.9` — heights and distances from one angle and one side — is the fifth
unplanned outcome and it is not in this tutorial.

It needs SOH-CAH-TOA, which arrives in Angles and Waves. Teaching the ratios here
so that 4.9 can live here means teaching them twice, or teaching them here and
having Angles and Waves refer backwards to a tutorial about coordinates for its
central definition. Both are worse than the alternative.

**Proposal: a short tutorial after Angles and Waves**, working title *How Tall Is
That?* — ladders, roof pitches, the height of a building from its shadow. It
builds on this tutorial for Pythagoras and on Angles and Waves for the ratios,
which is the natural order, and it is the one piece of Section 4 that is
straightforwardly about measuring something in the world.

---

## The shape

### 1. A line you have already written

- **Cell:** the students' own `f(x) = 2x + 1` from Tutorial 8, plotted with the
  machinery from Drawing Functions.
- **Cell:** change the 2, then change the 1, plotting each time on one pair of
  axes. Two numbers, two different effects.
- **Point to make:** everything in this tutorial is about those two numbers.

### 2. Slope, as how fast something changes

- **Cell:** a `slope(p, q)` the student writes from two points.
- **Cell:** the same slope computed from three different pairs of points on one
  line, agreeing every time. That agreement is what "straight" means.
- **Your turn:** given a table of (hours worked, pay), find the hourly rate.
  Slope with the mathematics taken out of it.
- **Point to make:** the number answers "if x goes up by one, what happens to
  y?" — which is a question about the world, not about graphs.

### 3. Parallel and perpendicular

- **Cell:** several lines plotted; group them by slope. Parallel needs no rule.
- **Cell:** the quarter-turn. Take the rise and run of a line, swap them, negate
  one, plot both. Then multiply the two slopes.
- **Your turn:** given a line and a point, find the perpendicular through it.
- **Point to make:** the rule is the picture written down, not a fact to hold on
  to separately.

### 4. The line that breaks the formula

- **Cell:** try to plot `x = 3` as a function. Watch it fail, or watch `y = mx +
  c` divide by zero.
- **Cell:** `ax + by + c = 0`, and the same vertical line expressed in it.
- **Cell:** convert between the two forms in both directions.
- **Point to make:** the general form is not a stricter way of writing the same
  thing. It describes one more line than the others can.

### 5. Midpoint, which needs no theory

- **Cell:** the average of two points, and the plot showing it lands between
  them.
- **Your turn:** the midpoint of a route between two towns, from real
  coordinates.

### 6. How far apart, and the theorem that answers it

- **Cell:** the horizontal gap and the vertical gap between two points. Easy.
- **Cell:** now the direct distance. Let them attempt it before the reveal.
- **Cell:** draw the triangle. The two gaps are the short sides.
- **Cell:** `a² + b² = c²`, checked against several triangles, then the general
  `distance(p, q)`.
- **Point to make:** the distance formula and Pythagoras are one thing seen from
  two directions. Neither is a special case of the other.

### 7. Where you will meet this again

Short and forward-looking rather than a summary.

- **Cell:** a circle of radius one, plotted from the distance formula — every
  point exactly 1 from the origin. Nothing is said about trigonometry.
- **Point to make:** that circle is where the next tutorial starts.

## What to reuse

The plotting helper from Drawing Functions, unchanged. `slope(p, q)` and
`distance(p, q)` are written here and used by Angles and Waves, the
right-triangle tutorial, and Rates of Change — worth naming them once and
keeping the names.

## Open Questions
- **Title Finalization**: Evaluate "Lines and Distances" versus alternatives against reader accessibility criteria.
- **Hook Effectiveness**: Evaluate whether the closing geometric circle construction effectively motivates *The Unit Circle*.
