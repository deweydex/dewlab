---
title: "Probability: simple, compound and conditional — Practice"
practice_for: what-are-the-chances
year: "2026-2027"
version: 2026.09.26.1
worlds:
  games-of-chance: Dice, cards and coins, and the games people play with them.
  dinosaurs: Dinosaurs and their fossils, what has been found, where, and how old it is.
  exoplanets: Planets around other stars, and the ways they were found.
datasets: [dinosaur-finds, exoplanets]
---

# Probability: simple, compound and conditional — Practice

Here are problems on chance, and three from earlier pages. Where a
problem can be both played and counted, do both, in whichever order you
like. When the two answers disagree, one of them has a mistake. Finding
it is the most useful part of the problem.

## Tools

Run this cell once before you start. `simulate(trial)` runs a trial many
times, 100,000 unless you say otherwise, and returns the share of runs
that returned `True`. You give it a function of your own that plays one
trial and returns `True` or `False`, such as `six` below.

```python exec
id: tools-1
import itertools
import random
from fractions import Fraction


def simulate(trial, n=100_000):
    """Run trial() n times, and give the share of the runs that returned True."""
    wins = 0
    for run in range(n):
        if trial():
            wins = wins + 1
    return wins / n


def six():
    """One trial: roll a die, and say whether it came up 6."""
    return random.randint(1, 6) == 6


print(simulate(six), "is close to", round(1 / 6, 4))
```

## Simple chances

**1.** A fair die is rolled. What is the probability of each of these?

- (a) a 4
- (b) an even number
- (c) a number above 4
- (d) a 7

<details class="dl-answer"><summary>answer</summary>

(a) $\frac{1}{6}$. (b) $\frac{1}{2}$. (c) $\frac{1}{3}$. (d) 0.

An impossible event has a probability of exactly 0, not a very small
number.

</details>

**2.** A bag holds 5 red, 3 blue and 2 green counters. What is the
probability of drawing each colour? Do the three add up to 1?

<details class="dl-answer"><summary>answer</summary>

0.5, 0.3 and 0.2, which add up to 1. They must, because every counter is one
of the three colours, and none is two. If a list like this does not add up
to 1, a case is missing or a case is counted twice.

</details>

**3.** A coin is flipped four times. What is the chance of exactly two
heads? Can you count it by listing the 16 ways four flips can land, then
check it with `simulate`?

```python exec
id: chances-two-heads
import itertools

flips = list(itertools.product("HT", repeat=4))
print(len(flips), "ways")

exactly_two = 0
```

```inputs
exactly_two
```

```hint
`flip.count("H")` counts the heads in one way of landing. For the
simulation, write a function that flips four coins with
`random.choice("HT")` and says whether exactly two were heads.
```

```solution
import itertools
import random

flips = list(itertools.product("HT", repeat=4))
print(len(flips), "ways")

exactly_two = 0
for flip in flips:
    if flip.count("H") == 2:
        exactly_two = exactly_two + 1
print(exactly_two, "of", len(flips), "=", exactly_two / len(flips))


def two_heads():
    """One trial: flip four coins, and say whether exactly two were heads."""
    heads = 0
    for i in range(4):
        if random.choice("HT") == "H":
            heads = heads + 1
    return heads == 2


print(simulate(two_heads))
---
It is 6 of 16, which is 0.375. The 6 is $C(4, 2)$ from
[Counting](tutorial:counting-carefully), choosing which 2 of the 4 flips
are heads. Many people guess a half, since two heads is the middle
result, but most ways of landing are not the middle one.
```

## Combining events

**4.** Two dice are rolled. What is the chance of each of these?

- (a) both sixes
- (b) a total of 7
- (c) at least one six

<details class="dl-answer"><summary>answer</summary>

(a) $\frac{1}{36}$. (b) $\frac{6}{36} = \frac{1}{6}$. (c)
$\frac{11}{36}$.

(c) is quickest with the complement. No six is $\frac{5}{6} \times
\frac{5}{6} = \frac{25}{36}$, so at least one is $1 - \frac{25}{36} =
\frac{11}{36}$. Adding $\frac{1}{6} + \frac{1}{6}$ gives
$\frac{12}{36}$, which counts the double six twice.

