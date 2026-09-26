---
title: "Sine and cosine waves: amplitude, period and shift"
year: "2026-2027"
version: 2026.09.25.1
covers:
  unrolling-the-circle:
    covers: [MIT-3.3]
  why-it-repeats:
    covers: [MIT-3.3]
  the-four-numbers:
    covers: [MIT-3.3]
  where-a-wave-comes-from:
    covers: [MIT-3.3]
---

# Sine and cosine waves: amplitude, period and shift

In [The unit circle: sine, cosine and tangent](tutorial:the-unit-circle)
we defined sine and cosine. On this page we look at what they look like
when we draw them, and at what we can do to that shape.

These are two different kinds of work. The circle page was a careful
argument about coordinates. This page is more like an experiment: change
a number, look at what happened, then change it back. Each kind of work
needs room, and that is why there are two pages.

On this page we:

- unroll the circle into a wave
- see why the wave repeats
- change four numbers that control the wave's shape
- fit a wave to some real data
- look at tangent, and see why it is not a wave

## Unrolling the circle

Take the point going round the circle again. This time, instead of
drawing where the point is, we draw how high it is against how far round
it has gone.

```python exec
id: unrolling-the-circle-1
import math
import matplotlib.pyplot as plt

def unit_point(turns):
    angle = turns * 2 * math.pi
    return (math.cos(angle), math.sin(angle))


fig, (left, right) = plt.subplots(1, 2, figsize=(10, 4.5))

# On the left: the circle, with a few points marked.
circle = [unit_point(t / 300) for t in range(301)]
left.plot([p[0] for p in circle], [p[1] for p in circle], color="lightgrey", linewidth=2)
marks = [0.05, 0.15, 0.30, 0.45, 0.60, 0.80]
for t in marks:
    x, y = unit_point(t)
    left.plot([0, x], [0, y], color="tab:orange", linewidth=1)
    left.plot([x], [y], "o", color="tab:orange")
left.set_aspect("equal")
left.axhline(0, color="black", linewidth=0.6)
left.axvline(0, color="black", linewidth=0.6)
left.set_title("Where the point is")

# On the right: how high it is, against how far round.
turns = [t / 300 for t in range(301)]
right.plot(turns, [unit_point(t)[1] for t in turns], linewidth=2)
for t in marks:
    right.plot([t], [unit_point(t)[1]], "o", color="tab:orange")
right.axhline(0, color="black", linewidth=0.6)
right.grid(alpha=0.3)
right.set_xlabel("turns")
right.set_title("How high it is")
```

The orange dots show the same six moments in both pictures. On the left
they go round the circle. On the right, their heights are laid out side
by side.

We have not defined anything new. The right-hand curve is the up column
(the sine) from the table on the circle page. The only difference is that
the angle now runs along the bottom, instead of sitting in a column
beside it.

What do you think we get if we do the same with the across column?

```python exec
id: unrolling-the-circle-2
fig, ax = plt.subplots(figsize=(8, 4))
turns = [t / 300 for t in range(301)]
ax.plot(turns, [unit_point(t)[1] for t in turns], linewidth=2, label="up (sine)")
ax.plot(turns, [unit_point(t)[0] for t in turns], linewidth=2, label="across (cosine)")
ax.axhline(0, color="black", linewidth=0.8)
ax.grid(alpha=0.3)
ax.legend()
ax.set_xlabel("turns")
ax.set_title("Both columns, unrolled")
```

We get the other curve, the cosine. The two curves have the same shape,
moved along by a quarter of a turn. Why does that make sense? The point
is furthest across at the start, and it reaches its highest point a
quarter turn later.

## Why it repeats

What happens if we keep walking past one full turn?

```python exec
id: why-it-repeats-1
fig, ax = plt.subplots(figsize=(9, 3.5))
turns = [t / 100 for t in range(-100, 301)]
ax.plot(turns, [math.sin(t * 2 * math.pi) for t in turns], linewidth=2)
ax.axhline(0, color="black", linewidth=0.8)
for mark in [-1, 0, 1, 2, 3]:
    ax.axvline(mark, color="tab:red", linestyle=":", linewidth=1)
ax.grid(alpha=0.3)
ax.set_xlabel("turns")
ax.set_title("Three turns forward, one turn back")
```

