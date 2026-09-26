---
title: "The unit circle: sine, cosine and tangent"
year: "2026-2027"
version: 2026.09.26.1
covers:
  going-round-in-circles:
    covers: [MIT-4.6]
  the-names-for-those-two-columns:
    covers: [MIT-4.6]
  measuring-the-walk:
    covers: [MIT-4.5]
  the-landmark-points:
    covers: [MIT-4.7]
  tangent-which-is-a-slope:
    covers: [MIT-4.6]
  the-circle-in-your-world:
    covers: [MIT-4.6, MIT-4.5]
worlds:
  sea-and-sky: A ship leaving harbour on a straight course. The numbers are made up.
  planets-and-moons: The Moon going round the Earth, with its orbit drawn as a circle.
  fantasy-maps: A windmill beside the castle, and the tips of its sails. The numbers are made up.
---

# The unit circle: sine, cosine and tangent

At the end of
[Distance and Pythagoras: how far apart two points are](tutorial:distance-and-pythagoras)
we drew a circle with radius 1 and its centre at $(0, 0)$. Every point on
it is 1 away from the centre. This circle is called the *unit circle*,
and this whole page is about it.

Think of a clock hand 1 unit long, pinned at the centre. It starts
pointing right, at $(1, 0)$, and turns anticlockwise. Where is its tip
after an eighth of a turn? After a quarter? After a half?

A quarter and a half are easy. After a quarter turn the tip points
straight up, at $(0, 1)$. After a half turn it points left, at
$(-1, 0)$. An eighth of a turn is harder. On this page we find it, and
every other place on the circle, and then we give the two coordinates
their names.

## Going round in circles

Here is a way to move the tip round the circle, using only things we
already have. We move it in many tiny steps. Each step goes at right
angles to the hand, because the tip of a turning hand always moves at
right angles to the hand. In
[Straight lines: slope, and the line that breaks the formula](tutorial:slope-and-lines)
we turned a direction a quarter turn by swapping its two numbers and
changing one sign, so $(x, y)$ becomes $(-y, x)$. After each step, the
tip is a tiny bit too far from the centre, so we pull it back to
distance 1.

The distance all the way round a circle is $2\pi r$. Here the radius
$r$ is 1, so the distance round is $2\pi$, about 6.28. An eighth of a
turn is an eighth of that distance.

```python exec
id: going-round-in-circles-1
import math
import matplotlib.pyplot as plt

def walk(distance_round, steps=10000):
    """Walk the tip from (1, 0), anticlockwise, this far round the circle."""
    x, y = 1.0, 0.0
    step = distance_round / steps
    for _ in range(steps):
        x, y = x - step * y, y + step * x    # a tiny step at right angles to the hand
        size = math.sqrt(x ** 2 + y ** 2)
        x, y = x / size, y / size            # back to distance 1 from the centre
    return x, y


print(walk(2 * math.pi / 4))
print(walk(2 * math.pi / 8))
```

```predict
type: number
tolerance: 0.01

The first line is a quarter turn, and prints about $(0, 1)$. The second
line is an eighth of a turn. How far up is the tip then, to two decimal
places?
```

The first line prints a tiny number, about `1.3e-08`, for the across
value. That is 0.000000013. The walk is very close, but not exact, so
read it as 0. After an eighth of a turn the tip is about 0.71 up, not
0.5. Why is it
more than halfway up, after half of a quarter turn?

At an eighth of a turn the hand points diagonally, so the tip has gone
as far across as it has gone up: $x = y$. The tip is also 1 from the
centre, so Pythagoras says $x^2 + y^2 = 1$. Put $x$ in place of $y$ and
solve:

$$
\begin{aligned}
x^2 + x^2 &= 1 \\
2x^2 &= 1 \\
x^2 &= \tfrac{1}{2} \\
x &= \tfrac{1}{\sqrt{2}} = \tfrac{\sqrt{2}}{2} \approx 0.7071
\end{aligned}
$$

The walk and the algebra agree. The tip climbs fast at first, when the
hand is flat, and slowly near the top, when the hand is almost upright.

Now let's walk to every eighth of a turn and write down where the tip
is.

```python exec
id: going-round-in-circles-2
print(" fraction of a turn      across      up")
for step in range(9):
    turns = step / 8
    x, y = walk(turns * 2 * math.pi)
    print(f"      {turns:>5.3f}           {x:>7.3f}   {y:>7.3f}")
```

