---
title: "Sine and cosine waves: amplitude, period and shift — Practice"
practice_for: sine-and-cosine-waves
year: "2026-2027"
version: 2026.09.26.1
datasets: [daylight, dublin-tides]
worlds:
  sea-and-sky: The tide at Dublin Port through a whole month, measured.
  sound: Two notes that are nearly the same.
  planets-and-moons: Daylight in Reykjavik, far to the north, measured.
  fantasy-maps: A water wheel on the river by the mill. The numbers are made up.
---

# Sine and cosine waves: amplitude, period and shift — Practice

The answers are hidden under each problem. Several of these problems are
about reading a picture, so plot first, and check the answer afterwards.

## Tools

This cell gives you the `wave` and `draw` functions from the tutorial.
Run it once before you start.

```python exec
id: tools-1
import math
import matplotlib.pyplot as plt

def wave(amplitude=1, period=1, shift=0, lift=0):
    """A sine wave. Period and shift are measured in turns."""
    def f(x):
        return amplitude * math.sin((x - shift) / period * 2 * math.pi) + lift
    return f


def draw(f, low=-0.5, high=2.5, label=None, ax=None):
    xs = [low + (high - low) * i / 400 for i in range(401)]
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 3.5))
        ax.axhline(0, color="black", linewidth=0.8)
        ax.grid(alpha=0.3)
        ax.set_xlabel("turns")
    ax.plot(xs, [f(x) for x in xs], label=label)
    if label:
        ax.legend(fontsize=8)
    return ax


draw(wave(), label="the plain one")
```

## Reading the four numbers

**1.** For $y = 3\sin x$, what are the highest and lowest values?

<details class="dl-answer"><summary>answer</summary>

3 and −3. The amplitude is how far the wave swings *from the middle*, so
the total height from top to bottom is 6.

Many people miss this. An amplitude of 3 does not mean a range of 3.

</details>

**2.** For $y = \sin x + 5$, what are the highest and lowest values?
Where is the middle?

<details class="dl-answer"><summary>answer</summary>

6 and 4, with the middle at 5. The lift moves the whole wave up. It does
not change how far the wave swings.

</details>

**3.** A wave has a maximum of 11 and a minimum of 3. What are its
amplitude and its lift?

<details class="dl-answer"><summary>answer</summary>

The middle is $\frac{11 + 3}{2} = 7$, so the lift is 7. The swing is
$\frac{11 - 3}{2} = 4$, so the amplitude is 4.

Half the sum gives the middle, and half the difference gives the swing.
You can read any wave from its highest and lowest values this way.

</details>

**4.** Which of these repeats fastest?

- (a) a sine wave with period 1 turn
- (b) a sine wave with period 0.25 turns
- (c) a sine wave with period 4 turns

<details class="dl-answer"><summary>answer</summary>

(b). A shorter period means more repeats in the same distance.

A *smaller* period means a *faster* wave. This can feel backwards at
first. That is why people often use the *frequency* instead. The frequency
is the number of repeats in one unit of time, and it is 1 divided by the
period.

</details>

**5.** A wave completes 50 cycles per second. What is its period?

<details class="dl-answer"><summary>answer</summary>

$\frac{1}{50} = 0.02$ seconds.

Fifty cycles per second is the mains electricity in Ireland. So one
full cycle of the voltage takes 0.02 seconds.

</details>

## Periodicity

Problems 7 and 8 ask for an angle when you know its sine or cosine. For
that, Python has `math.asin` (the inverse sine) and `math.acos` (the
inverse cosine). Both give an answer in radians, so use `math.degrees`
on the answer. For example, `math.degrees(math.asin(0.5))` gives about
30.

**6.** Here is a wave with an amplitude of 2 and a period of half a
turn. The cell asks for its value an eighth of a turn along.

```python exec
id: periodicity-1
print(wave(amplitude=2, period=0.5)(0.125))
```

```predict
type: number
tolerance: 0.01

What will it print?
```

<details class="dl-answer"><summary>why</summary>

It prints 2.0. An eighth of a turn is a quarter of this wave's period,
because the period is half a turn. A sine wave is at its peak a quarter
of a period along, and the peak is the amplitude, 2.

</details>

**7.** We know that $\sin\theta = 0.6$. Give two values of $\theta$
between 0° and 360°.

