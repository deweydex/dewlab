---
title: "Experiments with number patterns: dots in triangles, squares and pentagons"
year: "2026-2027"
version: 2026.11.23.2
---

# Experiments with number patterns: dots in triangles, squares and pentagons

Arrange dots in a triangle and you get 1, 3, 6, 10, 15 and so on. Arrange them in a square and you get 1, 4, 9, 16, 25. These are number sequences: lists of numbers that follow a rule. On this page you let Python grow the lists for you, and then you look at the lists and the pictures to find rules of your own.

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

## 2. Growing a triangle

Each new triangle is the one before it with one more row along the bottom. The fourth row has 4 dots, so the fourth triangle is the third triangle plus 4.

**2.1** This cell grows the list one triangle at a time. Run it, then read the line inside the loop aloud. What does `triangles[-1]` mean?

```python exec
id: growing-a-triangle-1
triangles = [1]
for row in range(2, 8):
    triangles.append(triangles[-1] + row)
print(triangles)
```

**2.2** Change the `8` to `11`. Then try `2`. What happens to the list?

**2.3** Put the loop inside a function, `triangle_list(k)`, which returns the first `k` triangular numbers.

```python exec
id: growing-a-triangle-2
def triangle_list(k):
    triangles = [1]
    # your loop here
    return triangles

print(triangle_list(10))
```

```solution
def triangle_list(k):
    triangles = [1]
    for row in range(2, k + 1):
        triangles.append(triangles[-1] + row)
    return triangles

print(triangle_list(10))
```

```inputs
triangle_list(1)
triangle_list(5)
triangle_list(10)
```

**2.4** Suppose you want only the 100th triangular number. With the list, you have to grow the 99 before it first. Is there a way to jump straight to the 100th? Keep the question in mind for the next section.

## 3. Two triangles make a rectangle

![On the left, a triangle of blue dots with rows of 1, 2, 3 and 4 dots, 10 dots in all. On the right, the same blue triangle with a second triangle of red rings turned upside down and fitted against it. Together they make a rectangle 4 rows tall and 5 dots wide, 20 dots in all.](two-triangles-make-a-rectangle.png)

**3.1** Look at the picture. Two copies of the fourth triangle fill a rectangle. How tall is it, and how wide? How many dots is that?

**3.2** Picture two copies of the fifth triangle fitted together in the same way. How tall and how wide is the rectangle now? Try the tenth triangle, and then the n-th triangle.

**3.3** If two triangles fill the rectangle, how many dots are in one triangle? Write your rule as a function `triangular(n)`, with no loop.

```python exec
id: two-triangles-make-a-rectangle-1
def triangular(n):
    # your rule here
    return 0

print(triangular(4))
print(triangular(100))
```

```solution
def triangular(n):
    return n * (n + 1) // 2

print(triangular(4))
print(triangular(100))
---
The rectangle is n tall and n + 1 wide, and one triangle is half of it. `//` divides and keeps a whole number. n × (n + 1) is always even, so nothing is lost.
```

**3.4** Check your rule against the list you grew. Does it agree for the first 50 triangles?

```python exec
id: two-triangles-make-a-rectangle-2
def triangle_list(k):
    triangles = [1]
    for row in range(2, k + 1):
        triangles.append(triangles[-1] + row)
    return triangles

# paste your triangular function here, then compare
```

## 4. Squares, two ways

A square number has a rule we already know: a square with n dots on each side has n × n dots.

**4.1** Write `square(n)`, which works out a square straight from `n`.

```python exec
id: squares-two-ways-1
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

**4.2** Now grow the squares instead. Draw a 4 by 4 square of dots, then add the dots that turn it into a 5 by 5 square. What shape do the new dots make, and how many are there? What do you add to get from 5 by 5 to 6 by 6?

**4.3** Write `square_list(k)`, which grows the squares the way `triangle_list` grows the triangles: each new square is the last one plus something. Then check that the two ways agree.

