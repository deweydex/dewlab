---
title: "Sorting a list: bubble, insertion and selection sort — Practice"
practice_for: putting-things-in-order
year: "2026-2027"
version: 2026.09.26.1
worlds:
  secret-messages: Codes and hidden messages, the kind spies and puzzle-setters make.
  pixel-art: Pictures made of small squares, the way a screen draws them.
---

# Sorting a list: bubble, insertion and selection sort — Practice

Problems on sorting, and three from earlier pages. Try tracing the short
ones by hand before you run anything. To *trace* a sort is to follow it
step by step on paper, writing down the list after each step. Once you have
traced a sort, you can find the mistakes in it; if you have only run it,
you usually cannot.

## 1. One pass

Trace one full pass of bubble sort over `[5, 1, 4, 2, 8]`. What is the
list after the pass? The cell prints the list after each swap, to check
your trace.

```python exec
id: one-pass-1
items = [5, 1, 4, 2, 8]
for i in range(len(items) - 1):
    if items[i] > items[i + 1]:
        items[i], items[i + 1] = items[i + 1], items[i]
        print(items)
```

<details class="dl-answer"><summary>answer</summary>

`[1, 4, 2, 5, 8]`. 5 is swapped with 1, then 4, then 2, and stops at 8.
The 5 travelled to its place in one pass, which is what "bubbling" means.

</details>

## 2. How many passes

How many passes does bubble sort need on `[5, 1, 4, 2, 8]` before the list
is sorted? How many does a plain bubble sort do?

<details class="dl-answer"><summary>answer</summary>

Two passes sort it: after the second, it is `[1, 2, 4, 5, 8]`. A plain
bubble sort still does all four, because it never checks whether the list
is sorted. Problem 6 fixes that.

</details>

## 3. Insertion, traced

Trace insertion sort over `[3, 1, 4, 1, 5]`. Write down the list after
each element is placed.

<details class="dl-answer"><summary>answer</summary>

Start with `[3]`: one element is always sorted. Insert 1: `[1, 3]`. Insert
4: `[1, 3, 4]`. Insert 1: `[1, 1, 3, 4]`. Insert 5: `[1, 1, 3, 4, 5]`.

The second 1 landed *after* the first. Equal elements keep the order they
started in, and a sort that does that is *stable*. It matters when data is
sorted twice, by two different things, as in problem 12.

</details>

## 4. Selection, traced

Trace selection sort over `[64, 25, 12, 22, 11]`.

<details class="dl-answer"><summary>answer</summary>

1. The smallest is 11. Swap it into place 0: `[11, 25, 12, 22, 64]`.
2. The smallest of the rest is 12: `[11, 12, 25, 22, 64]`.
3. Then 22: `[11, 12, 22, 25, 64]`.
4. Then 25, already in place. The list is sorted.

At most one swap for each place. Selection sort makes the fewest swaps of
the three, which matters when moving an element is slow.

</details>

## 5. Counting comparisons

```python exec
id: counting-comparisons-1
def bubble_counted(items):
    items = items[:]
    comparisons = 0
    for pass_number in range(len(items) - 1):
        for i in range(len(items) - 1 - pass_number):
            comparisons = comparisons + 1
            if items[i] > items[i + 1]:
                items[i], items[i + 1] = items[i + 1], items[i]
    return comparisons

for size in [10, 20, 40, 80]:
    backwards = list(range(size, 0, -1))
    in_order = list(range(1, size + 1))
    print(size, "items:", bubble_counted(backwards), "reversed,",
          bubble_counted(in_order), "in order")
```

How many comparisons does bubble sort make on 10 items? On 20? Does it
matter whether they start in order?

<details class="dl-answer"><summary>answer</summary>

45 and 190, in order or not. It is always n(n − 1)/2: the loops run the
same number of times whatever they find, and only the swaps depend on the
data. Doubling n makes about four times the comparisons.

</details>

## 6. Stop when it is sorted

Can you change `bubble_counted` so that it stops as soon as a pass swaps
nothing, and still returns the number of comparisons?

