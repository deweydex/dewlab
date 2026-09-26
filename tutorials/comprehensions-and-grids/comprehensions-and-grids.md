---
title: "Comprehensions, grids and aliasing"
year: "2026-2027"
version: 2026.09.26.1
worlds:
  secret-messages: Codes and hidden messages, the kind spies and puzzle-setters make.
  pixel-art: Pictures made of small squares, the way a screen draws them.
covers:
  comprehensions-a-loop-that-builds-a-list:
    covers: [MIT-6.3]
  a-grid-is-a-list-of-lists:
    covers: [MIT-6.3, MIT-6.5]
  two-names-for-one-list:
    covers: [MIT-6.3]
  mathematical-sequences-as-functions:
    covers: [MIT-6.2]
  the-dot-product-lists-meet-arithmetic:
    covers: [MIT-6.3]
---

# Comprehensions, grids and aliasing

Here is a list of squares built twice: once with a loop, the way
[Lists and looping over them](tutorial:lists-and-sequences) built lists,
and once on a single line. Will the two lists be the same?

```python exec
id: two-ways-to-build-1
squares = []
for n in range(1, 6):
    squares.append(n * n)
print(squares)

squares_again = [n * n for n in range(1, 6)]
print(squares == squares_again)
```

```predict
What will the last line print?

- True
  - Both make the squares of 1 to 5, in the same order.
- False
  - They are two separate lists, so they cannot be equal.
```

It prints `True`. `==` compares what two lists hold, element by element,
and both hold `[1, 4, 9, 16, 25]`. The one-line version is a
*comprehension*, and it is where this page starts. After it, a whole
picture goes into a list of lists, and then we meet the thing about lists
most likely to catch you out: two names for one list.

## Comprehensions: a loop that builds a list

A *list comprehension* is a loop that builds a list, written on one line
inside square brackets. Here are the two versions from above, one over the
other:

```python
squares = []
for n in range(1, 6):
    squares.append(n * n)

squares = [n * n for n in range(1, 6)]
```

To turn the loop into a comprehension:

1. Write the value you would append: `n * n`.
2. After it, write the `for` line, without its colon:
   `for n in range(1, 6)`.
3. Put square brackets round the whole thing.

Read it out loud as "a list of `n * n`, for each `n` in `range(1, 6)`". A
comprehension can go through any list, and the value at the front can be
any calculation. What do you think each line will show?

```python exec
id: comprehensions-a-loop-that-builds-a-list-1
words = ["MEET", "ME", "AT", "NOON"]
print([len(word) for word in words])
print([word[0] for word in words])

row = [30, 90, 250, 120]
print([255 - value for value in row])
```

The first list holds each word's length, and the second each word's first
letter. The third turns a row of pixels into its negative: black becomes
white, and white becomes black.

### Keeping only some values

In a loop, an `if` inside it decides which values to keep. In a
comprehension, the `if` goes at the end. Which values will each line keep?

```python exec
id: comprehensions-a-loop-that-builds-a-list-2
row = [30, 90, 250, 120, 250, 60]
print([value for value in row if value >= 128])

message = "MEET AT NOON"
print([letter for letter in message if letter != " "])
```

An `if` at the end of a comprehension is a *filter*: it keeps only the
values that pass a test. Here the tests are `value >= 128` and
`letter != " "`.

### Inside sum(), max() and join()

Python's own `sum()` adds up the values it is given, and `max()` gives the
largest. `join()` joins strings into one: the string before the dot goes
between the pieces. The first two lines here look almost the same. What is
different about them?

```python exec
id: comprehensions-a-loop-that-builds-a-list-3
row = [30, 90, 250, 120, 250, 60]
print(sum([value for value in row if value >= 128]))
print(sum(value for value in row if value >= 128))
print(sum(1 for value in row if value >= 128))
print(max(row))

words = ["MEET", "ME", "AT", "NOON"]
print(" ".join(words))
print("".join(word[0] for word in words))
```

The first two lines both print 500. The second has no square brackets.
When a comprehension is the only thing inside a function's brackets, its
square brackets can go. It is then a *generator expression*: it makes its
values one at a time and hands each one to the function, without building a
list first.

The third line counts. It adds 1 for each pixel of 128 or more, so it
prints 2. In the last two lines, `" "` puts a space between the words, and
`""` puts nothing between the first letters.

### Your turn

<div class="dl-world" data-world="secret-messages">

An *acrostic* hides a message in the first letters of other words. Can you
set `hidden` to the word these first letters make, with `join()` and a
generator expression?

