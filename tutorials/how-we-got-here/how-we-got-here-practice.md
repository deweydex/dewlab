---
title: "How programming languages came to be — Practice"
practice_for: how-we-got-here
year: "2026-2027"
version: 2026.09.26.1
worlds:
  secret-messages: Codes and hidden messages, the kind spies and puzzle-setters make.
  pixel-art: Pictures made of small squares, the way a screen draws them.
---

# How programming languages came to be — Practice

Problems on binary, hexadecimal and ASCII, on the history and the
paradigms, and three from earlier pages. Try the conversions by hand
before you use the cell to check them: the aim is that you can read the
notation yourself, without Python reading it for you.

## Tools

Run this cell first. It builds the tutorial's two tools.

```python exec
id: tools-1
def to_binary(n):
    if n == 0:
        return "0"
    text = ""
    while n > 0:
        text = str(n % 2) + text
        n = n // 2
    return text

def from_binary(text):
    total = 0
    for digit in text:
        total = total * 2 + int(digit)
    return total

print(to_binary(72), from_binary("01001000"), hex(72), chr(72))
```

## 1. Binary to base 10

Change these binary numbers to base 10 by hand, then check: `1101`,
`10000`, `11111`, `10101010`.

<details class="dl-answer"><summary>answer</summary>

13, 16, 31, 170. `11111` is 31, not 32: a row of ones is always one less
than the next power of two. That is why a byte holds 0 to 255, and not 0
to 256.

</details>

## 2. Base 10 to binary

Change these to binary by hand, then check: 6, 12, 100, 255.

<details class="dl-answer"><summary>answer</summary>

110, 1100, 1100100, 11111111. 12 is 6 moved one place to the left:
doubling a number in binary adds a 0 on the end, the way multiplying by
ten does in base 10.

</details>

## 3. Base 10 to hex

Change these to hexadecimal: 15, 16, 255, 256, 4095.

<details class="dl-answer"><summary>answer</summary>

F, 10, FF, 100, FFF. FF is eight binary digits, one byte, and FFF is
twelve.

</details>

## 4. Hex to binary, straight

Change `FF`, `A0` and `7E` from hex to binary, without going through
base 10.

<details class="dl-answer"><summary>answer</summary>

`11111111`, `10100000`, `01111110`. Each hex digit becomes four binary
digits on its own: F is 1111, A is 1010, 0 is 0000, 7 is 0111 and E is
1110. No base 10 is needed, which is the whole point of hex.

</details>

## 5. Two letters

Decode `01001000 01001001` as ASCII.

<details class="dl-answer"><summary>answer</summary>

72 and 73, which are H and I: `HI`.

</details>

## 6. A colour

The web colour `#FF7F50` is two hex digits each for red, green and blue.
What are the three in base 10?

<details class="dl-answer"><summary>answer</summary>

255, 127 and 80: a colour called coral.

</details>

## 7. Reading hex without int

Can you write `read_hex(text)`, which gives the value of a hex string like
`"2A"`, without `int(text, 16)`? `digits.index(character)` gives where a
character is in the string `digits`.

```python exec
id: reading-hex-without-int-1
def read_hex(text):
    digits = "0123456789ABCDEF"
    return 0
```

```inputs
guess: yes
read_hex("2A")
read_hex("FF")
read_hex("100")
```

```hint
It is `from_binary` with 16 in place of 2. At each digit, multiply the
total so far by 16, and add the digit's value.
```

```solution
def read_hex(text):
    digits = "0123456789ABCDEF"
    total = 0
    for character in text:
        total = total * 16 + digits.index(character)
    return total
---
`total * 16 + digit` is how to read a number in any base: move everything
up one place, then add the new digit. Change the 16 and the digits, and
the same function reads base 7.
```

## 8. Why binary

Why do computers use binary, and not base 10?

<details class="dl-answer"><summary>answer</summary>

