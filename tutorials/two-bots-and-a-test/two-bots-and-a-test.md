---
title: "Make it: two bots, and a test that tells them apart"
year: "2026-2027"
version: 2026.09.27.1
datasets: [the-time-machine, dracula, frankenstein, treasure-island]
worlds:
  one-word-or-two: A chain that remembers one word and one that remembers two, both from The Time Machine.
  two-temperatures: One chain from Dracula, writing at a low temperature and at a high one.
  two-books: A chain from Dracula and a chain from Frankenstein.
  bot-or-writer: A chain from Treasure Island, and the real Treasure Island.
---

# Make it: two bots, and a test that tells them apart

This course built bots that write, and ways to score what was written.
Now you make both at once: two bots that write in different ways, and a
test that reads a passage and says which bot wrote it. Then you make
the two bots harder to tell apart, and see whether your test
still can.

## A first step

Every world on this page has the same shape. `writer_a(seed)` and
`writer_b(seed)` each write a passage, as a list of words, from a
stated seed. `test(passage)` reads a passage and answers `"A"` or
`"B"`. `score_test()` gives the test passages from both writers, and
returns the share it names correctly.

Here is that shape with two very simple writers. Both write "yes" and
"no" at random, but writer B writes "yes" three times as often.

```python exec
id: a-first-step-1
import random


def writer_a(seed):
    random.seed(seed)
    return random.choices(["yes", "no"], k=30)


def writer_b(seed):
    random.seed(seed)
    return random.choices(["yes", "no"], weights=[3, 1], k=30)


def test(passage):
    """B writes fewer "no"s, so a passage with fewer than 11 is called B."""
    return "B" if passage.count("no") < 11 else "A"


def score_test(test, writer_a, writer_b, seeds):
    """The share of passages, from both writers, that the test names correctly."""
    right = 0
    for seed in seeds:
        if test(writer_a(seed)) == "A":
            right += 1
        if test(writer_b(seed)) == "B":
            right += 1
    return right / (2 * len(seeds))


print("seeds 0 to 49:", score_test(test, writer_a, writer_b, range(50)))
print("seeds 50 to 99:", score_test(test, writer_a, writer_b, range(50, 100)))
```

The number 11 was chosen by trying 9 to 13 on seeds 0 to 49, and
keeping the best. Choosing it that way is fair, but then a score on
those same seeds is not. A test chosen to suit some passages will
always look good on those passages. So the second line scores it on
seeds 50 to 99, which played no part in choosing it. That is the
held-back text from [Writing style: comparing two writers with Markov
chains](tutorial:whose-voice-is-this) again. Here the test scores 0.93
on the passages it was chosen on, and 0.95 on new ones.

## Bots from books

The bots in the worlds below are chains from books.
`chain_from(words, order)` builds a chain keyed on `order` words at a
time. `write()` writes a passage from a chain at a temperature, as in
[What a language model does differently](tutorial:what-a-language-model-does-differently).
If it reaches a key with no followers, it starts again from a key
chosen at random.

```python exec
id: bots-from-books-1
def strip_gutenberg(raw):
    start = raw.find("*** START OF")
    end = raw.find("*** END OF")
    return raw[raw.index("\n", start):end].strip()


def chain_from(words, order=1):
    """A chain keyed on `order` words at a time, as tuples."""
    chain = {}
    for i in range(len(words) - order):
        key = tuple(words[i:i + order])
        chain.setdefault(key, {})
        chain[key][words[i + order]] = chain[key].get(words[i + order], 0) + 1
    return chain


def write(chain, length, seed, t=1):
    """`length` words from the chain, at temperature t, from a stated seed."""
    random.seed(seed)
    order = len(next(iter(chain)))
    result = list(random.choice(list(chain)))
    while len(result) < length:
        key = tuple(result[-order:])
        if key not in chain:
            result.extend(random.choice(list(chain)))
            continue
        followers = chain[key]
        weights = [count ** (1 / t) for count in followers.values()]
        result.append(random.choices(list(followers), weights=weights)[0])
    return result[:length]
```

## Make it yours

<div class="dl-world" data-world="one-word-or-two">

