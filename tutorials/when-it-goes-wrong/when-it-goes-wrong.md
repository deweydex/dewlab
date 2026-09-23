---
title: "Finding bugs in bigger programs"
year: "2026-2027"
version: 2026.09.22.1
covers:
  errors-from-lists-and-dictionaries:
    covers: [PDP-LO9]
  tracebacks-through-several-functions:
    covers: [PDP-LO9]
  the-dangerous-kind:
    covers: [PDP-LO9]
  debugging-habits:
    covers: [PDP-LO9]
    touches: [PDP-LO10]
---

# Finding bugs in bigger programs

In [Reading an error message](tutorial:reading-an-error-message), we
broke small programs on purpose. We met the three kinds of wrong: syntax
errors, runtime errors and logical errors. We learned to read a short
traceback from the bottom. And we saw that the line that failed is not
always the line that is responsible.

Since then, our programs have grown. They repeat steps with loops, keep
values in lists and dictionaries, and split their work into functions.
Everything on that page still holds. But bigger programs bring a few new
errors, longer tracebacks, and logical errors that hide much better.

That is what this page is about. Most cells below are meant to fail, or
to give a wrong answer. Finding out why is the exercise.

If a message makes your heart sink, that is normal. It happens to people
who have programmed for thirty years. An error is a fact about this line,
on this run. It is not a fact about whether you can program.

## Errors From Lists and Dictionaries

A list holds values in order, and a dictionary holds values under names.
Both give us new ways to ask for something that is not there.

What do you think happens when this cell asks for the tenth score?

```python exec
id: errors-that-happen-while-it-runs-1
scores = [85, 90, 78]
print("The first score is", scores[0])
print("The tenth score is", scores[10])
```

The first `print` worked. The second did not. As with every runtime
error, some of the program ran before it stopped.

A dictionary fails in a similar way. What happens here?

```python exec
id: errors-from-lists-and-dictionaries-1
marks = {"Aoife": 72, "Ben": 65}
print("Aoife scored", marks["Aoife"])
print("Cara scored", marks["Cara"])
```

Here are the runtime errors that come with the tools we have met since
[Reading an error message](tutorial:reading-an-error-message), and what
each one is telling you.

| Error | What it means |
|---|---|
| `IndexError` | You asked for a position that does not exist in a list. |
| `KeyError` | You asked for a key that does not exist in a dictionary. The message shows the key you asked for. |
| `AttributeError` | You asked a value for something it does not have. This often means the value is not the type you thought it was. |
| `NameError` | We met this one before. It also happens when a variable was created inside a function, and the code that uses it is outside that function. |

### Your turn

Each cell below raises one of the errors above. For each one:

1. Before you run it, decide which error it will raise.
2. Run it. Were you right?
3. Read the last line of the message. What does it tell you that you
   did not know?

```python exec
id: errors-from-lists-and-dictionaries-2
names = ["Aoife", "Ben", "Cara"]
print(names[len(names)])
```

```python exec
id: errors-from-lists-and-dictionaries-3
stock = {"apples": 12, "pears": 5}
print(stock["Apples"])
```

```python exec
id: errors-from-lists-and-dictionaries-4
scores = [85, 90]
scores.add(78)
print(scores)
```

```python exec
id: errors-from-lists-and-dictionaries-5
def total_price(price, quantity):
    total = price * quantity
    return total


total_price(4, 3)
print(total)
```

Look at the first one. The list has three names, so `len(names)` is 3.
But the positions are 0, 1 and 2. The last position is always one less
than the length. This mistake is so common that it has a name: an
*off-by-one error*.

In the second one, the key `"Apples"` has a capital A, and the key in
the dictionary does not. To Python, those are two different keys. The
message shows the key you asked for, so compare it letter by letter with
the keys you have.

In the third one, the message says `'list' object has no attribute
'add'`. A list has no `add` method. To put a value at the end of a list,
we use `append`.

In the fourth one, `total` exists only inside `total_price`. The
function gives back its value, but this code never stores it anywhere.
`result = total_price(4, 3)` would keep it.

## Tracebacks Through Several Functions

In [Reading an error message](tutorial:reading-an-error-message), every
traceback had one step, in the main part of the program. Now the next
cell has one function that calls another. When an error happens inside
a function that was called by another function, Python shows you the
whole chain, one step for each call.

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
describes it. That is what went wrong. Above it, the steps run from the
outermost call down to the innermost one. So the place where the error
happened is nearest the bottom.

This order confuses a lot of people. The top of a traceback is where
your program started, and the bottom is where it broke. When someone
sends you an error and asks what it means, look at the last line first.

