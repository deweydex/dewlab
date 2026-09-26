---
title: "Composition: objects inside other objects"
year: "2026-2027"
version: 2026.09.26.1
worlds:
  game: A game world, with characters, the things they carry, and rooms.
  ocean: An ocean expedition, with a submarine, its crew, and what they find.
  solar-system: A solar system, with planets, moons and the probes sent to them.
  your-own: A world of your own, with a class you design and grow page by page.
covers:
  a-system-holds-its-planets:
    covers: [FOOP-LO7]
  is-a-or-has-a:
    covers: [FOOP-LO6, FOOP-LO7]
  cases-that-are-not-clear-cut:
    covers: [FOOP-LO6, FOOP-LO7]
---

# Composition: objects inside other objects

A solar system is not one planet. It holds many, and it can answer
questions about all of them at once: how many moons are there in all?
Which planet is farthest out? Is a star system one more kind of planet,
or something else?

## A system holds its planets

A class's fields do not have to be numbers or text. A field can hold a
list of other objects. Here, a `StarSystem` holds `Planet` objects. What
will the last line print?

```python exec
id: a-system-holds-its-planets-1
class Planet:
    def __init__(self, name, distance, moons):
        self.name = name
        self.distance = distance    # millions of km from its star
        self._moons = list(moons)

    def moon_count(self):
        return len(self._moons)


class StarSystem:
    def __init__(self, star):
        self.star = star
        self._planets = []

    def add(self, planet):
        self._planets.append(planet)

    def total_moons(self):
        total = 0
        for planet in self._planets:
            total = total + planet.moon_count()
        return total


sol = StarSystem("the Sun")
sol.add(Planet("Earth", 149.6, ["the Moon"]))
sol.add(Planet("Mars", 228.0, ["Phobos", "Deimos"]))
sol.add(Planet("Jupiter", 778.5, ["Io", "Europa", "Ganymede", "Callisto"]))
print(sol.total_moons())
```

```predict
type: number

What will the last line print?
```

It prints `7`: one, two and four. (Jupiter has over 90 moons that we
know of. These are its four big ones.)

Look at what `StarSystem` does and does not do:

- It never stores a distance or a moon of its own.
- Its field `_planets` starts as an empty list, and `add()` puts one
  planet in at a time.
- `total_moons()` asks each planet for its own `moon_count()`. It never
  looks inside a planet's list of moons. That list belongs to the planet.

When a class is built from objects of other classes, held in its fields,
we call it *composition*. A star system has planets.

Can you give `StarSystem` a `farthest()` method, which returns the planet
farthest from the star?

```python exec
id: a-system-holds-its-planets-2
sol = StarSystem("the Sun")
sol.add(Planet("Earth", 149.6, ["the Moon"]))
sol.add(Planet("Jupiter", 778.5, ["Io", "Europa", "Ganymede", "Callisto"]))
sol.add(Planet("Mars", 228.0, ["Phobos", "Deimos"]))
print(sol.farthest().name)
```

```inputs
sol.farthest().name
sol.farthest().moon_count()
```

```hint
The method goes inside `StarSystem`, in the cell above, so run that cell
again once it is there. Which planet should it start with, as the
farthest so far? It is the same loop as `heaviest()` on
[Sequence, selection and iteration inside a class](tutorial:the-moves-you-already-know).
```

```solution
class StarSystem:
    def __init__(self, star):
        self.star = star
        self._planets = []

    def add(self, planet):
        self._planets.append(planet)

    def total_moons(self):
        total = 0
        for planet in self._planets:
            total = total + planet.moon_count()
        return total

    def farthest(self):
        best = self._planets[0]
        for planet in self._planets:
            if planet.distance > best.distance:
                best = planet
        return best

sol = StarSystem("the Sun")
sol.add(Planet("Earth", 149.6, ["the Moon"]))
sol.add(Planet("Jupiter", 778.5, ["Io", "Europa", "Ganymede", "Callisto"]))
sol.add(Planet("Mars", 228.0, ["Phobos", "Deimos"]))
print(sol.farthest().name)
---
`Jupiter`. The method returns the planet itself, not its name, so a caller
can ask it anything: `sol.farthest().moon_count()` is 4.
```

## Is a, or has a?

