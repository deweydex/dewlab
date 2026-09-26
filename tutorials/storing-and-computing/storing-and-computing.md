---
title: "Variables, data types and text"
year: "2026-2027"
version: 2026.09.26.1
worlds:
  secret-messages: Codes and hidden messages, the kind spies and puzzle-setters make.
  pixel-art: Pictures made of small squares, the way a screen draws them.
covers:
  variables-giving-names-to-things:
    covers: [PDP-LO4, PDP-LO11]
  data-types-different-kinds-of-information:
    covers: [PDP-LO4]
  type-conversion:
    covers: [PDP-LO4]
  number-systems-how-computers-count:
    covers: [MIT-1.4]
  putting-it-together-a-small-program:
    covers: [PDP-LO7]
  putting-values-into-text:
    covers: [PDP-LO4]
---

# Variables, data types and text

Python can remember a value under a name, and use it again later. Here the
name `message` holds a piece of text. What will the last line print?

```python exec
id: a-name-for-a-message-1
message = "HELLO"
shout = message + "!!!"
print(shout)
```

```predict
What will the last line print?

- HELLO!!!
  - `message` holds HELLO, and `+` puts the three marks on the end.
- message!!!
  - This is what you would see if Python used the name itself, rather
    than what the name holds.
- An error
  - A name and a piece of text are different things. Can `+` join them?
```

It prints `HELLO!!!`. When Python meets the name `message`, it uses the
value the name holds. And `+` with two pieces of text joins them end to end.

In [Algorithms, pseudocode and your first Python](tutorial:first-steps),
each result was gone as soon as it was shown. With names, a value stays, so
we can build on it. This page is about names, the different kinds of value
Python keeps, and text: something Python can take apart, one character at a
time.

## Variables: giving names to things

A *variable* is a name that refers to a value. We make one with the `=`
sign. In programming, `=` means "give this name to this value". It does not
mean "is equal to", the way it does in maths, and the next cell shows why
that matters.

```python exec
id: variables-giving-names-to-things-1
count = 5
count = count + 1
print(count)
```

```predict
type: number

What will it print?
```

It prints 6. In maths, $c = c + 1$ can never be true. In Python it is an
instruction, carried out once: work out the right-hand side, `count + 1`,
which is 6, then give that value the name `count`. The old 5 is gone.

A variable's name should say what it holds. `shift` is a good name for the
number of places a secret code moves each letter. `s` is a poor one:
somebody reading the code, and that could be you in a few months, would
not know what `s` means. Python has a few rules for names:

- A name starts with a letter or an underscore (`_`).
- After that, it can contain letters, numbers and underscores.
- Capital letters matter: `Shift` and `shift` are two different variables.

Python programmers write names in *snake_case*: lowercase words joined by
underscores, like `secret_word`.

### Your turn

<div class="dl-world" data-world="secret-messages">

Can you make a variable for a secret word of your own, one for the number
of letters in it, and one for whether you would let anybody see it: `True`
or `False`? Then print each one with a label that says what it is.

```python exec
id: your-turn-1--secret-messages
# Your variables here

```

```solution
secret_word = "OTTER"
letters = 5
anyone_can_see = False
print("secret word:", secret_word)
print("letters:", letters)
print("anyone can see it:", anyone_can_see)
---
Yours will hold different values. What matters is that each name says
what it holds, and each label says it again for the person reading the
output.
```

</div>

<div class="dl-world" data-world="pixel-art">

Can you make variables for a picture's width and height in pixels, and one
for whether it is in colour: `True` or `False`? Then print how many pixels
it has, with a label that says what the number is.

```python exec
id: your-turn-1--pixel-art
# Your variables here

```

```solution
width = 64
height = 48
in_colour = True
print("pixels:", width * height)
print("in colour:", in_colour)
---
Yours will hold different values. What matters is that each name says
what it holds, and each label says it again for the person reading the
output.
```

</div>

## Data types: different kinds of information

A *data type*, or type for short, is the kind of data a value is. Python
has several types built in. These are the four we use most:

| Type | What it holds | Examples |
|---|---|---|
| `int` | whole numbers | `42`, `-7`, `0` |
| `float` | numbers with a decimal point | `3.14`, `-0.5`, `2.0` |
| `str` | text, in quotes | `"hello"`, `'world'` |
| `bool` | true or false | `True`, `False` |

