---
title: "Straight lines: slope, midpoint and distance"
year: "2026-2027"
version: 2026.09.24.1
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

# Straight lines: slope, midpoint and distance

This page is about two questions:

- How do we describe a line?
- How far apart are two points?

Both questions sound easy. The first one has three different answers,
and each answer is better than the others at something. The answer to
the second one is a theorem you may have heard of. Here it comes from a
direction that makes it make sense.

The course plan calls this topic "coordinate geometry". For many
people, geometry means something they did at school with a compass,
and did not enjoy. There is no compass here. There is a pair of axes,
which we have used since
[Charts: choosing the right chart for your data](tutorial:pictures-worth-numbers),
and there are two questions.

On this page we:

- look again at the two numbers that make a straight line
- see slope as a rate: how fast one thing changes when another does
- find when two lines are parallel, and when they meet at a right angle
- meet the one line that $y = mx + c$ cannot describe, and a form that can
- find the point halfway between two points
- find the distance between two points, and see Pythagoras' theorem
  appear

## A line you have already written

We have written straight lines as functions since
[Functions and their graphs](tutorial:drawing-functions). Here is one
again.

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

The line $y = 2x + 1$ has two numbers in it, 2 and 1. What happens when
we change each one? The next two cells change them one at a time.

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

Changing the first number tilts the line. Changing the second number
slides it up or down. Everything on this page is about those two
numbers, and what we can do with them.

## Slope, as how fast something changes

The first number, $m$, is the slope, which we met in
[Functions and their graphs](tutorial:drawing-functions). It is worth
being careful about what the slope means. We will need the careful
meaning later, in
[Derivatives: the rate of change of a curve](tutorial:rates-of-change).

You may hear slope called "rise over run". That phrase helps us
remember the calculation. A sentence about the world is more useful:

> **The slope answers the question: if $x$ goes up by one, how much does
> $y$ change?**

To find the slope from two points, we divide the change in $y$ by the
change in $x$:

$$m = \frac{y_2 - y_1}{x_2 - x_1}$$

For example, from $(0, 1)$ to $(1, 3)$, $y$ goes up by 2 while $x$ goes
up by 1, so the slope is $2 \div 1 = 2$.

The next cell finds the slope between three different pairs of points on
the line $y = 2x + 1$. Do you expect three different answers, or the
same one?

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

We get the same number all three times, from three different pairs of
points.

**That agreement is what "straight" means.** A line is straight because
its slope is the same between any two of its points. If the slope
changed from one pair to another, the line would be bending.

### A number about the world

Why describe slope as a rate, and not as a picture of a triangle on a
graph? Because a rate still makes sense away from the graph.

Here are four records of hours worked and the pay received. What will
the slope between each pair mean?

```python exec
id: slope-as-how-fast-something-changes-2
# Hours worked, and pay received. No axes anywhere in sight.
records = [(0, 20), (5, 82.5), (12, 170), (20, 270)]

for i in range(len(records) - 1):
    print(f"between {records[i]} and {records[i+1]}:  {slope(records[i], records[i+1])} per hour")
```

The slope is the hourly rate: €12.50 per hour. The 20 at zero hours is
the intercept. It is the amount you are paid for arriving, before you
work any hours at all.

We did not need any geometry for that to be useful.

### Your turn

A phone plan costs €15 a month, plus 8 cent a minute.

1. Write the cost as a line, $y = mx + c$. What are $m$ and $c$?
2. Plot the line.
3. Pick any two points on your line, and compute the slope between them.
   Do you get 8 cent back?

```python exec
id: your-turn-1
# Your code here.
```

Keep the "rate of change" meaning in mind. In
[Derivatives: the rate of change of a curve](tutorial:rates-of-change)
we ask for the slope of something that is *not* straight. It is the
same question, but the answer changes as we move along the curve.

## Parallel and perpendicular

Two lines are *parallel* when they go in the same direction and never
meet. The rule for this is short: two different lines are parallel when
they have the same slope.

Which two of these three lines are parallel?

```python exec
id: parallel-and-perpendicular-1
ax = axes()
draw_line(ax, 2, 1, label="y = 2x + 1")
draw_line(ax, 2, -4, label="y = 2x - 4")
draw_line(ax, -0.5, 1, label="y = -0.5x + 1")
ax.set_title("Two of these are parallel")
```

Two lines are *perpendicular* when they meet at a right angle. The rule
for perpendicular lines surprises many people:

> Two lines are perpendicular when their slopes multiply to $-1$.

For example, slopes 2 and $-\tfrac{1}{2}$ give $2 \times (-\tfrac{1}{2}) = -1$,
so those two lines are perpendicular.

The rule needs both lines to have a slope. A vertical line has no slope,
as we will see in the next section. A vertical line and a flat line are
also perpendicular.

Why would the slopes multiply to $-1$? Let's not take it on trust.
Let's draw it.

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

Look at the two triangles. The second one is the first one, turned
through a right angle (a quarter turn). What happens to the run and the
rise?

**When we turn a triangle a quarter turn, the run and the rise swap
places, and one of them changes sign.** Run 3 and rise 2 become run
$-2$ and rise 3.