The last page built classes on other classes by inheritance. What if a
star system inherited from `Planet`? Python will not object. What will
this print?

```python exec
id: is-a-or-has-a-1
class StarSystem(Planet):    # a star system is not a planet
    def __init__(self, star):
        super().__init__(star, 0, [])
        self._planets = []

sol = StarSystem("the Sun")
print(sol.name, sol.distance, sol.moon_count())
```

It prints `the Sun 0 0`. The system now has a distance from itself, and
moons of its own, and a caller could ask it for either. Python raised no
error. The mistake is in the design, not in the code.

A test helps. Say the sentences out loud, and ask which one is true:

| Sentence | True? | Choose |
|---|---|---|
| "A troll is a character." | Yes | inheritance |
| "A star system is a planet." | No | |
| "A star system has planets." | Yes | composition |

An *is a* relationship means one class is a special kind of another, and
calls for inheritance. A *has a* relationship means one object holds
others, and calls for composition. When both seem to fit, many
programmers choose "has a". An object that holds another can swap it for
a different one later. An object that inherits keeps everything its
parent does, even the parts that make no sense for it.

```question
id: is-a-or-has-a-q1
type: fill-in-the-blank

- A submarine and its crew: a submarine {has|is} a crew. {Composition|Inheritance}.
- A lander and a probe: a lander {is|has} a probe. {Inheritance|Composition}.
- A room and a treasure: a room {has|is} treasure. {Composition|Inheritance}.
- A planet and its moons: a planet {has|is} moons. {Composition|Inheritance}.
```

## Cases that are not clear-cut

The sentence test decides most cases. Here are four where good
programmers disagree, and the reasons each way.

**A dictionary or a class?** A moon could be
`{"name": "Io", "width": 3643}`, or a `Moon` object. The dictionary is
less code, and fine while a moon only knows things. A class is useful
when a moon keeps a rule (a width is never negative) or answers a
question (is it bigger than ours?). Many designs start with a dictionary
and grow a class the day the first rule arrives.

**A child class or a flag?** A body in space might be a planet or a dwarf
planet. One design has two child classes, `Planet(Body)` and
`DwarfPlanet(Body)`. Another has one class, with a field that says which
kind it is:

```python exec
id: cases-that-are-not-clear-cut-1
class Body:
    def __init__(self, name, kind):
        self.name = name
        self.kind = kind    # "planet" or "dwarf planet"

    def describe(self):
        if self.kind == "planet":
            return f"{self.name}, a planet"
        else:
            return f"{self.name}, a dwarf planet"

pluto = Body("Pluto", "planet")
print(pluto.describe())
pluto.kind = "dwarf planet"    # astronomers decided this in 2006
print(pluto.describe())
```

In 2006, astronomers decided that Pluto is a dwarf planet. With a flag,
that is one line. With child classes, it is harder: an object cannot
change its class, so the program has to build a new `DwarfPlanet` and put
it everywhere the old Pluto was. But suppose astronomers name a third
kind next year. The child classes take one new class, and nothing else
changes. The flag takes a new `elif` in `describe`, and in every other
method that asks which kind it is.

```question
id: cases-that-are-not-clear-cut-q1
type: multiple-choice
answer: 3

Which design survives better?

- The flag, always
  - An object's kind can change with one line.
- Child classes, always
  - A new kind is a new class, and nothing old is edited.
- It depends on which change is more likely
  - A flag survives a thing changing kind; child classes survive new kinds being added.
```

**When "is a" breaks.** In mathematics, a square is a rectangle. So
`Square(Rectangle)` looks right. What will these two lines print?

```python exec
id: cases-that-are-not-clear-cut-2
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def set_width(self, width):
        self.width = width

    def area(self):
        return self.width * self.height


class Square(Rectangle):
    def __init__(self, side):
        super().__init__(side, side)

    def set_width(self, width):
        self.width = width
        self.height = width    # a square keeps its sides equal


def double_width(shape):
    shape.set_width(shape.width * 2)
    return shape.area()

print(double_width(Rectangle(3, 3)))
print(double_width(Square(3)))
```

It prints `18`, then `36`. `double_width` was written for rectangles,
where doubling the width doubles the area, and every rectangle keeps that
promise but the square. A square must change its height when its width
changes, so it breaks that promise. "Is a" has to hold for everything
the parent does, not only for what the thing is.

