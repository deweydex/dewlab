---
title: "A Grid of Numbers"
slug: grid-of-numbers
module: computational-methods
module_title: "Computational Methods"
year: "2026-2027"
series: matrices
version: 2026.08.24.1
covers:
  nine-numbers-that-draw-a-picture:
    touches: [CMPS-LO1, MIT-6.3]
  two-grids-added-together:
    touches: [CMPS-LO4]
  scaling-and-the-shape-rule:
    touches: [CMPS-LO4]
  turning-it-sideways-the-transpose:
    touches: [CMPS-LO4]
---

# A Grid of Numbers

A spreadsheet is a grid of numbers. So is a small black-and-white image, a
table of exam results, and the weights inside a neural network. Once numbers
sit in a grid rather than a single row, a few new questions become possible —
how do you add two grids together, what does scaling one mean, and what
happens if you turn one sideways? Those questions are what this tutorial and
the four after it are about.

A grid of numbers, arranged in rows and columns, is called a *matrix*. We are
going to build one out of nothing but a plain Python list of lists, and do
every operation on it ourselves before any library does it for us. That is
slower than importing NumPy on the first line, and it is also the only way to
actually watch the arithmetic happen rather than trust that it did.

## Nine Numbers That Draw a Picture

Here is a small grid of numbers. Run it before reading any further.

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

Nine numbers, five rows of them, and a diamond appears. Each number stands for
how dark one square is — 0 is blank, 9 is solid — and `ramp` is just a string
being used as a lookup table from a number to a character. This is the same
idea behind every image on a screen: a grid of numbers, and a rule for turning
each number into something you can see.

`pixels` is our matrix. It has 5 *rows* and 5 *columns*, so we call it a 5×5
matrix — rows first, always. The number in row $i$ and column $j$ is usually
written $a_{ij}$, and in Python that is `pixels[i][j]`. Try reading off
`pixels[2][2]` below, the very centre of the diamond, and `pixels[0]`, the
whole first row.

```python exec
id: nine-numbers-that-draw-a-picture-2
print(pixels[2][2])
print(pixels[0])
```

### Your turn

What is `pixels[4][2]`, without running anything? Check your prediction, then
try `pixels[1][3]` as well.

```python exec
id: nine-numbers-that-draw-a-picture-3
hint: Row index first, then column — pixels[row][column].
```

## Two Grids, Added Together

A single picture is nice; two pictures you can combine is more interesting.
Adding two matrices together works exactly the way you might guess: add the
numbers that are in the same position.

$$\begin{bmatrix} a & b \\ c & d \end{bmatrix} + \begin{bmatrix} e & f \\ g & h \end{bmatrix} = \begin{bmatrix} a+e & b+f \\ c+g & d+h \end{bmatrix}$$

Here are three small matrices to work with for the rest of this section.

```python exec
id: two-grids-added-together-1
A = [[3, -1], [2, 4]]
B = [[1, 5], [-3, 2]]
C = [[0, 2], [1, -1]]
print("A =", A)
print("B =", B)
print("C =", C)
```

### Your turn

How might `add(a, b)` return the sum of two matrices of the same shape? A
nested loop — rows on the outside, columns on the inside — visits every
position exactly once.

```python exec
id: two-grids-added-together-2
hint: Two nested loops. The outer one picks a row index, the inner one a column index, and the result at [i][j] is a[i][j] + b[i][j].
# Your add(a, b)
```

Once `add` works, what is `A + B` by hand, and does your function agree? Try
`A + B + C` as well — you should be able to call `add` twice.

```python exec
id: two-grids-added-together-3
# Check add(A, B), and add(add(A, B), C)
```

Is `add(A, B)` the same as `add(B, A)`? Try it and see — addition of ordinary
numbers does not care about order, and it is worth checking whether matrices
inherit that.

```python exec
id: two-grids-added-together-4
# Compare add(A, B) with add(B, A)
```

## Scaling and the Shape Rule

Multiplying a matrix by a single number — a *scalar* — multiplies every entry
by it. $k\begin{bmatrix} a & b \\ c & d \end{bmatrix} = \begin{bmatrix} ka & kb \\ kc & kd \end{bmatrix}$.

