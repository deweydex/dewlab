---
title: "Reading an error message — Practice"
practice_for: reading-an-error-message
year: "2026-2027"
version: 2026.09.26.1
---

# Reading an error message — Practice

Here your guess is the exercise. Before you run a cell, say which error you
think it will raise, or whether it will run at all. Then run it, and read
what comes back from the bottom up.

Everything here uses only names, types, arithmetic, text, `print`, `input`
and `if`. There are no new tools, only new messages to read.

## 1. Which kind

For each of these, is it a syntax error, a runtime error, a logical error,
or no error at all?

- (a) `if total > 10` followed by an indented `print(total)`
- (b) `result = 10 + "5"`
- (c) `age = int("thirty")`
- (d) `average = total / count`, where `count` is 0

<details class="dl-answer"><summary>answer</summary>

(a) A syntax error: the colon is missing after `10`, so Python cannot read
the line, and runs nothing. (b) A runtime error, a `TypeError`: the line is
valid Python, but Python will not add a number to a string. (c) A runtime
error, a `ValueError`: `int` wants a string and got one, but `"thirty"` is
not written in digits. (d) A runtime error, a `ZeroDivisionError`. In real
programs, this error usually comes from a count that is zero when the
code expected it not to be.

</details>

## 2. Five times two

Somebody wanted the answer 10.

```python exec
id: five-times-two-1
doubled = "5" * 2
print(doubled)
```

```predict
What will it print?

- 10
  - 5 times 2 is 10.
- 55
  - `*` with a string repeats it.
- An error
  - You cannot multiply text.
```

<details class="dl-answer"><summary>why</summary>

It prints `55`, with no error. This is a logical error. `*` with a string repeats
the string. The line looks as if it should work, because `5 * 2` gives 10,
until you see that the value is a string. A value that came from `input()`
is always a string.

</details>

## 3. A number from text

```python exec
id: a-number-from-text-1
price = int("12")
print(price * 2)
```

```predict
type: number

What will it print?
```

## 4. Name the error

Before you run each cell, write the error you expect in its comment.

```python exec
id: naming-the-error-early-1
value = "12"
print(value + 3)
# I think it raises:
```

```python exec
id: naming-the-error-early-2
count = int("twelve")
# I think it raises:
```

```python exec
id: naming-the-error-early-3
message = "OTTER"
print(mesage)
# I think it raises:
```

```python exec
id: naming-the-error-early-5
print(17 % 0)
# I think it raises:
```

<details class="dl-answer"><summary>answer</summary>

A `TypeError`: Python cannot add a string and a number, though `value * 3`
would work and give `121212`. A `ValueError`: the type is right, because
`int` wants a string, but the content is not a number. A `NameError`,
ending `Did you mean: 'message'?`: read to the end of a message before you
search yourself. And a `ZeroDivisionError`, described as
`integer modulo by zero`. A remainder is a kind of division, and nothing
divides by zero.

</details>

## 5. A decimal comma

In many countries, people write a decimal comma: 12,50, not 12.50.

```python exec
id: naming-the-error-early-4
typed = "12,50"
price = float(typed)
print(price)
# I think it raises:
```

<details class="dl-answer"><summary>answer</summary>

A `ValueError`. Python only understands a decimal point, so `"12,50"` is
the right type for `float`, with content it cannot read. If `typed` came
from `input()`, the person using the program did nothing wrong. The
program needs to say what to type, or check what it got.

</details>

## 6. Where to look first

In a traceback, where do you find the error that stopped the program? And
when a syntax error puts its marker under a word that looks fine, where do
you look?

<details class="dl-answer"><summary>answer</summary>

At the last line. It names the error and describes it. The lines above it
say where, with the line number and a copy of the line.

For the marker, look just before it. Python complains at the moment it
becomes sure something is wrong, which is often a character or two after
the real mistake, or on the next line.

</details>

## 7. The line that failed, and the line responsible

```python exec
id: reading-a-short-traceback-1
letters = 45
extra = "5"
total = letters + extra
print("Total:", total)
```

