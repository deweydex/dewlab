---
title: "The unit circle: sine, cosine and tangent"
year: "2026-2027"
version: 2026.09.25.1
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
---

# The unit circle: sine, cosine and tangent

This whole page is about one drawing. The *unit circle* is a circle with
radius 1, with its centre at the origin, $(0, 0)$.

You have met this circle before. At the end of
[Straight lines: slope, midpoint and distance](tutorial:lines-and-distances)
you drew it, and you checked that every point on it is at distance 1 from
the centre. That one rule is all we need here.

Sine, cosine, radians and the exact values are often taught as four
separate things to learn. In fact they are one drawing, described in four
ways. On this page we:

- walk a point around the circle and write down where it is
- give the two coordinates of that point their names, sine and cosine
- measure angles in a new way, called radians
- work out some points on the circle exactly, with Pythagoras
- meet a third name, tangent, and see that it is a slope

## Going round in circles

Let's start at the right-hand side of the circle, walk a point around it,
and write down where the point is after each eighth of a turn.

```python exec
id: going-round-in-circles-1
import math
import matplotlib.pyplot as plt

def unit_point(turns):
    """Where you are after going `turns` of the way round, starting at the right."""
    angle = turns * 2 * math.pi
    return (math.cos(angle), math.sin(angle))


print(" fraction of a turn      across      up")
for step in range(9):
    turns = step / 8
    x, y = unit_point(turns)
    print(f"      {turns:>5.3f}           {x:>7.3f}   {y:>7.3f}")
```

We get two columns of numbers: how far across the point is, and how far
up. There is no new vocabulary yet, and we do not need any. The table is a
record of where the point went.

You may notice a `-0.000` in the table. That is a very small negative
number, which rounds to zero when we show three decimal places. You can
read it as 0.

Here are the same eight places, drawn on the circle:

```python exec
id: going-round-in-circles-2
fig, ax = plt.subplots(figsize=(5.5, 5.5))
circle = [unit_point(t / 200) for t in range(201)]
ax.plot([p[0] for p in circle], [p[1] for p in circle], linewidth=2)

for step in range(8):
    x, y = unit_point(step / 8)
    ax.plot([0, x], [0, y], color="tab:orange", linewidth=1)
    ax.plot([x], [y], "o", color="tab:orange")

ax.axhline(0, color="black", linewidth=0.8)
ax.axvline(0, color="black", linewidth=0.8)
ax.set_aspect("equal")
ax.grid(alpha=0.3)
ax.set_title("Eight places on the circle")
```

Are all the orange lines the same length? We can check with the
`distance` function from
[Straight lines: slope, midpoint and distance](tutorial:lines-and-distances).
What do you expect it to print?

```python exec
id: going-round-in-circles-3
def distance(p, q):
    (x1, y1), (x2, y2) = p, q
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


for step in range(8):
    p = unit_point(step / 8)
    print(f"({p[0]:>7.3f}, {p[1]:>7.3f})   distance from centre: {distance((0, 0), p):.10f}")
```

The distance is exactly 1, every time. That is the key fact. Everything
on the rest of this page follows from it: the two columns come from a
point that always stays at distance 1 from the middle.

## The names for those two columns

The across column has a name: it is called *cosine*. The up column is
called *sine*.

So, for a point on the unit circle:

- the cosine of the angle is the point's across value, its $x$
  coordinate
- the sine of the angle is the point's up value, its $y$ coordinate

That is all the two words mean. Each one is a coordinate of a point on a
circle of radius 1. We do not need a triangle or a formula to say what
they are.

Python calls them `math.cos` and `math.sin`. Do the columns match?

```python exec
id: the-names-for-those-two-columns-1
print("  turns        x        cos       y        sin")
for step in range(5):
    turns = step / 8
    angle = turns * 2 * math.pi
    x, y = unit_point(turns)
    print(f"  {turns:>5.3f}  {x:>8.4f} {math.cos(angle):>10.4f}"
          f" {y:>8.4f} {math.sin(angle):>9.4f}")
```

The columns match, because we built `unit_point` out of `cos` and `sin`
in the first place. What matters is the order of the ideas. The
coordinates came first, and cosine and sine are the names we gave them.

### The identity, discovered

In maths we often write the angle with the Greek letter $\theta$, called
"theta". Here is a fact about sine and cosine that many classrooms have
on the wall:

$$\sin^2\theta + \cos^2\theta = 1$$

The small 2 means "squared": $\sin^2\theta$ is $(\sin\theta)^2$.

