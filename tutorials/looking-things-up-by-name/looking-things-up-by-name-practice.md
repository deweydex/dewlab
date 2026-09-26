---
title: "Dictionaries: looking things up by name — Practice"
practice_for: looking-things-up-by-name
year: "2026-2027"
version: 2026.09.26.1
worlds:
  secret-messages: Codes and hidden messages, the kind spies and puzzle-setters make.
  pixel-art: Pictures made of small squares, the way a screen draws them.
---

# Dictionaries: looking things up by name — Practice

These problems are on dictionaries, with three from earlier pages. Try each problem
before you open anything under it, and run the cells to test your guesses.

## 1. Five lookups

With `key = {"A": "Q", "B": "W", "C": "E"}`, what does each of these give?
Try them in the cell.

- (a) `key["B"]`
- (b) `len(key)`
- (c) `"W" in key`
- (d) `key.get("D", "?")`
- (e) `key["D"]`

```python exec
id: five-lookups-1
key = {"A": "Q", "B": "W", "C": "E"}
print(key["B"])
```

<details class="dl-answer"><summary>answer</summary>

(a) `'W'`. (b) 3, the number of pairs. (c) `False`, because `in` checks the keys,
and W is a value. (d) `'?'`, the default. (e) A `KeyError: 'D'`.

</details>

## 2. The same key twice

```python exec
id: the-same-key-twice-1
counts = {"E": 1, "T": 4, "E": 2}
print(counts)
```

```predict
What will it print?

- {'E': 1, 'T': 4, 'E': 2}
  - A dictionary keeps every pair it is given.
- {'E': 2, 'T': 4}
  - A key appears once, so the later value replaces the first.
- An error
  - Python will not allow the same key twice.
```

<details class="dl-answer"><summary>why</summary>

`{'E': 2, 'T': 4}`. Each key appears only once, and the second `"E"`
replaces the first one's value, as `counts["E"] = 2` would. Python gives
no warning, so a repeated key can lose a value without you noticing.

</details>

## 3. The first pair

```python exec
id: the-first-pair-1
key = {"A": "Q", "B": "W", "C": "E"}
print(key[0])
```

```predict
What will it print?

- Q
  - `[0]` is the first pair's value, as in a list.
- An error
  - A dictionary has no positions, only keys.
```

<details class="dl-answer"><summary>why</summary>

A `KeyError: 0`. Python looked for the key `0`, and there is none. A
dictionary finds values by key, never by position, even though it keeps
its pairs in order.

</details>

## 4. Two changes

```python exec
id: two-changes-1
counts = {"E": 2}
counts["T"] = counts.get("T", 0) + 1
counts["E"] = counts["E"] + 1
print(counts)
```

```predict
What will it print?

- {'E': 3, 'T': 1}
  - T was new, so it starts at 0 + 1. E goes up from 2.
- {'E': 2, 'T': 1}
  - Only T was added.
- An error
  - T is not in the dictionary, so it cannot be looked up.
```

<details class="dl-answer"><summary>why</summary>

`{'E': 3, 'T': 1}`. `.get("T", 0)` gives 0 for a missing key, so T starts
at 1 with no error. `counts["T"] + 1` would have stopped with a
`KeyError`.

</details>

## 5. How many in all

Can you set `total` to the number of pixels counted in `counts`?

```python exec
id: how-many-in-all-1
counts = {"r": 14, ".": 8, "#": 2}
total = 0

print(total)
```

```inputs
total
```

```solution
title: with what you've met so far
counts = {"r": 14, ".": 8, "#": 2}
total = 0
for character, count in counts.items():
    total = total + count
print(total)
```

```solution
title: a shorter way you'll meet later
counts = {"r": 14, ".": 8, "#": 2}
total = sum(counts.values())
print(total)
---
`.values()` gives the values without the keys, and `sum()` adds them up:
24.
```

## 6. The rarest

Which letter appears least often? Can you set `rarest`?

```python exec
id: the-rarest-1
counts = {"H": 9, "W": 6, "K": 3, "D": 2, "P": 1, "B": 1}
rarest = ""

print(rarest)
```

```inputs
rarest
```

```hint
Start with any letter as the rarest so far. Go through `counts.items()`.
Is this count smaller than the rarest so far?
```

```solution
counts = {"H": 9, "W": 6, "K": 3, "D": 2, "P": 1, "B": 1}
rarest = "H"
for letter, count in counts.items():
    if count < counts[rarest]:
        rarest = letter
print(rarest)
---
P. B has the same count, and `<` keeps the first one it finds. Starting
from `"H"` works because H is a key. Starting from `""` would stop with a
`KeyError`, the first time round.
```

## 7. By first letter

Can you set `groups` to a dictionary that keeps the words in lists, by
their first letter?

```python exec
id: by-first-letter-1
words = ["OTTER", "OWL", "HEDGEHOG", "BAT", "HARE"]
groups = {}

print(groups)
```

```inputs
groups
```

```hint
The first time a letter turns up, its value needs to be a new list. After
that, the word is appended to that list.
```

```solution
words = ["OTTER", "OWL", "HEDGEHOG", "BAT", "HARE"]
groups = {}
for word in words:
    first = word[0]
    if first not in groups:
        groups[first] = []
    groups[first].append(word)
print(groups)
---
`{'O': ['OTTER', 'OWL'], 'H': ['HEDGEHOG', 'HARE'], 'B': ['BAT']}`. The
values are lists, so `append()` changes the list inside the dictionary.
```

## 8. Counting a vote

A class voted for the colour of a poster. Can you set `votes` to how many
votes each colour got?

