---
title: "Building Reusable Tools"
year: "2026-2027"
version: 2026.09.22.1
covers:
  what-makes-a-good-function:
    covers: [PDP-LO8, PDP-LO11]
  functions-calling-functions:
    covers: [PDP-LO8]
  handling-edge-cases:
    covers: [PDP-LO7]
  variable-scope-revisited:
    covers: [PDP-LO8]
  testing-as-a-habit:
    covers: [PDP-LO10]
---

# Building Reusable Tools

In the tutorials so far, we learned to write functions, and then used
them to build algorithms. On this page we think more carefully about how
to *design* a function. A well-designed function becomes a tool. We can
use it again, and combine it with other tools. A function that is not
designed well solves only one problem, once.

This page is about the craft of writing good functions. It builds on the
idea of modular programming from
[Lists and Sequences](tutorial:lists-and-sequences). Programmers also
call this modular design: building large programs from small, separate
pieces, each one well tested.

On this page we:

- look at what makes a function good, and how to describe it
- build functions out of other functions
- handle awkward inputs, such as an empty list
- test our functions on purpose, not only by eye

## What Makes a Good Function?

A good function does one thing, and does it well. It also makes clear
what it does. Here is an example. As you read it, ask yourself: what
makes it easy to use?

```python exec
id: what-makes-a-good-function-1
def mean(numbers):
    """Compute the arithmetic mean of a list of numbers.
    
    Parameters:
        numbers: a list of numeric values (must not be empty)
    
    Returns:
        the arithmetic mean as a float
    """
    total = 0
    for value in numbers:
        total = total + value
    return total / len(numbers)

# Test it
print(mean([10, 20, 30]))        # should be 20.0
print(mean([1, 2, 3, 4, 5]))     # should be 3.0
```

The string in triple quotes at the top of the function is a *docstring*.
A docstring is a description of a function, written at the top of it. It
says what the function does, what it needs as input, and what it gives
back.

Together, those things are the function's *contract*. A function's
contract is its promise: give it this, and it gives you that. Anyone who
wants to use `mean()` can read the docstring, and know what to pass in
and what they will get back, without reading the code.

From now on, every function we write should have a docstring. It does
not need to be long. One clear sentence is often enough. But it should
be there.

## Functions Calling Functions

Modular design becomes really useful when functions use other functions
as building blocks.

The next function works out the *standard deviation* of a list of
numbers. The standard deviation is a measure of how spread out the
numbers are around their mean. Here we compute the population
standard deviation, which uses every value in the list:

1. Find the mean.
2. For each value, find its difference from the mean, and square it.
3. Find the mean of those squares.
4. Take the square root.

Look at how the function uses `mean()`. How many times does it call it?

```python exec
id: functions-calling-functions-1
def std_dev(numbers):
    """Compute the population standard deviation of a list of numbers."""
    average = mean(numbers)
    squared_differences = []
    for value in numbers:
        difference = value - average
        squared_differences.append(difference ** 2)
    return mean(squared_differences) ** 0.5

print(std_dev([10, 20, 30]))
```

We did not write the averaging code again inside `std_dev`. We called
`mean()` twice: once for the mean of the numbers, and once for the mean
of the squared differences. This is the heart of modular design. We
build small tools, and then combine them.

Say we later find a bug in `mean()`. We fix it once, and `std_dev()` is
fixed too. If we want `mean()` somewhere else, it is already there. Each
function is a separate unit that we can test on its own.

### Your turn

1. Write a function `data_range(numbers)`. It returns the difference
   between the largest and the smallest values in a list. In statistics,
   this difference is called the range. It has nothing to do with
   Python's `range()`.
2. Write a function `describe(numbers)`. It calls `mean()`, `std_dev()`
   and `data_range()`, and prints a summary of the data.
3. Give both functions a docstring.
4. Test `describe` on the data in the third cell.

```python exec
id: your-turn-1
# Pseudocode for data_range:
#

# Your data_range function
```

```python exec
id: your-turn-2
# Your describe function
```

```python exec
id: your-turn-3
# Test describe with some data
test_data = [42, 38, 35, 47, 29, 41, 44, 33, 39, 48]
```

## Handling Edge Cases

What happens if someone calls `mean([])`, with an empty list? The list
has length 0, so `mean` divides by zero.

An empty list is an *edge case*. An edge case is an unusual input, at
the edge of what a function expects, that the function must handle on
purpose. A good function plans for its edge cases:

```python exec
id: handling-edge-cases-1
def safe_mean(numbers):
    """Compute the arithmetic mean, returning None for empty lists."""
    if len(numbers) == 0:
        return None
    total = 0
    for value in numbers:
        total = total + value
    return total / len(numbers)

print(safe_mean([1, 2, 3]))
print(safe_mean([]))
```

Returning `None` for input that makes no sense is one common way. Another
way is to print a clear error message. What matters is that the function
does not fail in a confusing way, and does not return an answer that
looks right but is wrong.

### Your turn

Go back to your `data_range` function.

1. What happens when you give it an empty list?
2. What happens with a list of one element?
3. Change the function so that it handles both cases in a way you chose
   on purpose.

```python exec
id: your-turn-4
# Updated data_range with edge case handling
```

## Variable Scope Revisited

Our functions now call other functions, so let's check that we
understand scope, which we met in [Finding Things](tutorial:finding-things).
Each function has its own workspace. The variables created inside a
function disappear when the function finishes.

The last two lines of the next cell are comments. What do you think
would happen if they ran?

```python exec
id: variable-scope-revisited-1
def add_tax(price, rate):
    tax = price * rate
    total = price + tax
    return total

result = add_tax(100, 0.23)
print("Total:", result)

# What happens if these lines run? Delete the # at the start of one to find out.
# print(tax)
# print(total)
```

Each line gives a `NameError`, because neither `tax` nor `total` exists
outside the function.

This helps us. We can use the name `total` inside many different
functions, and they do not get in each other's way. Each function's
`total` is its own separate variable.

Functions pass information in two ways. Parameters bring values in.
Return values send values back. This is clearer and more reliable than
sharing global variables.

### Your turn

1. Write two functions. Each one uses a variable called `count` inside
   it, for a different purpose.
2. In the second cell, call both functions. Do they get in each other's
   way?

```python exec
id: your-turn-5
# Two functions that both use 'count' internally
```

```python exec
id: your-turn-6
# Demonstrate they work independently
```

## Testing as a Habit

So far, we have tested by running a function and checking the output by
eye. Let's make testing more careful. A good test gives a function an
input where we already know the right answer, and checks that the
function gives that answer.

A *test function* is a function that does this for another function, and
prints PASS or FAIL for each check:

```python exec
id: testing-as-a-habit-1
def test_mean():
    """Test the mean function with known cases."""
    # Basic case
    result = mean([10, 20, 30])
    expected = 20.0
    if result == expected:
        print("PASS: mean([10, 20, 30]) = " + str(result))
    else:
        print("FAIL: mean([10, 20, 30]) expected " + str(expected) + " got " + str(result))
    
    # Single element
    result = mean([42])
    expected = 42.0
    if result == expected:
        print("PASS: mean([42]) = " + str(result))
    else:
        print("FAIL: mean([42]) expected " + str(expected) + " got " + str(result))
    
    # Negative numbers
    result = mean([-10, 10])
    expected = 0.0
    if result == expected:
        print("PASS: mean([-10, 10]) = " + str(result))
    else:
        print("FAIL: mean([-10, 10]) expected " + str(expected) + " got " + str(result))

test_mean()
```

Writing tests like this, before or while you write a function, is one of
the most valuable habits you can build. It makes you think carefully about
what the function should do. It also gives you confidence that the
function does it.

### Your turn

Write a test function for your `data_range` function. Include at least
four test cases:

1. an ordinary list
2. a list where every element is the same
3. a list with negative numbers
4. a list with only one element

```python exec
id: your-turn-7
# Your test_data_range function
```

## Reflection

This page had little new Python in it. It was about *how to think* when
we write functions:

- each function does one thing
- each function has a docstring
- each function handles its edge cases
- variables stay inside the function that made them
- we test each function on purpose

These habits are the difference between code that works once and code
that people can rely on.

If your course goes on to counting, probability and statistics, we use
these habits there to build more tools. Each one is a function with a
docstring and tests, and each one joins our growing toolkit.

What feels different about thinking of functions as *tools*, and not as
*answers to homework problems*?

## Where to Read More

Corey Schafer (2017). *Python Tutorial: Unit Testing Your Code with the
unittest Module.* <https://www.youtube.com/watch?v=6tNS--WetLI>. Testing by
hand, the way this page does it, is the first step; this is the second.

Python Software Foundation. *The Python Tutorial — Defining Functions.*
<https://docs.python.org/3/tutorial/controlflow.html#defining-functions>.
The official reference for docstrings, default arguments, and everything
else a function definition can do.
