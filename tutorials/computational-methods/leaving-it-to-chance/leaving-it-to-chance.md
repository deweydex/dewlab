---
title: "Leaving It to Chance"
slug: leaving-it-to-chance
module: computational-methods
module_title: "Computational Methods"
year: "2026-2027"
series: simulation
version: 2026.08.30.1
covers:
  asking-the-machine-for-a-number:
    covers: [CMPS-LO2]
  the-same-numbers-twice:
    covers: [CMPS-LO2]
  what-random-is-good-enough-for:
    covers: [CMPS-LO2]
    touches: [CMPS-LO3]
  choosing-from-a-list:
    covers: [CMPS-LO2]
---

# Leaving It to Chance

Everything in this series is built on one instruction: give me a number I
could not have predicted. Shuffling a deck, picking a lottery draw,
simulating a queue, testing a design against a thousand scenarios nobody
wrote down — all of it starts there.

So it is worth spending one tutorial on that instruction alone, before
building anything on top of it. Partly because it is the foundation, and
partly because the machine is not doing what it appears to be doing, and the
gap between those two things turns out to be useful rather than
disappointing.

## Asking the Machine for a Number

Python's `random` module is part of the standard library — nothing to
install, and it is already there.

```python exec
id: asking-the-machine-for-a-number-1
import random

print(random.random())
```

Run that a few times. Each click gives a different number, somewhere between
0 and 1.

That one function is enough to build almost everything else. A number between
0 and 1 can be stretched, shifted, rounded or compared into whatever shape a
problem needs — and `random` provides the common shapes directly so you do
not have to.

```python exec
id: asking-the-machine-for-a-number-2
import random

print("a dice roll:      ", random.randint(1, 6))
print("a number 0 to 100:", random.uniform(0, 100))
print("heads or tails:   ", random.choice(["heads", "tails"]))
```

### Your turn

How might you simulate rolling two dice and adding them? `random.randint(1, 6)`
gives one die; you need the total of two.

```python exec
id: asking-the-machine-for-a-number-3
hint: Call randint twice and add the results. Storing each roll in its own variable makes the total easier to read afterwards.
```

## The Same Numbers Twice

Now something that looks like a mistake.

```python exec
id: the-same-numbers-twice-1
import random

random.seed(42)
print([random.randint(1, 6) for _ in range(5)])
```

Run that cell again. And again.

The same five numbers, every time. Change the `42` to any other whole number
and you get a different five — but those five will then repeat just as
stubbornly.

### Your turn

Before reading on: what do you think `random.seed(42)` is doing, given what
you have just watched? And can you find a seed that makes the first roll a 6?

```python exec
id: the-same-numbers-twice-2
hint: Try a few seeds in a loop, printing the seed and its first roll, and stop when you see a 6.
```

Here is what is happening. The numbers were never random. `random.random()`
runs an algorithm — an entirely ordinary, deterministic piece of arithmetic —
that takes its current internal state, scrambles it thoroughly, and returns a
number derived from the result. The scrambling is good enough that the output
passes the statistical tests we would apply to genuine randomness: no
detectable pattern, every value equally likely, no correlation between one
number and the next.

But it is a calculation, and a calculation given the same starting point
produces the same answer. `random.seed(42)` sets that starting point by hand.
Without it, Python picks one from the system clock and some operating-system
entropy, which is why the numbers usually look different each run.

Numbers produced this way are called *pseudo-random*: not random, but
indistinguishable from random by any test that matters for our purposes.

## What Random Is Good Enough For

The obvious reaction is that pseudo-random is a compromise, a second-best
because true randomness is hard to come by. For one field that is exactly
right, and for ours it is almost the reverse.

Think about what you just did to find a seed giving a 6. You ran an
experiment, and you could run it again and get the same result. Now imagine
the simulation in tutorial 4 of this series produces a bizarre result — a
queue that never clears — and you want to know why. With genuinely random
numbers, that specific run is gone forever. You cannot reproduce it, cannot
step through it, cannot show it to anyone else. With a seed, you write down
one integer and the entire run comes back exactly.

An experiment nobody can re-run is not much of an experiment. Reproducibility
is why every serious piece of simulation code sets a seed and records it.

