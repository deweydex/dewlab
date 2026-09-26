---
title: "Writing your own functions"
year: "2026-2027"
version: 2026.09.26.1
worlds:
  secret-messages: Codes and hidden messages, the kind spies and puzzle-setters make.
  pixel-art: Pictures made of small squares, the way a screen draws them.
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

Here is a small program with a secret in it. What will appear under the
cell when you run it?

```python exec
id: defining-a-function-1
def secret():
    print("The password is OTTER")
```

```predict
What will appear under the cell?

- The password is OTTER
  - The `print` line is right there in the cell.
- Nothing
  - `def` gives the steps a name. It does not run them.
- secret
  - This is what you would see if Python printed the name.
```

Nothing appears. `def` teaches Python a new name, `secret`, and what the
name means. It does not run the lines under it. They run only when we
*call* the function, with its name and a pair of brackets:

```python exec
id: defining-a-function-2
secret()
secret()
```

We have used functions Python gives us from the start: `print()`, `int()`,
`len()`, `range()`. Each has a name, takes something inside its brackets,
and does one job. On this page we write our own, so that a piece of code
we need again, like the Caesar shift, gets a name we can call as often as
we like.

## Defining a function

A *function* is a named block of code. We define it once, then call it
whenever we need it, with different values each time.

```python exec
id: functions-reusable-algorithms-1
def greet(name):
    print("Hello, " + name + "!")

greet("Ada")
greet("Grace")
greet("Alan")
```

Try adding a fourth call with your own name, and run it again.

<details class="dl-answer"><summary>What each line does</summary>

- `def greet(name):` defines a function called `greet`. The line ends with
  a colon, like an `if` or a `for` line. Nothing is printed yet.
- The indented `print` line runs each time the function is called, not
  when it is defined.
- `greet("Ada")` calls the function. Python puts `"Ada"` into `name`, and
  runs the indented line.

</details>

`name` is a *parameter*: a placeholder for a value the function will be
given. The indented code under `def` is the *function body*. And the value
in a call, like `"Ada"`, is the *argument*: the actual value passed in,
which Python puts into the parameter.

A function can have more than one parameter, with commas between them, and
we pass the same number of arguments, in the same order. What will the last
line of this cell print?

```python exec
id: defining-a-function-3
def describe_pet(pet_name, animal):
    print(pet_name + " is a " + animal + ".")

describe_pet("Rex", "dog")
describe_pet("dog", "Rex")
```

```predict
type: text

What will the last line print?
```

Python matches arguments to parameters by their position: the first
argument goes into the first parameter. It does not know that "Rex" sounds
like a name, so the last line prints `dog is a Rex.`

### Your turn

<div class="dl-world" data-world="secret-messages">

Can you write a function `print_code_table(shift)`, which prints every
letter of the alphabet beside the letter a Caesar shift moves it to? Then
call it with a shift of 3, and again with 13.

```python exec
id: your-turn-1--secret-messages
# Your print_code_table function

# Call it with 3, then 13
```

```hint
The loop from [Repeating steps with loops](tutorial:repeating-yourself)
that printed the table for a shift of 3 goes inside the function. Where
did it use the number 3?
```

```solution
def print_code_table(shift):
    for position in range(26):
        letter = chr(position + ord("A"))
        moved = chr((position + shift) % 26 + ord("A"))
        print(letter, moved)

print_code_table(3)
print_code_table(13)
---
The 3 became the parameter `shift`, so one function prints the table for
any shift.
```

</div>

<div class="dl-world" data-world="pixel-art">

Can you write a function `draw_square(size)`, which prints a square of `#`,
`size` pixels wide and `size` tall? Then call it with 3, and again with 5.

```python exec
id: your-turn-1--pixel-art
# Your draw_square function

# Call it with 3, then 5
```

```hint
One loop, `size` times round, printing a row. `"#" * size` is a row.
```

```solution
def draw_square(size):
    for row in range(size):
        print("#" * size)

draw_square(3)
draw_square(5)
---
Everything that changes from one square to the next is the parameter,
`size`.
```

</div>

