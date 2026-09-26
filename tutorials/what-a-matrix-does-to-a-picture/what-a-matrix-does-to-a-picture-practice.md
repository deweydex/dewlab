---
title: "Matrix transformations: what a matrix does to a picture — Practice"
practice_for: what-a-matrix-does-to-a-picture
year: "2026-2027"
version: 2026.09.26.1
worlds:
  pixel-art: Pictures made of small squares, the way a screen draws them.
  starships: Starships, and the structures they are built from.
  space-scenes: Stars, planets and the paths they take across the sky.
---

# Matrix transformations: what a matrix does to a picture — Practice

Before you run anything, predict the picture from the matrix, or the
matrix from the picture. The prediction is the practice, and the plot
checks it. Your own `transform`, `transform_all` and `draw_shapes`
are already loaded, and so are the functions from the page before.

```python exec
id: reading-1
F = [(0, 0), (1, 0), (1, 2), (2, 2), (2, 3), (1, 3), (1, 4), (3, 4), (3, 5), (0, 5)]
m = [[3, 0], [0, 3]]
draw_shapes([F, transform_all(m, F)])
```

## Reading the columns

**1.** Where does $\begin{bmatrix} 3 & 0 \\ 0 & 3 \end{bmatrix}$ send
$(1, 0)$ and $(0, 1)$? What does it do to the F?

<details class="dl-answer"><summary>answer</summary>

$(1, 0) \to (3, 0)$ and $(0, 1) \to (0, 3)$, read from the two columns.
Both directions grow by the same amount, a *uniform scaling*: the F
three times as big, the same shape.

</details>

**2.** Where does $\begin{bmatrix} -1 & 0 \\ 0 & 1 \end{bmatrix}$ send
$(1, 0)$ and $(0, 1)$, and which way does the F face afterwards?

<details class="dl-answer"><summary>answer</summary>

$(1, 0) \to (-1, 0)$, and $(0, 1)$ stays put. Every x changes sign and
every y stays, so the F is mirrored left to right. Its arms point left.

</details>

**3.** What matrix turns every point 180° about $(0, 0)$?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. A half turn sends $(1, 0)$ to the point opposite it. Which point?
2. And $(0, 1)$?
3. Those two answers are the two columns, in order.

**Think about:** a half turn is the same as scaling by $-1$ in every
direction. Does your matrix agree?

</details>

<details class="dl-answer"><summary>answer</summary>

$\begin{bmatrix} -1 & 0 \\ 0 & -1 \end{bmatrix}$. It sends $(1, 0)$ to
$(-1, 0)$ and $(0, 1)$ to $(0, -1)$. Every corner of the F moves to the
other side of the origin. The F is upside down with its arms pointing
left. This is a half turn, not a flip, because turning the page gets you
there.

</details>

**4.** Can you write the matrix that does each of these, and check it on
the F?

```python exec
id: matrix-four-moves
twice_as_tall = [[1, 0], [0, 1]]
lean_left = [[1, 0], [0, 1]]
half_turn = [[1, 0], [0, 1]]
swap_x_and_y = [[1, 0], [0, 1]]

draw_shapes([F, transform_all(lean_left, F)])
```

```inputs
transform(twice_as_tall, (1, 1))
transform(lean_left, (0, 2))
transform(half_turn, (1, 2))
transform(swap_x_and_y, (1, 2))
```

```hint
For each, decide where "right", $(1, 0)$, and "up", $(0, 1)$, should
go, and write those in as the two columns. Leaning left, the bottom stays
and the top slides left, so "up" goes to something like $(-0.5, 1)$.
```

```solution
twice_as_tall = [[1, 0], [0, 2]]
lean_left = [[1, -0.5], [0, 1]]
half_turn = [[-1, 0], [0, -1]]
swap_x_and_y = [[0, 1], [1, 0]]

draw_shapes([F, transform_all(lean_left, F)])
---
Any negative number in the top-right corner leans the F left, and a
half is one choice. The swap is the flip across the line $y = x$. It is
the transpose from the page before, done to points.
```

## Matrix and picture

**5.** What does $\begin{bmatrix} 1 & 0 \\ 0.5 & 1 \end{bmatrix}$ do to
the F? Predict, then draw it.

<details class="dl-answer"><summary>answer</summary>

$(1, 0) \to (1, 0.5)$ and $(0, 1)$ stays. The left edge stays where it
is, and each point rises by half its distance to the right, so the F's
arms tilt upwards. It is a shear in the other direction from the
tutorial's. There, the extra number was in the first row, and the x's
moved. Here it is in the second row, and the y's move.

</details>

**6.** Is there a matrix that sends every corner of the F to $(0, 0)$?

<details class="dl-answer"><summary>answer</summary>

Yes, $\begin{bmatrix} 0 & 0 \\ 0 & 0 \end{bmatrix}$, the *zero matrix*.
Both columns are $(0, 0)$, so "right" and "up" land on the origin, and
every other point is built from those two. Some matrices flatten a
picture onto a line. This one flattens it to a point. The page after
next asks which matrices can be undone, and this one cannot.

</details>

**7.** Two matrices both send $(1, 0)$ to $(2, 0)$. Must they be the same
matrix?

<details class="dl-answer"><summary>answer</summary>

No. That fixes only the first column. $\begin{bmatrix} 2 & 0 \\ 0 & 1
\end{bmatrix}$ and $\begin{bmatrix} 2 & 5 \\ 0 & 3 \end{bmatrix}$ both do
it, and differ everywhere else. To know a matrix, you need to know where
both "right" and "up" go.

