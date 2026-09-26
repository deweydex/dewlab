---
title: "When Python says no: reading error messages — Practice"
practice_for: when-python-says-no
year: "2026-2027"
version: 2026.09.25.1
---

# When Python says no: reading error messages — Practice

Most cells on this page are meant to fail, the way they were on the
tutorial page. Each problem says what kind it is: **Predict**, **Make**,
**Fix**, **Explain** or **Another way**. Before you open an answer, try
the routine: read the last line, find the line it names, ask which of
the four questions it is about, change one thing, and run again. If red
text still worries you a little, come back to that routine. This page
is a place to practise it.

## Warm-up

**1. Predict.** Before you run this cell, say which kind of error it
will give, and what Python will suggest.

```python exec
id: when-python-practice-typo
pixel_count = 28
print(pixel_cuont)
```

<details class="dl-answer"><summary>answer</summary>

```text
NameError: name 'pixel_cuont' is not defined. Did you mean: 'pixel_count'?
```

The name on line 2 has the `o` and the `u` swapped, so it points at
nothing. Python looks for a name that is spelled nearly the same, and
suggests `pixel_count`.

</details>

<aside class="dl-note" id="when-python-practice-note-did-you-mean">

**A newer kind of help.** Python has not always suggested a name. The
"Did you mean" line arrived with Python 3.10, in October 2021. When a
name points at nothing, Python searches the names that do exist for one
spelled nearly the same.

</aside>

**2. Explain.** A traceback can be many lines long. Why do we start
reading it at the last line?

<details class="dl-answer"><summary>answer</summary>

