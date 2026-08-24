---
title: "Lines and Distances"
slug: lines-and-distances
module: mit-pdp-maths-prog-integration
module_title: "Programming and Maths, Integrated"
year: "2026-2027"
series: maths-and-programming
version: 2026.08.23.1
covers:
  a-line-you-have-already-written:
    covers: [MIT-4.1]
  slope-as-how-fast-something-changes:
    covers: [MIT-4.2]
  parallel-and-perpendicular:
    covers: [MIT-4.2]
  the-line-that-breaks-the-formula:
    covers: [MIT-4.1]
  midpoint-which-needs-no-theory:
    covers: [MIT-4.3]
  how-far-apart-and-the-theorem-that-answers-it:
    covers: [MIT-4.3, MIT-4.4]
---

# Lines and Distances

**Maths for IT**

Two questions, and the whole tutorial is about them: **how do you describe a line**, and **how far apart are two things**.

Both sound like they should be easy, and the first one has three different answers, each better than the others at something. The second one turns out to be a theorem you have heard of, arriving from a direction that makes it obvious.

This is not called "coordinate geometry", though that is the name in the syllabus. Geometry is a word that, for a lot of people, means a thing they did at fifteen with a compass and did not enjoy. There is no compass here. There is a pair of axes, which you have been using since *Pictures Worth Numbers*, and there are two questions somebody might actually have.

## A Line You Have Already Written

You have written straight lines as functions since *Drawing Functions*. Here is one again.

```python exec
id: a-line-you-have-already-written-1
import matplotlib.pyplot as plt

def axes(size=8):
    fig, ax = plt.subplots(figsize=(5.5, 5.5))
    ax.axhline(0, color="black", linewidth=0.8)
    ax.axvline(0, color="black", linewidth=0.8)
    ax.grid(alpha=0.3)
    ax.set_xlim(-size, size)
    ax.set_ylim(-size, size)
    ax.set_aspect("equal")
    return ax


def draw_line(ax, m, c, label=None, style="-"):
    xs = [-10, 10]
    ax.plot(xs, [m * x + c for x in xs], style, label=label)
    if label:
        ax.legend(loc="upper left", fontsize=8)
    return ax


ax = axes()
draw_line(ax, 2, 1, label="y = 2x + 1")
ax.set_title("Two numbers make a line")
```

Two numbers: the 2 and the 1. Change either and see what happens.

```python exec
id: a-line-you-have-already-written-2
ax = axes()
for m in [2, 1, 0.5, 0, -1]:
    draw_line(ax, m, 1, label=f"m = {m}")
ax.set_title("Changing the first number tilts it")
```

```python exec
id: a-line-you-have-already-written-3
ax = axes()
for c in [4, 1, -2, -5]:
    draw_line(ax, 2, c, label=f"c = {c}")
ax.set_title("Changing the second number slides it")
```

Everything in this tutorial is about those two numbers and what you can do with them.

## Slope, as How Fast Something Changes

The first number has a name — the **slope** — and it is worth being careful about what it means, because the careless version costs you three tutorials later.

You will hear it called "rise over run". That is a way of remembering the calculation. The more useful description is a sentence about the world:

> **The slope answers: if x goes up by one, what happens to y?**

Here is that, computed from two points on a line.

```python exec
id: slope-as-how-fast-something-changes-1
def slope(p, q):
    """The slope of the line through two points, each given as (x, y)."""
    (x1, y1), (x2, y2) = p, q
    return (y2 - y1) / (x2 - x1)


a, b, c = (0, 1), (1, 3), (4, 9)

print("from a to b:", slope(a, b))
print("from b to c:", slope(b, c))
print("from a to c:", slope(a, c))
```

The same number, all three times, from three different pairs of points.

**That agreement is what "straight" means.** A line is straight precisely because the slope you measure does not depend on which two points you measure it between. If it did, the thing would be bending.

### A number about the world

The point of naming slope as a rate rather than as a ratio of gaps is that it survives leaving the graph.

```python exec
id: slope-as-how-fast-something-changes-2
# Hours worked, and pay received. No axes anywhere in sight.
records = [(0, 20), (5, 82.5), (12, 172), (20, 272)]

for i in range(len(records) - 1):
    print(f"between {records[i]} and {records[i+1]}:  {slope(records[i], records[i+1])} per hour")
```

The slope is the hourly rate. And the `20` at zero hours — the intercept — is whatever you get paid for turning up.