</details>

```question
id: chances-which-are-independent
type: fill-in-the-blank

- Two rolls of a die are {independent|not independent}.
- Two cards drawn without returning the first are {not independent|independent}.
- Rain today and rain tomorrow are {not independent|independent}.
- A card being red and a card being a face card (a jack, queen or king) are {independent|not independent}.
```

**5.** The last one surprises people. Can you show it with numbers?

<details class="dl-answer"><summary>answer</summary>

$P(\text{red}) = \frac{1}{2}$ and $P(\text{face}) = \frac{12}{52}$. Six
cards are both, so $P(\text{both}) = \frac{6}{52}$, which is exactly
$\frac{1}{2} \times \frac{12}{52}$. Half the face cards are red, just as
half of all cards are, so knowing the colour tells you nothing about
whether it is a face card.

</details>

**6.** A coin has landed heads five times in a row. What is the chance
of heads next? This cell flips six coins, 100,000 times, keeps the runs
that start with five heads, and looks at the sixth flip.

```python exec
id: chances-after-five-heads
import random

five_heads = 0
heads_next = 0
for run in range(100_000):
    flips = []
    for i in range(6):
        flips.append(random.choice("HT"))
    if flips[:5] == ["H", "H", "H", "H", "H"]:
        five_heads = five_heads + 1
        if flips[5] == "H":
            heads_next = heads_next + 1

print(five_heads, "runs began with five heads")
print("The share of them with heads next:", round(heads_next / five_heads, 2))
```

```predict
type: number
tolerance: 0.05

What share of the runs with five heads will have heads next?
```

<details class="dl-answer"><summary>why</summary>

About 0.5. The coin has no memory. The feeling that tails is now "due"
is called the *gambler's fallacy*, and nearly everybody has it. Five
heads in a row is unlikely before the first flip: about $\frac{1}{32}$.
That is why only about 3,000 of the 100,000 runs were kept. Once they
have happened, they change nothing about the sixth.

</details>

## The birthday problem

**7.** A room holds 23 people. What is the chance that two of them share
a birthday? Make a guess, then run the cell, which fills the room 10,000
times. It ignores 29 February, and treats every birthday as equally
likely.

```python exec
id: chances-birthday-simulated
import random

rooms = 10_000
shared = 0
for room in range(rooms):
    birthdays = []
    for person in range(23):
        birthdays.append(random.randint(1, 365))
    if len(set(birthdays)) < 23:
        shared = shared + 1
print("Rooms with a shared birthday:", round(shared / rooms, 3))
```

Now count it. The chance that everyone's birthday is different is
$\frac{365}{365} \times \frac{364}{365} \times \frac{363}{365} \times
\cdots$, one fraction for each person, because each new person must miss
every birthday so far. Can you write `chance_all_different(people)`?

```python exec
id: chances-birthday-counted
def chance_all_different(people):
    """The chance that people birthdays, from 365 days, are all different."""
    # Your code here


print(round(1 - chance_all_different(23), 4))
```

```inputs
round(chance_all_different(23), 4)
round(chance_all_different(1), 4)
round(chance_all_different(50), 4)
```

```hint
Start a product at 1. The first person can have any of 365 days, the
second any of the 364 left, and so on. Multiply by `(365 - i) / 365` for
each person `i`, counting from 0.
```

```solution
def chance_all_different(people):
    """The chance that people birthdays, from 365 days, are all different."""
    chance = 1
    for i in range(people):
        chance = chance * (365 - i) / 365
    return chance


print(round(1 - chance_all_different(23), 4))
---
It is 0.5073, slightly better than even. Most people guess much lower,
because the question sounds like "does someone share *my* birthday?",
which for 23 people is only about 6%. But any two people can share, and
23 people make $C(23, 2) = 253$ pairs. With 50 people, a shared birthday
is 97% likely.
```

## Given that

**8.** You draw a card and see that it is red. What is the chance it is
a heart?

<details class="dl-answer"><summary>answer</summary>

