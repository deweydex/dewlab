---
title: "The Moves You Already Know — Practice"
slug: the-moves-you-already-know-practice
practice_for: the-moves-you-already-know
module: fundamentals-of-oop
module_title: "Fundamentals of Object Oriented Programming"
year: "2026-2027"
series: programming-with-objects
version: 2026.09.05.1
---

# The Moves You Already Know — Practice

Answers are folded. Several of these ask you to predict an output before
running anything. Resist checking first — being wrong and finding out why
is worth more than being right by accident.

## The Handful of Moves

```python exec
id: the-handful-of-moves-1
amounts = [40, -5, 25, 10]
total = 0

for amount in amounts:
    if amount >= 0:
        total = total + amount

print(total)
```

**1.** Change `>=` to `>` above, so `0` itself no longer counts. Predict
the new output before running it. Does it change?

<details class="dl-answer"><summary>answer</summary>

No — still `75`. None of the amounts in the list is exactly `0`, so the
change from `>= 0` to `> 0` never affects which ones pass the check.

</details>

**2.** Add `0` to the `amounts` list and run the cell again with `> 0`
still in place. What happens to the total, and why?

<details class="dl-answer"><summary>answer</summary>

It stays `75`. `0 > 0` is `False`, so the new `0` fails the check and is
skipped — the same as it would be added and change nothing, but here it
never reaches `total` at all.

</details>

**3.** Label each line below with the move it is: *sequence*,
*selection*, or *iteration*.

```python
prices = [12, 0, 8]        # line A
count = 0                  # line B
for price in prices:       # line C
    if price > 0:           # line D
        count = count + 1  # line E
```

<details class="dl-answer"><summary>answer</summary>

Every line runs in *sequence* — that part never stops applying. On top of
that: line C is *iteration* (repeats once per price), and line D is
*selection* (chooses whether line E runs). Lines A, B, and E are each a
single step with nothing to repeat or choose between.

</details>

**4.** Try writing a cell that counts how many numbers in `[3, -1, 4, -2, 5]`
are negative, using the same storing-then-iterating shape as the first
cell in this tutorial.

<details class="dl-answer"><summary>answer</summary>

```python
numbers = [3, -1, 4, -2, 5]
negative_count = 0

for number in numbers:
    if number < 0:
        negative_count = negative_count + 1

print(negative_count)
```

`2`. Same shape as the running total: store a starting value, repeat once
per number, choose whether to act on this one.

</details>

## The Same Moves, Inside a Class

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

**5.** Add a third, valid item to `basket` above — anything you like, at
a positive price. Predict `basket.items` before running.

<details class="dl-answer"><summary>answer</summary>

Whatever you added appears as a third tuple in the list, in the order you
called `add()`. `add()`'s own selection still rejects a negative price,
whatever name you give it.

</details>

**6.** Here is a `Counter` class with a broken `add()` method. What move
is missing, and what goes wrong without it?

```python
class Counter:
    def __init__(self):
        self.total = 0

    def add(self, amount):
        self.total + amount
```

<details class="dl-answer"><summary>answer</summary>

Storing. `self.total + amount` computes a new number and throws it away
— nothing stores it back into `self.total`. It needs to read
`self.total = self.total + amount`, the same store-a-value move as
`total = total + amount` in this tutorial's very first cell.

</details>

**7.** In your own words: what changes about selection when it moves
from a plain function into a method, and what stays the same?

<details class="dl-answer"><summary>answer</summary>

What stays the same: it is still an `if` choosing between two paths. What
changes: the condition and the effect can both now depend on `self` —
this specific object's own price, this object's own list — rather than on
whatever a function's caller happened to pass in.

</details>

## One Method, Several Moves

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

**8.** Add `basket.add("cheese", 3.20)` before the `print()` call and
predict the new total before running it.

<details class="dl-answer"><summary>answer</summary>

`7.5` — `2.50 + 1.80 + 3.20`. `total()` reruns its loop over whatever is
in `self.items` at the moment it is called, cheese included.

</details>

**9.** Try writing a `count()` method for `Basket` that returns how many
items it holds, using iteration the same way `total()` does.

<details class="dl-answer"><summary>answer</summary>

```python
def count(self):
    item_count = 0
    for name, price in self.items:
        item_count = item_count + 1
    return item_count
```

Same shape as `total()`: store a starting value, repeat once per item,
change the stored value each time. `len(self.items)` would do the same
job in one call, but this is the same storing-then-iterating pattern
practised throughout this tutorial.

</details>

**10.** In your own words: what does object orientation actually add to
the four moves this tutorial covers?

<details class="dl-answer"><summary>answer</summary>

A place to put them — inside a class, reached through `self` — so each
object keeps its own copy of whatever it stores. Not a fifth move. Every
method in every tutorial from here on is still built from the same four.

</details>

