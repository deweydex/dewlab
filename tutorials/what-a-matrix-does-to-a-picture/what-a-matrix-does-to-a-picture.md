---
title: "Matrix transformations: what a matrix does to a picture"
year: "2026-2027"
version: 2026.09.26.2
worlds:
  pixel-art: Pictures made of small squares, the way a screen draws them.
  starships: Starships, and the structures they are built from.
  space-scenes: Stars, planets and the paths they take across the sky.
covers:
  where-does-a-point-go:
    covers: [CMPS-LO4]
    touches: [MIT-3.2]
  a-playground:
    covers: [CMPS-LO4]
  read-the-columns:
    covers: [CMPS-LO4]
  a-matching-game:
    covers: [CMPS-LO4]
---

# Matrix transformations: what a matrix does to a picture

On the last page, a matrix was a picture. On this one, a small matrix is
an instruction that moves every point of a picture to a new place. Here
is the picture. It is an F, drawn as the corners of its outline.

```python exec
id: where-does-a-point-go-1
F = [(0, 0), (1, 0), (1, 2), (2, 2), (2, 3), (1, 3), (1, 4), (3, 4), (3, 5), (0, 5)]
print(len(F), "corners")
```

An F is useful because it is lopsided. Turn it, flip it or lean it, and
you can tell which. A square looks the same after a quarter turn or a
flip, so it would hide half of what a matrix does.

## Where does a point go?

A 2×2 matrix $\begin{bmatrix} a & b \\ c & d \end{bmatrix}$ moves the
point $(x, y)$ to

$$(ax + by, \; cx + dy)$$

The first row of the matrix makes the new $x$, and the second row the
new $y$. With `stretch = [[2, 0], [0, 1]]`, the point $(1, 2)$ goes to
$(2 \times 1 + 0 \times 2, \; 0 \times 1 + 1 \times 2) = (2, 2)$.

Can you write `transform(m, point)`? `transform_all` below it uses
`transform` on every corner of a shape. Both come with you to the later
pages.

```python exec
id: matrix-move
toolkit: yes
def transform(m, point):
    """Where the 2x2 matrix m sends the point (x, y)."""
    x, y = point
    ...


def transform_all(m, shape):
    """Every corner of shape, moved by m."""
    return [transform(m, point) for point in shape]
```

```python toolkit-reference
for: matrix-move
def transform(m, point):
    """Where the 2x2 matrix m sends the point (x, y)."""
    x, y = point
    return (m[0][0] * x + m[0][1] * y, m[1][0] * x + m[1][1] * y)


def transform_all(m, shape):
    """Every corner of shape, moved by m."""
    return [transform(m, point) for point in shape]
```

```inputs
transform([[2, 0], [0, 1]], (1, 2))
transform([[1, 1], [0, 1]], (0, 3))
transform([[0, -1], [1, 0]], (1, 0))
transform_all([[1, 0], [0, -1]], [(1, 1), (2, 3)])
```

```hint
`x, y = point` takes the point apart. The new x is `m[0][0] * x + m[0][1]
* y`: the first row of `m`, times x and y. The new y uses the second
row. Give them back together as `(new_x, new_y)`.
```

```solution
def transform(m, point):
    """Where the 2x2 matrix m sends the point (x, y)."""
    x, y = point
    new_x = m[0][0] * x + m[0][1] * y
    new_y = m[1][0] * x + m[1][1] * y
    return (new_x, new_y)


def transform_all(m, shape):
    """Every corner of shape, moved by m."""
    return [transform(m, point) for point in shape]
---
Each row of the matrix is paired with the point. The first entry is
multiplied by x, the second by y, and the two are added. The page after
next gives this pairing a name.
```

`draw_shapes` draws shapes on one pair of axes, each closed up into an
outline, with the axes through $(0, 0)$ marked in grey.

```python exec
id: matrix-draw
toolkit: yes
import matplotlib.pyplot as plt


def draw_shapes(shapes, closed=True):
    """Draw each shape, a list of (x, y) points, on one pair of axes."""
    plt.figure()
    for shape in shapes:
        xs = [x for x, y in shape]
        ys = [y for x, y in shape]
        if closed:
            xs.append(xs[0])
            ys.append(ys[0])
        plt.plot(xs, ys, marker="o")
    plt.axhline(0, color="grey", linewidth=0.5)
    plt.axvline(0, color="grey", linewidth=0.5)
    plt.gca().set_aspect("equal")
```

