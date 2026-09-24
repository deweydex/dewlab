---
title: "Complex numbers: roots that are not real"
year: "2026-2027"
version: 2026.09.23.1
covers:
  where-the-solver-stops:
    covers: [MIT-1.10]
  inventing-a-new-number:
    covers: [MIT-1.10]
    touches: [MIT-2.1]
  roots-that-are-not-real:
    covers: [MIT-1.10]
  complex-roots-come-in-pairs:
    covers: [MIT-1.10]
---

# Complex numbers: roots that are not real

In [Solving equations: linear, quadratic and simultaneous](tutorial:cracking-equations)
we wrote a solver for quadratic equations. It works out the discriminant.
When the discriminant is negative, the solver says "no real solutions"
and stops.

On this page we ask what lies past that stop. The answer was there all
along. Mathematicians found it with the same idea they had used three
times before, and that idea matters more than the arithmetic.

On this page we:

- look again at the quadratics our solver cannot answer
- invent a new number, $i$, whose square is $-1$
- use it to find roots that are not on the number line
- see why those roots always come in pairs

## Where the solver stops

Here is a short version of our solver, with three quadratics to try. The
first is a quadratic with two roots, and the second has one. The third,
$x^2 + 1 = 0$, is the simplest quadratic that has no real roots.

```python exec
id: the-cliff-edge-1
import math

def solve(a, b, c):
    """The quadratic solver from the Solving equations page."""
    discriminant = b ** 2 - 4 * a * c
    if discriminant < 0:
        return "No real solutions."
    root = math.sqrt(discriminant)
    return ((-b + root) / (2 * a), (-b - root) / (2 * a))


print("x^2 - 5x + 6 = 0  ->", solve(1, -5, 6))
print("x^2 - 4x + 4 = 0  ->", solve(1, -4, 4))
print("x^2 + 1 = 0       ->", solve(1, 0, 1))
```

We get three kinds of answer: two roots, one root, and a refusal.

What does the refusal look like as a picture? The next cell draws all
three curves.

```python exec
id: the-cliff-edge-2
import matplotlib.pyplot as plt

xs = [x / 20 for x in range(-100, 101)]

fig, ax = plt.subplots()
ax.plot(xs, [x ** 2 - 5 * x + 6 for x in xs], label="x^2 - 5x + 6")
ax.plot(xs, [x ** 2 - 4 * x + 4 for x in xs], label="x^2 - 4x + 4")
ax.plot(xs, [x ** 2 + 1 for x in xs], label="x^2 + 1")
ax.axhline(0, color="black", linewidth=0.8)
ax.set_ylim(-3, 12)
ax.legend()
ax.set_title("Crossing the axis twice, once, and never")
```

The first curve crosses the horizontal axis twice, and the second
touches it once. The third curve never comes down to the axis at all.

That is what "no real solutions" looks like. It is a true description,
as long as we only accept numbers that sit on that horizontal line.

So "no real solutions" says less than it seems to. It says there is no
answer *on this line*. It does not say there is no answer anywhere.

## Inventing a new number

In [Number types, powers and logarithms](tutorial:numbers-and-their-families)
we met the families of numbers: the naturals $\mathbb{N}$, the integers
$\mathbb{Z}$, the rationals $\mathbb{Q}$ and the reals $\mathbb{R}$.
What made each new family appear? Look at the pattern in the list below.

- $\mathbb{N}$ is the counting numbers. We can always add them. But
  $3 - 5$ has no answer in $\mathbb{N}$.
- $\mathbb{Z}$ adds the negative numbers, so now subtraction always
  works. But $3 \div 5$ has no answer in $\mathbb{Z}$.
- $\mathbb{Q}$ adds the fractions, so now division always works (except
  division by zero). But $\sqrt{2}$ has no answer in $\mathbb{Q}$.
- $\mathbb{R}$ fills in the irrational numbers, so now most things work.
  But $\sqrt{-1}$ has no answer in $\mathbb{R}$.