We get two columns of numbers: how far across the tip is, and how far
up. The table is a record of where the tip went.

You may notice a `-0.000` in the table. That is a very small negative
number, which rounds to zero when we show three decimal places. You can
read it as 0.

Here are the same eight places, drawn on the circle:

```python exec
id: going-round-in-circles-3
fig, ax = plt.subplots(figsize=(5.5, 5.5))
circle = [walk(2 * math.pi * t / 100, steps=200) for t in range(101)]
ax.plot([p[0] for p in circle], [p[1] for p in circle], linewidth=2)

for step in range(8):
    x, y = walk(2 * math.pi * step / 8)
    ax.plot([0, x], [0, y], color="tab:orange", linewidth=1)
    ax.plot([x], [y], "o", color="tab:orange")

ax.axhline(0, color="black", linewidth=0.8)
ax.axvline(0, color="black", linewidth=0.8)
ax.set_aspect("equal")
ax.grid(alpha=0.3)
ax.set_title("Eight places on the circle")
```

Every point on the circle has $x^2 + y^2 = 1$. So in the top half of the
circle, $y = \sqrt{1 - x^2}$, and in the bottom half, $y = -\sqrt{1 - x^2}$.
That is a second way to find a point on the circle, from its across
value alone.

## The names for those two columns

The across value of the tip is called the *cosine*. The up value is
called the *sine*. Each one belongs to the angle the hand has turned
through.

So, for a point on the unit circle:

- the cosine of the angle is the point's across value, its $x$
  coordinate
- the sine of the angle is the point's up value, its $y$ coordinate

That is all the two words mean. Each one is a coordinate of a point on a
circle of radius 1. We did not need a triangle or a formula to say what
they are.

Python has them, as `math.cos` and `math.sin`. They take the distance
walked round the circle, as `walk` does. Do their answers match the
walk?

```python exec
id: the-names-for-those-two-columns-1
print(" distance     walk: across     cos        walk: up        sin")
for distance_round in [0.5, 1, 2, 3]:
    x, y = walk(distance_round)
    print(f"   {distance_round:<5}    {x:>10.6f} {math.cos(distance_round):>10.6f}"
          f"    {y:>10.6f} {math.sin(distance_round):>10.6f}")
```

The columns agree to six decimal places. Our walk and Python's `cos`
and `sin` find the same points. Python finds them in one step, far more
exactly, so from now on we use `math.cos` and `math.sin`.

Move the slider to walk the tip round the circle yourself. The number
on the slider is the distance walked, which is what `math.cos` and
`math.sin` take. Where is the across value negative? Where are the two
values equal?

```python exec
id: the-names-for-those-two-columns-3
walked = slider("distance round the circle", 0.0, 6.28, value=0.79)
angle = walked.value

fig, ax = plt.subplots(figsize=(4.5, 4.5))
rim = [2 * math.pi * k / 100 for k in range(101)]
ax.plot([math.cos(t) for t in rim], [math.sin(t) for t in rim], color="lightgrey")
ax.plot([0, math.cos(angle)], [0, math.sin(angle)], "o-", color="tab:orange")
ax.set_xlim(-1.2, 1.2)
ax.set_ylim(-1.2, 1.2)
ax.set_aspect("equal")
ax.grid(alpha=0.3)
print("across (cos):", round(math.cos(angle), 3), "   up (sin):", round(math.sin(angle), 3))
```

### The identity, discovered

In maths we often write the angle with the Greek letter $\theta$, called
"theta". Here is a fact about sine and cosine that many classrooms have
on the wall:

$$\sin^2\theta + \cos^2\theta = 1$$

The small 2 means "squared": $\sin^2\theta$ is $(\sin\theta)^2$.

Can you see why this is true, using what you already know? Every point on
the circle has $x^2 + y^2 = 1$. Now put in the names: $x$ is
$\cos\theta$ and $y$ is $\sin\theta$. That gives the identity. It is
Pythagoras, with new names for the coordinates.

```python exec
id: the-names-for-those-two-columns-2
for step in range(9):
    angle = step / 8 * 2 * math.pi
    s, c = math.sin(angle), math.cos(angle)
    print(f"sin^2 + cos^2 = {s ** 2 + c ** 2:.12f}")
```

### Your turn

