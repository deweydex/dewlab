---
title: "Three Ways to Make Change"
slug: three-ways-to-make-change
module: computational-methods
module_title: "Computational Methods"
year: "2026-2027"
series: algorithms
version: 2026.09.05.1
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

# Three Ways to Make Change

Give someone a target amount and a handful of token values, and ask for the
fewest tokens that add up to it. This is one small problem, but there is more
than one honest way to solve it. Each way makes a different trade-off between
being fast and being certain. That trade-off is worth understanding on its
own — it shows up again in far bigger problems than making change.

## Trying Every Combination

Start with tokens worth `1`, `3`, and `4`, and a target amount to reach.

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

The idea is the simplest one available. Try every token at every step,
follow each choice all the way down to zero, and keep whichever path used
the fewest tokens. This is *brute force*: a strategy that checks every
possibility rather than reasoning about which ones are worth checking. It
is slow work, but it is honest work: it can never miss the real answer,
because it never skips a possibility.

### Your turn

Call `fewest_tokens_brute_force` with a target of `10` and confirm the result
by hand: which three tokens from `[1, 3, 4]` add up to `10`?

```python exec
id: trying-every-combination-2
```

## Remembering What We Already Worked Out

Brute force repeats itself. Reaching `6` by way of `3` then `3` asks, along
the way, "what is the fewest tokens for `3`?" Reaching `6` by way of `4`
then `1` then `1` asks that exact question too, then asks "what is the
fewest tokens for `2`?" as well. Each of those two questions gets answered
more than once, with the same answer every time.

A *cache* is a place to store an answer the first time it is worked out. A
repeated question can then be answered by looking it up, instead of
reworking it.

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

Storing an answer the first time it is worked out, so a repeat is looked up
instead, is called *memoization*. It changes nothing about which answer
comes back, and stays exactly as correct as brute force. What changes is
only how much work it costs to get there.

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

Brute force's time roughly doubles with every couple of tokens added to the
target. The cached version barely moves. Both still check the same
possibilities in principle — the cache just stops the same question from
being asked twice.

### Your turn

Time `fewest_tokens_cached` at `amount=100`. Then time
`fewest_tokens_brute_force` at the same amount — or, if you would rather not
wait, predict first whether it would finish in under a second, and say why.

```python exec
id: remembering-what-we-already-worked-out-3
hint: A fresh cache={} argument is optional -- the function already creates one on its own each call.
```

## The Greedy Shortcut

There is a third way, and it does not check every possibility at all. At
every step, hand over the largest token that still fits, and repeat until
nothing is left.

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

This is a *heuristic*: a rule of thumb that reaches an answer quickly by
never looking back, rather than checking whether an earlier choice was truly
the best one. `fewest_tokens_greedy(6, TOKENS)` returns `3`, using a `4` and
two `1`s. The cached version above already showed the real fewest is `2`,
using two `3`s instead. Taking the biggest token first was not wrong
exactly, but it closed off the one combination that would have won.

The ordinary coins on a till, `1`, `5`, `10`, and `25`, do not have this
problem. Try the same greedy shortcut against them:

```python exec
id: the-greedy-shortcut-2
ORDINARY_COINS = [1, 5, 10, 25]

for amount in [6, 41, 63]:
    greedy = fewest_tokens_greedy(amount, ORDINARY_COINS)
    guaranteed = fewest_tokens_cached(amount, ORDINARY_COINS)
    print(f"amount={amount}: greedy={greedy}, guaranteed correct={guaranteed}")
```

For every amount tried here, the fast shortcut and the slower, certain method
agree. That is a property of this particular set of coin values, not of
greedy shortcuts in general. The `[1, 3, 4]` tokens above are proof that a
greedy shortcut can be wrong, quietly, without ever announcing it.

### Your turn

Find a target amount, using `TOKENS = [1, 3, 4]`, where the greedy shortcut
and the cached method disagree by more than one token. Start from the
disagreement already shown at `amount=6` and try nearby amounts.

```python exec
id: the-greedy-shortcut-3
```

## Choosing a Strategy

Three strategies solved the same problem, and none of them is simply better
than the others.

Brute force is the strategy to reach for first. It is slow, but it is never
wrong, and for a small enough amount, slow does not matter. Caching keeps
brute force's guarantee while removing its worst cost, the repeated work
already done. That is why it is usually the strategy worth building once
brute force feels too slow.

The greedy shortcut trades that guarantee away entirely. It is the fastest
of the three, a single pass with no waiting, but its worst case is not
slowness. Its worst case is a wrong answer, delivered with just as much
confidence as a right one.

Which of the three a real program should use depends on what is actually
being asked. A calculator that must never shortchange anyone needs the
guarantee brute force or caching provides. A system recommending a rough
estimate to a person who will check it anyway can often afford the greedy
shortcut's risk, in exchange for its speed.

### Your turn

A vending machine gives change from `[1, 5, 10, 25]` after every purchase,
many times a minute. Which of the three strategies from this tutorial would
you build it around, and why?

## Where to Read More

Cormen, T. H., Leiserson, C. E., Rivest, R. L. and Stein, C. (2022).
*Introduction to Algorithms* (4th ed.). MIT Press. Chapter 15 covers
dynamic programming, the general name for the caching strategy this page
builds. Chapter 16 covers greedy algorithms, including exactly when a
greedy choice is provably safe.

Computerphile (2017). *Dynamic Programming.*
<https://www.youtube.com/watch?v=nJ2CjRmr9uw>. The same "remember what you
already worked out" idea, applied to a different problem.
