---
title: "Reading an error message — Practice"
practice_for: reading-an-error-message
year: "2026-2027"
version: 2026.09.25.1
---

# Reading an error message — Practice

The answers are hidden until you open them. On this page, your
prediction is the exercise, and running the code is the marking. For
most questions, try to predict the error before you run the code.

Everything here uses only variables, types, arithmetic, strings,
`print`, `input` and `if`. There are no new tools to learn, only new
messages to read.

## Tools

There is nothing to set up here. Each question is its own cell, and most
of them are meant to fail.

```python exec
id: three-kinds-reminder-1
# A reminder of the three kinds, and how each announces itself.
print("Syntax error:  Python refuses before running anything.")
print("Runtime error: some of your program runs, then it stops.")
print("Logical error: it all runs, and the answer is wrong.")
```

## Which Kind?

For each one, is it a syntax error, a runtime error, a logical error, or
no error at all?

**1.** `if total > 10` followed by an indented `print(total)`

<details class="dl-answer"><summary>answer</summary>

Syntax error. The colon is missing after `10`, so Python cannot read
the line, and it never runs anything.

</details>

**2.** `result = 10 + "5"`

<details class="dl-answer"><summary>answer</summary>

Runtime error: a `TypeError`. The line is valid Python, but Python will
not add a number to a string.

</details>

**3.** `doubled = "5" * 2`, written by somebody who wanted the answer 10

<details class="dl-answer"><summary>answer</summary>

Logical error. It runs and gives back `"55"`, because `*` with a string
repeats the string.

Nothing is red, and the answer is wrong. This is the dangerous kind. It
is even worse than that: `5 * 2` gives 10, so the line looks correct
until the value turns out to be a string. A value that came from
`input()` is always a string.

</details>

**4.** `price = int("12")` then `print(price * 2)`

<details class="dl-answer"><summary>answer</summary>

No error. It prints 24. `int("12")` turns the string into the number 12.

</details>

**5.** `age = int("thirty")`

<details class="dl-answer"><summary>answer</summary>

Runtime error: a `ValueError`. `int` wants a string, and it got one. But
`"thirty"` is not written in digits, so `int` cannot turn it into a
number.

</details>

**6.** `average = total / count` where `count` is 0

<details class="dl-answer"><summary>answer</summary>

Runtime error: a `ZeroDivisionError`.

In real programs, this is the most common cause of that error. A count
turns out to be zero when the code expected it not to be. That happens
far more often than somebody typing `/ 0`.

</details>

## Naming the Error

Which error do you think each one raises? Predict, then run it.

**7.**

```python exec
id: naming-the-error-early-1
value = "12"
print(value + 3)
```

<details class="dl-answer"><summary>answer</summary>

`TypeError`. Python cannot add a string and an integer.

Notice that `value * 3` would work, and give `121212`. That is a
different kind of surprise.

</details>

**8.**

```python exec
id: naming-the-error-early-2
count = int("twelve")
```

<details class="dl-answer"><summary>answer</summary>

`ValueError`. The type is right, because `int` wants a string. But the
content of the string is not a number.

People mix these two up more than any other pair. A `TypeError` means
the wrong kind of thing. A `ValueError` means the right kind of thing,
with content Python cannot use.

</details>

**9.**

```python exec
id: naming-the-error-early-3
score = 72
print("Your score is", scroe)
```

<details class="dl-answer"><summary>answer</summary>

`NameError`. `scroe` was never created, because the name is misspelled.

The message ends with `Did you mean: 'score'?` Python noticed a name
that is close to the one you typed. Read to the end of a message before
you go looking for the problem yourself.

</details>

**10.** In some countries, people write a decimal comma: 12,50 and not
12.50.

```python exec
id: naming-the-error-early-4
typed = "12,50"
price = float(typed)
print(price)
```

<details class="dl-answer"><summary>answer</summary>

`ValueError`. Python only understands a decimal point. To Python,
`"12,50"` is a string, the right type for `float`, but with content it
cannot read as a number.

If `typed` came from `input()`, the person using the program did nothing
wrong. The program needs to tell them what to type, or check what they
typed.

</details>

**11.** The `%` operator gives the remainder after division.

```python exec
id: naming-the-error-early-5
print(17 % 0)
```

<details class="dl-answer"><summary>answer</summary>

`ZeroDivisionError`. Finding a remainder is a kind of division, and
nothing can be divided by zero. The description says
`integer modulo by zero`. Modulo is the name of the `%` operator, which
we met in [Algorithms, pseudocode and your first Python](tutorial:first-steps).

`17 // 0` raises the same kind of error.

</details>

## Reading a Traceback

**12.** In a traceback, where do you find the error that stopped the
program?

<details class="dl-answer"><summary>answer</summary>

