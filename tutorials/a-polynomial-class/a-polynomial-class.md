---
title: "A polynomial class: a project in many methods"
year: "2026-2027"
version: 2026.09.26.1
covers:
  a-ball-in-the-air:
    covers: [FOOP-LO4]
  the-highest-power:
    covers: [FOOP-LO4]
  a-rule-for-the-coefficients:
    covers: [FOOP-LO3]
  printing-it-the-way-we-write-it:
    covers: [FOOP-LO4]
  polynomials-that-make-polynomials:
    covers: [FOOP-LO4, FOOP-LO8]
---

# A polynomial class: a project in many methods

This page is a project: one class, built a method at a time, on your own
or with a partner. It is harder than the pages before it. Each stage has a
first step anyone can take, and more for anyone who wants it, and each
has one good answer to compare with when you are ready.

A ball is thrown straight up at 20 metres a second, from a hand 1.5 m
above the ground. After $x$ seconds, its height in metres is

$$-5x^2 + 20x + 1.5$$

taking gravity as 10 m/s² to keep the numbers round. (It is nearer 9.8.)
A sum of terms like this, each a number times a power of $x$, is a
*polynomial*. The number in front of each power is its *coefficient*:
here, −5, 20 and 1.5.

## A ball in the air

We can store a polynomial as a list of its coefficients, where the item at
index `i` is the coefficient of $x^i$. So $-5x^2 + 20x + 1.5$ is
`[1.5, 20, -5]`: first the number on its own ($x^0$), then $x^1$, then
$x^2$. If you have done
[Polynomials: representing and combining them in Python](tutorial:expressions-come-alive),
you have met this list, and functions that work on it. Here the list and
the functions become one class.

The cell prints the ball's height each second for four seconds. What is
the greatest height it will print?

```python exec
id: a-ball-in-the-air-1
class Polynomial:
    def __init__(self, coefficients):
        self._coefficients = coefficients

    def evaluate(self, x):
        total = 0
        for power in range(len(self._coefficients)):
            total = total + self._coefficients[power] * x ** power
        return total

height = Polynomial([1.5, 20, -5])
for second in range(5):
    print(second, height.evaluate(second))
```

```question
id: a-ball-in-the-air-q1
type: multiple-choice
answer: 1

What is the greatest height it will print?

- 21.5, after 2 seconds
  - The ball slows as it rises, and stops rising half-way through its flight.
- 41.5, after 2 seconds
  - 20 metres a second for 2 seconds, plus the 1.5 m it started at.
- 81.5, after 4 seconds
  - The ball keeps going up for as long as we watch.
```

The greatest is `21.5` m, after 2 seconds, and after 4 seconds the ball is
back at 1.5 m, the height of the hand it left. Is 2 seconds the top, or
only the highest of the five times we asked about? The last stage of this
page answers that.

## The highest power

The *degree* of a polynomial is the highest power of $x$ with a
coefficient that is not 0. The ball's polynomial has degree 2.

Can you give `Polynomial` a `degree()` method? Before you start: what is
the degree of `Polynomial([1, 2, 0])`?

```python exec
id: the-highest-power-1
class Polynomial:
    def __init__(self, coefficients):
        self._coefficients = coefficients

    def evaluate(self, x):
        total = 0
        for power in range(len(self._coefficients)):
            total = total + self._coefficients[power] * x ** power
        return total

height = Polynomial([1.5, 20, -5])
print(height.degree())
```

```inputs
Polynomial([1.5, 20, -5]).degree()
Polynomial([1, 2, 0]).degree()
Polynomial([7]).degree()
```

```hint
`Polynomial([1, 2, 0])` is $0x^2 + 2x + 1$, which is $2x + 1$. Is its
highest power 2? Which coefficient should the method look at first, and
which way should it go through the list?
```

