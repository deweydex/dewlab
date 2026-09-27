---
title: "N-grams: a Markov chain that remembers more words — Practice"
practice_for: how-much-it-remembers
year: "2026-2027"
version: 2026.09.26.1
datasets: [the-time-machine, dracula, dubliners, irish-fairy-tales, treasure-island]
worlds:
  the-time-machine: The Time Machine, by H. G. Wells (1895), a journey to the far future.
  dracula: Dracula, by the Dublin-born writer Bram Stoker (1897), told in letters and diaries.
  dubliners: Dubliners, by James Joyce (1914), fifteen stories set in Dublin.
  irish-fairy-tales: Irish Fairy Tales, by James Stephens (1920), the old stories of Fionn and the Fianna.
  treasure-island: Treasure Island, by Robert Louis Stevenson (1883), pirates and a voyage by sea.
---

# N-grams: a Markov chain that remembers more words — Practice

Each answer is hidden until you open it. Write something down first,
even a guess, and then open the answer to compare.

## Tools

Run this cell first. It loads *The Time Machine* and builds both chains,
`order1` and `order2`, with `generate1` and `generate2`, just as the
tutorial did.

```python exec
id: tools-1
import random

raw = await load_text("the-time-machine.txt")
start = raw.find("*** START OF")
end = raw.find("*** END OF")
book = raw[raw.index("\n", start):end].strip()
words = book.split()

order1 = {}
for word, next_word in zip(words, words[1:]):
    order1.setdefault(word, {})
    order1[word][next_word] = order1[word].get(next_word, 0) + 1

order2 = {}
for w1, w2, w3 in zip(words, words[1:], words[2:]):
    key = (w1, w2)
    order2.setdefault(key, {})
    order2[key][w3] = order2[key].get(w3, 0) + 1


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


print(len(order1), "keys in order1,", len(order2), "in order2")
```

## Counting the choices

**1.** In the practice for the last tutorial, about two-thirds of
`order1`'s words had only one recorded follower. What about the pairs in
`order2`?

```python exec
id: counting-the-choices-1
def share_with_one_follower(chain):
    """The share of keys in the chain with exactly one follower."""
    one = [key for key in chain if len(chain[key]) == 1]
    return len(one) / len(chain)


print(round(share_with_one_follower(order1), 3))
print(round(share_with_one_follower(order2), 3))
```

```predict
type: number
tolerance: 0.05

The first line prints 0.665. What will the second line print? A guess to
one decimal place is enough.
```

<details class="dl-answer"><summary>why</summary>

It prints 0.874. For nearly nine pairs in ten, there is only one word
the chain can choose next. One more word of memory removes most of
the choices, so the chain copies the book for longer.

The same function works on both chains. It never looks inside a key, so
it does not matter that one chain's keys are words and the other's are
pairs.

</details>

**2.** In the last practice, `fixed_pairs(chain, at_least)` found words
that are always followed by the same word. It works on `order2` without
a change. How many pairs in `order2` are always followed by the same
word, at least four times? Which are fixed phrases, and which are names?

<details class="dl-answer"><summary>answer</summary>

```python
def fixed_pairs(chain, at_least):
    found = []
    for key, followers in chain.items():
        if len(followers) == 1:
            for follower, count in followers.items():
                if count >= at_least:
                    found.append((key, follower, count))
    return found


print(len(fixed_pairs(order2, 4)))
print(fixed_pairs(order2, 8))
```

There are 18. Three of them:

- `("a", "kind")` is always followed by `"of"`, 11 times. That is the
  fixed phrase `"a kind of"`.
- `("Palace", "of")` is always followed by `"Green"`, 10 times. This one
  is a place in the story, the *Palace of Green Porcelain*. The book
  names it the same way every time.
- `("I", "determined")` is always followed by `"to"`, 8 times. That is
  another fixed phrase, `"I determined to"`.

</details>

## Copied runs

**3.** In the tutorial, the `order2` line copied 13 words in a row from
the book. Can you write `longest_copied_run(sentence, words)`? It takes
a sentence as a list of words, and returns the longest run of them that
appears, in the same order, in `words`.

```python exec
id: copied-runs-1
def longest_copied_run(sentence, words):
    """The longest run of words from sentence that appears, in order, in words."""
    # Your code here.
```

```hint
Join the book into one string with a space at each end:
`" " + " ".join(words) + " "`. The spaces stop half-words from matching.
Then, for each place in the sentence where a run could start, make it
one word longer while it is still in the text.
```

```inputs
longest_copied_run("the heavy smell, the appearances".split(), words)
len(longest_copied_run("the Morlocks taken my Time Machine and the latter, because it happens that our consciousness moves intermittently in one hand and the".split(), words))
longest_copied_run(["Weena", "sang", "zzz"], words)
```

