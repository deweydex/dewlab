---
title: "Matrix multiplication: rows times columns"
year: "2026-2027"
version: 2026.09.26.2
worlds:
  pixel-art: Pictures made of small squares, the way a screen draws them.
  starships: Starships, and the structures they are built from.
  space-scenes: Stars, planets and the paths they take across the sky.
covers:
  one-move-after-another:
    touches: [CMPS-LO4]
  where-the-rule-comes-from:
    touches: [CMPS-LO4]
  order-matters:
    touches: [CMPS-LO4]
  every-corner-at-once:
    touches: [CMPS-LO4]
  the-matrix-that-does-nothing:
    touches: [CMPS-LO4]
---

# Matrix multiplication: rows times columns

On the last page, one matrix moved the F. Here are two moves, one after
the other: a shear, and then a quarter turn.

```python exec
id: one-move-after-another-1
F = [(0, 0), (1, 0), (1, 2), (2, 2), (2, 3), (1, 3), (1, 4), (3, 4), (3, 5), (0, 5)]
shear = [[1, 1], [0, 1]]
turn = [[0, -1], [1, 0]]

leaned = transform_all(shear, F)
leaned_then_turned = transform_all(turn, leaned)
draw_shapes([F, leaned, leaned_then_turned])
```

Is there one matrix that does both moves at once? If there is, a
program could store a whole sequence of moves as four numbers, however
long the sequence. That is how a game moves a character through a turn,
a lean and a shrink in one step.

## One move after another

The last page gave a way to find any matrix: decide where "right",
$(1, 0)$, and "up", $(0, 1)$, go, and write those in as its columns. So
follow those two points through both moves.

```python exec
id: one-move-after-another-2
right = transform(turn, transform(shear, (1, 0)))
up = transform(turn, transform(shear, (0, 1)))
print("right ends at", right)
print("up ends at", up)
```

```predict
Where will "right", $(1, 0)$, end up after the shear and then the turn?

- (0, 1)
  - The shear leaves the bottom edge alone, and the turn sends right to up.
- (1, 1)
  - The shear moves it, then the turn moves it again.
- (-1, 1)
  - Both moves act on it.
```

"Right" ends at $(0, 1)$ and "up" at $(-1, 1)$. Written in as columns,
that is the one matrix for both moves.

```python exec
id: one-move-after-another-3
both = [[0, -1], [1, 1]]
print(transform_all(both, F) == leaned_then_turned)
```

It is. The matrix that does "$S$, then $T$" is called the *product* of
the two, written $TS$: the move that happens first is written on the
right, next to the point it acts on, the way $f(g(x))$ does $g$ first.
Finding it by following two points works every time. The next section
turns it into a rule that needs no points at all.

## Where the rule comes from

Follow "up" again. The shear sends it to its second column, $(1, 1)$.
Then the turn acts on $(1, 1)$: its new x is the turn's first row paired
with $(1, 1)$, $0 \times 1 + (-1) \times 1 = -1$, and its new y is the
second row paired with it, $1 \times 1 + 0 \times 1 = 1$. So every entry
of $TS$ is one row of $T$ paired with one column of $S$: multiply the
matching numbers, and add.

That pairing is the *dot product*. For two lists of the same length, it
multiplies each pair and adds up the results: the dot product of
$[1, 2, 3]$ and $[4, 5, 6]$ is $1 \times 4 + 2 \times 5 + 3 \times 6 =
32$. You met it in
[Comprehensions, grids and aliasing](tutorial:comprehensions-and-grids).
`zip` pairs two lists position by position:

```python exec
id: the-dot-product-first-1
print(list(zip([1, 2, 3], [4, 5, 6])))
print(list(zip([1, 2, 3], [4, 5])))
```

```predict
What will the second line print, when one list is shorter?

- [(1, 4), (2, 5), (3, None)]
  - The missing number is filled in with nothing.
- [(1, 4), (2, 5)]
  - zip stops when the shorter list runs out.
- An error
  - The lists do not match.
```

