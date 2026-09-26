---
title: "Writing style: comparing two writers with Markov chains — Practice"
practice_for: whose-voice-is-this
year: "2026-2027"
version: 2026.09.26.1
datasets: [democracy-and-education, the-montessori-method, dracula, frankenstein, treasure-island, the-lost-world]
worlds:
  dewey-and-montessori: John Dewey and Maria Montessori, two writers on education, from the same few years.
  stoker-and-shelley: Bram Stoker's Dracula (1897) and Mary Shelley's Frankenstein (first published 1818), two tales of horror.
  stevenson-and-doyle: Robert Louis Stevenson's Treasure Island (1883) and Arthur Conan Doyle's The Lost World (1912), two adventures.
---

# Writing style: comparing two writers with Markov chains — Practice

Each answer is hidden until you open it. Write something down first,
even a guess, and then open the answer to compare.

## Tools

Run this cell first. It loads and cleans both books in the same way as
the tutorial, builds a chain from each whole book, and builds the two
chains from nine-tenths of each book, with `score()`.

```python exec
id: tools-1
import random

dewey_raw = await load_text("democracy-and-education.txt")
dewey_marker = "EDUCATION AS A NECESSITY OF LIFE"
dewey_first = dewey_raw.find(dewey_marker)
dewey_second = dewey_raw.find(dewey_marker, dewey_first + 1)
dewey_end = dewey_raw.find("INDEX")
dewey_book = dewey_raw[dewey_second:dewey_end].strip()


def clean_scan(text):
    """Remove blank lines and page headers, then join words split at a line end."""
    kept = []
    for line in text.split("\n"):
        words = line.split()
        if not words:
            continue
        if len(words) <= 8 and (words[0].isdigit() or words[-1].isdigit()):
            continue
        kept.append(line.strip())
    return "\n".join(kept).replace("-\n", "")


dewey_book = clean_scan(dewey_book)

montessori_raw = await load_text("the-montessori-method.txt")
montessori_marker = "A CRITICAL CONSIDERATION OF THE NEW PEDAGOGY IN ITS RELATION TO"
montessori_first = montessori_raw.find(montessori_marker)
montessori_second = montessori_raw.find(montessori_marker, montessori_first + 1)
montessori_book = montessori_raw[montessori_second:].strip()


def build_chain(book_text):
    words = book_text.split()
    chain = {}
    for word, next_word in zip(words, words[1:]):
        chain.setdefault(word, {})
        chain[word][next_word] = chain[word].get(next_word, 0) + 1
    return chain


def generate(chain, start_word, steps):
    result = [start_word]
    current = start_word
    for _ in range(steps):
        if current not in chain:
            break
        candidates = chain[current]
        current = random.choices(list(candidates.keys()), weights=list(candidates.values()))[0]
        result.append(current)
    return " ".join(result)


def score(chain, passage):
    """The average probability the chain gives each next word in the passage."""
    probabilities = []
    for word, next_word in zip(passage, passage[1:]):
        followers = chain.get(word, {})
        if next_word in followers:
            probabilities.append(followers[next_word] / sum(followers.values()))
        else:
            probabilities.append(0)
    return sum(probabilities) / len(probabilities)


dewey_chain = build_chain(dewey_book)
montessori_chain = build_chain(montessori_book)

dewey_words = dewey_book.split()
montessori_words = montessori_book.split()
dewey_cut = int(len(dewey_words) * 0.9)
montessori_cut = int(len(montessori_words) * 0.9)
dewey_train = build_chain(" ".join(dewey_words[:dewey_cut]))
montessori_train = build_chain(" ".join(montessori_words[:montessori_cut]))
dewey_held = dewey_words[dewey_cut:]
montessori_held = montessori_words[montessori_cut:]
print("ready")
```

## Comparing one word

**1.** How varied is each writer's use of `"child"`? Can you write
`variety(chain, word)`? It returns the number of different words that
follow `word`, divided by the number of times `word` is followed by
anything at all. A smaller answer means the same followers return
more often.

```python exec
id: comparing-one-word-1
def variety(chain, word):
    """Different followers of word, per use of word."""
    # Your code here.
```

