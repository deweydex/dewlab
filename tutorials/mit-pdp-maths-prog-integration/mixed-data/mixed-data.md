---
title: "Mixed Problems — Data, Chance and Logic"
slug: mixed-data
practice_across:
  - counting-carefully
  - what-are-the-chances
  - making-sense-of-data
  - pictures-worth-numbers
  - sets-as-sorted-lists
  - logic-and-truth
  - venn-diagrams
module: mit-pdp-maths-prog-integration
module_title: "Programming and Maths, Integrated"
year: "2026-2027"
series: data-chance-and-logic
version: 2026.08.23.1
---

# Mixed Problems — Data, Chance and Logic

Counting, probability, sets and logic keep turning out to be the same subject seen from four sides. These problems move between them on purpose.

Answers are folded. Where a problem can be simulated, simulate it — and where the simulation and the calculation disagree, work out which one is answering the wrong question.

## Tools

```python exec
id: tools-1
import math, random, statistics
from collections import Counter


def simulate(trial, n=100000):
    """Proportion of n runs of `trial` that come out True."""
    return sum(1 for _ in range(n) if trial()) / n


print(math.comb(52, 5), simulate(lambda: random.randrange(6) == 0))
```

## Counting Into Probability

**1.** A committee of 3 is chosen at random from 5 women and 4 men. What is the probability it is all women?

<details class="dl-answer"><summary>answer</summary>

$\dfrac{C(5,3)}{C(9,3)} = \dfrac{10}{84} \approx 0.119$.

Counting the favourable arrangements and dividing by all of them is the bridge between the two tutorials. Every probability on this page is a counting problem underneath.

</details>

**2.** From the same group, what is the probability of at least one man?

<details class="dl-answer"><summary>answer</summary>

$1 - \frac{10}{84} = \frac{74}{84} \approx 0.881$.

"At least one" is nearly always easier as one minus "none". Counting the committees with exactly one, exactly two and exactly three men gives the same answer and three times the work.

</details>

**3.** Four cards are dealt. What is the probability they are all different suits?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Deal the cards one at a time and ask what has to be true at each step.
2. The first card can be anything. What fraction of the remaining pack keeps the second card in a new suit?
3. Carry on for the third and fourth. The denominators shrink because cards have gone.
4. Now count a second way: how many four-card *hands* have one of each suit, out of all four-card hands?

**Think about:** the two routes look completely different and give the same number. When they do not, one of them has confused ordered sequences with unordered hands.

**Try this next:** the probability that four cards are all *different ranks*. Same shape, different numbers.

</details>

<details class="dl-answer"><summary>answer</summary>

About 0.1055.

$\frac{52}{52} \times \frac{39}{51} \times \frac{26}{50} \times \frac{13}{49}$ — after each card, one suit is spoken for.

Equivalently $\frac{13^4}{C(52,4)}$ counting hands rather than sequences: $\frac{28561}{270725}$. Two ways of counting, one answer, which is the check.

</details>

**4.** How many different five-card hands contain exactly two aces?

<details class="dl-answer"><summary>answer</summary>

103,776.

Choose 2 aces from 4, and 3 non-aces from the other 48: $C(4,2) \times C(48,3) = 6 \times 17{,}296$.

The probability is about 0.0399. Multiplying the choices for independent parts of a selection is the counting move that makes most card problems tractable.

</details>

## Sets and Logic

**5.** In a class of 30, 18 take maths, 15 take physics, and 8 take both. How many take neither?

<details class="dl-answer"><summary>answer</summary>

5.

$|M \cup P| = 18 + 15 - 8 = 25$, so 5 are outside both.

Draw it: 10 in maths only, 8 in both, 7 in physics only, 5 outside. The four regions have to add to 30, and that is the check.

</details>

**6.** From the same class, one student is picked at random. What is the probability they take maths but not physics?

<details class="dl-answer"><summary>answer</summary>

$\frac{10}{30} = \frac13$.

The Venn diagram region is the answer, divided by the total. Probability on a finite set is exactly "how big is this region compared with the whole".

</details>

**7.** Are "takes maths" and "takes physics" independent in that class?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Independence is not a feeling about whether two things are connected. It is an arithmetic test.
2. Work out $P(M)$ and $P(P)$ from the class of 30.
3. Multiply them. That is what $P(M \cap P)$ would be if the two were independent.
4. Compare with the actual overlap of 8 out of 30.

**Think about:** they are close but not equal. What would it mean about the class if the overlap were larger than the product? Smaller?

**Try this next:** how many students would have to take both for the two to be exactly independent? Is that a whole number?

</details>

