---
title: "Experiments with variables: naming things"
year: "2026-2027"
version: 2026.11.16.1
---

# Experiments with variables: naming things

A variable is a name that points at a value. Each question here is small. Run the cell, change one thing, and look at what comes back. An error counts as an answer, because every error message says something true about how Python reads our code. Keep a note of each error name you meet, because the last section asks about them.

## 1. Making a variable

**1.1** Run this. What does each line print?

```python exec
id: making-a-variable-1
score = 10
print(score)
print(score + 5)
```

**1.2** Change `10` to `99` and run the cell again. Which lines of output changed, and which did not?

```python exec
id: making-a-variable-2
# your code here
```

**1.3** Python runs the lines from the top down. Run this, and read the error from the bottom up. What does the error tell you about the order of the lines?

```python exec
id: making-a-variable-3
print(score)
score = 10
```

**1.4** Run this. Which side of the `=` does Python work out first?

```python exec
id: making-a-variable-4
total = 3 + 4 * 2
print(total)
```

**Worth knowing.** The `=` sign does not claim that two things are equal. It means "attach this name to this value". Python works out the right-hand side first, and then attaches the name on the left.

**1.5** Write the line the other way round and run it. What does the error message suggest?

```python exec
id: making-a-variable-5
score = 10
7 = score
```

**1.6** Make three variables that hold your first name, your age and your favourite number. Print all three on separate lines.

```python exec
id: making-a-variable-6
# your code here
```

```solution
for: making-a-variable-6
title: one way to do it
first_name = "Sam"
age = 17
favourite_number = 7
print(first_name)
print(age)
print(favourite_number)
```

**1.7** Print two of your variables in one `print`, with a comma between them. Then add a third. What does Python put between the values?

```python exec
id: making-a-variable-7
# your code here
```

```solution
for: making-a-variable-7
title: one way to do it
first_name = "Sam"
age = 17
favourite_number = 7
print(first_name, age)
print(first_name, age, favourite_number)
---
`print` puts a single space between the values it is given.
```

## 2. Changing what a name points at

**2.1** Predict what this prints, and then run it.

```python exec
id: changing-what-a-name-points-at-1
x = 5
x = 8
print(x)
```

**2.2** Predict `x` and `y` before you run this. Then explain why `y` kept its value.

```python exec
id: changing-what-a-name-points-at-2
x = 5
y = x
x = 8
print(x, y)
```

**2.3** Which value of `count` does the right-hand side use on each line: the old one or the new one?

```python exec
id: changing-what-a-name-points-at-3
count = 0
count = count + 1
count = count + 1
print(count)
```

**2.4** A variable keeps the value that Python worked out at the time. Predict what `total` holds at the end, and then run it.

```python exec
id: changing-what-a-name-points-at-4
a = 2
b = 3
total = a + b
a = 10
print(total)
```

What would you add to the program so that `total` matches the new `a`?

```solution
for: changing-what-a-name-points-at-4
title: one way to do it
a = 2
b = 3
total = a + b
a = 10
total = a + b
print(total)
---
A variable holds the value Python worked out at the time, and not the formula. We have to run `total = a + b` again after `a` changes.
```

**2.5** Run this. Does changing `a` change `b`?

```python exec
id: changing-what-a-name-points-at-5
a = b = 4
print(a, b)
a = 5
print(a, b)
```

**2.6** Run each of these lines in a cell, starting from `x = 10`. Each one is a short way of writing a longer line. Write out the longer line for each.

```python exec
id: changing-what-a-name-points-at-6
x = 10
x += 5
print(x)
```

Try `x -= 5`, `x *= 5`, `x /= 4`, `x //= 4`, `x %= 4` and `x **= 2` as well.

**2.7** Swap the values of `a` and `b` so that `a` holds 2 and `b` holds 1. You will need a third variable.

```python exec
id: changing-what-a-name-points-at-7
a = 1
b = 2
# swap them here
print(a, b)
```

```solution
for: changing-what-a-name-points-at-7
title: one way to do it
a = 1
b = 2
temporary = a
a = b
b = temporary
print(a, b)
```

**2.8** Try the swap without a third variable. Write `a = b` and then `b = a`, and look at what each variable holds afterwards. Why does it fail?

```python exec
id: changing-what-a-name-points-at-8
a = 1
b = 2
# your code here
```