Two bots from *The Time Machine*: A remembers one word, and B
remembers two. Every three-word run that B writes is copied from the
book, because B only ever adds a word that followed its last two words
somewhere in the book. A's runs are mostly new. The starter test uses
that. It calls a passage B if every one of its three-word runs is in
the book.

Then the cell makes the bots harder to tell apart: A now remembers two
words, and B three. Both copy every three-word run now.

Some questions your test could answer:

- The starter test fails on the harder pair. What could tell a
  two-word bot from a three-word bot? Longer runs, perhaps?
- Can you tell A from B without looking at the book at all?
- How short can a passage be before your test starts to guess?

```python exec
id: make-it-yours-1--one-word-or-two
words = strip_gutenberg(await load_text("the-time-machine.txt")).split()
book_triples = set(zip(words, words[1:], words[2:]))
one_word, two_words, three_words = chain_from(words, 1), chain_from(words, 2), chain_from(words, 3)


def share_of_triples_in_book(passage):
    triples = list(zip(passage, passage[1:], passage[2:]))
    return sum(1 for run in triples if run in book_triples) / len(triples)


def test(passage):
    return "B" if share_of_triples_in_book(passage) == 1 else "A"


writer_a = lambda seed: write(one_word, 30, seed)
writer_b = lambda seed: write(two_words, 30, seed)
print("one word or two:", score_test(test, writer_a, writer_b, range(50, 100)))

writer_a = lambda seed: write(two_words, 30, seed)
writer_b = lambda seed: write(three_words, 30, seed)
print("two words or three:", score_test(test, writer_a, writer_b, range(50, 100)))
```

</div>

<div class="dl-world" data-world="two-temperatures">

One chain from *Dracula*, and two bots: A writes at a temperature of
0.5, and B at 2. A cold bot keeps to the common words, and a hot one
takes rare turns. The starter test counts the share of the passage's
words that appear at least 100 times in the book, and calls it A if
that share is above 0.6.

Then the cell makes the bots harder to tell apart: 0.8 and 1.25, much
closer to each other.

Some questions your test could answer:

- The starter test gets worse on the harder pair. Is 0.6 still the
  best cut-off? Choose a new one on seeds 0 to 49, and score it on 50
  to 99.
- Does a hot bot write longer words? More punctuation?
- How close can the two temperatures be before no test can tell them
  apart?

```python exec
id: make-it-yours-1--two-temperatures
words = strip_gutenberg(await load_text("dracula.txt")).split()
chain = chain_from(words, 1)
counts = {}
for word in words:
    counts[word] = counts.get(word, 0) + 1


def common_share(passage):
    return sum(1 for word in passage if counts.get(word, 0) >= 100) / len(passage)


def test(passage):
    return "A" if common_share(passage) > 0.6 else "B"


writer_a = lambda seed: write(chain, 30, seed, t=0.5)
writer_b = lambda seed: write(chain, 30, seed, t=2)
print("0.5 or 2:", score_test(test, writer_a, writer_b, range(50, 100)))

writer_a = lambda seed: write(chain, 30, seed, t=0.8)
writer_b = lambda seed: write(chain, 30, seed, t=1.25)
print("0.8 or 1.25:", score_test(test, writer_a, writer_b, range(50, 100)))
```

</div>

<div class="dl-world" data-world="two-books">

Two bots: A is a chain from *Dracula*, and B a chain from
*Frankenstein*. The starter test counts how many of the passage's word
pairs appear in each book, and names the book with more.

Then the cell tries a test that never reads either book: it looks only
at the average length of the passage's words.

Some questions your test could answer:

- The book test is hard to beat. How short can a passage be before it
  starts to fail?
- Without reading either book, what else could differ between the two
  bots? Punctuation, capital letters, particular short words?
- Can you combine two weak tests into one stronger one?

