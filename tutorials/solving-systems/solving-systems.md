---
title: "Systems of equations: solving them with matrices"
year: "2026-2027"
version: 2026.09.26.2
worlds:
  photos: Photographs, and the filters that change them.
  starships: Starships, and the structures they are built from.
  space-scenes: Stars, planets and the paths they take across the sky.
covers:
  two-lines-that-cross:
    touches: [CMPS-LO4]
  lines-that-never-meet:
    covers: [CMPS-LO4]
  three-unknowns-row-by-row:
    covers: [CMPS-LO4]
    touches: [MIT-1.12]
  back-substitution:
    covers: [CMPS-LO4]
  elimination-for-any-size:
    covers: [CMPS-LO4]
    touches: [CMPS-LO1]
  checking-your-work:
    covers: [CMPS-LO4]
---

# Systems of equations: solving them with matrices

Here are two straight lines. Where do they cross?

```python exec
id: solving-systems-opening
import matplotlib.pyplot as plt

xs = [-1, 5]
plt.figure()
plt.plot(xs, [(7 - 2 * x) / 3 for x in xs], label="2x + 3y = 7")
plt.plot(xs, [x - 1 for x in xs], label="x - y = 1")
plt.axhline(0, color="grey", linewidth=0.5)
plt.axvline(0, color="grey", linewidth=0.5)
plt.gca().set_aspect("equal")
plt.legend()
```

Each line is an equation. The point where they cross makes both
equations true at once. A set of equations that must all be true at
the same time, for the same unknowns, is a *system of equations*.

On this page we:

- solve a system with two unknowns, using the inverse from the last page
- see why some systems have no solution, and some have too many
- solve a system with three unknowns, one row at a time
- write `eliminate`, which does that for any number of unknowns

## Two lines that cross

The lines seem to cross at $(2, 1)$. Here is the system:

$$\begin{cases} 2x + 3y = 7 \\ x - y = 1 \end{cases}$$

The left-hand sides are a matrix at work. Take $A = \begin{bmatrix} 2 & 3
\\ 1 & -1 \end{bmatrix}$. It moves the point $(x, y)$ to $(2x + 3y, x -
y)$. The numbers in $A$, in front of the unknowns, are the
*coefficients*. So the system asks which point $A$ moves to $(7, 1)$.
We write it as $A\mathbf{x} = \mathbf{b}$.

The last page ended with that question. Given where a point landed,
where did it start? Undo $A$, and move $(7, 1)$ back.

```python exec
id: two-lines-that-cross-1
A = [[2, 3], [1, -1]]
print(transform(inverse(A), (7, 1)))
```

It prints `(2.0, 1.0)`. So $x = 2$ and $y = 1$, and the picture agrees.
Put them back in to check: $2(2) + 3(1) = 7$, and $2 - 1 = 1$.

## Lines that never meet

Change the second equation to $4x + 6y = 5$.

```predict
How many points will the two lines share?

- One
  - Two different lines cross once.
- None
  - The lines might never meet.
- Infinitely many
  - The lines might be the same line.
```

```python exec
id: lines-that-never-meet-1
import matplotlib.pyplot as plt

xs = [-1, 5]
plt.figure()
plt.plot(xs, [(7 - 2 * x) / 3 for x in xs], label="2x + 3y = 7")
plt.plot(xs, [(5 - 4 * x) / 6 for x in xs], label="4x + 6y = 5")
plt.gca().set_aspect("equal")
plt.legend()

B = [[2, 3], [4, 6]]
print(det(B))
print(inverse(B))
```

The lines are parallel, so no point is on both, and the system has no
solution. `det(B)` is 0, and `inverse` raises your `ValueError`.

On the last page, a matrix with determinant 0 flattened the F onto a
line. $B$ does the same to the whole plane. It moves $(x, y)$ to $(2x +
3y, 4x + 6y)$, and the second number is always twice the first. So $B$
only ever lands on points like $(1, 2)$, $(3.5, 7)$ or $(7, 14)$.

