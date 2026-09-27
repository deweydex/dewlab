---
title: "Coordinates: two lines at right angles"
year: "2026-2027"
version: 2026.09.27.2
worlds:
  numbers: Normal numbers, like 3 and 10.
  squiggles: Shapes like ♡ and △, which can stand for any number.
  letters: Letters like b and n, which can stand for any number.
---

# Coordinates: two lines at right angles

Here is a grid of small squares. One line goes across the bottom, and
one line goes up the left side. Each line has the numbers 0 to 6. The
two lines meet at 0, in the corner. Three dots are on the grid.

<img src="three-points.svg" alt="A grid of small squares. A line across the bottom is labelled 0 to 6, and a line up the left side is labelled 0 to 6. They meet at 0 in the bottom left corner. Three dots are labelled A, B and C. A is 2 squares across and 3 squares up. B is 5 squares across and 1 square up. C is on the left line, 4 squares up.">

```question
id: three-points-1
type: fill-in-the-blank

To reach A from 0, take
{2|3|5}
steps across.

Then take
{3|2|1}
steps up.
```

## Across, then up

Every dot on the grid can be found in the same way. Start at 0. Take
some steps across, and then some steps up.

```question
id: across-then-up-1
type: multiple-choice
answer: 1

Which of these takes you from 0 to B?

- 5 steps across, then 1 step up
  - B is above the 5 on the bottom line, one square up.
- 1 step across, then 5 steps up
  - This lands high on the left of the grid. B is low on the right.
- 5 steps across, and no steps up
  - That lands on the bottom line. B is one square above it.
```

## A dot on a line

```question
id: a-dot-on-a-line-1
type: fill-in-the-blank

To reach C, take
{0|4|1}
steps across.

Then take
{4|0|3}
steps up.

So C sits on the
{up line|across line}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Put your finger on 0, in the corner.
2. Is C to the right of the up line, or on it?
3. If it is on it, how many steps across does it need?

**Think about:** zero steps is a number of steps too.

**Try this next:** a dot is 3 steps across and 0 steps up. Which line
is it on?

</details>

## Two numbers for one place

We can write the place of A as two numbers in brackets: (2, 3). The
first number is the steps across. The second number is the steps up.

```question
id: two-numbers-for-one-place-1
type: fill-in-the-blank

B is at
{(5, 1)|(1, 5)|(5, 0)}.

C is at
{(0, 4)|(4, 0)|(4, 4)}.
```

## Does the order matter?

```question
id: does-the-order-matter-1
type: multiple-choice
answer: 1

Are (2, 3) and (3, 2) the same place?

- No, they are different places
  - (2, 3) is 2 across and 3 up. (3, 2) is 3 across and 2 up.
- Yes, they have the same two numbers
  - The two numbers are the same. But each one tells a different
    direction.
- Yes, because 2 + 3 and 3 + 2 are both 5
  - Both take 5 steps in total. The steps go in different directions.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Put your finger on 0. Take 2 steps across and 3 steps up. That is
   A.
2. Start at 0 again. Take 3 steps across and 2 steps up.
3. Is your finger on A now?

**Think about:** which number says "across", and which says "up".

**Try this next:** is (1, 5) the same place as (5, 1)?

</details>

The order matters. Across comes first, and up comes second. Choose
numbers, shapes or letters in the box under the title.

<div class="dl-world" data-world="numbers">

```question
id: does-the-order-matter-2--numbers
type: fill-in-the-blank

(4, 1) is 4 steps across and
{1|4}
step up.

(1, 4) is 1 step across and
{4|1}
steps up.

So (4, 1) and (1, 4) are
{different places|the same place}.
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: does-the-order-matter-2--squiggles
type: fill-in-the-blank

(♡, △) is ♡ steps across and
{△|♡}
steps up.

(△, ♡) is △ steps across and
{♡|△}
steps up.
```

</div>

<div class="dl-world" data-world="letters">

```question
id: does-the-order-matter-2--letters
type: fill-in-the-blank

(a, b) is a steps across and
{b|a}
steps up.

(b, a) is b steps across and
{a|b}
steps up.
```

</div>

The two places are the same only when the two numbers are the same,
like (4, 4). The heart and the triangle can be any numbers at all, and
this stays true.

