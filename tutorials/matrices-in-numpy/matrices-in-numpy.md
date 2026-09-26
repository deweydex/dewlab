---
title: "NumPy: everything you built, in one line each"
year: "2026-2027"
version: 2026.09.26.1
worlds:
  photos: Photographs, and the filters that change them.
  starships: Starships, and the structures they are built from.
  space-scenes: Stars, planets and the paths they take across the sky.
covers:
  one-line-each:
    covers: [CMPS-LO4]
    touches: [CMPS-LO1, CMPS-LO8]
  two-kinds-of-times:
    touches: [CMPS-LO4]
  how-much-faster:
    covers: [CMPS-LO5]
  solving-in-one-line:
    covers: [CMPS-LO4]
  many-steps-at-once:
    touches: [CMPS-LO4]
---

# NumPy: everything you built, in one line each

Over the last five pages you wrote `add`, `scale`, `transpose`,
`multiply`, `det`, `inverse` and `solve`. Each one is a few lines of
Python, and each one is already loaded on this page.

*NumPy* is a Python library for arrays of numbers. Scientists,
engineers and games programmers use it every day, and it does each of
your functions in one line. On this page we:

- check each of your functions against NumPy
- time your `multiply` against NumPy's on a big matrix
- solve a system with five unknowns in one line
- move a planet 1,000 steps with one multiplication

## One line each

A NumPy *array* holds a grid of numbers. `np.array` makes one from the
lists of lists you have used so far.

```python exec
id: one-line-each-1
import numpy as np

A = np.array([[2, 3], [1, -1]])
B = np.array([[5, 0], [1, -1]])
print(A)
print(A.shape)
print(A.tolist())
```

It prints the grid without commas, then its shape, `(2, 2)`, which is
2 rows and 2 columns. `tolist()` turns it back into a list of lists.

Here is each of your functions beside its one line in NumPy:

| Yours | NumPy |
|---|---|
| `add(A, B)` | `A + B` |
| `scale(3, A)` | `3 * A` |
| `transpose(A)` | `A.T` |
| `multiply(A, B)` | `A @ B` |
| `det(A)` | `np.linalg.det(A)` |
| `inverse(A)` | `np.linalg.inv(A)` |

Your functions take lists, and NumPy takes arrays. `np.allclose(x, y)`
is `True` when two grids have the same shape and every pair of numbers
is equal, apart from rounding. It accepts lists and arrays.

```python exec
id: one-line-each-2
a, b = A.tolist(), B.tolist()
print(np.allclose(add(a, b), A + B))
print(np.allclose(multiply(a, b), A @ B))
print(det(a), np.linalg.det(A))
```

Can you finish the checks, for `scale`, `transpose` and `inverse`?

```python exec
id: one-line-each-3
a = A.tolist()
```

```solution
{{include: setup/matrices/grid.py}}
{{include: setup/matrices/inverse.py}}
import numpy as np

A = np.array([[2, 3], [1, -1]])
a = A.tolist()
print(np.allclose(scale(3, a), 3 * A))
print(np.allclose(transpose(a), A.T))
print(np.allclose(inverse(a), np.linalg.inv(A)))
---
It prints `True` three times. Your functions and NumPy agree.
```

`det(a)` gives `-5`, and `np.linalg.det(A)` gives
`-5.000000000000001`. NumPy finds a determinant with a method that
works for any size, and that method divides, so it rounds.

## Two kinds of times

```predict
What will `A * B` print?

- The same as `A @ B`
  - `*` is multiplication.
- Each number in A times the number in the same place in B
  - `+` worked entry by entry, so `*` might too.
- An error
  - Two grids cannot be multiplied with `*`.
```

```python exec
id: two-kinds-of-times-1
import numpy as np

A = np.array([[2, 3], [1, -1]])
B = np.array([[5, 0], [1, -1]])
print(A * B)
print(A @ B)
```

`A * B` multiplies entry by entry, as `A + B` adds entry by entry. The
first row is `[10, 0]`, because $2 \times 5 = 10$ and $3 \times 0 =
0$. `A @ B` is the row-times-column product from
[Matrix multiplication: rows times columns](tutorial:multiplying-grids).
Both are useful, and mixing them up is a common mistake in NumPy code.

## How much faster?

This cell makes a 200×200 matrix of random numbers, and multiplies it
by itself twice: once with your `multiply`, and once with `@`. That is
$200 \times 200 \times 200 = 8{,}000{,}000$ multiplications of single
numbers each time.

```predict
How many times faster will `@` be?

- About the same
  - Both do 8,000,000 multiplications.
- About 10 times
  - NumPy is written to be fast.
- Much more than 10 times
  - NumPy might do the work in a different way.
```

