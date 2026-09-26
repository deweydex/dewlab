---
title: "Writing style: comparing two writers with Markov chains"
year: "2026-2027"
version: 2026.09.26.1
datasets: [democracy-and-education, the-montessori-method, dracula, frankenstein, treasure-island, the-lost-world]
covers:
  cleaning-two-different-books:
    touches: [CMPS-LO1]
  two-writers-two-chains:
    covers: [CMPS-LO4]
  investigating-the-difference:
    touches: [CMPS-LO2]
  whose-passage-is-it:
    covers: [CMPS-LO6]
worlds:
  dewey-and-montessori: John Dewey and Maria Montessori, two writers on education, from the same few years.
  stoker-and-shelley: Bram Stoker's Dracula (1897) and Mary Shelley's Frankenstein (first published 1818), two tales of horror.
  stevenson-and-doyle: Robert Louis Stevenson's Treasure Island (1883) and Arthur Conan Doyle's The Lost World (1912), two adventures.
---

# Writing style: comparing two writers with Markov chains

Two writers on education published books at almost the same time. John
Dewey wrote *Democracy and Education* (1916). Maria Montessori wrote *The
Montessori Method*, which came out in Italian in 1909. Our copy is the
English translation by Anne E. George, from 1912.

On this page we build a chain from each writer's book, separately. Does
a chain trained on one writer's words sound different from a chain
trained on the other's? Then we try the real test. Given a passage with
no name on it, can the chains tell us who wrote it?

## Cleaning two different books

These two files are less tidy than the Project Gutenberg novels that
came with [A Markov chain from a whole book: a dictionary of
dictionaries](tutorial:a-chain-reads-a-book). Neither file has a
`*** START OF` line to show where the book begins. Dewey's file is a raw
scan of the printed book, with all the marks of a scan. Each one needs
its own way of cleaning. That is normal. Real data rarely arrives in
exactly one shape.

```python exec
id: cleaning-two-different-books-1
dewey_raw = await load_text("democracy-and-education.txt")
print(dewey_raw[:400])
```

The first several thousand characters are not Dewey's writing. First
comes a publisher's list of other books in the same series. Then come
the title page and the table of contents of *Democracy and Education*.

How do we find where Chapter I begins? The chapter's title,
`"EDUCATION AS A NECESSITY OF LIFE"`, appears twice in the file. The
first time is in the table of contents. The second time is the real
start of Chapter I.

```python exec
id: cleaning-two-different-books-2
marker = "EDUCATION AS A NECESSITY OF LIFE"
first = dewey_raw.find(marker)
second = dewey_raw.find(marker, first + 1)
dewey_end = dewey_raw.find("INDEX")
dewey_book = dewey_raw[second:dewey_end].strip()
print(len(dewey_book.split()), "words of real Dewey")
```

Can you add a line that prints the first 200 characters of
`dewey_book`, to see where it starts? And the last 200, to see where it
stops?

<details class="dl-answer"><summary>What each line does</summary>

1. `dewey_raw.find(marker)` finds the first copy of the title, in the
   table of contents.
2. `dewey_raw.find(marker, first + 1)` searches again, starting just
   after the first copy. So it finds the *second* copy, where Chapter I
   begins.
3. This book also has an index at the end. *The Time Machine* did not
   have one. `.find("INDEX")` gives the position where the index starts,
   and so where Dewey's writing stops.
4. The slice from `second` to `dewey_end` is the book itself.

</details>

There is more to clean. The scan kept everything on the printed page,
including things a reader's eye skips over. Here is one short stretch:

```python exec
id: cleaning-two-different-books-scan-1
where = dewey_book.find("assimilate, imaginatively")
print(dewey_book[where:where + 160])
```

Two extra things are inside Dewey's sentence. The word "something" did not
fit at the end of a printed line, so it was split with a hyphen:
`some-` on one line, `thing` on the next. And in between sits the top of
the next page, a *running header*: a title and a page number, printed on
every page. How many words end in a hyphen?

```python exec
id: cleaning-two-different-books-scan-2
split_words = [word for word in dewey_book.split() if word.endswith("-")]
print(len(split_words), "words end in a hyphen")
print(split_words[:10])
```