```python exec
id: squares-two-ways-2
def square_list(k):
    squares = [1]
    # your loop here
    return squares

print(square_list(10))
```

```solution
def square_list(k):
    squares = [1]
    for n in range(2, k + 1):
        squares.append(squares[-1] + (2 * n - 1))
    return squares

print(square_list(10))
print(square_list(20) == [n * n for n in range(1, 21)])
---
Each new square adds an L-shaped border of 2n − 1 dots: n along one side, n along the other, and one corner dot that both sides share.
```

**4.4** You now have two ways to make the same numbers. One works out any square on its own. The other builds each square from the one before it. When might you want each one?

## 5. A pentagon is three triangles

The pentagonal numbers begin 1, 5, 12, 22, 35. A pentagonal number can be drawn as a house: a square with a roof on top.

![The fourth pentagonal number drawn as a house of 22 dots. The bottom is a 4 by 4 square. Inside the square, blue dots fill the upper-left triangle, including the diagonal, and red rings fill the lower-right triangle. On top sits a roof of green squares with rows of 3, 2 and 1.](a-pentagon-of-three-triangles.png)

**5.1** Find three triangles in the picture. Which triangular number is each one?

**5.2** Draw the fifth pentagonal number as a house in the same way, with a 5 by 5 square. Which three triangles are in it now?

**5.3** Write `pentagonal(n)` using your `triangular` function. `pentagonal(4)` should give 22.

```python exec
id: a-pentagon-is-three-triangles-1
def triangular(n):
    return n * (n + 1) // 2

def pentagonal(n):
    # your code here
    return 0

print([pentagonal(n) for n in range(1, 8)])
```

```solution
def triangular(n):
    return n * (n + 1) // 2

def pentagonal(n):
    return triangular(n) + 2 * triangular(n - 1)

print([pentagonal(n) for n in range(1, 8)])
---
The square splits into one triangle of side n and one of side n − 1, and the roof is another triangle of side n − 1.
```

**5.4** Can you grow the pentagonal numbers as a list too, each one from the one before? Draw the fourth house, then the fifth, and look at which dots are new.

```python exec
id: a-pentagon-is-three-triangles-2
pentagons = [1]
# your loop here
print(pentagons)
```

## 6. Hexagons: questions to think about

The hexagonal numbers begin 1, 6, 15, 28, 45. This section has no answers to check. The questions are for drawing, talking over with someone, and testing in code.

**6.1** Draw the third or fourth hexagonal number with dots. A hexagon can be drawn in more than one way, so choose one you can count.

**6.2** How many triangles can you cut your hexagon into? Is there more than one answer?

**6.3** When two triangles share an edge, the dots along that edge can end up counted twice. Where does that happen in your drawing? How would you correct for it?

**6.4** Turn your idea into a function and test it on the list. Here is a helper that lists the gaps between neighbours, in case the gaps help you see something.

```python exec
id: hexagons-1
def differences(numbers):
    gaps = []
    for i in range(len(numbers) - 1):
        gaps.append(numbers[i + 1] - numbers[i])
    return gaps

hexagons = [1, 6, 15, 28, 45]
print(differences(hexagons))

def hexagonal(n):
    # your idea here
    return 0

print([hexagonal(n) for n in range(1, 6)])
```

## 7. Any number of sides

**7.1** Look back over triangles, squares, pentagons and hexagons. Is there a way to build a shape with any number of sides out of triangles? How does the number of triangles change as the number of sides goes up?

**7.2** If you write `polygonal(sides, n)`, what should it give when `sides` is 3? When it is 4? Does your idea give the right lists for those?

**7.3** What would a shape with 2 sides give? What about 1 side? Does your function give an answer anyway, and does the answer mean anything?

```python exec
id: any-number-of-sides-1
def polygonal(sides, n):
    # your idea here
    return 0

for sides in [3, 4, 5, 6]:
    print(sides, [polygonal(sides, n) for n in range(1, 7)])
```
