---
title: "Parabolas — Practice"
slug: parabolas-practice
practice_for: parabolas
module: mit-pdp-maths-prog-integration
module_title: "Programming and Maths, Integrated"
year: "2026-2027"
series: algebra-and-functions
version: 2026.08.23.1
---

# Parabolas — Practice

Answers are folded. Do the algebra before you unfold it.

## Tools

```python exec
id: tools-1
import math
import matplotlib.pyplot as plt

def complete_the_square(b, c):
    """Rewrite x^2 + bx + c as (x + h)^2 + k."""
    h = b / 2
    return h, c - h ** 2


def draw(f, low=-8, high=8, label=None, ax=None):
    xs = [low + (high - low) * i / 300 for i in range(301)]
    if ax is None:
        fig, ax = plt.subplots(figsize=(7, 4.5))
        ax.axhline(0, color="black", linewidth=0.8)
        ax.axvline(0, color="black", linewidth=0.8)
        ax.grid(alpha=0.3)
    ax.plot(xs, [f(x) for x in xs], label=label)
    if label:
        ax.legend(fontsize=8)
    return ax


print(complete_the_square(6, 5))
```

## Completing the Square

**1.** Complete the square on each.

- (a) `x² + 8x + 3`
- (b) `x² − 2x + 6`
- (c) `x² + 5x`
- (d) `x² − 12x + 36`

<details class="dl-answer"><summary>answer</summary>

(a) `(x + 4)² − 13`. (b) `(x − 1)² + 5`. (c) `(x + 2.5)² − 6.25`. (d) `(x − 6)²`.

The last one has nothing left over, because it was already a perfect square — 36 is exactly the square of half of 12.

</details>

**2.** Where is the vertex of each of the four above?

<details class="dl-answer"><summary>answer</summary>

(a) `(−4, −13)`. (b) `(1, 5)`. (c) `(−2.5, −6.25)`. (d) `(6, 0)`.

The sign flip on the first coordinate catches everybody at least once: `(x + 4)²` is smallest when `x = −4`.

</details>

**3.** Why is halving the middle coefficient the right move?

<details class="dl-answer"><summary>answer</summary>

Because `(x + h)²` expands to `x² + 2hx + h²`. The middle term of the expansion is `2h`, so to match a middle term of `b` you need `h = b/2`.

Expand the bracket once and the rule stops being arbitrary.

</details>

**4.** Complete the square on `2x² + 12x + 5`. (The leading coefficient is not 1.)

<details class="dl-answer"><summary>answer</summary>

Take the 2 out of the first two terms first: `2(x² + 6x) + 5`. Complete the square inside: `2((x + 3)² − 9) + 5`. Multiply out: `2(x + 3)² − 18 + 5 = 2(x + 3)² − 13`.

Vertex at `(−3, −13)`. The 2 stretches the curve but does not move where the bottom is horizontally.

</details>

## Vertex and Roots

**5.** Find the vertex and the roots of `x² − 6x + 5`, using the completed form for both.

<details class="dl-answer"><summary>answer</summary>

`(x − 3)² − 4`, so the vertex is at `(3, −4)`.

Setting it to zero: `(x − 3)² = 4`, so `x − 3 = ±2`, so `x = 5` or `x = 1`.

</details>

**6.** Which of these have real roots? Decide from the completed form alone.

- (a) `x² − 4x + 3`
- (b) `x² + 2x + 9`
- (c) `x² − 10x + 25`

<details class="dl-answer"><summary>answer</summary>

(a) `(x − 2)² − 1` — the vertex is below the axis, so two roots.

(b) `(x + 1)² + 8` — the vertex is 8 above the axis and the curve opens upwards, so none. A squared thing plus 8 is never zero.

(c) `(x − 5)²` — the vertex sits exactly on the axis, so one root, at 5.

</details>

**7.** The vertex of a parabola is at `(2, −9)` and it opens upwards with `a = 1`. Write it in both forms.

<details class="dl-answer"><summary>answer</summary>

`(x − 2)² − 9`, which expands to `x² − 4x − 5`.

Its roots are at 5 and −1, which you can read off the first form in one step.

</details>

**8.** Two parabolas have vertices at `(0, 3)` and `(0, −3)`, both with `a = 1`. How many roots does each have?

<details class="dl-answer"><summary>answer</summary>

The first has none — its lowest point is 3 above the axis. The second has two, at ±√3.

Which is the whole story of the discriminant, told as a picture: whether the vertex is above, on, or below the axis.

</details>

## Where the Formula Comes From

**9.** Complete the square on `x² + bx + c` using letters rather than numbers, and see what falls out when you set it to zero.

<details class="dl-answer"><summary>answer</summary>

`x² + bx + c = (x + b/2)² − b²/4 + c`.

Setting that to zero: `(x + b/2)² = b²/4 − c`, so `x + b/2 = ±√(b²/4 − c)`, so `x = −b/2 ± √(b²/4 − c)`.

Multiply through by 2 inside the root and it is the familiar formula with `a = 1`. **The quadratic formula is this, done once in general.**

</details>

**10.** In the formula, where does the `±` come from?

<details class="dl-answer"><summary>answer</summary>

From taking the square root of both sides. Both `2` and `−2` square to 4, so `(x + 3)² = 4` has two solutions and not one.

That is why a quadratic has two roots — the two branches of the square root, carried through.

</details>

## Reading the Picture

**11.** Plot `x² − 6x + 5` and mark its vertex and its roots. Confirm that the vertex sits exactly halfway between the roots.

<details class="dl-answer"><summary>answer</summary>

Vertex at `(3, −4)`, roots at 1 and 5, and 3 is halfway between them.

That is always true, because a parabola is symmetric about a vertical line through its vertex. It is also a fast way to find a vertex when you already know the roots.

</details>

**12.** A ball is thrown and its height is `h(t) = −5t² + 20t`. When is it highest, and how high?

<details class="dl-answer"><summary>answer</summary>

The roots are at t = 0 and t = 4, so the peak is halfway, at t = 2. Then `h(2) = −20 + 40 = 20` metres.

</details>

**13.** A rectangular pen is to be made against a wall with 40 m of fencing on three sides. Write the area as a quadratic in the width, and find the dimensions that give the most area.

<details class="dl-answer"><summary>answer</summary>

If the width (the two sides at right angles to the wall) is `w`, the remaining side is `40 − 2w`, so the area is `A = w(40 − 2w) = −2w² + 40w`.

Roots at w = 0 and w = 20, so the peak is at w = 10, giving an area of 200 m². The pen is 10 m deep and 20 m along the wall.

This is the standard shape of an optimisation problem, and the parabola does all the work.

</details>

**14.** Why can you find the maximum of a quadratic without any calculus?

<details class="dl-answer"><summary>answer</summary>

Because a parabola has exactly one turning point and you can find it exactly — either by completing the square, or by taking the midpoint of the roots.

Most curves are not that obliging, which is what *Rates of Change* is for. The quadratic is the case where a general method is not needed.

</details>
