---
title: "Your development environment: finding a bug inside a class"
year: "2026-2027"
version: 2026.09.26.1
worlds:
  game: A game world, with characters, the things they carry, and rooms.
  ocean: An ocean expedition, with a submarine, its crew, and what they find.
  solar-system: A solar system, with planets, moons and the probes sent to them.
  your-own: A world of your own, with a class you design and grow page by page.
covers:
  a-bug-two-calls-deep:
    covers: [FOOP-LO5]
  printing-what-you-need-to-see:
    covers: [FOOP-LO5]
  what-the-editor-already-knows:
    covers: [FOOP-LO5]
  where-a-bigger-project-lives:
    covers: [FOOP-LO5]
---

# Your development environment: finding a bug inside a class

Ada attacks Grace. The cell below should print Grace's health after the
hit. Run it: it stops with an error, and that is on purpose. The error
names three lines of the cell.

```python exec
id: a-bug-two-calls-deep-1
class Character:
    def __init__(self, name, health, strength):
        self.name = name
        self.health = health
        self.strength = strength

    def take_damage(self, amount):
        self.health = max(0, self.helth - amount)

    def attack(self, other):
        other.take_damage(self.strength)

ada = Character("Ada", 10, 4)
grace = Character("Grace", 8, 3)
ada.attack(grace)
print(grace.health)
```

```question
id: a-bug-two-calls-deep-q1
type: multiple-choice
answer: 3

Which of the three lines would you change?

- Line 15, `ada.attack(grace)`
  - The first line the error names is where the trouble started.
- Line 11, `other.take_damage(self.strength)`
  - The middle line is where one method calls the other.
- Line 8, `self.health = max(0, self.helth - amount)`
  - The last line the error names is the one that failed.
```

## A bug two calls deep

The error is a *traceback*: Python's list of the calls that were running
when it stopped. Read it from the bottom.

- The last line names the error: `AttributeError: 'Character' object has
  no attribute 'helth'. Did you mean: 'health'?`
- Just above it is the line that failed, line 8, inside `take_damage`. The
  marks under it point at the part that failed: `self.helth`.
- Each `File` line above that is one call further out. `take_damage` was
  called by line 11, inside `attack`. And `attack` was called by line 15,
  the line you ran.

This time the mistake is at the bottom: `helth` is a slip for `health`.
Lines 15 and 11 are fine. They are the route Python took to reach line 8.
Fix the slip, and run the cell again: Grace ends with 4 health.

Is the mistake always on the bottom line? In this cell, one word in
`attack` has changed. Run it, and look at where the error is.

```python exec
id: a-bug-two-calls-deep-2
class Character:
    def __init__(self, name, health, strength):
        self.name = name
        self.health = health
        self.strength = strength

    def take_damage(self, amount):
        self.health = max(0, self.health - amount)

    def attack(self, other):
        other.take_damage(self.name)

ada = Character("Ada", 10, 4)
grace = Character("Grace", 8, 3)
ada.attack(grace)
print(grace.health)
```

The error is at line 8 again, in `take_damage`:
`unsupported operand type(s) for -: 'int' and 'str'`. Python cannot take
a string away from a number. But `take_damage` is the same as it was in
the first cell, where it worked once the slip was fixed. The string came
from its caller. Line 11 passes `self.name`, which is `"Ada"`, where it
should pass `self.strength`.

An error shows where Python could go no further. The mistake can be one
call further out, in the line that passed in the wrong value. So read a
traceback from the bottom, and then ask of each line above it: did this
line give the method below it what that method expects? When one method
calls another, that is where a class's mistakes like to hide.

Finding the mistake that makes a program go wrong, and fixing it, is
called *debugging*.

### Your turn

<div class="dl-world" data-world="game">

Ada loots a chest, and each item should go into her bag. Run the cell,
read the traceback from the bottom, and find the mistake. Can you fix it?

```python exec
id: a-bug-two-calls-deep-3--game
class Character:
    def __init__(self, name, health):
        self.name = name
        self.health = health
        self.bag = []

    def pick_up(self, item):
        self.bag.add(item)

    def loot(self, items):
        for item in items:
            self.pick_up(item)

ada = Character("Ada", 10)
ada.loot(["rope", "lamp", "key"])
print(ada.bag)
```

```inputs
ada.bag
```

```hint
The last line names a list. Which of a list's methods puts one more item
at its end?
```

