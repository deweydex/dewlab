---
title: "First Steps"
slug: first-steps
module: mit-pdp-maths-prog-integration
module_title: "Programming and Maths, Integrated"
year: "2026-2027"
series: maths-and-programming
version: 2026.08.23.2
covers:
  what-is-an-algorithm:
    covers: [MIT-6.1, PDP-LO2]
  pseudocode-planning-before-coding:
    covers: [PDP-LO5, PDP-LO6]
  a-few-more-things-python-can-do:
    covers: [PDP-LO4]
---

# First Steps

**Programming Design Principles / Maths for IT**

Welcome. Here we explore programming and maths together. In this first
tutorial, we can run a small program, try calculations, and plan a set
of steps for a computer to follow.

We will meet the tools one at a time. You can return to an example or
ask for help whenever a step is unclear.

## How this page works

Many examples are in *cells*: code boxes you can change and run. A cell's
**Run** button shows the result below. `Ctrl+Enter` also runs the cell
while you are editing it.

Python runs in your browser. You do not need to install anything or make
an account. Settings has a **Your work** section with notes, saving
information, and ways to keep a copy of your work.

A tutorial cell's **reset** button restores its original code and clears
its result. This replaces your edits in that cell. It does not clear
values already held by Python. You can keep a copy before resetting.

We could begin with the cell below. What appears when you use **Run**?

```python exec
id: how-this-page-works-1
print("Hello, world!")
```

The result should be `Hello, world!` below the cell. This program asks
Python to display a message. `print()` is a *function*, a named piece of
code that performs a task. Here, its task is to display the text in quotes.
We will explore functions in more detail later.

If the result does not appear, Python may still be loading. The page's
status message can help explain what is happening. You can also ask your
teacher to look with you.

Let's try a few more things.

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

Notice that Python can work with numbers directly -- no quotes needed. The four basic operations are `+` (addition), `-` (subtraction), `*` (multiplication), and `/` (division). There are a few more we will meet shortly.

### Your turn

What calculation could we try next? You could work out the hours in a
week or choose numbers of your own. `print()` displays the result. A
comment can explain what your calculation means.

```python exec
id: your-turn-1
# Try some calculations here
```

## What is an Algorithm?

An *algorithm* is a sequence of clear, unambiguous steps that accomplish a task. You follow algorithms all the time without thinking about them. Making a cup of tea is an algorithm:

1. Fill the kettle with water
2. Turn the kettle on
3. While the water has not boiled, wait
4. Pour water into a cup containing a tea bag
5. Wait a few minutes
6. Remove the tea bag

This example has all the hallmarks of a good algorithm: it starts from a known state (you have a kettle, water, a cup, and a tea bag), the steps are in a specific order, and it terminates (you end up with tea). It even has a *loop* in step 3 -- "while the water has not boiled, wait" repeats the waiting until a condition is met.

Programming is the art of writing algorithms precisely enough that a computer can follow them. The computer is very fast but not very clever -- it will do exactly what you tell it, nothing more and nothing less. This means we need to be precise about our instructions.

### Your turn

What is a simple everyday task you could write out as a numbered sequence of steps? Making breakfast, getting to college, logging into a computer -- anything you like. How specific would it have to be for someone who had never done it before to follow along?

You can write the steps in **Your notes**, under Settings, or on paper.

## Pseudocode: Planning Before Coding

Before we write actual Python, it helps to plan what we want to do in plain English (or a mix of English and code-like structure). This is called *pseudocode*, and it is one of the most valuable habits you can develop.

Here is an example. Suppose we want to convert a temperature from Celsius to Fahrenheit. The formula is: multiply by 9, divide by 5, then add 32.

**Pseudocode:**
```
GET the temperature in Celsius
MULTIPLY it by 9
DIVIDE the result by 5
ADD 32 to get Fahrenheit
DISPLAY the result
```

Now let's turn that into Python:

```python exec
id: pseudocode-planning-before-coding-1
# Temperature conversion: Celsius to Fahrenheit
celsius = 20
fahrenheit = celsius * 9 / 5 + 32
print(fahrenheit)
```

That is the core loop of programming: think about what you want to do, write it in pseudocode, then translate to Python. The pseudocode step might feel unnecessary for simple problems, but as things get more complex it becomes essential. We will use it throughout these tutorials.

### Your turn

Here is a different formula: to convert kilometres to miles, multiply by 0.621371. How might that look as pseudocode?

Let's try the pseudocode first, as comments in the cell below — a line of plain
English per step. Then each line can become Python underneath it. Working this
way keeps the thinking and the code side by side, which is exactly what you
want when a step turns out to be harder than it looked.

```python exec
id: your-turn-2
# Now translate your pseudocode into Python here
```

## A Few More Things Python Can Do

Let's explore a bit more before we wrap up. Python follows the standard mathematical order of operations (sometimes called PEMDAS or BODMAS): parentheses first, then exponents, then multiplication and division, then addition and subtraction.

```python exec
id: a-few-more-things-python-can-do-1
# Order of operations
print(2 + 3 * 4)       # multiplication happens first: 2 + 12 = 14
print((2 + 3) * 4)     # parentheses override: 5 * 4 = 20

# Python has a power operator: **
print(2 ** 3)           # 2 to the power of 3 = 8
print(10 ** 2)          # 10 squared = 100

# And two types of division
print(17 / 5)           # regular division: 3.4
print(17 // 5)          # integer (floor) division: 3
print(17 % 5)           # remainder (modulo): 2
```

That last operator, `%` (called modulo), gives us the remainder after division. It turns out to be surprisingly useful. For instance, a number is even if its remainder when divided by 2 is zero. We will use this idea a lot.

### Your turn

What do you think each line below will print? You could write a
prediction in a comment, then run the cell to compare. You can also run
it first and use the results to explore what each operator does. If a
result is different from your prediction, an earlier example may help
explain it.

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

In this first tutorial we have covered:

- Running code in cells, and reading what comes back
- Using `print()` to display output
- Writing comments with `#`
- Basic arithmetic: `+`, `-`, `*`, `/`, `//`, `%`, `**`
- Order of operations
- The idea of an algorithm as a sequence of clear steps
- Pseudocode as a planning tool before writing code

That is a solid foundation. In the next tutorial we will learn about *variables* -- how to store information and work with different types of data -- and we will start exploring the different number systems that computers use.

### Reflection

What made sense? What would you like another example of? You can choose
one question to write about in **Your notes**, under Settings, or leave
it for another visit.

## Where to Read More

Everything here is covered elsewhere too, often in a form that will suit you
better than this one. These are worth your time.

Downey, A. B. (2015). *Think Python: How to Think Like a Computer Scientist*
(2nd ed.). Green Tea Press. Free at <https://greenteapress.com/wp/think-python-2e/>.
Chapters 1 and 2 cover this tutorial's ground at greater length, and the book is
written for exactly this audience.

Python Software Foundation. *The Python Tutorial*, sections 3.1 and 3.1.1.
<https://docs.python.org/3/tutorial/introduction.html>. The official reference
for the arithmetic operators, including the exact behaviour of `//` and `%`.

Computerphile (2017). *What on Earth is an Algorithm?*
<https://www.youtube.com/watch?v=X0HHUlAiA4E>. Nine minutes on what does and
does not count as an algorithm, which is a harder question than it first looks.

Khan Academy. *Intro to algorithms*.
<https://www.khanacademy.org/computing/computer-science/algorithms>. Worked
through slowly, with exercises, if the pace here was too quick.
