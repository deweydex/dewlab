---
title: "Numbers and Their Families — Practice"
slug: numbers-and-their-families-practice
practice_for: numbers-and-their-families
module: mit-pdp-maths-prog-integration
module_title: "Programming and Maths, Integrated"
year: "2026-2027"
series: algebra-and-functions
version: 2026.08.23.1
---

# Numbers and Their Families — Practice

Answers are folded. The index laws reward being *used* rather than memorised, so do the manipulations by hand and let the cells settle the arguments.

Some of these are adapted from the fractions and exponents worksheets in the Mathematics repository.

## Fractions

```python exec
id: fractions-1
from fractions import Fraction

print(Fraction(3, 4) + Fraction(5, 6))
print(Fraction(7, 8) - Fraction(2, 3))
print(Fraction(4, 5) / Fraction(2, 15))
```

**1.** Evaluate exactly.

- (a) $\frac{3}{4} + \frac{5}{6}$
- (b) $\frac{7}{8} - \frac{2}{3}$
- (c) $\frac{5}{9} \times \frac{3}{10}$
- (d) $\frac{4}{5} \div \frac{2}{15}$

<details class="dl-answer"><summary>answer</summary>

(a) $\frac{19}{12}$. (b) $\frac{5}{24}$. (c) $\frac{1}{6}$. (d) 6.

Dividing by a fraction multiplies by its reciprocal, which is why (d) comes out a whole number: $\frac{4}{5} \times \frac{15}{2} = \frac{60}{10}$.

</details>

**2.** Evaluate $\frac{2}{3} + \frac{1}{4} - \frac{1}{6}$.

<details class="dl-answer"><summary>answer</summary>

$\frac{3}{4}$.

Over twelfths: $\frac{8}{12} + \frac{3}{12} - \frac{2}{12} = \frac{9}{12}$.

</details>

**3.** Evaluate $\frac{5!}{4!}$ and $\frac{7!}{5! \cdot 2!}$.

<details class="dl-answer"><summary>answer</summary>

5 and 21.

Neither needs the factorials worked out. $\frac{5!}{4!}$ cancels everything below 5. The second is $\frac{7 \times 6}{2}$, and it is the number of ways to choose 2 things from 7 — which is where *Counting Carefully* picks this up.

</details>

**4.** Evaluate $1 + \frac{1}{2} + \frac{1}{4} + \frac{1}{8} + \frac{1}{16}$. What does this approach if you keep going?

<details class="dl-answer"><summary>answer</summary>

$\frac{31}{16}$, which is 1.9375. It approaches 2 and never reaches it.

Each term halves the remaining gap. After n terms you are $\frac{1}{2^n}$ short, which goes to zero but is never zero. This is a limit, and it is the same shape as Zeno's paradox about crossing a room.

</details>

**5.** Evaluate $\frac{1}{1 \cdot 2} + \frac{1}{2 \cdot 3} + \frac{1}{3 \cdot 4} + \frac{1}{4 \cdot 5}$. What is the pattern?

<details class="dl-answer"><summary>answer</summary>

$\frac{4}{5}$.

Each term splits: $\frac{1}{n(n+1)} = \frac{1}{n} - \frac{1}{n+1}$. Written that way the sum is

$$\left(1 - \tfrac12\right) + \left(\tfrac12 - \tfrac13\right) + \left(\tfrac13 - \tfrac14\right) + \left(\tfrac14 - \tfrac15\right)$$

and everything cancels except the first and last, leaving $1 - \frac{1}{5}$. Sums that collapse like this are called telescoping, and the infinite version comes to exactly 1.

</details>

## Number Domains

**6.** Which families does each belong to — natural, integer, rational, real?

`7`, `-3`, `0`, `2/3`, `√2`, `-1.5`, `π`

<details class="dl-answer"><summary>answer</summary>

7: all four. −3: integer, rational, real. 0: natural (by the convention this course uses), integer, rational, real. 2/3 and −1.5: rational and real. √2 and π: real only.

The families nest. Every natural number is an integer, every integer is rational, every rational is real — so naming the smallest family it belongs to says everything.

