---
title: "Classes and objects: keeping data and actions together — Practice"
practice_for: objects-and-classes
year: "2026-2027"
version: 2026.09.26.1
---

# Classes and objects: keeping data and actions together — Practice

This page has problems on classes, objects and printing them, and three
from earlier pages. Try each problem before you open anything under it, and run the
cells to test your guesses.

## 1. Two characters

```python exec
id: one-thing-many-parts-1
class Character:
    def __init__(self, name, health):
        self.name = name
        self.health = health

    def take_damage(self, amount):
        self.health = max(0, self.health - amount)

ada = Character("Ada", 10)
grace = Character("Grace", 10)
ada.take_damage(4)
print(grace.health)
```

```predict
type: number

What will it print?
```

<details class="dl-answer"><summary>why</summary>

`10`. Only Ada was hit. Inside `take_damage`, `self` is the object the
call was made on, so `ada.take_damage(4)` changes `ada.health` and never
touches Grace's.

</details>

## 2. A constructor without self

```python exec
id: a-constructor-without-self-1
class Moon:
    def __init__(name, width):
        self.name = name
        self.width = width

io = Moon("Io", 3643)
```

```question
id: a-constructor-without-self-q1
type: multiple-choice
answer: 2

Before you run it: what will the error say?

- `name 'self' is not defined`
  - `self` is used inside `__init__`, but never made.
- `Moon.__init__() takes 2 positional arguments but 3 were given`
  - Python passes the new object in first, and there is no parameter for it.
- Nothing: it makes the moon.
  - `__init__` has a parameter for the name and one for the width.
```

<details class="dl-answer"><summary>why</summary>

A `TypeError`: `Moon.__init__() takes 2 positional arguments but 3 were
given`. Python passes the new object in as the first argument, then
`"Io"` and `3643`: three in all, for two parameters. The line should read
`def __init__(self, name, width):`.

</details>

## 3. A class of your own making

Can you write a `Specimen` class for things an ocean expedition finds? It
stores a name and the depth it was found at, in metres. Build a specimen
called `"anglerfish"`, found at 1500 m.

```python exec
id: a-class-of-your-own-making-1
# Your Specimen class here

fish = Specimen("anglerfish", 1500)
print(fish.name, fish.depth)
```

```inputs
fish.name
fish.depth
Specimen("sea cucumber", 4000).depth
```

```solution
class Specimen:
    def __init__(self, name, depth):
        self.name = name
        self.depth = depth

fish = Specimen("anglerfish", 1500)
print(fish.name, fish.depth)
---
`anglerfish 1500`. Every `__init__` has this shape: `self` first, then
what the object needs to start with, each stored on `self`.
```

## 4. What self is for

What does a method have in its parameters that a plain function does
not? What is it for?

<details class="dl-answer"><summary>one answer</summary>

It has `self`, always first. A method is called through an object, as in
`grace.take_damage(5)`, and Python gives that object to the method as
`self`. Through `self`, the method knows whose fields to read and change. A
plain function is not called through an object, so it has no `self`.

</details>

## 5. A submarine in a list

```python exec
id: objects-and-classes-practice-printing-1
class Submarine:
    def __init__(self, name):
        self.name = name
        self.depth = 0

    def __str__(self):
        return f"{self.name} at {self.depth} m"

nautilus = Submarine("Nautilus")
print(nautilus)
print([nautilus])
```

```question
id: a-submarine-in-a-list-q1
type: multiple-choice
answer: 2

What will the second line show?

- `[Nautilus at 0 m]`
  - `__str__` gives the text for an object wherever it appears.
- Something like `[<__dewlab__.Submarine object at 0x...>]`
  - An object inside a list is shown with `__repr__`, not `__str__`.
```

<details class="dl-answer"><summary>why</summary>

`Nautilus at 0 m`, from `__str__`, then the long memory form. The number
at the end is different each time. An object inside a list is shown with
`__repr__`, and this class does not have one yet.

</details>

## 6. Code that builds it again

Can you give `Submarine` a `__repr__`, so that the list shows
`[Submarine('Nautilus')]`?

```python exec
id: code-that-builds-it-again-1
class Submarine:
    def __init__(self, name):
        self.name = name
        self.depth = 0

    def __str__(self):
        return f"{self.name} at {self.depth} m"

nautilus = Submarine("Nautilus")
print([nautilus])
```

```inputs
repr(nautilus)
repr(Submarine("Alvin"))
str(nautilus)
```

```solution
class Submarine:
    def __init__(self, name):
        self.name = name
        self.depth = 0

    def __str__(self):
        return f"{self.name} at {self.depth} m"

    def __repr__(self):
        return f"Submarine('{self.name}')"

nautilus = Submarine("Nautilus")
print([nautilus])
---
`[Submarine('Nautilus')]`: the code that would build it again. The depth
is left out, because `Submarine(...)` takes only a name. `print(nautilus)`
still uses `__str__`.
```

## 7. A dictionary or a class?

A game keeps 30 characters, each with a name and a health, and one rule:
health never goes below 0. The same game keeps a list of 30 place names,
with nothing to check. Which would you keep as a class, and which as a
plain list or dictionary?

<details class="dl-answer"><summary>one answer</summary>

Keep the characters as a class. There is a rule to keep, and a method is
one place to keep it. Keep the place names as a plain list. A name has no
rule and no actions, so a class would only add code. There is room to
disagree here. A place might grow a description, or exits to other
places, and then a class becomes useful.

</details>

## 8. From earlier: a name that is not there

From *Dictionaries: looking things up by name*.

```python exec
id: from-earlier-a-name-that-is-not-there-1
health = {"Ada": 10, "Grace": 8}
print(health.get("Alan", 0))
```

```predict
What will it print?

- 0
  - `.get()` gives the default when the key is missing.
- An error
  - There is no key `"Alan"`.
```

<details class="dl-answer"><summary>why</summary>

`0`. `health["Alan"]` would stop with a `KeyError`, but `.get()` returns
its second value, the default, when the key is missing.

</details>

## 9. From earlier: one list, two names

From *Comprehensions, grids and aliasing*.

```python exec
id: from-earlier-one-list-two-names-1
def add_hit(hits, amount):
    hits.append(amount)
    return len(hits)

ada_hits = [3]
count = add_hit(ada_hits, 5)
print(ada_hits)
```

```predict
What will it print?

- [3, 5]
  - `hits` and `ada_hits` are two names for one list.
- [3]
  - The function changed its own copy.
```

<details class="dl-answer"><summary>why</summary>

`[3, 5]`. The function gets the list itself, not a copy, so `append`
changes the one list both names point to. An object passed to a method
works the same way.

</details>

## 10. From earlier: counting with a condition

From *Repeating steps with loops*. How many of these depths are deeper
than 1000 m? Can you write a loop that counts them?

```python exec
id: from-earlier-counting-with-a-condition-1
depths = [120, 1500, 800, 4000, 1000]
deep = 0

print(deep)
```

```inputs
deep
```

```solution
depths = [120, 1500, 800, 4000, 1000]
deep = 0
for depth in depths:
    if depth > 1000:
        deep = deep + 1
print(deep)
---
2: 1500 and 4000. 1000 is not deeper than 1000, so `>` leaves it out.
```
