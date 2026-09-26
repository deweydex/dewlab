---
title: "Squaring: a closer look at (a + b)²"
year: "2026-2027"
version: 2026.09.26.1
---

# Squaring: a closer look at (a + b)²

In [Polynomials](tutorial:expressions-come-alive#multiplying-polynomials),
multiplying two brackets meant multiplying every term by every term.
$(a + b)^2$ is two brackets, $(a + b)(a + b)$, but it does not look like
two. Here are two ideas about it. Both are reasonable, and they cannot
both be true.

**Idea A.** Squaring a sum squares each part: $(a + b)^2 = a^2 + b^2$.

**Idea B.** $(a + b)^2$ is $(a + b)(a + b)$, and every term multiplies
every term. That gives $a^2 + 2ab + b^2$.

## An experiment

Try both ideas on some numbers.

```python exec
id: an-experiment-1
for a, b in [(1, 2), (3, 4), (0, 5), (-2, 2)]:
    print("a =", a, "b =", b, " (a + b)**2 =", (a + b) ** 2,
          " a**2 + b**2 =", a ** 2 + b ** 2)
```

```predict
type: choice

On how many of the four lines will the two answers be the same?

- All four
  - This is what idea A predicts.
- Some of them
  - This is what idea B predicts: they agree only when $2ab$ is 0.
- None of them
```

Run it. They agree on one line only, the line where $a$ is 0. With 3 and
4, $(3 + 4)^2$ is 49, and $3^2 + 4^2$ is 25. The difference is 24, which is
$2 \times 3 \times 4$. This is the $2ab$ in idea B. Idea A does not have
it.

Can you find the rule for when the two agree? Try a few more pairs.

<details class="dl-answer"><summary>the rule</summary>

They agree exactly when $2ab$ is 0, so when $a$ is 0 or $b$ is 0. For any
other pair, $(a + b)^2$ and $a^2 + b^2$ are different numbers.

</details>

## Why idea A feels right

Idea A works for multiplying. $(ab)^2 = a^2 b^2$: squaring a product does
square each part. It also looks like other rules we trust, such as
$2(a + b) = 2a + 2b$. So $(a + b)^2 = a^2 + b^2$ looks like one more rule
of the same kind.

A picture shows what it leaves out. Here is a square with sides $a + b$,
cut where $a$ ends.

```python exec
id: why-idea-a-feels-right-1
import matplotlib.pyplot as plt

a, b = 3, 2
fig, ax = plt.subplots(figsize=(4, 4))
pieces = [((0, 0), a, a, "a²"), ((a, a), b, b, "b²"),
          ((a, 0), b, a, "ab"), ((0, a), a, b, "ab")]
for (x, y), width, height, label in pieces:
    # add_patch draws one rectangle on the picture.
    ax.add_patch(plt.Rectangle((x, y), width, height, fill=False, linewidth=2))
    ax.text(x + width / 2, y + height / 2, label, ha="center", va="center",
            fontsize=16)
ax.set_xlim(0, a + b)
ax.set_ylim(0, a + b)
ax.set_aspect("equal")
ax.set_title("A square with sides a + b")
```

The whole square is $(a + b)^2$. Inside it are the two squares idea A
expects, $a^2$ and $b^2$, and two rectangles, each $a$ by $b$. Idea A
leaves out the two rectangles.

## Where else it happens

Square roots have the same trap. Is $\sqrt{9 + 16}$ the same as
$\sqrt{9} + \sqrt{16}$?

```python exec
id: where-else-it-happens-1
print((9 + 16) ** 0.5)
print(9 ** 0.5 + 16 ** 0.5)
```

The first is 5 and the second is 7. A square root of a sum is not the sum
of the square roots.

## Where to read more

The picture of the square cut into four pieces is very old. Euclid's
*Elements*, Book II, Proposition 4, proves $(a + b)^2 = a^2 + 2ab + b^2$
with it, about 2,300 years ago.
