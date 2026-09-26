---
title: "Searching a list: linear and binary search — Practice"
practice_for: finding-things
year: "2026-2027"
version: 2026.09.26.1
worlds:
  secret-messages: Codes and hidden messages, the kind spies and puzzle-setters make.
  pixel-art: Pictures made of small squares, the way a screen draws them.
---

# Searching a list: linear and binary search — Practice

Problems on searching, and three from earlier pages. Several ask you to
count comparisons without writing code: try those on paper first. Try each
problem before you open anything under it.

## 1. Why −1

Why does `linear_search` give back −1 when the target is not there, and
not 0?

<details class="dl-answer"><summary>answer</summary>

0 is a real index: the first element. A search that gave 0 for "not there"
could not be told apart from one that found the target first. −1 is never
an index that a search finds, so it can only mean "not there". In Python
it is a real index too, the last element, so a caller who forgets to check
for −1 gets a wrong answer and no error.

</details>

## 2. Counting looks

Linear search goes through a list of 100 items. How many comparisons does
it make when the target is first? When it is last? When it is not there?
And on average, when the target is there and equally likely to be
anywhere?

<details class="dl-answer"><summary>answer</summary>

1, 100 and 100. On average, about half the list: (1 + 2 + … + 100) / 100
= 50.5. A missing target is the worst case, because linear search has to
look at everything before it can say no.

</details>

## 3. The last one

Can you write `last_index(items, target)`, which gives the index of the
*last* place the target appears, or −1?

```python exec
id: the-last-one-1
def last_index(items, target):
    return -1
```

```inputs
guess: yes
last_index([4, 2, 4, 4, 1], 4)
last_index([4, 2, 4, 4, 1], 1)
last_index([4, 2, 4, 4, 1], 9)
```

```solution
title: with what you've met so far
def last_index(items, target):
    found = -1
    for index in range(len(items)):
        if items[index] == target:
            found = index
    return found
---
This one keeps going to the end, and remembers the latest match.
```

```solution
title: another way
def last_index(items, target):
    for index in range(len(items) - 1, -1, -1):
        if items[index] == target:
            return index
    return -1
---
Searching from the end can stop at the first match it meets, which is the
last one in the list.
```

## 4. A trace

Binary search looks for 72 in
`[3, 7, 11, 15, 19, 23, 27, 31, 35, 40, 42, 55, 68, 72, 89]`. Which
indexes does it look at, in order?

<details class="dl-answer"><summary>answer</summary>

7, then 11, then 13. At 7 it finds 31, and 72 is larger, so `low` becomes
8. The middle of 8 to 14 is 11, which holds 55, so `low` becomes 12. The
middle of 12 to 14 is 13, and that is 72: three looks.

</details>

## 5. Not sorted

```python exec
id: not-sorted-1
def binary_search(items, target):
    low = 0
    high = len(items) - 1
    while low <= high:
        mid = (low + high) // 2
        if items[mid] == target:
            return mid
        elif target < items[mid]:
            high = mid - 1
        else:
            low = mid + 1
    return -1

print(binary_search([5, 1, 9, 3, 7], 3))
```

```predict
What will it print?

- 3
  - 3 is at index 3, and binary search finds it.
- -1
  - Binary search throws half away, and 3 might be in that half.
- An error
  - Binary search cannot run on a list that is not sorted.
```

<details class="dl-answer"><summary>why</summary>

−1, with no error. The middle is 9, and 3 is smaller, so binary search
throws the right half away, where 3 is. On a list that is not sorted,
binary search gives wrong answers without complaint. Nothing in the code
checks the order: that is up to whoever calls it.

</details>

## 6. Why //

Why does binary search work out `mid = (low + high) // 2`, and not
`(low + high) / 2`?

<details class="dl-answer"><summary>answer</summary>

`/` always gives a float, even when the answer is whole: `(0 + 14) / 2` is
`7.0`. A list index must be a whole number, so `items[7.0]` stops with a
`TypeError: list indices must be integers or slices, not float`. `//`
divides and rounds down, so it always gives a whole number.

</details>

## 7. At most

What is the largest number of comparisons binary search needs on 1,000
items? On 1,000,000?

<details class="dl-answer"><summary>answer</summary>

10 and 20. Ten halvings cover 2¹⁰ = 1,024 items, and twenty cover
2²⁰ = 1,048,576. A thousand times more data costs ten more comparisons.

</details>

## 8. Where it would go

Can you write `where_it_goes(items, target)`, which gives the index where
`target` would go in the sorted list `items` to keep it sorted? If the
target is there already, it gives the index of the first one.

```python exec
id: where-it-would-go-1
sorted_numbers = [3, 7, 11, 15, 19, 23, 27, 31, 35, 40, 42, 55, 68, 72, 89]

def where_it_goes(items, target):
    return 0
```

```inputs
guess: yes
where_it_goes(sorted_numbers, 20)
where_it_goes(sorted_numbers, 31)
where_it_goes(sorted_numbers, 1)
where_it_goes(sorted_numbers, 100)
where_it_goes([], 5)
```

```hint
Keep `low` and `high` as before, but let `high` start at `len(items)`,
one past the end, since the target might go there. While `low < high`,
look at the middle. If it is smaller than the target, the answer is to its
right. If not, the answer is at the middle or to its left.
```