```python exec
id: stop-when-it-is-sorted-1
def bubble_counted(items):
    items = items[:]
    comparisons = 0
    for pass_number in range(len(items) - 1):
        for i in range(len(items) - 1 - pass_number):
            comparisons = comparisons + 1
            if items[i] > items[i + 1]:
                items[i], items[i + 1] = items[i + 1], items[i]
    return comparisons
```

```inputs
guess: yes
bubble_counted(list(range(10)))          # already in order
bubble_counted(list(range(10, 0, -1)))   # reversed
bubble_counted([5, 1, 4, 2, 8])
```

```hint
A variable that records whether something has happened is a *flag*. Set
`swapped = False` at the start of each pass, and `True` when a swap
happens. After the pass, if nothing was swapped, `break` leaves the loop.
```

```solution
def bubble_counted(items):
    items = items[:]
    comparisons = 0
    for pass_number in range(len(items) - 1):
        swapped = False
        for i in range(len(items) - 1 - pass_number):
            comparisons = comparisons + 1
            if items[i] > items[i + 1]:
                items[i], items[i + 1] = items[i + 1], items[i]
                swapped = True
        if not swapped:
            break
    return comparisons
---
Ten items in order now cost one pass, 9 comparisons, not 45. Reversed,
nothing changes: every pass swaps something. Real data is often nearly in
order, and there the flag saves most of the work.
```

## 7. Best and worst on sorted data

Which of the three sorts does best on a list that is already sorted? Which
gains nothing?

<details class="dl-answer"><summary>answer</summary>

Insertion sort does best: each element is already in place, so it makes
n − 1 comparisons and moves nothing. Fast sorts in real software often
hand small pieces of the job to insertion sort for that reason.

Selection sort gains nothing: it looks through the whole rest of the list
for the smallest every time, whatever the order. Bubble sort with the flag
from problem 6 matches insertion sort; without it, it matches selection
sort.

</details>

## 8. A million items

For a million items, about how many comparisons does an n² sort make? At
ten million comparisons a second, how long does that take?

<details class="dl-answer"><summary>answer</summary>

About n(n − 1)/2, which is 500,000,000,000: five hundred billion. At ten
million a second, that is 50,000 seconds, about fourteen hours. A sort
that takes about n log n steps makes about twenty million comparisons on
the same data, which takes two seconds. However quick each step is, it
cannot close a gap that size.

</details>

## 9. Selection sort from nothing

Can you write `selection_sort(items)` without looking back, so that it
returns a new sorted list and leaves `items` as it was?

```python exec
id: selection-sort-from-nothing-1
def selection_sort(items):
    return items
```

```inputs
guess: yes
selection_sort([64, 25, 12, 22, 11])
selection_sort([3, 1, 2])
selection_sort([])
```

```solution
def selection_sort(items):
    items = items[:]
    for i in range(len(items) - 1):
        smallest = i
        for j in range(i + 1, len(items)):
            if items[j] < items[smallest]:
                smallest = j
        items[i], items[smallest] = items[smallest], items[i]
    return items
---
It keeps the *index* of the smallest, not its value. With only the value,
it could not do the swap, because it would not know where the value came
from. `items[:]` makes the copy, so the caller's list is left alone.
```

## 10. The guard goes first

In insertion sort, the `while` line is
`while j >= 0 and items[j] > current:`. Why does `j >= 0` come first?

<details class="dl-answer"><summary>answer</summary>

It is a guard: it stops the loop walking off the front of the list. Python
works out an `and` from left to right, and stops as soon as one side is
`False`. With the sides swapped, when `j` reaches −1, Python reads
`items[-1]`, the last element, before the guard is checked. In Python the
answer still comes out right, because the guard then fails. But the code
has read something it never meant to, and in many other languages that is
a crash.

</details>

## 11. Why copy

Why do `bubble_counted` and `selection_sort` above start with
`items = items[:]`?

<details class="dl-answer"><summary>answer</summary>

So that they sort a copy, and leave the caller's list as it was. Without
it, `in_order = selection_sort(data)` would sort `data` too: two names for
one list, from
[Comprehensions, grids and aliasing](tutorial:comprehensions-and-grids).
Python offers both: `sorted(x)` returns a new list, and `x.sort()` changes
`x` itself.

