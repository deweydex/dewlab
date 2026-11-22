---
title: "Experiments with input: asking the person at the keyboard"
year: "2026-2027"
version: 2026.11.16.1
---

# Experiments with input: asking the person at the keyboard

The function `input` stops the program and waits for someone to type a line. When you run a cell that calls `input`, a box appears; type your answer and press Enter. Run each cell, try different answers, and keep a note of each error name you meet.

## 1. What input gives back

Whatever the person types, `input` hands it back as a string. That holds even when they type only digits.

**1.1** Run this and type your name. What does the program print back?

```python exec
id: what-input-gives-back-1
name = input()
print(name)
```

```typed
Sam
```

**1.2** Put a prompt inside the brackets of `input`. Then delete the space at the end of the prompt, and run it again. What changes on the screen?

```python exec
id: what-input-gives-back-2
name = input("What is your name? ")
print("Hello, " + name)
```

```typed
Sam
```

**1.3** Run this and type a number. What type does Python report?

```python exec
id: what-input-gives-back-3
answer = input("Type a number: ")
print(type(answer))
```

```typed
5
```

**1.4** Run this and type `5`. Read the error, and then fix the last line.

```python exec
id: what-input-gives-back-4
number_text = input("Number: ")
print(number_text + 1)
```

```typed
5
```

```solution
for: what-input-gives-back-4
title: one way to do it
number_text = input("Number: ")
print(int(number_text) + 1)
```

**1.5** Run this and type `5`. Why does the answer look like this?

```python exec
id: what-input-gives-back-5
x_text = input("x: ")
print(x_text * 3)
```

```typed
5
```

**1.6** Run this and type `1`, then `2`. Predict the output first.

```python exec
id: what-input-gives-back-6
print(input() + input())
```

```typed
1
2
```

**Worth knowing.** To use typed digits as a number, we convert the string with `int` or `float`. The line `age = int(input("Age: "))` asks, converts and stores in one go.

**1.7** Run this and type `3.5`. Then change `int` to `float` and run it again. Which one accepts the decimal?

```python exec
id: what-input-gives-back-7
amount = int(input("Amount: "))
print(amount + 1)
```

```typed
3
```

```solution
for: what-input-gives-back-7
title: one way to do it
amount = float(input("Amount: "))
print(amount + 1)
```

**1.8** Run this three times. Type `12` the first time, press Enter without typing the second time, and type `twelve` the third time. What does each error say?

```python exec
id: what-input-gives-back-8
age = int(input("Age: "))
print(age)
```

```typed
12
```

**1.9** Run this and type your name with spaces before and after it. What does `strip` change?

```python exec
id: what-input-gives-back-9
typed_name = input("Name: ")
print(len(typed_name))
print(len(typed_name.strip()))
```

```typed
  Sam  
```

## 2. Reading a line from the inside out

A line such as `age = int(input("Age: "))` holds a call inside a call. Python works from the inside out. First `input` asks and hands back text. Then `int` turns the text into a number. Last of all, `=` attaches the name `age`.

**2.1** For each line, say which call happens first and which happens last. Then run the cell with the answers `2.5`, `banana` and `7`.

```python exec
id: reading-a-line-from-the-inside-out-1
width = float(input("Width: "))
print(len(input("Word: ")))
print(int(input("Number: ")) * 2)
```

```typed
2.5
banana
7
```

**2.2** Rewrite the three lines from 2.1 so that each line makes only one call. Store each result under a name before the next step uses it.

```python exec
id: reading-a-line-from-the-inside-out-2
# your code here
```

```typed
2.5
banana
7
```

```solution
for: reading-a-line-from-the-inside-out-2
title: one way to do it
width_text = input("Width: ")
width = float(width_text)
word = input("Word: ")
length = len(word)
print(length)
number_text = input("Number: ")
number = int(number_text)
print(number * 2)
```

**2.3** Run this and read the error. Count the opening and closing brackets.

```python exec
id: reading-a-line-from-the-inside-out-3
size = int(input("Size: ")
print(size)
```

