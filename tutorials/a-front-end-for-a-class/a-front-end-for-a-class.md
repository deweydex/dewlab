---
title: "A front end: letting someone use your classes"
year: "2026-2027"
version: 2026.09.26.1
worlds:
  game: A game world, with characters, the things they carry, and rooms.
  ocean: An ocean expedition, with a submarine, its crew, and what they find.
  solar-system: A solar system, with planets, moons and the probes sent to them.
  your-own: A world of your own, with a class you design and grow page by page.
covers:
  a-program-only-its-author-can-use:
    covers: [FOOP-LO11]
  deciding-kept-apart-from-asking:
    covers: [FOOP-LO11]
  a-loop-that-asks:
    covers: [FOOP-LO11]
  a-menu-to-choose-from:
    covers: [FOOP-LO11]
---

# A front end: letting someone use your classes

Here are the game world's classes, as they stood at the end of
[Documenting a class](tutorial:documenting-a-class). Run the cell. It
makes the classes, and prints nothing.

```python exec
id: the-game-so-far
{{include: setup/oop/game-7.py}}
```

## A program only its author can use

To play this game now, you would write Python: `grog.take_damage(3)`,
then `print(grog)`, then `ada.heal(2)`. A friend who has never written
Python could not play it at all. The classes work. The problem is that
using them means writing code.

A *front end* is the part of a program that lets somebody use it without
reading or writing any of its code. It asks them a plain question, turns
the answer into a method call, and shows what happened. On this page we
build two, for the same classes.

## Deciding, kept apart from asking

The front end has two jobs: asking what the player wants, and deciding
what that means. We write the deciding part first, as a function,
`run_choice`. It takes the command as text, and it never asks for it. So
we can try it with a list of commands, before anybody types anything.
What will the third line print?

```python exec
id: deciding-kept-apart-from-asking-1
def run_choice(hero, monster, choice):
    """Run one command. Return False when the game should stop."""
    if choice == "look":
        print(hero)
        print(monster)
    elif choice == "attack":
        monster.take_damage(3)
        if not monster.is_down():
            hero.take_damage(2)
        print(hero, "|", monster)
    elif choice == "rest":
        hero.heal(2)
        print(hero)
    elif choice == "quit":
        return False
    else:
        print("Not a command:", choice)
    return True

ada = Character("Ada", 10)
grog = Character("Grog", 8)
for choice in ["look", "attack", "attack", "rest", "dance", "quit"]:
    still_playing = run_choice(ada, grog, choice)
print("still playing:", still_playing)
```

```predict
What will the third line print?

- Ada (health 8) | Grog (health 5)
  - Grog takes 3, and hits back for 2.
- Ada (health 10) | Grog (health 5)
  - Only Grog is hurt by an attack.
- Grog (health 8)
  - The third line is still part of `look`.
```

It prints `Ada (health 8) | Grog (health 5)`. Each command in the list
runs one call: two attacks, a rest, and `dance`, which is not a command,
so `run_choice` says so and carries on. `quit` returns `False`: the one
answer that means "stop".

`run_choice` never calls `input()`. It acts on whatever `choice` it is
given, as a method acts on its arguments. That is what lets us test it
with a list, and it is what lets us give it a second front end later with
no change at all.

## A loop that asks

A real front end asks, in a loop, until the player quits. On a computer,
it would look like this:

```python
still_playing = True
while still_playing:
    choice = input("What now? ")
    still_playing = run_choice(ada, grog, choice)
print("Goodbye.")
```

A cell on this page cannot wait for someone to type, so here the typing
is written in advance, in a list, and a small `ask` stands in for
`input`, as on
[From cells to a program](tutorial:from-cells-to-a-program). On a
computer, `ask = input` is the only change.

```python exec
id: a-loop-that-asks-1
typed = ["look", "attack", "fly", "quit"]

def ask(prompt):
    answer = typed.pop(0)
    print(prompt + answer)
    return answer

ada = Character("Ada", 10)
grog = Character("Grog", 8)
still_playing = True
while still_playing:
    choice = ask("What now? ")
    still_playing = run_choice(ada, grog, choice)
print("Goodbye.")
```

A player will type things nobody planned for: `fly`, `Attack` with a
capital, an empty line. A front end has to expect that, because the
player has never seen `run_choice` and cannot fix it. Checking what a
person typed, before the program uses it, is called *input validation*.
Here the `else` does it: anything unknown is answered, and the loop goes
on. Try adding `"Attack"` to `typed`. What happens, and should it?

## A menu to choose from

