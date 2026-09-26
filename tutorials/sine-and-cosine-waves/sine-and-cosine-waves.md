---
title: "Sine and cosine waves: amplitude, period and shift"
year: "2026-2027"
version: 2026.09.26.1
datasets: [daylight, dublin-tides]
covers:
  why-it-repeats:
    covers: [MIT-3.3]
  the-four-numbers:
    covers: [MIT-3.3]
  where-a-wave-comes-from:
    covers: [MIT-3.3]
  waves-in-your-world:
    covers: [MIT-3.3]
worlds:
  sea-and-sky: Daylight in Dublin, and the tide at Dublin Port, both measured.
  sound: The notes of a guitar, and the waves they make in the air.
  planets-and-moons: Daylight in Cape Town, on the other side of the equator, measured.
  fantasy-maps: The windmill beside the castle, and the height of a sail's tip. The numbers are made up.
---

# Sine and cosine waves: amplitude, period and shift

In [The unit circle: sine, cosine and tangent](tutorial:the-unit-circle)
a point went round a circle, and we wrote down how far across and how
far up it was. What happens if we draw how high the point is against how
far round it has gone? Watch the point on the left, and the curve on the
right.

```python exec
id: unrolling-the-circle-1
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

frames = 24
angles = [2 * math.pi * k / frames for k in range(frames + 1)]

figure, (left, right) = plt.subplots(1, 2, figsize=(5.5, 2.4),
                                     gridspec_kw={"width_ratios": [1, 2]})
rim = [2 * math.pi * k / 100 for k in range(101)]
left.plot([math.cos(a) for a in rim], [math.sin(a) for a in rim], color="lightgrey")
left.set_aspect("equal")
left.set_xlim(-1.2, 1.2)
left.set_ylim(-1.2, 1.2)
right.set_xlim(0, 2 * math.pi)
right.set_ylim(-1.2, 1.2)
right.axhline(0, color="black", linewidth=0.6)
right.set_xlabel("distance round (radians)")

hand, = left.plot([], [], color="tab:orange")
curve, = right.plot([], [], color="tab:blue")
dot, = right.plot([], [], "o", color="tab:orange")


def draw_step(k):
    a = angles[k]
    hand.set_data([0, math.cos(a)], [0, math.sin(a)])
    curve.set_data(angles[:k + 1], [math.sin(b) for b in angles[:k + 1]])
    dot.set_data([a], [math.sin(a)])


FuncAnimation(figure, draw_step, frames=frames, interval=120)
```

The orange dot on the right is always as high as the tip of the hand on
the left. As the hand goes round, the dot moves along, and the curve it
leaves behind is the sine. Nothing new has been defined. The curve is
the up column of the table on the circle page, with the angle along the
bottom.

Can you change `frames = 24` to 12, and see the separate steps? What
happens if `draw_step` uses `math.cos` in place of `math.sin` for the
curve and the dot?

What do you think we get if we draw the across column as well?

```python exec
id: unrolling-the-circle-2
fig, ax = plt.subplots(figsize=(8, 4))
turns = [t / 300 for t in range(301)]
ax.plot(turns, [math.sin(t * 2 * math.pi) for t in turns], linewidth=2, label="up (sine)")
ax.plot(turns, [math.cos(t * 2 * math.pi) for t in turns], linewidth=2, label="across (cosine)")
ax.axhline(0, color="black", linewidth=0.8)
ax.grid(alpha=0.3)
ax.legend()
ax.set_xlabel("turns")
ax.set_title("Both columns, unrolled")
```

We get a second curve, the cosine. The two curves have the same shape,
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

The curve repeats exactly, every turn, in both directions.

This happens because the point goes round a circle. After a full turn
you are back at the same point, so you must be at the same height, and
the curve must do the same thing again.

A curve that repeats exactly like this is *periodic*. The length of one
repeat is its *period*. For sine and cosine as we have drawn them, the
period is one turn. That is $2\pi$ radians, or 360 degrees, depending on
which unit you count in.