<details class="dl-answer"><summary>answer</summary>

About 36.87° and about 143.13°.

On the way up and over the top of the circle, the point reaches every
height between 0 and 1 twice. The second angle is 180° minus the first.
This fact is behind the ambiguous case of the sine rule, which you will
meet in
[Solving triangles: the sine rule and the cosine rule](tutorial:solving-triangles).

</details>

**8.** We know that $\cos\theta = 0.6$. Give two values of $\theta$
between 0° and 360°.

<details class="dl-answer"><summary>answer</summary>

About 53.13° and about 306.87°.

For cosine, the second angle is 360° minus the first, not 180° minus. The
two points with the same across value are mirror images of each other
across the horizontal axis. For sine, the mirror is the vertical axis.

</details>

**9.** Why must a sine wave repeat?

<details class="dl-answer"><summary>answer</summary>

A sine wave is a point going round a circle, drawn against how far it
has gone. After a full turn the point is back where it started. So its
height is the same as before, and the curve must do the same thing
again.

The curve does not repeat by chance.

</details>

## Fitting

**10.** Sketch $y = 2\sin x + 1$ by hand. Where is the middle? The top?
The bottom? Then plot it and compare.

<details class="dl-answer"><summary>answer</summary>

The middle is at 1, the top at 3 and the bottom at −1. There is one full
cycle per turn. The wave starts at the middle and goes up.

```python
draw(wave(amplitude=2, lift=1), label="2 sin(x) + 1")
```

</details>

**11.** In a harbour, the water is 5.2 m deep at high tide and 1.4 m deep
at low tide. High tides are about 12.4 hours apart. Write a wave for the
depth.

<details class="dl-answer"><summary>answer</summary>

Middle $= \frac{5.2 + 1.4}{2} = 3.3$.
Amplitude $= \frac{5.2 - 1.4}{2} = 1.9$.
Period $= 12.4$ hours.

$$\text{depth}(t) = 1.9\sin\left(\frac{2\pi(t - \text{shift})}{12.4}\right) + 3.3$$

Choose the shift so that the peak lands at the time of high tide.

</details>

**12.** Using that model, how deep is the water six hours after high
tide?

<details class="dl-answer"><summary>answer</summary>

Half a period is 6.2 hours. Six hours is a little less than that, so it
is near low tide. The model gives about 1.41 m, very
slightly above the minimum of 1.4 m.

Half a period after a peak is exactly the lowest point, and six hours is
a little short of that.

</details>

**13.** Daylight in Dublin runs from about 7.4 hours in December to
about 16.9 hours in June. Write a wave for it. Number the months from 1
(January) to 12 (December).

<details class="dl-answer"><summary>answer</summary>

Middle $= 12.15$, amplitude $= 4.75$, period $= 12$ months, and the peak
is at month 6 (June).

$$\text{daylight}(m) = 4.75\sin\left(\frac{2\pi(m - 3)}{12}\right) + 12.15$$

The shift of 3 puts the maximum at month 6, because a sine wave peaks a
quarter of a period after its shift.

(The tutorial used days, and a period of 365. Months make the numbers
smaller, and the shape is the same.)

</details>

**14.** The peak is in June, month 6. So why is the shift 3, and not 6?

<details class="dl-answer"><summary>answer</summary>

A plain sine wave starts at the middle and rises. It reaches its peak a
quarter of a period later. With a period of 12, the peak comes 3 months
after the shift.

A cosine wave starts at its peak, so using cosine would avoid this
arithmetic. That is a good reason to keep both in mind.

</details>

## Tangent

**15.** Tangent's shape is different from sine's in two ways. What are
they?

<details class="dl-answer"><summary>answer</summary>

First, tangent has no maximum or minimum: it grows without limit. Second,
it repeats twice as often. Its period is half a turn, not a whole turn.

</details>

**16.** Where does tangent have no value, and why?

<details class="dl-answer"><summary>answer</summary>

At 90°, at 270°, and at every 180° from there. At those angles the point
on the circle is straight up or straight down. So the across value is
zero, and tangent is up divided by across.

In the picture, this is the vertical line that has no slope. It is the
same fact as in
[Straight lines: slope, and the line that breaks the formula](tutorial:slope-and-lines).
This is the third time we meet it.

</details>

