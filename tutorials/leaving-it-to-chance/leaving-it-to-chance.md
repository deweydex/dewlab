---
title: "Random numbers: pseudo-random numbers and seeds"
year: "2026-2027"
version: 2026.09.27.1
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
worlds:
  living-systems: A diver's survey of the fish on a coral reef.
  queues-and-crowds: The orders at a busy café.
  spread: A rumour, passed from person to person.
  space-and-physics: A speck of dust, knocked left and right at random.
---

# Random numbers: pseudo-random numbers and seeds

Every simulation in this series starts with one instruction: give me a
number I could not have predicted. Shuffling a deck, drawing lottery
numbers, simulating a queue and testing a design against a thousand
situations nobody wrote down all need that one instruction.

So on this page we look at that instruction on its own, before we build
anything on top of it. We will find that the computer is not doing what
it seems to be doing. And we will find that this is useful, not
disappointing.

## Asking the machine for a number

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

| Function | What it returns |
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

## The same numbers twice

The next cell does something that looks like a mistake.

It builds a list of five dice rolls with a list comprehension, which we
met in [Comprehensions, grids and
aliasing](tutorial:comprehensions-and-grids). The loop variable is
called `_`. Python programmers use the name `_` for a loop variable the
loop never uses. Here the loop only needs to run five times.

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

## What random is good enough for

Your first thought might be that pseudo-random is second-best, and that
we only use it because true randomness is hard to get. In one field that
is true, as we will see below. For simulation, it is almost the opposite.

Think about what you did to find a seed that gives a 1. You ran an
experiment, and you can run it again and get the same result.

Now imagine that a simulation, like the one in [Simulating a queue: how
busy is too busy?](tutorial:when-a-queue-never-clears), gives a strange
result, such as a queue that never clears. You want to know why. With
truly random numbers, that run is gone forever. You cannot repeat it,
step through it, or show it to anyone else. With a seed, you write down
one whole number, and the whole run comes back exactly.

Scientists need to be able to run an experiment again and check it.
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
and after each roll it calculates the average of all the rolls so far. It
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
the path finishes.

There is one field where pseudo-random really is second-best: security.
If an attacker can find your seed, they can calculate every "random"
number you will ever make. For a login code or a password reset link,
that is a complete failure. Python's `secrets` module is the tool for
that job. For simulation, nobody is trying to guess your dice. So
`random` is the right choice, because it gives reproducibility.

### Your turn

Can you show that a seed repeats a run?

1. Call `random.seed(7)`, then print five random numbers.
2. Call `random.seed(7)` again, then print five more.
3. Check that the two lists match.

```python exec
id: what-random-is-good-enough-for-2
```

## Choosing from a list

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
can appear twice. Here the K appeared twice.

`random.sample` does not put the card back. This is drawing *without
replacement*, so no card can appear twice.

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

## Your world

Every task below sets its own seed inside the function, as
`one_experiment` did. So the same call always gives the same answer,
and a classmate can check yours.

<div class="dl-world" data-world="living-systems">

A diver swims along a reef and notes each fish on the way. On this
reef, 60% of the fish are damselfish, 30% are wrasse and 10% are
parrotfish. Can you write `survey(fish, seed)`? It sets the seed, uses
`random.choices` with those weights to make a list of `fish` sightings,
and returns how many were parrotfish.

```python exec
id: your-world-1--living-systems
import random


def survey(fish, seed):
    """How many parrotfish, in a survey of this many fish."""
    # Your code here.
```

```hint
`random.choices(["damselfish", "wrasse", "parrotfish"], weights=[60, 30,
10], k=fish)` draws the sightings, with replacement. `.count("parrotfish")`
counts one kind in the list.
```

```inputs
survey(20, 1)
survey(20, 2)
survey(2000, 1)
```

```solution
import random


def survey(fish, seed):
    """How many parrotfish, in a survey of this many fish."""
    random.seed(seed)
    seen = random.choices(["damselfish", "wrasse", "parrotfish"], weights=[60, 30, 10], k=fish)
    return seen.count("parrotfish")
---
In 20 fish, seed 1 sees 2 parrotfish and seed 2 sees 4: one survey
says 10% and the other 20%. In 2,000 fish, seed 1 sees 198, very close
to 10%. A short survey can be far out, by luck alone. `choices`, with
replacement, is right here: seeing one parrotfish does not make the
next one less likely.
```

</div>

<div class="dl-world" data-world="queues-and-crowds">

At a busy café, half of the customers order coffee, 30% order tea and
20% order hot chocolate. Can you write `orders(customers, seed)`? It
sets the seed, uses `random.choices` with those weights, and returns a
dictionary of how many of each drink were ordered.

```python exec
id: your-world-1--queues-and-crowds
import random


def orders(customers, seed):
    """How many of each drink, for this many customers."""
    # Your code here.
```

```hint
`random.choices(["coffee", "tea", "hot chocolate"], weights=[5, 3, 2],
k=customers)` makes the list of orders. Then count each drink with
`.count()`, and put the counts in a dictionary.
```

```inputs
orders(30, 1)
orders(30, 2)
orders(1000, 1)["coffee"]
```

```solution
import random


def orders(customers, seed):
    """How many of each drink, for this many customers."""
    random.seed(seed)
    drinks = random.choices(["coffee", "tea", "hot chocolate"], weights=[5, 3, 2], k=customers)
    return {drink: drinks.count(drink) for drink in ["coffee", "tea", "hot chocolate"]}
---
With seed 1, 19 of 30 customers order coffee; with seed 2, only 15. A
café that ordered its milk from one morning's count could be well out.
Over 1,000 customers, 473 order coffee, close to half. The weights `[5,
3, 2]` work like the counts in a chain: 5 parts in 10 is a half.
```

