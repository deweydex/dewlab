---
title: "Everything is ones and zeros"
year: "2026-2027"
version: 2026.09.24.1
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
  how-ff8800-makes-orange:
    covers: [MIT-1.4]
  two-tools-for-your-toolkit:
    touches: [MIT-1.4]
  why-01-02-is-not-03:
    covers: [MIT-1.4]
    touches: [MIT-1.1]
---

# Everything is ones and zeros

A web page asks for the colour `#FF8800`, and your screen shows orange.
Not one of those seven characters says "orange". So how does the screen
know? And why would anybody write a colour that way?

On this page we:

- count the way a computer counts, with only two digits, 0 and 1
- turn a whole number into binary and back again, by hand and in Python
- add two numbers in binary
- meet hexadecimal, a short way to write binary, and use it to read a colour
- put two new tools, `to_binary` and `to_hex`, into your toolkit
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
type: multiple-choice
correct: 2

On [Numbers a computer can hold](tutorial:numbers-a-computer-can-hold),
what did Python give for `7 // 2`?

- `3.5`
- `3`
- `4`
- `1`
```

```question
id: everything-is-warm-up-2
type: multiple-choice
correct: 1

On [Four questions for any puzzle](tutorial:four-questions), the same `*`
did two different jobs. What does `print(2 * "na")` show?

- `nana`
- `4`
- `na 2`
- nothing: Python cannot multiply text
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

Before you run the next cell, work that out. What number is `1101` in
binary? In Python, `0b` in front of a number means "this is binary".
Run it to check.

```python exec
id: everything-is-counting-1
print(0b1101)
print(8 + 4 + 0 + 1)
```

Both lines print 13. The first line is Python reading the binary for
us. The second is the same sum we did by hand.

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
[Recipes are algorithms](tutorial:recipes-are-algorithms). Here it is
in words:

1. Halve the number, and write down the remainder, 0 or 1.
2. Keep the half, without the remainder.
3. Repeat until the number is 0.
4. Read the remainders from the last one back to the first.

Python has what we need, from
[Numbers a computer can hold](tutorial:numbers-a-computer-can-hold).
`// 2` halves and drops the remainder, as `7 // 2` gave 3. `% 2` gives
the remainder that `//` dropped, as `7 % 2` gave 1.

The cell below follows the recipe for 13, one halving per pair of lines.
Before you run it, can you guess the four remainders?

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
first, they spell `1101`, which is where we started in the last section.

Writing the same two lines four times is tiring. This is the
repetition from [Recipes are algorithms](tutorial:recipes-are-algorithms),
and Python can repeat lines for us with a loop. Unit 3 is all about
loops. For now, Python already knows this recipe. `format(13, "b")` gives 13 written in binary,
as text.

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

Eight bits together are called a *byte*. The smallest byte is `00000000`,
which is 0. The largest is `11111111`, which is 255. So one byte holds
256 different values, and $256 = 2^8$. Each extra bit doubles the number
of values, because every old pattern can now start with a 0 or a 1.

This has real effects. In the arcade game Pac-Man, the level number was
kept in one byte. Players who reached level 256 found half the screen
turned into nonsense, because the game had never planned for a number
that one byte cannot hold.

The question also runs backwards. Say a festival sells 1,000 tickets,
and each needs its own number. How many bits do we need? We want the
power of 2 that reaches 1,000. That is a logarithm: "how many times do I
multiply 2 by itself?" On
[Numbers a computer can hold](tutorial:numbers-a-computer-can-hold),
`math.log2(1000)` came out at about 9.97. Now that number has a job to
do. Predict what it tells us, then run it to check.

```python exec
id: everything-is-bytes-1
import math

print(2 ** 8)
print(math.log2(1000))
print(2 ** 10)
```

`math.log2(1000)` is about 9.97, so 9 bits are not quite enough and 10
bits are. Ten bits give $2^{10} = 1024$ numbers, which is 24 more than
we need.

Python's own whole numbers never run out of bits. Try `print(2 ** 100)`
in the cell above. A machine that keeps each number in a fixed number
of bits could not hold that. Python grows the number as it needs to.

## Adding in binary

