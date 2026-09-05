---
title: "What Are the Chances — Practice"
slug: what-are-the-chances-practice
practice_for: what-are-the-chances
module: mit-pdp-maths-prog-integration
module_title: "Programming and Maths, Integrated"
year: "2026-2027"
series: data-chance-and-logic
version: 2026.08.23.1
---

# What Are the Chances — Practice

Answers are folded. Calculate first, then simulate — and when the two disagree, one of them is wrong and it is usually not the simulation.

Several of these are adapted from the statistics and probability worksheet in the Mathematics repository.

## Tools

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

## Basic Probability

**1.** A fair die is rolled. Find the probability of each.

- (a) a 4
- (b) an even number
- (c) a number above 4
- (d) a 7

<details class="dl-answer"><summary>answer</summary>

(a) 1/6. (b) 1/2. (c) 1/3. (d) 0.

Every probability is between 0 and 1, and an impossible event is exactly 0 rather than very small.

</details>

**2.** A bag holds 5 red, 3 blue and 2 green counters. Find the probability of drawing each colour, and check they sum to 1.

<details class="dl-answer"><summary>answer</summary>

0.5, 0.3, 0.2, and they sum to 1.

They must. The outcomes are exhaustive and mutually exclusive, so their probabilities partition the whole. A set of probabilities that does not sum to 1 has either a missing case or a double-counted one.

</details>

**3.** The chance of rain tomorrow is 0.3. What is the chance of no rain?

<details class="dl-answer"><summary>answer</summary>

0.7.

The complement rule: $P(\text{not } A) = 1 - P(A)$. It is trivial and it is the single most useful trick in the topic, because "at least one" problems are almost always easier as "not none".

</details>

## Compound Events

**4.** Two dice are rolled. Find the probability of each.

- (a) both sixes
- (b) a total of 7
- (c) a total of 12
- (d) at least one six

<details class="dl-answer"><summary>answer</summary>

(a) 1/36. (b) 6/36 = 1/6. (c) 1/36. (d) 11/36.

(b) is the most likely total, because there are six ways to make it and only one to make 12.

(d) is the complement trick: the chance of *no* six is $\frac{5}{6} \times \frac{5}{6} = \frac{25}{36}$, so at least one is $\frac{11}{36}$. Adding $\frac16 + \frac16$ gives 12/36 and double-counts the double six.

</details>

**5.** One card is drawn from 52. Find the probability of each.

- (a) an ace
- (b) a heart
- (c) an ace or a heart
- (d) a face card
- (e) red and a face card
- (f) red or a face card

<details class="dl-answer"><summary>answer</summary>

(a) 4/52. (b) 13/52. (c) 16/52 — $\frac{4}{52} + \frac{13}{52} - \frac{1}{52}$, subtracting the ace of hearts. (d) 12/52. (e) 6/52. (f) 32/52 — $\frac{26 + 12 - 6}{52}$.

Every "or" here needs the overlap subtracted, and every "and" is the overlap. This is inclusion–exclusion again, one tutorial later and wearing different clothes.

</details>

**6.** Two cards are drawn without replacement. Find the probability both are hearts.

<details class="dl-answer"><summary>answer</summary>

$\frac{13}{52} \times \frac{12}{51} = \frac{1}{17} \approx 0.0588$.

The second fraction is where "without replacement" lives. With replacement it would be $\frac{13}{52} \times \frac{13}{52} = 0.0625$ — slightly higher, because the first heart is not removed from the pack.

</details>

**7.** A coin is flipped four times. Find the probability of exactly two heads. Of at least one head.

<details class="dl-answer"><summary>answer</summary>

$\frac{6}{16} = 0.375$, and $\frac{15}{16} = 0.9375$.

Exactly two heads: $C(4,2) = 6$ of the 16 equally likely sequences. Pascal's triangle counting again.

At least one head: everything except the single all-tails outcome.

</details>

**8.** What is the probability of a royal flush in a five-card hand?

<details class="dl-answer"><summary>answer</summary>

$\frac{4}{2{,}598{,}960} \approx 1.5 \times 10^{-6}$, or about 1 in 650,000.

Four royal flushes exist, one per suit, out of $C(52,5)$ hands.

Simulating this is instructive precisely because it fails: a million deals will usually turn up one or two, and might turn up none, and that variability is itself the lesson.

</details>

## Independence

**9.** A coin has come up heads five times running. What is the probability of heads next?

<details class="dl-answer"><summary>answer</summary>

One half.

The coin has no memory. Believing otherwise is the gambler's fallacy, and it is nearly universal.

