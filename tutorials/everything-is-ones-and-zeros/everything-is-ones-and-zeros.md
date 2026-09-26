---
title: "Everything is ones and zeros"
year: "2026-2027"
version: 2026.09.25.1
covers:
  counting-with-two-digits:
    covers: [MIT-1.4]
  from-a-number-to-its-bits:
    covers: [MIT-1.4]
    touches: [MIT-1.1]
  how-many-bits-is-enough:
    covers: [MIT-1.4]
    touches: [MIT-1.1]
  adding-in-binary:
    covers: [MIT-1.4]
  hexadecimal-binary-written-short:
    covers: [MIT-1.4]
  tools-for-your-toolkit:
    touches: [MIT-1.4]
  a-digit-drawn-in-pixels:
    covers: [MIT-1.4]
  how-ff8800-makes-orange:
    covers: [MIT-1.4]
  why-01-02-is-not-03:
    covers: [MIT-1.4]
    touches: [MIT-1.1]
---

# Everything is ones and zeros

Here is the digit 8, drawn with 28 small squares, where `#` is a square
that is lit:

```text
.##.
#..#
#..#
.##.
#..#
#..#
.##.
```

And here is the same 8, written as one number: `0x6996996`. Look at
that number for a moment. Can you see the 8 in it? If it looks like
nonsense, that is the right feeling. By the end of this page it will
not. You will also know why a web page that asks for the colour
`#FF8800` gets orange, when not one of those characters says "orange".

On this page we:

- count the way a computer counts, with only two digits, 0 and 1
- turn a whole number into binary and back, and read a display digit as bits
- add two numbers in binary
- meet hexadecimal, a short way to write binary
- add `to_binary`, `to_hex` and `pixel_row` to your toolkit
- draw a digit from one hex number, and read a colour like `#FF8800`
- find out why Python says `0.1 + 0.2` is not quite `0.3`

> **The space we're in.** Inside a computer, every number, letter,
> colour and sound is kept as a long row of switches, each one off or on.
> For most of this page we use whole numbers from 0 upwards, the space
> called ℕ on [Numbers a computer can hold](tutorial:numbers-a-computer-can-hold).
> Python lets us write a number in base 2 or base 16 as well as base 10,
> and it keeps whole numbers of any size, which many machines do not.

## Warm-up

Two questions from earlier pages, to get going.

```question
id: everything-is-warm-up-1
type: fill-in-the-blank

On [Numbers a computer can hold](tutorial:numbers-a-computer-can-hold),
your toolkit gained `digit_at`. `digit_at(2026, 1)` gives {2}.
```

```question
id: everything-is-warm-up-2
type: multiple-choice
answer: 1

On [Four questions for any puzzle](tutorial:four-questions), the same `*`
did two different jobs. What does `print(2 * "na")` show?

- `nana`
  - `*` with text and a whole number repeats the text.
- `4`
  - This multiplies 2 by 2, as if `"na"` were a number.
- `na 2`
  - This puts the two side by side, as `print("na", 2)` would.
- nothing: Python cannot multiply text
  - Python can repeat text with `*`, though it cannot multiply two pieces of text.
```

## Counting with two digits

We write numbers with ten digits, 0 to 9. When we run out of digits, we
start a new column. In the number 305, the 3 is worth three hundreds,
the 0 is worth no tens, and the 5 is worth five ones. Each column is
worth ten times the column to its right: 1, 10, 100, 1,000.

A computer has only two digits, 0 and 1, because a switch is either off
or on. One of these 0s or 1s is called a *bit*. Counting with only two
digits is called *binary*, or base 2. It works the same way as our
counting, with one change: each column is worth two times the column to
its right.

| Column worth | 8 | 4 | 2 | 1 |
|---|---|---|---|---|
| Bits of `1101` | 1 | 1 | 0 | 1 |

So the binary number `1101` means one 8, one 4, no 2 and one 1. In
symbols, with a small 2 to say which base we are in:

$$1101_2 = 1 \times 2^3 + 1 \times 2^2 + 0 \times 2^1 + 1 \times 2^0 = 8 + 4 + 0 + 1$$

Before you run the next cell, work that out. In Python, `0b` in front of
a number means "this is binary". Run it to check.

```python exec
id: everything-is-counting-1
print(0b1101)
print(8 + 4 + 0 + 1)
```

