---
title: "Number types, powers and logarithms — Practice"
practice_for: numbers-and-their-families
year: "2026-2027"
version: 2026.08.23.1
---

# Number types, powers and logarithms — Practice

The answers are hidden in folds under each problem. The rules for powers
stick best when you use them, so try the working by hand first. Then use
the cells to check your answers.

Some of these problems are adapted from the fractions and exponents
worksheets in the Mathematics repository.

## Fractions

```python exec
id: fractions-1
from fractions import Fraction

print(Fraction(3, 4) + Fraction(5, 6))
print(Fraction(7, 8) - Fraction(2, 3))
print(Fraction(4, 5) / Fraction(2, 15))
```

**1.** Work out each one exactly, as a fraction.

- (a) $\frac{3}{4} + \frac{5}{6}$
- (b) $\frac{7}{8} - \frac{2}{3}$
- (c) $\frac{5}{9} \times \frac{3}{10}$
- (d) $\frac{4}{5} \div \frac{2}{15}$

<details class="dl-answer"><summary>answer</summary>

(a) $\frac{19}{12}$. (b) $\frac{5}{24}$. (c) $\frac{1}{6}$. (d) 6.

To divide by a fraction, we multiply by its reciprocal (the fraction
turned upside down). That is why (d) comes out as a whole number:
$\frac{4}{5} \times \frac{15}{2} = \frac{60}{10} = 6$.

</details>

**2.** Work out $\frac{2}{3} + \frac{1}{4} - \frac{1}{6}$.

<details class="dl-answer"><summary>answer</summary>

$\frac{3}{4}$.

Write every fraction in twelfths:
$\frac{8}{12} + \frac{3}{12} - \frac{2}{12} = \frac{9}{12} = \frac{3}{4}$.

</details>

**3.** Work out $\frac{5!}{4!}$ and $\frac{7!}{5! \cdot 2!}$.

<details class="dl-answer"><summary>answer</summary>

5 and 21.

You do not need to work out the factorials in full. In $\frac{5!}{4!}$,
everything below 5 cancels, and 5 is left. The second one cancels to
$\frac{7 \times 6}{2} = 21$. It is also the number of ways to choose 2
things from 7, which you met in
[Counting: factorials, permutations and combinations](tutorial:counting-carefully).

</details>

**4.** Work out $1 + \frac{1}{2} + \frac{1}{4} + \frac{1}{8} + \frac{1}{16}$.
What does the total get close to if you keep going?

<details class="dl-answer"><summary>answer</summary>

$\frac{31}{16}$, which is 1.9375. The total gets closer and closer to 2,
but never reaches it.

Each new term closes half of the gap that is left. After $n$ terms you
are $\frac{1}{2^n}$ short of 2. That gap shrinks towards zero, but it is
never zero. The value the total gets close to is called a limit, and
[Limits: getting closer without arriving](tutorial:approaching-a-limit)
is all about them. This has the same shape as Zeno's paradox about
crossing a room.

</details>

**5.** Work out $\frac{1}{1 \cdot 2} + \frac{1}{2 \cdot 3} + \frac{1}{3 \cdot 4} + \frac{1}{4 \cdot 5}$.
Can you see a pattern?

<details class="dl-answer"><summary>answer</summary>

$\frac{4}{5}$.

Each term splits into two: $\frac{1}{n(n+1)} = \frac{1}{n} - \frac{1}{n+1}$.
Written that way, the sum is

$$\left(1 - \tfrac12\right) + \left(\tfrac12 - \tfrac13\right) + \left(\tfrac13 - \tfrac14\right) + \left(\tfrac14 - \tfrac15\right)$$

Everything cancels except the first and last numbers, which leaves
$1 - \frac{1}{5}$. A sum that collapses like this is called a
telescoping sum. If the sum keeps going forever, the total is exactly 1.

</details>

## Number domains

**6.** Which families does each number belong to: natural, integer,
rational, real?

`7`, `-3`, `0`, `2/3`, `√2`, `-1.5`, `π`

<details class="dl-answer"><summary>answer</summary>

- 7: all four.
- −3: integer, rational, real.
- 0: natural (with the convention this course uses), integer, rational,
  real.
- 2/3 and −1.5: rational and real.
- √2 and π: real only.

