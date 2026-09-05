---
title: "When It Goes Wrong — Practice"
slug: when-it-goes-wrong-practice
practice_for: when-it-goes-wrong
module: mit-pdp-maths-prog-integration
module_title: "Programming and Maths, Integrated"
year: "2026-2027"
series: programming-foundations
version: 2026.08.23.1
---

# When It Goes Wrong — Practice

Answers are folded. Most of these ask you to predict an error before running the code — the prediction is the exercise, and running it is the marking.

## Tools

There is nothing to set up here. Each question is its own cell, and each is meant to fail.

```python exec
id: tools-1
# A reminder of the three kinds, and how each announces itself.
print("Syntax error:  Python refuses before running anything.")
print("Runtime error: some of your program runs, then it stops.")
print("Logical error: it all runs, and the answer is wrong.")
```

## Which Kind?

For each, say whether it is a syntax error, a runtime error, a logical error, or no error at all.

**1.** `def calculate(x)` followed by `return x * 2`

<details class="dl-answer"><summary>answer</summary>

Syntax. The colon is missing after the parameter list, so Python cannot parse the line and never runs anything.

</details>

**2.** `result = 10 + "5"`

<details class="dl-answer"><summary>answer</summary>

Runtime — a `TypeError`. The line is valid Python; adding a number to a string is not something Python will do.

</details>

**3.** `def double(x): return x + x` called as `double("5")`

<details class="dl-answer"><summary>answer</summary>

Logical. It runs and returns `"55"`, because `+` on strings joins them.

Nothing is red and the answer is wrong, which is the dangerous kind. Worse: `double(5)` gives 10, so the function looks correct until somebody passes it a string.

</details>

**4.** `numbers = [1, 2, 3]` then `total = sum(numbers)`

<details class="dl-answer"><summary>answer</summary>

No error. It gives 6.

</details>

**5.** `scores = [85, 90]` then `print(scores[2])`

<details class="dl-answer"><summary>answer</summary>

Runtime — `IndexError`. There are two items, at positions 0 and 1, so position 2 does not exist.

</details>

**6.** `average = sum(marks) / len(marks)` where `marks` is empty

<details class="dl-answer"><summary>answer</summary>

Runtime — `ZeroDivisionError`. The length is zero.

This is the most common cause of that error in practice: not somebody typing `/0`, but a collection turning out empty when the code assumed it would not be.

</details>

## Naming the Error

Predict which error each raises, then run it.

**7.**

```python exec
id: naming-the-error-1
value = "12"
print(value + 3)
```

<details class="dl-answer"><summary>answer</summary>

`TypeError`. A string and an integer cannot be added.

Note that `value * 3` would work and give `"121212"`, which is a different kind of surprise.

</details>

**8.**

```python exec
id: naming-the-error-2
count = int("twelve")
```

<details class="dl-answer"><summary>answer</summary>

`ValueError`. The type is right — `int` wants a string — but the content is not a number.

This is the distinction people mix up most: `TypeError` is the wrong kind of thing, `ValueError` is the right kind with unusable content.

</details>

**9.**

```python exec
id: naming-the-error-3
marks = {"Aoife": 72, "Ben": 65}
print(marks["Cara"])
```

<details class="dl-answer"><summary>answer</summary>

`KeyError`. There is no entry for Cara.

`marks.get("Cara")` returns `None` instead of raising, which is often what you want — and sometimes hides a problem you would rather have been told about.

</details>

**10.**

```python exec
id: naming-the-error-4
name = "Aoife"
print(name.lenght())
```

<details class="dl-answer"><summary>answer</summary>

`AttributeError`. It is misspelled — and even spelled correctly, a string has no `.length()` method. The answer is `len(name)`.

`AttributeError` frequently means the value is not the type you thought it was, so it is worth printing the value before assuming the method name is wrong.

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

Also raised when a variable exists but not where the code can see it — created inside a function and used outside it, say.

