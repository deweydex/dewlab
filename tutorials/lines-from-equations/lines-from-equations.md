---
title: "Lines from equations: painting y = ax + b"
year: "2026-2027"
version: 2026.10.21.2
---

# Lines from equations: painting y = ax + b

The lines we have painted so far run along a row or down a column. A
line can also slope. Run the cell. It lists some points on the line
$y = 0.4x + 1$, and rounds each $y$ to the nearest whole number.

```python exec
id: points-on-a-line-1
for x in range(0, 8):
    y = 0.4 * x + 1
    print(x, y, round(y))
```

```predict
type: number

What will the last number on the last line be?
```

A straight line follows the rule $y = ax + b$. The number $a$ is the
*slope*, how much $y$ rises for each step of $x$. The number $b$ is the
value of $y$ when $x$ is 0. A canvas has only whole squares, so we find
$y$ for every whole $x$, round it, and paint that square. The pictures
on this page use a canvas of 255 by 255, so that a line has room to run.

## Where is (0, 0)?

On the first page we chose where row 0 sits. With the bottom, which is
the choice in our pictures, the point $(0, 0)$ is the bottom-left square,
$x$ is the column and $y$ is the row, so nothing needs converting. With
the top, rows count downwards while $y$ counts upwards, so you would turn
$y$ into a row number. The function below is the one place where your
choice shows. Which did you choose, and what does `paint_xy` do about it?

Some squares of a line fall outside the canvas, and we skip them. A
check is needed here, because Python does not stop at a row of -1. Run
the cell.

```python exec
id: where-is-the-origin-1
letters = ["a", "b", "c"]
print(letters[-1])
```

```predict
type: text

What will the cell print?
```

A negative index counts from the end of the list. A row of -1 is the
last row, so a line that leaves the canvas at the bottom would quietly
paint along the top of the picture.

```python exec
id: paint-xy
toolkit: yes
expect: (lambda c: (paint_xy(c, 0, 0), paint_xy(c, 9, 9), paint_xy(c, -1, 1), paint_xy(c, 1, -1), c[0][0] + c[2][0] == 1 and sum(map(sum, c)) == 1)[4])(make_canvas(3, 3))
def paint_xy(canvas, x, y):
    """Paint the square at the point (x, y), with (0, 0) in the bottom-left square. Do nothing when the point is off the canvas."""
    # Which row holds y? That depends on the origin you chose on the first page.
    # Which conditions must be true before the square is painted?
    # What does Python do with a row of -1, or a column of -1?
    ...
```

```python toolkit-reference
for: paint-xy
def paint_xy(canvas, x, y):
    """Paint the square at the point (x, y), with (0, 0) in the bottom-left square. Do nothing when the point is off the canvas."""
    # A row of -1 would quietly wrap to the last row, so test both ends.
    if 0 <= y < len(canvas) and 0 <= x < len(canvas[0]):
        paint_point(canvas, y, x)
```

```hint
after: 3 errors
On a canvas of 3 rows, which row holds the point where $y$ is 0, with
the origin you chose? Which conditions must be true before `paint_point`
is called?
```

```solution
def paint_xy(canvas, x, y):
    """Paint the square at the point (x, y), with (0, 0) in the bottom-left square. Do nothing when the point is off the canvas."""
    # A row of -1 would quietly wrap to the last row, so test both ends.
    if 0 <= y < len(canvas) and 0 <= x < len(canvas[0]):
        paint_point(canvas, y, x)
---
Here is one answer. Yours may be different and work too. It counts rows
from the bottom, so $y$ is the row. If you chose the top, use `row =
len(canvas) - 1 - y` and test `row` instead. `0 <= y < len(canvas)`
rejects both a negative row and a row past the end. The same test for
`x` keeps the column inside the canvas.
```

## A line from a and b

How would you paint the line $y = ax + b$ between two values of $x$?

```python exec
id: a-line-from-a-and-b-1
toolkit: yes
expect: (lambda c: (paint_line(c, 1, 0, 0, 11), sum(map(sum, c)) == 12 and c[11][0] == 1 and c[0][11] == 1)[1])(make_canvas(12, 12))
def paint_line(canvas, a, b, start_x, end_x):
    """Paint the line y = a * x + b for every whole x from start_x to end_x."""
    # What is y for one x? How do you turn it into a whole number?
    # Which earlier function paints a point at (x, y)?
    # Does your function work for a steep line, such as a = 3? What do you see?
    ...
```

