---
title: "Classifying pictures: one perceptron for each class"
year: "2026-2027"
version: 2026.09.27.2
worlds:
  game-items: Items from a game, drawn as sprites. A sword, a shield, a potion and a key.
  weather-icons: The icons of a weather forecast. Sun, cloud, rain and lightning.
  arrows: Four arrows, pointing up, down, left and right.
  faces: Four faces, happy, sad, surprised and asleep.
---

# Classifying pictures: one perceptron for each class

The perceptron in [The perceptron: a model that learns from its
mistakes](tutorial:a-model-that-corrects-itself) answered one question:
plus or cross? Most real questions have more than two answers. A
machine that reads house numbers must tell ten digits apart, and one that
reads a page of text must tell dozens of letters apart.

Each kind of picture is called a *class*. A model that sorts pictures
into classes is called a *classifier*. On this page we build a
classifier for four digits, drawn on a grid of 5 by 5 pixels, from the
perceptron you already know.

## Four digits on a grid

`picture()` turns five rows of `#` and `.` into a list of 25 pixels:
1 for `#`, and 0 for `.`. It is easier to draw a digit that way than to
write 25 numbers.

```python exec
id: four-digits-on-a-grid-1
import random
import matplotlib.pyplot as plt


def picture(rows):
    """Five strings of five characters, # for black, to a list of 25 pixels."""
    return [1 if square == "#" else 0 for row in rows for square in row]


DIGITS = {
    "0": picture([".###.", "#...#", "#...#", "#...#", ".###."]),
    "1": picture(["..#..", ".##..", "..#..", "..#..", ".###."]),
    "4": picture(["#..#.", "#..#.", "#####", "...#.", "...#."]),
    "7": picture(["#####", "...#.", "..#..", ".#...", ".#..."]),
}


def show(pixels, axis, title):
    """Draw 25 pixels as a 5 by 5 grid."""
    axis.imshow([pixels[r * 5:r * 5 + 5] for r in range(5)], cmap="gray_r", vmin=0, vmax=1)
    axis.set_title(title)
    axis.set_xticks([])
    axis.set_yticks([])


fig, axes = plt.subplots(1, 4, figsize=(8, 2.5))
for axis, (name, pixels) in zip(axes, DIGITS.items()):
    show(pixels, axis, name)
```

## Test pictures first

On the last page, the test pictures were made after training. This
time we make them first, and put them aside. Then no training picture
can ever be one of them.

A messy copy of a digit has some of its 25 pixels flipped, black to
white or white to black. The test pictures have 6 flips each, 50 of
each digit. The training pictures have 5 flips each, and there are only
5 of each digit, so the model learns from 20 pictures and is tested on
200.

```python exec
id: test-pictures-first-1
def noisy(pixels, flips):
    """A copy of pixels with `flips` different pixels switched."""
    copy = list(pixels)
    for i in random.sample(range(len(pixels)), flips):
        copy[i] = 1 - copy[i]
    return copy


def make_test(classes, per_class=50, flips=6, seed=100):
    """Messy copies of every class, to test with, never to train on."""
    random.seed(seed)
    return [(noisy(pixels, flips), name)
            for name, pixels in classes.items() for _ in range(per_class)]


def make_train(classes, per_class, avoid, flips=5, seed=1):
    """Messy copies of every class, to train on. None of them is in `avoid`."""
    random.seed(seed)
    unseen = [pixels for pixels, name in avoid]
    train = []
    while len(train) < per_class * len(classes):
        for name, pixels in classes.items():
            messy = noisy(pixels, flips)
            if messy not in unseen:
                train.append((messy, name))
    train = train[:per_class * len(classes)]
    random.shuffle(train)
    return train


test = make_test(DIGITS)
train = make_train(DIGITS, 5, test)
print(len(train), "training pictures,", len(test), "test pictures")

fig, axes = plt.subplots(1, 4, figsize=(8, 2.5))
for axis, (pixels, name) in zip(axes, train):
    show(pixels, axis, "a messy " + name)
```

Five flips out of 25 is a lot. Can you name each messy digit before
you read its title?

## One perceptron for each digit

