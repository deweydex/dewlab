---
title: "Mixed problems: limits and derivatives"
practice_across:
  - approaching-a-limit
  - rates-of-change
  - derivative-rules
  - the-slope-of-a-wave
year: "2026-2027"
version: 2026.09.26.1
---

# Mixed problems: limits and derivatives

Each problem here needs at least one of the calculus tutorials, and
many need two. Nobody tells you which tool to use: choosing it is part
of the problem. When a problem can be done both by hand and with
numbers, try it both ways. The second way is your check.

Each answer is hidden in a fold under its question. Some problems also
have a hint fold, to open first if you get stuck.

## Tools

```python exec
id: tools-1
import math

def slope_between(f, x, gap):
    """The slope of the straight line joining two nearby points on f."""
    return (f(x + gap) - f(x)) / gap


def derivative_at(f, x, gap=1e-6):
    """The derivative, computed numerically."""
    return (f(x + gap) - f(x - gap)) / (2 * gap)


print(derivative_at(lambda x: x ** 3, 2))
```

## Limits and slopes

**1.** What is the limit of $\dfrac{x^3 - 8}{x - 2}$ as $x$ approaches 2?
Try it with numbers from both sides.

<details class="dl-answer"><summary>answer</summary>

12. At 2.001 it is about 12.006, and at 1.999 about 11.994. The top
factorises as $(x - 2)(x^2 + 2x + 4)$, so away from 2 the function is
$x^2 + 2x + 4$, which is 12 at 2.

</details>

**2.** What is the slope of $x^3$ at 2? Why is it the same number as
problem 1?

<details class="dl-answer"><summary>answer</summary>

By the power rule, $3x^2 = 12$ at 2. It is the same number because
$\dfrac{x^3 - 8}{x - 2}$ is the slope of the chord on $x^3$ from 2 to
$x$. Its limit, as $x$ approaches 2, is the slope at 2.

</details>

**3.** The cell divides the sine of a tiny angle by the angle, in
radians.

```python exec
id: limits-and-slopes-1
print(math.sin(1e-8) / 1e-8)
```

```predict
type: number
tolerance: 0.001

What will it print?
```

<details class="dl-answer"><summary>why</summary>

It prints 1.0. For a tiny angle, the up value on the unit circle is
almost the same as the distance walked round it. This limit, 1, is the
slope of sine at 0, which is $\cos 0 = 1$.

</details>

**4.** `derivative_at(abs, 0)` prints 0.0. Does $|x|$ have a slope of 0
at 0?

<details class="dl-answer"><summary>answer</summary>

No. `abs` has no slope at 0 at all. Chords from the right have a slope
of 1, and chords from the left a slope of $-1$. The two sides do not
agree, so there is no limit. `derivative_at` averages the two sides,
which hides the corner.

</details>

## Derivatives

**5.** A ball is thrown straight up. Its height is $20t - 4.9t^2$ metres
after $t$ seconds. When is it highest, and how high? How fast is it
going when it returns to 0?

<details class="dl-answer"><summary>one way through it</summary>

The slope is $20 - 9.8t$, which is 0 at $t = \frac{20}{9.8} \approx
2.04$ seconds. The height there is about 20.4 m. It is back at 0 when
$t(20 - 4.9t) = 0$, so at $t = \frac{20}{4.9} \approx 4.08$, and its
slope there is $20 - 9.8 \times 4.08 = -20$: it comes down at 20 m/s,
as fast as it went up.

</details>

**6.** Find the equation of the tangent line to $y = x^3 - 3x$ at
$x = 2$.

<details class="dl-hint"><summary>hint</summary>

A line needs a slope and one point. Which point on the curve does the
tangent touch?

</details>

<details class="dl-answer"><summary>one way through it</summary>

The slope is $3x^2 - 3 = 9$ at 2. The point is $(2, 8 - 6) = (2, 2)$.
So $2 = 9 \times 2 + c$, $c = -16$, and the tangent is $y = 9x - 16$.

</details>

**7.** What is the slope of $(x^2 + 1)(x - 3)$ at $x = 1$? Find it with
a rule, and check it with numbers.

<details class="dl-answer"><summary>answer</summary>

By the product rule, $2x(x - 3) + (x^2 + 1) \cdot 1$, which is
$-4 + 2 = -2$ at 1. `derivative_at(lambda x: (x ** 2 + 1) * (x - 3), 1)`
agrees.

</details>

