---
title: "Counting Darts — Practice"
slug: counting-darts-practice
practice_for: counting-darts
module: computational-methods
module_title: "Computational Methods"
year: "2026-2027"
series: simulation
version: 2026.08.30.1
---

# Counting Darts — Practice

Every problem here is the same three steps in a different costume: throw
points at a region you can measure, decide which ones land in the part you
cannot, and multiply the fraction by the area you started with.

The seeds in the answers are there so your numbers match. Where a problem
does not set one, expect your last two digits to differ from the ones printed
— and treat an answer that differs in the *first* digit as a sign something
is wrong with the code rather than with your luck.

```python exec
id: setup-1
import random
import math

def inside_circle(x, y):
    return x * x + y * y <= 1
```

## The Same Idea, Rearranged

**1.** The tutorial multiplied by 4 because the quarter-circle sits inside a
square of area 1. What would you multiply by if you threw darts at the square
from $(-1, -1)$ to $(1, 1)$ and counted those inside the *whole* unit circle?

<details class="dl-answer"><summary>answer</summary>

By 4 again — but for a different reason, and the difference is worth having
straight.

That square has area $2 \times 2 = 4$. The whole circle has area $\pi$. So
the fraction inside is $\pi/4$, and the estimate is $4 \times$ the fraction.
The arithmetic matches the tutorial by coincidence, not because it is the
same setup.

The general rule underneath both: **estimated area = (fraction that landed
inside) × (area of the region you threw at)**. Get into the habit of writing
down that outer area explicitly; it is where nearly every mistake in this
kind of code lives.

</details>

**2.** Estimate the area under the curve $y = x^2$ between 0 and 1, by
throwing darts at the unit square and counting those that fall below the
curve. The exact answer is $1/3$ — how close do you get with 20,000 darts?

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

Off by about 0.0035 with 20,000 darts, which is the accuracy the square-root
rule predicts and no better.

This one has a name — *Monte Carlo integration* — and it is the reason the
method matters. Nobody needs it for $x^2$, where calculus gives $1/3$ exactly
in one line. But swap in a function with no closed-form integral and the
calculus stops working while this code carries on unchanged.

</details>

**3.** Estimate the area of the quarter-ellipse where
$x^2 + (y/0.5)^2 \le 1$, inside the unit square. The exact answer is
$\pi ab / 4$ with $a = 1$ and $b = 0.5$.

```python exec
id: the-same-idea-rearranged-2
hint: Only the test changes: x*x + (y / 0.5) ** 2 <= 1. Work out the exact value from the formula first so you have something to compare against.
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

Close to three decimal places, this time — better than the last problem got,
from the same number of darts. That is not because ellipses are easier. It is
the same unreliable accuracy the tutorial's table showed, landing well on
this particular run.

</details>

## How Much Work Is Enough

**4.** The tutorial said a hundred thousand darts gets roughly two correct
decimal places, and that each extra decimal place costs about a hundred times
the darts. How many would four decimal places take? Is that a number you can
run in this browser tab?

<details class="dl-answer"><summary>answer</summary>

Two extra decimal places is $100 \times 100 = 10{,}000$ times the darts:
$100{,}000 \times 10{,}000 = 10^9$. A billion.

At the rate this loop runs in a browser — very roughly a million darts a
second, and you can time it to check — that is around fifteen to twenty
minutes of the tab doing nothing else, to compute a number already known to
fifty trillion digits by better methods.

Which is the honest conclusion, and worth stating plainly: for π, this method
is a toy. It earns its keep on questions where the alternative is not a
better algorithm but no algorithm at all.

</details>

**5.** Time it, rather than guessing. How long does 100,000 darts actually
take here, and what does that predict for a billion?

```python exec
id: how-much-work-is-enough-1
hint: time.perf_counter() before and after, and subtract. The prediction is just a multiplication — the loop's cost per dart does not change with n.
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

