---
title: "When It Goes Wrong"
slug: when-it-goes-wrong
module: mit-pdp-maths-prog-integration
module_title: "Programming and Maths, Integrated"
year: "2026-2027"
series: maths-and-programming
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

**Programming Design Principles**

By now you have written code that did not work. Everyone has, constantly, and it does not stop happening with experience -- what changes is how long it takes to find out why.

That is what this tutorial is about, and it is possibly the most useful hour in the whole series. Not because errors are interesting in themselves, but because **an error message is your computer trying to help you**, and most people never learn to read one. They see a wall of red text, feel a small drop in the stomach, and start changing things at random.

The red text is a description of what happened and where. It is written in an unfamiliar register, it puts the most useful line at the bottom, and it is often pointing slightly to the side of the real problem. All three of those are learnable.

So we are going to break things on purpose. Every cell below is meant to fail, and reading its failure is the exercise.

We might feel frustrated here, or unsure what to do next. That is something to expect, not something to fix. Every profession with this much left to discover feels this way sometimes, and so does every real attempt to learn something new. We do not always want to stop something from breaking. Sometimes we need it to break, to see how it works.

An error here is a fact about this line, on this run. It is not a fact about whether you can learn to program.

## Three Kinds of Wrong

Before the messages, a distinction that will save you a great deal of time, because the three kinds fail differently and are found differently.

A **syntax error** means your code is not valid Python at all. A sentence with no verb. Python notices before it runs a single line, so nothing happens -- which is frustrating, and is also the best case, because you find out immediately.

A **runtime error** means your code is valid Python that tried to do something impossible. Dividing by zero. Asking for the tenth item of a list of three. The program runs until it reaches that line and then stops, and it tells you exactly where it stopped.

A **logical error** means your code is valid, runs happily to the end, and gives you the wrong answer. Nothing is red. Nothing stops. This is the dangerous kind, and we will come back to it.

Roughly: the first is caught by Python before it starts, the second by Python while it runs, and the third only by you.

## Errors Python Catches Before It Starts

Run this cell. It will not work, and that is the point -- read what comes back before reading on.

```python exec
id: errors-python-catches-before-it-starts-1
hours = 12
if hours > 10
    print("That is a long day")
```

The missing colon is what Python is complaining about. Notice three things in the message.

It tells you the **line number**, which is where to look first.

It shows you **the line itself**, and often marks a position within it.

It says what kind of problem it is -- `SyntaxError` -- and adds a short description. In recent versions of Python those descriptions have become much more helpful and will often name the exact fix.

Now the awkward part. **The marker frequently points after the real error, not at it.** Python reads left to right and complains at the moment it becomes certain something is wrong, which can be a character or two later, or on the following line. If the marked spot looks fine, look at what comes just before it.

### Your turn

Four broken lines below. See if you can fix them one at a time — run, read, repair, run again — in order, paying attention to how the message differs each time.

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

The fourth one is worth a moment, because Python is being cleverer than it looks. An unclosed bracket is not discovered where it opened -- Python keeps reading, expecting the closing one, and only gives up further along. Older versions reported the error wherever they gave up, which was often a line that looked entirely innocent.

Modern Python tracks the bracket back to where it was opened and says so: *'(' was never closed*, pointing at the opening one. That is a large improvement, and it is worth knowing that older error messages, and other languages, will not always do it for you.

## Errors That Happen While It Runs

These are different in an important way: **your code was fine, and the data was not.** The program starts, does some work, and stops when it reaches something impossible.

```python exec
id: errors-that-happen-while-it-runs-1
scores = [85, 90, 78]
print("The first score is", scores[0])
print("The tenth score is", scores[10])
```

The first `print` worked. The second did not. That is the shape of every runtime error: some of your program ran.

Here are the ones you will meet most, and what each one is telling you.

**`ZeroDivisionError`** -- you divided by zero. Almost always this means a count came out empty when you assumed it would not.

**`TypeError`** -- you did something to a value that its type does not support. Adding a number to a string is the classic.

**`ValueError`** -- the right type, the wrong content. `int("hello")` is a string, which is what `int` wants, but not one that means anything as a number.

**`IndexError`** -- a position that does not exist in a list.

**`KeyError`** -- a name that does not exist in a dictionary.

**`NameError`** -- a variable you never created, or created somewhere the code cannot see, or misspelled.

