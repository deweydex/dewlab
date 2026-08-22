---
title: "Repeating Yourself"
slug: repeating-yourself
module: mit-pdp-maths-prog-integration
module_title: "Programming and Maths, Integrated"
year: "2026-2027"
series: maths-and-programming
version: 1
covers:
  while-loops-repeat-until-done:
    covers: [PDP-LO6]
  for-loops-when-you-know-how-many-times:
    covers: [PDP-LO6, MIT-6.7]
  sigma-notation-mathematics-meets-loops:
    covers: [MIT-6.4]
  nested-loops:
    covers: [PDP-LO6]
  building-up-gradually-counting-with-conditions:
    covers: [MIT-6.7]
---

# Repeating Yourself

**Programming Design Principles / Maths for IT**

We can now write programs that execute in sequence and make decisions. But we are still missing a crucial capability: repetition. Imagine calculating the sum of 100 numbers, or checking every item in a list, or converting a whole batch of temperatures. Without loops, we would need to write the same code over and over.

Today we learn to make the computer repeat things for us, and we will discover that mathematical notation has had the same idea for centuries.

## While Loops: Repeat Until Done

A `while` loop keeps executing its body as long as a condition remains True:

```python exec
id: while-loops-repeat-until-done-1
# Count from 1 to 5
count = 1

while count <= 5:
    print(count)
    count = count + 1

print("Done!")
```

Three things make a while loop work:

First, an initial state (`count = 1`). Second, a condition that gets checked before each iteration (`count <= 5`). Third, an update inside the loop body that eventually makes the condition False (`count = count + 1`). Forget that third part and the loop runs forever -- a very common mistake, and one worth experiencing once (you can interrupt a running cell with the stop button or Kernel > Interrupt).

### Your turn

Before running the next cell, trace through it by hand: for each iteration, write down the value of `total` and `n`. Predict the final output, then run it to check.

```python exec
id: your-turn-1
# Predict the output first
total = 0
n = 1

while n <= 4:
    total = total + n
    n = n + 1

print(total)

# Your trace:
# n=1: total becomes ?, n becomes ?
# n=2: total becomes ?, n becomes ?
# n=3: total becomes ?, n becomes ?
# n=4: total becomes ?, n becomes ?
# Final total: ?
```

That program computes 1 + 2 + 3 + 4. This pattern -- starting with zero and repeatedly adding -- is called the *accumulator pattern*, and it is one of the most common structures in programming.

## For Loops: When You Know How Many Times

When we know in advance how many times to repeat, a `for` loop is cleaner. The `range()` function generates a sequence of numbers:

```python exec
id: for-loops-when-you-know-how-many-times-1
# Count from 0 to 4
for i in range(5):
    print(i)
```

`range(5)` produces the numbers 0, 1, 2, 3, 4 -- five numbers starting from 0. This might seem odd, but starting from 0 turns out to be very convenient in programming (we will see why when we work with lists).

You can also specify a start and a step:

```python exec
id: for-loops-when-you-know-how-many-times-2
# range(start, stop) -- stop is excluded
for i in range(1, 6):
    print(i, end=" ")      # end=" " prints on the same line
print()                     # new line

# range(start, stop, step)
for i in range(0, 20, 5):
    print(i, end=" ")
print()

# Counting backwards
for i in range(10, 0, -1):
    print(i, end=" ")
print("Liftoff!")
```

### Your turn

Write a for loop that prints the first 10 multiples of 7 (that is: 7, 14, 21, ..., 70). Think about what start, stop, and step values you need for `range()`.

**Pseudocode:**

```python exec
id: your-turn-2
# Your loop here
```

## Sigma Notation: Mathematics Meets Loops

Mathematicians have a compact notation for writing sums. Instead of writing $1 + 2 + 3 + 4 + 5$, they write:

$$\sum_{i=1}^{5} i$$

That capital sigma means "add up all the values of the expression, for each value of i from 1 to 5." The variable $i$ is called the *index* of summation.

Here is the beautiful thing: this is *exactly* what a loop with an accumulator does.

