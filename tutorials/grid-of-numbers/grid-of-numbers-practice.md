---
title: "Matrices: adding, scaling and transposing a grid of numbers — Practice"
practice_for: grid-of-numbers
year: "2026-2027"
version: 2026.09.26.1
worlds:
  pixel-art: Pictures made of small squares, the way a screen draws them.
  photos: Photographs, and the filters that change them.
datasets: [grace-hopper]
---

# Matrices: adding, scaling and transposing a grid of numbers — Practice

Problems on reading, adding, scaling and transposing matrices, and three
from earlier pages. Work each one out by hand first, even the arithmetic
ones, then check it in a cell. Your own `add`, `scale`, `transpose` and
`show` from the tutorial are already loaded on this page.

## Reading a matrix

```python exec
id: reading-1
A = [[4, 7, -2], [1, 0, 6], [-3, 5, 8]]
print(A)
```

**1.** What are the dimensions of `A`? And what are $a_{12}$, $a_{23}$
and $a_{32}$?

<details class="dl-answer"><summary>answer</summary>

`A` is 3×3. $a_{12} = 7$, $a_{23} = 6$ and $a_{32} = 5$, which in Python
are `A[0][1]`, `A[1][2]` and `A[2][1]`. Maths counts from 1 and Python
from 0. Mixing the two is the commonest mistake here.

</details>

**2.** Write the second row of `A` as a list, and then the third column.

<details class="dl-answer"><summary>answer</summary>

The second row is `A[1]`, `[1, 0, 6]`. The third column is `[-2, 6, 8]`:
a list of lists has no shortcut for a column, so we collect it one row at
a time, `[row[2] for row in A]`.

</details>

## Adding and scaling

```python exec
id: adding-1
X = [[2, 0, -1], [3, 1, 4]]
Y = [[-1, 2, 0], [1, -3, 2]]
print(add(X, Y))
```

**3.** Calculate $2X - Y$ by hand, then $X - 2Y$. Are they the same?

<details class="dl-answer"><summary>answer</summary>

$2X - Y = \begin{bmatrix} 5 & -2 & -2 \\ 5 & 5 & 6 \end{bmatrix}$ and
$X - 2Y = \begin{bmatrix} 4 & -4 & -1 \\ 1 & 7 & 0 \end{bmatrix}$. There
is no reason for them to agree, any more than $2(3) - 5$ and $3 - 2(5)$
do.

</details>

**4.** Can you write `subtract(a, b)` with no loop at all, using only
`add` and `scale`?

```python exec
id: grid-subtract
def subtract(a, b):
    """A new matrix: b taken away from a, position by position."""
    ...


print(subtract(X, Y))
```

```inputs
subtract(X, Y)
subtract([[5]], [[5]])
subtract([[1, 2]], [[3, 5]])
```

```hint
Subtracting `b` is the same as adding minus `b`. Which scalar turns `b`
into minus `b`?
```

```solution
def subtract(a, b):
    """A new matrix: b taken away from a, position by position."""
    return add(a, scale(-1, b))


print(subtract(X, Y))
---
One line, built from two operations you already trust, and it inherits
`add`'s shape check for free.
```

**5.** A layer of a neural network updates its weights with
$W_{\text{new}} = W_{\text{old}} - \alpha G$, where $\alpha = 0.1$. With
$W_{\text{old}} = \begin{bmatrix} 0.5 & -0.3 \\ 1.2 & 0.8 \end{bmatrix}$
and $G = \begin{bmatrix} 0.4 & -0.2 \\ 0.6 & 1.0 \end{bmatrix}$, what is
$W_{\text{new}}$?

<details class="dl-answer"><summary>answer</summary>

$\alpha G = \begin{bmatrix} 0.04 & -0.02 \\ 0.06 & 0.10 \end{bmatrix}$, so
$W_{\text{new}} = \begin{bmatrix} 0.46 & -0.28 \\ 1.14 & 0.70
\end{bmatrix}$. Each weight moves a small step against its entry in $G$:
one `scale` and one subtraction, repeated millions of times, is how a
network is trained.

