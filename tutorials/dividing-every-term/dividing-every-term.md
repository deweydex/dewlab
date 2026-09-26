---
title: "Dividing: a closer look at (2x + 6) / 2"
year: "2026-2027"
version: 2026.09.26.1
---

# Dividing: a closer look at (2x + 6) / 2

In [Rearranging formulae](tutorial:rearranging-formulae#the-moves), one of
the moves was to divide both sides of a formula by the same number. When
one side is a sum, what happens to it? Here are two ideas. Both are
reasonable, and they cannot both be true.

**Idea A.** To divide $2x + 6$ by 2, divide the $2x$, which gives $x$. The
answer is $x + 6$.

**Idea B.** Dividing $2x + 6$ by 2 divides all of it. Both terms are
halved, and the answer is $x + 3$.

## An experiment

We can test both ideas without any algebra. Pick a value of $x$, find
$(2x + 6) / 2$ directly, and see which answer it matches.

```python exec
id: an-experiment-1
for x in [0, 1, 5, 10]:
    print("x =", x, " (2x + 6) / 2 =", (2 * x + 6) / 2,
          " x + 6 =", x + 6, " x + 3 =", x + 3)
```

```predict
type: choice

Which column will match (2x + 6) / 2 on every line?

- x + 6
  - This is what idea A predicts.
- x + 3
  - This is what idea B predicts.
- Neither
```

Run it. $(2x + 6) / 2$ matches $x + 3$ on every line, as idea B predicts.
When $x$ is 5, $2x + 6$ is 16, and half of 16 is 8. Idea A gives 11.

A line in the cell only tests one value of $x$. Can you find any value of
$x$ where $x + 6$ and $(2x + 6) / 2$ agree? Try a few, including negative
numbers and decimals.

<details class="dl-answer"><summary>why you cannot</summary>

$x + 6$ is always exactly 3 more than $x + 3$, whatever $x$ is. So it is
always 3 more than $(2x + 6) / 2$. No value of $x$ makes them agree.

</details>

## Why idea A feels right

Idea A comes from a move that works: $\frac{2x}{2} = x$. The 2 on top and
the 2 underneath look like they cancel, and in $\frac{2x}{2}$ they do. In
$\frac{2x + 6}{2}$, the eye sees the same 2 on top and the same 2
underneath, and makes the same move.

But the line under a fraction divides everything above it. $\frac{2x + 6}{2}$
means "half of the whole of $2x + 6$". To halve a sum, halve each part
and add them: $\frac{2x}{2} + \frac{6}{2}$, which is $x + 3$. You can cancel only
a number that multiplies everything above the line.

## Where else it happens

It happens with plain numbers too, where nobody would think of cancelling.
What is $(6 + 4) / 2$?

```python exec
id: where-else-it-happens-1
print((6 + 4) / 2)
print(6 / 2 + 4)
```

The first line is 5.0: half of 10. The second is 7.0: half of 6, and then the
whole 4. The second line is idea A written in numbers. With numbers, it is
easy to see that it halves only part of the 10.

## Where to read more

[Eedi](https://eedi.com/), co-founded by the teacher Craig Barton, collects
maths questions with four answers, where each wrong answer comes from one
common slip, like the one on this page.
