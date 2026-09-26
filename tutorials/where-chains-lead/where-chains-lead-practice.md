---
title: "Markov chains: where repeated steps settle — Practice"
practice_for: where-chains-lead
year: "2026-2027"
version: 2026.09.26.1
---

# Markov chains: where repeated steps settle — Practice

You can check every stationary distribution on this page in two ways:

1. Multiply the state by the matrix many times, and watch it settle.
2. Solve $\boldsymbol{\pi}P = \boldsymbol{\pi}$ directly, by hand as in
   problem 3, or with your `solve` as in problem 9.

Try both at least once. They should always agree. Your own `multiply`,
`solve` and the functions from the earlier pages are already loaded.

## Transition matrices

**1.** Each hour, a student either studies or *procrastinates* (delays the
work). If they are studying, there is an 80% chance that they are
still studying the next hour. If they are procrastinating, there is a
60% chance that they start studying the next hour. Write the 2×2
transition matrix, with studying as state 1.

<details class="dl-answer"><summary>answer</summary>

$P = \begin{bmatrix} 0.8 & 0.2 \\ 0.6 & 0.4 \end{bmatrix}$

- Row 1 is "studying now": 80% studying next hour, 20% procrastinating.
- Row 2 is "procrastinating now": 60% studying next hour, 40% still
  procrastinating.

Both rows add up to 1, as the rows of every transition matrix must.

</details>

**2.** Start from certainly procrastinating, `[[0, 1]]`. What is the
state one hour later? What is it two hours later?

<details class="dl-answer"><summary>answer</summary>

After one hour: `[0.6, 0.4]`, a 60% chance of studying. This comes
straight from row 2 of `P`.

After two hours: multiply that result by `P` again.
$[0.6, 0.4] \cdot P = [0.6(0.8) + 0.4(0.6),\ 0.6(0.2) + 0.4(0.4)] = [0.72, 0.28]$.

</details>

## Settling down

**3.** Run the study chain for 20 to 30 steps, from any starting state.
What does it settle on?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Start from any state vector you like. `[[1, 0]]` and `[[0.5, 0.5]]`
   both work, because the starting point stops mattering.
2. In a loop, calculate `multiply(state, P)` and store the result in
   `state` again, many times.
3. Print only the last few steps. Check that they have stopped changing,
   to about four decimal places.

**Think about:** does it matter whether you started from certainly
studying, certainly procrastinating, or fifty-fifty?

**Try this next:** solve $\boldsymbol{\pi}P = \boldsymbol{\pi}$ by hand for
this chain. Write $\boldsymbol{\pi} = [p, 1 - p]$. The first entry of
$\boldsymbol{\pi}P$ is $0.8p + 0.6(1 - p)$, and it must equal $p$. Solve
that for $p$. Does it match what the loop settled on?

</details>

<details class="dl-answer"><summary>answer</summary>

$[0.75, 0.25]$. In the long run, the student spends 75% of the time
studying, wherever they started.

By hand: $0.8p + 0.6(1 - p) = p$ gives $0.6 = 0.8p$, so $p = 0.75$.

```python
P = [[0.8, 0.2], [0.6, 0.4]]
state = [[1, 0]]
for _ in range(30):
    state = multiply(state, P)
print(state)
```

</details>

**4.** A chain has $P = \begin{bmatrix} 1 & 0 \\ 0.3 & 0.7 \end{bmatrix}$.
State 1 is *absorbing*. An absorbing state is a state that the chain
never leaves once it gets there. Row 1 says there is a 0% chance of
leaving state 1.

Run this chain from `[[0, 1]]` for 1, 2, 5, 10 and 20 steps. What is
happening to the numbers?

<details class="dl-answer"><summary>answer</summary>

They climb steadily towards `[1, 0]`. Rounded, they are `[0.3, 0.7]`,
`[0.51, 0.49]`, `[0.83, 0.17]`, `[0.97, 0.03]` and `[0.999, 0.001]`.

The chain never reaches `[1, 0]` exactly, in any number of steps. But it
gets as close as you like. At every step in state 2, there is a 30%
chance of moving into state 1 and staying there for ever. So in the end
it is almost certain.

Sometimes an absorbing state is the whole reason for building a Markov
chain. It models a process that matters only until it stops. One example
is a customer who, in the end, cancels their subscription. Another
is a gambler who keeps playing until all their money is gone.

</details>

## Ranking pages

**5.** Here are three pages:

- D links only to E.
- E links to D and to F.
- F links only to D.

Write the transition matrix, and find the stationary distribution.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Row D: D links only to E, so the whole chance of 1 goes in the "to E"
   column.
2. Row E: the chance is shared equally between "to D" and "to F".
3. Row F: the whole chance of 1 goes in the "to D" column.
4. When you have the matrix, run it from `[[1/3, 1/3, 1/3]]`, as the
   tutorial's web example did.

**Think about:** F only ever leads back to D. What does that do to the
time a random surfer spends on F, compared with D and E?

**Try this next:** how would the ranking change if F linked to E, and
not to D?

</details>

<details class="dl-answer"><summary>answer</summary>

