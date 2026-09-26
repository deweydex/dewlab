---
title: "Mixed problems: programming with objects"
practice_across:
  - objects-and-classes
  - the-moves-you-already-know
  - the-tools-around-your-code
  - keeping-details-inside-an-object
  - one-class-many-methods
  - a-polynomial-class
  - from-a-description-to-classes
  - one-parent-many-children
  - objects-inside-objects
  - testing-what-a-class-does
  - documenting-a-class
  - a-front-end-for-a-class
  - your-world-playable
year: "2026-2027"
version: 2026.09.26.1
worlds:
  game: A game world, with characters, the things they carry, and rooms.
  ocean: An ocean expedition, with a submarine, its crew, and what they find.
  solar-system: A solar system, with planets, moons and the probes sent to them.
  your-own: A world of your own, with a class you design and grow page by page.
---

# Mixed problems: programming with objects

Every problem here draws on more than one page of this series, and none
of them says which. You need to decide whether a problem wants a rule, a
child class, a container, a test, or all four. That is a skill of its
own, apart from writing any one of them.

Most answers have more than one good design. Where a problem has a real
decision in it, the answer says what was chosen and why.

## 1. A lifeboat with no name

```python exec
id: a-lifeboat-with-no-name-1
class Vessel:
    def __init__(self, name):
        self.name = name

    def describe(self):
        return f"{self.name}, {self.kind()}"

    def kind(self):
        return "a vessel"

class Lifeboat(Vessel):
    def __init__(self, name, seats):
        self.seats = seats

    def kind(self):
        return f"a lifeboat for {self.seats}"

boat = Lifeboat("Lifeboat 1", 12)
print(boat.describe())
```

Run it. The traceback ends inside `describe`, in the parent. Which line
would you change, and to what?

<details class="dl-answer"><summary>answer</summary>

Neither line the traceback names. `Lifeboat.__init__` never calls
`super().__init__(name)`, so no name was ever stored, and the error only
appears later, in a parent method that reads it. Add that call as the
first line of `Lifeboat.__init__`, and it prints `Lifeboat 1, a lifeboat
for 12`. Notice too that `describe` calls `self.kind()`, and for a
lifeboat that runs `Lifeboat.kind`.

</details>

## 2. The big tank

```python exec
id: the-big-tank-1
class Tank:
    capacity = 100

    def __init__(self):
        self.level = 0

    def fill(self):
        self.level = Tank.capacity

class BigTank(Tank):
    capacity = 500

tank = BigTank()
tank.fill()
print(tank.level)
```

```predict
type: number

What will it print?
```

<details class="dl-answer"><summary>why</summary>

`100`. `fill` reads `Tank.capacity` by name, so a big tank's own 500 is
never asked for. `self.capacity` would find it: Python looks on the
object, then its class, then the parent.

</details>

## 3. A squad that grows by itself

```python exec
id: a-squad-that-grows-1
class Squad:
    def __init__(self, names):
        self._names = names

    def size(self):
        return len(self._names)

names = ["Ada", "Grace"]
squad = Squad(names)
names.append("Alan")
print(squad.size())
```

```predict
type: number

What will it print?
```

<details class="dl-answer"><summary>why</summary>

`3`. `names` and `self._names` are one list with two names, so the
caller changed the squad without touching it. The underscore did not
help. Nobody used `_names` from outside. `self._names = list(names)` gives the squad a
copy of its own.

</details>

## 4. A container that asks

This is your world's container from
[Composition](tutorial:objects-inside-objects). Can you give it one more
method, which asks each object it holds a question and chooses between
the answers?

<div class="dl-world" data-world="game">

Can you give `Room` a `weakest()` method, which returns the character with
the least health?

```python exec
id: a-container-that-asks-1--game
{{include: setup/oop/game-6.py}}

cave = Room("Cave")
cave.enter(Character("Ada", 10))
cave.enter(Character("Grog", 4))
cave.enter(Healer("Mira", 7))
print(cave.weakest())
```

```inputs
str(cave.weakest())
```

```solution
class Room:
    def __init__(self, name):
        self.name = name
        self._characters = []

    def enter(self, character):
        if character in self._characters:
            print(f"Refused: {character.name} is already in {self.name}.")
            return
        self._characters.append(character)

    def weakest(self):
        best = self._characters[0]
        for character in self._characters:
            if character.get_health() < best.get_health():
                best = character
        return best

cave = Room("Cave")
cave.enter(Character("Ada", 10))
cave.enter(Character("Grog", 4))
cave.enter(Healer("Mira", 7))
print(cave.weakest())
---
`Grog (health 4)`. This answer shows only the parts of `Room` the
problem needs: in your world, `weakest` goes beside `standing`. It asks
each character `get_health()`, and never reaches for `_health`.
```

</div>

<div class="dl-world" data-world="ocean">

Can you give `Expedition` a `total_room_below()` method, which adds up how
many metres every submarine can still dive?

```python exec
id: a-container-that-asks-1--ocean
{{include: setup/oop/ocean-6.py}}

deep_blue = Expedition("Deep Blue")
nautilus = Submarine("Nautilus")
nautilus.dive(300)
deep_blue.add(nautilus)
deep_blue.add(Bathyscaphe("Trieste"))
print(deep_blue.total_room_below())
```

```inputs
deep_blue.total_room_below()
```

