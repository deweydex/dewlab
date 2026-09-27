---
title: "Negative powers: more on the bottom"
year: "2026-2027"
version: 2026.09.27.1
worlds:
  numbers: Normal numbers, like 3 and 10.
  squiggles: Shapes like ♡ and △, which can stand for any number.
  letters: Letters like b and n, which can stand for any number.
---

# Negative powers: more on the bottom

Here is a division of two powers, written the long way. There are 2
hearts on the top and 5 hearts on the bottom.

$$\frac{\heartsuit^2}{\heartsuit^5} = \frac{\heartsuit \times \heartsuit}{\heartsuit \times \heartsuit \times \heartsuit \times \heartsuit \times \heartsuit}$$

In *Dividing powers: crossing out pairs*, we crossed out a heart on the
top with a heart on the bottom. To *cross out* is to draw a line
through something. In the picture, every pair is crossed out.

<img src="cancel-two-over-five.svg" alt="A fraction made of hearts. On the top, 2 hearts. On the bottom, 5 hearts. The 2 hearts on the top and the first 2 hearts on the bottom are crossed out, in pairs. 3 hearts on the bottom are not crossed out.">

```question
id: cross-out-the-pairs-1
type: multiple-choice
answer: 1

After we cross out the pairs, where are the hearts that are left?

- 3 hearts, on the bottom
  - There were 5 on the bottom, and 2 are crossed out. 3 stay, under
    the line.
- 3 hearts, on the top
  - 5 − 2 is 3. Look at the picture again. Which side of the line are
    the 3 hearts on?
- No hearts at all
  - Every heart on the top has a partner. Does every heart on the
    bottom have one too?
```

On the pages before this one, the top always had more hearts. This
time, the bottom has more.

## What stays on the top

Every heart on the top is crossed out. So what is on the top now?

Each crossed-out pair is a heart divided by a heart: ♡/♡. In *Fractions:
one whole pizza, many slices*, that was ♡ slices of a pizza cut into ♡
slices. It is one whole pizza, so ♡/♡ = 1.

```question
id: what-stays-on-the-top-1
type: multiple-choice
answer: 1

The top has no hearts left. What number is on the top?

- 1
  - Each crossed-out pair is ♡/♡, which is 1. Multiplying by 1
    changes nothing, so 1 stays on the top.
- 0
  - Nothing is left to see, so it looks like zero. But each pair we
    crossed out was ♡/♡, and that is 1, not 0.
- ♡
  - The top had 2 hearts, and both found a partner on the bottom.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. What is 3/3? It is 3 slices of a pizza cut into 3 slices.
2. So 3/3 is one whole pizza: 1.
3. In the same way, ♡/♡ is 1, whatever number the heart is.

**Think about:** what is left of 5/5 when you cross out the 5 on the
top and the 5 on the bottom.

**Try this next:** what is 2/6, when you cross out a 2 from the top
and from the bottom? (6 is 2 × 3.)

</details>

So the top is 1, and 3 hearts stay on the bottom:

$$\frac{\heartsuit^2}{\heartsuit^5} = \frac{1}{\heartsuit \times \heartsuit \times \heartsuit} = \frac{1}{\heartsuit^3}$$

## A second picture

Here is $\heartsuit^3$ over $\heartsuit^4$. The pairs are crossed out
in the same way.

<img src="cancel-three-over-four.svg" alt="A fraction made of hearts. On the top, 3 hearts. On the bottom, 4 hearts. All 3 hearts on the top are crossed out, each with a heart on the bottom. 1 heart on the bottom is not crossed out.">

```question
id: a-second-picture-1
type: fill-in-the-blank

The number on the top is
{1|0|♡}.

So ♡³/♡⁴ is
{1/♡|♡|1}.
```

## The subtracting rule

In *Dividing powers: crossing out pairs*, we found a short way to
divide. We subtract the bottom exponent from the top exponent:

$$\frac{\heartsuit^5}{\heartsuit^2} = \heartsuit^{5-2} = \heartsuit^3$$

What happens if we use the same rule on $\heartsuit^2$ over
$\heartsuit^5$? The top exponent is 2, and the bottom exponent is 5. So
we need $2 - 5$.

A number below zero, like −3, is a *negative* number. We say "minus
three". On a thermometer, −3 is three degrees below zero.

```question
id: the-subtracting-rule-1
type: fill-in-the-blank

2 − 5 is
{−3|3|−7}.

So the rule says ♡²/♡⁵ is
{♡⁻³|♡³|♡⁷}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Start at 2 on a number line.
2. Take away 5, one step at a time: 1, 0, and then below zero.
3. Count the steps below zero. Where do you stop?

**Think about:** we took away more than we had, so the answer is below
zero.

**Try this next:** 3 − 4.

</details>

## Two ways, one answer

We did the same division in two ways.

- Crossing out the pairs gave $\dfrac{1}{\heartsuit^3}$.
- Subtracting the exponents gave $\heartsuit^{-3}$.

