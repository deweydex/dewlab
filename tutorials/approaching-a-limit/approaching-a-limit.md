---
title: "Limits: getting closer without arriving"
year: "2026-2027"
version: 2026.09.26.1
covers:
  a-hole-in-a-line:
    covers: [MIT-3.5]
  getting-closer-without-arriving:
    covers: [MIT-3.5]
  when-there-is-no-limit:
    covers: [MIT-3.5]
  why-we-need-limits:
    covers: [MIT-3.5]
  limits-in-your-world:
    covers: [MIT-3.5]
worlds:
  sea-and-sky: A harbour lock, draining. The numbers are made up.
  planets-and-moons: A ball dropped on the Moon, where things fall more slowly.
  fantasy-maps: A stone from the castle's catapult. The numbers are made up.
---

# Limits: getting closer without arriving

A limit answers a question of this kind: *what would this value be, if
we could get there?*

That can sound like a way of avoiding the question. Calculus began, in
the 1600s, with numbers that were "infinitely small": smaller than any
number you could name, but still not zero. For about two hundred years,
mathematicians were uneasy about those numbers. The philosopher George
Berkeley called them "the ghosts of departed quantities". Limits solved
this problem. A limit says the same thing using only ordinary numbers.
Limits became one of the most useful ideas in mathematics. They are the one idea we still need before we can say how
fast something is changing at a single instant.

A computer makes limits easy to see. We can try
numbers and watch what happens.

On this page we:

- look at a function with a hole in it, and ask what belongs in the hole
- get closer and closer to a point, from both sides
- meet functions that have no limit, and a limit "at infinity"
- use a limit to find the speed of a falling ball at one instant
- see where trying numbers stops working, and why

## A hole in a line

Here is a function that behaves normally everywhere except at one point.
Look at the values in the loop. Can you guess a short rule for the
answers before you run it?

```python exec
id: a-hole-in-a-line-1
def f(x):
    return (x ** 2 - 1) / (x - 1)


for value in [0, 0.5, 2, 3, 10]:
    print(f"f({value}) = {f(value)}")
```

Each answer is one more than the input: $x + 1$. There is a reason. The
top, $x^2 - 1$, factorises into $(x - 1)(x + 1)$. The $(x - 1)$ on the
top then cancels the $(x - 1)$ on the bottom, and $x + 1$ is left.

That works everywhere except at one place. What do you think happens at
$x = 1$? Run the cell to check.

```python exec
id: a-hole-in-a-line-2
print(f(1))
```

Python stops with a `ZeroDivisionError`. At $x = 1$ the bottom is zero,
so we are not allowed to cancel, and the function has no value there at
all. Remember that the domain of a function is the set of inputs it
accepts. The domain of `f` is every number except 1.

Here is the graph. The empty circle marks the missing point.

```python exec
id: a-hole-in-a-line-3
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(7, 4))
xs = [x / 100 for x in range(-100, 301) if abs(x / 100 - 1) > 0.005]
ax.plot(xs, [f(x) for x in xs], linewidth=2)
ax.plot([1], [2], "o", markerfacecolor="white", markeredgecolor="tab:blue",
        markersize=10, markeredgewidth=2)
ax.axhline(0, color="black", linewidth=0.8)
ax.axvline(0, color="black", linewidth=0.8)
ax.grid(alpha=0.3)
ax.set_title("A straight line with one point missing")
```

It is a normal straight line with a hole in it.

This leads to the question that limits answer. **The function has no
value at 1. But if it did have one, what would that value have to be?**

## Getting closer without arriving

We cannot ask for `f(1)`. But we can ask for `f` of numbers very close
to 1, from below and from above. What do you expect to see? Run the cell
and watch the answers.

```python exec
id: getting-closer-without-arriving-1
print("coming up from below")
for step in [0.1, 0.01, 0.001, 0.0001, 0.00001]:
    x = 1 - step
    print(f"   f({x:<10}) = {f(x)}")

print()
print("coming down from above")
for step in [0.1, 0.01, 0.001, 0.0001, 0.00001]:
    x = 1 + step
    print(f"   f({x:<10}) = {f(x)}")
```

From below, the answers climb towards 2. From above, they fall towards
2. Neither side ever *reaches* 2, because neither side ever reaches 1.

(You may notice long tails of digits, such as `1.990000000000001`. Those
are tiny rounding errors in the computer's arithmetic. We come back to
them at the end of the page.)

