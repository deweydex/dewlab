---
title: "Designing classes: from a description to classes"
year: "2026-2027"
version: 2026.09.26.1
worlds:
  game: A game world, with characters, the things they carry, and rooms.
  ocean: An ocean expedition, with a submarine, its crew, and what they find.
  solar-system: A solar system, with planets, moons and the probes sent to them.
  your-own: A world of your own, with a class you design and grow page by page.
covers:
  reading-a-description:
    covers: [FOOP-LO7]
  a-card-for-each-class:
    covers: [FOOP-LO7]
  more-than-one-good-answer:
    covers: [FOOP-LO7]
    touches: [FOOP-LO6]
  from-cards-to-skeletons:
    covers: [FOOP-LO7]
---

# Designing classes: from a description to classes

So far, every page has handed you a class and asked you to change it. A
real program starts before that, with a description of what it should do,
in words, and no code at all. Here is one. Read it through once. Which of
the things in it would you make into a class?

> The Deep Blue expedition has two submarines, the Nautilus and the
> Alvin. Each one dives and rises, and none may go deeper than its hull
> allows. Each carries a crew of up to three, and every crew member has a
> role: pilot, scientist or engineer. On each dive, the crew collect
> specimens, and for each one they note its name, the depth it was found
> at, and whether it is alive. The expedition keeps a logbook of every
> dive: which submarine, how deep, and what it found. At the end of each
> day, the leader wants to know the deepest dive, and how many living
> specimens came up.

Write your list down, on paper or in **Your notes**, before you read on.
There is no single answer, and this page shows three.

## Reading a description

A good first step is to find the nouns, the names of things: expedition,
submarine, hull, crew, crew member, role, dive, specimen, name, depth,
logbook, day, leader. Every class is a noun, but most nouns are not
classes. Three questions sort them.

- **Does it know several things, or do something?** A specimen knows its
  name, its depth, and whether it is alive: three facts that belong
  together. It might be a class. A depth is one number. It is a field of
  something else.
- **Does it keep a rule?** "None may go deeper than its hull allows" is a
  rule, and it belongs to the submarine, as it did on
  [Encapsulation](tutorial:keeping-details-inside-an-object). "A crew of
  up to three" is another, and it belongs to the submarine too.
- **Is it inside the program at all?** The leader is the person who uses
  the program. They are its front end, not one of its objects. A day is
  when the questions are asked, not a thing the program keeps.

The verbs are the other half: dives, rises, carries, collect, keeps,
wants to know. A verb usually becomes a method, on the class that does it,
or on the class that knows what the answer needs.

```question
id: reading-a-description-q1
type: fill-in-the-blank

- "The hull" is best as a {field of Submarine|class of its own}.
- "A specimen" is best as a {class of its own|field of Dive}, if it keeps three facts together.
- "The leader" is {the person using the program|a class of its own}.
- "Wants to know the deepest dive" is a {method|field} on whichever class keeps the dives.
```

## A card for each class

Before any code, designers often write each class on a small card, with
three parts:

- the class's name;
- its *responsibilities*: what it knows, and what it does;
- its *collaborators*: the other classes it works with.

A card like that is called a *CRC card*, for class, responsibilities and
collaborators. Cards are cheap: you can move them about, tear one up, or
put two together, which is much harder to do once the code exists. Here
is one set of cards for the expedition.

| Class | Knows | Does | Works with |
|---|---|---|---|
| `Submarine` | its name, its depth, its hull limit, its crew | dives, rises, takes a crew member on board (up to three) | `CrewMember` |
| `CrewMember` | a name, a role | nothing yet | |
| `Specimen` | a name, the depth found, alive or not | nothing yet | |
| `Dive` | which submarine, how deep, the specimens found | collects a specimen, counts the living ones | `Specimen` |
| `Logbook` | every dive | records a dive, finds the deepest, counts the living specimens | `Dive` |

Two cards say "nothing yet". A class that only knows things, and does
nothing, is worth asking about: would a dictionary do the same job? On
this set of cards, a crew member might as well be
`{"name": "Ada", "role": "pilot"}`. A class earns its place when it has a
rule to keep or a question to answer, and a crew member has neither, so
far.

## More than one good answer

Here are two other designs for the same paragraph.

**Design B: fewer classes.** `Submarine`, `Dive` and `Logbook` only. Crew
members are dictionaries, and specimens are dictionaries too. Less code,
and nothing lost today. But when the leader asks a new question about
specimens, such as "which were found below 1,000 m?", the answer goes in
`Dive` or `Logbook`, since a dictionary has no methods.