**8.** What is the slope of $\sin(x^2)$ at $x = 1$?

<details class="dl-answer"><summary>answer</summary>

By the chain rule, the inside $x^2$ has slope $2x$ and the outside
$\sin$ has slope $\cos$. So the slope is $2x\cos(x^2)$, which is
$2\cos 1 \approx 1.081$ at 1.

</details>

**9.** A rectangle has a perimeter of 20 cm. Which width gives the
biggest area?

<details class="dl-answer"><summary>one way through it</summary>

With a width of $x$, the length is $10 - x$, and the area is
$x(10 - x) = 10x - x^2$. Its slope, $10 - 2x$, is 0 at $x = 5$. The
biggest area is a 5 cm by 5 cm square, 25 cm².

</details>

**10.** Which polynomial has the slope $3x^2 + 2$, and is 5 at $x = 0$?

<details class="dl-answer"><summary>answer</summary>

Running the power rule backwards gives $x^3 + 2x$, plus a number. The
number is the value at 0, so it is 5: $x^3 + 2x + 5$.

</details>

## Waves

**11.** Dublin's daylight fitted a wave with an amplitude of 4.55
hours, a period of 365 days and a shift of day 79.75. On which two days
of the year do its days grow by 3 minutes a day?

<details class="dl-hint"><summary>hint</summary>

The slope, in minutes a day, is
$4.55 \times \frac{2\pi}{365} \times 60 \times \cos\left(\frac{2\pi(x - 79.75)}{365}\right)$.
Set it to 3, and find the angle with `math.acos`. A cosine has the same
value for an angle and for minus that angle.

</details>

<details class="dl-answer"><summary>one way through it</summary>

The fastest rate is about 4.70 minutes a day, so
$\cos(\ldots) = \frac{3}{4.70} \approx 0.638$, and the angle is about
0.878 radians either side of 0. That is about 51 days either side of
the shift. So the days grow by 3 minutes a day on about day 29, at the
end of January, and on about day 131, in the middle of May. Both are
growing: one on the way up to the fastest, one on the way down.

</details>

**12.** Why does a wave change fastest where it crosses its midline,
and not at its top?

<details class="dl-answer"><summary>answer</summary>

At the top, the wave stops going up and starts going down, so it is
flat for a moment: its slope is 0. Its slope is the cosine wave, moved
along, and that is biggest a quarter of a period away from the top,
where the wave crosses its midline.

</details>

## Longer ones

**13.** The limits page found that `slope_between` gives its best
answer with a gap of about $10^{-8}$. `derivative_at` uses a point on
each side, and a gap of $10^{-6}$. Can you draw the error against the
gap for both, for $x^3$ at 2, on one picture? Which one gets closer to
12, and at which gap?

```python exec
id: longer-ones-1
import matplotlib.pyplot as plt

cube = lambda x: x ** 3
gaps = [10 ** -k for k in range(1, 15)]
# Your code here.
```

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Yours may be different and work too.

```python
one_side = [abs(slope_between(cube, 2, g) - 12) for g in gaps]
both_sides = [abs(derivative_at(cube, 2, g) - 12) for g in gaps]
fig, ax = plt.subplots()
ax.plot(gaps, one_side, "o-", label="one side")
ax.plot(gaps, both_sides, "o-", label="both sides")
ax.set_xscale("log")
ax.set_yscale("log")
ax.invert_xaxis()
ax.legend()
```

Both make a V. The error with a point on each side falls much faster as
the gap shrinks, so its V is deeper, and its bottom is at a bigger gap,
about $10^{-5}$. There its error is below $10^{-9}$, far smaller than
the one-sided best. $10^{-6}$ is close to that bottom.

</details>

**14.** A big wheel's rider is at height $22 - 20\cos\left(\frac{2\pi
t}{4}\right)$ metres after $t$ minutes. For what fraction of each turn
is the rider rising faster than 20 m a minute?

<details class="dl-answer"><summary>one way through it</summary>

The rate is $20 \times \frac{2\pi}{4} \sin\left(\frac{2\pi t}{4}\right)
\approx 31.4\sin\left(\frac{2\pi t}{4}\right)$. It is above 20 when the
sine is above $\frac{20}{31.4} \approx 0.637$. The sine is above 0.637
for the angles between about 0.69 and 2.45 radians, which is
$\frac{2.45 - 0.69}{2\pi} \approx 0.28$ of a turn.

</details>
