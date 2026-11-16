---
title: "Experiments with numbers: operators and surprises"
year: "2026-2027"
version: 2026.11.16.1
---

# Experiments with numbers: operators and surprises

Python works as a calculator, and it has a few operators that a calculator lacks. Run each cell, change the numbers, and look for patterns. Some results will surprise you, and the surprises are the useful part. Each cell sets up everything it uses.

## 1. Two kinds of number

Python has two kinds of number. An `int` is a whole number, such as 7. A `float` has a decimal point, such as 7.0 or 3.5. The two often behave alike, and the differences show up at the edges.

**1.1** Predict the type of each value, and then run the cell.

```python exec
id: two-kinds-of-number-1
print(type(7))
print(type(7.0))
print(type(-3))
print(type(1e3))
print(7 == 7.0)
```

**1.2** Predict the type of each result. Which operator turns two whole numbers into a float?

```python exec
id: two-kinds-of-number-2
print(type(3 + 4))
print(type(3 + 4.0))
print(type(8 / 2))
print(type(8 // 2))
print(type(2 ** 3))
print(type(2 ** -1))
```

## 2. The operators

**2.1** Run this. Which results look familiar, and which operators are new to you?

```python exec
id: the-operators-1
print(7 + 2)
print(7 - 2)
print(7 * 2)
print(7 / 2)
print(7 // 2)
print(7 % 2)
print(7 ** 2)
```

**2.2** Print `n % 2` for each whole number `n` from 0 to 9, changing `n` each time. What pattern do the answers follow? Then try `n % 3`.

```python exec
id: the-operators-2
n = 0
print(n % 2)
```

**2.3** Predict `100 // 7` and `100 % 7`, and then check them. How would you work them out by hand?

```python exec
id: the-operators-3
# your code here
```

```solution
for: the-operators-3
title: one way to do it
print(100 // 7)
print(100 % 7)
```

**Worth knowing.** The operators `//` and `%` work as a pair. For whole numbers, `a // b` counts how many whole times `b` fits into `a`, and `a % b` gives what is left over. Together they give back the number we started with: `(a // b) * b + a % b` always equals `a`.

**2.4** Check the rule from the note above for three pairs of numbers of your own.

```python exec
id: the-operators-4
a = 100
b = 7
print((a // b) * b + a % b)
```

**2.5** Predict these four results, and then run the cell. Does `//` cut the decimal part off, or does it round down?

```python exec
id: the-operators-5
print(7 // 2)
print(-7 // 2)
print(7 // -2)
print(-7 // -2)
```

**2.6** Run each line, one at a time. Which of these fail, and how do the messages differ?

```python exec
id: the-operators-6
print(5 / 0)
# print(5 // 0)
# print(5 % 0)
# print(0 / 5)
# print(5 ** 0)
```

**2.7** Run this. What does `**` do when the power is zero, negative or a decimal?

```python exec
id: the-operators-7
print(2 ** 3)
print(2 ** 0)
print(2 ** -1)
print(9 ** 0.5)
print(10 ** 6)
```

**2.8** Run this. Can a whole number grow as large as we like? What about a float?

```python exec
id: the-operators-8
print(2 ** 100)
print(2 ** 1000)
print(2.0 ** 1000)
print(2.0 ** 1024)
```

## 3. Order of operations

**3.1** Predict each result before you run the cell. Then write down the order that Python follows.

```python exec
id: order-of-operations-1
print(2 + 3 * 4)
print((2 + 3) * 4)
print(2 + 3 ** 2)
print(-3 ** 2)
print((-3) ** 2)
print(2 ** 3 ** 2)
print(10 - 4 - 3)
print(100 / 10 / 5)
print(2 + 7 % 3)
```

**Worth knowing.** Python works out brackets first, then `**`, then `*`, `/`, `//` and `%` from left to right, and then `+` and `-` from left to right. Two cases catch people out. A run of `**` signs works from right to left, so `2 ** 3 ** 2` means `2 ** 9`. A minus sign in front of a number waits until after `**`, so `-3 ** 2` means `-(3 ** 2)`.

**3.2** Add brackets so that this prints `19`. Then find brackets that make it print `15`, and then `11`.

```python exec
id: order-of-operations-2
print(2 + 3 * 4 - 1)
```

```solution
for: order-of-operations-2
title: one way to do it
print((2 + 3) * 4 - 1)
print((2 + 3) * (4 - 1))
print(2 + 3 * (4 - 1))
```

**3.3** This program should print the average of 4, 9 and 14, which is 9. Fix it.

```python exec
id: order-of-operations-3
print(4 + 9 + 14 / 3)
```

```solution
for: order-of-operations-3
title: one way to do it
print((4 + 9 + 14) / 3)
```

**3.4** Run each line. Does Python mind the spaces? What do two minus signs in a row do?

```python exec
id: order-of-operations-4
print(2+3*4)
print(2 +3* 4)
print(2 - -3)
print(2--3)
```

**3.5** Run this and read the error. In maths, `2(3)` means 2 times 3. What does Python think the brackets mean?

```python exec
id: order-of-operations-5
print(2(3))
```

```solution
for: order-of-operations-5
title: one way to do it
print(2 * 3)
---
Brackets straight after a value mean a call, so Python tried to call the number 2 as if it were a function. Multiplication always needs the `*`.
```

## 4. Decimal numbers

