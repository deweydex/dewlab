---
title: "A canvas of numbers: painting points and lines"
year: "2026-2027"
version: 2026.10.21.2
---

# A canvas of numbers: painting points and lines

Every picture on a screen is a grid of numbers. In this series we build
a small library of functions that paint pictures onto such a grid, one
idea at a time. Here are three pictures made with a library like the one
you will write. Yours will look different, and that is the point.

![A night skyline. Overlapping grey buildings stand under a sky that fades from black to white, above a black road.](a-night-skyline.png)

![A black outline of a cube with a grey front face, standing on a black table with two legs.](a-cube-on-a-table.png)

![Nested squares that grow darker towards the centre, like a stepped pyramid seen from above.](nested-squares.png)

This page makes the first four functions of your toolkit: a blank
canvas, a point, and two kinds of line. Every later function is built
from them.

## A letter in numbers

Here is a small grid of numbers. Run the cell. Can you see a letter in
it?

```python exec
id: a-letter-in-numbers-1
letter = [
    [1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0],
    [1, 0, 0, 0, 0],
    [1, 1, 1, 1, 0],
    [1, 0, 0, 0, 0],
    [1, 0, 0, 0, 0],
    [1, 1, 1, 1, 1],
]
for row in letter:
    print(row)
```

Each number is the amount of *ink* on one square of the paper. A 0 means
no ink, so the square stays white. A 1 means one layer of ink. The whole
grid is a *canvas*: a list of rows, where each row is a list of numbers.
`canvas[row][column]` is the square in that row and that column. Row 0
is the top row and column 0 is the left column, the same way you read a
page.

The next cell teaches Python to draw a canvas. It uses `matplotlib`, a
library that draws pictures. You do not need to read it yet. Run it, and
then run the cell under it.

```python exec
id: a-letter-in-numbers-2
toolkit: yes
def show_picture(canvas, darkest=1):
    """Draw a canvas. A square with 0 ink is white. A square with `darkest` ink or more is black."""
    import matplotlib.pyplot as plt

    rows = len(canvas)
    columns = len(canvas[0])
    longest = max(rows, columns)
    size = min(7, max(3, longest / 5))
    plt.figure(figsize=(size * columns / longest, size * rows / longest))
    plt.imshow(canvas, cmap="gray_r", vmin=0, vmax=darkest, interpolation="nearest")
    plt.xticks(range(0, columns, max(1, columns // 10)))
    plt.yticks(range(0, rows, max(1, rows // 10)))
```

```python exec
id: a-letter-in-numbers-3
show_picture(letter)
```

It is an E. Now change one of the 0s in the second row of `letter` to a
3, and run both cells again. What do you think the 3 will look like?
Then try `show_picture(letter, darkest=3)`. The `darkest` number says
how much ink counts as black. With the default of 1, a square with 3
ink looks the same as a square with 1.

## A shortcut that goes wrong

How would you make a blank canvas of any size? Here is a short way to
make one with 4 rows and 6 columns. Run the cell, and then read the rows
it prints.

```python exec
id: a-shortcut-that-goes-wrong-1
rows = 4
columns = 6
shared = [[0] * columns] * rows
shared[1][2] = 1
for row in shared:
    print(row)
print(sum(sum(row) for row in shared))
```

```predict
type: number

Only one square got a 1. How many 1s will the cell print in total?
```

The shortcut makes one row, and then repeats that same row four times.
The four rows are one list with four names, the problem in
[Two names, one list](tutorial:two-names-one-list). Changing one square
changes the same square in every row.

## A blank canvas

Here is the function. It has a name, two inputs and an empty body. The
comments are questions for you. Answer them in your own words first, and
then in code.

```python exec
id: make-canvas
toolkit: yes
expect: make_canvas(2, 3) == [[0, 0, 0], [0, 0, 0]] and (lambda c: c[0] is not c[1])(make_canvas(2, 2))
def make_canvas(rows, columns):
    """A canvas of this size with no ink on any square."""
    # Inputs: what type is rows? What type is columns?
    # Returns: what type should come back? What does it look like when it is empty?
    # How many lists do you need? Do any of them share a name?
    ...
```

