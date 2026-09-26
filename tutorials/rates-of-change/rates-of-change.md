---
title: "Derivatives: the rate of change of a curve"
year: "2026-2027"
version: 2026.08.23.1
covers:
  the-slope-of-something-that-is-not-straight:
    covers: [MIT-3.6]
  three-descriptions-of-one-number:
    covers: [MIT-3.6]
  the-derivative-as-a-function:
    covers: [MIT-3.6]
  rules-instead-of-limits:
    covers: [MIT-3.7]
  the-chain-rule:
    covers: [MIT-3.7]
---

# Derivatives: the rate of change of a curve

In [Straight lines: slope, midpoint and distance](tutorial:lines-and-distances),
we described slope as a rate of change: **if $x$ goes up by one, what
happens to $y$?** For a straight line, the answer is one number, and it
is the same everywhere on the line.

For anything that bends, the answer changes as we move along it. On
this page we find that answer at a single point. Then we find rules, so
that we do not have to calculate it from the start every time.

The tool we need is the limit, from
[Limits: getting closer without arriving](tutorial:approaching-a-limit).
That is the only new idea. For everything else, we just need to be
careful.

On this page we:

- find the slope of a curve at one point, using a limit
- see three ways of describing that one number
- treat the slope as a function of its own, and use it to find turning
  points
- learn rules that give the slope without a limit: for powers, sums,
  products, and one function inside another

## The slope of something that is not straight

Here is the curve $y = x^2$, with four points marked on it. How steep is
the curve at each point?

```python exec
id: the-slope-of-something-that-is-not-straight-1
import matplotlib.pyplot as plt

def curve(x):
    return x ** 2


fig, ax = plt.subplots(figsize=(7, 4.5))
xs = [x / 50 for x in range(-150, 151)]
ax.plot(xs, [curve(x) for x in xs], linewidth=2)
for point in [-2, -0.5, 1, 2.5]:
    ax.plot([point], [curve(point)], "o", markersize=8)
ax.axhline(0, color="black", linewidth=0.8)
ax.axvline(0, color="black", linewidth=0.8)
ax.grid(alpha=0.3)
ax.set_ylim(-1, 9)
ax.set_title("Steep in different amounts at different places")
```

From left to right, the curve at the marked points is steeply downhill,
gently downhill, gently uphill, and steeply uphill. The curve has no
single slope.

But at each point there is a *local* slope: how steep the curve is
right there. We want to find that local slope.

We use the same method as for the falling ball in
[Limits: getting closer without arriving](tutorial:approaching-a-limit).
A *chord* is a straight line that joins two points on a curve. We take
two points on the curve, close together, and find the slope of the chord
between them. Then we bring the points closer.

The function `slope_between` does this. It finds the slope of the chord
from $x$ to $x + \text{gap}$:

$$\frac{f(x + \text{gap}) - f(x)}{\text{gap}}$$

For example, with $x = 3$ and a gap of 1, that is
$\dfrac{4^2 - 3^2}{1} = \dfrac{16 - 9}{1} = 7$. What do you think
happens as the gap gets smaller?

```python exec
id: the-slope-of-something-that-is-not-straight-2
def slope_between(f, x, gap):
    """The slope of the straight line joining two nearby points on f."""
    return (f(x + gap) - f(x)) / gap


print("Getting the slope of x^2 at x = 3:")
for gap in [1, 0.5, 0.1, 0.01, 0.001, 0.0001]:
    print(f"   gap {gap:<8} : {slope_between(curve, 3, gap)}")
```

The slopes move towards 6, and never arrive, because the gap can never be
zero.

**The limit of the chord's slope, as the gap shrinks to nothing, is the
slope of the curve at that point.** The *derivative* of a function at a
point is this limit: the slope of the curve at that one point. Here, the
derivative of $x^2$ at $x = 3$ is 6.

The picture below shows three of those chords, and the line they get
closer to.

