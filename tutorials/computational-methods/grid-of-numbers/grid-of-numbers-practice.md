---
title: "A Grid of Numbers — Practice"
slug: grid-of-numbers-practice
practice_for: grid-of-numbers
module: computational-methods
module_title: "Computational Methods"
year: "2026-2027"
series: matrices
version: 2026.08.24.1
---

# A Grid of Numbers — Practice

Answers are folded. Work each one out by hand first — even the arithmetic
ones — and use the cells only to check.

## Reading a Matrix

```python exec
id: reading-1
A = [[4, 7, -2], [1, 0, 6], [-3, 5, 8]]
print(A)
```

**1.** State the dimensions of `A`.

<details class="dl-answer"><summary>answer</summary>

3×3 — three rows, three columns.

</details>

**2.** Find $a_{12}$, $a_{23}$, and $a_{32}$.

<details class="dl-answer"><summary>answer</summary>

$a_{12} = 7$ (row 1, column 2). $a_{23} = 6$ (row 2, column 3). $a_{32} = 5$
(row 3, column 2).

In Python that is `A[0][1]`, `A[1][2]`, `A[2][1]` — the maths notation counts
rows and columns from 1, Python counts from 0, and mixing the two up is the
single most common mistake in this section.

</details>

**3.** Write the second row of `A` as a list, and the third column as a list.

<details class="dl-answer"><summary>answer</summary>

Second row: `[1, 0, 6]` — that's `A[1]` directly.

Third column: `[-2, 6, 8]` — there is no `A[..][2]` shortcut for a whole
column in a plain list of lists, so this has to be collected one row at a
time: `[row[2] for row in A]`.

</details>

## Adding and Scaling

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

**4.** Compute $X + Y$ by hand, then check it.

<details class="dl-answer"><summary>answer</summary>

$\begin{bmatrix} 1 & 2 & -1 \\ 4 & -2 & 6 \end{bmatrix}$

</details>

**5.** Compute $2X - Y$.

<details class="dl-answer"><summary>answer</summary>

$\begin{bmatrix} 5 & -2 & -2 \\ 5 & 5 & 6 \end{bmatrix}$

Scale first, then subtract: $2X = \begin{bmatrix} 4 & 0 & -2 \\ 6 & 2 & 8 \end{bmatrix}$,
and subtracting $Y$ from that gives the answer above.

</details>

**6.** Compute $X - 2Y$. Is it the same as $2X - Y$?

<details class="dl-answer"><summary>answer</summary>

$\begin{bmatrix} 4 & -4 & -1 \\ 1 & 7 & 0 \end{bmatrix}$ — not the same as
problem 5.

There is no reason to expect $X - 2Y$ and $2X - Y$ to agree, in the same way
there is no reason to expect $3 - 2(5)$ and $2(3) - 5$ to agree for plain
numbers. Scalar multiplication and subtraction do not commute with each other
just because addition commutes with itself.

</details>

**7.** A network layer updates its weights with
$W_{\text{new}} = W_{\text{old}} - \alpha G$, where $\alpha = 0.1$:

$$W_{\text{old}} = \begin{bmatrix} 0.5 & -0.3 \\ 1.2 & 0.8 \end{bmatrix}, \quad
G = \begin{bmatrix} 0.4 & -0.2 \\ 0.6 & 1.0 \end{bmatrix}$$

Compute $W_{\text{new}}$.

<details class="dl-answer"><summary>answer</summary>

$\begin{bmatrix} 0.46 & -0.28 \\ 1.14 & 0.70 \end{bmatrix}$

$\alpha G = \begin{bmatrix} 0.04 & -0.02 \\ 0.06 & 0.10 \end{bmatrix}$ first,
then subtract that from $W_{\text{old}}$. The weights move a small step in
the direction that shrinks $G$ — this is the entire update rule behind
training a neural network, one `scale` and one subtraction, repeated
millions of times.

</details>

## The Shape Rule

```python exec
id: shape-1
P = [[1, 2], [3, 4], [5, 6]]
Q = [[1, 2, 3], [4, 5, 6]]
print("P is", len(P), "by", len(P[0]))
print("Q is", len(Q), "by", len(Q[0]))
```

**8.** Can `P + Q` be computed? If not, what shape would `Q` need for it to
work?

<details class="dl-answer"><summary>answer</summary>

No — `P` is 3×2 and `Q` is 2×3. Addition needs identical shapes, and these are
not even the same shape turned sideways in a way addition would care about.

For `P + Q` to work, `Q` would need to be 3×2 as well — the exact same number
of rows and the exact same number of columns as `P`, not merely the same
total count of entries.

</details>