```python exec
id: your-turn-1--secret-messages
words = ["REPORT", "UNDER", "NIGHTFALL"]
hidden = ""
print(hidden)
```

```inputs
hidden
```

```hint
`word[0]` is a word's first letter. What goes before `.join`, if nothing
should come between the letters?
```

```solution
words = ["REPORT", "UNDER", "NIGHTFALL"]
hidden = "".join(word[0] for word in words)
print(hidden)
---
RUN. Try hiding a word of your own in a list of words, and see whether
someone else spots it.
```

</div>

<div class="dl-world" data-world="pixel-art">

Can you set `brighter` to this row with 50 added to every pixel, but never
above 255? `min(a, b)` gives the smaller of two values.

```python exec
id: your-turn-1--pixel-art
row = [30, 90, 250, 120, 210, 60]
brighter = []
print(brighter)
```

```inputs
brighter
```

```hint
For one pixel, the new value is the smaller of `value + 50` and 255. Can
you put that at the front of a comprehension?
```

```solution
row = [30, 90, 250, 120, 210, 60]
brighter = [min(value + 50, 255) for value in row]
print(brighter)
---
`[80, 140, 255, 170, 255, 110]`. Without `min()`, 250 would become 300, a
brightness no screen has.
```

</div>

## A grid is a list of lists

A list can hold other lists. A picture, a board or a table is a grid, and a
list of lists keeps a grid with one inner list for each row. To read one
value, we give two indexes. Before you run the cell, what will
`picture[1][3]` be?

```python exec
id: a-grid-is-a-list-of-lists-1
picture = [
    [0, 0, 1, 0, 0],
    [0, 0, 1, 1, 0],
    [1, 1, 1, 1, 1],
    [0, 0, 1, 1, 0],
    [0, 0, 1, 0, 0],
]
print(picture[1][3])
```

```predict
What will it print?

- 1
  - The first index picks row 1, and the second picks column 3 in it.
- 0
  - Across 3 and down 1, the way a graph gives x before y.
```

It prints 1. `picture[1]` is a whole row, `[0, 0, 1, 1, 0]`, and `[3]`
picks one element from that row. So a grid's index is the row first, then
the column: down, then across. A graph gives x first, across, so the two
orders are easy to mix up. Swap the two numbers and run it again.

To draw the grid, a loop goes through the rows, and a loop inside it goes
through the values in each row, as the nested loops did in
[Repeating steps with loops](tutorial:repeating-yourself):

```python exec
id: a-grid-is-a-list-of-lists-2
picture = [
    [0, 0, 1, 0, 0],
    [0, 0, 1, 1, 0],
    [1, 1, 1, 1, 1],
    [0, 0, 1, 1, 0],
    [0, 0, 1, 0, 0],
]
for row in picture:
    line = ""
    for value in row:
        if value == 1:
            line = line + "#"
        else:
            line = line + "."
    print(line)
```

### Building a grid

Two small tools help to build a grid. `[0] * 4` repeats a list, and makes
`[0, 0, 0, 0]`. And when a loop never uses its loop variable, Python
programmers often name it `_`, an underscore, which tells the reader "this
value is not used".

```python exec
id: a-grid-is-a-list-of-lists-3
size = 3
grid = [[0] * size for _ in range(size)]
print(grid)

times_table = [[row * column for column in range(1, 4)] for row in range(1, 4)]
print(times_table)
print(times_table[1][2])
```

The comprehension runs `[0] * size` once each time round, so it makes a
new row of zeros three times. `times_table` has a comprehension inside a
comprehension: the inner one builds one row, and the outer one does that
for each `row` from 1 to 3. Counting from 0, `times_table[1][2]` is row 1,
column 2, and that is 2 × 3, which is 6.

If your course goes on to matrices, as Computational Methods does in
[Matrices: adding, scaling and transposing a grid of numbers](tutorial:grid-of-numbers),
every grid there is kept like this.

### Your turn

<div class="dl-world" data-world="secret-messages">

A *Polybius square* codes each letter as two numbers: its row and its
column in a grid of the alphabet. There are 25 squares, so I and J share
one. These pairs spell a word, counting from 0 the way Python does. Can
you set `word` to it?

```python exec
id: your-turn-2--secret-messages
square = [
    ["A", "B", "C", "D", "E"],
    ["F", "G", "H", "I", "K"],
    ["L", "M", "N", "O", "P"],
    ["Q", "R", "S", "T", "U"],
    ["V", "W", "X", "Y", "Z"],
]
pairs = [[1, 2], [0, 4], [2, 0], [2, 4]]
word = ""

print(word)
```

