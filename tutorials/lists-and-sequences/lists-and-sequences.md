---
title: "Lists and looping over them"
year: "2026-2027"
version: 2026.09.26.1
worlds:
  secret-messages: Codes and hidden messages, the kind spies and puzzle-setters make.
  pixel-art: Pictures made of small squares, the way a screen draws them.
covers:
  lists-ordered-collections:
    covers: [MIT-6.3]
  changing-a-list:
    covers: [MIT-6.3]
  building-lists-with-loops:
    covers: [MIT-6.3, MIT-6.5]
  looping-over-lists:
    covers: [MIT-6.5, MIT-6.7]
---

# Lists and looping over them

Here is a message, kept as a list of words. What will the cell print?

```python exec
id: a-list-of-words-1
words = ["MEET", "ME", "AT", "NOON"]
print(words[1])
```

```predict
What will it print?

- MEET
  - It is the first word in the list.
- ME
  - Python counts the positions from 0, so 1 is the second word.
- An error
  - A list has no word 1, only a first word.
```

It prints `ME`. The list keeps four words under one name, in order, and
Python counts their positions from 0. Most programs work with many values,
not one: every letter of a message, every pixel in a row. Here we keep them
in a list, pick out the ones we want, and do something with each of them in
turn.

## Lists: ordered collections

A *list* is a row of values, written inside square brackets with commas
between them. Each value in it is an *element*. `len()` counts them, the
way it counted the characters in a string.

```python exec
id: lists-ordered-collections-1
letters = ["A", "L", "G", "O", "R", "I", "T", "H", "M", "S"]
print(letters)
print(len(letters))
```

Each element has a position, called its *index*. Python uses *zero-based
indexing*: the first element is at index 0, so the last of ten is at
index 9. A negative index counts from the end, and -1 is the last element.

```python exec
id: lists-ordered-collections-2
print(letters[0])     # the first element
print(letters[9])     # the last of ten
print(letters[-1])    # the last, counted from the end
print(letters[-2])    # the one before it
```

A string can be indexed in the same way. `"NOON"[0]` is `"N"`, and so is
`"NOON"[-1]`.

### Taking a slice

A *slice* takes a part of a list. It is written with two numbers and a
colon between them. What will this cell print?

```python exec
id: lists-ordered-collections-3
print(letters[2:5])
```

```predict
What will it print?

- ['G', 'O', 'R']
  - A slice stops before its second number.
- ['G', 'O', 'R', 'I']
  - From index 2 to index 5 is four letters: 2, 3, 4 and 5.
- ['L', 'G', 'O', 'R']
  - Counting from 1, the second letter is L.
```

From 2 to 5 looks like four elements, and there are three. The reason is
where the two numbers point. They do not point at elements. They point at
the gaps between them.

```python exec
id: lists-ordered-collections-4
print(letters[2:5])
print(letters[:3])     # no first number: from the start
print(letters[7:])     # no second number: to the end
```

![The ten letters A, L, G, O, R, I, T, H, M and S in a row. Above each one is its index, 0 to 9. Below, along the boundaries between them, are the eleven cut positions, 0 to 10, offset from the indices above. Underneath, each of the three slices is drawn as a band running between the two cuts it names: 2 to 5 takes G, O and R; the start-to-3 slice takes A, L and G; and the 7-to-end slice takes H, M and S.](where-the-cuts-are.svg)

Ten elements have eleven places to cut. A slice names two of those places
and takes everything between them. So `letters[2:5]` means "cut before G,
cut before I, and keep the middle", and that is three letters. The end
index is not left out by a special rule. A cut is a gap, and there is
nothing in a gap to take.

The picture also shows why `letters[:3]` and `letters[3:]` fit back
together, with nothing missing and nothing repeated: both meet at the same
cut. Try changing the numbers in the slices, and see which letters each
one takes.

## Changing a list

A list can be changed after it is made. A value that can be changed like
this is *mutable*.

```python exec
id: changing-a-list-1
letters = ["A", "L", "G", "O", "R", "I", "T", "H", "M", "S"]
letters[0] = "a"       # replace the first element
print(letters)
letters.append("!")    # add one element at the end
print(letters)
print(len(letters))
```

`append()` adds one element to the end of a list. It changes that list,
and gives nothing back. A string can be indexed like a list. Can it be
changed like one?

```python exec
id: changing-a-list-2
word = "NOON"
word[0] = "M"
print(word)
```

```predict
What will it print?

- MOON
  - A string is indexed like a list, so it changes like one.
- NOON
  - Python leaves the string as it was, and carries on.
- An error
  - A string cannot be changed once it is made.
```

It stops with a `TypeError`: `'str' object does not support item
assignment`. A string is *immutable*: once it is made, it cannot be
changed. To get MOON, build a new string from pieces of the old one:
`"M" + word[1:]`.

### Your turn

<div class="dl-world" data-world="secret-messages">

