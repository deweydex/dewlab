---
title: "Making change: brute force, memoization and greedy algorithms"
year: "2026-2027"
version: 2026.09.22.1
covers:
  trying-every-combination:
    covers: [CMPS-LO9]
  remembering-what-we-already-worked-out:
    covers: [CMPS-LO9]
    touches: [CMPS-LO5]
  the-greedy-shortcut:
    covers: [CMPS-LO9]
    touches: [CMPS-LO5]
  choosing-a-strategy:
    covers: [CMPS-LO9]
---

# Making change: brute force, memoization and greedy algorithms

Here is a small problem. You have a target amount, and tokens of a few
different values. What is the fewest number of tokens that add up to the
amount?

There is more than one honest way to solve this. On this page we try
three. Each one makes a different trade-off between being fast and being
certain of the right answer. The same trade-off comes up in problems far
bigger than making change.

## Trying Every Combination

We start with tokens worth `1`, `3` and `4`. How few tokens can make `6`?
Try it in your head before you run the cell.

```python exec
id: trying-every-combination-1
TOKENS = [1, 3, 4]

def fewest_tokens_brute_force(amount, denominations):
    """Fewest tokens for amount, trying every denomination at every step."""
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

Look at the line inside the loop: `fewest_tokens_brute_force` calls
itself, each time with a smaller amount. A function that calls itself is
using recursion. It stops when the amount reaches `0`, because the
first `if` returns `0` without calling itself again. If you have not met
recursion before,
[Recursion: finding every file in a folder tree](tutorial:finding-everything-inside-a-folder)
builds it up step by step.

The function returns `None` when there is no way to make the amount. The
long `if` inside the loop keeps a new answer only when there is one
(`rest is not None`), and only when it beats the best answer so far.

The idea is the simplest one there is:

1. Try every token at every step.
2. Follow each choice all the way down to zero.
3. Keep the path that used the fewest tokens.

This is called *brute force*. Brute force is a strategy that checks every
possibility, without trying to reason about which ones are worth
checking. It is slow. But it is reliable: it can never miss the real
answer, because it never skips a possibility.

### Your turn

1. Call `fewest_tokens_brute_force` with a target of `10`.
2. Check the result by hand. Which three tokens from `[1, 3, 4]` add up
   to `10`?

```python exec
id: trying-every-combination-2
```

## Remembering What We Already Worked Out

Brute force repeats itself. Think about how it reaches `6`:

- Taking a `4` leaves `2`. So it asks, "What is the fewest tokens for
  `2`?"
- Taking a `1` and then a `3` also leaves `2`. It asks the same question.
- Taking a `3` and then a `1` leaves `2` too. The same question again.

Each time, it works out the answer to that question from the beginning.
And each time, the answer is the same.

![The call tree from six. Three of its branches arrive at the amount two,
each by a different first move, and each one is worked out again from
scratch.](repeated-question.svg)

The picture shows only the first two moves. If we continued, `2` would
come up a fourth time, by taking four `1`s.

A *cache* is a place to store an answer the first time we work it out.
When the same question comes up again, we look up the answer, instead of
working it out again.

The function below keeps its cache in a dictionary, as in
[Dictionaries: looking things up by name](tutorial:looking-things-up-by-name).
Each key is an amount, and each value is the fewest tokens for that
amount.

```python exec
id: remembering-what-we-already-worked-out-1
def fewest_tokens_cached(amount, denominations, cache=None):
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

Storing each answer the first time we work it out, so that a repeated
question is looked up, is called *memoization*. Memoization does not
change which answer comes back. It is exactly as correct as brute force.
The only thing it changes is how much work it takes to get there.

Why is it safe to trust a stored answer? Because the fewest tokens for
an amount depends only on that amount and the token values. It does not
matter how we got there. "What is the fewest for 2?" has the same answer
whether we reached 2 from 6 by taking a 4, or from 5 by taking a 3. So
the first time we work out the answer for 2, we have worked it out for
every path that ever reaches 2.

How much work does it save? The next cell times both functions on larger
and larger amounts.

