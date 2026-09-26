---
title: "Straight lines: slope, and the line that breaks the formula"
year: "2026-2027"
version: 2026.09.26.1
covers:
  slope-as-how-fast-something-changes:
    covers: [MIT-4.2]
  slope-in-your-world:
    covers: [MIT-4.2]
  parallel-and-perpendicular:
    covers: [MIT-4.2]
  the-line-that-breaks-the-formula:
    covers: [MIT-4.1]
worlds:
  sea-and-sky: Submarines, ships and weather balloons. The numbers are made up.
  sound: Thunder, echoes and the speed of sound.
  planets-and-moons: Spacecraft, the Moon and the distances between them.
  fantasy-maps: A made-up kingdom and its straight roads. The numbers are made up.
---

# Straight lines: slope, and the line that breaks the formula

Here is a straight line, drawn by a Python function. The line
$y = 2x + 1$ has two numbers in it, 2 and 1. What does each number do to
the line? The first cell draws it, and the two cells after it change one
number at a time.

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

`draw_line` is the `plot_line` from
[Functions and their graphs](tutorial:drawing-functions), with a label
and a line style added.

```python exec
id: a-line-you-have-already-written-2
ax = axes()
for m in [2, 1, 0.5, 0, -1]:
    draw_line(ax, m, 1, label=f"m = {m}")
ax.set_title("Changing the first number")
```

```python exec
id: a-line-you-have-already-written-3
ax = axes()
for c in [4, 1, -2, -5]:
    draw_line(ax, 2, c, label=f"c = {c}")
ax.set_title("Changing the second number")
```

Changing the first number tilts the line. Changing the second number
slides it up or down. This page is about those two numbers, what they
mean, and the one line they cannot describe.

On this page we:

- see slope as a rate: how fast one thing changes when another does
- find when two lines are parallel, and when they meet at a right angle
- meet the one line that $y = mx + c$ cannot describe, and a form that
  can

## Slope, as how fast something changes

The first number, $m$, is the slope, which we met in
[Functions and their graphs](tutorial:drawing-functions). We need to be
careful about what the slope means, because
[Derivatives: the rate of change of a curve](tutorial:rates-of-change)
uses this meaning.

You may hear slope called "rise over run". That phrase helps us
remember the calculation. A sentence about the world helps more:

> **The slope answers the question: if $x$ goes up by one, how much does
> $y$ change?**

To find the slope from two points, we divide the change in $y$ by the
change in $x$:

$$m = \frac{y_2 - y_1}{x_2 - x_1}$$

For example, from $(0, 1)$ to $(1, 3)$, $y$ goes up by 2 while $x$ goes
up by 1, so the slope is $2 \div 1 = 2$.

The next cell finds the slope between three different pairs of points on
the line $y = 2x + 1$.

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

```predict
type: number

The first line prints 2.0. The pair from $a$ to $c$ is further apart
than the pair from $a$ to $b$. What will the last line print?
```

We get 2.0 all three times, from three different pairs of points.

**A line is straight when its slope is the same between any two of its
points.** If the slope changed from one pair to another, the line would
bend.

### A number about the world

Why describe slope as a rate, and not as a triangle on a graph? Because
a rate still makes sense away from the graph.

A submarine dives at a steady rate. Here are four readings of the time,
in minutes, and its depth, in metres. What will the slope between each
pair of readings mean?

```python exec
id: slope-as-how-fast-something-changes-2
# Minutes since the clock started, and the depth in metres.
readings = [(0, 20), (5, 95), (12, 200), (20, 320)]

for i in range(len(readings) - 1):
    print(f"between {readings[i]} and {readings[i + 1]}:",
          slope(readings[i], readings[i + 1]), "metres per minute")
```

The slope is the rate of the dive: 15 metres deeper every minute. The 20
at zero minutes is the intercept, where the line crosses the vertical
axis. Here it is the depth when the clock started. So the depth after
$x$ minutes is $y = 15x + 20$.

We needed no picture for that to be useful.

## Slope in your world

Keep the "rate of change" meaning in mind. In
[Derivatives: the rate of change of a curve](tutorial:rates-of-change)
we ask for the slope of something that is *not* straight. It is the same
question, but the answer changes as we move along the curve.

