---
title: "How likely is it? Probability and simulation — Practice"
practice_for: how-likely-is-it
year: "2026-2027"
version: 2026.09.24.1
---

# How likely is it? Probability and simulation — Practice

Each problem says what kind it is. **Predict** means guess first, then
run. **Make** means write something new. **Fix** means find one mistake
in code that looks fine. **Explain** means answer in words. **Another
way** means reach the same place by a second route. The answers are
folded away until you open them.

Your toolkit is loaded on this page: `simulate` from the tutorial, and
`combinations`, `all_pairs`, `total` and the rest from earlier pages.
Simulations are left to chance, so your numbers will differ a little
from the ones in the answers. That is expected, and the tutorial's
section "Why the two answers differ" says why.

## Warm-up

Use this cell for any of the warm-up problems.

```python exec
id: likely-practice-warm-up
import random

print(13 / 52)
```

**1. Predict.** A deck of 52 cards has 13 hearts. You pick one card
without looking. What is the probability that it is a heart? Say it as
a fraction, a decimal and a percentage, then run the cell above.

<details class="dl-answer"><summary>answer</summary>

$\frac{13}{52} = \frac{1}{4}$, which is 0.25, or 25%. Every card is
equally likely, and 13 of the 52 outcomes are in the event "a heart".

</details>

**2. Make.** A bag of sweets has 3 red, 5 green and 2 blue sweets. You
take one without looking. Work out the probability that it is green, in
Python, using names for the three counts.

<details class="dl-answer"><summary>answer</summary>

```python
red = 3
green = 5
blue = 2
print(green / (red + green + blue))
```

This prints `0.5`. There are 10 sweets, each equally likely, and 5 of
them are green.

</details>

**3. Explain.** A weather app says there is a "120% chance of sunshine"
tomorrow. What is wrong with that, whatever the weather does?

<details class="dl-answer"><summary>answer</summary>

A probability is a number from 0 to 1, which is 0% to 100%. 120% is
1.2, which is more than certain. Nothing can be more likely than
certain, so the number cannot be a probability. The app probably meant
something else, such as "very sunny", and used a percentage as a way of
shouting.

</details>

**4. Predict.** Which of these can `random.randint(1, 6)` give: 0, 1,
6, 7? Run it in the cell above ten or twenty times if you are not sure.

<details class="dl-answer"><summary>answer</summary>

It can give 1 and 6, and never 0 or 7. `random.randint(1, 6)` includes
both of its ends, the way a die does. That is different from
`range(1, 6)`, which stops before 6. Two tools, two rules, so it is
worth checking which one you are using.

</details>

## Core

Run this cell first. It gives the core and stretch problems a coin to
toss, the same `heads` as the tutorial.

```python exec
id: likely-practice-tools
import random


def heads():
    """Toss a fair coin once. True for heads."""
    return random.choice(["heads", "tails"]) == "heads"


print(simulate(heads, 1000))
```

**5. Make.** In a board game, you need a 5 or a 6 on one die to escape
from jail. Write a trial, `escape`, and use `simulate` with 10,000 runs.
Then work out the exact probability by counting, and compare.

<details class="dl-answer"><summary>answer</summary>

```python
def escape():
    """Roll a fair die once. True for a 5 or a 6."""
    return random.randint(1, 6) >= 5

print(simulate(escape, 10000))
print(2 / 6)
```

The simulation gives something near 0.333, such as 0.3371. The exact
answer is $\frac{2}{6} = \frac{1}{3}$: two of the six equally likely
faces let you out.

</details>

**6. Fix.** A basketball player scores 70% of her free throws. A neat
way to act this out is `random.random() < 0.7`, which is True about 70%
of the time, because `random.random()` gives a decimal from 0 up to 1.
This cell should count her baskets in 1,000 throws. It gives an answer
near 0 instead. Run it, then find the mistake.

```python exec
id: likely-practice-fix-baskets
baskets = 0
for throw in range(1000):
    baskets = 0
    if random.random() < 0.7:
        baskets = baskets + 1
print(baskets / 1000)
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. What value can `baskets` have when the loop ends? Try printing it.
2. How many times does the line `baskets = 0` run?
3. Where did the running totals on
   [Doing it again](tutorial:doing-it-again#a-running-total) start?

**Think about:** which lines should happen once, and which lines should
happen every time round.

</details>

<details class="dl-answer"><summary>answer</summary>

`baskets = 0` is inside the loop, so the count goes back to 0 before
every throw. At the end, `baskets` is 1 or 0, depending only on the last
throw, and the cell prints 0.001 or 0.0. Move that line above the loop,
so it runs once:

```python
baskets = 0
for throw in range(1000):
    if random.random() < 0.7:
        baskets = baskets + 1
