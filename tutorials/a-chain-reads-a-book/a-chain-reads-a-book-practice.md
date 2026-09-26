---
title: "A Markov chain from a whole book: a dictionary of dictionaries — Practice"
practice_for: a-chain-reads-a-book
year: "2026-2027"
version: 2026.09.26.1
datasets: [the-time-machine, dracula, dubliners, irish-fairy-tales, treasure-island, the-war-of-the-worlds, frankenstein, a-princess-of-mars, the-lost-world, pride-and-prejudice]
worlds:
  the-time-machine: The Time Machine, by H. G. Wells (1895), a journey to the far future.
  dracula: Dracula, by the Dublin-born writer Bram Stoker (1897), told in letters and diaries.
  dubliners: Dubliners, by James Joyce (1914), fifteen stories set in Dublin.
  irish-fairy-tales: Irish Fairy Tales, by James Stephens (1920), the old stories of Fionn and the Fianna.
  treasure-island: Treasure Island, by Robert Louis Stevenson (1883), pirates and a voyage by sea.
---

# A Markov chain from a whole book: a dictionary of dictionaries — Practice

Each answer is hidden until you open it. Write something down first,
even a guess, and then open the answer to compare.

## Tools

Run this cell first. It loads *The Time Machine*, cleans it, and builds
its chain, with the two functions from the end of the tutorial.

```python exec
id: tools-1
import random

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


book = strip_gutenberg(raw)
words = book.split()
next_words = chain_from(words)
print(len(words), "words,", len(next_words), "different")
```

## Cleaning the text

**1.** How many characters shorter is `book` than `raw`? What are those
missing characters?

<details class="dl-answer"><summary>answer</summary>

```python
print(len(raw) - len(book))
```

19,377. That is Project Gutenberg's own header and licence, at both ends
of the file, plus the marker lines and the empty lines that `.strip()`
removed. None of it is H. G. Wells's writing.

Try the same on `dracula.txt`: it loses 19,318 characters. Every file in
this series carries the same licence, so each one loses almost the same
amount.

</details>

**2.** *The Time Machine* has sixteen numbered chapters. Each chapter
heading is a line with nothing on it but a Roman numeral, like `XII`. The
table of contents near the top is different: there, each numeral shares
a line with the chapter's title. Can you write `count_chapters(text)`,
which counts the lines that hold nothing but a Roman numeral?

```python exec
id: cleaning-the-text-1
def count_chapters(text):
    """How many lines hold nothing but a Roman numeral."""
    # Your code here.
```

```hint
`text.split("\n")` gives every line. A heading, once `.strip()` has
removed its spaces, uses only the letters in `"IVXLC"`. The test
`set(line.strip()) <= set("IVXLC")` is `True` when every letter in the
line is one of those. An empty line passes that test too, so check that
the line is not empty first.
```

```inputs
count_chapters(book)
count_chapters("I\nThe start\n\nII\nThe end")
```

```solution
def count_chapters(text):
    """How many lines hold nothing but a Roman numeral."""
    roman = set("IVXLC")
    count = 0
    for line in text.split("\n"):
        if line.strip() and set(line.strip()) <= roman:
            count += 1
    return count
---
16, the number of chapters in the novel. The lines of the table of
contents never pass the test: each one also has the chapter's title on
it, and a title has other letters. The short text has two headings. Its
empty line is not counted, because `line.strip()` is empty.
```

## How many words does the chain know?

**3.** Which word in the book is followed by the largest number of
*different* words? Can you write `busiest(chain)`, which returns that
word for any chain?

```python exec
id: how-many-words-1
def busiest(chain):
    """The word with the most different words after it."""
    # Your code here.
```

```hint
`len(chain[word])` counts how many different words have followed
`word`. You could loop over the chain and keep the word with the biggest
count so far. Or `max()` can do the loop: `key=` tells it what to
compare.
```

```inputs
busiest(next_words)
len(next_words[busiest(next_words)])
busiest({"a": {"b": 1}, "b": {"a": 1, "c": 2}})
```

```solution
def busiest(chain):
    """The word with the most different words after it."""
    return max(chain, key=lambda word: len(chain[word]))
---
It is `"the"`, with 1,162 different words after it. `"the"` can go in
front of almost any noun, so it has had the chance to be followed by
almost every noun the book uses. `lambda word: len(chain[word])` is a
small function written in one line: it takes a word and returns its
number of followers.
```

**4.** Some words in the book are followed by the same word every time,
and never by anything else. Can you write `fixed_pairs(chain,
at_least)`, which returns every such pair that appears at least
`at_least` times, as `(word, follower, count)`?

```python exec
id: how-many-words-2
def fixed_pairs(chain, at_least):
    """Words with only one follower, seen at least at_least times."""
    # Your code here.
```

```hint
A word with exactly one follower has `len(chain[word]) == 1`. Its inner
dictionary then has one key and one value, and the value is how many
times that follower appeared.
```

```inputs
len(fixed_pairs(next_words, 5))
fixed_pairs(next_words, 9)
```

```solution
def fixed_pairs(chain, at_least):
    """Words with only one follower, seen at least at_least times."""
    found = []
    for word, followers in chain.items():
        if len(followers) == 1:
            for follower, count in followers.items():
                if count >= at_least:
                    found.append((word, follower, count))
    return found
---
There are ten pairs seen at least five times, and two seen at least
nine. `"sense"` is followed only by `"of"`, 11 times: every time it
appears in the book. `"determined"` is followed only by `"to"`, 9 times.
Both are the first half of a fixed phrase. English almost never puts a
different word in second place, so the chain never sees one either.
```

**5.** `generate()` stops its loop early if `current not in
next_words`. Does that ever happen with this book? Is there a word in
the book with no recorded follower at all?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. `set(words)` is every distinct word in the book.
2. `set(next_words.keys())` is every word that has at least one recorded
   follower.
3. If you take one set away from the other,
   `set(words) - set(next_words.keys())`, only the words that are in the
   first set and not in the second are left.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
missing = set(words) - set(next_words.keys())
print(missing)
```

It prints `set()`, an empty set. Every one of the 6,991 different words
in the book has at least one recorded follower. So `generate()`'s
early-stop line never runs on this book.

The line is still worth having. A shorter text, or one cleaned in a
different way, could end on a word that appears nowhere else in it.
Without the check, `generate()` would crash on that word. With it,
`generate()` stops.

Look at `words[-1]`, the very last word. It is `"Wells"`, from the
closing line that the tutorial found. `"Wells"` also appears on the
title page, so it still has a recorded follower.

</details>

## Seeds and runs

**6.** Pick any word that appears often in the book.

1. Generate 25 words starting from it.
2. Run the cell three times.
3. How different are the three results from each other?

```python exec
id: seeds-and-runs-1
```

**7.** In the tutorial, seed 1 and 20 steps from `"Weena"` wrote "Weena
was Weena would still remained one by their features, I left her to
speak of putrefaction and grew visible. “I". This cell asks for only 5
steps.

```python exec
id: seeds-and-runs-2
random.seed(1)
print(generate("Weena", 5))
```

```predict
type: choice

What will the cell print?

- Weena was Weena would still remained
- Six different words from the book, starting with Weena
  - A shorter run makes fewer choices, and the choices might change.
```

<details class="dl-answer"><summary>why</summary>

It prints the first six words of the long sentence. Each step makes one
random choice, and the seed fixes the whole list of choices in order.
`steps` only says how far along that list to go. So with the same seed,
a short run is always the start of a long one.

Now call `generate("Weena", 5)` twice after one `random.seed(1)`. The
second sentence is different, because it carries on down the list from
where the first one stopped.

</details>

## Your world

**8.** When the chain reaches a word with only one follower, it has no
choice to make. How common is that in your book? Can you write
`share_with_one_follower(chain)`, which
returns the share of the chain's words that have exactly one follower,
as a number between 0 and 1?

<div class="dl-world" data-world="the-time-machine">

```python exec
id: your-world-1--the-time-machine
mine = await load_text("the-time-machine.txt")
my_chain = chain_from(strip_gutenberg(mine).split())


