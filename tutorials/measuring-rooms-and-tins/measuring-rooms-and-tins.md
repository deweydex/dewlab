---
title: "Measuring rooms and tins: area, perimeter and volume"
year: "2026-2027"
version: 2026.09.24.1
covers:
  around-the-edge-perimeter:
    covers: [MIT-1.2]
    touches: [MIT-6.4]
  covering-a-surface-area:
    covers: [MIT-1.2]
  triangles-half-a-rectangle:
    covers: [MIT-1.2]
  circles-and-pi:
    covers: [MIT-1.2]
  tools-for-flat-shapes:
    touches: [MIT-1.2, PDP-LO8]
  how-much-a-tin-holds-volume:
    covers: [MIT-1.3]
  wrapping-it-surface-area:
    covers: [MIT-1.3]
  tools-for-solid-shapes:
    touches: [MIT-1.3, PDP-LO8]
  how-much-paint-does-the-room-need:
    touches: [MIT-1.2, PDP-LO8]
---

# Measuring rooms and tins: area, perimeter and volume

You want to paint a bedroom. The shop sells paint in 2.5 litre tins, and
the label says one litre covers about 12 square metres. How many tins do
you need? Buy too few, and you are back at the shop with one wall
half-done. Buy too many, and the spare tins sit in the shed for years.

On this page we:

- measure the edge of a shape: its perimeter
- measure the surface it covers: its area, for rectangles, triangles
  and circles
- meet $\pi$, and see where it comes from
- measure how much a solid holds, and how much it takes to wrap it
- turn every formula into a toolkit function, and check each one
- work out the paint for a real room

> **The space we're in.** Flat shapes and solid shapes, measured in
> metres or centimetres. Every length is 0 or more. Three spaces sit side
> by side on this page: lengths (m), areas (m²) and volumes (m³). A
> length and an area can be multiplied, but they cannot be added. One
> thing usually goes unsaid: every wall is flat and every corner is
> square. Real rooms are never quite that tidy.

## Warm-up

Two questions from earlier pages. The first is from
[Machines that take a number](tutorial:machines-that-take-a-number),
and the second from [Doing it again](tutorial:doing-it-again).

```question
id: measuring-rooms-warm-up-1
type: multiple-choice
correct: 2

`square(x)` gives `x * x`. What does `compose(math.sqrt, square)(-5)`
give?

- `-5`
- `5.0`
- `ValueError: math domain error`
```

```question
id: measuring-rooms-warm-up-2
type: fill-in-the-blank

Your toolkit's `total` adds up a row of values, so
`total([4, 3.5, 4, 3.5])` gives {15.0}.
```

## Around the edge: perimeter

Before painting, people often put masking tape all the way round the
edge of the floor, to protect it. How much tape does that take?

The *perimeter* of a shape is the distance all the way round its edge.
For the bedroom floor, 4 m long and 3.5 m wide, we walk round the four
sides and add them up: $4 + 3.5 + 4 + 3.5 = 15$ metres.

A rectangle always has two lengths and two widths. So, in words, its
perimeter is twice the length plus the width. In symbols, with $l$ for
the length and $w$ for the width:

$$P = 2(l + w)$$

A square is a rectangle with four equal sides, $s$, so its perimeter is
$P = 4s$.

Will the formula and the walk round agree? Run it to check.

```python exec
id: measuring-rooms-perimeter-1
length = 4
width = 3.5

print(total([length, width, length, width]))
print(2 * (length + width))
```

Both give `15.0` metres. The first line is the walk round the edge,
using `total` from your toolkit. The second is the formula. The formula
is shorter, and the walk round is the reason it is true.

## Covering a surface: area

The *area* of a shape is how much flat surface it covers. We measure it
in squares. A *square metre*, written m², is the area of a square 1 m
long on each side.

Picture a floor 4 m by 3 m, marked out in square metres. There are 3
rows, with 4 squares in each row: $3 \times 4 = 12$ squares. So the
area of a rectangle is its length times its width:

$$A = l \times w$$

and a square's area is $A = s \times s = s^2$. That is why $s^2$ is read
"s squared".

Now the walls. Picture the four walls unfolded into one long, flat strip,
like the paper round a present. The strip is as long as the way round
the room, which is the perimeter, and as tall as the room. So the wall
area is the perimeter times the height. Before you run it, how many
square metres of wall does a room 2.4 m high have?

```python exec
id: measuring-rooms-area-1
length = 4
width = 3.5
height = 2.4

floor_area = length * width
wall_area = 2 * (length + width) * height
print(floor_area)
print(wall_area)
```

