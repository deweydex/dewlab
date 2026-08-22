# Outline — Rates of Change

**Closes:** `MIT-3.6` (derivative as limit, tangent, rate of change), `MIT-3.7`
(sum and product rules only — chain and quotient are out of scope).
**Goes after:** Approaching a Limit.
**Builds on:** Approaching a Limit, Drawing Functions.

## Scope

Sum and product rules. Not chain, not quotient — see
`planning/curriculum/out-of-scope.yaml`. Polynomial integration as the closing
idea, and nothing beyond polynomials.

## The shape

### 1. The slope between two points

- **Cell:** pick two points on a curve, compute the slope of the line between
  them, plot both.
- **Cell:** move the second point closer. The line pivots. Print the slope each
  time.
- **Point to make:** this is the previous tutorial's limit, wearing a hat.

### 2. The derivative

- **Cell:** a `derivative_at(f, x, h)` using the difference quotient, with h
  shrinking.
- **Cell:** compare against the answer from the power rule for a handful of
  polynomials. They agree, which is the argument that the rule is not magic.
- **Point to make:** the rule is a shortcut for something they have now
  computed the slow way.

### 3. Rules that compose

- **Cell:** a symbolic `differentiate` over the Tutorial 14 polynomial
  representation. This is a genuinely satisfying twenty lines: the students'
  own data structure from a fortnight ago, differentiated.
- **Cell:** the sum rule, checked by differentiating `f + g` and comparing with
  `f' + g'`.
- **Cell:** the product rule, same treatment.
- **Your turn:** differentiate by hand, check with the function.

### 4. What a derivative tells you

- **Cell:** plot a function and its derivative on stacked axes. Where the
  derivative crosses zero, the function turns.
- **Your turn:** given a distance-time table, produce speed. Given speed,
  identify where the object was speeding up.
- **Point to make:** "rate of change" is not a second meaning of derivative. It
  is the same thing, asked about a different quantity.

### 5. Running it backwards

- **Cell:** an `integrate` over the same polynomial representation. Differentiate
  its output and get the original back — the check is the lesson.
- **Cell:** area under a curve by adding up rectangles, compared against the
  answer the integral gives.
- **Point to make:** the constant of integration is exactly what the round trip
  loses, and the cell can show it losing it.

## Note

The symbolic `differentiate`/`integrate` pair over the Tutorial 14 polynomial
representation is the strongest argument in this outline for dewlab as a format
rather than a worksheet. It should be the centrepiece.
