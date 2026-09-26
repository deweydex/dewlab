---
title: "N-grams: a Markov chain that remembers more words — Practice"
practice_for: how-much-it-remembers
year: "2026-2027"
version: 2026.09.25.1
datasets: [the-time-machine]
---

# N-grams: a Markov chain that remembers more words — Practice

The cell below loads and cleans the book, then builds both chains,
`order1` and `order2`, just as the tutorial did. Run it first.

```python exec
id: setup-1
raw = await load_text("the-time-machine.txt")
start_marker = "*** START OF THIS PROJECT GUTENBERG EBOOK THE TIME MACHINE ***"
end_marker = "*** END OF THIS PROJECT GUTENBERG EBOOK THE TIME MACHINE ***"
start = raw.find(start_marker)
end = raw.find(end_marker)
book = raw[raw.index("\n", start):end].strip()
words = book.split()

order1 = {}
for word, next_word in zip(words, words[1:]):
    order1.setdefault(word, {})
    order1[word][next_word] = order1[word].get(next_word, 0) + 1

order2 = {}
for w1, w2, w3 in zip(words, words[1:], words[2:]):
    key = (w1, w2)
    order2.setdefault(key, {})
    order2[key][w3] = order2[key].get(w3, 0) + 1
```

## Counting the choices

**1.** What fraction of `order1`'s keys have exactly one recorded
follower? What fraction of `order2`'s keys do? Which fraction do you
expect to be bigger?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. A key has exactly one recorded follower when its inner dictionary has
   exactly one entry: `len(order1[key]) == 1`.
2. Count how many keys in `order1` meet that test, then divide by
   `len(order1)`.
3. Do the same for `order2`.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
single1 = [k for k in order1 if len(order1[k]) == 1]
single2 = [k for k in order2 if len(order2[k]) == 1]
print(len(single1) / len(order1))
print(len(single2) / len(order2))
```

About 67% of `order1`'s keys have only one recorded follower. For
`order2`, that rises to about 87%. One more word of memory does more
than add detail. For most of the pairs the chain has seen, there is only
one word it can choose next.

</details>

**2.** Can you find three two-word keys in `order2` that have exactly one
recorded follower, where that follower appears at least four times?

<details class="dl-answer"><summary>answer</summary>

```python
common_single = [
    (pair, followers) for pair, followers in order2.items()
    if len(followers) == 1 and list(followers.values())[0] >= 4
]
print(len(common_single))
for item in common_single:
    print(item)
```

There are 18. Here are three of them:

- `("a", "kind")` is always followed by `"of"`, 11 times. That is the
  fixed phrase `"a kind of"`.
- `("Palace", "of")` is always followed by `"Green"`, 10 times. This one
  is a place in the story, the *Palace of Green Porcelain*. The book
  names it the same way every time.
- `("I", "determined")` is always followed by `"to"`, 8 times. That is
  another fixed phrase, `"I determined to"`.

</details>

## Generating and comparing

```python exec
id: generate-setup-1
import random

random.seed(1)    # run this cell again to start the same runs over

def generate1(start_word, steps):
    result = [start_word]
    current = start_word
    for _ in range(steps):
        if current not in order1:
            break
        candidates = order1[current]
        current = random.choices(list(candidates.keys()), weights=list(candidates.values()))[0]
        result.append(current)
    return " ".join(result)

def generate2(w1, w2, steps):
    result = [w1, w2]
    current = (w1, w2)
    for _ in range(steps):
        if current not in order2:
            break
        candidates = order2[current]
        next_word = random.choices(list(candidates.keys()), weights=list(candidates.values()))[0]
        result.append(next_word)
        current = (current[1], next_word)
    return " ".join(result)
```

**3.** Generate 25 words from `order1` and 25 words from `order2`, both
starting from the same word. Which one has a longer run of words that
also appears, in the same order, somewhere in `book`?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Generate both, and read them side by side.
2. To check whether a phrase you spot is copied from the book, test it:
   `"some phrase here" in book`.
3. A short, common phrase of two or three words will almost always test
   `True` by chance. Try a longer stretch before you decide it means
   anything.

</details>

<details class="dl-answer"><summary>answer</summary>

There is no single expected output, because the chain chooses at random.
Over several tries, though, the `order2` line should have the longer
copied run more often than not. That is the trade-off from the
tutorial: with more context, the chain leans more on stretches of the
book it has seen before.

</details>

**4. Try this next:** build an `order3` chain, keyed on the last *three*
words, and generate from it. Does it read even more like real sentences
from the book? Or does it start to fail for a different reason?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The loop needs one more word of lookahead:
   `zip(words, words[1:], words[2:], words[3:])`.
2. The key is now a triple, `(w1, w2, w3)`, and the value it maps to is
   `w4`.
3. `generate3` moves its key forward in the same way `generate2` did,
   one word longer. It drops the oldest word, keeps the two newer ones,
   and adds the word just chosen.

**Think about:** `order2` already had 22,457 keys from one book. Do you
expect `order3` to have more, fewer, or about the same?

</details>
