---
title: "Undoing It — Practice"
slug: undoing-it-practice
practice_for: undoing-it
module: computational-methods
module_title: "Computational Methods"
year: "2026-2027"
series: matrices
version: 2026.08.24.1
---

# Undoing It — Practice

Compute each determinant by hand before you run anything — it is two
multiplications and a subtraction, and the whole point of this page is to
make that arithmetic automatic.

## Determinants

```python exec
id: determinants-1
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
```

**1.** Compute $\det\begin{bmatrix} 3 & 2 \\ 1 & 4 \end{bmatrix}$ by hand,
then check it.

<details class="dl-answer"><summary>answer</summary>

$3(4) - 2(1) = 10$.

</details>

**2.** Compute $\det\begin{bmatrix} 5 & -1 \\ 10 & -2 \end{bmatrix}$. Look at
the two rows — is there a relationship between them that could have told you
the answer before multiplying anything?

<details class="dl-answer"><summary>answer</summary>

$5(-2) - (-1)(10) = -10 + 10 = 0$.

Row 2 is exactly row 1 doubled: $[10, -2] = 2 \times [5, -1]$. Whenever one
row of a 2×2 matrix is a multiple of the other, the determinant is zero —
which makes sense once you remember the determinant measures area, and two
proportional rows describe a "square" that has already been squashed flat
before you even multiply anything by it.

</details>

## Inverses

**3.** Find the inverse of $\begin{bmatrix} 3 & 2 \\ 1 & 4 \end{bmatrix}$
using the formula, then verify by multiplying the two together.

<details class="dl-answer"><summary>answer</summary>

$\begin{bmatrix} 0.4 & -0.2 \\ -0.1 & 0.3 \end{bmatrix}$

```python
A = [[3, 2], [1, 4]]
print(multiply(A, inverse(A)))
```

Running that does not print a perfectly clean
`[[1.0, 0.0], [0.0, 1.0]]` — one of the off-diagonal entries typically comes
out as something like `-1.11e-16` instead of exactly `0`. That is not a bug
in `inverse`; it is ordinary floating-point rounding, the same kind of noise
behind `0.1 + 0.2 != 0.3`. It is small enough to be worth checking with
`check()` — which allows a tiny tolerance for exactly this reason — rather
than an exact `==`.

</details>

**4.** A system $A\mathbf{x} = \mathbf{b}$:

$$A = \begin{bmatrix} 2 & 1 \\ 5 & 3 \end{bmatrix}, \quad
\mathbf{b} = \begin{bmatrix} 4 \\ 9 \end{bmatrix}$$

Solve it by computing $\mathbf{x} = A^{-1}\mathbf{b}$.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Find $\det(A)$ first — you will need it whether or not the formula asks
   for it explicitly, because `inverse` divides by it internally.
2. Compute $A^{-1}$ with the formula, or with your `inverse` function.
3. `b` needs to be a column, not a plain list — `[[4], [9]]`, matching the
   shape `multiply` expects.
4. `multiply(inverse(A), b)` gives $\mathbf{x}$ as a column too.

**Think about:** how would you check your answer without recomputing
anything — using $A$ and $\mathbf{x}$ rather than $A^{-1}$?

**Try this next:** solve the same system by writing it as two ordinary
simultaneous equations and eliminating a variable by hand. Do you get the
same $\mathbf{x}$?

</details>

<details class="dl-answer"><summary>answer</summary>

$\mathbf{x} = \begin{bmatrix} 3 \\ -2 \end{bmatrix}$.

$\det(A) = 2(3) - 1(5) = 1$, so
$A^{-1} = \begin{bmatrix} 3 & -1 \\ -5 & 2 \end{bmatrix}$, and
$A^{-1}\mathbf{b} = \begin{bmatrix} 3(4) + (-1)(9) \\ -5(4) + 2(9) \end{bmatrix}
= \begin{bmatrix} 3 \\ -2 \end{bmatrix}$.

Checking without recomputing: substitute back into the original system.
$2(3) + 1(-2) = 4$ and $5(3) + 3(-2) = 9$ — both match $\mathbf{b}$, so the
answer is right regardless of whether the inverse arithmetic was.

</details>

## Which Can Be Undone

**5.** $\det(A) = 5$ and $\det(B) = 3$, for two 2×2 matrices. What is
$\det(AB)$?

<details class="dl-answer"><summary>answer</summary>

$15$. Determinants multiply: $\det(AB) = \det(A)\det(B)$, always, for square
matrices of the same size.

This is worth sitting with for a moment: it says the *area-scaling factor*
of doing two transformations one after another is the product of their
individual factors — which is exactly what you would want "scale by 5, then
scale by 3" to mean, and it turns out to be true even when the two
transformations are not simple scalings at all.

</details>

**6.** If $\det(AB) = 0$, does that mean $\det(A) = 0$ and $\det(B) = 0$?

<details class="dl-answer"><summary>answer</summary>

No — only that *at least one* of them is zero. $\det(AB) = \det(A)\det(B)$,
and a product of two ordinary numbers is zero exactly when one of the two
factors is, not both.

Geometrically: if either transformation on its own flattens the square,
applying the other one afterward (or beforehand) cannot un-flatten it. One
collapse is enough to make the whole chain uninvertible.

</details>

**7.** A matrix has $\det(A) = -4$. Does it have an inverse?

<details class="dl-answer"><summary>answer</summary>

Yes. The only determinant value that rules out an inverse is exactly zero —
a negative determinant is completely fine, and just means the transformation
flips orientation (left-handed becomes right-handed) as well as scaling area
by a factor of 4.

</details>

## Writing It

**8.** Write `inverse(M)` from scratch, for a 2×2 matrix.

<details class="dl-answer"><summary>answer</summary>

```python
def inverse(M):
    d = M[0][0] * M[1][1] - M[0][1] * M[1][0]
    if d == 0:
        raise ValueError("this matrix has no inverse")
    a, b = M[0]
    c, e = M[1]
    return [[e / d, -b / d], [-c / d, a / d]]
```

Adding the `if d == 0` check turns "divide by zero, eventually, somewhere in
the return statement" into an error that names the actual problem — the same
shape-check instinct from *A Grid of Numbers*, applied to a different kind of
invalid input.

</details>

## Thinking About It

**9.** A matrix has determinant $0.0001$ — not zero, so it technically has an
inverse. Why might a computer still have trouble using it reliably?

<details class="dl-answer"><summary>answer</summary>

Because the inverse formula divides by the determinant, and dividing by a
very small number produces very large numbers — small errors already present
in the data get multiplied up enormously by that division.

This is called being *ill-conditioned*: technically invertible, but close
enough to singular that ordinary floating-point rounding can swing the
answer by more than the answer is worth trusting. It shows up constantly in
practice — fitting a model to data that is nearly, but not quite, repeating
itself in two different measurements.

</details>