So what is $\sin(10\pi)$? $10\pi$ is five whole turns.

```python exec
id: why-it-repeats-2
print(math.sin(10 * math.pi))
```

```predict
type: number
tolerance: 0.000001

What will the cell print?
```

Python prints `-1.2246467991473533e-15`. The `e-15` means "times
$10^{-15}$", so this is $-0.0000000000000012$. Five whole turns bring the
point back to $(1, 0)$, where the up value is 0. Python's `math.pi` is a
decimal, a tiny bit away from the real $\pi$, so the answer is a tiny
bit away from 0.

### Your turn

What is $\cos(4\pi)$? What about $\sin(2.5\pi)$? Can you answer without
plotting anything? Write your reasoning as a comment first. Then
remove the `#` from the two `print` lines, and run the cell.

```python exec
id: your-turn-1
# Your reasoning as a comment.
# print(math.cos(4 * math.pi))
# print(math.sin(2.5 * math.pi))
```

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Yours may be different and work too.

$4\pi$ is two whole turns, so the point is back at $(1, 0)$, and the
cosine is 1. $2.5\pi$ is one whole turn and a quarter more, so the point
is at the top of the circle, $(0, 1)$, and the sine is 1.

</details>

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

Let's build the function and change the numbers one at a time. Our
`wave` function takes the period itself, in the same units as $x$,
because that is easier to read from a picture.

```python exec
id: the-four-numbers-1
def wave(amplitude=1, period=1, shift=0, lift=0):
    """A sine wave with the four numbers as arguments."""
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

Each of the four numbers has its own separate effect. None of them
changes what the others do.

| Number | In the formula | What it does |
|---|---|---|
| amplitude | $A$ | makes the wave taller or shorter |
| period | set by $B$ | makes one repeat longer or shorter |
| shift | $C$ | slides the wave left or right |
| lift | $D$ | slides the wave up or down |

The same pattern, one number and one visible change, happened with lines
in [Functions and their graphs](tutorial:drawing-functions), and with
quadratics in [Parabolas: completing the square](tutorial:parabolas).

A note on the names. The wave swings up and down about a middle line,
$y = D$. That line is called the *midline*, and moving it is called a
*vertical shift*. So `lift` is the vertical shift. The *amplitude* is
how far the wave swings from its midline. It is not the height from top
to bottom, so a wave of amplitude 2 is 4 tall in total. What we call
`shift` is a sideways shift, and it usually has the name *phase*.

Here is a wave with an amplitude of 1.5 and a lift of 0.5. The cell
finds the highest value it reaches.

```python exec
id: the-four-numbers-5
tallest = wave(amplitude=1.5, lift=0.5)
print(max(tallest(x / 100) for x in range(100)))
```

```predict
type: number
tolerance: 0.01

What is the highest value the wave reaches?
```

The wave swings 1.5 above its midline, and the midline is at 0.5, so the
top is at 2.0. The bottom is at $0.5 - 1.5 = -1$.

One more fact is useful later. A sine wave crosses its midline going up
at $x = C$, and it reaches its peak a quarter of a period after that.

### Your turn

The cell below draws four waves, without showing their numbers. It also
defines `gap_to_data`, which measures how far a curve is from some
points, on average. How might you find the four numbers for each wave,
by reading the picture?

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

xs = [i / 200 for i in range(-100, 501)]


def gap_to_data(curve, xs, ys):
    """The average distance between a curve and some measured points."""
    total = 0
    for i in range(len(xs)):
        total += abs(curve(xs[i]) - ys[i])
    return total / len(xs)


fig, axes = plt.subplots(2, 2, figsize=(10, 6))
for i in range(4):
    cell = axes.flat[i]
    cell.axhline(0, color="black", linewidth=0.8)
    cell.grid(alpha=0.3)
    cell.plot(xs, [targets[i](x) for x in xs])
    cell.set_ylim(-4.5, 4.5)
    cell.set_title(f"wave {i}")
fig
```

