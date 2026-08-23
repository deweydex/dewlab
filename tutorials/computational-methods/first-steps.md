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

## Where to go next

The next tutorial in this series works with a table of data rather than single
values. See [working with a table](tutorial:working-with-tables#the-shared-table)
when you are ready.