</details>

**8.** Why does every 2×2 matrix send $(0, 0)$ to $(0, 0)$? What kind of
move would need more than a 2×2 matrix?

<details class="dl-answer"><summary>answer</summary>

$(a \times 0 + b \times 0, \; c \times 0 + d \times 0)$ is $(0, 0)$ for
any $a$, $b$, $c$ and $d$. So no 2×2 matrix can slide a picture across
the page, a *translation*. The graphics pages later in the course add a
third number to every point to make that possible.

</details>

## Your world

**9.** A move in the world you chose.

<div class="dl-world" data-world="pixel-art">

Italic letters lean. Can you find the matrix that turns the F into an
italic F, leaning right, with its bottom edge where it was and its top
shifted one square right?

```python exec
id: matrix-world--pixel-art
italic = [[1, 0], [0, 1]]
draw_shapes([F, transform_all(italic, F)])
```

```inputs
transform(italic, (0, 5))
transform(italic, (3, 0))
```

```hint
The top of the F is at height 5 and should move right by 1. So each
point moves right by a fifth of its height: "up" goes to $(0.2, 1)$.
```

```solution
italic = [[1, 0.2], [0, 1]]
draw_shapes([F, transform_all(italic, F)])
---
A shear. Fonts make italics roughly this way. A well-made italic font is
drawn letter by letter, because a shear makes the curved letters look
stretched.
```

</div>

<div class="dl-world" data-world="starships">

A ship flying away from the camera looks smaller and smaller. Can you
draw the ship at full size, half size and a quarter size, each with one
matrix?

```python exec
id: matrix-world--starships
ship = [(0, 4), (1, 1), (2, -1), (1, -0.5), (-1, -0.5), (-2, -1), (-1, 1)]
```

```hint
A uniform scaling by $k$ is $\begin{bmatrix} k & 0 \\ 0 & k
\end{bmatrix}$.
```

```solution
ship = [(0, 4), (1, 1), (2, -1), (1, -0.5), (-1, -0.5), (-2, -1), (-1, 1)]
half = [[0.5, 0], [0, 0.5]]
quarter = [[0.25, 0], [0, 0.25]]
draw_shapes([ship, transform_all(half, ship), transform_all(quarter, ship)])
---
Every ship shrinks towards $(0, 0)$, so the smaller ones sit inside the
bigger, around the origin, not off in the distance. Making a thing
smaller as it goes away is only half of perspective. The graphics pages
divide by the distance to do the rest.
```

</div>

<div class="dl-world" data-world="space-scenes">

Orion is in the skies of both hemispheres, and seen from the southern
one it is upside down compared with the northern view. Which matrix turns a star map upside down, without making it
a mirror image?

```python exec
id: matrix-world--space-scenes
# Betelgeuse, Bellatrix, Mintaka, Alnilam, Alnitak, Saiph, Rigel
orion = [(-3, 5), (3, 4.5), (1, 0.5), (0, 0), (-1, -0.5), (-2.5, -5), (3, -5.5)]
upside_down = [[1, 0], [0, 1]]
draw_shapes([orion, transform_all(upside_down, orion)], closed=False)
```

```inputs
transform(upside_down, (1, 2))
```

```hint
Upside down but not mirrored is a half turn. Where does it send "right"
and "up"?
```

```solution
orion = [(-3, 5), (3, 4.5), (1, 0.5), (0, 0), (-1, -0.5), (-2.5, -5), (3, -5.5)]
upside_down = [[-1, 0], [0, -1]]
draw_shapes([orion, transform_all(upside_down, orion)], closed=False)
---
A half turn, $\begin{bmatrix} -1 & 0 \\ 0 & -1 \end{bmatrix}$. The flip
$\begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix}$ would also put
Betelgeuse at the bottom, but as a mirror image, which no sky shows:
from the south you are looking at the same stars from the other side of
the Earth, turned, not reflected. (The positions are a sketch of
Orion's shape, not measured ones.)
```

</div>

## From earlier

**10.** From *Matrices: adding, scaling and transposing*. `scale(3, m)`
multiplies every entry of a matrix by 3. What does
`scale(3, [[1, 0], [0, 1]])` do to the F, used as a transformation?

<details class="dl-answer"><summary>answer</summary>

It is `[[3, 0], [0, 3]]`, problem 1's uniform scaling, which makes the
F three times as big. Scaling the do-nothing matrix makes the matrix that scales
pictures.

</details>

**11.** From *Comprehensions, grids and aliasing*. `transform_all` is one
line: `[transform(m, point) for point in shape]`. Can you write it as a
loop with `append` instead?

<details class="dl-answer"><summary>answer</summary>

```python
def transform_all(m, shape):
    result = []
    for point in shape:
        result.append(transform(m, point))
    return result
```

The comprehension says the same thing in one line. It makes a new list,
with one moved point for each point of the shape.

</details>

**12.** From *Writing your own functions*. `transform(m, point)` returns a
new point. Why not change the point where it is, as `point[0] = ...`?

<details class="dl-answer"><summary>answer</summary>

A point is a tuple, and a tuple cannot be changed, so Python would raise
a `TypeError`. Returning a new point is also safer. It leaves the
original F alone, so the playground can draw the before and the after
side by side.

</details>
