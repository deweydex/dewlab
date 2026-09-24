---
title: "Probability: simple, compound and conditional — Practice"
practice_for: what-are-the-chances
year: "2026-2027"
version: 2026.08.23.1
---

# Probability: simple, compound and conditional — Practice

Each answer is hidden until you open it. For each problem, calculate first, then simulate.

What if the two answers disagree? Then one of them is wrong, and usually it is the calculation.

Several of these are adapted from the statistics and probability worksheet in the Mathematics repository.

## Tools

Run this cell once before you start. It loads the `math` and `random` modules, and gives you two functions:

- `probability(favourable, total)` divides one count by the other.
- `simulate(trial)` runs a trial many times (100,000 by default) and gives back the proportion of runs that came out `True`. You give it a small function that runs one trial and returns `True` or `False`.

The last line shows one way to call it: `lambda: random.randint(1, 6) == 6` is a one-line function that rolls a die and says whether it came up 6. `random.randint(1, 6)` picks a whole number from 1 to 6.

```python exec
id: tools-1
import math, random

def probability(favourable, total):
    return favourable / total


def simulate(trial, n=100000):
    """Run a trial function n times and report the proportion of Trues."""
    return sum(1 for _ in range(n) if trial()) / n


print(probability(4, 52))
print(simulate(lambda: random.randint(1, 6) == 6))
```

## Basic probability

**1.** A fair die is rolled. What is the probability of each of these?

- (a) a 4
- (b) an even number
- (c) a number above 4
- (d) a 7

<details class="dl-answer"><summary>answer</summary>

(a) 1/6. (b) 1/2. (c) 1/3. (d) 0.

Every probability is between 0 and 1. An impossible event, like rolling a 7, has a probability of exactly 0. It is not a very small number; it is 0.

</details>

**2.** A bag holds 5 red, 3 blue and 2 green counters. What is the probability of drawing each color? Check that the three probabilities add up to 1.

<details class="dl-answer"><summary>answer</summary>

0.5, 0.3 and 0.2, and they add up to 1.

They must add up to 1. Every counter is one of the three colors, so no case is missing. No counter has two colors, so the events are mutually exclusive. Together, the three events cover every outcome exactly once.

If a list of probabilities like this does not add up to 1, either a case is missing or a case is counted twice.

</details>

**3.** The chance of rain tomorrow is 0.3. What is the chance of no rain?

<details class="dl-answer"><summary>answer</summary>

0.7.

This uses the complement rule: $P(\text{not } A) = 1 - P(A)$. The rule is short, and it is the most useful trick in this topic. A question that asks for "at least one" is almost always easier to answer as "1 minus the chance of none".

</details>

## Compound events

**4.** Two dice are rolled. What is the probability of each of these?

- (a) both sixes
- (b) a total of 7
- (c) a total of 12
- (d) at least one six

<details class="dl-answer"><summary>answer</summary>

(a) 1/36. (b) 6/36 = 1/6. (c) 1/36. (d) 11/36.

A total of 7 is the most likely total. There are six ways to make it (1 and 6, 2 and 5, and so on), and only one way to make 12.

(d) uses the complement trick. The chance of *no* six is $\frac{5}{6} \times \frac{5}{6} = \frac{25}{36}$, so the chance of at least one six is $1 - \frac{25}{36} = \frac{11}{36}$. Adding $\frac16 + \frac16$ gives $\frac{12}{36}$, which is wrong: it counts the double six twice.

</details>

**5.** One card is drawn from a deck of 52. What is the probability of each of these?

- (a) an ace
- (b) a heart
- (c) an ace or a heart
- (d) a face card
- (e) red and a face card
- (f) red or a face card

<details class="dl-answer"><summary>answer</summary>

- (a) 4/52.
- (b) 13/52.
- (c) 16/52. That is $\frac{4}{52} + \frac{13}{52} - \frac{1}{52}$: we subtract the ace of hearts, because it was counted twice.
- (d) 12/52.
- (e) 6/52.
- (f) 32/52. That is $\frac{26 + 12 - 6}{52}$.

