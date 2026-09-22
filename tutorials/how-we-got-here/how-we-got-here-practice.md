---
title: "How We Got Here — Practice"
practice_for: how-we-got-here
year: "2026-2027"
version: 2026.08.23.1
---

# How We Got Here — Practice

On this page we practise reading binary, hexadecimal and ASCII, and we
look back at the history and the paradigms. Each answer is folded away
under its problem. Try the problem first, then open the answer.

Try the conversion questions by hand before you use the cell to check
them. The aim is that you can read the notation yourself, without Python
reading it for you.

## Tools

Run this cell before you start. It builds the same tools as the
tutorial, plus `to_hex`, which writes a number in hexadecimal.

```python exec
id: tools-1
def to_binary(n):
    if n == 0:
        return "0"
    digits = []
    while n > 0:
        digits.append(str(n % 2))
        n = n // 2
    return "".join(reversed(digits))


def from_binary(text):
    total = 0
    for character in text:
        total = total * 2 + int(character)
    return total


def to_hex(n):
    return format(n, "X")


print(to_binary(72), from_binary("01001000"), to_hex(72), chr(72))
```

## Reading the Notation

**1.** Change these binary numbers to base 10: `1010`, `11111111`,
`10000000`, `01000001`.

<details class="dl-answer"><summary>answer</summary>

10, 255, 128, 65.

255 is the largest number that eight bits can hold. That is why so many
limits in computing are 255. And 65 is the ASCII code for a capital A.

</details>

**2.** Change these to binary: 5, 16, 100, 200.

<details class="dl-answer"><summary>answer</summary>

101, 10000, 1100100, 11001000.

</details>

**3.** Change these to hex: 15, 16, 255, 4096.

<details class="dl-answer"><summary>answer</summary>

F, 10, FF, 1000.

Notice that 16 in hex is `10`. This is for the same reason that ten in
decimal is `10`: you have run out of single digits, so you carry one to
the next place.

</details>

**4.** Change `FF`, `A0` and `7E` from hex to binary, without going
through base 10.

<details class="dl-answer"><summary>answer</summary>

`11111111`, `10100000`, `01111110`.

Each hex digit is exactly four binary digits, so you can change one
digit at a time: F is 1111, A is 1010, 7 is 0111, E is 1110.

This direct match is the whole reason hexadecimal exists.

</details>

**5.** Decode `01001000 01001001` as ASCII.

<details class="dl-answer"><summary>answer</summary>

The codes are 72 and 73, which are `H` and `I`. The message is "HI".

</details>

**6.** Decode the hex `43 4F 44 45` as ASCII.

<details class="dl-answer"><summary>answer</summary>

The codes are 67, 79, 68 and 69, which spell "CODE".

</details>

**7.** Why do computers use binary, and not base 10?

<details class="dl-answer"><summary>answer</summary>

Because a transistor works best with two states: on or off, high
voltage or low. Base 2 matches those two states exactly.

Base 10 would need each part to tell apart ten different voltage levels,
every time. That is harder to build and harder to keep stable, and it
gains nothing.

</details>

**8.** Why does hexadecimal exist, given that computers do not use it?

<details class="dl-answer"><summary>answer</summary>

It exists only for people. `11111111` and `11111011` are hard to tell
apart at a glance. `FF` and `FB` are easy.

One hex digit is exactly four binary digits, so changing between them
follows a fixed rule, and nothing is lost. Hexadecimal is binary written
shorter, for whoever has to read it.

</details>

## The History

**9.** What did Ada Lovelace do, and why is it significant that the machine was never built?

<details class="dl-answer"><summary>answer</summary>

She wrote a step-by-step method for the Analytical Engine to work out a
sequence of numbers, using loops and conditional branching. She wrote it
in notes added to a translation, and the notes ended up longer than the
paper itself.

The fact that the machine was never built is the point: **a program does
not need a working machine to exist.** A program is a list of exact
instructions. That is true whether or not anything can carry them out
yet.

</details>

**10.** Put these in order, and say what each one made easier: machine
code, high-level languages, assembly language.

<details class="dl-answer"><summary>answer</summary>

1. Machine code (1940s): binary patterns that the hardware runs
   directly. There is nothing between you and the circuits.
2. Assembly (1950s): short names like `ADD` and `MOV` in place of binary.
   An assembler turns them back into binary. This is the first time a
   program's job is to write another program.
3. High-level languages (1957 onwards): code that reads like English or
   maths. A compiler or an interpreter translates it, and it is no
   longer tied to one kind of machine.

Each step made things easier for people. The hardware never needed any
of them.

</details>

**11.** What was the problem with assembly that high-level languages solved?

