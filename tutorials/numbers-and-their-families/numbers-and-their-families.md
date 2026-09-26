---
title: "Number types, powers and logarithms"
year: "2026-2027"
version: 2026.09.26.1
covers:
  the-number-domains:
    covers: [MIT-2.1]
  powers-and-their-rules:
    covers: [MIT-1.1]
  logarithms-the-inverse-of-powers:
    covers: [MIT-1.1]
  formulas-as-functions:
    covers: [MIT-1.2, MIT-1.3]
worlds:
  music: Notes, octaves and the frequencies that make them.
  rockets: Rockets, orbits and the planets they travel between.
  fantasy-maps: A made-up kingdom, drawn to scale on a map.
---

# Number types, powers and logarithms

This page starts the pages on algebra and functions. We take the classic
tools of algebra, such as powers, formulas and equations, and build each
one as a program. We start with the numbers themselves.

In [Probability: simple, compound and conditional](tutorial:what-are-the-chances)
we used `Fraction` to keep a chance as an exact fraction. The cell asks
it for one tenth in two ways: first as the fraction 1 over 10, then from
the decimal `0.1`.

```python exec
id: opening-1
from fractions import Fraction

print(Fraction(1, 10))
print(Fraction(0.1))
```

```predict
type: choice

What will the second line print?

- 1/10
  - 0.1 and one tenth are the same number, so Python should store the
    same thing.
- A fraction, but not 1/10
- An error, because 0.1 is a decimal and not a fraction
  - A decimal and a fraction look like two kinds of number.
```

The second line prints `3602879701896397/36028797018963968`. That is a
fraction, but it is not one tenth. The number on the bottom is $2^{55}$.
A computer stores a decimal in binary, and in binary one tenth never
ends, in the same way that $\frac{1}{3} = 0.333\ldots$ never ends in
decimal. So Python keeps the nearest fraction with a power of 2 on the
bottom.

So every decimal Python stores is a fraction of two whole numbers. That
fact matters again later on this page. First we need names for the
families that numbers belong to.

## The number domains

You met the four number families in
[Making decisions with if, elif and else](tutorial:making-decisions).
Here they are again. Each family contains the one before it and adds
something new.

**N** (natural numbers): 0, 1, 2, 3, ... These are the counting numbers.
If you add two natural numbers, the answer is always a natural number.
Subtraction does not always work: $3 - 5 = -2$, and $-2$ is not a
natural number. (Some books start the natural numbers at 1. In this
course, 0 counts as a natural number.)

**Z** (integers): ..., −2, −1, 0, 1, 2, ... Now subtraction always works.
The letter Z comes from *Zahlen*, the German word for numbers.

**Q** (rationals): a rational number is any number we can write as
$\frac{p}{q}$, where $p$ and $q$ are integers and $q \neq 0$. For
example, $0.25 = \frac{1}{4}$. Now division works too, with one
exception: we still cannot divide by zero.

**R** (reals): the real numbers are all the points on the number line.
They include *irrational* numbers. An irrational number is a real number
that we cannot write as a fraction of two integers, such as $\sqrt{2}$
and $\pi$. The irrationals fill the gaps between the rationals.

Here is a word for what we have been describing. A family is *closed*
under an operation when that operation, used on two numbers from the
family, always gives an answer in the same family. So N is closed under
addition but not under subtraction, and Z is closed under subtraction.

| Family | Addition | Subtraction | Division (not by zero) |
|---|---|---|---|
| N | always works | not always | not always |
| Z | always works | always works | not always |
| Q | always works | always works | always works |
| R | always works | always works | always works |

Every natural number is an integer. Every integer is a rational number.
We can put it over 1, so $7 = \frac{7}{1}$. Every rational number is a
real number. The families sit one inside the next, like Russian dolls:
$\mathbb{N} \subset \mathbb{Z} \subset \mathbb{Q} \subset \mathbb{R}$.
The symbol $\subset$ means "is inside" (you met it as "is a subset of"
in [Sets: building them from sorted lists](tutorial:sets-as-sorted-lists)).

![Four rings, one inside the next. Naturals 0, 1, 2, 3 innermost, then
integers with −5 and −1, then rationals with 2/3, 0.25 and −1.5, then reals
with root 2 and pi outermost.](number-domains.svg)

