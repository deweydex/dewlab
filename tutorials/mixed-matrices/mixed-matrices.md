---
title: "Mixed problems: matrices"
practice_across:
  - grid-of-numbers
  - what-a-matrix-does-to-a-picture
  - multiplying-grids
  - undoing-it
  - solving-systems
  - matrices-in-numpy
  - where-chains-lead
year: "2026-2027"
version: 2026.09.26.1
---

# Mixed problems: matrices

These problems move between the pages of the series on purpose, and do
not say which page each one comes from. Choosing the tool is part of
the problem. Your own `add`, `scale`, `transpose`, `transform`,
`multiply`, `det`, `inverse`, `eliminate` and `solve` are already
loaded, and so is NumPy after the first cell runs.

Each answer is hidden in a fold under its question. Work it out on
paper first where you can, then check in a cell.

```python exec
id: mixed-matrices-tools
import math

import numpy as np
```

## Shapes and grids

**1.** $A$ is 2×3 and $B$ is 3×4. What shape is
`transpose(multiply(A, B))`?

<details class="dl-answer"><summary>answer</summary>

`multiply(A, B)` is 2×4, and its transpose is 4×2.

</details>

**2.** Two photos are grids of numbers from 0 to 255. `add(photo_a,
photo_b)` makes some parts pure white. What would mix the two photos
without that happening?

<details class="dl-answer"><summary>answer</summary>

`add(scale(0.5, photo_a), scale(0.5, photo_b))`. Each number is then
the average of two numbers from 0 to 255, so it stays from 0 to 255.
Adding them whole can reach 510, and a screen draws anything above
255 as white.

</details>

**3.** A function is meant to return a darker copy of a photo:

```python
def darker(photo):
    for row in photo:
        for j in range(len(row)):
            row[j] = row[j] // 2
    return photo
```

After `dim = darker(original)`, what has happened to `original`?

<details class="dl-answer"><summary>answer</summary>

It is darker too. `row[j] = ...` changes the rows of `original` in
place, and `darker` returns the same list, so `dim` and `original` are
two names for one grid. A comprehension that builds new rows,
`[[v // 2 for v in row] for row in photo]`, leaves `original` as it
was.

</details>

## Moves

**4.** Which matrix sends "right", $(1, 0)$, to $(2, 1)$, and "up",
$(0, 1)$, to $(0, 1)$? What does it do to the area of a shape?

<details class="dl-answer"><summary>answer</summary>

The columns are where "right" and "up" go, so it is
$\begin{bmatrix} 2 & 0 \\ 1 & 1 \end{bmatrix}$. Its determinant is
$2 \times 1 - 0 \times 1 = 2$, so it doubles every area.

</details>

**5.** A sprite is mirrored left to right, `[[-1, 0], [0, 1]]`, and
then given a quarter turn, `[[0, -1], [1, 0]]`. Which one matrix does
both? Is the result a turn or a mirror?

```python exec
id: mixed-matrices-mirror-turn
```

<details class="dl-answer"><summary>answer</summary>

Put the first move on the right. `multiply([[0, -1], [1, 0]], [[-1,
0], [0, 1]])` is `[[0, -1], [-1, 0]]`. Its determinant is $-1$, so it
is a mirror. It sends $(x, y)$ to $(-y, -x)$, which mirrors in the line
$y = -x$.

</details>

**6.** The shear `[[1, 1], [0, 1]]` has determinant 1, like a turn. Does
it keep every area? Does it keep every length?

<details class="dl-answer"><summary>answer</summary>

It keeps every area, because its determinant is 1. It does not keep
lengths. "Up", $(0, 1)$, goes to $(1, 1)$, which has length
$\sqrt{2}$. A determinant of 1 says only that areas stay the same.

</details>

**7.** What is the eighth power of the shear `[[1, 1], [0, 1]]`? And of
a turn by 45°?

```python exec
id: mixed-matrices-powers
```

<details class="dl-answer"><summary>answer</summary>

`np.linalg.matrix_power(np.array([[1, 1], [0, 1]]), 8)` is
`[[1, 8], [0, 1]]`: each shear adds one more lean. Eight turns of 45°
make a whole turn, so that power is the identity, up to rounding.

</details>

## Undoing and solving

**8.** What is the inverse of $\begin{bmatrix} 2 & 0 \\ 1 & 1
\end{bmatrix}$? Check it by multiplying.