Can you see why this is true, using what you already know? Every point on
the circle is at distance 1 from the centre. The distance formula comes
from Pythagoras, so every point on this circle has $x^2 + y^2 = 1$. Now
put in the names: $x$ is $\cos\theta$ and $y$ is $\sin\theta$. That gives
the identity.

For example, at an eighth of a turn both coordinates are about $0.7071$,
and $0.7071^2 + 0.7071^2 \approx 0.5 + 0.5 = 1$.

```python exec
id: the-names-for-those-two-columns-2
for step in range(9):
    angle = step / 8 * 2 * math.pi
    s, c = math.sin(angle), math.cos(angle)
    print(f"sin^2 + cos^2 = {s ** 2 + c ** 2:.12f}")
```

We did not need anything new for this. It is the distance formula from
[Straight lines: slope, midpoint and distance](tutorial:lines-and-distances),
used on a circle of radius 1, with new names for the coordinates.

### Your turn

The circle has four quarters. In each quarter, is the across value
positive or negative? What about the up value?

1. Write your prediction for each quarter in the comments below.
2. Check each one with `unit_point` at 0.1, 0.35, 0.6 and 0.85 of a turn.

```python exec
id: your-turn-1
# Quarter 1: top right   — across is ____, up is ____
# Quarter 2: top left    — across is ____, up is ____
# Quarter 3: bottom left — across is ____, up is ____
# Quarter 4: bottom right— across is ____, up is ____

# Check with unit_point at 0.1, 0.35, 0.6, 0.85 of a turn.
```

## Measuring the walk

So far we have measured angles as fractions of a turn. That is accurate,
but people do not usually write angles that way. There are two standard
ways, and one of them will look strange at first.

We start with something strange, because it is the reason the second way
exists. A quarter turn is 90 degrees, and at a quarter turn the up value
is exactly 1. So what do you think `math.sin(90)` gives?

```python exec
id: measuring-the-walk-1
print("math.sin(90) =", math.sin(90))
```

Python says about 0.894, not 1. Python is not wrong. It is answering a
different question, because `math.sin` does not take degrees. It takes
radians.

### What a radian is

A *radian* is a way to measure an angle by a distance walked around the
edge of the circle.

Take the circle of radius 1 and walk along its edge. When you have walked
a distance of 1, the same as the radius, you have turned through one
radian.

```python exec
id: measuring-the-walk-2
fig, ax = plt.subplots(figsize=(5.5, 5.5))
circle = [unit_point(t / 200) for t in range(201)]
ax.plot([p[0] for p in circle], [p[1] for p in circle], color="lightgrey", linewidth=2)

# One radian of arc: from angle 0 to angle 1, in radians.
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

How many radians are there in a full turn? The distance all the way round
a circle is $2\pi r$, so for a circle of radius 1 it is $2\pi$. That is
what $\pi$ is for. So a full turn is $2\pi$ radians, which is about
$6.28$.

```python exec
id: measuring-the-walk-3
print("A full turn:    ", 2 * math.pi, "radians")
print("Half a turn:    ", math.pi, "radians")
print("A quarter turn: ", math.pi / 2, "radians")
print()
print("sin of a quarter turn:", math.sin(math.pi / 2))
```

There is the 1 that was missing.

The $2\pi$ here is not a magic number that turns up in trigonometry for a
mysterious reason. It is the distance round the circle. Because the
circle has radius 1, that distance is also the number of radians in a
turn.

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

How would you convert these without using `math.radians`? Work each one
out first, then check it in the cell.

1. Convert 270 degrees to radians.
2. Convert 135 degrees to radians.
3. Convert $\pi/6$ radians to degrees.
4. Convert 2 radians to degrees.

```python exec
id: your-turn-2
# Your answers here.
```

## The landmark points

At some angles, we can work out the coordinates exactly, with no
calculator and no decimals. The working is Pythagoras again.

Why do we want exact values? A decimal is an approximation, and
sometimes the difference matters. We will see an example below.

### Forty-five degrees

At 45 degrees the point moves diagonally. It has gone as far across as it
has gone up, so $x = y$.

We also know that $x^2 + y^2 = 1$, because that is true for every point
on this circle. So we have two facts and one unknown. Put $x$ in place of
$y$ and solve:

$$
\begin{aligned}
x^2 + x^2 &= 1 \\
2x^2 &= 1 \\
x^2 &= \tfrac{1}{2} \\
x &= \tfrac{1}{\sqrt{2}} = \tfrac{\sqrt{2}}{2}
\end{aligned}
$$

Is that the same as the point `unit_point` finds? Run the cell to check.

```python exec
id: the-landmark-points-1
exact = math.sqrt(2) / 2
point = unit_point(45 / 360)