In the picture, each number sits in the ring of the smallest family it
belongs to. To find all the families a number is in, find the number and
read outwards. For example, $-5$ is in the integers ring. So it is an
integer, a rational and a real. It is not a natural number, because it
is outside that ring.

### Your turn

Can you write a function `classify_number(n)`? It takes a number and
returns a list of all the families it belongs to.

How could Python tell that a number is irrational? The opening cell
showed that it cannot. Python stores every decimal as a fraction, so
`2 ** 0.5` is stored as a rational number very close to $\sqrt{2}$. So
we will use this rule. If a number has no decimal part, it is an
integer, and it may also be natural. If it has a decimal part, we call
it rational, and so also real.

The test `value == int(value)` is true when a number has no decimal
part.

```python exec
id: your-turn-1
def classify_number(n):
    """Return a list of the families n belongs to, from "N", "Z", "Q" and "R"."""
    # Your code here.
```

```hint
What does `int(-2.5)` give, and what does `int(7.0)` give? Which of them
is equal to the number you started with?
```

```hint
after: 3 errors
title: the steps, in words
    IF the number equals its integer version:
        IF the number >= 0:
            RETURN ["N", "Z", "Q", "R"]
        ELSE:
            RETURN ["Z", "Q", "R"]
    ELSE:
        RETURN ["Q", "R"]
```

```inputs
classify_number(7)
classify_number(-3)
classify_number(0)
classify_number(0.5)
classify_number(-2.5)
classify_number(2 ** 0.5)   # the square root of 2, stored as a fraction
```

```solution
def classify_number(n):
    """Return a list of the families n belongs to, from "N", "Z", "Q" and "R"."""
    if n == int(n):
        if n >= 0:
            return ["N", "Z", "Q", "R"]
        return ["Z", "Q", "R"]
    return ["Q", "R"]
---
`2 ** 0.5` comes out as `["Q", "R"]`. The number Python stored is a
fraction, so the function is right about that number. $\sqrt{2}$
itself is irrational, and no Python decimal can hold it exactly.
```

## Powers and their rules

A power is a short way to write repeated multiplication. $a^n$ means
$n$ copies of $a$ multiplied together. The small raised number $n$ is
called the *exponent*, and $a$ is called the *base*. For example,
$2^3 = 2 \times 2 \times 2 = 8$.

Powers follow a few rules, and algebra uses them all the time.

| Rule | In words | Example |
|---|---|---|
| $a^m \times a^n = a^{m+n}$ | When you multiply powers of the same base, add the exponents. | $2^2 \times 2^3 = 2^5 = 32$ |
| $a^m \div a^n = a^{m-n}$ | When you divide powers of the same base, subtract the exponents. | $2^5 \div 2^3 = 2^2 = 4$ |
| $(a^m)^n = a^{m \times n}$ | For a power of a power, multiply the exponents. | $(2^2)^3 = 2^6 = 64$ |
| $a^0 = 1$ for any $a \neq 0$ | Any base (except 0) to the power 0 is 1. | $5^0 = 1$ |
| $a^{-n} = \frac{1}{a^n}$ | A negative exponent means one over the positive power (the *reciprocal*). | $2^{-3} = \frac{1}{8}$ |
| $a^{1/n} = \sqrt[n]{a}$ | An exponent of $\frac{1}{n}$ means the $n$th root. | $8^{1/3} = 2$ |

The rows for $a^0$ and $a^{-n}$ come from the division rule. Divide
$a^3$ by $a^3$ and you get 1, because any number divided by itself is 1.
The division rule says the answer is $a^{3-3} = a^0$. So $a^0$ has to
be 1. In the same way, $a^0 \div a^n = a^{-n}$, and that is
$\frac{1}{a^n}$.

The root comes from the power-of-a-power rule. $(8^{1/3})^3 = 8^1 = 8$.
So $8^{1/3}$ is the number whose cube is 8, and that is 2. An exponent
such as $\frac{2}{3}$ does two things: $8^{2/3}$ is the cube root of 8,
squared, which is $2^2 = 4$.

The cell below tests the rules with $a = 3$. On the first five lines,
it prints the left side of a rule and then the right side. If a rule is
true, what should you see on those lines? Write your guess in a comment
first. Then run the cell.

