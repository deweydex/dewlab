---
title: "A program of your own"
year: "2026-2027"
version: 2026.09.26.1
covers:
  choosing-what-to-build:
    covers: [PDP-LO7]
  planning-before-you-code:
    covers: [PDP-LO6]
  release-1:
    covers: [PDP-LO7]
---

# A program of your own

Here is a whole program. Before you run it, what do you think the second
line of its output will be?

```python exec
id: a-whole-program-1
def encode(message, shift):
    coded = ""
    for character in message:
        if character.isupper():
            position = ord(character) - ord("A")
            coded = coded + chr((position + shift) % 26 + ord("A"))
        else:
            coded = coded + character
    return coded

secret = encode("MEET ME AT NOON", 3)
print(secret)
print(encode(secret, -3))
```

It codes a message, and then decodes it again, by shifting back the other
way. It is fourteen lines long, and it uses nothing from after
[Writing your own functions](tutorial:writing-your-own-functions). That is
enough to count as a program: something goes in, something is done to it,
and something useful comes out.

This page is not like the others. It has no tasks to check and no
solutions to open. It asks you to build a small program of your own, over
a week or two, and to release a first version of it. Everything from the
pages before this one is yours to use, and so is anything you look up.

## Choosing what to build

Choose something with a *low floor*: a first version you could finish in
an evening. And choose something with *room to grow*: a next step, and a
step after that, each one small. Here are three starting points.

**A cipher tool.** The first version codes and decodes one message with a
Caesar shift, like the program above. Room to grow:

- a key of your own, kept in a dictionary, in place of a shift;
- small letters, spaces and punctuation handled on purpose;
- cracking a shift with no key, by counting letters;
- a keyword cipher, where each letter has its own shift, taken from a
  word the two spies share.

**A pixel-art maker.** The first version draws one picture from a list of
strings, with `#` and `.`. Room to grow:

- a palette dictionary, with more characters and more colours;
- functions that change a picture: mirror it, turn it upside down, make
  its negative;
- a function that makes a picture twice as big, each pixel becoming a
  2 × 2 square;
- a picture made by a rule, such as a checkerboard, a border or a circle.

**Something of your own.** A tool for a thing you do by hand, a small quiz
or game, a program that answers a question you have. Two questions decide
whether it is the right size:

- Can you say, in one sentence, what its first version will do?
- Does that first version need only what you have met, or can look up in
  an afternoon?

Some ideas go wrong in the same ways, whoever tries them: anything that
needs a login, or somebody else's service, or a library you have not used
yet. The interesting part of those is hard to reach, and the first version
never arrives.

## Planning before you code

Before you write any Python, write the plan, the way
[Algorithms, pseudocode and your first Python](tutorial:first-steps) did:
one line of plain English for each step. Then name the functions the
program needs, and for each one, write what goes in and what comes out.
`encode` above takes a message and a shift, and gives back the coded
message. Deciding that first is what lets you write it, and try it, on
its own.

```python exec
id: planning-before-you-code-1
# My program:
# What its first version does, in one sentence:
#
# The plan, one step per line:
#
# The functions it needs, and what goes in and comes out of each:
#
```

For a program longer than a few cells, the Notebook is a better home. This
starter opens there, ready for your plan and your first function:

```python challenge
# Name:
# Version 1, and the date:
# What it does, in one sentence:


# For each function: what goes in, and what comes out.
```

## Release 1

A *release* is a version of your program that somebody else could use on
the day it comes out, however little it does. A plan is not a release, and
neither is most of a program. Release 1 is the smallest thing that does
anything at all. It should feel almost too small to show anyone.

**Before you call it Release 1, check that:**

- [ ] it runs from the top, on a freshly loaded page, with no errors;
- [ ] it does one thing a person could use, however small;
- [ ] a comment at the top gives its name, a version number and the date;
- [ ] each function's name says what it does, and a comment under its
  `def` line says what goes in and what comes out;
- [ ] you have tried it on at least three inputs whose answers you knew
  already, and one of them was at an edge: an empty message, a picture
  one pixel wide;
- [ ] somebody else has run it, before you explained anything, and you
  watched where they got stuck;
- [ ] you have kept a copy of it before you change it for Release 2. On
  this page, **Export a copy**, in the Notes panel, does that.

The last one matters more than it looks. Release 2 will break something
that Release 1 did, and a copy is how you find out what changed.

## Looking back

These questions have no answers to open. Write yours in **Your notes**, in
the **Notes** panel at the top right of the page, where they are saved with
the page.

- What did you plan that you did not build? What did you build that you
  had not planned?
- Where did you get stuck, and what got you moving again: a hint, an
  earlier page, a person, or a break?
- Which part of your program would you most like somebody to read? Which
  part would you least like them to?
- When somebody else ran it, what did they do that you did not expect?
- What would Release 2 add, and what is the smallest version of that?

The next page, [Searching a list: linear and binary search](tutorial:finding-things),
looks at a question every program meets sooner or later: how to find one
thing among many, and how long it takes.

## Where to read more

Downey, A. B. (2015). *Think Python: How to Think Like a Computer Scientist*
(2nd ed.). Green Tea Press. Free at <https://greenteapress.com/wp/think-python-2e/>.
Chapter 4 builds a small program one step at a time, and names the steps:
a plan, a first version, and a better one.

Singh, S. (1999). *The Code Book: The Secret History of Codes and
Codebreaking*. Fourth Estate. Chapters 1 and 2 are full of ciphers a
cipher tool could grow into, including the keyword cipher above.
