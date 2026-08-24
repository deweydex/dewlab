---
title: "Undoing It"
slug: undoing-it
module: computational-methods
module_title: "Computational Methods"
year: "2026-2027"
series: matrices
version: 2026.08.24.1
covers:
  measuring-the-square:
    touches: [CMPS-LO4]
  when-the-square-collapses:
    touches: [CMPS-LO4]
  undoing-a-transformation:
    covers: [CMPS-LO4]
  which-ones-can-be-undone:
    covers: [CMPS-LO4]
---

# Undoing It

Some of the matrices in the last tutorial's gallery felt reversible — you
could imagine sliding the sheared square back, or rotating it back the other
way. Others did not. This tutorial asks what actually decides whether a
matrix can be undone, and builds the tool that undoes it when it can.

## Measuring the Square

Here is a function that measures the area enclosed by a shape given as
corner points, using the *shoelace formula* — cross-multiply consecutive
corners, add them up, and halve the result.

```python exec
id: measuring-the-square-1
def polygon_area(points):
    xs, ys = points
    n = len(xs)
    total = 0
    for i in range(n):
        j = (i + 1) % n
        total += xs[i] * ys[j] - xs[j] * ys[i]
    return abs(total) / 2

square = [[0, 1, 1, 0], [0, 0, 1, 1]]
print("area of the original square:", polygon_area(square))
```

Now transform it with `stretch = [[2, 0], [0, 1]]`, the very first matrix
from the last tutorial, and measure the result.

```python exec
id: measuring-the-square-2
def dot(a, b):
    return sum(x * y for x, y in zip(a, b))

def transpose(m):
    rows, cols = len(m), len(m[0])
    return [[m[r][c] for r in range(rows)] for c in range(cols)]

def multiply(a, b):
    bt = transpose(b)
    return [[dot(row, col) for col in bt] for row in a]

stretch = [[2, 0], [0, 1]]
transformed = multiply(stretch, square)
print("area after stretch:", polygon_area(transformed))
```

The area doubled. Is that because of the numbers 2 and 0 in `stretch`, and if
so, which arithmetic on them gives 2? Try `shear = [[1, 1], [0, 1]]` — the
one that looked most dramatically different in the last tutorial's
gallery — and measure its area too.

```python exec
id: measuring-the-square-3
```

### Your turn

For a 2×2 matrix $\begin{bmatrix} a & b \\ c & d \end{bmatrix}$, the quantity
$ad - bc$ is called the *determinant*. Compute $ad - bc$ by hand for `stretch`
and for `shear`, and compare each to the area you measured for it.

```python exec
id: measuring-the-square-4
hint: For stretch, a=2, b=0, c=0, d=1. For shear, a=1, b=1, c=0, d=1.
```

The determinant of a matrix is exactly the factor by which it scales area.
`shear` looked like the most extreme transformation in the gallery, and it
changed the area not at all — a fact the picture alone does not make obvious,
and the determinant states outright.

## When the Square Collapses

```python exec
id: when-the-square-collapses-1
singular = [[2, 4], [1, 2]]
collapsed = multiply(singular, square)
print(collapsed)
print("area:", polygon_area(collapsed))
```

Every one of those four points lies on the same straight line through the
origin — plot them and see. The determinant of `singular` is
$2(2) - 4(1) = 0$, and an area of zero is what a matrix with determinant zero
always produces: not a smaller square, but a shape with no width at all.

### Your turn

Plot `square` and `collapsed` on the same axes to see the flattening
directly.

```python exec
id: when-the-square-collapses-2
hint: Two calls to plt.plot, one for each set of points — the same pattern as the last tutorial's gallery.
import matplotlib.pyplot as plt
```

## Undoing a Transformation

If a matrix scales area by some factor, undoing it ought to scale area by
the reciprocal of that factor. For a 2×2 matrix, there is a direct formula:

$$A^{-1} = \frac{1}{\det(A)} \begin{bmatrix} d & -b \\ -c & a \end{bmatrix}$$

Notice $\det(A)$ sits in the denominator. If $\det(A) = 0$, this formula asks
you to divide by zero — which is the algebra saying the same thing the
collapsed square just showed as a picture: a matrix with determinant zero has
no inverse, because there is no way to recover a flattened shape's missing
dimension.

### Your turn

Write `inverse(M)` for a 2×2 matrix, following the formula above. Apply it to
`transformed` from the `measuring-the-square` section, and check that you get
`square` back.

```python exec
id: undoing-a-transformation-1
hint: det = M[0][0]*M[1][1] - M[0][1]*M[1][0], then build the swapped-and-negated matrix, then scale by 1/det.
# Your inverse(M)
```

```python exec
id: undoing-a-transformation-2
check(multiply(inverse(stretch), transformed), square)
```

`AA^{-1}` should give back the identity matrix — a direct way to check an
inverse without needing a square to transform at all.

```python exec
id: undoing-a-transformation-3
check(multiply(stretch, inverse(stretch)), [[1, 0], [0, 1]])
```

## Which Ones Can Be Undone

Five matrices. For each, compute the determinant first and predict whether it
has an inverse — then confirm by trying `inverse` on it, or by transforming
`square` and looking at the picture.

```python exec
id: which-ones-can-be-undone-1
candidates = {
    "M1": [[2, 1], [1, 1]],
    "M2": [[1, 2], [2, 4]],
    "M3": [[3, 0], [0, 0]],
    "M4": [[0, -1], [1, 0]],
    "M5": [[2, 4], [1, 2]],
}
for name, M in candidates.items():
    d = M[0][0] * M[1][1] - M[0][1] * M[1][0]
    print(name, "determinant:", d)
```

### Your turn

Which of the five can be undone, on the strength of the determinants alone?
Pick one you predicted is singular and confirm by trying to transform
`square` with it and looking at whether the picture collapses.

```python exec
id: which-ones-can-be-undone-2
```

## Reflection

One number, computed from four entries, and it answers a question a picture
can only illustrate: whether a matrix loses information. `ad - bc` is not an
arbitrary formula picked to make examples come out neatly — it is the area
scale factor, and a factor of zero means area disappears, which means two
different starting shapes could land on the same flattened result, which
means there is no way back.

Did any of the five candidates surprise you — one that looked like it should
be invertible from its numbers, but was not, or the reverse?

## Where to Read More

Grant Sanderson (3Blue1Brown) (2016). *Essence of Linear Algebra, Chapter 6:
The Determinant.* <https://www.youtube.com/watch?v=Ip3X9LOh2dk>. The area
argument in this tutorial, animated, and extended to what happens in three
dimensions.

Grant Sanderson (3Blue1Brown) (2016). *Essence of Linear Algebra, Chapter 7:
Inverse Matrices, Column Space and Null Space.*
<https://www.youtube.com/watch?v=uQhTuRlWMxw>. Why a determinant of zero is
exactly the condition under which an inverse cannot exist, argued
geometrically rather than from the formula.

Strang, G. (2016). *Introduction to Linear Algebra* (5th ed.).
Wellesley-Cambridge Press. Chapter 5 covers determinants properly, including
the $3\times3$ and general-$n$ cases this tutorial deliberately leaves out.