```inputs
word
```

```hint
`for row, column in pairs:` takes each pair apart, the way `enumerate()`
pairs were taken apart. Which letter is at that row and column?
```

```solution
square = [
    ["A", "B", "C", "D", "E"],
    ["F", "G", "H", "I", "K"],
    ["L", "M", "N", "O", "P"],
    ["Q", "R", "S", "T", "U"],
    ["V", "W", "X", "Y", "Z"],
]
pairs = [[1, 2], [0, 4], [2, 0], [2, 4]]
word = ""
for row, column in pairs:
    word = word + square[row][column]
print(word)
---
HELP. The Greek historian Polybius described a grid like this for
signalling with torches: the number raised on the left gave the row, and
the number on the right gave the column.
```

</div>

<div class="dl-world" data-world="pixel-art">

Can you set `negative` to the same picture with every 1 turned into 0, and
every 0 into 1? A comprehension inside a comprehension can do it.

```python exec
id: your-turn-2--pixel-art
picture = [
    [0, 0, 1, 0, 0],
    [0, 1, 1, 1, 0],
    [1, 1, 1, 1, 1],
]
negative = []

print(negative)
```

```inputs
negative
```

```hint
For one value, `1 - value` swaps 0 and 1. Can you build one row that way
first, and then put a comprehension round it for every row?
```

```solution
picture = [
    [0, 0, 1, 0, 0],
    [0, 1, 1, 1, 0],
    [1, 1, 1, 1, 1],
]
negative = [[1 - value for value in row] for row in picture]
print(negative)
---
The inner comprehension makes one row, and the outer one does it for every
row. `picture` itself is unchanged: the comprehension built a new grid.
```

</div>

## Two names for one list

A list can have more than one name. Before you run this cell, what will
`row` hold at the end?

```python exec
id: two-names-for-one-list-1
row = [0, 0, 0, 0]
copy = row
copy[0] = 255
print(row)
```

```predict
What will it print?

- [0, 0, 0, 0]
  - `copy` is a copy, so changing it leaves `row` alone.
- [255, 0, 0, 0]
  - `copy` and `row` are two names for the same list.
- An error
  - A list cannot be given a second name.
```

It prints `[255, 0, 0, 0]`. The line `copy = row` did not copy anything.
It gave the same list a second name. Think of the list as a box and each
name as a label on it: `copy = row` puts a second label on the same box,
so a change made through one name shows through the other. Two names for
one value is called *aliasing*.

To get a separate list, make one. `row[:]`, a slice from the start to the
end, is a new list with the same elements, and so is `list(row)`.

```python exec
id: two-names-for-one-list-2
row = [0, 0, 0, 0]
copy = row[:]
copy[0] = 255
print(row)
print(copy)
```

Numbers and strings never cause this. They cannot be changed in place, so
`=` can only give a name a new value, and the other names keep the old one.

### Inside a function

A function's parameter is one more name. In
[Writing your own functions](tutorial:writing-your-own-functions), giving
a name a new value inside a function left everything outside alone. What
happens when the function changes a list in place?

```python exec
id: two-names-for-one-list-3
def brighten(pixels):
    for index in range(len(pixels)):
        pixels[index] = pixels[index] + 10

row = [10, 20, 30]
brighten(row)
print(row)
```

It prints `[20, 30, 40]`: the function changed the caller's list. It did
not give `pixels` a new value with `=`. It changed the list that `pixels`
names, which is the same list `row` names. So there are two different
actions. Giving a name a new value stays inside the function. Changing a
list in place is seen by every name for that list.

A function that changes what it was given can surprise the person who
calls it. Decide on purpose whether a function returns a new list or
changes the one it was given, and let its name say which.

### The grid that was one row

Why build a grid with a comprehension, and not with `[[0] * 3] * 3`? The
cell below changes one value in each.

```python exec
id: two-names-for-one-list-4
shortcut = [[0] * 3] * 3
shortcut[0][0] = 5
print(shortcut)

grid = [[0] * 3 for _ in range(3)]
grid[0][0] = 5
print(grid)
```

In `shortcut`, one change shows up in all three rows. `* 3` did not make
three rows: it put the same row into the outer list three times. There is
one row, with three names. The comprehension ran `[0] * 3` three times, and
made three separate rows.

