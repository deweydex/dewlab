---
title: "A Chain Reads a Book — Practice"
slug: a-chain-reads-a-book-practice
practice_for: a-chain-reads-a-book
module: computational-methods
module_title: "Computational Methods"
year: "2026-2027"
series: text-generation
version: 2026.09.05.2
datasets: [the-time-machine, the-war-of-the-worlds, frankenstein, a-princess-of-mars, the-lost-world, pride-and-prejudice]
---

# A Chain Reads a Book — Practice

Every question below works on the real book, exactly as the tutorial loaded
it. Load it once at the top of each section, the way the tutorial did.

## Cleaning the Text

```python exec
id: cleaning-setup-1
raw = await load_text("the-time-machine.txt")
start_marker = "*** START OF THIS PROJECT GUTENBERG EBOOK THE TIME MACHINE ***"
end_marker = "*** END OF THIS PROJECT GUTENBERG EBOOK THE TIME MACHINE ***"
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

19,377 — roughly how many characters of Project Gutenberg's own header and
licence text sat around the real novel, on both ends of the file. Nothing
in that difference is H. G. Wells's writing.

</details>

**2.** *The Time Machine* is divided into sixteen numbered chapters. Each
real chapter heading is a line holding nothing but a Roman numeral, like
`XII`, on a line of its own — different from the table of contents near
the top of the book, where the same numeral shares a line with the
chapter's title. Count how many real chapter headings appear in `book`.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. `book.split("\n")` gives every line as a separate string.
2. A real chapter heading, once you strip its surrounding spaces, is made
   up only of the letters `I`, `V`, `X`, `L`, `C` — the same letters Roman
   numerals use. `set(line.strip()) <= set("IVXLC")` tests exactly that,
   using set membership instead of comparing letter by letter.
3. An empty line passes that test too, since an empty set counts as a
   subset of anything — check `line.strip()` is not empty first.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
roman = set("IVXLC")
lines = book.split("\n")
chapter_lines = [
    line for line in lines
    if line.strip() and set(line.strip()) <= roman
]
print(len(chapter_lines))
```

16 — the real number of chapters in the novel. The table of contents lines
never pass the test, because each one also has the chapter's title on the
same line, and a title's letters are not all drawn from `I`, `V`, `X`, `L`,
`C`.

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

`"the"`, with 1,162 different words following it somewhere in the book. That
makes sense once you think about it: `"the"` is one of the most common words
in English, sitting in front of almost any noun, so it has had a chance to
be followed by almost every noun the book ever uses.

</details>

**4.** Some words in the book are followed by exactly one other word, every
single time — never anything else. Find one where that single follower
appears at least five times, and say what the pair is.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. A word with exactly one follower has `len(next_words[word]) == 1`.
2. For such a word, `list(next_words[word].values())[0]` is how many times
   that one follower actually appeared.
3. Filter for words meeting both conditions, then look at a few.

**Try this next:** why might a word like `"determined"` almost always be
followed by the same next word?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
single = {
    w: d for w, d in next_words.items()
    if len(d) == 1 and list(d.values())[0] >= 5
}
print(sorted(single.items(), key=lambda kv: -list(kv[1].values())[0])[:5])
```

`"sense"` is followed only by `"of"`, 11 times: every single occurrence
in the book. `"determined"` is followed only by `"to"`, 9 times. Both are
half of a fixed phrase, `"sense of"` and `"determined to"`, where English
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

**5.** Pick any word that appears often in the book and generate 25 words
starting from it. Run it three times. How different are the three results
from each other?

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

An empty set. Every one of the 6,991 distinct words in the book has at
least one recorded follower, so `generate()`'s early-exit line never
actually runs on this particular text. It is still worth having: a
shorter piece of text, or one cleaned differently, could easily end on a
word that never appears anywhere else in it, and without that check
`generate()` would crash instead of simply stopping.

There is a small, honest wrinkle even in `words[-1]`, the very last word.
It reads `"Wells"`, not from the novel itself, but from Project
Gutenberg's own closing line, `"...by H. G. Wells"`, which sits inside the
`*** END OF... ***` marker along with the real text. `"Wells"` also
appears earlier, on the title page, so it still has a recorded follower.
That is a reminder that the cleaning step earlier in this tutorial finds
the *edges* Gutenberg marks, not a guarantee that every trace of
Gutenberg's own text is gone from inside them.

</details>

## A Different Book

This series bundles six real books: *The Time Machine*, *The War of the
Worlds*, *Frankenstein*, *A Princess of Mars*, *The Lost World*, and
*Pride and Prejudice* — each one a real filename in `data/`
(`the-war-of-the-worlds.txt`, `frankenstein.txt`, `a-princess-of-mars.txt`,
`the-lost-world.txt`, `pride-and-prejudice.txt`).

**7.** Pick a different book from that list. Every one of them is a real
Project Gutenberg release, so it carries the same
`*** START OF THIS PROJECT GUTENBERG EBOOK <TITLE> ***` and
`*** END OF THIS PROJECT GUTENBERG EBOOK <TITLE> ***` markers, just with
its own title in place of `THE TIME MACHINE`. Load it, clean it, build a
chain from it, and generate 25 words.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. `raw = await load_text("frankenstein.txt")` (or whichever filename you
   picked).
2. Print the first few hundred characters of `raw` to find that book's
   exact marker text — it always follows the same shape, but the title in
   the middle changes.
3. Everything else — cleaning, building `next_words`, `generate()` — is
   identical code to what this page already uses.

**Think about:** does this book's dense vocabulary size (distinct words
squared) turn out bigger or smaller than *The Time Machine*'s? Bigger or
smaller than *Pride and Prejudice*'s from the tutorial's own numbers?

</details>
