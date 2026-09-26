---
title: "Time steps: simulating a falling ball, one step at a time — Practice"
practice_for: stepping-forward-in-time
year: "2026-2027"
version: 2026.09.26.1
---

# Time steps: simulating a falling ball, one step at a time — Practice

The answers are in folds under each problem. Several problems ask what
you expect before you run anything. Write your guess down first: a guess
that misses teaches more than one that was never made.

The cell below holds the two functions from the tutorial. `landing_time`
now takes the strength of gravity too, so that we can drop a ball
somewhere other than Dublin. Run it first.

```python exec
id: setup-1
import math
import matplotlib.pyplot as plt

def landing_time(step, gravity=-9.8):
    height = 60
    velocity = 0
    steps = 0
    while height > 0:
        height = height + velocity * step
        velocity = velocity + gravity * step
        steps = steps + 1
    return steps * step

def bounce_heights(step, seconds, bounciness):
    height = 60
    velocity = 0
    heights = []
    for _ in range(round(seconds / step)):
        height = height + velocity * step
        velocity = velocity - 9.8 * step
        if height < 0:
            height = 0
            velocity = -velocity * bounciness
        heights.append(height)
    return heights
```

## Predicting a Step

**1.** The formula says the ball lands after 3.50 seconds. With a time
step of 1 second, the loop said 5.00. With a time step of 0.1 seconds,
it said 3.60. What do you expect with a time step of 0.5 seconds? Then
run it.

```python exec
id: predicting-a-step-1
print(f"{landing_time(0.5):.2f}")
```

<details class="dl-answer"><summary>answer</summary>

4.00 seconds, half a second late. That fits the pattern from the
tutorial: the answer is late by about one time step, and here the time
step is half a second.

</details>

**2.** Gravity on the Moon is about 1.62 metres per second, every
second: about a sixth of the Earth's. If we dropped a ball from 60
metres on the Moon, would it take six times as long to land? Guess
first, then use `landing_time` with a small time step to see.

```python exec
id: predicting-a-step-2
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. `landing_time` takes the gravity as its second number.
2. Moon gravity pulls down, so it is negative, like `-9.8`.
3. Use a time step of 0.01 so that the answer is close to the truth,
   and compare it with the Earth's 3.50 seconds.

**Think about:** the formula has $t^2$ in it. If gravity is six times
weaker, what happens to $t^2$, and what happens to $t$?

**Try this next:** how tall would a building on the Moon need to be for
a drop to take as long as the drop from Liberty Hall?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
print(f"{landing_time(0.01, gravity=-1.62):.2f}")
```

It prints 8.62. The formula gives 8.61. That is about 2.5 times as
long as on Earth, not six times.

Distance fallen grows with the square of the time. With gravity six
times weaker, $t^2$ has to be six times bigger to fall the same 60
metres, so $t$ is $\sqrt{6}$ times bigger, which is about 2.46.

</details>

## The Other Order

**3.** Here is the loop with its two main lines in the other order: the
velocity changes first, and then the ball moves with the new velocity.
After 3 seconds, the formula puts the ball at $60 - 4.9 \times 3^2 =
15.9$ metres. Where does each order put it, with a time step of 1
second? Guess before you run it: which one will be too high, and which
too low?

```python exec
id: the-other-order-1
height = 60
velocity = 0
for _ in range(3):
    height = height + velocity * 1
    velocity = velocity - 9.8 * 1
print(f"first order:  {height:.1f} m")

height = 60
velocity = 0
for _ in range(3):
    velocity = velocity - 9.8 * 1
    height = height + velocity * 1
print(f"other order:  {height:.1f} m")
```

<details class="dl-answer"><summary>answer</summary>

The first order puts the ball at 30.6 metres, too high. It moves with
the velocity from the start of each step, which is the slowest the ball
goes during that step.

The other order puts it at 1.2 metres, too low. It moves with the
velocity from the end of each step, which is the fastest.

The formula's 15.9 metres is between the two. In fact it is exactly
their average: $(30.6 + 1.2) / 2 = 15.9$. For a ball with steady
gravity, moving with the average of the start and end velocities gives
the exact answer. That idea is the start of better methods than
Euler's.

</details>

**4.** Change `bounce_heights` in the setup cell to use the other order,
and run the perfectly bouncy ball again, with a time step of 1/60 of a
second, as a game would use:

```python
heights = bounce_heights(1 / 60, 40, 1.0)
print(f"highest point: {max(heights):.1f} m")
```

With the first order, this ball climbs to 63.2 metres. What does it do
with the other order? If you were writing a game, which order would you
choose, and why?

