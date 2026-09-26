---
title: "The perceptron: a model that learns from its mistakes"
year: "2026-2027"
version: 2026.09.25.1
covers:
  a-model-that-starts-out-wrong:
    covers: [CMPS-LO7]
  running-it-again-and-again:
    covers: [CMPS-LO7]
    touches: [CMPS-LO11]
  checking-it-against-patterns-it-has-never-seen:
    covers: [CMPS-LO11]
  what-the-model-learned:
    covers: [CMPS-LO7]
---

# The perceptron: a model that learns from its mistakes

So far in this module, every model has been a fixed formula. A matrix
transformation, a system of equations, even the π estimate once its seed
is set: give each one the same numbers, and it gives back the same answer
every time.

On this page we build a different kind of model. It starts out wrong on
purpose. Then it changes its own numbers, based on the mistakes it makes.
This model is called a *perceptron*. A perceptron is the smallest model
that learns from its mistakes, and every neural network is built on the
same idea.

## A Model That Starts Out Wrong

Here is the task. We want the model to tell a plus sign from a cross.
Each one is drawn on a tiny grid of 3 by 3 pixels, and each pixel is
black or white.

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

Each picture is a list of nine numbers, one for each pixel: `PLUS` and
`CROSS` above. A 1 is a black pixel, and a 0 is a white one.

A *model* is a rule for turning some numbers into a decision. Our model
turns those nine numbers into one decision, in three steps:

1. Multiply each pixel by a number of its own, called its *weight*.
2. Add up all nine results. Then add one more number, called the *bias*.
3. If the total is above zero, decide "plus". Otherwise, decide "cross".

In the code, `predict()` does those three steps. `zip(weights, pixels)`
pairs each weight with its pixel, as in
[Comprehensions, grids and aliasing](tutorial:comprehensions-and-grids).
The last line returns 1 if the total is above zero, and 0 if it is not.

What do you think the model will say for each picture, with every weight
at zero?

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
too, whatever picture goes in. The model has not looked at a single pixel
yet. It calls `CROSS` correctly, by accident, and it calls `PLUS` wrongly.
A model that always gives the same answer is right only when that answer
happens to be true.

That is the whole model: nine weights, one bias, and the rule above. A
weight and a bias are ordinary numbers, like any other variable in this
module. What makes this model different is what happens next.

### Your turn

1. Set `weights[1]` (the top-middle pixel) to `1.0` by hand. Leave
   everything else at zero.
2. Run `predict()` on both pictures again.
3. Which picture's answer changes? Why that pixel?

```python exec
id: a-model-that-starts-out-wrong-3
hint: PLUS has a 1 in the top-middle position; CROSS has a 0 there. A weight of 1.0 on that one pixel is enough to push the total for PLUS above zero without moving CROSS's total at all.
```

## Running It Again and Again

We cannot work out the right weights on paper, the way
[Systems of equations: solving them with matrices](tutorial:solving-systems) found exact unknowns.
Instead, we correct the model one mistake at a time:

1. Show it a picture.
2. Check whether its guess matches the true label.
3. If the guess is wrong, move every weight a little, in the direction
   that would have helped.

The size of "a little" is set by one number, called the *learning rate*.

First we need pictures to learn from. Real pictures are messy, so ours
are too. `noisy()` takes a clean picture and flips three of its nine
pixels, chosen at random: black to white, or white to black. The cell
makes ten messy plus signs and ten messy crosses, and shuffles them.

```python exec
id: running-it-again-and-again-1
import random

random.seed(1)    # the same twenty pictures every time the cell runs


def noisy(picture, flips):
    """A copy of picture with `flips` different pixels switched."""
    copy = list(picture)
    for i in random.sample(range(9), flips):
        copy[i] = 1 - copy[i]
    return copy


train = []    # pairs of (pixels, label): 1 = plus, 0 = cross
for _ in range(10):
    train.append((noisy(PLUS, 3), 1))
    train.append((noisy(CROSS, 3), 0))
random.shuffle(train)

print(train[0])
print(train[1])
```

Now the correcting. Look at the inner `if` in the code below. `error` is
`label - guess`. It is 1 when the model said "cross" for a plus, and -1
when it said "plus" for a cross. So each lit pixel's weight moves up for
a missed plus, and down for a missed cross.

```python exec
id: running-it-again-and-again-2
weights = [0.0] * 9
bias = 0.0
learning_rate = 0.5
accuracy = []    # the share of train it got right, in each epoch

for epoch in range(1, 11):
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
    accuracy.append(correct / len(train))

print(accuracy)
plt.figure()
plt.plot(range(1, 11), accuracy, marker="o")
plt.ylim(0, 1.05)
plt.xlabel("epoch")
plt.ylabel("share of train right")
plt.title("Learning, one pass at a time")
```

One pass through all twenty examples is called an *epoch*. In the first
epoch, the model gets 12 of the 20 right. Each mistake nudges the
weights, and by the fifth epoch it gets 19 right. Then, in the sixth, it
gets one *more* wrong: a correction that fixed one picture broke
another. From the seventh epoch on, it gets all twenty right. Along the
way it made 21 corrections.

After that, every epoch changes nothing. Every example in `train` is
already correct, so `error` is zero every time, and no weight moves.

This loop is the *simulation*. A simulation runs a model again and
again, and lets each run change what the next run sees. The model itself
is nine numbers and a rule. Running that rule over and over, and letting
each pass change the next one, turns a fixed formula into something that
behaves like learning.

### Your turn

What do you think happens with a much smaller learning rate?

1. Change `learning_rate` from `0.5` to `0.05`.
2. Run the training loop again.
3. Does it still reach 100% train accuracy? Does it take more epochs,
   fewer, or the same number?