Each step happened because somebody would not accept "there is no
answer". They invented the number that makes an answer. People resisted
several of these inventions when they were new, and negative numbers
and irrational numbers met strong resistance. Today all of them are
taught in school.

So the next step is not a special trick. It is the same move, one more
time.

What do you think $i$ squared will be? Run the cell to check.

```python exec
id: inventing-a-number-1
# In Python, the imaginary unit is written 1j rather than i, because
# engineers already used i for current and the notation stuck.
i = 1j

print("i        =", i)
print("i squared =", i ** 2)
print("So the square root of -1 is:", i)
```

Python writes $-1$ as `(-1+0j)`, which is $-1$ plus zero lots of $i$.

The *imaginary unit* $i$ is a number whose square is $-1$:

$$i^2 = -1$$

That is the whole definition, and everything else on this page follows
from it. (The number $-i$ is also a square root of $-1$, because
$(-i)^2 = i^2 = -1$ as well.)

A *complex number* is a number with a real part and an imaginary part,
such as $3 + 2i$. Here the *real part* is 3 and the *imaginary part* is
2. The set of all complex numbers is called $\mathbb{C}$.

$\mathbb{C}$ is the fifth family of numbers, and it is the last one we
need for solving equations. Every polynomial equation of degree 1 or
more has an answer in $\mathbb{C}$. That is not true of any of the four
families before it.

Python works with complex numbers directly. What do you expect for
`z + w`? Run the cell and compare.

```python exec
id: inventing-a-number-2
z = 3 + 2j
w = 1 - 4j

print("z       =", z)
print("z + w   =", z + w)
print("z * w   =", z * w)
print("real part of z:", z.real)
print("imaginary part of z:", z.imag)
```

To add, Python adds the real parts together and the imaginary parts
together: $(3 + 1) + (2 - 4)i = 4 - 2i$.

Now look at `z * w`. We can multiply it out by hand, the same way we
multiply out two brackets:

$$(3 + 2i)(1 - 4i) = 3 - 12i + 2i - 8i^2$$

The last term is where the definition does its work. Since $i^2 = -1$,
the term $-8i^2$ is $-8 \times (-1) = +8$. So the total is
$3 + 8 - 10i = 11 - 10i$, which matches Python's `(11-10j)`.

The $i^2$ turning back into a real number is the only unusual step.

## Roots that are not real

Here is the solver again, with one change. It uses Python's `cmath`
module in place of `math`. The `cmath` module works with complex
numbers, and `cmath.sqrt` will take the square root of a negative number.

Compare this code with the first solver. What is missing?

```python exec
id: roots-that-are-not-real-1
import cmath

def solve(a, b, c):
    """The same solver, using cmath instead of math."""
    discriminant = b ** 2 - 4 * a * c
    root = cmath.sqrt(discriminant)
    return ((-b + root) / (2 * a), (-b - root) / (2 * a))


print("x^2 - 5x + 6 = 0  ->", solve(1, -5, 6))
print("x^2 - 4x + 4 = 0  ->", solve(1, -4, 4))
print("x^2 + 1 = 0       ->", solve(1, 0, 1))
```

**The `if` is gone.** There is no special case any more, because
nothing can fail. The same three lines answer all three questions. The
roots of $x^2 + 1 = 0$ are $i$ and $-i$.

This is a fact about mathematics, not only about Python. Making the
number system bigger removed a special case. It did not add one. Two
roots, one root and no real roots turn out to be one situation. We can
see all of it once we stand in $\mathbb{C}$.

### Does it work?

An answer is only worth having if it survives a check. Remember that a
root is a number that makes the expression equal zero. So we can put each root
back into its quadratic and see what comes out.

What do you expect to see in the last line for each quadratic?

