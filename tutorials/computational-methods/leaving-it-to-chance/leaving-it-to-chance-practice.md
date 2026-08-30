---
title: "Leaving It to Chance — Practice"
slug: leaving-it-to-chance-practice
practice_for: leaving-it-to-chance
module: computational-methods
module_title: "Computational Methods"
year: "2026-2027"
series: simulation
version: 2026.08.30.1
---

# Leaving It to Chance — Practice

A warning that applies to every problem on this page: your numbers will not
match the ones in the answers unless you set the same seed. That is the whole
point of the tutorial, and it makes checking your work slightly unusual here
— what you are confirming is that the *shape* of your result is right, not
that it matches digit for digit.

Where a problem sets a seed, use it and the numbers will agree exactly.

## Getting Numbers Out

```python exec
id: getting-numbers-out-1
import random
```

**1.** How would you produce a random number between 10 and 20?

<details class="dl-answer"><summary>answer</summary>

`random.uniform(10, 20)` gives a number with decimals; `random.randint(10, 20)`
gives a whole number, and includes both 10 and 20 as possibilities.

Worth knowing about that second one: most Python functions that take a range
stop *before* the end value — `range(1, 6)` gives you 1 to 5. `randint` is the
exception and includes both ends, which is exactly what you want for a die
but catches people out. `random.randrange(10, 20)` is the one that behaves
like `range` and stops at 19.

</details>

**2.** Simulate flipping a coin 100 times and count the heads. Roughly how
many would you expect, and how far from that did you land?

```python exec
id: getting-numbers-out-2
hint: random.choice(["H", "T"]) flips once. A loop, a counter, and a comparison will do the rest — or count a list of flips afterwards with .count("H").
```

<details class="dl-answer"><summary>answer</summary>

```python
import random
random.seed(1)

flips = [random.choice(["H", "T"]) for _ in range(100)]
heads = flips.count("H")
print(heads)
```

With `seed(1)` this gives 46. You would expect about 50, and anything from
roughly 40 to 60 should not raise an eyebrow — that spread is the subject of
the third tutorial in this series.

If you got a number like 3 or 97, something is wrong with the code rather
than with your luck.

</details>

**3.** Run your coin-flip cell several times without setting a seed. Then set
one and run it several times more. Describe the difference in one sentence.

<details class="dl-answer"><summary>answer</summary>

Without a seed the count changes on every run; with a seed it is the same
count every time, because the sequence of flips is the same sequence.

The sentence worth arriving at: setting a seed does not make the numbers less
random-looking, it makes the *run* repeatable.

</details>

## Seeds and Repetition

**4.** Write a function `roll_under(seed, n)` that sets the given seed and
returns a list of `n` dice rolls. Then show that calling it twice with the
same seed gives the same list, and that two different seeds give different
lists.

```python exec
id: seeds-and-repetition-1
hint: The function needs to call random.seed(seed) before it rolls anything — the setting has to happen inside, so that each call starts from the same place.
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

The second comparison is "almost certainly" rather than "certainly" — two
different seeds *could* produce the same four rolls by coincidence, with
about a one in 1,296 chance. Worth noticing that a test written this way is
not quite a proof.

</details>

**5.** A colleague reports that their simulation crashed after about forty
thousand steps, and sends you the code. What one piece of information do you
need from them to see the crash yourself, and what should their code have
been doing to make sure they can give it to you?

<details class="dl-answer"><summary>answer</summary>

The seed. And their code should have been choosing a seed explicitly and
printing or logging it at the start of every run, rather than letting Python
pick one silently from the clock.

This is the practical form of the tutorial's argument. A bug that appears one
run in fifty is nearly impossible to fix if every run is unrepeatable, and
completely ordinary to fix if you can replay the exact run that broke.

</details>

## Choosing Things

**6.** A bag holds four red, three blue and one green marble. Draw one marble
at random, and confirm over many draws that red comes up about half the time.

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

Red comes out near 0.5, blue near 0.375, green near 0.125 — matching 4/8, 3/8
and 1/8.

There is a neater way, worth meeting: `random.choices(["red", "blue",
"green"], weights=[4, 3, 1], k=10000)` says the same thing without building a
list of repeats. The repeated-list version is easier to see through, which is
why it comes first.

</details>

**7.** Deal a five-card hand from a standard 52-card deck, with no card
appearing twice.

```python exec
id: choosing-things-2
hint: Building the deck is the fiddly part: a nested loop or a comprehension over ranks and suits will give you all 52. Then it is one call — the question is which of sample and choices deals a hand.
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

`sample`, because a dealt card does not go back in the deck. Using `choices`
here would let the same card appear twice in one hand, which is the kind of
bug that survives a long time in a card game nobody plays much.

</details>

**8.** Shuffle a deck instead of sampling from it. What does
`random.shuffle` do that `random.sample` does not, and why does it not return
anything?

<details class="dl-answer"><summary>answer</summary>

```python
import random
random.seed(11)

deck = list(range(1, 53))
random.shuffle(deck)
print(deck[:5])
```

`shuffle` rearranges the list *in place* — it changes the list you gave it
rather than building a new one, which is why it returns `None`. Assigning
`deck = random.shuffle(deck)` is a common and painful mistake: it replaces
your deck with nothing at all.

`sample(deck, k=52)` gets you a shuffled copy while leaving the original
alone, which is often what you actually want.

</details>

## Thinking It Through

**9.** A lottery draws six numbers from 1 to 45. Someone argues that
1, 2, 3, 4, 5, 6 is a worse choice than 7, 19, 23, 31, 38, 44 because the
first "would never come up". Simulate enough draws to have an opinion, and
say what you think the argument is actually about.

```python exec
id: thinking-it-through-1
hint: You cannot simulate your way to seeing either specific combination appear — there are over eight million. Something you can measure instead: how often a draw contains six consecutive numbers, against how often it contains six scattered ones.
```

<details class="dl-answer"><summary>answer</summary>

Both combinations are exactly as likely as each other: one in 8,145,060. Any
simulation you write will show consecutive runs are rare, but it will show
*any* named combination is equally rare, which is the point.

What the argument is actually about is that the two look different to a
person, not to the draw. We read 1-2-3-4-5-6 as a pattern and patterns feel
designed, so it feels like it needs an explanation the other does not.

There is one real consideration hiding in it, and it is not about
probability: many people pick 1-2-3-4-5-6, so if it *did* come up the prize
would be split many ways. The expected payout is genuinely lower. That is an
argument about other players, not about the machine.

</details>

**10.** You are testing a program that fails roughly one run in a thousand,
and each run takes about a second. Estimate how long you would expect to wait
to see the failure once. Then say what you would do differently if the same
failure happened one run in a million.

<details class="dl-answer"><summary>answer</summary>

About a thousand seconds — roughly seventeen minutes — to expect one failure,
though you might wait far longer or hit it in the first minute. "One in a
thousand" is an average, not a schedule.

At one in a million you would be waiting about eleven days, and repeatedly
running the whole program stops being a sensible way to find it. The usual
answers: make each run faster or run many in parallel; log the seed on every
run so that the one failure you do eventually see becomes reproducible
forever; or stop sampling and reason about the code directly, which is where
this module's problem-solving outcomes come in.

The general shape is worth keeping: simulation is a fine tool for finding
something that happens often enough, and a poor one for finding something
rare. Knowing which side of that line you are on is most of the skill.

</details>
