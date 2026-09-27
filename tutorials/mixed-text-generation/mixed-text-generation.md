---
title: "Mixed problems: text generation"
practice_across:
  - a-chain-reads-a-book
  - how-much-it-remembers
  - whose-voice-is-this
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

# Mixed problems: text generation

These problems move between the pages of the series on purpose, and do
not say which page each one comes from. Choosing the tool is part of
the problem. The first cell loads `chain_from()`, which builds a
dictionary of dictionaries from a list of words.

```python exec
id: mixed-text-generation-tools
import random


def chain_from(words):
    """A dictionary of dictionaries: each word, and the words that followed it."""
    chain = {}
    for word, next_word in zip(words, words[1:]):
        chain.setdefault(word, {})
        chain[word][next_word] = chain[word].get(next_word, 0) + 1
    return chain


tiny = chain_from("the cat sat on the mat and the cat ran on the mat".split())
```

## 1.

A chain is built from "the cat sat on the mat and the cat ran". What
is the chance that "cat" comes after "the"? Which word of the sentence
has no followers at all?

```python exec
id: mixed-text-generation-by-hand
```

<details class="dl-hint"><summary>hint</summary>

Write out each pair of words that sit side by side, and count the ones
that start with "the".

</details>

<details class="dl-answer"><summary>one way through it</summary>

"the" is followed by "cat" twice and by "mat" once, so the chance of
"cat" is 2 in 3. "ran" is the last word, so nothing ever follows it,
and it is not a key in the chain. A chain that reaches "ran" has to
stop. `chain_from("the cat sat on the mat and the cat ran".split())`
checks both.

</details>

## 2.

A classmate wants your chain's sentence, exactly. The cell writes from
the chain `tiny` twice, with the same seed each time.

```python exec
id: mixed-text-generation-same-seed
def generate(chain, start, steps):
    result = [start]
    for _ in range(steps):
        followers = chain[result[-1]]
        result.append(random.choices(list(followers), weights=list(followers.values()))[0])
    return result


random.seed(7)
first = generate(tiny, "the", 8)
random.seed(7)
second = generate(tiny, "the", 8)
print(" ".join(first))
print(" ".join(second))
print(first == second)
```

```predict
type: choice

Will the two sentences be the same? What will the last line print?

- True
- False
  - The words are chosen at random, so it seems they must differ.
```

The seed fixes every random choice that follows it. So a classmate who
builds the chain from the same book, and uses the same seed and the
same start, gets your sentence word for word.

## 3.

This generator is meant to walk through the chain. Instead, every word
it writes is a follower of the first word. What is wrong? Can you write
`generate(chain, start, steps, seed)`, which walks the chain properly?

```python exec
id: mixed-text-generation-never-moves
def generate_broken(chain, start, steps, seed):
    random.seed(seed)
    result = [start]
    current = start
    for _ in range(steps):
        followers = chain[current]
        next_word = random.choices(list(followers), weights=list(followers.values()))[0]
        result.append(next_word)
    return result


print(" ".join(generate_broken(tiny, "the", 6, seed=3)))


def generate(chain, start, steps, seed):
    """`steps` more words after start, each chosen from the last word's followers."""
    # Your code here.
```

```hint
Which word's followers does the loop look up each time? Does that word
ever change?
```

```inputs
generate(tiny, "the", 6, seed=3)
generate(tiny, "cat", 4, seed=1)
```

```solution
def generate(chain, start, steps, seed):
    """`steps` more words after start, each chosen from the last word's followers."""
    random.seed(seed)
    result = [start]
    current = start
    for _ in range(steps):
        followers = chain[current]
        current = random.choices(list(followers), weights=list(followers.values()))[0]
        result.append(current)
    return result
---
The broken version never changes `current`, so it looks up the followers of the first word every time: every word it writes is "cat" or "mat". Giving the chosen word the name `current` moves the chain one step along.
```

## 4.

A chain that keys on two words uses keys such as `("the", "cat")`. Why
a tuple? Try `{["the", "cat"]: 1}` in the cell.

```python exec
id: mixed-text-generation-tuple-keys
```

<details class="dl-answer"><summary>answer</summary>

It gives `TypeError: unhashable type: 'list'`. A dictionary needs keys
that can never change, and a list can change: you can append to it at
any time. A tuple cannot be changed after it is made, so it can be a
key.

</details>

## 5.

The score of a passage under a chain is the average chance the chain
gives each next word. The cell scores "cat sat on the mat" under
`tiny`.

```python exec
id: mixed-text-generation-score
def score(chain, passage):
    chances = []
    for word, next_word in zip(passage, passage[1:]):
        followers = chain.get(word, {})
        chances.append(followers.get(next_word, 0) / sum(followers.values()) if followers else 0)
    return sum(chances) / len(chances)


print(score(tiny, "cat sat on the mat".split()))
```

```predict
type: number

`tiny` was built from "the cat sat on the mat and the cat ran on the
mat". What score will it give "cat sat on the mat"?
```

