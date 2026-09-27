---
title: "Dividing fractions: how many fit?"
year: "2026-2027"
version: 2026.09.27.1
---

# Dividing fractions: how many fit?

Here are 3 pizzas. Each pizza is cut into 4 equal slices, so each slice
is a quarter of a pizza.

<img src="three-pizzas-in-quarters.svg" alt="Three pizzas side by side. Each is cut into 4 equal slices, and every slice is shaded. Under each pizza is the label '4 quarters'.">

```question
id: three-pizzas-1
type: multiple-choice
answer: 1

How many quarter slices are there in total?

- 12
  - Each pizza has 4 quarters, and there are 3 pizzas.
- 3/4
  - 3 and a quarter are both in the question. But 3/4 is less than one
    pizza, and here we have three.
- 7
  - That adds the 3 pizzas and the 4 slices. Count the slices in the
    picture.
- 4
  - One pizza has 4 quarters. There are 3 pizzas.
```

## How many fit?

Here is a question with whole numbers first. How many 2s fit in 10?
Count in twos: 2, 4, 6, 8, 10. Five 2s fit. We write this as a
division:

$$10 \div 2 = 5$$

The sign $\div$ means *divided by*. One way to read $10 \div 2$ is "how
many 2s fit in 10?"

```question
id: how-many-fit-1
type: fill-in-the-blank

12 ÷ 3 asks how many {3s|12s|4s} fit in 12.

The answer is {4|36|9}.
```

## How many quarters fit in 3?

Now back to the pizzas. We found that 12 quarters fit in 3 pizzas. That
is a division too, with a fraction:

$$3 \div \frac{1}{4} = 12$$

```question
id: how-many-quarters-1
type: multiple-choice
answer: 1

We divided 3 by a quarter, and got 12. The answer is bigger than 3. Why?

- A quarter is small, so many of them fit
  - The smaller the slice, the more slices fit in the same pizzas.
- Dividing always makes a number bigger
  - 10 ÷ 2 = 5 made a number smaller. Look at what we divide by.
- The picture has too many slices
  - Count them again: 4 in each of 3 pizzas.
```

Dividing by a whole number, like 2, made 10 smaller. Dividing by a
quarter made 3 bigger. A quarter is smaller than 1, so more than one of
them fits in every pizza.

## How many quarters fit in a half?

Here is a wall of bars from *Equivalent fractions: the same amount,
different names*. The top bar is one whole. The next is cut into
halves, and the last into quarters.

<img src="half-in-quarters.svg" alt="A fraction wall of three bars of the same length. The top bar is one whole. The second is cut into 2 halves, and the left half is shaded. The third is cut into 4 quarters, and the 2 left quarters are shaded. The shaded half and the 2 shaded quarters end at the same place.">

```question
id: quarters-in-a-half-1
type: fill-in-the-blank

The number of quarters that fit in one half is {2|4|1/2}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Put your finger on the shaded half, in the second bar.
2. Move your finger straight down to the quarters.
3. Count the quarters under the half.

**Think about:** "how many fit" is a count. It is a whole number here.

**Try this next:** how many quarters fit in one whole bar?

</details>

So $\frac{1}{2} \div \frac{1}{4} = 2$.

## How many quarters fit in 1?

One pizza has 4 quarter slices. So 4 quarters fit in 1:

$$1 \div \frac{1}{4} = 4$$

This is the idea from [Fractions: one whole pizza, many
slices](tutorial:one-whole-many-slices). There, 4 slices of a quarter
made the whole pizza:

$$\frac{1}{4} \times 4 = 1$$

```question
id: quarters-in-one-1
type: fill-in-the-blank

1 ÷ 1/8 is {8|1/8|9}.

A whole pizza is {8|1|16} slices of one eighth.
```

{{include: setup/zen-calm-check.md}}

## A pattern

Here are our three answers together.

| How many quarters fit in… | Division | Answer |
|---|---|---|
| 1 pizza | $1 \div \frac{1}{4}$ | $4$ |
| 3 pizzas | $3 \div \frac{1}{4}$ | $12$ |
| half a pizza | $\frac{1}{2} \div \frac{1}{4}$ | $2$ |

Look at each answer. Is it 4 times something?

```question
id: a-pattern-1
type: fill-in-the-blank

Dividing by 1/4 gives the same answer as multiplying by {4|1/4|2}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The first row: 1 pizza holds 4 quarters. What is 1 × 4?
2. The second row: 3 pizzas. What is 3 × 4?
3. The third row: half a pizza. What is half of 4?

**Think about:** every whole pizza holds 4 quarters. So we count the
pizzas, and multiply by 4.

**Try this next:** dividing by 1/3. What would you multiply by instead?

</details>

Every whole holds 4 quarters. So to count the quarters, we count the
wholes and multiply by 4.

## Turning a fraction over

What about a fraction with a top that is not 1? How many two thirds fit
in 2 pizzas? Cut both pizzas into thirds. That makes 6 thirds. Now put
them in pairs. Each pair is two thirds, and there are 3 pairs.

$$2 \div \frac{2}{3} = 3$$

Now turn $\frac{2}{3}$ over, so the top goes to the bottom. We get
$\frac{3}{2}$. Multiply 2 by it:

$$2 \times \frac{3}{2} = \frac{6}{2} = 3$$

We get the same answer. A quarter works the same way. $\frac{1}{4}$
turned over is $\frac{4}{1}$, which is 4.

```question
id: turning-it-over-1
type: multiple-choice
answer: 2

Which is the same as 5 ÷ 3/4?

- 5 × 3/4
  - That is 5 times three quarters. We asked how many three
    quarters fit in 5.
- 5 × 4/3
  - Dividing by a fraction is multiplying by it turned over.
- 5 ÷ 4/3
  - The fraction is turned over. But the ÷ needs to change to × too.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. In the example, 2 ÷ 2/3 became 2 × 3/2.
2. Two things changed: the sign, and the fraction.
3. Make the same two changes to 5 ÷ 3/4.

**Think about:** 3/4 is smaller than 1, so more than 5 of them fit in
5. Which choice gives an answer bigger than 5?

**Try this next:** what is 1 ÷ 2/5 as a multiplication?

</details>

## The partner that makes 1

Multiply a fraction by itself turned over. Here are two:

$$\frac{1}{4} \times \frac{4}{1} = \frac{4}{4} = 1 \qquad \frac{2}{3} \times \frac{3}{2} = \frac{6}{6} = 1$$

The top and the bottom of the answer are always the same number. So the
answer is always 1. That is the first page's idea again: all the slices
make the whole pizza.

```question
id: the-partner-1
type: fill-in-the-blank

The partner of 5/7 is {7/5|5/7|1/7}.

5/7 × 7/5 is {1|25/49|35}.
```

A fraction turned over is called its *reciprocal*. A number times its
reciprocal is always 1. So dividing by a fraction is the same as
multiplying by its reciprocal.

## A machine that checks

The first line gets Python's `Fraction` tool ready. In Python, the sign
for dividing is a slash, `/`. `Fraction(3)` is the whole number 3,
written as a fraction.

```python exec
id: a-machine-that-checks-1
from fractions import Fraction

print(Fraction(3) / Fraction(1, 4))
```

```predict
type: choice

Before you run it: what is 3 ÷ 1/4?

- 12
  - Twelve quarter slices fit in 3 pizzas.
- 3/4
  - That is 3 times a quarter.
- 1/12
  - Dividing by 4 would make 3 smaller. We divide by a quarter.
```

Python prints 12, the number of slices in the picture at the top. Now
change the numbers. Can you check $\frac{1}{2} \div \frac{1}{4}$, and
$2 \div \frac{2}{3}$?

## Slices of nothing

Here is one last question. How many slices of nothing fit in a pizza?
A slice of size 0 has no pizza in it. Put 10 of them together, or a
million. You still have no pizza.

The cell below asks Python for $1 \div 0$. **This cell is meant to
fail.** Run it and read the last line.

```python exec
id: slices-of-nothing-1
print(1 / 0)
```

```predict
type: choice

What will Python do?

- Print 0
  - A slice of nothing feels like it should give nothing.
- Print a very big number
  - Thinner slices gave more slices. A slice of nothing could seem to
    give the most of all.
- Stop with an error
  - No number of empty slices ever makes a pizza.
```

Python stops with an error. The last line says `ZeroDivisionError:
division by zero`. You did not break anything. No number of empty
slices makes a pizza, so there is no number for Python to print. This is also why 0 has no partner. No number times 0
makes 1.

{{include: setup/zen-calm-check.md}}

## Your rule, in your words

Before you read our version, say how to divide by a fraction in your
own words. Write it in the Notes panel or on paper, or say it aloud.

<details class="dl-answer"><summary>one way to say it</summary>

Dividing by a fraction asks how many of that fraction fit. It gives
the same answer as multiplying by the fraction turned over. A fraction
and the same fraction turned over are partners. Multiplied together,
they make 1. Your way of saying it may be clearer than ours.

</details>

## Make your own

Can you make five division problems of your own, each with a fraction?
Here are some ideas:

- one where the answer is 100
- one where a fraction is divided by a fraction
- one where the answer is exactly 1
- one with a shape: $1 \div \frac{1}{\heartsuit}$

Check each one with `Fraction`, or with a picture.

## Looking back

On [Multiplying fractions: a fraction of a
fraction](tutorial:a-fraction-of-a-fraction), multiplying by a half made
a number smaller. On this page, dividing by a half makes a number
bigger. Why do the two go in opposite directions?

A challenge: the program below counts how many quarters fit in 3. It
adds one quarter at a time, and stops when the total gets to 3. Can
you change it to count how many two thirds fit in 2? How many one
tenths fit in 7?

```python challenge
# Count how many slices fit, by adding one slice at a time.
from fractions import Fraction

slice_size = Fraction(1, 4)
total = Fraction(0)
count = 0
while total < 3:
    total = total + slice_size
    count = count + 1
print(count)
```

## Read more

Wikipedia's page on fractions has a section on
[reciprocals](https://en.wikipedia.org/wiki/Fraction#Reciprocals_and_the_invisible_denominator),
and one on [dividing](https://en.wikipedia.org/wiki/Fraction#Division).
Its page on [division by
zero](https://en.wikipedia.org/wiki/Division_by_zero) says more about
why no number is the answer to $1 \div 0$.
