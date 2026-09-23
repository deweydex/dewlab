---
title: "Writing your own functions — Practice"
practice_for: writing-your-own-functions
year: "2026-2027"
version: 2026.09.22.1
---

# Writing your own functions — Practice

The answers are hidden in folds under each problem. Many problems ask
what a piece of code prints. Try to answer on paper first, then copy
the code into a cell and run it to check.

## Defining and Calling

```python exec
id: defining-and-calling-1
def greet(name):
    print("Hello, " + name + "!")


def describe_pet(pet_name, animal):
    print(pet_name + " is a " + animal + ".")


greet("Ada")
describe_pet("Rex", "dog")
```

**1.** What does each of these three pieces of code print?

(a)

```python
def wave():
    print("Hi!")
```

(b)

```python
def wave():
    print("Hi!")

wave()
wave()
```

(c)

```python
def wave():
    print("Hi!")

wave
```

<details class="dl-answer"><summary>answer</summary>

(a) Nothing. A `def` only tells Python what `wave` means. The body runs
when the function is called.

(b) `Hi!` twice, once for each call.

(c) Nothing is printed, and the function does not run. Without brackets,
`wave` is the name of the function, not a call to it. On this site, a
cell whose last line is a value on its own shows that value, so you may
see something like `<function wave at 0x...>`. That is Python describing
the function itself. The brackets are what make it run.

</details>

**2.** Using `describe_pet` from the tools cell, what does each line print?

- (a) `describe_pet("Tom", "cat")`
- (b) `describe_pet("cat", "Tom")`
- (c) `describe_pet("Tom")`
- (d) `describe_pet("Tom", "cat", "grey")`

<details class="dl-answer"><summary>answer</summary>

(a) `Tom is a cat.` (b) `cat is a Tom.`

(c) An error: `TypeError: describe_pet() missing 1 required positional
argument: 'animal'`. (d) An error too: `TypeError: describe_pet() takes
2 positional arguments but 3 were given`.

Arguments are matched to parameters by position, so the order matters
and the number must match. Both error messages name the function, and
(c) even names the parameter that got nothing. That is a lot of help,
if we read it.

</details>

**3.** What happens here? Why?

```python
shout("hello")

def shout(word):
    print(word + "!")
```

<details class="dl-answer"><summary>answer</summary>

`NameError: name 'shout' is not defined`.

Python runs a program from the top down. On the first line, the `def`
has not run yet, so the name `shout` does not exist. Put the `def`
first, and the call after it.

</details>

**4.** Write a function `countdown(start)`. It prints the whole numbers
from `start` down to 1, one on each line, and then prints `Go!`.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Start with the first line: `def countdown(start):`.
2. Inside the function, you need a loop that counts down. `range` can
   count down if you give it a step of -1.
3. Where does the loop stop? Remember that `range` never includes its
   stop value.
4. The `Go!` line comes after the loop, but still inside the function.

**Think about:** how far in should the `print("Go!")` line be indented?
What changes if it is indented as far as the `print` inside the loop?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def countdown(start):
    for n in range(start, 0, -1):
        print(n)
    print("Go!")


countdown(3)
```

This prints 3, 2, 1 and `Go!`, each on its own line.

The stop value is 0, so that the loop reaches 1. If `print("Go!")` is
indented to line up with `print(n)`, it becomes part of the loop, and
`Go!` appears after every number.

</details>

## Giving a Value Back

```python exec
id: giving-a-value-back-2
def sum_up_to(n):
    total = 0
    for i in range(1, n + 1):
        total = total + i
    return total


