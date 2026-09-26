---
title: "Parabolas: completing the square"
year: "2026-2027"
version: 2026.09.25.1
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

# Parabolas: completing the square

A quadratic makes a curve with one turn in it. A *parabola* is the curve
that a quadratic makes.

In [Solving equations: linear, quadratic and simultaneous](tutorial:cracking-equations)
we solved quadratics with the formula. In
[Functions and their graphs](tutorial:drawing-functions) we drew them.
On this page we do a third thing with a quadratic. We rewrite it in a
form that shows where the curve turns, so that we can read it straight
from the expression.

This rewriting is called completing the square. Many people learn it as
a trick, without being told what it is for. Its purpose is the best
reason to learn it, so we start there.

On this page we:

- see that many different quadratics are one curve, moved around
- rewrite a quadratic so that its turning point shows
- learn the steps for doing that rewriting
- find the roots from the same form, and see where the quadratic formula
  comes from

Every quadratic on this page starts with $x^2$, so the number in front
of $x^2$ is 1. If it is another number, we first take that number out as
a factor, for example $2x^2 + 8x + 6 = 2(x^2 + 4x + 3)$. Then we work on
the part inside the bracket.

## Every quadratic is the same curve

Here are three quadratics. How are the three curves different?

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

The three curves sit in different places. Now let's slide each one, so
that its lowest point sits at the origin, $(0, 0)$. What do you expect
to see?

```python exec
id: every-quadratic-is-the-same-curve-2
# Shift each one by hand so its turning point lands on (0, 0).
fig, ax2 = plt.subplots()
ax2.axhline(0, color="black", linewidth=0.8)
ax2.axvline(0, color="black", linewidth=0.8)
ax2.grid(alpha=0.3)
xs = [x / 30 for x in range(-150, 151)]
ax2.plot(xs, [x ** 2 for x in xs], linewidth=4, alpha=0.3, label="x^2")
ax2.plot(xs, [quadratic(1, -6, 5)(x + 3) + 4 for x in xs], "--", label="x^2 - 6x + 5, shifted")
ax2.plot(xs, [quadratic(1, 4, 7)(x - 2) - 3 for x in xs], ":", label="x^2 + 4x + 7, shifted")
ax2.legend()
ax2.set_title("All three, moved on top of each other")
```

The three curves land exactly on top of each other.

**They are one parabola.** Every quadratic with the same $a$ (the number
in front of $x^2$) is the same curve, slid sideways and up or down. A
different $a$ stretches the curve, or turns it upside down if $a$ is
negative. The shape underneath stays the same.

So a quadratic has only a few facts that matter:

- **where its turning point is**
- **how wide it is**, and which way it opens

Everything else follows from those.

## The form that tells you where the bottom is

Here is the same function written in two ways. Do the two columns
agree?

```python exec
id: the-form-that-tells-you-where-the-bottom-is-1
def standard(x):
    return x ** 2 + 6 * x + 5


def completed(x):
    return (x + 3) ** 2 - 4


for value in [-6, -3, 0, 2, 7]:
    print(f"x = {value:>3}    standard: {standard(value):>4}    completed: {completed(value):>4}")
```

The two columns are the same every time, because they are the same
function.

Now we plot the second form. Can you find its two numbers, 3 and $-4$,
in the picture?

```python exec
id: the-form-that-tells-you-where-the-bottom-is-2
ax = draw(completed, low=-9, high=3, label="(x + 3)^2 - 4")
ax.plot([-3], [-4], "o", markersize=9)
ax.annotate("(-3, -4)", (-3, -4), textcoords="offset points", xytext=(12, -14))
ax.set_ylim(-6, 20)
ax.set_title("The turning point is written in the expression")
```

The turning point is at $(-3, -4)$, and the expression is
$(x + 3)^2 - 4$.

**The two numbers in the completed form give the two coordinates of the
turning point.** Watch the first one. Its sign flips. The bracket
$(x + 3)^2$ puts the turning point at $x = -3$, because $x = -3$ is the
value that makes the bracket zero.

That flip catches almost everybody at least once. So exam papers, and
most books, write the completed form with a minus sign in the bracket:

$$a(x - h)^2 + k$$

Then the vertex is $(h, k)$, and there is nothing to flip. Our example
is $(x - (-3))^2 + (-4)$, so $h = -3$ and $k = -4$. Every quadratic on
this page has $a = 1$, so from here on we write $(x - h)^2 + k$.

Why is this point the bottom of the curve? Because a square is never
negative. $(x + 3)^2$ is zero at $x = -3$ and positive everywhere else.
So $-4$ is the smallest value this function ever gives.

