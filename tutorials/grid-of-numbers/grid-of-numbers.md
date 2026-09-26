---
title: "Matrices: adding, scaling and transposing a grid of numbers"
year: "2026-2027"
version: 2026.09.26.2
worlds:
  pixel-art: Pictures made of small squares, the way a screen draws them.
  photos: Photographs, and the filters that change them.
datasets: [grace-hopper]
covers:
  a-grid-that-draws-a-picture:
    touches: [CMPS-LO1, MIT-6.3]
  darker-scaling-a-grid:
    touches: [CMPS-LO4]
  overlay-adding-two-grids:
    touches: [CMPS-LO4]
  corner-to-corner-the-transpose:
    touches: [CMPS-LO4]
---

# Matrices: adding, scaling and transposing a grid of numbers

Here is a grid of numbers. What do you think it will draw?

```python exec
id: nine-numbers-that-draw-a-picture-1
ramp = " .:-=+*#%@"

pixels = [
    [0, 0, 9, 0, 0],
    [0, 9, 9, 9, 0],
    [9, 9, 9, 9, 9],
    [0, 9, 9, 9, 0],
    [0, 0, 9, 0, 0],
]

for row in pixels:
    print("".join(ramp[value] for value in row))
```

```predict
What will the picture be?

- A diamond
  - The 9s are widest in the middle row.
- A cross
  - The middle row and the middle column are full of 9s.
- A square with a hole
  - The 0s are all round the edge.
```

A diamond. Each number says how dark one square is: 0 is blank and 9 is
solid. `ramp` is a string used as a lookup table, from light to dark:
`ramp[value]` turns a number into a character. The last line builds one
row of text: `ramp[value] for value in row` makes one character for each
number, like a list comprehension from
[Comprehensions, grids and aliasing](tutorial:comprehensions-and-grids),
and `"".join(...)` glues them into one string.

Every picture on a screen works this way. It is a grid of numbers, with
a rule that turns each number into something you can see. A photograph is a
bigger grid with a longer ramp, from 0 for black to 255 for white.

A *matrix* is a grid of numbers in rows and columns. `pixels` has 5
*rows* and 5 *columns*, so it is a 5×5 matrix. The number of rows always
comes first. In maths, the number in row $i$ and column $j$ is written
$a_{ij}$, counting from 1. Python counts from 0, and the row comes first:
`pixels[row][column]`. So $a_{11}$ is `pixels[0][0]`, the top-left
corner.

```python exec
id: nine-numbers-that-draw-a-picture-2
print(pixels[0])
print(pixels[1][3])
```

```predict
type: number

What will the last line print?
```

This page does three things to pictures: makes them darker, lays one
over another, and flips them corner to corner. Each is a matrix
operation, and you write each one yourself, so you can watch the
arithmetic happen. Later pages use them again, and a library called
NumPy does each one in a single line. NumPy comes at the end of the
series.

## Darker: scaling a grid

To make a picture darker, make every number bigger. A *scalar* is a
single number used with a matrix, and *scalar multiplication* multiplies
every entry by it:

$$k\begin{bmatrix} a & b \\ c & d \end{bmatrix} = \begin{bmatrix} ka & kb \\ kc & kd \end{bmatrix}$$

Can you write `scale(k, m)`? It returns a new matrix, and leaves `m`
as it was. The functions you write in this cell and the others marked
as a toolkit come with you to the later pages of the series.

```python exec
id: grid-scale
toolkit: yes
def scale(k, m):
    """A new matrix: every entry of m multiplied by k."""
    ...
```

```python toolkit-reference
for: grid-scale
def scale(k, m):
    """A new matrix: every entry of m multiplied by k."""
    return [[k * value for value in row] for row in m]
```

```inputs
scale(2, [[1, 2], [3, 4]])
scale(0, [[5, 6]])
scale(-1, [[1], [2]])
scale(3, pixels) == [[3 * v for v in row] for row in pixels]
```

```hint
One new row for each row of `m`, and in it, `k * value` for each value.
A nested loop builds it, or a comprehension inside a comprehension.
```

```solution
def scale(k, m):
    """A new matrix: every entry of m multiplied by k."""
    result = []
    for row in m:
        new_row = []
        for value in row:
            new_row.append(k * value)
        result.append(new_row)
    return result
---
A new list for every row, so `m` is left alone. Changing `m` in place
would change the picture it came from, the aliasing trap from
Comprehensions, grids and aliasing.
```

