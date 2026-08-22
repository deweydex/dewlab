---
title: "Making Decisions"
slug: making-decisions
module: mit-pdp-maths-prog-integration
module_title: "Programming and Maths, Integrated"
year: "2026-2027"
series: maths-and-programming
version: 1
covers:
  comparisons-true-or-false:
    covers: [PDP-LO6]
  if-statements-choosing-a-path:
    covers: [PDP-LO6]
  if-else-two-paths:
    covers: [PDP-LO6]
  elif-multiple-paths:
    covers: [PDP-LO6]
  boolean-operators-combining-conditions:
    covers: [PDP-LO6]
    touches: [MIT-2.4]
  classifying-numbers-a-mathematical-application:
    covers: [MIT-1.1]
---

# Making Decisions

**Programming Design Principles / Maths for IT**

So far our programs have been strictly sequential: they execute every line from top to bottom, every time. But real algorithms need to make choices. "If the water has boiled, pour it; otherwise, keep waiting." "If the number is negative, handle it differently." Today we learn how to make our programs choose different paths depending on conditions.

## Comparisons: True or False?

Before we can make decisions, we need to be able to ask questions that have True or False answers. Python gives us comparison operators for this:

```python exec
id: comparisons-true-or-false-1
# Comparison operators
print(5 > 3)        # greater than
print(5 < 3)        # less than
print(5 >= 5)       # greater than or equal to
print(5 <= 4)       # less than or equal to
print(5 == 5)       # equal to (note: two equals signs!)
print(5 != 3)       # not equal to
```

A crucial distinction: `=` is *assignment* (give this name this value), while `==` is *comparison* (are these two things equal?). Mixing them up is one of the most common mistakes in programming.

Each comparison produces a Boolean value: `True` or `False`. These are the building blocks of all decision-making in programs.

### Your turn

Predict the output of each comparison, then run the cell to check:

```python exec
id: your-turn-1
# Predict first, then verify
print(10 > 10)        # prediction: 
print(10 >= 10)       # prediction: 
print("abc" == "abc") # prediction: 
print("abc" == "ABC") # prediction: 
print(1 == 1.0)       # prediction: 
print(0 == False)     # prediction: 
```

That last one is interesting. In Python, `False` is actually equivalent to `0` and `True` is equivalent to `1`. This connection between logic and arithmetic goes all the way back to George Boole's work in the 1850s.

## If Statements: Choosing a Path

The `if` statement lets us execute code only when a condition is True:

```python exec
id: if-statements-choosing-a-path-1
temperature = 35

if temperature > 30:
    print("It's hot today!")
    print("Maybe stay indoors.")

print("This line always runs, regardless of the temperature.")
```

Notice the structure: the `if` keyword, followed by a condition, followed by a colon. The indented lines below are the *body* of the if statement -- they only run when the condition is True. The unindented line after is back to the normal flow and runs no matter what.

Indentation is not optional in Python -- it is how Python knows which code belongs inside the if statement. Use four spaces for each level of indentation (most editors will do this automatically when you press Tab).

### What happens when the condition is False?

If the temperature were 20, the two indented lines would be skipped entirely, and only the final print would run. Try changing the temperature above to see this.

## If-Else: Two Paths

Often we want to do one thing if a condition is True and a different thing if it is False:

```python exec
id: if-else-two-paths-1
number = 7

if number % 2 == 0:
    print(str(number) + " is even")
else:
    print(str(number) + " is odd")
```

The `else` clause catches everything that the `if` condition does not. Between them, they cover all possibilities.

Notice the use of the modulo operator `%` here. If a number divided by 2 has a remainder of 0, it is even. Otherwise it is odd. This is a pattern you will see again and again.

### Your turn