A player may never see a prompt at all. This page has its own
*widgets*, the pieces a web page is built from: `dropdown` makes a menu
to choose from, and `text_input` a box to type in. Here is a second front
end for the same `run_choice`. The first cell starts a new game. The
second shows a menu: choose a command, then run the cell, and it plays
one turn. Choose again and run it again for the next.

```python exec
id: a-menu-to-choose-from-1
ada = Character("Ada", 10)
grog = Character("Grog", 8)
print("A new game: Ada against Grog.")
```

```python exec
id: a-menu-to-choose-from-2
command = dropdown("What now?", ["look", "attack", "rest", "quit"])
still_playing = run_choice(ada, grog, command.value)
```

This front end took two lines, because the deciding was already written,
and tested. Two front ends, one set of classes: the classes never knew
which one was asking.

A menu also changes what input validation has to do. Nobody can choose
`fly` from it, so that mistake cannot happen at all. A front end that
makes a mistake impossible is often kinder than one that catches it
afterwards, and `run_choice` still keeps its `else`, for the front ends
that let people type.

On a page like this one, the cell's own Run is the Go button. Python here
runs in the background, away from the page, so a button on the page
cannot call Python the moment it is pressed. A program running on your
own computer can have a button that does.

### Your turn: your class, eighth version

This is the eighth version of your world: a `run_choice` for your
classes, tested with a list of commands, and a menu for someone to play
with. Run the first cell in your world, which holds your
classes as they stood at the end of
[Documenting a class](tutorial:documenting-a-class).

<div class="dl-world" data-world="game">

```python exec
id: your-class-8-so-far--game
{{include: setup/oop/game-7.py}}
```

The party has a healer now. Can you write a `run_choice(hero, healer,
monster, choice)` with the commands `look`, `attack`, `heal` and `quit`,
where `heal` has the healer heal the hero by 2? Test it with the list,
then give it a menu.

```python exec
id: your-class-8--game
# Your run_choice here

ada = Character("Ada", 10)
mira = Healer("Mira", 10)
grog = Character("Grog", 8)
for choice in ["look", "attack", "heal", "sing", "quit"]:
    still_playing = run_choice(ada, mira, grog, choice)
print("still playing:", still_playing)
```

```hint
Start from this page's `run_choice`. What does the `heal` command need
that `rest` did not? Which of the healer's methods does it call?
```

```solution
def run_choice(hero, healer, monster, choice):
    """Run one command in the cave. Return False when the game should stop."""
    if choice == "look":
        print(hero, "|", healer, "|", monster)
    elif choice == "attack":
        monster.take_damage(3)
        if not monster.is_down():
            hero.take_damage(2)
        print(hero, "|", monster)
    elif choice == "heal":
        healer.heal_other(hero, 2)
        print(hero)
    elif choice == "quit":
        return False
    else:
        print("Not a command:", choice)
    return True

ada = Character("Ada", 10)
mira = Healer("Mira", 10)
grog = Character("Grog", 8)
for choice in ["look", "attack", "heal", "sing", "quit"]:
    still_playing = run_choice(ada, mira, grog, choice)
print("still playing:", still_playing)
---
The list prints a look, an attack, Ada healed back to 10, and `Not a
command: sing`, then `still playing: False`. The menu is the same two
lines as on this page, in a cell of its own, with Mira added:

    command = dropdown("What now?", ["look", "attack", "heal", "quit"])
    still_playing = run_choice(ada, mira, grog, command.value)
```

</div>

<div class="dl-world" data-world="ocean">

```python exec
id: your-class-8-so-far--ocean
{{include: setup/oop/ocean-7.py}}
```

Can you write a `run_choice(submarine, choice)` with the commands `dive`
and `rise` (50 m at a time), `depth` and `quit`? Test it with the list,
then give it a menu.

```python exec
id: your-class-8--ocean
# Your run_choice here

trieste = Bathyscaphe("Trieste")
for choice in ["dive", "dive", "depth", "rise", "swim", "quit"]:
    still_diving = run_choice(trieste, choice)
print("still diving:", still_diving)
```

```hint
Each command is one `elif`, and each calls one of the submarine's
methods. What should `run_choice` return for `quit`, and for everything
else?
```

```solution
def run_choice(submarine, choice):
    """Run one command for the submarine. Return False when the dive is over."""
    if choice == "dive":
        submarine.dive(50)
        print(submarine)
    elif choice == "rise":
        submarine.rise(50)
        print(submarine)
    elif choice == "depth":
        print(submarine, "with", submarine.room_below(), "m to spare")
    elif choice == "quit":
        return False
    else:
        print("Not a command:", choice)
    return True

trieste = Bathyscaphe("Trieste")
for choice in ["dive", "dive", "depth", "rise", "swim", "quit"]:
    still_diving = run_choice(trieste, choice)
print("still diving:", still_diving)
---
`Trieste at 50 m`, `at 100 m`, `with 10900 m to spare`, back to 50 m,
`Not a command: swim`, and `still diving: False`. The menu, in a cell of
its own:

    command = dropdown("Command", ["dive", "rise", "depth", "quit"])
    still_diving = run_choice(trieste, command.value)

The hull limit is kept by `dive`, not by the front end: choose `dive` and
run the cell enough times, and the bathyscaphe's own rule refuses.
```

