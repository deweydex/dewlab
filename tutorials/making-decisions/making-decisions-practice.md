---
title: "Making decisions with if, elif and else — Practice"
practice_for: making-decisions
year: "2026-2027"
version: 2026.09.26.1
worlds:
  secret-messages: Codes and hidden messages, the kind spies and puzzle-setters make.
  pixel-art: Pictures made of small squares, the way a screen draws them.
---

# Making decisions with if, elif and else — Practice

Before you write an `if`, work out which values its condition is `True`
for. When a decision goes a way you did not expect, the place to look is
usually the condition, not the lines under it. Try each problem before you
open anything under it.

## 1. Capitals and small letters

```python exec
id: capitals-and-small-letters-1
print("Apple" < "apple")
```

```predict
What will it print?

- True
  - Capital letters have smaller numbers than small letters.
- False
  - They are the same word, so neither comes first.
```

Then try `"apple" < "banana"`, `10 == 10.0` and `"10" == 10`.

<details class="dl-answer"><summary>why</summary>

`True`: Python compares strings character by character, using each
character's number, and capitals come before small letters. That is why a
simple sort puts `Zoe` before `adam`. `"apple" < "banana"` is `True` too.
`10 == 10.0` is `True`, because both are the number ten, and `"10" == 10`
is `False`, because one is text and the other a number.

</details>

## 2. One equals sign or two

What is the difference between `=` and `==`?

<details class="dl-answer"><summary>answer</summary>

`=` gives a name a value. `==` asks a question, and gives back `True` or
`False`. In Python, `if x = 5:` stops with a syntax error, and that helps
you. In some other languages that line is allowed: it quietly sets `x` to
5, and the condition is then always true.

</details>

## 3. Strictly between

Can you set `between` to `True` when `n` is strictly between 10 and 20, and
to `False` otherwise?

```python exec
id: strictly-between-1
n = 15

print(between)
```

```inputs
between
```

```solution
title: with what you've met so far
n = 15
between = n > 10 and n < 20
print(between)
```

```solution
title: a shorter way you'll meet later
n = 15
between = 10 < n < 20
print(between)
---
Python allows chained comparisons like this one, and they mean what they
look like. Most other languages need the first form.
```

## 4. Three ifs instead of elif

```python exec
id: three-ifs-instead-of-elif-1
brightness = 150
if brightness >= 64:
    print("-")
if brightness >= 128:
    print("+")
if brightness >= 192:
    print("#")
```

How many lines will it print for a brightness of 150? And for 200?

<details class="dl-answer"><summary>why</summary>

Two lines for 150, `-` and `+`, and three for 200. Separate `if`
statements are separate questions, and Python asks each one in turn.
`elif` means "otherwise, ask this", so only one path runs. A pixel should
get one character, so it needs `elif`, with the biggest threshold first.

</details>

## 5. Positive, negative or zero

Can you set `sign` to `"positive"`, `"negative"` or `"zero"`, whatever `n`
holds?

```python exec
id: positive-negative-or-zero-1
n = 0

print(sign)
```

```inputs
sign
```

```solution
n = 0
if n > 0:
    sign = "positive"
elif n < 0:
    sign = "negative"
else:
    sign = "zero"
print(sign)
---
There are three cases, and zero has to be one of them. With
`if n >= 0: sign = "positive"`, zero gets the wrong name, and zero is
exactly the value a tester tries first.
```

## 6. Even and positive

Can you set `description` to something like `"even and positive"` or `"odd
and negative"`, from two separate decisions?

```python exec
id: even-and-positive-1
n = -7

print(description)
```

```inputs
description
```

```solution
title: with what you've met so far
n = -7
if n % 2 == 0:
    parity = "even"
else:
    parity = "odd"
if n > 0:
    sign = "positive"
elif n < 0:
    sign = "negative"
else:
    sign = "zero"
description = parity + " and " + sign
print(description)
---
Even or odd, and the sign, are two separate questions, so the code makes
two separate decisions. One long `if` would need six paths.
```

