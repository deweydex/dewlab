---
title: "Random numbers: pseudo-random numbers and seeds"
year: "2026-2027"
version: 2026.09.22.1
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

# Random numbers: pseudo-random numbers and seeds

Every simulation in this series starts with one instruction: give me a
number I could not have predicted. Shuffling a deck, drawing lottery
numbers, simulating a queue, testing a design against a thousand
situations nobody wrote down: all of these need that one instruction.

So on this page we look at that instruction on its own, before we build
anything on top of it. We will find that the computer is not doing what
it seems to be doing. And we will find that this is useful, not
disappointing.

## Asking the Machine for a Number

Python's `random` module is part of the standard library. There is
nothing to install. We only need to import it.

```python exec
id: asking-the-machine-for-a-number-1
import random

print(random.random())
```

Run the cell a few times. What do you notice about the number each time?

Each run gives a different number between 0 and 1. It can be 0, but it
is always below 1.

That one function is enough to build almost everything else. We can
stretch a number between 0 and 1, shift it, round it or compare it, until
it has whatever shape a problem needs. The `random` module gives us the
common shapes ready-made, so we do not have to build them ourselves.

```python exec
id: asking-the-machine-for-a-number-2
import random

print("a dice roll:      ", random.randint(1, 6))
print("a number 0 to 100:", random.uniform(0, 100))
print("heads or tails:   ", random.choice(["heads", "tails"]))
```

Here are the three functions in that cell:

| Function | What it gives back |
|---|---|
| `random.randint(1, 6)` | a whole number from 1 to 6, including both 1 and 6 |
| `random.uniform(0, 100)` | a number with decimals, anywhere from 0 to 100 |
| `random.choice(["heads", "tails"])` | one item from the list |

### Your turn

How might you simulate rolling two dice and adding them?
`random.randint(1, 6)` gives one die, and you need the total of two.

```python exec
id: asking-the-machine-for-a-number-3
hint: Call randint twice and add the results. Storing each roll in its own variable makes the total easier to read afterwards.
```

## The Same Numbers Twice

The next cell does something that looks like a mistake.

It builds a list of five dice rolls with a list comprehension, which we
met in [Comprehensions, grids and aliasing](tutorial:comprehensions-and-grids).
The loop variable is called `_`. Python programmers use the name `_` for
a loop variable the loop never uses. Here the loop only needs to run five
times.

```python exec
id: the-same-numbers-twice-1
import random

random.seed(42)
print([random.randint(1, 6) for _ in range(5)])
```

Run the cell again. And again. What happens?

You get the same five numbers every time. If you change the `42` to
another whole number, you get a different five. But those five also
repeat every time you run the cell.

### Your turn

1. Before you read on, what do you think `random.seed(42)` is doing?
   Think about what you have just seen.
2. Can you find a seed that makes the first roll a 1?

```python exec
id: the-same-numbers-twice-2
hint: Try a few seeds in a loop. For each one, set the seed, then print the seed and its first roll. Stop when you see a 1.
```

Here is what is happening. The numbers were never random.
`random.random()` runs an algorithm: an ordinary piece of arithmetic
that gives the same result every time it starts from the same place.
The algorithm takes its current internal state and mixes it up very
thoroughly. Then it returns a number made from the result.

The mixing is good enough to pass the tests we would use on real
randomness. Nobody can find a pattern in the numbers. Every value is
equally likely. And one number tells you nothing about the next.

But it is still a calculation. A calculation that starts from the same
place gives the same answer. The *seed* is that starting place, and
`random.seed(42)` sets it by hand. If we do not set a seed, Python gets
one from the operating system. That is why the numbers usually look
different on each run.

Numbers made this way are called *pseudo-random*. A pseudo-random number
comes from a calculation, but it is so close to random that no test we
use can tell the difference.

## What Random Is Good Enough For

Your first thought might be that pseudo-random is second-best, and that
we only use it because true randomness is hard to get. In one field that
is true, as we will see below. For simulation, it is almost the opposite.

Think about what you did to find a seed that gives a 1. You ran an
experiment, and you can run it again and get the same result.

Now imagine that a simulation, like the one in
[Simulating a queue: stable and unstable queues](tutorial:when-a-queue-never-clears),
gives a strange result, such as a queue that never clears. You want to
know why. With truly random numbers, that run is gone forever. You cannot
repeat it, step through it, or show it to anyone else. With a seed, you
write down one whole number, and the whole run comes back exactly.

An experiment that nobody can run again is not much of an experiment.
Being able to repeat a run exactly is called *reproducibility*, and it is
why careful simulation code always sets a seed and writes it down.

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

Three numbers are easy to check by eye. Two thousand are not, so the
next cell shows the same idea as a picture. It rolls a die 2,000 times,
and after each roll it works out the average of all the rolls so far. It
does this three times: with seed 7, with seed 7 again, and with seed 8.
Before you run it, what do you expect the two seed 7 lines to look like?

