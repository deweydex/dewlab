---
title: "Angles: a closer look at degrees and radians"
year: "2026-2027"
version: 2026.11.04.3
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
90 radians is about 14.3 turns. Subtracting 14 whole turns leaves the
same direction, and so the same sine. Idea A says there is nothing to
find there: the 0.894 means nothing, so the two numbers have no reason to
match.

```python exec
id: an-experiment-1
import math

print(round(math.sin(90), 10))
print(round(math.sin(90 - 14 * 2 * math.pi), 10))
```

```predict
type: choice

Will the two lines print the same number?

- No
  - This is what idea A predicts.
- Yes
  - This is what idea B predicts.
```

Run it. Both lines print 0.8939966636, to ten decimal places, as idea B
predicts. The 0.894 is the sine of a real angle: 90
radians, which points the same way as about 0.3 of a turn.

To ask for the sine of 90 degrees, change the degrees to radians first.
Can you make the cell print 1?

<details class="dl-answer"><summary>two ways that do it</summary>

`math.sin(math.radians(90))` changes 90 degrees to radians first.
`math.sin(math.pi / 2)` writes a quarter turn in radians directly. Both
print 1.0.

</details>

## What each idea reads the number as

`math.sin` takes one number and gives the sine of the direction that number
points to. The two ideas give the number a different unit.

Idea A reads 90 as degrees, where a full turn is 360. Then 90 is a quarter
turn, and its sine is 1. Idea B reads 90 as radians, where a full turn is
$2\pi$, about 6.28. Then 90 is about 14.3 turns. The 14 whole turns bring
us back to the start, and the 0.3 of a turn left over has a sine of 0.894.

Python and spreadsheets both take radians for their sine and cosine, so
`math.sin(90)` gives idea B's answer. A calculator shows its unit on the
screen, as DEG or RAD. Python has no screen to show it on, so its unit is
written in its documentation.

Let's watch the two readings. The slider sets the number. One arrow points
where the number goes when it is read as degrees. The other points where it
goes when it is read as radians.

```python exec
id: what-each-idea-reads-the-number-as-1
import matplotlib.pyplot as plt

number = slider("number", 0, 360, step=1, value=90, id="angle-number").value

ts = [step * 2 * math.pi / 100 for step in range(101)]
fig, ax = plt.subplots(figsize=(4, 4))
ax.plot([math.cos(t) for t in ts], [math.sin(t) for t in ts],
        color="grey", alpha=0.4)
readings = [("read as degrees", math.radians(number), "o"),
            ("read as radians", number, "s")]
for label, angle, marker in readings:
    ax.plot([0, math.cos(angle)], [0, math.sin(angle)], marker=marker,
            label=label)
ax.set_xlim(-1.2, 1.2)
ax.set_ylim(-1.2, 1.2)
ax.set_aspect("equal")
ax.grid(alpha=0.3)
ax.legend(loc="lower left")
print(f"{number} read as degrees: sine {math.sin(math.radians(number)):.3f}")
print(f"{number} read as radians: sine {math.sin(number):.3f}")
```

Move the slider to 360. Which way does each arrow point? Is there a number
above 0 where the two arrows point the same way?

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
