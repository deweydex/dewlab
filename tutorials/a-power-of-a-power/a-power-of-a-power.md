---
title: "A power of a power: stacks of stacks"
year: "2026-2027"
version: 2026.09.27.1
worlds:
  numbers: Normal numbers, like 3 and 10.
  squiggles: Shapes like ♡ and △, which can stand for any number.
  letters: Letters like b and n, which can stand for any number.
---

# A power of a power: stacks of stacks

Here are three boxes. Each box holds two hearts, multiplied together.
The three boxes are multiplied together too.

<img src="two-in-three-boxes.svg" alt="Three boxes side by side. Each box holds 2 hearts. Under the boxes, a label says: 3 boxes of 2 = 6.">

```question
id: three-boxes-1
type: multiple-choice
answer: 1

All the hearts in all the boxes are multiplied together. Which power
is that?

- ♡⁶
  - There are 3 boxes, with 2 hearts in each. That is 6 hearts.
- ♡⁵
  - That is 2 + 3. Adding the two numbers feels natural. Count the
    hearts in the picture.
- ♡⁸
  - That is 2³, which is 8. Count the hearts in the picture.
- ♡⁹
  - That is 3², which is 9. There are only 3 boxes of 2.
```

## One box, three times

One box holds ♡ × ♡. That is $\heartsuit^2$. So the three boxes are

$$\heartsuit^2 \times \heartsuit^2 \times \heartsuit^2$$

That is the same thing, multiplied 3 times. So it is a power too. The
box is its base, and 3 is its exponent. We put the box in brackets,
and write the 3 outside:

$$\left(\heartsuit^2\right)^3 = \heartsuit^2 \times \heartsuit^2 \times \heartsuit^2$$

A power in brackets, with another exponent outside, is called a *power
of a power*.

```question
id: one-box-three-times-1
type: fill-in-the-blank

(♡²)³ the long way is
{♡² × ♡² × ♡²|♡² × 3|♡² + ♡² + ♡²}.

So (♡²)³ is ♡ to the power
{6|5|8}.
```

## Two boxes of three

Here is a second picture. This time there are two boxes, and each box
holds three hearts.

<img src="three-in-two-boxes.svg" alt="Two boxes side by side. Each box holds 3 hearts. Under the boxes, a label says: 2 boxes of 3 = 6.">

```question
id: two-boxes-of-three-1
type: fill-in-the-blank

Each box is
{♡³|♡²|♡⁶}.

Two of these boxes are written
{(♡³)²|(♡²)³|♡³ × 2}.

In total, there are
{6|5|9}
hearts.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Count the hearts in one box. That is the exponent inside the
   brackets.
2. Count the boxes. That is the exponent outside the brackets.
3. Count every heart in the picture.

**Think about:** the first picture had 3 boxes of 2. This one has 2
boxes of 3.

**Try this next:** how many hearts are in 4 boxes of 2?

</details>

## Stacks of stacks, or two stacks?

In *Multiplying powers: joining two stacks*, we joined $\heartsuit^2$
and $\heartsuit^3$ into one stack. Here, we have stacks of stacks. They
look alike, so let's look at them side by side.

```question
id: stacks-of-stacks-or-two-stacks-1
type: fill-in-the-blank

♡² × ♡³ is one stack of 2 and one stack of 3. That is ♡ to the power
{5|6}.

(♡²)³ is 3 stacks of 2. That is ♡ to the power
{6|5}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Write ♡² × ♡³ the long way. Count the hearts.
2. Write (♡²)³ the long way: ♡² three times. Then write each ♡² as
   ♡ × ♡.
3. Count the hearts again.

**Think about:** how many stacks there are in each one.

**Try this next:** ♡² × ♡² and (♡²)². Are they the same?

</details>

## Bigger boxes

With bigger numbers, drawing every heart is slow. We can picture the
boxes instead, and count.

```question
id: bigger-boxes-1
type: fill-in-the-blank

(♡⁴)³ is 3 boxes, with 4 hearts in each box. That is ♡ to the power
{12|7|64}.

(♡⁵)¹⁰ is 10 boxes, with 5 hearts in each box. That is ♡ to the power
{50|15|510}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The exponent inside the brackets is the hearts in one box.
2. The exponent outside is the number of boxes.
3. Count the hearts box by box: 5, 10, 15, … one box at a time.

**Think about:** a faster way to count 10 boxes of 5.

**Try this next:** (♡¹⁰)⁵. Is it the same as (♡⁵)¹⁰?

</details>

{{include: setup/zen-calm-check.md}}

## With numbers

Now let's check the idea with numbers. Take $\left(2^3\right)^2$.

```question
id: with-numbers-1
type: fill-in-the-blank

2³ is
{8|6|9}.

So (2³)² is 8 × 8, which is
{64|16|12}.

2⁶ is
{64|12|32}.
```

Counting says $\left(2^3\right)^2$ is 2 boxes of 3, so it is $2^6$. The
numbers agree. Both are 64. Python can check it. Python writes a power
with two stars, and the brackets say which power to find first.

```python exec
id: with-numbers-2
print((2 ** 3) ** 2)
print(2 ** 6)
```

## A surprise

In [Powers: the long way and the short
way](tutorial:the-long-way), $2^3$ was 8 and $3^2$ was 9. We swapped
the base and the exponent, and the answer changed.

Here is a different swap. We keep the base, and swap the two
exponents. $\left(2^3\right)^4$ is 4 boxes of 3 twos.
$\left(2^4\right)^3$ is 3 boxes of 4 twos. In Python, `==` asks "is
this equal to that?"

```python exec
id: a-surprise-1
print((2 ** 3) ** 4)
print((2 ** 4) ** 3)
print((2 ** 3) ** 4 == (2 ** 4) ** 3)
```

```predict
type: choice

