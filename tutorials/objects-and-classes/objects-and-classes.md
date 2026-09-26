---
title: "Classes and objects: keeping data and actions together"
year: "2026-2027"
version: 2026.09.26.1
worlds:
  game: A game world, with characters, the things they carry, and rooms.
  ocean: An ocean expedition, with a submarine, its crew, and what they find.
  solar-system: A solar system, with planets, moons and the probes sent to them.
  your-own: A world of your own, with a class you design and grow page by page.
covers:
  one-thing-many-parts:
    covers: [FOOP-LO1, FOOP-LO3]
  printing-an-object:
    covers: [FOOP-LO3]
---

# Classes and objects: keeping data and actions together

A game keeps its characters in a list of dictionaries, the way
[Dictionaries: looking things up by name](tutorial:looking-things-up-by-name)
kept values under names. Grace is hit, and loses 5 health. Ada falls into
a pit. What does the last line print?

```python exec
id: a-list-that-goes-wrong-1
crew = [
    {"name": "Ada", "health": 10},
    {"name": "Grace", "health": 8},
]

crew[1]["heath"] = 3                          # Grace is hit
crew[0]["health"] = crew[0]["health"] - 15    # Ada falls into a pit

for member in crew:
    print(member["name"], member["health"])
```

```predict
What will the last line print?

- Grace 3
  - The line for Grace set her health to 3.
- Grace 8
  - `"heath"` is a different key, so Grace's health never changed.
- An error
  - There is no key called `"heath"`.
```

It prints `Grace 8`, and above it, `Ada -5`. Two things went wrong, and
Python said nothing about either. The misspelt key quietly made a new
field, `"heath"`, and left Grace's health alone. And Ada's health went
below zero, which the game's rules say it never should.

So where does the rule "health never goes below 0" live? It is not in
one place. Every line that changes a health has to remember it. And where
does the list of a character's fields live? It is not in one place
either. Any line can add a key, on purpose or by a slip. Nothing in the code connects a character to the
rules about it. That connection lives only in the programmer's head, and
it holds only as long as they are careful.

## One thing, many parts

A *class* is an answer to both questions. It describes one kind of thing:
the data it holds, and the actions it can do.

```python exec
id: one-thing-many-parts-1
class Character:
    def __init__(self, name, health):
        self.name = name
        self.health = health

    def take_damage(self, amount):
        self.health = max(0, self.health - amount)

ada = Character("Ada", 10)
grace = Character("Grace", 8)
grace.take_damage(5)
ada.take_damage(15)
print(ada.name, ada.health)
print(grace.name, grace.health)
```

It prints `Ada 0` and `Grace 3`. The fields a character has are listed in
one place, `__init__`. The rule lives in one place, `take_damage`, and
`max(0, ...)` keeps health from going below zero, however hard the hit.
And a slip in a method's name gives an error, which the slip in the key
did not: `grace.take_damge(5)` stops with an `AttributeError`.

A class does not stop every slip. `grace.heath = 3` would still make a new
field, quietly, as the dictionary did. The difference comes when you use a
method, and
[Encapsulation](tutorial:keeping-details-inside-an-object) is about that.
Now we can name the parts.

| Part | In the code | What it is |
|---|---|---|
| *class* | `Character` | A description of what a character has (a name, a health) and what it can do (take damage). |
| *object* | `ada`, `grace` | One thing built from a class. Each object has its own values for the fields the class describes. |
| *field* | `name`, `health` | A piece of data one object carries with it. |
| *method* | `take_damage()` | A function that belongs to a class. It works on the fields of one particular object. |
| *constructor* | `__init__()` | The method Python runs by itself each time a new object is built. It sets that object's fields from the values passed in. |

Every method has `self` as its first parameter. *self* is the name a method
uses for the object it was called on. When we write `grace.take_damage(5)`,
`self` is `grace`, so `self.health` is Grace's health, and nobody else's.
That is why a hit on Grace cannot touch Ada.

Try building a third character, and hitting them twice.

<details class="dl-answer"><summary>What each line does</summary>

- `class Character:` starts the description. Nothing is built yet.
- `def __init__(self, name, health):` runs when a character is built.
  `self.name = name` stores the name given on the new object.
- `def take_damage(self, amount):` is a method. `self.health` is the
  health of whichever character it was called on.
- `ada = Character("Ada", 10)` builds an object. Python makes it, and runs
  `__init__` with `self` as the new object, `name` as `"Ada"` and
  `health` as 10.
- `grace.take_damage(5)` calls the method on Grace: `self` is `grace`.

</details>

### Your turn

<div class="dl-world" data-world="game">

Can you give `Character` a `heal(amount)` method, the same shape as
`take_damage`, that adds to the character's health?

