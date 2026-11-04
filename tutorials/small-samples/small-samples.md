---
title: "Chance: a closer look at small samples"
year: "2026-2027"
version: 2026.11.04.3
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

## What each idea counts

Idea A compares the result with one number, 9, and counts the gap: 8 is 1
away. It treats one sixth of 54 as the count the dice should give. Idea B
compares the result with every count the dice can give. It asks how often
fair dice give 8 or fewer, and the experiment found about 440 batches in
1,000.

The two ideas also look at different things as the number of rolls grows.
The count of sevens can move further from one sixth of the rolls, and the
share of sevens still comes closer to one sixth. That is why the
probability page rolled 10,000 times before it drew any conclusions.

The slider below sets the number of rolls in a batch. The cell does not
simulate. It calculates how likely each count of sevens is, for fair dice.
It shows the chance of exactly one sixth of the rolls, and the chance of
landing within 20% of that count.

```python exec
id: what-each-idea-counts-1
from math import lgamma, log, exp

rolls = slider("rolls", 6, 5400, step=6, value=54, id="rolls").value
expected = rolls // 6

def chance_of(count):
    ways = lgamma(rolls + 1) - lgamma(count + 1) - lgamma(rolls - count + 1)
    return exp(ways + count * log(1 / 6) + (rolls - count) * log(5 / 6))

near = sum(chance_of(count) for count in range(rolls + 1)
           if 0.8 * expected <= count <= 1.2 * expected)

print("expected sevens:", expected)
print("chance of exactly", expected, "sevens:", round(100 * chance_of(expected), 1), "%")
print("chance within 20% of", expected, ":", round(100 * near, 1), "%")
```

Move the slider from 6 up to 5,400. What happens to the chance of exactly
one sixth? What happens to the chance of landing within 20% of it?

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
