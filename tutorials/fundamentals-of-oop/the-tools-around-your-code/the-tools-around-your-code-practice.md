---
title: "The Tools Around Your Code — Practice"
slug: the-tools-around-your-code-practice
practice_for: the-tools-around-your-code
module: fundamentals-of-oop
module_title: "Fundamentals of Object Oriented Programming"
year: "2026-2027"
series: programming-with-objects
version: 2026.09.05.1
---

# The Tools Around Your Code — Practice

Answers are folded. Several of these ask you to predict an output before
running anything. Resist checking first — being wrong and finding out why
is worth more than being right by accident.

## An Environment You Are Already In

**1.** In your own words: what does a page like this one already have in
common with dewmini?

<details class="dl-answer"><summary>answer</summary>

The same editor and the same Python underneath. This page runs one
script and forgets it when you leave. dewmini is the same tool, grown
into several cells and several files that are still there when you come
back.

</details>

## Errors Worth Reading

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

**2.** Try running the cell above. Before reading the error message
closely, see if you can guess which word in the code is wrong.

<details class="dl-answer"><summary>answer</summary>

`totall`, on the last line. The class stores its value in `self.total`,
one `l`. The message names the object's actual attributes. That is
usually enough on its own to spot a typo like this, without reading the
rest of the traceback.

</details>

**3.** Now try fixing the typo and running the cell again. What does it
print, and why not `5` or `3` alone?

<details class="dl-answer"><summary>answer</summary>

`8`. Both calls to `add()` ran, each time increasing `self.total` by
the amount passed in — `0 + 5`, then `5 + 3`. `counter.total` is
whatever the last `add()` left it at, not just the most recent amount.

</details>

**4.** Here is a second broken cell. Predict what the error message will
name as wrong, without running it first.

```python
class Timer:
    def start():
        self.running = True


timer = Timer()
timer.start()
```

<details class="dl-answer"><summary>answer</summary>

`start()` is missing `self` as its first parameter, the same mistake
covered in *Objects and Classes*' own practice. Calling `timer.start()`
passes `timer` in as the first argument regardless, so Python complains
that `start()` was given one argument too many.

</details>

## What the Editor Already Knows

**5.** You are midway through typing `pri` in a cell, and a list of
matching names appears with `print` among them. What is the editor
actually using to build that list — a fixed dictionary of Python
keywords, or something else?

<details class="dl-answer"><summary>answer</summary>

Something else: the names actually available right now, in this cell
and in whatever earlier cells have already run. That is why `basket`, a
name you defined yourself, showed up in the tutorial's own example
alongside a built-in like `print`.

</details>

## Where a Bigger Project Lives

**6.** A classmate writes a `Shape` class in `shapes.py`, using dewmini's
Files panel, then imports it into a notebook with `import shapes`. What
would they need to type to create a `Shape` object and check its area,
assuming `Shape` has an `area()` method?

<details class="dl-answer"><summary>answer</summary>

```python
import shapes

my_shape = shapes.Shape(...)
print(my_shape.area())
```

The exact arguments to `Shape(...)` depend on how its `__init__` is
written, but the shape of it — module name, dot, class name — is the
same as calling anything else from an imported module.

</details>

**7.** A cell has been running for over a minute, stuck in a loop that
never ends. What in dewmini stops it without closing the tab?

<details class="dl-answer"><summary>answer</summary>

The **Stop** button next to that cell. It interrupts the runaway cell
right away, rather than waiting for it to finish. Stuck in a loop that
never ends, it never would.

</details>

**8.** The Workbench's Variables list updates every time a cell runs.
What question is it there to answer, in one sentence?

<details class="dl-answer"><summary>answer</summary>

"Did that work?" — a running summary of every name in the session, its
type, and a short description of its value, so you do not have to
print everything twice just to check.

</details>
