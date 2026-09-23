---
title: "Writing your own functions"
year: "2026-2027"
version: 2026.09.22.1
covers:
  defining-a-function:
    covers: [PDP-LO8]
  giving-a-value-back-return:
    covers: [PDP-LO8]
  return-or-print:
    covers: [PDP-LO8]
  functions-as-input-output-machines:
    covers: [MIT-6.2]
    touches: [MIT-3.1]
  functions-that-use-other-functions:
    covers: [PDP-LO8]
  scope-where-variables-live:
    covers: [PDP-LO8]
---

# Writing your own functions

We have already used several functions that Python gives us: `print()`,
`input()`, `int()`, `str()` and `range()`. Each one has a name. Each one
takes something inside its brackets and does a job with it. Some of them
also give something back: `int("42")` gives back the number 42.

Our programs are getting longer, and some pieces of them do the same job
more than once. On this page we write our own functions, so that we can
name a piece of code once and use it as often as we like.

On this page we:

- write functions with `def`, and give them values to work with
- send an answer back with `return`, and see how that is different from
  printing it
- look at a function as a machine that turns an input into an output
- build a function out of other functions
- see where a variable lives: inside a function, or outside it

## Defining a Function

Suppose we want to greet three people. We could write three `print`
lines that are almost the same. Then, if we want to change the greeting,
we have to change it in three places.

A *function* is a named block of code. We define it once. Then we can
*call* it, which means run it, whenever we need it, and give it
different values each time.

```python exec
id: functions-reusable-algorithms-1
def greet(name):
    print("Hello, " + name + "!")

# Now we can call it as many times as we want
greet("Ada")
greet("Grace")
greet("Alan")
```

Here is what each part does:

- The `def` keyword defines a function. Here the function's name is
  `greet`. The line ends with a colon, like an `if` or a `for` line.
- `name` is a *parameter*. A parameter is a placeholder for a value we
  give the function when we call it.
- The indented code under `def` is the *function body*. It runs each
  time we call the function.
- In `greet("Ada")`, the value `"Ada"` is the *argument*. An argument is
  the actual value we pass in. Python puts it into the parameter `name`.

What do you think the next cell prints? Run it to check.

```python exec
id: defining-a-function-1
def cheer():
    print("Well done!")
    print("Keep going!")
```

It prints nothing at all. A `def` teaches Python a new name and what the
name means. It does not run the body. The body runs only when we call
the function, with its name and a pair of brackets. This function has no
parameters, so the brackets stay empty:

```python exec
id: defining-a-function-2
cheer()
cheer()
```

A function can have more than one parameter. We put commas between them,
and pass the same number of arguments, in the same order. Look at the
last line of the next cell. What do you think it prints?

```python exec
id: defining-a-function-3
def describe_pet(pet_name, animal):
    print(pet_name + " is a " + animal + ".")

describe_pet("Rex", "dog")
describe_pet("Tom", "cat")
describe_pet("dog", "Rex")
```

Python matches arguments to parameters by their position. The first
argument goes into the first parameter, and the second into the second.
Python does not know that "Rex" sounds like a name and "dog" sounds like
an animal, so the last line prints `dog is a Rex.`

### Your turn

1. In the cell below, write a function `print_times_table(number)`. It
   prints the times table for `number`, from 1 times `number` up to 10
   times `number`, one line each. Use a `for` loop inside the function.
2. Call it for 7, and then for 12.

```python exec
id: your-turn-1
# Your print_times_table function

# Call it for 7 and 12
```

## Giving a Value Back: return

A function can also *return* a value. To return a value means to send it
back to the code that called the function. Most useful functions return
a value, so that we can keep working with it. What do you think the next
cell prints?

```python exec
id: functions-reusable-algorithms-2
def square(n):
    return n ** 2

result = square(7)
print(result)
print(square(12))
```

The `return` statement sends the value back to the caller. The call
`square(7)` then stands for the value 49, in the same way that
`int("42")` stands for 42. We can store the result, print it, or use it
in more calculations.

A `return` also ends the function straight away. Any lines after it in
the body do not run. Here is a function with two `return` lines. Which
one runs for `larger(5, 5)`?

```python exec
id: giving-a-value-back-1
def larger(a, b):
    if a > b:
        return a
    return b

print(larger(3, 8))
print(larger(10, 2))
print(larger(5, 5))
```

For `larger(10, 2)`, the test `a > b` is True, so the function returns
10 and stops. It never reaches `return b`. For `larger(5, 5)`, the test
is False, so the function goes on to the last line and returns `b`,
which is 5.

### Your turn