The same thing happens when a grid is copied with `grid[:]`. That makes a
new outer list, and puts the same rows in it. To copy the rows too, copy
each one: `[row[:] for row in grid]`.

### Your turn

<div class="dl-world" data-world="secret-messages">

This code is meant to keep a message, and make a coded copy of it. It
loses the message. Can you see why, and fix it?

```python exec
id: your-turn-3--secret-messages
message = ["M", "E", "E", "T"]
coded = message
for index in range(len(coded)):
    coded[index] = chr((ord(coded[index]) - ord("A") + 3) % 26 + ord("A"))
print(message)
print(coded)
```

```inputs
message
coded
```

```hint
After `coded = message`, how many lists are there? How could `coded`
start as a separate list with the same letters?
```

```solution
message = ["M", "E", "E", "T"]
coded = message[:]
for index in range(len(coded)):
    coded[index] = chr((ord(coded[index]) - ord("A") + 3) % 26 + ord("A"))
print(message)
print(coded)
---
With `message[:]`, `coded` starts as a new list, so the loop changes only
that one. The message stays `MEET`, and the code is `PHHW`.
```

</div>

<div class="dl-world" data-world="pixel-art">

This code is meant to keep a row of pixels, and make a darker copy of it.
It loses the original. Can you see why, and fix it?

```python exec
id: your-turn-3--pixel-art
row = [200, 150, 100, 50]
darker = row
for index in range(len(darker)):
    darker[index] = darker[index] // 2
print(row)
print(darker)
```

```inputs
row
darker
```

```hint
After `darker = row`, how many lists are there? How could `darker` start
as a separate list with the same pixels?
```

