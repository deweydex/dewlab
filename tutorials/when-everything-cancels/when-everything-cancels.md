---
title: "The zero power: when everything cancels"
year: "2026-2027"
version: 2026.09.27.1
worlds:
  numbers: Normal numbers, like 3 and 10.
  squiggles: Shapes like ♡ and △, which can stand for any number.
  letters: Letters like b and n, which can stand for any number.
---

# The zero power: when everything cancels

Here is a fraction made of heart tiles, like the ones on the last page.
This time, the top and the bottom have the same number of hearts.

<img src="cancel-four-over-four.svg" alt="A fraction made of heart tiles. The top row has four hearts and the bottom row has four. Every heart on the top and every heart on the bottom has a line through it.">

```question
id: every-heart-1
type: fill-in-the-blank

On the top,
{0|4|1}
hearts have no line through them.

On the bottom,
{0|4|1}
hearts have no line through them.
```

## What is left?

Every heart is crossed out. When pairs cross out like this, we also say
they *cancel*. Here every heart cancels.

```question
id: what-is-left-1
type: multiple-choice
answer: 2

What is ♡⁴/♡⁴?

- 0
  - No tile is left without a line, so 0 can feel natural. But each
    crossed-out pair is worth 1, not 0.
- 1
  - There are four pairs, each worth 1. And 1 × 1 × 1 × 1 = 1.
- ♡
  - Every heart has a line through it. No heart is left in the answer.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Take one heart from the top and its partner from the bottom. They
   make ♡/♡.
2. On the last page, what was each pair worth?
3. There are four pairs. Multiply what they are worth.

**Think about:** a line through a pair does not make it 0. It shows the
pair is worth 1.

**Try this next:** what is ♡/♡ × ♡/♡?

</details>

## The pizza again

On [the pizza page](tutorial:one-whole-many-slices), 4/4 of a pizza was
one whole pizza. So were 8/8 and 12/12. A fraction with the same top
and bottom is 1.

♡⁴/♡⁴ has the same top and bottom too.

```question
id: the-pizza-again-1
type: fill-in-the-blank

The top and the bottom of ♡⁴/♡⁴ are the same number. So ♡⁴/♡⁴ is
{1|0|♡⁴}.
```

## Try some

Choose numbers, shapes or letters in the box under the title.

<div class="dl-world" data-world="numbers">

```question
id: try-some-1--numbers
type: fill-in-the-blank

2³ is
{8|6|9}.

So 2³/2³ is 8/8, which is
{1|0|8}.
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: try-some-1--squiggles
type: fill-in-the-blank

△³/△³ crosses out
{3|0|6}
pairs.

So △³/△³ is
{1|0|△}.
```

</div>

<div class="dl-world" data-world="letters">

```question
id: try-some-1--letters
type: fill-in-the-blank

a³/a³ crosses out
{3|0|6}
pairs.

So a³/a³ is
{1|0|a}.
```

</div>

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Write the top the long way, and the bottom under it.
2. Cross out the pairs. Is any tile left?
3. Each pair was worth 1.

**Think about:** a fraction with the same top and bottom.

**Try this next:** what is ♡¹⁰⁰/♡¹⁰⁰?

</details>

## What the rule says

The last page had a rule for dividing: take the bottom exponent away
from the top one. On that page, the top always had more hearts. What
does the rule say when the top and the bottom are the same?

```question
id: what-the-rule-says-1
type: fill-in-the-blank

The rule says ♡⁴/♡⁴ is ♡ to the power
{0|1|8}.
```

4 − 4 = 0. So the rule gives ♡⁰. We say "heart to the power zero".

{{include: setup/zen-calm-check.md}}

## Two ways, one answer

We found ♡⁴/♡⁴ in two ways:

- Crossing out the pairs gave 1.
- The rule gave ♡⁰.

Both ways start from the same division. So they must give the same
number.

```question
id: two-ways-one-answer-1
type: multiple-choice
answer: 3

What must ♡⁰ be?

- 0
  - An exponent of 0 can feel like "no hearts, so nothing". But
    crossing out all the pairs gave 1.
- ♡
  - ♡ is ♡¹, one heart. The exponent here is 0.
- 1
  - Crossing out gave 1, and the rule gave ♡⁰. They are the same
    division.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Look at the two ways again. Both found ♡⁴/♡⁴.
2. The first way gave a number. Which number?
3. The second way gave ♡⁰. It is the same division.