Before you run it: what will the last line print? `True` means the two
are the same amount.

- True
- False
  - Swapping changed the answer for 2³ and 3², so it feels likely to
    change here too.
```

Both are 4096. Count the twos: 4 boxes of 3 is 12 twos, and 3 boxes of
4 is 12 twos too. $3 \times 4$ and $4 \times 3$ are both 12. The two
pictures at the top of this page showed the same thing: 3 boxes of 2
and 2 boxes of 3 both hold 6 hearts.

```question
id: a-surprise-2
type: fill-in-the-blank

(s³)⁴ and (s⁴)³ are both s to the power
{12|7|81}.
```

## What do we do with the exponents?

Look back at the counting on this page:

- 3 boxes of 2 made 6.
- 2 boxes of 3 made 6.
- 3 boxes of 4 made 12.
- 10 boxes of 5 made 50.

```question
id: what-do-we-do-1
type: multiple-choice
answer: 1

What do we do with the two exponents, to count all the hearts?

- Multiply them
  - The number of boxes, times the hearts in each box.
- Add them
  - Adding is for joining two stacks, like ♡² × ♡³. Here there are
    more than two stacks.
- Raise one to the power of the other
  - 2³ is 8, but 3 boxes of 2 is only 6 hearts.
```

## Your turn

Choose numbers, shapes or letters in the box under the title. The
heart could be any number at all, and the pattern still holds. That is
all a letter in algebra means.

<div class="dl-world" data-world="numbers">

```question
id: your-turn-1--numbers
type: fill-in-the-blank

(10²)³ is 10 to the power
{6|5|8}.

That is
{1,000,000|100,000|1000}.

(5²)⁴ is 5 to the power
{8|6|16}.
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: your-turn-1--squiggles
type: fill-in-the-blank

(△⁵)² is △ to the power
{10|7|25}.

(★³)⁵ is ★ to the power
{15|8|243}.

(□¹)⁷ is □ to the power
{7|8|1}.
```

</div>

<div class="dl-world" data-world="letters">

```question
id: your-turn-1--letters
type: fill-in-the-blank

(b⁴)⁵ is b to the power
{20|9|1024}.

(c²)⁷ is c to the power
{14|9|128}.

(d¹)⁷ is d to the power
{7|8|1}.
```

</div>

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Picture the boxes. The exponent outside is the number of boxes.
2. The exponent inside is the number in each box.
3. Count them all.

**Think about:** a box with only one in it.

**Try this next:** (♡²)¹⁰⁰.

</details>

## Two kinds in a box

This step is a stretch. Here, each box holds two hearts and a triangle:
♡ × ♡ × △. There are 3 boxes.

$$\left(\heartsuit^2 \triangle\right)^3 = \left(\heartsuit^2 \triangle\right) \times \left(\heartsuit^2 \triangle\right) \times \left(\heartsuit^2 \triangle\right)$$

```question
id: two-kinds-in-a-box-1
type: fill-in-the-blank

In total, there are
{6|2|3}
hearts, and
{3|1|6}
triangles.

So (♡²△)³ is
{♡⁶△³|♡⁶△|♡⁵△³}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Write the three boxes the long way, every heart and every triangle.
2. Count the hearts.
3. Count the triangles. There is one in each box.

**Think about:** the exponent outside reaches everything inside the
brackets.

**Try this next:** (♡△²)².

</details>

{{include: setup/zen-calm-check.md}}

## Your rule, in your words

The worksheet asks for your rule in your own words. How can you find a
power of a power, like $\left(\heartsuit^4\right)^3$, without drawing
any boxes? Write it in the Notes panel or on paper, or say it aloud.

<details class="dl-answer"><summary>one way to say it</summary>

A power of a power is boxes of hearts. The exponent inside the brackets
says how many hearts are in each box. The exponent outside says how
many boxes there are. To count all the hearts, multiply the two
exponents: $\left(\heartsuit^4\right)^3 = \heartsuit^{12}$. Swapping
the two exponents does not change the answer. Your way of saying it may
be clearer than ours.

</details>

## Make your own

Can you make five powers of powers of your own, and find each one? Try
one with very big exponents, one with a shape and one with a letter.
Can you make three different ones that all come to $\heartsuit^{24}$?

## Looking back

Joining two stacks adds the exponents. Stacks of stacks multiply them.
When you meet a new problem, how can you tell which one it is?

A challenge: the program below finds $\left(2^3\right)^2$ and
$2^{\left(3^2\right)}$. The numbers are the same, but the brackets are
in different places. Guess first: do they give the same answer? Then
add a line with no brackets at all, `print(2 ** 3 ** 2)`. Which of the
two does Python find?

```python challenge
# The same three numbers, with the brackets in two different places.
print((2 ** 3) ** 2)
print(2 ** (3 ** 2))
```

## Read more

Maths is Fun has a page on the [laws of
exponents](https://www.mathsisfun.com/algebra/exponent-laws.html),
with this page's rule and the ones before it. Wikipedia's page on
[exponentiation](https://en.wikipedia.org/wiki/Exponentiation#Identities_and_properties)
has a section on the rules for powers.
