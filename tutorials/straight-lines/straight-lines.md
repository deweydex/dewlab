---
title: "Straight lines: slope and gradient"
year: "2026-2027"
version: 2026.09.24.1
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

A small café has one step at its front door, 30 cm high. The owner wants
everyone to be able to come in, so she buys a ramp that reaches 3 metres
out from the door. A friend who uses a wheelchair looks at it and says
it is too steep. Is she right? And how would you measure "too steep"?

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
> as a tuple, like `(3, 0.3)`. One thing usually goes unsaid: both axes
> use the same unit, a metre across is a metre up. A slope compares the
> two, so it only means something when they are measured the same way.

## Warm-up

The first question is from
[Machines that take a number](tutorial:machines-that-take-a-number#a-machine-with-one-slot),
and the second from
[A row of numbers](tutorial:a-row-of-numbers#counting-from-0).

```question
id: straight-warm-up-1
type: fill-in-the-blank

A taxi fare is $f(x) = 4 + 1.5x$ euro for a trip of $x$ km. A 10 km trip
costs {19} euro.
```

```question
id: straight-warm-up-2
type: multiple-choice
correct: 3

After `point = (3, 7)`, what is `point[1]`?

- 3
- (3, 7)
- 7
- an `IndexError`
```

## How steep is a ramp?

Picture the ramp from the side. It starts on the ground 3 metres from
the door, and it ends at the top of the step, 0.3 metres up. The distance
it goes up is the *rise*. The distance it goes along the ground is the
*run*. Builders call the run the *going*.

A ramp that climbs 0.3 m over 1 m is far steeper than this one, with
the same rise. So steepness is how much the ramp rises for each metre
along:

$$\text{slope} = \frac{\text{rise}}{\text{run}}$$

This number is the *slope*. The word *gradient* means the same thing:
schools often say slope, and building guidance says gradient. What is
the slope of the café's ramp? Guess before you run it.

```python exec
id: straight-ramp-1
rise = 0.3   # metres, the height of the step
run = 3.0    # metres along the ground
ramp_slope = rise / run
print(ramp_slope)
print("1 in", round(1 / ramp_slope))
```

Python shows `0.09999999999999999`, a tiny way under 0.1. That is the
float rounding we met on
[Everything is ones and zeros](tutorial:everything-is-ones-and-zeros#why-01-02-is-not-03),
not a mistake in the ramp. The slope is 0.1: for every metre along, the
ramp rises 0.1 of a metre.
Building guidance writes a gradient as a ratio instead, like 1:10, said
"one in ten". It means 1 up for every 10 along. The two are the same
number: $1:10$ is $\frac{1}{10} = 0.1$. So `1 / ramp_slope` turns a slope
back into the "1 in" form.

A bigger slope is a steeper ramp, and a slope of 0 is flat ground. The
slope has no unit: metres divided by metres leave a plain number, so 30
cm over 300 cm gives the same answer.

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

The guidance also allows gradients in between these rows. We use the
three rows as they are, which is the careful reading, and a designer
would check the current edition before building anything.

Choosing a row is an `if` and `elif`, as on
[Choosing a path](tutorial:choosing-a-path#more-than-two-paths-elif).
A going of 1.5 m is also "up to 5 m", so the shortest row must be
checked first. Does the café's ramp pass? Decide before you run it.

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

The friend was right. A 3 m ramp may be at most 1:15, about 0.067, and
this one is 1:10.

So how long must the ramp be? Run the slope formula backwards, as on
[Running a formula backwards](tutorial:running-a-formula-backwards#the-same-move-on-both-sides):
if $\text{slope} = \frac{\text{rise}}{\text{run}}$, then
$\text{run} = \frac{\text{rise}}{\text{slope}}$. At 1:15, a rise of
0.3 m needs a run of $0.3 \times 15 = 4.5$ metres. That is still under
5 m, so 1:15 is the right row for it.

### Your turn

1. Work out the run needed for a 0.3 m step at 1:12. Is a ramp that
   long allowed to be 1:12? Check with `steepest_allowed`.
2. A second café has a step of 0.45 m. How long must its ramp be? Try
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

Now it is time for a tool, and its last line is yours to write. The
line `x1, y1 = p` gives each value in the pair a name, as the swap on
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

Run your cell, then the tests. Until `slope` has its `return` line, it
gives back `None`, and the first test stops with a `TypeError`: Python
cannot subtract a number from `None`. The third test asks something
worth a guess first: does it matter which point comes first?

```python exec
id: straight-toolkit-slope-tests
assert close_enough(slope((1, 2), (5, 4)), 0.5)
assert close_enough(slope((0, 6), (3, 0)), -2), "downhill is negative"
assert close_enough(slope((5, 4), (1, 2)), slope((1, 2), (5, 4))), "either order"
assert slope((0, 3), (7, 3)) == 0, "flat ground"
assert close_enough(slope((0, 0), (3, 0.3)), ramp_slope), "the café's ramp"
print("slope keeps its promise.")
```

```hint
Try `print(slope((1, 2), (5, 4)))` on its own. What came back? Which two
differences does the formula divide?
```

The order does not matter: swapping the points gives $\frac{-2}{-4}$,
which is still $0.5$. The tests use `close_enough` from
[Does it work?](tutorial:does-it-work#close-enough) because a division
of floats can land a tiny way off.

## A wall has no slope

The front wall of the café is a line too. Draw it from $(2, 0)$ to
$(2, 5)$: straight up. What will `slope` say about it? The cell is
meant to stop with an error.

```python exec
id: straight-wall-1
print(slope((2, 0), (2, 5)))
```

The last line of the traceback reads
`ZeroDivisionError: division by zero`. The run is $2 - 2 = 0$, and the
formula divides by the run. This is not a bug in your `slope`: the
docstring promised a slope only for points with different $x$ values.

Is "infinitely steep" an answer? Not in the real numbers, where every
number has some finite size. A *vertical line*, one that goes straight
up, has no slope in this space. Two sections on, a way of writing lines
makes room for it.

## A line as a rule: y = mx + c

Go back to the taxi from the warm-up. A graph of its fare is a straight
line with slope 1.5: one more kilometre along, €1.50 more up. It crosses
the $y$ axis at 4, the fare for 0 km.

On
[Drawing a rule](tutorial:drawing-a-rule#straight-lines-and-where-two-meet),
phone plan A was the line $y = 2x + 8$, and that page promised a proper
look at steepness. Every straight line that is not vertical can be
written this way:

$$y = mx + c$$

In words: to find $y$, multiply $x$ by the slope $m$, then add $c$. The
number $c$ is where the line crosses the $y$ axis, at $x = 0$. It is
called the *y-intercept*. The taxi's line is $y = 1.5x + 4$.

What do $m$ and $c$ each do to a line? The cell draws four lines with
`plot_rule` from your toolkit. Guess which will be steepest, and which
one goes down, before you run it.

```python exec
id: straight-rule-picture-1
def taxi(x):
    return 1.5 * x + 4

def taxi_no_start(x):
    return 1.5 * x

def gentle(x):
    return 0.5 * x

def downhill(x):
    return -2 * x + 1

for rule in [taxi, taxi_no_start, gentle, downhill]:
    plot_rule(rule, -4, 4)
plt.legend()
```

The two taxi lines have the same steepness, one lifted 4 above the
other. Changing $c$ slides a line up or down, and changing $m$ turns
it. The `downhill` line has $m = -2$.

If we know two points on a line, we know the line. First find $m$ with
`slope`. Then, since the first point $(x_1, y_1)$ is on the line,
$y_1 = m x_1 + c$, and moving $m x_1$ to the other side gives

$$c = y_1 - m x_1$$

That is your second tool. It gives back the pair `(m, c)`.

```python exec
id: straight-toolkit-line
toolkit: yes
def line_through(p, q):
    """Return (m, c) for the line y = mx + c through the points p and q.

    p and q are (x, y) pairs with different x values.
    line_through((0, 4), (10, 19)) is (1.5, 4.0), the taxi's line.
    """
    ...
```

```python toolkit-reference
for: straight-toolkit-line
def line_through(p, q):
    """Return (m, c) for the line y = mx + c through the points p and q.

    p and q are (x, y) pairs with different x values.
    line_through((0, 4), (10, 19)) is (1.5, 4.0), the taxi's line.
    """
    m = slope(p, q)
    x1, y1 = p
    c = y1 - m * x1
    return (m, c)
```

The tests check the answer the way Unit 7 checks every answer: put it
back in. Both points must land on the line that comes out.

```python exec
id: straight-toolkit-line-tests
m, c = line_through((0, 4), (10, 19))
assert close_enough(m, 1.5) and close_enough(c, 4), "the taxi"

for p, q in [((1, 2), (5, 4)), ((0, 6), (3, 0)), ((-3, 7), (2, -1.5))]:
    m, c = line_through(p, q)
    for x, y in [p, q]:
        assert close_enough(m * x + c, y), (p, q)
print("line_through keeps its promise:", line_through((1, 2), (5, 4)))
```

```hint
after: 8 errors
title: some steps
1. Find `m` with your toolkit's `slope(p, q)`.
2. Give the two values of `p` a name each: `x1, y1 = p`.
3. Work out `c = y1 - m * x1`, and give back `(m, c)`.

**Think about:** why is using `p` and not `q` for $c$ a free choice?
```

The line through $(1, 2)$ and $(5, 4)$ is $y = 0.5x + 1.5$.

## Every line at once: ax + by + c = 0

The wall from $(2, 0)$ to $(2, 5)$ is still missing. Every point on it
has $x = 2$, whatever its $y$. So "$x = 2$" describes the wall exactly,
and it has no $y$ in it to be the subject of the rule.

There is one way of writing a line that covers the wall and every other
line:

$$ax + by + c = 0$$

This is the *general form* of a line. A point is on the line when
putting its $x$ and $y$ in makes the left side 0. The wall is
$1x + 0y - 2 = 0$. The taxi's line $y = 1.5x + 4$ becomes
$1.5x - y + 4 = 0$ when we move $y$ to the right-hand side and swap the
sides round. Any line $y = mx + c$ is $mx - y + c = 0$, with
$a = m$ and $b = -1$.

A note on names: the $c$ in $y = mx + c$ and the $c$ in
$ax + by + c = 0$ are two different numbers that share a letter, like
two people called Seán.

Here is the test as a function. Which of the three points do you expect
to be on each line?

```python exec
id: straight-general-1
def on_line(a, b, c, point):
    """Return True when point is on the line ax + by + c = 0."""
    x, y = point
    return close_enough(a * x + b * y + c, 0)

for point in [(2, 0), (2, 3.7), (0, 4)]:
    print(point, "wall:", on_line(1, 0, -2, point), " taxi:", on_line(1.5, -1, 4, point))
```

Both points with $x = 2$ are on the wall, and $(0, 4)$ is on the taxi's
line. The general form does not say "here is how to find $y$", as
$y = mx + c$ does. In exchange, it has room for every straight line.

To get the slope back from the general form, move everything except
$by$ to the right: $by = -ax - c$, so $y = -\frac{a}{b}x - \frac{c}{b}$.
The slope is $-\frac{a}{b}$. That needs $b$ not to be 0, which is the
wall again, from the other side.

```question
id: straight-general-2
type: multiple-choice
correct: 2

What is the slope of the line $2x + 4y - 8 = 0$?

- 2
- −0.5
- 0.5
- −8
```

## Parallel and perpendicular

On
[Several unknowns at once](tutorial:several-unknowns-at-once#when-there-is-no-single-answer),
two parallel lines never met, so their equations had no single answer.
Now we can say what "the same steepness" means: parallel lines have the
same slope. The two taxi lines in the picture were parallel.

Two lines are *perpendicular* when they meet at a right angle, like the
floor and the café wall. Take a line that goes 2 across and 1 up, slope
$\frac{1}{2}$. Turn it a quarter turn to the left, and it goes 1 back
and 2 up: the run and rise swap, and one changes sign. The new slope is
$\frac{2}{-1} = -2$.

That is the rule: the slope of a perpendicular line is $-\frac{1}{m}$.
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
picture shows a square corner. The left one stretches $y$, and a
stretched right angle stops looking like one. This is the unsaid
assumption from the box at the top.

### Your turn

1. A path runs along $y = 3x - 2$. Write the line through $(0, 5)$
   parallel to it, then the one through $(0, 5)$ perpendicular to it.
2. Use `line_through` to find the line through $(1, 1)$ and $(4, 7)$.
   Is it parallel to the path?
3. Check your perpendicular slope from step 1 with `close_enough`: does
   its product with 3 come to $-1$?

<details class="dl-why"><summary>Why this way?</summary>

This page started with a real ramp and its rise and run, and wrote
$y = mx + c$ only halfway through.

Many courses start the other way, with $y = mx + c$ drawn on a grid,
and then practise reading $m$ and $c$ off graphs. That route is shorter,
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
[Straight lines: slope, midpoint and distance](tutorial:lines-and-distances)
meets slope as a rate, and the one line $y = mx + c$ cannot write, from
another direction.