def share_with_one_follower(chain):
    """The share of words in the chain with exactly one follower."""
    # Your code here.
```

```hint
Count the words where `len(chain[word]) == 1`, then divide by
`len(chain)`.
```

```inputs
round(share_with_one_follower(my_chain), 3)
share_with_one_follower({"a": {"b": 1}, "b": {"a": 2, "c": 1}})
```

```solution
def share_with_one_follower(chain):
    """The share of words in the chain with exactly one follower."""
    one = [word for word in chain if len(chain[word]) == 1]
    return len(one) / len(chain)
---
0.665: 4,652 of the 6,991 words have only one follower. For two words
in every three, the chain is not choosing at all. It copies the book.
```

</div>

<div class="dl-world" data-world="dracula">

```python exec
id: your-world-1--dracula
mine = await load_text("dracula.txt")
my_chain = chain_from(strip_gutenberg(mine).split())


def share_with_one_follower(chain):
    """The share of words in the chain with exactly one follower."""
    # Your code here.
```

```hint
Count the words where `len(chain[word]) == 1`, then divide by
`len(chain)`.
```

```inputs
round(share_with_one_follower(my_chain), 3)
share_with_one_follower({"a": {"b": 1}, "b": {"a": 2, "c": 1}})
```

```solution
def share_with_one_follower(chain):
    """The share of words in the chain with exactly one follower."""
    one = [word for word in chain if len(chain[word]) == 1]
    return len(one) / len(chain)
---
0.615: 11,353 of the 18,462 words have only one follower. *Dracula* is
the longest book here, so its words have had the most chances to meet a
second follower, and still more than half of them never did. For those
words, the chain copies the book.
```

</div>

<div class="dl-world" data-world="dubliners">

```python exec
id: your-world-1--dubliners
mine = await load_text("dubliners.txt")
my_chain = chain_from(strip_gutenberg(mine).split())


def share_with_one_follower(chain):
    """The share of words in the chain with exactly one follower."""
    # Your code here.
```

```hint
Count the words where `len(chain[word]) == 1`, then divide by
`len(chain)`.
```

```inputs
round(share_with_one_follower(my_chain), 3)
share_with_one_follower({"a": {"b": 1}, "b": {"a": 2, "c": 1}})
```

```solution
def share_with_one_follower(chain):
    """The share of words in the chain with exactly one follower."""
    one = [word for word in chain if len(chain[word]) == 1]
    return len(one) / len(chain)
---
0.651: 7,775 of the 11,949 words have only one follower. For nearly two
words in every three, the chain is not choosing at all. It copies Joyce.
```

</div>

<div class="dl-world" data-world="irish-fairy-tales">

```python exec
id: your-world-1--irish-fairy-tales
mine = await load_text("irish-fairy-tales.txt")
my_chain = chain_from(strip_gutenberg(mine).split())


def share_with_one_follower(chain):
    """The share of words in the chain with exactly one follower."""
    # Your code here.
```

```hint
Count the words where `len(chain[word]) == 1`, then divide by
`len(chain)`.
```

```inputs
round(share_with_one_follower(my_chain), 3)
share_with_one_follower({"a": {"b": 1}, "b": {"a": 2, "c": 1}})
```

```solution
def share_with_one_follower(chain):
    """The share of words in the chain with exactly one follower."""
    one = [word for word in chain if len(chain[word]) == 1]
    return len(one) / len(chain)
---
0.624: 6,499 of the 10,417 words have only one follower. For those
words, the chain is not choosing at all. It copies Stephens.
```

</div>

<div class="dl-world" data-world="treasure-island">

```python exec
id: your-world-1--treasure-island
mine = await load_text("treasure-island.txt")
my_chain = chain_from(strip_gutenberg(mine).split())


