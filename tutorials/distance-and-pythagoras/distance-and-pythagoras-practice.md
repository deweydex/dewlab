---
title: "Distance and Pythagoras: how far apart two points are — Practice"
practice_for: distance-and-pythagoras
year: "2026-2027"
version: 2026.09.26.1
worlds:
  sea-and-sky: Two lighthouses and a ship between them. The numbers are made up.
  sound: Two microphones and a clap.
  planets-and-moons: The Earth and Venus, with their orbits drawn as circles. The positions are made up.
  fantasy-maps: A made-up kingdom and its buried treasure. The numbers are made up.
---

# Distance and Pythagoras: how far apart two points are — Practice

Each answer is hidden until you open it. Write something down first,
even a guess, and then open the answer to compare.

The cell below has `distance` and `midpoint`, for checking your work.

## Tools

```python exec
id: tools-1
import math

def distance(p, q):
    (x1, y1), (x2, y2) = p, q
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def midpoint(p, q):
    (x1, y1), (x2, y2) = p, q
    return ((x1 + x2) / 2, (y1 + y2) / 2)


print(distance((0, 0), (3, 4)))
print(midpoint((1, 2), (7, 6)))
```

## Distance

**1.** Find the distance between each pair of points.

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

**2.** The distance from $(0, 0)$ to $(1, 1)$ is $\sqrt{2}$. The cell
squares it.

```python exec
id: distance-practice-1
print(distance((0, 0), (1, 1)))
print(distance((0, 0), (1, 1)) ** 2)
```

```predict
type: number

What will the second line print?
```

<details class="dl-answer"><summary>why</summary>

It prints `2.0000000000000004`, not 2. $\sqrt{2}$ has no end to its
decimals, so Python stores a number very close to it. Squaring that
number gives a number very close to 2. This is why the page uses a
small tolerance, such as `1e-9`, to compare two floats.

</details>

**3.** Two servers in a data centre are at grid positions $(12, 30)$
and $(45, 74)$, in metres. A cable runs straight between them. How long
does the cable need to be?

<details class="dl-answer"><summary>answer</summary>

$\sqrt{33^2 + 44^2} = \sqrt{1089 + 1936} = \sqrt{3025} = 55$ m.

This is a 3-4-5 triangle, made 11 times bigger. If you spot one, you
save a calculation.

</details>

**4.** Do $(1, 2)$, $(4, 6)$ and $(8, 3)$ make a right-angled triangle?
If they do, which corner has the right angle?

<details class="dl-answer"><summary>answer</summary>

The three side lengths are 5, 5 and $\sqrt{50}$. Since
$25 + 25 = 50$, Pythagoras' theorem holds. The right angle is at
$(4, 6)$, the corner opposite the longest side.

The triangle is also isosceles, because two of its sides are equal.

</details>

**5.** A triangle has corners at $(0, 0)$, $(4, 0)$ and $(4, 3)$. The
practice page for
[Straight lines: slope, and the line that breaks the formula](tutorial:slope-and-lines)
found its right angle from the slopes. Can you find it a second way,
with Pythagoras?

<details class="dl-answer"><summary>answer</summary>

The sides are 4, 3 and 5, and $4^2 + 3^2 = 16 + 9 = 25 = 5^2$. The
right angle is opposite the longest side, at $(4, 0)$.

</details>

**6.** Why is the distance formula the same thing as Pythagoras'
theorem?

<details class="dl-answer"><summary>answer</summary>

Draw the gap across and the gap up between two points. The two gaps
meet at a right angle. The straight-line distance is the third side of
that triangle.

So $\text{distance}^2 = \text{across}^2 + \text{up}^2$ is exactly
$c^2 = a^2 + b^2$, with the two gaps as the two short sides.

</details>

## Midpoint

**7.** Find the midpoint of $(2, 8)$ and $(6, 2)$. Then find the
midpoint of $(-3, 4)$ and $(5, -2)$.

<details class="dl-answer"><summary>answer</summary>

$(4, 5)$ and $(1, 1)$.

</details>

## Putting it together

**8.** A drone is at $(0, 0)$. There are two landing pads, at
$(30, 40)$ and $(-20, 45)$. Which pad is closer, and by how much?

<details class="dl-answer"><summary>answer</summary>