Each digit gets a perceptron of its own. Each perceptron answers one
yes-or-no question, such as "is this a 7?" It is trained exactly as on
the last page. For each training picture, the right answer is "yes"
for the perceptron of that picture's digit, and "no" for the other
three.

To name a picture, we ask all four perceptrons for their totals, and
take the digit whose total is highest. Why not take the one that says
"yes"? Because for some pictures, none of the four says "yes", and for
others, more than one does. The highest total always gives exactly one
answer. If two totals are equal, the loop keeps the first of them.

```python exec
id: one-perceptron-for-each-digit-1
def total(weights, bias, pixels):
    return sum(w * p for w, p in zip(weights, pixels)) + bias


def classify(model, pixels):
    """The class whose perceptron gives these pixels the highest total."""
    best_name, best_total = None, None
    for name, (weights, bias) in model.items():
        this_total = total(weights, bias, pixels)
        if best_total is None or this_total > best_total:
            best_name, best_total = name, this_total
    return best_name


def share_right(model, examples):
    return sum(1 for pixels, name in examples if classify(model, pixels) == name) / len(examples)


def train_model(train, test, epochs=10, learning_rate=0.5):
    """One perceptron per class, and the share right on train and test after each epoch."""
    names = sorted({name for pixels, name in train})
    model = {name: ([0.0] * 25, 0.0) for name in names}
    history = []
    for epoch in range(epochs):
        for pixels, label in train:
            for name, (weights, bias) in model.items():
                target = 1 if name == label else 0
                guess = 1 if total(weights, bias, pixels) > 0 else 0
                error = target - guess
                if error != 0:
                    for i in range(25):
                        weights[i] += learning_rate * error * pixels[i]
                    model[name] = (weights, bias + learning_rate * error)
        history.append((share_right(model, train), share_right(model, test)))
    return model, history


model, history = train_model(train, test)

plt.figure()
plt.plot(range(1, 11), [h[0] for h in history], marker="o", label="training pictures")
plt.plot(range(1, 11), [h[1] for h in history], marker="o", label="test pictures")
plt.ylim(0, 1.05)
plt.xlabel("epoch")
plt.ylabel("share right")
plt.legend()
print(round(history[-1][1], 2))
```

```predict
type: number
tolerance: 0.05

The last line is the share of the 200 test pictures it names
correctly, after ten epochs. What will it be? Guessing at random would
give about 0.25.
```

After three epochs it names every training picture correctly, and
after that nothing changes. On the test pictures it never saw, it gets
0.86: 172 of 200. The gap between the two lines is the gap from the
last page, now with four classes.

How often does no perceptron say "yes"? For 50 of the 200 test
pictures, all four totals are zero or below, and for 8, more than one
is above zero. The highest total still names each of them.

## Which digits does it mix up?

A table with a row for each true digit, and a column for each answer
the model gave, shows where the mistakes are. It is called a *confusion
matrix*. Each row of the printout is a true digit, and each column is
the answer the model gave. The right answers are on the diagonal, from
top left to bottom right. Every number off the diagonal is a mistake.

```python exec
id: which-digits-does-it-mix-up-1
names = sorted(DIGITS)
confusion = {true: {guess: 0 for guess in names} for true in names}
for pixels, name in test:
    confusion[name][classify(model, pixels)] += 1

print("read as:", names)
for true in names:
    print(true, [confusion[true][guess] for guess in names])

wrong = [(pixels, name) for pixels, name in test if classify(model, pixels) != name]
fig, axes = plt.subplots(1, 4, figsize=(8, 2.5))
for axis, (pixels, name) in zip(axes, wrong):
    show(pixels, axis, "a " + name + ", read as " + classify(model, pixels))
```

The 0s, 4s and 7s are nearly all right. The 1s are the problem: 14 of
them are read as 7, and 7 more as 0. Look at the four mistakes drawn
under the table. Would you have named them correctly? Some messy
pictures are hard for a person too, and some are not.

## More pictures to learn from

The model learned from only 5 pictures of each digit. What happens
with more? The test pictures stay the same, so the scores can be
compared fairly.

```python exec
id: more-pictures-to-learn-from-1
for per_class in [5, 10, 20, 40]:
    more = make_train(DIGITS, per_class, test)
    bigger_model, bigger_history = train_model(more, test)
    print(per_class, "of each digit:", round(bigger_history[-1][1], 3), "of the test pictures right")
```

