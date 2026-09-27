---
title: "The perceptron: a model that learns from its mistakes — Practice"
practice_for: a-model-that-corrects-itself
year: "2026-2027"
version: 2026.09.27.1
worlds:
  living-systems: Tracks in the snow, a bird's footprint or a fox's pawprint.
  queues-and-crowds: People seen from above, in a row at a counter or in a single-file queue.
  spread: A disease on a map, along a road or out in four directions from a town.
  space-and-physics: Meteor streaks on a camera, falling to the left or to the right.
---

# The perceptron: a model that learns from its mistakes — Practice

Each answer is hidden until you open it. Write something down first,
even a guess, and then open the answer to compare.

The cell below creates everything the problems use: the two shapes,
`predict()`, the tutorial's twenty messy pictures in `train`, and a
function `fit()` that runs the tutorial's training loop. Its last line
trains the same model the tutorial did.

```python exec
id: setup-1
import random
from itertools import combinations

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

**1.** Every weight is `0.0`, and the bias is `5.0`.

```python exec
id: a-model-that-starts-out-wrong-1
print(predict([0.0] * 9, 5.0, PLUS), predict([0.0] * 9, 5.0, CROSS))
```

```predict
type: choice

What will the cell print?

- 1 1
- 1 0
  - The model knows which picture is which.
- 0 0
```

<details class="dl-answer"><summary>why</summary>

Both are `1`, "plus". With every weight at zero, `total` is `0 + 5.0`,
whichever pixels are lit, and `5.0 > 0` is always true. A model with a
bias and no weights has made its decision before it looks at the
picture.

</details>

**2.** Can you write `predict_label()`, a version of `predict()` that
returns the word `"plus"` or `"cross"` instead of `1` or `0`, without
changing the arithmetic?

```python exec
id: a-model-that-starts-out-wrong-2
def predict_label(weights, bias, pixels):
    """ "plus" or "cross", by the same arithmetic as predict()."""
    # Your code here.
```

```hint
Call `predict()` and turn its answer into a word.
```

```inputs
predict_label(weights, bias, PLUS)
predict_label(weights, bias, CROSS)
predict_label([0.0] * 9, 5.0, CROSS)
```

```solution
def predict_label(weights, bias, pixels):
    """ "plus" or "cross", by the same arithmetic as predict()."""
    return "plus" if predict(weights, bias, pixels) == 1 else "cross"
---
The trained model names both clean shapes correctly. The model with a
bias of 5 and no weights calls the cross "plus", as problem 1 found.
Only the last step changed: a `1` or a `0` became a word a person would
say.
```

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

**5.** Can you write `accuracy(weights, bias, examples)`? It returns the
share of the examples, each a `(pixels, label)` pair, that the model
gets right.

```python exec
id: running-it-again-and-again-3
def accuracy(weights, bias, examples):
    """The share of (pixels, label) pairs the model gets right."""
    # Your code here.
```

```hint
Count the pairs where `predict(weights, bias, pixels) == label`, and
divide by `len(examples)`.
```

```inputs
accuracy(weights, bias, train)
accuracy([0.0] * 9, 0.0, train)
accuracy(weights, bias, [(PLUS, 1), (CROSS, 0)])
```

```solution
def accuracy(weights, bias, examples):
    """The share of (pixels, label) pairs the model gets right."""
    right = sum(1 for pixels, label in examples if predict(weights, bias, pixels) == label)
    return right / len(examples)
---
The trained model gets all of `train` right. The untrained one, with
every weight and the bias at zero, gets exactly half: it calls every
picture "cross", and half the pictures are crosses. A model that knows
nothing can still look half right, which is why a score means little
until you know what guessing would get.
```

## Checking it against patterns it has never seen

**6.** The two clean pictures, `PLUS` and `CROSS`, with no pixels
flipped, are in neither `train` nor the tutorial's `test`. What does the
trained model say about them?

```python exec
id: checking-it-against-patterns-it-has-never-seen-1
print(predict(weights, bias, PLUS), predict(weights, bias, CROSS))
```

```predict
type: choice

What will the cell print?

- 1 0
- 0 1
- 1 1
  - The model never saw a clean picture.
