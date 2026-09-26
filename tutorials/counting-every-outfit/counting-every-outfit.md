---
title: "Counting every outfit: lists of outcomes"
year: "2026-2027"
version: 2026.09.25.1
covers:
  every-outfit-one-by-one:
    covers: [MIT-5.1]
    touches: [PDP-LO6]
  outcomes-of-an-experiment:
    covers: [MIT-5.1]
  the-counting-principle:
    covers: [MIT-5.2]
  a-tool-that-lists-every-pair:
    covers: [MIT-5.1, MIT-5.2]
  every-pixel-every-colour:
    covers: [MIT-5.1, MIT-5.2]
    touches: [MIT-1.4]
  and-multiplies-or-adds:
    covers: [MIT-5.2]
  too-many-to-list-pins-and-passwords:
    covers: [MIT-5.2]
    touches: [MIT-1.1]
---

# Counting every outfit: lists of outcomes

You have three tops, two pairs of trousers and two pairs of shoes. How
many different outfits can you put together? You could try them all on.
You could write them all down. Or you could find a way to count them
without doing either.

That last way is worth having. How many colours can a screen show? How
many passwords would a thief have to try? Each is the outfit question
with bigger numbers, far too big to list, and by the end of this page
you will count them anyway.

On this page we:

- list every outfit, with one loop inside another
- meet experiments, outcomes, and the list of every outcome
- find the counting principle, and check it against the list
- add `all_pairs` to your toolkit, and list every pixel and colour
- count PINs and passwords, far too many to list

> **The space we're in.** Choices that do not change each other.
> Whichever top you pick, both pairs of trousers are still there. Every
> list on this page is finite: it ends, so a loop can reach every item
> in it. The next page, [Orders and choices](tutorial:orders-and-choices),
> is about choices that do change each other.

## Warm-up

Two questions from earlier pages. The first is from
[Doing it again](tutorial:doing-it-again), and the second from
[True, false and every case](tutorial:true-false-and-every-case).

```question
id: counting-every-warm-up-1
type: fill-in-the-blank

`total([3, 2, 2])` gives {7}, and `product([3, 2, 2])` gives {12}.
```

```question
id: counting-every-warm-up-2
type: multiple-choice
answer: 3

A rule has three True/False inputs. How many rows does its truth table
have?

- 3
  - This counts the inputs, not the ways they can be set.
- 6
  - This is 3 × 2, one row per input and value.
- 8
  - Each input is True or False: 2 × 2 × 2.
- 9
  - This is 3 × 3.
```

## Every outfit, one by one

Let's start smaller: three tops and two pairs of trousers. Each outfit
is one top with one pair of trousers. How many outfits is that? Guess
before you run the cell.

```python exec
id: counting-every-outfits-1
tops = ["white shirt", "blue T-shirt", "red jumper"]
trousers = ["jeans", "black trousers"]

for top in tops:
    for legs in trousers:
        print(top, "with", legs)
```

Six outfits. This is one loop inside another, the same shape as the
truth tables on
[True, false and every case](tutorial:true-false-and-every-case). Here
is what happens when:

1. The outer loop picks the first top, the white shirt.
2. The inner loop runs all the way through the trousers: jeans, then
   black trousers.
3. The outer loop picks the next top, and the inner loop runs all the
   way through the trousers again.
4. This happens once for each top.

So each top appears twice, once with each pair of trousers. A drawing
of this is called a *tree diagram*: one branch for each first choice,
and each branch splits into one twig for each second choice.

```text
white shirt  ── jeans
             └─ black trousers
blue T-shirt ── jeans
             └─ black trousers
red jumper   ── jeans
             └─ black trousers
```

Count the ends of the twigs, and you have counted the outfits: 6.

### Your turn

1. Add a fourth top to the list `tops`, and predict the new number of
   outfits before you run it.
2. Swap the two `for` lines, so that the trousers loop is on the
   outside. Does the number of outfits change? Does the order of the
   lines change?

