---
title: "The perceptron: a model that learns from its mistakes"
year: "2026-2027"
version: 2026.09.27.1
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
  your-world:
    touches: [CMPS-LO7, CMPS-LO11]
worlds:
  living-systems: Tracks in the snow, a bird's footprint or a fox's pawprint.
  queues-and-crowds: People seen from above, in a row at a counter or in a single-file queue.
  spread: A disease on a map, along a road or out in four directions from a town.
  space-and-physics: Meteor streaks on a camera, falling to the left or to the right.
---

# The perceptron: a model that learns from its mistakes

So far in this module, every model has been a fixed formula. A matrix
transformation, a system of equations and even the π estimate, once its
seed is set, all return the same answer every time you give them the
same numbers.

On this page we build a different kind of model. It starts out wrong on
purpose. Then it changes its own numbers, based on the mistakes it makes.
This model is called a *perceptron*. A perceptron is the smallest model
that learns from its mistakes, and every neural network is built on the
same idea.

## A model that starts out wrong

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

Each picture is a list of nine numbers, one for each pixel. `PLUS` and
`CROSS` above are two of them. A 1 is a black pixel, and a 0 is a white one.

A *model* is a rule for turning some numbers into a decision. Our model
turns those nine numbers into one decision, in three steps:

1. Multiply each pixel by a number of its own, called its *weight*.
2. Add up all nine results. Then add one more number, called the *bias*.
3. If the total is above zero, decide "plus". Otherwise, decide "cross".

In the code, `predict()` does those three steps. `zip(weights, pixels)`
pairs each weight with its pixel, as in
[Comprehensions, grids and aliasing](tutorial:comprehensions-and-grids).
The last line returns 1 if the total is above zero, and 0 if it is not.

Steps 1 and 2 are the *dot product* from
[Matrix multiplication: rows times columns](tutorial:multiplying-grids).
The weights and the pixels are two lists of the same length, each pair
is multiplied, and the results are added up. So the whole model is one
row of weights, times the picture as a column, plus the bias.

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

Both return `0`. With every weight at zero, the total is always zero
too, whatever picture goes in. The model has not looked at a single pixel
yet. It calls `CROSS` correctly, by accident, and it calls `PLUS` wrongly.

That is the whole model: nine weights, one bias, and the rule above. A
weight and a bias are ordinary numbers, like any other variable in this
module. This model is different because of what happens next.

### Your turn

1. Set `weights[1]` (the top-middle pixel) to `1.0` by hand. Leave
   everything else at zero.
2. Run `predict()` on both pictures again.
3. Which picture's answer changes? Why that pixel?

```python exec
id: a-model-that-starts-out-wrong-3
hint: PLUS has a 1 in the top-middle position; CROSS has a 0 there. A weight of 1.0 on that one pixel is enough to push the total for PLUS above zero without moving CROSS's total at all.
```

## Running it again and again

We cannot find the right weights on paper, the way
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

Now the model corrects itself. Look at the inner `if` in the code below. `error` is
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
gets one *more* wrong. A correction that fixed one picture broke
another. From the seventh epoch on, it gets all twenty right. In total
it made 21 corrections.

After that, every epoch changes nothing. Every example in `train` is
already correct, so `error` is zero every time, and no weight moves.

This loop is called *training*: it fits the model to the examples. It
has something in common with the simulations in this series. It runs
one rule again and again, and lets each pass change the next. But a
simulation's result is a picture of what might happen, such as a queue
or an estimate of π. Training's result is the model itself: nine
weights and a bias that now make good decisions. The model is nine
numbers and a rule. Training is what turns that fixed formula into
something that behaves like learning.

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
sixth, and every weight is exactly ten times smaller at the end. Why?

Every weight starts at zero, and every change is multiplied by the
learning rate. So a smaller learning rate shrinks every weight by the
same amount, and the bias too. When every number in the total shrinks
by the same amount, the total stays on the same side of zero. So every
decision stays the same.

In bigger models, the weights do not all start at zero, and then the
learning rate matters much more. In this model, it only changes the size
of the numbers.

## Checking it against patterns it has never seen

The model scores 100% on `train`. That shows it fits the twenty examples
we corrected it with. But has it found anything general about plus signs
and crosses? Or has it only memorised those twenty pictures, one by one?

To tell the difference, we need a second set of examples. The training
loop must never have seen them. We call these the *test* examples.

There are 84 ways to flip three of nine pixels, for each
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
learning? A good fit to the training examples is not enough. A model
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

## What the model learned

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

- All four of the plus sign's arms have a positive weight at the end:
  top-middle, mid-left, mid-right and bottom-middle. When one of these
  is lit, it pulls the total up, towards "plus".
- All four of the cross's corners have a negative weight at the end. When
  one of these is lit, it pulls the total down, towards "cross".