We add binary numbers the way we learned to add at school: column by
column, from the right, carrying when a column is full. The only new
fact is that a binary column is full at 2, so $1 + 1 = 10_2$: write 0,
carry 1.

Here is $0110_2 + 0111_2$, which is 6 + 7.

| | 8 | 4 | 2 | 1 |
|---|---|---|---|---|
| carry | 1 | 1 | | |
| | 0 | 1 | 1 | 0 |
| + | 0 | 1 | 1 | 1 |
| = | 1 | 1 | 0 | 1 |

From the right: 0 + 1 is 1. Then 1 + 1 is 10, so write 0 and carry 1.
Then 1 + 1 + the carried 1 is 11, so write 1 and carry 1. Last, 0 + 0 +
the carried 1 is 1. The answer is $1101_2$, which is 13. Run it to check.

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

The reason hexadecimal is useful is that one hex digit is exactly four
bits. Four bits make $2^4 = 16$ patterns, one for each hex digit.

| Hex | 0 | 1 | 7 | 8 | A | F |
|---|---|---|---|---|---|---|
| Bits | 0000 | 0001 | 0111 | 1000 | 1010 | 1111 |

So a byte, eight bits, is always two hex digits. `11111111` splits into
`1111 1111`, which is `F F`, so it is `FF`. In base 10 it is
$15 \times 16 + 15 = 255$.

In Python, `0x` in front of a number means hexadecimal, and
`format(n, "X")` writes a number in hexadecimal with capital letters.
What do you think each line prints? Run it to check.

```python exec
id: everything-is-hex-1
print(0xFF)
print(0x88)
print(format(255, "X"))
print(format(0b10001000, "X"))
```

## How #FF8800 makes orange

Look very closely at a screen and each dot, each *pixel*, is three tiny
lights: red, green and blue. Each light has a brightness from 0 (off) to
255 (as bright as it goes). That is one byte per light, so it is two hex
digits per light.

A colour like `#FF8800` is three bytes in a row:

| | Red | Green | Blue |
|---|---|---|---|
| Hex | FF | 88 | 00 |
| Brightness | 255 | 136 | 0 |

Red is full, green is about half, and blue is off. Red light and some
green light together look orange to our eyes.

```question
id: everything-is-colour-guess
type: multiple-choice
correct: 3

Using the same idea, what colour is `#0088FF`?

- a bright red
- a dark orange
- a sky blue
- a pale grey
```

The next cell draws a few colours side by side. The square brackets make
a list, a way to keep several values together. We meet lists properly
in Unit 5. Run it and look.

```python exec
id: everything-is-colour-1
import matplotlib.pyplot as plt

colours = ["#FF8800", "#0088FF", "#FFFF00", "#888888"]
plt.figure(figsize=(6, 2))
plt.bar(colours, [1, 1, 1, 1], color=colours)
plt.yticks([])
```

`#FFFF00` has red and green both full and no blue, and our eyes see
yellow. `#888888` has all three lights at the same brightness, so it is
a grey. Any colour with three equal bytes is a grey, from `#000000`
(black) to `#FFFFFF` (white).

### Your turn

1. Change one of the colours to a darker orange. Can you do it by making
   each light about half as bright as in `#FF8800`?
2. Make a colour of your own: a team's jersey, a favourite sweet
   wrapper, the sea in summer.
3. Add a fifth colour to the list of colours.
4. Add a fifth `1` to the list of heights, so the two lists match.

## Two tools for your toolkit

Your toolkit started with `split_bill` on
[Numbers a computer can hold](tutorial:numbers-a-computer-can-hold).
Later pages load it for you, so a tool you make once you can use on any
page after this one.

Here are two more. Each has a docstring, the text in triple quotes,
which says what the function promises. `to_binary` is complete. `to_hex` has
one line for you to finish: the `?` should be the letter that asks
`format` for hexadecimal.

```python exec
id: everything-is-toolkit
toolkit: yes
def to_binary(n):
    """Give the whole number n (0 or more) in binary, as a string of 0s and 1s."""
    return format(n, "b")


def to_hex(n):
    """Give the whole number n (0 or more) in hexadecimal, as a string, with capital letters."""
    return format(n, "?")
```

