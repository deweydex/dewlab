---
title: "Variables, data types and text"
year: "2026-2027"
version: 2026.10.09.2
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
Python keeps, and text. Python can also take text apart, one character at a
time.

## Variables: giving names to things

A *variable* is a name that refers to a value. We make one with the `=`
sign. In programming, `=` means "give this name to this value". It does not
mean "is equal to", the way it does in maths, and the next *cell*{.term} shows why
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
instruction, and Python runs it once. First it calculates the right-hand
side, `count + 1`, which is 6. Then it gives that value the name `count`. The old 5 is gone.

A variable's name should say what it holds. `price` is a good name for what
one thing costs. `p` tells us much less. Somebody reading the code, and that
could be you in a few months, would not know what `p` means. Python has a
few rules for names:

- A name starts with a letter or an underscore (`_`).
- After that, it can contain letters, numbers and underscores.
- Capital letters matter: `Price` and `price` are two different variables.

Python programmers write names in *snake_case*: lowercase words joined by
underscores, like `first_name`.

### Your turn

<div class="dl-world" data-world="secret-messages">

Can you make three variables? First, a secret word of your own. Then the
number of letters in it. Then `True` or `False`, for whether you would let
anybody see it. When you have them, print each one with a label that says
what it is.

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

Can you make three variables? First, the width of a picture in pixels. Then
its height. Then `True` or `False`, for whether it is in colour. When you
have them, print how many pixels the picture has, and whether it is in
colour, each with a label that says what it is.

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

An *integer* (`int`) is a whole number. Integers continue in both directions
from zero: …, −3, −2, −1, 0, 1, 2, 3, … Python's integers match the
integers in maths, which mathematicians call **Z**, from the German word
*Zahlen*, meaning "numbers".

A *floating-point number* (`float`) is a number with a decimal point.
Floats represent the real numbers of maths (**R**), but they cannot
store every real number exactly. The practice page for this tutorial shows
why.

A *string* (`str`) is a piece of text, written between quotes. Single
quotes and double quotes both work.

A *Boolean* (`bool`) is a value that is either `True` or `False`. Booleans
are named after George Boole, who created an algebra of logic in the
1840s.

The `type()` *function*{.term} tells us what type a value is.

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
types. For numbers it adds, and for strings it *concatenates*, which means
it joins them end to end. This is why types matter.

Before you run the next cell, write what you think each line will print in
the *comment*{.term} beside it.

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
`chr()` does the opposite, from a number to its character.

```python exec
id: text-you-can-take-apart-2
print(ord("A"))
print(ord("B"))
print(chr(67))
```

`"A"` is 65, `"B"` is 66, and so on up to `"Z"`, which is 90. The capital
letters are numbered in order, one after another.

<div class="dl-world" data-world="secret-messages">

So, to move a letter along the alphabet, we can add to its number. The next
section does this.

</div>

<div class="dl-world" data-world="pixel-art">

Text is stored as numbers, and so is the brightness of a pixel. We can add
to a number, whatever it stands for. The next section does this with a
pixel's brightness.

</div>

## Type conversion

Sometimes we need a value as another type. Python has a function for each
type: `int()`, `float()`, `str()` and `bool()`. Each one takes a value and
returns it as its own type.

```python exec
id: type-conversion-1
text_value = "42"
number_value = int(text_value)   # text to a whole number
print(number_value + 8)          # now arithmetic works: 50

number_as_text = str(100)        # a number to text
print("The answer is " + number_as_text)
```

This matters most when a *program*{.term} asks the person using it to type
something. The `input()` function asks for some typing, and returns what
was typed. It always returns a string, even when the person types a
number.

Run the next cell. It waits for you: a box appears after the question.
Type your answer, then press Enter.

```python exec
id: type-conversion-2
user_name = input("What is your name? ")
print("Hello, " + user_name)

user_age = input("How old are you? ")
print(type(user_age))          # it is a string, even if you typed digits
user_age = int(user_age)       # now it is a whole number
print("Next year you will be", user_age + 1)
```

What happens if you type `ten` for your age? Python stops with an error,
because `int()` cannot read `ten` as a number.

## Putting it together: a small program

Now we can put the ideas on this page together in one small program. A value
is stored, changed with arithmetic, and sent back round to the start with
`%` when it passes the end.

<div class="dl-world" data-world="secret-messages">

The program moves a letter along the alphabet, and goes back round to A
after Z. This is the main step in the oldest secret code there is. Julius
Caesar is said to have written to his generals with every letter moved three
places along: A became D, B became E. It is called a *Caesar shift*.

