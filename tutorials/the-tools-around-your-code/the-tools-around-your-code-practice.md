---
title: "Your development environment: finding a bug inside a class — Practice"
practice_for: the-tools-around-your-code
year: "2026-2027"
version: 2026.09.26.1
---

# Your development environment: finding a bug inside a class — Practice

Problems on reading tracebacks, printing what you need to see, and the
tools around your code, and three from earlier pages. Try each problem
before you open anything under it, and run the cells to test your
guesses.

## 1. Which line?

A crew's cook feeds everyone, and the cell stops with this traceback:

```text
Traceback (most recent call last):
  File "<cell galley-1>", line 20, in <module>
    galley.feed_everyone()
  File "<cell galley-1>", line 14, in feed_everyone
    member.eat(self.rations)
  File "<cell galley-1>", line 6, in eat
    self.hunger = self.hunger - food
TypeError: unsupported operand type(s) for -: 'int' and 'list'
```

```question
id: which-line-1
type: multiple-choice
answer: 2

`self.rations` is a list, with one ration for each member of the crew.
Which line most likely holds the mistake?

- Line 20, `galley.feed_everyone()`
  - The first line the error names is where the trouble started.
- Line 14, `member.eat(self.rations)`
  - `eat` expects one ration, and this line gives it the whole list.
- Line 6, `self.hunger = self.hunger - food`
  - The last line the error names is the one that failed.
```

<details class="dl-answer"><summary>why</summary>

Line 14. Line 6 failed, because it cannot take a list away from a number.
But `eat` was written for one ration, and line 14 handed it the whole list.
Line 6 is where the mistake showed. Line 14 is where it was made.

</details>

## 2. One letter too many

```python exec
id: one-letter-too-many-1
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

Run it. Before you read the whole error, can you find the wrong word from
its last line alone? Then fix it: what does the cell print?

<details class="dl-answer"><summary>answer</summary>

`totall`, on the last line, and the error's last line says so:
`'Counter' object has no attribute 'totall'. Did you mean: 'total'?`
Fixed, the cell prints `8`. Each `add()` changed `self.total`: first
0 + 5, then 5 + 3.

</details>

## 3. Missing self

```python exec
id: missing-self-1
class Timer:
    def start():
        self.running = True

timer = Timer()
timer.start()
```

```question
id: missing-self-q1
type: multiple-choice
answer: 1

Before you run it: what will the error say?

- `Timer.start() takes 0 positional arguments but 1 was given`
  - Python passes `timer` in, and `start` has no parameter for it.
- `name 'self' is not defined`
  - `self` is used, but never made.
- Nothing: it runs without an error.
  - `start` has no parameters, and the call gives it none.
```

<details class="dl-answer"><summary>why</summary>

A `TypeError`: `Timer.start() takes 0 positional arguments but 1 was
given`. `timer.start()` passes `timer` in as the first argument, as every
method call does, and `start` has no parameter to receive it. Python stops
there, before the line with `self` runs. Write `def start(self):`.

</details>

## 4. An average that is too big

A logbook should give the average depth of its dives. The Nautilus dived
120, 340, 85 and 210 metres, so the average is 188.75. Can you print
what you need inside `average_depth`, find the mistake, and fix it?

```python exec
id: an-average-that-is-too-big-1
class Logbook:
    def __init__(self, submarine, depths):
        self.submarine = submarine
        self.depths = depths

    def average_depth(self):
        total = 0
        count = 0
        for depth in self.depths:
            total = total + depth
        count = count + 1
        return total / count

log = Logbook("Nautilus", [120, 340, 85, 210])
print(log.average_depth())
```

```inputs
log.average_depth()
Logbook("Alvin", [45, 55]).average_depth()
```

```hint
Print `total` and `count` just before the `return`. Which of the two is
not what you expected?
```

```solution
class Logbook:
    def __init__(self, submarine, depths):
        self.submarine = submarine
        self.depths = depths

    def average_depth(self):
        total = 0
        count = 0
        for depth in self.depths:
            total = total + depth
            count = count + 1    # fixed: inside the loop
        return total / count

