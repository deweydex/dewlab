---
title: "Going round in circles: angles, radians and the unit circle — Practice"
practice_for: going-round-in-circles
year: "2026-2027"
version: 2026.09.26.2
---

# Going round in circles: angles, radians and the unit circle — Practice

Each problem says what kind it is. **Predict** means guess first, then
run. **Make** means write something new. **Fix** means find why code
that looks fine does something else, and change it. **Explain** means
answer in words. **Another way** means reach the same place by a second
route. The answers are folded away until you open them. Each is one
answer, and yours may be different and work too.

Your toolkit is loaded on this page, including `point_on_circle` from
the tutorial, `distance` from
[How far apart?](tutorial:how-far-apart) and `close_enough` from
[Does it work?](tutorial:does-it-work). `math` is not loaded. Each cell
that needs it starts with `import math`.

## Warm-up

Use this cell for any of the warm-up problems.

```python exec
id: going-round-practice-warm-up
import math
# Try things here
```

**1. Predict.** What does this line print?

```python
print(math.degrees(math.pi), math.radians(360))
```

<details class="dl-answer"><summary>answer</summary>

`180.0 6.283185307179586`.

$\pi$ radians is half a turn, which is $180^\circ$. A whole turn,
$360^\circ$, is $2\pi$ radians, about 6.28. That is the circumference of a
circle of radius 1.

</details>

**2. Predict.** A Ferris wheel has a radius of 10 m. A seat starts on
the right-hand side, level with the centre, and the wheel turns half a
turn anticlockwise. Where is the seat now? Say it before you run this.

```python
x, y = point_on_circle(10, 180)
print(round(x, 2), round(y, 2))
```

<details class="dl-answer"><summary>answer</summary>

`-10.0 0.0`.

Half a turn takes the seat straight across the centre, to the left-hand
side, still level with the centre. Without `round`, `y` would be
`1.2246467991473532e-15`. That is a float's tiny rounding error, which is 0 for
any Ferris wheel.

</details>

<aside class="dl-note" id="going-round-practice-note-ferris">

**The first Ferris wheel.** George Ferris built the first Ferris wheel
for the World's Fair in Chicago in 1893. It was about 80 m high, and
each of its 36 cars could hold 60 people. It was moved twice, to other
places, and destroyed in 1906.

</aside>

**3. Make.** A pie chart shows 8 groups of the same size. What angle is
each slice at the centre, in degrees and in radians? And for 6 groups?

<details class="dl-answer"><summary>answer</summary>

```python
for groups in [8, 6]:
    slice_angle = 360 / groups
    print(groups, slice_angle, math.radians(slice_angle))
```

8 slices are $45^\circ$ each, which is $\frac{\pi}{4} \approx 0.785$
radians. 6 slices are $60^\circ$ each, $\frac{\pi}{3} \approx 1.047$
radians. Each slice is a whole turn, $360^\circ$ or $2\pi$ radians,
divided by the number of slices. A charting library such as
matplotlib calculates each slice's angle this way, from its share of
the total.

</details>

**4. Explain.** Schlomi, who is learning Python too, knows that
$\sin 30^\circ = \frac{1}{2}$. She types `math.sin(30)` and Python
gives `-0.9880316240928618`. What happened, and what could she type
instead?

<details class="dl-answer"><summary>answer</summary>

`math.sin` takes an angle in radians, so it read 30 as 30 radians.
That is almost 5 whole turns, and then a bit, which ends low on the
circle.
Schlomi's idea holds in the space of degrees. She needs to move the
angle into radians first:

```python
print(math.sin(math.radians(30)))
```

This gives `0.49999999999999994`, which is $\frac{1}{2}$ with a
float's tiny rounding error.

</details>

## Core

A cell for the core problems.

```python exec
id: going-round-practice-core
import math
import matplotlib.pyplot as plt
# Your working for problems 5 to 12
```

**5. Make.** An artist wants a regular hexagon: six corners, evenly
spaced round a circle of radius 5. Find the six corners with
`point_on_circle`, and draw the hexagon. Then use `distance` to measure
each side. What do you notice?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Six corners evenly spaced are $360 \div 6 = 60^\circ$ apart, so the
   angles are 0, 60, 120, 180, 240 and 300: `range(0, 360, 60)`.
2. Keep the corners in a list. To close the shape, add the first corner
   again at the end.
3. Measure from each corner to the next.

**Think about:** what shape do the centre and two corners next to each
other make? The tutorial's $60^\circ$ triangle had the same shape.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
corners = []
for angle in range(0, 360, 60):
    corners.append(point_on_circle(5, angle))
corners.append(corners[0])

xs = []
ys = []
for x, y in corners:
    xs.append(x)
    ys.append(y)
plt.plot(xs, ys, marker="o")
plt.axis("equal")

for position in range(6):
    print(round(distance(corners[position], corners[position + 1]), 6))
