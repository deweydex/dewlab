---
title: "Debugging: from a report to the line that caused it — Practice"
practice_for: finding-where-it-went-wrong
year: "2026-2027"
version: 2026.09.26.1
---

# Debugging: from a report to the line that caused it — Practice

Four more reports, two questions to think about, and one problem you have
not met before. Three of the bugs use ideas from earlier pages, and each
one says which page. Try each problem before you open anything under it.

Keep a log for every bug, as on the tutorial page: a guess, a test, and
what happened.

## 1. One pixel, a whole column

From *Comprehensions, grids and aliasing*.

> "I made a grid of dark pixels, three by three, and lit the pixel at row
> 0, column 1. A whole column lit up."

```python exec
id: one-pixel-a-whole-column-1
# Guess:
# Test:
# What happened:

grid = [[0] * 3] * 3
grid[0][1] = 1

for row in grid:
    print(row)
```

```hint
How many different lists are inside `grid`? Can you change `grid[2][2]`
and print the grid again?
```

```inputs
grid
```

```solution
grid = [[0] * 3 for row in range(3)]
grid[0][1] = 1

for row in grid:
    print(row)
---
`[[0] * 3] * 3` makes one row, and puts the same row in the grid three
times. There is only one row to change, so every row shows the change. A
comprehension runs `[0] * 3` once for each row, so it makes three
different rows.
```

## 2. Every period counts once

From *Dictionaries: looking things up by name*.

> "I counted the fossils in the museum by the period they come from. There
> are three Cretaceous fossils, and the program shows only
> `{'Cretaceous': 1}`. The other periods are missing."

```python exec
id: every-period-counts-once-1
# Guess:
# Test:
# What happened:

fossils = ["Jurassic", "Cretaceous", "Jurassic", "Triassic",
           "Cretaceous", "Cretaceous"]

def count_periods(periods):
    for period in periods:
        counts = {}
        counts[period] = counts.get(period, 0) + 1
    return counts

print(count_periods(fossils))
```

```hint
Can you print `counts` inside the loop, after each fossil? What happens to
it each time round?
```

```inputs
count_periods(fossils)
count_periods(["Triassic"])     # one fossil
count_periods([])               # no fossils
```

```solution
def count_periods(periods):
    counts = {}
    for period in periods:
        counts[period] = counts.get(period, 0) + 1
    return counts

print(count_periods(fossils))
---
`counts = {}` was inside the loop, so a new, empty dictionary was made for
every fossil. Only the last fossil was left in it. Made once, before the
loop, the dictionary keeps every count.

The empty list shows one more difference. With `counts = {}` inside the
loop, the line never runs, and `return counts` stops with an error.
```

## 3. Heads every time

From *Random numbers: pseudo-random numbers and seeds*.

> "My coin lands heads every single time. I flipped it ten times."

```python exec
id: heads-every-time-1
# Guess:
# Test:
# What happened:

import random

flips = []
for flip in range(10):
    random.seed(42)
    flips.append(random.choice(["heads", "tails"]))

print(flips)
```

```predict
type: choice

Before you run it: what will the ten flips be?

- A mix of heads and tails, different on every run
  - `random.choice` picks at random each time.
- A mix of heads and tails, the same on every run
  - The seed makes the whole list repeat.
- Ten of the same
  - Something about where the seed is set.
```

```hint
What does `random.seed(42)` do to the numbers that come after it? How many
times does it run here?
```

```inputs
len(flips)
flips.count("heads")
```

```solution
import random

random.seed(42)
flips = []
for flip in range(10):
    flips.append(random.choice(["heads", "tails"]))

print(flips)
---
A seed sets where the random numbers start. Set inside the loop, it goes
back to the same start before every flip, so every flip is the first flip.
Set once, before the loop, it lets the flips continue from that start.
With seed 42, the ten flips have eight heads and two tails.
```

## 4. A cipher that crashes

> "My Caesar cipher works on `hello`. On a longer sentence, it stops with
> `IndexError: string index out of range`. The error does not say which
> letter."

The cipher moves each letter a number of places along the alphabet.

```python exec
id: a-cipher-that-crashes-1
alphabet = "abcdefghijklmnopqrstuvwxyz"

def shift(text, steps):
    coded = ""
    for letter in text:
        if letter in alphabet:
            position = alphabet.index(letter)
            coded = coded + alphabet[position + steps]
        else:
            coded = coded + letter
    return coded

print(shift("hello", 3))
print(shift("the quick brown fox jumps over the lazy dog", 3))
```

