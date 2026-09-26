---
title: "Making decisions with if, elif and else"
year: "2026-2027"
version: 2026.09.26.1
worlds:
  secret-messages: Codes and hidden messages, the kind spies and puzzle-setters make.
  pixel-art: Pictures made of small squares, the way a screen draws them.
covers:
  comparisons-true-or-false:
    covers: [PDP-LO6]
  if-statements-choosing-a-path:
    covers: [PDP-LO6]
  if-else-two-paths:
    covers: [PDP-LO6]
  elif-multiple-paths:
    covers: [PDP-LO6]
  boolean-operators-combining-conditions:
    covers: [PDP-LO6]
    touches: [MIT-2.4]
  classifying-numbers-a-mathematical-application:
    covers: [MIT-1.1]
---

# Making decisions with if, elif and else

A Caesar shift moves letters, and leaves a space or a question mark where
it is. So before a program changes a character, it has to ask what kind of
character it is. Python can answer questions like that with `True` or
`False`. What do you think this cell prints?

```python exec
id: which-comes-first-1
print("A" < "B")
print("Z" < "a")
```

```predict
What will the last line print?

- True
  - Every character has a number, and capitals come first.
- False
  - Z is the last letter of the alphabet, so nothing comes after it.
```

It prints `True` both times. Python compares characters by their numbers,
the ones `ord()` gives. `Z` is 90 and `a` is 97, so every capital comes
before every small letter. This page is about asking questions like these,
and choosing what to do with the answer.

## Comparisons: true or false?

Before a program can make a decision, it needs a question with a `True` or
`False` answer. Python has six *comparison operators* for this. A
comparison operator compares two values and gives back `True` or `False`.

```python exec
id: comparisons-true-or-false-1
print(5 > 3)        # greater than
print(5 < 3)        # less than
print(5 >= 5)       # greater than or equal to
print(5 <= 4)       # less than or equal to
print(5 == 5)       # equal to: two equals signs
print(5 != 3)       # not equal to
```

| Operator | Meaning |
|---|---|
| `>` | greater than |
| `<` | less than |
| `>=` | greater than or equal to |
| `<=` | less than or equal to |
| `==` | equal to |
| `!=` | not equal to |

Look closely at `==`. One equals sign, `=`, gives a name a value. Two,
`==`, asks whether two values are equal. Mixing them up is one of the most
common slips in programming, for beginners and for people who have
programmed for years.

Before you run the next cell, write what you think each line prints in the
comment beside it.

```python exec
id: your-turn-1
print(10 > 10)        # I think:
print(10 >= 10)       # I think:
print("abc" == "abc") # I think:
print("abc" == "ABC") # I think:
print(1 == 1.0)       # I think:
print(0 == False)     # I think:
```

The last one surprises most people. In Python, `False` counts as equal to
`0`, and `True` as equal to `1`. That link between logic and arithmetic
goes back to George Boole in the 1840s, and the word "Boolean" comes from
his name.

## If statements: choosing a path

An *if statement* is code that runs only when a condition is `True`.

```python exec
id: if-statements-choosing-a-path-1
character = "?"

if character == " ":
    print("A space: leave it where it is.")

print("On to the next character.")
```

The first line has three parts: the keyword `if`, a condition,
`character == " "`, and a colon. The indented line under it is the *body*
of the if statement, and it runs only when the condition is `True`. The
last line is not indented, so it is back in the normal flow, and it runs
every time.

Here the character is `?`, so only the last line runs. Change `"?"` to
`" "`, a space, and run it again.

Python uses indentation to know which lines belong inside the if
statement, so in Python indentation is required. We use four spaces for
each level; the editor puts them in for you when you press Tab.

## If-else: two paths

Often we want one thing when a condition is `True`, and something else when
it is `False`. An *if-else* statement does this. Here a pixel's brightness,
from 0 for black to 255 for white, decides whether it is drawn as `#` or as
`.`.

```python exec
id: if-else-two-paths-1
brightness = 128

if brightness >= 128:
    pixel = "#"
else:
    pixel = "."

print(pixel)
```

```predict
What will it print?

- #
  - `>=` is true when the two sides are equal, too.
- .
  - 128 is not more than 128.
```

It prints `#`. `>=` means "greater than *or equal to*", so 128 counts. The
`else` part catches every case the `if` condition does not, so between them
the two paths cover every possible brightness.

### Your turn

<div class="dl-world" data-world="secret-messages">

A Caesar shift keeps a space as it is, and moves anything else. Can you set
`action` to `"keep"` when `character` is a space, and to `"shift"`
otherwise?

```python exec
id: your-turn-2--secret-messages
character = " "

print(action)
```

```inputs
action
```

```hint
Which two paths are there? The condition for the first is
`character == " "`.
```

```solution
character = " "
if character == " ":
    action = "keep"
else:
    action = "shift"
print(action)
---
Try a letter too, and a question mark: at the moment, the question mark
would be shifted. The next section gives a program more than two paths.
```

</div>

<div class="dl-world" data-world="pixel-art">

A checkerboard stripe is dark in even columns and light in odd ones. Can
you set `shade` to `"dark"` when the column `x` is even, and to `"light"`
when it is odd?

