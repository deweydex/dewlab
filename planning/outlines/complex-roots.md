# Outline — When There Is No Answer (And Then There Is)

**Closes:** `MIT-1.10` (solve quadratics including complex roots).
**Extends:** `MIT-2.1` (the set ℂ).
**Goes after:** Tutorial 15, Cracking Equations.
**Builds on:** Tutorial 15, Tutorial 13.
**Size:** short.

## Why it exists

Tutorial 15 computes the discriminant, finds it negative, prints "no real
solutions", and stops. Every version of this in the source material stops in the
same place. The descriptor asks us to keep going, and the stopping point is a
good story rather than a gap to plug quietly: the answer was there all along and
the students were told it was not.

It also completes Tutorial 13's tour of the number domains, which lays out ℕ, ℤ,
ℚ, ℝ and leaves ℂ unmentioned.

## The shape

### 1. The cliff edge

- **Cell:** the Tutorial 15 solver, given `x² + 1 = 0`. It says there is no
  answer.
- **Cell:** plot it. The parabola misses the x-axis, which is what "no real
  root" looks like.
- **Point to make:** "no real solutions" is a true statement about the reals, and
  a smaller claim than it sounds.

### 2. Inventing a number

- **Cell:** Python's `1j`, and `(1j)**2` returning `-1`.
- **Cell:** the number domains from Tutorial 13, with ℂ added on the end.
- **Point to make:** each domain in that tour was invented because the previous
  one could not answer a question. ℂ is the same move one more time, not a
  special case.

### 3. Roots that are not real

- **Cell:** the quadratic formula with `cmath.sqrt` instead of `math.sqrt`, and
  the same three cases falling out of one code path.
- **Cell:** substitute a complex root back into the original and get zero. That
  check is the argument.
- **Your turn:** solve three quadratics by hand in a+bi form, check each.

### 4. Conjugates

- **Cell:** the two roots of any real quadratic, printed together. The pattern is
  visible before it is named.
- **Point to make:** they always arrive in pairs, and the plot explains why — a
  parabola crosses the axis twice, once, or not at all.

## Note

Short, and it depends on Tutorial 15's solver, so the two should be written or
revised together. If Tutorial 15 is revised anyway, the alternative is to extend
its quadratic section rather than write a new tutorial — cheaper, but it loses
the number-domains connection, which is the better half of this.
