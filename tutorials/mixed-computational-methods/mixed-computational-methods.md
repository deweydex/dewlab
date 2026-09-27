---
title: "Mixed problems: Computational Methods, the whole course"
practice_across:
  - lists-and-sequences
  - looking-things-up-by-name
  - what-a-matrix-does-to-a-picture
  - undoing-it
  - where-chains-lead
  - turning-a-cube
  - a-chain-reads-a-book
  - how-much-it-remembers
  - counting-darts
  - stepping-forward-in-time
  - finding-everything-inside-a-folder
  - three-ways-to-make-change
  - finding-where-it-went-wrong
year: "2026-2027"
version: 2026.09.27.1
datasets: [the-time-machine, dracula, dubliners, irish-fairy-tales, treasure-island]
worlds:
  the-time-machine: The Time Machine, by H. G. Wells (1895), a journey to the far future.
  dracula: Dracula, by the Dublin-born writer Bram Stoker (1897), told in letters and diaries.
  dubliners: Dubliners, by James Joyce (1914), fifteen stories set in Dublin.
  irish-fairy-tales: Irish Fairy Tales, by James Stephens (1920), the old stories of Fionn and the Fianna.
  treasure-island: Treasure Island, by Robert Louis Stevenson (1883), pirates and a voyage by sea.
---

# Mixed problems: Computational Methods, the whole course

These problems come from every series of the course, in no order, and
do not say which series each one comes from. Choosing the idea is the
first half of every problem. The set ends with something to make: two
bots, and a test that tells them apart.

```python exec
id: mixed-computational-methods-tools
import math
import random
```

## 1.

A 2×2 matrix has a determinant of 0. What does it do to a picture? Can
another matrix undo it? Try `[[1, 2], [2, 4]]` on the corners of a
square.

```python exec
id: mixed-computational-methods-flat
```

<details class="dl-answer"><summary>answer</summary>

It squashes the whole picture onto a line, so every area becomes 0.
`[[1, 2], [2, 4]]` sends $(1, 0)$ to $(1, 2)$ and $(0, 1)$ to $(2, 4)$,
and both lie on the line $y = 2x$. Nothing can undo it: many points
land on the same place, and no matrix can tell which one each came
from. That is why a matrix with a determinant of 0 has no inverse.

</details>

## 2.

You and a classmate both build a chain from the same book, and both
write with `random.seed(7)`. Your sentences are different. Name two
things that could explain it.

<details class="dl-answer"><summary>answer</summary>

Any of these, and there are others:

- The two chains are different: one of you cleaned the book
  differently, or split the words differently, so the counts differ.
- You started from different words, or wrote a different number of
  words.
- One of you drew another random number between `random.seed(7)` and
  the writing, which moves every choice after it one place along.
- The followers are in a different order in your dictionary, so the
  same random number picks a different word.

</details>

## 3.

This walk prints each folder only after it has walked every folder
inside it.

```python exec
id: mixed-computational-methods-after
music = {
    "name": "music",
    "subfolders": [
        {"name": "rock", "subfolders": [{"name": "live", "subfolders": []}]},
        {"name": "jazz", "subfolders": []},
    ],
}


def walk_after(folder):
    for sub in folder["subfolders"]:
        walk_after(sub)
    print(folder["name"], end=" ")


walk_after(music)
print()
```

```predict
type: choice

In what order will it print the folders?

- music rock live jazz
  - That is the order when each folder prints before its insides.
- live rock jazz music
- jazz live rock music
  - The loop takes the subfolders in the order they are listed.
```

"music" waits for both its subfolders. "rock" waits for "live", so
"live" prints first, then "rock", then "jazz", and "music" last. Moving
one `print` from before the loop to after it turns the whole order
round.

## 4.

Here are the lines of `generate2()`, a writer from a chain that keys on
two words, in the wrong order. The indentation is right. Can you put
them in order?

