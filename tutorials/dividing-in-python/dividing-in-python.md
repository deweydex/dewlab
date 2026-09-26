---
title: "Dividing: a closer look at //, / and 0.1"
year: "2026-2027"
version: 2026.09.26.1
---

# Dividing: a closer look at //, / and 0.1

In [Algorithms, pseudocode and your first Python](tutorial:first-steps#a-few-more-things-python-can-do),
`17 // 5` gave 3: the number of whole fives in 17. With positive numbers,
`//` looks like it removes the part after the decimal point. Here are two
ideas about what it does. Both are reasonable, and they cannot both be
true.

**Idea A.** `//` divides, then removes everything after the decimal point.
`7 / 2` is 3.5, so `7 // 2` is 3.

**Idea B.** `//` divides, then rounds down, to the whole number just below
the answer. 3.5 rounds down to 3.

For 7 and 2, both ideas give 3. We need a case where they give different
answers.

## An experiment

`-7 / 2` is -3.5. Idea A removes the .5 and gives -3. Idea B rounds down.
On a number line, the whole number just below -3.5 is -4, so idea B gives
-4.

```python exec
id: an-experiment-1
print(-7 / 2)
print(-7 // 2)
```

```predict
type: number

What will the last line print?
```

Run it. It prints -4, as idea B predicts. "Down" means towards the left of
the number line, and for a negative number, that is away from zero.

Can you find a division where `//` gives the same answer as removing the
decimal part, and one where it does not? What decides which?

<details class="dl-answer"><summary>what decides it</summary>

When the answer of `/` is positive, rounding down and removing the decimal
part give the same answer: `7 // 2` is 3. When it is negative and not
whole, rounding down gives the next number further from zero: `-7 // 2` is
-4. When the division is exact, there is nothing to remove or round:
`-8 // 2` is -4.

</details>

## Why idea A feels right

Most of the numbers we divide are positive: people, prices, minutes. For
all of them, removing the decimals and rounding down give the same answer.
So we learn the shortcut, "ignore the decimals", and it works every time,
until we divide a negative number.

Python's rule is the one that makes `//` and `%` fit together.
`-7 // 2` is -4 and `-7 % 2` is 1, and $-4 \times 2 + 1 = -7$, the number
we started with. The whole number and the remainder always rebuild the
number, and the remainder is never negative when you divide by a positive
number.

## Where else it happens

Decimals have a surprise of their own. What will this print?

```python exec
id: where-else-it-happens-1
print(0.1 * 3)
print(0.3)
```

```predict
type: choice

Will the two lines be the same?

- Yes
  - Three tenths are 0.3.
- No
```

It prints 0.30000000000000004, and then 0.3. A computer stores numbers in
binary, and 0.1 has no exact binary form, in the same way that a third has
no exact decimal form (0.333…). 0.1 is stored as the nearest number the
computer can hold, and multiplying by 3 makes the small difference bigger.

So two calculations that should give the same decimal can differ in the
last few digits. Later pages compare floats by asking whether they are
close, not whether they are exactly the same.

## Where to read more

The Python tutorial has a short page on why 0.1 is not exact:
[Floating-point arithmetic: issues and limitations](https://docs.python.org/3/tutorial/floatingpoint.html).
