---
title: "From cells to a program"
year: "2026-2027"
version: 2026.09.26.1
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

It prints 3. `while True` would go round for ever, because `True` never
becomes `False`. `break` leaves the loop at once, from wherever it is, and
the program continues after the loop.

Every program on this site so far has lived in cells: run one, look at the
answer, change something, run it again. A program somebody else can use is
different. It runs from its first line to its last, asks the person using
it what to do, keeps going until they tell it to stop, and copes when they
type something unexpected. This page makes that step, and then shows how a
team builds such a program in three releases. The team project, two pages
on, assumes all of it.

## A loop that waits for quit

`input("Choose: ")` shows its prompt, waits for the person to type
something and press Enter, and returns what they typed, always as a
string. A cell on this page cannot wait for typing. So here the typing is
written in advance, in a list, and a small function takes the place of
`input()`. `.pop(0)` takes the first element out of a list and returns
it.

```python exec
id: a-loop-that-waits-for-quit-1
typed = ["1", "MEET ME", "2", "9"]

def ask(prompt):
    """Stand in for input(): give back the next typed answer."""
    answer = typed.pop(0)
    print(prompt + answer)
    return answer

while True:
    print("1: shout a message   2: count the messages   9: quit")
    choice = ask("Choose: ")
    if choice == "9":
        break
    elif choice == "1":
        message = ask("Message: ")
        print(message.upper() + "!")
    elif choice == "2":
        print("That was the only one.")
    else:
        print("There is no choice", choice)
print("Goodbye.")
```

Change `typed` and run it again: try a choice that is not on the menu. On
your own computer, the whole of `ask` becomes one line, `ask = input`, and
the same program waits for a real person.

The menu is a `while True` loop with one way out: the choice that says
quit. Everything else goes round again. Every program that talks to a
person uses that shape, from a cash machine to a game.

### Your turn

Can you add a choice `3`, which prints the message backwards? The typed
answers already try it.

```python exec
id: your-turn-1
typed = ["3", "NOON", "3", "OTTER", "9"]

def ask(prompt):
    answer = typed.pop(0)
    print(prompt + answer)
    return answer

while True:
    print("1: shout a message   9: quit")
    choice = ask("Choose: ")
    if choice == "9":
        break
    elif choice == "1":
        message = ask("Message: ")
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
typed = ["3", "NOON", "3", "OTTER", "9"]

def ask(prompt):
    answer = typed.pop(0)
    print(prompt + answer)
    return answer

while True:
    print("1: shout a message   3: backwards   9: quit")
    choice = ask("Choose: ")
    if choice == "9":
        break
    elif choice == "1":
        message = ask("Message: ")
        print(message.upper() + "!")
    elif choice == "3":
        message = ask("Message: ")
        print(message[::-1])
    else:
        print("There is no choice", choice)
print("Goodbye.")
---
NOON stays NOON, and OTTER becomes RETTO. The menu line needs changing
too, or nobody knows choice 3 is there.
```

## Asking until the answer makes sense

A person will type anything: `seven` where a number was wanted, 30 where
the most is 25, nothing at all. A program has to decide what to do with
it, and the kindest answer is usually to say what it wanted, and ask
again. `.isdigit()` is `True` when a string is all digits, so `int()` can
read it.

```python exec
id: asking-until-the-answer-makes-sense-1
typed = ["seven", "30", "7"]

def ask(prompt):
    answer = typed.pop(0)
    print(prompt + answer)
    return answer

def ask_shift():
    """Keep asking until the answer is a whole number from 1 to 25."""
    while True:
        text = ask("Shift, 1 to 25: ")
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

### Your turn

You can test the code that decides without any typing at all, if it is in
its own function. Can you write `first_valid(answers, low, high)`, which
returns the first answer in the list that is a whole number from `low`
to `high`, as a number, or `None` if there is none?

```python exec
id: your-turn-2
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
id: your-turn-2-tests
tests: your-turn-2
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
says no to a minus sign and to a point. Is that right for a shift? Yes.
For a temperature, it would not be. Keeping the deciding in its own
function is what lets a test check it with no person typing.
```

## One place to start: main()

A program in cells starts wherever you press Run. A program in a file
starts at its first line and runs to its last. The usual way to organise
one is a `main()` function that holds the top level, the steps a person
would describe, with every detail in a function of its own. The last lines
call it.

```python exec
id: one-place-to-start-main-1
typed = ["1", "HELLO", "3", "9"]

