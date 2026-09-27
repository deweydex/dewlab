---
title: "Limits and judgement: testing what a model can do"
year: "2026-2027"
version: 2026.09.27.1
datasets: [the-time-machine, dracula, dubliners, irish-fairy-tales, treasure-island]
worlds:
  the-time-machine: The Time Machine, by H. G. Wells (1895), a journey to the far future.
  dracula: Dracula, by the Dublin-born writer Bram Stoker (1897), told in letters and diaries.
  dubliners: Dubliners, by James Joyce (1914), fifteen stories set in Dublin.
  irish-fairy-tales: Irish Fairy Tales, by James Stephens (1920), the old stories of Fionn and the Fianna.
  treasure-island: Treasure Island, by Robert Louis Stevenson (1883), pirates and a voyage by sea.
---

# Limits and judgement: testing what a model can do

The models in this course are small. The questions on this page are
the ones worth asking about any model, however big. Where does it
fail? What does its data leave out? Whose work did it learn from? And
when somebody makes a claim about it, how do you check the claim?

Each question comes with a test you can run, on the digit reader from
[Classifying pictures: one perceptron for each
class](tutorial:telling-many-pictures-apart), or on a chain built from
a book you choose. What you conclude is for you to decide.

## Where it fails

The first cell builds the digit reader again, with 20 training
pictures of each digit. It gets 0.935 of the test pictures right.

```python exec
id: where-it-fails-1
import random
import re


def picture(rows):
    return [1 if square == "#" else 0 for row in rows for square in row]


DIGITS = {
    "0": picture([".###.", "#...#", "#...#", "#...#", ".###."]),
    "1": picture(["..#..", ".##..", "..#..", "..#..", ".###."]),
    "4": picture(["#..#.", "#..#.", "#####", "...#.", "...#."]),
    "7": picture(["#####", "...#.", "..#..", ".#...", ".#..."]),
}


def noisy(pixels, flips):
    copy = list(pixels)
    for i in random.sample(range(len(pixels)), flips):
        copy[i] = 1 - copy[i]
    return copy


def make_test(classes, per_class=50, flips=6, seed=100):
    random.seed(seed)
    return [(noisy(pixels, flips), name)
            for name, pixels in classes.items() for _ in range(per_class)]


def make_train(classes, per_class, avoid, flips=5, seed=1):
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


def total(weights, bias, pixels):
    return sum(w * p for w, p in zip(weights, pixels)) + bias


def classify(model, pixels):
    best_name, best_total = None, None
    for name, (weights, bias) in model.items():
        this_total = total(weights, bias, pixels)
        if best_total is None or this_total > best_total:
            best_name, best_total = name, this_total
    return best_name


def share_right(model, examples):
    return sum(1 for pixels, name in examples if classify(model, pixels) == name) / len(examples)


def train_model(train, epochs=10, learning_rate=0.5):
    names = sorted({name for pixels, name in train})
    model = {name: ([0.0] * 25, 0.0) for name in names}
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
    return model


test = make_test(DIGITS)
train = make_train(DIGITS, 20, test)
model = train_model(train)
print("training pictures:", share_right(model, train))
print("test pictures:", share_right(model, test))
```

Now give it two pictures that are not any of its digits: 25 pixels
chosen at random, and a 3, a digit it was never taught. The cell
prints its answer, and the total from each of its four perceptrons.

```python exec
id: where-it-fails-2
random.seed(1)
noise = [random.randint(0, 1) for _ in range(25)]
three = picture(["####.", "....#", ".###.", "....#", "####."])

for name, pixels in [("random pixels", noise), ("a 3", three)]:
    totals = {digit: total(weights, bias, pixels) for digit, (weights, bias) in model.items()}
    print(name, "is read as", classify(model, pixels), totals)
```

It reads the random pixels as a 1, and the 3 as a 0. Every total is
below zero, so none of the four perceptrons said "yes". It answered
anyway. A reader with four answers gives one of the four every time.
It has no answer that means "none of these", or "I do not know".

Bigger models can say "I do not know". But they can also give a wrong
answer in the same confident words as a right one, and the words alone
do not tell you which it is.

Here is a harder test. Every picture it learned from had its digit in
the same place on the grid. What if each test picture is moved one
column to the right?

```python exec
id: where-it-fails-3
def move_right(pixels):
    """The same picture, one column to the right. The last column falls off."""
    rows = [pixels[r * 5:r * 5 + 5] for r in range(5)]
    return [p for row in rows for p in [0] + row[:4]]


moved = [(move_right(pixels), name) for pixels, name in test]
print(share_right(model, moved))
```

```predict
type: number
tolerance: 0.1

The reader gets 0.935 of the test pictures right. What share of the
same pictures, each moved one column, will it get right?
```

0.225: fewer than one in four, and worse than guessing. Even the four
clean digits, moved one column, are all read wrongly. To a person, a
digit moved one column is the same digit. To this model it is a new
picture, because it learned where the ink was, not the shape the ink
made. Its training pictures never showed it anything else.

## What the data leaves out