```solution
row = [200, 150, 100, 50]
darker = row[:]
for index in range(len(darker)):
    darker[index] = darker[index] // 2
print(row)
print(darker)
---
With `row[:]`, `darker` starts as a new list, so the loop changes only
that one. A comprehension would do it too, and build the new list as it
goes: `darker = [value // 2 for value in row]`.
```

</div>

## Mathematical sequences as functions

In mathematics, a *sequence* is a list of numbers made by a rule. The rule
is a function: it takes a position, $n$, and gives back the value at that
position. The square numbers $1, 4, 9, 16, 25, \ldots$ come from the rule
$f(n) = n^2$. The triangular numbers $1, 3, 6, 10, 15, \ldots$ come from
$f(n) = \frac{n(n+1)}{2}$, which is the same as $\sum_{i=1}^{n} i$, the sum
of the whole numbers from 1 to $n$.

```python exec
id: mathematical-sequences-as-functions-1
def square_number(n):
    return n ** 2

def triangular_number(n):
    return n * (n + 1) // 2

print([square_number(n) for n in range(1, 9)])
print([triangular_number(n) for n in range(1, 9)])
```

### Your turn

A function can be passed to another function, like any other value.
`square_number` without brackets is the function itself, and
`square_number(3)` is what it gives back for 3. Can you write
`generate_sequence(rule, n)`, which returns a list of the first `n` terms
of the sequence that `rule` makes?

```python exec
id: your-turn-4
def square_number(n):
    return n ** 2

def triangular_number(n):
    return n * (n + 1) // 2

def generate_sequence(rule, n):
    return []
```

```inputs
guess: yes
generate_sequence(square_number, 5)
generate_sequence(triangular_number, 5)
generate_sequence(square_number, 0)     # no terms at all
```

```hint
The terms are at positions 1 to `n`. Inside the function, `rule(i)` is the
term at position `i`. Can a comprehension collect them?
```

```solution
def square_number(n):
    return n ** 2

def triangular_number(n):
    return n * (n + 1) // 2

def generate_sequence(rule, n):
    return [rule(i) for i in range(1, n + 1)]
---
`range(1, n + 1)` starts at position 1 and stops after `n`. With `n` as 0,
the range is empty, and so is the list.
```

## The dot product: lists meet arithmetic

When two lists have the same length, we can pair them up element by
element. The *dot product* of two lists multiplies each pair, and adds up
the results:

$$\vec{a} \cdot \vec{b} = \sum_{i=0}^{n-1} a_i \times b_i$$

So $[1, 2, 3] \cdot [4, 5, 6] = 1 \times 4 + 2 \times 5 + 3 \times 6 = 32$.
A dot product turns up whenever some parts count for more than others: a
weighted average, a check digit, how bright a colour looks.

### Your turn

<div class="dl-world" data-world="secret-messages">

A code can catch mistakes as well as hide things. An old book number, an
ISBN-10, has ten digits. Weight them 10, 9, 8 and so on down to 1, and the
dot product of the digits and the weights can always be divided by 11. If
one digit is copied wrongly, it no longer can. Can you write
`dot_product(a, b)`, and use it to check the number 0-306-40615-2?

```python exec
id: your-turn-5--secret-messages
def dot_product(a, b):
    return 0

digits = [0, 3, 0, 6, 4, 0, 6, 1, 5, 2]
weights = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
print(dot_product(digits, weights) % 11)
```

```inputs
guess: yes
dot_product([1, 2, 3], [4, 5, 6])
dot_product(digits, weights)
dot_product([], [])
```

```hint
Loop over every index with `range(len(a))`. At each index, multiply the
two elements, and add the result to a running total.
```

```solution
def dot_product(a, b):
    total = 0
    for index in range(len(a)):
        total = total + a[index] * b[index]
    return total

digits = [0, 3, 0, 6, 4, 0, 6, 1, 5, 2]
weights = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
print(dot_product(digits, weights) % 11)
---
The dot product is 132, which is 11 × 12, so the remainder is 0. Change
one digit, and see the remainder change. What should `dot_product` do when
the two lists have different lengths? This one stops with an `IndexError`
when `b` is shorter, and ignores the extra when it is longer.
[Designing and testing good functions](tutorial:building-reusable-tools)
shows how to make it refuse on purpose.
```

</div>

<div class="dl-world" data-world="pixel-art">

An eye sees green as brighter than red, and red as brighter than blue. So
a colour's brightness is a dot product: its red, green and blue, weighted
0.299, 0.587 and 0.114. Can you write `dot_product(a, b)`, and use it to
find how bright the colour (200, 40, 90) looks?

```python exec
id: your-turn-5--pixel-art
def dot_product(a, b):
    return 0

weights = [0.299, 0.587, 0.114]
colour = [200, 40, 90]
print(dot_product(weights, colour))
```

```inputs
guess: yes
dot_product([1, 2, 3], [4, 5, 6])
dot_product(weights, colour)
dot_product(weights, [255, 255, 255])    # white
```

```hint
Loop over every index with `range(len(a))`. At each index, multiply the
two elements, and add the result to a running total.
```

```solution
def dot_product(a, b):
    total = 0
    for index in range(len(a)):
        total = total + a[index] * b[index]
    return total

weights = [0.299, 0.587, 0.114]
colour = [200, 40, 90]
print(dot_product(weights, colour))
---
About 93.5, where a plain average says 110: the red is strong, but red
counts for less than green. The weights add up to 1, so white comes out
at 255. What should `dot_product` do when the two lists have different
lengths? This one stops with an `IndexError` when `b` is shorter, and
ignores the extra when it is longer.
[Designing and testing good functions](tutorial:building-reusable-tools)
shows how to make it refuse on purpose.
```

</div>

## Looking back

Two names for one list is the idea on this page most likely to catch you
out, weeks from now, in a program much longer than these. When is it
useful that a function can change the list it was given? When does it
cause trouble?

A challenge: write a message in rows of four letters, then read it down
the columns. That is a *transposition cipher*, and the same move turns a
grid on its side. Can you build the columns from the rows, and read the
coded message off them? Can you get the message back?

```python challenge
# Write the message in rows of four, then read it down the columns.
message = "MEETMEATNOONXXXX"
rows = [[letter for letter in message[start:start + 4]]
        for start in range(0, len(message), 4)]
for row in rows:
    print(row)
# Build the columns: column 0 is the first letter of every row.
```

The next page,
[Looking things up by name](tutorial:looking-things-up-by-name), keeps
values under names of their own choosing, and uses one to hold a cipher's
key.

## Where to read more

Everything here is covered elsewhere too, often in a form that will suit you
better than this one.

Batchelder, N. (2015). *Facts and myths about Python names and values*.
PyCon 2015. <https://nedbatchelder.com/text/names.html>. The clearest
account there is of two names for one list, with pictures of names and
values, and why a function can change what it was given.

Python Software Foundation. *The Python Tutorial*, sections 5.1.3 and
5.1.4, "List Comprehensions" and "Nested List Comprehensions".
<https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions>.
The official reference for comprehensions, including one that turns a grid
on its side.

Sanderson, G. (3Blue1Brown) (2016). *Essence of Linear Algebra, Chapter 9:
Dot Products and Duality*. <https://www.youtube.com/watch?v=LyGKycYT2v0>.
The dot product this page meets as arithmetic, seen as geometry instead.