```python exec
id: your-turn-2--pixel-art
x = 6

print(shade)
```

```inputs
shade
```

```hint
A number is even when its remainder after dividing by 2 is 0. Which
operator gives the remainder?
```

```solution
x = 6
if x % 2 == 0:
    shade = "dark"
else:
    shade = "light"
print(shade)
---
`x % 2 == 0` is the test for "even" that comes back again and again in
programs. Try `x = 7` too.
```

</div>

## Elif: multiple paths

Sometimes there are more than two cases. The keyword `elif`, short for
"else if", adds another condition, so a program can have as many paths as
it needs. Here, a brightness picks one of four characters, from dark to
light.

```python exec
id: elif-multiple-paths-1
brightness = 200

if brightness >= 192:
    pixel = "#"
elif brightness >= 128:
    pixel = "+"
elif brightness >= 64:
    pixel = "-"
else:
    pixel = "."

print(pixel)
```

Python checks each condition in turn, from the top. It runs the body of the
first one that is `True`, and skips the rest.

So does the order matter? Suppose we checked `brightness >= 64` first. What
would 200 become then?

<details class="dl-answer"><summary>What happens</summary>

It would become `-`. 200 is more than 64, and that condition now comes
first, so Python never reaches the check for `#`. The order matters: with
`>=`, the biggest threshold goes first.

</details>

Try a few brightnesses in the cell, and then the boundaries: 64, 128 and
192. Does each one give the character you expect? Mistakes often hide at a
boundary, so a boundary is always worth trying.

### Your turn

<div class="dl-world" data-world="secret-messages">

`character.isupper()` is `True` for a capital letter, and
`character.islower()` for a small one. Can you set `kind` to
`"capital"`, `"small"`, `"space"` or `"other"`, whatever `character`
holds?

```python exec
id: your-turn-3--secret-messages
character = "e"

print(kind)
```

```inputs
kind
```

```hint
There are four paths: `if`, two `elif`s, and `else`. Which case can the
`else` catch?
```

```solution
character = "e"
if character.isupper():
    kind = "capital"
elif character.islower():
    kind = "small"
elif character == " ":
    kind = "space"
else:
    kind = "other"
print(kind)
---
A question mark, a digit and a full stop all land in `else`. Those are the
characters a Caesar shift leaves alone.
```

</div>

<div class="dl-world" data-world="pixel-art">

A picture is 64 pixels wide, with columns numbered 0 to 63. Can you set
`where` to `"left"` when `x` is below 0, `"on the picture"` when it is 0 to
63, and `"right"` when it is 64 or more?

```python exec
id: your-turn-3--pixel-art
x = 70

print(where)
```

```inputs
where
```

```hint
Three paths: `if`, `elif`, `else`. Try the boundaries when it runs: −1, 0,
63 and 64.
```

```solution
x = 70
if x < 0:
    where = "left"
elif x < 64:
    where = "on the picture"
else:
    where = "right"
print(where)
---
The `elif` only runs when `x < 0` was `False`, so it does not need to ask
whether `x` is 0 or more: that is already known.
```

</div>

## Boolean operators: combining conditions

Sometimes one comparison is not enough. A *Boolean operator* combines
`True` and `False` values, or turns one round. Python has three: `and`,
`or` and `not`.

`and` is `True` only when *both* sides are `True`. A capital letter is one
that is `"A"` or after, and `"Z"` or before:

```python exec
id: boolean-operators-combining-conditions-1
character = "Q"
print(character >= "A" and character <= "Z")
```

`or` is `True` when *at least one* side is `True`. A word ends at a space
or a full stop:

```python exec
id: boolean-operators-combining-conditions-2
character = "."
print(character == " " or character == ".")
```

`not` turns `True` into `False`, and `False` into `True`:

```python exec
id: boolean-operators-combining-conditions-3
see_through = False
if not see_through:
    print("draw this pixel")
```

| Operator | True when… |
|---|---|
| `a and b` | `a` and `b` are both true |
| `a or b` | at least one of `a` and `b` is true |
| `not a` | `a` is false |

What changes if `character` is `"q"` in the first cell, or `"!"` in the
second? Can you say before you run it?

When one line uses more than one of these, Python works them out in a fixed
order: `not` first, then `and`, then `or`. When you are not sure how Python
will read a line, add brackets to make your meaning clear.

### Your turn

<div class="dl-world" data-world="secret-messages">

Code-breakers count vowels. Can you set `is_vowel` to `True` when
`character` is A, E, I, O or U, and to `False` otherwise?

```python exec
id: your-turn-4--secret-messages
character = "O"

print(is_vowel)
```

```inputs
is_vowel
```

```hint
Five comparisons, joined by `or`. A comparison already gives `True` or
`False`, so you can give its result a name without an `if`.
```

```solution
title: with what you've met so far
character = "O"
is_vowel = (character == "A" or character == "E" or character == "I"
            or character == "O" or character == "U")
print(is_vowel)
---
Brackets let a long condition run onto a second line.
```

```solution
title: a shorter way you'll meet later
character = "O"
is_vowel = character in "AEIOU"
print(is_vowel)
---
`in` asks whether one piece of text appears inside another.
[Lists and looping over them](tutorial:lists-and-sequences) uses it on lists too.
```

</div>

<div class="dl-world" data-world="pixel-art">

A picture is 64 pixels wide and 48 tall. Can you set `on_picture` to `True`
when the point `(x, y)` is on it, and to `False` when it is not?

```python exec
id: your-turn-4--pixel-art
x = 10
y = 50

print(on_picture)
```

```inputs
on_picture
```

```hint
Four things must all be true: `x` is 0 or more, `x` is less than 64, and
the same two for `y` and 48. Which operator needs everything to be true?
```

```solution
title: with what you've met so far
x = 10
y = 50
on_picture = x >= 0 and x < 64 and y >= 0 and y < 48
print(on_picture)
---
`y` is 50, below the bottom row, so it is `False`.
```

```solution
title: a shorter way you'll meet later
x = 10
y = 50
on_picture = 0 <= x < 64 and 0 <= y < 48
print(on_picture)
---
Python lets comparisons chain, the way they do in maths: `0 <= x < 64`
means both at once.
```

</div>

## Classifying numbers: a mathematical application

Now we can use our new tools on a problem from mathematics: sorting
numbers into families. Mathematicians sort numbers into four families,
and each one sits inside the next.

| Family | Symbol | What it holds | Examples |
|---|---|---|---|
| natural numbers | N | whole numbers from 0 upwards | 0, 1, 7 |
| integers | Z | whole numbers, positive, negative or zero | -3, 0, 7 |
| rational numbers | Q | numbers we can write as one integer divided by another | 1/2, -3.5, 7 |
| real numbers | R | every number on the number line | π, 1/2, 7 |

Each family contains the one before it. Every natural number is also an
integer. Every integer is also a rational number, and every rational
number is also a real number. The families fit together like a set of
Russian dolls, one inside the next.

(Some books start the natural numbers at 1. On this page, and in the
code below, 0 counts as a natural number.)

The program below looks at a value and tells us which families it
belongs to. What do you think it will say about -3.5?

```python exec
id: classifying-numbers-a-mathematical-application-1
# Which number families does a value belong to?
value = -3.5

is_real = True                           # everything we can store is real (approximately)
is_rational = True                       # for our purposes, all Python numbers are rational
is_integer = (value == int(value))       # is it a whole number?
is_natural = is_integer and (value >= 0) # is it a non-negative whole number?

print("Value: " + str(value))
print("Natural (N): " + str(is_natural))
print("Integer (Z): " + str(is_integer))
print("Rational (Q): " + str(is_rational))
print("Real (R): " + str(is_real))
```

### Your turn

1. Change `value` to each of these in turn: 7, -3, 0.5, 0, 3.14159. How
   does the answer change each time?
2. In the cell below, plan a new version as pseudocode. It should use
   `if`, `elif` and `else`.
3. Write it so that it prints one clear summary, such as "7 is a natural
   number (and therefore also an integer, rational, and real)."

**Pseudocode first, then the code:**

```python exec
id: your-turn-6
# Pseudocode:
#
#
#

# Your number classifier
value = 7
```

## Looking back

The order of the `elif` conditions decided which character 200 became. When
does the order of the conditions *not* matter? Think of a set of conditions
where it makes no difference which comes first.

A challenge: can you make a Caesar shift that moves a capital letter three
places along, and leaves anything else, a space or a question mark, as it
is? Try it with `"Q"`, `"Z"`, `" "` and `"?"`.

```python challenge
# Move a capital letter three places along. Leave anything else alone.
character = "Q"
shift = 3
position = ord(character) - ord("A")
moved = (position + shift) % 26
print(chr(moved + ord("A")))
```

Sequence, one line after another, and *selection*, choosing a path, are
two of the three building blocks of every program. The third, repetition,
is in [Repeating steps with loops](tutorial:repeating-yourself). First,
[Reading an error message](tutorial:reading-an-error-message) shows what to
do when Python stops with an error.

## Where to read more

Khan Academy. *If Statements.*
<https://www.khanacademy.org/computing/intro-to-python-fundamentals/x5279a44ae0ab15d6:designing-algorithms-with-conditionals/x5279a44ae0ab15d6:boolean-conditions/v/if-statements>.
A second walk through the same idea, a program choosing between paths,
with its own examples.

Khan Academy. *Evaluating Compound Boolean Expressions.*
<https://www.khanacademy.org/computing/intro-to-python-fundamentals/x5279a44ae0ab15d6:designing-algorithms-with-conditionals/x5279a44ae0ab15d6:compound-boolean-conditions/v/evaluating-compound-boolean-expressions>.
Traces through `and`, `or` and `not` step by step, which is worth watching
once before trusting your own head to do it.

Stand-up Maths (2016). *Leap Years: we can do better.*
<https://www.youtube.com/watch?v=qkt_wmRKYNQ>. A year is a leap year if it
divides by 4, unless it divides by 100, unless it divides by 400: an `if`,
`elif` and `else` in one rule. Matt Parker explains where it comes from.
Twelve minutes.
