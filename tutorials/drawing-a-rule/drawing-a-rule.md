---
title: "Drawing a rule: graphs of functions"
year: "2026-2027"
version: 2026.09.24.1
covers:
  a-table-then-a-picture:
    covers: [MIT-3.2]
    touches: [MIT-3.1]
  a-tool-that-draws-any-rule:
    covers: [MIT-3.2]
    touches: [PDP-LO8]
  straight-lines-and-where-two-meet:
    covers: [MIT-3.2]
  curves-that-bend-parabolas-and-cubics:
    covers: [MIT-3.2]
    touches: [MIT-1.8]
  rules-with-gaps-and-rules-that-race:
    covers: [MIT-3.2]
    touches: [MIT-3.1, MIT-1.1]
  what-a-graph-shows-that-a-table-hides:
    covers: [MIT-3.2]
---

# Drawing a rule: graphs of functions

Here is a rule: $y = x^2 - 4$. Put in 3, and 5 comes out. Put in $-3$,
and 5 comes out again. Put in 0, and you get $-4$. What does the rule
look like when we put in every number at once? And where does it cross
zero?

A goalkeeper asks the same kind of question without knowing it. The
ball goes up, slows, turns and comes down. When does it land? A table of
heights can answer that. A picture answers it at a glance, and shows
more besides.

On this page we:

- draw a rule as every pair $(x, y)$ at once, and add `plot_rule` to
  the toolkit
- read where a graph crosses zero, and check it by substituting
- draw straight lines, parabolas and cubics, and find where two graphs
  meet
- meet a rule with a gap in it, $\frac{1}{x}$, and two rules that race,
  $x^2$ and $2^x$
- see what a graph shows that a table hides

> **The space we're in.** Pairs of real numbers, drawn on a flat grid.
> One line runs across and one runs up, and they cross at 0. A computer
> cannot draw every real number: it works out a few hundred points and
> joins them with short straight lines. One thing usually goes unsaid:
> a graph is only as honest as the points it was drawn from.

## Warm-up