```

Every side is 5, the same as the radius. The centre and two corners
next to each other make a triangle with two sides of 5 and a
$60^\circ$ angle between them. That is the equilateral triangle from
the tutorial, so its third side is 5 too.

</details>

**6. Fix.** Schlomo, who is learning Python too, is writing a game that
seats players round a campfire. His function is meant to measure angles
the maths way, so a quarter turn, $90^\circ$, should be the top of the
circle. What does it do instead, and what needs to change?

```python exec
id: going-round-practice-fix-seat
import math

def seat_position(radius, angle_degrees):
    """Return the (x, y) of a seat at angle_degrees, anticlockwise from the right."""
    angle = math.radians(angle_degrees)
    return (radius * math.sin(angle), radius * math.cos(angle))
```

```inputs
seat_position(3, 90)    # a quarter turn is the top
```

```solution
import math

def seat_position(radius, angle_degrees):
    """Return the (x, y) of a seat at angle_degrees, anticlockwise from the right."""
    angle = math.radians(angle_degrees)
    return (radius * math.cos(angle), radius * math.sin(angle))
---
The sine and the cosine were swapped. The $x$ of the point is the
cosine, how far across, and the $y$ is the sine, how far up.

Schlomo's version starts at the top and goes clockwise, as a clock
measures. It keeps a different promise from the one in its docstring.
For a clock, it would be the one to use.
```

**7. Predict.** Using the exact values from the tutorial, what will
this print? Say it in surd form first.

```python
print(point_on_circle(2, 60))
```

<details class="dl-answer"><summary>answer</summary>

`(1.0000000000000002, 1.7320508075688772)`.

On the unit circle, the point at $60^\circ$ is
$\left(\frac{1}{2}, \frac{\sqrt{3}}{2}\right)$. A radius of 2 doubles
both, so the exact point is $(1, \sqrt{3})$. Python's first number is
a tiny way over 1, and $\sqrt{3} \approx 1.7320508$.

</details>

**8. Make.** A bicycle wheel has a radius of 0.35 m. It turns three
whole turns and a quarter turn more. How far has the bike gone?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. On the unit circle, an angle in radians is the distance walked
   round the edge.
2. On a circle of radius $r$, everything is $r$ times as big, so the
   walk is $r$ times the angle in radians.
3. Three turns and a quarter is $3 \times 360 + 90$ degrees.

**Think about:** the ground under the wheel touches every part of the
rim once per turn.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
angle = math.radians(3 * 360 + 90)
print(0.35 * angle)
```

About 7.15 m. The distance round the edge of a circle, for an angle in
radians, is radius × angle. For one whole turn this gives
$0.35 \times 2\pi$, the circumference, as it should.

</details>

