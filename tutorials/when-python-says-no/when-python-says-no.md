---
title: "When Python says no: reading error messages"
year: "2026-2027"
version: 2026.09.25.1
covers:
  the-last-line-first:
    covers: [PDP-LO9]
  a-move-from-another-space:
    covers: [PDP-LO9]
    touches: [PDP-LO4]
  following-the-trail-back:
    covers: [PDP-LO9]
    touches: [PDP-LO5]
  mistakes-python-finds-before-it-starts:
    covers: [PDP-LO9]
  compilers-linkers-and-python:
    covers: [PDP-LO9]
  which-question-is-the-error-asking:
    covers: [PDP-LO9]
---

# When Python says no: reading error messages

You press Run, and instead of an answer, red text appears under the
cell. For a moment it can feel like being told off, or like proof that
this was never for you. It is neither. It is Python
telling you, as exactly as it can, which move it could not make, and
where. Every programmer sees these messages every day, including the
ones who wrote Python.

This page is about reading them. Our code comes from the digit display
this unit is building: finding a number's digits, and a pixel's row and
column, with a mistake in each on purpose.

On this page we:

- read an error message from its last line up
- meet the five errors people see most often when they start
- follow an error back through two functions to the line responsible
- see how Python's messages compare with a compiler's and a linker's
- fix a broken piece of display code, one error at a time

> **The space we're in.** Python reads a whole cell before it runs any
> of it, to check that it is written in Python at all. Then it runs the
> lines from the top down. If a line asks for a move that is not allowed
> here, Python stops at that line and reports it. The lines above it
> have already run. Almost every cell on this page is meant to fail, so
> red text here means the page is working.

## Warm-up

Two questions from earlier pages.

```question
id: when-python-warm-up-1
type: fill-in-the-blank

On [Everything is ones and zeros](tutorial:everything-is-ones-and-zeros),
`pixel_row(5)` gives the string "{.#.#}".
```

```question
id: when-python-warm-up-2
type: multiple-choice
answer: 2

On [Numbers a computer can hold](tutorial:numbers-a-computer-can-hold),
what kind of number does Python give for `7 / 2`?

- an int
  - `7 // 2` gives an int, 3; one slash gives a float.
- a float
  - `/` gives a float, 3.5, even when the answer is whole.
- a string
  - Dividing two numbers gives a number; a string is text in quotes.
