---
title: "Dictionaries: looking things up by name"
year: "2026-2027"
version: 2026.10.10.1
worlds:
  secret-messages: Codes and hidden messages, the kind spies and puzzle-setters make.
  pixel-art: Pictures made of small squares, the way a screen draws them.
covers:
  making-a-dictionary:
    touches: [PDP-LO4]
---

# Dictionaries: looking things up by name

Here is a small phrasebook, kept as a dictionary. Each Irish word is
joined to its English word. What will the cell print?

```python exec
id: a-phrasebook-1
phrasebook = {"madra": "dog", "capall": "horse", "bó": "cow", "uan": "lamb"}
print(phrasebook["madra"], phrasebook["bó"], phrasebook["capall"])
```

```predict
What will it print?

- dog cow horse
  - Each Irish word is looked up, and its English word comes back.
- madra bó capall
  - The three words are printed as they are.
- An error
  - A dictionary is looked up by position, like a list.
```

It prints `dog cow horse`. A *list*{.term} finds a value by its position. A
dictionary finds a value by a name we choose, here an Irish word. Most of
this page is about that one change, and what it makes easy: a phrasebook,
a price list, and counting how often each thing appears. You will make
dictionaries, look things up in them, and use them to count.

Under the title is a box called "Choose a world". The explanations on this
page are the same in both worlds. Only the tasks follow your choice.

## Making a dictionary

A *dictionary* is a collection of pairs. Each pair joins a *key*, the name
we look something up by, to a *value*, what is stored under that key. We
write a dictionary like this:

- curly brackets, `{` and `}`, go round the whole dictionary;
- a colon, `:`, joins each key to its value;
- commas go between the pairs.

```python exec
id: making-a-dictionary-1
sizes = {"S": "small", "M": "medium", "L": "large"}
print(sizes)
print(sizes["M"])
print(len(sizes))
```

To look up a value, write the dictionary's name, then the key in square
brackets: `sizes["M"]`. The brackets are the ones a list uses for an
*index*{.term}, with a key inside them where a list would have a position. `len()`
counts the pairs. Python shows the strings with single quotes when it
prints a dictionary. Single and double quotes mean the same thing.

The name comes from a paper dictionary. You look up a word, and find its
meaning beside it. Each key appears only once in a dictionary, but two keys
can share a value. A value can be any type, a list included.

### Your turn

<div class="dl-world" data-world="secret-messages">

This key joins each plain letter to its code letter. Can you set `coded` to
the word BEAD, written in the code this key gives?

```python exec
id: your-turn-1--secret-messages
key = {"A": "Q", "B": "W", "C": "E", "D": "R", "E": "T"}
coded = ""
print(coded)
```

```inputs
coded
```

```hint
`key["B"]` gives the code letter for B. How can you join four code letters
into one word?
```

```solution
key = {"A": "Q", "B": "W", "C": "E", "D": "R", "E": "T"}
coded = key["B"] + key["E"] + key["A"] + key["D"]
print(coded)
---
WTQR. Four lookups, one for each letter. A loop could do the looking up
for a word of any length, and it does, further down.
```

</div>

<div class="dl-world" data-world="pixel-art">

A screen makes each colour from red, green and blue, from 0 to 255. Here a
palette keeps each colour as a list of the three. Can you set `green` to
the green part of the colour `"o"`?

```python exec
id: your-turn-1--pixel-art
palette = {"#": [0, 0, 0], ".": [255, 255, 255], "o": [255, 165, 0]}
green = 0
print(green)
```

```inputs
green
```

```hint
`palette["o"]` is a list of three numbers. Which index is the green one?
```

```solution
palette = {"#": [0, 0, 0], ".": [255, 255, 255], "o": [255, 165, 0]}
green = palette["o"][1]
print(green)
---
165. `palette["o"]` is the list `[255, 165, 0]`, orange, and `[1]` picks
its second number. Two lookups in a row: first by key, then by index.
```

</div>

## Adding and changing values

A dictionary is *mutable*{.term}, like a list. The two middle lines here have the
same shape. How many pairs will the dictionary have at the end?