$\frac{1}{2}$. When you know it is red, the group we count in shrinks to
the 26 red cards, and 13 of them are hearts: $\frac{13}{26}$.

</details>

**9.** A family has two children, and at least one is a girl. What is
the chance both are?

<details class="dl-answer"><summary>answer</summary>

$\frac{1}{3}$. Write the older child first: GG, GB, BG and BB are
equally likely. BB is not possible, which leaves three, and one of them
is GG. If you are told instead that *the older child* is a girl, the
answer is $\frac{1}{2}$. It is the same trap as the dice on the tutorial
page. The answer depends on exactly what you were told.

</details>

**10.** In the tutorial's test for a rare disease, a positive test
meant about a 1% chance of having it. A doctor sends you for a second,
separate test, just as good, and it is positive too. What is the chance
now? Can you calculate it by following the people who tested positive
once?

```python exec
id: chances-second-test
def share_sick(rate, accuracy):
    """Among a million people, the share of positive tests that are right."""
    people = 1_000_000
    sick = people * rate
    well = people - sick
    sick_and_positive = sick * accuracy
    well_and_positive = well * (1 - accuracy)
    return sick_and_positive / (sick_and_positive + well_and_positive)


after_one = share_sick(1 / 10_000, 0.99)
print(round(after_one, 4))
```

```inputs
round(after_two, 4)
```

```hint
The people who take the second test are the ones who tested positive
once. Among them, the share who are sick is `after_one`. That is the new
rate.
```

```solution
def share_sick(rate, accuracy):
    """Among a million people, the share of positive tests that are right."""
    people = 1_000_000
    sick = people * rate
    well = people - sick
    sick_and_positive = sick * accuracy
    well_and_positive = well * (1 - accuracy)
    return sick_and_positive / (sick_and_positive + well_and_positive)


after_one = share_sick(1 / 10_000, 0.99)
after_two = share_sick(after_one, 0.99)
print(round(after_one, 4), round(after_two, 4))
---
It is about 0.495, just under a half. Of the 10,098 people with one positive
test, 99 are sick. The second test finds about 98 of them, and wrongly
flags about 100 of the 9,999 well ones. A third positive test would raise
it to 0.99. The answer after each test becomes the base rate for the
next, which is Bayes' theorem used again and again. It only works if the
two tests make their mistakes separately. A second test that fails on
the same people as the first adds nothing.
```

## Your world

**11.** Here is a question from the world you chose.

<div class="dl-world" data-world="games-of-chance">

Here is a game for two. Roll two dice. You win if the total is 7 or
more, and I win if it is less. Seven is the middle total, so it looks
fair. Is it? Can you count your chance of winning, and then change the
rule so the game is fair?

```python exec
id: chances-world--games-of-chance
import itertools
from fractions import Fraction

outcomes = list(itertools.product(range(1, 7), repeat=2))
you_win = [roll for roll in outcomes if roll[0] + roll[1] >= 7]
print(Fraction(len(you_win), len(outcomes)))
```

```hint
Count the totals of 7 and above, and those below 7. Which total is in
the wrong group, and what could happen when it is rolled?
```

```solution
import itertools
from fractions import Fraction

outcomes = list(itertools.product(range(1, 7), repeat=2))
you_win = [roll for roll in outcomes if roll[0] + roll[1] >= 7]
print(Fraction(len(you_win), len(outcomes)))

above = [roll for roll in outcomes if roll[0] + roll[1] > 7]
below = [roll for roll in outcomes if roll[0] + roll[1] < 7]
print(Fraction(len(above), 36), Fraction(len(below), 36))
---
You win 7 times in 12, which is 21 of the 36 outcomes. The rule gives
you all of the 7s, the commonest total, and the two sides are otherwise
mirror images. Here is one fair rule. Above 7 wins for you, below 7 for
me, each $\frac{15}{36}$, and a 7 means roll again. An unfair game that
looks fair usually hides its advantage in a case like this, which sounds
like a boundary and is the most likely result.
```

</div>

<div class="dl-world" data-world="dinosaurs">

Is a find's period independent of the country it was found in? Compare
the chance that a find is Cretaceous with the same chance given the find
is from the United States (US), China (CN) or Canada (CA).

