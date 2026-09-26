---
title: "Monte Carlo simulation: estimating π with random darts — Practice"
practice_for: counting-darts
year: "2026-2027"
version: 2026.09.22.1
---

# Monte Carlo simulation: estimating π with random darts — Practice

The answers are hidden in folds under each problem. Try each problem
yourself before you open its fold.

Every problem here uses the same three steps, with different details:

1. Throw points at a region whose area you know.
2. Decide which points land in the part whose area you want.
3. Multiply the fraction that landed there by the area you threw at.

The answers set seeds so that your numbers can match. If you do not use
the same seed, expect your last two digits to be different from the ones
printed. If your answer is different in the *first* digit, the problem is
probably in the code, not in your luck.

```python exec
id: setup-1
import random
import math

def inside_circle(x, y):
    return x * x + y * y <= 1
```

## The same idea, rearranged

**1.** The tutorial multiplied by 4, because the quarter-circle sits inside
a square of area 1. Now suppose you throw darts at the square from
$(-1, -1)$ to $(1, 1)$, and count the darts inside the *whole* unit
circle. What would you multiply by?

<details class="dl-answer"><summary>answer</summary>

You multiply by 4 again. That is not a coincidence.

The big square is made of four unit squares, one in each corner around
the origin. The circle is made of four quarter-circles, one in each of
those squares. Each small square holds the tutorial's picture, turned
round. So the fraction of darts inside is the same, $\pi/4$, and the 4
comes back.

The areas say the same thing. The big square has area $2 \times 2 = 4$,
and the whole circle has area $\pi$. So the fraction inside is $\pi/4$,
and the estimate is $4 \times$ the fraction.

Here is the general rule underneath both:

**estimated area = (fraction that landed inside) × (area of the region
you threw at)**

Write down that outer area every time. Most mistakes in this kind of
code happen there.

</details>

**2.** Estimate the area under the curve $y = x^2$, between 0 and 1.
Throw darts at the unit square, and count the darts that fall below the
curve. The exact answer is $1/3$. How close do you get with 20,000
darts?

```python exec
id: the-same-idea-rearranged-1
hint: A dart at (x, y) is below the curve when y <= x*x. Everything else is the tutorial's loop with that one comparison swapped in.
```

<details class="dl-answer"><summary>answer</summary>

```python
import random
random.seed(4)

n = 20000
hits = 0
for _ in range(n):
    x, y = random.random(), random.random()
    if y <= x * x:
        hits += 1

print(hits / n)        # 0.33685
print(1 / 3)           # 0.3333...
```

With 20,000 darts, this is off by about 0.0035. That is the accuracy
the square-root rule predicts, and no better.

Measuring an area this way is called *Monte Carlo integration*, and it is
the reason the method matters. Nobody needs it for $x^2$, because calculus gives
$1/3$ exactly, in one line. But some curves have no formula for the area
under them. For those, calculus cannot give an exact answer, and this
code still works without any change.

</details>

**3.** Estimate the area of the quarter-ellipse where
$x^2 + (y/0.5)^2 \le 1$, inside the unit square. The exact answer is
$\pi ab / 4$, with $a = 1$ and $b = 0.5$.

```python exec
id: the-same-idea-rearranged-2
hint: Only the test changes: x*x + (y / 0.5) ** 2 <= 1. Work out the exact value from the formula first, so you have something to compare against.
```

<details class="dl-answer"><summary>answer</summary>

```python
import random
random.seed(5)

n = 20000
hits = 0
for _ in range(n):
    x, y = random.random(), random.random()
    if x * x + (y / 0.5) ** 2 <= 1:
        hits += 1

print(hits / n)                  # 0.3917
print(math.pi * 1 * 0.5 / 4)     # 0.39270
```

This time the estimate is off by only about 0.001. That is better than
the last problem, with the same number of darts. Ellipses are not easier.
This is the same unreliable accuracy that the tutorial's table showed,
and on this run it happened to give a good result.

</details>

## How much work is enough

**4.** The tutorial said that a hundred thousand darts give roughly two
correct decimal places. Each extra decimal place costs about a hundred
times as many darts.

1. How many darts would four decimal places take?
2. Could you run that many in this browser tab?

<details class="dl-answer"><summary>answer</summary>

Two extra decimal places need $100 \times 100 = 10{,}000$ times the
darts: $100{,}000 \times 10{,}000 = 10^9$. That is a billion darts.

In a browser, this loop runs at very roughly a million darts a second.
You can time it to check. So a billion darts take around fifteen to twenty
minutes, with the tab doing nothing else. And the number it computes is
already known, by better methods, to more than a hundred trillion digits.

For π, this method is a toy. It is most
useful for questions that have no better method at all.

</details>

**5.** Now time it, instead of guessing.

1. How long do 100,000 darts take here?
2. What does that predict for a billion?

```python exec
id: how-much-work-is-enough-1
hint: Call time.perf_counter() before and after the loop, and subtract. The prediction is a multiplication, because each dart costs the same, whatever n is.
```