Can you find the smallest text that still crashes? Then fix `shift`.

```python exec
id: a-cipher-that-crashes-2
# Guess:
# Test:
# What happened:

print(shift("the quick brown fox", 3))
```

```hint
Cut the sentence in half. Which half still crashes? Then cut that half in
half, until one letter is left.
```

```inputs
shift("hello", 3)
shift("xyz", 3)
shift("the quick brown fox jumps over the lazy dog", 3)
shift("abc", 26)     # all the way round
```

```solution
def shift(text, steps):
    coded = ""
    for letter in text:
        if letter in alphabet:
            position = alphabet.index(letter)
            coded = coded + alphabet[(position + steps) % 26]
        else:
            coded = coded + letter
    return coded
---
The smallest text that crashes is one letter: `x`, `y` or `z`. The
position of `x` is 23, and 23 + 3 is 26, past the last index, 25. `% 26`
takes the remainder after dividing by 26, so 26 becomes 0, the index of
`a`. The alphabet goes round in a circle.
```

## 5. Symptom or cause?

**a.** A web page shows a total that is always 3 too high. Somebody adds
`- 3` to the line that prints the total. Is that a fix for the symptom, or
for the cause? What could go wrong next month?

<details class="dl-answer"><summary>one way through it</summary>

It is a fix for the symptom. The total now looks right, and the cause, the
line that adds 3 too many, is still there. If the cause changes, say the
extra 3 becomes 4 when somebody adds a new item, the `- 3` makes the total
wrong again, and it hides where the real mistake is.

</details>

**b.** In the tutorial, the dungeon game crashed only sometimes. Why did a
seed help, before we fixed anything?

<details class="dl-answer"><summary>one way through it</summary>

With a seed, the program makes the same "random" numbers on every run. So
the crash happened every time, at the same turn. A test that can pass by
luck says very little. With the seed, a test of a fix meant something.

</details>

## 6. A problem nobody has shown you

This one has no bug. It is a problem you have not met, and the steps for
it are like the steps for a bug.

A dungeon is a square of rooms, four rooms by four. You start in the room
at the top left. The treasure is in the room at the bottom right. From any
room, you can go one room to the right, or one room down. You cannot go
left or up.

How many different paths reach the treasure?

Before you do anything else, write a guess in the cell.

**First, make sure you understand the question.** What counts as a
different path? Is right, right, down, down the same path as down, down,
right, right?

**Then try smaller dungeons.** How many paths are there in a dungeon of
one room? Of two rooms by two? Of three by three? Draw them, or list the
moves.

**Then look for a plan.** Think about any room. From which rooms can you
arrive in it? How many paths reach it, if you know how many reach those
rooms?

```python exec
id: a-problem-nobody-has-shown-you-1
# My guess for four by four:

def paths(rows, columns):
    ...
```

```hint
Every room in the top row has only one path to it: right, right, right.
The same is true for every room in the left column. What about the room
at row 1, column 1?
```

```hint
after: 8 runs
title: some steps
1. Make a grid of counts, one for each room, all 1 to start with:
   `counts = [[1] * columns for row in range(rows)]`.
2. For every room not in the top row or the left column, its count is the
   count of the room above plus the count of the room to the left.
3. Visit the rooms row by row, from the top, so the rooms above and
   to the left always have their counts already.
4. The answer is the count in the bottom-right room.

**Think about:** does your answer for three by three match the paths you
listed by hand?
```

```inputs
paths(1, 1)
paths(2, 2)
paths(3, 3)
paths(4, 4)
paths(3, 5)    # a dungeon that is not square
```

```solution
def paths(rows, columns):
    counts = [[1] * columns for row in range(rows)]
    for row in range(1, rows):
        for column in range(1, columns):
            counts[row][column] = counts[row - 1][column] + counts[row][column - 1]
    return counts[rows - 1][columns - 1]
---
Four by four has 20 paths. The small dungeons give 1, 2 and 6, and the
next two squares give 70 and 252.

Each path has three moves right and three moves down, in some order.
```

**Now look back.** Does your answer for three by three match what you
found by hand? Would the same plan work for a dungeon with a wall in one
room?

You used four steps: you made sure you understood the question, you made a
plan, you followed the plan, and you looked back at the answer. The
mathematician George Pólya wrote these four steps down in 1945, in a book
called *How to Solve It*. Trying smaller cases was part of the plan, in the
same way that the smallest example helps to find a bug.
