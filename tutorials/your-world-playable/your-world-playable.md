---
title: "Your world, playable: the whole series in one program"
year: "2026-2027"
version: 2026.09.26.1
worlds:
  game: A game world, with characters, the things they carry, and rooms.
  ocean: An ocean expedition, with a submarine, its crew, and what they find.
  solar-system: A solar system, with planets, moons and the probes sent to them.
  your-own: A world of your own, with a class you design and grow page by page.
covers:
  what-you-have:
    covers: [FOOP-LO6, FOOP-LO7]
  your-world-running:
    covers: [FOOP-LO6, FOOP-LO10, FOOP-LO11]
  making-it-yours:
    covers: [FOOP-LO7]
---

# Your world, playable: the whole series in one program

Every page of this series added one thing to one class in your world. On
this page they come together: a world that someone else can play, or
explore, without reading a line of your code, with its tests passing.
Then it is yours to grow.

## What you have

Look back at what each page added:

1. [Classes and objects](tutorial:objects-and-classes): a class, with
   `__init__` and `__str__`.
2. [Encapsulation](tutorial:keeping-details-inside-an-object): one rule,
   kept by a method, and a private field with a getter.
3. [A class with many methods](tutorial:one-class-many-methods): a method
   that answers a question, used by another, and a class attribute.
4. [Designing classes](tutorial:from-a-description-to-classes): cards for
   the classes your world needs, before any code.
5. [Inheritance](tutorial:one-parent-many-children): at most one child
   class, and one sentence that says why.
6. [Composition](tutorial:objects-inside-objects): a class that holds
   your objects.
7. [Testing a class](tutorial:testing-what-a-class-does): five tests,
   one at a boundary, and one missing rule added.
8. [Documenting a class](tutorial:documenting-a-class): docstrings, with
   an example doctest can check.
9. [A front end](tutorial:a-front-end-for-a-class): a `run_choice`,
   tested with a list, and a menu to play from.

## Your world, running

Here is one world with all of it: every class as it stood at the end of
the last page, its five tests, and the runner from
[Testing a class](tutorial:testing-what-a-class-does). Run the first
cell: every test should pass. The second cell starts a new game. Then
choose from the menu in the third, and run it once for each turn.

<div class="dl-world" data-world="game">

```python exec
id: your-world-running--game
{{include: setup/oop/game-8.py}}

{{include: setup/oop/game-tests.py}}

{{include: setup/oop/run-tests.py}}

run_tests()
```

```python exec
id: your-world-new-game--game
ada = Character("Ada", 10)
mira = Healer("Mira", 10)
grog = Character("Grog", 8)
print("A new game: Ada and Mira against Grog.")
```

```python exec
id: your-world-front-end--game
command = dropdown("What now?", ["look", "attack", "heal", "quit"])
still_playing = run_choice(ada, mira, grog, command.value)
```

</div>

<div class="dl-world" data-world="ocean">

```python exec
id: your-world-running--ocean
{{include: setup/oop/ocean-8.py}}

{{include: setup/oop/ocean-tests.py}}

{{include: setup/oop/run-tests.py}}

run_tests()
```

```python exec
id: your-world-new-game--ocean
trieste = Bathyscaphe("Trieste")
print("A new dive: the Trieste, at the surface.")
```

```python exec
id: your-world-front-end--ocean
command = dropdown("Command", ["dive", "rise", "depth", "quit"])
still_diving = run_choice(trieste, command.value)
```

</div>

<div class="dl-world" data-world="solar-system">

```python exec
id: your-world-running--solar-system
{{include: setup/oop/solar-system-8.py}}

{{include: setup/oop/solar-system-tests.py}}

{{include: setup/oop/run-tests.py}}

run_tests()
```

```python exec
id: your-world-new-game--solar-system
philae = Lander("Philae", 40)
print("A new mission: Philae, with 40 kg of fuel.")
```

```python exec
id: your-world-front-end--solar-system
command = dropdown("Command", ["burn", "refuel", "status", "quit"])
still_flying = run_choice(philae, command.value)
```

</div>

<div class="dl-world" data-world="your-own">

Copy your classes, your tests and your `run_choice` from the pages
before into the first cell, the objects a new game starts with into the
second, and your menu into the third. Do your tests all pass together, in
one place?

```python exec
id: your-world-running--your-own
# My classes, my tests, and run_tests()
```

```python exec
id: your-world-new-game--your-own
# The objects a new game starts with
```

```python exec
id: your-world-front-end--your-own
# My menu, and one turn of run_choice
```

</div>

Your own version of this world may be different from the one above, and
it should be: different names, a different child class, a different
rule. Every piece should be there, and the tests should pass.

## Making it yours

The interesting part starts when your world runs. Choose something
to add, and add it the way this series did: the rule first, in a method;
then a test at its boundary, which fails before the rule is written; then
a docstring; then a command, so a player can reach it. Here are some
starting points, and your own idea is better than any of them.

<div class="dl-world" data-world="game">

- Treasure: a `Treasure` class with a value in gold, a room that holds
  it, and a hero who can carry at most three things.
- A second room, and a command to move between them.
- A monster that fights back harder when its health is low: a child class
  of `Character`, through `super()`.

</div>

<div class="dl-world" data-world="ocean">

- Crew: a `CrewMember` with oxygen, a submarine that holds at most three,
  and a dive that is refused when the crew would not have enough oxygen.
- Specimens found on each dive, and a logbook that answers "how many are
  alive?"
- A second submarine, and a command to choose which one the player is
  steering.

</div>

<div class="dl-world" data-world="solar-system">

- Planets and moons: a probe that orbits one planet at a time, and
  photographs its moons.
- A mission that answers "which moons have we photographed?"
- An `Orbiter` child class that uses less fuel for every burn, through
  `super()`.

</div>

<div class="dl-world" data-world="your-own">

- The rule in your world you have not written yet.
- A second container: something that holds your containers.
- A command a player would try first, and that your front end does not
  have yet.

</div>

```python exec
id: making-it-yours-1
# My addition: the rule, its test, its docstring, its command
```

Then show it to somebody. Ask someone who has never seen your code to
play, or explore, for five minutes. Watch, and do not help. What did they
type that you never planned for? Where did they get stuck? A front end is
finished when a stranger can use it, and the only way to find out is to
watch one try.

## Looking back

These questions are for you, and for a conversation with your teacher or
a classmate if you want one. There are no right answers to them.

- Which of your classes changed most between the first page and this
  one? What made it change?
- Which rule was hardest to put in the right place?
- Which test caught something you did not expect?
- If you started your world again tomorrow, what would you design
  differently on the first page?

Your code is saved on this page, on this device. The
[Notebook](../compose/notebook.html) keeps work in files. Take your world
there when it grows too big for one page.

## Where to read more

Everything here is covered elsewhere too, often in a form that will suit you
better than this one.

Sweigart, A. (2016). *Invent Your Own Computer Games with Python* (4th
ed.). No Starch Press. Free at <https://inventwithpython.com/invent4thed/>. Each
chapter builds a whole game. Use it when your world is ready to become one.

Python Software Foundation. *The Python Tutorial*, section 9, "Classes".
<https://docs.python.org/3/tutorial/classes.html>. This section covers
everything this series taught, in the official words. It also has more
that a bigger world will need later.
