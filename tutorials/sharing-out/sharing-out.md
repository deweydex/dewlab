---
title: "Dividing powers: crossing out pairs"
year: "2026-2027"
version: 2026.09.27.1
worlds:
  numbers: Normal numbers, like 3 and 10.
  squiggles: Shapes like ♡ and △, which can stand for any number.
  letters: Letters like b and n, which can stand for any number.
---

# Dividing powers: crossing out pairs

Here is a fraction made of hearts. On the top, five hearts are
multiplied together: ♡⁵. On the bottom, two hearts are multiplied
together: ♡². Some of the tiles have a line through them.

<img src="cancel-five-over-two.svg" alt="A fraction made of heart tiles. The top row has five hearts and the bottom row has two. The first two hearts on the top, and both hearts on the bottom, have a line through them. The last three hearts on the top have no line.">

```question
id: hearts-with-a-line-1
type: fill-in-the-blank

On the top,
{3|5|2}
hearts have no line through them.

On the bottom,
{0|2|3}
hearts have no line through them.
```

## Why a line?

Each heart with a line has a partner. One heart is on the top, and its
partner is on the bottom, under it. Together they make a fraction:

$$\frac{\heartsuit}{\heartsuit}$$

On [the pizza page](tutorial:one-whole-many-slices), a fraction with the
same top and bottom was one whole pizza. So ♡/♡ = 1. Each pair is worth
1, and multiplying by 1 changes nothing. So we can remove the pair. To
show this, we draw a line through both hearts. This is called *crossing
out* the pair.

```question
id: why-a-line-1
type: multiple-choice
answer: 3

Two pairs are crossed out. Each pair is ♡/♡. What are the two pairs
worth together?

- 0
  - A line through a heart can look like nothing is there. But each
    pair is worth 1, not 0.
- 2
  - There are two pairs, each worth 1. But the pairs are multiplied,
    not added.
- 1
  - Each pair is 1, and 1 × 1 = 1.
```

## What is left

Three hearts on the top have no partner. They are what is left.

```question
id: what-is-left-1
type: fill-in-the-blank

♡⁵/♡² is ♡ × ♡ × ♡, which is
{♡³|♡⁷|♡¹⁰}.
```

## Seven over three

Here is another one: seven hearts on the top, and three on the bottom.

<img src="cancel-seven-over-three.svg" alt="A fraction made of heart tiles. The top row has seven hearts and the bottom row has three. The first three hearts on the top, and all three hearts on the bottom, have a line through them. The last four hearts on the top have no line.">

```question
id: seven-over-three-1
type: fill-in-the-blank

The picture crosses out
{3|4|7}
pairs.

On the top,
{4|3|10}
hearts are left.

So ♡⁷/♡³ is
{♡⁴|♡¹⁰|♡²¹}.
```

## Without a picture

Now there is no picture. Write the top and the bottom the long way.
Cross out the pairs, and count what is left. Choose numbers, shapes or
letters in the box under the title.

<div class="dl-world" data-world="numbers">

```question
id: without-a-picture-1--numbers
type: fill-in-the-blank

2⁶/2² has 2 × 2 × 2 × 2 × 2 × 2 on the top, and 2 × 2 on the bottom.

We can cross out
{2|4|6}
pairs.

What is left is
{2⁴|2³|2⁸}.
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: without-a-picture-1--squiggles
type: fill-in-the-blank

△⁶/△² has △ × △ × △ × △ × △ × △ on the top, and △ × △ on the bottom.

We can cross out
{2|4|6}
pairs.

What is left is
{△⁴|△³|△⁸}.
```

</div>

<div class="dl-world" data-world="letters">

```question
id: without-a-picture-1--letters
type: fill-in-the-blank

a⁶/a² has a × a × a × a × a × a on the top, and a × a on the bottom.

We can cross out
{2|4|6}
pairs.

What is left is
{a⁴|a³|a⁸}.
```

</div>

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Write the top the long way, in a row.
2. Write the bottom the long way, in a row under it.
3. Draw a line through one tile on the top and one on the bottom. Do it
   again, until every tile on the bottom has a line.

