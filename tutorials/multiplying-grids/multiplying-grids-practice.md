---
title: "Matrix multiplication: rows times columns — Practice"
practice_for: multiplying-grids
year: "2026-2027"
version: 2026.08.24.1
---

# Matrix multiplication: rows times columns — Practice

Find the shape of the answer before you calculate its entries. The
shape catches more mistakes than the arithmetic does.

## Dot products

```python exec
id: dot-1
def dot(a, b):
    if len(a) != len(b):
        raise ValueError("lengths do not match")
    return sum(x * y for x, y in zip(a, b))


print(dot([2, -3, 1], [4, 0, -2]))
```

**1.** Calculate `dot([1, 2, 3], [1, 2, 3])` by hand. What does the dot
product of a vector with itself tell you?

<details class="dl-answer"><summary>answer</summary>

$1 + 4 + 9 = 14$.

A vector dotted with itself gives the sum of its entries squared. That
sum is the square of the vector's length. The length of a vector is also
called its *magnitude*. This fact matters when a vector represents a
point or a direction, and not only for a list of numbers.

</details>

**2.** Calculate `dot([1, 0, 0], [0, 5, 9])`. Then say in one sentence
why the answer came out that way.

<details class="dl-answer"><summary>answer</summary>

The answer is $0$. Every pair of entries has a zero in it:
$1 \times 0$, $0 \times 5$ and $0 \times 9$. So every term in the sum is
zero, before we add anything up.

Two vectors are *orthogonal* when their dot product is zero. For
ordinary vectors in space, orthogonal means at right angles, or
perpendicular. `[1, 0, 0]` has a number only in the first position, and
`[0, 5, 9]` has a zero there. They never have a number in the same
position to multiply together, so every product vanishes.

That is one way to get a zero, but not the only way. `dot([1, 1], [1, -1])`
is $1 - 1 = 0$ as well, and those two vectors share both positions. Here
the products cancel instead of vanishing. Draw $(1, 1)$ and $(1, -1)$
from the origin, and they are at right angles too.

</details>

## Shapes first

**3.** For each pair, can we multiply left by right? If we can, what
shape is the result?

| Left | Right |
|---|---|
| 2×3 | 3×4 |
| 3×2 | 3×2 |
| 4×1 | 1×3 |
| 1×4 | 4×1 |

<details class="dl-answer"><summary>answer</summary>

- 2×3 by 3×4: yes, and the result is 2×4. The inner numbers (3 and 3)
  match. The outer numbers (2 and 4) give the shape.
- 3×2 by 3×2: **no**. The first matrix has 2 columns, the second has 3
  rows, and $2 \neq 3$.
- 4×1 by 1×3: yes, and the result is 4×3. This is a *column vector* (a
  matrix with one column) times a *row vector* (a matrix with one row).
  The inner number is 1, the smallest it can be. Yet the result is the
  largest in this table compared with its inputs: 12 entries from 7.
- 1×4 by 4×1: yes, and the result is 1×1, a single number. This is the
  dot product in another form. A row vector times a column vector of the
  same length is the dot product, written as a 1×1 matrix instead of a
  plain number.

</details>

## Multiplying

```python exec
id: multiplying-1
def transpose(m):
    rows, cols = len(m), len(m[0])
    return [[m[r][c] for r in range(rows)] for c in range(cols)]


def multiply(a, b):
    bt = transpose(b)
    return [[dot(row, col) for col in bt] for row in a]


A = [[2, 0, 1], [-1, 3, 2]]
B = [[1, 4], [0, -2], [3, 1]]
print(multiply(A, B))
```

**4.** Check the result of `multiply(A, B)` above. Calculate the entry
$c_{11}$ by hand: row 1 of `A`, dotted with column 1 of `B`.

<details class="dl-answer"><summary>answer</summary>

$c_{11} = 2(1) + 0(0) + 1(3) = 5$. This matches the top-left entry
printed above.

</details>

**5.** A layer of a neural network calculates $\mathbf{y} = W\mathbf{x} + \mathbf{b}$:

$$W = \begin{bmatrix} 0.2 & 0.8 \\ -0.5 & 0.3 \\ 0.1 & 0.6 \end{bmatrix}, \quad
\mathbf{x} = \begin{bmatrix} 1 \\ 2 \end{bmatrix}, \quad
\mathbf{b} = \begin{bmatrix} 0.1 \\ -0.2 \\ 0.3 \end{bmatrix}$$

First calculate $W\mathbf{x}$. Then calculate $\mathbf{y} = W\mathbf{x} + \mathbf{b}$.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Check the shapes first: $W$ is 3×2 and $\mathbf{x}$ is 2×1. Can we
   multiply them? What shape is the result?
2. Each entry of $W\mathbf{x}$ is one row of $W$ dotted with the single
   column of $\mathbf{x}$.
3. Row 1 of $W$ is $[0.2, 0.8]$. Dot it with $[1, 2]$.
4. Do the same for rows 2 and 3.
5. Then add $\mathbf{b}$, entry by entry. This part is the matrix
   addition from the last page, not multiplication.

**Think about:** $\mathbf{x}$ has 2 entries and $\mathbf{b}$ has 3. Why is
that not a problem?

**Try this next:** if the next layer needs to take this 3-entry output and
produce 2 numbers, what shape would its own weight matrix need to be?

</details>

<details class="dl-answer"><summary>answer</summary>

$W\mathbf{x} = \begin{bmatrix} 1.8 \\ 0.1 \\ 1.3 \end{bmatrix}$,
so $\mathbf{y} = \begin{bmatrix} 1.9 \\ -0.1 \\ 1.6 \end{bmatrix}$.