```python exec
id: roots-that-are-not-real-2
def evaluate(a, b, c, x):
    return a * x ** 2 + b * x + c


for coefficients in [(1, 0, 1), (1, 2, 5), (2, -3, 4)]:
    a, b, c = coefficients
    first, second = solve(a, b, c)
    print(f"{a}x^2 + {b}x + {c}")
    print("   roots:", first, "and", second)
    print("   putting them back in:", evaluate(a, b, c, first),
          "and", evaluate(a, b, c, second))
```

Every root gives zero. For the last quadratic we see
`(4.440892098500626e-16+0j)`. The `e-16` means "times $10^{-16}$", so
this number is about 0.000000000000000444. It is zero plus a tiny
rounding error from the computer's arithmetic.

This check is the whole argument. A root is a number that makes the
expression zero. These numbers make the expression zero. So they are
roots. We do not have to take the definition on trust.

### Your turn

Here are three quadratics:

- $x^2 + 4 = 0$
- $x^2 - 2x + 5 = 0$
- $x^2 + 6x + 13 = 0$

1. Solve each one by hand with the quadratic formula. Write each answer
   in the form $a + bi$.
2. Check each answer with the solver in the cell below.

```python exec
id: your-turn-1
# Your answers, then the check.
# print(solve(1, 0, 4))
```

## Complex roots come in pairs

Look at the roots below. Before we give it a name, what do you notice
about each pair?

```python exec
id: they-come-in-pairs-1
for coefficients in [(1, 0, 1), (1, 2, 5), (1, 6, 13), (1, -2, 10)]:
    a, b, c = coefficients
    first, second = solve(a, b, c)
    print(f"{first}   and   {second}")
```

In every pair, the two roots have the same real part and opposite
imaginary parts. For example, $1 + 3i$ comes with $1 - 3i$.

The *conjugate* of a complex number is the number with the same real
part and the opposite imaginary part. So the conjugate of $2 + 3i$ is
$2 - 3i$. When a quadratic has ordinary real coefficients, its complex
roots always come as a conjugate pair.

Why? The reason is in the quadratic formula:

$$x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$$

The only place an $i$ can come in is the square root of a negative
discriminant. That square root appears once with a $+$ in front of it,
and once with a $-$. Nothing else in the formula can make an $i$.

The picture tells the same story. A parabola crosses the axis twice,
touches it once, or misses it. It cannot cross once and stop. So the
roots come two at a time. If one of them has left the real line, the
other one has left too.

### Your turn

The equation $x^2 - 6x + 25 = 0$ has a root at $3 + 4i$. Without
working anything out, can you say what the other root is? How do you
know?

Write your answer as a comment in the cell, then check it with the
solver.

```python exec
id: your-turn-2
# Your answer as a comment, then check it.
# print(solve(1, -6, 25))
```

## Reflection

In [Solving equations: linear, quadratic and simultaneous](tutorial:cracking-equations)
our solver stopped at "no real solutions". That was accurate, but it
was not the end. "No real solutions" tells us which numbers we were
willing to use. In a larger set, the answer was waiting.

Here are three ideas to take with you.

**Each new family of numbers was invented for the same reason.**
Somebody would not accept that a sensible question had no answer.
$\mathbb{C}$ is the fourth of these extensions and the last one. In
$\mathbb{C}$, every polynomial equation of degree 1 or more has a
solution.

**Making the numbers bigger removed a special case.** The solver got
shorter, not longer. That is often a sign that a new idea is the right
one.

**You can check an answer you do not fully believe.** Put the root back
into the equation. If it gives zero, it is a root, however strange it
looks.

Before this page, what did you think "no solution" meant? Has that
changed? Write a few sentences.

## Where to Read More

Stephen Welch (Welch Labs) (2015). *Imaginary Numbers Are Real
[Part 1: Introduction].* <https://www.youtube.com/watch?v=T647CGsuOVU>.
The same story this page tells — number systems extended one refusal at a
time — as a ten-part series, starting here.
