---
title: "Sequence, selection and iteration inside a class"
year: "2026-2027"
version: 2026.09.26.1
worlds:
  game: A game world, with characters, the things they carry, and rooms.
  ocean: An ocean expedition, with a submarine, its crew, and what they find.
  solar-system: A solar system, with planets, moons and the probes sent to them.
  your-own: A world of your own, with a class you design and grow page by page.
covers:
  the-handful-of-moves:
    covers: [FOOP-LO2]
  storing-inside-a-class:
    covers: [FOOP-LO2]
  one-method-several-moves:
    covers: [FOOP-LO2]
---

# Sequence, selection and iteration inside a class

Jupiter has four large moons: Io, Europa, Ganymede and Callisto. Here is a
planet, written as a class, with a method that counts the moons wider than
a given width. Our own Moon is 3,475 km across. How many of Jupiter's four
are wider?

```python exec
id: the-handful-of-moves-1
class Planet:
    def __init__(self, name, moons):
        self.name = name
        self.moons = moons

    def moons_wider_than(self, km):
        count = 0
        for width in self.moons:
            if width > km:
                count = count + 1
        return count

# The widths of Io, Europa, Ganymede and Callisto, in kilometres
jupiter = Planet("Jupiter", [3643, 3122, 5268, 4821])
print(jupiter.moons_wider_than(3475))
```

```predict
What will it print?

- 3
  - Three of the four widths are more than 3475.
- 4
  - Every one of Jupiter's big moons is bigger than ours.
- 13732
  - `count` adds up the widths of the moons that pass.
```

It prints `3`. Io, Ganymede and Callisto are wider than our Moon. Europa,
at 3,122 km, is a little smaller. `count` grows by 1 for each moon that
passes, not by its width.

## The handful of moves

Nothing inside `moons_wider_than` is new. It is built from the moves you
used all through Programming Foundations, in
[Variables, data types and text](tutorial:storing-and-computing),
[Making decisions with if, elif and else](tutorial:making-decisions) and
[Repeating steps with loops](tutorial:repeating-yourself). There are four
of them:

| Move | What it does | In `moons_wider_than` |
|---|---|---|
| storing | keeps a value under a name, for a later line to use | `count = 0` |
| sequence | runs lines one after another, in the order they are written | its lines, from top to bottom |
| selection | chooses between paths | `if width > km:` |
| iteration | repeats a step | `for width in self.moons:` |

*Storing* is a program keeping a value under a name, so a later line can
use it. A *sequence* is a program's lines running one after another. A
*selection* is a program choosing between paths, usually with `if`. An
*iteration* is a program repeating a step, usually with a loop.

Which move is each of these lines? Choose one for each.

```question
id: label-the-moves-1
type: fill-in-the-blank

- `count = 0` is {storing|sequence|selection|iteration}.
- `for width in self.moons:` is {iteration|storing|sequence|selection}.
- `if width > km:` is {selection|storing|sequence|iteration}.
- `count = count + 1` is {storing|sequence|selection|iteration}.
- In `__init__`, `self.moons = moons` is {storing|sequence|selection|iteration}.
```

`count = count + 1` is storing, even though it looks like arithmetic.
First Python adds 1 to `count`, then it stores the result under
`count` again. And every line is also part of a sequence: nothing in a
method runs out of order.

## Storing inside a class

`count = 0` and `self.moons = moons` are both storing. But they keep their
values in different places. Here is a probe that counts its photos. What
does it print after two photos?

```python exec
id: storing-inside-a-class-1
class Probe:
    def __init__(self, name):
        self.name = name
        self.photos = 0

    def take_photo(self):
        photos = self.photos + 1

voyager = Probe("Voyager 1")
voyager.take_photo()
voyager.take_photo()
print(voyager.photos)
```

```predict
What will it print?

- 0
  - `photos` without `self.` is a different name from `self.photos`.
- 2
  - Each call adds one photo.
- 1
  - Each call adds one to the same starting value.
```

It prints `0`, and no error says why. `photos = self.photos + 1` stores
the new value under `photos`, a name that belongs to this one call of the
method. When the method ends, the name is gone, and the value with it.
`self.photos` never changed. Put `self.` in front of `photos` on that line,
and run it again: now it prints `2`.

So there are two places to store a value inside a class.

- **On the object**, with `self.`: the value stays with the object, from
  one method call to the next, and every method can reach it.
- **In a plain name**, inside a method: the value lasts only until the
  method ends.

`count` in `moons_wider_than` is meant to vanish. It is only needed while
the loop runs, and the next call starts from 0 again. A photo count is
meant to last, so it lives on `self`.

## One method, several moves

Finding the largest value in a list uses all four moves. The method
stores the best value so far, repeats a step for each value in the list,
and chooses whether each one is better than the best so far.

### Your turn

<div class="dl-world" data-world="game">

A backpack holds items, and the list keeps their weights in kilograms.
Can you give `Backpack` a `heaviest()` method that returns the largest
weight?

```python exec
id: one-method-several-moves-1--game
class Backpack:
    def __init__(self, owner, weights):
        self.owner = owner
        self.weights = weights

ada = Backpack("Ada", [2, 5, 1, 3])
print(ada.heaviest())
```

```inputs
Backpack("Ada", [2, 5, 1, 3]).heaviest()
Backpack("Grace", [4]).heaviest()
Backpack("Alan", [1, 1, 9]).heaviest()
```