`zip` stops at the end of the shorter list, without a word. A dot
product built on `zip` would give an answer for lists that do not match,
and the answer would look exactly like a right one. So `dot` should
check the lengths first. Can you write it? It comes with you to the
later pages, with `multiply` below.

```python exec
id: matrix-dot-multiply
toolkit: yes
def dot(a, b):
    """The dot product: each pair multiplied, then added up.

    Raises ValueError if a and b are not the same length.
    """
    ...


def multiply(a, b):
    """The matrix product ab: row i of a with column j of b, in every place."""
    ...
```

```python toolkit-reference
for: matrix-dot-multiply
def dot(a, b):
    """The dot product: each pair multiplied, then added up.

    Raises ValueError if a and b are not the same length.
    """
    if len(a) != len(b):
        raise ValueError("lengths do not match")
    return sum(x * y for x, y in zip(a, b))


def multiply(a, b):
    """The matrix product ab: row i of a with column j of b, in every place."""
    columns = transpose(b)
    return [[dot(row, column) for column in columns] for row in a]
```

```inputs
dot([1, 2, 3], [4, 5, 6])
multiply([[0, -1], [1, 0]], [[1, 1], [0, 1]])
multiply([[1, 2], [3, 4]], [[5, 0], [1, -1]])
multiply([[1, 2, 3]], [[1], [0], [2]])
```

```hint
For `dot`: check the lengths, then add up `x * y` for each pair from
`zip(a, b)`. For `multiply`: the columns of `b` are the rows of
`transpose(b)`, from the first page. Each entry of the result is `dot(row,
column)`, one for each row of `a` and each column of `b`.
```

```solution
def dot(a, b):
    """The dot product: each pair multiplied, then added up.

    Raises ValueError if a and b are not the same length.
    """
    if len(a) != len(b):
        raise ValueError("lengths do not match")
    total = 0
    for x, y in zip(a, b):
        total = total + x * y
    return total


def multiply(a, b):
    """The matrix product ab: row i of a with column j of b, in every place."""
    result = []
    for row in a:
        new_row = []
        for column in transpose(b):
            new_row.append(dot(row, column))
        result.append(new_row)
    return result
---
A list of lists stores rows, so a column of `b` is awkward to reach;
`transpose` turns the columns into rows. `multiply(turn, shear)` gives
`[[0, -1], [1, 1]]`, the matrix found by following the two points.
```

```python exec
id: where-the-rule-comes-from-1
print(multiply(turn, shear))
```

The rule, written out: the entry in row $i$, column $j$ of $AB$ is row
$i$ of $A$ dotted with column $j$ of $B$,

$$c_{ij} = \sum_{k} a_{ik} \, b_{kj}$$

Here it is on bigger numbers.

```python exec
id: multiplying-two-grids-3
A = [[1, 2], [3, 4]]
B = [[5, 0], [1, -1]]
print(multiply(A, B))
```

![Matrix A times matrix B equals AB. The first row of A is shaded, the
first column of B is shaded, and the entry they produce in the top left of
AB is shaded. Below, the working: one times five plus two times one equals
seven.](row-times-column.svg)

One row and one column make one entry, and the entry goes where that
row and that column meet. The picture shows why the shapes must agree:
a row and a column can only pair up if they have the same length.

## Order matters

With numbers, $3 \times 5 = 5 \times 3$. Is a shear then a turn the same
as a turn then a shear?

```python exec
id: order-matters-1
print("turn after shear:", multiply(turn, shear))
print("shear after turn:", multiply(shear, turn))
draw_shapes([F, transform_all(multiply(turn, shear), F), transform_all(multiply(shear, turn), F)])
```

```predict
Will the two products be the same?

- Yes
  - The same two moves, so the same result.
- No
  - Leaning and then turning leans along a different edge from turning and then leaning.
```

Different matrices, and different pictures. Lean the F and then turn
it, and it leans one way; turn it first and then lean it, and the lean
acts on the turned F, along a different edge. For matrices, $AB$ and
$BA$ are usually different, which is why the order of writing them
matters: $TS$ means $S$ first.