**Two things at once.** An astronaut can be a commander and a scientist,
both at once, and change roles between missions. `Commander(Astronaut)`
and `Scientist(Astronaut)` leave nowhere for someone who is both.
Composition has room for both. An astronaut *has* roles.

```python exec
id: cases-that-are-not-clear-cut-3
class Astronaut:
    def __init__(self, name, roles):
        self.name = name
        self._roles = list(roles)

    def can(self, role):
        return role in self._roles

peggy = Astronaut("Peggy Whitson", ["commander", "scientist"])
print(peggy.can("scientist"), peggy.can("pilot"))
```

It prints `True False`. Peggy Whitson, a biochemist, was the first woman
to command the International Space Station. A person is rarely one kind
of thing for life.

### Your turn: your class, fifth version

This is the fifth version of your class: a new class that holds objects
of the classes you already have. Run the first cell in your world, which
holds your classes as they stood at the end of
[Inheritance](tutorial:one-parent-many-children), then write the container
in the second.

<div class="dl-world" data-world="game">

```python exec
id: your-class-5-so-far--game
{{include: setup/oop/game-4.py}}

{{include: setup/oop/game-4-kind.py}}
```

A room holds characters. Can you write a `Room` class, with a name, an
`enter(character)` method that refuses anyone already inside, and a
`standing()` method that returns the names of everyone who is not down
(everyone whose health is above 0)?

```python exec
id: your-class-5--game
# Your Room here

cave = Room("Cave")
ada = Character("Ada", 10)
cave.enter(ada)
cave.enter(Healer("Mira", 10))
cave.enter(ada)
ada.take_damage(12)
print(cave.standing())
```

```inputs
cave.standing()
str(cave)
```

```hint
A room's characters are a list it keeps to itself. `in` tells you whether
something is already in a list. Which of `Character`'s methods answers
whether someone is down?
```

```solution
class Room:
    def __init__(self, name):
        self.name = name
        self._characters = []

    def __str__(self):
        return f"{self.name}: {len(self.standing())} standing"

    def enter(self, character):
        if character in self._characters:
            print(f"Refused: {character.name} is already in {self.name}.")
            return
        self._characters.append(character)

    def standing(self):
        names = []
        for character in self._characters:
            if not character.is_down():
                names.append(character.name)
        return names

cave = Room("Cave")
ada = Character("Ada", 10)
cave.enter(ada)
cave.enter(Healer("Mira", 10))
cave.enter(ada)
ada.take_damage(12)
print(cave.standing())
---
A refusal for Ada's second entry, then `['Mira']`. `standing()` asks each
character `is_down()`, and a healer answers as a character does. `Room`
keeps one rule of its own: nobody is inside twice.
```

</div>

<div class="dl-world" data-world="ocean">

```python exec
id: your-class-5-so-far--ocean
{{include: setup/oop/ocean-4.py}}

{{include: setup/oop/ocean-4-kind.py}}
```

An expedition has submarines. Can you write an `Expedition` class, with a
name, an `add(submarine)` method, and a `deepest()` method that returns
the submarine that is deepest right now?

```python exec
id: your-class-5--ocean
# Your Expedition here

deep_blue = Expedition("Deep Blue")
nautilus = Submarine("Nautilus")
trieste = Bathyscaphe("Trieste")
deep_blue.add(nautilus)
deep_blue.add(trieste)
nautilus.dive(300)
trieste.dive(5000)
print(deep_blue.deepest())
```

```inputs
str(deep_blue.deepest())
deep_blue.deepest().name
```

```hint
`deepest()` is the same loop as `farthest()` above. Which of
`Submarine`'s methods tells you how deep one is, without reaching in?
```

```solution
class Expedition:
    def __init__(self, name):
        self.name = name
        self._submarines = []

    def add(self, submarine):
        self._submarines.append(submarine)

    def deepest(self):
        best = self._submarines[0]
        for submarine in self._submarines:
            if submarine.get_depth() > best.get_depth():
                best = submarine
        return best

deep_blue = Expedition("Deep Blue")
nautilus = Submarine("Nautilus")
trieste = Bathyscaphe("Trieste")
deep_blue.add(nautilus)
deep_blue.add(trieste)
nautilus.dive(300)
trieste.dive(5000)
print(deep_blue.deepest())
---
`Trieste at 5000 m`. The expedition asks each submarine `get_depth()`,
and never reaches for `_depth`: the rules about depth stay with the
submarine. An empty expedition has no deepest submarine, and this
version stops with an `IndexError`. What should it do instead?
```