Which line failed, and which line is *responsible*?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Read the last line first. What kind of error is it?
2. Which line number does the traceback name? That is the line that
   failed.
3. What types are `letters` and `extra`? Which line gave `extra` its type?

</details>

<details class="dl-answer"><summary>answer</summary>

Line 3 failed, `total = letters + extra`, with a `TypeError`. Line 2 is
responsible: `extra = "5"` made `extra` a string. Line 3 is written the
way it should be. It was given a value of a type it could not use.

</details>

## 8. Some output, then an error

Some of your output appeared above a traceback. What does that tell you?

<details class="dl-answer"><summary>answer</summary>

It tells you it is a runtime error. Python read the whole program, started to run
it, and got that far before it stopped. A syntax error prints nothing of
yours at all, because nothing runs.

</details>

## 9. Up by how much

A price goes from 50 to 60. It goes up by 10, which is 20% of the old price.
Percentage change is measured against the old value. This program runs.
Does it agree?

```python exec
id: when-nothing-looks-wrong-practice-1
old = 50
new = 60
change = (new - old) / new * 100
print("Change:", change, "%")
```

```inputs
change
```

```hint
Which number does the code divide by? Which one should it divide by?
```

```solution
old = 50
new = 60
change = (new - old) / old * 100
print("Change:", change, "%")
---
It divided by the new value, and gave about 16.67% instead of 20%. That is
close enough to look believable, which is why nobody notices it.
```

## 10. Exactly on the line

A pixel is drawn as `#` when its brightness is 128 or more. Run the cell
with `brightness` set to 127, then 128, then 129.

```python exec
id: when-nothing-looks-wrong-practice-2
brightness = 128
if brightness > 128:
    pixel = "#"
else:
    pixel = "."
print(pixel)
```

```inputs
pixel
```

```solution
brightness = 128
if brightness >= 128:
    pixel = "#"
else:
    pixel = "."
print(pixel)
---
With `>`, a brightness of exactly 128 was drawn as `.`. Logical errors
live at boundaries, so try the boundary itself, one below it and one above
it.
```

## 11. The habit that catches them

What is the one habit that catches logical errors?

<details class="dl-answer"><summary>answer</summary>

Try the program on answers you already know. Before you trust a program
on numbers you cannot check, give it numbers you can: halfway between 100
and 300 is 200, and ten percent of 50 is 5. If the program says something
else, you have found something.
[Designing and testing good functions](tutorial:building-reusable-tools),
later in the series, turns that habit into tests.

</details>

## 12. Two at once

This program has two mistakes. Can you fix them? Run it after each fix.

```python exec
id: fixing-early-1
brightness = 200
if brightness >= 128
    print("#")
else:
print(".")
```

```hint
Fix only the line the message names, then run it again. Is there a new
message? Which line does it name now?
```

```solution
brightness = 200
if brightness >= 128:
    print("#")
else:
    print(".")
---
The `if` line needs a colon, and `print(".")` needs to be indented under
`else:`. Python told you about the first mistake only: it stops at the
first thing it cannot read. So a new message after a fix does not mean the
fix failed. It can mean Python got further.
```

## 13. Next year

In a real program, `age` would come from `input("How old are you? ")`. Can
you fix the last line?

```python exec
id: fixing-early-2
age = "30"
print("Next year you will be " + age + 1)
```

```solution
age = "30"
print("Next year you will be", int(age) + 1)
---
`age` is a string, so `age + 1` is a `TypeError`. `int(age)` turns it into
a number first, and the comma lets `print` show text and a number side by
side, with no `str()` needed.
```

## 14. Better news

Why is an error message better news than no error message?

<details class="dl-answer"><summary>one good answer</summary>

An error message says where and what. A syntax error stops you before
anything happens, and a runtime error names the line and the reason. A
logical error says nothing at all. It may not be found for weeks, and by
then it has produced a great deal of confident output that nobody meant.

</details>
