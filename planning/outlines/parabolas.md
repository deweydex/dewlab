# Outline — Parabolas

**Closes:** `MIT-3.4` (complete the square to find roots and vertex).
**Goes after:** [Drawing Functions](./drawing-functions.md).
**Builds on:** Tutorial 14 (polynomials), Tutorial 15 (solving), Drawing
Functions (plotting a function and reading an answer off it).
**Size:** short, and not thin.

## Why it is not a section of Drawing Functions

Josh asked for graphing to be more than one tutorial, and this is the natural
seam. Drawing Functions is about the habit — plot the thing, read the answer.
This is about one curve in particular, and about a piece of algebra whose entire
payoff is a fact about that curve.

Kept together, the algebra gets rushed to reach the picture. Completing the
square is fiddly, most students have met it as a trick, and it deserves the
space to be shown as the rearrangement it actually is.

Kept apart, it also has somewhere to put the thing students most want from a
quadratic and rarely get: *where does it turn, and why is that the same
question as where it crosses.*

## The naming and describing decisions

**Completing the square is rewriting, not solving.** The students met quadratics
in Cracking Equations and solved them with the formula. Nothing here contradicts
that. What changes is the *form*: `x² + 6x + 5` and `(x + 3)² − 4` are the same
function, and the second one tells you where the bottom of the curve is by
looking at it. Say that first, and the manipulation has a reason.

**The vertex before the roots.** The usual order is roots, then vertex as an
afterthought. Reversed, completing the square answers the question it is best at
first, and the roots come out of the same form for free — set it to zero and
take a square root. That also makes the negative case obvious: if the bottom of
the curve is above the axis, there is nothing to find, and no formula will
conjure one. Which is the tutorial that comes before this one.

**"Parabola" is a name for a shape, said once.** It is not a topic. Every
quadratic makes one, they all look the same up to stretching and sliding, and
that is worth demonstrating rather than asserting.

## The shape

### 1. Every quadratic is the same curve

- **Cell:** several quadratics plotted on one pair of axes.
- **Cell:** each one shifted and stretched onto `y = x²`. They land on top of
  each other.
- **Point to make:** there is one parabola. Everything else is it, moved.

### 2. The form that tells you where the bottom is

- **Cell:** `x² + 6x + 5` and `(x + 3)² − 4` evaluated over a range and compared
  point by point. Identical.
- **Cell:** the second form plotted, with `(−3, −4)` marked. The two numbers in
  the expression are the two coordinates of the turning point.
- **Point to make:** this is why anyone completes the square. The answer is
  sitting in the expression.

### 3. Doing the rearrangement

- **Cell:** the steps, one per line, printed as the expression changes — halve
  the middle coefficient, square it, add and subtract it.
- **Cell:** a `complete_the_square(a, b, c)` the student writes, returning the
  three numbers, checked by plotting both forms.
- **Your turn:** four quadratics by hand, then checked against the function.
- **Point to make:** the halving is the whole trick, and it is there because
  `(x + h)²` has `2h` in the middle. Show that expansion first and the step
  stops being arbitrary.

### 4. Roots, from the same form

- **Cell:** set the completed form to zero and take the square root. The
  quadratic formula, derived rather than quoted.
- **Cell:** the same three quadratics from Cracking Equations, solved both ways,
  agreeing.
- **Point to make:** the formula they have been using *is* completing the square,
  done once in general so nobody has to do it again.

### 5. When there is nothing to find

- **Cell:** a parabola whose bottom is above the axis, plotted.
- **Point to make:** no roots is a fact about the picture, not a failure of the
  method — and it is where the previous tutorial's complex roots come from.

## What to reuse

The plotting helper from Drawing Functions and `evaluate_polynomial` from
Tutorial 14, both unchanged.

## Open questions

- **Whether to do `a ≠ 1`.** Completing the square with a leading coefficient is
  more algebra for the same insight. It could be a closing section, a bonus, or
  left out with a note — and the answer probably depends on whether the exercise
  sheets that follow ask for it.
