---
title: "The Moves You Already Know"
slug: the-moves-you-already-know
module: fundamentals-of-oop
module_title: "Fundamentals of Object Oriented Programming"
year: "2026-2027"
series: programming-with-objects
version: 2026.09.05.1
covers:
  the-handful-of-moves:
    covers: [FOOP-LO2]
  the-same-moves-inside-a-class:
    covers: [FOOP-LO2]
  one-method-several-moves:
    covers: [FOOP-LO2]
---

# The Moves You Already Know

**Fundamentals of Object Oriented Programming**

Object oriented programming sounds, at first, like a whole new way of
writing code. It is not. Every move a program makes still comes from a
small, familiar set. You already know it: storing a value, running
steps in order, choosing between paths, repeating a step. This tutorial
does not teach any of those again. It shows where they go once a
program starts using classes.

## The Handful of Moves

Here is a small program with no class in it at all: a running total,
built from the moves you already have.

```python exec
id: the-handful-of-moves-1
amounts = [40, -5, 25, 10]
total = 0

for amount in amounts:
    if amount >= 0:
        total = total + amount

print(total)
```

All four moves are here, each doing its usual job. `total = 0` stores
a value.
`for amount in amounts:` repeats a step once for each amount, an
*iteration*. `if amount >= 0:` chooses between two paths, a
*selection*. The lines themselves run in the order they are written, a
*sequence*. Nothing here is new. It is the same vocabulary every program
you have written so far is built from.

## The Same Moves, Inside a Class

A class does not remove any of those four moves. It gives them a new
place to live: inside `__init__` and inside a method, both reached
through `self`.

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

`self.items = []` stores a value, just like `total = 0` did above. This
time, though, the value lives on the object instead of in a plain
variable.
`if price >= 0:` inside `add()` is the same selection as before, only
now it decides whether *this object's* list should grow. The item
priced `-5` never made it in.

## One Method, Several Moves

A single method can use more than one of these moves at once, the same
way a plain function could.

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

`total()` stores a value (`running_total = 0`), then repeats a step once
per item in the basket (iteration), adding each price in turn. It
repeats the pattern from this tutorial's very first cell: storing, then
iterating, now written as a method instead of a standalone block.

Object orientation adds one place to put these four moves: inside a
class, reached through `self`. Each object then keeps its own copy of
whatever it stores. It does not add a fifth move to learn. Every method
you write from here on, however it is built, is still storing,
sequencing, choosing, and repeating.
