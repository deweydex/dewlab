---
title: "Your development environment: the tools around your code — Practice"
practice_for: the-tools-around-your-code
year: "2026-2027"
version: 2026.09.05.1
---

# Your development environment: the tools around your code — Practice

The answers are hidden in folds under each problem. Several problems ask
you to predict what a piece of code does. Try to answer before you run
anything. Being wrong and finding out why teaches you more than being
right by luck.

## An environment you are already in

**1.** In your own words, what does a page like this one have in
common with the dewlab Notebook?

<details class="dl-answer"><summary>answer</summary>

They have the same editor and the same Python underneath. This page
runs one script and forgets it when you leave. The Notebook is the same
tool, with more room: several cells and several files, which are still
there when you come back.

</details>

## Errors worth reading

```python exec
id: errors-worth-reading-1
class Counter:
    def __init__(self):
        self.total = 0

    def add(self, amount):
        self.total = self.total + amount


counter = Counter()
counter.add(5)
counter.add(3)
print(counter.totall)
```

**2.** Run the cell above. Before you read the error message closely,
can you guess which word in the code is wrong?

<details class="dl-answer"><summary>answer</summary>

`totall`, on the last line. The class stores its value in `self.total`,
with one `l`. The message says that a `'Counter' object has no
attribute 'totall'`, and then asks `Did you mean: 'total'?` That is
usually enough to spot a typo like this, without reading the rest of
the message.

</details>

**3.** Now fix the typo and run the cell again. What does it print?
Why not `5` or `3` on its own?

<details class="dl-answer"><summary>answer</summary>

It prints `8`. Both calls to `add()` ran, and each one increased
`self.total` by the amount passed in: first `0 + 5`, then `5 + 3`.
`counter.total` holds whatever the last `add()` left it at. It is not
only the most recent amount.

</details>

**4.** Here is a second broken cell. Without running it, predict what
the error message will say is wrong.

```python
class Timer:
    def start():
        self.running = True


timer = Timer()
timer.start()
```

<details class="dl-answer"><summary>answer</summary>

`start()` is missing `self` as its first parameter. It is the same
mistake as the `Dog` class in the practice for
[Classes and objects: keeping data and actions together](tutorial:objects-and-classes).
Calling `timer.start()` still passes `timer` in as the first argument.
So Python stops with a `TypeError`: `start()` takes 0 arguments, but 1
was given.

</details>

## What the editor already knows

**5.** You have typed `pri` in a cell, and a list of matching names
appears, with `print` among them. Where does the editor get that list?
Is it a fixed list of Python words, or something else?

<details class="dl-answer"><summary>answer</summary>

Something else. The list holds the names that exist right now: in this
cell, and in any earlier cells that have already run. That is why
`basket`, a name you made yourself, appeared in the tutorial's example,
next to a built-in name like `print`.

</details>

## Where a bigger project lives

**6.** A classmate writes a `Shape` class in `shapes.py`, using
the Notebook's Files panel. Then they import it into a notebook with
`import shapes`. `Shape` has an `area()` method. What would they type to
create a `Shape` object and check its area?

<details class="dl-answer"><summary>answer</summary>

```python
import shapes

my_shape = shapes.Shape(...)
print(my_shape.area())
```

The arguments inside `Shape(...)` depend on how its `__init__` is
written. The pattern is the same as using anything else from an
imported module: the module name, a dot, then the class name.

</details>

**7.** A cell has been running for over a minute, stuck in a loop that
never ends. What in the Notebook stops it, without closing the tab?

<details class="dl-answer"><summary>answer</summary>

The **Stop** button next to that cell. It stops the runaway cell right
away. You do not have to wait for it to finish on its own.

</details>

**8.** The Variables list in the Workbench updates every time a cell
runs. In one sentence, what question does it answer?

<details class="dl-answer"><summary>answer</summary>

"Did that work?" It shows every name in the session, with its type and
a short summary of its value, so you do not have to print everything a
second time to check.

</details>
