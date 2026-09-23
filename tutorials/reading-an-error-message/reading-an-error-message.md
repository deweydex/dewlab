---
title: "Reading an error message"
year: "2026-2027"
version: 2026.09.22.1
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

By now, you have written code that did not work. Everyone has, all the
time, and it never stops happening. What changes with experience is how
long it takes to find out why.

That is what this page is about, and it may be the most useful hour in
the whole series. An error message is your computer trying to help you.
Most people never learn to read one. They see a wall of red text, feel a
moment of panic, and start changing things at random.

The red text describes what happened, and where. It is hard to read at
first, for three reasons:

1. It is written in an unfamiliar style.
2. It puts the most useful line at the bottom.
3. It often points a little to the side of the real problem.

We can learn to handle all three.

So on this page, we break things on purpose. Most cells below are meant
to fail. Reading the failure is the exercise. Every cell uses only what
we have met so far: variables, types, arithmetic, strings, `print`,
`input`, and `if`, `elif` and `else`.

We might feel frustrated here, or unsure what to do next. That is
something to expect, not something to fix. Every profession with this
much left to discover feels this way sometimes, and so does every real
attempt to learn something new. We do not always want to stop something
from breaking. Sometimes we need it to break, to see how it works.

An error here is a fact about this line, on this run. It is not a fact
about whether you can learn to program.

## Three Kinds of Wrong

Before we look at the messages, it helps to know that there are three
kinds of error. Each kind fails in a different way, and we find each
kind in a different way. Knowing which kind you have will save you a lot
of time.

A *syntax error* is code that is not valid Python at all. It is like a
sentence with no verb. Python notices it before it runs a single line,
so nothing happens. That is frustrating, but it is also the best case,
because you find out straight away.

A *runtime error* is valid Python that tries to do something
impossible, such as dividing by zero, or turning the word `"hello"` into
a number. The program runs until it reaches that line. Then it stops,
and it tells you exactly where it stopped.

A *logical error* is valid code that runs to the end with no complaint
and gives you the wrong answer. Many people call it a logic error. Nothing
is red. Nothing stops. This is the dangerous kind, and we come back to it
at the end of the page.

| Kind | What happens | Who catches it |
|---|---|---|
| syntax error | nothing runs | Python, before it starts |
| runtime error | the program stops partway | Python, while it runs |
| logical error | the program finishes with a wrong answer | only you |

## Errors Python Catches Before It Starts

Run this cell. It will not work, and that is the point. Read what comes
back before you read on.

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

## Errors That Happen While It Runs

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

Each cell below raises one of the errors above. For each one:

1. Before you run it, decide which error it will raise.
2. Run it. Were you right?
3. If not, work out what you expected the values to be.

```python exec
id: runtime-your-turn-1
number = "10"
print(number + 2)
```

```python exec
id: runtime-your-turn-2
count = int("not a number")
print(count)
```

```python exec
id: runtime-your-turn-3
print(total_marks)
```

```python exec
id: runtime-your-turn-4
bill = 60
people = 0
print("Each person pays", bill / people)
```

Look at the second one. `int("10")` works, and `int("not a number")`
does not, but both are strings. The type is fine, and the content is
not. That is exactly the difference between `TypeError` and
`ValueError`, and it is the pair people mix up most.

Where does a `ValueError` like this come from in a real program? Most
often from `input()`. It always gives back a string, and the person
typing can type anything at all. `int(input("How old are you? "))`
works well until somebody types `thirty`.

## Reading a Traceback

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

## When Nothing Looks Wrong

Every error so far has announced itself. What about this one? It finds
the average of three marks.

```python exec
id: when-nothing-looks-wrong-1
first = 80
second = 90
third = 70
average = first + second + third / 3
print("Average:", average)
```

There is no red text, and no traceback. A number came out. But is it
right? Work out the average of 80, 90 and 70 yourself.

The average is 80, and the program says about 193. Python did exactly
what the line says. Division happens before addition, so only `third`
was divided by 3. The line needs brackets around the addition:
`(first + second + third) / 3`.

Nothing will tell you this, except knowing what the answer should be.

**This is why we check answers we already know.** Before you trust a
program on numbers you cannot check, give it numbers you can check. The
average of 80, 90 and 70 is 80. If your program says 193, you have found
something. This habit is often worth more than any tool for finding
mistakes.

### Your turn

This program converts a temperature from Celsius to Fahrenheit. It runs,
and it is wrong.

1. Water boils at 100 °C, which is 212 °F. What does the program say?
2. Can you find the mistake?
3. Fix it, and run it again. Does it give 212 now?
4. Try one more value you know: 0 °C is 32 °F.

```python exec
id: when-nothing-looks-wrong-2
celsius = 100
fahrenheit = celsius + 32 * 9 / 5
print(celsius, "C is", fahrenheit, "F")
```

## Reflection

There are three kinds of wrong, and we find each one in a different way.

**Syntax errors** stop the program before it starts. Read the line
number, look just before the marked spot, and expect an unclosed bracket
to be reported late.

**Runtime errors** stop the program partway through. Read the traceback
from the bottom. The last line says what happened. The lines above say
where. And the line that failed is not always the line that is
responsible.

**Logical errors** do not stop the program at all. Only one thing will
find them for you: checking against an answer you already know. That is
a habit you build, more than a technique you learn.

There is one more thing to say, and it is about the feeling more than
the technique. An error message is the most exact and most patient help
you will get from anything all day. It gives an exact place, an exact
kind of error, and often a description of the fix. It is not a
telling-off. Reading one calmly is a real skill. You can practise it on
purpose, the way this page did: by breaking things when nothing is at
stake.

In a few sentences: which of the three kinds do you expect to give you
the most trouble? What could you do while you write code to catch it
earlier?

Later, our programs grow. They repeat steps, keep lists of values, and
split their work into named pieces. The same three kinds of wrong turn
up there too, with a few new errors and longer tracebacks.
[Finding bugs in bigger programs](tutorial:when-it-goes-wrong) picks
them up once we have those tools.

## Where to Read More

Corey Schafer (2015). *Python Tutorial: Using Try/Except Blocks for Error
Handling.* <https://www.youtube.com/watch?v=NIWwJbo-9_8>. Where the errors
this page teaches you to read get handled deliberately, rather than fixed
by rewriting the line that raised them.