**4.1** Run this. Which results would your calculator disagree with?

```python exec
id: decimal-numbers-1
print(0.1 + 0.2)
print(0.1 + 0.2 == 0.3)
print(0.5 + 0.25 == 0.75)
print(1.1 * 3)
```

**Worth knowing.** A computer stores a float in binary. One third has no exact decimal form, and in the same way one tenth has no exact binary form, so Python stores the nearest value it can. Numbers built from halves and quarters, such as 0.5 and 0.25, are stored exactly.

**4.2** Run this. Which tests give the answer we want for `0.1 + 0.2`?

```python exec
id: decimal-numbers-2
print(0.1 + 0.2 == 0.3)
print(round(0.1 + 0.2, 2) == 0.3)
print(abs((0.1 + 0.2) - 0.3) < 0.000001)
```

**4.3** Run this. Look closely at the numbers that end in `.5`. What pattern does `round` follow?

```python exec
id: decimal-numbers-3
print(round(3.14159, 2))
print(round(3.14159))
print(round(0.5))
print(round(1.5))
print(round(2.5))
print(round(3.5))
```

**4.4** Compare `int` with `round`. Does `int` round, or does it cut the decimal part off?

```python exec
id: decimal-numbers-4
print(int(3.9))
print(int(-3.9))
print(round(3.9))
```

**4.5** Inside an f-string, the text after a colon sets the format. Change the `2` to `0`, `1` and `5`.

```python exec
id: decimal-numbers-5
price = 3.14159
print(f"{price:.2f}")
```

**4.6** Predict what each line prints, and then run the cell.

```python exec
id: decimal-numbers-6
print(f"{1234567:,}")
print(f"{7:03}")
print(f"{0.256:.1%}")
```

**4.7** Run this. What do `abs`, `min`, `max` and `divmod` do?

```python exec
id: decimal-numbers-7
print(abs(-5))
print(min(3, 1, 2))
print(max(3, 1, 2))
print(divmod(17, 5))
```

## 5. Puzzles with remainders

**5.1** A video lasts 1234 seconds. Print how many whole minutes that is, and how many seconds are left over.

```python exec
id: puzzles-with-remainders-1
seconds = 1234
# your code here
```

```solution
for: puzzles-with-remainders-1
title: one way to do it
seconds = 1234
print(seconds // 60)
print(seconds % 60)
```

**5.2** The number `n` holds four digits. Print each of its digits on a line of its own, using only `//` and `%`. Change `n` to test it.

```python exec
id: puzzles-with-remainders-2
n = 4729
# your code here
```

```solution
for: puzzles-with-remainders-2
title: one way to do it
n = 4729
print(n // 1000)
print(n // 100 % 10)
print(n // 10 % 10)
print(n % 10)
```

**5.3** Write an expression that prints `True` when `n` is even and `False` when it is odd. Test it with 7, 10, 0 and -3.

```python exec
id: puzzles-with-remainders-3
n = 7
# your code here
```

```solution
for: puzzles-with-remainders-3
title: one way to do it
n = 7
print(n % 2 == 0)
```

**5.4** It is 22:00 now. Print the hour after 5 hours, after 30 hours and after 100 hours.

```python exec
id: puzzles-with-remainders-4
hour = 22
# your code here
```

```solution
for: puzzles-with-remainders-4
title: one way to do it
hour = 22
print((hour + 5) % 24)
print((hour + 30) % 24)
print((hour + 100) % 24)
```

**5.5** An item costs 237 cents. Print how many euros and how many cents that is.

```python exec
id: puzzles-with-remainders-5
cents = 237
# your code here
```

```solution
for: puzzles-with-remainders-5
title: one way to do it
cents = 237
print(cents // 100, "euros and", cents % 100, "cents")
```

**5.6** Reverse a two-digit number without using strings. If `n` holds 47, print 74.

```python exec
id: puzzles-with-remainders-6
n = 47
# your code here
```

```solution
for: puzzles-with-remainders-6
title: one way to do it
n = 47
print(n % 10 * 10 + n // 10)
```

**5.7** Print the sum of the digits of 4729, which is 4 + 7 + 2 + 9.

```python exec
id: puzzles-with-remainders-7
n = 4729
# your code here
```

```solution
for: puzzles-with-remainders-7
title: one way to do it
n = 4729
print(n // 1000 + n // 100 % 10 + n // 10 % 10 + n % 10)
```

**5.8** Eight slices fit in one pizza. Print how many pizzas a group must buy for any number of slices. Three slices need one pizza, and nine slices need two. Hint: `//` rounds down, so think about what you could add to `slices` first.

```python exec
id: puzzles-with-remainders-8
slices = 9
# your code here
```

```solution
for: puzzles-with-remainders-8
title: one way to do it
slices = 9
print((slices + 7) // 8)
---
Adding 7 before dividing pushes any leftover slices up to one more pizza. Exactly 8 slices still gives one pizza.
```

**5.9** Convert 0, 100 and -40 degrees Celsius to Fahrenheit with `c * 9 / 5 + 32`. What is special about the last answer?

```python exec
id: puzzles-with-remainders-9
c = 100
print(c * 9 / 5 + 32)
```

## 6. Looking back

**6.1** Which of `/`, `//`, `%` and `**` gave you the most surprising result? Describe the experiment that showed you how it behaves.

**6.2** Write down two situations where `%` would help in a program.
