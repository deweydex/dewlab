---
title: "The perceptron: a model that learns from its mistakes — Practice"
practice_for: a-model-that-corrects-itself
year: "2026-2027"
version: 2026.09.22.1
---

# The perceptron: a model that learns from its mistakes — Practice

The answers are hidden in folds under each problem. Several problems ask
you to predict what the code will do before you run it. Try to answer
before you check. Being wrong, and finding out why, teaches you more than
being right by accident.

```python exec
id: setup-1
PLUS = [0, 1, 0,
        1, 1, 1,
        0, 1, 0]

CROSS = [1, 0, 1,
         0, 1, 0,
         1, 0, 1]

def predict(weights, bias, pixels):
    total = sum(w * p for w, p in zip(weights, pixels)) + bias
    return 1 if total > 0 else 0
```

## A Model That Starts Out Wrong

**1.** Set every weight to `0.0`, and the bias to `5.0`. Then call
`predict` on both `PLUS` and `CROSS`. Before you run it, what do you
expect, and why?

```python exec
id: a-model-that-starts-out-wrong-1
hint: With every weight at zero, the total is just the bias, whatever picture goes in.
```

<details class="dl-answer"><summary>answer</summary>

Both come back `1`, which means "plus", for both pictures. With every
weight at zero, `total` is `0 + 5.0`, whichever pixels are lit. And
`5.0 > 0` is always true. A model with a bias and no weights has made its
decision before it looks at the picture.

</details>

**2.** Write `predict_label()`, a version of `predict()` that returns the
string `"plus"` or `"cross"` instead of `1` or `0`. Do not change the
arithmetic.

<details class="dl-answer"><summary>answer</summary>

```python
def predict_label(weights, bias, pixels):
    return "plus" if predict(weights, bias, pixels) == 1 else "cross"
```

The arithmetic stays exactly as it is in `predict()`. Only the last step
changes: it turns a `1` or a `0` into a word a person would say.

</details>

## Running It Again and Again

**3.** The tutorial's training loop goes through `train` in the order it
is written.

1. Reverse that order with `list(reversed(train))`.
2. Train a new model from the start, with every weight at zero.
3. Compare the final weights with the tutorial's. Are they the same?

```python exec
id: running-it-again-and-again-1
hint: Copy the training loop, but iterate over list(reversed(train)) instead of train. Print the final weights and bias from both runs side by side.
```

<details class="dl-answer"><summary>answer</summary>

No. Both reach 100% train accuracy by the second epoch, but they end with
different weights.

| pixel | tutorial's order | reversed order |
|---|---|---|
| top-right | `0.0` | `-0.5` |
| mid-left | `+0.5` | `0.0` |
| mid-right | `0.0` | `+0.5` |
| bottom-right | `-0.5` | `0.0` |

The other five weights are the same in both.

There is no single correct set of weights here. There are only sets that
get every training example right. Which set the training finds depends on
which mistakes happened first.

</details>

**4.** Would a *larger* learning rate than `0.5` reach 100% train
accuracy in fewer epochs, the same number, or more? Make a prediction,
then try `2.0` and check.

```python exec
id: running-it-again-and-again-2
hint: Think back to what the tutorial found with 0.05. What does the learning rate do to every weight, when they all start at zero?
```

<details class="dl-answer"><summary>answer</summary>

It still takes two epochs. Every weight ends up four times as large as
with `0.5`: `2.0` in place of `0.5`, and `-2.0` in place of `-0.5`.

This is the same thing the tutorial found with `0.05`. Every weight
starts at zero, and every change is multiplied by the learning rate. So
changing the learning rate scales every weight and the bias by the same
amount. That never changes whether a total is above zero, so every
decision stays the same, and so does the number of epochs.

In bigger models, the weights do not all start at zero. There, the
learning rate matters much more. A rate that is too small can take a
very long time, and one that is too large can jump past good weights.

</details>

## Checking It Against Patterns It Has Never Seen

**5.** Use the tutorial's final `weights` and `bias`. Call `predict` on
the *original* `PLUS` and `CROSS`, with no pixels flipped. These two
pictures are in neither `train` nor `test`. What do you expect, before
you run it?

```python exec
id: checking-it-against-patterns-it-has-never-seen-1
hint: Every training example was PLUS or CROSS with one pixel flipped. So the clean originals are, in a way, the easiest possible test.
```

<details class="dl-answer"><summary>answer</summary>

Both are correct: `1` for `PLUS`, and `0` for `CROSS`. Every example in
`train` was one flipped pixel away from one of these two pictures. So the
clean pictures are closer to what the model learned than any of the
examples it was corrected against.

</details>

**6.** What does the model predict for a picture that is all zeros, with
no pixels lit at all? Work out the arithmetic by hand first.

```python exec
id: checking-it-against-patterns-it-has-never-seen-2
hint: Every weight gets multiplied by 0. What is left in the total?
```

<details class="dl-answer"><summary>answer</summary>

It predicts `0`, "cross". Here is why. Every term is `weight * 0`, so the
total is only the bias, which is `0.0`. The rule is
`1 if total > 0 else 0`. `0` is not greater than `0`, so a total of
exactly zero goes to "cross". For a blank picture, the bias alone decides
the answer. No weight plays any part.

</details>

## What the Model Learned

**7.** Imagine a tenth pixel added to every picture. It is always `0`, in
every training example, with no exceptions. What weight would you expect
it to end up with, and why?

<details class="dl-answer"><summary>answer</summary>

`0.0`. A pixel that never changes gives the model no way to tell the two
shapes apart. The tutorial gave the same reason for the centre pixel,
which both shapes share.

There is a second reason too. A weight only moves by
`learning_rate * error * pixel`. For a pixel that is always `0`, that
change is always zero, so its weight can never move.

</details>

**8.** In your own words, what is the difference between the *model* and
the *simulation* in this tutorial?

<details class="dl-answer"><summary>answer</summary>

The model is the fixed part: nine weights, one bias, and the rule in
`predict()` that turns a picture into a decision. The simulation runs
that rule over and over, across the training examples. The corrections
from each pass change what the next pass sees.

The difference matters. A new model, with every weight at zero, does
nothing useful on its own. The simulation is what produces a model that
works: guessing, checking and correcting, again and again.

</details>
