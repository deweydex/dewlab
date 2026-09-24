---
title: "Parabolas: completing the square — Practice"
practice_for: parabolas
year: "2026-2027"
version: 2026.08.23.1
---

# Parabolas: completing the square — Practice

Each answer is hidden until you open it. Try the algebra on paper first,
then open the answer to compare.

The cell below has `complete_the_square` and a `draw` helper, for
checking your work.

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

## Completing the square

**1.** Complete the square on each quadratic.

- (a) $x^2 + 8x + 3$
- (b) $x^2 - 2x + 6$
- (c) $x^2 + 5x$
- (d) $x^2 - 12x + 36$

<details class="dl-answer"><summary>answer</summary>

(a) $(x + 4)^2 - 13$

(b) $(x - 1)^2 + 5$

(c) $(x + 2.5)^2 - 6.25$

(d) $(x - 6)^2$

The last one has nothing left over, because it was already a perfect
square. 36 is exactly the square of half of 12.

</details>

**2.** Where is the vertex of each of the four quadratics above?

<details class="dl-answer"><summary>answer</summary>

(a) $(-4, -13)$

(b) $(1, 5)$

(c) $(-2.5, -6.25)$

(d) $(6, 0)$

The sign flip on the first coordinate catches almost everybody at least
once. $(x + 4)^2$ is smallest when $x = -4$.

</details>

**3.** Why is halving the middle number the right step?

<details class="dl-answer"><summary>answer</summary>

Because $(x + h)^2$ multiplies out to $x^2 + 2hx + h^2$. The middle term
is $2h$ times $x$. To match a middle number $b$, we need $2h = b$, so
$h = b/2$.

Multiply out the bracket once, and the rule has a clear reason.

</details>

**4.** Complete the square on $2x^2 + 12x + 5$. Here the number in front
of $x^2$ is not 1.

<details class="dl-answer"><summary>answer</summary>

1. Take the 2 out of the first two terms: $2(x^2 + 6x) + 5$.
2. Complete the square inside the bracket: $2\big((x + 3)^2 - 9\big) + 5$.
3. Multiply out: $2(x + 3)^2 - 18 + 5 = 2(x + 3)^2 - 13$.

The vertex is at $(-3, -13)$. The 2 stretches the curve, but it does
not change the $x$ value of the vertex.

</details>

## Vertex and roots

**5.** Find the vertex and the roots of $x^2 - 6x + 5$. Use the
completed form for both.

<details class="dl-answer"><summary>answer</summary>

The completed form is $(x - 3)^2 - 4$, so the vertex is at $(3, -4)$.

For the roots, set it to zero: $(x - 3)^2 = 4$, so $x - 3 = \pm 2$.
That gives $x = 5$ or $x = 1$.

</details>

**6.** Which of these have real roots? Decide from the completed form
alone.

- (a) $x^2 - 4x + 3$
- (b) $x^2 + 2x + 9$
- (c) $x^2 - 10x + 25$

<details class="dl-answer"><summary>answer</summary>

(a) $(x - 2)^2 - 1$. The vertex is below the axis, so there are two
roots.

(b) $(x + 1)^2 + 8$. The vertex is 8 above the axis and the curve opens
upwards, so there are no real roots. A square plus 8 is never zero.

(c) $(x - 5)^2$. The vertex sits exactly on the axis, so there is one
root, at 5.

</details>

**7.** A parabola has its vertex at $(2, -9)$. It opens upwards, with
$a = 1$. Write it in both forms.

<details class="dl-answer"><summary>answer</summary>

The completed form is $(x - 2)^2 - 9$. Multiplied out, it is
$x^2 - 4x - 5$.

Its roots are 5 and $-1$. From the completed form, this takes one step:
$(x - 2)^2 = 9$, so $x - 2 = \pm 3$.

</details>

**8.** Two parabolas both have $a = 1$. One has its vertex at $(0, 3)$,
and the other at $(0, -3)$. How many roots does each one have?

<details class="dl-answer"><summary>answer</summary>

The first has no real roots, because its lowest point is 3 above the
axis. The second has two roots, at $\pm\sqrt{3}$.

This is the discriminant's story told as a picture. It depends on
whether the vertex is above the axis, on it, or below it.

</details>

## Where the formula comes from

**9.** Complete the square on $x^2 + bx + c$ with letters instead of
numbers. Then set it to zero. What do you get?

<details class="dl-answer"><summary>answer</summary>

Completing the square:

$$x^2 + bx + c = \left(x + \frac{b}{2}\right)^2 - \frac{b^2}{4} + c$$

Setting that to zero and undoing it one step at a time:

$$
\begin{aligned}
\left(x + \frac{b}{2}\right)^2 &= \frac{b^2}{4} - c = \frac{b^2 - 4c}{4} \\
x + \frac{b}{2} &= \pm \frac{\sqrt{b^2 - 4c}}{2} \\
x &= \frac{-b \pm \sqrt{b^2 - 4c}}{2}
\end{aligned}
$$

This is the quadratic formula with $a = 1$. **The quadratic formula is
completing the square, done once with letters.**

</details>

**10.** In the formula, where does the $\pm$ come from?

<details class="dl-answer"><summary>answer</summary>

It comes from taking the square root of both sides. Both $2$ and $-2$
square to 4, so $(x + 3)^2 = 4$ has two solutions, not one.

That is why a quadratic can have two roots. They are the two square
roots, $+$ and $-$, carried through.

</details>

## Reading the picture

**11.** Plot $x^2 - 6x + 5$, and mark its vertex and its roots. Is the
vertex exactly halfway between the roots?

<details class="dl-answer"><summary>answer</summary>

The vertex is at $(3, -4)$ and the roots are 1 and 5. 3 is halfway
between 1 and 5.

This is always true, because a parabola is symmetric about a vertical
line through its vertex. It is also a fast way to find the vertex when
you already know the roots.

</details>

**12.** A ball is thrown upwards. Its height in metres after $t$ seconds
is $h(t) = -5t^2 + 20t$. When is it highest, and how high does it go?

<details class="dl-answer"><summary>answer</summary>

The roots are $t = 0$ and $t = 4$, so the peak is halfway, at $t = 2$.
The height there is $h(2) = -20 + 40 = 20$ metres.

</details>

**13.** A farmer builds a rectangular pen against a wall. The wall is
one side, and 40 m of fencing makes the other three sides.

1. Write the area as a quadratic in the width.
2. Find the width and length that give the largest area.

<details class="dl-answer"><summary>answer</summary>

1. Let the width be $w$. The width is each of the two sides at right
   angles to the wall. The side along the wall is then $40 - 2w$. So the
   area is $A = w(40 - 2w) = -2w^2 + 40w$.
2. The roots are $w = 0$ and $w = 20$, so the peak is at $w = 10$. The
   area there is $10 \times 20 = 200$ m². The pen is 10 m deep and 20 m
   along the wall.

This is the usual shape of an optimisation problem: find the largest or
smallest value. Here the parabola does all the work.

</details>

**14.** Why can we find the largest value of a quadratic without any
calculus?

<details class="dl-answer"><summary>answer</summary>

A parabola has exactly one turning point, and we can find it exactly.
We can complete the square, or we can take the point halfway between
the roots.

Most curves are harder than this. That is what
[Derivatives: the rate of change of a curve](tutorial:rates-of-change)
is for, later in the course. The quadratic is a case where we do not
need a general method.

</details>