For $W\mathbf{x}$:

- row 1 is $0.2(1) + 0.8(2) = 1.8$
- row 2 is $-0.5(1) + 0.3(2) = 0.1$
- row 3 is $0.1(1) + 0.6(2) = 1.3$

Then we add the three entries of $\mathbf{b}$ to those, and that gives
$\mathbf{y}$.

$\mathbf{x}$ has 2 entries because the layer before this one had 2
outputs. $\mathbf{b}$ has 3 entries because this layer has 3 outputs.
The two numbers belong to different layers, so there is no reason for
them to match. Only two numbers have to agree: the number of columns of
$W$ (2) and the length of $\mathbf{x}$ (2). Those are the inner numbers
of the multiplication.

</details>

## Order and the identity

```python exec
id: order-1
R = [[1, 2], [3, 4]]
S = [[5, 0], [1, -1]]
print("RS =", multiply(R, S))
print("SR =", multiply(S, R))
```

**6.** Are `RS` and `SR` the same matrix?

<details class="dl-answer"><summary>answer</summary>

No. `RS` is `[[7, -2], [19, -4]]` and `SR` is `[[5, 10], [-2, -2]]`.
Every entry is different.

</details>

**7.** The *rotation matrix* $R = \begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix}$
turns vectors 90° anticlockwise. Multiply it by $\begin{bmatrix} 1 \\ 0 \end{bmatrix}$
and by $\begin{bmatrix} 0 \\ 1 \end{bmatrix}$.

<details class="dl-answer"><summary>answer</summary>

$R\begin{bmatrix} 1 \\ 0 \end{bmatrix} = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$,
and $R\begin{bmatrix} 0 \\ 1 \end{bmatrix} = \begin{bmatrix} -1 \\ 0 \end{bmatrix}$.

Picture it on a compass. "Point right", turned 90° anticlockwise,
becomes "point up". "Point up" becomes "point left". The two answers say
exactly this.

The next page,
[Matrix transformations: what a matrix does to a picture](tutorial:what-a-matrix-does-to-a-picture),
builds a whole gallery of matrices in this way. For each matrix, it
reads where the matrix sends these two simplest vectors.

</details>

**8.** True or false? Give a one-sentence reason. Matrix multiplication
is *associative*: $(AB)C = A(BC)$ for any matrices whose shapes fit.

<details class="dl-answer"><summary>answer</summary>

True. The order of the matrices can matter, as problem 6 showed. But
the grouping does not. In $(AB)C$ and $A(BC)$, the matrices stay in the
same order. Only the pair we multiply first changes. Both groupings calculate
the same sums of products in the end.

This is why a chain of network layers, or a chain of transformations,
can be multiplied together ahead of time into a single matrix. We are
free to choose the grouping.

</details>

## Writing multiply

**9.** Write `multiply(a, b)` from the beginning. Write the `dot` and the
`transpose` it uses as well.

<details class="dl-answer"><summary>answer</summary>

```python
def dot(a, b):
    if len(a) != len(b):
        raise ValueError("lengths do not match")
    return sum(x * y for x, y in zip(a, b))


def transpose(m):
    rows, cols = len(m), len(m[0])
    return [[m[r][c] for r in range(rows)] for c in range(cols)]


def multiply(a, b):
    bt = transpose(b)
    return [[dot(row, col) for col in bt] for row in a]
```

The length check inside `dot` matters. When the shapes do not fit,
`multiply` raises a clear error, and does not drop entries with no
warning. The tutorial's `E` example shows why, if it is not clear yet.

</details>

**10.** Build `I3`, the 3×3 identity matrix. Check that `multiply(I3, I3)`
equals `I3`.

<details class="dl-answer"><summary>answer</summary>

```python
I3 = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
print(multiply(I3, I3) == I3)   # True
```

The identity times itself is itself. This has to be true. Multiplying
by the identity changes nothing, even when the other matrix is also the
identity.

</details>

## Thinking about it

**11.** Suppose $A$ is $m \times n$ and $B$ is $n \times m$. Then we can
calculate both $AB$ and $BA$. Are they the same shape?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Write down the shape rule again. The result has the rows of the left
   matrix and the columns of the right matrix.
2. For $AB$: $A$ is $m \times n$, $B$ is $n \times m$. What shape is the
   result?
3. For $BA$: $B$ is $n \times m$, $A$ is $m \times n$. What shape is *that*
   result?
4. Compare the two shapes you found in steps 2 and 3.

**Think about:** if $m \neq n$, can `AB == BA` possibly be true, even before
checking a single entry?

**Try this next:** pick an $A$ that is not square (say 2×3) and a
matching $B$ (3×2). Check both products in a cell.

</details>

<details class="dl-answer"><summary>answer</summary>

$AB$ is $m \times m$, and $BA$ is $n \times n$. When $m \neq n$, these
are different shapes.

So two matrices that are not square can still be multiplied in both
orders. But when the two results have different shapes, they cannot be
equal. We do not need to calculate a single entry to know that. Only when
$A$ and $B$ are both square, and the same size, is it worth comparing
the entries of `AB` and `BA`.

</details>

**12.** The shape rule checks the inner numbers. Why does it not ask for
both matrices to be the same shape, as addition does?

<details class="dl-answer"><summary>answer</summary>

Multiplication pairs a row of the left matrix with a column of the right
matrix. A dot product needs only its two lists to be the same length. It
does not care how many rows or columns either matrix has apart from
that.

If both matrices had to be the same shape, we would lose the most useful
cases. Think of a table of data times a vector of weights, or a rotation matrix
times a point. In neither case do the two shapes match, and these are
exactly what matrix multiplication is for.

</details>