```python exec
id: remembering-what-we-already-worked-out-2
import time

for amount in [10, 15, 20, 22, 24]:
    start = time.perf_counter()
    fewest_tokens_brute_force(amount, TOKENS)
    brute_time = time.perf_counter() - start

    start = time.perf_counter()
    fewest_tokens_cached(amount, TOKENS)
    cached_time = time.perf_counter() - start

    print(f"amount={amount}: brute force {brute_time:.4f}s, cached {cached_time:.6f}s")
```

Each time the amount goes up by 2, brute force takes two or three times
as long. The cached version hardly changes. The two do not do the same
work. Brute force walks every path of choices, and meets the same
smaller amounts again and again along different paths. For an amount of
20 it calls itself 20,736 times. The cached version works out each
amount from 0 to 20 once, and after that only looks it up: 56 calls.

### Your turn

1. Time `fewest_tokens_cached` at `amount=100`.
2. Now think about `fewest_tokens_brute_force` at the same amount. Before
   you run anything, predict: would it finish in under a second? Why?

Be careful with step 2. If brute force keeps growing the way the table
shows, it would take far longer than anyone would wait. You do not need
to run it to answer the question.

```python exec
id: remembering-what-we-already-worked-out-3
hint: You do not need to pass a cache={} argument. The function makes a new, empty cache on each call. Use time.perf_counter() before and after the call, as the cell above does.
```

## The Greedy Shortcut

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

This is a *heuristic*. A heuristic is a rule of thumb that gets to an
answer quickly. It never looks back to check whether an earlier choice
was really the best one.

`fewest_tokens_greedy(6, TOKENS)` returns `3`: a `4` and two `1`s. But
the cached version already showed that the real fewest is `2`: two `3`s.
Taking the biggest token first was not exactly wrong. But it closed off
the one combination that would have won.

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
true of greedy shortcuts in general. The `[1, 3, 4]` tokens above show
that a greedy shortcut can be wrong, and nothing tells you when it is.

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
token. They disagree at `6`, `10`, `14`, `18` and so on: every amount
that leaves `2` after greedy has taken all the `4`s it can. For the last
`6` of the amount, greedy uses a `4` and two `1`s, where two `3`s would
do. Other token values can make greedy much worse, as the practice
page shows.

## Choosing a Strategy

Three strategies solved the same problem. None of them is better than the
others in every way.

| Strategy | Speed | Always right? |
|---|---|---|
| Brute force | slow, and much slower for bigger amounts | yes |
| Memoization (caching) | fast | yes |
| Greedy | fastest: one pass, no waiting | no |

Brute force is the strategy to try first. It is slow, but it is never
wrong, and for a small enough amount, slow does not matter.

Caching keeps brute force's guarantee, and removes its worst cost: doing
the same work again and again. So it is usually the strategy to build
once brute force starts to feel too slow.

The greedy shortcut gives up the guarantee. It is the fastest of the
three, but its worst case is not slowness. Its worst case is a wrong
answer, given with just as much confidence as a right one.

Which one should a real program use? That depends on what it is being
asked to do. A till that must never give anyone the wrong change needs
the guarantee that brute force or caching gives. A system that gives a
rough suggestion, which a person will check anyway, can often accept the
greedy shortcut's risk, in return for its speed.

### Your turn

A vending machine gives change in euro coins, `[1, 2, 5, 10, 20, 50]`
cents, after every purchase, many times a minute. Which of the three
strategies would you build it around? Why?

## Where to Read More

Cormen, T. H., Leiserson, C. E., Rivest, R. L. and Stein, C. (2022).
*Introduction to Algorithms* (4th ed.). MIT Press. Chapter 14 covers
dynamic programming, the general name for the caching strategy this page
builds. Chapter 15 covers greedy algorithms, including exactly when a
greedy choice is provably safe.

Spanning Tree (2020). *How to Count Dice Rolls: An Introduction to Dynamic
Programming.* <https://www.youtube.com/watch?v=oifN-YVlrq8>. Counting the
ways dice can add to a total, first by trying everything, then by
remembering answers in a table: the same two steps this page takes with
coins. About nine minutes.