Nobody had to mention geometry for that to be useful.

### Your turn

A phone plan costs €15 a month plus 8 cent a minute. Write it as a line, plot it, and confirm that computing the slope from any two points on your plot gives you back the 8 cent.

```python exec
id: your-turn-1
# Your code here.
```

Hold on to the rate-of-change description. When [Rates of Change](tutorial:rates-of-change) arrives and asks for the slope of something that is *not* straight, it will be the same question with the answer changing as you move.

## Parallel and Perpendicular

Two lines are **parallel** when they never meet, and that needs no rule at all: they are parallel when they have the same slope.

```python exec
id: parallel-and-perpendicular-1
ax = axes()
draw_line(ax, 2, 1, label="y = 2x + 1")
draw_line(ax, 2, -4, label="y = 2x - 4")
draw_line(ax, -0.5, 1, label="y = -0.5x + 1")
ax.set_title("Two of these are parallel")
```

**Perpendicular** — meeting at a right angle — has a rule that is famously hard to believe:

> two lines are perpendicular when their slopes multiply to −1

Multiply to −1. Why would that be?

Do not take it on faith. Draw it.

```python exec
id: parallel-and-perpendicular-2
def slope_triangle(ax, x0, y0, run, rise, colour):
    """Draw the right triangle under a line: along by `run`, up by `rise`."""
    ax.plot([x0, x0 + run], [y0, y0], colour, linewidth=3)
    ax.plot([x0 + run, x0 + run], [y0, y0 + rise], colour, linewidth=3)
    ax.plot([x0, x0 + run], [y0, y0 + rise], colour, linewidth=1.5, linestyle="--")
    ax.annotate(f"run {run}", (x0 + run / 2, y0 - 0.6), ha="center", fontsize=8)
    ax.annotate(f"rise {rise}", (x0 + run + 0.3, y0 + rise / 2), fontsize=8)


ax = axes(6)
slope_triangle(ax, 0, 0, 3, 2, "tab:blue")
slope_triangle(ax, 0, 0, -2, 3, "tab:orange")
ax.set_title("The same triangle, turned a quarter turn")
```

Look at the two triangles. The second is the first, rotated by a right angle. And when you turn a triangle a quarter turn, **the run and the rise swap places, and one of them changes sign.**

Run 3, rise 2 becomes run −2, rise 3.

So the slopes are `2/3` and `3/−2`. Multiply them:

```python exec
id: parallel-and-perpendicular-3
first = 2 / 3
second = 3 / -2
print(first, "*", second, "=", first * second)
```

The rule is the picture written down. Swap two numbers and negate one of them, and the product of the before and after is always −1, because the swapping cancels and the negation is all that is left.

```python exec
id: parallel-and-perpendicular-4
ax = axes(6)
draw_line(ax, 2 / 3, 0, label="slope 2/3")
draw_line(ax, -3 / 2, 0, label="slope -3/2")
ax.set_title("And they do meet at a right angle")
```

### Your turn

Given the line `y = 4x − 1` and the point `(2, 3)`, find the line through that point at right angles to it. Plot both to check.

```python exec
id: your-turn-2
# Your code here.
```

## The Line That Breaks the Formula

Now try to draw the vertical line through `x = 3`.

Not a line that is very steep. A line that goes straight up.

```python exec
id: the-line-that-breaks-the-formula-1
ax = axes()
for m in [1, 3, 10, 50, 200]:
    draw_line(ax, m, -3 * m, label=f"m = {m}")
ax.set_title("Getting steeper, and never getting there")
```

Every one of those crosses the axis at 3 and leans a little closer to vertical. None of them is vertical, and no value of `m` will do it — you would need `y = mx + c` to produce a line where x never changes, and there is no slope that does that.

Try to compute one and the arithmetic says so.

```python exec
id: the-line-that-breaks-the-formula-2
def slope(p, q):
    (x1, y1), (x2, y2) = p, q
    return (y2 - y1) / (x2 - x1)


print(slope((3, 0), (3, 5)))
```

Divide by zero. The two points have the same x, so the run is nothing, and "how much does y change when x goes up by one" is a question with no answer — x never goes up by one on this line.

### The form that can

This is why the third way of writing a line exists:

**`ax + by + c = 0`**

It looks worse than `y = mx + c`, and for most lines it is worse. It earns its place on exactly one case.

