---
title: "How a computer stores a number"
context_for:
  - numbers-a-computer-can-hold
  - everything-is-ones-and-zeros
  - running-a-formula-backwards
  - does-it-work
year: "2026-2027"
version: 2026.09.24.1
---

# How a computer stores a number

Ask Python for `0.1 + 0.2`, and it answers `0.30000000000000004`. Is
Python bad at sums? No. It is doing exactly what it was built to do, in
a space with one rule that usually goes unsaid. This page says that rule
out loud, and uses it to explain every float surprise in this course.

On this page we:

- write a third in decimal, and see the same problem a computer has
- look at the number Python really keeps when we type `0.1`
- read answers that end in `e-16`, and see where they come from
- find out why the square root of 2 cannot be kept exactly
- see where Python's floats run out, and why its whole numbers never do
- see why `close_enough` is in your toolkit

> **The space we're in.** Python's floats. Each one is kept in 64 bits,
> and that number never changes: not for 0.5, not for a tenth, not for
> the distance to the Sun. A fixed number of bits means a fixed number
> of digits, and everything on this page follows from that one fact.

## A third, in four digits

Before we look at binary, let's make the same problem with our own
digits. Say you may write a number with at most four digits after the
point. Then a third is `0.3333`. That is close to $\frac{1}{3}$, but it
is not $\frac{1}{3}$, because the true answer is $0.3333\ldots$ with
threes for ever.

Now add three of those thirds. In ordinary maths,
$\frac{1}{3} + \frac{1}{3} + \frac{1}{3} = 1$. What do you think we get
with four digits? Run it to check.

```python exec
id: stores-a-third
third = 0.3333
print(third + third + third)
```

We get `0.9999`, not `1`. Each third was a tiny bit too small, and three
small shortfalls added up to one we can see. Nobody made a mistake. The
space only had room for four digits.

This gap between the true answer and the kept answer has a name. A
*rounding error* is the difference between a number and the nearest
value the space can hold. A computer's floats have exactly this problem,
with two changes: the digits are binary, and there are more of them.

## What Python really keeps for 0.1

