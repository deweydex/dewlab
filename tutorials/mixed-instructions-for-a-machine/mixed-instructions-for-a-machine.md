---
title: "Mixed problems: instructions for a machine"
practice_across:
  - four-questions
  - recipes-are-algorithms
  - numbers-a-computer-can-hold
  - everything-is-ones-and-zeros
  - when-python-says-no
year: "2026-2027"
version: 2026.09.25.1
---

# Mixed problems: instructions for a machine

These problems draw on every page of Unit 1, and none of them says which
page it needs. Working that out is part of the problem. When you are not
sure where to start, the four questions are always allowed: what is
named here, what is promised, what happens when, and what does this
space let us do?

In the middle of the page, you build the unit's project: a digit
display, like the clock on a microwave, drawn in text. Stage 1 is a
seven-segment display, in problems 7 to 11. Stage 2, a small pixel
font, is in the Stretch section, for when you want more. It may feel
like a lot of pieces at first. Every piece is one you have already met,
so when one stops you, ask the four questions of it, or open its hint.

Each problem says what kind it is: **Predict** (say what a cell will
print, then run it), **Make** (build something small), **Fix** (find
why code that looks fine does something else, and change it), **Explain** (answer in words) or **Another way** (reach the
same answer by a second route, or find the space where a "wrong" answer
is right). Answers are in the folds, and each is one way through, not
the only one.

## Your toolkit

Your toolkit from this unit is loaded on this page: `digit_at`,
`to_binary`, `to_hex` and `pixel_row`. Run this cell to check that all
four are there. If one of them gives a `NameError`, its page is where to
build it.

```python exec
id: mixed-instructions-toolkit-check
print(digit_at(2026, 0))
print(to_binary(13))
print(to_hex(255))
print(pixel_row(9))
```

This cell is a scratchpad for any problem below. Change it as much as you
like.

```python exec
id: mixed-instructions-scratchpad
print(3 * "#")
```

## Warm-up

**1. Predict.** What does each line print? Say all three answers, then
run them in the scratchpad.

```python
print(3 * "#")
print(7 // 2)
print(7 / 2)
```

<details class="dl-answer"><summary>answer</summary>

`###`, then `3`, then `3.5`.

- `*` with a string writes it out that many times, as on
  [Four questions for any puzzle](tutorial:four-questions): here, three
  lit pixels.
- `//` divides and keeps only the whole part, an int.
- `/` always gives a float, even when the answer could be whole.

</details>

**2. Another way.** In the counting numbers ℕ, $3 - 5$ has no answer.
Find a space where it does have one, and a place in daily life where you
would meet that answer.

<details class="dl-answer"><summary>answer</summary>

In the integers ℤ, which include the negative whole numbers,
$3 - 5 = -2$. The weather gives one place to meet it: it is 3 °C in the
evening, and by morning the temperature has fallen 5 degrees, to −2 °C.
Python's ints are a space with negative numbers in it, so
`print(3 - 5)` gives `-2`.

</details>

**3. Make.** Use your toolkit to write the year 2026 in binary and in
hexadecimal.

<details class="dl-answer"><summary>answer</summary>

```python
print(to_binary(2026))
print(to_hex(2026))
```

This prints `11111101010` and `7EA`. The hex form is much shorter: 11
bits become 3 hex digits, since each hex digit stands for four bits.

</details>

**4. Fix.** A robot pen draws on paper. This cell should print the
pen's two steps and then `Done.`. It prints only `Done.`, with no error.
Find why, and change it.

```python exec
id: mixed-instructions-pen
def draw_square(size_cm):
    print("Put the pen down.")
    print("Draw 4 sides of", size_cm, "cm, turning left after each.")


draw_square
print("Done.")
```

<details class="dl-answer"><summary>answer</summary>

Line 6 names the function but does not call it. A call needs brackets,
with the value for `size_cm` inside them:

```python
draw_square(3)
print("Done.")
```

This prints `Put the pen down.`, then `Draw 4 sides of 3 cm, turning
left after each.` and `Done.`. There was no error, because naming a
function without calling it is allowed. It does nothing, the same way
reading the title of a recipe card does not make any tea.

</details>

**5. Explain.** A robot vacuum cleaner is told: "Clean the floor until
it is clean." Why is this a poor step for a robot? Rewrite it as a
better one.

