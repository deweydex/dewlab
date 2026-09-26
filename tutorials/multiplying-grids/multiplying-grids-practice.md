---
title: "Matrix multiplication: rows times columns — Practice"
practice_for: multiplying-grids
year: "2026-2027"
version: 2026.09.26.1
worlds:
  pixel-art: Pictures made of small squares, the way a screen draws them.
  starships: Starships, and the structures they are built from.
  space-scenes: Stars, planets and the paths they take across the sky.
---

# Matrix multiplication: rows times columns — Practice

Problems on dot products, shapes and products, and three from earlier
pages. Find each answer by hand before you run anything. Your own
`dot`, `multiply` and the functions from the earlier pages are already
loaded.

## Dot products

```python exec
id: dot-1
print(dot([2, -3, 1], [4, 0, -2]))
```

**1.** Find `dot([1, 2, 3], [1, 2, 3])`. What does the dot product
of a list with itself tell you?

<details class="dl-answer"><summary>answer</summary>

It is $1 + 4 + 9 = 14$, the sum of the squares. Its square root is the length
of the arrow from $(0, 0, 0)$ to $(1, 2, 3)$, its *magnitude*, so a
dot product with itself measures how long a vector is.

</details>

**2.** Find `dot([1, 1], [1, -1])`. Draw the two arrows from
$(0, 0)$. What do you notice?

<details class="dl-answer"><summary>answer</summary>

$1 - 1 = 0$, and the two arrows are at right angles. Two vectors whose
dot product is 0 are *orthogonal*. For arrows in a plane or in space,
that means at right angles.

</details>

## Shapes first

**3.** For each pair, can the left be multiplied by the right? If so,
what shape is the result?

| Left | Right |
|---|---|
| 2×3 | 3×4 |
| 3×2 | 3×2 |
| 4×1 | 1×3 |
| 1×4 | 4×1 |

<details class="dl-answer"><summary>answer</summary>

- 2×3 by 3×4: yes, 2×4. The inner numbers match. The outer ones give
  the shape.
- 3×2 by 3×2: no. Two columns on the left, three rows on the right.
- 4×1 by 1×3: yes, 4×3. The 7 numbers you start with make 12 entries.
- 1×4 by 4×1: yes, 1×1. This single number is the dot product, written
  as a matrix.

</details>

## Products

```python exec
id: multiplying-1
A = [[2, 0, 1], [-1, 3, 2]]
B = [[1, 4], [0, -2], [3, 1]]
print(multiply(A, B))
```

```predict
type: number

What is the bottom-right entry of the product, row 2 of `A` dotted with
column 2 of `B`? It is the last number printed.
```

**4.** Find the top-left and bottom-right entries of `multiply(A, B)`
by hand.

<details class="dl-answer"><summary>answer</summary>

Top left: $2(1) + 0(0) + 1(3) = 5$. Bottom right: $-1(4) + 3(-2) + 2(1)
= -8$. The whole product is `[[5, 9], [5, -8]]`.

</details>

**5.** A layer of a neural network calculates $\mathbf{y} = W\mathbf{x} +
\mathbf{b}$, with $W = \begin{bmatrix} 0.2 & 0.8 \\ -0.5 & 0.3 \\ 0.1 &
0.6 \end{bmatrix}$, $\mathbf{x} = \begin{bmatrix} 1 \\ 2 \end{bmatrix}$
and $\mathbf{b} = \begin{bmatrix} 0.1 \\ -0.2 \\ 0.3 \end{bmatrix}$. What
is $\mathbf{y}$?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. $W$ is 3×2 and $\mathbf{x}$ is 2×1. What shape is $W\mathbf{x}$?
2. Each entry is one row of $W$ dotted with $[1, 2]$.
3. Then add $\mathbf{b}$, entry by entry, as in matrix addition on the
   first page.

**Think about:** $\mathbf{x}$ has 2 entries and $\mathbf{b}$ has 3. Why
is that not a problem?

</details>

<details class="dl-answer"><summary>answer</summary>

$W\mathbf{x} = \begin{bmatrix} 1.8 \\ 0.1 \\ 1.3 \end{bmatrix}$, so
$\mathbf{y} = \begin{bmatrix} 1.9 \\ -0.1 \\ 1.6 \end{bmatrix}$. Only the
inner numbers must agree: the columns of $W$ and the length of
$\mathbf{x}$. $\mathbf{b}$ matches the output, which can have a
different length.

</details>

## Order and grouping

```python exec
id: order-1
R = [[1, 2], [3, 4]]
S = [[5, 0], [1, -1]]
print("RS =", multiply(R, S))
print("SR =", multiply(S, R))
```

**6.** Are `RS` and `SR` the same? And is $(AB)C$ always the same as
$A(BC)$?

<details class="dl-answer"><summary>answer</summary>

`RS` is `[[7, -2], [19, -4]]` and `SR` is `[[5, 10], [-2, -2]]`. They
differ in every entry. But the grouping never matters. $(AB)C =
A(BC)$, because both do $C$ first, then $B$, then $A$. Multiplication is
*associative*. That is why a chain of moves can be multiplied into one
matrix ahead of time, in any grouping.

</details>

**7.** Can you write `identity(n)`, which builds the $n \times n$
identity matrix?

```python exec
id: multiply-identity
def identity(n):
    """The n x n identity matrix: ones down the diagonal, zeros elsewhere."""
    ...


print(identity(3))
```

```inputs
identity(1)
identity(3)
multiply(identity(2), R) == R
```