```solution
def longest_copied_run(sentence, words):
    """The longest run of words from sentence that appears, in order, in words."""
    text = " " + " ".join(words) + " "
    best = []
    for i in range(len(sentence)):
        for j in range(i + 1, len(sentence) + 1):
            if " " + " ".join(sentence[i:j]) + " " in text:
                if j - i > len(best):
                    best = sentence[i:j]
            else:
                break
    return best
---
"the heavy smell, the" is in the book, but "the heavy smell, the
appearances" is not, so the first run is 4 words long. The tutorial's
`order2` line gives 13. `"Weena"` is in the book, but `"Weena sang"` is
not. Without the spaces at each end, `"he"` would be found inside
`"the"`.
```

**4.** Use your `longest_copied_run` on sentences from both chains. For
each seed from 1 to 5, generate 25 words from `"the"` with `generate1`,
then 25 words from `("the", "Time")` with `generate2`. Which chain copies
the longer run?

```python exec
id: copied-runs-2
```

<details class="dl-answer"><summary>answer</summary>

```python
for seed in range(1, 6):
    random.seed(seed)
    run1 = longest_copied_run(generate1("the", 25).split(), words)
    run2 = longest_copied_run(generate2("the", "Time", 25).split(), words)
    print(seed, len(run1), len(run2))
```

| seed | `order1` | `order2` |
|---|---|---|
| 1 | 4 | 19 |
| 2 | 5 | 12 |
| 3 | 4 | 13 |
| 4 | 4 | 6 |
| 5 | 3 | 8 |

`order2` copies the longer run every time: between 6 and 19 words,
against 3 to 5 for `order1`. With seed 1, 19 of its 27 words come
straight from the book.

</details>

## Your world

**5.** Build an `order3` chain from your book, keyed on the last
*three* words. Can you write `chain_from3(words)`, and keep your book's
chain as `my_order3`? What share of its keys have only one follower?

<div class="dl-world" data-world="the-time-machine">

```python exec
id: your-world-1--the-time-machine
mine = await load_text("the-time-machine.txt")
start = mine.find("*** START OF")
end = mine.find("*** END OF")
my_words = mine[mine.index("\n", start):end].split()


def chain_from3(words):
    """An order-3 chain: each run of three words, and the words that followed it."""
    # Your code here.
```

```hint
`chain_from3` is the `order2` loop with one more list in the `zip`, and
a key of three words. `share_with_one_follower` from problem 1 works on
it without a change.
```

```inputs
len(my_order3)
round(share_with_one_follower(my_order3), 3)
```

```solution
def chain_from3(words):
    """An order-3 chain: each run of three words, and the words that followed it."""
    chain = {}
    for w1, w2, w3, w4 in zip(words, words[1:], words[2:], words[3:]):
        chain.setdefault((w1, w2, w3), {})
        chain[(w1, w2, w3)][w4] = chain[(w1, w2, w3)].get(w4, 0) + 1
    return chain


my_order3 = chain_from3(my_words)
---
*The Time Machine* gives 30,407 three-word keys. The share with only one
follower climbs with each word of memory: 0.665 for order 1,
0.874 for order 2, and 0.965 for order 3.
```

</div>

<div class="dl-world" data-world="dracula">

```python exec
id: your-world-1--dracula
mine = await load_text("dracula.txt")
start = mine.find("*** START OF")
end = mine.find("*** END OF")
my_words = mine[mine.index("\n", start):end].split()


def chain_from3(words):
    """An order-3 chain: each run of three words, and the words that followed it."""
    # Your code here.
```

```hint
`chain_from3` is the `order2` loop with one more list in the `zip`, and
a key of three words. `share_with_one_follower` from problem 1 works on
it without a change.
```

```inputs
len(my_order3)
round(share_with_one_follower(my_order3), 3)
```

```solution
def chain_from3(words):
    """An order-3 chain: each run of three words, and the words that followed it."""
    chain = {}
    for w1, w2, w3, w4 in zip(words, words[1:], words[2:], words[3:]):
        chain.setdefault((w1, w2, w3), {})
        chain[(w1, w2, w3)][w4] = chain[(w1, w2, w3)].get(w4, 0) + 1
    return chain


my_order3 = chain_from3(my_words)
---
*Dracula* gives 140,951 three-word keys. The share with only one
follower climbs with each word of memory: 0.615 for order 1,
0.82 for order 2, and 0.937 for order 3.
```

</div>

<div class="dl-world" data-world="dubliners">

```python exec
id: your-world-1--dubliners
mine = await load_text("dubliners.txt")
start = mine.find("*** START OF")
end = mine.find("*** END OF")
my_words = mine[mine.index("\n", start):end].split()


def chain_from3(words):
    """An order-3 chain: each run of three words, and the words that followed it."""
    # Your code here.
```

```hint
`chain_from3` is the `order2` loop with one more list in the `zip`, and
a key of three words. `share_with_one_follower` from problem 1 works on
it without a change.
```

