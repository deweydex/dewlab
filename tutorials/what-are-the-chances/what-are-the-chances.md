---
title: "Probability: simple, compound and conditional"
year: "2026-2027"
version: 2026.09.26.1
worlds:
  games-of-chance: Dice, cards and coins, and the games people play with them.
  dinosaurs: Dinosaurs and their fossils, what has been found, where, and how old it is.
  exoplanets: Planets around other stars, and the ways they were found.
datasets: [dinosaur-finds, exoplanets]
covers:
  rolling-ten-thousand-times:
    touches: [MIT-5.7]
  counting-the-cases:
    covers: [MIT-5.1, MIT-5.6, MIT-5.7]
  events-are-sets:
    covers: [MIT-5.8]
  a-test-for-a-rare-disease:
    covers: [MIT-5.8]
---

# Probability: simple, compound and conditional

Roll two dice, and add the two numbers. The total can be anything from 2
to 12. In a game, you choose one total, and win if you roll it. Which
total would you choose?

Here is one roll. Run it a few times.

```python exec
id: chances-roll-once
import random

first = random.randint(1, 6)
second = random.randint(1, 6)
print(first, "+", second, "=", first + second)
```

`random.randint(1, 6)` picks a whole number from 1 to 6, each as likely
as the others, like one fair die. A few rolls say very little about which
total is best. Ten thousand might say more.

## Rolling ten thousand times

This cell rolls two dice 10,000 times, counts how often each total
appears, and draws a bar for each total. It draws the bars with
matplotlib, a Python module for charts. The
[Statistics](tutorial:making-sense-of-data) page introduces it properly.

```python exec
id: chances-ten-thousand-rolls
import random
import matplotlib.pyplot as plt

counts = {}
for total in range(2, 13):
    counts[total] = 0
for roll in range(10000):
    total = random.randint(1, 6) + random.randint(1, 6)
    counts[total] = counts[total] + 1

plt.bar(list(counts.keys()), list(counts.values()))
plt.xlabel("total of two dice")
plt.ylabel("times in 10,000 rolls")

tallest = 2
for total in counts:
    if counts[total] > counts[tallest]:
        tallest = total
print("The tallest bar is", tallest)
```

```predict
type: number

Which total will have the tallest bar?
```

Run it again. The bars change a little every time, but the shape stays
the same. It is a triangle, highest at 7 and lowest at 2 and 12. Seven
appears about 1,670 times in 10,000, and 12 about 280 times. The dice
are fair, and yet the totals are not. The simulation shows the shape,
but not why it has that shape. Counting does.

To *simulate* a random event, we write code that makes it happen many
times, at random, and count the results. One run of the event, here
one roll of two dice, is a *trial*.

## Counting the cases

The first die can show 6 faces and the second 6, so there are
$6 \times 6 = 36$ ways the two can land. `itertools.product` from
[Counting](tutorial:counting-carefully) lists them. Each of the 36 is
equally likely, since each die is fair and neither affects the other.

```python exec
id: chances-count-the-cases
import itertools

outcomes = list(itertools.product(range(1, 7), repeat=2))
sevens = [roll for roll in outcomes if roll[0] + roll[1] == 7]
print(len(outcomes), "outcomes")
print(sevens)
```

Six of the 36 make 7: a 1 and a 6, a 2 and a 5, and so on. Only one
makes 12: two sixes. That explains the triangle.

An *outcome* is one possible result,
such as (3, 4). An event, as on the [Sets](tutorial:sets-as-sorted-lists)
page, is a set of outcomes we care about, such as "the total is 7". The
*probability* of an event is
a number from 0 to 1 that measures how likely it is: 0 is impossible and
1 is certain. When every outcome is equally likely, it is a count:

$$P(A) = \frac{\text{outcomes in } A}{\text{all outcomes}}
\qquad P(\text{total is } 7) = \frac{6}{36} = \frac{1}{6}$$