A *limit* is the value a function gets closer and closer to as its
input gets closer to some point. Here, **the limit of $f(x)$ as $x$
approaches 1 is 2.** In symbols, we write:

$$\lim_{x \to 1} f(x) = 2$$

Those symbols mean *we can make the output as close to 2 as we like, by
taking the input close enough to 1.*

Look at what that sentence does *not* say. It does not say that the
function equals 2 at 1. The function has no value at 1.

**A limit is about the numbers near a point. It says nothing about the
point itself.** Mathematicians call the numbers near a point its
*neighbourhood*. This is the whole idea. It lets a limit describe
places a function cannot reach.

### Both sides have to agree

Here is a function that jumps. It gives −1 for every negative number,
and 1 for zero and every positive number. What happens as we come
towards 0 from each side?

```python exec
id: getting-closer-without-arriving-2
def step_function(x):
    return -1 if x < 0 else 1


print("from below:")
for step in [0.1, 0.01, 0.001]:
    print(f"   step_function({-step}) = {step_function(-step)}")

print("from above:")
for step in [0.1, 0.01, 0.001]:
    print(f"   step_function({step}) = {step_function(step)}")
```

Coming towards zero from the left, the answers stay at −1. From the
right, they stay at 1. The two sides do not agree, so there is no single
number the function is moving towards.

So **this limit does not exist.** The calculation is not hard. The
question has two different answers, depending on which side we come
from, and a limit needs one.

### Your turn

What is the limit of $\dfrac{x^2 - 4}{x - 2}$ as $x$ approaches 2?

1. Try values of `g` just below 2 and just above 2.
2. Then factorise the top, $x^2 - 4$, and cancel.
3. Does the algebra agree with your numbers?

```python exec
id: your-turn-1
def g(x):
    return (x ** 2 - 4) / (x - 2)


# Your investigation here.
```

## When there is no limit

Not every hole can be filled. Sometimes getting closer makes things
worse. Here is $h(x) = \dfrac{1}{x}$, near 0. What do you think happens
to the answers as the step gets smaller?

```python exec
id: when-there-is-no-limit-1
def h(x):
    return 1 / x


for step in [0.1, 0.01, 0.001, 0.0001]:
    print(f"h({step}) = {h(step):>12.1f}     h({-step}) = {h(-step):>12.1f}")
```

From the right, the answers grow bigger and bigger, with no end. From
the left, they fall lower and lower, with no end. There is no number
they are getting close to, from either side.

```python exec
id: when-there-is-no-limit-2
fig, ax = plt.subplots(figsize=(7, 4))
left = [x / 100 for x in range(-300, -3)]
right = [x / 100 for x in range(3, 301)]
ax.plot(left, [1 / x for x in left], linewidth=2, color="tab:blue")
ax.plot(right, [1 / x for x in right], linewidth=2, color="tab:blue")
ax.axhline(0, color="black", linewidth=0.8)
ax.axvline(0, color="tab:red", linestyle=":", linewidth=1.5)
ax.set_ylim(-20, 20)
ax.grid(alpha=0.3)
ax.set_title("No limit at zero, in either direction")
```

You have met this shape twice before. In
[Straight lines: slope, and the line that breaks the formula](tutorial:slope-and-lines),
a vertical line had no slope. In
[The unit circle: sine, cosine and tangent](tutorial:the-unit-circle),
the tangent function had no value at 90 degrees. All three have the
same cause. We are dividing by something that is shrinking to nothing.

### A limit at infinity

We can also ask what happens as $x$ gets very *large*, instead of very
close to a point. What do you think happens to $\dfrac{1}{x}$ as $x$
grows?

```python exec
id: when-there-is-no-limit-3
for x in [1, 10, 100, 1000, 100000, 10000000]:
    print(f"1/{x:<10} = {1 / x}")
```

As $x$ grows, $\dfrac{1}{x}$ moves towards 0 and never gets there. That is a
limit too. A *limit at infinity* is the value a function settles on as
its input grows without end. Here, the limit as $x$ approaches infinity
is 0:

$$\lim_{x \to \infty} \frac{1}{x} = 0$$

Here is a more interesting one: $\dfrac{3n + 5}{n + 2}$. What number do
you think it settles on as $n$ grows? Make a guess, then run the cell.

```python exec
id: when-there-is-no-limit-4
# A more interesting one: what does this settle on?
def ratio(n):
    return (3 * n + 5) / (n + 2)


for n in [1, 10, 100, 1000, 100000]:
    print(f"n = {n:<8} -> {ratio(n)}")
```