The thing that *is* unlikely is five heads in a row *before you start*: 1/32. Once it has happened, it has happened, and it changes nothing about the next flip.

</details>

**10.** Which of these pairs are independent?

- (a) Two rolls of a die
- (b) Drawing two cards without replacement
- (c) It raining today and it raining tomorrow
- (d) A card being red and being a face card

<details class="dl-answer"><summary>answer</summary>

(a) and (d) are independent. (b) and (c) are not.

(d) surprises people: $P(\text{red}) = \frac12$, $P(\text{face}) = \frac{12}{52}$, and $P(\text{both}) = \frac{6}{52}$, which is exactly the product. Half the face cards are red, so knowing the colour tells you nothing about whether it is a face card.

That is what independence means — and it is a numerical fact to be checked rather than a feeling about whether things are related.

</details>

**11.** In a class of 23, what is the probability that two people share a birthday?

<details class="dl-answer"><summary>answer</summary>

About 50.7%.

Via the complement: the chance that all 23 differ is $\frac{365}{365} \times \frac{364}{365} \times \cdots \times \frac{343}{365} \approx 0.4927$.

```python
p = 1.0
for i in range(23):
    p = p * (365 - i) / 365
print(1 - p)
```

Everyone's first guess is far too low, because the question sounds like "does someone share *my* birthday" — which for 23 people is about 6%. There are 253 pairs in a class of 23, and it is the pairs that matter.

</details>

## Simulation

**12.** Simulate 10,000 die rolls and compare the proportion of sixes to 1/6.

<details class="dl-answer"><summary>answer</summary>

```python
import random
rolls = [random.randint(1, 6) for _ in range(10000)]
print(rolls.count(6) / 10000)
```

Somewhere near 0.167, and different each time. With 10,000 trials the answer is typically right to about two decimal places; with 100 trials it is not reliable to one.

The error shrinks like $\frac{1}{\sqrt{n}}$, so a hundred times more trials gives ten times the accuracy. That is a poor exchange rate and it is why simulation is a check rather than a substitute.

</details>

**13.** Simulate the two-hearts problem and compare to 1/17.

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

About 0.0588. `random.sample` draws without replacement, which is exactly the condition being modelled — using `random.choice` twice would silently simulate the wrong problem.

</details>

**14.** Simulate the Monty Hall problem: three doors, one prize, you pick one, the host opens a losing door, and you may switch.

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

The simulation is shorter than the argument, which is why it is worth writing. The whole problem reduces to one line: you switch into a win exactly when your first guess was wrong, and your first guess is wrong two times in three.

The host's behaviour matters enormously. If they opened a door at random and it happened to be empty, switching would be an even bet. The puzzle only works because they know where the prize is and never open it.

</details>

## Conditional Probability

**15.** You draw a card and see that it is red. What is the probability it is a heart?

<details class="dl-answer"><summary>answer</summary>

One half.

Half the red cards are hearts. Formally, $P(\text{heart} \mid \text{red}) = \frac{13/52}{26/52}$.

Conditioning narrows the world you are counting in: the denominator becomes the thing you now know.

</details>

**16.** A test for a disease is 99% accurate both ways. The disease affects 1 person in 10,000. You test positive. What is the probability you have it?

<details class="dl-answer"><summary>answer</summary>

About 1%.

In a million people: 100 have it, and 99 of those test positive. The other 999,900 do not have it, and 1% of them — 9,999 people — test positive anyway.

So 99 true positives sit among 10,098 positives, which is 0.98%.

The false positives swamp the true ones because the disease is rare. This is Bayes' theorem, and the reason to work it out with counts rather than the formula is that the counts make it obvious. Nearly everybody, doctors included, guesses 99%.

</details>

**17.** Two dice are rolled and you are told at least one is a six. What is the probability both are?

<details class="dl-answer"><summary>answer</summary>

1/11, not 1/6.

There are 11 outcomes with at least one six, and one of them is the double six.

Compare: if you are told *the first die* is a six, the answer is 1/6. Same-sounding information, different conditioning, different answer — and this is where most probability arguments actually go wrong.

</details>

**18.** A family has two children and at least one is a girl. What is the probability both are?

<details class="dl-answer"><summary>answer</summary>

1/3.

The four equally likely combinations are GG, GB, BG, BB. Ruling out BB leaves three, one of which is GG.

The same trap as the dice. And as with the dice, "the elder is a girl" gives 1/2 instead — the answer depends on precisely what you were told, not on what is true.

</details>
