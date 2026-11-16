---
title: "Experiments with if statements: choosing a path"
year: "2026-2027"
version: 2026.11.16.1
---

# Experiments with if statements: choosing a path

A program can choose which lines to run. It does this with a condition, which is a question that has the answer `True` or `False`. Run each cell, change the numbers, and find out where the boundaries lie. Keep a note of each error name you meet.

## 1. Questions with True or False answers

**1.1** Run this. Which comparison does each operator make?

```python exec
id: questions-with-true-or-false-answers-1
print(3 < 5)
print(3 > 5)
print(3 == 3)
print(3 != 3)
print(3 <= 3)
print(3 >= 4)
```

**1.2** Run each line, one at a time. Which of these work, and what does Python say about the ones that fail?

```python exec
id: questions-with-true-or-false-answers-2
x = 3
print(x == 3)
# print(3 = 3)
# print(x = 3)
```

**Worth knowing.** A single `=` attaches a name to a value. A double `==` asks whether two values are equal. Python gives an error when we use one where we meant the other, and it often suggests which one we meant.

**1.3** Predict each result before you run the cell. Which of them depend on capital letters?

```python exec
id: questions-with-true-or-false-answers-3
print("apple" == "apple")
print("Apple" == "apple")
print("apple" < "banana")
print("apple" < "Apple")
print("a" < "B")
print("10" < "9")
print(10 < 9)
```

**1.4** Run this. Which comparisons work between different types, and which fail?

```python exec
id: questions-with-true-or-false-answers-4
print(3 == 3.0)
print(3 == "3")
print(1 == True)
# print(3 < "5")
```

**1.5** Run this. Python allows several comparisons in a row. How does it read each one?

```python exec
id: questions-with-true-or-false-answers-5
print(1 < 2 < 3)
print(1 < 3 < 2)
print(3 > 2 > 1)
print(2 < 2 < 3)
print(1 == 1 == 1)
```

**1.6** Make `x` hold 15, then 5, then 25. For which values does `10 < x < 20` print `True`?

```python exec
id: questions-with-true-or-false-answers-6
x = 15
print(10 < x < 20)
```

**1.7** Run this. Fill in a table of the results for `and`, `or` and `not`, and write down what each word does.

```python exec
id: questions-with-true-or-false-answers-7
print(True and True)
print(True and False)
print(False and True)
print(False and False)
print(True or True)
print(True or False)
print(False or True)
print(False or False)
print(not True)
print(not False)
```

**1.8** Run this with `age` set to 12, 13, 19 and 20. Which values give `True`?

```python exec
id: questions-with-true-or-false-answers-8
age = 15
print(age >= 13 and age <= 19)
print(not age < 13)
```

**1.9** Predict each result, and then run the cell. In which order does Python handle `not`, `and` and `or`?

```python exec
id: questions-with-true-or-false-answers-9
print(True or False and False)
print((True or False) and False)
print(not True or True)
print(not (True or True))
```

**1.10** Run each line, one at a time. Which of these fail, and why do some of them not fail?

```python exec
id: questions-with-true-or-false-answers-10
print(True or 1 / 0)
# print(False and 1 / 0)
# print(False or 1 / 0)
# print(True and 1 / 0)
```

**Worth knowing.** Python stops as soon as it knows the answer. If the left side of `or` is `True`, the answer is `True` whatever the right side holds, so Python never looks at the right side.

## 2. Your first if

**2.1** Run this. Then change `25` to `10`. Which lines print each time?

```python exec
id: your-first-if-1
temperature = 25
if temperature > 20:
    print("warm")
print("done")
```

**2.2** Remove the spaces in front of `print("warm")`. Read the error. What does it say about the line after the colon?

```python exec
id: your-first-if-2
temperature = 25
if temperature > 20:
    print("warm")
print("done")
```

**2.3** Put four spaces in front of `print("done")` as well. Run it with `temperature` set to 25 and to 10. What changed?

```python exec
id: your-first-if-3
temperature = 25
if temperature > 20:
    print("warm")
print("done")
```

**2.4** Take the colon off the end of the `if` line. What does the error say?

```python exec
id: your-first-if-4
temperature = 25
if temperature > 20:
    print("warm")
```

**2.5** Change `==` to `=` in the `if` line. What does the error say?

```python exec
id: your-first-if-5
x = 3
if x == 3:
    print("three")
```

**2.6** Indent the first line of the body with four spaces and the second with two spaces. Read the error.

```python exec
id: your-first-if-6
x = 3
if x == 3:
    print("three")
    print("indeed")
```

**2.7** Put three lines in the body of an `if`, and put a blank line and a comment between two of them. Does the body still belong to the `if`?

```python exec
id: your-first-if-7
x = 3
if x == 3:
    print("one")
```

**2.8** Remove the body from this `if` and run it. Then put the word `pass` in its place. What does `pass` do?

```python exec
id: your-first-if-8
x = 3
if x == 3:
    print("three")
print("end")
```

