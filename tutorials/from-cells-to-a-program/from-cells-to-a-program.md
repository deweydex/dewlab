---
title: "From cells to a program"
year: "2026-2027"
version: 2026.10.09.2
worlds:
  secret-messages: Codes and hidden messages, the kind spies and puzzle-setters make.
  pixel-art: Pictures made of small squares, the way a screen draws them.
covers:
  a-loop-that-waits-for-quit:
    covers: [PDP-LO6]
  asking-until-the-answer-makes-sense:
    covers: [PDP-LO7]
  one-place-to-start-main:
    covers: [PDP-LO8, PDP-LO11]
  running-it-outside-the-page:
    covers: [PDP-LO7]
  three-releases-of-a-small-game:
    covers: [PDP-LO12]
  templates-for-a-team:
    covers: [PDP-LO12]
---

# From cells to a program

What does this cell print?

```python exec
id: a-loop-that-stops-itself-1
count = 0
while True:
    count = count + 1
    if count == 3:
        break
print(count)
```

```predict
type: number

What will it print?
```

It prints 3. `while True` would repeat forever, because `True` never
becomes `False`. `break` leaves the loop at once, from wherever it is, and
the program continues after the loop.

Every program on this site so far has lived in cells: run one, look at the
answer, change something, run it again. A program somebody else can use is
different. It runs from its first line to its last, asks the person using
it what to do, keeps going until they tell it to stop, and handles
something unexpected that they type. This page makes that step, and then shows how a
team builds such a program in three releases. The team project, two pages
on, assumes all of it.

Under the title is a box called "Choose a world". This page offers two
worlds: Secret messages (codes and hidden messages) and Pixel art
(pictures made of small squares). The explanations are the same for
everyone. Only the example program, a small game, follows your choice. You
can change it at any time, and your work in each world is saved separately.

## A loop that waits for quit

`input("Choose: ")` shows its prompt, waits for the person to type
something and press Enter, and returns what they typed, always as a
string. When a cell on this page calls `input()`, a box appears after the
prompt. Type your answer in the box, then press Enter.

Run this cell, and try each choice. What happens when you type a choice
that is not on the menu?

```python exec
id: a-loop-that-waits-for-quit-1
count = 0

while True:
    print("1: shout a message   2: count the messages   9: quit")
    choice = input("Choose: ")
    if choice == "9":
        break
    elif choice == "1":
        message = input("Message: ")
        print(message.upper() + "!")
        count = count + 1
    elif choice == "2":
        print("Messages so far:", count)
    else:
        print("There is no choice", choice)
print("Goodbye.")
```

The program keeps asking until you choose `9`. While it waits, the cell's
**Run** button becomes **Stop**: press it to leave without choosing 9. This is
the same program you would run on your own computer, and there it waits
for you in the same way.

The menu is a `while True` loop with one way out: the choice that says
quit. Everything else goes round again. Every program that talks to a
person uses that shape, from a cash machine to a game.

### Your turn

Can you add a choice `3`, which prints the message backwards? Try it
with `NOON`, and then with `OTTER`.

```python exec
id: your-turn-1
while True:
    print("1: shout a message   9: quit")
    choice = input("Choose: ")
    if choice == "9":
        break
    elif choice == "1":
        message = input("Message: ")
        print(message.upper() + "!")
    else:
        print("There is no choice", choice)
print("Goodbye.")
```

```hint
Another `elif`, before the `else`. It asks for the message the same way
choice 1 does. A slice with a step of -1, `[::-1]`, gives a string
backwards.
```

```solution
while True:
    print("1: shout a message   3: backwards   9: quit")
    choice = input("Choose: ")
    if choice == "9":
        break
    elif choice == "1":
        message = input("Message: ")
        print(message.upper() + "!")
    elif choice == "3":
        message = input("Message: ")
        print(message[::-1])
    else:
        print("There is no choice", choice)
print("Goodbye.")
---
NOON stays NOON, and OTTER becomes RETTO. The menu line needs changing
too, or nobody knows choice 3 is there.
```

```typed
3
NOON
3
OTTER
9
```

## Asking until the answer makes sense

