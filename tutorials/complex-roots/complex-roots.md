---
title: "Complex numbers: roots that are not real"
year: "2026-2027"
version: 2026.09.26.1
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
worlds:
  electronics: Resistors, coils and the alternating current through them.
  rockets: A satellite going round the Earth, a quarter at a time.
  fantasy-maps: A made-up kingdom, and a map that can be turned.
---

# Complex numbers: roots that are not real

In [Solving equations: linear, quadratic and simultaneous](tutorial:cracking-equations)
we wrote a solver for quadratic equations. It calculates the
discriminant. When the discriminant is negative, the solver says there
are no real solutions and stops. In
[Parabolas: completing the square](tutorial:parabolas) we saw the same
thing in a picture: the vertex sits above the axis, and the curve never
comes down to it.

On this page we ask what comes after that stop. The answer always
existed. Mathematicians found it with the same idea they had used three
times before, and that idea matters more than the arithmetic.

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

"No real solutions" is a true description, as long as we only accept
numbers that sit on that horizontal line. It says there is no answer on
this line. It does not say there is no answer anywhere.

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
- $\mathbb{R}$ fills the gaps with the irrational numbers, so now most
  things work. But $\sqrt{-1}$ has no answer in $\mathbb{R}$.

Each step happened because somebody would not accept "there is no
answer". They invented the number that makes an answer. People resisted
several of these inventions when they were new, and negative numbers
and irrational numbers met strong resistance. Today all of them are
taught in school.

So the next step uses the same idea one more time. It is not a special
trick.

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

Now look at `z * w`. We can multiply it by hand, the same way we
multiply two brackets:

$$(3 + 2i)(1 - 4i) = 3 - 12i + 2i - 8i^2$$

The definition matters in the last term. Since $i^2 = -1$,
the term $-8i^2$ is $-8 \times (-1) = +8$. So the total is
$3 + 8 - 10i = 11 - 10i$, which matches Python's `(11-10j)`.

Only one step is unusual. $i^2$ becomes a real number again.

## A cubic that needed it

For centuries, people were content to say that $x^2 + 1 = 0$ has no
answer. It was a cubic, not a quadratic, that changed their minds.

In 1572 Rafael Bombelli took the equation $x^3 = 15x + 4$. Its answer is
4, and anybody can check that: $4^3 = 64$, and $15 \times 4 + 4 = 64$.
But the formula for cubics, used on this equation, says

$$x = \sqrt[3]{2 + \sqrt{-121}} + \sqrt[3]{2 - \sqrt{-121}}$$

Halfway through, the formula needs $\sqrt{-121}$, which is $11i$. So
the answer 4 is made of two cube roots of complex numbers,
$\sqrt[3]{2 + 11i}$ and $\sqrt[3]{2 - 11i}$. Bombelli guessed that the
first is $2 + i$. Is he right? Cube it and see.

```python exec
id: a-cubic-that-needed-it-1
print((2 + 1j) ** 3)
```

```predict
type: choice

What will $(2 + i)^3$ be?

- $2 + 11i$
- $8 + i$
  - Cubing each part on its own gives $2^3$ and $i^3$.
- $8 - i$
  - $2^3$ is 8, and $i^3$ is $-i$.
- An error
  - A complex number to a power sounds like something Python may not
    do.
```

It prints `(2+11j)`. Multiplied out, $(2 + i)^3 = 8 + 12i + 6i^2 + i^3$.
The $i^2$ is $-1$ and the $i^3$ is $-i$, so it is
$8 + 12i - 6 - i = 2 + 11i$. So $2 + i$ is a cube root of $2 + 11i$, as
Bombelli guessed.

### Your turn

Bombelli's other cube root is $2 - i$. Can you check that
$(2 - i)^3 = 2 - 11i$? Then add the two cube roots together. What do
you get, and why is it the answer Bombelli wanted?

```python exec
id: your-turn-bombelli
first = 2 + 1j
second = 2 - 1j
```

```hint
The formula says $x$ is the first cube root plus the second. What is
$(2 + i) + (2 - i)$?
```

```inputs
second ** 3
first + second
```

```solution
print(second ** 3)
print(first + second)
---
`second ** 3` prints `(2-11j)`, and `first + second` prints `(4+0j)`.
The imaginary parts cancel, and 4 is left: the real answer, which the
formula could only reach by passing through complex numbers. Bombelli
treated $\sqrt{-1}$ as a number with its own rules, and it led him to
an answer everybody could check. That made the new number hard to
dismiss.
```

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
roots of $x^2 + 1 = 0$ are $i$ and $-i$, which Python writes as `1j`
and `-1j`.

Look at the first line. The roots of $x^2 - 5x + 6$ are 3 and 2, but
Python prints `(3+0j)` and `(2+0j)`. The `+0j` means "plus zero lots of
$i$". `cmath.sqrt` always returns a complex number, even when the
answer is real, so everything after it is complex too. $3 + 0i$ is the
number 3, stored as a complex number. The imaginary part is exactly 0,
and `(3+0j).imag` is `0.0`.

