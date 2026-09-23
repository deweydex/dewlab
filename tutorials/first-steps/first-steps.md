---
title: "Algorithms, pseudocode and your first Python"
year: "2026-2027"
version: 2026.09.22.1
covers:
  what-is-an-algorithm:
    covers: [MIT-6.1, PDP-LO2]
  pseudocode-planning-before-coding:
    covers: [PDP-LO5, PDP-LO6]
  a-few-more-things-python-can-do:
    covers: [PDP-LO4]
---

# Algorithms, pseudocode and your first Python

Welcome. This is the first programming page, and everyone starts here.
You do not need to know anything about computers or maths to begin.

Over the coming weeks we will learn to program, and we will learn some
maths along the way. The two are closer than most people expect. A
*program* is a set of clear steps, written carefully enough for a
computer to follow. A formula is also a set of steps, written for a
person. The idea is the same. Only the reader is different.

On this page we:

- run our first lines of Python
- use Python as a calculator
- write an everyday task as a list of clear steps
- plan a small program in plain English before we write it

Most of all, this page is about getting comfortable with the tools and
with a new way of thinking. We will take it one step at a time.

## How this page works

This is a page you can run. Most of it is reading, like this paragraph.
Between the paragraphs are *cells*. A cell is a small box of Python code.
You can change the code in a cell and run it, and the result appears
underneath.

The Python runs inside this browser tab, on the computer in front of you.
You do not need to install anything, and nobody else can see what you
type. If you make a mess of a cell, its **reset** button brings back the
code you started with.

To run a cell, press its **Run** button, or hold Ctrl and press Enter.
Let's try it with the cell below.

```python exec
id: how-this-page-works-1
print("Hello, world!")
```

Did `Hello, world!` appear under the cell? Then everything is working.
If nothing appears, Python may still be loading. The status message on
the page can tell you what is happening. You can also ask your teacher
to look at it with you.

That one line is a complete Python program. It tells the computer to
display a message. `print()` is a *function*. A function is a named tool
that does one job, and the job of `print()` is to display what is inside
its brackets. Here, that is the text in quotes. We will learn much more
about functions later.

The next cell has a few more lines. The lines that start with `#` are
*comments*. A comment is a note for the people who read the code. Python
ignores everything on a line after the `#`.

What do you think each `print()` line will show? Run the cell to check.

```python exec
id: how-this-page-works-2
# This is a comment. Python ignores everything after the # symbol.
# Comments are how we leave notes for ourselves and for other people
# reading our code. They are surprisingly important.

print("Python can do arithmetic too:")
print(2 + 3)
print(10 * 7)
print(100 / 4)
```

Did you notice that the numbers have no quotes around them? Python works
with numbers directly. Text needs quotes, and numbers do not.

The four basic operations are `+` for addition, `-` for subtraction, `*`
for multiplication and `/` for division. We will meet a few more further
down this page.

### Your turn

What could we work out next? Here are two ideas, or you can choose
numbers of your own.

1. How many hours are there in a week?
2. How many seconds are there in a day?

For each calculation, use `print()` to show the result. Add a comment
that says what the calculation works out.

```python exec
id: your-turn-1
# Try some calculations here
```

## What is an Algorithm?

An *algorithm* is a list of clear steps that complete a task. Each step
has only one meaning. We follow algorithms every day without thinking
about them. Here is one for making a cup of tea:

1. Fill the kettle with water
2. Turn the kettle on
3. While the water has not boiled, wait
4. Pour water into a cup containing a tea bag
5. Wait a few minutes
6. Remove the tea bag

What makes this a good algorithm? Three things:

- It starts from a known point: we have a kettle, water, a cup and a tea
  bag.
- The steps come in a clear order.
- It finishes: at the end, we have a cup of tea.

Step 3 is different from the others. "While the water has not boiled,
wait" repeats the waiting until the water boils. This is a *loop*. A loop
is a step, or a group of steps, that repeats until a condition is met.
We will write loops in Python in
[Repeating steps with loops](tutorial:repeating-yourself).

Programming is writing algorithms carefully enough for a computer to
follow them. A computer is very fast, but it cannot guess what you meant.
It does exactly what you tell it, and nothing more. So our instructions
need to be exact.

### Your turn

Think of a simple task from your everyday life: making breakfast, getting
to college, logging in to a computer, or anything you like. Can you write
it as a numbered list of steps? How much detail would the steps need for
someone who had never done the task before?

You could write the steps on paper, in a notebook, or in **Your notes**
under Settings. Use whatever is easiest for you.

## Pseudocode: Planning Before Coding

Before we write Python, it helps to plan the steps in plain English.
*Pseudocode* is a plan for a program, written in plain English, sometimes
with a little code-like structure. It looks a bit like code, but no
computer runs it. Writing pseudocode first is one of the most useful
habits you can build.

Here is an example. Suppose we want to change a temperature from Celsius
to Fahrenheit. The formula has three steps: multiply by 9, divide by 5,
then add 32.

**Pseudocode:**
```
GET the temperature in Celsius
MULTIPLY it by 9
DIVIDE the result by 5
ADD 32 to get Fahrenheit
DISPLAY the result
```

