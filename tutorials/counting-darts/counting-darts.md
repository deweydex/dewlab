---
title: "Monte Carlo simulation: estimating π with random darts"
year: "2026-2027"
version: 2026.09.27.1
covers:
  a-question-you-can-answer-by-throwing-things:
    covers: [CMPS-LO3]
  one-dart-at-a-time:
    covers: [CMPS-LO3]
  watching-it-settle:
    covers: [CMPS-LO3]
  more-darts-better-on-average:
    covers: [CMPS-LO3, CMPS-LO13]
  your-world:
    touches: [CMPS-LO3]
worlds:
  living-systems: An atoll, a ring-shaped coral reef around a lagoon.
  queues-and-crowds: Two friends meeting at the gate of a theme park.
  spread: A wildfire, stopped by a road.
  space-and-physics: The shadow of an asteroid.
---

# Monte Carlo simulation: estimating π with random darts

In [Random numbers: pseudo-random numbers and
seeds](tutorial:leaving-it-to-chance), we got the computer to give us
unpredictable numbers whenever we asked. On this page we spend those
numbers on something that seems like a strange way to do mathematics. We
calculate the value of π by throwing darts at a wall and counting where
they land.

It is a strange way. It also works. And the reason it works is the basis
of a whole family of methods, called Monte Carlo methods. People use them
on problems where nothing else works.

The *Monte Carlo method* answers a question by making many random cases,
and counting how many of them meet some condition. It is named after the
casino in Monte Carlo, a place built on chance. When we run the method on
a computer, we call it a *Monte Carlo simulation*.

## A question you can answer by throwing things

Picture a square, one unit on each side. Inside it, draw a quarter of a
circle, with its centre at one corner and a radius of 1.

The square's area is $1 \times 1 = 1$. The quarter-circle's area is a
quarter of the area of a full circle of radius 1, which is $\pi/4$.

Now suppose you scatter points across that square completely at random.
What *fraction* of them would you expect to land inside the curve? It
should be the quarter-circle's share of the square:

$$\frac{\text{quarter-circle area}}{\text{square area}} = \frac{\pi/4}{1} = \frac{\pi}{4}$$

We can use this the other way. Take the fraction that lands inside, and
multiply it by 4. That gives an estimate of π. We never measure a
circle. We never use a formula for its area. And we do not need to know
π at the start.

We only need a way to tell whether a point is inside the curve. A point
$(x, y)$ is inside a circle of radius 1, centred on the origin, when
$x^2 + y^2 \le 1$. This is Pythagoras' theorem. It is the only place the
method uses it.

```python exec
id: a-question-you-can-answer-by-throwing-things-1
def inside_circle(x, y):
    """True when the point lies within the quarter-circle of radius 1."""
    return x * x + y * y <= 1

print(inside_circle(0.2, 0.3))   # near the corner the curve encloses
print(inside_circle(0.9, 0.9))   # out past the curve
```

### Your turn

Where does the point $(0.6, 0.8)$ fall?

1. Calculate $0.6^2 + 0.8^2$ on paper first. It is worth doing by hand.
2. Then check with `inside_circle`.

```python exec
id: a-question-you-can-answer-by-throwing-things-2
hint: 0.36 + 0.64. The answer is exactly on the boundary, which is why this particular point is worth asking about.
```

## One dart at a time

Now we throw the darts. Each dart is a pair of random numbers between 0
and 1, one for $x$ and one for $y$. That is what `random.random()`
gives, so each dart costs two calls and nothing else.

The function below throws `n` darts, counts the hits, and returns 4 times
the fraction that landed inside. It sets its own seed, as we did on the
last page. So every call can be repeated, whatever ran before it.

