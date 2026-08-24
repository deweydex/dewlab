---
title: "Where Chains Lead"
slug: where-chains-lead
module: computational-methods
module_title: "Computational Methods"
year: "2026-2027"
series: matrices
version: 2026.08.24.1
covers:
  a-weather-machine:
    covers: [CMPS-LO4]
    touches: [CMPS-LO2]
  watching-it-settle:
    covers: [CMPS-LO4]
  words-that-follow-words:
    covers: [CMPS-LO4]
    touches: [CMPS-LO1]
  ranking-a-small-web:
    covers: [CMPS-LO4]
---

# Where Chains Lead

Every matrix so far has done something once — added, transformed, solved.
This tutorial is about a matrix that gets multiplied by itself, or by a
changing state, over and over — and about the strange fact that doing this
enough times settles down to an answer that no longer depends on where you
started. That single idea turns out to predict tomorrow's weather, rank
every page on the web, and write sentences a machine has never seen.

## A Weather Machine

Suppose today is either sunny or rainy, and tomorrow's weather depends only
on today's — not on last week's. In Dublin, say sunny days are followed by
another sunny day 70% of the time, and rainy days are followed by more rain
60% of the time.

```python exec
id: a-weather-machine-1
P = [[0.7, 0.3], [0.4, 0.6]]
for row in P:
    print(row, "sums to", sum(row))
```

Row 1 is "if today is sunny": 70% sunny tomorrow, 30% rainy. Row 2 is "if
today is rainy": 40% sunny, 60% more rain. Every row sums to 1, because
tomorrow is certainly *something*. This is a *transition matrix*, and each
row is a probability distribution over what happens next.

Today's weather can be written as a *state vector* too — `[1, 0]` for
"definitely sunny today", `[0, 1]` for "definitely rainy". Multiplying a
state vector by `P` gives tomorrow's probabilities.

```python exec
id: a-weather-machine-2
def dot(a, b):
    return sum(x * y for x, y in zip(a, b))

def transpose(m):
    rows, cols = len(m), len(m[0])
    return [[m[r][c] for r in range(rows)] for c in range(cols)]

def multiply(a, b):
    bt = transpose(b)
    return [[dot(row, col) for col in bt] for row in a]

today = [[1, 0]]
tomorrow = multiply(today, P)
print(tomorrow)
```

### Your turn

Starting from a definitely-rainy today, `[[0, 1]]`, compute tomorrow's
weather, and the day after that.

```python exec
id: a-weather-machine-3
hint: The day after tomorrow is tomorrow's state vector multiplied by P again — the state vector changes, P never does.
```

## Watching It Settle

What happens ten days out, if today is definitely sunny?

```python exec
id: watching-it-settle-1
state = [[1, 0]]
for day in range(1, 11):
    state = multiply(state, P)
    print(day, [round(v, 4) for v in state[0]])
```

The numbers stop moving. By day nine or so, the forecast is the same
whichever day you check — about 57% sunny, 43% rainy — and it no longer
matters at all that today started out definitely sunny.

### Your turn

Run the same ten steps starting from definitely rainy, `[[0, 1]]`, instead.
Does it settle on the same numbers?

```python exec
id: watching-it-settle-2
```

It does — the *stationary distribution* is a property of the transition
matrix itself, not of where you started. Once a state vector reaches it,
multiplying by `P` again changes nothing: $\boldsymbol{\pi} P = \boldsymbol{\pi}$,
a fixed point of the whole process.

## Words That Follow Words

A transition matrix does not need to be about weather. Here it is built from
a sentence — treating every distinct word as a state, and the matrix entry
for word $i$, word $j$ as how often $j$ followed $i$ in the text.

```python exec
id: words-that-follow-words-1
text = ("it was the best of times it was the worst of times "
        "it was the age of wisdom it was the age of foolishness "
        "it was the epoch of belief it was the epoch of incredulity "
        "it was the season of light it was the season of darkness "
        "it was the spring of hope it was the winter of despair")
words = text.split()
states = sorted(set(words))
index = {word: i for i, word in enumerate(states)}

counts = [[0] * len(states) for _ in states]
for a, b in zip(words, words[1:]):
    counts[index[a]][index[b]] += 1

P_words = []
for row in counts:
    total = sum(row)
    P_words.append([c / total if total else 0 for c in row])

print(len(states), "distinct words")
print("after 'it':", dict(zip(states, [round(v, 2) for v in P_words[index["it"]]])))
```