<details class="dl-answer"><summary>answer</summary>

"Clean" has no single meaning, and the robot cannot see dirt the way a
person does. Two robots could stop at different times, and one might
never stop at all. A step a robot can follow has one meaning, and a repeated step
needs a clear end.

A better version: "Drive over every part of the floor once. If the dust
sensor still finds dust, repeat, at most 3 times." Now every part can
be checked, and the steps must end.

</details>

## Core

**6. Predict.** What does this print: 750 or 1250?

```python
row_width = 250
rows = 3
pixels = rows * row_width
rows = 5
print(pixels)
```

<details class="dl-answer"><summary>answer</summary>

`750`. On line 3, Python works out `3 * 250` and names the result
`pixels`. Line 4 points `rows` at a new value, but `pixels` was worked
out already, and nothing tells Python to work it out again. A value is
worked out when its line runs, not later.

</details>

The next five problems build Stage 1 of the project: a seven-segment
display that shows 2026. Each answer fold has code you can copy, so if
one step will not come, you can still go on to the next.

**7. Make.** Use `digit_at` to print the four digits of 2026, from left
to right. Then print `math.log10(2026)`, and use it to say why 2026
needs four digits on the display.

<details class="dl-answer"><summary>answer</summary>

```python
import math

print(digit_at(2026, 3), digit_at(2026, 2), digit_at(2026, 1), digit_at(2026, 0))
print(math.log10(2026))
```

This prints `2 0 2 6`, then about `3.3`. So $10^3 = 1000$ is below 2026,
and $10^4 = 10000$ is above it. Any number from 1000 to 9999 has 4
digits: its logarithm, base 10, rounded down, plus 1.

</details>

**8. Explain.** Schlomo, who is learning Python too, says: "Seven
segments make 128 patterns, so a seven-segment display can show 128
different digits." Where does his idea work, and where does it stop
working?

<details class="dl-answer"><summary>answer</summary>

His idea works for the patterns and stops working for the digits. Each segment
is on or off, so there are $2^7 = 128$ patterns. But only ten of them
are the digits 0 to 9. Most of the others do not look like anything we
would read.

Some of them are useful all the same. Many seven-segment displays show
all sixteen hex digits, with A, b, C, d, E and F for the letters, some
of them lower case so that they do not look like 8 or 0. So Schlomo's
count of patterns holds. What a pattern *means* is a question for the people
who read it.

</details>

**9. Make.** A display keeps each digit's pattern as one byte, with
segment a as the ones bit, b the twos, and so on up to g, the 64s. All
ten patterns fit in one number, one byte each, the way `#FF8800` holds
three bytes. The digit 0's pattern is the last byte, `3F`, and the digit
9's is the first, `6F`. Run the cell. Then use `digit_at` in base 256 to
get the pattern for the digit 8, and print it in binary and in hex.

```python exec
id: mixed-instructions-segments
segment_table = 0x6F7F077D6D664F5B063F


def mark(on, symbol):
    """Give symbol when on is 1, and a space when on is 0."""
    return symbol * on + " " * (1 - on)


def lit(digit, segment):
    """Give 1 if segment (0 for a, up to 6 for g) is lit in digit, else 0."""
    pattern = digit_at(segment_table, digit, 256)
    return digit_at(pattern, segment, 2)


def top_row(digit):
    """Give the top row of digit as three characters: segment a."""
    return " " + mark(lit(digit, 0), "_") + " "
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. One byte is 8 bits, which count up to 255. So a byte is one digit in
   base 256.
2. The digit 8's pattern is in place 8.
3. `digit_at(segment_table, 8, 256)` gives it as a number. Give that
   number to `to_binary` and to `to_hex`.

**Think about:** why the digit 8's pattern should be seven 1s.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
pattern = digit_at(segment_table, 8, 256)
print(to_binary(pattern))
print(to_hex(pattern))
```

This prints `1111111`, then `7F`: the 8 lights all seven segments. The
cell also made tools for the next problem. `mark` uses the string
repeat from the first page of this unit: `"_" * 1` is `"_"`, and
`"_" * 0` is empty.

</details>

**10. Make.** `top_row` draws segment a. Write `middle_row(digit)`,
which draws f, g and b, and `bottom_row(digit)`, which draws e, d and
c. Use `|` for an upright segment and `_` for a flat one. Then print
the three rows of an 8, one under another. The segments a to g are
numbered 0 to 6.

