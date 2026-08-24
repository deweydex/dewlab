---
title: "Where Chains Lead — Practice"
slug: where-chains-lead-practice
practice_for: where-chains-lead
module: computational-methods
module_title: "Computational Methods"
year: "2026-2027"
series: matrices
version: 2026.08.24.1
---

# Where Chains Lead — Practice

Every stationary distribution here can be checked two ways: multiply the
state by the matrix many times and watch it settle, or solve
$\boldsymbol{\pi}P = \boldsymbol{\pi}$ directly. Do both at least once — they
should always agree.

## Transition Matrices

```python exec
id: transitions-1
def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def transpose(m):
    rows, cols = len(m), len(m[0])
    return [[m[r][c] for r in range(rows)] for c in range(cols)]


def multiply(a, b):
    bt = transpose(b)
    return [[dot(row, col) for col in bt] for row in a]
```

**1.** A student either studies or procrastinates each hour. If studying,
there is an 80% chance they keep studying next hour. If procrastinating,
there is a 60% chance they start studying next hour. Write the 2×2
transition matrix, with studying as state 1.

<details class="dl-answer"><summary>answer</summary>

$P = \begin{bmatrix} 0.8 & 0.2 \\ 0.6 & 0.4 \end{bmatrix}$

Row 1 is "currently studying": 80% studying next hour, 20% procrastinating.
Row 2 is "currently procrastinating": 60% studying next hour, 40% still
procrastinating. Both rows sum to 1, as any transition matrix's rows must.

</details>

**2.** Starting from definitely procrastinating, `[[0, 1]]`, what is the
state one hour later? Two hours later?

<details class="dl-answer"><summary>answer</summary>

One hour: `[0.6, 0.4]` — 60% chance of studying now, straight from row 2 of
`P`.

Two hours: multiply that result by `P` again —
$[0.6, 0.4] \cdot P = [0.6(0.8) + 0.4(0.6),\ 0.6(0.2) + 0.4(0.4)] = [0.72, 0.28]$.

</details>

## Settling Down

**3.** Iterate the study/procrastinate chain for 20-30 steps from any
starting state. What does it settle on?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Start from any state vector you like — `[[1, 0]]` or `[[0.5, 0.5]]` both
   work, since the whole point is that the starting point stops mattering.
2. Loop `multiply(state, P)` some number of times, reassigning `state` each
   time.
3. Print the last few iterations rather than all of them, and check they
   have stopped changing to four decimal places or so.

**Think about:** does it matter whether you started from definitely
studying, definitely procrastinating, or fifty-fifty?

**Try this next:** solve $\boldsymbol{\pi}P = \boldsymbol{\pi}$ by hand for
this chain, the way the tutorial's weather section did, and confirm it
matches what the iteration settled on.

</details>

<details class="dl-answer"><summary>answer</summary>

$[0.75, 0.25]$ — 75% of the long run spent studying, regardless of where you
started.

```python
P = [[0.8, 0.2], [0.6, 0.4]]
state = [[1, 0]]
for _ in range(30):
    state = multiply(state, P)
print(state)
```

</details>

**4.** A chain has $P = \begin{bmatrix} 1 & 0 \\ 0.3 & 0.7 \end{bmatrix}$.
State 1 is called *absorbing* because once entered, row 1 says there is a
0% chance of ever leaving. Iterate this chain starting from `[[0, 1]]` for
1, 2, 5, 10, and 20 steps. What is happening to the numbers?

<details class="dl-answer"><summary>answer</summary>

They climb steadily toward `[1, 0]`: `[0.3, 0.7]`, `[0.51, 0.49]`,
`[0.83, 0.17]`, `[0.97, 0.03]`, `[0.999, 0.001]` (rounded).

The chain never actually reaches `[1, 0]` exactly in a finite number of
steps, but it gets arbitrarily close — every visit to state 2 carries a 30%
chance of being swallowed by state 1 forever, so eventually it is a near
certainty. This is why absorbing states are sometimes what a Markov chain is
*for*: modelling a process that is only interesting until it stops, like a
gambler's ruin or a customer who eventually unsubscribes.

</details>

## Ranking Pages

**5.** Three pages: D links only to E. E links equally to D and F. F links
only to D. Write the transition matrix and find the stationary distribution.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Row D: D links only to E, so the whole row is concentrated on the "to E"
   column.
2. Row E: split equally between "to D" and "to F".
3. Row F: concentrated entirely on "to D".
4. Once you have the matrix, iterate from `[[1/3, 1/3, 1/3]]` the way the
   tutorial's web example did.

**Think about:** F only ever leads back to D. What does that do to how much
time a random surfer spends on F compared with D and E?

**Try this next:** what would change about the ranking if F linked to E
instead of D?

</details>

<details class="dl-answer"><summary>answer</summary>

$P = \begin{bmatrix} 0 & 1 & 0 \\ 0.5 & 0 & 0.5 \\ 1 & 0 & 0 \end{bmatrix}$,
and the stationary distribution is exactly $[0.4, 0.4, 0.2]$ — D and E tied
for the highest rank, F lowest.

```python
P = [[0, 1, 0], [0.5, 0, 0.5], [1, 0, 0]]
state = [[1/3, 1/3, 1/3]]
for _ in range(30):
    state = multiply(state, P)
print(state)
```

F only ever sends a visitor back to D, and never to itself or to E directly,
so a surfer passes *through* F rather than lingering — which is exactly why
its long-run share is the smallest, even though it is linked to just as
often as D is.

</details>

**6.** In the tutorial's three-page example, page A had the highest rank
even though it has exactly one outgoing link (to itself it has none — it
splits between B and C). Why does the *number* of outgoing links a page has
not straightforwardly predict its rank?

<details class="dl-answer"><summary>answer</summary>

Because rank depends on how much traffic a page *receives*, not how much it
sends out — and how much it receives depends on who links to it and how
concentrated those pages' own outgoing links are.

Page A ranked highest because both other pages link to it, and one of them
(B) links to *nothing else at all* — every single visit to B sends its full
weight straight back to A. A page's own out-degree only ever splits its
existing weight among its neighbours; it has no bearing on how much weight
that page has to split in the first place.

</details>

## Words and Chains

```python exec
id: words-1
import random

def build_chain(text):
    words = text.split()
    states = sorted(set(words))
    index = {w: i for i, w in enumerate(states)}
    counts = [[0] * len(states) for _ in states]
    for a, b in zip(words, words[1:]):
        counts[index[a]][index[b]] += 1
    P = [[c / sum(row) if sum(row) else 0 for c in row] for row in counts]
    return states, index, P
```

**7.** Build a chain from `"red fish blue fish one fish two fish"`, and print
the row for `"fish"`. Why does it have three different words with a
non-zero probability, and are they equally likely?

<details class="dl-answer"><summary>answer</summary>

```python
states, index, P = build_chain("red fish blue fish one fish two fish")
print(dict(zip(states, [round(v, 2) for v in P[index["fish"]]])))
```

`"fish"` appears four times in the sentence. Three of those are followed by
another word — `"blue"`, `"one"`, `"two"`, each exactly once — so the row
splits evenly, $\frac{1}{3}$ each. The fourth `"fish"` is the very last word
in the sentence and has nothing after it, so it never contributes a
transition at all; it simply is not one of the three pairs the row is built
from.

</details>

**8.** Using the chain from problem 7, is it possible for `generate` to
produce the word `"red"` anywhere except as the very first word?

<details class="dl-answer"><summary>answer</summary>

No. `"red"` never appears anywhere in the training text except at the very
start, so no row of the matrix has a nonzero probability of transitioning
*into* `"red"` — nothing in the text was ever followed by it. A Markov chain
can only produce transitions it has actually seen; it cannot invent one
because the resulting sentence would sound more natural.

</details>