<div class="dl-world" data-world="sea-and-sky">

A weather balloon is let go from a hill 50 m high. It rises at a steady
rate. After 2 minutes it is 650 m up, and after 5 minutes it is 1550 m
up. Can you find its slope and its intercept, and write
`height(minutes)`? Weather balloons usually burst at about 30 km, which
is 30,000 m. When will this one get there, if it keeps rising at the
same rate? Keep that time, in minutes, as `burst`.

```python exec
id: slope-in-your-world-1--sea-and-sky
readings = [(0, 50), (2, 650), (5, 1550)]    # minutes, and metres up
```

```hint
The slope is the number of metres the balloon rises in one minute.
Which reading tells you the intercept straight away?
```

```inputs
height(0)
height(10)
burst
```

```solution
m = slope(readings[0], readings[1])
c = 50


def height(minutes):
    return m * minutes + c


burst = (30000 - c) / m
print("slope", m, "and intercept", c)
print("it reaches 30,000 m after", burst, "minutes")
---
The balloon rises 300 m every minute, so $y = 300x + 50$. It gets to
30,000 m after about 99.8 minutes, a little under an hour and three
quarters. To find that, subtract the 50 m it started with, then divide
by the rate.
```

</div>

<div class="dl-world" data-world="sound">

Sound travels about 343 metres every second in air at 20 °C. The light
from a flash of lightning reaches you almost at once, and the thunder
takes longer. Can you write `storm_distance(seconds)`, the distance to
the storm in metres when you count that many seconds between the flash
and the thunder? What are $m$ and $c$ for this line? Many people say
"count the seconds, and divide by 3 to get kilometres". How close is
that?

```python exec
id: slope-in-your-world-1--sound
speed_of_sound = 343    # metres every second, in air at 20 °C
```

```hint
After 0 seconds, how far has the sound gone? After 1 second? That gives
you $c$ and $m$.
```

```inputs
storm_distance(0)
storm_distance(3)
storm_distance(6)
```

```solution
def storm_distance(seconds):
    return speed_of_sound * seconds


print(storm_distance(3), "metres after 3 seconds")
print(storm_distance(6), "metres after 6 seconds")
---
The line is $y = 343x + 0$. The slope is the speed, and the intercept
is 0, because the sound has gone nowhere when you start counting. Three
seconds gives 1029 m, which is very close to 1 km. So "divide by 3" is
very close.
```

</div>

<div class="dl-world" data-world="planets-and-moons">

The spacecraft Voyager 1 is moving away from the Sun at about 17 km
every second. Can you write its journey as a line, with the time in
days? Its slope is the number of kilometres it goes in one day. Write
`travelled(days)`. The Moon is about 384,400 km from the Earth. How
many hours would Voyager 1 take to go that far? Keep that as
`hours_to_moon`.

```python exec
id: slope-in-your-world-1--planets-and-moons
km_each_second = 17
```

```hint
How many seconds are there in one day? Multiply them out, one step at a
time: seconds in a minute, minutes in an hour, hours in a day.
```

```inputs
travelled(1)
travelled(365)
hours_to_moon
```

```solution
per_day = km_each_second * 60 * 60 * 24


def travelled(days):
    return per_day * days


hours_to_moon = 384400 / km_each_second / 3600
print(per_day, "km every day")
print(hours_to_moon, "hours to go as far as the Moon")
---
The slope is 1,468,800 km a day, and the intercept is 0, since we
measure from now. In a year that is over 536 million km. It would go as
far as the Moon in about 6.3 hours. The Apollo astronauts took about
three days, because they were much slower.
```

</div>

<div class="dl-world" data-world="fantasy-maps">

An old road runs straight from the mill at $(-4, 1)$ to the castle at
$(4, 5)$, in kilometres on the kingdom's map. Can you find its slope
and its intercept? Then write `on_the_road(point)`, which says whether
a place is on the road. Is the well at $(10, 8)$ on the road? What
about the tower at $(6, 7)$?

```python exec
id: slope-in-your-world-1--fantasy-maps
mill, castle = (-4, 1), (4, 5)
```

