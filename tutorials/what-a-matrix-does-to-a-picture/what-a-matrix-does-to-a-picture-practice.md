---
title: "Matrix transformations: what a matrix does to a picture — Practice"
practice_for: what-a-matrix-does-to-a-picture
year: "2026-2027"
version: 2026.08.24.1
---

# Matrix transformations: what a matrix does to a picture — Practice

Before you run anything, predict the picture from the matrix, or the
matrix from the picture. The prediction is the real practice. The plot
only shows whether your prediction matched.

## Reading columns

```python exec
id: reading-1
def dot(a, b):
    if len(a) != len(b):
        raise ValueError("lengths do not match")
    return sum(x * y for x, y in zip(a, b))


def transpose(m):
    rows, cols = len(m), len(m[0])
    return [[m[r][c] for r in range(rows)] for c in range(cols)]


def multiply(a, b):
    bt = transpose(b)
    return [[dot(row, col) for col in bt] for row in a]


square = [[0, 1, 1, 0], [0, 0, 1, 1]]
```

**1.** Without running anything, where does
$M = \begin{bmatrix} 3 & 0 \\ 0 & 3 \end{bmatrix}$ send $(1, 0)$ and
$(0, 1)$? What would you call its effect on the square?

<details class="dl-answer"><summary>answer</summary>

$(1,0) \to (3,0)$ and $(0,1) \to (0,3)$. We read these straight from the
two columns.

Both directions grow by the same amount, so this is a *uniform scaling*.
The square becomes a bigger square, three times as wide and three times
as tall. It does not become a rectangle.

</details>

**2.** Where does $M = \begin{bmatrix} -1 & 0 \\ 0 & 1 \end{bmatrix}$ send
$(1, 0)$ and $(0, 1)$? Check it against the picture.

<details class="dl-answer"><summary>answer</summary>

$(1,0) \to (-1,0)$, and $(0,1) \to (0,1)$, which does not change.

```python
result = multiply([[-1, 0], [0, 1]], square)
```

Only the $x$-coordinates change sign. Every $y$-coordinate stays exactly
where it was. This is a reflection across the $y$-axis. The square is
flipped from left to right, not upside down.

</details>

## From description to matrix

**3.** What 2×2 matrix rotates every point 180°?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. A 180° turn sends $(1, 0)$ to the point exactly opposite it. What
   point is that?
2. It sends $(0, 1)$ to the point exactly opposite it too. What point is
   that?
3. Those two answers are the two columns of your matrix, in order.
4. Write the matrix and check it against the square. Does every corner
   land on the other side of the origin from where it started?

**Think about:** a 180° rotation is the same as scaling by $-1$ in every
direction at once. Does your matrix agree with that?

**Try this next:** what matrix rotates by 180° and then reflects across
the $x$-axis? Is that the same as reflecting across the $y$-axis?

</details>

<details class="dl-answer"><summary>answer</summary>

$\begin{bmatrix} -1 & 0 \\ 0 & -1 \end{bmatrix}$

$(1,0) \to (-1,0)$ and $(0,1) \to (0,-1)$. Both points land exactly
opposite where they started. The square turns upside down and flips
from left to right. Every corner lands on the
other side of the origin, along a line through $(0,0)$.

</details>

**4.** What matrix swaps the $x$ and $y$ coordinates of every point? It
sends $(x, y)$ to $(y, x)$.

<details class="dl-answer"><summary>answer</summary>

$\begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}$

$(1,0) \to (0,1)$ and $(0,1) \to (1,0)$. The two points change places.
That is what "swap the coordinates" means for every other point too.
This is a reflection across the diagonal line $y = x$.

</details>

**5.** Here is a square that a matrix has already transformed:

```python exec
id: mystery-1
import matplotlib.pyplot as plt

mystery = [[0, 0, 1, 1], [0, 1, 1, 0]]

def plot_shape(pts, color, label):
    plt.plot(pts[0] + [pts[0][0]], pts[1] + [pts[1][0]], color=color, marker="o", label=label)

plot_shape(square, "C0", "original")
plot_shape(mystery, "C2", "mystery")
plt.gca().set_aspect("equal")
plt.legend()
```

