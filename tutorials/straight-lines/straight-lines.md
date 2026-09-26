---
title: "Straight lines: slope and gradient"
year: "2026-2027"
version: 2026.09.26.2
covers:
  how-steep-is-a-ramp:
    covers: [MIT-4.2]
    touches: [MIT-1.7]
  the-rule-for-a-ramp:
    covers: [MIT-4.2]
    touches: [PDP-LO6, MIT-1.7]
  slope-between-any-two-points:
    covers: [MIT-4.2]
    touches: [PDP-LO8, PDP-LO10]
  a-wall-has-no-slope:
    covers: [MIT-4.2]
    touches: [PDP-LO9]
  a-line-as-a-rule-y-mx-c:
    covers: [MIT-4.1]
    touches: [MIT-3.1, PDP-LO8]
  every-line-at-once-ax-by-c-0:
    covers: [MIT-4.1]
    touches: [MIT-1.7]
  parallel-and-perpendicular:
    covers: [MIT-4.2]
---

# Straight lines: slope and gradient

A community hall has one step at its front door, 30 cm high. The
committee buys a ramp that reaches 3 metres out from the door. It is ten
times longer than the step is high. That sounds gentle. A wheelchair user
tries it and says it is too steep. Is it? And how would you
measure "too steep" at all?

The answer comes from a real Irish rule, one division and one `if`,
and I think it is a surprise.

On this page we:

- measure a ramp's steepness as rise over run, and check it against
  the Irish guidance
- find the slope between two points, and add `slope` to the toolkit
- meet a line with no slope
- write a line as $y = mx + c$, and find it with `line_through`
- write every line as $ax + by + c = 0$
- tell parallel and perpendicular lines from their slopes

> **The space we're in.** A flat plane with two axes at right angles:
> $x$ across and $y$ up. A point is an $(x, y)$ pair, which Python keeps
> as a tuple, like `(3, 0.3)`. Both axes use the same unit, so a metre across is a metre up. A slope compares
> the two, so it only means something when they are measured the same
> way.

## Warm-up

