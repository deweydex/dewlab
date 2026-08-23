---
title: "Sine and Cosine Waves"
slug: sine-and-cosine-waves
module: mit-pdp-maths-prog-integration
module_title: "Programming and Maths, Integrated"
year: "2026-2027"
series: maths-and-programming
version: 2026.08.23.1
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

# Sine and Cosine Waves

**Maths for IT**

The last tutorial defined sine and cosine. This one is about what they look like when you draw them, and what you can do to that shape.

Those are two different activities. The circle is a careful argument about coordinates; this is experiment — change a number, look at what happened, change it back. Both want room, which is why they are two tutorials.

## Unrolling the Circle

Take the point going round the circle and, instead of plotting where it is, plot **how high it is against how far round it has got**.

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

The orange dots are the same six moments in both pictures. On the left they go round; on the right their heights are laid out side by side.

**Nothing new has been defined.** That is the up column from the last tutorial's table, with the angle along the bottom instead of in a column beside it.

Do the same for the across column and you get the other curve.

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

The two curves are the same shape, shifted along by a quarter of a turn. Which makes sense: the point is at its highest a quarter turn after it is at its furthest across.

## Why It Repeats

Keep walking past one full turn.

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

That is not a property the curve happens to have. **It is what going round in a circle looks like when you draw it flat.** After a full turn you are back at the same point, so you must be at the same height, so the curve must do the same thing again.

The proper word is **periodic**, and the length of one repeat is the **period**. For sine and cosine as we have drawn them, that is one turn — or `2π` radians, or 360 degrees, depending on which units you are counting in.

### Your turn

Without plotting anything: what is `sin(10π)`? And `cos(4π)`? Say why, then check.

```python exec
id: your-turn-1
# Your reasoning as a comment.
# print(math.sin(10 * math.pi))
# print(math.cos(4 * math.pi))
```

## The Four Numbers

Here is the general shape of a wave, with four numbers you can change:

`y = A · sin(B(x − C)) + D`

Rather than learning what each letter does, build the function and change them one at a time.

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

Four numbers, four completely separate effects, none of them interfering with the others.

This is the same "one coefficient, one visible change" pattern you met with lines in *Drawing Functions* and with quadratics in *Parabolas*. Third time — it is worth noticing as a habit of mathematics rather than a coincidence, because it is how families of curves are usually built.

A note on the names. **Amplitude** is how far it swings from the middle, not top to bottom — a wave of amplitude 2 is 4 tall in total. **Phase** is the usual word for what is called `shift` here.

```python exec
id: the-four-numbers-5
# All four at once.
mystery = wave(amplitude=1.5, period=0.8, shift=0.2, lift=0.5)
ax = draw(mystery, label="all four changed")
ax.set_title("A wave with all four numbers set")
```

### Your turn

Four waves below, drawn without their numbers shown. For each one, work out the four numbers by reading the picture, then plot your version over the original and see whether it lands.

```python exec
id: your-turn-2
import random

targets = [
    wave(amplitude=2, period=1, shift=0, lift=0),
    wave(amplitude=1, period=0.5, shift=0, lift=1),
    wave(amplitude=0.5, period=2, shift=0.5, lift=0),
    wave(amplitude=3, period=1, shift=0.25, lift=-1),
]

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
```

## Where a Wave Comes From

The section that says why anybody would want this.

**A wave is what anything that goes round and comes back looks like when you plot it against time.** Daylight through the year, the tides, a spinning motor, a sound, an alternating current. All of them are something circling, drawn flat.

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

That shape should look familiar by now.

The earth goes round the sun once a year, which is a circle, and the amount of daylight is a coordinate of where we are on it. So it should be a wave — and fitting one is a matter of finding the four numbers.

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
#   it peaks around June, which is month 6.
guess = fitted(amplitude=5, period=12, shift=3, lift=12)

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(months, daylight, "o", markersize=7, label="real")
fine = [m / 10 for m in range(121)]
ax.plot(fine, [guess(m) for m in fine], label="a wave with four numbers in it")
ax.grid(alpha=0.3)
ax.legend()
ax.set_xlabel("month")
ax.set_title("Fitting a wave to data")
```

Not perfect, and close enough to be useful. Each of the four numbers was read straight off the data rather than computed: **the middle, the swing, the repeat, and where the peak is.**

### Your turn

Adjust the four numbers until the curve sits better on the points. There is no formula for this — look at where it is wrong and change the number responsible.

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

Doing this by eye is the honest version of what a fitting algorithm does automatically, and it is worth doing once by hand so that the automatic version is not magic.

## Tangent, Briefly

The third function is not a wave, and it is worth seeing beside the two that are.

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

It repeats — twice as often as sine — but it does not swing between two limits. It runs away to infinity at every quarter turn and comes back from the other side.

Those red lines are where the point on the circle is straight up or straight down, so the across value is zero, and a slope of "up over nothing" has no value. Same fact as the vertical line in *Lines and Distances*, showing up for the third time.

## Reflection

The circle, laid out flat.

**A wave is a circle drawn against time.** That is why it repeats: after a full turn you are back where you started, so the picture must do the same thing again.

**Four numbers, four separate effects.** Amplitude, period, phase and lift, none of them interfering with the others — the same pattern as lines and quadratics, for the third time.

**Real periodic data is a wave with four numbers in it**, and all four can be read off the data by looking: the middle, the swing, the repeat, and where the peak sits.

**Tangent is not one of these.** It repeats without swinging, and it breaks where the slope of a vertical line breaks.

Write a few sentences: name something in your own life that repeats. Would it plot as a wave, and if not, what would be different about its shape?