<details class="dl-answer"><summary>answer</summary>

Not quite. $P(M) = 0.6$, $P(P) = 0.5$, and their product is 0.30. But $P(M \cap P) = \frac{8}{30} \approx 0.267$.

So taking maths makes physics slightly *less* likely than chance — a mild negative association, probably a timetable clash rather than anything about the students.

Independence is a numerical coincidence, and the interesting cases are the ones where it nearly holds and does not.

</details>

**8.** Write the truth table for $\neg(A \land B)$ and for $\neg A \lor \neg B$. What do you notice?

<details class="dl-answer"><summary>answer</summary>

They are identical — De Morgan's law.

| A | B | ¬(A∧B) | ¬A∨¬B |
|---|---|---|---|
| T | T | F | F |
| T | F | T | T |
| F | T | T | T |
| F | F | T | T |

In set language it is $\overline{A \cap B} = \bar{A} \cup \bar{B}$: outside the overlap is the same region as outside one or outside the other. The Venn diagram and the truth table are the same statement.

In code it is the rewrite that turns `not (a and b)` into `not a or not b`, which matters when you want to short-circuit on the cheaper test first.

</details>

**9.** A system logs a warning if the temperature is above 80 *and* either the fan has failed *or* the load is above 90%. Write the condition, then its negation.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Write the condition in ordinary words first: warn when the temperature is high *and* one of two other things is true.
2. Turn that into Python, and be careful with brackets — `and` binds more tightly than `or`, so the grouping matters.
3. For the negation, apply De Morgan's law: the negation of "A and B" is "not A or not B".
4. The inner bracket needs negating too, and every comparison flips — including its boundary.

**Think about:** if you write `temperature < 80` where you should write `<=`, exactly one temperature falls through both branches. Which, and how long would that take to find?

**Try this next:** write a small loop that tests every combination of inputs against both conditions and asserts they are always opposite.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
warn = temperature > 80 and (fan_failed or load > 90)
```

The negation, by De Morgan applied twice:

```python
quiet = temperature <= 80 or (not fan_failed and load <= 90)
```

Note both flips: `and` became `or`, `or` became `and`, and every comparison inverted including the boundary. Writing `temperature < 80` there would leave exactly 80 handled by neither branch, which is the bug this kind of rewrite most often introduces.

</details>

## Data

**10.** Ten response times in milliseconds: `[12, 14, 13, 15, 14, 13, 12, 98, 14, 13]`. Summarise them, and say what you would report.

<details class="dl-answer"><summary>answer</summary>

Mean 21.8, median 13.5, mode 13 and 14 jointly, standard deviation about 25.4.

The median. One request took 98 ms and the other nine took about 13, and a reported "average response time of 22 ms" describes nothing that happened.

What you would actually report for a service is the median *and* a high percentile — the 95th here is 98, and that outlier is not noise to be discarded. It is somebody's slow request, and it is usually the number that matters.

</details>

**11.** Two exam sittings both have a mean of 60. The first has a standard deviation of 5, the second of 18. Sketch plausible histograms.

<details class="dl-answer"><summary>answer</summary>

The first is a narrow hump around 60 — nearly everyone between 50 and 70.

The second is wide, and could be one broad hump or two separate ones near 40 and 80 with almost nobody in the middle. Those two shapes have the same mean and standard deviation and mean entirely different things about the class.

That ambiguity is why the histogram is not optional.

</details>

**12.** A dataset of 1,000 values has a mean of 50 and a standard deviation of 10. Roughly how many fall between 30 and 70?

<details class="dl-answer"><summary>answer</summary>

About 950, *if* the distribution is roughly bell-shaped.

Two standard deviations either side covers about 95% of a normal distribution. One covers about 68%, three about 99.7%.

The "if" is doing a lot of work. For an arbitrary distribution the guarantee is much weaker — Chebyshev's inequality only promises at least 75% within two standard deviations, which is true for anything at all and rarely tight.

</details>

**13.** Simulate rolling two dice 10,000 times, plot the totals, and compare with the exact probabilities.

<details class="dl-answer"><summary>answer</summary>

```python
totals = Counter(random.randint(1, 6) + random.randint(1, 6) for _ in range(10000))
for total in range(2, 13):
    exact = (6 - abs(7 - total)) / 36
    print(f"{total:>3}  simulated {totals[total] / 10000:.4f}   exact {exact:.4f}")