The diamond's 9s are already the darkest character in `ramp`. What
happens when the loop draws `scale(2, pixels)`?

```python exec
id: darker-scaling-a-grid-1
darker = scale(2, pixels)
for row in darker:
    print("".join(ramp[value] for value in row))
```

```predict
What will happen?

- A darker diamond
  - Twice the numbers, twice the darkness.
- The same diamond
  - It is as dark as it can be already.
- An error
  - Something about 18 does not fit.
```

An `IndexError`: `string index out of range`. The 9s became 18s, and
`ramp` has only ten characters, `ramp[0]` to `ramp[9]`. `scale` did
exactly what it should, and the matrix is fine. The picture has a limit.
A matrix does not know what its numbers mean. The rule that draws it
does. `show` below draws a grid with that limit built in. It draws
anything past 9 as 9 and anything below 0 as 0, and it rounds
fractions.

```python exec
id: grid-show
toolkit: yes
RAMP = " .:-=+*#%@"


def show(grid):
    """Draw a grid of numbers from 0 to 9 as text, one character a number."""
    for row in grid:
        line = ""
        for value in row:
            level = min(9, max(0, round(value)))
            line = line + RAMP[level]
        print(line)
```

```python exec
id: darker-scaling-a-grid-2
show(scale(2, pixels))
print()
show(scale(0.5, pixels))
```

Doubling the diamond changes nothing you can see, because it was
already at the limit, and halving it makes it paler. The matrix still
holds 18s, so scaling it down again gives the diamond back. A saved
photo is different. Its values stop at white, so any detail brighter
than white is lost.

## Overlay: adding two grids

To lay one picture over another, add them. *Matrix addition* adds the
numbers in the same position:

$$\begin{bmatrix} a & b \\ c & d \end{bmatrix} + \begin{bmatrix} e & f \\ g & h \end{bmatrix} = \begin{bmatrix} a+e & b+f \\ c+g & d+h \end{bmatrix}$$

Here is a frame the same size as the diamond.

```python exec
id: overlay-adding-two-grids-1
frame = [
    [5, 5, 5, 5, 5],
    [5, 0, 0, 0, 5],
    [5, 0, 0, 0, 5],
    [5, 0, 0, 0, 5],
    [5, 5, 5, 5, 5],
]
show(frame)
```

Can you write `add(a, b)`? Two pictures of different sizes cannot be
laid one over the other, so if the shapes do not match, `add` should
stop with an error that says so. The line `raise ValueError("a
message")` stops a function at once with a `ValueError` and your
message. [Reading an error message](tutorial:reading-an-error-message)
has more.

```python exec
id: grid-add
toolkit: yes
def add(a, b):
    """A new matrix: a and b added position by position.

    Raises ValueError if a and b are not the same shape.
    """
    ...
```

```python toolkit-reference
for: grid-add
def add(a, b):
    """A new matrix: a and b added position by position.

    Raises ValueError if a and b are not the same shape.
    """
    if len(a) != len(b) or len(a[0]) != len(b[0]):
        raise ValueError("a and b are not the same shape")
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]
```

```inputs
add([[1, 2], [3, 4]], [[10, 20], [30, 40]])
add([[1, 2, 3]], [[0, 0, 1]])
add(pixels, frame)[0]
```

```hint
Check the shapes first, before any loop. `len(a) == len(b)` checks the
rows, and `len(a[0]) == len(b[0])` checks the columns. Then build one
new row for each `i`, with `a[i][j] + b[i][j]` for each `j`.
```

```solution
def add(a, b):
    """A new matrix: a and b added position by position.

    Raises ValueError if a and b are not the same shape.
    """
    if len(a) != len(b) or len(a[0]) != len(b[0]):
        raise ValueError("a and b are not the same shape")
    result = []
    for i in range(len(a)):
        new_row = []
        for j in range(len(a[0])):
            new_row.append(a[i][j] + b[i][j])
        result.append(new_row)
    return result
---
The check comes before the loops. Without it, `add(pixels, small)`
fails deep inside a loop, with an `IndexError` about a position that
does not exist. `add(small, pixels)` quietly adds only the corner the
two share.
```

