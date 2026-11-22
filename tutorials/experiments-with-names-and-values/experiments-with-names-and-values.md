---
title: "Experiments with names and values: what the = sign does"
year: "2026-2027"
version: 2026.11.16.1
---

# Experiments with names and values: what the = sign does

A variable is a name attached to a value. Run each cell, change one thing, and look at what comes back. An error counts as an answer, because the message tells us how Python read the line. Each cell sets up everything it uses, so you can run the cells in any order.

## 1. The parts of an assignment

A line such as `price = 4 * 3` is an assignment. An assignment has three parts: a name on the left, the `=` sign, and an expression on the right. Python works out the expression first. Then it attaches the name to the result, and from then on the name stands for that value.

**1.1** Run this. What value does `price` stand for after the first line?

```python exec
id: the-parts-of-an-assignment-1
price = 4 * 3
print(price)
```

**1.2** Find the three parts in each of the first four lines: the name, the `=` sign and the expression. Predict what each name holds, and then run the cell to check.

```python exec
id: the-parts-of-an-assignment-2
width = 7
height = width + 3
area = width * height
shape = "rectangle"
print(width, height, area, shape)
```

**1.3** Write an assignment for each set of parts, and print each name afterwards. The first has the name `minutes` and the expression `3 * 60`. The second has the name `greeting` and the text `"hello"`. The third has the name `half` and an expression that divides 9 by 2.

```python exec
id: the-parts-of-an-assignment-3
# your code here
```

```solution
for: the-parts-of-an-assignment-3
title: one way to do it
minutes = 3 * 60
greeting = "hello"
half = 9 / 2
print(minutes)
print(greeting)
print(half)
```

**1.4** Remove the `#` from one line at a time, run the cell, and put the `#` back. Which lines are assignments? For each line that fails, say which part is missing or in the wrong place.

```python exec
id: the-parts-of-an-assignment-4
# speed = 40
# speed 40
# = 40
# speed =
# 40 = speed
```

**1.5** Run this. Read the second line as if it were an equation in a maths class. Why would it be false as an equation? What does Python do with it instead?

```python exec
id: the-parts-of-an-assignment-5
count = 5
count = count + 1
print(count)
```

**Worth knowing.** The `=` sign in Python does not say that two things are equal. It is an instruction: work out the right side, and then attach the name on the left to the result. That is why `count = count + 1` makes sense to Python, even though it makes no sense as an equation.

**1.6** Python runs the lines from the top down. Run this, and read the error from the bottom up. What does the error tell you about the order of the two lines? Fix the program.

```python exec
id: the-parts-of-an-assignment-6
print(points)
points = 10
```

```solution
for: the-parts-of-an-assignment-6
title: one way to do it
points = 10
print(points)
```

## 2. A name is only a label

Python does not read the words we choose for names. To Python, `price`, `banana` and `x7` are labels and nothing more. Only the value attached to a label matters.

**2.1** Run this. Does Python object to any of these names? What does `seventeen` hold?

```python exec
id: a-name-is-only-a-label-1
banana = 15
print(banana + 1)
seventeen = 4
print(seventeen)
```

**2.2** This program works. Rename `age` to `shoe_size` on every line where it appears, and run it again. What changed in the output?

```python exec
id: a-name-is-only-a-label-2
age = 15
next_year = age + 1
print(next_year)
```

**2.3** Someone renamed the first line of a working program and forgot the second line. Run it and read the error. Why does Python not work out that `tall` and `height_cm` meant the same thing? Fix it in two different ways.

```python exec
id: a-name-is-only-a-label-3
tall = 170
height_m = height_cm / 100
print(height_m)
```

```solution
for: a-name-is-only-a-label-3
title: one way to do it
height_cm = 170
height_m = height_cm / 100
print(height_m)
---
The other fix renames the second line instead, so that it reads `height_m = tall / 100`. Either way, both lines must use the same name, because Python matches names letter by letter and knows nothing of what they mean.
```

**2.4** Quotes change everything. Without quotes, a word is a name, and Python looks up its value. With quotes, the word is text, and Python uses its letters as they are. Predict both lines, and then run the cell.

```python exec
id: a-name-is-only-a-label-4
city = "Dublin"
print(city)
print("city")
```

**2.5** Run this and read the error. What did Python try to do with the word `Galway`? Fix the line so that `town` holds the text.

```python exec
id: a-name-is-only-a-label-5
town = Galway
print(town)
```

```solution
for: a-name-is-only-a-label-5
title: one way to do it
town = "Galway"
print(town)
```

**2.6** Predict all three lines before you run this.

```python exec
id: a-name-is-only-a-label-6
colour = "blue"
blue = "red"
print(colour)
print(blue)
print("blue")
```

**2.7** Write a program in which `print(fruit)` prints `apple` and `print("fruit")` prints `fruit`.

```python exec
id: a-name-is-only-a-label-7
# your code here
```

```solution
for: a-name-is-only-a-label-7
title: one way to do it
fruit = "apple"
print(fruit)
print("fruit")
```

**2.8** Remove the `#` from one line at a time and run it. Keep a list of which names work and which fail.

```python exec
id: a-name-is-only-a-label-8
# age = 1
# age2 = 1
# 2age = 1
# my age = 1
# my_age = 1
# my-age = 1
# Age = 1
# _age = 1
# age! = 1
```

