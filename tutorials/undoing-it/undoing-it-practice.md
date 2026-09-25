---
title: "Inverse matrices: undoing a transformation — Practice"
practice_for: undoing-it
year: "2026-2027"
version: 2026.08.24.1
---

# Inverse matrices: undoing a transformation — Practice

Work out each determinant by hand before you run anything. It is two
multiplications and a subtraction. The aim of this page is to make that
arithmetic automatic.

## Determinants

```python exec
id: determinants-1
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
```

**1.** Work out $\det\begin{bmatrix} 3 & 2 \\ 1 & 4 \end{bmatrix}$ by hand.
Then check it.

<details class="dl-answer"><summary>answer</summary>

$3(4) - 2(1) = 10$.

</details>

**2.** Work out $\det\begin{bmatrix} 5 & -1 \\ 10 & -2 \end{bmatrix}$. Now look
at the two rows. Is there a link between them that could have told you
the answer before you multiplied anything?

<details class="dl-answer"><summary>answer</summary>

$5(-2) - (-1)(10) = -10 + 10 = 0$.

Row 2 is exactly row 1 doubled: $[10, -2] = 2 \times [5, -1]$. Whenever
one row of a 2×2 matrix is a multiple of the other, the determinant is
zero.

This makes sense, because the determinant measures area. When one row is
a multiple of the other, the matrix sends every point onto the same line
through the origin. So it flattens the square, and the area is zero.

</details>

## Inverses

**3.** Find the inverse of $\begin{bmatrix} 3 & 2 \\ 1 & 4 \end{bmatrix}$
with the formula. Then check it by multiplying the two matrices
together.

<details class="dl-answer"><summary>answer</summary>

$\begin{bmatrix} 0.4 & -0.2 \\ -0.1 & 0.3 \end{bmatrix}$

```python
A = [[3, 2], [1, 4]]
print(multiply(A, inverse(A)))
```

This does not print a perfectly clean `[[1.0, 0.0], [0.0, 1.0]]`. It
prints `[[1.0000000000000002, -1.1102230246251565e-16], [0.0, 1.0]]`.
`-1.11e-16` means $-1.11 \times 10^{-16}$, a tiny number very close to
`0`.

This is not a bug in `inverse`. It is ordinary rounding in
floating-point numbers, the same kind of small error that makes
`0.1 + 0.2 == 0.3` come out `False`. So it is better to check the result
with `check()`, which allows a tiny difference for exactly this reason.
An exact `==` would say `False`.

</details>

**4.** Here is a system of equations, $A\mathbf{x} = \mathbf{b}$:

$$A = \begin{bmatrix} 2 & 1 \\ 5 & 3 \end{bmatrix}, \quad
\mathbf{b} = \begin{bmatrix} 4 \\ 9 \end{bmatrix}$$

Solve it by working out $\mathbf{x} = A^{-1}\mathbf{b}$. The next page,
[Systems of equations: solving them with matrices](tutorial:solving-systems),
looks at systems like this one in more detail.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Find $\det(A)$ first. You need it either way, because `inverse`
   divides by it.
2. Work out $A^{-1}$ with the formula, or with your `inverse` function.
3. Write `b` as a column: `[[4], [9]]`. That is the shape `multiply`
   expects. A plain list `[4, 9]` will not work.
4. `multiply(inverse(A), b)` gives $\mathbf{x}$, as a column too.

**Think about:** how could you check your answer without working it all
out again? Use $A$ and $\mathbf{x}$, not $A^{-1}$.

**Try this next:** write the same system as two ordinary simultaneous
equations. Solve them by hand, by removing one unknown. Do you get the
same $\mathbf{x}$?

</details>

<details class="dl-answer"><summary>answer</summary>

$\mathbf{x} = \begin{bmatrix} 3 \\ -2 \end{bmatrix}$.

$\det(A) = 2(3) - 1(5) = 1$, so
$A^{-1} = \begin{bmatrix} 3 & -1 \\ -5 & 2 \end{bmatrix}$, and
$A^{-1}\mathbf{b} = \begin{bmatrix} 3(4) + (-1)(9) \\ -5(4) + 2(9) \end{bmatrix}
= \begin{bmatrix} 3 \\ -2 \end{bmatrix}$.

