---
title: "Sine and cosine waves: amplitude, period and shift — Practice"
practice_for: sine-and-cosine-waves
year: "2026-2027"
version: 2026.08.23.1
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

This catches many people: an amplitude of 3 does not mean a range of 3.

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
You can read any wave off its highest and lowest values this way.

</details>

**4.** Which of these repeats fastest?

- (a) a sine wave with period 1 turn
- (b) a sine wave with period 0.25 turns
- (c) a sine wave with period 4 turns

<details class="dl-answer"><summary>answer</summary>

(b). A shorter period means more repeats in the same distance.

This can feel backwards at first: a *smaller* period means a *faster*
wave. That is why people often use the *frequency* instead. The frequency
is the number of repeats in one unit of time, and it is 1 divided by the
period.

</details>

**5.** A wave completes 50 cycles per second. What is its period?

<details class="dl-answer"><summary>answer</summary>

$\frac{1}{50} = 0.02$ seconds.

Fifty cycles per second is the mains electricity in Ireland. So 0.02
seconds is how long one full cycle of the voltage takes.

</details>

## Periodicity

Problems 7 and 8 ask for an angle when you know its sine or cosine. For
that, Python has `math.asin` (the inverse sine) and `math.acos` (the
inverse cosine). Both give an answer in radians, so wrap them in
`math.degrees`. For example, `math.degrees(math.asin(0.5))` gives about
30.

**6.** What is $\sin(10\pi)$? What is $\cos(4\pi)$? Try to answer without
computing.

<details class="dl-answer"><summary>answer</summary>

0 and 1.

$10\pi$ is five full turns, which brings you back to the start, where
the up value is 0. $4\pi$ is two full turns, and there the across value
is 1.

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

The curve does not repeat by chance. Repeating is what going round in a
circle looks like when we draw it flat.

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
is near low tide. Putting the numbers in gives about 1.41 m, very
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

(The tutorial numbered the months from 0, so June was month 5 there.)

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
[Straight lines: slope, midpoint and distance](tutorial:lines-and-distances),
met for the third time.

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
Noise-cancelling headphones work this way: they make the opposite wave.

</details>