The floor is 14 m² and the walls are 36 m². The door (2 m by 0.8 m) and
the window (1.2 m by 1 m) are not painted, so we take their areas away:
$36 - 1.6 - 1.2 = 33.2$ m².

Here is a question about the space we are in. What is $15 \text{ m} + 14
\text{ m}^2$? It has no answer. One is a length and the other is an
area, and adding them is like adding 15 minutes to 14 euro. Multiplying
across spaces is allowed: a length times a length is an area. Checking
the units is a quick test of any formula. If the answer to an area
question comes out in metres, something has gone wrong.

## Triangles: half a rectangle

An attic bedroom has a sloping roof, so one end wall is a triangle. The
base of a triangle is the side it stands on: here, 4 m along the floor.
Its height is measured straight up from the base to the top point: here,
1.8 m.

Picture the triangle drawn inside a rectangle with the same base and
height. The triangle fills exactly half of it: the two pieces left
over, one on each side, fit together to make a second copy of the
triangle. So in words, a triangle's area is half its base times its
height. In symbols, with $b$ for the base and $h$ for the height:

$$A = \frac{1}{2} b h$$

The height must be measured at a right angle to the base, straight up.
The sloping side is longer, and using it gives too big an answer.

```python exec
id: measuring-rooms-triangle-1
base = 4
height = 1.8

triangle = 0.5 * base * height
rectangle = base * height
print(triangle)
print(2 * triangle == rectangle)
```

The triangle is 3.6 m², and two of them make the 4 m by 1.8 m rectangle
exactly.

## Circles and pi

A circle has a centre. The *radius*, $r$, is the distance from the
centre to the edge. The *diameter*, $d$, is the distance right across,
through the centre, so $d = 2r$. The *circumference* is a circle's
perimeter: the distance all the way round.

Here is something you can try with a piece of string. Measure round a
circle, and across it, and divide. Someone did that with a two-euro
coin, a dinner plate and a bicycle wheel. What do you notice about the
three answers?

```python exec
id: measuring-rooms-circle-1
# (name, distance across, distance round), all in millimetres
measured = [
    ("coin", 25.75, 80.9),
    ("plate", 270, 848),
    ("wheel", 670, 2105),
]
for name, across, around in measured:
    print(name, around / across)
```

Every answer is close to 3.14, whether the circle is small or large.
This number is called *pi*, written $\pi$. It is the circumference of
any circle divided by its diameter. Its digits go on forever without a
pattern, so nobody can write it down exactly. Python keeps a very close
value in `math.pi`.

So, in words, the circumference is $\pi$ times the diameter. In
symbols:

$$C = \pi d = 2 \pi r$$

What about the area? Picture a round pizza cut into many thin slices.
Lay them in a row, points up and points down in turn. They make a
shape that is almost a rectangle. Its height is the radius, $r$, and its
length is half the crust, $\pi r$. The thinner the slices, the closer it
comes to a real rectangle. So the area is $\pi r \times r$:

$$A = \pi r^2$$

A pizza shop sells a 40 cm pizza for the same price as two 25 cm ones.
Which gives more pizza? Guess before you run it. The sizes are
diameters, so the radius is half.

```python exec
id: measuring-rooms-circle-2
import math

one_large = math.pi * 20 ** 2
two_medium = 2 * math.pi * 12.5 ** 2
print(round(one_large), "cm² from one large")
print(round(two_medium), "cm² from two medium")
```

One large pizza is about 1,257 cm², and two medium ones are about 982
cm². Doubling the radius makes the area four times bigger, because the
radius is squared. Most people guess the other way.

## Tools for flat shapes

Now each formula becomes a function in your toolkit, with its promise
in the docstring. Two are written. Replace each `...` in the other
three with one `return` line, using the formulas above and `math.pi`.

```python exec
id: measuring-rooms-toolkit-flat
toolkit: yes
import math


def rectangle_perimeter(length, width):
    """Return the distance round a rectangle."""
    return 2 * (length + width)


def rectangle_area(length, width):
    """Return the area of a rectangle. For a square, give the side twice."""
    return length * width


def triangle_area(base, height):
    """Return the area of a triangle.

    height is measured at a right angle to the base.
    """
    ...


def circle_circumference(radius):
    """Return the distance round a circle of this radius."""
    ...


def circle_area(radius):
    """Return the area of a circle of this radius."""
    ...
```