The families sit one inside the next. Every natural number is an
integer, every integer is rational, and every rational number is real.
So once you name the smallest family a number belongs to, you know all
the others.

</details>

**7.** Can you prove that √2 is not rational?

<details class="dl-answer"><summary>answer</summary>

Suppose that √2 is rational. Then we can write it as $\frac{a}{b}$ in
lowest terms, where $a$ and $b$ are integers.

1. Squaring both sides gives $2 = \frac{a^2}{b^2}$, so $a^2 = 2b^2$.
2. So $a^2$ is even. That means $a$ is even too, because an odd number
   squared is odd.
3. Write $a = 2k$. Then $4k^2 = 2b^2$, so $b^2 = 2k^2$. So $b^2$ is
   even, and $b$ is even too.

But we said the fraction was in lowest terms. If $a$ and $b$ are both
even, it is not. This is a contradiction, so no such fraction exists.

This is one of the oldest proofs we know. It is short enough to rebuild
from the idea, without memorising it. Notice what it tells us: no
fraction is equal to √2. It does not give us any way to calculate √2.

</details>

**8.** Is 0.999… equal to 1?

<details class="dl-answer"><summary>answer</summary>

Yes, exactly. It is not approximately equal, and it is not "close
enough".

The quickest argument: $\frac{1}{3} = 0.333\ldots$ Multiply both sides by
3, and you get $1 = 0.999\ldots$ The careful argument: the difference
between them is never negative, and it is smaller than every positive
number. The only number like that is zero.

Many people find this uncomfortable, and that feeling is worth naming. It
comes from thinking of 0.999… as a process that keeps going. It is a
single number.

</details>

## Powers

```python exec
id: powers-1
a = 3
print(a**2 * a**3, a**5)
print((a**2)**3, a**6)
print(a**0, a**-2, 1 / a**2)
```

**9.** Simplify each one without a calculator.

- (a) $2^3 \times 2^4$
- (b) $(5^2)^3$
- (c) $\frac{7^8}{7^5}$
- (d) $3^{-2}$
- (e) $(2^3)^0$

<details class="dl-answer"><summary>answer</summary>

(a) $2^7 = 128$. (b) $5^6 = 15625$. (c) $7^3 = 343$. (d) $\frac{1}{9}$. (e) 1.

| When you… | you… |
|---|---|
| multiply powers of the same base | add the exponents |
| take a power of a power | multiply the exponents |
| divide powers of the same base | subtract the exponents |

</details>

**10.** Why is $a^0 = 1$?

<details class="dl-answer"><summary>answer</summary>

Because $\frac{a^n}{a^n} = a^{n-n} = a^0$, and any number (except 0)
divided by itself is 1.

So $a^0 = 1$ is not an extra rule added on. It is the only value that
keeps the subtraction rule working. The same reason explains why
$a^{-n}$ has to be $\frac{1}{a^n}$. Follow the pattern downwards,
$a^3, a^2, a^1, a^0, a^{-1}$, and each step divides by $a$.

$0^0$ is the one case people disagree on, and different areas of
mathematics answer it differently. Python says 1.

</details>

**11.** Work out $16^{1/2}$, $27^{1/3}$, $8^{2/3}$ and $16^{-1/2}$.

<details class="dl-answer"><summary>answer</summary>

4, 3, 4, $\frac{1}{4}$.

A fractional power is a root. The bottom of the fraction says which
root, and the top says what power to raise it to. So $8^{2/3}$ is the
cube root of 8, squared: $2^2 = 4$. You can also do it in the other
order (square 8 to get 64, then take the cube root). You get the same
answer, but the numbers along the way are bigger.

</details>

**12.** Can you write `power(base, exponent)` without using `**`? It
should handle negative and zero exponents.

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

`power(2, 10)` is 1024, `power(3, 0)` is 1, and `power(2, -3)` is 0.125.

The neat part is the negative case, where the function calls itself. It
turns a case it cannot do into one it can.

</details>

**13.** How many multiplications does that function do for
`power(2, 1000)`? Can it be done with fewer?

<details class="dl-answer"><summary>answer</summary>

It does a thousand. And yes, it can be done with far fewer: about ten
squarings.

The trick is to square again and again: $a^{1000} = (a^{500})^2$, and
$a^{500} = (a^{250})^2$, and so on. Each step halves the exponent, so we
need about $\log_2(1000) \approx 10$ squarings. When the exponent is odd,
there is one extra multiplication by the base. For 1000, the function
below does 16 multiplications in total.