```python exec
id: adding-and-changing-values-1
sizes = {"S": "small", "M": "medium", "L": "large"}
sizes["XL"] = "extra large"
sizes["M"] = "middle"
print(sizes)
print(len(sizes))
```

```predict
type: number

How many pairs will it have at the end?
```

Four. `"XL"` was not a key yet, so Python added a new pair. `"M"` was a key
already, so Python replaced its value. The two lines look the same. The
only difference is whether the key is already there. A dictionary keeps
its pairs in the order they were added, so a new pair goes at the end.

A value can be used to calculate its own new value, the way
`total = total + n` did in
[Repeating steps with loops](tutorial:repeating-yourself):

```python exec
id: adding-and-changing-values-2
orders = {"tea": 4, "coffee": 2}
orders["tea"] = orders["tea"] + 1
print(orders)
```

Python calculates the right-hand side first. It reads 4, and adds 1. Then
it stores 5 back under `"tea"`. We use this further down to count things.

### Your turn

<div class="dl-world" data-world="secret-messages">

Can you build `key`, a dictionary for the whole Caesar shift of 3, with a
loop? Each capital letter is a key, and the letter three places along is
its value. Then, with a second loop, set `coded` to the word HELLO in that
code.

```python exec
id: your-turn-2--secret-messages
shift = 3
key = {}

coded = ""
print(coded)
```

```inputs
len(key)
coded
```

```hint
`{}` is an empty dictionary. For each number from 0 to 25, the key is
`chr(number + ord("A"))`. What is its value?
```

```solution
shift = 3
key = {}
for number in range(26):
    key[chr(number + ord("A"))] = chr((number + shift) % 26 + ord("A"))

coded = ""
for letter in "HELLO":
    coded = coded + key[letter]
print(coded)
---
KHOOR. The arithmetic happens once, when the key is built. After that,
coding a letter is one lookup, and the key could be any table at all, not
only a shift.
```

</div>

<div class="dl-world" data-world="pixel-art">

A screen draws a shade of grey as a brightness from 0 to 255. Can you build
`shades`, a dictionary from a level, 0 to 4, to a brightness, with a loop?
Level 0 has brightness 0, and level 4 has 255. Each level in between is
255 / 4 brighter than the one before, rounded to a whole number. Then add a
level 5, which is also 255.

```python exec
id: your-turn-2--pixel-art
shades = {}

print(shades)
```

```inputs
shades
```

```hint
`{}` is an empty dictionary. For each level from 0 to 4, the brightness is
`round(level * 255 / 4)`. How do you store it under that level?
```

```solution
shades = {}
for level in range(5):
    shades[level] = round(level * 255 / 4)
shades[5] = 255
print(shades)
---
`{0: 0, 1: 64, 2: 128, 3: 191, 4: 255, 5: 255}`. The keys here are whole
numbers, not strings. A key can be any value that cannot change: a number
or a string, but not a list.
```

</div>

## Checking whether a key is there

What happens if we ask for a key that is not in the dictionary? This cell
is meant to stop. Read the last line of what it prints.

```python exec
id: checking-whether-a-key-is-there-1
sizes = {"S": "small", "M": "medium", "L": "large"}
print(sizes["XL"])
```

A `KeyError` means that Python looked for a key and did not find it. The
last line names the key it looked for, here `'XL'`. Often the key is there,
spelled another way. `"m"` and `"M"` are two different keys.

We can ask before we look. `in` checks whether a key is in a dictionary,
and gives `True` or `False`. What will the last line print?

```python exec
id: checking-whether-a-key-is-there-2
sizes = {"S": "small", "M": "medium", "L": "large"}
print("S" in sizes)
print("XL" in sizes)
print("small" in sizes)
```

```predict
What will the last line print?

- True
  - small is in the dictionary: it is S's value.
- False
  - `in` checks the keys, and small is a value.
```

It prints `False`. `in` checks the keys of a dictionary, and does not look
at the values. With `if`, it lets a *program*{.term} decide before it looks
anything up:

```python exec
id: checking-whether-a-key-is-there-3
sizes = {"S": "small", "M": "medium", "L": "large"}
size = "XL"
if size in sizes:
    print(sizes[size])
else:
    print(size, "is not a size we sell")
```

### Looking up with a default

`.get()` does that check and the lookup in one. `sizes.get(size, default)`
returns the size's value if it is a key. If it is not, it returns
the *default*, the value we choose to get when nothing else is there.

```python exec
id: looking-up-with-a-default-1
sizes = {"S": "small", "M": "medium", "L": "large"}
print(sizes.get("S", "?"))
print(sizes.get("XL", "?"))
print(sizes.get("XL"))
```

With no default, `.get()` returns `None`, Python's value for "nothing".
Which should you use? It depends on what a missing key means. If it is a
mistake, `sizes["XL"]` says so at once, with a `KeyError`. If it is normal,
such as a size we do not stock, `.get()` with a sensible default lets the
program continue.

## Looping over a dictionary

A `for` loop can loop over a dictionary. Each time round, it gives a key.
`.items()` gives each pair instead, as a key and a value together, the way
`enumerate()` gave an index and an *element*{.term} in
[Lists and looping over them](tutorial:lists-and-sequences).

```python exec
id: looping-over-a-dictionary-1
sizes = {"S": "small", "M": "medium", "L": "large"}
for size in sizes:
    print(size)
for size, name in sizes.items():
    print(size, "is", name)
```

### Your turn

<div class="dl-world" data-world="secret-messages">

A key codes a message. To decode it, we need the key reversed: each code
letter is a key, and the plain letter is its value. Can you build
`decode_key` from `key` with a loop? Then, with a second loop, set `plain`
to the decoded `message`.

```python exec
id: your-turn-3--secret-messages
key = {"A": "Q", "B": "W", "C": "E", "D": "R", "E": "T"}
decode_key = {}

message = "EQRT"
plain = ""
print(plain)
```

```inputs
decode_key
plain
```

```hint
`for letter, code in key.items():` gives each pair. In `decode_key`, which
of the two is the key, and which the value?
```

```solution
key = {"A": "Q", "B": "W", "C": "E", "D": "R", "E": "T"}
decode_key = {}
for letter, code in key.items():
    decode_key[code] = letter

message = "EQRT"
plain = ""
for code in message:
    plain = plain + decode_key[code]
print(plain)
---
CADE, a name. Reversing a key like this works only because no two
letters share a code letter. If two did, the second would overwrite the
first, and the message could not be read back.
```

</div>

<div class="dl-world" data-world="pixel-art">

A palette joins each character in a picture to a colour's name. To write
a picture from colour names, we need the palette reversed: each colour's
name is a key, and its character is the value. Can you build `symbol_for`
from `palette` with a loop? Then, with a second loop, set `row` to the
characters for the colours in `colours`.

```python exec
id: reverse-a-palette--pixel-art
palette = {"#": "black", ".": "white", "r": "red"}
symbol_for = {}

colours = ["red", "black", "red", "white"]
row = ""
print(row)
```

```inputs
symbol_for
row
```

```hint
`for character, name in palette.items():` gives each pair. In
`symbol_for`, which of the two is the key, and which the value?
```

```solution
palette = {"#": "black", ".": "white", "r": "red"}
symbol_for = {}
for character, name in palette.items():
    symbol_for[name] = character

colours = ["red", "black", "red", "white"]
row = ""
for name in colours:
    row = row + symbol_for[name]
print(row)
---
`r#r.`. Reversing a palette like this works only because no two characters
share a colour. If two did, the second would overwrite the first, and a
colour name could not be turned back into one character.
```

</div>

## Counting things

How often does each letter appear in a piece of text? We do not know the
letters before we start, so we cannot make a *variable*{.term} for each. A
dictionary can do it. Each letter is a key, and its count is the value.

```
START with an empty dictionary
FOR each letter in the text
    IF the letter is already a key: ADD 1 to its count
    OTHERWISE: store the letter with a count of 1