That is the pattern a person would name. But look at the sizes. Mid-right
is $+2.5$, and top-middle only $+0.5$. Nothing about a plus sign makes
its right arm five times as important as its top. So why are they
different?

Training only changes a weight when there is a mistake to correct, and
only for the pixels that were lit in that picture. So the sizes record
which pixels happened to be lit in the pictures the model got wrong.
Top-middle moved 13 times, but 6 of those were pushes down, from messy
crosses that had that pixel switched on. Mid-right was pushed down only
4 times. Shuffle `train` differently, and the sizes change.

The centre is shared by both shapes, so it cannot tell them apart. Yet
its weight moved more often than any other: 19 of the 21 corrections
moved it, because it is lit in most pictures of both shapes. It went up
10 times, after a missed plus, and down 9 times, after a missed cross.
The ups and downs nearly cancelled, and it ended at $+0.5$.

The rule in `predict()` never says "a positive number means plus". It
never says "a negative number means cross". The model made that link
itself, from its corrections, one mistake at a time.

A real handwriting-recognition network shares that core idea: numbers
that multiply the inputs, adjusted a little after each mistake. But it
is not simply a bigger version of this model. It has many layers of
these units, one feeding the next, and a smoother rule than "above zero
or not". It also needs a way to divide the blame for a mistake among
all those layers. And a single perceptron like ours has a hard limit.
It cannot learn some patterns at all, however many examples it sees.

## Your world

Can the same model learn to tell apart two other shapes? Each world
below has its own pair, and the cell makes twenty messy pictures of
them, with two pixels flipped in each. It also keeps every other
picture with two flips as a test. Can you write
`train_perceptron(examples, learning_rate=0.5, epochs=10)`? It runs the
training loop from this page on `examples`, starting from zero, and
returns the weights and the bias.

<div class="dl-world" data-world="living-systems">

Tracks in fresh snow: a bird's footprint, three toes shaped like a Y, or a fox's pawprint, four pads at the corners.

```python exec
id: your-world-1--living-systems
BIRD = [1, 0, 1,
        0, 1, 0,
        0, 1, 0]    # a bird's footprint: label 1

FOX = [1, 0, 1,
       0, 0, 0,
       1, 0, 1]    # a fox's pawprint: label 0

random.seed(1)
world_train = []
for _ in range(10):
    world_train.append((noisy(BIRD, 2), 1))
    world_train.append((noisy(FOX, 2), 0))
random.shuffle(world_train)

world_seen = [pixels for pixels, label in world_train]
world_test = []
for shape, label in [(BIRD, 1), (FOX, 0)]:
    for spots in combinations(range(9), 2):
        pixels = list(shape)
        for i in spots:
            pixels[i] = 1 - pixels[i]
        if pixels not in world_seen:
            world_test.append((pixels, label))


def score(weights, bias, examples):
    """How many of the examples the model gets right."""
    return sum(1 for pixels, label in examples if predict(weights, bias, pixels) == label)


def train_perceptron(examples, learning_rate=0.5, epochs=10):
    """The training loop, as a function: returns the weights and the bias."""
    # Your code here.
```

```hint
Start with `weights = [0.0] * 9` and `bias = 0.0`. Then the loop from
"Running it again and again", without the accuracy list. End with
`return weights, bias`.
```

```inputs
score(*train_perceptron(world_train), world_train)
score(*train_perceptron(world_train), world_test)
len(world_test)
```

```solution
def train_perceptron(examples, learning_rate=0.5, epochs=10):
    """The training loop, as a function: returns the weights and the bias."""
    weights = [0.0] * 9
    bias = 0.0
    for _ in range(epochs):
        for pixels, label in examples:
            error = label - predict(weights, bias, pixels)
            for i in range(9):
                weights[i] += learning_rate * error * pixels[i]
            bias += learning_rate * error
    return weights, bias
---
Trained, the model gets all 20 training pictures right, and 43 of the 50 it never saw. The two tracks differ in 4 pixels, so two flips can meet in the middle: a picture two flips from the footprint can also be two flips from the pawprint. 4 of the test pictures are like that, and they appear with both labels. No model could get all of those right.
```

</div>

<div class="dl-world" data-world="queues-and-crowds">

People seen from above: standing in a row along a counter, or waiting one behind the other in a single-file queue.