**`AttributeError`** -- you asked a value for something it does not have. Often this means the value is not the type you thought it was.

### Your turn

Each cell raises one of the errors above. Before you run it, decide which. Then run it and see whether you were right -- and if you were not, work out what you expected the values to be.

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

The middle one is worth noticing: `int("10")` works perfectly and `int("not a number")` does not, and both are strings. The type is fine. The content is not. That distinction is exactly what separates `TypeError` from `ValueError`, and it is the one people mix up most.

## Reading a Traceback

When an error happens inside a function, which is called by another function, Python shows you the whole chain. That is a **traceback**: a record of how it got to the place where things went wrong.

```python exec
id: reading-a-traceback-1
def average(numbers):
    return sum(numbers) / len(numbers)


def report(name, numbers):
    return name + " averaged " + str(average(numbers))


print(report("Class A", [70, 80, 90]))
print(report("Class B", []))
```

The first call worked. The second produced several lines of traceback, and they are in a deliberate order.

**Read it from the bottom.** The last line names the error and describes it -- that is what went wrong. Above it, the lines run from the outermost call downwards, so the *innermost* frame, the place the error happened, is nearest the bottom.

That ordering catches people out constantly. The top of a traceback is where your program started; the bottom is where it broke. When someone sends you an error and asks what it means, the last line is where you look.

But notice something about this one. The error is in `average`, on the division -- and `average` is not wrong. It divides by the length of the list, which is the correct thing to do. **The mistake is in the empty list handed to it, which came from the line at the top of the traceback.**

So the bottom tells you *what happened*, and the frames above tell you *how it came to happen*. You need both. A fix inside `average` -- returning zero for an empty list, say -- might be right, or it might hide the real problem, which is that something produced an empty class.

### Your turn

Run this and read the traceback — which line is *responsible*, as opposed to which line failed? Say so in a comment.

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

Everything so far announced itself. This does not.

```python exec
id: the-dangerous-kind-1
def average(numbers):
    total = sum(numbers)
    return total / len(numbers) + 1


scores = [80, 90, 70]
print("Average:", average(scores))
```

No red text. No traceback. A number came out, and it looks reasonable.

It is wrong. The average of 80, 90 and 70 is 80, and that says 81, because `+ 1` is outside the division and should not be there at all. Nothing in the world will tell you this except knowing what the answer should be.

Two more, both of which run perfectly.

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

The first uses `>` where it means `>=`, so a student on exactly the pass mark fails. The second never uses `attendance` at all -- it multiplies `hours` twice -- and produces a confident number that means nothing.

**This is why you check answers you already know.** Before you trust a function on data you cannot verify, give it data you can. The average of 80, 90 and 70 is 80; if your function says 81, you have found something. That habit is worth more than any debugging tool, and it is what *Building Reusable Tools* takes further into testing properly.

### Your turn

Each of these runs and each is wrong. Can you find the mistake? Work out the right answer yourself first, then compare.

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

The first works on the numbers you would try first and fails on a set nobody thinks to test. The second is not obviously wrong at all -- it depends entirely on which argument you meant to go where, which is a question the code cannot answer for you.

## Reflection

Three kinds of wrong, and each is found a different way.

**Syntax errors** stop the program before it starts. Read the line number, look just before the marked spot, and expect an unclosed bracket to be reported late.

**Runtime errors** stop it partway. The last line of the traceback says what happened; the lines above say how it got there; and the line that failed is often not the line that is responsible.

**Logical errors** do not stop it at all. Nothing will find these for you except checking against an answer you already know -- which is a habit rather than a technique.

There is one more thing worth saying, and it is about the feeling rather than the technique. An error message is not a rebuke. It is the most specific, most patient help you will get from anything all day: an exact location, an exact category, and usually a description of the fix. Learning to read one calmly is a real skill, and it is one you can practise deliberately by doing exactly what this tutorial did -- breaking things on purpose, when nothing is at stake.

In a few sentences, which of the three kinds do you expect to give you the most trouble, and what could you do while writing code to catch it earlier?

## Where to Read More

Corey Schafer (2015). *Python Tutorial: Using Try/Except Blocks for Error
Handling.* <https://www.youtube.com/watch?v=NIWwJbo-9_8>. Where the errors
this page teaches you to read get handled deliberately, rather than fixed
by rewriting the line that raised them.