## Giving a value back: return

A function can also *return* a value: send it back to the code that called
it. Most useful functions return a value, so we can keep working with it.

```python exec
id: functions-reusable-algorithms-2
def square(n):
    return n ** 2

result = square(7)
print(result)
print(square(12))
```

The call `square(7)` then stands for the value 49, the same way `int("42")`
stands for 42. We can store it, print it, or use it in more calculations.

A `return` also ends the function straight away. Any lines after it do not
run. Which `return` runs for `larger(5, 5)`?

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

For `larger(10, 2)`, `a > b` is `True`, so the function returns 10 and
stops. For `larger(5, 5)`, it is `False`, so the function continues to the
last line and returns `b`, which is 5.

### Your turn

From here on, a task's cases come with a column for your own guess. Before
you compare your function with a solution, write what you think each call
gives.

<div class="dl-world" data-world="secret-messages">

Can you write `encode(message, shift)`, which returns the message with
every capital letter moved `shift` places along, and anything else, a
space or a full stop, left as it is?

```python exec
id: your-turn-2--secret-messages
def encode(message, shift):
    ...
```

```inputs
guess: yes
encode("HELLO", 3)
encode("ZOO", 1)
encode("HI THERE", 13)    # with a space
encode("", 5)             # an empty message
```

```hint
Start with an empty accumulator, `coded = ""`. Go through the message one
character at a time. A capital gets the shift; anything else is added as it
is. What does the function return at the end?
```

```solution
def encode(message, shift):
    coded = ""
    for character in message:
        if character.isupper():
            position = ord(character) - ord("A")
            coded = coded + chr((position + shift) % 26 + ord("A"))
        else:
            coded = coded + character
    return coded
---
Every piece of this is from an earlier page: the shift, the `if`, the loop,
the accumulator. The function gives them one name.
```

</div>

<div class="dl-world" data-world="pixel-art">

A checkerboard is `#` where the column and the row add up to an even
number, and `.` where they add up to an odd one. Can you write
`checker(x, y)`, which returns the pixel for column `x` and row `y`?

```python exec
id: your-turn-2--pixel-art
def checker(x, y):
    ...
```

```inputs
guess: yes
checker(0, 0)
checker(1, 0)
checker(3, 5)
checker(-1, 0)     # a column off the left edge
```

```hint
`(x + y) % 2` is 0 when the sum is even. Which pixel goes with which?
```

```solution
def checker(x, y):
    if (x + y) % 2 == 0:
        return "#"
    return "."
---
It returns the pixel rather than printing it, so another function can use
it to build a whole picture. That is the next section.
```

</div>

## Return or print?

A function that prints a value and a function that returns a value can
look the same when we run them. They are not the same, and nearly
everyone confuses them at first.

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

Only one line appears. `double_and_return(5)` did calculate 10, and it
returned 10. But nothing on that line used the value, so Python did
nothing with it. `double_and_print(5)` showed 10 on the screen, because `print`
puts text on the screen.

Now let's keep what each function returns, and look at it. What do
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
function had no `return`, so it returned nothing. In Python, "nothing"
is a value of its own. *`None`* is Python's value for "no value here".
A function without a `return` always returns `None`.

| | `print` inside the function | `return` inside the function |
|---|---|---|
| Who sees the value? | a person, on the screen | the code that called the function |
| Can we store it or calculate with it? | no | yes |
| What does the call return? | `None` | the value |

So when a function calculates an answer, return it. The code that calls
the function can then decide what to do with the answer: print it,
store it, or use it in a bigger calculation.

### Your turn

Before you run this cell, is it going to print a number, or stop with an
error? Then, can you change `add_postage` so that the last line prints 48?

```python exec
id: your-turn-4
def add_postage(price):
    print(price + 4)

total = add_postage(20) * 2
print(total)
```

```inputs
total
```

```hint
What does `add_postage(20)` give back? Can `None` be multiplied by 2?
```

```solution
def add_postage(price):
    return price + 4

total = add_postage(20) * 2
print(total)
---
With `print`, the function showed 24 and gave back `None`, so `None * 2`
stopped with a `TypeError`. With `return`, the call stands for 24, and the
last line can use it.
```