```python toolkit-reference
for: make-canvas
def make_canvas(rows, columns):
    """A canvas of this size with no ink on any square."""
    canvas = []
    for row in range(rows):
        canvas.append([0] * columns)
    return canvas
```

```hint
after: 3 errors
Which line of the error is yours? What did you expect
`make_canvas(2, 3)` to return, and what did it return?
```

```hint
after: 6 errors
title: some steps
1. Start with an empty list called `canvas`.
2. Go round a loop once for each row. Inside it, add a new list of
   `columns` zeros to `canvas`.
3. Return `canvas` after the loop.

**Think about:** which part of the shortcut made every row the same
list, and why a loop does not.
```

```solution
def make_canvas(rows, columns):
    """A canvas of this size with no ink on any square."""
    canvas = []
    for row in range(rows):
        canvas.append([0] * columns)
    return canvas
---
Here is one answer. Yours may be different and work too. `[0] * columns`
runs again on every trip round the loop, so every row is a new list.
```

Let's make a small canvas and draw it. The picture is all white.

```python exec
id: a-blank-canvas-1
canvas = make_canvas(5, 8)
show_picture(canvas)
print(len(canvas), "rows of", len(canvas[0]))
```

## A point

How would you put ink on one square?

```python exec
id: paint-point
toolkit: yes
expect: (lambda c: (paint_point(c, 1, 2), c[1][2] == 1 and sum(map(sum, c)) == 1)[1])(make_canvas(3, 4))
def paint_point(canvas, row, column):
    """Add 1 ink to the square at this row and column."""
    # Inputs: what type is each of the three inputs?
    # Returns: does this function need to return anything? Why, or why not?
    ...
```

```python toolkit-reference
for: paint-point
def paint_point(canvas, row, column):
    """Add 1 ink to the square at this row and column."""
    canvas[row][column] = canvas[row][column] + 1
```

```solution
def paint_point(canvas, row, column):
    """Add 1 ink to the square at this row and column."""
    canvas[row][column] = canvas[row][column] + 1
---
Here is one answer. Yours may be different and work too. It changes the
list the canvas holds, so the caller's canvas changes and nothing needs
to be returned.
```

Can you make this picture? Read the numbers along its edges to find the
rows and columns.

![A white 16 by 16 grid with three black squares: one near the top left, one in the middle and one near the lower right.](three-points.png)

```python exec
id: paint-a-point-1
# Your picture of three points
```

```solution
{{include: setup/painting/toolkit.py}}

canvas = make_canvas(16, 16)
paint_point(canvas, 3, 4)
paint_point(canvas, 8, 8)
paint_point(canvas, 12, 13)
show_picture(canvas)
---
Here is one answer. Yours may be different and work too.
```

What happens when we paint one square twice?

```python exec
id: paint-a-point-2
canvas = make_canvas(5, 5)
paint_point(canvas, 2, 3)
paint_point(canvas, 2, 3)
print(canvas[2][3])
show_picture(canvas)
```

```predict
type: number

What will the cell print?
```

The square holds 2 ink, and the picture looks the same as with 1 ink,
because the default `darkest` is 1. Run `show_picture(canvas, darkest=2)`
in a new cell. Which square is the darkest now?

Try your own canvas. Paint some squares on a size you choose. What
happens when you paint a square that is not on the canvas?

## Lines

How would you draw a horizontal line? A vertical line? You already have
a function that paints one square.

```python exec
id: lines-1
toolkit: yes
expect: (lambda c: (paint_horizontal(c, 1, 1, 3), c[1] == [0, 1, 1, 1, 0])[1])(make_canvas(3, 5))
def paint_horizontal(canvas, row, start_column, end_column):
    """Paint a run of squares along one row, from start_column to end_column."""
    # Decide: does the run include the end column? Keep your choice in every function.
    # Which earlier function paints one square? What needs to repeat?
    ...
```