```hint
What does the method need to remember as it goes through the list? That
is the storing move. What should it start as, before the loop looks at
anything?
```

```solution
class Backpack:
    def __init__(self, owner, weights):
        self.owner = owner
        self.weights = weights

    # The new method
    def heaviest(self):
        best = self.weights[0]
        for weight in self.weights:
            if weight > best:
                best = weight
        return best

ada = Backpack("Ada", [2, 5, 1, 3])
print(ada.heaviest())
---
5. `best` starts as the first weight, so the method works for weights of
any size. Python's `max(self.weights)` gives the same answer in one line:
this loop is what `max()` does inside. What should an empty backpack
return?
```

</div>

<div class="dl-world" data-world="ocean">

A submarine's logbook keeps the depth of each dive, in metres. Can you
give `Logbook` a `deepest()` method that returns the deepest dive?

```python exec
id: one-method-several-moves-1--ocean
class Logbook:
    def __init__(self, submarine, depths):
        self.submarine = submarine
        self.depths = depths

log = Logbook("Nautilus", [120, 340, 85, 210])
print(log.deepest())
```

```inputs
Logbook("Nautilus", [120, 340, 85, 210]).deepest()
Logbook("Alvin", [45]).deepest()
Logbook("Trieste", [10, 10, 10916]).deepest()
```

```hint
What does the method need to remember as it goes through the list? That
is the storing move. What should it start as, before the loop looks at
anything?
```

```solution
class Logbook:
    def __init__(self, submarine, depths):
        self.submarine = submarine
        self.depths = depths

    # The new method
    def deepest(self):
        best = self.depths[0]
        for depth in self.depths:
            if depth > best:
                best = depth
        return best

log = Logbook("Nautilus", [120, 340, 85, 210])
print(log.deepest())
---
340. `best` starts as the first depth, so the method works for any
depths. Python's `max(self.depths)` gives the same answer in one line:
this loop is what `max()` does inside. What should an empty logbook
return?
```

</div>

<div class="dl-world" data-world="solar-system">

Can you give `Planet` a `widest_moon()` method that returns the width
of its widest moon?

```python exec
id: one-method-several-moves-1--solar-system
class Planet:
    def __init__(self, name, moons):
        self.name = name
        self.moons = moons

    def moons_wider_than(self, km):
        count = 0
        for width in self.moons:
            if width > km:
                count = count + 1
        return count

jupiter = Planet("Jupiter", [3643, 3122, 5268, 4821])
print(jupiter.widest_moon())
```

```inputs
Planet("Jupiter", [3643, 3122, 5268, 4821]).widest_moon()
Planet("Earth", [3475]).widest_moon()
Planet("Mars", [22, 12]).widest_moon()
```

```hint
What does the method need to remember as it goes through the list? That
is the storing move. What should it start as, before the loop looks at
anything?
```

```solution
class Planet:
    def __init__(self, name, moons):
        self.name = name
        self.moons = moons

    def moons_wider_than(self, km):
        count = 0
        for width in self.moons:
            if width > km:
                count = count + 1
        return count

    # The new method
    def widest_moon(self):
        best = self.moons[0]
        for width in self.moons:
            if width > best:
                best = width
        return best

jupiter = Planet("Jupiter", [3643, 3122, 5268, 4821])
print(jupiter.widest_moon())
---
5268: Ganymede, the widest moon in the solar system. `best` starts as the
first width, so the method works for moons of any size. Python's
`max(self.moons)` gives the same answer in one line: this loop is what
`max()` does inside. What should a planet with no moons, such as Venus,
return?
```

</div>

<div class="dl-world" data-world="your-own">

Give a class in your world a list: the scores in a game, the fish in a
net, the heights of the trees in a forest. Can you write a method that
goes through the list and chooses? It might find the largest, the
smallest, or how many pass a test of your own.

```python exec
id: one-method-several-moves-1--your-own
# A class with a list, and a method that loops over it and chooses.
```

</div>

## Looking back

Every method on this page was built from storing, sequence, selection and
iteration. A class did not add a fifth move. What it added is a second
place to store a value: on the object, through `self`, where it lasts from
one method call to the next. In the method you wrote, which names should
last, and which should vanish when the method ends?

A challenge: a probe burns its fuel in steps of 10 kg, for as long as it
has at least 10 kg left. Can you write `burns_left()`, which counts how
many burns it can make, with a `while` loop? And can you count them
without using up the probe's fuel?

```python challenge
class Probe:
    def __init__(self, name, fuel):
        self.name = name
        self.fuel = fuel

    def burns_left(self):
        burns = 0
        # Repeat while there are at least 10 kg left.
        return burns

juno = Probe("Juno", 75)
print(juno.burns_left())
print(juno.fuel)
```

Next, [Your development environment: the tools around your code](tutorial:the-tools-around-your-code)
finds and fixes the mistakes that hide inside methods.

## Where to read more

Everything here is covered elsewhere too, often in a form that will suit you
better than this one.

Python Software Foundation. *The Python Tutorial*, section 4, "More Control
Flow Tools". <https://docs.python.org/3/tutorial/controlflow.html>. The
official tour of `if`, `for` and `while`, with more of what each can do
than this page shows.

Downey, A. B. (2015). *Think Python: How to Think Like a Computer
Scientist* (2nd ed.). Green Tea Press. Free at
<https://greenteapress.com/wp/think-python-2e/>. Chapter 17, "Classes and
methods", turns functions you could already write into methods.