```python exec
id: one-dart-at-a-time-1
import random

def estimate_pi(n, seed=0):
    """Throw n darts at the unit square; return 4 x the fraction inside.

    Seeds itself, so every call is repeatable and independent of whatever
    ran before it — the habit from the last tutorial, doing real work here.
    """
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

The result is 3.04. It came from a hundred darts. The only mathematics was
Pythagoras, and we never even took a square root.

The answer is also wrong in the second decimal place. Think about that
for a moment, because it matters. The method has not made an error.
There is no bug to find. A hundred darts do not hold enough information
to find π more exactly than this, and no amount of care in the code
would change that.

### Your turn

What happens with more darts? Try 1,000, then 10,000. How close does each
one get?

```python exec
id: one-dart-at-a-time-2
hint: The function already takes n as its argument, so this is three calls. Printing the difference from math.pi alongside each estimate makes the comparison easier to read than the estimates alone.
```

## Watching it settle

Three printed numbers tell you that the answer gets better. They do not
show you *how* it gets better, and how it gets better is the most
important thing on this page.

So this version does not throw a batch of darts and report one number.
It keeps a *running estimate*. After every single dart, it records the
estimate of π we would get if we stopped right there. Then it plots all
of those estimates.

Before you run it, what do you think the line will look like?

```python exec
id: watching-it-settle-1
import random
import matplotlib.pyplot as plt

random.seed(0)

hits = 0
running = []
for throw in range(1, 5001):
    x, y = random.random(), random.random()
    if inside_circle(x, y):
        hits += 1
    running.append(4 * hits / throw)

plt.plot(running, linewidth=0.8)
plt.axhline(3.14159, color="grey", linestyle="--", label="π")
plt.ylim(2.6, 3.6)
plt.xlabel("darts thrown")
plt.ylabel("estimate")
plt.legend()
```

That picture holds the main idea of this page. Here are three things to
notice in it.

**It is wild at the start.** With ten darts, one dart more or less moves
the estimate by 0.4. The estimate settles as the count grows. Each new
dart is a smaller part of the total, so it can move the average less.

**It never stops moving.** There is no point where it reaches π and stays
there. It wanders around the answer. At a million darts it will still be
wandering, only in a narrower band.

**It comes from no particular direction.** The estimate is not climbing
up to π, or falling down to it. It crosses the line again and again.
Luck decides whether it is above or below π when you stop.

### Your turn

What does the same plot look like with a different seed?

1. Change `random.seed(0)` to another number, and run the cell again.
2. What stays the same between the two pictures? What changes?

```python exec
id: watching-it-settle-2
hint: Look at the shape of the settling rather than the particular wiggles. The wiggles are different every time; something about them is not.
```

## More darts, better on average

This method has real limits. The table below shows them. For each number
of darts, it prints the estimate, and how far that estimate is from π.

Before you run it, which row do you expect to be closest to π?

```python exec
id: more-is-not-reliably-better-1
import math

for n in [100, 1000, 10000, 100000]:
    estimate = estimate_pi(n)
    print(f"n = {n:>6}   estimate = {estimate:.5f}   off by {abs(estimate - math.pi):.5f}")
```

Read the last column from the top down. A hundred darts are off by about
0.10. A thousand darts are off by about 0.014, which is a real
improvement. Ten thousand darts get to 0.006.

And a hundred thousand darts are off by 0.0069. That is *worse than ten
thousand*.

This is not a mistake in the code, and it is not a bad seed. Ten times
the work gave a slightly worse answer on this run. That is a normal thing
for this method to do. With another seed the numbers will be different,
but the pattern will be the same. On average, more darts give a better
answer, slowly, but not on every single run.

The next cell makes four runs of a hundred thousand darts each, with four
different seeds.

```python exec
id: more-is-not-reliably-better-3
for seed in [0, 1, 2, 3]:
    estimate = estimate_pi(100000, seed=seed)
    print(f"seed = {seed}   estimate = {estimate:.5f}")