```solution
title: a shorter way you'll meet later
n = -7
parity = "even" if n % 2 == 0 else "odd"
sign = "positive" if n > 0 else "negative" if n < 0 else "zero"
description = parity + " and " + sign
print(description)
---
`"even" if n % 2 == 0 else "odd"` is an if-else that fits on one line: it
gives `"even"` when the condition is true, and `"odd"` when it is not.
```

## 7. And, or, not

This cell prints every result of `and` and `or`. It uses a loop, which is
in [Repeating steps with loops](tutorial:repeating-yourself). For now, you
only need its output.

```python exec
id: boolean-operators-1
for p in [True, False]:
    for q in [True, False]:
        print(p, q, "   and:", p and q, "   or:", p or q)
```

Say what each of these gives: `True and False`, `True or False`,
`not True`, `not (5 > 3)`, `(5 > 3) and (2 > 4)`, `(5 > 3) or (2 > 4)`.

<details class="dl-answer"><summary>answer</summary>

`False`, `True`, `False`, `False`, `False`, `True`.

</details>

## 8. Half price

A cinema charges half price to anyone under 16 or over 65. Can you set
`half_price` for any `age`?

```python exec
id: half-price-1
age = 70

print(half_price)
```

```inputs
half_price
```

```solution
age = 70
half_price = age < 16 or age > 65
print(half_price)
---
With `and`, nobody would get half price: no age is both under 16 and over
65. When a condition comes out `True` for nothing, or for everything, look
at the operator first.
```

## 9. A good password

A password is acceptable when it has at least 8 characters and contains a
digit. `len(password)` gives the number of characters. Can you set
`acceptable`?

```python exec
id: a-good-password-1
password = "otter2026"
has_digit = True

print(acceptable)
```

```inputs
acceptable
```

```solution
password = "otter2026"
has_digit = True
acceptable = len(password) >= 8 and has_digit
print(acceptable)
---
There is no `== True` on the end. `has_digit` is already `True` or
`False`, so comparing it with `True` adds a step and says nothing new.
```

## 10. A leap year

A year is a leap year when it can be divided by 4, except that a century is
not, unless it can also be divided by 400. So 2024 is, 1900 is not, and 2000
is. Can you set `is_leap` for any `year`?

```python exec
id: a-leap-year-1
year = 1900

print(is_leap)
```

```inputs
is_leap
```

```hint
Build it in two parts: "divided by 4 and not a century", or "divided by
400". Can you write each part on its own first?
```

```solution
year = 1900
is_leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
print(is_leap)
---
Python does not need the brackets, because it works out `and` before `or`.
They are there for the reader. Try 2024, 2000, 2023 and 1600 too.
```

## 11. Two opposites

Write `not (a > b)` in a simpler way. Then write `not (a and b)` in a
simpler way.

<details class="dl-answer"><summary>answer</summary>

`a <= b`: the opposite of "greater than" is "less than *or equal to*".
Forgetting the equal case is one of the most common slips there is.

