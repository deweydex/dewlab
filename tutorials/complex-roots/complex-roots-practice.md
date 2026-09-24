---
title: "Complex numbers: roots that are not real — Practice"
practice_for: complex-roots
year: "2026-2027"
version: 2026.08.23.1
---

# Complex numbers: roots that are not real — Practice

Each answer is hidden until you open it. Try the question first.

The cell below has the solver and a checking function. The checking
function puts a root back into the quadratic. If the result is zero, the
number is a root. That check is more than a convenience: it is the proof.

## Tools

```python exec
id: tools-1
import cmath

def solve(a, b, c):
    discriminant = b ** 2 - 4 * a * c
    root = cmath.sqrt(discriminant)
    return ((-b + root) / (2 * a), (-b - root) / (2 * a))


def evaluate(a, b, c, x):
    return a * x ** 2 + b * x + c


for coefficients in [(1, 0, 1), (1, -5, 6), (1, 2, 5)]:
    a, b, c = coefficients
    first, second = solve(a, b, c)
    print(f"{a}x^2 + {b}x + {c}:  {first}  and  {second}")
    print(f"   substituted back: {evaluate(a, b, c, first)}  {evaluate(a, b, c, second)}")
```

## Arithmetic with i

**1.** Simplify $i^2$, $i^3$, $i^4$ and $i^5$.

<details class="dl-answer"><summary>answer</summary>

$-1$, $-i$, $1$ and $i$.

The powers repeat every four steps. This is because $i^4 = 1$, and
multiplying by 1 changes nothing. So $i^{100}$ is 1 and $i^{101}$ is $i$.

</details>

**2.** Work out $(3 + 2i) + (1 - 5i)$ and $(3 + 2i) - (1 - 5i)$.

<details class="dl-answer"><summary>answer</summary>

$4 - 3i$ and $2 + 7i$.

We combine real parts with real parts, and imaginary parts with
imaginary parts. This is the same as collecting like terms.

</details>

**3.** Work out $(3 + 2i)(1 - 4i)$.

<details class="dl-answer"><summary>answer</summary>

Multiplying out gives $3 - 12i + 2i - 8i^2$. The last term is
$-8 \times (-1) = +8$, so the answer is $11 - 10i$.

The $i^2$ turning into a real number is the only unusual step. That is
the definition $i^2 = -1$ doing its work.

</details>

**4.** Work out $(2 + 3i)(2 - 3i)$.

<details class="dl-answer"><summary>answer</summary>

$4 - 6i + 6i - 9i^2 = 4 + 9 = 13$.

A complex number multiplied by its conjugate always gives a real answer,
because the imaginary parts cancel. This is the trick for dividing
complex numbers: multiply the top and the bottom by the conjugate of the
bottom.

</details>

**5.** What is the conjugate of $5 - 7i$? Of $4$? Of $2i$?

<details class="dl-answer"><summary>answer</summary>

$5 + 7i$, $4$ and $-2i$.

A real number is its own conjugate, because it has no imaginary part to
change.

</details>

## Solving

**6.** Solve $x^2 + 4 = 0$.

<details class="dl-answer"><summary>answer</summary>

$x^2 = -4$, so $x = \pm 2i$.

</details>

**7.** Solve $x^2 - 2x + 5 = 0$.

<details class="dl-answer"><summary>answer</summary>

The discriminant is $4 - 20 = -16$, so its square root is
$\sqrt{-16} = 4i$.

$x = \dfrac{2 \pm 4i}{2} = 1 \pm 2i$.

</details>

**8.** Solve $x^2 + 6x + 13 = 0$.

<details class="dl-answer"><summary>answer</summary>

The discriminant is $36 - 52 = -16$.

$x = \dfrac{-6 \pm 4i}{2} = -3 \pm 2i$.

</details>

**9.** Check one of your answers by putting it back into the original
equation.

<details class="dl-answer"><summary>answer</summary>

Here is $x = 1 + 2i$ in $x^2 - 2x + 5$:

1. $(1 + 2i)^2 = 1 + 4i + 4i^2 = 1 + 4i - 4 = -3 + 4i$
2. $-2(1 + 2i) = -2 - 4i$
3. Adding everything: $-3 + 4i - 2 - 4i + 5 = 0$

**This substitution is the argument.** A root is a number that makes the
expression zero. This number makes it zero. So it is a root, however it
looks.

</details>