```solution
class Character:
    def __init__(self, name, health):
        self.name = name
        self.health = health
        self.bag = []

    def pick_up(self, item):
        self.bag.append(item)    # fixed: append, not add

    def loot(self, items):
        for item in items:
            self.pick_up(item)

ada = Character("Ada", 10)
ada.loot(["rope", "lamp", "key"])
print(ada.bag)
---
`['rope', 'lamp', 'key']`. The mistake was on the bottom line this time:
a list has no `add`. `loot` and the last line were only the route there.
```

</div>

<div class="dl-world" data-world="ocean">

The Nautilus uses 1 litre of oxygen for every 10 metres it dives. Run
the cell, read the traceback from the bottom, and find the mistake. Can
you fix it?

```python exec
id: a-bug-two-calls-deep-3--ocean
class Submarine:
    def __init__(self, name, oxygen):
        self.name = name
        self.oxygen = oxygen
        self.depth = 0

    def use_oxygen(self, litres):
        self.oxygen = max(0, oxygen - litres)

    def dive(self, metres):
        self.depth = self.depth + metres
        self.use_oxygen(metres // 10)

nautilus = Submarine("Nautilus", 500)
nautilus.dive(120)
print(nautilus.oxygen)
```

```inputs
nautilus.oxygen
nautilus.depth
```

```hint
The last line makes a suggestion. Inside a method, where does Python find
the fields of the object the method was called on?
```

```solution
class Submarine:
    def __init__(self, name, oxygen):
        self.name = name
        self.oxygen = oxygen
        self.depth = 0

    def use_oxygen(self, litres):
        self.oxygen = max(0, self.oxygen - litres)    # fixed: self.oxygen

    def dive(self, metres):
        self.depth = self.depth + metres
        self.use_oxygen(metres // 10)

nautilus = Submarine("Nautilus", 500)
nautilus.dive(120)
print(nautilus.oxygen)
---
488 litres. Inside a method, a field is always reached through `self`.
Leaving `self.` out is one of the most common slips in a class, and Python
now suggests the fix in its error.
```

</div>

<div class="dl-world" data-world="solar-system">

Juno burns 3 kg of fuel for each day it travels. Run the cell, read the
traceback from the bottom, and find the mistake. Can you fix it?

```python exec
id: a-bug-two-calls-deep-3--solar-system
class Probe:
    def __init__(self, name, fuel, rate):
        self.name = name
        self.fuel = fuel
        self.rate = rate

    def burn(self, kg):
        self.fuel = max(0, self.fuel - kg)

    def travel(self, days):
        self.burn(days, self.rate)

juno = Probe("Juno", 100, 3)
juno.travel(10)
print(juno.fuel)
```

```inputs
juno.fuel
```

```hint
`burn` has one parameter besides `self`. How many values does line 11
give it? And why might Python count one more than you can see?
```

```solution
class Probe:
    def __init__(self, name, fuel, rate):
        self.name = name
        self.fuel = fuel
        self.rate = rate

    def burn(self, kg):
        self.fuel = max(0, self.fuel - kg)

    def travel(self, days):
        self.burn(days * self.rate)    # fixed: one value, the kilograms

juno = Probe("Juno", 100, 3)
juno.travel(10)
print(juno.fuel)
---
70 kg. The error said `burn()` takes 2 positional arguments but 3 were
given: one more on each side than you can see, because Python counts
`self`. The method has `self` and `kg`. The call gave it `juno`, `days`
and `self.rate`.
```

</div>

<div class="dl-world" data-world="your-own">

Can you break your own class on purpose? Misspell a field inside one
method, and call that method from another. Before you run it, which lines
do you think the traceback will name?

```python exec
id: a-bug-two-calls-deep-3--your-own
# My class, broken on purpose, one method calling another.
```

</div>

## Printing what you need to see

Not every bug stops with an error. Ada takes three hits of 5. Her armour
blocks 1 point of each hit, so each hit costs her 4 health, and three
hits should leave her at 0. Run the cell.

```python exec
id: printing-what-you-need-to-see-1
class Character:
    def __init__(self, name, health):
        self.name = name
        self.health = health

    def take_damage(self, amount):
        self.health = max(0, self.health - amount)

    def take_hits(self, hits):
        for hit in hits:
            self.take_damage(hit)
            self.health = self.health + 1    # the armour blocks 1 point

ada = Character("Ada", 10)
ada.take_hits([5, 5, 5])
print(ada.health)
```

It prints `1`, and nothing says why. A traceback cannot help, because
nothing failed. What we need is to see the health after each hit. Add
this line at the end of the loop, under the armour line, with the same
indent, and run the cell again:

```python
            print("after a hit of", hit, "health is", self.health)
```

Now we can see each step: 6, then 2, then 1. The first two are what we
expected: 10 take away 4 is 6, and 6 take away 4 is 2. The third is
where it goes wrong. Health 2 and a hit of 4 should leave 0.

