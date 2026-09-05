---
title: "Sine and Cosine Waves — Practice"
slug: sine-and-cosine-waves-practice
practice_for: sine-and-cosine-waves
module: mit-pdp-maths-prog-integration
module_title: "Programming and Maths, Integrated"
year: "2026-2027"
series: trigonometry-and-calculus
version: 2026.08.23.1
---

# Sine and Cosine Waves — Practice

Answers are folded. Several of these are about reading a picture, so plot first and check afterwards.

## Tools

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

## Reading the Four Numbers

**1.** For `y = 3 sin(x)`, what are the highest and lowest values?

<details class="dl-answer"><summary>answer</summary>

3 and −3. The amplitude is how far it swings *from the middle*, so the total height from top to bottom is 6.

That distinction catches people: an amplitude of 3 does not mean a range of 3.

</details>

**2.** For `y = sin(x) + 5`, what are the highest and lowest values, and where is the middle?

<details class="dl-answer"><summary>answer</summary>

6 and 4, with the middle at 5. The lift moves the whole thing up without changing how far it swings.

</details>

**3.** A wave has a maximum of 11 and a minimum of 3. What are its amplitude and its lift?

<details class="dl-answer"><summary>answer</summary>

The middle is (11 + 3)/2 = 7, so the lift is 7. The swing is (11 − 3)/2 = 4, so the amplitude is 4.

Half the sum and half the difference — that pair is how you read any wave off its extremes.

</details>

**4.** Which of these repeats fastest?

- (a) `sin(x)` with period 1 turn
- (b) `sin(x)` with period 0.25 turns
- (c) `sin(x)` with period 4 turns

<details class="dl-answer"><summary>answer</summary>

(b). A shorter period means more repeats in the same distance.

The word is slightly counterintuitive — a *smaller* period is a *faster* wave — which is why frequency, its reciprocal, is often used instead.

</details>

**5.** A wave completes 50 cycles per second. What is its period?

<details class="dl-answer"><summary>answer</summary>

1/50 = 0.02 seconds.

Fifty cycles per second is mains electricity in Ireland, and 0.02 s is how long one full cycle of the voltage takes.

</details>

## Periodicity

**6.** Without computing: what is `sin(10π)`? And `cos(4π)`?

<details class="dl-answer"><summary>answer</summary>

0 and 1.

10π is five full turns, which brings you back to the start, where the up value is 0. 4π is two full turns, where the across value is 1.

</details>

**7.** `sin(θ) = 0.6`. Give two values of θ between 0 and 360° that satisfy it.

<details class="dl-answer"><summary>answer</summary>

About 36.87° and about 143.13°.

Every height between 0 and 1 is reached twice on the way up and over, and the second is 180 minus the first. That is the fact behind the ambiguous case of the Sine Rule.

</details>

**8.** `cos(θ) = 0.6`. Give two values of θ between 0 and 360°.

<details class="dl-answer"><summary>answer</summary>

About 53.13° and about 306.87°.

Cosine's second solution is 360 minus the first, not 180 minus — because cosine is symmetric about the horizontal axis rather than the vertical one.

</details>

**9.** Why must a sine wave repeat?

<details class="dl-answer"><summary>answer</summary>

Because it is a point going round a circle, drawn against how far it has gone. After a full turn the point is back where it started, so its height is what it was, so the curve must do the same thing again.

The repetition is not a property the curve happens to have; it is what circling looks like drawn flat.

</details>

## Fitting

**10.** Sketch `y = 2 sin(x) + 1` by hand — where is the middle, the top, the bottom — then plot it and compare.

<details class="dl-answer"><summary>answer</summary>

Middle at 1, top at 3, bottom at −1, one full cycle per turn, starting at the middle and going up.

```python
draw(wave(amplitude=2, lift=1), label="2 sin(x) + 1")
```

</details>

**11.** The tide in a harbour is 5.2 m at high tide and 1.4 m at low tide, with high tides about 12.4 hours apart. Write a wave for the depth.

<details class="dl-answer"><summary>answer</summary>

Middle = (5.2 + 1.4)/2 = 3.3. Amplitude = (5.2 − 1.4)/2 = 1.9. Period = 12.4 hours.

`depth(t) = 1.9 sin(2π(t − shift)/12.4) + 3.3`, with the shift chosen so the peak lands at whatever time high tide actually is.

</details>

**12.** Using that model, at what depth is the harbour six hours after high tide?

<details class="dl-answer"><summary>answer</summary>

Six hours is just under half a period (6.2 hours), so it is near low tide. Plugging in gives about 1.42 m — very slightly above the minimum.

Half a period after a peak is exactly the trough, and six hours is a little short of that.

</details>

**13.** Daylight in Dublin runs from about 7.4 hours in December to about 16.9 in June. Write a wave for it, in months.

<details class="dl-answer"><summary>answer</summary>

Middle = 12.15, amplitude = 4.75, period = 12 months, peaking around month 6.

`daylight(m) = 4.75 sin(2π(m − 3)/12) + 12.15`, where the shift of 3 puts the maximum at month 6, because a sine peaks a quarter of a period after its shift.

</details>

**14.** Why is the shift 3 rather than 6, if the peak is in June?

<details class="dl-answer"><summary>answer</summary>

Because a plain sine wave starts at the middle and rises, reaching its peak a quarter of a period later. With a period of 12, the peak is 3 months after the shift.

Using a cosine instead would avoid the arithmetic — cosine starts at its peak — which is a good reason to keep both in mind.

</details>

## Tangent

**15.** How is tangent's shape different from sine's, in two respects?

<details class="dl-answer"><summary>answer</summary>

It has no maximum or minimum — it runs away to infinity. And it repeats twice as often: its period is half a turn, not a whole one.

</details>

**16.** Where does tangent have no value, and why?

<details class="dl-answer"><summary>answer</summary>

At 90°, 270°, and every 180° from there. At those angles the point on the circle is straight up or straight down, so the across value is zero, and tangent is up divided by across.

Geometrically it is the vertical line that has no slope — the same fact as in *Lines and Distances*, met for the third time.

</details>

## One Longer One

**17.** A Ferris wheel has a radius of 20 m, its centre is 22 m above the ground, and it takes 4 minutes to go round.

- (a) Write your height above the ground as a function of time, starting at the bottom.
- (b) How high are you after 1 minute? After 3?
- (c) For how much of each turn are you more than 30 m up?

<details class="dl-answer"><summary>answer</summary>

(a) Starting at the bottom means starting at the minimum, which a negative cosine does: `h(t) = −20 cos(2πt/4) + 22`.

(b) After 1 minute you are a quarter of the way round, at the height of the centre: 22 m. After 3 minutes you are three quarters round, also 22 m — the other side.

(c) Solve `−20 cos(2πt/4) + 22 = 30`, giving `cos(2πt/4) = −0.4`, so `2πt/4 ≈ ±1.982`, so `t ≈ 1.26` and `t ≈ 2.74`. You are above 30 m for about 1.48 minutes of each 4 — a bit over a third of the ride.

</details>

**18.** Two sound waves are `sin(x)` and `sin(x + π)`. Plot their sum. What happens, and what is that called?

<details class="dl-answer"><summary>answer</summary>

They cancel completely — the sum is flat zero.

A shift of π is half a period, so wherever one is up the other is exactly as far down. This is destructive interference, and it is how noise-cancelling headphones work: they generate the opposite wave.

</details>
