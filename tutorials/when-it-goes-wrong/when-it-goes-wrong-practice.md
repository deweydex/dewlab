---
title: "When It Goes Wrong — Practice"
practice_for: when-it-goes-wrong
year: "2026-2027"
version: 2026.08.23.1
---

# When It Goes Wrong — Practice

The answers are hidden until you open them. On this page, your
prediction is the exercise, and running the code is the marking. For
most questions, try to predict the error before you run the code.

Some of the code here uses lists, functions and loops, which we meet
properly in [Repeating Yourself](tutorial:repeating-yourself) and
[Lists and Sequences](tutorial:lists-and-sequences). You only need to
read the errors they cause.

## Tools

There is nothing to set up here. Each question is its own cell, and
each one is meant to fail.

```python exec
id: tools-1
# A reminder of the three kinds, and how each announces itself.
print("Syntax error:  Python refuses before running anything.")
print("Runtime error: some of your program runs, then it stops.")
print("Logical error: it all runs, and the answer is wrong.")
```

## Which Kind?

For each one, is it a syntax error, a runtime error, a logical error, or
no error at all?

**1.** `def calculate(x)` followed by `return x * 2`

<details class="dl-answer"><summary>answer</summary>

Syntax error. The colon is missing after `(x)`, so Python cannot read
the line, and it never runs anything.

</details>

**2.** `result = 10 + "5"`

<details class="dl-answer"><summary>answer</summary>

Runtime error: a `TypeError`. The line is valid Python, but Python will
not add a number to a string.

</details>

**3.** `def double(x): return x + x` called as `double("5")`

<details class="dl-answer"><summary>answer</summary>

Logical error. It runs and gives back `"55"`, because `+` joins two
strings together.

Nothing is red, and the answer is wrong. This is the dangerous kind. It
is even worse than that: `double(5)` gives 10, so the function looks
correct until somebody passes it a string.

</details>

**4.** `numbers = [1, 2, 3]` then `total = sum(numbers)`

<details class="dl-answer"><summary>answer</summary>

No error. It gives 6.

</details>

**5.** `scores = [85, 90]` then `print(scores[2])`

<details class="dl-answer"><summary>answer</summary>

Runtime error: an `IndexError`. The list has two items, at positions 0
and 1, so position 2 does not exist.

</details>

**6.** `average = sum(marks) / len(marks)` where `marks` is empty

<details class="dl-answer"><summary>answer</summary>

Runtime error: a `ZeroDivisionError`. The length of an empty list is
zero.

In real programs, this is the most common cause of that error. A
collection turns out to be empty when the code expected it not to be.
That happens far more often than somebody typing `/0`.

</details>

## Naming the Error

Which error do you think each one raises? Predict, then run it.

**7.**

```python exec
id: naming-the-error-1
value = "12"
print(value + 3)
```

<details class="dl-answer"><summary>answer</summary>

`TypeError`. Python cannot add a string and an integer.

Notice that `value * 3` would work, and give `"121212"`. That is a
different kind of surprise.

</details>

**8.**

```python exec
id: naming-the-error-2
count = int("twelve")
```

<details class="dl-answer"><summary>answer</summary>

`ValueError`. The type is right, because `int` wants a string. But the
content of the string is not a number.

People mix these two up more than any other pair. A `TypeError` means
the wrong kind of thing. A `ValueError` means the right kind of thing,
with content Python cannot use.

</details>

**9.** This cell uses a dictionary, which stores values under names. We
meet dictionaries later in the course.

```python exec
id: naming-the-error-3
marks = {"Aoife": 72, "Ben": 65}
print(marks["Cara"])
```

<details class="dl-answer"><summary>answer</summary>

`KeyError`. There is no entry for Cara.

`marks.get("Cara")` gives back `None` instead of raising an error. That
is often what you want. Sometimes, though, it hides a problem you would
have preferred to hear about.

</details>

**10.**

```python exec
id: naming-the-error-4
name = "Aoife"
print(name.lenght())
```

<details class="dl-answer"><summary>answer</summary>

`AttributeError`. The name is misspelled. And even spelled correctly, a
string has no `.length()` method. The way to get the length is
`len(name)`.

An `AttributeError` often means the value is not the type you thought it
was. So it is worth printing the value before you decide the method name
is wrong.

</details>

**11.**

```python exec
id: naming-the-error-5
def total(items):
    return sum(items)

print(total(prices))
```

<details class="dl-answer"><summary>answer</summary>

`NameError`. `prices` was never created.

Python also raises a `NameError` when a variable exists, but not where
the code can see it. One example is a variable created inside a function
and used outside it.

</details>

## Reading a Traceback

**12.** In a traceback, where do you find the error that stopped the
program?

<details class="dl-answer"><summary>answer</summary>

The last line names it. Above that line, the steps run from the
outermost call downwards. So the innermost step, where the error
happened, is nearest the bottom.

Read from the bottom. The top of a traceback is where your program
started, and the bottom is where it broke.

</details>

**13.** Run this. Can you find two things: the line that failed, and the
line that is *responsible*?

