---
title: "Repeating steps with loops"
year: "2026-2027"
version: 2026.09.26.1
worlds:
  secret-messages: Codes and hidden messages, the kind spies and puzzle-setters make.
  pixel-art: Pictures made of small squares, the way a screen draws them.
covers:
  while-loops-repeat-until-done:
    covers: [PDP-LO6]
  for-loops-when-you-know-how-many-times:
    covers: [PDP-LO6, MIT-6.7]
  sigma-notation-mathematics-meets-loops:
    covers: [MIT-6.4]
  nested-loops:
    covers: [PDP-LO6]
  building-up-gradually-counting-with-conditions:
    covers: [MIT-6.7]
---

# Repeating steps with loops

On [Variables, data types and text](tutorial:storing-and-computing), moving
a whole word three places along meant writing the same line once for every
letter. Here is a loop that does it for every letter, however long the
word. What will it print?

```python exec
id: a-loop-that-codes-1
word = "CAT"
coded = ""
for letter in word:
    position = ord(letter) - ord("A")
    coded = coded + chr((position + 3) % 26 + ord("A"))
print(coded)
```

```predict
type: text

What will it print?
```

It prints `FDW`: C moved to F, A to D, and T to W. The indented lines ran
three times, once for each letter of `CAT`, and each time round `letter`
held the next one. Change the word to your own name, in capitals, and run
it again. The loop does not care how long it is.

Our programs can run lines in order, and make decisions. This page adds
the third thing every program is built from: repetition.

## While loops: repeat until done

A *while loop* runs its body again and again, for as long as a condition
stays `True`. It is for "keep going until…". Here a square pattern keeps
doubling in size, until the next doubling would no longer fit on a canvas
64 pixels wide.

```python exec
id: while-loops-repeat-until-done-1
side = 1
while side * 2 <= 64:
    side = side * 2
    print(side)
print("Done")
```

```predict
type: number

What is the last number it prints?
```

It prints 2, 4, 8, 16, 32 and 64, then `Done`. After 64, doubling again
would make 128, so the condition is `False` and the loop stops.

A while loop needs three things:

1. a starting state: `side = 1`
2. a condition that Python checks before each time round: `side * 2 <= 64`
3. a change inside the body that, in the end, makes the condition `False`:
   `side = side * 2`

What happens without the third one? The condition never becomes `False`,
so the loop never stops. It is worth seeing once. While a cell is running,
its **Run** button changes to **Stop**: press it to stop the loop. (If you
do not see a Stop button, reloading the page stops it too.)

### Trace it by hand

Before you run the next cell, write the values of `total` and `n` for each
time round in the comments at the bottom. What will it print at the end?

```python exec
id: your-turn-1
total = 0
n = 1

while n <= 4:
    total = total + n
    n = n + 1

print(total)

# Your trace:
# n=1: total becomes ?, n becomes ?
# n=2: total becomes ?, n becomes ?
# n=3: total becomes ?, n becomes ?
# n=4: total becomes ?, n becomes ?
```

It adds 1 + 2 + 3 + 4. It starts a total at zero, then adds to it again and
again. This is the *accumulator pattern*, one of the most common shapes in
programming. `coded` in the first cell on this page was an accumulator too,
of letters instead of numbers.

### Your turn

<div class="dl-world" data-world="secret-messages">

In English, E is the most common letter. So in a message moved along by a
Caesar shift, the most common letter is probably E, moved. Suppose the most
common letter in a coded message is Q. Can you try shifts 0, 1, 2 and so on,
until moving Q back by the shift gives E? Which shift is it?

```python exec
id: your-turn-2--secret-messages
letter = "Q"
shift = 0

print(shift)
```

```inputs
shift
```

```hint
The condition is "moving Q back by `shift` does not give E yet". Moving
back is the Caesar shift with `- shift` in place of `+ shift`.
```

```solution
letter = "Q"
shift = 0
while chr((ord(letter) - ord("A") - shift) % 26 + ord("A")) != "E":
    shift = shift + 1
print(shift)
---
The shift is 12. A code-breaker who finds it can move every letter of the
message back by 12. This is the oldest way of breaking a Caesar shift:
count the letters.
```

</div>

<div class="dl-world" data-world="pixel-art">

A pattern starts 3 pixels wide, and each step makes it 5 pixels wider. How
many steps until it is at least 64 pixels wide?