Both came from $\heartsuit^2$ over $\heartsuit^5$. So they are the same
amount:

$$\heartsuit^{-3} = \frac{1}{\heartsuit^3}$$

A power with a negative exponent is called a *negative power*. It means
one over the power: a 1 on the top, and the power on the bottom. The
minus sign tells us where the hearts are. They are on the bottom.

```question
id: two-ways-one-answer-1
type: multiple-choice
answer: 1

What is △⁻²?

- 1/△²
  - The minus sign in the exponent puts the two triangles on the
    bottom, under a 1.
- −△²
  - A minus sign in front of a number makes it negative, so this feels
    natural. Here, the minus sign is in the exponent. It tells us where
    the triangles go.
- △ × △
  - That is △², with both triangles on the top.
```

## Powers and fractions

This page comes from a worksheet. The worksheet asks how $2^3$ over
$2^5$ might be a fraction. Here it is the long way:

$$\frac{2^3}{2^5} = \frac{2 \times 2 \times 2}{2 \times 2 \times 2 \times 2 \times 2}$$

```question
id: powers-and-fractions-1
type: fill-in-the-blank

After crossing out the pairs, 2³/2⁵ is 1 over
{2²|2³|2⁸}.

That is the fraction
{1/4|1/8|4}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Cross out a 2 on the top with a 2 on the bottom. Do this three
   times.
2. Count the 2s left on the bottom.
3. Multiply them together.

**Think about:** the subtracting rule says $2^{3-5} = 2^{-2}$. Does
that agree?

**Try this next:** 2²/2⁵.

</details>

There is a second path to the same fraction. $2^3$ is 8, and $2^5$ is
32, so this is $\frac{8}{32}$. In [Equivalent fractions: the same
amount, different names](tutorial:same-amount-different-names), we
divided the top and the bottom by the same number. Divide both by 8,
and $\frac{8}{32}$ becomes $\frac{1}{4}$. Crossing out a pair of 2s
does the same thing. It divides the top and the bottom by 2.

{{include: setup/zen-calm-check.md}}

## Going down in tens

Here are the golden beads from *Powers: the long way and the short
way*, going down. Each line is the line above it, divided by 10.

| Power | Amount |
|---|---|
| $10^3$ | 1000 |
| $10^2$ | 100 |
| $10^1$ | 10 |
| $10^0$ | 1 |

The last line comes from *The zero power: when everything cancels*.
What comes after it?

```question
id: going-down-in-tens-1
type: fill-in-the-blank

10⁻¹ is 1 divided by 10, which is
{1/10|0|−10}.

10⁻² is 1/10 divided by 10, which is
{1/100|−100|−20}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Going down one line divides by 10: 1000, then 100, then 10, then 1.
2. Divide 1 by 10. Picture a pizza cut into 10 slices. How big is one
   slice?
3. Now cut that slice into 10 again.

**Think about:** each line down cuts the amount into 10 pieces, and
keeps one of them.

**Try this next:** 10⁻³.

</details>

The table continues below zero. Each line is still the line above,
divided by 10. So $10^{-2} = \frac{1}{100} = \frac{1}{10^2}$, which is
one over the power, as before.

## Centimetres and millimetres

A metre is 100 centimetres. A centimetre (cm) is about the width of a
fingernail. So one centimetre is one hundredth of a metre:

$$1 \text{ cm} = \frac{1}{100} \text{ m} = \frac{1}{10^2} \text{ m} = 10^{-2} \text{ m}$$

A metre is also 1000 millimetres. A millimetre (mm) is about the
thickness of a bank card.

```question
id: centimetres-and-millimetres-1
type: fill-in-the-blank

1 mm is
{1/1000|1/100|1/10}
of a metre.

So 1 mm is
{10⁻³|10³|10⁻¹⁰⁰⁰}
metres.
```

Scientists write very small lengths in this way. A negative power of
ten is short, even when the length is tiny.

## Python and negative powers

Python writes a power with two stars. A negative power works too:
`10 ** -2` means $10^{-2}$.

```python exec
id: python-and-negative-powers-1
print(10 ** -2)
```

```predict
type: choice

Before you run it: what will Python print?

- -100
  - A minus sign often makes a number negative, so this feels natural.
- 0.01
- -20
  - That is 10 × −2. The exponent is not multiplied. It counts the 10s,
    and its sign says where they go.
```

Python printed 0.01. This is a *decimal*: a number with a point in it.
A decimal is another way to write a fraction. The first place after the
point counts tenths, and the second counts hundredths. So 0.01 is
$\frac{1}{100}$, one centimetre in metres.

Now one with a 2.

```python exec
id: python-and-negative-powers-2
print(2 ** -1)
```

```predict
type: choice

Before you run it: what will Python print for `2 ** -1`?

- -2
  - The minus sign seems to make the 2 negative.
- 0.5
- 1/2
  - This is the same amount as 0.5. Which way will Python write it?
```

$2^{-1}$ is $\frac{1}{2}$, and Python writes one half as the decimal
0.5. If you want fractions, Python has a tool for them. The first line
below gets the fraction tool ready.