### Your turn

Write `scale(k, m)`, and use it together with `add` (or a `subtract` you write
the same way) to work out `3A` and `2B - A` from the matrices above.

```python exec
id: scaling-and-the-shape-rule-1
hint: scale(k, m) is one nested loop, no addition needed — just k * m[i][j] at every position.
# Your scale(k, m)
```

```python exec
id: scaling-and-the-shape-rule-2
# 3A and 2B - A
```

Now try something that should not work. Here is a matrix with a different
shape from `A` entirely — one row instead of two.

```python exec
id: scaling-and-the-shape-rule-3
D = [[1, 2, 3]]
add(A, D)
```

This is meant to fail, so if you see a traceback, nothing is broken. What it
raises depends on how you wrote `add` — probably an `IndexError`, complaining
about a position partway through the loop that does not exist in `D`. That
error is truthful but not exactly helpful: it points at the *symptom*, deep
inside a loop, rather than the actual problem, which is that the two matrices
were never addable in the first place.

A matrix has a *shape* — its number of rows and columns — and addition is only
defined when both matrices have the same shape. Add one line to the top of
your `add` that checks `len(a) == len(b) and len(a[0]) == len(b[0])`, and
raises a `ValueError` with a message that says what actually went wrong if it
does not. Then `add(A, D)` fails immediately, with an error that tells you why
instead of where.

```python exec
id: scaling-and-the-shape-rule-4
hint: if not (len(a) == len(b) and len(a[0]) == len(b[0])): raise ValueError(...) — put it before the loops, not inside them.
# Your add(a, b), with a shape check
```

## Turning It Sideways: the Transpose

One more operation, and this one has no arithmetic in it at all — nothing is
added or multiplied, only rearranged.

```python exec
id: turning-it-sideways-the-transpose-1
def show_grid(m):
    for row in m:
        print(row)

M = [[1, 2, 3], [4, 5, 6]]
show_grid(M)
```

`M` is 2 rows by 3 columns. What would it look like with the rows and columns
swapped — the first *column* of `M` written out as the first *row*?

### Your turn

Write `transpose(m)`, which returns a new matrix where row $i$, column $j$
holds what used to be at row $j$, column $i$. Try it on `M` above, and check
the shape of the result — it should come out 3 rows by 2 columns, the other
way round from `M`.

```python exec
id: turning-it-sideways-the-transpose-2
hint: Build the result row by row, one row per column of m. The new row i is [row[i] for row in m].
# Your transpose(m)
```

This flip-the-shape operation is called the *transpose*, written $A^T$. A
matrix that is its own transpose — where swapping rows and columns changes
nothing — is called *symmetric*. Try your `transpose` on this one:

```python exec
id: turning-it-sideways-the-transpose-3
S = [[1, 4, 7], [4, 2, 5], [7, 5, 3]]
check(transpose(S), S)
```

## Reflection

Four operations now, all of them a handful of lines: add, scale, a shape
check that turns a confusing error into a clear one, and a transpose that
rearranges without any arithmetic at all. None of them needed a library —
which is worth noticing, because the next tutorial gets to the one matrix
operation that genuinely surprises people, and it is worth having built
everything up to it yourself first.

What surprised you about any of these? Was it obvious in advance that
`add(A, B)` would equal `add(B, A)`, or did you expect to have to check?

## Where to Read More

Grant Sanderson (3Blue1Brown) (2016). *Essence of Linear Algebra, Chapter 1:
Vectors, What Even Are They?*
<https://www.youtube.com/watch?v=fNk_zzaMoSs>. Matrices in this tutorial are
built from plain lists; this is the geometric picture underneath them, and the
series it opens is worth the whole hour.

Downey, A. B. (2015). *Think Python: How to Think Like a Computer Scientist*
(2nd ed.). Green Tea Press. <https://greenteapress.com/wp/think-python-2e/>.
Chapter 10 on lists is the Python half of what a matrix is built from here.

Python Software Foundation. *5. Data Structures — Nested List
Comprehensions.* <https://docs.python.org/3/tutorial/datastructures.html>.
The pattern behind every nested loop in this tutorial, spelled out as its own
topic.
