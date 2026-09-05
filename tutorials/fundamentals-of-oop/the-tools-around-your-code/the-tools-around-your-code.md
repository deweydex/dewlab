---
title: "The Tools Around Your Code"
slug: the-tools-around-your-code
module: fundamentals-of-oop
module_title: "Fundamentals of Object Oriented Programming"
year: "2026-2027"
series: programming-with-objects
version: 2026.09.05.1
covers:
  an-environment-you-are-already-in:
    covers: [FOOP-LO5]
  errors-worth-reading:
    covers: [FOOP-LO5]
  what-the-editor-already-knows:
    covers: [FOOP-LO5]
  where-a-bigger-project-lives:
    covers: [FOOP-LO5]
---

# The Tools Around Your Code

**Fundamentals of Object Oriented Programming**

Writing a class is one skill. Running it and finding out why it broke
is another. Both depend on the tools sitting around your code, not on
the code itself. This tutorial is about those tools: what a
*development environment* actually gives you. dewlab's own pages are a
small one already. dewmini is the bigger sibling, for a real project.

## An Environment You Are Already In

Every cell you have run so far, in every tutorial, already sits inside a
development environment. It edits your code, runs it, and shows you what
happened, all on this page. That is small on purpose: one script, one
job. `compose/dewmini.html` is the same editor and the same Python,
grown into several cells, several files, and work that is still there
when you come back. Learning what a page like this one already offers is
learning dewmini too, since the tool underneath is the same one.

## Errors Worth Reading

```python exec
id: errors-worth-reading-1
class Basket:
    def __init__(self):
        self.items = []

    def add(self, name, price):
        self.items.appendd((name, price))


basket = Basket()
basket.add("bread", 2.50)
print(basket.items)
```

Try running that cell. It fails — and that is the point here, not a
problem. The message on screen is worth reading slowly rather than
skimming past. It names the line and the mistake: `Basket` objects have
no method called `appendd`, and it usually names something close to
what you meant. A development environment's whole job, in this moment,
is to get you to that sentence as fast as possible. What is on screen is
trimmed down to your own code, not buried in everything Python did to
get there.

Now try changing `appendd` back to `append` and running the cell again.
The empty list was never the problem. One misspelled word was the
problem, and now you can see exactly why.

## What the Editor Already Knows

Click at the end of the comment in the cell below, press Enter, and
start typing `bas`. A short list of names appears before you finish the
word, `basket` among them — press Tab, or click it, to finish typing it
for you. Pause instead over a name already on the page, `Basket` in the cell
above included. Its docstring or its shape shows up, with no need to
scroll back to find it.

```python exec
id: what-the-editor-already-knows-1
# type here
```

Neither of those needed a lookup. The editor already knew, because it
was reading the same code you were. That is what an integrated
environment adds over a plain text file: it is not neutral about what
you are writing. It is helping.

## Where a Bigger Project Lives

A page like this one holds one script and no memory between visits. A
real project grows past that: several files, a class in one place used
from another, work you want to find again next week. That is exactly
what dewmini is for.

Three things there do a real project's actual work. **Files** is a real
filesystem. Write `shapes.py` in it, and a cell elsewhere can
`import shapes`, the way any real Python program is spread across
several files. **Variables**, in the Workbench, lists every name in your
current session: its type, and a short summary of its value. It
updates every time you run a cell, answering "did that work?" without
printing everything twice. A runaway cell is one stuck in a loop that
will not end. Press the **Stop** button next to it, and it stops right
away, rather than waiting to finish on its own.

None of this is a new set of instructions to learn. It is what an
environment does around the code you already know how to write. It
runs your code, shows you what broke, and keeps track of what you
named things. Your own thinking then stays on the problem, not on the
tool.
