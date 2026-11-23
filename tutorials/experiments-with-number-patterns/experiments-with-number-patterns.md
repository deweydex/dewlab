---
title: "Experiments with number patterns: dots in triangles, squares and pentagons"
year: "2026-2027"
version: 2026.11.23.1
---

# Experiments with number patterns: dots in triangles, squares and pentagons

Arrange dots in a triangle and you get 1, 3, 6, 10, 15 and so on. Arrange them in a square and you get 1, 4, 9, 16, 25. These are number sequences: lists of numbers that follow a rule. On this page you write small functions that follow the rule for you, collect the results in lists, and finish with the pentagons.

A function is a named piece of code. You give it some values, called arguments, and it hands back a result with `return`.

## 1. A first function

**1.1** Run this cell. Nothing prints. Why not?

```python exec
id: a-first-function-1
def double(n):
    return n * 2
```

**1.2** Now call it. Predict each line before you run it.

```python exec
id: a-first-function-2
def double(n):
    return n * 2

print(double(4))
print(double(10) + 1)
print(double(double(3)))
```

**1.3** Change `return` to `print` inside the function and run the cell again. What comes out, and where does `None` come from?

```python exec
id: a-first-function-3
def double(n):
    return n * 2

print(double(4))
```

## 2. Triangular numbers

The fourth triangular number is 1 + 2 + 3 + 4 = 10. Each row of the triangle has one more dot than the row above it.

**2.1** Write `triangular(n)`, which adds up the whole numbers from 1 to `n` and returns the total. `triangular(4)` should give 10.

```python exec
id: triangular-numbers-1
def triangular(n):
    total = 0
    # your loop here
    return total

print(triangular(4))
```

```solution
def triangular(n):
    total = 0
    for row in range(1, n + 1):
        total = total + row
    return total

print(triangular(4))
---
`range(1, n + 1)` stops one short of its second number, so the `+ 1` lets the last row in.
```

```inputs
triangular(1)
triangular(4)
triangular(10)
triangular(0)    # a triangle with no rows
```

**2.2** Try `triangular(0)`. Does the answer make sense for a triangle with no rows?

**2.3** Write `triangular_list(k)`, which returns a list of the first `k` triangular numbers. It can call `triangular` inside a loop and use `.append()`.

```python exec
id: triangular-numbers-2
def triangular(n):
    total = 0
    for row in range(1, n + 1):
        total = total + row
    return total

def triangular_list(k):
    numbers = []
    # your loop here
    return numbers

print(triangular_list(6))
```

```solution
def triangular(n):
    total = 0
    for row in range(1, n + 1):
        total = total + row
    return total

def triangular_list(k):
    numbers = []
    for n in range(1, k + 1):
        numbers.append(triangular(n))
    return numbers

print(triangular_list(6))
```

## 3. The gaps between neighbours

**3.1** Write `differences(numbers)`, which takes any list and returns the gaps between each number and the next. `differences([1, 3, 6, 10])` should give `[2, 3, 4]`.

```python exec
id: the-gaps-between-neighbours-1
def differences(numbers):
    gaps = []
    # your loop here
    return gaps

print(differences([1, 3, 6, 10]))
```

```solution
def differences(numbers):
    gaps = []
    for i in range(len(numbers) - 1):
        gaps.append(numbers[i + 1] - numbers[i])
    return gaps

print(differences([1, 3, 6, 10]))
```

```inputs
differences([1, 3, 6, 10])
differences([5])       # one number has no neighbour
differences([])        # an empty list
```

**3.2** Run `differences` on the first ten triangular numbers. Then run `differences` on that answer. What do you notice each time?

```python exec
id: the-gaps-between-neighbours-2
triangles = [1, 3, 6, 10, 15, 21, 28, 36, 45, 55]
# your code here
```

```solution
def differences(numbers):
    gaps = []
    for i in range(len(numbers) - 1):
        gaps.append(numbers[i + 1] - numbers[i])
    return gaps

triangles = [1, 3, 6, 10, 15, 21, 28, 36, 45, 55]
first_gaps = differences(triangles)
print(first_gaps)
print(differences(first_gaps))
```

## 4. Square numbers, two ways

**4.1** Write `square(n)` the quick way, with `n * n`, and print the first ten squares in a list.

```python exec
id: square-numbers-two-ways-1
def square(n):
    # your code here
    return 0

print([square(n) for n in range(1, 11)])
```

```solution
def square(n):
    return n * n

print([square(n) for n in range(1, 11)])
```

**4.2** Run `differences` on the squares. The gaps make a pattern of their own. What is it?

```python exec
id: square-numbers-two-ways-2
squares = [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
# your code here
```

