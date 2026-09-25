---
title: "Chances that combine: and, or, and the birthday problem"
year: "2026-2027"
version: 2026.09.25.1
covers:
  two-sixes-at-once:
    covers: [MIT-5.8]
    touches: [MIT-5.1, MIT-5.7]
  when-one-changes-the-other:
    covers: [MIT-5.8]
    touches: [MIT-5.4]
  one-or-the-other:
    covers: [MIT-5.8]
  when-both-can-happen:
    covers: [MIT-5.8]
    touches: [MIT-2.4]
  not-and-at-least-once:
    covers: [MIT-5.8]
  a-tool-for-at-least-once:
    touches: [MIT-5.8, PDP-LO8]
  the-birthday-problem:
    covers: [MIT-5.8]
    touches: [MIT-5.5, MIT-6.4, PDP-LO6]
---

# Chances that combine: and, or, and the birthday problem

There are 23 people in a room. How likely is it that two of them share
a birthday? Make a guess now, as a percentage, and keep it in mind.
Many people guess something small, like 5% or 10%. Most people do not
believe the real answer the first time they see it. By the end of this
page we will know it three ways, and why it matters inside every
computer that stores files.

On this page we:

- find the chance that both of two things happen, or either one
- see what changes when one changes the chance of the other
- turn "at least once" round into "not even once", with `at_least_one`
- solve the birthday problem three ways, then meet it in computer codes

> **The space we're in.** Every chance is a number from 0 to 1, as on
> [How likely is it?](tutorial:how-likely-is-it), and dice and coins are
> fair. For birthdays we assume 365 days, each one equally likely, and
> leave out 29 February. Real birthdays are not quite that even. We use
> Python's `random` module, and `simulate`, `product`, `all_pairs` and
> `combinations` from your toolkit.

## Warm-up

Two questions from [How likely is it?](tutorial:how-likely-is-it) and
[Orders and choices](tutorial:orders-and-choices).

```question
id: chances-warm-up-1
type: fill-in-the-blank

A fair die has six faces, and three of them are even. The chance of
rolling an even number is {1/2|1/3|1/6}.
```

```question
id: chances-warm-up-2
type: multiple-choice
correct: 2

Two of four friends will play the first game of table tennis. How many
different pairs could play first? The order of the two does not matter.

- 4
- 6
- 12
- 16
```

## Two sixes at once

In some board games you need a six to bring a piece onto the board. A
stricter house rule asks for two sixes at once, on two dice. How likely
is that?

Three guesses people often make are $\frac{1}{6}$, $\frac{2}{6}$ and
$\frac{1}{12}$. Which is right, or is it none of them?

We do not have to argue about it. On
[Counting every outfit](tutorial:counting-every-outfit) we listed every
outcome with `all_pairs`. How many outcomes do you expect, and how many
are two sixes?

```python exec
id: chances-dice-1
faces = [1, 2, 3, 4, 5, 6]
outcomes = all_pairs(faces, faces)
print(len(outcomes), "outcomes")

both_six = 0
for first, second in outcomes:
    if first == 6 and second == 6:
        both_six = both_six + 1
print("two sixes:", both_six)
```

There are 36 outcomes, all equally likely, and only one is two sixes.
So the chance is $\frac{1}{36}$. None of the three guesses was right.

Draw the 36 outcomes as a grid, with a row for each roll of the first
die and a column for the second. A six on the first die is one row out
of 6. Inside that row, a six on the second die is one square out of 6.
So two sixes is $\frac{1}{6}$ of $\frac{1}{6}$ of the grid, and "of"
means multiply:

$$\frac{1}{6} \times \frac{1}{6} = \frac{1}{36}$$

Two events are *independent* when one happening does not change the
chance of the other. Dice and coins have no memory, so each roll is
independent of the last. For independent events, the chance that both
happen is the two chances multiplied. This is the *multiplication
rule*. With $P(A)$ for the probability of A, it is

$$P(A \text{ and } B) = P(A) \times P(B)$$

Now let's check it with `simulate`. `random.randint(1, 6)` gives a
whole number from 1 to 6, each one equally likely. Will the last two
lines match the first exactly?