</div>

<div class="dl-world" data-world="solar-system">

```python exec
id: your-class-8-so-far--solar-system
{{include: setup/oop/solar-system-7.py}}
```

Can you write a `run_choice(probe, choice)` with the commands `burn` (10
kg), `refuel` (20 kg), `status` and `quit`? Test it with the list, then
give it a menu.

```python exec
id: your-class-8--solar-system
# Your run_choice here

philae = Lander("Philae", 40)
for choice in ["burn", "status", "refuel", "orbit", "quit"]:
    still_flying = run_choice(philae, choice)
print("still flying:", still_flying)
```

```hint
Each command is one `elif`, and each calls one of the probe's methods.
What should `status` show, so that a player knows whether the next burn
will work?
```

```solution
def run_choice(probe, choice):
    """Run one command for the probe. Return False when the mission is over."""
    if choice == "burn":
        probe.burn(10)
        print(probe)
    elif choice == "refuel":
        probe.refuel(20)
        print(probe)
    elif choice == "status":
        print(probe, "| can burn 10 kg:", probe.can_burn(10))
    elif choice == "quit":
        return False
    else:
        print("Not a command:", choice)
    return True

philae = Lander("Philae", 40)
for choice in ["burn", "status", "refuel", "orbit", "quit"]:
    still_flying = run_choice(philae, choice)
print("still flying:", still_flying)
---
`Philae (fuel 30 kg)`, the status with `True`, 50 kg after refuelling,
`Not a command: orbit`, and `still flying: False`. The menu, in a cell of
its own:

    command = dropdown("Command", ["burn", "refuel", "status", "quit"])
    still_flying = run_choice(philae, command.value)

`status` asks `can_burn`, so after `philae.land()` it says `False`, and
the front end never needed to know about landers.
```

</div>

<div class="dl-world" data-world="your-own">

Copy your classes from [Documenting a class](tutorial:documenting-a-class)
into the first cell. Then write a `run_choice` for your world: three or
four commands, and `quit`. Test it with a list of commands, including one
that is not a command. Then give it a menu, in a cell of its own.

```python exec
id: your-class-8-so-far--your-own
# My classes so far
```

```python exec
id: your-class-8--your-own
# My run_choice, its test, and its menu
```

</div>

## Looking back

`run_choice` never asked for anything, so it could be tested with a list
and given a second front end with no change. Which other method in your
classes would be easier to test if it did one job fewer?

A challenge: players type `Attack`, ` attack ` and `ATTACK`, and mean
the same thing. Can you make the front end accept all three, without
changing `run_choice`? (Text has a method `.strip()`, which removes
spaces at the ends, and `.lower()`, which makes every letter small.)

```python challenge
def run_choice(choice):
    if choice == "attack":
        print("You swing at the troll.")
    elif choice == "look":
        print("A cave, and a troll.")
    elif choice == "quit":
        return False
    else:
        print("Not a command:", choice)
    return True

typed = ["Attack", " look ", "QUIT"]

def ask(prompt):
    answer = typed.pop(0)
    print(prompt + answer)
    return answer

still_playing = True
while still_playing:
    choice = ask("What now? ")
    still_playing = run_choice(choice)
print("Goodbye.")
```

Next, [Your world, playable](tutorial:your-world-playable) puts every
version of your class together, with its tests passing, for someone else
to play or explore.

## Where to read more

Everything here is covered elsewhere too, often in a form that will suit you
better than this one.

Sweigart, A. (2019). *Automate the Boring Stuff with Python* (2nd ed.).
No Starch Press. Free at <https://automatetheboringstuff.com/>. Chapter 8,
"Input Validation", on checking what a person types before a program
trusts it.

Python Software Foundation. *The Python Tutorial*, section 7.1, "Fancier
Output Formatting".
<https://docs.python.org/3/tutorial/inputoutput.html>. How a front end
can lay out what it shows, once plain `print()` is not enough.

CrashCourse (2017). *Keyboards & Command Line Interfaces: Crash Course
Computer Science #22.* <https://www.youtube.com/watch?v=4RPtJ9UyHS0>.
Before windows and a mouse, people used programs the way this page's menu
does: type something, read the answer. About eleven minutes.