A chain can write only what its book contains. Choose a book, and the
next cells ask what that book leaves out.

<div class="dl-world" data-world="the-time-machine">

```python exec
id: what-the-data-leaves-out-1--the-time-machine
raw = await load_text("the-time-machine.txt")
```

</div>

<div class="dl-world" data-world="dracula">

```python exec
id: what-the-data-leaves-out-1--dracula
raw = await load_text("dracula.txt")
```

</div>

<div class="dl-world" data-world="dubliners">

```python exec
id: what-the-data-leaves-out-1--dubliners
raw = await load_text("dubliners.txt")
```

</div>

<div class="dl-world" data-world="irish-fairy-tales">

```python exec
id: what-the-data-leaves-out-1--irish-fairy-tales
raw = await load_text("irish-fairy-tales.txt")
```

</div>

<div class="dl-world" data-world="treasure-island">

```python exec
id: what-the-data-leaves-out-1--treasure-island
raw = await load_text("treasure-island.txt")
```

</div>

First, a sentence from today. Which of its words has your book never
used?

```python exec
id: what-the-data-leaves-out-2
start = raw.find("*** START OF")
end = raw.find("*** END OF")
book = raw[raw.index("\n", start):end].strip()
counts = {}
for word in re.findall("[a-z]+", book.lower()):
    counts[word] = counts.get(word, 0) + 1

sentence = "I sent a text message from my phone to the computer"
print("in the book:", [w for w in sentence.lower().split() if w in counts])
print("never in the book:", [w for w in sentence.lower().split() if w not in counts])
```

None of the five books has "phone" or "computer". A chain built from
your book can never write them, and it can never say anything about
the world since the book was written.

Now a question about who the book is about. How often does it say
"he", and how often "she"?

```python exec
id: what-the-data-leaves-out-3
for word in ["he", "she", "his", "her", "him"]:
    print(word, counts.get(word, 0))
print("he for every she:", round(counts["he"] / counts["she"], 1))
```

<div class="dl-world" data-world="the-time-machine">

In *The Time Machine*, "he" appears 123 times and "she" 46: about 2.7
to 1.

</div>

<div class="dl-world" data-world="dracula">

In *Dracula*, "he" appears 2,580 times and "she" 816: about 3.2 to 1,
even though Mina and Lucy are two of its main characters.

</div>

<div class="dl-world" data-world="dubliners">

In *Dubliners*, "he" appears 1,711 times and "she" 714: about 2.4 to 1.

</div>

<div class="dl-world" data-world="irish-fairy-tales">

In *Irish Fairy Tales*, "he" appears 1,460 times and "she" 470: about
3.1 to 1.

</div>

<div class="dl-world" data-world="treasure-island">

In *Treasure Island*, "he" appears 936 times and "she" 82: about 11 to
1. Apart from Jim's mother, who stays at home, almost every character
is a man.

</div>

A chain from this book will write "he" far more often than "she",
because the book does. That is not an error in the chain. It is the
book, repeated. A model learns the world of the text it was given:
the time, the place, and the people the writers chose to write about.
A model trained on much more text learns much more of the world, but
the same question applies to it. Whose world is in the text, and
whose is missing?

Try another word. Pick a word from today's world, a place, or a kind
of person, and count it in your book.

```python exec
id: what-the-data-leaves-out-4
# Your own counts.
```

## Whose work it learns from

Every word your chain writes came from somebody. Here is the start of
the file the book came from, before the story begins.

```python exec
id: whose-work-it-learns-from-1
print(raw[:raw.find("*** START OF")].strip()[:400])
```

The book comes from Project Gutenberg, a free online library. Its writer
died long ago, and the book is in the *public domain*: free for anyone
to copy, in the United States and many other countries. So the writer's
permission was not needed to build a chain from it.

How much of what the chain writes is the writer's own words? A chain
keyed on three words, from the whole book, writes 40 more words, and
`longest_copied()` finds the longest run that appears, word for word,
in the book.

```python exec
id: whose-work-it-learns-from-2
words = book.split()
chain3 = {}
for w1, w2, w3, next_word in zip(words, words[1:], words[2:], words[3:]):
    chain3.setdefault((w1, w2, w3), {})
    chain3[(w1, w2, w3)][next_word] = chain3[(w1, w2, w3)].get(next_word, 0) + 1

random.seed(1)
result = list(random.choice(list(chain3)))
for _ in range(40):
    key = tuple(result[-3:])
    if key not in chain3:
        break
    followers = chain3[key]
    result.append(random.choices(list(followers), weights=list(followers.values()))[0])

book_text = " " + " ".join(words) + " "


def longest_copied(result):
    longest = 0
    for i in range(len(result)):
        j = i + longest + 1
        while j <= len(result) and " " + " ".join(result[i:j]) + " " in book_text:
            longest = j - i
            j += 1
    return longest


print(" ".join(result))
print(longest_copied(result), "of", len(result), "words copied in one run")
```

<div class="dl-world" data-world="the-time-machine">

37 of the 43 words are one run from the book.