```python toolkit-reference
for: everything-is-toolkit
def to_binary(n):
    """Give the whole number n (0 or more) in binary, as a string of 0s and 1s."""
    return format(n, "b")


def to_hex(n):
    """Give the whole number n (0 or more) in hexadecimal, as a string, with capital letters."""
    return format(n, "X")
```

A promise is only worth something if we check it. The next cell tests
both tools with `assert`. If every promise holds, it prints one line. If
one does not, it stops with an error and names the line that failed.
Until `to_hex` is finished, expect an error that ends
`Unknown format code '?'`: Python does not know a format called `?`.

```python exec
id: everything-is-toolkit-tests
assert to_binary(13) == "1101"
assert to_binary(0) == "0"
assert to_binary(255) == "11111111"
assert to_hex(255) == "FF"
assert to_hex(136) == "88"
assert to_hex(16) == "10"
print("Both tools keep their promises.")
```

### Your turn

1. Run the tests, and read the last line of anything that goes wrong.
2. Finish `to_hex`, and run the toolkit cell again.
3. Run the tests again.
4. Add one test of your own to the cell, one you worked out by hand
   first. What is 100 in hexadecimal?

## Why 0.1 + 0.2 is not 0.3

So far we have used whole numbers. What happens with a number that has
a decimal point? Before you run this cell, say what you expect each line
to print.

```python exec
id: everything-is-float-1
print(0.1 + 0.2)
print(0.1 + 0.2 == 0.3)
```

Python says `0.30000000000000004`, and `False`. That looks like a
mistake, and it is not one. It is what happens in the space Python's
decimals live in.

A float, the kind of number with a decimal point from
[Numbers a computer can hold](tutorial:numbers-a-computer-can-hold), is
kept in binary too. After the point, binary columns are worth a half, a
quarter, an eighth, and so on. Some numbers can be made from those exactly:
$0.75$ is a half plus a quarter. But $0.1$ is a tenth, and no set of
halves, quarters and eighths adds up to a tenth exactly. In binary it
repeats for ever:

$$0.1 = 0.000110011001100110011\ldots_2$$

It is like writing $\frac{1}{3}$ in our own digits: $0.3333\ldots$ never
ends, and wherever we stop, we are a tiny bit off. The computer stops after
about 16 digits' worth, so it keeps a number very close to 0.1, not
0.1 itself. The next cell shows 20 digits of what is really kept.

```python exec
id: everything-is-float-2
print(format(0.1, ".20f"))
print(format(0.75, ".20f"))
```

`0.75` is kept exactly. `0.1` is not. When two numbers that are both a
little off are added, the small errors can show.

So in the space of fractions, ℚ, the move "check that two answers are
equal with `==`" works. In the space of floats, it can fail. That does
not make floats wrong. It means that with floats, we ask "are these close
enough?" instead:

```python exec
id: everything-is-float-3
print(round(0.1 + 0.2, 10) == 0.3)
print(10 + 20 == 30)
```

The second line shows another way, which banks and shops use: count
money in whole cents, where binary has no trouble at all. There will be
a separate page about how a computer stores a number, for anyone who
wants the full story.

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
| What is named here? | A column's worth (1, 2, 4, 8…), a bit, a byte, and the two new tools `to_binary` and `to_hex` |
| What is promised? | Each tool's docstring, checked by `assert`; `#FF8800` promises three brightnesses |
| What happens when? | The halving recipe, step by step, and the carries in binary addition, from right to left |
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
| `to_binary(n)`, `to_hex(n)` | your two new toolkit tools |
| `0.1 + 0.2` | not exactly `0.3`, because 0.1 has no exact binary form |

Ready to try some on your own? The practice page is next. After it,
[When Python says no](tutorial:when-python-says-no) is about the red
text that appears when a move is not allowed.

## Where to read more

The dewlab page [Variables, data types and text](tutorial:storing-and-computing)
meets binary and hexadecimal from another direction, with a small
converter to build.

Petzold, C. (2022). *Code: The Hidden Language of Computer Hardware and
Software* (2nd ed.). Microsoft Press. Starts from torches and switches
and builds a whole computer out of them, one bit at a time.
