---
title: "Derivatives: the rate of change of a curve"
year: "2026-2027"
version: 2026.09.26.1
covers:
  the-slope-of-something-that-is-not-straight:
    covers: [MIT-3.6]
  three-descriptions-of-one-number:
    covers: [MIT-3.6]
  the-derivative-as-a-function:
    covers: [MIT-3.6]
  derivatives-in-your-world:
    covers: [MIT-3.6]
worlds:
  sea-and-sky: A diver going down and coming back up. The numbers are made up.
  planets-and-moons: A rocket, climbing faster and faster. The numbers are made up.
  fantasy-maps: The road over a hill near the village. The numbers are made up.
---

# Derivatives: the rate of change of a curve

In [Straight lines: slope, and the line that breaks the formula](tutorial:slope-and-lines),
we described slope as a rate of change: **if $x$ goes up by one, what
happens to $y$?** For a straight line, the answer is one number, and it
is the same everywhere on the line.

Here is the curve $y = x^2$, with four points marked on it. How steep is
the curve at each point?

```python exec
id: the-slope-of-something-that-is-not-straight-1
import matplotlib.pyplot as plt

def curve(x):
    return x ** 2


fig, ax = plt.subplots(figsize=(7, 4.5))
xs = [x / 50 for x in range(-150, 151)]
ax.plot(xs, [curve(x) for x in xs], linewidth=2)
for point in [-2, -0.5, 1, 2.5]:
    ax.plot([point], [curve(point)], "o", markersize=8)
ax.axhline(0, color="black", linewidth=0.8)
ax.axvline(0, color="black", linewidth=0.8)
ax.grid(alpha=0.3)
ax.set_ylim(-1, 9)
ax.set_title("Steep in different amounts at different places")
```

From left to right, the curve at the marked points is steeply downhill,
gently downhill, gently uphill, and steeply uphill. The curve has no
single slope. On this page we find the slope at a single point, and
then at every point. The tool we need is the limit, from
[Limits: getting closer without arriving](tutorial:approaching-a-limit).

## The slope of something that is not straight

At each point there is a *local* slope: how steep the curve is right
there. We use the same method as for the falling ball on the limits
page. A *chord* is a straight line that joins two points on a curve. We
take two points on the curve, close together, and find the slope of the
chord between them. Then we bring the points closer.

The function `slope_between` does this. It finds the slope of the chord
from $x$ to $x + \text{gap}$:

$$\frac{f(x + \text{gap}) - f(x)}{\text{gap}}$$

For example, with $x = 3$ and a gap of 1, that is
$\dfrac{4^2 - 3^2}{1} = \dfrac{16 - 9}{1} = 7$. What do you think
happens as the gap gets smaller?

```python exec
id: the-slope-of-something-that-is-not-straight-2
def slope_between(f, x, gap):
    """The slope of the straight line joining two nearby points on f."""
    return (f(x + gap) - f(x)) / gap


print("Getting the slope of x^2 at x = 3:")
for gap in [1, 0.5, 0.1, 0.01, 0.001, 0.0001]:
    print(f"   gap {gap:<8} : {slope_between(curve, 3, gap)}")
```

The slopes move towards 6, and never arrive, because the gap can never be
zero.

Here are the chords, one after another, as the second point slides
towards the first. Watch the line turn.

```python exec
id: the-slope-of-something-that-is-not-straight-3
from matplotlib.animation import FuncAnimation

gaps = [2 * 0.85 ** k for k in range(24)]

figure, ax = plt.subplots(figsize=(5.5, 3.6))
xs = [x / 50 for x in range(0, 251)]
ax.plot(xs, [curve(x) for x in xs], linewidth=2, color="tab:blue")
ax.plot([1.5, 5], [9 + 6 * (x - 3) for x in [1.5, 5]], color="tab:red",
        linewidth=1, label="the line the chords turn towards")
chord, = ax.plot([], [], color="tab:orange")
ends, = ax.plot([], [], "o", color="tab:orange")
ax.set_xlim(0, 5)
ax.set_ylim(0, 25)
ax.legend(loc="upper left", fontsize=8)


def draw_step(k):
    gap = gaps[k]
    m = slope_between(curve, 3, gap)
    chord.set_data([1.5, 5], [curve(3) + m * (x - 3) for x in [1.5, 5]])
    ends.set_data([3, 3 + gap], [curve(3), curve(3 + gap)])
    ax.set_title(f"gap {gap:.3f}: slope {m:.3f}")


FuncAnimation(figure, draw_step, frames=24, interval=150)
```