```solution
def differences(numbers):
    gaps = []
    for i in range(len(numbers) - 1):
        gaps.append(numbers[i + 1] - numbers[i])
    return gaps

squares = [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
print(differences(squares))
```

**4.3** Write `square_by_adding(n)`, which builds a square by adding up only those gaps, with no multiplication. Check that it agrees with `square(n)` for the first 20 values.

```python exec
id: square-numbers-two-ways-3
def square_by_adding(n):
    total = 0
    # your loop here
    return total

print([square_by_adding(n) for n in range(1, 11)])
```

```solution
def square_by_adding(n):
    total = 0
    for k in range(1, n + 1):
        total = total + (2 * k - 1)
    return total

print([square_by_adding(n) for n in range(1, 11)])
print(all(square_by_adding(n) == n * n for n in range(1, 21)))
---
The gaps are the odd numbers, and the k-th odd number is 2k − 1.
```

## 5. Two triangles make a square

**5.1** Add two neighbouring triangular numbers, such as `triangular(4) + triangular(3)`. Try several pairs. What kind of number comes out every time?

```python exec
id: two-triangles-make-a-square-1
def triangular(n):
    total = 0
    for row in range(1, n + 1):
        total = total + row
    return total

print(triangular(4) + triangular(3))
# try more pairs here
```

**5.2** On paper, draw a 4 by 4 square of dots and cut it along a diagonal. One triangle keeps the diagonal and the other does not. How many dots are in each piece?

## 6. Pentagonal numbers

The pentagonal numbers begin 1, 5, 12, 22, 35.

**6.1** Run `differences` on these five numbers, and then on the result. The second set of gaps tells you how each step grows.

```python exec
id: pentagonal-numbers-1
pentagons = [1, 5, 12, 22, 35]
# your code here
```

```solution
def differences(numbers):
    gaps = []
    for i in range(len(numbers) - 1):
        gaps.append(numbers[i + 1] - numbers[i])
    return gaps

pentagons = [1, 5, 12, 22, 35]
print(differences(pentagons))
print(differences(differences(pentagons)))
```

**6.2** Using what you found, write `pentagonal(n)` with a loop, in the same style as `triangular(n)`. `pentagonal(5)` should give 35.

```python exec
id: pentagonal-numbers-2
def pentagonal(n):
    total = 0
    # your loop here
    return total

print([pentagonal(n) for n in range(1, 8)])
```

```solution
def pentagonal(n):
    total = 0
    for k in range(1, n + 1):
        total = total + (3 * k - 2)
    return total

print([pentagonal(n) for n in range(1, 8)])
---
The gaps are 1, 4, 7, 10, … They start at 1 and grow by 3, so the k-th gap is 3k − 2.
```

```inputs
pentagonal(1)
pentagonal(5)
pentagonal(10)
```

**6.3** A short formula also gives pentagonal numbers: `n * (3 * n - 1) // 2`. Does your loop agree with it for the first 20 values?

```python exec
id: pentagonal-numbers-3
# paste your pentagonal function here, then compare
```

```solution
def pentagonal(n):
    total = 0
    for k in range(1, n + 1):
        total = total + (3 * k - 2)
    return total

print(all(pentagonal(n) == n * (3 * n - 1) // 2 for n in range(1, 21)))
```

**6.4** Compare `pentagonal(n)` with `square(n) + triangular(n - 1)` for several values of `n`. What do you find? Can you see a square and a triangle inside a drawn pentagon?

```python exec
id: pentagonal-numbers-4
# your code here
```

```solution
def triangular(n):
    return sum(range(1, n + 1))

def square(n):
    return n * n

def pentagonal(n):
    return n * (3 * n - 1) // 2

for n in range(1, 8):
    print(n, pentagonal(n), square(n) + triangular(n - 1))
```

## 7. One function for every shape

**7.1** Look back at the second gaps. Triangles (3 sides) gave 1, squares (4 sides) gave 2, pentagons (5 sides) gave 3. How does the second gap relate to the number of sides?

**7.2** Write `polygonal(sides, n)` so that it gives triangular numbers when `sides` is 3, squares when it is 4 and pentagons when it is 5. What does it give for hexagons, with 6 sides?

```python exec
id: one-function-for-every-shape-1
def polygonal(sides, n):
    total = 0
    # your loop here
    return total

for sides in [3, 4, 5, 6]:
    print(sides, [polygonal(sides, n) for n in range(1, 7)])
```

```solution
def polygonal(sides, n):
    step = sides - 2
    total = 0
    for k in range(1, n + 1):
        total = total + 1 + step * (k - 1)
    return total

for sides in [3, 4, 5, 6]:
    print(sides, [polygonal(sides, n) for n in range(1, 7)])
---
Every gap list starts at 1 and grows by `sides - 2`.
```
