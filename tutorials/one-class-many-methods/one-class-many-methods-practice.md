---
title: "Reusable methods: one class that does many jobs — Practice"
practice_for: one-class-many-methods
year: "2026-2027"
version: 2026.09.04.1
---

# Reusable methods: one class that does many jobs — Practice

The answers are hidden in folds under each problem. A few problems ask
you to predict what a piece of code prints. Try to answer before you
run anything. Being wrong and finding out why teaches you more than
being right by luck.

## From loose functions to one class

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

**1.** In the cell above, create a `Polynomial` for $x^2 - 4$, called
`difference_of_squares`. Its coefficients are `[-4, 0, 1]`. Predict
`difference_of_squares.evaluate(2)` before you run it.

<details class="dl-answer"><summary>answer</summary>

It prints `0`, because $2^2 - 4 = 0$.

```python
difference_of_squares = Polynomial([-4, 0, 1])
print(difference_of_squares.evaluate(2))
```

</details>

**2.** Two `Polynomial` objects, `quadratic` and
`difference_of_squares`, exist at the same time. Why does
`quadratic.evaluate(2)` never need to be told which coefficients to use?

<details class="dl-answer"><summary>answer</summary>

`evaluate()` is called *on* `quadratic`. So inside it, `self` is that
one object, and `self.coeffs` is its own list. The same call on
`difference_of_squares` reads a different `self.coeffs`. Nothing in the
method has to change.

</details>

**3.** Before `Polynomial` existed, `evaluate(coeffs, x)` took the
coefficient list as a parameter. Once a program tracks several
polynomials, what problem does that cause? Why does the class version
not have it?

<details class="dl-answer"><summary>answer</summary>

Every call has to be given the right list by name, as in
`evaluate(quadratic, 2)` and `evaluate(cubic, 2)`. If you pass the wrong
one by mistake, the function has no way to notice. The class version
cannot mix them up, because each object has only its own coefficients
to read.

</details>

## Giving it more to do

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

**4.** Predict `degree()` and `leading_coefficient()` for
`Polynomial([5, 0, 0, 0, -1])` before you run it.

<details class="dl-answer"><summary>answer</summary>

`4` and `-1`. The list has five items, at indexes 0 to 4, so the highest
power is $x^4$. Its coefficient is the last item in the list, `-1`.

</details>

**5.** Add a `num_terms()` method. It should return how many of a
`Polynomial`'s coefficients are not zero. For `Polynomial([5, 0, 0, 0, -1])`
it should return `2`.

<details class="dl-answer"><summary>answer</summary>

```python
def num_terms(self):
    count = 0
    for coeff in self.coeffs:
        if coeff != 0:
            count = count + 1
    return count
```

It needs nothing except `self`, like `degree()` and
`leading_coefficient()`. Every new method reaches `self.coeffs` in the
same way the first one did.

</details>

**6.** In your own words, what does "modular, reusable code" mean for
`Polynomial`? Use `degree()` as your example.

<details class="dl-answer"><summary>answer</summary>

`degree()` works on any `Polynomial` object, using the coefficients
that object already carries. We did not change `degree()` to make it
work on `cubic` instead of `quadratic`. The object it is called on
supplies the data.

</details>

## Data that belongs together

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

**7.** Predict the two lines of output before you run the cell.

<details class="dl-answer"><summary>answer</summary>

`cost at x=3: 56`, because $50 + 2(3) = 56$.

`height at x=3: 15`, because $20(3) - 5(3)^2 = 60 - 45 = 15$.

</details>

**8.** Create a third `Polynomial`, called `profit`, with your own
coefficients and label. Add it to the list in the loop above. Do all
three print correctly?

<details class="dl-answer"><summary>answer</summary>

```python
profit = Polynomial([-20, 3], "profit")

for polynomial in [cost, height, profit]:
    print(polynomial.label, "at x=3:", polynomial.evaluate(3))
```

The loop itself does not change. It was never written for exactly two
polynomials. It runs its body once for each item in whatever list it is
given.

</details>

**9.** Without the `label` field, `cost` and `height` would need two
separate lists kept in step by hand: one of coefficients and one of
labels. What can go wrong with two lists like that? How does one list of
`Polynomial` objects avoid it?

<details class="dl-answer"><summary>answer</summary>

The two lists must stay the same length and in the same order, and
nothing in the code makes sure of that. Suppose you add a new polynomial
to one list and forget the other. A label now sits next to the wrong
coefficients, and no error tells you. Sorting one list but not the other
breaks it just as quietly.

A list of `Polynomial` objects avoids this. Each object carries its own
label and its own coefficients, so they cannot come apart.

</details>
