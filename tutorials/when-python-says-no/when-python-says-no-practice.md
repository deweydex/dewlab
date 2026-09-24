---
title: "When Python says no: reading error messages — Practice"
practice_for: when-python-says-no
year: "2026-2027"
version: 2026.09.24.1
---

# When Python says no: reading error messages — Practice

Most cells on this page are meant to fail, the way they were on the
tutorial page. Each problem says what kind it is: **Predict**, **Make**,
**Fix**, **Explain** or **Another way**. Before you open an answer, try
the routine: read the last line, find the line it names, ask which of
the four questions it is about, change one thing, and run again.

## Warm-up

**1. Predict.** Before you run this cell, say which kind of error it
will give, and what Python will suggest.

```python exec
id: when-python-practice-playlist
playlist_length = 12
print(playlist_lenght)
```

<details class="dl-answer"><summary>answer</summary>

```text
NameError: name 'playlist_lenght' is not defined. Did you mean: 'playlist_length'?
```

The name on line 2 has the `h` and the `t` swapped, so it points at
nothing. Python looks for a name that is spelled nearly the same, and
suggests `playlist_length`.

</details>

**2. Explain.** A traceback can be many lines long. Why do we start
reading it at the last line?

<details class="dl-answer"><summary>answer</summary>

The last line says what went wrong: the kind of error, and a sentence
about what happened. Everything above it says where, and how the program
got there. Knowing *what* first tells us what to look for when we read
the *where*. The places above are listed oldest first ("most recent call
last"), so the bottom is also where Python stopped.

</details>

**3. Fix.** This recipe card will not run. Read the message, then fix
it so that it prints both steps.

```python exec
id: when-python-practice-oven
def oven_steps():
print("Heat the oven to 200 degrees.")
    print("Wait 10 minutes.")


oven_steps()
```

<details class="dl-answer"><summary>answer</summary>

The message is:

```text
IndentationError: expected an indented block after function definition on line 1
```

Both steps belong to the function, so both must be pushed in by the
same amount:

```python
def oven_steps():
    print("Heat the oven to 200 degrees.")
    print("Wait 10 minutes.")


oven_steps()
```

</details>

**4. Another way.** A scoreboard program has this line, which gives a
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
Neither is more correct: they are two routes out of the same problem.

</details>

## Core

**5. Predict.** Will the first line of this cell print? Say your answer
before you run it.

```python exec
id: when-python-practice-bus
print("Leaving Bray now")
print("Next stop: Killiney")
print("Arriving at Dún Laoghaire)
```

<details class="dl-answer"><summary>answer</summary>

No. Nothing prints at all.

```text
  File "<cell when-python-practice-bus>", line 3
    print("Arriving at Dún Laoghaire)
          ^
SyntaxError: unterminated string literal (detected at line 3)
```

The string on line 3 opens with a quote mark and never closes, so this
cell is not valid Python. Python reads the whole cell before running
any of it, so a SyntaxError on the last line stops the first line too.
There is no "Traceback" line at the top, because nothing ran.

</details>

**6. Explain.** A running app works out your pace in minutes per
kilometre. Run the cell. The first report works and the second does
not. Which line failed? Which line is responsible? Answer in the
comment at the end.

```python exec
id: when-python-practice-pace
def pace(minutes, km):
    return minutes / km


def report(minutes, km):
    print("Your pace:", pace(minutes, km), "minutes per km")


report(30, 5)
report(30, 0)

# The line that failed:
# The line that is responsible:
```

<details class="dl-answer"><summary>answer</summary>

The first report prints `Your pace: 6.0 minutes per km`. Then:

```text
Traceback (most recent call last):
  File "<cell when-python-practice-pace>", line 10, in <module>
    report(30, 0)
    ~~~~~~^^^^^^^
  File "<cell when-python-practice-pace>", line 6, in report
    print("Your pace:", pace(minutes, km), "minutes per km")
                        ~~~~^^^^^^^^^^^^^
  File "<cell when-python-practice-pace>", line 2, in pace
    return minutes / km
           ~~~~~~~~^~~~
ZeroDivisionError: division by zero
```

The line that failed is line 2, inside `pace`, where the division
happens. The line responsible is line 10, `report(30, 0)`, which asked
for a pace over 0 km. Line 2 is fine: it worked for `report(30, 5)`.
The trail from line 10 to line 2 is exactly what the traceback shows.

</details>

**7. Fix.** This cell should print the average rainfall over three
days. It has one mistake. Fix it.

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

There are many good answers. Here is one set:

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
answer with no error goes on quietly. `int(lives) * 2` gives `6`.

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
found: the C compiler finds it before the program runs, and Python
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
The important words are at the end: the object
was a `str`, a string. `to_hex` promises to work with a whole number,
so turn the text into one with `int()`:

```python
brightness = int("255")
print(to_hex(brightness))
```

This prints `FF`. We had never seen `ValueError` before, and the message
still told us what was wrong. That is the point of reading the last
line first.

</details>

**12. Another way.** A concert venue plans its rows of seats. The cell
stops with a `ZeroDivisionError` on line 7. The traceback says where
it stopped, but not where the 0 came from. Find the responsible line a
second way: add `print` lines that show the value of each name, and run
again.

```python exec
id: when-python-practice-concert
tickets = 120
sold_online = 45
sold_at_door = 75
left = tickets - sold_online - sold_at_door
seats_per_row = 10
rows_needed = left / seats_per_row
cost_per_row = 50 / rows_needed
```

<details class="dl-answer"><summary>answer</summary>

```python
tickets = 120
sold_online = 45
sold_at_door = 75
left = tickets - sold_online - sold_at_door
print("left:", left)
seats_per_row = 10
rows_needed = left / seats_per_row
print("rows_needed:", rows_needed)
```

This prints `left: 0` and `rows_needed: 0.0`. Every ticket is sold, so
line 4 makes `left` zero, and the 0 travels down to line 7. Nothing is
wrong with line 7 at all: the question it asks has no answer when no
rows are needed. Printing values is a second way to follow the trail,
and it works even when there is no error to read.

</details>

**13. Predict.** Your toolkit's `split_bill` from
[Numbers a computer can hold](tutorial:numbers-a-computer-can-hold)
takes a total and a number of people. What do you think happens here?
Which of the four questions is the error about?

```python exec
id: when-python-practice-split
print(split_bill(60))
```

<details class="dl-answer"><summary>answer</summary>

```text
TypeError: split_bill() missing 1 required positional argument: 'people'
```

`split_bill` promises a share for a given total and a given number of
people. We gave only the total. So this is about *what is promised*: a
function's promise holds only when it gets everything it asked for. An
*argument* is Python's word for a value given to a function when it is
called. `split_bill(60, 4)` keeps the promise, and gives `15.0`.

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
price = 12
people = 0
print("Each pays", price / people)
print("Total:", prce
```

Python reports the `SyntaxError` on line 4 first, because it reads the
whole cell before running any of it. Once the bracket is closed, the
`ZeroDivisionError` on line 3 comes next, because line 3 runs before
line 4. Once `people` is not zero, the `NameError` for `prce` on line 4
comes last. A mistake Python finds while reading always comes first.
After that, running mistakes come in the order of the lines.

</details>
