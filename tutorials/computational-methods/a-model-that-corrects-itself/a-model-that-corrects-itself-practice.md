---
title: "A Model That Corrects Itself — Practice"
slug: a-model-that-corrects-itself-practice
practice_for: a-model-that-corrects-itself
module: computational-methods
module_title: "Computational Methods"
year: "2026-2027"
series: simulation
version: 2026.09.05.1
---

# A Model That Corrects Itself — Practice

Answers are folded. Several of these ask you to predict an output before
running anything. Resist checking first — being wrong and finding out why
is worth more than being right by accident.

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

**1.** Set every weight to `0.0` but the bias to `5.0`, and predict on both
`PLUS` and `CROSS`. What do you expect, and why, before running it?

```python exec
id: a-model-that-starts-out-wrong-1
hint: With every weight at zero, the total is just the bias, whatever picture goes in.
```

<details class="dl-answer"><summary>answer</summary>

Both come back `1` — "plus," for both pictures. With every weight at zero,
`total` is `0 + 5.0` regardless of which pixels are lit, and `5.0 > 0` no
matter what. A bias with no weights behind it is a model that has already
made up its mind before looking at the picture.

</details>

**2.** Write `predict_label()`, a version of `predict()` that returns the
string `"plus"` or `"cross"` instead of `1` or `0`, without changing the
arithmetic.

<details class="dl-answer"><summary>answer</summary>

```python
def predict_label(weights, bias, pixels):
    return "plus" if predict(weights, bias, pixels) == 1 else "cross"
```

The arithmetic stays exactly as `predict()` left it. Only the last step —
turning a `1` or a `0` into a word a person would say — changes.

</details>

## Running It Again and Again

**3.** The tutorial's training loop goes through `train` in the order it is
written. Reverse that order — `list(reversed(train))` — retrain from
scratch, and compare the final weights to the tutorial's. Are they the
same?

```python exec
id: running-it-again-and-again-1
hint: Copy the training loop, but iterate over list(reversed(train)) instead of train. Print the final weights and bias from both runs side by side.
```

<details class="dl-answer"><summary>answer</summary>

No — both reach 100% train accuracy by the second epoch, but land on
different weights. The forward order gives `top-right` and `mid-right`
both `0.0`; reversed, `top-right` ends at `-0.5` and `mid-right` at
`+0.5`, with `bottom-right` now `0.0` instead.

There is no single correct set of weights here, only sets that happen to
get every training example right. Which one training lands on depends on
which mistakes happened to come first.

</details>

**4.** Would you expect a *larger* learning rate than `0.5` to reach 100%
train accuracy in fewer epochs, the same number, or more? Try `2.0` and
check.

```python exec
id: running-it-again-and-again-2
hint: A bigger learning_rate makes each correction bigger too — but "bigger correction" is not automatically "better correction" once a mistake is already fixable in one step.
```

<details class="dl-answer"><summary>answer</summary>

Still two epochs here — a correction big enough to fix a mistake in one
step does not get any more effective by being made even bigger. The
tutorial's own comparison (`0.5` against `0.05`) showed the opposite
effect, a *smaller* rate taking more epochs to arrive at the same place.
Both are real: there is a rate too small to be efficient, and a point past
which going bigger stops helping, without necessarily hurting either.

</details>

## Checking It Against Patterns It Has Never Seen

**5.** Using the tutorial's own final `weights` and `bias`, predict on the
*original*, noise-free `PLUS` and `CROSS` — patterns that appear in neither
`train` nor `test`. Predict the result before running it.

```python exec
id: checking-it-against-patterns-it-has-never-seen-1
hint: Every training example was PLUS or CROSS with one pixel flipped; the clean originals are, in a sense, the easiest possible test.
```

<details class="dl-answer"><summary>answer</summary>

Both correct: `1` for `PLUS`, `0` for `CROSS`. Every noisy example in
`train` was one pixel-flip away from one of these two pictures, so the
clean originals sit closer to what the model learned than any of the
noisy examples it was actually corrected against.

</details>

**6.** What does the model predict for a picture that is all zeros — no
pixels lit at all? Work out the arithmetic by hand first.

```python exec
id: checking-it-against-patterns-it-has-never-seen-2
hint: Every weight gets multiplied by 0. What is left in the total?
```

<details class="dl-answer"><summary>answer</summary>

`0`, "cross" — and it is worth seeing exactly why. Every weighted term is
`weight * 0`, so the whole sum collapses to just the bias, which is
`0.0`. The rule is `1 if total > 0 else 0`, and `0` is not greater than
`0`, so the tie goes to "cross." A blank picture is the one input where
the bias alone, not any weight, decides the answer.

</details>

## What the Model Actually Learned

**7.** Imagine a tenth pixel added to every picture — a padding pixel that
is always `0`, in every training example, with no exceptions. What weight
would you expect it to end up with, and why?

<details class="dl-answer"><summary>answer</summary>

`0.0`. A pixel that never varies carries no information a weight could
use to separate the two classes, the same reasoning the tutorial gave for
the shared centre pixel. Training only moves a weight when a mistake
needs correcting, and a pixel that is always `0` can never be the reason
a prediction came out wrong.

</details>

**8.** In your own words: what is the difference between the *model* and
the *simulation* in this tutorial?

<details class="dl-answer"><summary>answer</summary>

The model is the fixed part: nine weights, one bias, and the rule in
`predict()` for turning a picture into a decision. The simulation is
running that rule over and over across the training examples, letting
each pass's corrections change what the next pass sees.

The distinction matters because the model on its own — freshly created,
every weight at zero — does nothing useful. What actually produces a
working classifier is the simulation: the repeated process of guessing,
checking, and correcting, not any one weighted sum by itself.

</details>