```hint
`len(chain[word])` counts the different followers.
`sum(chain[word].values())` counts every use.
```

```inputs
round(variety(dewey_chain, "child"), 2)
round(variety(montessori_chain, "child"), 2)
variety({"a": {"b": 3, "c": 1}}, "a")
```

```solution
def variety(chain, word):
    """Different followers of word, per use of word."""
    return len(chain[word]) / sum(chain[word].values())
---
Dewey has 38 different followers in 53 uses, about 0.72. Montessori has
230 in 604, about 0.38. So Montessori looks more repetitive. Problem 2
asks whether that is a fair test.
```

**2.** Is that a fair test? The more times anybody uses a word, the
more its followers repeat, because only so many words can sensibly come
next. Montessori writes `"child"` 604 times, and Dewey 53. How could you
compare them fairly?

<details class="dl-answer"><summary>answer</summary>

A fair test compares both writers in the same way. Take 53 of
Montessori's 604 uses, at random, as many as Dewey has, and count how
many different followers they have. Then do that a thousand times:

```python
random.seed(1)
uses = []
for follower, count in montessori_chain["child"].items():
    uses = uses + [follower] * count

counts = [len(set(random.sample(uses, 53))) for _ in range(1000)]
print(sum(counts) / len(counts))
```

The average is about 37. Dewey's 53 uses have 38. So, compared fairly,
the two writers use `"child"` with about the same variety. The first
difference came from *how often* each one wrote the word, not from how.

The difference is in *which* words come next:

```python
print(sorted(montessori_chain["child"].items(), key=lambda kv: -kv[1])[:3])
print(sorted(dewey_chain["child"].items(), key=lambda kv: -kv[1])[:3])
```

In Montessori, `"to"`, `"is"` and `"who"` follow `"child"` 50, 42 and 32
times. In Dewey, the top three are `"and"`, `"is"` and `"has"`, only 5,
5 and 4 times each.

</details>

## Comparing the whole vocabulary

**3.** How many different words appear in *both* chains? How many appear
in only one of them? Can you write `overlap(chain_a, chain_b)`, which
returns the three numbers: shared, only in `chain_a`, only in `chain_b`?

```python exec
id: comparing-the-whole-vocabulary-1
def overlap(chain_a, chain_b):
    """How many keys are shared, only in chain_a, and only in chain_b."""
    # Your code here.
```

```hint
`set(chain_a)` is the set of its keys. `&` between two sets keeps what
they share, and `-` keeps what is only in the set on the left.
```

```inputs
overlap(dewey_chain, montessori_chain)
overlap({"a": {}, "b": {}}, {"b": {}, "c": {}})
```

```solution
def overlap(chain_a, chain_b):
    """How many keys are shared, only in chain_a, and only in chain_b."""
    a = set(chain_a)
    b = set(chain_b)
    return len(a & b), len(a - b), len(b - a)
---
5,099 words are in both. 9,284 appear only in Dewey, and 9,294 only in
Montessori. So two books on a related subject share less than half of
their words. Before `clean_scan`, about 1,700 more words counted as
"only in Dewey": halves of words the printer had split at the end of a
line, such as `environ-`. And `split()` splits only at spaces, so some
of the words "only in Dewey" are words Montessori also uses, with
different punctuation next to them.
```

**4.** Pick a word that both books use.

1. Generate 20 words from each writer's chain, starting from that word.
2. Read them side by side. What do you notice?

```python exec
id: comparing-the-whole-vocabulary-2
```

## Whose passage is it?

**5.** This passage is Dewey's, from the part of his book that the
chains did not see. Montessori's chain gives it the higher score. Read
it first. Why might that be?

```python exec
id: whose-passage-is-it-1
passage = dewey_held[2600:2700]
print(" ".join(passage))
print("Dewey's chain:", round(score(dewey_train, passage), 3))
print("Montessori's chain:", round(score(montessori_train, passage), 3))
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. For each pair of words in the passage, find the probability each
   chain gives it, as `score()` does.
2. Print the pairs where Montessori's probability is much bigger than
   Dewey's, say by more than 0.3.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
for word, next_word in zip(passage, passage[1:]):
    d = dewey_train.get(word, {})
    m = montessori_train.get(word, {})
    p_d = d.get(next_word, 0) / sum(d.values()) if d else 0
    p_m = m.get(next_word, 0) / sum(m.values()) if m else 0
    if p_m - p_d > 0.3:
        print(word, next_word, round(p_d, 3), round(p_m, 3))
```