**9. Another way.** How many radians are in a whole turn? Find it three
ways: with `math.radians`, with `2 * math.pi`, and with
`circle_circumference` from
[Measuring rooms and tins](tutorial:measuring-rooms-and-tins#tools-for-flat-shapes).

<details class="dl-answer"><summary>answer</summary>

```python
print(math.radians(360))
print(2 * math.pi)
print(circle_circumference(1))
```

All three give `6.283185307179586`. The third works because an angle in
radians is the distance walked round the unit circle, and a whole turn
walks the whole circumference.

</details>

**10. Explain.** The tutorial defined sine and cosine as the across and
up of a point going round a circle. Many courses start with a
right-angled triangle instead, and define the sine as one side divided
by another. Which way would you have wanted to learn it first, and why?
There is no single answer.

<details class="dl-answer"><summary>answer</summary>

An answer might weigh a few things, and can choose either way.

- **What it is for.** Heights and distances, such as a tree or a roof,
  come with a right-angled triangle already in them. Clocks, wheels and
  sounds go round, and past $90^\circ$.
- **How far it reaches.** The triangle only has angles less than
  $90^\circ$. The circle gives a sine for every angle, even a negative
  one.
- **The picture.** Some people picture a triangle better than a point
  moving. Others picture the moving point better.
- **What comes next.** The next page, on waves, needs the circle. The
  page after, on solving triangles, starts from the triangle.

You might also want both, one after the other, as this unit does.

</details>

**11. Predict.** What does this print? Is it 1?

```python
print(math.tan(math.radians(45)))
```

<details class="dl-answer"><summary>answer</summary>

`0.9999999999999999`.

At $45^\circ$ the line out to the point rises as far as it runs, so the
tangent is exactly 1. The angle in radians, $\frac{\pi}{4}$, has
endless digits, and the float is not quite exact, so its tangent is not
exact either.
`close_enough(math.tan(math.radians(45)), 1)` is `True`.

</details>

**12. Make.** Write `gap_between_hands(hours, minutes)`, which returns
the angle between a clock's two hands, the smaller way round, so never
more than $180^\circ$. Test it at 3:00, 6:00, 12:30 and 10:10.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The hour hand has turned `(hours % 12) * 30 + minutes * 0.5`
   degrees, and the minute hand `minutes * 6`.
2. Take the difference, and keep its size with `abs`.
3. If the difference is more than 180, the other way round is shorter.
   It is `360 - difference`.

**Think about:** at 12:30 the difference is 165. At 1:55 it is 292.5.
Which way round is shorter at 1:55?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def gap_between_hands(hours, minutes):
    """Return the smaller angle between a clock's hands, in degrees."""
    hour_angle = (hours % 12) * 30 + minutes * 0.5
    minute_angle = minutes * 6
    difference = abs(hour_angle - minute_angle)
    if difference > 180:
        difference = 360 - difference
    return difference

for hours, minutes in [(3, 0), (6, 0), (12, 30), (10, 10)]:
    print(hours, minutes, gap_between_hands(hours, minutes))
```

It gives `90.0`, `180.0`, `165.0` and `115.0`. At 12:30 the gap is not $180^\circ$.
The hour hand has moved $15^\circ$ past the 12 towards the 1.

</details>

## Stretch

A cell for the stretch problems.

```python exec
id: going-round-practice-stretch
import math
import matplotlib.pyplot as plt
# Your working for problems 13 to 16
```

**13. Make.** In a space game, a planet goes round a sun on a circle of
radius 10, turning $1^\circ$ a day. A moon goes round the planet on a
circle of radius 2, turning $12^\circ$ a day. Draw the moon's path over
360 days. The moon's position is the planet's position, plus its own
point on its own small circle.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. For each `day` in `range(361)`, find the planet with
   `point_on_circle(10, day)`.
2. Find where the moon is from the planet with
   `point_on_circle(2, 12 * day)`.
3. Add the two $x$ values together, and the two $y$ values, and keep
   them in two lists.

**Think about:** how many loops will the moon make in a year? Guess it
from the two speeds before you draw.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
moon_xs = []
moon_ys = []
for day in range(361):
    planet_x, planet_y = point_on_circle(10, day)
    around_x, around_y = point_on_circle(2, 12 * day)
    moon_xs.append(planet_x + around_x)
    moon_ys.append(planet_y + around_y)

plt.axis("equal")
plt.plot(moon_xs, moon_ys)
```

The path is a large circle with 11 small loops in it, like a flower.
Did you guess 12? The moon makes 12 turns in the year, but the planet
makes one turn round the sun in the same direction. The loops count
only the turns the moon makes beyond the planet's: $12 - 1 = 11$.
Drawing toys with toothed wheels make patterns like this, and games use
the same maths for things in orbit.

</details>

**14. Another way.** The triangle on the ball in the tutorial had
angles adding up to $270^\circ$, which is $90^\circ$ more than a flat
triangle's. In 1629, Albert Girard showed that on a ball of radius $R$,
a triangle's area is $R^2$ times this extra angle, in radians. Use it
to find the area of that triangle on the Earth, taking $R$ as 6,371
km. Then find the same area another way, with `sphere_surface_area`
from your toolkit. Why do they agree?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The extra angle is $270 - 180 = 90$ degrees. Turn it into radians.
2. Girard's area is `6371 ** 2` times that.
3. Look at the picture in the tutorial again. The equator and the two
   lines of longitude cut the ball into how many pieces the same shape
   as the orange one?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
radius = 6371
print(radius ** 2 * math.radians(270 - 180))
print(sphere_surface_area(radius) / 8)
```

Both give about 63,758,059 km². The equator cuts the ball into two
halves, and the two lines of longitude, a quarter turn apart, cut each
half into four. That makes 8 pieces of the same shape, and the orange
triangle is one of them. A triangle on a ball has an area that the
angles alone decide. On a flat plane, a triangle's angles tell you its
shape, but nothing about its size.

</details>

**15. Fix.** A loading spinner on a web page should show 12 dots in a
ring, like the hours on a clock. This version shows far too many.
How many does it show, and what needs to change?

```python exec
id: going-round-practice-fix-spinner
import matplotlib.pyplot as plt

dot_xs = []
dot_ys = []
for angle in range(0, 360, 12):
    x, y = point_on_circle(1, angle)
    dot_xs.append(x)
    dot_ys.append(y)

plt.plot(dot_xs, dot_ys, "o")
plt.axis("equal")
print(len(dot_xs), "dots")
```

<details class="dl-answer"><summary>answer</summary>

It prints `30 dots`. The third number in `range` is the step between
angles, not the number of dots. A step of 12 degrees fits 30 times in
a turn. For 12 dots, the step is $360 \div 12 = 30$ degrees:

```python
for angle in range(0, 360, 30):
```

Now it prints `12 dots`.

</details>

**16. Explain.** On a flat map of the world, the route of a flight from
Dublin to Chicago curves up towards the north, and does not follow the
straight line you could draw on the map with a ruler. Why does the
plane go that way?

<details class="dl-answer"><summary>answer</summary>

The Earth is a ball, and the shortest path between two places on a
ball runs along a great circle. A flat map has to stretch the ball to
lay it flat, and the usual world maps stretch the far north most. So the great circle
looks curved on the map, and the ruler's straight line, which looks
shorter, is longer on the real Earth.

</details>
