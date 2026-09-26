---
title: "Parabolas: a closer look at the sign in (x - h)²"
year: "2026-2027"
version: 2026.09.26.1
---

# Parabolas: a closer look at the sign in (x - h)²

In [Parabolas: completing the square](tutorial:parabolas#the-form-that-tells-you-where-the-bottom-is),
$(x + 3)^2 - 4$ had its turning point at $(-3, -4)$. The page warned that
the first sign flips. Here are two ideas about the turning point of
$(x - 3)^2 + 1$. Both are reasonable, and they cannot both be true.

**Idea A.** Read the numbers as they are written. The turning point is at
$x = -3$, and $y = 1$.

**Idea B.** The turning point is where the bracket is 0. $x - 3$ is 0 when
$x$ is 3, so the turning point is at $x = 3$, and $y = 1$.

## An experiment

We do not need a graph. We can calculate $y$ for many values of $x$, and
look for the smallest.

```python exec
id: an-experiment-1
def y(x):
    return (x - 3) ** 2 + 1

for x in range(-5, 8):
    print("x =", x, " y =", y(x))
```

```predict
type: choice

At which x will y be smallest?

- x = -3
  - This is what idea A predicts.
- x = 3
  - This is what idea B predicts.
```

Run it. $y$ is smallest, 1, at $x = 3$, as idea B predicts. At $x = -3$,
$y$ is 37, nowhere near the bottom. Either side of 3, $y$ goes up
the same way: 2 at both 2 and 4, and 5 at both 1 and 5.

Can you change one number in `y` so that the lowest point moves to
$x = -3$?

<details class="dl-answer"><summary>one change that does it</summary>

`(x + 3) ** 2 + 1`. Now the bracket is 0 when $x$ is -3, so the lowest
point is at $x = -3$. The number in the bracket and the turning point
always have opposite signs.

</details>

## Why idea A feels right

The second number, the $+1$, does mean what it says: it lifts the whole
curve up by 1. So it is natural to read the first number the same way.
$-3$ appears on the page, so $-3$ is where the turning point should be.

The difference is where each number sits. The $+1$ is added to the answer,
after the square. The $-3$ is inside the bracket, with $x$, before the
square. A number inside the bracket changes which $x$ gives a particular
answer. Without the $-3$, the bracket is 0 at $x = 0$. With it, the
bracket is 0 at $x = 3$. So the whole curve moves 3 to the right.

## Where else it happens

It happens with every function, not only parabolas. Here are two curves.
One is $x^3$, and one is $(x - 1)^3$. Is the second one 1 to the left or 1
to the right of the first?

```python exec
id: where-else-it-happens-1
import matplotlib.pyplot as plt

xs = [step / 10 for step in range(-20, 31)]
plt.plot(xs, [x ** 3 for x in xs], label="x cubed")
plt.plot(xs, [(x - 1) ** 3 for x in xs], label="(x - 1) cubed")
plt.axhline(0, color="grey", linewidth=0.5)
plt.axvline(0, color="grey", linewidth=0.5)
plt.legend()
```

$(x - 1)^3$ is 1 to the right. It crosses 0 at $x = 1$, where $x^3$
crosses at 0. It reaches every height 1 later, because $x$ has to be 1
bigger to put the same number inside the brackets.

## Where to read more

The graphing calculator [Desmos](https://www.desmos.com/calculator) draws
$(x - h)^2 + k$ with sliders for $h$ and $k$. Move $h$, and watch which way
the curve goes.