It settles on 3. We could have guessed this. When $n$ is very large, the
$+5$ and the $+2$ are tiny next to $3n$ and $n$. That leaves
$\dfrac{3n}{n}$, which is 3.

## Why we need limits

Here is the question that this page has been building towards. We
cannot answer it without a limit:

**How fast is something changing at one instant?**

Speed is distance divided by time. To measure it, we need two moments:
a start and an end. At a single instant, the distance travelled is 0
and the time taken is 0. That gives $\dfrac{0}{0}$, which is not a
number.

Here is a ball dropped from a height. After $t$ seconds, it has fallen
about $4.9t^2$ metres. For example, after 2 seconds it has fallen
$4.9 \times 2^2 = 4.9 \times 4 = 19.6$ metres.

```python exec
id: why-anybody-needs-this-1
def fallen(t):
    return 4.9 * t ** 2


print("After 1 second:", fallen(1), "m")
print("After 2 seconds:", fallen(2), "m")
print()
print("Average speed over that second:", fallen(2) - fallen(1), "m/s")
```

That is the *average* speed over a whole second. The ball was getting
faster the whole time, so this is not its speed at any one moment.

So let's make the time interval smaller. The function `average_speed`
below divides the distance fallen by the length of the interval, which
we call the `gap`. What do you think happens to the answers as the gap
shrinks?

```python exec
id: why-anybody-needs-this-2
def average_speed(t, gap):
    return (fallen(t + gap) - fallen(t)) / gap


print("Speed at t = 1, measured over shorter and shorter intervals:")
for gap in [1, 0.5, 0.1, 0.01, 0.001, 0.0001, 0.00001]:
    print(f"   gap of {gap:<9} : {average_speed(1, gap)}")
```

The numbers are moving towards 9.8, and they never arrive. We cannot set
the gap to zero, because that gives $\dfrac{0}{0}$.

**But the limit exists, and it is 9.8 m/s.** That is the speed at the
instant $t = 1$. It is a real answer to a question that ordinary
arithmetic could not answer.

The graph shows the same thing. The gap gets smaller as we move to the
right, and the average speed gets closer to the red line at 9.8.

```python exec
id: why-anybody-needs-this-3
fig, ax = plt.subplots(figsize=(7, 4))
gaps = [1 / (1.6 ** k) for k in range(22)]
ax.plot(gaps, [average_speed(1, g) for g in gaps], "o-", markersize=4)
ax.axhline(9.8, color="tab:red", linestyle="--", label="9.8")
ax.set_xscale("log")
ax.invert_xaxis()
ax.set_xlabel("size of the gap (getting smaller to the right)")
ax.set_ylabel("average speed over that gap")
ax.grid(alpha=0.3)
ax.legend()
ax.set_title("Closing in on the speed at one instant")
```

### Your turn

1. How fast is the ball travelling three seconds after it is released? Use
   `average_speed` with `t = 3` and smaller and smaller gaps.
2. Now try `t = 0`. Does your answer make sense for a ball that has only
   just been released?

```python exec
id: your-turn-2
# Your code here.
```

## Limits in your world

<div class="dl-world" data-world="sea-and-sky">

A harbour lock is draining. Its depth is $(3 - 0.1t)^2$ metres, $t$
minutes after the gates open. How fast is the depth changing at
$t = 10$? Can you write `rate_at(t)`, using a gap that shrinks, as
`average_speed` did? What does a negative answer mean here?

```python exec
id: limits-in-your-world-1--sea-and-sky
def depth(t):
    return (3 - 0.1 * t) ** 2
```

```hint
Divide the change in depth over a small gap by the gap. Try smaller and
smaller gaps, and watch where the answers are going.
```

```inputs
round(rate_at(10), 3)
round(rate_at(0), 3)
```

```solution
def rate_at(t, gap=1e-7):
    return (depth(t + gap) - depth(t)) / gap


for gap in [1, 0.1, 0.01, 0.001]:
    print(gap, (depth(10 + gap) - depth(10)) / gap)
---
The answers move towards $-0.4$. At $t = 10$ the depth is falling by
0.4 metres a minute. The minus sign says it is falling, not rising. At
the start, $t = 0$, it falls faster: 0.6 metres a minute.
```

</div>

<div class="dl-world" data-world="planets-and-moons">