```python exec
id: counting-a-vote-1
ballots = ["red", "blue", "red", "green", "red", "blue"]
votes = {}

print(votes)
```

```inputs
votes
```

```solution
ballots = ["red", "blue", "red", "green", "red", "blue"]
votes = {}
for colour in ballots:
    votes[colour] = votes.get(colour, 0) + 1
print(votes)
---
`{'red': 3, 'blue': 2, 'green': 1}`. The loop does not need to know the
colours before it starts. A new one gets a count the first time it turns
up.
```

## 9. Two lists into one dictionary

A key has been kept as two lists, in matching order. Can you set `key` to
one dictionary, with each plain letter as a key and its code letter as the
value?

```python exec
id: two-lists-into-one-1
plain = ["A", "B", "C", "D"]
code = ["X", "M", "Q", "L"]
key = {}

print(key)
```

```inputs
key
```

```solution
title: with what you've met so far
plain = ["A", "B", "C", "D"]
code = ["X", "M", "Q", "L"]
key = {}
for index in range(len(plain)):
    key[plain[index]] = code[index]
print(key)
```

```solution
title: a shorter way you'll meet later
plain = ["A", "B", "C", "D"]
code = ["X", "M", "Q", "L"]
key = dict(zip(plain, code))
print(key)
---
Two lists in matching order are easy to break: sort one, and the pairs no
longer match. One dictionary keeps each pair together.
```

## 10. List or dictionary

For each of these, would you use a list or a dictionary? Say why.

1. The moves in a game of chess, in the order they were played.
2. The colour of each character in a pixel-art palette.
3. How many times each word appears in a book.
4. The high scores on a game's leaderboard, best first.

<details class="dl-answer"><summary>one way to answer</summary>

1. A list, because the order matters. 2. A dictionary, because you look a
colour up by its character. 3. A dictionary. Each word is a key, and its
count the value. 4. A list, because the order matters, though each entry might
be a small dictionary holding a name and a score.

</details>

## 11. Letting things through

<div class="dl-world" data-world="secret-messages">

This key has only the letters it needs. Can you write `decode(message,
key)`, which decodes each letter in the key, and leaves anything else, such
as a space, as it is?

```python exec
id: letting-things-through-1--secret-messages
key = {"W": "B", "T": "E", "Q": "A", "R": "D"}

def decode(message, key):
    plain = ""
    return plain
```

```inputs
guess: yes
decode("WTQR", key)
decode("WTQR WTQR", key)
decode("", key)
```

```hint
`key.get(character, character)` gives the character's decoded letter if
it is a key, and the character itself if it is not.
```

```solution
key = {"W": "B", "T": "E", "Q": "A", "R": "D"}

def decode(message, key):
    plain = ""
    for character in message:
        plain = plain + key.get(character, character)
    return plain
---
The default in `.get()` can be the thing being looked up. Here that means
"if there is no code for it, leave it alone".
```

</div>

<div class="dl-world" data-world="pixel-art">

Can you write `brightness(row, shades)`, which turns a row of characters
into a list of brightnesses with the `shades` dictionary, and makes any
character it does not know 0?

```python exec
id: letting-things-through-1--pixel-art
shades = {"#": 255, "+": 128, ".": 32}

def brightness(row, shades):
    values = []
    return values
```

```inputs
guess: yes
brightness("#+.", shades)
brightness("# x", shades)
brightness("", shades)
```

```hint
`shades.get(character, 0)` gives the character's brightness if it is a
key, and 0 if it is not.
```

```solution
shades = {"#": 255, "+": 128, ".": 32}

def brightness(row, shades):
    values = []
    for character in row:
        values.append(shades.get(character, 0))
    return values
---
`brightness("# x", shades)` gives `[255, 0, 0]`: a space and an x are
both unknown, so both are black. Is that right? For a space, probably.
For an x, it might hide a mistake in the picture.
```

</div>

## 12. From earlier: two names for one dictionary

From *Comprehensions, grids and aliasing*.

```python exec
id: from-earlier-two-names-1
key = {"A": "Q"}
spare = key
spare["B"] = "W"
print(key)
```

```predict
What will it print?

- {'A': 'Q'}
  - Only `spare` was changed.
- {'A': 'Q', 'B': 'W'}
  - `key` and `spare` are two names for one dictionary.
```

<details class="dl-answer"><summary>why</summary>

`{'A': 'Q', 'B': 'W'}`. A dictionary is mutable, like a list, so the same
thing happens. `spare = key` gives one dictionary a second name. For a
separate copy, write `spare = dict(key)`.

</details>

## 13. From earlier: counting from 1

From *Lists and looping over them*.

```python exec
id: from-earlier-counting-from-1-1
for index, letter in enumerate(["X", "Y", "Z"], 1):
    print(index, letter)
```

```predict
What will the last line print?

- 3 Z
  - Counting starts at 1, so the third letter is 3.
- 2 Z
  - The last index of three elements is 2.
```

<details class="dl-answer"><summary>why</summary>

`3 Z`. The second number given to `enumerate()` is where the counting
starts. The list's own indexes are still 0 to 2.

</details>

## 14. From earlier: which error

From *Reading an error message*. Which error does each of these raise?

- (a) `int("12.5")`
- (b) `[1, 2, 3][3]`
- (c) `"12" + 5`

<details class="dl-answer"><summary>answer</summary>

(a) A `ValueError`, because `int()` wants a whole number written in
digits, and 12.5 has a point. `float("12.5")` works. (b) An `IndexError`,
because three elements have indexes 0 to 2. (c) A `TypeError`, because
`+` will not join a string to a number.

</details>
