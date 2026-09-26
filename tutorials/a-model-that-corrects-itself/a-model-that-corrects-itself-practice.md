---
title: "The perceptron: a model that learns from its mistakes — Practice"
practice_for: a-model-that-corrects-itself
year: "2026-2027"
version: 2026.09.25.1
---

# The perceptron: a model that learns from its mistakes — Practice

The answers are hidden in folds under each problem. Several problems ask
you to predict what the code will do before you run it. Try to answer
before you check. A wrong guess teaches you more than a lucky right one,
once you see why it was wrong.

The cell below creates everything the problems use: the two shapes,
`predict()`, the tutorial's twenty messy pictures in `train`, and a
function `fit()` that runs the tutorial's training loop. Its last line
trains the same model the tutorial did.

```python exec
id: setup-1
import random

PLUS = [0, 1, 0,
        1, 1, 1,
        0, 1, 0]

CROSS = [1, 0, 1,
         0, 1, 0,
         1, 0, 1]

def predict(weights, bias, pixels):
    total = sum(w * p for w, p in zip(weights, pixels)) + bias
    return 1 if total > 0 else 0


def noisy(picture, flips):
    copy = list(picture)
    for i in random.sample(range(9), flips):
        copy[i] = 1 - copy[i]
    return copy


random.seed(1)    # the same twenty pictures as the tutorial
train = []
for _ in range(10):
    train.append((noisy(PLUS, 3), 1))
    train.append((noisy(CROSS, 3), 0))
random.shuffle(train)


def fit(examples, learning_rate=0.5, epochs=10):
    """The tutorial's training loop. Gives back the final weights and bias."""
    weights, bias = [0.0] * 9, 0.0
    for _ in range(epochs):
        for pixels, label in examples:
            error = label - predict(weights, bias, pixels)
            for i in range(9):
                weights[i] += learning_rate * error * pixels[i]
            bias += learning_rate * error
    return weights, bias


weights, bias = fit(train)
```

## A model that starts out wrong

**1.** Set every weight to `0.0`, and the bias to `5.0`. Then call
`predict` on both `PLUS` and `CROSS`. Before you run it, what do you
expect, and why?

```python exec
id: a-model-that-starts-out-wrong-1
hint: With every weight at zero, the total is just the bias, whatever picture goes in.
```

<details class="dl-answer"><summary>answer</summary>

Both return `1`, which means "plus", for both pictures. With every
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
changes. It turns a `1` or a `0` into a word a person would say.

</details>

## Running it again and again

**3.** The tutorial's training loop uses the examples in `train` in the
order they are written.

1. Reverse that order with `list(reversed(train))`.
2. Train a new model from the start, with every weight at zero.
3. Compare the final weights with the tutorial's. Are they the same?

```python exec
id: running-it-again-and-again-1
hint: fit(list(reversed(train))) trains a new model on the reversed list. Print its weights and bias beside weights and bias.
```

<details class="dl-answer"><summary>answer</summary>

No. Both get every training example right in the end, but they end with
different weights.

| pixel | tutorial's order | reversed order |
|---|---|---|
| top-left | `-2.0` | `-1.0` |
| top-middle | `+0.5` | `+1.0` |
| top-right | `-1.5` | `-2.0` |
| mid-left | `+1.0` | `+1.5` |
| mid-right | `+2.5` | `+2.0` |
| bottom-left | `-1.5` | `-1.0` |
| bottom-middle | `+1.5` | `+1.0` |
| bottom-right | `-1.0` | `-2.0` |

The centre, `+0.5`, and the bias, `+0.5`, are the same in both. Every
arm of the plus is still positive, and every corner of the cross is
still negative. Only the sizes changed.

There is no single correct set of weights here. There are only sets that
get every training example right. The set the training finds depends on
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

It still takes seven epochs, with the same dip in the sixth. Every
weight is four times as large as with `0.5`: `+10.0` in place of
`+2.5`, and `-8.0` in place of `-2.0`.

This is the same thing the tutorial found with `0.05`. Every weight
starts at zero, and every change is multiplied by the learning rate. So
changing the learning rate scales every weight and the bias by the same
amount. That never changes whether a total is above zero, so every
decision stays the same, and so does the number of epochs.

In bigger models, the weights do not all start at zero. There, the
learning rate matters much more. A rate that is too small can take a
very long time, and one that is too large can jump past good weights.

</details>

## Checking it against patterns it has never seen

**5.** Use the tutorial's final `weights` and `bias`. Call `predict` on
the *original* `PLUS` and `CROSS`, with no pixels flipped. These two
pictures are in neither `train` nor `test`. What do you expect, before
you run it?

```python exec
id: checking-it-against-patterns-it-has-never-seen-1
hint: Every training example was PLUS or CROSS with three pixels flipped. So the clean originals are, in a way, the easiest possible test.
```

<details class="dl-answer"><summary>answer</summary>

Both are correct: `1` for `PLUS`, and `0` for `CROSS`. The totals are
far from zero, $+6.5$ and $-5.0$. Every example in `train` was three
flipped pixels away from one of these two pictures. So the clean
pictures are closer to what the model learned than any of the examples
it was corrected against.

</details>

**6.** What does the model predict for a picture that is all zeros, with
no pixels lit at all? Do the arithmetic by hand first.

```python exec
id: checking-it-against-patterns-it-has-never-seen-2
hint: Every weight gets multiplied by 0. What is left in the total?
```

<details class="dl-answer"><summary>answer</summary>

It predicts `1`, "plus". Every term is `weight * 0`, so the
total is only the bias, which is `+0.5`. The rule is
`1 if total > 0 else 0`, and `0.5` is greater than `0`. For a blank
picture, the bias alone decides the answer. No weight plays any part.

A blank picture is neither shape, and the model has no way to say so. It
can only ever answer "plus" or "cross".

</details>

## What the model learned

**7.** Imagine a tenth pixel added to every picture. It is always `0`, in
every training example, with no exceptions. What weight would you expect
it to have at the end, and why?

<details class="dl-answer"><summary>answer</summary>

`0.0`. A weight only moves by `learning_rate * error * pixel`. For a
pixel that is always `0`, that change is always zero, so its weight can
never move.

Compare the centre pixel in the tutorial. It could not tell the shapes
apart either, but it was lit in most pictures, so it moved 19 times.
The ups and downs cancelled each other, and that brought it back near
zero. So a pixel can tell the model nothing and still move.

</details>

**8.** In your own words, what is the difference between the *model* and
the *simulation* in this tutorial?

<details class="dl-answer"><summary>answer</summary>

The model is the fixed part: nine weights, one bias, and the rule in
`predict()` that turns a picture into a decision. The simulation runs
that rule over and over, across the training examples. The corrections
from each pass change what the next pass sees.

The difference matters. A new model, with every weight at zero, does
nothing useful on its own. The simulation produces a model that works. It
guesses, checks and corrects, again and again.

</details>