4. Print `weights`. How are they different from before?

```python exec
id: running-it-again-and-again-3
hint: Copy the training loop into this cell and change the learning_rate line. After the loop, print(weights) and compare the numbers with the tutorial's.
```

Many people expect a smaller learning rate to need more epochs. Here it
does not. It takes the same seven epochs, with the same dip in the
sixth, and every weight ends up exactly ten times smaller. Why?

Every weight starts at zero, and every change is multiplied by the
learning rate. So a smaller learning rate shrinks every weight by the
same amount, and the bias too. Shrinking every number in the total by
the same amount never changes whether the total is above zero. So every
decision stays the same.

In bigger models, the weights do not all start at zero, and then the
learning rate matters much more. In this model, it only changes the size
of the numbers.

## Checking It Against Patterns It Has Never Seen

The model scores 100% on `train`. That shows it fits the twenty examples
we corrected it with. But has it found anything general about plus signs
and crosses? Or has it only memorised those twenty pictures, one by one?

To tell the difference, we need a second set of examples. The training
loop must never have seen them. We call these the *test* examples.

There are only so many ways to flip three of nine pixels: 84 for each
shape. `combinations(range(9), 3)` gives every one of them, as three
positions at a time. The cell keeps every messy picture that is not in
`train`, and asks the model about each one.

```python exec
id: checking-it-against-patterns-it-has-never-seen-1
from itertools import combinations

seen = [pixels for pixels, label in train]
test = []
for shape, label in [(PLUS, 1), (CROSS, 0)]:
    for spots in combinations(range(9), 3):
        pixels = list(shape)
        for i in spots:
            pixels[i] = 1 - pixels[i]
        if pixels not in seen:
            test.append((pixels, label))

test_correct = sum(1 for pixels, label in test if predict(weights, bias, pixels) == label)
print(len(test), "pictures it never saw")
print(test_correct, "of them right:", f"{test_correct / len(test):.2f}")
```

The model gets 141 of the 149 right. That is 95%, not 100%. On the
twenty pictures it was corrected against, it makes no mistakes. On
pictures it never saw, it gets about one in twenty wrong.

That gap is normal, and it is the number that matters. Does the model
still behave like the real pattern, on cases it never saw while it was
learning? Fitting the training examples alone is not enough. A model
that passed only that first check could still be useless outside the
examples we built it with.

### Your turn

1. Which eight pictures does the model get wrong? List them with
   `[pixels for pixels, label in test if predict(weights, bias, pixels) != label]`.
2. Draw one or two of them on paper as a 3 by 3 grid. Would you have
   known which shape it was meant to be?

```python exec
id: checking-it-against-patterns-it-has-never-seen-2
hint: Each picture is nine numbers, read in rows of three. After three flips, some pictures are hard for a person to call too.
```

## What the Model Learned

We can read the weights directly. What do you expect the plus-sign
pixels to look like?

```python exec
id: what-the-model-actually-learned-1
labels = [
    "top-left", "top-middle", "top-right",
    "mid-left", "centre", "mid-right",
    "bottom-left", "bottom-middle", "bottom-right",
]
for name, w in zip(labels, weights):
    print(f"{name:>13}: {w:+.2f}")
print(f"{'bias':>13}: {bias:+.2f}")
```

Each shape has four pixels that the other shape does not have.

- All four of the plus sign's arms ended up with a positive weight:
  top-middle, mid-left, mid-right and bottom-middle. When one of these
  is lit, it pulls the total up, towards "plus".
- All four of the cross's corners ended up with a negative weight. When
  one of these is lit, it pulls the total down, towards "cross".

That is the pattern a person would name. But look at the sizes. Mid-right
is $+2.5$, and top-middle only $+0.5$. Nothing about a plus sign makes
its right arm five times as important as its top. So why the difference?

Training only changes a weight when there is a mistake to correct, and
only for the pixels that were lit in that picture. So the sizes record
which pixels happened to be lit in the pictures the model got wrong.
Top-middle moved 13 times, but 6 of those were pushes down, from messy
crosses that had that pixel switched on. Mid-right was pushed down only
4 times. Shuffle `train` differently, and the sizes come out
differently. A model learns only what the examples in front of it force
it to learn.

The centre is shared by both shapes, so it cannot tell them apart. Yet
its weight moved more often than any other: 19 of the 21 corrections
moved it, because it is lit in most pictures of both shapes. It went up
10 times, after a missed plus, and down 9 times, after a missed cross.
The ups and downs nearly cancelled, and it ended at $+0.5$.

The rule in `predict()` never says "a positive number means plus". It
never says "a negative number means cross". That link came entirely from
being corrected against examples, one mistake at a time.

A real handwriting-recognition network shares that core idea: numbers
that multiply the inputs, adjusted a little after each mistake. But it
is not simply a bigger version of this model. It has many layers of
these units, one feeding the next, and a smoother rule than "above zero
or not". It also needs a way to share out the blame for a mistake among
all those layers. And a single perceptron like ours has a hard limit:
some patterns it cannot learn at all, however many examples it sees.

## Where to Read More

Rosenblatt, F. (1958). *The Perceptron: A Probabilistic Model for
Information Storage and Organization in the Brain.* Psychological Review,
65(6), 386–408. The original paper. The `predict()` rule and the training
loop on this page are a simplified form of the perceptron it describes,
nearly seventy years before this course.

Nielsen, M. (2015). *Neural Networks and Deep Learning*.
<http://neuralnetworksanddeeplearning.com/>. Free online book. Chapter 1
builds up from exactly this kind of small, hand-checkable example toward a
real handwritten-digit classifier, without skipping the arithmetic in
between.