So in 10,000 rolls we expect about $10{,}000 \times \frac{1}{6}
\approx 1{,}667$ sevens, close to the height of the tallest bar. In fewer
rolls, the count can land much further from what we expect.
[Chance: a closer look at small samples](tutorial:small-samples) asks how
far.

Can you
write `chance(total)`, which counts the outcomes that add up to `total`
and returns its probability?

```python exec
id: chances-chance-of-a-total
import itertools

outcomes = list(itertools.product(range(1, 7), repeat=2))


def chance(total):
    """The probability that two dice add up to total, by counting outcomes."""
    # Your code here


print(chance(7))
print(chance(12))
```

```inputs
chance(7)
chance(12)
chance(2)
chance(13)
```

```hint
Start a count at 0. For each roll in `outcomes`, add 1 when its two
numbers add up to `total`. Then divide by how many outcomes there are.
```

```solution
import itertools

outcomes = list(itertools.product(range(1, 7), repeat=2))


def chance(total):
    """The probability that two dice add up to total, by counting outcomes."""
    favourable = 0
    for roll in outcomes:
        if roll[0] + roll[1] == total:
            favourable = favourable + 1
    return favourable / len(outcomes)


print(chance(7))
print(chance(12))
---
$\frac{6}{36} \approx 0.167$ and $\frac{1}{36} \approx 0.028$. A total
of 13 has no outcomes, so its probability is 0. An impossible event has
a probability too.
```

This cell sets the counts beside the simulation's bars, as shares of the
10,000 rolls. Run the simulation first if you have not.

```python exec
id: chances-count-beside-simulation
for total in range(2, 13):
    counted = len([roll for roll in outcomes if roll[0] + roll[1] == total]) / 36
    print(total, " counted", round(counted, 3), "  simulated", round(counts[total] / 10000, 3))
```

### How close is close?

The simulated shares are near the counted ones, and never exactly the
same. This cell rolls 10,000 times again, and after each roll calculates
the share of the rolls so far that were 7. The dashed line is
$\frac{1}{6}$.

```python exec
id: chances-running-share
import random
import matplotlib.pyplot as plt

seven_count = 0
running = []
for roll in range(1, 10001):
    if random.randint(1, 6) + random.randint(1, 6) == 7:
        seven_count = seven_count + 1
    running.append(seven_count / roll)

plt.plot(range(1, 10001), running)
plt.axhline(1 / 6, color="grey", linestyle="--")
plt.xscale("log")
plt.xlabel("rolls so far")
plt.ylabel("share of the rolls that were 7")
print("After 10,000 rolls:", round(running[-1], 4), "  1/6 is", round(1 / 6, 4))
```

The line swings wildly at first, and settles as the number of rolls
grows. The more trials we run, the closer the share usually comes to the
probability. This is the *law of large numbers*. It settles slowly,
though. To be ten times closer, we need about a hundred times as many
trials. So a simulation is good for checking a calculation, but it is a poor
replacement for one.

## Events are sets

Events are sets of outcomes, so the set operations from
[Venn diagrams](tutorial:venn-diagrams) make new events from old ones:
"A and B" is the intersection, "A or B" is the union, and "not A" is the
complement. An event made from others with "and", "or" and "not" is a
*compound event*. Take two events: rolling a double, and a high total, 10
or more.

`Fraction` keeps a probability as an exact fraction, so $\frac{1}{6}$
stays $\frac{1}{6}$ rather than 0.16666666666666666.

```python exec
id: chances-events-as-sets
import itertools
from fractions import Fraction

outcomes = set(itertools.product(range(1, 7), repeat=2))
double = {roll for roll in outcomes if roll[0] == roll[1]}
high = {roll for roll in outcomes if roll[0] + roll[1] >= 10}


def P(event):
    """The probability of an event: its share of all the outcomes."""
    return Fraction(len(event), len(outcomes))


print("P(double) =", P(double))
print("P(high) =", P(high))
print("P(double and high) =", P(double & high))
print("P(double or high) =", P(double | high))
```