</div>

<div class="dl-world" data-world="dracula">

24 of the 43 words are one run from the book.

</div>

<div class="dl-world" data-world="dubliners">

16 of the 43 words are one run from the book.

</div>

<div class="dl-world" data-world="irish-fairy-tales">

23 of the 43 words are one run from the book.

</div>

<div class="dl-world" data-world="treasure-island">

All 43 words are one run from the book: the chain has copied a whole
passage of Stevenson.

</div>

A chain keyed on three words is mostly a copy machine. Big language
models are not built like this, but they can also repeat parts of the
text they learned from, word for word. Researchers have shown it, and
some of the text they found was personal information about real people.

Big models learn from far more than one old book: web pages, books,
news articles, pieces of code. Much of it was written by people who
are alive, and who were never asked. Many writers, artists and news
organisations have objected that their work was used without their
permission, and some have gone to court. Here are two questions to
think about, with no answer given here:

- Should a model be allowed to learn from somebody's writing without
  asking them? Does your answer change if the model can repeat the
  writing word for word?
- Your chain is free to build because its writer died long ago. What
  would change if you built it from a friend's messages, or from a
  living writer's new novel?

## Checking a claim

Suppose somebody says: "Our digit reader is 93.5% accurate." It is
true of the reader on this page. What should you ask before you trust
it? Here are four questions, each with a test.

**1. Accurate on what?** On the pictures it was trained on, the
reader is 100% right. On pictures it never saw, 93.5%. A claim that
does not say which is not worth much.

**2. Compared with what?** A reader that always says "0", without
looking at the picture, gets 25% of our test pictures right, because a
quarter of them are 0s. That is the lowest score that means anything
here, and it is called the *baseline*. But a test set can be built to
make that number much higher. The next cell makes a test set of the 50
zeros and 10 other digits.

```python exec
id: checking-a-claim-1
lopsided = [(p, n) for p, n in test if n == "0"] + [(p, n) for p, n in test if n != "0"][:10]
print("always '0':", round(sum(1 for p, n in lopsided if n == "0") / len(lopsided), 3))
print("the reader:", round(share_right(model, lopsided), 3))
```

On this set, a reader that never looks at a picture gets 0.833, and
ours gets 0.9. The same reader could be called "90% accurate" or
"93.5% accurate", depending on who chose the test pictures.

**3. Accurate for whom?** One overall number can hide a class that
does badly. In 2018, Joy Buolamwini and Timnit Gebru tested three
systems that guessed a person's gender from a photo of their face.
The systems were sold by large companies, and their overall accuracy
looked high. But when the two researchers counted the mistakes for
each group of people separately, the error rate for darker-skinned
women was up to 34.7%, and for lighter-skinned men at most 0.8%.
`right_by_class()` from the classifier page asks the same question of
our reader.

**4. On pictures like which?** The reader is 93.5% right on test
pictures made in the same way as its training pictures. Moved one
column, it is 22.5% right. A claim is only as wide as its test.

### Your turn

Can you write `baseline_share(examples)`? It returns the share of the
examples that a reader would get right by always giving the most
common answer, without looking at any picture.

```python exec
id: checking-a-claim-2
def baseline_share(examples):
    """The share right for a reader that always gives the most common answer."""
    # Your code here.
```

```hint
Count how many times each name appears in `examples`. The largest
count, divided by the number of examples, is the share.
```

```inputs
baseline_share(test)
round(baseline_share(lopsided), 3)
baseline_share(train)
```

```solution
def baseline_share(examples):
    """The share right for a reader that always gives the most common answer."""
    counts = {}
    for pixels, name in examples:
        counts[name] = counts.get(name, 0) + 1
    return max(counts.values()) / len(examples)
---
0.25 on the test pictures and the training pictures, where every digit appears equally often, and 0.833 on the lopsided set. Any claim about a reader's accuracy can be set beside this number.
```

## A claim of your own

Find a claim made about a real model: in an advert, a news story, or
a company's own web page. Write the four questions beside it. Which
of them does the claim answer? Which could you test yourself, and
which could only the makers answer?

## Where to read more

Buolamwini, J. and Gebru, T. (2018). *Gender Shades: Intersectional
Accuracy Disparities in Commercial Gender Classification.* Proceedings
of the 1st Conference on Fairness, Accountability and Transparency,
PMLR 81, 77–91. The study in question 3. It shows how to count the
mistakes for each group, not only overall.

Carlini, N. and others (2021). *Extracting Training Data from Large
Language Models.* 30th USENIX Security Symposium. The researchers
asked a language model, GPT-2, to write, and found passages of its
training text in what it wrote, word for word, some with names and
contact details of real people.

Bender, E. M., Gebru, T., McMillan-Major, A. and Shmitchell, S. (2021).
*On the Dangers of Stochastic Parrots: Can Language Models Be Too
Big?* Proceedings of the 2021 ACM Conference on Fairness,
Accountability, and Transparency. It asks what a very large collection
of web text leaves out, and whose language and views it gives the
most weight to.