There are more than two thousand half-words, and each would become a
key in the chain. And about four hundred headers would put words like
"18 Philosophy of Education" into the middle of Dewey's sentences. The
next cell deals with both.

```python exec
id: cleaning-two-different-books-scan-3
def clean_scan(text):
    """Remove blank lines and page headers, then join words split at a line end."""
    kept = []
    for line in text.split("\n"):
        words = line.split()
        if not words:
            continue    # a blank line
        if len(words) <= 8 and (words[0].isdigit() or words[-1].isdigit()):
            continue    # a header: a short line that starts or ends with a page number
        kept.append(line.strip())
    return "\n".join(kept).replace("-\n", "")


dewey_book = clean_scan(dewey_book)
print(len(dewey_book.split()), "words of real Dewey")
print(len([word for word in dewey_book.split() if word.endswith("-")]), "words still end in a hyphen")
```

Some problems remain. A handful of broken words are left, where something
else sat between the two halves. And a word that really had a hyphen,
such as "self-control", becomes "selfcontrol" if the line happened
to break at its hyphen. Both are far fewer than the two thousand broken
words it fixed. Real data cleaning usually works like this. Each
rule fixes a lot, and makes a few new mistakes.

### Your turn

The Montessori text needs the same find-it-twice method, with a different
marker: `"A CRITICAL CONSIDERATION OF THE NEW PEDAGOGY IN ITS RELATION TO"`.
These are the first words of Chapter I, and they also appear once in the
book's table of contents. This file ends with the words `"THE END"`, so
there is no index to cut from the end. Can you keep everything from the
second copy of the marker to the end of the file, as `montessori_book`?

```python exec
id: cleaning-two-different-books-3
montessori_raw = await load_text("the-montessori-method.txt")
marker2 = "A CRITICAL CONSIDERATION OF THE NEW PEDAGOGY IN ITS RELATION TO"
# Your code here.
```

```hint
It is the find-it-twice pattern used above for Dewey, with no second
`.find()` for an ending: `montessori_raw[second2:].strip()`.
```

```inputs
montessori_book[:40]
len(montessori_book.split())
```

```solution
montessori_raw = await load_text("the-montessori-method.txt")
marker2 = "A CRITICAL CONSIDERATION OF THE NEW PEDAGOGY IN ITS RELATION TO"
first2 = montessori_raw.find(marker2)
second2 = montessori_raw.find(marker2, first2 + 1)
montessori_book = montessori_raw[second2:].strip()
---
The book starts with the first words of Chapter I, and has 108,800
words.
```

## Two writers, two chains

The next cell cleans the Montessori book, in case you want to compare
your answer. Then it builds a chain from each book. `build_chain()` is
the loop from the earlier tutorials, put inside a function so that we can
use it twice.

```python exec
id: two-writers-two-chains-1
montessori_raw = await load_text("the-montessori-method.txt")
marker2 = "A CRITICAL CONSIDERATION OF THE NEW PEDAGOGY IN ITS RELATION TO"
first2 = montessori_raw.find(marker2)
second2 = montessori_raw.find(marker2, first2 + 1)
montessori_book = montessori_raw[second2:].strip()

def build_chain(book_text):
    words = book_text.split()
    chain = {}
    for word, next_word in zip(words, words[1:]):
        chain.setdefault(word, {})
        chain[word][next_word] = chain[word].get(next_word, 0) + 1
    return chain

dewey_chain = build_chain(dewey_book)
montessori_chain = build_chain(montessori_book)

print(len(dewey_chain), "distinct words in Dewey's chain")
print(len(montessori_chain), "distinct words in Montessori's chain")
```

`generate()` changes in the same way. It now takes the chain as its first
argument, so the one function works for both writers.

```python exec
id: two-writers-two-chains-2
import random

random.seed(1)    # change the 1 to any other number for a different run

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

print("Dewey:", generate(dewey_chain, "education", 20))
print("Montessori:", generate(montessori_chain, "education", 20))
```

Run the cell, then change the seed and run it a few more times. Both
chains start from the same word. Do they go to the same kind of
sentence, or does each one go its own way?

### Your turn

1. Pick a word that appears in both books, `"child"` or `"life"`, for
   example.
2. Generate 20 words from each writer's chain, starting from that word.
3. What differences do you notice?

