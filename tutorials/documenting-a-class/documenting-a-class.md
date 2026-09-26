---
title: "Documenting a class with docstrings"
year: "2026-2027"
version: 2026.09.26.1
worlds:
  game: A game world, with characters, the things they carry, and rooms.
  ocean: An ocean expedition, with a submarine, its crew, and what they find.
  solar-system: A solar system, with planets, moons and the probes sent to them.
  your-own: A world of your own, with a class you design and grow page by page.
covers:
  a-class-docstring:
    covers: [FOOP-LO9]
  what-a-method-promises:
    covers: [FOOP-LO9]
  examples-python-can-check:
    covers: [FOOP-LO9]
    touches: [FOOP-LO10]
---

# Documenting a class with docstrings

Somebody on your team wants to use your class. They have not read its
code, and they should not have to. What do they need to know? What would
you want to know about somebody else's class before you used it?

A *docstring* is a description in triple quotes, on the first line inside
a class or a function. Python keeps it with the class, and `help()` shows
it. You may have met docstrings on functions, in
[Designing and testing good functions](tutorial:building-reusable-tools).
A class needs them in two places: on the class, and on each method.

## A class docstring

Here is the probe from the solar-system world, with a docstring on the
class. `help()` shows the docstrings of whatever it is given. What will
it show first?

```python exec
id: a-class-docstring-1
class Probe:
    """One space probe: a name, and fuel in kilograms, from 0 up to
    tank_size."""

    tank_size = 100

    def __init__(self, name, fuel):
        self.name = name
        self._fuel = fuel

    def get_fuel(self):
        return self._fuel

help(Probe)
```

It shows the class docstring first, before any method. A class docstring
answers one question: what does one object of this class stand for? It
says what the object knows, and any rule that holds for every one of them
(here, the fuel is never below 0 or above `tank_size`). What the methods
do belongs in their own docstrings.

## What a method promises

A method's docstring is a promise to whoever calls it. A good one says
four things:

- what the method does, in one line;
- what each parameter should be;
- what it returns, if anything;
- what happens when the method refuses.

Here are two docstrings for the same `burn`:

```python
    def burn(self, kg):
        """Burns fuel."""
```

```python
    def burn(self, kg):
        """Burn kg kilograms of fuel.

        kg: a number of kilograms, 0 or more.
        Refuses, prints why, and changes nothing if can_burn(kg) is False.
        Returns nothing.
        """
```

```question
id: what-a-method-promises-q1
type: multiple-choice
answer: 2

A caller wants to know what `voyager.burn(200)` does to a probe with 70
kg. Which docstring tells them?

- The first: "Burns fuel."
  - It says what the method is for.
- The second
  - It says what happens when the probe cannot burn that much.
- Neither
  - Only the code can say what happens.
```

The first docstring is true, but it does not help a caller. It says what
the name `burn` already said. The second answers the questions a caller
has before they call it. The refusal matters most, because at a refusal,
a caller's program and the method disagree.

## Examples Python can check

A docstring can also hold examples: a line that starts `>>>`, as if typed
into Python, and the answer under it. A reader sees at once how the method
is used. And Python's *doctest* module can run each example, and check
that the answer is still the one written down. What will this print?

```python exec
id: examples-python-can-check-1
import doctest

class Probe:
    """One space probe: a name, and fuel in kilograms."""

    def __init__(self, name, fuel):
        self.name = name
        self._fuel = fuel

    def can_burn(self, kg):
        """Return True if the probe can burn kg kilograms now.

        >>> Probe("Voyager", 70).can_burn(30)
        True
        >>> Probe("Voyager", 70).can_burn(80)
        False
        """
        if kg < 0:
            return False
        return kg <= self._fuel

doctest.run_docstring_examples(Probe.can_burn, globals(), verbose=True, name="can_burn")
```

It prints each example, what it expected, and `ok` for each. `globals()`
gives doctest the page's names, so the examples can find `Probe`.

Now suppose a teammate changes one character, `<=` to `<`, so that a
probe can no longer burn its very last kilogram. Nobody touches the
docstring, which is exactly what happens in real projects. Add this
example to the docstring, change `<=` to `<` in the code, and run the cell
again:

```python
        >>> Probe("Voyager", 70).can_burn(70)
        True
```

