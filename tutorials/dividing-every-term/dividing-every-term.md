---
title: "Dividing: a closer look at (2x + 6) / 2"
year: "2026-2027"
version: 2026.11.04.3
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

## What the line under the fraction does under each idea

Both ideas use the same small fact: $\frac{2x}{2}$ is $x$, because the 2 on
top and the 2 underneath cancel.

Idea A uses that fact on the $2x$ and leaves the 6 as it is. The 2 under
the line divides only the first term. The answer is $x + 6$.

Idea B reads the line under a fraction as dividing everything above it.
$\frac{2x + 6}{2}$ is half of the whole of $2x + 6$. To halve a sum, we
halve each part and add them: $\frac{2x}{2} + \frac{6}{2}$, which is
$x + 3$. A number cancels only when it multiplies everything above the
line.

The two ideas differ in one place, the 6. Idea A keeps 6. Idea B halves it
to 3. The cell below lets us move $x$ and watch both answers against the
direct calculation.

```python exec
id: what-the-line-under-the-fraction-does-under-each-idea-1
x = slider("x", -10, 10, step=1, value=5, id="x").value

direct = (2 * x + 6) / 2
print("x =", x)
print("(2x + 6) / 2 =", direct)
print("idea A, x + 6 =", x + 6, " gap from direct:", x + 6 - direct)
print("idea B, x + 3 =", x + 3, " gap from direct:", x + 3 - direct)
```

Move the slider to a few values. What happens to the gap for idea A? What
happens to the gap for idea B?

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
