---
title: "Chances that combine: and, or, and the birthday problem — Practice"
practice_for: chances-that-combine
year: "2026-2027"
version: 2026.09.25.1
---

# Chances that combine: and, or, and the birthday problem — Practice

Each problem says what kind it is. **Predict** means guess first, then
run. **Make** means write something new. **Fix** means find why code
that looks fine does something else, and change it. **Explain** means answer in words. **Another
way** means reach the same place by a second route. The answers are
folded away until you open them, and each shows one way through: yours
may be different, and work as well.

Your toolkit is loaded on this page, `at_least_one` included, along with
`all_pairs`, `product`, `combinations` and `simulate` from earlier in
the unit.

## Warm-up

Use this cell for any of the warm-up problems.

```python exec
id: chances-practice-warm-up
print(0.5 * 0.5)
```

**1. Predict.** Two captains toss a coin before a match, and then toss
again before extra time. What is the chance that both tosses are heads?
Say it as a fraction, then run the cell above to see it as a decimal.

<details class="dl-answer"><summary>answer</summary>

$\frac{1}{4}$, which is `0.25`.

The two tosses are independent: a coin does not remember. So the
multiplication rule gives $\frac{1}{2} \times \frac{1}{2} = \frac{1}{4}$.
Listing them gives the same: heads-heads, heads-tails, tails-heads and
tails-tails, and only one of the four is two heads.

</details>

**2. Explain.** Which of these pairs of events are independent? Say why
for each one.

- a. Rain in Galway today, and rain in Galway tomorrow.
- b. Your numbers coming up in this week's Lotto draw, and in next
  week's.
- c. Drawing a king from a deck of cards, then drawing a second card
  without putting the first one back, and that one being a king too.

<details class="dl-answer"><summary>answer</summary>

- a. Not independent. Weather comes in spells, so a wet day makes a wet
  day tomorrow more likely.
- b. Independent. Each draw starts with every ball back in the drum, so
  last week's draw cannot change this week's.
- c. Not independent. After one king is gone, 3 kings are left in 51
  cards, not 4 in 52. The first draw changes the second.

A useful question for each one: does the first event change what is
left, or what is likely, for the second?

</details>

**3. Make.** A web server is up and working on 85% of days. Write one
line that works out the chance it is down on a given day. What does Python
print, and why is it not exactly `0.15`?

<details class="dl-answer"><summary>answer</summary>

```python
print(1 - 0.85)
```

It prints `0.15000000000000002`. Down is the complement of up, so the
chance is $1 - 0.85 = 0.15$. (A real server that was down on 15% of days
would lose its customers quickly. Real ones aim for 99.9% and more.)

The tiny extra at the end is the float rounding from
[Everything is ones and zeros](tutorial:everything-is-ones-and-zeros):
0.85 has no exact binary form, so Python holds a number very close to
it. The answer is right to about 16 digits.

</details>

**4. Predict.** What does this print? Work it out by hand first, with
the complement.

```python
print(at_least_one(0.5, 3))
```

<details class="dl-answer"><summary>answer</summary>

`0.875`.

This is the chance of at least one head in three coin tosses. The only
way to get no head is tails three times: $\left(\frac{1}{2}\right)^3 =
\frac{1}{8}$. So at least one head is $1 - \frac{1}{8} = \frac{7}{8} =
0.875$.

</details>

## Core

A scratch cell for the core problems. It brings in the `random` module
for the problems that simulate.

```python exec
id: chances-practice-core
import random

# Try things here
```

**5. Make.** An online game needs two players' phones to be online at
the same minute. The first player's phone is online 40% of the time,
and the second's 50% of the time, and the two have nothing to do with
each other. What is the chance that both are online? Work it out with
the multiplication rule, then check it with `simulate`.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The phones have nothing to do with each other, so the two events
   are independent.
2. Multiply the two chances.
3. For the simulation, `random.randint(1, 10) <= 4` is True 4 times in
   10, the same as a 40% chance.

**Think about:** what would change if the two players were friends
who always play at the same time of day?

**Try this next:** what is the chance that at least one of the two is
offline?

</details>

<details class="dl-answer"><summary>answer</summary>

$0.4 \times 0.5 = 0.2$.

