---
title: "Distance and Pythagoras: how far apart two points are"
year: "2026-2027"
version: 2026.09.26.1
covers:
  how-far-apart:
    covers: [MIT-4.3, MIT-4.4]
  checking-the-theorem:
    covers: [MIT-4.4]
  halfway-the-midpoint:
    covers: [MIT-4.3]
  distance-in-your-world:
    covers: [MIT-4.3, MIT-4.4]
  where-you-will-meet-this-again:
    covers: [MIT-4.3]
worlds:
  sea-and-sky: A lighthouse, and the ships that watch for its light. The numbers are made up.
  sound: A concert, and how long its sound takes to reach you.
  planets-and-moons: The Earth and Mars, with their orbits drawn as circles. The positions are made up.
  fantasy-maps: A made-up kingdom, its roads and its crows. The numbers are made up.
---

# Distance and Pythagoras: how far apart two points are

A lighthouse stands at $(1, 2)$ on a ship's chart, and a boat is at
$(5, 5)$. Each square of the chart is one kilometre. How far apart are
they?

## How far apart

The easy part first. The gap across and the gap up are each one
subtraction.

```python exec
id: how-far-apart-1
import math
import matplotlib.pyplot as plt

lighthouse, boat = (1, 2), (5, 5)

across = boat[0] - lighthouse[0]
up = boat[1] - lighthouse[1]
print("across:", across)
print("up:    ", up)
```

The gaps are 4 km across and 3 km up. Neither of those is the distance
between the points. If the boat sails 4 km east and then 3 km north, it
sails 7 km in total. The straight line from start to finish is shorter
than 7 km, and longer than 4 km.

How long is the straight line? Can you think of a way to find it?

```python exec
id: how-far-apart-2
def axes(size=8):
    fig, ax = plt.subplots(figsize=(5.5, 5.5))
    ax.axhline(0, color="black", linewidth=0.8)
    ax.axvline(0, color="black", linewidth=0.8)
    ax.grid(alpha=0.3)
    ax.set_xlim(-1, size)
    ax.set_ylim(-1, size)
    ax.set_aspect("equal")
    return ax


ax = axes()
ax.plot([1, 5], [2, 5], "-o", linewidth=2, markersize=8)
ax.annotate("lighthouse", lighthouse, textcoords="offset points", xytext=(-30, -16))
ax.annotate("boat", boat, textcoords="offset points", xytext=(8, 2))
ax.set_title("How long is that line?")
```

Now let's draw the two gaps as well. What shape do they make with the
line?

```python exec
id: how-far-apart-3
ax = axes()
ax.plot([1, 5], [2, 2], color="tab:orange", linewidth=3)
ax.plot([5, 5], [2, 5], color="tab:green", linewidth=3)
ax.plot([1, 5], [2, 5], color="tab:blue", linewidth=2)
ax.annotate("4 across", (2.5, 1.4), color="tab:orange")
ax.annotate("3 up", (5.2, 3.4), color="tab:green")
ax.annotate("?", (2.6, 3.8), color="tab:blue", fontsize=14)
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
$3^2 + 4^2 = 9 + 16 = 25$, and $\sqrt{25} = 5$. So the boat is 5 km
from the lighthouse.

Written with coordinates, this is the *distance formula*:

$$d = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}$$

```python exec
id: how-far-apart-4
def distance(p, q):
    (x1, y1), (x2, y2) = p, q
    across = x2 - x1
    up = y2 - y1
    return math.sqrt(across ** 2 + up ** 2)