</details>

## The shape rule and the transpose

```python exec
id: shape-1
P = [[1, 2], [3, 4], [5, 6]]
Q = [[1, 2, 3], [4, 5, 6]]
print("P is", len(P), "by", len(P[0]), "and Q is", len(Q), "by", len(Q[0]))
print(transpose(Q) == P)
```

```predict
Will `transpose(Q)` be the same as `P`?

- True
  - Q has the shape of P turned sideways.
- False
  - The shape is right, but the numbers are in different places.
```

**6.** Can Python add `P` and `Q`? If not, what shape would `Q` need to be?

<details class="dl-answer"><summary>answer</summary>

No: `P` is 3×2 and `Q` is 2×3, and addition needs the same shape. The
same number of entries is not enough. And `transpose(Q)` is 3×2, but
it is `[[1, 4], [2, 5], [3, 6]]`, not `P`: the right shape with the
numbers in other places.

</details>

**7.** If $M$ is 4×7, what shape is $M^T$? And what does the transpose of
an *upper-triangular* matrix look like, one with zeros everywhere below
the diagonal?

<details class="dl-answer"><summary>answer</summary>

7×4: the transpose swaps the two dimensions. The zeros below the
diagonal move above it, so the transpose is *lower-triangular*. The
diagonal itself never moves.

</details>

**8.** Can you write `is_symmetric(m)`, which says whether a matrix is its
own transpose?

```python exec
id: grid-is-symmetric
def is_symmetric(m):
    """True when m is the same as its own transpose."""
    ...


print(is_symmetric([[2, -3], [-3, 5]]))
```

```inputs
is_symmetric([[2, -3], [-3, 5]])
is_symmetric([[1, 2], [3, 4]])
is_symmetric([[1, 2, 3]])
is_symmetric([[7]])
```

```solution
def is_symmetric(m):
    """True when m is the same as its own transpose."""
    return transpose(m) == m


print(is_symmetric([[2, -3], [-3, 5]]))
---
A 1×3 matrix is never symmetric. Its transpose is 3×1, a different
shape, so `==` is `False` at once. Only a square matrix can be symmetric.
```

**9.** Is scaling and then transposing the same as transposing and then
scaling?

<details class="dl-answer"><summary>answer</summary>

Yes. Scaling multiplies each entry on its own, and transposing only
moves entries. Neither one combines two entries, so the order cannot
matter. Matrix multiplication does combine entries, and there the order
matters. It comes two pages later.

</details>

**10.** An image classifier sorts pictures into Cat, Dog and Bird. Its
*confusion matrix* has the true label as rows and the classifier's
answer as columns, in that order:
$C = \begin{bmatrix} 850 & 30 & 20 \\ 15 & 920 & 25 \\ 10 & 20 & 970
\end{bmatrix}$. How many dogs were called birds, and what share of all
the answers were right?

<details class="dl-answer"><summary>answer</summary>

25, in row 2 (Dog), column 3 (Bird). The diagonal holds the right
answers: $\frac{850 + 920 + 970}{2860} = \frac{2740}{2860} \approx
95.8\%$. A matrix can store data without ever being added or multiplied.

</details>

## Your world

**11.** A new operation from the three you have.

<div class="dl-world" data-world="pixel-art">

`mirror(m)` reverses each row, a mirror left to right. Transposing and
mirroring are both flips. What do you get if you transpose the F and then
mirror it? And mirror it, then transpose?

```python exec
id: grid-world--pixel-art
flag = [
    [9, 9, 9, 9],
    [9, 0, 0, 0],
    [9, 9, 9, 0],
    [9, 0, 0, 0],
    [9, 0, 0, 0],
]


def mirror(m):
    """A new matrix: each row of m reversed, a mirror left to right."""
    return [row[::-1] for row in m]


show(mirror(transpose(flag)))
```

