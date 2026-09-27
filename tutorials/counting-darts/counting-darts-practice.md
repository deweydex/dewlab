---
title: "Monte Carlo simulation: estimating π with random darts — Practice"
practice_for: counting-darts
year: "2026-2027"
version: 2026.09.27.1
worlds:
  living-systems: Turtle hatchlings racing to the sea.
  queues-and-crowds: The riders on a theme-park ride, and their birthdays.
  spread: A disease passed on at a meeting.
  space-and-physics: Meteors in the same minute of a shower.
---

# Monte Carlo simulation: estimating π with random darts — Practice

Each answer is hidden until you open it. Write something down first,
even a guess, and then open the answer to compare.

Every problem here uses the same three steps, with different details:

1. Throw points at a region whose area you know.
2. Decide which points land in the part whose area you want.
3. Multiply the fraction that landed there by the area you threw at.

Where a problem asks you to write a function, it takes a `seed` and sets
it first, so your numbers and the answer's can be compared row by row.

## Tools

```python exec
id: tools-1
import random
import math


def inside_circle(x, y):
    return x * x + y * y <= 1


def estimate_pi(n, seed=0):
    """Throw n darts at the unit square; return 4 x the fraction inside."""
    random.seed(seed)
    hits = 0
    for _ in range(n):
        x = random.random()
        y = random.random()
        if inside_circle(x, y):
            hits += 1
    return 4 * hits / n


print(estimate_pi(100))
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

**2.** Can you write `area_under_square(n, seed)`? It estimates the
area under the curve $y = x^2$, between 0 and 1, by throwing `n` darts
at the unit square and counting the ones below the curve. The exact
answer is $1/3$.

```python exec
id: the-same-idea-rearranged-1
def area_under_square(n, seed):
    """The share of n darts in the unit square that land below y = x^2."""
    # Your code here.
```

```hint
A dart at `(x, y)` is below the curve when `y <= x * x`. Take `x` first
and then `y`, each from `random.random()`, as the tutorial did.
```

```inputs
area_under_square(1000, 4)
area_under_square(20000, 4)
area_under_square(200000, 4)
```

```solution
def area_under_square(n, seed):
    """The share of n darts in the unit square that land below y = x^2."""
    random.seed(seed)
    hits = 0
    for _ in range(n):
        x, y = random.random(), random.random()
        if y <= x * x:
            hits += 1
    return hits / n
---
With 20,000 darts, 0.33685, off by about 0.0035: the accuracy the
square-root rule predicts, and no better. With 200,000, 0.334715.
Measuring an area this way is called *Monte Carlo integration*. Nobody
needs it for $x^2$, because calculus gives $1/3$ in one line. But some
curves have no formula for the area under them, and this code works on
them without any change.
```

**3.** Change one line of your function to estimate the area of the
quarter-ellipse where $x^2 + (y/0.5)^2 \le 1$, inside the unit square.
The exact answer is $\pi \times 1 \times 0.5 / 4 \approx 0.3927$.

```python exec
id: the-same-idea-rearranged-2
def quarter_ellipse(n, seed):
    """The share of n darts in the unit square inside the quarter-ellipse."""
    # Your code here.
```

```hint
Only the test changes: `x * x + (y / 0.5) ** 2 <= 1`.
```

```inputs
quarter_ellipse(20000, 5)
round(quarter_ellipse(20000, 5) - math.pi * 0.5 / 4, 4)
```

```solution
def quarter_ellipse(n, seed):
    """The share of n darts in the unit square inside the quarter-ellipse."""
    random.seed(seed)
    hits = 0
    for _ in range(n):
        x, y = random.random(), random.random()
        if x * x + (y / 0.5) ** 2 <= 1:
            hits += 1
    return hits / n
---
0.3917, off by only about 0.001: better than problem 2, with the same
number of darts. Ellipses are not easier. This is the unreliable
accuracy the tutorial's table showed, and on this run it happened to
come out well.
```

**4.** With 10 darts, the estimate is $4 \times \text{hits} / 10$, and
`hits` is a whole number from 0 to 10. This cell finds the estimate,
out of all of those, that is closest to π.

```python exec
id: the-same-idea-rearranged-3
closest = min((4 * hits / 10 for hits in range(11)), key=lambda e: abs(e - math.pi))
print(closest)
```

```predict
type: number

