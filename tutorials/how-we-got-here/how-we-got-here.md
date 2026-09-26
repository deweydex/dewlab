---
title: "How programming languages came to be"
year: "2026-2027"
version: 2026.08.23.1
covers:
  before-there-were-computers:
    covers: [PDP-LO1]
  the-only-language-the-machine-understands:
    covers: [PDP-LO1]
    touches: [MIT-1.4]
  assembly-and-why-hexadecimal-exists:
    covers: [PDP-LO1]
    touches: [MIT-1.4]
  languages-people-can-read:
    covers: [PDP-LO1, PDP-LO3]
  the-same-problem-four-ways:
    covers: [PDP-LO3]
---

# How programming languages came to be

This is the last page of the series, so it is a good moment to look
back. You have written programs that store values, make decisions and
repeat steps. You have written your own functions, kept data in lists and
dictionaries, searched and sorted, and learned to read an error message.

Back in [Variables, data types and text](tutorial:storing-and-computing),
you also met binary and hexadecimal: two ways of writing numbers that
seemed to come from nowhere. Where did they come from? This page tells
that story.

It is also a short history of programming, the thing you have been
learning to do. Many parts of programming look like strange choices at first. Almost
every one of them was a decision somebody made for a reason, and the
reasons still hold today.

We will travel forwards in time:

1. a program written before there was a machine to run it
2. the patterns of on and off that early computers read
3. the languages we use now

At each stop, someone has left a message written in the notation of that
time. The only way to read each message is to write the code that
translates it.

## Before There Were Computers

By 1843, Charles Babbage had designed a machine called the Analytical
Engine. It was mechanical, made of gears and cards, with no electricity.
It was never finished in his lifetime.

**Ada Lovelace** was translating a paper about the machine into English.
The paper was by an Italian engineer, Luigi Menabrea, and it was written
in French. Lovelace added notes of her own. One of them described, step
by step, how the Engine could work out a sequence of numbers, using loops
and conditional branching. (Conditional branching means choosing which
step to do next, depending on a result, as `if` and `else` do in
Python.) Her notes were longer than the
paper she was translating.

Most historians say this makes her the first computer programmer. She
wrote her program more than a century before there was an electronic
computer to run it.

What can we take from this? It is an idea, and not a fact to memorise:
**a program does not need a working machine, or electricity, to exist.**
A program is a list of exact instructions. The rest of this page is about
how those instructions get carried out. It turns out to be a story about
making instructions easier for people to write, again and again, for a
hundred and eighty years.

## The Only Language the Machine Understands

ENIAC, built in 1945, had no programming language at all. To program it,
engineers rewired it by hand: they moved cables between boards and set
switches. A few years later, people built machines that could read their
instructions from memory. That was a huge step forward, but the
instructions were still only patterns of on and off.

*Machine code* is the computer's own language: instructions the hardware
runs directly, with nothing in between. In machine code every
instruction, every number and every letter is written in binary, base 2.

Why binary? It is not a question of style. A transistor, or a vacuum
tube in ENIAC's time, works best with two states: on or off, high
voltage or low. Base 2 matches those two states exactly. Base 10, which
we use because we have ten fingers, does not. (ENIAC itself still counted
in base 10, with a ring of ten on-off circuits for each digit. The machines that
came after it moved to binary, because two states are simpler to build
and more reliable.)

The cell below builds two tools that we will need: `to_binary` and
`from_binary`. You met these ideas in
[Variables, data types and text](tutorial:storing-and-computing). Here they
are as functions you can use.

You know almost everything in this cell already: `def`, `return`, `if`,
`while`, `for` and a list. One line is new. In `to_binary`,
`reversed(digits)` puts the digits in the opposite order, because the
loop finds the last digit first. Then `"".join(...)` joins them into one
string. Run the cell, and after that you can use `to_binary` and `from_binary` the same
way you use `print()`.

```python exec
id: the-only-language-the-machine-understands-1
def to_binary(n):
    """Convert a whole number to a binary string, with no '0b' in front."""
    if n == 0:
        return "0"
    digits = []
    while n > 0:
        digits.append(str(n % 2))
        n = n // 2
    return "".join(reversed(digits))


def from_binary(text):
    """Convert a binary string back to a whole number."""
    total = 0
    for character in text:
        total = total * 2 + int(character)
    return total


print(to_binary(72))
print(from_binary("01001000"))
```

How does `from_binary` work? It moves along the string, one digit at a
time. At each digit, it doubles the total so far, then adds the new
digit. You do the same thing in base 10 without thinking about it, with
ten in place of two.

### Your turn

Imagine that an operator from the 1940s has left a message. It is
written in *ASCII*, a standard code that gives each character a number.
(The message is made up: ASCII came later, in 1963.) Each group of eight
binary digits is the code for one letter. For example, `01001000` is 72,
and 72 is the code for `H`.