```predict
What does transposing and then mirroring do to the F?

- A quarter turn clockwise
  - Two flips across lines that meet at an angle make a turn.
- A half turn
  - Two flips, twice as far.
- A mirror image of the F
  - Two flips are still a flip.
```

<details class="dl-answer"><summary>why</summary>

A quarter turn clockwise. Mirroring first and then transposing turns it
a quarter anticlockwise. Two flips across lines that meet at 45° make a
turn of 90°, and the order decides which way it turns. The page after
next looks at this closely.

</details>

</div>

<div class="dl-world" data-world="photos">

A photographic *negative* swaps light and dark: 0 becomes 255, and 255
becomes 0. Can you make the negative of the portrait with `add` and
`scale`, and no loop of your own?

```python exec
id: grid-world--photos
import matplotlib.pyplot as plt

text = await load_text("grace-hopper.csv")
photo = [[int(value) for value in line.split(",")] for line in text.splitlines()]
white = [[255] * 60 for i in range(70)]


def negative(picture):
    """A new picture: every value v becomes 255 - v."""
    ...
```

```inputs
negative([[0, 255, 100]])
negative(photo)[0][:3]
```

```hint
255 − v is the white picture plus minus the photo: `add(white, scale(-1,
picture))`. For a picture of another size, `white` would need to match
it.
```

```solution
import matplotlib.pyplot as plt

text = await load_text("grace-hopper.csv")
photo = [[int(value) for value in line.split(",")] for line in text.splitlines()]
white = [[255] * 60 for i in range(70)]


def negative(picture):
    """A new picture: every value v becomes 255 - v."""
    white = [[255] * len(picture[0]) for row in picture]
    return add(white, scale(-1, picture))


plt.imshow(negative(photo), cmap="gray", vmin=0, vmax=255)
plt.axis("off")
---
The white picture has to be the same shape as the one it is added to,
so the solution builds one to fit. `[[255] * 60 for i in range(70)]`
makes 70 separate rows. `[[255] * 60] * 70` would make one row shared 70
times, the aliasing trap. It would do no harm here only because `add`
never changes its inputs.
```

</div>

## From earlier

**12.** From *Comprehensions, grids and aliasing*. What does this print?

```python exec
id: grid-from-earlier-aliasing
grid = [[0] * 3] * 3
grid[0][0] = 5
print(grid)
```

```predict
What will it print?

- [[5, 0, 0], [0, 0, 0], [0, 0, 0]]
  - Only the first row's first number was changed.
- [[5, 0, 0], [5, 0, 0], [5, 0, 0]]
  - The three rows are one row, three times.
```

<details class="dl-answer"><summary>why</summary>

`[[5, 0, 0], [5, 0, 0], [5, 0, 0]]`. `* 3` copies the reference to one
list three times, so there is one row with three names. This is why the
tutorial's functions build a new list for every row.

</details>

**13.** From *Reading an error message*. Drawing `scale(2, pixels)` with
the ten-character `ramp` raised `IndexError: string index out of
range`. Which line would the traceback point to, and why is the error
true but not the whole story?

<details class="dl-answer"><summary>answer</summary>

The line `ramp[value]`, where 18 is past the last character. The error
is true, because there is no `ramp[18]`. But the cause is earlier, in
`scale`, which made numbers larger than the picture can draw. A
traceback points to where Python noticed the problem. The mistake may
be on an earlier line.

</details>

**14.** From *Repeating steps with loops*. How many times does the
inner line run when `add` adds two 70×60 pictures?

<details class="dl-answer"><summary>answer</summary>

$70 \times 60 = 4{,}200$ times, once for every position. A photo
1,000 pixels square needs 1,000,000 additions. The NumPy page at the end
of the series shows a faster way.

</details>
