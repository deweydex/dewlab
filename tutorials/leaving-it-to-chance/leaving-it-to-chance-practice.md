---
title: "Random numbers: pseudo-random numbers and seeds — Practice"
practice_for: leaving-it-to-chance
year: "2026-2027"
version: 2026.09.27.1
worlds:
  living-systems: Turtles on a coral reef, tagged by a biologist.
  queues-and-crowds: The riders on a theme-park ride.
  spread: A disease that starts somewhere on a grid of towns.
  space-and-physics: The minutes in which meteors streak across the sky.
---

# Random numbers: pseudo-random numbers and seeds — Practice

Each answer is hidden until you open it. Write something down first,
even a guess, and then open the answer to compare.

Where a problem asks you to write a function, the function takes a
`seed` and sets it before it draws any random numbers. That is the
tutorial's main idea at work: with the same seed, your function and the
answer's give the same numbers, and you can compare them row by row.

## Getting numbers out

```python exec
id: getting-numbers-out-1
import random
```

**1.** How would you produce a random number between 10 and 20?

<details class="dl-answer"><summary>answer</summary>

There are two ways, depending on the kind of number you want.

- `random.uniform(10, 20)` gives a number with decimals.
- `random.randint(10, 20)` gives a whole number. Both 10 and 20 can come
  up.

Look closely at `randint`. Most Python functions that take a range stop
*before* the end value: `range(1, 6)` gives you 1 to 5. `randint` is
different, and includes both ends. That is what you want for a die, but
it surprises many people. `random.randrange(10, 20)` works like `range`,
and stops at 19.

</details>

**2.** Can you write `count_heads(flips, seed)`? It sets the seed,
flips a coin `flips` times with `random.choice(["H", "T"])`, and returns
the number of heads. About how many heads would you expect from 100
flips?

```python exec
id: getting-numbers-out-2
def count_heads(flips, seed):
    """Heads in this many coin flips, under a stated seed."""
    # Your code here.
```

```hint
Set the seed first. Then build a list of flips with a comprehension,
and count the heads with `.count("H")`.
```

```inputs
count_heads(100, 1)
count_heads(100, 2)
count_heads(10000, 1)
```

```solution
def count_heads(flips, seed):
    """Heads in this many coin flips, under a stated seed."""
    random.seed(seed)
    flips_made = [random.choice(["H", "T"]) for _ in range(flips)]
    return flips_made.count("H")
---
Seed 1 gives 46 heads in 100, and seed 2 gives exactly 50. Anything from
about 40 to 60 is normal for 100 flips. In 10,000 flips, seed 1 gives
5,055, only half a percent from half. If your count were 3 or 97, the
cause would be in the code, not in the luck.
```

**3.** Try these two steps, then describe the difference in one sentence.

1. Flip 100 coins in a cell without setting a seed, and run it several
   times.
2. Set a seed at the top of the cell, and run it several more times.

```python exec
id: getting-numbers-out-4
```

<details class="dl-answer"><summary>answer</summary>

Without a seed, the count changes on every run. With a seed, the count is
the same every time, because the flips come out in the same order.

Here is one sentence: a seed makes the *run* repeatable, and the
numbers look just as random as before.

</details>

**4.** `randint(1, 6)` includes both 1 and 6. `random.randrange(1, 6)`
works like `range(1, 6)`. This cell draws from it a thousand times, and
prints the biggest number it saw.

```python exec
id: getting-numbers-out-3
random.seed(3)
print(max(random.randrange(1, 6) for _ in range(1000)))
```

```predict
type: number

What will the cell print?
```

<details class="dl-answer"><summary>why</summary>

It prints 5. `randrange(1, 6)` stops *before* 6, like `range(1, 6)`,
however many times you draw. `randint` is the one function here that
includes its end value. That suits a die, and it surprises many people.

</details>

## Seeds and repetition

**5.** Can you write `roll_under(seed, n)`? It sets the given seed,
then returns a list of `n` dice rolls. Two calls with the same seed
should give the same list.

```python exec
id: seeds-and-repetition-1
def roll_under(seed, n):
    """n dice rolls, starting from the given seed."""
    # Your code here.
```

```hint
The function calls `random.seed(seed)` before it rolls anything, so
each call starts from the same place.
```

```inputs
roll_under(5, 4)
roll_under(5, 4) == roll_under(5, 4)
roll_under(5, 4) == roll_under(6, 4)
```

```solution
def roll_under(seed, n):
    """n dice rolls, starting from the given seed."""
    random.seed(seed)
    return [random.randint(1, 6) for _ in range(n)]
---
Seed 5 gives `[5, 3, 6, 3]` every time, and seed 6 gives `[5, 1, 4, 3]`.
Two different seeds *could* give the same four rolls by chance: about
one time in 1,296. So a comparison like the last one shows the seeds
differ here, but it does not prove they always would.
```

**6.** A colleague tells you that their simulation crashed after about
forty thousand steps, and sends you the code.

- What one piece of information do you need from them, to see the crash
  yourself?
- What should their code have been doing, so that they can give it to
  you?

<details class="dl-answer"><summary>answer</summary>

You need the seed. Their code should choose a seed itself, and print it or
write it to a log at the start of every run. Otherwise Python picks a seed
from the operating system, and nobody ever sees it.

This is the tutorial's argument in practice. Say a bug appears on one run
in fifty. If no run can be repeated, that bug is nearly impossible to fix.
If you can replay the exact run that broke, it is an ordinary bug to fix.

</details>

## Choosing things

**7.** A bag holds four red marbles, three blue and one green. Can you
write `share_red(draws, seed)`? It sets the seed, draws a marble
`draws` times, putting it back each time, and returns the share of
draws that were red.

```python exec
id: choosing-things-1
def share_red(draws, seed):
    """The share of red, in this many draws with replacement."""
    # Your code here.
```

```hint
A list that holds each marble as many times as it occurs,
`["red"] * 4 + ["blue"] * 3 + ["green"]`, works with `random.choice`.
```

```inputs
share_red(10000, 3)
share_red(8, 3)
share_red(8, 4)
```

```solution
def share_red(draws, seed):
    """The share of red, in this many draws with replacement."""
    random.seed(seed)
    bag = ["red"] * 4 + ["blue"] * 3 + ["green"]
    drawn = [random.choice(bag) for _ in range(draws)]
    return drawn.count("red") / draws
---
In 10,000 draws, 0.4911 are red, close to 4/8. In eight draws, seed 3
gives exactly half, and seed 4 gives 0.625. There is a shorter way to
draw with weights: `random.choices(["red", "blue", "green"], weights=[4,
3, 1], k=draws)`. It is the call a Markov chain uses to choose its next
word.
```

**8.** Can you write `deal(seed)`? It builds a standard 52-card deck,
sets the seed, and deals a five-card hand in which no card can appear
twice.

```python exec
id: choosing-things-2
def deal(seed):
    """A five-card hand from a 52-card deck, under a stated seed."""
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    suits = ["♠", "♥", "♦", "♣"]
    # Your code here.
```

```hint
`[rank + suit for suit in suits for rank in ranks]` builds the deck: for
each suit, every rank. Then one call deals the hand. Which of `sample`
and `choices` puts a card back?
```

```inputs
deal(11)
len(set(deal(12)))
```

```solution
def deal(seed):
    """A five-card hand from a 52-card deck, under a stated seed."""
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    suits = ["♠", "♥", "♦", "♣"]
    deck = [rank + suit for suit in suits for rank in ranks]
    random.seed(seed)
    return random.sample(deck, k=5)
---
Seed 11 deals `['4♦', 'J♦', 'Q♣', '5♦', '8♦']`. `sample` never repeats
a card, so the set of any hand has 5 cards in it. With `choices`, the
same card could appear twice in one hand: a bug that can go unnoticed
for a long time in a game few people play.
```

**9.** Shuffle a deck, instead of sampling from it.

- What does `random.shuffle` do that `random.sample` does not?
- Why does `random.shuffle` not return anything?

