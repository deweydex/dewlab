---
title: "One Class, Many Methods"
slug: one-class-many-methods
module: fundamentals-of-oop
module_title: "Fundamentals of Object Oriented Programming"
year: "2026-2027"
series: programming-with-objects
version: 2026.09.04.1
covers:
  from-loose-functions-to-one-class:
    covers: [FOOP-LO4]
  giving-it-more-to-do:
    covers: [FOOP-LO4]
  data-that-belongs-together:
    covers: [FOOP-LO8]
---

# One Class, Many Methods

**Fundamentals of Object Oriented Programming**

*Expressions Come Alive* represented a polynomial as a list of
coefficients. Index `i` holds the coefficient of $x^i$, so $3x^2 + 5x - 2$
becomes `[-2, 5, 3]`. *Objects and Classes* wrapped one piece of data and
one operation together, as a class. This tutorial asks what happens once
there is more than one operation to wrap.

## From Loose Functions to One Class

Here is a polynomial and a function that evaluates it, the way you already
know how to write one.

```python exec
id: from-loose-functions-to-one-class-1
def evaluate(coeffs, x):
    result = 0
    for i in range(len(coeffs)):
        result = result + coeffs[i] * x ** i
    return result

quadratic = [-2, 5, 3]   # 3x^2 + 5x - 2
print(evaluate(quadratic, 1))
print(evaluate(quadratic, 4))
```

A program that tracks two polynomials needs two lists, and `evaluate()`
has to be given the right one every time.

```python exec
id: from-loose-functions-to-one-class-2
quadratic = [-2, 5, 3]    # 3x^2 + 5x - 2
cubic = [1, 0, -3, 2]     # 2x^3 - 3x^2 + 1

print(evaluate(quadratic, 2))
print(evaluate(cubic, 2))
```

This is the same shape of problem *Objects and Classes* found in a bank
balance. We can fix it the same way: wrap the coefficients and the
operation on them into one class.

```python exec
id: from-loose-functions-to-one-class-3
class Polynomial:
    def __init__(self, coeffs):
        self.coeffs = coeffs

    def evaluate(self, x):
        result = 0
        for i in range(len(self.coeffs)):
            result = result + self.coeffs[i] * x ** i
        return result

quadratic = Polynomial([-2, 5, 3])
cubic = Polynomial([1, 0, -3, 2])

print(quadratic.evaluate(2))
print(cubic.evaluate(2))
```

`quadratic` and `cubic` each carry their own coefficients. Neither
`evaluate()` call needs to be told which list to use — it already knows,
because it is being asked of one particular object.

### Your turn

Create a `Polynomial` for $x^2 - 1$ below (the coefficients are `[-1, 0,
1]`), then evaluate it at a few values of your own choosing.

```python exec
id: from-loose-functions-to-one-class-4
class Polynomial:
    def __init__(self, coeffs):
        self.coeffs = coeffs

    def evaluate(self, x):
        result = 0
        for i in range(len(self.coeffs)):
            result = result + self.coeffs[i] * x ** i
        return result

# Create your own Polynomial here, and evaluate it at a few values
```

## Giving It More to Do

A polynomial has more than one useful question to answer. Its *degree* is
the highest power in it — two for a quadratic, three for a cubic. Its
*leading coefficient* is the coefficient attached to that highest power.
Both are easy to add as methods, once the coefficients already live on
`self`.

```python exec
id: giving-it-more-to-do-1
class Polynomial:
    def __init__(self, coeffs):
        self.coeffs = coeffs

    def evaluate(self, x):
        result = 0
        for i in range(len(self.coeffs)):
            result = result + self.coeffs[i] * x ** i
        return result

    def degree(self):
        return len(self.coeffs) - 1

    def leading_coefficient(self):
        return self.coeffs[-1]

cubic = Polynomial([1, 0, -3, 2])
print(cubic.degree())
print(cubic.leading_coefficient())
```

Notice what did not have to change. `degree()` and `leading_coefficient()`
needed no new parameter for the coefficients, and no care at the call site
about which polynomial's list to pass. Both already have `self`, and
`self.coeffs` is right there. This is what "modular, reusable code" means
for a class. Every new capability is a method that can call on everything
the object already carries. A stand-alone function has no such luck — it
needs the same data handed to it all over again.

