---
title: "Writing your own functions — Practice"
practice_for: writing-your-own-functions
year: "2026-2027"
version: 2026.09.26.1
worlds:
  secret-messages: Codes and hidden messages, the kind spies and puzzle-setters make.
  pixel-art: Pictures made of small squares, the way a screen draws them.
---

# Writing your own functions — Practice

Problems on functions, and three from earlier pages. Where a problem gives
you cases to try, write what you think each one gives in the guess column
first, then try them on your code.

## 1. Three ways to write wave

What does each of these print?

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

(a) Nothing: a `def` only tells Python what `wave` means. (b) `Hi!` twice,
once for each call. (c) The function does not run. Without brackets,
`wave` is the name of the function, not a call to it. On this site a cell
whose last line is a value on its own shows that value, so you may see
something like `<function wave at 0x...>`: Python describing the function
itself. The brackets are what make it run.

</details>

## 2. The wrong number of arguments

```python exec
id: defining-and-calling-1
def describe_pet(pet_name, animal):
    print(pet_name + " is a " + animal + ".")

describe_pet("Tom", "cat")
```

What happens with `describe_pet("cat", "Tom")`? With `describe_pet("Tom")`?
And `describe_pet("Tom", "cat", "grey")`? Try them.

<details class="dl-answer"><summary>answer</summary>

`cat is a Tom.`, then two errors:
`TypeError: describe_pet() missing 1 required positional argument:
'animal'`, and `TypeError: describe_pet() takes 2 positional arguments but
3 were given`. Arguments are matched to parameters by position, so the
order matters and the number must match. Both messages name the function,
and the first even names the parameter that got nothing.

</details>

## 3. Called too soon

What happens here, and why?

```python
shout("hello")

def shout(word):
    print(word + "!")
```

<details class="dl-answer"><summary>answer</summary>

`NameError: name 'shout' is not defined`. Python runs a program from the
top down, and on the first line the `def` has not run yet. Put the `def`
first, and the call after it.

</details>

## 4. Countdown

Can you write `countdown(start)`, which prints the whole numbers from
`start` down to 1, one on each line, and then `Go!`?

```python exec
id: countdown-1
def countdown(start):
    ...

countdown(3)
```

```hint
`range` can count down with a step of −1. Where does it stop, given that
it never includes its stop value? And how far in should the `Go!` line be
indented?
```

```solution
def countdown(start):
    for n in range(start, 0, -1):
        print(n)
    print("Go!")

countdown(3)
---
The stop value is 0, so the loop reaches 1. If `print("Go!")` lines up
with `print(n)`, it becomes part of the loop, and `Go!` appears after
every number.
```

## 5. Is it even

Can you write `is_even(n)`, which returns `True` when `n` is even and
`False` when it is not?

```python exec
id: is-it-even-1
def is_even(n):
    ...
```

```inputs
guess: yes
is_even(4)
is_even(7)
is_even(0)
is_even(-2)
```

```solution
def is_even(n):
    return n % 2 == 0
---
`n % 2 == 0` is already `True` or `False`, so the function can return it
as it is. An `if` with `return True` and `return False` works too; this
says the same thing in one line.
```

## 6. Factorial

Can you write `factorial(n)`, which returns $n!$? What should `factorial(0)`
give?

```python exec
id: factorial-1
def factorial(n):
    ...
```

```inputs
guess: yes
factorial(5)
factorial(1)
factorial(0)
```

```hint
It is an accumulator that multiplies. What should it start at? And what
does your function return when the loop runs zero times?
```

```solution
def factorial(n):
    result = 1
    for i in range(2, n + 1):
        result = result * i
    return result
---
`factorial(0)` gives 1: the loop does not run, and the function returns
the starting value. Mathematicians define $0!$ as 1 too, which is one
reason to start the accumulator at 1.
```

## 7. Found, or not found

This function asks whether `n` has a factor between 2 and `n - 1`. Before
you try the cases, write what you think each gives.

```python exec
id: found-or-not-found-1
def has_factor(n):
    for d in range(2, n):
        if n % d == 0:
            return True
    return False
```

```inputs
guess: yes
has_factor(9)
has_factor(7)
has_factor(2)
```

<details class="dl-answer"><summary>why</summary>

`True` for 9, `False` for 7, and `False` for 2. For 9, the loop tries 2,
then 3, and 9 divides by 3, so the function returns `True` and stops. For
7, nothing from 2 to 6 divides it, so the loop ends and the last line
returns `False`. For 2, `range(2, 2)` is empty, so the function goes
straight to `return False`.