```solution
class Polynomial:
    def __init__(self, coefficients):
        self._coefficients = coefficients

    def evaluate(self, x):
        total = 0
        for power in range(len(self._coefficients)):
            total = total + self._coefficients[power] * x ** power
        return total

    def degree(self):
        for power in range(len(self._coefficients) - 1, -1, -1):
            if self._coefficients[power] != 0:
                return power
        return 0

height = Polynomial([1.5, 20, -5])
print(height.degree())
---
2, then 1, then 0. `len(self._coefficients) - 1` gives 2 for
`[1, 2, 0]`, and that is the trap: the zero at the top has to be
skipped. This method starts at the highest power and walks down to the
first coefficient that is not 0. (A polynomial that is all zeros has no
degree at all, strictly. Returning 0 keeps it simple here.)
```

## A rule for the coefficients

Zeros at the top of the list are a nuisance. `degree()` had to walk past
them, and every method we write later would have to remember them too.
Encapsulation offers a better place for the rule: `__init__`, which every
polynomial passes through once. If it removes the zeros at the top, every
other method can trust the list, and `degree()` is one line.

There is a second thing `__init__` should do, and it is harder to see.
With `__init__` as it is, what will this print?

```python exec
id: a-rule-for-the-coefficients-1
class Polynomial:
    def __init__(self, coefficients):
        self._coefficients = coefficients

    def degree(self):
        for power in range(len(self._coefficients) - 1, -1, -1):
            if self._coefficients[power] != 0:
                return power
        return 0

numbers = [1.5, 20, -5]
height = Polynomial(numbers)
numbers.append(3)
print(height.degree())
```

```predict
type: number

What will it print?
```

It prints `3`. The caller never touched `_coefficients`, and still changed
the polynomial. `numbers` and `self._coefficients` are two names for one
list, as in
[Comprehensions, grids and aliasing](tutorial:comprehensions-and-grids),
so a change through one name is a change through both. `list(coefficients)`
makes a copy that belongs to the polynomial alone. Here is `__init__` with
both rules:

```python exec
id: a-rule-for-the-coefficients-2
{{include: setup/polynomial/tidy.py}}

numbers = [1, 2, 0]
tidy = Polynomial(numbers)
numbers.append(3)
print(tidy.degree())
print(numbers)
```

It prints `1`, then `[1, 2, 0, 3]`. The polynomial dropped its own zero
and kept its own copy, and the caller's list is untouched by either. The
`while` loop removes the top coefficient for as long as it is 0, but never
the last one left, so `Polynomial([0])` is still a polynomial: the one that
is 0 everywhere.

## Printing it the way we write it

`print(height)` shows the long memory form. Can you give `Polynomial` a
`__str__` that shows it the way we write it: `-5x^2 + 20x + 1.5`? A
computer usually writes $x^2$ as `x^2`, since it cannot raise the 2.

This one has no top. A first version might show every term, as
`-5x^2 + 20x^1 + 1.5x^0`. Then take the cases one at a time: leave out a
term whose coefficient is 0; write `x^1` as `x`, and leave `x^0` out;
write `- 5` in place of `+ -5`; and write `x^2`, not `1x^2`.

```python exec
id: printing-it-the-way-we-write-it-1
{{include: setup/polynomial/tidy.py}}

height = Polynomial([1.5, 20, -5])
print(height)
```

```inputs
str(Polynomial([1.5, 20, -5]))
str(Polynomial([-1, 0, 1]))
str(Polynomial([3, -1, 0, 2]))
str(Polynomial([0]))
```

```hint
Build the text in a variable, starting from `""`, one term at a time,
from the highest power down. For each term, which sign goes in front
depends on two things: is the coefficient below 0, and is the text still
empty?
```

```solution
{{include: setup/polynomial/printed.py}}

height = Polynomial([1.5, 20, -5])
print(height)
---
`-5x^2 + 20x + 1.5`, `x^2 - 1`, `2x^3 - x + 3` and `0`. `abs()` gives a
number without its sign, so the sign is written once, as `-` or `+`, and
the number after it is always the size. `__str__` asks `self.degree()`
where to start, and trusts the rule in `__init__` that there is no zero at
the top.
```

## Polynomials that make polynomials

Two polynomials can be added: add the coefficients of each power. Can you
give `Polynomial` an `add(other)` method that returns a new polynomial,
and leaves both of the old ones as they were?