- $(7, 5)$ is not on that line. No point lands there, so there is no
  solution.
- $(7, 14)$ is on the line. A whole line of points lands there, so
  there are infinitely many solutions. The two equations are then
  $2x + 3y = 7$ and $4x + 6y = 14$, which is the same line drawn twice.

A determinant of 0 always means one of these two cases. A determinant
that is not 0 means exactly one solution.

## Three unknowns, row by row

Here is a system with three unknowns:

$$\begin{cases} x + y + z = 6 \\ 2x - y + z = 3 \\ x + 2y - z = 2 \end{cases}$$

Each equation is now a flat surface in space, and we want the point
where all three meet. Our `inverse` only works for 2×2 matrices. There
is a 3×3 formula, but it is long, and for 4×4 it is longer still. So we
use a method that needs no inverse at all.

First, write the system as an *augmented matrix*. It holds the
coefficients, with the right-hand sides added as one more column.

```python exec
id: three-unknowns-row-by-row-1
M = [[1, 1, 1, 6], [2, -1, 1, 3], [1, 2, -1, 2]]
for row in M:
    print(row)
```

A *row operation* changes the rows but keeps the same solution. There
are three:

1. swap two rows
2. multiply a row by a number that is not 0
3. add a multiple of one row to another row

The plan is to put zeros in the bottom-left corner, one column at a
time. Then the last row has only one unknown in it.

The lines in the cell below do this, but they are shuffled.
Can you put them in an order that works? Run the cell as it is first,
and read the error.

```python exec
id: three-unknowns-row-by-row-2
row3 = [3 * row3[k] + row2[k] for k in range(4)]
row2 = [M[1][k] - 2 * M[0][k] for k in range(4)]
print(row1, row2, row3, sep="\n")
row3 = [M[2][k] - M[0][k] for k in range(4)]
row1 = M[0]
```

```hint
A line can only use a name that an earlier line made. `row3` is made
twice. Which of the two lines has to come first?
```

```solution
row1 = M[0]
row2 = [M[1][k] - 2 * M[0][k] for k in range(4)]
row3 = [M[2][k] - M[0][k] for k in range(4)]
row3 = [3 * row3[k] + row2[k] for k in range(4)]
print(row1, row2, row3, sep="\n")
---
Here is one answer. Yours may be different and work too. `row1` can go
anywhere before the `print`. The `row2` line subtracts 2 × row 1 from
row 2, and the first `row3` line subtracts row 1 from row 3. That clears
$x$ from both. Then row 3 has 1 in front of $y$ and row 2 has $-3$, so
3 × row 3 plus row 2 clears $y$ from row 3.
```

When the lines are in order, the cell prints:

```
[1, 1, 1, 6]
[0, -3, -1, -9]
[0, 0, -7, -21]
```

Each row starts with more zeros than the row above it. The zeros make a
staircase, and a matrix in this shape is in *row echelon form*.

Each line makes a new list, and `M` never changes. That is on purpose.
If a line changed `M`, running the cell a second time would subtract
2 × row 1 from a row that had already lost it once.

## Back substitution

The last row now has one unknown: $-7z = -21$. Start there, and climb
back up the staircase. This is *back substitution*.

1. Solve the last row for $z$.
2. Row 2 is $-3y - z = -9$. Put in your $z$, and solve for $y$.
3. Put $y$ and $z$ into row 1, and solve for $x$.

```python exec
id: back-substitution-1
# z, then y, then x
```

```inputs
z
y
x
```

```hint
Once you know $z$, row 2 is one equation in one unknown:
$-3y = -9 + z$.
```

```solution
z = -21 / -7
y = (-9 + z) / -3
x = 6 - y - z
print(x, y, z)
---
It prints `1.0 2.0 3.0`. Each row has one new unknown, because the row
below it has already been solved.
```

## Elimination for any size

Clearing the columns and then back substitution together make *Gaussian
elimination*. The steps are the same, whatever the size.

1. Look at column 0. Use row 0 to put a 0 in that column of every row
   below it.
