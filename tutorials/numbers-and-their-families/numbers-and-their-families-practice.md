---
title: "Number types, powers and logarithms — Practice"
practice_for: numbers-and-their-families
year: "2026-2027"
version: 2026.09.26.1
worlds:
  music: Notes, octaves and the frequencies that make them.
  rockets: Rockets, orbits and the planets they travel between.
  fantasy-maps: A made-up kingdom, drawn to scale on a map.
---

# Number types, powers and logarithms — Practice

The answers are hidden in folds under each problem. You remember the
rules for powers best when you use them, so try the working by hand
first. Then use the cells to check your answers.

Some of these problems are adapted from an earlier set of worksheets on
fractions and exponents.

## Fractions

```python exec
id: fractions-1
from fractions import Fraction

print(Fraction(3, 4) + Fraction(5, 6))
print(Fraction(7, 8) - Fraction(2, 3))
print(Fraction(4, 5) / Fraction(2, 15))
```

**1.** Calculate each one exactly, as a fraction.

- (a) $\frac{3}{4} + \frac{5}{6}$
- (b) $\frac{7}{8} - \frac{2}{3}$
- (c) $\frac{5}{9} \times \frac{3}{10}$
- (d) $\frac{4}{5} \div \frac{2}{15}$

<details class="dl-answer"><summary>answer</summary>

(a) $\frac{19}{12}$. (b) $\frac{5}{24}$. (c) $\frac{1}{6}$. (d) 6.

To divide by a fraction, we multiply by its reciprocal (the fraction
turned upside down). That is why (d) is a whole number:
$\frac{4}{5} \times \frac{15}{2} = \frac{60}{10} = 6$.

</details>

**2.** Calculate $\frac{2}{3} + \frac{1}{4} - \frac{1}{6}$.

<details class="dl-answer"><summary>answer</summary>

It is $\frac{3}{4}$.

Write every fraction in twelfths:
$\frac{8}{12} + \frac{3}{12} - \frac{2}{12} = \frac{9}{12} = \frac{3}{4}$.

</details>

**3.** Calculate $\frac{5!}{4!}$ and $\frac{7!}{5! \cdot 2!}$.

<details class="dl-answer"><summary>answer</summary>

They are 5 and 21.

You do not need to calculate the factorials in full. In $\frac{5!}{4!}$,
everything below 5 cancels, and 5 is left. The second one cancels to
$\frac{7 \times 6}{2} = 21$. It is also the number of ways to choose 2
things from 7, which you met in
[Counting: factorials, permutations and combinations](tutorial:counting-carefully).

</details>

**4.** Calculate $1 + \frac{1}{2} + \frac{1}{4} + \frac{1}{8} + \frac{1}{16}$.
What does the total get close to if you keep going?

<details class="dl-answer"><summary>answer</summary>

It is $\frac{31}{16}$, which is 1.9375. The total gets closer and closer to 2,
but never reaches it.

Each new term closes half of the gap that is left. After $n$ terms you
are $\frac{1}{2^{n-1}}$ short of 2: after the five terms here, the gap is
$\frac{1}{16}$. That gap shrinks towards zero, but it is
never zero. The value the total gets close to is called a limit, and
[Limits: getting closer without arriving](tutorial:approaching-a-limit)
is all about them. This has the same shape as Zeno's paradox about
crossing a room.

</details>

**5.** Calculate $\frac{1}{1 \cdot 2} + \frac{1}{2 \cdot 3} + \frac{1}{3 \cdot 4} + \frac{1}{4 \cdot 5}$.
Can you see a pattern?

<details class="dl-answer"><summary>answer</summary>

It is $\frac{4}{5}$.

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

1. When we square both sides, we get $2 = \frac{a^2}{b^2}$, so $a^2 = 2b^2$.
2. So $a^2$ is even. That means $a$ is even too, because an odd number
   squared is odd.
3. Write $a = 2k$. Then $4k^2 = 2b^2$, so $b^2 = 2k^2$. So $b^2$ is
   even, and $b$ is even too.

But we said the fraction was in lowest terms. If $a$ and $b$ are both
even, it is not. This is a contradiction, so no such fraction exists.

This is one of the oldest proofs we know. It is short enough to rebuild
from the idea, without memorising it. Notice what it tells us. No
fraction is equal to √2. It does not give us any way to calculate √2.

</details>

**8.** Is 0.999… equal to 1?

<details class="dl-answer"><summary>answer</summary>

Yes, exactly. It is not approximately equal, and it is not "close
enough".

