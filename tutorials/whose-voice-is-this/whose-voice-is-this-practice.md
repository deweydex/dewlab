---
title: "Writing style: comparing two writers with Markov chains — Practice"
practice_for: whose-voice-is-this
year: "2026-2027"
version: 2026.09.05.1
---

# Writing style: comparing two writers with Markov chains — Practice

The cell below loads and cleans both books, in the same way as the
tutorial, and builds a chain from each. Run it first.

```python exec
id: setup-1
dewey_raw = await load_text("democracy-and-education.txt")
dewey_marker = "EDUCATION AS A NECESSITY OF LIFE"
dewey_first = dewey_raw.find(dewey_marker)
dewey_second = dewey_raw.find(dewey_marker, dewey_first + 1)
dewey_end = dewey_raw.find("INDEX")
dewey_book = dewey_raw[dewey_second:dewey_end].strip()

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

dewey_chain = build_chain(dewey_book)
montessori_chain = build_chain(montessori_book)
```

## Comparing One Word

**1.** How many different words follow `"child"` in Dewey's chain? In
Montessori's? Which writer's use of the word is more repetitive? Here,
more repetitive means going back to the same few next words again and
again.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. `len(dewey_chain["child"])` and `len(montessori_chain["child"])` count
   how many different words follow `"child"` in each.
2. `sum(dewey_chain["child"].values())` counts how many times `"child"`
   is followed by anything at all. That is how many times the writer
   used the word.
3. Divide the number of different followers by the number of uses. A
   smaller answer means the same followers come back more often: the use
   is more repetitive.

**Think about:** why is it not fair to compare the numbers of different
followers on their own?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
print(len(dewey_chain["child"]))
print(len(montessori_chain["child"]))
print(sum(dewey_chain["child"].values()))
print(sum(montessori_chain["child"].values()))
```

There are 38 different followers in Dewey and 230 in Montessori. So
Montessori's chain has *more* different words after `"child"`. Does that
make her less repetitive? No. She uses the word 604 times, and Dewey
uses it only 53 times. Her book is about children from start to finish,
so the word meets many more neighbours. Dewey's book covers a wider
subject and mentions `"child"` much less often.

Now divide. For Dewey, $38 / 53 pprox 0.72$: almost every use has a
new follower. For Montessori, $230 / 604 pprox 0.38$: the same
followers come back much more often. Montessori's use of `"child"` is
the more repetitive one.

```python
print(sorted(montessori_chain["child"].items(), key=lambda kv: -kv[1])[:3])
```

Three words alone, `"to"`, `"is"` and `"who"`, follow `"child"` 124
times between them in Montessori's book: 50, 42 and 32. That is a real
pattern in how she builds a sentence around the word.

</details>

## Comparing the Whole Vocabulary

**2.** How many different words appear in *both* chains? How many appear
in only one of them?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. `set(dewey_chain)` and `set(montessori_chain)` give the different
   words that each chain has as keys.
2. `&` between two sets gives the values they share.
3. `-` between two sets gives the values that are only in the set on the
   left.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
shared = set(dewey_chain) & set(montessori_chain)
dewey_only = set(dewey_chain) - set(montessori_chain)
montessori_only = set(montessori_chain) - set(dewey_chain)
print(len(shared), len(dewey_only), len(montessori_only))
```

5,115 words are in both. 11,026 words appear only in Dewey, and 9,278
only in Montessori. So two books on a related subject share less than
half of their words. Most of the words each writer uses never appear in
the other's book.

One thing to keep in mind: `split()` cuts only at spaces, so `"child"`
and `"child,"` count as different words. Some of the words "only in
Dewey" are words Montessori also uses, with different punctuation next
to them.

</details>

## Generating and Comparing

```python exec
id: generate-setup-1
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
```

**3.** Pick a word that is in `shared` from problem 2.

1. Generate 20 words from each writer's chain, starting from that word.
2. Read them side by side. What do you notice?

```python exec
id: generate-1
hint: Check "your word" in shared first — problem 2's shared set only exists if you ran that answer cell, so build it again here if you skipped straight to this one.
```

**4. Try this next:** repeat problem 1 for a few more shared words of your
own. Can you see a pattern in *which kinds* of words show the biggest
gap between the two writers? Compare words about each book's subject,
like `"child"`, with ordinary joining words.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Choose a word close to each book's main subject, like `"child"` or
   `"development"`.
2. Choose a very ordinary word that both books use all the time,
   whatever the subject, like `"and"` or `"the"`.
3. Work out the same numbers for both.

**Think about:** which kind of word do you expect to differ more between
the two writers?

</details>
