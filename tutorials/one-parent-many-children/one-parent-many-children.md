---
title: "Inheritance: one class built on another"
year: "2026-2027"
version: 2026.09.26.1
worlds:
  game: A game world, with characters, the things they carry, and rooms.
  ocean: An ocean expedition, with a submarine, its crew, and what they find.
  solar-system: A solar system, with planets, moons and the probes sent to them.
  your-own: A world of your own, with a class you design and grow page by page.
covers:
  a-class-built-on-another-class:
    covers: [FOOP-LO3, FOOP-LO6]
  a-limit-of-its-own:
    covers: [FOOP-LO3]
  another-kind-of-creature:
    covers: [FOOP-LO6]
  many-kinds-one-loop:
    covers: [FOOP-LO6, FOOP-LO7]
---

# Inheritance: one class built on another

In a game, heroes and monsters share most of what they know: a name,
health, and a way to take damage. A troll is a character too, with a
thicker hide: it takes half damage. Do we have to copy the whole
`Character` class to write a `Troll`?

Here is `Character` as it stood at the end of
[A class with many methods](tutorial:one-class-many-methods), in the game
world. Run it first. The cells below build on it.

```python exec
id: character-so-far
{{include: setup/oop/game-3.py}}
```

## A class built on another class

`Troll` below never defines `__init__`, `__str__` or `heal`. Will
`Troll("Grog", 10)` work? What will the first line print?

```python exec
id: a-class-built-on-another-class-1
class Troll(Character):
    def take_damage(self, amount):
        super().take_damage(amount // 2)

grog = Troll("Grog", 10)
grog.take_damage(7)
print(grog)
grog.heal(2)
print(grog)
```

```predict
What will the first line print?

- Grog (health 7)
  - Half of 7 is 3, as a whole number, and 10 take away 3 is 7.
- Grog (health 3)
  - The troll takes the full 7.
- An error
  - `Troll` has no `__init__` or `__str__` of its own.
```

It prints `Grog (health 7)`, then `Grog (health 9)`. The first line,
`class Troll(Character):`, says "a troll is a character, plus something
different". This is *inheritance*: building a new class on an existing
one. The new class keeps everything the existing class does, and changes
or adds only what is different.

Two names help us talk about it:

- The *parent class* is the existing class, here `Character`. It gives
  `__init__`, `__str__`, `heal` and the rest to the new class, for free.
- The *child class* is the new class, here `Troll`. It changes one
  method, `take_damage`.

<details class="dl-answer"><summary>What each line does</summary>

- `class Troll(Character):` makes a class whose parent is `Character`.
- `def take_damage(self, amount):` gives trolls their own version of
  `take_damage`.
- `super()` reaches the parent class. `super().take_damage(amount // 2)`
  runs `Character`'s own `take_damage`, with half the amount. `//` divides
  and keeps the whole number, so 7 becomes 3.
- `Troll("Grog", 10)` looks for `__init__` in `Troll`, finds none, and
  uses the one in `Character`. `grog.heal(2)` does the same.

</details>

Why go through `super()`, and not write `self._health = ...` again? Because
`Character.take_damage` already keeps two rules: a negative hit is
refused, and health stops at 0. Going through it keeps both, for trolls
too, without writing either again. Try `grog.take_damage(-8)`.

## A limit of its own

A troll can also be tougher: up to 20 health, where a person has 10. A
class attribute in the child gives it a value of its own. Grog has 18
health, and heals 5. What will it print?

```python exec
id: a-limit-of-its-own-1
class Troll(Character):
    max_health = 20

    def take_damage(self, amount):
        super().take_damage(amount // 2)

grog = Troll("Grog", 18)
grog.heal(5)
print(grog)
```

```predict
What will it print?

- Grog (health 20)
  - 18 and 5 is 23, and a troll stops at its own 20.
- Grog (health 23)
  - Nothing stops a troll at 20.
- Grog (health 10)
  - `heal` reads a limit that is not the troll's.
```

It prints `Grog (health 10)`: healing took Grog *down* from 18 to 10. Look
at the last line of `heal`, in the cell at the top of the page:

```python
        self._health = min(Character.max_health, self._health + amount)
```

`Character.max_health` asks the `Character` class, by name, and its answer
is always 10. The troll's own 20 is never asked for. Reading it through
`self` fixes that. Python looks for `self.max_health` on the object first,
then on the object's class, `Troll`, and only then on the parent. Here is
`Character` with that one line changed, and the same `Troll` under it.
Where does Grog stop now?

