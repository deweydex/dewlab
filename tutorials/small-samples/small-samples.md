---
title: "Chance: a closer look at small samples"
year: "2026-2027"
version: 2026.09.26.1
---

# Chance: a closer look at small samples

In [Probability: simple, compound and conditional](tutorial:what-are-the-chances#counting-the-cases),
6 of the 36 ways two dice can land make a total of 7. So a total of 7 happens one
time in six. Roll the two dice 54 times, and one sixth of 54 is 9. You
count the sevens, and there are 8. Here are two ideas about what that
means. Both are reasonable, and they cannot both be true.

**Idea A.** The chance says 9, and we got 8. Something is not quite fair:
the dice, or the way they were thrown.

**Idea B.** One sixth of 54 is the middle of what can happen, not what
will happen. With fair dice, 8 is an ordinary result, and so are 7 and 11.

## An experiment

We can find out what fair dice do. This cell rolls two fair dice 54 times,
counts the sevens, and does all of that 1,000 times. Then it counts how
many of the 1,000 batches gave exactly 9 sevens, and how many gave 8 or
fewer.

```python exec
id: an-experiment-1
import random

exactly_nine = 0
eight_or_fewer = 0
for batch in range(1000):
    sevens = 0
    for roll in range(54):
        if random.randint(1, 6) + random.randint(1, 6) == 7:
            sevens = sevens + 1
    if sevens == 9:
        exactly_nine = exactly_nine + 1
    if sevens <= 8:
        eight_or_fewer = eight_or_fewer + 1

print("exactly 9 sevens:", exactly_nine)
print("8 or fewer:", eight_or_fewer)
```

Idea A says fair dice should give 9 most of the time, so 8 or fewer should
be rare. Idea B says 9 is only the most common count, and many batches
miss it.

```predict
type: choice

Out of 1,000 batches of fair rolls, about how many give exactly 9 sevens?

- Most of them, 700 or more
  - This is close to what idea A predicts.
- About half, around 500
- About one in seven, around 150
  - 9 is the most likely count, but many counts are nearly as likely.
```

Run it, and run it again. About 140 to 150 batches give exactly 9 sevens,
and about 440 give 8 or fewer. The dice in the cell are as fair as a
computer can make them. So 8 sevens in 54 rolls happens almost half the
time with fair dice. It says nothing about the dice. Idea B matches what
happens.

How many rolls would make a small difference mean something? Can you
change 54 to 5,400, so that one sixth is 900, and count the batches that
land within 10 of 900? The test `if sevens >= 890 and sevens <= 910:`
finds them. With 5,400 rolls the cell takes longer, so try 100 batches.

<details class="dl-answer"><summary>what changes</summary>

With 5,400 rolls, only about 3 batches in 10 land within 10 of 900, and
about 7 in 10 land within 30. So 30 below 900 is still ordinary. But as
a share, 30 in 900 is only about 3%, where 1 in 9 was 11%. The more rolls, the closer the share of
sevens comes to one sixth, even though the count itself can be further
from 900.

</details>

## Why idea A feels right

A probability sounds like a promise. "One time in six" sounds like "every
sixth roll", and 54 rolls sounds like enough. In most of life, a number
someone calculates carefully is a number that comes true: a recipe, a bus
timetable, a bill.

The share of sevens comes close to one sixth only after many rolls. Over
a few dozen rolls it can be far from one sixth, further than most people
expect. That is why the
probability page rolled 10,000 times before it drew any conclusions.

## Where else it happens

Roll one fair die 12 times. Each face should appear about twice. How
often is at least one face missing altogether?

```python exec
id: where-else-it-happens-1
import random

a_face_missing = 0
for batch in range(1000):
    rolls = [random.randint(1, 6) for roll in range(12)]
    if len(set(rolls)) < 6:
        a_face_missing = a_face_missing + 1

print("at least one face missing:", a_face_missing, "out of 1,000")
```

```predict
type: choice

In about how many of 1,000 batches is a face missing?

- Hardly any
- About one in ten
- More than half
```

It is more than half, about 560 in 1,000. A fair die that never shows a
3 in 12 rolls is not a strange die.

## Where to read more

David Spiegelhalter's *The Art of Statistics* (Pelican, 2019) explains,
with real examples, how far chance can move a count.
