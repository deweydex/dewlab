---
title: "Composition: objects inside other objects — Practice"
practice_for: objects-inside-objects
year: "2026-2027"
version: 2026.09.26.1
---

# Composition: objects inside other objects — Practice

Problems on classes that hold other objects, and on choosing between "is
a" and "has a", and three from earlier pages. Several have more than one
good answer, and the answers say which way they went, and why.

## 1. One crew member, two submarines

```python exec
id: one-crew-member-two-submarines-1
class CrewMember:
    def __init__(self, name):
        self.name = name
        self.oxygen = 100

class Submarine:
    def __init__(self, name):
        self.name = name
        self._crew = []

    def board(self, member):
        self._crew.append(member)

    def oxygen_left(self):
        total = 0
        for member in self._crew:
            total = total + member.oxygen
        return total

ada = CrewMember("Ada")
nautilus = Submarine("Nautilus")
alvin = Submarine("Alvin")
nautilus.board(ada)
alvin.board(ada)
ada.oxygen = 40
print(nautilus.oxygen_left(), alvin.oxygen_left())
```

```predict
What will it print?

- 40 40
  - Both submarines hold the same crew member.
- 100 40
  - The Nautilus took Ada on board before her oxygen changed.
- 40 100
  - Only the last submarine sees the change.
```

<details class="dl-answer"><summary>why</summary>

`40 40`. Neither submarine holds a copy of Ada: both lists hold the one
`CrewMember` object, so a change to her is seen by both. That is what the
real world would say too: one person cannot be in two submarines, so a
`board` method might refuse someone already on board somewhere.

</details>

## 2. Gold in the vault

Can you give `Room` a `gold()` method that adds up the gold of every
treasure hidden in it?

```python exec
id: gold-in-the-vault-1
class Treasure:
    def __init__(self, name, gold):
        self.name = name
        self.gold = gold

class Room:
    def __init__(self, name):
        self.name = name
        self._treasure = []

    def hide(self, treasure):
        self._treasure.append(treasure)

vault = Room("Vault")
vault.hide(Treasure("crown", 50))
vault.hide(Treasure("ring", 12))
print(vault.gold())
```

```inputs
vault.gold()
Room("Hall").gold()
```

```solution
class Treasure:
    def __init__(self, name, gold):
        self.name = name
        self.gold = gold

class Room:
    def __init__(self, name):
        self.name = name
        self._treasure = []

    def hide(self, treasure):
        self._treasure.append(treasure)

    def gold(self):
        total = 0
        for treasure in self._treasure:
            total = total + treasure.gold
        return total

vault = Room("Vault")
vault.hide(Treasure("crown", 50))
vault.hide(Treasure("ring", 12))
print(vault.gold())
---
62, and an empty room has 0. The room asks each treasure for its gold,
and knows nothing else about treasure.
```

## 3. Is, or has?

```question
id: is-or-has-1
type: fill-in-the-blank

- A fleet {has|is} submarines.
- A rocket {has|is} engines.
- A dwarf planet {is|has} a body in space.
- A library {has|is} books.
- A scientist {is|has} an astronaut, on one mission at least.
```

<details class="dl-answer"><summary>why</summary>

Has, has, is, has, and the last is the hard one: a scientist is an
astronaut only while they fly. The page's answer was that an astronaut
*has* roles, so the sentence to trust is "an astronaut has the role of
scientist".

</details>

## 4. A fleet that is a submarine

Someone writes `class Fleet(Submarine):`, so that a fleet can "dive
together". What goes wrong?

<details class="dl-answer"><summary>one answer</summary>

A fleet would get a depth of its own, a hull limit of its own, and a
`dive` that changes only that one depth, not the submarines in it. "A
fleet is a submarine" is false, and every inherited method shows it. A
fleet *has* submarines, and its own `dive(metres)` can ask each one to
dive.

</details>

## 5. A specimen: dictionary or class?

An expedition records specimens: a name, a depth, and whether it is
alive. Would you use a dictionary for each, or a class? What would change
your mind?

<details class="dl-answer"><summary>one answer</summary>

A dictionary is enough while specimens only hold facts. A class earns its
place when a rule arrives (a depth is never negative) or a question does
(was it found below 1,000 m?). Both answers are fair today. The answer that
is hard to defend is a dictionary with the same rule copied into every
place that makes one.

</details>

## 6. Hero or monster: child class or flag?

A game has heroes and monsters. One design has `Hero(Character)` and
`Monster(Character)`. Another has one `Character` class with a field
`side`, either `"hero"` or `"monster"`. A spell can turn a monster into a
hero. Which design copes better?

<details class="dl-answer"><summary>one answer</summary>

The flag: the spell changes one field. With child classes, the program
would have to build a new `Hero` and put it everywhere the monster was.
If heroes and monsters behave very differently (heroes carry things,
monsters guard rooms), child classes keep each set of methods in one
place, and the spell is the price. It depends on which change the game
needs more.

</details>

## 7. A bird that cannot fly

```python
class Bird:
    def fly(self):
        return "up and away"

class Penguin(Bird):
    def fly(self):
        return "no"
```

```question
id: a-bird-that-cannot-fly-1
type: multiple-choice
answer: 2

A penguin is a bird. What is wrong with this design?

- Nothing: overriding `fly` is what overriding is for.
  - A child may change any method it inherits.
- `Bird` promises that every bird can fly, and a penguin breaks the promise.
  - Code written for birds expects `fly()` to fly.
- `Penguin` should not have a parent at all.
  - A penguin is not a kind of anything.
```

<details class="dl-answer"><summary>why</summary>

A program that sends every `Bird` flying gets a "no" it was never written
for, the way `double_width` got a square's area. It is the square and
the rectangle again. One fix is a parent that promises less: `Bird` with
no `fly`, and `FlyingBird(Bird)` for the birds that do.

</details>

## 8. From earlier: a child with no parent's fields

From *Inheritance*.

```python exec
id: from-earlier-a-child-with-no-parents-fields-1
class Planet:
    def __init__(self, name):
        self.name = name

class GasGiant(Planet):
    def __init__(self, name, rings):
        self.rings = rings

saturn = GasGiant("Saturn", True)
print(saturn.rings)
print(saturn.name)
```

```question
id: from-earlier-a-child-with-no-parents-fields-q1
type: multiple-choice
answer: 2

What happens?

- It prints `True`, then `Saturn`.
  - `GasGiant` inherits the name from `Planet`.
- It prints `True`, then stops with an `AttributeError`.
  - `GasGiant.__init__` replaces `Planet.__init__`, which never runs.
```

<details class="dl-answer"><summary>why</summary>

`True`, then an `AttributeError`: Saturn has no `name`, because the
child's `__init__` never called `super().__init__(name)`.

</details>

## 9. From earlier: whose rule?

From *Designing classes*. "A room may hold at most six characters." Would
that rule live in `Room` or in `Character`?

<details class="dl-answer"><summary>one answer</summary>

`Room`: the room knows how many are inside, and `enter` is the one
method every character passes through to get in. A character would have
to ask the room anyway.

</details>

## 10. From earlier: asking, not reaching

From *Encapsulation*. `Expedition.deepest()` on the tutorial page calls
`submarine.get_depth()`, where it could have read `submarine._depth`.
Both give the same number today. Why ask?

<details class="dl-answer"><summary>answer</summary>

`_depth` is private: the submarine may change how it stores its depth
(in centimetres, say), and every caller that reached in would break.
`get_depth()` is the promise the submarine keeps, however it stores the
number.

</details>
