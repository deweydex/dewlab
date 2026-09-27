---
title: "Sides that never end: surds, the square root of 2"
year: "2026-2027"
version: 2026.09.27.1
worlds:
  numbers: Normal numbers, like 3 and 10.
  squiggles: Shapes like ♡ and △, which can stand for any number.
  letters: Letters like b and n, which can stand for any number.
---

# Sides that never end: surds, the square root of 2

Here are two grids of small squares. Inside each grid is a shaded
square, tilted on its corner. Its corners touch the middle of each side
of the grid. Look at the small grid on the left first.

<img src="tilted-squares.svg" alt="Two grids of small squares. On the left, a grid 2 squares by 2, labelled grid of 4. Inside it is a shaded square, tilted on its corner, labelled tilted square: 2. Each side of the tilted square goes from corner to corner across one small square. On the right, a grid 4 squares by 4, labelled grid of 16, with a bigger tilted square inside it, labelled tilted square: 8.">

```question
id: tilted-squares-1
type: multiple-choice
answer: 2

In the small grid, how much of each small square does the tilted
square cover?

- All of it
  - The tilted square does not reach the outside corners of the grid.
    Look at the four corners.
- Half of it
  - Each small square is cut in two by the side of the tilted square.
    One of the two halves is shaded.
- A quarter of it
  - Look at one small square at a time. The shaded part is one of two
    equal pieces.
- Three quarters of it
  - The line from corner to corner cuts a small square into two equal
    pieces, not four.
```

## Counting half squares

The tilted square covers half of each small square. There are 4 small
squares, so it covers 4 halves.

```question
id: counting-half-squares-1
type: fill-in-the-blank

4 halves make {2|4|8} whole small squares.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Two halves make one whole.
2. Put the 4 halves into pairs.
3. How many pairs are there?

**Think about:** this is the pizza idea again: 2 halves make 1.

**Try this next:** how many whole small squares do 8 halves make?

</details>

How much flat space a shape covers is called its *area*. We count it
in small squares. The small grid has an area of 4. The tilted square
has an area of 2. That is what its label says.

## A square with area 2

On [Undoing a square: square roots, the side of a square](tutorial:the-side-of-a-square),
a square of 9 beads had side(9) = 3. The tilted square is not made of
beads. But it is a square, and its area is 2. So the length of its side
is side(2).

Look at one side of the tilted square. It goes from one corner of a
small square to the opposite corner. A line like that is called a
*diagonal*.

```question
id: a-square-with-area-2-1
type: multiple-choice
answer: 3

How long is one side of the tilted square?

- 1 small square long
  - A square with side 1 has area 1 × 1 = 1. The tilted square has
    area 2.
- 2 small squares long
  - A square with side 2 has area 2 × 2 = 4. That is the whole grid.
- The diagonal of one small square
  - Each side goes corner to corner across one small square.
- Half a small square long
  - A diagonal is longer than the side of its small square, not shorter.
```

So side(2) is the diagonal of one small square.

## Between 1 and 2

How long is side(2), as a number? Here are two squares we know:

$$1 \times 1 = 1 \qquad 2 \times 2 = 4$$

```question
id: between-1-and-2-1
type: multiple-choice
answer: 4

What can we say about side(2)?

- It is 1
  - 1 × 1 is 1, not 2. A side of 1 makes a square that is too small.
- It is 2
  - 2 × 2 is 4, the whole grid. That is too big.
- It is 1.5
  - 1.5 is halfway between 1 and 2. Try 1.5 × 1.5: it is 2.25, a
    little too big.
- It is between 1 and 2
  - 1 × 1 is too small, and 2 × 2 is too big. So side(2) is somewhere
    between.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. side(2) is the number that, times itself, makes 2.
2. 1 × 1 = 1. Is that more or less than 2?
3. 2 × 2 = 4. Is that more or less than 2?

**Think about:** on the last page, side(10) was between 3 and 4 in the
same way.

**Try this next:** between which two whole numbers is side(5)?

</details>

## Guess and check

side(2) is more than 1 and less than 2. Let's guess a decimal, like
1.4, and check it. A decimal is a number with a point in it. A *digit*
is one of the signs 0 to 9.

$$1.4 \times 1.4 = 1.96 \qquad 1.41 \times 1.41 = 1.9881$$

Both are a little less than 2. Each extra digit brings us closer. The
cell below checks a guess for you. The first line gets Python's
`Decimal` tool ready. It multiplies decimals exactly, the way you would
on paper. The quotes keep the digits exactly as you wrote them.

```python exec
id: guess-and-check-1
hint: 1.41 × 1.41 was 1.9881. Will a guess a little bigger go past 2? Make a guess now, or run the cell and see.
from decimal import Decimal

guess = Decimal("1.414")
print(guess * guess)
```