The function `chr()` turns a number into the character it stands for.
How might you write `decode_binary_message(groups)`? For each group:

1. Change the group into a number with `from_binary`.
2. Turn that number into a character with `chr`.
3. Join the characters together.

Then remove the `#` from the last line, and run the cell.

Before you write the loop, you can try one group on its own:
`chr(from_binary("01001000"))` gives `H`.

```python exec
id: your-turn-1
message_1945 = [
    "01001000",
    "01000101",
    "01001100",
    "01001100",
    "01001111",
]

def decode_binary_message(groups):
    # Your code here.
    pass


# print(decode_binary_message(message_1945))
```

## Assembly, and Why Hexadecimal Exists

Writing binary by hand is tiring, and it is very easy to make mistakes.
`01001000` and `01001100` differ in only one digit, and you have to count
to find it. People found two answers to this problem, and both were
about making life easier for people. The machines did not need either of
them.

*Assembly language* gives each machine instruction a short name that a
person can read, such as `ADD`, `MOV` or `JMP`, in place of a binary
pattern. An *assembler* is a program that turns those names back into
the binary the hardware needs. This is the first time in our story that
a program's job is to write another program.

Hexadecimal, base 16, became the usual short way to write binary. It
works because one hex digit is exactly four binary digits: `1111` is
`F`, `1010` is `A`, and any eight-digit binary byte is exactly two hex
characters. (Some early machines used octal, base 8, for the same job.
Hexadecimal became the standard in the 1960s, along with the eight-digit
byte.)

That is the whole reason hexadecimal exists. It is binary, written
shorter, for the person reading it. It is not a separate number system
with ideas of its own.

What do you think `hex_to_binary("48")` will print? Run the cell to
check.

```python exec
id: assembly-and-why-hexadecimal-exists-1
def to_hex(n):
    """Convert a whole number to an uppercase hex string, with no '0x' in front."""
    return format(n, "X")


def hex_to_binary(text):
    """Convert a hex string to a binary string, going through base 10."""
    return to_binary(int(text, 16))


print(to_hex(255))
print(hex_to_binary("FF"))
print(hex_to_binary("48"))
```

Now compare that last line with the first group of the message in the
previous section. The message had `01001000`, and the cell printed
`1001000`. Where did the first zero go?

It was never part of the number. `to_binary` writes only the digits the
number needs, the same way nobody writes 72 as 072. The message used
groups of eight digits so that every letter took the same space, and
`H` needed only seven, so it got a zero in front. `48` in hex, `1001000`
and `01001000` are the same number, written three ways. All of them are
the letter `H`.

### Your turn

