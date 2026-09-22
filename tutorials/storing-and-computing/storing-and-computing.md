---
title: "Storing and Computing"
year: "2026-2027"
version: 2026.09.22.1
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

In [First Steps](tutorial:first-steps) we did arithmetic and displayed
the results. But each result was gone as soon as it was displayed. To use
it again, we had to work it out again. What if Python could remember a
value for us?

On this page we:

- store values under names, so we can use them again
- meet the different types of data Python works with
- change a value from one type to another
- look at how computers write numbers, which is quite different from how
  we write them on paper

## Variables: Giving Names to Things

A *variable* is a name that refers to a value. We make one with the `=`
sign. In programming, `=` means "give this name to this value". This is
different from "is equal to" in maths, and the difference will matter
later.

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
print(is_raining)
```

We now have four variables, and each one holds a different kind of data.
Did you notice that we never told Python what kind of data each one
holds? Python works that out from the value we give it. This is one of
the things that makes Python pleasant to work with.

A variable's name should describe what it holds. `temperature` is a good
name. `t` is a poor one, because someone reading your code would not know
what `t` means, and that someone could be you, a few months from now.
Good names are a professional habit that keeps code easy to change. They
are more than a matter of style.

Python has a few rules for names:

- A name starts with a letter or an underscore (`_`).
- After that, it can contain letters, numbers and underscores.
- Capital letters matter: `Age` and `age` are two different variables.

Python programmers write variable names in *snake_case*. Snake case is
lowercase words joined by underscores, like `is_raining`.

### Your turn

Let's store some information about you. You can make it up if you
prefer.

1. Make a variable for your first name.
2. Make one for your age.
3. Make one for the number of years you have been using computers.
4. Make one for whether you have programmed before: `True` or `False`.
5. Print each one with a label that says what it is.

```python exec
id: your-turn-1
# Your variables here
```

## Data Types: Different Kinds of Information

A *data type*, or type for short, is the kind of data a value is. Python
has several types built in. These are the four we will use most:

| Type | What it holds | Examples |
|---|---|---|
| `int` | whole numbers | `42`, `-7`, `0` |
| `float` | numbers with a decimal point | `3.14`, `-0.5`, `2.0` |
| `str` | text, in quotes | `"hello"`, `'world'` |
| `bool` | true or false | `True`, `False` |

An *integer* (`int`) is a whole number. Integers go on in both
directions from zero: …, -3, -2, -1, 0, 1, 2, 3, … Python's integers
match the integers in maths, which mathematicians call **Z**, from the
German word *Zahlen*, meaning "numbers".

A *floating-point number* (`float`) is a number with a decimal point.
Floats stand in for the real numbers of maths (**R**), but they cannot
store every real number exactly. The practice page for this tutorial has
a section on why.

A *string* (`str`) is a piece of text, written between quotes. Single
quotes and double quotes both work.

A *Boolean* (`bool`) is a value that is either `True` or `False`.
Booleans are named after George Boole, who worked out an algebra of
logic in the 1840s and 1850s.

What type is a value? The `type()` function tells us. Run the cell to
see the four types.

```python exec
id: data-types-different-kinds-of-information-1
print(type(42))
print(type(3.14))
print(type("hello"))
print(type(True))
```

### Where I might get stuck

This one catches out almost everyone at first. `"42"`, with quotes, is a
string. To Python, it is text that happens to contain two digits, and
you cannot do arithmetic with it. Getting this right matters a great
deal.

The cell below adds `40` and `2`, and then `"40"` and `"2"`. What do you
think each line prints? Run it to check.

```python exec
id: where-i-might-get-stuck-1
# This works fine
print(40 + 2)

# This does something unexpected
print("40" + "2")
```

The `+` operator does different things for different types. For numbers,
it adds. For strings, it *concatenates*. To concatenate is to join pieces
of text end to end. This is why types matter.

### Your turn

What will each line print?

1. Write your prediction after `prediction:` on each line.
2. Run the cell.
3. Compare the results with your predictions.

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

Sometimes we need to change a value from one type to another. Python has
a function for each type: `int()`, `float()`, `str()` and `bool()`. Each
one takes a value and gives back that value as its own type.

```python exec
id: type-conversion-1
# Converting between types
text_value = "42"
print(type(text_value))          # str

number_value = int(text_value)   # convert string to integer
print(type(number_value))        # int
print(number_value + 8)          # now we can do arithmetic: 50

decimal_value = float("3.14")    # string to float
print(decimal_value * 2)         # 6.28