```python exec
id: powers-and-their-rules-1
a = 3

print("a^2 * a^3 =", a**2 * a**3, "   a^5 =", a**5)
print("a^5 / a^3 =", a**5 / a**3, "   a^2 =", a**2)
print("(a^2)^3   =", (a**2)**3, "   a^6 =", a**6)
print("a^0       =", a**0)
print("a^(-2)    =", a**(-2), "   1/a^2 =", 1/a**2)
print("8^(1/3)   =", 8**(1/3), "   8^(2/3) =", 8**(2/3))
```

On the first five lines, the two sides match. The division line prints `9.0`,
not `9`, because `/` always gives a decimal in Python. The last line
prints `3.9999999999999996` for $8^{2/3}$. The exponent $\frac{2}{3}$
is a decimal that never ends, and Python stores a fraction close to it,
as in the opening cell. So the answer is very close to 4, but not
exactly 4.

A note on names. The syllabus, and any exam paper you sit, calls powers
*indices*, and calls the rules above the *laws of indices*. Indices and
powers are the same thing, so it is good to recognise the word. This
course says *power* and *exponent*, because the word *index* already
means something else here: the position of an item in a list.

### Powers in Python, and in maths

Python writes a power as `**`. Most calculators, and many books, write
it as `^`. What happens if you use the calculator's sign in Python?

```python exec
id: powers-in-python-1
print(3 ** 2)
print(3 ^ 2)
```

```predict
type: choice

The first line prints 9. What will the second line print?

- 9
  - `^` means "to the power of" on a calculator and in a lot of
    maths writing. There is
    [a closer look at this](tutorial:powers-in-python).
- 1
- 6
  - It could be a way of writing "3 times 2".
- An error
  - Python does not know `^`, so it should refuse it.
```

