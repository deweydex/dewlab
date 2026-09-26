---
title: "Matrix transformations: what a matrix does to a picture"
year: "2026-2027"
version: 2026.09.26.1
covers:
  where-do-the-corners-go:
    covers: [CMPS-LO4]
    touches: [MIT-3.2]
  a-small-gallery:
    covers: [CMPS-LO4]
  guess-the-matrix:
    covers: [CMPS-LO4]
---

# Matrix transformations: what a matrix does to a picture

On the last two pages, a matrix was a grid of numbers. We added grids,
scaled them, and multiplied one grid by another.

A 2×2 matrix has a second use, too. We can read it as an instruction
that moves every point in a picture to a new place. On this page we
watch that happen.

On this page we:

- use a matrix to move the four corners of a square
- see five effects a matrix can have on a picture
- read a matrix's columns to know where it sends each point
- work out a hidden matrix from the picture it made

## Where do the corners go?

Here is a square, drawn as four corner points, before anything has been
done to it.

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

The first line imports `matplotlib`, the library we use to draw. The
function `plot_shape` draws a line from corner to corner. It adds the
first corner again at the end, so that the shape is closed.

`square` holds the four corners in two rows. The first row holds the
$x$-coordinates, and the second row holds the $y$-coordinates. So each
*column* of `square` is one point.

We chose this layout on purpose. With it, one multiplication applies a
2×2 matrix to all four corners at once. We use the `multiply` you built
on the last page,
[Matrix multiplication: rows times columns](tutorial:multiplying-grids).

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

1. How would you plot `square` and `transformed` on the same axes, in
   two different colours?
2. Look at the picture. What did `stretch` do to the square?

```python exec
id: where-do-the-corners-go-3
hint: Two calls to plot_shape, one for each set of points, before the plot appears.
```

## A small gallery

Each matrix below has one effect on the square. Before you run each
cell, try to predict what it will do.

Five words may help you: stretch, squash, rotate, shear and reflect. You
do not have to use them until after you have seen the pictures.

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

A matrix used in this way is a *transformation matrix*. A transformation
matrix is a matrix that we read as an instruction for moving every point
of a picture. Here are the five effects we have seen:

| Matrix | Effect on the square |
|---|---|
| `stretch = [[2, 0], [0, 1]]` | stretch: twice as wide, same height |
| `squash = [[1, 0], [0, 0.5]]` | squash: same width, half as tall |
| `rotate90 = [[0, -1], [1, 0]]` | rotate: turned 90° anticlockwise |
| `shear = [[1, 1], [0, 1]]` | shear: bottom edge stays, top edge slides sideways |
| `reflect_x = [[1, 0], [0, -1]]` | reflect: flipped upside down, across the $x$-axis |

Now look back at `rotate90`. You met the same matrix in problem 7 of the
practice page for
[Matrix multiplication: rows times columns](tutorial:multiplying-grids).
There you worked out that it sends $(1,0)$ to $(0,1)$, and $(0,1)$ to
$(-1,0)$.

Can you see those two results in `rotate90`? They are its two
*columns*. This is true for every 2×2 matrix:

- the first column is where $(1,0)$ lands
- the second column is where $(0,1)$ lands

Those two columns are enough to tell you what the matrix does to every
other point.

### Your turn

1. Read the columns of `shear`. They say that $(1,0)$ goes to $(1,0)$
   and $(0,1)$ goes to $(1,1)$.
2. Does that match the picture from the shear cell? Does the bottom edge
   of the square stay where it is? Does the top edge move?

```python exec
id: a-small-gallery-5
```

## Guess the matrix

Here is a square that some 2×2 matrix has already transformed. The
matrix itself is hidden.

```python exec
id: guess-the-matrix-1
mystery = [[0.0, 1.0, 1.5, 0.5], [0.0, 0.0, 1.0, 1.0]]
plot_shape(square, "C0", "original")
plot_shape(mystery, "C2", "mystery")
plt.gca().set_aspect("equal")
plt.legend()
```

The bottom edge has not moved at all. The top edge has slid sideways.
What matrix would do that?

Remember that the columns of your answer are where $(1,0)$ and $(0,1)$
land. The bottom-left corner stays at $(0,0)$, but that is not a clue on
its own. None of these matrices ever moves $(0,0)$.

1. Write your guess in the first cell, as `your_guess`.
2. Run the second cell to check it.

```python exec
id: guess-the-matrix-2
hint: (1, 0) is on the unmoved bottom edge — where does the picture say it goes? (0, 1) is a top corner — where does the picture say that one lands?
# Call it your_guess, as a 2x2 matrix
your_guess = [[1, 0], [0, 1]]
```

```inputs
multiply(your_guess, square)
```

```solution
your_guess = [[1, 0.5], [0, 1]]
---
A shear: each point moves right by half its height, so the top of the
square slides over and the bottom stays where it was.
```

```python exec
id: guess-the-matrix-3
print(multiply(your_guess, square))
print(mystery)
```

## Reflection

We can read the same few numbers in two ways. They are a grid that we
can add and multiply. They are also an instruction for moving every
point in a picture. Neither reading is more correct than the other. They
are the same object, and the useful reading depends on what you want to
do with it.

Which of the five words (stretch, squash, rotate, shear, reflect)
matched your prediction before you saw the picture? Which one surprised
you?

This page leaves a question open: can every matrix be undone? The next
page, [Inverse matrices: undoing a transformation](tutorial:undoing-it),
starts from that question.

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