```python exec
id: how-much-faster-1
import random
import time

import numpy as np

big = [[random.random() for j in range(200)] for i in range(200)]
big_array = np.array(big)

start = time.perf_counter()
yours = multiply(big, big)
your_time = time.perf_counter() - start

start = time.perf_counter()
numpys = big_array @ big_array
numpy_time = time.perf_counter() - start

print("yours:", round(your_time, 3), "seconds")
print("NumPy:", round(numpy_time, 5), "seconds")
print("NumPy is", round(your_time / numpy_time), "times faster")
print("Same answer:", np.allclose(yours, numpys))
```

Run it two or three times. The times change a little. In a browser,
`@` is usually 40 or 50 times faster. In Python on a laptop, outside a
browser, it is often several hundred times faster, because NumPy can
use code tuned for that processor. Both do the same 8,000,000
multiplications.
Your `multiply` does them one at a time in Python, and Python checks
the type of every number before it multiplies. NumPy stores the
numbers packed together, all of one type, and does the loops in C, a
language that runs much faster than Python.

Double the size to 400×400, and your `multiply` does 8 times the work,
since $2 \times 2 \times 2 = 8$. A 1,000×1,000 matrix, which is small
for a real program, would take your function 125 times as long as the
200×200 one.

## Solving in one line

`np.linalg.solve(A, b)` solves $A\mathbf{x} = \mathbf{b}$. It takes the
coefficients and the right-hand sides separately, not as one augmented
matrix. Here is a system with five unknowns. The answer was chosen
first, and `b` was made from it with `@`.

```python exec
id: solving-in-one-line-1
import numpy as np

C = np.array([
    [2, 1, 0, 3, 1],
    [1, 3, 2, 0, 1],
    [0, 2, 4, 1, 3],
    [3, 0, 1, 2, 2],
    [1, 1, 3, 1, 4],
])
chosen = np.array([1, -2, 3, 0, 4])
b = C @ chosen
print(b)
print(np.round(np.linalg.solve(C, b), 6))
```

It prints `[ 1. -2.  3.  0.  4.]`, the chosen answer. Without `np.round`,
the 0 comes out as a tiny number, about 0.0000000000000002, because of
rounding inside the elimination.

Can you solve the same system with your `solve`? It needs the augmented
matrix: each row of `C`, with the matching number from `b` on the end.

```python exec
id: solving-in-one-line-2
```

```hint
`C.tolist()` and `b.tolist()` give plain lists. Then
`[row + [v] for row, v in zip(C.tolist(), b.tolist())]` is the
augmented matrix.
```

```solution
{{include: setup/matrices/solve.py}}
import numpy as np

C = np.array([
    [2, 1, 0, 3, 1],
    [1, 3, 2, 0, 1],
    [0, 2, 4, 1, 3],
    [3, 0, 1, 2, 2],
    [1, 1, 3, 1, 4],
])
chosen = np.array([1, -2, 3, 0, 4])
b = C @ chosen
M = [row + [v] for row, v in zip(C.tolist(), b.tolist())]
print([round(v, 9) for v in solve(M)])
---
It prints `[1.0, -2.0, 3.0, 0.0, 4.0]`, the answer chosen at the start.
NumPy's `solve` also uses a form of elimination, with row swaps.
```

When the determinant is 0, `np.linalg.solve` raises a `LinAlgError`
that says `Singular matrix`. It is the same case as your `ValueError`.

## Many steps at once

On the practice page for matrix multiplication, a planet turned 30°
each step, and three steps made `multiply(step, multiply(step, step))`.
`np.linalg.matrix_power(step, n)` multiplies `step` by itself to make
$n$ steps in one line.

```python exec
id: many-steps-at-once-1
import math

import numpy as np

angle = math.radians(30)
step = np.array([[math.cos(angle), -math.sin(angle)],
                 [math.sin(angle), math.cos(angle)]])
print(np.round(np.linalg.matrix_power(step, 3), 6))
print(np.allclose(np.linalg.matrix_power(step, 12), np.identity(2)))
```

Three steps are the quarter turn, `[[0, -1], [1, 0]]`. `np.round`
rounds every entry at once. Twelve steps are a whole turn, so the
matrix is the identity, and the second line prints `True`.
`np.identity(2)` is the 2×2 identity. The next page,
[Markov chains](tutorial:where-chains-lead), uses `matrix_power` to see
where a chain of chances leads after many steps.

## Your world

One line of NumPy doing the work of a whole loop, in the world you
chose.

<div class="dl-world" data-world="photos">

A photo is a grid of pixels, and each pixel is three numbers. So a
photo is an array with shape (height, width, 3). The warm filter from
the page before changes every pixel with the same matrix. `photo @
warm.T` does that for every pixel at once. Can you undo it with one more
line, and check you get the photo back?