Here is a memory dump from 1958, and this time it is in hex. (A memory
dump is a copy of what was stored in a computer's memory.)

1. Change each group into a number with `int(group, 16)`.
2. Turn each number into a character with `chr`.
3. Join the characters together, and remove the `#` from the last line
   to print the result.

```python exec
id: your-turn-2
memory_dump_1958 = ["43", "4F", "44", "45"]

def decode_hex_message(groups):
    # Your code here.
    pass


# print(decode_hex_message(memory_dump_1958))
```

## Languages People Can Read

Assembly was still tied to one kind of machine. Its instruction names
matched that machine's own instructions, so a program written for one
computer would not run on another. Nobody enjoyed rewriting every program
for every new machine.

The next step was the *high-level language*. A high-level language is a
way of writing code that reads more like English or maths. Software
translates it into machine code, so a person does not have to.

| Year | Language | What it was for |
|---|---|---|
| 1957 | FORTRAN | Scientific and engineering calculation |
| 1959 | COBOL | Business data processing |
| 1958–1960 | LISP | Symbolic and mathematical reasoning, and the ancestor of functional programming |
| 1972 | C | Systems programming, close to the hardware |
| 1991 | Python | General purpose, readable, and what you are writing now |

There are two ways to turn a high-level language into something a
machine can run. The difference between them shapes how it feels to work
in the language.

A *compiler* translates the whole program into machine code *before* it
runs. The result is a file that the machine can run on its own. C works
this way.

An *interpreter* reads the program and runs it line by line, *as it
goes*, with no separate translation step. Python works this way. To be
exact, Python first translates your code into an in-between form called
bytecode, and then interprets that. So it is a mix of the two. But from
where you sit, it behaves like an interpreted language.

Here is a question to think about before you read on. A compiled program
usually runs faster than an interpreted one. An interpreted language is
usually quicker to test and fix while you are writing it. Both facts come
from the difference above. **Can you see how each one follows from it?**

## The Same Problem, Four Ways

A *paradigm* is a way of organising a program. It is a set of habits
about where the logic goes and what the pieces are. Most languages
encourage one paradigm. Some, including Python, let you use several.

All four pieces of code below do the same thing: they double every
number in a list. The first one uses only a loop and a list, like the
ones you have written. The other three use some Python this series has
not taught: `map` and `lambda`, a `class`, and a list comprehension. So
do not worry about every word. Run the cell, then compare the four.
What is different about each one?

```python exec
id: the-same-problem-four-ways-1
numbers = [1, 2, 3, 4, 5]

# Procedural: step-by-step instructions that change something as they go.
doubled_procedural = []
for n in numbers:
    doubled_procedural.append(n * 2)
print("Procedural:", doubled_procedural)

# Functional: describe the transformation, not the loop that applies it.
doubled_functional = list(map(lambda n: n * 2, numbers))
print("Functional:", doubled_functional)


# Object-oriented: keep the data and the things you do to it together.
class NumberList:
    def __init__(self, values):
        self.values = values

    def doubled(self):
        return [v * 2 for v in self.values]


print("Object-oriented:", NumberList(numbers).doubled())

# Comprehension: compact and declarative, and very common in Python.
doubled_scripting = [n * 2 for n in numbers]
print("Comprehension:", doubled_scripting)
```

- The procedural version says *how* to build the answer, step by step.
- The functional version says *what* the answer is.
- The object-oriented version says *what kind of thing* has the answer.
- The comprehension says the same as the functional version, in fewer
  characters.

None of them is right and the others wrong. They are habits of thought.
Which one suits depends on the problem, and on who else has to read your
code.

### Your turn

Here are three snippets, and each one adds up a shopping basket. For each
one:

1. Which paradigm is it closest to?
2. What exact feature of the code told you? This is the part that
   matters most.

Fill in the blanks in the comments.

```python exec
id: your-turn-3
# Snippet 1
total = 0
for price in [4.50, 2.20, 7.00]:
    total = total + price
print(total)
# This is ___________ because ___________


# Snippet 2
from functools import reduce
total = reduce(lambda running, price: running + price, [4.50, 2.20, 7.00], 0)
print(total)
# This is ___________ because ___________


# Snippet 3
class ShoppingCart:
    def __init__(self):
        self.items = []

    def add(self, price):
        self.items.append(price)

    def total(self):
        return sum(self.items)


cart = ShoppingCart()
cart.add(4.50)
cart.add(2.20)
cart.add(7.00)
print(cart.total())
# This is ___________ because ___________
```

## The Vault

Here is one last message, and this one mixes both notations. Each entry
is a pair: the base it is written in, and the code.

You have already written the logic for this twice. This time, the two
go into one function, with a check to decide which one applies to each
pair.

```python exec
id: your-turn-4
vault_message = [
    ("hex", "54"), ("hex", "48"), ("hex", "45"),
    ("bin", "00100000"),
    ("hex", "46"), ("hex", "49"), ("hex", "52"), ("hex", "53"), ("hex", "54"),
    ("bin", "00100000"),
    ("hex", "50"), ("hex", "52"), ("hex", "4F"), ("hex", "47"), ("hex", "52"),
    ("hex", "41"), ("hex", "4D"), ("hex", "4D"), ("hex", "45"), ("hex", "52"),
]

def crack_the_vault(groups):
    # For each (base, code) pair:
    #   "bin" converts with from_binary
    #   "hex" converts with int(code, 16)
    # Then chr() the result, and join everything together.
    pass


# print(crack_the_vault(vault_message))
```

When your function is ready, remove the `#` from the last line and run
the cell. If your answer is right, the message describes somebody from
the first section of this page.

## Reflection

You have travelled a long way on this page:

- from a program written on paper in 1843
- through the on-and-off patterns that a 1945 machine read
- past the short notation invented so that people could bear to read
  those patterns
- into languages that let you say what you mean
- and out into four different views of how a program should be
  organised

Two ideas run through all of it.

**Every step was about making things easier for people.** The hardware
never needed assembly, or hexadecimal, or Python. It needs binary, and it
always has. Everything above binary exists because a person had to
write it, read it, or fix it at three in the morning.

**Notation is a tool with a purpose.** Hexadecimal is a choice made to
help people read, and not a fact about computers. Knowing why that
choice was made is more useful than knowing the conversion table.

Which step on this page do you think made the biggest difference to what
a person could build? Why? You could answer in a few sentences.

## Where to Read More

Computerphile (2016). *Computer Science's Wonder Woman: Ada Lovelace.*
<https://www.youtube.com/watch?v=wnHHzBY1SPQ>. The fuller story of the
translator's note that got longer than the paper it was translating.

Ben Eater. *Build an 8-Bit Computer.* <https://eater.net/8bit>. Everything
this page only describes — machine code, binary, and an instruction set —
built by hand, one logic gate at a time, on video.
