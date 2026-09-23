---
title: "Running Python in a cell"
year: "2026-2027"
version: 2026.09.22.1
---

# Running Python in a cell

In Computational Methods, we use Python to work with matrices, run
simulations and test algorithms. Every page has *cells*. A cell is a
small box of Python code that you can change and run, right on the page.
This page shows how a cell works, and what to do when one does not do
what you expect.

Everything on this page runs in your own browser. Nothing installs, and
nothing you type leaves the computer in front of you. If you break a
cell and cannot fix it, its **reset** button brings back the code the
page started with.

If you have already done
[Algorithms, pseudocode and your first Python](tutorial:first-steps) in
your programming class, most of this page will look familiar. The
section on what to do when a cell fails is still worth a read.

## Running your first cell

To run a cell, press its **Run** button, or hold Ctrl and press Enter.
Whatever the code produces appears under the cell.

```python exec
id: first-run
hint: Change 3 to another number and run it again.
for step in range(3):
    print("step", step)
```

Did three lines appear? This cell uses a *loop*. A loop is a line, or a
group of lines, that Python repeats. We learn how loops work in
[Repeating steps with loops](tutorial:repeating-yourself). For now, try
the hint: change the 3 to another number, and run the cell again. What
changes?

The area under a cell shows two kinds of thing:

- anything the code prints with `print()`
- the value of the last line, if that line is an expression

An *expression* is a piece of code that has a value, such as `2 + 3`.
Some lines are instructions instead. An instruction, such as
`total = 5`, does a job, but it has no value to show.

The next cell has no `print()`. Its only line is an expression, so the
cell shows its value. `**` means "to the power of". What do you think
`2 ** 10` is? Run the cell to check.

```python exec
id: last-expression
2 ** 10
```

## A little arithmetic

Python works as a calculator. These are its arithmetic operators:

| Operator | What it does | Example | Result |
|---|---|---|---|
| `+` | adds | `22 + 4` | `26` |
| `-` | subtracts | `22 - 4` | `18` |
| `*` | multiplies | `22 * 4` | `88` |
| `/` | divides | `22 / 4` | `5.5` |
| `//` | divides, then rounds down to a whole number | `22 // 4` | `5` |
| `%` | gives the remainder after dividing | `22 % 4` | `2` |
| `**` | raises to a power | `2 ** 3` | `8` |

The last three may be new to you. What do you think each line of the
next cell will show? Run it to check.

```python exec
id: a-little-arithmetic-1
print(17 / 5)
print(17 // 5)
print(17 % 5)
```

5 goes into 17 three times, with 2 left over. `/` gives 3.4. `//`
gives the 3, and `%` gives the 2. The `%` operator is called *modulo*. It is useful more
often than you might expect. For example, `10 % 2` is 0, and that tells
us 10 is even.

## Reading code that is not a cell

Not every piece of code on a page is meant to be run. A block like this
one is there to be read:

```python
total = 0
for value in [1, 2, 3]:
    total = total + value
```

How can you tell the difference? Look for the **Run** button. A block
with no Run button is an *illustration*: code for you to read. It is
real code, and you are welcome to copy it into a cell to try it.

## When a cell does not do what you expect

A cell can fail when nothing is wrong with the site. Here are three
things to try, in this order.

**Reset the cell.** The reset button next to Run brings back the code
the page started with. If the cell works again after that, the problem
was in an edit, not in the page.

**Run the cells above it.** A later cell often uses something that an
earlier cell made. The cells on a page share their work, so the order
you run them in matters. The small **⋯** button beside Run opens "Run
this cell and all above". It runs every cell before this one, from the
top of the page.

**Reload the page.** This starts Python again, fresh. It does not
delete anything you have saved. Your work is kept in this browser, on
this device.

When a cell stops with an error, Python shows an error message. The
section "Reading a Traceback" in
[Reading an error message](tutorial:reading-an-error-message#reading-a-traceback)
shows what an error message tells you, line by line.

If none of the three things explains it, click the small circle beside
a cell's hint. It opens a report with your code and the cell's last
output already in it, so there is nothing to copy. The line at the
bottom of every page does the same for the whole page.

## Where to go next

This page is about the cells. The Python inside them comes from seven
Programming Foundations pages, which come next in this series. You may
be doing them in your programming class at the same time. The later
pages in this course use all seven:

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
6. [Lists: keeping many values in order](tutorial:lists-and-sequences):
   lists, comprehensions, and a grid stored as a list of lists.
7. [Dictionaries: looking things up by name](tutorial:looking-things-up-by-name):
   the tool behind the text-generation pages.

## Where to Read More

Python Software Foundation. *The Python Tutorial — An Informal Introduction
to Python.* <https://docs.python.org/3/tutorial/introduction.html>. The
official walk through what a first program does — printing, arithmetic, and
the difference between an instruction and an expression — for anyone who
wants the same ground covered a second way.

Khan Academy. *Intro to Python Fundamentals.*
<https://www.khanacademy.org/computing/intro-to-python-fundamentals>. A
slower course through the same first ideas, with its own practice problems,
if one cell was not enough.