**10.** The equation $x^2 - 6x + 25 = 0$ has a root at $3 + 4i$. What is
the other root? How can you know without working it out?

<details class="dl-answer"><summary>answer</summary>

$3 - 4i$, the conjugate.

In a quadratic with real coefficients, the only place an $i$ can come
in is the square root of a negative discriminant. It appears once with a
$+$ and once with a $-$. So complex roots always come in conjugate
pairs.

</details>

## Understanding the discriminant

**11.** How many real roots does each quadratic have? Answer without
solving.

- (a) $x^2 - 7x + 12$
- (b) $x^2 + x + 1$
- (c) $4x^2 - 12x + 9$

<details class="dl-answer"><summary>answer</summary>

(a) The discriminant is $49 - 48 = 1$. It is positive, so there are two
real roots.

(b) The discriminant is $1 - 4 = -3$. It is negative, so there are no
real roots. There are two complex roots.

(c) The discriminant is $144 - 144 = 0$, so there is one repeated real
root, at 1.5.

</details>

**12.** What does a negative discriminant look like on a graph?

<details class="dl-answer"><summary>answer</summary>

The parabola misses the horizontal axis completely. It sits all above
the axis, or all below it.

The roots still exist, but they are not on the real number line. "No
real solutions" tells us which numbers we are willing to use.

</details>

**13.** Can a quadratic with real coefficients have exactly one complex
root and one real root?

<details class="dl-answer"><summary>answer</summary>

No. Complex roots come in conjugate pairs, so either both roots are real
or both are complex.

The picture says the same thing. A parabola crosses the axis twice,
touches it once, or misses it. No parabola crosses once and stops.

</details>

## Why complex numbers exist

**14.** Each new family of numbers was made because a question had no
answer. Match each family to the question that made it necessary:
$\mathbb{Z}$, $\mathbb{Q}$, $\mathbb{R}$, $\mathbb{C}$.

<details class="dl-answer"><summary>answer</summary>

- $\mathbb{Z}$: $3 - 5$. Subtracting can give an answer that is not a
  counting number.
- $\mathbb{Q}$: $3 \div 5$. Dividing can give an answer that is not an
  integer.
- $\mathbb{R}$: $\sqrt{2}$. A square root can give an answer that is not
  a fraction.
- $\mathbb{C}$: $\sqrt{-1}$. The square root of a negative number is not
  a real number.

Several of these were resisted when they were new, and all of them are
now taught in school.

</details>

**15.** Using complex numbers made the solver *shorter*. Why is that a
good sign?

<details class="dl-answer"><summary>answer</summary>

The `if discriminant < 0` special case disappeared. Two roots, one root
and no real roots turned out to be one situation. We see all of it once
we work in $\mathbb{C}$.

A new idea that removes special cases is usually the right one. An idea
that adds special cases is usually a patch.

</details>

**16.** Does every polynomial equation have a solution in $\mathbb{C}$?

<details class="dl-answer"><summary>answer</summary>

Yes, as long as it has degree 1 or more. This is the Fundamental Theorem
of Algebra. It is why $\mathbb{C}$ is the last family we need for
solving polynomial equations.

A polynomial of degree $n$ has exactly $n$ roots in $\mathbb{C}$, if we
count repeated roots. No statement like this is true in $\mathbb{R}$,
$\mathbb{Q}$, $\mathbb{Z}$ or $\mathbb{N}$.

</details>

## In use

**17.** Where are complex numbers used outside a maths class?

<details class="dl-answer"><summary>answer</summary>

- **Alternating current.** One complex number holds both the size and
  the timing of a signal.
- **Signal processing.** The Fourier transform is built on complex
  numbers.
- **Control systems.** Where the roots sit tells engineers whether a
  system is stable.
- **Computer graphics.** Quaternions, a larger relative of complex
  numbers, handle rotation without the problems that angles can cause.

In each of these, the complex numbers do real work. They are not
decoration.

</details>

**18.** A circuit's behaviour is described by $x^2 + 2x + 5 = 0$. If a
root has a negative real part, the circuit settles down. Does this one
settle?

<details class="dl-answer"><summary>answer</summary>

The roots are $-1 \pm 2i$, so the real part is $-1$. That is negative,
so the circuit settles.

The real part decides whether the oscillation grows or dies away. The
imaginary part gives how fast it oscillates. A positive real part would
mean the oscillation keeps growing. In a physical system, that can mean
something breaks.

</details>