```python exec
id: reading-a-traceback-1
def rate(distance, hours):
    return distance / hours


def report(journey):
    return "Average speed: " + str(rate(journey[0], journey[1]))


print(report([120, 2]))
print(report([120, 0]))
```

<details class="dl-answer"><summary>answer</summary>

The line that failed is `return distance / hours`, in `rate`. That is
where the `ZeroDivisionError` happened.

The line that is responsible is `print(report([120, 0]))`, because it
supplied the zero.

`rate` is not wrong. Dividing distance by hours is the correct thing to
do. You could "fix" `rate` so that it gives back zero when hours is
zero. That might be right. Or it might hide the real problem, which is
a journey that took no time.

</details>

**14.** Why does a traceback show the whole chain of calls, and not only
the line that failed?

<details class="dl-answer"><summary>answer</summary>

Because the line that failed is often not where the mistake is. A
function can be completely correct and still fail on bad input. The
chain tells you where the bad input came from.

</details>

## The Dangerous Kind

Each of these runs, and each one is wrong. Can you find the mistake?

**15.**

```python exec
id: the-dangerous-kind-1
def average(numbers):
    total = sum(numbers)
    return total / len(numbers) + 1


print(average([80, 90, 70]))
```

<details class="dl-answer"><summary>answer</summary>

The `+ 1` is outside the division, and it should not be there at all.
The average of 80, 90 and 70 is 80, and this code says 81.

The only way to find this is to know what the answer should be. That is
the whole lesson.

</details>

**16.**

```python exec
id: the-dangerous-kind-2
def biggest(numbers):
    largest = 0
    for n in numbers:
        if n > largest:
            largest = n
    return largest


print(biggest([3, 9, 4]))
print(biggest([-5, -2, -9]))
```

<details class="dl-answer"><summary>answer</summary>

Starting `largest` at 0 assumes the numbers are positive. On a list of
only negative numbers, it gives back 0, which is not in the list at all.

The fix is to start at the first item: `largest = numbers[0]`. But then
an empty list raises an `IndexError`. So decide what an empty list
should do. Do not leave it to chance.

Notice that the code works on the numbers you would try first. That is
what makes this kind of error hard.

</details>

**17.**

```python exec
id: the-dangerous-kind-3
def classify(score):
    if score > 40:
        return "Pass"
    return "Fail"


for score in [39, 40, 41]:
    print(score, classify(score))
```

<details class="dl-answer"><summary>answer</summary>

If 40 is the pass mark, this code fails everyone who scored exactly 40.
It needs `>=`.

Logical errors live at boundaries. Always test the exact boundary, one
below it, and one above it.

</details>

**18.**

```python exec
id: the-dangerous-kind-4
def percentage_change(old, new):
    return (new - old) / new * 100


print(percentage_change(50, 60))
```

<details class="dl-answer"><summary>answer</summary>

It divides by the new value, but percentage change is measured against
the *old* value. The code gives 16.67%, and the right answer is 20%.

The wrong answer is close enough to look believable. That is exactly
why nobody notices it.

</details>

**19.** What is the one habit that catches logical errors?

<details class="dl-answer"><summary>answer</summary>

Checking against an answer you already know.

Before you trust a function on data you cannot check, give it data you
can check. The average of 80, 90 and 70 is 80. Ten percent of 50 is 5.
If the function disagrees, you have found something.

That habit is worth more than any debugging tool.
[Building Reusable Tools](tutorial:building-reusable-tools) takes it
further, into testing code properly.

</details>

## Fixing

**20.** Can you fix this so that it works for any list, including an
empty one?

```python exec
id: fixing-1
def average(numbers):
    return sum(numbers) / len(numbers)


# print(average([]))
```

<details class="dl-answer"><summary>answer</summary>

```python
def average(numbers):
    if not numbers:
        return None      # or 0, or raise — the point is to decide
    return sum(numbers) / len(numbers)
```

The important part is the decision, more than the code. What *should*
the average of nothing be? There are three choices:

- `None` says "no answer exists".
- `0` gives an answer that is not true.
- Raising an error says "you should not have asked".

You could defend any of the three, and they mean different things. If
you leave the code to crash, nobody made the decision.

</details>

**21.** This code is meant to count how many marks are passes. Can you
fix it?

```python exec
id: fixing-2
def count_passes(marks):
    passes = 0
    for mark in marks:
        if mark >= 40:
            passes = 1
    return passes


print(count_passes([35, 50, 60, 20]))
```

<details class="dl-answer"><summary>answer</summary>

`passes = 1` should be `passes += 1`, which is short for
`passes = passes + 1`. As written, the code sets the count to 1 each
time. So it gives back 1 for any list with at least one pass.

It gives the right answer for a list with exactly one pass. That is
probably the list somebody tested it on.

</details>

**22.** Why is an error message better news than no error message?

<details class="dl-answer"><summary>answer</summary>

Because an error message tells you where and what. A syntax error stops
you before anything happens. A runtime error names the line and the
reason.

A logical error tells you nothing. It may not be found for weeks, and by
then it has produced a great deal of confident, wrong output.

The red text is the computer helping you as much as it can.

</details>
