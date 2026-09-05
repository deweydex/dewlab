---
title: "When There Is No Answer — Practice"
slug: complex-roots-practice
practice_for: complex-roots
module: mit-pdp-maths-prog-integration
module_title: "Programming and Maths, Integrated"
year: "2026-2027"
series: algebra-and-functions
version: 2026.08.23.1
---

# When There Is No Answer — Practice

Answers are folded. The checking cell will confirm a root by substituting it back — which is the argument, not just a convenience.

## Tools

```python exec
id: tools-1
import cmath

def solve(a, b, c):
    discriminant = b ** 2 - 4 * a * c
    root = cmath.sqrt(discriminant)
    return ((-b + root) / (2 * a), (-b - root) / (2 * a))


def evaluate(a, b, c, x):
    return a * x ** 2 + b * x + c


for coefficients in [(1, 0, 1), (1, -5, 6), (1, 2, 5)]:
    a, b, c = coefficients
    first, second = solve(a, b, c)
    print(f"{a}x^2 + {b}x + {c}:  {first}  and  {second}")
    print(f"   substituted back: {evaluate(a, b, c, first)}  {evaluate(a, b, c, second)}")
```

## Imaginary Arithmetic

**1.** Simplify: `i²`, `i³`, `i⁴`, `i⁵`.

<details class="dl-answer"><summary>answer</summary>

−1, −i, 1, i.

The powers cycle every four, because `i⁴ = 1` and multiplying by 1 changes nothing. So `i¹⁰⁰` is 1 and `i¹⁰¹` is i.

</details>

**2.** Compute `(3 + 2i) + (1 − 5i)` and `(3 + 2i) − (1 − 5i)`.

<details class="dl-answer"><summary>answer</summary>

`4 − 3i` and `2 + 7i`.

Real parts with real parts, imaginary with imaginary — exactly like collecting like terms.

</details>

**3.** Compute `(3 + 2i)(1 − 4i)`.

<details class="dl-answer"><summary>answer</summary>

`3 − 12i + 2i − 8i²`. The last term is `−8 × (−1) = +8`, so it comes to `11 − 10i`.

The `i²` collapsing into a real number is the only unusual step, and it is the definition doing its work.

</details>

**4.** Compute `(2 + 3i)(2 − 3i)`.

<details class="dl-answer"><summary>answer</summary>

`4 − 6i + 6i − 9i² = 4 + 9 = 13`.

A number multiplied by its conjugate always gives a real answer — the imaginary parts cancel. That is the trick for dividing complex numbers: multiply top and bottom by the bottom's conjugate.

</details>

**5.** What is the conjugate of `5 − 7i`? Of `4`? Of `2i`?

<details class="dl-answer"><summary>answer</summary>

`5 + 7i`, `4`, and `−2i`.

A real number is its own conjugate, because there is no imaginary part to flip.

</details>

## Solving

**6.** Solve `x² + 4 = 0`.

<details class="dl-answer"><summary>answer</summary>

`x² = −4`, so `x = ±2i`.

</details>

**7.** Solve `x² − 2x + 5 = 0`.

<details class="dl-answer"><summary>answer</summary>

Discriminant: 4 − 20 = −16, so `√(−16) = 4i`.

`x = (2 ± 4i)/2 = 1 ± 2i`.

</details>

**8.** Solve `x² + 6x + 13 = 0`.

<details class="dl-answer"><summary>answer</summary>

Discriminant: 36 − 52 = −16.

`x = (−6 ± 4i)/2 = −3 ± 2i`.

</details>

**9.** Check one of your answers by substituting it back into the original.

<details class="dl-answer"><summary>answer</summary>

For `x = 1 + 2i` in `x² − 2x + 5`:

`(1 + 2i)² = 1 + 4i + 4i² = 1 + 4i − 4 = −3 + 4i`.
`−2(1 + 2i) = −2 − 4i`.
Adding: `−3 + 4i − 2 − 4i + 5 = 0`.