</details>

## 8. One step too far in

Somebody wrote `has_factor` with the last line indented one step further,
inside the loop. Can you find what goes wrong, and fix it?

```python exec
id: one-step-too-far-in-1
def has_factor(n):
    for d in range(2, n):
        if n % d == 0:
            return True
        return False
```

```inputs
guess: yes
has_factor(9)
has_factor(15)
has_factor(7)
```

```solution
def has_factor(n):
    for d in range(2, n):
        if n % d == 0:
            return True
    return False
---
Indented inside the loop, `return False` runs on the first number that
does not divide, so 9 looked as if it had no factor after trying only 2.
"Found it" can be answered inside the loop, but "not found" only after the
loop has tried everything.
```

## 9. Half of ten

```python exec
id: half-of-ten-1
def half(n):
    print(n / 2)

result = half(10)
print(result)
```

```predict
type: text

What will the last line print?
```

<details class="dl-answer"><summary>why</summary>

`5.0`, then `None`. The first line comes from the `print` inside the
function. The function has no `return`, so it gives back `None`, and that
is what `result` holds.

</details>

## 10. Print a print

```python exec
id: print-a-print-1
print(print("hi"))
```

```predict
type: text

What will the last line print?
```

<details class="dl-answer"><summary>why</summary>

`hi`, then `None`. Python works out the inner call first: `print("hi")`
shows `hi`, and, like every function without a `return` value, gives back
`None`. The outer `print` then shows that `None`. `print` is a function
whose job is to show things. It does not give anything back.

</details>

## 11. Two rooms

Can you change `floor_area` so that
`floor_area(4, 3) + floor_area(5, 2)` gives the total floor area of two
rooms?

```python exec
id: two-rooms-1
def floor_area(length, width):
    print(length * width)
```

```inputs
guess: yes
floor_area(4, 3) + floor_area(5, 2)
```

```solution
def floor_area(length, width):
    return length * width
---
22. With `print`, each call shows its own area and gives back `None`, and
`None + None` stops with a `TypeError`. A function that returns its answer
can be part of a bigger calculation.
```

## 12. Which are pure

A *pure function* depends only on its arguments: the same input always
gives the same output, and it changes nothing outside itself. Which of
these are pure?

- (a) `def double(x): return x * 2`
- (b) `def price_with_tax(price): return price * (1 + tax_rate)`, where
  `tax_rate` is a variable outside the function
- (c) `def roll(): return random.randint(1, 6)`, where
  `random.randint(1, 6)` gives a random whole number from 1 to 6
- (d) `def area(r): return 3.14159 * r * r`

<details class="dl-answer"><summary>answer</summary>

(a) and (d). (b) depends on `tax_rate`, outside the function, so changing
it changes the answer for the same price. (c) gives a different answer
each time. A change a function makes outside itself, such as printing or
changing a variable elsewhere, is called a *side effect*. Pure functions
are the easiest to test, but the others are needed too: a dice game needs
`roll`.

</details>

## 13. Its own inverse

Some functions undo themselves: doing them twice gets you back where you
started.

<div class="dl-world" data-world="secret-messages">

Can you write `reverse(message)`, which returns the message backwards? Then
what is `reverse(reverse("OTTER"))`?

```python exec
id: its-own-inverse-1--secret-messages
def reverse(message):
    ...
```

```inputs
guess: yes
reverse("RETTO")
reverse(reverse("OTTER"))
reverse("")
```

```solution
def reverse(message):
    backwards = ""
    for letter in message:
        backwards = letter + backwards
    return backwards
---
Turning a message round twice puts it back as it was, so `reverse` is its
own inverse. ROT13, a Caesar shift of 13, is another: 13 and 13 make the
whole 26.
```

</div>

<div class="dl-world" data-world="pixel-art">

A photo negative turns each brightness `b`, from 0 to 255, into `255 - b`.
Can you write `invert(brightness)`? Then what is `invert(invert(200))`?

```python exec
id: its-own-inverse-1--pixel-art
def invert(brightness):
    ...
```

```inputs
guess: yes
invert(0)
invert(200)
invert(invert(200))
```

```solution
def invert(brightness):
    return 255 - brightness
---
Black becomes white, and white black. Inverting twice gives back the
brightness you started with, so `invert` is its own inverse.
```

</div>

## 14. Outside the domain

```python
def reciprocal(x):
    return 1 / x
```

Which input is outside this function's domain? What happens if you call it
with that input?

