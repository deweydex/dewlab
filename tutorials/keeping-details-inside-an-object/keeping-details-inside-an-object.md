---
title: "Encapsulation: keeping an object's data behind its methods"
year: "2026-2027"
version: 2026.09.26.1
worlds:
  game: A game world, with characters, the things they carry, and rooms.
  ocean: An ocean expedition, with a submarine, its crew, and what they find.
  solar-system: A solar system, with planets, moons and the probes sent to them.
  your-own: A world of your own, with a class you design and grow page by page.
covers:
  one-place-for-the-rules:
    covers: [FOOP-LO3]
  reaching-in-from-outside:
    covers: [FOOP-LO3]
  what-a-caller-needs-to-know:
    covers: [FOOP-LO3]
    touches: [FOOP-LO4]
---

# Encapsulation: keeping an object's data behind its methods

The Nautilus has a hull that is safe to 400 m, and no deeper. Here is its
class, with that rule inside `dive`. The submarine is told to dive 500 m,
then 150 m. How deep is it at the end?

```python exec
id: keeping-details-to-itself-1
class Submarine:
    def __init__(self, name):
        self.name = name
        self.depth = 0

    def dive(self, metres):
        if self.depth + metres > 400:
            print("Refused: the hull is safe only to 400 m.")
            return
        self.depth = self.depth + metres

nautilus = Submarine("Nautilus")
nautilus.dive(500)
nautilus.dive(150)
print(nautilus.depth)
```

```predict
What will the last line print?

- 150
  - The first dive is refused, and the second goes through.
- 650
  - Both dives go through.
- 400
  - The first dive stops at the limit, and the second is refused.
```

It prints the refusal, then `150`. The first dive would take the
Nautilus past 400 m, so `dive` refuses it and changes nothing. The second
goes through.

## One place for the rules

Every dive passes through one method, so that is the place to put the
rule. The check is not copied into every line of the program that makes
the submarine dive. Any code that calls `dive()` gets the check, whether
its writer remembered the rule or not.

This idea has a name. *Encapsulation* means that an object's data stays
behind its own methods. Code outside the class asks the object to make a change,
and the object's methods decide how. The rules about the data then live
in one place, next to the data itself.

But the other methods need rules too. What does `rise(-500)` do to this submarine? Run it and see. Can you make
`rise` refuse a negative number of metres, the way `dive` refuses a dive
that is too deep?

```python exec
id: keeping-details-to-itself-2
class Submarine:
    def __init__(self, name):
        self.name = name
        self.depth = 0

    def dive(self, metres):
        if self.depth + metres > 400:
            print("Refused: the hull is safe only to 400 m.")
            return
        self.depth = self.depth + metres

    def rise(self, metres):
        # Refuse a negative number of metres here.
        self.depth = max(0, self.depth - metres)

nautilus = Submarine("Nautilus")
nautilus.rise(-500)
print(nautilus.depth)
```

```inputs
nautilus.depth
```

```hint
Copy the shape of the check in `dive`: an `if`, a message, and `return`.
What is the condition this time? And where must the check go, so that the
`return` stops the method before the depth changes?
```

```solution
class Submarine:
    def __init__(self, name):
        self.name = name
        self.depth = 0

    def dive(self, metres):
        if self.depth + metres > 400:
            print("Refused: the hull is safe only to 400 m.")
            return
        self.depth = self.depth + metres

    def rise(self, metres):
        if metres < 0:
            print("Refused: rise needs a positive number of metres.")
            return
        self.depth = max(0, self.depth - metres)

nautilus = Submarine("Nautilus")
nautilus.rise(-500)
print(nautilus.depth)
---
The refusal, then `0`. Without the check, rising by −500 m took the
Nautilus down to 500 m, past its hull's limit, and `dive` never had a
chance to say no. Is there another call that goes around the limit?
```

## Reaching in from outside

The rule in `dive` works when code calls `dive`. But does Python make code
call it? With the `Submarine` from the top of the page, what does this
print?

```python exec
id: reaching-in-from-outside-1
nautilus = Submarine("Nautilus")
nautilus.dive(500)     # through the method: refused
nautilus.depth = 600   # reaching in: nothing checks it
print(nautilus.depth)
```

```predict
What will the last line print?

- 600
  - The last line changes the field directly, and nothing checks it.
- 0
  - The rule in `dive` keeps the depth safe.
```

It prints `600`. The method refused the dive, but the next line went
around the method and changed the field directly. Python did not stop it.

Some languages, such as Java, can lock a field so that only the class's
own methods can change it. Python has no lock like that. It relies on a
*convention*: a habit that programmers agree to follow. A name that
starts with one underscore, such as `_depth`, means "this is private to
the class; use the methods instead". A *private* field is one that only
the class's own methods should read or change.

