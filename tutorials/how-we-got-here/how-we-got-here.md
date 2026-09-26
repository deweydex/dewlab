---
title: "How programming languages came to be"
year: "2026-2027"
version: 2026.09.26.1
worlds:
  secret-messages: Codes and hidden messages, the kind spies and puzzle-setters make.
  pixel-art: Pictures made of small squares, the way a screen draws them.
covers:
  before-there-were-computers:
    covers: [PDP-LO1]
  the-only-language-the-machine-understands:
    covers: [PDP-LO1, MIT-1.4]
  assembly-and-why-hexadecimal-exists:
    covers: [PDP-LO1, MIT-1.4]
  languages-people-can-read:
    covers: [PDP-LO1, PDP-LO3]
  the-same-problem-four-ways:
    covers: [PDP-LO3]
---

# How programming languages came to be

Here is a number, written two ways. What will the cell print?

```python exec
id: one-number-two-ways-1
print(0b101010)
print(0b101010 == 42)
```

```predict
What will the first line print?

- 101010
  - It prints what is written after the 0b.
- 42
  - 0b means the digits are binary, and Python shows the number in base 10.
- An error
  - A number cannot start with 0b.
```

It prints 42, and then `True`. `0b101010` is *binary*, the way a computer
stores 42, and Python shows it the way people write it. Underneath every
program on every page so far, everything was patterns like that one.

This is the last page of the series, and it looks back: at a program
written before there was a machine to run it, at the on-and-off patterns
the first computers read, and at the languages that made those patterns
bearable. Almost every part of programming that looks like a strange
choice was a decision somebody made for a reason, and the reasons still
hold. At each step in the story, a message is left in the notation of its
time. To read it, you write the code that translates it.

## Before there were computers

By 1843, Charles Babbage had designed a machine called the Analytical
Engine. It was mechanical, made of gears and cards, with no electricity,
and it was never finished in his lifetime.

**Ada Lovelace** was translating a paper about the machine into English.
The paper was by an Italian engineer, Luigi Menabrea, and it was written
in French. Lovelace added notes of her own, and one of them described,
step by step, how the Engine could calculate a sequence of numbers, with
loops and with conditional branching. That means the Engine chooses its
next step from a result, as `if` and `else` do. Her notes were longer than the paper
she was translating.

Most historians call her the first computer programmer. She wrote her
program more than a century before there was an electronic computer to run
it. **A program does not need a working machine to exist.** It is a list of
exact instructions. The rest of this page is about how machines follow
those instructions. It is a story about how people made them easier to
write, again and again, for a hundred and eighty years.

## The only language the machine understands

ENIAC, built in 1945, had no programming language at all. Engineers
programmed it by moving cables between boards and setting switches. A few
years later, machines could read their instructions from memory, but the
instructions were still patterns of on and off. *Machine code* is the
computer's own language: instructions the hardware runs directly. In
machine code, every instruction, number and letter is written in binary.

We count in *base 10*, decimal, with ten digits, 0 to 9, probably because
we have ten fingers. Each position in a number is worth a power of 10, so
42 means 4 tens and 2 ones. *Binary* is base 2. It has two digits, 0 and
1, and each position is worth a power of 2: 1, 2, 4, 8, 16, 32, and so on.

    101010  =  1 × 32 + 0 × 16 + 1 × 8 + 0 × 4 + 1 × 2 + 0 × 1  =  42

Why binary? A transistor, or a vacuum tube in ENIAC's day, works best with
two states: on or off, high voltage or low. Base 2 matches those exactly.
(ENIAC itself still counted in base 10, with a ring of ten circuits for
each digit. The machines after it moved to binary, because two states are
simpler to build and more reliable.)

`bin()` writes a number in binary, and these two functions do the
conversions by hand. Before you run it, what will `to_binary(72)` print?

```python exec
id: the-only-language-the-machine-understands-1
print(bin(42))

def to_binary(n):
    """Give back n, a whole number, as a string of binary digits."""
    if n == 0:
        return "0"
    text = ""
    while n > 0:
        text = str(n % 2) + text
        n = n // 2
    return text

def from_binary(text):
    """Give back the whole number a string of binary digits stands for."""
    total = 0
    for digit in text:
        total = total * 2 + int(digit)
    return total

print(to_binary(72))
print(from_binary("01001000"))
```