<details class="dl-answer"><summary>answer</summary>

```python
import time

start = time.perf_counter()
hits = 0
for _ in range(100000):
    x, y = random.random(), random.random()
    if inside_circle(x, y):
        hits += 1
elapsed = time.perf_counter() - start

print(f"{elapsed:.3f} s for 100,000")
print(f"predicts {elapsed * 10000 / 60:.0f} minutes for a billion")
```

The exact time depends on the machine, and on how busy the browser is. So
yours will be different from anyone else's. The useful part is the ratio.
The prediction is a plain multiplication, because each dart costs the same
as every other dart.

Notice what this measurement does *not* tell you. It says nothing about
whether the answer is any good. Time and accuracy are separate questions
here. Running for longer improves accuracy only in the slow, unreliable,
square-root way that the tutorial showed.

</details>

## A shape with no formula

**6.** Two unit circles, one centred at $(0, 0)$ and one at $(1, 0)$,
overlap. The overlap is shaped like a lens. Estimate its area.

```python exec
id: a-shape-with-no-formula-1
hint: A point is in the lens when it is inside both circles. Choose a rectangle big enough to hold the lens: x from -1 to 2 and y from -1 to 1 will do. Throw darts across it with random.uniform. Remember to multiply by that rectangle's area, not by 1.
```

<details class="dl-answer"><summary>answer</summary>

```python
import random
random.seed(6)

n = 50000
hits = 0
for _ in range(n):
    x = random.uniform(-1, 2)
    y = random.uniform(-1, 1)
    if x * x + y * y <= 1 and (x - 1) ** 2 + y * y <= 1:
        hits += 1

box_area = 3 * 2
print(hits / n * box_area)     # 1.2259
```

The estimate is about 1.226. If you want to check it, the exact answer is
$2\cos^{-1}(1/2) - \sin(2\cos^{-1}(1/2)) \approx 1.2284$. That formula
takes real work to find, and it only works for this one arrangement of
two equal circles.

That difference is the whole argument for the method. The formula gets
harder to find for two circles of different sizes. It gets much harder
for three circles. For a blob of any shape, there is no formula at all.
The eight lines of the loop stay the same. Change the condition, and they
measure a different shape, with no new mathematics.

</details>

**7.** Think about the rectangle you throw darts at.

- What goes wrong if the rectangle does not fully contain the shape you
  are measuring?
- What goes wrong if the rectangle is enormous compared to the shape?

<details class="dl-answer"><summary>answer</summary>

If the rectangle is too small, the estimate is wrong, and nothing tells
you. A dart can never hit the part of the shape outside the rectangle,
so that part is never counted. The answer looks perfectly reasonable.
This is the most dangerous mistake on the page, because there is no error
message to warn you.

If the rectangle is too large, the estimate is still correct, but it
wastes work. Say the shape fills one thousandth of the rectangle. Then
999 darts in every thousand tell you nothing, and you need about a
thousand times as many darts for the same accuracy.

Choose the smallest rectangle that you are *certain* contains the shape.
"Certain" is the important word. If you are unsure, take the larger
rectangle. A slower program is better than a wrong answer that nobody
notices.

</details>

## Thinking it through

**8.** Someone suggests a tidier method. Instead of throwing darts at
random, lay a regular grid of points over the square, and count the
points inside the curve. There is no randomness, no wobble, and the same
answer every time. Is that better?

<details class="dl-answer"><summary>answer</summary>

In two dimensions, yes, it usually is. A grid gives a more accurate area
for the same number of points. It is also repeatable without a seed. For
this problem, the grid wins.

The problem comes with more dimensions. A dimension here is one
coordinate of a point: a point on a flat square has two, $x$ and $y$.
A grid of 100 points per side needs $100^2 = 10{,}000$ points in two
dimensions. That is fine. In ten dimensions it needs $100^{10}$, which is
$10^{20}$ points, and that is impossible.

Random sampling does not have this problem. The error still falls as
$1/\sqrt{n}$, whether the problem has two dimensions or two hundred.

That is why Monte Carlo methods are the main tool in physics, finance
and machine learning, where problems often have hundreds of dimensions.
It is also why they look like an odd choice in the two-dimensional
example everyone learns first. That example was chosen because it is
easy to draw. It is not the case where the method is most useful.

</details>

**9.** You run the dart estimate and get 3.19. A colleague runs exactly the
same code and gets 3.11. Who has made a mistake?

<details class="dl-answer"><summary>answer</summary>

Probably neither of you. Two runs of a correct simulation with different
seeds are *supposed* to disagree. With a few hundred darts, a spread of
that size is completely ordinary.

How much disagreement would be too much? At
what point would you suspect a bug, and not luck? To answer that, you
need a number for how far apart two correct runs usually fall, and not
only a feeling. The $1/\sqrt{n}$ rule is the first step towards that
number.
Statistics gives the full answer, and it is beyond this page.

Until then, use this habit. When two people compare
simulation results, they should compare seeds first. The same seed with
different answers means a real bug. Different seeds with different
answers is normal.

</details>