Write a program that takes a variable `year` and prints whether it is a leap year or not. The rule is: a year is a leap year if it is divisible by 4. (There are more detailed rules involving centuries, but let's start simple.)

Pseudocode first, as comments in the cell below — then the Python for each
step underneath it.

```python exec
id: your-turn-2
# Your leap year checker
year = 2024
```

## Elif: Multiple Paths

Sometimes there are more than two possibilities. The `elif` keyword (short for "else if") lets us chain multiple conditions:

```python exec
id: elif-multiple-paths-1
score = 72

if score >= 80:
    grade = "Distinction"
elif score >= 65:
    grade = "Merit"
elif score >= 50:
    grade = "Pass"
else:
    grade = "Unsuccessful"

print("Score: " + str(score) + " -> " + grade)
```

Python checks each condition from top to bottom and executes the first one that is True. Once a matching condition is found, the rest are skipped. This means the order matters: if we checked `score >= 50` first, a score of 90 would match it and get "Pass" instead of "Distinction."

### Your turn

Modify the cell above to try different scores. Make sure you test at least one value in each range, plus the boundary values (50, 65, 80). Boundary testing is where bugs often hide.

Now write your own classifier. Create a program that takes a number and classifies it as positive, negative, or zero:

```python exec
id: your-turn-3
# Pseudocode:
#
#

# Your number classifier
number = -5
```

## Boolean Operators: Combining Conditions

Sometimes a single comparison is not enough. Python provides three Boolean operators for combining conditions: `and`, `or`, and `not`.

**`and`** is True only when *both* conditions are True:

```python exec
id: boolean-operators-combining-conditions-1
age = 25
has_licence = True

if age >= 17 and has_licence:
    print("Can drive")
else:
    print("Cannot drive")
```

**`or`** is True when *at least one* condition is True:

```python exec
id: boolean-operators-combining-conditions-2
day = "Saturday"

if day == "Saturday" or day == "Sunday":
    print("It's the weekend!")
else:
    print("It's a weekday.")
```

**`not`** flips True to False and vice versa:

```python exec
id: boolean-operators-combining-conditions-3
is_raining = False

if not is_raining:
    print("No umbrella needed")
```

These operators follow a precedence order: `not` is evaluated first, then `and`, then `or`. When in doubt, use parentheses to make your intention clear.

### Your turn

Let's revisit the leap year problem with the full rule: a year is a leap year if it is divisible by 4, *except* that years divisible by 100 are not leap years, *unless* they are also divisible by 400.

So 2024 is a leap year (divisible by 4). 1900 is not (divisible by 100 but not 400). 2000 is (divisible by 400).

Write pseudocode first, then implement it:

```python exec
id: your-turn-4
# Pseudocode:
#
#
#

# Full leap year checker
year = 2000
```

```python exec
id: your-turn-5
# Test with several years: 2024, 1900, 2000, 2023, 1600
```

## Classifying Numbers: A Mathematical Application

Let's use our new tools for something that connects to mathematics. Remember the number domains from our last tutorial: natural numbers (N), integers (Z), rationals (Q), and reals (R)?

We can write a program that examines a number and tells us which domains it belongs to. Every natural number is also an integer, which is also a rational, which is also a real -- they are nested like Russian dolls.

```python exec
id: classifying-numbers-a-mathematical-application-1
# Which number families does a value belong to?
value = -3.5

is_real = True                           # everything we can store is real (approximately)
is_rational = True                       # for our purposes, all Python numbers are rational
is_integer = (value == int(value))       # is it a whole number?
is_natural = is_integer and (value >= 0) # is it a non-negative whole number?

print("Value: " + str(value))
print("Natural (N): " + str(is_natural))
print("Integer (Z): " + str(is_integer))
print("Rational (Q): " + str(is_rational))
print("Real (R): " + str(is_real))
```

### Your turn

Try changing the value to different numbers: 7, -3, 0.5, 0, 3.14159. Observe how the classification changes. Then turn this into a proper program using if/elif/else that prints a clean summary like "7 is a natural number (and therefore also an integer, rational, and real)."

**Pseudocode:**

```python exec
id: your-turn-6
# Your number classifier
```

## Reflection

Today we learned to make our programs choose different paths: `if`, `else`, `elif`, and Boolean operators `and`, `or`, `not`. These are *selection structures*, and together with *sequential* execution (which we already knew) they give us two of the three fundamental building blocks of programming. The third -- *iteration* (repetition) -- comes next.

We also saw that the simple act of classifying a number into mathematical categories requires exactly the kind of conditional logic we have been learning. The mathematics and the programming are the same activity viewed from different angles.

What did you find most interesting or challenging today?
