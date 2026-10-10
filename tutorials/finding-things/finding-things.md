---
title: "Searching a list: linear and binary search"
year: "2026-2027"
version: 2026.10.10.2
worlds:
  secret-messages: Codes and hidden messages, the kind spies and puzzle-setters make.
  pixel-art: Pictures made of small squares, the way a screen draws them.
covers:
  linear-search-the-straightforward-approach:
    covers: [MIT-6.8, CMPS-LO5]
  binary-search-the-power-of-sorted-data:
    covers: [MIT-6.8, CMPS-LO5]
  divide-and-conquer:
    covers: [MIT-6.6]
---

# Searching a list: linear and binary search

The computer is thinking of a whole number from 1 to 100. Run the first
cell once, to choose it. Then change the number after `guess =` in the
second cell, run it, and continue until you find the number.

```python exec
id: guess-my-number-1
import random
secret = random.randint(1, 100)
tries = 0
print("I am thinking of a whole number from 1 to 100.")
```

```python exec
id: guess-my-number-2
guess = 50
tries = tries + 1
if guess == secret:
    print("Yes!", guess, "it is. That took", tries, "tries.")
elif guess < secret:
    print("Higher than", guess)
else:
    print("Lower than", guess)
```

How many tries did it take? Run the first cell again for a new number,
and play once more. What was your first guess, and why that one?

Most people who play a few times start at 50, and then go to the middle of
whatever is left. Each answer removes half of the numbers still
possible. That is the idea behind one of the two ways to search that this
page writes, and the reason it is so much quicker than the other.

## Linear search: the straightforward approach

In the *search problem*, we want to find one item in a collection.
*Linear search* checks each *element*{.term} in turn, from the start of the list,
and stops when it finds the target, or when it reaches the end. You would
use it to look for a friend's name on a guest list in no order.

```
FOR each index i in the list:
    IF items[i] equals the target:
        RETURN i
RETURN -1, because the target is not there
```

### Your turn

Can you turn the *pseudocode*{.term} into `linear_search(items, target)`, which
returns the *index*{.term} where it finds the target, or `-1` if the target is not
in the list?

```python exec
id: your-turn-1
names = ["OTTER", "HERON", "BADGER", "WREN", "HARE", "STOAT"]

def linear_search(items, target):
    return -1
```

```inputs
guess: yes
linear_search(names, "WREN")
linear_search(names, "OTTER")     # the first one
linear_search(names, "FOX")       # not there
linear_search([], "FOX")          # an empty list
```

```hint
`for index in range(len(items)):` visits every index. Where does the
`return -1` go, so that it runs only once the whole list has been checked?
```

```solution
names = ["OTTER", "HERON", "BADGER", "WREN", "HARE", "STOAT"]

def linear_search(items, target):
    for index in range(len(items)):
        if items[index] == target:
            return index
    return -1
---
The `return -1` sits after the loop, not inside it. Inside the loop, as an
`else`, it would give up after checking only the first element.
```

### How much work is linear search?

With 10 items, linear search might need 10 comparisons. With a million, it
might need a million. In the worst case, the work grows at the same rate
as the size of the list. This is written *O(n)*, said "order n". It means
the time grows in proportion to n, the number of items. Twice as many items means up to
twice as many comparisons.

### Your turn

Linear search does one comparison for each item it looks at. Can you count
them? The next task gives you a list of 24 items and a target. It comes in
the world you chose, and the idea is the same in both. Can you set `looks`
to the number of items linear search looks at, up to and including the first
one that matches the target?

<div class="dl-world" data-world="secret-messages">

The list is a coded message, read one letter at a time, from the left. It
is in no order, so a codebreaker has to check the letters in turn. The
target is `"Q"`. Use a `while` loop to move `position` along the message
until `coded[position]` is the target.

```python exec
id: counting-linear-looks--secret-messages
coded = "WKH NHB LV XQGHU WKH PDW"
target = "Q"
position = 0
looks = 1

print(looks)
```

