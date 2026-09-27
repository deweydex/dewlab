---
title: "What a language model does differently"
year: "2026-2027"
version: 2026.09.27.1
datasets: [the-time-machine, dracula, dubliners, irish-fairy-tales, treasure-island]
worlds:
  the-time-machine: The Time Machine, by H. G. Wells (1895), a journey to the far future.
  dracula: Dracula, by the Dublin-born writer Bram Stoker (1897), told in letters and diaries.
  dubliners: Dubliners, by James Joyce (1914), fifteen stories set in Dublin.
  irish-fairy-tales: Irish Fairy Tales, by James Stephens (1920), the old stories of Fionn and the Fianna.
  treasure-island: Treasure Island, by Robert Louis Stevenson (1883), pirates and a voyage by sea.
---

# What a language model does differently

The chains in [A Markov chain from a whole book: a dictionary of
dictionaries](tutorial:a-chain-reads-a-book) write one word at a time.
Each word is chosen by chance, from the words that followed the last
one in a book. A *language model*, the kind of program behind a
chatbot, also writes one piece at a time, and each piece is also
chosen by chance. Some of what it does is what our chain does. Some of
it is different.

This page takes the differences one at a time, and tries each one on a
real book: temperature, recitation, the gaps in a table, scoring a
sentence, pieces smaller than words, and weights that are learned.

## A chain to compare with

The first cell loads *The Time Machine*, and keeps the last tenth of it
back, as in [Writing style: comparing two writers with Markov
chains](tutorial:whose-voice-is-this). The chain learns from the first
nine-tenths only. `strip_gutenberg()` and `chain_from()` are the
functions from the chain page.

```python exec
id: a-chain-to-compare-with-1
import random
import re

raw = await load_text("the-time-machine.txt")


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


words = strip_gutenberg(raw).split()
cut = int(len(words) * 0.9)
train, held = words[:cut], words[cut:]
chain = chain_from(train)
print(len(train), "words to learn from,", len(held), "held back")
```

## Choosing with a temperature

After "the", which word comes next? The chain chooses in proportion to
the counts. The cell prints the five most common followers, with the
share of the time each one comes next.

```python exec
id: choosing-with-a-temperature-1
followers = chain["the"]
total = sum(followers.values())
print(len(followers), "different words follow 'the', in", total, "places")
for word in sorted(followers, key=followers.get, reverse=True)[:5]:
    print(word, followers[word], round(followers[word] / total, 3))
```

"Time" is the most common, but only 62 times in 1,807, a share of
0.034. The chain almost never takes the same turn twice.

A language model has a setting called its *temperature*, which changes
that. Before it chooses, it raises every weight to the power 1 ÷
temperature. At a temperature of 1, nothing changes. Below 1, the common
words become much more common. Above 1, the rare words become more
common. The cell tries three temperatures on the followers of "the", and
then writes 15 words at each, from the same seed.

```python exec
id: choosing-with-a-temperature-2
def with_temperature(counts, t):
    """Each count raised to the power 1 / t."""
    return {word: count ** (1 / t) for word, count in counts.items()}


for t in [0.5, 1, 2]:
    weights = with_temperature(followers, t)
    print("temperature", t, ":", round(weights["Time"] / sum(weights.values()), 3), "of the time, 'Time'")


def generate(chain, start, steps, t=1):
    """Up to `steps` more words from `start`, chosen at temperature t."""
    result = [start]
    current = start
    for _ in range(steps):
        if current not in chain:
            break
        weights = with_temperature(chain[current], t)
        current = random.choices(list(weights), weights=list(weights.values()))[0]
        result.append(current)
    return result


for t in [0.5, 1, 2]:
    random.seed(1)
    print(t, " ".join(generate(chain, "The", 15, t)))
```

At a temperature of 0.5, each count is squared, and "Time" comes next
0.363 of the time, not 0.034. The writing keeps to the book's most
common paths: "The Time Traveller", "the little people". At 2, each
count is replaced by its square root, "Time" falls to 0.006, and the
chain takes rare turns, such as "The thing flame".

A real language model works in the same way. A low temperature makes it
choose the likely words and repeat itself, and a high one makes it take
risks. At a very high temperature, it writes nonsense.