print(distance(lighthouse, boat))
print(distance((0, 0), (3, 4)))
print(distance((0, 0), (1, 1)))
```

**The distance formula and Pythagoras' theorem say the same thing.** We
wanted a distance. We drew the triangle that the two gaps make. The
theorem answered the question we were already asking.

What does `distance` give if the two gaps are negative, as they are when
the boat is south-west of the lighthouse? Try `distance(boat, lighthouse)`
too. Why does the order not matter?

## Checking the theorem

How could we test the theorem, and not only use it? We need to measure
the third side of a triangle without calculating it from $a^2 + b^2$
first. `distance` can do that. It measures the gap between two points.

Here is the experiment. Take two sides, 3 and 4 long, joined at one
corner. Open the angle between them to 80°, then 90°, then 100°. Each
time, measure the gap across the open end, and call it $c$.

The cell uses `math.cos` and `math.sin` to point the second side at the
angle we choose. We meet them properly on the next page.

```python exec
id: checking-the-theorem-1
a_side, b_side = 3, 4
for angle in [80, 90, 100]:
    turn = math.radians(angle)    # cos and sin expect radians, not degrees
    end_of_a = (a_side, 0)
    end_of_b = (b_side * math.cos(turn), b_side * math.sin(turn))
    c_side = distance(end_of_a, end_of_b)
    print(f"{angle:>3} degrees:   a^2 + b^2 = {a_side ** 2 + b_side ** 2}    c^2 = {c_side ** 2:.2f}")
```

```predict
type: choice

$a^2 + b^2$ is 25 every time. What will $c^2$ be?

- 25 every time
  - The theorem is about the three sides of a triangle, and these are
    three triangles.
- 25 only at 90 degrees
- Close to 25 every time, but never exactly 25
  - Measuring with decimals always leaves a little error.
```

Only the right angle gives 25. Close the angle, and the third side is
shorter than the theorem says. Open it, and the third side is longer.
So the theorem is a fact about triangles with a right angle. It is not
true for every triangle. The rule that works for every angle is called
the cosine rule, and it is on
[Solving triangles: the sine rule and the cosine rule](tutorial:solving-triangles).

### Your turn

Here are three points: $(0, 0)$, $(8, 0)$ and $(4, 3)$. They make a
triangle. A triangle is *isosceles* when two of its sides have the same
length. Is this one isosceles? Can you write `sides(p, q, r)`, which
returns the three side lengths of a triangle?

```python exec
id: checking-the-theorem-2
def sides(p, q, r):
    """The lengths of the three sides of the triangle with corners p, q, r."""
    # Your code here.
```

```hint
Each side joins two of the corners. Which pairs of corners are there?
```

```inputs
sides((0, 0), (8, 0), (4, 3))
sides((0, 0), (3, 0), (0, 4))
sides((1, 1), (4, 5), (8, 2))
```

```solution
def sides(p, q, r):
    """The lengths of the three sides of the triangle with corners p, q, r."""
    return distance(p, q), distance(q, r), distance(r, p)
---
The first triangle has sides 8, 5 and 5, so it is isosceles. The second
is the 3-4-5 triangle. The third has sides 5, 5 and about 7.07, so it is
isosceles too, and $5^2 + 5^2 = 50 = 7.07^2$ says it has a right angle.
```

## Halfway: the midpoint

The *midpoint* of two points is the point halfway between them. It is
the average of the two points. We average the $x$ values, and we
average the $y$ values:

$$\text{midpoint} = \left(\frac{x_1 + x_2}{2}, \frac{y_1 + y_2}{2}\right)$$

For example, the midpoint of $(1, 2)$ and $(7, 6)$ is
$\left(\frac{1 + 7}{2}, \frac{2 + 6}{2}\right) = (4, 4)$.

```python exec
id: halfway-the-midpoint-1
def midpoint(p, q):
    (x1, y1), (x2, y2) = p, q
    return ((x1 + x2) / 2, (y1 + y2) / 2)