Each "or" here needs the overlap subtracted, and each "and" is the overlap. This idea comes back with sets in [Sets: building them from sorted lists](tutorial:sets-as-sorted-lists), where it is called the inclusion-exclusion principle.

</details>

**6.** Two cards are drawn without replacement. What is the probability that both are hearts?

<details class="dl-answer"><summary>answer</summary>

$\frac{13}{52} \times \frac{12}{51} = \frac{1}{17} \approx 0.0588$.

The second fraction is where "without replacement" shows: only 12 hearts are left among 51 cards. With replacement, the first card goes back into the deck, so the answer would be $\frac{13}{52} \times \frac{13}{52} = 0.0625$. That is slightly higher, because the first heart is still in the deck.

</details>

**7.** A coin is flipped four times. What is the probability of exactly two heads? What is the probability of at least one head?

<details class="dl-answer"><summary>answer</summary>

$\frac{6}{16} = 0.375$, and $\frac{15}{16} = 0.9375$.

Four flips give $2^4 = 16$ equally likely sequences, such as HHTT. For exactly two heads, we choose which 2 of the 4 flips are heads: $C(4,2) = 6$ ways. This is the Pascal's triangle counting from the practice page of [Counting: factorials, permutations and combinations](tutorial:counting-carefully) again.

For at least one head, every sequence counts except one: all tails. That gives $\frac{15}{16}$.

</details>

**8.** What is the probability of a royal flush in a five-card hand?

<details class="dl-answer"><summary>answer</summary>

$\frac{4}{2{,}598{,}960} \approx 1.5 \times 10^{-6}$, or about 1 in 650,000.

There are four royal flushes, one in each suit, out of $C(52,5)$ hands.

A simulation of this teaches something because it struggles. A million deals usually find one or two royal flushes, and sometimes none. How much the count changes from run to run is the lesson.

</details>

## Independence

**9.** A coin has come up heads five times in a row. What is the probability of heads on the next flip?

<details class="dl-answer"><summary>answer</summary>

One half.

The coin has no memory. The belief that a tails is now "due" is called the gambler's fallacy, and nearly everybody feels it.

What *is* unlikely is five heads in a row, judged *before you start*: $\frac{1}{32}$. Once those five flips have happened, they change nothing about the next flip.

</details>

**10.** Which of these pairs are independent?

- (a) Two rolls of a die
- (b) Drawing two cards without replacement
- (c) It raining today and it raining tomorrow
- (d) A card being red and being a face card

<details class="dl-answer"><summary>answer</summary>

(a) and (d) are independent. (b) and (c) are not.

(d) surprises people. $P(\text{red}) = \frac12$ and $P(\text{face}) = \frac{12}{52}$. $P(\text{both}) = \frac{6}{52}$, which is exactly $\frac12 \times \frac{12}{52}$. Half the face cards are red, so knowing the color tells you nothing about whether it is a face card.

Independence is a fact about numbers that we can check. It is not a feeling about whether two things seem related.

</details>

**11.** In a class of 23, what is the probability that at least two people share a birthday?

<details class="dl-answer"><summary>answer</summary>

About 50.7%.

We use the complement. The chance that all 23 birthdays are different is $\frac{365}{365} \times \frac{364}{365} \times \cdots \times \frac{343}{365} \approx 0.4927$.

```python
p = 1.0
for i in range(23):
    p = p * (365 - i) / 365
print(1 - p)
```

Almost everyone's first guess is far too low. The question sounds like "does someone share *my* birthday?", and for 23 people that is only about 6%. But any pair of people can share a birthday. A class of 23 has $C(23,2) = 253$ pairs, and it is the pairs that matter.

(This ignores 29 February, and assumes every birthday is equally likely.)

</details>

## Simulation

**12.** Can you simulate 10,000 die rolls, and compare the proportion of sixes with 1/6?

<details class="dl-answer"><summary>answer</summary>

```python
import random
rolls = [random.randint(1, 6) for _ in range(10000)]
print(rolls.count(6) / 10000)
```

The answer is somewhere near 0.167, and different each time. With 10,000 trials the answer is usually right to about two decimal places. With 100 trials, it is not reliable even to one.

