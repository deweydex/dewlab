---
title: "Storing and Computing"
slug: storing-and-computing
module: mit-pdp-maths-prog-integration
module_title: "Programming and Maths, Integrated"
year: "2026-2027"
series: maths-and-programming
version: 1
covers:
  variables-giving-names-to-things:
    covers: [PDP-LO4, PDP-LO11]
  data-types-different-kinds-of-information:
    covers: [PDP-LO4]
  type-conversion:
    covers: [PDP-LO4]
  number-systems-how-computers-count:
    covers: [MIT-1.4]
  putting-it-together-a-small-program:
    covers: [PDP-LO7]
---

# Storing and Computing

**Programming Design Principles / Maths for IT**

Last time we learned to do arithmetic and display results. But we had a limitation: every time we calculated something, it was gone. If we wanted to use the result again, we would have to recalculate it. Today we learn to *store* information using variables, and we will explore the different types of data Python can work with.

Along the way, we will start thinking about how computers represent numbers -- which turns out to be quite different from how we write them on paper.

## Variables: Giving Names to Things

A variable is a name that refers to a value. You create one with the `=` sign, which in programming means "assign this value to this name" (not "is equal to" as in mathematics -- that distinction will matter later).

```python exec
id: variables-giving-names-to-things-1
# Creating variables
age = 25
name = "Ada"
temperature = 18.5
is_raining = False

# Using them
print(name)
print(age)
print(temperature)
```

We now have four variables, each holding a different kind of data. Notice that we did not have to declare what kind of data each variable would hold -- Python figures that out from the value we assign. This is one of the things that makes Python pleasant to work with.

Variable names should describe what they contain. `temperature` is a good name; `t` is not, because someone reading your code (including future you) would not know what `t` refers to. This is not just a style preference -- it is a professional practice that makes code maintainable.

Names must start with a letter or underscore, can contain letters, numbers, and underscores, and are case-sensitive (`Age` and `age` are different variables). By convention in Python, we use `snake_case` for variable names: lowercase words separated by underscores.

### Your turn

Create variables to store the following information about yourself (or make something up): your first name, your age, the number of years you have been using computers, and whether you have programmed before (True or False). Then print each one with a descriptive label.

```python exec
id: your-turn-1
# Your variables here
```

## Data Types: Different Kinds of Information

Python has several built-in data types. The ones we will use most are:

**Integers** (`int`): whole numbers like 42, -7, 0. These correspond to the mathematical integers, which mathematicians call **Z** (from the German word *Zahlen*, meaning numbers). Integers extend in both directions from zero: ..., -3, -2, -1, 0, 1, 2, 3, ...

**Floating-point numbers** (`float`): numbers with a decimal point like 3.14, -0.5, 2.0. These approximate the real numbers (**R**), though they cannot represent every real number exactly (more on this in a moment).

**Strings** (`str`): text enclosed in quotes like "hello" or 'world'. Single or double quotes both work.

**Booleans** (`bool`): either `True` or `False`. Named after George Boole, who developed the algebra of logic in the 1850s.

You can check what type a value has using the `type()` function:

```python exec
id: data-types-different-kinds-of-information-1
print(type(42))
print(type(3.14))
print(type("hello"))
print(type(True))
```

### Where I might get stuck

A common source of confusion: `"42"` (with quotes) is a string, not a number. Python sees it as text that happens to contain digit characters. You cannot do arithmetic with it. This distinction matters enormously.

```python exec
id: where-i-might-get-stuck-1
# This works fine
print(40 + 2)

# This does something unexpected
print("40" + "2")
```

The `+` operator behaves differently depending on the types involved. For numbers, it adds. For strings, it *concatenates* (joins them end to end). This is why types matter.

### Your turn

Before running the next cell, predict what each line will output. Then run it and check.

```python exec
id: your-turn-2
# Predict, then verify
print(type(7))              # prediction: 
print(type(7.0))            # prediction: 
print(type("7"))            # prediction: 
print(type(True))           # prediction: 
print(type(7 + 0.5))        # prediction: 
print("3" + "4")            # prediction: 
print(3 + 4)                # prediction: 
```

## Type Conversion

Sometimes we need to convert between types. Python gives us functions for this: `int()`, `float()`, `str()`, and `bool()`.

