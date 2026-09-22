---
title: "When It Goes Wrong"
year: "2026-2027"
version: 2026.08.23.1
covers:
  three-kinds-of-wrong:
    covers: [PDP-LO9]
  errors-python-catches-before-it-starts:
    covers: [PDP-LO9]
  errors-that-happen-while-it-runs:
    covers: [PDP-LO9]
  reading-a-traceback:
    covers: [PDP-LO9]
  the-dangerous-kind:
    covers: [PDP-LO9]
---

# When It Goes Wrong

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

So on this page, we break things on purpose. Every cell below is meant
to fail. Reading its failure is the exercise.

We might feel frustrated here, or unsure what to do next. That is
something to expect, not something to fix. Every profession with this
much left to discover feels this way sometimes, and so does every real
attempt to learn something new. We do not always want to stop something
from breaking. Sometimes we need it to break, to see how it works.

An error here is a fact about this line, on this run. It is not a fact
about whether you can learn to program.

**A note before we start.** Some cells on this page use parts of Python
we have not met yet: lists, such as `[85, 90, 78]`; functions made with
`def`; and a `for` loop. You do not need to understand them fully to read
their errors. We meet loops in
[Repeating Yourself](tutorial:repeating-yourself), and lists and
functions in [Lists and Sequences](tutorial:lists-and-sequences).

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
impossible, such as dividing by zero, or asking for the tenth item of a
list of three. The program runs until it reaches that line. Then it
stops, and it tells you exactly where it stopped.

A *logical error* is valid code that runs to the end with no complaint
and gives you the wrong answer. Nothing is red. Nothing stops. This is
the dangerous kind, and we come back to it at the end of the page.

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
helpful. They often name the exact fix.

Now the tricky part. The marker often points *after* the real error.
Python reads from left to right, and it complains at the moment it
becomes sure that something is wrong. That can be a character or two
later, or even on the next line. If the marked spot looks fine, look at
what comes just before it.

### Your turn

Here are four broken lines. Can you fix them, one at a time and in
order? For each one:

1. Run it.
2. Read the message. How is it different from the last one?
3. Fix the line.
4. Run it again.

(The first and third cells use `def`, which makes a function. We meet
`def` properly later. For now, the error is what matters.)

```python exec
id: your-turn-1
# 1. A misspelled keyword
deff greet(name):
    return "Hello, " + name
```

```python exec
id: your-turn-2
# 2. A string that is never closed
name = "Alice
print(name)
```

```python exec
id: your-turn-3
# 3. Indentation that does not line up
def check():
print("checking")
```

```python exec
id: your-turn-4
# 4. A bracket that is opened and not closed
result = (5 + 3
print(result)
```

Did the third one say `IndentationError`? That is a special kind of
`SyntaxError`, for lines that are not indented the way Python expects.

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

A runtime error is different in one important way: your code was fine,
but the data was not. The program starts, does some work, and stops
when it reaches something impossible.

This cell uses a list, `scores`. A list holds several values in order,
and `scores[0]` means the first value in it. What do you think happens
when it asks for the tenth?

```python exec
id: errors-that-happen-while-it-runs-1
scores = [85, 90, 78]
print("The first score is", scores[0])
print("The tenth score is", scores[10])
```

The first `print` worked. The second did not. Every runtime error has
this shape: some of your program ran before it stopped.

Here are the runtime errors you will meet most often, and what each one
is telling you.

| Error | What it means |
|---|---|
| `ZeroDivisionError` | You divided by zero. This nearly always means a count came out as zero when you expected it not to. |
| `TypeError` | You did something to a value that its type does not allow. Adding a number to a string is the classic example. |
| `ValueError` | The type is right, but the content is wrong. `int("hello")` gives `int` a string, which is what `int` wants, but not a string that means anything as a number. |
| `IndexError` | You asked for a position that does not exist in a list. |
| `KeyError` | You asked for a name that does not exist in a dictionary. (A dictionary is a way of storing values under names. We meet it later in the course.) |
| `NameError` | You used a variable that was never created, or that was created somewhere this code cannot see, or whose name is misspelled. |
| `AttributeError` | You asked a value for something it does not have. This often means the value is not the type you thought it was. |

### Your turn

Each cell below raises one of the errors above. For each one:

1. Before you run it, decide which error it will raise.
2. Run it. Were you right?
3. If not, work out what you expected the values to be.

```python exec
id: your-turn-5
number = "10"
print(number + 2)
```

```python exec
id: your-turn-6
count = int("not a number")
print(count)
```

```python exec
id: your-turn-7
print(total_marks)
```

Look at the middle one. `int("10")` works, and `int("not a number")`
does not, but both are strings. The type is fine, and the content is
not. That is exactly the difference between `TypeError` and
`ValueError`, and it is the pair people mix up most.

## Reading a Traceback

The next cell has one function that calls another. (A function is a
named piece of code that we can run again and again. `def` makes one.)
When an error happens inside a function that was called by another
function, Python shows you the whole chain. That record is a
*traceback*: it shows how the program got to the place where things
went wrong.

```python exec
id: reading-a-traceback-1
def average(numbers):
    return sum(numbers) / len(numbers)


def report(name, numbers):
    return name + " averaged " + str(average(numbers))


print(report("Class A", [70, 80, 90]))
print(report("Class B", []))
```

The first call worked. The second call produced several lines of
traceback, and they come in a deliberate order.

**Read it from the bottom.** The last line names the error and
describes it. That is what went wrong. Above it, the lines run from the
outermost call down to the innermost one. So the place where the error
happened is nearest the bottom.

