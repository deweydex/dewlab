---
title: "Making change: brute force, memoization and greedy algorithms — Practice"
practice_for: three-ways-to-make-change
year: "2026-2027"
version: 2026.09.05.1
---

# Making change: brute force, memoization and greedy algorithms — Practice

The answers are hidden in folds under each problem. Several problems ask
you to predict what the code will do before you run it. Try to answer
before you check. A wrong guess teaches you more than a lucky right one,
once you see why it was wrong.

```python exec
id: setup-1
TOKENS = [1, 3, 4]

def fewest_tokens_brute_force(amount, denominations):
    if amount == 0:
        return 0
    best = None
    for coin in denominations:
        if coin <= amount:
            rest = fewest_tokens_brute_force(amount - coin, denominations)
            if rest is not None and (best is None or rest + 1 < best):
                best = rest + 1
    return best

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

def fewest_tokens_greedy(amount, denominations):
    remaining = amount
    count = 0
    for coin in sorted(denominations, reverse=True):
        while remaining >= coin:
            remaining -= coin
            count += 1
    return count if remaining == 0 else None
```

## Checking the guarantee

**1.** Before you run it, can you predict
`fewest_tokens_brute_force(10, TOKENS)`? Which three tokens from
`[1, 3, 4]` add up to `10`?

```python exec
id: checking-the-guarantee-1
hint: 4 + 3 + 3 is one path worth trying by hand first.
```

<details class="dl-answer"><summary>answer</summary>

It returns `3`. One combination that makes `10` is `4 + 3 + 3`. No two tokens from
`[1, 3, 4]` make `10` at all, so three is the fewest possible.

</details>

**2.** What does `fewest_tokens_cached(0, TOKENS)` return? Why does that
answer matter for every other amount the function is ever asked about?

```python exec
id: checking-the-guarantee-2
```

<details class="dl-answer"><summary>answer</summary>

It returns `0`. When nothing is left to make, no tokens are needed.

The function finds the answer for every other amount by trying a token, then asking
the same question about a smaller amount. Every chain of questions ends
at `0`. This case is the base case: the case the function answers
without calling itself. Without it, the function would keep asking about
smaller amounts forever, and never return a number.

</details>

## When the shortcut fails

**3.** Try a different set of tokens, `TOKENS2 = [1, 4, 5]`. Compare
`fewest_tokens_greedy(8, TOKENS2)` with `fewest_tokens_cached(8, TOKENS2)`.
With `[1, 3, 4]`, the two never disagreed by more than one token. Does
this pair disagree by more?

```python exec
id: when-the-shortcut-fails-1
hint: Work out the greedy choice by hand first: which token does it take at each step?
```

<details class="dl-answer"><summary>answer</summary>

Yes, they disagree by two. Greedy takes the `5` first. That leaves `3`, which needs
three `1`s. So greedy uses `4` tokens in total. The cached answer, which
is always correct, is `2`: two `4`s. A greedy shortcut's mistake is not
always as small as the tutorial's example made it look.

</details>

**4.** This time, call `fewest_tokens_greedy(5, [3, 4])`. There is no `1`
token.

1. Predict what it returns, before you run it.
2. Why does it return that? Look at what the function does with
   `remaining` at the end.

```python exec
id: when-the-shortcut-fails-2
hint: Walk through the two coins by hand: take a 4, what is left, does a 3 fit into what's left?
```

<details class="dl-answer"><summary>answer</summary>

It returns `None`. Greedy takes the `4` first, which leaves `1`. A `3`
does not fit into `1`, so
the loop ends with `remaining` still at `1`, not `0`. The function's last
line, `count if remaining == 0 else None`, catches this. Here that answer
is correct. `5` cannot be made from `[3, 4]` at all, and
`fewest_tokens_brute_force(5, [3, 4])` gives `None` too.

But be careful what greedy's `None` means. Try
`fewest_tokens_greedy(6, [3, 4])`. It takes a `4`, is left with `2`, and
gives `None`. Yet `3 + 3` makes `6`. When greedy says `None`, it only
means the shortcut got stuck. When brute force says `None`, it means no
combination works.

</details>

## Reading the trade-off

**5.** The tutorial says that caching "keeps brute force's guarantee", and
that the greedy shortcut does not. In your own words, why?

<details class="dl-answer"><summary>answer</summary>

Caching still compares every choice of first token, just as brute force
does. It only avoids solving the same smaller amount a second time.
That is safe because the fewest tokens for an amount depends only on the
amount, not on how we reached it. So the answers it compares are the
same answers, and it still always finds the true fewest.

The greedy shortcut never compares possibilities at all. At each step it
takes the biggest token, and it never goes back to an earlier choice. It
never asks whether
a smaller choice earlier would have led to a better answer later. That is
the choice that goes wrong with `TOKENS = [1, 3, 4]` at `amount=6`.
Once it takes the `4` first, it can never reach the two-token answer,
`3 + 3`.

</details>

## Where to read more

SimonDev (2021). *What can "The Simpsons" teach us about Dynamic
Programming?* <https://www.youtube.com/watch?v=6z4ePR7YYa8>. SimonDev
shows a few problems that repeat the same work, and shows how
remembering answers saves it. The video is about fifteen minutes long.
