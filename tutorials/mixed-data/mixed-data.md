---
title: "Mixed problems: data, chance and logic"
practice_across:
  - sets-as-sorted-lists
  - venn-diagrams
  - logic-and-truth
  - counting-carefully
  - what-are-the-chances
  - three-doors
  - making-sense-of-data
  - pictures-worth-numbers
  - a-chart-that-tells-the-truth
year: "2026-2027"
version: 2026.09.26.1
---

# Mixed problems: data, chance and logic

Sets, logic, counting, chance and data are often the same subject, seen
from different sides. These problems move between them on purpose, and
do not say which page each one comes from. Choosing the tool is part of
the problem.

Each answer is hidden in a fold under its question. Some problems also
have a hint fold, to open first if you get stuck. When you can simulate
a problem, try it. If the simulation and the calculation disagree, ask
yourself: which one is answering the wrong question?

## Tools

This cell loads the modules the problems use, and defines one helper.
`simulate(trial)` runs a function of yours 100,000 times, and returns the
share of runs that returned `True`. The last line tries it on `six`,
which rolls one die, so the answer should be close to
$\frac{1}{6} \approx 0.167$.

```python exec
id: tools-1
import math
import random
import statistics
from collections import Counter


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


print(simulate(six))
```

## Counting into probability

**1.** A committee of 3 people is chosen at random from 5 women and 4
men. What is the probability that it is all women?

<details class="dl-answer"><summary>answer</summary>

$\dfrac{C(5,3)}{C(9,3)} = \dfrac{10}{84} \approx 0.119$.

There are $C(9,3) = 84$ possible committees, and $C(5,3) = 10$ of them
are all women.

Count the outcomes you want, and divide by all the outcomes. That step
connects counting to probability. Every probability on this page is a
counting problem underneath.

</details>

**2.** From the same group, what is the probability of at least one man?

<details class="dl-answer"><summary>answer</summary>

$1 - \dfrac{10}{84} = \dfrac{74}{84} \approx 0.881$.

"At least one" is nearly always easier as "one minus the chance of
none". You could also count the committees with exactly one man,
exactly two, and exactly three. That gives the same answer, with three
times the work.

</details>

**3.** Five dice are rolled. What is the probability of exactly two
sixes?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Pick one particular way it could happen: the first two dice are
   sixes, and the other three are not. What is the chance of that one
   way?
2. How many ways are there to choose which two of the five dice are the
   sixes?
3. Each of those ways has the same chance. Combine the two.

**Think about:** why multiply by the number of ways, and not add?

**Try this next:** check your answer with `simulate` and a trial that
rolls five dice and counts the sixes.

</details>

<details class="dl-answer"><summary>answer</summary>

About 0.161.

One particular way, sixes on the first two dice only, has chance
$\left(\frac{1}{6}\right)^2 \left(\frac{5}{6}\right)^3 =
\frac{125}{7{,}776}$. There are $C(5, 2) = 10$ ways to choose which two
dice are the sixes, and they cannot happen together, so their chances
add: $10 \times \frac{125}{7{,}776} = \frac{1{,}250}{7{,}776} \approx
0.161$. That is the binomial distribution, with $n = 5$ and
$p = \frac{1}{6}$.

</details>

**4.** Ten students choose three of themselves to give a talk. How many
ways can they choose? And how many if the three have different jobs:
one speaks, one runs the slides, and one takes questions?

<details class="dl-answer"><summary>answer</summary>

120, and 720.

With no jobs, only who is chosen matters: $C(10, 3) = 120$. With three
different jobs, the order matters too: $P(10, 3) = 10 \times 9 \times 8
= 720$. Each group of three can take the jobs in $3! = 6$ ways, and
$120 \times 6 = 720$.

</details>

## Sets and logic

**5.** In a class of 30, 18 students take maths, 15 take physics, and 8
take both. How many take neither?

<details class="dl-answer"><summary>answer</summary>

5.