A person will type anything: `seven` where a number was wanted, a number
that is too big, nothing at all. A program has to decide what to do with
it, and the kindest answer is usually to say what it wanted, and ask
again. `.isdigit()` is `True` when a string is all digits, so `int()` can
read it.

<div class="dl-world" data-world="secret-messages">

Run this cell, and type `seven` first, then `30`, then `7`. The cell asks
for the shift of a code, a whole number from 1 to 25.

```python exec
id: asking-until-the-answer-makes-sense-1--secret-messages
def ask_shift():
    """Keep asking until the answer is a whole number from 1 to 25."""
    while True:
        text = input("Shift, 1 to 25: ")
        if text.isdigit() and 1 <= int(text) <= 25:
            return int(text)
        print("Please type a whole number from 1 to 25.")

print("Shift:", ask_shift())
```

`return` inside the loop ends the function, and the loop with it, as
soon as the answer makes sense. The `and` matters too. `int(text)` only
runs when `text.isdigit()` is `True`, so `int("seven")` never runs. This
is the short-circuit from
[Making decisions with if, elif and else](tutorial:making-decisions).

</div>

<div class="dl-world" data-world="pixel-art">

Run this cell, and type `seven` first, then `6`, then `3`. The cell asks
for the number of rows of a picture to show, a whole number from 1 to 5.

```python exec
id: asking-until-the-answer-makes-sense-1--pixel-art
def ask_rows():
    """Keep asking until the answer is a whole number from 1 to 5."""
    while True:
        text = input("Rows to show, 1 to 5: ")
        if text.isdigit() and 1 <= int(text) <= 5:
            return int(text)
        print("Please type a whole number from 1 to 5.")

print("Rows:", ask_rows())
```

`return` inside the loop ends the function, and the loop with it, as
soon as the answer makes sense. The `and` matters too. `int(text)` only
runs when `text.isdigit()` is `True`, so `int("seven")` never runs. This
is the short-circuit from
[Making decisions with if, elif and else](tutorial:making-decisions).

</div>

### Your turn

You can test the code that decides without any typing at all, if it is in
its own function. Can you write `first_valid(answers, low, high)`, which
returns the first answer in the list that is a whole number from `low`
to `high`, as a number, or `None` if there is none?

<div class="dl-world" data-world="secret-messages">

```python exec
id: your-turn-2--secret-messages
def first_valid(answers, low, high):
    return None
```

```inputs
guess: yes
first_valid(["seven", "30", "7"], 1, 25)
first_valid(["0", "1"], 1, 25)
first_valid(["-3", "7.5"], 1, 25)
first_valid([], 1, 25)
```

```python exec
id: your-turn-2-tests--secret-messages
tests: your-turn-2--secret-messages
assert first_valid(["25"], 1, 25) == 25
```

```solution
def first_valid(answers, low, high):
    """The first answer that is a whole number from low to high, or None."""
    for text in answers:
        if text.isdigit() and low <= int(text) <= high:
            return int(text)
    return None
---
`"-3"` and `"7.5"` are not all digits, so neither counts: `.isdigit()`
says no to a minus sign and to a point. That suits a shift. For a
temperature, a minus sign would have to count. Keeping the deciding in its own
function is what lets a test check it with no person typing.
```

</div>

<div class="dl-world" data-world="pixel-art">

```python exec
id: your-turn-2--pixel-art
def first_valid(answers, low, high):
    return None
```

```inputs
guess: yes
first_valid(["big", "9", "3"], 1, 5)
first_valid(["0", "1"], 1, 5)
first_valid(["-3", "2.5"], 1, 5)
first_valid([], 1, 5)
```

```python exec
id: your-turn-2-tests--pixel-art
tests: your-turn-2--pixel-art
assert first_valid(["5"], 1, 5) == 5
```

```solution
def first_valid(answers, low, high):
    """The first answer that is a whole number from low to high, or None."""
    for text in answers:
        if text.isdigit() and low <= int(text) <= high:
            return int(text)
    return None
---
`"-3"` and `"2.5"` are not all digits, so neither counts: `.isdigit()`
says no to a minus sign and to a point. That suits a number of rows. For a
temperature, a minus sign would have to count. Keeping the deciding in its own
function is what lets a test check it with no person typing.
```

</div>

## One place to start: main()