```python exec
id: what-random-is-good-enough-for-1
import random

def one_experiment(seed):
    """Roll three dice under a stated seed, so the run can be repeated."""
    random.seed(seed)
    return [random.randint(1, 6) for _ in range(3)]

for seed in [1, 2, 3]:
    print(f"seed {seed}: {one_experiment(seed)}")

print("seed 2, again:", one_experiment(2))
```

The one place this genuinely is a compromise is security. If an attacker can
work out your seed, they can produce every "random" number you will ever
generate — which for a session token or a password reset link is a complete
failure. That is what Python's `secrets` module is for, and it is a different
tool for a different job. For simulation, where nobody is trying to predict
your dice, `random` is the right choice and reproducibility is the reason.

### Your turn

Can you show the difference directly? Write a cell that calls
`random.seed(7)` and prints five numbers, then calls `random.seed(7)` again
and prints five more — and satisfy yourself that the two lists match.

```python exec
id: what-random-is-good-enough-for-2
```

## Choosing From a List

One more tool, because the rest of the series leans on it. Often what you
want is not a number but a *thing*: a customer, a word, a country, a row of
data.

```python exec
id: choosing-from-a-list-1
import random
random.seed(0)

weather = ["sunny", "cloudy", "rain"]

print("one day: ", random.choice(weather))
print("a week:  ", [random.choice(weather) for _ in range(7)])
```

`random.choice` picks one, with every item equally likely. Two neighbours are
worth knowing, and the difference between them is the thing people get wrong:

```python exec
id: choosing-from-a-list-2
import random
random.seed(0)

deck = ["A", "K", "Q", "J", "10"]

print("with replacement:   ", random.choices(deck, k=4))
print("without replacement:", random.sample(deck, k=4))
```

`random.choices` — note the **s** — puts each card back before drawing the
next, so the same card can come up twice. `random.sample` does not, so it
cannot. Dealing a hand of cards is `sample`. Rolling a die four times is
`choices`, because a die has no memory of what it just showed.

### Your turn

Which of the two would you use to simulate drawing five names out of a hat
for a prize draw, where nobody can win twice? Write it, and check that no
name appears more than once.

```python exec
id: choosing-from-a-list-3
hint: Ask yourself whether a name goes back into the hat after it is drawn. Comparing len(drawn) with len(set(drawn)) is one way to confirm there are no repeats.
names = ["Aoife", "Brendan", "Ciara", "Dara", "Eimear", "Fionn", "Gráinne"]
```

## Reflection

The word *random* did a lot of work in this tutorial, and by the end it meant
something narrower than it did at the start: not unpredictable in principle,
but unpredictable to anyone not holding the seed, and statistically
well-behaved enough that the difference does not show up in the answer.

Was the discovery that the numbers repeat a disappointment when you first ran
that cell, or did the reason for it land before the explanation did? Both are
common, and the second is worth trusting — the argument for reproducibility
is one you can reconstruct yourself from a single afternoon of debugging.

Where else have you met something that is technically not what it claims to
be, but close enough that the difference never surfaces? Computing is
unusually full of these, and noticing them is most of what it means to
understand a system rather than only use it.

## Where to Read More

Python Software Foundation. *`random` — Generate pseudo-random numbers.*
<https://docs.python.org/3/library/random.html>. The module's own
documentation, and unusually readable for a standard-library page — the
opening note on which functions are and are not suitable for security is
worth the visit on its own.

Python Software Foundation. *`secrets` — Generate secure random numbers for
managing secrets.* <https://docs.python.org/3/library/secrets.html>. The
other half of the story, for the cases where being predictable is a
vulnerability rather than a feature.

Downey, A. B. (2015). *Think Python* (2nd ed.). O'Reilly. Chapter 13 builds a
word-frequency study on `random` and is a good next step if the "choose a
thing, not a number" half of this tutorial was the interesting part.

Matsumoto, M. and Nishimura, T. (1998). *Mersenne Twister: A 623-dimensionally
equidistributed uniform pseudo-random number generator.* ACM Transactions on
Modeling and Computer Simulation, 8(1), 3–30.
<https://doi.org/10.1145/272991.272995>. The algorithm behind Python's own
generator. Considerably heavier than anything in this series, and included
because "an algorithm produces the sequence" is a claim you are entitled to
go and check.
