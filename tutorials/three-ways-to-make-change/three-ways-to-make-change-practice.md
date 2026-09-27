---
title: "Making change: brute force, memoization and greedy algorithms — Practice"
practice_for: three-ways-to-make-change
year: "2026-2027"
version: 2026.09.27.1
worlds:
  mazes-and-dungeons: A dungeon merchant who takes gems as payment.
  maps-and-networks: A post office with stamps of odd values.
  collections: A collection of the old Irish coins, from before 1971.
  puzzles: A dragon kingdom with coins of its own.
---

# Making change: brute force, memoization and greedy algorithms — Practice

Each answer is hidden until you open it. Write something down first,
even a guess, and then open the answer to compare.

## Tools

```python exec
id: tools-1
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

**1.** Which tokens from `[1, 3, 4]` make `10`, as few as possible?

```python exec
id: checking-the-guarantee-1
print(fewest_tokens_brute_force(10, TOKENS))
```

```predict
type: number

What will the cell print?
```

<details class="dl-answer"><summary>why</summary>

It prints `3`: for example `4 + 3 + 3`. No two tokens from `[1, 3, 4]`
make `10` at all, so three is the fewest possible.

</details>

**2.** When nothing is left to make, how many tokens are needed?

```python exec
id: checking-the-guarantee-2
print(fewest_tokens_cached(0, TOKENS))
```

```predict
type: number

What will the cell print?
```

<details class="dl-answer"><summary>why</summary>

It prints `0`. Every other amount is found by trying a token, then
asking the same question about a smaller amount, and every chain of
questions ends at `0`. This is the base case: the one the function
answers without calling itself. Without it, the function would keep
asking about smaller amounts forever.

</details>

## When the shortcut fails

**3.** Can you write `extra_tokens(amount, coins)`? It returns how many
more tokens the greedy shortcut uses than the fewest possible, or
`None` if greedy gets stuck.

```python exec
id: when-the-shortcut-fails-1
def extra_tokens(amount, coins):
    """How many more tokens greedy uses than it needs, or None if it gets stuck."""
    # Your code here.
```

```hint
Ask `fewest_tokens_greedy` first. If it says `None`, return `None`.
Otherwise, subtract what `fewest_tokens_cached` says.
```

```inputs
extra_tokens(8, [1, 4, 5])
extra_tokens(6, [1, 3, 4])
extra_tokens(41, [1, 2, 5, 10, 20, 50])
extra_tokens(6, [3, 4])
```

```solution
def extra_tokens(amount, coins):
    """How many more tokens greedy uses than it needs, or None if it gets stuck."""
    greedy = fewest_tokens_greedy(amount, coins)
    if greedy is None:
        return None
    return greedy - fewest_tokens_cached(amount, coins)
---
With `[1, 4, 5]`, greedy pays 8 with a 5 and three 1s, two more than the
two 4s it needs. With `[1, 3, 4]` it is one out at 6, and with euro
coins at 41 it needs nothing extra. With `[3, 4]` it gets stuck at 6,
though `3 + 3` would do: problem 4 looks at that.
```

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

## Counting the work

**5.** Brute force calls itself once for every token that fits, and
each of those calls does the same. Can you write
`brute_calls(amount, coins)`, which counts the calls without making
them? It is a recursion of its own: one call for this amount, plus the
calls for each smaller amount it would try.

```python exec
id: counting-the-work-1
def brute_calls(amount, coins):
    """How many calls fewest_tokens_brute_force makes for this amount."""
    # Your code here.
```

```hint
`1 + sum(brute_calls(amount - coin, coins) for coin in coins if coin <=
amount)`. When no coin fits, the `sum` is 0, and the answer is 1: that
is the base case.
```

```inputs
brute_calls(10, TOKENS)
brute_calls(20, TOKENS)
brute_calls(6, [1])
```

```solution
def brute_calls(amount, coins):
    """How many calls fewest_tokens_brute_force makes for this amount."""
    return 1 + sum(brute_calls(amount - coin, coins) for coin in coins if coin <= amount)
---
168 calls for 10 and 20,736 for 20, the tutorial's counts. With only a
`1` token there is one path, and 6 takes 7 calls: 6, 5, 4, 3, 2, 1 and
0. More kinds of token make more branches at every step, and that is
where the exponential growth comes from.
```

**6.** The tutorial counted *handfuls*, where order does not matter.
Count *orders* instead: paying 4 with `[1, 2]` as 1, 1, 2 is different
from 2, 1, 1. Can you write `count_orders(amount, coins)`?

```python exec
id: counting-the-work-2
def count_orders(amount, coins):
    """How many different orders of coins make the amount."""
    # Your code here.
```

```hint
The first coin can be any coin that fits. After it, the rest is the
same question for a smaller amount. Nothing left to pay is one order:
the empty one.
```

```inputs
count_orders(4, [1, 2])
count_orders(10, [1, 2])
count_orders(6, [1, 3, 4])
```

```solution
def count_orders(amount, coins):
    """How many different orders of coins make the amount."""
    if amount == 0:
        return 1
    return sum(count_orders(amount - coin, coins) for coin in coins if coin <= amount)
---
Five orders make 4 from 1s and 2s, and 89 make 10. These are the
Fibonacci numbers: the orders for $n$ are the orders for $n - 1$ (start
with a 1) plus the orders for $n - 2$ (start with a 2). For 6 with
`[1, 3, 4]` there are 9 orders, but only 4 handfuls.
```

## Reading the trade-off

**7.** The tutorial says that caching "keeps brute force's guarantee", and
that the greedy shortcut does not. In your own words, why?

<details class="dl-answer"><summary>answer</summary>

Caching still compares every choice of first token, just as brute force
does. It only avoids solving the same smaller amount a second time.
That is safe because the fewest tokens for an amount depends only on the
amount, not on how we reached it. So the answers it compares are the
same answers, and it still always finds the true fewest.

The greedy shortcut never compares possibilities at all. At each step it
takes the biggest token, and it never goes back to an earlier choice. It
never asks whether a smaller choice earlier would have led to a better
answer later. That is where it goes wrong with `TOKENS = [1, 3, 4]` at
`amount=6`. Once it takes the `4` first, it can never reach the
two-token answer, `3 + 3`.

</details>

## Your world

**8.** Can you write `worst_gap(limit, coins)`? It returns the largest
number of extra coins greedy ever uses, for amounts from 1 to `limit`,
and the first amount where that happens, as `(extra, amount)`. If greedy
is never wrong, it returns `(0, None)`.

<div class="dl-world" data-world="mazes-and-dungeons">

```python exec
id: your-world-1--mazes-and-dungeons
DUNGEON_GEMS = [1, 5, 6, 9]


def worst_gap(limit, coins):
    """(extra coins, first amount) for greedy's worst mistake up to limit."""
    # Your code here.
```

```hint
Start with `worst = (0, None)`. For each amount, work out how many extra
coins greedy uses, and keep it only if it is *more* than the worst so
far, so that the first amount is the one kept.
```

```inputs
worst_gap(100, DUNGEON_GEMS)
worst_gap(30, DUNGEON_GEMS)
worst_gap(100, [1, 7, 10])
```

```solution
def worst_gap(limit, coins):
    """(extra coins, first amount) for greedy's worst mistake up to limit."""
    worst = (0, None)
    for amount in range(1, limit + 1):
        extra = fewest_tokens_greedy(amount, coins) - fewest_tokens_cached(amount, coins)
        if extra > worst[0]:
            worst = (extra, amount)
    return worst
---
With these coins, greedy pays 12 gold with a 9 and three 1s, four gems, where two 6s would do: 2 too many. No amount up to 100 is worse. The tutorial's kingdom, with coins of 1, 7 and
10, is worse: 3 extra coins at 14.
```

</div>

<div class="dl-world" data-world="maps-and-networks">

```python exec
id: your-world-1--maps-and-networks
STAMPS = [1, 4, 9, 16]


def worst_gap(limit, coins):
    """(extra coins, first amount) for greedy's worst mistake up to limit."""
    # Your code here.
