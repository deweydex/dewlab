---
title: "Multiplying: a closer look at bigger and smaller"
year: "2026-2027"
version: 2026.09.27.1
---

# Multiplying: a closer look at bigger and smaller

On [Multiplying fractions: a fraction of a fraction](tutorial:a-fraction-of-a-fraction),
half of a half was a quarter. We multiplied, and the answer was smaller
than both numbers we started with. Here are two ideas about multiplying.
Both make sense, and they cannot both be true.

**Idea A.** Multiplying always makes a number bigger.

**Idea B.** Multiplying by a number bigger than 1 makes a number
bigger. Multiplying by a number smaller than 1 makes it smaller.

## An experiment

The two ideas agree about $40 \times 3$. Both say the answer is bigger
than 40. They disagree about 40 times a half, and 40 times a quarter.
Idea A says these answers are bigger than 40 too. Idea B says they are
smaller.

The cell below multiplies 40 by four different numbers. The first line
gets the `Fraction` tool ready. In Python, the times sign is a star,
`*`, and 0.5 is a half, written as a decimal.

```python exec
id: an-experiment-1
from fractions import Fraction

print(40 * 3)
print(40 * 1)
print(40 * 0.5)
print(40 * Fraction(1, 4))
```

```predict
type: choice

Before you run it: what will the last two lines print?

- Two numbers bigger than 40
  - This is what idea A predicts.
- Two numbers smaller than 40
  - This is what idea B predicts.
- 40 both times
  - A half and a quarter are small. Multiplying by something small
    could seem to change nothing.
```

Run it. The four lines print 120, 40, 20.0 and 10. Python writes 20.0
with a decimal point, because 0.5 was a decimal.

- Multiplying by 3 made 40 bigger.
- Multiplying by 1 left 40 the same.
- Multiplying by a half made it smaller: half of 40 is 20.
- Multiplying by a quarter made it smaller again: a quarter of 40 is
  10.

So idea B matches what happens. The number we multiply by decides it.
Bigger than 1 makes the answer bigger. Smaller than 1 makes it smaller.
Exactly 1 changes nothing.

Can you find a number to multiply 40 by, so that the answer is exactly
41? Try a few in the cell.

<details class="dl-answer"><summary>one number that does it</summary>

$\frac{41}{40}$, which is a little bigger than 1. In the cell,
`40 * Fraction(41, 40)` prints 41. A number a little bigger than 1
makes the answer a little bigger.

</details>

## Why idea A feels so natural

Idea A comes from real experience.

At school, most people first met multiplying with whole numbers: the
times tables, $3 \times 4$, $7 \times 8$. Almost every one of those
numbers is bigger than 1. So almost every answer is bigger than the
numbers we started with. After years of these, the pattern feels like
a rule.

The words help the pattern too. "Three times" means three goes: three
bags of 4 apples. "Times" sounds like "more times". Nobody says "half a
time". So the word itself seems to promise more.

Idea A works for every multiplication in the times tables, except the
ones with 0 or 1. It stops working when fractions and decimals arrive.
For them, "of" is a better word than "times". "Half of 40" does not
sound like more than 40.

## Where else it happens

Dividing can surprise us too. Dividing by 2 makes
40 smaller. What does dividing by a half do? In Python, the sign for
dividing is a slash, `/`.

```python exec
id: where-else-it-happens-1
print(40 / 2)
print(40 / Fraction(1, 2))
```

```predict
type: number

What will the last line print?
```

It prints 80. Dividing by a number smaller than 1 makes the answer
bigger. $40 \div \frac{1}{2}$ asks how many halves fit in 40, and 80
halves fit. [Dividing fractions: how many fit?](tutorial:how-many-fit)
is about this.

## Where to read more

People who teach maths have argued about how to teach multiplying. Is
multiplying the same as adding again and again? Wikipedia's page
[Multiplication and repeated
addition](https://en.wikipedia.org/wiki/Multiplication_and_repeated_addition)
describes the argument. It also shows where fractions make "adding
again and again" hard to use.