```inputs
looks
```

```hint
`looks` starts at 1, because the first letter is always checked. While
`coded[position]` is not the target, what two numbers change before the next
look?
```

```solution
coded = "WKH NHB LV XQGHU WKH PDW"
target = "Q"
position = 0
looks = 1
while coded[position] != target:
    position = position + 1
    looks = looks + 1
print(looks)
---
13: the `"Q"` is at position 12, and the 13th look finds it. A space counts
as a letter here, so there are 24 places in all. A `"Q"` that was not
there would cost all 24 looks, which is the worst case.
```

</div>

<div class="dl-world" data-world="pixel-art">

The list is a row of 24 pixels, read one pixel at a time, from the left.
Each number is a brightness, and the row is in no order. The target is
`255`, a fully lit pixel. Use a `while` loop to move `position` along the row
until `row[position]` is the target.

```python exec
id: counting-linear-looks--pixel-art
row = [0, 10, 0, 0, 30, 0, 0, 0, 0, 20, 0, 0, 255, 0, 0, 0, 40, 0, 255, 0, 0, 10, 0, 0]
target = 255
position = 0
looks = 1

print(looks)
```

```inputs
looks
```

```hint
`looks` starts at 1, because the first pixel is always checked. While
`row[position]` is not the target, what two numbers change before the next
look?
```

```solution
row = [0, 10, 0, 0, 30, 0, 0, 0, 0, 20, 0, 0, 255, 0, 0, 0, 40, 0, 255, 0, 0, 10, 0, 0]
target = 255
position = 0
looks = 1
while row[position] != target:
    position = position + 1
    looks = looks + 1
print(looks)
---
13: the first `255` is at position 12, and the 13th look finds it. The
second `255`, at position 18, is never reached. A target that was not
there would cost all 24 looks, which is the worst case.
```

</div>

## Binary search: the power of sorted data

Think about looking up a word in a paper dictionary. You would not start at
page one. You would open it near the middle, see whether your word comes
before or after that page, and so remove half of the dictionary with one
look. Then you would do the same with the half that is left.

This is *binary search*. It works only on data that is *sorted*: in order,
from smallest to largest. Step by step:

1. Remember the part of the list that is still possible. Two indexes
   mark its ends: `low` and `high`.
2. Look at the middle element, at index `mid`.
3. If the middle element is the target, we are done.
4. If the target is smaller, search the left half: set `high = mid - 1`.
5. If the target is larger, search the right half: set `low = mid + 1`.
6. Repeat from step 2, until the target is found, or nothing is left.

![Four passes over a fifteen-item sorted list, searching for 3. The
range still to search shrinks from fifteen cells to seven, then three, then one, with low,
mid and high marked under it each time.](range-collapsing.svg)

Count the shaded cells in each row, from top to bottom: fifteen, then
seven, then three, then one. Binary search is quick because it halves the
range each time. Most mistakes happen in the halving too. `mid - 1` and
`mid + 1` make the range smaller each time. If either is wrong, the range can stop
shrinking, and the *loop*{.term} never ends.

### Your turn

Here is the pseudocode, with three gaps:

```
SET low = 0
SET high = length of list - 1
WHILE low <= high:
    SET mid = (low + high) // 2
    IF items[mid] equals target:
        ???
    ELIF target < items[mid]:
        ???
    ELSE:
        ???
RETURN -1
```

Can you fill the gaps, and write `binary_search(items, target)`?

```python exec
id: your-turn-2
sorted_numbers = [3, 7, 11, 15, 19, 23, 27, 31, 35, 40, 42, 55, 68, 72, 89]

def binary_search(items, target):
    return -1
```

```inputs
guess: yes
binary_search(sorted_numbers, 31)
binary_search(sorted_numbers, 20)     # not there
binary_search(sorted_numbers, 3)      # the first element
binary_search(sorted_numbers, 89)     # the last element
```