```

<details class="dl-answer"><summary>why</summary>

It prints `1 0`: both right. The totals are far from zero, $+6.5$ and
$-5.0$. Every example in `train` was three flipped pixels away from one
of these two pictures, so the clean pictures are closer to what the
model learned than any example it was corrected against.

</details>

**7.** What does the model predict for a picture that is all zeros, with
no pixels lit at all? Do the arithmetic by hand first.

```python exec
id: checking-it-against-patterns-it-has-never-seen-2
print(predict(weights, bias, [0] * 9))
```

```predict
type: number

What will the cell print?
```

<details class="dl-answer"><summary>why</summary>

It prints `1`, "plus". Every term is `weight * 0`, so the total is only
the bias, `+0.5`, which is greater than `0`. For a blank picture, the
bias alone decides. A blank picture is neither shape, and the model has
no way to say so: it can only ever answer "plus" or "cross".

</details>

## What the model learned

**8.** Imagine a tenth pixel added to every picture. It is always `0`, in
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

**9.** In your own words, what is the difference between the *model*
and the *training* in this tutorial?

<details class="dl-answer"><summary>answer</summary>

The model is the fixed part: nine weights, one bias, and the rule in
`predict()` that turns a picture into a decision. The training runs
that rule over and over, across the examples, and corrects the weights
after each mistake.

A new model, with every weight at zero, does nothing useful on its own.
The training produces a model that works. After that, the training is
finished, and the model is used on its own, on pictures it never saw.

</details>

## Your world

**10.** Some messy pictures could have come from either shape. Can you
write `could_be_both(shape_a, shape_b, flips)`? It returns how many
pictures can be made from *both* shapes by flipping exactly `flips`
pixels.

<div class="dl-world" data-world="living-systems">

```python exec
id: your-world-1--living-systems
BIRD = [1, 0, 1,
        0, 1, 0,
        0, 1, 0]    # a bird's footprint

FOX = [1, 0, 1,
       0, 0, 0,
       1, 0, 1]    # a fox's pawprint


def could_be_both(shape_a, shape_b, flips):
    """How many pictures both shapes can become, with this many pixels flipped."""
    # Your code here.
```

```hint
Make a set of every picture one shape can become:
`combinations(range(9), flips)` gives every choice of pixels to flip.
Store each picture as a `tuple`, because a list cannot go in a set. Do
the same for the other shape, and count what the two sets share with
`&`.
```

```inputs
could_be_both(BIRD, FOX, 1)
could_be_both(BIRD, FOX, 2)
could_be_both(PLUS, CROSS, 3)
```

```solution
def could_be_both(shape_a, shape_b, flips):
    """How many pictures both shapes can become, with this many pixels flipped."""
    def made_from(shape):
        pictures = set()
        for spots in combinations(range(9), flips):
            pixels = list(shape)
            for i in spots:
                pixels[i] = 1 - pixels[i]
            pictures.add(tuple(pixels))
        return pictures
    return len(made_from(shape_a) & made_from(shape_b))
---
With one flip, no picture could be either track. With two, 6 pictures could: the tracks differ in 4 pixels, and two flips from each can meet in the middle. The tutorial's plus and cross differ in 8 pixels, so even three flips from each never meet. Every mistake the tutorial's model made was its own.
```

</div>

<div class="dl-world" data-world="queues-and-crowds">

```python exec
id: your-world-1--queues-and-crowds
ROW = [0, 0, 0,
       1, 1, 1,
       0, 0, 0]    # people in a row

QUEUE = [0, 1, 0,
         0, 1, 0,
         0, 1, 0]    # a single-file queue


def could_be_both(shape_a, shape_b, flips):
    """How many pictures both shapes can become, with this many pixels flipped."""
    # Your code here.
```

```hint
Make a set of every picture one shape can become:
`combinations(range(9), flips)` gives every choice of pixels to flip.
Store each picture as a `tuple`, because a list cannot go in a set. Do
the same for the other shape, and count what the two sets share with
`&`.
```

```inputs
could_be_both(ROW, QUEUE, 1)
could_be_both(ROW, QUEUE, 2)
could_be_both(PLUS, CROSS, 3)
```

```solution
def could_be_both(shape_a, shape_b, flips):
    """How many pictures both shapes can become, with this many pixels flipped."""
    def made_from(shape):
        pictures = set()
        for spots in combinations(range(9), flips):
            pixels = list(shape)
            for i in spots:
                pixels[i] = 1 - pixels[i]
            pictures.add(tuple(pixels))
        return pictures
    return len(made_from(shape_a) & made_from(shape_b))