```

The four runs give four different answers, two above π and two below.
They disagree from the second decimal place on: some start 3.14, and
some start 3.13. This shows two different questions we can ask about any
model's numbers.

- *Accuracy* is whether the estimates are centred on the true answer. If
  we averaged a great many runs, would the average be π?
- *Precision* is how close the runs are to each other, or how much the
  answer changes when the whole thing is run again.

Darts are accurate. The four runs land on both sides of π, and their
average, 3.14116, is off by less than a thousandth. That is closer than
any one of the four runs. Darts lack precision. Two runs of a hundred
thousand darts can differ by more than a hundredth.

If you know which of the two is missing, you know what will fix it. An
imprecise method, like this one, gets better with more darts, and the
rule below says how much better. An inaccurate method is different. If
every run is off in the same direction, more darts only make you more
sure of the wrong answer, and you need a better method instead.

Underneath all of this is a rule. The typical error shrinks in proportion
to $1/\sqrt{n}$, where $n$ is the number of darts. This page shows the
rule at work, but does not prove it. Here is what it means:

- One more correct decimal place needs about **a hundred times** as many
  darts.
- Two more decimal places need about ten thousand times as many.

That is why nobody calculates π this way. There are far better methods.
But it is still the first example everyone is shown. The arithmetic is
simple, so you notice the behaviour.

### Your turn

A hundred thousand darts give you roughly two correct decimal places.

1. Roughly how many darts would you need for four? Use the rule above to
   find it, before you run anything.
2. Then decide: is running it a good use of your afternoon?

```python exec
id: more-is-not-reliably-better-2
hint: Two more decimal places means the error has to fall by a factor of 100. If error goes as 1/sqrt(n), what does n have to do?
```

## Your world

The darts work on any shape, as long as we can tell whether a point is
inside it. Can you write `estimate_area(inside, width, height, n,
seed=0)`? It throws `n` darts at a box `width` by `height`, counts the
ones for which `inside(x, y)` is `True`, and returns that share of the
box's area.

<div class="dl-world" data-world="living-systems">

An atoll is a ring of coral reef around a lagoon. Seen from above, this
one is the ring between a circle of radius 1 and a circle of radius 0.5,
both centred at (1, 1) in a 2 by 2 square. What is the reef's area?

```python exec
id: your-world-1--living-systems
def inside_reef(x, y):
    """True when the point is on the ring of reef."""
    return 0.25 <= (x - 1) ** 2 + (y - 1) ** 2 <= 1


def estimate_area(inside, width, height, n, seed=0):
    """The share of n random darts that land inside, times the box's area."""
    # Your code here.
```

```hint
It is `estimate_pi` with two changes. A dart is `random.random() *
width` across and `random.random() * height` up, and the answer is the
share of hits times `width * height`, not times 4.
```

```inputs
round(estimate_area(inside_reef, 2, 2, 1000), 3)
round(estimate_area(inside_reef, 2, 2, 100000), 3)
inside_reef(2 / 2, 2 / 2)
```

```solution
def inside_reef(x, y):
    """True when the point is on the ring of reef."""
    return 0.25 <= (x - 1) ** 2 + (y - 1) ** 2 <= 1


def estimate_area(inside, width, height, n, seed=0):
    """The share of n random darts that land inside, times the box's area."""
    random.seed(seed)
    hits = 0
    for _ in range(n):
        x = random.random() * width
        y = random.random() * height
        if inside(x, y):
            hits += 1
    return width * height * hits / n
---
A thousand darts give 2.216, and 100,000 give 2.343. The exact area is the big circle minus the lagoon: $\pi \times 1^2 - \pi \times 0.5^2 = 0.75\pi \approx 2.356$. The darts never needed that formula. For a reef with a ragged edge, there would be no formula, and the darts would work just the same.
```

</div>

<div class="dl-world" data-world="queues-and-crowds">

Two friends each arrive at the gate of a theme park at a random moment
in the same hour. Each waits 10 minutes for the other, then goes in
alone. A dart $(x, y)$ in a 1 by 1 square gives the two arrival times,
as fractions of the hour. What share of the square is "they meet"?

```python exec
id: your-world-1--queues-and-crowds
def they_meet(x, y):
    """True when the two arrival times are within 10 minutes."""
    return abs(x - y) <= 10 / 60


def estimate_area(inside, width, height, n, seed=0):
    """The share of n random darts that land inside, times the box's area."""
    # Your code here.