The circle has four quarters. In each quarter, is the across value
positive or negative? What about the up value? Write your guesses in the
comments first. Then check each one with `math.cos` and `math.sin`, at
0.1, 0.35, 0.6 and 0.85 of a turn.

```python exec
id: your-turn-1
# Quarter 1: top right    across is ____, up is ____
# Quarter 2: top left     across is ____, up is ____
# Quarter 3: bottom left  across is ____, up is ____
# Quarter 4: bottom right across is ____, up is ____

# Check at 0.1, 0.35, 0.6 and 0.85 of a turn.
```

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Yours may be different and work too.

```python
for turns in [0.1, 0.35, 0.6, 0.85]:
    angle = turns * 2 * math.pi
    print(turns, math.cos(angle), math.sin(angle))
```

In the top right both are positive. In the top left the across value is
negative and the up value is positive. In the bottom left both are
negative. In the bottom right the across value is positive and the up
value is negative.

</details>

## Measuring the walk

So far we have measured angles as fractions of a turn, or as a distance
walked round the circle. People usually write angles in degrees, and a
quarter turn is 90 degrees. At a quarter turn the up value is exactly 1.

```python exec
id: measuring-the-walk-1
print("math.sin(90) =", math.sin(90))
```

```predict
type: choice

What will the cell print?

- math.sin(90) = 1.0
  - A quarter turn is 90 degrees, and the up value there is 1. There is
    [a closer look at this](tutorial:degrees-and-radians).
- Some other number between −1 and 1
- An error
  - `math.sin` may not accept a number as big as 90.
```

Python says about 0.894, not 1. `math.sin` does not take degrees. It
takes the distance walked round the unit circle, and 90 is a very long
walk: more than fourteen times round.

### What a radian is

A *radian* is a way to measure an angle by a distance walked round the
edge of the unit circle. When you have walked a distance of 1, the same
as the radius, you have turned through one radian.

```python exec
id: measuring-the-walk-2
fig, ax = plt.subplots(figsize=(5.5, 5.5))
circle = [(math.cos(t / 100 * 2 * math.pi), math.sin(t / 100 * 2 * math.pi))
          for t in range(101)]
ax.plot([p[0] for p in circle], [p[1] for p in circle], color="lightgrey", linewidth=2)

# One radian of arc: a walk of length 1 round the edge.
arc = [(math.cos(t / 100), math.sin(t / 100)) for t in range(101)]
ax.plot([p[0] for p in arc], [p[1] for p in arc], color="tab:orange", linewidth=4)
ax.plot([0, 1], [0, 0], color="tab:blue", linewidth=3)
ax.plot([0, math.cos(1)], [0, math.sin(1)], color="tab:blue", linewidth=3)
ax.annotate("radius = 1", (0.45, -0.12), color="tab:blue")
ax.annotate("arc = 1", (0.72, 0.62), color="tab:orange")
ax.axhline(0, color="black", linewidth=0.6)
ax.axvline(0, color="black", linewidth=0.6)
ax.set_aspect("equal")
ax.set_title("One radian: the angle where the arc equals the radius")
```

The orange arc and the blue radius have the same length. The angle
between the two blue lines is one radian.

A full turn is a walk of $2\pi$, so a full turn is $2\pi$ radians,
about 6.28. The $2\pi$ here is the distance round the circle. Because
the circle has radius 1, that distance is also the number of radians in
a turn.

```python exec
id: measuring-the-walk-3
print("A full turn:    ", 2 * math.pi, "radians")
print("Half a turn:    ", math.pi, "radians")
print("A quarter turn: ", math.pi / 2, "radians")
print()
print("sin of a quarter turn:", math.sin(math.pi / 2))
```

There is the 1 that was missing.

### Converting

A full turn is 360 degrees, and it is also $2\pi$ radians. So 360 degrees
and $2\pi$ radians are the same angle, and we can convert any angle by
proportion:

$$\text{radians} = \text{degrees} \times \frac{\pi}{180} \qquad \text{degrees} = \text{radians} \times \frac{180}{\pi}$$

For example, 90 degrees is $90 \times \frac{\pi}{180} = \frac{\pi}{2}$
radians, which is about $1.5708$.

```python exec
id: measuring-the-walk-4
def to_radians(degrees):
    return degrees * math.pi / 180


def to_degrees(radians):
    return radians * 180 / math.pi


for d in [0, 30, 45, 60, 90, 180, 360]:
    mine = to_radians(d)
    print(f"{d:>4} degrees = {mine:.6f} radians"
          f"   (Python says {math.radians(d):.6f})")

print()
print("One radian is about", round(to_degrees(1), 2), "degrees.")
```