a, b = (1, 2), (7, 6)
middle = midpoint(a, b)
print("midpoint of", a, "and", b, "is", middle)
print("distances:", distance(a, middle), distance(middle, b))
```

This is the same average we used for marks in
[Statistics: averages, spread and frequency](tutorial:making-sense-of-data),
done twice: once for $x$ and once for $y$. The last line shows that the
midpoint is the same distance from each end.

### Your turn

The midpoint of a line segment is $(3, 1)$, and one end of it is
$(7, 4)$. Where is the other end? Can you find it on paper first, and
then check it with `midpoint`?

```python exec
id: halfway-the-midpoint-2
# Your answer, then a check with midpoint.
```

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Yours may be different and work too.

The other end is $(-1, -2)$. To get from $(7, 4)$ to the midpoint, we
move 4 left and 3 down. The other end is the same move again from the
midpoint: $(3 - 4, 1 - 3) = (-1, -2)$. `midpoint((7, 4), (-1, -2))`
prints `(3.0, 1.0)`.

</details>

## Distance in your world

<div class="dl-world" data-world="sea-and-sky">

A lighthouse stands at $(0, 0)$ on the chart. Ships can see its light
from up to 20 km away. A ship sails in a straight line from $(12, 9)$
to $(18, 13)$. Can you write `can_see(ship)`, which says whether a ship
at that point can see the light? Can the ship see it at the start of
its journey? At the end? Can you find roughly where the ship loses
sight of it?

```python exec
id: distance-in-your-world-1--sea-and-sky
lighthouse = (0, 0)
reach = 20    # km
```

```hint
The ship can see the light when its distance from the lighthouse is no
more than `reach`. To find where it loses sight of it, try points along
the way, such as the midpoint of the start and the end.
```

```inputs
can_see((12, 9))
can_see((18, 13))
can_see((15, 11))
```

```solution
def can_see(ship):
    return distance(lighthouse, ship) <= reach


print(distance(lighthouse, (12, 9)), distance(lighthouse, (18, 13)))
---
At the start the ship is 15 km away and can see the light. At the end it
is about 22.2 km away and cannot. The midpoint, $(15, 11)$, is about
18.6 km away, so the ship loses sight of the light in the second half
of its journey.
```

</div>

<div class="dl-world" data-world="sound">

A band plays on a stage at $(0, 0)$, and positions in the field are in
metres. Sound travels about 343 metres every second. The big screens
show the drummer at once, because light is far faster. Can you write
`delay(listener)`, the time in seconds that the sound takes to reach a
listener? How late is the sound at $(30, 40)$? At $(120, 160)$?

```python exec
id: distance-in-your-world-1--sound
stage = (0, 0)
speed_of_sound = 343    # metres every second
```

```hint
Time is distance divided by speed. Which function gives the distance?
```

```inputs
delay((30, 40))
delay((120, 160))
delay((0, 343))
```

```solution
def delay(listener):
    return distance(stage, listener) / speed_of_sound


print(delay((30, 40)), delay((120, 160)))
---
At $(30, 40)$ you are 50 m away, and the sound is about 0.15 seconds
late. At $(120, 160)$ you are 200 m away, and the sound is about 0.58
seconds late. That is over half a second behind the drummer on the
screen, which is easy to see and hear.
```

</div>

<div class="dl-world" data-world="planets-and-moons">

Put the Sun at $(0, 0)$, and measure in *astronomical units* (AU). One
AU is the average distance from the Earth to the Sun, about 150 million
km. On one day, the Earth is at $(1, 0)$ and Mars is at $(-1.2, 0.9)$.
A radio message crosses 1 AU in about 8.3 minutes. How far apart are
the two planets? How long does a message from Mars take to reach the
Earth? Keep the minutes as `message_minutes`.

```python exec
id: distance-in-your-world-1--planets-and-moons
sun, earth, mars = (0, 0), (1, 0), (-1.2, 0.9)
minutes_per_au = 8.3
```

```hint
First find the distance in AU. Then, if 1 AU takes 8.3 minutes, how
long do 2 AU take?
```

```inputs
distance(earth, mars)
distance(sun, mars)
message_minutes
```

```solution
apart = distance(earth, mars)
message_minutes = apart * minutes_per_au
print(apart, "AU apart")
print(message_minutes, "minutes for a message")
---
Mars is 1.5 AU from the Sun, and on this day it is about 2.38 AU from
the Earth, on the far side of the Sun. A message takes about 19.7
minutes. When the two planets are on the same side of the Sun, they are
only about 0.5 AU apart, and a message takes about 4 minutes.
```

</div>

<div class="dl-world" data-world="fantasy-maps">

The kingdom's roads run only north–south and east–west, and positions
are in kilometres. A crow flies in a straight line. The mill is at
$(-4, 1)$ and the castle is at $(4, 5)$. Can you write
`crow_and_road(start, end)`, which returns two distances: how far the
crow flies, and how far a rider goes on the roads? How much shorter is
the crow's journey?

```python exec
id: distance-in-your-world-1--fantasy-maps
mill, castle = (-4, 1), (4, 5)
```

```hint
The rider goes the whole gap across, and then the whole gap up. A gap
can be negative, so `abs()` makes it a length.
```

```inputs
crow_and_road(mill, castle)
crow_and_road((0, 0), (3, 4))
crow_and_road((2, 2), (2, 9))
```

```solution
def crow_and_road(start, end):
    (x1, y1), (x2, y2) = start, end
    road = abs(x2 - x1) + abs(y2 - y1)
    return distance(start, end), road