So the slopes are $\tfrac{2}{3}$ and $\tfrac{3}{-2}$. What do you get
when you multiply them? Run the cell to check.

```python exec
id: parallel-and-perpendicular-3
first = 2 / 3
second = 3 / -2
print(first, "*", second, "=", first * second)
```

The rule is the picture, written down. The two numbers swap, so they
cancel when we multiply: $\tfrac{2}{3} \times \tfrac{3}{2} = 1$. The
change of sign is all that is left, and that makes $-1$.

Here are the two lines, drawn in full. Do they meet at a right angle?

```python exec
id: parallel-and-perpendicular-4
ax = axes(6)
draw_line(ax, 2 / 3, 0, label="slope 2/3")
draw_line(ax, -3 / 2, 0, label="slope -3/2")
ax.set_title("And they do meet at a right angle")
```

### Your turn

Here is the line $y = 4x - 1$ and the point $(2, 3)$.

1. What slope does a line at right angles to $y = 4x - 1$ have?
2. Find the line with that slope that passes through $(2, 3)$.
3. Plot both lines to check.

```python exec
id: your-turn-2
# Your code here.
```

## The line that breaks the formula

Now let's try to draw the vertical line through $x = 3$. This line goes
straight up. It is not only very steep.

The cell draws lines that get steeper and steeper. Can any of them be
vertical?

```python exec
id: the-line-that-breaks-the-formula-1
ax = axes()
for m in [1, 3, 10, 50, 200]:
    draw_line(ax, m, -3 * m, label=f"m = {m}")
ax.set_title("Getting steeper, and never getting there")
```

Every one of those lines crosses the horizontal axis at 3, and each one
is a little closer to vertical. None of them is vertical, and no value
of $m$ will make one. On a vertical line, $x$ never changes, and
$y = mx + c$ cannot make a line like that.

What happens if we try to compute the slope of the vertical line?

```python exec
id: the-line-that-breaks-the-formula-2
def slope(p, q):
    (x1, y1), (x2, y2) = p, q
    return (y2 - y1) / (x2 - x1)


print(slope((3, 0), (3, 5)))
```

Python gives a `ZeroDivisionError`. The two points have the same $x$,
so the run is zero, and we cannot divide by zero. The slope asks "how
much does $y$ change when $x$ goes up by one?" On this line, $x$ never
goes up by one, so the question has no answer.

### The form that can

This is why a third way of writing a line exists. The *general form* of
a line is

$$ax + by + c = 0$$

For most lines it looks worse than $y = mx + c$, and it is worse. We
need it for one case.

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

The vertical line is $1x + 0y - 3 = 0$. Here $b$ is zero. That is
allowed, and it is what makes the vertical line possible.

In $y = mx + c$, $y$ is on its own, so $y$ must depend on $x$. The
general form does not have $y$ on its own, so $y$ does not have to
depend on $x$.

This is the main reason we need the general form here. It describes one
kind of line that the other two ways cannot: a vertical line.

The next cell turns one form into the other, when that is possible. What
do you expect for the vertical line, $(1, 0, -3)$?

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

Here are three lines:

- the line through $(0, 4)$ with slope $-2$
- the vertical line through $(-5, 0)$
- the horizontal line through $(0, 7)$

1. Write each one in the form $ax + by + c = 0$.
2. Which of them could not be written as $y = mx + c$?

```python exec
id: your-turn-3
# Your answers here.
```

The third line is worth a moment. A horizontal line works in both forms,
because it has a slope: its slope is zero. Only a vertical line breaks
$y = mx + c$.

## Midpoint, which needs no theory

The *midpoint* of two points is the point halfway between them. It is
the average of the two points. We average the $x$ values, and we
average the $y$ values:

$$\text{midpoint} = \left(\frac{x_1 + x_2}{2}, \frac{y_1 + y_2}{2}\right)$$

For example, the midpoint of $(1, 2)$ and $(7, 6)$ is
$\left(\frac{1 + 7}{2}, \frac{2 + 6}{2}\right) = (4, 4)$.

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

This is the same average we used for marks in
[Statistics: averages, spread and frequency](tutorial:making-sense-of-data),
done twice: once for $x$ and once for $y$.

### Your turn

1. Two towns are at $(12, 40)$ and $(48, 16)$ on a map grid. Where is
   the meeting point halfway between them?
2. A harder one: the midpoint of a line segment is $(3, 1)$, and one end
   of it is $(7, 4)$. Where is the other end?

```python exec
id: your-turn-4
# Your code here.
```

## How far apart, and the theorem that answers it

Here are two points. How far apart are they?

Let's start with the easy part. The gap across and the gap up are each
one subtraction.

```python exec
id: how-far-apart-and-the-theorem-that-answers-it-1
a, b = (1, 2), (5, 5)

across = b[0] - a[0]
up = b[1] - a[1]
print("across:", across)
print("up:    ", up)
```

The gaps are 4 across and 3 up. But neither of those is the distance
between the points. If you walk 4 east and then 3 north, you walk 7 in
total. The straight line from start to finish is shorter than 7, and
longer than 4.

