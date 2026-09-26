---
title: "Powers: the long way and the short way"
year: "2026-2027"
version: 2026.09.26.1
worlds:
  numbers: Ordinary numbers, like 3 and 10.
  squiggles: Shapes like ♡ and △, which can stand for any number.
  letters: Letters like b and n, which can stand for any number.
---

# Powers: the long way and the short way

Here is a sheet of paper, folded in half again and again. After each
fold, we opened the paper flat to see the folds. The dashed lines are
the folds. They cut the sheet into equal pieces.

<img src="folded-paper.svg" alt="Five sheets of paper side by side, after 0, 1, 2, 3 and 4 folds, opened flat. Dashed creases divide them into 1, 2, 4, 8 and 16 equal pieces.">

```question
id: folded-paper-1
type: multiple-choice
answer: 3

After 5 folds, how many pieces will there be?

- 10
  - That adds 2 pieces for each fold. Look at how the count grows from
    one picture to the next: is it adding, or doing something else?
- 25
  - That is 5 × 5. Each fold does something to the pieces that were
    already there.
- 32
  - Each fold doubles the pieces: 16 becomes 32.
- 20
  - That adds 4 to the last picture. The jumps between pictures are
    getting bigger each time.
```

## Doubling, written out

Each fold doubles the pieces. After 5 folds, the pieces are

$$2 \times 2 \times 2 \times 2 \times 2 = 32$$

That is five 2s, multiplied together. Writing all of them is the *long
way*. There is also a short way:

$$2^5 = 2 \times 2 \times 2 \times 2 \times 2$$

A number written like $2^5$ is called a *power*. We say "two to the
power of five". It has two parts:

- The big number, 2, is the *base*. It is the number being multiplied.
- The small raised number, 5, is the *exponent*. It says how many times
  the base appears in the multiplying.

The short way and the long way mean exactly the same thing. The short
way is only quicker to write.

```question
id: doubling-written-out-1
type: fill-in-the-blank

The long way to write 2³ is {2 × 2 × 2|2 × 3|3 × 3 × 3}, and it comes to
{8|6|9}.
```

## The golden beads

In a Montessori classroom, children count with *golden beads*: a single
bead, a bar of 10 beads, a square of 100, and a cube of 1000.

<img src="golden-beads.svg" alt="Four shapes made of beads. A single bead, labelled 1. A straight bar of 10 beads, labelled 10. A flat square of 10 rows of 10 beads, labelled 100. A cube, 10 beads wide, 10 high and 10 deep, labelled 1000.">

Each shape is ten of the shape before it:

- The bar is 10 beads: $10 = 10^1$.
- The square is 10 bars: $10 \times 10 = 10^2$.
- The cube is 10 squares: $10 \times 10 \times 10 = 10^3$.

The exponent counts the tens being multiplied. It also counts
directions: a bar goes one way, a square goes two ways, and a cube goes
three ways.

```question
id: the-golden-beads-1
type: fill-in-the-blank

The cube is 10 beads wide, 10 high and 10 deep, so it is
{10³|10 × 3|3¹⁰} beads.
```

What comes after the cube? $10^4$ is ten cubes, or 10,000 beads. A
cube has only three directions. So for $10^4$, we put ten cubes in a
long row.

{{include: setup/zen-calm-check.md}}

## Writing it the long way

Now let's write some powers the long way. Choose numbers, shapes or
letters in the box under the title. The pattern is the same in each.

<div class="dl-world" data-world="numbers">

```question
id: writing-it-the-long-way-1--numbers
type: fill-in-the-blank

3⁴ the long way is {3 × 3 × 3 × 3|3 × 4|4 × 4 × 4}.

5² the long way is {5 × 5|5 × 2|2 × 2 × 2 × 2 × 2}.

10⁶ the long way is {10 × 10 × 10 × 10 × 10 × 10|10 × 6|10 + 10 + 10 + 10 + 10 + 10}.
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: writing-it-the-long-way-1--squiggles
type: fill-in-the-blank

♡⁴ the long way is {♡ × ♡ × ♡ × ♡|♡ × 4|4 × 4 × 4 × 4}.

△² the long way is {△ × △|△ × 2|2 × 2}.

★⁶ the long way is {★ × ★ × ★ × ★ × ★ × ★|★ × 6|★ + ★ + ★ + ★ + ★ + ★}.
```