</div>

<div class="dl-world" data-world="solar-system">

```python exec
id: your-class-5-so-far--solar-system
{{include: setup/oop/solar-system-4.py}}

{{include: setup/oop/solar-system-4-kind.py}}
```

A mission has probes. Can you write a `Mission` class, with a name, a
`launch(probe)` method, a `total_fuel()` method, and a `ready_for(kg)`
method that returns the names of the probes that can burn that much now?

```python exec
id: your-class-5--solar-system
# Your Mission here

outer = Mission("Outer Planets")
voyager = Probe("Voyager", 70)
philae = Lander("Philae", 40)
outer.launch(voyager)
outer.launch(philae)
philae.land()
print(outer.total_fuel(), outer.ready_for(30))
```

```inputs
outer.total_fuel()
outer.ready_for(30)
outer.ready_for(100)
```

```hint
Both methods loop over the mission's probes. Which of `Probe`'s methods
answer "how much fuel?" and "can you burn this much?", for a lander too?
```

```solution
class Mission:
    def __init__(self, name):
        self.name = name
        self._probes = []

    def launch(self, probe):
        self._probes.append(probe)

    def total_fuel(self):
        total = 0
        for probe in self._probes:
            total = total + probe.get_fuel()
        return total

    def ready_for(self, kg):
        names = []
        for probe in self._probes:
            if probe.can_burn(kg):
                names.append(probe.name)
        return names

outer = Mission("Outer Planets")
voyager = Probe("Voyager", 70)
philae = Lander("Philae", 40)
outer.launch(voyager)
outer.launch(philae)
philae.land()
print(outer.total_fuel(), outer.ready_for(30))
---
`110 ['Voyager']`. Philae has 40 kg and still is not ready: it has landed,
and a lander's own `can_burn` says so. `Mission` never asks which kind of
probe it has. That is the last page's polymorphism, at work inside a
container.
```

</div>

<div class="dl-world" data-world="your-own">

What in your world holds several of your things? A shop holds stock, a
herd holds animals, a library holds books. Can you write that class, with
at least one method that asks each thing it holds a question? Your
classes from [Inheritance](tutorial:one-parent-many-children) are saved
there. Copy them into the first cell.

```python exec
id: your-class-5-so-far--your-own
# My classes so far
```

```python exec
id: your-class-5--your-own
# My container class
```

</div>

## Looking back

Of the four cases that are not clear-cut, which one would you have
decided differently before this page? And which would you still argue
about?

A challenge: Alpha Centauri has two stars close together, A and B, and a
third, Proxima, farther out. Can you change `StarSystem` so that it can
hold more than one star, without changing how planets are added or
counted?

```python challenge
class StarSystem:
    def __init__(self, star):
        self.star = star
        self._planets = []

    def add(self, planet):
        self._planets.append(planet)

alpha = StarSystem("Alpha Centauri A")
print(alpha.star)
```

Next, [Testing a class: hunting for the bug](tutorial:testing-what-a-class-does)
writes tests that find the mistakes a class hides.

## Where to read more

Everything here is covered elsewhere too, often in a form that will suit you
better than this one.

Downey, A. B. (2015). *Think Python: How to Think Like a Computer
Scientist* (2nd ed.). Green Tea Press. Free at
<https://greenteapress.com/wp/think-python-2e/>. Section 18.8, "Class
diagrams", names the two relationships on this page: IS-A and HAS-A.

Martin, R. C. (1996). "The Liskov Substitution Principle". *C++ Report*,
March 1996. This article uses the same square and rectangle to explain
the rule behind them: a child must keep every promise its parent makes.
It is written for C++, and the idea is the same in Python.

Real Python. *Inheritance and Composition: A Python OOP Guide*.
<https://realpython.com/inheritance-composition-python/>. This is a longer
look at the choice this page makes, with more examples of each.
