---
title: "Matrices: adding, scaling and transposing a grid of numbers"
year: "2026-2027"
version: 2026.09.26.1
covers:
  a-grid-that-draws-a-picture:
    touches: [CMPS-LO1, MIT-6.3]
  two-grids-added-together:
    touches: [CMPS-LO4]
  scaling-and-the-shape-rule:
    touches: [CMPS-LO4]
  turning-it-sideways-the-transpose:
    touches: [CMPS-LO4]
---

# Matrices: adding, scaling and transposing a grid of numbers

A spreadsheet is a grid of numbers. A small black-and-white image is a
grid of numbers too. So is a table of exam results, and so are the
weights inside a neural network.

When numbers sit in a grid, and not in a single row, we can ask some new
questions:

- How do you add two grids together?
- What does it mean to scale a grid?
- What happens if you turn a grid sideways?

This page and the five pages after it answer questions like these.

A *matrix* is a grid of numbers, arranged in rows and columns. We will
build matrices from plain Python lists of lists, and we will write every
operation ourselves before any library does it for us. A library such as
NumPy would be faster to use. Our own code is slower, but we can watch
the arithmetic happen, so we do not have to trust that it did.

On this page we:

- read a matrix, one number at a time
- add two matrices, and multiply a matrix by a number
- check that two matrices have the same shape before we add them
- turn a matrix sideways, with the transpose

## A grid that draws a picture

Here is a small grid of numbers. What do you think it will draw? Run it
to find out.

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

Five rows of numbers make a diamond. Each number says how dark one
square is: 0 is blank and 9 is solid. `ramp` is a string that we use as
a lookup table. `ramp[value]` turns a number into a character.

The last line builds the text for one row. The part inside the brackets,
`ramp[value] for value in row`, works like a list comprehension. It
makes one character for each number in the row. `"".join(...)` joins
those characters into a single string. Comprehensions are in
[Comprehensions, grids and aliasing](tutorial:comprehensions-and-grids).

Every image on a screen works in the same way. It is a grid of numbers,
with a rule that turns each number into something you can see.

`pixels` is our matrix. It has 5 *rows* and 5 *columns*, so we call it a
5×5 matrix. We always say the number of rows first.

In maths, the number in row $i$ and column $j$ is written $a_{ij}$. Maths
counts rows and columns from 1, so $a_{11}$ is the top-left number.
Python counts from 0, so the same number is `pixels[0][0]`. In Python,
the row index always comes first and the column index second:
`pixels[row][column]`.

The cell below reads two things: `pixels[2][2]`, the number in the
centre of the diamond, and `pixels[0]`, the whole first row. What do you
expect each one to print?

```python exec
id: nine-numbers-that-draw-a-picture-2
print(pixels[2][2])
print(pixels[0])
```

### Your turn

1. What is `pixels[4][2]`? Decide before you run anything.
2. Check your prediction in the cell below.
3. Then try `pixels[1][3]` as well.

```python exec
id: nine-numbers-that-draw-a-picture-3
hint: Row index first, then column — pixels[row][column].
```

## Two grids, added together

One picture is nice. Two pictures that we can combine are more
interesting. How would you add two matrices together?

*Matrix addition* works the way you might guess. We add the numbers that
are in the same position:

$$\begin{bmatrix} a & b \\ c & d \end{bmatrix} + \begin{bmatrix} e & f \\ g & h \end{bmatrix} = \begin{bmatrix} a+e & b+f \\ c+g & d+h \end{bmatrix}$$

Here are three small matrices. We will use them for the rest of this
section.

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

How might `add(a, b)` return the sum of two matrices of the same shape?

A nested loop visits every position exactly once. The outer loop visits
each row, and the inner loop visits each column.

```python exec
id: two-grids-added-together-2
expect: add([[1, 2], [3, 4]], [[10, 20], [30, 40]]) == [[11, 22], [33, 44]]
hint: Two nested loops. The outer one picks a row index, the inner one a column index, and the result at [i][j] is a[i][j] + b[i][j].
# Your add(a, b)
```

