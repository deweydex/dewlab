---
title: "Reading an error message"
year: "2026-2027"
version: 2026.09.26.1
worlds:
  secret-messages: Codes and hidden messages, the kind spies and puzzle-setters make.
  pixel-art: Pictures made of small squares, the way a screen draws them.
covers:
  three-kinds-of-wrong:
    covers: [PDP-LO9]
  errors-python-catches-before-it-starts:
    covers: [PDP-LO9]
  errors-that-happen-while-it-runs:
    covers: [PDP-LO9]
  reading-a-traceback:
    covers: [PDP-LO9]
  when-nothing-looks-wrong:
    covers: [PDP-LO9]
---

# Reading an error message

This cell has a mistake in it. Before you run it, can you find it? Then run
it, and read everything that comes back.

```python exec
id: a-first-error-1
shift = 3
message = "HELLO"
print(mesage)
```

The last line of what comes back says `NameError: name 'mesage' is not
defined`, and then, most likely, `Did you mean: 'message'?`. Python read
the whole program, ran the first two lines, and stopped at the third,
because nothing called `mesage` exists. It says which line, which name,
and even what you probably meant.

By now you have written code that did not work. Everybody does, all the
time, and it never stops happening. What changes with experience is how
long it takes to find out why, and most of that is reading the message.
The message puts its most useful line at the bottom, writes in a style you
have not met yet, and sometimes points a little to the side of the real
problem. This page is about all three.

So here we break things on purpose. Most cells below are meant to fail, and
reading the failure is the exercise. Every cell uses only what we have met
so far: names, types, arithmetic, text, `print`, `input`, and `if`, `elif`
and `else`.

An error here is a fact about this line, on this run. It is not a fact
about whether you can learn to program.

## Three kinds of wrong

There are three kinds of error, and each fails in a different way, so
knowing which kind you have saves a lot of time.

A *syntax error* is code that is not valid Python at all, like a sentence
with no verb. Python notices it before it runs a single line, so nothing
happens. That is annoying, and it is also the best case, because you find
out straight away.

A *runtime error* is valid Python that tries to do something impossible,
such as dividing by zero, or turning the word `"hello"` into a number. The
program runs until it reaches that line, then stops, and says where.

A *logical error* is valid code that runs to the end with no complaint,
and gives a different answer from the one you meant. Many people call it a
logic error. Nothing is red, and nothing stops. This is the dangerous kind,
and it has the last section of the page to itself.

| Kind | What happens | Who catches it |
|---|---|---|
| syntax error | nothing runs | Python, before it starts |
| runtime error | the program stops partway | Python, while it runs |
| logical error | the program finishes with an answer you did not mean | only you |

## Errors Python catches before it starts

This cell will not work, and that is the point. Run it, and read what
comes back before you read on.

```python exec
id: errors-python-catches-before-it-starts-1
hours = 12
if hours > 10
    print("That is a long day")
```

What is Python complaining about? Can you find the missing colon? Now
look for three things in the message:

1. the **line number**, which tells you where to look first
2. **the line itself**, often with a marker under one position in it
3. the **kind** of problem, here `SyntaxError`, with a short
   description

In recent versions of Python, these descriptions have become much more
helpful. They often name the exact fix. This one says `expected ':'`.

Now the tricky part. The marker often points *after* the real error.
Python reads from left to right, and it complains at the moment it
becomes sure that something is wrong. That can be a character or two
later, or even on the next line. If the marked spot looks fine, look at
what comes just before it.

### Your turn

Here are four broken programs. Can you fix them, one at a time and in
order? For each one:

1. Run it.
2. Read the message. How is it different from the last one?
3. Fix the line.
4. Run it again.

```python exec
id: syntax-your-turn-1
# 1. A misspelled keyword
hours = 12
iff hours > 10:
    print("That is a long day")
```

```python exec
id: syntax-your-turn-2
# 2. A string that is never closed
name = "Alice
print(name)
```

```python exec
id: syntax-your-turn-3
# 3. A line that is not indented
hours = 12
if hours > 10:
print("That is a long day")
```

```python exec
id: syntax-your-turn-4
# 4. A bracket that is opened and not closed
result = (5 + 3
print(result)
```

Look back at the first one. Where did the marker point? It sat under
`hours`, but `hours` is fine. The mistake is the word just before it.
Python does not know that `iff` was meant to be `if`. It only knows that
two names side by side make no sense.

Did the third one say `IndentationError`? That is a special kind of
`SyntaxError`, for lines that are not indented the way Python expects.
The message even names the `if` on line 3 that needed an indented line
after it. (Line 1 is the comment.)

