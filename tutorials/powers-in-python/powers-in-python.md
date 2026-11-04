---
title: "Powers: a closer look at ** and ^"
year: "2026-2027"
version: 2026.11.04.3
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
few in the *cell*{.term}.

<details class="dl-answer"><summary>one pair that does it</summary>

There is almost none. `2 ^ 2` is 0 and `2 ** 2` is 4. `5 ^ 2` is 7 and
`5 ** 2` is 25. Even `0 ^ 1` gives 1 and `0 ** 1` gives 0. With whole
numbers from 0 to 20, only `1 ^ 0` and `1 ** 0` agree: both give 1. So a
test with ordinary numbers almost always shows the mistake, if somebody
checks the answer.

</details>

## What each idea counts

Idea A counts a power. `2 ^ 3` multiplies 2 by itself 3 times, so it gives
$2 \times 2 \times 2 = 8$. A calculator key marked `^` and the spreadsheet
formula `=2^3` do this.

Idea B counts digits. Python writes both whole numbers in binary, which
uses only the digits 0 and 1. Then it compares them one place at a time.
It writes 1 where the two digits differ, and 0 where they are the same.
This job is called *exclusive or*{.term}. For `2 ^ 3`:

| | left place | right place |
|---|---|---|
| 2 in binary | 1 | 0 |
| 3 in binary | 1 | 1 |
| result | 0 (same) | 1 (differ) |

The result is `01` in binary, which is 1. That is what the experiment
printed.

Python took `^` from the language C, where it does this job. It took `**`
for powers from Fortran.

Let's watch the two jobs side by side. The slider sets the left number.
The right number is 3. The cell prints each number in binary, with five
places.

```python exec
id: what-each-idea-counts-1
left = slider("left", 0, 20, step=1, value=2, id="left").value
right = 3

print(f"{left} in binary:  {left:05b}")
print(f"{right} in binary:  {right:05b}")
print(f"{left} ^ {right} = {left ^ right}   in binary: {left ^ right:05b}")
print(f"{left} ** {right} = {left ** right}")
```

Move the slider from 0 to 20. How does the `**` line grow, and how does
the `^` line grow? Can you see in the binary rows which places the `^`
result changes?

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
