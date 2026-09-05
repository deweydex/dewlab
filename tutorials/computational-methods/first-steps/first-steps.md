---
title: "First Steps"
slug: first-steps
module: computational-methods
module_title: "Computational Methods"
year: "2026-2027"
series: python-fundamentals
version: 2026.08.23.1
---

# First Steps

Everything on this page runs in your own browser. Nothing installs, nothing is
submitted, and nothing you type here leaves the machine you are sitting at. If
you break a cell beyond repair, the **reset** button puts the author's version
back.

## Running your first cell

A cell is a small piece of Python you can edit and run. Press **Run**, or hold
Ctrl and press Enter, and whatever the code produces appears directly
underneath it.

```python exec
id: first-run
hint: Change 3 to another number and run it again.
for step in range(3):
    print("step", step)
```

Two things show up in the output area: anything the code prints, and the value
of the last line if that line is an expression rather than an instruction. The
cell below ends in an expression, so its value is shown without any `print`.

```python exec
id: last-expression
2 ** 10
```

## Reading code that is not a cell

Not every piece of code on a page is meant to be run. A block like this one is
there to be read:

```python
total = 0
for value in [1, 2, 3]:
    total = total + value
```

You can tell the difference by looking for the **Run** button. If there isn't
one, the code is an illustration.

## When a cell does not do what you expect

A cell can fail without anything being wrong with the site. Three things are
worth trying, in this order.

**Reset the cell.** The button next to Run puts back the code the tutorial
started with. If the cell works again after that, an edit was the cause, not
the page.

**Run the cells above it.** A later cell often needs something an earlier one
set up. The small **⋯** button beside Run opens "Run this cell and all
above," which runs every cell before this one from the top.

**Reload the page.** This starts Python fresh. It clears nothing you have
saved — your work is kept in this browser, on this device.

[When It Goes Wrong](tutorial:when-it-goes-wrong#reading-a-traceback) covers
what an error message is actually telling you, line by line.

If none of the three explain it, click the small circle beside a cell's
hint. It opens a report with your code and the cell's last output already
included, nothing to copy. The line at the foot of every page does the same
for the page as a whole, rather than one cell.

## Where to go next

The next tutorial in this series works with a table of data rather than single
values. See [working with a table](tutorial:working-with-tables#the-shared-table)
when you are ready.

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
