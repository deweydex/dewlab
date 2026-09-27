---
title: "N-grams: a Markov chain that remembers more words"
year: "2026-2027"
version: 2026.09.26.1
datasets: [the-time-machine, dracula, dubliners, irish-fairy-tales, treasure-island]
covers:
  keying-on-more-than-one-word:
    covers: [CMPS-LO4]
  comparing-what-each-one-writes:
    touches: [CMPS-LO1]
  two-words-from-your-book:
    touches: [CMPS-LO4]
worlds:
  the-time-machine: The Time Machine, by H. G. Wells (1895), a journey to the far future.
  dracula: Dracula, by the Dublin-born writer Bram Stoker (1897), told in letters and diaries.
  dubliners: Dubliners, by James Joyce (1914), fifteen stories set in Dublin.
  irish-fairy-tales: Irish Fairy Tales, by James Stephens (1920), the old stories of Fionn and the Fianna.
  treasure-island: Treasure Island, by Robert Louis Stevenson (1883), pirates and a voyage by sea.
---

# N-grams: a Markov chain that remembers more words

In [A Markov chain from a whole book: a dictionary of
dictionaries](tutorial:a-chain-reads-a-book), we built a chain that
chooses the next word by looking at one word only: the word just before
it. What happens if the chain can remember more than that?

## Keying on more than one word

Here is the same book, loaded and cleaned in the same way as before.

```python exec
id: keying-on-more-than-one-word-1
raw = await load_text("the-time-machine.txt")
start = raw.find("*** START OF")
end = raw.find("*** END OF")
book = raw[raw.index("\n", start):end].strip()
words = book.split()
```

Next is the one-word chain from the last tutorial again. This time it is
called `order1`. The *order* of a chain is how many words before it the
chain looks at, when it chooses what comes next. `order1` looks at one.

```python exec
id: keying-on-more-than-one-word-2
order1 = {}
for word, next_word in zip(words, words[1:]):
    order1.setdefault(word, {})
    order1[word][next_word] = order1[word].get(next_word, 0) + 1

print(len(order1["Morlocks"]), "different words have ever followed just 'Morlocks'")
```

A dictionary key does not have to be a single word. It can be a pair of
words, kept together as one key. A chain keyed on pairs remembers the
last *two* words, one more than before.

To keep two words together, we write them in round brackets:
`("the", "Morlocks")`. A *tuple* is a group of values in round brackets,
like this one. A tuple is like a list that cannot be changed after it is
made. Because it cannot change, Python lets us use a tuple as a
dictionary key. A list cannot be a key.

```python exec
id: keying-on-more-than-one-word-3
order2 = {}
for w1, w2, w3 in zip(words, words[1:], words[2:]):
    key = (w1, w2)
    order2.setdefault(key, {})
    order2[key][w3] = order2[key].get(w3, 0) + 1

print(len(order2[("the", "Morlocks")]), "different words have ever followed 'the Morlocks' specifically")
```

This loop is the one from `order1` with one more list in the `zip`. It
moves through the book three words at a time. The first two words make
the key. The third word is the one that followed them.

What do the two cells print? `order1["Morlocks"]` has 24 different words
that have followed `"Morlocks"`. Sometimes the sentence continues with what
the Morlocks did, like `"had"` or `"came"`. Sometimes it is just `"and"`
or `"were"`. When we ask about `"the Morlocks"` instead, the number
drops to 17. The extra word of context does more than add memory. It
removes some of the choices that only made sense after a different
word.

These runs of words have a name. A run of $n$ words in a row is an
*n-gram*. A pair of words is a 2-gram, also called a *bigram*, and a run
of three words is a 3-gram, or *trigram*. `order1` counts every bigram in
the book. `order2` counts every trigram. A Markov chain built this way is
often called an *n-gram model*.

`order1` has 6,991 keys, one for every different word in the book. Does
`order2` have more keys than that?

```python exec
id: keying-on-more-than-one-word-4
print(len(order1), len(order2))
print(len(order2) > len(order1))
```

```predict
type: choice

What will the last line print?

- True
- False
  - A pair of words is more particular than one word, so there should be
    fewer pairs than words.
```

Each word in the book can be followed by many different words, and
every one of those makes a different pair. So there are more than three
times as many keys. There is still a limit: the book has only 32,465
places where three words in a row begin, and `order2` cannot have more
keys than that.

## Comparing what each one writes

`generate()` from the last tutorial walks an `order1` chain one word at a
time. Here it is again as `generate1`, beside a `generate2` for the
`order2` chain.

