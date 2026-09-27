---
title: "Undoing a square: square roots, the side of a square"
year: "2026-2027"
version: 2026.09.27.1
worlds:
  numbers: Normal numbers, like 3 and 10.
  squiggles: Shapes like ♡ and △, which can stand for any number.
  letters: Letters like b and n, which can stand for any number.
---

# Undoing a square: square roots, the side of a square

Here are some beads, laid out in squares. Under each square is the
number of beads in it, and the number of beads along one side.

<img src="bead-squares.svg" alt="Five squares of beads, from small to big. A single bead, labelled 1 bead, side 1. A square of 2 rows of 2, labelled 4 beads, side 2. A square of 3 rows of 3, labelled 9 beads, side 3. A square of 4 rows of 4, labelled 16 beads, side 4. A square of 5 rows of 5, labelled 25 beads, side 5.">

```question
id: bead-squares-1
type: multiple-choice
answer: 2

The next square would have 6 beads along each side. How many beads
would it have?

- 12
  - That is 6 + 6, two sides of the square. The square has beads in
    the middle too.
- 36
  - 6 rows, with 6 beads in each row: 6 × 6 = 36.
- 24
  - That is 4 × 6, the beads around the outside. The middle is full
    of beads too.
- 30
  - That is 25 + 5, one more row on the last square. A bigger square
    needs one more row and one more column.
```

## Which numbers make a square?

Some numbers of beads make a square. A square has the same number of
beads in every row and in every column, with none left over. Other
numbers of beads do not make a square.

```question
id: which-numbers-make-a-square-1
type: multiple-choice
answer: 3

Which of these numbers of beads makes a square?

- 12
  - 3 rows of 4 is 12. That is a rectangle, not a square: the rows are
    longer than the columns.
- 20
  - 4 rows of 5 is 20, a rectangle. 4 rows of 4 is only 16, and 5 rows
    of 5 is 25.
- 16
  - 4 rows, with 4 beads in each row.
- 8
  - 2 rows of 4 is 8, a rectangle. 3 rows of 3 needs 9 beads.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Look at the picture again. Which numbers of beads are there?
2. Write them down: 1, 4, 9, 16, 25.
3. Is any of the four choices in your list?

**Think about:** a square has the same number of rows as columns.

**Try this next:** can 7 beads make a square?

</details>

Numbers like 1, 4, 9, 16 and 25 are called *square numbers*. A square
number of beads makes a square, with no beads left over.

```question
id: which-numbers-make-a-square-2
type: fill-in-the-blank

The square number after 25 is {36|30|26}.

The square number after that is {49|42|37}.
```

## The side of a square

A square of 9 beads has 3 beads along each side. We call that its
*side*. We write it like this:

$$\text{side}(9) = 3$$

Say it aloud as "the side of 9 is 3". The number in the brackets is the
beads. The answer is the number along one side.

```question
id: the-side-of-a-square-1
type: fill-in-the-blank

side(16) = {4|8|2}

side(25) = {5|12.5|10}

side(49) = {7|24.5|14}
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. side(16) asks: a square of 16 beads has how many beads along one
   side?
2. Look at the picture. Find the square labelled 16 beads.
3. For 49, there is no picture. Try some numbers: 5 × 5, 6 × 6, 7 × 7.

**Think about:** which number, times itself, makes the beads.

**Try this next:** side(64).

</details>

## Undoing a square

On [Powers: the long way and the short way](tutorial:the-long-way),
the golden beads had a square of 100 beads: $10 \times 10 = 10^2$. A
square of beads is always a number times itself. That is a power with
exponent 2:

$$3 \times 3 = 3^2 = 9$$

side(…) goes the other way. It starts with the beads, and finds the
number we multiplied. So side(9) = 3.

$$3 \quad \xrightarrow{\text{square it}} \quad 9 \quad \xrightarrow{\text{side}} \quad 3$$

Squaring a number, then taking the side, returns the number we started
with. side(…) *undoes* the square. Choose numbers, shapes or letters in
the box under the title. The pattern is the same in each.

<div class="dl-world" data-world="numbers">

```question
id: undoing-a-square-1--numbers
type: fill-in-the-blank

side(8 × 8) = {8|64|16}

side(10²) = {10|100|20}
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: undoing-a-square-1--squiggles
type: fill-in-the-blank

side(♡ × ♡) = {♡|♡ × ♡|2 × ♡}

side(△²) = {△|△ × △|2 × △}
```

</div>

<div class="dl-world" data-world="letters">

```question
id: undoing-a-square-1--letters
type: fill-in-the-blank

side(b × b) = {b|b × b|2b}

side(n²) = {n|n × n|2n}
```

</div>

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Picture a square with the same number of rows and columns.
2. The thing in the brackets is the number of beads: rows times
   columns.
3. side(…) asks how many beads are along one side.