What will the cell print?
```

<details class="dl-answer"><summary>why</summary>

It prints 3.2, from 8 hits. Ten darts can only give 0, 0.4, 0.8 and so
on, up to 4. No seed, however lucky, can do better than 3.2. More darts
make the steps between possible answers smaller, and that is one reason
more darts can get closer.

</details>

## How much work is enough

**5.** The tutorial said that a hundred thousand darts give roughly two
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

**6.** Now time it, instead of guessing.

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

**7.** Two unit circles, one centred at $(0, 0)$ and one at $(1, 0)$,
overlap in a shape like a lens. Can you write `lens_area(n, seed)`? It
throws `n` darts at the rectangle from $x = -1$ to $2$ and $y = -1$ to
$1$, using `random.uniform`, and estimates the lens's area.

```python exec
id: a-shape-with-no-formula-1
def lens_area(n, seed):
    """The estimated area where the two circles overlap."""
    # Your code here.
```

```hint
A point is in the lens when it is inside both circles:
`x * x + y * y <= 1 and (x - 1) ** 2 + y * y <= 1`. Take `x` first, with
`random.uniform(-1, 2)`, then `y`. The rectangle's area is 3 × 2.
```

```inputs
lens_area(1000, 6)
lens_area(50000, 6)
```

```solution
def lens_area(n, seed):
    """The estimated area where the two circles overlap."""
    random.seed(seed)
    hits = 0
    for _ in range(n):
        x = random.uniform(-1, 2)
        y = random.uniform(-1, 1)
        if x * x + y * y <= 1 and (x - 1) ** 2 + y * y <= 1:
            hits += 1
    box_area = 3 * 2
    return hits / n * box_area
---
50,000 darts give about 1.226. The exact answer is
$2\cos^{-1}(1/2) - \sin(2\cos^{-1}(1/2)) \approx 1.2284$. That formula
takes real work to find, and it only works for two equal circles this
far apart. The loop works for any shape: change the condition, and it
measures a different one.
```

**8.** Think about the rectangle you throw darts at.

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

## Your world

**9.** Darts can measure a chance as well as an area: the share of
trials in which something happens.

<div class="dl-world" data-world="living-systems">

A turtle lays 100 eggs on a beach. Each hatchling has a chance of 0.02 of reaching the sea and growing up. What is the chance that at least one does? Can you write `chance_any(k, p, trials, seed)`? In each trial it checks `k` hatchlings, each with chance `p`, and it returns the share of trials in which at least one made it.

```python exec
id: your-world-1--living-systems
def chance_any(k, p, trials, seed):
    """The share of trials in which at least one of k chances, each p, comes true."""
    # Your code here.
```

```hint
In each trial, `any(random.random() < p for _ in range(k))` is `True` when at least one of the `k` checks comes true.
```

```inputs
chance_any(100, 0.02, 10000, 1)
chance_any(1, 0.02, 10000, 1)
chance_any(5, 0.2, 10000, 1)
```

```solution
def chance_any(k, p, trials, seed):
    """The share of trials in which at least one of k chances, each p, comes true."""
    random.seed(seed)
    yes = 0
    for _ in range(trials):
        if any(random.random() < p for _ in range(k)):
            yes += 1
    return yes / trials
---
0.8701: at least one hatchling of 100 makes it, in 87 trials in 100. The exact answer is $1 - 0.98^{100} \approx 0.867$. One chance in fifty for each, and still very likely overall: that is how a species with long odds for each young survives.
```

</div>

<div class="dl-world" data-world="queues-and-crowds">

23 riders queue for a ride. What is the chance that two of them share a birthday? Can you write `chance_shared(people, days, trials, seed)`? In each trial, each person gets a day from 1 to `days` at random, and the function returns the share of trials in which two people got the same day.

```python exec
id: your-world-1--queues-and-crowds
def chance_shared(people, days, trials, seed):
    """The share of trials in which two of the people share a day."""
    # Your code here.
```

```hint
`[random.randint(1, days) for _ in range(people)]` gives each person a day. Two share a day when the set of days is smaller than the list.
```

```inputs
chance_shared(23, 365, 10000, 1)
chance_shared(5, 365, 10000, 1)
chance_shared(10, 60, 10000, 1)
```

```solution
def chance_shared(people, days, trials, seed):
    """The share of trials in which two of the people share a day."""
    random.seed(seed)
    shared = 0
    for _ in range(trials):
        days_given = [random.randint(1, days) for _ in range(people)]
        if len(set(days_given)) < people:
            shared += 1
    return shared / trials