## Functions as input-output machines

In mathematics, a function is a rule that gives *exactly one output* for
each input. $f(x) = x^2$ takes 3 and gives 9, and takes −3 and also gives
9. The same input always gives the same output. `square` is a rule like
that, written in code, and so is `encode`. The same message and shift
always give the same code.

Not every Python function works this way. Some depend on things outside the
function. What do you think this cell prints? The two calls have the same
input.

```python exec
id: functions-as-input-output-machines-1
discount_rate = 0.10

def with_discount(price):
    return price - price * discount_rate

print(with_discount(50))
discount_rate = 0.25
print(with_discount(50))
```

The same input, 50, gave 45.0 and then 37.5. The answer depends on
`discount_rate`, a variable outside the function, so we cannot know what
`with_discount(50)` gives by looking at the call. A *pure function* is one
whose output depends only on its inputs. Pure functions are the easiest to
understand, to test and to trust. `with_discount` becomes pure if the rate
is passed in: `def with_discount(price, rate):`.

In mathematics, the inputs a function is meant to take are its *domain*.
The domain of `square` is every number. A function that divides by its
input has every number except 0. When we write a function, we should
ask which inputs make sense for it.

### Your turn

A function that undoes another is called its *inverse*. The square root
undoes the square of a positive number.

<div class="dl-world" data-world="secret-messages">

Can you write `decode(message, shift)`, the inverse of `encode`? It should
move each capital letter `shift` places back. Can you do it by calling
`encode`?

```python exec
id: your-turn-5--secret-messages
def decode(message, shift):
    ...
```

```inputs
guess: yes
decode("KHOOR", 3)
decode(encode("OTTER", 5), 5)
decode("URYYB", 13)
```

```hint
Moving back 3 places is moving forward −3 places. What does
`encode(message, -shift)` do?
```

```solution
def encode(message, shift):
    coded = ""
    for character in message:
        if character.isupper():
            position = ord(character) - ord("A")
            coded = coded + chr((position + shift) % 26 + ord("A"))
        else:
            coded = coded + character
    return coded

def decode(message, shift):
    return encode(message, -shift)
---
`decode` is one line, because `encode` already does the work. (This
solution brings its own `encode` with it, in case yours is not finished.) And
`decode(encode("OTTER", 5), 5)` gives back `OTTER`: the inverse undoes
the function.
```

</div>

<div class="dl-world" data-world="pixel-art">

When we mirror a picture left to right, column 0 goes to the last
column, and the last goes to column 0. For a picture `width` pixels wide, can you write
`mirror(x, width)`, which returns the column that `x` moves to?

```python exec
id: your-turn-5--pixel-art
def mirror(x, width):
    ...
```

```inputs
guess: yes
mirror(0, 8)
mirror(7, 8)
mirror(mirror(3, 8), 8)
```

```hint
In a picture 8 wide, the columns are 0 to 7. Column 0 goes to 7, and
column 1 to 6. What do the two numbers in each pair add up to?
```

```solution
def mirror(x, width):
    return width - 1 - x
---
Mirroring twice puts every column back where it was, so `mirror` is its
own inverse: `mirror(mirror(3, 8), 8)` is 3 again.
```

</div>

## Functions that use other functions

A function can call another function inside its own body. How many times
does `sum_of_squares` call `square`?

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

`sum_of_squares` calls `square` twice. `hypotenuse` then uses
`sum_of_squares`, and takes the square root with `** 0.5`. This is
Pythagoras' theorem. In a triangle with a square corner and sides 3 and 4,
the longest side is 5.

Each function does one small job, so we can test each one on its own, then
build bigger ones out of the ones we trust. If we find a mistake in
`square`, we fix it in one place, and every function that uses it is fixed
too.

### Your turn

<div class="dl-world" data-world="secret-messages">

A code-breaker who does not know the shift can try all 26. Can you write
`try_every_shift(message)`, which prints each shift beside the message
decoded with it, using your `decode`? Try it on `"WKLV LV D VHFUHW"`.