Look again at the fourth one. Python is doing something clever there.
When a bracket is opened and not closed, Python keeps reading past it,
looking for the closing bracket. It only gives up further along, so the
error shows up well after the place where the bracket was opened. Older
versions of Python reported the error where they gave up, which was
often a line that looked completely fine.

Modern Python tracks the bracket back to where it was opened, and says
so: *'(' was never closed*, pointing at the opening bracket. That is a
big improvement. Older versions of Python, and other languages, will
not always do this for you.

## Errors that happen while it runs

A runtime error is different in one important way: Python could read
every line. The program starts, does some work, and stops when it
reaches a line it cannot carry out.

What do you think happens when this cell runs? Will anything print at
all?

```python exec
id: runtime-errors-1
price = 12
print("The price is", price)
print("With delivery:", price + delivery)
```

The first `print` worked. The second did not, because nothing called
`delivery` was ever created. Every runtime error has this shape: some of
your program ran before it stopped.

Here are the runtime errors you can meet with what we know so far, and
what each one is telling you.

| Error | What it means |
|---|---|
| `NameError` | You used a variable that was never created, or whose name is misspelled. |
| `TypeError` | You did something to a value that its type does not allow. Adding a number to a string is the classic example. |
| `ValueError` | The type is right, but the content is wrong. `int("hello")` gives `int` a string, which is what `int` wants, but not a string that means anything as a number. |
| `ZeroDivisionError` | You divided by zero. This nearly always means a value came out as zero when you expected it not to. |

A `NameError` for a misspelled name often ends with a suggestion, such
as `Did you mean: 'score'?` Python has noticed a name that is close to
the one you typed. It is right more often than not.

### Your turn

Each cell below raises one of the errors in the table. Before you run each
one, write which error you think it will raise in the comment at its end.
Then run it. Where it raised a different one, what did you expect the
values to be?

```python exec
id: runtime-your-turn-1
number = "10"
print(number + 2)
# I think it raises:
```

```python exec
id: runtime-your-turn-2
count = int("not a number")
print(count)
# I think it raises:
```

```python exec
id: runtime-your-turn-3
secret = "OTTER"
print(secert)
# I think it raises:
```

```python exec
id: runtime-your-turn-4
pixels = 640 * 480
columns = 0
print("Rows:", pixels / columns)
# I think it raises:
```

Look at the second one. `int("10")` works, and `int("not a number")`
does not, but both are strings. What does this one print?

```python exec
id: runtime-the-fix-1
number = "10"
print(int(number) + 2)
```

```predict
type: number

What will it print?
```

It prints 12: `int()` turns the text into a number first, and then `+`
adds. The first cell above stopped because `"10" + 2` asks `+` to join text
to a number, and that is a `TypeError`: the type is the trouble. In the
second cell the type is fine, a string, and the content is not: that is a
`ValueError`. It is the pair people mix up most.

Where does a `ValueError` like this come from in a real program? Most
often from `input()`. It always gives back a string, and the person
typing can type anything at all. `int(input("How old are you? "))`
works well until somebody types `thirty`.

## Reading a traceback

When a runtime error stops a program, Python prints a report. That
report is a *traceback*: the record of how the program got to the place
where it broke. For the short programs we write now, it has only a few
lines.

Run this cell. Which line number does the report name?

```python exec
id: a-short-traceback-1
bill = 60
people = 3
print("Each person pays", bill / people)
people = people - 3
print("Each person pays", bill / people)
```

Here is the same report again, with its parts marked.

<div class="dl-drawn dl-traceback">
<p class="dl-tb-edge">The top says a report is starting.</p>
<div class="dl-tb-body">
<div class="dl-tb-row"><code>Traceback (most recent call last):</code></div>
<div class="dl-tb-row"><code>  File "&lt;cell a-short-traceback-1&gt;", line 5, in &lt;module&gt;</code><span class="dl-tb-note">which cell, and which line</span></div>
<div class="dl-tb-row dl-tb-failed"><code>    print("Each person pays", bill / people)</code><span class="dl-tb-note">the line that failed</span></div>
<div class="dl-tb-row dl-tb-failed"><code>                              ~~~~~^~~~~~~~</code><span class="dl-tb-note">the part of it that failed</span></div>
<div class="dl-tb-row dl-tb-error"><code>ZeroDivisionError: division by zero</code></div>
</div>
<p class="dl-tb-edge">The bottom line says what went wrong. It is the one to read first.</p>
</div>

**Read it from the bottom.** The last line names the kind of error, and
then describes it. That is what went wrong. The lines above it say
where: the cell, the line number, and a copy of the line, with a marker
under the part that failed. The words `in <module>` mean that the line is
in the main part of the program. Once our programs have functions, which
we meet later, a traceback can name other places too.

