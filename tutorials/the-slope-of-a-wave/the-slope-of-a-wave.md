---
title: "The slope of a wave: how fast daylight and tides change"
year: "2026-2027"
version: 2026.09.26.1
datasets: [daylight, dublin-tides]
covers:
  the-slope-of-sine:
    covers: [MIT-3.6, MIT-3.3]
  why-the-slope-is-cosine:
    covers: [MIT-3.6, MIT-4.6]
  the-slope-of-any-wave:
    covers: [MIT-3.7, MIT-3.3]
  how-fast-the-days-grow:
    covers: [MIT-3.6, MIT-3.3]
  the-slope-in-your-world:
    covers: [MIT-3.6, MIT-3.3]
worlds:
  sea-and-sky: The tide, and the sailors' rule of twelfths.
  planets-and-moons: Daylight in Reykjavik, Dublin, Cape Town and Accra.
  fantasy-maps: A big wheel at the castle fair. The numbers are made up.
---

# The slope of a wave: how fast daylight and tides change

In [Sine and cosine waves: amplitude, period and shift](tutorial:sine-and-cosine-waves)
a wave described daylight through the year. In
[Derivatives: the rate of change of a curve](tutorial:rates-of-change)
a derivative said how fast something was changing. This page puts the
two together. How fast do the days grow longer in March? And in June?

We start with the plain sine wave. What is its slope at each point? The
cell uses `derivative_at` from the derivatives page, and draws the slope
of `math.sin` underneath the wave.

```python exec
id: the-slope-of-sine-1
import math
import matplotlib.pyplot as plt

def derivative_at(f, x, gap=1e-6):
    """The derivative, computed numerically."""
    return (f(x + gap) - f(x - gap)) / (2 * gap)


xs = [x / 50 for x in range(-50, 400)]
fig, (top, bottom) = plt.subplots(2, 1, figsize=(8, 5.5), sharex=True)
top.plot(xs, [math.sin(x) for x in xs], linewidth=2)
top.set_ylabel("sin x")
bottom.plot(xs, [derivative_at(math.sin, x) for x in xs], linewidth=2, color="tab:orange")
bottom.set_ylabel("its slope")
bottom.set_xlabel("x, in radians")
for ax in (top, bottom):
    ax.axhline(0, color="black", linewidth=0.8)
    ax.grid(alpha=0.3)
```

```predict
type: choice

Before you look closely: what shape will the slope make?

- A straight line
  - The wave goes up and down evenly, so its slope could be even too.
- Another wave, the same shape, moved along
- A parabola
  - The top of the wave looks like the top of a parabola.
```

The slope is another wave, the same size and shape, moved along. Where
have you seen a wave like that, which is 1 at $x = 0$? It looks like the
cosine. Let's check it at every point, and print the biggest difference.

## The slope of sine

```python exec
id: the-slope-of-sine-2
differences = [abs(derivative_at(math.sin, x) - math.cos(x)) for x in xs]
print("the biggest difference:", max(differences))
```

The biggest difference is about $10^{-10}$, the size of the error in
`derivative_at` itself. So the slope of the sine wave is the cosine
wave:

> **The derivative of $\sin x$ is $\cos x$**, when $x$ is in radians.

Read it from the two pictures. Where the sine wave climbs fastest, at
$x = 0$, its slope is 1, the top of the cosine. At the top of the sine
wave, $x = \frac{\pi}{2}$, it is flat for a moment, and the cosine is 0.
Where it falls fastest, at $x = \pi$, the slope is $-1$.

What is the slope of the cosine wave? Can you change the cell above to
draw `derivative_at(math.cos, x)`, and compare it with `-math.sin(x)`?

## Why the slope is cosine

On [the unit circle](tutorial:the-unit-circle) we walked a point round
in tiny steps. Each step went at right angles to the hand, from
$(x, y)$ in the direction $(-y, x)$:

```python
x, y = x - step * y, y + step * x
```

The up value changes by `step * x` for each step round the circle. So
the rate at which the up value changes is $x$, the across value. The up
value is the sine, and the across value is the cosine. That is the
derivative of sine: cosine.

The across value changes by `-step * y` for each step. So its rate is
$-y$, which is minus the sine. The derivative of $\cos x$ is $-\sin x$.

Both rules only hold in radians, because the walk measured the angle as
a distance round the circle. In degrees, the chain rule adds a factor.
$\sin(\text{degrees})$ is $\sin\left(\frac{\pi}{180} \times \text{degrees}\right)$,
so its slope is $\frac{\pi}{180}\cos$, about $0.01745\cos$.

```python exec
id: why-the-slope-is-cosine-1
in_degrees = lambda d: math.sin(math.radians(d))
print("slope of sin at 0, radians:", derivative_at(math.sin, 0))
print("slope of sin at 0, degrees:", derivative_at(in_degrees, 0))
print("pi / 180:                  ", math.pi / 180)
```

## The slope of any wave

