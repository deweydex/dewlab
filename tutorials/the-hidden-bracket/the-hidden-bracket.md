---
title: "The fraction line: a closer look at v - u / a"
year: "2026-2027"
version: 2026.09.26.1
---

# The fraction line: a closer look at v - u / a

In [Rearranging formulae](tutorial:rearranging-formulae#the-same-formula-four-ways),
$t = \frac{v - u}{a}$ became the Python line `return (v - u) / a`. On paper
the formula has no brackets. In Python it has two. Here are two ideas about
whether they matter. Both are reasonable, and they cannot both be true.

**Idea A.** `v - u / a` is the same formula, written on one line. Python
reads it the way we read $\frac{v - u}{a}$.

**Idea B.** Python has no fraction line. It divides before it subtracts,
so `v - u / a` divides only `u`.

## An experiment

A car goes from 5 m/s to 13 m/s, and gains 2 m/s every second. How long does
it take? On paper, $\frac{13 - 5}{2} = 4$ seconds.

```python exec
id: an-experiment-1
v = 13     # final speed, m/s
u = 5      # starting speed, m/s
a = 2      # acceleration, m/s each second
print((v - u) / a)
print(v - u / a)
```

Idea A says both lines print 4. Idea B says the second line calculates
$u / a$ first, which is 2.5, and then takes it from 13.

```predict
type: number

What will the last line print?
```

Run it. The last line prints 10.5, as idea B predicts: $13 - 2.5$. Python
does division before subtraction, in the order from
[the first page](tutorial:first-steps#a-few-more-things-python-can-do). A
car cannot take 10.5 seconds to do something that takes 4, but Python
cannot know that. It gives no error.

Can you write $\frac{v + u}{2}$, the average of the two speeds, as a line
of Python?

<details class="dl-answer"><summary>one way to write it</summary>

`(v + u) / 2`, which is 9.0. Without the brackets, `v + u / 2` is
$13 + 2.5 = 15.5$.

</details>

## Why idea A feels right

On paper, the fraction line does two jobs. It says "divide", and it also
groups. Everything above the line is one number, and everything below it
is another. Nobody writes brackets round $v - u$, because the line already
holds it together. The fraction line is a bracket you cannot see.

When the formula is typed on one line, the grouping disappears, and only
"divide" is left. So the brackets that the fraction line hid have to be
written back in.

## Where else it happens

The same thing happens below the line. On paper, $\frac{6}{2 \times 3}$ is
1. What does Python say?

```python exec
id: where-else-it-happens-1
print(6 / 2 * 3)
print(6 / (2 * 3))
```

The first line prints 9.0. Python works from left to right: $6 / 2$ is 3,
and $3 \times 3$ is 9. To divide by the whole of $2 \times 3$, it needs its
brackets back. A calculator and a spreadsheet do the same: in a
spreadsheet, the formula `=(A1-B1)/C1` needs its brackets for the same
reason.

## Where to read more

Python's documentation lists the order it does its operators in:
[operator precedence](https://docs.python.org/3/reference/expressions.html#operator-precedence).