The curve repeats exactly, every turn, forever, in both directions.

This is not an accident of this one curve. It is what going round in a
circle looks like when you draw it flat. After a full turn you are back
at the same point, so you must be at the same height. So the curve must
do the same thing again.

A curve that repeats exactly like this is *periodic*. The length of one
repeat is its *period*. For sine and cosine as we have drawn them, the
period is one turn. That is $2\pi$ radians, or 360 degrees, depending on
which unit you count in.

### Your turn

What is $\sin(10\pi)$? What is $\cos(4\pi)$? Can you answer without
plotting anything?

1. Write your reasoning as a comment in the cell.
2. Then remove the `#` from the two `print` lines and run the cell to
   check.

```python exec
id: your-turn-1
# Your reasoning as a comment.
# print(math.sin(10 * math.pi))
# print(math.cos(4 * math.pi))
```

If Python prints a tiny number such as `-1.2246467991473533e-15`, read it
as 0. The `e-15` means "times $10^{-15}$". Python's `math.pi` is a
decimal, a tiny bit away from the real $\pi$, so the answer is off by a
very tiny amount.

## The four numbers

Here is the general shape of a wave. It has four numbers, $A$, $B$, $C$
and $D$, that you can change:

$$y = A\sin\big(B(x - C)\big) + D$$

In words: we take $x$ and subtract $C$, multiply by $B$, and take the
sine. Then we multiply by $A$, and add $D$.

$B$ controls the period. When $x$ is in radians, the period is
$\frac{2\pi}{B}$. For example, $B = 2$ gives a period of
$\frac{2\pi}{2} = \pi$, which is half a turn. So a bigger $B$ means a
shorter repeat.

Instead of learning what each letter does from a list, let's build the
function and change the numbers one at a time. Our `wave` function takes
the period directly, measured in turns, because that is easier to read
off a picture.

```python exec
id: the-four-numbers-1
def wave(amplitude=1, period=1, shift=0, lift=0):
    """A sine wave with the four numbers as arguments, in turns."""
    def f(x):
        return amplitude * math.sin((x - shift) / period * 2 * math.pi) + lift
    return f


def draw(f, label=None, ax=None, low=-0.5, high=2.5):
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 3.5))
        ax.axhline(0, color="black", linewidth=0.8)
        ax.grid(alpha=0.3)
        ax.set_xlabel("turns")
    xs = [low + (high - low) * i / 400 for i in range(401)]
    ax.plot(xs, [f(x) for x in xs], label=label)
    if label:
        ax.legend(fontsize=8)
    return ax


ax = draw(wave(), label="the plain one")
draw(wave(amplitude=2), label="amplitude 2", ax=ax)
draw(wave(amplitude=0.4), label="amplitude 0.4", ax=ax)
ax.set_title("Amplitude: how tall")
```

What do you expect a period of 0.5 to look like? And a period of 2?

```python exec
id: the-four-numbers-2
ax = draw(wave(), label="the plain one")
draw(wave(period=0.5), label="period 0.5", ax=ax)
draw(wave(period=2), label="period 2", ax=ax)
ax.set_title("Period: how long one repeat takes")
```

```python exec
id: the-four-numbers-3
ax = draw(wave(), label="the plain one")
draw(wave(shift=0.25), label="shift 0.25", ax=ax)
draw(wave(shift=-0.25), label="shift -0.25", ax=ax)
ax.set_title("Shift: sliding it along")
```

```python exec
id: the-four-numbers-4
ax = draw(wave(), label="the plain one")
draw(wave(lift=1.5), label="lift 1.5", ax=ax)
draw(wave(lift=-1), label="lift -1", ax=ax)
ax.set_title("Lift: sliding it up and down")
```

Did you notice? There are four numbers, and each one has its own separate
effect. None of them changes what the others do.

| Number | In the formula | What it does |
|---|---|---|
| amplitude | $A$ | makes the wave taller or shorter |
| period | set by $B$ | makes one repeat longer or shorter |
| shift | $C$ | slides the wave left or right |
| lift | $D$ | slides the wave up or down |

