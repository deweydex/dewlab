---
title: "The slope of a wave: how fast daylight and tides change — Practice"
practice_for: the-slope-of-a-wave
year: "2026-2027"
version: 2026.09.26.1
worlds:
  sea-and-sky: The tide at Dublin Port, falling.
  planets-and-moons: Daylight in Cape Town, in its spring and its autumn.
  fantasy-maps: The windmill beside the castle, and the tip of a sail. The numbers are made up.
---

# The slope of a wave: how fast daylight and tides change — Practice

Each answer is hidden until you open it. Write something down first,
even a guess, and then open the answer to compare.

## Tools

```python exec
id: tools-1
import math

def derivative_at(f, x, gap=1e-6):
    """The derivative, computed numerically."""
    return (f(x + gap) - f(x - gap)) / (2 * gap)


def wave(amplitude=1, period=1, shift=0, lift=0):
    def f(x):
        return amplitude * math.sin((x - shift) / period * 2 * math.pi) + lift
    return f


print(derivative_at(math.sin, 0))
```

## Slopes of sine and cosine

**1.** The cell asks for the slope of the cosine wave at 0.

```python exec
id: slopes-of-sine-and-cosine-1
print(derivative_at(math.cos, 0))
```

```predict
type: number
tolerance: 0.001

What will it print?
```

<details class="dl-answer"><summary>why</summary>

It prints 0.0. The slope of $\cos x$ is $-\sin x$, and $\sin 0 = 0$. The
cosine wave is at its top at 0, where it is flat for a moment.

</details>

**2.** What is the slope of the cosine wave at $\frac{\pi}{2}$? Say it
first, then check.

<details class="dl-answer"><summary>answer</summary>

$-\sin\frac{\pi}{2} = -1$. The cosine wave crosses its midline going
down there, as fast as it ever falls.

</details>

**3.** What is the slope of $\sin(2x)$ at 0? Use the chain rule, then
check with `derivative_at`.

<details class="dl-answer"><summary>answer</summary>

The inside is $2x$, with slope 2. The outside is $\sin$, with slope
$\cos$. So the slope is $2\cos(2x)$, which is 2 at 0. A wave that
repeats twice as often climbs twice as steeply.

</details>

**4.** What is the slope of $3\sin x + 5$? Where is it biggest?

<details class="dl-answer"><summary>answer</summary>

$3\cos x$. The 5 is a number on its own, so its slope is 0. The slope is
biggest, 3, where $\cos x = 1$: at 0, $2\pi$, and every whole turn,
where the wave crosses its midline going up.

</details>

**5.** A wave has an amplitude of 2 and a period of 10. What is the
fastest it ever changes? Check it with `derivative_at` on
`wave(amplitude=2, period=10)` at 0.

<details class="dl-answer"><summary>answer</summary>

$2 \times \frac{2\pi}{10} \approx 1.257$. It happens where the wave
crosses its midline, such as at 0.

</details>

## Your world

**6.** A problem from the world you chose.

<div class="dl-world" data-world="sea-and-sky">

The tide at Dublin Port fitted `wave(amplitude=1.5, period=12.42,
shift=6.75, lift=2.75)`, with the time in hours. When is it falling
fastest, and how fast?

```python exec
id: your-world-1--sea-and-sky
tide = wave(amplitude=1.5, period=12.42, shift=6.75, lift=2.75)
```

<details class="dl-answer"><summary>answer</summary>

A sine wave falls fastest where it crosses its midline going down, half
a period after its shift: $6.75 + 6.21 = 12.96$ hours after midnight.
`derivative_at(tide, 12.96)` is about $-0.76$: the water falls about
0.76 m an hour.

</details>

</div>

<div class="dl-world" data-world="planets-and-moons">

Cape Town's daylight fitted `wave(amplitude=2.27, period=365,
shift=257.75, lift=12.15)`, with the time in days. How fast are its days
changing on day 80, in March, and on day 258, in September, in minutes
a day?

```python exec
id: your-world-1--planets-and-moons
cape = wave(amplitude=2.27, period=365, shift=257.75, lift=12.15)
```

<details class="dl-answer"><summary>answer</summary>

`derivative_at(cape, 80) * 60` is about $-2.3$, and
`derivative_at(cape, 258) * 60` is about $+2.3$. In March, Cape Town's
days get shorter, because it is autumn there. In September they grow,
because it is spring. The rate is half of Dublin's, because Cape Town's
wave is about half as tall.

</details>

</div>

<div class="dl-world" data-world="fantasy-maps">

The windmill's sail tip has height `wave(amplitude=6, period=8,
lift=10)` metres, with the time in seconds. How fast does the tip rise
at its fastest? Where is the tip then?

```python exec
id: your-world-1--fantasy-maps
tip = wave(amplitude=6, period=8, lift=10)
```

<details class="dl-answer"><summary>answer</summary>

$6 \times \frac{2\pi}{8} \approx 4.71$ m a second, and
`derivative_at(tip, 0)` agrees. The tip rises fastest at 0 seconds,
when the sail points straight out sideways, level with the hub.

</details>

</div>

## From earlier

**7.** From [The unit circle: sine, cosine and tangent](tutorial:the-unit-circle).
What is the slope of $\tan x$ at 0? At $\frac{\pi}{4}$? What happens to
it near $\frac{\pi}{2}$?

<details class="dl-answer"><summary>answer</summary>

`derivative_at(math.tan, 0)` is 1, and at $\frac{\pi}{4}$ it is 2. Near
$\frac{\pi}{2}$ the slope grows without limit, as the tangent itself
does: the line from the origin is close to vertical there.

</details>

**8.** From
[Derivative rules: power, sum, product and chain, found by experiment](tutorial:derivative-rules).
What does the product rule give for the slope of $\sin x \cos x$ at 0?

<details class="dl-answer"><summary>one way through it</summary>

$\cos x \cdot \cos x + \sin x \cdot (-\sin x) = \cos^2 x - \sin^2 x$.
At 0 that is $1 - 0 = 1$, and
`derivative_at(lambda x: math.sin(x) * math.cos(x), 0)` agrees.

</details>