That is the whole idea. Completing the square is worth doing because it
makes the answer visible. It works because a squared number cannot be
negative.

The *vertex* of a parabola is its turning point. It is the lowest point
when the parabola opens upwards, and the highest point when it opens
downwards.

## Doing the rearrangement

Let's do the steps once, slowly.

We start with $x^2 + 6x + 5$. The goal is a squared bracket plus a
number.

First, which bracket would give us the $x^2$ and the $6x$? Multiplying
out $(x - h)^2$ gives

$$(x - h)^2 = x^2 - 2hx + h^2$$

The middle term is $-2h$ times $x$. So **half of the middle number, with
its sign changed, is $h$.** Half of 6 is 3, so $h = -3$, and the bracket
is $(x - (-3))$, which is $(x + 3)$.

What does $(x + 3)^2$ multiply out to? The cell compares it with
$x^2 + 6x + 9$ for a few values of $x$.

```python exec
id: doing-the-rearrangement-1
h = -3
print("(x + 3)^2 expands to:")
for x in [0, 1, 2, 5]:
    print(f"   x={x}:  {(x - h) ** 2}   and   x^2 + 6x + 9 = {x**2 + 6*x + 9}")
```

So $(x + 3)^2 = x^2 + 6x + 9$. This is close to what we want. It has the
right $x^2$ and the right $6x$, but it has a 9 where we want a 5.

So we take away the 9 and add the 5:

$$x^2 + 6x + 5 = (x + 3)^2 - 9 + 5 = (x + 3)^2 - 4$$

Here are the steps for $x^2 + bx + c$:

1. Halve the middle number $b$, and change its sign. Call the result
   $h$. This gives the bracket $(x - h)^2$.
2. Square $h$, and take $h^2$ away, because the bracket added it.
3. Add the number $c$ that was there at the start.

In the example, $h = -3$, so we take away $(-3)^2 = 9$ and add 5. The
number at the end is $k = c - h^2 = 5 - 9 = -4$.

The next cell does the same steps in code. Every quadratic on this page
starts with $x^2$, so $a = 1$, and `complete_the_square` takes only $b$
and $c$, in the same order as `solve(a, b, c)` on the complex numbers
page. The small function `signed`
only makes the output easier to read. It writes a number with its sign
in front, so that the cell prints `- 4` and not `+ -4`.

```python exec
id: doing-the-rearrangement-2
def complete_the_square(b, c):
    """Rewrite x^2 + bx + c as (x - h)^2 + k, and return h and k."""
    h = -b / 2
    k = c - h ** 2
    return h, k


def signed(number):
    """Write a number with its sign in front, as ' + 3' or ' - 4'."""
    if number < 0:
        return f" - {-number:g}"
    return f" + {number:g}"


for b, c in [(6, 5), (-4, 1), (2, 7), (-10, 21)]:
    h, k = complete_the_square(b, c)
    print(f"x^2{signed(b)}x{signed(c)}  =  (x{signed(-h)})^2{signed(k)}     vertex at ({h:g}, {k:g})")
```

Do the two forms really agree for every $x$? This cell tries 200 random
values of $x$ for each quadratic.

```python exec
id: doing-the-rearrangement-3
# And a check: do the two forms agree everywhere?
import random

def agree(b, c, tries=200):
    h, k = complete_the_square(b, c)
    for _ in range(tries):
        x = random.uniform(-50, 50)
        if abs((x ** 2 + b * x + c) - ((x - h) ** 2 + k)) > 1e-9:
            return False
    return True


print(all(agree(b, c) for b, c in [(6, 5), (-4, 1), (2, 7), (-10, 21), (0, 0)]))
```

### Your turn

Here are four quadratics:

- $x^2 + 8x + 3$
- $x^2 - 2x + 6$
- $x^2 + 5x$
- $x^2 - 12x + 36$

1. Complete the square on each one by hand. Write your answers as
   comments in the cell.
2. Check each answer with `complete_the_square`.

Look at the last one before you start. What do you notice about
it?

```python exec
id: your-turn-1
# Your answers as comments, then:
# print(complete_the_square(8, 3))
```

## Roots from the same form

The completed form also gives us the roots. Many people find the roots
easier to see this way than with the formula.

A root is a value of $x$ where the function is zero. So we set the
completed form equal to zero and undo it one step at a time:

$$
\begin{aligned}
(x + 3)^2 - 4 &= 0 \\
(x + 3)^2 &= 4 \\
x + 3 &= \pm 2 \\
x &= -3 \pm 2
\end{aligned}
$$