```python
def fast_power(base, exponent):
    if exponent == 0:
        return 1
    half = fast_power(base, exponent // 2)
    if exponent % 2 == 0:
        return half * half
    return half * half * base
```

This is the same halving idea as binary search, used on arithmetic
instead of on a list. It is what makes public-key cryptography possible.

</details>

## Logarithms

**14.** Work out each one without a calculator.

- (a) $\log_2 8$
- (b) $\log_{10} 1000$
- (c) $\log_2 1024$
- (d) $\log_5 1$
- (e) $\log_3 \frac{1}{9}$

<details class="dl-answer"><summary>answer</summary>

3, 3, 10, 0, −2.

A logarithm asks "what power gives me this number?". The log of 1 is
always 0, because any base to the power 0 is 1. A log is negative
exactly when the number is below 1: $3^{-2} = \frac{1}{9}$.

</details>

**15.** Why is $\log(ab) = \log a + \log b$?

<details class="dl-answer"><summary>answer</summary>

Because multiplying powers adds their exponents, and a logarithm *is* an
exponent.

Say $a = 10^x$ and $b = 10^y$. Then $ab = 10^{x+y}$, so the log of the
product is $x + y$. That is all the rule says.

For three hundred years, this rule turned multiplication into addition,
and it was the fastest way to do large calculations. A slide rule is
this rule built into a ruler.

</details>

**16.** Can you write `log_base(x, base)` so that it returns the
whole-number part of the logarithm, using repeated division?

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

`log_base(1024, 2)` is 10, `log_base(1000, 10)` is 3, and
`log_base(100, 3)` is 4, since $3^4 = 81$ and $3^5 = 243$.

Dividing until you fall below the base is the definition of a logarithm
read backwards. When we count the steps of an algorithm, the whole-number
part is all we use.

</details>

**17.** A binary search on a million items takes about twenty steps. How
many steps does it take on a billion items?

<details class="dl-answer"><summary>answer</summary>

About thirty.

$\log_2(10^9) \approx 30$. Multiplying the data by a thousand adds only
ten steps, because a thousand is about $2^{10}$. This is what a logarithm
means in practice: it counts doublings.

</details>

**18.** Sound is measured in decibels (dB). A sound of 10 dB has ten
times the power of a sound of 0 dB. How much more powerful is 60 dB than
30 dB?

<details class="dl-answer"><summary>answer</summary>

A thousand times.

Every 10 dB is a factor of ten, and 60 − 30 is three steps of 10 dB. So
the factor is $10 \times 10 \times 10 = 1000$. Decibels use a
logarithmic scale so that a range of a trillion to one fits on a short
scale. The same idea gives the Richter scale for earthquakes and the
magnitude scale for the brightness of stars.

</details>

## Geometry as functions

**19.** Can you write functions for the area of a circle, the area of a
triangle from its base and height, and the volume of a cylinder?

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

It is worth making the last function call the first one on purpose. A
cylinder is a circle with depth. Writing $\pi r^2 h$ out again would
hide that.

</details>

**20.** A circle's radius doubles. What happens to its circumference and
its area?

<details class="dl-answer"><summary>answer</summary>

The circumference doubles, and the area becomes four times as big.

The circumference is $2\pi r$, so it grows in step with $r$. The area is
$\pi r^2$, so it grows with $r$ squared, and $2^2 = 4$. This is why a
pizza twice as wide is four times as much pizza. It is also why doubling
the width and height of an image needs four times the memory.

</details>

**21.** Can you write a function that takes a number and reports which
families it belongs to, whether it is prime, and its prime factors?

<details class="dl-answer"><summary>answer</summary>

The families come from `classify_number` in the tutorial. The new part
is the prime factors. Once we have them, we can also tell whether the
number is prime:

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

A number is prime exactly when its list of factors holds only the number
itself. `factorise(360)` gives `[2, 2, 2, 3, 3, 5]`, and `factorise(97)`
gives `[97]`, so 97 is prime.

The `if n > 1` at the end catches the last prime factor. That factor is
larger than the square root, so the loop never reaches it. If you leave
the check out, every number with a large prime factor loses that factor
without any error. Most quick tests will not catch this bug.

</details>
