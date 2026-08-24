---
title: "Rates of Change"
slug: rates-of-change
module: mit-pdp-maths-prog-integration
module_title: "Programming and Maths, Integrated"
year: "2026-2027"
series: maths-and-programming
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

# Rates of Change

**Maths for IT**

In *Lines and Distances* you named slope as a rate of change: **if x goes up by one, what happens to y?** For a straight line the answer is one number and it is the same everywhere.

For anything that bends, the answer changes as you move along it. This tutorial is about getting that answer at a single point — and then about not having to work it out from scratch every time.

The machinery is the limit from the last tutorial. That is the only new idea; everything else is bookkeeping.

## The Slope of Something That Is Not Straight

Take a curve and ask how steep it is.

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

At the marked points the curve is steeply downhill, gently downhill, gently uphill, and steeply uphill. There is no one slope.

But at each point there is a *local* slope — how steep it is just there — and that is what we are after.

The trick is the one from the last tutorial. Take two points on the curve, close together, and find the slope of the straight line between them. Then bring them closer.

```python exec
id: the-slope-of-something-that-is-not-straight-2
def slope_between(f, x, gap):
    """The slope of the straight line joining two nearby points on f."""
    return (f(x + gap) - f(x)) / gap


print("Getting the slope of x^2 at x = 3:")
for gap in [1, 0.5, 0.1, 0.01, 0.001, 0.0001]:
    print(f"   gap {gap:<8} : {slope_between(curve, 3, gap)}")
```

Heading for 6, and never arriving, because the gap can never be zero.

**The limit of that as the gap shrinks to nothing is the slope of the curve at that point.** It is called the **derivative**.

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

Each dotted line joins two points on the curve. As the second point slides towards the first, the line pivots — and the thing it pivots towards is the red line, which touches the curve at exactly one place.

That red line is the **tangent**, and its slope is the derivative.

## Three Descriptions of One Number

Here is the part worth being careful about, because these look like three topics and are one.

**A limit.** The value that `(f(x + gap) − f(x)) / gap` heads towards as the gap shrinks. That is the definition.

**The slope of a tangent.** The steepness of the straight line that touches the curve at that point and does not cross it.

**A rate of change.** How fast the output is changing per unit of input, right there.

```python exec
id: three-descriptions-of-one-number-1
def derivative_at(f, x, gap=1e-6):
    """The derivative, computed numerically. Good enough to see with."""
    return (f(x + gap) - f(x - gap)) / (2 * gap)


for x in [-2, -0.5, 0, 1, 3]:
    print(f"slope of x^2 at x = {x:>4} is {derivative_at(curve, x):>8.4f}")
```

Look at that column of answers against the x values beside them. Every one is exactly double the x.

**The derivative of `x²` is `2x`.** Not a number — a function, one that tells you the slope wherever you ask.

The rate-of-change description is the one that leaves the graph. The falling ball from the last tutorial fell `4.9t²` metres, and its speed is the derivative:

```python exec
id: three-descriptions-of-one-number-2
def fallen(t):
    return 4.9 * t ** 2


for t in [0, 1, 2, 3]:
    print(f"at t = {t}s the ball has fallen {fallen(t):>6.1f} m "
          f"and is travelling at {derivative_at(fallen, t):>5.2f} m/s")
```

Distance and speed. Same relationship, no axes required — which is what "rate of change" means, and why the phrasing was worth committing to back in *Lines and Distances*.

## The Derivative as a Function

Plot the slope alongside the thing it is the slope of, and the relationship becomes readable.

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

Read them together. Where the top curve goes downhill, the bottom one is negative. Where the top curve is flat — at the very bottom — the bottom one crosses zero. Where the top curve climbs steeply, the bottom one is large.

**The derivative being zero is where the original is flat**, which is where its turning points are. That is the most useful single fact in this tutorial, and it connects straight back to *Parabolas*: the vertex is where the slope is nothing.

```python exec
id: the-derivative-as-a-function-2
def quadratic(x):
    return x ** 2 + 6 * x + 5


# Completing the square said the vertex was at x = -3. Ask the slope instead.
for x in [-5, -4, -3, -2, -1]:
    print(f"slope at x = {x:>3}: {derivative_at(quadratic, x):>7.4f}")
```