**Think about:** the heart, or the letter, could be any number at all.
The pattern still holds. That is all a letter in algebra means.

**Try this next:** side(1000 × 1000).

</details>

{{include: setup/zen-calm-check.md}}

## Ten beads

Not every number of beads makes a square. Here are 9 beads, and then
10 beads.

<img src="ten-beads.svg" alt="On the left, a square of 3 rows of 3 beads, labelled 9 beads, side 3. On the right, the same 3 by 3 square with one more bead beside it, labelled 10 beads, 1 left over.">

With 10 beads, the biggest square has 3 beads on a side. 1 bead is
left over. A square with 4 on a side needs 16 beads, and we only have
10.

```question
id: ten-beads-1
type: multiple-choice
answer: 3

side(10) is the side of a square of 10 beads. What can we say about
side(10)?

- It is exactly 3
  - 3 × 3 is only 9. There is 1 bead left over.
- It is exactly 5
  - 10 ÷ 2 is 5. But 5 × 5 is 25, much more than 10.
- It is between 3 and 4
  - 3 × 3 = 9 is a little too small, and 4 × 4 = 16 is too big.
- It is between 4 and 5
  - 4 × 4 is already 16, which is more than 10.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Find 3 × 3. Is it more or less than 10?
2. Find 4 × 4. Is it more or less than 10?
3. side(10) must be bigger than one of them and smaller than the other.

**Think about:** 10 is between the square numbers 9 and 16.

**Try this next:** side(20) is between which two whole numbers?

</details>

A *whole number* is a number with no fraction part: 1, 2, 3, and so
on. side(10) is not a whole number. It is a little more than 3. The
next page is about sides like this.

## A machine that tries

The box below is a small Python program. It finds side(…) the way we
did: it tries 1, then 2, then 3, and so on. Each time, it checks the
number times itself. If that makes the beads, it prints the side.

```python exec
id: a-machine-that-tries-1
hint: Which whole number, times itself, makes 49? Make a guess now, or run the cell and see.
beads = 49

for side_length in range(1, beads + 1):
    if side_length * side_length == beads:
        print("A square of", beads, "beads has side", side_length)
```

```predict
type: number

Before you run it: what side will it print for 49 beads?
```

Now change `beads = 49` to other numbers and run it again.

- Try 144. Try 400.
- Try 10. What happens when no whole number works?
- Can you find a square number bigger than 1000?

<details class="dl-answer"><summary>What each line does</summary>

- `beads = 49` keeps the number of beads under a name we can read.
- `for side_length in range(1, beads + 1):` is a loop. It runs the
  lines under it again and again. The first time, `side_length` is 1.
  Then it is 2, then 3, and so on, up to the number of beads.
- `if side_length * side_length == beads:` checks one guess. `==` asks
  "is this equal to that?"
- `print(...)` runs only when the check says yes.

For 10 beads, no whole number passes the check, so the cell prints
nothing at all.

</details>

## Between two numbers

Most numbers are not square numbers. Their side is between two whole
numbers.

```question
id: between-two-numbers-1
type: multiple-choice
answer: 1

Between which two whole numbers is side(30)?

- 5 and 6
  - 5 × 5 = 25 is less than 30, and 6 × 6 = 36 is more.
- 15 and 16
  - 15 is half of 30. But 15 × 15 is 225, far more than 30.
- 6 and 7
  - 6 × 6 is 36, which is already more than 30.
- 4 and 5
  - 5 × 5 is only 25, so the side is more than 5.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Write the square numbers: 1, 4, 9, 16, 25, 36, 49.
2. Find the two square numbers that 30 sits between.
3. What is the side of each of those two squares?

**Think about:** the side of 30 beads is bigger than the side of the
square number below 30.

**Try this next:** side(50).

</details>

## Cubes of beads

Beads can also make a *cube*. A cube is a box shape. It is the same
number of beads wide, high and deep. The number of beads along one edge
is called its *edge*.

<img src="bead-cubes.svg" alt="Three cubes of beads. A single bead, labelled 1 bead, edge 1. A cube 2 beads wide, 2 high and 2 deep, labelled 8 beads, edge 2. A cube 3 beads wide, 3 high and 3 deep, labelled 27 beads, edge 3.">

A cube with 3 beads along each edge has $3 \times 3 \times 3 = 27$
beads. So we write

$$\text{edge}(27) = 3 \qquad \text{edge}(8) = 2$$

The golden beads had a cube of $10 \times 10 \times 10 = 10^3 = 1000$
beads. A cube is a power with exponent 3.

```question
id: cubes-of-beads-1
type: multiple-choice
answer: 2

A cube has 4 beads along each edge. How many beads does it have?

- 16
  - That is 4 × 4, one face of the cube. The cube has 4 of those
    layers, one behind the other.
- 64
  - 4 × 4 × 4: 4 layers, with 16 beads in each layer.
- 12
  - That is 4 × 3. The 3 in a cube says how many 4s we multiply.
- 48
  - That is 16 × 3. The cube has 4 layers of 16, not 3.
```

