---
title: "A program of your own"
year: "2026-2027"
version: 2026.10.09.2
worlds:
  secret-messages: Codes and hidden messages, the kind spies and puzzle-setters make.
  pixel-art: Pictures made of small squares, the way a screen draws them.
covers:
  choosing-what-to-build:
    covers: [PDP-LO7]
  planning-before-you-code:
    covers: [PDP-LO6]
  release-1:
    covers: [PDP-LO7]
---

# A program of your own

<div class="dl-world" data-world="secret-messages">

Here is a whole *program*{.term}. Before you run it, what do you think the second
line of its output will be?

```python exec
id: a-whole-program-1--secret-messages
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

```predict
type: choice

What will the second line be?

- MEET ME AT NOON
  - The second line shifts the coded message back by 3, the other way.
- PHHW PH DW QRRQ
  - This is the first line again. Does the second line use the same shift?
- SKKZ SK GZ TUUT
  - This shifts the coded message forward by 3 again. The second call uses -3.
```

It codes a message, and then decodes it again, by shifting back the other
way. It is twelve lines long, and it uses nothing from after
[Writing your own functions](tutorial:writing-your-own-functions). It has a
function, `encode`, that does the work. It has the data the function works
on, a message and a shift. And it has a few lines at the end that use the
function and show the result.

</div>

<div class="dl-world" data-world="pixel-art">

Here is a whole *program*{.term}. Before you run it, what do you think the
last row of the second picture will be?

```python exec
id: a-whole-program-1--pixel-art
def mirror(picture):
    mirrored = []
    for row in picture:
        flipped = ""
        for pixel in row:
            flipped = pixel + flipped
        mirrored.append(flipped)
    return mirrored

def show(picture):
    for row in picture:
        print(row)

letter = ["###..", "#.#..", "###..", "#...."]
mirrored = mirror(letter)
show(mirrored)
print()
show(mirror(mirrored))
```

```predict
type: choice

What will the last row of the second picture be?

- #....
  - The second picture is the mirror of a mirror. Where does each pixel end up?
- ....#
  - This is the last row of the first picture. Does the second picture mirror it again?
- .....
  - Mirroring moves pixels from one side to the other. Does it remove any?
```

It draws a picture, mirrors it, and then mirrors the mirrored picture, which
turns it back. It is sixteen lines long, and it uses only what the pages
before this one covered. It has two functions: `mirror` changes a picture, and `show` draws
one. It has the data they work on, a picture made of rows of text. And it
has a few lines at the end that use the functions.

</div>

A program that does a real job is made of pieces like these: functions that
each do one job, the data they work on, and a few lines that put them
together and show the result. That is enough to count as a program.
Something goes in, something is done to it, and something useful comes out.

This page is not like the others. It has no tasks to check and no
solutions to open. It asks you to build a small program of your own, over
a week or two, and to release a first version of it. Everything from the
pages before this one is yours to use, and so is anything you look up.

Under the title is a box called "Choose a world". This page offers two
worlds: Secret messages (codes and hidden messages) and Pixel art (pictures
made of small squares). The explanations are the same for everyone. Only the
example program and the first project follow your choice. You can change it
at any time.

## Choosing what to build

Choose something with a first version you could finish in an evening. And
choose something with *room to grow*: a next step, and a step after that,
each one small. Here are three starting points. The first follows the world
you chose.

<div class="dl-world" data-world="secret-messages">

**A cipher tool.** The first version codes and decodes one message with a
Caesar shift, like the program above. It has room to grow:

- a key of your own, kept in a *dictionary*{.term}, in place of a shift;
- small letters, spaces and punctuation handled on purpose;
- cracking a shift with no key, by counting letters;
- a keyword cipher, where each letter has its own shift, taken from a
  word the two spies share.

**A pixel-art maker.** If you would like pictures instead, the first
version draws one picture from a list of strings, with `#` and `.`. It can
grow with a mirror, a palette of more characters, and pictures made by a
rule.

</div>

<div class="dl-world" data-world="pixel-art">