---
With one flip, no picture could be either. With two, 6 pictures could: the row and the queue differ in 4 pixels, and two flips from each can meet in the middle. That is how the same picture ended up in the tutorial's world task twice, with both labels. The plus and the cross differ in 8 pixels, so three flips from each never meet.
```

</div>

<div class="dl-world" data-world="spread">

```python exec
id: your-world-1--spread
ROAD = [0, 0, 0,
        1, 1, 1,
        0, 0, 0]    # along a road

FOUR_WAYS = [0, 1, 0,
             1, 1, 1,
             0, 1, 0]    # in four directions


def could_be_both(shape_a, shape_b, flips):
    """How many pictures both shapes can become, with this many pixels flipped."""
    # Your code here.
```

```hint
Make a set of every picture one shape can become:
`combinations(range(9), flips)` gives every choice of pixels to flip.
Store each picture as a `tuple`, because a list cannot go in a set. Do
the same for the other shape, and count what the two sets share with
`&`.
```

```inputs
could_be_both(ROAD, FOUR_WAYS, 1)
could_be_both(ROAD, FOUR_WAYS, 2)
could_be_both(PLUS, CROSS, 3)
```

```solution
def could_be_both(shape_a, shape_b, flips):
    """How many pictures both shapes can become, with this many pixels flipped."""
    def made_from(shape):
        pictures = set()
        for spots in combinations(range(9), flips):
            pixels = list(shape)
            for i in spots:
                pixels[i] = 1 - pixels[i]
            pictures.add(tuple(pixels))
        return pictures
    return len(made_from(shape_a) & made_from(shape_b))
---
Even one flip makes 2 pictures that could be either: the two shapes differ in only 2 pixels. With two flips, 14 pictures could be either, and two flips can turn either shape into the other exactly. That is why the model scored only 29 of 45 on this pair. The plus and the cross differ in 8 pixels, so three flips from each never meet.
```

</div>

<div class="dl-world" data-world="space-and-physics">

```python exec
id: your-world-1--space-and-physics
LEFT = [1, 0, 0,
        0, 1, 0,
        0, 0, 1]    # a streak falling to the left

RIGHT = [0, 0, 1,
         0, 1, 0,
         1, 0, 0]    # a streak falling to the right


def could_be_both(shape_a, shape_b, flips):
    """How many pictures both shapes can become, with this many pixels flipped."""
    # Your code here.
```

```hint
Make a set of every picture one shape can become:
`combinations(range(9), flips)` gives every choice of pixels to flip.
Store each picture as a `tuple`, because a list cannot go in a set. Do
the same for the other shape, and count what the two sets share with
`&`.
```

```inputs
could_be_both(LEFT, RIGHT, 1)
could_be_both(LEFT, RIGHT, 2)
could_be_both(PLUS, CROSS, 3)
```

```solution
def could_be_both(shape_a, shape_b, flips):
    """How many pictures both shapes can become, with this many pixels flipped."""
    def made_from(shape):
        pictures = set()
        for spots in combinations(range(9), flips):
            pixels = list(shape)
            for i in spots:
                pixels[i] = 1 - pixels[i]
            pictures.add(tuple(pixels))
        return pictures
    return len(made_from(shape_a) & made_from(shape_b))
---
With one flip, no picture could be either streak. With two, 6 pictures could: the streaks share the centre and differ in the 4 corners, so two flips from each can meet in the middle. The plus and the cross differ in 8 pixels, so three flips from each never meet.
```

</div>

## From earlier

**11.** From [Matrix multiplication: rows times
columns](tutorial:multiplying-grids). `predict()` starts with a dot
product: each pair multiplied, then added up.

```python exec
id: from-earlier-1
print(sum(w * p for w, p in zip([0.5, -1.0, 2.0], [1, 1, 0])))
```

```predict
type: number

What will the cell print?
```

<details class="dl-answer"><summary>why</summary>

It prints `-0.5`: $0.5 \times 1 + (-1.0) \times 1 + 2.0 \times 0$. The
third weight is large, but its pixel is off, so it adds nothing. A
weight only counts when its pixel is lit.

</details>