```hint
Row `i` has a 1 in position `i` and 0 everywhere else. For each `j`,
that is `1 if i == j else 0`.
```

```solution
def identity(n):
    """The n x n identity matrix: ones down the diagonal, zeros elsewhere."""
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]


print(identity(3))
---
The outer comprehension makes a row for each `i`. The inner one fills
it with a number for each `j`.
```

**8.** $A$ is $m \times n$ and $B$ is $n \times m$, so both $AB$ and $BA$
exist. Are they the same shape?

<details class="dl-answer"><summary>answer</summary>

$AB$ is $m \times m$ and $BA$ is $n \times n$. Unless $m = n$, they
cannot be equal. You can tell without looking at a single entry.

</details>

**9.** Why does multiplication need only the inner numbers to match,
when addition needs the whole shape to?

<details class="dl-answer"><summary>answer</summary>

Multiplication pairs a row of the left matrix with a column of the
right, and a dot product needs only its two lists to be the same length.
The most useful products have different shapes: a 2×2 move times a
2×10 matrix of corners, or a layer's weights times a column of inputs.

</details>

## Your world

**10.** A product from the world you chose.

<div class="dl-world" data-world="pixel-art">

A sprite is made twice as wide, and then turned a quarter. Is that the
same as turning it first, and then making it twice as wide? Predict,
then check with `multiply`.

```python exec
id: multiply-world--pixel-art
wide = [[2, 0], [0, 1]]
turn = [[0, -1], [1, 0]]
```

```hint
"wide, then turn" is `multiply(turn, wide)`. Compare it with
`multiply(wide, turn)`.
```

```solution
wide = [[2, 0], [0, 1]]
turn = [[0, -1], [1, 0]]
print(multiply(turn, wide))
print(multiply(wide, turn))
---
The two products are `[[0, -1], [2, 0]]` and `[[0, -2], [1, 0]]`. If you
widen and then turn, the sprite is tall. If you turn and then widen, it
is wide. A stretch in one direction and a turn give a different picture
in each order.
```

</div>

<div class="dl-world" data-world="starships">

A space station's ring is drawn as a circle of points. Squashing it to
half height makes an ellipse, the way a ring looks seen at an angle.
Then the view turns 90°. Can you make the one matrix for "squash, then
turn", and say what shape the ring becomes?

```python exec
id: multiply-world--starships
import math

ring = [(math.cos(math.radians(a)), math.sin(math.radians(a))) for a in range(0, 360, 30)]
squash = [[1, 0], [0, 0.5]]
turn = [[0, -1], [1, 0]]
```

```hint
Put the first move on the right, as in `multiply(turn, squash)`. Draw the
ring and the moved ring with `draw_shapes`.
```

```solution
import math

ring = [(math.cos(math.radians(a)), math.sin(math.radians(a))) for a in range(0, 360, 30)]
squash = [[1, 0], [0, 0.5]]
turn = [[0, -1], [1, 0]]
both = multiply(turn, squash)
print(both)
draw_shapes([ring, transform_all(both, ring)])
---
The matrix is `[[0, -0.5], [1, 0]]`. The squash makes the ring wider
than tall, and the turn stands it up, taller than wide. Its second
column, where "up" goes, has length a half. That is the squash, carried
through the turn.
```

</div>

<div class="dl-world" data-world="space-scenes">

A planet goes round its star once every 12 time steps, turning 30° each
step. Starting from $(1, 0)$, where is it after 3 steps? Build the
3-step matrix by multiplying the one-step matrix by itself.

```python exec
id: multiply-world--space-scenes
import math

angle = math.radians(30)
step = [[math.cos(angle), -math.sin(angle)], [math.sin(angle), math.cos(angle)]]
```

```hint
`multiply(step, multiply(step, step))` is three steps. Then use
`transform` on `(1, 0)`, and round the answer.
```

```solution
import math

angle = math.radians(30)
step = [[math.cos(angle), -math.sin(angle)], [math.sin(angle), math.cos(angle)]]
three_steps = multiply(step, multiply(step, step))
x, y = transform(three_steps, (1, 0))
print(round(x, 6), round(y, 6))
---
The planet is at $(0, 1)$, a quarter of the way round. Three 30° turns
make one 90° turn.
A simulation that moves a planet with the same small matrix at every
step builds up the orbit the same way, one multiplication at a time.
```

</div>

## From earlier

**11.** From *Matrices: adding, scaling and transposing*. Is the
transpose of a product the product of the transposes, in the same
order? Try it on `R` and `S`.

<details class="dl-answer"><summary>answer</summary>

No. $(RS)^T = S^T R^T$, the other way round. `transpose(multiply(R, S))`
equals `multiply(transpose(S), transpose(R))`. A row of $R$ with a
column of $S$ becomes, after transposing, a row of $S^T$ with a column
of $R^T$.

</details>

**12.** From *what a matrix does to a picture*. Every matrix sends
$(0, 0)$ to $(0, 0)$. Does every product of matrices too?

<details class="dl-answer"><summary>answer</summary>

Yes. The product is two moves, and each leaves $(0, 0)$ where it is.

</details>

**13.** From *Repeating steps with loops*. To multiply two 3×3 matrices,
how many multiplications of single numbers does `multiply` do? And for
two 100×100 matrices?

<details class="dl-answer"><summary>answer</summary>

Each of the 9 entries is a dot product of 3 pairs, so 27. For 100×100, it
is $100 \times 100 \times 100 = 1{,}000{,}000$. Double the size and the
work goes up eight times, which is why the NumPy page at the end of the
series times one.

</details>
