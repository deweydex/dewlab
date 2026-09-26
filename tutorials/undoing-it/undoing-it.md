---
title: "Inverse matrices: undoing a transformation"
year: "2026-2027"
version: 2026.09.26.2
worlds:
  starships: Starships, and the structures they are built from.
  space-scenes: Stars, planets and the paths they take across the sky.
  pixel-art: Pictures made of small squares, the way a screen draws them.
covers:
  measuring-the-f:
    touches: [CMPS-LO4]
  one-number-from-four:
    touches: [CMPS-LO4]
  when-the-f-collapses:
    touches: [CMPS-LO4]
  undoing-a-transformation:
    covers: [CMPS-LO4]
  which-ones-can-be-undone:
    covers: [CMPS-LO4]
---

# Inverse matrices: undoing a transformation

A quarter turn anticlockwise moved the F on the last two pages. Which
matrix would turn it back?

```python exec
id: undoing-it-opening
F = [(0, 0), (1, 0), (1, 2), (2, 2), (2, 3), (1, 3), (1, 4), (3, 4), (3, 5), (0, 5)]
turn = [[0, -1], [1, 0]]
back = [[1, 0], [0, 1]]      # change this to the matrix that turns it back

turned = transform_all(turn, F)
print(transform_all(back, turned) == F)
```

```hint
Turning back is a quarter turn clockwise. Where does that send "right",
$(1, 0)$, and "up", $(0, 1)$? Those are its columns.
```

`[[0, 1], [-1, 0]]` turns it back: "right" goes to "down", $(0, -1)$,
and "up" goes to "right". Doing the turn and then the turn back is doing
nothing, so `multiply(back, turn)` is the identity. A matrix that undoes
another is its *inverse*. Every move so far has felt as if it could be
undone. Can every one? This page finds a single number that says.

## Measuring the F

Here is a function that measures the area inside a shape from its
corners, with the *shoelace formula*: for each pair of neighbouring
corners, cross-multiply, $x_1 y_2 - x_2 y_1$; add them all up; halve the
total. The total keeps its sign. It is positive when the corners go
round anticlockwise, as the F's do, and negative when they go round
clockwise.

```python exec
id: measuring-the-f-1
def area(shape):
    """The area inside shape, positive if its corners go round anticlockwise."""
    total = 0
    for i in range(len(shape)):
        x1, y1 = shape[i]
        x2, y2 = shape[(i + 1) % len(shape)]
        total = total + x1 * y2 - x2 * y1
    return total / 2


print("the F:", area(F))
```

The F covers 8 squares: a stem of 5, a top arm of 2, a middle arm of 1.
`(i + 1) % len(shape)` is the next corner, going back to the first after
the last. Now measure the F after five moves. Before you run it, guess
each one: which grow, which shrink, and which stay 8?

```python exec
id: measuring-the-f-2
moves = {
    "stretch": [[2, 0], [0, 1]],
    "shear": [[1, 1], [0, 1]],
    "turn": [[0, -1], [1, 0]],
    "flip": [[1, 0], [0, -1]],
    "mix": [[2, 1], [1, 3]],
}
for name in moves:
    after = area(transform_all(moves[name], F))
    print(name, after, "  times", after / area(F))
```

```predict
What will the flipped F's area be?

- 8
  - A flip does not change the size.
- -8
  - The corners now go round the other way.
- 0
  - A flip turns the F over, flat.
```

The stretch doubles the area, the shear and the turn leave it at 8, and
the mix multiplies it by 5. The flip gives $-8$: the same size, but its
corners now go round clockwise, because the F has been turned over like
a mirror image. The sign is not a mistake to hide; it says the picture
has been flipped.

## One number from four

Each move multiplies the area by a factor: 2, 1, 1, $-1$ and 5. Can the
factor be worked out from the four numbers of the matrix, without
drawing anything? Here they are side by side.

| Move | $a$ | $b$ | $c$ | $d$ | factor |
|---|---|---|---|---|---|
| stretch | 2 | 0 | 0 | 1 | 2 |
| shear | 1 | 1 | 0 | 1 | 1 |
| turn | 0 | $-1$ | 1 | 0 | 1 |
| flip | 1 | 0 | 0 | $-1$ | $-1$ |
| mix | 2 | 1 | 1 | 3 | 5 |

