---
title: "What a Matrix Does to a Picture"
slug: what-a-matrix-does-to-a-picture
module: computational-methods
module_title: "Computational Methods"
year: "2026-2027"
series: matrices
version: 2026.08.24.1
covers:
  where-do-the-corners-go:
    covers: [CMPS-LO4]
    touches: [MIT-3.2]
  a-small-gallery:
    covers: [CMPS-LO4]
  guess-the-matrix:
    covers: [CMPS-LO4]
---

# What a Matrix Does to a Picture

Every matrix in the last two tutorials sat still on the page — a grid of
numbers you added, scaled, or multiplied by another grid. A 2×2 matrix has a
second life that has nothing to do with any of that: it can be read as an
instruction for moving every point in a picture somewhere else. This
tutorial is about watching that happen.

## Where Do the Corners Go?

A square, drawn as four corner points, before anything is done to it:

```python exec
id: where-do-the-corners-go-1
import matplotlib.pyplot as plt

def plot_shape(points, color="C0", label=None):
    xs = points[0] + [points[0][0]]
    ys = points[1] + [points[1][0]]
    plt.plot(xs, ys, color=color, marker="o", label=label)

xs = [0, 1, 1, 0]
ys = [0, 0, 1, 1]
square = [xs, ys]

plot_shape(square, label="original")
plt.axhline(0, color="grey", linewidth=0.5)
plt.axvline(0, color="grey", linewidth=0.5)
plt.gca().set_aspect("equal")
plt.legend()
```

`square` holds the four corners as two rows — one row of $x$-coordinates, one
row of $y$-coordinates — so each *column* is one point. That is a deliberate
choice: it means a 2×2 matrix can be applied to all four corners in a single
multiplication, using the `multiply` you built in the last tutorial.

```python exec
id: where-do-the-corners-go-2
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

stretch = [[2, 0], [0, 1]]
transformed = multiply(stretch, square)
print(transformed)
```

### Your turn

Plot `square` and `transformed` on the same axes, in two different colours.
What did `stretch` actually do to the picture?

```python exec
id: where-do-the-corners-go-3
hint: Two calls to plot_shape, one for each set of points, before the plot appears.
```

## A Small Gallery

One matrix, one effect. Predict what each of these will do to the square
*before* you run it — stretch, squash, rotate, shear, and reflect are the
five words you are looking for, though nothing forces you to use them until
after you have seen the picture.

```python exec
id: a-small-gallery-1
squash = [[1, 0], [0, 0.5]]
result = multiply(squash, square)

plot_shape(square, "C0", "original")
plot_shape(result, "C1", "transformed")
plt.gca().set_aspect("equal")
plt.legend()
```

```python exec
id: a-small-gallery-2
rotate90 = [[0, -1], [1, 0]]
result = multiply(rotate90, square)

plot_shape(square, "C0", "original")
plot_shape(result, "C1", "transformed")
plt.gca().set_aspect("equal")
plt.legend()
```

```python exec
id: a-small-gallery-3
shear = [[1, 1], [0, 1]]
result = multiply(shear, square)

plot_shape(square, "C0", "original")
plot_shape(result, "C1", "transformed")
plt.gca().set_aspect("equal")
plt.legend()
```

```python exec
id: a-small-gallery-4
reflect_x = [[1, 0], [0, -1]]
result = multiply(reflect_x, square)

plot_shape(square, "C0", "original")
plot_shape(result, "C1", "transformed")
plt.gca().set_aspect("equal")
plt.legend()
```

Now look back at `rotate90` — the same matrix from the end of *Multiplying
Grids*, where you worked out that it sends $(1,0)$ to $(0,1)$ and $(0,1)$ to
$(-1,0)$. Those two results are the two *columns* of `rotate90`. That is not
a coincidence: for any 2×2 matrix, the first column is where $(1,0)$ lands,
and the second column is where $(0,1)$ lands, and that alone is enough to
tell you what the matrix does to every other point.

### Your turn

Look at `shear` above and read its columns directly: $(1,0) \to (1,0)$,
$(0,1) \to (1,1)$. Does that match the picture the shear cell drew — does the
bottom edge of the square stay put, and does the top edge shift?

```python exec
id: a-small-gallery-5
```

## Guess the Matrix

Here is a square that has already been transformed by some 2×2 matrix. The
matrix itself is not shown.

```python exec
id: guess-the-matrix-1
mystery = [[0.0, 1.0, 1.5, 0.5], [0.0, 0.0, 1.0, 1.0]]
plot_shape(square, "C0", "original")
plot_shape(mystery, "C2", "mystery")
plt.gca().set_aspect("equal")
plt.legend()
```

The bottom edge has not moved at all, and the top edge has slid sideways.
What matrix would do that? Remember that the columns of your answer should be
where $(1,0)$ and $(0,1)$ land — and $(0,0)$ never moves under any of these
matrices, so the bottom-left corner staying at the origin is not a clue by
itself.

```python exec
id: guess-the-matrix-2
hint: (1, 0) is on the unmoved bottom edge — where does the picture say it goes? (0, 1) is a top corner — where does the picture say that one lands?
# Call it your_guess, as a 2x2 matrix
your_guess = [[1, 0], [0, 1]]
```

```python exec
id: guess-the-matrix-3
check(multiply(your_guess, square), mystery)
```

## Reflection

The same handful of numbers, read two ways: as a grid you can add and
multiply, and as an instruction for moving every point in a picture. Neither
reading is more "real" than the other — they are the same object, and which
one is useful depends entirely on what you are trying to do with it.

Which of the five words — stretch, squash, rotate, shear, reflect — matched
your prediction before you saw the picture, and which one surprised you? The
next tutorial asks what it takes to undo one of these, and it starts from a
question this one leaves open: is every matrix undoable?

## Where to Read More

Grant Sanderson (3Blue1Brown) (2016). *Essence of Linear Algebra, Chapter 3:
Linear Transformations and Matrices.*
<https://www.youtube.com/watch?v=kYB8IZa5AuE>. The geometric picture behind
everything in this tutorial, animated far better than a static plot can
manage.

Grant Sanderson (3Blue1Brown) (2016). *Essence of Linear Algebra, Chapter 4:
Matrix Multiplication as Composition.*
<https://www.youtube.com/watch?v=XkY2DOUCWMU>. What happens when you apply
two of these transformations one after another — a natural next question
once the gallery in this tutorial stops feeling new.

Hughes, J. F., van Dam, A., McGuire, M., Sklar, D. F., Foley, J. D., Feiner,
S. K. and Akeley, K. (2013). *Computer Graphics: Principles and Practice*
(3rd ed.). Addison-Wesley. Chapter 6 covers exactly these transformation
matrices, as they are actually used to move things on a screen.
