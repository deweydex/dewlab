---
title: "One Class, Many Methods — Practice"
slug: one-class-many-methods-practice
practice_for: one-class-many-methods
module: fundamentals-of-oop
module_title: "Fundamentals of Object Oriented Programming"
year: "2026-2027"
series: programming-with-objects
version: 2026.09.04.1
---

# One Class, Many Methods — Practice

Answers are folded. A few of these ask you to predict an output before
running anything. Resist checking first — being wrong and finding out why
is worth more than being right by accident.

## From Loose Functions to One Class

```python exec
id: from-loose-functions-to-one-class-1
class Polynomial:
    def __init__(self, coeffs):
        self.coeffs = coeffs

    def evaluate(self, x):
        result = 0
        for i in range(len(self.coeffs)):
            result = result + self.coeffs[i] * x ** i
        return result


quadratic = Polynomial([-2, 5, 3])
print(quadratic.evaluate(1))
```

**1.** Create a `Polynomial` for $x^2 - 4$ above (coefficients `[-4, 0,
1]`), called `difference_of_squares`. Predict `difference_of_squares.evaluate(2)`
before running it.

<details class="dl-answer"><summary>answer</summary>

`0`. $2^2 - 4 = 0$.

```python
difference_of_squares = Polynomial([-4, 0, 1])
print(difference_of_squares.evaluate(2))
```

</details>

**2.** Two `Polynomial` objects, `quadratic` and `difference_of_squares`,
both exist at once. Why does `quadratic.evaluate(2)` never need to be told
which coefficients to use?

<details class="dl-answer"><summary>answer</summary>

Because `evaluate()` is called *on* `quadratic`, `self` inside it refers to
that one object, and `self.coeffs` is already sitting there. The same
method call on `difference_of_squares` would read a completely different
`self.coeffs`, with nothing in the method itself needing to change.

</details>

**3.** Before `Polynomial` existed, `evaluate(coeffs, x)` took the
coefficient list as a parameter. What problem does that create once a
program tracks several polynomials, that the class version does not have?

<details class="dl-answer"><summary>answer</summary>

Every call has to be handed the right list by name: `evaluate(quadratic,
2)`, `evaluate(cubic, 2)`. Passing the wrong one by mistake is a bug the
function itself has no way to catch. `Polynomial.evaluate()` has no such
mix-up to make, since each object only ever has its own coefficients to
read.

</details>

## Giving It More to Do

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
print(cubic.degree(), cubic.leading_coefficient())
```

**4.** Predict `degree()` and `leading_coefficient()` for `Polynomial([5,
0, 0, 0, -1])` before running it.

<details class="dl-answer"><summary>answer</summary>

`4` and `-1`. Four coefficients above index 0 means the highest power is
$x^4$, and the coefficient attached to it, the last entry in the list, is
`-1`.

</details>

**5.** Add a `num_terms()` method, returning how many of a `Polynomial`'s
coefficients are not zero. `Polynomial([5, 0, 0, 0, -1])` should report
`2`.

<details class="dl-answer"><summary>answer</summary>

```python
def num_terms(self):
    count = 0
    for coeff in self.coeffs:
        if coeff != 0:
            count = count + 1
    return count
```

Needs nothing beyond `self`, the same shape as `degree()` and
`leading_coefficient()` above it. Every new method reaches `self.coeffs`
the same way the first one did.

</details>

**6.** In your own words: what does "modular, reusable code" mean for
`Polynomial`, using `degree()` as the example?

<details class="dl-answer"><summary>answer</summary>

`degree()` works on any `Polynomial` object, using whatever coefficients
that particular object already carries. Nothing about `degree()` itself
needed to change to work on `cubic` instead of `quadratic` — the object it
is called on supplies the rest.

</details>

## Data That Belongs Together

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


cost = Polynomial([50, 2], "cost")
height = Polynomial([0, 20, -5], "height")

for polynomial in [cost, height]:
    print(polynomial.label, "at x=3:", polynomial.evaluate(3))
```

**7.** Predict the cell's two lines of output before running it.

<details class="dl-answer"><summary>answer</summary>

`cost at x=3: 56` — $50 + 2(3) = 56$.

`height at x=3: 15` — $20(3) - 5(3)^2 = 60 - 45 = 15$.

</details>

**8.** Create a third `Polynomial`, `profit`, with your own coefficients
and label. Add it to the list in the loop above and confirm all three
print correctly.

<details class="dl-answer"><summary>answer</summary>

```python
profit = Polynomial([-20, 3], "profit")

for polynomial in [cost, height, profit]:
    print(polynomial.label, "at x=3:", polynomial.evaluate(3))
```

Nothing about the loop itself changes. It was never written to expect
exactly two polynomials, only to run its body once per item in whatever
list it is given.

</details>

**9.** Before `label` was added, `cost` and `height` would have needed two
separate lists kept in step by hand: one of coefficients, one of labels.
What goes wrong with two lists like that, that a single list of
`Polynomial` objects avoids?

<details class="dl-answer"><summary>answer</summary>

The two lists have to stay the same length and in the same order by
convention alone — nothing enforces it. Insert a new polynomial into one
list and forget the other. A label ends up next to the wrong coefficients,
with no error to say so. Sorting one list without sorting the other the
same way breaks it just as quietly.

</details>