```python exec
id: numpy-your-world--photos
import matplotlib.pyplot as plt
import numpy as np

height, width = 100, 150
photo = np.zeros((height, width, 3))
photo[:, :, 0] = np.linspace(40, 220, width)
photo[:, :, 1] = 120
photo[:, :, 2] = np.linspace(200, 60, height)[:, np.newaxis]

warm = np.array([[1.2, 0.1, 0.0], [0.1, 1.0, 0.1], [0.0, 0.1, 0.8]])
warmed = photo @ warm.T

plt.figure()
plt.axis("off")
plt.imshow(np.clip(np.hstack([photo, warmed]) / 255, 0, 1))
```

```hint
The filter was `warm.T` on the right. To undo it, use the inverse of
`warm`, transposed, on the right of `warmed`.
```

```solution
import numpy as np

height, width = 100, 150
photo = np.zeros((height, width, 3))
photo[:, :, 0] = np.linspace(40, 220, width)
photo[:, :, 1] = 120
photo[:, :, 2] = np.linspace(200, 60, height)[:, np.newaxis]

warm = np.array([[1.2, 0.1, 0.0], [0.1, 1.0, 0.1], [0.0, 0.1, 0.8]])
warmed = photo @ warm.T

back = warmed @ np.linalg.inv(warm).T
print(np.allclose(back, photo))
print(warmed.max())
---
It prints `True`, so the photo is back exactly. The second line prints 276.0,
more red than a screen can show. A real editor stores whole numbers
from 0 to 255, so it would cut 276 down to 255. Then even the inverse
could not restore the red that was cut.
```

</div>

<div class="dl-world" data-world="starships">

A starship's hull is drawn with 10,000 points. The ship turns a quarter,
and every point has to move. How long does `transform_all` take, and
how long does one `@` take?

```python exec
id: numpy-your-world--starships
import time

import numpy as np

hull = np.random.rand(10000, 2) * 20 - 10
turn = np.array([[0, -1], [1, 0]])
```

```hint
Each point is a row of `hull`, so `hull @ turn.T` turns every point.
`transform_all(turn.tolist(), hull.tolist())` does the same with your
function. Time each one with `time.perf_counter()`.
```

```solution
{{include: setup/matrices/transform.py}}
import time
import numpy as np

hull = np.random.rand(10000, 2) * 20 - 10
turn = np.array([[0, -1], [1, 0]])

start = time.perf_counter()
yours = transform_all(turn.tolist(), hull.tolist())
your_time = time.perf_counter() - start

start = time.perf_counter()
numpys = hull @ turn.T
numpy_time = time.perf_counter() - start

print(np.allclose(yours, numpys))
print(your_time > numpy_time)
---
It prints `True` twice. The two agree, and `@` is faster. A game that turns thousands of points 60 times a second
needs that speed.
```

</div>

<div class="dl-world" data-world="space-scenes">

A planet turns 30° round its star each step. Where is it after 1,000
steps, if it starts at $(1, 0)$? Predict first. How many whole turns is
that, and what is left over?

```python exec
id: numpy-your-world--space-scenes
import math

import numpy as np

angle = math.radians(30)
step = np.array([[math.cos(angle), -math.sin(angle)],
                 [math.sin(angle), math.cos(angle)]])
```

```hint
`np.linalg.matrix_power(step, 1000) @ np.array([1, 0])` moves the
point 1,000 steps. Round the answer with `np.round`.
```

```solution
import math
import numpy as np

angle = math.radians(30)
step = np.array([[math.cos(angle), -math.sin(angle)],
                 [math.sin(angle), math.cos(angle)]])
print(np.round(np.linalg.matrix_power(step, 1000) @ np.array([1, 0]), 6))
---
It prints `[-0.5       0.866025]`. 1,000 steps of 30° is 30,000°, which is
83 whole turns and 120° more. The point at 120° round the circle is
$(-0.5, 0.866)$.
```

</div>

## Looking back

You wrote seven functions, and NumPy has each one in a line. Why write
them yourself? Try to say one thing that writing `multiply` taught you
that `A @ B` would not have.

A challenge: time your `multiply` and NumPy's `@` for sizes 50, 100,
200 and 400, and draw both times on one chart. Does your time grow 8
times each time the size doubles?

```python challenge
import random
import time

import numpy as np


def multiply(a, b):
    columns = [[row[j] for row in b] for j in range(len(b[0]))]
    return [[sum(x * y for x, y in zip(row, column)) for column in columns] for row in a]


for n in [50, 100, 200, 400]:
    m = [[random.random() for j in range(n)] for i in range(n)]
    # Time multiply(m, m) and np.array(m) @ np.array(m) here.
```

## Where to read more

NumPy Developers. *NumPy: the absolute basics for beginners.*
<https://numpy.org/doc/stable/user/absolute_beginners.html>. The official
introduction, from making an array to the `@` operator and
`np.linalg`.

Harris, C. R. et al. (2020). Array programming with NumPy. *Nature*,
585, 357–362. <https://doi.org/10.1038/s41586-020-2649-2>. The paper
that describes how NumPy works, and why so much science is built on it.
The first few pages need no mathematics beyond this series.