```python exec
id: mixed-instructions-rows
def middle_row(digit):
    """Give the middle row of digit: segments f, g and b."""
    ...


def bottom_row(digit):
    """Give the bottom row of digit: segments e, d and c."""
    ...
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Look at `top_row`. It joins three characters with `+`.
2. In the middle row, f is on the left, g in the middle, and b on the
   right. f is segment 5, g is 6 and b is 1.
3. In the bottom row, e is segment 4, d is 3 and c is 2.

**Think about:** why the names a to g are single letters here, when
names are usually words. (What would you call segment f?)

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def middle_row(digit):
    """Give the middle row of digit: segments f, g and b."""
    return mark(lit(digit, 5), "|") + mark(lit(digit, 6), "_") + mark(lit(digit, 1), "|")


def bottom_row(digit):
    """Give the bottom row of digit: segments e, d and c."""
    return mark(lit(digit, 4), "|") + mark(lit(digit, 3), "_") + mark(lit(digit, 2), "|")


print(top_row(8))
print(middle_row(8))
print(bottom_row(8))
```

This prints the 8:

```text
 _ 
|_|
|_|
```

The letters a to g are the names every seven-segment display uses, so
here a single letter is the clearest name there is.

</details>

**11. Make.** Now the whole display. Print 2026 as four seven-segment
digits side by side, with a space between digits. Then change the
number to one of your own.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Give each digit of the number a name with `digit_at`: `thousands`,
   `hundreds`, `tens`, `ones`.
2. The display's top line is the four top rows joined with `+`, with
   `" "` between them.
3. Do the same for the middle line and the bottom line.

**Think about:** what happens to the order of the steps if you print
one whole digit, then the next?

**Try this next:** what does your display show for 12345, and why?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
number = 2026
thousands = digit_at(number, 3)
hundreds = digit_at(number, 2)
tens = digit_at(number, 1)
ones = digit_at(number, 0)
print(top_row(thousands) + " " + top_row(hundreds) + " " + top_row(tens) + " " + top_row(ones))
print(middle_row(thousands) + " " + middle_row(hundreds) + " " + middle_row(tens) + " " + middle_row(ones))
print(bottom_row(thousands) + " " + bottom_row(hundreds) + " " + bottom_row(tens) + " " + bottom_row(ones))
```

This prints:

```text
 _   _   _   _ 
 _| | |  _| |_ 
|_  |_| |_  |_|
```

Text comes out line by line, top to bottom, so each line needs a piece
of every digit. That is why we print row by row, not digit by digit.
For the "try this next", 12345 shows `2345`: the 1 in place 4 has
nowhere to go. Unit 3's loops will shorten the three long lines.

</details>

**12. Fix.** The number came from a box on a web page, as text. Run the
cell, read the last line of the error, and fix the cell.

```python exec
id: mixed-instructions-form-total
number = "2026"
print(digit_at(number, 0))
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Read the last line. What kind of error is it?
2. Which kind of value does it name that should not be there?
3. Which line of *your* cell gave `digit_at` that value?
4. Which function turns text into a whole number?

**Think about:** the line that failed is inside `digit_at`. The line
responsible is in your cell.

**Try this next:** what happens if the box gives `"2,026"`, with a
comma?

</details>

<details class="dl-answer"><summary>answer</summary>

The last line is:

```text
TypeError: unsupported operand type(s) for //: 'str' and 'int'
```

This is the message from
[When Python says no](tutorial:when-python-says-no): `//` cannot divide
a string by a number. The line that failed is inside `digit_at`, but
the line responsible is line 1 of this cell, which made `number` a
string. Turn it into a number first:

```python
number = int("2026")
print(digit_at(number, 0))
```

This prints `6`. For the "try this next", `int("2,026")` stops with a
`ValueError`: a comma is not a digit.

</details>

## Stretch

**13. Predict.** `to_binary` and `to_hex` promise to work with whole
numbers of 0 or more. What happens if we step outside that space? Say
what you expect, then run each line on its own.

```python
print(to_binary(-5))
print(to_hex(2.5))
```

<details class="dl-answer"><summary>answer</summary>

The first line prints `-101`, with no error. The second stops with:

```text
ValueError: Unknown format code 'X' for object of type 'float'
```

So one broken promise gives an error, and the other gives an answer we
never agreed on: `-101` is not the string of 0s and 1s that `to_binary`
promised. A promise holds only inside its space. Outside it, anything
may happen, and an error is the better of the two outcomes, because it
tells us.

</details>

**14. Make.** Stage 2 of the project: a pixel font. On
[Everything is ones and zeros](tutorial:everything-is-ones-and-zeros),
a digit was 7 hex digits, one per row. Here are the glyphs, the drawn
shapes, for the digits of 2026. Write `glyph_row(glyph, row)`, which
gives one row of a glyph as pixels, with row 0 at the top. Then print
2026 in pixels, the four glyphs side by side.

```python exec
id: mixed-instructions-font
two = 0x691248F
zero = 0x6999996
six = 0x688E996
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Row 0, the top row, is the hex digit in place 6. Row 6 is place 0.
   So row `row` is place `6 - row`.
2. `digit_at(glyph, 6 - row, 16)` gives that row's 4 bits as a number,
   and `pixel_row` draws it.
3. Each of the 7 lines of the display joins one row from each glyph.

**Think about:** why the pixel font needs 7 print lines, and the
seven-segment display only 3.

**Try this next:** design a glyph for 3 on the 4 by 7 grid, and draw
2023.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def glyph_row(glyph, row):
    """Give row (0 at the top, 6 at the bottom) of a 4 by 7 glyph as pixels."""
    return pixel_row(digit_at(glyph, 6 - row, 16))


def display_row(row):
    """Give one row of 2026, all four glyphs side by side."""
    return glyph_row(two, row) + " " + glyph_row(zero, row) + " " + glyph_row(two, row) + " " + glyph_row(six, row)


print(display_row(0))
print(display_row(1))
print(display_row(2))
print(display_row(3))
print(display_row(4))
print(display_row(5))
print(display_row(6))
```

This prints:

```text
.##. .##. .##. .##.
#..# #..# #..# #...
...# #..# ...# #...
..#. #..# ..#. ###.
.#.. #..# .#.. #..#
#... #..# #... #..#
#### .##. #### .##.
```

The seven-segment display needed only 3 lines, because a segment is a
whole bar. The pixel font needs one line for every row of pixels.

</details>

**15. Another way.** Schlomi, who is also learning Python, has an idea.
"The segment table held ten bytes in one number. Python's whole numbers
never run out, so the whole pixel font can be one number too, one glyph
of 7 hex digits after another." Here is her number, with 9 on the left
and 0 on the right. Does her idea work? Use `digit_at` to get the glyph
for 2 out of it.

```python exec
id: mixed-instructions-font-number
font = 0x69971166996996F122444688E996F8E11961359F116916196691248F26222276999996
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. In the segment table, each pattern was one digit in base 256, which
   is $2^8$, one byte.
2. Here, each glyph is 7 hex digits. What base makes one glyph one
   digit?
3. Try `digit_at(font, 2, 16 ** 7)`, and give the answer to `to_hex`.

**Think about:** how many hex digits long her number is.

</details>

<details class="dl-answer"><summary>answer</summary>

It works. Each glyph is 7 hex digits, so in base $16^7$ each glyph
is one digit, and `digit_at` can pick out any of them:

```python
print(to_hex(digit_at(font, 2, 16 ** 7)))
print(to_hex(digit_at(font, 8, 16 ** 7)))
```

This prints `691248F`, the 2, then `6996996`, the 8. Her number has 70
hex digits, which is 280 bits. In many languages, an ordinary whole
number stops at 64 bits. Python does not mind at all.

</details>

**16. Explain.** Schlomo says: "Python is broken. `1 + 2 == 3` is
`True`, but `0.1 + 0.2 == 0.3` is `False`." Using what this unit taught
about the spaces numbers live in, explain what is happening, and whether
anything is broken.

<details class="dl-answer"><summary>answer</summary>

Nothing is broken, and Schlomo's surprise is a fair one. The two sums
live in different spaces.

`1`, `2` and `3` are ints. Python keeps whole numbers exactly, in
binary, so `1 + 2` is exactly `3`.

`0.1`, `0.2` and `0.3` are floats. A float is a binary fraction, built
from halves, quarters, eighths and so on, and a tenth cannot be made
exactly from those. So Python keeps a number very close to 0.1, and the
tiny differences show up in the sum: `0.30000000000000004`.

In the space of fractions, ℚ, `0.1 + 0.2 == 0.3` is true. In the space
of floats, the question to ask is "close enough?", for example
`round(0.1 + 0.2, 10) == 0.3`.

</details>

**17. Fix.** A game controller sends the state of four buttons as four
bits. This function should turn them back into a number, so `1, 1, 0, 1`
should give 13. The test fails. Find why, and change it.

```python exec
id: mixed-instructions-bits
def from_bits(bit_8, bit_4, bit_2, bit_1):
    """The number made by four bits, worth 8, 4, 2 and 1."""
    return bit_8 * 2 ** 3 + bit_4 * 2 ** 2 + bit_2 * 2 + bit_1 * 2 ** 1