## A playground

One cell, one matrix. It draws the F in blue and the moved F in orange.
Change `m`, run it again, and watch what happens. Before each run, say
what you expect.

```python exec
id: a-playground-1
m = [[2, 0], [0, 1]]
draw_shapes([F, transform_all(m, F)])
```

Try these five, one at a time:

| Name | `m` |
|---|---|
| stretch | `[[2, 0], [0, 1]]` |
| squash | `[[1, 0], [0, 0.5]]` |
| turn | `[[0, -1], [1, 0]]` |
| shear | `[[1, 1], [0, 1]]` |
| flip | `[[1, 0], [0, -1]]` |

```python exec
id: a-playground-2
turn = [[0, -1], [1, 0]]
print(transform_all(turn, F)[:3])
```

```predict
`turn` moves $(1, 0)$ to $(0, 1)$. Which way will the F face?

- Turned a quarter anticlockwise, lying on its back with its arms up
  - (1, 0) points right and (0, 1) points up, so right turns into up.
- Turned a quarter clockwise
  - Turns in maths go the way a clock does.
- Upside down
  - Turning moves the top of the F to the bottom.
```

`turn` turns the F a quarter turn anticlockwise, about $(0, 0)$. The
stretch doubles its width, and the squash halves its height. The shear
leaves the bottom edge where it is and slides every point sideways by
its height, so the F leans. The flip turns it upside down across the x
axis, like a reflection in a lake, and its arms still point right. A
matrix read this way is a *transformation matrix*.

Every one of them leaves $(0, 0)$ where it is: $a \times 0 + b \times 0$
is 0 whatever the numbers. A 2×2 matrix can stretch, turn, lean and
flip, but it cannot slide a picture across the page. That needs one more
idea, on the graphics pages later in the course.

## Read the columns

Look at `turn`'s two columns: $(0, 1)$ and $(-1, 0)$. Now move the two
simplest points there are, one step right and one step up.

```python exec
id: read-the-columns-1
for name, m in [("turn", [[0, -1], [1, 0]]), ("shear", [[1, 1], [0, 1]])]:
    print(name, transform(m, (1, 0)), transform(m, (0, 1)))
```

The first column of a matrix is where $(1, 0)$ lands, and the second
column is where $(0, 1)$ lands. That is true of every 2×2 matrix, since
$a \times 1 + b \times 0 = a$ and $c \times 1 + d \times 0 = c$. And
those two points decide everything else: $(3, 2)$ is three steps right
and two up, so it lands at three of the first column plus two of the
second. So to design a matrix, decide where you want "right" and "up" to
go, and write them in as its columns.

## A matching game

Four matrices, and four pictures they made. Which made which? Decide
from the pictures before you look at the numbers.

```python exec
id: a-matching-game-1
mysteries = {
    "A": [[-1, 0], [0, 1]],
    "B": [[1, 0], [0.5, 1]],
    "C": [[0, 1], [-1, 0]],
    "D": [[0.5, 0], [0, 0.5]],
}
fig, axes = plt.subplots(1, 4, figsize=(12, 3.5))
for ax, name in zip(axes, mysteries):
    moved = transform_all(mysteries[name], F)
    for shape in [F, moved]:
        ax.plot([x for x, y in shape] + [shape[0][0]], [y for x, y in shape] + [shape[0][1]])
    ax.set_title(name)
    ax.set_aspect("equal")
plt.tight_layout()
```

```question
id: matrix-matching
type: fill-in-the-blank

- Picture A was made by a {mirror left to right|quarter turn clockwise|shear upwards|shrink to half size}.
- Picture B was made by a {shear upwards|mirror left to right|quarter turn clockwise|shrink to half size}.
- Picture C was made by a {quarter turn clockwise|shrink to half size|mirror left to right|shear upwards}.
- Picture D was made by a {shrink to half size|shear upwards|quarter turn clockwise|mirror left to right}.
```

Now the other way round. Here is a picture, made by a hidden matrix. The bottom
edge of this F has not moved, and the top has slid to the right. Which
matrix did it?

```python exec
id: guess-the-matrix-1
mystery = [(0, 0), (1, 0), (2, 2), (3, 2), (3.5, 3), (2.5, 3), (3, 4), (5, 4), (5.5, 5), (2.5, 5)]
draw_shapes([F, mystery])
```

