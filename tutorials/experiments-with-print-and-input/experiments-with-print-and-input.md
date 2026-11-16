---
title: "Experiments with print and input: talking to the program"
year: "2026-2027"
version: 2026.11.16.1
---

# Experiments with print and input: talking to the program

The function `print` sends text out, and the function `input` brings text in. Each question here is small. Run the cell, change one thing, and watch what happens. Cells that call `input` wait for you to type a line and press Enter.

## 1. Print

**1.1** Run this. What does Python put between the two words?

```python exec
id: print-1
print("hello")
print("hello", "world")
print("hello", 5)
```

**1.2** Run this. What does a `print` with nothing inside the brackets do?

```python exec
id: print-2
print("above")
print()
print("below")
```

**1.3** Run this, and then change `"-"` to other things such as `""`, `", "` and `"\n"`. What does `sep` control?

```python exec
id: print-3
print("a", "b", "c", sep="-")
```

**1.4** Run this. What does `end` control, and what is its normal value?

```python exec
id: print-4
print("a", end="")
print("b")
print("c", end="!")
print("d", end=" ")
print("e")
```

**Worth knowing.** The words `sep` and `end` are options that we give to `print` by name. If we do not give them, `sep` is a single space and `end` is a line break.

**1.5** Write three `print` lines that put the words `one`, `two` and `three` on a single line, separated by spaces.

```python exec
id: print-5
# your code here
```

```solution
for: print-5
title: one way to do it
print("one", end=" ")
print("two", end=" ")
print("three")
```

**1.6** Predict which of the last four lines look alike, and then run the cell.

```python exec
id: print-6
print(3)
print(3.0)
print("3")
print(3 + 4)
print("3" + "4")
print("3", "4")
print(3, 4)
```

**1.7** Break this program in each of these ways, one at a time, and read each error: delete the last bracket, delete one quote, delete the first bracket, and add an extra bracket at the end.

```python exec
id: print-7
print("hi")
```

**1.8** Run each line, one at a time. Which of these work?

```python exec
id: print-8
print("hi")
# Print("hi")
# print ("hi")
# print"hi"
# PRINT("hi")
```

**1.9** Run this. What does `print` give back when it finishes?

```python exec
id: print-9
result = print("hi")
print(result)
```

**1.10** Run this. What do `\t`, `\\` and `\"` do inside a string? Why does the last line print a line break?

```python exec
id: print-10
print("Tab\there")
print("Backslash: \\")
print("Quote: \"")
print("C:\new")
```

**1.11** Print a row of 20 equals signs without typing 20 of them.

```python exec
id: print-11
# your code here
```

```solution
for: print-11
title: one way to do it
print("=" * 20)
```

**1.12** Print this shape with two `print` lines that each use a string and `*`.

```
>>>>>>>>>>
----------
```

```python exec
id: print-12
# your code here
```

```solution
for: print-12
title: one way to do it
print(">" * 10)
print("-" * 10)
```

## 2. Building text

**2.1** Run this. How does the first version differ from the second?

```python exec
id: building-text-1
name = "Sam"
print("Hello, " + name + "!")
print("Hello,", name, "!")
```

**2.2** Run this and read the error. Then fix the first line in two different ways.

```python exec
id: building-text-2
age = 15
print("Age: " + age)
```

```solution
for: building-text-2
title: one way to do it
age = 15
print("Age: " + str(age))
print("Age:", age)
```

**2.3** Run this. What does the letter `f` in front of the quote do, and what do the curly brackets do?

```python exec
id: building-text-3
name = "Sam"
age = 15
print(f"{name} is {age} years old")
```

**2.4** Change the `print` in 2.3 so that it also says how old Sam will be next year, by putting `{age + 1}` in the curly brackets.

```python exec
id: building-text-4
name = "Sam"
age = 15
# your code here
```

```solution
for: building-text-4
title: one way to do it
name = "Sam"
age = 15
print(f"{name} is {age} years old and will be {age + 1} next year")
```

**2.5** Break the f-string in three ways: remove the `f`, remove a closing curly bracket, and use a name that does not exist.

```python exec
id: building-text-5
name = "Sam"
print(f"Hello, {name}")
```

**2.6** Put the function call `name.upper()` inside the curly brackets. What can go inside curly brackets?

```python exec
id: building-text-6
name = "Sam"
print(f"Hello, {name}")
```

