---
title: "Putting the derivative to work: choose a project"
year: "2026-2027"
version: 2026.09.25.1
datasets: [life-expectancy]
covers:
  one-idea-four-jobs:
    touches: [MIT-3.6]
  project-1-where-does-the-letter-sit:
    touches: [MIT-3.6, MIT-3.4]
  project-2-finding-an-edge:
    touches: [MIT-3.6, MIT-6.3, MIT-6.7]
  project-3-the-best-line-through-data:
    touches: [MIT-3.7, MIT-5.12, MIT-4.2]
  project-4-walking-downhill:
    touches: [MIT-3.6, PDP-LO2]
---

# Putting the derivative to work: choose a project

You have spent three pages building one idea: the slope of a curve at
a single point. It is fair to ask what it is for. This page answers
with four short projects, and you choose. A font designer, a photo
app, a scientist with a table of data, and a program that learns all
lean on the same idea, and each project shows one of them. Choose one,
or do more than one if you like. None of them needs another.

On this page we:

- see the two questions a derivative answers: where is it flat, and
  where is it steep?
- choose one or more projects: the bottom of a letter, an edge in a
  picture, the best line through real Irish data, or walking downhill
  to the bottom of a curve
- finish each project with a check of its own

> **The space we're in.** Everything from this unit is in your toolkit:
> `derivative_at`, `bisect_root` and `newton`, with `vertex`,
> `solve_quadratic`, `smallest` and the rest from earlier units. Some
> projects use rules, some use lists of measured numbers, and one uses
> a picture made of numbers. One thing usually goes unsaid: a real
> problem does not tell you which tool it wants. Choosing is part of
> the work, and here you choose the problem too.

## Warm-up

