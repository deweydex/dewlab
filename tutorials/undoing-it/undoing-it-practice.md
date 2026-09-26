---
title: "Inverse matrices: undoing a transformation — Practice"
practice_for: undoing-it
year: "2026-2027"
version: 2026.09.26.1
worlds:
  starships: Starships, and the structures they are built from.
  space-scenes: Stars, planets and the paths they take across the sky.
  pixel-art: Pictures made of small squares, the way a screen draws them.
---

# Inverse matrices: undoing a transformation — Practice

Work out each determinant by hand before you run anything: two
multiplications and a subtraction, until it is automatic. Your own
`det`, `inverse` and the functions from the earlier pages are already
loaded.

## Determinants

```python exec
id: determinants-1
print(det([[3, 2], [1, 4]]))
print(det([[5, -1], [10, -2]]))
```

**1.** Work out $\det\begin{bmatrix} 3 & 2 \\ 1 & 4 \end{bmatrix}$ and
$\det\begin{bmatrix} 5 & -1 \\ 10 & -2 \end{bmatrix}$ by hand. Is there a
link between the second matrix's columns that could have told you its
answer first?

<details class="dl-answer"><summary>answer</summary>

$3(4) - 2(1) = 10$, and $5(-2) - (-1)(10) = 0$. The second column,
$(-1, -2)$, is the first, $(5, 10)$, times $-\frac{1}{5}$: "right" and
"up" land on the same line, so everything does, and the area is 0.

</details>

**2.** A matrix has $\det = -4$. Does it have an inverse?

<details class="dl-answer"><summary>answer</summary>

Yes. Only exactly 0 rules an inverse out. $-4$ means it scales areas by
4 and flips the picture over; its inverse scales by $\frac{1}{4}$ and
flips it back.

</details>

## Inverses

**3.** Find the inverse of $\begin{bmatrix} 3 & 2 \\ 1 & 4 \end{bmatrix}$
with the formula, then multiply the two together.

```python exec
id: inverses-1
A = [[3, 2], [1, 4]]
print(inverse(A))
print(multiply(A, inverse(A)))
```

```predict
Will the second line be exactly `[[1.0, 0.0], [0.0, 1.0]]`?

- Yes
  - A matrix times its inverse is the identity.
- No, but very close
  - Dividing by 10 leaves tiny rounding errors.
```

<details class="dl-answer"><summary>why</summary>

The inverse is `[[0.4, -0.2], [-0.1, 0.3]]`, and the product comes out
as `[[1.0000000000000002, -1.1102230246251565e-16], [0.0, 1.0]]`: the
identity, give or take rounding in the sixteenth decimal place, the same
kind that makes `0.1 + 0.2 == 0.3` false. Compare such numbers after
rounding them, or with `math.isclose`.

</details>

**4.** Solve $A\mathbf{x} = \mathbf{b}$ with $A = \begin{bmatrix} 2 & 1 \\
5 & 3 \end{bmatrix}$ and $\mathbf{b} = (4, 9)$, by undoing $A$. Can you
write `solve2(a, b)`, which gives the point that $A$ sends to $\mathbf{b}$?

```python exec
id: undoing-solve2
def solve2(a, b):
    """The point p with transform(a, p) == b, for a 2x2 matrix a."""
    ...


print(solve2([[2, 1], [5, 3]], (4, 9)))
```

```inputs
solve2([[2, 1], [5, 3]], (4, 9))
solve2([[1, 0], [0, 2]], (3, 4))
```

```hint
Where did the point start, before $A$ moved it to $\mathbf{b}$? Undo
$A$: `transform(inverse(a), b)`.
```

```solution
def solve2(a, b):
    """The point p with transform(a, p) == b, for a 2x2 matrix a."""
    return transform(inverse(a), b)


print(solve2([[2, 1], [5, 3]], (4, 9)))
---
$(3.0, -2.0)$. Check it by moving it forwards: $2(3) + 1(-2) = 4$ and
$5(3) + 3(-2) = 9$. The next page does this for any number of unknowns,
without an inverse at all.
```

## Products and determinants

**5.** $\det(A) = 5$ and $\det(B) = 3$. What is $\det(AB)$? And if
$\det(AB) = 0$, must both determinants be 0?

<details class="dl-answer"><summary>answer</summary>

15: doing $B$ then $A$ scales areas by 3 and then by 5. And no: one zero
is enough. If either move flattens the picture, the other cannot
unflatten it, before or after.

</details>

**6.** Two matrices, both with determinant $0.0001$:
$A = \begin{bmatrix} 0.01 & 0 \\ 0 & 0.01 \end{bmatrix}$ and
$B = \begin{bmatrix} 1 & 1 \\ 1 & 1.0001 \end{bmatrix}$. Undo each one on
a point, then nudge the point by $0.0001$ and undo it again. Which
answer moves more?

```python exec
id: undoing-ill-conditioned
A = [[0.01, 0], [0, 0.01]]
B = [[1, 1], [1, 1.0001]]
print(transform(inverse(B), (2, 2.0001)), transform(inverse(B), (2, 2.0002)))
print(transform(inverse(A), (0.02, 0.02)), transform(inverse(A), (0.02, 0.0201)))
```