A wave from the waves page has four numbers:

$$y = A\sin\left(\frac{2\pi(x - C)}{P}\right) + D$$

with amplitude $A$, period $P$, shift $C$ and lift $D$. What is its
slope? The chain rule from
[Derivative rules: power, sum, product and chain, found by experiment](tutorial:derivative-rules)
answers it. The inside is $\frac{2\pi(x - C)}{P}$, whose slope is
$\frac{2\pi}{P}$. The outside is $A\sin$, whose slope is $A\cos$. The
lift $D$ never changes, so its slope is 0. So:

$$\text{slope} = A \cdot \frac{2\pi}{P} \cdot \cos\left(\frac{2\pi(x - C)}{P}\right)$$

The biggest the cosine can be is 1. So the fastest a wave ever changes
is $A \cdot \frac{2\pi}{P}$: the amplitude times $2\pi$, divided by the
period. It happens where the wave crosses its midline.

```python exec
id: the-slope-of-any-wave-1
def wave(amplitude=1, period=1, shift=0, lift=0):
    def f(x):
        return amplitude * math.sin((x - shift) / period * 2 * math.pi) + lift
    return f


tall = wave(amplitude=3, period=2, lift=5)
print("fastest, by the rule:  ", 3 * 2 * math.pi / 2)
print("slope at the midline:  ", derivative_at(tall, 0))
print("slope at the top:      ", derivative_at(tall, 0.5))
```

## How fast the days grow

Here is the daylight in Dublin again, and the wave that fits it. The
numbers come from the copy of the file saved on
{{snapshot: daylight}}. The wave is the one from the waves page, with an
amplitude of 4.55 hours, which gives a slightly smaller gap.

```python exec
id: how-fast-the-days-grow-1
table = await load_csv("daylight.csv")
hours = table[table.place == "Dublin"]["daylight_hours"].tolist()
days = list(range(len(hours)))

daylight = wave(amplitude=4.55, period=365, shift=79.75, lift=12.26)
print("fastest change:", round(4.55 * 2 * math.pi / 365 * 60, 2), "minutes a day")
```

The slope of the wave is in hours per day, so we multiply by 60 to get
minutes per day. The fastest the days ever grow is about 4.7 minutes a
day. When does that happen, and how fast do they grow in June?

Move the slider to choose a day. The cell draws the tangent line to the
wave on that day, and prints its slope. It also prints the rate from the
measured data, over the week around that day.

```python exec
id: how-fast-the-days-grow-2
day = slider("day of 2026 (0 = 1 January)", 3, 361, value=79).value

wave_rate = derivative_at(daylight, day) * 60
data_rate = (hours[day + 3] - hours[day - 3]) / 6 * 60

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(days, hours, ".", markersize=2, color="grey")
ax.plot(days, [daylight(d) for d in days], color="tab:blue")
slope = derivative_at(daylight, day)
near = [day - 40, day + 40]
ax.plot(near, [daylight(day) + slope * (d - day) for d in near], color="tab:red")
ax.plot([day], [daylight(day)], "o", color="tab:red")
ax.set_ylim(6, 18)
ax.grid(alpha=0.3)
print(f"day {day}: the wave says {wave_rate:.2f} minutes a day,"
      f" the data says {data_rate:.2f}")
```

On day 79, 21 March, the days grow by about 4.7 minutes a day by the
wave, and about 4.2 by the data. On day 171, 21 June, both say 0: the
longest day is the top of the wave, where it is flat. Around 23
September the days shrink as fast as they grew in March.

The wave and the data do not agree exactly, because daylight is not
exactly a sine wave, as the gap on the waves page showed. But the shape
of the answer is the same. The days change fastest at the equinoxes,
and hardly at all at the solstices. Many people notice this: the
evenings seem to stretch quickly in March, and the long days of June
seem to stay the same for weeks.

## The slope in your world

<div class="dl-world" data-world="sea-and-sky">

The tide at Dublin Port fitted a wave with an amplitude of 1.5 m and a
period of 12.42 hours. How fast does the tide rise at its fastest, in
metres an hour? Sailors have an old rule, the *rule of twelfths*: in
the six hours from low to high tide, the water rises by 1, 2, 3, 3, 2
and 1 twelfths of the range, hour by hour. Can you find what a sine wave
says, hour by hour, and compare?

```python exec
id: the-slope-in-your-world-1--sea-and-sky
tide = wave(amplitude=1.5, period=12.42, shift=6.75, lift=2.75)
twelfths = [1 / 12, 2 / 12, 3 / 12, 3 / 12, 2 / 12, 1 / 12]
```

```hint
The fastest rate is the amplitude times $2\pi$, divided by the period.
For the hour-by-hour part, take a half wave from its lowest point: after
$k$ of 6 hours it has risen $\frac{1 - \cos(\pi k / 6)}{2}$ of the
range.
```

```inputs
round(fastest, 3)
[round(r, 3) for r in by_the_wave]
```

