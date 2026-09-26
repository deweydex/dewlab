---
title: "Inheritance: one class built on another — Practice"
practice_for: one-parent-many-children
year: "2026-2027"
version: 2026.09.26.1
---

# Inheritance: one class built on another — Practice

This page has problems on child classes, overriding and `super()`, and
three from earlier pages. Try each problem before you open anything under it, and
run the cells to test your guesses.

## 1. Which describe?

```python exec
id: which-describe-1
class Ship:
    def describe(self):
        return "a ship"

class Tug(Ship):
    def describe(self):
        return "a tug, which is " + super().describe()

for vessel in [Ship(), Tug()]:
    print(vessel.describe())
```

```predict
What will the last line print?

- a tug, which is a ship
  - `Tug.describe` adds to the parent's answer through `super()`.
- a tug, which is a tug, which is a ship
  - `super()` calls `Tug.describe` again.
- a ship
  - A `Tug` is a `Ship`, so it uses `Ship.describe`.
```

<details class="dl-answer"><summary>why</summary>

`a ship`, then `a tug, which is a ship`. The tug's own `describe` runs,
and `super().describe()` inside it runs the parent's, once.

</details>

## 2. A captain with no name

```python exec
id: a-captain-with-no-name-1
class CrewMember:
    def __init__(self, name):
        self.name = name

class Captain(CrewMember):
    def __init__(self, name, ship):
        self.ship = ship

nemo = Captain("Nemo", "Nautilus")
print(nemo.name, "commands", nemo.ship)
```

Run it. The error says a captain has no `name`, and yet `Captain` is
given one. Can you fix it with one line?

```inputs
nemo.name
nemo.ship
```

```solution
class CrewMember:
    def __init__(self, name):
        self.name = name

class Captain(CrewMember):
    def __init__(self, name, ship):
        super().__init__(name)
        self.ship = ship

nemo = Captain("Nemo", "Nautilus")
print(nemo.name, "commands", nemo.ship)
---
`Nemo commands Nautilus`. A child with its own `__init__` replaces the
parent's, so the parent's never ran, and nothing stored the name.
`super().__init__(name)` runs it.
```

## 3. Through super, or not?

```question
id: through-super-or-not-1
type: fill-in-the-blank

- A knight's armour blocks 2 of every hit, and every other rule about damage still applies. Its `take_damage` should {go through super()|replace the parent's without super()}.
- A ghost cannot be hurt by an ordinary hit at all. Its `take_damage` should {replace the parent's without super()|go through super()}.
```

<details class="dl-answer"><summary>why</summary>

The knight only changes the amount, so the parent's rules are still the
right rules: `super().take_damage(...)` with a smaller hit. The ghost
refuses the very thing the parent does, so it writes its own version,
perhaps one line that prints "The blow passes through."

</details>

## 4. A knight in armour

Can you write `Knight(Character)`, whose armour blocks 2 of every hit? A
hit of 1 or 2 does no harm at all. The cell starts with `Character` as it
stands now.

```python exec
id: a-knight-in-armour-1
{{include: setup/oop/game-4.py}}

lancelot = Knight("Lancelot", 10)
lancelot.take_damage(5)
print(lancelot)
```

```inputs
str(lancelot)
lancelot.get_health()
```

```hint
Which method already keeps the rules about damage? What should the amount
be, after the armour, for a hit of 5? And for a hit of 1?
```

```solution
{{include: setup/oop/game-4.py}}


class Knight(Character):
    def take_damage(self, amount):
        super().take_damage(max(0, amount - 2))

lancelot = Knight("Lancelot", 10)
lancelot.take_damage(5)
print(lancelot)
---
`Lancelot (health 7)`. `max(0, ...)` keeps a small hit from turning into
a negative one, which the parent would refuse with the wrong message.
```

## 5. The tanker's tank

```python exec
id: the-tankers-tank-1
class Probe:
    tank_size = 100

    def __init__(self, fuel):
        self.fuel = fuel

    def refuel(self, kg):
        self.fuel = min(Probe.tank_size, self.fuel + kg)

class Tanker(Probe):
    tank_size = 500

tanker = Tanker(300)
tanker.refuel(100)
print(tanker.fuel)
```

```predict
type: number

What will it print?
```

<details class="dl-answer"><summary>why</summary>

`100`: refuelling took the tanker from 300 down to 100. `refuel` reads
`Probe.tank_size`, which is always 100, and the tanker's own 500 is never
asked for. `min(self.tank_size, ...)` would find the tanker's value first,
and print 400.

</details>

## 6. Is it a kind?

```question
id: is-it-a-kind-1
type: fill-in-the-blank

- `Captain(CrewMember)`: a captain {is a kind of|is not a kind of} crew member.
- `Engine(Submarine)`: an engine {is not a kind of|is a kind of} submarine.
- `Moon(Planet)`: a moon {is not a kind of|is a kind of} planet.
```

<details class="dl-answer"><summary>why</summary>

A captain is a crew member with something more, so a child class fits.
A submarine *has* an engine, which is the next page's subject. A moon
and a planet share a lot (a name, a size, an orbit), but a moon is not a
planet. Both could be children of one parent, perhaps `Body`.

</details>

## 7. From earlier: class or field?

From *Designing classes*. A description says: "Each dragon has a name, a
colour and a hoard of treasure, and guards its hoard: nobody may take more
than one piece at a time." Which of name, colour and hoard would you make
a class?

<details class="dl-answer"><summary>one answer</summary>

Name and colour are fields: one value each. The hoard keeps a rule (one
piece at a time) and holds many things, so it could be a class, or a
private list on the dragon, with a `take()` method that keeps the rule.
Both are good answers.

</details>

## 8. From earlier: where the mistake is

From *Your development environment: finding a bug inside a class*.

```text
Traceback (most recent call last):
  File "<cell party-1>", line 15, in <module>
    mira.heal_other(ada, "5")
    ~~~~~~~~~~~~~~~^^^^^^^^^^
  File "<cell party-1>", line 11, in heal_other
    other.heal(amount)
    ~~~~~~~~~~^^^^^^^^
  File "<cell party-1>", line 7, in heal
    self._health = min(self.max_health, self._health + amount)
                                        ~~~~~~~~~~~~~^~~~~~~~
TypeError: unsupported operand type(s) for +: 'int' and 'str'
```

```question
id: where-the-mistake-is-1
type: multiple-choice
answer: 1

Which line would you change?

- Line 15, `mira.heal_other(ada, "5")`
  - `"5"` is text, and it travels down two calls before anything fails.
- Line 11, `other.heal(amount)`
  - The middle call passes the amount on.
- Line 7, the line with `min`
  - The last line named is the one that failed.
```

<details class="dl-answer"><summary>why</summary>

Line 15: the quotes make `"5"` a string. It passes through `heal_other`
and into `heal` before `+` meets it. Write `5`.

</details>

## 9. From earlier: stored, or gone?

From *Sequence, selection and iteration inside a class*.

```python exec
id: from-earlier-stored-or-gone-1
class Healer:
    def __init__(self, name):
        self.name = name
        self.heals_given = 0

    def heal_other(self, other):
        heals_given = self.heals_given + 1

mira = Healer("Mira")
mira.heal_other("Ada")
mira.heal_other("Grace")
print(mira.heals_given)
```

```predict
type: number

What will it print?
```

<details class="dl-answer"><summary>why</summary>

`0`. The count was stored in a plain name, which vanished when the method
ended. `self.heals_given = self.heals_given + 1` would keep it on the
healer.

</details>