The exact figure depends on the machine and how busy the browser is, so
yours will differ from anyone else's — the useful part is the ratio, and that
the prediction is a straight multiplication because each dart costs the same
as every other one.

Worth noticing what this measurement is *not*: it says nothing about whether
the answer is any good. Time and accuracy are separate questions here, and
running longer buys you the second only in the unreliable, square-root way
the tutorial showed.

</details>

## A Shape With No Formula

**6.** Two unit circles, one centred at $(0, 0)$ and one at $(1, 0)$, overlap
in a lens-shaped region. Estimate its area.

```python exec
id: a-shape-with-no-formula-1
hint: A point is in the lens when it is inside both circles. Choose a rectangle big enough to contain the lens — x from -1 to 2 and y from -1 to 1 will do — throw darts uniformly across it with random.uniform, and remember to multiply by that rectangle's area rather than by 1.
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

About 1.226. The exact answer, for anyone who wants to chase it, is
$2\cos^{-1}(1/2) - \sin(2\cos^{-1}(1/2)) \approx 1.2284$ — a formula that
takes real work to derive and applies only to this one arrangement of two
equal circles.

That contrast is the whole argument for the method. The derivation gets
harder for unequal circles, much harder for three circles, and stops existing
for an arbitrary blob. The eight lines above do not care: change the
condition and they measure a different shape, with no new mathematics
required at all.

</details>

**7.** What goes wrong if you throw darts at a rectangle that does not fully
contain the shape you are measuring? And what goes wrong if the rectangle is
enormous compared to the shape?

<details class="dl-answer"><summary>answer</summary>

Too small, and the estimate is simply wrong — silently. Any part of the shape
outside the rectangle can never be hit, so it is not counted, and nothing in
the output announces this. The answer comes back looking perfectly
reasonable. This is the most dangerous mistake on the page precisely because
it does not fail loudly.

Too large, and the estimate is still correct but wasteful. If the shape fills
one thousandth of the rectangle, then 999 darts in every thousand tell you
nothing, and you need a thousand times as many to reach any given accuracy.

The rectangle should be the smallest one you are certain contains the shape.
"Certain" is doing the work in that sentence — when unsure, take the larger
one and pay in time rather than in a wrong answer nobody spots.

</details>

## Thinking It Through

**8.** Someone proposes a tidier method: instead of throwing darts randomly,
lay a regular grid of points over the square and count those inside the
curve. No randomness, no wobble, and the same answer. Is that better?

<details class="dl-answer"><summary>answer</summary>

In two dimensions, honestly, yes — it usually is. A grid gives a more
accurate area for the same number of points, and it is repeatable without
needing a seed. For this problem the grid wins.

The catch arrives with dimensions. A grid of 100 points per side is $100^2 =
10{,}000$ points in 2D, which is fine; $100^{10}$ in ten dimensions, which is
$10^{20}$ and impossible. Random sampling has no such term — the error still
falls as $1/\sqrt{n}$ whether the problem has two dimensions or two hundred,
because a random point does not know or care how many coordinates it has.

That is why Monte Carlo methods dominate in physics, finance and machine
learning, where problems routinely have hundreds of dimensions, and why they
look like an odd choice in the two-dimensional example everyone learns them
from. The example is chosen to be drawable, not to be the case where the
method wins.

</details>

**9.** You run the dart estimate and get 3.19. A colleague runs the identical
code and gets 3.11. Who has made a mistake?

<details class="dl-answer"><summary>answer</summary>

Neither, most likely. Two runs of a correct simulation with different seeds
are *supposed* to disagree, and with a few hundred darts a spread of that
size is entirely ordinary.

The question worth asking instead is how much disagreement would be too much
— at which point you would suspect a bug rather than luck. Answering that
needs a way to say how far apart two honest runs should typically fall, which
is a quantity rather than a feeling, and it is exactly what the next tutorial
sets out to measure.

Until then, the practical habit: two people comparing simulation results
should compare seeds first. Identical seeds and different answers is a real
bug. Different seeds and different answers is Tuesday.

</details>