```hint
What does the last line of the error name? Is it a variable Python has
not met yet, an index past the end of a list, or something about the
shape of a line? Which line of your `add` does it point at? Before you
change that line, write down what you expected `a[0]` to be there. Is it
one number, or a whole row?
```

```hint
after: 10 errors
title: some steps
1. Start with an empty list, `result = []`.
2. For each row index `i`, build one new row, then append it to `result`.
3. Inside that, for each column index `j`, the new row gets `a[i][j] + b[i][j]`.
4. Return `result` after both loops have finished, not inside them.

**Think about:** why the inner loop's range comes from `len(a[0])` and the
outer one from `len(a)`.

**Try this next:** the same shape with subtraction, then with `max` of the
two entries.
```

When `add` works, try these:

1. Calculate `A + B` by hand.
2. Does `add(A, B)` agree with you?
3. Now find `A + B + C`. You can do this by calling `add` twice.

```python exec
id: two-grids-added-together-3
# Check add(A, B), and add(add(A, B), C)
```

For ordinary numbers, the order of addition does not matter: $3 + 5$ is
the same as $5 + 3$. Do matrices behave in the same way? Is `add(A, B)`
the same as `add(B, A)`? Try it and see.

```python exec
id: two-grids-added-together-4
# Compare add(A, B) with add(B, A)
```

## Scaling and the shape rule

A *scalar* is a single number, used together with a matrix. *Scalar
multiplication* multiplies every entry of a matrix by the same scalar:

$$k\begin{bmatrix} a & b \\ c & d \end{bmatrix} = \begin{bmatrix} ka & kb \\ kc & kd \end{bmatrix}$$

### Your turn

1. How might you write `scale(k, m)`? Write it in the first cell below.
2. Write a `subtract(a, b)` in the same way as `add`, if you want one.
3. In the second cell, use `scale` together with `add` or `subtract` to
   calculate `3A` and `2B - A`, with the matrices from above.

```python exec
id: scaling-and-the-shape-rule-1
expect: scale(2, [[1, 2], [3, 4]]) == [[2, 4], [6, 8]]
hint: scale(k, m) is one nested loop, no addition needed — just k * m[i][j] at every position.
# Your scale(k, m)
```

```hint
How is `scale` different from your `add`? How many matrices does it use,
and what happens at each position? If your `add` works, which of
its lines could you keep as they are, and which one line changes?
```

```python exec
id: scaling-and-the-shape-rule-2
# 3A and 2B - A
```

Now let's try something that should not work. The matrix `D` below has a
different shape from `A`. It has one row, and `A` has two.

```python exec
id: scaling-and-the-shape-rule-3
D = [[1, 2, 3]]
add(A, D)
```

This cell is meant to fail. If you see a traceback, nothing is broken.

The error you see depends on how you wrote `add`. It is probably an
`IndexError`, about a position that does not exist in `D`. That error is
true, but it does not help much. It points at a symptom, deep inside a
loop. The real problem is that these two matrices could never be added.

The *shape* of a matrix is its number of rows and its number of columns.
Addition works only when both matrices have the same shape.

So what if `add` checked the shapes first? This condition is `True` when
the shapes match:

```python
len(a) == len(b) and len(a[0]) == len(b[0])
```

When the condition is `False`, `add` can stop with an error of its own.
The line `raise ValueError("a message")` stops the function at once and
reports a `ValueError` with your message. Then `add(A, D)` fails
straight away, and the error says why it failed, not only where.
[Reading an error message](tutorial:reading-an-error-message) has more
on `ValueError` and `IndexError`.

Write a new `add` with this check in the cell below.

```python exec
id: scaling-and-the-shape-rule-4
hint: if not (len(a) == len(b) and len(a[0]) == len(b[0])): raise ValueError(...) — put it before the loops, not inside them.
# Your add(a, b), with a shape check
```

```hint
Is the error you see the one you wrote, or one Python raised on its own?
Read the last line. If it says `ValueError` with your own message, the
check is working. Is that the case you meant to test? If it says something
else, which line is it pointing at, and does that line run before the
loops or inside them?
```

## Turning it sideways: the transpose

Here is one more operation. It has no arithmetic in it at all. Nothing
is added or multiplied. The numbers only move to new places.