A first guess is $a \times d$, the two numbers on the diagonal. It works
for the stretch, the shear and the flip. The turn breaks it: $0 \times 0
= 0$, but the turned F still covers 8 squares. And the mix: $2 \times 3
= 6$, but the factor is 5. Something with $b$ and $c$ in it is missing,
and it is 1 in both cases: for the turn, $b \times c = -1$, and for the
mix, $b \times c = 1$. Take it away:

$$ad - bc$$

For the turn, $0 - (-1) = 1$; for the mix, $6 - 1 = 5$. This number is
the *determinant* of the matrix, written $\det$: the factor by which the
matrix multiplies every area, with a minus sign when it flips the
picture over. Can you write `det(m)`? It comes with you, with `inverse`
below.

```python exec
id: matrix-det-inverse
toolkit: yes
def det(m):
    """The determinant of the 2x2 matrix m: ad - bc."""
    ...


def inverse(m):
    """The matrix that undoes the 2x2 matrix m.

    Raises ValueError if m cannot be undone.
    """
    ...
```

```python toolkit-reference
for: matrix-det-inverse
def det(m):
    """The determinant of the 2x2 matrix m: ad - bc."""
    return m[0][0] * m[1][1] - m[0][1] * m[1][0]


def inverse(m):
    """The matrix that undoes the 2x2 matrix m.

    Raises ValueError if m cannot be undone.
    """
    d = det(m)
    if d == 0:
        raise ValueError("this matrix has determinant 0, so it cannot be undone")
    return [[m[1][1] / d, -m[0][1] / d], [-m[1][0] / d, m[0][0] / d]]
```

Write `det` first; `inverse` comes in a later section.

```inputs
det([[2, 0], [0, 1]])
det([[0, -1], [1, 0]])
det([[2, 1], [1, 3]])
det([[1, 0], [0, -1]])
```

```hint
`m[0][0]` is $a$, `m[0][1]` is $b$, `m[1][0]` is $c$ and `m[1][1]` is
$d$.
```

```solution
def det(m):
    """The determinant of the 2x2 matrix m: ad - bc."""
    a, b = m[0]
    c, d = m[1]
    return a * d - b * c


def inverse(m):
    """The matrix that undoes the 2x2 matrix m.

    Raises ValueError if m cannot be undone.
    """
    d = det(m)
    if d == 0:
        raise ValueError("this matrix has determinant 0, so it cannot be undone")
    return [[m[1][1] / d, -m[0][1] / d], [-m[1][0] / d, m[0][0] / d]]
---
`a, b = m[0]` takes the first row apart into two names, which makes the
formula read like the maths.
```

The shear changed the F's shape more than any move in the gallery, and
it did not change its area at all: its determinant is $1 \times 1 - 1
\times 0 = 1$. The picture alone does not make that obvious; the number
says it at once.

## When the F collapses

What happens when the determinant is 0? This matrix has $\det = 2 \times
2 - 4 \times 1 = 0$.

```python exec
id: when-the-f-collapses-1
singular = [[2, 4], [1, 2]]
collapsed = transform_all(singular, F)
print(collapsed[:4])
print("area:", area(collapsed))
draw_shapes([F, collapsed])
```

Every corner lands on one straight line through $(0, 0)$, the line $y =
x / 2$. The F has no width left at all. A matrix with determinant 0 is
*singular*: it squashes the whole plane onto a line, or to a single
point.

## Undoing a transformation

The *inverse* of a matrix $A$, written $A^{-1}$, is the matrix that
undoes it: $A^{-1} A = I$. For a 2×2 matrix there is a formula:

$$A^{-1} = \frac{1}{\det(A)} \begin{bmatrix} d & -b \\ -c & a \end{bmatrix}$$

Swap $a$ and $d$, change the signs of $b$ and $c$, and divide everything
by the determinant. The determinant is under the fraction line, so when
it is 0, there is no inverse. The algebra says what the collapsed F
showed: once a picture is flat, there is no way to get back the width it
lost, because many different pictures flatten to the same line.