</div>

<div class="dl-world" data-world="letters">

```question
id: writing-it-the-long-way-1--letters
type: fill-in-the-blank

b⁴ the long way is {b × b × b × b|b × 4|4 × 4 × 4 × 4}.

c² the long way is {c × c|c × 2|2 × 2}.

d⁶ the long way is {d × d × d × d × d × d|d × 6|d + d + d + d + d + d}.
```

</div>

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The big number, shape or letter is the base. Write it down once.
2. The small raised number says how many times the base appears.
3. Write the base that many times, with × between each one.

**Think about:** the small number is never multiplied. It is a count.

**Try this next:** what would a power with exponent 12 look like, the
long way? Why do you think people invented the short way?

</details>

## Two numbers, two ways round

$2 \times 3$ and $3 \times 2$ are both 6. The order does not change
the answer. Is it the same for powers? Is $2^3$ the same as $3^2$?

In code, we cannot write a small raised number. So Python writes a
power with two stars, `**`. In Python, `2 ** 3` means $2^3$.

```python exec
id: two-ways-round-1
print(2 ** 3)
print(3 ** 2)
```

```predict
type: choice

Before you run it: which is bigger, 2³ or 3²?

- 2³ is bigger
  - 3 is the bigger exponent, and that feels like it should win.
- 3² is bigger
- They are the same
  - 2 × 3 and 3 × 2 are the same, so this feels like it should be too.
```

$2^3$ is $2 \times 2 \times 2 = 8$, and $3^2$ is $3 \times 3 = 9$. They
are close, but different. If we change the places of the base and the
exponent, the answer changes. So for powers, the order matters. Try
some others in the box: $2^4$ and $4^2$, or $2^5$ and $5^2$. Can you
find a pair that gives the same answer both ways?

## When the base is a fraction

Look at the folded paper again. After 4 folds, there are 16 equal
pieces. So each piece is $\frac{1}{16}$ of the sheet. Each fold cut
every piece in half:

$$\frac{1}{2} \times \frac{1}{2} \times \frac{1}{2} \times \frac{1}{2} = \frac{1}{16}$$

That is a power too, with a fraction for its base:

$$\left(\frac{1}{2}\right)^4 = \frac{1}{16}$$

This is the pizza idea again, with paper: 16 pieces of $\frac{1}{16}$
make one whole sheet.

```question
id: when-the-base-is-a-fraction-1
type: fill-in-the-blank

After 3 folds, each piece is (1/2)³ = {1/8|3/2|1/6} of the sheet.
```

Multiply a number bigger than 1 by itself again and again, and it gets
bigger. Multiply a fraction smaller than 1 by itself, and it gets
smaller. Each fold makes the pieces smaller. But they never get to
zero.

{{include: setup/zen-calm-check.md}}

## Your rule, in your words

Before you read our version, say what a power is in your own words.
Write it in the Notes panel or on paper, or say it aloud.

<details class="dl-answer"><summary>one way to say it</summary>

A power is a short way to write a number multiplied by itself. The big
number is the number we multiply. The small raised number counts how
many times it appears. Your way of saying it may be clearer than
ours.

</details>

## Make your own

Can you make five powers of your own, and write each one the long way?
Try one with a big exponent, one with a fraction as the base, and one
with a shape. Which one surprises you most?

## Looking back

The short way and the long way mean the same thing. When is the long
way better? When is the short way better?

A challenge: the program below prints the powers of 2, from $2^1$ to
$2^{10}$. $2^{10}$ is very close to 1000. Can you make it go up to
$2^{20}$? Which power of 10 is $2^{20}$ close to?

```python challenge
# The powers of 2, from 2 to the power 1 up to 2 to the power 10.
for exponent in range(1, 11):
    print("2 **", exponent, "=", 2 ** exponent)
```

## Read more

People still make and use Maria Montessori's golden beads today.
Wikipedia's page on the [Montessori
materials](https://en.wikipedia.org/wiki/Montessori_sensorial_materials)
describes some of them. Wikipedia's page on
[exponentiation](https://en.wikipedia.org/wiki/Exponentiation) says much
more about powers.
