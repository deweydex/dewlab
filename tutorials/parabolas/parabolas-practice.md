---
title: "Parabolas: completing the square — Practice"
practice_for: parabolas
year: "2026-2027"
version: 2026.09.26.1
worlds:
  rockets: Rockets, launches and the arcs they fly. The numbers are made up.
  electronics: Batteries, resistors and the power between them. The numbers are made up.
  fantasy-maps: A made-up kingdom, its river and its bridges. The numbers are made up.
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

def complete_the_square(a, b, c):
    """Rewrite ax^2 + bx + c as a(x - h)^2 + k, and return a, h and k."""
    h = -b / (2 * a)
    return a, h, c - a * h ** 2


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


print(complete_the_square(1, 6, 5))
```

## Completing the square

**1.** Complete the square on each quadratic. Write each in the form
$a(x - h)^2 + k$.

- (a) $x^2 + 10x + 7$
- (b) $x^2 - 3x + 1$
- (c) $2x^2 - 8x + 3$
- (d) $-x^2 + 6x$

<details class="dl-answer"><summary>answer</summary>

(a) $(x + 5)^2 - 18$

(b) $(x - 1.5)^2 - 1.25$

(c) $2(x - 2)^2 - 5$

(d) $-(x - 3)^2 + 9$

In each, $h = -\frac{b}{2a}$ and $k = c - ah^2$. In (d), $a = -1$, so
$h = -\frac{6}{-2} = 3$ and $k = 0 - (-1)(9) = 9$.

</details>

**2.** Where is the vertex of each of the four quadratics above? Is it
the lowest point or the highest?

<details class="dl-answer"><summary>answer</summary>

(a) $(-5, -18)$, the lowest point.

(b) $(1.5, -1.25)$, the lowest point.

(c) $(2, -5)$, the lowest point.

(d) $(3, 9)$, the highest point, because $a$ is negative and the
parabola opens downwards.

</details>

**3.** Why is halving the middle number the right step?

<details class="dl-answer"><summary>answer</summary>

Because $a(x - h)^2$ multiplies out to $ax^2 - 2ahx + ah^2$. The middle
term is $-2ah$ times $x$. To match a middle number $b$, we need
$-2ah = b$, so $h = -\frac{b}{2a}$.

Multiply out the bracket once, and the rule has a clear reason.

</details>

**4.** Complete the square on $3x^2 + 6x - 1$ by taking the 3 out of
the first two terms, instead of using the formula for $h$ and $k$.

<details class="dl-answer"><summary>answer</summary>

1. Take the 3 out of the first two terms: $3(x^2 + 2x) - 1$.
2. Complete the square inside the bracket: $3\big((x + 1)^2 - 1\big) - 1$.
3. Multiply out: $3(x + 1)^2 - 3 - 1 = 3(x + 1)^2 - 4$.

The vertex is at $(-1, -4)$, the same as the formulas give. The 3
stretches the curve, but it does not change where the vertex is along
the $x$ axis.

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

The picture shows what the discriminant tells us. It depends on
whether the vertex is above the axis, on it, or below it.

</details>

**9.** Before you plot it: where is the vertex of $-2(x - 1)^2 + 3$,
and is it the lowest point or the highest?

```python exec
id: vertex-of-a-downward-parabola
ax = draw(lambda x: -2 * (x - 1) ** 2 + 3, low=-2, high=4, label="-2(x - 1)^2 + 3")
ax.plot([1], [3], "o")
```

```predict
type: choice

Where is the vertex?

- $(-1, 3)$, the highest point
  - The bracket has a minus sign, so the curve should move left.
- $(1, 3)$, the highest point
- $(1, 3)$, the lowest point
  - Every parabola so far has had its vertex at the bottom.
- $(1, -3)$, the highest point
  - The $-2$ in front could turn the 3 upside down as well.
