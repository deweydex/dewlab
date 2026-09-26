---
title: "The rotation matrix: turning a cube in 3D — Practice"
practice_for: turning-a-cube
year: "2026-2027"
version: 2026.09.26.1
---

# The rotation matrix: turning a cube in 3D — Practice

Read the matrix before you run it. The columns say where the three
axes land, and that is usually enough to predict the picture.

## Reading a rotation

```python exec
id: reading-1
import math


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def transpose(m):
    rows, cols = len(m), len(m[0])
    return [[m[r][c] for r in range(rows)] for c in range(cols)]


def multiply(a, b):
    bt = transpose(b)
    return [[dot(row, col) for col in bt] for row in a]


def rotate_y(angle):
    cos_angle, sin_angle = math.cos(angle), math.sin(angle)
    return [[cos_angle, 0, sin_angle],
            [0, 1, 0],
            [-sin_angle, 0, cos_angle]]


def rotate_x(angle):
    cos_angle, sin_angle = math.cos(angle), math.sin(angle)
    return [[1, 0, 0],
            [0, cos_angle, -sin_angle],
            [0, sin_angle, cos_angle]]


def rounded(matrix):
    return [[round(value, 3) for value in row] for row in matrix]


print(rounded(rotate_y(math.radians(90))))
```

**1.** Where does `rotate_y` at a quarter turn send the point
$(1, 0, 0)$? Read it from the matrix's first column before you look at
the printout.

<details class="dl-answer"><summary>answer</summary>

To $(0, 0, -1)$. The first column of $R_y(\theta)$ is
$(\cos\theta, 0, -\sin\theta)$, and at $90°$ that is $(0, 0, -1)$. A
point out to the right swings round to be one unit in front of the
origin, on the negative side of $z$. The printout shows that column,
with $0.0$ where $\cos 90°$ rounds to zero.

</details>

**2.** What does `rotate_y` at a half turn look like, and what does it
do to a point?

<details class="dl-answer"><summary>answer</summary>

$$\begin{bmatrix} -1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & -1 \end{bmatrix}$$

It flips the sign of $x$ and of $z$ and leaves $y$ alone. A half turn
puts everything on the opposite side, left for right and
front for back, at the same height. The printout has a `-0.0` in one
place, which is a very small negative number rounded to zero, and it
counts as the $0$ in the matrix.

```python
print(rounded(rotate_y(math.radians(180))))
```

</details>

**3.** What is `multiply(rotate_y(0.7), rotate_y(-0.7))`? Say what it
should be before you run it, and say why.

<details class="dl-answer"><summary>answer</summary>

The identity matrix, to within rounding. A turn by $0.7$ radians and
then by $-0.7$ radians is no turn at all. Every rotation can be undone
by the same rotation the other way. So the inverse of a rotation matrix
is easy to write down. It is the rotation matrix for the opposite
angle.

```python
print(rounded(multiply(rotate_y(0.7), rotate_y(-0.7))))
```

</details>

## A third axis

**4.** `rotate_y` leaves $y$ alone and `rotate_x` leaves $x$ alone. How
might you write `rotate_z(angle)`, which leaves $z$ alone and turns $x$
and $y$? Check that a quarter turn sends $(1, 0, 0)$ to $(0, 1, 0)$.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The row and column for $z$ are the ones that do nothing:
   $[0, 0, 1]$ across the bottom and down the right.
2. The 2D rotation matrix fills the top-left $2 \times 2$ corner.
3. Multiply by the column $[[1], [0], [0]]$ to test it.

**Think about:** which of the three rotation matrices looks most like
the 2D one, and why that one.

**Try this next:** does `rotate_z` at a half turn agree with
`rotate_y` at a half turn about what happens to $x$?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def rotate_z(angle):
    cos_angle, sin_angle = math.cos(angle), math.sin(angle)
    return [[cos_angle, -sin_angle, 0],
            [sin_angle, cos_angle, 0],
            [0, 0, 1]]