The second line prints 1, with no error. In Python, `^` is XOR, the
exclusive or from
[Logic: truth tables, XOR and De Morgan's laws](tutorial:logic-and-truth).
On two whole numbers, it compares them digit by digit in binary. 3 is
`11` in binary and 2 is `10`. They differ only in the last digit, so the
answer is `01`, which is 1. Nothing on this page needs XOR.
The danger is that `x^2` runs without an error and gives a wrong
answer, so a mistake is easy to miss.

Here is a second place where Python and a quick reading can disagree.

```python exec
id: powers-in-python-2
print((-3) ** 2)
print(-3 ** 2)
```

```predict
type: number

The first line squares $-3$ and prints 9. What will the second line
print?
```

The second line prints $-9$. Python does the power before the minus
sign, so `-3 ** 2` means $-(3^2)$. Mathematics agrees. On paper, $-3^2$
is $-9$ too. To square the number $-3$, put it in brackets, as the
first line does. The [closer look at powers](tutorial:powers-in-python)
tests both of these.

### Your turn

Can we build `power(base, exponent)` ourselves, without Python's `**`?
There are three cases to think about:

- A positive exponent means we multiply by the base again and again.
- An exponent of zero gives 1.
- A negative exponent gives one over the positive power.

Your function only needs to handle whole-number exponents.

```python exec
id: your-turn-3
def power(base, exponent):
    """base to a whole-number exponent, without using **."""
    # Your code here.
```

```hint
Which of the three cases is the easiest? Can you write that one first,
and run `power(3, 0)`?
```

```hint
after: 3 errors
title: the steps, in words
    IF exponent is 0:
        RETURN 1
    IF exponent is negative:
        RETURN 1 / power(base, -exponent)
    SET result = 1
    REPEAT exponent times:
        MULTIPLY result by base
    RETURN result
```

```inputs
guess: yes
power(2, 10)
power(3, 0)
power(2, -3)
power(-2, 3)
power(10, 1)
```

```solution
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
---
In the negative case, the function calls itself with a positive
exponent, which it can already do.
```

### Powers in your world

<div class="dl-world" data-world="music">

On a piano, each key is a *semitone* above the one before it. Twelve
semitones make an *octave*, and a note an octave higher has exactly
twice the frequency. The A that orchestras tune to vibrates 440 times a
second, 440 Hz, and the next A up is 880 Hz.

Each semitone multiplies the frequency by the same number. Call it
$r$. Twelve of them make 2, so $r^{12} = 2$. Which power of 2 is $r$?
Can you find $r$, check that $r^{12}$ is 2, and find the note seven
semitones above 440 Hz?

```python exec
id: powers-in-your-world-1--music
a4 = 440
```

```hint
Twelve copies of $r$ multiplied together make 2. The power-of-a-power
rule says $(2^{1/12})^{12} = 2^1$. What does that tell you about $r$?
```

```inputs
r
r ** 12
a4 * r ** 7    # seven semitones up
```

```solution
r = 2 ** (1 / 12)
print(r)
print(r ** 12)
print(a4 * r ** 7)
---
$r = 2^{1/12}$, about 1.0595. `r ** 12` prints `2.000000000000001`,
which is 2 with a rounding error. Seven semitones above 440 Hz is about
659.26 Hz, the note E. Musicians call that gap a fifth.
```

</div>

<div class="dl-world" data-world="rockets">

In 1619, Johannes Kepler published a rule for the planets. Measure a
planet's distance from the Sun in *astronomical units* (AU), where the
Earth is 1 AU from the Sun. Then the time the planet takes to go round
the Sun, in Earth years, is the distance to the power $\frac{3}{2}$:

$$\text{years} = \text{distance}^{3/2}$$

A mission planner needs to know how long Mars, Jupiter and Saturn take
to go round the Sun. Their average distances are 1.524, 5.203 and 9.537
AU. Can you find all three years? What does the rule give for the Earth?

```python exec
id: powers-in-your-world-1--rockets
distances = {"Mars": 1.524, "Jupiter": 5.203, "Saturn": 9.537}
```

```hint
How do you write the power $\frac{3}{2}$ in Python? Remember the
brackets: `2 ** 3 / 2` and `2 ** (3 / 2)` are different.
```

```inputs
years["Mars"]
years["Jupiter"]
years["Saturn"]
1 ** 1.5       # the Earth
```

```solution
years = {}
for planet, distance in distances.items():
    years[planet] = distance ** (3 / 2)
print(years)
---
Mars takes about 1.88 years, Jupiter about 11.87 and Saturn about
29.45. NASA's measured values are 1.88, 11.86 and 29.46, so the rule
is very close. For the Earth, $1^{3/2} = 1$: one year, as it must be.
```

</div>

## Logarithms: the inverse of powers

A *logarithm* is a power read backwards. It answers the question: "what
power of $a$ gives $x$?"

$$\text{If } a^n = x, \text{ then } \log_a(x) = n.$$

Here $a$ is the base again. For example, $2^{10} = 1024$, so
$\log_2(1024) = 10$. In words, we need ten 2s multiplied together to
make 1024.

Logarithms matter a lot in computing. In
[Searching a list: linear and binary search](tutorial:finding-things)
we saw that binary search needs about $\log_2(n)$ steps to search $n$
items. It counts how many times we can halve $n$ before we reach 1.

Python's `math` module has logarithm functions. `math.log2(x)` returns
the base-2 logarithm, and `math.log10(x)` returns the base-10
logarithm. What do you think the first two lines print? Write your guess
in a comment first. Then run the cell.

```python exec
id: logarithms-the-inverse-of-powers-1
import math

print("log2(1024) =", math.log2(1024))
print("log10(1000) =", math.log10(1000))
print("log2(1000000) =", round(math.log2(1000000), 2), "(binary search steps for 1M items)")
```

The first two print 10.0 and 3.0, because $2^{10} = 1024$ and
$10^3 = 1000$. The third prints 19.93. So binary search on a million
items needs about 20 steps.

### The rules for logarithms

A logarithm is an exponent, so the rules for exponents become rules for
logarithms. Multiplying powers adds their exponents, so

$$\log(ab) = \log a + \log b$$

Raising to a power multiplies the exponent, so

$$\log(x^n) = n \log x$$

The second rule says that $x^n$ is $n$ copies of $x$ multiplied
together, and each copy adds $\log x$. These rules hold for any base,
as long as every logarithm uses the same one. The cell checks both with
base 10.

```python exec
id: the-rules-for-logarithms-1
print(math.log10(20 * 50), math.log10(20) + math.log10(50))
print(math.log10(1000 ** 5), 5 * math.log10(1000))
```

Both lines print two equal numbers: 3.0 twice, then 15.0 twice.

The second rule solves a question that has the unknown in the
exponent. For what $n$ is $2^n = 1000$? Take the logarithm of both
sides: $n \log 2 = \log 1000$. Then divide:

$$n = \frac{\log 1000}{\log 2} = \frac{3}{0.30103} \approx 9.97$$

So ten doublings take 1 past 1000.

### Your turn

Here is another way to find a logarithm. Take a number and keep
dividing it by the base. Count how many divisions you can do while the
result stays at 1 or more. That count is the whole-number part of
$\log_{\text{base}}(x)$. For example, $1024 \div 2$ ten times gives
exactly 1, and one more division would drop below 1, so the count is
10.

The whole-number part is all we need when we count the steps an
algorithm takes. Can you write `log_base(x, base)` this way, for
$x \geq 1$?

```python exec
id: your-turn-5
def log_base(x, base):
    """The whole-number part of the logarithm of x, for x >= 1."""
    # Your code here.
```

```hint
Which kind of loop keeps going for as long as something is true? What
has to be true for one more division to be allowed?
```

```inputs
guess: yes
log_base(1024, 2)
log_base(1000, 10)
log_base(100, 3)     # 3^4 = 81 and 3^5 = 243
log_base(1, 5)
```

```solution
def log_base(x, base):
    """The whole-number part of the logarithm of x, for x >= 1."""
    count = 0
    while x >= base:
        x = x / base
        count = count + 1
    return count
---
The loop stops as soon as one more division would take `x` below 1.
`log_base(1, 5)` is 0, because $5^0 = 1$.
```

### Logarithms in your world

<div class="dl-world" data-world="music">

A semitone multiplies the frequency by $2^{1/12}$, so $n$ semitones
multiply it by $2^{n/12}$. So the number of semitones between two notes
is

$$n = 12 \log_2\left(\frac{\text{higher}}{\text{lower}}\right)$$

A whistle at 1000 Hz sounds above the orchestra's A at 440 Hz. How many
semitones above? People can hear from about 20 Hz to about 20,000 Hz.
How many octaves is that?

```python exec
id: logarithms-in-your-world-1--music
import math

a4 = 440
whistle = 1000
```

```hint
An octave doubles the frequency. So the number of octaves between two
frequencies is the power of 2 that turns one into the other. Which
logarithm is that?
```

```inputs
semitones
octaves
```

```solution
semitones = 12 * math.log2(whistle / a4)
octaves = math.log2(20000 / 20)
print(semitones, octaves)
---
The whistle is about 14.2 semitones above the A. That is between two
piano keys, a little above the B an octave and a tone up. Human hearing
covers $\log_2 1000 \approx 9.97$, so about ten octaves. A piano's 88
keys cover a little over seven.
```

</div>

<div class="dl-world" data-world="fantasy-maps">

The map of the kingdom can zoom. At zoom 0, the whole kingdom, 1,024 km
across, fits in one square 256 pixels wide. Each zoom level doubles the
number of pixels across, so at zoom $z$ one pixel covers

$$\frac{1\,024\,000}{256 \times 2^z} = \frac{4000}{2^z} \text{ metres}$$

The map maker wants to see single houses, so one pixel must cover 1 m
or less. What is the smallest zoom level that does it?

```python exec
id: logarithms-in-your-world-1--fantasy-maps
import math

metres_across = 1_024_000
pixels_at_zoom_0 = 256
```

```hint
You need $\frac{4000}{2^z} \leq 1$, so $2^z \geq 4000$. Which logarithm
turns "what power of 2 gives 4000?" into a number?
```

```inputs
exact
zoom
metres_across / (pixels_at_zoom_0 * 2 ** zoom)    # metres per pixel at that zoom
```

```solution
exact = math.log2(metres_across / pixels_at_zoom_0)
zoom = math.ceil(exact)
print(exact, zoom)
---
$\log_2 4000 \approx 11.97$, and a zoom level is a whole number, so
the answer is zoom 12. There, one pixel covers about 0.98 m. At zoom 11
it covers about 1.95 m. Many map websites double from one zoom level to
the next in the same way.
```

</div>

## Formulas as functions

A formula for area, perimeter or volume is a function. It takes
measurements as input and returns a value. For example, the area of a
circle takes a radius $r$ and returns $\pi r^2$. For $r = 5$ that is
$\pi \times 25$, about 78.54.

| Shape | Formulas |
|---|---|
| Rectangle, length $l$ and width $w$ | area $lw$, perimeter $2(l + w)$ |
| Triangle, base $b$ and height $h$ | area $\frac{1}{2}bh$ |
| Circle, radius $r$ | area $\pi r^2$, circumference $2\pi r$ |
| Cylinder, radius $r$ and height $h$ | volume $\pi r^2 h$, surface area $2\pi r^2 + 2\pi r h$ |
| Cone, radius $r$ and height $h$ | volume $\frac{1}{3}\pi r^2 h$ |
| Sphere, radius $r$ | volume $\frac{4}{3}\pi r^3$, surface area $4\pi r^2$ |

A square is a rectangle with $l = w$. A cube with side $s$ has volume
$s^3$ and surface area $6s^2$.

### Your turn

Can you write three of these as Python functions, each with a
docstring: `circle_area(radius)`, `cylinder_volume(radius, height)` and
`sphere_volume(radius)`? A cylinder is a circle with depth, so
`cylinder_volume` can call `circle_area`.

```python exec
id: your-turn-7
import math

# Your three functions
```

```hint
What does `math.pi * 5 ** 2` give? Is it about 78.54?
```

```inputs
guess: yes
circle_area(5)
cylinder_volume(2, 10)
sphere_volume(3)
circle_area(0)
```

```solution
def circle_area(radius):
    """The area of a circle with this radius."""
    return math.pi * radius ** 2


def cylinder_volume(radius, height):
    """The volume of a cylinder: a circle, with depth."""
    return circle_area(radius) * height


def sphere_volume(radius):
    """The volume of a sphere with this radius."""
    return 4 / 3 * math.pi * radius ** 3
---
`cylinder_volume` calls `circle_area`. If you wrote $\pi r^2 h$ out
again, the code would work, but it would hide the fact that a cylinder
is a circle with depth.
```

### What doubling does

The formulas can answer a question that surprises many people. If you
double the radius, what happens to the area and the volume? The cell
finds both, for a radius of 1, 2 and 4.

```python exec
id: what-doubling-does-1
import math

for radius in [1, 2, 4]:
    area = math.pi * radius ** 2
    volume = 4 / 3 * math.pi * radius ** 3
    print(radius, round(area, 2), round(volume, 2))
```

```predict
type: choice

The radius doubles from 1 to 2. What happens to the sphere's volume?

- It doubles
  - Twice the radius sounds like twice the sphere.
- It becomes four times as big
  - An area grows four times, and a volume sounds like an area with
    some depth.
- It becomes eight times as big
```

The area goes from 3.14 to 12.57, four times as big. The volume goes
from 4.19 to 33.51, eight times as big. Double again, and the same
thing happens: four times the area, eight times the volume.

The reason is the power in each formula. An area has $r^2$ in it, and
$(2r)^2 = 4r^2$. A volume has $r^3$, and $(2r)^3 = 8r^3$. So when every
length is multiplied by $k$, every area is multiplied by $k^2$ and
every volume by $k^3$.

<div class="dl-world" data-world="music">

A snare drum is about 36 cm across, and a bass drum about 56 cm. How
many times bigger is the bass drum's skin? Can you find it with the
area formula, or your `circle_area`, and then again with the rule,
without $\pi$?

```python exec
id: what-doubling-does-2--music
snare = 36
bass = 56
```

```inputs
ratio
(bass / snare) ** 2
```

```solution
ratio = (math.pi * (bass / 2) ** 2) / (math.pi * (snare / 2) ** 2)
print(ratio)
print((bass / snare) ** 2)
---
Both give about 2.42. The bass drum is $\frac{56}{36}$ times as wide,
and $\left(\frac{56}{36}\right)^2 \approx 2.42$. The $\pi$ and the halving cancel when you divide
one area by the other, so only the ratio of the widths matters.
```

</div>

<div class="dl-world" data-world="rockets">

A rocket's fuel tank is a cylinder 1.8 m in radius and 30 m tall. The
engineers are offered a tank with twice the radius, or a tank twice as
tall. Which one holds more fuel, and how many times more than the
original? What about a tank twice as big in every direction?

```python exec
id: what-doubling-does-2--rockets
radius = 1.8
height = 30
```

```inputs
original
wider / original
taller / original
bigger / original
```

```solution
original = math.pi * radius ** 2 * height
wider = math.pi * (2 * radius) ** 2 * height
taller = math.pi * radius ** 2 * (2 * height)
bigger = math.pi * (2 * radius) ** 2 * (2 * height)
print(original, wider / original, taller / original, bigger / original)
---
The original tank holds about 305 m³. Twice the radius holds 4 times
as much, because the radius is squared. Twice the height holds only
twice as much. Twice as big in every direction holds 8 times as much.
```

</div>

<div class="dl-world" data-world="fantasy-maps">

The kingdom's map is redrawn for a wall, twice as wide and twice as
tall as the old one. On the old map, the Lake of Mists was a circle
3 cm in radius. How many times more ink does the lake need on the new
map? The map maker also carves a model of the Black Mountain, a cone,
at twice the size of the old model. How many times more clay does the
new model need?

```python exec
id: what-doubling-does-2--fantasy-maps
lake_radius = 3
```

```inputs
ink
clay
```

```solution
ink = (math.pi * (2 * lake_radius) ** 2) / (math.pi * lake_radius ** 2)
clay = 2 ** 3
print(ink, clay)
---
The lake needs 4 times the ink, because an area grows with the square
of the scale. The mountain needs 8 times the clay. A cone's volume,
$\frac{1}{3}\pi r^2 h$, has three lengths multiplied together, and
each one doubles.
```

</div>

## Looking back

A power and a logarithm are the same fact, read in two directions.
$2^{10} = 1024$ answers "what is ten 2s multiplied together?", and
$\log_2 1024 = 10$ answers "how many 2s make 1024?". Where on this page
did you need the second question, and not the first?

A challenge: can you write a number explorer? Give it a number, and it
prints what it can find: the families from `classify_number`, whether
the number is a perfect square or a perfect cube, and its logarithm to
base 2. What else could it report?

```python challenge
# A number explorer: what can you find out about a number?
import math


def explore_number(n):
    print("Number:", n)
    if n > 0:
        print("log2:", round(math.log2(n), 4))
    print("squared:", n ** 2, " cubed:", n ** 3)


explore_number(49)
explore_number(-3.5)
```

## Where to read more

3Blue1Brown (2020). *Logarithm Fundamentals* (Lockdown live math, episode 6).
<https://www.youtube.com/watch?v=cEvgcoyZvB4>. It shows, and does not only
state, why a logarithm is an exponent read backwards.

3Blue1Brown (2016). *Triangle of Power.*
<https://www.youtube.com/watch?v=sULa9Lc4pck>. Powers, roots and
logarithms are three questions about the same three numbers. This short
video draws all three with one triangle. The video is about eight minutes
long.

Veritasium (2021). *The Discovery That Transformed Pi*.
<https://www.youtube.com/watch?v=gMlf1ELvRzc>. It is not directly about why
pi is irrational. It shows that a number can be defined exactly and still
be impossible to write down in full.

Stewart, I. (2008). *Taming the Infinite: The Story of Mathematics.* Quercus.
Chapters 2 and 3 describe how the number families were built one at a time, each to
solve a problem the previous one could not.

Python Software Foundation. *Floating Point Arithmetic: Issues and Limitations.*
<https://docs.python.org/3/tutorial/floatingpoint.html>. It gives the
official short answer to why `Fraction(0.1)` is not one tenth, and why
`0.1 + 0.2` is not `0.3`. It is worth reading once, carefully.

Khan Academy. *Exponents, radicals, and scientific notation.*
<https://www.khanacademy.org/math/algebra/x2f8bb11595b61c86:rational-exponents-radicals>.
It gives practice on the rules for powers, if the ones here went too
quickly.

The planets' distances are JPL's mean values, from
[Approximate Positions of the Planets](https://ssd.jpl.nasa.gov/planets/approx_pos.html).
Their measured years are from NASA's
[planetary fact sheets](https://nssdc.gsfc.nasa.gov/planetary/factsheet/).
