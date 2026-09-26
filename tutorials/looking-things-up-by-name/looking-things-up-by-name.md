---
title: "Dictionaries: looking things up by name"
year: "2026-2027"
version: 2026.09.26.1
worlds:
  secret-messages: Codes and hidden messages, the kind spies and puzzle-setters make.
  pixel-art: Pictures made of small squares, the way a screen draws them.
covers:
  making-a-dictionary:
    touches: [PDP-LO4]
---

# Dictionaries: looking things up by name

Two spies share a key: a table that says which letter stands for which.
Here are its first five letters, as a dictionary. What will the cell
print?

```python exec
id: a-shared-key-1
key = {"A": "Q", "B": "W", "C": "E", "D": "R", "E": "T"}
print(key["C"] + key["A"] + key["B"])
```

```predict
What will it print?

- EQW
  - Each letter is looked up, and its code letter comes back.
- CAB
  - The three letters are joined as they are.
- An error
  - A dictionary is looked up by position, like a list.
```

It prints `EQW`: CAB, in code. A list finds a value by its position. A
dictionary finds a value by a name we choose, here a letter. Most of this
page is about that one change, and what it makes easy: a cipher's key, a
picture's palette, and counting how often each thing turns up.

## Making a dictionary

A *dictionary* is a collection of pairs. Each pair joins a *key*, the name
we look something up by, to a *value*, what is stored under that key. We
write a dictionary like this:

- curly brackets, `{` and `}`, go round the whole dictionary;
- a colon, `:`, joins each key to its value;
- commas go between the pairs.

```python exec
id: making-a-dictionary-1
palette = {"#": "black", ".": "white", "r": "red"}
print(palette)
print(palette["r"])
print(len(palette))
```

To look up a value, write the dictionary's name, then the key in square
brackets: `palette["r"]`. The brackets are the ones a list uses for an
index, with a key inside them where a list would have a position. `len()`
counts the pairs. Python shows the strings with single quotes when it
prints a dictionary; single and double quotes mean the same thing.

The name comes from a paper dictionary: you look up a word, and find its
meaning beside it. Each key appears only once in a dictionary, but two keys
can share a value. A value can be any type, a list included.

### Your turn

<div class="dl-world" data-world="secret-messages">

Can you set `coded` to the word BEAD, in the code of this key?

```python exec
id: your-turn-1--secret-messages
key = {"A": "Q", "B": "W", "C": "E", "D": "R", "E": "T"}
coded = ""
print(coded)
```

```inputs
coded
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

A dictionary is mutable, like a list. The two middle lines here have the
same shape. How many pairs will the palette have at the end?

```python exec
id: adding-and-changing-values-1
palette = {"#": "black", ".": "white", "r": "red"}
palette["g"] = "green"
palette["r"] = "dark red"
print(palette)
print(len(palette))
```

```predict
type: number

How many pairs will it have at the end?
```

Four. `"g"` was not a key yet, so Python added a new pair. `"r"` was a key
already, so Python replaced its value. The two lines look the same, and
what decides between them is whether the key is already there. A new pair
goes at the end: a dictionary keeps its pairs in the order they were
added.

A value can be used to work out its own new value, the way
`total = total + n` did in
[Repeating steps with loops](tutorial:repeating-yourself):

```python exec
id: adding-and-changing-values-2
counts = {"E": 4, "T": 2}
counts["E"] = counts["E"] + 1
print(counts)
```

Python works out the right-hand side first: it reads 4, and adds 1. Then
it stores 5 back under `"E"`. We use this further down to count things.

### Your turn

<div class="dl-world" data-world="secret-messages">

Can you build `key`, a dictionary for the whole Caesar shift of 3, with a
loop? Each capital letter is a key, and the letter three places along is
its value. Then set `coded` to HELLO in that code, with a second loop.

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

Can you build `shades`, a dictionary from a level, 0 to 4, to a
brightness? Level 0 is 0, level 4 is 255, and the others are in between,
each 255 / 4 more than the last, rounded to a whole number. Then add a
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
key = {"A": "Q", "B": "W", "C": "E"}
print(key["Z"])
```

