---
title: "When There Is No Answer"
slug: complex-roots
module: mit-pdp-maths-prog-integration
module_title: "Programming and Maths, Integrated"
year: "2026-2027"
series: algebra-and-functions
version: 2026.08.23.1
covers:
  the-cliff-edge:
    covers: [MIT-1.10]
  inventing-a-number:
    covers: [MIT-1.10]
    touches: [MIT-2.1]
  roots-that-are-not-real:
    covers: [MIT-1.10]
  they-come-in-pairs:
    covers: [MIT-1.10]
---

# When There Is No Answer

**Maths for IT**

In *Cracking Equations* you wrote a solver for quadratics. It computes the discriminant, and when that comes out negative it prints something like "no real solutions" and stops.

This tutorial is about what is on the other side of that stop.

It is a good story rather than a gap to be plugged quietly, because the answer was there the whole time and you were told it was not. And the way mathematicians got to it is the same move they had already made four times before -- which is the part worth having, more than the arithmetic.

## The Cliff Edge

Start with the simplest quadratic that fails.

```python exec
id: the-cliff-edge-1
import math

def solve(a, b, c):
    """The solver from Cracking Equations."""
    discriminant = b ** 2 - 4 * a * c
    if discriminant < 0:
        return "No real solutions."
    root = math.sqrt(discriminant)
    return ((-b + root) / (2 * a), (-b - root) / (2 * a))


print("x^2 - 5x + 6 = 0  ->", solve(1, -5, 6))
print("x^2 - 4x + 4 = 0  ->", solve(1, -4, 4))
print("x^2 + 1 = 0       ->", solve(1, 0, 1))
```

Three quadratics, three different kinds of answer. Two roots, one root, and a refusal.

Here is what the refusal looks like as a picture.

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

The third curve never comes down to the axis. That is what "no real solutions" looks like, and it is a completely accurate description of the situation -- as long as the only numbers you are willing to consider are the ones on that horizontal line.

**"No real solutions" is a true statement about the real numbers, and it is a smaller claim than it sounds.** It does not say there is no answer. It says there is no answer *on this line*.

## Inventing a Number

In *Numbers and Their Families* you took a tour of the number systems: the naturals ℕ, the integers ℤ, the rationals ℚ, and the reals ℝ. It is worth noticing what drove each step of that tour, because it is the same thing every time.

**ℕ** -- the counting numbers. You can add them. But `3 − 5` has no answer.

**ℤ** -- so negatives were invented, and now subtraction always works. But `3 ÷ 5` has no answer.

**ℚ** -- so fractions were invented, and now division always works. But `√2` has no answer.

**ℝ** -- so the irrationals were filled in, and now most things work. But `√−1` has no answer.

Each step is somebody refusing to accept "there is no answer" and inventing the number that makes it one. Every one of those inventions was resisted, and every one of them is now taught to children.

So the next step is not a special trick. It is the same move, one more time.

```python exec
id: inventing-a-number-1
# In Python, the imaginary unit is written 1j rather than i, because
# engineers already used i for current and the notation stuck.
i = 1j

print("i        =", i)
print("i squared =", i ** 2)
print("So the square root of -1 is:", i)
```

`i² = −1`. That is the whole definition. There is no more to it than that, and everything else follows.

A number with a real part and an imaginary part -- `3 + 2i` -- is a **complex number**, and the set of them is called **ℂ**. That is the fifth family, and it is the last one you will need: every polynomial equation has an answer in ℂ, which is not true of any of the four before it.

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

Notice `z * w`. Multiply it out by hand and you get `3 − 12i + 2i − 8i²`, and the last term is `−8 × (−1) = +8`. The `i²` collapsing back into a real number is the only unusual step, and it is the definition doing its work.

## Roots That Are Not Real

Now the solver again, with one line changed.

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

Look at what happened to the code, not just to the output. **The `if` is gone.** There is no special case any more, because there is no failure to handle. `cmath.sqrt` will take the square root of a negative number, so the same three lines answer all three questions.

That is a real thing about mathematics and not a fact about Python. Extending the number system removed a special case rather than adding one. The three separate situations -- two roots, one root, no roots -- turn out to be one situation looked at from a place where you can see all of it.

### Does it actually work?

A definition is only worth having if the answers it produces survive being checked. So check.

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

Every one comes back to zero, or to something like `(4.44e-16+0j)`, which is zero with floating-point dust on it.

**That is the argument.** A root is a number that makes the expression zero, these numbers make the expression zero, so these are roots. Nothing about the definition has to be taken on trust.

### Your turn

How would you solve these three by hand, in `a + bi` form, using the quadratic formula? Check each one with the solver.

- `x² + 4 = 0`
- `x² − 2x + 5 = 0`
- `x² + 6x + 13 = 0`

```python exec
id: your-turn-1
# Your answers, then the check.
# print(solve(1, 0, 4))
```

## They Come in Pairs

Look back at those printed roots and something should stand out before it is named.

```python exec
id: they-come-in-pairs-1
for coefficients in [(1, 0, 1), (1, 2, 5), (1, 6, 13), (1, -2, 10)]:
    a, b, c = coefficients
    first, second = solve(a, b, c)
    print(f"{first}   and   {second}")
```

Every pair has the same real part and opposite imaginary parts. `2 + 3i` comes with `2 − 3i`, always. Those two are called **conjugates**, and for a quadratic with ordinary real coefficients the complex roots always arrive as a conjugate pair.

The reason is visible in the formula. The only place an `i` can enter is the `√` of a negative discriminant, and it enters once with a `+` and once with a `−` in front of it. Nothing else in the formula can produce one.

And the picture says the same thing. A parabola crosses the axis twice, touches it once, or misses it -- there is no shape it can be that crosses once and stops. So the roots come two at a time, and if one of them has left the real line the other must have gone with it.

### Your turn

Without computing anything: `x² − 6x + 25 = 0` has a root at `3 + 4i`. What is the other one, and how do you know?

```python exec
id: your-turn-2
# Your answer as a comment, then check it.
# print(solve(1, -6, 25))
```

## Reflection

The stopping point in *Cracking Equations* was honest and it was not the end. "No real solutions" is a statement about which numbers you are willing to use, and there is a larger set where the answer has been waiting.

Three things to take.

**Every extension of the number system was invented for the same reason** -- somebody refused to accept that a perfectly reasonable question had no answer. ℂ is the fifth and last of those, and it is where every polynomial equation finally has a solution.

**Extending the numbers removed a special case.** The solver got shorter, not longer. That is often the sign that a generalisation is the right one.

**You can check an answer you do not fully believe.** Put the root back into the equation. If it gives zero, it is a root, whatever it looks like.

In a few sentences, before this tutorial, what did you think "no solution" meant? Has that changed?

## Where to Read More

Stephen Welch (Welch Labs) (2015). *Imaginary Numbers Are Real
[Part 1: Introduction].* <https://www.youtube.com/watch?v=T647CGsuOVU>.
The same story this page tells — number systems extended one refusal at a
time — as a ten-part series, starting here.
