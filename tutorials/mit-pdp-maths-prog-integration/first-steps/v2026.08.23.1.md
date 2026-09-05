---
title: "First Steps"
slug: first-steps
module: mit-pdp-maths-prog-integration
module_title: "Programming and Maths, Integrated"
year: "2026-2027"
series: programming-foundations
version: 2026.08.23.1
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

Welcome. Over the coming weeks we are going to learn to program and to think mathematically, and we are going to discover that these two activities are much more closely related than most people realise. A program is just an algorithm written precisely enough for a computer to follow. A mathematical formula is just an algorithm written precisely enough for a person to follow. Same idea, different audience.

This first tutorial is about getting comfortable with the tools and the way of thinking. There is nothing to be afraid of here -- we will take it step by step, and every expert started exactly where you are now.

## How this page works

You are looking at a page you can run. Most of it is ordinary reading — like
this paragraph. Interleaved with the reading are *cells*: small boxes of Python
that you can edit and run, with the result appearing directly underneath.

The Python runs inside this browser tab, on the machine in front of you.
Nothing is installed, nothing is sent anywhere, and nobody else can see what
you type. If you make a mess of a cell, the **reset** button on it puts back
the version you started with.

To run a cell, press its **Run** button, or hold Ctrl and press Enter. Try it
with the cell below.

```python exec
id: how-this-page-works-1
print("Hello, world!")
```

If you saw `Hello, world!` appear below the cell, everything is working. That single line is a complete Python program -- it tells the computer to display a message. The `print()` part is a *function* (we will learn much more about functions later), and the text in quotes is what we want it to display.

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

In the cell below, try a few calculations of your own. Maybe work out how many hours there are in a week, or how many seconds in a day. Use `print()` to display the results, and use comments to explain what each calculation does.

```python exec
id: your-turn-1
# Try some calculations here
```

## What is an Algorithm?

An algorithm is simply a sequence of clear, unambiguous steps that accomplish a task. You follow algorithms all the time without thinking about them. Making a cup of tea is an algorithm:

1. Fill the kettle with water
2. Turn the kettle on
3. While the water has not boiled, wait
4. Pour water into a cup containing a tea bag
5. Wait a few minutes
6. Remove the tea bag

This example has all the hallmarks of a good algorithm: it starts from a known state (you have a kettle, water, a cup, and a tea bag), the steps are in a specific order, and it terminates (you end up with tea). It even has a *loop* in step 3 -- "while the water has not boiled, wait" repeats the waiting until a condition is met.

Programming is the art of writing algorithms precisely enough that a computer can follow them. The computer is very fast but not very clever -- it will do exactly what you tell it, nothing more and nothing less. This means we need to be precise about our instructions.

### Your turn

Think of a simple everyday task and write it out as a numbered sequence of steps. It could be making breakfast, getting to college, logging into a computer -- anything you like. Try to be specific enough that someone who had never done the task before could follow your instructions.

Double-click this cell and write your algorithm below:

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

Here is a different formula: to convert kilometres to miles, multiply by 0.621371.

Write your pseudocode first, as comments in the cell below — a line of plain
English per step. Then turn each line into Python underneath it. Working this
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

Before running the cell below, *predict* what each line will print. Write your predictions as comments, then run the cell and see if you were right. Getting predictions wrong is perfectly fine -- that is how we learn what is actually happening.

```python exec
id: your-turn-3
# Write your prediction next to each line, then run the cell
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

Take a moment to write a few sentences about this tutorial. What made sense? What was confusing? What are you curious about?

Double-click this cell to write your thoughts:
