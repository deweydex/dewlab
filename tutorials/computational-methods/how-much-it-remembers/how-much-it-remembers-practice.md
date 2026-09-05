---
title: "How Much It Remembers — Practice"
slug: how-much-it-remembers-practice
practice_for: how-much-it-remembers
module: computational-methods
module_title: "Computational Methods"
year: "2026-2027"
series: text-generation
version: 2026.09.05.2
---

# How Much It Remembers — Practice

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

## Counting the Choices

**1.** What fraction of `order1`'s keys have exactly one recorded
follower? What fraction of `order2`'s keys do?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. A key has exactly one recorded follower when its dictionary has exactly
   one entry — `len(order1[key]) == 1`.
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

About 67% of `order1`'s keys have only ever had one recorded follower.
For `order2`, that climbs to about 87%. Remembering one more word of
context does not just add detail — it turns most of the situations the
chain has ever seen into ones with only a single recorded outcome.

</details>

**2.** Find three real two-word pairs in `order2` that each have exactly
one recorded follower, appearing at least four times.

<details class="dl-answer"><summary>answer</summary>

```python
common_single = {
    k: v for k, v in order2.items()
    if len(v) == 1 and list(v.values())[0] >= 4
}
print(list(common_single.items())[:5])
```

`("a", "kind")` is always followed by `"of"`, 11 times: the fixed phrase
`"a kind of"`. `("Palace", "of")` is always followed by `"Green"`, 10
times — not an idiom this time, but a real place in the story, the
*Palace of Green Porcelain*, named the same way every time it comes up.
`("I", "determined")` is always followed by `"to"`, 8 times: another
fixed phrase, `"I determined to"`.

</details>

## Generating and Comparing

```python exec
id: generate-setup-1
import random

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
starting from the same word. Which one contains a longer unbroken run of
words that also appears, in the same order, somewhere in `book`?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Generate both, and read them side by side.
2. To check whether a phrase you spot really is lifted from the book, test
   it directly: `"some phrase here" in book`.
3. A short, common phrase (two or three words) will almost always test
   `True` by coincidence. Try a longer stretch before deciding it means
   anything.

</details>

<details class="dl-answer"><summary>answer</summary>

There is no single correct output, since the chain is genuinely random,
but the `order2` line should contain the longer verbatim run more often
than not, across repeated tries. That is the whole trade-off this
tutorial names: more context makes the chain lean more heavily on
stretches it has literally seen before.

</details>

**4. Try this next:** build an `order3` chain, keyed on the last *three*
words instead of two, and generate from it. Does it read even more like
real sentences from the book — or does it start breaking down for a
different reason?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The loop needs one more word of lookahead:
   `zip(words, words[1:], words[2:], words[3:])`.
2. The key is now a triple, `(w1, w2, w3)`, and the value it maps to is
   `w4`.
3. `generate3` needs to slide its key forward by dropping the oldest word
   and keeping the two newest, plus the word just chosen — the same idea
   `generate2` used, one word longer.

**Think about:** `order2` already had 22,457 keys from one book. What do
you expect `order3` to have — more, fewer, or about the same?

</details>