print("Worked out by hand: ", exact)
print("From the circle:    ", point[0], point[1])
print()
print("Do they agree?", abs(exact - point[0]) < 1e-12)
```

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
    x, y = unit_point(degrees / 360)
    print(f"{degrees} degrees:  across {x:.6f}   up {y:.6f}")
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
That is why we use *surd form*: a surd is a root such as $\sqrt{2}$ that
we leave as a root, without turning it into a decimal. It is more than a
tidier way to write the decimal. The decimal is wrong by a small amount,
and in some calculations small amounts add up.

### Your turn

What are the exact values for 120°, 135° and 150°?

1. Use the first-quarter table above.
2. Use the signs you worked out for each quarter earlier.
3. Fill in the comments, then run the check.

```python exec
id: your-turn-3
# 120 degrees: across ____   up ____
# 135 degrees: across ____   up ____
# 150 degrees: across ____   up ____

# Then check:
# for d in [120, 135, 150]:
#     print(d, unit_point(d / 360))
```

## Tangent, which is a slope

There is a third name. It is not a third coordinate, because the point
has only two.

The *tangent* of an angle is the up value divided by the across value:

$$\tan\theta = \frac{\sin\theta}{\cos\theta} = \frac{y}{x}$$

Now think about the line from the origin out to the point. Its rise is
$y$ and its run is $x$. In
[Straight lines: slope, midpoint and distance](tutorial:lines-and-distances)
we called rise divided by run the slope. So the tangent is the slope of
the line from the origin to the point.

For example, at 60 degrees the point is
$\left(\frac{1}{2}, \frac{\sqrt{3}}{2}\right)$, so
$\tan 60^\circ = \frac{\sqrt{3}}{2} \div \frac{1}{2} = \sqrt{3} \approx 1.732$.

```python exec
id: tangent-which-is-a-slope-1
print(" degrees      up/across        math.tan")
for d in [0, 30, 45, 60, 80, 89]:
    x, y = unit_point(d / 360)
    print(f"   {d:>3}      {y / x:>10.5f}    {math.tan(to_radians(d)):>12.5f}")
```

At 45 degrees the tangent is 1. That is the slope of the line $y = x$,
which also goes out at 45 degrees. Does that match your picture of the
line?

### The place it breaks

What happens to the tangent as the angle gets close to 90 degrees? Make a
guess, then run the cell.

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
[Straight lines: slope, midpoint and distance](tutorial:lines-and-distances).
Here it arrives from a different direction.

If you try `math.tan(math.pi / 2)` yourself, Python gives a huge number
instead of an error. That is because `math.pi / 2` is a decimal, a tiny
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

## Reflection

We looked at one circle, and everything else was a description of it.

**Cosine and sine are coordinates.** They are the across and up values of
a point on a circle of radius 1. Later, triangles use them too, but the
circle comes first.

**$\sin^2\theta + \cos^2\theta = 1$ is Pythagoras.** Every point on the
circle is at distance 1 from the centre. The distance formula tells us
what that means for the coordinates.

**A radian is a distance walked.** That is why a full turn is $2\pi$
radians: $2\pi$ is the distance round a circle of radius 1.

**The exact values are places on the circle.** You do not need to
memorise them. $\frac{\sqrt{2}}{2}$ is where the 45° line crosses the
circle, and one line of Pythagoras shows why.

**Tangent is a slope.** It has no value at 90 degrees, for the same
reason that a vertical line has no slope.

Next, [Sine and cosine waves: amplitude, period and shift](tutorial:sine-and-cosine-waves)
takes this circle and unrolls it flat.

Before this page, what did you think sine and cosine were? Write a few
sentences. Has your idea changed? If it has, where on the page did it
change?

## Where to Read More

Khan Academy. *Introduction to the Unit Circle.*
<https://www.youtube.com/watch?v=1m9p9iubMLU>. The same across-and-up
coordinates this page builds, introduced from SOH CAH TOA instead.

Khan Academy. *Introduction to Radians.*
<https://www.youtube.com/watch?v=EnwWxMZVBeg>. Why a full turn is `2π`
radians, covered a second way.

SimonDev (2023). *So how does your computer ACTUALLY compute sine?*
<https://www.youtube.com/watch?v=kkMt4lrJzs8>. Sine and cosine on the unit
circle, and then the question this page leaves open: how does a computer
find the sine of an angle at all? About eight minutes.
