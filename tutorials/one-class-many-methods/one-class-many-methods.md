---
title: "Reusable methods: one class that does many jobs"
year: "2026-2027"
version: 2026.09.04.1
covers:
  from-loose-functions-to-one-class:
    covers: [FOOP-LO4]
  giving-it-more-to-do:
    covers: [FOOP-LO4]
  data-that-belongs-together:
    covers: [FOOP-LO8]
---

# Reusable methods: one class that does many jobs

So far our classes have had only a few methods. What happens when a
class has many jobs to do? On this page we build one class step by
step, and give it a new method each time.

The class is for polynomials. A *polynomial* is a sum of terms, where
each term is a number times a power of $x$. For example, $3x^2 + 5x - 2$
is a polynomial. The number in front of each power is its
*coefficient*: here, 3, 5 and −2.

We can store a polynomial as a list of its coefficients. The item at
index `i` is the coefficient of $x^i$. So $3x^2 + 5x - 2$ becomes
`[-2, 5, 3]`: first the number on its own ($x^0$), then $x^1$, then
$x^2$. If you have done
[Expressions Come Alive](tutorial:expressions-come-alive), you have
seen this list before.

## From loose functions to one class

Here is a polynomial and a function that works out its value for a
given $x$, written the way you already know. What do you think the two
lines print? Run it to check.

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

It prints `6` and `66`. For $x = 1$: $3 + 5 - 2 = 6$.

A program that tracks two polynomials needs two lists. Each time we call
`evaluate()`, we have to give it the right one.

```python exec
id: from-loose-functions-to-one-class-2
quadratic = [-2, 5, 3]    # 3x^2 + 5x - 2
cubic = [1, 0, -3, 2]     # 2x^3 - 3x^2 + 1

print(evaluate(quadratic, 2))
print(evaluate(cubic, 2))
```

This is the same problem we met with bank balances in
[Classes and objects: keeping data and actions together](tutorial:objects-and-classes).
We can fix it the same way. We put the coefficients and the operation on
them together, in one class.

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

`quadratic` and `cubic` each carry their own coefficients. Neither call
to `evaluate()` needs to be told which list to use. Each call is made on
one particular object, and `self.coeffs` is that object's own list.

### Your turn

1. Create a `Polynomial` for $x^2 - 1$ in the cell below. Its
   coefficients are `[-1, 0, 1]`.
2. Evaluate it at a few values of $x$ that you choose.
3. Can you find a value of $x$ where it gives `0`?

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

## Giving it more to do

A polynomial can answer more than one useful question.

- Its *degree* is the highest power of $x$ in it. A quadratic has
  degree 2, and a cubic has degree 3.
- Its *leading coefficient* is the coefficient of that highest power.

Once the coefficients live on `self`, both are short methods. What do
you think this cell prints for the cubic $2x^3 - 3x^2 + 1$?

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

It prints `3`, then `2`.

Look at what did not have to change. `degree()` and
`leading_coefficient()` needed no new parameter for the coefficients.
The call `cubic.degree()` does not pass in a list at all. Both methods
already have `self`, and `self.coeffs` is there for them.

This is what *reusable* code means for a class. Each new job is a
method that can use everything the object already carries. A method
written once works on every object of its class. A stand-alone function
cannot do that. It needs the same data given to it every time.

### Your turn

1. Add a `constant_term()` method to the class below. It should return
   the coefficient of $x^0$. That is the value a polynomial takes when
   $x$ is 0.
2. Try it on `my_polynomial`, or on a `Polynomial` of your own.

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

1. `constant_term()` needs no parameters except `self`. It has the same
   shape as `degree()` and `leading_coefficient()` above it.
2. The coefficient of $x^0$ is the first entry in the list, at index 0.
3. Compare your answer with `evaluate(0)` on the same polynomial. They
   should always agree. Every term except the constant one is multiplied
   by a positive power of 0, such as $0^1$ or $0^2$, and each of those
   is 0. So only the constant term is left.

**Think about:** could `constant_term()` return `self.evaluate(0)`
instead of reading `self.coeffs[0]`? Try it. Does it give the same
answer?

</details>

## Data that belongs together

So far a `Polynomial` has one field, its coefficients. An object can
carry as many fields as a program needs.

Suppose a program keeps several polynomials at once: a company's costs,
and the height of a ball thrown in the air. Each one needs a label, and
the label must stay with the right coefficients. Here, the constructor
takes a label too. Predict the two lines of output, then run it to
check.

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

Now look at what the loop does not need. There is no second list of
labels to keep in step with a list of coefficients. Each `Polynomial`
object carries both. To get one polynomial's label and its value
together, we ask that one object.

`BankAccount`, on the
[Classes and objects](tutorial:objects-and-classes) page, already had
two fields: an owner and a balance. The same idea works for any data
that belongs together. Put it on the same object, and it stays together.

### Your turn

1. Create two `Polynomial` objects of your own in the cell below. Give
   each one a list of coefficients and a label.
2. Put the two objects in a list.
3. Loop over the list, as the cell above does. For each one, print its
   label and its `degree()`.

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

## Wrapping up

On this page:

- Putting data and its operations into a class works for many
  operations, not only one. A method added later uses the fields on
  `self` in the same way the first method did, with nothing new to pass
  in.
- That is what makes a method *reusable*: it works on any object of its
  class, using the data that object already carries.
- An object can have as many fields as it needs. Fields that belong
  together, such as coefficients and a label, or a balance and an owner,
  stay together once they live on the same object.

### Reflection

Write a few sentences about this page, whenever you are ready. Once
`Polynomial` existed, which method felt most natural to add?

Double-click this cell to write your thoughts:

## Where to Read More

Downey, A. B. (2015). *Think Python: How to Think Like a Computer
Scientist* (2nd ed.). Green Tea Press. Chapter 16 covers classes with
several methods and fields, continuing from where chapter 15 left off.
Free at <https://greenteapress.com/wp/think-python-2e/>.

Python Software Foundation. *The Python Tutorial*, section 9.3.5: Class
and Instance Variables. <https://docs.python.org/3/tutorial/classes.html#class-and-instance-variables>.
The official reference on what belongs on `self` and why.