```predict
Each event has a probability of 1/6. What will the last line say?

- P(double or high) = 1/3
  - Two events, each 1/6: add them.
- P(double or high) = 5/18
  - Some rolls are in both events.
- P(double or high) = 1/36
  - "Or" makes it harder, like "and".
```

(5, 5) and (6, 6) are both doubles and high. Adding $\frac{6}{36} +
\frac{6}{36}$ counts them twice, so we subtract them once:
$\frac{12}{36} - \frac{2}{36} = \frac{10}{36} = \frac{5}{18}$. That is
inclusion-exclusion from the Venn diagrams page, with probabilities in
place of counts. Each rule for combining events is a set operation:

| The event | The set | Its probability |
|---|---|---|
| not A | the complement | $1 - P(A)$ |
| A or B | the union | $P(A) + P(B) - P(A \text{ and } B)$ |
| A and B, if A and B are independent | the intersection | $P(A) \times P(B)$ |

Events are *mutually exclusive* when they cannot both happen, such as a
total of 2 and a total of 12. Their intersection is empty, so for them
"or" is plain adding.

The complement rule is the most useful of the three. "At least one six in
two rolls" has 11 outcomes to count. "No six" is $\frac{5}{6} \times
\frac{5}{6} = \frac{25}{36}$ in one step, so at least one six is
$1 - \frac{25}{36} = \frac{11}{36}$.

### Independent events

Two events are *independent* when knowing one happened does not change
the chance of the other. For those, and only those, the chance of both
is the two chances multiplied. Is "the first die is a 6" independent of
"the total is 7"? And of "the total is 8"?

```python exec
id: chances-independent
first_six = {roll for roll in outcomes if roll[0] == 6}
seven = {roll for roll in outcomes if roll[0] + roll[1] == 7}
eight = {roll for roll in outcomes if roll[0] + roll[1] == 8}

print(P(first_six & seven) == P(first_six) * P(seven),
      P(first_six & eight) == P(first_six) * P(eight))
```

```predict
Does multiplying give the right answer for each pair?

- True True
  - The two dice do not affect each other, so nothing about one tells us anything.
- True False
  - Seven is special somehow.
- False False
  - The total depends on the first die, so neither pair can be independent.
```

Seven is special. Whatever the first die shows, exactly one face of the
second makes 7, so knowing the first die changes nothing. The chance is
still 1 in 6. Eight is different. A 1 on the first die makes 8
impossible, and a 6 makes it 1 in 6, up from $\frac{5}{36}$. We can
check independence by counting. It does not depend on whether two things
seem connected.

### One draw changes the next

Draw two cards from a deck of 52 without returning the first. How
often are both aces? *Without replacement* means the first card stays
out, so it changes what the second draw can be. `random.sample(deck, 2)`
draws two different cards, the way a hand does.

```python exec
id: chances-two-aces
import random

deck = []
for suit in ["hearts", "diamonds", "clubs", "spades"]:
    for rank in range(1, 14):
        deck.append((rank, suit))

both_aces = 0
for trial in range(100000):
    first, second = random.sample(deck, 2)
    if first[0] == 1 and second[0] == 1:
        both_aces = both_aces + 1
print(both_aces, "times in 100,000")
```

It happens about 450 times in 100,000. Now we count. The first card is
an ace 4 times in 52. If it was, 3 aces are left among 51 cards:

$$P(\text{two aces}) = \frac{4}{52} \times \frac{3}{51} = \frac{1}{221}
\approx 0.0045$$

and $100{,}000 \div 221 \approx 452$.

![A tree from 52 cards. The first draw branches into ace, 4 over 52, and
other, 48 over 52. Under ace the next draw is 3 over 51; under other it is
4 over 51. The ace then ace path is marked.](two-aces-tree.svg)

Both branches of the second draw have 51 on the bottom, since one card
has gone, whichever it was. The top number is different. 3 aces are left
if the first card was an ace, and 4 if it was not. So the two draws are
not independent. We still multiply, but the second number has to depend
on the first draw.

