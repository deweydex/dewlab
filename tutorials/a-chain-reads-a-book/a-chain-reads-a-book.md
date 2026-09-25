---
title: "A Markov chain from a whole book: a dictionary of dictionaries"
year: "2026-2027"
version: 2026.09.25.1
datasets: [the-time-machine]
covers:
  loading-a-real-book:
    touches: [CMPS-LO1]
  too-many-words-for-a-grid:
    covers: [CMPS-LO1]
  a-dictionary-of-dictionaries:
    covers: [CMPS-LO4]
---

# A Markov chain from a whole book: a dictionary of dictionaries

In "Words that follow words", a section of [Markov chains: where
repeated steps settle](tutorial:where-chains-lead#words-that-follow-words), we built a Markov chain from one short
text. It was a single sentence pattern, "it was the ___ of ___", repeated
ten times: 60 words, and only 20 different ones.

On this page we build the same kind of chain from a whole novel, H. G.
Wells's *The Time Machine*. A whole book brings a real problem that the
short text never had. The grid we used before gets far too big. We solve
that with a new way of storing the chain.

## Loading a Real Book

The book is already in dewlab's shared data folder. `load_text()` fetches
it in the same way that `load_csv()` fetches a table. The difference is
what comes back. `load_csv()` gives back a table. `load_text()` gives back
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

Look at the top of what printed. The header ends with a line of its own,
a few lines further down the file:
`*** START OF THIS PROJECT GUTENBERG EBOOK THE TIME MACHINE ***`. The
novel is everything between that line and a matching `*** END OF...`
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

Here is what the cell does, one step at a time:

1. `raw.find(start_marker)` gives the position where the start line
   begins. `raw.find(end_marker)` does the same for the end line.
2. `raw.index("\n", start)` looks for the first new line after `start`.
   That is the end of the start line itself.
3. The slice from there to `end` is the novel. So `book` begins on the
   line after the marker, and the marker text is left out.
4. `.strip()` removes the empty lines left at each end.

### Your turn

Is the licence text really gone? The words `"Project Gutenberg"` appear
all through it. Before you run anything, guess: is
`"Project Gutenberg" in book` True or False? Then check.

```python exec
id: loading-a-real-book-3
hint: The in operator tests whether one string sits inside another. "cat" in "concatenate" is True.
```

Did you get True? Most people expect False. So something called Project
Gutenberg is still inside the novel. Where? `book.find("Project Gutenberg")`
gives the position where the words first appear, and a slice from a
little before that point shows the rest.

```python exec
id: loading-a-real-book-4
where = book.find("Project Gutenberg")
print(where, "of", len(book), "characters")
print(book[where - 60:])
```

It is the very last line of `book`: *End of the Project Gutenberg EBook
of The Time Machine, by H. G. Wells*. Project Gutenberg put that closing
line before its END marker, not after it, so our slice kept it. Nothing
is broken. The cell did exactly what we asked. The marker was just not
quite where we assumed. That is the reason to check a cleaned text,
and not only trust it. One line of 14 words makes no real difference to
a chain built from more than 32,000 words, so we leave it in.

## Too Many Words for a Grid

In *Words That Follow Words*, the chain was a transition matrix: a grid
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

`book.split()` cuts the book into words at every space and new line.
`set(words)` keeps one copy of each different word, and `sorted()` puts
them in order. One thing to know: `split()` cuts only at spaces, so
`"time"` and `"time,"` count as two different words.

The book has 6,991 different words. A grid with a row and a column for
each one needs 6,991 × 6,991 cells. That is more than 48 million cells,
and almost all of them hold a zero. There is a zero for every pair of
words that never sit next to each other anywhere in the book.

A grid that size is too big for a browser tab to hold in memory. Worse,
building it means writing tens of millions of zeros before a single real
count goes in.

There is another way to write down the same chain. For each word, we
keep a dictionary of only the words that really followed it somewhere in
the book. A dictionary like this never has to store a zero.

## A Dictionary of Dictionaries

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

What each line of the loop does:

- `zip(words, words[1:])` pairs every word with the word after it. We met
  `zip` in [Matrix multiplication: rows times columns](tutorial:multiplying-grids). `words[1:]`
  is the same list with the first word left off, so the two lists are
  one step apart.
- `next_words.setdefault(word, {})` gives `word` an empty inner
  dictionary, but only if it does not have one yet.
- The last line adds 1 to the count for `next_word` inside that inner
  dictionary. `.get(next_word, 0)` gives 0 the first time a pair is seen,
  so there is no need for a separate check.

Why ask about `"Weena"`? Weena is the only person in the far future whom
the Time Traveller calls by name. Her name appears often enough to have
many different words after it. It is also not one of the very common
words, like "the", "and" or "I", whose inner dictionaries grow huge.

The values in each inner dictionary are counts: how many times that word
followed. They are not probabilities. In *Words That Follow Words*, we
divided every row by its total to turn counts into probabilities before
`random.choices()` could use them. With a dictionary we can skip that
step, because `random.choices()` accepts plain counts as weights. It
treats a count of 4 as four times as likely as a count of 1, just as it
would with probabilities.

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

`for _ in range(steps)` repeats the loop `steps` times. The name `_` is
the usual way to say "we do not need the loop variable".

`random.seed(1)` fixes where the random choices start, so the cell
gives the same sentence every time it runs. Seed 1 gives this:

> Weena was Weena would still remained one by their features, I left her to
> speak of putrefaction and grew visible. “I

Change the 1 to a 2, and run it again. Seed 2 gives this:

> Weena lay awake most of intense relief, I was free from which I thought
> of increasing apprehensions drew her hands, and

Every other seed gives another sentence. Every run mixes up the same
32,467 words, but always by what really follows what in this
one book. Each pair of words next to each other in the output is a pair
from the book.

### Your turn

1. Pick a word that appears often in the book, `"Morlocks"`, for example.
2. Generate 20 words starting from it.
3. How many different words follow your word somewhere in the book?

```python exec
id: a-dictionary-of-dictionaries-3
hint: len(next_words["Morlocks"]) counts how many different words follow "Morlocks" anywhere in the book — the same thing len(next_words["Weena"]) counted above.
```

## Reflection

A grid worked for 20 different words. A dictionary of dictionaries works
for thousands, because it stores only the pairs that really happen. It
never stores the millions of pairs that do not.

This series comes with five other real books as well as this one: *The
War of the Worlds*, *Frankenstein*, *A Princess of Mars*, *The Lost
World*, and Jane Austen's *Pride and Prejudice*. On the practice page you
can build a chain from any of them.

The next tutorial, [N-grams: a Markov chain that remembers more
words](tutorial:how-much-it-remembers), asks a different question. How
much of the sentence so far should the chain remember?
