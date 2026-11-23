---
title: "Experiments with slopes: how steep is a curve?"
year: "2026-2027"
version: 2026.11.23.3
---

# Experiments with slopes: how steep is a curve?

The slope of a line says how steep it is. For every step we move to the right, the slope says how far the line goes up, or down when the slope is negative. On this page we write a function for the slope between two points. Then we hand other functions to it, and use it to measure how steep a curve is at a single point.

We measure slope with two points on the line. The change in height is called the rise, the change across is called the run, and the slope is the rise divided by the run.

$$\text{slope} = \frac{y_2 - y_1}{x_2 - x_1}$$

![A straight line through the points (1, 3) and (4, 9). Dashed lines mark a run of 3 across and a rise of 6 up, so the slope is 6 divided by 3, which is 2. The line crosses the y-axis at (0, 1).](slope_two_points.png)

There are questions on this page to answer in words as well as in code. The **+ Text** button between cells adds a text cell where you can write your answers.

## 1. Slope between two points

**1.1** In the picture, which numbers from the two points make the rise of 6? Which make the run of 3?

<!-- answer -->

**1.2** Write a function `slope(x1, y1, x2, y2)` that hands back the slope of the line through the points (x1, y1) and (x2, y2). For the points in the picture, `slope(1, 3, 4, 9)` should give 2.0.

```python exec
id: slope-between-two-points-1
def slope(x1, y1, x2, y2):
    # your code here
    return 0

print(slope(1, 3, 4, 9))
```

<details class="dl-hint"><summary>smaller steps</summary>

1. The rise in the picture is 9 − 3. Which two arguments hold the 9 and the 3?
2. The run is 4 − 1. Which two arguments hold those?
3. Store the rise and the run in two variables, and return one divided by the other.

</details>

```solution
def slope(x1, y1, x2, y2):
    rise = y2 - y1
    run = x2 - x1
    return rise / run

print(slope(1, 3, 4, 9))
```

**1.3** What do you expect if the two points are given the other way round? Try it.

```python exec
id: slope-between-two-points-2
print(slope(4, 9, 1, 3))
```

<!-- answer -->

**1.4** The points (2, 5) and (2, 8) sit one above the other. Run the cell and read the error. What does the line through those two points look like, and why can it not have a slope?

```python exec
id: slope-between-two-points-3
print(slope(2, 5, 2, 8))
```

<!-- answer -->

**1.5** Change `slope` so that it hands back `None` when the run is zero, instead of stopping with an error. `None` is Python's value for "nothing".

```python exec
id: slope-between-two-points-4
def slope(x1, y1, x2, y2):
    # your code here
    return (y2 - y1) / (x2 - x1)

print(slope(2, 5, 2, 8))
print(slope(1, 3, 4, 9))
```

```solution
def slope(x1, y1, x2, y2):
    if x2 == x1:
        return None
    return (y2 - y1) / (x2 - x1)

print(slope(2, 5, 2, 8))
print(slope(1, 3, 4, 9))
```

## 2. Where the line crosses the y-axis

The height where a line crosses the y-axis is called its y-intercept. In the picture, the line crosses at a height of 1.

**2.1** Start at the point (1, 3) and walk left along the line until you reach x = 0. How many steps do you take? The slope is 2, so how far down do you go on each step? Where do you end up? Try the same walk from (4, 9).

<!-- answer -->

**2.2** Write `y_intercept(x1, y1, x2, y2)`, which hands back the height where the line through two points crosses the y-axis. It can call your `slope` function. The points in the picture should give 1.0.

```python exec
id: where-the-line-crosses-1
def y_intercept(x1, y1, x2, y2):
    # your code here
    return 0

print(y_intercept(1, 3, 4, 9))
print(y_intercept(2, 1, 4, -3))
```

<details class="dl-hint"><summary>smaller steps</summary>

1. Find the slope first, with `slope(x1, y1, x2, y2)`, and store it as `m`.
2. Starting from (x1, y1), how many steps left is it to x = 0?
3. Each step left, the line drops by `m`. How far does it drop in all, and what height is left?

</details>

