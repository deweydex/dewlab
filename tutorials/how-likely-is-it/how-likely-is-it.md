---
title: "How likely is it? Probability and simulation"
year: "2026-2027"
version: 2026.09.24.1
covers:
  a-scale-from-0-to-1:
    covers: [MIT-5.6]
  counting-equally-likely-outcomes:
    covers: [MIT-5.7]
    touches: [MIT-5.1, MIT-5.2]
  letting-python-toss-the-coin:
    touches: [MIT-5.6, PDP-LO4]
  a-tool-that-runs-it-many-times:
    covers: [MIT-5.6]
    touches: [PDP-LO6, PDP-LO8]
  why-the-two-answers-differ:
    covers: [MIT-5.6]
  seven-heads-in-ten:
    covers: [MIT-5.7]
    touches: [MIT-5.5]
---

# How likely is it? Probability and simulation

A friend tosses a coin ten times and gets seven heads. "This coin is
not fair," they say. Are they right? Or could an ordinary coin do that
too?

To answer, we need to say how likely something is, with a number. By
the end of this page we will have that number, found in two different
ways, and we will see why the two ways agree only nearly.

On this page we:

- put chances on a scale from 0 to 1
- work out a chance by counting outcomes that are equally likely
- let Python toss coins and roll dice, with the `random` module
- add `simulate` to the toolkit: it runs a chance experiment many times,
  and counts
- see why a simulation and the exact answer differ a little, and how
  more runs bring them closer
- answer the question about the coin, two ways

> **The space we're in.** A fair coin and a fair die, where every
> outcome is equally likely. That is an assumption about the world, and
> maths cannot prove it for a real coin. Real coins come very close, and
> we agree to treat them as fair. Python gives us random numbers once we
> `import random`. Your toolkit gives us `all_pairs`, `total` and
> `combinations` from the pages before this one.

## Warm-up

The first question is from
[Orders and choices](tutorial:orders-and-choices), and the second from
[Counting every outfit: lists of outcomes](tutorial:counting-every-outfit).

```question
id: likely-warm-up-1
type: fill-in-the-blank

A band has 5 songs ready and will play 2 of them as an encore. The order
does not matter to us, so there are `combinations(5, 2)`, which is {10},
possible encores.
```

```question
id: likely-warm-up-2
type: multiple-choice
correct: 3

You roll a red die and a blue die. How many different outcomes are
there, if red 2 and blue 5 is different from red 5 and blue 2?

- 12
- 21
- 36
- 66
```

## A scale from 0 to 1

People talk about chance all the time. "It will probably rain." "No
chance." "It's fifty-fifty." Maths puts these on one scale.

The *probability* of something is a number from 0 to 1 that says how
likely it is. A probability of 0 means *impossible*: it will never
happen. A probability of 1 means *certain*: it will always happen. In
between, a bigger number means more likely. An even chance, like heads
on a fair coin, is $\frac{1}{2}$, or 0.5.

The same number can be written three ways. When Met Éireann gives a 70%
chance of rain in Galway, that is the probability 0.7, or
$\frac{7}{10}$. A percentage is the probability multiplied by 100.

We write the probability of an event A as $P(A)$. So
$P(\text{heads}) = 0.5$. A probability can never be less than 0 or more
than 1:

$$0 \le P(A) \le 1$$

That is a rule of this space. If a calculation ever gives a probability
of 1.3, or −0.2, something has gone wrong, in the same way a count of
−2 people would be wrong.

```question
id: likely-scale-1
type: multiple-choice
correct: 2

You roll an ordinary die once. Which of these has probability 0?

- You roll a number less than 7.
- You roll a 7.
- You roll an even number.
- You roll a 6.
```

## Counting equally likely outcomes