## A test for a rare disease

A disease affects 1 person in 10,000. A test for it is right 99% of the
time. It says "positive" for 99% of people who have the disease, and
"negative" for 99% of people who do not. You take the test, and it says
positive. How likely is it that you have the disease?

Before anything else, make a guess. Then this cell tests a town of a
million people. `random.random()` gives a number from 0 up to 1, so it
is below 0.99 on 99% of calls. Python lets us write `1_000_000` for
`1000000`. The underscores are only there to help us read it. It takes a
few seconds to run.

```python exec
id: chances-disease-simulated
import random

sick_and_positive = 0
well_and_positive = 0
for person in range(1_000_000):
    sick = random.random() < 1 / 10_000
    test_is_right = random.random() < 0.99
    if sick and test_is_right:
        sick_and_positive = sick_and_positive + 1
    if not sick and not test_is_right:
        well_and_positive = well_and_positive + 1

positives = sick_and_positive + well_and_positive
print("Positive tests:", positives)
print("Of those, sick:", sick_and_positive)
print("Sick, out of every 100 positive tests:", round(100 * sick_and_positive / positives))
```

```predict
type: number

Out of every 100 people who test positive, how many have the disease?
```

It is about 1 in 100. Nearly everyone guesses much higher, and studies
have found that many doctors do too. The first line of the loop makes
the difference. `sick` is `True` for only 1 person in 10,000. The test
is wrong for 1% of the well people, and there are so many well people
that their 1% outnumbers the sick people's 99%.

### Counting a million people

The same argument works with no simulation at all. Picture a million
people, and follow them:

| | Test positive | Test negative | Everyone |
|---|---|---|---|
| Have the disease | 99 | 1 | 100 |
| Do not | 9,999 | 989,901 | 999,900 |
| Everyone | 10,098 | 989,902 | 1,000,000 |

100 people have the disease, and the test finds 99 of them. 999,900 do
not, and the test wrongly says positive for 1% of them, which is 9,999
people. So 10,098 people test positive, and 99 of them are sick:
$\frac{99}{10{,}098} \approx 0.0098$, just under 1%.

When we count people, rather than multiply percentages, we are using
*natural frequencies*. It asks a question most of us can answer: out of
these people, how many?

### Given that

A *conditional probability* is the chance of one event when we know
another has happened. We write $P(B \mid A)$, and say "the probability of
B given A". It counts inside a smaller group. Among
the outcomes where A happened, it is the share where B happened too.

$$P(B \mid A) = \frac{P(A \text{ and } B)}{P(A)}$$

The table has two of them, and they are very different:

- $P(\text{positive} \mid \text{sick}) = \frac{99}{100} = 0.99$: among
  the sick, the share who test positive.
- $P(\text{sick} \mid \text{positive}) = \frac{99}{10{,}098} \approx
  0.0098$: among the positives, the share who are sick.

The test's makers can promise the first. A patient wants to know the
second. The guess of 99% is the first. The question asked for
the second. *Bayes' theorem* is the rule that turns one into the other.
The table above is that rule, written as a count.

Can you write `share_sick(rate, accuracy)`, which follows a million
people as the table does, and returns the share of the positives who are
sick? Then try a disease that affects 1 person in 100.

```python exec
id: chances-share-sick
def share_sick(rate, accuracy):
    """Among a million people, the share of positive tests that are right.

    rate is the share of people with the disease; accuracy is the share
    of people, sick or well, for whom the test is right.
    """
    people = 1_000_000
    # Your code here


print(round(share_sick(1 / 10_000, 0.99), 4))
print(round(share_sick(1 / 100, 0.99), 4))
```

```inputs
round(share_sick(1 / 10_000, 0.99), 4)
round(share_sick(1 / 100, 0.99), 4)
round(share_sick(1 / 10_000, 0.999), 4)
```