</details>

## 12. Length, then letters

Can you set `ordered` to these names sorted by length, with names of the
same length in alphabetical order?

```python exec
id: length-then-letters-1
names = ["OTTER", "OWL", "HEDGEHOG", "BAT", "HARE", "WREN"]
ordered = []

print(ordered)
```

```inputs
ordered
```

```hint
Python's sort is stable: elements that tie keep the order they came in.
What if the list were already in alphabetical order when you sorted it by
length?
```

```solution
title: with what you've met so far
names = ["OTTER", "OWL", "HEDGEHOG", "BAT", "HARE", "WREN"]
ordered = sorted(sorted(names), key=len)
print(ordered)
---
Sort alphabetically first, then by length. The second sort keeps the
alphabetical order among names of the same length, because it is stable.
```

```solution
title: a shorter way you'll meet later
names = ["OTTER", "OWL", "HEDGEHOG", "BAT", "HARE", "WREN"]
ordered = sorted(names, key=lambda name: (len(name), name))
print(ordered)
---
`lambda name: (len(name), name)` is a function with no name, written where
it is used. It gives each name a pair: its length, then the name. Pairs
sort by their first value, and use the second only to break a tie.
```

## 13. The best first

<div class="dl-world" data-world="secret-messages">

A codebreaker tries every shift, and sorts the decodings so the most
English-looking is first. A rough score: how many of its letters are E, T,
A, O, I or N. Can you write `score(text)`, and set `best` to the decoding
with the highest score?

```python exec
id: the-best-first-1--secret-messages
def decode(message, shift):
    plain = ""
    for character in message:
        if character.isupper():
            plain = plain + chr((ord(character) - ord("A") - shift) % 26 + ord("A"))
        else:
            plain = plain + character
    return plain

def score(text):
    return 0

message = "WKH HQHPB LV DW WKH EULGJH"
decodings = []
for shift in range(26):
    decodings.append(decode(message, shift))
best = ""
print(best)
```

```inputs
guess: yes
score("THE ENEMY")
score("XYZ")
best
```

```hint
`letter in "ETAOIN"` is `True` for those six letters. Count the letters of
`text` for which it is `True`. Then sort the decodings with `key=score`,
largest first, and take the first one.
```

```solution
def decode(message, shift):
    plain = ""
    for character in message:
        if character.isupper():
            plain = plain + chr((ord(character) - ord("A") - shift) % 26 + ord("A"))
        else:
            plain = plain + character
    return plain

def score(text):
    count = 0
    for letter in text:
        if letter in "ETAOIN":
            count = count + 1
    return count

message = "WKH HQHPB LV DW WKH EULGJH"
decodings = []
for shift in range(26):
    decodings.append(decode(message, shift))
best = sorted(decodings, key=score, reverse=True)[0]
print(best)
---
THE ENEMY IS AT THE BRIDGE, with 12. The runner-up scores 10. On a short
message, a score this rough can tie, and then a person has to read the
top few.
```

</div>

<div class="dl-world" data-world="pixel-art">

Can you write `lit(row)`, which counts the `#` in a row, and set
`busiest_first` to the rows of this picture sorted from most lit to
least?

```python exec
id: the-best-first-1--pixel-art
picture = ["#..#", "####", "....", "#.#."]

def lit(row):
    return 0

busiest_first = []
print(busiest_first)
```

```inputs
guess: yes
lit("#..#")
lit("....")
busiest_first
```

```hint
Count the `#` characters with a loop. Then sort the rows with `key=lit`,
largest first.
```

```solution
picture = ["#..#", "####", "....", "#.#."]

def lit(row):
    count = 0
    for pixel in row:
        if pixel == "#":
            count = count + 1
    return count