On the Moon, a dropped ball falls about $0.81t^2$ metres in $t$ seconds.
How fast is it falling after 3 seconds? Can you write `speed_at(t)`,
using a gap that shrinks, as `average_speed` did? How does it compare
with the 29.4 m/s on the Earth?

```python exec
id: limits-in-your-world-1--planets-and-moons
def moon_fallen(t):
    return 0.81 * t ** 2
```

```hint
Divide the distance fallen over a small gap by the gap. Try smaller and
smaller gaps, and watch where the answers are going.
```

```inputs
round(speed_at(3), 3)
round(speed_at(1), 3)
```

```solution
def speed_at(t, gap=1e-7):
    return (moon_fallen(t + gap) - moon_fallen(t)) / gap


for gap in [1, 0.1, 0.01, 0.001]:
    print(gap, (moon_fallen(3 + gap) - moon_fallen(3)) / gap)
---
The answers move towards 4.86. After 3 seconds the ball is falling at
4.86 m/s, about a sixth of the 29.4 m/s it would have on the Earth. The
Moon pulls about a sixth as hard.
```

</div>

<div class="dl-world" data-world="fantasy-maps">

A stone leaves the castle's catapult going straight up. Its height is
$20t - 4.9t^2$ metres after $t$ seconds. How fast is it going after 1
second? After 3? Can you write `speed_at(t)`, using a gap that shrinks,
as `average_speed` did? What does a negative speed mean here?

```python exec
id: limits-in-your-world-1--fantasy-maps
def height(t):
    return 20 * t - 4.9 * t ** 2
```

```hint
Divide the change in height over a small gap by the gap. Try smaller
and smaller gaps, and watch where the answers are going.
```

```inputs
round(speed_at(1), 3)
round(speed_at(3), 3)
```

```solution
def speed_at(t, gap=1e-7):
    return (height(t + gap) - height(t)) / gap


for gap in [1, 0.1, 0.01, 0.001]:
    print(gap, (height(1 + gap) - height(1)) / gap)
---
After 1 second the stone is rising at 10.2 m/s. After 3 seconds the
answer is $-9.4$: the stone is falling, at 9.4 m/s. Between the two, at
about 2.04 seconds, the speed is 0. That is the top of its flight.
```

</div>

## A warning about trying it with numbers

Everything above worked by computing values and looking at them. That is
an excellent way to *see* a limit. It is not a proof. And there is a
point where floating-point arithmetic, the way a computer stores
decimals, starts to give wrong answers.

Here is the first function again, much closer to 1 than before. What do
you think happens as the step gets tiny?

```python exec
id: a-warning-about-trying-it-with-numbers-1
def f(x):
    return (x ** 2 - 1) / (x - 1)


for step in [1e-10, 1e-13, 1e-15, 1e-16]:
    x = 1 + step
    try:
        print(f"f(1 + {step:<8}) = {f(x)}")
    except ZeroDivisionError:
        print(f"f(1 + {step:<8}) = the arithmetic gave up")
```

(`1e-16` is Python's way of writing $10^{-16}$, which is
0.0000000000000001.)

The first three lines print 2.0. The fourth line is not a number at all.

In double-precision floating point, **`1 + 1e-16` is the same number as
`1`**. There is no room left to record such a small difference. So
`x - 1` on the bottom is exactly zero, and the division fails.

Look at *how* it failed. The answers did not drift away from 2. They
printed 2.0, and then the calculation stopped. This is a helpful way to
fail, because you cannot miss it.

**The mathematics works. The computer's arithmetic does not have enough
digits.** The limit is still 2. Nothing about the function changed at
`1e-16`. The computer could no longer tell `1 + 1e-16` from `1`.

The ball's speed from earlier fails in a less kind way. The cell below asks
`average_speed` for the speed at $t = 3$, with smaller and smaller gaps.
The true answer is 29.4. Guess before you run it: what happens at a gap
of `1e-16`?

```python exec
id: a-warning-about-trying-it-with-numbers-2
for gap in [1e-6, 1e-10, 1e-12, 1e-14, 1e-15, 1e-16]:
    print(f"gap {gap:<8}   speed = {average_speed(3, gap)}")
```

The answers drift away from 29.4, a little and then a lot. At `1e-16`,
the cell prints 0.0, with no error at all. `3 + 1e-16` is stored as 3,
so the two distances are the same number, and the top of the fraction
is exactly zero. The speed is still 29.4. The arithmetic ran out of
digits again, but this time there was no error. A wrong number that
looks like an answer is much harder to catch than a calculation that
stops.