```python exec
id: two-writers-two-chains-3
hint: "child" in dewey_chain and "child" in montessori_chain are both True — check before you pick a word, since not every word appears in both books.
```

## Investigating the difference

Both books are about the same word: `"education"`. Do the two writers
follow it with the same words?

```python exec
id: investigating-the-difference-1
dewey_after = sorted(dewey_chain["education"].items(), key=lambda kv: -kv[1])[:5]
montessori_after = sorted(montessori_chain["education"].items(), key=lambda kv: -kv[1])[:5]
print("Dewey, most common words after 'education':", dewey_after)
print("Montessori, most common words after 'education':", montessori_after)
```

Can you change the cell to show ten words for each writer, and not five?

<details class="dl-answer"><summary>How the cell finds the most common words</summary>

- `.items()` gives each follower with its count, as a pair such as
  `("is", 58)`.
- `sorted(..., key=...)` puts the pairs in order. `key=` says what to
  sort them by.
- `lambda kv: -kv[1]` is a small function written in one line. It takes
  a pair `kv` and returns its count, `kv[1]`, with a minus sign. The
  minus sign puts the biggest count first.
- `[:5]` keeps the first five. `[:10]` keeps ten.

</details>

What do the two lines show? Dewey's most common word after `"education"`
is `"is"`, 58 times. Montessori's is `"of"`, 68 times. These counts come
from the whole of each book. They are not a random sample, so the numbers
are the same every time you run the cell.

Here is one way to read the difference. Dewey often returns to what
education *is*, which is a philosopher's habit. Montessori often returns
to the education *of* someone or something, which is a practical habit.

Dewey's book has 97 different words after `"education"`. Montessori's
has 36. So Dewey's use of the word ranges more widely. Part of the
reason is that he also uses the word more than twice as often, 301 times
against 133, which gives it more chances to meet new neighbours.

Those counts are for `"education"` exactly, with a small e and nothing
attached to it. The chain treats `"Education"` at the start of a
sentence, and `"education,"` with a comma, as different words. So does
`"_education_"`: the Montessori file marks words in italics with
underscores. Counted in every form, Dewey writes the word 464 times and
Montessori 227, so he still uses it about twice as often.

### Your turn

None of this shows that a chain can tell who wrote a sentence with no
name on it. It only shows that two real writers used one shared word in
different ways.

1. Pick your own word that both books use.
2. How many different words follow it in each chain?
3. What is the single most common one in each?
4. Does the difference say anything believable about how these two
   writers wrote?

```python exec
id: investigating-the-difference-2
```

## Whose passage is it?

Now for the real test. Suppose we find a passage with no name on it. Can
the chains tell us who wrote it?

To test that fairly, the chains must not have seen the passages we try
them on. A chain that has read a passage will recognise it, just as the
`order2` chain recited *The Time Machine*. So we hold back the last tenth
of each book, as *held-back text*. The chains are built from the first
nine-tenths only, and the held-back text gives us our test passages.

```python exec
id: whose-passage-is-it-1
dewey_words = dewey_book.split()
montessori_words = montessori_book.split()
dewey_cut = int(len(dewey_words) * 0.9)
montessori_cut = int(len(montessori_words) * 0.9)

dewey_train = build_chain(" ".join(dewey_words[:dewey_cut]))
montessori_train = build_chain(" ".join(montessori_words[:montessori_cut]))
dewey_held = dewey_words[dewey_cut:]
montessori_held = montessori_words[montessori_cut:]

print(len(dewey_held), "words of Dewey held back")
print(len(montessori_held), "words of Montessori held back")
```

`build_chain()` takes text, not a list of words, so `" ".join()` puts
the words back together first.

How well does a chain fit a passage? Take the passage one pair of words
at a time. For each pair, ask the chain: after the first word, how often
did the second one come next? That is a probability, between 0 and 1.
If the chain never saw the pair, the probability is 0. The average of
these probabilities is the passage's *score* under that chain. A higher
score means the passage looks more like the book the chain was built
from.

```python exec
id: whose-passage-is-it-2
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


passage = dewey_held[:100]
print(" ".join(passage[:30]), "...")
print("Dewey's chain:", round(score(dewey_train, passage), 3))
print("Montessori's chain:", round(score(montessori_train, passage), 3))
```

