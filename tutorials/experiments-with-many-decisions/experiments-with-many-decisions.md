---
title: "Experiments with if: many decisions"
year: "2026-2027"
version: 2026.11.16.1
---

# Experiments with if: many decisions

One `if` chooses between two paths. This page is about choosing between many paths. Run each cell, change the values, and trace which line runs. Each cell sets up everything it uses.

## 1. elif

An `elif` chain asks its questions in order, from the top. Python runs the block of the first condition that is `True`, and then it skips the rest of the chain, even when later conditions are `True` as well. The `else` at the end runs only when every condition was `False`.

**1.1** Run this with `score` set to 100, 70, 69, 50, 49 and 0. Which block runs for each score?

```python exec
id: elif-1
score = 72
if score >= 70:
    print("A")
elif score >= 60:
    print("B")
elif score >= 50:
    print("C")
else:
    print("F")
```

**1.2** The score 72 makes all three conditions in 1.1 true. Why does only one letter print?

**1.3** These conditions come in the opposite order. Run it with 72. Why does it print what it prints? Which scores could ever reach the `A`?

```python exec
id: elif-2
score = 72
if score >= 50:
    print("C")
elif score >= 60:
    print("B")
elif score >= 70:
    print("A")
else:
    print("F")
```

**1.4** Every `elif` from 1.1 has become an `if`. Run it with 72. What does `elif` do that `if` does not?

```python exec
id: elif-3
score = 72
if score >= 70:
    print("A")
if score >= 60:
    print("B")
if score >= 50:
    print("C")
else:
    print("F")
```

**1.5** Run this with `x` set to 2, 4 and 5. Which `if` does the `else` belong to?

```python exec
id: elif-4
x = 5
if x > 3:
    print("big")
if x > 4:
    print("bigger")
else:
    print("not bigger")
```

**1.6** Run this and read the error. What must come before an `elif`?

```python exec
id: elif-5
mark = 55
elif mark > 50:
    print("pass")
```

**1.7** Write a chain for the weather. Below 0 prints `freezing`, from 0 up to 15 prints `cold`, from 15 up to 25 prints `mild`, and 25 or more prints `hot`. Test the values at each boundary.

```python exec
id: elif-6
temperature = 15
# your code here
```

```solution
for: elif-6
title: one way to do it
temperature = 15
if temperature < 0:
    print("freezing")
elif temperature < 15:
    print("cold")
elif temperature < 25:
    print("mild")
else:
    print("hot")
```

## 2. Decisions inside decisions

**2.1** Run this for each of the four combinations of `age` and `has_ticket`. Which line prints each time?

```python exec
id: decisions-inside-decisions-1
age = 20
has_ticket = True
if age >= 18:
    if has_ticket:
        print("enter")
    else:
        print("buy a ticket")
else:
    print("too young")
```

**2.2** Write the program from 2.1 again with no `if` inside another `if`. Use `and` to join two conditions.

```python exec
id: decisions-inside-decisions-2
age = 20
has_ticket = True
# your code here
```

```solution
for: decisions-inside-decisions-2
title: one way to do it
age = 20
has_ticket = True
if age >= 18 and has_ticket:
    print("enter")
elif age >= 18:
    print("buy a ticket")
else:
    print("too young")
```

**2.3** Predict which letters this prints, and then run it. Change `a` to 1, 3 and 11 and predict again each time.

```python exec
id: decisions-inside-decisions-3
a = 5
if a > 3:
    print("x")
if a > 4:
    print("y")
elif a > 2:
    print("z")
if a > 10:
    print("w")
else:
    print("v")
```

**2.4** Find values of `x` and `y` that make each of `A`, `B`, `C` and `D` print.

```python exec
id: decisions-inside-decisions-4
x = 7
y = 12
if x > y:
    print("A")
elif x + y > 15:
    if x % 2 == 1:
        print("B")
    else:
        print("C")
else:
    print("D")
```

```solution
for: decisions-inside-decisions-4
title: one way to do it
x = 8
y = 12
if x > y:
    print("A")
elif x + y > 15:
    if x % 2 == 1:
        print("B")
    else:
        print("C")
else:
    print("D")
---
This version prints `C`. The values `x = 9, y = 3` print `A`, the starting values print `B`, and `x = 1, y = 2` print `D`.
```

## 3. Programs that choose

**3.1** A ticket costs nothing under 5, 5 euros from 5 to 17, 10 euros from 18 to 64, and 7 euros from 65. Ask for an age and print the price.

```python exec
id: programs-that-choose-1
# your code here
```

```typed
30
```

```solution
for: programs-that-choose-1
title: one way to do it
age = int(input("Age: "))
if age < 5:
    print(0)
elif age < 18:
    print(5)
elif age < 65:
    print(10)
else:
    print(7)
```

**3.2** Write the ticket program again so that each block stores the price in a name, and a single `print` at the end shows it.

```python exec
id: programs-that-choose-2
age = 30
# your code here
```

```solution
for: programs-that-choose-2
title: one way to do it
age = 30
if age < 5:
    price = 0
elif age < 18:
    price = 5
elif age < 65:
    price = 10
else:
    price = 7
print(price)
```

