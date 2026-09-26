---
title: "Angles: a closer look at degrees and radians"
year: "2026-2027"
version: 2026.09.26.1
---

# Angles: a closer look at degrees and radians

In [The unit circle](tutorial:the-unit-circle#measuring-the-walk),
`math.sin(90)` gave about 0.894, not 1. The page said that `math.sin`
takes radians. Here are two ideas about that 0.894. Both are reasonable,
and they cannot both be true.

**Idea A.** 0.894 is a mistake, or a number with no meaning. The sine of
90 is 1, and Python got it wrong.

**Idea B.** 0.894 is the right answer to a different question. Python
read 90 as 90 radians, and gave the sine of that angle.

## An experiment

The two ideas predict different things. If idea B is right, 90 radians is
an angle like any other. One full turn is $2\pi$ radians, about 6.28, so
90 radians is about 14.3 turns. Taking away 14 whole turns leaves the
same direction, and so the same sine. Idea A says there is nothing to
find there: the 0.894 means nothing, so the two numbers have no reason to
match.

```python exec
id: an-experiment-1
import math

print(math.sin(90))
print(math.sin(90 - 14 * 2 * math.pi))
```

```predict
type: choice

Will the two lines print the same number?

- No
  - This is what idea A predicts.
- Yes
  - This is what idea B predicts.
```

Run it. Both lines print 0.89399666360055, apart from the last digit or
two, as idea B predicts. The 0.894 is the sine of a real angle: 90
radians, which points the same way as about 0.3 of a turn.

To ask for the sine of 90 degrees, turn the degrees into radians first.
Can you make the cell print 1?

<details class="dl-answer"><summary>two ways that do it</summary>

`math.sin(math.radians(90))` turns 90 degrees into radians first.
`math.sin(math.pi / 2)` writes a quarter turn in radians directly. Both
print 1.0.

</details>

## Why idea A feels right

Degrees are the angles most of us learned first. A right angle is 90, a
full turn is 360, and a calculator in school was usually set to degrees.
So 90 looks like an angle in degrees, and "the sine of 90 is 1" feels like
a fact about the number 90.

But 90 is only a number. It needs a unit, like 90 metres or 90 minutes.
Python, NumPy, spreadsheets and JavaScript all take radians for their
sine and cosine. A calculator shows its unit on the screen, as DEG or
RAD. Python has no screen to show it on, so its unit is written in its
documentation.

## Where else it happens

What will this print: the cosine of a full turn, 360 degrees?

```python exec
id: where-else-it-happens-1
import math

print(math.cos(math.radians(360)))
print(math.cos(360))
```

```predict
type: number
tolerance: 0.01

What will the last line print?
```

The first line prints 1.0. The last prints about -0.284, because 360
radians is not a full turn. A mix of units gives no error, only a wrong
answer, so it is worth checking an angle you already know the answer for.

## Where to read more

Python's documentation for the
[`math` module](https://docs.python.org/3/library/math.html#angular-conversion)
has `math.radians` and `math.degrees` side by side.
