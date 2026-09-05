---
title: "A Chain Reads a Book — Practice"
slug: a-chain-reads-a-book-practice
practice_for: a-chain-reads-a-book
module: computational-methods
module_title: "Computational Methods"
year: "2026-2027"
series: text-generation
version: 2026.09.05.1
---

# A Chain Reads a Book — Practice

Every question below works on the real book, exactly as the tutorial loaded
it. Load it once at the top of each section, the way the tutorial did.

## Cleaning the Text

```python exec
id: cleaning-setup-1
raw = await load_text("pride-and-prejudice.txt")
start_marker = "*** START OF THIS PROJECT GUTENBERG EBOOK PRIDE AND PREJUDICE ***"
end_marker = "*** END OF THIS PROJECT GUTENBERG EBOOK PRIDE AND PREJUDICE ***"
start = raw.find(start_marker)
end = raw.find(end_marker)
book = raw[raw.index("\n", start):end].strip()
```

**1.** How many characters shorter is `book` than `raw`? What does that
difference actually represent?

<details class="dl-answer"><summary>answer</summary>

```python
print(len(raw) - len(book))
```

19,293 — roughly how many characters of Project Gutenberg's own header and
licence text sat around the real novel, on both ends of the file. Nothing
in that difference is Jane Austen's writing.

</details>

**2.** *Pride and Prejudice* is divided into numbered chapters, each one
starting with a line like `Chapter 12`. Count how many chapter headings
appear in `book`.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. `book.split("\n")` gives every line as a separate string.
2. A chapter heading is a line that starts with the word `"Chapter"` —
   `line.startswith("Chapter")` tests exactly that.
3. Count how many lines pass that test.

**Think about:** would `"Chapter" in line` count anything extra that
`line.startswith("Chapter")` would not?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
lines = book.split("\n")
chapter_lines = [line for line in lines if line.startswith("Chapter")]
print(len(chapter_lines))
```

61 — the real number of chapters in the novel. `"Chapter" in line` would
also have matched any sentence that happened to mention the word
`"Chapter"` in passing, not only the headings themselves.

</details>

## How Many Words Does the Chain Actually Know

```python exec
id: chain-setup-1
words = book.split()
next_words = {}
for word, next_word in zip(words, words[1:]):
    next_words.setdefault(word, {})
    next_words[word][next_word] = next_words[word].get(next_word, 0) + 1
```

**3.** Which word in the book has the largest number of *different* words
following it somewhere? How many different followers does it have?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. For each word, `len(next_words[word])` counts how many different words
   have ever followed it.
2. `max(next_words, key=lambda w: len(next_words[w]))` finds the word with
   the largest count of any word in `next_words`.

**Think about:** is this likely to be a rare, distinctive word, or a very
common one?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
busiest = max(next_words, key=lambda w: len(next_words[w]))
print(busiest, len(next_words[busiest]))
```

`"the"`, with 1,685 different words following it somewhere in the book. That
makes sense once you think about it: `"the"` is one of the most common words
in English, sitting in front of almost any noun, so it has had a chance to
be followed by almost every noun the book ever uses.

</details>

**4.** Some words in the book are followed by exactly one other word, every
single time — never anything else. Find one where that single follower
appears at least ten times, and say what the pair is.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. A word with exactly one follower has `len(next_words[word]) == 1`.
2. For such a word, `list(next_words[word].values())[0]` is how many times
   that one follower actually appeared.
3. Filter for words meeting both conditions, then look at a few.

**Try this next:** why might a word like `"obliged"` almost always be
followed by the same next word?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
single = {
    w: d for w, d in next_words.items()
    if len(d) == 1 and list(d.values())[0] >= 10
}
print(sorted(single.items(), key=lambda kv: -list(kv[1].values())[0])[:5])
```

`"obliged"` is followed only by `"to"`, 26 times: every single occurrence
in the book. `"spite"` is followed only by `"of"`, 23 times. Both are half
of a fixed phrase, `"obliged to"` and `"in spite of"`, where English
almost never allows a different word in second place, so the chain never
sees one either.

</details>

## Generating Your Own Sentences

```python exec
id: generating-setup-1
import random

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
```

**5.** Pick any character's name that appears in the book and generate 25
words starting from it. Run it three times. How different are the three
results from each other?

```python exec
id: generating-1
```

**6.** `generate()` breaks out of its loop early if `current not in
next_words`. Does that line actually ever run for this book — is there a
real word with no recorded follower at all?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. `set(words)` is every distinct word in the book.
2. `set(next_words.keys())` is every word that has at least one recorded
   follower.
3. Subtracting one set from the other, `set(words) - set(next_words.keys())`,
   leaves only the words that are in the first set but not the second.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
missing = set(words) - set(next_words.keys())
print(missing)
```

An empty set. Every one of the 13,067 distinct words in the book has at
least one recorded follower, so `generate()`'s early-exit line never
actually runs on this particular text. It is still worth having: a
shorter piece of text, or one cleaned differently, could easily end on a
word that never appears anywhere else in it, and without that check
`generate()` would crash instead of simply stopping.

There is a small, honest wrinkle even in `words[-1]`, the very last word.
It reads `"Austen"`, not from the novel itself, but from Project
Gutenberg's own closing line, `"...by Jane Austen"`, which sits inside the
`*** END OF... ***` marker along with the real text. `"Austen"` also
appears earlier, on the title page, so it still has a recorded follower.
That is a reminder that the cleaning step earlier in this tutorial finds
the *edges* Gutenberg marks, not a guarantee that every trace of
Gutenberg's own text is gone from inside them.

</details>