You have seen this pattern before: one number, one visible change. It
happened with lines in [Functions and their graphs](tutorial:drawing-functions),
and with quadratics in [Parabolas: completing the square](tutorial:parabolas).
This is the third time. It is not a coincidence. It is a habit of
mathematics, because families of curves are usually built this way.

A note on the names. The *amplitude* is how far the wave swings from its
middle line. It is not the height from top to bottom, so a wave of
amplitude 2 is 4 tall in total. What we call `shift` here usually has the
name *phase*.

One more fact is useful later. A sine wave crosses its middle line going
up at $x = C$, and it reaches its peak a quarter of a period after that.

```python exec
id: the-four-numbers-5
# All four at once.
mystery = wave(amplitude=1.5, period=0.8, shift=0.2, lift=0.5)
ax = draw(mystery, label="all four changed")
ax.set_title("A wave with all four numbers set")
```

### Your turn

The cell below draws four waves, without showing their numbers. How
might you work out the four numbers for each one, by reading the picture?

1. Run the cell to see the four waves.
2. For each wave, read off the amplitude, period, shift and lift.
3. In the next cell, make your own wave with those numbers.
4. Draw it over the original, for example with
   `draw(mine, ax=axes[0, 0])` for the top-left wave, and put `fig` on
   the last line to show the pictures again. Does your wave land on top
   of the original?

```python exec
id: your-turn-2
import random

random.seed(11)    # the same four waves every time the cell runs

answers = []
targets = []
for _ in range(4):
    amplitude = random.choice([0.5, 1, 1.5, 2, 3])
    period = random.choice([0.5, 1, 2])
    shift = random.choice([0, 0.25, 0.5])
    lift = random.choice([-1, 0, 1])
    answers.append((amplitude, period, shift, lift))
    targets.append(wave(amplitude, period, shift, lift))

fig, axes = plt.subplots(2, 2, figsize=(10, 6))
for target, cell in zip(targets, axes.flat):
    cell.axhline(0, color="black", linewidth=0.8)
    cell.grid(alpha=0.3)
    xs = [i / 200 for i in range(-100, 501)]
    cell.plot(xs, [target(x) for x in xs])
    cell.set_ylim(-4.5, 4.5)
fig
```

```python exec
id: your-turn-3
# Your guesses. Plot each over its target and see whether it lands.
# mine = wave(amplitude=?, period=?, shift=?, lift=?)

# When you have tried all four, print(answers) shows the numbers the
# cell chose. Yours can be different and still land on top. How?
```

## Where a wave comes from

Why would anybody want this? Here is the answer.

A wave is what we get when we draw anything that goes round and comes
back, against time. Daylight through the year, the tides, a spinning
motor, a sound, an alternating current: each of them is something going
round in a circle, drawn flat.

```python exec
id: where-a-wave-comes-from-1
# Hours of daylight in Dublin, roughly, by month.
daylight = [7.8, 9.5, 11.6, 13.8, 15.8, 16.9, 16.4, 14.7, 12.6, 10.5, 8.6, 7.4]
months = list(range(12))

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(months, daylight, "o-", markersize=7, label="daylight hours")
ax.grid(alpha=0.3)
ax.set_xlabel("month (0 = January)")
ax.set_ylabel("hours")
ax.legend()
ax.set_title("A year of daylight in Dublin")
```

Does that shape look familiar?

The Earth goes round the Sun once a year, and its axis is tilted. The
tilt always points the same way in space. So for half the year, our
half of the Earth leans towards the Sun, and the days are long. For the
other half, it leans away, and the days are short. The lean changes
smoothly and comes back every year, so we expect a wave. Fitting a wave
means finding its four numbers. The comments in
the next cell read each number off the data.