More examples help: from 0.86 with 5 of each digit, to 0.985 with 40.
The model and its rule never changed. Only the number of examples did.
This is true of much bigger models too. Much of their skill comes from
the number of examples they learn from.

## What each perceptron learned

Each perceptron has 25 weights, one for each pixel. We can draw them as
a picture of their own. Here they are for the model trained on 40 of
each digit. Red is a positive weight: a lit pixel there pushes the
total up, towards "yes". Blue is a negative weight, which pushes it
down.

```python exec
id: what-each-perceptron-learned-1
model_40, history_40 = train_model(make_train(DIGITS, 40, test), test)

fig, axes = plt.subplots(1, 4, figsize=(8, 2.5))
for axis, name in zip(axes, sorted(model_40)):
    weights, bias = model_40[name]
    axis.imshow([weights[r * 5:r * 5 + 5] for r in range(5)], cmap="bwr", vmin=-3, vmax=3)
    axis.set_title("weights for " + name)
    axis.set_xticks([])
    axis.set_yticks([])
```

Some of the pattern is easy to read. The 0's most negative weight is
the blue square in the centre, where every other digit has ink and a 0
has a hole. The 7's strongest weight is the top-right corner, where
only the 7 has ink. The 4's weights are red across its crossbar, the
middle row, except in the centre, which all four digits share. Much of
the rest looks like noise, as the sizes did on the last page: a weight
moves only when there is a mistake to correct.

## Digits that look alike

Now add an 8 and a 9. They share many pixels with the 0, and with each
other. The cell trains on 20 of each of the six digits, and prints the
share right on both sets after each epoch.

```python exec
id: digits-that-look-alike-1
SIX = dict(DIGITS)
SIX["8"] = picture([".###.", "#...#", ".###.", "#...#", ".###."])
SIX["9"] = picture([".###.", "#...#", ".####", "....#", ".###."])

test_six = make_test(SIX)
model_six, history_six = train_model(make_train(SIX, 20, test_six), test_six)
print("training:", [round(h[0], 2) for h in history_six])
print("test:    ", [round(h[1], 2) for h in history_six])
```

Two things change. The score on the test pictures falls, to about 0.8.
And it jumps about from epoch to epoch: epochs 3 to 6 give 0.83, 0.81,
0.82 and 0.75. In none of the ten epochs does the model name every
training picture correctly. So every epoch still corrects some weights,
and a correction that helps one digit can undo another. The 9 suffers
most: only 20 of its 50 test pictures are named correctly. The rest are
read as every one of the other digits, most often 1 and 0.

## Your world

Can you write `right_by_class(model, test)`? It returns a dictionary
with one entry for each class: how many of that class's test pictures
the model names correctly.

<div class="dl-world" data-world="game-items">

Four items from a game. The cell draws them, and trains a model on 10
messy copies of each, with the functions from this page.

```python exec
id: your-world-1--game-items
ITEMS = {
    "sword": picture(["..#..", "..#..", "..#..", "#####", "..#.."]),
    "shield": picture(["#####", "#...#", "#...#", ".#.#.", "..#.."]),
    "potion": picture(["..#..", ".###.", "#...#", "#####", ".###."]),
    "key": picture([".#...", "#.#..", ".#...", ".###.", ".#.#."]),
}
fig, axes = plt.subplots(1, 4, figsize=(8, 2.5))
for axis, (name, pixels) in zip(axes, ITEMS.items()):
    show(pixels, axis, name)

world_test = make_test(ITEMS)
world_model, world_history = train_model(make_train(ITEMS, 10, world_test), world_test)


def right_by_class(model, test):
    """For each class, how many of its test pictures the model names correctly."""
    # Your code here.
```

```hint
Start with a dictionary with 0 for every class. Then, for each
`(pixels, name)` in `test`, add 1 to that name's count when
`classify(model, pixels)` gives the same name.
```

```inputs
right_by_class(world_model, world_test)
round(share_right(world_model, world_test), 3)
```

