---
title: "Matrices: adding, scaling and transposing a grid of numbers — Practice"
practice_for: grid-of-numbers
year: "2026-2027"
version: 2026.08.24.1
---

# Matrices: adding, scaling and transposing a grid of numbers — Practice

The answers are hidden in folds. Solve each problem by hand first,
even the arithmetic ones. Then use the cells to check your work.

Some cells on this page use list comprehensions, such as
`[row[2] for row in A]`. You met these in
[Comprehensions, grids and aliasing](tutorial:comprehensions-and-grids).

## Reading a matrix

```python exec
id: reading-1
A = [[4, 7, -2], [1, 0, 6], [-3, 5, 8]]
print(A)
```

**1.** What are the dimensions of `A`?

<details class="dl-answer"><summary>answer</summary>

`A` is 3×3. It has three rows and three columns.

</details>

**2.** Find $a_{12}$, $a_{23}$ and $a_{32}$.

<details class="dl-answer"><summary>answer</summary>

$a_{12} = 7$ (row 1, column 2). $a_{23} = 6$ (row 2, column 3). $a_{32} = 5$
(row 3, column 2).

In Python these are `A[0][1]`, `A[1][2]` and `A[2][1]`. Maths notation
counts rows and columns from 1, and Python counts from 0. The most common
mistake in this section is to confuse the two.

</details>

**3.** Write the second row of `A` as a list. Then write the third column
as a list.

<details class="dl-answer"><summary>answer</summary>

The second row is `[1, 0, 6]`. That is `A[1]`.

The third column is `[-2, 6, 8]`. A plain list of lists has no shortcut
for a whole column, so we collect it one row at a time:
`[row[2] for row in A]`.

</details>

## Adding and scaling

```python exec
id: adding-1
def add(a, b):
    if not (len(a) == len(b) and len(a[0]) == len(b[0])):
        raise ValueError("shapes do not match")
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def scale(k, m):
    return [[k * v for v in row] for row in m]


X = [[2, 0, -1], [3, 1, 4]]
Y = [[-1, 2, 0], [1, -3, 2]]
print("X =", X)
print("Y =", Y)
```

**4.** Calculate $X + Y$ by hand. Then check it.

<details class="dl-answer"><summary>answer</summary>

$\begin{bmatrix} 1 & 2 & -1 \\ 4 & -2 & 6 \end{bmatrix}$

</details>

**5.** Calculate $2X - Y$.

<details class="dl-answer"><summary>answer</summary>

$\begin{bmatrix} 5 & -2 & -2 \\ 5 & 5 & 6 \end{bmatrix}$

First scale: $2X = \begin{bmatrix} 4 & 0 & -2 \\ 6 & 2 & 8 \end{bmatrix}$.
Then subtract $Y$ from that. The result is the answer above.

</details>

**6.** Calculate $X - 2Y$. Is it the same as $2X - Y$?

<details class="dl-answer"><summary>answer</summary>

$\begin{bmatrix} 4 & -4 & -1 \\ 1 & 7 & 0 \end{bmatrix}$. This is not the
same as the answer to problem 5.

There is no reason for $X - 2Y$ and $2X - Y$ to be equal. With plain
numbers, $3 - 2(5) = -7$ and $2(3) - 5 = 1$ are not equal either.
Addition does not care about order, but that does not mean you can move
the scalar from one matrix to the other.

</details>

**7.** A layer of a neural network updates its weights with this rule,
where $\alpha = 0.1$:

$$W_{\text{new}} = W_{\text{old}} - \alpha G$$

$$W_{\text{old}} = \begin{bmatrix} 0.5 & -0.3 \\ 1.2 & 0.8 \end{bmatrix}, \quad
G = \begin{bmatrix} 0.4 & -0.2 \\ 0.6 & 1.0 \end{bmatrix}$$

Calculate $W_{\text{new}}$.

<details class="dl-answer"><summary>answer</summary>

$\begin{bmatrix} 0.46 & -0.28 \\ 1.14 & 0.70 \end{bmatrix}$

First calculate $\alpha G = \begin{bmatrix} 0.04 & -0.02 \\ 0.06 & 0.10 \end{bmatrix}$.
Then subtract that from $W_{\text{old}}$.

Each weight moves a small step in the opposite direction to its entry
in $G$. This is the basic step in training a neural network: one `scale`
and one subtraction, repeated millions of times.

</details>

## The shape rule

```python exec
id: shape-1
P = [[1, 2], [3, 4], [5, 6]]
Q = [[1, 2, 3], [4, 5, 6]]
print("P is", len(P), "by", len(P[0]))
print("Q is", len(Q), "by", len(Q[0]))
```

**8.** Can we calculate `P + Q`? If not, what shape would `Q` need to be?

<details class="dl-answer"><summary>answer</summary>

No. `P` is 3×2 and `Q` is 2×3. Addition needs the same shape. `Q` has
the shape of `P` turned sideways, and that is not enough.

For `P + Q` to work, `Q` would also need to be 3×2. It needs the same
number of rows and the same number of columns as `P`. Having the same
total number of entries is not enough.

</details>

**9.** Suppose your `add` from the tutorial checks the shapes before it
loops. What does `add(P, Q)` raise, and what does the message say?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Look back at the shape check you wrote: `len(a) == len(b) and len(a[0]) == len(b[0])`.
2. Find `len(P)` and `len(Q)`. Are they equal?
3. The check fails. Which branch of the `if` runs?
4. That branch is a `raise`, not a `return`. So the function stops
   there, before any loop starts.