```solution
def slope(x1, y1, x2, y2):
    return (y2 - y1) / (x2 - x1)

def y_intercept(x1, y1, x2, y2):
    m = slope(x1, y1, x2, y2)
    return y1 - m * x1

print(y_intercept(1, 3, 4, 9))
print(y_intercept(2, 1, 4, -3))
---
Walking back x1 steps to the y-axis, the line drops m on each step, so it drops m × x1 in all.
```

**2.3** A line can be described by its slope and its y-intercept, as in `y = 2.0x + 1.0`. Write `describe_line(x1, y1, x2, y2)`, which hands back a description like that as a string. What does yours give for the points (2, 1) and (4, −3)? Can you make it say `- 3.0` rather than `+ -3.0`?

```python exec
id: where-the-line-crosses-2
def describe_line(x1, y1, x2, y2):
    # your code here
    return ""

print(describe_line(1, 3, 4, 9))
print(describe_line(2, 1, 4, -3))
```

<details class="dl-hint"><summary>smaller steps</summary>

1. Find the slope and the y-intercept with your two functions, and store them.
2. Build the string with an f-string, such as `f"y = {m}x + {b}"`.
3. Add an `if` for a negative intercept. In that case, which sign do you write, and which number?

</details>

```solution
def describe_line(x1, y1, x2, y2):
    m = (y2 - y1) / (x2 - x1)
    b = y1 - m * x1
    if b < 0:
        return f"y = {m}x - {-b}"
    return f"y = {m}x + {b}"

print(describe_line(1, 3, 4, 9))
print(describe_line(2, 1, 4, -3))
```

## 3. A function inside a function

So far every argument has been a number. In Python a function is a value too, so we can hand one function to another as an argument. Here `f` is a function, and `apply_twice` takes a function and a number.

```python exec
id: a-function-inside-a-function-1
def f(x):
    return x ** 2

def apply_twice(func, value):
    return func(func(value))

print(apply_twice(f, 3))
```

**3.1** Before you run the cell, what do you expect it to print? Then run it. Inside `apply_twice`, what does `func` stand for?

<!-- answer -->

**3.2** This cell hands over `f(3)` instead of `f`. Run it and read the error. What is the difference between `f` and `f(3)`?

```python exec
id: a-function-inside-a-function-2
print(apply_twice(f(3), 3))
```

<!-- answer -->

**3.3** Write a function `add_one(x)` and hand it to `apply_twice` in place of `f`. What do you expect, and what do you get?

```python exec
id: a-function-inside-a-function-3
# your code here
```

```solution
def apply_twice(func, value):
    return func(func(value))

def add_one(x):
    return x + 1

print(apply_twice(add_one, 3))
```

## 4. Slope between two points on a curve

The curve $y = x^2$ has no single slope, because its steepness changes as we move along it. We can still pick two points on the curve and measure the slope of the straight line that joins them.

![The curve y equals x squared, with three straight lines that all start from the point at x equals 1. The second points sit at x equals 3, 2 and 1.25, and the slopes are 4, 3 and 2.25. The closer the second point, the closer the line hugs the curve.](parabola_pairs.png)

**4.1** Write `slope_between(func, a, b)`, which hands back the slope of the line joining the points of the curve at x = a and at x = b. Using the function `f` from section 3, `slope_between(f, 1, 3)` should give 4.0, as in the picture.

```python exec
id: slope-on-a-curve-1
def slope_between(func, a, b):
    # your code here
    return 0

print(slope_between(f, 1, 3))
print(slope_between(f, 1, 2))
```

<details class="dl-hint"><summary>smaller steps</summary>

1. The first point has x = a. Its height is the curve's value at a. How do you write that with `func`?
2. Do the same for the second point.
3. The rise is the difference in heights and the run is `b - a`.

</details>

```solution
def f(x):
    return x ** 2

def slope_between(func, a, b):
    return (func(b) - func(a)) / (b - a)

print(slope_between(f, 1, 3))
print(slope_between(f, 1, 2))
```

**4.2** The cell below keeps the first point at x = 1 and moves the second point closer, from both sides. Run it. Which number are the slopes heading towards?

```python exec
id: slope-on-a-curve-2
for b in [2, 1.5, 1.1, 1.01, 1.001]:
    print(b, slope_between(f, 1, b))
print()
for b in [0, 0.5, 0.9, 0.99, 0.999]:
    print(b, slope_between(f, 1, b))
```

<!-- answer -->

When the second point is very close to the first, the line between them barely cuts the curve. Its slope tells us how steep the curve is at that one point, and we will call it the slope at a point.

## 5. The slope at a point

**5.1** Write `slope_at(func, a, h=0.0001)`, which hands back the slope between `a` and `a + h`. Writing `h=0.0001` gives `h` a default: if a call leaves `h` out, Python uses 0.0001.

```python exec
id: the-slope-at-a-point-1
def slope_at(func, a, h=0.0001):
    # your code here
    return 0

print(slope_at(f, 1))
```

```solution
def f(x):
    return x ** 2

def slope_at(func, a, h=0.0001):
    return (func(a + h) - func(a)) / h

print(slope_at(f, 1))
```

**5.2** The cell below prints the slope of $y = x^2$ at every whole number from −3 to 5. Run it and look at the list. What rule turns each x into its slope?

```python exec
id: the-slope-at-a-point-2
for x in range(-3, 6):
    print(x, round(slope_at(f, x), 2))
```

<!-- answer -->

<details class="dl-hint"><summary>smaller steps</summary>

1. Look only at x = 0, 1, 2 and 3. How does the slope change each time x goes up by 1?
2. What is the slope when x is 0? Where is that on the curve?
3. Compare each slope with its x. Is the slope bigger by the same amount each time, or bigger by the same multiple?
4. Do the negative values of x follow the same rule?

</details>

**5.3** Write your rule as a function `slope_rule(x)`, and check it against `slope_at` at x = 10 and x = −7.

```python exec
id: the-slope-at-a-point-3
def slope_rule(x):
    # your rule here
    return 0

for x in [10, -7]:
    print(x, round(slope_at(f, x), 2), slope_rule(x))
```

```solution
def f(x):
    return x ** 2

def slope_at(func, a, h=0.0001):
    return (func(a + h) - func(a)) / h

def slope_rule(x):
    return 2 * x

for x in [10, -7]:
    print(x, round(slope_at(f, x), 2), slope_rule(x))
```

## 6. Other curves: questions to think about

This section has no answers to check. The questions are for testing in code and talking over with someone.

**6.1** Make a list of slopes in the same way for $y = 3x^2$, $y = x^2 + x$ and $y = x^3$. Can you find a rule for each one? To try a new curve, change only the `return` line of `g`.

```python exec
id: other-curves-1
def g(x):
    return 3 * x ** 2

for x in range(-3, 6):
    print(x, round(slope_at(g, x), 2))
```

<!-- answer -->

**6.2** What happens to the slopes when a curve is multiplied by 3? What happens when $x$ is added to it? What is the slope of a straight line such as $y = 3x + 1$, everywhere along it?

<!-- answer -->

<details class="dl-hint"><summary>ways in</summary>

1. Put the slopes of $x^2$ and $3x^2$ side by side. How are the two lists related?
2. Do the same for $x^2$ and $x^2 + x$.
3. For $x^3$, compare each slope with the square of its x.

</details>

## 7. A curve that goes up and down

![The curve y equals x cubed minus 3x. Near x equals minus 2 a short red line shows the curve climbing steeply, with a slope of about 7.8. Near x equals 0 a short blue line shows it falling, with a slope of about minus 3.](cubic_two_places.png)

**7.1** Before computing anything, look at the picture. At which values of x should the slope be zero? Where should it be negative?

<!-- answer -->

**7.2** Check your answers with `slope_at`.

```python exec
id: a-curve-that-goes-up-and-down-1
def h(x):
    return x ** 3 - 3 * x

# your code here
```

**7.3** Can a curve have the same slope at two different points? Look for an example on this curve, or on $x^2$. Is there a curve whose slope is the same everywhere?

<!-- answer -->

## 8. A detour: when h gets too small

**8.1** The cell below finds the slope of $x^2$ at x = 1 with smaller and smaller values of `h`. The answer should stay close to 2. Where does it start to go wrong?

```python exec
id: when-h-gets-too-small-1
for small in [1e-4, 1e-8, 1e-12, 1e-15]:
    print(small, slope_at(f, 1, small))
```

<!-- answer -->

A computer stores a decimal with only about 16 significant digits. Subtracting two numbers that are almost equal throws most of those digits away, and dividing by a tiny `h` makes the leftover error large.