```python
        result.append(random.choices(list(followers), weights=list(followers.values()))[0])
def generate2(chain, w1, w2, steps):
    return result
        followers = chain[key]
    result = [w1, w2]
            break
        if key not in chain:
    for _ in range(steps):
        key = (result[-2], result[-1])
```

```python exec
id: mixed-computational-methods-parsons
words = "the cat sat on the mat and then it slept".split()
tiny2 = {}
for w1, w2, next_word in zip(words, words[1:], words[2:]):
    tiny2.setdefault((w1, w2), {})
    tiny2[(w1, w2)][next_word] = tiny2[(w1, w2)].get(next_word, 0) + 1


# Your generate2 here.
```

```hint
The function starts with its `def` line and the list it builds. Inside
the loop, it makes the key first, stops if the key has no followers,
and only then chooses a follower.
```

```inputs
generate2(tiny2, "the", "cat", 5)
generate2(tiny2, "it", "slept", 3)
```

```solution
def generate2(chain, w1, w2, steps):
    result = [w1, w2]
    for _ in range(steps):
        key = (result[-2], result[-1])
        if key not in chain:
            break
        followers = chain[key]
        result.append(random.choices(list(followers), weights=list(followers.values()))[0])
    return result
---
Every pair of words in this sentence appears once, so every key has one follower and the writer recites. From "it slept" there is nothing further, so the `break` stops it at once.
```

## 5.

Can you write `first_failure(coins, limit)`? It returns the smallest
amount, from 1 to `limit`, for which greedy change uses more coins than
the fewest possible, or `None` if there is no such amount.

```python exec
id: mixed-computational-methods-first-failure
def fewest(amount, coins, cache=None):
    """The fewest coins that make amount exactly, or None."""
    if cache is None:
        cache = {}
    if amount == 0:
        return 0
    if amount in cache:
        return cache[amount]
    best = None
    for coin in coins:
        if coin <= amount:
            rest = fewest(amount - coin, coins, cache)
            if rest is not None and (best is None or rest + 1 < best):
                best = rest + 1
    cache[amount] = best
    return best


def greedy(amount, coins):
    """Coins taken largest first, or None if that leaves a remainder."""
    remaining = amount
    count = 0
    for coin in sorted(coins, reverse=True):
        while remaining >= coin:
            remaining -= coin
            count += 1
    return count if remaining == 0 else None


def first_failure(coins, limit):
    """The smallest amount where greedy uses more coins than it needs, or None."""
    # Your code here.
```

```hint
Try each amount in order, from 1, and return the first one where
`greedy()` and `fewest()` disagree.
```

```inputs
first_failure([1, 3, 4], 20)
first_failure([1, 5, 6, 9], 30)
first_failure([1, 2, 5, 10], 50)
```

```solution
def first_failure(coins, limit):
    """The smallest amount where greedy uses more coins than it needs, or None."""
    for amount in range(1, limit + 1):
        if greedy(amount, coins) != fewest(amount, coins):
            return amount
    return None
---
With [1, 3, 4], greedy first fails at 6: 4 + 1 + 1 against 3 + 3. With [1, 5, 6, 9], at 11: 9 + 1 + 1 against 5 + 6. The euro coins up to 10c never fail up to 50, so the answer is None.
```

## 6.

This loop is meant to drop a ball from 60 metres. It never finishes.
Why? Read it: do not run it.

```python
height = 60
velocity = 0
step = 0.1
while height > 0:
    velocity = velocity + -9.8 * step
    new_height = height + velocity * step
```

<details class="dl-answer"><summary>answer</summary>

The loop calculates `new_height`, but never gives that value to
`height`. So `height` stays 60, `height > 0` stays true, and the loop
runs for ever. The last line should be `height = height + velocity *
step`. A loop ends only when something inside it changes what its
condition tests.

</details>

## 7.

In a room of 23 people, what is the chance that two share a birthday?
Guess first. Can you write `shared_birthday(people, trials, seed)`? It
sets the seed, then, in each trial, gives each person a birthday with
`random.randint(1, 365)`, and returns the share of trials in which two
or more people share one.

```python exec
id: mixed-computational-methods-birthdays
def shared_birthday(people, trials, seed):
    """The share of trials in which two or more people share a birthday."""
    # Your code here.
```

```hint
In each trial, make a list of birthdays. If a set made from the list is
smaller than the list, some birthday appeared twice.
```

```inputs
shared_birthday(23, 1000, seed=1)
shared_birthday(10, 1000, seed=1)
shared_birthday(50, 1000, seed=1)
```

```solution
def shared_birthday(people, trials, seed):
    """The share of trials in which two or more people share a birthday."""
    random.seed(seed)
    shared = 0
    for _ in range(trials):
        birthdays = [random.randint(1, 365) for _ in range(people)]
        if len(set(birthdays)) < people:
            shared += 1
    return shared / trials
---
With 23 people, half the trials, 0.5, had a shared birthday. Most people guess much lower, because they think of the chance that somebody shares *their* birthday. But 23 people make 253 pairs, and any pair will do.
```

Now calculate it. The chance that nobody shares is the chance that the
second person misses the first, times the chance that the third misses
both, and so on: $\frac{364}{365} \times \frac{363}{365} \times \dots$
Can you write `no_shared(people)`, which multiplies those chances?

```python exec
id: mixed-computational-methods-birthdays-exact
def no_shared(people):
    """The exact chance that no two of `people` share a birthday."""
    # Your code here.
```

```hint
Start with a chance of 1. For each person after the first, multiply by
the share of days still free: `(365 - k) / 365`, where `k` is how many
people came before.
```

```inputs
round(1 - no_shared(23), 4)
round(1 - no_shared(10), 4)
round(1 - no_shared(50), 4)
```

```solution
def no_shared(people):
    """The exact chance that no two of `people` share a birthday."""
    chance = 1
    for k in range(1, people):
        chance = chance * (365 - k) / 365
    return chance
---
With 23 people the exact chance of a shared birthday is 0.5073. The simulation came close with 1,000 trials, and would come closer with more. The formula is exact but needed a clever idea; the simulation needed only the rules of the problem.
```

## 8.

Which part of the course would you reach for?

1. A shop's prices in euro, and the same prices after a 10% rise and a
   €2 delivery charge, for 500 products at once.
2. The chance that a queue of trucks at a port grows longer during a
   busy week.
3. The fewest changes of bus from one side of a city to the other.
4. Which of two writers wrote an unsigned letter.
5. A 3D model of a building, drawn on a flat screen from where a
   visitor stands.

<details class="dl-answer"><summary>answer</summary>

1. A list, and a comprehension or a loop, or NumPy for all 500 at once.
2. A simulation of the queue, run many times with many seeds.
3. Breadth-first search on a graph of bus stops.
4. A chain from each writer's books, and the score each gives the
   letter.
5. Matrices: a move and a turn for the camera, then a projection and
   the divide by depth.

</details>

## 9. In your world

How often does "the" appear in your book? You could count every word.
Or you could look at 500 words chosen at random, and estimate. Can you
write `estimate_share(words, target, n, seed)`? It sets the seed, picks
`n` words with `random.choice(words)`, and returns the share of them
that equal `target` when put in lower case.

<div class="dl-world" data-world="the-time-machine">

```python exec
id: in-your-world-1--the-time-machine
raw = await load_text("the-time-machine.txt")
start = raw.find("*** START OF")
end = raw.find("*** END OF")
words = raw[raw.index("\n", start):end].split()
exact = sum(1 for word in words if word.lower() == "the") / len(words)
print("exact:", round(exact, 4))


def estimate_share(words, target, n, seed):
    """The share of n randomly chosen words that equal target, in lower case."""
    # Your code here.
```