</div>

<div class="dl-world" data-world="spread">

One person knows a rumour. Every day, each person who knows it tells
one other person, chosen at random from everyone, who may know it
already. Can you write `days_to_spread(people, seed)`? It sets the
seed, and returns how many days pass before everyone knows.

```python exec
id: your-world-1--spread
import random


def days_to_spread(people, seed):
    """Days until all of `people` know the rumour, starting from person 0."""
    # Your code here.
```

```hint
Keep a set of the people who know, starting with `{0}`. Each day, make
a list with one `random.choice(range(people))` for each person who
knows, and add them all to the set. Count the days until the set has
`people` in it.
```

```inputs
days_to_spread(30, 1)
days_to_spread(30, 2)
days_to_spread(300, 1)
```

```solution
import random


def days_to_spread(people, seed):
    """Days until all of `people` know the rumour, starting from person 0."""
    random.seed(seed)
    knows = {0}
    days = 0
    while len(knows) < people:
        told = [random.choice(range(people)) for _ in knows]
        knows.update(told)
        days += 1
    return days
---
A class of 30 all know in 9 days with seed 1, and 11 with seed 2. A
school of 300 all know in 14 days: ten times the people, and only five
more days. The number who know roughly doubles each day at first,
because everyone who knows is telling someone. Try 3,000.
```

</div>

<div class="dl-world" data-world="space-and-physics">

A speck of dust in the air is knocked by molecules from every side. In
this simple model it moves along a line, one step left or one step
right, chosen at random each time. Can you write `walk(steps, seed)`? It
sets the seed and returns where the speck finishes, counting from 0.

```python exec
id: your-world-1--space-and-physics
import random


def walk(steps, seed):
    """Where the speck ends, after this many random steps of -1 or +1."""
    # Your code here.
```

```hint
Start at `position = 0`. Each step, add `random.choice([-1, 1])`.
```

```inputs
walk(100, 1)
walk(100, 2)
walk(10000, 1)
```

```solution
import random


def walk(steps, seed):
    """Where the speck ends, after this many random steps of -1 or +1."""
    random.seed(seed)
    position = 0
    for _ in range(steps):
        position += random.choice([-1, 1])
    return position
---
After 100 steps, seed 1 ends at 8 and seed 2 back at 0. After 10,000
steps, seed 1 is at -110. The speck does not go anywhere on purpose,
but it wanders further the longer it runs: about 10 steps from the
start after 100 steps, and about 100 after 10,000. That is the square
root of the number of steps, the same $\sqrt{n}$ the darts page meets.
```

</div>

## Lab bench

Every number this experiment uses is named at the top of the cell.
Change them, run it, and see what happens.

```python exec
id: lab-bench-1
import random
import matplotlib.pyplot as plt

SEED = 42       # change it for another run
ROLLS = 1000    # how many times to roll
SIDES = 6       # the number of faces on the die

random.seed(SEED)
rolls = [random.randint(1, SIDES) for _ in range(ROLLS)]
counts = [rolls.count(face) for face in range(1, SIDES + 1)]
print(counts)

plt.bar(range(1, SIDES + 1), counts)
plt.xlabel("face")
plt.ylabel("times rolled")
```

Choose one of these questions, or ask one of your own:

1. How uneven are the counts with 60 rolls? With 60,000?
2. Can you find a seed where, in 60 rolls, one face comes up twice as
   often as another?
3. Change the cell to roll two dice and add them. Which total comes up
   most often, and why?
4. A die with 20 faces is used in some games. How many rolls does it
   need before its counts look as even as a six-sided die's at 1,000?

## Reflection

The word *random* has a narrower meaning now than it had at the start of
this page. It no longer means "impossible to predict". It means
"impossible to predict for anyone who does not know the seed". It also
means "regular enough that the difference never appears in the answer".

When you first saw the numbers repeat, did it feel like a
disappointment? Or did the reason make sense before you read the
explanation? Both reactions are common. If it was the second, trust that
feeling. You could build the whole argument for reproducibility yourself,
from one afternoon spent chasing a bug.

Where else have you met something that is not exactly what it claims to
be, but is so close that the difference never matters? Computing has many
examples like this. When you notice them, you understand a system
better, and do not only use it.

## Where to read more

Python Software Foundation. *`random` — Generate pseudo-random numbers.*
<https://docs.python.org/3/library/random.html>. This is the module's own
documentation. It is unusually easy to read for a standard-library page.
The opening note on which functions are safe for security is worth
reading on its own.

Python Software Foundation. *`secrets` — Generate secure random numbers for
managing secrets.* <https://docs.python.org/3/library/secrets.html>. This
page covers the cases where a predictable number is a weakness, not a
feature.

Downey, A. B. (2015). *Think Python* (2nd ed.). O'Reilly. Chapter 13
builds a word-frequency study on `random` and is a good next step if the
"choose a thing, not a number" half of this tutorial was the interesting
part.

Matsumoto, M. and Nishimura, T. (1998). *Mersenne Twister: A
623-dimensionally equidistributed uniform pseudo-random number
generator.* ACM Transactions on Modeling and Computer Simulation, 8(1),
3–30.
<https://doi.org/10.1145/272991.272995>. The algorithm behind Python's own
generator. It is much harder than anything in this series. We include it
because you can go and check the claim that an algorithm makes the
sequence.

Veritasium (2014). *What is NOT Random?*
<https://www.youtube.com/watch?v=sMb00lz-IfE>. Is anything truly random,
or would it all be predictable if we knew enough? Veritasium asks
physicists. The video is ten minutes long.