The quickest argument starts from $\frac{1}{3} = 0.333\ldots$ Multiply
both sides by 3, and you get $1 = 0.999\ldots$ The careful argument says
that the difference between them is never negative, and it is smaller
than every positive number. The only number like that is zero.

Many people find this hard to accept at first, because 0.999… looks
like a process that keeps going. It is a single number, and both
arguments above show which one.

</details>

**9.** The tutorial showed that Python stores `0.1` as a fraction with
$2^{55}$ on the bottom. The cell asks for five decimals as fractions.

```python exec
id: stored-exactly
from fractions import Fraction

for value in [0.5, 0.1, 0.25, 0.2, 0.75]:
    print(value, Fraction(value))
```

```predict
type: choice

Before you run it: which of the five come out as the fraction you would
write by hand?

- All five
  - Each one is a short decimal, so each should be easy to store.
- 0.5, 0.25 and 0.75
- Only 0.5
  - One half is the simplest fraction there is.
- None of them
  - If 0.1 is not stored exactly, perhaps no decimal is.
```

<details class="dl-answer"><summary>answer</summary>

0.5, 0.25 and 0.75 come out as $\frac{1}{2}$, $\frac{1}{4}$ and
$\frac{3}{4}$. 0.1 and 0.2 do not.

A fraction with a power of 2 on the bottom has a binary decimal that
ends, in the same way that a fraction with a power of 10 on the bottom
has an ordinary decimal that ends. $\frac{1}{4}$ is 0.01 in binary.
$\frac{1}{10}$ has a 5 on the bottom as well as a 2, and in binary it
never ends, like $\frac{1}{3} = 0.333\ldots$ in decimal.

</details>

## Powers

```python exec
id: powers-1
a = 3
print(a**2 * a**3, a**5)
print((a**2)**3, a**6)
print(a**0, a**-2, 1 / a**2)
```

**10.** Simplify each one without a calculator.

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

**11.** Simplify $\dfrac{(a^3 b^2)^2}{a^2 b}$.

<details class="dl-answer"><summary>answer</summary>

$a^4 b^3$.

First the power of a power: $(a^3 b^2)^2 = a^6 b^4$. Then divide, one
base at a time: $a^{6-2} = a^4$ and $b^{4-1} = b^3$.

Check it with numbers. With $a = 2$ and $b = 3$, the top is
$(8 \times 9)^2 = 5184$ and the bottom is $4 \times 3 = 12$, so the
fraction is 432. And $2^4 \times 3^3 = 16 \times 27 = 432$.

</details>

**12.** Calculate $16^{1/2}$, $27^{1/3}$, $8^{2/3}$ and $16^{-1/2}$.

<details class="dl-answer"><summary>answer</summary>

They are 4, 3, 4 and $\frac{1}{4}$.

A fractional power is a root. The bottom of the fraction says which
root, and the top says what power to raise it to. So $8^{2/3}$ is the
cube root of 8, squared: $2^2 = 4$. You can also do it in the other
order (square 8 to get 64, then take the cube root). You get the same
answer, but the numbers along the way are bigger.

</details>

**13.** Here is a power of a power, with no brackets.

```python exec
id: power-of-a-power
print(2 ** 3 ** 2)
```

```predict
type: number

What will it print?
```

<details class="dl-answer"><summary>answer</summary>

It prints 512.

Python reads a chain of powers from the right, so `2 ** 3 ** 2` means
$2^{(3^2)} = 2^9 = 512$. If it worked from the left, it would be
$(2^3)^2 = 2^6 = 64$. Mathematics reads a tower of powers the same way
as Python: $2^{3^2}$ is $2^9$. When you mean $(2^3)^2$, write the
brackets.

</details>

**14.** Here is the `power` function from the tutorial. What happens
when you ask it for `power(2, 0.5)`? Why?

```python exec
id: power-with-a-fraction
def power(base, exponent):
    """base to a whole-number exponent, without using **."""
    if exponent == 0:
        return 1
    if exponent < 0:
        return 1 / power(base, -exponent)
    result = 1
    for _ in range(exponent):
        result = result * base
    return result


print(power(2, 0.5))
```

<details class="dl-answer"><summary>answer</summary>

It stops with `TypeError: 'float' object cannot be interpreted as an
integer`.

The loop runs `range(exponent)` times, and `range` needs a whole number.
"Multiply by the base half a time" has no meaning, so repeated
multiplication cannot make a square root. That is why $a^{1/2}$ needs
the power-of-a-power rule to give it a meaning. Python's `**` uses a
different method, based on logarithms, so `2 ** 0.5` works.

</details>

**15.** How many multiplications does that function do for
`power(2, 1000)`? Can it be done with fewer?

<details class="dl-answer"><summary>answer</summary>

