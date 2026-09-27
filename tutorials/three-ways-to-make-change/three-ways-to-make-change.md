---
title: "Making change: brute force, memoization and greedy algorithms"
year: "2026-2027"
version: 2026.09.27.1
covers:
  trying-every-combination:
    covers: [CMPS-LO9]
  remembering-what-we-already-worked-out:
    covers: [CMPS-LO9]
    touches: [CMPS-LO5]
  the-greedy-shortcut:
    covers: [CMPS-LO9]
    touches: [CMPS-LO5]
  how-the-work-grows:
    covers: [CMPS-LO5]
  how-many-ways:
    covers: [CMPS-LO9]
  choosing-a-strategy:
    covers: [CMPS-LO9]
worlds:
  mazes-and-dungeons: A dungeon merchant who takes gems as payment.
  maps-and-networks: A post office with stamps of odd values.
  collections: A collection of the old Irish coins, from before 1971.
  puzzles: A dragon kingdom with coins of its own.
---

# Making change: brute force, memoization and greedy algorithms

Here is a small problem. You have a target amount, and tokens of a few
different values. What is the fewest number of tokens that add up to the
amount?

There is more than one way to solve this. On this page we try
three. Each one makes a different trade-off between being fast and being
certain of the right answer. The same trade-off appears in problems far
bigger than making change.

## Trying every combination

We start with tokens worth `1`, `3` and `4`. How few tokens can make `6`?
Try it in your head before you run the cell.

```python exec
id: trying-every-combination-1
TOKENS = [1, 3, 4]
calls = {"brute force": 0, "cached": 0}    # for counting calls, later on this page

def fewest_tokens_brute_force(amount, denominations):
    """Fewest tokens for amount, trying every denomination at every step."""
    calls["brute force"] += 1
    if amount == 0:
        return 0
    best = None
    for coin in denominations:
        if coin <= amount:
            rest = fewest_tokens_brute_force(amount - coin, denominations)
            if rest is not None and (best is None or rest + 1 < best):
                best = rest + 1
    return best

print(fewest_tokens_brute_force(6, TOKENS))
```

Look at the line inside the loop. `fewest_tokens_brute_force` calls
itself, each time with a smaller amount. A function that calls itself is
using recursion. It stops when the amount reaches `0`, because the
first `if` returns `0` without calling itself again. If you have not met
recursion before,
[Recursion: finding every file in a folder tree](tutorial:finding-everything-inside-a-folder)
explains it step by step.

The function returns `None` when there is no way to make the amount. The
long `if` inside the loop keeps a new answer only when there is one
(`rest is not None`), and only when it beats the best answer so far.

The idea is the simplest one there is:

1. Try every token at every step.
2. Follow each choice all the way down to zero.
3. Keep the path that used the fewest tokens.

This is called *brute force*. Brute force is a strategy that checks every
possibility, without trying to reason about which ones are worth
checking. It is slow. But it is reliable. It can never miss the real
answer, because it never skips a possibility.

### Your turn

1. Call `fewest_tokens_brute_force` with a target of `10`.
2. Check the result by hand. Which three tokens from `[1, 3, 4]` add up
   to `10`?

```python exec
id: trying-every-combination-2
```

## Remembering what we already worked out

Brute force repeats itself. Think about how it reaches `6`:

- If it takes a `4`, `2` is left. So it asks, "What is the fewest tokens
  for `2`?"
- If it takes a `1` and then a `3`, `2` is left too. It asks the same
  question.
- If it takes a `3` and then a `1`, `2` is left again. It asks the same
  question again.

Each time, it finds the answer to that question from the beginning.
And each time, the answer is the same.

![The call tree from six. Three of its branches arrive at the amount two,
each by a different first move, and each one is solved again from the
start.](repeated-question.svg)

The picture shows only the first two moves. If we continued, `2` would
appear a fourth time, after four `1`s.

A *cache* is a place to store an answer the first time we find it.
When the same question appears again, we look up the answer, instead of
finding it again.

The function below keeps its cache in a dictionary, as in
[Dictionaries: looking things up by name](tutorial:looking-things-up-by-name).
Each key is an amount, and each value is the fewest tokens for that
amount.