This order confuses a lot of people. The top of a traceback is where
your program started, and the bottom is where it broke. When someone
sends you an error and asks what it means, look at the last line first.

Now look closer. Where is the error? It is in `average`, on the
division. But is `average` wrong? It divides by the length of the list,
which is the correct thing to do. The mistake is the empty list that was
handed to it, and that came from the line at the top of the traceback.

So the bottom tells you *what* happened, and the lines above tell you
*how* it came to happen. You need both. You could fix `average` so that
it gives back zero for an empty list. That might be right. Or it might
hide the real problem, which is that something produced a class with no
marks in it.

<div class="dl-drawn dl-traceback">
<p class="dl-tb-edge">The top is where the program started.</p>
<div class="dl-tb-body">
<div class="dl-tb-row"><code>Traceback (most recent call last):</code></div>
<div class="dl-tb-row"><code>  File "&lt;cell reading-a-traceback-1&gt;", line 10, in &lt;module&gt;</code></div>
<div class="dl-tb-row dl-tb-cause"><code>    print(report("Class B", []))</code><span class="dl-tb-note">the line that is responsible</span></div>
<div class="dl-tb-row dl-tb-cause"><code>          ~~~~~~^^^^^^^^^^^^^^^</code></div>
<div class="dl-tb-row"><code>  File "&lt;cell reading-a-traceback-1&gt;", line 6, in report</code></div>
<div class="dl-tb-row"><code>    return name + " averaged " + str(average(numbers))</code></div>
<div class="dl-tb-row"><code>                                     ~~~~~~~^^^^^^^^^</code></div>
<div class="dl-tb-row"><code>  File "&lt;cell reading-a-traceback-1&gt;", line 2, in average</code></div>
<div class="dl-tb-row dl-tb-failed"><code>    return sum(numbers) / len(numbers)</code><span class="dl-tb-note">the line that failed</span></div>
<div class="dl-tb-row dl-tb-failed"><code>           ~~~~~~~~~~~~~^~~~~~~~~~~~~~</code></div>
<div class="dl-tb-row dl-tb-error"><code>ZeroDivisionError: division by zero</code></div>
</div>
<p class="dl-tb-edge">The bottom is where it broke. That last line is the one to read first.</p>
</div>

### Your turn

1. Run the cell below, and read the traceback.
2. Which line failed?
3. Which line is *responsible*? Is it the same line?
4. Write both answers in the comments at the end of the cell.

```python exec
id: your-turn-8
def price_each(total, people):
    return total / people


def split_bill(bill, names):
    each = price_each(bill, len(names))
    return "Each person pays " + str(round(each, 2))


print(split_bill(60, ["Aoife", "Ben", "Cara"]))
print(split_bill(60, []))

# The line that failed:
# The line that is responsible:
```

## The Dangerous Kind

Every error so far has announced itself. What about this one?

```python exec
id: the-dangerous-kind-1
def average(numbers):
    total = sum(numbers)
    return total / len(numbers) + 1


scores = [80, 90, 70]
print("Average:", average(scores))
```

There is no red text, and no traceback. A number came out, and it looks
reasonable. But is it right? Work out the average of 80, 90 and 70
yourself.

The average is 80, and the program says 81. The `+ 1` sits outside the
division, and it should not be there at all. Nothing will tell you this,
except knowing what the answer should be.

Here are two more. Both run with no error. What is wrong with each one?

```python exec
id: the-dangerous-kind-2
def classify(score):
    if score > 50:
        return "Pass"
    return "Fail"


print("A score of 50 is a", classify(50))
print("A score of 51 is a", classify(51))
```

```python exec
id: the-dangerous-kind-3
hours = 10
attendance = 0.85

prediction = (hours * 3.5) + (hours * 20) + 30
print("Predicted mark:", prediction)
```

- The first one uses `>` where it means `>=`. So a student with exactly
  the pass mark, 50, fails.
- The second one never uses `attendance` at all. It multiplies by
  `hours` twice, and prints a confident number that means nothing.

**This is why we check answers we already know.** Before you trust a
function on data you cannot check, give it data you can check. The
average of 80, 90 and 70 is 80. If your function says 81, you have found
something. This habit is often worth more than any debugging tool.
[Building Reusable Tools](tutorial:building-reusable-tools) takes it
further, into testing code properly.

### Your turn

Each of these runs, and each one is wrong. Can you find the mistake?
First work out the right answer yourself, then compare it with what the
code prints.

```python exec
id: your-turn-9
def biggest(numbers):
    largest = 0
    for n in numbers:
        if n > largest:
            largest = n
    return largest


print(biggest([3, 9, 4]))
print(biggest([-5, -2, -9]))
```

```python exec
id: your-turn-10
def percentage(part, whole):
    return part / whole * 100


print(percentage(45, 60))
print(percentage(60, 45))
```

The first one works on the numbers you would try first, and fails on a
set of numbers that few people think to test. The second one depends on
which value you meant to put where. The code cannot answer that for
you, so its mistake is hard to see.

## Reflection

There are three kinds of wrong, and we find each one in a different way.

**Syntax errors** stop the program before it starts. Read the line
number, look just before the marked spot, and expect an unclosed bracket
to be reported late.

**Runtime errors** stop the program partway through. The last line of
the traceback says what happened. The lines above say how the program
got there. And the line that failed is often not the line that is
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

## Where to Read More

Corey Schafer (2015). *Python Tutorial: Using Try/Except Blocks for Error
Handling.* <https://www.youtube.com/watch?v=NIWwJbo-9_8>. Where the errors
this page teaches you to read get handled deliberately, rather than fixed
by rewriting the line that raised them.