```python exec
id: chances-dice-2
import random

def two_sixes():
    """Roll two dice once. True when both show 6."""
    return random.randint(1, 6) == 6 and random.randint(1, 6) == 6

print("exact:          ", 1 / 36)
print("1,000 games:    ", simulate(two_sixes, 1000))
print("100,000 games:  ", simulate(two_sixes, 100000))
```

The exact answer is about 0.0278. The simulated answers are close, and
change each time you run the cell. That is the law of large numbers from
[How likely is it?](tutorial:how-likely-is-it#why-the-two-answers-differ):
the more games, the smaller the wobble.

### Your turn

A game starts with a coin toss and a roll of a die. You win a prize for
heads and a six.

1. Use the multiplication rule to work out the chance, before you run
   anything.
2. The cell below lists every outcome. Add a loop that counts the ones
   that are heads and a six.
3. Does your count, divided by the number of outcomes, match step 1?

```python exec
id: chances-dice-your-turn
coin = ["heads", "tails"]
outcomes = all_pairs(coin, faces)
print(len(outcomes), "outcomes")
```

## When one changes the other

A playlist has 10 songs, and 2 of them are your favourites. You press
shuffle. What is the chance that the first two songs are both
favourites?

That depends on the shuffle. Some players pick every song from all 10,
so a song can play twice in a row. Others play each song only once.
Which kind of shuffle do you think gives the better chance?

The songs are numbered 1 to 10, and songs 1 and 2 are the favourites.
One new move is in this cell: `first in favourites` is True when
`first` is one of the values in the list `favourites`.

```python exec
id: chances-playlist-1
songs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
favourites = [1, 2]

def chance_both_favourites(pairs):
    """The fraction of pairs where both songs are favourites."""
    count = 0
    for first, second in pairs:
        if first in favourites and second in favourites:
            count = count + 1
    return count / len(pairs)
```

With repeats, every pair from `all_pairs` can happen. With no repeats,
we keep only the pairs of two different songs.

```python exec
id: chances-playlist-2
with_repeats = all_pairs(songs, songs)

no_repeats = []
for first, second in with_repeats:
    if first != second:
        no_repeats.append((first, second))

print(len(with_repeats), chance_both_favourites(with_repeats))
print(len(no_repeats), chance_both_favourites(no_repeats))
```

With repeats, there are 100 pairs, and the chance is 0.04:
$\frac{2}{10} \times \frac{2}{10}$, the multiplication rule.

With no repeats, there are 90 pairs, `permutations(10, 2)` from
[Orders and choices](tutorial:orders-and-choices), and the chance is
about 0.022. Here the first song changes the chance for the second. Once
a favourite has played, only 1 favourite is left, out of 9 songs:

$$\frac{2}{10} \times \frac{1}{9} = \frac{2}{90} \approx 0.022$$

We still multiply, but the second number is the chance after the
first song, because these events are not independent.

<aside class="dl-note" id="chances-note-shuffle">

**A shuffle that is less random on purpose.** In 2014, the music app
Spotify wrote that it had stopped using a purely random shuffle. Its
listeners complained that songs by one artist came up close together
too often, which real chance does. The new shuffle spreads each
artist's songs out, because that feels more random to people.

</aside>

Before you multiply two chances, ask which space you are in: does the
first one change the second?

## One or the other

A message crosses a network in small pieces called *packets*. Over a
bad Wi-Fi link, 20 of the last 100 packets were lost, and 10 arrived
damaged, so we take those chances as 0.2 and 0.1. What is the chance
that a packet does not arrive whole?

A packet cannot be lost and arrive damaged at the same time. Two events
are *mutually exclusive* when they cannot both happen at once. Then the
chance that one or the other happens is the two chances added. This is
the *addition rule*:

$$P(A \text{ or } B) = P(A) + P(B)$$

So the chance a packet does not arrive whole is $0.2 + 0.1 = 0.3$. This
is "and multiplies, or adds" from
[Counting every outfit](tutorial:counting-every-outfit#and-multiplies-or-adds),
and it needs the same care: the two groups must not overlap.

```question
id: chances-or-1
type: multiple-choice
correct: 2

One fair die is rolled. What is the chance that it shows a 1 or a 2?

- $\frac{1}{36}$, because $\frac{1}{6} \times \frac{1}{6}$
- $\frac{2}{6}$, because $\frac{1}{6} + \frac{1}{6}$
- $\frac{1}{6}$, because it is one roll
```

A die cannot show 1 and 2 at once, so the addition rule works:
$\frac{2}{6}$, which is $\frac{1}{3}$.

## When both can happen

A board game gives you a bonus when you roll an even number or a number
more than 4. What is the chance of a bonus?

Three of the six faces are even, and two are more than 4. The addition
rule would say $\frac{3}{6} + \frac{2}{6} = \frac{5}{6}$. Does that feel
right? Let's count. How many faces do you expect to give a bonus?

```python exec
id: chances-both-1
bonus_faces = 0
for roll in range(1, 7):
    if roll % 2 == 0 or roll > 4:
        bonus_faces = bonus_faces + 1

print(bonus_faces, "of 6 faces give a bonus")
print("adding the two chances:", 3 / 6 + 2 / 6)
print("counting the faces:    ", bonus_faces / 6)
```

Four faces give a bonus: 2, 4, 5 and 6. Adding gave five, because the 6
was counted twice: it is even, and it is more than 4. These events are
not mutually exclusive. To count the 6 only once, we take away the
chance that both happen:

$$P(A \text{ or } B) = P(A) + P(B) - P(A \text{ and } B)$$

Here that is $\frac{3}{6} + \frac{2}{6} - \frac{1}{6} = \frac{4}{6}$,
which matches the count.

This is the `or` from
[True, false and every case](tutorial:true-false-and-every-case): True
when at least one input is True, including when both are. For mutually
exclusive events the overlap is empty, so the addition rule is this
rule with nothing taken away.

## Not, and at least once

Back to the packets. The chance one arrives whole is $1 - 0.3 = 0.7$.
The *complement* of an event is everything that can happen except that
event. The two chances add up to 1, so

$$P(\text{not } A) = 1 - P(A)$$

The complement is very useful for questions with "at least" in them. A
story is told about the Chevalier de Méré, a French gambler of the
1650s. He liked to bet that he would roll at least one six in four rolls
of a die, and reasoned like this: one roll gives a six with chance
$\frac{1}{6}$, so four rolls give $4 \times \frac{1}{6} = \frac{2}{3}$.

Is he right? Here is a warning sign: with seven rolls, his reasoning
gives $\frac{7}{6}$, and no chance can be more than 1. Two rolls can
both be sixes, so adding is the wrong move.

So let's turn the question round. The only way to lose the bet is to
roll no six at all. Each roll misses with chance $\frac{5}{6}$, and the
rolls are independent, so

$$P(\text{no six in four rolls}) = \left(\frac{5}{6}\right)^4
\qquad
P(\text{at least one six}) = 1 - \left(\frac{5}{6}\right)^4$$

Which do you expect to be closer to the simulation: the gambler's
$\frac{2}{3}$, or the complement? Inside `six_in_four`, `return True`
stops the function as soon as one six appears.

```python exec
id: chances-not-1
import random

def six_in_four():
    """Roll a die four times. True when at least one roll is a 6."""
    for roll in range(4):
        if random.randint(1, 6) == 6:
            return True
    return False

print("the gambler:", 4 * (1 / 6))
print("complement: ", 1 - (5 / 6) ** 4)
print("simulate:   ", simulate(six_in_four, 100000))
```

The complement gives about 0.518, and the simulation agrees. The bet
wins a little more often than it loses, so in the story the gambler did
well, but far less often than his $\frac{2}{3}$.

In general, for $n$ independent tries that each succeed with chance
$p$,

$$P(\text{at least one in } n \text{ tries}) = 1 - (1 - p)^n$$

## A tool for at least once

We will use that formula again, so let's make it a toolkit function.
Fill in the two lines with `...`, then run the cell.

```python exec
id: chances-toolkit
toolkit: yes
def at_least_one(chance, tries):
    """Return the chance that something happens at least once.

    chance is its probability on one try, from 0 to 1. tries is how
    many tries there are. The tries must be independent: one try must
    not change the chance of another.
    """
    never = ...  # the chance it fails on every one of the tries
    return ...
```

```python toolkit-reference
for: chances-toolkit
def at_least_one(chance, tries):
    """Return the chance that something happens at least once.

    chance is its probability on one try, from 0 to 1. tries is how
    many tries there are. The tries must be independent: one try must
    not change the chance of another.
    """
    never = (1 - chance) ** tries
    return 1 - never
```

Until your stub is filled in, the tests stop with an error. The last
test uses `round`, because a float is very close to the true value, and
seldom equal to it.

```python exec
id: chances-toolkit-tests
assert at_least_one(0.5, 1) == 0.5
assert at_least_one(0, 10) == 0
assert at_least_one(1, 3) == 1
assert round(at_least_one(1 / 6, 4), 4) == 0.5177
print("at_least_one keeps its promise.")
```

```hint
Which test does the error point at? Try `print(at_least_one(0.5, 1))`
on its own. What did you expect it to give?
```

```hint
after: 10 errors
title: some steps
1. On one try, the chance of failing is `1 - chance`.
2. The tries are independent, so failing on every one of them is that
   chance multiplied by itself `tries` times: a power.
3. At least once is the complement of never.

**Think about:** why `at_least_one(0, 10)` should be 0, and why
`at_least_one(1, 3)` should be 1.
```

### Your turn

1. A forecast gives a 30% chance of rain on each day of a week's holiday
   in Kerry. If the days were independent, what is the chance of at
   least one wet day? Use `at_least_one`.
2. A message gets through on 75% of tries. If a phone tries twice,
   what is the chance at least one try works?
3. How many rolls of a die do you need before the chance of at least one
   six is more than 0.9? Try different numbers, or write a `while` loop
   that adds one try until the chance passes 0.9.

```python exec
id: chances-toolkit-your-turn
print(at_least_one(0.3, 7))
```

## The birthday problem

Now we have every tool for the question at the top of the page.

### Way one: simulate it

To simulate one room, we give each person a random day from 1 to 365,
and keep the days seen so far in a list. If a new day is already in the
list, two people share it. Look back at your guess from the top of the
page. Do you still believe it?

```python exec
id: chances-birthday-1
import random

def shared_birthday(people):
    """Give this many people random birthdays. True when two share one."""
    seen = []
    for person in range(people):
        day = random.randint(1, 365)
        if day in seen:
            return True
        seen.append(day)
    return False

def room_of_23():
    return shared_birthday(23)

print(simulate(room_of_23, 10000))
```

The answer is about 0.5. In a room of 23 people, two share a birthday
about half the time. That is a strange result, isn't it?

### Way two: count it exactly

Let's use the complement again: the opposite of "two share" is "all 23
are different". The first person can have any day: $\frac{365}{365}$.
The second must miss that day: $\frac{364}{365}$. The third must miss
two days: $\frac{363}{365}$. Each person changes the chance for the
next one, as the favourite songs did. The 23rd person must miss 22 days:
$\frac{343}{365}$.

All 23 must happen, so we multiply. On
[Doing it again](tutorial:doing-it-again) we wrote a product with
$\prod$:

$$P(\text{all different}) = \prod_{k=0}^{22} \frac{365 - k}{365}$$

Here $k$ is the number of people already in the room. The cell hands
the list to your toolkit's `product`. What do you expect?

```python exec
id: chances-birthday-2
chances = []
for already in range(23):
    chances.append((365 - already) / 365)

all_different = product(chances)
print("all different:     ", all_different)
print("two share a day:   ", 1 - all_different)
```

The exact answer is about 0.507, a little more than a half. The
simulation was right.

### Way three: think about pairs

Why is it so high? The usual guess asks: "does anyone share my
birthday?" With 22 others in the room, that is
`at_least_one(1 / 365, 22)`, about 0.06. But any two people can share a
birthday, and a room of 23 has a lot of pairs. How many? `combinations`
from [Orders and choices](tutorial:orders-and-choices) counts them.

```python exec
id: chances-birthday-3
pairs = combinations(23, 2)
print(pairs, "pairs")
print(at_least_one(1 / 365, pairs))
```

There are 253 pairs, and each shares a birthday with chance
$\frac{1}{365}$. So `at_least_one` says about 0.5005: close to the exact
0.5073, but not the same. Why? Its promise needs independent tries, and
these pairs are not quite independent. If Ann shares a birthday with
Ben, and Ben shares with Cara, then Ann must share with Cara too. The
pairs are nearly independent, so the tool is a good guide, but the exact
answer came from the product.

### A picture of every room size

What happens to the chance as the room grows? The grey line marks a
chance of one half. Where do you expect the curve to cross it?

```python exec
id: chances-birthday-4
import matplotlib.pyplot as plt

def chance_of_shared(people):
    """The exact chance of a shared birthday among this many people."""
    chances = []
    for already in range(people):
        chances.append((365 - already) / 365)
    return 1 - product(chances)

sizes = []
results = []
for people in range(1, 61):
    sizes.append(people)
    results.append(chance_of_shared(people))

plt.plot(sizes, results)
plt.axhline(0.5, color="grey")
plt.xlabel("people in the room")
plt.ylabel("chance two share a birthday")
```

The curve crosses one half between 22 and 23 people. By 60 people it is
very close to 1. Very few people guess that shape before they see it.

### Your turn

1. Print `chance_of_shared(23)`, and check it matches way two.
2. Find the smallest room where the chance is more than 0.9. Then find
   the smallest where it is more than 0.99.
3. What is the chance for your own class? If two people in it share a
   birthday, that is not as strange as it seemed.

```python exec
id: chances-birthday-your-turn
print(chance_of_shared(23))
```

### Birthdays inside a computer

Programs often give each file a short code worked out from its
contents, called a hash, so that two files can be compared by their
codes. Two different files with the same code are a collision. A
file's code is like a birthday, and a 32-bit hash has $2^{32}$ possible
codes, about 4.3 billion. How many files before two of them probably
share a code? A million? A billion? Guess, then run it.

```python exec
id: chances-hash-1
codes = 2 ** 32
files = 77000
pairs = combinations(files, 2)
print(pairs, "pairs of files")
print(at_least_one(1 / codes, pairs))
```

About 77,000 files are enough for an even chance, out of more than four
billion codes, because 77,000 files make almost three billion pairs.
Security people call using this a *birthday attack*, and it is why the
hashes used to check downloads today, such as SHA-256, are 256 bits
long. [Maths that runs the world](tutorial:maths-that-runs-the-world)
tells more of this story.

<details class="dl-why"><summary>Why this way?</summary>

Most pages in this course open with a question people tend to get
right, because a first success matters, most of all to someone who
expects to fail. This one opened with a question most people get far
too low. The way chances combine is hard to believe until your own guess
has been wrong, and a wrong guess shows which way your sense of chance
leans. Your guess was never marked.

</details>

## Four questions, looking back

| Question | On this page |
|---|---|
| What is named here? | Events got names, $A$ and $B$, and $P(A)$ named each one's chance. Each game became a trial, like `two_sixes`. |
| What is promised? | Each rule promises a chance. `at_least_one` keeps its promise only when the tries are independent. |
| What happens when? | Whether an earlier event changes a later one decides the rule. In the birthday count, each person changes the chance for the next. |
| What does this space let us do? | Multiplying belongs to independent events, and adding to mutually exclusive ones. Asking which space we are in comes first. |

## What we have now

| Term or tool | What it means |
|---|---|
| independent events | One does not change the chance of the other |
| multiplication rule | For independent events, $P(A \text{ and } B) = P(A) \times P(B)$ |
| mutually exclusive events | They cannot both happen at once |
| addition rule | For mutually exclusive events, $P(A \text{ or } B) = P(A) + P(B)$ |
| or, with an overlap | $P(A \text{ or } B) = P(A) + P(B) - P(A \text{ and } B)$ |
| complement | Everything except the event: $P(\text{not } A) = 1 - P(A)$ |
| at least once | $1 - (1 - p)^n$, for $n$ independent tries |
| `x in values` | True when `x` is in the list |
| the birthday problem | In a room of 23, two share a birthday about half the time |
| `at_least_one(chance, tries)` | Your toolkit function for "at least once" |

The practice page is next. After it,
[Mixed problems: loops, counting and chance](tutorial:mixed-loops-counting-and-chance)
uses the whole unit to build a password-strength checker.

For another route through the same ideas, the integrated course has
[Probability: simple, compound and conditional](tutorial:what-are-the-chances).