**Design C: an expedition that holds everything.** An `Expedition` class
holds the submarines and the dives, and answers the leader's questions
itself. There is no `Logbook`. One object to ask, and one place to look.
But `Expedition` now does two jobs: it looks after the submarines, and it
keeps the records. As the program grows, a class with two jobs tends to
grow into a class with five.

Each is a fair answer. They trade the same things in different amounts:

- more classes give every rule and every question its own home, but mean
  more code, and more places to look;
- fewer classes mean less code, but a rule with no home ends up copied
  wherever it is needed.

```question
id: more-than-one-good-answer-q1
type: multiple-choice
answer: 2

The leader adds a new rule: "a dead specimen is never brought up". Which
design gives that rule the most natural home?

- Design B, with specimens as dictionaries
  - Dictionaries are simpler, so the rule is simpler to add.
- The first design, with a `Specimen` class and `Dive.collect()`
  - `collect()` is one method that every specimen passes through.
- Design C, with everything in `Expedition`
  - One class sees everything, so it can check anything.
```

## From cards to skeletons

The last step before real code is a *skeleton*: each class with its
`__init__`, and every method named, but with nothing inside yet. A method
needs at least one line, so a skeleton uses `pass`, a line that does
nothing and stands in for the body you will write later. A skeleton runs.
It shows that the cards fit together: that every call has a method to go
to, and every method has what it needs.

What will the last line print?

```python exec
id: from-cards-to-skeletons-1
class Specimen:
    def __init__(self, name, depth, alive):
        self.name = name
        self.depth = depth
        self.alive = alive


class Dive:
    def __init__(self, submarine, depth):
        self.submarine = submarine
        self.depth = depth
        self._specimens = []

    def collect(self, specimen):
        pass

    def living(self):
        pass


class Logbook:
    def __init__(self):
        self._dives = []

    def record(self, dive):
        pass

    def deepest(self):
        pass

log = Logbook()
dive = Dive("Nautilus", 340)
dive.collect(Specimen("anglerfish", 340, True))
log.record(dive)
print(log.deepest())
```

```predict
What will the last line print?

- None
  - `deepest` has no `return` yet, so it gives back `None`.
- 340
  - The only dive was 340 m deep.
- An error
  - The methods have nothing in them.
```

It prints `None`: every call found its method, and each method did
nothing, as a skeleton should. Filling in `deepest` is the challenge at the
end of this page.

### Your turn

<div class="dl-world" data-world="game">

Read the description of this game. Which classes would you choose? Write
your cards first, then the skeleton.

> In the Cave of Echoes, a party of heroes explores rooms. Each hero has a
> name and health, and can carry up to three things. Rooms hold heroes and
> treasure, and a treasure has a name and a value in gold. Monsters wait
> in some rooms: a monster has a name, health and strength, and attacks
> the first hero it meets. The game ends when every hero is down, or when
> the party has found 100 gold.

```python exec
id: from-cards-to-skeletons-2--game
# My skeleton for the Cave of Echoes
```

```solution
class Hero:
    def __init__(self, name, health):
        self.name = name
        self._health = health
        self._bag = []

    def pick_up(self, treasure):
        pass    # refuses a fourth thing

    def take_damage(self, amount):
        pass


class Monster:
    def __init__(self, name, health, strength):
        self.name = name
        self._health = health
        self.strength = strength

    def attack(self, hero):
        pass

    def take_damage(self, amount):
        pass


class Treasure:
    def __init__(self, name, gold):
        self.name = name
        self.gold = gold


class Room:
    def __init__(self, name):
        self.name = name
        self._heroes = []
        self._treasure = []

    def enter(self, hero):
        pass
---
One good answer, with four classes. `Hero` keeps the carrying rule,
`Room` holds heroes and treasure, and `Treasure` is small but earns its
place if the party ever adds up its gold. "The game ends when…" needs a
home too: a `Game` class, or a method on `Room`? Look at `Hero` and
`Monster`: both have a name, health and `take_damage`. Writing that twice
is the problem [Inheritance](tutorial:one-parent-many-children) solves.
```

</div>

<div class="dl-world" data-world="ocean">

This page's expedition was yours. Here is one more paragraph from it, for
the part the description left out. Can you write cards for it, then add
to the skeleton above?

> Each submarine has a crew of up to three. A crew member has a name and
> a role, and uses oxygen as the submarine dives: 1 litre for every 10 m.
> A submarine may not dive if its crew would run out of oxygen.

```python exec
id: from-cards-to-skeletons-2--ocean
# My skeleton for the submarine and its crew
```