```python toolkit-reference
for: a-line-from-a-and-b-1
def paint_line(canvas, a, b, start_x, end_x):
    """Paint the line y = a * x + b for every whole x from start_x to end_x."""
    if abs(a) <= 1:
        for x in range(start_x, end_x + 1):
            paint_xy(canvas, x, round(a * x + b))
    else:
        # A steep line climbs more than one row per column, so stepping through x
        # leaves gaps. Step through y instead, and find x for each row.
        first_y = round(a * start_x + b)
        last_y = round(a * end_x + b)
        for y in range(min(first_y, last_y), max(first_y, last_y) + 1):
            paint_xy(canvas, round((y - b) / a), y)
```

```hint
after: 3 errors
For $x = 0$ on the line $y = 0.4x + 1$, what is $y$? What does the
cell at the top of the page print for it? Which function paints that
square?
```

```solution
def paint_line(canvas, a, b, start_x, end_x):
    """Paint the line y = a * x + b for every whole x from start_x to end_x."""
    for x in range(start_x, end_x + 1):
        paint_xy(canvas, x, round(a * x + b))
---
Here is one answer. Yours may be different and work too. It steps
through $x$ and finds a $y$ for each. The next section shows where that
stops working.
```

Can you make this picture? It has three lines on a canvas of 255 by 255.
Before you run it, write a guess in a comment: which two lines meet
nearest the bottom-left corner?

![A white 255 by 255 grid with three long lines of black squares: one rising steeply from the bottom-left corner, one rising gently from the left edge, and one falling gently from the upper left.](three-lines.png)

```python exec
id: a-line-from-a-and-b-2
# Your three lines
```

```hint
Read three points off each line, using the numbers along the edge. How
much does $y$ rise when $x$ goes up by 100? That is $100a$, and it gives
you $a$.
```

```solution
{{include: setup/painting/toolkit.py}}

canvas = make_canvas(255, 255)
paint_line(canvas, 1, 0, 0, 254)
paint_line(canvas, 0.4, 30, 0, 254)
paint_line(canvas, -0.4, 220, 0, 254)
show_picture(canvas)
---
Here is one answer. Yours may be different and work too. The lines
$y = x$ and $y = 0.4x + 30$ meet where $x = 0.4x + 30$, which is at
$x = 50$.
```

A half-way value can round either way. Python's `round(2.5)` gives 2 and
`round(3.5)` gives 4, so a half-way value goes to the even number. The
lines above never land on a half, so the two ways agree. Try
$y = 0.5x + 20$ on your own and look at the steps it makes.

## A steep line

A line with a slope of 3 climbs three rows for each column. Can you make
this picture, a line with no gaps?

![A white 255 by 255 grid with one steep line of black squares that touch each other, rising from near the bottom-left corner.](a-steep-line.png)

```python exec
id: a-steep-line-1
# Your steep line
```

```predict
type: choice

If your `paint_line` steps through $x$ only, how will its squares look?

- Joined, with no gaps
  - A line is made of squares that touch.
- In separate dots
  - Each whole $x$ gives one square, and the line climbs three rows for each.
```

When you try it, what do you see? Why do the squares not touch? What
would you change in `paint_line`, in its own cell above, so that a steep
line has no gaps? Run the cell above again afterwards.

```hint
for: a-steep-line-1
after: 2 unchanged runs
title: a way to start
There are only as many squares as there are whole values of $x$. For a
steep line, can you step through $y$ instead? The rule rearranged is
$x = (y - b) / a$. Which of the first and last $y$ is smaller when $a$
is negative?
```

```solution
for: a-steep-line-1
{{include: setup/painting/toolkit.py}}

canvas = make_canvas(255, 255)
paint_line(canvas, 3, -2, 1, 80)
show_picture(canvas)
---
Here is one answer. Yours may be different and work too. It needs a
`paint_line` that steps through $y$ for a steep line, like the toolkit
version. `min` and `max` make that work when $a$ is negative.
```

Now try your own. Paint a line that leaves the canvas at the bottom, and
a line with a negative slope. What does your `paint_xy` do with the
squares that are off the canvas?

## Your turn: a cube on a table