```

<details class="dl-answer"><summary>answer</summary>

The vertex is $(1, 3)$, and it is the highest point.

In $a(x - h)^2 + k$, this has $a = -2$, $h = 1$ and $k = 3$. The
bracket is zero at $x = 1$. The $-2$ in front turns the curve upside
down, so the square is subtracted from 3, and 3 is the largest value.

</details>

## Where the formula comes from

**10.** Complete the square on $x^2 + bx + c$ with letters instead of
numbers. Then set it to zero. What do you get? (With $a = 1$ the
letters are easier. The general case goes the same way.)

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

**11.** In the formula, where does the $\pm$ come from?

<details class="dl-answer"><summary>answer</summary>

It comes from taking the square root of both sides. Both $2$ and $-2$
square to 4, so $(x + 3)^2 = 4$ has two solutions, not one.

So a quadratic can have two roots. They are the two square
roots, $+$ and $-$, carried through.

</details>

## Reading the picture

**12.** Plot $x^2 - 6x + 5$, and mark its vertex and its roots. Is the
vertex exactly halfway between the roots?

<details class="dl-answer"><summary>answer</summary>

The vertex is at $(3, -4)$ and the roots are 1 and 5. 3 is halfway
between 1 and 5.

This is always true, because a parabola is symmetric about a vertical
line through its vertex. It is also a fast way to find the vertex when
you already know the roots.

</details>

**13.** A ball is thrown upwards. Its height in metres after $t$ seconds
is $h(t) = -5t^2 + 20t$. When is it highest, and how high does it go?

<details class="dl-answer"><summary>answer</summary>

The roots are $t = 0$ and $t = 4$, so the peak is halfway, at $t = 2$.
The height there is $h(2) = -20 + 40 = 20$ metres.

</details>

**14.** A farmer builds a rectangular pen against a wall. The wall is
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

**15.** Why can we find the largest value of a quadratic without any
calculus?

<details class="dl-answer"><summary>answer</summary>

A parabola has exactly one turning point, and we can find it exactly.
We can complete the square, or we can take the point halfway between
the roots.

Most curves are harder than this.
[Derivatives: the rate of change of a curve](tutorial:rates-of-change),
later in the course, gives a method for those. The quadratic is a case where we do not
need a general method.

</details>

## Your world

**16.** A problem from the world you chose.

<div class="dl-world" data-world="rockets">

A rocket is launched from the ground at 20 m/s. Its height after $t$
seconds is $-4.9t^2 + 20t$ metres. How high does it go, and when? Use
the vertex form.

<details class="dl-answer"><summary>answer</summary>

It reaches about 20.4 m, after about 2.04 s.

`complete_the_square(-4.9, 20, 0)` gives $h \approx 2.04$ and
$k \approx 20.41$. The rocket starts and lands at height 0, and the
vertex is halfway between those two times: $t = 0$ and
$t = \frac{20}{4.9} \approx 4.08$.

</details>

</div>

<div class="dl-world" data-world="electronics">

A 9 V battery has 1.5 ohms inside it. At a current of $I$ amps it
delivers $9I - 1.5I^2$ watts. What is the most power it can deliver,
and what resistance draws it?

<details class="dl-answer"><summary>answer</summary>

13.5 W, at 3 A, into a 1.5 ohm resistor.

`complete_the_square(-1.5, 9, 0)` gives $h = 3$ and $k = 13.5$. At 3 A
the resistor gets $9 - 1.5 \times 3 = 4.5$ V, so it is
$\frac{4.5}{3} = 1.5$ ohms. It matches the battery's inside
resistance, as the 12 V supply's best resistor did.

</details>

</div>

<div class="dl-world" data-world="fantasy-maps">

An arched bridge crosses the river. The underside of the arch is
$y = -0.05(x - 10)^2 + 5$ metres above the water, $x$ metres from one
bank. How wide is the arch at water level, and how high is it? Can a
boat 6 m wide and 4 m tall pass under the middle?

```python exec
id: your-world--fantasy-maps
def arch(x):
    return -0.05 * (x - 10) ** 2 + 5
```

<details class="dl-answer"><summary>answer</summary>

The arch is 20 m wide and 5 m high, and the boat fits.

The vertex form shows the top at $(10, 5)$. At water level,
$(x - 10)^2 = 100$, so $x = 0$ or 20. A boat 6 m wide in the middle
reaches from $x = 7$ to $x = 13$, and `arch(7)` and `arch(13)` are both
4.55 m, higher than the boat's 4 m.

</details>

</div>

## From earlier

**17.** In [Functions and their graphs](tutorial:drawing-functions),
the vertices of $x^2 + bx$ seemed to lie on the curve $y = -x^2$. Can
you show that they do, with $h$ and $k$?

<details class="dl-answer"><summary>answer</summary>

For $x^2 + bx$, $a = 1$ and $c = 0$. So $h = -\frac{b}{2}$ and
$k = 0 - h^2 = -h^2$.

Every vertex $(h, k)$ has $k = -h^2$, so it lies on $y = -x^2$, whatever
$b$ is. Changing $b$ moves the vertex along that curve.

</details>

**18.** In [Solving equations: linear, quadratic and
simultaneous](tutorial:cracking-equations), the discriminant
$b^2 - 4ac$ told us how many roots a quadratic has. Show that
$k = -\frac{b^2 - 4ac}{4a}$. Why does that explain the three cases?

<details class="dl-answer"><summary>answer</summary>

$k = c - ah^2 = c - a \cdot \frac{b^2}{4a^2} = c - \frac{b^2}{4a} =
\frac{4ac - b^2}{4a} = -\frac{b^2 - 4ac}{4a}$.

Take $a$ positive, so the parabola opens upwards. A positive
discriminant makes $k$ negative: the vertex is below the axis, and the
curve crosses twice. A zero discriminant makes $k = 0$: the vertex sits
on the axis. A negative discriminant makes $k$ positive: the vertex is
above the axis, and the curve never reaches it. For
$x^2 - 6x + 5$, the discriminant is 16 and $k = -4$.

</details>