</div>

<div class="dl-world" data-world="pixel-art">

The program makes a pixel brighter. A pixel's brightness is a whole number
from 0 to 255, so there are 256 steps. A pixel at 255 is as bright as it can
be. If we add to it anyway, the number can go back round to 0, the way a
clock goes from 23 back to 0.

</div>

Here is the plan, as *pseudocode*{.term}:

<div class="dl-world" data-world="secret-messages">

```
STORE the letter, and how far to move it
TURN the letter into a number, counting A as 0
ADD the shift, and go back round after Z with % 26
TURN the number back into a letter
DISPLAY it
```

</div>

<div class="dl-world" data-world="pixel-art">

```
STORE the brightness of a pixel, and how much to add
ADD the amount to the brightness
GO BACK ROUND after 255 with % 256
DISPLAY the new brightness
```

</div>

And here it is in Python.

<div class="dl-world" data-world="secret-messages">

What will X become?

```python exec
id: now-the-implementation-1--secret-messages
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

X moves on to Y, then Z, then round to A. The `% 26` is the remainder
from [Algorithms, pseudocode and your first Python](tutorial:first-steps), the
one that sends a clock back to 0 after 23. There are 26 letters, so position
26 is position 0 again. Can you delete `% 26` from the cell? What does X
become then?

<details class="dl-answer"><summary>What each line does</summary>

- `position = ord(letter) - ord("A")` turns the letter into its place in
  the alphabet. `ord("X")` is 88 and `ord("A")` is 65, so X is at position
  23.
- `moved = (position + shift) % 26` adds the shift, which makes 26, and
  keeps the remainder after dividing by 26, which is 0.
- `new_letter = chr(moved + ord("A"))` turns position 0 back into a
  character: `chr(65)`, which is A.

</details>

</div>

<div class="dl-world" data-world="pixel-art">

What will the new brightness be?

```python exec
id: now-the-implementation-1--pixel-art
brightness = 250                         # 0 is black, 255 is the brightest
step = 10
new_brightness = (brightness + step) % 256   # go back round after 255
print(new_brightness)
```

```predict
What will the new brightness be?

- 4
  - 250 plus 10 is 260, which is past 255. Going back round to 0 leaves 4.
- 260
  - This is the sum, without going back round. No pixel has a brightness of
    260.
- 240
  - That is 10 less, not 10 more.
```

250 plus 10 is 260. The `% 256` is the remainder from [Algorithms,
pseudocode and your first Python](tutorial:first-steps), the one that sends
a clock back to 0 after 23. There are 256 brightness steps, so step 256 is
step 0 again, and 260 is step 4. Can you delete `% 256` from the cell? What
does the brightness become then?

<details class="dl-answer"><summary>What each line does</summary>

- `brightness = 250` and `step = 10` store the pixel's brightness, and how
  much to add to it.
- `new_brightness = (brightness + step) % 256` adds the step, which makes
  260, and keeps the remainder after dividing by 256, which is 4.
- `print(new_brightness)` shows the result.

</details>

</div>

### Your turn

<div class="dl-world" data-world="secret-messages">

A letter was moved three places along, and it became D. What was it before?
Can you change `shift` so the program moves backwards, and find out? Then
change `letter` to `"A"` and run it again. Which letter, moved three places
along, becomes A?

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
Moving backwards three places is a `shift` of `-3`. Does `% 26` still bring
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
For `"A"`, `-3` takes the position below 0, and `% 26` brings it back round
to X.
```

</div>

<div class="dl-world" data-world="pixel-art">

A pixel was made 60 steps brighter, and now has a brightness of 20. What was
it before? Can you change `step` so the program makes the pixel darker, and
find out? Then change `brightness` to `0` and run it again. Which brightness,
made 60 steps brighter, becomes 0?

```python exec
id: your-turn-4--pixel-art
brightness = 20
step = 60
new_brightness = (brightness + step) % 256
print(new_brightness)
```

```inputs
new_brightness
```

```hint
Making a pixel darker by 60 is a `step` of `-60`. Does `% 256` still bring
the number back into 0 to 255?
```

```solution
brightness = 20
step = -60
new_brightness = (brightness + step) % 256
print(new_brightness)
---
The pixel was at 216 before. Making it darker is the same program with the
step the other way. For `20`, `-60` takes the brightness below 0, and
`% 256` brings it back round to 216. With `brightness = 0`, the same step
gives 196.
```

</div>