</details>

**7.** Prove that √2 is not rational.

<details class="dl-answer"><summary>answer</summary>

Suppose it were, written as $\frac{a}{b}$ in lowest terms. Then $a^2 = 2b^2$, so $a^2$ is even, so $a$ is even — an odd number squared is odd. Write $a = 2k$: then $4k^2 = 2b^2$, so $b^2 = 2k^2$, so $b$ is even too.

But we said lowest terms, and both being even contradicts that. So no such fraction exists.

This is one of the oldest proofs there is, and it is short enough to reconstruct rather than remember. What it does *not* give you is any way to compute √2 — it only says no fraction is it.

</details>

**8.** Is 0.999… equal to 1?

<details class="dl-answer"><summary>answer</summary>

Yes, exactly — not approximately, not "close enough".

The quickest argument: $\frac{1}{3} = 0.333\ldots$, so three times each side gives $1 = 0.999\ldots$. The careful argument is that the difference between them is smaller than every positive number, and the only such number is zero.

The discomfort people feel here is real and worth naming: it comes from thinking of 0.999… as a process that keeps going rather than as a single number.

</details>

## Powers

```python exec
id: powers-1
a = 3
print(a**2 * a**3, a**5)
print((a**2)**3, a**6)
print(a**0, a**-2, 1 / a**2)
```

**9.** Simplify without a calculator.

- (a) $2^3 \times 2^4$
- (b) $(5^2)^3$
- (c) $\frac{7^8}{7^5}$
- (d) $3^{-2}$
- (e) $(2^3)^0$

<details class="dl-answer"><summary>answer</summary>

(a) $2^7 = 128$. (b) $5^6 = 15625$. (c) $7^3 = 343$. (d) $\frac{1}{9}$. (e) 1.

Same base multiplied means add the exponents; a power of a power means multiply them; dividing means subtract.

</details>

**10.** Why is $a^0 = 1$?

<details class="dl-answer"><summary>answer</summary>

Because $\frac{a^n}{a^n} = a^{n-n} = a^0$, and any number divided by itself is 1.

It is not a special rule bolted on. It is the only value that keeps the subtraction rule working, which is the same reason $a^{-n}$ has to be $\frac{1}{a^n}$: continue the pattern downwards and each step divides by $a$.

$0^0$ is the genuinely unsettled case, and different fields answer it differently. Python says 1.

</details>

**11.** Evaluate $16^{1/2}$, $27^{1/3}$, $8^{2/3}$, $16^{-1/2}$.

<details class="dl-answer"><summary>answer</summary>

4, 3, 4, $\frac{1}{4}$.

A fractional power is a root: the bottom of the fraction says which root, the top says what power to raise it to. $8^{2/3}$ is the cube root of 8, squared — 2² = 4. Doing it the other way (64 then cube root) gives the same answer and larger numbers.

</details>

**12.** Write `power(base, exponent)` without using `**`, handling negative and zero exponents.

<details class="dl-answer"><summary>answer</summary>

```python
def power(base, exponent):
    """base raised to a whole-number exponent, without **."""
    if exponent == 0:
        return 1
    if exponent < 0:
        return 1 / power(base, -exponent)
    result = 1
    for _ in range(exponent):
        result = result * base
    return result
```

`power(2, 10)` is 1024, `power(3, 0)` is 1, `power(2, -3)` is 0.125.

The negative case calling itself is the neat part: it turns a case it cannot do into one it can.

</details>

**13.** How many multiplications does that do for `power(2, 1000)`? Can it be done in fewer?

<details class="dl-answer"><summary>answer</summary>

A thousand, and yes — about ten.

Square repeatedly instead: $a^{1000} = (a^{500})^2$, and $a^{500} = (a^{250})^2$, and so on. Halving the exponent each time means log₂(1000) ≈ 10 squarings.

```python
def fast_power(base, exponent):
    if exponent == 0:
        return 1
    half = fast_power(base, exponent // 2)
    if exponent % 2 == 0:
        return half * half
    return half * half * base
```

This is exactly binary search's halving, applied to arithmetic instead of to a list, and it is what makes public-key cryptography possible at all.