```python exec
id: turning-it-sideways-the-transpose-1
def show_grid(m):
    for row in m:
        print(row)

M = [[1, 2, 3], [4, 5, 6]]
show_grid(M)
```

`M` has 2 rows and 3 columns. What would it look like if we swapped the
rows and the columns? The first *column* of `M` would become the first
*row*.

### Your turn

1. How might you write `transpose(m)`? It returns a new matrix. The
   number at row $i$, column $j$ of the new matrix is the number that was
   at row $j$, column $i$ of `m`.
2. Try it on `M` above.
3. Check the shape of the result. It should have 3 rows and 2 columns,
   the opposite of `M`.

```python exec
id: turning-it-sideways-the-transpose-2
expect: transpose([[1, 2, 3], [4, 5, 6]]) == [[1, 4], [2, 5], [3, 6]]
hint: Build the result row by row, one row per column of m. The new row i is [row[i] for row in m].
# Your transpose(m)
```

```hint
Take `M = [[1, 2, 3], [4, 5, 6]]`. What should the first row of the result
be, written out in full? Which column of `M` did those numbers come from?
How many rows will the result have, and where in `M` does that number
come from?
```

```hint
after: 10 errors
title: some steps
1. The result has one row for each column of `m`, so the outer loop runs
   `len(m[0])` times.
2. Row `i` of the result collects position `i` from every row of `m`.
3. Build each new row first, then append it, then move to the next `i`.

**Think about:** why `len(m)` and `len(m[0])` change places between `m`
and the result.

**Try this next:** transpose the transpose. What comes back, and why?
```

```inputs
transpose([[1, 2, 3], [4, 5, 6]])
transpose([[1, 2], [3, 4], [5, 6]])
transpose([[7]])                 # a single number
transpose([[1, 2, 3]])           # one row
```

```solution
def transpose(m):
    result = []
    for i in range(len(m[0])):
        new_row = []
        for row in m:
            new_row.append(row[i])
        result.append(new_row)
    return result
---
Row `i` of the result collects position `i` from every row of `m`.
```

This operation is called the *transpose*. The transpose of a matrix
swaps its rows and its columns. The transpose of $A$ is written $A^T$.

A *symmetric* matrix is a matrix that is equal to its own transpose. If
you swap its rows and columns, nothing changes. Try your `transpose` on
this one. Are the two lines the same?

```python exec
id: turning-it-sideways-the-transpose-3
S = [[1, 4, 7], [4, 2, 5], [7, 5, 3]]
print(transpose(S))
print(S)
```

## Reflection

We now have four operations, and each one is only a few lines long:

- `add`, which adds numbers in matching positions
- `scale`, which multiplies every number by the same scalar
- a shape check, which turns a confusing error into a clear one
- `transpose`, which moves numbers around with no arithmetic at all

None of them needed a library. The next page,
[Matrix multiplication: rows times columns](tutorial:multiplying-grids),
brings in the one matrix operation that surprises most people. It helps
to have built everything before it yourself.

What surprised you on this page? Did you know in advance that
`add(A, B)` would equal `add(B, A)`, or did you expect to have to check?

## Where to read more

Grant Sanderson (3Blue1Brown) (2016). *Essence of Linear Algebra, Chapter 1:
Vectors, What Even Are They?*
<https://www.youtube.com/watch?v=fNk_zzaMoSs>. Matrices in this tutorial are
built from plain lists. This video shows the geometric picture underneath
them. The whole series takes about an hour, and it is worth watching.

Downey, A. B. (2015). *Think Python: How to Think Like a Computer Scientist*
(2nd ed.). Green Tea Press. <https://greenteapress.com/wp/think-python-2e/>.
Chapter 10 covers lists, which is what we build a matrix from here.

Python Software Foundation. *5. Data Structures — Nested List
Comprehensions.* <https://docs.python.org/3/tutorial/datastructures.html>.
This section explains the pattern behind every nested loop in this
tutorial.

Sam Levey (2024). *The Matrix Transpose: Visual Intuition.*
<https://www.youtube.com/watch?v=wjYpzkQoyD8>. The transpose can look
like bookkeeping. This video shows what the transpose means, and why it
matters later. About twenty-six minutes.