### How small should the gap be?

A big gap gives a chord that is not the tangent. A tiny gap runs out of
digits. So there must be a best gap somewhere between. The next cell
measures the error, how far each answer is from 29.4, for every gap
from 1 down to $10^{-16}$, and draws them. Both axes use a log scale, as
in [Charts: choosing the right chart for your data](tutorial:pictures-worth-numbers):
each step of the grid is ten times the one before, so that tiny numbers
and big ones fit on one picture.

```python exec
id: how-small-should-the-gap-be-1
gaps = [10 ** -k for k in range(17)]
errors = [abs(average_speed(3, gap) - 29.4) for gap in gaps]

fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(gaps, errors, "o-")
ax.set_xscale("log")
ax.set_yscale("log")
ax.invert_xaxis()
ax.set_xlabel("gap (getting smaller to the right)")
ax.set_ylabel("error: distance from 29.4")
ax.grid(alpha=0.3)
ax.set_title("The error, for every gap")
```

```predict
type: choice

As the gap gets smaller, what will the errors do?

- Keep getting smaller
  - A smaller gap gives a chord closer to the tangent, so every answer
    should be better than the last.
- Get smaller, then bigger again
- Stay about the same
```

The errors make a V. On the left, where the gaps are big, the error is
about 4.9 times the gap, because the chord is not yet the tangent. Each
gap ten times smaller makes the error ten times smaller. On the right,
where the gaps are tiny, the arithmetic runs out of digits, and the
error grows as the gap shrinks. The bottom of the V, at a gap of about
$10^{-7}$ or $10^{-8}$, is the best this way of measuring can do. There
the answer is right to about six decimal places. The last point, at
$10^{-16}$, is the silent 0.0: the error is the whole 29.4.

The next page measures slopes with a gap of `1e-6`, and a better way of
measuring, with one point on each side. That gap is near the bottom of
that method's own V.

You met the same problem on the practice page for
[Variables, data types and text](tutorial:storing-and-computing). There,
`0.1 + 0.2 == 0.3` gave `False`, because two floats that should have
been equal were not.

So we use the numbers to *see* what the answer is, and we use algebra to
*know* it. In the very first example, cancelling $(x - 1)$ tells us that
the function is $x + 1$, so the limit is exactly 2, with no
approximation anywhere.

## Looking back

A limit is the value a function moves towards, whether or not it ever
gets there. It is about the numbers near a point, not the point itself,
and both sides have to agree. Some limits do not exist. A limit turns
"how fast is it changing right now?", which is $\dfrac{0}{0}$ if we ask
it directly, into a question we can answer. Numbers show you the
answer, and algebra proves it. Past about fifteen decimal places, the
numbers stop showing you anything.

In a few sentences, in your own words: what is the difference between
"$f(1) = 2$" and "the limit of $f(x)$ as $x$ approaches 1 is 2"?

A challenge: the best gap for the ball at $t = 3$ was about $10^{-8}$.
Is it the same for the ball at $t = 100$, or for a car whose distance is
$2t^3$ at $t = 2$? Can you draw the V for each, and find where its
bottom moves?

```python challenge
import matplotlib.pyplot as plt


def fallen(t):
    return 4.9 * t ** 2


def average_speed(f, t, gap):
    return (f(t + gap) - f(t)) / gap


gaps = [10 ** -k for k in range(17)]
errors = [abs(average_speed(fallen, 100, gap) - 980) for gap in gaps]

fig, ax = plt.subplots()
ax.plot(gaps, errors, "o-")
ax.set_xscale("log")
ax.set_yscale("log")
ax.invert_xaxis()
```

## Where to read more

Grant Sanderson (3Blue1Brown) (2017). *Essence of Calculus, Chapter 7:
Limits, L'Hôpital's Rule, and Epsilon Delta Definitions.*
<https://www.youtube.com/watch?v=kfF40MiS7zA>. This video gives the
formal definition behind "getting closer without arriving". This page
only tried numbers.

Up and Atom (2020). *3 Paradoxes That Gave Us Calculus.*
<https://www.youtube.com/watch?v=EbHqtENNnSY>. Jade Tan-Holmes tells three
old puzzles about the infinitely small, and shows how trying to answer
them led to the limit. It is about fourteen minutes long.