What rule separates the names that work from the names that fail?

**2.9** Run this and read the error. What does it tell you about capital letters in names?

```python exec
id: a-name-is-only-a-label-9
Pet = "cat"
print(pet)
```

**2.10** Remove the `#` from one line at a time. Which of these work as names?

```python exec
id: a-name-is-only-a-label-10
# class = 5
# if = 5
# True = 5
# else = 5
# score = 5
```

**Worth knowing.** A name may use letters, digits and underscores, and it may not start with a digit. A capital letter makes a different name from the lower-case one. Python keeps some words for itself, such as `if`, `else`, `class` and `True`, and it will not let us use them as names.

**2.11** These names work, but they say nothing about the program. Rename the variables so that a reader can tell what the program works out.

```python exec
id: a-name-is-only-a-label-11
a = 40
b = 12
c = a * b
print(c)
```

```solution
for: a-name-is-only-a-label-11
title: one way to do it
hours = 40
rate = 12
pay = hours * rate
print(pay)
```

## 3. Changing what a name holds

**3.1** Predict what this prints, and then run it.

```python exec
id: changing-what-a-name-holds-1
x = 5
x = 8
print(x)
```

**3.2** Predict `x` and `y` before you run this. Then explain why `y` kept its value.

```python exec
id: changing-what-a-name-holds-2
x = 5
y = x
x = 8
print(x, y)
```

**3.3** A name holds the value that Python worked out at the time, and not the expression. Predict what `total` holds at the end, and then run it.

```python exec
id: changing-what-a-name-holds-3
a = 2
b = 3
total = a + b
a = 10
print(total)
```

What would you add so that `total` matches the new `a`?

```solution
for: changing-what-a-name-holds-3
title: one way to do it
a = 2
b = 3
total = a + b
a = 10
total = a + b
print(total)
---
The name `total` holds the number 5 and not the expression `a + b`, so we have to run the expression again after `a` changes.
```

**3.4** Each of these lines is a short way of writing a longer assignment. Run the cell. Then write out the longer form of `x += 5`.

```python exec
id: changing-what-a-name-holds-4
x = 10
x += 5
print(x)
x *= 2
print(x)
x -= 1
print(x)
```

Try `x //= 4`, `x %= 4` and `x **= 2` as well.

**3.5** Swap the values of `a` and `b` so that `a` holds 2 and `b` holds 1. You will need a third name.

```python exec
id: changing-what-a-name-holds-5
a = 1
b = 2
# swap them here
print(a, b)
```

```solution
for: changing-what-a-name-holds-5
title: one way to do it
a = 1
b = 2
temporary = a
a = b
b = temporary
print(a, b)
```

**3.6** Run this attempt at a swap. What does each name hold afterwards, and why did the first value disappear?

```python exec
id: changing-what-a-name-holds-6
a = 1
b = 2
a = b
b = a
print(a, b)
```

**3.7** Trace this by hand, one line at a time, and write down `a`, `b` and `c` after each line. Then run it and compare.

```python exec
id: changing-what-a-name-holds-7
a = 1
b = 2
c = a + b
a = c
b = a + c
c = b - a
print(a, b, c)
```

## 4. Puzzles

**4.1** Rotate three values. After the program runs, `a` should hold 2, `b` should hold 3 and `c` should hold 1.

```python exec
id: puzzles-1
a = 1
b = 2
c = 3
# rotate them here
print(a, b, c)
```

```solution
for: puzzles-1
title: one way to do it
a = 1
b = 2
c = 3
temporary = a
a = b
b = c
c = temporary
print(a, b, c)
```

**4.2** Swap `a` and `b` again, but this time use only `+` and `-` and no third name. Hint: think about what `a + b` holds.

```python exec
id: puzzles-2
a = 3
b = 8
# swap them here
print(a, b)
```

```solution
for: puzzles-2
title: one way to do it
a = 3
b = 8
a = a + b
b = a - b
a = a - b
print(a, b)
---
After the first line `a` holds the sum. The sum minus `b` is the old `a`, which goes into `b`. The sum minus the new `b` is the old `b`, which goes into `a`.
```

**4.3** Predict the output, and then run it.

```python exec
id: puzzles-3
a = 3
b = a
a = a + 1
b = b + a
print(a, b)
```

**4.4** A bank pays 5 percent a year. Predict the balance after one year, and then run it. Copy the last two lines and paste them below to find the balance after two years.

```python exec
id: puzzles-4
balance = 100
rate = 0.05
interest = balance * rate
balance = balance + interest
print(balance)
```

How many copies would ten years need?

```solution
for: puzzles-4
title: one way to do it
balance = 100
rate = 0.05
interest = balance * rate
balance = balance + interest
interest = balance * rate
balance = balance + interest
print(balance)
---
After two years the balance is 110.25. Ten years would need ten copies of the pair of lines, and a loop is the tool that saves us the copying.
```

**4.5** Write five lines of your own that end with a `print` of three names. Give them to the person next to you and ask for a prediction.

```python exec
id: puzzles-5
# your code here
```

## 5. Looking back

**5.1** Which error names did you meet on this page? Write one sentence for each that says what caused it.

**5.2** Explain to someone who has never programmed why `print(city)` and `print("city")` print different things.
