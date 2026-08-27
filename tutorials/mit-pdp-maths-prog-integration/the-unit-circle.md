---
title: "The Unit Circle"
slug: the-unit-circle
module: mit-pdp-maths-prog-integration
module_title: "Programming and Maths, Integrated"
year: "2026-2027"
series: maths-and-programming
version: 2026.08.23.1
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

# The Unit Circle

**Maths for IT**

A circle of radius one, centred on the origin. That is the whole subject of this tutorial, and three separate-looking pieces of trigonometry turn out to be three things you can read off it.

At the end of *Lines and Distances* you drew this circle and checked that every point on it really was distance 1 from the centre. That check is the only rule everything here rests on.

Sine, cosine, radians and the exact values are usually taught as four things to learn. They are one drawing, described four ways.

## Going Round in Circles

Walk a point around the circle and write down where it is.

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

Two columns of numbers. No vocabulary yet, and none needed — this is just a record of where a point got to.

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

Every one of those orange lines is the same length, and you can check that with the distance function you wrote last tutorial.

```python exec
id: going-round-in-circles-3
def distance(p, q):
    (x1, y1), (x2, y2) = p, q
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


for step in range(8):
    p = unit_point(step / 8)
    print(f"({p[0]:>7.3f}, {p[1]:>7.3f})   distance from centre: {distance((0, 0), p):.10f}")
```

Exactly 1, every time. **That is the whole of it.** Everything below is a consequence of those two columns coming from a point that stays 1 away from the middle.

## The Names for Those Two Columns

The across column is called **cosine**. The up column is called **sine**.

That is all those two words mean. Not a formula, not an operation on a triangle — the two coordinates of a point on a circle of radius one.

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

The columns match because `unit_point` was built out of `cos` and `sin` in the first place. The point is the direction of the definition: **cosine and sine were named after the coordinates, not the other way round.**

### The identity, discovered

There is a fact about sine and cosine that gets written on classroom walls:

`sin²θ + cos²θ = 1`

You already have it. Every point is distance 1 from the centre, and distance is Pythagoras, so `x² + y² = 1` for every point on this circle. Substitute the names in and there it is.

```python exec
id: the-names-for-those-two-columns-2
for step in range(9):
    angle = step / 8 * 2 * math.pi
    s, c = math.sin(angle), math.cos(angle)
    print(f"sin^2 + cos^2 = {s ** 2 + c ** 2:.12f}")
```

**Nothing new was needed to get that.** It is the distance formula from the previous tutorial, applied to a circle of radius 1, with the coordinates renamed.

### Your turn

What sign would you predict for the across value and the up value in each of the four quarters of the circle? Check your predictions below.

```python exec
id: your-turn-1
# Quarter 1: top right   — across is ____, up is ____
# Quarter 2: top left    — across is ____, up is ____
# Quarter 3: bottom left — across is ____, up is ____
# Quarter 4: bottom right— across is ____, up is ____

# Check with unit_point at 0.1, 0.35, 0.6, 0.85 of a turn.
```

## Measuring the Walk

So far angles have been fractions of a turn, which is honest but not how anyone writes them. There are two standard ways, and one of them will look strange.

Start with the strangeness, because it is the reason the second one exists.

```python exec
id: measuring-the-walk-1
print("math.sin(90) =", math.sin(90))
```

Ninety degrees is a quarter turn, and the up value there is exactly 1. Python said 0.894.

Python is not wrong. It is answering a different question, because `math.sin` does not take degrees.

### What a radian is

**A radian is a distance walked around the edge.**

Take the circle of radius 1 and walk along its edge. When you have walked a distance of 1 — the same as the radius — you have turned through one radian.

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

The orange arc and the blue radius are the same length. The angle between the two blue lines is one radian.

That definition immediately tells you how many there are in a full turn. The whole way round a circle of radius 1 is a distance of `2π` — that is what π is for — so **a full turn is `2π` radians.**

```python exec
id: measuring-the-walk-3
print("A full turn:    ", 2 * math.pi, "radians")
print("Half a turn:    ", math.pi, "radians")
print("A quarter turn: ", math.pi / 2, "radians")
print()
print("sin of a quarter turn:", math.sin(math.pi / 2))
```

There is the 1 that was missing.

`2π` is not a magic constant that appears in trigonometry for mysterious reasons. It is the distance round the circle, and the circle has radius 1, so it is also the number of radians in a turn.

### Converting

A full turn is 360 degrees and `2π` radians, so those two are equal, and everything follows by proportion.

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

That last number is worth remembering as a sanity check. A radian is a bit under 60 degrees, so if you convert something and the answer is wildly off that scale, you have multiplied where you should have divided.

### Your turn

How would you convert these without using `math.radians`? Work them out, then check.

- 270 degrees
- 135 degrees
- `π/6` radians into degrees
- 2 radians into degrees

```python exec
id: your-turn-2
# Your answers here.
```