## One longer one

**17.** A Ferris wheel (a big wheel at a fair) has a radius of 20 m. Its
centre is 22 m above the ground, and it takes 4 minutes to go round once.

- (a) You start at the bottom. Write your height above the ground as a
  function of time.
- (b) How high are you after 1 minute? After 3 minutes?
- (c) For how much of each turn are you more than 30 m up?

<details class="dl-answer"><summary>answer</summary>

(a) Starting at the bottom means starting at the minimum. A negative
cosine does that:

$$h(t) = -20\cos\left(\frac{2\pi t}{4}\right) + 22$$

(b) After 1 minute you are a quarter of the way round, at the same height
as the centre: 22 m. After 3 minutes you are three quarters of the way
round. That is also 22 m, on the other side.

(c) Solve $-20\cos\left(\frac{2\pi t}{4}\right) + 22 = 30$. This gives
$\cos\left(\frac{2\pi t}{4}\right) = -0.4$. So
$\frac{2\pi t}{4} \approx 1.982$ or $2\pi - 1.982 \approx 4.301$, which
gives $t \approx 1.26$ and $t \approx 2.74$. You are above 30 m for about
1.48 minutes of every 4, a bit over a third of the ride.

</details>

**18.** Two sound waves are $\sin x$ and $\sin(x + \pi)$. Plot their sum.
What happens? What is it called?

<details class="dl-answer"><summary>answer</summary>

They cancel completely: the sum is zero everywhere.

A shift of $\pi$ is half a period. So wherever one wave is up, the other
is exactly as far down. This is called destructive interference.
Noise-cancelling headphones work this way. They make the opposite wave.

</details>

## Your world

**19.** A problem from the world you chose.

<div class="dl-world" data-world="sea-and-sky">

The tide rises and falls twice a day, but its *range*, from low to high,
changes too. The cell finds the range on each day of March 2026 at
Dublin Port. The numbers come from the copy of the file saved on
{{snapshot: dublin-tides}}. Can you draw the ranges, and find how many
days apart the biggest ranges are?

```python exec
id: your-world-1--sea-and-sky
tides = await load_csv("dublin-tides.csv")
levels = tides["level_m"].tolist()

ranges = []
for day in range(31):
    one_day = levels[day * 24:(day + 1) * 24]
    ranges.append(max(one_day) - min(one_day))

print([round(r, 2) for r in ranges])
```

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Yours may be different and work too.

```python
fig, ax = plt.subplots(figsize=(8, 3.5))
ax.plot(range(31), ranges, "o-")
ax.set_xlabel("day of March (0 = 1 March)")
```

The biggest ranges are about 3.9 m, on 5 March and 20 March, 15 days
apart. The smallest, about 1.4 m, is on 13 March, between them. The
range is a slow wave, with a period of about 15 days. It comes from two
waves added together, as in "Two waves at once" on the tutorial page:
one wave from the Moon and one from the Sun. When they are in step, the
tides are biggest. These are *spring tides*, and they usually come a day
or two after a full Moon or a new Moon.

</details>

</div>

<div class="dl-world" data-world="sound">

Two guitar strings play notes of 440 Hz and 443 Hz. Added together,
they go in and out of step, and you hear the sound grow loud and quiet:
*beats*. Can you draw one second of the sum? How many beats are there in
the second? Can you write `beats(first, second)`, the number of beats
each second for any two notes?

```python exec
id: your-world-1--sound
first = wave(period=1 / 440)
second = wave(period=1 / 443)
seconds = [i / 20000 for i in range(20001)]
# Your code here.
```

```hint
Draw `first(s) + second(s)` against `seconds`, and count the places where
the sum shrinks to nothing. How does that count compare with the two
frequencies?
```

```inputs
beats(440, 443)
beats(440, 437)
beats(440, 440)
```

```solution
def beats(first, second):
    return abs(first - second)


fig, ax = plt.subplots(figsize=(8, 3.5))
ax.plot(seconds, [first(s) + second(s) for s in seconds], linewidth=0.5)
ax.set_xlabel("seconds")
---
There are 3 beats in the second, the difference between 443 and 440.
With the same two notes there are no beats at all. A guitarist tunes
two strings by turning one until the beats slow down and stop.
```

</div>

<div class="dl-world" data-world="planets-and-moons">

