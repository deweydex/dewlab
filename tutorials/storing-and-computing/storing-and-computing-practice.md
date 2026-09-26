---
title: "Variables, data types and text — Practice"
practice_for: storing-and-computing
year: "2026-2027"
version: 2026.09.26.1
worlds:
  secret-messages: Codes and hidden messages, the kind spies and puzzle-setters make.
  pixel-art: Pictures made of small squares, the way a screen draws them.
---

# Variables, data types and text — Practice

These problems are about names, types and text. Take your time with the
ones about types. In your first term, most confusing errors come from a
value whose type you did not expect. Try each one before you open anything
under it.

## 1. Allowed names

Which of these can be variable names in Python? For the ones that cannot,
can you say why?

`total`, `2nd_place`, `first name`, `_hidden`, `class`, `Total`,
`total_2`, `my-name`

```python exec
id: allowed-names-1
# Try a name here, and see what Python says
total = 1
```

<details class="dl-answer"><summary>answer</summary>

Allowed: `total`, `_hidden`, `Total`, `total_2`.

- `2nd_place`: a name cannot start with a digit.
- `first name`: a name cannot contain a space. Python reads it as two
  separate things.
- `class`: this is a reserved word, which Python keeps for its own use.
- `my-name`: the hyphen is a minus sign, so Python reads it as `my - name`.

`Total` is allowed, and it is a different variable from `total`. If you
confuse the two, you can lose an afternoon.

</details>

## 2. A copy, or a link

```python exec
id: a-copy-or-a-link-1
x = 5
y = x
x = 10
print(y)
```

```predict
type: number

What will it print?
```

<details class="dl-answer"><summary>why</summary>

`y` is still 5. The line `y = x` gave `y` the value 5 at the moment it ran.
It did not tie `y` to `x`. In an equation, `y = x` stays true. In Python,
it was a single instruction, and Python ran it once.

</details>

## 3. Swap them

Can you swap the values of `a` and `b`, so that `a` gets what `b`
had, and `b` with what `a` had?

```python exec
id: swap-them-1
a = "left"
b = "right"
# swap them here

print(a, b)
```

```inputs
a
b
```

```solution
title: with what you've met so far
a = "left"
b = "right"
spare = a
a = b
b = spare
print(a, b)
---
Without `spare`, the line `a = b` would come first and wipe out the value
of `a` that you still need.
```

```solution
title: a shorter way you'll meet later
a = "left"
b = "right"
a, b = b, a
print(a, b)
---
Python can swap two names in one line. It works out both values on the
right before it gives either name a new one.
```

## 4. Names that explain

Can you rename these so that a person reading the code can tell what it
does?

```python exec
id: names-that-explain-1
x = 64
y = 48
z = x * y
print(z)
```

<details class="dl-answer"><summary>one good answer</summary>

```python
width = 64
height = 48
pixels = width * height
print(pixels)
```

The arithmetic is the same, and now the code says what it is about.

</details>

## 5. What type is it

Say the type of each of these, then check with `type()` in the cell:
`42`, `42.0`, `"42"`, `True`, `4 / 2`, `4 // 2`, `"4" + "2"`.

```python exec
id: what-type-is-it-1
print(type(4 / 2))
```

<details class="dl-answer"><summary>answer</summary>

`int`, `float`, `str`, `bool`, `float`, `int`, `str`.

Most people miss `4 / 2`. Division with `/` always gives a
float, even when the answer is whole: `2.0`, not `2`.

</details>

## 6. A number times some text

```python exec
id: a-number-times-some-text-1
print(5 * "3")
```

```predict
What will it print?

- 15
  - This reads "3" as the number it looks like.
- 33333
  - A string times a whole number is the string repeated.
- An error
  - Multiplying text by a number sounds like it should not work.
```

What do `"5" + "3"` and `"5" + 3` do? Try them.

<details class="dl-answer"><summary>why</summary>

`5 * "3"` repeats the text five times: `33333`. `"5" + "3"` joins two
pieces of text: `53`. And `"5" + 3` stops with a `TypeError`. `+` with one
string and one number has no clear meaning, so Python stops rather than
guess. (There is
more on errors in
[Reading an error message](tutorial:reading-an-error-message).)

</details>

## 7. Text that looks like a number

Why does `int("3.7")` stop with an error, when `int(3.7)` gives 3?

<details class="dl-answer"><summary>answer</summary>

`int(3.7)` takes a number and drops the part after the decimal point.
`int("3.7")` takes a *string* and tries to read it as a whole number, and
"3.7" is not a whole number written down. `float("3.7")` works, and
`int(float("3.7"))` gets to 3 by doing the two steps in order.

</details>

## 8. Cutting, or rounding

```python exec
id: cutting-or-rounding-1
print(int(-3.7))
```

```predict
type: number

What will it print?
```

<details class="dl-answer"><summary>why</summary>

−3. `int()` cuts off the part after the decimal point, which moves the
number towards zero. That is called truncating. Rounding would give −4,
and `round(-3.7)` does. The two agree on positive numbers and differ on
negative ones. This difference can hide in code for months.

</details>

## 9. The word False

```python exec
id: the-word-false-1
print(bool("False"))
```

```predict
What will it print?

- True
  - Text that is not empty counts as true, whatever it says.
- False
  - This reads what the text says.
```

<details class="dl-answer"><summary>why</summary>

`True`. Zero and empty things are false, and everything else is true.
`"False"` is a piece of text that is not empty, so it counts as true.
Python does not read what the text says. Try `bool(0)`, `bool("")` and
`bool(-5)` too.

</details>

## 10. 25 plus 1 is 251

A program asks somebody to type their age with `input()`, then adds 1. It
prints `251` instead of `26`. What happened?

<details class="dl-answer"><summary>answer</summary>

`input()` always returns a string, so `"25" + "1"` joined two pieces of
text. The fix is `int(input(...))`, which turns the text into a number the
moment it arrives.

</details>

## 11. Going round

<div class="dl-world" data-world="secret-messages">

A code called ROT13 moves every letter 13 places along. Can you use the
Caesar shift from the tutorial to find what N becomes? Then move the
answer 13 places again. What do you notice?

```python exec
id: thirteen-places-along-1--secret-messages
letter = "N"
shift = 13

```

```inputs
new_letter
```

```solution
letter = "N"
shift = 13
position = ord(letter) - ord("A")
moved = (position + shift) % 26
new_letter = chr(moved + ord("A"))
print(new_letter)
---
N becomes A, and A moved 13 places becomes N again. There are 26 letters,
so two moves of 13 go all the way round: ROT13 decodes itself. People once
used it online to hide the end of a joke or a spoiler.
```

</div>

<div class="dl-world" data-world="pixel-art">

A pixel's red is 200, and a brush adds 100 to it. A colour stops at 255,
so the brush should stop there. Can you find what `%` would
do to 300, going round like a clock with 256 steps? And why would a brush
not want that?

```python exec
id: thirteen-places-along-1--pixel-art
red = 200
brighter = red + 100

```

```inputs
brighter % 256
```

```solution
red = 200
brighter = red + 100
print(brighter % 256)
---
`300 % 256` is 44: going round after 255 turns a bright red almost black.
The remainder is right for a clock or an alphabet, which really do go
round. A colour does not. [Making decisions with if, elif and
else](tutorial:making-decisions) shows how to stop at 255 instead.
```

</div>

## 12. Point one plus point two

```python exec
id: floating-point-1
print(0.1 + 0.2)
print(0.1 + 0.2 == 0.3)
```

```predict
What will the last line print?

- True
  - 0.1 and 0.2 do make 0.3.
- False
  - A computer cannot store 0.1 exactly.
```

<details class="dl-answer"><summary>why</summary>

0.1 and 0.2 cannot be stored exactly in binary, in the same way that a
third cannot be written exactly in decimal (0.333…). The computer stores
each as the nearest number it can, and the two small differences do not
cancel. The sum is 0.30000000000000004, which is wrong in the seventeenth
decimal place. That rarely matters, except when you ask whether two values are
exactly equal.

To compare two floats, ask whether they are close enough:
`abs(a - b) < 1e-9`. The limit depends on what the numbers
are. Money in cents needs a different limit from the distance between
stars. Python has `math.isclose()` too, with a limit of its own.

</details>

## 13. Exact in binary

Which of these can binary floating point store exactly? `0.5`, `0.25`,
`0.1`, `0.75`, `0.3`

<details class="dl-answer"><summary>answer</summary>

`0.5`, `0.25` and `0.75` are exact. `0.1` and `0.3` are not. A number is
exact in binary when it is made of halves, quarters, eighths and so on. A
tenth is not, because 10 has a factor of 5, and binary has only 2s to work
with. A third is not exact in decimal for the same reason.

</details>

## 14. Hours and minutes

Can you change a number of minutes into hours and minutes, with clear
names, and print it with an f-string?

```python exec
id: hours-and-minutes-1
total_minutes = 500

```

```inputs
hours
minutes
```

```solution
total_minutes = 500
hours = total_minutes // 60
minutes = total_minutes % 60
print(f"{total_minutes} minutes is {hours} hours and {minutes} minutes")
---
8 hours and 20 minutes.
```

## 15. Counting in cents

A shop's till stores prices in euro as floats. Adding up fifty items at
€0.10 gives €4.999999999999998. What should the till store instead?

<details class="dl-answer"><summary>answer</summary>

Whole cents, as integers. Fifty lots of 10 cents is exactly 500, and the
till divides by 100 only when it shows the total. Real payment systems work
this way. When a quantity is made of whole small units, store the whole
units. Floats are for measurements. For counting, use integers.

</details>

## 16. Four answers from two values

```python exec
id: four-answers-from-two-values-1
x = "10"
y = 5
print(x * y)
print(int(x) * y)
print(x + str(y))
print(int(x) + y)
```

```predict
type: number

What will the last line print?
```

<details class="dl-answer"><summary>why</summary>

`1010101010`, then `50`, then `105`, then `15`. The same two values give
four different answers, and the types decide every one.

</details>

## 17. An f-string instead

Can you rewrite the last line with an f-string, and without `str()`?

```python exec
id: an-f-string-instead-1
name = "Aoife"
age = 34
print("Hello, " + name + ". You are " + str(age) + " years old.")
```

```solution
name = "Aoife"
age = 34
print(f"Hello, {name}. You are {age} years old.")
---
The f-string turns `age` into text for you. If you forget the `f`, Python
prints the curly brackets and the names as they are, with no error, so
that slip is easy to miss.
```

## 18. Decimal places

```python exec
id: putting-values-into-text-practice-1
share = 2 / 3
print(f"{share:.0f}")
```

```predict
type: number

What will it print?
```

Then try `:.2f` and `:.4f`, and `f"{5:.2f}"`.

<details class="dl-answer"><summary>why</summary>

`1`. With no decimal places, 0.666… rounds up to 1. `:.2f` gives `0.67`,
`:.4f` gives `0.6667`, and `f"{5:.2f}"` gives `5.00`. So `:.2f` can add places
as well as remove them. That is useful for prices.

</details>

## 19. A price from cents

The till's total is `total_cents = 1234`. Can you print it as
`Total: €12.34`?

```python exec
id: a-price-from-cents-1
total_cents = 1234

```

```solution
total_cents = 1234
print(f"Total: €{total_cents / 100:.2f}")
---
Inside the curly brackets, a small calculation works as well as a name.
The `:.2f` matters when the total is a whole number of euro: 500 cents
prints as `€5.00`, not `€5.0`.
```