Filter that down to the words that actually have a non-zero chance of
following "it" and it is one word, always: "was". The sentence this came from
repeats "it was the ___ of ___" ten times, so from "it" the matrix has
learned there is only ever one thing that comes next.

```python exec
id: words-that-follow-words-2
after_the = dict(zip(states, [round(v, 3) for v in P_words[index["the"]]]))
print({k: v for k, v in after_the.items() if v > 0})
```

### Your turn

`"the"` is followed by several different words, each with roughly the same
small probability. Which words are they, and why does that match the
sentence this matrix was built from?

```python exec
id: words-that-follow-words-3
```

Now generate new text by walking the chain: start on a word, look up its row
of probabilities, and pick the next word randomly according to those
weights.

```python exec
id: words-that-follow-words-4
import random

def generate(start, steps):
    result = [start]
    current = start
    for _ in range(steps):
        row = P_words[index[current]]
        if sum(row) == 0:
            break
        current = random.choices(states, weights=row)[0]
        result.append(current)
    return " ".join(result)

print(generate("it", 12))
```

Run that cell a few times. Every sentence it produces is a genuine
recombination of the ten parallel clauses it was trained on — "it was the
season of incredulity" is not anywhere in the original text, but every pair
of adjacent words in it is. This is the entire idea behind predictive text on
a phone keyboard, scaled up enormously: given what came just before, what is
likely to come next?

## Ranking a Small Web

Three web pages link to each other. Page A links equally to B and C. Page B
links only to A. Page C links equally to A and B. Imagine a random surfer who
always follows one of the links on whatever page they are on — that is a
Markov chain, with the pages as states.

```python exec
id: ranking-a-small-web-1
P_web = [[0, 0.5, 0.5], [1, 0, 0], [0.5, 0.5, 0]]

visits = [[1/3, 1/3, 1/3]]
for step in range(20):
    visits = multiply(visits, P_web)
print("A, B, C:", [round(v, 4) for v in visits[0]])
```

Before running that, which page did you expect to end up with the highest
share of a random surfer's time — the same question the search engine this
is modelled on has to answer for the entire web? Page A is linked to by both
of the others, and that turns out to matter more than how many outgoing
links a page has.

### Your turn

Rank the three pages from the numbers above. Does the order match what you
predicted before running the cell?

```python exec
id: ranking-a-small-web-2
```

This is a deliberately small version of *PageRank*, the algorithm Google was
founded on: the stationary distribution of a random-surfer Markov chain over
the entire link graph of the web, with a page's rank being nothing more than
how much of a random surfer's long-run time it accumulates.

## Reflection

Three settings — weather, sentences, web pages — and one mechanism
underneath all of them: multiply a state by a matrix of probabilities, do it
again, and again, and watch the answer stop depending on where you started.
That convergence is not a coincidence specific to any one of these examples;
it is a property of the matrix, discovered the same way in all three, well
before this tutorial ever wrote the words "stationary distribution."

Which of the three applications felt the most surprising — that weather
forecasting, sentence generation, and ranking a search engine are, at the
arithmetic level, the same handful of lines?

## Where to Read More

Grant Sanderson (3Blue1Brown) (2022). *Markov Chains.*
<https://www.youtube.com/watch?v=JGSaEwGZoDE>. A visual argument for why
repeated multiplication by a transition matrix settles down at all, which
this tutorial only demonstrates numerically.

Page, L. and Brin, S. (1998). *The Anatomy of a Large-Scale Hypertextual Web
Search Engine.* Computer Networks and ISDN Systems, 30(1-7), 107–117.
<http://infolab.stanford.edu/~backrub/google.html>. The original PageRank
paper, from the two Stanford students who wrote it — the small three-page
example in this tutorial is the same mathematics at a readable scale.

Dickens, C. (1859). *A Tale of Two Cities.* The opening sentence, sourced for
the word-transition matrix here, is public domain and among the most
recognisable in English literature — worth reading the rest of, well beyond
what a Markov chain can imitate.

Shannon, C. E. (1948). *A Mathematical Theory of Communication.* Bell System
Technical Journal, 27(3), 379–423. Section 2 builds English text from letter
and word transition frequencies — the origin of the technique used in *Words
That Follow Words*, from 1948.