To check without working it all out again, put the answer back into the
original system: $2(3) + 1(-2) = 4$ and $5(3) + 3(-2) = 9$. Both match
$\mathbf{b}$. So the answer is right, even if you made a mistake in the
inverse along the way.

</details>

## Which can be undone

**5.** Two 2×2 matrices have $\det(A) = 5$ and $\det(B) = 3$. What is
$\det(AB)$?

<details class="dl-answer"><summary>answer</summary>

$15$. Determinants multiply: $\det(AB) = \det(A)\det(B)$. This is always
true for square matrices of the same size.

Think about what this says. Doing two transformations one after the
other scales area by the product of their two factors. That is exactly
what you would want "scale by 5, then scale by 3" to mean. It stays true
even when the two transformations are not simple scalings at all.

</details>

**6.** If $\det(AB) = 0$, does that mean $\det(A) = 0$ and $\det(B) = 0$?

<details class="dl-answer"><summary>answer</summary>

No. It means only that at least one of them is zero. We know that
$\det(AB) = \det(A)\det(B)$. A product of two ordinary numbers is zero
when at least one of the two numbers is zero. Both do not have to be.

In pictures: if either transformation flattens the square on its own,
the other one cannot unflatten it, whether it comes before or after. One
collapse is enough, and then the whole chain has no inverse.

</details>

**7.** A matrix has $\det(A) = -4$. Does it have an inverse?

<details class="dl-answer"><summary>answer</summary>

Yes. The only determinant that rules out an inverse is exactly zero. A
negative determinant is fine. It means that the transformation flips the
shape over, like a mirror, as well as scaling its area by a factor of
4. After the flip, a left hand would look like a right hand.

</details>

## Writing it

**8.** Write `inverse(M)` for a 2×2 matrix, from the beginning.

<details class="dl-answer"><summary>answer</summary>

```python
def inverse(M):
    d = M[0][0] * M[1][1] - M[0][1] * M[1][0]
    if d == 0:
        raise ValueError("this matrix has no inverse")
    a, b = M[0]
    c, e = M[1]  # e stands in for the formula's own d, already taken by the determinant above
    return [[e / d, -b / d], [-c / d, a / d]]
```

Without the `if d == 0` check, the function would divide by zero
somewhere in the `return` line. With the check, the error names the real
problem. This is the same idea as the shape check in
[Matrices: adding, scaling and transposing a grid of numbers](tutorial:grid-of-numbers),
used for a different kind of bad input.

</details>

## Thinking about it

**9.** Here are two matrices. Both have determinant $0.0001$, so both
have an inverse.

$$A = \begin{bmatrix} 0.01 & 0 \\ 0 & 0.01 \end{bmatrix} \qquad
B = \begin{bmatrix} 1 & 1 \\ 1 & 1.0001 \end{bmatrix}$$

Undo each one on a point, then nudge the point by $0.0001$ and undo it
again. Which answer moves more? Can you say why?

<details class="dl-answer"><summary>answer</summary>

With $B$, the point $(2, 2.0001)$ undoes to $(1, 1)$. Nudge it to
$(2, 2.0002)$, and it undoes to $(0, 2)$. A change in the fourth decimal
place moved the answer by a whole unit.

With $A$, the point $(0.02, 0.02)$ undoes to $(2, 2)$. Nudge it to
$(0.02, 0.0201)$, and it undoes to $(2, 2.01)$. The answer moved, but
only in step with the nudge, 100 times over, because $A$ shrinks
everything by 100 in every direction.

So a small determinant is not the problem on its own. $A$ shrinks the
plane evenly, and undoing it is safe. $B$'s two rows are almost the
same, so it squashes the plane nearly flat onto a line. Undoing it means
pulling apart two directions that are almost one direction, and a tiny
change in the input decides where they land.

A matrix like $B$ is *ill-conditioned*: it has an inverse, but a tiny
change in what you give it can make a big change in what you get back.
Rounding in a computer is exactly that kind of tiny change. This happens
often in real work. One example is fitting a model to data where two
different measurements almost repeat each other, but not quite, just as
$B$'s two rows do.

</details>