```python exec
id: chances-world--dinosaurs
finds = await load_csv("dinosaur-finds.csv", keep_default_na=False)

cretaceous = (finds.oldest_mya <= 145) & (finds.youngest_mya >= 66)
print("P(Cretaceous) =", round(cretaceous.mean(), 3))
```

```hint
`cretaceous[finds.country_code == "US"]` keeps only the United States'
rows, and `.mean()` of `True` and `False` values is the share that are
`True`.
```

```solution
finds = await load_csv("dinosaur-finds.csv", keep_default_na=False)

cretaceous = (finds.oldest_mya <= 145) & (finds.youngest_mya >= 66)
print("P(Cretaceous) =", round(cretaceous.mean(), 3))
for code in ["US", "CN", "CA"]:
    in_country = finds.country_code == code
    print(code, round(cretaceous[in_country].mean(), 3))
---
With the copy saved on {{snapshot: dinosaur-finds}}, 0.722 of all finds
are Cretaceous. So are 0.641 of the United States' finds and 0.652 of
China's, but 0.997 of Canada's. The country changes the chance, so the
two are not independent. For Canada they are far from it. Nearly all of
its finds come from Cretaceous rock, such as the badlands of Alberta. A
figure close to the overall one does not make them independent. The
question is whether knowing one changes the other.
```

</div>

<div class="dl-world" data-world="exoplanets">

Is the way a planet was found independent of the year it was found?
Compare the chance that a planet was found by transit, the dip in its
star's light, with the same chance for the planets found in 2000, 2010,
2016 and 2023.

```python exec
id: chances-world--exoplanets
planets = await load_csv("exoplanets.csv")

transit = planets.method == "Transit"
print("P(transit) =", round(transit.mean(), 3))
```

```hint
`transit[planets.discovered == 2016]` keeps only the planets found in
2016, and `.mean()` of `True` and `False` values is the share that are
`True`.
```

```solution
planets = await load_csv("exoplanets.csv")

transit = planets.method == "Transit"
print("P(transit) =", round(transit.mean(), 3))
for year in [2000, 2010, 2016, 2023]:
    in_year = planets.discovered == year
    print(year, in_year.sum(), "planets", round(transit[in_year].mean(), 3))
---
With the copy saved on {{snapshot: exoplanets}}, 0.739 of all known
planets were found by transit, but none of the 16 found in 2000, about
half in 2010, and 0.952 of the 1,504 in 2016. The two are far from
independent. Transits need a telescope that watches the same stars for a
long time, and the Kepler telescope, which did that, reported most of
its planets in the 2010s.
```

</div>

## From earlier

**12.** From *Counting*. Three dice show three different numbers in 120
of their 216 outcomes. What is the chance? Is it more or less than a
half?

<details class="dl-answer"><summary>answer</summary>

$\frac{120}{216} = \frac{5}{9} \approx 0.556$, a little more than a
half. Can you check it with `simulate`, and a trial that rolls three dice
and asks whether `len(set(roll)) == 3`?

</details>

**13.** From *Venn diagrams*. In a year group, 60% of students take
Maths, 50% take Physics, and 30% take both. What is the chance that a
student chosen at random takes neither?

<details class="dl-answer"><summary>answer</summary>

0.2. Maths or Physics is $0.6 + 0.5 - 0.3 = 0.8$, by inclusion-exclusion,
and neither is the complement: $1 - 0.8 = 0.2$. A Venn diagram of the
year group shows it as the region outside both circles.

</details>

**14.** From *Logic and truth*. By De Morgan, "not both sixes" is the
same event as "the first is not a six, or the second is not a six". Can
you calculate its chance both ways, and check that they agree?

<details class="dl-answer"><summary>answer</summary>

Both ways give $\frac{35}{36}$. The complement gives $1 - \frac{1}{36}$.
The "or", with inclusion-exclusion, gives
$\frac{5}{6} + \frac{5}{6} - \frac{25}{36} = \frac{60}{36} - \frac{25}{36} = \frac{35}{36}$.
Both routes reach the same answer, and one of them is much shorter.

</details>