A `KeyError` means that Python looked for a key and did not find it. The
last line names the key it looked for, here `'Z'`. Often the key is there,
spelled another way: `"a"` and `"A"` are two different keys.

We can ask before we look. `in` checks whether a key is in a dictionary,
and gives `True` or `False`. What will the last line print?

```python exec
id: checking-whether-a-key-is-there-2
key = {"A": "Q", "B": "W", "C": "E"}
print("A" in key)
print("Z" in key)
print("Q" in key)
```

```predict
What will the last line print?

- True
  - Q is in the dictionary: it is A's code letter.
- False
  - `in` checks the keys, and Q is a value.
```

It prints `False`. `in` checks the keys of a dictionary, and does not look
at the values. With `if`, it lets a program decide before it looks
anything up:

```python exec
id: checking-whether-a-key-is-there-3
key = {"A": "Q", "B": "W", "C": "E"}
letter = "Z"
if letter in key:
    print(key[letter])
else:
    print(letter, "is not in the key")
```

### Looking up with a default

`.get()` does that check and the lookup in one. `key.get(letter, default)`
gives back the letter's value if it is a key. If it is not, it gives back
the *default*: the value we choose to get when nothing else is there.

```python exec
id: looking-up-with-a-default-1
key = {"A": "Q", "B": "W", "C": "E"}
print(key.get("A", "?"))
print(key.get("Z", "?"))
print(key.get("Z"))
```

With no default, `.get()` gives back `None`, Python's value for "nothing".
Which should you use? It depends on what a missing key means. If it is a
mistake, `key["Z"]` says so at once, with a `KeyError`. If it is normal,
such as a space in a message, `.get()` with a sensible default carries on.

## Looping over a dictionary

A `for` loop can go through a dictionary. Each time round, it gives a key.
`.items()` gives each pair instead, as a key and a value together, the way
`enumerate()` gave an index and an element in
[Lists and looping over them](tutorial:lists-and-sequences).

```python exec
id: looping-over-a-dictionary-1
palette = {"#": "black", ".": "white", "r": "red"}
for character in palette:
    print(character)
for character, colour in palette.items():
    print(character, "is", colour)
```

### Your turn

<div class="dl-world" data-world="secret-messages">

A key codes a message. To decode it, we need the key the other way round:
each code letter as a key, and the plain letter as its value. Can you
build `decode_key` from `key` with a loop, and use it to set `plain`?

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
CADE, a name. Turning a key round like this works only because no two
letters share a code letter. If two did, the second would overwrite the
first, and the message could not be read back.
```

</div>

<div class="dl-world" data-world="pixel-art">

Can you set `drawn` to this picture with each character replaced by its
colour's name? Use `.get()`, so that a character missing from the palette
shows as `"?"`.

```python exec
id: your-turn-3--pixel-art
palette = {"#": "black", ".": "white", "r": "red"}
picture = ["#r#", ".x."]
drawn = []

print(drawn)
```

```inputs
drawn
```

```hint
Build one row of names at a time. For each character in the row, look its
colour up with `palette.get(character, "?")`. When the row is done, append
it to `drawn`.
```

```solution
palette = {"#": "black", ".": "white", "r": "red"}
picture = ["#r#", ".x."]
drawn = []
for row in picture:
    names = []
    for character in row:
        names.append(palette.get(character, "?"))
    drawn.append(names)
print(drawn)
---
The second row has an `x`, which the palette does not have. With
`palette[character]`, the picture would stop with a `KeyError` halfway
through. With `.get()`, it shows `?` and carries on. Which is better
depends on whether an unknown character is a mistake.
```

</div>

## Counting things

How often does each letter turn up in a piece of text? We do not know the
letters before we start, so we cannot make a variable for each. A
dictionary can: each letter is a key, and its count is the value.

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

This is the accumulator pattern again, with one accumulator for each key.
`.get()` makes the loop shorter. Why is the default 0 here?

```python exec
id: counting-things-2
text = "MEET ME BY THE TREE"
counts = {}
for letter in text:
    counts[letter] = counts.get(letter, 0) + 1