```python exec
id: your-turn-2--pixel-art
width = 3
steps = 0

print(steps)
```

```inputs
steps
width
```

```hint
Keep going while the width is less than 64. Inside the loop, two things
change: the width, and the count of steps.
```

```solution
width = 3
steps = 0
while width < 64:
    width = width + 5
    steps = steps + 1
print(steps)
---
Thirteen steps, and the pattern ends 68 pixels wide. A while loop suits
this because nobody knew the number of steps in advance: the loop found it.
```

</div>

## For loops: when you know how many times

When we know how many times to repeat, or have something to go through one
item at a time, a *for loop* is simpler. It runs its body once for each item
in a sequence: each letter of a string, as in the first cell, or each number
`range()` gives.

```python exec
id: for-loops-when-you-know-how-many-times-1
for i in range(5):
    print(i)
```

```predict
type: number

What will the last line be?
```

`range(5)` gives five numbers, 0, 1, 2, 3 and 4, starting from 0. So the
last line is 4, not 5. Starting from 0 turns out to be very useful, and
[Lists: keeping many values in order](tutorial:lists-and-sequences) shows
why.

`range()` can also take a start and a step:

```python exec
id: for-loops-when-you-know-how-many-times-2
for i in range(1, 6):
    print(i, end=" ")      # end=" " keeps the next print on the same line
print()

for i in range(0, 20, 5):
    print(i, end=" ")
print()

for i in range(10, 0, -1):
    print(i, end=" ")
print("Liftoff!")
```

| Call | Numbers it gives |
|---|---|
| `range(stop)` | from 0 up to, but not including, `stop` |
| `range(start, stop)` | from `start` up to, but not including, `stop` |
| `range(start, stop, step)` | from `start`, jumping by `step`, stopping before `stop` |

### Your turn

<div class="dl-world" data-world="secret-messages">

A code-breaker's table shows every letter beside the letter it becomes.
Can you print the whole alphabet, 26 lines, each with a letter and that
letter moved three places along? `A D`, `B E`, and so on, to `Z C`.

```python exec
id: your-turn-3--secret-messages
# 26 lines: each letter, and where a shift of 3 moves it

```

```hint
`range(26)` gives the positions 0 to 25. `chr(position + ord("A"))` turns
a position back into a letter.
```

```solution
for position in range(26):
    letter = chr(position + ord("A"))
    moved = chr((position + 3) % 26 + ord("A"))
    print(letter, moved)
---
Read from the right-hand column back to the left, and the same table
decodes a message.
```

</div>

<div class="dl-world" data-world="pixel-art">

Can you print one row of a checkerboard 16 pixels wide: `#` in the even
columns and `.` in the odd ones, all on one line?

```python exec
id: your-turn-3--pixel-art
# One row, 16 pixels: #.#.#.#.#.#.#.#.

```

```hint
`range(16)` gives the columns 0 to 15. `print("#", end="")` prints without
starting a new line.
```

```solution
for column in range(16):
    if column % 2 == 0:
        print("#", end="")
    else:
        print(".", end="")
print()
---
The last `print()` ends the line. Without it, whatever the next cell prints
would carry on from the end of this row.
```

</div>

## Sigma notation: mathematics meets loops

Mathematicians have a short way to write sums. Instead of
$1 + 2 + 3 + 4 + 5$, they write:

$$\sum_{i=1}^{5} i$$

The large symbol is the capital Greek letter sigma. It means "add up the
expression, for each value of $i$ from 1 to 5." The variable $i$ is
called the *index* of the sum.

Does that sound like something we have already written? It is exactly
what a loop with an accumulator does.

```python exec
id: sigma-notation-mathematics-meets-loops-1
# Computing the sum from i=1 to i=5 of i
total = 0
for i in range(1, 6):     # 1 through 5
    total = total + i
print("Sum:", total)       # should be 15
```

The notation is not a new subject. It writes down the same five
decisions you already make when you write that loop:

| The decision | In $\sum_{i=1}^{5} i$ | In the loop |
|---|---|---|
| What the index is called | the $i$ under the sigma | the `i` in `for i in ...` |
| Where it starts | the $1$ in $i = 1$ | the `1` in `range(1, 6)` |
| Where it stops | the $5$ above the sigma | the `6` in `range(1, 6)` |
| What gets accumulated | the $i$ after the sigma | the `+ i` in `total = total + i` |
| What the total starts at | nothing — it is assumed | `total = 0`, written out |

