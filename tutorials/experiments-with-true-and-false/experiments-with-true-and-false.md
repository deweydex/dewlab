---
title: "Experiments with True and False: questions Python can answer"
year: "2026-2027"
version: 2026.11.16.1
---

# Experiments with True and False: questions Python can answer

A program makes decisions by asking questions that have one of two answers, `True` or `False`. This page is about the questions themselves. The next two pages use them to choose which lines run. Run each cell, change the numbers, and find out where the answers flip.

## 1. Comparisons

A comparison has a value on each side and an operator in the middle. Python answers it with a value of type `bool`, which is either `True` or `False`.

**1.1** Run this. Which comparison does each operator make?

```python exec
id: comparisons-1
print(3 < 5)
print(3 > 5)
print(3 == 3)
print(3 != 3)
print(3 <= 3)
print(3 >= 4)
print(type(3 < 5))
```

**1.2** For each line, find the two values and the operator. Predict each answer, and then run the cell.

```python exec
id: comparisons-2
temperature = 18
print(temperature > 20)
print(temperature + 5 > 20)
print(temperature * 2 == 36)
print(temperature != 18)
```

**1.3** Run this and read the error. Then change the line so that it asks whether 3 equals 3.

```python exec
id: comparisons-3
print(3 = 3)
```

```solution
for: comparisons-3
title: one way to do it
print(3 == 3)
```

**Worth knowing.** A single `=` attaches a name to a value. A double `==` asks whether two values are equal. Python gives an error when we use one where we meant the other, and the message often suggests which one we meant.

**1.4** Predict each line before you run the cell. Which ones depend on capital letters?

```python exec
id: comparisons-4
print("apple" == "apple")
print("Apple" == "apple")
print("apple" < "banana")
print("apple" < "Apple")
print("10" < "9")
print(10 < 9)
```

**1.5** Run this. Which comparisons between different types work?

```python exec
id: comparisons-5
print(3 == 3.0)
print(3 == "3")
print(3 != "3")
```

**1.6** Run this and read the error. Why can Python answer `3 == "5"` but not `3 < "5"`?

```python exec
id: comparisons-6
print(3 < "5")
```

**1.7** Python lets us chain comparisons. Set `x` to 5, 10, 15, 20 and 25 in turn. For which values does the line print `True`?

```python exec
id: comparisons-7
x = 15
print(10 < x < 20)
```

## 2. and, or, not

**2.1** Run this. Fill in a table of the results, and write one sentence each for what `and`, `or` and `not` do.

```python exec
id: and-or-not-1
print(True and True)
print(True and False)
print(False and False)
print(True or False)
print(False or False)
print(not True)
print(not False)
```

**2.2** Run this with `age` set to 12, 13, 19 and 20. Which values give `True` on each line?

```python exec
id: and-or-not-2
age = 15
print(age >= 13 and age <= 19)
print(age < 13 or age > 19)
print(not age < 13)
```

**2.3** Write a question that is `True` only when `day` is `"Saturday"` or `"Sunday"`. Test it with three days.

```python exec
id: and-or-not-3
day = "Saturday"
# your code here
```

```solution
for: and-or-not-3
title: one way to do it
day = "Saturday"
print(day == "Saturday" or day == "Sunday")
```

**2.4** This line was meant to ask whether `day` is a weekend day. Run it with `day` set to `"Monday"`. Why does it print what it prints?

```python exec
id: and-or-not-4
day = "Monday"
print(day == "Saturday" or "Sunday")
```

```solution
for: and-or-not-4
title: one way to do it
day = "Monday"
print(day == "Saturday" or day == "Sunday")
---
Python reads the original as `(day == "Saturday") or "Sunday"`. The text `"Sunday"` counts as true by itself, so the `or` hands it back whatever the day is. Each side of `or` needs its own comparison.
```

**2.5** Predict each result, and then run the cell. In which order does Python handle `not`, `and` and `or`?

