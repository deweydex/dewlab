---
title: "Finding bugs in bigger programs — Practice"
practice_for: when-it-goes-wrong
year: "2026-2027"
version: 2026.09.26.1
worlds:
  secret-messages: Codes and hidden messages, the kind spies and puzzle-setters make.
  pixel-art: Pictures made of small squares, the way a screen draws them.
---

# Finding bugs in bigger programs — Practice

Here your prediction is the exercise. Before you run a cell, say which
error it will raise, or what wrong answer it will give. Then run it, and
find out why. There are three problems from earlier pages at the end.

## 1. Which error

```python exec
id: which-error-1
word = "OTTER"
print(word[5])
```

```predict
What will it do?

- Print R
  - The fifth letter of OTTER is R.
- Stop with an IndexError
  - Five letters have positions 0 to 4.
- Print nothing
  - There is nothing at position 5.
```

<details class="dl-answer"><summary>why</summary>

It raises an `IndexError: string index out of range`. A string is indexed like a
list, and fails like one: five letters have positions 0 to 4.

</details>

## 2. A count that starts from nothing

```python exec
id: a-count-that-starts-from-nothing-1
counts = {}
counts["E"] = counts["E"] + 1
print(counts)
```

```predict
What will it do?

- Print {'E': 1}
  - A new count starts at 0, and 0 + 1 is 1.
- Stop with a KeyError
  - Python reads `counts["E"]` before there is one.
```

<details class="dl-answer"><summary>why</summary>

It raises a `KeyError: 'E'`. The right-hand side runs first, and it asks for a key
that is not there yet. `counts.get("E", 0) + 1` starts it at 0.

</details>

## 3. A name that was a function

```python exec
id: a-name-that-was-a-function-1
list = [1, 2]
letters = list("AB")
print(letters)
```

<details class="dl-answer"><summary>answer</summary>

It raises a `TypeError: 'list' object is not callable`. `list` was
Python's function for making lists, and the first line gave the name to a
list. From then on, `list(...)` tries to call a list. A different name,
such as `numbers`, fixes it. Restart Python, or reload the page, to get
`list` back.

</details>

## 4. Two things to find

Run this, and read the traceback. Which line failed, and which line is
responsible?

```python exec
id: two-things-to-find-1
def colour_of(character, palette):
    return palette[character]


def row_colours(row, palette):
    colours = []
    for character in row:
        colours.append(colour_of(character, palette))
    return colours


palette = {"#": "black", ".": "white"}
print(row_colours("#.#", palette))
print(row_colours("#x#", palette))
```

<details class="dl-answer"><summary>answer</summary>

`return palette[character]` failed, with `KeyError: 'x'`. The line
responsible is the last one, whose row has an `x` the palette does not
know. Or the palette is responsible, for not knowing it. Which one to
change depends on whether `x` was meant to be there.

</details>

## 5. The whole chain

Why does a traceback show the whole chain of calls, and not only the line
that failed?

<details class="dl-answer"><summary>answer</summary>

The line that failed is often correct, and the cause is earlier in the
program. A value is made in one place and used in another. The chain shows
how the bad value travelled, call by call, so you can trace it to where
it came from.

</details>

## 6. The same name twice

This is meant to print each row's number, and its row of four `#`.

```python exec
id: the-same-name-twice-1
for i in range(3):
    line = ""
    for i in range(4):
        line = line + "#"
    print(i, line)
```

```predict
What will the first line print?

- 0 ####
  - The outer loop is on its first row, row 0.
- 3 ####
  - The inner loop used `i` too, and left it at 3.
```

<details class="dl-answer"><summary>why</summary>

It prints `3 ####`, three times. Both loops use the name `i`, so the inner loop
overwrites the outer one's, and when the `print` runs, `i` is the inner
loop's last value. Give each loop its own name: `row` and `column`, say.

</details>

## 7. Counting in the wrong thing

<div class="dl-world" data-world="secret-messages">

This is meant to count the Es in a word. It runs, and gives 0 for every
word. Can you find the bug, fix it, and add a test that catches it?

```python exec
id: counting-in-the-wrong-thing-1--secret-messages
def count_e(word):
    """Give back how many times E appears in word."""
    count = 0
    for letter in range(len(word)):
        if letter == "E":
            count = count + 1
    return count
```

```inputs
guess: yes
count_e("TREE")
count_e("SKY")
count_e("")
```

```python exec
id: counting-in-the-wrong-thing-1-tests--secret-messages
tests: counting-in-the-wrong-thing-1--secret-messages
assert count_e("EYE") == 2
```

```hint
Add `print(letter)` inside the loop. What is `letter`, each time round?
```

```solution
def count_e(word):
    """Give back how many times E appears in word."""
    count = 0
    for letter in word:
        if letter == "E":
            count = count + 1
    return count
---
`range(len(word))` gives the positions, 0, 1, 2 and 3, so `letter` was a
number, never equal to `"E"`. A word with no E gives 0 either way, which
is why a test on `"SKY"` passes the bug.
```

</div>

<div class="dl-world" data-world="pixel-art">

