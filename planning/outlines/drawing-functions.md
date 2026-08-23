# Outline — Drawing Functions

**Closes:** `MIT-3.1` (function and inverse function), `MIT-3.2` (graph linear,
quadratic and cubic; solve from a graph), `MIT-3.4` (complete the square).
**Followed by:** [Lines and Distances](./lines-and-distances.md), which takes
the straight line seriously. This outline used to carry `MIT-4.1` to `MIT-4.3`
conditionally, written while most of Section 4 was out of scope; they have their
own tutorial now.
**Goes after:** Tutorial 15, Cracking Equations.
**Builds on:** 12 (plotting), 14 (polynomials), 15 (solving).

## Why this one first

This is the largest single gap and the one that unlocks the rest of the
mathematics. The students can already build a polynomial, solve it, and plot a
dataset. Nobody has yet asked them to plot a *function* and read an answer off
the picture — which is the habit every later tutorial depends on. Trigonometry
is a graph. A limit is a graph. A derivative is the slope of a graph.

It also fixes something slightly odd about the current series: Tutorial 12
teaches plotting for data and never comes back to it, and Tutorial 14 builds a
polynomial evaluator that never gets drawn.

## The shape

### 1. A function is a machine, and a machine has a picture

Pick up `evaluate_polynomial` from Tutorial 14 and plot it. One cell, and the
students see their own code from a fortnight ago produce a curve.

- **Cell:** paste the Tutorial 14 evaluator, feed it a range of x values, plot.
- **Point to make:** the list of (x, y) pairs and the curve are the same thing.

### 2. Straight lines

Linear functions, and slope as the thing that makes them different from each
other.

- **Cell:** a `plot_line(m, c)` the student writes, called several times on one
  pair of axes.
- **Your turn:** which of these lines look parallel? Plot them and see.

Slope from two points, the perpendicular rule, and distance all move to Lines
and Distances. Here a line is one more function to draw; there it becomes a
thing with parts that have names.

### 3. Curves that bend

Quadratics, then cubics, with the same plotting function.

- **Cell:** plot `x**2`, then `2*x**2`, then `x**2 + 3`, then `(x-2)**2`, one
  change at a time. The student predicts before running.
- **Point to make:** each coefficient does one recognisable thing to the shape.

### 4. Completing the square

Where the vertex comes from, and why the algebra is worth doing.

- **Cell:** a function returning `(h, k)` for `a(x-h)^2 + k`.
- **Cell:** plot the original and mark the vertex the algebra predicted. The
  point lands on the curve, which is the whole argument.
- **Your turn:** complete the square by hand for three quadratics, then check
  each with the function.

### 5. Solving by looking

Where a curve crosses the x-axis, and where two curves cross each other.

- **Cell:** plot a quadratic and its roots from Tutorial 15's solver on the same
  axes.
- **Cell:** plot `f(x)` and `g(x)`, find the intersection numerically, mark it.
- **Point to make:** "solve `f(x) = g(x)`" and "find where the curves cross" are
  the same instruction in two languages. This is `MIT-3.2`'s second half, and
  the students have already done the algebraic version in Tutorial 15.

### 6. Undoing a function

Inverse functions, which is `MIT-3.1` and currently the weakest thing in the
series — Tutorial 6 mentions functions as mappings and moves on.

- **Cell:** a function and its inverse plotted together, with `y = x` dashed
  between them. The reflection is the definition, seen rather than stated.
- **Cell:** a function that has no inverse over its whole domain (`x**2`), and
  what restricting the domain fixes.
- **Point to make:** Tutorial 13 already taught logarithms as the inverse of
  powers. This names the pattern they met there.

## What to reuse

`plot_function(f, lo, hi)` should be written once in section 1 and used for the
rest of the tutorial — it is the reusable-function habit from Tutorial 8 applied
to something the student will actually keep using.

## Open questions

- Does coordinate geometry (`MIT-4.1`–`4.3`) come in here, or not at all? It is
  cheap here and homeless otherwise. Listed as undecided in
  `out-of-scope.yaml`.
- This tutorial is long. It may want to be two: straight lines and curves, then
  solving and inverses.