```python exec
id: where-a-wave-comes-from-2
def fitted(amplitude, period, shift, lift):
    def f(month):
        return amplitude * math.sin((month - shift) / period * 2 * math.pi) + lift
    return f


# A first attempt. The four numbers are readable off the data:
#   the highest is about 17 and the lowest about 7, so the middle is 12
#   and it swings about 5 either way;
#   it repeats once a year, so the period is 12 months;
#   it peaks in June, which is month 5 here (0 = January). A sine wave
#   peaks a quarter of a period after its shift, and a quarter of 12
#   months is 3, so the shift is 5 - 3 = 2.
guess = fitted(amplitude=5, period=12, shift=2, lift=12)

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(months, daylight, "o", markersize=7, label="real")
fine = [m / 10 for m in range(121)]
ax.plot(fine, [guess(m) for m in fine], label="a wave with four numbers in it")
ax.grid(alpha=0.3)
ax.legend()
ax.set_xlabel("month")
ax.set_title("Fitting a wave to data")
```

It is not perfect, but it is close enough to be useful. We did not
compute any of the four numbers. We read each one off the data: the
middle, the swing, the repeat, and where the peak is.

### Your turn

Can you change the four numbers until the curve sits better on the
points? There is no formula for this. Look at where the curve is wrong,
and change the number that controls that part.

```python exec
id: your-turn-4
# better = fitted(amplitude=?, period=?, shift=?, lift=?)
#
# fig, ax = plt.subplots(figsize=(8, 4))
# ax.plot(months, daylight, "o", markersize=7, label="real")
# fine = [m / 10 for m in range(121)]
# ax.plot(fine, [better(m) for m in fine], label="mine")
# ax.legend()
# ax.grid(alpha=0.3)
```

Fitting by eye is the hand-made version of what a fitting algorithm does
automatically. It is worth doing once by hand, so that the automatic
version is not a mystery.

## Tangent, briefly

The third function, tangent, is not a wave. It helps to see it beside
sine, which is.

```python exec
id: tangent-briefly-1
fig, ax = plt.subplots(figsize=(9, 4))
turns = [t / 400 for t in range(-200, 601)]
ax.plot(turns, [math.sin(t * 2 * math.pi) for t in turns], label="sine")
ax.plot(turns, [math.tan(t * 2 * math.pi) for t in turns], label="tangent")
for asymptote in [-0.25, 0.25, 0.75, 1.25]:
    ax.axvline(asymptote, color="tab:red", linestyle=":", linewidth=1)
ax.axhline(0, color="black", linewidth=0.8)
ax.set_ylim(-6, 6)
ax.grid(alpha=0.3)
ax.legend()
ax.set_xlabel("turns")
ax.set_title("Tangent is not a wave")
```

Tangent repeats, twice as often as sine: its period is half a turn. But
it does not swing between two limits. Near each red line it grows without
limit, and then it comes back from the other side. The red lines are a
quarter turn, three quarters of a turn, and so on, half a turn apart.

At those red lines, the point on the circle is straight up or straight
down. So the across value is zero, and a slope of "up divided by nothing"
has no value. It is the same fact as the vertical line in
[Straight lines: slope, midpoint and distance](tutorial:lines-and-distances),
showing up for the third time.

## Reflection

On this page we laid the circle out flat.

**A wave is a circle drawn against time.** That is why it repeats. After
a full turn you are back where you started, so the picture must do the
same thing again.

**Four numbers, four separate effects.** Amplitude, period, phase and
lift each do their own job, and none of them changes the others. We saw
the same pattern with lines and quadratics, so this is the third time.

**Real periodic data is a wave with four numbers in it.** You can read
all four off the data by looking: the middle, the swing, the repeat, and
where the peak is.

**Tangent is not one of these.** It repeats without swinging, and it
breaks where the slope of a vertical line breaks.

Think of something in your own life that repeats. Would it make a wave if
you plotted it? If not, how would its shape be different? Write a few
sentences.

## Where to Read More

Khan Academy. *Midline, Amplitude and Period of a Function.*
<https://www.youtube.com/watch?v=s4cLM0l1gd4>. The same four numbers this
page changes one at a time, read the other way round — off a graph rather
than off a function.

engineerguy (2014). *Intro/History: Introducing a 100-year-old mechanical
computer.* <https://www.youtube.com/watch?v=NAsM30MAHLg>. Bill Hammack
shows a machine of gears and springs, built about 100 years ago, that adds
sine waves together to draw new curves. This is the first of four short
videos; the second shows the adding in action.
