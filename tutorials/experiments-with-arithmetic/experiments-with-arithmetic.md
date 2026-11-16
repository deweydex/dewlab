---
title: "Experiments with arithmetic: numbers in, numbers out"
year: "2026-2027"
version: 2026.11.16.1
---

# Experiments with arithmetic: numbers in, numbers out

Python can work as a calculator, and it has a few operators that a calculator lacks. Run each cell, change the numbers, and look for patterns. Some of the results will surprise you, and the surprises are the useful part.

## 1. The operators

**1.1** Run this. Which results look familiar, and which operators are new to you?

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

**1.2** Change `7` and `2` to `8` and `2`. Which lines now look different from before? Compare `/` with `//`.

```python exec
id: the-operators-2
print(8 / 2)
print(8 // 2)
print(8 % 2)
print(type(8 / 2))
print(type(8 // 2))
```

**1.3** Predict these four results, and then run the cell. Does `//` cut off the decimal part, or does it round down?

```python exec
id: the-operators-3
print(7 // 2)
print(-7 // 2)
print(7 // -2)
print(-7 // -2)
```

**1.4** Run this. What does the sign of the second number do to the answer?

```python exec
id: the-operators-4
print(7 % 2)
print(-7 % 2)
print(7 % -2)
print(8 % 2)
print(2 % 7)
print(0 % 5)
```

**1.5** Predict `100 % 7`, and then check it. How could you work it out by hand?

**1.6** Print `x % 2` for each whole number from 0 to 9. Write the lines out one by one. What pattern do the answers follow?

```python exec
id: the-operators-5
x = 0
print(x % 2)
```

**1.7** Now print `x % 3` for each whole number from 0 to 8. How does the pattern differ from the one for `% 2`?

```python exec
id: the-operators-6
# your code here
```

**1.8** Run each line, one at a time. Which of these fail, and how do the messages differ?

```python exec
id: the-operators-7
print(5 / 0)
# print(5 // 0)
# print(5 % 0)
# print(0 / 5)
# print(0 ** 0)
# print(5 ** 0)
```

**1.9** Run this. What does `**` do when the power is negative, zero or a decimal?

```python exec
id: the-operators-8
print(2 ** 3)
print(2 ** 0)
print(2 ** -1)
print(2 ** 0.5)
print(4 ** 0.5)
print(10 ** 6)
```

**1.10** Run this. Is there a limit to how large a whole number can grow? What about a decimal number?

```python exec
id: the-operators-9
print(2 ** 100)
print(2 ** 1000)
print(2.0 ** 1000)
print(2.0 ** 1024)
```

## 2. Order of operations

**2.1** Predict each result before you run the cell. Then write down the rule that Python follows.

```python exec
id: order-of-operations-1
print(2 + 3 * 4)
print((2 + 3) * 4)
print(2 + 3 ** 2)
print(-3 ** 2)
print((-3) ** 2)
print(2 ** 3 ** 2)
print(10 - 4 - 3)
print(10 - (4 - 3))
print(100 / 10 / 5)
print(100 / (10 / 5))
print(2 * 3 % 4)
print(2 + 3 % 2)
```

**Worth knowing.** Python works out brackets first, then `**`, then `*`, `/`, `//` and `%` from left to right, and then `+` and `-` from left to right. Two cases are easy to miss. A line of `**` signs works from right to left, so `2 ** 3 ** 2` means `2 ** 9`. A minus sign in front of a number comes after `**`, so `-3 ** 2` means `-(3 ** 2)`.

**2.2** Add brackets to this expression so that it prints `19`. Then find brackets that make it print `15`, and then `11`.

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

**2.3** This program should print the average of 4, 9 and 14. It does not. Fix it.

```python exec
id: order-of-operations-3
print(4 + 9 + 14 / 3)
```

```solution
for: order-of-operations-3
title: one way to do it
print((4 + 9 + 14) / 3)
---
Division comes before addition, so the brackets make the three numbers add up first.
```

**2.4** Run each line. Does Python mind the spaces? What does a minus sign next to another minus sign do?

```python exec
id: order-of-operations-4
print(2+3*4)
print(2 + 3 * 4)
print(2 +3* 4)
print(2 - -3)
print(2--3)
print(2 + -3)
```

**2.5** Run each line, one at a time. What does Python say when we leave out an operator?

```python exec
id: order-of-operations-5
print(2(3))
# print(2 3)
# x = 4
# print(3x)
```

## 3. Decimal numbers

**3.1** Run this. Which results does your own calculator disagree with?

```python exec
id: decimal-numbers-1
print(0.1 + 0.2)
print(0.1 + 0.2 == 0.3)
print(0.5 + 0.25 == 0.75)
print(0.1 * 3)
print(1.1 * 3)
print(0.1 + 0.7)
```

**Worth knowing.** A computer stores decimal numbers in binary. A fraction such as one third has no exact decimal form, and a fraction such as one tenth has no exact binary form, in the same way. Numbers built from halves and quarters, such as 0.5 and 0.25, are stored exactly.

**3.2** Run this. Which of these two tests gives the answer we want?

```python exec
id: decimal-numbers-2
print(0.1 + 0.2 == 0.3)
print(round(0.1 + 0.2, 2) == 0.3)
print(abs((0.1 + 0.2) - 0.3) < 0.000001)
```

