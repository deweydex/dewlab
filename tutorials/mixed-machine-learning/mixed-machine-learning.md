---
title: "Mixed problems: machine learning"
practice_across:
  - a-chain-reads-a-book
  - how-much-it-remembers
  - whose-voice-is-this
  - a-model-that-corrects-itself
  - telling-many-pictures-apart
  - what-a-language-model-does-differently
  - limits-and-judgement
year: "2026-2027"
version: 2026.09.27.1
---

# Mixed problems: machine learning

These problems move between the pages of the course on purpose, and do
not say which page each one comes from. Choosing the idea is part of
the problem.

Each answer is hidden in a fold under its question. Work it out on
paper first where you can, then check in a cell.

```python exec
id: mixed-machine-learning-tools
import random
```

## Writing

**1.** In a chain, "the" is followed by "cat" 3 times and by "dog" once.
What is the chance of "dog" after "the" at a temperature of 1? At 0.5?
At 2?

```python exec
id: mixed-machine-learning-temperature
```

<details class="dl-answer"><summary>answer</summary>

At 1, the weights are the counts, so "dog" has 1 of 4: 0.25. At 0.5,
each count is squared, to 9 and 1, so "dog" has 1 of 10: 0.1. At 2,
each count is replaced by its square root, about 1.73 and 1, so "dog"
has about 1 ÷ 2.73: 0.366. A low temperature makes the common word
more common, and a high one gives the rare word more of a chance.

</details>

**2.** A chain keyed on two words writes 40 words, and 25 of them in a
row are copied, word for word, from its book. A chain keyed on one
word, from the same book, is asked to do the same. Would you expect a
longer copied run, or a shorter one? Why?

<details class="dl-answer"><summary>answer</summary>

A shorter one. Most two-word keys in a book have only one follower, so
after such a key the two-word chain has no choice, and it follows the
book. A one-word key such as "the" has hundreds of followers, so the
one-word chain leaves the book's path almost at once.

</details>

**3.** A tiny book has only these words: "hug" 10 times, "pug" 5,
"pun" 12, "bun" 4 and "hugs" 5. In byte-pair encoding, which two
letters become the first new piece? Which pair is joined second?

```python exec
id: mixed-machine-learning-pieces
```

<details class="dl-answer"><summary>answer</summary>

Count each pair of letters, once for every time its word appears. "u"
then "g" is in "hug", "pug" and "hugs": 10 + 5 + 5 = 20, more than any
other pair, so "ug" is the first new piece. After that, "u" then "n",
in "pun" and "bun", has 12 + 4 = 16, and "h" then "ug" has 15, so "un"
is second.

</details>

## Scoring

**4.** A model gives each next word in a 5-word passage a chance of
0.1. What is the passage's perplexity?

<details class="dl-answer"><summary>answer</summary>

There are 4 chances, one for each word after the first. Their product
is $0.1^4 = 0.0001$, and $0.0001^{-1/4} = 10$. A perplexity of 10 means
the model was as unsure as if it were choosing among 10 equally likely
words at each step.

</details>

**5.** A chain is built from the first nine-tenths of a book, with no
small chance kept for pairs it never saw. In the last tenth, 60% of the
word pairs never appeared in the first nine-tenths. What is the
product of the chances for a typical 20-word passage from the last
tenth?

<details class="dl-answer"><summary>answer</summary>

Almost certainly 0. A 20-word passage has 19 pairs, and with 60% of
pairs unseen, it would be very unlikely for all 19 to be seen. One
unseen pair has a chance of 0, and one 0 makes the whole product 0.
That is why `chance()` keeps a small chance for every word.

</details>

**6.** Two chains score a passage by the average chance they give each
next word. Chain A gives 0.12, and chain B gives 0.09. Which book is
the passage more likely to come from? What would make you trust that
answer more?

<details class="dl-answer"><summary>answer</summary>

A's book, since A gives it the higher score. One passage proves
little, though. The answer is worth more if the passages were held
back from both chains, if the test names the right book for most of
many passages, and if the passage is long enough: shorter passages
give closer, less reliable scores.

</details>

## Pictures

**7.** A perceptron wrongly says "cross" for a picture of a plus sign.
With a learning rate of 0.5, which weights change, and in which
direction? What happens to the bias?

<details class="dl-answer"><summary>answer</summary>

The error is 1 - 0 = 1. Each weight of a lit pixel goes up by 0.5,
and the weights of unlit pixels do not change, because they are
multiplied by a pixel of 0. The bias goes up by 0.5 too. Next time,
the same picture gets a higher total, closer to "plus".

</details>

**8.** Four perceptrons, one for each digit, give a picture the totals
0: −3.0, 1: −0.5, 4: −2.0, 7: −4.5. What does the classifier answer?
Did any perceptron say "yes"?

<details class="dl-answer"><summary>answer</summary>

It answers 1, the highest total. No perceptron said "yes": every total
is below zero. The classifier always names one class, even for a
picture that belongs to none of them.

</details>

**9.** A classifier for two classes has this confusion matrix. The rows
are the true classes, and the columns are its answers.

| | read as A | read as B |
|---|---|---|
| true A | 48 | 2 |
| true B | 15 | 35 |

What share does it get right overall? Which class does it do worse on,
and what share of that class does it get right?

```python exec
id: mixed-machine-learning-confusion
```

<details class="dl-answer"><summary>answer</summary>

The right answers are on the diagonal: 48 + 35 = 83 of 100, so 0.83
overall. It does worse on B: 35 of 50, or 0.7. The overall 0.83 hides
the fact that almost a third of the Bs are read as A.

</details>

## Claims

**10.** A test set has 90 pictures of class A and 10 of class B. A
classifier scores 0.91 on it. Is that good?

<details class="dl-answer"><summary>answer</summary>

Not by itself. A classifier that always says "A", without looking,
scores 0.9 on this set: that is the baseline. 0.91 is barely above it.
The confusion matrix would show how many of the 10 Bs it gets right,
which is the question that matters here.

</details>

**11.** A digit reader was trained on pictures with each digit in the
middle of the grid. Its makers say it is "95% accurate on handwritten
digits". Which question would you ask first, and what test would you
run?

<details class="dl-answer"><summary>answer</summary>

"On digits like which?" Real handwriting is not always in the middle.
Move the test pictures a column or two, and score them again. A model
that learned where the ink was, and not the shape, can fall far below
95%, as the reader on the limits page fell from 0.935 to 0.225.

</details>

**12.** A chain is built from a book in which "he" appears 900 times and
"she" 80 times. It writes 10,000 words. About how often would you
expect it to write "she", compared with "he"? Why?

<details class="dl-answer"><summary>answer</summary>

About the same ratio as the book: roughly 1 "she" for every 11 "he".
The chain only repeats the book's counts, so over a long passage its
words appear about as often as they do in the book. The chain adds
nothing of its own.

</details>
