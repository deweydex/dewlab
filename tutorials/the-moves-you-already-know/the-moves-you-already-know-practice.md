---
title: "Sequence, selection and iteration inside a class — Practice"
practice_for: the-moves-you-already-know
year: "2026-2027"
version: 2026.09.05.1
---

# Sequence, selection and iteration inside a class — Practice

The answers are hidden in folds under each problem. Several problems ask
you to predict what a piece of code prints. Try to answer before you
run anything. Being wrong and finding out why teaches you more than
being right by luck.

## The handful of moves

```python exec
id: the-handful-of-moves-1
amounts = [40, -5, 25, 10]
total = 0

for amount in amounts:
    if amount >= 0:
        total = total + amount

print(total)
```

**1.** In the cell above, change `>=` to `>`, so that `0` itself no
longer counts. Predict the new output before you run it. Does it change?

<details class="dl-answer"><summary>answer</summary>

No. It still prints `75`. None of the amounts in the list is exactly
`0`, so changing `>= 0` to `> 0` does not change which amounts pass the
check.

</details>

**2.** Add `0` to the `amounts` list, and keep `> 0` in place. Run the
cell again. What happens to the total, and why?

<details class="dl-answer"><summary>answer</summary>

It stays `75`. `0 > 0` is `False`, so the new `0` fails the check and is
skipped. It never reaches `total` at all. (With `>= 0` it would be
added, but adding `0` changes nothing, so the total would still be
`75`.)

</details>

**3.** Label each line below with the move it uses: sequence,
selection or iteration.

```python
prices = [12, 0, 8]        # line A
count = 0                  # line B
for price in prices:       # line C
    if price > 0:           # line D
        count = count + 1  # line E
```

<details class="dl-answer"><summary>answer</summary>

Every line runs in sequence. That is true of every program, all the
time. On top of that, line C is iteration: it repeats once for each
price. Line D is selection: it chooses whether line E runs. Lines A, B
and E are each a single step, with nothing to repeat or choose. All
three store a value.

</details>

**4.** Write a cell that counts how many numbers in `[3, -1, 4, -2, 5]`
are negative. Use the same shape as the first cell on the tutorial page:
store a starting value, then repeat.

<details class="dl-answer"><summary>answer</summary>

```python
numbers = [3, -1, 4, -2, 5]
negative_count = 0

for number in numbers:
    if number < 0:
        negative_count = negative_count + 1

print(negative_count)
```

It prints `2`. The shape is the same as the running total. Store a
starting value. Repeat once for each number. Choose whether to act on
this one.

</details>

## The same moves, inside a class

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

**5.** Add a third valid item to `basket` above. Choose any name and a
positive price. Predict `basket.items` before you run it.

<details class="dl-answer"><summary>answer</summary>

Your item appears as a third tuple in the list, after bread and milk.
Items appear in the order you called `add()`. The selection inside
`add()` still refuses a negative price, whatever the item's name is.

</details>

**6.** Here is a `Counter` class with a broken `add()` method. Which
move is missing, and what goes wrong without it?

```python
class Counter:
    def __init__(self):
        self.total = 0

    def add(self, amount):
        self.total + amount
```

<details class="dl-answer"><summary>answer</summary>

Storing is missing. `self.total + amount` works out a new number, then
throws it away. Nothing stores it back into `self.total`, so the total
stays at `0`. The line needs to read
`self.total = self.total + amount`. That is the same storing move as
`total = total + amount` in the first cell on the tutorial page.

</details>

**7.** In your own words, what changes about selection when it moves
from a plain function into a method? What stays the same?

<details class="dl-answer"><summary>answer</summary>

What stays the same: it is still an `if` choosing between two paths.

What changes: the condition and its effect can now use `self`, this
particular object's own data, such as its own list. In a plain function
they can use only what the caller passed in.

</details>

## One method, several moves

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

**8.** Add `basket.add("cheese", 3.20)` before the `print()` line.
Predict the new total before you run it.

<details class="dl-answer"><summary>answer</summary>

`7.5`, which is `2.50 + 1.80 + 3.20`. Each time `total()` is called, it
runs its loop again over whatever is in `self.items` at that moment.
This time the cheese is included.

</details>

**9.** Write a `count()` method for `Basket` that returns how many items
it holds. Use iteration, the same way `total()` does.

<details class="dl-answer"><summary>answer</summary>

```python
def count(self):
    item_count = 0
    for name, price in self.items:
        item_count = item_count + 1
    return item_count
```

The shape is the same as `total()`. Store a starting value, repeat once
for each item, and change the stored value each time.
`len(self.items)` would do the same job in one call. The loop is here
to practise the storing-then-repeating pattern from this tutorial.

</details>

**10.** In your own words, what does object oriented programming add
to the four moves on the tutorial page?

<details class="dl-answer"><summary>answer</summary>

It adds a place to put them: inside a class, reached through `self`.
Each object then keeps its own copy of whatever it stores. It does not
add a fifth move. Every method in every tutorial from here on is still
built from the same four.

</details>