```python exec
id: type-conversion-1
# Converting between types
x = "42"
print(type(x))          # str

y = int(x)              # convert string to integer
print(type(y))          # int
print(y + 8)            # now we can do arithmetic: 50

z = float("3.14")       # string to float
print(z * 2)            # 6.28

w = str(100)            # integer to string
print("The answer is " + w)
```

This becomes especially important when we get input from the user, because the `input()` function always returns a string -- even if the user types a number.

```python exec
id: type-conversion-2
# Getting input from the user
# Uncomment these lines to try them (they will wait for you to type something)

# user_name = input("What is your name? ")
# print("Hello, " + user_name)

# user_age = input("How old are you? ")
# print(type(user_age))          # it's a string!
# user_age = int(user_age)       # now it's an integer
# print("Next year you will be", user_age + 1)
```

## Number Systems: How Computers Count

We count in base 10 (decimal), using digits 0-9. This is probably because we have ten fingers. But there is nothing special about base 10 -- you can build a perfectly good number system with any base.

Computers use base 2 (binary), because their fundamental building blocks (transistors) have two states: on and off, 1 and 0.

In decimal, the number 42 means: `4 tens + 2 ones`, or `4 x 10^1 + 2 x 10^0`.

In binary, the number 101010 means: `1x32 + 0x16 + 1x8 + 0x4 + 1x2 + 0x1 = 42`.

Each position is a power of 2 instead of a power of 10.

```python exec
id: number-systems-how-computers-count-1
# Python can work with binary directly
print(0b101010)       # 0b prefix means "this is binary"
print(bin(42))        # bin() converts to a binary string

# And hexadecimal (base 16), which uses digits 0-9 and letters A-F
print(0x2A)           # 0x prefix means "this is hexadecimal"
print(hex(42))        # hex() converts to a hex string

# Let's verify that binary conversion by hand
print(1*32 + 0*16 + 1*8 + 0*4 + 1*2 + 0*1)
```

Hexadecimal is popular because each hex digit corresponds to exactly four binary digits, making it a compact way to write binary. The hex digit `A` is 1010 in binary, `F` is 1111, and so on.

### Your turn

Convert these numbers by hand first (write your working in comments), then verify with Python:

1. What is the decimal value of binary `11001`?
2. What is the binary representation of decimal 100?
3. What is the hex representation of decimal 255?

```python exec
id: your-turn-3
# Work through the conversions by hand, then verify
# 1. Binary 11001 = ?
#    Working: 

# 2. Decimal 100 in binary = ?
#    Working: 

# 3. Decimal 255 in hex = ?
#    Working: 

# Verification:
```

## Putting It Together: A Small Program

Let's write a program that brings together everything from this tutorial. We will make a converter that takes a temperature in Celsius and converts it to Fahrenheit, with properly named variables and clear output.

### First, the pseudocode

```
STORE the temperature in Celsius
CALCULATE Fahrenheit using the formula: (celsius * 9/5) + 32
DISPLAY the result with a clear label
```

### Now the implementation

```python exec
id: now-the-implementation-1
# Temperature converter
celsius = 20

# The conversion formula
fahrenheit = (celsius * 9 / 5) + 32

# Display the result
print("Temperature conversion:")
print(str(celsius) + " degrees Celsius = " + str(fahrenheit) + " degrees Fahrenheit")
```

### Your turn

Write a small program that converts between two units of your choice. Some ideas: kilometres to miles (multiply by 0.621371), kilograms to pounds (multiply by 2.20462), or euros to another currency. Follow the same pattern: pseudocode first, then implementation, then test with a few values you can verify by hand.

Start with the pseudocode, written as comments at the top of the cell below,
then fill in the Python underneath each step.

```python exec
id: your-turn-4
# Your converter here
```

```python exec
id: your-turn-5
# Test it with a few values
```

## Reflection

We covered a lot of ground today: variables, data types (int, float, str, bool), type conversion, user input, and the binary and hexadecimal number systems.

The key idea is that *types matter*. The same symbols can mean different things depending on context -- `+` adds numbers but concatenates strings, `"42"` looks like a number but is text. Being precise about types is one of the things that separates clear thinking from fuzzy thinking, in programming and in mathematics.

Write a few sentences about what you found most interesting or most confusing:
