---
title: "Three Ways to Make Change — Practice"
slug: three-ways-to-make-change-practice
practice_for: three-ways-to-make-change
module: computational-methods
module_title: "Computational Methods"
year: "2026-2027"
series: algorithms
version: 2026.09.05.1
---

# Three Ways to Make Change — Practice

Answers are folded. Several of these ask you to predict an output before
running anything. Resist checking first — being wrong and finding out why
is worth more than being right by accident.

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

## Checking the Guarantee

**1.** Predict `fewest_tokens_brute_force(10, TOKENS)` before running it: which
three tokens from `[1, 3, 4]` add up to `10`?

```python exec
id: checking-the-guarantee-1
hint: 4 + 3 + 3 is one path worth trying by hand first.
```

<details class="dl-answer"><summary>answer</summary>

`3`. One combination that reaches it is `4 + 3 + 3`; no combination of two
tokens from `[1, 3, 4]` reaches `10` at all, so three is the fewest possible.

</details>

**2.** What does `fewest_tokens_cached(0, TOKENS)` return, and why does that
particular answer matter to every other amount the function is ever asked
about?

```python exec
id: checking-the-guarantee-2
```

<details class="dl-answer"><summary>answer</summary>

`0`. Zero remaining means zero tokens needed. Every other amount is worked
out by trying a token and asking the same question about a smaller amount.
Without this base case, the function would keep asking about smaller
amounts forever, never handing back an actual number.

</details>

## When the Shortcut Fails

**3.** Using a different set of tokens, `TOKENS2 = [1, 4, 5]`, compare
`fewest_tokens_greedy(8, TOKENS2)` against `fewest_tokens_cached(8, TOKENS2)`.
The tutorial's own example disagreed by one token — does this one disagree by
more?

```python exec
id: when-the-shortcut-fails-1
hint: Work out the greedy choice by hand first: which token does it take at each step?
```

<details class="dl-answer"><summary>answer</summary>

Yes, by two. Greedy takes the `5` first, leaving `3`, then three separate
`1`s, for `4` tokens total. The cached, guaranteed-correct answer is `2`:
two `4`s. A greedy shortcut's mistake is not always as small as the
tutorial's own example made it look.

</details>

**4.** This time, call `fewest_tokens_greedy(5, [3, 4])`, where no `1` token
is available. Predict what it returns before running it, and say why in
terms of what the function actually does with `remaining` at the end.

```python exec
id: when-the-shortcut-fails-2
hint: Walk through the two coins by hand: take a 4, what is left, does a 3 fit into what's left?
```

<details class="dl-answer"><summary>answer</summary>

`None`. Taking the `4` first leaves `1` remaining, and no `3` fits into
`1`, so the loop ends with `remaining` still `1`, not `0`. The function's
own check, `count if remaining == 0 else None`, catches this and correctly
reports that `5` cannot be made from `[3, 4]` at all — the same answer
`fewest_tokens_brute_force(5, [3, 4])` would give.

</details>

## Reading the Trade-Off

**5.** In your own words: why does the tutorial say caching "keeps brute
force's guarantee" while the greedy shortcut does not?

<details class="dl-answer"><summary>answer</summary>

Caching still checks every possibility that brute force would check — it
only skips checking the *same* possibility a second time. Nothing about
which answers get compared changes, so the guarantee that the true fewest
gets found survives intact.

The greedy shortcut never compares possibilities at all. It commits to the
biggest token at each step and never looks back to ask whether an earlier,
smaller choice would have opened up a better path later. That is exactly
the choice that goes wrong with `TOKENS = [1, 3, 4]` at `amount=6`: taking
the `4` first closes off the two-token answer, `3 + 3`, for good.

</details>