```python exec
id: overlay-adding-two-grids-4
show(add(pixels, frame))
```

Where the diamond meets the frame, 9 and 5 make 14, and `show` draws it
as 9. Now try two matrices of different shapes.

```python exec
id: overlay-adding-two-grids-2
small = [[1, 1], [1, 1]]
add(pixels, small)
```

This cell is meant to fail, with your own message. The *shape* of a
matrix is its number of rows and its number of columns. Addition works
only on matrices of the same shape.

Does the order of adding matter? For numbers, $3 + 5 = 5 + 3$.

```python exec
id: overlay-adding-two-grids-3
print(add(pixels, frame) == add(frame, pixels))
```

```predict
Will the two overlays be the same?

- True
  - Each position adds the same two numbers, in either order.
- False
  - Laying a picture on top is not the same as laying it underneath.
```

## Corner to corner: the transpose

The last operation has no arithmetic in it. The numbers only move. The
*transpose* of a matrix swaps its rows and columns, so row $i$, column
$j$ of the new matrix is row $j$, column $i$ of the old one. It is
written $A^T$. The diamond looks the same either way round, so here is a
picture that does not.

```python exec
id: corner-to-corner-the-transpose-1
flag = [
    [9, 9, 9, 9],
    [9, 0, 0, 0],
    [9, 9, 9, 0],
    [9, 0, 0, 0],
    [9, 0, 0, 0],
]
show(flag)
```

An F, 5 rows by 4 columns. Can you write `transpose(m)`? Its result has
one row for each column of `m`.

```python exec
id: grid-transpose
toolkit: yes
def transpose(m):
    """A new matrix: the rows of m become its columns."""
    ...
```

```python toolkit-reference
for: grid-transpose
def transpose(m):
    """A new matrix: the rows of m become its columns."""
    return [[row[j] for row in m] for j in range(len(m[0]))]
```

```inputs
transpose([[1, 2, 3], [4, 5, 6]])
transpose([[1, 2], [3, 4], [5, 6]])
transpose([[7]])
transpose(flag)
```

```hint
The first row of the result is the first number of every row of `m`:
`[row[0] for row in m]`. The second is `[row[1] for row in m]`. How many
of those rows are there?
```

```solution
def transpose(m):
    """A new matrix: the rows of m become its columns."""
    result = []
    for j in range(len(m[0])):
        new_row = []
        for row in m:
            new_row.append(row[j])
        result.append(new_row)
    return result
---
The loop runs once for each column of `m`, `len(m[0])` times, so a 5×4
matrix gives a 4×5 one.
```

```python exec
id: corner-to-corner-the-transpose-3
show(transpose(flag))
```

The F lies on its back, flipped corner to corner. The top-left square
stays where it is, and every other square swaps places across the line
from the top-left corner to the bottom-right. It is a mirror across that
diagonal, not a turn.

The diamond does not change when it is flipped this way. A matrix that
equals its own transpose is *symmetric*.

```python exec
id: corner-to-corner-the-transpose-2
print(transpose(pixels) == pixels)
print(transpose(flag) == flag)
```

## Your turn

A picture from the world you chose, and the three operations on it.

<div class="dl-world" data-world="pixel-art">

Here is a sprite, 7 squares wide. Can you make a ghost of it, half as
dark? Then can you lay it over its own transpose, and check whether the
overlay is symmetric? Before you run it, guess whether a picture added
to its own transpose is always symmetric.

```python exec
id: grid-your-world--pixel-art
sprite = [
    [0, 0, 9, 9, 9, 0, 0],
    [0, 9, 3, 9, 3, 9, 0],
    [9, 9, 9, 9, 9, 9, 9],
    [9, 0, 9, 0, 9, 0, 9],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
]
show(sprite)
```

```hint
`scale(0.5, sprite)` is the ghost. `add(sprite, transpose(sprite))` is the
overlay, and `transpose(overlay) == overlay` checks it.
```

