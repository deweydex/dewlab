---
title: "Lists and Sequences"
slug: lists-and-sequences
module: mit-pdp-maths-prog-integration
module_title: "Programming and Maths, Integrated"
year: "2026-2027"
series: maths-and-programming
version: 1
covers:
  lists-ordered-collections:
    covers: [MIT-6.3]
  building-lists-with-loops:
    covers: [MIT-6.3, MIT-6.7]
  looping-over-lists:
    covers: [MIT-6.5, MIT-6.7]
  functions-reusable-algorithms:
    covers: [PDP-LO8]
  mathematical-sequences-as-functions:
    covers: [MIT-6.2]
  the-dot-product-lists-meet-arithmetic:
    covers: [MIT-6.3]
---

# Lists and Sequences

**Programming Design Principles / Maths for IT**

Until now we have been working with individual values: a single number, a single string. But most interesting problems involve *collections* of data: a set of test scores, a sequence of temperatures, a list of student names. Today we learn how Python handles collections, and we will write our first *functions* -- reusable blocks of code that we can call whenever we need them.

## Lists: Ordered Collections

A list is an ordered sequence of values, enclosed in square brackets:

```python exec
id: lists-ordered-collections-1
scores = [42, 38, 35, 47, 29, 41, 44, 33, 39, 48]
print(scores)
print("Number of scores:", len(scores))
```

Each element in a list has a position called its *index*. Python uses zero-based indexing, meaning the first element is at index 0:

```python exec
id: lists-ordered-collections-2
print(scores[0])    # first element
print(scores[1])    # second element
print(scores[9])    # tenth (last) element
print(scores[-1])   # also the last element (negative indexing counts from the end)
```

You can also take a *slice* -- a portion of the list:

```python exec
id: lists-ordered-collections-3
print(scores[2:5])    # elements at indices 2, 3, 4 (the end index is excluded)
print(scores[:3])     # first three elements
print(scores[7:])     # from index 7 to the end
```

Lists are *mutable* -- we can change their contents:

```python exec
id: lists-ordered-collections-4
scores[0] = 45       # replace the first element
print(scores)

scores.append(50)    # add an element at the end
print(scores)
print("Now we have", len(scores), "scores")
```

### Your turn

Create a list called `temperatures` containing at least 7 temperature values. Then:
1. Print the first and last temperatures
2. Print the middle three temperatures (using a slice)
3. Change one of the temperatures and print the updated list

```python exec
id: your-turn-1
# Your list work here
```

## Building Lists with Loops

One of the most useful patterns is constructing a list by starting empty and appending values:

```python exec
id: building-lists-with-loops-1
# Build a list of the first 10 square numbers
squares = []
for i in range(1, 11):
    squares.append(i ** 2)
print(squares)
```

This is the list-building version of the accumulator pattern. Instead of accumulating a sum, we accumulate a collection.

### Your turn

Build a list containing the first 15 terms of the Fibonacci sequence. Each term is the sum of the two preceding terms, starting with 1, 1. So the sequence begins: 1, 1, 2, 3, 5, 8, 13, ...

**Pseudocode:**

```python exec
id: your-turn-2
# Your Fibonacci list builder
```

## Looping Over Lists

A `for` loop can iterate directly over the elements of a list:

```python exec
id: looping-over-lists-1
names = ["Ada", "Grace", "Alan", "Margaret"]

for name in names:
    print("Hello, " + name)
```

Sometimes we need both the index and the value. We could use `range(len(list))`, but Python provides a cleaner way with `enumerate()`:

```python exec
id: looping-over-lists-2
for index, name in enumerate(names):
    print(str(index) + ": " + name)
```

### Your turn: Summing a list

Using the accumulator pattern and a for loop, compute the sum of all elements in the `scores` list we created earlier. Do not use Python's built-in `sum()` function -- write the loop yourself.

```python exec
id: your-turn-summing-a-list-1
# Sum the scores using a loop
scores = [42, 38, 35, 47, 29, 41, 44, 33, 39, 48]
```

