---
title: "A Markov chain from a whole book: a dictionary of dictionaries — Practice"
practice_for: a-chain-reads-a-book
year: "2026-2027"
version: 2026.09.05.2
datasets: [the-time-machine, the-war-of-the-worlds, frankenstein, a-princess-of-mars, the-lost-world, pride-and-prejudice]
---

# A Markov chain from a whole book: a dictionary of dictionaries — Practice

Every question below works on the real book, loaded and cleaned just as
in the tutorial. Each section starts with a cell that does that
loading. Run it before you try the questions in that section.

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

**1.** How many characters shorter is `book` than `raw`? What are those
missing characters?

<details class="dl-answer"><summary>answer</summary>

```python
print(len(raw) - len(book))
```

19,377. That is how many characters of Project Gutenberg's own header and
licence text sat around the novel, at both ends of the file, plus the
marker lines and the empty lines that `.strip()` removed. None of it is
H. G. Wells's writing.

</details>

**2.** *The Time Machine* has sixteen numbered chapters. Each chapter
heading is a line with nothing on it but a Roman numeral, like `XII`. The
table of contents near the top is different: there, each numeral shares
a line with the chapter's title. How many chapter headings can you count
in `book`?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. `book.split("\n")` gives a list with every line as a separate string.
2. A chapter heading, once `.strip()` removes the spaces around it, is
   made only of the letters `I`, `V`, `X`, `L` and `C`. Those are the
   letters Roman numerals use.
3. `set(line.strip())` is the set of different letters in the line. The
   test `set(line.strip()) <= set("IVXLC")` is `True` when every one of
   those letters is also in `"IVXLC"`. That saves checking the letters one
   at a time.
4. An empty line passes that test too, because an empty set counts as
   being inside any set. So check that `line.strip()` is not empty
   first.

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

16, the number of chapters in the novel. The lines of the table of
contents never pass the test. Each one also has the chapter's title on
it, and a title has letters that are not `I`, `V`, `X`, `L` or `C`.

</details>

## How Many Words Does the Chain Know?

```python exec
id: chain-setup-1
words = book.split()
next_words = {}
for word, next_word in zip(words, words[1:]):
    next_words.setdefault(word, {})
    next_words[word][next_word] = next_words[word].get(next_word, 0) + 1
```

**3.** Which word in the book is followed by the largest number of
*different* words? How many different followers does it have?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. For each word, `len(next_words[word])` counts how many different words
   have followed it.
2. You could loop over `next_words` and keep the word with the biggest
   count so far.
3. Or `max()` can do the loop for you. `key=` tells `max()` what to
   compare. `lambda word: len(next_words[word])` is a small function
   written in one line. It takes a word and gives back its number of
   followers.

**Think about:** is this likely to be a rare, distinctive word, or a very
common one?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
busiest = max(next_words, key=lambda word: len(next_words[word]))
print(busiest, len(next_words[busiest]))
```

It is `"the"`, with 1,162 different words after it. Does that make
sense? `"the"` is one of the most common words in English, and it can go
in front of almost any noun. So it has had the chance to be followed by
almost every noun the book uses.

</details>

**4.** Some words in the book are followed by the same word every time,
and never by anything else. Can you find one where that pair appears at
least five times? What is the pair?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. A word with exactly one follower has `len(next_words[word]) == 1`.
2. For such a word, the inner dictionary has one key and one value. The
   value is how many times that follower appeared.
3. Loop over the words, keep the ones that pass both tests, and look at
   a few.

**Try this next:** why might a word like `"determined"` almost always be
followed by the same next word?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
for word, followers in next_words.items():
    if len(followers) == 1:
        for follower, count in followers.items():
            if count >= 5:
                print(word, follower, count)
```

There are ten. `"sense"` is followed only by `"of"`, 11 times: every
time it appears in the book. `"determined"` is followed only by `"to"`,
9 times. Both are the first half of a fixed phrase, `"sense of"` and
`"determined to"`. English almost never puts a different word in second
place, so the chain never sees one either.

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

**5.** Pick any word that appears often in the book.

1. Generate 25 words starting from it.
2. Run the cell three times.
3. How different are the three results from each other?

```python exec
id: generating-1
```

**6.** `generate()` stops its loop early if `current not in next_words`.
Does that ever happen with this book? Is there a word in the book with no
recorded follower at all?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. `set(words)` is every distinct word in the book.
2. `set(next_words.keys())` is every word that has at least one recorded
   follower.
3. Taking one set away from the other,
   `set(words) - set(next_words.keys())`, leaves only the words that are
   in the first set and not in the second.

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

Look at `words[-1]`, the very last word. It is `"Wells"`, and it does not
come from the novel. It comes from Project Gutenberg's own closing line,
`"End of the Project Gutenberg EBook of The Time Machine, by H. G. Wells"`, which
sits before the `*** END OF... ***` marker, so the cleaning kept it.
`"Wells"` also appears earlier, on the title page, so it still has a
recorded follower. The cleaning step finds the edges that Gutenberg
marks. It does not promise that every trace of Gutenberg's own text is
gone from between them.

</details>

## A Different Book

This series comes with six real books: *The Time Machine*, *The War of
the Worlds*, *Frankenstein*, *A Princess of Mars*, *The Lost World*, and
*Pride and Prejudice*. Each one is a file in the shared data folder:
`the-war-of-the-worlds.txt`, `frankenstein.txt`, `a-princess-of-mars.txt`,
`the-lost-world.txt` and `pride-and-prejudice.txt`.

**7.** Pick a different book from that list. Every one of them comes from
Project Gutenberg, so each has the same two marker lines,
`*** START OF THIS PROJECT GUTENBERG EBOOK <TITLE> ***` and
`*** END OF THIS PROJECT GUTENBERG EBOOK <TITLE> ***`, with its own title
in place of `THE TIME MACHINE`.

1. Load the book.
2. Clean it.
3. Build a chain from it.
4. Generate 25 words.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. `raw = await load_text("frankenstein.txt")` (or whichever filename you
   picked).
2. Print the first few hundred characters of `raw` to find that book's
   exact marker text. The shape is always the same. Only the title in the
   middle changes.
3. Everything else is the same code this page already uses: the
   cleaning, building `next_words`, and `generate()`.

**Think about:** how many cells would a dense grid need for this book?
(That is the number of different words, squared.) Is it bigger or
smaller than for *The Time Machine*? Bigger or smaller than for *Pride
and Prejudice*?

</details>