Each step names a place. `in <module>` is the main part of the program,
as before. `in report` and `in average` mean the line is inside that
function.

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

In [Reading an error message](tutorial:reading-an-error-message), a
logical error hid in one line of arithmetic. In bigger programs, logical
errors hide much better: inside a function, a loop, or a condition that
somebody wrote weeks ago. What is wrong here?

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
something. We wrote test functions for exactly this in
[Designing and testing good functions](tutorial:building-reusable-tools).

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

## Debugging Habits

A mistake in a program is often called a *bug*. *Debugging* is finding
the bugs in a program and fixing them. When a program gives a wrong
answer and no error, where do we start? Two habits help more than any
others.

**The first habit: print the values in the middle.** This function
should add up some prices, then take off a discount. The prices add up
to 60, and 10% off 60 is 54. What does it print?

```python exec
id: debugging-habits-1
def shop_total(prices, discount):
    total = 0
    for price in prices:
        total = price
    return total - total * discount


print(shop_total([10, 20, 30], 0.1))
```

The answer is wrong, but where does it go wrong? We cannot see inside
the loop. So let's make the loop tell us. The next cell is the same
function, with one extra `print`.

```python exec
id: debugging-habits-2
def shop_total(prices, discount):
    total = 0
    for price in prices:
        total = price
        print("after adding", price, "the total is", total)
    return total - total * discount


print(shop_total([10, 20, 30], 0.1))
```

Now we can see it. After 10 the total is 10, which is right. After 20
it should be 30, but it is 20. The loop replaces the total each time,
when it should add to it. The line should be `total = total + price`.

Give each `print` a label, as this one does. A column of bare numbers is
hard to read. When the bug is fixed, take the extra `print` lines out
again.

**The second habit: test the small pieces.** A long function can go
wrong in many places. Two short functions, each tested on its own, can
only go wrong in two. Here is the same work split into two pieces:

```python exec
id: debugging-habits-3
def add_up(prices):
    total = 0
    for price in prices:
        total = total + price
    return total


def apply_discount(amount, discount):
    return amount - amount * discount


# Test each piece on its own, with answers we know.
print(add_up([10, 20, 30]), "should be 60")
print(apply_discount(100, 0.1), "should be 90")
print(apply_discount(add_up([10, 20, 30]), 0.1), "should be 54")
```

Each test uses numbers we can check in our heads. If a piece fails its
test, we know which piece to look at. If both pieces pass, and the whole
program still goes wrong, the bug is in how the pieces are joined.

### Your turn

This program gives each student a grade from the average of their
marks. A grade of Distinction needs 70 or more, Merit needs 50 or more,
and Pass needs 40 or more. Something is wrong.

1. Work out each student's average and grade by hand.
2. Run the cell. Which results are wrong?
3. Test `average` on its own, with a list whose average you know.
4. Test `grade` on its own, with 75, 55, 45 and 30.
5. Which function has the bug? Fix it, and run the cell again.

```python exec
id: debugging-habits-4
def average(marks):
    total = 0
    for mark in marks:
        total = total + mark
    return total / len(marks)


def grade(mark):
    if mark >= 40:
        return "Pass"
    elif mark >= 50:
        return "Merit"
    elif mark >= 70:
        return "Distinction"
    else:
        return "Fail"


def student_result(name, marks):
    return name + ": " + grade(average(marks))


print(student_result("Aoife", [72, 68, 80]))
print(student_result("Ben", [45, 50, 40]))
print(student_result("Cara", [30, 35, 20]))
```

## Reflection

Bigger programs bring the same three kinds of wrong, in new places.

**New runtime errors** come with new tools. An `IndexError` asks for a
position a list does not have, and it is very often off by one. A
`KeyError` asks for a key a dictionary does not have, and the message
shows the key, so check its spelling and its capitals.

**Long tracebacks** have one step for each function call. Read the last
line first. Then read upwards to see how the program got there. The
function where it broke is often correct, and the bad value came from a
line higher up.

**Logical errors** hide better in bigger programs. Check against answers
you already know, and test the exact boundary of every condition.

**Debugging habits** turn a hunt into a search. Print the values in the
middle, with labels, to see where they stop being right. Test each small
piece on its own, so that a failing test points at one piece.

In a few sentences: think of a bug you have met in your own code on an
earlier page. Which of these habits would have found it fastest?

## Where to Read More

Corey Schafer (2015). *Python Tutorial: Using Try/Except Blocks for Error
Handling.* <https://www.youtube.com/watch?v=NIWwJbo-9_8>. Where the errors
this page teaches you to read get handled deliberately, rather than fixed
by rewriting the line that raised them.