```python exec
id: lines-2
toolkit: yes
expect: (lambda c: (paint_vertical(c, 2, 0, 2), [r[2] for r in c] == [1, 1, 1])[1])(make_canvas(3, 4))
def paint_vertical(canvas, column, start_row, end_row):
    """Paint a run of squares down one column, from start_row to end_row."""
    # How is this like paint_horizontal? What is different?
    ...
```

```python toolkit-reference
for: lines-1
def paint_horizontal(canvas, row, start_column, end_column):
    """Paint a run of squares along one row, from start_column to end_column."""
    for column in range(start_column, end_column + 1):
        paint_point(canvas, row, column)
```

```python toolkit-reference
for: lines-2
def paint_vertical(canvas, column, start_row, end_row):
    """Paint a run of squares down one column, from start_row to end_row."""
    for row in range(start_row, end_row + 1):
        paint_point(canvas, row, column)
```

```hint
for: lines-1
after: 3 errors
`range(2, 5)` gives 2, 3 and 4. Which squares does your loop paint when
`start_column` is 1 and `end_column` is 3? Does the last square get its
ink?
```

```solution
for: lines-1
def paint_horizontal(canvas, row, start_column, end_column):
    """Paint a run of squares along one row, from start_column to end_column."""
    for column in range(start_column, end_column + 1):
        paint_point(canvas, row, column)
---
Here is one answer. Yours may be different and work too. A `range` stops
one before its end value, so `end_column + 1` includes the last square.
```

```solution
for: lines-2
def paint_vertical(canvas, column, start_row, end_row):
    """Paint a run of squares down one column, from start_row to end_row."""
    for row in range(start_row, end_row + 1):
        paint_point(canvas, row, column)
---
Here is one answer. Yours may be different and work too. It is the same
loop as `paint_horizontal`, with the row changing instead of the column.
```

## Your turn: a letter

Can you make this picture? It is a canvas of 32 by 32. Where do two of
its lines share a square? Try `darkest=2` to find out.

![A black capital letter E on a white 32 by 32 grid: a vertical bar with three horizontal arms, the middle arm shorter.](a-letter-e.png)

```python exec
id: your-turn-1
# Your letter E
```

```hint
Four lines make the whole E. Which of them are horizontal and which are
vertical? What do the numbers along the edge tell you about where each
one starts and ends?
```

```solution
{{include: setup/painting/toolkit.py}}

canvas = make_canvas(32, 32)
paint_vertical(canvas, 6, 6, 26)
paint_horizontal(canvas, 6, 6, 24)
paint_horizontal(canvas, 16, 6, 20)
paint_horizontal(canvas, 26, 6, 24)
show_picture(canvas)
---
Here is one answer. Yours may be different and work too. The corners of
the E are painted twice, so `darkest=2` shows them as black.
```

Now try your own. Make a canvas that is wider than it is tall. Paint the
whole bottom row and the whole last column. What happens when the start
of a line is bigger than its end?

## Looking back

Painting the same square twice made no visible difference until we
changed `darkest`. What does that tell you about where the ink is
stored, and what the picture shows?

A challenge: paint the first letter of your name on a canvas, using only
points and lines. Which letters are easy, and which are hard?

```python challenge
# Paint the first letter of your name.
# Your toolkit has make_canvas, paint_point, paint_horizontal,
# paint_vertical and show_picture.
```

The next page, [Rectangles and grids](tutorial:rectangles-and-grids),
fills whole regions with ink, using the functions you wrote here.

## Where to read more

Wikipedia. *Raster graphics.*
<https://en.wikipedia.org/wiki/Raster_graphics>. The name for pictures
made of a grid of squares, and how screens and printers use them.

Downey, A. B. (2015). *Think Python: How to Think Like a Computer
Scientist* (2nd ed.). Green Tea Press.
<https://greenteapress.com/wp/think-python-2e/>. Chapter 10 covers the
lists that every canvas on this page is made of.