## Outcomes of an experiment

Picking an outfit is one example of something maths has a general name
for. An *experiment* is any action that can end in more than one way:
tossing a coin, rolling a die, picking an outfit, drawing a raffle
ticket. An *outcome* is one way it can end. The *sample space* is the
list of every outcome, with none left out and none written twice.

Maths writes a sample space in curly brackets. For one roll of a die:

$$S = \{1, 2, 3, 4, 5, 6\}$$

The curly brackets mark a collection where only what is in it matters,
not the order. Unit 5 has much more about them. In Python, a list does
the job for us.

Now a bigger experiment: toss a coin, and roll a die. One outcome is
"heads, and a 4". We can write it as a *pair*: two values in round
brackets, in a fixed order, like `("H", 4)`. A pair is a tuple with two
values in it. You met tuples on
[Untangling a condition](tutorial:untangling-a-condition#checking-every-row-with-one-function).

The cell builds the sample space as a list, adding one pair at a time
with `append`, the way `truth_table` built its results. How many
outcomes will it find?

```python exec
id: counting-every-outcomes-1
coin = ["H", "T"]
die = [1, 2, 3, 4, 5, 6]

outcomes = []
for side in coin:
    for roll in die:
        outcomes.append((side, roll))

print(outcomes)
print(len(outcomes), "outcomes")
```

Twelve outcomes, from `('H', 1)` to `('T', 6)`. The list starts empty,
and each time round the inner loop, one more pair goes on the end.
Listing every outcome like this is where all counting begins: once the
list is right, counting it is only `len()`.

### Your turn

Now toss two coins: a 10c coin and a 20c coin.

1. On paper, write every outcome. Is "heads on the 10c, tails on the
   20c" the same outcome as "tails on the 10c, heads on the 20c"?
2. Change the cell above so that it lists the outcomes for two coins,
   and check your list.

## The counting principle

Let's put the counts side by side.

| Experiment | First choice | Second choice | Outcomes |
|---|---|---|---|
| top, then trousers | 3 | 2 | 6 |
| coin, then die | 2 | 6 | 12 |
| two coins | 2 | 2 | 4 |

Every time, the number of outcomes is the first number times the
second. That makes sense from the tree diagram. Each of the first
choices is a branch, and every branch has the same number of twigs.

This is the *fundamental principle of counting*, often called the
counting principle. In words: if one choice can be made in $m$ ways,
and then a second choice in $n$ ways, whatever the first choice was,
then the two together can be made in $m \times n$ ways. In symbols:

$$\text{outcomes} = m \times n$$

It works for more choices too. Three choices in $m$, $n$ and $p$ ways
make $m \times n \times p$ outcomes. That is a product, so your toolkit
tool `product` can do it.

Let's check the principle on the full wardrobe, with shoes as well. The
loop counts every outfit, one by one. The last two lines use the
principle. Do you expect the three numbers to agree?

```python exec
id: counting-every-principle-1
tops = ["white shirt", "blue T-shirt", "red jumper"]
trousers = ["jeans", "black trousers"]
shoes = ["runners", "boots"]

outfits = 0
for top in tops:
    for legs in trousers:
        for feet in shoes:
            outfits = outfits + 1

print(outfits)
print(len(tops) * len(trousers) * len(shoes))
print(product([len(tops), len(trousers), len(shoes)]))
```

All three say 12. The loop is the proof: it met every outfit. The
formula is the fast way, and it agrees.

Look back at the warm-up. A truth table with three inputs has 8 rows,
because each input is a choice of 2: $2 \times 2 \times 2 = 2^3$. The
$2^n$ rows on that page were the counting principle all along. So were
the 128 patterns of a seven-segment display on
[Numbers a computer can hold](tutorial:numbers-a-computer-can-hold#powers-and-how-many-times):
seven segments, each a choice of on or off, make $2^7$.

```question
id: counting-every-principle-2
type: fill-in-the-blank

A laptop comes with 4 screen sizes, 3 amounts of memory and 2 colours.
Each laptop is one of each, so there are {24} different laptops.
```

## A tool that lists every pair

We have written "a loop inside a loop, adding each pair to a list" three
times now. Let's make it a tool.

`all_pairs(first, second)` promises every pair `(a, b)`, with `a` from
`first` and `b` from `second`, as a list of tuples. The pairs come in
the same order as our loops made them: every pair with the first value
of `first`, then every pair with the second, and so on.

The cell below is a stub: only the promise is written. Write the body
yourself. The cell `counting-every-outcomes-1` has the shape you need.

```python exec
id: counting-every-toolkit
toolkit: yes
def all_pairs(first, second):
    """Return every pair (a, b) with a from first and b from second.

    The result is a list of tuples. All the pairs with the first value
    of first come first, then all the pairs with the next, and so on.
    all_pairs(["H", "T"], [1, 2]) is
    [("H", 1), ("H", 2), ("T", 1), ("T", 2)].
    """
    ...
```

```python toolkit-reference
for: counting-every-toolkit
def all_pairs(first, second):
    """Return every pair (a, b) with a from first and b from second.

    The result is a list of tuples. All the pairs with the first value
    of first come first, then all the pairs with the next, and so on.
    all_pairs(["H", "T"], [1, 2]) is
    [("H", 1), ("H", 2), ("T", 1), ("T", 2)].
    """
    pairs = []
    for a in first:
        for b in second:
            pairs.append((a, b))
    return pairs
```

Run the toolkit cell, then the tests. Until the body is written,
`all_pairs` gives back nothing at all, `None`, so expect the first test
to stop with an `AssertionError`.

```python exec
id: counting-every-toolkit-tests
assert all_pairs(["H", "T"], [1, 2]) == [("H", 1), ("H", 2), ("T", 1), ("T", 2)]
assert len(all_pairs(tops, trousers)) == len(tops) * len(trousers)
assert len(all_pairs(range(10), range(10))) == 100
assert all_pairs([], [1, 2, 3]) == []          # no first choice: 0 × 3 = 0
print("all_pairs keeps its promise.")
```

```hint
Which test does the error point at? Try
`print(all_pairs(["H", "T"], [1, 2]))` on its own. What does your
version give?
```

```hint
after: 12 errors
title: some steps
1. Start with an empty list, `pairs = []`.
2. A loop over `first`, and inside it a loop over `second`.
3. Inside both loops, `pairs.append((a, b))`. Note the two sets of
   round brackets: one for `append`, one for the pair.
4. After both loops, and not inside them, `return pairs`.

**Think about:** why does the last test give an empty list, and why is
that the answer we want?
```

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Yours may be different and still do the same job.

```python
def all_pairs(first, second):
    pairs = []
    for a in first:
        for b in second:
            pairs.append((a, b))
    return pairs
```

</details>

The second test is the counting principle, written as a test. The cells
from here on use `all_pairs`. If you have not written it yet, copy the
answer above into the stub and run it.

A pair can itself go into a pair. What do you think this cell prints
last?

```python exec
id: counting-every-toolkit-2
outfits = all_pairs(all_pairs(tops, trousers), shoes)
print(outfits[0])
print(len(outfits))
```

The first outfit is `(('white shirt', 'jeans'), 'runners')`: a top and
trousers, paired with shoes. There are 12 of them, $6 \times 2$. Three
choices are two choices, where the first choice is itself a pair.

## Every pixel, every colour

Each pixel on a screen has a column and a row, so a screen is
`all_pairs` of its columns and its rows. Here is a tiny one, 4 pixels
wide and 3 tall. How many pixels, and which comes last?

```python exec
id: counting-every-pixels-1
pixels = all_pairs(range(4), range(3))
print(pixels)
print(len(pixels), "pixels")
```

Twelve pixels, from `(0, 0)` to `(3, 2)`. A grid is the counting
principle drawn as a rectangle. A common laptop screen is
1920 pixels wide and 1080 tall, so it has $1920 \times 1080 =
2{,}073{,}600$ pixels.

Each pixel mixes red, green and blue light, as on
[Everything is ones and zeros](tutorial:everything-is-ones-and-zeros#how-ff8800-makes-orange).
Let's pair four levels of red with four of green, blue off, and draw
every mix. Guess first: how many squares, and what
colour is the corner where both are full?

```python exec
id: counting-every-colours-1
import matplotlib.pyplot as plt

levels = [0, 85, 170, 255]
mixes = all_pairs(levels, levels)

figure, grid = plt.subplots(figsize=(3, 3))
for red, green in mixes:
    square = plt.Rectangle((green, red), 85, 85, color=(red / 255, green / 255, 0))
    grid.add_patch(square)
grid.set_xlim(0, 340)
grid.set_ylim(0, 340)
grid.set_xlabel("green")
grid.set_ylabel("red")
print(len(mixes), "mixes")
```

Sixteen squares, $4 \times 4$, from black in one corner to yellow in
the other: full red and full green light together look yellow. A real
screen has 256 levels of each colour, not 4, and blue as well:
$256 \times 256 \times 256 = 16{,}777{,}216$ colours for every pixel.

<aside class="dl-note" id="counting-every-note-colour">

**Why 256?** Each of red, green and blue is stored in 8 bits, and 8
bits hold $2^8 = 256$ values. Three of them make 24 bits a pixel, often
called "24-bit colour".

</aside>

## And multiplies, or adds

A game lets you build a team of one robot and one pet. There are 3
robots and 4 pets. By the counting principle, that is $3 \times 4 = 12$
teams.

Another game lets you play as a robot or as a pet, not both. How many
choices now?

```question
id: counting-every-or-1
type: multiple-choice
answer: 1

You can play as one of 3 robots, or one of 4 pets, but not both. How
many different choices is that?

- 7
  - One choice from the robots or one from the pets: 3 + 4.
- 12
  - Multiplying counts a robot and a pet together, which the game does not allow.
- 1
  - This counts the one choice you make, not the choices on offer.
```

Seven. Each choice is one robot or one pet, so we list the robots, then
the pets, and count them all: $3 + 4$. When the choices are
made one after the other, "this and then that", the counts multiply.
When you make only one choice, from one group or the other, the counts
add. The two groups must not share anything, or some choices would be
counted twice.

## Too many to list: PINs and passwords

A bank card has a four-digit PIN. Each digit is a choice of 10, from 0
to 9, and each choice does not change the others. By the counting
principle:

$$10 \times 10 \times 10 \times 10 = 10^4 = 10{,}000 \text{ PINs}$$

Let's prove it by listing. Four nested loops would work, but there is a
shorter route: every PIN from 0000 to 9999 is a whole number from 0 to
9999, with zeros in front. `format(pin, "04")` writes a number with at
least four digits, the way `format(n, "08b")` did on
[Bits that flip](tutorial:bits-that-flip). What do the first and last
lines print?

```python exec
id: counting-every-pins-1
pins = []
for pin in range(10000):
    pins.append(format(pin, "04"))

print(pins[0], pins[1], pins[-1])
print(len(pins), 10 ** 4)
```

The first PIN is `0000`, the second `0001`, and the last `9999`. The
list has 10,000 of them, the same as $10^4$. (`pins[-1]` is the last
item in a list.) Someone who guesses a PIN at random has 1 chance in
10,000 of being right. That is why a card locks after three wrong
guesses.

A password is the same kind of count, with bigger numbers. A password
of 8 small letters has 26 choices for each letter, so there are $26^8$
passwords. Which do you think makes more passwords: 8 characters from
small letters, capitals and digits (62 choices each), or 12 small
letters only? Guess, then run it.

```python exec
id: counting-every-passwords-1
print(26 ** 8)
print(62 ** 8)
print(26 ** 12)
```

Twelve small letters win by a long way: 95,428,956,661,682,176
passwords, more than 400 times as many as 8 characters with capitals
and digits. Length beats variety. I find that the nicest surprise on
the page: the plain, long password wins. Say an attacker's
computer can try a billion passwords a second. It would try every 8-letter password in about three
and a half minutes, every 8-character mixed one in about two and a half
days, and every 12-letter one in about three years.

<aside class="dl-note" id="counting-every-note-guesses">

**A billion a second is slow.** In 2012, the researcher Jeremi Gosney
showed a machine of 25 graphics cards that tried about 348 billion
guesses a second, against one common way that Windows stored
passwords.

</aside>

Nobody can list $26^{12}$ passwords to check that count: a loop would
run for years. We trust the formula here because we have checked it
against the loop on every list small enough to finish. The loop is the
proof, and the formula is how we go further than the loop can reach.

### Your turn

1. Some phones use a six-digit PIN. How many are there? Work it out
   with the counting principle first, then check with Python.
2. A lock has three wheels, each with the digits 0 to 9. Make a list of
   every code with `all_pairs`, or with loops, and check its length.
3. Which adds more passwords: one more character of small letters, or
   allowing capitals as well? Try both on an 8-letter password.

```python exec
id: counting-every-your-turn
# Your PIN and lock counts here
```

<details class="dl-why"><summary>Why this way?</summary>

We counted every outfit with a loop before we gave you the formula. Most
textbooks do it the other way round: the counting principle first,
$m \times n$, and then examples that use it.

Formula first is quicker. A reader who is comfortable with symbols can
start using it at once.

We listed first because a formula is a promise, and a list is how we
check it. The loop met every outfit, so its count cannot be wrong, and
$m \times n$ agreed with it. For $26^{12}$ passwords no loop could
finish, and there we trust the formula because we checked it everywhere
we could. A formula you have tested is one you can believe, not only
remember.

</details>

## Four questions, looking back

| The question | On this page |
|---|---|
| What is named here? | each outcome, as a pair like `("H", 4)` or a pixel's `(column, row)`; the sample space $S$; `all_pairs` |
| What is promised? | the counting principle promises $m \times n$ outcomes for two choices that do not change each other; `all_pairs` promises every pair, in order |
| What happens when? | the inner loop runs all the way through for each value of the outer loop, so each first choice meets every second choice |
| What does this space let us do? | choices that do not change each other, and finite lists; "and" multiplies and "or" adds; lists too long to write, which the formula still counts |

## What we have now

| Term or tool | What it means |
|---|---|
| experiment | an action that can end in more than one way |
| outcome | one way an experiment can end |
| sample space, $S$ | the list of every outcome, none left out and none twice |
| tree diagram | a drawing with a branch for each first choice, and a twig for each second choice |
| pair | two values in round brackets, in order: `("H", 4)` |
| counting principle | $m$ ways, then $n$ ways, makes $m \times n$ ways |
| and, or | choices made one after the other multiply; one choice from two separate groups adds |
| `format(n, "04")` | `n` written with at least four digits, zeros in front |
| `all_pairs(first, second)` | your toolkit tool: every pair, as a list of tuples |

The practice page is next. After it,
[Orders and choices](tutorial:orders-and-choices) counts the ways to
arrange things, where each choice leaves one fewer for the next.

For another route through counting, the integrated course has
[Counting: factorials, permutations and combinations](tutorial:counting-carefully).

## Where to read more

Stand-up Maths (2025). *The fewest items of clothes to never repeat an
outfit.* <https://www.youtube.com/watch?v=yoR2obq4YUw>. How few clothes do
you need to wear a different outfit every day of the year? Matt Parker
answers it with the counting principle from this page, and then buys the
clothes. About seventeen minutes.