The first pad is 50 away. The second is
$\sqrt{400 + 2025} = \sqrt{2425} \approx 49.24$ away.

The second pad is closer, by about 0.76. That is so close that a guess
from a picture could easily go the other way.

</details>

**9.** Which point on the horizontal axis is the same distance from
$(0, 4)$ and from $(6, 2)$?

<details class="dl-hint"><summary>hint</summary>

Call the point $(x, 0)$. What are its two squared distances?

</details>

<details class="dl-answer"><summary>one way through it</summary>

The two squared distances must be equal:

$$x^2 + 16 = (x - 6)^2 + 4$$

If we expand the bracket, we get $x^2 + 16 = x^2 - 12x + 40$. So
$12x = 24$, and $x = 2$.

The point is $(2, 0)$. It is $2\sqrt{5}$ from each of the two points.

</details>

**10.** A circle has its centre at $(3, 1)$, and it passes through
$(7, 4)$. What is its radius? Is the point $(0, 5)$ inside the circle or
outside it?

<details class="dl-answer"><summary>answer</summary>

The radius is the distance from the centre to the point we know:
$\sqrt{16 + 9} = 5$.

The point $(0, 5)$ is $\sqrt{9 + 16} = 5$ from the centre. So it is
on the circle, neither inside nor outside.

</details>

**11.** Three points are *collinear* when they lie on one straight
line. Can you write `collinear(p, q, r)`? Does your version work for
three points on a vertical line?

```python exec
id: putting-it-together-1
def collinear(p, q, r):
    """True when the three points lie on one straight line."""
    # Your code here.
```

```hint
On one straight line, the slope from `p` to `q` is the same as the
slope from `q` to `r`. What happens to a slope on a vertical line?
```

```hint
after: 3 errors
title: A way with no dividing

The two slopes are equal when
$(y_2 - y_1)(x_3 - x_2) = (y_3 - y_2)(x_2 - x_1)$. This is the two
fractions with their bottoms multiplied across, so nothing is divided,
and a vertical line is no trouble. Floats are not always exact, so
compare the difference with a tiny number such as `1e-9`.
```

```inputs
collinear((0, 0), (1, 2), (3, 6))
collinear((0, 0), (1, 0.1), (3, 0.3))
collinear((2, 0), (2, 5), (2, -1))    # a vertical line
collinear((0, 0), (1, 1), (2, 3))
```

```solution
def collinear(p, q, r):
    """True when the three points lie on one straight line."""
    (x1, y1), (x2, y2), (x3, y3) = p, q, r
    return abs((y2 - y1) * (x3 - x2) - (y3 - y2) * (x2 - x1)) < 1e-9
---
A version that compares two slopes with `==` says `False` for
$(0, 0)$, $(1, 0.1)$ and $(3, 0.3)$, which are on one line: Python
computes the two slopes as `0.1` and `0.09999999999999999`. It also
stops with a `ZeroDivisionError` on a vertical line. Multiplying across
avoids both problems.
```

## Your world

**12.** A problem from the world you chose.

<div class="dl-world" data-world="sea-and-sky">

Two lighthouses stand at $(0, 0)$ and $(10, 0)$ on a chart, in
kilometres. A ship's radar says it is 6 km from the first and 8 km from
the second. Where could the ship be? Try it on paper first, then check
your answer with `distance`.

```python exec
id: your-world-1--sea-and-sky
first, second = (0, 0), (10, 0)
# Your check here.
```

<details class="dl-hint"><summary>hint</summary>

Call the ship $(x, y)$. Then $x^2 + y^2 = 36$ and
$(x - 10)^2 + y^2 = 64$. What happens if you subtract one equation from
the other?

</details>

<details class="dl-answer"><summary>one way through it</summary>

Subtracting the first equation from the second leaves
$-20x + 100 = 28$, so $x = 3.6$. Then $y^2 = 36 - 3.6^2 = 23.04$, so
$y = 4.8$ or $y = -4.8$.

The ship is at $(3.6, 4.8)$ or at $(3.6, -4.8)$: two places, one on
each side of the line between the lighthouses. The two distances
cannot tell them apart. A third lighthouse, off that line, could.

</details>

</div>

<div class="dl-world" data-world="sound">

