---
title: "Sequence, selection and iteration inside a class"
year: "2026-2027"
version: 2026.09.05.1
covers:
  the-handful-of-moves:
    covers: [FOOP-LO2]
  the-same-moves-inside-a-class:
    covers: [FOOP-LO2]
  one-method-several-moves:
    covers: [FOOP-LO2]
---

# Sequence, selection and iteration inside a class

In [Classes and objects: keeping data and actions together](tutorial:objects-and-classes)
we built our first classes. A class can look like a whole new way of
writing code. It is not. The code inside a class is built from the same
small set of moves you used in the Programming Foundations series:

| Move | What it does | Example |
|---|---|---|
| storing | keeps a value under a name | `total = 0` |
| sequence | runs lines in the order they are written | one line, then the next |
| selection | chooses between paths | `if amount >= 0:` |
| iteration | repeats a step | `for amount in amounts:` |

This page does not teach those moves again. It finds them inside a
class: in the constructor, and in the methods.

## The handful of moves

Here is a small program with no class in it at all. It adds up a running
total, using only the moves you already know. Which lines store a value,
which choose, and which repeat? What do you think it prints? Run it to
check.

```python exec
id: the-handful-of-moves-1
amounts = [40, -5, 25, 10]
total = 0

for amount in amounts:
    if amount >= 0:
        total = total + amount

print(total)
```

It prints `75`. All four moves are here, each doing its usual job.

- `total = 0` stores a value.
- `for amount in amounts:` repeats a step once for each amount. An
  *iteration* is a program repeating a step, usually with a loop.
- `if amount >= 0:` chooses between two paths, so `-5` is skipped. A
  *selection* is a program choosing between paths, usually with an `if`
  statement.
- The lines run in the order they are written. A *sequence* is a
  program's lines running one after another, in that order.

Nothing here is new. Every program you have written so far is built from
these same moves.

## The same moves, inside a class

A class does not remove any of these four moves. It gives them a new
place to live: inside the constructor, `__init__`, and inside the
methods. Both reach the object's own data through `self`.

The `Basket` class below stores items in a list. Each item is a name and
a price, written together in brackets as `(name, price)`. A pair like
that is called a *tuple*. A tuple is a fixed group of values kept
together, and here each tuple holds one item's name and price.

Three items are added to the basket, and one has a price of `-5`. What
do you think `basket.items` will hold? Run it to check.

```python exec
id: the-same-moves-inside-a-class-1
class Basket:
    def __init__(self):
        self.items = []

    def add(self, name, price):
        if price >= 0:
            self.items.append((name, price))

basket = Basket()
basket.add("bread", 2.50)
basket.add("milk", 1.80)
basket.add("mistake", -5)

print(basket.items)
```

```hint
after: 3 identical errors
Which of the four moves is the line the error points at doing: storing a
value, choosing a path, or repeating a step? If Python says it cannot find
a name, is `self.` in front of that name where the class stores it, and is
it missing where the error is?
```

Two of the three items are in the list. Where are the moves?

- `self.items = []` stores a value, like `total = 0` did above. This
  time the value lives on the object, as a field, instead of in a plain
  variable.
- `if price >= 0:` inside `add()` is the same selection as before. Now
  it decides whether *this object's* list should grow. The item priced
  `-5` never gets in.

## One method, several moves

A single method can use more than one of these moves, in the same way a
plain function can. The `total()` method below adds up the prices in the
basket. Which move does each line of `total()` use? What will it print?

```python exec
id: one-method-several-moves-1
class Basket:
    def __init__(self):
        self.items = []

    def add(self, name, price):
        if price >= 0:
            self.items.append((name, price))

    def total(self):
        running_total = 0
        for name, price in self.items:
            running_total = running_total + price
        return running_total

basket = Basket()
basket.add("bread", 2.50)
basket.add("milk", 1.80)

print(basket.total())
```

It prints `4.3`. `total()` first stores a value, `running_total = 0`.
Then it repeats a step once for each item in the basket, adding that
item's price. That is iteration. The line
`for name, price in self.items:` takes each tuple apart into two
variables, `name` and `price`, one item at a time.

This is the pattern from the first cell on this page: store a value,
then repeat. The only difference is that it is now written as a method.

So what does object oriented programming add to these four moves? It
adds a place to put them: inside a class, reached through `self`. Each
object then keeps its own copy of whatever it stores. It does not add a
fifth move to learn. Every method you write from here on is still
built from storing, sequence, selection and iteration.

Next,
[Encapsulation: keeping an object's data behind its methods](tutorial:keeping-details-inside-an-object)
uses selection inside methods to protect an object's data.