**Think about:** each pair you cross out is worth 1.

**Try this next:** 2⁶ is 64, and 2² is 4. What is 64 ÷ 4? Is it the
same as your answer?

</details>

## Bigger stacks

<div class="dl-world" data-world="numbers">

```question
id: bigger-stacks-1--numbers
type: fill-in-the-blank

3¹⁰/3³ crosses out
{3|7|10}
pairs.

So 3¹⁰/3³ is
{3⁷|3¹³|3³⁰}.

3¹⁰⁰/3⁹⁸ is
{3²|3¹⁹⁸|1}.
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: bigger-stacks-1--squiggles
type: fill-in-the-blank

♡¹⁰/♡³ crosses out
{3|7|10}
pairs.

So ♡¹⁰/♡³ is
{♡⁷|♡¹³|♡³⁰}.

♡¹⁰⁰/♡⁹⁸ is
{♡²|♡¹⁹⁸|1}.
```

</div>

<div class="dl-world" data-world="letters">

```question
id: bigger-stacks-1--letters
type: fill-in-the-blank

b¹⁰/b³ crosses out
{3|7|10}
pairs.

So b¹⁰/b³ is
{b⁷|b¹³|b³⁰}.

b¹⁰⁰/b⁹⁸ is
{b²|b¹⁹⁸|1}.
```

</div>

Did you draw a hundred tiles for the last one? Or did you find another
way to count?

{{include: setup/zen-calm-check.md}}

## A quicker way

Here is what we found so far:

$$\frac{\heartsuit^5}{\heartsuit^2} = \heartsuit^3 \qquad \frac{\heartsuit^7}{\heartsuit^3} = \heartsuit^4 \qquad \frac{\heartsuit^6}{\heartsuit^2} = \heartsuit^4 \qquad \frac{\heartsuit^{10}}{\heartsuit^3} = \heartsuit^7$$

```question
id: a-quicker-way-1
type: multiple-choice
answer: 2

Look only at the small numbers. How can you find the exponent after
the equals sign, without crossing out any tiles?

- Add the two exponents
  - Adding worked on the last page, for multiplying. Here 5 + 2 = 7,
    but only 3 hearts are left.
- Take the bottom exponent away from the top one
  - 5 − 2 = 3, 7 − 3 = 4, 6 − 2 = 4, and 10 − 3 = 7.
- Divide the top exponent by the bottom one
  - 6 ÷ 2 = 3, but ♡⁶/♡² left 4 hearts. And 5 ÷ 2 is not a whole
    number.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Take the first one. The small number on the top is 5, and on the
   bottom it is 2.
2. The small number after the equals sign is 3.
3. What can you do to 5 and 2 to get 3?

**Think about:** each pair crossed out takes one heart from the top.

**Try this next:** does the same thing work for 7 and 3?

</details>

Each heart on the bottom crosses out one heart on the top. So the top
loses as many hearts as the bottom has. We take the bottom exponent
away from the top exponent. Taking away is also called *subtracting*.

This is a rule. When we divide two powers with the same base, we
subtract their exponents. Many books call it the *quotient rule* for
powers. A *quotient* is the answer to a division. Here is the rule with
shapes:

$$\frac{\heartsuit^{\triangle}}{\heartsuit^{\square}} = \heartsuit^{\triangle - \square}$$

On this page, the top always has more hearts than the bottom. So △ is
bigger than □. The heart can be any number except 0, because we cannot
divide by 0. Here is the same rule with letters:

$$\frac{a^m}{a^n} = a^{m - n}$$

<div class="dl-world" data-world="numbers">

```question
id: a-quicker-way-2--numbers
type: fill-in-the-blank

5¹²/5⁸ is
{5⁴|5²⁰|1⁴}.
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: a-quicker-way-2--squiggles
type: fill-in-the-blank

♡¹²/♡⁸ is
{♡⁴|♡²⁰|4♡}.
```

</div>

<div class="dl-world" data-world="letters">

```question
id: a-quicker-way-2--letters
type: fill-in-the-blank