$|M \cup P| = 18 + 15 - 8 = 25$, so 5 are outside both.

Draw the Venn diagram: 10 in maths only, 8 in both, 7 in physics only,
and 5 outside. The four regions have to add up to 30, and that is the
check.

</details>

**6.** One student from the same class is picked at random. What is the
probability that they take maths but not physics?

<details class="dl-answer"><summary>answer</summary>

$\dfrac{10}{30} = \dfrac{1}{3}$.

The answer is the size of a region in the Venn diagram, divided by the
total. On a finite set, probability is exactly "how big is this region
compared with the whole?"

</details>

**7.** Are "takes maths" and "takes physics" independent in that class?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Independence is an arithmetic test. It is not a feeling about whether
   two things are connected.
2. Calculate $P(M)$ and $P(P)$ from the class of 30.
3. Multiply them. That is what $P(M \cap P)$ would be if the two were
   independent.
4. Compare it with the real overlap: 8 out of 30.

**Think about:** they are close, but not equal. What would it say about
the class if the overlap were larger than the product? And smaller?

**Try this next:** how many students would have to take both for the
two to be exactly independent? Is that a whole number?

</details>

<details class="dl-answer"><summary>answer</summary>

By the arithmetic test, not quite. $P(M) = 0.6$ and $P(P) = 0.5$, and
their product is 0.30. That is 9 students out of 30. But the class has
8, and $P(M \cap P) = \dfrac{8}{30} \approx 0.267$.

Is one student short of 9 worth explaining, though? We can test it with
chance. Suppose the 18 maths places and the 15 physics places were given
at random, with nothing at all connecting them. How often would the
overlap be 8 or fewer? This uses `simulate` from the tools
cell:

```python
students = range(30)


def overlap_is_8_or_fewer():
    maths = set(random.sample(students, 18))
    physics = set(random.sample(students, 15))
    return len(maths & physics) <= 8


print(simulate(overlap_is_8_or_fewer))
```

It gives about 0.36. With no link at all, a class gives 8 or
fewer about a third of the time. An overlap of exactly 9, the
"independent" number, happens less often than that, about 0.29 of the
time.

So this class tells us nothing about a link between the two subjects.
The missing student is noise. The arithmetic test asks whether two
numbers are equal. With real data, the better question is whether the
difference is bigger than chance usually makes.

</details>

**8.** Write the truth table for $\neg(A \land B)$, and the truth table
for $\neg A \lor \neg B$. What do you notice?

<details class="dl-answer"><summary>answer</summary>

They are identical. This is De Morgan's law.

| $A$ | $B$ | $\neg(A \land B)$ | $\neg A \lor \neg B$ |
|---|---|---|---|
| T | T | F | F |
| T | F | T | T |
| F | T | T | T |
| F | F | T | T |

In the language of sets, it says
$\overline{A \cap B} = \bar{A} \cup \bar{B}$. The region outside the
overlap is the same as the region outside one circle or outside the
other. The Venn diagram and the truth table say the same thing.

In code, it is the rewrite that turns `not (a and b)` into
`not a or not b`. That is useful when you want a condition without the
`not` around the whole thing, which is often easier to read.

</details>

**9.** A system logs a warning if the temperature is above 80 *and*
either the fan has failed *or* the load is above 90%.

1. Write the condition in Python.
2. Write its negation: the condition for *no* warning.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Write the condition in ordinary words first: warn when the
   temperature is high *and* one of two other things is true.
2. Write that in Python. Be careful with brackets. `and` is applied
   before `or`, so the grouping matters.
3. For the negation, use De Morgan's law: the negation of "A and B" is
   "not A or not B".
4. The part inside the brackets needs negating too. Every comparison
   flips, and so does its boundary.

**Think about:** suppose you write `temperature < 80` where you should
write `<=`. Then one temperature fits neither condition.
Which one? And how long would that bug take to find?