## Nonsense and recitation

[N-grams: a Markov chain that remembers more
words](tutorial:how-much-it-remembers) built a chain that keys on two
words, not one. The cell builds one from the same nine-tenths, and
writes 30 words with each chain. Then `longest_copied()` finds the
longest run of words in the output that appears, word for word, in
the book.

```python exec
id: nonsense-and-recitation-1
def chain2_from(words):
    """A chain keyed on pairs of words."""
    chain = {}
    for w1, w2, next_word in zip(words, words[1:], words[2:]):
        chain.setdefault((w1, w2), {})
        chain[(w1, w2)][next_word] = chain[(w1, w2)].get(next_word, 0) + 1
    return chain


def generate2(chain, w1, w2, steps):
    result = [w1, w2]
    for _ in range(steps):
        key = (result[-2], result[-1])
        if key not in chain:
            break
        followers = chain[key]
        result.append(random.choices(list(followers), weights=list(followers.values()))[0])
    return result


book_text = " " + " ".join(train) + " "


def longest_copied(result):
    """The length of the longest run of words in result that is also in the book."""
    longest = 0
    for i in range(len(result)):
        j = i + longest + 1
        while j <= len(result) and " " + " ".join(result[i:j]) + " " in book_text:
            longest = j - i
            j += 1
    return longest


chain2 = chain2_from(train)
random.seed(1)
one = generate(chain, "The", 30)
random.seed(1)
two = generate2(chain2, "The", "Time", 30)
print("one word: ", " ".join(one))
print("two words:", " ".join(two))
print("longest copied:", longest_copied(one), "and", longest_copied(two))
```

The one-word chain writes nonsense that sounds like the book, and its
longest copied run is 4 words. The two-word chain copies 12 words in a
row: "the Provincial Mayor. “It is simply this. That Space, as our
mathematicians". It is not writing. It is reciting.

## Why a table breaks

Why does the two-word chain recite? Count how many of its keys have
only one follower. After such a key, the chain has no choice to make.

```python exec
id: why-a-table-breaks-1
single = sum(1 for key in chain2 if len(chain2[key]) == 1)
print(single, "of", len(chain2), "two-word keys have only one follower")
print(round(single / len(chain2), 3))
```

```predict
type: number
tolerance: 0.1

The last line is the share of two-word keys with only one follower.
What will it be?
```

0.877: nearly nine keys in ten. Most pairs of words appear only once in
the whole book, so the table knows only one way to continue them.

The held-back tenth shows the other half of the problem. How many of
its word pairs did the one-word chain never see? And how many of its
three-word runs did the two-word chain never see?

```python exec
id: why-a-table-breaks-2
pairs = list(zip(held, held[1:]))
triples = list(zip(held, held[1:], held[2:]))
unseen_pairs = sum(1 for word, next_word in pairs if next_word not in chain.get(word, {}))
unseen_triples = sum(1 for w1, w2, next_word in triples if next_word not in chain2.get((w1, w2), {}))
print(round(unseen_pairs / len(pairs), 3), "of the pairs are new")
print(round(unseen_triples / len(triples), 3), "of the three-word runs are new")
```

In the book's last tenth, 0.613 of the word pairs never appeared in
the first nine-tenths, and 0.905 of the three-word runs never did. For
most of what a writer writes next, the table has no entry at all.

So a table breaks in two ways at once. A longer key gives better
sentences, but more of its keys have one follower, so it recites. And
more of real text is missing from it, so it has nothing to say. A
bigger book helps only slowly. No real language model is a table.

## Scoring a sentence

[Writing style: comparing two writers with Markov
chains](tutorial:whose-voice-is-this) scored a passage by the average
chance the chain gives each next word. A language model is scored by
its *perplexity*, which multiplies the chances. Our first problem is
the word pairs the chain never saw: their chance is 0, and one 0 makes
the whole product 0.

`chance()` fixes that. It trusts the chain 90% of the time, and keeps
10% for any word at all, in proportion to how common the word is in
the book. The `+ 1` gives even a word the book never uses a small
chance. Then `perplexity()` multiplies the chances, and takes the
result to the power −1 ÷ (the number of chances).

```python exec
id: scoring-a-sentence-1
counts = {}
for word in train:
    counts[word] = counts.get(word, 0) + 1


def word_chance(word):
    """How common a word is in the book, never exactly 0."""
    return (counts.get(word, 0) + 1) / (len(train) + len(counts))


def chance(chain, word, next_word, trust=0.9):
    """The chance of next_word after word: mostly the chain, a little of any word."""
    followers = chain.get(word, {})
    from_chain = followers.get(next_word, 0) / sum(followers.values()) if followers else 0
    return trust * from_chain + (1 - trust) * word_chance(next_word)


def perplexity(chain, passage):
    product = 1.0
    for word, next_word in zip(passage, passage[1:]):
        product = product * chance(chain, word, next_word)
    return product ** (-1 / (len(passage) - 1))


mine = "I saw the Time Traveller in the laboratory".split()
yours = perplexity(chain, mine)
backwards = perplexity(chain, list(reversed(mine)))
print("the sentence:", round(yours))
print("backwards:", round(backwards))
print("lower:", "the sentence" if yours < backwards else "backwards")
```

```predict
type: choice

The same eight words, in order and backwards. Which one will have the
lower perplexity?

- lower: the sentence
- lower: backwards
  - The same words are in both, but the chain's chances depend on the
    order.
```

The sentence has a perplexity of 30, and the same words backwards
have 1,156. A perplexity of 30 means the chain was, on average, as
unsure as if it were choosing among 30 equally likely words at each
step. Lower means less surprised.

A test on one sentence proves little. The next cell takes every
20-word passage in the held-back tenth, shuffles a copy of each, and
counts how often the real passage has the lower perplexity.

```python exec
id: scoring-a-sentence-2
random.seed(2)
lower = 0
tried = 0
for start in range(0, len(held) - 20 + 1, 20):
    passage = held[start:start + 20]
    shuffled = passage[:]
    random.shuffle(shuffled)
    tried += 1
    if perplexity(chain, passage) < perplexity(chain, shuffled):
        lower += 1
print(lower, "of", tried)
```

The real passage wins 154 times out of 162. The chain has never seen
these passages, but it can still tell real writing from the same
words in a random order.

## Pieces smaller than words

In the held-back tenth, about a quarter of the different words never
appear anywhere in the first nine-tenths. Our chain can never write
them. A language model does not work in whole words. It works in
*tokens*: pieces of words, chosen so that common words are one piece
and rare words are several.

One way to choose the pieces is called *byte-pair encoding*. Start
with single letters. Find the pair of pieces that sit next to each
other most often in the book, and join them into one new piece. Do
that again, and again. The cell does it 100 times, on the book's words
in lower case, and prints the first 20 new pieces.

```python exec
id: pieces-smaller-than-words-1
word_counts = {}
for word in re.findall("[a-z]+", " ".join(train).lower()):
    word_counts[word] = word_counts.get(word, 0) + 1
pieces = {word: list(word) for word in word_counts}


def merge(parts, pair):
    """Join every place where the two pieces of `pair` sit side by side."""
    new = []
    i = 0
    while i < len(parts):
        if i + 1 < len(parts) and (parts[i], parts[i + 1]) == pair:
            new.append(parts[i] + parts[i + 1])
            i += 2
        else:
            new.append(parts[i])
            i += 1
    return new


merges = []
for _ in range(100):
    pair_counts = {}
    for word, count in word_counts.items():
        parts = pieces[word]
        for pair in zip(parts, parts[1:]):
            pair_counts[pair] = pair_counts.get(pair, 0) + count
    best = max(pair_counts, key=pair_counts.get)
    merges.append(best)
    for word in word_counts:
        pieces[word] = merge(pieces[word], best)

print(["".join(pair) for pair in merges[:20]])
```

The first pieces are the commonest parts of English: "th", then "the",
"in", "an", "re". By the 16th, "ing" is a piece of its own. Now split
some words from the held-back tenth that the book never used before:

```python exec
id: pieces-smaller-than-words-2
def split(word):
    """A word, split into the pieces the merges have made."""
    parts = list(word)
    for pair in merges:
        parts = merge(parts, pair)
    return parts


held_words = set(re.findall("[a-z]+", " ".join(held).lower()))
new_words = [word for word in held_words if word not in word_counts]
print(len(new_words), "of", len(held_words), "held-back words were never seen whole")
for word in ["waving", "stalked", "gleaming", "corrugated", "ornamented"]:
    print(word, split(word))
```

260 of the 1,043 different words were never seen whole, but every one
of them can be written from pieces: "gleaming" is g, le, a, m, ing,
and "ornamented" is or, n, a, m, ent, ed. A model that writes pieces
never meets a word it cannot write, even a word nobody has written
before. Real models make tens of thousands of pieces, not 100. GPT-2,
a language model from 2019, had 50,257.

## The learned half

Our chain is a table. It stores what it counted, and nothing else. So
it has nothing to say about a pair it never saw, and after a key with
one follower, it has no choice at all.

A language model keeps no table of counts. Like the perceptron in [The
perceptron: a model that learns from its
mistakes](tutorial:a-model-that-corrects-itself), it has weights,
numbers that multiply its inputs, and it learns them in a similar way.
It reads some text, gives its chances for the next piece, and then
moves its weights a little towards the piece that really came next.
That is repeated over an enormous amount of text. A language model is
far bigger than one perceptron, with many layers of weights, but the
idea is the same: after each guess, move the numbers a little towards
the right answer.

The weights can do what the table cannot. After training, words used in
similar places have similar weights. So a model that has read "the dog
ran" and "the cat sat" can give a sensible chance to "the dog sat", even
if it never read those words together. Our table can do nothing with a
pair it never saw, except use how common the word is, as `chance()`
does.

## Your world

Can you write `one_follower_share(chain)`? It returns the share of the
chain's keys that have exactly one follower. It should work for a
one-word chain and a two-word chain alike.

<div class="dl-world" data-world="the-time-machine">

The cell builds both chains from the first nine-tenths of *The Time
Machine*.

```python exec
id: your-world-1--the-time-machine
mine = await load_text("the-time-machine.txt")
my_words = strip_gutenberg(mine).split()
my_train = my_words[:int(len(my_words) * 0.9)]
my_chain = chain_from(my_train)
my_chain2 = chain2_from(my_train)


def one_follower_share(chain):
    """The share of the chain's keys that have exactly one follower."""
    # Your code here.
```

```hint
Count the keys whose inner dictionary has a length of 1, and divide
by the number of keys.
```

```inputs
round(one_follower_share(my_chain), 3)
round(one_follower_share(my_chain2), 3)
```

```solution
def one_follower_share(chain):
    """The share of the chain's keys that have exactly one follower."""
    single = 0
    for key in chain:
        if len(chain[key]) == 1:
            single += 1
    return single / len(chain)
---
0.674 of the one-word keys and 0.877 of the two-word keys have one follower. *The Time Machine* is the shortest of the five books. Would a longer book have fewer one-follower keys? Try another book to see.
```

</div>

<div class="dl-world" data-world="dracula">

The cell builds both chains from the first nine-tenths of *Dracula*.

```python exec
id: your-world-1--dracula
mine = await load_text("dracula.txt")
my_words = strip_gutenberg(mine).split()
my_train = my_words[:int(len(my_words) * 0.9)]
my_chain = chain_from(my_train)
my_chain2 = chain2_from(my_train)


def one_follower_share(chain):
    """The share of the chain's keys that have exactly one follower."""
    # Your code here.
```

```hint
Count the keys whose inner dictionary has a length of 1, and divide
by the number of keys.
```

```inputs
round(one_follower_share(my_chain), 3)
round(one_follower_share(my_chain2), 3)
```

```solution
def one_follower_share(chain):
    """The share of the chain's keys that have exactly one follower."""
    single = 0
    for key in chain:
        if len(chain[key]) == 1:
            single += 1
    return single / len(chain)
---
0.618 of the one-word keys and 0.822 of the two-word keys have one follower. *Dracula* is about five times as long as *The Time Machine*, whose shares are 0.674 and 0.877. Five times the text lowers the share of two-word keys with one follower by only about 0.05.
```

</div>

<div class="dl-world" data-world="dubliners">