These are the first 100 of Dewey's words that neither chain has seen.
Dewey's chain gives them the higher score. Change `dewey_held` to
`montessori_held` and run it again. Which chain gives the higher score
now?

<details class="dl-answer"><summary>What each line of score() does</summary>

1. `zip(passage, passage[1:])` pairs each word with the word after it,
   just as the chains do.
2. `chain.get(word, {})` gives the word's followers, or an empty
   dictionary if the chain has never seen the word.
3. If `next_word` is one of those followers, its count divided by the
   total of all the counts is the probability the chain gives it.
4. If not, the chain gives it no chance at all, so the probability is 0.
5. The last line is the average of all the probabilities.

</details>

One passage proves very little. The next cell cuts Dewey's held-back
words into passages of 100 words, and counts how many of them his own
chain scores higher.

```python exec
id: whose-passage-is-it-3
def guess_writer(passage):
    if score(dewey_train, passage) > score(montessori_train, passage):
        return "Dewey"
    return "Montessori"


right = 0
tried = 0
for start in range(0, len(dewey_held) - 100 + 1, 100):
    tried += 1
    if guess_writer(dewey_held[start:start + 100]) == "Dewey":
        right += 1
print(right, "of", tried, "passages")
print(round(right / tried, 2))
```

```predict
type: number
tolerance: 0.1

The last line is the share of Dewey's passages that the chains name
correctly. What will it be? Tossing a coin would give about 0.5.
```

Neither chain knows anything about education, or about Dewey or
Montessori as people. Each knows only which word followed which, in
nine-tenths of one book. Most of the time, that is enough. Can you
change the loop to test Montessori's passages?

The passages it names wrongly are mostly close calls, where the two
scores are nearly the same and both are lower than usual. Two of them
are Dewey writing about the philosophers of ancient Greece. The
practice page looks at one of them.

Language models are tested in a similar way. Their score is called
*perplexity*. It combines the probabilities by multiplying them, not by
averaging them, which punishes one unlikely word much more. It is also
turned round, so that a *lower* perplexity means the model was less
surprised by the text. Multiplying brings a problem our score does not
have. A single pair the model has never seen would have a probability
of 0, and make the whole product 0. So a real language model never
gives any word a chance of exactly 0.

### Your turn

Can you write `share_named(held, own_chain, other_chain, length)`? It
cuts `held` into passages of `length` words, and returns the share of
them that score higher under `own_chain` than under `other_chain`. Try
passages of 100 words, then 20. Does a shorter passage make the task
harder?

<div class="dl-world" data-world="dewey-and-montessori">

Try it on Dewey and Montessori.

```python exec
id: whose-passage-is-it-4--dewey-and-montessori
def share_named(held, own_chain, other_chain, length):
    """The share of passages from held that score higher under own_chain."""
    # Your code here.
```

```hint
The loop in `guess_writer`'s cell does this for one writer and 100
words. Put it inside a function, with `length` in place of 100, and
compare `score(own_chain, passage)` with `score(other_chain, passage)`.
```

```inputs
round(share_named(dewey_held, dewey_train, montessori_train, 100), 3)
round(share_named(montessori_held, montessori_train, dewey_train, 100), 3)
round(share_named(dewey_held, dewey_train, montessori_train, 20), 3)
round(share_named(montessori_held, montessori_train, dewey_train, 20), 3)
```

```solution
def share_named(held, own_chain, other_chain, length):
    """The share of passages from held that score higher under own_chain."""
    right = 0
    tried = 0
    for start in range(0, len(held) - length + 1, length):
        passage = held[start:start + length]
        tried += 1
        if score(own_chain, passage) > score(other_chain, passage):
            right += 1
    return right / tried
---
At 100 words, the chains name 0.905 of Dewey's passages and 0.907 of
Montessori's. At 20 words, that falls to 0.721 and 0.735: still better
than tossing a coin, but wrong about one time in four. A passage of 20
words has only 19 pairs to go on, so a few lucky or unlucky pairs can
swing its score.
```

</div>

<div class="dl-world" data-world="stoker-and-shelley">

Try it on two tales of horror: Bram Stoker's *Dracula* and Mary
Shelley's *Frankenstein*. The cell builds a chain from nine-tenths of
each, and holds back the rest.

