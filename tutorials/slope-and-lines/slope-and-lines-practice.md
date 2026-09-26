---
title: "Straight lines: slope, and the line that breaks the formula — Practice"
practice_for: slope-and-lines
year: "2026-2027"
version: 2026.09.26.1
worlds:
  sea-and-sky: Ships' courses on a chart. The numbers are made up.
  sound: Echoes from a cliff.
  planets-and-moons: The Moon, slowly moving away from the Earth.
  fantasy-maps: A made-up kingdom and its straight roads. The numbers are made up.
---

# Straight lines: slope, and the line that breaks the formula — Practice

Each answer is hidden until you open it. Write something down first,
even a guess, and then open the answer to compare.

The cell below has `slope` and `to_slope_intercept`, for checking your
work.

## Tools

```python exec
id: tools-1
def slope(p, q):
    """The slope of the line through two points, each given as (x, y)."""
    (x1, y1), (x2, y2) = p, q
    return (y2 - y1) / (x2 - x1)


def to_slope_intercept(a, b, c):
    """ax + by + c = 0 becomes y = mx + c, when it can."""
    if b == 0:
        return "Vertical: this line has no slope-intercept form."
    return (-a / b, -c / b)


print(slope((0, 0), (3, 6)))
print(to_slope_intercept(2, -1, 1))
```

## Slope

**1.** Find the slope of the line through each pair of points.

- (a) $(0, 0)$ and $(4, 8)$
- (b) $(2, 5)$ and $(6, 1)$
- (c) $(-3, -2)$ and $(1, 6)$
- (d) $(4, 7)$ and $(9, 7)$

<details class="dl-answer"><summary>answer</summary>

(a) 2

(b) $-1$

(c) 2

(d) 0

The last line is flat. $y$ does not change at all when $x$ changes, so
the rate of change is zero.

</details>

**2.** The cell finds the slope between the same two points twice, once
in each order.

```python exec
id: slope-practice-1
print(slope((2, 5), (6, 1)))
print(slope((6, 1), (2, 5)))
```

```predict
type: number

The first line prints -1.0. What will the second line print?
```

<details class="dl-answer"><summary>why</summary>

Both lines print $-1.0$. When we swap the points, the rise changes sign
and the run changes sign. A negative divided by a negative is the same
as the positive divided by the positive, so the slope does not change.

</details>

**3.** What is the slope of the line through $(3, 1)$ and $(3, 9)$?

<details class="dl-answer"><summary>answer</summary>

This line has no slope. Both points have $x = 3$, so the run is zero,
and we cannot divide by zero.

This is the vertical line that $y = mx + c$ cannot describe. The form
$ax + by + c = 0$ can describe it: $x - 3 = 0$.

</details>

**4.** A line passes through $(1, 4)$, $(3, 10)$ and $(6, k)$. What is
$k$?

<details class="dl-hint"><summary>hint</summary>

A straight line has the same slope between any two of its points.

</details>

<details class="dl-answer"><summary>one way through it</summary>

The slope from the first two points is $\dfrac{10 - 4}{3 - 1} = 3$.

From $(1, 4)$ to $(6, k)$ the slope must also be 3:

$$\frac{k - 4}{6 - 1} = 3$$

So $k - 4 = 15$, and $k = 19$.

</details>

**5.** A mobile phone plan costs €12 a month, plus 6 cent a minute.
Can you write it as $y = mx + c$? What does each of the two numbers
mean?

<details class="dl-answer"><summary>answer</summary>

$y = 0.06x + 12$, where $x$ is the number of minutes and $y$ is the
cost in euro.

The 0.06 is the rate. It is the cost of one more minute. The 12 is the
cost for zero minutes, which is the fixed monthly charge.

</details>

**6.** Two points on a line are $(10, 250)$ and $(30, 610)$. Here $x$ is
the number of items a workshop makes, and $y$ is the total cost in euro.
What does each item cost, and what is the fixed cost?

<details class="dl-answer"><summary>answer</summary>

The slope is $\dfrac{610 - 250}{30 - 10} = 18$, so each item costs €18.

To find the fixed cost, go back to $x = 0$: $250 - 10 \times 18 = 70$.
The fixed cost is €70.

</details>

## Parallel and perpendicular

**7.** Which of these lines are parallel, and which are perpendicular?

- (a) $y = 3x + 1$
- (b) $y = 3x - 7$
- (c) $y = -\tfrac{x}{3} + 2$
- (d) $y = \tfrac{x}{3}$

<details class="dl-answer"><summary>answer</summary>

(a) and (b) are parallel. They have the same slope, 3.