```solution
for: building-text-6
title: one way to do it
name = "Sam"
print(f"Hello, {name.upper()}")
```

**2.7** Run this. What does `:.2f` do to the number?

```python exec
id: building-text-7
price = 3.14159
print(f"{price}")
print(f"{price:.2f}")
```

Change the `2` to `0`, `1` and `5`.

**Worth knowing.** The text after the colon inside the curly brackets is a format. The format `.2f` means "show two digits after the decimal point". Other formats exist, and the next question shows three of them.

**2.8** Predict what each line prints, and then run the cell.

```python exec
id: building-text-8
print(f"{1234567:,}")
print(f"{7:03}")
print(f"{0.256:.1%}")
print(f"[{'hi':>6}]")
print(f"[{'hi':<6}]")
print(f"[{'hi':^6}]")
```

**2.9** Print a three-line price list so that the names line up on the left and the prices line up on the right.

```python exec
id: building-text-9
item1 = "Tea"
price1 = 2.5
item2 = "Sandwich"
price2 = 4.75
item3 = "Cake"
price3 = 3
# your code here
```

```solution
for: building-text-9
title: one way to do it
item1 = "Tea"
price1 = 2.5
item2 = "Sandwich"
price2 = 4.75
item3 = "Cake"
price3 = 3
print(f"{item1:<10}{price1:>6.2f}")
print(f"{item2:<10}{price2:>6.2f}")
print(f"{item3:<10}{price3:>6.2f}")
```

**2.10** Print a box around a name so that the box fits any name.

```python exec
id: building-text-10
name = "Sam"
# your code here
```

The output for `Sam` should look like this.

```
+-----+
| Sam |
+-----+
```

```solution
for: building-text-10
title: one way to do it
name = "Sam"
border = "+" + "-" * (len(name) + 2) + "+"
print(border)
print("| " + name + " |")
print(border)
---
The border has two spaces and two corner characters more than the name has letters, so its length follows the name.
```

## 3. Input

**3.1** Run this and type your name. What does the program print back?

```python exec
id: input-1
name = input()
print(name)
```

```typed
Sam
```

**3.2** Add a prompt by putting some text inside the brackets of `input`. What happens when the prompt has no space at the end?

```python exec
id: input-2
name = input("What is your name? ")
print("Hello, " + name)
```

```typed
Sam
```

**3.3** Run this and type a number. What type is the answer?

```python exec
id: input-3
answer = input("Type a number: ")
print(type(answer))
```

```typed
5
```

**3.4** Run this and type a number. Read the error, and then fix the last line.

```python exec
id: input-4
number = input("Number: ")
print(number + 1)
```

```typed
5
```

**Worth knowing.** The function `input` always gives back a string, even when we type digits. To work with the digits as a number, we convert the string with `int` or `float`.

**3.5** Run this and type `3.5`. Then change `int` to `float` and run it again. Which one accepts the decimal?

```python exec
id: input-5
number = int(input("Number: "))
print(number + 1)
```

```typed
3.5
```

**3.6** Run this and press Enter without typing anything. Then run it again and type some letters. What does each error say?

```python exec
id: input-6
age = int(input("Age: "))
print(age)
```

```typed
12
```

**3.7** Run this and type your name with some spaces before and after it. How long is the string? What does `strip` change?

```python exec
id: input-7
name = input("Name: ")
print(len(name))
print(len(name.strip()))
```

```typed
  Sam  
```

**3.8** Run this and type two words. Which word comes out first? Change the last line so that it prints them in the other order.

```python exec
id: input-8
first = input("First word: ")
second = input("Second word: ")
print(first, second)
```

```typed
cat
dog
```

**3.9** Run this and type two numbers. Then change `int` to `float`, and type a decimal.

```python exec
id: input-9
a = int(input("First: "))
b = int(input("Second: "))
print(a + b)
```

```typed
3
4
```

**3.10** Run this and type `1` and then `2`. Predict the output first.

```python exec
id: input-10
print(input() + input())
```

```typed
1
2
```

**3.11** Run this and type a number. Why does the answer look like this?

```python exec
id: input-11
x = input("x: ")
print(x * 3)
```

```typed
5
```

**3.12** Ask for a name, and then print it back inside a box, as in 2.10.

```python exec
id: input-12
# your code here
```

```typed
Sam
```

```solution
for: input-12
title: one way to do it
name = input("Name: ")
border = "+" + "-" * (len(name) + 2) + "+"
print(border)
print("| " + name + " |")
print(border)
```

**3.13** Ask for a radius, and print the area of a circle. Use 3.14159 for the value of pi.

```python exec
id: input-13
# your code here
```

```typed
2
```

```solution
for: input-13
title: one way to do it
radius = float(input("Radius: "))
area = 3.14159 * radius ** 2
print(f"{area:.2f}")
```

**3.14** Ask for a number of minutes, and print how many hours and minutes that is. For 135 minutes the program should say 2 hours and 15 minutes.

```python exec
id: input-14
# your code here
```

```typed
135
```

```solution
for: input-14
title: one way to do it
minutes = int(input("Minutes: "))
print(minutes // 60, "hours and", minutes % 60, "minutes")
```

**3.15** Make a mad-lib. Ask for a name, an animal and a food, and print a sentence that uses all three.

```python exec
id: input-15
# your code here
```

```typed
Ada
cat
toast
```

```solution
for: input-15
title: one way to do it
name = input("A name: ")
animal = input("An animal: ")
food = input("A food: ")
print(f"{name} met a {animal} that was eating {food}.")
```

## 4. Small programs

**4.1** Ask for a person's age in years, and print how many days old they are. Ignore leap years.

```python exec
id: small-programs-1
# your code here
```

```typed
15
```

```solution
for: small-programs-1
title: one way to do it
age = int(input("Age in years: "))
print(age * 365, "days old")
```

**4.2** Ask for a bill and a tip percentage. Print the tip, and print the total, each with two digits after the decimal point.

```python exec
id: small-programs-2
# your code here
```

```typed
42.50
15
```

```solution
for: small-programs-2
title: one way to do it
bill = float(input("Bill: "))
percent = float(input("Tip percent: "))
tip = bill * percent / 100
print(f"Tip: {tip:.2f}")
print(f"Total: {bill + tip:.2f}")
```

**4.3** Ask for a name, and print how many letters it has.

```python exec
id: small-programs-3
# your code here
```

```typed
Sam
```

```solution
for: small-programs-3
title: one way to do it
name = input("Name: ")
print("Your name has", len(name), "letters")
```

**4.4** Eight slices fit in one pizza. Ask how many slices a group needs, and print how many pizzas they must buy. Three slices need one pizza, and nine slices need two. Hint: `//` rounds down, so think about what you could add to the number of slices first.

```python exec
id: small-programs-4
# your code here
```

```typed
9
```

```solution
for: small-programs-4
title: one way to do it
slices = int(input("Slices needed: "))
pizzas = (slices + 7) // 8
print(pizzas)
---
Adding 7 before the whole-number division makes any leftover slices push the answer up to the next whole pizza. With exactly 8 slices the answer stays at 1.
```

**4.5** Ask for an amount of money in cents. Print how many 50c, 20c, 10c and 5c coins make up the amount, using as many large coins as possible, and then print the cents left over.

```python exec
id: small-programs-5
# your code here
```

```typed
187
```

```solution
for: small-programs-5
title: one way to do it
cents = int(input("Cents: "))
print(cents // 50, "coins of 50c")
cents = cents % 50
print(cents // 20, "coins of 20c")
cents = cents % 20
print(cents // 10, "coins of 10c")
cents = cents % 10
print(cents // 5, "coins of 5c")
cents = cents % 5
print(cents, "cents left over")
```

**4.6** Ask for a four-digit number. Print the digits in reverse order, using `//` and `%`.

```python exec
id: small-programs-6
# your code here
```

```typed
4729
```

```solution
for: small-programs-6
title: one way to do it
n = int(input("Four-digit number: "))
print(n % 10, n // 10 % 10, n // 100 % 10, n // 1000, sep="")
```

**4.7** Ask for a temperature in Celsius, and print it in Fahrenheit with one digit after the decimal point.

```python exec
id: small-programs-7
# your code here
```

```typed
37
```

```solution
for: small-programs-7
title: one way to do it
celsius = float(input("Celsius: "))
fahrenheit = celsius * 9 / 5 + 32
print(f"{fahrenheit:.1f}")
```

## 5. Looking back

**5.1** Which experiment taught you the most about `input`? What did you change to find out?

**5.2** Write down three errors that can happen when a person types something unexpected into a program that calls `int(input())`.