```python exec
id: your-turn-1--game
class Character:
    def __init__(self, name, health):
        self.name = name
        self.health = health

    def take_damage(self, amount):
        self.health = max(0, self.health - amount)

ada = Character("Ada", 4)
ada.heal(3)
print(ada.health)
```

```inputs
ada.health
```

```hint
A method's first parameter is `self`. Inside it, `self.health` is this
character's health. What should it become?
```

```solution
class Character:
    def __init__(self, name, health):
        self.name = name
        self.health = health

    def take_damage(self, amount):
        self.health = max(0, self.health - amount)

    def heal(self, amount):
        self.health = self.health + amount

ada = Character("Ada", 4)
ada.heal(3)
print(ada.health)
---
7. Should there be a most a character can heal to? That would be a second
rule, and it would live in `heal`, in one place.
```

</div>

<div class="dl-world" data-world="ocean">

A submarine starts at the surface, at depth 0, and `dive` takes it deeper.
Can you give it a `rise(metres)` method that raises it, but never above
the surface?

```python exec
id: your-turn-1--ocean
class Submarine:
    def __init__(self, name):
        self.name = name
        self.depth = 0

    def dive(self, metres):
        self.depth = self.depth + metres

nautilus = Submarine("Nautilus")
nautilus.dive(120)
nautilus.rise(200)
print(nautilus.depth)
```

```inputs
nautilus.depth
```

```hint
Rising takes metres away from the depth. What stops the depth going below
0? `max()` gives the larger of two values.
```

```solution
class Submarine:
    def __init__(self, name):
        self.name = name
        self.depth = 0

    def dive(self, metres):
        self.depth = self.depth + metres

    def rise(self, metres):
        self.depth = max(0, self.depth - metres)

nautilus = Submarine("Nautilus")
nautilus.dive(120)
nautilus.rise(200)
print(nautilus.depth)
---
0: a submarine cannot rise above the surface, however far it is told to.
`__init__` sets the depth to 0 without being given it: a field can start
at a value every new object shares.
```

</div>

<div class="dl-world" data-world="solar-system">

A probe carries fuel, in kilograms, and `burn` uses some, never going
below empty. Can you give it a `refuel(kg)` method?

```python exec
id: your-turn-1--solar-system
class Probe:
    def __init__(self, name, fuel):
        self.name = name
        self.fuel = fuel

    def burn(self, kg):
        self.fuel = max(0, self.fuel - kg)

voyager = Probe("Voyager", 100)
voyager.burn(30)
voyager.refuel(15)
print(voyager.fuel)
```

```inputs
voyager.fuel
```

```hint
A method's first parameter is `self`. Inside it, `self.fuel` is this
probe's fuel. What should it become?
```

```solution
class Probe:
    def __init__(self, name, fuel):
        self.name = name
        self.fuel = fuel

    def burn(self, kg):
        self.fuel = max(0, self.fuel - kg)

    def refuel(self, kg):
        self.fuel = self.fuel + kg

voyager = Probe("Voyager", 100)
voyager.burn(30)
voyager.refuel(15)
print(voyager.fuel)
---
85. A real probe cannot be refuelled once it is launched, so perhaps
`refuel` belongs to a probe on the launch pad. What a class allows is a
decision about the world it describes.
```

</div>

<div class="dl-world" data-world="your-own">

Choose a kind of thing in your world: a creature, a vehicle, a shop, a
spell. What two or three fields would one of them carry? What is one thing
it can do? Can you write the class, with `__init__` and that one method,
and build two objects from it?

```python exec
id: your-turn-1--your-own
# My class, and two objects built from it.
```

</div>

## Printing an object

We printed `ada.name` and `ada.health` one at a time. What happens if we
print the whole object?

```python exec
id: printing-an-object-1
class Character:
    def __init__(self, name, health):
        self.name = name
        self.health = health

ada = Character("Ada", 10)
print(ada)
```

It prints something like `<__dewlab__.Character object at 0xf28380>`:
where the class was made (on this site, `__dewlab__`; in a file run as a
program, `__main__`), the class's name, and the place in memory where this
object is stored. The number changes each time you run it. It tells us the
object exists, and not much else.

`__str__` is a method that returns the text `print()` shows for an object.
Like `__init__`, its name has two underscores on each side, and Python
calls it for us: we never write `ada.__str__()` ourselves. What do you
think the last line shows?

```python exec
id: printing-an-object-2
class Character:
    def __init__(self, name, health):
        self.name = name
        self.health = health

    def __str__(self):
        return f"{self.name} (health {self.health})"

ada = Character("Ada", 10)
grace = Character("Grace", 8)
print(ada)
print([ada, grace])
```

The first line is `Ada (health 10)`. `__str__` *returns* the text. It does
not print it. `print()` does the printing. The list still shows the long
memory form, because an object inside a list is shown with a second method,
`__repr__`: text meant for the programmer, usually written to look like the
code that would build the object:

```python
    def __repr__(self):
        return f"Character('{self.name}', {self.health})"
```

With it, `print([ada, grace])` shows
`[Character('Ada', 10), Character('Grace', 8)]`.

### Your turn: your class, first version

This is the first version of the class you will grow over the next pages:
one class with `__init__` and `__str__`.

<div class="dl-world" data-world="game">

Can you give `Character` a `__str__` that shows its name and health, like
`Ada (health 7)`, and keep `take_damage` and `heal`?

```python exec
id: your-class-1--game
class Character:
    def __init__(self, name, health):
        self.name = name
        self.health = health

    def take_damage(self, amount):
        self.health = max(0, self.health - amount)

    def heal(self, amount):
        self.health = self.health + amount

ada = Character("Ada", 10)
ada.take_damage(3)
print(ada)
```

```inputs
str(ada)
str(Character("Grace", 8))
```

```solution
{{include: setup/oop/game-1.py}}

ada = Character("Ada", 10)
ada.take_damage(3)
print(ada)
---
`str(ada)` is what `print(ada)` shows: `Ada (health 7)`. The next pages
build on this class.
```

</div>

<div class="dl-world" data-world="ocean">

Can you give `Submarine` a `__str__` that shows its name and depth, like
`Nautilus at 120 m`, and keep `dive` and `rise`?

```python exec
id: your-class-1--ocean
class Submarine:
    def __init__(self, name):
        self.name = name
        self.depth = 0

    def dive(self, metres):
        self.depth = self.depth + metres

    def rise(self, metres):
        self.depth = max(0, self.depth - metres)

nautilus = Submarine("Nautilus")
nautilus.dive(120)
print(nautilus)
```

```inputs
str(nautilus)
str(Submarine("Alvin"))
```

```solution
{{include: setup/oop/ocean-1.py}}

nautilus = Submarine("Nautilus")
nautilus.dive(120)
print(nautilus)
---
`Nautilus at 120 m`, and a new submarine is `Alvin at 0 m`. The next pages
build on this class.
```

</div>

<div class="dl-world" data-world="solar-system">

Can you give `Probe` a `__str__` that shows its name and fuel, like
`Voyager (fuel 70 kg)`, and keep `burn` and `refuel`?

```python exec
id: your-class-1--solar-system
class Probe:
    def __init__(self, name, fuel):
        self.name = name
        self.fuel = fuel

    def burn(self, kg):
        self.fuel = max(0, self.fuel - kg)

    def refuel(self, kg):
        self.fuel = self.fuel + kg

voyager = Probe("Voyager", 100)
voyager.burn(30)
print(voyager)
```

```inputs
str(voyager)
str(Probe("Juno", 12))
```

```solution
{{include: setup/oop/solar-system-1.py}}

voyager = Probe("Voyager", 100)
voyager.burn(30)
print(voyager)
---
`Voyager (fuel 70 kg)`. The next pages build on this class.
```

</div>

<div class="dl-world" data-world="your-own">

Can you give your class a `__str__` that shows what a person would want to
know about one object, and print two objects with it? This is the first
version of your class. The next pages build on it.

```python exec
id: your-class-1--your-own
# My class, with __init__ and __str__.
```

</div>

## Looking back

Loose variables, dictionaries and functions can do everything a class can.
Nothing here was impossible before. A class changes where the rules and
the fields live, and how much you have to hold in your head as a program
grows past one character, one submarine, one anything. Which of the two
problems at the top of the page, the misspelt key or the broken rule, do
you think a class solves better?

A challenge: give a class a `__repr__` as well as a `__str__`, and put
three objects in a list. Can you make `print()` of the list show code that
would build them again?

```python challenge
class Character:
    def __init__(self, name, health):
        self.name = name
        self.health = health

    def __str__(self):
        return f"{self.name} (health {self.health})"

party = [Character("Ada", 10), Character("Grace", 8), Character("Alan", 9)]
print(party)
```

Next, [Sequence, selection and iteration inside a class](tutorial:the-moves-you-already-know)
looks inside methods, and finds the moves you already know.

## Where to read more

Everything here is covered elsewhere too, often in a form that will suit you
better than this one.

Downey, A. B. (2015). *Think Python: How to Think Like a Computer
Scientist* (2nd ed.). Green Tea Press. Free at
<https://greenteapress.com/wp/think-python-2e/>. Chapter 15 covers classes
and objects at greater length, from the same starting point as this page.

Python Software Foundation. *The Python Tutorial*, section 9, "Classes".
<https://docs.python.org/3/tutorial/classes.html>. This is the official
reference. It covers more of what `self` and inheritance can do than this
page has room for.
