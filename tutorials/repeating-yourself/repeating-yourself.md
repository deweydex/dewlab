---
title: "Repeating steps with loops"
year: "2026-2027"
version: 2026.09.22.1
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

# Repeating steps with loops

Our programs can now run lines in order, and make decisions. One thing
is still missing: repetition. How would we add up 100 numbers, check
every item in a list, or convert a whole batch of temperatures? Without
a way to repeat, we would have to write the same code again and again.

On this page, we make the computer repeat things for us. We also find
that mathematical notation has had the same idea for centuries.

## While Loops: Repeat Until Done

A *while loop* runs its body again and again, for as long as a condition
stays True. What do you think this one prints?

```python exec
id: while-loops-repeat-until-done-1
# Count from 1 to 5
count = 1

while count <= 5:
    print(count)
    count = count + 1

print("Done!")
```

A while loop needs three things to work:

1. a starting state: `count = 1`
2. a condition that Python checks before each pass through the loop:
   `count <= 5`
3. an update inside the body that, in the end, makes the condition
   False: `count = count + 1`

What happens if we forget the third part? The condition never becomes
False, so the loop runs forever. This is a very common mistake, and it
is worth seeing once. While a cell is running, its **Run** button
changes to **Stop**. Press it to stop the loop. (If you do not see a
Stop button, reloading the page stops the loop too.)

### Your turn

Before you run the next cell, trace it by hand:

1. For each pass through the loop, write down the values of `total` and
   `n` in the comments at the bottom of the cell.
2. Predict what the cell prints at the end.
3. Run it to check.

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

Which sum did that program work out? It adds 1 + 2 + 3 + 4. The program
starts a total at zero, then adds to it again and again. This is the
*accumulator pattern*, and it is one of the most common shapes in
programming.

## For Loops: When You Know How Many Times

When we know in advance how many times to repeat, a *for loop* is
simpler. A for loop runs its body once for each item in a sequence. The
`range()` function makes a sequence of numbers for it:

```python exec
id: for-loops-when-you-know-how-many-times-1
# Count from 0 to 4
for i in range(5):
    print(i)
```

Did you expect it to start at 0? `range(5)` gives the numbers 0, 1, 2, 3
and 4: five numbers, starting from 0. This might seem strange. Starting
from 0 turns out to be very useful in programming, and we will see why
when we work with lists in
[Lists: keeping many values in order](tutorial:lists-and-sequences).

We can also give `range()` a start and a step:

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

| Call | Numbers it gives |
|---|---|
| `range(stop)` | from 0 up to, but not including, `stop` |
| `range(start, stop)` | from `start` up to, but not including, `stop` |
| `range(start, stop, step)` | from `start`, jumping by `step` each time, stopping before `stop` |

### Your turn

Can you write a for loop that prints the first 10 multiples of 7? (That
is 7, 14, 21, and so on, up to 70.)

1. Decide what start, stop and step values `range()` needs.
2. Write your plan as pseudocode comments in the cell below.
3. Write the loop, and run it.

**Pseudocode first, then the code:**

```python exec
id: your-turn-2
# Your loop here
```

## Sigma Notation: Mathematics Meets Loops

Mathematicians have a short way to write sums. Instead of
$1 + 2 + 3 + 4 + 5$, they write:

$$\sum_{i=1}^{5} i$$

The large symbol is the capital Greek letter sigma. It means "add up the
expression, for each value of $i$ from 1 to 5." The variable $i$ is
called the *index* of the sum.

Does that sound like something we have already written? It is exactly
what a loop with an accumulator does.

```python exec
id: sigma-notation-mathematics-meets-loops-1
# Computing the sum from i=1 to i=5 of i
total = 0
for i in range(1, 6):     # 1 through 5
    total = total + i
print("Sum:", total)       # should be 15
```

The notation is not a new subject. It writes down the same five
decisions you already make when you write that loop:

| The decision | In $\sum_{i=1}^{5} i$ | In the loop |
|---|---|---|
| What the index is called | the $i$ under the sigma | the `i` in `for i in ...` |
| Where it starts | the $1$ in $i = 1$ | the `1` in `range(1, 6)` |
| Where it stops | the $5$ above the sigma | the `6` in `range(1, 6)` |
| What gets accumulated | the $i$ after the sigma | the `+ i` in `total = total + i` |
| What the total starts at | nothing — it is assumed | `total = 0`, written out |

Two of those rows need a closer look.

The stopping row is the one that trips people up. Sigma stops **at** 5,
and `range` stops **before** 6. So the two numbers differ by one, but
they describe the same five values. The number in `range` marks a
boundary, not an item. We will see the same idea again with slices, in
[Lists: keeping many values in order](tutorial:lists-and-sequences).

The last row is a real difference between the two. Sigma never writes
down that the total starts at zero: a sum of nothing is zero, and
mathematicians leave that unsaid. A loop has to say it out loud. That is
why `total = 0` sits above every accumulator you write.