```python exec
id: make-it-yours-1--two-books
dracula = strip_gutenberg(await load_text("dracula.txt")).split()
frankenstein = strip_gutenberg(await load_text("frankenstein.txt")).split()
dracula_pairs = set(zip(dracula, dracula[1:]))
frankenstein_pairs = set(zip(frankenstein, frankenstein[1:]))
dracula_chain, frankenstein_chain = chain_from(dracula), chain_from(frankenstein)


def pairs_in(passage, pairs):
    passage_pairs = list(zip(passage, passage[1:]))
    return sum(1 for pair in passage_pairs if pair in pairs) / len(passage_pairs)


def test(passage):
    if pairs_in(passage, dracula_pairs) >= pairs_in(passage, frankenstein_pairs):
        return "A"
    return "B"


def average_length(passage):
    return sum(len(word) for word in passage) / len(passage)


def test_without_books(passage):
    return "A" if average_length(passage) < 4.5 else "B"


writer_a = lambda seed: write(dracula_chain, 30, seed)
writer_b = lambda seed: write(frankenstein_chain, 30, seed)
print("reading the books:", score_test(test, writer_a, writer_b, range(50, 100)))
print("word length only:", score_test(test_without_books, writer_a, writer_b, range(50, 100)))
```

</div>

<div class="dl-world" data-world="bot-or-writer">

A is a bot, and B is Stevenson himself. A is a one-word chain built
from the first nine-tenths of *Treasure Island*. B is a real passage
of 30 words, taken from a random place in the last tenth. Every word
pair that A writes is in the first nine-tenths. Only about half of a
real passage's pairs are. The starter test uses that.

Then the cell makes it harder: the bot is built from the whole book,
and the test checks the whole book too. Now every pair from both
writers is in the book.

Some questions your test could answer:

- The starter test cannot tell them apart on the harder pair. What
  does a real writer do that a one-word chain does not? Look at where
  sentences start and end, and at quotation marks.
- Could a person tell them apart? Print a few passages from each, and
  try it on somebody without saying which is which.
- Does your test still work if the bot remembers two words?

```python exec
id: make-it-yours-1--bot-or-writer
words = strip_gutenberg(await load_text("treasure-island.txt")).split()
cut = int(len(words) * 0.9)
first_part, last_part = words[:cut], words[cut:]


def pairs_in(passage, pairs):
    passage_pairs = list(zip(passage, passage[1:]))
    return sum(1 for pair in passage_pairs if pair in pairs) / len(passage_pairs)


def stevenson(seed):
    """30 real words from a random place in the last tenth of the book."""
    random.seed(seed)
    start = random.randrange(len(last_part) - 30)
    return last_part[start:start + 30]


known_pairs = set(zip(first_part, first_part[1:]))
test = lambda passage: "A" if pairs_in(passage, known_pairs) == 1 else "B"
first_chain = chain_from(first_part)
writer_a = lambda seed: write(first_chain, 30, seed)
print("bot from the first part:", score_test(test, writer_a, stevenson, range(50, 100)))

known_pairs = set(zip(words, words[1:]))
test = lambda passage: "A" if pairs_in(passage, known_pairs) == 1 else "B"
whole_chain = chain_from(words)
writer_a = lambda seed: write(whole_chain, 30, seed)
print("bot from the whole book:", score_test(test, writer_a, stevenson, range(50, 100)))
```

</div>

## Is your test fair?

Before you trust your test's score, ask the questions from [Limits and
judgement: testing what a model can do](tutorial:limits-and-judgement):

- **On what?** Score it on seeds that played no part in designing it.
  The starters use seeds 50 to 99 for that reason.
- **Compared with what?** A test that always says "A" gets 0.5 here,
  since half of the passages come from each writer.
- **On passages like which?** Every passage here has 30 words. Does
  your test still work on 10?

## If you want more

- Can your test say how sure it is, not only "A" or "B"? For example,
  return a number from 0 to 1, and call it A above 0.5.
- Can you make a bot that fools your own test? What did you change?
- Can you make a third bot, and a test that names one of three?

## Show somebody

Show your bots and your test to somebody, or write a few lines for
yourself:

- What are your two bots, and how do they differ?
- What does your test look at, and why did you expect that to differ?
- What was its score on seeds it was not designed on, and what is the
  score of a test that always says "A"?
- When did your test fail, and what did that tell you about the bots?