number_as_text = str(100)        # integer to string
print("The answer is " + number_as_text)
```

This matters most when a program asks the person using it to type
something. The `input()` function asks for some typing, and gives back
what was typed. It always gives back a string, even when the person
types a number.

The lines in the next cell are comments, so the cell does nothing yet.
To try them, remove the `#` at the start of each line of code, then run
the cell. The cell will wait for you to type something.

```python exec
id: type-conversion-2
# Getting input from the user
# To try these lines, remove the # at the start of each line of code.
# Each input() line waits for you to type something.

# user_name = input("What is your name? ")
# print("Hello, " + user_name)

# user_age = input("How old are you? ")
# print(type(user_age))          # it's a string!
# user_age = int(user_age)       # now it's an integer
# print("Next year you will be", user_age + 1)
```

## Number Systems: How Computers Count

We count in *base 10*, also called decimal. Base 10 uses ten digits,
0 to 9. We probably count in tens because we have ten fingers. But there
is nothing special about ten: you can build a working number system on
any base.

Computers use base 2, also called *binary*. Binary uses only two
digits, 0 and 1. The reason is in the hardware: a computer is built from
tiny switches called transistors, and each one has two states, on and
off.

In decimal, each position in a number is worth a power of 10. The number
42 means 4 tens and 2 ones:

    4 × 10 + 2 × 1  =  42

In binary, each position is worth a power of 2: 1, 2, 4, 8, 16, 32, and
so on. The binary number 101010 means:

    1 × 32 + 0 × 16 + 1 × 8 + 0 × 4 + 1 × 2 + 0 × 1  =  42

Python can write numbers in binary too. The cell below also shows base
16, *hexadecimal*, which uses the digits 0 to 9 and then the letters A to
F. What do you think `print(0b101010)` will show? Run the cell to check.

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

Why do people use hexadecimal? Each hex digit matches exactly four
binary digits, so hexadecimal is a short way to write binary. The hex
digit `A` is 1010 in binary, `F` is 1111, and so on.

### Your turn

Let's convert these numbers by hand first, and then check them with
Python.

1. What is the decimal value of binary `11001`?
2. How do you write decimal 100 in binary?
3. How do you write decimal 255 in hex?

Write your working in the comments in the cell. Then, under
`# Verification:`, use Python to check each answer.

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

Now we can write a program that uses everything on this page. It will
change a temperature in Celsius to Fahrenheit, with clear variable names
and a clear result.

### First, the pseudocode

```
STORE the temperature in Celsius
CALCULATE Fahrenheit using the formula: (celsius * 9/5) + 32
DISPLAY the result with a clear label
```

### Now the implementation

Look at the last line of the cell. Why do you think it needs `str()`
around `celsius` and `fahrenheit`?

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

Now you can write a small program that converts between two units of
your choice. Here are some ideas:

- kilometres to miles: multiply by 0.621371
- kilograms to pounds: multiply by 2.20462
- euros to another currency

Follow the same pattern as the temperature converter:

1. In the first cell, write your pseudocode as comments at the top.
2. Under each comment, write the Python for that step.
3. In the second cell, test your program with a few values you can
   check by hand.

```python exec
id: your-turn-4
# Your converter here
```

```python exec
id: your-turn-5
# Test it with a few values
```

## Reflection

We have met a lot of new ideas on this page: variables, the four data
types (`int`, `float`, `str` and `bool`), type conversion, input from the
user, and the binary and hexadecimal number systems.

The key idea is that *types matter*. The same symbols can mean different
things, depending on the types involved. `+` adds numbers, but it joins
strings. `"42"` looks like a number, but it is text. Being exact about
types is part of thinking clearly, in programming and in maths.

What did you find most interesting on this page, or most confusing? You
could write a few sentences about it.

## Where to Read More

Computerphile (2014). *Floating Point Numbers.*
<https://www.youtube.com/watch?v=PZRI1IfStY0>. Why `float` cannot represent
every number exactly, and why that turns out to matter — the part of this
page that is easiest to skim past.

Python Software Foundation. *The Python Tutorial — An Informal Introduction
to Python.* <https://docs.python.org/3/tutorial/introduction.html>. The
official reference for `int`, `float`, `str` and `bool`, with the exact
rules Python follows for each.

Khan Academy. *The Binary Number System.*
<https://www.khanacademy.org/computing/computers-and-internet/xcae6f4a7ff015e7d:digital-information/xcae6f4a7ff015e7d:binary-numbers/v/the-binary-number-system>.
Slower, worked ground through binary, for anyone who wants a second example
before trying the conversions themselves.