```python exec
id: remembering-what-we-already-worked-out-1
def fewest_tokens_cached(amount, denominations, cache=None):
    calls["cached"] += 1
    if cache is None:
        cache = {}
    if amount == 0:
        return 0
    if amount in cache:
        return cache[amount]
    best = None
    for coin in denominations:
        if coin <= amount:
            rest = fewest_tokens_cached(amount - coin, denominations, cache)
            if rest is not None and (best is None or rest + 1 < best):
                best = rest + 1
    cache[amount] = best
    return best

print(fewest_tokens_cached(6, TOKENS))
```

We store each answer the first time we find it, so that we can look up
a repeated question. This is called *memoization*. Memoization does not
change the answer the function returns. It is exactly as correct as
brute force. It only changes how much work the function does.

Why is it safe to trust a stored answer? It is safe because the fewest
tokens for an amount depends only on that amount and the token values. It does not
matter how we got there. "What is the fewest for 2?" has the same answer
whether we reached 2 from 6 by taking a 4, or from 5 by taking a 3. So
the first time we find the answer for 2, we have found it for every
path that ever reaches 2.

That is also when a cache would *not* be safe. Suppose the till held
only three `3`s. Then the fewest for 2 would depend on how many `3`s
the path had used up already, and an answer stored on one path could be
wrong on another. A cache is safe when the answer depends only on the
question asked, and on nothing that changes along the way.

How much work does it save? Timing the two would depend on the
computer, so the next cell counts something that does not: how many
times each function is called. The `calls` dictionary counts them.

```python exec
id: remembering-what-we-already-worked-out-2
for amount in [10, 12, 14, 16, 18, 20, 22, 24]:
    calls["brute force"] = 0
    calls["cached"] = 0
    fewest_tokens_brute_force(amount, TOKENS)
    fewest_tokens_cached(amount, TOKENS)
    print(f"amount={amount}: brute force {calls['brute force']:>6} calls, cached {calls['cached']} calls")
```

```predict
type: number

For an amount of 10, the cached version makes 26 calls, and for 12 it
makes 32. How many will it make for 24?
```

Brute force walks every path of choices, and meets the same smaller
amounts again and again along different paths. For an amount of 20 it
calls itself 20,736 times. The cached version finds each amount from 0
to 20 once, and after that only looks it up. That makes 56 calls.

### Your turn

1. Count the calls `fewest_tokens_cached` makes for `amount=100`.
2. Now think about `fewest_tokens_brute_force` at the same amount. Before
   you run anything, predict: would it finish in under a second? Why?

Be careful with step 2. If brute force keeps growing the way the table
shows, it would take far longer than anyone would wait. You do not need
to run it to answer the question.

```python exec
id: remembering-what-we-already-worked-out-3
hint: Set calls["cached"] = 0, call fewest_tokens_cached(100, TOKENS), then print calls["cached"]. For brute force, look at how many times as many calls each step of 2 makes in the table above.
```

## How the work grows

Look at the table again, down each column. Every time the amount goes
up by 2, brute force makes about 2.6 times as many calls as before. The
cached version makes 6 more.

```python exec
id: how-the-work-grows-1
import matplotlib.pyplot as plt

amounts = list(range(2, 25, 2))
brute_calls = []
cached_calls = []
for amount in amounts:
    calls["brute force"] = 0
    calls["cached"] = 0
    fewest_tokens_brute_force(amount, TOKENS)
    fewest_tokens_cached(amount, TOKENS)
    brute_calls.append(calls["brute force"])
    cached_calls.append(calls["cached"])

plt.plot(amounts, brute_calls, marker="o", label="brute force")
plt.plot(amounts, cached_calls, marker="o", label="cached")
plt.yscale("log")
plt.xlabel("amount")
plt.ylabel("calls (log scale)")
plt.legend()
```

The scale up the side is a *log scale*: each step up multiplies by 10,
so a count that multiplies by the same amount each time draws a
straight line. Brute force's line climbs steadily across the page.

These two ways of growing have names. Brute force's count is
multiplied by a fixed amount for each step up in the size of the
problem: that is *exponential* growth, and it overwhelms any computer
soon. The cached count grows by a fixed amount for each step: that is
*linear* growth, and doubling the amount only doubles the work. At 100,
the cached version makes 296 calls. Brute force would make about
$10^{21}$.