## Every corner at once

`transform_all` moves one point at a time. Multiplication can move them
all together. Put the F's corners side by side as the columns of one
matrix: the x's along the top row, the y's along the bottom.

```python exec
id: every-corner-at-once-1
corners = [[x for x, y in F], [y for x, y in F]]
print(corners)
moved = multiply(turn, corners)
print(moved)
```

`corners` is 2×10: one column for each corner. `multiply(turn,
corners)` is 2×10 too, and each of its columns is one corner, moved. A
2×2 matrix times a 2×10 matrix: this is the layout the graphics pages
later in the course use, so that one multiplication moves every corner
of a shape.

That needs the shapes to fit. An $m \times n$ matrix times an $n \times
p$ matrix makes an $m \times p$ one: the two inner numbers, the columns
of the first and the rows of the second, must match. What happens if
they do not?

```python exec
id: every-corner-at-once-2
flat = [[1, 2, 3], [4, 5, 6]]
multiply(turn, flat)
multiply(flat, turn)
```

The first works: 2×2 times 2×3 makes 2×3. The second, 2×3 times 2×2,
stops with your `ValueError`: a row of `flat` has three numbers, and a
column of `turn` has two. Without the length check in `dot`, `zip` would
have paired the first two numbers of each row, and quietly thrown the
third away.

## The matrix that does nothing

Which matrix leaves every point where it is? It must send "right" to
$(1, 0)$ and "up" to $(0, 1)$, so those are its columns.

```python exec
id: the-matrix-that-does-nothing-1
I = [[1, 0], [0, 1]]
print(multiply(I, turn) == turn, multiply(turn, I) == turn)
print(transform_all(I, F) == F)
```

This is the *identity matrix*: ones down the diagonal from top left to
bottom right, zeros everywhere else, written $I$. Doing nothing and
then turning is turning, in either order. Every square size has one:
$I_3$ has three ones down its diagonal.

## Your world

A sequence of moves from the world you chose, made into one matrix.

<div class="dl-world" data-world="pixel-art">

On the practice page for the first page, transposing and then mirroring
a grid turned it a quarter. Here are the same two flips as matrices on
points: `swap` swaps x and y, and `mirror` mirrors left to right. What
single matrix is "swap, then mirror"? And "mirror, then swap"?

```python exec
id: multiply-your-world--pixel-art
swap = [[0, 1], [1, 0]]
mirror = [[-1, 0], [0, 1]]
```

```hint
"swap, then mirror" is `multiply(mirror, swap)`: the move that happens
first goes on the right. Read the columns of the answer to name it.
```

```solution
{{include: setup/matrices/transform.py}}
{{include: setup/matrices/multiply.py}}

F = [(0, 0), (1, 0), (1, 2), (2, 2), (2, 3), (1, 3), (1, 4), (3, 4), (3, 5), (0, 5)]
swap = [[0, 1], [1, 0]]
mirror = [[-1, 0], [0, 1]]
print(multiply(mirror, swap), multiply(swap, mirror))
draw_shapes([F, transform_all(multiply(mirror, swap), F)])
---
`[[0, -1], [1, 0]]`, the quarter turn anticlockwise, and `[[0, 1], [-1,
0]]`, the quarter turn clockwise. Two flips make a turn, and the order
decides its direction. (On the grid, the turn looked clockwise, because
a grid counts its rows downwards and points count upwards.)
```

</div>

<div class="dl-world" data-world="starships">

A ship docks in three moves: it turns 90°, shrinks to half size as it
flies off, and leans for speed with a shear. Can you make the one matrix
for all three, in that order, and check it on the ship?

```python exec
id: multiply-your-world--starships
ship = [(0, 4), (1, 1), (2, -1), (1, -0.5), (-1, -0.5), (-2, -1), (-1, 1)]
turn = [[0, -1], [1, 0]]
shrink = [[0.5, 0], [0, 0.5]]
lean = [[1, 0.3], [0, 1]]
```

