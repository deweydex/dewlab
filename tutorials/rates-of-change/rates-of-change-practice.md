---
title: "Derivatives: the rate of change of a curve — Practice"
practice_for: rates-of-change
year: "2026-2027"
version: 2026.09.26.1
worlds:
  sea-and-sky: A kite surfer, jumping off a wave. The numbers are made up.
  planets-and-moons: A lander coming down to the ground. The numbers are made up.
  fantasy-maps: A dragon, swooping up and down. The numbers are made up.
---

# Derivatives: the rate of change of a curve — Practice

Each answer is hidden until you open it. Write something down first,
even a guess, and then open the answer to compare. The rules for
derivatives come on the next page, so these problems use numbers.

## Tools

```python exec
id: tools-1
def slope_between(f, x, gap):
    """The slope of the straight line joining two nearby points on f."""
    return (f(x + gap) - f(x)) / gap


def derivative_at(f, x, gap=1e-6):
    """The derivative, computed numerically."""
    return (f(x + gap) - f(x - gap)) / (2 * gap)


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


print(derivative_at(lambda x: x ** 2, 3))
```

## Chords and slopes

**1.** The cell finds the slope of two chords on $x^2$, both starting
at $x = 3$.

```python exec
id: chords-and-slopes-1
square = lambda x: x ** 2
print(slope_between(square, 3, 0.5))
print(slope_between(square, 3, 0.25))
```

```predict
type: number
tolerance: 0.001

The first line prints 6.5. What will the second line print?
```

<details class="dl-answer"><summary>why</summary>

It prints 6.25. For $x^2$ at 3, the chord's slope is always
$6 + \text{gap}$. Can you see why in problem 2?

</details>

**2.** Why is the slope of the chord on $x^2$, from 3 to $3 + h$, always
$6 + h$?

<details class="dl-answer"><summary>one way through it</summary>

$\dfrac{(3 + h)^2 - 9}{h} = \dfrac{9 + 6h + h^2 - 9}{h} = \dfrac{6h + h^2}{h} = 6 + h$.
As $h$ shrinks, $6 + h$ moves towards 6, the slope at 3.

</details>

**3.** The absolute value, `abs(x)`, makes a V shape with a sharp corner
at 0. What does `derivative_at` say its slope is at 0?

```python exec
id: chords-and-slopes-2
print(derivative_at(abs, 0))
print(slope_between(abs, 0, 0.001), slope_between(abs, 0, -0.001))
```

<details class="dl-answer"><summary>answer</summary>

`derivative_at` prints 0.0. But the chords say otherwise: from the right
their slope is 1, and from the left it is $-1$. The two sides do not
agree, so there is no limit, and `abs` has no derivative at 0.
`derivative_at` averages the two sides, and hides the corner. A number
from a computer needs the same care as a limit: look from both sides.

</details>

**4.** A runner's distance from the start is measured every second, in
metres. Can you write `speeds(distances)`, which returns her speed over
each second? When was she speeding up?

```python exec
id: chords-and-slopes-3
distances = [0, 2, 6, 12, 20, 30, 40, 50]


def speeds(distances):
    """The speed over each second, from distances measured every second."""
    # Your code here.
```

```hint
Her speed over one second is how far she went in that second. Which two
numbers in the list tell you that?
```

```inputs
speeds(distances)
speeds([0, 5, 10, 15])
```

```solution
def speeds(distances):
    """The speed over each second, from distances measured every second."""
    return [distances[i + 1] - distances[i] for i in range(len(distances) - 1)]
---
Her speeds are 2, 4, 6, 8 and 10 m/s for the first five seconds, then
10, 10: she sped up for five seconds, then kept a steady 10 m/s. Each
speed is a chord's slope, with a gap of one second.
```

## Turning points

**5.** Where does $x^3 - 3x$ turn? Is each turning point a top or a
bottom?

<details class="dl-answer"><summary>answer</summary>

`turning_points(lambda x: x ** 3 - 3 * x, -3, 3)` gives `[-1.0, 1.0]`.
At $-1$ the slope goes from positive to negative, so it is a top, with
height 2. At 1 it goes from negative to positive, so it is a bottom,
with height $-2$.

</details>