```python toolkit-reference
for: measuring-rooms-toolkit-flat
import math


def rectangle_perimeter(length, width):
    """Return the distance round a rectangle."""
    return 2 * (length + width)


def rectangle_area(length, width):
    """Return the area of a rectangle. For a square, give the side twice."""
    return length * width


def triangle_area(base, height):
    """Return the area of a triangle.

    height is measured at a right angle to the base.
    """
    return 0.5 * base * height


def circle_circumference(radius):
    """Return the distance round a circle of this radius."""
    return 2 * math.pi * radius


def circle_area(radius):
    """Return the area of a circle of this radius."""
    return math.pi * radius ** 2
```

The tests below check each promise against something we already know.
Until all three functions are written, they stop with an error.

```python exec
id: measuring-rooms-toolkit-flat-tests
assert rectangle_perimeter(4, 3.5) == 15
assert rectangle_area(4, 3.5) == 14
assert triangle_area(4, 1.8) == 3.6
assert 2 * triangle_area(6, 5) == rectangle_area(6, 5)
assert circle_circumference(1) == 2 * math.pi
assert circle_area(1) == math.pi
assert round(circle_area(20)) == 1257
print("The flat-shape tools keep their promises.")
```

```hint
Which line does the error point at? Try `print(triangle_area(4, 1.8))`
on its own. If it shows `None`, that function still has `...` where its
`return` line should be.
```

A test like `circle_area(1) == math.pi` is worth a moment. A circle of
radius 1 has area $\pi \times 1^2 = \pi$, so any mistake in the formula,
such as `2 * math.pi * radius`, shows up at once.

## How much a tin holds: volume

The *volume* of a solid is how much space it takes up. We measure it in
cubes. A *cubic centimetre*, cm³, is a cube 1 cm long on each side. A
litre is 1,000 cm³: a cube 10 cm on each side.

A box shape, like a shoebox or a room, is a *cuboid*. Picture it filled
with layers of centimetre cubes. One layer covers the base, so it holds
$l \times w$ cubes. There are $h$ layers. So:

$$V = l \times w \times h$$

and a cube, with every side $s$, has $V = s^3$.

The same idea works for a paint tin, which is a *cylinder*: a solid
with two equal circles at its ends. Each layer is a circle, with area
$\pi r^2$, and there are $h$ layers. In words, the volume is the area of
the base times the height:

$$V = \pi r^2 h$$

Look at how that is built. It is the circle's area, with one more
multiply. A tin is 16 cm across and 14 cm tall, so its radius is 8 cm.
Can it hold 2.5 litres?

```python exec
id: measuring-rooms-volume-1
tin_volume = math.pi * 8 ** 2 * 14
print(round(tin_volume), "cm³")
print(round(tin_volume / 1000, 2), "litres")
```

About 2,815 cm³, which is 2.81 litres. The 2.5 litres fit, with some
room left at the top for stirring.

Two more solids come up everywhere. A *cone* has a circle for a base
and comes to a point, like an ice cream cone or a traffic cone. Fill a
cone with water and pour it into a cylinder with the same base and
height, and it takes three cones to fill it. So a cone's volume is a
third of the cylinder's:

$$V = \frac{1}{3} \pi r^2 h$$

A *sphere* is a perfect ball, like a football. Its volume is

$$V = \frac{4}{3} \pi r^3$$

More than 2,000 years ago, Archimedes showed that a sphere fills two
thirds of the smallest cylinder that fits round it. He was so pleased
with this that he asked for it to be carved on his grave.

A scoop of ice cream is a sphere with a radius of 2.5 cm. It sits on a
cone with the same radius and a height of 11 cm. If the scoop melts,
does it all fit inside the cone? Guess, then run it.

```python exec
id: measuring-rooms-volume-2
scoop = 4 / 3 * math.pi * 2.5 ** 3
cone = 1 / 3 * math.pi * 2.5 ** 2 * 11
print(round(scoop, 1), "cm³ of ice cream")
print(round(cone, 1), "cm³ of cone")
```

About 65.4 cm³ of ice cream, and 72.0 cm³ of cone. It all fits, with a little room to spare.

## Wrapping it: surface area

The *surface area* of a solid is the total area of its outside. It is
what you would paint, or wrap in paper.

A cube has six square faces, so its surface area is $6s^2$.

A tin's outside is two circles, the lid and the base, and a label.
Peel the label off, and it unrolls into a rectangle. How long is that
rectangle? It went once round the tin, so its length is the
circumference, $2\pi r$. Its height is the tin's height, $h$. So, in
words, the surface area is two circles plus the label:

$$A = 2\pi r^2 + 2\pi r h$$