### Your turn

Add a `constant_term()` method below, returning the coefficient of $x^0$
— the value a polynomial takes when $x$ is 0. Then try it on a
`Polynomial` of your own.

```python exec
id: giving-it-more-to-do-2
class Polynomial:
    def __init__(self, coeffs):
        self.coeffs = coeffs

    def evaluate(self, x):
        result = 0
        for i in range(len(self.coeffs)):
            result = result + self.coeffs[i] * x ** i
        return result

    def degree(self):
        return len(self.coeffs) - 1

    def leading_coefficient(self):
        return self.coeffs[-1]

    # Add a constant_term method here

my_polynomial = Polynomial([-1, 0, 1])
# Try constant_term() on it
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. `constant_term()` needs no parameters beyond `self` — the same shape
   as `degree()` and `leading_coefficient()` above it.
2. The coefficient of $x^0$ is the first entry in the list, at index 0.
3. Compare your answer against `evaluate(0)` on the same polynomial. They
   should always agree: every term except the constant one multiplies by
   a positive power of 0, which is 0 itself, so only the constant term
   survives.

**Think about:** could `constant_term()` have been written as
`self.evaluate(0)` instead of reading `self.coeffs[0]` directly? Try it
and see if it gives the same answer.

</details>

## Data That Belongs Together

A `Polynomial` so far carries one field: its coefficients. A field can be
anything else a program needs tracked alongside it, too. Suppose a
program keeps several polynomials at once — a company's cost function, a
projectile's height over time. Each one needs its own label kept right
next to its own coefficients.

```python exec
id: data-that-belongs-together-1
class Polynomial:
    def __init__(self, coeffs, label):
        self.coeffs = coeffs
        self.label = label

    def evaluate(self, x):
        result = 0
        for i in range(len(self.coeffs)):
            result = result + self.coeffs[i] * x ** i
        return result

cost = Polynomial([50, 2], "cost")           # 2x + 50
height = Polynomial([0, 20, -5], "height")   # -5x^2 + 20x

for polynomial in [cost, height]:
    print(polynomial.label, "at x=3:", polynomial.evaluate(3))
```

Run that and notice what the loop does not need: a second list of labels,
kept in step by hand with a first list of coefficients. Each
`Polynomial` object already carries both, so asking for one's label and
its coefficients together is just asking that one object. *Objects and
Classes* introduced a field as one piece of data. Here the same idea
applies to more than one piece, on the same object at once.

### Your turn

Create two `Polynomial` objects of your own, each with a coefficient list
and a label. Put them in a list and, like the cell above, print each
one's label alongside its `degree()`.

```python exec
id: data-that-belongs-together-2
class Polynomial:
    def __init__(self, coeffs, label):
        self.coeffs = coeffs
        self.label = label

    def evaluate(self, x):
        result = 0
        for i in range(len(self.coeffs)):
            result = result + self.coeffs[i] * x ** i
        return result

    def degree(self):
        return len(self.coeffs) - 1

# Create two Polynomial objects here, then print each label and degree
```

## Wrapping Up

In this tutorial:

- Wrapping data and an operation into a class scales past one operation.
  A method added later reaches `self`'s fields the same way the first one
  did, with nothing new to pass in.
- That is what makes a method *reusable* in the object oriented sense: it
  works on any object of its class, using whatever that particular object
  already carries.
- A class's fields are not limited to the one piece of data it started
  with. Two fields that belong together — coefficients and a label, a
  balance and an owner — travel together automatically once they live on
  the same object.

### Reflection

A few sentences about this tutorial, whenever you are ready. Which method
felt most natural to add once `Polynomial` already existed?

Double-click this cell to write your thoughts:

## Where to Read More

Downey, A. B. (2015). *Think Python: How to Think Like a Computer
Scientist* (2nd ed.). Green Tea Press. Chapter 16 covers classes with
several methods and fields, continuing from where chapter 15 left off.
Free at <https://greenteapress.com/wp/think-python-2e/>.

Python Software Foundation. *The Python Tutorial*, section 9.3.5: Class
and Instance Variables. <https://docs.python.org/3/tutorial/classes.html#class-and-instance-variables>.
The official reference on what belongs on `self` and why.
