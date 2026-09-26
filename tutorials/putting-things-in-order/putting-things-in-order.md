---
title: "Sorting a list: bubble, insertion and selection sort"
year: "2026-2027"
version: 2026.09.26.1
worlds:
  secret-messages: Codes and hidden messages, the kind spies and puzzle-setters make.
  pixel-art: Pictures made of small squares, the way a screen draws them.
covers:
  bubble-sort-let-things-rise:
    covers: [MIT-6.8]
  insertion-sort-sort-like-you-sort-cards:
    covers: [MIT-6.8]
  selection-sort-find-the-smallest:
    covers: [MIT-6.8]
  comparing-our-sorts:
    covers: [MIT-6.8]
# CMPS-LO5 is taught here, but this page is not on Computational Methods,
# so it is not claimed for that module until #333 brings it into the course.
---

# Sorting a list: bubble, insertion and selection sort

Python can sort a list in one line, with `sorted()`. Here it sorts three
numbers, and then the same three written as strings. What will the last
line print?

```python exec
id: sorted-in-one-line-1
print(sorted([10, 9, 100]))
print(sorted(["10", "9", "100"]))
```

```predict
What will the last line print?

- ['9', '10', '100']
  - They are the same numbers, so they sort the same way.
- ['10', '100', '9']
  - Strings are compared character by character, from the first.
```

The numbers sort as numbers, and the strings as text: `"10"` and `"100"`
both start with 1, which comes before 9, so both go first. The same thing
puts `file10` before `file9` in a folder of files. A sort is only as good
as its idea of which of two things comes first.

In a real program, `sorted()` is the way to sort. This page builds three
sorts by hand anyway: bubble sort, insertion sort and selection sort. Each
is short enough to hold in your head all at once, and building them is how
you see what sorting costs, and why some ways are far slower than others.
[Searching a list](tutorial:finding-things) showed why it matters: binary
search needs sorted data.

## The swap

Every sort here moves elements by *swapping* two of them: exchanging their
places. Python does it in one line.

```python exec
id: the-swap-1
numbers = [10, 20, 30, 40, 50]
numbers[1], numbers[3] = numbers[3], numbers[1]
print(numbers)
```

`a, b = b, a` works because Python works out the whole right-hand side
first, and only then gives the values to the names on the left. Many other
languages need a spare variable: `spare = a`, then `a = b`, then
`b = spare`.

## Bubble sort: let things rise

*Bubble sort* walks through the list comparing each pair of neighbours,
and swaps any pair that is in the wrong order. After one full pass, the
largest element has bubbled up to the end. Then it goes again.

In this list, 90 is already at the end. 64, the next largest, starts at the
front. Where will it be after one pass?

```python exec
id: bubble-sort-let-things-rise-1
data = [64, 34, 25, 12, 22, 11, 90]
print("Start:", data)
for i in range(len(data) - 1):
    if data[i] > data[i + 1]:
        data[i], data[i + 1] = data[i + 1], data[i]
        print("  Swapped", i, "and", i + 1, ":", data)
    else:
        print("  No swap at", i, ":", data)
print("After one pass:", data)
```

64 moves one place right at every swap, until it meets 90. A pass carries
the largest element it meets along with it, so after each pass, one more
element is in its final place, and a list of n elements needs at most
n − 1 passes. Here is the whole sort. A bar, `|`, marks the part that has
settled.

```python exec
id: bubble-sort-let-things-rise-2
data = [64, 34, 25, 12, 22, 11, 90]
comparisons = 0
print("Start:", data)

for pass_number in range(len(data) - 1):
    still_to_check = len(data) - pass_number
    swaps = 0
    for i in range(still_to_check - 1):
        comparisons = comparisons + 1
        if data[i] > data[i + 1]:
            data[i], data[i + 1] = data[i + 1], data[i]
            swaps = swaps + 1
    print("Pass", pass_number + 1, ":", data[:still_to_check - 1], "|",
          data[still_to_check - 1:], "  swapped:", swaps)

print("Comparisons in total:", comparisons)
```