1. Write a function called `celsius_to_fahrenheit`. It takes a
   temperature in Celsius and returns the same temperature in Fahrenheit.
   To convert, multiply by 9, divide by 5, then add 32. You can plan it
   in pseudocode first, in the comment lines at the top of the first
   cell.
2. Test it in the second cell with a few values you can check. What
   should 0 and 100 give?

```python exec
id: your-turn-2
# Pseudocode:
#

# Your function
```

```python exec
id: your-turn-3
# Test it
```

## Return or Print?

A function that prints a value and a function that returns a value can
look the same when we run them. They are not the same, and mixing them
up trips up nearly everyone at first.

Here are two functions. How many lines do you think this cell prints:
one, or two? Run it to check.

```python exec
id: return-or-print-1
def double_and_return(n):
    return n * 2

def double_and_print(n):
    print(n * 2)

double_and_return(5)
double_and_print(5)
```

Only one line appears. `double_and_return(5)` did work out 10, and it
gave 10 back. But nothing on that line used the value, so Python threw
it away. `double_and_print(5)` showed 10 on the screen, because `print`
is what puts text on the screen.

Now let's keep what each function gives back, and look at it. What do
you think `a` holds?

```python exec
id: return-or-print-2
a = double_and_print(5)
b = double_and_return(5)
print("a is", a)
print("b is", b)
print("b + 1 is", b + 1)
```

The first line printed 10, because the function body ran. But the
function had no `return`, so it gave nothing back. In Python, "nothing"
is a value of its own. *`None`* is Python's value for "no value here".
A function without a `return` always gives back `None`.

| | `print` inside the function | `return` inside the function |
|---|---|---|
| Who sees the value? | a person, on the screen | the code that called the function |
| Can we store it or calculate with it? | no | yes |
| What does the call give back? | `None` | the value |

So when a function works out an answer, return it. The code that calls
the function can then decide what to do with the answer: print it,
store it, or use it in a bigger calculation.

### Your turn

1. Before you run the cell, predict what happens. Is it a number, or
   an error?
2. Run it. If there is an error, which line does it point to, and what
   type of value does it complain about?
3. Change `add_postage` so that the last line works and prints 48.

```python exec
id: your-turn-4
def add_postage(price):
    print(price + 4)

total = add_postage(20) * 2
print(total)
```

## Functions as Input-Output Machines

In mathematics, a function is a rule that gives *exactly one output* for
each input. For example, $f(x) = x^2$ takes 3 and gives 9. It takes -3
and also gives 9. The important property is this: the same input always
gives the same output.

Our Python functions can work the same way. Look again at `square`:

```python
def square(n):
    return n ** 2
```

This code defines a rule that gives exactly one output for each input.
It is a mathematical function, written in code. An algorithm can be seen
in the same way: a set of steps that takes an input and produces an
output.

Not every Python function is a mathematical function. Some depend on
things outside the function. Others use random numbers. What do you
think this cell prints? Look at the two calls: they have the same input.

```python exec
id: functions-as-input-output-machines-1
discount_rate = 0.10

def with_discount(price):
    return price - price * discount_rate

print(with_discount(50))
discount_rate = 0.25
print(with_discount(50))
```

The same input, 50, gave two different outputs, 45.0 and 37.5. The
answer depends on `discount_rate`, a variable outside the function. So
we cannot know what `with_discount(50)` gives by looking at the call.

A *pure function* is a function whose output depends only on its inputs.
Pure functions are the easiest to understand, to test and to trust, so
they are worth aiming for. Here, we can make `with_discount` pure by
passing the rate in as a second parameter:
`def with_discount(price, rate):`.

In mathematics, the inputs a function is meant to take are called its
*domain*. The domain of `square` is every number. What about a function
that divides by its input? Its domain is every number except 0. When we
write a function, it is worth asking which inputs make sense for it.

### Your turn

A function that undoes another function is called its *inverse*. For
example, taking the square root undoes squaring a positive number.

1. Write `fahrenheit_to_celsius(fahrenheit)`, the inverse of your
   `celsius_to_fahrenheit`. To convert, subtract 32, multiply by 5, then
   divide by 9.
2. Test it: `fahrenheit_to_celsius(212)` should give 100.
3. What do you expect `fahrenheit_to_celsius(celsius_to_fahrenheit(37))`
   to give? Run it to check.

```python exec
id: your-turn-5
# Your fahrenheit_to_celsius function
```

```python exec
id: your-turn-6
# Test it
```

## Functions That Use Other Functions

In the last step of that Your turn, the answer of one function became the
argument of another. A function can also call another function inside
its own body. Look at `sum_of_squares`. How many times does it call
`square`?