Three pairs tip it:

- Montessori uses `"dwelt"` once, followed by `"in"`. So her chain gives
  `"dwelt in"` a probability of 1. Dewey's chain has never seen that
  pair, and gives it 0.
- In Montessori, `"activity"` is followed by `"of"` 8 times in 19, as in
  "the activity of the child". In Dewey, only 9 times in 150.
- `"gained through"` is another pair Montessori's chain has seen once.

A pair seen once can be worth 1, as much as five `"of the"` pairs in
Dewey's chain, which gives that pair 0.2. That is one weakness of this
score: a chain is most sure of itself about the words it has seen
least.

</details>

**6.** Dewey's first 100 words were part of what built `dewey_train`.
The first 100 words that it did not see scored 0.066.

```python exec
id: whose-passage-is-it-2
print(score(dewey_train, dewey_words[:100]) > 0.066)
```

```predict
type: choice

What will the cell print?

- True
- False
  - A passage from the start of the book might be no more typical of
    Dewey than one from the end.
```

<details class="dl-answer"><summary>why</summary>

It prints `True`: those words score 0.232, more than three times as
much. The chain has seen every pair in them, so none of them scores 0.
A chain always does well on the text it was built from. That is why the
tutorial held back a tenth of each book, and tested only on words the
chains had never seen.

</details>

## Your world

**7.** How many of the pairs in a new passage has a chain ever seen?
Can you write `share_seen(chain, passage)`, which returns the share of
the passage's pairs of words that are in the chain?

<div class="dl-world" data-world="dewey-and-montessori">

```python exec
id: your-world-1--dewey-and-montessori
def share_seen(chain, passage):
    """The share of the passage's pairs of words that the chain has seen."""
    # Your code here.
```

```hint
Loop over `zip(passage, passage[1:])` as `score()` does. A pair has
been seen when `word in chain` and `next_word in chain[word]`. Count
those, and divide by the number of pairs.
```

```inputs
round(share_seen(dewey_train, dewey_held), 3)
round(share_seen(montessori_train, dewey_held), 3)
round(share_seen(montessori_train, montessori_held), 3)
round(share_seen(dewey_train, montessori_held), 3)
```

```solution
def share_seen(chain, passage):
    """The share of the passage's pairs of words that the chain has seen."""
    seen = 0
    pairs = 0
    for word, next_word in zip(passage, passage[1:]):
        pairs += 1
        if word in chain and next_word in chain[word]:
            seen += 1
    return seen / pairs
---
Dewey's own chain has seen 0.556 of the pairs in Dewey's held-back
words. Montessori's chain has seen 0.377 of them. For Montessori's
held-back words, the shares are 0.489 under Montessori's own chain and
0.422 under Dewey's. Each writer's chain knows more of that writer's
pairs. But even a writer's own chain has never seen about half of the
pairs in the next tenth of the book. Every one of those scores 0.
```

</div>

<div class="dl-world" data-world="stoker-and-shelley">

```python exec
id: your-world-1--stoker-and-shelley
def words_of(raw):
    """The words between the START OF and END OF marker lines."""
    start = raw.find("*** START OF")
    end = raw.find("*** END OF")
    return raw[raw.index("\n", start):end].split()


stoker_words = words_of(await load_text("dracula.txt"))
shelley_words = words_of(await load_text("frankenstein.txt"))
stoker_cut = int(len(stoker_words) * 0.9)
shelley_cut = int(len(shelley_words) * 0.9)
stoker_train = build_chain(" ".join(stoker_words[:stoker_cut]))
shelley_train = build_chain(" ".join(shelley_words[:shelley_cut]))
stoker_held = stoker_words[stoker_cut:]
shelley_held = shelley_words[shelley_cut:]


def share_seen(chain, passage):
    """The share of the passage's pairs of words that the chain has seen."""
    # Your code here.
```