Three things to look for: the bar moves one place left on every pass; each
pass makes one comparison fewer than the last; and the last pass swaps
nothing, because the list was sorted before it ran, and bubble sort had no
way to know. Try a list of your own: one already sorted, and one in reverse
order.

### Your turn

Here are the lines of `bubble_sort(items)`, in the wrong order. Each line
has the right indentation already. Can you put them in order, so that it
returns the list sorted from smallest to largest?

```python exec
id: your-turn-1
            items[i], items[i + 1] = items[i + 1], items[i]
    return items
        for i in range(len(items) - 1 - pass_number):
def bubble_sort(items):
            if items[i] > items[i + 1]:
    for pass_number in range(len(items) - 1):
```

```inputs
guess: yes
bubble_sort([5, 2, 9, 1])
bubble_sort([1, 2, 3])        # already sorted
bubble_sort([7])              # one element
bubble_sort([])               # an empty list
```

```hint
The indentation tells you which line belongs inside which. Which line has
no indentation at all? Which two lines are a loop inside a loop?
```

```solution
def bubble_sort(items):
    for pass_number in range(len(items) - 1):
        for i in range(len(items) - 1 - pass_number):
            if items[i] > items[i + 1]:
                items[i], items[i + 1] = items[i + 1], items[i]
    return items
---
The inner loop stops `pass_number` places earlier each time, because that
many elements have settled at the end. With one element or none,
`range(len(items) - 1)` is empty, and the list comes back as it went in.
```

## Insertion sort: sort like you sort cards

*Insertion sort* works the way most people sort a hand of cards: pick up
the cards one at a time, and put each new one into its place among the
cards already sorted. In a list, it keeps a sorted part at the start. It
takes the next element, and moves each larger element in the sorted part
one place right, until the gap is where the new element belongs.

```
FOR each index i from 1 to the end:
    SET current = items[i]
    SET j = i - 1
    WHILE j >= 0 AND items[j] > current:
        MOVE items[j] one place to the right
        DECREASE j by 1
    PUT current at position j + 1
RETURN items
```

### Your turn

Here are the lines of `insertion_sort(items)`, in the wrong order, with
their indentation. Can you put them in order?

```python exec
id: your-turn-2
        items[j + 1] = current
            j = j - 1
def insertion_sort(items):
        current = items[i]
    return items
        while j >= 0 and items[j] > current:
    for i in range(1, len(items)):
            items[j + 1] = items[j]
        j = i - 1
```

```inputs
guess: yes
insertion_sort([5, 2, 9, 1])
insertion_sort([1, 2, 3])
insertion_sort([3, 3, 1])     # two the same
insertion_sort([])
```

```hint
Follow the pseudocode above, one line at a time. `current` has to be
taken out before anything moves into its place.
```

```solution
def insertion_sort(items):
    for i in range(1, len(items)):
        current = items[i]
        j = i - 1
        while j >= 0 and items[j] > current:
            items[j + 1] = items[j]
            j = j - 1
        items[j + 1] = current
    return items
---
The `while` stops at the first element that is not larger than `current`,
so an already sorted list costs one comparison per element, and nothing
moves. That is where insertion sort beats the other two.
```

## Selection sort: find the smallest

*Selection sort* finds the smallest element in the part of the list not yet
sorted, and swaps it to the front of that part. Then it finds the next
smallest, and so on. With a hand of cards, it is looking through all of
them for the lowest, putting it first, and then looking through the rest.

### Your turn

This selection sort is broken. It sorts some lists and not others, so a
test that happens to pass says nothing. Can you find a list it gets wrong,
and then fix it?

```python exec
id: your-turn-3
def selection_sort(items):
    for i in range(len(items) - 1):
        smallest = i
        for j in range(i + 1, len(items)):
            if items[j] < items[i]:
                smallest = j
        items[i], items[smallest] = items[smallest], items[i]
    return items
```

```inputs
guess: yes
selection_sort([5, 4, 3, 2, 1])
selection_sort([3, 1, 2])
selection_sort([4, 1, 3, 2])
```