```python exec
id: guess-the-matrix-2
your_guess = [[1, 0], [0, 1]]
print(transform_all(your_guess, F) == mystery)
```

```inputs
transform_all(your_guess, F)
```

```hint
Read the columns. Where did $(1, 0)$, the corner one step right of the
origin, go? And the top corner $(0, 5)$ went to $(2.5, 5)$, so where
would $(0, 1)$ go, a fifth of the way up?
```

```solution
{{include: setup/matrices/transform.py}}

F = [(0, 0), (1, 0), (1, 2), (2, 2), (2, 3), (1, 3), (1, 4), (3, 4), (3, 5), (0, 5)]
mystery = [(0, 0), (1, 0), (2, 2), (3, 2), (3.5, 3), (2.5, 3), (3, 4), (5, 4), (5.5, 5), (2.5, 5)]
your_guess = [[1, 0.5], [0, 1]]
print(transform_all(your_guess, F) == mystery)
---
$(1, 0)$ stayed where it was, so the first column is $(1, 0)$. $(0, 5)$
went to $(2.5, 5)$, so $(0, 1)$ goes to $(0.5, 1)$, the second column.
It is a shear by a half. Each point slides right by half its height.
```

## Your world

A shape from the world you chose, and a matrix to move it.

<div class="dl-world" data-world="pixel-art">

On the last page, `transpose` flipped a picture corner to corner. Is
there a matrix that does the same to the F's points? Which matrix swaps
each point's x and y? Can you find it, and a matrix that mirrors the F
left to right?

```python exec
id: matrix-your-world--pixel-art
swap = [[1, 0], [0, 1]]
mirror = [[1, 0], [0, 1]]
draw_shapes([F, transform_all(swap, F)])
draw_shapes([F, transform_all(mirror, F)])
```

```inputs
transform(swap, (1, 2))
transform(mirror, (1, 2))
```

```hint
Read the columns. Swapping x and y sends $(1, 0)$ to $(0, 1)$ and $(0,
1)$ to $(1, 0)$. A mirror left to right sends $(1, 0)$ to $(-1, 0)$ and
leaves $(0, 1)$ alone.
```

```solution
{{include: setup/matrices/transform.py}}

F = [(0, 0), (1, 0), (1, 2), (2, 2), (2, 3), (1, 3), (1, 4), (3, 4), (3, 5), (0, 5)]
swap = [[0, 1], [1, 0]]
mirror = [[-1, 0], [0, 1]]
draw_shapes([F, transform_all(swap, F)])
draw_shapes([F, transform_all(mirror, F)])
---
`swap` is a flip across the line $y = x$: the transpose from the last
page, done to points instead of to a grid. Pixels are counted from the
top-left and points from the bottom-left, so the grid's flip and the
points' flip look like mirror images of each other, but both flip
across a diagonal.
```

</div>

<div class="dl-world" data-world="starships">