print(baskets / 1000)
```

Now it prints something near 0.7.

</details>

**7. Predict.** You roll a red die and a blue die. What is the
probability that the red one shows more than the blue one? Guess first.
Then count with `all_pairs`.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. How many outcomes are there in all?
2. How many of them are doubles, where neither die is bigger?
3. Of the rest, is "red bigger" more likely than "blue bigger", or
   the same?

**Think about:** why the answer is a little less than a half.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
faces = [1, 2, 3, 4, 5, 6]
outcomes = all_pairs(faces, faces)
red_bigger = 0
for red, blue in outcomes:
    if red > blue:
        red_bigger = red_bigger + 1
print(red_bigger, "of", len(outcomes), "=", red_bigger / len(outcomes))
```

This prints `15 of 36 = 0.4166666666666667`. Six of the 36 outcomes are
doubles. The other 30 split evenly: 15 with red bigger, and 15 with blue
bigger. So the answer is $\frac{15}{36}$, a little less than a half.

</details>

**8. Explain.** A friend runs `simulate(heads, 10)` and gets 0.8. "Your
`simulate` is broken," they say, "a coin is 0.5." What would you tell
them?

<details class="dl-answer"><summary>answer</summary>

Nothing is broken. Ten runs are very few, so the result wobbles a lot.
A fair coin gives 8 or more heads in 10 tosses about 5% of the time,
so 0.8 will turn up now and then. The law of large numbers promises that
the fraction gets closer to 0.5 as the runs grow. Try
`simulate(heads, 100000)`, and it will be very close to 0.5. It still
will not be exactly 0.5, and that is fine too.

</details>

**9. Another way.** In the tutorial, $P(\text{the dice add up to 7})$
was $\frac{6}{36}$, found by counting. Find it another way, with a trial
and `simulate`.

<details class="dl-answer"><summary>answer</summary>

```python
def sum_is_seven():
    """Roll two fair dice. True when they add up to 7."""
    return random.randint(1, 6) + random.randint(1, 6) == 7

print(simulate(sum_is_seven, 100000))
print(6 / 36)
```

The simulation gives something near 0.1667, such as 0.16561. The two
routes agree closely. Counting is exact and fast here, because there
are only 36 outcomes. Simulating is the route that still works when
there are far too many outcomes to count.

</details>

**10. Fix.** This trial should roll a fair die and give True for a 6.
The simulation says a 6 never comes up. Run it, then find the mistake.

```python exec
id: likely-practice-fix-die
def rolled_six():
    """Roll a fair die once. True for a 6."""
    return random.randint(1, 5) + 1 == 7

print(simulate(rolled_six, 10000))
```

<details class="dl-answer"><summary>answer</summary>

`random.randint(1, 5)` gives 1 to 5, so `+ 1` gives 2 to 6, which can
never be 7. Whoever wrote it was thinking of `range()`, which leaves
out its last number, and tried to make up for it. `randint` includes
both ends, so the plain version is right:

```python
def rolled_six():
    """Roll a fair die once. True for a 6."""
    return random.randint(1, 6) == 6

print(simulate(rolled_six, 10000))
```

Now it prints something near $\frac{1}{6} \approx 0.167$. A simulation
that gives exactly 0 for something that should happen is a good sign
of a mistake in the trial.

</details>

**11. Make.** The Irish Lotto draws 6 numbers from 47. What is the
probability that one ticket wins the jackpot? Use `combinations` from
your toolkit, and say the answer as "1 in …".

<details class="dl-answer"><summary>answer</summary>

```python
tickets = combinations(47, 6)
print(tickets)
print(1 / tickets)
```

There are 10,737,573 equally likely tickets, and one of them wins, so
the probability is $\frac{1}{10{,}737{,}573}$: 1 in about ten million.
Python writes it as `9.313091515186905e-08`, which is 0.000000093.
Simulating this would need hundreds of millions of runs to see even a
few wins. Here counting is the only practical way.

</details>

## Stretch

Use this cell for any of the stretch problems. It needs `heads` from the
core tools cell, so run that one first.

```python exec
id: likely-practice-stretch
import itertools

print(simulate(heads, 10))
```

**12. Make.** Your friend would also have called the coin unfair after
7 or more tails. So the real question is: how often does a fair coin
give a result at least as uneven as 7 to 3, either way? Answer it
exactly, with `combinations`, and then with a simulation.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. From the tutorial, 176 of the 1,024 rows have 7 or more heads.
2. How many rows have 7 or more tails? Can a row be in both groups?
3. For the simulation, count the heads in 10 tosses, and return True
   when there are 7 or more, or 3 or fewer.

**Think about:** why we can add the two groups here. (Page
[Chances that combine](tutorial:chances-that-combine) is about when
that works.)

</details>

<details class="dl-answer"><summary>answer</summary>