log = Logbook("Nautilus", [120, 340, 85, 210])
print(log.average_depth())
---
188.75. `count = count + 1` was not indented under the `for`, so it ran
once, after the loop, and the total was divided by 1. `len(self.depths)`
would count the dives without a loop at all.
```

## 5. Where the list comes from

You have typed `pri` in a cell, and a list of matching names appears,
with `print` among them. Where does the editor get that list? Is it a
fixed list of Python words, or something else?

<details class="dl-answer"><summary>answer</summary>

Something else. The list holds the names that exist right now: in this
cell, and in any earlier cells that have already run. That is why `grace`,
a name made in a cell, appeared on the tutorial page, next to a name
that comes with Python, such as `print`.

</details>

## 6. A class in another file

A classmate writes a `Shape` class in `shapes.py`, using the Notebook's
Files panel. Then they import it into a notebook with `import shapes`.
`Shape` has an `area()` method. What would they type to make a `Shape`
object and print its area?

<details class="dl-answer"><summary>answer</summary>

```python
import shapes

my_shape = shapes.Shape(...)
print(my_shape.area())
```

The values inside `Shape(...)` depend on how its `__init__` is written.
The pattern is the same as for anything else from an imported module: the
module's name, a dot, then the class's name.

</details>

## 7. A cell that never ends

A cell has been running for over a minute, stuck in a loop that never
ends. What in the Notebook stops it, without closing the tab? And what in
the Workbench would tell you, afterwards, what the loop's variables held?

<details class="dl-answer"><summary>answer</summary>

The **Stop** button next to the cell stops it at once. Then **Variables**,
in the Workbench, lists every name in the session with a short summary of
its value, so you can see how far the loop got without printing anything.

</details>

## 8. From earlier: a count that never counts

From *Sequence, selection and iteration inside a class*.

```python exec
id: from-earlier-a-count-that-never-counts-1
class Probe:
    def __init__(self, name):
        self.name = name
        self.burns = 0

    def burn(self):
        burns = self.burns + 1
        return burns

juno = Probe("Juno")
print(juno.burn())
print(juno.burn())
```

```predict
What will the second line print?

- 1
  - `burns` is a plain name, so `self.burns` stays at 0.
- 2
  - Each call adds one burn.
```

<details class="dl-answer"><summary>why</summary>

`1`, both times. `burn` adds 1 to `self.burns`, which gives 1, and
stores it in a plain name that vanishes when the method ends. `self.burns`
never changes, so the next call starts from 0 again. A `print()` of
`self.burns` inside `burn` would show 0 every time.

</details>

## 9. From earlier: an object in a list

From *Classes and objects*.

```python exec
id: from-earlier-an-object-in-a-list-1
class Character:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

ada = Character("Ada")
print(ada)
print([ada])
```

```question
id: from-earlier-an-object-in-a-list-q1
type: multiple-choice
answer: 2

What will the second line show?

- `['Ada']`
  - `__str__` gives the text for an object wherever it appears.
- Something like `[<__dewlab__.Character object at 0x...>]`
  - Inside a list, an object is shown with `__repr__`, not `__str__`.
```

<details class="dl-answer"><summary>why</summary>

The first line is `Ada`, from `__str__`. The second shows the long memory
form, because a list shows each object inside it with `__repr__`. Give
the class a `__repr__` as well, and the list shows that instead.

</details>

## 10. From earlier: three errors

From *Reading an error message*. Which error does each of these raise?

- (a) `int("twelve")`
- (b) `["rope", "lamp"][2]`
- (c) `"depth: " + 120`

<details class="dl-answer"><summary>answer</summary>

(a) A `ValueError`: `int()` wants a whole number written in digits.
(b) An `IndexError`: two items have indexes 0 and 1. (c) A `TypeError`:
`+` will not join a string to a number. `"depth: " + str(120)` works.

</details>
