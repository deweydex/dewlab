---
title: "Random numbers: pseudo-random numbers and seeds — Practice"
practice_for: leaving-it-to-chance
year: "2026-2027"
version: 2026.09.22.1
---

# Random numbers: pseudo-random numbers and seeds — Practice

The answers are hidden in folds under each problem. Try each problem
yourself before you open its fold.

One warning applies to every problem on this page. Your numbers will not
match the numbers in the answers unless you set the same seed. That is
the main idea of the tutorial, and it makes your checks a little
unusual here. You are checking that the *shape* of your result is right:
roughly the right size, and the right kind of number. You are not
checking that it matches digit for digit.

Where an answer sets a seed, use the same seed, and your numbers will
match exactly.

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

**2.** Simulate flipping a coin 100 times, and count the heads. About how
many heads would you expect? How far from that did you land?

```python exec
id: getting-numbers-out-2
hint: random.choice(["H", "T"]) flips once. A loop, a counter and an if will do the rest. Or you can build a list of flips, then count the heads with .count("H").
```

<details class="dl-answer"><summary>answer</summary>

```python
import random
random.seed(1)

flips = [random.choice(["H", "T"]) for _ in range(100)]
heads = flips.count("H")
print(heads)
```

With `seed(1)`, this gives 46. You would expect about 50. Anything from
about 40 to 60 is normal, and should not surprise you.

If you got a number like 3 or 97, the problem is in the code. It is not
bad luck.

</details>

**3.** Try these two steps, then describe the difference in one sentence.

1. Run your coin-flip cell several times without setting a seed.
2. Set a seed, and run it several more times.

<details class="dl-answer"><summary>answer</summary>

Without a seed, the count changes on every run. With a seed, the count is
the same every time, because the flips come out in the same order.

Here is one sentence: a seed makes the *run* repeatable, and the
numbers look just as random as before.

</details>

## Seeds and repetition

**4.** This problem has three steps.

1. Write a function `roll_under(seed, n)`. It sets the given seed, then
   returns a list of `n` dice rolls.
2. Show that two calls with the same seed give the same list.
3. Show that two different seeds give different lists.

```python exec
id: seeds-and-repetition-1
hint: The function needs to call random.seed(seed) before it rolls anything. Setting the seed inside the function means each call starts from the same place.
```

<details class="dl-answer"><summary>answer</summary>

```python
import random

def roll_under(seed, n):
    random.seed(seed)
    return [random.randint(1, 6) for _ in range(n)]

print(roll_under(5, 4) == roll_under(5, 4))   # True
print(roll_under(5, 4) == roll_under(6, 4))   # almost certainly False
```

The second comparison says "almost certainly", and not "certainly". Two
different seeds *could* give the same four rolls by chance. The chance is
about one in 1,296. So a test written this way is not quite a proof.

</details>

**5.** A colleague tells you that their simulation crashed after about
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

**6.** A bag holds four red marbles, three blue and one green.

1. Draw one marble at random.
2. Draw many times, and check that red comes up about half the time.

```python exec
id: choosing-things-1
hint: One way is a list holding each marble as many times as it occurs, then random.choice on it. Counting the results of many draws will tell you whether the proportions look right.
```

<details class="dl-answer"><summary>answer</summary>

```python
import random
random.seed(3)

bag = ["red"] * 4 + ["blue"] * 3 + ["green"]
draws = [random.choice(bag) for _ in range(10000)]

for colour in ["red", "blue", "green"]:
    print(colour, draws.count(colour) / len(draws))
```

Red comes out near 0.5, blue near 0.375 and green near 0.125. These match
4/8, 3/8 and 1/8.

There is a shorter way:
`random.choices(["red", "blue", "green"], weights=[4, 3, 1], k=10000)`.
It says the same thing, without building a list of repeats. The
repeated-list version is easier to understand, so we met it first.

</details>

**7.** Deal a five-card hand from a standard 52-card deck. No card can
appear twice.

```python exec
id: choosing-things-2
hint: Building the deck is the hardest part. A nested loop, or a comprehension over ranks and suits, gives you all 52 cards. Then you need one call. Which of sample and choices deals a hand?
```

<details class="dl-answer"><summary>answer</summary>

```python
import random
random.seed(11)

ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
suits = ["♠", "♥", "♦", "♣"]
deck = [rank + suit for suit in suits for rank in ranks]

hand = random.sample(deck, k=5)
print(hand)
print("all different:", len(hand) == len(set(hand)))
```

The line that builds `deck` is a list comprehension with two `for` parts.
It works like a nested loop: for each suit, it visits every rank.

Use `sample`, because a dealt card does not go back in the deck. With
`choices`, the same card could appear twice in one hand. In a card game
that few people play, a bug like that can go unnoticed for a long time.

</details>

**8.** Shuffle a deck, instead of sampling from it.

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

## Thinking it through

**9.** A lottery draws six numbers from 1 to 45. Someone says that
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

**10.** You are testing a program that fails about one run in a thousand.
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