print(counts)
```

The first time a letter turns up, it has no count yet, so `.get()` gives
back 0, and 0 + 1 stores a count of 1. After that, `.get()` gives back the
count so far. Both cells make the same dictionary.

### Your turn

Can you write `count_letters(text)`, which returns a dictionary of how
often each capital letter appears in `text`, and leaves out everything
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
The loop from the cell above counts everything. `.isupper()`, from
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
gives an empty dictionary, `{}`, which is the right answer: no letters,
no counts.
```

<div class="dl-world" data-world="secret-messages">

In English, E is the most common letter, then T and A. That is a crack in
every Caesar shift: the most common letter in a coded message is probably
a coded E. Which letter is most common in this message? Can you set
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
Go through `counts.items()`, and keep the letter with the biggest count so
far, the way you kept the brightest pixel.
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

Which colour does this picture use most? Can you count every character in
it, and set `most` to the most common one?

```python exec
id: your-turn-5--pixel-art
picture = [
    "..rr..",
    ".rrrr.",
    "rr##rr",
    ".rrrr.",
]
counts = {}

most = ""
print(most, counts.get(most))
```

```inputs
most
```

```hint
Two loops: one over the rows, and one over the characters in each row.
Then go through `counts.items()`, and keep the character with the biggest
count so far.
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
| An example | the pixels in a row | a cipher's key |
| A missing item gives | `IndexError` | `KeyError` |

One question settles most cases: will you look values up by a name? If so,
use a dictionary. If you care about the order, or you only go through all
the values one by one, use a list. And the two go together: a dictionary's
value can be a list, as the palette of colours was.

For each of these, would you use a list or a dictionary? Write your
answer, and your reason, as a comment in the cell.

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

1. A list. The order the songs play in is the point.
2. A dictionary. Each player's name is the key, and their goals are the
   value.
3. A list. The position is the day: index 0 is the 1st of March.
4. A dictionary. You look up an Irish word, and find the English word
   under it.
5. A list. A queue is all about order: who is first, and who is next.

Some could go either way. The rainfall could be a dictionary with the date
as its key. A reason that holds up matters more than which one you picked.

</details>

## Looking back

A list answers "what is at position 3?", and a dictionary answers "what
goes with this name?". Think of a program you use every day: a phone's
contacts, a shopping app, a game. Where do you think it keeps values under
names, and where in order?

A challenge: crack a Caesar shift with no key at all. Count the letters in
the coded message, guess that the most common one is a coded E, work out
the shift, and decode it. What if the guess is wrong? Try T next, then A.

```python challenge
# Crack this Caesar shift: count, guess E, work out the shift, decode.
message = "WKLV LV D PHVVDJH IURP WKH IURQW OLQH"
counts = {}
for character in message:
    if character.isupper():
        counts[character] = counts.get(character, 0) + 1
print(counts)
```

The next page, [A program of your own](tutorial:a-program-of-your-own), is
a chance to build something with everything so far: a cipher tool, a
pixel-art maker, or an idea of your own.

## Where to read more

Everything here is covered elsewhere too, often in a form that will suit you
better than this one.

Python Software Foundation. *The Python Tutorial*, section 5.5,
"Dictionaries". <https://docs.python.org/3/tutorial/datastructures.html#dictionaries>.
The official reference for dictionaries, including the methods this page
does not cover.

Singh, S. (1999). *The Code Book: The Secret History of Codes and
Codebreaking*. Fourth Estate. Chapter 1 tells how Arab scholars in the
ninth century cracked substitution ciphers by counting letters, which is
the challenge above, done by hand.

SimonDev (2021). *Hash Tables, Associative Arrays, and Dictionaries.*
<https://www.youtube.com/watch?v=S5NY1fqisSY>. How a dictionary finds a
value from its key without looking through everything, and what happens
when two keys land in the same place. About twelve minutes.
