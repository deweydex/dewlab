---
title: "Markov chains: where repeated steps settle"
year: "2026-2027"
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

# Markov chains: where repeated steps settle

So far, every matrix has done something once. We added matrices,
transformed pictures with them, and solved systems with them.

On this page, we multiply by the same matrix over and over. Something
strange happens. After enough steps, the answer settles down, and it no
longer depends on where we started.

This one idea can forecast the weather, rank every page on the web, and
write sentences that nobody has written before. On this page we:

- build a matrix of probabilities for tomorrow's weather
- watch the forecast settle as the days go on
- build the same kind of matrix from a sentence, and use it to write new
  text
- rank three small web pages

## A weather machine

Suppose each day is either sunny or rainy. Suppose also that tomorrow's
weather depends only on today's weather, and not on last week's.

Let's make up some numbers for Dublin. A sunny day is followed by
another sunny day 70% of the time. A rainy day is followed by more rain
60% of the time.

```python exec
id: a-weather-machine-1
P = [[0.7, 0.3], [0.4, 0.6]]
for row in P:
    print(row, "sums to", sum(row))
```

![Two states, sunny and rainy. An arrow from sunny to rainy carries 30%,
and one back carries 40%. Each state also has an arrow looping back to
itself: 70% on sunny, 60% on rainy.](weather-states.svg)

This drawing is a *state diagram*. A state diagram shows the states that
something can be in, as circles. Each arrow is a way of moving from one
state to another, labelled with how likely that move is. You will meet
this kind of picture wherever something moves between a small number of
conditions.

The picture and the matrix `P` say the same thing in two ways. Each row
of the matrix holds the arrows that leave one state:

- Row 1 is "if today is sunny": 70% sunny tomorrow, 30% rainy.
- Row 2 is "if today is rainy": 40% sunny tomorrow, 60% rainy.

The drawing shows every arrow that leaves a state. That includes the
arrow that loops back to where it started, which means "the weather
stays the same".

Why does each row add up to 1? When we leave a state, something has to
happen next. Tomorrow will certainly have some weather.

`P` is a *transition matrix*. A transition matrix is a matrix of
probabilities, where each row gives the chances of each thing that can
happen next. A *Markov chain* is a process that moves from state to
state using a transition matrix. What happens next depends only on the
current state, and not on how the process got there.

We can write today's weather as a *state vector*. A state vector is a
row that holds the probability of each state. `[1, 0]` means "certainly
sunny today", and `[0, 1]` means "certainly rainy today".

When we multiply a state vector by `P`, we get the probabilities for
tomorrow. If today is certainly sunny, what do you expect tomorrow's
state vector to be? Run the cell to check.

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

1. Start from a day that is certainly rainy, `[[0, 1]]`. What is
   tomorrow's weather?
2. What about the day after that?

```python exec
id: a-weather-machine-3
hint: The day after tomorrow is tomorrow's state vector multiplied by P again — the state vector changes, P never does.
```

## Watching it settle

What will the forecast be ten days from now, if today is certainly
sunny? Before you run the cell, guess: will the chance of sun keep
falling, or will it stop somewhere?

```python exec
id: watching-it-settle-1
state = [[1, 0]]
for day in range(1, 11):
    state = multiply(state, P)
    print(day, [round(v, 4) for v in state[0]])
```

The numbers stop moving. By about day nine, the forecast is the same
from one day to the next: about 57% sunny and 43% rainy. It no longer
matters that today was certainly sunny.

### Your turn

1. Run the same ten steps, but start from a day that is certainly rainy,
   `[[0, 1]]`.
2. Does the forecast settle on the same numbers?

```python exec
id: watching-it-settle-2
```

It does. The numbers it settles on are the *stationary distribution*.
The stationary distribution is the state vector that stays the same when
we multiply it by `P` again. In symbols, $\boldsymbol{\pi} P = \boldsymbol{\pi}$,
where $\boldsymbol{\pi}$ is the stationary distribution. It is a fixed
point of the whole process.

For a chain like this weather one, the stationary distribution belongs
to the transition matrix itself. It does not depend on where we started.

## Words that follow words

A transition matrix does not have to be about weather. The cell below
builds one from a sentence. Every different word is a state. The entry
for word $i$ and word $j$ is the share of times that word $j$ came
straight after word $i$ in the text.

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
for word, next_word in zip(words, words[1:]):
    counts[index[word]][index[next_word]] += 1

P_words = []
for row in counts:
    total = sum(row)
    P_words.append([c / total if total else 0 for c in row])