```hint
Trace `[3, 1, 2]` by hand. When `j` reaches 2, which element is it being
compared with, and which should it be compared with?
```

```solution
def selection_sort(items):
    for i in range(len(items) - 1):
        smallest = i
        for j in range(i + 1, len(items)):
            if items[j] < items[smallest]:
                smallest = j
        items[i], items[smallest] = items[smallest], items[i]
    return items
---
The broken version compared each element with `items[i]`, the first of the
unsorted part, and not with the smallest found so far. So it found the
*last* element smaller than the first, which is not always the smallest.
It sorted `[5, 4, 3, 2, 1]` anyway, and gave `[2, 1, 3]` for `[3, 1, 2]`.
A reversed list is a good test, and not enough on its own.
```

## Sorting with a key

`sorted()` can sort by anything: give it a function as `key=`, and it sorts
by what that function gives back for each element. `reverse=True` puts the
largest first.

```python exec
id: sorting-with-a-key-1
words = ["OTTER", "OWL", "HEDGEHOG", "BAT", "HARE"]
print(sorted(words))
print(sorted(words, key=len))

def last_letter(word):
    return word[-1]

print(sorted(words, key=last_letter))
```

`key=len` sorts by length, and `key=last_letter` by the last letter. The
function is passed without brackets, as `generate_sequence` was given a
rule in [Comprehensions, grids and aliasing](tutorial:comprehensions-and-grids):
`sorted()` calls it on each element. Words with the same length keep the
order they came in, so OWL stays before BAT.

A list also has a `.sort()` method, which sorts that list in place. What
will this print?

```python exec
id: sorting-with-a-key-2
numbers = [3, 1, 2]
result = numbers.sort()
print(result)
```

```predict
What will it print?

- [1, 2, 3]
  - `.sort()` sorts the list, and gives it back.
- None
  - `.sort()` changes the list it belongs to, and gives nothing back.
- [3, 1, 2]
  - `result` holds the list from before it was sorted.
```

It prints `None`. `.sort()` changes `numbers` itself, like `append()`, and
gives back nothing. `sorted()` leaves the old list alone, and gives back a
new one. The difference is the one from
[Comprehensions, grids and aliasing](tutorial:comprehensions-and-grids):
change the list you were given, or return a new one.

### Your turn

<div class="dl-world" data-world="secret-messages">

Here are the letter counts of a coded message. Can you set `by_count` to
its letters, most common first? In English, the most common letters are E,
then T. What do the first two tell you?

```python exec
id: your-turn-4--secret-messages
counts = {"W": 6, "K": 3, "H": 9, "Q": 2, "P": 2, "B": 1, "L": 3,
          "V": 1, "J": 2, "D": 2, "E": 1, "U": 2, "G": 1}

def how_often(letter):
    return counts[letter]

by_count = []
print(by_count)
```

```inputs
by_count[:3]
```

```hint
`sorted(counts)` sorts the keys. Which `key=` sorts them by their count,
and what puts the largest first?
```

```solution
counts = {"W": 6, "K": 3, "H": 9, "Q": 2, "P": 2, "B": 1, "L": 3,
          "V": 1, "J": 2, "D": 2, "E": 1, "U": 2, "G": 1}

def how_often(letter):
    return counts[letter]

by_count = sorted(counts, key=how_often, reverse=True)
print(by_count)
---
H, then W. If H is a coded E and W a coded T, both are three letters on,
so the shift is probably 3. Two letters agreeing is much stronger evidence
than one.
```

</div>

<div class="dl-world" data-world="pixel-art">

Can you set `darkest_first` to these colours sorted by how bright they
look, darkest first? `brightness` weighs red, green and blue the way an
eye does.

```python exec
id: your-turn-4--pixel-art
colours = [[255, 0, 0], [0, 255, 0], [0, 0, 255], [255, 255, 0], [128, 128, 128]]

def brightness(colour):
    return 0.299 * colour[0] + 0.587 * colour[1] + 0.114 * colour[2]

darkest_first = []
print(darkest_first)
```

```inputs
darkest_first
```

```hint
Which function should `sorted()` call on each colour, to know which comes
first?
```