A spy's message is kept as a list of words. The meeting place has moved.
Can you change `"BRIDGE"` to `"STATION"`, and add `"TONIGHT"` at the end?
Then print the first word, the last word, and a slice that takes `BY`,
`THE` and `STATION`.

```python exec
id: your-turn-1--secret-messages
message = ["MEET", "ME", "BY", "THE", "BRIDGE"]

print(message)
```

```inputs
message
```

```hint
Which index is `"BRIDGE"` at? And which cut comes just before `BY`, and
which just after `STATION`?
```

```solution
message = ["MEET", "ME", "BY", "THE", "BRIDGE"]
message[4] = "STATION"
message.append("TONIGHT")
print(message[0])
print(message[-1])
print(message[2:5])
print(message)
---
`message[-1]` finds the last word however long the message grows, so
nobody has to count it.
```

</div>

<div class="dl-world" data-world="pixel-art">

A row of a picture is kept as a list of brightnesses, from 0 for black to
255 for white. Can you print the three pixels in the middle of the row?
Then make the first pixel white, add a black pixel at the end, and print
the row.

```python exec
id: your-turn-1--pixel-art
row = [0, 40, 80, 120, 160, 200, 240]

print(row)
```

```inputs
row
```

```hint
Seven pixels have eight cuts, from 0 to 7. Which two cuts are either side
of the middle three?
```

```solution
row = [0, 40, 80, 120, 160, 200, 240]
print(row[2:5])
row[0] = 255
row.append(0)
print(row)
---
The middle three are `[80, 120, 160]`. Printing them first matters: after
`append()`, the row has eight pixels, and no three are in the middle.
```

</div>

## Building lists with loops

An empty list, `[]`, can be filled one element at a time. Here a loop
builds the alphabet, with `chr()` from
[Variables, data types and text](tutorial:storing-and-computing). How long
will the list be?

```python exec
id: building-lists-with-loops-1
alphabet = []
for number in range(26):
    alphabet.append(chr(ord("A") + number))
print(alphabet)
print(len(alphabet))
```

```predict
type: number

How long will the list be?
```

It is 26 long, from A to Z. `range(26)` gives 0 to 25: 26 numbers, one for
each letter. This is the accumulator pattern from
[Repeating steps with loops](tutorial:repeating-yourself), with a list
where the total was. It starts empty, and gets one more value each time
round.

### Your turn

<div class="dl-world" data-world="secret-messages">

Can you build `shifted`, the alphabet moved three places along, so that it
starts `D`, `E`, `F` and ends `A`, `B`, `C`? Kept beside the plain
alphabet, it turns a message into code one letter at a time.

```python exec
id: your-turn-2--secret-messages
shift = 3
shifted = []

print(shifted)
```

```inputs
shifted
```

```hint
The letter at position `number` moves to position `(number + shift) % 26`.
Which letter is at that position?
```

```solution
shift = 3
shifted = []
for number in range(26):
    shifted.append(chr((number + shift) % 26 + ord("A")))
print(shifted)
---
`% 26` takes the last three positions back round to A, B and C. Try a
shift of 13: that table undoes itself, because 13 and 13 make 26.
```

</div>

<div class="dl-world" data-world="pixel-art">

Can you build `fade`, a row of 11 pixels that goes from black towards
white in equal steps: 0, 25, 50, and so on, up to 250?

```python exec
id: your-turn-2--pixel-art
fade = []

print(fade)
```

```inputs
fade
```

```hint
Eleven pixels means eleven times round the loop. What is pixel number
`step` worth, if each step adds 25?
```

```solution
fade = []
for step in range(11):
    fade.append(step * 25)
print(fade)
---
`range(0, 251, 25)` counts in steps of 25 by itself, and gives the same
eleven numbers.
```

</div>

## Looping over lists

A `for` loop can go through a list directly, one element at a time, in
order.

```python exec
id: looping-over-lists-1
words = ["MEET", "ME", "AT", "NOON"]
for word in words:
    print(word, len(word))
```

A string's `.split()` makes a list like this one from a sentence, cutting
it wherever there are spaces: `"MEET ME AT NOON".split()` gives
`['MEET', 'ME', 'AT', 'NOON']`.

Sometimes we need the index as well as the element. `enumerate()` gives
both, as a pair, each time round the loop.

```python exec
id: looping-over-lists-2
words = ["MEET", "ME", "AT", "NOON"]
for index, word in enumerate(words):
    print(index, word)
```

Try `enumerate(words, 1)` in place of `enumerate(words)`, and see what
changes.

<details class="dl-answer"><summary>What each line does</summary>

- `enumerate(words)` gives the pairs `0, "MEET"`, then `1, "ME"`, and so
  on, one pair each time round.
- `for index, word in` takes each pair apart: the first value goes into
  `index`, and the second into `word`.
- `print(index, word)` shows both. With `enumerate(words, 1)`, the
  counting starts at 1 instead of 0, and the words stay the same.

</details>

There is a second way to get the same pairs: loop over every index, and
look each element up.