print(from_bits(1, 1, 0, 1))
assert from_bits(1, 1, 0, 1) == 13
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The cell prints 14, one too many. Which bit is 1 here, and worth 1?
2. Work out each of the four parts of the sum on its own.
3. What is $2^1$? What should the last bit be worth?

**Think about:** the names promise worths of 8, 4, 2 and 1. Does the
code keep that promise?

**Try this next:** add a test that uses only the last bit,
`from_bits(0, 0, 0, 1)`. Would it have caught the problem alone?

</details>

<details class="dl-answer"><summary>answer</summary>

The last part is `bit_1 * 2 ** 1`, which is worth 2, not 1. The ones
column is $2^0 = 1$:

```python
def from_bits(bit_8, bit_4, bit_2, bit_1):
    """The number made by four bits, worth 8, 4, 2 and 1."""
    return bit_8 * 2 ** 3 + bit_4 * 2 ** 2 + bit_2 * 2 ** 1 + bit_1 * 2 ** 0


print(from_bits(1, 1, 0, 1))
assert from_bits(1, 1, 0, 1) == 13
assert from_bits(0, 0, 0, 1) == 1
assert from_bits(1, 1, 1, 1) == 15
```

This prints `13`, and every test passes. Python saw nothing wrong with
the first version: only the test noticed. Without the test, 14 would have
looked like a fine answer. That is what a test is for.

</details>

**18. Make.** A Gaelic football or hurling score has two parts, goals
and points, and a goal is worth 3 points. So a scoreboard showing
`2-11` means two goals and eleven points: 17 points in all. Write
`gaa_total(goals, points)`. Then use it on a match where the board
shows `1-15` against `3-08`. Before you run it, which team do you think
is ahead?

```python exec
id: mixed-instructions-gaa
def gaa_total(goals, points):
    """Give a GAA score as one number of points: a goal is worth 3."""
    ...


print(gaa_total(1, 15), gaa_total(3, 8))
```

Then draw `2-11` on the display from problem 11. The dash is a
"digit" with only segment g lit.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The total is three for every goal, plus the points.
2. For the display, the goals take one digit and the points take two.
   Name them with `digit_at`, as in problem 11.
3. The dash has no pattern in `segment_table`. Its three rows are
   `"   "`, `" _ "` and `"   "`.

**Think about:** the team with more goals is behind. How many points
would the team with three goals need to catch up?

</details>

<details class="dl-answer"><summary>one way through</summary>

```python
def gaa_total(goals, points):
    """Give a GAA score as one number of points: a goal is worth 3."""
    return 3 * goals + points


print(gaa_total(1, 15), gaa_total(3, 8))

goals, points = 2, 11
tens = digit_at(points, 1)
ones = digit_at(points, 0)
print(top_row(goals) + " " + "   " + " " + top_row(tens) + " " + top_row(ones))
print(middle_row(goals) + " " + " _ " + " " + middle_row(tens) + " " + middle_row(ones))
print(bottom_row(goals) + " " + "   " + " " + bottom_row(tens) + " " + bottom_row(ones))
```

The first line prints `18 17`. The team with one goal is ahead by a
point: fifteen points beat eight, even with two goals' help. The
display shows:

```text
 _             
 _|  _    |   |
|_        |   |
```

A score in two parts works like minutes and seconds on the microwave
timer: to compare two of them, turn both into the smaller unit first.

</details>