Read the four numbers of a wave from its picture. Then move the four
sliders to make your own wave with them. The cell draws your wave over
the target and measures the gap between them. The gap is 0 when your
wave lies exactly on the target. When it is not 0, which part of your
wave is furthest away? The last slider chooses which of the four waves
to aim at.

```python exec
id: your-turn-3
amplitude = slider("amplitude", 0.0, 3.0, step=0.1, value=1.0)
period = slider("period", 0.25, 2.5, step=0.05, value=1.0)
shift = slider("shift", -1.0, 1.0, step=0.05, value=0.0)
lift = slider("lift", -2.0, 2.0, step=0.1, value=0.0)
which = slider("which wave", 0, 3)

mine = wave(amplitude.value, period.value, shift.value, lift.value)
target = targets[which.value]

fig, ax = plt.subplots(figsize=(8, 3.5))
ax.plot(xs, [target(x) for x in xs], linewidth=4, alpha=0.4, label=f"wave {which.value}")
ax.plot(xs, [mine(x) for x in xs], label="mine")
ax.set_ylim(-4.5, 4.5)
ax.grid(alpha=0.3)
ax.legend(fontsize=8)
print("gap:", round(gap_to_data(mine, xs, [target(x) for x in xs]), 3))
```

When you have tried all four, `print(answers)` in a new cell shows the
numbers the page chose. Yours can be different and still give a gap of
0. How?

```hint
Start with the midline. Where is the middle of the wave, halfway
between its top and its bottom? That is the lift. How far is the top
above the midline?
```

```hint
after: 2 minutes
title: Reading the other two

The period is the distance from one peak to the next. For the shift,
find a place where the wave crosses its midline going up. Any one of
them works, and that is why two different shifts can both give a gap
of 0.
```

## Where a wave comes from

Why would anybody want this? When we draw anything that goes round and
comes back, with time along the bottom, we get a wave. Daylight through
the year, the tides, a spinning motor, a sound and an alternating
current all make waves.

Here is a year of daylight in Dublin: the hours from sunrise to sunset,
on every day of 2026. The numbers come from the copy of the file saved
on {{snapshot: daylight}}.

```python exec
id: where-a-wave-comes-from-1
table = await load_csv("daylight.csv")
hours = table[table.place == "Dublin"]["daylight_hours"].tolist()
days = list(range(len(hours)))    # day 0 is 1 January

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(days, hours, ".", markersize=3, label="daylight in Dublin")
ax.grid(alpha=0.3)
ax.set_xlabel("day of 2026 (0 = 1 January)")
ax.set_ylabel("hours")
ax.legend()
ax.set_title("A year of daylight in Dublin")
print("longest:", max(hours), "hours, on day", hours.index(max(hours)))
print("shortest:", min(hours), "hours, on day", hours.index(min(hours)))
```

Does that shape look familiar?

The Earth goes round the Sun once a year, and its axis is tilted. The
tilt always points the same way in space. So for half the year, our
half of the Earth leans towards the Sun, and the days are long. For the
other half, it leans away, and the days are short. The lean changes
smoothly and comes back every year, so we expect a wave. There is
[a closer look at the seasons](tutorial:why-we-have-seasons) that tests
this against another idea many people hold.

Fitting a wave means finding its four numbers. We can read each one from
the data:

- The midline is halfway between the longest day, 17.02 hours, and the
  shortest, 7.5 hours. That is 12.26, so the lift is 12.26.
- The amplitude is how far the longest day is above the midline:
  $17.02 - 12.26 = 4.76$.
- The wave repeats once a year, so the period is 365 days.
- The longest day is day 171, which is 21 June. A sine wave peaks a
  quarter of a period after its shift, and a quarter of 365 is 91.25.
  So the shift is $171 - 91.25 = 79.75$.