```python exec
id: what-random-is-good-enough-for-3
import random
import matplotlib.pyplot as plt

def running_mean(seed, rolls):
    """The average roll so far, after each of `rolls` dice."""
    random.seed(seed)
    total = 0
    averages = []
    for count in range(1, rolls + 1):
        total = total + random.randint(1, 6)
        averages.append(total / count)
    return averages

rolls = 2000
plt.plot(running_mean(7, rolls), linewidth=1.6, label="seed 7")
plt.plot(running_mean(7, rolls), linewidth=1.6, linestyle="--",
         label="seed 7, again")
plt.plot(running_mean(8, rolls), linewidth=0.9, label="seed 8")
plt.axhline(3.5, color="grey", linestyle=":", label="3.5")
plt.ylim(2.5, 4.5)
plt.xlabel("dice rolled")
plt.ylabel("average so far")
plt.legend()
```

There are three runs on the chart, but you can only see two paths. The
two seed 7 runs lie exactly on top of each other, for all 2,000 rolls.
The dashes are the only way to tell that the second one is there at all.
The same seed gives the same dice, every time.

Seed 8 takes a different path. It is not a better or worse run. It is
only another run, and it settles towards the same average of 3.5 as the
others. The seed decides which path you get. It does not decide where
the path ends up.

There is one field where pseudo-random really is second-best: security.
If an attacker can find your seed, they can work out every "random"
number you will ever make. For a login code or a password reset link,
that is a complete failure. Python's `secrets` module is the tool for
that job. For simulation, nobody is trying to guess your dice. So
`random` is the right choice, and reproducibility is the reason.

### Your turn

Can you show that a seed repeats a run?

1. Call `random.seed(7)`, then print five random numbers.
2. Call `random.seed(7)` again, then print five more.
3. Check that the two lists match.

```python exec
id: what-random-is-good-enough-for-2
```

## Choosing From a List

The rest of this series uses one more tool. Often we do not want a
number. We want a thing: a customer, a word, a country, a row of data.

```python exec
id: choosing-from-a-list-1
import random
random.seed(0)

weather = ["sunny", "cloudy", "rain"]

print("one day: ", random.choice(weather))
print("a week:  ", [random.choice(weather) for _ in range(7)])
```

`random.choice` picks one item, and every item is equally likely. It has
two close relatives, `random.choices` and `random.sample`. People often
mix them up. Look at the two lines this cell prints. Can you spot a card
that appears twice?

```python exec
id: choosing-from-a-list-2
import random
random.seed(3)

deck = ["A", "K", "Q", "J", "10"]

print("with replacement:   ", random.choices(deck, k=4))
print("without replacement:", random.sample(deck, k=4))
```

`random.choices`, with an **s**, puts each card back before it draws the
next one. This is called drawing *with replacement*, and the same card
can come up twice. Here the K came up twice.

`random.sample` does not put the card back. This is drawing *without
replacement*, so no card can come up twice.

| Function | Puts each item back? | Can repeat? | Example |
|---|---|---|---|
| `random.choices(items, k=4)` | yes | yes | rolling a die four times |
| `random.sample(items, k=4)` | no | no | dealing a hand of cards |

Rolling a die four times is `choices`, because a die has no memory of
what it showed last time.

### Your turn

You want to draw five names out of a hat for a prize draw, and nobody can
win twice.

1. Which of the two functions would you use?
2. Write the draw.
3. Check that no name appears more than once.

```python exec
id: choosing-from-a-list-3
hint: Ask yourself whether a name goes back into the hat after it is drawn. To check for repeats, compare len(drawn) with len(set(drawn)). A set keeps only one copy of each item.
names = ["Aoife", "Brendan", "Ciara", "Dara", "Eimear", "Fionn", "Gráinne"]
```

## Reflection

The word *random* has a narrower meaning now than it had at the start of
this page. It no longer means "impossible to predict". It means
"impossible to predict for anyone who does not know the seed". It also
means "regular enough that the difference never shows up in the answer".

When you first saw the numbers repeat, did it feel like a
disappointment? Or did the reason make sense before you read the
explanation? Both reactions are common. If it was the second, trust that
feeling. You could build the whole argument for reproducibility yourself,
from one afternoon spent chasing a bug.

Where else have you met something that is not exactly what it claims to
be, but is so close that the difference never matters? Computing has many
examples like this. Noticing them is a large part of understanding a
system, and not only using it.

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

Veritasium (2014). *What is NOT Random?*
<https://www.youtube.com/watch?v=sMb00lz-IfE>. Is anything truly random,
or would it all be predictable if we knew enough? Veritasium asks
physicists. Ten minutes.