```python exec
id: your-world-1--queues-and-crowds
ROW = [0, 0, 0,
       1, 1, 1,
       0, 0, 0]    # people in a row: label 1

QUEUE = [0, 1, 0,
         0, 1, 0,
         0, 1, 0]    # people in a single-file queue: label 0

random.seed(1)
world_train = []
for _ in range(10):
    world_train.append((noisy(ROW, 2), 1))
    world_train.append((noisy(QUEUE, 2), 0))
random.shuffle(world_train)

world_seen = [pixels for pixels, label in world_train]
world_test = []
for shape, label in [(ROW, 1), (QUEUE, 0)]:
    for spots in combinations(range(9), 2):
        pixels = list(shape)
        for i in spots:
            pixels[i] = 1 - pixels[i]
        if pixels not in world_seen:
            world_test.append((pixels, label))


def score(weights, bias, examples):
    """How many of the examples the model gets right."""
    return sum(1 for pixels, label in examples if predict(weights, bias, pixels) == label)


def train_perceptron(examples, learning_rate=0.5, epochs=10):
    """The training loop, as a function: returns the weights and the bias."""
    # Your code here.
```

```hint
Start with `weights = [0.0] * 9` and `bias = 0.0`. Then the loop from
"Running it again and again", without the accuracy list. End with
`return weights, bias`.
```

```inputs
score(*train_perceptron(world_train), world_train)
score(*train_perceptron(world_train), world_test)
len(world_test)
```

```solution
def train_perceptron(examples, learning_rate=0.5, epochs=10):
    """The training loop, as a function: returns the weights and the bias."""
    weights = [0.0] * 9
    bias = 0.0
    for _ in range(epochs):
        for pixels, label in examples:
            error = label - predict(weights, bias, pixels)
            for i in range(9):
                weights[i] += learning_rate * error * pixels[i]
            bias += learning_rate * error
    return weights, bias
---
Trained, the model gets 19 of the 20 training pictures right, not all of them, and 46 of the 52 it never saw. The one it misses is a picture that appears in the training set twice, once as a row and once as a queue: two flips from each shape made the same picture. No model could get both copies right. The two shapes differ in only 4 pixels, which is why that can happen.
```

</div>

<div class="dl-world" data-world="spread">

A disease on a map of towns: spreading along a road, or out from one town in four directions.

```python exec
id: your-world-1--spread
ROAD = [0, 0, 0,
        1, 1, 1,
        0, 0, 0]    # along a road: label 1

FOUR_WAYS = [0, 1, 0,
             1, 1, 1,
             0, 1, 0]    # out in four directions: label 0

random.seed(1)
world_train = []
for _ in range(10):
    world_train.append((noisy(ROAD, 2), 1))
    world_train.append((noisy(FOUR_WAYS, 2), 0))
random.shuffle(world_train)

world_seen = [pixels for pixels, label in world_train]
world_test = []
for shape, label in [(ROAD, 1), (FOUR_WAYS, 0)]:
    for spots in combinations(range(9), 2):
        pixels = list(shape)
        for i in spots:
            pixels[i] = 1 - pixels[i]
        if pixels not in world_seen:
            world_test.append((pixels, label))


def score(weights, bias, examples):
    """How many of the examples the model gets right."""
    return sum(1 for pixels, label in examples if predict(weights, bias, pixels) == label)


def train_perceptron(examples, learning_rate=0.5, epochs=10):
    """The training loop, as a function: returns the weights and the bias."""
    # Your code here.
```

```hint
Start with `weights = [0.0] * 9` and `bias = 0.0`. Then the loop from
"Running it again and again", without the accuracy list. End with
`return weights, bias`.
```

```inputs
score(*train_perceptron(world_train), world_train)
score(*train_perceptron(world_train), world_test)
len(world_test)
```

```solution
def train_perceptron(examples, learning_rate=0.5, epochs=10):
    """The training loop, as a function: returns the weights and the bias."""
    weights = [0.0] * 9
    bias = 0.0
    for _ in range(epochs):
        for pixels, label in examples:
            error = label - predict(weights, bias, pixels)
            for i in range(9):
                weights[i] += learning_rate * error * pixels[i]
            bias += learning_rate * error
    return weights, bias
---
Trained, the model gets all 20 training pictures right, but only 29 of the 45 it never saw. The two shapes differ in only 2 pixels. Two flips, at the top and bottom middle, turn the road into the four directions exactly. 10 of the test pictures could have come from either shape, and they appear with both labels. The model is not careless here: the pictures do not hold enough to tell the two apart.
```

</div>

<div class="dl-world" data-world="space-and-physics">

A camera's picture of a meteor streak: falling to the left, from top-left to bottom-right, or to the right.

```python exec
id: your-world-1--space-and-physics
LEFT = [1, 0, 0,
        0, 1, 0,
        0, 0, 1]    # a streak falling to the left: label 1

RIGHT = [0, 0, 1,
         0, 1, 0,
         1, 0, 0]    # a streak falling to the right: label 0

random.seed(1)
world_train = []
for _ in range(10):
    world_train.append((noisy(LEFT, 2), 1))
    world_train.append((noisy(RIGHT, 2), 0))
random.shuffle(world_train)

world_seen = [pixels for pixels, label in world_train]
world_test = []
for shape, label in [(LEFT, 1), (RIGHT, 0)]:
    for spots in combinations(range(9), 2):
        pixels = list(shape)
        for i in spots:
            pixels[i] = 1 - pixels[i]
        if pixels not in world_seen:
            world_test.append((pixels, label))


def score(weights, bias, examples):
    """How many of the examples the model gets right."""
    return sum(1 for pixels, label in examples if predict(weights, bias, pixels) == label)


def train_perceptron(examples, learning_rate=0.5, epochs=10):
    """The training loop, as a function: returns the weights and the bias."""
    # Your code here.
```

```hint
Start with `weights = [0.0] * 9` and `bias = 0.0`. Then the loop from
"Running it again and again", without the accuracy list. End with
`return weights, bias`.
```

```inputs
score(*train_perceptron(world_train), world_train)
score(*train_perceptron(world_train), world_test)
len(world_test)
```

```solution
def train_perceptron(examples, learning_rate=0.5, epochs=10):
    """The training loop, as a function: returns the weights and the bias."""
    weights = [0.0] * 9
    bias = 0.0
    for _ in range(epochs):
        for pixels, label in examples:
            error = label - predict(weights, bias, pixels)
            for i in range(9):
                weights[i] += learning_rate * error * pixels[i]
            bias += learning_rate * error
    return weights, bias
---
Trained, the model gets all 20 training pictures right, and 38 of the 50 it never saw. The two streaks share the centre and differ in the 4 corners, so two flips from each can meet in the middle. 4 of the test pictures are like that, and appear with both labels. The rest of its misses are its own.
```

</div>

## Lab bench

Every number the training uses is named at the top of the cell. Change
them, run it, and see what happens.

```python exec
id: lab-bench-1
FLIPS = 3             # pixels switched in each messy picture
PER_SHAPE = 10        # messy training pictures of each shape
LEARNING_RATE = 0.5
EPOCHS = 10
SEED = 1              # change it for a different set of training pictures

random.seed(SEED)
lab_train = []
for _ in range(PER_SHAPE):
    lab_train.append((noisy(PLUS, FLIPS), 1))
    lab_train.append((noisy(CROSS, FLIPS), 0))
random.shuffle(lab_train)

lab_weights, lab_bias = [0.0] * 9, 0.0
for epoch in range(1, EPOCHS + 1):
    for pixels, label in lab_train:
        error = label - predict(lab_weights, lab_bias, pixels)
        for i in range(9):
            lab_weights[i] += LEARNING_RATE * error * pixels[i]
        lab_bias += LEARNING_RATE * error
    right = sum(1 for pixels, label in lab_train if predict(lab_weights, lab_bias, pixels) == label)
    print(f"after epoch {epoch}: {right} of {len(lab_train)} training pictures right")

lab_seen = [pixels for pixels, label in lab_train]
lab_test = []
for shape, label in [(PLUS, 1), (CROSS, 0)]:
    for spots in combinations(range(9), FLIPS):
        pixels = list(shape)
        for i in spots:
            pixels[i] = 1 - pixels[i]
        if pixels not in lab_seen:
            lab_test.append((pixels, label))
right = sum(1 for pixels, label in lab_test if predict(lab_weights, lab_bias, pixels) == label)
print(f"never seen: {right} of {len(lab_test)} right")
```

Choose one of these questions, or ask one of your own:

1. Set `FLIPS = 4`. The plus and the cross differ in 8 pixels, so four
   flips from each can now meet in the middle. What happens to the
   score on the pictures it never saw?
2. Set `PER_SHAPE = 2`. How well does a model trained on four pictures
   do on the ones it never saw?
3. Try five different values of `SEED`. How much does the never-seen
   score depend on which pictures it trained on?
4. Does training for 100 epochs, not 10, change the never-seen score?

## Where to read more

Rosenblatt, F. (1958). *The Perceptron: A Probabilistic Model for
Information Storage and Organization in the Brain.* Psychological Review,
65(6), 386–408. This is the original paper. The `predict()` rule and the training
loop on this page are a simplified form of the perceptron it describes,
nearly seventy years before this course.

Nielsen, M. (2015). *Neural Networks and Deep Learning*.
<http://neuralnetworksanddeeplearning.com/>. It is a free online book.
Chapter 1 starts from exactly this kind of small example, which you can
check by hand. It moves towards a real handwritten-digit classifier, and
it shows all the arithmetic in between.

Spanning Tree (2025). *Perceptrons: The First Trainable Neural Networks.*
<https://www.youtube.com/watch?v=Ip6RIHwi21c>. Brian Yu tells the story of
Frank Rosenblatt's perceptron, from 1957, and shows how it learns: each
time it gets an example wrong, it moves its weights a little. The video
is about twelve minutes long.