```

```hint
It is `estimate_pi` with two changes. A dart is `random.random() *
width` across and `random.random() * height` up, and the answer is the
share of hits times `width * height`, not times 4.
```

```inputs
round(estimate_area(they_meet, 1, 1, 1000), 3)
round(estimate_area(they_meet, 1, 1, 100000), 3)
they_meet(1 / 2, 1 / 2)
```

```solution
def they_meet(x, y):
    """True when the two arrival times are within 10 minutes."""
    return abs(x - y) <= 10 / 60


def estimate_area(inside, width, height, n, seed=0):
    """The share of n random darts that land inside, times the box's area."""
    random.seed(seed)
    hits = 0
    for _ in range(n):
        x = random.random() * width
        y = random.random() * height
        if inside(x, y):
            hits += 1
    return width * height * hits / n
---
A thousand darts give 0.279, and 100,000 give 0.307. The exact answer is $1 - (5/6)^2 = 11/36 \approx 0.306$: the friends meet a little under one time in three. Here the "area" is a chance, and the square is every pair of arrival times. That is the Monte Carlo idea at its widest: a fraction of cases.
```

</div>

<div class="dl-world" data-world="spread">

A wildfire burns everything within a distance of 1 of the point (1, 1),
in a 2 by 2 square, except where a road stops it. The road runs up the
square at $x = 1.4$, and nothing past it burns. What area burns?

```python exec
id: your-world-1--spread
def burns(x, y):
    """True when the fire reaches the point."""
    return (x - 1) ** 2 + (y - 1) ** 2 <= 1 and x < 1.4


def estimate_area(inside, width, height, n, seed=0):
    """The share of n random darts that land inside, times the box's area."""
    # Your code here.
```

```hint
It is `estimate_pi` with two changes. A dart is `random.random() *
width` across and `random.random() * height` up, and the answer is the
share of hits times `width * height`, not times 4.
```

```inputs
round(estimate_area(burns, 2, 2, 1000), 3)
round(estimate_area(burns, 2, 2, 100000), 3)
burns(2 / 2, 2 / 2)
```

```solution
def burns(x, y):
    """True when the fire reaches the point."""
    return (x - 1) ** 2 + (y - 1) ** 2 <= 1 and x < 1.4


def estimate_area(inside, width, height, n, seed=0):
    """The share of n random darts that land inside, times the box's area."""
    random.seed(seed)
    hits = 0
    for _ in range(n):
        x = random.random() * width
        y = random.random() * height
        if inside(x, y):
            hits += 1
    return width * height * hits / n
---
A thousand darts give 2.26, and 100,000 give 2.335. The exact area, from a formula for a slice of a circle that this page does not need, is about 2.349: the road saves about a quarter of the circle's $\pi \approx 3.14$. Change the road, and the darts answer at once. The formula would have to be worked out again.
```

</div>

<div class="dl-world" data-world="space-and-physics">

An asteroid's shadow, seen from a spacecraft, is an ellipse: 4 wide and
2 tall, centred at (2, 1) in a 4 by 2 box. What is its area?

```python exec
id: your-world-1--space-and-physics
def in_shadow(x, y):
    """True when the point is inside the ellipse."""
    return (x - 2) ** 2 / 4 + (y - 1) ** 2 <= 1


def estimate_area(inside, width, height, n, seed=0):
    """The share of n random darts that land inside, times the box's area."""
    # Your code here.
```

```hint
It is `estimate_pi` with two changes. A dart is `random.random() *
width` across and `random.random() * height` up, and the answer is the
share of hits times `width * height`, not times 4.
```

```inputs
round(estimate_area(in_shadow, 4, 2, 1000), 3)
round(estimate_area(in_shadow, 4, 2, 100000), 3)
in_shadow(4 / 2, 2 / 2)
```

```solution
def in_shadow(x, y):
    """True when the point is inside the ellipse."""
    return (x - 2) ** 2 / 4 + (y - 1) ** 2 <= 1


def estimate_area(inside, width, height, n, seed=0):
    """The share of n random darts that land inside, times the box's area."""
    random.seed(seed)
    hits = 0
    for _ in range(n):
        x = random.random() * width
        y = random.random() * height
        if inside(x, y):
            hits += 1
    return width * height * hits / n
