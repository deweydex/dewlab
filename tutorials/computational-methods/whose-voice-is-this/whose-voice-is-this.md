---
title: "Whose Voice Is This"
slug: whose-voice-is-this
module: computational-methods
module_title: "Computational Methods"
year: "2026-2027"
series: text-generation
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

# Whose Voice Is This

Two educational philosophers wrote at almost the same moment in history:
John Dewey's *Democracy and Education* (1916), and Maria Montessori's *The
Montessori Method* (1912, translated into English by Anne E. George). This
tutorial builds a chain from each writer separately and asks a genuinely
open question — does a chain trained on one writer's words actually sound
different from a chain trained on the other's?

## Cleaning Two Different Books

These two files are scans of real printed books, not clean digital
editions like *Pride and Prejudice* was. Neither has Project Gutenberg's
handy `*** START OF... ***` marker, and each needs a slightly different
cleaning approach — real data rarely arrives in exactly one shape.

```python exec
id: cleaning-two-different-books-1
dewey_raw = await load_text("democracy-and-education.txt")
print(dewey_raw[:400])
```

The first several thousand characters are a publisher's catalogue of other
books in the same series, followed by *Democracy and Education*'s own
title page and table of contents — none of it Dewey's own writing. The
chapter title `"EDUCATION AS A NECESSITY OF LIFE"` appears twice: once in
the table of contents, and once again at the real start of Chapter I.

```python exec
id: cleaning-two-different-books-2
marker = "EDUCATION AS A NECESSITY OF LIFE"
first = dewey_raw.find(marker)
second = dewey_raw.find(marker, first + 1)
dewey_end = dewey_raw.find("INDEX")
dewey_book = dewey_raw[second:dewey_end].strip()
print(len(dewey_book.split()), "words of real Dewey")
```

`dewey_raw.find(marker, first + 1)` searches again, starting just after
the first match, so it finds the *second* occurrence instead of stopping at
the first. This book also has an index at the very end, the same kind of
back matter *A Chain Reads a Book* never had to handle — `.find("INDEX")`
marks where the real writing stops.

### Your turn

The Montessori text needs the same find-it-twice technique, on a different
marker: `"A CRITICAL CONSIDERATION OF THE NEW PEDAGOGY IN ITS RELATION TO"`
— the real opening words of Chapter I, which also appear once in that
book's own table of contents. This file ends cleanly with the words
`"THE END"`, so there is no index to trim from the end.

```python exec
id: cleaning-two-different-books-3
hint: montessori_raw = await load_text("the-montessori-method.txt"), then the same find-it-twice pattern used above for Dewey, without a second .find() for an ending — just raw[second:].strip().
```

## Two Writers, Two Chains

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

Run that cell a few times. Both chains start from the same word, and both
still wander into their own kind of sentence.

### Your turn

Pick a word that appears in both books, `"child"` or `"life"`, say, and
generate 20 words from each writer's chain, starting from that same word.

```python exec
id: two-writers-two-chains-3
hint: "child" in dewey_chain and "child" in montessori_chain are both True — check before you pick a word, since not every word appears in both books.
```

## Investigating the Difference

Both books are, in a real sense, about the same word: `"education"`.
What actually follows it is not the same at all.

```python exec
id: investigating-the-difference-1
dewey_after = sorted(dewey_chain["education"].items(), key=lambda kv: -kv[1])[:5]
montessori_after = sorted(montessori_chain["education"].items(), key=lambda kv: -kv[1])[:5]
print("Dewey, most common words after 'education':", dewey_after)
print("Montessori, most common words after 'education':", montessori_after)
```

Dewey's most common word after `"education"` is `"is"`, used 57 times.
Montessori's is `"of"`, used 68 times. This is a real, repeatable
difference in how each writer uses the word, not a coincidence between two
random samples: Dewey keeps returning to what education *is*, a
philosophical, definitional habit; Montessori keeps returning to education
*of* something or someone, a practical, applied one. `"education"` has 92
different words that have ever followed it somewhere in Dewey's book,
against 36 in Montessori's — Dewey's use of the word ranges more widely.

### Your turn

None of this proves a chain can identify who wrote an unlabelled sentence
— it only shows that two real writers used one shared word differently.
Pick your own shared word and investigate: how many different words follow
it in each chain, and what is the single most common one in each? Does the
difference say anything believable about how these two writers actually
wrote?

```python exec
id: investigating-the-difference-2
```

## Reflection

A dictionary of dictionaries does not know anything about Dewey or
Montessori as people. It only ever counts what word followed what, in one
particular book. And yet that counting alone is enough to produce two
visibly different habits of speech. A writer's voice is, at least in part,
a pattern in which words follow other words, often enough to be worth
counting.