This is a fact about mathematics, not only about Python. Making the
number system bigger removed a special case. It did not add one. Two
roots, one root and no real roots become one situation. We can see all
of it once we work in $\mathbb{C}$.

### Does it work?

Now we check the answers. Remember that a root is a number that makes
the expression equal zero. So we can put each root back into its
quadratic and see what we get.

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

This check proves it. A root is a number that makes the expression
zero. These numbers make the expression zero. So they are roots. We do
not have to take the definition on trust.

### Your turn, on paper

Here are three quadratics:

- $x^2 + 4 = 0$
- $x^2 - 2x + 5 = 0$
- $x^2 + 6x + 13 = 0$

Can you solve each one by hand with the quadratic formula, and write
each answer in the form $a + bi$? Then check each answer with the
solver in the cell below.

```python exec
id: your-turn-1
# Your answers, then the check.
# print(solve(1, 0, 4))
```

<details class="dl-answer"><summary>answer</summary>

- $x^2 + 4 = 0$: the discriminant is $-16$, and $\sqrt{-16} = 4i$, so
  $x = \pm 2i$.
- $x^2 - 2x + 5 = 0$: the discriminant is $4 - 20 = -16$, so
  $x = \frac{2 \pm 4i}{2} = 1 \pm 2i$.
- $x^2 + 6x + 13 = 0$: the discriminant is $36 - 52 = -16$, so
  $x = \frac{-6 \pm 4i}{2} = -3 \pm 2i$.

</details>

## Where the roots go

When the discriminant goes from positive to negative, the roots do not
vanish. Where do they go? Let's watch. The cell solves
$x^2 - 2x + c = 0$ for $c$ from $-3$ to 5, and marks both roots on a
plane: the real part along the bottom, and the imaginary part up the
side. This is called the *complex plane*.

```python exec
id: where-the-roots-go-1
fig, ax = plt.subplots()
for step in range(0, 81):
    c = -3 + step / 10
    for root in solve(1, -2, c):
        ax.plot(root.real, root.imag, "o", markersize=3, color=plt.cm.viridis(step / 80))
ax.axhline(0, color="black", linewidth=0.8, zorder=0)
ax.axvline(0, color="black", linewidth=0.8, zorder=0)
ax.set_xlabel("real part")
ax.set_ylabel("imaginary part")
ax.set_aspect("equal")
ax.set_title("The roots of x^2 - 2x + c, for c from -3 (dark) to 5 (light)")
```

```predict
type: choice

Before you run it: as $c$ grows past 1, where do the two roots go?

- They vanish
  - "No real roots" sounds as if there is nothing left to draw.
- They meet at 1, then move apart, up and down
- They meet at 1, then both move off to the right
  - A bigger $c$ sounds like the roots should get bigger.
```

For $c$ up to 1, both roots are real, on the horizontal axis. They move
towards each other and meet at $x = 1$ when $c = 1$. That is the
repeated root, where the parabola just touches the axis. Then they turn
a corner. For $c$ above 1 they move apart again, straight up and
straight down, as $1 + \sqrt{c - 1}\,i$ and $1 - \sqrt{c - 1}\,i$. The
roots never stop existing. They leave the real line, one above and one
below it, always a mirror image of each other.

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

Why? Take $x^2 - 4x + 13 = 0$, which has a root at $2 + 3i$. That means

$$(2 + 3i)^2 - 4(2 + 3i) + 13 = 0$$

Now change the sign of every $i$ in that line. Every step of the working
stays true, because $-i$ behaves exactly like $i$: its square is $-1$
too. The numbers 1, $-4$ and 13 have no $i$ in them, so they do not
change, and neither does the 0 on the right. What is left is

$$(2 - 3i)^2 - 4(2 - 3i) + 13 = 0$$

So $2 - 3i$ is a root as well. This only needed the numbers in the
equation to be real. The same argument works for a cubic, or for any
polynomial whose numbers are real. It is also why the picture of the
roots above was the same above and below the axis.

### Your turn

The equation $x^2 - 6x + 25 = 0$ has a root at $3 + 4i$. Without
calculating anything, can you say what the other root is? How do you
know? Write your answer as a comment in the cell, then check it with
the solver.

```python exec
id: your-turn-2
# Your answer as a comment, then check it.
# print(solve(1, -6, 25))
```

## Multiplying by i

Adding complex numbers moves a point on the plane. Multiplying by $i$
does something more surprising. The cell starts at $3 + i$ and
multiplies by $i$ again and again, marking each answer.

```python exec
id: multiplying-by-i-1
z = 3 + 1j
fig, ax = plt.subplots()
for turn in range(4):
    ax.plot([0, z.real], [0, z.imag], "o-", label=f"times i, {turn} times: {z}")
    z = z * 1j
ax.axhline(0, color="black", linewidth=0.8)
ax.axvline(0, color="black", linewidth=0.8)
ax.set_aspect("equal")
ax.legend()
```

The four points are $3 + i$, $-1 + 3i$, $-3 - i$ and $1 - 3i$. Each one
is the one before, turned a quarter of the way round the origin,
anticlockwise. Multiplying by $i$ is a quarter turn. Four quarter turns
bring the point back where it started, which is another way of saying
$i^4 = 1$. Two quarter turns make a half turn, and a half turn sends a
point to its opposite: that is $i^2 = -1$, seen as a picture.