```python exec
id: the-slope-of-something-that-is-not-straight-3
fig, ax = plt.subplots(figsize=(7, 4.5))
xs = [x / 50 for x in range(0, 251)]
ax.plot(xs, [curve(x) for x in xs], linewidth=2, label="x^2")

at = 3
for gap, style in [(2, ":"), (1, "--"), (0.3, "-.")]:
    m = slope_between(curve, at, gap)
    ax.plot([at, at + gap], [curve(at), curve(at + gap)], "o-", markersize=5)
    line_xs = [1.5, 4.5]
    ax.plot(line_xs, [curve(at) + m * (x - at) for x in line_xs], style,
            linewidth=1, label=f"gap {gap}: slope {m}")

ax.plot([1.5, 4.5], [curve(at) + 6 * (x - at) for x in [1.5, 4.5]],
        linewidth=2, color="tab:red", label="the limit: slope 6")
ax.grid(alpha=0.3)
ax.legend(fontsize=8)
ax.set_ylim(0, 20)
ax.set_title("Chords closing in on the tangent")
```

Each thin line goes through two points on the curve. As the second point
slides towards the first, the line turns. The line it turns towards is
the red one. The red line touches the curve at $x = 3$ and has the same
steepness as the curve there.

The *tangent line* at a point is the straight line that touches the
curve at that point and has the same steepness as the curve there. Its
slope is the derivative.

(This "tangent" is a line. It is a different thing from the tangent
ratio, $\tan$, in
[The unit circle: sine, cosine and tangent](tutorial:the-unit-circle),
even though the two share a name.)

## Three descriptions of one number

This part needs care. Here are three ideas that look like three separate
topics. They all describe the same number.

| Description | What it means |
|---|---|
| **A limit** | The value that $\dfrac{f(x + \text{gap}) - f(x)}{\text{gap}}$ moves towards as the gap shrinks. This is the definition of the derivative. |
| **The slope of a tangent line** | The steepness of the straight line that touches the curve at that point. |
| **A rate of change** | How fast the output is changing for each unit of input, right at that point. |

The next cell defines `derivative_at`, which computes the derivative
with numbers. It takes a very small gap, and uses one point on each side
of $x$. That gives a more accurate answer than a chord on one side only.

Look at the $x$ values in the loop. Can you predict any of the slopes?
Run it to check.

```python exec
id: three-descriptions-of-one-number-1
def derivative_at(f, x, gap=1e-6):
    """The derivative, computed numerically. Good enough to see with."""
    return (f(x + gap) - f(x - gap)) / (2 * gap)


for x in [-2, -0.5, 0, 1, 3]:
    print(f"slope of x^2 at x = {x:>4} is {derivative_at(curve, x):>8.4f}")
```

Compare each answer with the $x$ value beside it. What do you notice?

Each slope is double the $x$. **The derivative of $x^2$ is $2x$.** So
the derivative is a function, and not a single number. It tells us the
slope wherever we ask. For example, at $x = 5$ the slope is
$2 \times 5 = 10$.

We write $f'$, said "f prime", for the derivative of $f$. So if
$f(x) = x^2$, then $f'(x) = 2x$. To *differentiate* a function means to
find its derivative.

The "rate of change" description does not need a graph.
The falling ball in the last tutorial fell $4.9t^2$ metres after $t$
seconds. Its speed is the rate of change of that distance, so its speed
is the derivative:

```python exec
id: three-descriptions-of-one-number-2
def fallen(t):
    return 4.9 * t ** 2


for t in [0, 1, 2, 3]:
    print(f"at t = {t}s the ball has fallen {fallen(t):>6.1f} m "
          f"and is travelling at {derivative_at(fallen, t):>5.2f} m/s")
```

The first column is distance, and the second is speed. The relationship
is the same as between a curve and its slope, and no axes are needed.
This is why the straight-lines page used "rate of change" for slope.

## The derivative as a function

Let's plot the slope underneath the curve it comes from. Then we can
read the two together.