2. Look at column 1. Use row 1 to put a 0 in that column of every row
   below it.
3. Continue until the last column before the right-hand sides.

To clear a row, subtract row `col` times a *factor*. The factor is the
number you want to clear, divided by the number on the staircase:
`rows[r][col] / rows[col][col]`.

One problem can happen. If the number on the staircase is 0, there is
nothing to divide by. Then swap in a lower row that has a number there.

Can you write `eliminate(M)`? It comes with you to the later pages.

```python exec
id: systems-eliminate
toolkit: yes
def eliminate(M):
    """The augmented matrix M in row echelon form, as a new list of rows.

    M is not changed.
    """
    rows = [list(row) for row in M]
    for col in range(len(rows)):
        # 1. If rows[col][col] is 0, swap in a lower row with a number there.
        # 2. Clear column col in every row below row col.
        ...
    return rows
```

```python toolkit-reference
for: systems-eliminate
def eliminate(M):
    """The augmented matrix M in row echelon form, as a new list of rows.

    M is not changed.
    """
    rows = [list(row) for row in M]
    n = len(rows)
    for col in range(n):
        pivot = col
        while pivot < n and rows[pivot][col] == 0:
            pivot = pivot + 1
        if pivot == n:
            continue
        rows[col], rows[pivot] = rows[pivot], rows[col]
        for r in range(col + 1, n):
            factor = rows[r][col] / rows[col][col]
            rows[r] = [a - factor * b for a, b in zip(rows[r], rows[col])]
    return rows
```

```inputs
eliminate([[1, 1, 1, 6], [2, -1, 1, 3], [1, 2, -1, 2]])
eliminate([[2, 3, 7], [1, -1, 1]])
eliminate([[0, 1, 2], [1, 1, 3]])
```

```hint
For step 2, loop `r` over the rows below: `range(col + 1, len(rows))`.
Find the factor, then make the new row with a comprehension:
`[a - factor * b for a, b in zip(rows[r], rows[col])]`. For step 1,
a `while` loop can move down the column until it finds a number that
is not 0.
```

```solution
def eliminate(M):
    """The augmented matrix M in row echelon form, as a new list of rows.

    M is not changed.
    """
    rows = [list(row) for row in M]
    n = len(rows)
    for col in range(n):
        pivot = col
        while pivot < n and rows[pivot][col] == 0:
            pivot = pivot + 1
        if pivot == n:
            continue
        rows[col], rows[pivot] = rows[pivot], rows[col]
        for r in range(col + 1, n):
            factor = rows[r][col] / rows[col][col]
            rows[r] = [a - factor * b for a, b in zip(rows[r], rows[col])]
    return rows


print(eliminate([[1, 1, 1, 6], [2, -1, 1, 3], [1, 2, -1, 2]]))
---
Here is one answer. Yours may be different and work too. The last row
is `[0.0, 0.0, -2.333…, -7.0]`, not `[0, 0, -7, -21]`. This loop divides
where the cell above multiplied by 3, so the row is a third as big. It
is the same equation, and it gives the same $z$. When a whole column is
0 below the staircase, `continue` moves to the next column.
```

The first line copies each row, so `eliminate` never changes `M`. With
`rows = M`, both names would point to the same list, as on
[Comprehensions, grids and aliasing](tutorial:comprehensions-and-grids).

Here is back substitution as a loop. It works from the last row up, and
`solve` runs both halves. It raises a `ValueError` when a number on the
staircase is 0, or so close to 0 that only rounding makes it different.
Then the system has no solution, or infinitely many.

```python exec
id: systems-solve
toolkit: yes
def back_substitute(E):
    """The unknowns of a system whose augmented matrix E is in row echelon form."""
    n = len(E)
    values = [0] * n
    for i in range(n - 1, -1, -1):
        if abs(E[i][i]) < 1e-12:
            raise ValueError("this system does not have exactly one solution")
        known = sum(E[i][j] * values[j] for j in range(i + 1, n))
        values[i] = (E[i][n] - known) / E[i][i]
    return values


def solve(M):
    """The solution of the system whose augmented matrix is M."""
    return back_substitute(eliminate(M))
```