```python exec
id: your-turn-7--secret-messages
def try_every_shift(message):
    ...

try_every_shift("WKLV LV D VHFUHW")
```

```solution
def encode(message, shift):
    coded = ""
    for character in message:
        if character.isupper():
            position = ord(character) - ord("A")
            coded = coded + chr((position + shift) % 26 + ord("A"))
        else:
            coded = coded + character
    return coded

def decode(message, shift):
    return encode(message, -shift)

def try_every_shift(message):
    for shift in range(26):
        print(shift, decode(message, shift))

try_every_shift("WKLV LV D VHFUHW")
---
One line of the 26 reads as English: shift 3, `THIS IS A SECRET`. The
function is three lines because `decode` and `encode` do the rest.
```

</div>

<div class="dl-world" data-world="pixel-art">

Can you write `draw_checkerboard(width, height)`, which returns a whole
checkerboard as one piece of text, using your `checker` for each pixel?
`"\n"` in a string starts a new line.

```python exec
id: your-turn-7--pixel-art
def draw_checkerboard(width, height):
    ...

print(draw_checkerboard(8, 4))
```

```inputs
draw_checkerboard(4, 2)
draw_checkerboard(1, 1)
```

```hint
An accumulator, `picture = ""`. One loop for the rows, and inside it one
for the columns, adding `checker(x, y)` for each pixel. After each row,
add `"\n"`.
```

```solution
def checker(x, y):
    if (x + y) % 2 == 0:
        return "#"
    return "."

def draw_checkerboard(width, height):
    picture = ""
    for y in range(height):
        for x in range(width):
            picture = picture + checker(x, y)
        picture = picture + "\n"
    return picture

print(draw_checkerboard(8, 4))
---
It returns the picture instead of printing it, so a caller can print it,
store it, or change it first. `checker` decides each pixel;
`draw_checkerboard` only puts them in order.
```

</div>

## Scope: where variables live

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
inside one function cannot be confused with a variable in another
function, even when the two have the same name. A parameter is local
too. `radius` exists only inside `calculate_area`.

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

The line `count = 10` inside the function made a new, local variable
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

## Looking back

Which is easier to test: a function that prints its answer, or one that
returns it? Think of the comparison tables on this page. Could they have
shown your answer if the function had only printed it?

A challenge: `try_every_shift` prints 26 lines, and you find the English
one by eye. Can you make the computer pick? Here is one way. English text has
many E's, so the shift whose decoding has the most E's is probably the right one.

```python challenge
# Which shift gives the decoding with the most E's?
def encode(message, shift):
    coded = ""
    for character in message:
        if character.isupper():
            coded = coded + chr((ord(character) - ord("A") + shift) % 26 + ord("A"))
        else:
            coded = coded + character
    return coded

message = "WKH HDJOH KDV ODQGHG DW WKUHH"
best_shift = 0
# Try every shift, count the E's, and keep the best.
print(best_shift, encode(message, -best_shift))
```

From now on, when we solve a problem, we often put the solution inside a
function, so we can use it again. Building large programs out of small,
tested pieces is called *modular programming*. Next,
[Lists and looping over them](tutorial:lists-and-sequences) keeps
many values together, and our functions start to work on whole lists.

## Where to read more

Python Software Foundation. *The Python Tutorial — Defining Functions.*
<https://docs.python.org/3/tutorial/controlflow.html#defining-functions>.
This is the official reference for `def`, `return` and parameters. It also shows
default values for parameters, which this page does not cover.

Downey, A. B. (2015). *Think Python: How to Think Like a Computer Scientist*
(2nd ed.). Green Tea Press. Free at <https://greenteapress.com/wp/think-python-2e/>.
Chapter 3 covers defining and calling functions, and chapter 6 covers
functions that return a value, at greater length than this page.

CrashCourse (2017). *Programming Basics: Statements & Functions: Crash
Course Computer Science #12.*
<https://www.youtube.com/watch?v=l26oaHV7D40>. This video explains
statements, then functions that return a value, in a small game. About eleven minutes.