That last number is a useful check to remember. One radian is a little
under 60 degrees. If you convert an angle and the answer is very far from
that scale, you have probably multiplied where you should have divided.

### Your turn

How would you convert these without `math.radians`? Find each one on
paper first, then check it in the cell.

1. 270 degrees to radians
2. 135 degrees to radians
3. $\pi/6$ radians to degrees
4. 2 radians to degrees

```python exec
id: your-turn-2
# Your answers here.
```

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Yours may be different and work too.

1. $270 \times \frac{\pi}{180} = \frac{3\pi}{2} \approx 4.712$
2. $135 \times \frac{\pi}{180} = \frac{3\pi}{4} \approx 2.356$
3. $\frac{\pi}{6} \times \frac{180}{\pi} = 30$ degrees
4. $2 \times \frac{180}{\pi} \approx 114.6$ degrees

</details>

## The landmark points

At some angles, we can find the coordinates exactly, with no calculator
and no decimals. We found one at the top of the page: at 45 degrees,
both coordinates are $\frac{\sqrt{2}}{2}$. Pythagoras finds two more.

Why do we want exact values? A decimal is an approximation, and
sometimes the difference matters. We will see an example below.

### Thirty and sixty degrees

These two angles come from half of an equilateral triangle.

1. Start with an equilateral triangle with sides of length 1. All its
   angles are 60 degrees.
2. Cut it down the middle. Each half is a right-angled triangle.
3. The *hypotenuse* of a right-angled triangle is its longest side, the
   one opposite the right angle. Each half has a hypotenuse of 1 and a
   short side of $\frac{1}{2}$.
4. We find the third side with Pythagoras:
   $\sqrt{1 - \left(\frac{1}{2}\right)^2} = \sqrt{\frac{3}{4}} = \frac{\sqrt{3}}{2}$.

```python exec
id: the-landmark-points-2
short = 1 / 2
other = math.sqrt(1 - short ** 2)
print("The short side is    ", short)
print("So the other side is ", other)
print("which is sqrt(3)/2 = ", math.sqrt(3) / 2)
print()

for degrees in [30, 45, 60]:
    angle = math.radians(degrees)
    print(f"{degrees} degrees:  across {math.cos(angle):.6f}   up {math.sin(angle):.6f}")
```

Here is the whole table for the first quarter of the circle:

| Angle | across ($\cos$) | up ($\sin$) |
|---|---|---|
| 0° | $1$ | $0$ |
| 30° | $\frac{\sqrt{3}}{2}$ | $\frac{1}{2}$ |
| 45° | $\frac{\sqrt{2}}{2}$ | $\frac{\sqrt{2}}{2}$ |
| 60° | $\frac{1}{2}$ | $\frac{\sqrt{3}}{2}$ |
| 90° | $0$ | $1$ |

Look at the rows for 30° and 60°. What do you notice? The two values are
swapped. That is because they come from the same triangle, seen from its
other corner.

### Why the exact form matters

The decimal is not the same number as the exact value. Here is a case
where we can see the difference.

We know that $\left(\frac{\sqrt{2}}{2}\right)^2 = \frac{2}{4} = \frac{1}{2}$
exactly. What happens when we square a decimal version instead? Which
answer do you think will be closer to a half?

```python exec
id: the-landmark-points-3
exact = math.sqrt(2) / 2
rounded = 0.7071

print("Python's value squared:", exact ** 2)
print("0.7071 squared:        ", rounded ** 2)
print()
print("Python's value misses a half by:", abs(exact ** 2 - 0.5))
print("0.7071 misses a half by:        ", abs(rounded ** 2 - 0.5))
```

An ending such as `e-16` means "times $10^{-16}$". So Python's value
misses a half by about $0.0000000000000001$, and $0.7071$ misses by about
$0.00001$.

$0.7071$ squared is $0.49999\ldots$. That is close to a half, but it is a
different number. Even Python's own `math.sqrt(2) / 2` is a decimal with
about 16 digits, so its square misses a half by a very tiny amount.

Only the exact form $\frac{\sqrt{2}}{2}$ squares to exactly $\frac{1}{2}$.
That is why we use *surd form*. A *surd* is a root such as $\sqrt{2}$
that we leave as a root, without turning it into a decimal. The decimal
differs from it by a small amount, and in some calculations small amounts add
up.