```python exec
id: elimination-for-any-size-1
print(solve(M))
print(solve([[2, 3, 7], [1, -1, 1]]))
print(solve([[2, 3, 7], [4, 6, 5]]))
```

The first two lines print `[1.0, 2.0, 3.0]` and `[2.0, 1.0]`. The third
raises the `ValueError`, because those are the parallel lines.

## Checking your work

The real test of an answer is whether it makes the original equations
true. We mean the equations as they were before any row operation
changed them.

1. Put your answer into each of the three original left-hand sides:
   $x + y + z$, $2x - y + z$ and $x + 2y - z$.
2. Do you get the right-hand sides, 6, 3 and 2?

```python exec
id: checking-your-work-1
```

```solution
x, y, z = solve(M)
print(x + y + z, 2 * x - y + z, x + 2 * y - z)
---
It prints `6.0 3.0 2.0`. `multiply` does the same check in one line:
`multiply([[1, 1, 1], [2, -1, 1], [1, 2, -1]], [[x], [y], [z]])`.
```

The same method works for four unknowns, or forty. Computers solve
large systems with a form of elimination, not with an inverse. For a
large matrix, finding the inverse takes much more work, and it can make
rounding errors worse.

## Your world

A system of equations from the world you chose.

<div class="dl-world" data-world="photos">

A photo filter mixes the red, green and blue of every pixel. This one
warms the picture:

- new red is 1.2 × red + 0.1 × green
- new green is 0.1 × red + green + 0.1 × blue
- new blue is 0.1 × green + 0.8 × blue

After the filter, one pixel reads red 192, green 144 and blue 84. What
colour was it before?

```python exec
id: solving-your-world--photos
warm = [[1.2, 0.1, 0.0], [0.1, 1.0, 0.1], [0.0, 0.1, 0.8]]
after = [192, 144, 84]
```

```hint
Add `after` as a fourth column to each row of `warm`, then use `solve`.
Round each answer to a whole number.
```

```solution
{{include: setup/matrices/solve.py}}

warm = [[1.2, 0.1, 0.0], [0.1, 1.0, 0.1], [0.0, 0.1, 0.8]]
after = [192, 144, 84]
M = [warm[i] + [after[i]] for i in range(3)]
print([round(v) for v in solve(M)])
---
It prints `[150, 120, 90]`, a light brown. Undoing a filter means
solving one small system for each pixel. A photo with 1,000,000 pixels
needs 1,000,000 of them, all with the same coefficients.
```

</div>

<div class="dl-world" data-world="starships">

A ship has three thrusters. Each second of firing changes its sideways
speed, its forward speed and its spin:

- thruster 1: sideways 2, forward 0, spin 1
- thruster 2: sideways 0, forward 3, spin −1
- thruster 3: sideways 1, forward 1, spin 0

The pilot needs a change of sideways 4, forward 7 and spin −0.5. How
long should each thruster fire?

```python exec
id: solving-your-world--starships
thrusters = [(2, 0, 1), (0, 3, -1), (1, 1, 0)]
wanted = [4, 7, -0.5]
```

```hint
Each thruster is a column, as on
[what a matrix does to a picture](tutorial:what-a-matrix-does-to-a-picture).
Row 0 of the augmented matrix holds the three sideways numbers and then
the 4.
```

```solution
{{include: setup/matrices/solve.py}}

thrusters = [(2, 0, 1), (0, 3, -1), (1, 1, 0)]
wanted = [4, 7, -0.5]
M = [[t[i] for t in thrusters] + [wanted[i]] for i in range(3)]
print([round(v, 6) for v in solve(M)])
---
It prints `[1.5, 2.0, 1.0]`. Thruster 1 fires for 1.5 seconds,
thruster 2 for 2 and thruster 3 for 1. Check the spin:
$1.5 - 2 + 0 = -0.5$.
```