```hint
The three gaps are: return `mid`; move `high` to just before `mid`;
move `low` to just after `mid`. Why just before and just after, and not
`mid` itself?
```

```solution
sorted_numbers = [3, 7, 11, 15, 19, 23, 27, 31, 35, 40, 42, 55, 68, 72, 89]

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
---
31 is found at once: it is exactly in the middle. 3 and 89 each take four
looks, the picture's four rows. `mid` has been checked already, so the new
range leaves it out. With `high = mid`, the range could stop shrinking.
```

### Your turn

The next task searches a sorted list with your `binary_search`. It comes in
the world you chose, and the idea is the same in both. If you have not
written `binary_search` yet, open the fold below, and paste the function
at the top of the task's cell.

<details class="dl-answer"><summary>a binary_search you can paste</summary>

```python
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
```

</details>

<div class="dl-world" data-world="secret-messages">

A codebreaker has a coded word, and does not know the Caesar shift. The
codebreaker tries every shift from 0 to 25, and checks each decoding against
a list of English words in alphabetical order. Strings compare
alphabetically, so binary search works on the list as it does on numbers.
The cell has `decode(word, shift)`, which undoes one shift. Can you set
`found` to a list of the shifts whose decoding is in `words`, using
`binary_search`?

```python exec
id: your-turn-3--secret-messages
words = ["AND", "ARE", "BIRD", "BRIDGE", "CODE", "DOOR", "EAST", "FROM",
         "HELLO", "HOUSE", "KEY", "LETTER", "MEET", "NIGHT", "NOON",
         "OTTER", "SPY", "THE", "TREE", "WEST"]

def decode(word, shift):
    plain = ""
    for letter in word:
        plain = plain + chr((ord(letter) - ord("A") - shift) % 26 + ord("A"))
    return plain

coded = "KHOOR"
found = []

print(found)
```

```inputs
found
```

```hint
Loop over the shifts, `range(26)`. For each one, decode the word, and ask
`binary_search(words, ...)` whether it is there. It is there when the
result is not `-1`, and then you can append the shift to `found`.
```

```solution
words = ["AND", "ARE", "BIRD", "BRIDGE", "CODE", "DOOR", "EAST", "FROM",
         "HELLO", "HOUSE", "KEY", "LETTER", "MEET", "NIGHT", "NOON",
         "OTTER", "SPY", "THE", "TREE", "WEST"]

def decode(word, shift):
    plain = ""
    for letter in word:
        plain = plain + chr((ord(letter) - ord("A") - shift) % 26 + ord("A"))
    return plain

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

coded = "KHOOR"
found = []
for shift in range(26):
    if binary_search(words, decode(coded, shift)) != -1:
        found.append(shift)
print(found)
---
`[3]`: shift 3 gives HELLO. A real word list has tens of thousands of
words. Binary search finds out whether a word is there in about 15 looks,
where linear search could take tens of thousands, and it does that 26
times, once for each shift.
```

</div>

<div class="dl-world" data-world="pixel-art">

A picture 100 pixels wide and 100 tall has 10,000 pixels. Number them
along each row, so the pixel at `row` and `column` is number
`row * 100 + column`. This picture is a diagonal line, and `lit` is the
sorted list of the numbers of its lit pixels. Is the pixel at each point in
`points` lit? Can you set `answers` to a list of `True` or `False`, one for
each point, using `binary_search`?

```python exec
id: your-turn-3--pixel-art
lit = [row * 100 + row for row in range(100)]
points = [[42, 42], [42, 43], [0, 0], [99, 99], [50, 49]]
answers = []

print(answers)
```

```inputs
answers
```

```hint
Loop over `points`. For each one, find its number, `row * 100 + column`.
Is that number in `lit`? It is when `binary_search` does not return `-1`,
and then you can append `True` to `answers`.
```