```hint
Loop over `zip(passage, passage[1:])` as `score()` does. A pair has
been seen when `word in chain` and `next_word in chain[word]`. Count
those, and divide by the number of pairs.
```

```inputs
round(share_seen(stoker_train, stoker_held), 3)
round(share_seen(shelley_train, stoker_held), 3)
round(share_seen(shelley_train, shelley_held), 3)
round(share_seen(stoker_train, shelley_held), 3)
```

```solution
def share_seen(chain, passage):
    """The share of the passage's pairs of words that the chain has seen."""
    seen = 0
    pairs = 0
    for word, next_word in zip(passage, passage[1:]):
        pairs += 1
        if word in chain and next_word in chain[word]:
            seen += 1
    return seen / pairs
---
Stoker's own chain has seen 0.527 of the pairs in Stoker's held-back
words. Shelley's chain has seen 0.347 of them. For Shelley's held-back
words, the shares are 0.434 under Shelley's own chain and 0.388 under
Stoker's. Each writer's chain knows more of that writer's pairs. But
even a writer's own chain has never seen about half of the pairs in the
next tenth of the book. Every one of those scores 0.
```

</div>

<div class="dl-world" data-world="stevenson-and-doyle">

```python exec
id: your-world-1--stevenson-and-doyle
def words_of(raw):
    """The words between the START OF and END OF marker lines."""
    start = raw.find("*** START OF")
    end = raw.find("*** END OF")
    return raw[raw.index("\n", start):end].split()


stevenson_words = words_of(await load_text("treasure-island.txt"))
doyle_words = words_of(await load_text("the-lost-world.txt"))
stevenson_cut = int(len(stevenson_words) * 0.9)
doyle_cut = int(len(doyle_words) * 0.9)
stevenson_train = build_chain(" ".join(stevenson_words[:stevenson_cut]))
doyle_train = build_chain(" ".join(doyle_words[:doyle_cut]))
stevenson_held = stevenson_words[stevenson_cut:]
doyle_held = doyle_words[doyle_cut:]


def share_seen(chain, passage):
    """The share of the passage's pairs of words that the chain has seen."""
    # Your code here.
```

```hint
Loop over `zip(passage, passage[1:])` as `score()` does. A pair has
been seen when `word in chain` and `next_word in chain[word]`. Count
those, and divide by the number of pairs.
```

```inputs
round(share_seen(stevenson_train, stevenson_held), 3)
round(share_seen(doyle_train, stevenson_held), 3)
round(share_seen(doyle_train, doyle_held), 3)
round(share_seen(stevenson_train, doyle_held), 3)
```

```solution
def share_seen(chain, passage):
    """The share of the passage's pairs of words that the chain has seen."""
    seen = 0
    pairs = 0
    for word, next_word in zip(passage, passage[1:]):
        pairs += 1
        if word in chain and next_word in chain[word]:
            seen += 1
    return seen / pairs
---
Stevenson's own chain has seen 0.422 of the pairs in Stevenson's
held-back words. Doyle's chain has seen 0.344 of them. For Doyle's
held-back words, the shares are 0.424 under Doyle's own chain and 0.323
under Stevenson's. Each writer's chain knows more of that writer's
pairs. But even a writer's own chain has never seen about half of the
pairs in the next tenth of the book. Every one of those scores 0.
```

</div>


## From earlier

**8.** From [Repeating steps with loops](tutorial:repeating-yourself).
The loop in the tutorial ran `range(0, len(held) - 100 + 1, 100)`. Here
is the same loop for a list of 250 words.

```python exec
id: from-earlier-1
print(list(range(0, 250 - 100 + 1, 100)))
```

```predict
type: choice

What will the cell print?

- `[0, 100]`
- `[0, 100, 200]`
  - The list has 250 words, and 200 is less than 250.
```

<details class="dl-answer"><summary>why</summary>

`range` stops *before* its stop value, here 151. So the passages start
at 0 and at 100, and each has a full 100 words. A passage starting at
200 would have only 50, and the tutorial found that a short passage is
harder to name.

</details>