```python
import random

def both_online():
    """One minute. True when both phones are online."""
    first = random.randint(1, 10) <= 4
    second = random.randint(1, 10) <= 5
    return first and second

print(0.4 * 0.5)
print(simulate(both_online, 100000))
```

The simulation gives a number near 0.2, a little different each time
you run it.

</details>

**6. Predict.** One card is drawn from a deck of 52. What is the chance
that it is a heart or a king? Predict the answer with a rule, then run
the cell, which lists the whole deck and counts.

```python exec
id: chances-practice-cards
ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
suits = ["hearts", "diamonds", "clubs", "spades"]
deck = all_pairs(ranks, suits)

count = 0
for rank, suit in deck:
    if suit == "hearts" or rank == "K":
        count = count + 1
print(count, "of", len(deck))
```

<details class="dl-answer"><summary>answer</summary>

16 of 52, which is about 0.308.

A heart and a king are not mutually exclusive, because the king of
hearts is both. There are 13 hearts and 4 kings, and 1 card is in both
groups. So

$$\frac{13}{52} + \frac{4}{52} - \frac{1}{52} = \frac{16}{52}$$

If you predicted $\frac{17}{52}$, the king of hearts was counted twice.
The overlap rule is there to catch that.

</details>

**7. Fix.** A weather app works out the chance of at least one wet day in
a week, when each day has a 30% chance of rain. It says 0.9998, which
seems far too sure. Find why, and change it.

```python exec
id: chances-practice-fix-rain
def chance_of_a_wet_day(chance_of_rain, days):
    """The chance of at least one wet day in this many days."""
    return 1 - chance_of_rain ** days

print(chance_of_a_wet_day(0.3, 7))
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. "At least one wet day" is the complement of which event?
2. What is the chance that one day is dry?
3. What should be raised to the power `days`: the chance of rain, or
   the chance of no rain?

**Think about:** what `0.3 ** 7` means in words.

</details>

<details class="dl-answer"><summary>answer</summary>

The code raises the chance of rain to the power 7. That is the chance
that it rains on every day, not the chance that it never rains. The
complement of "at least one wet day" is "every day is dry", and a dry
day has chance $1 - 0.3 = 0.7$:

```python
def chance_of_a_wet_day(chance_of_rain, days):
    """The chance of at least one wet day in this many days."""
    return 1 - (1 - chance_of_rain) ** days

print(chance_of_a_wet_day(0.3, 7))
```

Now it prints about `0.918`, the same as `at_least_one(0.3, 7)`. Nothing
crashed before the fix. The number looked like a chance, and it was
between 0 and 1. Only a sense of what the answer should be caught it.

</details>

**8. Another way.** The Chevalier de Méré's bet was at least one six in
four rolls of a die. The page found $1 - \left(\frac{5}{6}\right)^4$.
Find the same answer a second way: loop over every possible set of four
rolls, and count the ones with a six in them.

```python exec
id: chances-practice-four-rolls
# Four loops, one inside another, and a count
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. One loop for each roll, each over `range(1, 7)`.
2. Inside all four, check whether any of the four rolls is 6, with `or`.
3. Count the outcomes, and the ones with a six. How many outcomes should
   there be in all?

**Think about:** which is quicker to count, the outcomes with a six, or
the outcomes with none?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
outcomes = 0
with_a_six = 0
for first in range(1, 7):
    for second in range(1, 7):
        for third in range(1, 7):
            for fourth in range(1, 7):
                outcomes = outcomes + 1
                if first == 6 or second == 6 or third == 6 or fourth == 6:
                    with_a_six = with_a_six + 1