</details>

## Reading a Traceback

**12.** In a traceback, where is the error that actually stopped the program?

<details class="dl-answer"><summary>answer</summary>

The last line names it. Above that, the frames run from the outermost call downwards, so the innermost — where it happened — is nearest the bottom.

Read from the bottom. The top of a traceback is where your program started; the bottom is where it broke.

</details>

**13.** Run this and identify two things: the line that failed, and the line that is *responsible*.

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

The line that failed is `return distance / hours` in `rate` — that is where the `ZeroDivisionError` happened.

The line responsible is `print(report([120, 0]))`, which supplied a zero.

`rate` is not wrong. Dividing distance by hours is the correct thing to do. A "fix" inside `rate` — returning zero for zero hours, say — might be right, or it might hide the real problem, which is that a journey took no time.

</details>

**14.** Why does a traceback show the whole chain rather than just the failing line?

<details class="dl-answer"><summary>answer</summary>

Because the failing line is often not where the mistake is. A function can be perfectly correct and still fail on bad input, and the chain is what tells you where the bad input came from.

</details>

## The Dangerous Kind

Each of these runs. Each is wrong. Find the mistake.

**15.**

```python exec
id: the-dangerous-kind-1
def average(numbers):
    total = sum(numbers)
    return total / len(numbers) + 1


print(average([80, 90, 70]))
```

<details class="dl-answer"><summary>answer</summary>

The `+ 1` is outside the division and should not be there at all. The average of 80, 90 and 70 is 80, and this says 81.

Found only by knowing what the answer should be, which is the whole lesson.

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

Starting at 0 assumes the numbers are positive. On an all-negative list it returns 0, which is not in the list at all.

The fix is to start at the first item: `largest = numbers[0]`. Which then raises an `IndexError` on an empty list — so decide what an empty list should do, rather than leaving it to chance.

Notice it works on the numbers you would try first. That is what makes this kind hard.

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

If 40 is the pass mark, this fails everyone who scored exactly 40 — it needs `>=`.

Boundary conditions are where logical errors live. Always test the exact boundary, one below, and one above.

</details>

**18.**

```python exec
id: the-dangerous-kind-4
def percentage_change(old, new):
    return (new - old) / new * 100


print(percentage_change(50, 60))
```

<details class="dl-answer"><summary>answer</summary>

It divides by the new value; percentage change is measured against the *old* one. This gives 16.67% when the answer is 20%.

It is close enough to look plausible, which is exactly why it survives.

</details>

**19.** What is the one habit that catches logical errors?

<details class="dl-answer"><summary>answer</summary>

Checking against an answer you already know.

Before trusting a function on data you cannot verify, give it data you can. The average of 80, 90 and 70 is 80. Ten percent of 50 is 5. If the function disagrees, you have found something.

That habit is worth more than any debugging tool, and it is what *Building Reusable Tools* takes further into testing properly.

</details>

## Fixing

**20.** Fix this so it works for any list, including an empty one.

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

The important part is not the code, it is the decision. What *should* the average of nothing be? `None` says "no answer exists", `0` claims an answer that is not true, and raising an error says "you should not have asked".

All three are defensible and they mean different things. Leaving it to crash means nobody decided.

</details>

**21.** This is meant to count how many marks are passes. Fix it.

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

`passes = 1` should be `passes += 1`. As written it sets the count to 1 every time and returns 1 for any list with at least one pass.

It gives the right answer for a list with exactly one pass, which is probably the list it was tested on.

</details>

**22.** Why is an error message better news than no error message?

<details class="dl-answer"><summary>answer</summary>

Because it tells you where and what. A syntax error stops you before anything happens; a runtime error names the line and the reason.

A logical error tells you nothing, and may not be found for weeks — by which point it has produced a great deal of confident, wrong output.

The red text is the computer being as helpful as it knows how.

</details>
