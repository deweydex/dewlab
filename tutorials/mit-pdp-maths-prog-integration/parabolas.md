---
title: "Parabolas"
slug: parabolas
module: mit-pdp-maths-prog-integration
module_title: "Programming and Maths, Integrated"
year: "2026-2027"
series: maths-and-programming
version: 2026.08.23.1
covers:
  every-quadratic-is-the-same-curve:
    covers: [MIT-3.4]
  the-form-that-tells-you-where-the-bottom-is:
    covers: [MIT-3.4]
  doing-the-rearrangement:
    covers: [MIT-3.4]
  roots-from-the-same-form:
    covers: [MIT-3.4]
---

# Parabolas

**Maths for IT**

A quadratic makes a curve with one turn in it, and that curve has a name: a **parabola**. Every quadratic makes one, and — this is the surprising part — they are all the same shape.

In *Cracking Equations* you solved quadratics with the formula. In *Drawing Functions* you plotted them. This tutorial is about a third thing you can do to one: **rewrite it into a form that tells you where the curve turns, just by looking at it.**

The rewriting is called completing the square. Most people meet it as a trick with no obvious purpose, which is a shame, because its purpose is the best reason to learn it.

## Every Quadratic Is the Same Curve

Start with something worth being surprised by.

```python exec
id: every-quadratic-is-the-same-curve-1
import matplotlib.pyplot as plt

def draw(f, low=-6, high=6, steps=300, label=None, ax=None):
    xs = [low + (high - low) * i / steps for i in range(steps + 1)]
    if ax is None:
        fig, ax = plt.subplots()
        ax.axhline(0, color="black", linewidth=0.8)
        ax.axvline(0, color="black", linewidth=0.8)
        ax.grid(alpha=0.3)
    ax.plot(xs, [f(x) for x in xs], label=label)
    if label:
        ax.legend()
    return ax


def quadratic(a, b, c):
    return lambda x: a * x ** 2 + b * x + c


ax = draw(quadratic(1, 0, 0), label="x^2")
draw(quadratic(1, -6, 5), label="x^2 - 6x + 5", ax=ax)
draw(quadratic(1, 4, 7), label="x^2 + 4x + 7", ax=ax)
ax.set_ylim(-6, 20)
ax.set_title("Three quadratics")
```

Three different curves. Now slide each one so its lowest point sits at the origin.

```python exec
id: every-quadratic-is-the-same-curve-2
# Each of these has been shifted by hand so its turning point is at (0, 0).
ax = draw(lambda x: x ** 2, label="x^2")
draw(lambda x: (x + 3) ** 2 - 4 + 4 - (x + 3) ** 2 + x ** 2, label="", ax=ax)
ax.set_ylim(-1, 20)

# Simpler: shift each one and plot the result.
fig, ax2 = plt.subplots()
ax2.axhline(0, color="black", linewidth=0.8)
ax2.axvline(0, color="black", linewidth=0.8)
ax2.grid(alpha=0.3)
xs = [x / 30 for x in range(-150, 151)]
ax2.plot(xs, [x ** 2 for x in xs], linewidth=4, alpha=0.3, label="x^2")
ax2.plot(xs, [(x + 3) ** 2 - 4 - (-4) for x in xs], "--", label="x^2 - 6x + 5, shifted")
ax2.plot(xs, [(x - 2) ** 2 + 3 - 3 for x in xs], ":", label="x^2 + 4x + 7, shifted")
ax2.legend()
ax2.set_title("All three, moved on top of each other")
```

They land on each other exactly.

**There is one parabola.** Every quadratic with the same `a` is that curve, slid sideways and up or down. Change `a` and it stretches, but the shape underneath is still the same.

That means a quadratic really only has two interesting facts about it: **where its turning point is**, and **how wide it is**. Everything else follows.

## The Form That Tells You Where the Bottom Is

Here is the same function written two ways.

```python exec
id: the-form-that-tells-you-where-the-bottom-is-1
def standard(x):
    return x ** 2 + 6 * x + 5


def completed(x):
    return (x + 3) ** 2 - 4


for value in [-6, -3, 0, 2, 7]:
    print(f"x = {value:>3}    standard: {standard(value):>4}    completed: {completed(value):>4}")
```

Identical, every time. They are the same function.

Now plot the second one and look at where the two numbers in it went.

```python exec
id: the-form-that-tells-you-where-the-bottom-is-2
ax = draw(completed, low=-9, high=3, label="(x + 3)^2 - 4")
ax.plot([-3], [-4], "o", markersize=9)
ax.annotate("(-3, -4)", (-3, -4), textcoords="offset points", xytext=(12, -14))
ax.set_ylim(-6, 20)
ax.set_title("The turning point is written in the expression")
```

The turning point is at `(−3, −4)`, and the expression is `(x + 3)² − 4`.

**The two numbers in the completed form are the two coordinates of the turning point** — the first with its sign flipped, which is the one thing to watch. `(x + 3)²` puts the bottom at `x = −3`, because `x = −3` is what makes the bracket zero.

And it has to be the bottom, because a square is never negative. `(x + 3)²` is zero at `x = −3` and positive everywhere else, so `−4` is the smallest this function ever gets.

That last sentence is the whole idea. **Completing the square is worth doing because it makes the answer visible**, and the reason it works is that a squared thing cannot be negative.

The name for that turning point is the **vertex**.

## Doing the Rearrangement

The mechanics, once, slowly.

Start with `x² + 6x + 5`. The goal is a squared bracket plus a number.

Begin by asking what bracket would give you the `x²` and the `6x`. Expanding `(x + h)²` gives `x² + 2hx + h²`, so the middle term is `2h` — which means **halving the middle coefficient tells you what goes in the bracket.** Half of 6 is 3, so the bracket is `(x + 3)`.