Reykjavik is far north of Dublin. The cell loads its daylight for 2026.
Can you fit a wave to it, as the tutorial did for Dublin, and measure
the gap? Keep the gap, in minutes, as `reykjavik_gap`. Is it bigger or
smaller than Dublin's 10 minutes? Where on the picture is the wave
furthest from the data?

```python exec
id: your-world-1--planets-and-moons
table = await load_csv("daylight.csv")
hours = table[table.place == "Reykjavik"]["daylight_hours"].tolist()
days = list(range(len(hours)))
print("longest:", max(hours), "on day", hours.index(max(hours)))
print("shortest:", min(hours), "on day", hours.index(min(hours)))


def gap_to_data(curve, xs, ys):
    """The average distance between a curve and some measured points."""
    total = 0
    for i in range(len(xs)):
        total += abs(curve(xs[i]) - ys[i])
    return total / len(xs)
```

```hint
The midline is halfway between the longest and shortest days. The shift
is a quarter of a year before the longest day.
```

```inputs
round(reykjavik_gap)
```

```solution
reykjavik = wave(amplitude=8.505, period=365, shift=77.75, lift=12.625)
reykjavik_gap = gap_to_data(reykjavik, days, hours) * 60
print(reykjavik_gap, "minutes")
---
Read from the data, the wave has an amplitude of about 8.5 hours, a
midline of about 12.6, and a shift of about day 78. The gap is about 38
minutes, nearly four times Dublin's. Reykjavik's daylight changes very
fast in spring and autumn, and stays near its longest and shortest for
weeks, so it is further from a sine wave. The further a place is from
the equator, the bigger the swing, and the less it looks like a sine.
```

</div>

<div class="dl-world" data-world="fantasy-maps">

The mill's water wheel has a radius of 3 m, and its centre is 1 m above
the river. A bucket on the rim is under water whenever its height is
below 0. For what fraction of each turn is a bucket under water? Can you
find it by trying 1000 places round the wheel?

```python exec
id: your-world-1--fantasy-maps
radius = 3        # metres
centre = 1        # metres above the water
bucket = wave(amplitude=radius, period=1, lift=centre)
# Your code here.
```

```hint
Try `bucket(k / 1000)` for each `k` from 0 to 999, and count the
heights below 0. What fraction of 1000 is that?
```

```inputs
round(underwater, 2)
```

```solution
count = 0
for k in range(1000):
    if bucket(k / 1000) < 0:
        count += 1
underwater = count / 1000
print(underwater)
---
A bucket is under water for about 0.39 of each turn, a little under
two fifths. The bottom of the wheel is 2 m below the surface, so a
bucket goes under well before the lowest point, and comes out well
after it.
```

</div>

## From earlier

**20.** From [Number types, powers and logarithms](tutorial:numbers-and-their-families).
The tutorial's E was 660 Hz, exactly $\frac{3}{2}$ of the A at 440 Hz.
A piano's E is 7 semitones above the A: $440 \times 2^{7/12}$ Hz. How
far apart are the two Es, in Hz? How many beats a second would you hear
if both played at once?

<details class="dl-answer"><summary>answer</summary>

$440 \times 2^{7/12} \approx 659.26$ Hz, about 0.74 Hz below 660. So
you would hear about 0.74 beats a second, one every 1.3 seconds or so.
A piano tuned this way is very slightly out of step with a pure fifth,
so that every key works equally well.

</details>

**21.** From
[Solving equations: linear, quadratic and simultaneous](tutorial:cracking-equations)
and [The unit circle: sine, cosine and tangent](tutorial:the-unit-circle).
For which angles between 0° and 360° is $2\sin\theta + 1 = 0$?

<details class="dl-hint"><summary>hint</summary>

Balance it first, as you would a linear equation, to get $\sin\theta$
on its own. Then where on the unit circle is the up value that number?

</details>

<details class="dl-answer"><summary>one way through it</summary>

Subtract 1 and divide by 2: $\sin\theta = -\frac{1}{2}$. The up value
is $-\frac{1}{2}$ in the bottom half of the circle, 30° past a half
turn and 30° short of a full turn. So $\theta = 210°$ or $\theta = 330°$.
Check: `2 * math.sin(math.radians(210)) + 1` prints a number very close
to 0.

</details>