```solution
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

lit = [row * 100 + row for row in range(100)]
points = [[42, 42], [42, 43], [0, 0], [99, 99], [50, 49]]
answers = []
for row, column in points:
    answers.append(binary_search(lit, row * 100 + column) != -1)
print(answers)
---
`[True, False, True, True, False]`. Keeping only the lit pixels, in order,
saves space when most of a picture is empty. Binary search needs at most 7
looks among these 100.
```

</div>

### How much work is binary search?

Each step cuts the part left to search in half. Start with 1,000,000 items:

| After | Items left to search |
|---|---|
| 1 step | 500,000 |
| 2 steps | 250,000 |
| 10 steps | about 1,000 |
| 20 steps | about 1 |

So binary search on a million items needs at most about 20 comparisons,
where linear search might need a million. That is the difference between
*O(log n)* and O(n). O(log n) means the time grows with the number of
times n can be halved before it reaches 1, and that grows very slowly as n
gets bigger.

There is a cost. The data must be sorted first, and sorting takes time. So
binary search is worth it when the same data is searched many times, which
happens very often.

### Your turn

The table promises at most about 20 looks for a million items. Does a real
list keep the promise? The cell has `count_looks(items, target)`, which does
what `binary_search` does, and gives back the number of looks it made. It
comes in the world you chose. Can you set `most` to the largest number of
looks it needs, over every item in the list as the target?

<div class="dl-world" data-world="secret-messages">

The list is `words`, the 20 English words in alphabetical order that a
codebreaker checks each decoding against. Make each word the target in turn,
and keep the largest count.

```python exec
id: counting-binary-looks--secret-messages
words = ["AND", "ARE", "BIRD", "BRIDGE", "CODE", "DOOR", "EAST", "FROM",
         "HELLO", "HOUSE", "KEY", "LETTER", "MEET", "NIGHT", "NOON",
         "OTTER", "SPY", "THE", "TREE", "WEST"]

def count_looks(items, target):
    looks = 0
    low = 0
    high = len(items) - 1
    while low <= high:
        looks = looks + 1
        mid = (low + high) // 2
        if items[mid] == target:
            return looks
        elif target < items[mid]:
            high = mid - 1
        else:
            low = mid + 1
    return looks

most = 0

print(most)
```

```inputs
most
```

```hint
Loop over `words`, with `for word in words:`. For each word, ask
`count_looks(words, word)`. When is the count larger than `most`, and what
should `most` become then?
```

```solution
words = ["AND", "ARE", "BIRD", "BRIDGE", "CODE", "DOOR", "EAST", "FROM",
         "HELLO", "HOUSE", "KEY", "LETTER", "MEET", "NIGHT", "NOON",
         "OTTER", "SPY", "THE", "TREE", "WEST"]

def count_looks(items, target):
    looks = 0
    low = 0
    high = len(items) - 1
    while low <= high:
        looks = looks + 1
        mid = (low + high) // 2
        if items[mid] == target:
            return looks
        elif target < items[mid]:
            high = mid - 1
        else:
            low = mid + 1
    return looks

most = 0
for word in words:
    looks = count_looks(words, word)
    if looks > most:
        most = looks
print(most)
---
5. Four halvings take 20 words down to 1, and one more look checks it.
Linear search could need all 20 for one word.
```

</div>

<div class="dl-world" data-world="pixel-art">

The list is `lit`, the 100 numbers of a diagonal line's lit pixels, in
order. Make each number the target in turn, and keep the largest count.

```python exec
id: counting-binary-looks--pixel-art
lit = [row * 100 + row for row in range(100)]

def count_looks(items, target):
    looks = 0
    low = 0
    high = len(items) - 1
    while low <= high:
        looks = looks + 1
        mid = (low + high) // 2
        if items[mid] == target:
            return looks
        elif target < items[mid]:
            high = mid - 1
        else:
            low = mid + 1
    return looks

most = 0

print(most)
```

```inputs
most
```

```hint
Loop over `lit`, with `for number in lit:`. For each number, ask
`count_looks(lit, number)`. When is the count larger than `most`, and what
should `most` become then?
```