`to_binary` finds the last digit first, `n % 2`, so it puts each new digit
at the front. `from_binary` goes the other way. At each digit, it doubles
the total so far and adds the new digit. You do the same in base 10
without thinking, with ten in place of two.

### Your turn

Try these by hand first, and write your working as comments. Then check
each one with the functions above.

1. What is binary `11001` in base 10?
2. How do you write 100 in binary?

```python exec
id: your-turn-1
# 1. Binary 11001 = ?
#    Working:

# 2. 100 in binary = ?
#    Working:

# Check:
```

<details class="dl-answer"><summary>answer</summary>

`11001` is 16 + 8 + 1 = 25. 100 is 64 + 32 + 4, which is `1100100`.

</details>

<div class="dl-world" data-world="secret-messages">

An operator from the 1940s has left a message, written in *ASCII*: a code
that gives each character a number. (The message is made up. ASCII came
later, in 1963.) Each group of eight binary digits is one letter's code:
`01001000` is 72, and 72 is `H`, which `chr(72)` gives. Can you write
`decode_binary(groups)`?

```python exec
id: your-turn-2--secret-messages
message_1945 = ["01001000", "01000101", "01001100", "01001100", "01001111"]

def decode_binary(groups):
    return ""
```

```inputs
guess: yes
decode_binary(message_1945)
decode_binary(["01001000", "01001001"])
decode_binary([])
```

```hint
For each group: `from_binary` turns it into a number, and `chr()` turns
the number into a character. Add each character to a string.
```

```solution
message_1945 = ["01001000", "01000101", "01001100", "01001100", "01001111"]

def from_binary(text):
    total = 0
    for digit in text:
        total = total * 2 + int(digit)
    return total

def decode_binary(groups):
    text = ""
    for group in groups:
        text = text + chr(from_binary(group))
    return text
---
HELLO. The groups are all eight digits long, so every letter takes the
same space, and the message can be cut into letters without a separator.
```

</div>

<div class="dl-world" data-world="pixel-art">

Early games kept their pictures as rows of binary digits, one bit for each
pixel: 1 lit, 0 dark. Can you write `draw_binary(rows)`, which returns
the picture as rows of `#` and `.`?

```python exec
id: your-turn-2--pixel-art
sprite = ["00011000", "00111100", "01111110", "11111111", "00011000", "00011000"]

def draw_binary(rows):
    return []

for line in draw_binary(sprite):
    print(line)
```

```inputs
guess: yes
draw_binary(["101", "010"])
draw_binary(sprite)
draw_binary([])
```

```hint
For each row, build a line: `#` for each `"1"`, and `.` for each `"0"`.
Append each line to a list, and give the list back.
```

```solution
sprite = ["00011000", "00111100", "01111110", "11111111", "00011000", "00011000"]

def draw_binary(rows):
    lines = []
    for row in rows:
        line = ""
        for bit in row:
            if bit == "1":
                line = line + "#"
            else:
                line = line + "."
        lines.append(line)
    return lines

for line in draw_binary(sprite):
    print(line)
---
A tree. Eight pixels a row, one bit each, is one byte a row: the whole
picture is six bytes, which mattered when a machine had a few thousand of
them.
```

</div>

## Assembly, and why hexadecimal exists

Binary is tiring to write by hand, and easy to get wrong. `01001000` and
`01001100` differ in one digit, and you have to count to find it. People
found two answers, and both were for people. The machines needed neither.

*Assembly language* gives each machine instruction a short name, such as
`ADD`, `MOV` or `JMP`, in place of a binary pattern. An *assembler* is a
program that turns those names back into binary. It is the first time in
this story that a program's job is to write another program.

*Hexadecimal*, base 16, became the usual short way to write binary. It
uses the digits 0 to 9 and then the letters A to F, for ten to fifteen.
One hex digit is exactly four binary digits: `1111` is `F`, and `1010` is
`A`. So an eight-digit byte is exactly two hex digits. (Some early machines
used base 8 for the same job. Hexadecimal became the standard in the
1960s, along with the eight-digit byte.) Hex exists only for this reason.
It is binary, written shorter, for the person reading it.

```python exec
id: assembly-and-why-hexadecimal-exists-1
print(hex(255))
print(0x48)
print(int("48", 16))
print(to_binary(int("48", 16)))
```

`hex()` writes a number in hex, with `0x` in front. `0x48` is a number
written in hex, and `int("48", 16)` reads hex from a string. The last line
prints `1001000`. The message above had `01001000`. The zero in front was
never part of the number, the way nobody writes 72 as 072. `48` in hex,
72, `1001000` and `01001000` are one number written four ways, and all of
them are H.

### Your turn

<div class="dl-world" data-world="secret-messages">

Here is a memory dump from 1958: a copy of what was in a computer's
memory, and this time it is in hex. Can you write `decode_hex(groups)`?

```python exec
id: your-turn-3--secret-messages
memory_dump_1958 = ["43", "4F", "44", "45"]

