---
title: "Searching a list: linear and binary search"
year: "2026-2027"
version: 2026.09.26.1
worlds:
  secret-messages: Codes and hidden messages, the kind spies and puzzle-setters make.
  pixel-art: Pictures made of small squares, the way a screen draws them.
covers:
  linear-search-the-straightforward-approach:
    covers: [MIT-6.8]
  binary-search-the-power-of-sorted-data:
    covers: [MIT-6.8]
  divide-and-conquer:
    covers: [MIT-6.6]
# CMPS-LO5 is taught here, but this page is not on Computational Methods,
# so it is not claimed for that module until #333 brings it into the course.
---

# Searching a list: linear and binary search

The computer is thinking of a whole number from 1 to 100. Run the first
cell once, to choose it. Then put a guess in the second cell and run it,
and keep going until you find the number.

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
whatever is left. Each answer rules out half of the numbers still
possible. That is the idea behind one of the two ways to search that this
page writes, and the reason it is so much quicker than the other.

## Linear search: the straightforward approach

The *search problem* is finding one item in a collection. *Linear search*
checks each element in turn, from the start of the list, and stops when it
finds the target, or when it reaches the end. It is how you would look for
a friend's name on a guest list in no order.

```
FOR each index i in the list:
    IF items[i] equals the target:
        RETURN i
RETURN -1, because the target is not there
```

### Your turn

Can you turn the pseudocode into `linear_search(items, target)`, which
returns the index where it finds the target, or -1 if the target is not in
the list?

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
might need a million. In the worst case, the work grows in step with the
size of the list. This is written *O(n)*, said "order n": the time grows in
proportion to n, the number of items. Twice as many items means up to
twice as many comparisons.

## Binary search: the power of sorted data

Think about looking up a word in a paper dictionary. You would not start at
page one. You would open it near the middle, see whether your word comes
before or after that page, and so rule out half of the dictionary with one
look. Then you would do the same with the half that is left.

This is *binary search*. It works only on data that is *sorted*: in order,
from smallest to largest. Step by step:

1. Keep track of the part of the list that is still possible. Two indexes
   mark its ends: `low` and `high`.
2. Look at the middle element, at index `mid`.
3. If the middle element is the target, we are done.
4. If the target is smaller, search the left half: set `high = mid - 1`.
5. If the target is larger, search the right half: set `low = mid + 1`.
6. Repeat from step 2, until the target is found, or nothing is left.

![Four passes over a fifteen-item sorted list, searching for 3. The live
range shrinks from fifteen cells to seven, then three, then one, with low,
mid and high marked under it each time.](range-collapsing.svg)

Count the shaded cells in each row, from top to bottom: fifteen, then
seven, then three, then one. The halving is why binary search is quick,
and it is also where the mistakes happen. `mid - 1` and `mid + 1` are what
make the range smaller each time. If either is wrong, the range can stop
shrinking, and the loop never ends.

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
The three gaps are: give back `mid`; move `high` to just before `mid`;
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

<div class="dl-world" data-world="secret-messages">

A codebreaker tries every shift on a coded word, and checks each decoding
against a list of English words, kept in alphabetical order. Strings
compare alphabetically, so binary search works on the list as it does on
numbers. Can you set `found` to the shifts whose decoding is in `words`?

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
Try every shift from 0 to 25. For each one, decode the word, and ask
`binary_search(words, ...)` whether it is there. It is there when the
answer is not -1.
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
sorted list of its lit pixels. Can you set `answers` to `True` or `False`
for each point, with binary search?

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
For each point, work out its number, `row * 100 + column`. Is that number
in `lit`? It is when `binary_search` does not give back -1.
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

There is a cost: the data must be sorted first, and sorting takes time. So
binary search pays off when the same data is searched many times, which
happens very often.

## Divide and conquer

Binary search is our first example of *divide and conquer*: split a
problem into smaller pieces, solve the pieces, and combine the answers. It
is one of the most useful ideas in the design of algorithms. Looking up a
contact on a phone, finding a page in a book, and a doctor ruling out half
the possible causes with each test all work this way.

In the game at the top of this page, what is the largest number of guesses
you could need, if you always guess the middle of what is left? How do you
know?

<details class="dl-answer"><summary>answer</summary>

Seven. Each guess halves what is left: 100 numbers, then at most 50, 25,
12, 6, 3, 1. Another way to see it: six halvings cover 2 × 2 × 2 × 2 × 2 × 2
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
looks at the other side: how data comes to be sorted in the first place.

## Where to read more

Everything here is covered elsewhere too, often in a form that will suit you
better than this one.

Pound, M. (Computerphile) (2023). *Binary Search Algorithm*.
<https://www.youtube.com/watch?v=hDn8iOc30Tk>. The same halve-and-repeat
idea this page builds, explained with a different worked example.

Computerphile (2013). *Getting Sorted & Big O Notation*.
<https://www.youtube.com/watch?v=kgBjXUE_Nwc>. Where O(log n) and O(n)
come from, and how the same notation applies to sorting as well as
searching.
