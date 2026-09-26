---
title: "Numbers a computer can hold"
year: "2026-2027"
version: 2026.09.25.1
covers:
  the-row-and-column-of-a-pixel:
    covers: [PDP-LO4]
    touches: [MIT-1.1]
  families-of-numbers:
    covers: [MIT-1.1]
  two-kinds-of-number-in-python:
    covers: [PDP-LO4, MIT-1.1]
  which-comes-first:
    covers: [PDP-LO4]
  powers-and-how-many-times:
    covers: [MIT-1.1]
  taking-a-number-apart:
    covers: [PDP-LO4]
---

# Numbers a computer can hold

Look at the clock on a microwave. Each digit is made of seven small bars
of light. Inside, the computer keeps one number, and every time the
display changes, it takes that number apart to know which bars to light.

Here is the first surprise. Ask Python to divide 7 by 2, and it can give
you three answers: `3.5`, `3` and `1`. If division at school had one
answer, that may feel wrong. It is not. Each answer belongs to a
different question, and the last two are the tools a display needs.

On this page we:

- meet three kinds of division, and find a pixel on a screen with them
- meet the families of numbers, and Python's two kinds of number
- work out the order Python does things in, inside one line
- count the patterns that seven bars of light can make
- take a number apart, and write `digit_at`, the first tool in your toolkit

> **The space we're in.** Numbers, and the question "which family of
> numbers are we in?". Python gives us `+`, `-`, `*`, `/` and a few more
> without being asked. Two things about Python's numbers usually go
> unsaid. Its whole numbers never run out, however big they get. Its
> decimal numbers are rounded, very slightly, almost all the time.

## Warm-up

```question
id: numbers-warm-up-1
type: fill-in-the-blank

After `cups = 2`, then `water = cups * 250`, then `cups = 3`, the line `print(water)` shows {500}.
```

```question
id: numbers-warm-up-2
type: multiple-choice
answer: 2

What does `print(3 * "7")` show?

- `21`
  - This treats `"7"` as the number 7; the quotes make it text.
- `777`
  - Multiplying text by a whole number repeats it: three copies of `"7"`.
- An error, because `"7"` is not a number.
  - Adding a number to text raises an error, but multiplying text by a whole number repeats it.
```

## The row and column of a pixel

A screen is a grid of tiny squares of light. Each square is a *pixel*.
A computer often numbers the pixels from 0, row after row. Here is a
very small screen, 2 pixels wide:

```text
 0  1
 2  3
 4  5
 6  7
```

Counting from 0, the way the computer counts, pixel 7 is in row 3 and
column 1. How could a computer work that out from 7 and 2 alone? Before
you run the cell, guess what each line shows. The third line uses `%`,
which you may not have met. Guess anyway.

```python exec
id: numbers-pixel-1
print(7 / 2)
print(7 // 2)
print(7 % 2)
```

Each answer belongs to a different question.

- `7 / 2` is ordinary division. 3.5 is a true answer, but there is no
  row 3.5.
- `7 // 2` is *floor division*: division that keeps only the whole
  number part of the answer. It gives 3, the row.
- `7 % 2` gives the *remainder*, what is left over after floor division.
  It gives 1, the column. Programmers often call `%` "modulo", or "mod".

Pixels 0 to 5 fill three rows, and pixel 7 is second in the next. `//` counts the full rows before it, and `%` counts how
far along its own row it is. So on any screen, a pixel's row is
`pixel // width`, and its column is `pixel % width`.

### Your turn

Later in this unit we draw digits on a grid 4 pixels wide and 7 pixels
tall. Its pixels are numbered from 0 to 27.

1. Before you run anything, work out the row and column of pixel 25.
2. Change the cell below to check, using `//` and `%`.

```python exec
id: numbers-pixel-your-turn
print(7 // 2)
print(7 % 2)
```

## Families of numbers

Some questions only make sense with whole things: there is no pixel
3.5. Mathematicians have names for these different spaces of numbers.
There are four main ones, and each is bigger than the last.