```hint
Follow the table's rows. How many people are sick? How many of them test
positive? How many are well, and how many of those test positive anyway?
```

```solution
def share_sick(rate, accuracy):
    """Among a million people, the share of positive tests that are right.

    rate is the share of people with the disease; accuracy is the share
    of people, sick or well, for whom the test is right.
    """
    people = 1_000_000
    sick = people * rate
    well = people - sick
    sick_and_positive = sick * accuracy
    well_and_positive = well * (1 - accuracy)
    return sick_and_positive / (sick_and_positive + well_and_positive)


print(round(share_sick(1 / 10_000, 0.99), 4))
print(round(share_sick(1 / 100, 0.99), 4))
---
It prints 0.0098, and then 0.5. With 1 person in 100 sick, 9,900 sick
people and 9,900 well people test positive, so a positive is right half
the time. The same test is worth a great deal more when the disease is
common. A better test helps too. At 99.9% right, the share is 0.0908,
still under one in ten. How common the disease is, the *base rate*,
matters as much as how good the test is.
```

## Given which?

The order of a "given" matters, and it is easy to swap without noticing.
Choose a world at the top of the page. Each asks one conditional
probability in both directions.

<div class="dl-world" data-world="games-of-chance">

Two dice are rolled out of sight. Someone tells you that at least one of
them is a six. What is the chance that both are? And if you are told
that both are sixes, what is the chance that at least one is?

```python exec
id: chances-given-which--games-of-chance
import itertools
from fractions import Fraction

outcomes = set(itertools.product(range(1, 7), repeat=2))
at_least_one_six = {roll for roll in outcomes if 6 in roll}
both_sixes = {roll for roll in outcomes if roll == (6, 6)}
print(len(at_least_one_six), "outcomes have at least one six")
```

```hint
Given at least one six, count inside `at_least_one_six`. What share of it
is also in `both_sixes`? `Fraction(top, bottom)` keeps the answer exact.
```

```solution
import itertools
from fractions import Fraction

outcomes = set(itertools.product(range(1, 7), repeat=2))
at_least_one_six = {roll for roll in outcomes if 6 in roll}
both_sixes = {roll for roll in outcomes if roll == (6, 6)}
print(len(at_least_one_six), "outcomes have at least one six")

print(Fraction(len(both_sixes & at_least_one_six), len(at_least_one_six)))
print(Fraction(len(at_least_one_six & both_sixes), len(both_sixes)))
---
The answers are $\frac{1}{11}$, and 1. Eleven outcomes have at least
one six, and one of them is the double. The other direction is certain,
because two sixes always include a six. There is a third question. If you
are told that the *first* die is a six, the chance of both is
$\frac{1}{6}$, not $\frac{1}{11}$. Three questions sound alike, and have
three different answers.
```

</div>

<div class="dl-world" data-world="dinosaurs">

Choose a dinosaur find at random. What is the chance it is Jurassic, if
it was found in Portugal? And the chance it was found in Portugal, if it
is Jurassic? Portugal's code is PT.

```python exec
id: chances-given-which--dinosaurs
finds = await load_csv("dinosaur-finds.csv", keep_default_na=False)

jurassic = (finds.oldest_mya <= 201.4) & (finds.youngest_mya >= 145)
portugal = finds.country_code == "PT"
print(len(finds), "finds;", jurassic.sum(), "Jurassic;", portugal.sum(), "in Portugal")
```

```hint
`(jurassic & portugal).sum()` counts the finds that are both. Divide it by
the size of the group you are given.
```