---
0.5039, and the exact answer is about 0.507: with only 23 riders, two share a birthday about half the time. Most people guess far lower. With 5 riders the chance is about 0.02.
```

</div>

<div class="dl-world" data-world="spread">

At a meeting, one person has an illness, and each of the 5 people they talk to catches it with a chance of 0.2. What is the chance that at least one of them catches it? Can you write `chance_any(k, p, trials, seed)`? In each trial it checks `k` contacts, each with chance `p`, and it returns the share of trials in which at least one caught it.

```python exec
id: your-world-1--spread
def chance_any(k, p, trials, seed):
    """The share of trials in which at least one of k chances, each p, comes true."""
    # Your code here.
```

```hint
In each trial, `any(random.random() < p for _ in range(k))` is `True` when at least one of the `k` checks comes true.
```

```inputs
chance_any(5, 0.2, 10000, 1)
chance_any(1, 0.2, 10000, 1)
chance_any(100, 0.02, 10000, 1)
```

```solution
def chance_any(k, p, trials, seed):
    """The share of trials in which at least one of k chances, each p, comes true."""
    random.seed(seed)
    yes = 0
    for _ in range(trials):
        if any(random.random() < p for _ in range(k)):
            yes += 1
    return yes / trials
---
0.6782, and the exact answer is $1 - 0.8^5 \approx 0.672$. One contact is caught about one time in five; five contacts, two times in three. Each extra contact adds less than the one before, because the illness only has to pass on once.
```

</div>

<div class="dl-world" data-world="space-and-physics">

Ten meteors appear during an hour, each in a minute chosen at random. What is the chance that two appear in the same minute? Can you write `chance_shared(people, days, trials, seed)`? In each trial, each of `people` meteors gets a minute from 1 to `days` at random, and the function returns the share of trials in which two got the same minute.

```python exec
id: your-world-1--space-and-physics
def chance_shared(people, days, trials, seed):
    """The share of trials in which two of the people share a day."""
    # Your code here.
```

```hint
`[random.randint(1, days) for _ in range(people)]` gives each meteor a minute. Two share a minute when the set of minutes is smaller than the list.
```

```inputs
chance_shared(10, 60, 10000, 1)
chance_shared(5, 60, 10000, 1)
chance_shared(23, 365, 10000, 1)
```

```solution
def chance_shared(people, days, trials, seed):
    """The share of trials in which two of the people share a day."""
    random.seed(seed)
    shared = 0
    for _ in range(trials):
        days_given = [random.randint(1, days) for _ in range(people)]
        if len(set(days_given)) < people:
            shared += 1
    return shared / trials
---
0.5526, and the exact answer is about 0.548: with ten meteors in sixty minutes, two share a minute more often than not. It is the same question as two people sharing a birthday: 23 people and 365 days give about a half too.
```

</div>

## Thinking it through

**10.** Someone suggests a tidier method. Instead of throwing darts at
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

**11.** You run the dart estimate and get 3.19. A colleague runs exactly the
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

## From earlier

**12.** From [Comprehensions, grids and
aliasing](tutorial:comprehensions-and-grids). Can you write
`estimate_pi_short(n, seed=0)` with a single `sum(1 for ... if ...)`,
in place of the loop? It should give exactly the tutorial's numbers.

```python exec
id: from-earlier-1
def estimate_pi_short(n, seed=0):
    """estimate_pi, with a comprehension in place of the loop."""
    # Your code here.
```

```hint
`sum(1 for _ in range(n) if ...)` counts the darts that pass the test.
Draw `x` before `y`, with `random.random() ** 2 + random.random() ** 2
<= 1`, so the numbers come in the same order as in the loop.
```

```inputs
estimate_pi_short(100)
estimate_pi_short(100000)
```

```solution
def estimate_pi_short(n, seed=0):
    """estimate_pi, with a comprehension in place of the loop."""
    random.seed(seed)
    hits = sum(1 for _ in range(n) if random.random() ** 2 + random.random() ** 2 <= 1)
    return 4 * hits / n
---
3.04 and 3.14844, exactly the tutorial's. The same seed and the same
order of random numbers give the same darts, however the code is
written. Draw `y` before `x` and the numbers still match, because
$x^2 + y^2$ is the same whichever comes first. A test that treats `x`
and `y` differently, such as problem 2's, would change.
```
