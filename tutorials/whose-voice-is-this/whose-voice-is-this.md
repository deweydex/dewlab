---
title: "Writing style: comparing two writers with Markov chains"
year: "2026-2027"
version: 2026.09.05.1
datasets: [democracy-and-education, the-montessori-method]
covers:
  cleaning-two-different-books:
    touches: [CMPS-LO1]
  two-writers-two-chains:
    covers: [CMPS-LO4]
  investigating-the-difference:
    touches: [CMPS-LO2]
---

# Writing style: comparing two writers with Markov chains

Two writers on education published books at almost the same time. John
Dewey wrote *Democracy and Education* (1916). Maria Montessori wrote *The
Montessori Method*, which came out in Italian in 1909. Our copy is the
English translation by Anne E. George, from 1912.

On this page we build a chain from each writer's book, separately. Then
we ask an open question. Does a chain trained on one writer's words
sound different from a chain trained on the other's?

## Cleaning Two Different Books

These two files come from scans of printed books. They are less tidy
than the Project Gutenberg books, such as *Pride and Prejudice*, that
came with [A Markov chain from a whole book: a dictionary of
dictionaries](tutorial:a-chain-reads-a-book). Neither
file has a `*** START OF... ***` marker to show where the book begins.
Each one needs its own way of cleaning. That is normal: real data rarely
arrives in exactly one shape.

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

Here is what the cell does:

1. `dewey_raw.find(marker)` finds the first copy of the title, in the
   table of contents.
2. `dewey_raw.find(marker, first + 1)` searches again, starting just
   after the first copy. So it finds the *second* copy, where Chapter I
   begins.
3. This book also has an index at the end. *The Time Machine* did not
   have one. `.find("INDEX")` gives the position where the index starts,
   and so where Dewey's writing stops.
4. The slice from `second` to `dewey_end` is the book itself.

### Your turn

The Montessori text needs the same find-it-twice method, with a different
marker: `"A CRITICAL CONSIDERATION OF THE NEW PEDAGOGY IN ITS RELATION TO"`.
These are the first words of Chapter I, and they also appear once in the
book's table of contents. This file ends with the words `"THE END"`, so
there is no index to cut from the end.

1. Load `"the-montessori-method.txt"`.
2. Find the first copy of the marker, then the second.
3. Keep everything from the second copy to the end of the file.

```python exec
id: cleaning-two-different-books-3
hint: montessori_raw = await load_text("the-montessori-method.txt"), then the same find-it-twice pattern used above for Dewey, without a second .find() for an ending — just raw[second:].strip().
```

## Two Writers, Two Chains

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

Run the cell a few times. Both chains start from the same word. Do they
go to the same kind of sentence, or does each one wander off in its own
way?

### Your turn

1. Pick a word that appears in both books, `"child"` or `"life"`, for
   example.
2. Generate 20 words from each writer's chain, starting from that word.
3. What differences do you notice?

```python exec
id: two-writers-two-chains-3
hint: "child" in dewey_chain and "child" in montessori_chain are both True — check before you pick a word, since not every word appears in both books.
```

## Investigating the Difference

Both books are about the same word: `"education"`. Do the two writers
follow it with the same words?

```python exec
id: investigating-the-difference-1
dewey_after = sorted(dewey_chain["education"].items(), key=lambda kv: -kv[1])[:5]
montessori_after = sorted(montessori_chain["education"].items(), key=lambda kv: -kv[1])[:5]
print("Dewey, most common words after 'education':", dewey_after)
print("Montessori, most common words after 'education':", montessori_after)
```

Here is how the cell finds the five most common words:

- `.items()` gives each follower with its count, as a pair such as
  `("is", 57)`.
- `sorted(..., key=...)` puts the pairs in order. `key=` says what to
  sort them by.
- `lambda kv: -kv[1]` is a small function written in one line. It takes
  a pair `kv` and gives back its count, `kv[1]`, with a minus sign. The
  minus sign puts the biggest count first.
- `[:5]` keeps the first five.

What do the two lines show? Dewey's most common word after `"education"`
is `"is"`, 57 times. Montessori's is `"of"`, 68 times. These counts come
from the whole of each book. They are not a random sample, so the numbers
are the same every time you run the cell.

One way to read the difference: Dewey keeps coming back to what
education *is*, which is a philosopher's habit. Montessori keeps coming
back to the education *of* someone or something, which is a practical
habit.

Dewey's book has 92 different words after `"education"`. Montessori's
has 36. So Dewey's use of the word ranges more widely. Part of the
reason is that he also uses the word about twice as often, 281 times
against 133, which gives it more chances to meet new neighbours.

### Your turn

None of this proves that a chain can tell who wrote a sentence with no
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

## Reflection

A dictionary of dictionaries knows nothing about Dewey or Montessori as
people. It only counts which word followed which, in one book. Yet that
counting alone is enough to show two different habits of writing. A
writer's voice is, at least in part, a pattern in which words follow
which. That pattern shows up often enough to be worth counting.
