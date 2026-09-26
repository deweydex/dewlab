---
title: "Markov chains: where repeated steps settle"
year: "2026-2027"
version: 2026.09.26.1
datasets: [dublin-weather]
covers:
  a-weather-machine:
    covers: [CMPS-LO4]
    touches: [CMPS-LO2]
  watching-it-settle:
    covers: [CMPS-LO4]
  a-chain-from-real-weather:
    covers: [CMPS-LO4]
    touches: [CMPS-LO6]
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
strange happens. After enough steps, the answer stops changing. We say it
settles. It no longer depends on where we started.

This one idea can forecast the weather, rank every page on the web, and
write sentences that nobody has written before. On this page we:

- build a matrix of probabilities for tomorrow's weather
- watch the forecast settle as the days pass
- build a real chain from three years of Dublin's weather
- build the same kind of matrix from a sentence, and use it to write new
  text
- rank three small web pages

## A weather machine

Suppose each day is either sunny or rainy. Suppose also that tomorrow's
weather depends only on today's weather, and not on last week's.

Here are some invented numbers for Dublin. A sunny day is followed by
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
row that holds the probability of each state. `[[1, 0]]` means
"certainly sunny today", and `[[0, 1]]` means "certainly rainy today".

This is a change from the earlier pages. There, a point was a column,
and the matrix went on its left, as in $A\mathbf{x}$. Here the state is
a row, and the matrix goes on its right: `multiply(today, P)`. The
reason is the way `P` is written, with one row for each state today. A
row times `P` takes each row of `P`, weights it by the chance of that
state today, and adds them up. Books on Markov chains nearly always
write the state as a row, so this page does too.

If today is certainly sunny, what do you expect tomorrow's state vector
to be? Run the cell to check.

```python exec
id: a-weather-machine-2
today = [[1, 0]]
tomorrow = multiply(today, P)
print(tomorrow)
```

It prints `[[0.7, 0.3]]`, which is row 1 of `P`.

Now start from a day that is certainly rainy, `[[0, 1]]`. What is
tomorrow's weather, and the day after that?

```python exec
id: a-weather-machine-3
today = [[0, 1]]
```

```hint
The day after tomorrow is tomorrow's state vector multiplied by `P`
again. The state vector changes, and `P` stays the same.
```

```solution
{{include: setup/matrices/multiply.py}}

P = [[0.7, 0.3], [0.4, 0.6]]
today = [[0, 1]]
tomorrow = multiply(today, P)
after = multiply(tomorrow, P)
print(tomorrow)
print(after)
---
Tomorrow is `[[0.4, 0.6]]`, row 2 of `P`. The day after is
`[[0.52, 0.48]]`. The chance of sun is 0.4 × 0.7 from a sunny
tomorrow, plus 0.6 × 0.4 from a rainy one.
```

## Watching it settle

What will the forecast be ten days from now, if today is certainly
sunny?

```predict
Will the chance of sun keep falling, day after day?

- Yes, towards 0
  - Each day removes some of the sun.
- No, it stops somewhere between 0 and 1
  - Rain also turns back into sun, 40% of the time.
- It goes back up to 1
  - The weather goes round in a cycle.
```

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

Does it matter where we start? Run the same ten steps from a day that
is certainly rainy.

```python exec
id: watching-it-settle-2
state = [[0, 1]]
```

```solution
{{include: setup/matrices/multiply.py}}

P = [[0.7, 0.3], [0.4, 0.6]]
state = [[0, 1]]
for day in range(1, 11):
    state = multiply(state, P)
    print(day, [round(v, 4) for v in state[0]])
---
It settles on the same numbers, 0.5714 and 0.4286, from the other side.
The chance of sun starts at 0.4 and rises.
```

The numbers it settles on are the *stationary distribution*. The
stationary distribution is the state vector that stays the same when
we multiply it by `P` again. In symbols, $\boldsymbol{\pi} P =
\boldsymbol{\pi}$, where $\boldsymbol{\pi}$ is the stationary
distribution. It is a fixed point of the whole process.

For a chain like this weather one, the stationary distribution belongs
to the transition matrix itself. It does not depend on where we started.

The NumPy page's `matrix_power` shows this in one line. $P^{10}$ is ten
days at once. Its row 1 is the forecast ten days after a sunny day, and
its row 2 is the forecast ten days after a rainy day.

```python exec
id: watching-it-settle-3
import numpy as np

print(np.round(np.linalg.matrix_power(np.array(P), 10), 4))
```

Both rows are `[0.5714 0.4286]`. After ten days, the start no longer
shows.

## A chain from real weather

The numbers in `P` were invented. NASA keeps a record of Dublin's
weather, one row a day, and it has real ones. It has no column for
rain, but it does have sunlight. That is how much of the Sun's energy
reached each square metre of ground that day.

Call a day *bright* when it had more sunlight than the middle day of
its month, over the three years, and *dull* when it did not. We compare
each day only with its own month, because a dull day in June has more
sunlight than a bright day in December.

```python exec
id: a-chain-from-real-weather-1
text = await load_text("dublin-weather.csv")
rows = []
for line in text.strip().split("\n")[1:]:
    parts = line.split(",")
    rows.append((int(parts[1]), float(parts[6])))

by_month = {}
for month, sun in rows:
    by_month.setdefault(month, []).append(sun)
middle = {month: sorted(suns)[len(suns) // 2] for month, suns in by_month.items()}

bright = [sun > middle[month] for month, sun in rows]
print(len(bright), "days,", sum(bright), "of them bright")
print(bright[:10])
```

Each row of the file is year, month, day, three temperatures and the
sunlight, so `parts[1]` is the month and `parts[6]` is the sunlight.
`middle` holds the middle sunlight of each month, and `bright` holds
`True` or `False` for every day, in order.

If each day were bright or dull at random, a bright day would be
followed by another bright day about half the time. Is it? Can you
count the four kinds of pair (bright then bright, bright then dull,
dull then bright, dull then dull) and make the transition matrix
`P_real`?

```python exec
id: a-chain-from-real-weather-2
counts = [[0, 0], [0, 0]]
```

```hint
`zip(bright, bright[1:])` pairs each day with the next one, as
`zip(words, words[1:])` does below. Use row 0 and column 0 for bright,
and row 1 and column 1 for dull. Then divide each row of `counts` by
its total.
```

```solution
text = await load_text("dublin-weather.csv")
rows = []
for line in text.strip().split("\n")[1:]:
    parts = line.split(",")
    rows.append((int(parts[1]), float(parts[6])))
by_month = {}
for month, sun in rows:
    by_month.setdefault(month, []).append(sun)
middle = {month: sorted(suns)[len(suns) // 2] for month, suns in by_month.items()}
bright = [sun > middle[month] for month, sun in rows]

counts = [[0, 0], [0, 0]]
for today, tomorrow in zip(bright, bright[1:]):
    counts[0 if today else 1][0 if tomorrow else 1] += 1
P_real = [[c / sum(row) for c in row] for row in counts]
print(counts)
print([[round(v, 3) for v in row] for row in P_real])
---
With the copy saved on {{snapshot: dublin-weather}}, the counts are
`[[327, 212], [213, 343]]`, and `P_real` is
`[[0.607, 0.393], [0.383, 0.617]]`. A bright day is followed by another
bright day 61% of the time, not 50%. A dull day is followed by another
dull day 62% of the time. Dublin's weather remembers yesterday, a
little.
```

Where does this chain settle? Add
`print(np.round(np.linalg.matrix_power(np.array(P_real), 10), 3))` to
your cell. Both rows come out close to `[0.493 0.507]`. That is the
share of bright days in the file, 540 of 1,096. It is close to a half
because *bright* means "above the middle day of the month".

This chain is only a model, and the data shows where it falls short.
After two bright days in a row, the next day is bright 65% of the time.
After a dull day and then a bright one, it is bright 55% of the time.
So the day before yesterday matters too. A Markov chain keeps only
today, and a real forecast uses much more.

## Words that follow words

A transition matrix does not have to be about weather. The cells below
build one from a sentence. Every different word is a state. The entry
for word $i$ and word $j$ is the share of times that word $j$ came
straight after word $i$ in the text.

First, the words and the states.

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
print(len(states), "different words")
print(states)
```

1. `text.split()` cuts the text into a list of words.
2. `set(words)` keeps one copy of each different word, and `sorted`
   puts them in alphabetical order. These are the `states`.
3. `index` is a dictionary that gives each word its row number. It is
   built with a dictionary comprehension, which works like a list
   comprehension but makes a dictionary. Comprehensions are in
   [Comprehensions, grids and aliasing](tutorial:comprehensions-and-grids),
   and dictionaries are in
   [Dictionaries: looking things up by name](tutorial:looking-things-up-by-name).

Next, count which word comes after which.

```python exec
id: words-that-follow-words-2
counts = [[0] * len(states) for _ in states]
for word, next_word in zip(words, words[1:]):
    counts[index[word]][index[next_word]] += 1
print(counts[index["it"]])
```

`counts` starts as a grid of zeros, one row and one column for each
word. `zip(words, words[1:])` pairs each word with the word after it.
For each pair, we add 1 to the matching entry in `counts`. The row for
"it" has one number that is not 0: a 10, in the column for "was".

Last, divide each row by its total, so that the row adds up to 1.

```python exec
id: words-that-follow-words-3
P_words = []
for row in counts:
    total = sum(row)
    P_words.append([c / total if total else 0 for c in row])