Now write `inverse` in the toolkit cell above, using `det`, and run it
again. Then check it here: does the inverse of the turn turn the F back?

```python exec
id: undoing-a-transformation-1
print(inverse(turn))
print(multiply(inverse(turn), turn))
print(transform_all(inverse(turn), turned) == F)
```

The inverse of the turn is the turn back, `[[0, 1], [-1, 0]]`, the
answer to the opening question, found by a formula this time. The
entries come out as floats, `0.0` and `1.0`, because of the division.

```python exec
id: undoing-a-transformation-2
inverse(singular)
```

This cell is meant to fail, with your own `ValueError`: a determinant of
0 has no inverse.

## Which ones can be undone?

Five matrices. For each, work out the determinant in your head, and
decide whether it can be undone. Then run the cell.

```python exec
id: which-ones-can-be-undone-1
candidates = {
    "M1": [[2, 1], [1, 1]],
    "M2": [[1, 2], [2, 4]],
    "M3": [[3, 0], [0, 0]],
    "M4": [[0, -1], [1, 0]],
    "M5": [[1, 0.5], [2, 1]],
}
for name in candidates:
    print(name, "determinant", det(candidates[name]))
```

```question
id: which-can-be-undone
type: fill-in-the-blank

- M2, `[[1, 2], [2, 4]]`, {cannot|can} be undone: its second column is twice its first.
- M3, `[[3, 0], [0, 0]]`, {cannot|can} be undone: it squashes every point onto the x axis.
- M5, `[[1, 0.5], [2, 1]]`, {cannot|can} be undone: $1 \times 1 - 0.5 \times 2 = 0$.
```

M1 and M4 can be undone; M2, M3 and M5 cannot. When one column is a
multiple of the other, "right" and "up" land on the same line, and so
does everything built from them: the determinant is 0.

## Your world

Undoing a move in the world you chose, or finding one that cannot be
undone.

<div class="dl-world" data-world="starships">

The ship's autopilot records one matrix for a whole manoeuvre: a turn,
a shrink and a lean, `[[0.15, -0.5], [0.5, 0.0]]`. To fly home, it needs
the matrix that undoes all three. Can you find it, and check that it
brings the ship back?

```python exec
id: undoing-your-world--starships
ship = [(0, 4), (1, 1), (2, -1), (1, -0.5), (-1, -0.5), (-2, -1), (-1, 1)]
manoeuvre = [[0.15, -0.5], [0.5, 0.0]]
away = transform_all(manoeuvre, ship)
```

```hint
`inverse(manoeuvre)`. Moving a point there and back will leave tiny
rounding errors, so round each coordinate before comparing.
```

```solution
{{include: setup/matrices/transform.py}}
{{include: setup/matrices/multiply.py}}
{{include: setup/matrices/inverse.py}}

ship = [(0, 4), (1, 1), (2, -1), (1, -0.5), (-1, -0.5), (-2, -1), (-1, 1)]
manoeuvre = [[0.15, -0.5], [0.5, 0.0]]
away = transform_all(manoeuvre, ship)

home = transform_all(inverse(manoeuvre), away)
print([(round(x, 9), round(y, 9)) for x, y in home] == ship)
print(det(manoeuvre))
---
It brings the ship home, up to rounding in the last few decimal places.
The determinant is 0.25: the manoeuvre shrank the ship to a quarter of
its area, a half in each direction, so the way home grows it four times.
```

</div>

<div class="dl-world" data-world="space-scenes">

A planet moves one step along its orbit with `step`, a turn of 30°. To
run the simulation backwards in time, each step needs undoing. Is the
inverse of a 30° turn a 30° turn the other way?

```python exec
id: undoing-your-world--space-scenes
import math


def turn_by(degrees):
    """The matrix that turns anticlockwise by this many degrees."""
    angle = math.radians(degrees)
    return [[math.cos(angle), -math.sin(angle)],
            [math.sin(angle), math.cos(angle)]]


step = turn_by(30)
```

```hint
Compare `inverse(step)` with `turn_by(-30)`, rounding each entry.
```