The class then gives other code a method to read the value, often called
a *getter*. A getter is a method that returns the value of a private
field. Here is the submarine with a private `_depth` and a getter,
`get_depth()`. What will it print?

```python exec
id: reaching-in-from-outside-2
class Submarine:
    def __init__(self, name):
        self.name = name
        self._depth = 0

    def get_depth(self):
        return self._depth

    def dive(self, metres):
        if self._depth + metres > 400:
            print("Refused: the hull is safe only to 400 m.")
            return
        self._depth = self._depth + metres

nautilus = Submarine("Nautilus")
nautilus.dive(250)
nautilus.dive(250)
print(nautilus.get_depth())
```

The first dive goes through, the second is refused, and it prints `250`.
Code outside the class now reads the depth with `get_depth()`, and changes
it only with the methods.

The underscore is a sign for people, not a lock. `nautilus._depth = 600`
would still work. But anyone who writes it can see they are breaking the
class's rules, and someone reading the code can see it at once.

You may also see a name with two underscores at the start, such as
`__depth`. Python then adds the class's name to the front of it, which
makes it harder to reach from outside. One underscore is the more common
choice.

### Your turn: your class, second version

This is the second version of the class you started in
[Classes and objects](tutorial:objects-and-classes): one rule, kept by a
method, and the field it protects made private, with a getter.

<div class="dl-world" data-world="game">

A hit of −5 heals Ada. Can you make `take_damage` refuse a negative
amount, keep her health private as `_health`, and give the class a
`get_health()` method?

```python exec
id: your-class-2--game
{{include: setup/oop/game-1.py}}

ada = Character("Ada", 10)
ada.take_damage(-5)
print(ada)
```

```inputs
str(ada)
ada.get_health()
```

```hint
There are three changes. First the check, at the top of `take_damage`:
what is the condition? Then `health` becomes `_health`: on how many lines?
Then a getter, the same shape as `get_depth()` above.
```

```solution
{{include: setup/oop/game-2.py}}

ada = Character("Ada", 10)
ada.take_damage(-5)
print(ada)
---
The refusal, then `Ada (health 10)`. `health` became `_health` on every
line of the class, `__str__` included. `heal` has no check yet: what
would `ada.heal(-50)` do?
```

</div>

<div class="dl-world" data-world="ocean">

The Nautilus dives 300 m, then 150 m more, past its hull's limit. Can you
give your `Submarine` the rule from this page, keep its depth private as
`_depth`, and give the class a `get_depth()` method?

```python exec
id: your-class-2--ocean
{{include: setup/oop/ocean-1.py}}

nautilus = Submarine("Nautilus")
nautilus.dive(300)
nautilus.dive(150)
print(nautilus)
```

```inputs
str(nautilus)
nautilus.get_depth()
```

```hint
There are three changes. First the check, at the top of `dive`. Then
`depth` becomes `_depth`: on how many lines? Then a getter that returns
it.
```

```solution
{{include: setup/oop/ocean-2.py}}

nautilus = Submarine("Nautilus")
nautilus.dive(300)
nautilus.dive(150)
print(nautilus)
---
The refusal, then `Nautilus at 300 m`. `depth` became `_depth` on every
line of the class, `__str__` included. What would `nautilus.rise(-500)` do
to this version?
```

</div>

<div class="dl-world" data-world="solar-system">

Voyager has 70 kg of fuel left and is told to burn 80. It burns what it
has, and nothing says so. Can you make `burn` refuse a burn bigger than the
fuel that is left, keep the fuel private as `_fuel`, and give the class a
`get_fuel()` method?

```python exec
id: your-class-2--solar-system
{{include: setup/oop/solar-system-1.py}}

voyager = Probe("Voyager", 100)
voyager.burn(30)
voyager.burn(80)
print(voyager)
```

```inputs
str(voyager)
voyager.get_fuel()
```

```hint
There are three changes. First the check, at the top of `burn`: when
should it refuse? Then `fuel` becomes `_fuel`: on how many lines? Then a
getter that returns it.
```

```solution
{{include: setup/oop/solar-system-2.py}}

voyager = Probe("Voyager", 100)
voyager.burn(30)
voyager.burn(80)
print(voyager)
---
The refusal, then `Voyager (fuel 70 kg)`. With the check in place,
`max(0, ...)` has nothing left to do, so the burn is a plain subtraction.
What would `voyager.burn(-50)` do to this version?
```

</div>

<div class="dl-world" data-world="your-own">

Which rule does your world have that your class does not keep yet? A
shop's stock cannot go below zero. A creature cannot run faster than its
top speed. Can you keep the rule in a method, make the field it protects
private, and give it a getter? Your class from
[Classes and objects](tutorial:objects-and-classes) is saved in that
page's last cell. Copy it here to start.

```python exec
id: your-class-2--your-own
# My class, second version: one rule, kept by a method.
```