```hint
Once you have the slope $m$, put the mill's $x$ and $y$ into
$y = mx + c$. Which value of $c$ makes it true?

A place is on the road when its $y$ is exactly $mx + c$. Floats are not
always exact, so a tiny difference, such as `1e-9`, is safer than `==`.
```

```inputs
on_the_road((10, 8))
on_the_road((6, 7))
on_the_road((0, 3))
```

```solution
m = slope(mill, castle)
c = mill[1] - m * mill[0]


def on_the_road(point):
    x, y = point
    return abs(m * x + c - y) < 1e-9


print("slope", m, "and intercept", c)
---
The road is $y = 0.5x + 3$. The well is on it, because
$0.5 \times 10 + 3 = 8$. The tower is not. At $x = 6$ the road is at 6,
one kilometre south of the tower.
```

</div>

## Parallel and perpendicular

Two lines are *parallel* when they go in the same direction and never
meet. The rule is short. Two different lines are parallel when they
have the same slope.

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

Why would the slopes multiply to $-1$? Let's draw it and see.

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
when you multiply them?

```python exec
id: parallel-and-perpendicular-3
first = 2 / 3
second = 3 / -2
print(first, "*", second, "=", first * second)
```

```predict
type: number

What will the product of the two slopes be?
```

The 2 and the 3 swap places, so they cancel when we multiply:
$\tfrac{2}{3} \times \tfrac{3}{2} = 1$. Only the change of sign is left,
and that makes $-1$.

Here are the two lines, drawn in full. Do they meet at a right angle?

```python exec
id: parallel-and-perpendicular-4
ax = axes(6)
draw_line(ax, 2 / 3, 0, label="slope 2/3")
draw_line(ax, -3 / 2, 0, label="slope -3/2")
ax.set_title("Two lines, one quarter turn apart")
```