</details>

## Logarithms

**14.** Evaluate without a calculator.

- (a) $\log_2 8$
- (b) $\log_{10} 1000$
- (c) $\log_2 1024$
- (d) $\log_5 1$
- (e) $\log_3 \frac{1}{9}$

<details class="dl-answer"><summary>answer</summary>

3, 3, 10, 0, −2.

A logarithm asks "what power gives me this?". The log of 1 is always 0 because anything to the power 0 is 1, and a log is negative exactly when its argument is below 1.

</details>

**15.** Why is $\log(ab) = \log a + \log b$?

<details class="dl-answer"><summary>answer</summary>

Because multiplying powers adds their exponents, and a logarithm *is* an exponent.

If $a = 10^x$ and $b = 10^y$ then $ab = 10^{x+y}$, so the log of the product is $x + y$. That is the whole content of the rule.

For three hundred years this turned multiplication into addition and was the fastest way to do arithmetic — slide rules are this identity carved into wood.

</details>

**16.** Write `log_base(x, base)` returning the integer part, by repeated division.

<details class="dl-answer"><summary>answer</summary>

```python
def log_base(x, base):
    """The integer part of log(x) to the given base, for x >= 1."""
    count = 0
    while x >= base:
        x = x / base
        count = count + 1
    return count
```

`log_base(1024, 2)` is 10, `log_base(1000, 10)` is 3, `log_base(100, 3)` is 4 since 3⁴ = 81 and 3⁵ = 243.

Dividing until you fall below the base is the definition read backwards, and for algorithm analysis the integer part is all anybody uses.

</details>

**17.** A binary search on a million items takes about twenty steps. On a billion?

<details class="dl-answer"><summary>answer</summary>

About thirty.

$\log_2(10^9) \approx 30$. Multiplying the data by a thousand adds ten steps, because a thousand is roughly 2¹⁰. That is the practical meaning of a logarithm: it counts doublings.

</details>

**18.** Sound is measured in decibels, where 10 dB is ten times the power of 0 dB. How much more powerful is 60 dB than 30 dB?

<details class="dl-answer"><summary>answer</summary>

A thousand times.

Every 10 dB is a factor of ten, and 60 − 30 is three of those. Decibels are a logarithmic scale precisely so that a range of a trillion to one fits on a ruler — and the same reasoning gives the Richter scale and stellar magnitudes.

</details>

## Geometry as Functions

**19.** Write functions for the area of a circle, the area of a triangle from base and height, and the volume of a cylinder.

<details class="dl-answer"><summary>answer</summary>

```python
import math


def circle_area(radius):
    """Area of a circle."""
    return math.pi * radius ** 2


def triangle_area(base, height):
    """Area of a triangle from its base and perpendicular height."""
    return base * height / 2


def cylinder_volume(radius, height):
    """Volume of a cylinder."""
    return circle_area(radius) * height
```

The last one calling the first is worth doing deliberately. A cylinder is a circle with depth, and writing $\pi r^2 h$ out again would hide that.

</details>

**20.** A circle's radius doubles. What happens to its circumference and its area?

<details class="dl-answer"><summary>answer</summary>

The circumference doubles; the area quadruples.

Circumference is linear in r, area is quadratic. This is why a pizza twice the diameter is four times the pizza, and why doubling the resolution of an image costs four times the memory.

</details>

**21.** Write a function that takes a number and reports which families it belongs to, whether it is prime, and its prime factors.

<details class="dl-answer"><summary>answer</summary>

```python
def factorise(n):
    """The prime factors of a positive whole number, with repeats."""
    factors, d = [], 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n = n // d
        d = d + 1
    if n > 1:
        factors.append(n)
    return factors
```

`factorise(360)` gives `[2, 2, 2, 3, 3, 5]`, and `factorise(97)` gives `[97]` — a number is prime exactly when its factorisation is itself.

The `if n > 1` at the end catches the last prime factor, which is larger than the square root and so never reached by the loop. Leaving it out silently drops a factor from every number with a large prime in it, which is a bug that passes most casual testing.

</details>