It does a thousand. It can be done with far fewer, about ten
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
instead of on a list. It makes public-key cryptography possible.

</details>

## Logarithms

**16.** Calculate each one without a calculator.

- (a) $\log_2 8$
- (b) $\log_{10} 1000$
- (c) $\log_2 1024$
- (d) $\log_5 1$
- (e) $\log_3 \frac{1}{9}$

<details class="dl-answer"><summary>answer</summary>

They are 3, 3, 10, 0 and −2.

A logarithm asks "what power gives me this number?". The log of 1 is
always 0, because any base to the power 0 is 1. A log is negative
exactly when the number is below 1: $3^{-2} = \frac{1}{9}$.

</details>

**17.** Why is $\log(ab) = \log a + \log b$?

<details class="dl-answer"><summary>answer</summary>

It is true because we add exponents when we multiply powers, and a logarithm *is* an
exponent.

Say $a = 10^x$ and $b = 10^y$. Then $ab = 10^{x+y}$, so the log of the
product is $x + y$. That is all the rule says.

For three hundred years, this rule turned multiplication into addition,
and it was the fastest way to do large calculations. A slide rule is
this rule built into a ruler.

</details>

**18.** Here is the `log_base` function from the tutorial. What does
it return for `log_base(0.25, 2)`? What should the answer be? Can you
change the function so that it works for numbers between 0 and 1 too?

```python exec
id: log-below-one
def log_base(x, base):
    """The whole-number part of the logarithm of x, for x >= 1."""
    count = 0
    while x >= base:
        x = x / base
        count = count + 1
    return count


print(log_base(0.25, 2))
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. $0.25 = \frac{1}{4} = 2^{-2}$. What is $\log_2 0.25$?
2. For a number below 1, dividing makes it smaller still. What could
   you do to it instead, to bring it up to 1?
3. Each time you do that, which way should `count` move?

**Think about:** for 0.3, the logarithm is about $-1.74$. Which whole
number should the function return: $-1$ or $-2$?

</details>

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Yours may be different and work too. It returns 0,
because $0.25 < 2$, so the loop never runs. The answer should be $-2$,
because $2^{-2} = \frac{1}{4}$.

```python
def log_base(x, base):
    """The whole number at or just below the logarithm of x, for x > 0."""
    count = 0
    while x < 1:
        x = x * base
        count = count - 1
    while x >= base:
        x = x / base
        count = count + 1
    return count
```

`log_base(0.25, 2)` is now $-2$, and `log_base(0.3, 2)` is also $-2$,
the whole number just below $-1.74$. For numbers of 1 or more, nothing
has changed.

</details>

**19.** Sound is measured in decibels (dB). A sound of 10 dB has ten
times the power of a sound of 0 dB. How much more powerful is 60 dB than
30 dB?

<details class="dl-answer"><summary>answer</summary>

It is a thousand times more powerful.

Every 10 dB is a factor of ten, and 60 − 30 is three steps of 10 dB. So
the factor is $10 \times 10 \times 10 = 1000$. Decibels use a
logarithmic scale so that a range of a trillion to one fits on a short
scale. The same idea gives the Richter scale for earthquakes and the
magnitude scale for the brightness of stars.

</details>

## Your world

**20.** A problem from the world you chose.

<div class="dl-world" data-world="music">

A *pure* fifth, the sound of two notes that fit together best, has
frequencies in the ratio $\frac{3}{2}$. A piano's fifth is seven
semitones, $2^{7/12}$. How close are they? Musicians measure small gaps
in *cents*, where one semitone is 100 cents, so a ratio $r$ is
$1200 \log_2 r$ cents.

```python exec
id: your-world--music
import math

pure = 3 / 2
piano = 2 ** (7 / 12)
```

<details class="dl-answer"><summary>answer</summary>

The piano's fifth is about 1.4983, a little below 1.5. The gap is
$1200 \log_2 \frac{1.5}{1.4983} \approx 1.96$ cents, about a fiftieth
of a semitone.

```python
print(piano, 1200 * math.log2(pure / piano))
```

Twelve pure fifths would overshoot seven octaves, so a piano cannot
have every fifth pure and every octave pure at once. Tuning every
semitone to $2^{1/12}$ shares the small error out equally. It is called
*equal temperament*.

</details>

</div>

<div class="dl-world" data-world="rockets">

Kepler's rule says years $= \text{distance}^{3/2}$. A mission planner
knows that Uranus takes about 84 years to go round the Sun, and Neptune
about 165. How far from the Sun is each, in AU? Which power undoes a
power of $\frac{3}{2}$?

```python exec
id: your-world--rockets
years = {"Uranus": 84, "Neptune": 165}
```

<details class="dl-answer"><summary>answer</summary>

Raise both sides to the power $\frac{2}{3}$:
$\text{distance} = \text{years}^{2/3}$, because
$(d^{3/2})^{2/3} = d^1$.

```python
for planet, time in years.items():
    print(planet, time ** (2 / 3))