<details class="dl-answer"><summary>why</summary>

With $B$, a change in the fourth decimal place moves the answer from
about $(1, 1)$ to about $(0, 2)$, a whole unit. With $A$, the answer
moves only 100 times the nudge, because $A$ shrinks everything evenly.
$B$'s columns point in nearly the same direction, so it squashes the
plane almost flat, and undoing it means pulling apart two directions
that are almost one. A matrix like $B$ is *ill-conditioned*: it has an
inverse, but tiny changes in its input, such as rounding, make large
changes in what comes back.

</details>

## Your world

**7.** Undoing, or not, in the world you chose.

<div class="dl-world" data-world="starships">

Two ships each record their manoeuvre as one matrix. Ship A's is
`[[2, 1], [1, 1]]` and ship B's is `[[2, 1], [4, 2]]`. Which ship can fly
back along its path, and what does the other one's matrix do to it?

```python exec
id: undoing-world--starships
ship = [(0, 4), (1, 1), (2, -1), (1, -0.5), (-1, -0.5), (-2, -1), (-1, 1)]
ship_a = [[2, 1], [1, 1]]
ship_b = [[2, 1], [4, 2]]
```

```hint
Work out both determinants. Then draw each ship after its manoeuvre.
```

```solution
ship = [(0, 4), (1, 1), (2, -1), (1, -0.5), (-1, -0.5), (-2, -1), (-1, 1)]
ship_a = [[2, 1], [1, 1]]
ship_b = [[2, 1], [4, 2]]
print(det(ship_a), det(ship_b))
draw_shapes([ship, transform_all(ship_a, ship), transform_all(ship_b, ship)])
---
Ship A's determinant is 1: it leans and stretches, but keeps its area,
and `inverse` brings it back. Ship B's is 0: every point lands on the
line $y = 2x$, and the ship is a streak with no width. Its second row
is twice its first, the telltale sign.
```

</div>

<div class="dl-world" data-world="space-scenes">

A telescope's camera stretches the sky: every picture is 1.5 times too
wide and 0.8 times too tall. Which matrix undoes it, and what is its
determinant?

```python exec
id: undoing-world--space-scenes
camera = [[1.5, 0], [0, 0.8]]
```

```hint
`inverse(camera)`, and `det` of both.
```

```solution
camera = [[1.5, 0], [0, 0.8]]
print(inverse(camera))
print(det(camera), det(inverse(camera)))
---
`[[0.667, 0], [0, 1.25]]`, rounded: squash the width by 1.5 and stretch
the height by 1.25. The determinants are 1.2 and about 0.833, which
multiply to 1: the camera grows areas by 1.2, and the fix shrinks them
back.
```

</div>

<div class="dl-world" data-world="pixel-art">

A mirror is its own undo: flip a sprite twice, and it is back where it
started. Which of these are their own inverse: the mirror left to
right, the quarter turn, the half turn, and the swap of x and y?

```python exec
id: undoing-world--pixel-art
moves = {
    "mirror": [[-1, 0], [0, 1]],
    "quarter turn": [[0, -1], [1, 0]],
    "half turn": [[-1, 0], [0, -1]],
    "swap": [[0, 1], [1, 0]],
}
```

```hint
A matrix is its own inverse when multiplying it by itself gives the
identity.
```

```solution
moves = {
    "mirror": [[-1, 0], [0, 1]],
    "quarter turn": [[0, -1], [1, 0]],
    "half turn": [[-1, 0], [0, -1]],
    "swap": [[0, 1], [1, 0]],
}
for name in moves:
    print(name, multiply(moves[name], moves[name]) == [[1, 0], [0, 1]])
---
The mirror, the half turn and the swap are their own inverses; the
quarter turn is not, since twice a quarter turn is a half turn. Every
flip undoes itself, and so does the half turn: two half turns are a
whole turn.
```

</div>

## From earlier

**8.** From *Matrix multiplication*. $(AB)^{-1}$ undoes "$B$, then $A$".
Is it $A^{-1}B^{-1}$ or $B^{-1}A^{-1}$?

<details class="dl-answer"><summary>answer</summary>

$B^{-1}A^{-1}$: to undo putting on socks and then shoes, take off the
shoes first. The last move is the first to be undone. Try it in a cell
with two of your own matrices.

</details>

**9.** From *what a matrix does to a picture*. The columns of `turn` are
where "right" and "up" go. What are the columns of `inverse(turn)`?

<details class="dl-answer"><summary>answer</summary>

$(0, -1)$ and $(1, 0)$: where "right" and "up" go when the F is turned
back, a quarter clockwise. Reading columns works for inverses too.

</details>

**10.** From *Reading an error message*. `inverse([[2, 4], [1, 2]])`
raises your own `ValueError`. Without the `if d == 0` check, what error
would Python raise, and where?

<details class="dl-answer"><summary>answer</summary>

A `ZeroDivisionError`, on the line that divides by `d`. It would be true
but less helpful: it says a division failed, not that the matrix
flattens the plane. The check turns the symptom into the reason.

</details>
