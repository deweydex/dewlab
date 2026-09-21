---
title: "Turning a Cube"
year: "2026-2027"
version: 2026.09.21.1
covers:
  eight-corners-twelve-edges:
    covers: [CMPS-LO4]
  a-matrix-that-turns:
    covers: [CMPS-LO4]
    touches: [MIT-4.6]
  a-flip-book:
    covers: [CMPS-LO4]
  two-turns-at-once:
    covers: [CMPS-LO4]
---

# Turning a Cube

[A Point on the Screen](tutorial:a-point-on-the-screen) projected posts
and a ball, one point at a time. A cube is eight points, and the
interesting thing about a cube is not the points but the lines between
them, and what happens to the whole shape when it turns. Turning, it
turns out, is a matrix, and the `multiply` you built in [Multiplying
Grids](tutorial:multiplying-grids) does all the work.

## Eight Corners, Twelve Edges

A cube two units on a side, centred on $(0, 0, 0)$, so every corner is
some mix of $-1$ and $1$:

```python exec
id: eight-corners-twelve-edges-1
import matplotlib.pyplot as plt

cube = [
    [-1, 1, 1, -1, -1, 1, 1, -1],   # x of each corner
    [-1, -1, 1, 1, -1, -1, 1, 1],   # y
    [-1, -1, -1, -1, 1, 1, 1, 1],   # z
]
edges = [(0, 1), (1, 2), (2, 3), (3, 0),   # the square at the front
         (4, 5), (5, 6), (6, 7), (7, 4),   # the square at the back
         (0, 4), (1, 5), (2, 6), (3, 7)]   # the four joining them
```

This is the layout the square had in [What a Matrix Does to a
Picture](tutorial:what-a-matrix-does-to-a-picture): one row per
coordinate, one column per point, so that a matrix can be applied to
every corner in a single multiplication. There are three rows now
instead of two. `edges` says which corners to join, by their column
numbers, and there are twelve of them.

The cube is sitting exactly where the camera stands, so before anything
can be projected it has to be pushed out in front. `move` adds a fixed
amount to every coordinate, and `project` is the divide from the last
tutorial, done to a whole row of points at once:

```python exec
id: eight-corners-twelve-edges-2
def move(points, dx, dy, dz):
    xs, ys, zs = points
    return [[x + dx for x in xs], [y + dy for y in ys], [z + dz for z in zs]]

def project(points):
    xs, ys, zs = points
    return [[x / z for x, z in zip(xs, zs)], [y / z for y, z in zip(ys, zs)]]

print(project(move(cube, 0, 0, 5)))
```

Sixteen numbers, and not much of a cube yet. Drawing the twelve edges
between them is what makes it one:

```python exec
id: eight-corners-twelve-edges-3
def draw_edges(screen_points, color="C0", limit=0.6):
    screen_xs, screen_ys = screen_points
    for start, end in edges:
        plt.plot([screen_xs[start], screen_xs[end]],
                 [screen_ys[start], screen_ys[end]], color=color)
    plt.xlim(-limit, limit)
    plt.ylim(-limit, limit)
    plt.gca().set_aspect("equal")

def draw(points, color="C0"):
    draw_edges(project(points), color)

draw(move(cube, 0, 0, 5))
```

The front face is the bigger square and the back face is the smaller
one inside it, because it is two units further away. Nothing here drew
a cube. Twelve straight lines were drawn between projected corners, and
your eye did the rest.

### Your turn

What does the cube look like from further away? Try pushing it out to
depth 20 instead of 5. And what happens if you move it sideways as well,
say two units to the right, so that you are no longer looking at it
straight on?

```python exec
id: eight-corners-twelve-edges-4
hint: draw(move(cube, 0, 0, 20)) for the first. Compare the sizes of the two squares.
```

Far away, the two squares are nearly the same size and the cube looks
flat. That is also why a photograph taken with a long lens from a
distance looks flat, and one taken up close with a wide lens does not.

## A Matrix That Turns

In the gallery of 2×2 matrices, `rotate90 = [[0, -1], [1, 0]]` turned
the square a quarter turn. For any angle $\theta$, the matrix that turns
the plane by that angle is