```

## The last line first

The cell below should find the ones digit of 2026, for the right-hand
digit of a display. It has a typing mistake in it, on purpose. Before
you run it, can you find the mistake? What do you think Python will say
about it?

```python exec
id: when-python-last-line-1
number = 2026
ones = numbr % 10
print(ones)
```

Python stops, and shows this report. A report like this is called a
*traceback*, because it traces back the steps that led to the problem.

<div class="dl-drawn dl-traceback">
<p class="dl-tb-edge">The top says a report is starting.</p>
<div class="dl-tb-body">
<div class="dl-tb-row"><code>Traceback (most recent call last):</code></div>
<div class="dl-tb-row"><code>  File "&lt;cell when-python-last-line-1&gt;", line 2, in &lt;module&gt;</code><span class="dl-tb-note">which cell, and which line</span></div>
<div class="dl-tb-row dl-tb-failed"><code>    ones = numbr % 10</code><span class="dl-tb-note">a copy of that line</span></div>
<div class="dl-tb-row dl-tb-failed"><code>           ^^^^^</code><span class="dl-tb-note">the part Python could not use</span></div>
<div class="dl-tb-row dl-tb-error"><code>NameError: name 'numbr' is not defined. Did you mean: 'number'?</code></div>
</div>
<p class="dl-tb-edge">The last line says what went wrong. Read it first.</p>
</div>

We read a traceback from the bottom up. The last line has three parts:

1. **The kind of error**, before the colon: `NameError`.
2. **What happened**, after the colon: the name `numbr` is not defined.
3. **Sometimes, a suggestion**: did you mean `number`?

Then the lines above say where: line 2 of this cell, with a copy of
the line and marks under the part Python could not use.

A *NameError* means Python met a name that points at nothing. Ask the
first of the four questions, *what is named here?* We named `number`
and `ones`. We never named `numbr`. To Python, `numbr` is not a
spelling mistake. It is a new word it has never been told about.

<aside class="dl-note" id="when-python-note-bug">

**The first bug.** Engineers called faults "bugs" long before
computers: Thomas Edison used the word in the 1870s. In 1947, the team
working on the Harvard Mark II computer found a real moth stuck in one
of its switches. They taped it into their logbook, under the words
"First actual case of bug being found." The page is now in the
Smithsonian's National Museum of American History.

</aside>

### Your turn

1. Fix the typing mistake in the cell above, and run it again. You should
   see `6`.
2. Now change `print` to `Print`, with a capital P, and run it.
3. Read the last line of the new message. What does Python suggest?
4. Change it back.

## A move from another space

On [Four questions for any puzzle](tutorial:four-questions), `*` did
one job with numbers and another with text. The same is true of `+`.
It adds two numbers, and it joins two strings. What do you think happens
when we ask it to join a string and a number? Run it to check.

```python exec
id: when-python-other-space-1
ones = 6
print("Ones digit: " + ones)
```

The last line says:

```text
TypeError: can only concatenate str (not "int") to str
```

A *TypeError* means a move was used on the wrong kind of value.
"Concatenate" is a long word for "join". `str` is Python's short name for
a string, so the message says: I can only join a string to a string, and
you gave me an int.

The move `+` is fine in the space of numbers, and fine in the space of
strings. It has no meaning between them. Python will not guess what we
wanted, so it asks us to choose. Here are two ways. `str()` turns a
number into a string, and `print` with a comma shows several things with
a space between them.

```python exec
id: when-python-other-space-2
ones = 6
print("Ones digit: " + str(ones))
print("Ones digit:", ones)
```

Here is a harder one, and I think it is the strangest message on this
page. Someone types 2026 into a box on a web page. Boxes give back
text, so `number` is the string `"2026"`, not the number. Before you
run it, what do you think Python will say?

```python exec
id: when-python-other-space-3
number = "2026"
print(number % 10)
```

The message is:

```text
TypeError: not all arguments converted during string formatting
```

That seems to have nothing to do with digits. Here is what happened.
With numbers, `%` gives a remainder. With text, `%` does a different
job: it is an old way of filling gaps in a piece of text, a little like
filling in a form. Python tried to put the 10 into a gap in `"2026"`,
found no gap, and said the 10 was "not converted". The same `%`, in a
different space, means a different move.

So when a message makes no sense, ask what kind of value each name
holds. Here, the words after the colon were about text, and that was
the clue: `number` was text.

### Your turn

1. `int()` turns text like `"2026"` into the whole number `2026`. In the
   cell above, change the first line to `number = int("2026")`.
2. Run it. You should see `6`. (`float()` does the same for text with a
   decimal point, like `"2.5"`.)

## Following the trail back

Sometimes the line that fails is not the line that is wrong. Here are
two small functions. `row_of` finds a pixel's row, as on
[Numbers a computer can hold](tutorial:numbers-a-computer-can-hold).
`show_position` uses it and prints the result. The last line asks about
a screen whose width was never set, so it is 0. This cell is meant to
fail.

```python exec
id: when-python-trail-1
def row_of(pixel, width):
    return pixel // width


def show_position(pixel, width):
    print("Pixel", pixel, "is in row", row_of(pixel, width))


show_position(37, 0)
```

The traceback now names three places:

```text
Traceback (most recent call last):
  File "<cell when-python-trail-1>", line 9, in <module>
    show_position(37, 0)
    ~~~~~~~~~~~~~^^^^^^^
  File "<cell when-python-trail-1>", line 6, in show_position
    print("Pixel", pixel, "is in row", row_of(pixel, width))
                                       ~~~~~~^^^^^^^^^^^^^^
  File "<cell when-python-trail-1>", line 2, in row_of
    return pixel // width
           ~~~~~~^^~~~~~~