## Functions: Reusable Algorithms

We have been writing code that does useful things, but if we wanted to do the same thing again with different data, we would have to copy and paste. Functions solve this problem. A function is a named block of code that we can call whenever we need it, passing in different inputs each time.

```python exec
id: functions-reusable-algorithms-1
def greet(name):
    print("Hello, " + name + "!")

# Now we can call it as many times as we want
greet("Ada")
greet("Grace")
greet("Alan")
```

The `def` keyword defines a function. `name` is a *parameter* -- a placeholder for the value we will provide when we call the function. The indented code is the function body. When we write `greet("Ada")`, `"Ada"` is the *argument* that gets assigned to the parameter `name`.

Most useful functions *return* a value rather than just printing:

```python exec
id: functions-reusable-algorithms-2
def square(n):
    return n ** 2

result = square(7)
print(result)
print(square(12))
```

The `return` statement sends a value back to the caller. This is what makes functions truly powerful -- we can use the result in further calculations.

### Your turn

Write a function called `celsius_to_fahrenheit` that takes a temperature in Celsius and returns the Fahrenheit equivalent. Test it with a few values you can verify.

```python exec
id: your-turn-3
# Pseudocode:
#

# Your function
```

```python exec
id: your-turn-4
# Test it
```

## Mathematical Sequences as Functions

In mathematics, a sequence is a list of numbers generated by a rule. The rule is just a function that maps a position (index) to a value.

For example, the sequence of square numbers $1, 4, 9, 16, 25, ...$ is generated by the function $f(n) = n^2$.

The sequence of triangular numbers $1, 3, 6, 10, 15, ...$ is generated by $f(n) = \frac{n(n+1)}{2}$ -- which is also $\sum_{i=1}^{n} i$.

Let's write functions that generate these sequences:

```python exec
id: mathematical-sequences-as-functions-1
def square_number(n):
    return n ** 2

def triangular_number(n):
    return n * (n + 1) // 2

# Generate the first 8 terms of each
for i in range(1, 9):
    print("n=" + str(i) + ":  square=" + str(square_number(i)) + 
          "  triangular=" + str(triangular_number(i)))
```

### Your turn

Write a function `generate_sequence(func, n)` that takes *another function* as its first argument and an integer n, and returns a list containing the first n terms of the sequence generated by that function. Then use it with `square_number` and `triangular_number`.

This might seem strange -- passing a function to a function -- but it is a powerful idea.

```python exec
id: your-turn-5
# Your generate_sequence function
```

```python exec
id: your-turn-6
# Test it
# generate_sequence(square_number, 5) should give [1, 4, 9, 16, 25]
```

## The Dot Product: Lists Meet Arithmetic

When we have two lists of the same length, we can combine them element by element. The *dot product* multiplies corresponding elements and sums the results:

$$\vec{a} \cdot \vec{b} = \sum_{i=0}^{n-1} a_i \times b_i$$

For example, $[1, 2, 3] \cdot [4, 5, 6] = 1 \times 4 + 2 \times 5 + 3 \times 6 = 32$.

This operation is fundamental in machine learning, physics, and many other fields.

### Your turn

Write a function `dot_product(a, b)` that computes the dot product of two lists. Think about what should happen if the lists are different lengths -- your function should handle this gracefully rather than crashing.

**Pseudocode:**

```python exec
id: your-turn-7
# Your dot_product function
```

```python exec
id: your-turn-8
# Test cases
# dot_product([1, 2, 3], [4, 5, 6]) should be 32
# What should dot_product([1, 2], [3, 4, 5]) return?
```

## Reflection

Today we covered lists (creation, indexing, slicing, mutability, building with loops), iteration over lists, and functions (definition, parameters, return values). We also saw how mathematical sequences and operations like the dot product translate directly into code.

Functions are a major turning point. From now on, when we solve a problem, we will package the solution as a function so we can reuse it. This is the beginning of *modular* programming -- building complex programs from simple, tested pieces.

What connections are you seeing between the mathematical ideas and the programming patterns?