An *integer* (`int`) is a whole number. Integers go on in both directions
from zero: …, −3, −2, −1, 0, 1, 2, 3, … Python's integers match the
integers in maths, which mathematicians call **Z**, from the German word
*Zahlen*, meaning "numbers".

A *floating-point number* (`float`) is a number with a decimal point.
Floats stand in for the real numbers of maths (**R**), but they cannot
store every real number exactly. The practice page for this tutorial shows
why.

A *string* (`str`) is a piece of text, written between quotes. Single
quotes and double quotes both work.

A *Boolean* (`bool`) is a value that is either `True` or `False`. Booleans
are named after George Boole, who worked out an algebra of logic in the
1840s.

The `type()` function tells us what type a value is.

```python exec
id: data-types-different-kinds-of-information-1
print(type(42))
print(type(3.14))
print(type("hello"))
print(type(True))
```

`"42"`, with quotes, is a string. To Python it is text that happens to
contain two digits. What do you think the second line of this cell prints?

```python exec
id: where-i-might-get-stuck-1
print(40 + 2)
print("40" + "2")
```

```predict
What will the second line print?

- 42
  - This treats "40" and "2" as the numbers they look like.
- 402
  - `+` with two pieces of text joins them, whatever the characters are.
- An error
  - You cannot add text, can you?
```

It prints `402`. The `+` operator does different things for different
types: for numbers it adds, and for strings it *concatenates*, which means
it joins them end to end. This is why types matter.

Before you run the next cell, write what you think each line will print in
the comment beside it.

```python exec
id: your-turn-2
print(type(7))              # I think:
print(type(7.0))            # I think:
print(type("7"))            # I think:
print(type(7 + 0.5))        # I think:
print("3" * 4)              # I think:
print(3 * 4)                # I think:
```

## Text you can take apart

A string is a row of characters, in order. Python can tell you how long it
is, change its capitals, and repeat it.

```python exec
id: text-you-can-take-apart-1
message = "meet at noon"
print(len(message))       # how many characters, spaces included
print(message.upper())    # the same text in capitals
print("ha" * 3)           # a string repeated
```

Every character also has a number of its own. The computer stores the
number, and shows you the character. `ord()` gives a character's number, and
`chr()` goes the other way, from a number to its character.

```python exec
id: text-you-can-take-apart-2
print(ord("A"))
print(ord("B"))
print(chr(67))
```

`A` is 65, `B` is 66, and so on up to `Z`, which is 90. The capital letters
are numbered in order, one after another. That is what makes the next
section possible: to move a letter along the alphabet, we can move its
number.

## Type conversion

Sometimes we need a value as another type. Python has a function for each
type: `int()`, `float()`, `str()` and `bool()`. Each one takes a value and
gives it back as its own type.

```python exec
id: type-conversion-1
text_value = "42"
number_value = int(text_value)   # text to a whole number
print(number_value + 8)          # now arithmetic works: 50

number_as_text = str(100)        # a number to text
print("The answer is " + number_as_text)
```

This matters most when a program asks the person using it to type
something. The `input()` function asks for some typing, and gives back what
was typed. It always gives back a string, even when the person types a
number.

The lines in the next cell are comments, so the cell does nothing yet. To
try them, remove the `#` at the start of each line of code, then run the
cell. It waits for you to type something.

```python exec
id: type-conversion-2
# user_name = input("What is your name? ")
# print("Hello, " + user_name)

# user_age = input("How old are you? ")
# print(type(user_age))          # it is a string
# user_age = int(user_age)       # now it is a whole number
# print("Next year you will be", user_age + 1)
```

## Number Systems: How Computers Count

We count in *base 10*, also called decimal. Base 10 uses ten digits,
0 to 9. We probably count in tens because we have ten fingers. But there
is nothing special about ten: you can build a working number system on
any base.

Computers use base 2, also called *binary*. Binary uses only two
digits, 0 and 1. The reason is in the hardware: a computer is built from
tiny switches called transistors, and each one has two states, on and
off.

In decimal, each position in a number is worth a power of 10. The number
42 means 4 tens and 2 ones:

    4 × 10 + 2 × 1  =  42

In binary, each position is worth a power of 2: 1, 2, 4, 8, 16, 32, and
so on. The binary number 101010 means:

    1 × 32 + 0 × 16 + 1 × 8 + 0 × 4 + 1 × 2 + 0 × 1  =  42