A program in cells starts wherever you press Run. A program in a file
starts at its first line and runs to its last. The usual way to organise
one is a `main()` function that holds the top level, the steps a person
would describe, with every detail in a function of its own. The last lines
call it.

<div class="dl-world" data-world="secret-messages">

```python exec
id: one-place-to-start-main-1--secret-messages
def encode(message, shift):
    """Give back message with each capital moved shift places along."""
    coded = ""
    for character in message:
        if character.isupper():
            position = ord(character) - ord("A")
            coded = coded + chr((position + shift) % 26 + ord("A"))
        else:
            coded = coded + character
    return coded

def ask_shift():
    """Keep asking until the answer is a whole number from 1 to 25."""
    while True:
        text = input("Shift, 1 to 25: ")
        if text.isdigit() and 1 <= int(text) <= 25:
            return int(text)
        print("Please type a whole number from 1 to 25.")

def main():
    """Code messages until the person chooses to quit."""
    while True:
        choice = input("1: code a message   9: quit   Choose: ")
        if choice == "9":
            break
        if choice == "1":
            message = input("Message: ").upper()
            shift = ask_shift()
            print(encode(message, shift))
    print("Goodbye.")

main()
```

</div>

<div class="dl-world" data-world="pixel-art">

```python exec
id: one-place-to-start-main-1--pixel-art
SPRITES = {
    "HEART": [".#.#.", "#####", "#####", ".###.", "..#.."],
    "TREE": ["..#..", ".###.", "#####", "..#..", "..#.."],
    "FLAG": ["####.", "#####", "#....", "#....", "#...."],
}

def top_part(rows, count):
    """Give back the first count rows of a picture, as one block of text."""
    return "\n".join(rows[:count])

def ask_rows():
    """Keep asking until the answer is a whole number from 1 to 5."""
    while True:
        text = input("Rows to show, 1 to 5: ")
        if text.isdigit() and 1 <= int(text) <= 5:
            return int(text)
        print("Please type a whole number from 1 to 5.")

def main():
    """Show the top of a sprite until the person chooses to quit."""
    while True:
        choice = input("1: show a sprite   9: quit   Choose: ")
        if choice == "9":
            break
        if choice == "1":
            name = input("Sprite (HEART, TREE or FLAG): ").upper()
            if name in SPRITES:
                print(top_part(SPRITES[name], ask_rows()))
            else:
                print("There is no sprite", name)
    print("Goodbye.")

main()
```

</div>

When you read `main()`, you see what the program does, in a few lines,
without any of the detail. In a file, the last line is usually written a
little differently:

```python
if __name__ == "__main__":
    main()
```

`__name__` is `"__main__"` when the file is run as a program, and
something else when another program borrows its functions with `import`.
So the file can be both: a program to run, and a toolkit to borrow from,
without the menu starting uninvited. A cell on this page is neither, which
is why the cell above calls `main()` plainly.

## Running it outside the page

A program meant for somebody else lives in a file. To run one on your own
computer:

1. Install Python from <https://www.python.org/downloads/>, or install
   Thonny, <https://thonny.org>, which comes with Python and a simple
   editor, and suits a first program well.
2. Copy your program into a file ending in `.py`, such as `game.py`.
3. Run it: Thonny's Run button, or `python codebreaker.py` in a terminal.
   `input()` waits for you there, as it did on this page.

Without installing anything, the [Notebook](../compose/notebook.html) runs
Python in the browser, and keeps files. `input()` waits for typing there
too.

To share the file, send it, or keep it on GitHub, the way the web-authoring
pages do. [Creating a GitHub account](tutorial:a-github-account) shows
how to make one. GitHub keeps every version you upload, and a release
needs that.

## Three releases of a small game

Here is a small game built the way a team would build it: three releases,
each one something a person could use.

<div class="dl-world" data-world="secret-messages">

The game is *Codebreaker*: the computer codes a word with a secret shift,
and the player tries to read it.

**Release 1: the smallest thing that is a game.** It has one round and
one word, written into the code. It asks once, and says whether the answer is right.