```python exec
id: the-derivative-as-a-function-1
fig, (top, bottom) = plt.subplots(2, 1, figsize=(7, 6), sharex=True)

xs = [x / 50 for x in range(-150, 151)]
top.plot(xs, [curve(x) for x in xs], linewidth=2)
top.set_ylabel("x^2")
top.grid(alpha=0.3)
top.axhline(0, color="black", linewidth=0.8)

bottom.plot(xs, [derivative_at(curve, x) for x in xs], linewidth=2, color="tab:orange")
bottom.set_ylabel("its slope")
bottom.set_xlabel("x")
bottom.grid(alpha=0.3)
bottom.axhline(0, color="black", linewidth=0.8)
top.set_title("A curve, and how steep it is")
```

Read the two graphs together:

- Where the top curve goes downhill, the bottom graph is negative.
- Where the top curve is flat, at its lowest point, the bottom graph
  crosses zero.
- Where the top curve climbs steeply, the bottom graph is large.

**At a turning point, the curve is flat for a moment, so the derivative
is zero there.** This is the most useful single fact on this page. It
connects back to
[Parabolas: completing the square](tutorial:parabolas): the vertex of a
parabola is the point where the slope is zero.

(The opposite is not always true. A zero slope tells you where to *look*
for a turning point. The curve $x^3$ is flat for a moment at $x = 0$, but it
keeps climbing on both sides, so that point is not a turning point.)

Completing the square put the vertex of $x^2 + 6x + 5$ at $x = -3$. What
should the slope be there? Run the cell to check.

```python exec
id: the-derivative-as-a-function-2
def quadratic(x):
    return x ** 2 + 6 * x + 5


# Completing the square said the vertex was at x = -3. Ask the slope instead.
for x in [-5, -4, -3, -2, -1]:
    print(f"slope at x = {x:>3}: {derivative_at(quadratic, x):>7.4f}")
```

The slope is zero at −3, exactly where completing the square put the
vertex. (The `-0.0000` is a tiny rounding error, and it means zero.)
**Two completely different methods give the same answer.** When that
happens, you can trust both methods.

### Your turn

Where are the turning points of $x^3 - 3x$?

1. Use `derivative_at` to find the slope of `cubic` at several values of
   $x$.
2. Look for the values of $x$ where the slope is zero.
3. Check that the curve really turns there: is the slope negative on one
   side and positive on the other?

```python exec
id: your-turn-1
def cubic(x):
    return x ** 3 - 3 * x


# Your investigation here.
```

## Rules instead of limits

Computing a limit every time would be tiring. Luckily, the answers
follow patterns. The cell below prints the slopes of $x$, $x^2$, $x^3$
and $x^4$ at three points. Can you find a pattern in each row?

```python exec
id: rules-instead-of-limits-1
print("  function        slope at 2      slope at 3      slope at 5")
for name, f in [("x", lambda x: x),
                ("x^2", lambda x: x ** 2),
                ("x^3", lambda x: x ** 3),
                ("x^4", lambda x: x ** 4)]:
    row = [f"{derivative_at(f, x):>13.4f}" for x in (2, 3, 5)]
    print(f"  {name:<12} {''.join(row)}")
```

Compare each row with powers of the $x$ values. For example, the slope
of $x^3$ at 3 is 27, which is $3 \times 3^2$. The pattern is:

| Function | Its derivative |
|---|---|
| $x$ | $1$ everywhere |
| $x^2$ | $2x$ |
| $x^3$ | $3x^2$ |
| $x^4$ | $4x^3$ |

> **The power rule:** the derivative of $x^n$ is $n x^{n-1}$.

In words: bring the power down to the front, and reduce the power by
one. For example, the derivative of $x^7$ is $7x^6$.

The next cell checks the rule against the numerical derivative, at
$x = 2.5$. Do you expect the two columns to agree?

```python exec
id: rules-instead-of-limits-2
def power_rule(n):
    """The derivative of x^n, as a function."""
    return lambda x: n * x ** (n - 1)


for n in [1, 2, 3, 4, 7]:
    numeric = derivative_at(lambda x: x ** n, 2.5)
    by_rule = power_rule(n)(2.5)
    print(f"x^{n}:  numerically {numeric:>12.5f}   by the rule {by_rule:>12.5f}")
```

