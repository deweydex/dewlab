---
title: "A Model That Corrects Itself"
slug: a-model-that-corrects-itself
module: computational-methods
module_title: "Computational Methods"
year: "2026-2027"
series: simulation
version: 2026.09.05.1
covers:
  a-model-that-starts-out-wrong:
    covers: [CMPS-LO7]
  running-it-again-and-again:
    covers: [CMPS-LO7]
    touches: [CMPS-LO11]
  checking-it-against-patterns-it-has-never-seen:
    covers: [CMPS-LO11]
  what-the-model-actually-learned:
    covers: [CMPS-LO7]
---

# A Model That Corrects Itself

Every model built so far in this module has been a fixed formula. Feed it
numbers, and it gives back the same answer every time — a matrix
transformation, a π estimate, a system of equations solved. This tutorial
builds a different kind of model: one that starts out wrong on purpose. It
changes its own numbers based on what it gets wrong. It is the same idea
behind every neural network, shown at the smallest scale that still works.

## A Model That Starts Out Wrong

The task: tell a plus sign apart from a cross, drawn as a tiny 3×3 grid of
black and white pixels.

```python exec
id: a-model-that-starts-out-wrong-1
import matplotlib.pyplot as plt

PLUS = [0, 1, 0,
        1, 1, 1,
        0, 1, 0]

CROSS = [1, 0, 1,
         0, 1, 0,
         1, 0, 1]

fig, axes = plt.subplots(1, 2)
axes[0].imshow([PLUS[0:3], PLUS[3:6], PLUS[6:9]], cmap="gray_r")
axes[0].set_title("PLUS")
axes[1].imshow([CROSS[0:3], CROSS[3:6], CROSS[6:9]], cmap="gray_r")
axes[1].set_title("CROSS")
for axis in axes:
    axis.set_xticks([])
    axis.set_yticks([])
```

Each grid is really just a list of nine numbers — `PLUS` and `CROSS` above,
one entry per pixel. The *model* is a rule for turning those nine numbers
into a single decision. Multiply each pixel by a *weight* of its own. Add
them up, along with one extra number called a *bias*. Decide "plus" if the
total comes out above zero.

```python exec
id: a-model-that-starts-out-wrong-2
def predict(weights, bias, pixels):
    """1 means "plus", 0 means "cross"."""
    total = sum(w * p for w, p in zip(weights, pixels)) + bias
    return 1 if total > 0 else 0


weights = [0.0] * 9
bias = 0.0

print(predict(weights, bias, PLUS))
print(predict(weights, bias, CROSS))
```

Both come back `0`. With every weight at zero, the total is always zero
too, whatever picture goes in — the model has not looked at a single pixel
yet. It calls `CROSS` correctly by accident, and `PLUS` wrong. Guessing the
same answer every time is right exactly as often as that answer happens
to be true.

This is the whole model: nine weights, one bias, and the rule above. Nothing
about it changes what a weight or a bias *is* — they are still just numbers,
the same as any other variable in this module. What makes this one different
is what happens next.

### Your turn

Try setting `weights[1]` (the top-middle pixel) to `1.0` by hand, leaving
everything else at zero, then run `predict()` on both patterns again.
Which one flips, and why that particular pixel?

```python exec
id: a-model-that-starts-out-wrong-3
hint: PLUS has a 1 in the top-middle position; CROSS has a 0 there. A weight of 1.0 on that one pixel is enough to push the total for PLUS above zero without moving CROSS's total at all.
```

## Running It Again and Again

A model this small cannot be solved for the right weights on paper the way
`solving-systems` solved for exact unknowns. Instead, it is corrected one
mistake at a time. Show it a picture, and check whether its guess matches
the true label. If not, nudge every weight a little in the direction that
would have helped — the size of "a little" set by one number, the
*learning rate*.

```python exec
id: running-it-again-and-again-1
# A handful of noisy examples: each is PLUS or CROSS with one pixel flipped,
# so the model never sees the same picture twice. 1 = plus, 0 = cross.
train = [
    ([0, 1, 0, 1, 1, 0, 0, 1, 0], 1),
    ([1, 0, 0, 0, 1, 0, 1, 0, 1], 0),
    ([0, 1, 0, 1, 1, 1, 1, 1, 0], 1),
    ([0, 0, 1, 0, 1, 0, 1, 0, 1], 0),
    ([0, 0, 0, 1, 1, 1, 0, 1, 0], 1),
    ([1, 0, 1, 0, 1, 0, 1, 0, 0], 0),
    ([0, 0, 0, 1, 1, 1, 0, 1, 0], 1),
    ([1, 0, 1, 0, 1, 1, 1, 0, 1], 0),
    ([1, 1, 0, 1, 1, 1, 0, 1, 0], 1),
    ([1, 0, 1, 0, 1, 0, 1, 0, 0], 0),
    ([0, 1, 0, 0, 1, 1, 0, 1, 0], 1),
    ([0, 0, 1, 0, 1, 0, 1, 0, 1], 0),
]

weights = [0.0] * 9
bias = 0.0
learning_rate = 0.5

for epoch in range(1, 9):
    correct = 0
    for pixels, label in train:
        guess = predict(weights, bias, pixels)
        error = label - guess
        if error != 0:
            for i in range(9):
                weights[i] += learning_rate * error * pixels[i]
            bias += learning_rate * error
        else:
            correct += 1
    print(f"epoch {epoch}: train accuracy = {correct / len(train):.2f}")
```