## Putting values into text

Joining pieces with `+` and `str()` works, but it is easy to forget a space
or a `str()`. An *f-string* is a shorter way. It is a string with the letter `f`
straight before the opening quote. Inside it, Python replaces each name in
curly brackets with that name's value, turned into text for you.

<div class="dl-world" data-world="secret-messages">

```python exec
id: putting-values-into-text-1--secret-messages
letter = "X"
new_letter = "A"
shift = 3
print(f"{letter} moved {shift} places is {new_letter}")
```

</div>

<div class="dl-world" data-world="pixel-art">

```python exec
id: putting-values-into-text-1--pixel-art
brightness = 250
new_brightness = 4
step = 10
print(f"{brightness} made {step} steps brighter is {new_brightness}")
```

</div>

Some results have more decimal places than anybody wants to read. A poster
100 cm wide and 70 cm tall has a shape we can find by dividing:

```python exec
id: putting-values-into-text-2
ratio = 100 / 70
print(f"The poster is {ratio} times as wide as it is tall")
print(f"The poster is {ratio:.2f} times as wide as it is tall")
```

`:.2f` after the name, inside the curly brackets, means "show this number
with 2 decimal places". Change the `2` to `1` or `4`, and run the cell
again. It changes only how the number is shown. `ratio` still holds every
decimal place.

### Your turn

<div class="dl-world" data-world="secret-messages">

A message has 47 letters, and 12 of them are E. What share of the letters
is E, as a percentage? Can you print it with an f-string, to 1 decimal
place, like `E is 8.3% of the letters`? (Code-breakers count letters like
this. In English, E is the most common letter, so the most common letter
in a Caesar-shifted message is probably a moved E.)

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

Python joins `"40" + "2"` into `402`, but it stops with an error at
`"40" + 2`. Why does Python need `str()` before it will join a number to a
piece of text, when a person reading the line would know what was meant?

<div class="dl-world" data-world="secret-messages">

A challenge: can you move a whole word, like `CAT`, three places along the
alphabet, with what this page has? What makes it tedious? What would you
want Python to do for you, if you had a word of a hundred letters?

```python challenge
# Move each letter of CAT three places along the alphabet.
word = "CAT"
shift = 3
print(chr((ord(word[0]) - ord("A") + shift) % 26 + ord("A")))
```

`word[0]` is the first letter of the word, and
[Lists and looping over them](tutorial:lists-and-sequences) explains why it is 0,
not 1. [Repeating steps with loops](tutorial:repeating-yourself) does the
tedious part for you.

</div>

<div class="dl-world" data-world="pixel-art">

A challenge: can you make a whole row of three pixels, with brightness
`200`, `90` and `250`, 60 steps brighter, with what this page has? What
makes it tedious? What would you want Python to do for you, if you had a row
of a thousand pixels?

```python challenge
# Make each pixel of the row 60 steps brighter, going back round after 255.
row = [200, 90, 250]
step = 60
print((row[0] + step) % 256)
```

`row[0]` is the first pixel of the row, and
[Lists and looping over them](tutorial:lists-and-sequences) explains why it is 0,
not 1. [Repeating steps with loops](tutorial:repeating-yourself) does the
tedious part for you.

</div>

## Where to read more

Computerphile (2014). *Floating Point Numbers.*
<https://www.youtube.com/watch?v=PZRI1IfStY0>. This video explains why `float`
cannot represent every number exactly, and why that matters.

Python Software Foundation. *The Python Tutorial — An Informal Introduction
to Python.* <https://docs.python.org/3/tutorial/introduction.html>. This is the
official reference for `int`, `float`, `str` and `bool`, with the exact
rules Python follows for each.

<div class="dl-world" data-world="secret-messages">

Singh, S. (1999). *The Code Book.* Fourth Estate. This book tells the history of secret
codes, from Caesar's shift to the machines of the Second World War, and how
each one was broken.

</div>

<div class="dl-world" data-world="pixel-art">

Technology Connections. *The Weird World in RGB.*
<https://www.youtube.com/watch?v=uYbdx4I7STg>. This video shows how a screen
mixes red, green and blue light into every colour, the three numbers we put
into `rgb(...)` on this page. About twenty minutes.

</div>

CrashCourse (2017). *Representing Numbers and Letters with Binary: Crash
Course Computer Science #4.*
<https://www.youtube.com/watch?v=1GSjbWt0c9M>. Every value on this page, a
number or a piece of text, is stored as ones and zeros. This video shows
how. About eleven minutes.