```hint
Set the seed, then loop `n` times, picking a word with
`random.choice(words)` each time, and count the ones whose `.lower()`
equals `target`.
```

```inputs
estimate_share(words, "the", 500, seed=1)
estimate_share(words, "the", 5000, seed=1)
```

```solution
def estimate_share(words, target, n, seed):
    """The share of n randomly chosen words that equal target, in lower case."""
    random.seed(seed)
    hits = 0
    for _ in range(n):
        if random.choice(words).lower() == target:
            hits += 1
    return hits / n
---
The whole book gives 0.0695. 500 words give 0.054, and 5,000 give 0.064: the larger sample is closer, as more darts were. A computer can count every word of a book, so here the sample is only practice. Sampling matters when counting everything is impossible: a poll before an election, or a survey of the fish on a reef.
```

</div>

<div class="dl-world" data-world="dracula">

```python exec
id: in-your-world-1--dracula
raw = await load_text("dracula.txt")
start = raw.find("*** START OF")
end = raw.find("*** END OF")
words = raw[raw.index("\n", start):end].split()
exact = sum(1 for word in words if word.lower() == "the") / len(words)
print("exact:", round(exact, 4))


def estimate_share(words, target, n, seed):
    """The share of n randomly chosen words that equal target, in lower case."""
    # Your code here.
```

```hint
Set the seed, then loop `n` times, picking a word with
`random.choice(words)` each time, and count the ones whose `.lower()`
equals `target`.
```

```inputs
estimate_share(words, "the", 500, seed=1)
estimate_share(words, "the", 5000, seed=1)
```

```solution
def estimate_share(words, target, n, seed):
    """The share of n randomly chosen words that equal target, in lower case."""
    random.seed(seed)
    hits = 0
    for _ in range(n):
        if random.choice(words).lower() == target:
            hits += 1
    return hits / n
---
The whole book gives 0.0484. 500 words give 0.044, and 5,000 give 0.0458: the larger sample is closer, as more darts were. A computer can count every word of a book, so here the sample is only practice. Sampling matters when counting everything is impossible: a poll before an election, or a survey of the fish on a reef.
```

</div>

<div class="dl-world" data-world="dubliners">

```python exec
id: in-your-world-1--dubliners
raw = await load_text("dubliners.txt")
start = raw.find("*** START OF")
end = raw.find("*** END OF")
words = raw[raw.index("\n", start):end].split()
exact = sum(1 for word in words if word.lower() == "the") / len(words)
print("exact:", round(exact, 4))


def estimate_share(words, target, n, seed):
    """The share of n randomly chosen words that equal target, in lower case."""
    # Your code here.
```

```hint
Set the seed, then loop `n` times, picking a word with
`random.choice(words)` each time, and count the ones whose `.lower()`
equals `target`.
```

```inputs
estimate_share(words, "the", 500, seed=1)
estimate_share(words, "the", 5000, seed=1)
```

```solution
def estimate_share(words, target, n, seed):
    """The share of n randomly chosen words that equal target, in lower case."""
    random.seed(seed)
    hits = 0
    for _ in range(n):
        if random.choice(words).lower() == target:
            hits += 1
    return hits / n
---
The whole book gives 0.0595. 500 words give 0.056, and 5,000 give 0.0566: the larger sample is closer, as more darts were. A computer can count every word of a book, so here the sample is only practice. Sampling matters when counting everything is impossible: a poll before an election, or a survey of the fish on a reef.
```

</div>

<div class="dl-world" data-world="irish-fairy-tales">

```python exec
id: in-your-world-1--irish-fairy-tales
raw = await load_text("irish-fairy-tales.txt")
start = raw.find("*** START OF")
end = raw.find("*** END OF")
words = raw[raw.index("\n", start):end].split()
exact = sum(1 for word in words if word.lower() == "the") / len(words)
print("exact:", round(exact, 4))


def estimate_share(words, target, n, seed):
    """The share of n randomly chosen words that equal target, in lower case."""
    # Your code here.
```