### Your turn

What are the exact values for 120°, 135° and 150°? Can you find them
from the first-quarter table, and the signs you found for each quarter?
Write your answers in the comments, then run the check.

```python exec
id: your-turn-3
# 120 degrees: across ____   up ____
# 135 degrees: across ____   up ____
# 150 degrees: across ____   up ____

# Then check:
# for d in [120, 135, 150]:
#     print(d, math.cos(math.radians(d)), math.sin(math.radians(d)))
```

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Yours may be different and work too.

Each of these is in the top-left quarter, so the across value is
negative and the up value is positive. 120° is 60° short of a half
turn, so it uses the 60° row. 135° uses the 45° row, and 150° uses the
30° row.

- 120°: across $-\frac{1}{2}$, up $\frac{\sqrt{3}}{2}$
- 135°: across $-\frac{\sqrt{2}}{2}$, up $\frac{\sqrt{2}}{2}$
- 150°: across $-\frac{\sqrt{3}}{2}$, up $\frac{1}{2}$

</details>

## Tangent, which is a slope

There is a third name. It is not a third coordinate, because the point
has only two.

The *tangent* of an angle is the up value divided by the across value:

$$\tan\theta = \frac{\sin\theta}{\cos\theta} = \frac{y}{x}$$

Now think about the line from the origin out to the point. Its rise is
$y$ and its run is $x$. In
[Straight lines: slope, and the line that breaks the formula](tutorial:slope-and-lines)
we called rise divided by run the slope. So the tangent is the slope of
the line from the origin to the point.

For example, at 60 degrees the point is
$\left(\frac{1}{2}, \frac{\sqrt{3}}{2}\right)$, so
$\tan 60^\circ = \frac{\sqrt{3}}{2} \div \frac{1}{2} = \sqrt{3} \approx 1.732$.

```python exec
id: tangent-which-is-a-slope-1
print(" degrees      up/across        math.tan")
for d in [0, 30, 45, 60, 80, 89]:
    angle = to_radians(d)
    x, y = math.cos(angle), math.sin(angle)
    print(f"   {d:>3}      {y / x:>10.5f}    {math.tan(angle):>12.5f}")
```

At 45 degrees the tangent is 1. That is the slope of the line $y = x$,
which also goes out at 45 degrees. Does that match your picture of the
line?

### The place it breaks

What happens to the tangent as the angle gets close to 90 degrees? Write
your guess in a comment first. Then run the cell.

```python exec
id: tangent-which-is-a-slope-2
for d in [80, 85, 89, 89.9, 89.99]:
    print(f"tan({d:>6}) = {math.tan(to_radians(d)):>16.3f}")
```

The tangent grows without any limit as the angle gets close to 90
degrees. At exactly 90 degrees there is no answer at all.

You have met this before. At 90 degrees the point is at $(0, 1)$, so the
across value is zero, and $\frac{1}{0}$ is not a number. The line from
the origin is vertical, and a vertical line has no slope. It is the same
line that would not fit $y = mx + c$ in
[Straight lines: slope, and the line that breaks the formula](tutorial:slope-and-lines).

If you try `math.tan(math.pi / 2)` yourself, Python gives a huge number
in place of an error. That is because `math.pi / 2` is a decimal, a tiny
bit away from the exact quarter turn.

```python exec
id: tangent-which-is-a-slope-3
fig, ax = plt.subplots(figsize=(7, 4))
degrees = [d / 4 for d in range(-4 * 89, 4 * 90)]
ax.plot(degrees, [math.tan(to_radians(d)) for d in degrees], linewidth=2)
ax.axhline(0, color="black", linewidth=0.8)
ax.axvline(90, color="tab:red", linestyle="--", label="90 degrees")
ax.axvline(-90, color="tab:red", linestyle="--")
ax.set_ylim(-8, 8)
ax.legend()
ax.set_title("Tangent, and the angle where it has no value")
```

## The circle in your world

A circle of radius $r$ is the unit circle made $r$ times bigger. So the
point at angle $\theta$ on it is $(r\cos\theta, r\sin\theta)$.

<div class="dl-world" data-world="sea-and-sky">

A ship leaves the harbour at $(0, 0)$ and sails 12 km in a straight line,
at 35 degrees anticlockwise from east. Where is it on the chart? Can you
write `position(km, degrees)` for any distance and angle?