### Adding things together

What is the slope of $x^3 + x^2$? Here $f$ is $x^3$ and $g$ is $x^2$.
Before you run the cell, can you guess how the third slope relates to
the first two?

```python exec
id: rules-instead-of-limits-3
f = lambda x: x ** 3
g = lambda x: x ** 2
both = lambda x: f(x) + g(x)

for x in [1, 2, 4]:
    print(f"at x = {x}:  slope of f is {derivative_at(f, x):>8.4f},"
          f"  of g is {derivative_at(g, x):>8.4f},"
          f"  of f+g is {derivative_at(both, x):>8.4f}")
```

> **The sum rule:** the derivative of $f + g$ is the derivative of $f$
> plus the derivative of $g$.

That is as convenient as it sounds. A polynomial is a sum of powers, so
we can differentiate it one term at a time. For example, the derivative
of $x^2 + 6x + 5$ is $2x + 6 + 0$, which is $2x + 6$. (A number on its
own, like 5, never changes, so its slope is 0.)

The next cell stores a polynomial as a list of its coefficients, from
the constant term upwards. The list `[5, 6, 1]` means $5 + 6x + x^2$.

```python exec
id: rules-instead-of-limits-4
def differentiate_polynomial(coefficients):
    """Coefficients from the constant term upwards: [c, b, a] means a x^2 + b x + c."""
    return [i * coefficients[i] for i in range(1, len(coefficients))]


def evaluate(coefficients, x):
    return sum(c * x ** i for i, c in enumerate(coefficients))


poly = [5, 6, 1]           # 5 + 6x + x^2
slope_poly = differentiate_polynomial(poly)
print("the polynomial:", poly)
print("its derivative:", slope_poly)

for x in [-5, -3, 0, 2]:
    print(f"  at x = {x:>3}:  by rule {evaluate(slope_poly, x):>8.4f}"
          f"   numerically {derivative_at(lambda v: evaluate(poly, v), x):>8.4f}")
```

The derivative is `[6, 2]`, which means $6 + 2x$. That is the
$2x + 6$ we found by hand.

### Multiplying things together

Most people expect this rule: "the derivative of a product is the
product of the derivatives". It is wrong, and it helps to see that it is
wrong before we see the right rule.

Here $f$ is $x^2$ and $g$ is $x^3$, at $x = 2$. Do you think the last two
lines will match?

```python exec
id: rules-instead-of-limits-5
f = lambda x: x ** 2
g = lambda x: x ** 3
product = lambda x: f(x) * g(x)

x = 2
print("slope of f:      ", derivative_at(f, x))
print("slope of g:      ", derivative_at(g, x))
print("those multiplied:", derivative_at(f, x) * derivative_at(g, x))
print("slope of f*g:    ", derivative_at(product, x))
```

They do not match, and they are not close: 48 against 80. Multiplying
the two derivatives does not give the derivative of the product.

> **The product rule:** the derivative of $f \cdot g$ is
> $f' \cdot g + f \cdot g'$.

In words: differentiate the first and leave the second alone. Then
differentiate the second and leave the first alone. Add the two results.

```python exec
id: rules-instead-of-limits-6
def product_rule(f, df, g, dg):
    return lambda x: df(x) * g(x) + f(x) * dg(x)


by_rule = product_rule(lambda x: x ** 2, lambda x: 2 * x,
                       lambda x: x ** 3, lambda x: 3 * x ** 2)

for x in [1, 2, 3.5]:
    print(f"at x = {x}:  rule gives {by_rule(x):>10.4f},"
          f"   numerically {derivative_at(product, x):>10.4f}")
```

We can check this another way. $x^2 \cdot x^3$ is $x^5$, and by the
power rule its derivative is $5x^4$. The product rule gives:

$$2x \cdot x^3 + x^2 \cdot 3x^2 = 2x^4 + 3x^4 = 5x^4$$

The two methods agree. At $x = 2$, $5x^4 = 5 \times 16 = 80$, the same
80 as the cell above.