```python exec
id: three-releases-of-a-small-game-1--secret-messages
import random

def encode(message, shift):
    coded = ""
    for character in message:
        if character.isupper():
            position = ord(character) - ord("A")
            coded = coded + chr((position + shift) % 26 + ord("A"))
        else:
            coded = coded + character
    return coded

word = "OTTER"
shift = random.randint(1, 25)
print("Decode this:", encode(word, shift))
guess = input("Your answer: ").upper()
if guess == word:
    print("Yes!")
else:
    print("No: it was", word)
```

It is almost too small to show anyone, on purpose. It proves that the
three pieces work together: the code that encodes, the code that asks,
and the code that checks. Anything built later is
built on something that works.

**Release 2: the game, done properly.** It has a menu, several rounds, a
score, and answers checked with care. A guess is compared in capitals, so
`otter` counts.

```python exec
id: three-releases-of-a-small-game-2--secret-messages
import random

def encode(message, shift):
    coded = ""
    for character in message:
        if character.isupper():
            position = ord(character) - ord("A")
            coded = coded + chr((position + shift) % 26 + ord("A"))
        else:
            coded = coded + character
    return coded

def play_round(word):
    """Play one round with word. Give back True if the player read it."""
    shift = random.randint(1, 25)
    print("Decode this:", encode(word, shift))
    guess = input("Your answer: ").upper()
    if guess == word:
        print("Yes!")
        return True
    print("No: it was", word)
    return False

def main():
    words = ["OTTER", "HERON", "BADGER"]
    rounds = 0
    score = 0
    while True:
        choice = input("1: play   2: score   9: quit   Choose: ")
        if choice == "9":
            break
        elif choice == "1":
            word = words[rounds % len(words)]
            rounds = rounds + 1
            if play_round(word):
                score = score + 1
        elif choice == "2":
            print("You have read", score, "of", rounds)
        else:
            print("There is no choice", choice)
    print("Goodbye.")

main()
```

`words[rounds % len(words)]` takes the words in turn, and goes back to
the first after the last. This uses the remainder again, like the hours
on a clock.

**Release 3: finished, tidied, and tested.** Release 3 adds nothing
flashy. It adds what makes Release 2 safe to give to somebody else:

- a docstring on every function, saying what goes in and what comes out;
- tests for the parts that can be tested without typing, such as
  `assert encode("ABC", 1) == "BCD"` and
  `assert encode(encode("OTTER", 5), 21) == "OTTER"`;
- a word chosen at random from a longer list, with `random.choice(words)`;
- a change log, saying what each release changed.

</div>

<div class="dl-world" data-world="pixel-art">

The game is *Name the sprite*: the computer shows the top rows of a small
picture, a *sprite*, drawn with `#` for a filled square and `.` for an
empty one, and the player tries to name it.

**Release 1: the smallest thing that is a game.** It has one round and
one sprite, written into the code. It asks once, and says whether the answer is right.

```python exec
id: three-releases-of-a-small-game-1--pixel-art
import random

def top_part(rows, count):
    return "\n".join(rows[:count])

sprite = [".#.#.", "#####", "#####", ".###.", "..#.."]
name = "HEART"
rows_shown = random.randint(2, 4)
print("Name this sprite:")
print(top_part(sprite, rows_shown))
guess = input("Your answer: ").upper()
if guess == name:
    print("Yes!")
else:
    print("No: it was", name)
```

It is almost too small to show anyone, on purpose. It proves that the
three pieces work together: the code that draws, the code that asks,
and the code that checks. Anything built later is
built on something that works.

**Release 2: the game, done properly.** It has a menu, several rounds, a
score, and answers checked with care. A guess is compared in capitals, so
`heart` counts.

```python exec
id: three-releases-of-a-small-game-2--pixel-art
import random

SPRITES = {
    "HEART": [".#.#.", "#####", "#####", ".###.", "..#.."],
    "TREE": ["..#..", ".###.", "#####", "..#..", "..#.."],
    "FLAG": ["####.", "#####", "#....", "#....", "#...."],
}

def top_part(rows, count):
    return "\n".join(rows[:count])

def play_round(name):
    """Play one round with the sprite called name. Give back True if the player named it."""
    rows_shown = random.randint(2, 4)
    print("Name this sprite:")
    print(top_part(SPRITES[name], rows_shown))
    guess = input("Your answer: ").upper()
    if guess == name:
        print("Yes!")
        return True
    print("No: it was", name)
    return False

def main():
    names = ["HEART", "TREE", "FLAG"]
    rounds = 0
    score = 0
    while True:
        choice = input("1: play   2: score   9: quit   Choose: ")
        if choice == "9":
            break
        elif choice == "1":
            name = names[rounds % len(names)]
            rounds = rounds + 1
            if play_round(name):
                score = score + 1
        elif choice == "2":
            print("You have named", score, "of", rounds)
        else:
            print("There is no choice", choice)
    print("Goodbye.")

main()
```