```python exec
id: the-other-order-2
```

<details class="dl-answer"><summary>answer</summary>

With the other order, the ball never goes above 60.0 metres. It loses a
little height instead, and by the second half of the 40 seconds its
bounces reach only about 58.6 metres.

Neither order is exact. But the errors go in opposite directions, and
that matters. A ball that loses a little height looks like a ball
meeting some air. A ball that gains height is getting energy from
nowhere, and in a game with many objects touching, that extra energy
can grow until objects shoot off the screen. Most games use the other order for
this reason.

</details>

## Thrown Upwards

**5.** Throw a ball straight up from the street at 15 metres per second.
How high does it go? Can you write a function `highest_point(step)`
that runs the loop and gives back the greatest height the ball reaches?
Physics has a formula for this one too: the highest point is
$15^2 / (2 \times 9.8)$ metres.

```python exec
id: thrown-upwards-1
def highest_point(step):
    height = 0
    velocity = 15
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Keep a name for the greatest height so far, starting at 0.
2. Each step, move the ball and change the velocity, as before.
3. After each step, if the height is greater than the greatest so far,
   keep it. Python's `max` can do that in one line.
4. Stop when the ball is back below the street.

**Think about:** the ball starts at height 0. What does
`while height > 0` do before the first step?

**Try this next:** throw the ball at 30 metres per second instead. Does
it go twice as high?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def highest_point(step):
    height = 0
    velocity = 15
    highest = 0
    while True:
        height = height + velocity * step
        velocity = velocity - 9.8 * step
        highest = max(highest, height)
        if height < 0:
            return highest

for step in [0.1, 0.01, 0.001]:
    print(step, round(highest_point(step), 3))
print("formula:", round(15 ** 2 / (2 * 9.8), 3))
```

The loop gives 12.24, then 11.555, then 11.487 metres. The formula gives
11.48. The same pattern as the falling ball: ten times shorter steps,
about ten times closer.

The ball starts at height 0, so `while height > 0` would stop before
the first step. `while True` with a `return` inside is one way to
handle that; checking the height at the end of each step is another.

Twice the speed sends the ball four times as high, since the formula
has the speed squared.

</details>

## From Earlier Pages

**6.** From [Monte Carlo simulation](tutorial:counting-darts). Run
`landing_time(0.1)` twice. Then think about two runs of a hundred
thousand darts. The darts page split error into accuracy and
precision. Which of the two is missing from `landing_time`, and what
does that tell you about how to make it better?

```python exec
id: from-earlier-pages-1
print(landing_time(0.1))
print(landing_time(0.1))
```

<details class="dl-answer"><summary>answer</summary>

Two runs of `landing_time(0.1)` give the same answer, 3.6, every time,
because nothing in it is random. So it has perfect precision. What it
lacks is accuracy: it is always late, in the same direction.

Running it again, or running it many times and taking the average, can
never help, because every run gives the same number. Only a shorter
time step or a better method moves it closer. With darts it was the
other way round: they were accurate but imprecise, and more darts
helped.

</details>

**7.** From [Simulating a queue](tutorial:when-a-queue-never-clears).
That queue moved in steps of time too. Two chances of an arrival each
step, each with `arrival_prob` of 0.45, and a server that clears 1 item
a step. Stable or unstable? Answer without running anything.

<details class="dl-answer"><summary>answer</summary>

Stable. Average arrivals are $2 \times 0.45 = 0.9$ per step, below
the capacity of 1. The queue keeps coming back to empty, although this
close to 1 it can grow long on an unlucky run.

</details>

**8.** From [Random numbers](tutorial:leaving-it-to-chance). A friend
says that `bounce_heights` should start with `random.seed(1)`, so that
it gives the same answer every time. What would you tell them?

<details class="dl-answer"><summary>answer</summary>

It already gives the same answer every time. A seed fixes the numbers
that `random` produces, and `bounce_heights` never asks `random` for
anything. Every step follows from the one before it by the same
arithmetic. A seed would do nothing here.

</details>

## Where to Read More

braintruffle (2025). *The Code That Revolutionized Orbital Simulation.*
<https://www.youtube.com/watch?v=nCg3aXn5F3M>. Problem 4 swapped two
lines, and a gaining ball became a losing one. This video shows that
same swap keeping simulated planets and asteroids on their orbits for
millions of years, and explains why it works. 28 minutes.

Sebastian Lague (2020). *Coding Adventure: Solar System.*
<https://www.youtube.com/watch?v=7axImc1sxa0>. The time steps from this
page, with gravity pulling between planets instead of down to a street.
He builds a small solar system you can fly through. 12 minutes.