```python exec
id: looping-over-lists-3
words = ["MEET", "ME", "AT", "NOON"]
for index in range(len(words)):
    print(index, words[index])
```

`range(len(words))` gives every index of the list, from 0 to one less than
its length. Both loops print the same thing. `enumerate()` says what it
means more plainly. Looping by index is the way to go when the loop needs
another element too, such as the one next door, at `index + 1`.

### Your turn

<div class="dl-world" data-world="secret-messages">

Where does the letter E appear in this message? Can you build `places`, a
list of the index of every E?

```python exec
id: your-turn-3--secret-messages
message = "MEET ME BY THE OLD TREE"
places = []

print(places)
```

```inputs
places
```

```hint
`enumerate()` works on a string too, one character at a time. When the
character is an E, what goes into `places`?
```

```solution
message = "MEET ME BY THE OLD TREE"
places = []
for index, letter in enumerate(message):
    if letter == "E":
        places.append(index)
print(places)
---
There are six, at `[1, 2, 6, 13, 21, 22]`. The spaces have positions too,
which is why the second word's E is at 6.
```

</div>

<div class="dl-world" data-world="pixel-art">

Which pixel in this row is the brightest? Can you set `brightest` to its
index, with a loop, and without `max()`?

```python exec
id: your-turn-3--pixel-art
row = [30, 90, 250, 120, 250, 60]
brightest = 0

print(brightest)
```

```inputs
brightest
```

```hint
Keep the index of the brightest pixel so far. Each time round, is this
pixel brighter than the one at that index?
```

```solution
row = [30, 90, 250, 120, 250, 60]
brightest = 0
for index, value in enumerate(row):
    if value > row[brightest]:
        brightest = index
print(brightest)
---
It prints 2. Two pixels are 250, and `>` keeps the first one it finds.
With `>=` it keeps the last, and prints 4. The question did not say which,
so the code decides, and it is worth saying which way it went.
```

</div>

### Your turn: adding up a list

<div class="dl-world" data-world="secret-messages">

How many letters does this message have, not counting the spaces between
the words? Can you set `total` with a loop, without `sum()`?

```python exec
id: your-turn-4--secret-messages
words = ["MEET", "ME", "BY", "THE", "OLD", "TREE"]
total = 0

print(total)
```

```inputs
total
```

```solution
words = ["MEET", "ME", "BY", "THE", "OLD", "TREE"]
total = 0
for word in words:
    total = total + len(word)
print(total)
---
18. Each time round, the loop adds one word's length to the running total.
```

</div>

<div class="dl-world" data-world="pixel-art">

What is the average brightness of this row? Can you set `average` with a
loop, without `sum()`? Is the row closer to `#` or to `.`, if `#` is 128
or more?

```python exec
id: your-turn-4--pixel-art
row = [30, 90, 250, 120, 250, 60]
total = 0

print(average)
```

```inputs
average
```

```solution
row = [30, 90, 250, 120, 250, 60]
total = 0
for value in row:
    total = total + value
average = total / len(row)
print(average)
---
The total is 800, and the average about 133.3, so the row as a whole is
`#`. Dividing by `len(row)`, and not by 6, keeps the code right when the
row changes length.
```

</div>

## Looking back

A slice stops before its second number, and so does `range()`. So
`letters[0:len(letters)]` is the whole list, and `range(len(letters))`
gives every index of it. What would go wrong if one of them stopped *at*
its second number instead?

A challenge: a rail-fence cipher writes a message's letters in a zig-zag
across two rails, then reads the top rail and then the bottom. The letters
at even indexes go on the top rail, and the rest on the bottom. Can you
code a message this way with a loop? Can you get it back again?

```python challenge
# A rail-fence cipher: even indexes on the top rail, odd on the bottom.
message = "MEETMEATNOON"
top = []
bottom = []
# Fill the two rails with a loop, then join them into one coded message.
# Can you get the message back from the coded one?
```

The next page,
[Comprehensions, grids and aliasing](tutorial:comprehensions-and-grids),
writes these loops on one line, keeps a whole picture in a list of lists,
and shows what happens when two names share one list.

## Where to read more

Everything here is covered elsewhere too, often in a form that will suit you
better than this one.

Downey, A. B. (2015). *Think Python: How to Think Like a Computer Scientist*
(2nd ed.). Green Tea Press. Free at <https://greenteapress.com/wp/think-python-2e/>.
Chapter 10, "Lists", covers indexing, slicing and looping at greater length,
with exercises.

Python Software Foundation. *The Python Tutorial*, section 3.1.3, "Lists".
<https://docs.python.org/3/tutorial/introduction.html#lists>. The official
introduction to lists, including slicing with a step, which this page leaves
for the practice.

Reducible (2019). *What if you had to invent a dynamic array?*
<https://www.youtube.com/watch?v=5AllG-i_yto>. What a Python list does
underneath, so that adding to the end stays quick however long the list
grows. About fourteen minutes.
