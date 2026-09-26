---
title: "Running Python in a cell"
year: "2026-2027"
version: 2026.09.26.1
---

# Running Python in a cell

Here is something this course builds. Press **Run**, and it throws 100,000
darts at a square, one at a time, and uses the ones that land inside a
circle to work out π. You do not need to read the code yet.

```python exec
id: a-trailer-1
import random

inside = 0
for dart in range(1, 100001):
    x = random.random()
    y = random.random()
    if x * x + y * y <= 1:
        inside = inside + 1
    if dart in [10, 100, 1000, 10000, 100000]:
        print(dart, "darts: pi is about", 4 * inside / dart)
```

What happens to the estimate as the darts go up? Run it again: are the
numbers the same? You will build this yourself in
[Monte Carlo simulation: estimating π with random darts](tutorial:counting-darts),
and find out why more darts help, and how much.

That is Computational Methods: Python on problems too big, or too
tedious, to do by hand. It turns pictures with matrices, writes text from
the words of a book, simulates chance and queues, and races algorithms.
On most pages the tasks come in worlds, and you choose one on each page:
photos and filters, sprites, starships and space scenes; living systems,
queues and the way things spread; mazes, maps, collections and puzzles.
The page remembers your choice.

Everything runs in the box above: a *cell*. This page is about how cells
work, and what to do when one does not do what you expect.

## How a cell works

To run a cell, press its **Run** button, or hold Ctrl and press Enter.
Everything runs in this browser, on the computer in front of you: nothing
installs, and nothing you type leaves it. What will appear under this
cell?

```python exec
id: first-run
print("Running Python in a cell")
2 ** 10
```

```predict
What will the last line under the cell be?

- 1024
  - The last line is worked out, and its value is shown.
- 2 ** 10
  - Python shows the line as it is written.
- Nothing
  - Only `print()` shows anything.
```

The area under a cell shows two kinds of thing:

- anything the code prints with `print()`;
- the value of the last line, if that line is an expression.

An *expression* is a piece of code that has a value, such as `2 ** 10`,
which is 2 to the power of 10. Some lines are instructions instead. An
instruction, such as `total = 5`, does a job, but has no value to show.
Change the last line to `total = 2 ** 10`, and run it again: the printed
line appears, and nothing else.

The arithmetic operators, including `//` and `%`, which later pages use a
great deal, are in
[Algorithms, pseudocode and your first Python](tutorial:first-steps#a-few-more-things-python-can-do).
It is worth reading that section before the next page.

## Reading code that is not a cell

Not every piece of code on a page is meant to be run. A block like this
one is there to be read:

```python
total = 0
for value in [1, 2, 3]:
    total = total + value
```

How can you tell the difference? Look for the **Run** button. A block with
no Run button is an *illustration*: code for you to read. It is real code,
and you are welcome to copy it into a cell to try it.

{{include: setup/when-a-cell-does-not-do-what-you-expect.md}}

## Looking back

The trailer gives a different estimate every time it runs. Is it still an
answer? What would make you trust it more?

A challenge: change the dart game to find the chance that a dart lands
below the line from one corner of the square to the other, where
`x + y <= 1`. Before you run it, what should the chance be?

```python challenge
import random

darts = 100000
below = 0
for dart in range(darts):
    x = random.random()
    y = random.random()
    # Count the darts where x + y <= 1.
print(below / darts)
```

## Where to go next

This page is about the cells. The Python inside them comes from eight
Programming Foundations pages, which come next in this series. You may be
doing them in your programming class at the same time. The later pages in
this course use all eight:

1. [Variables, data types and text](tutorial:storing-and-computing):
   giving a value a name, and putting numbers into text.
2. [Making decisions with if, elif and else](tutorial:making-decisions):
   choosing what to do with `if`.
3. [Reading an error message](tutorial:reading-an-error-message): what
   Python is telling you when a cell stops.
4. [Repeating steps with loops](tutorial:repeating-yourself): `for`,
   `while`, and a loop inside a loop.
5. [Writing your own functions](tutorial:writing-your-own-functions):
   `def` and `return`. Nearly every matrix page asks you to write one.
6. [Lists and looping over them](tutorial:lists-and-sequences): many
   values under one name, and a loop that goes through them.
7. [Comprehensions, grids and aliasing](tutorial:comprehensions-and-grids):
   a loop on one line, and a grid stored as a list of lists.
8. [Dictionaries: looking things up by name](tutorial:looking-things-up-by-name):
   the tool behind the text-generation pages.

## Where to read more

Everything here is covered elsewhere too, often in a form that will suit you
better than this one.

Python Software Foundation. *The Python Tutorial*, section 3.1, "Using
Python as a Calculator". <https://docs.python.org/3/tutorial/introduction.html>.
The official walk through a first program: printing, arithmetic, and the
difference between an instruction and an expression, for anyone who wants
the same ground covered a second way.

Khan Academy. *Intro to Python Fundamentals*.
<https://www.khanacademy.org/computing/intro-to-python-fundamentals>. A
slower course through the same first ideas, with its own practice
problems, if one cell was not enough.