```inputs
len(my_order3)
round(share_with_one_follower(my_order3), 3)
```

```solution
def chain_from3(words):
    """An order-3 chain: each run of three words, and the words that followed it."""
    chain = {}
    for w1, w2, w3, w4 in zip(words, words[1:], words[2:], words[3:]):
        chain.setdefault((w1, w2, w3), {})
        chain[(w1, w2, w3)][w4] = chain[(w1, w2, w3)].get(w4, 0) + 1
    return chain


my_order3 = chain_from3(my_words)
---
*Dubliners* gives 61,839 three-word keys. The share with only one
follower climbs with each word of memory: 0.651 for order 1,
0.858 for order 2, and 0.955 for order 3.
```

</div>

<div class="dl-world" data-world="irish-fairy-tales">

```python exec
id: your-world-1--irish-fairy-tales
mine = await load_text("irish-fairy-tales.txt")
start = mine.find("*** START OF")
end = mine.find("*** END OF")
my_words = mine[mine.index("\n", start):end].split()


def chain_from3(words):
    """An order-3 chain: each run of three words, and the words that followed it."""
    # Your code here.
```

```hint
`chain_from3` is the `order2` loop with one more list in the `zip`, and
a key of three words. `share_with_one_follower` from problem 1 works on
it without a change.
```

```inputs
len(my_order3)
round(share_with_one_follower(my_order3), 3)
```

```solution
def chain_from3(words):
    """An order-3 chain: each run of three words, and the words that followed it."""
    chain = {}
    for w1, w2, w3, w4 in zip(words, words[1:], words[2:], words[3:]):
        chain.setdefault((w1, w2, w3), {})
        chain[(w1, w2, w3)][w4] = chain[(w1, w2, w3)].get(w4, 0) + 1
    return chain


my_order3 = chain_from3(my_words)
---
*Irish Fairy Tales* gives 60,031 three-word keys. The share with only one
follower climbs with each word of memory: 0.624 for order 1,
0.844 for order 2, and 0.952 for order 3.
```

</div>

<div class="dl-world" data-world="treasure-island">

```python exec
id: your-world-1--treasure-island
mine = await load_text("treasure-island.txt")
start = mine.find("*** START OF")
end = mine.find("*** END OF")
my_words = mine[mine.index("\n", start):end].split()


def chain_from3(words):
    """An order-3 chain: each run of three words, and the words that followed it."""
    # Your code here.
```

```hint
`chain_from3` is the `order2` loop with one more list in the `zip`, and
a key of three words. `share_with_one_follower` from problem 1 works on
it without a change.
```

```inputs
len(my_order3)
round(share_with_one_follower(my_order3), 3)
```

```solution
def chain_from3(words):
    """An order-3 chain: each run of three words, and the words that followed it."""
    chain = {}
    for w1, w2, w3, w4 in zip(words, words[1:], words[2:], words[3:]):
        chain.setdefault((w1, w2, w3), {})
        chain[(w1, w2, w3)][w4] = chain[(w1, w2, w3)].get(w4, 0) + 1
    return chain


my_order3 = chain_from3(my_words)
---
*Treasure Island* gives 63,025 three-word keys. The share with only one
follower climbs with each word of memory: 0.641 for order 1,
0.855 for order 2, and 0.957 for order 3.
```

</div>

Does `order3` read even more like the book? Try generating from it. It
also fails in a new way. Almost every three-word key has been seen only
once, so the chain can only start from a run of three words that is
already in the book, and then it mostly recites what follows.

## From earlier

**6.** From [Matrix multiplication: rows times
columns](tutorial:multiplying-grids). `zip` pairs lists position by
position. The chains on this page give it lists of different lengths.

```python exec
id: from-earlier-1
for triple in zip("abcd", "abcd"[1:], "abcd"[2:]):
    print(*triple)
```

```predict
type: choice

What will the last line print?

- b c d
- d
  - `zip` keeps going until every string has run out.
```

<details class="dl-answer"><summary>why</summary>

`zip` stops when its shortest list runs out. `"abcd"[2:]` is `"cd"`, only
two letters, so there are two triples. That is why the `order2` loop
never goes past the end of the book: its last triple is the book's last
three words.

</details>

**7.** From [Two names, one list: a closer look at
copying](tutorial:two-names-one-list). The tutorial said a list cannot
be a dictionary key. Run the cell. Why do you think Python refuses?

```python exec
id: from-earlier-2
pair = ["the", "Time"]
chain = {pair: 1}
```

<details class="dl-answer"><summary>answer</summary>

It stops with `TypeError: unhashable type: 'list'`. *Hashable* is
Python's word for a value that can be a key.

Suppose Python did allow it. A list can change after it is made, even
through a different name, as that page showed. If `pair` later became
`["the", "Morlocks"]`, the dictionary would have its count filed under
words the key no longer holds. A tuple cannot change, so it is safe to
use as a key.

</details>