<details class="dl-answer"><summary>answer</summary>

```python
import random
random.seed(11)

deck = list(range(1, 53))
random.shuffle(deck)
print(deck[:5])
```

`shuffle` changes the order of the list you gave it. This is called
changing the list *in place*. It does not build a new list, so it returns
`None`.

A common and painful mistake is to write `deck = random.shuffle(deck)`.
That line replaces your deck with `None`, which is nothing at all.

`sample(deck, k=52)` gives you a shuffled copy, and leaves the original
list as it was. Often, that is what you want.

</details>

## Your world

**10.** A problem from the world you chose.

<div class="dl-world" data-world="living-systems">

A biologist tags turtles on a reef, choosing `k` of the `turtles` at
random, numbered from 1, and never the same turtle twice. Can you write
`tag_turtles(turtles, k, seed)`, which returns the chosen numbers in
order?

```python exec
id: your-world-1--living-systems
def tag_turtles(turtles, k, seed):
    """k different turtles, numbered from 1, chosen at random and sorted."""
    # Your code here.
```

```hint
`range(1, turtles + 1)` is every turtle's number. Which of `sample` and
`choices` never picks the same one twice? `sorted()` puts the result in
order.
```

```inputs
tag_turtles(40, 5, 1)
tag_turtles(40, 5, 2)
tag_turtles(5, 5, 3)
```

```solution
def tag_turtles(turtles, k, seed):
    """k different turtles, numbered from 1, chosen at random and sorted."""
    random.seed(seed)
    return sorted(random.sample(range(1, turtles + 1), k))
---
Seed 1 tags turtles 5, 8, 9, 17 and 37. When `k` is every turtle, as in
the last row, `sample` has no choice left: every turtle is tagged.
`choices` would be the wrong tool, because a turtle already tagged
cannot be tagged again.
```

</div>

<div class="dl-world" data-world="queues-and-crowds">

The riders for a theme-park ride arrive together, and the order they
board is chosen at random. Can you write `ride_order(riders, seed)`,
which returns a shuffled copy of the list and leaves the original as it
was?

```python exec
id: your-world-1--queues-and-crowds
def ride_order(riders, seed):
    """A shuffled copy of riders; the list passed in is left as it was."""
    # Your code here.
```

```hint
`random.shuffle` changes the list you give it, in place, and returns
`None`. So shuffle a copy: `list(riders)` makes one.
```

```inputs
ride_order(["Aoife", "Brendan", "Ciara", "Dara"], 1)
ride_order(["Aoife", "Brendan", "Ciara", "Dara"], 2)
sorted(ride_order(list(range(10)), 3))
```

```solution
def ride_order(riders, seed):
    """A shuffled copy of riders; the list passed in is left as it was."""
    random.seed(seed)
    order = list(riders)
    random.shuffle(order)
    return order
---
Seed 1 puts Dara first and Brendan last. Sorted, any shuffle of 0 to 9
gives 0 to 9 again: a shuffle changes the order and nothing else.
`random.sample(riders, k=len(riders))` would also give a shuffled copy.
```

</div>

<div class="dl-world" data-world="spread">

A disease starts in one town on a grid of towns, `rows` by `cols`. Can
you write `random_cell(rows, cols, seed)`, which returns the row and
column of the first town, each counted from 0?

```python exec
id: your-world-1--spread
def random_cell(rows, cols, seed):
    """A (row, column) pair on the grid, chosen at random."""
    # Your code here.
```

```hint
`random.randrange(rows)` gives a row from 0 to `rows - 1`, like
`range(rows)`. Do the same for the column, and return the two as a
tuple.
```

```inputs
random_cell(10, 10, 1)
random_cell(10, 10, 2)
random_cell(1, 1, 5)
```

```solution
def random_cell(rows, cols, seed):
    """A (row, column) pair on the grid, chosen at random."""
    random.seed(seed)
    return (random.randrange(rows), random.randrange(cols))
---
Seed 1 starts the disease at row 2, column 9. On a grid of one town,
it can only start at (0, 0). `randint(0, rows - 1)` gives the same
range of rows; `randrange(rows)` says it without the `- 1`.
```