Counting steps like this, and watching how the count grows as the
problem gets bigger, is how people compare algorithms without a
stopwatch. [Searching a list: linear and binary
search](tutorial:finding-things) counted the steps of two searches in
the same way.

## The greedy shortcut

There is a third way, and it does not check every possibility at all.
At every step, take the largest token that still fits. Repeat until
nothing is left.

What do you think it will say for `6`?

```python exec
id: the-greedy-shortcut-1
def fewest_tokens_greedy(amount, denominations):
    """Fewest tokens, always taking the largest that fits."""
    remaining = amount
    count = 0
    for coin in sorted(denominations, reverse=True):
        while remaining >= coin:
            remaining -= coin
            count += 1
    return count if remaining == 0 else None

print(fewest_tokens_greedy(6, TOKENS))
```

This is a *heuristic*. A heuristic is a simple rule that finds an
answer quickly. It never goes back to check whether an earlier choice
was really the best one.

`fewest_tokens_greedy(6, TOKENS)` returns `3`: a `4` and two `1`s. But
the cached version already showed that the real fewest is `2`: two `3`s.
Greedy made a reasonable choice when it took the biggest token first.
But after that choice, it could never reach the best combination.

A strategy that always takes whatever looks best right now, and never
goes back, is called a *greedy* algorithm.

Does greedy go wrong with real coins? Euro coins in cents are `1`, `2`,
`5`, `10`, `20` and `50`. Let's try the same greedy shortcut with them.

```python exec
id: the-greedy-shortcut-2
ORDINARY_COINS = [1, 2, 5, 10, 20, 50]   # euro coins, in cents

for amount in [6, 41, 63]:
    greedy = fewest_tokens_greedy(amount, ORDINARY_COINS)
    guaranteed = fewest_tokens_cached(amount, ORDINARY_COINS)
    print(f"amount={amount}: greedy={greedy}, guaranteed correct={guaranteed}")
```

For every amount tried here, the fast shortcut and the slower, certain
method agree. That is a property of this set of coin values. It is not
true of greedy shortcuts in general. Here is a kingdom that mints coins
of 1, 7 and 10 crowns.

```python exec
id: the-greedy-shortcut-4
KINGDOM_COINS = [1, 7, 10]

for amount in [14, 15, 21]:
    greedy = fewest_tokens_greedy(amount, KINGDOM_COINS)
    guaranteed = fewest_tokens_cached(amount, KINGDOM_COINS)
    print(f"amount={amount}: greedy={greedy}, guaranteed correct={guaranteed}")
```

For 14 crowns, greedy takes a 10 and four 1s: five coins, where two 7s
would do. For 15, six coins where three would do. For 21 the two
agree. A greedy shortcut can be wrong, by a lot, and nothing tells you
when it is.

### Your turn

Using `TOKENS = [1, 3, 4]`, look for more amounts where the greedy
shortcut and the cached method disagree.

1. Start from `6`, where we already know they disagree, and try the
   amounts near it.
2. Can you find an amount where they disagree by more than one token?
3. What do the amounts where they disagree have in common?

```python exec
id: the-greedy-shortcut-3
hint: A for loop over range(1, 41) can print the amount, the greedy answer and the cached answer side by side. Print only the amounts where the two answers are different.
```

With these tokens, the two methods never disagree by more than one
token. They disagree at `6`, `10`, `14`, `18` and so on. These are the
amounts that leave `2` after greedy has taken all the `4`s it can. For
the last `6` of the amount, greedy uses a `4` and two `1`s, where two
`3`s would do. The kingdom's coins make greedy much worse.

## How many ways?

A different question: how many different handfuls of tokens make the
amount? Two handfuls with the same tokens in a different order count
as one. List the handfuls for `6` with tokens of 1, 3 and 4 before you
run the cell.

```python exec
id: how-many-ways-1
def count_ways(amount, coins):
    """How many different handfuls of coins make the amount. Order does not matter."""
    if amount == 0:
        return 1
    if amount < 0 or not coins:
        return 0
    return count_ways(amount - coins[0], coins) + count_ways(amount, coins[1:])

print(count_ways(6, TOKENS))
```

```predict
type: number

How many handfuls make 6?
```

Four: six 1s; three 1s and a 3; two 3s; two 1s and a 4. The last line
of the function splits every handful into two kinds. Either it uses at
least one of the first coin, `coins[0]`, and then the rest of it makes
`amount - coins[0]`. Or it uses none of the first coin, and then it is
made from `coins[1:]` alone. No handful is both kinds, so nothing is
counted twice.

The same questions come back again and again, so a cache helps here
too. What should the key be? The answer depends on the amount and on
which coins are still allowed, and on nothing else, so those two make a
safe key.

```python exec
id: how-many-ways-2
def count_ways_cached(amount, coins, cache=None):
    """count_ways, remembering each (amount, coins left) it has answered."""
    if cache is None:
        cache = {}
    if amount == 0:
        return 1
    if amount < 0 or not coins:
        return 0
    key = (amount, len(coins))
    if key not in cache:
        cache[key] = (count_ways_cached(amount - coins[0], coins, cache)
                      + count_ways_cached(amount, coins[1:], cache))
    return cache[key]

print(count_ways_cached(100, ORDINARY_COINS))
```

There are 4,562 different handfuls of euro coins, up to 50 cent, that
make one euro. `len(coins)` is enough to say which coins are left,
because `coins[1:]` always drops from the front: the same length means
the same coins.

## Choosing a strategy

Three strategies solved the same problem. None of them is better than the
others in every way.

| Strategy | Speed | Always right? |
|---|---|---|
| Brute force | slow, and much slower for bigger amounts | yes |
| Memoization (caching) | fast | yes |
| Greedy | fastest: one pass, no waiting | no |

Brute force is the strategy to try first. It is slow, but it is never
wrong, and for a small enough amount, slow does not matter.

Caching keeps brute force's guarantee. It also removes its worst cost,
because it never does the same work twice. So it is usually the
strategy to build once brute force starts to feel too slow.

The greedy shortcut loses the guarantee. It is the fastest of the
three. Its worst case is a wrong answer, not a slow one, and it gives
that wrong answer with just as much confidence as a right one.

Which one should a real program use? That depends on what it is being
asked to do. A till that must never give anyone the wrong change needs
the guarantee that brute force or caching gives. A system that gives a
rough suggestion, which a person will check anyway, can often accept the
greedy shortcut's risk, in return for its speed.

### Your turn

A vending machine gives change in euro coins, `[1, 2, 5, 10, 20, 50]`
cents, after every purchase, many times a minute. Which of the three
strategies would you use? Why?

## Your world

Can you write `greedy_gaps(limit, coins)`? It returns every amount from
1 to `limit` where the greedy shortcut uses more coins than the fewest
possible.

<div class="dl-world" data-world="mazes-and-dungeons">

A merchant deep in the dungeon takes gems worth 1, 5, 6 and 9 gold. For which amounts does greedy use too many?

```python exec
id: your-world-1--mazes-and-dungeons
DUNGEON_GEMS = [1, 5, 6, 9]


def greedy_gaps(limit, coins):
    """Every amount up to limit where greedy uses more coins than it needs."""
    # Your code here.
```

```hint
For each amount in `range(1, limit + 1)`, compare
`fewest_tokens_greedy(amount, coins)` with
`fewest_tokens_cached(amount, coins)`, and keep the amounts where they
differ.
```

```inputs
greedy_gaps(30, DUNGEON_GEMS)
len(greedy_gaps(100, DUNGEON_GEMS))
greedy_gaps(100, [1, 2, 5, 10, 20, 50])
```

```solution
def greedy_gaps(limit, coins):
    """Every amount up to limit where greedy uses more coins than it needs."""
    return [amount for amount in range(1, limit + 1)
            if fewest_tokens_greedy(amount, coins) != fewest_tokens_cached(amount, coins)]
---
Up to 30 gold, greedy pays too many gems for ten amounts, starting at 11: a 9 and two 1s, where a 5 and a 6 would do. Up to 100, forty amounts. The euro coins never trip greedy up, at any amount up to 100.
```

</div>

<div class="dl-world" data-world="maps-and-networks">

A post office sells stamps worth 1, 4, 9 and 16 cents: the square numbers. For which amounts does greedy use too many?

```python exec
id: your-world-1--maps-and-networks
STAMPS = [1, 4, 9, 16]


def greedy_gaps(limit, coins):
    """Every amount up to limit where greedy uses more coins than it needs."""
    # Your code here.
```