```solution
lit = [row * 100 + row for row in range(100)]

def count_looks(items, target):
    looks = 0
    low = 0
    high = len(items) - 1
    while low <= high:
        looks = looks + 1
        mid = (low + high) // 2
        if items[mid] == target:
            return looks
        elif target < items[mid]:
            high = mid - 1
        else:
            low = mid + 1
    return looks

most = 0
for number in lit:
    looks = count_looks(lit, number)
    if looks > most:
        most = looks
print(most)
---
7. Six halvings take 100 pixels down to 1, and one more look checks it.
Linear search could need all 100 for one number.
```

</div>

## Divide and conquer

Binary search is our first example of *divide and conquer*: split a
problem into smaller pieces, solve the pieces, and combine the answers. It
is one of the most useful ideas in the design of *algorithms*{.term}. A phone finds
a contact this way. You find a page in a book this way. A doctor who
halves the possible causes with each test works this way too.

In the game at the top of this page, what is the largest number of guesses
you could need, if you always guess the middle of what is left? How do you
know?

<details class="dl-answer"><summary>answer</summary>

You could need seven. Each guess halves what is left: 100 numbers, then at
most 50, 25, 12, 6, 3, 1. You can also see it this way. Six halvings cover 2 × 2 × 2 × 2 × 2 × 2
= 64 numbers, which is not enough, and seven cover 128, which is.

</details>

## Putting it together

This cell counts the comparisons both searches make, for the same target
in the same list. The list holds 0, 3, 6, 9 and so on up to 999, which is
334 numbers, and the target is 600.

```python exec
id: putting-it-together-1
def linear_search_counted(items, target):
    comparisons = 0
    for index in range(len(items)):
        comparisons = comparisons + 1
        if items[index] == target:
            return comparisons
    return comparisons

def binary_search_counted(items, target):
    comparisons = 0
    low = 0
    high = len(items) - 1
    while low <= high:
        comparisons = comparisons + 1
        mid = (low + high) // 2
        if items[mid] == target:
            return comparisons
        elif target < items[mid]:
            high = mid - 1
        else:
            low = mid + 1
    return comparisons

data = list(range(0, 1000, 3))
target = 600
print("Linear search:", linear_search_counted(data, target), "comparisons")
print("Binary search:", binary_search_counted(data, target), "comparisons")
```

```predict
type: number
tolerance: 1

How many comparisons will binary search make?
```

Linear search makes 201 comparisons, and binary search 8. For most targets
in this list, binary search needs 7 to 9, and never more than 9. Try a few
more targets: the first number in the list, the last, a number in the
middle, and one that is not there. Which search does better each time? Is
there a target where linear search wins?

## Looking back

Binary search needs sorted data, and sorting takes time. When is it worth
sorting a list first, and when is a linear search the better choice?

A challenge: how many guesses does the game at the top need on average, if
you always guess the middle? Play it for every secret number from 1 to 100,
count the guesses for each, and find the average. Is it closer to 7, or
lower?

```python challenge
# Guess my number, played by the computer, for every secret from 1 to 100.
def guesses_needed(secret):
    low = 1
    high = 100
    count = 0
    # Guess the middle of low and high until the guess is the secret.
    return count

print(guesses_needed(50))
```

The next page,
[Sorting a list: bubble, insertion and selection sort](tutorial:putting-things-in-order),
looks at the other side of the problem. It shows how data gets sorted.

## Where to read more

Everything here is covered elsewhere too, often in a form that will suit you
better than this one.

Pound, M. (Computerphile) (2023). *Binary Search Algorithm*.
<https://www.youtube.com/watch?v=hDn8iOc30Tk>. It explains the same
halve-and-repeat idea as this page, with a different worked example.

Computerphile (2013). *Getting Sorted & Big O Notation*.
<https://www.youtube.com/watch?v=kgBjXUE_Nwc>. It explains where O(log n)
and O(n) come from, and how the same notation applies to sorting as well as
searching.