**2.9** Replace the condition in each of these with the value shown. Which values make the body run?

```python exec
id: your-first-if-9
if 5:
    print("ran")
```

Try `0`, `""`, `"no"`, `True`, `False`, `0.0` and `" "`.

## 3. else and elif

**3.1** Run this with `age` set to 17, 18 and 19. Where does the boundary lie?

```python exec
id: else-and-elif-1
age = 15
if age >= 18:
    print("adult")
else:
    print("minor")
```

**3.2** Break it in three ways, one at a time: indent `else` by four spaces, give `else` a condition, and write `else` with no `if` above it.

```python exec
id: else-and-elif-2
age = 15
if age >= 18:
    print("adult")
else:
    print("minor")
```

**3.3** Run this with `score` set to 100, 70, 69, 50, 49, 0 and -5. Which lines run for each score?

```python exec
id: else-and-elif-3
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

**3.4** Reverse the order of the three conditions, so that the one for 50 comes first. Run it with 72. Why does it print what it prints?

```python exec
id: else-and-elif-4
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

**3.5** Change every `elif` in 3.3 to `if`, and run it with 72. How does `elif` differ from `if`?

```python exec
id: else-and-elif-5
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

**3.6** Run this with `x` set to 2, 4 and 5. Which `if` does the `else` belong to?

```python exec
id: else-and-elif-6
x = 5
if x > 3:
    print("big")
if x > 4:
    print("bigger")
else:
    print("not bigger")
```

**3.7** Run this for each of the four combinations of `age` and `has_ticket`. Which line prints in each case?

```python exec
id: else-and-elif-7
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

**3.8** Write the same program with a single `if`, an `elif` and an `else`, using `and` to join two conditions.

```python exec
id: else-and-elif-8
age = 20
has_ticket = True
# your code here
```

```solution
for: else-and-elif-8
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

**3.9** Predict which letters this prints, and then run it. Change the indentation of the last `print` to see what moves.

```python exec
id: else-and-elif-9
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

## 4. Programs that decide

**4.1** Ask for a number and print `even` or `odd`.

```python exec
id: programs-that-decide-1
# your code here
```

```typed
7
```

```solution
for: programs-that-decide-1
title: one way to do it
n = int(input("Number: "))
if n % 2 == 0:
    print("even")
else:
    print("odd")
```

**4.2** Ask for a password. Print `welcome` if it is `swordfish` and `denied` if it is anything else. Then change the program so that `Swordfish` and `SWORDFISH` also work.

```python exec
id: programs-that-decide-2
# your code here
```

```typed
Swordfish
```

```solution
for: programs-that-decide-2
title: one way to do it
password = input("Password: ")
if password.lower() == "swordfish":
    print("welcome")
else:
    print("denied")
---
Without `.lower()` only the exact text `swordfish` works. Turning the answer into lower case first lets `Swordfish` and `SWORDFISH` through as well.
```

**4.3** A ticket costs nothing under 5, 5 euros from 5 to 17, 10 euros from 18 to 64, and 7 euros from 65. Ask for an age and print the price.

```python exec
id: programs-that-decide-3
# your code here
```

```typed
30
```

```solution
for: programs-that-decide-3
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

**4.4** Ask for two numbers and print the larger one. Print a different message when they are equal.

```python exec
id: programs-that-decide-4
# your code here
```

```typed
8
3
```

```solution
for: programs-that-decide-4
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

**4.5** Ask for three numbers and print the largest one, without using `max`.

```python exec
id: programs-that-decide-5
# your code here
```

```typed
4
9
6
```

```solution
for: programs-that-decide-5
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

**4.6** Ask for a year and say whether it is a leap year. A year is a leap year when 4 divides it, unless 100 divides it, unless 400 divides it. Test 1900, 2000, 2023 and 2024.

```python exec
id: programs-that-decide-6
# your code here
```

```typed
2024
```

```solution
for: programs-that-decide-6
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

**4.7** Ask for three side lengths. Say whether they make a triangle, and if they do, say whether it is equilateral, isosceles or scalene. Three lengths make a triangle when every pair adds up to more than the third.

```python exec
id: programs-that-decide-7
# your code here
```

```typed
3
4
5
```

```solution
for: programs-that-decide-7
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

**4.8** Ask for a number. Print `Fizz` when 3 divides it, `Buzz` when 5 divides it, `FizzBuzz` when both divide it, and the number itself otherwise.

```python exec
id: programs-that-decide-8
# your code here
```

```typed
15
```

```solution
for: programs-that-decide-8
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
The test for both has to come first. A number such as 15 would match `n % 3 == 0` before it ever reached a later test.
```

**4.9** Two players each type `rock`, `paper` or `scissors`. Print which player wins, or print `draw`.

```python exec
id: programs-that-decide-9
# your code here
```

```typed
rock
scissors
```

```solution
for: programs-that-decide-9
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

**4.10** Ask for text. If the text is made only of digits, print the number doubled. Otherwise print `that is not a whole number`.