```python exec
id: python-and-negative-powers-3
from fractions import Fraction

print(Fraction(2) ** -1)
print(Fraction(2) ** -3)
print(Fraction(2 ** 3, 2 ** 5))
```

`Fraction(2)` is the number 2, kept as a fraction. The last line is
$2^3$ over $2^5$ from earlier on this page. Change the numbers, and run
it again. What does `Fraction(10) ** -3` print?

## Your turn

Choose numbers, shapes or letters in the box under the title. The
heart could be any number at all, and the pattern still holds. That is
all a letter in algebra means.

<div class="dl-world" data-world="numbers">

```question
id: your-turn-1--numbers
type: fill-in-the-blank

3²/3⁶ is
{3⁻⁴|3⁴|3⁸}.

That is
{1/3⁴|−3⁴|3⁴}.

3⁴ is 81, so this is the fraction
{1/81|1/12|81}.
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: your-turn-1--squiggles
type: fill-in-the-blank

△³/△⁵ is
{△⁻²|△²|△⁸}.

That is
{1/△²|−△²|△²}.

★⁴/★⁵ is
{★⁻¹|★|★⁹},
which is 1/★.
```

</div>

<div class="dl-world" data-world="letters">

```question
id: your-turn-1--letters
type: fill-in-the-blank

b³/b⁷ is
{b⁻⁴|b⁴|b¹⁰}.

That is
{1/b⁴|−b⁴|b⁴}.

n⁴/n⁵ is
{n⁻¹|n|n⁹},
which is 1/n.
```

</div>

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Write the top and the bottom the long way.
2. Cross out pairs, one from the top and one from the bottom.
3. Count what is left on the bottom. The top is 1.

**Think about:** the subtracting rule, top exponent minus bottom
exponent, gives the same answer as step 3.

**Try this next:** a power over the same power with 10 more, like
♡¹/♡¹¹.

</details>

## A slice of pizza

This step is a stretch. In *Fractions: one whole pizza, many slices*,
a pizza is cut into ♡ slices. Each slice is $\frac{1}{\heartsuit}$. Now we have another name
for one slice: $\heartsuit^{-1}$.

What happens if we multiply $\heartsuit$ by $\heartsuit^{-1}$?

```question
id: a-slice-of-pizza-1
type: fill-in-the-blank

♡ × ♡⁻¹ is ♡ slices of size 1/♡. Together they make
{1|♡|0}.

In *Multiplying powers: joining two stacks*, we add the exponents.
Here that is 1 + (−1), which is
{0|2|−1}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Choose a number for the heart, like 4.
2. 4⁻¹ is 1/4, one slice of a pizza cut into 4.
3. 4 × 1/4 is 4 of those slices. How much pizza is that?

**Think about:** what ♡⁰ is, from *The zero power: when everything
cancels*.

**Try this next:** ♡³ × ♡⁻³.

</details>

The two answers agree. $\heartsuit \times \heartsuit^{-1} =
\heartsuit^0$, and that is 1. A number and its negative power make one
whole, like all the slices of a pizza.

{{include: setup/zen-calm-check.md}}

## Your rule, in your words

The worksheet asks for your rule in your own words. What does a
negative power mean? And how can you divide $\heartsuit^2$ by
$\heartsuit^5$ without drawing any hearts? Write it in the Notes panel
or on paper, or say it aloud.

<details class="dl-answer"><summary>one way to say it</summary>

A negative power is one over the power: $\heartsuit^{-3} =
\frac{1}{\heartsuit^3}$. The minus sign says that the hearts are on the
bottom. When we divide two powers of the same base, we subtract the
exponents in the same way. If the bottom has more, the answer has a negative
exponent. Your way of saying it may be clearer than ours.

</details>

## Make your own

Can you make five divisions of powers where the bottom has more? Write
each answer in two ways: as a negative power, and as one over a power.
Try one with numbers, one with a shape and one with a letter. Can you
make one whose answer is $\frac{1}{\heartsuit}$? And one with very big
exponents, like 1000?

## Looking back

The minus sign in $2^{-3}$ does not make the number negative. What
does it tell you?

A challenge: the program below prints the powers of 2, from $2^5$ down
to $2^{-5}$. Each line is half of the line above it. Can you change it
to show the powers of 10? Which line is one millimetre, in metres?

```python challenge
# The powers of 2, from 2 to the power 5 down to 2 to the power -5.
from fractions import Fraction

for exponent in range(5, -6, -1):
    print("2 **", exponent, "=", Fraction(2) ** exponent)
```

## Read more

Maths is Fun has a short page on [negative
exponents](https://www.mathsisfun.com/algebra/negative-exponents.html),
with more pictures. Wikipedia's page on
[exponentiation](https://en.wikipedia.org/wiki/Exponentiation#Negative_exponents)
has a section on negative powers. Its page on [metric
prefixes](https://en.wikipedia.org/wiki/Metric_prefix) lists the names
for other powers of ten, from very big to very small.