doctest prints `Failed example`, with what it expected and what it got. A
docstring with examples cannot quietly stop telling the truth. The next
time its examples run, they say so. That is why the example at the
boundary, 70 out of 70, is the one worth writing.

### Your turn: your class, seventh version

This is the seventh version of your class: a docstring on every class,
and on every method a caller would use, with the four things a method
promises. Give at least one method an example that doctest can check,
at a boundary if you can.

<div class="dl-world" data-world="game">

```python exec
id: your-class-7--game
{{include: setup/oop/game-6.py}}

import doctest
doctest.run_docstring_examples(Room.standing, globals(), verbose=True, name="standing")
```

```solution
{{include: setup/oop/game-7.py}}

import doctest
doctest.run_docstring_examples(Room.standing, globals(), verbose=True, name="standing")
---
One set of docstrings. Each method says what it does, what its parameter
should be, and what it refuses. `is_down` and `standing` carry examples.
The example in `standing` takes three lines, because it has to build a
room first: an example can be as many lines as it needs.
```

</div>

<div class="dl-world" data-world="ocean">

```python exec
id: your-class-7--ocean
{{include: setup/oop/ocean-6.py}}

import doctest
doctest.run_docstring_examples(Submarine.room_below, globals(), verbose=True, name="room_below")
```

```solution
{{include: setup/oop/ocean-7.py}}

import doctest
doctest.run_docstring_examples(Submarine.room_below, globals(), verbose=True, name="room_below")
---
One set of docstrings. The bathyscaphe's example sits in its class
docstring, since it has no methods of its own: `room_below()` gives
11000, which is the whole reason the class exists. `deepest` says what a
caller must do first: give the expedition a submarine.
```

</div>

<div class="dl-world" data-world="solar-system">

```python exec
id: your-class-7--solar-system
{{include: setup/oop/solar-system-6.py}}

import doctest
doctest.run_docstring_examples(Probe.can_burn, globals(), verbose=True, name="can_burn")
```

```solution
{{include: setup/oop/solar-system-7.py}}

import doctest
doctest.run_docstring_examples(Probe.can_burn, globals(), verbose=True, name="can_burn")
---
One set of docstrings. `Lander.can_burn` says only what is different
about a lander, and leaves the rest to the promise `Probe.can_burn`
already makes. `burn` says where its refusal comes from, `can_burn`,
rather than saying it all again.
```

</div>

<div class="dl-world" data-world="your-own">

Copy your classes from [Testing a class](tutorial:testing-what-a-class-does)
into the cell. Give every class a docstring, and every method a caller
would use. Which method's refusal was hardest to put into words?

```python exec
id: your-class-7--your-own
# My classes, with docstrings
```

</div>

## Looking back

Your tests from the last page and your doctest examples both check what
the class does. What is each one better at?

A challenge: `Mission.total_fuel` has no example. Can you write one that
doctest can run, which builds a mission, launches two probes, and checks
the total? Then change `total_fuel` so it leaves out the last probe, and
see whether your example notices.

```python challenge
import doctest

class Probe:
    def __init__(self, name, fuel):
        self.name = name
        self._fuel = fuel

    def get_fuel(self):
        return self._fuel


class Mission:
    def __init__(self, name):
        self.name = name
        self._probes = []

    def launch(self, probe):
        self._probes.append(probe)

    def total_fuel(self):
        """Return the fuel of every probe in the mission, added up."""
        total = 0
        for probe in self._probes:
            total = total + probe.get_fuel()
        return total

doctest.run_docstring_examples(Mission.total_fuel, globals(), verbose=True, name="total_fuel")
```

Next, [A front end for a class](tutorial:a-front-end-for-a-class) lets
someone use your classes without writing any Python at all.

## Where to read more

Everything here is covered elsewhere too, often in a form that will suit you
better than this one.

Python Software Foundation. *PEP 257: Docstring Conventions*.
<https://peps.python.org/pep-0257/>. This is the agreement most Python
programmers follow about what goes in a docstring, and where.

Python Software Foundation. *doctest: Test interactive Python examples*.
<https://docs.python.org/3/library/doctest.html>. This is the module this
page used. It also shows how to run every example in a whole file at
once.