**Try this next:** write a small loop that tests every combination of
inputs against both conditions. Use `assert` to check that the two are
always opposite.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
warn = temperature > 80 and (fan_failed or load > 90)
```

The negation uses De Morgan's law twice:

```python
quiet = temperature <= 80 or (not fan_failed and load <= 90)
```

Notice all the flips. `and` became `or`, `or` became `and`, and every
comparison flipped, including its boundary.

If you wrote `temperature < 80` there, a temperature of exactly 80
(with a failed fan or a high load) would make neither `warn` nor
`quiet` true. This is the bug that this kind of rewrite most often
causes.

</details>

## Data

**10.** Here are ten response times, in milliseconds:
`[12, 14, 13, 15, 14, 13, 12, 98, 14, 13]`. Summarise them. Which number
would you report?

<details class="dl-answer"><summary>answer</summary>

The mean is 21.8 and the median is 13.5. There are two modes, 13 and
14. The standard deviation is about 25.4 (dividing by $n$).

Report the median. One request took 98 ms, and the other nine took
about 13 ms. An "average response time of 22 ms" describes nothing that
happened.

For a real service, report the median *and* a high percentile. The 95th
percentile is the time that 95% of requests are no slower than. With
only ten values, that is the slowest one: 98 ms. That outlier is
somebody's slow request. It is not noise, and it is usually the
number that matters most.

</details>

**11.** Two exam sittings both have a mean of 60. The first has a
standard deviation of 5, and the second has a standard deviation of 18.
Sketch histograms that could fit.

<details class="dl-answer"><summary>answer</summary>

The first is a narrow hump around 60, with nearly everyone between 50
and 70.

The second is wide. It could be one broad hump. Or it could be two
separate humps, near 40 and 80, with almost nobody in the middle. Those
two shapes have the same mean and standard deviation, but they tell you
very different things about the class.

So always look at the histogram.

</details>

**12.** A dataset of 1,000 values has a mean of 50 and a standard
deviation of 10. Roughly how many values are between 30 and 70?

<details class="dl-answer"><summary>answer</summary>

About 950, *if* the distribution is roughly bell-shaped.

30 and 70 are two standard deviations either side of the mean. For a
bell-shaped curve (a *normal distribution*), about 95% of the values
fall within two standard deviations. About 68% fall within one, and
about 99.7% within three.

The "if" matters a lot. For a distribution of any shape, the guarantee
is much weaker. Chebyshev's inequality promises only that at least 75%
are within two standard deviations. That is true for any data at all,
and it is usually far below the real figure.

</details>

**13.** In NASA's list of planets around other stars, the median orbit
is about 11 days and the mean about 71,000 days. A reporter writes: "The
typical exoplanet takes 195 years to go round its star." Where did 195
come from, and what should the sentence say?

<details class="dl-answer"><summary>answer</summary>

It came from the mean: $71{,}126 \div 365.25 \approx 195$ years. But the
orbits are skewed far to the right, and one planet, whose year lasts
about a million of ours, is most of that total. Remove it and the mean
falls to about 12 years. The median hardly moves. A typical planet in the
list goes round its star in about 11 days. And "typical exoplanet" is
itself too strong. The list holds the planets that are easiest to find,
and short orbits are the easiest of all.

</details>

## Putting it together

**14.** A spam filter flags 95% of spam. It also wrongly flags 2% of
real mail. 40% of incoming mail is spam. A message is flagged. What is
the probability that it is spam?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Do not start with a formula. Take a thousand messages, and count what
   happens to them.
2. How many are spam? How many of those get flagged?
3. How many are real mail? How many of *those* get flagged anyway?
4. Of all the flagged messages, what fraction was spam?

**Think about:** compare this with the disease example, where a test
that sounded just as accurate gave about 1%. The test did not change.
The base rate did.

**Try this next:** what if only 2% of mail were spam? Calculate it with
counts again, and see how far the answer moves.

</details>

<details class="dl-answer"><summary>answer</summary>

About 96.9%.

Out of 1,000 messages, 400 are spam, and 380 of those are flagged. 600
are real, and 12 of those are flagged. So 380 of the 392 flagged
messages are spam: $\dfrac{380}{392} \approx 0.969$.

Compare the rare disease in
[Probability: simple, compound and conditional](tutorial:what-are-the-chances).
There, numbers that sounded similar gave about 1%. The whole difference
is the *base rate*, how common the thing is before any test. Spam is
common, and the disease is rare. The test does not decide the answer.

</details>

**15.** A quiz has 10 multiple-choice questions, each with 4 options.
You guess every answer. What is the probability of getting exactly 5
right? And at least 5?

<details class="dl-answer"><summary>answer</summary>

About 0.0584 for exactly 5, and about 0.0781 for at least 5.

Exactly 5: $C(10,5) \times 0.25^5 \times 0.75^5$.

At least 5: add up the same kind of term for 5, 6, 7, 8, 9 and 10
right.

The counting term $C(10,5)$ is there because there are 252 different
ways to get five of the ten right. This is the binomial distribution. It
uses the numbers from Pascal's triangle, multiplied by probabilities.

</details>

**16.** Three friends each pick a number from 1 to 10. What is the
probability that at least two of them pick the same number?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. "At least two the same" is awkward to count directly, because it can
   happen in several ways.
2. Count the opposite instead: all three different.
3. The first person can pick anything. What fraction of the choices
   keeps the second person different? And the third?
4. Subtract from 1.

**Think about:** this is the birthday problem, with ten days in the year
instead of 365. The method is identical. Only the numbers change.

**Try this next:** out of 10 numbers, how many people does it take for
"at least two the same" to go above one half? Out of 365?

</details>

<details class="dl-answer"><summary>answer</summary>

0.28.

All different: $\dfrac{10}{10} \times \dfrac{9}{10} \times \dfrac{8}{10} = 0.72$.
So at least two the same: $1 - 0.72 = 0.28$.

This is the birthday problem with ten days in the year. The same
calculation with 365 days and 23 people gives 50.7%. The method is the
same: count the ways to *avoid* it, and subtract from 1.

</details>

**17.** Two events have $P(A) = 0.6$ and $P(B) = 0.5$. What are the
largest and smallest possible values of $P(A \cap B)$?

<details class="dl-answer"><summary>answer</summary>

It is between 0.1 and 0.5.

The largest is when $B$ sits completely inside $A$. Then the overlap is
all of $B$: 0.5.

The smallest is when they overlap as little as possible. They cannot
avoid each other completely, because $0.6 + 0.5 = 1.1$, which is more
than 1. So the overlap is at least $1.1 - 1 = 0.1$.

Draw it as two circles in a box, and slide them around. If the events
were independent, the overlap would be $0.6 \times 0.5 = 0.30$. That is
one particular value in the range, and not a default.

</details>

**18.** You have a list of 10,000 email addresses, with duplicates. You
also have a list of 500 people who have unsubscribed. How would you
produce the mailing list? What could go wrong?

<details class="dl-answer"><summary>answer</summary>

```python
mailing = {e.strip().lower() for e in everyone} - {e.strip().lower() for e in unsubscribed}
```

This is a set difference, which is exactly the operation the problem
describes. Turning each list into a set also removes the duplicates.

What could go wrong? Suppose an address has different capital letters,
or extra spaces at the end, on one list but not the other. Without the
`.strip().lower()`, it would survive the subtraction and get mailed.
Other cases pass even with it: an address written
`name+tag@example.com` on one list and `name@example.com` on the other,
or an address on a domain that has since changed its name.

The whole job is to clean the addresses into one standard form before
comparing them. And the failure is silent. The code runs, the count
looks right, and somebody who asked to be left alone gets an email.

</details>

**19.** Design a small study: does a coin you own land heads more than
half the time?

1. What would you measure?
2. How many trials would you run?
3. What result would convince you?

<details class="dl-answer"><summary>answer</summary>

The shape of the answer matters more than the exact numbers.

With $n$ flips of a fair coin, the number of heads has a standard
deviation of about $\dfrac{\sqrt{n}}{2}$. For 100 flips, that is
$\dfrac{10}{2} = 5$. So anything from 40 to 60 heads is normal. A coin
has to be badly biased for 100 flips to show it.

For 10,000 flips, the standard deviation is $\dfrac{100}{2} = 50$. A
real bias to 51% heads would appear as about 5,100 heads. That is two
standard deviations from 5,000, the fair result. It suggests a bias,
but it does not prove one.

So finding a small bias takes far more trials than most people
expect. And a result inside the normal range is not
evidence that the coin is fair, either. "No difference found" and "no
difference exists" are not the same sentence.

</details>

**20.** Three prisoners, A, B and C, are told that one of them, chosen
at random, will be set free. A asks the guard, who knows, to name one of
the other two who will *not* be freed. If neither B nor C is to be freed,
the guard chooses between them at random. The guard says "B". A thinks:
now it is between me and C, so my chance has gone up to a half. Is A
right?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Before anything is said, each prisoner's chance is a third.
2. Could the guard's answer have been anything other than "B" or "C"?
   Does hearing it tell A anything about A?
3. Have you met a puzzle where somebody who knows the answer opens one
   of the other two doors?

**Try this next:** simulate it. Choose who is freed at random, let the
guard answer by the rules, keep only the runs where he says "B", and
count how often A is the one freed.

</details>

<details class="dl-answer"><summary>answer</summary>

No. A's chance is still a third, and C's is now two thirds.

It is the Monty Hall problem with prisoners for doors. The guard is the
host, who knows, and who never names the one to be freed. Whatever
happens, the guard can name one of B and C, so his answer says nothing
about A. It says a great deal about C, who was not named, like the door
the host leaves shut. A simulation that keeps only the runs where the
guard says "B" finds A freed in about a third of them.

</details>

**21.** What is the chance of at least one six in $n$ rolls of a die?
Draw it for $n$ from 1 to 20. Which kind of chart fits, what should its
y axis be, and at which $n$ does the chance first pass a half?

<details class="dl-answer"><summary>answer</summary>

The chance is $1 - \left(\frac{5}{6}\right)^n$, by the complement.
It first passes a half at $n = 4$, with about 0.518.

```python
import matplotlib.pyplot as plt