What matrix produced this? Is it the same one you found in problem 4?
Look at the lists of corners, `square` and `mystery`, as well as the
picture.

<details class="dl-answer"><summary>answer</summary>

Yes, it is $\begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}$ again, the
coordinate swap from problem 4.

The picture alone cannot tell you this. The square reflected across the
line $y = x$ lands exactly on itself, so the mystery shape covers the
original square. The corner lists show what happened. The second corner
of `square` is $(1,0)$, and the second corner of `mystery` is $(0,1)$.
The fourth corner was $(0,1)$ and is now $(1,0)$. So $(1,0)$ and $(0,1)$
have changed places. $(0,0)$ and $(1,1)$ both sit on the line $y=x$, so
they stay where they are.

</details>

## Gallery, continued

```python exec
id: gallery-1
def show_transform(M, name):
    result = multiply(M, square)
    plot_shape(square, "C0", "original")
    plot_shape(result, "C1", name)
    plt.gca().set_aspect("equal")
    plt.legend()
```

**6.** What does $M = \begin{bmatrix} 1 & 0 \\ 0.5 & 1 \end{bmatrix}$ do to
the square? Predict first, then check.

<details class="dl-answer"><summary>answer</summary>

$(1,0) \to (1, 0.5)$ and $(0,1) \to (0,1)$. The left edge stays where it
is, and the right edge slides upward by 0.5. So the bottom and top edges
tilt.

This is a shear, along the other axis from the one in the tutorial.
There, the bottom edge stayed where it was and the top edge slid
sideways, so the left and right edges tilted. Here, the extra number is
in the second row, so the $y$-coordinates change, not the
$x$-coordinates.

```python
show_transform([[1, 0], [0.5, 1]], "sheared")
```

</details>

**7.** Is there a matrix that sends the square to a single point, with
every corner landing on $(0, 0)$?

<details class="dl-answer"><summary>answer</summary>

Yes: $\begin{bmatrix} 0 & 0 \\ 0 & 0 \end{bmatrix}$, the *zero matrix*.

Both columns are $(0,0)$, so both $(1,0)$ and $(0,1)$ land on the
origin. Every other point is built from those two, so every other point
lands there too.

This is the most extreme matrix that cannot be undone. Some matrices
flatten a picture onto a line. This one flattens it all the way to a
point. The next page,
[Inverse matrices: undoing a transformation](tutorial:undoing-it),
introduces the determinant. The determinant marks this case as exactly
as impossible to undo as the line case.

</details>

## Thinking about it

**8.** Two matrices both send $(1, 0)$ to $(2, 0)$. Must they be the same
matrix?

<details class="dl-answer"><summary>answer</summary>

No. Where $(1,0)$ lands decides only the first column of the matrix. The
second column, where $(0,1)$ lands, can be anything.

$\begin{bmatrix} 2 & 0 \\ 0 & 1 \end{bmatrix}$ and
$\begin{bmatrix} 2 & 5 \\ 0 & 3 \end{bmatrix}$ both send $(1,0)$ to
$(2,0)$, and they are different everywhere else. In problems 3 to 5, we
could read a matrix from a picture or a description only because we
knew where both points went, not only one.

</details>

**9.** Every matrix on this practice page sends $(0, 0)$ to $(0, 0)$. Why
is that not a coincidence? What kind of transformation would move the
origin?

<details class="dl-answer"><summary>answer</summary>

Any matrix times the zero vector $(0, 0)$ gives the zero vector. Every
term in every dot product has a zero in it, so every sum is zero. This is
true for every matrix, not only the ones chosen here.

A *translation* slides the whole square to a new place, without
stretching or turning it. A translation does move the origin. So no 2×2
matrix multiplication can do it. It also needs an addition, like the one
in
[Matrices: adding, scaling and transposing a grid of numbers](tutorial:grid-of-numbers):
$\text{new point} = M\mathbf{p} + \mathbf{t}$. This has the same form as
the neural-network layer in problem 5 of the practice page for
[Matrix multiplication: rows times columns](tutorial:multiplying-grids).

</details>
