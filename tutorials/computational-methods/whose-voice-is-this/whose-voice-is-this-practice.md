---
title: "Whose Voice Is This — Practice"
slug: whose-voice-is-this-practice
practice_for: whose-voice-is-this
module: computational-methods
module_title: "Computational Methods"
year: "2026-2027"
series: text-generation
version: 2026.09.05.1
---

# Whose Voice Is This — Practice

Both books are loaded and cleaned once, the same way the tutorial did.

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
Montessori's? Which writer's use of the word is more repetitive, in the
sense of returning to a small handful of the same next words again and
again?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. `len(dewey_chain["child"])` and `len(montessori_chain["child"])` count
   how many different words follow `"child"` in each.
2. A smaller number of distinct followers, spread across the same total
   number of uses, means each one is chosen more often on average — more
   repetitive, not less.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
print(len(dewey_chain["child"]))
print(len(montessori_chain["child"]))
```

38 in Dewey, 230 in Montessori. That is a striking difference in the
opposite direction from what the raw numbers might suggest at first
glance: Montessori's chain has *more* different words following `"child"`,
not fewer — because her whole book returns to the word constantly, in
enough different sentences to have paired it with far more neighbours.
Dewey's book is broader in subject and mentions `"child"` comparatively
rarely.

```python
print(sorted(montessori_chain["child"].items(), key=lambda kv: -kv[1])[:3])
```

Even so, three words alone, `"to"`, `"is"`, and `"who"`, account for well
over a hundred of Montessori's uses between them: a real pattern in how
she tends to build a sentence around the word.

</details>

## Comparing the Whole Vocabulary

**2.** How many distinct words appear in *both* chains? How many appear in
only one or the other?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. `set(dewey_chain)` and `set(montessori_chain)` give the distinct words
   each chain actually has as keys.
2. `&` between two sets gives what they share; `-` gives what is only in
   the one on the left.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
shared = set(dewey_chain) & set(montessori_chain)
dewey_only = set(dewey_chain) - set(montessori_chain)
montessori_only = set(montessori_chain) - set(dewey_chain)
print(len(shared), len(dewey_only), len(montessori_only))
```

5,115 words in both. 11,026 words that only ever appear in Dewey.
9,278 that only ever appear in Montessori. Two books on a related subject
still end up mostly *not* sharing vocabulary — most of what either writer
says, they say using words the other one never happens to use at all.

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

**3.** Pick a word that appears in `shared` from problem 2. Generate 20
words from each writer's chain, starting from that word, and read them
side by side.

```python exec
id: generate-1
hint: Check "your word" in shared first — problem 2's shared set only exists if you ran that answer cell, so build it again here if you skipped straight to this one.
```

**4. Try this next:** repeat problem 1 for a few more shared words of your
own choosing. Does a pattern emerge in *which kinds* of words show the
biggest gap between the two writers — proper subjects of each book, like
`"child"`, versus more ordinary connecting words?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

Compare a word close to each book's central subject (`"child"`,
`"development"`) against a very ordinary word both books use constantly
regardless of subject (`"and"`, `"the"`). Which kind of word do you expect
to differ more between the two writers?

</details>