The length of each line, the point's distance from the origin, stays
the same. Python's `abs(z)` gives that distance for a complex number:
`abs(3 + 1j)` is about 3.16. Turning and distance on a circle are the
subject of [The unit circle: sine, cosine and tangent](tutorial:the-unit-circle),
where these quarter turns appear again.

### Complex numbers in your world

<div class="dl-world" data-world="electronics">

Engineers write $j$ for $\sqrt{-1}$, as Python does, because $i$ is
already the current. In an alternating current circuit, a resistor of
30 ohms and a coil in a line behave like the complex number $30 + 40j$.
The coil's part is imaginary because its voltage runs a quarter of a
cycle ahead of the current. This complex number is called the
*impedance*, and its distance from the origin, `abs`, is how much the
pair resists the current. What is it? And a second pair, $20 - 15j$, is
added in the same line: impedances in a line add. What is the total,
and how much does it resist?

```python exec
id: in-your-world-1--electronics
first = 30 + 40j
second = 20 - 15j
```

```hint
`abs(z)` gives the distance of `z` from the origin. What do you add to
find the total?
```

```inputs
abs(first)
first + second
abs(first + second)
```

```solution
print(abs(first))
total = first + second
print(total, abs(total))
---
`abs(30 + 40j)` is 50.0, because $\sqrt{30^2 + 40^2} = 50$: the 30 and
the 40 are two sides of a right-angled triangle. The total is
`(50+25j)`, which resists about 55.9 ohms, less than $50 + 25 = 75$.
The $-15j$ part undoes some of the $40j$.
```

</div>

<div class="dl-world" data-world="rockets">

A satellite goes round the Earth in a circle. Put the Earth's centre at
the origin of the complex plane, and write the satellite's position,
in km, as a complex number. It starts at $7000 + 0i$. Every quarter of
an orbit, its position is multiplied by $i$. Where is it after one,
two, three and four quarters? How far from the Earth's centre is it
each time?

```python exec
id: in-your-world-1--rockets
position = 7000 + 0j
```

```hint
Multiply by `1j` once for each quarter. `abs(position)` gives the
distance from the origin.
```

```inputs
position * 1j
position * 1j ** 2
position * 1j ** 4
abs(position * 1j ** 3)
```

```solution
for quarter in range(1, 5):
    where = position * 1j ** quarter
    print(quarter, where, abs(where))
---
After one quarter it is at $7000i$, straight up the imaginary axis.
After two it is at $-7000$, the other side of the Earth, and after four
it is back at 7000. After three it is at `-7000j`, straight down. The
distance is 7000 km every time, because a quarter turn never changes
the distance from the origin.
```

</div>

<div class="dl-world" data-world="fantasy-maps">

The map maker keeps every place on the map as a complex number, with
east as the real part and north as the imaginary part, in km from the
market cross. The castle is at $3 + 2i$. The map is turned a quarter
turn anticlockwise, to fit a new frame. Where is the castle now? Where
is the mill, at $-1 + 4i$?

```python exec
id: in-your-world-1--fantasy-maps
castle = 3 + 2j
mill = -1 + 4j
```

```hint
A quarter turn anticlockwise is a multiplication by one number. Which?
```

```inputs
castle * 1j
mill * 1j
abs(castle)
abs(castle * 1j)
```

```solution
print(castle * 1j, mill * 1j)
---
The castle moves to $-2 + 3i$, and the mill to $-4 - i$. Each is the
same distance from the market cross as before, about 3.61 km for the
castle. A turn moves every place, but it never changes a distance.
```

</div>

## Looking back

In [Solving equations: linear, quadratic and simultaneous](tutorial:cracking-equations)
our solver stopped at "no real solutions". That was accurate, but it
was not the end. In a larger set of numbers, there was an answer, and
the picture of the roots showed where it had gone.

Before this page, what did you think "no solution" meant? What would
you say now, to somebody who told you that $x^2 + 1 = 0$ has no
answer?

A challenge: the powers of $i$ go round in a square. Can you mark
$(1 + i)^n$ on the complex plane for $n$ from 0 to 8? What shape do the
points make, and why do they move further out each time?

```python challenge
import matplotlib.pyplot as plt

z = 1 + 1j
fig, ax = plt.subplots()
for n in range(9):
    point = z ** n
    ax.plot(point.real, point.imag, "o")
ax.set_aspect("equal")
```

## Where to read more

Stephen Welch (Welch Labs) (2015). *Imaginary Numbers Are Real
[Part 1: Introduction].* <https://www.youtube.com/watch?v=T647CGsuOVU>.
This ten-part series tells the same story as this page. Each family of
numbers grows from one question with no answer. This is part one.

Veritasium (2021). *How Imaginary Numbers Were Invented.*
<https://www.youtube.com/watch?v=cUzklzVXJwo>. The first people to need
square roots of negative numbers were solving cubic equations, not
quadratics. Veritasium tells the story of Bombelli's cubic and the
people before him. It is about twenty-three minutes long.