The error shrinks like $\frac{1}{\sqrt{n}}$, where $n$ is the number of trials. So a hundred times more trials gives only ten times the accuracy. That is a poor trade. It is why we use simulation to check a calculation, and not in place of one.

</details>

**13.** Can you simulate the two-hearts problem, and compare your answer with 1/17?

<details class="dl-answer"><summary>answer</summary>

```python
import random

deck = [(rank, suit) for suit in "HDCS" for rank in range(1, 14)]
hits = 0
for _ in range(100000):
    a, b = random.sample(deck, 2)
    if a[1] == "H" and b[1] == "H":
        hits += 1
print(hits / 100000, 1 / 17)
```

About 0.0588. `random.sample(deck, 2)` draws 2 cards without replacement, which is what the problem describes. Calling `random.choice` twice could pick the same card twice. That would simulate a different problem, and Python would give no warning.

</details>

**14.** Can you simulate the Monty Hall problem? There are three doors and one prize. You pick a door. The host, who knows where the prize is, opens a different door with no prize behind it. Then you may switch to the other closed door.

The next tutorial, [The Monty Hall problem: three doors and a simulation](tutorial:three-doors), is all about this puzzle. You may like to try this problem after reading it.

<details class="dl-answer"><summary>answer</summary>

Switching wins two thirds of the time.

```python
import random

wins = 0
for _ in range(100000):
    prize, choice = random.randrange(3), random.randrange(3)
    if prize != choice:          # switching wins exactly when the first pick was wrong
        wins += 1
print(wins / 100000)
```

The simulation is shorter than the argument, which is a good reason to write it. The whole problem comes down to one line. Switching wins exactly when your first guess was wrong, and your first guess is wrong two times in three.

How the host behaves matters a great deal. Suppose the host opened a door at random, and it happened to have no prize. Then switching would win only half the time. The puzzle works because the host knows where the prize is, and never opens that door.

</details>

## Conditional probability

**15.** You draw a card and see that it is red. What is the probability it is a heart?

<details class="dl-answer"><summary>answer</summary>

One half.

Half the red cards are hearts. With the formula, $P(\text{heart} \mid \text{red}) = \frac{13/52}{26/52} = \frac{13}{26} = \frac12$.

Knowing the card is red shrinks the group we count in. We now count only among the 26 red cards, so the bottom of the fraction becomes the thing we know.

</details>

**16.** A test for a disease is 99% accurate both ways: it is right for 99% of people who have the disease, and for 99% of people who do not. The disease affects 1 person in 10,000. You test positive. What is the probability that you have the disease?

<details class="dl-answer"><summary>answer</summary>

About 1%.

Picture a million people. 100 of them have the disease, and 99 of those test positive. The other 999,900 do not have it, but 1% of them, which is 9,999 people, test positive anyway.

So there are $99 + 9{,}999 = 10{,}098$ positive tests, and only 99 of them are true. $\frac{99}{10{,}098}$ is about 0.98%.

The disease is rare, so the false positives far outnumber the true ones. This is Bayes' theorem at work. Counting people, as we did here, makes the answer much easier to see than the formula does. Nearly everybody, doctors included, guesses 99%.

</details>

**17.** Two dice are rolled, and you are told that at least one of them is a six. What is the probability that both are sixes?

<details class="dl-answer"><summary>answer</summary>

1/11. The answer is not 1/6.

There are 11 outcomes with at least one six, and only one of them is the double six.

Now compare: if you are told that *the first die* is a six, the answer is 1/6. The two pieces of information sound alike, but they narrow the outcomes differently, so the answers are different. Most wrong probability arguments go wrong at exactly this point.

</details>

**18.** A family has two children, and at least one of them is a girl. What is the probability that both are girls?

<details class="dl-answer"><summary>answer</summary>

1/3.

Write the older child first. The four equally likely cases are GG, GB, BG and BB. We know BB did not happen, so three cases are left, and one of them is GG.

This is the same trap as the dice question. And as with the dice, being told "the older child is a girl" gives 1/2 instead. The answer depends on exactly what you were told, not on what is true.

</details>