Both lines print 13. The first is Python reading the binary for us. The
second is the same sum we did by hand.

### Your turn

1. Change `0b1101` to `0b1111` and run the cell. Were you right?
2. Try `0b10000`. Why is it one more than `0b1111`?
3. Make up a row of 0s and 1s of your own, work it out, and check.

```python exec
id: everything-is-counting-2
print(0b1111)
```

## From a number to its bits

Going the other way needs a recipe, like the ones on
[Recipes are algorithms](tutorial:recipes-are-algorithms):

1. Halve the number, and write down the remainder, 0 or 1.
2. Keep the half, without the remainder.
3. Repeat until the number is 0.
4. Read the remainders from the last one back to the first.

`// 2` halves and drops the remainder, and `% 2` gives the remainder
that `//` dropped. The cell below follows the recipe for 13, one
halving per pair of lines. Can you guess the four remainders first?

```python exec
id: everything-is-bits-1
number = 13
print(number // 2, "remainder", number % 2)
number = number // 2
print(number // 2, "remainder", number % 2)
number = number // 2
print(number // 2, "remainder", number % 2)
number = number // 2
print(number // 2, "remainder", number % 2)
```

The remainders come out as 1, 0, 1, 1. Read from the last back to the
first, they spell `1101`, where we started. Look again at what the
recipe does: it is `digit_at` in base 2, one place at a time.

Writing the same two lines four times is tiring. Python can repeat lines
for us with a loop, and Unit 3 is all about loops. For now, Python
already knows this recipe: `format(13, "b")` gives 13 written in
binary, as text.

```python exec
id: everything-is-bits-2
print(format(13, "b"))
print(format(100, "b"))
```

### Your turn

1. Work out 25 in binary by hand, with the halving recipe.
2. Check your answer by changing `100` in the cell above to `25`.
3. Then check it the other way: put `0b` in front of your answer and print it.

## How many bits is enough?

