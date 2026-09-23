---
title: "Inverse matrices: undoing a transformation"
year: "2026-2027"
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

# Inverse matrices: undoing a transformation

Look back at the gallery in
[Matrix transformations: what a matrix does to a picture](tutorial:what-a-matrix-does-to-a-picture).
Some of those matrices felt as if we could reverse them. We could
imagine sliding the sheared square back, or turning the rotated square
back the other way. Others did not feel reversible.

What decides whether a matrix can be undone? On this page we:

- measure how much a matrix changes the area of a shape
- meet the determinant, one number that answers the question
- build a function that undoes a matrix, when that is possible
- sort some matrices into ones that can be undone and ones that cannot

## Measuring the square

Here is a function that measures the area inside a shape, from its
corner points. It uses the *shoelace formula*. The shoelace formula
finds the area of a shape in three steps:

1. For each pair of neighbouring corners, cross-multiply their
   coordinates: $x_1 y_2 - x_2 y_1$.
2. Add up all of those results.
3. Halve the total.

```python exec
id: measuring-the-square-1
def polygon_area(points):
    xs, ys = points
    point_count = len(xs)
    total = 0
    for i in range(point_count):
        j = (i + 1) % point_count
        total += xs[i] * ys[j] - xs[j] * ys[i]
    return abs(total) / 2

square = [[0, 1, 1, 0], [0, 0, 1, 1]]
print("area of the original square:", polygon_area(square))
```

`j` is the corner after corner `i`. The `%` makes `j` go back to 0 after
the last corner, so the last corner is paired with the first one.

Now let's transform the square with `stretch = [[2, 0], [0, 1]]`, the
first matrix from the last page. What do you think the new area will
be? Run the cell to check.

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

The area doubled. Does that come from the numbers 2, 0, 0 and 1 in
`stretch`? If it does, which arithmetic on them gives 2?

Now try `shear = [[1, 1], [0, 1]]`. It changed the square's shape more
than any other matrix in the last page's gallery. Transform the square
with it, and measure the area. What do you expect?

```python exec
id: measuring-the-square-3
```

### Your turn

For a 2×2 matrix $\begin{bmatrix} a & b \\ c & d \end{bmatrix}$, the
*determinant* is the number $ad - bc$.

1. Work out $ad - bc$ by hand for `stretch`.
2. Work out $ad - bc$ by hand for `shear`.
3. Compare each one with the area you measured.

```python exec
id: measuring-the-square-4
hint: For stretch, a=2, b=0, c=0, d=1. For shear, a=1, b=1, c=0, d=1.
```

What did you find? The determinant of a matrix is the factor by which
the matrix scales area. The determinant can also be negative. A negative
determinant means the matrix also flips the shape over, like a mirror.

`shear` looked like the biggest change in the gallery. Yet it did not
change the area at all. The picture alone does not make that clear, but
the determinant says it straight away.

## When the square collapses

What happens to the square when the determinant is zero? The
determinant of the matrix below is $2(2) - 4(1) = 0$. Run the cell and
look at the points and the area.

```python exec
id: when-the-square-collapses-1
singular = [[2, 4], [1, 2]]
collapsed = multiply(singular, square)
print(collapsed)
print("area:", polygon_area(collapsed))
```

All four points lie on the same straight line through the origin. A
matrix with determinant zero always gives an area of zero. The result is
not a smaller square. It is a shape with no width at all. A matrix with
determinant zero is called *singular*.

### Your turn

Plot `square` and `collapsed` on the same axes, to see the flattening
for yourself.

```python exec
id: when-the-square-collapses-2
hint: Two calls to plt.plot, one for each set of points — the same pattern as the last tutorial's gallery.
import matplotlib.pyplot as plt
```

## Undoing a transformation

The *inverse* of a matrix $A$ is the matrix that undoes $A$. It is
written $A^{-1}$.

If a matrix scales area by some factor, its inverse should scale area by
1 divided by that factor. For a 2×2 matrix, there is a formula for the
inverse:

$$A^{-1} = \frac{1}{\det(A)} \begin{bmatrix} d & -b \\ -c & a \end{bmatrix}$$

Here $\det(A)$ is the determinant of $A$. Look at where it sits: under
the fraction line. What happens when $\det(A) = 0$? The formula would
divide by zero.

The algebra says the same thing that the collapsed square showed in a
picture. A matrix with determinant zero has no inverse. Once a shape has
been flattened, there is no way to get back the width it lost.

### Your turn

1. How might you write `inverse(M)` for a 2×2 matrix, with the formula
   above? Write it in the first cell.
2. The second cell applies your inverse to `transformed`, from the
   section on measuring the square. Do you get `square` back?

```python exec
id: undoing-a-transformation-1
hint: det = M[0][0]*M[1][1] - M[0][1]*M[1][0], then build the swapped-and-negated matrix, then scale by 1/det.
# Your inverse(M)
```

```python exec
id: undoing-a-transformation-2
check(multiply(inverse(stretch), transformed), square)
```

There is also a way to check an inverse without transforming any shape.
A matrix times its inverse, $AA^{-1}$, should give the identity matrix.

```python exec
id: undoing-a-transformation-3
check(multiply(stretch, inverse(stretch)), [[1, 0], [0, 1]])
```

## Which ones can be undone?

Here are five matrices. For each one:

1. Work out the determinant first.
2. Predict whether the matrix has an inverse.
3. Then check your prediction. You can try `inverse` on the matrix, or
   you can transform `square` with it and look at the picture.

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

1. From the determinants alone, which of the five can be undone?
2. Pick one that you predicted is singular.
3. Transform `square` with it. Does the picture collapse?

```python exec
id: which-ones-can-be-undone-2
```

## Reflection

One number, worked out from four entries, answers a question that a
picture can only illustrate: does this matrix lose information?

$ad - bc$ is not a formula chosen to make the examples come out neatly.
It is the factor by which the matrix scales area. Follow the reasoning
one step at a time:

1. A factor of zero means that the area disappears.
2. When the area disappears, two different starting shapes can end up
   as the same flattened result.
3. So from the flattened result, there is no way to know which shape
   we started with. There is no way back.

Did any of the five matrices surprise you? Was there one whose numbers
made you expect an inverse, but it had none? Or the other way round?

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