```python exec
id: whose-passage-is-it-4--stoker-and-shelley
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


def share_named(held, own_chain, other_chain, length):
    """The share of passages from held that score higher under own_chain."""
    # Your code here.
```

```hint
The loop in `guess_writer`'s cell does this for one writer and 100
words. Put it inside a function, with `length` in place of 100, and
compare `score(own_chain, passage)` with `score(other_chain, passage)`.
```

```inputs
round(share_named(stoker_held, stoker_train, shelley_train, 100), 3)
round(share_named(shelley_held, shelley_train, stoker_train, 100), 3)
round(share_named(stoker_held, stoker_train, shelley_train, 20), 3)
round(share_named(shelley_held, shelley_train, stoker_train, 20), 3)
```

```solution
def share_named(held, own_chain, other_chain, length):
    """The share of passages from held that score higher under own_chain."""
    right = 0
    tried = 0
    for start in range(0, len(held) - length + 1, length):
        passage = held[start:start + length]
        tried += 1
        if score(own_chain, passage) > score(other_chain, passage):
            right += 1
    return right / tried
---
At 100 words, the chains name 0.857 of Stoker's passages and 0.96 of
Shelley's. At 20 words, that falls to 0.72 and 0.723: still better than
tossing a coin, but wrong about one time in four. A passage of 20 words
has only 19 pairs to go on, so a few lucky or unlucky pairs can swing
its score.
```

</div>

<div class="dl-world" data-world="stevenson-and-doyle">

Try it on two adventures: Robert Louis Stevenson's *Treasure Island*
and Arthur Conan Doyle's *The Lost World*. The cell builds a chain from
nine-tenths of each, and holds back the rest.

```python exec
id: whose-passage-is-it-4--stevenson-and-doyle
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


def share_named(held, own_chain, other_chain, length):
    """The share of passages from held that score higher under own_chain."""
    # Your code here.
```

```hint
The loop in `guess_writer`'s cell does this for one writer and 100
words. Put it inside a function, with `length` in place of 100, and
compare `score(own_chain, passage)` with `score(other_chain, passage)`.
```

```inputs
round(share_named(stevenson_held, stevenson_train, doyle_train, 100), 3)
round(share_named(doyle_held, doyle_train, stevenson_train, 100), 3)
round(share_named(stevenson_held, stevenson_train, doyle_train, 20), 3)
round(share_named(doyle_held, doyle_train, stevenson_train, 20), 3)
```

```solution
def share_named(held, own_chain, other_chain, length):
    """The share of passages from held that score higher under own_chain."""
    right = 0
    tried = 0
    for start in range(0, len(held) - length + 1, length):
        passage = held[start:start + length]
        tried += 1
        if score(own_chain, passage) > score(other_chain, passage):
            right += 1
    return right / tried
---
At 100 words, the chains name 0.912 of Stevenson's passages and 0.88 of
Doyle's. At 20 words, that falls to 0.738 and 0.728: still better than
tossing a coin, but wrong about one time in four. A passage of 20 words
has only 19 pairs to go on, so a few lucky or unlucky pairs can swing
its score.
```

</div>

## Reflection

A dictionary of dictionaries knows nothing about these writers as
people. It only counts which word followed which, in one book. Yet that
counting was enough to name the writer of most passages it had never
seen. A writer's voice is, at least in part, a pattern in which words
follow which, and the pattern is strong enough to measure.

A challenge: write two or three sentences in the style of Dewey or of
Montessori. Which chain claims them? Can you write one that fools the
chains? Then show your sentences to a classmate. Can they tell which
writer you were imitating before the chains do?

```python exec
id: reflection-1
mine = "Write your own sentences here, in the style of one of the two writers."
print("Dewey's chain:", round(score(dewey_train, mine.split()), 3))
print("Montessori's chain:", round(score(montessori_train, mine.split()), 3))
```

## Where to read more

CrashCourse (2019). *Make an AI sound like a YouTuber (LAB): Crash Course
AI #8.* <https://www.youtube.com/watch?v=kZWum5omEv4>. This lab trains a
program on one person's writing and asks it to write more in the same
style. It builds its model differently from our chain, and comes with a
notebook you can follow. Fifteen minutes.