**6.** Where does $x^4 - 8x^2$ turn? Draw it.

<details class="dl-answer"><summary>answer</summary>

It turns at $-2$, 0 and 2. `turning_points` may print the middle one as
`-0.0`, which is 0. The curve is a W: two bottoms, at a height of $-16$,
with a top at 0 between them.

</details>

**7.** A curve has a slope of zero at some point. Must that point be a
top or a bottom?

<details class="dl-answer"><summary>answer</summary>

No. $x^3$ has a slope of zero at $x = 0$, but the curve keeps going up
through that point without turning. It is flat for an instant, and then
it continues. A point like that is called a *point of inflection*. So a
zero slope tells you where to look, and you still need to check which
way the slope goes on each side.

</details>

**8.** Distance is in metres and time in seconds. What are the units of
the derivative of distance? What are the units of the derivative of
*that*?

<details class="dl-answer"><summary>answer</summary>

Metres per second, which is speed. Then metres per second per second,
which is acceleration. A derivative divides a change in the output by a
change in the input, so its units are output units per input unit.

</details>

## Your world

**9.** A problem from the world you chose.

<div class="dl-world" data-world="sea-and-sky">

A kite surfer jumps off a wave. Her height is $3t - t^2$ metres, $t$
seconds after she leaves the water. When is she highest, and how high?
How fast is she rising as she leaves the water?

```python exec
id: your-world-1--sea-and-sky
def height(t):
    return 3 * t - t ** 2
```

<details class="dl-answer"><summary>answer</summary>

`turning_points(height, 0, 3)` gives `[1.5]`, and `height(1.5)` is 2.25.
She is highest after 1.5 seconds, at 2.25 m.
`derivative_at(height, 0)` is about 3: she leaves the water rising at
3 m/s.

</details>

</div>

<div class="dl-world" data-world="planets-and-moons">

A lander's height above the ground is $100 - 20t + t^2$ metres, $t$
seconds after its engine starts. How fast is it coming down at the
start? What is its speed when it reaches the ground, at $t = 10$?

```python exec
id: your-world-1--planets-and-moons
def height(t):
    return 100 - 20 * t + t ** 2
```

<details class="dl-answer"><summary>answer</summary>

`derivative_at(height, 0)` is about $-20$: it starts coming down at
20 m/s. `height(10)` is 0 and `derivative_at(height, 10)` is about 0.
The lander reaches the ground at the very moment its speed reaches 0:
the ground is the bottom of its curve, a soft landing.

</details>

</div>

<div class="dl-world" data-world="fantasy-maps">

A dragon's height is $30 + 8x - x^2$ metres, $x$ km from its cave. Where
is it highest, and how high? How steeply is it climbing as it leaves
the cave?

```python exec
id: your-world-1--fantasy-maps
def height(x):
    return 30 + 8 * x - x ** 2
```

<details class="dl-answer"><summary>answer</summary>

`turning_points(height, 0, 8)` gives `[4.0]`, and `height(4)` is 46. The
dragon is highest 4 km from its cave, at 46 m. It leaves the cave
climbing 8 m for each kilometre.

</details>

</div>

## From earlier

**10.** From [Parabolas: completing the square](tutorial:parabolas).
The rocket's height was $-4.9t^2 + 15t + 2$. Completing the square put
its highest point at $t = \frac{15}{9.8} \approx 1.53$ seconds. Does
`turning_points` agree?

<details class="dl-answer"><summary>answer</summary>

`turning_points(lambda t: -4.9 * t ** 2 + 15 * t + 2, 0, 3)` gives
`[1.5]`, to one decimal place. Two different methods agree.

</details>

**11.** From [Limits: getting closer without arriving](tutorial:approaching-a-limit).
Why does `derivative_at` use a gap of `1e-6`, and not the smallest gap
it can, such as `1e-16`? What does `derivative_at(square, 3, gap=1e-16)`
print?

<details class="dl-answer"><summary>answer</summary>

It prints 0.0. `3 + 1e-16` is stored as 3, so both points are the same,
and the top of the fraction is 0. The limits page drew the error
against the gap as a V: too big a gap gives a chord that is not the
tangent, and too small a gap runs out of digits. `1e-6` is near the
bottom of that V for this way of measuring.

</details>
