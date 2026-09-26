---
title: "Systems of equations: solving them with matrices"
year: "2026-2027"
version: 2026.09.25.1
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

# Systems of equations: solving them with matrices

A *system of equations* is a set of equations that must all be true at
the same time, for the same unknowns. You may have solved systems with
two unknowns at school, by substitution.

On this page we:

- solve a system with two unknowns using the inverse from
  [Inverse matrices: undoing a transformation](tutorial:undoing-it), and
  see that it gives the same answer as substitution
- solve a system with three unknowns, one row at a time
- check an answer against the original equations

Why do we need a second method? For a 2×2 matrix, we could write down a
formula for the inverse. With three unknowns or more, writing down an
inverse formula stops being practical, and we need something else.

## A system you can already solve

Here is a system with two unknowns, $x$ and $y$:

$$\begin{cases} 2x + 3y = 7 \\ x - y = 1 \end{cases}$$

We can write it as one matrix equation, $A\mathbf{x} = \mathbf{b}$:

- $A$ holds the numbers in front of the unknowns, the *coefficients*
- $\mathbf{x}$ holds the unknowns, $x$ and $y$
- $\mathbf{b}$ holds the numbers on the right-hand side

To find $\mathbf{x}$, we multiply $\mathbf{b}$ by the inverse of $A$:
$\mathbf{x} = A^{-1}\mathbf{b}$.

```python exec
id: a-system-you-can-already-solve-1
def det2(M):
    return M[0][0] * M[1][1] - M[0][1] * M[1][0]

def inverse(M):
    d = det2(M)
    a, b = M[0]
    c, e = M[1]  # e stands in for the formula's own d, already taken by the determinant above
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

The cell prints `[[2.0], [1.0]]`, a column. It says that $x = 2$ and
$y = 1$.

### Your turn

Can you confirm it?

1. On paper, solve $2x + 3y = 7$ and $x - y = 1$ by substitution.
2. Do you get the same pair of numbers as the cell above?

```python exec
id: a-system-you-can-already-solve-2
```

## Three unknowns, row by row

Here is a system with three unknowns:

$$\begin{cases} x + y + z = 6 \\ 2x - y + z = 3 \\ x + 2y - z = 2 \end{cases}$$

A third unknown means a third column. The 2×2 inverse formula from the
last page does not work for a 3×3 matrix. There is a 3×3 version of it,
but it gets complicated fast.

*Gaussian elimination* is a method that avoids inverses completely. It
simplifies the system itself, one step at a time, until we can read the
answer straight off.

First we write the system as an *augmented matrix*. An augmented matrix
holds the coefficients, with the right-hand sides added as one more
column:

```python exec
id: three-unknowns-row-by-row-1
M = [[1, 1, 1, 6], [2, -1, 1, 3], [1, 2, -1, 2]]
for row in M:
    print(row)
```

There are three *row operations*. A row operation is a change to the
matrix that leaves the solution the same:

1. swap two rows
2. multiply a row by a number that is not zero
3. replace a row with itself plus a multiple of another row

Our goal is to use these moves to put zeros into the bottom-left corner,
one column at a time.

The cell below uses the third move twice. It takes 2 × row 1 away from
row 2, and row 1 away from row 3. Each line uses a list comprehension,
from [Lists: keeping many values in order](tutorial:lists-and-sequences),
to work out all four numbers in the new row at once. What will the first
number in each new row be?

```python exec
id: three-unknowns-row-by-row-2
row1 = M[0]
row2 = [M[1][k] - 2 * row1[k] for k in range(4)]
print("row 2 - 2 * row 1:", row2)

row3 = [M[2][k] - 1 * row1[k] for k in range(4)]
print("row 3 - row 1:    ", row3)
```

Both new rows start with 0. We have removed $x$ from them.

Each step gets a new name, and `M` itself never changes. That is on
purpose. If the cell had changed `M`, running it a second time would
take 2 × row 1 away again, from a row that had already lost it once.

One more zero to go. Next, we use row 2 to remove the $y$ from row 3.
Row 3 has $1$ in front of $y$ and row 2 has $-3$. So we first multiply
row 3 by 3, and then add row 2.

```python exec
id: three-unknowns-row-by-row-3
row3_tripled = [3 * v for v in row3]
print("3 * row 3:        ", row3_tripled)

row3_last = [row3_tripled[k] + row2[k] for k in range(4)]
print("that, plus row 2: ", row3_last)
```

Now put the three rows together. What shape do the zeros make?

```python exec
id: three-unknowns-row-by-row-4
for row in [row1, row2, row3_last]:
    print(row)
```

Each row starts with more zeros than the row above it. The zeros make a
staircase. A matrix in this shape is in *row echelon form*.

## Reading off the answer

The last row now says one thing about one unknown: $-7z = -21$.

### Your turn

How would you work back up the staircase?

1. Solve the last row for $z$.
2. Row 2 now has only $y$ and $z$ in it. Put your $z$ into row 2, and
   solve for $y$.
3. Put $y$ and $z$ into row 1, and solve for $x$.

```python exec
id: reading-off-the-answer-1
hint: Row 2 is -3y - z = -9. Once you know z, that's one equation in one unknown.
# z, then y, then x
```

```python exec
id: reading-off-the-answer-2
check([x, y, z], [1, 2, 3])
```

## Checking your work

The elimination steps may look right, but that is not the real test.
The real test is this: do $x$, $y$ and $z$ make the original three
equations true? We mean the equations as they were before any row
operation changed them.

### Your turn

1. Put your answer into each of the three original left-hand sides:
   $x+y+z$, $2x-y+z$ and $x+2y-z$.
2. Do you get the right-hand sides, 6, 3 and 2?

```python exec
id: checking-your-work-1
```

The same method works for four unknowns, or forty. A row operation does
not care how many columns come before the one we are clearing.

This is the main reason computers solve systems with a form of
elimination, and do not work out an inverse. For a large matrix, an
inverse takes a lot of work to compute, and it can make rounding errors
worse. Elimination never forms an inverse, so it avoids both problems.

## Reflection

With two unknowns, we had two routes to the same answer: the inverse
and elimination. When a third unknown came in, we had only one route,
because the 2×2 inverse formula no longer worked.

This often happens with a tool made for a special case. It is useful
where it applies, and a general method is needed everywhere else.

Did some of the elimination feel more like bookkeeping than
mathematics, such as keeping track of which row to subtract from which?
That feeling is worth noticing. That part is exactly what a computer
does without getting tired or making an arithmetic mistake. It is why
elimination, and not the 2×2 formula, is the version that works at any
size.

## Where to Read More

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