<details class="dl-answer"><summary>Why the third hit leaves 1</summary>

The armour line runs after the hit has landed. For the first two hits,
that makes no difference: taking 5 and adding 1 comes to the same as
taking 4. But the third hit takes the health from 2 to 0, and
`max(0, ...)` stops it there. Then the armour line adds 1, and Ada is
standing again. The armour should make the hit smaller before it lands:

```python
    def take_hits(self, hits):
        for hit in hits:
            self.take_damage(hit - 1)    # the armour blocks 1 point
```

</details>

A `print()` inside a method, showing the fields of `self` at the moment
it runs, is one of the oldest ways of debugging, and one of the most used.
Delete the print lines once you have found the bug. They are for you, not
for the people who use your program.

### Your turn

<div class="dl-world" data-world="game">

Gold is worth 10 points, silver 5, and any other coin 1. Ada collects a
gold, a silver and a copper coin, so she should score 16. Can you print
her score after each coin, find the coin that goes wrong, and fix it?

```python exec
id: printing-what-you-need-to-see-2--game
class Character:
    def __init__(self, name):
        self.name = name
        self.score = 0

    def collect(self, coins):
        for coin in coins:
            if coin == "gold":
                self.score = self.score + 10
            if coin == "silver":
                self.score = self.score + 5
            else:
                self.score = self.score + 1

ada = Character("Ada")
ada.collect(["gold", "silver", "copper"])
print(ada.score)
```

```inputs
ada.score
```

```hint
Which coin gives a score you did not expect? For that coin, which of the
`if` lines and the `else` line run?
```

```solution
class Character:
    def __init__(self, name):
        self.name = name
        self.score = 0

    def collect(self, coins):
        for coin in coins:
            if coin == "gold":
                self.score = self.score + 10
            elif coin == "silver":    # fixed: elif, not if
                self.score = self.score + 5
            else:
                self.score = self.score + 1

ada = Character("Ada")
ada.collect(["gold", "silver", "copper"])
print(ada.score)
---
16. With two separate `if` lines, the `else` belongs only to the second
one. A gold coin is not silver, so it scored 10 and then 1 more. `elif`
joins the three paths into one choice.
```

</div>

<div class="dl-world" data-world="ocean">

The Nautilus dives 120 m, rises 50 m, then dives 200 m more, so the
deepest it has been is 270 m. Can you print the fields inside `dive`,
find where the deepest depth goes missing, and fix it?

```python exec
id: printing-what-you-need-to-see-2--ocean
class Submarine:
    def __init__(self, name):
        self.name = name
        self.depth = 0
        self.deepest = 0

    def dive(self, metres):
        self.depth = self.depth + metres
        if self.depth > self.deepest:
            deepest = self.depth

    def rise(self, metres):
        self.depth = max(0, self.depth - metres)

nautilus = Submarine("Nautilus")
nautilus.dive(120)
nautilus.rise(50)
nautilus.dive(200)
print(nautilus.deepest)
```

```inputs
nautilus.deepest
nautilus.depth
```

```hint
Print `self.depth` and `self.deepest` at the end of `dive`. Which one
never changes? Which line was meant to change it?
```

```solution
class Submarine:
    def __init__(self, name):
        self.name = name
        self.depth = 0
        self.deepest = 0

    def dive(self, metres):
        self.depth = self.depth + metres
        if self.depth > self.deepest:
            self.deepest = self.depth    # fixed: stored on the object

    def rise(self, metres):
        self.depth = max(0, self.depth - metres)

nautilus = Submarine("Nautilus")
nautilus.dive(120)
nautilus.rise(50)
nautilus.dive(200)
print(nautilus.deepest)
---
270. `deepest = self.depth` stored the depth in a plain name, which
vanished when `dive` ended. The same slip was on
[Sequence, selection and iteration inside a class](tutorial:the-moves-you-already-know#storing-inside-a-class).
```

</div>

<div class="dl-world" data-world="solar-system">

Jupiter's four big moons are 16,854 km wide, laid side by side. Can you
print `total` inside the loop, find where the sum goes wrong, and fix it?

```python exec
id: printing-what-you-need-to-see-2--solar-system
class Planet:
    def __init__(self, name, moons):
        self.name = name
        self.moons = moons

    def total_moon_width(self):
        for width in self.moons:
            total = 0
            total = total + width
        return total

jupiter = Planet("Jupiter", [3643, 3122, 5268, 4821])
print(jupiter.total_moon_width())
```

```inputs
jupiter.total_moon_width()
Planet("Mars", [22, 12]).total_moon_width()
```

