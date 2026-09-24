---
title: "Numbers a computer can hold"
year: "2026-2027"
version: 2026.09.24.1
covers:
  sharing-seven-euro:
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
  a-calculator-for-splitting-the-bill:
    covers: [PDP-LO4]
---

# Numbers a computer can hold

Two friends find €7 on the ground and decide to share it. Ask Python,
and it gives two answers. `7 / 2` is `3.5`, and `7 // 2` is `3`.

Which one is right? Both of them. They answer two different questions,
in two different spaces. By the end of this page you will know which
space each one lives in, and you will have built a calculator that
splits a restaurant bill.

On this page we:

- meet three kinds of division in Python
- meet the families of numbers that mathematicians use, and the moves
  each one allows
- see Python's two kinds of number, and what each can hold
- work out the order Python does things in, inside one line
- meet powers, and turn them round into logarithms
- write `split_bill`, the first function in your own toolkit

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
correct: 2

What does `print(3 * "7")` show?

- `21`
- `777`
- An error, because `"7"` is not a number.
```

## Sharing seven euro

Here are three ways Python can divide 7 by 2. Before you run the cell,
guess what each line will show. The third line uses `%`, which you may
not have met. Guess anyway.

```python exec
id: numbers-sharing-1
print(7 / 2)
print(7 // 2)
print(7 % 2)
```

The three answers are `3.5`, `3` and `1`. Each answers a different
question about sharing €7 between two people.

- `7 / 2` asks: how much does each person get? If you can make change,
  each gets €3.50.
- `7 // 2` asks: how many whole euro coins does each person get, if
  nobody can make change? Each gets 3. This is *floor division*:
  division that keeps only the whole number part of the answer.
- `7 % 2` asks: how many coins are left over? One. This is the
  *remainder*. Programmers often call `%` "modulo", or "mod".

Picture seven coins in a line. Deal them out to two people, one at a
time. Each person ends up with three, and one coin is left on the table.
`//` counts the coins in each hand, and `%` counts the coin on the
table.

### Your turn

Twenty-five sweets are shared between four children, and no sweet is
cut in half.

1. Before you run anything, work out how many each child gets, and how
   many are left over.
2. Change the cell below to check your answer, using `//` and `%`.

```python exec
id: numbers-sharing-your-turn
print(7 // 2)
print(7 % 2)
```

## Families of numbers

Why does Python need two kinds of division? Because some questions only
make sense with whole things. You cannot hand someone half a coin, or
half a bus. Mathematicians have names for these different spaces of
numbers. There are four main ones, and each is bigger than the last.

The *natural numbers*, written $\mathbb{N}$, are the counting numbers:
0, 1, 2, 3 and so on. (Some books start at 1. This course counts 0 as a
natural number.) In $\mathbb{N}$ you can always add, and
always multiply. But $3 - 5$ has no answer. It is like the building in
[Four questions for any puzzle](tutorial:four-questions#the-same-move-in-a-different-space)
with no floors below the ground.

The *integers*, written $\mathbb{Z}$, are the whole numbers, with the
negative ones added: …, −2, −1, 0, 1, 2, …. Now $3 - 5 = -2$. But $7 \div 2$ has no answer in
$\mathbb{Z}$, because no whole number doubles to make 7.

The *rational numbers*, written $\mathbb{Q}$, are all the numbers you
can write as one integer divided by another: the fractions, like
$\frac{7}{2}$ or $-\frac{1}{4}$. Now $7 \div 2 = \frac{7}{2} = 3.5$. You
can divide by anything except 0.

The *real numbers*, written $\mathbb{R}$, are all the points on the
number line. Some of them are not fractions at all. The number that
squares to make 2, written $\sqrt{2}$, is one; so is $\pi$. Mathematicians
proved more than two thousand years ago that no fraction, however
carefully chosen, squares to exactly 2.

| Family | What it adds | A move that has no answer here |
|---|---|---|
| $\mathbb{N}$, natural | counting: 0, 1, 2, … | $3 - 5$ |
| $\mathbb{Z}$, integers | negative whole numbers | $7 \div 2$ |
| $\mathbb{Q}$, rational | fractions | $\sqrt{2}$ |
| $\mathbb{R}$, real | every point on the line | (a later unit builds a bigger space still) |

Each family sits inside the next, like a set of boxes, one inside
another. Every natural number is an integer, every integer is a
rational number, and every rational number is a real number. We write
that as $\mathbb{N} \subset \mathbb{Z} \subset \mathbb{Q} \subset \mathbb{R}$.

So when someone says "you can't take 5 from 3", they are right, in
$\mathbb{N}$. The move is not foolish. It needs a bigger space.

```question
id: numbers-families-1
type: multiple-choice
correct: 2

What is the smallest family in which $3 - 5$ has an answer?

- $\mathbb{N}$, the natural numbers
- $\mathbb{Z}$, the integers
- $\mathbb{Q}$, the rational numbers
- $\mathbb{R}$, the real numbers
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

Python calls whole numbers `int`, short for integer. An *int* is a whole
number in Python: Python's version of $\mathbb{Z}$. A *float* is a number
with a decimal point, like `3.5`. Floats are Python's stand-in for
$\mathbb{R}$. The name comes from the "floating" decimal point, which
can sit anywhere in the number.

Now look at the last line. `6 / 3` gives `2.0`, not `2`. The `/` sign
always gives a float, even when the division comes out exactly. `//`
stays with ints, when it is given ints.

Each space has its own rules about what it can hold. What do you think
will happen here? The first line multiplies three nine-digit numbers.
The second adds two small decimals.

```python exec
id: numbers-two-kinds-2
print(123456789 * 987654321 * 123456789)
print(0.1 + 0.2)
```

The first answer has 26 digits, and every one of them is right. Python's
ints never run out of room. Many other languages have a largest whole
number, but Python does not.

The second answer is `0.30000000000000004`. That is not a mistake by
you, and it is not really a mistake by Python. A float keeps about 16
digits, and some decimals, like 0.1, cannot be stored exactly in a
computer. The float that Python holds is very, very close to 0.1, but
not equal to it. A later page in this unit shows why. For now, the thing
to know is this: ints are exact, and floats are very close.

## Which comes first

Three friends each have a starter at €6, and one of them also has a main
course at €14. Here are three ways to write the bill. Which ones give
the right total? Predict all three, then run the cell.

```python exec
id: numbers-order-1
print(3 * 6 + 14)
print(14 + 3 * 6)
print((14 + 3) * 6)
```

The first two show `32`, the right bill. The third shows `102`.

Even inside one line, there is a "what happens when?". Python does not
always work from left to right. It follows the *order of operations*:

1. anything in brackets, first;
2. then powers (we meet these in the next section);
3. then multiplying and dividing, from left to right;
4. then adding and subtracting, from left to right.

You may have met this at school as BIMDAS or BODMAS. It is the same rule
in maths and in Python. In `14 + 3 * 6`, the multiply happens first, so
it is $14 + 18$. In `(14 + 3) * 6`, the brackets go first, so it is
$17 \times 6$, which is the wrong bill.

A few words for what we have been writing. An *expression* is a piece of
code that Python works out to one value, like `3 * 6 + 14`. An
*operator* is a symbol that does one job in an expression, like `+`,
`*`, `//` or `%`. A *statement* is one complete instruction, usually one
line, like `total = 3 * 6 + 14` or `print(total)`.

### Your turn

The friends want to leave a 10% tip on the €32 bill.

1. Predict what `32 + 32 * 10 / 100` gives. Which part happens first?
2. Run it in the cell below and check.
3. Write the same tip calculation another way, using brackets:
   `32 * (1 + 10 / 100)`. Do the two agree?

```python exec
id: numbers-order-your-turn
print(32 + 32 * 10 / 100)
```

## Powers, and how many times

Take a sheet of paper about 0.1 mm thick, and fold it in half. It is now
0.2 mm thick. Fold it again: 0.4 mm. Every fold doubles it.

After 10 folds, we have doubled 10 times:
$2 \times 2 \times 2 \times \dots \times 2$, with ten 2s. That is a *power*, written $2^{10}$ and
said "2 to the power 10". The 2 is the *base*, the number being
multiplied, and the 10 is the *exponent*, how many times. In Python,
the power sign is `**`.

How thick is the paper after 10 folds? And after 42 folds? Guess the
second one in whatever units you like, then run the cell. The last line
turns millimetres into kilometres and rounds to a whole number.

```python exec
id: numbers-powers-1
print(2 ** 10)
print(0.1 * 2 ** 10)
print(round(0.1 * 2 ** 42 / 1000 / 1000))
```

After 10 folds, the paper is 102.4 mm thick, about the width of your
hand. After 42 folds, it is about 439,805 km thick, which is further
than from here to the Moon. (Real paper cannot be folded much more
than about a dozen times, and even that needs a very long, thin sheet.
The maths does not mind.) The function `round()`
rounds a number to the nearest whole number; `round(x, 2)` rounds it to
two decimal places.

Now let's turn the question round. Music gives a good example. When a
note goes up by one octave, its frequency doubles. A low A on a bass
guitar is 55 Hz, and a high A, on a flute or a piano, is 880 Hz. How many octaves apart are
they? That is: how many times do we double 55 to reach 880?

$55 \to 110 \to 220 \to 440 \to 880$, so the answer is 4.

The question "how many times do I multiply by 2?" has a name. A
*logarithm* is the number of times you multiply a base to reach a
number. Here, $880 \div 55 = 16$, and we double 4 times to reach 16. So
the logarithm of 16, base 2, is 4:

$$\log_2 16 = 4 \quad \text{because} \quad 2^4 = 16$$

A logarithm is a power, read backwards. Python keeps it in a *module*:
a collection of extra tools that Python keeps on the shelf until you
ask for them with `import`. What do you think the last line will show?

```python exec
id: numbers-powers-2
import math

print(math.log2(16))
print(math.log2(880 / 55))
print(math.log2(1000))
```

The first two are `4.0`. The last is about 9.97. To reach 1000, you
double nine times, reaching 512, and then you need a little less than
one more doubling. So a logarithm need not be a whole number.

Asking "which space?" helps here too. Without `import math`, Python does
not know `math.log2` at all. The tools were there, but not in our space
until we asked.

### Your turn

1. Put 1 cent on the first square of a board, 2 cents on the next, 4 on
   the next, doubling each time. How many doublings until you reach
   €1,000,000, which is 100,000,000 cents? Use `math.log2`.
2. `math.log10` asks "how many times do I multiply by 10?". Before you
   run it, what do you think `math.log10(1000000)` gives?

```python exec
id: numbers-powers-your-turn
import math

print(math.log2(100000000))
```

## A calculator for splitting the bill

Four friends have a meal. The bill is €84, and they want to leave a 10%
tip and split it evenly. Here are the steps, in words:

1. Work out the tip: 10% of the bill.
2. Add it to the bill.
3. Divide by the number of people.
4. Round to the nearest cent.

As a formula, before rounding, with the tip as a percentage:

$$\text{share} = \frac{\text{total} \times \left(1 + \frac{\text{tip}}{100}\right)}{\text{people}}$$

Let's check that with the numbers. What do you expect?

```python exec
id: numbers-bill-1
print(84 * (1 + 10 / 100) / 4)
```

Each person pays €23.10. Now we want this as a function we can use again
with any bill. On the last page, a function showed steps with `print`.
This one needs to hand back a number, so that other code can use it.

```python exec
id: numbers-bill-2
def share_of(total, people):
    """Each person's part of a bill, with no tip."""
    return total / people

print(share_of(84, 4))
print(share_of(10, 4))
```

The *return* line hands a value back to whoever called the function.
`share_of(84, 4)` is replaced by 21.0, and `print` shows it. Words like
`def` and `return` are *keywords*: words Python keeps for its own use,
so you cannot use them as names.

The text in three quote marks, under the `def` line, is a *docstring*.
A docstring says what the function promises. Python does not check it;
it is there for people.

So how do we check that a function keeps its promise? With `assert`. An
*assert* statement checks that something is true. If it is true, nothing
happens at all. If it is false, Python stops with an error.

```python exec
id: numbers-bill-3
assert share_of(84, 4) == 21
assert share_of(10, 4) == 2.5
print("share_of keeps its promise.")
```

The `==` sign asks "are these equal?". It is different from `=`, which
makes a name point at a value.

The next cell tests for a wrong answer on purpose, so that you can see
what a failed test looks like. It is meant to stop with an error.

```python exec
id: numbers-bill-4
assert share_of(84, 4) == 20
```

Read the last line of the message: `AssertionError`. The line above it
shows which test failed. An error here is not a verdict on you. It is
information: this promise, on this line, was not kept. That is exactly
what a test is for.

### Your turn: your first toolkit function

The cell below is the start of `split_bill`, the first function in your
*toolkit*. Your toolkit is a set of functions you build across this
course. Later pages can use them without you writing them again.

Two lines have `...` where the working should go. Fill them in, then run
the cell.

- `tip_percent=0` gives the parameter a *default value*. If nobody says
  what the tip is, it is 0.
- `round(share, 2)` rounds to two decimal places, which is the nearest
  cent.

```python exec
id: numbers-toolkit
toolkit: yes
def split_bill(total, people, tip_percent=0):
    """Return each person's share of a bill, in euro, rounded to the cent.

    total is the bill before the tip, and people is how many are paying.
    tip_percent is the tip as a percentage, so 10 means 10%. With no
    tip_percent given, there is no tip.
    """
    with_tip = ...  # the bill, with the tip added
    share = ...     # one person's part of with_tip
    return round(share, 2)
```

```python toolkit-reference
for: numbers-toolkit
def split_bill(total, people, tip_percent=0):
    """Return each person's share of a bill, in euro, rounded to the cent.

    total is the bill before the tip, and people is how many are paying.
    tip_percent is the tip as a percentage, so 10 means 10%. With no
    tip_percent given, there is no tip.
    """
    with_tip = total * (1 + tip_percent / 100)
    share = with_tip / people
    return round(share, 2)
```

Now test it. Until both lines are filled in, this cell stops with an
error; that is the tests doing their job. Once it prints its message,
your `split_bill` keeps its promise.

```python exec
id: numbers-toolkit-tests
assert split_bill(84, 4) == 21.0
assert split_bill(84, 4, 10) == 23.1
assert split_bill(100, 3) == 33.33
assert split_bill(50, 1, 20) == 60.0
print("split_bill keeps its promise.")
```

```hint
Which line does the error point at, and what did you expect
`split_bill(84, 4)` to give? Try `print(split_bill(84, 4))` on its own
to see what your version gives now.
```

```hint
after: 10 errors
title: some steps
1. `with_tip` is the bill times $(1 + \frac{\text{tip}}{100})$. In
   Python, the tip is `tip_percent`, and the bill is `total`.
2. `share` is `with_tip` divided by `people`.
3. The formula is in the cell `numbers-bill-1`, with numbers in place of
   the names.

**Think about:** why does `100 / 3` need rounding, when `84 / 4` does
not?
```

A real calculator at a restaurant till would ask for the bill. Python
has a function for that, `input()`, which waits for someone to type.
Asking for a value is *input*, and showing a result is *output*.

```python
total = float(input("What is the bill? "))
print(split_bill(total, 4, 10))
```

There is no keyboard for the Python on this page to listen to, so here
we give values by editing the cell instead. `float()` turns the typed
text into a number, because whatever someone types arrives as a string.

<details class="dl-why"><summary>Why this way?</summary>

This page met logarithms as a question, "how many times do I multiply?",
and asked it about folded paper and octaves. A textbook usually meets
them much later, as rules: the logarithm of a product is the sum of the
logarithms, and so on.

The rules are useful. They let you work with logarithms on paper, and
exams often ask for them.

We started with the question because a rule means little until you know
what it is a rule about. Here a logarithm is a power, read backwards.
`math.log2` answers the question for us, and the next page uses the same
question to count the bits a number needs. The rules can come when a
page needs them.

</details>

## Four questions, looking back

| The question | On this page |
|---|---|
| What is named here? | the number families $\mathbb{N}$, $\mathbb{Z}$, $\mathbb{Q}$, $\mathbb{R}$; `int` and `float`; the toolkit function `split_bill` |
| What is promised? | `//` promises a whole number, `/` a float; `split_bill` promises each person's share, to the cent; `assert` checks a promise |
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
| power, `**` | $2^{10}$: 2 multiplied by itself 10 times |
| logarithm | how many times you multiply the base to reach a number: $\log_2 16 = 4$ |
| `return`, docstring, `assert` | hand back a value; the promise in words; a check that the promise is kept |
| `split_bill(total, people, tip_percent=0)` | your first toolkit function |