There are four chances. "sat" after "cat" is 1 in 2, "on" after "sat"
is certain, "the" after "on" is certain, and "mat" after "the" is 2 in
4. The average of 0.5, 1, 1 and 0.5 is 0.75.

## 6.

Can you write `strip_gutenberg(raw)`? It returns the text between the
`*** START OF` line and the `*** END OF` line, without either marker
line, and without blank lines at the ends.

```python exec
id: mixed-text-generation-strip
raw = """The Project Gutenberg eBook of A Test
*** START OF THE PROJECT GUTENBERG EBOOK A TEST ***

Once upon a time.
The end.

*** END OF THE PROJECT GUTENBERG EBOOK A TEST ***
Licence text."""


def strip_gutenberg(raw):
    """The text between the START OF and END OF marker lines."""
    # Your code here.
```

```hint
`raw.find("*** START OF")` finds where the start line begins. The text
begins after the end of that line: look for the next `"\n"` from there.
`.strip()` removes the blank lines.
```

```inputs
strip_gutenberg(raw)
```

```solution
def strip_gutenberg(raw):
    """The text between the START OF and END OF marker lines."""
    start = raw.find("*** START OF")
    end = raw.find("*** END OF")
    return raw[raw.index("\n", start):end].strip()
```

## 7.

A chain keyed on one word writes nonsense that sounds like its book. A
chain keyed on three words writes whole sentences from its book. You
want to tell whether a passage was written by Stoker or by Shelley.
Which chain would you build from each book to score the passage with?
Why?

<details class="dl-answer"><summary>answer</summary>

A one-word or two-word chain. A three-word chain has seen so few
three-word runs that almost every run in a new passage is missing from
both chains, and both give it a score near 0. A shorter key has been
seen often enough to give a useful chance for most pairs in a new
passage. The chain that writes the best sentences is not the one that
scores new text best.

</details>

## In your world

Which word most often starts a sentence in your book? Can you write
`most_common_start(words)`? It counts each word that follows a word
ending in a full stop, but only if it starts with a capital letter, and
returns the word with the highest count.

<div class="dl-world" data-world="the-time-machine">

```python exec
id: in-your-world-1--the-time-machine
raw = await load_text("the-time-machine.txt")
start = raw.find("*** START OF")
end = raw.find("*** END OF")
words = raw[raw.index("\n", start):end].split()


def most_common_start(words):
    """The capitalised word that most often follows a word ending in a full stop."""
    # Your code here.
```

```hint
Loop over `zip(words, words[1:])`. When the first word ends with `"."`
and the second starts with a capital (`next_word[:1].isupper()`), add
1 to the second word's count. Then find the word with the largest
count.
```

```inputs
most_common_start(words)
```

```solution
title: with what you've met so far
def most_common_start(words):
    """The capitalised word that most often follows a word ending in a full stop."""
    counts = {}
    for word, next_word in zip(words, words[1:]):
        if word.endswith(".") and next_word[:1].isupper():
            counts[next_word] = counts.get(next_word, 0) + 1
    best = None
    for word in counts:
        if best is None or counts[word] > counts[best]:
            best = word
    return best
---
"I", 305 times: the Time Traveller tells most of the book himself. "The" is next, with 167.
```

```solution
title: a shorter way you'll meet later
def most_common_start(words):
    """The capitalised word that most often follows a word ending in a full stop."""
    counts = {}
    for word, next_word in zip(words, words[1:]):
        if word.endswith(".") and next_word[:1].isupper():
            counts[next_word] = counts.get(next_word, 0) + 1
    return max(counts, key=counts.get)
```

</div>

<div class="dl-world" data-world="dracula">

```python exec
id: in-your-world-1--dracula
raw = await load_text("dracula.txt")
start = raw.find("*** START OF")
end = raw.find("*** END OF")
words = raw[raw.index("\n", start):end].split()


def most_common_start(words):
    """The capitalised word that most often follows a word ending in a full stop."""
    # Your code here.
```

```hint
Loop over `zip(words, words[1:])`. When the first word ends with `"."`
and the second starts with a capital (`next_word[:1].isupper()`), add
1 to the second word's count. Then find the word with the largest
count.
```

```inputs
most_common_start(words)
```

```solution
title: with what you've met so far
def most_common_start(words):
    """The capitalised word that most often follows a word ending in a full stop."""
    counts = {}
    for word, next_word in zip(words, words[1:]):
        if word.endswith(".") and next_word[:1].isupper():
            counts[next_word] = counts.get(next_word, 0) + 1
    best = None
    for word in counts:
        if best is None or counts[word] > counts[best]:
            best = word
    return best
---
"I", 1,049 times, more than twice as often as "The". The book is told in letters and diaries, each written by an "I".
```

```solution
title: a shorter way you'll meet later
def most_common_start(words):
    """The capitalised word that most often follows a word ending in a full stop."""
    counts = {}
    for word, next_word in zip(words, words[1:]):
        if word.endswith(".") and next_word[:1].isupper():
            counts[next_word] = counts.get(next_word, 0) + 1
    return max(counts, key=counts.get)
```

