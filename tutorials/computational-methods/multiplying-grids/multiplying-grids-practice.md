---
title: "Multiplying Grids — Practice"
slug: multiplying-grids-practice
practice_for: multiplying-grids
module: computational-methods
module_title: "Computational Methods"
year: "2026-2027"
series: matrices
version: 2026.08.24.1
---

# Multiplying Grids — Practice

Work out the shape of the answer before you work out its entries — that
catches more mistakes than the arithmetic itself does.

## Dot Products

```python exec
id: dot-1
def dot(a, b):
    if len(a) != len(b):
        raise ValueError("lengths do not match")
    return sum(x * y for x, y in zip(a, b))


print(dot([2, -3, 1], [4, 0, -2]))
```

**1.** Compute `dot([1, 2, 3], [1, 2, 3])` by hand. What does the dot product
of a vector with itself tell you?

<details class="dl-answer"><summary>answer</summary>

$1 + 4 + 9 = 14$.

A vector dotted with itself is the sum of its entries squared — which is the
square of its length (its *magnitude*), a fact that turns out to matter a
great deal once vectors represent points or directions rather than lists of
numbers.

</details>

**2.** `dot([1, 0, 0], [0, 5, 9])` — compute it, then say in one sentence why
the answer came out that way.

<details class="dl-answer"><summary>answer</summary>

$0$. Every pair of entries has at least one zero in it — $1 \times 0$,
$0 \times 5$, $0 \times 9$ — so every term in the sum is zero before the
sum even happens.

Two vectors with a dot product of zero are called *orthogonal*, which for
ordinary geometric vectors means at right angles. `[1, 0, 0]` and
`[0, 5, 9]` never share a direction to multiply against, which is the
arithmetic reason they turn out to be perpendicular.

</details>

## Shapes First

**3.** State whether each product is defined, and if so, its shape:

| Left | Right |
|---|---|
| 2×3 | 3×4 |
| 3×2 | 3×2 |
| 4×1 | 1×3 |
| 1×4 | 4×1 |

<details class="dl-answer"><summary>answer</summary>

2×3 by 3×4: defined, result 2×4 — inner dimensions (3 and 3) match, outer
dimensions (2 and 4) become the shape.

3×2 by 3×2: **not** defined — the first matrix has 2 columns, the second has
3 rows, and $2 \neq 3$.

4×1 by 1×3: defined, result 4×3. This is a column vector times a row vector —
the smallest possible inner dimension, 1 — and it produces the largest result
relative to its inputs of anything in this table.

1×4 by 4×1: defined, result 1×1 — a single number. This is the dot product
in disguise: a row vector times a column vector of the same length *is* the
dot product, just written as a 1×1 matrix instead of a plain number.

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

**4.** Verify the result of `multiply(A, B)` above by computing entry $c_{11}$
by hand — row 1 of `A` dotted with column 1 of `B`.

<details class="dl-answer"><summary>answer</summary>

$c_{11} = 2(1) + 0(0) + 1(3) = 5$, which matches the top-left entry printed
above.

</details>

**5.** A neural network layer computes $\mathbf{y} = W\mathbf{x} + \mathbf{b}$:

$$W = \begin{bmatrix} 0.2 & 0.8 \\ -0.5 & 0.3 \\ 0.1 & 0.6 \end{bmatrix}, \quad
\mathbf{x} = \begin{bmatrix} 1 \\ 2 \end{bmatrix}, \quad
\mathbf{b} = \begin{bmatrix} 0.1 \\ -0.2 \\ 0.3 \end{bmatrix}$$

Compute $W\mathbf{x}$, then $\mathbf{y} = W\mathbf{x} + \mathbf{b}$.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Check the shapes first: $W$ is 3×2, $\mathbf{x}$ is 2×1. Is the product
   defined, and what shape does it come out?
2. Each entry of $W\mathbf{x}$ is one row of $W$ dotted with the single
   column of $\mathbf{x}$.
3. Row 1 of $W$ is $[0.2, 0.8]$. Dot it with $[1, 2]$.
4. Repeat for rows 2 and 3, then add $\mathbf{b}$ entry by entry — that part
   is the addition from the last tutorial, not multiplication.

**Think about:** $\mathbf{x}$ has 2 entries and $\mathbf{b}$ has 3. Why is
that not a contradiction?

**Try this next:** if the next layer needs to take this 3-entry output and
produce 2 numbers, what shape would its own weight matrix need to be?

</details>

<details class="dl-answer"><summary>answer</summary>

$W\mathbf{x} = \begin{bmatrix} 1.8 \\ 0.1 \\ 1.3 \end{bmatrix}$,
so $\mathbf{y} = \begin{bmatrix} 1.9 \\ -0.1 \\ 1.6 \end{bmatrix}$.