The cell builds both chains from the first nine-tenths of *Dubliners*.

```python exec
id: your-world-1--dubliners
mine = await load_text("dubliners.txt")
my_words = strip_gutenberg(mine).split()
my_train = my_words[:int(len(my_words) * 0.9)]
my_chain = chain_from(my_train)
my_chain2 = chain2_from(my_train)


def one_follower_share(chain):
    """The share of the chain's keys that have exactly one follower."""
    # Your code here.
```

```hint
Count the keys whose inner dictionary has a length of 1, and divide
by the number of keys.
```

```inputs
round(one_follower_share(my_chain), 3)
round(one_follower_share(my_chain2), 3)
```

```solution
def one_follower_share(chain):
    """The share of the chain's keys that have exactly one follower."""
    single = 0
    for key in chain:
        if len(chain[key]) == 1:
            single += 1
    return single / len(chain)
---
0.659 of the one-word keys and 0.862 of the two-word keys have one follower. *Dubliners* is about twice as long as *The Time Machine*, whose shares are 0.674 and 0.877. Twice the text lowers them only a little.
```

</div>

<div class="dl-world" data-world="irish-fairy-tales">

The cell builds both chains from the first nine-tenths of *Irish Fairy
Tales*.

```python exec
id: your-world-1--irish-fairy-tales
mine = await load_text("irish-fairy-tales.txt")
my_words = strip_gutenberg(mine).split()
my_train = my_words[:int(len(my_words) * 0.9)]
my_chain = chain_from(my_train)
my_chain2 = chain2_from(my_train)


def one_follower_share(chain):
    """The share of the chain's keys that have exactly one follower."""
    # Your code here.
```

```hint
Count the keys whose inner dictionary has a length of 1, and divide
by the number of keys.
```

```inputs
round(one_follower_share(my_chain), 3)
round(one_follower_share(my_chain2), 3)
```

```solution
def one_follower_share(chain):
    """The share of the chain's keys that have exactly one follower."""
    single = 0
    for key in chain:
        if len(chain[key]) == 1:
            single += 1
    return single / len(chain)
---
0.631 of the one-word keys and 0.849 of the two-word keys have one follower. These are a little lower than the shares for *Dubliners*, a book of about the same length. Perhaps Stephens repeats his phrases more, as the old stories do. How could you test that?
```

</div>

<div class="dl-world" data-world="treasure-island">

The cell builds both chains from the first nine-tenths of *Treasure
Island*.

```python exec
id: your-world-1--treasure-island
mine = await load_text("treasure-island.txt")
my_words = strip_gutenberg(mine).split()
my_train = my_words[:int(len(my_words) * 0.9)]
my_chain = chain_from(my_train)
my_chain2 = chain2_from(my_train)


def one_follower_share(chain):
    """The share of the chain's keys that have exactly one follower."""
    # Your code here.
```

```hint
Count the keys whose inner dictionary has a length of 1, and divide
by the number of keys.
```

```inputs
round(one_follower_share(my_chain), 3)
round(one_follower_share(my_chain2), 3)
```

```solution
def one_follower_share(chain):
    """The share of the chain's keys that have exactly one follower."""
    single = 0
    for key in chain:
        if len(chain[key]) == 1:
            single += 1
    return single / len(chain)
---
0.646 of the one-word keys and 0.857 of the two-word keys have one follower. *Treasure Island* is about twice as long as *The Time Machine*, whose shares are 0.674 and 0.877. Twice the text lowers them only a little.
```

</div>

## Where to read more

Jurafsky, D. and Martin, J. H. (2026). *Speech and Language
Processing* (3rd edition, draft of 19 August 2026). Chapter 3, "N-gram
Language Models". <https://web.stanford.edu/~jurafsky/slp3/>. A free
textbook chapter on chains like ours. It covers perplexity, the
problem of word pairs never seen, and ways to give them a small
chance.

Sennrich, R., Haddow, B. and Birch, A. (2016). *Neural Machine
Translation of Rare Words with Subword Units.* Proceedings of the 54th
Annual Meeting of the Association for Computational Linguistics. This
is the paper that brought byte-pair encoding to language models, for
the same reason as this page: rare and new words.
