---
title: "Powers: a closer look at ** and ^"
year: "2026-2027"
version: 2026.09.26.1
---

# Powers: a closer look at ** and ^

In [Algorithms, pseudocode and your first Python](tutorial:first-steps#a-few-more-things-python-can-do),
`2 ** 3` gave 8: two to the power of three. Many people write a power
another way, with `^`, as in `2^3`. Here are two ideas about what `^` does
in Python. Both are reasonable, and they cannot both be true.

**Idea A.** `^` means a power, as it does on a calculator or in a
spreadsheet. `2 ^ 3` is another way to write `2 ** 3`.

**Idea B.** In Python, only `**` means a power. `^` does some other job.

## An experiment

Idea A says both lines print 8. Idea B says the second line prints
something else, or stops with an error.

```python exec
id: an-experiment-1
print(2 ** 3)
print(2 ^ 3)
```

```predict
type: choice

What will the second line print?

- 8
  - This is what idea A predicts.
- 1
- An error
```

Run it. The second line prints 1, so idea B matches what happens. `^` is
an operator too, and Python runs it without any complaint. It does a job
from logic, not arithmetic, so it gives a number that looks like nothing
to do with powers. That is the dangerous part. There is no error to warn
you.

Can you find two numbers where `^` and `**` give the same answer? Try a
few in the cell.

<details class="dl-answer"><summary>one pair that does it</summary>

It is hard to find one. `2 ^ 2` is 0 and `2 ** 2` is 4. `5 ^ 2` is 7 and
`5 ** 2` is 25. Even `0 ^ 1` gives 1 and `0 ** 1` gives 0. With whole
numbers from 0 to 20, only `1 ^ 0` and `1 ** 0` agree: both give 1. So a
test with ordinary numbers almost always shows the mistake, if somebody
checks the answer.

</details>

## Why idea A feels right

Idea A is not a strange idea. It is what many tools do. On a calculator,
the power key is often marked `^`. In a spreadsheet, `=2^3` gives 8. In an
email or a message, people type `x^2` when they cannot write a small raised
2. So `^` means "power" in many places a reader has been before Python.

Python took `^` from the language C, where it does this logic job. It took
`**` for powers from Fortran.

## Where else it happens

Here is a second surprise with powers. What is $-3$ squared?

```python exec
id: where-else-it-happens-1
print(-3 ** 2)
```

```predict
type: number

What will it print?
```

It prints -9. Python does powers before the minus sign, in the same order
as the calculation rules on the first page: powers come before
subtraction. So it squares 3 to get 9, and then makes it negative. Maths
writes $-3^2$ and means $-9$ too.

To square $-3$ itself, put it in brackets. Can you make the cell print 9?

<details class="dl-answer"><summary>one change that does it</summary>

`print((-3) ** 2)`. The brackets make $-3$ one number, and then it is
squared.

</details>

## Where to read more

Python's documentation lists every operator and the order it runs in:
[operator precedence](https://docs.python.org/3/reference/expressions.html#operator-precedence).