<details class="dl-answer"><summary>answer</summary>

Swap the diagonal, change the signs of the other two, and divide by the
determinant, 2: $\begin{bmatrix} 0.5 & 0 \\ -0.5 & 1 \end{bmatrix}$.
`multiply` of the two, in either order, is the identity.

</details>

**9.** For each system, is there one solution, none, or infinitely
many? Decide without solving.

(a) $x + 2y = 3$ and $2x + 4y = 6$
(b) $x + 2y = 3$ and $2x + 4y = 7$
(c) $x + 2y = 3$ and $2x + 3y = 7$

<details class="dl-answer"><summary>answer</summary>

(a) Infinitely many. The second equation is the first times 2, so the
two lines are the same line.
(b) None. The left-hand sides are in the same ratio, but the right-hand
sides are not, so the lines are parallel.
(c) One. The coefficients have determinant $1 \times 3 - 2 \times 2 =
-1$, which is not 0.

</details>

**10.** `inverse` works for 2×2 matrices only. How would you find the
point that `[[1, 2, 0], [0, 1, 1], [1, 0, 1]]` sends to $(5, 2, 4)$?

<details class="dl-answer"><summary>answer</summary>

Solve it as a system: `solve([[1, 2, 0, 5], [0, 1, 1, 2], [1, 0, 1,
4]])`, or `np.linalg.solve` with the matrix and `[5, 2, 4]`. Both give
$(3, 1, 1)$. Check it: $3 + 2 = 5$, $1 + 1 = 2$ and
$3 + 1 = 4$.

</details>

**11.** $B = \begin{bmatrix} 1 & 1 \\ 1 & 1.0001 \end{bmatrix}$ has an
inverse. Why might a program that undoes $B$ still give answers you
cannot trust?

<details class="dl-answer"><summary>answer</summary>

Its determinant is only 0.0001, because its columns point in nearly the
same direction. Undoing it multiplies tiny changes in the input, such
as rounding, by thousands. The answer is exact for the numbers you give
it, but a nudge in the fourth decimal place moves it by a whole unit.

</details>

## Code and speed

**12.** `dot([1, 2, 3], [4, 5])` gives 14 with a `dot` built on `zip`.
Why is that a problem, and how does the `dot` that `multiply` uses guard
against it?

<details class="dl-answer"><summary>answer</summary>

`zip` stops at the end of the shorter list, so the 3 is never used, and
Python says nothing. The lists should have been the same length. A
check that the lengths match, raising a `ValueError` when they do not,
turns the silent wrong answer into an error.

</details>

**13.** With two 2×2 NumPy arrays $R = \begin{bmatrix} 1 & 2 \\ 3 & 4
\end{bmatrix}$ and $Q = \begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}$,
what do `R * Q` and `R @ Q` print?

<details class="dl-answer"><summary>answer</summary>

`R * Q` multiplies entry by entry: `[[0 2] [3 0]]`. `R @ Q` is the
matrix product: `[[2 1] [4 3]]`, which swaps the columns of $R$.

</details>

**14.** A 100×100 multiply with your `multiply` takes 0.05 seconds on
one computer. About how long would a 300×300 multiply take?

<details class="dl-answer"><summary>answer</summary>

About 1.35 seconds. Three times the size is $3 \times 3 \times 3 = 27$
times the multiplications, and $27 \times 0.05 = 1.35$.

</details>

## Chains

**15.** A light is either on or off each minute. When it is on, it
stays on 90% of the time. When it is off, it comes on 30% of the time.
In the long run, what share of the minutes is it on? Use `solve`.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The transition matrix is $\begin{bmatrix} 0.9 & 0.1 \\ 0.3 & 0.7
   \end{bmatrix}$.
2. Write $\boldsymbol{\pi} = [p, q]$. The first column of
   $\boldsymbol{\pi}P = \boldsymbol{\pi}$ says $0.9p + 0.3q = p$.
3. Move everything to the left, and add $p + q = 1$.

</details>

<details class="dl-answer"><summary>answer</summary>

$\frac{3}{4}$ of the minutes. The first column gives $-0.1p + 0.3q = 0$,
and `solve([[-0.1, 0.3, 0], [1, 1, 1]])` gives
`[0.7499999999999999, 0.25]`. Running the chain with `multiply` many
times, or `np.linalg.matrix_power` with a large power, settles on the
same numbers.

</details>
