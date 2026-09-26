---
title: "N-grams: a Markov chain that remembers more words"
year: "2026-2027"
version: 2026.09.25.1
datasets: [the-time-machine]
covers:
  keying-on-more-than-one-word:
    covers: [CMPS-LO4]
  comparing-what-each-one-writes:
    touches: [CMPS-LO1]
---

# N-grams: a Markov chain that remembers more words

In [A Markov chain from a whole book: a dictionary of
dictionaries](tutorial:a-chain-reads-a-book), we built a chain that
chooses the next word by looking at one word only: the word just before
it. What happens if the chain can remember more than that?

## Keying On More Than One Word

Here is the same book, loaded and cleaned in the same way as before.

```python exec
id: keying-on-more-than-one-word-1
raw = await load_text("the-time-machine.txt")
start_marker = "*** START OF THIS PROJECT GUTENBERG EBOOK THE TIME MACHINE ***"
end_marker = "*** END OF THIS PROJECT GUTENBERG EBOOK THE TIME MACHINE ***"
start = raw.find(start_marker)
end = raw.find(end_marker)
book = raw[raw.index("\n", start):end].strip()
words = book.split()
```

Next is the one-word chain from the last tutorial again. This time it is
called `order1`. The *order* of a chain is how many words before it the
chain looks at, when it chooses what comes next. `order1` looks at one.

```python exec
id: keying-on-more-than-one-word-2
order1 = {}
for word, next_word in zip(words, words[1:]):
    order1.setdefault(word, {})
    order1[word][next_word] = order1[word].get(next_word, 0) + 1

print(len(order1["Morlocks"]), "different words have ever followed just 'Morlocks'")
```

A dictionary key does not have to be a single word. It can be a pair of
words, kept together as one key. A chain keyed on pairs remembers the
last *two* words, one more than before.

To keep two words together, we write them in round brackets:
`("the", "Morlocks")`. A *tuple* is a group of values in round brackets,
like this one. A tuple is like a list that cannot be changed after it is
made. Because it cannot change, Python lets us use a tuple as a
dictionary key. A list cannot be a key.

```python exec
id: keying-on-more-than-one-word-3
order2 = {}
for w1, w2, w3 in zip(words, words[1:], words[2:]):
    key = (w1, w2)
    order2.setdefault(key, {})
    order2[key][w3] = order2[key].get(w3, 0) + 1

print(len(order2), "distinct two-word keys")
print(len(order2[("the", "Morlocks")]), "different words have ever followed 'the Morlocks' specifically")
```

This loop is the one from `order1` with one more list in the `zip`. It
walks through the book three words at a time. The first two words make
the key. The third word is the one that followed them.

What do the two cells print? `order1["Morlocks"]` has 24 different words
that have followed `"Morlocks"`. Sometimes the sentence goes on to what
the Morlocks did, like `"had"` or `"came"`. Sometimes it is just `"and"`
or `"were"`. When we ask about `"the Morlocks"` instead, the number
drops to 17. The extra word of context does more than add memory. It
takes away some of the choices that only made sense after a different
word.

These runs of words have a name. A run of $n$ words in a row is an
*n-gram*. A pair of words is a 2-gram, also called a *bigram*, and a run
of three words is a 3-gram, or *trigram*. `order1` counts every bigram in
the book. `order2` counts every trigram. A Markov chain built this way is
often called an *n-gram model*.

### Your turn

`order1` has 6,991 keys, one for every different word in the book. Does
`order2` have more keys, fewer keys, or the same number? Decide what you
think, and why. Then run the cell to check.

```python exec
id: keying-on-more-than-one-word-4
hint: len(order2) counts how many distinct two-word keys exist, the same way len(order1) counted single-word keys.
```

## Comparing What Each One Writes

`generate()` from the last tutorial walks an `order1` chain one word at a
time. An `order2` chain needs a small change. Its key is a pair. After
it chooses a new word, the key moves forward by one word: it drops the
older word and adds the new one. So the key always holds the *last* two
words, and it never grows longer.

```python exec
id: comparing-what-each-one-writes-1
import random

random.seed(1)    # change the 1 to any other number for a different run

def generate1(start_word, steps):
    result = [start_word]
    current = start_word
    for _ in range(steps):
        if current not in order1:
            break
        candidates = order1[current]
        current = random.choices(list(candidates.keys()), weights=list(candidates.values()))[0]
        result.append(current)
    return " ".join(result)

def generate2(w1, w2, steps):
    result = [w1, w2]
    current = (w1, w2)
    for _ in range(steps):
        if current not in order2:
            break
        candidates = order2[current]
        next_word = random.choices(list(candidates.keys()), weights=list(candidates.values()))[0]
        result.append(next_word)
        current = (current[1], next_word)
    return " ".join(result)

print("order1:", generate1("the", 20))
print("order2:", generate2("the", "Morlocks", 20))
```

The line `current = (current[1], next_word)` is the step where the key
moves forward. `current[1]` is the second word of the old key, and
`next_word` is the word just chosen.

Which line reads more like real English? `random.seed(1)` fixes where
the random choices start, so the cell gives the same two lines every
time it runs. Seed 1 gives this:

> order1: the machine below grew scattered, as the eyes glared at work as
> the heavy smell, the appearances of fire. Upon these
>
> order2: the Morlocks taken my Time Machine and the latter, because it
> happens that our consciousness moves intermittently in one hand and the

The `order2` line reads more like real English, at least in stretches.
Why? The first key, `("the", "Morlocks")`, has 17 possible next words.
But 11 of the 20 pairs after it have only one recorded next word in the
whole book. For long stretches, the chain is not choosing at all.

"and the latter, because it happens that our consciousness moves
intermittently in one" is not a coincidence. Those 13 words are in the
book, in that order. Can we check? `in` looks for an exact match, so we
have to be careful. Guess before you run the cell: which line will say
True?

```python exec
id: comparing-what-each-one-writes-check
phrase = "and the latter, because it happens that our consciousness moves intermittently in one"
print(phrase in book)
print(phrase in " ".join(words))
```

The first line says False. In `book`, a line break sits between two of
those words, where the phrase has a space. The second line joins the
words with single spaces, the same way `generate2` does, and says True.

The more context a chain remembers, the more often it recites a piece of
the book it has already seen. With less context, it combines pieces of
the book in new ways.

### Your turn

1. Choose a word to start `order1`, and a pair of words to start
   `order2`.
2. Generate 20 words from each.
3. Which one reads more like a sentence a person might write?
4. Which one is more likely to contain a run of words copied straight
   from the book?

```python exec
id: comparing-what-each-one-writes-2
```

## Reflection

More context makes a chain sound more like the book it learned from, but
less new. Less context makes it sound less like the book, and more like
itself. Neither is simply *better*. Suppose you want a chain that writes
in an author's own voice. Then you want more context. For a chain that
surprises you, you want less.

The next tutorial, [Writing style: comparing two writers with Markov
chains](tutorial:whose-voice-is-this), asks how far that can go. Does a
chain trained on one writer sound different from a chain trained on
another?

## Where to read more

3Blue1Brown (2024). *Large Language Models explained briefly.*
<https://www.youtube.com/watch?v=LPZh9BOjkQs>. A chatbot also chooses each
next word from the words before it, but it looks back much further than
two or three words. Grant Sanderson shows how, in eight minutes.