```typed
4
```

```solution
for: reading-a-line-from-the-inside-out-3
title: one way to do it
size = int(input("Size: "))
print(size)
```

**2.4** A call has a name, brackets, and arguments inside the brackets, separated by commas. Some arguments carry a name of their own, such as `sep=` and `end=` for `print`. Find the name and the arguments of each call here, and then run the cell.

```python exec
id: reading-a-line-from-the-inside-out-4
print("a", "b", "c", sep="-")
print("one", end=" ")
print("two")
print(max(3, 9, 4))
print(round(3.14159, 2))
```

**2.5** Run this. What does `print` hand back when it has finished?

```python exec
id: reading-a-line-from-the-inside-out-5
result = print("hi")
print(result)
```

## 3. Small programs

**3.1** Ask for two whole numbers and print their sum.

```python exec
id: small-programs-1
# your code here
```

```typed
3
4
```

```solution
for: small-programs-1
title: one way to do it
a = int(input("First: "))
b = int(input("Second: "))
print(a + b)
```

**3.2** Ask for a radius and print the area of a circle with two digits after the decimal point. Use 3.14159 for pi.

```python exec
id: small-programs-2
# your code here
```

```typed
2
```

```solution
for: small-programs-2
title: one way to do it
radius = float(input("Radius: "))
print(f"{3.14159 * radius ** 2:.2f}")
```

**3.3** Ask for a number of minutes and print it as hours and minutes. For 135 the program should say 2 hours and 15 minutes.

```python exec
id: small-programs-3
# your code here
```

```typed
135
```

```solution
for: small-programs-3
title: one way to do it
minutes = int(input("Minutes: "))
print(minutes // 60, "hours and", minutes % 60, "minutes")
```

**3.4** Ask for a name, an animal and a food, and print a sentence that uses all three.

```python exec
id: small-programs-4
# your code here
```

```typed
Ada
cat
toast
```

```solution
for: small-programs-4
title: one way to do it
name = input("A name: ")
animal = input("An animal: ")
food = input("A food: ")
print(f"{name} met a {animal} that was eating {food}.")
```

**3.5** Ask for an age in years and print roughly how many days old that is. Ignore leap years.

```python exec
id: small-programs-5
# your code here
```

```typed
15
```

```solution
for: small-programs-5
title: one way to do it
years = int(input("Age in years: "))
print(years * 365, "days old")
```

**3.6** Ask for a bill and a tip percentage. Print the tip and the total, each with two digits after the decimal point.

```python exec
id: small-programs-6
# your code here
```

```typed
42.50
15
```

```solution
for: small-programs-6
title: one way to do it
bill = float(input("Bill: "))
percent = float(input("Tip percent: "))
tip = bill * percent / 100
print(f"Tip: {tip:.2f}")
print(f"Total: {bill + tip:.2f}")
```

**3.7** Ask for a name and print it inside a box that fits the name, like the one below for `Sam`.

```
+-----+
| Sam |
+-----+
```

```python exec
id: small-programs-7
# your code here
```

```typed
Sam
```

```solution
for: small-programs-7
title: one way to do it
name = input("Name: ")
border = "+" + "-" * (len(name) + 2) + "+"
print(border)
print("| " + name + " |")
print(border)
```

**3.8** Ask for an amount in cents. Print how many 50c, 20c, 10c and 5c coins make it up, using as many large coins as possible, and print the cents left over.

```python exec
id: small-programs-8
# your code here
```

```typed
187
```

```solution
for: small-programs-8
title: one way to do it
cents = int(input("Cents: "))
print(cents // 50, "coins of 50c")
cents = cents % 50
print(cents // 20, "coins of 20c")
cents = cents % 20
print(cents // 10, "coins of 10c")
cents = cents % 10
print(cents // 5, "coins of 5c")
print(cents % 5, "cents left over")
```

## 4. Looking back

**4.1** Write down three things a person could type that would make `int(input())` fail.

**4.2** Explain why `input() + input()` joins the two answers instead of adding them.