`(not a) or (not b)`: the opposite of "both" is "at least one is not". This
is De Morgan's law. The other half: the opposite of "either" is "neither".
We meet it again in
[Logic: truth tables, XOR and De Morgan's laws](tutorial:logic-and-truth).

</details>

## 12. A condition that protects

```python exec
id: a-condition-that-protects-1
n = 0
if n != 0 and 10 / n > 1:
    print("yes")
else:
    print("no")
```

```predict
What will it print?

- yes
  - 10 divided by something is more than 1.
- no
  - The first half is `False`, so the whole `and` is `False`.
- An error
  - Dividing by zero stops Python.
```

<details class="dl-answer"><summary>why</summary>

It prints `no`, with no error. Python stops working out an `and` as soon as
one side is `False`, because nothing on the right could make the whole
thing `True`. This is called *short-circuiting*, and here it guards the
division. Swap the two conditions, and the program stops with a
`ZeroDivisionError`.

</details>

## 13. Opposite signs

Can you set `opposite` to `True` when one of `a` and `b` is negative and the
other is positive?

```python exec
id: opposite-signs-1
a = 0
b = -5

print(opposite)
```

```inputs
opposite
```

```solution
title: with what you've met so far
a = 0
b = -5
opposite = (a < 0 and b > 0) or (a > 0 and b < 0)
print(opposite)
```

```solution
title: a shorter way you'll meet later
a = 0
b = -5
opposite = (a < 0) != (b < 0)
print(opposite)
---
This asks whether "`a` is negative" and "`b` is negative" differ. The two
give different answers for zero: here, with 0 and −5, the first says
`False` and this one `True`. The question did not say what to do with
zero. When a question has a gap, whoever writes the code fills it, and
should say how.
```

## 14. Near a hundred

Can you set `near` to `True` when `n` is within 20 of 100, or within 20 of
200? `abs()` gives the size of a number without its sign: `abs(-7)` is 7.

```python exec
id: near-a-hundred-1
n = 185

print(near)
```

```inputs
near
```

```solution
n = 185
near = abs(n - 100) <= 20 or abs(n - 200) <= 20
print(near)
---
`abs(n - target) <= 20` is the general shape of "within 20 of". It saves
two comparisons for each target.
```

## 15. One more path

<div class="dl-world" data-world="secret-messages">

The tutorial's Caesar shift moves capitals. Can you set `moved` so that a
small letter moves too, counting from `"a"`, and anything else stays as it
is?

```python exec
id: one-more-path-1--secret-messages
character = "q"
shift = 3

print(moved)
```

```inputs
moved
```

```hint
Three paths: a capital counts from `"A"`, a small letter from `"a"`, and
anything else is left alone.
```

```solution
character = "q"
shift = 3
if character.isupper():
    moved = chr((ord(character) - ord("A") + shift) % 26 + ord("A"))
elif character.islower():
    moved = chr((ord(character) - ord("a") + shift) % 26 + ord("a"))
else:
    moved = character
print(moved)
---
`q` moves to `t`. The two letter paths are the same shift, with a
different starting letter.
```

</div>

<div class="dl-world" data-world="pixel-art">

A colour pixel has a red, a green and a blue, each from 0 to 255. Its
brightness is roughly the average of the three. Can you set `pixel` to
`"#"` when the brightness is 128 or more, and to `"."` otherwise?

```python exec
id: one-more-path-1--pixel-art
red = 200
green = 40
blue = 90

print(pixel)
```

```inputs
pixel
```

```solution
red = 200
green = 40
blue = 90
brightness = (red + green + blue) / 3
if brightness >= 128:
    pixel = "#"
else:
    pixel = "."
print(pixel)
---
The brightness is 110, so it is `.`. An eye sees green as brighter than
red or blue, so real programs weigh the three differently. The plain
average is a fair start.
```

</div>

## 16. Which families

Can you set `summary` to say which number families `value` belongs to,
the way the tutorial's last task does? For example
`"-3 is an integer, and so rational and real"`.

```python exec
id: which-families-1
value = -3

print(summary)
```

```inputs
summary
```

```solution
value = -3
is_integer = value == int(value)
is_natural = is_integer and value >= 0
if is_natural:
    summary = f"{value} is natural, and so an integer, rational and real"
elif is_integer:
    summary = f"{value} is an integer, and so rational and real"
else:
    summary = f"{value} is rational and real, but not an integer"
print(summary)
---
The families sit one inside the next, and that gives the code its shape:
the first test that comes out true gives the most exact answer.
```

## 17. Is every float rational

The tutorial's classifier says every Python float is rational. Is that
true?

<details class="dl-answer"><summary>one good answer</summary>

For the floats themselves, yes. Apart from a few special values, such as
infinity, every float is a whole number times a power of two, and that is
a fraction.

For the numbers the floats *stand for*, no. `math.pi` is a float, and π is
irrational, so the float is only a rational number close to π. A computer
cannot store an irrational number exactly: every number it stores is
rational, whether or not the thing it stands for is.

</details>

## 18. A possible triangle

A triangle is possible when each side is shorter than the other two added
together. Can you set `possible` for any three sides?

```python exec
id: a-possible-triangle-1
a = 1
b = 10
c = 2

print(possible)
```

```inputs
possible
```

```solution
a = 1
b = 10
c = 2
possible = a + b > c and a + c > b and b + c > a
print(possible)
---
All three comparisons are needed. Checking only `a + b > c` lets 1, 10, 2
through, because the long side is not the one in the `c` place.
```