print(with_a_six, "of", outcomes)
print(with_a_six / outcomes)
print(1 - (5 / 6) ** 4)
```

It prints `671 of 1296`, then `0.5177...` twice. There are $6^4 = 1296$
outcomes, and $5^4 = 625$ of them have no six, so $1296 - 625 = 671$
have at least one. The loop lists every case, and the formula is the
fast way to the same count.

</details>

**9. Make.** The Chevalier had a second bet: at least one double six in
24 rolls of two dice. The story says he reasoned that $24 \times \frac{1}{36} =
\frac{2}{3}$, so he should win. Work out the real chance with
`at_least_one`. Should he have taken the bet?

<details class="dl-answer"><summary>answer</summary>

```python
print(at_least_one(1 / 36, 24))
```

It prints about `0.491`. That is a little less than a half, so over many
games this bet loses slightly more often than it wins. He should not
have taken it.

His reasoning added chances, but 24 rolls are not mutually exclusive:
two of them can both be double sixes. The complement gets it right: no
double six in 24 rolls is $\left(\frac{35}{36}\right)^{24}$. The story
goes that he asked the mathematician Blaise Pascal why he was losing
money, and that letters between Pascal and Pierre de Fermat in 1654
about this kind of question helped start probability as a branch of maths.

</details>

**10. Make.** A GAA club raffle sells 20 tickets, and you have bought 3.
Two prizes are drawn, and a drawn ticket is not put back. Work out:

- a. the chance that you win both prizes;
- b. the chance that you win at least one prize.

Check both by listing every possible draw, with `all_pairs` and a loop
that leaves out pairs where the same ticket is drawn twice.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. For a: the first draw is yours with chance $\frac{3}{20}$. After
   that, how many of your tickets are left, and how many tickets in all?
2. For b: the complement of "at least one" is "none". Work out the
   chance that neither draw is yours, in the same way.
3. For the listing: number the tickets 1 to 20, and say yours are 1, 2
   and 3.

**Think about:** why the second fraction in each part has 19 at the
bottom.

</details>

<details class="dl-answer"><summary>answer</summary>

a. $\frac{3}{20} \times \frac{2}{19} = \frac{6}{380} \approx 0.0158$.

b. Neither draw is yours with chance
$\frac{17}{20} \times \frac{16}{19} \approx 0.716$, so at least one is
yours with chance about $1 - 0.716 = 0.284$.

```python
tickets = range(1, 21)
mine = [1, 2, 3]

draws = []
for first, second in all_pairs(tickets, tickets):
    if first != second:
        draws.append((first, second))

both = 0
at_least_one_prize = 0
for first, second in draws:
    if first in mine and second in mine:
        both = both + 1
    if first in mine or second in mine:
        at_least_one_prize = at_least_one_prize + 1

print(len(draws), both / len(draws), at_least_one_prize / len(draws))
```

It prints `380`, then about `0.0158` and `0.284`. There are
$20 \times 19 = 380$ possible draws, which is `permutations(20, 2)`.

</details>

**11. Explain.** For part b of problem 10, Schlomi, who is learning
Python too, uses `at_least_one(3 / 20, 2)` and gets about 0.2775, not
0.284. Which answer fits this raffle, and why do the two differ?

<details class="dl-answer"><summary>answer</summary>

The listing fits this raffle: about 0.284.

`at_least_one` keeps its promise only when the tries are
independent. The raffle draws are not. A ticket that has been drawn is
not put back, so the first draw changes the second. If the first draw
is not yours, one of the 17 tickets that are not yours has gone, and
your chance on the second draw goes up to $\frac{3}{19}$.

Schlomi's answer would fit a raffle where each drawn ticket
goes back in the drum before the next draw. Her move is fine; it
belongs to a different space.

</details>

## Stretch

A scratch cell for the stretch problems.

```python exec
id: chances-practice-stretch
# Try things here
```

**12. Make.** A program keeps names in 12 boxes, called buckets. It
works out a short code from each name, a hash, and the code chooses the
bucket. Suppose each name is equally likely to land in any of the 12.
How many names must go in before the chance that two share a bucket is
more than a half? Use a `while` loop and `product`.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. This is the birthday problem with a "year" of 12 days.
2. For `names` names, the chance that all buckets are different is
   the product of $\frac{12 - k}{12}$ for $k$ from 0 to `names - 1`.
3. Start at `names = 1`, and keep adding one name while the chance of a
   shared bucket is 0.5 or less.

**Think about:** what the answer would be with 365 in place of 12.

**Try this next:** how many people for a chance of more than 0.9?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def chance_of_shared_bucket(names):
    """The chance that two of this many names land in the same bucket."""
    chances = []
    for already in range(names):
        chances.append((12 - already) / 12)
    return 1 - product(chances)

names = 1
while chance_of_shared_bucket(names) <= 0.5:
    names = names + 1

print(names, chance_of_shared_bucket(names))
```

It prints `5` and about `0.618`. With 4 names the chance is about
0.427, so 5 is the first count where a shared bucket is more likely
than not. With 365 in place of 12, the same loop stops at 23. A shared
bucket does not break the program: it keeps a short list in each
bucket. But the birthday problem says the programmer should plan for
it from the start.