The first question is from
[How fast, right now?](tutorial:how-fast-right-now#the-tangent-line),
and the second from
[Solving by computing](tutorial:solving-by-computing#a-tool-that-halves).

```question
id: putting-warm-up-1
type: multiple-choice
correct: 2

At the lowest point of a smooth curve, the tangent line is:

- as steep as it gets
- flat, with a slope of 0
- straight up and down
```

```question
id: putting-warm-up-2
type: fill-in-the-blank

`bisect_root(rule, low, high)` needs `rule(low)` and `rule(high)` to
have {opposite|the same|no} signs.
```

## One idea, four jobs

A derivative answers two questions about a curve, and between them
they cover all four projects.

1. **Where is it flat?** A slope of 0 marks a place where the curve
   turns: a top or a bottom. Projects 1, 3 and 4 look for it.
2. **Where is it steep?** A large slope, up or down, marks a place
   where things change fast. Project 2 looks for it.

Here are both on one curve, the sine wave from
[Waves](tutorial:waves). Before you run it, guess: where is the slope
0, and where is it steepest?

```python exec
id: putting-one-idea-1
import math

for tenths in range(0, 64, 4):
    x = tenths / 10
    print(x, round(math.sin(x), 2), round(derivative_at(math.sin, x), 2))
```

The slope, in the last column, is near 0 at about 1.6 and 4.8, the top
and the bottom of the wave. It is largest, near 1 or $-1$, at 0, 3.2
and 6.0, where the wave crosses the middle. Flat means "turning here".
Steep means "changing fast here".

Here are the projects. Each takes a few cells, and each ends with a
`check()` that says whether you got there.

| Project | The question | What it uses |
|---|---|---|
| 1. Where does the letter sit? | How far does a round letter dip below the line? | flat: `derivative_at`, `bisect_root` |
| 2. Finding an edge | Where does a picture change from dark to light? | steep: differences between neighbours |
| 3. The best line through data | Which line fits Ireland's life expectancy best? | flat: the slope of an error |
| 4. Walking downhill | How does a program find the bottom of a curve by feel? | flat, found by stepping |

## Project 1: Where does the letter sit?

On [The top of the curve](tutorial:the-top-of-the-curve#a-letter-that-sits-below-the-line),
the bottom of a letter's bowl was a quadratic Bézier curve, and its
lowest point was a vertex, 9 font units below the baseline. Completing
the square found it. Many fonts use a *cubic Bézier curve* instead,
with two control points, and then the height is a cubic in $t$.
Completing the square cannot touch a cubic. A slope of 0 can.

First, the old bowl the new way, as a warm-up. Where do you expect the
slope to be 0?

```python exec
id: putting-letter-1
def bowl_height(t):
    """Return the height of the quadratic bowl, in font units, at t from 0 to 1."""
    return 400 * t ** 2 - 440 * t + 112

def bowl_slope(t):
    return derivative_at(bowl_height, t)

flat_t = bisect_root(bowl_slope, 0, 1)
print(flat_t, bowl_height(flat_t))
print(vertex(400, -440, 112))
```

The same bottom, $t = 0.55$ and $-9$, by a route that does not care
what shape the rule is. Now a cubic bowl, with its start at height
130, control points at $-60$ and $-50$, and its end at 110. Its height
is a mix of four heights:

$$y = (1 - t)^3 \times 130 + 3t(1 - t)^2 \times (-60) + 3t^2(1 - t) \times (-50) + t^3 \times 110$$

```python exec
id: putting-letter-2
import matplotlib.pyplot as plt

def cubic_point(start, pull_1, pull_2, end, t):
    """Return one coordinate of a cubic Bézier curve at t, from its four points."""
    return ((1 - t) ** 3 * start + 3 * t * (1 - t) ** 2 * pull_1
            + 3 * t ** 2 * (1 - t) * pull_2 + t ** 3 * end)

def cubic_height(t):
    return cubic_point(130, -60, -50, 110, t)

def cubic_slope(t):
    return derivative_at(cubic_height, t)

lowest_t = bisect_root(cubic_slope, 0, 1)
lowest_height = cubic_height(lowest_t)
print(lowest_t, lowest_height)

ts = [step / 100 for step in range(0, 101)]
plt.plot([cubic_point(80, 150, 360, 470, t) for t in ts], [cubic_height(t) for t in ts])
plt.plot(cubic_point(80, 150, 360, 470, lowest_t), lowest_height, "o", color="C3")
plt.axhline(0, color="black", linewidth=1)
plt.gca().set_aspect("equal")
```

The bowl is lowest at $t \approx 0.507$, about 11.3 units below the
baseline. No formula from Unit 7 could have found that, and the slope
found it in one line. Is the dip the right size? Designers aim for
about 1% to 3% of the letter's height, and this letter is 500 units
tall.

```python exec
id: putting-letter-check
overshoot_percent = -lowest_height / 500 * 100
print(round(overshoot_percent, 2), "% of the letter's height")
check(1 <= overshoot_percent <= 3, True, label="the dip is 1% to 3% of the height")
```

**Try this next:** change the two control heights, $-60$ and $-50$, and
run the cells again. Can you make a dip of exactly 2%? Can you make a
curve with a top and a bottom, like the middle of a letter "s"? Then
the slope is 0 in two places, and `bisect_root` needs a `low` and
`high` round each one.

## Project 2: Finding an edge

A photo is a grid of numbers, one brightness per pixel, from 0 for
black to 255 for white, as on
[Everything is ones and zeros](tutorial:everything-is-ones-and-zeros).
Here is one row of pixels, across a dark pen stroke on white paper.
The numbers are made up, but they have the shape a real scan has: the
edges are a little soft.

```python exec
id: putting-edge-1
row = [250, 251, 249, 250, 248, 200, 90, 30, 28, 31, 29, 30, 27, 32, 85, 190, 247, 250, 251, 249]
```

On [Getting closer](tutorial:getting-closer#when-the-two-sides-disagree),
a perfect edge was a jump. In a real picture the jump is spread over a
pixel or two, so the edge is where the brightness changes fastest.
That is a large slope. With pixels, the smallest step is one pixel, so
the slope is the difference between neighbours: a chord one pixel
long. Before you run it, which differences will be biggest?

```python exec
id: putting-edge-2
import matplotlib.pyplot as plt

differences = []
for i in range(len(row) - 1):
    differences.append(row[i + 1] - row[i])
print(differences)

figure, (top, bottom) = plt.subplots(2, 1, figsize=(6, 4), sharex=True)
top.plot(row, "o-")
top.set_ylabel("brightness")
bottom.bar([i + 0.5 for i in range(len(differences))], differences)
bottom.set_ylabel("difference")
bottom.set_xlabel("pixel")
```

Most differences are tiny, a pixel or two of noise. Two stand out:
$-110$, from pixel 5 to 6, going into the stroke, and $+105$, from
pixel 14 to 15, coming out. Those are the edges. Let's find them with
a rule: any difference bigger than 100, either way.

```python exec
id: putting-edge-check
big_steps = []
for i in range(len(differences)):
    if abs(differences[i]) > 100:
        big_steps.append(i)
print(big_steps)
check(big_steps, [5, 14], label="both edges of the stroke")
```

Now a whole picture. This cell draws a letter "o" as a grid of 40 by
40 pixels with `numpy`, which met rows of numbers on
[A row of numbers](tutorial:a-row-of-numbers). It then
takes differences along each row and down each column, and marks a
pixel as an edge when either one is big. What do you expect the edges
to look like?

```python exec
id: putting-edge-3
import numpy as np

down, across = np.mgrid[0:40, 0:40]
distance_from_centre = np.hypot(across - 20, down - 20)
picture = np.where((distance_from_centre >= 8) & (distance_from_centre <= 14), 30, 250)

across_differences = np.abs(np.diff(picture, axis=1, append=picture[:, -1:]))
down_differences = np.abs(np.diff(picture, axis=0, append=picture[-1:, :]))
edges = (across_differences > 100) | (down_differences > 100)

figure, (left, right) = plt.subplots(1, 2, figsize=(6, 3))
left.imshow(picture, cmap="gray", vmin=0, vmax=255)
left.set_title("the picture")
right.imshow(edges, cmap="gray_r")
right.set_title("where it is steep")
print(edges.sum(), "edge pixels")
```

The edges come out as two thin rings, the outline of the "o" inside
and out, and every flat part of the picture is gone. I think that is
a lovely result: a letter's whole shape, found by asking only "where
does the brightness change fast?"

<aside class="dl-note" id="putting-note-sobel">

**Edge detection.** Photo apps and many other programs that look at
pictures find edges in much the same way, with a few refinements. One
of the best known is the Sobel filter, described by Irwin Sobel and
Gary Feldman in 1968.
It takes differences like these, but averages each one with its
neighbours first, so that noise does not look like an edge.

</aside>

**Try this next:** add some noise to the row, for example change 27
to 60. Does the rule still find only two edges? What threshold would
you choose, and why?

## Project 3: The best line through data

In the course's Our World in Data file, Ireland's life expectancy at
birth rose every single year from 1990 to 2016. Is there one straight
line that fits it best, and how fast does it climb?

```python exec
id: putting-line-1
import matplotlib.pyplot as plt
import numpy as np

frame = await load_csv("life-expectancy.csv")
ireland = frame[(frame.country == "Ireland") & (frame.year >= 1990)]
years = ireland["year"].tolist()
lifespans = ireland["life_expectancy"].tolist()
print(len(years), "years, from", years[0], "to", years[-1])
print(lifespans[0], lifespans[-1])
```

Twenty-seven years, from 74.84 to 81.14. "Best" needs a meaning. Here
is the usual one. For each year, measure how far the line misses the
data, square the miss, and add up the squares. The best line makes
that total as small as it can be. This is called *least squares*. A
square is never negative, so a miss above the line and a miss below
both count against it.

One fact makes the maths short: the best line always passes through
the middle of the data, the point (mean year, mean life expectancy).
So we measure every year and value from that middle point. Then the
line is $y = m \times x$, and only its slope $m$ is left to choose.

```python exec
id: putting-line-2
middle_year = mean(years)
middle_lifespan = mean(lifespans)
year_gaps = [year - middle_year for year in years]
lifespan_gaps = [value - middle_lifespan for value in lifespans]

def total_error(m):
    """Return the total squared miss of the line with slope m through the middle point."""
    total_so_far = 0
    for x, y in zip(year_gaps, lifespan_gaps):
        total_so_far = total_so_far + (y - m * x) ** 2
    return total_so_far

for m in [0, 0.1, 0.2, 0.3, 0.4]:
    print(m, round(total_error(m), 2))
```

The error falls and then rises again: it has a bottom. It is a
parabola in $m$, since every miss squared is a quadratic in $m$. So
the best slope is where the error's slope is 0. Your toolkit can find
it with no algebra at all.

```python exec
id: putting-line-3
def error_slope(m):
    return derivative_at(total_error, m)

best_m = bisect_root(error_slope, 0, 0.4)
print(best_m)

plt.plot(years, lifespans, "o")
plt.plot(years, [middle_lifespan + best_m * (year - middle_year) for year in years])
plt.xlabel("year")
plt.ylabel("life expectancy at birth, years")
```

About 0.278 years of life expectancy for every year that passes:
roughly three months and a bit more, every year, for 27 years. The
line runs straight through the dots.

With the rules from
[Rules for change](tutorial:rules-for-change), the slope of the error
can be written out: it is 0 when $m$ is the sum of $x \times y$ over
the sum of $x^2$. `numpy` has a line fitter of its own, `np.polyfit`.
Do all three agree?

```python exec
id: putting-line-check
by_rule = sum(x * y for x, y in zip(year_gaps, lifespan_gaps)) / sum(x * x for x in year_gaps)
by_numpy = np.polyfit(years, lifespans, 1)[0]
print(best_m, by_rule, by_numpy)
check(best_m, by_numpy, tolerance=1e-6, label="your slope matches numpy's")
```

**Try this next:** the file goes back to 1950. Fit a line to 1950 to
2016. Is one straight line still a good fit? What does the picture
say that the slope alone does not?

## Project 4: Walking downhill

Sometimes nobody can solve "slope = 0" at all, because the rule is too
big to write down. Then a program can feel its way down instead. Stand
somewhere on the curve. Find the slope where you stand. Take a small
step the other way, downhill. Repeat. This is *gradient descent*
("gradient" is another word for slope, as on
[Straight lines](tutorial:straight-lines)).

In symbols, each step is $x_{\text{new}} = x - r \times f'(x)$, where
$r$ is a small number that sets the size of the step. Here it is on a
curve with two valleys:

```python exec
id: putting-downhill-1
import matplotlib.pyplot as plt

def valley_rule(x):
    return x ** 4 - 3 * x ** 2 + x + 4

def walk_downhill(start, rate, steps):
    """Return every x visited, stepping against the slope from start."""
    visited = [start]
    x = start
    for step in range(steps):
        x = x - rate * derivative_at(valley_rule, x)
        visited.append(x)
    return visited

path = walk_downhill(2, 0.05, 30)
print([round(x, 3) for x in path[:8]], "...", round(path[-1], 4))

plot_rule(valley_rule, -2.2, 2.2)
plt.plot(path, [valley_rule(x) for x in path], "o", color="C3")
```

From 2, the walk takes one big stride, then small ones, and settles at
about 1.131, the bottom of the right-hand valley. The steps shrink by
themselves, because the slope shrinks as the curve flattens.

How big should the rate be? Pause here and guess what happens with a
rate of 0.3, six times bigger, and with 0.001. Then run it.

```python exec
id: putting-downhill-2
print("rate 0.3:  ", walk_downhill(2, 0.3, 4))
print("rate 0.001:", round(walk_downhill(2, 0.001, 30)[-1], 4))
```

With 0.3, the walk leaps right over the valley to $-4.3$, where the
curve is very steep, then to 83, then to about minus 690,000, then
to a number 18 digits long. It is falling off the world. With 0.001 it is safe, and after 30 steps
it has only crept from 2 to about 1.6. Too big jumps out; too small
takes for ever. Choosing the step is most of the craft.

There is one more surprise. Start on the left, at $-2$:

```python exec
id: putting-downhill-check
left_path = walk_downhill(-2, 0.05, 30)
right_path = walk_downhill(2, 0.05, 30)
print(round(left_path[-1], 4), round(valley_rule(left_path[-1]), 4))
print(round(right_path[-1], 4), round(valley_rule(right_path[-1]), 4))
check(abs(derivative_at(valley_rule, left_path[-1])) < 1e-6, True, label="the walk ended where the curve is flat")
```

From $-2$ the walk ends at about $-1.301$, and that valley is lower,
0.49 against 2.93. The walk from 2 found a bottom, but not the lowest
one. Walking downhill only knows about the ground under its feet.

Training a machine-learning model works this way on a huge scale: its
error depends on millions of numbers, and the training program
steps every one of them against its slope, a little at a time.

**Try this next:** find a start that walks to the left-hand valley,
and a start between the valleys that walks to the right. Where is the
line between them?

<details class="dl-why"><summary>Why this way?</summary>

This page gave you a choice of four projects, and did not ask you to do
all of them. Most courses choose one application for everyone, so
everyone practises the same thing and the teacher can compare the
work.

A shared example is fair and quick to mark. But one example chosen for
everyone suits some readers and leaves the rest asking what the idea
is for. A choice lets you pick the use that makes sense to you, and
every project still turns on the same two questions: where is it flat,
and where is it steep?

The cost is that you may not see all four uses. If you did one, the
other three are still here.

</details>

## Four questions, looking back

| The question | On this page |
|---|---|
| What is named here? | a cubic Bézier curve's four points; a row and a grid of pixels; the total squared error; the step size $r$ |
| What is promised? | a slope of 0 promises a place where a curve turns; a large difference promises an edge; `check()` says whether each project got there |
| What happens when? | gradient descent repeats one move, step against the slope, and the steps shrink as the curve flattens |
| What does this space let us do? | pixels have no step smaller than one, so an edge is a difference, not a limit; walking downhill only sees the ground under it, so it can stop in a valley that is not the lowest |

## What we have now

| Term or tool | What it means |
|---|---|
| flat and steep | a slope of 0 marks a top or a bottom; a large slope marks fast change |
| cubic Bézier curve | a curve from four points, whose height is a cubic in $t$ |
| edge, in a picture | a place where the brightness changes fast: a large difference between neighbours |
| least squares | choosing the line that makes the total of the squared misses as small as it can be |
| gradient descent | finding a bottom by stepping against the slope, again and again |
| step size, or rate | how far each step of gradient descent goes; too big jumps out, too small crawls |

The mixed problems for this unit are next:
[Mixed problems: change](tutorial:mixed-change).