```hint
The first move goes on the right: `multiply(lean, multiply(shrink,
turn))`. Check it against `transform_all` applied three times.
```

```solution
{{include: setup/matrices/transform.py}}
{{include: setup/matrices/multiply.py}}

ship = [(0, 4), (1, 1), (2, -1), (1, -0.5), (-1, -0.5), (-2, -1), (-1, 1)]
turn = [[0, -1], [1, 0]]
shrink = [[0.5, 0], [0, 0.5]]
lean = [[1, 0.3], [0, 1]]

all_three = multiply(lean, multiply(shrink, turn))
print(all_three)
one_by_one = transform_all(lean, transform_all(shrink, transform_all(turn, ship)))
print(transform_all(all_three, ship) == one_by_one)
draw_shapes([ship, one_by_one])
---
`[[0.15, -0.5], [0.5, 0.0]]`, and the two ways agree. Three moves, four
numbers. A game with a thousand ships can work out each ship's matrix
once and move all its corners with it, however many moves went into it.
```

</div>

<div class="dl-world" data-world="space-scenes">

The sky turns about 15° an hour. Multiply the one-hour turn by itself
six times: is the result the six-hour turn, a quarter turn?

```python exec
id: multiply-your-world--space-scenes
import math


def turn_by(degrees):
    """The matrix that turns anticlockwise by this many degrees."""
    angle = math.radians(degrees)
    return [[math.cos(angle), -math.sin(angle)],
            [math.sin(angle), math.cos(angle)]]


one_hour = turn_by(15)
```

```hint
Start from the identity, `[[1, 0], [0, 1]]`, and multiply by `one_hour`
six times in a loop. Round the entries to see them clearly.
```

```solution
{{include: setup/matrices/multiply.py}}

import math


def turn_by(degrees):
    """The matrix that turns anticlockwise by this many degrees."""
    angle = math.radians(degrees)
    return [[math.cos(angle), -math.sin(angle)],
            [math.sin(angle), math.cos(angle)]]


one_hour = turn_by(15)
six_hours = [[1, 0], [0, 1]]
for hour in range(6):
    six_hours = multiply(one_hour, six_hours)
print([[round(value, 6) for value in row] for row in six_hours])
---
`[[0.0, -1.0], [1.0, 0.0]]`, the quarter turn, up to rounding. Turning
by 15° six times is turning by 90°: for turns, multiplying the matrices
adds the angles. So two turns can be done in either order, since 15 + 90
and 90 + 15 are the same turn: one of the few pairs of moves where the
order does not matter.
```

</div>

## Looking back

On this page the rule for multiplying came out of doing one move after
another. Can you say, in your own words, why an entry of $AB$ is a row
of $A$ with a column of $B$, and not a row with a row?

A challenge: the shear `[[1, 1], [0, 1]]` leans the F. Multiply it by
itself: what does `multiply(shear, shear)` do? And the shear ten times?
Predict each before you run it.

```python challenge
def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def multiply(a, b):
    columns = [[row[j] for row in b] for j in range(len(b[0]))]
    return [[dot(row, column) for column in columns] for row in a]


shear = [[1, 1], [0, 1]]
print(multiply(shear, shear))
```

The next page, [Undoing it](tutorial:undoing-it), asks the question
every move raises: can it be taken back?

## Where to read more

Grant Sanderson (3Blue1Brown) (2016). *Matrix multiplication as
composition: Chapter 4, Essence of linear algebra.*
<https://www.youtube.com/watch?v=XkY2DOUCWMU>. Multiplying two matrices
means doing one move after another, shown with the same shear and turn
as this page. Ten minutes.

Grant Sanderson (3Blue1Brown) (2017). *But What Is a Neural Network? |
Deep Learning, Chapter 1.* <https://www.youtube.com/watch?v=aircAruvnKk>.
A forward pass through a network is the matrix multiplication from this
page, applied over and over.

Strang, G. (2016). *Introduction to Linear Algebra* (5th ed.).
Wellesley-Cambridge Press. The standard textbook, for the proofs behind
why the rule works the way it does.