## Why two lines?

The line across the bottom is a number line. The line up the side is a
number line too. They meet at 0, at a *right angle*. A right angle is
a square corner, like the corner of a page.

```question
id: why-two-lines-1
type: fill-in-the-blank

One number line gives a place on a line, with
{one|two|three}
number.

Two lines at right angles give a place on a page, with
{two|one|four}
numbers.
```

{{include: setup/zen-calm-check.md}}

## Below and to the left

On the page
[The number line: whole numbers, fractions and negatives](tutorial:the-number-line),
the line continued past 0, to the left. The negative numbers were
there. Here both lines continue past 0. The across line continues to
the left of 0. The up line continues below 0. Now 0 is in the middle.

<img src="four-corners.svg" alt="A grid from −5 to 5 across and from −5 to 5 up. The across line and the up line cross at 0, in the middle. Four dots are labelled A, B, C and D. A is 2 across and 3 up. B is 3 to the left and 2 up. C is 2 to the left and 3 down. D is 4 across and 1 down.">

A negative number of steps across goes to the left. A negative number
of steps up goes down.

```question
id: below-and-to-the-left-1
type: fill-in-the-blank

B is at (−3, 2). From 0, take 3 steps to the
{left|right}.

Then take 2 steps
{up|down}.
```

```question
id: below-and-to-the-left-2
type: fill-in-the-blank

C is 2 steps to the left of the up line. So its first number is
{−2|2|−3}.

C is 3 steps below the across line. So its second number is
{−3|3|−2}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Put your finger on 0, in the middle of the grid.
2. Move to the left along the across line, until you are straight
   above C. Count the steps. Steps to the left give a negative number.
3. Now move down to C. Count the steps. Steps down give a negative
   number too.

**Think about:** the across line and the up line are both number lines,
with negative numbers on one side of 0.

**Try this next:** which point is 3 steps to the left and 2 steps up?

</details>

```question
id: below-and-to-the-left-3
type: multiple-choice
answer: 1

Where is D?

- (4, −1)
  - D is 4 steps to the right, and 1 step down.
- (−1, 4)
  - That is 1 step to the left and 4 steps up. The across number
    comes first.
- (4, 1)
  - D is below the across line, so its up number is negative.
```

## The usual names

The across number is usually called *x*. The up number is usually
called *y*. The two numbers together are the *coordinates* of the
point. So the coordinates of A are (2, 3). Its x is 2, and its y is 3.

Each of the two number lines is called an *axis*. The across line is
the *x-axis*, and the up line is the *y-axis*.

```question
id: the-usual-names-1
type: fill-in-the-blank

The coordinates of D are (4, −1).

Its x is
{4|−1}.

Its y is
{−1|4}.
```

```question
id: the-usual-names-2
type: multiple-choice
answer: 1

A stretch, if you want one. A point is on the y-axis, the up line. What
is its x?

- 0
  - A point on the up line takes no steps across.
- The same as its y
  - That is true for some points, like (3, 3). They are not on the up
    line.
- 1
  - One step across moves the point off the up line.
```

## A grid you can change

The program below draws dots on a grid. The list `across` has the x of
each dot, and the list `up` has the y. The first dot uses the first
number of each list, so it is at (1, −2).

```python exec
id: a-grid-you-can-change-1
import matplotlib.pyplot as plt

across = [1, -4, 3]
up = [-2, 1, 3]

plt.figure(figsize=(4, 4))
plt.scatter(across, up, s=80)
plt.xticks(range(-6, 7))
plt.yticks(range(-6, 7))
plt.grid()
plt.axhline(0, color="black")
plt.axvline(0, color="black")
```

```predict
type: choice

Before you run it: the dots are at (1, −2), (−4, 1) and (3, 3). Which
dot will be below the across line?

- The dot at (1, −2)
  - Its up number is −2, so it is 2 steps down.
- The dot at (−4, 1)
  - It has a negative number, −4. That number is across, so it moves
    the dot to the left.
- The dot at (3, 3)
  - Both of its numbers are on the right of 0, so it is up and to the
    right.