Now look closer. The line that failed is line 5. But is line 5 wrong? It
is the same as line 3, and line 3 worked. The mistake is the value that
line 5 was given: `people` is 0. Which line made it 0?

The answer is line 4. So the line that *failed* is not always the line
that is *responsible*. The traceback tells you where the program
stopped. You then look back through the code to find where the bad value
came from.

### Your turn

In a real program, the first line would be
`typed = input("How many hours did you work? ")`. Here we set `typed`
ourselves, as if somebody had typed the word `seven`.

1. Run the cell, and read the traceback from the bottom.
2. What kind of error is it? What does the description say?
3. Which line failed?
4. Which line is *responsible*? Is it the same line?
5. Write your answers in the comments at the end of the cell.

```python exec
id: a-short-traceback-2
typed = "seven"
hours = float(typed)
pay = hours * 14
print("You earned", pay)

# The kind of error:
# The line that failed:
# The line that is responsible:
```

## When nothing looks wrong

Every error so far has announced itself. What about this one? It finds the
middle of a line on a screen, between the pixel at 100 and the pixel at
300.

```python exec
id: when-nothing-looks-wrong-1
left = 100
right = 300
middle = left + right / 2
print("The middle is at", middle)
```

```predict
type: number

What will it print?
```

There is no red text, and no traceback. A number came out. Is it the
middle? Halfway between 100 and 300 is 200, and the program says 250.

Python did exactly what the line says. Division happens before addition,
so only `right` was divided by 2. The line needs brackets:
`(left + right) / 2`. Nothing will tell you this, except knowing what the
answer should be.

**So we try answers we already know.** Before you trust a program on
numbers you cannot check, give it numbers you can check. If it says 250
where you know the answer is 200, you have found something. This habit is
often worth more than any tool for finding mistakes.

### Your turn

This program runs, and gives a different answer from the one it was meant
to give. Can you find out where, with an answer you already know?

<div class="dl-world" data-world="secret-messages">

It is meant to move the letter X three places along, which should give A:
X, Y, Z, then round to A. What does it give?

```python exec
id: when-nothing-looks-wrong-2--secret-messages
letter = "X"
shift = 3
position = ord(letter) - ord("A")
moved = position + shift % 26
print(chr(moved + ord("A")))
```

```inputs
chr(moved + ord("A"))
```

```hint
Which happens first, `+` or `%`? What is `3 % 26`?
```

```solution
letter = "X"
shift = 3
position = ord(letter) - ord("A")
moved = (position + shift) % 26
print(chr(moved + ord("A")))
---
`%` happens before `+`, the same as `*` and `/`, so the line worked out
`3 % 26`, which is 3, and never went back round after Z. The brackets
make the remainder apply to the whole sum.
```

</div>

<div class="dl-world" data-world="pixel-art">

It is meant to find a pixel's brightness, the average of its red, green
and blue. For red 90, green 120 and blue 210, the average is 140. What does
it give?

```python exec
id: when-nothing-looks-wrong-2--pixel-art
red = 90
green = 120
blue = 210
brightness = red + green + blue / 3
print(brightness)
```

```inputs
brightness
```

```hint
Try the numbers yourself: 90 + 120 + 210 is 420, and 420 divided by 3 is
140. Which part of the line did Python divide?
```

```solution
red = 90
green = 120
blue = 210
brightness = (red + green + blue) / 3
print(brightness)
---
Only `blue` was divided, so the program said 280, which is not even a
possible brightness. The brackets make Python add first.
```

</div>

## Looking back

Which of the three kinds of wrong do you expect to give you the most
trouble? What could you do while you write code, rather than after, to
catch it earlier?

A challenge: this program has one error of each kind in it. Can you find
all three? One stops it before it starts, one stops it partway, and one
lets it finish with an answer nobody meant.

```python challenge
# One syntax error, one runtime error and one logical error.
width = 64
height = 48
pixels = width * height
print("Pixels:" pixels)
bytes_needed = pixels * 3
print("Kilobytes:", bytes_needed / 1024)
average_side = width + height / 2
print("Average side:", average_side)
print("Colours:", colours)
```

An error message is the most exact and most patient help you will get from
anything all day: an exact place, an exact kind, and often the fix.
Reading one calmly is a skill you can practise on purpose, the way this
page did: by breaking things when nothing is at stake. Later, our programs
repeat steps, keep lists and split their work into named pieces, and
[Finding bugs in bigger programs](tutorial:when-it-goes-wrong) picks the
three kinds up again there.

## Where to read more

Corey Schafer (2015). *Python Tutorial: Using Try/Except Blocks for Error
Handling.* <https://www.youtube.com/watch?v=NIWwJbo-9_8>. Where the errors
this page teaches you to read get handled on purpose, rather than fixed
by rewriting the line that raised them.