```python exec
id: functions-that-use-other-functions-1
def square(n):
    return n ** 2

def sum_of_squares(a, b):
    return square(a) + square(b)

def hypotenuse(a, b):
    return sum_of_squares(a, b) ** 0.5

print(sum_of_squares(3, 4))
print(hypotenuse(3, 4))
```

`sum_of_squares` calls `square` twice. Then `hypotenuse` uses
`sum_of_squares`, and takes the square root with `** 0.5`. This is
Pythagoras' theorem: in a right-angled triangle with sides 3 and 4, the
longest side is 5.

Each function does one small job. We can test each one on its own, and
then build bigger functions out of the ones we trust. If we find a
mistake in `square`, we fix it in one place, and every function that
uses it is fixed too.

A function can also return more than one value. We put a comma between
the values, and the code that calls it can store them in two variables
at once:

```python
def example():
    return 10, 20

a, b = example()   # a gets 10, b gets 20
```

### Your turn

1. In the first cell, write two functions: `circle_area(radius)` and
   `circle_circumference(radius)`. Use 3.14159 for $\pi$. The area is
   $\pi r^2$, and the circumference is $2 \pi r$.
2. Write a third function, `circle_info(radius)`. It calls the other two,
   and returns *both* the area and the circumference.
3. In the second cell, test it with a radius you can check by hand.

```python exec
id: your-turn-7
# Your three circle functions
```

```python exec
id: your-turn-8
# Test circle_info
```

## Scope: Where Variables Live

A variable's *scope* is the part of the program where that variable
exists. A variable we create inside a function has *local scope*: it
exists only while that function is running.

Look at the last line of the next cell. It is a comment, so it does not
run. What do you think would happen if it did run?

```python exec
id: scope-where-variables-live-1
def calculate_area(radius):
    pi = 3.14159
    area = pi * radius ** 2
    return area

result = calculate_area(5)
print(result)

# What happens if this line runs? Delete the # at its start to find out.
# print(area)
```

Try it: delete the `#` at the start of the last line, and run the cell
again. Python stops with a `NameError`. The name `area` does not exist
outside the function.

Local scope helps us. Each function has its own workspace. A variable
inside one function cannot get mixed up with a variable in another
function, even when the two have the same name. A parameter is local
too: `radius` exists only inside `calculate_area`.

A variable we create outside any function has *global scope*: we can
read it from anywhere in the program. `discount_rate`, earlier on this
page, was a global variable. Even so, it is better to pass values into a
function as parameters than to rely on global variables. Then the
function does not depend on anything outside it, so we can move it to
another program and test it on its own.

What happens when a function gives a new value to a name that also
exists outside it? What do you think this cell prints?

```python exec
id: scope-where-variables-live-2
count = 0

def set_count():
    count = 10
    print("inside:", count)

set_count()
print("outside:", count)
```

The line `count = 10` inside the function made a *new*, local variable
called `count`. The global `count` is still 0. Giving a name a value
inside a function never changes a variable outside it. If we want a
function to change a value, the clear way is to return the new value,
and let the caller store it: `count = new_count()`.

### Your turn

1. In the first cell, write two functions. Each one uses a variable
   called `total` inside it, for a different job. For example, one could
   add up the numbers from 1 to `n`, and the other could add up three
   prices given to it as three parameters.
2. In the second cell, set a global variable `total = 1000`. Then call
   both functions and print their results.
3. Print `total` at the end. Is it still 1000? Why?

```python exec
id: your-turn-9
# Two functions that both use 'total' inside them
```

```python exec
id: your-turn-10
# Call both, then print the global total
```

## Reflection

On this page we wrote our own functions. We defined them with `def`,
gave them parameters, and called them with arguments. We sent answers
back with `return`, and saw that returning a value and printing it are
two different things. We saw a function as a machine that turns inputs
into outputs, built functions out of other functions, and found that the
variables inside a function stay inside it.

From now on, when we solve a problem, we will often put the solution
inside a function, so that we can use it again. This is the start of
*modular programming*. Modular programming means building large
programs out of small pieces, each one tested on its own.

Next, in [Lists: keeping many values in order](tutorial:lists-and-sequences), we keep
many values together in one list, and write functions that work with
them.

Which do you find easier to test: a function that prints its answer, or
one that returns it? Why?

## Where to Read More

Python Software Foundation. *The Python Tutorial — Defining Functions.*
<https://docs.python.org/3/tutorial/controlflow.html#defining-functions>.
The official reference for `def`, `return` and parameters. It also shows
default values for parameters, which this page does not cover.

Downey, A. B. (2015). *Think Python: How to Think Like a Computer Scientist*
(2nd ed.). Green Tea Press. Free at <https://greenteapress.com/wp/think-python-2e/>.
Chapter 3 covers defining and calling functions, and chapter 6 covers
functions that return a value, at greater length than this page.