</div>

<div class="dl-world" data-world="dubliners">

```python exec
id: in-your-world-1--dubliners
raw = await load_text("dubliners.txt")
start = raw.find("*** START OF")
end = raw.find("*** END OF")
words = raw[raw.index("\n", start):end].split()


def most_common_start(words):
    """The capitalised word that most often follows a word ending in a full stop."""
    # Your code here.
```

```hint
Loop over `zip(words, words[1:])`. When the first word ends with `"."`
and the second starts with a capital (`next_word[:1].isupper()`), add
1 to the second word's count. Then find the word with the largest
count.
```

```inputs
most_common_start(words)
```

```solution
title: with what you've met so far
def most_common_start(words):
    """The capitalised word that most often follows a word ending in a full stop."""
    counts = {}
    for word, next_word in zip(words, words[1:]):
        if word.endswith(".") and next_word[:1].isupper():
            counts[next_word] = counts.get(next_word, 0) + 1
    best = None
    for word in counts:
        if best is None or counts[word] > counts[best]:
            best = word
    return best
---
"He", 487 times, with "The" at 333 and "She" at 170. Most of the stories are told from outside, about "he" or "she", not by an "I".
```

```solution
title: a shorter way you'll meet later
def most_common_start(words):
    """The capitalised word that most often follows a word ending in a full stop."""
    counts = {}
    for word, next_word in zip(words, words[1:]):
        if word.endswith(".") and next_word[:1].isupper():
            counts[next_word] = counts.get(next_word, 0) + 1
    return max(counts, key=counts.get)
```

</div>

<div class="dl-world" data-world="irish-fairy-tales">

```python exec
id: in-your-world-1--irish-fairy-tales
raw = await load_text("irish-fairy-tales.txt")
start = raw.find("*** START OF")
end = raw.find("*** END OF")
words = raw[raw.index("\n", start):end].split()


def most_common_start(words):
    """The capitalised word that most often follows a word ending in a full stop."""
    # Your code here.
```

```hint
Loop over `zip(words, words[1:])`. When the first word ends with `"."`
and the second starts with a capital (`next_word[:1].isupper()`), add
1 to the second word's count. Then find the word with the largest
count.
```

```inputs
most_common_start(words)
```

```solution
title: with what you've met so far
def most_common_start(words):
    """The capitalised word that most often follows a word ending in a full stop."""
    counts = {}
    for word, next_word in zip(words, words[1:]):
        if word.endswith(".") and next_word[:1].isupper():
            counts[next_word] = counts.get(next_word, 0) + 1
    best = None
    for word in counts:
        if best is None or counts[word] > counts[best]:
            best = word
    return best
---
"He", 209 times. "“I" would come second, but it starts with a quotation mark, not a capital, so the test leaves it out. Should it? What would you change to count it?
```

```solution
title: a shorter way you'll meet later
def most_common_start(words):
    """The capitalised word that most often follows a word ending in a full stop."""
    counts = {}
    for word, next_word in zip(words, words[1:]):
        if word.endswith(".") and next_word[:1].isupper():
            counts[next_word] = counts.get(next_word, 0) + 1
    return max(counts, key=counts.get)
```

</div>

<div class="dl-world" data-world="treasure-island">

```python exec
id: in-your-world-1--treasure-island
raw = await load_text("treasure-island.txt")
start = raw.find("*** START OF")
end = raw.find("*** END OF")
words = raw[raw.index("\n", start):end].split()


def most_common_start(words):
    """The capitalised word that most often follows a word ending in a full stop."""
    # Your code here.
```

```hint
Loop over `zip(words, words[1:])`. When the first word ends with `"."`
and the second starts with a capital (`next_word[:1].isupper()`), add
1 to the second word's count. Then find the word with the largest
count.
```

```inputs
most_common_start(words)
```

```solution
title: with what you've met so far
def most_common_start(words):
    """The capitalised word that most often follows a word ending in a full stop."""
    counts = {}
    for word, next_word in zip(words, words[1:]):
        if word.endswith(".") and next_word[:1].isupper():
            counts[next_word] = counts.get(next_word, 0) + 1
    best = None
    for word in counts:
        if best is None or counts[word] > counts[best]:
            best = word
    return best
---
"I", 233 times: Jim Hawkins tells the story. Without the capital-letter test, the top answer would be a lone full stop, 333 times. The book's table of contents joins each chapter title to its page number with a row of dots, ". . . .".
```

```solution
title: a shorter way you'll meet later
def most_common_start(words):
    """The capitalised word that most often follows a word ending in a full stop."""
    counts = {}
    for word, next_word in zip(words, words[1:]):
        if word.endswith(".") and next_word[:1].isupper():
            counts[next_word] = counts.get(next_word, 0) + 1
    return max(counts, key=counts.get)
```

</div>