Two microphones stand at $(0, 0)$ and $(20, 0)$, in metres. Somebody
claps at $(5, 12)$. Sound travels about 343 metres every second. Can
you write `arrival(source, microphone)`, the time in seconds the sound
takes to arrive? Which microphone hears the clap first, and by how
much?

```python exec
id: your-world-1--sound
speed_of_sound = 343    # metres every second
clap = (5, 12)
```

```hint
Time is distance divided by speed.
```

```inputs
arrival(clap, (0, 0))
arrival(clap, (20, 0))
arrival((10, 0), (10, 343))
```

```solution
def arrival(source, microphone):
    return distance(source, microphone) / speed_of_sound


print(arrival(clap, (20, 0)) - arrival(clap, (0, 0)))
---
The clap is 13 m from the first microphone and about 19.2 m from the
second. The first hears it after about 0.038 seconds, and the second
about 0.018 seconds later. Some phones and smart speakers use gaps
this small to tell which way a sound came from.
```

</div>

<div class="dl-world" data-world="planets-and-moons">

Put the Sun at $(0, 0)$, in astronomical units (AU). On one day the
Earth is at $(1, 0)$ and Venus is at $(0, 0.72)$. A radio message
crosses 1 AU in about 8.3 minutes. How far apart are the two planets,
and how long does a message take? How long would it take when Venus is
at $(0.72, 0)$, on the same side of the Sun as the Earth?

```python exec
id: your-world-1--planets-and-moons
earth = (1, 0)
minutes_per_au = 8.3
```

```hint
Find each distance in AU first. Then multiply by the minutes for 1 AU.
```

```inputs
distance(earth, (0, 0.72)) * minutes_per_au
distance(earth, (0.72, 0)) * minutes_per_au
```

```solution
for venus in [(0, 0.72), (0.72, 0)]:
    apart = distance(earth, venus)
    print(apart, "AU apart, and", apart * minutes_per_au, "minutes")
---
At $(0, 0.72)$ Venus is about 1.23 AU from the Earth, and a message
takes about 10.2 minutes. On the same side of the Sun it is only 0.28
AU away, and a message takes about 2.3 minutes. Venus comes closer to
the Earth than any other planet.
```

</div>

<div class="dl-world" data-world="fantasy-maps">

A treasure is buried halfway between the old oak at $(-3, 7)$ and the
standing stone at $(5, -1)$, in kilometres on the kingdom's map. Where
is it? How far is it from the castle at $(4, 5)$?

```python exec
id: your-world-1--fantasy-maps
oak, stone, castle = (-3, 7), (5, -1), (4, 5)
# Your code here.
```

```hint
Which of the two tools finds a place halfway between two others?
```

```inputs
midpoint(oak, stone)
distance(midpoint(oak, stone), castle)
```

```solution
treasure = midpoint(oak, stone)
print(treasure, distance(treasure, castle))
---
The treasure is at $(1, 3)$, about 3.6 km from the castle.
```

</div>

## From earlier

**13.** From
[Straight lines: slope, and the line that breaks the formula](tutorial:slope-and-lines).
Take the line segment from $(1, 2)$ to $(7, 6)$. The line at right
angles to it, through its midpoint, is called its *perpendicular
bisector*. What is its equation? Pick a point on it, and check with
`distance` that the point is the same distance from both ends.

<details class="dl-answer"><summary>one way through it</summary>

The midpoint is $(4, 4)$. The segment's slope is
$\tfrac{6 - 2}{7 - 1} = \tfrac{2}{3}$, so the slope at right angles is
$-\tfrac{3}{2}$. Through $(4, 4)$, that is $y = -1.5x + 10$.

The point $(2, 7)$ is on it. `distance((2, 7), (1, 2))` and
`distance((2, 7), (7, 6))` both print about 5.099, which is
$\sqrt{26}$. Every point on the perpendicular bisector is the same
distance from both ends.

</details>

**14.** From [Complex numbers: roots that are not real](tutorial:complex-roots).
What will `abs(3 + 4j)` print? Why is that the same as
`distance((0, 0), (3, 4))`?

```python exec
id: from-earlier-1
print(abs(3 + 4j))
```

<details class="dl-answer"><summary>why</summary>

It prints `5.0`. The complex number $3 + 4i$ is the point $(3, 4)$ on
the complex plane, and `abs` gives its distance from the origin. Python
uses the distance formula for it.

</details>