```python exec
id: where-a-wave-comes-from-2
guess = wave(amplitude=4.76, period=365, shift=79.75, lift=12.26)

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(days, hours, ".", markersize=3, label="measured")
ax.plot(days, [guess(d) for d in days], label="a wave with four numbers in it")
ax.axhline(12.26, color="grey", linestyle=":", label="the midline")
ax.grid(alpha=0.3)
ax.legend(fontsize=8)
ax.set_xlabel("day of 2026")
ax.set_title("Fitting a wave to data")

print("gap:", round(gap_to_data(guess, days, hours) * 60, 1), "minutes")
```

The wave is close. On an average day it is about 10 minutes away from
the measured daylight. We did not compute any of the four numbers. We
read each one from the data.

Look at the shift, day 79.75. The wave crosses its midline going up on
about 21 March. That is close to the spring *equinox*, on 20 March in
2026, when the Sun is straight above the equator. Its name comes from
the Latin for "equal night".

### Your turn

Can you move the sliders until the gap is smaller? The period stays at
365 days, and the sliders change the other three numbers. There is no
formula for this. Look at where the curve is furthest from the points,
and change the number that controls that part. How small can you make
the gap? Why can it never be 0?

```python exec
id: your-turn-4
amplitude = slider("amplitude", 3.0, 6.0, step=0.02, value=4.76)
shift = slider("shift", 60.0, 100.0, step=0.25, value=79.75)
lift = slider("lift", 11.0, 13.5, step=0.01, value=12.26)

better = wave(amplitude.value, 365, shift.value, lift.value)

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(days, hours, ".", markersize=3, label="measured")
ax.plot(days, [better(d) for d in days], label="mine")
ax.set_ylim(6, 18)
ax.legend()
ax.grid(alpha=0.3)
print("gap:", round(gap_to_data(better, days, hours) * 60, 1), "minutes")
```

<details class="dl-answer"><summary>one way to think about it</summary>

Here is one answer. Yours may be different and work too.

Near the longest and shortest days, the measured points are flatter than
the wave: they stay near the top and bottom for longer. A smaller
amplitude, about 4.5, brings the wave closer there, and the gap falls to
about 7 minutes. It cannot reach 0, because daylight through a year is
not exactly a sine wave. The wave is a model of the data, and the gap
says how close the model is.

</details>

## Waves in your world

<div class="dl-world" data-world="sea-and-sky">

The tide rises and falls at Dublin Port about twice a day. The cell
loads two days of it, 1 and 2 March 2026, one reading an hour. The
numbers come from the copy of the file saved on
{{snapshot: dublin-tides}}. Can you read the four numbers from the
picture, and make `tide`, a wave with a small gap? Keep the gap, in
metres, as `tide_gap`.

```python exec
id: waves-in-your-world-1--sea-and-sky
tides = await load_csv("dublin-tides.csv")
levels = tides["level_m"].tolist()[:48]    # the first two days
hours_since = list(range(48))

fig, ax = plt.subplots(figsize=(8, 3.5))
ax.plot(hours_since, levels, "o-", markersize=3)
ax.grid(alpha=0.3)
ax.set_xlabel("hours since midnight on 1 March")
ax.set_ylabel("metres")
```

```hint
How many high tides are there in two days? The period is the time from
one high tide to the next. It is not a whole number of hours.
```

```inputs
round(tide(0), 2)
round(tide(10), 2)
round(tide_gap, 2)
```

```solution
tide = wave(amplitude=1.5, period=12.42, shift=6.75, lift=2.75)
tide_gap = gap_to_data(tide, hours_since, levels)
print("gap:", tide_gap, "metres")
---
Here is one set of numbers, found by trying: an amplitude of 1.5 m, a
period of 12.42 hours, a shift of 6.75 hours and a lift of 2.75 m. The
gap is about 0.16 m. Numbers read from the picture, with a period of
about 12.4 hours, give a gap of about 0.26 m. One high tide is higher
than the next, which no single wave can match. The period of 12.42
hours, 12 hours and 25 minutes, comes from the Moon.
```