The first question is from
[Machines that take a number](tutorial:machines-that-take-a-number#a-machine-with-one-slot),
and the second from
[A row of numbers](tutorial:a-row-of-numbers#counting-from-0).

```question
id: straight-warm-up-1
type: fill-in-the-blank

The TMP36 temperature chip follows the rule $f(x) = 100x - 50$, where
$x$ is its voltage. At 0.75 volts it reads {25} °C.
```

```question
id: straight-warm-up-2
type: multiple-choice
answer: 3

After `point = (3, 7)`, what is `point[1]`?

- 3
  - Counting starts at 0, so `point[0]` is 3.
- (3, 7)
  - `point` on its own is the whole pair; `[1]` picks one item.
- 7
  - Counting from 0, index 1 is the second item.
- an `IndexError`
  - The pair has indexes 0 and 1, so 1 is inside it.
```

## How steep is a ramp?

Picture the ramp from the side. It starts on the ground 3 metres from
the door, and it ends at the top of the step, 0.3 metres up. The distance
it goes up is the *rise*. The distance it goes along the ground is the
*run*. Builders call the run the *going*.

<img src="ramp-from-the-side.svg" alt="The hall's ramp seen from the side, drawn to scale. A long, thin triangle rises from the ground to the top of a step at the door. Its run, or going, along the ground is 3 m, and its rise, the height of the step, is 0.3 m.">

A ramp that climbs 0.3 m over 1 m is far steeper than this one, with
the same rise. So steepness is how much the ramp rises for each metre
along:

$$\text{slope} = \frac{\text{rise}}{\text{run}}$$

This number is the *slope*. The word *gradient* means the same thing.
Schools often say slope, and building guidance says gradient. What is
the slope of the hall's ramp? Guess before you run it.

```python exec
id: straight-ramp-1
rise = 0.3   # metres, the height of the step
run = 3.0    # metres along the ground
ramp_slope = rise / run
print(ramp_slope)
print("1 in", round(1 / ramp_slope))
```

Python shows `0.09999999999999999`, a tiny way under 0.1. That is the
float rounding from
[Everything is ones and zeros](tutorial:everything-is-ones-and-zeros#why-01-02-is-not-03).
The slope is 0.1. For every
metre along, the ramp rises 0.1 of a metre.

Building guidance writes a gradient as a ratio instead, like 1:10, said
"one in ten". It means 1 up for every 10 along. The two are the same
number: $1:10$ is $\frac{1}{10} = 0.1$. So `1 / ramp_slope` turns a slope
back into the "1 in" form.

A bigger slope is a steeper ramp, and a slope of 0 is flat ground. The
slope has no unit, because metres divided by metres leave a plain
number.

## The rule for a ramp

Ireland's building regulations come with guidance on how to meet them,
and for access to buildings it is Technical Guidance Document M. Its
table for ramps, from the 2010 edition, says that a longer ramp must be
gentler, because a long steep climb is tiring to push up and hard to
control on the way down:

| Going of the ramp, up to | Steepest gradient allowed |
|---|---|
| 2 m | 1:12 |
| 5 m | 1:15 |
| 10 m | 1:20 |

The guidance also allows gradients in between. We use the three rows as
they are, which is the careful reading.

An `if` and `elif` choose the row, as on
[Choosing a path](tutorial:choosing-a-path#more-than-two-paths-elif).
A going of 1.5 m is also "up to 5 m", so the shortest row must be
checked first. Does the hall's ramp pass? Decide before you run it.

```python exec
id: straight-rule-1
def steepest_allowed(going):
    """Return the steepest slope allowed for a ramp with this going, in metres.

    Uses the three rows of the table. Gives back None past 10 m, where
    the table has no row.
    """
    if going <= 2:
        return 1 / 12
    elif going <= 5:
        return 1 / 15
    elif going <= 10:
        return 1 / 20
    return None

limit = steepest_allowed(run)
print("the ramp:", round(ramp_slope, 3), " the limit:", round(limit, 3))
print("steep enough to fail?", ramp_slope > limit)
```

The ramp fails. A 3 m ramp may be at most 1:15, about 0.067, and this
one is 1:10.

So how long must the ramp be? Run the slope formula backwards, as on
[Running a formula backwards](tutorial:running-a-formula-backwards#the-same-move-on-both-sides):
if $\text{slope} = \frac{\text{rise}}{\text{run}}$, then
$\text{run} = \frac{\text{rise}}{\text{slope}}$. At 1:15, a rise of
0.3 m needs a run of $0.3 \times 15 = 4.5$ metres. That is still under
5 m, so 1:15 is the row that applies.

### Your turn

1. Find the run needed for a 0.3 m step at 1:12. Is a ramp that
   long allowed to be 1:12? Check with `steepest_allowed`.
2. A second hall has a step of 0.45 m. How long must its ramp be? Try
   1:15 first, then 1:20.

## Slope between any two points

Now let's put lines on a grid. Take two points, $(1, 2)$ and $(5, 4)$.
Going from the first to the second, the run is how far $x$ changes, and
the rise is how far $y$ changes:

- run: $5 - 1 = 4$
- rise: $4 - 2 = 2$
- slope: $\frac{2}{4} = 0.5$

For any two points $(x_1, y_1)$ and $(x_2, y_2)$, the slope is the
change in $y$ over the change in $x$. Maths names the slope $m$:

$$m = \frac{y_2 - y_1}{x_2 - x_1}$$

The cell draws the two points, the line through them, and the rise and
the run as dashed lines. The grey lines are the axes, through 0.

```python exec
id: straight-points-1
import matplotlib.pyplot as plt

start = (1, 2)
end = (5, 4)
plt.plot([start[0], end[0]], [start[1], end[1]], marker="o")
plt.plot([start[0], end[0]], [start[1], start[1]], linestyle="--", color="orange")
plt.plot([end[0], end[0]], [start[1], end[1]], linestyle="--", color="orange")
plt.text(3, 1.6, "run = 4")
plt.text(5.1, 3, "rise = 2")
plt.axis("equal")
plt.axhline(0, color="grey")
plt.axvline(0, color="grey")
```

A line can go downhill too. From $(0, 6)$ to $(3, 0)$, $y$ falls by 6
while $x$ grows by 3, so the rise is $-6$ and the slope is $-2$. A
*negative slope* means the line goes down as we read it from left to
right.

Here is a tool, and its last line is yours to write. The line
`x1, y1 = p` gives each value in the pair a name, as the swap on
[Sorting a hand of cards](tutorial:sorting-a-hand-of-cards#swapping-two-cards)
named two values at once.

```python exec
id: straight-toolkit-slope
toolkit: yes
def slope(p, q):
    """Return the slope of the straight line through the points p and q.

    p and q are (x, y) pairs with different x values.
    slope((1, 2), (5, 4)) is 0.5, and slope((0, 6), (3, 0)) is -2.
    """
    x1, y1 = p
    x2, y2 = q
    ...
```

```python toolkit-reference
for: straight-toolkit-slope
def slope(p, q):
    """Return the slope of the straight line through the points p and q.

    p and q are (x, y) pairs with different x values.
    slope((1, 2), (5, 4)) is 0.5, and slope((0, 6), (3, 0)) is -2.
    """
    x1, y1 = p
    x2, y2 = q
    return (y2 - y1) / (x2 - x1)
```

Run your cell. How does your `slope` compare with one way to
write it? The table below runs the same calls on your function and on
a solution, side by side. Until `slope` has its `return` line, it
returns `None`, and its column shows `None`. Guess the third row
first. Does it matter which point comes first?

```inputs
for: straight-toolkit-slope
slope((1, 2), (5, 4))
slope((0, 6), (3, 0))      # downhill is negative
slope((5, 4), (1, 2))      # either order: the same as the first row?
slope((0, 3), (7, 3))      # flat ground
slope((0, 0), (3, 0.3))    # the hall's ramp...
ramp_slope                 # ...and its slope from the first cell
```

```solution
for: straight-toolkit-slope
def slope(p, q):
    """Return the slope of the straight line through the points p and q.

    p and q are (x, y) pairs with different x values.
    slope((1, 2), (5, 4)) is 0.5, and slope((0, 6), (3, 0)) is -2.
    """
    x1, y1 = p
    x2, y2 = q
    return (y2 - y1) / (x2 - x1)
```

```hint
for: straight-toolkit-slope
after: 3 runs
Try `print(slope((1, 2), (5, 4)))` on its own. What came back? Which two
differences does the formula divide?
```

The order does not matter. If we swap the points, we get
$\frac{-2}{-4}$, which is still $0.5$.

## A wall has no slope

The front wall of the hall is a line too. Draw it from $(2, 0)$ to
$(2, 5)$: straight up. What will `slope` say about it? The cell is
meant to stop with an error.

```python exec
id: straight-wall-1
print(slope((2, 0), (2, 5)))
```

The last line of the traceback reads
`ZeroDivisionError: division by zero`. The run is $2 - 2 = 0$, and the
formula divides by the run. Your `slope` is keeping its promise here.
The docstring promised a slope only for points with different $x$
values.

Is "infinitely steep" an answer? It is not, in the real numbers. A *vertical
line*, one that goes straight up, has no slope in this space. Two
sections on, a way of writing lines makes room for it.

## A line as a rule: y = mx + c

On
[Drawing a rule](tutorial:drawing-a-rule#straight-lines-and-where-two-meet),
server A took 8 ms to answer, plus 2 ms for every thousand people using
the app. Its graph was the line $y = 2x + 8$, and that page promised a
proper look at steepness. Here it is. The slope is 2. For each thousand
more people, the time goes up 2 ms. The line crosses the $y$ axis at 8, the
time with nobody else using the app.

Every straight line that is not vertical can be written this way:

$$y = mx + c$$

In words: multiply $x$ by the slope $m$, then add $c$. The number $c$
is where the line crosses the $y$ axis, at $x = 0$. It is called the
*y-intercept*. The TMP36 chip from the warm-up is a line too:
$y = 100x - 50$, with a slope of 100 and a y-intercept of −50.

What do $m$ and $c$ each do? The cell draws server A, server A without
its 8 ms start, server C, and server B, which always took 20 ms. Which
will be steepest, and which one is flat?

```python exec
id: straight-rule-picture-1
def server_a(thousands):
    return 2 * thousands + 8

def server_a_no_start(thousands):
    return 2 * thousands

def server_c(thousands):
    return 1.2 * thousands + 15

def server_b(thousands):
    return 0 * thousands + 20

for rule in [server_a, server_a_no_start, server_c, server_b]:
    plot_rule(rule, 0, 10)
plt.legend()
```

The two server A lines have the same steepness, one lifted 8 above the
other. Changing $c$ slides a line up or down, and changing $m$ turns
it. Server B has $m = 0$, so its line is flat, whatever the crowd.

If we know two points on a line, we know the line. First find $m$ with
`slope`. Then, since the first point $(x_1, y_1)$ is on the line,
$y_1 = m x_1 + c$, and moving $m x_1$ to the other side gives

$$c = y_1 - m x_1$$

That is your second tool. It returns the pair `(m, c)`.

```python exec
id: straight-toolkit-line
toolkit: yes
def line_through(p, q):
    """Return (m, c) for the line y = mx + c through the points p and q.

    p and q are (x, y) pairs with different x values.
    line_through((0, 8), (10, 28)) is (2.0, 8.0), server A's line.
    """
    ...
```

```python toolkit-reference
for: straight-toolkit-line
def line_through(p, q):
    """Return (m, c) for the line y = mx + c through the points p and q.

    p and q are (x, y) pairs with different x values.
    line_through((0, 8), (10, 28)) is (2.0, 8.0), server A's line.
    """
    m = slope(p, q)
    x1, y1 = p
    c = y1 - m * x1
    return (m, c)
```

How does your `line_through` compare with a solution? The first row
of the table below is server A. The second row finds the TMP36 chip's
rule from two readings: 0.5 volts at 0 °C, and 0.75 volts at 25 °C.
Where a row is different, try that call on its own.

```inputs
for: straight-toolkit-line
line_through((0, 8), (10, 28))       # server A
line_through((0.5, 0), (0.75, 25))   # the TMP36 chip
line_through((1, 2), (5, 4))
line_through((0, 6), (3, 0))
line_through((-3, 7), (2, -1.5))
```

```solution
for: straight-toolkit-line
def line_through(p, q):
    """Return (m, c) for the line y = mx + c through the points p and q.

    p and q are (x, y) pairs with different x values.
    line_through((0, 8), (10, 28)) is (2.0, 8.0), server A's line.
    """
    m = slope(p, q)
    x1, y1 = p
    c = y1 - m * x1
    return (m, c)
```

Unit 7 checks every answer the same way: put it back in. Both points
must land on the line that comes out. Can you check one of the last
three rows like that? For $(1, 2)$ and $(5, 4)$, is $m \times 1 + c$
equal to 2, and $m \times 5 + c$ equal to 4?

```hint
for: straight-toolkit-line
after: 3 runs
title: some steps
1. Find `m` with your toolkit's `slope(p, q)`.
2. Give the two values of `p` a name each: `x1, y1 = p`.
3. Work out `c = y1 - m * x1`, and give back `(m, c)`.

**Think about:** why is using `p` and not `q` for $c$ a free choice?
```

The line through $(1, 2)$ and $(5, 4)$ is $y = 0.5x + 1.5$, and two
readings were enough to find the chip's whole rule.

<aside class="dl-note" id="straight-note-bresenham">

**A line made of pixels.** A screen has no slopes, only squares. To
draw a line from one pixel to another, a program steps along one pixel
at a time and decides, at each step, whether to go up one as well.
Jack Bresenham found the best-known way to decide, at IBM in 1962, to
drive a pen plotter. Drawing programs still use ideas from it.

</aside>

## Every line at once: ax + by + c = 0

The wall from $(2, 0)$ to $(2, 5)$ is still missing. Every point on it
has $x = 2$, whatever its $y$. So "$x = 2$" describes the wall exactly,
and it has no $y$ in it to be the subject of the rule.

There is one way of writing a line that covers the wall and every other
line:

$$ax + by + c = 0$$

This is the *general form* of a line. A point is on the line when
its $x$ and $y$ make the left side 0. The wall is
$1x + 0y - 2 = 0$. Server A's line $y = 2x + 8$ becomes
$2x - y + 8 = 0$ when we move $y$ to the right-hand side and swap the
sides round. Any line $y = mx + c$ is $mx - y + c = 0$, with
$a = m$ and $b = -1$.

A note on names: the $c$ in $y = mx + c$ and the $c$ in
$ax + by + c = 0$ are two different numbers that share a letter, like
two people called Seán. If this many letters feels like a lot, run the
next cell first and come back to the algebra after it.

Here is the test as a function. Which of the three points do you expect
to be on each line?

```python exec
id: straight-general-1
def on_line(a, b, c, point):
    """Return True when point is on the line ax + by + c = 0."""
    x, y = point
    return close_enough(a * x + b * y + c, 0)

for point in [(2, 0), (2, 3.7), (0, 8)]:
    print(point, "wall:", on_line(1, 0, -2, point), " server A:", on_line(2, -1, 8, point))
```

Both points with $x = 2$ are on the wall, and $(0, 8)$ is on server
A's line. The general form does not say how to find $y$, as $y = mx + c$ does.
In exchange, it has room for every straight line.

To get the slope back from the general form, move everything except
$by$ to the right: $by = -ax - c$, so $y = -\frac{a}{b}x - \frac{c}{b}$.
The slope is $-\frac{a}{b}$. That needs $b$ not to be 0. When $b$ is 0,
the line is straight up, like the wall.

```question
id: straight-general-2
type: multiple-choice
answer: 2

What is the slope of the line $2x + 4y - 8 = 0$?

- 2
  - 2 is the number with x before rearranging, and y has a 4 with it.
- −0.5
  - Rearranged, 4y = −2x + 8, so y = −0.5x + 2.
- 0.5
  - The size is the same, but moving 2x to the other side makes it negative.
- −8
  - −8 is the number on its own; it moves the line, and does not tilt it.
```

## Parallel and perpendicular

On
[Several unknowns at once](tutorial:several-unknowns-at-once#when-there-is-no-single-answer),
two parallel lines never met, so their equations had no single answer.
Now we can say what "the same steepness" means: parallel lines have the
same slope. The two server A lines in the picture were parallel.

Two lines are *perpendicular* when they meet at a right angle, like the
floor and the hall's wall. Take a line that goes 2 across and 1 up,
slope $\frac{1}{2}$. Turn it a quarter turn to the left, and it goes 1
back and 2 up. The run and rise swap, and one changes sign. The new
slope is $-2$.

So the slope of a perpendicular line is $-\frac{1}{m}$.
Said another way, two slopes $m_1$ and $m_2$ belong to perpendicular
lines when

$$m_1 \times m_2 = -1$$

The cell draws $y = 0.5x + 1$ and $y = -2x + 6$ twice. On the left,
matplotlib chooses the scale of each axis. On the right,
`plt.axis("equal")` makes a unit across the same length as a unit up.
Before you run it, which picture do you think shows the right angle?

```python exec
id: straight-perpendicular-1
figure, (left, right) = plt.subplots(1, 2, figsize=(9, 4))
xs = [0, 4]
for axes in [left, right]:
    axes.plot(xs, [0.5 * 0 + 1, 0.5 * 4 + 1])
    axes.plot(xs, [-2 * 0 + 6, -2 * 4 + 6])
    axes.axhline(0, color="grey")
    axes.axvline(0, color="grey")
right.axis("equal")

print(0.5 * -2)
```

The product is $-1$, so the lines are perpendicular, but only the right
picture shows a square corner. The box at the top said that both axes
use the same unit. The left picture does not. It stretches $y$, and a
stretched right angle stops looking like one.

### Your turn

1. A path in a game level runs along $y = 3x - 2$. Write the line
   through $(0, 5)$ parallel to it, then the one through $(0, 5)$
   perpendicular to it.
2. Use `line_through` to find the line through $(1, 1)$ and $(4, 7)$.
   Is it parallel to the path?
3. Check your perpendicular slope from step 1 with `close_enough`: does
   its product with 3 come to $-1$?

<details class="dl-why"><summary>Why this way?</summary>

This page started with a real ramp and its rise and run, and wrote
$y = mx + c$ only halfway through.

Many courses start the other way, with $y = mx + c$ drawn on a grid,
and then practise reading $m$ and $c$ from graphs. That route is shorter,
it gives the algebra first, and it leads straight into questions like
"where do two lines meet?", which Unit 7 answered.

We started with a ramp because a slope is a measurement before it is a
letter in a rule, and a measurement is something you can check against
a building's guidance. The cost is that the general form,
$ax + by + c = 0$, arrived late and quickly, and a reader who likes
the algebra first had to wait for it.

</details>

## Four questions, looking back

| The question | On this page |
|---|---|
| What is named here? | a point as a pair, `(x, y)`; the slope $m$ and the intercept $c$; two different numbers that both get called $c$ |
| What is promised? | `slope(p, q)` promises rise over run for points with different $x$; `line_through(p, q)` promises a line that both points land on |
| What happens when? | the shortest row of the ramp table is checked first; `line_through` finds $m$ before it can find $c$ |
| What does this space let us do? | a flat plane with the same unit both ways; a vertical line has no slope among the real numbers, and $ax + by + c = 0$ makes room for it |

## What we have now

| Term or tool | What it means |
|---|---|
| rise, run (going) | how far a line goes up, and how far along |
| slope, gradient, $m$ | rise over run: $m = \frac{y_2 - y_1}{x_2 - x_1}$ |
| 1:12, "one in twelve" | a gradient as a ratio: 1 up for 12 along, a slope of $\frac{1}{12}$ |
| negative slope | a line that goes down from left to right |
| vertical line | a line straight up, like $x = 2$, with no slope |
| $y = mx + c$ | a line as a rule: slope $m$, crossing the $y$ axis at $c$ |
| y-intercept | where a line crosses the $y$ axis |
| $ax + by + c = 0$ | the general form, which can write every straight line |
| parallel lines | lines with the same slope, which never meet |
| perpendicular lines, $m_1 m_2 = -1$ | lines at a right angle: each slope is $-1$ over the other |
| `slope(p, q)` | your toolkit tool: the slope of the line through two points |
| `line_through(p, q)` | your toolkit tool: the `(m, c)` of the line through two points |

The practice page is next. Then
[How far apart?](tutorial:how-far-apart) measures the length of a line.

## Where to read more

The dewlab page
[Straight lines: slope, and the line that breaks the formula](tutorial:slope-and-lines)
meets slope as a rate, and the one line $y = mx + c$ cannot write, from
another direction.

Stand-up Maths (2015). *NYC: The Linear Equation of Broadway.*
<https://www.youtube.com/watch?v=Quwvw0vYkRA>. Matt Parker walks along
Broadway in New York with graph paper, and finds the equation of the
street as a straight line. Eleven minutes.