</div>

## What a caller needs to know

A *caller* is any code that uses an object's methods, such as
`nautilus.dive(250)` and `nautilus.get_depth()`.

*Abstraction* is the other half of encapsulation, seen from the caller's
side. Abstraction means a caller uses what a method does, without needing
to know how it does it. `nautilus.dive(250)` tells you what will happen:
the submarine goes 250 m deeper, or refuses. You do not need to know how
the depth is stored, or that an `if` guards it.

That gives the class's writer a lot of freedom: the inside of the class
can change, and callers never notice. Here is a reason to change it. The
expedition carries a spare tank of oxygen, 1 litre, and a machine uses
0.1 litres of it each minute. After 10 minutes, is the tank empty?

```python exec
id: what-a-caller-needs-to-know-1
class OxygenTank:
    def __init__(self, litres):
        self._litres = litres

    def get_litres(self):
        return self._litres

    def use(self, litres):
        self._litres = self._litres - litres

    def is_empty(self):
        return self._litres == 0

spare = OxygenTank(1.0)
for minute in range(10):
    spare.use(0.1)
print(spare.get_litres())
print(spare.is_empty())
```

```predict
What will the last line print?

- False
  - Something is left in the tank after 10 uses.
- True
  - Ten uses of 0.1 litres take 1 litre.
```

It prints `1.3877787807814457e-16`, then `False`. That first number is
0.00000000000000013877…, very nearly 0, but not 0. A decimal such as
`0.1` cannot be stored exactly in a computer, and each `use` adds a tiny
error. Ten of them leave a tank that is never quite empty.

A whole number is stored exactly. So the tank below keeps its oxygen in
whole millilitres, `_millilitres`, and changes litres to millilitres on
the way in and back to litres on the way out. `round()` gives the nearest
whole number. Compare the last five lines with the cell above. Which of
them had to change?

```python exec
id: what-a-caller-needs-to-know-2
class OxygenTank:
    def __init__(self, litres):
        self._millilitres = round(litres * 1000)

    def get_litres(self):
        return self._millilitres / 1000

    def use(self, litres):
        self._millilitres = self._millilitres - round(litres * 1000)

    def is_empty(self):
        return self._millilitres == 0

spare = OxygenTank(1.0)
for minute in range(10):
    spare.use(0.1)
print(spare.get_litres())
print(spare.is_empty())
```

None of them changed, and now it prints `0.0` and `True`. The way the
oxygen is stored is completely different. But the callers only ever used
the methods, so they did not need to change.

```question
id: what-a-caller-needs-to-know-q1
type: multiple-choice
answer: 2

A program used the first tank in these three lines. Which one stops
working when the tank changes to millilitres?

- `spare.get_litres()`
  - A getter reads the field for you.
- `print(spare._litres)`
  - The private field it reached for is gone.
- `spare.use(0.1)`
  - `use` works in litres on the outside.
```

A caller that used `_litres` directly breaks, because that field is
gone. Every caller that used the methods works as before. That is
what encapsulation and abstraction protect.

## Looking back

Python never stops code from changing `_depth` directly. So what does the
underscore protect, and who is it for?

A challenge: a health bar that starts full at `1.0` goes wrong the same
way the oxygen tank did. Ten hits of `0.1` do not bring her health to 0. Can you
change the inside of the class to keep whole hit points, 100 for a full
bar, without changing any line below the class?

```python challenge
class Character:
    def __init__(self, name):
        self.name = name
        self._health = 1.0    # a full health bar

    def get_health(self):
        return self._health

    def take_damage(self, fraction):
        self._health = max(0, self._health - fraction)

    def is_down(self):
        return self._health == 0

ada = Character("Ada")
for hit in range(10):
    ada.take_damage(0.1)
print(ada.get_health(), ada.is_down())
```

Next, [A class with many methods](tutorial:one-class-many-methods) gives a
class more to do, and keeps its rules in place while it grows.

## Where to read more

Everything here is covered elsewhere too, often in a form that will suit you
better than this one.

Python Software Foundation. *The Python Tutorial*, section 9.6, "Private
Variables". <https://docs.python.org/3/tutorial/classes.html#private-variables>.
This is the official note on the one-underscore convention and on names
with two underscores.

Python Software Foundation. *The Python Tutorial*, section 15,
"Floating-Point Arithmetic: Issues and Limitations".
<https://docs.python.org/3/tutorial/floatingpoint.html>. This section
explains why `0.1` cannot be stored exactly, and what to do about it.

Downey, A. B. (2015). *Think Python: How to Think Like a Computer
Scientist* (2nd ed.). Green Tea Press. Free at
<https://greenteapress.com/wp/think-python-2e/>. Section 17.11, "Interface
and implementation", keeps what a class shows its callers apart from how
it works inside.