```

Uranus is about 19.18 AU from the Sun and Neptune about 30.08 AU. The
measured mean distances are about 19.19 and 30.07 AU.

</details>

</div>

<div class="dl-world" data-world="fantasy-maps">

The kingdom's map is drawn at a scale of 1 : 50,000, so 1 cm on the map
is 50,000 cm on the ground. The King's Road is 7.2 cm long on the map.
How long is it in kilometres? A field is 4 cm² on the map. How many
km² is it?

```python exec
id: your-world--fantasy-maps
scale = 50_000
```

<details class="dl-answer"><summary>answer</summary>

The road is 3.6 km, and the field is 1 km².

$7.2 \times 50\,000 = 360\,000$ cm, which is 3.6 km. An area
multiplies by the scale squared: $4 \times 50\,000^2 = 10^{10}$ cm². A
km² is $100\,000^2 = 10^{10}$ cm², so the field is exactly 1 km².

```python
print(7.2 * scale / 100 / 1000, 4 * scale ** 2 / 100_000 ** 2)
```

</details>

</div>

## Formulas as functions

**21.** The tutorial wrote `circle_area`, `cylinder_volume` and
`sphere_volume`. Can you write `cone_volume(radius, height)` and
`sphere_surface_area(radius)`? A cone fits exactly inside a cylinder of
the same radius and height. What fraction of the cylinder does it fill?

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Yours may be different and work too.

```python
import math


def cone_volume(radius, height):
    """The volume of a cone: a third of the cylinder around it."""
    return math.pi * radius ** 2 * height / 3


def sphere_surface_area(radius):
    """The area of the outside of a sphere."""
    return 4 * math.pi * radius ** 2
```

A cone fills exactly a third of its cylinder. With radius 3 and height
12, the cone is about 113.1 and the cylinder about 339.3.

`sphere_surface_area(3)` is also about 113.1. That is a coincidence of
these numbers: for radius 3, $4\pi r^2 = 36\pi$, and the cone
$\frac{1}{3}\pi \times 9 \times 12$ is $36\pi$ too.

</details>

**22.** A model of a building is made at a scale of 1 : 10, so every
length is a tenth of the real one. The real building needs 400 litres
of paint for its walls. How much paint does the model need? The model
is solid clay, and the real building would fill 2,000 m³. How much clay
is the model?

<details class="dl-answer"><summary>answer</summary>

4 litres of paint, and 2 m³ of clay.

Paint covers an area, and an area scales by $\left(\frac{1}{10}\right)^2
= \frac{1}{100}$. Clay fills a volume, and a volume scales by
$\left(\frac{1}{10}\right)^3 = \frac{1}{1000}$. So the model needs a
hundredth of the paint and a thousandth of the clay.

</details>

**23.** Can you write a function that takes a number and reports which
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
the check out, every number with a prime factor larger than its square
root loses that factor without any error. `factorise(12)` would give
`[2, 2]`, and `factorise(97)` would give `[]`.

</details>

## From earlier

**24.** A binary search on a million items takes about twenty steps. How
many steps does it take on a billion items?

<details class="dl-answer"><summary>answer</summary>

It takes about thirty.

$\log_2(10^9) \approx 30$. If you multiply the data by a thousand, you add
only ten steps, because a thousand is about $2^{10}$. In practice, a
logarithm counts doublings.

</details>

**25.** In [Probability: simple, compound and
conditional](tutorial:what-are-the-chances) we found the chance of an event
by counting. The `fractions` module keeps a chance exact. What is the
chance of rolling two sixes with two fair dice? And the chance of at
least one six?

```python exec
id: from-earlier-chances
from fractions import Fraction

six = Fraction(1, 6)
```

<details class="dl-answer"><summary>answer</summary>

Two sixes: $\frac{1}{36}$. At least one six: $\frac{11}{36}$.

The two dice do not affect each other, so the chances multiply:
`six * six` is `Fraction(1, 36)`. For at least one six, it is easier to
count the other way. The chance of no six is
$\left(\frac{5}{6}\right)^2 = \frac{25}{36}$, so the chance of at
least one is $1 - \frac{25}{36} = \frac{11}{36}$. `1 - (1 - six) ** 2`
gives `Fraction(11, 36)`, with no rounding anywhere.

</details>