The last line names it, and then describes it. The lines above it say
where it happened: the line number, and a copy of the line.

Read from the bottom. The top of a traceback is where Python starts its
report, and the bottom is what went wrong.

</details>

**13.** Run this. Can you find two things: the line that failed, and the
line that is *responsible*?

```python exec
id: reading-a-short-traceback-1
marks = 45
bonus = "5"
total = marks + bonus
print("Total:", total)
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Read the last line first. What kind of error is it?
2. Which line number does the traceback name? That is the line that
   failed.
3. What types are `marks` and `bonus`? Which line gave `bonus` its type?

</details>

<details class="dl-answer"><summary>answer</summary>

The line that failed is line 3, `total = marks + bonus`. That is where
the `TypeError` happened.

The line that is responsible is line 2, `bonus = "5"`, because it made
`bonus` a string. Line 3 is written correctly. It was given a value of
the wrong type.

</details>

**14.** A syntax error message puts its marker under a word that looks
fine. Where should you look?

<details class="dl-answer"><summary>answer</summary>

Just before it. Python complains at the moment it becomes sure that
something is wrong, and that is often a character or two after the real
mistake, or even on the next line.

</details>

**15.** Some output appeared above the traceback. What does that tell
you?

<details class="dl-answer"><summary>answer</summary>

It tells you that the error is a runtime error. Python read the whole
program, started to run it, and got that far before it stopped. A syntax
error prints nothing of yours at all, because nothing runs.

</details>

## When Nothing Looks Wrong

Each of these runs, and each one is wrong. Can you find the mistake?

**16.** Percentage change is measured against the old value. A price
that goes from 50 to 60 has gone up by 20%.

```python exec
id: when-nothing-looks-wrong-practice-1
old = 50
new = 60
change = (new - old) / new * 100
print("Change:", change, "%")
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Work it out by hand first: the price went up by 10. What is 10 as a
   percentage of 50?
2. Which number does the code divide by? Which number should it divide
   by?

</details>

<details class="dl-answer"><summary>answer</summary>

It divides by the new value, but percentage change is measured against
the *old* value. The code gives about 16.67%, and the right answer is
20%.

The wrong answer is close enough to look believable. That is exactly
why nobody notices it.

</details>

**17.** The pass mark is 50. Run the cell with `score` set to 49, then
50, then 51.

```python exec
id: when-nothing-looks-wrong-practice-2
score = 50
if score > 50:
    print(score, "is a pass")
else:
    print(score, "is a fail")
```

<details class="dl-answer"><summary>answer</summary>

If 50 is the pass mark, this code fails everyone who scored exactly 50.
It needs `>=`.

Logical errors live at boundaries. Always test the exact boundary, one
below it, and one above it.

</details>

**18.** What is the one habit that catches logical errors?

<details class="dl-answer"><summary>answer</summary>

Checking against an answer you already know.

Before you trust a program on numbers you cannot check, give it numbers
you can check. The average of 80, 90 and 70 is 80. Ten percent of 50 is
5. If the program disagrees, you have found something.

That habit is worth more than any tool.
[Designing and testing good functions](tutorial:building-reusable-tools), later in
the series, takes it further, into testing code properly.

</details>

## Fixing

**19.** This program has two mistakes. Can you fix it? Run it after each
fix.

```python exec
id: fixing-early-1
temperature = 25
if temperature > 20
    print("Warm")
else:
print("Cool")
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Run it, and fix only the line the message names.
2. Run it again. Is there a new message? Which line does it name now?
3. Look at the example in the tutorial: which lines need a colon, and
   which lines need to be indented?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
temperature = 25
if temperature > 20:
    print("Warm")
else:
    print("Cool")
```

The `if` line needs a colon, and `print("Cool")` needs to be indented
under `else:`.

Did you notice that Python only told you about the first mistake? It
stops at the first thing it cannot read. So after a fix, run the code
again. A new message does not mean the fix failed. It can mean Python
got further.

</details>

**20.** In a real program, `age` would come from
`input("How old are you? ")`. Can you fix the last line?

```python exec
id: fixing-early-2
age = "30"
print("Next year you will be " + age + 1)
```

<details class="dl-answer"><summary>answer</summary>

`age` is a string, so `age + 1` is a `TypeError`. Turn it into a number
first:

```python
age = "30"
print("Next year you will be", int(age) + 1)
```

The comma lets `print` show a string and a number side by side, so you
do not need to turn the number back into a string.

</details>

**21.** Why is an error message better news than no error message?

<details class="dl-answer"><summary>answer</summary>

Because an error message tells you where and what. A syntax error stops
you before anything happens. A runtime error names the line and the
reason.

A logical error tells you nothing. It may not be found for weeks, and by
then it has produced a great deal of confident, wrong output.

The red text is the computer helping you as much as it can.

</details>