def ask(prompt):
    answer = typed.pop(0)
    print(prompt + answer)
    return answer

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
        text = ask("Shift, 1 to 25: ")
        if text.isdigit() and 1 <= int(text) <= 25:
            return int(text)
        print("Please type a whole number from 1 to 25.")

def main():
    """Code messages until the person chooses to quit."""
    while True:
        choice = ask("1: code a message   9: quit   Choose: ")
        if choice == "9":
            break
        if choice == "1":
            message = ask("Message: ").upper()
            shift = ask_shift()
            print(encode(message, shift))
    print("Goodbye.")

main()
```

When you read `main()`, you see what the program does, in a few lines,
without any of the arithmetic. In a file, the last line is usually written a
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
2. Copy your program into a file ending in `.py`, such as `codebreaker.py`.
   Replace `typed` and your `ask` function with `ask = input`.
3. Run it: Thonny's Run button, or `python codebreaker.py` in a terminal.
   Now `input()` waits for you.

Without installing anything, the [Notebook](../compose/notebook.html) runs
Python in the browser, and keeps files. It cannot wait for typing either,
so keep your `ask` there, and swap it for `input` when the program moves
to a computer.

To share the file, send it, or keep it on GitHub, the way the web-authoring
pages do. [Creating a GitHub account](tutorial:a-github-account) shows
how to make one. GitHub keeps every version you upload, and a release
needs that.

## Three releases of a small game

Here is a small game built the way a team would build it: three releases,
each one something a person could use. The game is *Codebreaker*: the
computer codes a word with a secret shift, and the player tries to read
it.

**Release 1: the smallest thing that is a game.** It has one round and
one word, written into the code. It asks once, and says whether the answer is right.

```python exec
id: three-releases-of-a-small-game-1
import random

typed = ["KITE"]

def ask(prompt):
    answer = typed.pop(0)
    print(prompt + answer)
    return answer

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
guess = ask("Your answer: ").upper()
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
id: three-releases-of-a-small-game-2
import random

typed = ["1", "otter", "1", "BADGER", "2", "9"]

def ask(prompt):
    answer = typed.pop(0)
    print(prompt + answer)
    return answer

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
    guess = ask("Your answer: ").upper()
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
        choice = ask("1: play   2: score   9: quit   Choose: ")
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

Each release was something a person could play on the day it came out.

## Templates for a team

Copy these into a shared document, or into a file beside your code, and
complete them. Each is short on purpose.

**An interface agreement**, written before anybody writes code, for each
place where one person's code calls another's:

```
Function:     play_round(word)
Written by:   ...
Called by:    main(), written by ...
Takes:        word, a string in capitals
Gives back:   True if the player read it, False if not
Prints:       the coded word, and whether the answer was right
```

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

```
Release 2, 14 November
- Added a menu, several rounds and a score.
- Guesses in small letters now count.
- Known problem: the same three words, in the same order.
```

## Looking back

What was the hardest part of this page to picture: a loop that only ends
when told to, a function standing in for a person typing, or a program
that starts at `main()`? What would you try, to make it clearer to
yourself?

A challenge: build Release 1 of a game of your own, in any world you
like, on the same shape: a loop, a way to quit, and an answer checked with
care.

```python challenge
typed = ["1", "9"]

def ask(prompt):
    answer = typed.pop(0)
    print(prompt + answer)
    return answer

def main():
    while True:
        choice = ask("1: play   9: quit   Choose: ")
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