Because the hardware has two states. A transistor is on or off, high
voltage or low, and base 2 matches that exactly. A circuit that had to
tell ten voltage levels apart would be harder to build and easier to
fool. Base 10 is about people's fingers, not about machines.

</details>

## 9. Why hex

Why does hexadecimal exist, when computers do not use it?

<details class="dl-answer"><summary>answer</summary>

For people. One hex digit is exactly four binary digits, so a byte is two
hex digits, and a long binary pattern becomes short enough to read and
copy without losing count. It is binary, written shorter.

</details>

## 10. Lovelace

What did Ada Lovelace do, and why does it matter that the machine was
never built?

<details class="dl-answer"><summary>answer</summary>

She wrote a step-by-step method for the Analytical Engine to work out a
sequence of numbers, with loops and conditional branching, in notes to a
translation that ended up longer than the paper. That the machine was
never built is the point: a program does not need a working machine to
exist. It is a list of exact instructions, whether or not anything can
carry them out yet.

</details>

## 11. In order

Put these in order, and say what each one made easier: high-level
languages, machine code, assembly language.

<details class="dl-answer"><summary>answer</summary>

1. Machine code, in the 1940s: binary the hardware runs directly.
2. Assembly, in the 1950s: short names like `ADD` in place of binary,
   turned back into binary by an assembler.
3. High-level languages, from 1957: code that reads like English or
   mathematics, no longer tied to one kind of machine.

Each step made things easier for people. The hardware never needed any of
them.

</details>

## 12. Compiled or interpreted

Why does a compiled program usually run faster? And why is an interpreted
language usually quicker to find and fix mistakes in?

<details class="dl-answer"><summary>answer</summary>

A compiled program was translated before it ran, so no time goes on
translating while it runs, and the compiler could look at the whole
program to make it faster. An interpreted program is translated as it
runs, which takes time, but there is no step between changing a line and
seeing what it does. When you are hunting a bug, that is worth a great
deal.

</details>

## 13. The overnight batch

A bank processes the day's payments overnight, in one large batch. Which
language from the table would you expect to find doing that job? Why?

<details class="dl-answer"><summary>answer</summary>

COBOL, and a surprising amount of this work still runs on it. It was built
in 1959 for business data, banks took it up early, and code that has
worked, and been checked, for decades is not replaced without a very good
reason. Software lasts much longer than the reasons it was written.

</details>

## 14. Which paradigm

Which paradigm is each closest to? What told you?

- (a) `total = 0`, then a loop adding each price to it
- (b) `sum(price for price in prices)`
- (c) `basket.add(4.50)`, then `basket.total()`
- (d) `apply_to_all(double, prices)`

<details class="dl-answer"><summary>answer</summary>

(a) Procedural: a variable changed step by step. (b) Declarative: it says
what the answer is. (c) Object-oriented: the basket keeps its prices, and
adding and totalling are things it does. (d) Functional: a function,
`double`, is handed to another function as a value.

</details>

## 15. Back to a loop

Rewrite `doubled = [n * 2 for n in numbers]` in the procedural style.

<details class="dl-answer"><summary>answer</summary>

```python
doubled = []
for n in numbers:
    doubled.append(n * 2)
```

Three lines in place of one, doing the same thing. Which is better depends
on who is reading it.

</details>

## 16. Is one of them right

Is any of the four paradigms the right one?

<details class="dl-answer"><summary>answer</summary>

No. They are habits of thought. A procedural loop is clearer for a
beginner; a declarative line is clearer once you are used to it; an
object helps when there is data to keep track of between steps, and gets
in the way when there is not. A program that mixes all four without a plan
is harder to read than one that keeps to one.

</details>

## 17. The first two bytes

A file's first two bytes are `50 4B` in hex. What are they as characters,
and what might they tell you about the file?

<details class="dl-answer"><summary>answer</summary>

80 and 75, which are P and K. `PK` starts every ZIP file: they are the
initials of Phil Katz, who wrote the ZIP format in 1989. Many formats
start with a few fixed bytes like these, a *magic number*, and software
often reads them to decide what a file is, without trusting its name.