## Undoing a cube

edge(…) undoes a cube, the way side(…) undoes a square.

<div class="dl-world" data-world="numbers">

```question
id: undoing-a-cube-1--numbers
type: fill-in-the-blank

edge(5 × 5 × 5) = {5|125|15}

edge(1000) = {10|100|333}
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: undoing-a-cube-1--squiggles
type: fill-in-the-blank

edge(△ × △ × △) = {△|△ × △|3 × △}

edge(★³) = {★|★ × ★ × ★|3 × ★}
```

</div>

<div class="dl-world" data-world="letters">

```question
id: undoing-a-cube-1--letters
type: fill-in-the-blank

edge(c × c × c) = {c|c × c|3c}

edge(n³) = {n|n × n × n|3n}
```

</div>

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Picture a cube of beads. It is the same number wide, high and deep.
2. The thing in the brackets is the number of beads: wide times high
   times deep.
3. edge(…) asks how many beads are along one edge.

**Think about:** 1000 is the golden beads' cube.

**Try this next:** edge(64).

</details>

## A square and a cube

64 beads make a square, 8 by 8. 64 beads also make a cube, 4 by 4 by
4. So side(64) = 8 and edge(64) = 4.

```question
id: a-square-and-a-cube-1
type: multiple-choice
answer: 4

Which other number of beads makes a square and a cube?

- 16
  - 16 is a square, 4 by 4. For a cube, 2 × 2 × 2 is 8, and 3 × 3 × 3
    is 27.
- 27
  - 27 is a cube, 3 by 3 by 3. For a square, 5 × 5 is 25, and 6 × 6 is
    36.
- 100
  - 100 is a square, 10 by 10. For a cube, 4 × 4 × 4 is 64, and
    5 × 5 × 5 is 125.
- 1
  - One bead is a square, 1 by 1. It is also a cube, 1 by 1 by 1.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Write the square numbers up to 100: 1, 4, 9, 16, 25, 36, 49, 64, 81,
   100.
2. Write the cubes up to 100: 1 × 1 × 1, 2 × 2 × 2, 3 × 3 × 3,
   4 × 4 × 4.
3. Which numbers are in both lists?

**Think about:** the smallest square of beads, and the smallest cube.

**Try this next:** there is one more number like this below 1000. Can
you find it?

</details>

{{include: setup/zen-calm-check.md}}

## Your rule, in your words

Before you read our version, say what side(…) and edge(…) do, in your
own words. Write it in the Notes panel or on paper, or say it aloud.

<details class="dl-answer"><summary>one way to say it</summary>

side(…) starts with a square of beads, and gives the number of beads
along one side. It undoes a square: side(7 × 7) = 7. edge(…) does the
same for a cube: edge(3 × 3 × 3) = 3. When the beads do not make a
square, the side is between two whole numbers. Your way of saying it
may be clearer than ours.

</details>

## The usual way to write it

Books and calculators have a sign for side(…). They write side(49)
like this:

$$\sqrt{49} = 7$$

The sign √ is read "the *square root* of". So √49 is "the square root
of 49". It means exactly the same as side(49). The word *square* in
its name is the same square as our square of beads.

edge(…) has a sign too. edge(27) is written like this:

$$\sqrt[3]{27} = 3$$

This is read "the *cube root* of 27". It means exactly the same as
edge(27).

You will see these signs in other books. You can keep writing side(…)
and edge(…) when that feels calmer. They mean the same thing.

```question
id: the-usual-way-to-write-it-1
type: fill-in-the-blank

√36 means {side(36)|36 × 36|36 ÷ 2}.

∛8 means {edge(8)|8 × 8 × 8|8 ÷ 3}.
```

## Make your own

Can you make five problems of your own, and find each answer? Here are
some ideas:

- the side of a square number bigger than 1000
- the edge of a cube bigger than 1000
- a number whose side is between 9 and 10
- side(♡ × ♡), with a shape of your choice

Which of your problems looks hardest, but is not?

## Looking back

side(10) is not a whole number. Look at the picture of 10 beads again.
What does it show about why?

A challenge: the program below prints the square numbers, from 1 up to
400. Can you change it to print the cubes instead? Which numbers up to
1000 are in both lists?

```python challenge
# The square numbers: 1 × 1, 2 × 2, 3 × 3, and so on.
for side_length in range(1, 21):
    print("side", side_length, "makes", side_length * side_length)
```

## Read more

Wikipedia's page on [square numbers](https://en.wikipedia.org/wiki/Square_number)
has pictures of square numbers made of dots. Its page on
[cube numbers](https://en.wikipedia.org/wiki/Cube_(algebra)) does the
same for cubes.