print(sum_up_to(100))
print(100 * 101 // 2)
```

**5.** Write a function `is_even(n)` that returns `True` when `n` is even,
and `False` when it is not.

<details class="dl-answer"><summary>answer</summary>

```python
def is_even(n):
    return n % 2 == 0
```

`is_even(4)` is `True`, `is_even(7)` is `False`, and `is_even(0)` is
`True`.

You may have written this:

```python
def is_even(n):
    if n % 2 == 0:
        return True
    else:
        return False
```

That works too. But `n % 2 == 0` is already `True` or `False`, so we can
return it as it is.

</details>

**6.** The tools cell has `sum_up_to(n)`. It adds up the whole numbers
from 1 to `n` with a loop. What does it return for 100? For 0? Does it
agree with the formula $\frac{n(n+1)}{2}$?

<details class="dl-answer"><summary>answer</summary>

5050 for 100, and 0 for 0. The formula gives 5050 too.

For 0, `range(1, 1)` holds no numbers, so the loop body never runs, and
the function returns the starting value of `total`, which is 0. The
formula also gives 0. A function and a formula that agree on an awkward
input like 0 is a good sign.

</details>

**7.** Write `factorial(n)`, which returns $n!$. What should `factorial(0)`
give?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. $5! = 1 \times 2 \times 3 \times 4 \times 5$. This is an accumulator,
   like `sum_up_to`, but it multiplies.
2. What should the accumulator start at? Starting at 0 would make every
   answer 0.
3. The loop runs over the numbers to multiply. The `return` comes after
   the loop.

**Think about:** what your function returns when the loop runs zero
times.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def factorial(n):
    result = 1
    for i in range(2, n + 1):
        result = result * i
    return result
```

`factorial(5)` is 120, and `factorial(10)` is 3628800.

`factorial(0)` gives 1. The loop does not run at all, so the function
returns the starting value. Mathematicians also define $0!$ as 1, so the
function agrees with them. That is one reason to start the accumulator
at 1.

</details>

**8.** This function tells us whether `n` has a factor between 2 and
`n - 1`. What does it return for 9, 7 and 2?

```python
def has_factor(n):
    for d in range(2, n):
        if n % d == 0:
            return True
    return False
```

<details class="dl-answer"><summary>answer</summary>

`True` for 9, `False` for 7, and `False` for 2.

For 9, the loop tries 2, then 3. 9 divides by 3, so the function
returns `True` and stops. It never tries 4 or more. For 7, no number
from 2 to 6 divides it, so the loop ends and the last line returns
`False`. For 2, `range(2, 2)` is empty, so the function goes straight to
`return False`.

</details>

**9.** Somebody writes `has_factor` with the last line indented one step
further, inside the loop. What goes wrong? Try `has_factor(9)`.

```python
def has_factor(n):
    for d in range(2, n):
        if n % d == 0:
            return True
        return False
```

<details class="dl-answer"><summary>answer</summary>

`has_factor(9)` now returns `False`, and 9 is 3 times 3.

The loop tries 2 first. 9 does not divide by 2, so the function reaches
`return False` and stops, after checking only one number. Every odd
number now looks as if it has no factor.

The rule: "found it" can be answered inside the loop, but "not found"
can only be answered after the loop has checked everything.

</details>

## Return or Print?

**10.** What does this print?

```python
def half(n):
    print(n / 2)


result = half(10)
print(result)
```

<details class="dl-answer"><summary>answer</summary>

```
5.0
None
```

The first line comes from the `print` inside the function. The function
has no `return`, so it gives back `None`, and that is what `result`
holds.

</details>

**11.** What does `print(print("hi"))` print?

<details class="dl-answer"><summary>answer</summary>

```
hi
None
```

Python works out the inner call first. `print("hi")` shows `hi`, and
like every function without a `return` value, it gives back `None`. The
outer `print` then shows that `None`.

So `print` is a function too, and its job is to show things. It does not
give anything back.

</details>

**12.** A room's floor is a rectangle. This function works out its area:

```python
def floor_area(length, width):
    print(length * width)
```

Change it so that you can work out the total floor area of two rooms,
one 4 by 3 and one 5 by 2, with `floor_area(4, 3) + floor_area(5, 2)`.

<details class="dl-answer"><summary>answer</summary>

```python
def floor_area(length, width):
    return length * width


print(floor_area(4, 3) + floor_area(5, 2))
```

This prints 22.

With the `print` version, each call shows its own area and gives back
`None`, and `None + None` stops with a `TypeError`. A function that
returns its answer can be used inside a bigger calculation. A function
that prints its answer cannot.

</details>

## Input-Output Machines

**13.** A *pure function* depends only on its arguments. The same input
always gives the same output, and it changes nothing outside itself.
Which of these are pure?

- (a) `def double(x): return x * 2`
- (b) `def price_with_tax(price): return price * (1 + tax_rate)`, where
  `tax_rate` is a variable outside the function
- (c) `def roll(): return random.randint(1, 6)`, where
  `random.randint(1, 6)` gives a random whole number from 1 to 6
- (d) `def area(r): return 3.14159 * r * r`

<details class="dl-answer"><summary>answer</summary>

(a) and (d) are pure.

(b) depends on `tax_rate`, which is outside the function. If somebody
changes `tax_rate`, the same price gives a different answer. (c) gives a
different answer each time, even with no input at all.

A pure function has no *side effects*. A side effect is any change a
function makes outside itself, such as changing a variable elsewhere in
the program, or printing to the screen.

Pure functions are easy to test and easy to think about. Their answers
can also be saved and reused, because the answer to the same question
never changes. Still, the goal is to know which kind you are writing.
Functions that are not pure are useful and needed too: a dice game
needs `roll`.

</details>

**14.** Here is a function and its inverse:

```python
def celsius_to_fahrenheit(celsius):
    return celsius * 9 / 5 + 32


def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * 5 / 9
```

What does `fahrenheit_to_celsius(celsius_to_fahrenheit(20))` give? And
what does `celsius_to_fahrenheit(36.6)` give?

<details class="dl-answer"><summary>answer</summary>

`20.0`, and `97.88000000000001`.

The inverse undoes the first function, so we get back to 20. It comes
back as a float, because `/` always gives a float.

The second answer should be 97.88. The tiny extra part at the end comes
from the way a computer stores decimal numbers. Most decimals, such as
36.6, cannot be stored exactly, so a small error can appear in the last
digit. It is not a mistake in the function.

</details>

**15.** Here is a function:

```python
def reciprocal(x):
    return 1 / x
```

Which input is outside its domain? What happens if you call the function
with it?

<details class="dl-answer"><summary>answer</summary>

0. The call `reciprocal(0)` stops with
`ZeroDivisionError: division by zero`.

Every other number works. When a function has an input it cannot
handle, it is worth deciding on purpose what should happen. We come
back to this in [Designing and testing good functions](tutorial:building-reusable-tools),
where such inputs are called edge cases.

</details>

## Functions That Use Other Functions

```python exec
id: functions-that-use-other-functions-2
def has_factor(n):
    for d in range(2, n):
        if n % d == 0:
            return True
    return False


def is_prime(n):
    if n < 2:
        return False
    return not has_factor(n)


print(is_prime(7), is_prime(9), is_prime(1))
```

**16.** The tools cell builds `is_prime` out of `has_factor`. Why does
`is_prime` need the line `if n < 2`? Then use `is_prime` to count the
prime numbers below 50.

<details class="dl-answer"><summary>answer</summary>

`has_factor(1)` returns `False`, because `range(2, 1)` is empty. Without
the extra line, `is_prime(1)` would say `True`. But 1 is not a prime
number. The `if n < 2` line handles 1, and also 0 and negative numbers.

```python
count = 0
for n in range(1, 50):
    if is_prime(n):
        count = count + 1
print(count)
```

There are 15 primes below 50: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31,
37, 41, 43 and 47.

</details>

**17.** Write `sum_of_squares(a, b)`, and then `hypotenuse(a, b)`, which
uses it. Check your function with a triangle whose shorter sides are 5
and 12.

<details class="dl-answer"><summary>answer</summary>

```python
def sum_of_squares(a, b):
    return a ** 2 + b ** 2


def hypotenuse(a, b):
    return sum_of_squares(a, b) ** 0.5


print(hypotenuse(5, 12))
```

This prints 13.0. $5^2 + 12^2 = 25 + 144 = 169$, and the square root of
169 is 13.

</details>

**18.** Write `divide_with_remainder(a, b)`. It returns two values: how
many whole times `b` goes into `a`, and what is left over.

<details class="dl-answer"><summary>answer</summary>

```python
def divide_with_remainder(a, b):
    return a // b, a % b


times, left_over = divide_with_remainder(17, 5)
print(times, left_over)
```

This prints `3 2`: 5 goes into 17 three times, with 2 left over.

If you print `divide_with_remainder(17, 5)` directly, you see `(3, 2)`.
Python shows the two values together, in round brackets.

Python has a built-in function that does the same job: `divmod(17, 5)`
also gives `(3, 2)`.

</details>

## Scope

```python exec
id: scope-1
count = 0

def bump():
    count = 10          # a new, local count
    return count


print(bump(), count)
```

**19.** What does the cell above print? Why is `count` still 0 afterwards?

<details class="dl-answer"><summary>answer</summary>

`10 0`.

The line `count = 10` inside the function created a *new* variable. That
variable exists only while the function is running. An assignment inside
a function never changes a variable outside it, unless you use the word
`global`. If you find you need `global`, that is usually a sign that the
function should return a value instead.

</details>

**20.** What does this print?

```python
def double(n):
    n = n * 2
    return n


n = 5
print(double(n), n)
```

<details class="dl-answer"><summary>answer</summary>

`10 5`.

A parameter is a local variable. When we call `double(n)`, the value 5
goes into the function's own `n`. The line `n = n * 2` changes that
local `n` to 10. The `n` outside the function is a different variable,
and it is still 5.

Using the same name inside and outside a function is allowed. It is
also a common cause of confusion, so choose different names when you
can.

</details>

**21.** One of these works, and one stops with an error. Which one? Why?

```python
greeting = "Hello"

def greet(name):
    return greeting + ", " + name

print(greet("Ada"))
```

```python
total = 0

def add(n):
    total = total + n

add(5)
```

<details class="dl-answer"><summary>answer</summary>

The first works, and prints `Hello, Ada`. The second stops with an
`UnboundLocalError`, with a message like "cannot access local variable
'total' where it is not associated with a value".

A function may *read* a global variable, as `greet` reads `greeting`.
But `add` gives `total` a new value. When a function assigns to a name
anywhere in its body, Python treats that name as local in the whole
function. So on the right of `total = total + n`, Python looks for a
local `total`, and there is none yet.

The clear fix is to pass the value in and return the new one:

```python
def add(total, n):
    return total + n


total = 0
total = add(total, 5)
```

This is a hard one. It trips up experienced programmers too.

</details>