busiest_first = sorted(picture, key=lit, reverse=True)
print(busiest_first)
---
`['####', '#..#', '#.#.', '....']`. The two rows with 2 lit pixels keep
the order they had, because the sort is stable.
```

</div>

## 14. A function that calls itself

Binary search can be written so that it calls itself on a smaller range,
in place of a loop. A function that calls itself uses *recursion*. What
does every recursive function need, to stop?

```python exec
id: a-function-that-calls-itself-1
def binary_search(items, target, low, high):
    if low > high:
        return -1
    mid = (low + high) // 2
    if items[mid] == target:
        return mid
    if target < items[mid]:
        return binary_search(items, target, low, mid - 1)
    return binary_search(items, target, mid + 1, high)

numbers = [3, 7, 11, 15, 19, 23, 27, 31, 35, 40, 42, 55, 68, 72, 89]
print(binary_search(numbers, 72, 0, len(numbers) - 1))
```

<details class="dl-answer"><summary>answer</summary>

Two things. A case that returns without calling itself again: here, an
empty range, `low > high`, or finding the target. And a call that always
moves closer to that case: here, each call has a smaller range. Leave
either out, and the function calls itself until Python stops it with a
`RecursionError`.

</details>

## 15. Better than n log n

Can any sort beat about n log n comparisons, for any list?

<details class="dl-answer"><summary>answer</summary>

Not a sort that works by comparing, and that has been proved. Each
comparison answers one yes-or-no question, so k comparisons can tell apart
at most 2ᵏ orders. A list of n elements can be in n! orders, and telling
them all apart takes about n log n questions. Sorts that do not compare,
such as counting sort, can beat it, but only when something is known about
the data, such as that it is whole numbers in a small range.

</details>

## 16. One more item

You have a sorted list of a million items, and one new item to add. What
is the cheapest way to keep it sorted?

<details class="dl-answer"><summary>answer</summary>

Find its place with binary search, about 20 comparisons, and insert it
there. Sorting the whole list again would take about twenty million. There
is still a cost: inserting into the middle of a list moves every element
after it one place along, and that grows with n.

</details>

## 17. Correct, and slower

Two students hand in sorts that both give the right answers. One makes 45
comparisons on ten items, and the other 90. Is the second one wrong?

<details class="dl-answer"><summary>answer</summary>

No: it is right, and slower, which are two different things. Is ten items
the real size? Then the difference is millionths of a second, and code
that is easy to read matters more. If the real input is ten million items,
the difference is everything. First make it right, then measure it, then
make it faster where the measurement says it matters.

</details>

## 18. From earlier: at most how many looks

From *Searching a list: linear and binary search*. What is the largest
number of comparisons binary search can need on a sorted list of 64
items?

```python exec
id: from-earlier-at-most-how-many-looks-1
looks = 0
left = 64
while left > 0:
    left = left // 2
    looks = looks + 1
print(looks)
```

```predict
type: number

What will it print?
```

<details class="dl-answer"><summary>why</summary>

7. Each look halves what is left, 64, 32, 16, 8, 4, 2, 1, and then there
is nothing left: seven looks. Six halvings of 64 leave one item, which
still has to be looked at.

</details>

## 19. From earlier: what a loop over a dictionary gives

From *Dictionaries: looking things up by name*.

```python exec
id: from-earlier-a-loop-over-a-dictionary-1
key = {"A": "Q", "B": "W"}
for x in key:
    print(x)
```

```predict
What will the last line print?

- B
  - A loop over a dictionary gives its keys.
- W
  - A loop over a dictionary gives its values.
- B W
  - A loop over a dictionary gives each pair.
```

<details class="dl-answer"><summary>why</summary>

`B`. A loop over a dictionary gives its keys, in the order they were
added. `key.items()` gives the pairs.

</details>

## 20. From earlier: nothing back

From *Lists and looping over them*.

```python exec
id: from-earlier-nothing-back-1
row = [1, 2]
result = row.append(3)
print(result)
```

```predict
What will it print?

- [1, 2, 3]
  - `append()` adds 3, and gives back the list.
- None
  - `append()` changes the list, and gives nothing back.
```

<details class="dl-answer"><summary>why</summary>

`None`, the same as `.sort()`. A method that changes its list in place
gives back nothing, so `row` is `[1, 2, 3]` and `result` is `None`.

</details>