Python can write numbers in binary too. The cell below also shows base
16, *hexadecimal*, which uses the digits 0 to 9 and then the letters A to
F. What do you think `print(0b101010)` will show? Run the cell to check.

```python exec
id: number-systems-how-computers-count-1
# Python can work with binary directly
print(0b101010)       # 0b prefix means "this is binary"
print(bin(42))        # bin() converts to a binary string

# And hexadecimal (base 16), which uses digits 0-9 and letters A-F
print(0x2A)           # 0x prefix means "this is hexadecimal"
print(hex(42))        # hex() converts to a hex string

# Let's verify that binary conversion by hand
print(1*32 + 0*16 + 1*8 + 0*4 + 1*2 + 0*1)
```

Why do people use hexadecimal? Each hex digit matches exactly four
binary digits, so hexadecimal is a short way to write binary. The hex
digit `A` is 1010 in binary, `F` is 1111, and so on.

### Your turn

Let's convert these numbers by hand first, and then check them with
Python.

1. What is the decimal value of binary `11001`?
2. How do you write decimal 100 in binary?
3. How do you write decimal 255 in hex?

Write your working in the comments in the cell. Then, under
`# Verification:`, use Python to check each answer.

```python exec
id: your-turn-3
# Work through the conversions by hand, then verify
# 1. Binary 11001 = ?
#    Working: 

# 2. Decimal 100 in binary = ?
#    Working: 

# 3. Decimal 255 in hex = ?
#    Working: 

# Verification:
```

## Putting it together: a small program

Now we can move a letter along the alphabet, which is the heart of the
oldest secret code there is. Julius Caesar is said to have written to his
generals with every letter moved three places along: A became D, B became E.
It is called a *Caesar shift*.

Here is the plan, as pseudocode:

```
STORE the letter, and how far to move it
TURN the letter into a number, counting A as 0
ADD the shift, and go back round after Z with % 26
TURN the number back into a letter
DISPLAY it
```

And here it is in Python. What will X become?

```python exec
id: now-the-implementation-1
letter = "X"
shift = 3
position = ord(letter) - ord("A")      # A is 0, B is 1, ... X is 23
moved = (position + shift) % 26        # go back round after Z
new_letter = chr(moved + ord("A"))
print(new_letter)
```

```predict
What will X become?

- A
  - X moves on to Y, Z, and then round to A.
- [
  - This is what `chr()` gives for the number after Z, without going back
    round.
- U
  - That is three places back, not three places on.
```

X moves on to Y, then Z, then round to A. The `% 26` is the same remainder
that made a clock go back to 0 after 23: there are 26 letters, so position 26
is position 0 again. Take it out of the cell, and see what X becomes then.

<details class="dl-answer"><summary>What each line does</summary>

- `position = ord(letter) - ord("A")` turns the letter into its place in
  the alphabet. `ord("X")` is 88 and `ord("A")` is 65, so X is at position
  23.
- `moved = (position + shift) % 26` adds the shift, which makes 26, and
  keeps the remainder after dividing by 26, which is 0.
- `new_letter = chr(moved + ord("A"))` turns position 0 back into a
  character: `chr(65)`, which is A.

</details>

### Your turn

<div class="dl-world" data-world="secret-messages">

A letter was moved three places along, and it became D. What was it before?
Can you change the program to move a letter backwards, and find out? Then
try A: which letter moves three places along to become A?

```python exec
id: your-turn-4--secret-messages
letter = "D"
shift = 3
position = ord(letter) - ord("A")
moved = (position + shift) % 26
new_letter = chr(moved + ord("A"))
print(new_letter)
```

```inputs
new_letter
```

```hint
Moving backwards three places is a shift of −3. Does `% 26` still bring
the number back into 0 to 25?
```

```solution
letter = "D"
shift = -3
position = ord(letter) - ord("A")
moved = (position + shift) % 26
new_letter = chr(moved + ord("A"))
print(new_letter)
---
D came from A. Decoding is the same program with the shift the other way.
Try A too: −3 takes it below 0, and `% 26` brings it back round to X.
```

</div>

<div class="dl-world" data-world="pixel-art">

A web page writes a colour as text: `rgb(30, 144, 255)`, with its red,
green and blue from 0 to 255. Here the three are in variables. Can you
build that text, under the name `colour`, from the three numbers?

```python exec
id: your-turn-4--pixel-art
red = 30
green = 144
blue = 255
colour = ""
print(colour)
```

```inputs
colour
```

