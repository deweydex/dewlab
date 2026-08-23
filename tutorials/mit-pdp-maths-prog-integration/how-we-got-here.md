---
title: "How We Got Here"
slug: how-we-got-here
module: mit-pdp-maths-prog-integration
module_title: "Programming and Maths, Integrated"
year: "2026-2027"
series: maths-and-programming
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

# How We Got Here

**Programming Design Principles / Maths for IT**

Last time you taught a computer to store things, and near the end of it you met binary and hexadecimal -- two ways of writing numbers that seemed to come out of nowhere. This tutorial is where they came from.

It is also a short history of the thing you are learning to do. Not because history is decorative, but because almost everything that seems arbitrary about programming turns out to be a decision somebody made for a reason, and the reasons are still there.

We will travel forwards: from a program written before there was a machine to run it, through the raw patterns of on and off that early computers consumed, to the languages you are using now. At each stop there is a message left behind in the notation of its era, and the only way to read it is to write the code that translates it.

## Before There Were Computers

In 1843, Charles Babbage had designed a machine called the Analytical Engine. It was mechanical -- gears and cards, no electricity -- and it was never finished in his lifetime.

**Ada Lovelace** was translating an Italian paper about the machine into English. She added notes of her own, and one of them described, step by step, how the Engine could be made to compute a sequence of numbers, using loops and conditional branching. It was longer than the paper she was translating.

By most historians' account that makes her the first computer programmer, more than a century before there was an electronic computer to run her program on.

There is an idea worth taking from this, and it is not a fact to memorise. **A program does not need a working machine, or electricity, to exist.** It is a sequence of precise instructions. Everything in the rest of this tutorial is about how those instructions get carried out -- which turns out to be a story about making them easier for people to write, over and over again, for a hundred and eighty years.

## The Only Language the Machine Understands

ENIAC, in 1945, had no programming language at all. To program it, engineers physically rewired it -- moving cables between plugboards and setting switches by hand. A few years later machines were built that could read their instructions from memory instead. That was an enormous step, and the instructions were still just patterns of on and off.

This is **machine code**: the raw, native language of the hardware, with nothing standing between it and the circuits. Every instruction, every number, every letter, all of it written in **binary** -- base 2.

Binary is not a stylistic choice. A transistor, or a vacuum tube in ENIAC's day, is naturally a two-state device: on or off, high voltage or low. Base 2 maps onto that exactly. Base 10, which we use because we have ten fingers, does not.

Run the cell below to build the two tools you will need. You met these ideas in *Storing and Computing*; here they are as functions you can call.

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

Notice what `from_binary` is doing: it walks along the string, doubling what it has so far and adding the next digit. That is the same thing you do in base 10 without thinking about it, with ten instead of two.

### Your turn

An ENIAC operator has left a message, written as ASCII character codes in binary. Each group of eight digits is one letter's code -- `01001000` is 72, and 72 is `H`.

Write `decode_binary_message(groups)`. For each group, convert it to a number with `from_binary`, turn that number into a character with `chr`, and join the characters together.

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

Writing binary by hand is exhausting and very easy to get wrong. `01001000` and `01001100` differ in one digit, and you have to count to find it. Two things happened in response, and both of them are about people rather than about machines.

**Assembly language** gave each machine instruction a short readable name -- `ADD`, `MOV`, `JMP` -- instead of a binary pattern. A program called an **assembler** translated those names back into the binary the hardware needed. This is the first time in our story that a program's job is to write another program.

**Hexadecimal**, base 16, became the standard shorthand for writing binary. It works because one hex digit is exactly four binary digits: `1111` is `F`, `1010` is `A`, and any eight-digit binary byte is exactly two hex characters.

That is the whole reason hexadecimal exists. It is not a third number system with its own ideas; it is binary, written shorter, for the benefit of the person reading it.

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

Look at that last line beside the first message in the previous section. `48` in hex and `01001000` in binary are the same number, written two ways, and both of them are the letter `H`.

### Your turn

A memory dump from 1958, in hex this time. The idea is the same as before -- `int(group, 16)` converts a hex string to a number, and `chr` turns a number into a character.

```python exec
id: your-turn-2
memory_dump_1958 = ["43", "4F", "44", "45"]

def decode_hex_message(groups):
    # Your code here.
    pass


# print(decode_hex_message(memory_dump_1958))
```

## Languages People Can Read

Assembly was still tied to one particular machine. Its instruction names matched that machine's instruction set, so a program written for one computer would not run on another. Rewriting everything for each new machine was, unsurprisingly, unpopular.

The next step was the **high-level language**: code that reads more like English or mathematics, translated into machine code by software rather than by a person.

| Year | Language | What it was for |
|---|---|---|
| 1957 | FORTRAN | Scientific and engineering calculation |
| 1959 | COBOL | Business data processing |
| 1958--60 | LISP | Symbolic and mathematical reasoning, and the ancestor of functional programming |
| 1972 | C | Systems programming, close to the hardware |
| 1991 | Python | General purpose, readable, and what you are writing now |

There are two ways a high-level language becomes something a machine can run, and the difference between them shapes how it feels to work in.

A **compiler** translates the whole program into machine code *before* it runs, producing a file the machine can execute on its own. C works this way.

An **interpreter** reads and runs the program line by line *as it goes*, with no separate translation step. Python works this way -- strictly it compiles to an intermediate form called bytecode first and then interprets that, which is a hybrid, but from where you are sitting it behaves like an interpreted language.

Here is a question worth sitting down with before reading on. A compiled program usually runs faster than an interpreted one, and an interpreted language is usually quicker to test and debug while you are writing it. Both of those follow from the difference above. **How might each one follow from it?**

## The Same Problem, Four Ways

A **paradigm** is a way of organising a program -- a set of habits about where the logic goes and what the pieces are. Languages tend to encourage one, and some, Python among them, will let you use several.

The four below all do exactly the same thing: double every number in a list. Run the cell and read them against each other, because the differences are the point.

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

The procedural version says *how* to build the answer. The functional version says *what* the answer is. The object-oriented version says *what kind of thing* has an answer. The comprehension says the same as the functional one in fewer characters.

None of them is correct and the others wrong. They are habits of thought, and which one suits depends on the problem and on who else has to read your code.

### Your turn

Three snippets below, all adding up a shopping basket. For each one, say which paradigm it is closest to and -- this is the part that matters -- *what specific feature of the code told you*.

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

One last message, and this one mixes both notations. Each entry is a pair: the base it is written in, and the code.

You have written the logic for this twice already. This is the two of them in one function, with a check to decide which applies.

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

If it comes out right, it describes somebody from the first section of this tutorial.

## Reflection

You have travelled from a program written on paper in 1843, through the on-and-off patterns a 1945 machine consumed, past the shorthand invented so that people could stand to read them, into languages that let you say what you mean, and out into four different opinions about how a program should be organised.

Two threads run through all of it and are worth naming.

**Every step was about making things easier for people.** The hardware never needed assembly, or hexadecimal, or Python. It needs binary and it always has. Everything above binary exists because a person had to write it, read it, or fix it at three in the morning.

**Notation is a tool with a purpose.** Hexadecimal is not a fact about computers, it is a decision about legibility -- and knowing why it was made is more useful than knowing the conversion table.

Write a few sentences on this: which of the steps in this tutorial do you think made the biggest difference to what a person could build, and why?