```solution
{{include: setup/matrices/inverse.py}}

import math


def turn_by(degrees):
    """The matrix that turns anticlockwise by this many degrees."""
    angle = math.radians(degrees)
    return [[math.cos(angle), -math.sin(angle)],
            [math.sin(angle), math.cos(angle)]]


step = turn_by(30)
backwards = inverse(step)
print([[round(v, 9) for v in row] for row in backwards])
print([[round(v, 9) for v in row] for row in turn_by(-30)])
print(round(det(step), 9))
---
The same matrix. A turn has determinant $\cos^2\theta + \sin^2\theta =
1$, so its inverse needs no dividing: it swaps the diagonal and changes
the signs of $\pm\sin\theta$, which is the turn by $-\theta$. A turn can
always be undone, since it never changes an area.
```

</div>

<div class="dl-world" data-world="pixel-art">

A game draws each sprite's shadow on the ground by pushing every point
down onto the line $y = 0$ and sliding it sideways by half its height:
`[[1, 0.5], [0, 0]]`. Can the sprite be rebuilt from its shadow?

```python exec
id: undoing-your-world--pixel-art
shadow_of = [[1, 0.5], [0, 0]]
shadow = transform_all(shadow_of, F)
draw_shapes([F, shadow])
print(det(shadow_of))
```

```hint
What is the determinant? And look at the shadow: two different corners
of the F, $(1, 2)$ and $(2, 0)$, land on the same point. Can a rebuild
know which one it came from?
```

```solution
{{include: setup/matrices/transform.py}}
{{include: setup/matrices/inverse.py}}

F = [(0, 0), (1, 0), (1, 2), (2, 2), (2, 3), (1, 3), (1, 4), (3, 4), (3, 5), (0, 5)]
shadow_of = [[1, 0.5], [0, 0]]
print(det(shadow_of))
print(transform(shadow_of, (1, 2)), transform(shadow_of, (2, 0)))
---
No: the determinant is 0, and the shadow lies flat on the line $y = 0$.
$(1, 2)$ and $(2, 0)$ both land on $(2, 0)$, so from the shadow alone
there is no telling which corner made it. A shadow keeps the width and
loses the height, and nothing can bring it back.
```

</div>

## Looking back

The determinant of the turn was 1, and of the collapse 0. Can you say,
using the word "area", why a matrix with determinant 0 cannot be undone,
and one with determinant 1 always can?

A challenge: the determinant of a product. Pick two matrices, and
compare `det(multiply(A, B))` with `det(A) * det(B)`. What rule do you
find, and why does it make sense for areas?

```python challenge
def det(m):
    return m[0][0] * m[1][1] - m[0][1] * m[1][0]


def multiply(a, b):
    columns = [[row[j] for row in b] for j in range(len(b[0]))]
    return [[sum(x * y for x, y in zip(row, column)) for column in columns] for row in a]


A = [[2, 1], [1, 3]]
B = [[0, -1], [1, 0]]
print(det(multiply(A, B)), det(A), det(B))
```

The next page, [Solving systems](tutorial:solving-systems), uses the
same question from the other end: given where a point landed, where did
it start?

## Where to read more

Grant Sanderson (3Blue1Brown) (2016). *Essence of Linear Algebra, Chapter
6: The Determinant.* <https://www.youtube.com/watch?v=Ip3X9LOh2dk>. The
area argument on this page, animated, and taken into three dimensions.

Grant Sanderson (3Blue1Brown) (2016). *Essence of Linear Algebra, Chapter
7: Inverse Matrices, Column Space and Null Space.*
<https://www.youtube.com/watch?v=uQhTuRlWMxw>. Why a determinant of zero
is exactly when an inverse cannot exist, argued from the picture.

Strang, G. (2016). *Introduction to Linear Algebra* (5th ed.).
Wellesley-Cambridge Press. Chapter 5 covers determinants properly,
including the 3×3 and larger cases this page leaves out.

Looking Glass Universe (2018). *A simple condition for when the matrix
inverse exists.* <https://www.youtube.com/watch?v=ESKcF8XFzLM>. When can a
transformation be undone, and when does it lose something for ever? About
eighteen minutes.
