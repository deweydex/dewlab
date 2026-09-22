---
title: "The Fourth Number"
year: "2026-2027"
version: 2026.09.21.1
covers:
  a-move-no-matrix-can-make:
    covers: [CMPS-LO4]
  one-more-row:
    covers: [CMPS-LO4]
  everything-in-one-matrix:
    covers: [CMPS-LO4]
  the-divide-as-a-matrix:
    covers: [CMPS-LO4]
  field-of-view:
    covers: [CMPS-LO4]
    touches: [MIT-4.6]
---

# The Fourth Number

Two tutorials, two kinds of step. Turning a cube was a matrix. Moving
it was not: `move` added a number to every coordinate, and no
multiplication does that. This tutorial fixes that with a trick that
looks like cheating. Then it uses the same trick to turn the
perspective divide itself into a matrix. By the end, everything a
camera does to a point is one multiplication and one division, which
is exactly how a graphics card works.

Everything from the last two tutorials, gathered into one cell. Let's
run it first, and then it is out of the way:

```python exec
id: a-move-no-matrix-can-make-1
{{include: setup/cube.py}}
```

## A Move No Matrix Can Make

Is there a 3×3 matrix that shifts every point two units to the right?
Think about the origin, $(0, 0, 0)$, before you try to build one.
Whatever the matrix holds, every entry of it gets multiplied by a zero:

```python exec
id: a-move-no-matrix-can-make-2
origin = [[0], [0], [0]]
any_matrix = [[2, 7, 1], [-3, 5, 0], [4, 4, 4]]
print(multiply(any_matrix, origin))
```

Let's do the top row by hand: $2 \cdot 0 + 7 \cdot 0 + 1 \cdot 0 = 0$.
The other two rows are the same story. The origin cannot move. Every
3×3 matrix leaves it where it is, so no 3×3 matrix can move
everything.

This matters, because a ***scene***, everything the camera can see, is
a long chain of moves and turns. For one car in a racing game:

1. Turn the wheel about its own axle.
2. Move the wheel onto the car.
3. Turn the car to face down the road.
4. Move the car along the road.
5. Turn and move the whole world so that the camera is at the origin,
   looking along $z$.

A ***graphics card***, the part of a computer that draws, wants to
combine that whole chain into one matrix, work it out once, and apply
it once to every point. It cannot do that while moving is an addition
and turning is a multiplication. They are different kinds of step, and
a chain of different kinds of step cannot be combined into one.

```question
id: a-move-no-matrix-can-make-3
type: multiple-choice
correct: 1

Which of these can a 3×3 matrix do to a cube centred on the origin?

- Turn it about its centre
- Slide it two units to the right
- Both of those
```

## One More Row

Here is the trick. Give every point a fourth number, and make it 1. The
cube gets a fourth row, all ones. Now a 4×4 matrix's last column gets
multiplied by that 1 and added on:

$$\begin{bmatrix} 1 & 0 & 0 & d_x \\ 0 & 1 & 0 & d_y \\ 0 & 0 & 1 & d_z \\ 0 & 0 & 0 & 1 \end{bmatrix}
\begin{bmatrix} x \\ y \\ z \\ 1 \end{bmatrix} =
\begin{bmatrix} x + d_x \\ y + d_y \\ z + d_z \\ 1 \end{bmatrix}$$

Work through the top row: $1 \cdot x + 0 \cdot y + 0 \cdot z + d_x \cdot 1$.
The $d_x$ gets in because it is multiplied by the 1 at the bottom. The
last row, $0, 0, 0, 1$, puts the 1 back, so that the next matrix along
can do the same.

```python exec
id: one-more-row-1
def with_ones(points):
    return points + [[1] * len(points[0])]

def translation(dx, dy, dz):
    return [[1, 0, 0, dx],
            [0, 1, 0, dy],
            [0, 0, 1, dz],
            [0, 0, 0, 1]]

cube4 = with_ones(cube)
shifted = multiply(translation(0, 0, 5), cube4)
print("z row:  ", shifted[2])
print("ones row:", shifted[3])
```

The $z$ row has gone from $-1$ and $1$ to $4$ and $6$. The cube was
pushed out five units by a multiplication, which could not be done a
moment ago. The first three rows are an ordinary set of points again,
so `draw` can have them:

```python exec
id: one-more-row-2
draw(shifted[:3])
```

Three new words, for three things you have just seen:

- A point written with an extra 1 on the end is in ***homogeneous
  coordinates***. Homogeneous means "all of one kind", and the point
  of it is that moves and turns become one kind of step.
- The fourth number is called ***w***. For now it stays at 1.
- A matrix shaped like `translation` is a ***translation matrix***.
  Translation is the graphics word for a move that keeps the shape and
  the direction and only changes the position.

There is nothing four-dimensional going on. The fourth number is a
trick for making addition look like multiplication.

### Your turn