**2.9** Trace this by hand, one line at a time, and write down `a`, `b` and `c` after each line. Then run it and compare.

```python exec
id: changing-what-a-name-points-at-9
a = 1
b = 2
c = a + b
a = c
b = a + c
c = b - a
print(a, b, c)
```

```solution
for: changing-what-a-name-points-at-9
title: one way to do it
a = 1
b = 2
c = a + b
print(a, b, c)
a = c
print(a, b, c)
b = a + c
print(a, b, c)
c = b - a
print(a, b, c)
---
The last line prints `3 6 3`.
```

## 3. Choosing names

**3.1** Remove the `#` from one line at a time and run the cell. Keep a list of which names work and which fail.

```python exec
id: choosing-names-1
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

**3.2** Run this and read the error. What does it tell you about capital letters in names?

```python exec
id: choosing-names-2
Name = "Sam"
print(name)
```

**3.3** Remove the `#` from one line at a time. Which of these work as names?

```python exec
id: choosing-names-3
# class = 5
# if = 5
# True = 5
# else = 5
# in = 5
# score = 5
```

**Worth knowing.** A name may use letters, digits and underscores, and it may not start with a digit. A capital letter makes a different name from the lower-case one. Python also keeps some words for itself, such as `if`, `else`, `class` and `True`, and it will not let us use them as names.

**3.4** These names work, but they do not say much. Rename the variables so that the program says what it works out.

```python exec
id: choosing-names-4
a = 40
b = 12
c = a * b
print(c)
```

```solution
for: choosing-names-4
title: one way to do it
hours = 40
rate = 12
pay = hours * rate
print(pay)
```

**3.5** Read these two programs. Which one is easier to check for a mistake? Why?

```python exec
id: choosing-names-5
x = 3
y = 4
z = x * y / 2
print(z)
```

```python exec
id: choosing-names-6
base = 3
height = 4
area = base * height / 2
print(area)
```

## 4. Names meeting values

**4.1** Make `first = "Ada"` and `last = "Lovelace"`. Then make a third variable `full` that holds both names with a space between them, and print it.

```python exec
id: names-meeting-values-1
# your code here
```

```solution
for: names-meeting-values-1
title: one way to do it
first = "Ada"
last = "Lovelace"
full = first + " " + last
print(full)
```

**4.2** Make a typo on purpose in a variable name when you print it. What error do you get, and which line does it point at?

```python exec
id: names-meeting-values-2
colour = "green"
print(colur)
```

**4.3** Run this and read the error. What does `del` do to a variable?

```python exec
id: names-meeting-values-3
temporary = 5
print(temporary)
del temporary
print(temporary)
```

**4.4** Predict the balance after one year, and then run it. Then copy the last two lines of the program and paste them below to find the balance after two years.

```python exec
id: names-meeting-values-4
balance = 100
rate = 0.05
interest = balance * rate
balance = balance + interest
print(balance)
```

How many times would you need to copy those lines to model ten years?

```solution
for: names-meeting-values-4
title: one way to do it
balance = 100
rate = 0.05
interest = balance * rate
balance = balance + interest
interest = balance * rate
balance = balance + interest
print(balance)
---
After two years the balance is `110.25`. Ten years would need ten copies of the pair of lines, and a loop is the tool that saves us that copying.
```

## 5. Puzzles

**5.1** Rotate three values. After the program runs, `a` should hold 2, `b` should hold 3 and `c` should hold 1.

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

**5.2** Swap `a` and `b` again, but this time use only `+` and `-` and no third variable. Hint: think about what `a + b` holds.

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
After the first line `a` holds the sum. Taking `b` away from the sum leaves the old `a`, which goes into `b`. Taking the new `b` away from the sum leaves the old `b`, which goes into `a`.
```

**5.3** Trace this by hand before you run it.

```python exec
id: puzzles-3
x = 2
y = x * x
x = y + x
y = x - y
print(x, y)
```

**5.4** Predict the output, and then run it.

```python exec
id: puzzles-4
a = 3
b = a
a = a + 1
b = b + a
print(a, b)
```

**5.5** Write five lines of your own that end with a `print` of three variables. Give them to the person next to you and ask for a prediction.

```python exec
id: puzzles-5
# your code here
```

## 6. Looking back

**6.1** Which error names did you meet on this page? Write one sentence for each that says what caused it.

**6.2** Which experiment surprised you most, and what did you change to find out more?