d¹²/d⁸ is
{d⁴|d²⁰|4d}.
```

</div>

## Join, then cross out

The rule from the last page and the rule from this page can work
together. Here the top is two stacks, multiplied.

<div class="dl-world" data-world="numbers">

```question
id: join-then-cross-out-1--numbers
type: fill-in-the-blank

The top of (2⁵ × 2³)/2⁴ joins into
{2⁸|2¹⁵|4⁸}.

Then crossing out pairs leaves
{2⁴|2¹²|2²}.
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: join-then-cross-out-1--squiggles
type: fill-in-the-blank

The top of (♡⁵ × ♡³)/♡⁴ joins into
{♡⁸|♡¹⁵|8♡}.

Then crossing out pairs leaves
{♡⁴|♡¹²|♡²}.
```

</div>

<div class="dl-world" data-world="letters">

```question
id: join-then-cross-out-1--letters
type: fill-in-the-blank

The top of (c⁵ × c³)/c⁴ joins into
{c⁸|c¹⁵|8c}.

Then crossing out pairs leaves
{c⁴|c¹²|c²}.
```

</div>

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Look at the top only. It is two stacks, multiplied. Join them into
   one row.
2. Count the row. That is the top's exponent.
3. Now it is one stack over one stack. Cross out the pairs.

**Think about:** the order: first the top, then the whole fraction.

**Try this next:** what is (♡⁶ × ♡⁶)/♡¹⁰?

</details>

## A checking machine

Python can check the rule with numbers. In Python, `/` means divide.
So `2 ** 7 / 2 ** 3` means 2⁷ ÷ 2³.

```python exec
id: a-checking-machine-1
print(2 ** 7 / 2 ** 3)
print(2 ** 4)
print(2 ** 10)
```

```predict
type: choice

Before you run it: the first line is 2⁷ ÷ 2³. Which other line will
print the same number?

- The second line, 2 ** 4
- The third line, 2 ** 10
  - 7 + 3 = 10. Adding the exponents worked on the last page, for
    multiplying.
- Neither of them
  - Dividing can feel like it should give a fraction, not a power.
```

The first line prints 16.0. Python writes the answer to a `/` division
with a decimal point. 16.0 is the same number as 16. The second line
prints 16, and the third prints 1024.

Now change the numbers and run it again. Keep the top exponent bigger
than the bottom one. Later pages are about the other cases.

{{include: setup/zen-calm-check.md}}

## Your rule, in your words

Before you read our version, say the rule of this page in your own
words. Write it in the Notes panel or on paper, or say it aloud.

<details class="dl-answer"><summary>one way to say it</summary>

To divide two powers with the same base, write the top and the bottom
the long way. Each tile on the bottom crosses out one tile on the top,
because ♡/♡ = 1. What is left on the top is the answer. So we take the
bottom exponent away from the top exponent, and keep the base. Your way
of saying it may be clearer than ours.

</details>

## Make your own

Can you make five divisions of powers, with more on the top than on the
bottom? Write each answer as one power. Try one with a very big
exponent, and one where the top is two stacks. Can you make one whose
answer is ♡¹?

## Looking back

On the pizza page, a fraction with the same top and bottom was one
whole pizza. Where did that idea help on this page?

A challenge: the program below prints many divisions of two powers of
2. The top always has the bigger exponent. Can you change it, so that
it prints only the divisions that give 8? What do those divisions have
in common?

```python challenge
# Divisions of two powers of 2, with more on the top.
for top in range(1, 11):
    for bottom in range(1, top):
        answer = 2 ** top / 2 ** bottom
        print("2 **", top, "/ 2 **", bottom, "=", answer)
```

## Read more

Maths is Fun has a page on the [laws of
exponents](https://www.mathsisfun.com/algebra/exponent-laws.html). Its
part on dividing writes the letters the long way, as we did here. The page before this one is [Multiplying powers:
joining two stacks](tutorial:joining-two-stacks).