```hint
Set the seed, then loop `n` times, picking a word with
`random.choice(words)` each time, and count the ones whose `.lower()`
equals `target`.
```

```inputs
estimate_share(words, "the", 500, seed=1)
estimate_share(words, "the", 5000, seed=1)
```

```solution
def estimate_share(words, target, n, seed):
    """The share of n randomly chosen words that equal target, in lower case."""
    random.seed(seed)
    hits = 0
    for _ in range(n):
        if random.choice(words).lower() == target:
            hits += 1
    return hits / n
---
The whole book gives 0.0585. 500 words give 0.066, and 5,000 give 0.061: the larger sample is closer, as more darts were. A computer can count every word of a book, so here the sample is only practice. Sampling matters when counting everything is impossible: a poll before an election, or a survey of the fish on a reef.
```

</div>

<div class="dl-world" data-world="treasure-island">

```python exec
id: in-your-world-1--treasure-island
raw = await load_text("treasure-island.txt")
start = raw.find("*** START OF")
end = raw.find("*** END OF")
words = raw[raw.index("\n", start):end].split()
exact = sum(1 for word in words if word.lower() == "the") / len(words)
print("exact:", round(exact, 4))


def estimate_share(words, target, n, seed):
    """The share of n randomly chosen words that equal target, in lower case."""
    # Your code here.
```

```hint
Set the seed, then loop `n` times, picking a word with
`random.choice(words)` each time, and count the ones whose `.lower()`
equals `target`.
```

```inputs
estimate_share(words, "the", 500, seed=1)
estimate_share(words, "the", 5000, seed=1)
```

```solution
def estimate_share(words, target, n, seed):
    """The share of n randomly chosen words that equal target, in lower case."""
    random.seed(seed)
    hits = 0
    for _ in range(n):
        if random.choice(words).lower() == target:
            hits += 1
    return hits / n
---
The whole book gives 0.0634. 500 words give 0.06, and 5,000 give 0.0602: the larger sample is closer, as more darts were. A computer can count every word of a book, so here the sample is only practice. Sampling matters when counting everything is impossible: a poll before an election, or a survey of the fish on a reef.
```

</div>

## 10. Make it: two bots, and a test

The cell builds two bots from your book: A keys on one word, and B on
two. Each writes a 30-word passage from any seed you give it.

```python exec
id: mixed-computational-methods-two-bots
def chain_from(words, order):
    chain = {}
    for i in range(len(words) - order):
        key = tuple(words[i:i + order])
        chain.setdefault(key, {})
        chain[key][words[i + order]] = chain[key].get(words[i + order], 0) + 1
    return chain


def write(chain, seed, length=30):
    random.seed(seed)
    order = len(next(iter(chain)))
    result = list(random.choice(list(chain)))
    while len(result) < length:
        key = tuple(result[-order:])
        if key not in chain:
            result.extend(random.choice(list(chain)))
            continue
        followers = chain[key]
        result.append(random.choices(list(followers), weights=list(followers.values()))[0])
    return result[:length]


bot_a = chain_from(words, 1)
bot_b = chain_from(words, 2)
print("A:", " ".join(write(bot_a, seed=1)))
print("B:", " ".join(write(bot_b, seed=1)))
```

Now make a test: a function that reads a passage and answers `"A"` or
`"B"`. Choose it by looking at passages from seeds 0 to 49. Then score
it on seeds 50 to 99, which played no part in choosing it. How often
is it right? What does a test that always says "A" score?

```python exec
id: mixed-computational-methods-your-test
# Your test, and its score on seeds 50 to 99.
```

The Machine Learning course takes this further, in [Make it: two bots,
and a test that tells them
apart](tutorial:two-bots-and-a-test): harder pairs of bots, and tests
that stop working when the bots get closer.