A turn needs to become 4×4 too, to sit in the same chain. Put the 3×3
rotation in the top-left corner, a 1 in the bottom-right, and zeros in
the rest. How might you write `rotation_y(angle)` that way, reusing
`rotate_y` for the 3×3 part?

```python exec
id: one-more-row-3
hint: Take each row of rotate_y(angle) and add a 0 on the end, then add the row [0, 0, 0, 1].
# Your rotation_y(angle), a 4x4 matrix
```

```python exec
id: one-more-row-4
check(multiply(rotation_y(0), cube4), cube4)
```

## Everything in One Matrix

Now a move and a turn are the same kind of thing, and the product of
the two is a single matrix that does both:

```python exec
id: everything-in-one-matrix-1
place = multiply(translation(0, 0, 5), rotation_y(math.radians(30)))
draw(multiply(place, cube4)[:3])
```

That is the turned cube from the last tutorial, drawn with one
multiplication instead of a `multiply` and then a `move`. The matrix
nearest the points acts first, so `place` turns the cube on the spot
and then pushes it out. Swap the two and you get the other picture
from last time, the cube swung round the camera:

```python exec
id: everything-in-one-matrix-2
swing = multiply(rotation_y(math.radians(15)), translation(0, 0, 5))
draw(multiply(swing, cube4)[:3])
```

### Your turn

Sixty frames of `swing`, with a different angle in each, is the ball's
orbit from [A Point on the Screen](tutorial:a-point-on-the-screen)
with a cube in place of the ball. Could you draw four of those frames,
at $0°$, $30°$, $60°$ and $90°$? `plt.subplots(1, 4)` and `plt.sca` are
in the flip-book cells of the last tutorial if you want the shape of
the loop.

```python exec
id: everything-in-one-matrix-3
hint: Build swing inside the loop from the frame's own angle. The cube leaves the picture by 90 degrees, which is fine. Where has it gone?
```

## The Divide as a Matrix

Dividing by $z$ is not a multiplication, so no matrix can do it. But a
matrix can *arrange* for it. Here is the arrangement. After the
multiplying is done, every point is divided by its own fourth number,
$w$. So far $w$ has been 1 throughout, and dividing by 1 changes
nothing. Now watch what this matrix does to $w$:

$$P = \begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 1 & 0 \end{bmatrix}$$

The last row reads $0, 0, 1, 0$: the new $w$ is $z$. Let's follow one
point through, the corner $(2, 1, 4, 1)$:

1. Multiply by $P$: the first three rows pass $x$, $y$ and $z$ through
   unchanged, and the last row copies $z$ into $w$. Result:
   $(2, 1, 4, 4)$.
2. Divide everything by $w = 4$: $(0.5, 0.25, 1, 1)$.