```solution
sorted_numbers = [3, 7, 11, 15, 19, 23, 27, 31, 35, 40, 42, 55, 68, 72, 89]

def where_it_goes(items, target):
    low = 0
    high = len(items)
    while low < high:
        mid = (low + high) // 2
        if items[mid] < target:
            low = mid + 1
        else:
            high = mid
    return low
---
20 would go at index 5, between 19 and 23. When `low` and `high` meet,
that is the place. Python has this in its standard library, as
`bisect.bisect_left`.
```

## 9. Every place

Can you set `places` to every index where 4 appears?

```python exec
id: every-place-1
numbers = [4, 2, 4, 4, 1]
places = []

print(places)
```

```inputs
places
```

```solution
title: with what you've met so far
numbers = [4, 2, 4, 4, 1]
places = []
for index in range(len(numbers)):
    if numbers[index] == 4:
        places.append(index)
print(places)
```

```solution
title: a shorter way
numbers = [4, 2, 4, 4, 1]
places = [index for index, number in enumerate(numbers) if number == 4]
print(places)
---
`[0, 2, 3]`. Finding every place has to look at every element, sorted or
not, so this one is linear whichever way it is written.
```

## 10. The first one past a line

<div class="dl-world" data-world="secret-messages">

In a sorted word list, where do the words starting with M begin? The
place where `"M"` would go is the answer, because `"M"` comes before every
word that starts with M. Can you set `start` to it, with `where_it_goes`
from problem 8?

```python exec
id: the-first-one-past-a-line-1--secret-messages
words = ["AND", "ARE", "BIRD", "BRIDGE", "CODE", "DOOR", "EAST", "FROM",
         "HELLO", "HOUSE", "KEY", "LETTER", "MEET", "NIGHT", "NOON",
         "OTTER", "SPY", "THE", "TREE", "WEST"]
start = 0

print(start, words[start])
```

```inputs
start
```

```solution
def where_it_goes(items, target):
    low = 0
    high = len(items)
    while low < high:
        mid = (low + high) // 2
        if items[mid] < target:
            low = mid + 1
        else:
            high = mid
    return low

words = ["AND", "ARE", "BIRD", "BRIDGE", "CODE", "DOOR", "EAST", "FROM",
         "HELLO", "HOUSE", "KEY", "LETTER", "MEET", "NIGHT", "NOON",
         "OTTER", "SPY", "THE", "TREE", "WEST"]
start = where_it_goes(words, "M")
print(start, words[start])
---
12, where MEET is. The words starting with M run from there up to
`where_it_goes(words, "N")`, which is 13. For a letter no word starts
with, both are the same place, and the range is empty.
```

</div>

<div class="dl-world" data-world="pixel-art">

These are a picture's brightnesses, sorted. Where do the bright pixels,
128 or more, begin? Can you set `start` to that index, with
`where_it_goes` from problem 8?

```python exec
id: the-first-one-past-a-line-1--pixel-art
brightnesses = [12, 30, 45, 90, 127, 128, 200, 255]
start = 0

print(start, brightnesses[start])
```

```inputs
start
```

```solution
def where_it_goes(items, target):
    low = 0
    high = len(items)
    while low < high:
        mid = (low + high) // 2
        if items[mid] < target:
            low = mid + 1
        else:
            high = mid
    return low

brightnesses = [12, 30, 45, 90, 127, 128, 200, 255]
start = where_it_goes(brightnesses, 128)
print(start, brightnesses[start])
---
5, where 128 is. Everything from there on is bright, so
`len(brightnesses) - start`, 3, counts the bright pixels without looking
at them one by one.
```

</div>

## 11. From earlier: the last three

From *Lists and looping over them*.

```python exec
id: from-earlier-the-last-three-1
word = "ALGORITHMS"
print(word[-3:])
```

```predict
What will it print?

- HMS
  - A negative cut counts from the end, and no second number means to the
    end.
- MS
  - -3 is the third from the end, and the slice stops before it.
- THM
  - The slice goes from -3 up to -1.
```

<details class="dl-answer"><summary>why</summary>

`HMS`. `-3` is the cut three places from the end, and a slice with no
second number runs to the end.

</details>

## 12. From earlier: counting with a generator

From *Comprehensions, grids and aliasing*.

```python exec
id: from-earlier-counting-with-a-generator-1
print(sum(1 for letter in "MISSISSIPPI" if letter == "S"))
```

```predict
type: number

What will it print?
```

<details class="dl-answer"><summary>why</summary>

4. The generator gives a 1 for each S, and `sum()` adds them up.
`"MISSISSIPPI".count("S")` gives the same.

</details>

## 13. From earlier: a count that starts itself

From *Dictionaries: looking things up by name*.

```python exec
id: from-earlier-a-count-that-starts-itself-1
counts = {}
for letter in "BANANA":
    counts[letter] = counts.get(letter, 0) + 1
print(counts)
```

```predict
What will it print?

- {'B': 1, 'A': 3, 'N': 2}
  - Each letter is counted, in the order it first turns up.
- {'A': 3, 'B': 1, 'N': 2}
  - A dictionary keeps its keys in alphabetical order.
- An error
  - B is not in `counts` when the loop starts.
```

<details class="dl-answer"><summary>why</summary>

`{'B': 1, 'A': 3, 'N': 2}`. `.get(letter, 0)` gives 0 the first time a
letter turns up, so there is no `KeyError`. The keys stay in the order
they were added: B first, because BANANA starts with B.

</details>
