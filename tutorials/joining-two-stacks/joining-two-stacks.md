---
title: "Multiplying powers: joining two stacks"
year: "2026-2027"
version: 2026.09.27.1
worlds:
  numbers: Normal numbers, like 3 and 10.
  squiggles: Shapes like ♡ and △, which can stand for any number.
  letters: Letters like b and n, which can stand for any number.
---

# Multiplying powers: joining two stacks

A heart, ♡, stands for a number. We do not say which one. On the last
page, ♡³ meant ♡ × ♡ × ♡: three hearts, multiplied together. On this
page, we call a row of hearts multiplied together a *stack*.

Here are two stacks of hearts, multiplied. Each heart sits on a small
square tile.

<img src="join-two-and-three.svg" alt="Two yellow hearts, then a times sign, then three blue hearts. After an equals sign, all five hearts sit in one row: two yellow, then three blue.">

```question
id: two-stacks-1
type: fill-in-the-blank

The yellow hearts, the first stack, are ♡ × ♡. Written the short way,
that is
{♡²|2♡|♡³}.

The blue hearts, the second stack, are ♡ × ♡ × ♡. Written the short
way, that is
{♡³|3♡|♡²}.
```

## Two stacks, one row

The picture multiplies the yellow stack by the blue stack. After the
equals sign, every heart is in one long row. Each heart keeps its
colour, so you can see where it came from: the first two hearts come
from the first stack, and the last three from the second.

```question
id: two-stacks-one-row-1
type: multiple-choice
answer: 2

The long row is the long way to write one power. Which power?

- $\heartsuit^6$
  - 2 × 3 = 6. Multiplying the powers can feel like multiplying the
    small numbers too. Count the hearts in the row.
- $\heartsuit^5$
  - Five hearts, multiplied together.
- $5\heartsuit$
  - $5\heartsuit$ is five hearts added together. The hearts in the row
    are multiplied.
```

So ♡² × ♡³ = ♡⁵. The two stacks joined into one.

## Four and one

Here is another pair of stacks. A stack of one heart is ♡¹, which is
♡ on its own.

<img src="join-four-and-one.svg" alt="Four yellow hearts, then a times sign, then one blue heart. After an equals sign, all five hearts sit in one row: four yellow, then one blue.">

```question
id: four-and-one-1
type: fill-in-the-blank

♡⁴ × ♡¹ is a row of
{5|4|6}
hearts.

So ♡⁴ × ♡¹ is
{♡⁵|♡⁴|5♡}.
```

## Without a picture

Now there is no picture. Write both stacks the long way. Then join them
into one row, and count. Choose numbers, shapes or letters in the box
under the title. The pattern is the same in each.

<div class="dl-world" data-world="numbers">

```question
id: without-a-picture-1--numbers
type: fill-in-the-blank

2³ the long way is
{2 × 2 × 2|2 × 3|3 × 3}.

2³ × 2³ is one row of
{6|9|5}
twos, multiplied together.

So 2³ × 2³ is
{2⁶|2⁹|2 × 6}.
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: without-a-picture-1--squiggles
type: fill-in-the-blank

△³ the long way is
{△ × △ × △|△ × 3|3 × 3}.

△³ × △³ is one row of
{6|9|5}
triangles, multiplied together.

So △³ × △³ is
{△⁶|△⁹|6△}.
```

</div>

<div class="dl-world" data-world="letters">

```question
id: without-a-picture-1--letters
type: fill-in-the-blank

a³ the long way is
{a × a × a|a × 3|3 × 3}.

a³ × a³ is one row of
{6|9|5}
a's, multiplied together.

So a³ × a³ is
{a⁶|a⁹|6a}.
```

</div>

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Write the first power the long way. It has 3 of the same thing.
2. Write the second power the long way, after it, with × between them.
3. Now there is one row. Count everything in it.

**Think about:** the exponent counts how many are in the row.

**Try this next:** what is a stack of 3, times a stack of 1?

</details>

## A longer row

<div class="dl-world" data-world="numbers">

