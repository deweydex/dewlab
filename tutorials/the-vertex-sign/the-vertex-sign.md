---
title: "Parabolas: a closer look at the sign in (x - h)²"
year: "2026-2027"
version: 2026.11.03.1
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
$y$ is 37, far from the lowest value. Either side of 3, $y$ goes up
the same way: 2 at both 2 and 4, and 5 at both 1 and 5.

Can you change one number in `y` so that the lowest point moves to
$x = -3$?

<details class="dl-answer"><summary>one change that does it</summary>

`(x + 3) ** 2 + 1`. Now the bracket is 0 when $x$ is -3, so the lowest
point is at $x = -3$. The number in the bracket and the turning point
always have opposite signs.

</details>

## Moving the bracket ourselves

The experiment used one value of $h$. Let's try many. The slider sets
$h$ in $(x - h)^2 + 1$. The grey curve is $x^2 + 1$, so we can see how
far the new curve has moved. The dotted line marks the $x$ where the
bracket is 0.

```python exec
id: moving-the-bracket-1
import matplotlib.pyplot as plt

h = slider("h", -6, 6, value=3, id="h").value

xs = [step / 10 for step in range(-100, 101)]
fig, ax = plt.subplots()
ax.plot(xs, [x ** 2 + 1 for x in xs], color="grey", alpha=0.4, label="x^2 + 1")
ax.plot(xs, [(x - h) ** 2 + 1 for x in xs], label=f"(x - ({h}))^2 + 1")
ax.axvline(h, linestyle=":", color="black")
ax.plot([h], [1], "o")
ax.set_xlim(-10, 10)
ax.set_ylim(-1, 30)
ax.grid(alpha=0.3)
ax.legend()
print(f"h = {h}: the bracket is 0 when x = {h}")
```

Move the slider to $-3$. What does the bracket look like in the legend?
Then move it to $4$. In each case, where is the turning point, and
where is the bracket 0?

## Two numbers, two jobs

Now we add the second number. Both sliders are below. $h$ is inside the
bracket and $k$ is added after the square.

```python exec
id: two-numbers-two-jobs-1
h = slider("h", -6, 6, value=2, id="h").value
k = slider("k", -10, 10, value=3, id="k").value

xs = [step / 10 for step in range(-100, 101)]
fig, ax = plt.subplots()
ax.plot(xs, [x ** 2 for x in xs], color="grey", alpha=0.4, label="x^2")
ax.plot(xs, [(x - h) ** 2 + k for x in xs], label=f"(x - ({h}))^2 + ({k})")
ax.plot([h], [k], "o")
ax.set_xlim(-10, 10)
ax.set_ylim(-12, 30)
ax.grid(alpha=0.3)
ax.legend()
print(f"turning point: x = {h}, y = {k}")
```

```predict
type: choice

We set $h = 2$ and $k = 3$ in the cell above, then change only $k$ to
$-5$. What happens to the turning point?

- It moves down 8 and stays at the same $x$
  - This reads $k$ as the height of the turning point. It goes from 3 to
    $-5$.
- It moves down 5 and stays at the same $x$
  - This reads the minus sign in $-5$ as the amount of movement.
- It moves left 5 and stays at the same height
  - This reads $k$ as if it were inside the bracket.
- I am not sure yet
  - Move the $k$ slider in the cell above, then come back to this question.
```

The two numbers do different jobs because they sit in different places.
$k$ is added to the answer, after the square, so it raises or lowers
every point. $h$ is inside the bracket, with $x$, before the square. A
square is smallest when its bracket is 0, and $x - h$ is 0 when $x$ is
$h$. So $h$ moves the turning point to $x = h$.

### Your turn

Can you set the sliders so that the turning point is at $(-4, 6)$? Write
the bracket you expect in a comment first. Then check it against the
legend.

<details class="dl-answer"><summary>one way through it</summary>

$h = -4$ and $k = 6$. The function is $(x - (-4))^2 + 6$, which is
$(x + 4)^2 + 6$. Here is one answer. Yours may be different and work
too.

</details>

## Where else it happens

It happens with every function, not only parabolas. The slider below
moves $(x - h)^3$ to the right or left of $x^3$. The curve crosses 0
where the bracket is 0.

```python exec
id: where-else-it-happens-1
import matplotlib.pyplot as plt

h = slider("h", -3, 3, value=1, id="h").value

xs = [step / 10 for step in range(-40, 41)]
fig, ax = plt.subplots()
ax.plot(xs, [x ** 3 for x in xs], color="grey", alpha=0.4, label="x cubed")
ax.plot(xs, [(x - h) ** 3 for x in xs], label=f"(x - ({h})) cubed")
ax.axhline(0, color="black", linewidth=0.5)
ax.axvline(h, linestyle=":", color="black")
ax.set_ylim(-30, 30)
ax.grid(alpha=0.3)
ax.legend()
print(f"h = {h}: (x - h) cubed crosses 0 at x = {h}")
```

With $h = 1$, $(x - 1)^3$ is 1 to the right of $x^3$. It reaches every
height 1 further to the right, because $x$ has to be 1 bigger to put
the same number inside the bracket.

## Where to read more

The graphing calculator [Desmos](https://www.desmos.com/calculator) draws
$(x - h)^2 + k$ with sliders for $h$ and $k$. Move $h$, and watch which way
the curve goes.