Two of those rows need a closer look.

The stopping row is the one that trips people up. Sigma stops **at** 5,
and `range` stops **before** 6. So the two numbers differ by one, but
they describe the same five values. The number in `range` marks a
boundary, not an item. We will see the same idea again with slices, in
[Lists: keeping many values in order](tutorial:lists-and-sequences).

The last row is a real difference between the two. Sigma never writes
down that the total starts at zero: a sum of nothing is zero, and
mathematicians leave that unsaid. A loop has to say it out loud. That is
why `total = 0` sits above every accumulator you write.

We can make this more general. $\sum_{i=1}^{n} i^2$ means "add up the
squares of all the integers from 1 to n":

```python exec
id: sigma-notation-mathematics-meets-loops-2
# Sum of squares from 1 to 10
n = 10
total = 0
for i in range(1, n + 1):
    total = total + i ** 2
print("Sum of squares from 1 to " + str(n) + ":", total)
```

There is also a notation for products, using the capital Greek letter
pi: $\prod_{i=1}^{n} i$ means "multiply all the integers from 1 to n."
This is the factorial function, written with `!`:
$5! = 1 \times 2 \times 3 \times 4 \times 5 = 120.$

```python exec
id: sigma-notation-mathematics-meets-loops-3
# Computing 5! (factorial of 5) using the product pattern
n = 5
product = 1               # start at 1 for multiplication, not 0
for i in range(1, n + 1):
    product = product * i
print(str(n) + "! =", product)
```

Why does `product` start at 1 and not at 0? What would happen if it
started at 0?

A sum starts at 0, because adding 0 changes nothing. A product starts at
1, because multiplying by 1 changes nothing. In mathematics, 0 is called
the identity element for addition, and 1 is the identity element for
multiplication.

### Your turn

Can you work out each of these with a loop? For each one, write
pseudocode first, then the code.

1. $\sum_{i=1}^{100} i$, the sum of the first 100 natural numbers. (There
   is a famous story that the young Gauss worked this out in moments.)
2. $\sum_{i=1}^{10} \frac{1}{i}$, the first 10 terms of the *harmonic
   series*. The harmonic series is the sum
   $1 + \frac{1}{2} + \frac{1}{3} + \frac{1}{4} + \dots$
3. $10!$, which is 10 factorial.

```python exec
id: your-turn-3
# Pseudocode:
#
#

# 1. Sum of first 100 natural numbers
```

```python exec
id: your-turn-4
# 2. First 10 terms of the harmonic series
```

```hint
`1 / i` gives a float. What would `1 // i` give instead, and why would
the total come out as 1?
```

```python exec
id: your-turn-5
# 3. 10 factorial
```

## Nested loops

A loop can hold another loop. These are *nested loops*. For each single
time round the outer loop, the inner loop runs all the way through. What do
you think this one draws?

```python exec
id: nested-loops-1
for row in range(4):
    for column in range(8):
        if (row + column) % 2 == 0:
            print("#", end="")
        else:
            print(".", end="")
    print()   # end the row
```

A checkerboard, four rows of eight. The outer loop runs 4 times, and for
each of those the inner loop runs 8 times, so the `if` runs 32 times, once
for every pixel. `(row + column) % 2` is what shifts each row along by one.

If the outer loop runs $n$ times, and the inner loop runs $n$ times for
each, the total is $n \times n$, or $n^2$. Counting the steps an algorithm
takes matters a great deal when we come to searching and sorting, in
[Searching a list: linear and binary search](tutorial:finding-things) and
[Sorting a list: bubble, insertion and selection sort](tutorial:putting-things-in-order).

### Your turn

<div class="dl-world" data-world="secret-messages">

Can you print a table of the first five letters, A to E, moved by the
shifts 1, 2 and 3, one row for each shift? The first row is `B C D E F`.

```python exec
id: your-turn-6--secret-messages
# One row per shift: 1, 2 and 3

```

```hint
The outer loop picks a shift. The inner loop goes through the positions 0
to 4, and prints each moved letter with `end=" "`.
```

```solution
for shift in range(1, 4):
    for position in range(5):
        print(chr((position + shift) % 26 + ord("A")), end=" ")
    print()