print(rounded(multiply(rotate_z(math.radians(90)), [[1], [0], [0]])))
```

That prints $[[0.0], [1.0], [0.0]]$. The point on the $x$ axis has
turned onto the $y$ axis. `rotate_z` is the 2D rotation matrix with
a $z$ row and column added, since a turn about $z$ is a turn in the
$x$–$y$ plane, which is the plane the 2D matrix always worked in. Both
half turns send $x$ to $-x$. They differ in which of the other two
axes they flip.

</details>

## Order

**5.** Is `multiply(rotate_x(a), rotate_y(b))` the same matrix as
`multiply(rotate_y(b), rotate_x(a))`? Test it with $a = 30°$ and
$b = 45°$, and then say in a sentence what each one does to a cube.

<details class="dl-answer"><summary>answer</summary>

They are different matrices.

```python
tilt = rotate_x(math.radians(30))
spin = rotate_y(math.radians(45))
print(rounded(multiply(tilt, spin)))
print(rounded(multiply(spin, tilt)))
```

The first spins the cube on its own vertical axis and then tips the
whole turntable towards you. The second tips the cube first, and then
spins the tipped cube about the vertical axis of the room, so its own
axis moves round in a circle. Matrix multiplication is not commutative,
and here the difference is something you can see.

</details>

## Shapes

**6.** `rotate_y(angle)` is 3×3, and the cube is 3 rows of 8. What
shape is `multiply(rotate_y(angle), cube)`?

```python exec
id: shapes-1
{{include: setup/cube.py}}

turned = multiply(rotate_y(math.radians(30)), cube)
print(len(turned), "rows of", len(turned[0]))
```

```predict
What will the cell print?

- 3 rows of 3
  - The rotation is 3×3.
- 3 rows of 8
  - The cube has 8 corners.
- 8 rows of 3
  - There are 8 points of 3 numbers each.
```

<details class="dl-answer"><summary>answer</summary>

3 rows of 8. A 3×3 times a 3×8 is a 3×8: the inner 3s match, and the
outer numbers give the shape. It has to be, because the answer is still
8 corners, each with an $x$, a $y$ and a $z$.

</details>

## A wireframe of your own

**7.** A house is a box with a roof. Make the box 2 wide, 1.5 tall and 2
deep, from $y = -1$ to $y = 0.5$, and put the ridge of the roof along
the middle, at $y = 1.25$. Can you write its corners and edges, and
draw it turned 30° and moved 7 units out?

```python exec
id: wireframe-1
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Draw it on paper first, and number the corners: 0 to 3 round the
   bottom, 4 to 7 round the top of the box, and 8 and 9 for the two
   ends of the ridge.
2. The box has 12 edges, like the cube. The roof adds 5: two lines up
   to each end of the ridge, and the ridge itself.
3. `draw_edges` uses the cube's `edges`, so write a `draw_shape` that
   takes its own list of edges.

**Think about:** how many corners and edges does your own shape have?
Can you count them before you write them?

</details>

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Yours may be different and work too. The house has
10 corners and 17 edges.

```python
house = [
    [-1, 1, 1, -1, -1, 1, 1, -1, 0, 0],
    [-1, -1, -1, -1, 0.5, 0.5, 0.5, 0.5, 1.25, 1.25],
    [-1, -1, 1, 1, -1, -1, 1, 1, -1, 1],
]
house_edges = [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4),
               (0, 4), (1, 5), (2, 6), (3, 7),
               (4, 8), (5, 8), (7, 9), (6, 9), (8, 9)]


def draw_shape(points, shape_edges):
    screen_xs, screen_ys = project(points)
    for start, end in shape_edges:
        plt.plot([screen_xs[start], screen_xs[end]],
                 [screen_ys[start], screen_ys[end]], color="C0")
    plt.gca().set_aspect("equal")


draw_shape(move(multiply(rotate_y(math.radians(30)), house), 0, 0, 7), house_edges)
```

Corners 8 and 9 are the ends of the ridge, at the front and the back.
Each joins the two top corners at its own end.

</details>

## From earlier

**8.** From *Inverse matrices: undoing a transformation*. What undoes
`rotate_y(angle)`? Check your answer with `multiply`.

<details class="dl-answer"><summary>answer</summary>

`rotate_y(-angle)`, the same turn the other way. It is also the
transpose of `rotate_y(angle)`: swapping rows and columns changes the
signs of the two sines and leaves the cosines alone. So
`multiply(rotate_y(-0.7), rotate_y(0.7))` is the identity, apart from
rounding, as in problem 3. A turn has determinant 1, so it never
flattens anything, and it can always be undone.

</details>
