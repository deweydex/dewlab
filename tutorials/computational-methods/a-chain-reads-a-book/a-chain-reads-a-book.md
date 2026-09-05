---
title: "A Chain Reads a Book"
slug: a-chain-reads-a-book
module: computational-methods
module_title: "Computational Methods"
year: "2026-2027"
series: text-generation
version: 2026.09.05.2
datasets: [the-time-machine]
covers:
  loading-a-real-book:
    touches: [CMPS-LO1]
  too-many-words-for-a-grid:
    covers: [CMPS-LO1]
  a-dictionary-of-dictionaries:
    covers: [CMPS-LO4]
---

# A Chain Reads a Book

*Words That Follow Words*, in *Where Chains Lead*, built a chain from one
repeated sentence, ten words long. This tutorial builds the same kind of
chain from an entire novel instead, H. G. Wells's *The Time Machine*, and
immediately hits a real technical problem the ten-word version never had.

## Loading a Real Book

This book already lives in dewlab's shared data folder. `load_text()`
fetches it the same way `load_csv()` fetches a table — the difference is
what comes back: a table for `load_csv()`, one long string for `load_text()`.

```python exec
id: loading-a-real-book-1
raw = await load_text("the-time-machine.txt")
print(len(raw), "characters")
print(raw[:300])
```

The text you just loaded includes more than *The Time Machine* itself.
Project Gutenberg, the library this copy comes from, adds its own header
to the top of every file it distributes, and a long licence to the bottom.
Look near the top of what printed above: a few lines down sits
`*** START OF THIS PROJECT GUTENBERG EBOOK THE TIME MACHINE ***`.
Everything from there up to the matching `*** END OF...` line, further down
in the file, is the actual novel.

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

`raw.find(start_marker)` finds where that marker line begins.
`raw.index("\n", start)` then finds the end of that same line, so `book`
starts on the line right after it rather than on the marker text itself.

### Your turn

Check that a phrase from the licence, `"Project Gutenberg"` itself, say,
really is gone from `book`.

```python exec
id: loading-a-real-book-3
hint: The in operator tests whether one string sits inside another — "cat" in "concatenate" is True. "Project Gutenberg" in book should say False.
```

## Too Many Words for a Grid

*Words That Follow Words* built a transition matrix as a grid — one row and
one column for every distinct word, most of the grid holding a zero. That
worked because the toy sentence had ten words. This book does not.

```python exec
id: too-many-words-for-a-grid-1
words = book.split()
states = sorted(set(words))
print(len(words), "words in total")
print(len(states), "distinct words")
print(len(states) ** 2, "cells a dense grid would need")
```

Picture a grid with more than 48 million cells, almost all of them holding
a zero — one for every pair of words that never actually sits next to each
other anywhere in the book. That is not something a browser tab can
comfortably hold in memory, and building it would mean writing tens of
millions of zeros before a single real count goes in.

A different way to write the same idea down solves this: keep one
dictionary for each word, with an entry only for the words that actually
followed it somewhere in the book, instead of one row with an entry for
every other word. A dictionary like this never has to write down a zero.

## A Dictionary of Dictionaries

One dictionary, keyed by word. Each value is itself a dictionary — every
word that followed the key somewhere in the book, and how many times. This
structure has a name: a *dictionary of dictionaries*.

```python exec
id: a-dictionary-of-dictionaries-1
next_words = {}
for word, next_word in zip(words, words[1:]):
    next_words.setdefault(word, {})
    next_words[word][next_word] = next_words[word].get(next_word, 0) + 1

print(len(next_words), "words have at least one dictionary of their own")
print(len(next_words["Weena"]), "different words follow 'Weena' somewhere in the book")
```

`"Weena"` is the one companion the Time Traveller names in the whole book,
a good word to ask about because it appears often enough in the story to
have many neighbours already, without being one of the handful of words
("the", "and", "I") whose dictionaries grow huge from sheer repetition.

Each inner dictionary's values are plain counts, not probabilities — how
many times that word actually followed. *Words That Follow Words* had to
divide every row by its own total to turn counts into probabilities before
`random.choices()` could use them. A dictionary does not need that step:
`random.choices()` accepts raw counts as weights just as happily as it
accepts probabilities that add up to one.

```python exec
id: a-dictionary-of-dictionaries-2
import random

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

Run that cell a few times. One run produced this:

> Weena was Weena would still remained one by their features, I left her to
> speak of putrefaction and grew visible. "I

Another produced this:

> Weena lay awake most of intense relief, I was free from which I thought
> of increasing apprehensions drew her hands, and

Your own run will almost certainly read differently. Every run reshuffles
the same 32,467 words according to what genuinely follows what, word by
word, in this one particular book.

### Your turn

Pick a word that appears often in the book, `"Morlocks"`, say, and generate
20 words starting from it. How many different words follow your chosen
word somewhere in the book?

```python exec
id: a-dictionary-of-dictionaries-3
hint: len(next_words["Morlocks"]) counts how many different words follow "Morlocks" anywhere in the book — the same thing len(next_words["Weena"]) counted above.
```

## Reflection

A grid worked for ten words. A dictionary of dictionaries works for tens
of thousands, because it only ever writes down what genuinely happens,
never the millions of pairs that do not. This series bundles five other
real books alongside this one, too: *The War of the Worlds*,
*Frankenstein*, *A Princess of Mars*, *The Lost World*, and Jane Austen's
*Pride and Prejudice*. The practice page lets you build a chain from any
of them. *How Much It Remembers*, next in this series, asks a different
question: how much of the sentence so far should the chain actually
remember?