---
Each row is the alphabet slid one place further along. A cipher table
like this, with all 26 rows, was once printed on cards for people who
sent coded messages by hand.
```

</div>

<div class="dl-world" data-world="pixel-art">

Can you draw a hollow square, 6 pixels by 6: `#` round the edge, and `.`
inside?

```python exec
id: your-turn-6--pixel-art
# A 6 by 6 square: # on the edges, . inside

```

```hint
A pixel is on the edge when its row is the first or the last, or its
column is the first or the last. That is four comparisons joined by `or`.
```

```solution
size = 6
for row in range(size):
    for column in range(size):
        if row == 0 or row == size - 1 or column == 0 or column == size - 1:
            print("#", end="")
        else:
            print(".", end="")
    print()
---
Change `size` and the same loops draw a square of any size. The edge is
row 0 and row `size - 1`, because the rows are numbered from 0.
```

</div>

## Building up gradually: counting with conditions

An `if` inside a loop lets us count, or add, only some of the values. How
many numbers from 1 to 100 can be divided by both 3 and 7? Can you guess
before you run it?

```python exec
id: building-up-gradually-counting-with-conditions-1
count = 0
for i in range(1, 101):
    if i % 3 == 0 and i % 7 == 0:
        count = count + 1
        print(i, end=" ")
print()
print("Total:", count)
```

Four: 21, 42, 63 and 84. A number divided by both 3 and 7 is divided by 21,
so the loop could have asked `i % 21 == 0`, and found the same four.

### Your turn

<div class="dl-world" data-world="secret-messages">

Code-breakers count letters. How many E's are in this message? Can you
count them with a loop?

```python exec
id: your-turn-7--secret-messages
message = "MEET ME BY THE OLD TREE"
count = 0

print(count)
```

```inputs
count
```

```solution
title: with what you've met so far
message = "MEET ME BY THE OLD TREE"
count = 0
for letter in message:
    if letter == "E":
        count = count + 1
print(count)
---
Six. Counting every letter this way, and finding the most common, is the
first step in breaking a Caesar shift.
```

```solution
title: a shorter way you'll meet later
message = "MEET ME BY THE OLD TREE"
count = message.count("E")
print(count)
---
A string can count its own characters. It is the same loop, written by
somebody else.
```

</div>

<div class="dl-world" data-world="pixel-art">

A row of a picture is written as text: `#` for a lit pixel and `.` for a
dark one. How many pixels are lit in this row? Can you count them with a
loop?

```python exec
id: your-turn-7--pixel-art
row = "..##.###..#"
count = 0

print(count)
```

```inputs
count
```

```solution
title: with what you've met so far
row = "..##.###..#"
count = 0
for pixel in row:
    if pixel == "#":
        count = count + 1
print(count)
```

```solution
title: a shorter way you'll meet later
row = "..##.###..#"
count = row.count("#")
print(count)
---
A string can count its own characters. It is the same loop, written by
somebody else.
```

</div>

## Looking back

Sigma writes down a loop, and a loop with an accumulator works out a sum.
Which parts of $\sum_{i=1}^{5} i$ does a mathematician leave unsaid, that
a program has to say out loud?

A challenge: this message was moved along by a Caesar shift, but nobody
told you by how much. Can you try all 26 shifts, and print what each one
gives? One of them reads as English.

```python challenge
# Try every shift. Which one reads as English?
message = "WKLV LV D VHFUHW"
for shift in range(26):
    decoded = ""
    for letter in message:
        # Move each capital back by shift. Leave the spaces alone.
        decoded = decoded + letter
    print(shift, decoded)
```

The first cell on this page did one word with one loop. Next,
[Writing your own functions](tutorial:writing-your-own-functions) gives a
loop like that a name, so you can use it again without writing it out.

## Where to read more

Khan Academy. *Sigma Notation for Sums.*
<https://www.youtube.com/watch?v=5jwXThH6fg4>. The mathematical side of the
accumulator pattern this page builds: the same $\sum$ notation, worked
through on paper.

Python Software Foundation. *The Python Tutorial — More Control Flow
Tools.* <https://docs.python.org/3/tutorial/controlflow.html>. The official
reference for `for`, `range()`, and the rest of Python's looping tools,
including a few this page does not have room for.