```python exec
id: comparing-what-each-one-writes-1
import random

random.seed(1)    # change the 1 to any other number for a different run

def generate1(start_word, steps):
    result = [start_word]
    current = start_word
    for _ in range(steps):
        if current not in order1:
            break
        candidates = order1[current]
        current = random.choices(list(candidates.keys()), weights=list(candidates.values()))[0]
        result.append(current)
    return " ".join(result)

def generate2(w1, w2, steps):
    result = [w1, w2]
    current = (w1, w2)
    for _ in range(steps):
        if current not in order2:
            break
        candidates = order2[current]
        next_word = random.choices(list(candidates.keys()), weights=list(candidates.values()))[0]
        result.append(next_word)
        current = (current[1], next_word)
    return " ".join(result)

print("order1:", generate1("the", 20))
print("order2:", generate2("the", "Morlocks", 20))
```

Run it with another seed. Then start `generate2` from a pair of your
own, such as `("the", "Time")`. What happens if you choose a pair that
is not in the book?

<details class="dl-answer"><summary>How generate2 moves its key</summary>

The key is a pair. After `generate2` chooses a new word, the line
`current = (current[1], next_word)` moves the key forward by one word.
`current[1]` is the second word of the old key, and `next_word` is the
word just chosen. So the key drops its older word and adds the new one.
It always holds the *last* two words, and it never grows longer.

A pair that is not in the book is not a key in `order2`, so the loop
stops before it begins, and `generate2` returns only your two words.

</details>

Which line reads more like real English? `random.seed(1)` fixes where
the random choices start, so the cell gives the same two lines every
time it runs. Seed 1 gives this:

> order1: the machine below grew scattered, as the eyes glared at work as
> the heavy smell, the appearances of fire. Upon these
>
> order2: the Morlocks taken my Time Machine and the latter, because it
> happens that our consciousness moves intermittently in one hand and the

The `order2` line reads more like real English, at least in stretches.
Why? The first key, `("the", "Morlocks")`, has 17 possible next words.
But 11 of the 20 pairs after it have only one recorded next word in the
whole book. For long stretches, the chain is not choosing at all.

"and the latter, because it happens that our consciousness moves
intermittently in one" is not a coincidence. Those 13 words are in the
book, in that order. Can we check? `in` looks for an exact match, so we
have to be careful. Guess before you run the cell: which line will say
True?

```python exec
id: comparing-what-each-one-writes-check
phrase = "and the latter, because it happens that our consciousness moves intermittently in one"
print(phrase in book)
print(phrase in " ".join(words))
```

The first line says False. In `book`, a line break sits between two of
those words, where the phrase has a space. The second line joins the
words with single spaces, the same way `generate2` does, and says True.

The more context a chain remembers, the more often it recites a piece of
the book it has already seen. With less context, it combines pieces of
the book in new ways.

## Two words from your book

Can you write `chain_from2(words)`, which builds an order-2 chain from
any list of words? Keep your book's chain as `my_order2`. Then, with
`random.seed(1)`, generate 20 words from the pair given for your book,
and look for a stretch of it that is copied from the book. You can check
a stretch with `in " ".join(my_words)`.

<div class="dl-world" data-world="the-time-machine">

Start from `("Time", "Traveller")`. How many different words follow that
pair?

```python exec
id: two-words-from-your-book-1--the-time-machine
mine = await load_text("the-time-machine.txt")
start = mine.find("*** START OF")
end = mine.find("*** END OF")
my_words = mine[mine.index("\n", start):end].split()


def chain_from2(words):
    """An order-2 chain: each pair of words, and the words that followed it."""
    # Your code here.
```

```hint
`chain_from2` is the `order2` loop above, inside a function that returns
the chain. To generate, the key is always the last two words of the
sentence so far: `(sentence[-2], sentence[-1])`.
```

```inputs
len(my_order2)
len(my_order2[("Time", "Traveller")])
```

```solution
def chain_from2(words):
    """An order-2 chain: each pair of words, and the words that followed it."""
    chain = {}
    for w1, w2, w3 in zip(words, words[1:], words[2:]):
        chain.setdefault((w1, w2), {})
        chain[(w1, w2)][w3] = chain[(w1, w2)].get(w3, 0) + 1
    return chain


my_order2 = chain_from2(my_words)
random.seed(1)
sentence = ["Time", "Traveller"]
for _ in range(20):
    followers = my_order2[(sentence[-2], sentence[-1])]
    sentence.append(random.choices(list(followers.keys()), weights=list(followers.values()))[0])
print(" ".join(sentence))
---
The chain has the same 22,457 keys as `order2`, and 28 different words
follow `("Time", "Traveller")`. With seed 1 it writes "Time Traveller
smiled. “Are you so sure we can the spoke of a very bright red star that
was over. As the". Its first 9 words are in the book, in that order.
```