---
A thousand darts give 6.144, and 100,000 give 6.258. The exact area of an ellipse with half-widths 2 and 1 is $\pi \times 2 \times 1 \approx 6.283$. A real asteroid is lumpy, and has no formula for its shadow. A spacecraft's camera could still throw darts at its picture.
```

</div>

## Lab bench

Every number this experiment uses is named at the top of the cell.
Change them, run it, and see what happens.

```python exec
id: lab-bench-1
import math
import matplotlib.pyplot as plt

DARTS = 10000      # darts in each run
RUNS = 20          # how many runs
FIRST_SEED = 0     # the runs use seeds FIRST_SEED, FIRST_SEED + 1, and so on

estimates = [estimate_pi(DARTS, seed=FIRST_SEED + run) for run in range(RUNS)]
print(f"lowest:  {min(estimates):.4f}")
print(f"highest: {max(estimates):.4f}")
print(f"average: {sum(estimates) / len(estimates):.4f}")

plt.hist(estimates, bins=10)
plt.axvline(math.pi, color="grey", linestyle="--", label="π")
plt.xlabel("estimate")
plt.ylabel("runs")
plt.legend()
```

Choose one of these questions, or ask one of your own:

1. Multiply `DARTS` by 100. How much narrower does the gap between the
   lowest and highest get? Is that what the $1/\sqrt{n}$ rule says?
2. Twenty runs of 10,000 darts use 200,000 darts in all. Is their
   average closer to π than one run of 200,000 darts?
3. Change `inside_circle` to a shape whose area you know exactly, such
   as a triangle. Do the darts find it?
4. How many darts does one run need before every one of 20 runs starts
   with 3.14?

## Reflection

There is no formula for π anywhere in the method on this page. The
method does not know what π is. It counts a fraction, and the shape of
the question we asked gives us π.

That idea goes far beyond circles. Can you write a quantity as "the
fraction of cases where something is true"? Then you can estimate it by
making cases and counting them. Plenty of real questions have that
shape, and have no formula at all. What fraction of delivery routes finish
before 5pm? How often does this design fail when it is busy? We need
simulation to answer questions like these, and we can throw darts at them
as easily as at a quarter-circle.

Did the wandering estimate feel uncomfortable to look at? Most of the
mathematics you have met so far gives an answer that is exactly right.
This method gives an answer that is *roughly* right. We can only describe
how far off it is using statistics. It asks you to trust an answer in a
different way. It makes sense to feel uncomfortable about that.

## Where to read more

Metropolis, N. and Ulam, S. (1949). *The Monte Carlo Method.* Journal of the
American Statistical Association, 44(247), 335–341.
<https://doi.org/10.1080/01621459.1949.10483310>. This is the paper that
named the method. The authors wrote it while they were using the method on
problems nobody could solve any other way. It is short, and much easier to
read than its date suggests.

Downey, A. B. (2014). *Think Stats* (2nd ed.). O'Reilly.
<https://greenteapress.com/thinkstats2/>. Chapter 9 uses simulation to answer
statistical questions without formulas. It applies this tutorial's argument
to real data.

Robert, C. P. and Casella, G. (2004). *Monte Carlo Statistical Methods*
(2nd ed.). Springer. This is the standard graduate reference, far beyond
this course's level. We list it because Chapter 1's opening pages make
the same argument as this tutorial. The method is most useful on
problems where no formula is available. It is worth seeing the people
who use it for real work say so.

AlphaPhoenix (2016). *RainPi: Calculate Pi with Raindrops!*
<https://www.youtube.com/watch?v=I-BC_vI4CAE>. Our darts are random
numbers from Python. Brian Haidet used real raindrops instead, falling on
sensors shaped to do the same job. The video is four minutes long.

PurpleMind (2025). *Why Do Random Matchsticks Calculate Pi?*
<https://www.youtube.com/watch?v=8stFid5aI9k>. Drop matchsticks on a floor
of straight lines, count how many cross a line, and pi appears. This video
shows why. It is eight minutes long.