```solution
def right_by_class(model, test):
    """For each class, how many of its test pictures the model names correctly."""
    right = {}
    for pixels, name in test:
        if name not in right:
            right[name] = 0
        if classify(model, pixels) == name:
            right[name] += 1
    return right
---
The shield gets 49 of its 50 right and the key only 42, with 0.92 of all 200 right. Which item has the most pixels in common with another? Try 20 of each item in place of 10: does the key do better?
```

</div>

<div class="dl-world" data-world="weather-icons">

The icons of a weather forecast. The cell draws them, and trains a
model on 10 messy copies of each, with the functions from this page.

```python exec
id: your-world-1--weather-icons
ICONS = {
    "sun": picture(["#.#.#", ".###.", "#####", ".###.", "#.#.#"]),
    "cloud": picture([".....", ".##..", "####.", "#####", "....."]),
    "rain": picture([".###.", "#####", ".....", "#.#.#", ".#.#."]),
    "lightning": picture(["...#.", "..#..", ".###.", "..#..", ".#..."]),
}
fig, axes = plt.subplots(1, 4, figsize=(8, 2.5))
for axis, (name, pixels) in zip(axes, ICONS.items()):
    show(pixels, axis, name)

world_test = make_test(ICONS)
world_model, world_history = train_model(make_train(ICONS, 10, world_test), world_test)


def right_by_class(model, test):
    """For each class, how many of its test pictures the model names correctly."""
    # Your code here.
```

```hint
Start with a dictionary with 0 for every class. Then, for each
`(pixels, name)` in `test`, add 1 to that name's count when
`classify(model, pixels)` gives the same name.
```

```inputs
right_by_class(world_model, world_test)
round(share_right(world_model, world_test), 3)
```

```solution
def right_by_class(model, test):
    """For each class, how many of its test pictures the model names correctly."""
    right = {}
    for pixels, name in test:
        if name not in right:
            right[name] = 0
        if classify(model, pixels) == name:
            right[name] += 1
    return right
---
The sun gets 49 of its 50 right, and the cloud only 37, with 0.86 of all 200 right. The sun has the most ink of the four. Is a picture with more black pixels easier to recognise after six flips? Try 20 of each icon in place of 10.
```

</div>

<div class="dl-world" data-world="arrows">

Four arrows. The cell draws them, and trains a model on 10 messy
copies of each, with the functions from this page.

```python exec
id: your-world-1--arrows
ARROWS = {
    "up": picture(["..#..", ".###.", "#.#.#", "..#..", "..#.."]),
    "down": picture(["..#..", "..#..", "#.#.#", ".###.", "..#.."]),
    "left": picture(["..#..", ".#...", "#####", ".#...", "..#.."]),
    "right": picture(["..#..", "...#.", "#####", "...#.", "..#.."]),
}
fig, axes = plt.subplots(1, 4, figsize=(8, 2.5))
for axis, (name, pixels) in zip(axes, ARROWS.items()):
    show(pixels, axis, name)

world_test = make_test(ARROWS)
world_model, world_history = train_model(make_train(ARROWS, 10, world_test), world_test)


def right_by_class(model, test):
    """For each class, how many of its test pictures the model names correctly."""
    # Your code here.
```

```hint
Start with a dictionary with 0 for every class. Then, for each
`(pixels, name)` in `test`, add 1 to that name's count when
`classify(model, pixels)` gives the same name.
```

```inputs
right_by_class(world_model, world_test)
round(share_right(world_model, world_test), 3)
```

```solution
def right_by_class(model, test):
    """For each class, how many of its test pictures the model names correctly."""
    right = {}
    for pixels, name in test:
        if name not in right:
            right[name] = 0
        if classify(model, pixels) == name:
            right[name] += 1
    return right
---
Only 0.655 of the 200 are right, and "up" only 14 of its 50. Up and down differ in just four pixels, as do left and right, so six flips can easily move one arrow most of the way to another. But why is "up" so much worse than "down"? The next cells look.
```

### Why "up" does badly

Is something wrong with the up arrow? The cell trains the same model
three times, each time on a different set of messy training arrows,
chosen by the `seed`. Then it counts what each model names correctly.
It has its own copy of the counting, so it runs even if yours is not
finished.