### Your turn

How would you differentiate these by hand?

1. $3x^4 - 2x + 7$
2. $(x + 1)(x^2 - 3)$
3. $x^2 (x + 5)$

For each one, find the derivative first. Then check it at a few
points with `derivative_at`.

```python exec
id: your-turn-2
# Your answers, then a check with derivative_at.
```

## The chain rule

There is one more rule. It is worth meeting, but you do not need to
practise it until it is automatic.

What happens when one function is inside another? Here the inner
function is $2x + 1$, and the outer function cubes whatever it is given.
So the whole thing is $(2x + 1)^3$. Look at the last two lines of the
cell. Do you think they will agree?

```python exec
id: the-chain-rule-1
inner = lambda x: 2 * x + 1
outer = lambda u: u ** 3
nested = lambda x: outer(inner(x))

x = 1.5
print("slope of the inner:  ", derivative_at(inner, x))
print("slope of the outer at inner(x):", derivative_at(outer, inner(x)))
print("those multiplied:    ",
      derivative_at(inner, x) * derivative_at(outer, inner(x)))
print("slope of the whole:  ", derivative_at(nested, x))
```

Those last two agree: both are 96.

> **The chain rule:** the derivative of $f(g(x))$ is
> $f'(g(x)) \cdot g'(x)$.

In words: first, differentiate the outside function, and leave the
inside alone. Then multiply by the derivative of the inside.

The idea behind it is that rates multiply. Suppose $u$ changes three
times as fast as $x$, and $y$ changes twice as fast as $u$. Then $y$
changes $3 \times 2 = 6$ times as fast as $x$. Rates multiply along a
chain, and that gives the rule its name.

### Your turn

How might you differentiate $(3x + 2)^5$ with the chain rule?

1. Name the inside function and the outside function.
2. Find the derivative by hand.
3. Check it at a point with `derivative_at`.

```python exec
id: your-turn-3
# Your answer, then the check.
```

## What is not on this page

We have left out two topics on purpose. Here they are, so that you do
not have to wonder.

**The quotient rule** is a rule for one function divided by another. It
is mechanical. You can manage without it. Write the division as a
product with a negative power, and use the product rule and the chain
rule.

**Integration by parts** is a technique for integration, which undoes
differentiation: it goes from a rate of change back to the total. A
course that uses a lot of integration needs it. This course does not.

Calculus is not the focus of this course. You need to know what a
derivative *is*: a rate of change, the slope of a tangent line, and a
limit. You also need to compute simple ones. More practice with the
other techniques would take weeks and give you very little.

## Reflection

A derivative is the slope of a curve at a single point. It is a limit,
and the limit makes the question possible to answer.

**One number has three descriptions.** A limit of chords, the slope of the
tangent line, and a rate of change. Which one you use depends on what
you are doing.

**The derivative is a function.** It is a rule that gives the slope
wherever you ask, and not a single number.

**A turning point has zero slope.** This is the most useful fact here,
and it agrees with what completing the square told you in
[Parabolas: completing the square](tutorial:parabolas).

**The rules save you the limit.** Bring the power down and reduce it by
one. Sums split into their parts. Products do not. They need
$f'g + fg'$. For one function inside another, the rates multiply.

Pick something that changes over time: a bank balance, a temperature, a
download. In a few sentences, what would its derivative be, in words,
and what units would it have?

## Where to read more

Grant Sanderson (3Blue1Brown) (2017). *Essence of Calculus, Chapter 2: The
Paradox of the Derivative.* <https://www.youtube.com/watch?v=9vKqVkMQHKk>.
This video draws the same picture as this page, with chords moving
towards a tangent. It also explains why "instantaneous rate of change"
is a stranger idea than it sounds.

3Blue1Brown (2018). *The other way to visualize derivatives: Chapter 12,
Essence of calculus.* <https://www.youtube.com/watch?v=CfW845LNObM>. This
video draws a derivative as how much a function stretches or squashes the
numbers near a point, rather than as a slope. It is about fourteen
minutes long.