```hint
For each amount in `range(1, limit + 1)`, compare
`fewest_tokens_greedy(amount, coins)` with
`fewest_tokens_cached(amount, coins)`, and keep the amounts where they
differ.
```

```inputs
greedy_gaps(30, STAMPS)
len(greedy_gaps(100, STAMPS))
greedy_gaps(100, [1, 2, 5, 10, 20, 50])
```

```solution
def greedy_gaps(limit, coins):
    """Every amount up to limit where greedy uses more coins than it needs."""
    return [amount for amount in range(1, limit + 1)
            if fewest_tokens_greedy(amount, coins) != fewest_tokens_cached(amount, coins)]
---
For 12 cents, greedy sticks a 9 and three 1s on the letter, where three 4s would do. Up to 30, seven amounts go wrong; up to 100, thirty-eight. The euro coins never trip greedy up, at any amount up to 100.
```

</div>

<div class="dl-world" data-world="collections">

Before Ireland's coins went decimal in 1971, there were 12 pence in a shilling. The coins included the penny, the threepence and the sixpence, the shilling, the florin (24 pence) and the half crown (30 pence). For which amounts does greedy use too many?

```python exec
id: your-world-1--collections
OLD_COINS = [1, 3, 6, 12, 24, 30]


def greedy_gaps(limit, coins):
    """Every amount up to limit where greedy uses more coins than it needs."""
    # Your code here.
```

```hint
For each amount in `range(1, limit + 1)`, compare
`fewest_tokens_greedy(amount, coins)` with
`fewest_tokens_cached(amount, coins)`, and keep the amounts where they
differ.
```

```inputs
greedy_gaps(60, OLD_COINS)
len(greedy_gaps(100, OLD_COINS))
greedy_gaps(100, [1, 2, 5, 10, 20, 50])
```

```solution
def greedy_gaps(limit, coins):
    """Every amount up to limit where greedy uses more coins than it needs."""
    return [amount for amount in range(1, limit + 1)
            if fewest_tokens_greedy(amount, coins) != fewest_tokens_cached(amount, coins)]
---
Greedy does well with the old coins until 48 pence: there it takes a half crown, a shilling and a sixpence, where two florins would do. Six amounts in a row go wrong, from 48 to 53, and twelve up to 100. The half crown, at 30, is what trips it up. The euro coins never do, at any amount up to 100.
```

</div>

<div class="dl-world" data-world="puzzles">

The dragon kingdom mints coins worth 1, 6 and 10 scales. For which amounts does greedy use too many?

```python exec
id: your-world-1--puzzles
DRAGON_COINS = [1, 6, 10]


def greedy_gaps(limit, coins):
    """Every amount up to limit where greedy uses more coins than it needs."""
    # Your code here.
```

```hint
For each amount in `range(1, limit + 1)`, compare
`fewest_tokens_greedy(amount, coins)` with
`fewest_tokens_cached(amount, coins)`, and keep the amounts where they
differ.
```

```inputs
greedy_gaps(30, DRAGON_COINS)
len(greedy_gaps(100, DRAGON_COINS))
greedy_gaps(100, [1, 2, 5, 10, 20, 50])
```

```solution
def greedy_gaps(limit, coins):
    """Every amount up to limit where greedy uses more coins than it needs."""
    return [amount for amount in range(1, limit + 1)
            if fewest_tokens_greedy(amount, coins) != fewest_tokens_cached(amount, coins)]
---
Greedy first goes wrong at 12 scales: a 10 and two 1s, where two 6s would do. Up to 30, twelve amounts go wrong, and up to 100, fifty-four: more than half. The euro coins never trip greedy up, at any amount up to 100.
```

</div>

## Where to read more

Cormen, T. H., Leiserson, C. E., Rivest, R. L. and Stein, C. (2022).
*Introduction to Algorithms* (4th ed.). MIT Press. Chapter 14 covers
dynamic programming, the general name for the caching strategy this page
builds. Chapter 15 covers greedy algorithms, including exactly when a
greedy choice is provably safe.

Spanning Tree (2020). *How to Count Dice Rolls: An Introduction to Dynamic
Programming.* <https://www.youtube.com/watch?v=oifN-YVlrq8>. It counts the
ways dice can add to a total. First it tries everything, then it
remembers answers in a table. These are the same two steps this page
takes with coins. The video is about nine minutes long.