That gives $x = -1$ and $x = -5$.

The next cell finds roots in two ways: by completing the square, and by
the formula. Do you expect the two methods to agree?

```python exec
id: roots-from-the-same-form-1
import math

def roots_by_completing(b, c):
    h, k = complete_the_square(b, c)
    if k > 0:
        return "No real roots — the vertex is above the axis."
    root = math.sqrt(-k)
    return (h + root, h - root)


def roots_by_formula(b, c):
    d = b ** 2 - 4 * c
    if d < 0:
        return "No real roots."
    return ((-b + math.sqrt(d)) / 2, (-b - math.sqrt(d)) / 2)


for b, c in [(6, 5), (-4, 1), (2, 7), (-10, 21)]:
    print(f"x^2{signed(b)}x{signed(c)}")
    print("   completing the square:", roots_by_completing(b, c))
    print("   the formula:          ", roots_by_formula(b, c))
```

Both methods give the same answers.

Why? **The quadratic formula is completing the square, done once with
letters so that nobody has to do it again.** Somebody did the
steps above with $a$, $b$ and $c$ in place of numbers. The result was
the formula we have been using.

If you have seen a formula built, you can build it again when you
forget it.

### The ± matters

Look at the step $(x + 3)^2 = 4$. The next line is $x + 3 = \pm 2$,
because $2^2 = 4$ and $(-2)^2 = 4$ as well.

This step gives the two roots, so a quadratic can have two of them. The $\pm$ in the quadratic formula is the same $\pm$,
carried through.

## When there is nothing to find

Where is the vertex of $x^2 + 2x + 7$? Does the curve reach the
horizontal axis?

```python exec
id: when-there-is-nothing-to-find-1
ax = draw(quadratic(1, 2, 7), low=-7, high=5, label="x^2 + 2x + 7")
h, k = complete_the_square(2, 7)
ax.plot([h], [k], "o", markersize=9)
ax.annotate(f"vertex at ({h:g}, {k:g})", (h, k), textcoords="offset points", xytext=(12, -6))
ax.set_ylim(-2, 30)
ax.set_title("A parabola with no roots")
```

The vertex is at $(-1, 6)$, above the axis, and the curve opens
upwards. So the curve never comes down to zero, and there are no real
roots.

We can see this from the completed form, $(x + 1)^2 + 6$, without
calculating anything. The square $(x + 1)^2$ is never negative, so the
whole expression is always at least 6.

The formula tells us the same thing with a negative discriminant. The
completed form says it in a way we can picture.

And [Complex numbers: roots that are not real](tutorial:complex-roots)
showed where those roots have gone. They exist, but they are not on
this line.

### Your turn

Here are three quadratics:

- a: $x^2 - 6x + 5$
- b: $x^2 + 4x + 9$
- c: $x^2 - 2x + 1$

1. Without plotting, use the completed form to decide which of them
   have real roots. Write your answers as comments.
2. Check with `complete_the_square`.

```python exec
id: your-turn-2
# a: x^2 - 6x + 5
# b: x^2 + 4x + 9
# c: x^2 - 2x + 1

# Your answers as comments, then check with complete_the_square.
```

## Reflection

There is one curve, moved around. One rearrangement tells us where it
has been moved to.

Here are four ideas to take with you.

**Completing the square rewrites a quadratic. It does not solve it.** $x^2 + 6x + 5$ and
$(x + 3)^2 - 4$ are the same function. The second one has the turning
point written on the outside.

**The halving step has a reason.** $(x - h)^2$ has $-2h$ in the middle,
so halving the middle number, and changing its sign, finds $h$. Multiply
out the bracket once, and the step stops being a rule to remember.

**The quadratic formula is completing the square, done with letters.**
If you ever forget the formula, you can build it again.

**You can see "no real roots" in the picture.** The vertex is above the
axis and the curve opens upwards, so the curve never crosses. No amount
of algebra will give a real answer.

Think about $x^2 - 6x + 5$. Which of the two forms would you prefer to
be given, and for which question? Write a few sentences.

## Where to read more

Khan Academy. *Example 3: Completing the Square.*
<https://www.youtube.com/watch?v=TV5kDqiJ1Os>. It shows the same
halve-square-subtract steps as this page, on a different quadratic.

Stand-up Maths (2016). *There is only One True Parabola.*
<https://www.youtube.com/watch?v=hoh4TmPzu1w>. Every parabola is the same
curve, made bigger or smaller and moved. Matt Parker shows why. Completing
the square finds how much it was moved. About nine minutes.