$$R(\theta) = \begin{bmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{bmatrix}$$

Read its columns the way you learned to. The first column is where
$(1, 0)$ lands: at $(\cos\theta, \sin\theta)$, which is the point on the
unit circle at angle $\theta$. The second column is where $(0, 1)$
lands, a quarter turn further round. Put in $\theta = 90°$ and the two
columns are $(0, 1)$ and $(-1, 0)$, which are the columns of `rotate90`.

In three dimensions, turning about the vertical axis leaves $y$ alone
and turns $x$ and $z$ into each other, the way a turntable does. So the
matrix is the 2D one with an extra row and column that do nothing:

$$R_y(\theta) = \begin{bmatrix} \cos\theta & 0 & \sin\theta \\ 0 & 1 & 0 \\ -\sin\theta & 0 & \cos\theta \end{bmatrix}$$

To apply it we need `multiply`, which is the same as it was, exactly as
before, since each page here begins with no code from previous pages:

```python exec
id: a-matrix-that-turns-1
import math

def dot(a, b):
    return sum(x * y for x, y in zip(a, b))

def transpose(m):
    rows, cols = len(m), len(m[0])
    return [[m[r][c] for r in range(rows)] for c in range(cols)]

def multiply(a, b):
    bt = transpose(b)
    return [[dot(row, col) for col in bt] for row in a]
```

```python exec
id: a-matrix-that-turns-2
def rotate_y(angle):
    cos_angle, sin_angle = math.cos(angle), math.sin(angle)
    return [[cos_angle, 0, sin_angle],
            [0, 1, 0],
            [-sin_angle, 0, cos_angle]]

turned = multiply(rotate_y(math.radians(30)), cube)
draw(move(turned, 0, 0, 5))
```

Notice the order. The cube is turned first, while it is still centred
on the origin, and moved out to depth 5 afterwards. Turning is always
about the origin, because $(0, 0, 0)$ is the one point every matrix
leaves alone. What happens if you do it the other way round, and turn
the cube after moving it?

```python exec
id: a-matrix-that-turns-3
draw(multiply(rotate_y(math.radians(15)), move(cube, 0, 0, 5)))
```

Now the cube swings off to the side, because it is being turned about
the camera rather than about its own centre. Keep going, a few degrees
at a time, and it would go all the way round the camera and come back.
That is the ball's orbit from the last tutorial, done with a matrix
instead of with $\cos$ and $\sin$ written out by hand. The ball was a
single point being turned about the camera.

### Your turn

Turning about the vertical axis is `rotate_y`. Nodding, forwards and
back, is turning about the $x$ axis: it leaves $x$ alone and turns $y$
and $z$ into each other. How might you write `rotate_x(angle)`? Start
from the 2D matrix and decide which row and column should be the one
that does nothing.

```python exec
id: a-matrix-that-turns-4
hint: The first row and first column are [1, 0, 0]. The 2D rotation matrix fills the other four places, cos on the diagonal and the minus sign top right.
# Your rotate_x(angle)
```

A quarter turn about $x$ should send the top of the cube, $(0, 1, 0)$,
to the back, $(0, 0, 1)$:

```python exec
id: a-matrix-that-turns-5
check(multiply(rotate_x(math.radians(90)), [[0], [1], [0]]), [[0.0], [0.0], [1.0]])
```

## A Flip-Book

Twelve frames, each with the cube turned a further thirtieth of a turn:

```python exec
id: a-flip-book-1
figure, frames = plt.subplots(3, 4, figsize=(10, 7.5))
for index, frame in enumerate(frames.flat):
    angle = index * 2 * math.pi / 12
    plt.sca(frame)
    draw(move(multiply(rotate_y(angle), cube), 0, 0, 5))
    frame.set_xticks([])
    frame.set_yticks([])
    frame.set_title(f"{round(math.degrees(angle))}°")
```

At 90° the picture is the same as at 0°, because a different face has
turned to the front and a cube's faces are all alike. Halfway between,
at 45°, it is at its widest, with two faces showing. A game does exactly this, sixty times a second:
the same eight columns, multiplied by a slightly different matrix each
time, then divided and drawn.

## Two Turns at Once

A cube spinning on a turntable, seen straight on, never shows you its
top. To look down on it a little, tilt it about $x$ as well, by a fixed
angle, and let the spin about $y$ carry on underneath. Two matrices,
applied one after the other, are one matrix: their product.

```python exec
id: two-turns-at-once-1
tilt = rotate_x(math.radians(-25))
figure, frames = plt.subplots(1, 4, figsize=(10, 2.5))
for index, frame in enumerate(frames.flat):
    angle = index * 2 * math.pi / 12
    both = multiply(tilt, rotate_y(angle))
    plt.sca(frame)
    draw(move(multiply(both, cube), 0, 0, 5))
    frame.set_xticks([])
    frame.set_yticks([])
```

`multiply(tilt, rotate_y(angle))` spins first and tilts second, since
the matrix nearest the points is the one that acts first. That is the
one you want here: spin the cube on its own vertical axis, then tip the
whole turntable towards the camera.

### Your turn

What does `multiply(rotate_y(angle), tilt)` do instead, with the two
swapped? Draw the same four frames and compare them. [Order
Matters](tutorial:multiplying-grids#order-matters) said that $AB$ and
$BA$ are different matrices. Here is what the difference looks like.

```python exec
id: two-turns-at-once-2
hint: Copy the cell above and swap the two arguments to multiply. Watch which axis the cube spins about.
```

## Reflection

Eight columns of numbers, a list of which to join, and a matrix. Was
there a moment where the cube stopped being sixteen numbers and started
being a cube? For most people it is the first `draw`, which is worth
noticing, because nothing changed in the numbers at that moment.

Turning was a matrix. Moving was not: `move` added a number to every
coordinate, and there is no 3×3 matrix that does that, since every one
of them leaves the origin where it is. The next tutorial fixes that
with a trick that looks like cheating, and then uses the same trick on
the perspective divide itself.

## Where to Read More

Grant Sanderson (3Blue1Brown) (2016). *Essence of Linear Algebra,
Chapter 4: Matrix Multiplication as Composition.*
<https://www.youtube.com/watch?v=XkY2DOUCWMU>. Why two turns applied
one after the other are one matrix, and why the one nearest the points
goes first.

O'Flaherty-Chan, G. (2026). *Divide by depth for instant 3D.*
<https://gabrieloc.com/2026/09/15/perspective.html>. The rotating cube
this tutorial's flip-book is a paper version of, drawn live in a
browser.

Hughes, J. F., van Dam, A., McGuire, M., Sklar, D. F., Foley, J. D.,
Feiner, S. K. and Akeley, K. (2013). *Computer Graphics: Principles and
Practice* (3rd ed.). Addison-Wesley. Its chapter on transformations in
three dimensions has every rotation matrix, and the reasons for the
signs.