**3.3** Run this. How many digits does Python show?

```python exec
id: decimal-numbers-3
print(10 / 3)
print(2 / 3)
print(1 / 7)
print(100 / 3)
```

**3.4** Run this. Which of the last lines surprise you?

```python exec
id: decimal-numbers-4
print(round(3.14159, 2))
print(round(3.14159, 0))
print(round(3.14159))
print(round(1234, -2))
print(round(2.5))
print(round(3.5))
```

**3.5** Run this. What do `abs`, `min`, `max`, `pow` and `divmod` do?

```python exec
id: decimal-numbers-5
print(abs(-5))
print(abs(2.5))
print(min(3, 1, 2))
print(max(3, 1, 2))
print(pow(2, 3))
print(pow(2, 3, 5))
print(divmod(17, 5))
```

## 4. Puzzles with // and %

**4.1** A video lasts 1234 seconds. Print how many whole minutes that is, and how many seconds are left over.

```python exec
id: puzzles-with-and-1
seconds = 1234
# your code here
```

```solution
for: puzzles-with-and-1
title: one way to do it
seconds = 1234
minutes = seconds // 60
left_over = seconds % 60
print(minutes)
print(left_over)
```

**4.2** The number `n` holds four digits. Print each of its digits on a separate line, using only `//` and `%`.

```python exec
id: puzzles-with-and-2
n = 4729
# your code here
```

Change `n` to a different four-digit number to test it.

```solution
for: puzzles-with-and-2
title: one way to do it
n = 4729
print(n // 1000)
print(n // 100 % 10)
print(n // 10 % 10)
print(n % 10)
```

**4.3** Write an expression that prints `True` when `n` is even and `False` when it is odd. Test it with 7, 10, 0, -4 and -3.

```python exec
id: puzzles-with-and-3
n = 7
# your code here
```

```solution
for: puzzles-with-and-3
title: one way to do it
n = 7
print(n % 2 == 0)
```

**4.4** An item costs 237 cents. Print how many euros and how many cents that is.

```python exec
id: puzzles-with-and-4
cents = 237
# your code here
```

```solution
for: puzzles-with-and-4
title: one way to do it
cents = 237
print(cents // 100)
print(cents % 100)
```

**4.5** A clock face shows 12 hours. It shows 10 o'clock now. What does it show after 5 hours, after 50 hours, and after 2 hours? Use `%` and look carefully at the last answer for 12 o'clock.

```python exec
id: puzzles-with-and-5
hour = 10
print((hour + 5) % 12)
```

**4.6** A day has 24 hours. It is 22:00 now. Print the hour after 5 hours, after 30 hours, and after 100 hours.

```python exec
id: puzzles-with-and-6
hour = 22
# your code here
```

```solution
for: puzzles-with-and-6
title: one way to do it
hour = 22
print((hour + 5) % 24)
print((hour + 30) % 24)
print((hour + 100) % 24)
```

**4.7** A shop takes 20 percent off a price of 50 euros. Print the new price. Then print the amount of the discount.

```python exec
id: puzzles-with-and-7
price = 50
# your code here
```

```solution
for: puzzles-with-and-7
title: one way to do it
price = 50
discount = price * 20 / 100
print(price - discount)
print(discount)
```

**4.8** Convert 0, 100 and -40 degrees Celsius to Fahrenheit with `c * 9 / 5 + 32`. What is special about the last answer?

```python exec
id: puzzles-with-and-8
c = 100
print(c * 9 / 5 + 32)
```

```solution
for: puzzles-with-and-8
title: one way to do it
print(0 * 9 / 5 + 32)
print(100 * 9 / 5 + 32)
print(-40 * 9 / 5 + 32)
```

**4.9** A packet of crisps weighs 45 grams. How many whole packets fit in a 1000 gram box, and how many grams are left over?

```python exec
id: puzzles-with-and-9
# your code here
```

```solution
for: puzzles-with-and-9
title: one way to do it
grams = 1000
packet = 45
print(grams // packet)
print(grams % packet)
```

**4.10** Take the number 7381. Print the number with its last digit removed, and then print only its last digit. Use two lines.

```python exec
id: puzzles-with-and-10
n = 7381
# your code here
```

```solution
for: puzzles-with-and-10
title: one way to do it
n = 7381
print(n // 10)
print(n % 10)
```

**4.11** Reverse a two-digit number. If `n` holds 47, print 74. Use `//` and `%` and no strings.

```python exec
id: puzzles-with-and-11
n = 47
# your code here
```

```solution
for: puzzles-with-and-11
title: one way to do it
n = 47
print(n % 10 * 10 + n // 10)
```

**4.12** The sum of the digits of 4729 is 4 + 7 + 2 + 9. Print the sum, using `//` and `%`.

```python exec
id: puzzles-with-and-12
n = 4729
# your code here
```

```solution
for: puzzles-with-and-12
title: one way to do it
n = 4729
print(n // 1000 + n // 100 % 10 + n // 10 % 10 + n % 10)
```

## 5. Looking back

**5.1** Which of the operators `/`, `//`, `%` and `**` gave you the most surprising result? Describe the experiment you used to find out how it behaves.

**5.2** Write down two situations where `%` would help you in a program.
