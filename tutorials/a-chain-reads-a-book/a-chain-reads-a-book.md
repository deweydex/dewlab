---
title: "A Markov chain from a whole book: a dictionary of dictionaries"
year: "2026-2027"
version: 2026.09.26.1
datasets: [the-time-machine, dracula, dubliners, irish-fairy-tales, treasure-island]
covers:
  loading-a-real-book:
    touches: [CMPS-LO1]
  too-many-words-for-a-grid:
    covers: [CMPS-LO1]
  a-dictionary-of-dictionaries:
    covers: [CMPS-LO4]
  a-chain-from-your-book:
    covers: [CMPS-LO4]
worlds:
  the-time-machine: The Time Machine, by H. G. Wells (1895), a journey to the far future.
  dracula: Dracula, by the Dublin-born writer Bram Stoker (1897), told in letters and diaries.
  dubliners: Dubliners, by James Joyce (1914), fifteen stories set in Dublin.
  irish-fairy-tales: Irish Fairy Tales, by James Stephens (1920), the old stories of Fionn and the Fianna.
  treasure-island: Treasure Island, by Robert Louis Stevenson (1883), pirates and a voyage by sea.
---

# A Markov chain from a whole book: a dictionary of dictionaries

In "Words that follow words", a section of [Markov chains: where
repeated steps
settle](tutorial:where-chains-lead#words-that-follow-words), we built a
Markov chain from one short text. It was a single sentence pattern, "it
was the ___ of ___", repeated ten times. It had 60 words, and only 20
different ones.

On this page we build the same kind of chain from a whole novel, H. G.
Wells's *The Time Machine*. Then you build one from a book you choose. A
whole book brings a real problem that the short text never had. The
grid we used before gets far too big. We solve that with a new way of
storing the chain.

## Loading a real book

The book is already in dewlab's shared data folder. `load_text()` fetches
it in the same way that `load_csv()` fetches a table. The difference is
in what they return. `load_csv()` returns a table. `load_text()` returns
one long string.

```python exec
id: loading-a-real-book-1
raw = await load_text("the-time-machine.txt")
print(len(raw), "characters")
print(raw[:300])
```

The text we just loaded holds more than *The Time Machine*. It comes from
Project Gutenberg, a free online library. Project Gutenberg adds its own
header to the top of every file, and a long licence to the bottom.

The header ends with a line of its own, a few lines further down the
file: `*** START OF THIS PROJECT GUTENBERG EBOOK THE TIME MACHINE ***`.
The novel is everything between that line and a matching `*** END OF...`
line near the bottom. The next cell keeps only that part.

```python exec
id: loading-a-real-book-2
start_marker = "*** START OF THIS PROJECT GUTENBERG EBOOK THE TIME MACHINE ***"
end_marker = "*** END OF THIS PROJECT GUTENBERG EBOOK THE TIME MACHINE ***"
start = raw.find(start_marker)
end = raw.find(end_marker)
book = raw[raw.index("\n", start):end].strip()
print(len(book), "characters of real novel")
print(book[:200])
```

What do you expect the last 200 characters of `book` to be? Can you
change the last line to `print(book[-200:])`, and see?

<details class="dl-answer"><summary>What each line does</summary>

1. `raw.find(start_marker)` gives the position where the start line
   begins. `raw.find(end_marker)` does the same for the end line.
2. `raw.index("\n", start)` looks for the first new line after `start`.
   That is the end of the start line itself.
3. The slice from there to `end` is the novel. So `book` begins on the
   line after the marker, and the marker text is left out.
4. `.strip()` removes the empty lines left at each end.

</details>

Is the licence text really gone? The words "Project Gutenberg" appear
all through it.

```python exec
id: loading-a-real-book-3
print("Project Gutenberg" in book)
```

```predict
type: choice

What will the cell print?

- True
- False
  - The cell cut off Project Gutenberg's header and its licence, so its
    name should be gone.
```

It prints `True`, and many people expect `False`. So something called
Project Gutenberg is still inside the novel. Where? `book.find("Project
Gutenberg")` gives the position where the words first appear, and a
slice from a little before that point shows the rest.

```python exec
id: loading-a-real-book-4
where = book.find("Project Gutenberg")
print(where, "of", len(book), "characters")
print(book[where - 60:])
```

It is the very last line of `book`: *End of the Project Gutenberg EBook
of The Time Machine, by H. G. Wells*. Project Gutenberg put that closing
line before its END marker, not after it, so our slice kept it. Nothing
is broken. The cell did exactly what we asked, and the marker was not
quite where we assumed. So it is worth checking a cleaned text, not
only trusting it. One line of 14 words makes no real difference to a
chain built from more than 32,000 words, so we leave it in.

## Too many words for a grid

In *Words that follow words*, the chain was a transition matrix: a grid
with one row and one column for every different word. Most of the grid
held zeros. A grid worked there because the text had only 20 different
words. How many different words does a whole novel have?

```python exec
id: too-many-words-for-a-grid-1
words = book.split()
states = sorted(set(words))
print(len(words), "words in total")
print(len(states), "distinct words")
print(len(states) ** 2, "cells a dense grid would need")
```

`book.split()` splits the book into words at every space and new line.
`set(words)` keeps one copy of each different word, and `sorted()` puts
them in order. `split()` splits only at spaces, so `"time"` and
`"time,"` count as two different words.

The book has 6,991 different words. A grid with a row and a column for
each one needs 6,991 × 6,991 cells. That is more than 48 million cells,
and almost all of them hold a zero. There is a zero for every pair of
words that never sit next to each other anywhere in the book.

A grid that size is too big for a browser tab to hold in memory. Worse,
to build it, Python must write tens of millions of zeros before a single
real count goes in.

There is another way to write down the same chain. For each word, we
keep a dictionary of only the words that really followed it somewhere in
the book. A dictionary like this never has to store a zero.

## A dictionary of dictionaries

The chain is one big dictionary, and its keys are words. Each value is
another dictionary. That inner dictionary holds every word that followed
the key somewhere in the book, and how many times it did. A dictionary
whose values are dictionaries is called a *dictionary of dictionaries*.

For example, if the book held only "the cat sat on the mat", the chain
would be:

```python
{"the": {"cat": 1, "mat": 1}, "cat": {"sat": 1}, "sat": {"on": 1}, "on": {"the": 1}}
```

Here is the chain for the whole book:

```python exec
id: a-dictionary-of-dictionaries-1
next_words = {}
for word, next_word in zip(words, words[1:]):
    next_words.setdefault(word, {})
    next_words[word][next_word] = next_words[word].get(next_word, 0) + 1

print(len(next_words), "words have at least one dictionary of their own")
print(len(next_words["Weena"]), "different words follow 'Weena' somewhere in the book")
```

Weena is the only person in the far future whom the Time Traveller calls
by name. Her name appears often enough to have many different words
after it. Can you change `"Weena"` to `"the"`, and see how big a very
common word's inner dictionary grows?

<details class="dl-answer"><summary>What each line of the loop does</summary>

- `zip(words, words[1:])` pairs every word with the word after it. We met
  `zip` in [Matrix multiplication: rows times
  columns](tutorial:multiplying-grids). `words[1:]` is the same list with
  the first word left off, so the two lists are one step apart.
- `next_words.setdefault(word, {})` gives `word` an empty inner
  dictionary, but only if it does not have one yet.
- The last line adds 1 to the count for `next_word` inside that inner
  dictionary. `.get(next_word, 0)` returns 0 the first time a pair is seen,
  so there is no need for a separate check.

</details>

The values in each inner dictionary are counts. Each one says how many
times that word followed. They are not probabilities. In *Words that
follow words*, we divided every row by its total to turn counts into
probabilities before `random.choices()` could use them. With a
dictionary we can skip that step, because `random.choices()` accepts
plain counts as weights. It treats a count of 4 as four times as likely
as a count of 1, just as it would with probabilities.

```python exec
id: a-dictionary-of-dictionaries-2
import random

random.seed(1)    # change the 1 to any other number for a different run

def generate(start_word, steps):
    result = [start_word]
    current = start_word
    for _ in range(steps):
        if current not in next_words:
            break
        candidates = next_words[current]
        current = random.choices(list(candidates.keys()), weights=list(candidates.values()))[0]
        result.append(current)
    return " ".join(result)

print(generate("Weena", 20))
```

`random.seed(1)` fixes where the random choices start, so the cell
gives the same sentence every time it runs. Seed 1 gives this:

> Weena was Weena would still remained one by their features, I left her to
> speak of putrefaction and grew visible. “I

Change the 1 to a 2, and run it again. Seed 2 gives this:

> Weena lay awake most of intense relief, I was free from which I thought
> of increasing apprehensions drew her hands, and

Every other seed gives another sentence. Every run mixes the same
32,467 words, but only in the orders that really happen in this one
book. Each pair of words next to each other in the output is a pair
from the book. `for _ in range(steps)` repeats the loop `steps` times.
The name `_` is the usual way to say "we do not need the loop variable".

## A chain from your book

The cleaning above works for one book, because its two marker lines are
typed out in full. Newer Project Gutenberg files write the markers a
little differently, such as
`*** START OF THE PROJECT GUTENBERG EBOOK DRACULA ***`. Every file still
has a line that starts `*** START OF` and one that starts `*** END OF`.

Can you write `strip_gutenberg(raw)`, which keeps what is between the
two marker lines of any Project Gutenberg file? And `chain_from(words)`,
which builds a dictionary of dictionaries from any list of words? Keep
your book's chain as `my_chain`.

<div class="dl-world" data-world="the-time-machine">

Try it on *The Time Machine*: how many different words follow
`"Morlocks"`? With `random.seed(1)`, what does your chain write in 20
words from `"Morlocks"`?

```python exec
id: a-chain-from-your-book-1--the-time-machine
mine = await load_text("the-time-machine.txt")


def strip_gutenberg(raw):
    """The text between the START OF and END OF marker lines."""
    # Your code here.


def chain_from(words):
    """A dictionary of dictionaries: each word, and the words that followed it."""
    # Your code here.
```

```hint
`raw.find("*** START OF")` finds the start line, whatever title follows
it. The rest of `strip_gutenberg` is the cleaning cell above, with the
two new searches. `chain_from` is the loop above, inside a function
that returns the dictionary.
```

```inputs
len(my_chain)
len(my_chain["Morlocks"])
```

```solution
def strip_gutenberg(raw):
    """The text between the START OF and END OF marker lines."""
    start = raw.find("*** START OF")
    end = raw.find("*** END OF")
    return raw[raw.index("\n", start):end].strip()


def chain_from(words):
    """A dictionary of dictionaries: each word, and the words that followed it."""
    chain = {}
    for word, next_word in zip(words, words[1:]):
        chain.setdefault(word, {})
        chain[word][next_word] = chain[word].get(next_word, 0) + 1
    return chain


my_chain = chain_from(strip_gutenberg(mine).split())
random.seed(1)
current, sentence = "Morlocks", ["Morlocks"]
for _ in range(20):
    followers = my_chain[current]
    current = random.choices(list(followers.keys()), weights=list(followers.values()))[0]
    sentence.append(current)
print(" ".join(sentence))
---
The chain has the same 6,991 keys as `next_words`, and 24 different
words follow `"Morlocks"`. With seed 1, the chain writes "Morlocks I
would take for a huge variety of the Time Machine, I stoutly to my
pocket, and grew visible. “I".
```

</div>

<div class="dl-world" data-world="dracula">

Try it on *Dracula*: how many different words does the book have? How
many different words follow `"Count"`? With `random.seed(1)`, what does
your chain write in 20 words from `"Count"`?

```python exec
id: a-chain-from-your-book-1--dracula
mine = await load_text("dracula.txt")


def strip_gutenberg(raw):
    """The text between the START OF and END OF marker lines."""
    # Your code here.


def chain_from(words):
    """A dictionary of dictionaries: each word, and the words that followed it."""
    # Your code here.
```

```hint
`raw.find("*** START OF")` finds the start line, whatever title follows
it. The rest of `strip_gutenberg` is the cleaning cell above, with the
two new searches. `chain_from` is the loop above, inside a function
that returns the dictionary.
```

```inputs
len(my_chain)
len(my_chain["Count"])
```

```solution
def strip_gutenberg(raw):
    """The text between the START OF and END OF marker lines."""
    start = raw.find("*** START OF")
    end = raw.find("*** END OF")
    return raw[raw.index("\n", start):end].strip()


def chain_from(words):
    """A dictionary of dictionaries: each word, and the words that followed it."""
    chain = {}
    for word, next_word in zip(words, words[1:]):
        chain.setdefault(word, {})
        chain[word][next_word] = chain[word].get(next_word, 0) + 1
    return chain


my_chain = chain_from(strip_gutenberg(mine).split())
random.seed(1)
current, sentence = "Count", ["Count"]
for _ in range(20):
    followers = my_chain[current]
    current = random.choices(list(followers.keys()), weights=list(followers.values()))[0]
    sentence.append(current)
print(" ".join(sentence))
---
*Dracula* is about five times as long as *The Time Machine*: 161,321
words, and 18,462 different ones. 66 different words follow `"Count"`.
With seed 1, the chain writes "Count himself see us as though he said.
“When I could take her power draw down soon as others. It seems".
```

</div>

<div class="dl-world" data-world="dubliners">

Try it on *Dubliners*: how many different words does the book have? How
many different words follow `"Gabriel"`, from the last story, *The
Dead*? With `random.seed(1)`, what does your chain write in 20 words
from `"Gabriel"`?

```python exec
id: a-chain-from-your-book-1--dubliners
mine = await load_text("dubliners.txt")


def strip_gutenberg(raw):
    """The text between the START OF and END OF marker lines."""
    # Your code here.


def chain_from(words):
    """A dictionary of dictionaries: each word, and the words that followed it."""
    # Your code here.
```

```hint
`raw.find("*** START OF")` finds the start line, whatever title follows
it. The rest of `strip_gutenberg` is the cleaning cell above, with the
two new searches. `chain_from` is the loop above, inside a function
that returns the dictionary.
```

```inputs
len(my_chain)
len(my_chain["Gabriel"])
```

```solution
def strip_gutenberg(raw):
    """The text between the START OF and END OF marker lines."""
    start = raw.find("*** START OF")
    end = raw.find("*** END OF")
    return raw[raw.index("\n", start):end].strip()


def chain_from(words):
    """A dictionary of dictionaries: each word, and the words that followed it."""
    chain = {}
    for word, next_word in zip(words, words[1:]):
        chain.setdefault(word, {})
        chain[word][next_word] = chain[word].get(next_word, 0) + 1
    return chain


my_chain = chain_from(strip_gutenberg(mine).split())
random.seed(1)
current, sentence = "Gabriel", ["Gabriel"]
for _ in range(20):
    followers = my_chain[current]
    current = random.choices(list(followers.keys()), weights=list(followers.values()))[0]
    sentence.append(current)
print(" ".join(sentence))
---
*Dubliners* has 67,559 words, and 11,949 different ones. 67 different
words follow `"Gabriel"`. With seed 1, the chain writes "Gabriel had two
cases?” “What do a smart moustache, praised the carman, he really had
great Blackwhite, whose expression on the".
```

</div>

<div class="dl-world" data-world="irish-fairy-tales">

Try it on *Irish Fairy Tales*: how many different words does the book
have? How many different words follow `"Fionn"`? With `random.seed(1)`,
what does your chain write in 20 words from `"Fionn"`?

```python exec
id: a-chain-from-your-book-1--irish-fairy-tales
mine = await load_text("irish-fairy-tales.txt")


def strip_gutenberg(raw):
    """The text between the START OF and END OF marker lines."""
    # Your code here.


def chain_from(words):
    """A dictionary of dictionaries: each word, and the words that followed it."""
    # Your code here.
```

```hint
`raw.find("*** START OF")` finds the start line, whatever title follows
it. The rest of `strip_gutenberg` is the cleaning cell above, with the
two new searches. `chain_from` is the loop above, inside a function
that returns the dictionary.
```

```inputs
len(my_chain)
len(my_chain["Fionn"])
```

```solution
def strip_gutenberg(raw):
    """The text between the START OF and END OF marker lines."""
    start = raw.find("*** START OF")
    end = raw.find("*** END OF")
    return raw[raw.index("\n", start):end].strip()


def chain_from(words):
    """A dictionary of dictionaries: each word, and the words that followed it."""
    chain = {}
    for word, next_word in zip(words, words[1:]):
        chain.setdefault(word, {})
        chain[word][next_word] = chain[word].get(next_word, 0) + 1
    return chain


my_chain = chain_from(strip_gutenberg(mine).split())
random.seed(1)
current, sentence = "Fionn", ["Fionn"]
for _ in range(20):
    followers = my_chain[current]
    current = random.choices(list(followers.keys()), weights=list(followers.values()))[0]
    sentence.append(current)
print(" ".join(sentence))
---
*Irish Fairy Tales* has 66,089 words, and 10,417 different ones. 131
different words follow `"Fionn"`, far more than follow any name in the
other books here: Fionn is in almost every story. With seed 1, the chain
writes "Fionn was sung and I charged him. Her lips my pedigree,” Tuan
thoughtfully, “Duv Laca suggested. “Let us keep Becuma Cneisgel,".
```

</div>

<div class="dl-world" data-world="treasure-island">

Try it on *Treasure Island*: how many different words does the book
have? How many different words follow `"Silver"`, as in Long John
Silver? With `random.seed(1)`, what does your chain write in 20 words
from `"Silver"`?

```python exec
id: a-chain-from-your-book-1--treasure-island
mine = await load_text("treasure-island.txt")


def strip_gutenberg(raw):
    """The text between the START OF and END OF marker lines."""
    # Your code here.


def chain_from(words):
    """A dictionary of dictionaries: each word, and the words that followed it."""
    # Your code here.
```

```hint
`raw.find("*** START OF")` finds the start line, whatever title follows
it. The rest of `strip_gutenberg` is the cleaning cell above, with the
two new searches. `chain_from` is the loop above, inside a function
that returns the dictionary.
```

```inputs
len(my_chain)
len(my_chain["Silver"])
```

```solution
def strip_gutenberg(raw):
    """The text between the START OF and END OF marker lines."""
    start = raw.find("*** START OF")
    end = raw.find("*** END OF")
    return raw[raw.index("\n", start):end].strip()


def chain_from(words):
    """A dictionary of dictionaries: each word, and the words that followed it."""
    chain = {}
    for word, next_word in zip(words, words[1:]):
        chain.setdefault(word, {})
        chain[word][next_word] = chain[word].get(next_word, 0) + 1
    return chain


my_chain = chain_from(strip_gutenberg(mine).split())
random.seed(1)
current, sentence = "Silver", ["Silver"]
for _ in range(20):
    followers = my_chain[current]
    current = random.choices(list(followers.keys()), weights=list(followers.values()))[0]
    sentence.append(current)
print(" ".join(sentence))
---
*Treasure Island* has 68,637 words, and 11,318 different ones. 54
different words follow `"Silver"`. With seed 1, the chain writes
"Silver unearthed a crack at once, and walked more dreadful-looking
figure. So far worse that had somewhat cleared away without paying".
```

</div>

## Looking back

A grid worked for 20 different words. A dictionary of dictionaries works
for thousands, because it stores only the pairs that really happen. It
never stores the millions of pairs that do not.

Every sentence on this page came with its seed, so you could make it
again. Why does that matter, for a program whose whole job is to be
random?

A challenge: surprise a classmate. Choose a book, a seed and a start
word, and write down the sentence your chain makes. Give your classmate
only the book, the seed and the start word. Can they make the same
sentence? What else must they do exactly as you did?

```python challenge
import random

raw = await load_text("the-time-machine.txt")
start = raw.find("*** START OF")
end = raw.find("*** END OF")
words = raw[raw.index("\n", start):end].split()

chain = {}
for word, next_word in zip(words, words[1:]):
    chain.setdefault(word, {})
    chain[word][next_word] = chain[word].get(next_word, 0) + 1

random.seed(1)          # your seed
current = "Weena"       # your start word
sentence = [current]
for _ in range(20):
    followers = chain[current]
    current = random.choices(list(followers.keys()), weights=list(followers.values()))[0]
    sentence.append(current)
print(" ".join(sentence))
```

The next tutorial, [N-grams: a Markov chain that remembers more
words](tutorial:how-much-it-remembers), asks a different question. How
much of the sentence so far should the chain remember?

## Where to read more

3Blue1Brown (2024). *Large Language Models explained briefly.*
<https://www.youtube.com/watch?v=LPZh9BOjkQs>. A chatbot also writes one
word at a time, and chooses each word from the words that came before it.
That is the job our chain does with a dictionary. Grant Sanderson shows
what is different inside, in eight minutes.