```

```hint
Start with `worst = (0, None)`. For each amount, work out how many extra
coins greedy uses, and keep it only if it is *more* than the worst so
far, so that the first amount is the one kept.
```

```inputs
worst_gap(100, STAMPS)
worst_gap(30, STAMPS)
worst_gap(100, [1, 7, 10])
```

```solution
def worst_gap(limit, coins):
    """(extra coins, first amount) for greedy's worst mistake up to limit."""
    worst = (0, None)
    for amount in range(1, limit + 1):
        extra = fewest_tokens_greedy(amount, coins) - fewest_tokens_cached(amount, coins)
        if extra > worst[0]:
            worst = (extra, amount)
    return worst
---
With these coins, greedy is never more than one stamp out up to 100, and the first amount where it is out at all is 12: a 9 and three 1s, where three 4s would do. The tutorial's kingdom, with coins of 1, 7 and
10, is worse: 3 extra coins at 14.
```

</div>

<div class="dl-world" data-world="collections">

```python exec
id: your-world-1--collections
OLD_COINS = [1, 3, 6, 12, 24, 30]


def worst_gap(limit, coins):
    """(extra coins, first amount) for greedy's worst mistake up to limit."""
    # Your code here.
```

```hint
Start with `worst = (0, None)`. For each amount, work out how many extra
coins greedy uses, and keep it only if it is *more* than the worst so
far, so that the first amount is the one kept.
```

```inputs
worst_gap(100, OLD_COINS)
worst_gap(30, OLD_COINS)
worst_gap(100, [1, 7, 10])
```

```solution
def worst_gap(limit, coins):
    """(extra coins, first amount) for greedy's worst mistake up to limit."""
    worst = (0, None)
    for amount in range(1, limit + 1):
        extra = fewest_tokens_greedy(amount, coins) - fewest_tokens_cached(amount, coins)
        if extra > worst[0]:
            worst = (extra, amount)
    return worst
---
With these coins, greedy is never more than one coin out, and it first goes wrong at 48 pence, where two florins beat a half crown, a shilling and a sixpence. Up to 30 pence it is never wrong at all: `(0, None)`. The tutorial's kingdom, with coins of 1, 7 and
10, is worse: 3 extra coins at 14.
```

</div>

<div class="dl-world" data-world="puzzles">

```python exec
id: your-world-1--puzzles
DRAGON_COINS = [1, 6, 10]


def worst_gap(limit, coins):
    """(extra coins, first amount) for greedy's worst mistake up to limit."""
    # Your code here.
```

```hint
Start with `worst = (0, None)`. For each amount, work out how many extra
coins greedy uses, and keep it only if it is *more* than the worst so
far, so that the first amount is the one kept.
```

```inputs
worst_gap(100, DRAGON_COINS)
worst_gap(30, DRAGON_COINS)
worst_gap(100, [1, 7, 10])
```

```solution
def worst_gap(limit, coins):
    """(extra coins, first amount) for greedy's worst mistake up to limit."""
    worst = (0, None)
    for amount in range(1, limit + 1):
        extra = fewest_tokens_greedy(amount, coins) - fewest_tokens_cached(amount, coins)
        if extra > worst[0]:
            worst = (extra, amount)
    return worst
---
With these coins, greedy is at worst 2 coins out, first at 24 scales: two 10s and four 1s, where four 6s would do. The tutorial's kingdom, with coins of 1, 7 and
10, is worse: 3 extra coins at 14.
```

</div>

## From earlier

**9.** From [Dictionaries: looking things up by
name](tutorial:looking-things-up-by-name). The cache is a dictionary,
and `in` asks whether a key is there.

```python exec
id: from-earlier-1
cache = {}
cache[2] = 2
print(3 in cache, 2 in cache)
```

```predict
type: choice

What will the cell print?

- False True
- True True
  - Every amount has an answer, stored or not.
- False False
  - `in` looks at the values.
```

<details class="dl-answer"><summary>why</summary>

It prints `False True`. `in` looks at a dictionary's keys. The key `2`
is there, with the value `2`; the key `3` is not. That one test is what
lets the cached function skip the work it has done before.

</details>

## Where to read more

SimonDev (2021). *What can "The Simpsons" teach us about Dynamic
Programming?* <https://www.youtube.com/watch?v=6z4ePR7YYa8>. SimonDev
shows a few problems that repeat the same work, and shows how
remembering answers saves it. The video is about fifteen minutes long.