**3.3** Ask for two numbers. Print the larger one, or print a message when they are equal.

```python exec
id: programs-that-choose-3
# your code here
```

```typed
8
3
```

```solution
for: programs-that-choose-3
title: one way to do it
a = float(input("First: "))
b = float(input("Second: "))
if a > b:
    print(a)
elif b > a:
    print(b)
else:
    print("They are equal")
```

**3.4** Ask for three numbers and print the largest, without using `max`.

```python exec
id: programs-that-choose-4
# your code here
```

```typed
4
9
6
```

```solution
for: programs-that-choose-4
title: one way to do it
a = float(input("First: "))
b = float(input("Second: "))
c = float(input("Third: "))
if a >= b and a >= c:
    print(a)
elif b >= c:
    print(b)
else:
    print(c)
```

**3.5** Ask for a year and say whether it is a leap year. A year is a leap year when 4 divides it, unless 100 divides it, unless 400 divides it. Test 1900, 2000, 2023 and 2024.

```python exec
id: programs-that-choose-5
# your code here
```

```typed
2024
```

```solution
for: programs-that-choose-5
title: one way to do it
year = int(input("Year: "))
if year % 400 == 0:
    print("leap year")
elif year % 100 == 0:
    print("not a leap year")
elif year % 4 == 0:
    print("leap year")
else:
    print("not a leap year")
```

**3.6** Ask for a number. Print `Fizz` when 3 divides it, `Buzz` when 5 divides it, `FizzBuzz` when both divide it, and the number itself otherwise.

```python exec
id: programs-that-choose-6
# your code here
```

```typed
15
```

```solution
for: programs-that-choose-6
title: one way to do it
n = int(input("Number: "))
if n % 15 == 0:
    print("FizzBuzz")
elif n % 3 == 0:
    print("Fizz")
elif n % 5 == 0:
    print("Buzz")
else:
    print(n)
---
The test for both has to come first. Otherwise 15 would match `n % 3 == 0` and never reach a later test.
```

**3.7** Ask for three side lengths. Say whether they make a triangle, and if they do, whether it is equilateral, isosceles or scalene. Three lengths make a triangle when each pair adds up to more than the third.

```python exec
id: programs-that-choose-7
# your code here
```

```typed
3
4
5
```

```solution
for: programs-that-choose-7
title: one way to do it
a = float(input("Side one: "))
b = float(input("Side two: "))
c = float(input("Side three: "))
if a + b > c and a + c > b and b + c > a:
    if a == b and b == c:
        print("equilateral")
    elif a == b or b == c or a == c:
        print("isosceles")
    else:
        print("scalene")
else:
    print("not a triangle")
```

**3.8** Two players each type `rock`, `paper` or `scissors`. Print which player wins, or print `draw`.

```python exec
id: programs-that-choose-8
# your code here
```

```typed
rock
scissors
```

```solution
for: programs-that-choose-8
title: one way to do it
first = input("Player one: ")
second = input("Player two: ")
if first == second:
    print("draw")
elif first == "rock" and second == "scissors":
    print("player one wins")
elif first == "scissors" and second == "paper":
    print("player one wins")
elif first == "paper" and second == "rock":
    print("player one wins")
else:
    print("player two wins")
```

**3.9** The program keeps a secret number. Ask for a guess and print `too low`, `too high` or `correct`.

```python exec
id: programs-that-choose-9
# your code here
```

```typed
50
```

```solution
for: programs-that-choose-9
title: one way to do it
secret = 42
guess = int(input("Guess: "))
if guess < secret:
    print("too low")
elif guess > secret:
    print("too high")
else:
    print("correct")
```

**3.10** Ask for a month number from 1 to 12 and print how many days that month has. Ignore leap years.

```python exec
id: programs-that-choose-10
# your code here
```

```typed
4
```

```solution
for: programs-that-choose-10
title: one way to do it
month = int(input("Month number: "))
if month == 2:
    print(28)
elif month == 4 or month == 6 or month == 9 or month == 11:
    print(30)
else:
    print(31)
```

## 4. Puzzles

**4.1** Write an `if`, `elif`, `elif` chain in which every condition is true, yet only one line prints.

```python exec
id: puzzles-1
# your code here
```

```solution
for: puzzles-1
title: one way to do it
x = 10
if x > 1:
    print("first")
elif x > 2:
    print("second")
elif x > 3:
    print("third")
```

**4.2** Ask for a number and print it limited to the range from 0 to 100. A number below 0 becomes 0, and a number above 100 becomes 100.

```python exec
id: puzzles-2
# your code here
```

```typed
150
```

```solution
for: puzzles-2
title: one way to do it
number = float(input("Number: "))
if number < 0:
    print(0)
elif number > 100:
    print(100)
else:
    print(number)
```

**4.3** Write a small adventure with three rooms. Ask the player to choose `left` or `right` in each room, and use decisions inside decisions to say where each choice leads.

```python exec
id: puzzles-3
# your code here
```

## 5. Looking back

**5.1** Which error names did you meet on this page? Write one sentence for each that says what caused it.

**5.2** When would you choose a chain of `elif` over several separate `if` statements?