<details class="dl-answer"><summary>answer</summary>

0: `reciprocal(0)` stops with `ZeroDivisionError: division by zero`. When a
function has an input it cannot handle, it is worth deciding on purpose
what should happen.
[Designing and testing good functions](tutorial:building-reusable-tools)
comes back to such inputs, called edge cases.

</details>

## 15. Counting primes

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

Why does `is_prime` need the line `if n < 2`? Then can you use `is_prime`
to count the primes below 50?

```python exec
id: counting-primes-1
count = 0

print(count)
```

```inputs
count
```

```solution
count = 0
for n in range(1, 50):
    if is_prime(n):
        count = count + 1
print(count)
---
15: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43 and 47. Without
`if n < 2`, `is_prime(1)` would say `True`, because `range(2, 1)` is empty
and `has_factor(1)` finds nothing. But 1 is not a prime.
```

## 16. Distance on a screen

Two pixels are at `(x1, y1)` and `(x2, y2)`. The distance between them is
Pythagoras again: the square root of the difference across, squared, plus
the difference down, squared. Can you write `distance(x1, y1, x2, y2)`?

```python exec
id: distance-on-a-screen-1
def distance(x1, y1, x2, y2):
    ...
```

```inputs
guess: yes
distance(0, 0, 3, 4)
distance(1, 1, 4, 5)
distance(2, 3, 2, 3)      # the same pixel
```

```solution
def distance(x1, y1, x2, y2):
    across = x2 - x1
    down = y2 - y1
    return (across ** 2 + down ** 2) ** 0.5
---
Naming `across` and `down` makes the line with Pythagoras in it read like
the formula.
```

## 17. Two answers at once

Can you write `divide_with_remainder(a, b)`, which returns two values: how
many whole times `b` goes into `a`, and what is left over?

```python exec
id: two-answers-at-once-1
def divide_with_remainder(a, b):
    ...
```

```inputs
guess: yes
divide_with_remainder(17, 5)
divide_with_remainder(5, 17)
```

```solution
def divide_with_remainder(a, b):
    return a // b, a % b
---
A comma between the two values returns both. The caller can keep them
under two names at once: `times, left_over = divide_with_remainder(17, 5)`.
Python's own `divmod(17, 5)` does the same job.
```

## 18. A count inside and outside

```python exec
id: scope-1
count = 0

def bump():
    count = 10          # a new, local count
    return count

print(bump(), count)
```

```predict
type: text

What will it print?
```

<details class="dl-answer"><summary>why</summary>

`10 0`. The line `count = 10` inside the function made a new variable,
which exists only while the function runs. An assignment inside a function
never changes a variable outside it. If you want a function to change a
value, return the new value, and let the caller keep it.

</details>

## 19. One works, one does not

One of these works, and one stops with an error. Which one, and why?

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
`UnboundLocalError`: "cannot access local variable 'total' where it is not
associated with a value".

A function may *read* a variable from outside, as `greet` reads
`greeting`. But `add` gives `total` a new value, and when a function
assigns to a name anywhere in its body, Python treats that name as local
in the whole function. So on the right of `total = total + n`, Python looks
for a local `total`, and there is none yet. The clear fix is to pass the
value in and return the new one:
`def add(total, n): return total + n`. This one catches out experienced
programmers too.

</details>

## 20. From earlier: how many times round

From *Repeating steps with loops*.

```python exec
id: from-earlier-how-many-times-1
x = 100
steps = 0
while x > 1:
    x = x // 3
    steps = steps + 1
print(steps)
```

```predict
type: number

What will it print?
```

<details class="dl-answer"><summary>why</summary>

4: 100 becomes 33, then 11, then 3, then 1, and the loop stops because 1
is not more than 1.

</details>

## 21. From earlier: the biggest first

From *Making decisions with if, elif and else*. Why does this give `"-"`
for a brightness of 200?

```python
if brightness >= 64:
    pixel = "-"
elif brightness >= 192:
    pixel = "#"
```

<details class="dl-answer"><summary>answer</summary>

Python runs the first path whose condition is `True`. 200 is 64 or more,
so the first path catches it, and the second is never asked. With `>=`,
the biggest threshold goes first.

</details>

## 22. From earlier: two decimal places

From *Variables, data types and text*. What does `f"{2 / 3:.2f}"` give?

<details class="dl-answer"><summary>answer</summary>

`0.67`: the value of `2 / 3`, shown with two decimal places. The value
itself keeps every place; `:.2f` only changes how it is shown.

</details>