print("after 'it':", dict(zip(states, [round(v, 2) for v in P_words[index["it"]]])))
```

The last word, "despair", is never followed by anything, so its total
is 0. `if total else 0` leaves its row all zeros, and does not divide
by 0.

Only one word follows "it". It is "was", with a chance of 1. The text
repeats "it was the ___ of ___" ten times. So the matrix has learned
that only one word ever comes after "it".

Which words do you think can follow "the"? The cell below prints only
the words with a chance above zero.

```python exec
id: words-that-follow-words-4
after_the = dict(zip(states, [round(v, 3) for v in P_words[index["the"]]]))
print({k: v for k, v in after_the.items() if v > 0})
```

Some of these words have twice the chance of others. Can you find the
reason in the text the matrix was built from?

<details class="dl-answer"><summary>answer</summary>

"age", "epoch" and "season" each come after "the" twice in the text,
as in "the age of wisdom" and "the age of foolishness". The other four
come after "the" once. "the" appears 10 times, so twice is 0.2 and once
is 0.1.

</details>

Now we can write new text by walking along the chain:

1. Start on a word.
2. Look up its row of probabilities.
3. Pick the next word at random, using those probabilities as weights.
4. Repeat from the new word.

`random.choices(states, weights=row)` picks one word from `states` at
random, so that a word with a bigger weight is picked more often. It
returns a list with one word in it, so `[0]` gets that word.

```python exec
id: words-that-follow-words-5
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

A search engine asks which page the random surfer spends the most time
on, in the long run.

```predict
Which page will the random surfer visit most?

- A
  - Two pages link to A.
- B
  - Two pages link to B as well.
- C
  - Only one page links to C.
```

```python exec
id: ranking-a-small-web-1
P_web = [[0, 0.5, 0.5], [1, 0, 0], [0.5, 0.5, 0]]

visits = [[1/3, 1/3, 1/3]]
for step in range(20):
    visits = multiply(visits, P_web)
print("A, B, C:", [round(v, 4) for v in visits[0]])
```

A comes first, with 4 visits in every 9. Why A? The number of links pointing
at it does not explain it. B has two pages linking to it as well, A and C.
The difference is what those links carry. B has only one link out, so
every surfer on B goes to A next. A and C each split their surfers in
half. A page ranks high when the pages that link to it send it a big
share of their visitors, and when those pages are visited often
themselves.

This is a very small version of *PageRank*, the algorithm that Google
was founded on. PageRank finds the stationary distribution of a
random-surfer Markov chain over the links of the whole web. A page's
rank is the share of the random surfer's time that the page gets, in the
long run. The real PageRank adds one more detail: now and then, the
surfer jumps to a page chosen at random, and does not follow a link.

## Looking back

We met four settings: invented weather, real weather, sentences and web
pages. Underneath all four is one mechanism. We multiply a state by a
matrix of probabilities, then do it again, and again.

For the weather and the web pages, we watched the answer stop depending
on where we started. It settles because of the matrix, and we saw it
before we gave it a name, "stationary distribution". The sentence maker
used the same kind of matrix, one random step at a time.

Can you say, in a sentence of your own, why every row of a transition
matrix adds up to 1, but its columns do not have to?

A challenge: add a fourth page, D, to the small web. D links to A, and
nothing links to D. Where does D rank? Then add a link from C to D, and
look again.

```python challenge
def multiply(a, b):
    columns = [[row[j] for row in b] for j in range(len(b[0]))]
    return [[sum(x * y for x, y in zip(row, column)) for column in columns] for row in a]


P_web = [[0, 0.5, 0.5], [1, 0, 0], [0.5, 0.5, 0]]
visits = [[1/3, 1/3, 1/3]]
for step in range(50):
    visits = multiply(visits, P_web)
print([round(v, 4) for v in visits[0]])
```

## Where to read more

Josh Starmer (StatQuest) (2020). *Markov Chains Clearly Explained! Part 1.*
<https://www.youtube.com/watch?v=i3AkTO9HLXo>. This video shows, in pictures,
why repeated multiplication by a transition matrix settles at all. This
tutorial only shows it with numbers.

Brin, S. and Page, L. (1998). *The Anatomy of a Large-Scale Hypertextual Web
Search Engine.* Computer Networks and ISDN Systems, 30(1-7), 107–117.
<http://infolab.stanford.edu/~backrub/google.html>. This is the original
PageRank paper, by two Stanford students. The small three-page example in
this tutorial uses the same mathematics at a readable scale.

Dickens, C. (1859). *A Tale of Two Cities.* The word-transition matrix here
uses its opening sentence. The book is in the public domain, and its
opening is one of the best known in English literature. It is worth
reading in full.

Shannon, C. E. (1948). *A Mathematical Theory of Communication.* Bell System
Technical Journal, 27(3), 379–423. Section 2 builds English text from letter
and word transition frequencies. The method in *Words that follow words*,
on this page, comes from this paper.

Veritasium (2025). *The Strange Math That Predicts (Almost) Anything.*
<https://www.youtube.com/watch?v=KZeIEiBrT_w>. This video tells how an
argument between two Russian mathematicians led to Markov chains, and where they appeared
later: card shuffling, nuclear physics and web search. About thirty-two
minutes.

Stand-up Maths (2016). *The Mathematics of Winning Monopoly.*
<https://www.youtube.com/watch?v=ubQXz5RBBtU>. Matt Parker and Hannah Fry
treat a Monopoly board as a Markov chain, and find where players settle,
and so which squares are worth buying. About nineteen minutes.