rolls = list(range(1, 21))
chances = [1 - (5 / 6) ** n for n in rolls]
plt.plot(rolls, chances, marker="o")
plt.ylim(0, 1)
plt.axhline(0.5, color="grey", linestyle="--")
plt.xlabel("rolls")
plt.ylabel("chance of at least one six")
```

A line chart with dots fits, because $n$ is in order, and the dots show that
only whole numbers of rolls exist. The y axis should run from 0 to 1,
the whole range a chance can take. If the library chose the range, it would
make the curve look steeper than it is. The chance climbs quickly at
first, then more and more slowly, and never reaches 1.

</details>

**22.** A class rolls two dice 20 times on Monday and gets eight 7s. On
Tuesday, 20 rolls give three 7s. A student draws two bars, Monday and
Tuesday, with the axis running from 2 to 9, under the headline "Sevens
collapse by 60%". Give two reasons the headline could be wrong, and say
which day was the unusual one.

<details class="dl-answer"><summary>answer</summary>

First, the chart. An axis from 2 makes 8 look six times as tall as 3,
but it is not even three times as big.

Second, the numbers. 20 rolls is a tiny sample. A 7 appears 1 time in 6,
so 20 rolls should give about 3.3, plus or minus about 1.7. Tuesday's
three is exactly what to expect. Monday's eight is the surprise. Eight
or more happens only about once in 90 sessions. The "collapse" is a
lucky Monday, followed by an ordinary Tuesday, drawn on a cut axis.
Starting from the unusual day uses the chosen-window trick, with a window
of two.

</details>