```python exec
id: the-circle-in-your-world-1--sea-and-sky
harbour = (0, 0)
```

```hint
The ship is on a circle of radius 12 round the harbour. `math.cos` and
`math.sin` take radians.
```

```inputs
position(12, 35)
position(12, 90)
position(5, 180)
```

```solution
def position(km, degrees):
    angle = math.radians(degrees)
    return km * math.cos(angle), km * math.sin(angle)


print(position(12, 35))
---
The ship is at about $(9.83, 6.88)$: 9.83 km east of the harbour and
6.88 km north. At 90 degrees it would be due north, at about $(0, 12)$.
A tiny number such as `7.3e-16` in place of 0 is a rounding effect.
```

</div>

<div class="dl-world" data-world="planets-and-moons">

The Moon goes round the Earth once in about 27.3 days, about 384,400 km
away. Its path is not quite a circle, but a circle is close. Put the
Earth at $(0, 0)$ and the Moon at $(384400, 0)$ on day 0, going
anticlockwise. Can you write `moon_position(days)`? Where is the Moon
after 5 days?

```python exec
id: the-circle-in-your-world-1--planets-and-moons
orbit_km = 384400
orbit_days = 27.3
```

```hint
What fraction of a turn does the Moon make in 5 days? A full turn is
$2\pi$ radians.
```

```inputs
moon_position(5)
moon_position(orbit_days / 4)
moon_position(orbit_days)
```

```solution
def moon_position(days):
    angle = days / orbit_days * 2 * math.pi
    return orbit_km * math.cos(angle), orbit_km * math.sin(angle)


print(moon_position(5))
---
After 5 days the Moon has turned through about 66 degrees, and it is at
about $(156754, 350987)$. After a quarter of 27.3 days it is at the top
of the circle, and after 27.3 days it is back where it started.
```

</div>

<div class="dl-world" data-world="fantasy-maps">

The windmill beside the castle has sails 6 m long, turning round a hub
10 m above the ground. How high is the tip of a sail when it has turned
50 degrees anticlockwise from pointing right? Can you write
`tip_height(degrees)`? What are the highest and lowest the tip goes?

```python exec
id: the-circle-in-your-world-1--fantasy-maps
hub_height = 10    # metres
sail = 6           # metres
```

```hint
The tip is on a circle of radius 6 round the hub. Its height is the hub's
height, plus the up value on that circle.
```

```inputs
tip_height(50)
tip_height(90)
tip_height(270)
```

```solution
def tip_height(degrees):
    return hub_height + sail * math.sin(math.radians(degrees))


print(tip_height(50))
---
At 50 degrees the tip is about 14.6 m up. It is highest at 90 degrees,
16 m, and lowest at 270 degrees, 4 m.
```

</div>

## Looking back

We walked a point round one circle, and wrote down where it went. The
across value is the cosine, the up value is the sine, and the tangent
is the slope of the hand. A radian is a distance walked round the
circle.

Before this page, what did you think sine and cosine were? Has your idea
changed? If it has, where on the page did it change?

A challenge: can you draw a clock face, with its hour hand and minute
hand, for any time? A clock measures clockwise from 12 o'clock, and the
unit circle measures anticlockwise from 3 o'clock. How do you change one
into the other?

```python challenge
import math
import matplotlib.pyplot as plt


def draw_clock(hours, minutes):
    """Draw a clock face showing this time."""
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.set_aspect("equal")
    # Your code here.


draw_clock(3, 0)
draw_clock(10, 10)
```

[Sine and cosine waves: amplitude, period and shift](tutorial:sine-and-cosine-waves)
takes this circle and unrolls it flat.

## Where to read more

Khan Academy. *Introduction to the Unit Circle.*
<https://www.youtube.com/watch?v=1m9p9iubMLU>. This video explains the
same across-and-up coordinates as this page, but starts from SOH CAH TOA.

Khan Academy. *Introduction to Radians.*
<https://www.youtube.com/watch?v=EnwWxMZVBeg>. This video shows a second
way to see why a full turn is `2π` radians.

SimonDev (2023). *So how does your computer ACTUALLY compute sine?*
<https://www.youtube.com/watch?v=kkMt4lrJzs8>. Our `walk` found sine and
cosine in ten thousand small steps. This video shows how a computer
finds them much faster. It is about eight minutes long.