One pass through all twelve examples is an *epoch*. The first one gets ten
out of twelve right. That is already better than guessing, since a few
mistakes have already nudged the weights toward the pixels that matter. By
the second epoch it gets all twelve. Every epoch after that changes
nothing: once every example in `train` is already correct, `error` is zero
every time, and nothing gets nudged.

This loop is the *simulation*. The model itself is nine numbers and a rule.
Running that rule over and over, letting each pass change what the next
pass sees, is what turns a fixed formula into something that behaves like
learning.

### Your turn

Try changing `learning_rate` from `0.5` to `0.05`, then run the training
loop again. Does it still reach 100% train accuracy? Does it take more
epochs, fewer, or about the same?

```python exec
id: running-it-again-and-again-2
hint: A smaller learning_rate means each mistake nudges the weights by less, so getting to the same place takes smaller, more numerous steps.
```

## Checking It Against Patterns It Has Never Seen

100% on `train` proves the model fits the twelve examples it was corrected
against. It does not yet prove the model has found anything general about
plus signs and crosses — it could just as easily have memorised those
twelve pictures individually. Telling the two apart needs a second set of
examples the training loop never touched.

```python exec
id: checking-it-against-patterns-it-has-never-seen-1
test = [
    ([0, 1, 0, 1, 1, 1, 1, 1, 0], 1),
    ([1, 0, 1, 0, 1, 0, 0, 0, 1], 0),
    ([0, 1, 0, 0, 1, 1, 0, 1, 0], 1),
    ([1, 0, 0, 0, 1, 0, 1, 0, 1], 0),
    ([0, 1, 0, 0, 1, 1, 0, 1, 0], 1),
    ([1, 0, 1, 1, 1, 0, 1, 0, 1], 0),
]

test_correct = sum(1 for pixels, label in test if predict(weights, bias, pixels) == label)
print(f"test accuracy = {test_correct / len(test):.2f}")
```

All six come back correct, each on a picture with its own pixel flipped
differently from anything in `train`. The real check is whether the
model's behaviour still matches the real pattern, on cases it never saw
while correcting itself. Fitting the training data alone is not enough. A
model that only passed that first check would be worth nothing outside
the exact examples used to build it.

### Your turn

Add one more test example of your own: a `PLUS` or `CROSS` with a
different pixel flipped from any used above. Check whether the model
still gets it right.

```python exec
id: checking-it-against-patterns-it-has-never-seen-2
hint: Copy PLUS or CROSS, flip exactly one entry, and pass it to predict(weights, bias, ...) along with the label you'd expect. Getting one wrong is a real, useful result here too — not every possible flip has to work.
```

## What the Model Actually Learned

The weights are not a mystery. They can be read directly.

```python exec
id: what-the-model-actually-learned-1
labels = [
    "top-left", "top-middle", "top-right",
    "mid-left", "center", "mid-right",
    "bottom-left", "bottom-middle", "bottom-right",
]
for name, w in zip(labels, weights):
    print(f"{name:>13}: {w:+.2f}")
print(f"{'bias':>13}: {bias:+.2f}")
```

Three of `PLUS`'s four unique pixels ended up with a positive weight:
top-middle, mid-left, and bottom-middle, each pulling the total up when
lit. Three of `CROSS`'s four unique pixels ended up negative: top-left,
bottom-left, and bottom-right, each pulling the total down when lit. The
centre is on in every example of both shapes, so it sits at zero. It
carries no information about which one a picture is, and the model never
had a reason to move it.

Two pixels, mid-right and top-right, also sit at zero, and neither is
shared between the shapes the way the centre is. That is not a mistake.
Training only nudges a weight when a mistake needs correcting. The twelve
examples in `train` never happened to need those two moved, because the
other weights already carried enough signal to get every one of them
right. A model only learns what the data in front of it actually forces
it to learn, not everything a person looking at the pictures would notice.

The rule in `predict()` never says a positive number means "plus" and a
negative one means "cross." That correspondence came entirely from being
corrected against examples, twelve mistakes at a time. A far larger
version of exactly this model is most of what a real handwriting-
recognition network is. The only real difference: it is corrected
against tens of thousands of handwritten digits, not twelve plus signs
and crosses.

## Where to Read More

Rosenblatt, F. (1958). *The Perceptron: A Probabilistic Model for
Information Storage and Organization in the Brain.* Psychological Review,
65(6), 386–408. The original paper — this tutorial's `predict()` and
training loop are a direct, unsimplified descendant of the "perceptron"
described here, sixty-odd years before this course.

Nielsen, M. (2015). *Neural Networks and Deep Learning*.
<http://neuralnetworksanddeeplearning.com/>. Free online book. Chapter 1
builds up from exactly this kind of small, hand-checkable example toward a
real handwritten-digit classifier, without skipping the arithmetic in
between.