def decode_hex(groups):
    return ""
```

```inputs
guess: yes
decode_hex(memory_dump_1958)
decode_hex(["48", "49"])
```

```solution
memory_dump_1958 = ["43", "4F", "44", "45"]

def decode_hex(groups):
    text = ""
    for group in groups:
        text = text + chr(int(group, 16))
    return text
---
CODE. Two hex digits a letter, where binary took eight: the same bytes,
four times shorter to write.
```

Then there is the vault. Each entry is a pair, the base it is written in
and the code. You have written both halves already. Can you put them into one
function, with an `if` to choose between them?

```python exec
id: your-turn-4--secret-messages
vault = [
    ["hex", "54"], ["hex", "48"], ["hex", "45"], ["bin", "00100000"],
    ["hex", "46"], ["hex", "49"], ["hex", "52"], ["hex", "53"], ["hex", "54"],
    ["bin", "00100000"], ["hex", "50"], ["hex", "52"], ["hex", "4F"],
    ["hex", "47"], ["hex", "52"], ["hex", "41"], ["hex", "4D"], ["hex", "4D"],
    ["hex", "45"], ["hex", "52"],
]

def crack_the_vault(pairs):
    return ""
```

```inputs
guess: yes
crack_the_vault(vault)
crack_the_vault([["bin", "01001000"], ["hex", "49"]])
```

```hint
`for base, code in pairs:` takes each pair apart. If the base is `"bin"`,
use `from_binary`; if it is `"hex"`, use `int(code, 16)`. Then `chr()`.
```

```solution
vault = [
    ["hex", "54"], ["hex", "48"], ["hex", "45"], ["bin", "00100000"],
    ["hex", "46"], ["hex", "49"], ["hex", "52"], ["hex", "53"], ["hex", "54"],
    ["bin", "00100000"], ["hex", "50"], ["hex", "52"], ["hex", "4F"],
    ["hex", "47"], ["hex", "52"], ["hex", "41"], ["hex", "4D"], ["hex", "4D"],
    ["hex", "45"], ["hex", "52"],
]

def from_binary(text):
    total = 0
    for digit in text:
        total = total * 2 + int(digit)
    return total

def crack_the_vault(pairs):
    text = ""
    for base, code in pairs:
        if base == "bin":
            number = from_binary(code)
        else:
            number = int(code, 16)
        text = text + chr(number)
    return text
---
THE FIRST PROGRAMMER: somebody from the first section of this page. The
two binary entries are 32, the code for a space.
```

</div>

<div class="dl-world" data-world="pixel-art">

Games kept their sprites in hex, two hex digits for each row of eight
pixels. Can you write `draw_hex(rows)`, which returns the picture as
rows of `#` and `.`? Each row has to become eight binary digits, zeros in
front included.

```python exec
id: your-turn-3--pixel-art
invader = ["18", "3C", "7E", "DB", "FF", "24", "5A", "A5"]

def draw_hex(rows):
    return []

for line in draw_hex(invader):
    print(line)
```

```inputs
guess: yes
draw_hex(["FF", "81"])
draw_hex(invader)
```

```hint
`to_binary(int(row, 16))` gives the binary digits, without the zeros in
front. `"0" * (8 - len(bits)) + bits` puts them back. Then draw each bit,
as you did with binary.
```