```solution
finds = await load_csv("dinosaur-finds.csv", keep_default_na=False)

jurassic = (finds.oldest_mya <= 201.4) & (finds.youngest_mya >= 145)
portugal = finds.country_code == "PT"
print(len(finds), "finds;", jurassic.sum(), "Jurassic;", portugal.sum(), "in Portugal")

both = (jurassic & portugal).sum()
print("P(Jurassic | Portugal) =", round(both / portugal.sum(), 3))
print("P(Portugal | Jurassic) =", round(both / jurassic.sum(), 3))
---
With the copy saved on {{snapshot: dinosaur-finds}}, 59 of Portugal's 75
finds are Jurassic, about 0.79, but they are only 59 of the 891 Jurassic
finds, about 0.07. The first says Portugal's dinosaur rock is mostly
Jurassic, and a find there is very likely from that period. The second
says that most Jurassic finds come from elsewhere, because Portugal is one
small country among many. Both are true, of the same 59 finds.
```

</div>

<div class="dl-world" data-world="exoplanets">

Choose a known planet at random. What is the chance it was found by
radial velocity, the wobble of its star, if it is within 100 light years
of us? And the chance it is within 100 light years, if it was found by
radial velocity?

```python exec
id: chances-given-which--exoplanets
planets = await load_csv("exoplanets.csv")

wobble = planets.method == "Radial Velocity"
near = planets.distance_ly < 100
print(len(planets), "planets;", wobble.sum(), "found by wobble;", near.sum(), "near")
```

```hint
`(wobble & near).sum()` counts the planets that are both. Divide it by
the size of the group you are given.
```

```solution
planets = await load_csv("exoplanets.csv")

wobble = planets.method == "Radial Velocity"
near = planets.distance_ly < 100
print(len(planets), "planets;", wobble.sum(), "found by wobble;", near.sum(), "near")

both = (wobble & near).sum()
print("P(wobble | near) =", round(both / near.sum(), 3))
print("P(near | wobble) =", round(both / wobble.sum(), 3))
---
With the copy saved on {{snapshot: exoplanets}}, about 0.77 of the near
planets were found by the wobble, but only about 0.34 of the wobble
planets are near. A star's wobble is easiest to measure when the star is
bright, and near stars look bright, so the wobble finds most of the near
planets. Most wobble planets are still further away, because there are
far more stars further away.
```

</div>

## Looking back

This page found every probability twice: once by playing the game many
times, and once by counting. In the medical test, and in the "given
which" question, a conditional probability had two directions. Can you
say, in a sentence of your own, why $P(\text{sick} \mid \text{positive})$
and $P(\text{positive} \mid \text{sick})$ are so far apart?

A challenge. The Chevalier de Méré's first bet, a six in four rolls of
one die, won slightly more often than it lost. His second bet was a
double six in 24 rolls of two dice. Four rolls for a 1-in-6 chance, so
24 rolls for a 1-in-36 chance, seems the same bet. Is it? Play it many
times, then count it with the complement rule.

```python challenge
import random

# One bet: roll two dice 24 times. It wins if a double six comes up at
# least once. Play many bets, and find the share that win.
# Then count: the chance of no double six in one roll is 35/36.
```

The next page is a game show with [three doors](tutorial:three-doors),
where the answer surprises nearly everyone, and a simulation settles
it before the counting explains it.

## Where to read more

3Blue1Brown (2020). *Bayes theorem, the geometry of changing beliefs.*
<https://www.youtube.com/watch?v=HZGCoVF3YvM>. Conditional probability
drawn as areas: the medical test as a picture.

Gigerenzer, G. (2002). *Reckoning with Risk: Learning to Live with
Uncertainty.* Penguin. The case for natural frequencies, made by the
psychologist who studied how doctors and patients read test results.

StatQuest with Josh Starmer (2017). *Probability is not Likelihood.*
<https://www.youtube.com/watch?v=pYxNSUDSFH4>. A distinction this page
does not make, and which matters the moment you meet statistics
properly.

Mlodinow, L. (2008). *The Drunkard's Walk: How Randomness Rules Our
Lives.* Pantheon. Readable, and good on why our sense of chance is so
unreliable.

Python Software Foundation. *`random` — Generate pseudo-random numbers.*
<https://docs.python.org/3/library/random.html>. In particular the
difference between `random.choice` and `random.sample`, which is the
difference between drawing with and without replacement.