```

A triangle peaking at 7. The formula $(6 - |7 - t|)/36$ counts the ways: one way to make 2, six to make 7, one to make 12.

With 10,000 rolls the agreement is usually to about three decimal places. With 100 it is not, and running it with both is more convincing than any explanation of sampling error.

</details>

## Putting It Together

**14.** A spam filter flags 95% of spam and wrongly flags 2% of real mail. 40% of incoming mail is spam. A message is flagged. What is the probability it is spam?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Do not start with the formula. Take a thousand messages and count what happens to them.
2. How many are spam, and how many of those get flagged?
3. How many are real, and how many of *those* get flagged anyway?
4. Of everything flagged, what fraction was actually spam?

**Think about:** compare this with the disease example, where the same-sounding accuracy gave 1%. The test did not change; the base rate did.

**Try this next:** what if only 2% of mail were spam? Work it out with counts again, and see how far the answer moves.

</details>

<details class="dl-answer"><summary>answer</summary>

About 96.9%.

Out of 1,000 messages: 400 spam, of which 380 are flagged; 600 real, of which 12 are flagged. So 380 of 392 flagged messages are spam.

Compare with the disease example in *What Are the Chances*, where the same-sounding numbers gave 1%. The difference is entirely the base rate: spam is common and the disease is rare. The test is not what decides the answer.

</details>

**15.** A quiz has 10 multiple-choice questions with 4 options each. Guessing throughout, what is the probability of getting exactly 5 right? At least 5?

<details class="dl-answer"><summary>answer</summary>

About 0.0584, and about 0.0781.

Exactly 5: $C(10,5) \times 0.25^5 \times 0.75^5$.

At least 5: sum that from 5 to 10.

The counting term $C(10,5)$ is there because there are 252 different ways to be right on five of them. That is the binomial distribution, and it is Pascal's triangle multiplied by a probability.

</details>

**16.** Three friends each pick a number from 1 to 10. What is the probability at least two pick the same?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. "At least two the same" is awkward to count directly — there are several ways it can happen.
2. Count the opposite instead: all three different.
3. The first person can pick anything. What fraction of choices keeps the second different? The third?
4. Subtract from 1.

**Think about:** this is the birthday problem with ten days in the year instead of 365. The method is identical and only the numbers change.

**Try this next:** how many people does it take for "at least two the same" to pass a half, out of 10? Out of 365?

</details>

<details class="dl-answer"><summary>answer</summary>

0.28.

All different: $\frac{10}{10} \times \frac{9}{10} \times \frac{8}{10} = 0.72$.

This is the birthday problem with ten days in the year. The same calculation with 365 and 23 people gives 50.7%, and the shape of the answer — count the ways to *avoid* it and subtract — is identical.

</details>

**17.** Two events have $P(A) = 0.6$ and $P(B) = 0.5$. What are the largest and smallest possible values of $P(A \cap B)$?

<details class="dl-answer"><summary>answer</summary>

Between 0.1 and 0.5.

The largest is when B sits entirely inside A: 0.5. The smallest is when they overlap as little as possible, and they cannot avoid each other entirely because 0.6 + 0.5 exceeds 1 — the overlap is at least 0.1.

Draw it as two circles in a box and slide them. If they were independent the overlap would be 0.30, which is one particular value in that range rather than a default.

</details>

**18.** You have a list of 10,000 email addresses with duplicates, and a list of 500 that have unsubscribed. Produce the mailing list, and say what could go wrong.

<details class="dl-answer"><summary>answer</summary>

```python
mailing = {e.strip().lower() for e in everyone} - {e.strip().lower() for e in unsubscribed}
```

A set difference, which is the operation the problem is describing.

What could go wrong: an address with different capitalisation or trailing whitespace on one list and not the other survives the subtraction and gets mailed. So does one written `name+tag@example.com` on one list and `name@example.com` on the other, and one on a domain that has since been renamed.

Normalising before comparing is the whole job, and the failure is silent — the code runs, the count looks right, and somebody who asked to be left alone gets an email.

</details>

**19.** Design a small study: does a coin you own land heads more than half the time? Say what you would measure, how many trials, and what result would convince you.

<details class="dl-answer"><summary>answer</summary>

The shape of the answer matters more than the numbers.

With n flips, the count of heads has a standard deviation of about $\frac{\sqrt{n}}{2}$. For 100 flips that is 5, so anything from 40 to 60 heads is unremarkable — a coin has to be badly wrong for 100 flips to reveal it.

For 10,000 flips the standard deviation is 50, so a genuine 51% bias would show up as about 5,100 heads, two standard deviations from fair. That is suggestive rather than conclusive.

The honest conclusion is that detecting a small bias takes far more trials than anyone expects, and that a result inside the noise is not evidence of fairness either. "No difference found" and "no difference exists" are not the same sentence.

</details>