```python exec
id: the-line-that-breaks-the-formula-3
def general_line(ax_, a, b, c, label=None):
    """Plot ax + by + c = 0, whatever a and b happen to be."""
    if b != 0:
        xs = [-10, 10]
        ax_.plot(xs, [(-a * x - c) / b for x in xs], label=label)
    else:
        # b = 0 means the line is vertical: x = -c/a, and y is anything.
        ax_.axvline(-c / a, label=label, color="tab:red")
    if label:
        ax_.legend(loc="upper left", fontsize=8)


ax = axes()
general_line(ax, 2, -1, 1, label="2x - y + 1 = 0  (that is y = 2x + 1)")
general_line(ax, 1, 0, -3, label="x - 3 = 0  (that is x = 3)")
ax.set_title("One form, both lines")
```

The vertical line is `1x + 0y − 3 = 0`. The `b` is zero, which is allowed, and it is what makes the whole thing possible: **`y = mx + c` has y on its own, so y must depend on x. The general form does not, so it does not have to.**

That is the entire reason this form is in the syllabus. Not tidiness, not tradition — it describes one more line than the other two can.

```python exec
id: the-line-that-breaks-the-formula-4
def to_general(m, c):
    """y = mx + c  becomes  mx - y + c = 0."""
    return (m, -1, c)


def to_slope_intercept(a, b, c):
    """ax + by + c = 0 becomes y = mx + c, when it can."""
    if b == 0:
        return "Vertical — this line has no slope-intercept form."
    return (-a / b, -c / b)


print(to_general(2, 1))
print(to_slope_intercept(2, -1, 1))
print(to_slope_intercept(1, 0, -3))
```

### Your turn

Convert these to `ax + by + c = 0`, and say which of them could not have been written as `y = mx + c`.

- The line through `(0, 4)` with slope `−2`
- The vertical line through `(−5, 0)`
- The horizontal line through `(0, 7)`

```python exec
id: your-turn-3
# Your answers here.
```

The third one is worth a moment: horizontal is fine in both forms, because a horizontal line has a slope — it is zero. Only vertical breaks.

## Midpoint, Which Needs No Theory

The halfway point between two points is the average of them. That is the whole of it.

```python exec
id: midpoint-which-needs-no-theory-1
def midpoint(p, q):
    (x1, y1), (x2, y2) = p, q
    return ((x1 + x2) / 2, (y1 + y2) / 2)


a, b = (1, 2), (7, 6)
m = midpoint(a, b)
print("midpoint of", a, "and", b, "is", m)

ax = axes(10)
ax.plot([a[0], b[0]], [a[1], b[1]], "-o", markersize=8)
ax.plot([m[0]], [m[1]], "o", markersize=10, color="tab:orange")
ax.annotate("midpoint", m, textcoords="offset points", xytext=(10, -12))
ax.set_title("Halfway is the average")
```

Average the x values, average the y values. It is the same "average" you used on marks in *Making Sense of Data*, done twice.

### Your turn

Two towns are at `(12, 40)` and `(48, 16)` on a map grid. A meeting point halfway between them — where?

And a harder one: the midpoint of a segment is `(3, 1)`, and one end of it is `(7, 4)`. Where is the other end?

```python exec
id: your-turn-4
# Your code here.
```

## How Far Apart, and the Theorem That Answers It

Two points. How far apart are they?

Start with the easy part. The horizontal gap and the vertical gap are just subtractions.

```python exec
id: how-far-apart-and-the-theorem-that-answers-it-1
a, b = (1, 2), (5, 5)

across = b[0] - a[0]
up = b[1] - a[1]
print("across:", across)
print("up:    ", up)
```

Four across and three up. But that is not how far apart they are — nobody walks four east and then three north and calls it four, or seven.

Try to get the direct distance and you will find you have no method.

```python exec
id: how-far-apart-and-the-theorem-that-answers-it-2
ax = axes(8)
ax.plot([a[0], b[0]], [a[1], b[1]], "-o", linewidth=2, markersize=8)
ax.annotate("A", a, textcoords="offset points", xytext=(-16, -6))
ax.annotate("B", b, textcoords="offset points", xytext=(8, 2))
ax.set_title("How long is that line?")
```

Now draw the two gaps as a triangle.

