---
title: "Solving Systems"
slug: solving-systems
module: computational-methods
module_title: "Computational Methods"
year: "2026-2027"
series: matrices
version: 2026.08.24.1
covers:
  a-system-you-can-already-solve:
    touches: [CMPS-LO4]
  three-unknowns-row-by-row:
    covers: [CMPS-LO4]
    touches: [MIT-1.12]
  reading-off-the-answer:
    covers: [CMPS-LO4]
  checking-your-work:
    covers: [CMPS-LO4]
---

# Solving Systems

Two unknowns, solved by substitution, is something you have done since long
before this series started. This tutorial does two things: shows that the
inverse from the last tutorial gets the same answer a different way, and then
scales the method up to three unknowns and beyond — where writing down an
inverse formula the way we did for 2×2 stops being practical, and something
else has to take over.

## A System You Can Already Solve

$$\begin{cases} 2x + 3y = 7 \\ x - y = 1 \end{cases}$$

As a matrix equation, this is $A\mathbf{x} = \mathbf{b}$:

```python exec
id: a-system-you-can-already-solve-1
def det2(M):
    return M[0][0] * M[1][1] - M[0][1] * M[1][0]

def inverse(M):
    d = det2(M)
    a, b = M[0]
    c, e = M[1]
    return [[e / d, -b / d], [-c / d, a / d]]

def dot(a, b):
    return sum(x * y for x, y in zip(a, b))

def transpose(m):
    rows, cols = len(m), len(m[0])
    return [[m[r][c] for r in range(rows)] for c in range(cols)]

def multiply(a, b):
    bt = transpose(b)
    return [[dot(row, col) for col in bt] for row in a]

A = [[2, 3], [1, -1]]
b = [[7], [1]]
x = multiply(inverse(A), b)
print(x)
```

`x = 2, y = 1` — solve the same system by substitution, the way you learned
long before this series, and you should land on exactly the same pair of
numbers.

### Your turn

Confirm it: solve $2x + 3y = 7$ and $x - y = 1$ by substitution, on paper,
and check that it agrees with the cell above.

```python exec
id: a-system-you-can-already-solve-2
```

## Three Unknowns, Row by Row

$$\begin{cases} x + y + z = 6 \\ 2x - y + z = 3 \\ x + 2y - z = 2 \end{cases}$$

A third unknown means a third column, and the 2×2 inverse formula from the
last tutorial has nothing to say about a 3×3 matrix — there is a version of
it, but it gets complicated fast. *Gaussian elimination* sidesteps the
question entirely: rather than inverting anything, it simplifies the system
itself, one row operation at a time, until the answer can be read straight
off.

Written as an *augmented matrix* — the coefficients, with the right-hand side
tacked on as one more column — the system above is:

```python exec
id: three-unknowns-row-by-row-1
M = [[1, 1, 1, 6], [2, -1, 1, 3], [1, 2, -1, 2]]
for row in M:
    print(row)
```

Three legal moves on a matrix like this leave its solution unchanged:
swapping two rows, scaling a row by a non-zero number, and replacing a row
with itself plus a multiple of another row. The goal is to use them to get
zeros into the bottom-left corner, one column at a time.

```python exec
id: three-unknowns-row-by-row-2
M[1] = [M[1][k] - 2 * M[0][k] for k in range(4)]
print("R2 = R2 - 2*R1:", M[1])

M[2] = [M[2][k] - 1 * M[0][k] for k in range(4)]
print("R3 = R3 - R1:", M[2])
```

Both rows now start with 0 — $x$ has been eliminated from them. One column
of zeros to go: use row 2 to clear the $y$ out of row 3 as well.

```python exec
id: three-unknowns-row-by-row-3
M[2] = [3 * v for v in M[2]]
print("R3 = 3*R3:", M[2])

M[2] = [M[2][k] + M[1][k] for k in range(4)]
print("R3 = R3 + R2:", M[2])
```

Print `M` now. Every row starts with more zeros than the one above it — a
staircase, called *row echelon form*.

```python exec
id: three-unknowns-row-by-row-4
for row in M:
    print(row)
```

## Reading Off the Answer

The last row now says one thing about one unknown: $-7z = -21$.

### Your turn

Work back up the staircase. Solve the last row for $z$. Substitute that into
row 2, which now only has $y$ and $z$ in it, and solve for $y$. Substitute
both into row 1 and solve for $x$.

```python exec
id: reading-off-the-answer-1
hint: Row 2 is -3y - z = -9. Once you know z, that's one equation in one unknown.
# z, then y, then x
```

```python exec
id: reading-off-the-answer-2
check([x, y, z], [1, 2, 3])
```

## Checking Your Work

The real test is not whether the elimination steps look right — it is
whether $x$, $y$, $z$ actually satisfy the *original* three equations, before
any row operation touched them.

### Your turn

Substitute your answer into all three of the original equations —
$x+y+z$, $2x-y+z$, and $x+2y-z$ — and confirm each gives the right-hand side
it is supposed to: 6, 3, and 2.

```python exec
id: checking-your-work-1
```

This is the same technique that would handle four unknowns, or forty — the
row operations do not care how many columns are in front of the one being
cleared. That scalability is the whole reason this is the method computers
actually use, in preference to computing an inverse: an inverse for a large
matrix is expensive to compute and can amplify rounding error, and
elimination sidesteps both problems by never forming one at all.

## Reflection

Two routes to the same answer for two unknowns — inverse and elimination —
and only one route once a third unknown showed up, because the other route
had already run out of road. That is usually how it goes with a special-case
tool: useful exactly where it applies, and a general method waiting behind it
for everywhere else.

Which part of the elimination felt more like bookkeeping than mathematics —
tracking which row to subtract from which? That feeling is worth noticing:
it is exactly the part a computer does without getting tired or making an
arithmetic slip, which is why this, and not the 2×2 formula, is the version
that scales.

## Where to Read More

Grant Sanderson (3Blue1Brown) (2016). *Essence of Linear Algebra, Chapter 9:
Change of Basis.* <https://www.youtube.com/watch?v=P2LTAUO1TdA>. Not about
elimination directly, but the clearest available picture of what a system of
equations is actually asking, geometrically.

Kalid Azad (BetterExplained). *Linear Algebra Guide.*
<https://betterexplained.com/articles/linear-algebra-guide/>. An intuition-first
companion to the mechanical row operations in this tutorial.

Strang, G. (2016). *Introduction to Linear Algebra* (5th ed.).
Wellesley-Cambridge Press. Chapter 2 covers Gaussian elimination as the
central algorithm of the whole subject, which by the end of this series is a
fair description of why it is here.