Zero at −3, exactly where completing the square put the vertex. **Two completely different methods, same answer** — which is the sort of agreement that tells you both are right.

### Your turn

Find the turning points of `x³ − 3x` by looking for where its slope is zero.

```python exec
id: your-turn-1
def cubic(x):
    return x ** 3 - 3 * x


# Your investigation here.
```

## Rules Instead of Limits

Computing a limit every time would be exhausting. Fortunately the answers follow patterns.

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

Compare each row against the powers of the x values and the pattern comes out:

- `x` has slope 1 everywhere
- `x²` has slope `2x`
- `x³` has slope `3x²`
- `x⁴` has slope `4x³`

> **The power rule:** the derivative of `xⁿ` is `n·xⁿ⁻¹`.

Bring the power down to the front, and reduce it by one.

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

> **The sum rule:** the derivative of `f + g` is the derivative of `f` plus the derivative of `g`.

Which is exactly as convenient as it sounds. A polynomial is a sum of powers, so you can differentiate the whole thing term by term.

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

### Multiplying things together

The rule people expect here is wrong, and it is worth seeing that it is wrong before seeing the right one.

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

Not equal, and not close. The derivative of a product is **not** the product of the derivatives.

> **The product rule:** the derivative of `f·g` is `f′·g + f·g′`.

Each one differentiated in turn, with the other left alone, and the two added.

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

There is a sanity check available here. `x² · x³` is `x⁵`, whose derivative by the power rule is `5x⁴`. The product rule gives `2x·x³ + x²·3x² = 2x⁴ + 3x⁴ = 5x⁴`. The same.

### Your turn

Differentiate these by hand, then check each numerically.

- `3x⁴ − 2x + 7`
- `(x + 1)(x² − 3)`
- `x²·(x + 5)`

```python exec
id: your-turn-2
# Your answers, then a check with derivative_at.
```

## The Chain Rule

One more, and it is a bonus rather than a drill — worth meeting, not worth grinding.

What happens when a function is inside another function?

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

Those last two agree.

> **The chain rule:** the derivative of `f(g(x))` is `f′(g(x)) · g′(x)`.

Differentiate the outside, leaving the inside alone; then multiply by the derivative of the inside.

The intuition is about rates stacking. If `u` changes three times as fast as `x`, and `y` changes twice as fast as `u`, then `y` changes six times as fast as `x`. Rates multiply along a chain, which is why this is the one rule with a name that describes what it does.

### Your turn

Differentiate `(3x + 2)⁵` using the chain rule, then check.

```python exec
id: your-turn-3
# Your answer, then the check.
```

## What Is Not Here

Two things are deliberately left out, and it is worth saying so rather than leaving you to wonder.

**The quotient rule**, for dividing one function by another, is mechanical and you can get by with the product rule and a negative power.

**Integration by parts** is a technique for a course that needs a lot of integration. This one does not.

Calculus is not the focus of this course. What matters is that you know what a derivative *is* — a rate of change, a tangent slope, a limit — and that you can compute simple ones. Grinding through the remaining techniques would cost weeks and buy very little.

## Reflection

The slope of a curve at a single point, which is a limit, which is what made the question answerable at all.

**Three descriptions, one number.** A limit of chords, the slope of the tangent, and a rate of change. Which one you reach for depends on what you are doing.

**The derivative is a function.** Not a number — a rule that gives the slope wherever you ask.

**Zero slope is a turning point.** The most useful fact here, and it agrees with what completing the square told you in *Parabolas*.

**The rules save you the limit.** Bring the power down and reduce it by one; sums come apart; products do not, and need `f′g + fg′`; nesting multiplies the rates.

Write a few sentences: pick something that changes over time — a bank balance, a temperature, a download. What would its derivative be, in words, and what units would it have?

## Where to Read More

Grant Sanderson (3Blue1Brown) (2017). *Essence of Calculus, Chapter 2: The
Paradox of the Derivative.* <https://www.youtube.com/watch?v=9vKqVkMQHKk>.
The same chords-closing-in-on-a-tangent picture this page draws, and why
"instantaneous rate of change" is a stranger idea than it sounds.