print(len(states), "distinct words")
print("after 'it':", dict(zip(states, [round(v, 2) for v in P_words[index["it"]]])))
```

There is a lot in this cell, so here it is one step at a time:

1. `text.split()` cuts the text into a list of words.
2. `set(words)` keeps one copy of each different word, and `sorted`
   puts them in alphabetical order. These are the `states`.
3. `index` is a dictionary that gives each word its row number. It is
   built with a dictionary comprehension, which works like a list
   comprehension but makes a dictionary. Comprehensions are in
   [Comprehensions, grids and aliasing](tutorial:comprehensions-and-grids),
   and dictionaries are in
   [Dictionaries: looking things up by name](tutorial:looking-things-up-by-name).
4. `counts` starts as a grid of zeros, one row and one column for each
   word.
5. `zip(words, words[1:])` pairs each word with the word after it. For
   each pair, we add 1 to the matching entry in `counts`.
6. Finally, each row of counts is divided by its total, so that the row
   adds up to 1. The last word, "despair", is never followed by anything.
   Its row stays all zeros.

Look at the words that follow "it". Only one has a chance above zero:
"was", with a chance of 1. The text repeats "it was the ___ of ___" ten
times. So the matrix has learned that only one word ever comes after
"it".

Which words do you think can follow "the"? The cell below prints only
the words with a chance above zero.

```python exec
id: words-that-follow-words-2
after_the = dict(zip(states, [round(v, 3) for v in P_words[index["the"]]]))
print({k: v for k, v in after_the.items() if v > 0})
```

### Your turn

"the" is followed by several different words, and each one has a small
chance.

1. Which words are they?
2. Some have twice the chance of others. Why? Look back at the text the
   matrix was built from.

```python exec
id: words-that-follow-words-3
```

Now we can write new text by walking along the chain:

1. Start on a word.
2. Look up its row of probabilities.
3. Pick the next word at random, using those probabilities as weights.
4. Repeat from the new word.

`random.choices(states, weights=row)` picks one word from `states` at
random, so that a word with a bigger weight is picked more often. It
gives back a list with one word in it, so `[0]` takes that word out.

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

Run the cell a few times. What do you notice about the sentences?

Every sentence it makes is a new mix of the ten clauses in the text.
"it was the season of incredulity" is nowhere in the original text. But
every pair of neighbouring words in it is. When the walk reaches
"despair", it stops, because "despair" is never followed by anything.

Predictive text on a phone keyboard uses this idea, on a much bigger
scale. It asks: given the words that came right before, what is likely to
come next?

This chain saw only 20 different words, all from one repeated sentence.
A real book has thousands.
[A Markov chain from a whole book: a dictionary of dictionaries](tutorial:a-chain-reads-a-book)
continues from here. It builds the same kind of chain from a whole
novel, and uses it to write sentences that nobody has read before.

## Ranking a small web

Three web pages link to each other:

- Page A links to B and to C.
- Page B links only to A.
- Page C links to A and to B.

Imagine a *random surfer*: a person who always clicks one of the links
on the page they are on, chosen at random. The surfer's journey is a
Markov chain, and the pages are its states. Each row of `P_web` below
is one page, and it shares the chances equally between that page's
links.

Which page do you think the random surfer spends the most time on, in
the long run? A search engine asks the same question about the whole
web. Make a guess, then run the cell.

```python exec
id: ranking-a-small-web-1
P_web = [[0, 0.5, 0.5], [1, 0, 0], [0.5, 0.5, 0]]

visits = [[1/3, 1/3, 1/3]]
for step in range(20):
    visits = multiply(visits, P_web)
print("A, B, C:", [round(v, 4) for v in visits[0]])
```

A comes first, with 4 visits in every 9. Why A? It is not the number of
links pointing at it: B has two pages linking to it as well, A and C.
The difference is what those links carry. B has only one link out, so
every surfer on B goes to A next. A and C each split their surfers in
half. A page ranks high when the pages that link to it send it a big
share of their visitors, and when those pages are visited often
themselves.

### Your turn

1. How would you rank the three pages from the numbers above?
2. Does the order match your guess from before you ran the cell?

```python exec
id: ranking-a-small-web-2
```

This is a very small version of *PageRank*, the algorithm that Google
was founded on. PageRank finds the stationary distribution of a
random-surfer Markov chain over the links of the whole web. A page's
rank is the share of the random surfer's time that the page gets, in the
long run. The real PageRank adds one more detail: now and then, the
surfer jumps to a page chosen at random, and does not follow a link.

## Reflection

We met three settings: weather, sentences and web pages. Underneath all
three is one mechanism. We multiply a state by a matrix of
probabilities, then do it again, and again.

For the weather and the web pages, we watched the answer stop depending
on where we started. That settling is not a lucky accident of those two
examples. It comes from the matrix. We saw it with our own eyes before
we gave it a name, "stationary distribution". The sentence maker used
the same kind of matrix, one random step at a time.

Which of the three surprised you most? Weather forecasts, sentence
making and ranking for a search engine are, in their arithmetic, the
same few lines.

## Where to Read More

Josh Starmer (StatQuest) (2020). *Markov Chains Clearly Explained! Part 1.*
<https://www.youtube.com/watch?v=i3AkTO9HLXo>. A visual argument for why
repeated multiplication by a transition matrix settles down at all, which
this tutorial only demonstrates numerically.

Brin, S. and Page, L. (1998). *The Anatomy of a Large-Scale Hypertextual Web
Search Engine.* Computer Networks and ISDN Systems, 30(1-7), 107–117.
<http://infolab.stanford.edu/~backrub/google.html>. The original PageRank
paper, from the two Stanford students who wrote it — the small three-page
example in this tutorial is the same mathematics at a readable scale.

Dickens, C. (1859). *A Tale of Two Cities.* The opening sentence, sourced for
the word-transition matrix here, is public domain and among the most
recognisable in English literature — worth reading in full, well beyond
what a Markov chain can copy.

Shannon, C. E. (1948). *A Mathematical Theory of Communication.* Bell System
Technical Journal, 27(3), 379–423. Section 2 builds English text from letter
and word transition frequencies — the origin of the technique used in *Words
That Follow Words*, from 1948.