```hint
`+` joins strings, but `red` is a number. Which function turns a number
into text?
```

```solution
red = 30
green = 144
blue = 255
colour = "rgb(" + str(red) + ", " + str(green) + ", " + str(blue) + ")"
print(colour)
---
`str()` turns each number into text, and `+` joins the pieces. The next
section shows a shorter way to write lines like this one.
```

</div>

## Putting values into text

Joining pieces with `+` and `str()` works, but it is easy to forget a space
or a `str()`. An *f-string* is a shorter way: a string with the letter `f`
straight before the opening quote. Inside it, Python replaces each name in
curly brackets with that name's value, turned into text for you.

```python exec
id: putting-values-into-text-1
letter = "X"
new_letter = "A"
shift = 3
print(f"{letter} moved {shift} places is {new_letter}")
```

Some results have more decimal places than anybody wants to read. A screen
1920 pixels wide and 1080 tall has a shape we can find by dividing:

```python exec
id: putting-values-into-text-2
ratio = 1920 / 1080
print(f"The screen is {ratio} times as wide as it is tall")
print(f"The screen is {ratio:.2f} times as wide as it is tall")
```

`:.2f` after the name, inside the curly brackets, means "show this number
with 2 decimal places". Change the `2` to `1` or `4`, and run the cell
again. It changes only how the number is shown: `ratio` still holds every
decimal place.

### Your turn

<div class="dl-world" data-world="secret-messages">

A message has 47 letters, and 12 of them are E. What share of the letters
is E, as a percentage? Can you print it with an f-string, to 1 decimal
place, like `E is 25.5% of the letters`? (Code-breakers count letters like
this. In English, E is the most common letter, so the most common letter
in a Caesar-shifted message is probably E, moved.)

```python exec
id: putting-values-into-text-3--secret-messages
letters = 47
es = 12

```

```solution
letters = 47
es = 12
share = es / letters * 100
print(f"E is {share:.1f}% of the letters")
---
About a quarter of these letters are E, which is more than in most English
text, where E is about one letter in eight.
```

</div>

<div class="dl-world" data-world="pixel-art">

A photo is 640 pixels wide and 480 tall. Can you print one line, with an
f-string, like `640 × 480 is 307200 pixels, 0.31 megapixels`? A megapixel
is a million pixels.

```python exec
id: putting-values-into-text-3--pixel-art
width = 640
height = 480

```

```solution
width = 640
height = 480
pixels = width * height
print(f"{width} × {height} is {pixels} pixels, {pixels / 1000000:.2f} megapixels")
---
Inside the curly brackets you can write a small calculation as well as a
name: `{pixels / 1000000:.2f}` divides first, then shows 2 decimal places.
```

</div>

## Looking back

Python stopped at `"40" + 2`, but not at `"40" + "2"`. Why does Python need
`str()` before it will join a number to a piece of text, when a person
reading the line would know what was meant?

A challenge: can you move a whole word, like `CAT`, three places along,
with what this page has? What makes it tedious? What would you want Python
to do for you, if you had a word of a hundred letters?

```python challenge
# Move each letter of CAT three places along the alphabet.
word = "CAT"
shift = 3
print(chr((ord(word[0]) - ord("A") + shift) % 26 + ord("A")))
```

`word[0]` is the first letter of the word, and
[Lists and sequences](tutorial:lists-and-sequences) explains why it is 0,
not 1. [Repeating steps with loops](tutorial:repeating-yourself) does the
tedious part for you.

## Where to read more

Computerphile (2014). *Floating Point Numbers.*
<https://www.youtube.com/watch?v=PZRI1IfStY0>. Why `float` cannot represent
every number exactly, and why that turns out to matter.

Python Software Foundation. *The Python Tutorial — An Informal Introduction
to Python.* <https://docs.python.org/3/tutorial/introduction.html>. The
official reference for `int`, `float`, `str` and `bool`, with the exact
rules Python follows for each.

Khan Academy. *The Binary Number System.*
<https://www.khanacademy.org/computing/computers-and-internet/xcae6f4a7ff015e7d:digital-information/xcae6f4a7ff015e7d:binary-numbers/v/the-binary-number-system>.
Slower, worked ground through binary, for anyone who wants a second example
before trying the conversions themselves.

Singh, S. (1999). *The Code Book.* Fourth Estate. The history of secret
codes, from Caesar's shift to the machines of the Second World War, and how
each one was broken.