The first two numbers are $2/4$ and $1/4$: the perspective divide,
exactly as [A Point on the
Screen](tutorial:a-point-on-the-screen#why-dividing-works) had it.

```python exec
id: the-divide-as-a-matrix-1
simple_projection = [[1, 0, 0, 0],
                     [0, 1, 0, 0],
                     [0, 0, 1, 0],
                     [0, 0, 1, 0]]

def divide_by_w(points):
    xs, ys, zs, ws = points
    return [[x / w for x, w in zip(xs, ws)], [y / w for y, w in zip(ys, ws)]]

on_screen = divide_by_w(multiply(simple_projection, shifted))
check(on_screen, project(shifted[:3]))
```

The two agree, and the whole process now fits in one line:

```python exec
id: the-divide-as-a-matrix-2
camera = multiply(simple_projection, place)
draw_edges(divide_by_w(multiply(camera, cube4)))
```

One matrix, `camera`, built once from a projection, a move and a turn.
Then, for every point in the scene, one multiplication and one divide.
A matrix shaped like $P$ is a ***projection matrix***. The divide by
$w$ afterwards is the perspective divide, under the name graphics
people use for it. This is the arrangement a graphics card is built
around: it multiplies millions of points by one 4×4 matrix, divides
each by its $w$, and draws. That is why a game can draw a whole city
sixty times a second. Each point is one multiplication and one divide,
and a graphics card does thousands of those at the same time.

## Field of View

The blog post this series follows ends with the projection matrix a
graphics card is really handed. It differs from `simple_projection` in
two places.

The first is the pair of 1s at the top of the diagonal. They become a
number $f$. This is where the zoom lens from the first tutorial comes
back. A camera is described by its ***field of view***, the angle it
can see from one edge of the picture to the other, and

$$f = \frac{1}{\tan(\text{fov} / 2)}$$

A wide field of view gives a small $f$, and everything is drawn smaller
to fit it in. A narrow one gives a large $f$, and everything is drawn
bigger, like looking through a zoom lens.

```python exec
id: field-of-view-1
for fov in [30, 60, 90, 120]:
    f = 1 / math.tan(math.radians(fov) / 2)
    print(f"{fov} degrees: f = {f:.2f}")
```

The second difference is the third row, which so far has just passed
$z$ through. A graphics card needs to know, for every pixel, which of
several surfaces is nearest, so that a wall in front hides the wall
behind it. So it keeps a depth for each pixel, and it wants that depth
as a number between $-1$ and $1$. The third row does the conversion. It
uses two more numbers: the depths of the near plane and the ***far
plane***, the nearest and the farthest anything is allowed to be. The
near plane is the rule the first tutorial's orbit was missing.

$$P = \begin{bmatrix} f & 0 & 0 & 0 \\ 0 & f & 0 & 0 \\ 0 & 0 & \dfrac{\text{far} + \text{near}}{\text{far} - \text{near}} & \dfrac{-2 \cdot \text{far} \cdot \text{near}}{\text{far} - \text{near}} \\ 0 & 0 & 1 & 0 \end{bmatrix}$$

```python exec
id: field-of-view-2
def projection(fov_degrees, near, far):
    f = 1 / math.tan(math.radians(fov_degrees) / 2)
    depth_scale = (far + near) / (far - near)
    depth_shift = -2 * far * near / (far - near)
    return [[f, 0, 0, 0],
            [0, f, 0, 0],
            [0, 0, depth_scale, depth_shift],
            [0, 0, 1, 0]]

for depth in [1, 2, 5, 10, 20]:
    point = multiply(projection(60, near=1, far=20), [[0], [0], [depth], [1]])
    x, y, z, w = [row[0] for row in point]
    print(f"depth {depth:2} -> {z / w:.3f}")
```

Reading the printout:

- Depth 1, the near plane, comes out as exactly $-1$.
- Depth 20, the far plane, comes out as exactly $1$.
- Anything whose converted depth falls outside that range is
  ***clipped***: cut away before the divide. That is how a renderer
  avoids ever dividing by a depth of zero.
- The range is shared out unevenly. Depths 1 to 2 use up half of it,
  and 10 to 20 use a twentieth. Nearby things get the finest depth
  steps. That is where you would most easily notice two surfaces, one
  just behind the other, drawn in the wrong order.

Here is the cube through two lenses, a wide one and a narrow one, with
the screen's edges now at $-1$ and $1$:

```python exec
id: field-of-view-3
figure, frames = plt.subplots(1, 2, figsize=(8, 4))
for frame, fov in zip(frames, [100, 40]):
    camera = multiply(projection(fov, near=1, far=20), place)
    plt.sca(frame)
    draw_edges(divide_by_w(multiply(camera, cube4)), limit=1)
    frame.set_title(f"field of view {fov}°")
```

The blog post's matrix has a $-1$ where ours has a $1$ in the last row,
and a $w$ that is $-z$ rather than $z$. That is because its camera
looks along the negative $z$ axis, which is what most graphics
libraries do, and ours has looked along positive $z$ since the first
tutorial. The arithmetic is the same either way. It also divides $f$ by
the picture's width-to-height ratio in the top-left entry, so that a
wide screen does not stretch a circle into an oval. Our pictures are
square, so that ratio is 1 and the correction vanishes.

### Your turn

A near plane very close to the camera is tempting, since nothing gets
clipped. What does `projection(60, near=0.01, far=100)` do to the
converted depths of 1, 2, 5, 10 and 20? Where has most of the range
gone?

```python exec
id: field-of-view-4
hint: Copy the loop from the cell above and change near and far. Compare the converted depths of 10 and 20.
```

## Reflection

Three tutorials, and the whole of a camera fits in a 4×4 matrix and a
divide. Which of the two tricks felt more like cheating: the row of
ones that lets a matrix add, or the last row that lets a divide hide
inside a multiplication? Both are ordinary matrix multiplication, which
you built by hand out of the dot product in [Multiplying
Grids](tutorial:multiplying-grids). Nothing new was added to the
arithmetic. What changed was what the rows and columns were made to
mean.

A browser has all of this built in. CSS has a property called
`perspective`, and it is this divide. [An Orbit in Pure
CSS](tutorial:an-orbit-in-css), on the Web Authoring course, has the
ball from the first tutorial going round with no arithmetic written
down at all.

## Where to Read More

O'Flaherty-Chan, G. (2026). *Divide by depth for instant 3D.*
<https://gabrieloc.com/2026/09/15/perspective.html>. The post whose
closing matrix this tutorial builds up to, and a clear answer to the
question "what is the extra 1 for?".

Scratchapixel. *The Perspective and Orthographic Projection Matrix.*
<https://www.scratchapixel.com/lessons/3d-basic-rendering/perspective-and-orthographic-projection-matrix/>.
Every entry of the matrix in Field of View derived from the near plane,
the far plane and the field of view, one at a time.

Grant Sanderson (3Blue1Brown) (2016). *Essence of Linear Algebra,
Chapter 4: Matrix Multiplication as Composition.*
<https://www.youtube.com/watch?v=XkY2DOUCWMU>. Why a chain of matrices
is one matrix, which is the whole reason a graphics card wants moving
to be a multiplication.