## The Landmark Points

Some angles land on coordinates you can work out exactly, with no calculator and no decimals — and the working is Pythagoras again.

These are worth having because a decimal is an approximation and sometimes that matters.

### Forty-five degrees

At 45 degrees you are going diagonally, which means **you have gone as far across as you have gone up**. So `x = y`.

And you know `x² + y² = 1`, because every point on this circle does. Two facts, one unknown:

```
x² + x² = 1
2x²     = 1
x²      = 1/2
x       = 1/√2 = √2/2
```

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

These come from half an equilateral triangle. An equilateral triangle with sides of 1 has all angles 60 degrees; cut it down the middle and you get a right-angled triangle with a hypotenuse of 1, a short side of 1/2, and a third side you can get from Pythagoras.

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

So the whole first-quarter table is:

| Angle | across (cos) | up (sin) |
|---|---|---|
| 0° | 1 | 0 |
| 30° | √3⁄2 | 1⁄2 |
| 45° | √2⁄2 | √2⁄2 |
| 60° | 1⁄2 | √3⁄2 |
| 90° | 0 | 1 |

Notice that 30 and 60 are each other's, swapped. That is the same triangle looked at from its other corner.

### Why the exact form matters

The decimal is not the same as the exact value, and here is a case where the difference shows.

```python exec
id: the-landmark-points-3
exact = math.sqrt(2) / 2
rounded = 0.7071

print("exact squared:  ", exact ** 2)
print("rounded squared:", rounded ** 2)
print()
print("exact is exactly a half:  ", exact ** 2 == 0.5)
print("rounded is exactly a half:", rounded ** 2 == 0.5)
```

`√2⁄2` squared is exactly `1/2`. `0.7071` squared is `0.49999`, which is close and is not the same number.

**That is the point of surd form.** It is not a tidier way of writing a decimal — the decimal is *wrong*, by a small amount, and there are places where a small amount accumulates.

### Your turn

What are the exact values for 120°, 135° and 150°? Use the first-quarter table and the signs you worked out earlier.

```python exec
id: your-turn-3
# 120 degrees: across ____   up ____
# 135 degrees: across ____   up ____
# 150 degrees: across ____   up ____

# Then check:
# for d in [120, 135, 150]:
#     print(d, unit_point(d / 360))
```

## Tangent, Which Is a Slope

There is a third name, and it is not a third coordinate — the point only has two.

**Tangent is the up divided by the across.** And the up divided by the across of a line from the origin is exactly what *Lines and Distances* called the slope.

```python exec
id: tangent-which-is-a-slope-1
print(" degrees      up/across        math.tan")
for d in [0, 30, 45, 60, 80, 89]:
    x, y = unit_point(d / 360)
    print(f"   {d:>3}      {y / x:>10.5f}    {math.tan(to_radians(d)):>12.5f}")
```

So tangent is the slope of the line from the origin out to that point. At 45 degrees it is 1, which is the slope of `y = x`, and that should feel right.

### The place it breaks

```python exec
id: tangent-which-is-a-slope-2
for d in [80, 85, 89, 89.9, 89.99]:
    print(f"tan({d:>6}) = {math.tan(to_radians(d)):>16.3f}")
```

It runs away to infinity as the angle approaches 90 degrees. At exactly 90 there is no answer at all — and you have met this before.

At 90 degrees the point is at `(0, 1)`, so the across is zero, and `1/0` is not a number. **It is the vertical line that has no slope** — the same one that would not fit `y = mx + c` in the previous tutorial, arriving from a different direction.

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

One circle, and everything else was a description of it.

**Cosine and sine are coordinates.** Across and up, for a point on a circle of radius one. They are not operations to perform on a triangle; the triangle comes later and inherits them.

**`sin²θ + cos²θ = 1` is Pythagoras.** Every point on the circle is 1 from the centre, and the distance formula says what that means about the coordinates.

**A radian is a distance walked.** Which is why a full turn is `2π` of them — that is how far it is round a circle of radius 1.

**The exact values are places, not numbers to memorise.** √2⁄2 is where the 45° line crosses, and the reason it is √2⁄2 is one line of Pythagoras.

**Tangent is a slope**, and it has no value at 90 degrees for the same reason a vertical line has no slope.

Next, [Sine and Cosine Waves](tutorial:sine-and-cosine-waves) takes this circle and unrolls it flat.

In a few sentences, before this tutorial, what did you think sine and cosine were? Has that changed, and if so, when in the tutorial did it change?

## Where to Read More

Khan Academy. *Introduction to the Unit Circle.*
<https://www.youtube.com/watch?v=1m9p9iubMLU>. The same across-and-up
coordinates this page builds, introduced from SOH CAH TOA instead.

Khan Academy. *Introduction to Radians.*
<https://www.youtube.com/watch?v=EnwWxMZVBeg>. Why a full turn is `2π`
radians, covered a second way.