The seven segments of a display digit, from
[Numbers a computer can hold](tutorial:numbers-a-computer-can-hold#powers-and-how-many-times),
are seven switches. So a digit's pattern is 7 bits. Give segment a the
ones column, b the twos, c the fours, and so on up to g, the 64s. Then
the digit 1, which lights b and c, is `0000110`, and the digit 8, which
lights them all, is `1111111`. A lot of real code for these displays
numbers the segments in this same order.

```python exec
id: everything-is-bytes-1
print(0b0000110)
print(0b1111111)
print(0b1011011)
```

```question
id: everything-is-segments-guess
type: multiple-choice
answer: 3

The last line's pattern, `1011011`, lights segments g, e, d, b and a.
Which digit is that?

- 1
  - A 1 lights only the two segments on the right.
- 7
  - A 7 lights the top and the two on the right, with no middle.
- 2
  - g, e, d, b and a: the top, upper right, middle, lower left and bottom make a 2.
- 9
  - A 9 lights the upper left segment, f, and the lower right, c.
```

Eight bits together are called a *byte*. The smallest byte is
`00000000`, which is 0, and the largest is `11111111`, which is 255. So
one byte holds $2^8 = 256$ different values. A digit's seven bits fit in
one byte with a bit to spare, and display code often uses that eighth
bit for the decimal point.

A byte's limit has real effects. In the arcade game Pac-Man, the level
number was kept in one byte. Players who reached level 256 found half
the screen turned into nonsense, because the game had never planned for
a number one byte cannot hold.

The question also runs backwards. A Full HD screen has 2,073,600
pixels. How many bits does it take to give each one its own number?
That is "how many times do I double 1?", a logarithm. Predict, then run.

```python exec
id: everything-is-bytes-2
import math

print(math.log2(2073600))
print(2 ** 21)
```

It is about 20.98, so 20 bits are not quite enough and 21 are.
$2^{21}$ is 2,097,152 numbers, enough for every pixel. Python's own
whole numbers never run out of bits: try `print(2 ** 100)` in the cell
above.

## Adding in binary

We add binary numbers the way we learned at school: column by column,
from the right, carrying when a column is full. The only new fact is
that a binary column is full at 2, so $1 + 1 = 10_2$: write 0, carry 1.
Here is $0110_2 + 0111_2$, which is 6 + 7.

| | 8 | 4 | 2 | 1 |
|---|---|---|---|---|
| carry | 1 | 1 | | |
| | 0 | 1 | 1 | 0 |
| + | 0 | 1 | 1 | 1 |
| = | 1 | 1 | 0 | 1 |

From the right: 0 + 1 is 1. Then 1 + 1 is 10: write 0, carry 1. Then
1 + 1 + the carried 1 is 11: write 1, carry 1. Last, 0 + 0 + the carried
1 is 1. The answer is $1101_2$, which is 13.

```python exec
id: everything-is-adding-1
print(0b0110 + 0b0111)
print(format(0b0110 + 0b0111, "b"))
```

### Your turn

1. Add $1011_2 + 0101_2$ by hand, carrying where you need to.
2. Check your answer in the cell below.

```python exec
id: everything-is-adding-2
# Check 1011 + 0101 here
```

## Hexadecimal: binary, written short

Long rows of bits are hard for people to read. Is `11111111` eight 1s,
or seven? So programmers often use *hexadecimal*, or base 16. It needs
sixteen digits, so after 0 to 9 it uses the letters A to F, where A is
10 and F is 15.

Hexadecimal is useful because one hex digit is exactly four bits. Four
bits make $2^4 = 16$ patterns, one for each hex digit.

| Hex | 0 | 1 | 6 | 7 | 9 | F |
|---|---|---|---|---|---|---|
| Bits | 0000 | 0001 | 0110 | 0111 | 1001 | 1111 |

So a byte is always two hex digits. The display's 8, `01111111`, splits
into `0111 1111`, which is `7F`. In Python, `0x` in front of a number
means hexadecimal, and `format(n, "X")` writes a number in hex with
capital letters. What do you think each line prints?

```python exec
id: everything-is-hex-1
print(0xFF)
print(0x7F)
print(format(255, "X"))
print(format(0b1111111, "X"))
```

## Tools for your toolkit

Your toolkit started with `digit_at` on
[Numbers a computer can hold](tutorial:numbers-a-computer-can-hold).
Here are three more. `to_binary` and `pixel_row` are complete. `to_hex`
has one line for you to finish: the `?` should be the letter that asks
`format` for hexadecimal.

`pixel_row` turns a number into a row of pixels, `#` for each 1 bit and
`.` for each 0. It uses two new moves on text. `zfill(width)` fills the
text with 0s on the left until it is `width` long, and `replace` swaps
one character for another, everywhere in the text.

```python exec
id: everything-is-toolkit
toolkit: yes
def to_binary(n):
    """Give the whole number n (0 or more) in binary, as a string of 0s and 1s."""
    return format(n, "b")


def to_hex(n):
    """Give the whole number n (0 or more) in hexadecimal, as a string, with capital letters."""
    return format(n, "?")


def pixel_row(bits, width=4):
    """Give a row of pixels as text: # for each 1 bit, . for each 0 bit.

    bits is a whole number from 0 up to 2 ** width - 1. width is how
    many pixels wide the row is: 4 unless you say otherwise.
    """
    ones_and_zeros = to_binary(bits).zfill(width)
    return ones_and_zeros.replace("1", "#").replace("0", ".")
```

```python toolkit-reference
for: everything-is-toolkit
def to_binary(n):
    """Give the whole number n (0 or more) in binary, as a string of 0s and 1s."""
    return format(n, "b")


def to_hex(n):
    """Give the whole number n (0 or more) in hexadecimal, as a string, with capital letters."""
    return format(n, "X")


def pixel_row(bits, width=4):
    """Give a row of pixels as text: # for each 1 bit, . for each 0 bit.

    bits is a whole number from 0 up to 2 ** width - 1. width is how
    many pixels wide the row is: 4 unless you say otherwise.
    """
    ones_and_zeros = to_binary(bits).zfill(width)
    return ones_and_zeros.replace("1", "#").replace("0", ".")
```

The next cell tests all three with `assert`. Until `to_hex` is
finished, expect an error that ends `Unknown format code '?'`: Python
does not know a format called `?`.

```python exec
id: everything-is-toolkit-tests
assert to_binary(13) == "1101"
assert to_binary(0) == "0"
assert to_hex(255) == "FF"
assert to_hex(127) == "7F"
assert pixel_row(9) == "#..#"
assert pixel_row(6) == ".##."
assert pixel_row(1, 8) == ".......#"
print("All three tools keep their promises.")
```

### Your turn

1. Run the tests, and read the last line of anything that goes wrong.
2. Finish `to_hex`, run the toolkit cell again, then the tests.
3. Add one test of your own, worked out by hand first. What is 100 in
   hexadecimal?

## A digit drawn in pixels

Now the 8 from the top of the page. It is drawn in a *pixel font*: each
digit is a small grid of pixels, here 4 pixels wide and 7 tall. Each row is 4 pixels, so each row is 4 bits,
and 4 bits are one hex digit. The 8's rows are `.##.`, `#..#`, `#..#`,
`.##.`, `#..#`, `#..#` and `.##.`, which are 6, 9, 9, 6, 9, 9, 6. So
the whole digit is seven hex digits: `0x6996996`. The 8 was in the
number all along.

To draw it, we need each hex digit on its own. `digit_at` does that in
base 16: place 6 is the top row, and place 0 is the bottom one.

```python exec
id: everything-is-glyph-1
eight = 0x6996996
print(pixel_row(digit_at(eight, 6, 16)))
print(pixel_row(digit_at(eight, 5, 16)))
print(pixel_row(digit_at(eight, 4, 16)))
print(pixel_row(digit_at(eight, 3, 16)))
print(pixel_row(digit_at(eight, 2, 16)))
print(pixel_row(digit_at(eight, 1, 16)))
print(pixel_row(digit_at(eight, 0, 16)))
```

And here is something I find strange and a little lovely. `0x6996996`
is also an ordinary number: `print(0x6996996)` gives 110717334. A
number, a row of bits, a picture of an 8: to the computer they are one
thing. Only we decide what it means.

<aside class="dl-note" id="everything-is-note-font">

**Fonts made of dots.** A common kind of small text screen, found on
printers and many other machines, draws each letter in a cell 5 dots
wide and 8 dots tall. Our font is a model with 4 columns, chosen so
that each row is exactly one hex digit.

</aside>

### Your turn

1. Change `eight` to `0x691248F`. Before you run it, can you guess which
   digit it draws?
2. Design a digit of your own on the 4 by 7 grid, on paper. Write each
   row as 4 bits, then as one hex digit, and draw it.

## How #FF8800 makes orange

Each pixel on a colour screen is three tiny lights: red, green and
blue. Each light has a brightness from 0 (off) to 255 (as bright as it
goes). That is one byte per light, so two hex digits per light, and a
colour like `#FF8800` is three bytes in a row:

| | Red | Green | Blue |
|---|---|---|---|
| Hex | FF | 88 | 00 |
| Brightness | 255 | 136 | 0 |

Red is full, green is about half, and blue is off. Red light and some
green light together look orange to our eyes.

```question
id: everything-is-colour-guess
type: multiple-choice
answer: 3

Using the same idea, what colour is `#0088FF`?

- a bright red
  - Red is the first pair, `00` here: none at all.
- a dark orange
  - Orange needs a lot of red, and `00` is none.
- a sky blue
  - No red, some green (`88`) and full blue (`FF`).
- a pale grey
  - A grey has all three pairs equal.
```

The next cell draws a few colours side by side. The square brackets
make a list, a way to keep several values together; we meet lists
properly in Unit 5.

```python exec
id: everything-is-colour-1
import matplotlib.pyplot as plt

colours = ["#FF8800", "#0088FF", "#FFFF00", "#888888"]
plt.figure(figsize=(6, 2))
plt.bar(colours, [1, 1, 1, 1], color=colours)
plt.yticks([])
```

`#888888` has all three lights at the same brightness, so it is a grey.
Any colour with three equal bytes is a grey, from `#000000` (black) to
`#FFFFFF` (white).

### Your turn

1. Change one colour to a darker orange, with each light about half as
   bright as in `#FF8800`.
2. Make a colour of your own, add it to the list of colours, and add a
   fifth `1` to the list of heights so the two lists match.

## Why 0.1 + 0.2 is not 0.3

So far we have used whole numbers. What about a number with a decimal
point? Before you run this cell, say what you expect each line to print.

```python exec
id: everything-is-float-1
print(0.1 + 0.2)
print(0.1 + 0.2 == 0.3)
```

Python says `0.30000000000000004`, and `False`. That looks like a
mistake, and it is not one. It is what happens in the space Python's
decimals live in.

A float is kept in binary too. After the point, binary columns are worth
a half, a quarter, an eighth, and so on. Some numbers can be made from
those exactly: $0.75$ is a half plus a quarter. But no set of halves,
quarters and eighths adds up to a tenth exactly. In binary, 0.1 repeats
for ever:

$$0.1 = 0.000110011001100110011\ldots_2$$

It is like writing $\frac{1}{3}$ in our own digits: $0.3333\ldots$
never ends, and wherever we stop, we are a tiny bit off. The computer
stops after about 16 digits' worth, so it keeps a number very close to
0.1, not 0.1 itself. The next cell shows 20 digits of what is kept.

```python exec
id: everything-is-float-2
print(format(0.1, ".20f"))
print(format(0.75, ".20f"))
```

`0.75` is kept exactly. `0.1` is not. When two numbers that are both a
little off are added, the small errors can show.

So in the space of fractions, ℚ, the move "check that two answers are
equal with `==`" works. In the space of floats, it can fail. That does
not make floats wrong. With floats, we ask "are these close enough?":

```python exec
id: everything-is-float-3
print(round(0.1 + 0.2, 10) == 0.3)
print(10 + 20 == 30)
```

The second line shows another way, which banks and shops use: count
money in whole cents, where binary has no trouble at all. The page
[How a computer stores a number](tutorial:how-a-computer-stores-a-number)
has the full story, for anyone who wants it.

<details class="dl-why"><summary>Why this way?</summary>

To turn a number into binary, this page did the halving by hand, then
gave the job to Python's `format()`. Your toolkit's `to_binary` is one
line that calls it. A common exercise is to write the whole halving
recipe as a loop of your own.

That exercise is a good one. It shows every step, and it practises
loops.

But loops come in Unit 3, so the choice was to wait, or to use the tool
Python already has. "What does this space let us do?" includes what the
space gives us without asking, and knowing when to use a tool that is
already there is part of programming too. The halving recipe is still on
the page, in words and done by hand, so nothing about how it works is
hidden.

</details>

## Four questions, looking back

| Question | On this page |
|---|---|
| What is named here? | A column's worth (1, 2, 4, 8…), a bit, a byte, and the tools `to_binary`, `to_hex` and `pixel_row` |
| What is promised? | Each tool's docstring, checked by `assert`; `0x6996996` promises a picture of an 8, and `#FF8800` three brightnesses |
| What happens when? | The halving recipe, step by step; the carries in binary addition, from right to left; the rows of a digit, top to bottom |
| What does this space let us do? | Python's whole numbers grow as needed; a byte stops at 255; floats keep a tenth only nearly |

## What we have now

| Term or move | What it means |
|---|---|
| bit | one 0 or 1 |
| binary, base 2 | counting with two digits; columns worth 1, 2, 4, 8… |
| byte | eight bits; 256 values, 0 to 255 |
| hexadecimal, base 16 | digits 0–9 and A–F; one hex digit is four bits |
| `0b1101`, `0xFF` | a number written in binary, or in hex, in Python |
| `format(n, "b")`, `format(n, "X")` | a whole number as binary text, or as hex text |
| `#RRGGBB` | a colour as three bytes: red, green, blue |
| `to_binary(n)`, `to_hex(n)`, `pixel_row(bits, width=4)` | your three new toolkit tools |
| `0.1 + 0.2` | not exactly `0.3`, because 0.1 has no exact binary form |

Ready to try some on your own? The practice page is next. After it,
[When Python says no](tutorial:when-python-says-no) is about the red
text that appears when a move is not allowed.

## Where to read more

The dewlab page [How programming languages came to be](tutorial:how-we-got-here)
meets binary and hexadecimal from another direction, with a small
converter to build.

Petzold, C. (2022). *Code: The Hidden Language of Computer Hardware and
Software* (2nd ed.). Microsoft Press. Starts from torches and switches
and builds a whole computer out of them, one bit at a time.

3Blue1Brown (2015). *How to count to 1000 on two hands.*
<https://www.youtube.com/watch?v=1SMmc9gQmHQ>. Each finger is one bit: up
or down. Grant Sanderson counts in binary on his fingers. Under three
minutes.

CrashCourse (2017). *Representing Numbers and Letters with Binary: Crash
Course Computer Science #4.*
<https://www.youtube.com/watch?v=1GSjbWt0c9M>. How the same ones and zeros
can stand for numbers and for letters. About eleven minutes.