**Think about:** what would happen without the check. How far into the
nested loop would Python get before something broke?

**Try this next:** call `add` on two matrices with the same number of
rows but a different number of columns. Does the same check catch that
case too?

</details>

<details class="dl-answer"><summary>answer</summary>

It raises `ValueError: shapes do not match`, or whatever message your own
check used.

`len(P)` is 3 and `len(Q)` is 2. So the first half of the `and` is
already false, and Python does not look at the columns at all. The
function raises the error straight away, before the loop runs even once.

</details>

## The transpose

```python exec
id: transpose-1
def transpose(m):
    rows, cols = len(m), len(m[0])
    return [[m[r][c] for r in range(rows)] for c in range(cols)]


N = [[1, 2, 3], [0, 4, 5], [0, 0, 6]]
print(transpose(N))
```

**10.** If $M$ is 4×7, what is the shape of $M^T$?

<details class="dl-answer"><summary>answer</summary>

$M^T$ is 7×4. The transpose always swaps the two dimensions. So a square
matrix stays square, and a matrix that is not square changes shape.

</details>

**11.** Is $\begin{bmatrix} 2 & -3 \\ -3 & 5 \end{bmatrix}$ symmetric?

<details class="dl-answer"><summary>answer</summary>

Yes. When we swap the rows and the columns, every entry lands back in
the same place. The two entries off the diagonal are both $-3$. The
diagonal never moves in a transpose.

A matrix is symmetric when this mirroring works for every pair of
positions, not only the one pair you checked. Here there is only one
pair, so one check is enough.

</details>

**12.** `N` above is *upper-triangular*: all the entries below its
diagonal are zero. What does `transpose(N)` look like? What would you
call the result?

<details class="dl-answer"><summary>answer</summary>

`[[1, 0, 0], [2, 4, 0], [3, 5, 6]]`. This is *lower-triangular*: all the
entries above its diagonal are zero. The zeros that were below the
diagonal have moved above it. The diagonal itself (1, 4, 6) does not
move.

</details>

## Writing them

**13.** Write `add(a, b)` with a shape check, from the beginning.

<details class="dl-answer"><summary>answer</summary>

```python
def add(a, b):
    if not (len(a) == len(b) and len(a[0]) == len(b[0])):
        raise ValueError("shapes do not match")
    rows, cols = len(a), len(a[0])
    return [[a[i][j] + b[i][j] for j in range(cols)] for i in range(rows)]
```

The check goes before the loop, not inside it. A check inside the loop
would work, but the function might then fail at entry 50 of 100, not
straight away. That error is harder to find.

</details>

**14.** Write `transpose(m)` from the beginning.

<details class="dl-answer"><summary>answer</summary>

```python
def transpose(m):
    rows, cols = len(m), len(m[0])
    return [[m[r][c] for r in range(rows)] for c in range(cols)]
```

The outer loop runs over `cols`, not `rows`. This is the detail to check
twice. The result has `cols` rows and `rows` columns, the opposite of
`m`.

</details>

## Thinking about it

**15.** Does the order matter? If you scale a matrix and then transpose
it, do you get the same as if you transpose it and then scale it?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Pick a small matrix and a scalar. Try both orders in a cell.
2. Compare the two results entry by entry. Do not only glance at them.
3. Think about what each operation does. Scaling multiplies every entry
   by the same number. Transposing moves each entry to a mirrored
   position, but it never combines two entries.
4. Can moving an entry and multiplying it ever affect each other?

**Think about:** which of the four operations in this tutorial (add,
scale, the shape check, transpose) combine two different numbers into
one. Which ones only move or multiply single numbers on their own?

**Try this next:** does the same reasoning work for
`add(scale(k, a), scale(k, b))` compared with `scale(k, add(a, b))`?

</details>

<details class="dl-answer"><summary>answer</summary>

No, the order does not matter. Scaling multiplies each entry on its own.
Transposing only moves entries to a mirrored position. Neither operation
looks at more than one entry at a time. So in either order, the same
entries get the same multiplication.

This changes when an operation combines two different entries. Matrix
multiplication, on the next page,
[Matrix multiplication: rows times columns](tutorial:multiplying-grids),
does exactly that. Remember this question when you get there.

</details>

**16.** An image classifier sorts pictures into Cat, Dog and Bird. Its
*confusion matrix* counts its answers. The rows are the true label and
the columns are the label the classifier chose, in the order Cat, Dog,
Bird:

$$C = \begin{bmatrix} 850 & 30 & 20 \\ 15 & 920 & 25 \\ 10 & 20 & 970 \end{bmatrix}$$

1. How many dogs did the classifier label as birds?
2. What is its overall accuracy? Accuracy is the sum of the diagonal,
   divided by the sum of every entry.

<details class="dl-answer"><summary>answer</summary>

1. 25 dogs were labelled as birds. That entry is in row 2 (Dog), column 3
   (Bird).
2. The diagonal adds up to $850 + 920 + 970 = 2740$. All the entries add
   up to $2860$. So the accuracy is $2740 / 2860 \approx 95.8\%$.

The diagonal holds every example the classifier labelled correctly. Every entry
off the diagonal is a mistake, and its position says what kind of
mistake it was. Here the matrix is used to store data. We do not add or
multiply it.

</details>
