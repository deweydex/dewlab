---
title: "Straight lines: slope, midpoint and distance — Practice"
practice_for: lines-and-distances
year: "2026-2027"
version: 2026.08.23.1
---

# Straight lines: slope, midpoint and distance — Practice

Each answer is hidden until you open it. Write something down first,
even a guess, and then open the answer to compare.

The cell below has `slope`, `midpoint` and `distance`, for checking your
work.

## Tools

```python exec
id: tools-1
import math

def slope(p, q):
    (x1, y1), (x2, y2) = p, q
    return (y2 - y1) / (x2 - x1)


def midpoint(p, q):
    (x1, y1), (x2, y2) = p, q
    return ((x1 + x2) / 2, (y1 + y2) / 2)


def distance(p, q):
    (x1, y1), (x2, y2) = p, q
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


print(slope((0, 0), (3, 6)))
print(midpoint((1, 2), (7, 6)))
print(distance((0, 0), (3, 4)))
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

The last line is horizontal. $y$ does not change at all when $x$
changes, so the rate of change is zero.

</details>

**2.** What is the slope of the line through $(3, 1)$ and $(3, 9)$?

<details class="dl-answer"><summary>answer</summary>

This line has no slope. Both points have $x = 3$, so the run is zero,
and we cannot divide by zero.

The slope asks "how much does $y$ change when $x$ goes up by one?" On
this line $x$ never goes up, so the question has no answer. This is the
vertical line that $y = mx + c$ cannot describe, and it is why the form
$ax + by + c = 0$ exists.

</details>

**3.** A line passes through $(1, 4)$, $(3, 10)$ and $(6, k)$. Find $k$.

<details class="dl-answer"><summary>answer</summary>

The slope from the first two points is $\dfrac{10 - 4}{3 - 1} = 3$.

A straight line has the same slope everywhere. So from $(1, 4)$ to
$(6, k)$ the slope must also be 3:

$$\frac{k - 4}{6 - 1} = 3$$

So $k - 4 = 15$, and $k = 19$.

</details>

**4.** A mobile phone plan costs €12 a month, plus 6 cent a minute.
Write it as $y = mx + c$. What does each of the two numbers mean?

<details class="dl-answer"><summary>answer</summary>

$y = 0.06x + 12$, where $x$ is the number of minutes and $y$ is the
cost in euro.

The 0.06 is the rate: what one more minute costs. The 12 is what you
pay for zero minutes. This is the fixed monthly charge.

</details>

**5.** Two points on a line are $(10, 250)$ and $(30, 610)$. Here $x$ is
the number of items made, and $y$ is the total cost in euro. What is
the cost for each item, and what is the fixed cost?

<details class="dl-answer"><summary>answer</summary>

The slope is $\dfrac{610 - 250}{30 - 10} = 18$, so each item costs €18.

To find the fixed cost, work back to $x = 0$: $250 - 10 \times 18 = 70$.
The fixed cost is €70.

</details>

## Parallel and perpendicular

**6.** Which of these lines are parallel, and which are perpendicular?

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

**7.** Find the line through $(2, 3)$ that is perpendicular to
$y = 4x - 1$.

<details class="dl-answer"><summary>answer</summary>

The perpendicular slope is $-\tfrac{1}{4}$, because
$4 \times \left(-\tfrac{1}{4}\right) = -1$.

The line passes through $(2, 3)$, so
$3 = -\tfrac{1}{4} \times 2 + c$. That gives $c = 3.5$.

The line is $y = -0.25x + 3.5$.

</details>

**8.** A triangle has corners at $(0, 0)$, $(4, 0)$ and $(4, 3)$. Does it
have a right angle? Show it in two ways.

<details class="dl-answer"><summary>answer</summary>

Yes, at $(4, 0)$.

1. **By slopes.** The side from $(0, 0)$ to $(4, 0)$ is flat, with
   slope 0. The side from $(4, 0)$ to $(4, 3)$ is vertical. A flat line
   and a vertical line meet at a right angle.
2. **By Pythagoras.** The sides are 4, 3 and 5, and
   $4^2 + 3^2 = 16 + 9 = 25 = 5^2$.

</details>

**9.** Why do the slopes of perpendicular lines multiply to $-1$, and
not to some other number?

<details class="dl-answer"><summary>answer</summary>

Turning a right-angled triangle a quarter turn swaps its rise and its
run, and makes one of them negative. So a slope of
$\dfrac{\text{rise}}{\text{run}}$ becomes $\dfrac{\text{run}}{-\text{rise}}$,
or $\dfrac{-\text{run}}{\text{rise}}$.

Multiply the two slopes together. The rise and the run cancel
completely, and $-1$ is left. The swap makes everything cancel, and the
change of sign is all that remains.

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

<details class="dl-answer"><summary>answer</summary>

$4y = -3x + 12$, so $y = -0.75x + 3$.

The line crosses the vertical axis at 3 (set $x = 0$). It crosses the
horizontal axis at 4 (set $y = 0$).

</details>

**12.** What does $ax + by + c = 0$ become when $b = 0$? What about when
$a = 0$?

<details class="dl-answer"><summary>answer</summary>

When $b = 0$, we get $ax + c = 0$, so $x = -\tfrac{c}{a}$. This is a
vertical line, which the other forms cannot describe.

When $a = 0$, we get $by + c = 0$, so $y = -\tfrac{c}{b}$. This is a
horizontal line, which the other forms can describe.

If both are zero, we get $c = 0$. That is either true for every point
or for none, so it is not a line.

</details>

## Midpoint and distance

**13.** Find the midpoint of $(2, 8)$ and $(6, 2)$. Then find the
midpoint of $(-3, 4)$ and $(5, -2)$.

<details class="dl-answer"><summary>answer</summary>

$(4, 5)$ and $(1, 1)$.

</details>

**14.** The midpoint of a line segment is $(3, 1)$, and one end is
$(7, 4)$. Where is the other end?

<details class="dl-answer"><summary>answer</summary>

$(-1, -2)$.

The midpoint is the average of the two ends. To get from $(7, 4)$ to
the midpoint, we move 4 left and 3 down. The other end is the same move
again from the midpoint: $(3 - 4, 1 - 3) = (-1, -2)$.

</details>

**15.** Find the distance between each pair of points.

- (a) $(0, 0)$ and $(3, 4)$
- (b) $(1, 2)$ and $(4, 6)$
- (c) $(-2, 3)$ and $(4, -1)$
- (d) $(5, 5)$ and $(5, 12)$

<details class="dl-answer"><summary>answer</summary>

(a) 5

(b) 5

(c) $\sqrt{52} \approx 7.211$

(d) 7

The last one needs no square root. The two points are on a vertical
line, so the distance is the difference in the $y$ values.

</details>

**16.** A triangle has corners at $(0, 0)$, $(6, 0)$ and $(3, 4)$. Is it
isosceles?

<details class="dl-answer"><summary>answer</summary>

Yes. The base is 6, and both sloping sides are
$\sqrt{9 + 16} = 5$.

</details>

**17.** Two servers in a data centre are at grid positions $(12, 30)$
and $(45, 74)$, in metres. A cable runs straight between them. How long
does the cable need to be?

<details class="dl-answer"><summary>answer</summary>

$\sqrt{33^2 + 44^2} = \sqrt{1089 + 1936} = \sqrt{3025} = 55$ m.

This is a 3-4-5 triangle, made 11 times bigger. These triangles turn up
often, and spotting one saves a calculation.

</details>

**18.** Show that $(1, 2)$, $(4, 6)$ and $(8, 3)$ make a right-angled
triangle. Which corner has the right angle?

<details class="dl-answer"><summary>answer</summary>

The three side lengths are 5, 5 and $\sqrt{50}$. Since
$25 + 25 = 50$, Pythagoras' theorem holds. The right angle is at
$(4, 6)$, the corner opposite the longest side.

The triangle is also isosceles, because two of its sides are equal.

</details>

**19.** Why is the distance formula the same thing as Pythagoras'
theorem?

<details class="dl-answer"><summary>answer</summary>

Draw the gap across and the gap up between two points. The two gaps
meet at a right angle. The straight-line distance is the third side of
that triangle.

So $\text{distance}^2 = \text{across}^2 + \text{up}^2$ is exactly
$c^2 = a^2 + b^2$, with the two gaps as the two short sides. Neither is
a special case of the other. They are one statement.

</details>

## Putting it together

**20.** A drone is at $(0, 0)$. There are two landing pads, at
$(30, 40)$ and $(-20, 45)$. Which pad is closer, and by how much?

<details class="dl-answer"><summary>answer</summary>

The first pad is 50 away. The second is
$\sqrt{400 + 2025} = \sqrt{2425} \approx 49.24$ away.

The second pad is closer, by about 0.76. That is so close that a guess
from the picture would not be reliable.

</details>

**21.** Find the point on the horizontal axis that is the same distance
from $(0, 4)$ and from $(6, 2)$.

<details class="dl-answer"><summary>answer</summary>

Call the point $(x, 0)$. The two squared distances must be equal:

$$x^2 + 16 = (x - 6)^2 + 4$$

Multiplying out the bracket gives $x^2 + 16 = x^2 - 12x + 40$. So
$12x = 24$, and $x = 2$.

The point is $(2, 0)$. It is $2\sqrt{5}$ from each of the two points.

</details>

**22.** A circle has its centre at $(3, 1)$, and it passes through
$(7, 4)$. What is its radius? Is the point $(0, 5)$ inside the circle or
outside it?

<details class="dl-answer"><summary>answer</summary>

The radius is the distance from the centre to the point we know:
$\sqrt{16 + 9} = 5$.

The point $(0, 5)$ is $\sqrt{9 + 16} = 5$ from the centre. So it is
exactly on the circle: neither inside nor outside.

</details>

**23.** Write a function that takes three points and says whether they
lie on one straight line.

<details class="dl-answer"><summary>answer</summary>

Compare the slope between the first two points with the slope between
the last two. If the slopes are equal, the three points lie on one
straight line. Points like this are called collinear.

```python
def collinear(p, q, r):
    return abs(slope(p, q) - slope(q, r)) < 1e-9
```

The tolerance, `1e-9`, matters. Floats are not always exact, so testing
for exact equality can call a perfectly straight set of points bent.
For example, $(0, 0)$, $(1, 0.1)$ and $(3, 0.3)$ lie on one line. But
Python computes their two slopes as `0.1` and `0.09999999999999999`, so
an exact `==` test says no.

This version also fails if any pair of points is on a vertical line,
because `slope` divides by zero. It is worth guarding against that. One
way is to compare $(y_2 - y_1)(x_3 - x_2)$ with $(y_3 - y_2)(x_2 - x_1)$,
which avoids dividing at all:

```python
def collinear(p, q, r):
    (x1, y1), (x2, y2), (x3, y3) = p, q, r
    return abs((y2 - y1) * (x3 - x2) - (y3 - y2) * (x2 - x1)) < 1e-9
```

</details>