```python exec
id: polynomials-that-make-polynomials-1
{{include: setup/polynomial/printed.py}}

first = Polynomial([1, 2, 3])
second = Polynomial([0, 0, -3])
print(first.add(second))
```

```inputs
str(Polynomial([1, 2, 3]).add(Polynomial([0, 0, -3])))
str(Polynomial([1, 2]).add(Polynomial([0, 0, 3])))
Polynomial([1, 2, 3]).add(Polynomial([0, 0, -3])).degree()
```

```hint
The two lists may not be the same length. What can you add to the end of
the shorter one, without changing the polynomial it describes?
```

```solution
{{include: setup/polynomial/added.py}}

first = Polynomial([1, 2, 3])
second = Polynomial([0, 0, -3])
print(first.add(second))
---
`2x + 1`. The two $x^2$ terms cancel, and the answer's degree is 1, not 2,
because `add` returns `Polynomial(total)`, and the new polynomial's own
`__init__` removes the zero at the top. A method can make a new object of
its own class, and that object keeps the same rules.
```

If you have met derivatives in
[Derivatives: the rate of change of a curve](tutorial:rates-of-change),
there is one more method to write. By the power rule, the derivative of
$ax^n$ is $nax^{n-1}$. Can you give `Polynomial` a `derivative()` method
that returns the derivative as a new polynomial? The ball is highest when
its height stops growing, which is where the derivative is 0. When is
that?

```python exec
id: polynomials-that-make-polynomials-2
{{include: setup/polynomial/added.py}}

height = Polynomial([1.5, 20, -5])
speed = height.derivative()
print(speed)
print(speed.evaluate(2))
```

```inputs
str(Polynomial([1.5, 20, -5]).derivative())
Polynomial([1.5, 20, -5]).derivative().evaluate(2)
str(Polynomial([7]).derivative())
```

```hint
The coefficient of $x^1$ in the derivative comes from the coefficient of
$x^2$ in the polynomial, times 2. Which power of the polynomial gives the
derivative's $x^0$? And which power gives nothing at all?
```

```solution
{{include: setup/polynomial/added.py}}

    def derivative(self):
        slopes = []
        for power in range(1, len(self._coefficients)):
            slopes.append(power * self._coefficients[power])
        if slopes == []:
            slopes = [0]
        return Polynomial(slopes)

height = Polynomial([1.5, 20, -5])
speed = height.derivative()
print(speed)
print(speed.evaluate(2))
---
`-10x + 20`, and `0` at 2 seconds. So the ball is highest at exactly 2
seconds, at 21.5 m, which answers the question from the first stage. The
derivative of a number on its own is 0, so a polynomial of degree 0 gives
`Polynomial([0])`.
```

## Looking back

Which decision made the most methods easier to write? And which method
was the hardest to get exactly right? If you worked with a partner, did
you agree?

A challenge: Python calls `__add__` for `+`, the way it calls `__str__`
for `print()`. Can you make `height + Polynomial([-1.5])` work, using the
`add` you already have? And can you write `multiply(other)`? Each term of
one polynomial multiplies each term of the other, and the powers add.

```python challenge
# Your Polynomial class from this page goes here.

height = Polynomial([1.5, 20, -5])
print(height + Polynomial([-1.5]))
print(Polynomial([1, 1]).multiply(Polynomial([-1, 1])))
```

Next, [Designing classes: from a description to classes](tutorial:from-a-description-to-classes)
starts where a real program starts: with a description in words, and no
code at all.

## Where to read more

Everything here is covered elsewhere too, often in a form that will suit you
better than this one.

Downey, A. B. (2015). *Think Python: How to Think Like a Computer
Scientist* (2nd ed.). Green Tea Press. Free at
<https://greenteapress.com/wp/think-python-2e/>. Section 17.7, "Operator
overloading", shows `__add__` at work on a class of its own.

Python Software Foundation. *The Python Language Reference*, section 3.3.8,
"Emulating numeric types".
<https://docs.python.org/3/reference/datamodel.html#emulating-numeric-types>.
Every method like `__add__` that Python calls for an operator, for when
the challenge wants more.