$W\mathbf{x}$: row 1 is $0.2(1) + 0.8(2) = 1.8$; row 2 is
$-0.5(1) + 0.3(2) = 0.1$; row 3 is $0.1(1) + 0.6(2) = 1.3$. Adding
$\mathbf{b}$'s three entries to those gives $\mathbf{y}$.

$\mathbf{x}$ has 2 entries because the *previous* layer had 2 outputs;
$\mathbf{b}$ has 3 because *this* layer has 3 outputs. The two counts belong
to different layers and have no reason to match — only $W$'s columns (2) and
$\mathbf{x}$'s length (2) have to agree, because those are the inner
dimensions of the multiplication.

</details>

## Order and the Identity

```python exec
id: order-1
R = [[1, 2], [3, 4]]
S = [[5, 0], [1, -1]]
print("RS =", multiply(R, S))
print("SR =", multiply(S, R))
```

**6.** Are `RS` and `SR` the same matrix?

<details class="dl-answer"><summary>answer</summary>

No — `RS` is `[[7, -2], [19, -4]]` and `SR` is `[[5, 10], [-2, -2]]`,
different in every entry.

</details>

**7.** A rotation matrix $R = \begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix}$
turns vectors 90° anticlockwise. Apply it to $\begin{bmatrix} 1 \\ 0 \end{bmatrix}$
and to $\begin{bmatrix} 0 \\ 1 \end{bmatrix}$.

<details class="dl-answer"><summary>answer</summary>

$R\begin{bmatrix} 1 \\ 0 \end{bmatrix} = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$,
and $R\begin{bmatrix} 0 \\ 1 \end{bmatrix} = \begin{bmatrix} -1 \\ 0 \end{bmatrix}$.

Picture it on a compass: "point right" rotated 90° anticlockwise becomes
"point up", and "point up" becomes "point left" — which is exactly what both
answers say. The next tutorial builds an entire gallery of matrices this way,
reading off where they send the two simplest vectors.

</details>

**8.** True or false, with a one-sentence reason: matrix multiplication is
associative — $(AB)C = A(BC)$ for any matrices where the shapes work out.

<details class="dl-answer"><summary>answer</summary>

True. Unlike commutativity, associativity does hold for matrix
multiplication — the order the matrices appear in never changes, only which
adjacent pair is multiplied first, and both groupings compute the exact same
sum of products underneath.

This is why a chain of network layers, or a chain of transformations, can be
composed in advance into a single matrix — the grouping is a free choice.

</details>

## Writing Multiply

**9.** Write `multiply(a, b)` from scratch, using a `dot` and a `transpose`
you also write.

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

The length check inside `dot` is what makes a shape mismatch in `multiply`
raise cleanly instead of silently dropping entries — see the tutorial's own
`E` example if that is not immediately obvious why.

</details>

**10.** Construct `I3`, the 3×3 identity matrix, and verify `multiply(I3, I3)`
equals `I3`.

<details class="dl-answer"><summary>answer</summary>

```python
I3 = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
print(multiply(I3, I3) == I3)   # True
```

The identity multiplied by itself is itself — which has to be true, since
multiplying by the identity changes nothing, including when what it is
multiplying is another identity.

</details>

## Thinking About It

**11.** If $A$ is $m \times n$ and $B$ is $n \times m$, both $AB$ and $BA$
are defined — but are they the same *shape*?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Write down the shape rule again: (rows of left) × (columns of right).
2. For $AB$: $A$ is $m \times n$, $B$ is $n \times m$. What shape is the
   result?
3. For $BA$: $B$ is $n \times m$, $A$ is $m \times n$. What shape is *that*
   result?
4. Compare the two shapes you found in steps 2 and 3.

**Think about:** if $m \neq n$, can `AB == BA` possibly be true, even before
checking a single entry?

**Try this next:** pick a genuinely rectangular $A$ (say 2×3) and a matching
$B$ (3×2), and confirm both products in a cell.

</details>

<details class="dl-answer"><summary>answer</summary>

$AB$ comes out $m \times m$, and $BA$ comes out $n \times n$ — different
shapes whenever $m \neq n$.

So two matrices that are not even square can still both be multiplied both
ways, and the two results cannot possibly be equal if their shapes differ —
no need to compute a single entry to know that. It is only when $A$ and $B$
are both square, and the same size, that `AB == BA` is even a question worth
asking about the entries.

</details>

**12.** Why does the rule check the *inner* dimensions rather than, say,
requiring both matrices to be the same shape?

<details class="dl-answer"><summary>answer</summary>

Because multiplication pairs up a *row* of the left matrix with a *column*
of the right one, and a dot product only needs its two lists to be the same
length — it does not care how many rows or columns either matrix has beyond
that.

Requiring the same shape entirely, the way addition does, would rule out
every genuinely useful case here — a dataset matrix times a weight vector,
a rotation matrix times a point, none of these have matching left and right
shapes, and all of them are exactly what matrix multiplication is for.

</details>