A starship is drawn nose up. To steer it, it turns about its centre. A
turn by an angle $\theta$ anticlockwise is the matrix
$\begin{bmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta
\end{bmatrix}$. Can you write `turn_by(degrees)`, and turn the ship 30°,
then 90°?

```python exec
id: matrix-your-world--starships
import math

ship = [(0, 4), (1, 1), (2, -1), (1, -0.5), (-1, -0.5), (-2, -1), (-1, 1)]


def turn_by(degrees):
    """The matrix that turns a shape anticlockwise by this many degrees."""
    ...
```

```inputs
[[round(v, 3) for v in row] for row in turn_by(90)]
[[round(v, 3) for v in row] for row in turn_by(30)]
```

```hint
`math.radians(degrees)` changes degrees to the unit `math.cos` and
`math.sin` use. The first column is where $(1, 0)$ goes after the turn:
$(\cos\theta, \sin\theta)$.
```

```solution
{{include: setup/matrices/transform.py}}

import math

ship = [(0, 4), (1, 1), (2, -1), (1, -0.5), (-1, -0.5), (-2, -1), (-1, 1)]


def turn_by(degrees):
    """The matrix that turns a shape anticlockwise by this many degrees."""
    angle = math.radians(degrees)
    return [[math.cos(angle), -math.sin(angle)],
            [math.sin(angle), math.cos(angle)]]


draw_shapes([ship,
             transform_all(turn_by(30), ship),
             transform_all(turn_by(90), ship)])
---
At 90°, $\cos$ is 0 and $\sin$ is 1, so `turn_by(90)` is the `turn` from
the playground, give or take a tiny rounding error: `math.cos` of a
quarter turn comes out as about $6 \times 10^{-17}$, not exactly 0.
The first column is where "right" goes, $(\cos\theta, \sin\theta)$, a
point a distance 1 from the centre at angle $\theta$.
```

</div>

<div class="dl-world" data-world="space-scenes">

The seven bright stars of the Plough, in degrees from the pole star,
drawn as they stand at one moment in the night. The sky turns about
the pole star, anticlockwise as you face north, about 15° every hour.
Can you draw where the Plough is 6 hours later, and 12 hours later?

```python exec
id: matrix-your-world--space-scenes
import math

# Alkaid, Mizar, Alioth, Megrez, Phecda, Merak, Dubhe, and back to Megrez
plough = [(-18.4, -36.3), (-12.6, -32.7), (-7.9, -33.1), (-2.2, -32.9),
          (1.0, -36.3), (8.4, -32.5), (6.9, -27.4), (-2.2, -32.9)]
pole_star = [(0, 0)]
draw_shapes([plough, pole_star], closed=False)


def turn_by(degrees):
    """The matrix that turns a shape anticlockwise by this many degrees."""
    ...
```

```hint
15° an hour for 6 hours is 90°. A turn by an angle $\theta$ is
$\begin{bmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta
\end{bmatrix}$, with the angle in radians from `math.radians`.
```

```solution
{{include: setup/matrices/transform.py}}

import math

plough = [(-18.4, -36.3), (-12.6, -32.7), (-7.9, -33.1), (-2.2, -32.9),
          (1.0, -36.3), (8.4, -32.5), (6.9, -27.4), (-2.2, -32.9)]
pole_star = [(0, 0)]


def turn_by(degrees):
    """The matrix that turns a shape anticlockwise by this many degrees."""
    angle = math.radians(degrees)
    return [[math.cos(angle), -math.sin(angle)],
            [math.sin(angle), math.cos(angle)]]


draw_shapes([plough,
             transform_all(turn_by(90), plough),
             transform_all(turn_by(180), plough),
             pole_star], closed=False)
---
Six hours turns it a quarter, and twelve hours turn it half way round.
Twelve hours later, the Plough is on the other side of the pole star,
upside down. The shape never changes, because a turn changes no
distances. The two stars at the end of the bowl, Merak and Dubhe, always
point at the pole star. The line from Merak through Dubhe, made five
times as long, reaches it. (The sky turns 360° in just under 24
hours, so 15° an hour is close, not exact.)
```

</div>

## Looking back

On this page the same four numbers were a picture's instruction, and
their columns said where "right" and "up" go. Can you say why every
matrix on this page left the point $(0, 0)$ exactly where it was?

A challenge: a matrix that flattens the F onto a line, so every point
lands on the line $y = x$. What do its columns have to be? And once it
is flat, could any matrix bring the F back?

```python challenge
F = [(0, 0), (1, 0), (1, 2), (2, 2), (2, 3), (1, 3), (1, 4), (3, 4), (3, 5), (0, 5)]


def transform(m, point):
    x, y = point
    return (m[0][0] * x + m[0][1] * y, m[1][0] * x + m[1][1] * y)


flatten = [[1, 0], [0, 1]]   # change this so every point lands on y = x
print([transform(flatten, p) for p in F])
```

The next page, [Matrix multiplication](tutorial:multiplying-grids),
asks what happens when one move follows another, such as a shear and
then a turn. Is there one matrix that does both?

## Where to read more

Grant Sanderson (3Blue1Brown) (2016). *Essence of Linear Algebra, Chapter
3: Linear Transformations and Matrices.*
<https://www.youtube.com/watch?v=kYB8IZa5AuE>. The columns-as-landing-
places idea on this page, animated far better than a static plot can.

Hughes, J. F., van Dam, A., McGuire, M., Sklar, D. F., Foley, J. D.,
Feiner, S. K. and Akeley, K. (2013). *Computer Graphics: Principles and
Practice* (3rd ed.). Addison-Wesley. Chapter 6 covers these
transformation matrices as they are used to move things on a screen.

Looking Glass Universe (2018). *Matrices, matrix multiplication and linear
transformations.* <https://www.youtube.com/watch?v=CBIO4xJ1Cok>. A matrix
as instructions for where each arrow goes, which is how this page moves a
picture. About fourteen minutes.