A drawing looks flat until the edges that run away from us meet at one
point. That point is the *vanishing point*, and every edge that runs
back from the front face of the cube points at it. Here the vanishing
point is $(80, 88)$ on a canvas of 120 by 120. The cube sits on a table
that is drawn the same way, and a shadow falls on the table. Which edges
need `paint_line`, and which can use the functions from the first page?
Hidden edges are not drawn.

![A cube on a table drawn in perspective. The cube has a grey front face, a white top and a darker side, and casts a grey shadow on the table top.](a-cube-on-a-table.png)

```python exec
id: your-turn-1
# Your cube on a table
```

```hint
Start with the front face of the cube, which is a square with a flat
edge on every side. Then the three edges that run back are lines that
pass through $(80, 88)$. If one end is at $(60, 58)$, which $a$ and $b$
make $y = ax + b$ go through both points?
```

```hint
after: 2 unchanged runs
title: a way to start
The front face is a rectangle from $(30, 28)$ to $(60, 58)$. The edge
from $(60, 58)$ to the vanishing point has the slope
$(88 - 58) / (80 - 60)$. Which line of $y = ax + b$ is that? The cube
stops before the vanishing point, so paint only a few squares of it.
```

```solution
{{include: setup/painting/toolkit.py}}

# Edges hold 3 ink (black), the front face 1, the shaded side 2 and the shadow 1.
canvas = make_canvas(120, 120)

for row in range(28, 41):                    # the shadow on the table
    left = round(60 + (row - 28) / 3)
    paint_horizontal(canvas, row, left, left + 16)
paint_rectangle(canvas, 28, 30, 58, 60)      # the front face
for x in range(60, 65):                      # the shaded side, one column at a time
    for layer in range(2):
        paint_vertical(canvas, x, round(3 * x - 152), round(1.5 * x - 32))

for layer in range(3):
    paint_horizontal(canvas, 14, 6, 100)     # the table: front edge and back edge
    paint_horizontal(canvas, 51, 65, 90)     # the cube hides the rest of the back edge
    paint_line(canvas, 1, 8, 6, 29)          # its two sides run towards the vanishing point
    paint_line(canvas, -3.7, 384, 90, 100)   # the cube hides the left side from x = 30
    paint_horizontal(canvas, 6, 6, 100)      # the table's edge, and its legs
    paint_vertical(canvas, 6, 6, 14)
    paint_vertical(canvas, 100, 6, 14)
    paint_rectangle(canvas, 0, 8, 5, 10)
    paint_rectangle(canvas, 0, 96, 5, 98)
    paint_horizontal(canvas, 28, 30, 60)     # the front face of the cube
    paint_horizontal(canvas, 58, 30, 60)
    paint_vertical(canvas, 30, 28, 58)
    paint_vertical(canvas, 60, 28, 58)
    paint_horizontal(canvas, 64, 40, 64)     # the back edges, seen above and beside it
    paint_vertical(canvas, 64, 40, 64)
    paint_line(canvas, 0.6, 40, 30, 40)      # three edges that run back to the vanishing point
    paint_line(canvas, 1.5, -32, 60, 64)
    paint_line(canvas, 3, -152, 60, 64)
show_picture(canvas, darkest=3)
---
Here is one answer. Yours may be different and work too. The three edges
that run back have the slopes 0.6, 1.5 and 3, and every one passes
through the vanishing point: $0.6 \times 80 + 40$, $1.5 \times 80 - 32$
and $3 \times 80 - 152$ all equal 88. The edges are painted three times
so that they are black at `darkest=3`, and the table's left side and
back edge stop where the cube hides them.
```

## Looking back

Your toolkit now holds every function behind the three pictures on the
first page of the series. What did you change in `paint_line` to make
steep lines join, and why did the change matter only for lines steeper
than 1?

A challenge: paint the diagonals of a square canvas, and then a star
shape made of lines through its centre.

```python challenge
# The two diagonals of a 255 by 255 canvas, and then more lines through its centre.
canvas = make_canvas(255, 255)
```

## Where to read more

Wikipedia. *Bresenham's line algorithm.*
<https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm>. The
method that computers use to draw a line quickly, using only whole
numbers. It solves the same problem as the steep line on this page.

Grant Sanderson (3Blue1Brown) (2016). *Essence of Linear Algebra,
Chapter 1: Vectors, What Even Are They?*
<https://www.youtube.com/watch?v=fNk_zzaMoSs>. The picture behind the
grids of numbers in the next series, and the start of a series worth
the whole hour.
