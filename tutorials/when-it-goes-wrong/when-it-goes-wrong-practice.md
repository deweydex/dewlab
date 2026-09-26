---
title: "Finding bugs in bigger programs — Practice"
practice_for: when-it-goes-wrong
year: "2026-2027"
version: 2026.09.25.1
---

# Finding bugs in bigger programs — Practice

The answers are hidden until you open them. On this page, your
prediction is the exercise, and running the code is the marking. For
most questions, try to predict the error, or the wrong answer, before you
run the code.

The short errors, such as `TypeError` and `ValueError`, have their own
questions on the practice page for
[Reading an error message](tutorial:reading-an-error-message). This page
uses loops, lists, dictionaries and functions.

## Tools

There is nothing to set up here. Each question is its own cell, and most
of them are meant to fail.

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

**2.** `def double(x): return x + x` called as `double("5")`

<details class="dl-answer"><summary>answer</summary>

Logical error. It runs and gives back `"55"`, because `+` joins two
strings together.

Nothing is red, and the answer is wrong. This is the dangerous kind. It
is even worse than that: `double(5)` gives 10, so the function looks
correct until somebody passes it a string.

</details>

**3.** `numbers = [1, 2, 3]` then `total = sum(numbers)`

<details class="dl-answer"><summary>answer</summary>

No error. It gives 6.

</details>

**4.** `scores = [85, 90]` then `print(scores[2])`

<details class="dl-answer"><summary>answer</summary>

Runtime error: an `IndexError`. The list has two items, at positions 0
and 1, so position 2 does not exist.

</details>

**5.** `average = sum(marks) / len(marks)` where `marks` is empty

<details class="dl-answer"><summary>answer</summary>

Runtime error: a `ZeroDivisionError`. The length of an empty list is
zero.

In real programs, this is the most common cause of that error. A
collection turns out to be empty when the code expected it not to be.
That happens far more often than somebody typing `/0`.

</details>

## Naming the Error

Which error do you think each one raises? Predict, then run it.

**6.**

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

**7.**

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

**8.**

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

**9.**

```python exec
id: naming-the-error-6
week = ["Mon", "Tue", "Wed", "Thu", "Fri"]
for day in range(1, len(week) + 1):
    print(week[day])
```

<details class="dl-answer"><summary>answer</summary>

`IndexError`, after four days have printed: Tue, Wed, Thu and Fri.

This loop is off by one in two ways. It starts at 1, so it skips `Mon`
at position 0. And it goes up to 5, but the last position is 4. The
loop should be `for day in range(len(week)):`, or, simpler,
`for day in week:`.

</details>

## Reading a Traceback

**10.** In a traceback with several steps, where do you find the error
that stopped the program?

<details class="dl-answer"><summary>answer</summary>

The last line names it. Above that line, the steps run from the
outermost call downwards. So the innermost step, where the error
happened, is nearest the bottom.

Read from the bottom. The top of a traceback is where your program
started, and the bottom is where it broke.

</details>

**11.** Run this. Can you find two things: the line that failed, and the
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

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Read the last line. What kind of error is it?
2. The step just above it names a function and a line. That is the line
   that failed.
3. Read upwards. Which line first handed over the value that caused it?

</details>

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

**12.** Why does a traceback show the whole chain of calls, and not only
the line that failed?

<details class="dl-answer"><summary>answer</summary>

Because the line that failed is often not where the mistake is. A
function can be completely correct and still fail on bad input. The
chain tells you where the bad input came from.

</details>

## The Dangerous Kind

Each of these runs, and each one is wrong. Can you find the mistake?

**13.**

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

**14.**

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

**15.**

```python exec
id: the-dangerous-kind-3
def classify(score):
    if score > 50:
        return "Pass"
    return "Fail"


for score in [49, 50, 51]:
    print(score, classify(score))
```

<details class="dl-answer"><summary>answer</summary>

If 50 is the pass mark, this code fails everyone who scored exactly 50.
It needs `>=`.

Logical errors live at boundaries. Always test the exact boundary, one
below it, and one above it. The loop here does exactly that.

</details>

**16.**

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

## Debugging Habits

**17.** This function should count the words longer than four letters.
In the list below, that is "banana" and "cherry", so the answer is 2.
Add a `print` inside the loop, with a label, to find out where it goes
wrong. Then fix it.

```python exec
id: debugging-habits-practice-1
def count_long(words):
    count = 0
    for word in words:
        if len(word) > 4:
            count = count + 1
        return count


print(count_long(["fig", "banana", "kiwi", "cherry"]))
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Put `print("checking", word, "count is", count)` as the first line
   inside the loop.
2. Run it. How many words does the loop check?
3. Look at how far `return count` is indented. Which block is it inside?

</details>

<details class="dl-answer"><summary>answer</summary>

The `print` shows only one line: `checking fig count is 0`. The loop
stops after the first word.

`return count` is indented inside the loop, so the function gives back
its answer after the first word. Move `return count` out to the same
indent as `for`:

```python
def count_long(words):
    count = 0
    for word in words:
        if len(word) > 4:
            count = count + 1
    return count
```

Now it gives 2. A `return` one indent too far in is a very common bug,
and a `print` in the loop finds it quickly.

</details>

**18.** Here are two functions and a line that uses both. The last line
prints the wrong answer: a 10% discount on 50 plus 30 should give 72.
Test each function on its own, with numbers you can check in your head.
Which one has the bug?

```python exec
id: debugging-habits-practice-2
def add_up(prices):
    total = 0
    for price in prices:
        total = total + price
    return total


def apply_discount(amount, percent):
    return amount - percent / 100


print(apply_discount(add_up([50, 30]), 10))
```

<details class="dl-answer"><summary>answer</summary>

Tests like these show it:

```python
print(add_up([50, 30]), "should be 80")
print(apply_discount(100, 10), "should be 90")
```

`add_up` passes. `apply_discount(100, 10)` gives 99.9, so the bug is
there. It takes away 10 / 100, which is 0.1, when it should take away
10% *of the amount*. The line should be
`return amount - amount * percent / 100`.

With that fix, the last line gives 72.0.

</details>

**19.** Why is it worth splitting a long function into small ones before
you go looking for a bug?

<details class="dl-answer"><summary>answer</summary>

Because each small function can be tested on its own, with an answer you
already know. A failing test then points at one small piece of code. In
a long function, the bug could be on any line.

[Designing and testing good functions](tutorial:building-reusable-tools) wrote test
functions that do this for you, and print PASS or FAIL.

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
        if mark >= 50:
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
reason, and a traceback shows how the program got there.

A logical error tells you nothing. It may not be found for weeks, and by
then it has produced a great deal of confident, wrong output.

The red text is the computer helping you as much as it can.

</details>