</div>

<div class="dl-world" data-world="space-scenes">

A comet is seen three times, at $(1, 3.5)$, $(3, 3.5)$ and $(5, 7.5)$.
Near the Sun, its path is close to a curve $y = ax^2 + bx + c$. Each
sighting gives one equation in $a$, $b$ and $c$. For example, the first
gives $a + b + c = 3.5$. Can you find the curve, and draw it through
the three points?

```python exec
id: solving-your-world--space-scenes
sightings = [(1, 3.5), (3, 3.5), (5, 7.5)]
```

```hint
The row for the sighting $(x, y)$ is `[x ** 2, x, 1, y]`.
```

```solution
{{include: setup/matrices/solve.py}}
import matplotlib.pyplot as plt

sightings = [(1, 3.5), (3, 3.5), (5, 7.5)]
M = [[x ** 2, x, 1, y] for x, y in sightings]
a, b, c = [round(v, 6) for v in solve(M)]
print(a, b, c)
xs = [i / 10 for i in range(0, 61)]
plt.figure()
plt.plot(xs, [a * x ** 2 + b * x + c for x in xs])
plt.plot([x for x, y in sightings], [y for x, y in sightings], "o")
---
It prints `0.5 -2.0 5.0`, so the curve is $y = 0.5x^2 - 2x + 5$.
Three points fix a curve of this kind, in the same way that two points
fix a straight line.
```

</div>

## Looking back

A system with two unknowns is two lines. Can you draw the three cases,
one solution, none and infinitely many, and say what the determinant
is in each?

A challenge: make a system with 10 unknowns, where you choose the
answer first. Pick 10 numbers, make random coefficients, and find each
right-hand side from your numbers. Does `solve` find your numbers
again?

```python challenge
import random


def eliminate(M):
    rows = [list(row) for row in M]
    n = len(rows)
    for col in range(n):
        pivot = col
        while pivot < n and rows[pivot][col] == 0:
            pivot = pivot + 1
        if pivot == n:
            continue
        rows[col], rows[pivot] = rows[pivot], rows[col]
        for r in range(col + 1, n):
            factor = rows[r][col] / rows[col][col]
            rows[r] = [a - factor * b for a, b in zip(rows[r], rows[col])]
    return rows


def solve(M):
    E = eliminate(M)
    n = len(E)
    values = [0] * n
    for i in range(n - 1, -1, -1):
        known = sum(E[i][j] * values[j] for j in range(i + 1, n))
        values[i] = (E[i][n] - known) / E[i][i]
    return values


answer = [random.randint(-5, 5) for i in range(10)]
coefficients = [[random.randint(-9, 9) for j in range(10)] for i in range(10)]
# Find each right-hand side from answer, build M, and solve it.
```

The next page, [Everything you built, in one line each](tutorial:matrices-in-numpy),
checks all of this against NumPy.

## Where to read more

Grant Sanderson (3Blue1Brown) (2016). *Essence of Linear Algebra, Chapter 7:
Inverse Matrices, Column Space and Null Space.*
<https://www.youtube.com/watch?v=uQhTuRlWMxw>. Not about elimination directly,
but the clearest picture there is of what a system of equations is asking,
geometrically, and of what goes wrong when the determinant is zero.

Kalid Azad (BetterExplained). *Linear Algebra Guide.*
<https://betterexplained.com/articles/linear-algebra-guide/>. An intuition-first
companion to the mechanical row operations in this tutorial.

Strang, G. (2016). *Introduction to Linear Algebra* (5th ed.).
Wellesley-Cambridge Press. Chapter 2 covers Gaussian elimination as the
central algorithm of the whole subject, which by the end of this series is a
fair description of why it is here.

Random Noise (2026). *Solving Lights Out Puzzles: Light Chasing vs Linear
Algebra.* <https://www.youtube.com/watch?v=rQtRK-AJOGg>. In the game
Lights Out, pressing a light switches it and its neighbours. This video
solves it two ways, and one of them is a system of equations. About ten
minutes.