`names[rounds % len(names)]` takes the sprites in turn, and goes back to
the first after the last. This uses the remainder again, like the hours
on a clock.

**Release 3: finished, tidied, and tested.** Release 3 adds nothing
flashy. It adds what makes Release 2 safe to give to somebody else:

- a docstring on every function, saying what goes in and what comes out;
- tests for the parts that can be tested without typing, such as
  `assert top_part(["#.", ".#", "##"], 2) == "#.\n.#"` and
  `assert top_part(["#."], 3) == "#."`;
- a sprite chosen at random from a longer list, with
  `random.choice(names)`;
- a change log, saying what each release changed.

</div>

Each release was something a person could play on the day it came out.

## Templates for a team

Copy these into a shared document, or into a file beside your code, and
write your own words in the gaps. Each is short on purpose.

**An interface agreement**, written before anybody writes code, for each
place where one person's code calls another's:

<div class="dl-world" data-world="secret-messages">

```
Function:     play_round(word)
Written by:   ...
Called by:    main(), written by ...
Takes:        word, a string in capitals
Gives back:   True if the player read it, False if not
Prints:       the coded word, and whether the answer was right
```

</div>

<div class="dl-world" data-world="pixel-art">

```
Function:     play_round(name)
Written by:   ...
Called by:    main(), written by ...
Takes:        name, a string in capitals, a key of SPRITES
Gives back:   True if the player named the sprite, False if not
Prints:       the top rows of the sprite, and whether the answer was right
```

</div>

**A team charter**, agreed in the first meeting:

```
Our project, in one sentence:
Who is building which piece:
When we meet, and where we talk between meetings:
How we decide when we disagree:
What we do when somebody is stuck: say so on the same day.
```

**A review checklist**, for reading each other's code before a release:

- [ ] Can I tell what each function does from its name and docstring?
- [ ] What does it do with an empty list, a zero, or a word where a number
  was expected?
- [ ] Have we written the same thing twice, in two places?
- [ ] Does every test still pass?

**A change log**, one entry for each release:

<div class="dl-world" data-world="secret-messages">

```
Release 2, 14 November
- Added a menu, several rounds and a score.
- Guesses in small letters now count.
- Known problem: the same three words, in the same order.
```

</div>

<div class="dl-world" data-world="pixel-art">

```
Release 2, 14 November
- Added a menu, several rounds and a score.
- Guesses in small letters now count.
- Known problem: the same three sprites, in the same order.
```

</div>

## Looking back

What was the hardest part of this page to picture: a loop that only ends
when told to, a question asked again until the answer makes sense, or a
program that starts at `main()`? What would you try, to make it clearer to
yourself?

A challenge: can you build Release 1 of a game of your own, in any world
you like? Use the same shape: a loop, a way to quit, and an answer checked
with care.

```python challenge
def main():
    while True:
        choice = input("1: play   9: quit   Choose: ")
        if choice == "9":
            break
        # Your game's one round goes here.
    print("Goodbye.")

main()
```

The next page, [Reviewing code and reflecting on your work](tutorial:critique-and-reflection),
turns to reading code: your own program, and somebody else's.

## Where to read more

Everything here is covered elsewhere too, often in a form that will suit you
better than this one.

Sweigart, A. (2019). *Automate the Boring Stuff with Python* (2nd ed.). No
Starch Press. Free at <https://automatetheboringstuff.com/>. Chapter 2 has
`while True`, `break` and `input()`, run on your own computer, and chapter
8 is about checking what a person types.

Python Software Foundation. *The Python Tutorial*, section 6.1.1,
"Executing modules as scripts".
<https://docs.python.org/3/tutorial/modules.html#executing-modules-as-scripts>.
This section explains what `if __name__ == "__main__":` is for, in the
official words.