**A pixel-art maker.** The first version draws one picture from a list of
strings, with `#` and `.`, like the program above. It has room to grow:

- a palette dictionary, with more characters and more colours;
- functions that change a picture: turn it upside down, make its
  negative;
- a function that makes a picture twice as big, each pixel becoming a
  2 × 2 square;
- a picture made by a rule, such as a checkerboard, a border or a circle.

**A cipher tool.** If you would like codes instead, the first version codes
and decodes one message with a Caesar shift. It can grow with a key of your
own, cracking a shift by counting letters, and a keyword cipher.

</div>

**Something of your own.** It could be a tool for a thing you do by hand,
a small quiz or game, or a program that answers a question you have. Two questions decide
whether it is the right size:

- Can you say, in one sentence, what its first version will do?
- Does that first version need only what you have met, or what you can
  look up in an afternoon?

Some ideas go wrong in the same ways, whoever tries them: anything that
needs a login, or somebody else's service, or a library you have not used
yet. The interesting part of those is hard to reach, and the first version
never arrives.

## Planning before you code

Before you write any Python, write the plan, the way
[Algorithms, pseudocode and your first Python](tutorial:first-steps) did:
one line of plain English for each step. Then name the functions the
program needs, and for each one, write what goes in and what comes out.

<div class="dl-world" data-world="secret-messages">

`encode` above takes a message and a shift, and returns the coded message.

</div>

<div class="dl-world" data-world="pixel-art">

`mirror` above takes a picture, and returns the mirrored picture.

</div>

If you decide what goes in and what comes out first, you can write the
function and try it on its own.

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

For a program longer than a few cells, the Notebook is a better place. This
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
- [ ] a *comment*{.term} at the top gives its name, a version number and the date;
- [ ] each function's name says what it does, and a comment under its
  `def` line says what goes in and what comes out;
- [ ] you have tried it on at least three inputs whose answers you knew
  already, and one of them was at an edge, such as an empty input or the smallest
  one there could be;
- [ ] somebody else has run it, before you explained anything, and you
  watched where they got stuck;
- [ ] you have kept a copy of it before you change it for Release 2. On
  this page, **Export a copy**, in the Notes panel, does that.

The last one matters more than it looks. Release 2 will break something
that Release 1 did, and with a copy, you can see what changed.

## Looking back

These questions have no answers to open. Write yours in **Your notes**, in
the **Notes** panel at the top right of the page, where they are saved with
the page.

- What did you plan that you did not build? What did you build that you
  had not planned?
- Where did you get stuck, and what helped you continue: a hint, an
  earlier page, a person, or a break?
- Which part of your program would you most like somebody to read? Which
  part would you least like them to?
- When somebody else ran it, what did they do that you did not expect?
- What would Release 2 add, and what is the smallest version of that?

The next page, [Searching a list: linear and binary search](tutorial:finding-things),
looks at a question every program meets at some point: how to find one
thing among many, and how long it takes.

## Where to read more

Downey, A. B. (2015). *Think Python: How to Think Like a Computer Scientist*
(2nd ed.). Green Tea Press. Free at <https://greenteapress.com/wp/think-python-2e/>.
Chapter 4 builds a small program one step at a time, and names the steps:
a plan, a first version, and a better one.

<div class="dl-world" data-world="secret-messages">

Singh, S. (1999). *The Code Book: The Secret History of Codes and
Codebreaking*. Fourth Estate. Chapters 1 and 2 are full of ciphers a
cipher tool could grow into, including the keyword cipher above.

</div>

<div class="dl-world" data-world="pixel-art">

Ben Eater. *The world's worst video card?*
<https://www.youtube.com/watch?v=l7rce6IQDWs>. He builds a screen that
draws pictures from numbers kept in memory. It shows what a pixel-art
maker is doing, one level down. The video is about 33 minutes long.

</div>

DevDuck (2020). *When is it Time to Move On from a Personal Project?*
<https://www.youtube.com/watch?v=4f3Ss5n7SRQ>. A developer talks about
losing the will to work on a project he started. He covers creative
blocks, burnout, and what to do about them. The video is about seven
minutes long.