You may remember the quarter turn from
[Complex numbers: roots that are not real](tutorial:complex-roots#multiplying-by-i),
where multiplying by $i$ turned a point a quarter of the way round. It
is the same move: $(x, y)$ becomes $(-y, x)$.

### Your turn

Here is the line $y = 4x - 1$ and the point $(2, 3)$. What slope does a
line at right angles to $y = 4x - 1$ have? Which line with that slope
passes through $(2, 3)$?

Can you write `perpendicular_through(m, point)`? It returns the slope
and the intercept of the line at right angles to a line of slope `m`,
through `point`. Draw both lines to see them meet.

```python exec
id: your-turn-2
def perpendicular_through(m, point):
    """The slope and intercept of the line at right angles to slope m,
    through point."""
    # Your code here.
```

```hint
Which slope multiplies with 4 to give $-1$? Once you have the slope,
which value of $c$ puts $(2, 3)$ on the line?
```

```hint
after: 3 errors
title: The steps

1. The new slope is $-1$ divided by `m`.
2. The point is on the line, so $y = \text{new slope} \times x + c$.
   Subtract the slope times $x$ from $y$ to find $c$.
3. Return the two numbers.

What should happen when `m` is 0? The line at right angles to a flat
line is vertical.
```

```inputs
perpendicular_through(4, (2, 3))
perpendicular_through(-0.5, (0, 1))
perpendicular_through(0, (1, 1))     # a flat line
```

```solution
def perpendicular_through(m, point):
    """The slope and intercept of the line at right angles to slope m,
    through point."""
    x, y = point
    new_m = -1 / m
    return new_m, y - new_m * x
---
The line at right angles to $y = 4x - 1$ through $(2, 3)$ is
$y = -0.25x + 3.5$. For a flat line, `m` is 0, and $-1 \div 0$ stops
with a `ZeroDivisionError`. The line at right angles to a flat line is
vertical, and the next section is about that line.
```

## The line that breaks the formula

On a ship's chart, north is up. A ship that sails due north keeps the
same across value, so its course is a vertical line. Let's try to draw
the vertical line through $x = 3$.

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

What happens if we compute the slope between two points on the vertical
line?

```python exec
id: the-line-that-breaks-the-formula-2
print(slope((3, 0), (3, 5)))
```

```predict
type: choice

What will the cell do?

- Print a very big number
  - The lines above got steeper and steeper, so a vertical line sounds
    like the steepest of all.
- Print 0
  - $x$ does not change at all, so the slope could be nothing.
- Stop with an error
```

Python stops with a `ZeroDivisionError`. The two points have the same
$x$, so the run is zero, and we cannot divide by zero. The slope asks
"how much does $y$ change when $x$ goes up by one?" On this line, $x$
never goes up by one, so the question has no answer.

### The form that can

This is why a third way of writing a line exists. The *general form* of
a line is

$$ax + by + c = 0$$

For most lines it is harder to read than $y = mx + c$. We need it for
one case.

```python exec
id: the-line-that-breaks-the-formula-3
def general_line(ax_, a, b, c, label=None):
    """Plot ax + by + c = 0, whatever a and b are."""
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

The vertical line is $1x + 0y - 3 = 0$. Here $b$ is zero. The general
form allows that, and that is what makes the vertical line possible.

In $y = mx + c$, $y$ is on its own, so $y$ must depend on $x$. The
general form does not have $y$ on its own, so $y$ does not have to
depend on $x$.

The next cell changes one form into the other, when that is possible.
What do you expect for the vertical line, $(1, 0, -3)$?

```python exec
id: the-line-that-breaks-the-formula-4
def to_general(m, c):
    """y = mx + c  becomes  mx - y + c = 0."""
    return (m, -1, c)


def to_slope_intercept(a, b, c):
    """ax + by + c = 0 becomes y = mx + c, when it can."""
    if b == 0:
        return "Vertical: this line has no slope-intercept form."
    return (-a / b, -c / b)


print(to_general(2, 1))
print(to_slope_intercept(2, -1, 1))
print(to_slope_intercept(1, 0, -3))
```

### Your turn, on paper

Here are three lines:

- the line through $(0, 4)$ with slope $-2$
- the vertical line through $(-5, 0)$
- the horizontal line through $(0, 7)$

Can you write each one in the form $ax + by + c = 0$? Which of them
could not be written as $y = mx + c$? Check your answers with
`to_slope_intercept`.

```python exec
id: your-turn-3
# Your three lines as (a, b, c), then a check with to_slope_intercept.
```

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Yours may be different and work too. Any line can
be multiplied through by a number, so $4x + 2y - 8 = 0$ is the same
line as the first one here.

1. $y = -2x + 4$ becomes $2x + y - 4 = 0$, which is `(2, 1, -4)`.
2. The vertical line is $x + 5 = 0$, which is `(1, 0, 5)`.
3. The horizontal line is $y - 7 = 0$, which is `(0, 1, -7)`.

Only the vertical line could not be written as $y = mx + c$. The
horizontal line works in both forms, because it has a slope. Its slope
is zero.

</details>

## Looking back

A line has three descriptions:

| Form | What it is good for |
|---|---|
| a Python function | drawing and computing, as in [Functions and their graphs](tutorial:drawing-functions) |
| $y = mx + c$ | naming the slope and the intercept |
| $ax + by + c = 0$ | describing every line, including a vertical line |

Think about the three ways to write a line. Which one would you use to
describe the edge of a building on a map, and why?

A challenge: two lines in the general form meet at one point, unless
they are parallel. Can you write `where_they_meet(first, second)` for
two lines given as `(a, b, c)`? It should work when one of the lines is
vertical. What should it return for two parallel lines?
[Solving equations: linear, quadratic and simultaneous](tutorial:cracking-equations)
solved a pair of lines by elimination, and that method works here too.

```python challenge
def where_they_meet(first, second):
    """Where two lines ax + by + c = 0 cross. Each line is (a, b, c)."""
    # Your code here.


print(where_they_meet((2, -1, 1), (1, 0, -3)))    # y = 2x + 1 and x = 3
print(where_they_meet((2, -1, 1), (2, -1, -4)))   # two parallel lines
```

## Where to read more

Khan Academy. *Proof: Perpendicular Lines Have Negative Reciprocal Slope.*
<https://www.youtube.com/watch?v=HyThzLRuqXo>. This video uses the same
quarter-turn picture as this page, and proves the rule a second way.

Stand-up Maths (2015). *NYC: The Linear Equation of Broadway.*
<https://www.youtube.com/watch?v=Quwvw0vYkRA>. Matt Parker walks along
Broadway in New York with graph paper, and finds the straight line that
fits it, slope and all. It is eleven minutes long.