How long is the straight line? Can you think of a way to work it out?

```python exec
id: how-far-apart-and-the-theorem-that-answers-it-2
ax = axes(8)
ax.plot([a[0], b[0]], [a[1], b[1]], "-o", linewidth=2, markersize=8)
ax.annotate("A", a, textcoords="offset points", xytext=(-16, -6))
ax.annotate("B", b, textcoords="offset points", xytext=(8, 2))
ax.set_title("How long is that line?")
```

Now let's draw the two gaps as well. What shape do they make with the
line?

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

The two gaps and the line make a right-angled triangle. The distance we
want is the long side of that triangle, and we already know the two
short sides.

There is a rule for this. You may have met it before, perhaps without a
reason for it. The *Pythagorean theorem* (Pythagoras' theorem) says:

> **In a right-angled triangle, square the two short sides and add them.
> The result is the square of the long side.**

$$a^2 + b^2 = c^2$$

Here $c$ is the long side. For our triangle,
$3^2 + 4^2 = 9 + 16 = 25$, and $\sqrt{25} = 5$. So the two points are 5
apart.

Written with coordinates, this is the *distance formula*:

$$d = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}$$

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

**The distance formula and Pythagoras' theorem are the same thing, seen
from two directions.** Neither one is a special case of the other. We
wanted a distance. We drew the triangle that the two gaps make. The
theorem is the answer to the question we were already asking.

The order matters. If we learn the theorem first and the distance
second, the theorem is a fact to accept, and the formula is a second
thing to remember. In this order, they are one idea.

### Checking it

Does $a^2 + b^2$ always equal $c^2$? The cell tries five triangles.

```python exec
id: how-far-apart-and-the-theorem-that-answers-it-5
# A triangle with sides 3, 4, 5 — check the theorem directly.
for a_side, b_side in [(3, 4), (5, 12), (8, 15), (1, 1), (2.5, 6)]:
    c_side = math.sqrt(a_side ** 2 + b_side ** 2)
    print(f"{a_side}^2 + {b_side}^2 = {a_side**2 + b_side**2:>7.2f}"
          f"    and c^2 = {c_side ** 2:>7.2f}    so c = {c_side:.4f}")
```

### Your turn

Here are three points: $(0, 0)$, $(6, 0)$ and $(3, 4)$. They make a
triangle.

A triangle is *isosceles* when two of its sides have the same length.

1. Use `distance` to find the length of each side.
2. Is the triangle isosceles?

```python exec
id: your-turn-5
# Your code here.
```

## Where you will meet this again

Here is one last picture. It does not teach anything new. It shows
where this page leads.

The cell uses `math.cos` and `math.sin` to place 61 points around a
circle. We meet these two functions properly on the next page. Here we
only need the points.

```python exec
id: where-you-will-meet-this-again-1
import math

ax = axes(2)
points = [(math.cos(t / 60 * 2 * math.pi), math.sin(t / 60 * 2 * math.pi))
          for t in range(61)]
ax.plot([p[0] for p in points], [p[1] for p in points], linewidth=2)
ax.set_title("Every point on this is distance 1 from the center")
```

Is every point on this circle really 1 away from the centre? Let's
check a few with our `distance` function.

```python exec
id: where-you-will-meet-this-again-2
# Check that claim on a few of them.
for t in [0, 7, 15, 33, 48]:
    p = points[t]
    print(f"({p[0]:>6.3f}, {p[1]:>6.3f})   distance from origin: {distance((0, 0), p):.6f}")
```

The distance is 1 every time, from the formula we wrote above.

That circle is where
[The unit circle: sine, cosine and tangent](tutorial:the-unit-circle)
starts. That whole page rests on one fact: every point on the circle is
1 away from the centre.

## Reflection

We started with two questions, and both of them turned out to be about
the same right-angled triangle.

Here are four ideas to take with you.

**A line has three descriptions, and now you have all three.**

| Form | What it is good for |
|---|---|
| a Python function | drawing and computing, as in [Functions and their graphs](tutorial:drawing-functions) |
| $y = mx + c$ | naming the slope and the intercept |
| $ax + by + c = 0$ | describing every line, including a vertical line |

**Slope is a rate of change.** It is how much $y$ changes when $x$ goes
up by one. Keep that meaning: derivatives need it.

**The perpendicular rule is a picture.** Turn the slope triangle a
quarter turn. The rise and the run swap, one of them changes sign, and
the product of the two slopes is $-1$.

**Distance is Pythagoras' theorem, and Pythagoras' theorem is
distance.** We did not learn a theorem and then apply it. We asked how
far apart two points were, and the theorem is what the answer looks
like.

Think about the three ways to write a line. Which one would you use to
describe the edge of a building on a map, and why? Write a few
sentences.

## Where to Read More

Khan Academy. *Proof: Perpendicular Lines Have Negative Reciprocal Slope.*
<https://www.youtube.com/watch?v=HyThzLRuqXo>. The same quarter-turn
picture this page draws, proved a second way.
