---
title: "What a Matrix Does to a Picture — Practice"
slug: what-a-matrix-does-to-a-picture-practice
practice_for: what-a-matrix-does-to-a-picture
module: computational-methods
module_title: "Computational Methods"
year: "2026-2027"
series: matrices
version: 2026.08.24.1
---

# What a Matrix Does to a Picture — Practice

Predict the picture from the matrix, or the matrix from the picture, before
you run anything. That prediction is the actual practice — the plot only
tells you whether you were right.

## Reading Columns

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
$(0, 1)$? What would you call what it does to the square?

<details class="dl-answer"><summary>answer</summary>

$(1,0) \to (3,0)$ and $(0,1) \to (0,3)$ — read straight off the two columns.

Both directions grow by the same factor, so this is a uniform scaling — the
square becomes a bigger square, three times the size in each direction, not
a rectangle.

</details>

**2.** Where does $M = \begin{bmatrix} -1 & 0 \\ 0 & 1 \end{bmatrix}$ send
$(1, 0)$ and $(0, 1)$? Check it against the picture.

<details class="dl-answer"><summary>answer</summary>

$(1,0) \to (-1,0)$, and $(0,1) \to (0,1)$ — unchanged.

```python
result = multiply([[-1, 0], [0, 1]], square)
```

Only the $x$-coordinates flip sign; every $y$-coordinate stays exactly where
it was. That is a reflection across the $y$-axis — the square's mirror
image, folded left-to-right rather than upside down.

</details>

## From Description to Matrix

**3.** What 2×2 matrix rotates every point 180°?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. A 180° turn sends $(1, 0)$ to its exact opposite. What point is that?
2. It sends $(0, 1)$ to its exact opposite too. What point is that?
3. Those two answers are the two columns of your matrix, in order.
4. Write the matrix and check it against the square: does every corner end
   up diagonally opposite where it started?

**Think about:** a 180° rotation is the same as scaling by $-1$ in every
direction at once. Does your matrix agree with that?

**Try this next:** what matrix rotates by 180° and *then* reflects across the
$x$-axis — is that the same as just reflecting across the $y$-axis?

</details>

<details class="dl-answer"><summary>answer</summary>

$\begin{bmatrix} -1 & 0 \\ 0 & -1 \end{bmatrix}$

$(1,0) \to (-1,0)$ and $(0,1) \to (0,-1)$ — both basis points land on their
own opposite, which is exactly what turning something upside down and
backwards means. Applied to the square, every corner ends up diagonally
across the origin from where it started.

</details>

**4.** What matrix swaps the $x$ and $y$ coordinate of every point — sends
$(x, y)$ to $(y, x)$?

<details class="dl-answer"><summary>answer</summary>

$\begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}$

$(1,0) \to (0,1)$ and $(0,1) \to (1,0)$ — the two basis points trade places,
which is exactly what "swap the coordinates" has to mean for every other
point too. This is a reflection across the diagonal line $y = x$.

</details>

**5.** A square, already transformed:

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

What matrix produced this, and is it the same one you found in problem 4?

<details class="dl-answer"><summary>answer</summary>

Yes — $\begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}$ again. The square looks
reflected across the diagonal, which is exactly the coordinate-swap from
problem 4, and the corner coordinates confirm it: $(1,0)$ and $(0,1)$ have
traded places while $(0,0)$ and $(1,1)$ — both sitting on the line $y=x$ —
stayed put.

</details>

## Gallery, Continued

```python exec
id: gallery-1
def show_transform(M, name):
    result = multiply(M, square)
    plot_shape(square, "C0", "original")
    plot_shape(result, "C1", name)
    plt.gca().set_aspect("equal")
    plt.legend()
```

**6.** Predict, then check: what does
$M = \begin{bmatrix} 1 & 0 \\ 0.5 & 1 \end{bmatrix}$ do to the square?

<details class="dl-answer"><summary>answer</summary>

$(1,0) \to (1, 0.5)$ and $(0,1) \to (0,1)$ — the left edge stays put and the
right edge tilts upward. This is a shear, but along the *other* axis from the
one in the tutorial: there, the top and bottom edges slid sideways; here,
the left and right edges tilt, because it is the *second* row that carries
the extra term this time.

```python
show_transform([[1, 0], [0.5, 1]], "sheared")
```

</details>

**7.** Is there a matrix that sends the square to a single point — every
corner landing on $(0, 0)$?

<details class="dl-answer"><summary>answer</summary>

Yes: $\begin{bmatrix} 0 & 0 \\ 0 & 0 \end{bmatrix}$, the zero matrix.

Both columns are $(0,0)$, so both $(1,0)$ and $(0,1)$ collapse to the origin
— and everything else made of them collapses along with them. This is the
most extreme version of a matrix that cannot be undone: not merely flattened
to a line, but flattened all the way to a point, which the next tutorial's
determinant will mark as exactly as broken as the line case.

</details>

## Thinking About It

**8.** Two different matrices both send $(1, 0)$ to $(2, 0)$. Are they
necessarily the same matrix?

<details class="dl-answer"><summary>answer</summary>

No. $(1,0)$ only pins down the *first* column of the matrix — the second
column, where $(0,1)$ lands, is completely free.

$\begin{bmatrix} 2 & 0 \\ 0 & 1 \end{bmatrix}$ and
$\begin{bmatrix} 2 & 5 \\ 0 & 3 \end{bmatrix}$ both send $(1,0)$ to $(2,0)$
and disagree everywhere else. Reading a matrix off a picture, as in problems
3 through 5, only works because those problems gave you *both* columns'
worth of information, not one.

</details>

**9.** Every matrix in this practice page sends $(0, 0)$ to $(0, 0)$. Why is
that not a coincidence — and what kind of transformation would move the
origin?

<details class="dl-answer"><summary>answer</summary>

Multiplying any matrix by the zero vector gives the zero vector — every term
in every dot product has a zero in it, so the whole sum is zero. That is true
for every matrix, not a property of the ones chosen here.

A transformation that *does* move the origin — sliding the whole square
sideways without stretching or rotating it, a *translation* — cannot be
written as a 2×2 matrix multiplication at all. It needs the vector addition
from *A Grid of Numbers* as well: $\text{new point} = M\mathbf{p} + \mathbf{t}$,
the same shape as the neural-network layer from the last tutorial's practice.

</details>