```python exec
id: sigma-notation-mathematics-meets-loops-1
# Computing the sum from i=1 to i=5 of i
total = 0
for i in range(1, 6):     # 1 through 5
    total = total + i
print("Sum:", total)       # should be 15
```

We can generalise this. $\sum_{i=1}^{n} i^2$ means "add up the squares of all integers from 1 to n":

```python exec
id: sigma-notation-mathematics-meets-loops-2
# Sum of squares from 1 to 10
n = 10
total = 0
for i in range(1, n + 1):
    total = total + i ** 2
print("Sum of squares from 1 to " + str(n) + ":", total)
```

There is also a product notation using the capital pi: $\prod_{i=1}^{n} i$ means "multiply all the integers from 1 to n." This is exactly the factorial function! $5! = 1 \times 2 \times 3 \times 4 \times 5 = 120.$

```python exec
id: sigma-notation-mathematics-meets-loops-3
# Computing 5! (factorial of 5) using the product pattern
n = 5
product = 1               # start at 1 for multiplication, not 0
for i in range(1, n + 1):
    product = product * i
print(str(n) + "! =", product)
```

Notice the key difference between sum and product accumulators: the sum starts at 0 (the identity element for addition) while the product starts at 1 (the identity element for multiplication).

### Your turn

Compute the following using loops. Write pseudocode first for each one.

1. $\sum_{i=1}^{100} i$ (the sum of the first 100 natural numbers -- there is a famous story about the young Gauss solving this instantly)

2. $\sum_{i=1}^{10} \frac{1}{i}$ (the first 10 terms of the harmonic series)

3. $10!$ (10 factorial)

```python exec
id: your-turn-3
# Pseudocode:
#
#

# 1. Sum of first 100 natural numbers
```

```python exec
id: your-turn-4
# 2. First 10 terms of the harmonic series
# (Hint: be careful about integer vs float division)
```

```python exec
id: your-turn-5
# 3. 10 factorial
```

## Nested Loops

Loops can contain other loops. The inner loop completes all its iterations for each single iteration of the outer loop:

```python exec
id: nested-loops-1
# A multiplication table (small version)
for row in range(1, 4):
    for col in range(1, 4):
        result = row * col
        print(str(result).rjust(4), end="")
    print()   # new line after each row
```

### Your turn

Modify the code above to produce a full 10x10 multiplication table. Then think about how many total multiplications it computes. If the outer loop runs n times and the inner loop runs n times, the total number of operations is n x n, or $n^2$. This idea -- counting how many operations an algorithm performs -- will be very important when we study search and sort algorithms.

```python exec
id: your-turn-6
# Your 10x10 multiplication table
```

## Building Up Gradually: Counting with Conditions

We can combine loops with conditionals to count or accumulate selectively. For instance, let's count how many numbers between 1 and 100 are divisible by both 3 and 7:

```python exec
id: building-up-gradually-counting-with-conditions-1
count = 0
for i in range(1, 101):
    if i % 3 == 0 and i % 7 == 0:
        count = count + 1
        print(i, end=" ")
print()
print("Total:", count)
```

### Your turn

Write a program that finds and prints all numbers between 1 and 50 that are *either* perfect squares (1, 4, 9, 16, ...) *or* perfect cubes (1, 8, 27, ...). One approach: for each number, check whether its square root (or cube root) is a whole number.

**Pseudocode:**

```python exec
id: your-turn-7
# Your program here
```

## Reflection

Today we covered `while` loops, `for` loops with `range()`, the accumulator pattern for both sums and products, nested loops, and loops combined with conditionals.

The big insight is the connection between loops and mathematical notation. When a mathematician writes $\sum$ or $\prod$, they are describing a loop. When a programmer writes a `for` loop with an accumulator, they are computing a sum or product. Same idea, different notation.

We now have all three fundamental control structures: sequential execution, selection (if/elif/else), and iteration (while, for). Every program ever written is built from these three building blocks.

What patterns are you starting to see? What questions do you have?