</div>

<div class="dl-world" data-world="dracula">

Start from `("the", "Count")`. How many different words follow that
pair?

```python exec
id: two-words-from-your-book-1--dracula
mine = await load_text("dracula.txt")
start = mine.find("*** START OF")
end = mine.find("*** END OF")
my_words = mine[mine.index("\n", start):end].split()


def chain_from2(words):
    """An order-2 chain: each pair of words, and the words that followed it."""
    # Your code here.
```

```hint
`chain_from2` is the `order2` loop above, inside a function that returns
the chain. To generate, the key is always the last two words of the
sentence so far: `(sentence[-2], sentence[-1])`.
```

```inputs
len(my_order2)
len(my_order2[("the", "Count")])
```

```solution
def chain_from2(words):
    """An order-2 chain: each pair of words, and the words that followed it."""
    chain = {}
    for w1, w2, w3 in zip(words, words[1:], words[2:]):
        chain.setdefault((w1, w2), {})
        chain[(w1, w2)][w3] = chain[(w1, w2)].get(w3, 0) + 1
    return chain


my_order2 = chain_from2(my_words)
random.seed(1)
sentence = ["the", "Count"]
for _ in range(20):
    followers = my_order2[(sentence[-2], sentence[-1])]
    sentence.append(random.choices(list(followers.keys()), weights=list(followers.values()))[0])
print(" ".join(sentence))
---
*Dracula*'s chain has 85,621 two-word keys, and 55 different words
follow `("the", "Count")`. With seed 1 it writes "the Count stayed with
me, drowned in the limitations of sympathetic understanding. He did not
sleep all the time come for you,". The 9 words "in the limitations of
sympathetic understanding. He did not" are in the book, in that order.
```

</div>

<div class="dl-world" data-world="dubliners">

Start from `("Mr", "Duffy")`, from the story *A Painful Case*. How many
different words follow that pair?

```python exec
id: two-words-from-your-book-1--dubliners
mine = await load_text("dubliners.txt")
start = mine.find("*** START OF")
end = mine.find("*** END OF")
my_words = mine[mine.index("\n", start):end].split()


def chain_from2(words):
    """An order-2 chain: each pair of words, and the words that followed it."""
    # Your code here.
```

```hint
`chain_from2` is the `order2` loop above, inside a function that returns
the chain. To generate, the key is always the last two words of the
sentence so far: `(sentence[-2], sentence[-1])`.
```

```inputs
len(my_order2)
len(my_order2[("Mr", "Duffy")])
```

```solution
def chain_from2(words):
    """An order-2 chain: each pair of words, and the words that followed it."""
    chain = {}
    for w1, w2, w3 in zip(words, words[1:], words[2:]):
        chain.setdefault((w1, w2), {})
        chain[(w1, w2)][w3] = chain[(w1, w2)].get(w3, 0) + 1
    return chain


my_order2 = chain_from2(my_words)
random.seed(1)
sentence = ["Mr", "Duffy"]
for _ in range(20):
    followers = my_order2[(sentence[-2], sentence[-1])]
    sentence.append(random.choices(list(followers.keys()), weights=list(followers.values()))[0])
print(" ".join(sentence))
---
*Dubliners*' chain has 43,092 two-word keys, and only 6 different words
follow `("Mr", "Duffy")`. With seed 1 it writes "Mr Duffy abhorred
anything which betokened physical or mental disorder. A mediæval doctor
would have gone up on the area railings. The". Its first 15 words are
Joyce's own, in that order.
```

</div>

<div class="dl-world" data-world="irish-fairy-tales">

Start from `("the", "Fianna")`, Fionn's band of warriors. How many
different words follow that pair?

```python exec
id: two-words-from-your-book-1--irish-fairy-tales
mine = await load_text("irish-fairy-tales.txt")
start = mine.find("*** START OF")
end = mine.find("*** END OF")
my_words = mine[mine.index("\n", start):end].split()


def chain_from2(words):
    """An order-2 chain: each pair of words, and the words that followed it."""
    # Your code here.
```

```hint
`chain_from2` is the `order2` loop above, inside a function that returns
the chain. To generate, the key is always the last two words of the
sentence so far: `(sentence[-2], sentence[-1])`.
```

```inputs
len(my_order2)
len(my_order2[("the", "Fianna")])
```