```python exec
id: and-or-not-5
print(True or False and False)
print((True or False) and False)
print(not True or True)
print(not (True or True))
```

**2.6** Run each line, one at a time. Some of these never reach the division by zero. Which ones, and why?

```python exec
id: and-or-not-6
print(True or 1 / 0)
# print(False and 1 / 0)
# print(False or 1 / 0)
# print(True and 1 / 0)
```

**Worth knowing.** Python stops as soon as it knows the answer. When the left side of `or` is `True`, the whole question is `True` whatever the right side says, so Python never looks at the right side. When the left side of `and` is `False`, Python stops in the same way.

## 3. What counts as true

**3.1** Predict which of these print `False`, and then run the cell. What rule picks out the values that become `False`?

```python exec
id: what-counts-as-true-1
print(bool(0))
print(bool(1))
print(bool(-1))
print(bool(""))
print(bool(" "))
print(bool("False"))
print(bool(0.0))
```

**3.2** Run this. What numbers do `True` and `False` stand for in arithmetic?

```python exec
id: what-counts-as-true-2
print(True + True)
print(True * 5)
print(False + 5)
print(1 == True)
```

**Worth knowing.** Python treats `True` as the whole number 1 and `False` as 0 when it does arithmetic. Adding up a few comparisons therefore counts how many of them are true.

**3.3** Use the note above to count how many of the three numbers are above 10, with one line of arithmetic.

```python exec
id: what-counts-as-true-3
a = 4
b = 12
c = 30
# your code here
```

```solution
for: what-counts-as-true-3
title: one way to do it
a = 4
b = 12
c = 30
print((a > 10) + (b > 10) + (c > 10))
```

**3.4** Run this. What does `or` hand back when its left side counts as false?

```python exec
id: what-counts-as-true-4
print(0 or 5)
print(3 or 5)
print("" or "nobody")
print("Sam" or "nobody")
```

## 4. Puzzles

**4.1** Write a question that is `True` only when `n` has exactly two digits. Test it with 5, 10, 99 and 100.

```python exec
id: puzzles-1
n = 47
# your code here
```

```solution
for: puzzles-1
title: one way to do it
n = 47
print(10 <= n <= 99)
---
A negative number such as -47 has two digits as well. The question `10 <= abs(n) <= 99` covers both signs.
```

**4.2** Write a question that is `True` when `x` is odd and greater than 10, or when `x` is 0. Test it with 0, 3, 11, 12 and 13.

```python exec
id: puzzles-2
x = 11
# your code here
```

```solution
for: puzzles-2
title: one way to do it
x = 11
print((x % 2 == 1 and x > 10) or x == 0)
```

**4.3** Write a question that is `True` when `letter` is a vowel. Test it with `"e"`, `"z"` and `"E"`.

```python exec
id: puzzles-3
letter = "e"
# your code here
```

```solution
for: puzzles-3
title: one way to do it
letter = "e"
print(letter.lower() in "aeiou")
```

**4.4** A year is a leap year when 4 divides it, unless 100 divides it, unless 400 divides it. Write one question that is `True` for leap years. Test it with 1900, 2000, 2023 and 2024.

```python exec
id: puzzles-4
year = 2024
# your code here
```

```solution
for: puzzles-4
title: one way to do it
year = 2024
print(year % 4 == 0 and (year % 100 != 0 or year % 400 == 0))
```

**4.5** Find values of `a` and `b` that make all three lines print `True`.

```python exec
id: puzzles-5
a = 1
b = 1
print(a < b)
print(a + b > 10)
print(a % 2 == 0)
```

```solution
for: puzzles-5
title: one way to do it
a = 4
b = 9
print(a < b)
print(a + b > 10)
print(a % 2 == 0)
```

## 5. Looking back

**5.1** Which error names did you meet on this page? Write one sentence for each that says what caused it.

**5.2** Explain the mistake in `day == "Saturday" or "Sunday"` to someone who has not seen it before.