```python exec
id: how-far-apart-and-the-theorem-that-answers-it-3
ax = axes(8)
ax.plot([a[0], b[0]], [a[0] * 0 + a[1], a[1]], color="tab:orange", linewidth=3)
ax.plot([b[0], b[0]], [a[1], b[1]], color="tab:green", linewidth=3)
ax.plot([a[0], b[0]], [a[1], b[1]], color="tab:blue", linewidth=2)
ax.annotate("4 across", (3, 1.4), color="tab:orange")
ax.annotate("3 up", (5.2, 3.5), color="tab:green")
ax.annotate("?", (2.8, 3.8), color="tab:blue", fontsize=14)
ax.set_title("The gaps make a right-angled triangle")
```

The distance you want is the long side of a right-angled triangle whose short sides you already know.

And there is a rule for that, which you may have met before without a reason for it:

> **In a right-angled triangle, the two short sides squared, added together, give the long side squared.**

That is the Pythagorean theorem. `3² + 4² = 9 + 16 = 25`, and `√25 = 5`.

```python exec
id: how-far-apart-and-the-theorem-that-answers-it-4
import math

def distance(p, q):
    (x1, y1), (x2, y2) = p, q
    across = x2 - x1
    up = y2 - y1
    return math.sqrt(across ** 2 + up ** 2)


print(distance((1, 2), (5, 5)))
print(distance((0, 0), (3, 4)))
print(distance((0, 0), (1, 1)))
```

**The distance formula and Pythagoras are the same thing seen from two directions.** Neither is a special case of the other. You wanted a distance, you drew the triangle the two gaps make, and the theorem is the answer to the question you were already asking.

That is worth having in that order. Taught the other way round — theorem first, distance as an application — Pythagoras is a fact to accept and the formula is a second thing to remember.

### Checking it

```python exec
id: how-far-apart-and-the-theorem-that-answers-it-5
# A triangle with sides 3, 4, 5 — check the theorem directly.
for a_side, b_side in [(3, 4), (5, 12), (8, 15), (1, 1), (2.5, 6)]:
    c_side = math.sqrt(a_side ** 2 + b_side ** 2)
    print(f"{a_side}^2 + {b_side}^2 = {a_side**2 + b_side**2:>7.2f}"
          f"    and c^2 = {c_side ** 2:>7.2f}    so c = {c_side:.4f}")
```

### Your turn

Three points: `(0, 0)`, `(6, 0)` and `(3, 4)`. Is the triangle they make isosceles — that is, does it have two sides the same length?

```python exec
id: your-turn-5
# Your code here.
```

## Where You Will Meet This Again

One last picture, and nothing is being taught by it.

```python exec
id: where-you-will-meet-this-again-1
import math

ax = axes(2)
points = [(math.cos(t / 60 * 2 * math.pi), math.sin(t / 60 * 2 * math.pi))
          for t in range(61)]
ax.plot([p[0] for p in points], [p[1] for p in points], linewidth=2)
ax.set_title("Every point on this is distance 1 from the centre")
```

```python exec
id: where-you-will-meet-this-again-2
# Check that claim on a few of them.
for t in [0, 7, 15, 33, 48]:
    p = points[t]
    print(f"({p[0]:>6.3f}, {p[1]:>6.3f})   distance from origin: {distance((0, 0), p):.6f}")
```

Exactly 1, every time, by the formula you just wrote.

That circle is where [The Unit Circle](tutorial:the-unit-circle) starts, and the fact that every point on it is distance 1 from the centre is the only rule that whole tutorial rests on.

## Reflection

Two questions, and both of them turned out to be about the same right-angled triangle.

**A line has three descriptions and you now have all three.** A function, which is what you had; `y = mx + c`, which names the two numbers; and `ax + by + c = 0`, which exists because it can describe a vertical line and the other two cannot.

**Slope is a rate of change.** How much y moves when x moves by one. Keep that phrasing — it is the one the derivative needs.

**The perpendicular rule is a picture.** Turn the triangle a quarter turn, the rise and run swap, one of them goes negative, and the product is −1.

**Distance is Pythagoras, and Pythagoras is distance.** You did not learn a theorem and apply it; you asked how far apart two things were and the theorem is what the answer looks like.

Write a few sentences: of the three ways to write a line, which would you use to describe the edge of a building on a map, and why?

## Where to Read More

Khan Academy. *Proof: Perpendicular Lines Have Negative Reciprocal Slope.*
<https://www.youtube.com/watch?v=HyThzLRuqXo>. The same quarter-turn
picture this page draws, proved a second way.