<details class="dl-answer"><summary>answer</summary>

Assembly was tied to one kind of machine. Its instruction names matched
that machine's own instructions, so a program written for one computer
would not run on another. Every program had to be rewritten for each new
machine.

</details>

**12.** What is the difference between a compiler and an interpreter?

<details class="dl-answer"><summary>answer</summary>

A compiler translates the whole program into machine code before it
runs. The result is something the machine can run on its own. An
interpreter reads the program and runs it line by line, as it goes.

C is usually compiled. Python is usually interpreted, although, to be
exact, it first translates your code into bytecode and then interprets
that.

</details>

**13.** Why does a compiled program usually run faster? And why is an
interpreted program usually quicker to debug, that is, to find and fix
its mistakes?

<details class="dl-answer"><summary>answer</summary>

A compiled program has already been translated, so no time goes on
translating while it runs. Also, the compiler could see the whole
program at once, so it could make the whole program faster.

An interpreted program is translated while it runs, and that takes time.
But there is no compile step between writing a line and seeing what it
does. You change something and run it straight away, and when you are
looking for a bug, that is worth a great deal.

</details>

**14.** A bank processes all of the day's payments overnight, in one
large batch. Which language from the table would you expect to find
doing that job? Why?

<details class="dl-answer"><summary>answer</summary>

COBOL, and a surprising amount of this work still runs on COBOL. It was
built in 1959 for business data processing, and banks took it up early.
Code that works, and has been checked for forty years, is not something
anyone replaces without a very good reason.

This is a fact about the industry as much as about the language:
software lasts much longer than the reasons it was written.

</details>

## Paradigms

**15.** Which paradigm is each of these closest to? What told you?

- (a) `total = 0` then a loop adding to it
- (b) `reduce(lambda a, b: a + b, prices, 0)`
- (c) `cart.add(4.50)` then `cart.total()`
- (d) `[p * 2 for p in prices]`

<details class="dl-answer"><summary>answer</summary>

(a) Procedural: step-by-step instructions that change something as they
go.

(b) Functional: it describes the change to make, with no loop written
out, and no variable is updated.

(c) Object-oriented: the data and the operations on it are kept together,
and the object remembers its data between calls.

(d) A comprehension. Its style is declarative: you say what the result
is, and Python works out how to build it.

</details>

**16.** Which of these paradigms does Python support?

<details class="dl-answer"><summary>answer</summary>

All of them. That is unusual, and it is part of why Python is used for
teaching.

Most languages push you firmly towards one paradigm. Python lets you
choose. That is a freedom, and also a responsibility. A program that
mixes all four without a plan is harder to read than one that sticks to
one.

</details>

**17.** Is any of the four paradigms correct?

<details class="dl-answer"><summary>answer</summary>

No. They are habits of thought. Which one suits depends on the problem,
and on who else has to read the code.

- A procedural loop is clearer for a beginner.
- A functional version is clearer once you are used to it.
- An object-oriented design helps when there is data to keep track of
  between steps, and gets in the way when there is not.

</details>

**18.** Rewrite this in the procedural style:
`doubled = [n * 2 for n in numbers]`.

<details class="dl-answer"><summary>answer</summary>

```python
doubled = []
for n in numbers:
    doubled.append(n * 2)
```

This takes three lines in place of one, and does exactly the same thing.
Which one is better depends on who is reading it.

</details>

## Putting It Together

**19.** Write `crack_the_vault(groups)`. Each entry in `groups` is a
pair: the base (`"bin"` or `"hex"`), and the code. The function should
give back the decoded message.

<details class="dl-answer"><summary>answer</summary>

```python
def crack_the_vault(groups):
    letters = []
    for base, code in groups:
        number = from_binary(code) if base == "bin" else int(code, 16)
        letters.append(chr(number))
    return "".join(letters)
```

The line that sets `number` makes a choice in one line: use
`from_binary` if the base is `"bin"`, and `int(code, 16)` if not.
[Making Decisions](tutorial:making-decisions) explains choices like this.

The function is the two earlier decoders joined together, with a check
to decide which one applies. This shape is common, and worth noticing.
When two functions differ in only one step, they can usually become one
function, with an extra input that picks the step.

</details>

**20.** A file's first two bytes are `50 4B` in hex. What are they as
characters? What might that tell you about the file?

<details class="dl-answer"><summary>answer</summary>

They are 80 and 75, which are `P` and `K`.

`PK` marks the start of a ZIP file. The letters are the initials of Phil
Katz, who wrote the original ZIP format in 1989. Many file formats start
with a few fixed bytes like these, called a magic number. A lot of
software works out what kind of file it has by reading those bytes. It
does not trust the file's name or extension.

</details>