```python
seven_or_more = total([combinations(10, 7), combinations(10, 8),
                       combinations(10, 9), combinations(10, 10)])
print(2 * seven_or_more / 2 ** 10)

def uneven():
    """Toss a fair coin 10 times. True for 7 or more heads, or 7 or more tails."""
    heads_count = 0
    for toss in range(10):
        if heads():
            heads_count = heads_count + 1
    return heads_count >= 7 or heads_count <= 3

print(simulate(uneven, 10000))
```

Seven or more tails is the same as three or fewer heads, and there are
176 such rows too. No row has both, so there are 352 uneven rows, and
the probability is $\frac{352}{1024} = 0.34375$. The simulation gives
something near 0.344. A fair coin gives a result this uneven about one
time in three.

</details>

**13. Make.** Check the tutorial's 176 a third way, by listing all 1,024
rows of ten tosses. Use `itertools.product([False, True], repeat=10)`
from
[Untangling a condition](tutorial:untangling-a-condition), with True for
heads, and count the rows with 7 or more True values.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Loop over the rows that `itertools.product` makes.
2. For each row, `total(row)` counts its True values, because True
   counts as 1 and False as 0.
3. Keep a running count of the rows where that is 7 or more.

**Think about:** why we write `itertools.product` in full here, and not
`product` on its own.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
rows = 0
seven_or_more = 0
for row in itertools.product([False, True], repeat=10):
    rows = rows + 1
    if total(row) >= 7:
        seven_or_more = seven_or_more + 1
print(seven_or_more, "of", rows)
```

This prints `176 of 1024`, the same as the formula. `product` on its own
is your toolkit's `product` from
[Doing it again](tutorial:doing-it-again), which multiplies. The
`itertools.` in front says we mean the other one, which lists rows.

</details>

**14. Another way.** Someone says: "Two dice can add up to 11 different
totals, 2 to 12, so each total has probability $\frac{1}{11}$." For two
dice that is wrong. Describe a different experiment, a different space,
in which that answer would be right.

<details class="dl-answer"><summary>answer</summary>

A spinner with 11 equal sections, marked 2 to 12. There, each total is
one equally likely outcome, and $P(7) = \frac{1}{11}$ is right.

With two dice, the equally likely outcomes are the 36 pairs, not the 11
totals. A total of 7 has six pairs behind it, and 12 has only one. The
move "count the outcomes and divide" was fine. It needs a space where
the outcomes being counted really are equally likely.

</details>

**15. Predict.** You toss a fair coin 20 times. How likely is it that
somewhere in those tosses there are 4 heads in a row? Guess first: 5%,
20% or 50%? Then write a trial and simulate it.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Keep a `streak`: the number of heads in a row so far.
2. On heads, add 1 to it. On tails, set it back to 0.
3. As soon as the streak reaches 4, `return True`. If the loop ends
   without that, `return False`.

**Think about:** where `streak = 0` goes the first time, and why it
also appears inside the loop here, unlike in problem 6.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def four_in_a_row():
    """Toss a fair coin 20 times. True when 4 heads come in a row somewhere."""
    streak = 0
    for toss in range(20):
        if heads():
            streak = streak + 1
            if streak == 4:
                return True
        else:
            streak = 0
    return False

print(simulate(four_in_a_row, 10000))
```

It gives something near 0.48: almost half the time. The exact answer
is about 0.478. Most people guess much lower. Streaks in real chance
are longer and more common than they feel, which is one reason a
"hot streak" in sport or at a casino often means less than it seems.

</details>

**16. Explain.** A penalty taker scored 9 of her 10 penalties this
season. A commentator says her probability of scoring is 0.9. What is
0.9 here, in the words of this page, and how much should we trust it?

<details class="dl-answer"><summary>answer</summary>

0.9 is a relative frequency: how often she scored, divided by how many
times she tried. It is not a probability found by counting equally
likely outcomes, because a penalty has no such outcomes to count.

With only 10 tries, the relative frequency wobbles a lot, just as
`simulate(heads, 10)` does. A player whose real chance is 0.75 could
score 9 of 10 in a lucky season. After 100 or 200 penalties, the
relative frequency would be a much better guide to her real chance.

</details>

**17. Explain.** The tutorial page answered "is this coin unfair?"
without the words "hypothesis test" or "p-value", which a statistics book
would use. Would you have given the reader those names? If yes, where on
the page: before the question, or after the answer? If no, when would you
bring them in?

<details class="dl-answer"><summary>answer</summary>

There is no one right answer. A good answer weighs a few things.

- **Why give the names.** They are the words used in news reports, in
  research, and in later courses. A reader who has them can search for
  them and read more.
- **Before the question.** The reader gets a label before there is
  anything to put it on, and it can feel like something to memorise.
- **After the answer.** The name is a label for something the reader has
  already done. Many pages in this course name a thing after you have
  used it.
- **Not yet.** The idea is fresh and has room to settle. The cost: a
  reader may not recognise the same idea when they meet it under its
  name.

A strong answer might put the names after the answer, in one or two
sentences, so they label the idea without taking its place.

</details>