ZeroDivisionError: integer division or modulo by zero
```

The last line names a *ZeroDivisionError*, which means the code tried
to divide by zero. "Integer division" is `//` on whole numbers, and
"modulo" is `%`: either one can fail this way. In mathematics, dividing
by zero has no answer in any of the number families we have met, and
Python follows the same rule.

Now read upwards. The words "most recent call last" tell us the order.
The places are listed in the order they happened, oldest first:

1. Line 9 of the cell called `show_position`, with a width of 0.
2. Inside `show_position`, line 6 called `row_of`.
3. Inside `row_of`, line 2 tried to divide, and stopped.

`in <module>` means the main part of the cell, outside any function.

Which line should we fix? Line 2 is where Python stopped, but
`pixel // width` is a perfectly good line. The 0 came from line 9. So
the line that *failed* and the line that is *responsible* can be far
apart, and the traceback is the trail between them. The most useful
line to look at first is often the lowest one that you wrote or changed
most recently.

### Your turn

Your toolkit has `digit_at` from
[Numbers a computer can hold](tutorial:numbers-a-computer-can-hold),
already loaded on this page. Its third input is the base.

1. Run the cell below as it is. The trail goes into your toolkit's own
   code.
2. Read the last line of the message. What kind of error is it?
3. Which line of *this* cell is responsible? Change the 0 to a base that
   makes sense, and run it again.

```python exec
id: when-python-trail-2
print(digit_at(2026, 1, 0))
```

## Mistakes Python finds before it starts

Every error so far happened while the cell was running. Some mistakes
Python finds earlier, while it reads the cell, before it runs a single
line. Before you run this one, do you think the first line will print?

```python exec
id: when-python-before-1
print("Starting the display")
digit = 7
print("Showing:", digit
```

Nothing is printed, not even the first line. The message is:

```text
  File "<cell when-python-before-1>", line 3
    print("Showing:", digit
         ^
SyntaxError: '(' was never closed
```

A *SyntaxError* means the code is not written in valid Python. *Syntax*
is the grammar of a language: which words and marks may go where. It is
like a sentence with a missing full stop. Python cannot run a cell it
cannot read, so it runs none of it.

Notice there is no "Traceback" line at the top. No line ran, so there
is nothing to trace back through. That is a quick way to tell the two
kinds apart.

Python also cares about the spaces at the start of a line. The lines
inside a function are pushed in, or *indented*, to show that they belong
to it. This cell is meant to fail.

```python exec
id: when-python-before-2
def ones_digit(number):
return number % 10
```

```text
IndentationError: expected an indented block after function definition on line 1
```

An *IndentationError* is a kind of SyntaxError about those spaces.
Python saw `def` on line 1, and expected the next line to be pushed in.

### Your turn

The cell below has one mistake that stops Python reading it.

1. Run it, and read the last line.
2. Look at where the `^` points, and fix the line.
3. Run it again. It should print `6`.

```python exec
id: when-python-before-3
def ones_digit(number)
    return number % 10


print(ones_digit(2026))
```

```hint
The last line says what Python expected. Where on the line does the
`^` point, and what is missing at that place?
```

## Compilers, linkers and Python

In many languages, such as C or C++, a program goes through two tools
before it runs.

A *compiler* reads the whole program first and translates it into
instructions the machine can follow. If the program breaks the
language's grammar, the compiler refuses, and nothing runs. A C compiler
might say something like this:

```text
display.c:6:5: error: expected ';' before 'return'
```

A *linker* runs next. It joins your program to other pieces of code it
uses, like a library of maths tools. If your program uses a name that
none of the pieces defines, the linker says so:

```text
undefined reference to `draw_digt'
```

Python does both jobs, as it goes. Before a cell runs, Python compiles
it, and a SyntaxError is Python's version of a compiler error. While the
cell runs, Python looks up each name at the moment it is used, and a
NameError is Python's version of a linker's "undefined reference". So
the skills are the same in every language:

| Look for | In Python | From a compiler or linker |
|---|---|---|
| the kind of error | `SyntaxError`, `NameError` | `error:`, `undefined reference` |
| where | `File "<cell …>", line 3` | `display.c:6:5` (file, line 6, column 5) |
| what happened | the words after the colon | the words after `error:` |

## Which question is the error asking?

Each error we met is one of the four questions, asked by Python.

| Error | What it means | The question to ask |
|---|---|---|
| `NameError` | a name points at nothing | What is named here? |
| `TypeError` | a move used on the wrong kind of value | What does this space let us do? |
| `ZeroDivisionError` | dividing by zero | What does this space let us do? |
| `SyntaxError`, `IndentationError` | not written in valid Python | What does this space let us do? Only valid Python can be read |

So when red text appears, there is a routine to follow:

1. Read the last line: the kind of error, and what happened.
2. Find the line it names, and look at the marks under it.
3. Ask which question the error is about.
4. Change one thing, and run again.

An error is a fact about one line, on one run. It says nothing about
whether you can learn to program. If you are stuck after the routine,
the Reference panel on this page has every error named here, and the
practice page has more to try.

### Your turn

This piece of display code finds the row and column of pixel 13 on a
screen 4 pixels wide. It has three mistakes. Python reports only one
at a time.

1. Run the cell, and fix the mistake the message names.
2. Run it again, and fix the next one.
3. Keep going until it prints `Row 3 column 1`.

Which mistake did Python report first? Why that one?

```python exec
id: when-python-routine-1
width = "4"
pixel = 13
row = pixel // width
column = pixel % width
print("Row", row, "column", colum
```

```hint
Which kind of error comes first: one Python finds while reading the
cell, or one it finds while running it?
```

```hint
after: 10 errors
title: some steps
1. The first message is a SyntaxError. Which bracket was never closed?
2. The next is a TypeError on line 3. What kind of value is `width`?
3. The last is a NameError. Which name did we define on line 4?

**Think about:** why a SyntaxError is always reported before the others.
```

<details class="dl-why"><summary>Why this way?</summary>

A whole page on error messages came in the first unit, before most of
the code in this course. Many courses leave errors until later, or deal
with each one when it happens.

Leaving them until later has a real reason. With little code there is
little to go wrong, and a beginner can spend the first weeks writing
things that work.

We put this page early because the red text comes anyway, usually on the
first day. If nobody has said what it is, it can look like a mark against
you. Read early, a traceback is Python answering one of the four
questions: which move is not allowed here, and where. A mistake becomes
information about one line.

</details>

## Four questions, looking back

| Question | On this page |
|---|---|
| What is named here? | `numbr` and `colum` were never named, so Python could not find them |
| What is promised? | a traceback promises the kind of error, what happened and where |
| What happens when? | Python reads the whole cell, then runs it line by line; a traceback lists calls oldest first |
| What does this space let us do? | `+` joins strings or adds numbers, not both at once; `%` finds a remainder, but on text it fills gaps; nothing divides by zero |

## What we have now

| Term | What it means |
|---|---|
| traceback | Python's report of an error; read it from the last line up |
| `NameError` | a name that points at nothing |
| `TypeError` | a move used on the wrong kind of value |
| `ZeroDivisionError` | a division by zero |
| `SyntaxError` | code that is not valid Python; nothing in the cell runs |
| `IndentationError` | the spaces at the start of a line are not what Python expected |
| `str()`, `int()`, `float()` | turn a number into text; turn text into a whole number, or into a float |
| compiler, linker | tools that check a program before it runs; Python does their jobs as it goes |
| failed and responsible | the line where Python stopped, and the line that caused it |

That is the end of Unit 1. Next is its practice page, and after it the
[mixed problems](tutorial:mixed-instructions-for-a-machine), which draw on
every page of the unit.

## Where to read more

The dewlab page [Reading an error message](tutorial:reading-an-error-message)
covers the same errors with other examples, and adds the errors that
give no message at all.

The Python documentation's list of built-in exceptions,
[docs.python.org/3/library/exceptions.html](https://docs.python.org/3/library/exceptions.html),
names every kind of error Python can report, with a sentence on each.
