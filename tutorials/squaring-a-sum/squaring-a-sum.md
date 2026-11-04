---
title: "Squaring: a closer look at (a + b)²"
year: "2026-2027"
version: 2026.11.04.3
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
  - This reads the sum as always different, even when $a$ is 0.
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

## What each idea counts

Idea A counts two pieces, a square with side $a$ and a square with side
$b$. Idea B counts four pieces, because every term multiplies every term:
$a \cdot a$, $a \cdot b$, $b \cdot a$ and $b \cdot b$.

Squaring a product does square each part: $(ab)^2 = a^2 b^2$. The bracket
holds one term, so there is nothing else to multiply. In $2(a + b)$, the 2
multiplies each term once. In $(a + b)^2$, the bracket multiplies itself, so
each term meets each term.

A picture shows the four pieces. Here is a square with sides $a + b$, cut
where $a$ ends.

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
counts, $a^2$ and $b^2$, and two rectangles, each $a$ by $b$. Idea A leaves
out the two rectangles. They add $2ab$ to the area, so the two ideas differ
by $2ab$ and agree only when that is 0.

Let's change the sides ourselves. The sliders set $a$ and $b$.

```python exec
id: what-each-idea-counts-1
a = slider("a", 0, 6, step=1, value=3, id="side-a").value
b = slider("b", 0, 6, step=1, value=2, id="side-b").value

fig, ax = plt.subplots(figsize=(4, 4))
pieces = [((0, 0), a, a, "a²"), ((a, a), b, b, "b²"),
          ((a, 0), b, a, "ab"), ((0, a), a, b, "ab")]
for (x, y), width, height, label in pieces:
    ax.add_patch(plt.Rectangle((x, y), width, height, fill=False, linewidth=2))
    if width > 0 and height > 0:
        ax.text(x + width / 2, y + height / 2, label, ha="center",
                va="center", fontsize=12)
ax.set_xlim(0, 12)
ax.set_ylim(0, 12)
ax.set_aspect("equal")
ax.set_title("A square with sides a + b")
print("whole square:", (a + b) ** 2)
print("the two squares:", a ** 2 + b ** 2)
print("the two rectangles:", 2 * a * b)
```

Can you set $a$ and $b$ so that the two rectangles have the same area as
the two squares together? Can you make the rectangles larger?

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