**9.** If your `add` from the tutorial checks shapes before it loops, what
does `add(P, Q)` raise, and what does the message say?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Look back at the shape check you wrote: `len(a) == len(b) and len(a[0]) == len(b[0])`.
2. Work out `len(P)` and `len(Q)` — are they equal?
3. Since the check fails, which branch of the `if` runs?
4. That branch is a `raise`, not a `return` — so the function stops there,
   before any loop ever starts.

**Think about:** what would have happened without the check — how far into
the nested loop would Python get before something broke?

**Try this next:** call `add` on two matrices with the same number of rows
but a different number of columns, and confirm the same check catches that
case too.

</details>

<details class="dl-answer"><summary>answer</summary>

`ValueError: shapes do not match` — or whatever message your own check used.

`len(P)` is 3 and `len(Q)` is 2, so the `and` in the check is already false
before either matrix's columns are even looked at, and the function raises
immediately rather than running a single iteration of the loop.

</details>

## The Transpose

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

7×4. The transpose always swaps the two dimensions, so a matrix that started
square stays square, and one that did not, does not.

</details>

**11.** Is $\begin{bmatrix} 2 & -3 \\ -3 & 5 \end{bmatrix}$ symmetric?

<details class="dl-answer"><summary>answer</summary>

Yes. Swap rows and columns and every entry lands back where it started: the
off-diagonal pair are both $-3$, and the diagonal never moves under a
transpose regardless.

A symmetric matrix is exactly one where that off-diagonal mirroring holds for
every pair of positions, not only the one you happened to check.

</details>

**12.** For `N` above — upper-triangular, with zeros below the diagonal —
what does `transpose(N)` look like, and what would you call the result?

<details class="dl-answer"><summary>answer</summary>

`[[1, 0, 0], [2, 4, 0], [3, 5, 6]]` — lower-triangular. The zeros that were
above the diagonal move below it, and the diagonal itself (1, 4, 6) does not
move.

</details>

## Writing Them

**13.** Write `add(a, b)` with a shape check, from scratch.

<details class="dl-answer"><summary>answer</summary>

```python
def add(a, b):
    if not (len(a) == len(b) and len(a[0]) == len(b[0])):
        raise ValueError("shapes do not match")
    rows, cols = len(a), len(a[0])
    return [[a[i][j] + b[i][j] for j in range(cols)] for i in range(rows)]
```

The check has to come before the loop, not inside it — checking on every
single element would work, but it means the function might raise on entry
50 of 100 instead of immediately, which is a worse error to debug.

</details>

**14.** Write `transpose(m)` from scratch.

<details class="dl-answer"><summary>answer</summary>

```python
def transpose(m):
    rows, cols = len(m), len(m[0])
    return [[m[r][c] for r in range(rows)] for c in range(cols)]
```

The outer loop runs over `cols`, not `rows` — that is the one detail worth
double-checking, because the result has `cols` rows and `rows` columns, the
opposite of `m`.

</details>

## Thinking About It

**15.** Does it matter whether you scale a matrix first and then transpose
it, or transpose it first and then scale it?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Pick a small matrix and a scalar, and try both orders in a cell.
2. Compare the two results entry by entry rather than eyeballing them.
3. Think about what scaling does — multiplies every entry by the same
   number — and what transposing does — moves entries to a mirrored
   position but never combines two entries together.
4. Ask whether moving an entry and multiplying it can ever interfere with
   each other.

**Think about:** which of the four operations in this tutorial — add, scale,
the shape check, transpose — actually combine two different numbers into one,
and which only rearrange or multiply single numbers on their own.

**Try this next:** does the same reasoning apply to `add(scale(k, a), scale(k, b))`
compared with `scale(k, add(a, b))`?

</details>

<details class="dl-answer"><summary>answer</summary>

No — the order does not matter. Scaling multiplies each entry on its own;
transposing only moves entries to a mirrored position. Neither operation
looks at more than one entry at a time, so doing them in either order visits
the same entries and does the same multiplication to each.

This stops being obvious once an operation combines two different entries —
which is exactly what tutorial 2's multiplication does, and it is worth
remembering this question when you get there.

</details>

**16.** A confusion matrix from an image classifier — rows are the true
label, columns are the predicted one:

$$C = \begin{bmatrix} 850 & 30 & 20 \\ 15 & 920 & 25 \\ 10 & 20 & 970 \end{bmatrix}$$

The order is Cat, Dog, Bird. How many dogs were misclassified as birds, and
what is the overall accuracy (sum of the diagonal, divided by the sum of
everything)?

<details class="dl-answer"><summary>answer</summary>

25 dogs were classified as birds — row 2 (Dog), column 3 (Bird).

Accuracy: the diagonal sums to $850 + 920 + 970 = 2740$, and every entry
sums to $2860$, so accuracy is $2740 / 2860 \approx 95.8\%$.

The diagonal is every example the classifier got right; everything off it is
a mistake, and which off-diagonal cell it landed in says what kind of
mistake — this table is a matrix used as a data structure, not as an object
you add or multiply.

</details>