```python exec
id: why-up-does-badly-1--arrows
def right_per_arrow(model, test):
    """How many test arrows of each kind the model names correctly."""
    counts = {name: 0 for name in ARROWS}
    for pixels, name in test:
        if classify(model, pixels) == name:
            counts[name] += 1
    return counts


for seed in (1, 2, 3):
    arrow_model, arrow_history = train_model(make_train(ARROWS, 10, world_test, seed=seed), world_test)
    print("seed", seed, right_per_arrow(arrow_model, world_test), "training:", arrow_history[-1][0])
```

With seed 1, "up" gets only 14 right. With seed 2, "right" gets 14, and
with seed 3, "down" is the worst. So the up arrow is not the problem.
Which arrow does badly depends on the training arrows.

Look at the last number on each line. After 10 epochs, no model names
all of its own training arrows correctly, so its perceptrons are still
being corrected when training stops. Each perceptron's weights are
where the last few corrections left them. With seed 1, the last
corrections made the "up" perceptron's weights smaller: they add up to
−12, and the other three add up to between −1 and −3. So the "up" total
is rarely the highest, even for an up arrow.

### Keep the average

One way around this is to keep, for each perceptron, the average of its
weights over the whole of training, not its weights at the end. A few
bad corrections at the end then change the average only a little. This
is called an *averaged perceptron*.

```python exec
id: keep-the-average-1--arrows
def train_averaged(train, epochs=10, learning_rate=0.5):
    """Like train_model, but returns the average of each perceptron's weights
    over the whole of training, not its weights at the end."""
    names = sorted({name for pixels, name in train})
    model = {name: ([0.0] * 25, 0.0) for name in names}
    sums = {name: ([0.0] * 25, 0.0) for name in names}
    steps = 0
    for epoch in range(epochs):
        for pixels, label in train:
            for name, (weights, bias) in model.items():
                target = 1 if name == label else 0
                guess = 1 if total(weights, bias, pixels) > 0 else 0
                error = target - guess
                if error != 0:
                    for i in range(25):
                        weights[i] += learning_rate * error * pixels[i]
                    model[name] = (weights, bias + learning_rate * error)
            # After every picture, add each perceptron's weights to its sums.
            steps += 1
            for name, (weights, bias) in model.items():
                weight_sums, bias_sum = sums[name]
                sums[name] = ([s + w for s, w in zip(weight_sums, weights)], bias_sum + bias)
    return {name: ([s / steps for s in weight_sums], bias_sum / steps)
            for name, (weight_sums, bias_sum) in sums.items()}


averaged = train_averaged(make_train(ARROWS, 10, world_test))
print(right_per_arrow(averaged, world_test), round(share_right(averaged, world_test), 3))
```

The same training arrows now give "up" 30 right, not 14, and the share
rises from 0.655 to 0.685.

### Turn the arrows

The arrows have something the other worlds do not. Each one is a
quarter turn of another: turn "up" a quarter to the left, and it is
"left". So every messy training arrow can make three more, one pointing
each other way. The 10 training arrows of each kind become 40, with no
new drawing.

```python exec
id: turn-the-arrows-1--arrows
def turn(pixels):
    """A quarter turn to the left: the right-hand column becomes the top row."""
    return [pixels[column * 5 + (4 - row)] for row in range(5) for column in range(5)]


TURNED = {"up": "left", "left": "down", "down": "right", "right": "up"}
print(turn(ARROWS["up"]) == ARROWS["left"])


def with_turns(train):
    """Each training arrow, and the three arrows made by turning it."""
    more = []
    for pixels, name in train:
        for _ in range(4):
            more.append((pixels, name))
            pixels, name = turn(pixels), TURNED[name]
    return more


turned_train = with_turns(make_train(ARROWS, 10, world_test))
test_pixels = [pixels for pixels, name in world_test]
print(len(turned_train), "training arrows, and",
      sum(1 for pixels, name in turned_train if pixels in test_pixels), "of them are test arrows")
turned_model = train_averaged(turned_train)
print(right_per_arrow(turned_model, world_test), round(share_right(turned_model, world_test), 3))
```

The first line checks that a quarter turn of "up" is "left". None of
the 160 training arrows is a test arrow, so the test is still fair.
With turned arrows and the average, the model names 0.84 of the test
arrows correctly.

How good is that? The cell below compares each test arrow with the four
clean arrows, and chooses the one it differs from in the fewest pixels.