```question
id: a-longer-row-1--numbers
type: fill-in-the-blank

3⁵ × 3⁴ is one row of
{9|20|1}
threes.

So 3⁵ × 3⁴ is
{3⁹|3²⁰|9³}.

2¹⁰ × 2²⁰ is one row of
{30|200|10}
twos.

So 2¹⁰ × 2²⁰ is
{2³⁰|2²⁰⁰|4³⁰}.
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: a-longer-row-1--squiggles
type: fill-in-the-blank

♡⁵ × ♡⁴ is one row of
{9|20|1}
hearts.

So ♡⁵ × ♡⁴ is
{♡⁹|♡²⁰|9♡}.

♡¹⁰ × ♡²⁰ is one row of
{30|200|10}
hearts.

So ♡¹⁰ × ♡²⁰ is
{♡³⁰|♡²⁰⁰|30♡}.
```

</div>

<div class="dl-world" data-world="letters">

```question
id: a-longer-row-1--letters
type: fill-in-the-blank

b⁵ × b⁴ is one row of
{9|20|1}
b's.

So b⁵ × b⁴ is
{b⁹|b²⁰|9b}.

c¹⁰ × c²⁰ is one row of
{30|200|10}
c's.

So c¹⁰ × c²⁰ is
{c³⁰|c²⁰⁰|30c}.
```

</div>

Thirty is a lot to write. Did you write them all, or did you find
another way to count?

{{include: setup/zen-calm-check.md}}

## A quicker way

Here is what we found so far:

$$\heartsuit^2 \times \heartsuit^3 = \heartsuit^5 \qquad \heartsuit^4 \times \heartsuit^1 = \heartsuit^5$$

$$\heartsuit^3 \times \heartsuit^3 = \heartsuit^6 \qquad \heartsuit^5 \times \heartsuit^4 = \heartsuit^9$$

```question
id: a-quicker-way-1
type: multiple-choice
answer: 2

Look only at the small numbers. How can you find the exponent after
the equals sign, without counting hearts?

- Multiply the two exponents
  - For ♡³ × ♡³, that gives ♡⁹. But the row has 6 hearts. Try it on
    each line.
- Add the two exponents
  - 2 + 3 = 5, 4 + 1 = 5, 3 + 3 = 6, and 5 + 4 = 9.
- Take the bigger exponent
  - For ♡² × ♡³, that gives 3. The row has more hearts than either
    stack.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Take the first line. The two small numbers on the left are 2 and 3.
2. The small number after the equals sign is 5.
3. What can you do to 2 and 3 to get 5?

**Think about:** where each heart in the long row came from.

**Try this next:** does the same thing work for 4 and 1?

</details>

Each stack brings its own hearts to the row. So we add the exponents.
This is a rule. When we multiply two powers with the same base, we add
their exponents. Many books call it the *product rule* for powers. A
*product* is the answer to a multiplication.

Here is the rule with shapes in the exponents:

$$\heartsuit^{\triangle} \times \heartsuit^{\square} = \heartsuit^{\triangle + \square}$$

The first stack has △ hearts, and the second has □ hearts. So the row
has △ + □ hearts. The heart could be any number at all, and the pattern
still holds. That is all a letter in algebra means. Here is the same
rule with letters:

$$a^m \times a^n = a^{m + n}$$

<div class="dl-world" data-world="numbers">

```question
id: a-quicker-way-2--numbers
type: fill-in-the-blank

5⁸ × 5¹² is
{5²⁰|5⁹⁶|25²⁰}.
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: a-quicker-way-2--squiggles
type: fill-in-the-blank

♡⁸ × ♡¹² is
{♡²⁰|♡⁹⁶|20♡}.
```

</div>

<div class="dl-world" data-world="letters">

```question
id: a-quicker-way-2--letters
type: fill-in-the-blank

d⁸ × d¹² is
{d²⁰|d⁹⁶|20d}.
```

</div>

## Two different shapes

The rule needs the same base in both stacks. What happens when the
bases are different?

<div class="dl-world" data-world="numbers">

2² × 3³ the long way is 2 × 2 × 3 × 3 × 3.

```question
id: two-different-shapes-1--numbers
type: multiple-choice
answer: 2

Can we write 2² × 3³ as one power?

- Yes, it is 5⁵
  - 2 + 3 = 5 in both places. But 5⁵ is 3125, and 2² × 3³ is
    4 × 27 = 108.
- No, the bases are different
  - Twos and threes do not join into one stack of the same number.
- Yes, it is 6⁵
  - 2 × 3 = 6. But 6⁵ is 7776, and 2² × 3³ is only 108.
```

</div>

<div class="dl-world" data-world="squiggles">

♡² × △³ the long way is ♡ × ♡ × △ × △ × △.

```question
id: two-different-shapes-1--squiggles
type: multiple-choice
answer: 2

Can we write ♡² × △³ as one power?