We can make this more general. $\sum_{i=1}^{n} i^2$ means "add up the
squares of all the integers from 1 to n":

```python exec
id: sigma-notation-mathematics-meets-loops-2
# Sum of squares from 1 to 10
n = 10
total = 0
for i in range(1, n + 1):
    total = total + i ** 2
print("Sum of squares from 1 to " + str(n) + ":", total)
```

There is also a notation for products, using the capital Greek letter
pi: $\prod_{i=1}^{n} i$ means "multiply all the integers from 1 to n."
This is the factorial function, written with `!`:
$5! = 1 \times 2 \times 3 \times 4 \times 5 = 120.$

```python exec
id: sigma-notation-mathematics-meets-loops-3
# Computing 5! (factorial of 5) using the product pattern
n = 5
product = 1               # start at 1 for multiplication, not 0
for i in range(1, n + 1):
    product = product * i
print(str(n) + "! =", product)
```

Why does `product` start at 1 and not at 0? What would happen if it
started at 0?

A sum starts at 0, because adding 0 changes nothing. A product starts at
1, because multiplying by 1 changes nothing. In mathematics, 0 is called
the identity element for addition, and 1 is the identity element for
multiplication.

### Your turn

Can you work out each of these with a loop? For each one, write
pseudocode first, then the code.

1. $\sum_{i=1}^{100} i$, the sum of the first 100 natural numbers. (There
   is a famous story that the young Gauss worked this out in moments.)
2. $\sum_{i=1}^{10} \frac{1}{i}$, the first 10 terms of the *harmonic
   series*. The harmonic series is the sum
   $1 + \frac{1}{2} + \frac{1}{3} + \frac{1}{4} + \dots$
3. $10!$, which is 10 factorial.

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
# (Hint: 1 / i gives a float. What would 1 // i give instead?)
```

```python exec
id: your-turn-5
# 3. 10 factorial
```

## Nested Loops

A loop can contain another loop. These are called *nested loops*. For
each single pass of the outer loop, the inner loop runs all the way
through. What do you think this prints?

```python exec
id: nested-loops-1
# A multiplication table (small version)
for row in range(1, 4):
    for col in range(1, 4):
        result = row * col
        # rjust(4) pads each number to 4 characters wide, so the columns line up
        print(str(result).rjust(4), end="")
    print()   # new line after each row
```

### Your turn

1. Change the code above so that it prints a full 10 by 10
   multiplication table.
2. How many multiplications does your table work out?

If the outer loop runs n times, and the inner loop runs n times for each
of those, the total number of steps is n × n, or $n^2$. Counting how many
steps an algorithm takes will matter a lot when we study searching and
sorting, in [Searching a list: linear and binary search](tutorial:finding-things) and
[Sorting a list: bubble, insertion and selection sort](tutorial:putting-things-in-order).

```python exec
id: your-turn-6
# Your 10x10 multiplication table
```

## Building Up Gradually: Counting with Conditions

We can put an `if` inside a loop, so that we only count or add some of
the values. For example, how many numbers from 1 to 100 can be divided
by both 3 and 7? Can you guess before you run it?

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

Can you write a program that finds and prints every number from 1 to 50
that is *either* a perfect square (1, 4, 9, 16, …) *or* a perfect cube
(1, 8, 27, …)?

One way: for each number, check whether its square root, or its cube
root, is a whole number. `n ** 0.5` gives the square root of `n`, and
`n ** (1/3)` gives the cube root.

Be careful with that cube root, though. Python stores most fractions
only approximately, so `64 ** (1/3)` gives `3.9999999999999996`, not
`4`. Another way avoids the problem: loop over whole numbers `k`, and
check whether `k * k` or `k * k * k` equals your number.

**Pseudocode first, then the code:**

```python exec
id: your-turn-7
# Your program here
```

## Reflection

On this page, we met `while` loops, `for` loops with `range()`, the
accumulator pattern for both sums and products, nested loops, and loops
with an `if` inside them.

The big idea is the link between loops and mathematical notation. When
a mathematician writes $\sum$ or $\prod$, they are describing a loop.
When a programmer writes a `for` loop with an accumulator, they are
working out a sum or a product. It is the same idea, in two notations.

We now have all three basic control structures: sequential execution,
selection (`if`, `elif`, `else`), and *iteration*. Iteration is
repetition: `while` and `for`. Any program can be built from these three
building blocks.

What patterns are you starting to see? What questions do you have?

## Where to Read More

Khan Academy. *Sigma Notation for Sums.*
<https://www.youtube.com/watch?v=5jwXThH6fg4>. The mathematical side of the
accumulator pattern this page builds — the same $\sum$ notation, worked
through on paper.

Python Software Foundation. *The Python Tutorial — More Control Flow
Tools.* <https://docs.python.org/3/tutorial/controlflow.html>. The official
reference for `for`, `range()`, and the rest of Python's looping tools,
including a few this page does not have room for.