```solution
def chain_from2(words):
    """An order-2 chain: each pair of words, and the words that followed it."""
    chain = {}
    for w1, w2, w3 in zip(words, words[1:], words[2:]):
        chain.setdefault((w1, w2), {})
        chain[(w1, w2)][w3] = chain[(w1, w2)].get(w3, 0) + 1
    return chain


my_order2 = chain_from2(my_words)
random.seed(1)
sentence = ["the", "Fianna"]
for _ in range(20):
    followers = my_order2[(sentence[-2], sentence[-1])]
    sentence.append(random.choices(list(followers.keys()), weights=list(followers.values()))[0])
print(" ".join(sentence))
---
*Irish Fairy Tales*' chain has 40,521 two-word keys, and 24 different
words follow `("the", "Fianna")`. With seed 1 it writes "the Fianna na
h-Eirinn. Tales of how he ran or wriggled through the door I loved and
would look and remark on". Its first 8 words are in the book, in that
order.
```

</div>

<div class="dl-world" data-world="treasure-island">

Start from `("the", "captain")`. How many different words follow that
pair?

```python exec
id: two-words-from-your-book-1--treasure-island
mine = await load_text("treasure-island.txt")
start = mine.find("*** START OF")
end = mine.find("*** END OF")
my_words = mine[mine.index("\n", start):end].split()


def chain_from2(words):
    """An order-2 chain: each pair of words, and the words that followed it."""
    # Your code here.
```

```hint
`chain_from2` is the `order2` loop above, inside a function that returns
the chain. To generate, the key is always the last two words of the
sentence so far: `(sentence[-2], sentence[-1])`.
```

```inputs
len(my_order2)
len(my_order2[("the", "captain")])
```

```solution
def chain_from2(words):
    """An order-2 chain: each pair of words, and the words that followed it."""
    chain = {}
    for w1, w2, w3 in zip(words, words[1:], words[2:]):
        chain.setdefault((w1, w2), {})
        chain[(w1, w2)][w3] = chain[(w1, w2)].get(w3, 0) + 1
    return chain


my_order2 = chain_from2(my_words)
random.seed(1)
sentence = ["the", "captain"]
for _ in range(20):
    followers = my_order2[(sentence[-2], sentence[-1])]
    sentence.append(random.choices(list(followers.keys()), weights=list(followers.values()))[0])
print(" ".join(sentence))
---
*Treasure Island*'s chain has 43,516 two-word keys, and 37 different
words follow `("the", "captain")`. With seed 1 it writes "the captain
held his Bible, and that’s what’s wrong with you. But these men down
there, they couldn’t keep their word--no, not". The 12 words from "you."
to "not" are in the book, in that order.
```

</div>

## Reflection

More context makes a chain sound more like the book it learned from, but
it writes less that is new. Less context makes it sound less like the
book, and it writes more new combinations. Neither one is *better*.
Suppose you want a chain that writes in an author's own voice. Then you
want more context. For a chain that surprises you, you want less.

A challenge: make one sentence with `order1` and one with `order2`, from
the same book and the same seed. Show both to a classmate without saying
which is which. Can they tell? What gave it away?

```python challenge
import random

raw = await load_text("the-time-machine.txt")
start = raw.find("*** START OF")
end = raw.find("*** END OF")
words = raw[raw.index("\n", start):end].split()

order1 = {}
for w1, w2 in zip(words, words[1:]):
    order1.setdefault(w1, {})
    order1[w1][w2] = order1[w1].get(w2, 0) + 1

order2 = {}
for w1, w2, w3 in zip(words, words[1:], words[2:]):
    order2.setdefault((w1, w2), {})
    order2[(w1, w2)][w3] = order2[(w1, w2)].get(w3, 0) + 1

random.seed(1)                 # your seed
one = ["the"]                  # your start word
two = ["the", "Time"]          # your start pair
for _ in range(20):
    followers = order1[one[-1]]
    one.append(random.choices(list(followers.keys()), weights=list(followers.values()))[0])
    followers = order2[(two[-2], two[-1])]
    two.append(random.choices(list(followers.keys()), weights=list(followers.values()))[0])
print("A:", " ".join(one))
print("B:", " ".join(two))
```

The next tutorial, [Writing style: comparing two writers with Markov
chains](tutorial:whose-voice-is-this), asks how far that can go. Can a
chain tell which writer wrote a passage it has never seen?

## Where to read more

3Blue1Brown (2024). *Large Language Models explained briefly.*
<https://www.youtube.com/watch?v=LPZh9BOjkQs>. A chatbot also chooses each
next word from the words before it, but it uses far more of them than
two or three. Grant Sanderson shows how, in eight minutes.