```

The first line, `import`, gets the drawing tools ready. You do not need
to change it. Change the numbers in the two lists, and run it again.

- Can you put a dot at each of A, B, C and D from the picture?
- Can you put a dot in each corner of the grid?
- What happens if the two lists have a different number of numbers?

<details class="dl-answer"><summary>What each line does</summary>

- `across = [...]` and `up = [...]` are the x and the y of each dot.
- `plt.figure(figsize=(4, 4))` makes a square picture.
- `plt.scatter(...)` puts a dot at each place. `s=80` makes the dots
  big enough to see.
- `plt.xticks(...)` and `plt.yticks(...)` put a number on each line of
  the grid, from −6 to 6.
- `plt.grid()` draws the grid of squares.
- `plt.axhline(...)` draws the across line through 0 in black, and
  `plt.axvline(...)` draws the up line.

</details>

## Moving a point

Start at A, (2, 3). Move 4 steps to the left. Only the across number
changes. It goes from 2 to −2. So the new place is (−2, 3).

<div class="dl-world" data-world="numbers">

```question
id: moving-a-point-1--numbers
type: fill-in-the-blank

(2, 3) moved 5 steps down is
{(2, −2)|(−3, 3)|(2, 8)}.

(−3, 2) moved 4 steps to the right is
{(1, 2)|(−7, 2)|(−3, 6)}.
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: moving-a-point-1--squiggles
type: fill-in-the-blank

(♡, △) moved 1 step to the right is
{(♡ + 1, △)|(♡, △ + 1)|(♡ − 1, △)}.

(♡, △) moved 2 steps down is
{(♡, △ − 2)|(♡ − 2, △)|(♡, △ + 2)}.
```

</div>

<div class="dl-world" data-world="letters">

```question
id: moving-a-point-1--letters
type: fill-in-the-blank

(x, y) moved 1 step to the right is
{(x + 1, y)|(x, y + 1)|(x − 1, y)}.

(x, y) moved 2 steps down is
{(x, y − 2)|(x − 2, y)|(x, y + 2)}.
```

</div>

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. A move to the left or the right changes only the first number.
2. A move up or down changes only the second number.
3. Use the number line for the number that changes: to the right or up
   adds, and to the left or down takes away.

**Think about:** which of the two numbers each move changes.

**Try this next:** (4, −1) moved 3 steps up.

</details>

{{include: setup/zen-calm-check.md}}

## Your rule, in your words

Before you read our version, say in your own words how two numbers give
a place on a page. Write it in the Notes panel or on paper, or say it
aloud.

<details class="dl-answer"><summary>one way to say it</summary>

Two number lines meet at 0, at a square corner. A place on the page is
two numbers in brackets. The first says how far across: to the right,
or to the left if it is negative. The second says how far up: up, or
down if it is negative. The order matters, so (2, 3) and (3, 2) are
different places. The usual names for the two numbers are x and y. Your
way of saying it may be clearer than ours.

</details>

## Make your own

Can you make five coordinates problems of your own? Here are some
ideas:

- a point on the x-axis, and one on the y-axis
- a point with two negative numbers
- two points that swap their numbers, like (1, 6) and (6, 1)
- a move from one point to another
- a point with a fraction in it, like (1/2, 3)

## Looking back

Why do we need two numbers to give a place on a page, and only one to
give a place on a line?

A challenge: the program below joins five points in order, with a line
between each pair. It draws a square. The last point is the same as
the first, so the square closes. Can you move the square 3 steps to the
left? Can you draw a triangle? A house?

```python challenge
# Join the points in order, to draw a shape.
import matplotlib.pyplot as plt

across = [1, 4, 4, 1, 1]
up = [1, 1, 4, 4, 1]

plt.figure(figsize=(4, 4))
plt.plot(across, up, "o-")
plt.xticks(range(-6, 7))
plt.yticks(range(-6, 7))
plt.grid()
```

## Read more

Maths is Fun has a page on
[Cartesian coordinates](https://www.mathsisfun.com/data/cartesian-coordinates.html).
*Cartesian* is another name for the coordinates on this page. The page
has many points on grids, and a way to remember which number comes
first. The Simple English Wikipedia has a short page on the
[Cartesian coordinate system](https://simple.wikipedia.org/wiki/Cartesian_coordinate_system).
Both pages say the name comes from René Descartes, a French thinker.
