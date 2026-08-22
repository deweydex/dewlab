# Outline — Rearranging Formulae

**Closes:** `MIT-1.7` (transpose formulae; operate on rational algebraic
expressions).
**Goes after:** Tutorial 14, Expressions Come Alive.
**Builds on:** Tutorial 14.
**Size:** short.

## Why it exists

The one algebra outcome with no home anywhere. Tutorial 14 builds expressions
and Tutorial 15 solves equations; getting a formula into the shape you need sits
exactly between the two, and every other subject these students take assumes
they can already do it.

## The shape

### 1. The same formula, five ways

- **Cell:** `v = u + a*t` as five Python functions, one per unknown.
- **Point to make:** writing the five functions is transposition. The algebra
  and the code are the same work, and the code makes the point that no version
  is more "correct" than another.

### 2. The moves

- Doing the same thing to both sides, one operation at a time.
- **Cell:** a worked transposition with each step printed and each step checked
  numerically against the original.
- **Your turn:** transpose three formulae from physics or finance, checking each
  the same way.

### 3. When the unknown is underneath

Rational expressions: the unknown in a denominator, and what multiplying through
does.

- **Cell:** the lens formula or a parallel-resistance formula, transposed.
- **Cell:** what happens numerically when a denominator hits zero, and why the
  algebra warned about it first.

### 4. Checking yourself

- **Cell:** a `check_transposition(original, rearranged, **values)` that
  substitutes random numbers into both and compares.
- **Point to make:** a rearrangement is right if it agrees with the original for
  every input, and the student can now test that instead of hoping.

## Note

Short, and it could be folded into the end of Tutorial 14 rather than standing
alone. Standing alone is the recommendation only because Tutorial 14 is already
long.
