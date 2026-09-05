---
title: "How Much It Remembers"
slug: how-much-it-remembers
module: computational-methods
module_title: "Computational Methods"
year: "2026-2027"
series: text-generation
version: 2026.09.05.2
datasets: [the-time-machine]
covers:
  keying-on-more-than-one-word:
    covers: [CMPS-LO4]
  comparing-what-each-one-writes:
    touches: [CMPS-LO1]
---

# How Much It Remembers

*A Chain Reads a Book* built a chain that decides what comes next by
looking at exactly one word — whatever word came immediately before. This
tutorial asks what happens if the chain is allowed to remember more than
that.

## Keying On More Than One Word

This is the same book, loaded and cleaned the same way as before.

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

Here is the one-word chain from the previous tutorial again, this time
called `order1`. The name comes from a chain's *order* — how many previous
words it looks at before choosing what comes next.

```python exec
id: keying-on-more-than-one-word-2
order1 = {}
for word, next_word in zip(words, words[1:]):
    order1.setdefault(word, {})
    order1[word][next_word] = order1[word].get(next_word, 0) + 1

print(len(order1["Morlocks"]), "different words have ever followed just 'Morlocks'")
```

Nothing about a dictionary's key has to be a single word. It can just as
easily be a pair, the last *two* words kept together as one key, and the
chain that results remembers one more word of context than before.

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

`order1["Morlocks"]` has 24 different words that have ever followed the
bare word `"Morlocks"`: sometimes the sentence is about what they did,
sometimes about where they live, sometimes just `"and"` or `"were"`.
Narrow the question to `"the Morlocks"` specifically and the field drops
to 17. The extra word of context does more than add memory: it removes
some of the choices that only made sense after a different word than
`"the"`.

### Your turn

`order1` has 6,991 keys — one for every distinct word in the book.
Predict whether `order2` has more keys, fewer keys, or the same number,
before running the cell to check.

```python exec
id: keying-on-more-than-one-word-4
hint: len(order2) counts how many distinct two-word keys exist, the same way len(order1) counted single-word keys.
```

## Comparing What Each One Writes

`generate()` from the previous tutorial walks an `order1` chain one word at
a time. An `order2` chain needs a small change: the current key is a pair,
and after choosing a new word, the key slides forward to keep the *last*
two words rather than growing forever.

```python exec
id: comparing-what-each-one-writes-1
import random

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

Run that cell a few times. One pair of runs produced this:

> order1: the machine below grew scattered, as the eyes glared at work as
> the heavy smell, the appearances of fire. Upon these
>
> order2: the Morlocks their mechanical servants: but that this is what is
> meant by the Morlocks, subterranean for innumerable generations, had
> come to

The `order2` line reads far more like real English — because for long
stretches of it, `("the", "Morlocks")` and the pairs that follow only ever
had one recorded continuation in the whole book, so the chain is not
really choosing at all. "the Morlocks their mechanical servants: but that"
is not a coincidence: that exact phrase appears in the book, word for
word. The more context an `order2` chain remembers, the more often it ends
up reciting a piece of the book it has already seen, rather than
genuinely recombining it.

### Your turn

Generate 20 words from `order1` and 20 words from `order2`, both starting
from a word or pair of your own choosing. Which one reads more like a
sentence a person might write? Which one is more likely to contain a
run of words lifted straight from the book?

```python exec
id: comparing-what-each-one-writes-2
```

## Reflection

More context makes a chain sound more faithful to what it was trained on,
at the cost of sounding less new. Less context makes it sound less
faithful, and more genuinely its own. Neither is simply *better* — a chain
built to write something recognisably in an author's own voice wants more
context; a chain built to surprise wants less. *Whose Voice Is This*, next
in this series, asks how far that faithfulness can go: whether a chain
trained on one writer actually sounds different from a chain trained on
another.