```solution
class CrewMember:
    def __init__(self, name, role, oxygen):
        self.name = name
        self.role = role
        self._oxygen = oxygen

    def breathe(self, litres):
        pass

    def has_oxygen_for(self, litres):
        pass


class Submarine:
    def __init__(self, name):
        self.name = name
        self._depth = 0
        self._crew = []

    def board(self, member):
        pass    # refuses a fourth crew member

    def dive(self, metres):
        pass    # asks every crew member has_oxygen_for(metres // 10)
---
One good answer. The oxygen rule changes the card for `CrewMember`: now
it knows its oxygen, and does something, so it has earned its class.
`Submarine.dive` asks each crew member the question, and each crew member
answers for itself. The rule about oxygen lives with the oxygen.
```

</div>

<div class="dl-world" data-world="solar-system">

Read the description of this mission. Which classes would you choose?
Write your cards first, then the skeleton.

> The Outer Planets mission sends probes to Jupiter and Saturn. Each
> probe carries fuel, and can burn it to change course, but never more
> than it has. Each planet has a name, a distance from the Sun, and moons.
> A probe orbits one planet at a time, and photographs the moons of the
> planet it orbits. Mission control wants to know how much fuel is left
> across the mission, and which moons have been photographed.

```python exec
id: from-cards-to-skeletons-2--solar-system
# My skeleton for the Outer Planets mission
```

```solution
class Planet:
    def __init__(self, name, distance, moons):
        self.name = name
        self.distance = distance
        self.moons = moons


class Probe:
    def __init__(self, name, fuel):
        self.name = name
        self._fuel = fuel
        self._orbiting = None
        self._photographed = []

    def burn(self, kg):
        pass    # never more than it has

    def orbit(self, planet):
        pass

    def photograph_moons(self):
        pass    # the moons of the planet it orbits


class Mission:
    def __init__(self, name):
        self.name = name
        self._probes = []

    def launch(self, probe):
        pass

    def fuel_left(self):
        pass

    def photographed(self):
        pass
---
One good answer, with three classes. A moon is a name here, in a list on
its planet. If the mission started to ask about moons (their size, who
found them), a `Moon` class would earn its place. `_orbiting` starts as
`None`, Python's value for "nothing yet": a probe on its way orbits no
planet.
```

</div>

<div class="dl-world" data-world="your-own">

Write a paragraph about your world, of four or five sentences: the things
in it, what each one knows, what each one does, and one or two rules.
Then do what this page did: find the nouns and the verbs, write a card for
each class, and write the skeleton. Your class from the pages before
should be one of the cards. Does it still look the same, next to the
others?

```python exec
id: from-cards-to-skeletons-2--your-own
# My world's skeleton
```

</div>

## Looking back

Which noun in your world's description was hardest to decide about: class,
field, or neither? And what would make you change your mind about it
later?

A challenge: fill in the expedition's skeleton, so that the leader's two
questions have answers. What is the deepest dive, and how many living
specimens came up?

```python challenge
class Specimen:
    def __init__(self, name, depth, alive):
        self.name = name
        self.depth = depth
        self.alive = alive


class Dive:
    def __init__(self, submarine, depth):
        self.submarine = submarine
        self.depth = depth
        self._specimens = []

    def collect(self, specimen):
        pass

    def living(self):
        pass


class Logbook:
    def __init__(self):
        self._dives = []

    def record(self, dive):
        pass

    def deepest(self):
        pass

    def living_specimens(self):
        pass


log = Logbook()
first = Dive("Nautilus", 340)
first.collect(Specimen("anglerfish", 340, True))
first.collect(Specimen("sea cucumber", 310, False))
second = Dive("Alvin", 1200)
second.collect(Specimen("tube worm", 1200, True))
log.record(first)
log.record(second)
print(log.deepest())
print(log.living_specimens())
```

Next, [Inheritance: one class built on another](tutorial:one-parent-many-children)
takes two classes that share most of what they know, like a hero and a
monster, and builds both from one.

## Where to read more

Everything here is covered elsewhere too, often in a form that will suit you
better than this one.

Beck, K. and Cunningham, W. (1989). "A Laboratory for Teaching
Object-Oriented Thinking". *OOPSLA '89 Conference Proceedings*, 1–6.
<https://c2.com/doc/oopsla89/paper.html>. The short paper where CRC cards
began, written to teach exactly what this page tries to: how to think in
objects before writing them.

Downey, A. B. (2015). *Think Python: How to Think Like a Computer
Scientist* (2nd ed.). Green Tea Press. Free at
<https://greenteapress.com/wp/think-python-2e/>. Section 18.10, "Data
encapsulation", designs classes by finding what belongs together, starting
from a program that has none.