DISPLAY the dictionary
```

Before you run the cell, can you count the Es by hand?

```python exec
id: counting-things-1
text = "MEET ME BY THE TREE"
counts = {}
for letter in text:
    if letter in counts:
        counts[letter] = counts[letter] + 1
    else:
        counts[letter] = 1
print(counts)
```

This is the *accumulator pattern*{.term} again, with one accumulator for each key.
`.get()` makes the *loop*{.term} shorter. Why is the default 0 here?

```python exec
id: counting-things-2
text = "MEET ME BY THE TREE"
counts = {}
for letter in text:
    counts[letter] = counts.get(letter, 0) + 1
print(counts)
```

The first time a letter appears, it has no count yet, so `.get()`
returns 0, and 0 + 1 stores a count of 1. After that, `.get()` returns the
count so far. Both cells make the same dictionary.

### Your turn

Can you write `count_letters(text)`, which returns a dictionary of how
often each capital letter appears in `text`, and ignores everything
else?

```python exec
id: your-turn-4
def count_letters(text):
    counts = {}
    return counts
```

```inputs
guess: yes
count_letters("BANANA")
count_letters("MEET ME")        # the space is left out
count_letters("")
```

```hint
The loop we just wrote counts every character. `.isupper()`, from
[Making decisions with if, elif and else](tutorial:making-decisions), can
decide which characters to count.
```

```solution
def count_letters(text):
    counts = {}
    for character in text:
        if character.isupper():
            counts[character] = counts.get(character, 0) + 1
    return counts
---
`count_letters("BANANA")` gives `{'B': 1, 'A': 3, 'N': 2}`. An empty text
gives an empty dictionary, `{}`: no letters, so no counts.
```

<div class="dl-world" data-world="secret-messages">

In English, E is the most common letter, then T and A. This is a weakness
in every Caesar shift. The most common letter in a coded message is
probably a coded E. Which letter is most common in this message? Can you set
`most`?

```python exec
id: your-turn-5--secret-messages
message = "WKH HQHPB LV PHHWLQJ DW WKH EULGJH DW WKUHH"
counts = {}
for character in message:
    if character.isupper():
        counts[character] = counts.get(character, 0) + 1

most = ""
print(most, counts.get(most))
```

```inputs
most
```

```hint
Loop over `counts.items()`, and keep the letter with the biggest count so
far.
```

```solution
message = "WKH HQHPB LV PHHWLQJ DW WKH EULGJH DW WKUHH"
counts = {}
for character in message:
    if character.isupper():
        counts[character] = counts.get(character, 0) + 1

most = ""
for letter, count in counts.items():
    if count > counts.get(most, 0):
        most = letter
print(most, counts.get(most))
---
H, nine times. If H is a coded E, the shift is 3, because H is three
letters after E. Decode it with a shift of 3, and see whether it reads as
English.
```

</div>

<div class="dl-world" data-world="pixel-art">

Which character does this picture use most? The cell has counted every
character already. Can you set `most` to the character with the biggest
count?

```python exec
id: most-used-character--pixel-art
picture = [
    "..rr..",
    ".rrrr.",
    "rr##rr",
    ".rrrr.",
]
counts = {}
for row in picture:
    for character in row:
        counts[character] = counts.get(character, 0) + 1

most = ""
print(most, counts.get(most))
```

```inputs
most
```

```hint
Loop over `counts.items()`, and keep the character with the biggest count
so far.
```

```solution
picture = [
    "..rr..",
    ".rrrr.",
    "rr##rr",
    ".rrrr.",
]
counts = {}
for row in picture:
    for character in row:
        counts[character] = counts.get(character, 0) + 1

most = ""
for character, count in counts.items():
    if count > counts.get(most, 0):
        most = character