On [Counting every outfit](tutorial:counting-every-outfit#outcomes-of-an-experiment)
we met an experiment, like rolling a die, and its outcomes, like
rolling a 4. The sample space was the list of every outcome. We need one
more word. An *event* is a group of outcomes we care about: "rolling an
even number" is the event made of the outcomes 2, 4 and 6.

When every outcome is equally likely, a probability is a count:

$$P(\text{event}) = \frac{\text{number of outcomes in the event}}{\text{number of outcomes in all}}$$

In words: count the outcomes you want, and divide by all the outcomes.
For an even number on one die, that is $\frac{3}{6} = 0.5$.

Now two dice, as in many board games. What is the chance that the two
add up to 7? Your toolkit's `all_pairs` lists all 36 outcomes, and a loop counts the ones we want. Guess first: is 7 more
likely than, say, 12?

```python exec
id: likely-dice-1
faces = [1, 2, 3, 4, 5, 6]
outcomes = all_pairs(faces, faces)

sevens = 0
for red, blue in outcomes:
    if red + blue == 7:
        sevens = sevens + 1

print(sevens, "of", len(outcomes))
print(sevens / len(outcomes))
```

The line `for red, blue in outcomes:` takes each pair apart as the
loop goes round: `red` points at the pair's first value, and `blue` at
its second.

Six of the 36 outcomes add up to 7: 1 and 6, 2 and 5, and so on, up to
6 and 1. So $P(\text{7}) = \frac{6}{36} = \frac{1}{6}$, about 0.167.
Only one outcome, 6 and 6, adds up to 12, so $P(12) = \frac{1}{36}$.

This is why "each outcome equally likely" matters. The sums 2 to 12 are
not equally likely, so we cannot say $P(7) = \frac{1}{11}$. The pairs
are equally likely, so we count pairs.

### Your turn

1. Change the cell so that it counts the outcomes where the two dice
   show the same number: a double. Guess the answer first.
2. Change it again to count sums of 10 or more.
3. Write each answer as a fraction, a decimal and a percentage.

## Letting Python toss the coin

Counting works when we can list every outcome. Often we cannot, or the
list is too long. Then there is another way: do the experiment many
times, and see how often the event happens. A computer can toss a coin
a million times without getting bored.

Python keeps its random tools in a module called `random`. A module, as
[Numbers a computer can hold](tutorial:numbers-a-computer-can-hold#powers-and-how-many-times)
said, is a collection of extra tools that Python keeps on the shelf
until we `import` it. Three of its tools are enough for this page:

- `random.choice(values)` picks one value from a list, each equally
  likely.
- `random.randint(1, 6)` picks a whole number from 1 to 6, with both
  ends included, the way a die does.
- `random.random()` gives a decimal from 0 up to, but not including, 1.

What will this cell print? You cannot know in advance, and that is the
point. Run it three or four times.

```python exec
id: likely-toss-1
import random

print(random.choice(["heads", "tails"]))
print(random.randint(1, 6))
print(random.random())
```

Each run gives different results. The numbers come from a formula
inside Python, so they are not truly random. They are *pseudo-random*:
made by a formula, but mixed so well that they behave like a fair coin
for everything on this page. The page
[Random numbers: pseudo-random numbers and seeds](tutorial:leaving-it-to-chance)
says more about how they are made.

Now 1,000 tosses. How many heads do you expect? Exactly 500? Run the
cell a few times, and watch the count.

```python exec
id: likely-toss-2
heads = 0
for toss in range(1000):
    if random.choice(["heads", "tails"]) == "heads":
        heads = heads + 1

print(heads, "heads in 1000 tosses")
print(heads / 1000)
```

The count is close to 500, and it is rarely exactly 500. The fraction
of tosses that came up heads is the *relative frequency*: how often the
event happened, divided by how many times we tried. Probability from
counting is exact. Relative frequency comes from trying, and it changes
a little every time.

## A tool that runs it many times

We will want to run many different experiments many times. So let's
make one tool that does it for any experiment.

The experiment itself becomes a function with no inputs, which we call
a *trial*. It returns True when the event happens, and False when it
does not. Here are two:

```python exec
id: likely-trial-1
def heads():
    """Toss a fair coin once. True for heads."""
    return random.choice(["heads", "tails"]) == "heads"


def roll_six():
    """Roll a fair die once. True for a 6."""
    return random.randint(1, 6) == 6


print(heads(), roll_six())
```

On [True, false and every case](tutorial:true-false-and-every-case) we
handed a rule to `truth_table` without brackets after its name. We do
the same here: `simulate(heads, 1000)` hands over the trial `heads`
itself, so that `simulate` can call it 1,000 times.

A *simulation* is a program that acts out an experiment many times, to
see what usually happens. Here is the promise of `simulate`, as a
docstring. Write its body: a loop that calls `trial()` `times` times,
counts the True results, and returns the fraction.

```python exec
id: likely-toolkit
toolkit: yes
def simulate(trial, times):
    """Run trial() the given number of times, and return the fraction of
    runs where it gave True.

    trial is a function with no inputs that returns True or False.
    times is a whole number, 1 or more. The result is from 0 to 1.
    """
    ...
```

```python toolkit-reference
for: likely-toolkit
def simulate(trial, times):
    """Run trial() the given number of times, and return the fraction of
    runs where it gave True.

    trial is a function with no inputs that returns True or False.
    times is a whole number, 1 or more. The result is from 0 to 1.
    """
    successes = 0
    for run in range(times):
        if trial():
            successes = successes + 1
    return successes / times
```

Testing something random needs care, because we cannot know its exact
answer. So the first two tests use trials whose answers are fixed. The
last test checks that 10,000 fair tosses give heads between 45% and
55% of the time, with `between` from
[Choosing a path](tutorial:choosing-a-path). A fair coin lands outside
that range far less often than once in a billion billion tries. Until
your `simulate` is written, this cell stops with an error.

```python exec
id: likely-toolkit-tests
def always():
    return True


def never():
    return False


assert simulate(always, 50) == 1
assert simulate(never, 50) == 0
assert between(simulate(heads, 10000), 0.45, 0.55)
print("simulate keeps its promise.")
```

```hint
What does `print(simulate(always, 50))` show? If it shows `None`, the
function has no `return` yet. If it shows 50, check what you divide by.
```

## Why the two answers differ

Counting says $P(\text{heads}) = 0.5$ exactly. A simulation says
something near 0.5. Which one is right?

Both are, and they answer different questions. Counting tells us what
the coin would do on average, over ever more tosses. A simulation tells
us what happened in these tosses. Every toss is left to chance, so a
simulation can land a little above or below the exact answer, and it
lands somewhere different every run.

What happens as the runs grow? Before you run the cell, guess: which
row will be furthest from 0.5? This cell, and the ones after it that
call `simulate`, need your `simulate` from the last section. Until it is
written, this cell stops with a `TypeError`, because a function with no
`return` gives back `None`.

```python exec
id: likely-differ-1
for times in [10, 100, 1000, 10000, 100000]:
    fraction = simulate(heads, times)
    print(times, "runs:", fraction, " off by", round(abs(fraction - 0.5), 4))
```

`abs()` gives the size of a number without its sign, so it tells us how
far off each fraction is, above or below. Run the cell a few times. The
10-run row jumps about: 0.3 one time, 0.7 the next. The 100,000-run row
hardly moves from 0.5.

This pattern has a name. The *law of large numbers* says that as an
experiment is repeated more times, its relative frequency tends to get
closer to the probability. It does not promise to hit it exactly, and a
few more runs can make it worse for a while. What it promises is that
the wobble gets smaller. As a rough guide, 100 times as many runs make
the wobble about 10 times smaller.

A picture shows the same thing. The chart below tosses one coin 2,000
times and plots the fraction of heads so far, after every toss. We
learn to draw charts properly in a later unit. For now, `plt.plot`
draws the line, and `plt.axhline` draws the flat line at 0.5.

```python exec
id: likely-differ-2
import matplotlib.pyplot as plt

heads_so_far = 0
fractions = []
for toss in range(1, 2001):
    if heads():
        heads_so_far = heads_so_far + 1
    fractions.append(heads_so_far / toss)

plt.plot(range(1, 2001), fractions)
plt.axhline(0.5, color="grey", linestyle="--")
plt.xlabel("tosses so far")
plt.ylabel("fraction of heads")
```

At the left, after a handful of tosses, the line swings a long way. By
the right-hand side it has settled close to the dashed line. Run it
again, and you get a different line that settles the same way.

So when a simulation disagrees with the exact answer a little, nothing
is broken. When it disagrees a lot, look for a mistake: in the trial, in
the counting, or in the assumption that every outcome is equally
likely.

## Seven heads in ten

Now back to the friend's coin. The question to ask is this: if the coin
*is* fair, how often would ten tosses give 7 heads or more? If a fair
coin does that often, seven heads is no evidence against it.

We ask about "7 or more", not "exactly 7", because 8, 9 or 10 heads
would have made the friend even more suspicious.

First, the simulation. One trial is ten tosses, and it returns True when
7 or more of them are heads. Guess first: about how often do you think
a fair coin does this?

```python exec
id: likely-seven-1
def seven_or_more():
    """Toss a fair coin 10 times. True when 7 or more are heads."""
    heads_count = 0
    for toss in range(10):
        if heads():
            heads_count = heads_count + 1
    return heads_count >= 7


print(simulate(seven_or_more, 10000))
```

Near 0.17. Now the exact answer, by counting. Ten tosses have
$2^{10} = 1024$ outcomes, each one a row of heads and tails, and each
equally likely. How many rows have exactly 7 heads? That is the number
of ways to choose which 7 of the 10 tosses are the heads:
$C(10, 7)$, from [Orders and choices](tutorial:orders-and-choices).

```python exec
id: likely-seven-2
ways = [combinations(10, 7), combinations(10, 8),
        combinations(10, 9), combinations(10, 10)]
print(ways)
print(total(ways), "of", 2 ** 10)
print(total(ways) / 2 ** 10)
```

$120 + 45 + 10 + 1 = 176$ of the 1,024 rows have 7 heads or more, so
the probability is $\frac{176}{1024} = 0.171875$. Your simulation was
close to that, and a little off, as the last section said it would be.

So a fair coin gives 7 heads or more in about 1 test in 6. That happens
often enough that seven heads is no real evidence of an unfair coin.
Your friend's claim is not foolish, but ten tosses are too few to show
it.

What about 70 heads in 100 tosses? It is the same fraction, 70%. Guess
before you run: is it about as likely as 7 in 10?

```python exec
id: likely-seven-3
ways = []
for heads_count in range(70, 101):
    ways.append(combinations(100, heads_count))
print(total(ways) / 2 ** 100)
```

Python writes the answer as `3.925069822796835e-05`. The `e-05` at the
end means "times $10^{-5}$": move the decimal point five places to the
left, to get 0.0000392…. So it is about 0.00004, or 4 in 100,000. A fair coin almost never does
that. More tosses give the same wobble less room, just as the law of
large numbers said. With 100 tosses, 70 heads would be strong evidence
that something about the coin is not fair.

### Your turn

1. Change `seven_or_more` so that it returns True when there are 8 heads
   or more. Guess the new probability first.
2. Run the simulation, and then change the counting cell to check it
   exactly.
3. Try the simulation with 1,000 runs and then 100,000 runs. Which one
   is closer to the exact answer?

## Four questions, looking back

| The question | On this page |
|---|---|
| What is named here? | probability, $P(A)$; an event, a group of outcomes; each trial, such as `heads` and `seven_or_more`; your toolkit function `simulate` |
| What is promised? | $P(A)$ is from 0 to 1; with equally likely outcomes, $P$ is a count divided by a count; `simulate` promises the fraction of runs that gave True |
| What happens when? | each run of a trial is new and left to chance; a simulation's answer settles as the runs grow |
| What does this space let us do? | fair coins and dice, where every outcome is equally likely; `random` once we import it; numbers that are pseudo-random, and good enough |

## What we have now

| Term or tool | What it means |
|---|---|
| probability, $P(A)$ | a number from 0 (impossible) to 1 (certain) for how likely A is |
| event | a group of outcomes we care about, such as "an even number" |
| equally likely outcomes | $P(\text{event})$ = outcomes in the event ÷ all outcomes |
| `random.choice`, `random.randint`, `random.random` | pick from a list; a whole number in a range; a decimal from 0 to 1 |
| pseudo-random | made by a formula, but behaving like chance |
| relative frequency | how often an event happened ÷ how many times we tried |
| simulation, trial | a program that acts out an experiment many times; one run of it |
| law of large numbers | more runs bring the relative frequency closer to the probability |
| `abs()` | the size of a number, without its sign |
| `simulate(trial, times)` | your new toolkit function |

The next page, [Chances that combine](tutorial:chances-that-combine),
asks what happens when two chances meet, and why two people in a class
share a birthday more often than you would think.

For another route through the same ideas, the integrated course has
[Probability: simple, compound and conditional](tutorial:what-are-the-chances).