Here is the same plan in Python. The cell uses two names, `celsius` and
`fahrenheit`, to hold numbers. The next page,
[Variables, data types and text](tutorial:storing-and-computing), explains how
names like these work.

What do you expect 20 degrees Celsius to be in Fahrenheit? Run the cell
to check.

```python exec
id: pseudocode-planning-before-coding-1
# Temperature conversion: Celsius to Fahrenheit
celsius = 20
fahrenheit = celsius * 9 / 5 + 32
print(fahrenheit)
```

This is the main way of working in programming:

1. Think about what you want to do.
2. Write it as pseudocode.
3. Turn the pseudocode into Python.

For a small problem like this one, the pseudocode step can feel like
extra work. As problems get bigger, it becomes essential. We will use it
all through these tutorials.

### Your turn

Here is a different formula. To change kilometres to miles, multiply by
0.621371. How might that look as pseudocode?

1. In the cell below, write your pseudocode as comments: one line of
   plain English for each step, each starting with `#`.
2. Under each comment, write the Python for that step.
3. Run the cell.

Working this way keeps your thinking and your code side by side. That
helps when a step turns out to be harder than it looked.

```python exec
id: your-turn-2
# Now translate your pseudocode into Python here
```

## A Few More Things Python Can Do

Python works through a calculation in a fixed order, called the
*order of operations*. It is the same order you may know from school
maths as BODMAS or PEMDAS:

1. brackets (parentheses) first
2. then powers (exponents)
3. then multiplication and division
4. then addition and subtraction

Before you run the cell, what do you think `2 + 3 * 4` gives: 20 or 14?
Run the cell, and read the comment beside each line.

```python exec
id: a-few-more-things-python-can-do-1
# Order of operations
print(2 + 3 * 4)       # multiplication happens first: 2 + 12 = 14
print((2 + 3) * 4)     # brackets come first: 5 * 4 = 20

# Python has a power operator: **
print(2 ** 3)           # 2 to the power of 3 = 8
print(10 ** 2)          # 10 squared = 100

# Two kinds of division, and the remainder
print(17 / 5)           # regular division: 3.4
print(17 // 5)          # floor division, the whole-number part: 3
print(17 % 5)           # remainder (modulo): 2
```

Here are all the operators from this page in one table:

| Operator | What it does | Example | Result |
|---|---|---|---|
| `+` | addition | `17 + 5` | `22` |
| `-` | subtraction | `17 - 5` | `12` |
| `*` | multiplication | `17 * 5` | `85` |
| `/` | division | `17 / 5` | `3.4` |
| `//` | floor division: divides, then rounds down to a whole number | `17 // 5` | `3` |
| `%` | modulo: the remainder after division | `17 % 5` | `2` |
| `**` | power | `2 ** 3` | `8` |

The last operator, `%`, is called modulo. It gives the remainder after
division: 5 goes into 17 three times, with 2 left over. The remainder is
useful more often than you might expect. For example, a number is even
when its remainder after dividing by 2 is zero. We will use this idea a
lot.

### Your turn

What will each line print?

1. Write your prediction after `prediction:` on each line.
2. Run the cell.
3. Compare the results with your predictions.

A wrong prediction is the most useful kind. It is the moment you find out
what Python really does, which may be different from what you assumed.
If you would rather run the cell first and then work out why, that works
too.

```python exec
id: your-turn-3
# Your prediction next to each line, then run the cell
print(3 ** 4)           # prediction: 
print(100 // 7)         # prediction: 
print(100 % 7)          # prediction: 
print(2 ** 10)          # prediction: 
print(15 % 4)           # prediction: 
```

## Wrapping Up

On this page we have:

- run code in cells, and read what comes back
- used `print()` to display output
- written comments with `#`
- done arithmetic with `+`, `-`, `*`, `/`, `//`, `%` and `**`
- used the order of operations
- met the idea of an algorithm: a list of clear steps
- used pseudocode to plan before writing code

That is a good start. On the next page,
[Variables, data types and text](tutorial:storing-and-computing), we will learn
about *variables*: how to store information, and how to work with
different types of data. We will also start to explore the number
systems that computers use.

### Reflection

When you are ready, write a few sentences about this page. What made
sense? What was confusing? What are you curious about? You could write
in **Your notes** under Settings, or think it over.

## Where to Read More

Everything here is covered elsewhere too, often in a form that will suit you
better than this one. These are worth your time.

Downey, A. B. (2015). *Think Python: How to Think Like a Computer Scientist*
(2nd ed.). Green Tea Press. Free at <https://greenteapress.com/wp/think-python-2e/>.
Chapters 1 and 2 cover this tutorial's ground at greater length, and the book is
written for exactly this audience.

Python Software Foundation. *The Python Tutorial*, sections 3.1 and 3.1.1.
<https://docs.python.org/3/tutorial/introduction.html>. The official reference
for the arithmetic operators, including the exact behavior of `//` and `%`.

Computerphile (2017). *What on Earth is an Algorithm?*
<https://www.youtube.com/watch?v=X0HHUlAiA4E>. Nine minutes on what does and
does not count as an algorithm, which is a harder question than it first looks.

Khan Academy. *Intro to algorithms*.
<https://www.khanacademy.org/computing/computer-science/algorithms>. Worked
through slowly, with exercises, if the pace here was too quick.
