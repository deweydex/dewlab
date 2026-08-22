---
title: "Building Reusable Tools"
slug: building-reusable-tools
module: mit-pdp-maths-prog-integration
module_title: "Programming and Maths, Integrated"
year: "2026-2027"
series: maths-and-programming
version: 1
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

**Programming Design Principles / Maths for IT**

In the first seven tutorials, we learned to write functions. In Skills Demo 1, we used them to build algorithms. Now we are going to think more carefully about how to *design* functions -- not just to solve a specific problem, but to create tools we can reuse and combine.

This tutorial is about the craft of writing good functions. It connects to a professional practice called *modular design*, where complex programs are built from small, independent, well-tested pieces.

## What Makes a Good Function?

A good function does one thing, does it well, and communicates clearly what it does. Let's look at an example and think about what makes it work:

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

That triple-quoted string at the top of the function is called a *docstring*. It describes what the function does, what it expects as input, and what it returns. This is not just decoration -- it is how professional programmers communicate the *contract* of a function. Anyone who wants to use `mean()` can read the docstring and know exactly what to pass in and what they will get back.

From now on, every function we write should have a docstring. It does not need to be elaborate -- a single clear sentence is often enough -- but it should be there.

## Functions Calling Functions

The real power of modular design appears when functions use other functions as building blocks. Here is a function that computes the standard deviation -- and notice how it uses `mean()`:

```python exec
id: functions-calling-functions-1
def std_dev(numbers):
    """Compute the population standard deviation of a list of numbers."""
    avg = mean(numbers)
    squared_diffs = []
    for value in numbers:
        diff = value - avg
        squared_diffs.append(diff ** 2)
    return mean(squared_diffs) ** 0.5

print(std_dev([10, 20, 30]))
```

We did not rewrite the averaging logic inside `std_dev`. We called `mean()` twice -- once for the original average, and once to average the squared differences. This is the essence of modular design: build small tools and combine them.

If we later discover a bug in `mean()`, we fix it once and `std_dev()` automatically benefits. If we want to use `mean()` somewhere else, it is already available. Each function is an independent, tested unit.

### Your turn

Write a function `data_range(numbers)` that returns the difference between the largest and smallest values in a list. Then write a function `describe(numbers)` that calls `mean()`, `std_dev()`, and `data_range()` to print a summary of the data.

Include docstrings for both functions.

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

What happens if someone calls `mean([])` -- with an empty list? Division by zero. A good function anticipates this:

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

Returning `None` for invalid input is one common approach. Another is to print a clear error message. The important thing is that the function does not crash silently or return a misleading result.

### Your turn

Go back to your `data_range` function. What happens with an empty list? A list with one element? Update it to handle these cases gracefully.

```python exec
id: your-turn-4
# Updated data_range with edge case handling
```

## Variable Scope Revisited

Now that we are writing functions that call other functions, let's make sure we understand scope. Each function has its own workspace. Variables created inside a function vanish when the function finishes:

```python exec
id: variable-scope-revisited-1
def add_tax(price, rate):
    tax = price * rate
    total = price + tax
    return total

result = add_tax(100, 0.23)
print("Total:", result)

# These would cause errors if uncommented:
# print(tax)      # does not exist here
# print(total)    # does not exist here either
```

This is a feature: it means you can use the name `total` inside multiple different functions without them interfering with each other. Each function's `total` is its own separate variable.

The way functions communicate is through *parameters* (values passed in) and *return values* (values sent back). This is cleaner and more reliable than sharing global variables.

### Your turn

Write two functions that each use a variable called `count` internally but for different purposes. Verify that they do not interfere with each other.

```python exec
id: your-turn-5
# Two functions that both use 'count' internally
```

```python exec
id: your-turn-6
# Demonstrate they work independently
```

## Testing as a Habit

So far we have been testing informally: run the function, check the output by eye. Let's make this more systematic. A good test checks that a function produces the expected output for a known input:

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

Writing tests like this before or alongside your functions is one of the most valuable habits you can develop. It forces you to think clearly about what the function should do, and it gives you confidence that the function actually does it.

### Your turn

Write a test function for your `data_range` function. Include at least four test cases: a normal list, a list where all elements are the same, a list with negative numbers, and a single-element list.

```python exec
id: your-turn-7
# Your test_data_range function
```

## Reflection

Today was less about new Python syntax and more about *how to think* when writing functions: single responsibility, docstrings, edge cases, scope discipline, and systematic testing. These are the practices that separate code that works once from code that can be relied upon.

In the next tutorials, we will use these practices to build tools for counting, probability, and statistics -- each one a well-documented, well-tested function that becomes part of our growing toolkit.

What feels different about thinking of functions as *tools* versus thinking of them as *solutions to homework problems*?