(c) is perpendicular to both (a) and (b), because
$3 \times \left(-\tfrac{1}{3}\right) = -1$.

(d) is not parallel or perpendicular to any of the others. Its slope is
$\tfrac{1}{3}$, not $-\tfrac{1}{3}$. The sign is easy to miss.

</details>

**8.** A triangle has corners at $(0, 0)$, $(4, 0)$ and $(4, 3)$. Does
it have a right angle? What do the slopes of its sides say?

<details class="dl-answer"><summary>answer</summary>

Yes, at $(4, 0)$. The side from $(0, 0)$ to $(4, 0)$ is flat, with
slope 0. The side from $(4, 0)$ to $(4, 3)$ is vertical. A flat line
and a vertical line meet at a right angle. The rule about multiplying
to $-1$ cannot say this, because the vertical side has no slope.

</details>

**9.** Why do the slopes of perpendicular lines multiply to $-1$, and
not to some other number?

<details class="dl-answer"><summary>answer</summary>

Turning a right-angled triangle a quarter turn swaps its rise and its
run, and makes one of them negative. So a slope of
$\dfrac{\text{rise}}{\text{run}}$ becomes $\dfrac{\text{run}}{-\text{rise}}$.

Multiply the two slopes together. The rise and the run cancel, and
$-1$ is left.

</details>

## The general form

**10.** Write each line in the form $ax + by + c = 0$.

- (a) $y = 2x + 5$
- (b) $y = -3x$
- (c) the vertical line through $(7, 0)$
- (d) the horizontal line through $(0, -4)$

<details class="dl-answer"><summary>answer</summary>

(a) $2x - y + 5 = 0$

(b) $3x + y = 0$

(c) $x - 7 = 0$

(d) $y + 4 = 0$

Only (c) could not be written as $y = mx + c$.

</details>

**11.** Change $3x + 4y - 12 = 0$ into the form $y = mx + c$. Where does
the line cross each axis?

<details class="dl-answer"><summary>one way through it</summary>

$4y = -3x + 12$, so $y = -0.75x + 3$.

The line crosses the vertical axis at 3 (put $x = 0$). It crosses the
horizontal axis at 4 (put $y = 0$).

</details>

**12.** What does $ax + by + c = 0$ become when $b = 0$? What about when
$a = 0$?

<details class="dl-answer"><summary>answer</summary>

When $b = 0$, we get $ax + c = 0$, so $x = -\tfrac{c}{a}$. This is a
vertical line, which the other forms cannot describe.

When $a = 0$, we get $by + c = 0$, so $y = -\tfrac{c}{b}$. This is a
flat line, which the other forms can describe.

If both are zero, we get $c = 0$. That is either true for every point
or for none, so it is not a line.

</details>

**13.** Somebody wrote their own `to_slope_intercept`. For
$2x - y + 1 = 0$, which is $y = 2x + 1$, it returns `(-2.0, -1.0)`.
Can you find the mistake, and fix it?

```python exec
id: the-general-form-1
def to_slope_intercept(a, b, c):
    """ax + by + c = 0 becomes y = mx + c, when it can."""
    if b == 0:
        return "Vertical: this line has no slope-intercept form."
    return (a / b, c / b)


print(to_slope_intercept(2, -1, 1))
```

```hint
Start from $ax + by + c = 0$ and get $y$ on its own, on paper. What
happens to $ax$ and $c$ when they move to the other side?
```

```inputs
to_slope_intercept(2, -1, 1)
to_slope_intercept(3, 4, -12)
to_slope_intercept(1, 0, -3)
```

```solution
def to_slope_intercept(a, b, c):
    """ax + by + c = 0 becomes y = mx + c, when it can."""
    if b == 0:
        return "Vertical: this line has no slope-intercept form."
    return (-a / b, -c / b)
---
Moving $ax$ and $c$ to the other side changes their signs:
$by = -ax - c$. Then dividing by $b$ gives $y = -\tfrac{a}{b}x - \tfrac{c}{b}$.
The two minus signs were missing.
```

## Your world

**14.** A problem from the world you chose.

<div class="dl-world" data-world="sea-and-sky">

Two ships sail straight courses on a chart. The first passes $(2, 1)$
and $(6, 9)$. The second passes $(0, 5)$ and $(4, 3)$. Do their courses
cross at a right angle? Can you write `at_right_angles(first, second)`,
which takes two courses, each a pair of points?

```python exec
id: your-world-1--sea-and-sky
first = ((2, 1), (6, 9))
second = ((0, 5), (4, 3))
```

```hint
Find the slope of each course. What do the two slopes multiply to? A
float may be a tiny bit away from $-1$.
```

```inputs
at_right_angles(first, second)
at_right_angles(((0, 0), (3, 1)), ((0, 0), (1, -3)))
at_right_angles(((0, 0), (1, 1)), ((0, 0), (1, -2)))
```

```solution
def at_right_angles(first, second):
    product = slope(*first) * slope(*second)
    return abs(product + 1) < 1e-9
---
The slopes are 2 and $-0.5$, and $2 \times (-0.5) = -1$, so the courses
cross at a right angle. `slope(*first)` gives `slope` the two points in
`first`, one by one.
```

</div>

<div class="dl-world" data-world="sound">

You shout at a cliff, and the echo returns after a number of
seconds. Sound travels about 343 metres every second, and it goes to
the cliff and back. Can you write `cliff_distance(seconds)`? What is
the slope of this line, and what does it mean?

```python exec
id: your-world-1--sound
speed_of_sound = 343    # metres every second
```

```hint
In 1 second the sound goes 343 m. How much of that is the way out to
the cliff?
```

```inputs
cliff_distance(1)
cliff_distance(2)
cliff_distance(0.5)
```

```solution
def cliff_distance(seconds):
    return speed_of_sound * seconds / 2
---
The slope is 171.5: every extra second of echo means the cliff is 171.5
metres further away. It is half the speed of sound, because the sound
travels the distance twice.
```

</div>

<div class="dl-world" data-world="planets-and-moons">

The Moon moves away from the Earth by about 3.8 cm every year. Lasers
fired at mirrors that the Apollo astronauts left on the Moon measure
this. Can you write `years_to_move(km)`, the number of years the Moon
takes to move that many kilometres further away? One kilometre is
100,000 cm.

```python exec
id: your-world-1--planets-and-moons
cm_each_year = 3.8
```

```hint
The distance added is a line, $y = 3.8x$, with $x$ in years and $y$ in
centimetres. Which way do you need to use it?
```

```inputs
years_to_move(1)
years_to_move(384.4)
```

```solution
def years_to_move(km):
    return km * 100000 / cm_each_year
---
One kilometre takes about 26,300 years. The Moon is about 384,400 km
away, and moving a tenth of a percent of that, 384.4 km, takes about
10 million years.
```

</div>

<div class="dl-world" data-world="fantasy-maps">

The King's Road is the line $y = 0.5x + 3$. A new path leaves the tower
at $(6, 7)$ and meets the road at a right angle. This is the shortest
way from the tower to the road. Where does the path meet the road? Can
you write `foot(m, c, point)`, which finds where the path at right
angles from `point` meets the line $y = mx + c$?

```python exec
id: your-world-1--fantasy-maps
tower = (6, 7)
```

```hint
First find the path's own line: its slope, and its intercept through
the tower. Then find where two lines meet, as in
[Solving equations: linear, quadratic and simultaneous](tutorial:cracking-equations).
```

```inputs
foot(0.5, 3, tower)
foot(1, 0, (0, 2))
foot(-2, 4, (0, 0))
```

```solution
def foot(m, c, point):
    x, y = point
    path_m = -1 / m
    path_c = y - path_m * x
    meet_x = (path_c - c) / (m - path_m)
    return meet_x, m * meet_x + c
---
The path is $y = -2x + 19$, and it meets the King's Road at $(6.4, 6.2)$.
That is less than a kilometre from the tower. `foot` stops with a
`ZeroDivisionError` for a flat road, where the path would be vertical.
```

</div>

## From earlier

**15.** From
[Solving equations: linear, quadratic and simultaneous](tutorial:cracking-equations).
Where do $y = 2x + 1$ and $y = -x + 7$ cross? What are their slopes,
and are they perpendicular?

<details class="dl-answer"><summary>one way through it</summary>

Where they cross, the two $y$ values are equal: $2x + 1 = -x + 7$. So
$3x = 6$, $x = 2$, and $y = 5$. They cross at $(2, 5)$.

Their slopes are 2 and $-1$, which multiply to $-2$. They cross, but
not at a right angle.

</details>

**16.** From [Number types, powers and logarithms](tutorial:numbers-and-their-families).
`slope((1, 2), (4, 3))` prints `0.3333333333333333`. Can you use
`Fraction` to find the slope exactly?

```python exec
id: from-earlier-1
from fractions import Fraction

# Your code here.
```

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Yours may be different and work too.

`Fraction(3 - 2, 4 - 1)` is `Fraction(1, 3)`. The rise and the run are
whole numbers, so `Fraction` can keep the slope exact, where a float
cannot.

</details>