Each orange line goes through two points on the curve. As the second
point slides towards the first, the line turns, and it turns towards
the red line. The red line touches the curve at $x = 3$ and has the same
steepness as the curve there.

**The limit of the chord's slope, as the gap shrinks to nothing, is the
slope of the curve at that point.** The *derivative* of a function at a
point is this limit. Here, the derivative of $x^2$ at $x = 3$ is 6.

The *tangent line* at a point is the straight line that touches the
curve at that point and has the same steepness as the curve there. Its
slope is the derivative. (This "tangent" is a line. It is a different
thing from the tangent ratio, $\tan$, in
[The unit circle: sine, cosine and tangent](tutorial:the-unit-circle),
although the two share a name.)

## Three descriptions of one number

Here are three ideas that look like three separate topics. They all
describe the same number.

| Description | What it means |
|---|---|
| **A limit** | The value that $\dfrac{f(x + \text{gap}) - f(x)}{\text{gap}}$ moves towards as the gap shrinks. This is the definition of the derivative. |
| **The slope of a tangent line** | The steepness of the straight line that touches the curve at that point. |
| **A rate of change** | How fast the output is changing for each unit of input, right at that point. |

The next cell defines `derivative_at`, which computes the derivative
with numbers. It uses one point on each side of $x$, a little way
before and a little way after, and a gap of `1e-6`. One point on each
side gives a more accurate answer than a chord on one side only. The
gap is near the bottom of the V from
[the limits page](tutorial:approaching-a-limit#how-small-should-the-gap-be),
for this way of measuring.

```python exec
id: three-descriptions-of-one-number-1
def derivative_at(f, x, gap=1e-6):
    """The derivative, computed numerically. Good enough to see with."""
    return (f(x + gap) - f(x - gap)) / (2 * gap)


for x in [-0.5, 0, 1, 3, -2]:
    print(f"slope of x^2 at x = {x:>4} is {derivative_at(curve, x):>8.4f}")
```

```predict
type: number
tolerance: 0.01

The slope at 3 is 6. What will the last line print, for $x = -2$?
```

Compare each answer with the $x$ value beside it. What do you notice?

Each slope is double the $x$. **The derivative of $x^2$ is $2x$.** So
the derivative is a function, and not a single number. It tells us the
slope wherever we ask. For example, at $x = 5$ the slope is
$2 \times 5 = 10$. At $x = -2$ it is $-4$: the curve goes downhill
there, so the slope is negative.

We write $f'$, said "f prime", for the derivative of $f$. So if
$f(x) = x^2$, then $f'(x) = 2x$. To *differentiate* a function means to
find its derivative.

The "rate of change" description needs no graph. The falling ball on
the limits page fell $4.9t^2$ metres after $t$ seconds. Its speed is the
rate of change of that distance, so its speed is the derivative:

```python exec
id: three-descriptions-of-one-number-2
def fallen(t):
    return 4.9 * t ** 2


for t in [0, 1, 2, 3]:
    print(f"at t = {t}s the ball has fallen {fallen(t):>6.1f} m "
          f"and is travelling at {derivative_at(fallen, t):>5.2f} m/s")
```

The first column is distance, and the second is speed. The
relationship is the same as between a curve and its slope, and no axes
are needed.

## The derivative as a function

Let's plot the slope underneath the curve it comes from. Then we can
read the two together.

```python exec
id: the-derivative-as-a-function-1
fig, (top, bottom) = plt.subplots(2, 1, figsize=(7, 6), sharex=True)

xs = [x / 50 for x in range(-150, 151)]
top.plot(xs, [curve(x) for x in xs], linewidth=2)
top.set_ylabel("x^2")
top.grid(alpha=0.3)
top.axhline(0, color="black", linewidth=0.8)

bottom.plot(xs, [derivative_at(curve, x) for x in xs], linewidth=2, color="tab:orange")
bottom.set_ylabel("its slope")
bottom.set_xlabel("x")
bottom.grid(alpha=0.3)
bottom.axhline(0, color="black", linewidth=0.8)
top.set_title("A curve, and how steep it is")
```

Read the two graphs together:

- Where the top curve goes downhill, the bottom graph is negative.
- Where the top curve is flat, at its lowest point, the bottom graph
  crosses zero.
- Where the top curve climbs steeply, the bottom graph is large.

**At a turning point, the curve is flat for a moment, so the derivative
is zero there.** This connects back to
[Parabolas: completing the square](tutorial:parabolas): the vertex of a
parabola is the point where the slope is zero.

(The opposite is not always true. A zero slope tells you where to *look*
for a turning point. The curve $x^3$ is flat for a moment at $x = 0$, but
it keeps climbing on both sides, so that point is not a turning point.)

Completing the square writes $x^2 - 4x + 1$ as $(x - 2)^2 - 3$, so its
vertex is at $x = 2$. What should the slope be there?

```python exec
id: the-derivative-as-a-function-2
def quadratic(x):
    return x ** 2 - 4 * x + 1


for x in [0, 1, 2, 3, 4]:
    print(f"slope at x = {x}: {derivative_at(quadratic, x):>7.4f}")
```

The slope is zero at 2, where completing the square put the vertex.
**Two different methods give the same answer.** When that happens, each one
checks the other.

### Your turn

Where does a curve turn? We can let Python look for us. Between two
points where the slope has different signs, it must pass through zero.
Can you write `turning_points(f, low, high)`? It tries 1000 small steps
from `low` to `high`, and returns the middle of each step where the
slope changes sign, rounded to one decimal place. Try it on
$2x^3 - 3x^2 - 12x + 1$.

```python exec
id: the-derivative-as-a-function-3
def cubic(x):
    return 2 * x ** 3 - 3 * x ** 2 - 12 * x + 1


def turning_points(f, low, high, steps=1000):
    """Where the slope of f changes sign, between low and high."""
    # Your code here.
```

```hint
The width of one step is `(high - low) / steps`. For each step, find the
slope at its left end and at its right end. When one is below zero and
the other is not, the slope has changed sign inside the step.
```

```hint
after: 3 errors
title: The shape of it

    found = []
    width = (high - low) / steps
    for i in range(steps):
        left = derivative_at(f, low + i * width)
        right = ...
        if ...:
            found.append(round(low + (i + 0.5) * width, 1))
    return found

What should happen when a slope is exactly zero at the end of a step?
It is best to count it once, not twice.
```

```inputs
turning_points(cubic, -3, 3)
turning_points(quadratic, 0, 5)
turning_points(lambda x: x ** 3, -3, 3)     # flat at 0, but not a turn
```

```solution
def turning_points(f, low, high, steps=1000):
    """Where the slope of f changes sign, between low and high."""
    found = []
    width = (high - low) / steps
    for i in range(steps):
        left = derivative_at(f, low + i * width)
        right = derivative_at(f, low + (i + 1) * width)
        if left < 0 <= right or left > 0 >= right:
            found.append(round(low + (i + 0.5) * width, 1))
    return found
---
The cubic turns at $x = -1$ and at $x = 2$. `left < 0 <= right` counts a
step where the slope goes from negative to zero or positive, and the
other test counts the opposite. A slope of exactly 0 at the end of one
step is counted in that step, and not again in the next. $x^3$ has no
turning points: its slope is never negative, so it never changes sign.
```

## Derivatives in your world

<div class="dl-world" data-world="sea-and-sky">

A diver goes down and comes back up. Her depth is $6t - 0.3t^2$ metres,
$t$ minutes after she leaves the surface. How fast is she going down
after 4 minutes? When is she deepest, and how deep is that? Use
`derivative_at` and `turning_points`.

```python exec
id: derivatives-in-your-world-1--sea-and-sky
def depth(t):
    return 6 * t - 0.3 * t ** 2
```

```hint
"How fast" is the derivative. "Deepest" is a turning point: where the
depth stops growing and starts to shrink.
```

```inputs
round(derivative_at(depth, 4), 2)
turning_points(depth, 0, 20)
```

```solution
def turning_points(f, low, high, steps=1000):
    found = []
    width = (high - low) / steps
    for i in range(steps):
        left = derivative_at(f, low + i * width)
        right = derivative_at(f, low + (i + 1) * width)
        if left < 0 <= right or left > 0 >= right:
            found.append(round(low + (i + 0.5) * width, 1))
    return found


print("going down at", derivative_at(depth, 4), "m a minute")
deepest = turning_points(depth, 0, 20)[0]
print("deepest at", deepest, "minutes:", depth(deepest), "m")
---
`turning_points` is your function from earlier on the page. After 4
minutes she is going down at 3.6 metres a minute. She is
deepest after 10 minutes, at 30 m, where her rate of going down is 0.
After that, the rate is negative: she is coming back up.
```

</div>

<div class="dl-world" data-world="planets-and-moons">

A rocket's height is $5t^2 + 0.1t^3$ metres, $t$ seconds after launch.
How fast is it climbing after 10 seconds? After 20? Can you draw its
speed for the first 30 seconds, under its height?

```python exec
id: derivatives-in-your-world-1--planets-and-moons
def height(t):
    return 5 * t ** 2 + 0.1 * t ** 3
```

```hint
The speed is the derivative of the height. For the drawing, use two
axes, as the cell with `top` and `bottom` did.
```

```inputs
round(derivative_at(height, 10), 2)
round(derivative_at(height, 20), 2)
```

```solution
print(derivative_at(height, 10), derivative_at(height, 20))

times = [t / 10 for t in range(301)]
fig, (up, fast) = plt.subplots(2, 1, figsize=(7, 5), sharex=True)
up.plot(times, [height(t) for t in times])
up.set_ylabel("height (m)")
fast.plot(times, [derivative_at(height, t) for t in times], color="tab:orange")
fast.set_ylabel("speed (m/s)")
fast.set_xlabel("seconds")
---
After 10 seconds it climbs at 130 m/s, and after 20 seconds at 320 m/s.
The speed grows faster and faster, so its graph curves upwards too.
```

</div>

<div class="dl-world" data-world="fantasy-maps">

The road from the village goes over a hill. The road's height is
$40 + 12x - 3x^2$ metres, $x$ km from the village. How steep is the road
where it leaves the village, in metres of climb for each kilometre?
Where is the top of the hill, and how high is it?

```python exec
id: derivatives-in-your-world-1--fantasy-maps
def road(x):
    return 40 + 12 * x - 3 * x ** 2
```

```hint
The steepness is the derivative. The top of the hill is a turning
point.
```

```inputs
round(derivative_at(road, 0), 2)
turning_points(road, 0, 4)
```

```solution
def turning_points(f, low, high, steps=1000):
    found = []
    width = (high - low) / steps
    for i in range(steps):
        left = derivative_at(f, low + i * width)
        right = derivative_at(f, low + (i + 1) * width)
        if left < 0 <= right or left > 0 >= right:
            found.append(round(low + (i + 0.5) * width, 1))
    return found


print("steepness at the village:", derivative_at(road, 0))
top = turning_points(road, 0, 4)[0]
print("the top is", top, "km out, at", road(top), "m")
---
`turning_points` is your function from earlier on the page. The road
climbs 12 m for each kilometre as it leaves the village. The
top is 2 km out, at 52 m. After that the slope is negative, and the
road goes down.
```

</div>

## Looking back

A derivative is the slope of a curve at a single point. It is a limit,
the slope of a tangent line, and a rate of change: three descriptions
of one number. The derivative of a function is a function, and where it
is zero, the curve may turn.

Pick something that changes over time: a bank balance, a temperature, a
download. In a few sentences, what would its derivative be, in words,
and what units would it have?

A challenge: `turning_points` says where a curve turns, but not whether
it is a top or a bottom. Can you make it say which? What does the slope
do on each side of a top?

```python challenge
def derivative_at(f, x, gap=1e-6):
    return (f(x + gap) - f(x - gap)) / (2 * gap)


def tops_and_bottoms(f, low, high, steps=1000):
    """Each turning point, and whether it is a top or a bottom."""
    # Your code here.


print(tops_and_bottoms(lambda x: 2 * x ** 3 - 3 * x ** 2 - 12 * x + 1, -3, 3))
```

Every slope on this page came from a limit.
[Derivative rules: found by experiment](tutorial:derivative-rules)
finds patterns in the answers, so that we can write down a derivative
without computing one.

## Where to read more

Grant Sanderson (3Blue1Brown) (2017). *Essence of Calculus, Chapter 2: The
Paradox of the Derivative.* <https://www.youtube.com/watch?v=9vKqVkMQHKk>.
This video draws the same picture as this page, with chords moving
towards a tangent. It also explains why "instantaneous rate of change"
is a stranger idea than it sounds.

3Blue1Brown (2018). *The other way to visualize derivatives: Chapter 12,
Essence of calculus.* <https://www.youtube.com/watch?v=CfW845LNObM>. This
video draws a derivative as how much a function stretches or squashes the
numbers near a point, rather than as a slope. It is about fourteen
minutes long.