</details>

**13. Another way.** Here is a birthday problem small enough to list
every case. A "year" has 4 days, and there are 3 people. Find the chance
that two of them share a day twice: once with the complement and
`product`, and once with three loops that list every case.

<details class="dl-answer"><summary>answer</summary>

With the complement: all different is
$\frac{4}{4} \times \frac{3}{4} \times \frac{2}{4} = \frac{24}{64}$, so
a shared day has chance $1 - \frac{24}{64} = \frac{40}{64} = 0.625$.

```python
print(1 - product([4 / 4, 3 / 4, 2 / 4]))

outcomes = 0
shared = 0
for first in range(1, 5):
    for second in range(1, 5):
        for third in range(1, 5):
            outcomes = outcomes + 1
            if first == second or first == third or second == third:
                shared = shared + 1
print(shared, "of", outcomes, "=", shared / outcomes)
```

It prints `0.625`, then `40 of 64 = 0.625`. The listing is the proof,
and the product is the fast way. For 23 people and 365 days, the listing
would have $365^{23}$ rows, a number with 59 digits, so the
fast way is the only way.

</details>

**14. Fix.** Schlomo, who is learning Python too, wrote this version of
`shared_birthday`. It says that even 2 people share a birthday every
single time. Run it, find why, and change it.

```python exec
id: chances-practice-fix-birthday
import random

def shared_birthday(people):
    """Give this many people random birthdays. True when two share one."""
    seen = []
    for person in range(people):
        day = random.randint(1, 365)
        seen.append(day)
        if day in seen:
            return True
    return False

def room_of_2():
    return shared_birthday(2)

print(simulate(room_of_2, 1000))
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Follow the loop for the first person, line by line.
2. After `seen.append(day)`, is `day in seen` True or False?
3. What order should the two steps be in?

**Think about:** which of the four questions this is about.

</details>

<details class="dl-answer"><summary>answer</summary>

The two steps are in the wrong order. The day is added to `seen` first,
so the check `day in seen` always finds it, even for the first person.
The function returns True straight away, every time. Check first, then
add:

```python
def shared_birthday(people):
    """Give this many people random birthdays. True when two share one."""
    seen = []
    for person in range(people):
        day = random.randint(1, 365)
        if day in seen:
            return True
        seen.append(day)
    return False

print(simulate(room_of_2, 100000))
```

Now it prints a number near $\frac{1}{365} \approx 0.0027$. The
problem was about sequence: what happens when. Both lines did their
jobs, and only their order had to change.

</details>

**15. Explain.** On the tutorial page, `at_least_one(0.3, 7)` gave about
0.918 for at least one wet day in a week, "if the days were independent".
Real weather comes in spells: a dry day is often followed by another
dry day. Do you expect the true chance of at least one wet day to be
higher or lower than 0.918? Why?

<details class="dl-answer"><summary>answer</summary>

Lower.

The only way to have no wet day is a whole dry week. With independent
days, that needs seven separate pieces of luck, each with chance 0.7,
and $0.7^7$ is only about 0.08. When dry days come in spells, one dry
day makes the next one more likely, so a whole dry week is more likely
than 0.08. The complement, at least one wet day, is then less likely
than 0.918.

The formula is not wrong. It answers the question for a space where the
days are independent. Real weather is a different space, and the first
step is to notice that.

</details>

**16. Explain.** This page opened with the birthday problem, a
question where most people's guess misses. Picture teaching a friend who
is sure they are "bad at maths". Would you open with a question where
their guess will probably miss, or one where it will probably land? What
could go wrong with each choice?

<details class="dl-answer"><summary>answer</summary>

Here is one way through. It weighs a few things.

- **A question where the guess misses.** The surprise makes people want
  to know why, and it shows that a feeling about chance can be checked.
  What can go wrong: to someone who expects to fail, a missed guess can
  look like more proof. It helps to say that most people guess the same way,
  and that the guess is not marked.
- **A question where the guess lands.** It builds confidence, and it gives
  the friend a first success. What can go wrong: if the point of the
  lesson is a surprise, starting safely can make the surprise feel like
  a trick later.

What makes a missed guess safe is how it is treated: nobody marks it, and
the answer is used to find out which way the guess leaned. Whichever
question you chose, say what you would do to make it safe.

</details>