```python exec
id: programs-that-decide-10
# your code here
```

```typed
12
```

```solution
for: programs-that-decide-10
title: one way to do it
text = input("Type a whole number: ")
if text.isdigit():
    print(int(text) * 2)
else:
    print("that is not a whole number")
```

**4.11** Ask for a number and print it limited to the range from 0 to 100. A number below 0 becomes 0, and a number above 100 becomes 100.

```python exec
id: programs-that-decide-11
# your code here
```

```typed
150
```

```solution
for: programs-that-decide-11
title: one way to do it
number = float(input("Number: "))
if number < 0:
    print(0)
elif number > 100:
    print(100)
else:
    print(number)
```

**4.12** Ask for a month number from 1 to 12, and print how many days that month has. Ignore leap years.

```python exec
id: programs-that-decide-12
# your code here
```

```typed
4
```

```solution
for: programs-that-decide-12
title: one way to do it
month = int(input("Month number: "))
if month == 2:
    print(28)
elif month == 4 or month == 6 or month == 9 or month == 11:
    print(30)
else:
    print(31)
```

**4.13** The program holds a secret number. Ask for a guess, and print `too low`, `too high` or `correct`.

```python exec
id: programs-that-decide-13
# your code here
```

```typed
50
```

```solution
for: programs-that-decide-13
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

## 5. Shorter ways to write a decision

**5.1** Run this. How does the second version of the program compare with the first?

```python exec
id: shorter-ways-to-write-a-decision-1
age = 15
if age >= 18:
    print("adult")
else:
    print("minor")

print("adult" if age >= 18 else "minor")
```

**Worth knowing.** The form `A if condition else B` is one expression that gives back `A` when the condition is true and `B` when it is false. We can put it inside a `print`, or on the right of an `=`.

**5.2** Write the ticket prices from 4.3 with three conditions, but this time store the price in a variable and print it once at the end.

```python exec
id: shorter-ways-to-write-a-decision-2
age = 30
# your code here
```

```solution
for: shorter-ways-to-write-a-decision-2
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

**5.3** Run this. What does `or` hand back when the left side is empty or zero?

```python exec
id: shorter-ways-to-write-a-decision-3
print(0 or 5)
print(3 or 5)
print("" or "none given")
print("Sam" or "none given")
print(3 and 5)
print(0 and 5)
```

**5.4** Use what you saw in 5.3 to print `stranger` when `name` is empty, and the name otherwise, in a single `print`.

```python exec
id: shorter-ways-to-write-a-decision-4
name = ""
# your code here
```

```solution
for: shorter-ways-to-write-a-decision-4
title: one way to do it
name = ""
print(name or "stranger")
```

## 6. Puzzles

**6.1** Run this with `x` and `y` set to 7 and 12. Then find values of `x` and `y` that make each of `A`, `B`, `C` and `D` print.

```python exec
id: puzzles-1
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
for: puzzles-1
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
This version prints `C`. The values `x = 9` and `y = 3` print `A`, the values `x = 7` and `y = 12` print `B`, and the values `x = 1` and `y = 2` print `D`.
```

**6.2** Write a condition that is `True` only when `n` has exactly two digits. Test it with 5, 10, 99 and 100.

```python exec
id: puzzles-2
n = 47
# your code here
```

```solution
for: puzzles-2
title: one way to do it
n = 47
print(10 <= n <= 99)
---
A negative number such as -47 also has two digits. The test `10 <= abs(n) <= 99` covers both signs.
```

**6.3** Write a program in which every condition on an `if`, `elif`, `elif` ladder is true, yet only one line prints.

```python exec
id: puzzles-3
# your code here
```

```solution
for: puzzles-3
title: one way to do it
x = 10
if x > 1:
    print("first")
elif x > 2:
    print("second")
elif x > 3:
    print("third")
```

**6.4** Write a condition that is `True` when `x` is odd and greater than 10, or when `x` is exactly 0. Test it with 0, 3, 11, 12 and 13.

```python exec
id: puzzles-4
x = 11
# your code here
```

```solution
for: puzzles-4
title: one way to do it
x = 11
print((x % 2 == 1 and x > 10) or x == 0)
```

**6.5** Make `a` hold the smaller of two values and `b` hold the larger, using one `if` and a third variable.

```python exec
id: puzzles-5
a = 9
b = 4
# your code here
print(a, b)
```

```solution
for: puzzles-5
title: one way to do it
a = 9
b = 4
if a > b:
    temporary = a
    a = b
    b = temporary
print(a, b)
```

**6.6** Write a small adventure with three rooms. Ask the player to choose `left` or `right` in each room, and use nested `if` statements to decide where each choice leads.

```python exec
id: puzzles-6
# your code here
```

## 7. Looking back

**7.1** Which error names did you meet on this page? Write one sentence for each that says what caused it.

**7.2** Which of the experiments changed how you read an `if` statement, and what did you change to find out?