</div>

<div class="dl-world" data-world="sound">

A sound is a wave in the air. The air's pressure rises and falls very
fast, hundreds of times a second. The number of waves each second is
the *frequency*, measured in hertz (Hz). The cell draws a note from a
guitar for one hundredth of a second. Can you read its period from the
picture, in milliseconds? Then write `frequency_from_period(ms)`. Which
note is it: A at 440 Hz, E at 330 Hz, or D at 294 Hz?

```python exec
id: waves-in-your-world-1--sound
mystery = wave(amplitude=1, period=1 / 330)
seconds = [i / 100000 for i in range(1001)]

fig, ax = plt.subplots(figsize=(8, 3.5))
ax.plot([s * 1000 for s in seconds], [mystery(s) for s in seconds])
ax.grid(alpha=0.3)
ax.set_xlabel("milliseconds")
```

```hint
How many whole waves fit in the 10 milliseconds? The period is 10 ms
divided by that. A frequency is waves each second, and a second is 1000
milliseconds.
```

```inputs
frequency_from_period(3.03)
frequency_from_period(2.27)
frequency_from_period(1000)
```

```solution
def frequency_from_period(ms):
    return 1000 / ms
---
About 3.3 waves fit in 10 ms, so the period is about 3.03 ms, and the
frequency is $1000 \div 3.03 \approx 330$ Hz. The note is E. A at 440 Hz
has a period of about 2.27 ms.
```

</div>

<div class="dl-world" data-world="planets-and-moons">

Cape Town is far south of the equator. The cell loads its daylight for
2026, from the same file as Dublin's. Can you read the four numbers
from the picture, and make `cape`, a wave with a small gap? Keep the
gap, in minutes, as `cape_gap`. What is different about the shift, and
why?

```python exec
id: waves-in-your-world-1--planets-and-moons
cape_hours = table[table.place == "Cape Town"]["daylight_hours"].tolist()

fig, ax = plt.subplots(figsize=(8, 3.5))
ax.plot(days, cape_hours, ".", markersize=3)
ax.grid(alpha=0.3)
ax.set_xlabel("day of 2026 (0 = 1 January)")
print("longest:", max(cape_hours), "on day", cape_hours.index(max(cape_hours)))
print("shortest:", min(cape_hours), "on day", cape_hours.index(min(cape_hours)))
```

```hint
Read the numbers as we did for Dublin: the midline, the amplitude, the
period, and the day of the longest day. The shift is a quarter of a
year before the longest day.
```

```inputs
round(cape(0), 2)
round(cape(172), 2)
round(cape_gap, 1)
```

```solution
cape = wave(amplitude=2.27, period=365, shift=257.75, lift=12.15)
cape_gap = gap_to_data(cape, days, cape_hours) * 60
print("gap:", cape_gap, "minutes")
---
The longest day is 14.42 hours, on day 349 in mid-December, and the
shortest is 9.88 hours, in June. So the midline is 12.15, the amplitude
is 2.27, and the shift is $349 - 91.25 = 257.75$, in mid-September. The
gap is about 7.3 minutes. The shift is half a year from Dublin's,
because when the north leans towards the Sun, the south leans away. The
amplitude is smaller, because Cape Town is closer to the equator than
Dublin is.
```

</div>

<div class="dl-world" data-world="fantasy-maps">

The windmill beside the castle has sails 6 m long, turning round a hub
10 m above the ground, once every 8 seconds. At 0 seconds a sail points
straight out to the right, and it turns anticlockwise. The height of
its tip is a wave. What are its four numbers? Can you write
`tip_height(seconds)` with `wave`, and draw 16 seconds of it?

```python exec
id: waves-in-your-world-1--fantasy-maps
hub_height = 10    # metres
sail = 6           # metres
turn_seconds = 8
```

```hint
Which of the four numbers is the hub's height? Which is the sail's
length? The tip starts on the midline, going up.
```