```solution
invader = ["18", "3C", "7E", "DB", "FF", "24", "5A", "A5"]

def to_binary(n):
    if n == 0:
        return "0"
    text = ""
    while n > 0:
        text = str(n % 2) + text
        n = n // 2
    return text

def draw_hex(rows):
    lines = []
    for row in rows:
        bits = to_binary(int(row, 16))
        bits = "0" * (8 - len(bits)) + bits
        line = ""
        for bit in bits:
            if bit == "1":
                line = line + "#"
            else:
                line = line + "."
        lines.append(line)
    return lines

for line in draw_hex(invader):
    print(line)
---
An invader, eight bytes. Without the zeros in front, `"18"` would be
`11000`, five pixels wide, and the picture would lean to the left.
```

Web pages still write colours in hex: `#1E90FF` is two hex digits each
for red, green and blue. Can you write `rgb(colour)`, which returns the
three as numbers?

```python exec
id: your-turn-4--pixel-art
def rgb(colour):
    return [0, 0, 0]
```

```inputs
guess: yes
rgb("#1E90FF")
rgb("#FFD700")
rgb("#000000")
```

```hint
`colour[1:3]` is the red pair. Which slices are the green and the blue?
```

```solution
def rgb(colour):
    return [int(colour[1:3], 16), int(colour[3:5], 16), int(colour[5:7], 16)]
---
`[30, 144, 255]`, the blue called dodger blue, and `[255, 215, 0]`, gold.
Three bytes fit in six hex digits, with no doubt about where one ends.
```

</div>

## Languages people can read

Assembly was still tied to one kind of machine. Its instruction names
matched that machine's own, so a program for one computer would not run
on another. Nobody enjoyed rewriting every program for every new machine.

The next step was the *high-level language*: code that reads more like
English or mathematics, which software translates into machine code, so a
person does not have to.

| Year | Language | What it was for |
|---|---|---|
| 1957 | FORTRAN | Scientific and engineering calculation |
| 1959 | COBOL | Business data processing |
| 1958–1960 | LISP | Symbolic and mathematical reasoning, and the ancestor of functional programming |
| 1972 | C | Systems programming, close to the hardware |
| 1991 | Python | General purpose, readable, and what you are writing now |

There are two ways to turn a high-level language into something a machine
can run. A *compiler* translates the whole program into machine code
*before* it runs, into a file the machine can run on its own. C works this
way. An *interpreter* reads the program and runs it *while it reads*. Python
works this way. To be exact, Python first translates your code into an
in-between form called bytecode, and interprets that. But for you, it
behaves like an interpreted language.

A compiled program usually runs faster than an interpreted one, and an
interpreted language is usually quicker to try things in while you are
writing. **Can you see how each follows from the difference above?**

## The same problem, four ways

A *paradigm* is a way of organising a program. It is a set of habits
about where the logic goes and what the pieces are. Most languages encourage
one, and Python allows several. All four of these double every number in
a list. The last uses a `class`, which this series has not taught. You do
not need to write one, only to see what it keeps together.

```python exec
id: the-same-problem-four-ways-1
numbers = [1, 2, 3, 4, 5]

# Procedural: step-by-step instructions that change something as they go.
doubled = []
for n in numbers:
    doubled.append(n * 2)
print("Procedural:     ", doubled)

# Declarative: say what the answer is, not how to build it.
print("Comprehension:  ", [n * 2 for n in numbers])

# Functional: functions are values, and one can be handed to another.
def double(n):
    return n * 2

def apply_to_all(rule, values):
    return [rule(value) for value in values]

print("Functional:     ", apply_to_all(double, numbers))

# Object-oriented: keep the data, and what you do with it, together.
class NumberList:
    def __init__(self, values):
        self.values = values

    def doubled(self):
        return [value * 2 for value in self.values]

print("Object-oriented:", NumberList(numbers).doubled())
```

The procedural version says *how*, step by step. The comprehension says
*what*. The functional version treats `double` as a value, handed to
another function, as `sorted()` was handed a `key=`. And the
object-oriented version makes a new kind of thing, a `NumberList`, that
carries its values and knows how to double them. `self` is the particular
list being asked. None of them is right and the others wrong. They are
habits of thought, and which suits depends on the problem, and on who will
read the code. The object-oriented course builds classes properly.

For each of these, which paradigm is it closest to, and what told you?