</details>

## 18. The other way

<div class="dl-world" data-world="secret-messages">

Can you write `to_hex_message(text)`, which gives back each character's
ASCII code as two hex digits, the way the 1958 memory dump was written?
`hex(n)[2:]` is the hex without its `0x`, and `.upper()` makes it capitals.

```python exec
id: the-other-way-1--secret-messages
def to_hex_message(text):
    return []
```

```inputs
guess: yes
to_hex_message("HI")
to_hex_message("CODE")
to_hex_message("")
```

```solution
def to_hex_message(text):
    groups = []
    for character in text:
        groups.append(hex(ord(character))[2:].upper())
    return groups
---
`ord()` gives the code, and `hex()` writes it in hex. For capital letters,
the codes are 65 to 90, so two hex digits are always enough.
```

</div>

<div class="dl-world" data-world="pixel-art">

Can you write `row_to_hex(row)`, which turns a row of eight pixels, `#`
and `.`, into the two hex digits a game would store it as?
`hex(n)[2:]` is the hex without its `0x`, and `.upper()` makes it capitals.

```python exec
id: the-other-way-1--pixel-art
def row_to_hex(row):
    return ""
```

```inputs
guess: yes
row_to_hex("##..##..")
row_to_hex("#..#....")
row_to_hex("........")
```

```hint
First turn the row into binary digits, 1 for `#` and 0 for `.`. Then
`from_binary` gives the number, and `hex()` writes it.
```

```solution
def from_binary(text):
    total = 0
    for digit in text:
        total = total * 2 + int(digit)
    return total

def row_to_hex(row):
    bits = ""
    for pixel in row:
        if pixel == "#":
            bits = bits + "1"
        else:
            bits = bits + "0"
    text = hex(from_binary(bits))[2:].upper()
    return "0" * (2 - len(text)) + text
---
`"##..##.."` is `CC`, and a dark row is `00`. Without the last line, it
would be `0`, one digit, and a program reading two digits a row would lose
its place.
```

</div>

## 19. From earlier: a key that is missing

From *Dictionaries: looking things up by name* and *Finding bugs in
bigger programs*.

```python exec
id: from-earlier-a-key-that-is-missing-1
counts = {"A": 1}
print(counts.get("B") + 1)
```

```predict
What will it do?

- Print 1
  - A missing count is 0, and 0 + 1 is 1.
- Stop with a KeyError
  - B is not a key.
- Stop with a TypeError
  - `.get()` gives None, and None + 1 is not allowed.
```

<details class="dl-answer"><summary>why</summary>

A `TypeError`: `.get()` with no default gives `None`, and `None + 1` has
no meaning. The mistake is the missing default, `.get("B", 0)`, and the
error turns up a step later, on the `+`.

</details>

## 20. From earlier: a test that asks the wrong thing

From *Designing and testing good functions* and *Sorting a list*.

```python exec
id: from-earlier-a-test-that-asks-the-wrong-thing-1
assert [3, 1, 2].sort() == [1, 2, 3]
print("passed")
```

```predict
What will it do?

- Print passed
  - The list sorted is [1, 2, 3].
- Stop with an AssertionError
  - `.sort()` gives back None.
```

<details class="dl-answer"><summary>why</summary>

It stops with an `AssertionError`. `.sort()` sorts its list and gives
back `None`, and `None` is not `[1, 2, 3]`. The test is right to fail, and
it is the test that is wrong: `sorted([3, 1, 2])` is what it meant.

</details>

## 21. From earlier: how many

From *Dictionaries: looking things up by name*.

```python exec
id: from-earlier-how-many-1
counts = {}
for letter in "HELLO":
    counts[letter] = counts.get(letter, 0) + 1
print(counts["L"])
```

```predict
type: number

What will it print?
```

<details class="dl-answer"><summary>why</summary>

2. The loop counts each letter as it meets it, and there are two Ls.

</details>