A sphere's surface area is exactly four circles of the same radius:
$A = 4\pi r^2$. Archimedes found that too.

A cone's outside is its base circle, $\pi r^2$, and its sloping side,
which has area $\pi r l$. Here $l$ is the *slant height*: the distance
from the point, down the side, to the edge of the base.

$$A = \pi r^2 + \pi r l$$

The slant height, the radius and the height make a triangle with a
right angle in it. For any triangle like that,
$l^2 = r^2 + h^2$. This is Pythagoras' theorem, which Unit 8 explains
properly; for now we use it. So $l = \sqrt{r^2 + h^2}$, and
`math.sqrt` from the last page works it out.

## Tools for solid shapes

Here are the solid shapes as toolkit functions. Most are written, and
several use the flat-shape tools: a cylinder's volume is
`circle_area(radius) * height`. Small promises, joined into bigger
ones. Two are left for you. Replace each `...` with a `return` line.

```python exec
id: measuring-rooms-toolkit-solid
toolkit: yes
import math


def cuboid_volume(length, width, height):
    """Return the volume of a box shape. For a cube, give the side three times."""
    return length * width * height


def cylinder_volume(radius, height):
    """Return the volume of a cylinder: the base circle times the height."""
    return circle_area(radius) * height


def cone_volume(radius, height):
    """Return the volume of a cone: a third of the cylinder with the same base and height."""
    ...


def sphere_volume(radius):
    """Return the volume of a sphere of this radius."""
    return 4 / 3 * math.pi * radius ** 3


def cube_surface_area(side):
    """Return the total area of the six faces of a cube."""
    return 6 * side ** 2


def cylinder_surface_area(radius, height):
    """Return the area of a closed cylinder: two circles and the label."""
    ...


def cone_surface_area(radius, height):
    """Return the area of a cone: the base circle and the sloping side.

    height is straight up from the base to the point, not the slant.
    """
    slant = math.sqrt(radius ** 2 + height ** 2)
    return circle_area(radius) + math.pi * radius * slant


def sphere_surface_area(radius):
    """Return the area of the outside of a sphere: four circles."""
    return 4 * circle_area(radius)
```

```python toolkit-reference
for: measuring-rooms-toolkit-solid
import math


def cuboid_volume(length, width, height):
    """Return the volume of a box shape. For a cube, give the side three times."""
    return length * width * height


def cylinder_volume(radius, height):
    """Return the volume of a cylinder: the base circle times the height."""
    return circle_area(radius) * height


def cone_volume(radius, height):
    """Return the volume of a cone: a third of the cylinder with the same base and height."""
    return cylinder_volume(radius, height) / 3


def sphere_volume(radius):
    """Return the volume of a sphere of this radius."""
    return 4 / 3 * math.pi * radius ** 3


def cube_surface_area(side):
    """Return the total area of the six faces of a cube."""
    return 6 * side ** 2


def cylinder_surface_area(radius, height):
    """Return the area of a closed cylinder: two circles and the label."""
    return 2 * circle_area(radius) + circle_circumference(radius) * height


def cone_surface_area(radius, height):
    """Return the area of a cone: the base circle and the sloping side.

    height is straight up from the base to the point, not the slant.
    """
    slant = math.sqrt(radius ** 2 + height ** 2)
    return circle_area(radius) + math.pi * radius * slant


def sphere_surface_area(radius):
    """Return the area of the outside of a sphere: four circles."""
    return 4 * circle_area(radius)
```

Floats round very slightly, as we saw on
[Everything is ones and zeros](tutorial:everything-is-ones-and-zeros),
so some of these tests round both sides before comparing them. Until
your two functions are written, the tests stop with an error. Which
test checks Archimedes' two thirds?

```python exec
id: measuring-rooms-toolkit-solid-tests
assert cuboid_volume(10, 10, 10) == 1000
assert round(cylinder_volume(8, 14)) == 2815
assert round(cone_volume(2.5, 11), 1) == 72.0
assert round(3 * cone_volume(3, 7), 9) == round(cylinder_volume(3, 7), 9)
assert round(sphere_volume(3), 9) == round(2 / 3 * cylinder_volume(3, 6), 9)
assert cube_surface_area(2) == 24
assert round(cylinder_surface_area(8, 14)) == 1106
assert cone_surface_area(3, 4) == 24 * math.pi
assert sphere_surface_area(1) == 4 * math.pi
print("The solid-shape tools keep their promises.")
```