def share_with_one_follower(chain):
    """The share of words in the chain with exactly one follower."""
    # Your code here.
```

```hint
Count the words where `len(chain[word]) == 1`, then divide by
`len(chain)`.
```

```inputs
round(share_with_one_follower(my_chain), 3)
share_with_one_follower({"a": {"b": 1}, "b": {"a": 2, "c": 1}})
```

```solution
def share_with_one_follower(chain):
    """The share of words in the chain with exactly one follower."""
    one = [word for word in chain if len(chain[word]) == 1]
    return len(one) / len(chain)
---
0.641: 7,250 of the 11,318 words have only one follower. For those
words, the chain is not choosing at all. It copies Stevenson.
```

</div>

**9.** Try one more book. The series has ten:

- *The Time Machine*, `the-time-machine.txt`
- *Dracula*, `dracula.txt`
- *Dubliners*, `dubliners.txt`
- *Irish Fairy Tales*, `irish-fairy-tales.txt`
- *Treasure Island*, `treasure-island.txt`
- *The War of the Worlds*, `the-war-of-the-worlds.txt`
- *Frankenstein*, `frankenstein.txt`
- *A Princess of Mars*, `a-princess-of-mars.txt`
- *The Lost World*, `the-lost-world.txt`
- *Pride and Prejudice*, `pride-and-prejudice.txt`

Load one, clean it with `strip_gutenberg`, build its chain with
`chain_from`, and find its share of words with one follower. Is it
closer to a half, or to two-thirds?

```python exec
id: your-world-2
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. `raw2 = await load_text("frankenstein.txt")`, or whichever file you
   picked.
2. `chain2 = chain_from(strip_gutenberg(raw2).split())`.
3. Count the words in `chain2` with one follower, and divide by
   `len(chain2)`.

**Think about:** how many cells would a dense grid need for this book?
That is the number of different words, squared.

</details>

## From earlier

**10.** From [Markov chains: where repeated steps
settle](tutorial:where-chains-lead#words-that-follow-words). That page
divided each row of counts by its total, to turn counts into
probabilities. Can you do the same for one inner dictionary? Write
`as_probabilities(followers)`, which returns a new dictionary with each
count divided by the total.

```python exec
id: from-earlier-1
def as_probabilities(followers):
    """Each follower's count, divided by the total of all the counts."""
    # Your code here.
```

```hint
`sum(followers.values())` is the total. Then make a new dictionary with
the same keys, and each count divided by that total.
```

```inputs
as_probabilities({"cat": 1, "mat": 3})
round(as_probabilities(next_words["Weena"])["was"], 3)
round(sum(as_probabilities(next_words["the"]).values()), 6)
```

```solution
def as_probabilities(followers):
    """Each follower's count, divided by the total of all the counts."""
    total = sum(followers.values())
    return {word: count / total for word, count in followers.items()}
---
`"Weena"` appears 24 times with a follower, and 4 of those are `"was"`,
so its probability is 4/24, about 0.167. The probabilities after
`"the"` add up to 1, as every row of a transition matrix does.
`random.choices()` gives the same results with the counts or with these
probabilities, which is why the tutorial could skip this step.
```

**11.** From [Dictionaries: looking things up by
name](tutorial:looking-things-up-by-name). The chain's loop adds 1 with
`chain[word].get(next_word, 0) + 1`. What goes wrong if it uses
`chain[word][next_word] + 1` instead? Run the cell.

```python exec
id: from-earlier-2
chain = {}
for word, next_word in zip(["the", "cat", "sat"], ["cat", "sat", "on"]):
    chain.setdefault(word, {})
    chain[word][next_word] = chain[word][next_word] + 1
print(chain)
```

<details class="dl-answer"><summary>answer</summary>

It stops with `KeyError: 'cat'`. The first time a pair is seen, its
follower is not yet a key in the inner dictionary, so there is nothing
to add 1 to. `.get(next_word, 0)` says what to use when the key is
missing: 0, a count that has not started yet.

</details>