**That substitution is the argument.** A root is a number that makes the expression zero; this makes it zero; so it is a root, whatever it looks like.

</details>

**10.** `x² − 6x + 25 = 0` has a root at `3 + 4i`. What is the other, and how do you know without computing?

<details class="dl-answer"><summary>answer</summary>

`3 − 4i`, the conjugate.

For a quadratic with real coefficients, the only place an `i` can enter is the square root of a negative discriminant, and it enters once with a `+` and once with a `−`. So complex roots always arrive in conjugate pairs.

</details>

## Understanding the Discriminant

**11.** For each, say how many real roots without solving.

- (a) `x² − 7x + 12`
- (b) `x² + x + 1`
- (c) `4x² − 12x + 9`

<details class="dl-answer"><summary>answer</summary>

(a) Discriminant 49 − 48 = 1, positive: two real roots.
(b) 1 − 4 = −3, negative: none — two complex ones.
(c) 144 − 144 = 0: one repeated real root, at 1.5.

</details>

**12.** What does a negative discriminant look like on a graph?

<details class="dl-answer"><summary>answer</summary>

The parabola misses the horizontal axis entirely — it sits wholly above it, or wholly below.

The roots have not disappeared; they are not on the real line. "No real solutions" is a statement about which numbers you are willing to consider.

</details>

**13.** Can a quadratic with real coefficients have exactly one complex root and one real one?

<details class="dl-answer"><summary>answer</summary>

No. They come in conjugate pairs, so either both are real or both are complex.

The picture says the same: a parabola crosses the axis twice, touches once, or misses. There is no shape that crosses once and stops.

</details>

## Why Any of This Exists

**14.** Each extension of the number system was made because something had no answer. Match each to the question that forced it: ℤ, ℚ, ℝ, ℂ.

<details class="dl-answer"><summary>answer</summary>

ℤ — `3 − 5`, because subtraction escaped the counting numbers.
ℚ — `3 ÷ 5`, because division escaped the integers.
ℝ — `√2`, because roots escaped the fractions.
ℂ — `√−1`, because roots of negatives escaped the reals.

Each one was resisted when it was new, and each is now taught to children.

</details>

**15.** Adding complex numbers made the solver *shorter*. Why is that a good sign?

<details class="dl-answer"><summary>answer</summary>

Because the `if discriminant < 0` special case disappeared. The three separate situations — two roots, one root, none — turned out to be one situation seen from somewhere you can see all of it.

A generalisation that removes special cases is usually the right generalisation. One that adds them is usually a patch.

</details>

**16.** Does every polynomial equation have a solution in ℂ?

<details class="dl-answer"><summary>answer</summary>

Yes — that is the Fundamental Theorem of Algebra, and it is why ℂ is the last extension you need for this purpose.

A polynomial of degree n has exactly n roots in ℂ, counting repeats. No such statement is true of ℝ, ℚ, ℤ or ℕ.

</details>

## In Use

**17.** Where do complex numbers turn up outside a maths class?

<details class="dl-answer"><summary>answer</summary>

Alternating current, where a complex number carries both the size and the timing of a signal at once. Signal processing, where the Fourier transform is built on them. Control systems, where where the roots sit tells you whether a system is stable. Computer graphics, where their bigger cousins the quaternions handle rotation without the failure modes of angles.

In every one of those the complex number is doing real work — it is not decorative notation.

</details>

**18.** A circuit's behaviour is governed by `x² + 2x + 5 = 0`, where a root with a negative real part means it settles down. Does this one?

<details class="dl-answer"><summary>answer</summary>

Roots are `−1 ± 2i`, so the real part is −1, which is negative. It settles.

The real part governs whether the oscillation grows or dies away; the imaginary part gives how fast it oscillates. A positive real part would mean it runs away — which in a physical system means something breaks.

</details>