The *natural numbers*, written $\mathbb{N}$, are the counting numbers:
0, 1, 2, 3 and so on. (Some books start at 1. This course counts 0 as a
natural number.) In $\mathbb{N}$ you can always add, and always
multiply. But $3 - 5$ has no answer. It is like the building in
[Four questions for any puzzle](tutorial:four-questions#the-same-move-in-a-different-space)
with no floors below the ground.

The *integers*, written $\mathbb{Z}$, are the whole numbers, with the
negative ones added: …, −2, −1, 0, 1, 2, …. Now $3 - 5 = -2$. But
$7 \div 2$ has no answer in $\mathbb{Z}$, because no whole number
doubles to make 7.

The *rational numbers*, written $\mathbb{Q}$, are all the numbers you
can write as one integer divided by another: the fractions, like
$\frac{7}{2}$ or $-\frac{1}{4}$. Now $7 \div 2 = \frac{7}{2} = 3.5$. You
can divide by anything except 0.

The *real numbers*, written $\mathbb{R}$, are all the points on the
number line. Some of them are not fractions at all. The number that
squares to make 2, written $\sqrt{2}$, is one; so is $\pi$.

| Family | What it adds | A move that has no answer here |
|---|---|---|
| $\mathbb{N}$, natural | counting: 0, 1, 2, … | $3 - 5$ |
| $\mathbb{Z}$, integers | negative whole numbers | $7 \div 2$ |
| $\mathbb{Q}$, rational | fractions | $\sqrt{2}$ |
| $\mathbb{R}$, real | every point on the line | (a later unit goes bigger) |

Each family sits inside the next, like boxes inside boxes:
$\mathbb{N} \subset \mathbb{Z} \subset \mathbb{Q} \subset \mathbb{R}$.
So when someone says "you can't take 5 from 3", they are right, in
$\mathbb{N}$. The move is not foolish. It needs a bigger space.

```question
id: numbers-families-1
type: multiple-choice
answer: 2

What is the smallest family in which $3 - 5$ has an answer?

- $\mathbb{N}$, the natural numbers
  - The answer is −2, and no natural number is below 0.
- $\mathbb{Z}$, the integers
  - The integers add the numbers below 0, and −2 is one of them.
- $\mathbb{Q}$, the rational numbers
  - −2 is a rational number, but the integers already hold it, and they sit inside the rationals.
- $\mathbb{R}$, the real numbers
  - −2 is a real number, but the integers already hold it, and they sit inside the reals.
```

```question
id: numbers-families-2
type: fill-in-the-blank

`7 // 2` gives an answer that stays inside the {integers|rational numbers|real numbers}. `7 / 2` gives an answer from the {rational numbers|integers|natural numbers}.
```

## Two kinds of number in Python

Python has its own number spaces. The function `type()` tells you which
kind of value something is. Before you run the cell, look at the last
line. Will Python show `2` or `2.0`?

```python exec
id: numbers-two-kinds-1
print(type(7))
print(type(3.5))
print(type(7 / 2))
print(type(7 // 2))
print(6 / 3)
```

An *int*, short for integer, is a whole number in Python: Python's
version of $\mathbb{Z}$. A *float* is a number with a decimal point,
like `3.5`: Python's stand-in for $\mathbb{R}$. The name comes from the
"floating" decimal point, which can sit anywhere in the number.

Now look at the last line. `6 / 3` gives `2.0`, not `2`. The `/` sign
always gives a float, even when the division comes out exactly. `//`
stays with ints, when it is given ints.

What do you think will happen here? The first line multiplies three
nine-digit numbers.

```python exec
id: numbers-two-kinds-2
print(123456789 * 987654321 * 123456789)
print(0.1 + 0.2)
```

The first answer has 26 digits, and every one of them is right. Python's
ints never run out of room. Many other languages have a largest whole
number, but Python does not.

The second answer is `0.30000000000000004`. That is not your mistake,
and not really Python's. A float keeps about 16 digits, and some
decimals, like 0.1, cannot be stored exactly. A later page in this unit
shows why. For now: ints are exact, and floats are very close.

## Which comes first

The pixel sum also runs the other way. On the grid 4 pixels wide, which
pixel is in row 6, column 1? Six full rows of 4 come before it, then 1
more. Which of these give the right pixel? Predict all three, then run.

```python exec
id: numbers-order-1
print(6 * 4 + 1)
print(1 + 6 * 4)
print((1 + 6) * 4)
```

The first two show `25`, the pixel from the last Your turn. The third
shows `28`, which is not on the grid at all.

Even inside one line, there is a "what happens when?". Python does not
always work from left to right. It follows the *order of operations*:

1. anything in brackets, first;
2. then powers (we meet these in the next section);
3. then multiplying and dividing, from left to right;
4. then adding and subtracting, from left to right.

You may have met this at school as BIMDAS or BODMAS. In `1 + 6 * 4`, the
multiply happens first. In `(1 + 6) * 4`, the brackets go first.
Python counts `//` and `%` as dividing, so they take their turn with `*`
and `/`.

A few words for what we have been writing. An *expression* is a piece of
code that Python works out to one value, like `6 * 4 + 1`. An *operator*
is a symbol that does one job in an expression, like `+`, `*`, `//` or
`%`. A *statement* is one complete instruction, usually one line, like
`pixel = 6 * 4 + 1` or `print(pixel)`.

### Your turn

Each pixel has a brightness from 0 to 255. We want the brightness
halfway between 255 and 136.

1. Predict what `255 + 136 / 2` gives. Which part happens first?
2. Run it in the cell below and check.
3. Add brackets so that the line gives the halfway value, 195.5.

```python exec
id: numbers-order-your-turn
print(255 + 136 / 2)
```

## Powers, and how many times

Back to the microwave clock. Each bar of light is a *segment*, and a
digit made of seven is a *seven-segment display*. The segments have
standard names, a to g:

```text
 aaaa
f    b
f    b
 gggg
e    c
e    c
 dddd
```

The digit 1 lights b and c, and 8 lights all seven. How many different
patterns can seven segments make, each on or off? Pause here and make
a guess before you read on.

One segment has 2 patterns: off and on. Two have 4: off-off, off-on,
on-off and on-on. Each new segment doubles the count, because every old
pattern can come with the new one off or on. So seven segments give
$2 \times 2 \times 2 \times 2 \times 2 \times 2 \times 2$ patterns.

That is a *power*, written $2^7$ and said "2 to the power 7". The 2 is
the *base*, the number being multiplied, and the 7 is the *exponent*,
how many times. In Python, the power sign is `**`.

```python exec
id: numbers-powers-1
print(2 ** 7)
print(2 * 2 * 2 * 2 * 2 * 2 * 2)
print(2 ** 7 - 10)
```

There are 128 patterns, and only 10 of them are digits. The other 118
are shapes no clock ever shows.

<aside class="dl-note" id="numbers-note-hello">

**Words on a calculator.** A calculator's digits are seven segments too,
and upside down some of them look like letters. Type 0.7734, turn the
calculator over, and it says "hELLO".

</aside>

Now turn the question round. How many on-or-off lights would give
1,000 different patterns? That asks how many times we double 1 to reach
1,000. A *logarithm* is the number of times you multiply a base to reach
a number. For example:

$$\log_2 128 = 7 \quad \text{because} \quad 2^7 = 128$$

A logarithm is a power, read backwards. Python keeps it in a *module*:
a collection of extra tools that Python keeps on the shelf until you
ask for them with `import`. Guess the last line before you run it.
About 8 billion people live on Earth. How many on-or-off lights would
give every one of them a pattern of their own?

```python exec
id: numbers-powers-2
import math

print(math.log2(128))
print(math.log2(1000))
print(math.log2(8000000000))
```

The second is about 9.97: nine doublings reach 512, and a little less
than one more reaches 1,000. So a logarithm need not be a whole number,
and 10 lights are enough.

The last is about 32.9. So 33 lights are enough for every person on
Earth. I think this is the most surprising number on the page. Doubling
grows so fast that its backwards question, the logarithm, grows very
slowly.

### Your turn

1. A display with 4 digits shows numbers from 0000 to 9999. How many
   different numbers is that? Write it as a power of 10 with `**`.
2. `math.log10` asks "how many times do I multiply by 10?". Before you
   run it, what do you think `math.log10(10000)` gives?

```python exec
id: numbers-powers-your-turn
import math

print(math.log10(10000))
```

## Taking a number apart

Now the display's real job. The computer holds the number 2026, and the
display has four digits to light. Which digit goes where?

The last digit is what is left over when we divide by 10, so it is
`2026 % 10`. Floor division by 10 drops the last digit: `2026 // 10` is
202. So the digit before it is `202 % 10`. Before you run this cell,
say what each line shows.

```python exec
id: numbers-digits-1
print(2026 % 10)
print(2026 // 10 % 10)
print(2026 // 100 % 10)
print(2026 // 1000 % 10)
```

Read from the bottom up, the lines show 2, 0, 2, 6. Each line divides
by 1, 10, 100 or 1000, which are $10^0$ to $10^3$, then keeps the last
digit. So the digit in place 3, counting from 0 on the right, is
`2026 // 10 ** 3 % 10`: first the power, then `//`, then `%`.

On the last page, a function printed steps. A tool for the display
should hand back a number that other code can use.

```python exec
id: numbers-digits-2
def last_digit(number):
    """Give the last digit of a whole number."""
    return number % 10

print(last_digit(2026))
print(last_digit(7))
```

The *return* line hands a value back to whoever called the function:
`last_digit(2026)` is replaced by 6. Words like `def` and `return` are
*keywords*: words Python keeps for its own use, so they cannot be
names. The text in three quote marks is a *docstring*, which says what
the function promises. Python does not check it; it is for people.

So how do we check a promise? An *assert* statement checks that
something is true. If it is true, nothing happens. If it is false,
Python stops with an error.

```python exec
id: numbers-digits-3
assert last_digit(2026) == 6
assert last_digit(7) == 7
print("last_digit keeps its promise.")
```

The `==` sign asks "are these equal?". It is different from `=`, which
makes a name point at a value.

The next cell tests for a wrong answer on purpose, so that you can see
a failed test. It is meant to stop with an error.

```python exec
id: numbers-digits-4
assert last_digit(2026) == 2
```

The last line says `AssertionError`, and the line above it shows which
test failed. An error here is not a verdict on you. It is information:
this promise, on this line, was not kept.

### Your turn: your first toolkit tool

A microwave timer shows minutes and seconds. 1234 seconds is 20
minutes and 34 seconds, because `1234 // 60` is 20 and `1234 % 60` is
34. Minutes and seconds are digits in *base 60*: their columns are
worth 1, 60, 3600 and so on, the powers of 60.

<aside class="dl-note" id="numbers-note-sixty">

**Why sixty?** Mathematicians in ancient Mesopotamia, in what is now
Iraq, wrote numbers in base 60 about four thousand years ago.
Astronomers kept using it, and our 60 minutes in an hour come from that
tradition.

</aside>

The cell below is the start of `digit_at`, the first tool in your
*toolkit*: the set of functions you build across this course. Later
pages load them for you. Replace the `...` with one line that starts
with `return`. The digits cell above has the pattern, with 10 in place
of `base`.

`base=10` gives the parameter a *default value*: if a call does not say
what the base is, it is 10. So `digit_at(2026, 3)` counts in tens, and
`digit_at(1234, 1, 60)` counts in sixties.

```python exec
id: numbers-toolkit
toolkit: yes
def digit_at(number, place, base=10):
    """Give the digit of a whole number in one place.

    number is a whole number, 0 or more. place counts from 0 on the
    right: place 0 is the ones, place 1 the tens, and so on. base is how
    many digits the counting uses: 10 unless you say otherwise, or 60
    for minutes and seconds.
    """
    ...
```

```python toolkit-reference
for: numbers-toolkit
def digit_at(number, place, base=10):
    """Give the digit of a whole number in one place.

    number is a whole number, 0 or more. place counts from 0 on the
    right: place 0 is the ones, place 1 the tens, and so on. base is how
    many digits the counting uses: 10 unless you say otherwise, or 60
    for minutes and seconds.
    """
    return number // base ** place % base
```

Now test it. Until the `return` line is written, this cell stops with
an error: the tests are doing their job.

```python exec
id: numbers-toolkit-tests
assert digit_at(2026, 0) == 6
assert digit_at(2026, 3) == 2
assert digit_at(2026, 4) == 0
assert digit_at(1234, 0, 60) == 34
assert digit_at(1234, 1, 60) == 20
print("digit_at keeps its promise.")
```

```hint
Which line does the error point at, and what did you expect
`digit_at(2026, 0)` to give? Try `print(digit_at(2026, 0))` on its own
to see what your version gives now.
```

```hint
after: 10 errors
title: some steps
1. The digit in place 3 of 2026 was `2026 // 10 ** 3 % 10`.
2. In the function, the number is `number`, the place is `place`, and
   10 is `base`.
3. Put those names where the numbers were, after `return`.

**Think about:** why does `digit_at(2026, 4)` give 0, when 2026 has only
four digits?
```

A real microwave reads its buttons. Python's `input()` waits for
someone to type. Asking for a value is *input*, and showing a result is
*output*.

```python
seconds = int(input("How many seconds? "))
print(digit_at(seconds, 1, 60), "minutes and", digit_at(seconds, 0, 60), "seconds")
```

The Python on this page has no keyboard to listen to, so we edit a cell
instead. `int()` turns the typed text into a whole number, because
whatever someone types arrives as a string.

<details class="dl-why"><summary>Why this way?</summary>

This page met logarithms as a question, "how many times do I multiply?",
and asked it about lights that are on or off. A textbook usually meets
them much later, as rules: the logarithm of a product is the sum of the
logarithms, and so on.

The rules are useful. They let you work with logarithms on paper, and
exams often ask for them.

We started with the question because a rule means little until you know
what it is a rule about. Here a logarithm is a power, read backwards,
and the next page uses the same question to count bits. The rules can
come when a page needs them.

</details>

## Four questions, looking back

| The question | On this page |
|---|---|
| What is named here? | the number families $\mathbb{N}$, $\mathbb{Z}$, $\mathbb{Q}$, $\mathbb{R}$; `int` and `float`; each segment, a to g; the toolkit tool `digit_at` |
| What is promised? | `//` promises a whole number, `/` a float; `digit_at` promises the digit in one place; `assert` checks a promise |
| What happens when? | brackets, then powers, then × and ÷, then + and −; a test runs after the function it tests |
| What does this space let us do? | $3 - 5$ needs $\mathbb{Z}$; $7 \div 2$ needs $\mathbb{Q}$; ints are exact and never run out; floats are very close; `math` needs `import` |

## What we have now

| Term | What it means |
|---|---|
| `/`, `//`, `%` | divide; divide and keep the whole part; the remainder |
| $\mathbb{N}$, $\mathbb{Z}$, $\mathbb{Q}$, $\mathbb{R}$ | natural numbers, integers, rational numbers, real numbers |
| `int`, `float` | Python's whole numbers (exact), and its decimals (very close) |
| order of operations | brackets, powers, × and ÷, + and − |
| expression, operator, statement | a piece of code with a value; a symbol that does one job; one complete instruction |
| power, `**` | $2^7$: 2 multiplied by itself 7 times |
| logarithm | how many times you multiply the base to reach a number: $\log_2 128 = 7$ |
| `return`, docstring, `assert` | hand back a value; the promise in words; a check that the promise is kept |
| `digit_at(number, place, base=10)` | your first toolkit tool: `number // base ** place % base` |