$P = \begin{bmatrix} 0 & 1 & 0 \\ 0.5 & 0 & 0.5 \\ 1 & 0 & 0 \end{bmatrix}$.
The stationary distribution is exactly $[0.4, 0.4, 0.2]$. D and E tie
for the highest rank, and F is lowest. After 30 steps, the loop below
prints numbers very close to these.

```python
P = [[0, 1, 0], [0.5, 0, 0.5], [1, 0, 0]]
state = [[1/3, 1/3, 1/3]]
for _ in range(30):
    state = multiply(state, P)
print(state)
```

E and F each have only one page linking to them. E gets all of D's
visitors, because D links only to E. F gets only half of E's visitors,
because E shares its visitors between D and F. So F's long-run share is
half of E's. F then sends every visitor on to D, so D collects visitors
from both E and F.

</details>

**6.** In the tutorial's three-page example, pages A and C both have two
outgoing links. Yet A has the highest rank and C has the lowest. Why
does the number of outgoing links not tell us a page's rank?

<details class="dl-answer"><summary>answer</summary>

Rank depends on how many visitors a page receives, not on how many it
sends out. The visitors a page receives depend on which pages link to
it, and on how many other links those pages have.

Page A ranked highest because both other pages link to it. One of them,
B, links to nothing else, so every visitor to B goes straight on to A.

A page's outgoing links only share the visitors that the page
already has. They do not change how many visitors the page has to share
in the first place.

</details>

## Words and chains

```python exec
id: words-1
import random

def build_chain(text):
    words = text.split()
    states = sorted(set(words))
    index = {w: i for i, w in enumerate(states)}
    counts = [[0] * len(states) for _ in states]
    for word, next_word in zip(words, words[1:]):
        counts[index[word]][index[next_word]] += 1
    P = [[c / sum(row) if sum(row) else 0 for c in row] for row in counts]
    return states, index, P
```

**7.** Build a chain from `"red fish blue fish one fish two fish"`. Print
the row for `"fish"`.

1. Why do three different words have a chance above zero?
2. Are they equally likely?

<details class="dl-answer"><summary>answer</summary>

```python
states, index, P = build_chain("red fish blue fish one fish two fish")
print(dict(zip(states, [round(v, 2) for v in P[index["fish"]]])))
```

`"fish"` appears four times in the sentence. Three of those times, it is
followed by another word: `"blue"`, `"one"` and `"two"`, once each. So
the row shares its chance equally, $\frac{1}{3}$ each.

The fourth `"fish"` is the last word in the sentence, with nothing after
it. So it adds no pair to the row. The row is built from the other three
pairs only.

</details>

**8.** Take the chain from problem 7, and a `generate` function like the
one in the tutorial. Can `generate` ever produce the word `"red"`,
except as the very first word?

<details class="dl-answer"><summary>answer</summary>

No. `"red"` appears in the text only at the very start. Nothing in the
text is ever followed by `"red"`. So no row of the matrix has a chance
above zero of moving to `"red"`.

A Markov chain can only make moves it has seen in its text. It cannot
invent a new move, even one that would make the sentence sound more
natural.

</details>

## From earlier

**9.** From *Solving systems*. For the study chain, write
$\boldsymbol{\pi} = [p, q]$. The first column of
$\boldsymbol{\pi}P = \boldsymbol{\pi}$ says $0.8p + 0.6q = p$, which is
$-0.2p + 0.6q = 0$. The second column says $0.2p + 0.4q = q$. Together
with $p + q = 1$, can you use `solve` to find $p$ and $q$? Why is the
second column's equation no help?

```python exec
id: chains-solve
```

```hint
Move everything to the left. The second column's equation becomes
$0.2p - 0.6q = 0$. Compare it with the first.
```

```solution
{{include: setup/matrices/solve.py}}

print(solve([[-0.2, 0.6, 0], [1, 1, 1]]))
---
It prints `[0.7499999999999999, 0.25]`, which is 0.75 and 0.25 with
rounding in the last decimal place. The loop in problem 3 settles on the
same numbers. The second column's equation is the
first one times $-1$, so the two together have determinant 0 and
infinitely many solutions, every $[p, q]$ with $p = 3q$. The line
$p + q = 1$ picks one of them.
```

**10.** From *NumPy*. What does
`np.linalg.matrix_power(np.array(P), 30)` look like for the study
chain, and why are its two rows the same?

```python exec
id: chains-matrix-power
import numpy as np

P = [[0.8, 0.2], [0.6, 0.4]]
print(np.round(np.linalg.matrix_power(np.array(P), 30), 4))
```

<details class="dl-answer"><summary>answer</summary>

Both rows are `[0.75 0.25]`. Row 1 is the state 30 hours after certainly
studying, and row 2 is the state 30 hours after certainly
procrastinating. After 30 steps the start no longer shows, so both rows
are the stationary distribution.

</details>

## Where to read more

Spanning Tree (2020). *How Google's PageRank Algorithm Works.*
<https://www.youtube.com/watch?v=meonLcN7LD4>. This video explains the random
surfer from the ranking problems, and the damping factor that stops it being trapped on
one page. About five minutes.