```python exec
id: turn-the-arrows-2--arrows
def closest_clean(pixels):
    """The arrow whose clean picture differs from these pixels in the fewest places."""
    best_name, best_count = None, None
    for name, clean in ARROWS.items():
        count = sum(1 for a, b in zip(clean, pixels) if a != b)
        if best_count is None or count < best_count:
            best_name, best_count = name, count
    return best_name


print(sum(1 for pixels, name in world_test if closest_clean(pixels) == name) / len(world_test))
```

It gets 0.825, and it was given the clean arrows. The model never saw a
clean arrow, only messy ones, and it does a little better.

How much of the gain comes from each idea? `train_model(turned_train,
world_test)[0]` is a model trained on the turned arrows without the
average. And could you turn the pictures in the other worlds? After a
quarter turn, which of them would still be the same class?

</div>

<div class="dl-world" data-world="faces">

Four faces. The cell draws them, and trains a model on 10 messy copies
of each, with the functions from this page.

```python exec
id: your-world-1--faces
FACES = {
    "happy": picture([".....", ".#.#.", ".....", "#...#", ".###."]),
    "sad": picture([".....", ".#.#.", ".....", ".###.", "#...#"]),
    "surprised": picture([".#.#.", ".....", "..#..", ".#.#.", "..#.."]),
    "asleep": picture([".....", "##.##", ".....", ".###.", "....."]),
}
fig, axes = plt.subplots(1, 4, figsize=(8, 2.5))
for axis, (name, pixels) in zip(axes, FACES.items()):
    show(pixels, axis, name)

world_test = make_test(FACES)
world_model, world_history = train_model(make_train(FACES, 10, world_test), world_test)


def right_by_class(model, test):
    """For each class, how many of its test pictures the model names correctly."""
    # Your code here.
```

```hint
Start with a dictionary with 0 for every class. Then, for each
`(pixels, name)` in `test`, add 1 to that name's count when
`classify(model, pixels)` gives the same name.
```

```inputs
right_by_class(world_model, world_test)
round(share_right(world_model, world_test), 3)
```

```solution
def right_by_class(model, test):
    """For each class, how many of its test pictures the model names correctly."""
    right = {}
    for pixels, name in test:
        if name not in right:
            right[name] = 0
        if classify(model, pixels) == name:
            right[name] += 1
    return right
---
Only 0.655 of the 200 are right. Each face has only six or seven black pixels, and six flips change as many again, so a messy face can be mostly noise. Draw a few test faces with `show()`: could you name them? With 20 of each face, the share rises to 0.835.
```

</div>

## Towards real handwriting

The digits on this page were drawn once, by one person, and then
messed up at random. Real handwriting is harder. Each person writes a
7 in their own way, a little to the left or right, a little larger or
smaller.

The best-known collection of real handwritten digits is called MNIST.
It has 70,000 digits, written by hundreds of people. Each one is a
grid of 28 by 28 pixels, with grey levels in place of black and white.
60,000 of them are for training, and 10,000 are kept apart for testing,
just as our test pictures were.

A classifier for MNIST can have exactly the shape of the one on this
page: one set of weights for each digit, now 784 weights each, and the
highest total wins. In 1998, a model of that kind got about 12 of every
100 test digits wrong. Models with many layers do much better, but the
first step is this one.

## Where to read more

LeCun, Y., Bottou, L., Bengio, Y. and Haffner, P. (1998).
*Gradient-Based Learning Applied to Document Recognition.* Proceedings
of the IEEE, 86(11), 2278–2324. This is the paper that made MNIST
famous. Its comparison of methods begins with a linear classifier, one
weighted sum for each digit, like ours, with an error rate of 12% on
the test digits.

Freund, Y. and Schapire, R. E. (1999). *Large Margin Classification
Using the Perceptron Algorithm.* Machine Learning, 37(3), 277–296. The
paper behind the averaged perceptron in the arrows world. It keeps
every set of weights that training passes through, and lets them vote.
Averaging them is its simpler form.

3Blue1Brown (2017). *But what is a neural network? | Deep learning
chapter 1.* <https://www.youtube.com/watch?v=aircAruvnKk>. It takes
MNIST's 28 by 28 digits and shows how a network with layers builds on
weighted sums like the ones on this page.