```python exec
id: a-limit-of-its-own-2
{{include: setup/oop/game-4.py}}


class Troll(Character):
    max_health = 20

    def take_damage(self, amount):
        super().take_damage(amount // 2)

grog = Troll("Grog", 18)
grog.heal(5)
print(grog)
```

It prints `Grog (health 20)`.

So a method that reads a class attribute should read it through `self`,
if a child class might have its own. Changing the value is still done
through the class, as on
[A class with many methods](tutorial:one-class-many-methods#class-attributes-and-instance-attributes).

## Another kind of creature

A child's method with the same name as the parent's replaces it, for the
child. This is called *overriding*. `Troll` overrides `take_damage`, and
still calls the parent's version through `super()`.

A phoenix is different. When a phoenix is down, it can still heal: it
rises from its own ashes. `Character.heal` refuses anyone who is down, so
a phoenix cannot go through it. What will the last line print?

```python exec
id: another-kind-of-creature-1
class Phoenix(Character):
    def heal(self, amount):
        self._health = min(self.max_health, self._health + amount)

ember = Phoenix("Ember", 10)
ember.take_damage(15)
print(ember, ember.is_down())
ember.heal(5)
print(ember)
```

```predict
What will the last line print?

- Ember (health 5)
  - The phoenix's own `heal` has no check for being down.
- Ember (health 0)
  - Nobody who is down can be healed.
```

It prints `Ember (health 5)`. The two overrides are two different
decisions:

- `Troll.take_damage` goes through `super()`, because the parent's rules
  are still the right rules. Only the amount changes.
- `Phoenix.heal` does not, because the parent's rule is the one thing a
  phoenix breaks. It writes its own line instead, and keeps the rule that
  still applies: never above `max_health`.

`take_damage` is not overridden at all in `Phoenix`. A phoenix is hurt
like anyone else, so it keeps its parent's version. A parent can have
many children, each changing something different, and none of them
changes the others.

## Many kinds, one loop

A person, a troll and a phoenix are all characters, so one loop can treat
them alike. Each takes a hit of 12, then heals 4. What will each line
print?

```python exec
id: many-kinds-one-loop-1
party = [Character("Ada", 10), Troll("Grog", 20), Phoenix("Ember", 10)]
for member in party:
    member.take_damage(12)
    member.heal(4)
    print(member)
```

It prints the refusal for Ada, then `Ada (health 0)`, `Grog (health 18)`
and `Ember (health 4)`. The same two lines did three different things:

- Ada took all 12, went down, and could not be healed.
- Grog took 6, from 20 to 14, and healed to 18.
- Ember went down too, and healed anyway.

The loop never asked which kind of character it had. Each object runs the
version of the method that belongs to its own class. This is
*polymorphism*: one method name working across several classes, each
object running its own version.

### Your turn: your class, fourth version

This is the fourth version of your class. It gets at most one child class,
and one sentence, as a comment, that says why the child is a kind of the
parent. A class with no child is a fair answer too, if you can say why.
Is there a class attribute that a child might want its own value for?

<div class="dl-world" data-world="game">

A healer is a character who can also heal someone else. Can you write
`Healer(Character)`, with a `heal_other(other, amount)` method? A healer
who is down cannot heal anyone. The `Character` here is the one with
`self.max_health`.

```python exec
id: your-class-4--game
{{include: setup/oop/game-4.py}}

# Your Healer here

ada = Character("Ada", 4)
mira = Healer("Mira", 10)
mira.heal_other(ada, 5)
print(ada)
```

```inputs
str(ada)
str(mira)
```

```hint
Which of `Character`'s methods already does the healing, and keeps its
rules? How does one object ask another to do something?
```

```solution
{{include: setup/oop/game-4.py}}

{{include: setup/oop/game-4-kind.py}}

ada = Character("Ada", 4)
mira = Healer("Mira", 10)
mira.heal_other(ada, 5)
print(ada)
---
`Ada (health 9)`. `heal_other` does not change Ada's health itself: it
asks Ada to `heal`, so Ada's own rules decide, down or not, and her own
`max_health`. A healer is still a character: it can take damage, and be
healed, with nothing new written.
```

</div>

<div class="dl-world" data-world="ocean">

A bathyscaphe is a submarine built for the deepest trenches: the real
Trieste reached 10,916 m in 1960. Can you write
`Bathyscaphe(Submarine)`, with a hull safe to 11,000 m? Watch what
happens to the limit, and remember this page's troll.

```python exec
id: your-class-4--ocean
{{include: setup/oop/ocean-3.py}}

# Your Bathyscaphe here

trieste = Bathyscaphe("Trieste")
trieste.dive(5000)
print(trieste)
```

```inputs
str(trieste)
trieste.room_below()
str(Submarine("Nautilus"))
```

```hint
A class attribute in the child gives it its own limit. If the dive is
still refused at 400 m, which lines of `Submarine` ask for the limit, and
whose limit do they ask for?
```

```solution
{{include: setup/oop/ocean-4.py}}

{{include: setup/oop/ocean-4-kind.py}}

trieste = Bathyscaphe("Trieste")
trieste.dive(5000)
print(trieste)
---
`Trieste at 5000 m`. The child is one line, `hull_limit = 11000`. The
work is in the parent: `room_below` and the refusal both read
`self.hull_limit`, not `Submarine.hull_limit`, so a bathyscaphe's own
limit is the one they find.
```

</div>

<div class="dl-world" data-world="solar-system">

A lander is a probe that can land, and once it is down, it burns no more
fuel. Can you write `Lander(Probe)`, with a `land()` method? Which one
method would you override, so that `burn` refuses after landing without
being written again?

```python exec
id: your-class-4--solar-system
{{include: setup/oop/solar-system-3.py}}

# Your Lander here

philae = Lander("Philae", 40)
philae.burn(10)
philae.land()
philae.burn(5)
print(philae)
```

```inputs
str(philae)
philae.can_burn(5)
Lander("Rosetta", 40).can_burn(5)
```

```hint
`Probe.burn` asks `self.can_burn(kg)` before it burns. For a lander,
`self` is the lander. What should a lander that has landed answer?
```

```solution
{{include: setup/oop/solar-system-4.py}}

{{include: setup/oop/solar-system-4-kind.py}}

philae = Lander("Philae", 40)
philae.burn(10)
philae.land()
philae.burn(5)
print(philae)
---
A refusal, then `Philae (fuel 30 kg)`. `Lander` overrides `can_burn`
only. `Probe.burn` asks `self.can_burn(kg)`, and for a lander that runs
`Lander`'s version: the parent's method calls the child's. The refusal
now says "cannot burn 5 kg now", since "not enough fuel" is no longer the
only reason. `refuel` reads `self.tank_size` too, ready for a child with a
bigger tank.
```

</div>

<div class="dl-world" data-world="your-own">

Is there a kind of your thing that is a special case: it does one thing
differently, or one thing more? Write at most one child class, with a
comment of one sentence that says why it is a kind of your class. If no
kind fits your world, write that sentence instead: it is a design decision
too.

```python exec
id: your-class-4--your-own
# My class, fourth version: at most one child class, and why.
```

</div>

## Looking back

`Troll.take_damage` went through `super()`, and `Phoenix.heal` did not.
What did each one keep of its parent, and what did each one give up?

A challenge: a zombie is a character that gets up once. The first time a
hit knocks it down, it stands up again with 5 health. Can you write
`Zombie(Character)`, and keep every rule `take_damage` already has?

```python challenge
# Paste Character from the top of the page here, with self.max_health.

class Zombie(Character):
    def __init__(self, name, health):
        super().__init__(name, health)
        self._risen = False

mort = Zombie("Mort", 10)
mort.take_damage(12)
print(mort)
mort.take_damage(12)
print(mort)
```

Next, [Composition: objects inside other objects](tutorial:objects-inside-objects)
builds a class that holds other objects, which is a second way to build
one class from another.

## Where to read more

Everything here is covered elsewhere too, often in a form that will suit you
better than this one.

Downey, A. B. (2015). *Think Python: How to Think Like a Computer
Scientist* (2nd ed.). Green Tea Press. Free at
<https://greenteapress.com/wp/think-python-2e/>. Chapter 18,
"Inheritance", builds a deck of cards and a hand from it, one class on
another.

Python Software Foundation. *The Python Tutorial*, section 9.5,
"Inheritance". <https://docs.python.org/3/tutorial/classes.html#inheritance>.
The official reference, including how Python finds a method, and classes
with more than one parent, which this page does not need.