```predict
type: choice

Before you run it: what is 1.414 × 1.414?

- A little less than 2
  - 1.41 was a little less than 2, and 1.414 is only a little bigger.
- Exactly 2
  - Three digits after the point feels like enough to be exact.
- A little more than 2
  - 1.414 is bigger than 1.41, so it might go past 2.
```

Now change the guess and run it again. Try 1.4142. Try 1.415.

```question
id: guess-and-check-2
type: fill-in-the-blank

1.414 × 1.414 = 1.999396. So side(2) is more than {1.414|1.415|2}.

1.415 × 1.415 = 2.002225. So side(2) is less than {1.415|1.414|1}.
```

{{include: setup/zen-calm-check.md}}

## One more digit each time

Guessing by hand gets slow. This cell guesses for us. It finds one more
digit each time round the loop. For each place after the point, it
tries adding 1 to that digit, again and again. It stops when one more
would make the square bigger than the area.

```python exec
id: one-more-digit-each-time-1
hint: So far the digits are 1.414. Will they continue 1.41414…, or do something else? Make a guess now, or run the cell and see.
from decimal import Decimal

area = 2
side = Decimal(0)
step = Decimal(1)
for places in range(0, 21):
    while (side + step) * (side + step) <= area:
        side = side + step
    print(round(side, places))
    step = step / 10
```

```predict
type: choice

Before you run it: the cell finds side(2) to 20 places after the point.
What will the digits do?

- They will stop after a few digits
  - 1/4 is 0.25, and its digits stop. Some numbers do that.
- They will repeat a pattern, over and over
  - 1/3 is 0.333…, and its 3s repeat forever. Some numbers do that.
- They will not stop, and will not repeat
  - Each new place has a new digit, with no pattern.
```

The digits do not stop. They do not repeat a pattern either. The cell
stops at 20 places only because we told it to. Change `range(0, 21)`
to `range(0, 31)`, and it finds 30.

<details class="dl-answer"><summary>What each line does</summary>

- `area = 2` is the area of the square. We want its side.
- `side` starts at 0. `step` starts at 1, then becomes 0.1, then 0.01,
  and so on. Each step is one place further after the point.
- `while ... <= area:` adds one step to the side, again and again,
  while the square of the next guess is still no bigger than the area.
- `print(round(side, places))` shows the side with that many places
  after the point.
- `step = step / 10` moves one place further along.

</details>

The digits of side(2) never stop, and never repeat. No fraction can
ever equal side(2), however big its top and bottom are. People proved
this long ago.

```question
id: one-more-digit-each-time-2
type: multiple-choice
answer: 2

The cell found 1.4142135623 at 10 places. Is that exactly side(2)?

- Yes, ten places is exact
  - Ten places is very close. But the cell kept finding new digits
    after it.
- No, its square is a tiny bit less than 2
  - 1.4142135623 × 1.4142135623 is about 1.9999999998. The next
    digits add a tiny bit more.
- No, its square is a tiny bit more than 2
  - The cell only adds to a digit while the square stays at 2 or
    less. So it is never more than 2.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Look at the line after 1.4142135623 in the output.
2. Did the cell find more digits after it?
3. If more digits were still needed, was 1.4142135623 too big or too
   small?

**Think about:** the cell adds to a digit only while the square stays
at 2 or below.

**Try this next:** change the guess in the first cell to 1.4142135623,
and run it.

</details>

## A bigger tilted square

Now look at the grid on the right. It is 4 small squares by 4, and its
tilted square is bigger.

```question
id: a-bigger-tilted-square-1
type: fill-in-the-blank

The grid has 16 small squares. The tilted square covers half the grid.
So its area is {8|4|16}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Count the small squares in the grid on the right: 4 rows of 4.
2. The tilted square covers half of the grid, as in the small grid.
3. What is half of 16?

**Think about:** in the small grid, the tilted square was half of 4.

**Try this next:** a grid 6 by 6. What is the area of its tilted
square?

</details>

The tilted square has area 8, so its side is side(8).

## Two diagonals long

Look at one side of the big tilted square. It crosses 2 small squares,
corner to corner. So it is 2 diagonals long. One diagonal is side(2).
So

$$\text{side}(8) = 2 \times \text{side}(2)$$

```question
id: two-diagonals-long-1
type: fill-in-the-blank

side(2) is about 1.414. So side(8) is about {2.828|1.414|4}.
```

Let's check it with the machine. Return to the cell under "One more
digit each time". Change `area = 2` to `area = 8`, and run it. Then compare with $2 \times \text{side}(2)$
below. We copied the 20 places of side(2) from the first run.

```python exec
id: two-diagonals-long-2
from decimal import Decimal

print(2 * Decimal("1.41421356237309504880"))
```

Both give 2.82842712474619009760. So side(8) is two side(2)s, to 20
places.