**Think about:** two paths to one place.

**Try this next:** find ♡⁷/♡⁷ in both ways. Do you get the same pair of
answers?

</details>

So ♡⁰ = 1. A power with the exponent 0 is called a *zero power*.

$$\heartsuit^0 = 1$$

The heart can be 2, or 10, or a million, or a fraction like ½. Each
time, the zero power is 1. With letters, $a^0 = 1$.

## A checking machine

Python can check this. In Python, `5 ** 0` means 5⁰.

```python exec
id: a-checking-machine-1
print(5 ** 0)
print(10 ** 0)
print((1/2) ** 0)
```

```predict
type: choice

Before you run it: what will the first line, `5 ** 0`, print?

- 1
- 0
  - An exponent of 0 can feel like "no fives", so nothing.
- 5
  - With no multiplying at all, it can feel like the 5 stays as it is.
```

The first two lines print 1. The last line prints 1.0. Python writes
1/2 as the decimal 0.5, so its answer has a decimal point too. 1.0 is
the same number as 1. Now try other numbers: `1000000 ** 0`, or
`2.5 ** 0`.

## A third way: going down

Here are the powers of 2, going down one step at a time:

$$2^4 = 16 \qquad 2^3 = 8 \qquad 2^2 = 4 \qquad 2^1 = 2$$

Each step down divides by 2.

```question
id: a-third-way-1
type: fill-in-the-blank

The next step down is 2⁰. It is 2 ÷ 2, which is
{1|0|2}.
```

The golden beads on [the powers page](tutorial:the-long-way) go down in
the same way. The cube is 10³ = 1000 beads. The square is 10² = 100,
and the bar is 10¹ = 10. One step down from the bar is a single bead:
10⁰ = 1.

## Join, then cancel

The rule for joining two stacks works here too.

<div class="dl-world" data-world="numbers">

```question
id: join-then-cancel-1--numbers
type: fill-in-the-blank

The top of (2³ × 2²)/2⁵ joins into
{2⁵|2⁶|4⁵}.

So (2³ × 2²)/2⁵ is
{1|0|2}.
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: join-then-cancel-1--squiggles
type: fill-in-the-blank

The top of (♡³ × ♡²)/♡⁵ joins into
{♡⁵|♡⁶|5♡}.

So (♡³ × ♡²)/♡⁵ is
{1|0|♡}.
```

</div>

<div class="dl-world" data-world="letters">

```question
id: join-then-cancel-1--letters
type: fill-in-the-blank

The top of (a³ × a²)/a⁵ joins into
{a⁵|a⁶|5a}.

So (a³ × a²)/a⁵ is
{1|0|a}.
```

</div>

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Look at the top only. Join its two stacks into one row.
2. Now compare the top and the bottom. How many tiles does each have?
3. Cross out the pairs. Is anything left?

**Think about:** the top and the bottom only need the same number of
tiles in the end.

**Try this next:** (♡⁴ × ♡⁴)/(♡² × ♡⁶).

</details>

{{include: setup/zen-calm-check.md}}

## Your rule, in your words

Before you read our version, say the idea of this page in your own
words. Write it in the Notes panel or on paper, or say it aloud.

<details class="dl-answer"><summary>one way to say it</summary>

A power divided by itself is 1, because every tile cancels. The rule
for dividing gives it an exponent of 0. The two ways must agree, so a
power with the exponent 0 is 1. Your way of saying it may be clearer
than ours.

</details>

## Make your own

Can you make five messy divisions that are exactly 1? Try one with a
very big exponent, and one with two stacks on the top and two on the
bottom. Try one with a fraction as the base. Then write each one with
the rule, as a zero power.

## Looking back

On the pizza page, 8/8 was one whole pizza. On this page, ♡⁴/♡⁴ was 1.
How are these the same idea?

A challenge: the program below prints the powers of 2, going down to
2⁰. Each step down divides by 2. Can you make it show the powers of 10
instead? Or the powers of 3? What does each step down do to the number?

```python challenge
# The powers of 2, going down one step at a time.
for exponent in [5, 4, 3, 2, 1, 0]:
    print("2 **", exponent, "=", 2 ** exponent)
```

## Read more

Maths is Fun has a page on the [laws of
exponents](https://www.mathsisfun.com/algebra/exponent-laws.html). Its
part on dividing shows why x⁰ = 1, in the same way as this page. The
page before this one is [Dividing powers: crossing out
pairs](tutorial:sharing-out).