The fifth test is Archimedes: a sphere of radius 3 fits inside a
cylinder of radius 3 and height 6, and fills two thirds of it. The
cone test uses a cone with radius 3 and height 4, whose slant is
exactly 5, so its area is $9\pi + 15\pi = 24\pi$.

### Your turn

A size 5 football has a radius of about 11 cm.

1. Before you run anything, guess how many litres of air it holds.
2. Use `sphere_volume` to check, and turn cm³ into litres.
3. Use `sphere_surface_area` to find how much leather covers it, in cm².

```python exec
id: measuring-rooms-solid-your-turn
# The football, in cm³, litres and cm²
```

## How much paint does the room need?

Back to the bedroom. Here are the steps, in order:

1. Find the wall area: the perimeter times the height.
2. Take away the door and the window.
3. Multiply by the number of coats. Two coats is usual.
4. Divide by 12 m² a litre, to get the litres of paint.
5. Divide by 2.5 litres a tin, to get the number of tins.
6. Round the number of tins up.

Why up? Tins come whole. We are in the natural numbers, $\mathbb{N}$,
where 2.2 tins is not something a shop sells. Rounding to the nearest
whole number gives 2 tins, and one wall goes unfinished. `math.ceil`
rounds any number up to the next whole number. Its name is short for
"ceiling".

```python exec
id: measuring-rooms-paint-1
def tins_for_walls(length, width, height, gaps, coats=2):
    """Return how many 2.5 litre tins paint the walls of a room.

    gaps is the area in m² that is not painted: doors and windows.
    One litre covers 12 m² for one coat.
    """
    wall_area = rectangle_perimeter(length, width) * height - gaps
    litres = wall_area * coats / 12
    return math.ceil(litres / 2.5)


door = rectangle_area(2, 0.8)
window = rectangle_area(1.2, 1)
print(tins_for_walls(4, 3.5, 2.4, door + window))
print(round(33.2 * 2 / 12 / 2.5, 2))
```

Three tins. The second line shows the number before rounding up: 2.21
tins. Look at how `tins_for_walls` is built. It asks
`rectangle_perimeter` for one job, and trusts it. That is the whole
idea of a toolkit.

### Your turn

1. What would one coat need? Call `tins_for_walls` with `coats=1`.
   Predict first.
2. The ceiling needs painting too: one coat over the floor's area. Write
   `tins_for_ceiling(length, width)` in the same way, using
   `rectangle_area`.
3. Is it fair to add the two answers to find the tins for the whole
   job? Try a room where it makes a difference. (Hint: think about what
   rounding up twice does.)

```python exec
id: measuring-rooms-paint-your-turn
# Your tins_for_ceiling, and the whole job
```

## Four questions, looking back

| The question | On this page |
|---|---|
| What is named here? | lengths ($l$, $w$, $h$, $r$), the number $\pi$, and a toolkit function for each shape |
| What is promised? | each formula, said in words, written in symbols, and checked by a test; bigger tools built from smaller ones |
| What happens when? | the paint steps in order: area, then gaps, then coats, then litres, then tins, rounded up last |
| What does this space let us do? | m, m² and m³ are different spaces: multiply across them, never add; tins live in $\mathbb{N}$, so we round up |

## What we have now

| Term | What it means |
|---|---|
| perimeter | the distance round a shape; a rectangle's is $2(l + w)$ |
| area, m² | the flat surface a shape covers, counted in squares |
| rectangle, square | $A = lw$; $A = s^2$ |
| triangle | $A = \frac{1}{2}bh$, with the height at a right angle to the base |
| radius, diameter, circumference | centre to edge; right across, $d = 2r$; round the edge, $C = 2\pi r$ |
| $\pi$, `math.pi` | the circumference of any circle divided by its diameter, about 3.14159 |
| circle | $A = \pi r^2$ |
| volume, cm³, litre | the space a solid takes up; 1 litre is 1,000 cm³ |
| cuboid, cylinder, cone, sphere | $V = lwh$; $V = \pi r^2 h$; $V = \frac{1}{3}\pi r^2 h$; $V = \frac{4}{3}\pi r^3$ |
| surface area | the total area of a solid's outside: cube $6s^2$; cylinder $2\pi r^2 + 2\pi r h$; cone $\pi r^2 + \pi r l$; sphere $4\pi r^2$ |
| slant height | the distance from a cone's point down its side: $l = \sqrt{r^2 + h^2}$ |
| `math.ceil()` | rounds a number up to the next whole number |
| your shape tools | `rectangle_perimeter`, `rectangle_area`, `triangle_area`, `circle_circumference`, `circle_area`, and the volumes and surface areas of the solids |