The first question is from
[Rules with letters in them](tutorial:rules-with-letters-in-them#putting-a-number-in-for-the-letter),
and the second from
[Machines that take a number](tutorial:machines-that-take-a-number#what-goes-in-and-what-comes-out).

```question
id: drawing-a-warm-up-1
type: fill-in-the-blank

`[-4, 0, 1]` is the polynomial $x^2 - 4$. So `evaluate([-4, 0, 1], 3)`
is {5}.
```

```question
id: drawing-a-warm-up-2
type: fill-in-the-blank

The {domain|range|inverse} of a function is the set of inputs it
accepts.
```

## A table, then a picture

Let's start with a table. For each whole number $x$ from $-3$ to 3, the
cell prints $x$ and then $x^2 - 4$. Where do you expect the value to be
0?

```python exec
id: drawing-a-table-1
def square_minus_four(x):
    """Return x squared, take away 4."""
    return x ** 2 - 4

for x in range(-3, 4):
    print(x, square_minus_four(x))
```

The value is 0 at $x = -2$ and at $x = 2$. It is smallest, $-4$, at
$x = 0$, and the rows above and below 0 match: 5 at $-3$ and at 3.

Each row of the table is a pair of numbers. Written as $(x, y)$, a pair
like $(3, 5)$ is a point's *coordinates*: go 3 across, then 5 up. The
line across is the *x-axis*, and the line up is the *y-axis*. They cross
at the *origin*, the point $(0, 0)$. A negative $x$ means "go left", and
a negative $y$ means "go down".

The cell below draws the seven rows as seven dots. The two grey lines
are the axes, drawn through 0. What shape will the dots make?

```python exec
id: drawing-a-table-2
import matplotlib.pyplot as plt

xs = []
ys = []
for x in range(-3, 4):
    xs.append(x)
    ys.append(square_minus_four(x))

plt.plot(xs, ys, "o")
plt.axhline(0, color="grey")
plt.axvline(0, color="grey")
```

The dots make a U. `"o"` asks for dots with no line between them. But
what happens between the dots? The rule has a value at $x = 0.5$ and at
$x = 2.71$ too. The *graph* of a function is the picture of every pair
$(x, f(x))$, for every $x$ in its domain. We write the rule as
$y = f(x)$, so that $y$ names the output.

## A tool that draws any rule

We cannot work out every real number, but we can work out a lot of
them. `plot_rule` works out 401 evenly spaced points between `low` and
`high`, and joins them. The points are so close together that the short
straight lines look like one smooth curve.

This toolkit tool is written for you. Read it before you run it: which
lines are the table, and which lines draw?

```python exec
id: drawing-a-toolkit
toolkit: yes
import matplotlib.pyplot as plt


def plot_rule(rule, low, high):
    """Draw the graph of rule, every point (x, rule(x)), for x from low to high.

    The axes are drawn through 0 wherever 0 is in view. Each call draws
    on the same picture, so two calls in one cell draw two rules together.
    """
    steps = 400
    xs = []
    ys = []
    for step in range(steps + 1):
        x = low + step * (high - low) / steps
        xs.append(x)
        ys.append(rule(x))
    plt.plot(xs, ys, label=rule.__name__)
    if low <= 0 <= high:
        plt.axvline(0, color="grey", linewidth=1)
    if min(ys) <= 0 <= max(ys):
        plt.axhline(0, color="grey", linewidth=1)
    plt.grid(alpha=0.3)
```

The loop is the table from the last section, with 401 rows in place of
7. The rest draws. `rule.__name__` is the name the rule was given with
`def`: every Python function knows its own name, and `plot_rule` uses it
as a label. The two `if` lines draw an axis only where 0 is in view, so
a graph from 5 to 10 has no y-axis squeezed in at its edge.

`plot_rule` is a procedure, as on
[Machines that take a number](tutorial:machines-that-take-a-number#functions-that-give-back-and-procedures-that-do):
it draws, and gives back `None`. Now the whole of $y = x^2 - 4$:

```python exec
id: drawing-a-toolkit-2
plot_rule(square_minus_four, -3, 3)
```

The U is smooth, with its lowest point at $(0, -4)$. It crosses the
x-axis at two places, which look like $-2$ and 2. An $x$ where a
function's value is 0 is a *root* of the function. On a graph, a root
is a place where the graph meets the x-axis.

Reading a root off a graph is *solving from a graph*. A picture gives
an answer to the width of a line, so we check it by substituting, as
on the last page. Will both lines print 0?

```python exec
id: drawing-a-toolkit-3
print(square_minus_four(-2), square_minus_four(2))
print(evaluate([-4, 0, 1], -2), evaluate([-4, 0, 1], 2))
```

Both give 0. The last page expanded $(x - 2)(x + 2)$ into $x^2 - 4$.
The brackets tell us the same roots: $x - 2$ is 0 when $x$ is 2, and
$x + 2$ is 0 when $x$ is $-2$.

## Straight lines, and where two meet

Two phone plans. Plan A costs €8 a month, plus €2 for each gigabyte of
data you use. Plan B costs €20 a month, however much you use. Which is
cheaper? It depends on the gigabytes. Here are both plans, drawn on one
picture. `plt.legend()` shows which line is which. Before you run it,
predict the shape of each line.

```python exec
id: drawing-a-lines-1
def plan_a(gigabytes):
    """Return the monthly cost in euro of plan A: €8, plus €2 a gigabyte."""
    return 8 + 2 * gigabytes


def plan_b(gigabytes):
    """Return the monthly cost in euro of plan B: €20, however much you use."""
    return 20


plot_rule(plan_a, 0, 10)
plot_rule(plan_b, 0, 10)
plt.legend()
```

Both graphs are straight lines. Plan A starts at 8 and climbs 2 for
every step to the right. Plan B is flat. A *linear function* is a
function whose graph is a straight line. Its rule has the shape
$y = mx + c$: the number $m$ in front of $x$ says how steep the line is,
and $c$ is where it crosses the y-axis. Plan A is $y = 2x + 8$.
[Straight lines](tutorial:straight-lines) looks at steepness properly.

The lines cross at about 6 gigabytes and €20. Left of the crossing,
plan A is cheaper; right of it, plan B is. Where two graphs meet, the
two rules give the same value, so the crossing answers the equation
$2x + 8 = 20$. Let's check by substituting:

```python exec
id: drawing-a-lines-2
print(plan_a(6), plan_b(6))
print(plan_a(5), plan_a(7))
```

At 6 gigabytes both cost €20. At 5, plan A costs €18, and at 7 it costs
€22. The graph gave the answer, and substitution checked it.
[Solving for x](tutorial:solving-for-x) finds the same answer with no
picture at all.

### Your turn

1. Plan C costs €12 a month plus €1 a gigabyte. Write `plan_c` and draw
   all three plans from 0 to 15.
2. Read off where plan C crosses each of the others.
3. Check each crossing by substituting.

```python exec
id: drawing-a-lines-your-turn
# Your plan_c, and the three graphs
```

## Curves that bend: parabolas and cubics

Back to the goalkeeper. In a simple model with rounded numbers, a ball
kicked straight up at 20 metres a second is $20t - 5t^2$ metres high,
$t$ seconds after the kick. What shape will its graph be? Where will it
cross zero?

```python exec
id: drawing-a-curves-1
def ball_height(seconds):
    """Return the height in metres of the kicked ball, seconds after the kick."""
    return 20 * seconds - 5 * seconds ** 2


plot_rule(ball_height, 0, 4)
plt.xlabel("seconds after the kick")
plt.ylabel("height in metres")
```

The graph is an upside-down U. It starts at 0, rises to a top of 20
metres after 2 seconds, and comes back to 0 after 4 seconds. That is
when the ball lands: `ball_height(4)` is 0. The top of the curve is the
subject of [The top of the curve](tutorial:the-top-of-the-curve).

The graph of a quadratic function is a curve called a *parabola*. When
the $x^2$ term has a positive coefficient, as in $x^2 - 4$, the
parabola opens upwards, like a U. When it is negative, as in
$-5t^2 + 20t$, it opens downwards.

What about a cubic? On the last page, three brackets made a cubic. Here
is $x^3 - 4x$, which is $x(x - 2)(x + 2)$, using `evaluate`. How many
times do you think it will cross the x-axis?

```python exec
id: drawing-a-curves-2
def cubic(x):
    """Return x cubed, take away 4x."""
    return evaluate([0, -4, 0, 1], x)


plot_rule(cubic, -3, 3)
```

It crosses three times: at $-2$, 0 and 2, one root for each bracket. A
cubic's graph can turn twice, so it can cross the x-axis up to three
times. A parabola turns once, and crosses at most twice. A straight line
that is not flat crosses exactly once.

### Your turn

1. Draw `ball_height` from $-1$ to 5. What does the graph say the height
   is at $t = 5$?
2. The rule gives an answer, but the ball is on the grass by then. Which
   inputs belong in this model's domain?

```python exec
id: drawing-a-curves-your-turn
# Your graph here
```

## Rules with gaps, and rules that race

Four friends share a €60 prize, and each gets €15. Ten friends get €6
each. The more people, the smaller each share. The share is
$\frac{60}{x}$, and its shape comes from $\frac{1}{x}$.

What happens to $\frac{1}{x}$ at $x = 0$? The cell below asks
`plot_rule` to find out. It is meant to stop with an error.

```python exec
id: drawing-a-gaps-1
def one_over(x):
    """Return 1 divided by x."""
    return 1 / x


plot_rule(one_over, -5, 5)
```

Read the last line of the error, as on
[When Python says no](tutorial:when-python-says-no):
`ZeroDivisionError: float division by zero`. One of the 401 points was
exactly 0.0, a float 0, and $\frac{1}{0}$ has no value. So 0 is not in the domain of
this function. The graph has a gap there. We can draw it in two pieces,
one on each side of the gap:

```python exec
id: drawing-a-gaps-2
plot_rule(one_over, -5, -0.1)
plot_rule(one_over, 0.1, 5)
```

Near 0, the two pieces race away, one up and one down. Far from 0, they
creep towards the x-axis and never reach it: $\frac{1}{x}$ gets small,
but it is never 0.

Now two rules that race each other: $x^2$ and $2^x$. At $x = 3$, $x^2$
is 9 and $2^3$ is 8, so $x^2$ is ahead. Which one wins by $x = 6$?
Predict, then draw.

```python exec
id: drawing-a-gaps-3
def squared(x):
    """Return x squared."""
    return x ** 2


def two_to_the(x):
    """Return 2 to the power x."""
    return 2 ** x


plot_rule(squared, 0, 6)
plot_rule(two_to_the, 0, 6)
plt.legend()
```

The graphs meet at $x = 2$ and $x = 4$. Between them $x^2$ is ahead,
and after 4, $2^x$ pulls away: at 6 it is 64, to the square's 36. The
curve of $2^x$ is the rumour from
[Doubling and halving](tutorial:doubling-and-halving#a-rumour-that-doubles),
flat at first and then steep. That page also drew $\log_2 x$, which is
the same curve reflected, so it grows very slowly.

### Your turn

1. Check the two meeting points: is `squared(4) == two_to_the(4)`? And
   at 2?
2. Draw `math.log2` from 0.5 to 64. Then try it from 0. What does the
   error say about the domain of $\log_2 x$?

```python exec
id: drawing-a-gaps-your-turn
import math
# Your checks and graphs here
```

## What a graph shows that a table hides

Here is one more rule, $y = x^2 - 7x + 12.24$. The table works out
every whole number from 0 to 7. Does the rule ever cross zero?

```python exec
id: drawing-a-hides-1
def close_call(x):
    """Return x squared, take away 7x, add 12.24."""
    return evaluate([12.24, -7, 1], x)


for x in range(0, 8):
    print(x, round(close_call(x), 2))
```

Every value in the table is above 0. The smallest are 0.24, at 3 and at
4. From the table, you would say this rule never reaches zero. Now draw
it. `plt.figure()` starts a second picture, which zooms in between 3
and 4.

```python exec
id: drawing-a-hides-2
plot_rule(close_call, 0, 7)
plt.figure()
plot_rule(close_call, 3, 4)
```

In the first picture, the curve seems to touch the x-axis at its
lowest point and go no further. The zoom tells a different story: the
curve dips below the x-axis, between two rows of the table. It has two
roots, close together, at about 3.4 and 3.6. The table was right about
every row it had. It had no row where the dip was, and the first
picture was drawn at a size where the dip was too small to see. Let's check
the roots by substituting. The values are floats, so we use
`close_enough`:

```python exec
id: drawing-a-hides-3
print(close_call(3.4), close_call(3.6))
print(close_enough(close_call(3.4), 0), close_enough(close_call(3.6), 0))
```

Both are 0, to within a tiny float error. A table gives exact values,
one row at a time. A graph gives the shape at a glance: where it rises
and falls, where it turns, and how many times it crosses. A graph drawn
from only the 8 rows of the table would have missed the dip too. That
is why `plot_rule` works out 401 points.

<details class="dl-why"><summary>Why this way?</summary>

This page let the computer draw every graph, from 401 points. The usual
school way is to plot by hand: make a table of about seven values, mark
each point on squared paper, and join them with a pencil.

Plotting by hand is slow on purpose. Each point is one you worked out
yourself, and after a few you know the shapes of lines and parabolas by
heart. It is also what many exams ask for.

We drew by computer because it makes a graph cheap, so we could draw
many and compare them. The cost is that a picture on a screen can
feel like the truth. The last section is there to show that a picture
is only as good as the points behind it.

</details>

## Four questions, looking back

| The question | On this page |
|---|---|
| What is named here? | a point, by its coordinates $(x, y)$; the output, $y = f(x)$; a root, an $x$ where the value is 0; a rule, by `rule.__name__` |
| What is promised? | `plot_rule` promises the graph of any rule over a range, with the axes through 0; a graph promises only as much as its points |
| What happens when? | the table of points is worked out first, then drawn; left of a crossing one plan is cheaper, right of it the other |
| What does this space let us do? | a flat grid of pairs; $\frac{1}{x}$ has a gap at 0 and $\log_2 x$ needs $x > 0$; the ball's model means nothing after it lands |

## What we have now

| Term or tool | What it means |
|---|---|
| coordinates, $(x, y)$ | a pair of numbers that places a point: $x$ across, $y$ up |
| x-axis, y-axis, origin | the line across, the line up, and the point $(0, 0)$ where they cross |
| graph of a function | the picture of every pair $(x, f(x))$ for $x$ in the domain |
| `plot_rule(rule, low, high)` | your toolkit tool: draws the graph of `rule` from `low` to `high`, with the axes through 0 |
| root | an $x$ where a function's value is 0; where its graph meets the x-axis |
| solving from a graph | reading an answer off a graph, then checking it by substituting |
| linear function, $y = mx + c$ | a straight-line graph; $m$ says how steep, $c$ where it crosses the y-axis |
| where two graphs meet | the $x$ where two rules give the same value |
| parabola | the graph of a quadratic: a U when the $x^2$ coefficient is positive, upside down when negative |
| a cubic's graph | turns up to twice, crosses the x-axis up to three times |
| a gap in a graph | an $x$ outside the domain, like 0 for $\frac{1}{x}$ |
| `plt.legend()` | shows which line is which, using each line's label |

The practice page is next. On the next page,
[Solving for x](tutorial:solving-for-x), we find where the phone plans
meet with no picture at all.