On [Everything is ones and zeros](tutorial:everything-is-ones-and-zeros#why-01-02-is-not-03)
we saw that the binary columns after the point are worth a half, a
quarter, an eighth, and so on. A tenth cannot be built from those
exactly. In binary it repeats for ever, the way a third does in decimal.

A float keeps 53 binary digits of a number. That is about 16 decimal
digits. So Python cuts 0.1 off after 53 binary digits, and keeps the
nearest fraction it can. Every float is really a fraction whose bottom
number is a power of 2. We can ask Python for that fraction with
`.as_integer_ratio()`, which gives the top and the bottom as whole
numbers.

What do you expect the bottom number to be? Run it, then compare it with
the second line.

```python exec
id: stores-the-real-tenth
print((0.1).as_integer_ratio())
print(2 ** 55)
print((0.75).as_integer_ratio())
```

The bottom number is exactly $2^{55}$. So what Python keeps for 0.1 is

$$\frac{3602879701896397}{36028797018963968}$$

which is very close to a tenth, and a tiny bit bigger. A tenth would
need the top number to be 3602879701896396.8, and a fraction of this
kind must have a whole number on top. Compare `0.75`: it is
$\frac{3}{4}$, and 4 is a power of 2, so it is kept exactly.

## Why 0.1 + 0.2 lands next door

Here is the kept value of each number, written out to 30 decimal places.
Before you run it, think about the last section. Will each kept value be
too big, or too small?

```python exec
id: stores-three-neighbours
print(format(0.1, ".30f"))
print(format(0.2, ".30f"))
print(format(0.1 + 0.2, ".30f"))
print(format(0.3, ".30f"))
```

The kept 0.1 and the kept 0.2 are both a little too big. The kept 0.3 is
a little too small. When we add 0.1 and 0.2, their two small extras add
up, and the answer lands on the float just above 0.3, not on the one
Python uses for 0.3. The two floats are neighbours. `==` asks whether
two floats are the same float, so it says `False`.

Python also prints numbers in a helpful way: it shows the shortest
decimal that leads back to the same float. For the kept 0.3, that is
`0.3`. For its neighbour, the shortest is `0.30000000000000004`.

## Reading e-16

Some answers in this course end in something like `e-16`. This is
*scientific notation*, a way to write a very large or very small number
as a short number times a power of 10. Python writes it with an `e`,
which means "times 10 to the power". So `1.1e-16` is
$1.1 \times 10^{-16}$, which is 0.00000000000000011.

What size is the gap between two neighbouring floats? Near 1, it is about
$2.2 \times 10^{-16}$. A change smaller than half of that cannot be kept
at all. What do you think the first line prints? Run it to check.

```python exec
id: stores-e-minus-16
print(1 + 1e-16 == 1)
print(1 + 1e-15 == 1)
print((0.1 + 0.2) - 0.3)
```

Adding $10^{-16}$ to 1 changes nothing: the answer rounds straight back
to 1. Adding $10^{-15}$ is big enough to land on a different float. And
the leftover in `(0.1 + 0.2) - 0.3` is about $5.6 \times 10^{-17}$.

So when an answer that should be 0 comes out as something `e-16` or
`e-17`, read it as "0, plus a rounding error". The size of the error
tells you it came from the 16th digit, far past anything we measured.

## The square root of 2

On [Numbers a computer can hold](tutorial:numbers-a-computer-can-hold#families-of-numbers)
we met $\sqrt{2}$, a real number that is not a fraction. A number that
cannot be written as one whole number divided by another is called
*irrational*. Its digits go on for ever without repeating, in decimal,
in binary, in any base at all.

A float is always a fraction. So a float can never be $\sqrt{2}$. Half
of $\sqrt{2}$, squared, should be exactly $\frac{2}{4} = 0.5$. What do
you expect from Python?

```python exec
id: stores-root-two
import math

half_root_two = math.sqrt(2) / 2
print(half_root_two)
print(half_root_two ** 2)
print(half_root_two ** 2 - 0.5)
```

The square is `0.5000000000000001`, and the difference from 0.5 is about
$1.1 \times 10^{-16}$. Python kept the nearest float to $\sqrt{2}$, which
was very slightly off. Squaring it doubled the tiny error, and the
answer landed on the neighbour of 0.5. This is the same number you meet
in trigonometry, as the sine of 45°, so this surprise will come back.

## How big can a number be?

Python's two number spaces run out in different ways.

An int has no fixed size. Python gives a whole number as many bits as
it needs, so `10 ** 400`, a 1 with 400 zeros, is kept exactly.

A float always has 64 bits. They are shared out a little like
scientific notation: 1 bit for the sign, 11 bits for the power of 2,
and the rest for the digits. The power can only go so high. So there is
a largest float, a little under $1.8 \times 10^{308}$. What happens when
we go past it? Predict, then run it.

```python exec
id: stores-running-out
print(10 ** 400 > 0)
print(1e308)
print(1e308 * 10)
```

`10 ** 400` is fine. But `1e308 * 10` gives `inf`, short for infinity.
Going past the largest value a space can hold is called *overflow*. In
some languages, an int that overflows wraps round to a negative number
without a word of warning. Python's ints never overflow. Its floats do,
and when they do, Python gives the answer `inf`: a float that means
"bigger than any float".

So each space has its own promise. Ints promise to be exact, however
large. Floats promise to be very close, over a huge range, and to stay
the same size in memory.

## When rounding errors add up

One rounding error of $10^{-16}$ does no harm. Many of them, added up
over time, can.

In 1991, during the Gulf War, a Patriot missile defence system at
Dhahran, in Saudi Arabia, failed to stop an incoming Scud missile. The
Scud hit an army barracks, and 28 American soldiers were killed. A
government report found the cause. The system counted time in tenths
of a second, and kept 0.1 in binary with a fixed number of digits, so
every tick was very slightly short. The battery had been running for
more than 100 hours. By then, the small error in every tick had added
up to about a third of a second, and in a third of a second a Scud
travels far enough to be looked for in the wrong place.

The software had already been corrected. The new version arrived at
Dhahran the day after the attack.

## So what do we do? Close enough

None of this makes floats wrong. It means that with floats, "equal" is
the wrong question. The right question is "how far apart are these?".

On [Does it work?](tutorial:does-it-work#close-enough) you wrote
`close_enough`, which says two numbers are equal when the distance
between them is no bigger than a small *tolerance*. Here is the same
test, written out in one line, so that it runs on this page too. What
will each line print?

```python exec
id: stores-close-enough
tolerance = 1e-9

print(0.1 + 0.2 == 0.3)
print(abs((0.1 + 0.2) - 0.3) <= tolerance)
print(abs(half_root_two ** 2 - 0.5) <= tolerance)
```

`==` says `False`, and the tolerance test says `True` both times. A
billionth is far bigger than a rounding error of $10^{-16}$, and far
smaller than any difference a person would care about in a bill, a
temperature or a distance.

There are two other ways, and each fits a different space:

- **Count in whole units.** A bank keeps €12.30 as 1230 cents, an int.
  Ints are exact, so adding a million payments gives an exact total.
- **Use a fraction.** Python's `fractions` module keeps $\frac{1}{10}$
  as a true fraction, with no rounding at all. It is slower, and it
  cannot hold $\sqrt{2}$, but for exact sums of fractions it is right.

Which to choose is the fourth question again: what does this space let
us do? Floats let us work fast with very large and very small numbers,
and ask us to accept a tiny error. When that error matters, we choose a
different space.

## Where to read more

Python Software Foundation. *Floating-Point Arithmetic: Issues and
Limitations*. A chapter of the official Python tutorial. It covers the
same ground as this page, with a little more detail on how Python
prints a float.

Goldberg, D. (1991). What every computer scientist should know about
floating-point arithmetic. *ACM Computing Surveys*, 23(1). The classic
long account. It needs more maths than this course, and it is worth
coming back to later.