</div>

<div class="dl-world" data-world="space-and-physics">

During an hour of a meteor shower, each meteor appears in a minute
chosen at random, from 0 to 59. Can you write `meteor_minutes(meteors,
seed)`, which returns the list of minutes?

```python exec
id: your-world-1--space-and-physics
def meteor_minutes(meteors, seed):
    """The minute, 0 to 59, in which each meteor appears."""
    # Your code here.
```

```hint
One `random.randint(0, 59)` for each meteor, in a list. Two meteors can
appear in the same minute.
```

```inputs
meteor_minutes(5, 1)
len(set(meteor_minutes(10, 1)))
len(set(meteor_minutes(10, 2)))
```

```solution
def meteor_minutes(meteors, seed):
    """The minute, 0 to 59, in which each meteor appears."""
    random.seed(seed)
    return [random.randint(0, 59) for _ in range(meteors)]
---
With seed 1, five meteors appear in minutes 8, 36, 54, 51 and 48. With
ten meteors, seeds 1 and 2 each give only 9 different minutes: two
meteors shared a minute. With 60 minutes to choose from, that happens
more often than most people guess.
```

</div>

## Thinking it through

**11.** A lottery draws six numbers from 1 to 45. Someone says that
1, 2, 3, 4, 5, 6 is a worse choice than 7, 19, 23, 31, 38, 44, because
the first "would never come up".

1. Simulate enough draws to form an opinion.
2. What do you think the argument is really about?

```python exec
id: thinking-it-through-1
hint: There are over eight million combinations, so a simulation will almost never show either one. Here is something you can measure instead. How often does a draw contain six numbers in a row? How often does it contain six numbers spread out?
```

<details class="dl-answer"><summary>answer</summary>

Both combinations are equally likely: one chance in 8,145,060 each. Any
simulation you write will show that six numbers in a row are rare. But it
will also show that *any* one named combination is just as rare.

The argument is really about how the two combinations look to a person.
The draw cannot see any difference. We see 1-2-3-4-5-6 as a pattern, and
a pattern feels planned. So it seems to need an explanation that the other
combination does not.

There is one real point hidden in the argument, and it is not about
probability. Many people pick 1-2-3-4-5-6. If it *did* come up, the prize
would be shared between many winners, so each winner would expect to get
less. That is an argument about the other players, not about the machine.

</details>

**12.** You are testing a program that fails about one run in a thousand.
Each run takes about a second.

1. Estimate how long you would expect to wait to see the failure once.
2. What would you do differently if the failure happened one run in a
   million?

<details class="dl-answer"><summary>answer</summary>

You would expect to wait about a thousand seconds, which is about
seventeen minutes. But you might wait much longer, or see it in the first
minute. "One in a thousand" is an average, not a timetable.

At one in a million, you would wait about eleven days. It is no longer
sensible to run the whole program again and again to find the failure.
Here are the usual choices:

- Make each run faster, or run many at the same time.
- Log the seed on every run. Then the one failure you do see can be
  repeated as often as you like.
- Stop running it, and reason about the code directly. The Problem Solving
  part of this module is about exactly that.

The general idea is worth keeping. Simulation is a good tool for finding
something that happens often. It is a poor tool for finding something
rare. So first decide which of the two you are looking for.

</details>

## From earlier

**13.** From [Comprehensions, grids and
aliasing](tutorial:comprehensions-and-grids). The deck in problem 8 is
built by a comprehension with two `for` parts.

```python exec
id: from-earlier-1
print(" ".join(rank + suit for suit in "♠♥" for rank in "AK"))
```

```predict
type: choice

What will the cell print?

- A♠ K♠ A♥ K♥
- A♠ A♥ K♠ K♥
  - The first `for` is the one nearest the start of the line.
```

<details class="dl-answer"><summary>why</summary>

The two `for` parts run in the order they are written, like a loop
inside a loop: the first is the outer loop. For each suit, every rank.
So both spades come first.

</details>