```python exec
id: the-same-problem-four-ways-2
prices = [4.50, 2.20, 7.00]

# Snippet 1
total = 0
for price in prices:
    total = total + price
print(total)

# Snippet 2
print(sum(price for price in prices))

# Snippet 3
class Basket:
    def __init__(self):
        self.prices = []

    def add(self, price):
        self.prices.append(price)

    def total(self):
        return sum(self.prices)

basket = Basket()
basket.add(4.50)
basket.add(2.20)
basket.add(7.00)
print(basket.total())
```

<details class="dl-answer"><summary>one way to answer</summary>

1 is procedural: a running total, changed step by step. 2 is declarative:
it says the answer is the sum of the prices, and leaves the loop to
Python. 3 is object-oriented: the basket holds its prices, and adding to
it and totalling it are things the basket does. The clues matter most.
They are a changing variable, a description of the answer, and a thing
that carries its own data.

</details>

## Looking back

Two ideas run through this page. Every step, from assembly to Python,
made things easier for people. The hardware never needed any of them, and
it still needs binary, as it always has. And a notation is a tool with a
purpose. Hexadecimal is a choice made to help people read, not a fact
about computers. Which step do you think made the biggest difference to
what a person could build?

This is the end of the series. Here is something to make with all of it.
The first step is easy, and you can take it as far as you like.

<div class="dl-world" data-world="secret-messages">

**Break a classmate's cipher.** Each of you codes a paragraph of English,
a few sentences long, with a cipher of your own, and swaps it. Then write a
program that cracks the other's without the key. The first step is a
Caesar shift. You crack it by counting letters and guessing that the most
common is E. A harder step is a key where every letter can stand for any
other. You crack it by matching the order of frequencies to English's, E,
T, A, O, I, N, and you fix the rest by hand, one word at a time.

```python challenge
# Paste your classmate's coded paragraph here.
coded = "WKLV LV D PHVVDJH IURP WKH IURQW OLQH"

counts = {}
for character in coded:
    if character.isupper():
        counts[character] = counts.get(character, 0) + 1

def how_often(letter):
    return counts[letter]

print(sorted(counts, key=how_often, reverse=True))
# Guess which letter is E. What shift, or what key, does that suggest?
```

</div>

<div class="dl-world" data-world="pixel-art">

**Make a pixel-art animation.** An animation is a list of pictures, the
frames, shown one after another. The first step is two frames of a
sprite, one with its eyes open and one with them shut, printed one under
the other. A harder step is frames made by a rule, such as a sprite moving one pixel to the
right each frame, a picture growing from its middle, or a palette that
cycles its colours.

```python challenge
# Each frame is a picture: a list of rows.
frames = [
    ["..##..", ".#..#.", "..##.."],
    ["..##..", ".####.", "..##.."],
]

for number, frame in enumerate(frames):
    print("Frame", number)
    for row in frame:
        print(row)
    print()
# Can a function make the frames for you, from a rule?
```

</div>

The mixed problems, [Mixed problems: programming](tutorial:mixed-programming),
review the whole series, with no label on which page each problem
needs.

## Where to read more

Everything here is covered elsewhere too, often in a form that will suit you
better than this one.

Computerphile (2016). *Computer Science's Wonder Woman: Ada Lovelace*.
<https://www.youtube.com/watch?v=wnHHzBY1SPQ>. It tells the fuller story
of the translator's note that became longer than the paper it was
translating.

Khan Academy. *The Binary Number System*.
<https://www.khanacademy.org/computing/computers-and-internet/xcae6f4a7ff015e7d:digital-information/xcae6f4a7ff015e7d:binary-numbers/v/the-binary-number-system>.
This video explains binary more slowly, with worked examples, for anyone
who wants a second example before trying the conversions.

Eater, B. *Build an 8-Bit Computer*. <https://eater.net/8bit>. On video,
Ben Eater builds everything this page only describes: machine code, binary
and an instruction set. He builds it by hand, one logic gate at a time.

CrashCourse (2017). *The First Programming Languages: Crash Course
Computer Science #11.* <https://www.youtube.com/watch?v=RU1u-js7db8>. It
goes from machine code to assembly to FORTRAN, and explains why each step
made programs easier for people to write. The video is about eleven
minutes long.