```solution
{{include: setup/matrices/grid.py}}

sprite = [
    [0, 0, 9, 9, 9, 0, 0],
    [0, 9, 3, 9, 3, 9, 0],
    [9, 9, 9, 9, 9, 9, 9],
    [9, 0, 9, 0, 9, 0, 9],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
]
show(scale(0.5, sprite))
print()
overlay = add(sprite, transpose(sprite))
show(overlay)
print(transpose(overlay) == overlay)
---
Always. Position $(i, j)$ of the overlay is $a_{ij} + a_{ji}$, and
position $(j, i)$ is $a_{ji} + a_{ij}$: the same two numbers, added the
other way round. So any matrix plus its transpose is symmetric. The
sprite has to be square. A 5×7 sprite and its 7×5 transpose are not the
same shape, and `add` says so.
```

</div>

<div class="dl-world" data-world="photos">

The file `grace-hopper.csv` is a photograph of Grace Hopper, a pioneer
of programming languages, as 70 rows of 60 numbers from 0 (black) to 255
(white). This cell loads it and draws it. Can you make a darker copy,
flip it corner to corner, and fade it into a *gradient*, a grid that
goes smoothly from dark on the left to light on the right?

```python exec
id: grid-your-world--photos
import matplotlib.pyplot as plt

text = await load_text("grace-hopper.csv")
photo = [[int(value) for value in line.split(",")] for line in text.splitlines()]
print(len(photo), "rows of", len(photo[0]))

gradient = [[round(255 * j / 59) for j in range(60)] for i in range(70)]


def draw(grid):
    """Draw a grid of numbers from 0 to 255 as a greyscale picture."""
    plt.figure()
    plt.imshow(grid, cmap="gray", vmin=0, vmax=255)
    plt.axis("off")


draw(photo)
```

```hint
Darker means smaller numbers here, since 0 is black: `scale(0.5,
photo)`. For the fade, halve each picture and add them, so that the
result stays between 0 and 255.
```

```solution
{{include: setup/matrices/grid.py}}

import matplotlib.pyplot as plt

text = await load_text("grace-hopper.csv")
photo = [[int(value) for value in line.split(",")] for line in text.splitlines()]
print(len(photo), "rows of", len(photo[0]))

gradient = [[round(255 * j / 59) for j in range(60)] for i in range(70)]


def draw(grid):
    """Draw a grid of numbers from 0 to 255 as a greyscale picture."""
    plt.figure()
    plt.imshow(grid, cmap="gray", vmin=0, vmax=255)
    plt.axis("off")


draw(scale(0.5, photo))
draw(transpose(photo))
draw(add(scale(0.5, photo), scale(0.5, gradient)))
---
In a photograph, 0 is black and 255 is white, the other way round from
the diamond's ramp, so darker is `scale(0.5, photo)`. The transpose lays
her on her side, 60 rows by 70, with the top-left corner where it was.
The fade is an average. It adds half of each picture, which is how a
photo editor mixes two layers. Adding them whole would push the bright
parts past 255, and `imshow` would draw all of it as white.
```

</div>

## Looking back

Scaling past 9 broke the drawing and not the matrix. Can you say, for
one of the three operations on this page, what it does to the numbers,
and separately what it does to the picture?

A challenge: subtract a picture from a copy of itself moved one square
to the right. Where the picture stays the same from one square to the
next, the difference is 0. What do the other squares draw?

```python challenge
pixels = [
    [0, 0, 9, 0, 0],
    [0, 9, 9, 9, 0],
    [9, 9, 9, 9, 9],
    [0, 9, 9, 9, 0],
    [0, 0, 9, 0, 0],
]
# For each row, the difference between each square and the one to its left.
# Draw the absolute values: what do the non-zero squares outline?
```

The next page, [what a matrix does to a
picture](tutorial:what-a-matrix-does-to-a-picture), uses a 2×2 matrix in
a new way, as an instruction that moves every point of a picture.

## Where to read more

Grant Sanderson (3Blue1Brown) (2016). *Essence of Linear Algebra, Chapter
1: Vectors, What Even Are They?*
<https://www.youtube.com/watch?v=fNk_zzaMoSs>. The geometric picture
underneath the grids on this page, and the start of a series worth the
whole hour.

Downey, A. B. (2015). *Think Python: How to Think Like a Computer
Scientist* (2nd ed.). Green Tea Press.
<https://greenteapress.com/wp/think-python-2e/>. Chapter 10 on lists is
the Python half of what a matrix is built from here.

Python Software Foundation. *5. Data Structures — Nested List
Comprehensions.* <https://docs.python.org/3/tutorial/datastructures.html>.
The pattern behind every nested loop on this page, as its own topic.