The last line says what went wrong: the kind of error, and a sentence
about what happened. Everything above it says where, and how the program
got there. When we know *what* happened, we know what to look for in
the *where*. The places above are listed oldest first ("most recent call
last"), so the bottom is also where Python stopped.

</details>

**3. Fix.** A display runs these steps when it is switched on. The
cell will not run. Read the message, then fix it so that it prints both
steps.

```python exec
id: when-python-practice-startup
def startup_steps():
print("Light every segment for one second.")
    print("Show 0000.")


startup_steps()
```

<details class="dl-answer"><summary>answer</summary>

The message is:

```text
IndentationError: expected an indented block after function definition on line 1
```

Both steps belong to the function, so both must be pushed in by the
same amount:

```python
def startup_steps():
    print("Light every segment for one second.")
    print("Show 0000.")


startup_steps()
```

Many devices light every segment for a moment when they start. This
shows at once if a segment is broken.

</details>

**4. Another way.** A game's score display has this line, which gives a
`TypeError`:

```python
goals = 14
print("Goals this season: " + goals)
```

Find two different ways to fix it. Try both in the cell below.

```python exec
id: when-python-practice-goals
goals = 14
print("Goals this season: " + goals)
```

<details class="dl-answer"><summary>answer</summary>

```python
goals = 14
print("Goals this season: " + str(goals))
print("Goals this season:", goals)
```

Both lines print `Goals this season: 14`. The first turns the number
into a string, so `+` joins two strings. The second gives `print` two
things, separated by a comma, and `print` puts a space between them.

</details>

## Core

**5. Predict.** The display on a DART train shows the stops. Will the
first line of this cell print? Say your answer before you run it.

```python exec
id: when-python-practice-dart
print("Leaving Bray now")
print("Next stop: Shankill")
print("Arriving at Dún Laoghaire)
```

<details class="dl-answer"><summary>answer</summary>

No. Nothing prints at all.

```text
  File "<cell when-python-practice-dart>", line 3
    print("Arriving at Dún Laoghaire)
          ^
SyntaxError: unterminated string literal (detected at line 3)
```

The string on line 3 opens with a quote mark and never closes, so this
cell is not valid Python. Python reads the whole cell before running
any of it, so a SyntaxError on the last line stops the first line too.
There is no "Traceback" line at the top, because nothing ran.

</details>

**6. Explain.** A GPS logger records how far you went, in metres, and
how long it took, in seconds, and reports your speed. Run the cell. The
first report works and the second does not. Schlomo, who is learning
Python too, says line 2 must be the problem, because that is where
Python stopped. Where does his idea work, and where does it stop
working? Which line failed, and which line is responsible? Answer in the comments at the end.

```python exec
id: when-python-practice-speed
def speed(metres, seconds):
    return metres / seconds


def report(metres, seconds):
    print("Speed:", speed(metres, seconds), "metres per second")


report(300, 60)
report(300, 0)

# The line that failed:
# The line that is responsible:
```

<details class="dl-answer"><summary>answer</summary>

The first report prints `Speed: 5.0 metres per second`. Then:

```text
Traceback (most recent call last):
  File "<cell when-python-practice-speed>", line 10, in <module>
    report(300, 0)
    ~~~~~~^^^^^^^^
  File "<cell when-python-practice-speed>", line 6, in report
    print("Speed:", speed(metres, seconds), "metres per second")
                    ~~~~~^^^^^^^^^^^^^^^^^
  File "<cell when-python-practice-speed>", line 2, in speed
    return metres / seconds
           ~~~~~~~^~~~~~~~~
ZeroDivisionError: division by zero
```

Schlomo's idea works for half of the question. Line 2, inside `speed`,
is the line that failed, because the division happens there. But the line
responsible is line 10, `report(300, 0)`, which asked for a speed over
0 seconds. Line 2 did its job for `report(300, 60)`. Most people start
with his idea. The traceback leads us from line 2 back to line 10.

</details>

**7. Fix.** This cell should print the average rainfall over three
days. It stops with an error instead. Find why, and change it.

```python exec
id: when-python-practice-rain
monday_mm = 4.2
tuesday_mm = 0.0
wednesday_mm = 7.5
average_mm = (monday_mm + tuesday_mm + wendesday_mm) / 3
print("Average rainfall:", round(average_mm, 1), "mm")
```

<details class="dl-answer"><summary>answer</summary>

```text
NameError: name 'wendesday_mm' is not defined. Did you mean: 'wednesday_mm'?
```

On line 4, `wendesday_mm` has two letters swapped. Change it to
`wednesday_mm`, and the cell prints `Average rainfall: 3.9 mm`. The sum
is $4.2 + 0.0 + 7.5 = 11.7$, and $11.7 \div 3 = 3.9$.

</details>

**8. Make.** A small game keeps a score. In the cell below, write three
short lines, each one about the score, and each one causing a different
kind of error: a `NameError`, a `TypeError` and a `ZeroDivisionError`.
Run them one at a time: put a `#` in front of the other two lines while
you run each one.

```python exec
id: when-python-practice-make-errors
score = 250
# your three lines here
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. For a `NameError`, use a name that was never given a value.
2. For a `TypeError`, use a move between two kinds of value that do not
   go together.
3. For a `ZeroDivisionError`, divide by something that is zero.

**Think about:** which of the four questions each error is about.

**Try this next:** can you make a `SyntaxError` with a single character?

</details>

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Yours may be different and work too.

```python
score = 250
print(scor)                 # NameError: scor was never named
print("Score: " + score)    # TypeError: joining a string and an int
print(score / (score - 250))  # ZeroDivisionError: score - 250 is 0
```

Each line alone raises the error named in its comment. And one
character is enough for a `SyntaxError`: delete a closing bracket, or a
quote mark.

</details>

**9. Predict.** A game keeps the number of lives as `"3"`, because it
was read from a settings file. What does this print? Is it an error?

```python exec
id: when-python-practice-lives
lives = "3"
print(lives * 2)
```

<details class="dl-answer"><summary>answer</summary>

It prints `33`, and there is no error.

`lives` is a string, and `*` between a string and a whole number writes
the string out that many times, like `3 * "ha "` on
[Four questions for any puzzle](tutorial:four-questions). So Python
does exactly what it was asked. The move is allowed in the space of
strings. It is not the move we meant.

This is worse than an error. An error stops and tells us. A wrong
answer with no error does not stop, and says nothing. `int(lives) * 2` gives `6`.

</details>

**10. Explain.** A student writing a program in C sees this message:

```text
scores.c:12:9: error: 'totl' undeclared (first use in this function)
```

Which file, which line, and what went wrong? Which Python error is the
closest to this one?

<details class="dl-answer"><summary>answer</summary>

The file is `scores.c`, the line is 12, and the 9 is the column, the
place along the line. The problem is that the name `totl` was never
declared, which in C means it was never named before it was used.

The closest Python error is a `NameError`. The difference is when it is
found. The C compiler finds it before the program runs, and Python
finds it when it reaches that line.

</details>

## Stretch

**11. Fix.** On [Everything is ones and zeros](tutorial:everything-is-ones-and-zeros)
we built `to_hex`. Here a brightness has come from a form, as text.
Run the cell. The error is a kind we have not met. Read it anyway, and
fix the cell so it prints `FF`.

```python exec
id: when-python-practice-hex
brightness = "255"
print(to_hex(brightness))
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Read the last line. What kind of value does it say it was given?
2. What kind of value does `to_hex` promise to work with?
3. `float()` turns text into a float. Is there a matching way to turn
   text into a whole number?

**Think about:** the words after the colon told you the fix, even
though the kind of error was new.

**Try this next:** what happens with `to_hex(int("twelve"))`?

</details>

<details class="dl-answer"><summary>answer</summary>

The last line says:

```text
ValueError: Unknown format code 'X' for object of type 'str'
```

A `ValueError` means a function was given a value it cannot work with.
The important words are at the end. They say the object
was a `str`, a string. `to_hex` promises to work with a whole number,
so turn the text into one with `int()`:

```python
brightness = int("255")
print(to_hex(brightness))
```

This prints `FF`. We had never seen `ValueError` before, and the message
still told us what was wrong. That is why we read the last line
first.

</details>

**12. Another way.** A paint program fills an image of 120 pixels. It
has painted 45 pixels red and 75 blue, and it shares 50 seconds among
the rows it still has to paint. The cell stops with a
`ZeroDivisionError` on line 7. The traceback says where it stopped, but
not where the 0 came from. Find the responsible line a second way: add
`print` lines that show the value of each name, and run again.

```python exec
id: when-python-practice-paint
pixels = 120
painted_red = 45
painted_blue = 75
left = pixels - painted_red - painted_blue
pixels_per_row = 10
rows_needed = left / pixels_per_row
seconds_per_row = 50 / rows_needed
```

<details class="dl-answer"><summary>answer</summary>

```python
pixels = 120
painted_red = 45
painted_blue = 75
left = pixels - painted_red - painted_blue
print("left:", left)
pixels_per_row = 10
rows_needed = left / pixels_per_row
print("rows_needed:", rows_needed)
```

This prints `left: 0` and `rows_needed: 0.0`. Every pixel is painted,
so line 4 makes `left` zero, and the 0 travels down to line 7. Line 7
has no mistake in it. The question it asks has no answer when no rows
are left. You can also print values to follow the trail, and this works
even when there is no error to read.

</details>

**13. Predict.** Your toolkit's `digit_at` from
[Numbers a computer can hold](tutorial:numbers-a-computer-can-hold)
takes a number and a place. What do you think happens here? Which of
the four questions is the error about?

```python exec
id: when-python-practice-missing-place
print(digit_at(2026))
```

<details class="dl-answer"><summary>answer</summary>

```text
TypeError: digit_at() missing 1 required positional argument: 'place'
```

`digit_at` promises the digit of a number in a given place. We gave
only the number. So this is about *what is promised*. A function's
promise holds only when it gets everything it asked for. An *argument*
is Python's word for a value given to a function when it is called.
`digit_at(2026, 0)` keeps the promise, and gives `6`. The base could be
left out, because it has a default value, 10.

</details>

**14. Make.** Write a cell with exactly three mistakes of three
different kinds, for a friend to fix. Before you run it, write down the
order in which Python will report them. Then run it and fix one
mistake at a time, to check your order.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Choose one mistake Python finds before it runs anything, such as a
   missing bracket.
2. Choose two it finds while running, such as a misspelled name and a
   division by zero.
3. Remember that Python runs from the top down.

**Think about:** why one kind of mistake always comes first, wherever
it is in the cell.

**Try this next:** swap the order of your two running mistakes. Does the
order of the reports change?

</details>

<details class="dl-answer"><summary>answer</summary>

Here is one:

```python
pixels = 12
width = 0
print("Rows:", pixels // width)
print("Pixels:", pixls
```

Python reports the `SyntaxError` on line 4 first, because it reads the
whole cell before running any of it. Once the bracket is closed, the
`ZeroDivisionError` on line 3 comes next, because line 3 runs before
line 4. Once `width` is not zero, the `NameError` for `pixls` on line 4
comes last. This is one answer. Yours will be different, and the
order of its reports follows the same rule. A mistake Python finds while reading always comes first.
After that, running mistakes come in the order of the lines.

</details>

**15. Explain.** This page on error messages comes in the first
unit of the course. Some courses leave errors until later, and explain
each one when it happens. If you were planning a course for people who are
new to programming, where would you put a page like this one: in the first
week, after a few weeks, or nowhere, with errors met one at a time? Give a
reason, and say what your choice costs.

<details class="dl-answer"><summary>answer</summary>

Here is one answer. It looks at a few things.

- **In the first week.** Errors arrive on the first day anyway, and a
  reader who expects to fail may read red text as a mark against them.
  If they read this page early, that changes. The cost is that, with
  little code written, most of the examples have to be made up.
- **After a few weeks.** By then a reader has met real errors of their
  own, and the page can use them. The cost is that nobody explains the
  red text in those first weeks.
- **Nowhere, one error at a time.** Each error is met in a real place,
  when it matters. The cost is that nobody may ever say the routine
  that works for every error, last line first.

Whichever you choose, say who the course is for, because that changes
which cost matters most.

</details>