```python exec
id: doing-the-rearrangement-1
h = 3
print("(x + 3)^2 expands to:")
for x in [0, 1, 2, 5]:
    print(f"   x={x}:  {(x + h) ** 2}   and   x^2 + 6x + 9 = {x**2 + 6*x + 9}")
```

`(x + 3)²` is `x² + 6x + 9`. That is nearly what we want — it has the right `x²` and the right `6x`, but a 9 where we wanted a 5.

So subtract the difference:

`x² + 6x + 5 = (x + 3)² − 9 + 5 = (x + 3)² − 4`

Three steps: halve the middle number, square it and take it away again, then add on whatever was there originally.

```python exec
id: doing-the-rearrangement-2
def complete_the_square(b, c):
    """Rewrite x^2 + bx + c as (x + h)^2 + k, and return h and k."""
    h = b / 2
    k = c - h ** 2
    return h, k


for b, c in [(6, 5), (-4, 1), (2, 7), (-10, 21)]:
    h, k = complete_the_square(b, c)
    print(f"x^2 + {b}x + {c}  =  (x + {h})^2 + {k}     vertex at ({-h}, {k})")
```

```python exec
id: doing-the-rearrangement-3
# And a check: do the two forms agree everywhere?
import random

def agree(b, c, tries=200):
    h, k = complete_the_square(b, c)
    for _ in range(tries):
        x = random.uniform(-50, 50)
        if abs((x ** 2 + b * x + c) - ((x + h) ** 2 + k)) > 1e-9:
            return False
    return True


print(all(agree(b, c) for b, c in [(6, 5), (-4, 1), (2, 7), (-10, 21), (0, 0)]))
```

### Your turn

Complete the square on these four by hand, then check each against the function above.

- `x² + 8x + 3`
- `x² − 2x + 6`
- `x² + 5x`
- `x² − 12x + 36`

The last one is worth thinking about before you compute it.

```python exec
id: your-turn-1
# Your answers as comments, then:
# print(complete_the_square(8, 3))
```

## Roots from the Same Form

The completed form also hands you the roots, and it hands them over more honestly than the formula does.

A root is where the function is zero. So set the completed form to zero and unwrap it:

```
(x + 3)² − 4 = 0
(x + 3)²     = 4
 x + 3       = ±2
 x           = −3 ± 2
```

which is `−1` and `−5`.

```python exec
id: roots-from-the-same-form-1
import math

def roots_by_completing(b, c):
    h, k = complete_the_square(b, c)
    if -k < 0:
        return "No real roots — the vertex is above the axis."
    root = math.sqrt(-k)
    return (-h + root, -h - root)


def roots_by_formula(b, c):
    d = b ** 2 - 4 * c
    if d < 0:
        return "No real roots."
    return ((-b + math.sqrt(d)) / 2, (-b - math.sqrt(d)) / 2)


for b, c in [(6, 5), (-4, 1), (2, 7), (-10, 21)]:
    print(f"x^2 + {b}x + {c}")
    print("   completing the square:", roots_by_completing(b, c))
    print("   the formula:          ", roots_by_formula(b, c))
```

The same answers, both ways.

They are the same answers because **the quadratic formula is completing the square, done once in general so nobody has to do it again.** Somebody worked through the steps above with letters instead of numbers, and what fell out was the formula you have been using.

That is worth knowing for its own sake. A formula that arrives from nowhere is a thing to memorise; a formula you have seen derived is a thing you could rebuild if you forgot it.

### The ± is not decoration

Look at the step `(x + 3)² = 4`. The next line is `x + 3 = ±2`, because both `2² ` and `(−2)²` are 4.

That is where the two roots come from, and it is why a quadratic has two of them. The `±` in the formula is the same `±`, carried through.

## When There Is Nothing to Find

```python exec
id: when-there-is-nothing-to-find-1
ax = draw(quadratic(1, 2, 7), low=-7, high=5, label="x^2 + 2x + 7")
h, k = complete_the_square(2, 7)
ax.plot([-h], [k], "o", markersize=9)
ax.annotate(f"vertex at ({-h}, {k})", (-h, k), textcoords="offset points", xytext=(12, -6))
ax.set_ylim(-2, 30)
ax.set_title("A parabola with no roots")
```

The vertex is at `(−1, 6)`, which is above the axis, and the curve opens upwards. So it never comes down to zero and there are no real roots — and you can see that from the completed form without computing anything, because `(x + 1)² + 6` is a non-negative thing plus 6.

The formula says the same by giving a negative discriminant. The completed form says it in a way you can picture.

And [When There Is No Answer](tutorial:complex-roots) is where those roots have gone. They exist; they are just not on this line.

### Your turn

Without plotting: which of these have real roots? Use the completed form to decide.

```python exec
id: your-turn-2
# a: x^2 - 6x + 5
# b: x^2 + 4x + 9
# c: x^2 - 2x + 1

# Your answers as comments, then check with complete_the_square.
```

## Reflection

One curve, moved around, and one rearrangement that tells you where it has been moved to.

**Completing the square is rewriting, not solving.** `x² + 6x + 5` and `(x + 3)² − 4` are the same function; the second one just has the answer written on the outside.

**The trick is halving, and it is not arbitrary.** `(x + h)²` has `2h` in the middle, so halving the middle coefficient is how you find `h`. Expand the bracket once and the step stops being a rule to remember.

**The quadratic formula is this, done in general.** If you ever forget it, you can rebuild it.

**No roots is a fact about the picture.** The vertex is above the axis and the curve opens upwards, so nothing crosses. No amount of algebra will produce a real answer, and that is not a failure.

Write a few sentences: for `x² − 6x + 5`, which of the two forms would you rather be given, and for what question?