```hint
Print `total` after it grows, inside the loop. Does it ever hold more than
one moon's width at a time? What happens to it at the start of each
repeat?
```

```solution
class Planet:
    def __init__(self, name, moons):
        self.name = name
        self.moons = moons

    def total_moon_width(self):
        total = 0    # fixed: set once, before the loop
        for width in self.moons:
            total = total + width
        return total

jupiter = Planet("Jupiter", [3643, 3122, 5268, 4821])
print(jupiter.total_moon_width())
---
16854. With `total = 0` inside the loop, every repeat started counting
from nothing, so only the last moon was left: 4821. The loop did exactly
what it was told.
```

</div>

<div class="dl-world" data-world="your-own">

Can you add a `print()` to one method of your class, showing its fields
at the moment the method runs? Call the method two or three times. Does
every field change the way you expected?

```python exec
id: printing-what-you-need-to-see-2--your-own
# My class, with a print inside one method.
```

</div>

## What the editor already knows

The page you are reading is a small *development environment*: the set of
tools around your code. It gives you an editor to write in, a way to run
the code and see what happened, and the tracebacks that help you learn
why it broke. The editor does more than hold your code. Let's try two
things it can do.

1. Click at the end of the comment in the cell below, and press Enter.
2. Start typing `gra`. What appears before you finish the word?
3. Press Tab, or click `grace` in the list, to finish the word.
4. Now rest the mouse pointer over a name that is already on the page,
   such as `Character` in a cell above. What does the editor show you?

```python exec
id: what-the-editor-already-knows-1
# type here
```

A short list of names appears as you type, with `grace` among them, if you
have run a cell above that makes her. This is called *autocomplete*: the
editor offers to finish a name for you. When you rest the pointer over
`Character`, the editor shows its docstring or its shape, so you do not
have to scroll back to find it. (A docstring is a short description
written at the top of a class or function.)

Neither of those needed you to search for anything. The editor already knew,
because it reads the same code you do. That is what an *integrated
development environment* adds to a plain text file. It pays attention to
what you are writing, and it helps.

## Where a bigger project lives

A page like this one holds one script, and it does not remember your work
between visits. A real project grows past that. It has several files,
with a class in one file used from another, and work you want to find
again next week. The Notebook, at `compose/notebook.html`, has the same
editor and the same Python as this page, and it is made for that.

Three parts of the Notebook help most.

- **Files** is a real set of files and folders. Write `shapes.py` there,
  and a cell elsewhere can `import shapes`. Real Python programs are
  spread across several files in the same way.
- **Variables**, in the Workbench, lists every name in your current
  session, with its type and a short summary of its value. It updates
  each time you run a cell. It answers the question "did that work?"
  without you having to print everything a second time.
- **Stop** is a button next to each cell. A runaway cell is one stuck in
  a loop that never ends. Press **Stop**, and the cell stops at once. You
  do not have to wait for it, or close the tab.

## Looking back

The traceback at the top of this page named three lines, and the mistake
was on the last one. In the second cell, the error named the same three
lines, and the mistake was one line further up. When a traceback names
several lines, how will you decide which one to change?

A challenge: this probe has fuel for three photos, at 1 kg each. It has
two bugs. One stops with an error, and one does not. Can you find both,
and make it report 3 photos and 0 kg left?

```python challenge
class Probe:
    def __init__(self, name, fuel):
        self.name = name
        self.fuel = fuel
        self.photos = []

    def photograph(self, target):
        if self.fuel > 0:
            self.photos.append(target)
            self.burn(1)

    def burn(self, kg):
        fuel = max(0, self.fuel - kg)

    def report(self):
        return f"{self.name}: {len(self.photo)} photos, {self.fuel} kg left"

voyager = Probe("Voyager", 3)
for target in ["Jupiter", "Io", "Europa", "Saturn", "Titan"]:
    voyager.photograph(target)
print(voyager.report())
```

Next, [Encapsulation: keeping an object's data behind its methods](tutorial:keeping-details-inside-an-object)
puts the rules about an object's data in one place, where every caller
meets them.

## Where to read more

Everything here is covered elsewhere too, often in a form that will suit you
better than this one.

Downey, A. B. (2015). *Think Python: How to Think Like a Computer
Scientist* (2nd ed.). Green Tea Press. Free at
<https://greenteapress.com/wp/think-python-2e/>. Appendix A, "Debugging",
sorts bugs into three kinds, and has advice for each, including what to
do when you are stuck.

Python Software Foundation. *The Python Tutorial*, section 8, "Errors and
Exceptions". <https://docs.python.org/3/tutorial/errors.html>. How Python
reports an error, and the names of the errors you will meet most often.