```solution
fastest = 1.5 * 2 * math.pi / 12.42

risen = [(1 - math.cos(math.pi * k / 6)) / 2 for k in range(7)]
by_the_wave = [risen[k + 1] - risen[k] for k in range(6)]
for k in range(6):
    print(k + 1, round(by_the_wave[k], 3), round(twelfths[k], 3))
---
At its fastest, halfway between low and high tide, the water rises
about 0.76 m an hour. Hour by hour, a sine wave rises 0.067, 0.183,
0.25, 0.25, 0.183 and 0.067 of the range. The rule of twelfths says
0.083, 0.167, 0.25, 0.25, 0.167 and 0.083. The rule is a sine wave's
slope, made easy to work out in your head.
```

</div>

<div class="dl-world" data-world="planets-and-moons">

The fastest a daylight wave changes is its amplitude times $2\pi$,
divided by 365, in hours a day. The waves page read these amplitudes
from the data: Reykjavik 8.5 hours, Dublin 4.76, Cape Town 2.27 and
Accra 0.325. Can you write `fastest_change(amplitude)`, in minutes a
day, and find it for each place?

```python exec
id: the-slope-in-your-world-1--planets-and-moons
amplitudes = {"Reykjavik": 8.5, "Dublin": 4.76, "Cape Town": 2.27, "Accra": 0.325}
```

```hint
The rate in hours a day is the amplitude times $2\pi$, divided by 365.
How do you turn hours into minutes?
```

```inputs
round(fastest_change(8.5), 2)
round(fastest_change(0.325), 2)
```

```solution
def fastest_change(amplitude):
    return amplitude * 2 * math.pi / 365 * 60


for place, amplitude in amplitudes.items():
    print(place, round(fastest_change(amplitude), 2), "minutes a day")
---
At the equinoxes, Reykjavik's days change by nearly 9 minutes a day,
Dublin's by nearly 5, Cape Town's by about 2.3, and Accra's by only
about a third of a minute. The further a place is from the equator, the
bigger its daylight wave, and the faster its days change in spring and
autumn.
```

</div>

<div class="dl-world" data-world="fantasy-maps">

The big wheel at the castle fair has a radius of 20 m, its centre 22 m
above the ground, and it turns once every 4 minutes. A rider gets on at
the bottom. Their height is $22 - 20\cos\left(\frac{2\pi t}{4}\right)$
metres after $t$ minutes. How fast are they rising after 1 minute? When
are they rising fastest? Can you write `rising(t)` with the rules, and
check it with `derivative_at`?

```python exec
id: the-slope-in-your-world-1--fantasy-maps
def height(t):
    return 22 - 20 * math.cos(2 * math.pi * t / 4)
```

```hint
The derivative of $\cos$ is $-\sin$. The inside, $\frac{2\pi t}{4}$,
has slope $\frac{2\pi}{4}$.
```

```inputs
round(rising(1), 2)
round(rising(0), 2)
round(derivative_at(height, 1), 2)
```

```solution
def rising(t):
    return 20 * (2 * math.pi / 4) * math.sin(2 * math.pi * t / 4)
---
The minus from $-\sin$ and the minus in front of the 20 cancel. After 1
minute, a quarter of the way round, the rider is level with the centre
and rising fastest: about 31.4 m a minute. At the bottom and the top,
the rate is 0 for a moment.
```

</div>

## Looking back

The slope of the sine wave is the cosine wave, and the walk round the
unit circle shows why: the up value grows at the rate of the across
value. The chain rule gives the slope of any wave. It is fastest where
the wave crosses its midline, and 0 at the top and the bottom. So the
days grow fastest at the equinoxes.

The slope of sine is cosine, and the slope of cosine is minus sine.
What is the slope of the slope of the slope of the slope of sine? Can
you say it before you check it?

A challenge: the tide data itself, one reading an hour, has a rate too:
the change from one hour to the next. Can you draw the measured rate
for the first two days of March, and the slope of the fitted wave, on
one picture? Where do they differ most?

```python challenge
import math
import matplotlib.pyplot as plt

tides = await load_csv("dublin-tides.csv")
levels = tides["level_m"].tolist()[:48]

rates = [levels[h + 1] - levels[h] for h in range(47)]
fig, ax = plt.subplots()
ax.plot(range(47), rates, "o-", label="measured, metres an hour")
ax.legend()
```

## Where to read more

3Blue1Brown (2017). *Derivative formulas through geometry: Chapter 3,
Essence of calculus.* <https://www.youtube.com/watch?v=S0_qX4VJhMQ>.
Grant Sanderson shows why the slope of sine is cosine with a point
moving round a circle, as this page did with the walk.

Stand-up Maths. *An unexciting video about distance derivatives.*
<https://www.youtube.com/watch?v=sB2X5l5CsNs>. Matt Parker looks at the
derivatives of distance, one after another: speed, acceleration, and
the ones after those. It is about 24 minutes long.