## More tilted squares

The same idea works for bigger grids. A grid of 6 by 6 has a tilted
square of area 18. Each side of it crosses 3 small squares, so
side(18) = 3 × side(2). And $18 = 2 \times 3 \times 3$.

<div class="dl-world" data-world="numbers">

```question
id: more-tilted-squares-1--numbers
type: fill-in-the-blank

side(2 × 10 × 10) = {10|100|20} × side(2)
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: more-tilted-squares-1--squiggles
type: fill-in-the-blank

side(2 × ♡ × ♡) = {♡|♡ × ♡|2 × ♡} × side(2)
```

</div>

<div class="dl-world" data-world="letters">

```question
id: more-tilted-squares-1--letters
type: fill-in-the-blank

side(2 × k × k) = {k|k × k|2k} × side(2)
```

</div>

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. side(8) is side(2 × 2 × 2), and it is 2 × side(2).
2. side(18) is side(2 × 3 × 3), and it is 3 × side(2).
3. What stays the same, and what changes?

**Think about:** the heart, or the letter, could be any number at all.
The pattern still holds.

**Try this next:** use the cell to find side(200). Which digits do you
see?

</details>

{{include: setup/zen-calm-check.md}}

## Your rule, in your words

Before you read our version, say what you found about side(2) in your
own words. Write it in the Notes panel or on paper, or say it aloud.

<details class="dl-answer"><summary>one way to say it</summary>

side(2) is the diagonal of a small square. It is between 1 and 2. Its
digits never stop, and they never repeat a pattern, so no fraction is
ever exactly side(2). A square of area 8 has a side of two diagonals:
side(8) = 2 × side(2). Your way of saying it may be clearer than ours.

</details>

## The usual way to write it

On the last page, side(49) had a sign: $\sqrt{49}$, "the square root
of 49". side(2) is written the same way:

$$\text{side}(2) = \sqrt{2} \qquad \text{side}(8) = \sqrt{8}$$

√2 means exactly the same as side(2). What we found about side(8) looks
like this with the sign:

$$\sqrt{8} = 2\sqrt{2}$$

A number written next to √2 means "times", so $2\sqrt{2}$ is
$2 \times \sqrt{2}$. You can keep writing side(2) when that feels
calmer. They mean the same thing.

Python has a short way to find side(2) too. It writes `2 ** 0.5`: 2 to
the power of 0.5. The next page, on halfway powers, shows why a power
of 0.5 finds the side.

```python exec
id: the-usual-way-to-write-it-1
print(2 ** 0.5)
print(8 ** 0.5)
print(2 * 2 ** 0.5)
```

Python's normal numbers keep only about 16 digits. So the last digit of
each line is a little off from the 20 places we found.

```question
id: the-usual-way-to-write-it-2
type: fill-in-the-blank

√2 means {side(2)|2 × 2|2 ÷ 2}.

√18 = {3|9|6} × √2
```

Last of all, a word. A number like side(2), whose digits never end and
never repeat, is called a *surd*. Many people find the word scary. On
this page, you found one, and measured it to 20 places.

The word is very old. About 1200 years ago, the mathematician
al-Khwarizmi called numbers like this "inaudible", which means "cannot
be heard". Later, the Arabic word for these numbers meant "deaf".
People translated that word into Latin as *surdus*, which also means
"deaf". *Surd* comes from *surdus*.

## Make your own

Can you make five problems of your own, and find each answer? Here are
some ideas:

- the side of a tilted square in a grid 10 by 10
- side(…) of a number that is 2 times a square number
- side(3) or side(5), to 10 places, with the cell
- side(2 × ♡ × ♡), with a shape of your choice

Which of your problems looks scary, but is simple?

## Looking back

side(9) is a whole number, and side(2) never ends. What is different
about the two squares?

A challenge: the program below finds side(3). Which numbers from 1 to
20 have a side whose digits stop? (Stop means that after a while, every
new digit is 0.) Some decimals have a side that stops too. For 1.44,
write `area = Decimal("1.44")`, and the side is 1.2. Can you find
another?

```python challenge
# Find side(area), one more digit each time.
from decimal import Decimal

area = 3
side = Decimal(0)
step = Decimal(1)
for places in range(0, 21):
    while (side + step) * (side + step) <= area:
        side = side + step
    print(round(side, places))
    step = step / 10
```

## Read more

About 3,700 years ago, a student in Mesopotamia drew a square and its
two diagonals on a clay tablet. On one diagonal, they wrote side(2) in
their own number signs. It matches our digits as far as 1.41421. Wikipedia's page on the tablet,
[YBC 7289](https://en.wikipedia.org/wiki/YBC_7289), has a photo. Its
page on the [square root of 2](https://en.wikipedia.org/wiki/Square_root_of_2)
says much more about this number.