```solution
class Expedition:
    def __init__(self, name):
        self.name = name
        self._submarines = []

    def add(self, submarine):
        self._submarines.append(submarine)

    def total_room_below(self):
        total = 0
        for submarine in self._submarines:
            total = total + submarine.room_below()
        return total

deep_blue = Expedition("Deep Blue")
nautilus = Submarine("Nautilus")
nautilus.dive(300)
deep_blue.add(nautilus)
deep_blue.add(Bathyscaphe("Trieste"))
print(deep_blue.total_room_below())
---
11100: 100 m for the Nautilus, and 11,000 m for the Trieste, whose own
`room_below` reads its own hull limit. This answer shows only the parts
of `Expedition` the problem needs: in your world, the new method goes
beside `deepest`.
```

</div>

<div class="dl-world" data-world="solar-system">

Can you give `Mission` an `emptiest()` method, which returns the probe
with the least fuel?

```python exec
id: a-container-that-asks-1--solar-system
{{include: setup/oop/solar-system-6.py}}

outer = Mission("Outer Planets")
outer.launch(Probe("Voyager", 70))
outer.launch(Lander("Philae", 40))
outer.launch(Probe("Juno", 55))
print(outer.emptiest())
```

```inputs
str(outer.emptiest())
```

```solution
class Mission:
    def __init__(self, name):
        self.name = name
        self._probes = []

    def launch(self, probe):
        self._probes.append(probe)

    def emptiest(self):
        best = self._probes[0]
        for probe in self._probes:
            if probe.get_fuel() < best.get_fuel():
                best = probe
        return best

outer = Mission("Outer Planets")
outer.launch(Probe("Voyager", 70))
outer.launch(Lander("Philae", 40))
outer.launch(Probe("Juno", 55))
print(outer.emptiest())
---
`Philae (fuel 40 kg)`. This answer shows only the parts of `Mission` the
problem needs: in your world, `emptiest` goes beside `ready_for`.
```

</div>

<div class="dl-world" data-world="your-own">

What question would you like to ask everything your container holds?
Can you write it as a method, with a loop that asks and a choice between
the answers?

```python exec
id: a-container-that-asks-1--your-own
# My container, with one more method
```

</div>

## 5. The test that finds the slip

A `can_dive(metres)` method is meant to allow a dive to exactly the hull
limit of 400 m. Somebody wrote `<` where they meant `<=`. Which one test
would catch it, and which tests would pass either way?

<details class="dl-answer"><summary>answer</summary>

A dive from the surface to exactly 400 m: `<` refuses it, `<=` allows it.
Dives of 100 m or 500 m give the same answer both ways. The two
comparisons disagree only at the boundary, so a test belongs there.

</details>

## 6. An example that is almost right

```python exec
id: an-example-that-is-almost-right-1
import doctest

class Probe:
    def __init__(self, name, fuel):
        self.name = name
        self._fuel = fuel

    def half_tank(self):
        """Return half the probe's fuel.

        >>> Probe("Voyager", 70).half_tank()
        35
        """
        return self._fuel / 2

doctest.run_docstring_examples(Probe.half_tank, globals(), name="half_tank")
```

```question
id: an-example-that-is-almost-right-q1
type: multiple-choice
answer: 2

Does the example pass?

- Yes: 35 and 35.0 are the same number.
  - `35 == 35.0` is True in Python.
- No: Python shows `35.0`, and doctest compares what is shown.
  - `/` always gives a decimal, and doctest reads text.
```

<details class="dl-answer"><summary>why</summary>

It fails: `Expected: 35`, `Got: 35.0`. `/` always gives a decimal, even
when it divides exactly. Either the example says `35.0`, or the method
uses `//` and promises a whole number, which is a design decision the
docstring should then say clearly.

</details>

## 7. Two jobs in one function

```python
def play_turn(hero, monster):
    choice = input("What now? ")
    if choice == "attack":
        monster.take_damage(3)
    elif choice == "rest":
        hero.heal(2)
```

Why is `play_turn` hard to test? Can you split it so that it is not?

<details class="dl-answer"><summary>one answer</summary>

It asks and decides in one place, so every test would wait for somebody
to type. Split it: `run_choice(hero, monster, choice)` decides, and never
asks, and a loop asks and passes the answer on. Then a list of choices
tests `run_choice`, and a menu, a prompt or a test can all use it.

</details>

## 8. Class, child, container or flag?

A zoo keeps animals. Every animal has a name and eats. Penguins also
swim, and lions also roar. Keepers look after several animals each, and
an animal can be moved to another keeper. Which classes would you write,
and which relationships are "is a" and which "has a"?

<details class="dl-answer"><summary>one answer</summary>

`Animal`, with `Penguin(Animal)` and `Lion(Animal)`: a penguin is an
animal, and adds swimming. `Keeper` has animals, in a list. Moving an
animal is two method calls, one keeper's `remove` and another's `add`,
so the animal itself never changes class. If animals changed kind (they
do not), a flag would be the safer design. Another good answer has no
child classes at all, only a `sound` field, if roaring and swimming never
become more than a line of text.

</details>

## 9. One more rule, the whole way through

Choose one rule your world does not keep yet. Can you add it the way the
series did: the test first, at the boundary, failing; then the rule, in
one method; then the docstring; then a command in `run_choice`, so a
player can meet it?

```python exec
id: one-more-rule-1
# The test, the rule, the docstring, the command
```

<details class="dl-answer"><summary>one way to check</summary>

Run the test before the rule exists, and see it fail. Run it again after,
and see it pass. Run your other tests too. A new rule sometimes breaks an
old promise, and this is the best time to find out.

</details>