print(most, counts.get(most))
---
`r`, 14 times out of 24. An image file can store a picture this way: a
palette of the colours it uses, and each pixel as a short key into it.
```

</div>

## Dictionary or list?

Lists and dictionaries both keep many values together. Here they are side
by side.

| | List | Dictionary |
|---|---|---|
| We find a value by | its position: `row[0]` | its key: `key["A"]` |
| We write it with | square brackets, `[ ]` | curly brackets, `{ }` |
| It is a good choice when | order matters, or the values have no names | each value has a name we look it up by |
| An example | the scores in a game, in order | a phone's contacts |
| A missing item gives | `IndexError` | `KeyError` |

One question decides most cases. Will you look values up by a name? If so,
use a dictionary. If you care about the order, or you only use the values
one by one, use a list. And the two work together. A dictionary's value
can be a list too.

For each of these, would you use a list or a dictionary? Write your
answer, and your reason, as a *comment*{.term} in the cell.

1. The ten songs in a playlist, in the order they play.
2. The number of goals each player on a team has scored.
3. The rainfall on each day of March.
4. A phrasebook that gives the English word for each Irish word.
5. The people waiting in a queue.

```python exec
id: dictionary-or-list-1
# 1.
# 2.
# 3.
# 4.
# 5.
```

<details class="dl-answer"><summary>one way to answer</summary>

1. A list. The order the songs play in matters most.
2. A dictionary. Each player's name is the key, and their goals are the
   value.
3. A list. The position is the day: index 0 is the 1st of March.
4. A dictionary. You look up an Irish word, and find the English word
   under it.
5. A list. A queue is all about order: who is first, and who is next.

Some could be either. The rainfall could be a dictionary with the date
as its key. Your reason matters more than which one you picked.

</details>

## Looking back

A list answers "what is at position 3?", and a dictionary answers "what
goes with this name?". Think of a program you use every day: a phone's
contacts, a shopping app, a game. Where do you think it keeps values under
names, and where in order?

<div class="dl-world" data-world="secret-messages">

A challenge: crack a Caesar shift with no key at all. Count the letters in
the coded message, guess that the most common one is a coded E, find
the shift, and decode it. What if the guess is wrong? Try T next, then A.

```python challenge
# Crack this Caesar shift: count, guess E, find the shift, decode.
message = "WKLV LV D PHVVDJH IURP WKH IURQW OLQH"
counts = {}
for character in message:
    if character.isupper():
        counts[character] = counts.get(character, 0) + 1
print(counts)
```

</div>

<div class="dl-world" data-world="pixel-art">

A challenge: draw a bar chart of a picture's colours. Count the characters
in the picture, and print each colour's name with one `*` for every pixel
of it. What should it print for a character that is not in the palette?

```python challenge
# Count the characters, then print each colour's name and a row of stars.
palette = {"#": "black", ".": "white", "r": "red"}
picture = [
    "..rr..",
    ".rrrr.",
    "rr##rr",
    ".rrrr.",
]
counts = {}
for row in picture:
    for character in row:
        counts[character] = counts.get(character, 0) + 1
print(counts)
```

</div>

The next page, [A program of your own](tutorial:a-program-of-your-own), is
a chance to build something with everything so far.

## Where to read more

Everything here is covered elsewhere too, often in a form that will suit you
better than this one.

Python Software Foundation. *The Python Tutorial*, section 5.5,
"Dictionaries". <https://docs.python.org/3/tutorial/datastructures.html#dictionaries>.
This is the official reference for dictionaries, including the methods this page
does not cover.

<div class="dl-world" data-world="secret-messages">

Singh, S. (1999). *The Code Book: The Secret History of Codes and
Codebreaking*. Fourth Estate. Chapter 1 tells how Arab scholars in the
ninth century cracked substitution ciphers by counting letters, which is
the challenge above, done by hand.

</div>

<div class="dl-world" data-world="pixel-art">

Wikipedia. *Indexed color*. <https://en.wikipedia.org/wiki/Indexed_color>.
It describes the palette method used in the tasks above: a picture stores a
short number for each pixel, and a table of the real colours.

</div>

SimonDev (2021). *Hash Tables, Associative Arrays, and Dictionaries.*
<https://www.youtube.com/watch?v=S5NY1fqisSY>. This video shows how a
dictionary finds a value from its key without looking at everything, and what happens
when two keys land in the same place. About twelve minutes.