- Yes, it is $\heartsuit^5$
  - 2 + 3 = 5 counts every tile. But three of the tiles are triangles,
    not hearts.
- No, the bases are different
  - A heart and a triangle can be different numbers. They do not join
    into one stack.
- Yes, it is $(\heartsuit \times \triangle)^5$
  - That would be five hearts and five triangles. The row has two
    hearts and three triangles.
```

</div>

<div class="dl-world" data-world="letters">

a² × b³ the long way is a × a × b × b × b.

```question
id: two-different-shapes-1--letters
type: multiple-choice
answer: 2

Can we write a² × b³ as one power?

- Yes, it is $a^5$
  - 2 + 3 = 5 counts every letter. But three of them are b's, not a's.
- No, the bases are different
  - a and b can be different numbers. They do not join into one stack.
- Yes, it is $(ab)^5$
  - That would be five a's and five b's. The row has two a's and three
    b's.
```

</div>

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Write the row the long way. Look at each tile in it.
2. A power has one base, repeated. Is every tile in the row the same?
3. If not, how many different things are in the row?

**Think about:** what "the same base" means in the rule.

**Try this next:** can ♡² × △³ × ♡⁴ be made shorter? Which parts can
join?

</details>

## A checking machine

Python can check the rule with numbers. In Python, `**` means a power,
and `*` means multiply. So `2 ** 3 * 2 ** 4` means 2³ × 2⁴. Python
finds the powers first, and then multiplies.

```python exec
id: a-checking-machine-1
print(2 ** 3 * 2 ** 4)
print(2 ** 7)
print(2 ** 12)
```

```predict
type: choice

Before you run it: the first line is 2³ × 2⁴. Which other line will
print the same number?

- The second line, 2 ** 7
- The third line, 2 ** 12
  - 3 × 4 = 12. When two powers are multiplied, multiplying the
    exponents can feel natural.
- Neither of them
  - Two powers multiplied together can feel too big to be one power.
```

The first two lines both print 128. The third prints 4096, which is
much bigger. Now change the numbers and run it again. Try
`10 ** 2 * 10 ** 3` on the first line and `10 ** 5` on the second. Do
they still agree?

## Powers of ten

Computers count their memory in *bytes*. One byte can hold one letter,
like A. Big amounts of memory have names made from powers of ten:

- A *gigabyte* is 10⁹ bytes.
- A *zettabyte* is 10²¹ bytes.

That is what the two words mean. How many gigabytes make a zettabyte?

```question
id: powers-of-ten-1
type: fill-in-the-blank

10⁹ × 10¹² =
{10²¹|10¹⁰⁸|100²¹}
```

So 10¹² gigabytes make one zettabyte. 10¹² is a million million. With
the rule, we only need to add: 9 + 12 = 21.

{{include: setup/zen-calm-check.md}}

## Your rule, in your words

Before you read our version, say the rule of this page in your own
words. Write it in the Notes panel or on paper, or say it aloud.

<details class="dl-answer"><summary>one way to say it</summary>

To multiply two powers with the same base, write both the long way.
They join into one row. The row has all the hearts from both stacks. So
we add the two exponents, and keep the base. Your way of saying it may
be clearer than ours.

</details>

## Make your own

Can you make five multiplications of two powers, and write each answer
as one power? Try one with a very big exponent, one with three stacks,
and one with a shape. Can you make one whose answer is ♡¹⁰⁰?

## Looking back

On [the last page](tutorial:the-long-way), the exponent counted how many
times the base appears. How does that explain why we add the exponents
here, and do not multiply them?

A challenge: the program below checks the rule for many pairs of
exponents. It finds 2 to the power `first`, times 2 to the power
`second`. Then it asks if that is the same as 2 to the power
`first + second`. `True` means yes. Can you make it use 3, or 10, as the base? Can you find a
pair where it prints `False`?

```python challenge
# Does 2 ** first * 2 ** second equal 2 ** (first + second)?
for first in range(1, 6):
    for second in range(1, 6):
        joined = 2 ** first * 2 ** second
        print(first, second, joined == 2 ** (first + second))
```

## Read more

Maths is Fun has a page on the [laws of
exponents](https://www.mathsisfun.com/algebra/exponent-laws.html). It
writes every letter the long way, as we did here. Wikipedia's page on
[metric prefixes](https://en.wikipedia.org/wiki/Metric_prefix) lists
giga, zetta and the other names for powers of ten.