This is meant to return one column of a picture, top to bottom. It
works on some pictures. Can you find the bug, fix it, and add a test that
catches it?

```python exec
id: counting-in-the-wrong-thing-1--pixel-art
def column(picture, c):
    """Give back column c of picture, from the top row down."""
    values = []
    for row in range(len(picture)):
        values.append(picture[c][row])
    return values
```

```inputs
guess: yes
column([[1, 2], [3, 4]], 0)
column([[1, 2, 3], [4, 5, 6]], 0)
column([[1, 2, 3], [4, 5, 6]], 2)
```

```python exec
id: counting-in-the-wrong-thing-1-tests--pixel-art
tests: counting-in-the-wrong-thing-1--pixel-art
assert column([[7], [8]], 0) == [7, 8]
```

```hint
A picture is `picture[row][column]`: the row first. Which index is the
row here, and which the column?
```

```solution
def column(picture, c):
    """Give back column c of picture, from the top row down."""
    values = []
    for row in range(len(picture)):
        values.append(picture[row][c])
    return values
---
The two indexes were swapped, so it gave back part of row `c`. On a
2 × 2 picture that is still a list of two numbers, and wrong, with no
error. On a picture wider than it is tall, it stops with an `IndexError`,
which is lucky: that at least says something is wrong.
```

</div>

## 8. Where it stops being right

This is meant to count the words longer than four letters. It gives 0.
Add a labelled `print` inside the loop, and find where it goes wrong.

```python exec
id: where-it-stops-being-right-1
def long_words(sentence):
    count = 0
    for word in sentence:
        if len(word) > 4:
            count = count + 1
    return count

print(long_words("MEET ME BY THE BRIDGE TONIGHT"))
```

<details class="dl-answer"><summary>answer</summary>

`print("word:", word)` inside the loop shows `M`, then `E`, then `E`. A
loop over a string uses its characters, not its words. Every
"word" has length 1. `for word in sentence.split():` gives the words, and
the answer 2: BRIDGE and TONIGHT.

</details>

## 9. Test the pieces

This is meant to decode a message by moving each letter back. It gives
nonsense. Test each piece on its own, with a letter whose answer you know,
and find the one with the bug.

```python exec
id: test-the-pieces-1
def shift_back(letter, shift):
    return chr((ord(letter) - ord("A") + shift) % 26 + ord("A"))


def decode(message, shift):
    plain = ""
    for character in message:
        if character.isupper():
            plain = plain + shift_back(character, shift)
        else:
            plain = plain + character
    return plain


print(decode("PHHW PH", 3))
```

<details class="dl-answer"><summary>answer</summary>

`shift_back("D", 3)` should give A, three letters back, and it gives G.
The `+ shift` moves forward. With `- shift`, it gives A, and the message
decodes to MEET ME. `decode` was right from the start. A test of `decode`
would have pointed at the bug too. A test of the smallest piece says
exactly which line.

</details>

## 10. Explain it to a duck

Some programmers keep a rubber duck on their desk. When they are stuck,
they explain their code to it, line by line, out loud. Why would that
help?

<details class="dl-answer"><summary>answer</summary>

When you explain a line, you have to say what it does, not what you meant
it to do. The bug is in the gap between the two. Halfway through an
explanation, people often stop and say "oh". The duck does nothing, and
that helps. It does not interrupt, and it does not already know what the
code is supposed to do. A classmate who lets you finish works as well.

</details>

## 11. From earlier: raise on purpose

From *Designing and testing good functions*.

```python exec
id: from-earlier-raise-on-purpose-1
def half(n):
    if n % 2 == 1:
        raise ValueError("half() needs an even number")
    return n // 2

print(half(8))
print(half(7))
```

```predict
What will the last line do?

- Print 3
  - 7 // 2 is 3.
- Stop with a ValueError
  - 7 is odd, so the function raises before it divides.
```

<details class="dl-answer"><summary>why</summary>

It prints 4 for 8, and then stops with
`ValueError: half() needs an even number`. The error is the function's
own, with its own message, at the place the problem was found.

</details>

## 12. From earlier: nearly in order

From *Sorting a list: bubble, insertion and selection sort*. A list is
already sorted except for its last element. Which of the three sorts does
least work on it?

<details class="dl-answer"><summary>answer</summary>

Insertion sort does least work. Every element but the last is already in place, so each
costs one comparison, and only the last is moved back to where it belongs.
Selection sort still searches the whole unsorted part every time, and
bubble sort, without a flag, still makes every comparison.

</details>

## 13. From earlier: a number and a letter

From *Lists and looping over them*.

```python exec
id: from-earlier-a-number-and-a-letter-1
for index, letter in enumerate("AB"):
    print(index + letter)
```

```predict
What will it do?

- Print 0A, then 1B
  - `+` joins the index and the letter.
- Stop with a TypeError
  - The index is a number, and the letter a string.
```

<details class="dl-answer"><summary>why</summary>

It raises a `TypeError`, because `+` will not join a number to a string. `str(index) +
letter` gives `0A`, and `print(index, letter)` shows both with a space
between.

</details>