---
From the mill to the castle, the crow flies about 8.94 km and the rider
goes 12 km, about 3 km further. When the two places are due north of
each other, as in the last line, both journeys are the same.
```

</div>

## Where you will meet this again

Here is one last picture. It shows where this page leads.

The cell uses `math.cos` and `math.sin` to place 61 points around a
circle. We meet these two functions properly on the next page. Here we
need only the points.

```python exec
id: where-you-will-meet-this-again-1
fig, ax = plt.subplots(figsize=(5, 5))
points = [(math.cos(t / 60 * 2 * math.pi), math.sin(t / 60 * 2 * math.pi))
          for t in range(61)]
ax.plot([p[0] for p in points], [p[1] for p in points], linewidth=2)
ax.axhline(0, color="black", linewidth=0.8)
ax.axvline(0, color="black", linewidth=0.8)
ax.set_aspect("equal")
ax.grid(alpha=0.3)
ax.set_title("A circle of radius 1")
```

How far is each point on this circle from the centre? Let's check a few
with our `distance` function.

```python exec
id: where-you-will-meet-this-again-2
for t in [0, 7, 15, 33, 48]:
    p = points[t]
    print(f"({p[0]:>6.3f}, {p[1]:>6.3f})   distance from the centre: {distance((0, 0), p):.6f}")
```

The distance is 1 every time.
[The unit circle: sine, cosine and tangent](tutorial:the-unit-circle)
starts with that circle. That whole page depends on one fact. Every
point on the circle is 1 away from the centre.

## Looking back

We asked how far apart two points are. The gap across and the gap up
make a right-angled triangle, and Pythagoras' theorem gives the long
side. The theorem holds only when the angle is a right angle.

Why is the straight line between two points always shorter than going
across and then up, unless one of the gaps is zero?

A challenge: a ship's captain has a dictionary of ports and their
places on the chart. Can you write `nearest(ship, ports)`, which returns
the name of the nearest port? What should it do with two ports at the
same distance?

```python challenge
import math

ports = {"Howth": (3, 8), "Dún Laoghaire": (4, 1), "Wicklow": (6, -20),
         "Holyhead": (95, 12)}


def nearest(ship, ports):
    """The name of the port closest to the ship."""
    # Your code here.


print(nearest((10, 5), ports))
```

## Where to read more

3Blue1Brown (2017). *All possible pythagorean triples, visualized.*
<https://www.youtube.com/watch?v=QJYmyhnaaek>. Some right-angled
triangles have three whole-number sides, like 3, 4 and 5. Grant
Sanderson shows how to find every one of them, using complex numbers.
It is about fifteen minutes long.

Sebastian Lague (2017). *Gamedev Maths: distance from point to line.*
<https://www.youtube.com/watch?v=KHuI9bXZS74>. It takes the next step
after this page, and finds how far a point is from a line, rather than
from another point. Sebastian Lague builds the formula for a game. It
is about five minutes long.