```inputs
round(tip_height(0), 2)
round(tip_height(2), 2)
round(tip_height(6), 2)
```

```solution
tip_height = wave(amplitude=sail, period=turn_seconds, shift=0, lift=hub_height)

seconds = [i / 10 for i in range(161)]
fig, ax = plt.subplots(figsize=(8, 3.5))
ax.plot(seconds, [tip_height(s) for s in seconds])
ax.grid(alpha=0.3)
---
The amplitude is the sail, 6 m. The period is 8 seconds. The shift is
0, because the tip starts on the midline going up. The lift is the
hub's height, 10 m, which is the midline. The tip is 16 m up after 2
seconds and 4 m up after 6.
```

</div>

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
down. So the across value is zero, and a slope of "up divided by
nothing" has no value. It is the vertical line from
[Straight lines: slope, and the line that breaks the formula](tutorial:slope-and-lines)
again.

## Two waves at once

Here is something to try if you have time. What happens when we add two
waves together? A guitar chord is several notes at once, and each note
is a wave. The cell adds an A, at 440 Hz, to an E above it, at 660 Hz.

```python exec
id: two-waves-at-once-1
a_note = wave(period=1 / 440)
e_note = wave(period=1 / 660)
seconds = [i / 200000 for i in range(2001)]    # one hundredth of a second

fig, ax = plt.subplots(figsize=(8, 3.5))
ax.plot([s * 1000 for s in seconds], [a_note(s) + e_note(s) for s in seconds])
ax.grid(alpha=0.3)
ax.set_xlabel("milliseconds")
ax.set_title("Two notes at once")
```

The sum is not a sine wave, but it still repeats. How long is one
repeat? It is about 4.5 milliseconds, which is $\frac{1}{220}$ of a
second: two waves of the A, and three of the E. Notes whose frequencies
make a simple fraction, such as $\frac{660}{440} = \frac{3}{2}$, add up
to a wave that repeats quickly, and many people hear them as sounding
well together.

What happens if you change 660 to 444, so the two notes are very close?
Try a whole second, `range(200001)`, in place of a hundredth. The two
waves go in and out of step four times a second. Musicians hear this
as *beats*, and use it to tune one string to another.

## Looking back

A wave is a circle drawn against time, so it repeats. Its four numbers
each have their own job: the amplitude, the period, the shift, and the
lift, which moves the midline. Measured data, such as daylight, is close
to a wave, and the gap says how close.

Think of something in your own life that repeats. Would it make a wave if
you plotted it? If not, how would its shape be different?

A challenge: the file has daylight for four places, Reykjavik, Dublin,
Accra and Cape Town. Can you fit a wave to each, and put all four on one
picture? Which of the four numbers changes most from place to place, and
why?

```python challenge
import math
import matplotlib.pyplot as plt

table = await load_csv("daylight.csv")
places = ["Reykjavik", "Dublin", "Accra", "Cape Town"]


def wave(amplitude=1, period=1, shift=0, lift=0):
    def f(x):
        return amplitude * math.sin((x - shift) / period * 2 * math.pi) + lift
    return f


fig, ax = plt.subplots(figsize=(8, 4))
for place in places:
    hours = table[table.place == place]["daylight_hours"].tolist()
    ax.plot(range(len(hours)), hours, ".", markersize=2, label=place)
ax.legend()
```

## Where to read more

Khan Academy. *Midline, Amplitude and Period of a Function.*
<https://www.youtube.com/watch?v=s4cLM0l1gd4>. This video uses the same
four numbers this page changes one at a time. It reads them from a graph
rather than from a function.

engineerguy (2014). *Intro/History: Introducing a 100-year-old mechanical
computer.* <https://www.youtube.com/watch?v=NAsM30MAHLg>. Bill Hammack
shows a machine of gears and springs, built about 100 years ago, that adds
sine waves together to draw new curves. This is the first of four short
videos. The second one shows the machine adding waves.