```solution
colours = [[255, 0, 0], [0, 255, 0], [0, 0, 255], [255, 255, 0], [128, 128, 128]]

def brightness(colour):
    return 0.299 * colour[0] + 0.587 * colour[1] + 0.114 * colour[2]

darkest_first = sorted(colours, key=brightness)
print(darkest_first)
---
Blue, red, grey, green, yellow. Pure blue looks darker than pure red, and
pure green brighter than mid-grey. Without `key=`, `sorted()` would
compare the lists element by element, red first, which is not how an eye
sees them.
```

</div>

## Comparing our sorts

All three sorts give the same sorted list. Which does less work? A good
measure is the number of comparisons. This cell counts them for bubble
sort, on lists of 10, 50, 100 and 200 items, each in reverse order. What do
you think happens to the count when the size doubles?

```python exec
id: comparing-our-sorts-1
def bubble_sort_counted(items):
    items = items[:]
    comparisons = 0
    for pass_number in range(len(items) - 1):
        for i in range(len(items) - 1 - pass_number):
            comparisons = comparisons + 1
            if items[i] > items[i + 1]:
                items[i], items[i + 1] = items[i + 1], items[i]
    return comparisons

for size in [10, 50, 100, 200]:
    backwards = list(range(size, 0, -1))
    print("Size", size, ":", bubble_sort_counted(backwards), "comparisons")
```

When the size doubles, the comparisons go up about four times: 4,950 for
100 items, 19,900 for 200. Each of the three sorts makes about
$\frac{n(n-1)}{2}$ comparisons in its worst case, and that grows in
proportion to $n^2$, written $O(n^2)$.

| Items | Comparisons, about | Time |
|---|---|---|
| 10 | 45 | instant |
| 1,000 | 500,000 | still quick |
| 1,000,000 | 500,000,000,000 | a long wait |

Faster sorts exist: merge sort takes about $n \log n$ steps, and Python's
own `sorted()` is built on the same idea. Add a counter to your insertion
sort and your selection sort, and run all three on the same lists: random,
already sorted, and reversed. Does each one always make the same number of
comparisons, or does it depend on the list?

```python exec
id: comparing-our-sorts-2
# Your experiments: three sorts, three kinds of list.
```

## Looking back

Insertion sort is quick on a list that is nearly in order, and bubble sort
makes the same number of comparisons whatever it is given. What would you
want to know about your data before you chose one?

A challenge: *Shell sort* improves insertion sort. It first compares
elements a gap apart, say 4, then a smaller gap, and finishes with a gap of
1, which is an ordinary insertion sort. By then the list is nearly in
order, where insertion sort is at its quickest. Can you build it, and count
its comparisons against insertion sort's?

```python challenge
# Shell sort: insertion sort on elements `gap` apart, for smaller and smaller gaps.
def shell_sort(items):
    gap = len(items) // 2
    while gap > 0:
        # An insertion sort, where "the element before" is `gap` places back.
        gap = gap // 2
    return items

print(shell_sort([64, 34, 25, 12, 22, 11, 90]))
```

The next page,
[Designing and testing good functions](tutorial:building-reusable-tools),
turns the testing you did here, with lists chosen to catch a sort out, into
tests a program runs for you.

## Where to read more

Everything here is covered elsewhere too, often in a form that will suit you
better than this one.

Bingmann, T. (2013). *15 Sorting Algorithms in 6 Minutes*.
<https://www.youtube.com/watch?v=kPRA0W1kECg>. Sorting made audible and
visible at once. The difference between the $n^2$ sorts and the
$n \log n$ ones is plain here in a way no table of numbers manages.

Computerphile (2013). *Getting Sorted & Big O Notation*.
<https://www.youtube.com/watch?v=kgBjXUE_Nwc>. Why the growth rate matters
more than the constant factor, which is the whole argument of the
comparison section.

Python Software Foundation. *Sorting Techniques*.
<https://docs.python.org/3/howto/sorting.html>. How `sorted()` and `key=`
work, including why Python's sort is stable, and when that matters.
