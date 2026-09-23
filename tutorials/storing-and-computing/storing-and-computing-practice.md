---
title: "Variables, data types and text — Practice"
practice_for: storing-and-computing
year: "2026-2027"
version: 2026.09.22.1
---

# Variables, data types and text — Practice

On this page we practise variables, types, floating-point numbers, and
binary and hexadecimal. Each answer is folded away under its problem.
Try the problem first, then open the answer.

The questions about types are the ones to slow down on. In your first
term, most confusing errors will turn out to come from a value whose type
you did not expect.

## Variables

The cell below is a scratchpad for this section.

```python exec
id: variables-1
# A scratchpad.
a = 3
b = 4
print(a, b, type(a), type(b))
```

**1.** Which of these are allowed as variable names in Python? For the
ones that are not allowed, can you say why?

`total`, `2nd_place`, `first name`, `_hidden`, `class`, `Total`,
`total_2`, `my-name`

<details class="dl-answer"><summary>answer</summary>

Allowed: `total`, `_hidden`, `Total`, `total_2`.

Not allowed:

- `2nd_place`: a name cannot start with a digit.
- `first name`: a name cannot contain a space. Python reads it as two
  separate things.
- `class`: this is a reserved word, which Python keeps for its own use.
- `my-name`: the hyphen is a minus sign, so Python reads it as
  `my - name`.

`Total` is allowed, and it is a different variable from `total`. Mixing
the two up is an easy way to lose time looking for a bug.

</details>

**2.** After these lines run, what is `x`?

```python
x = 5
y = x
x = 10
```

<details class="dl-answer"><summary>answer</summary>

`x` is 10, and `y` is 5.

The line `y = x` copied the value 5 into `y`. Assignment happens once, at
the moment the line runs, so it did not tie `y` to `x`. This is the
difference between `=` in Python and `=` in maths. In an equation,
`y = x` stays true. In Python, it was a single instruction, carried out
once.

</details>

**3.** How could you swap the values of two variables, so that `a` ends
up with what `b` had, and `b` ends up with what `a` had?

<details class="dl-answer"><summary>answer</summary>

```python
a, b = b, a
```

Python can do it in one line. Many other languages need a third
variable. That version is worth knowing too, because it shows what is
happening:

```python
temp = a
a = b
b = temp
```

Without `temp`, the line `a = b` would come first and wipe out the value
of `a` that you still need.

</details>

**4.** Rewrite this code so that a person reading it can tell what it
does.

```python
x = 4.5
y = 12
z = x * y
print(z)
```

<details class="dl-answer"><summary>answer</summary>

Something like this:

```python
hourly_rate = 4.5
hours_worked = 12
pay = hourly_rate * hours_worked
print(pay)
```

The arithmetic is the same, and now the code is easy to read. Names are
the cheapest way to explain your code. They are also the only kind of
explanation that cannot go out of date unless the code changes with it.

</details>

## Types

The cell below prints five values, each with its type.

```python exec
id: types-1
print(7, type(7))
print(7.0, type(7.0))
print("7", type("7"))
print(True, type(True))
print(7 + 0.5, type(7 + 0.5))
```

**5.** What is the type of each of these? `42`, `42.0`, `"42"`, `True`,
`4 / 2`, `4 // 2`, `"4" + "2"`

<details class="dl-answer"><summary>answer</summary>

`int`, `float`, `str`, `bool`, `float`, `int`, `str`.

Most people miss `4 / 2`. In Python, division with `/` always gives a
float, even when the answer is whole: `2.0`, and not `2`.

</details>

**6.** Predict each result, then check.

- (a) `"5" + "3"`
- (b) `5 + 3`
- (c) `"5" * 3`
- (d) `5 * "3"`
- (e) `"5" + 3`

<details class="dl-answer"><summary>answer</summary>

(a) `53`. (b) `8`. (c) `555`. (d) `33333`. (e) An error called a
`TypeError`.

- `+` joins strings, and adds numbers.
- `*` with a string and a whole number repeats the string that many
  times.
- `+` with one string and one number has no clear meaning, so Python
  stops with an error. It does not guess.

Stopping is what you want here. A wrong guess that nobody notices is much
worse than an error. (We look at errors properly in
[Reading an error message](tutorial:reading-an-error-message).)

</details>

**7.** Why does `int("3.7")` fail, when `int(3.7)` works?

<details class="dl-answer"><summary>answer</summary>

`int(3.7)` takes a number and throws away the part after the decimal
point, giving 3.

`int("3.7")` takes a *string* and tries to read it as a whole number.
But "3.7" is not a whole number written down, so there is nothing for
`int()` to read. `float("3.7")` works, and `int(float("3.7"))` gets you
to 3 by doing the two steps in order.

</details>

**8.** What does `int(-3.7)` give? Is that rounding?

<details class="dl-answer"><summary>answer</summary>

−3. No, it is not rounding.

`int()` cuts off the part after the decimal point, which moves the number
towards zero. This is called truncating. Rounding would give −4, and
`round(-3.7)` does give −4. These two operations agree on positive
numbers, but they give different answers for negative ones. A difference
like this can hide in code for months.

</details>

**9.** Predict each result, then check: `bool(0)`, `bool(1)`, `bool(-5)`,
`bool("")`, `bool("False")`.

<details class="dl-answer"><summary>answer</summary>

`False`, `True`, `True`, `False`, `True`.

Zero and empty things are false. Everything else is true.
`bool("False")` is here because it catches people out. `"False"` is a
piece of text that is not empty, so it counts as true. Python does not
read what the text says.

</details>

**10.** A program asks someone to type their age with `input()`, then
adds 1. It prints `251` instead of `26`. What happened?

<details class="dl-answer"><summary>answer</summary>

`input()` always gives back a string, so `"25" + "1"` joined two pieces
of text.

The fix is `int(input(...))`. This changes the text to a number the
moment it arrives, so you do not have to remember to change it
everywhere it is used.

</details>

## Floating Point

```python exec
id: floating-point-1
print(0.1 + 0.2)
print(0.1 + 0.2 == 0.3)
print(abs((0.1 + 0.2) - 0.3) < 1e-9)   # is the gap smaller than 0.000000001?
```

**11.** Why is `0.1 + 0.2 == 0.3` false?

<details class="dl-answer"><summary>answer</summary>

Because 0.1 and 0.2 cannot be stored exactly in binary, in the same way
that one third cannot be written exactly in decimal (0.333…). The
computer stores each one as the nearest number it can. The two small
errors do not cancel out.

The result is 0.30000000000000004. It is wrong in the seventeenth
decimal place. For most uses that does not matter. But it is not equal
to 0.3, and that does matter when you test whether two values are equal.

</details>

**12.** How should you compare two floats, then?

<details class="dl-answer"><summary>answer</summary>

Ask whether they are close enough:

```python
abs(a - b) < 1e-9
```

`abs()` gives the size of a number without its sign, and `1e-9` is
0.000000001.

How close is close enough depends on what the numbers are. Money counted
in cents needs a different limit from distances between stars. There is
no single right answer. Python does have a helper, `math.isclose()`, with
a default limit, but you still need to check that its limit suits your
numbers.

</details>

**13.** Which of these can binary floating point store exactly? `0.5`,
`0.25`, `0.1`, `0.75`, `0.3`

<details class="dl-answer"><summary>answer</summary>

`0.5`, `0.25` and `0.75` are exact. `0.1` and `0.3` are not.

A number is exact in binary when it is a sum of halves, quarters, eighths
and so on. A tenth is not, for the same reason that a third is not exact
in decimal. 10 has a factor of 5, and binary has only 2s to work with.

</details>

## Binary and Hexadecimal

This cell shows 42 in binary, hexadecimal and base 8, and then reads
text written in base 2 and base 16.

```python exec
id: binary-and-hexadecimal-1
number = 42
print(number, bin(number), hex(number), oct(number))   # oct() writes base 8

# int() with a second number reads text written in that base
print(int("101010", 2), int("2A", 16))
```

**14.** Change these binary numbers to decimal by hand, then check:
`1101`, `10000`, `11111`, `10101010`.

<details class="dl-answer"><summary>answer</summary>

13, 16, 31, 170.

Notice that `11111` is 31, and not 32. A row of ones is always one less
than the next power of two. That is why a byte holds 0 to 255, and not 0
to 256.

</details>

**15.** Change these to binary by hand, then check: 6, 12, 100, 255.

<details class="dl-answer"><summary>answer</summary>

110, 1100, 1100100, 11111111.

Notice that 12 is 6 moved one place to the left. Multiplying by two in
binary works the same way as multiplying by ten in decimal: you add a
zero on the end.

</details>

**16.** Change these to hexadecimal: 15, 16, 255, 256, 4095.

<details class="dl-answer"><summary>answer</summary>

F, 10, FF, 100, FFF.

Each hex digit is exactly four binary digits, so FF is eight bits, which
is one byte. This match is the whole reason people use hexadecimal: it
is a short way of writing binary that a person can read.

</details>

**17.** A colour on the web is written `#1E90FF`. What are its red, green
and blue values in decimal?

<details class="dl-answer"><summary>answer</summary>

30, 144, 255.

```python
print(int("1E", 16), int("90", 16), int("FF", 16))
```

There are two hex digits for each colour, and each pair is a number from
0 to 255. This colour is called dodger blue. Web colours use hexadecimal
because three bytes fit into six digits, with no confusion about where
one ends and the next begins.

</details>

**18.** Write a program that takes a hex string like `"2A"` and prints
its value in decimal, without using `int(x, 16)`.

<details class="dl-answer"><summary>answer</summary>

This answer uses a `for` loop, which repeats a step once for each
character. [Repeating steps with loops](tutorial:repeating-yourself) explains
loops properly.

```python
digits = "0123456789ABCDEF"
text = "2A"
total = 0
for character in text.upper():
    total = total * 16 + digits.index(character)
print(total)
```

42. The key step is `total = total * 16 + digit`. It is the general way
to read a number in any base: move everything you have up one place,
then add the new digit. Change the 16 and the list of digits, and the
same program reads binary, or base 7.

</details>

## Putting It Together

**19.** Write a converter that changes a number of minutes into hours
and minutes. Use clear names, and label the output.

<details class="dl-answer"><summary>answer</summary>

```python
total_minutes = 500
hours = total_minutes // 60
minutes = total_minutes % 60
print(f"{total_minutes} minutes is {hours} hours and {minutes} minutes")
```

8 hours and 20 minutes.

The last line uses an f-string, from the tutorial's section *Putting
Values into Text*. Python replaces each name in curly brackets, such as
`{hours}`, with that variable's value.

</details>

**20.** A shop's till stores prices in euro as floats. Adding up fifty
items at €0.10 gives €4.999999999999998. What should the till store
instead?

<details class="dl-answer"><summary>answer</summary>

Whole cents, as integers. Fifty lots of 10 cents is exactly 500. You
divide by 100 only when you display the total.

Real payment systems work this way. The general rule: when a quantity is
made of whole small units, store the whole units. Floats are for
measurements. For counting, use integers.

</details>

**21.** Predict what this prints, then run it.

```python
x = "10"
y = 5
print(x * y)
print(int(x) * y)
print(x + str(y))
print(int(x) + y)
```

<details class="dl-answer"><summary>answer</summary>

`1010101010`, then `50`, then `105`, then `15`.

The same two values give four different answers, and the types decide
every one. That is the main idea of the tutorial, in one cell.

</details>

## Putting Values into Text

This cell shows the same value with an f-string three ways: as it is,
with 2 decimal places, and with 4.

```python exec
id: putting-values-into-text-practice-1
share = 2 / 3
print(f"{share}")
print(f"{share:.2f}")
print(f"{share:.4f}")
```

**22.** Rewrite this line with an f-string. Can you do it without
`str()`?

```python
print("Hello, " + name + ". You are " + str(age) + " years old.")
```

<details class="dl-answer"><summary>answer</summary>

```python
print(f"Hello, {name}. You are {age} years old.")
```

With `name = "Aoife"` and `age = 34`, both lines print `Hello, Aoife.
You are 34 years old.`

The f-string turns `age` into text for you, so `str()` is not needed.
The spaces are easier to see, too, because they sit inside one string.

If you forget the `f`, Python prints the curly brackets and the names
as they are: `Hello, {name}.` There is no error, so this mistake is easy
to miss.

</details>

**23.** Here `share = 2 / 3`. Predict what each line prints, then check.

- (a) `print(f"{share:.2f}")`
- (b) `print(f"{share:.4f}")`
- (c) `print(f"{share:.0f}")`
- (d) `print(f"{5:.2f}")`

<details class="dl-answer"><summary>answer</summary>

(a) `0.67`. (b) `0.6667`. (c) `1`. (d) `5.00`.

Each one rounds to the number of places after the dot. With `.0f` there
are no decimal places, so 0.666… rounds up to 1.

(d) shows that `:.2f` can also add places. A whole number gets `.00`,
which is what you want when you print prices.

</details>

**24.** Problem 20 stored a till's total in whole cents. The total is
`total_cents = 1234`. Print it as `Total: €12.34`.

<details class="dl-answer"><summary>answer</summary>

```python
total_cents = 1234
print(f"Total: €{total_cents / 100:.2f}")
```

Inside the curly brackets, we can write a small calculation as well as a
name. Here Python divides by 100, and then shows the result with 2
decimal places.

The `:.2f` matters when the total is a whole number of euro. With
`total_cents = 500`, the line prints `Total: €5.00`. Without `:.2f`, it
would print `Total: €5.0`, which does not look like a price.

</details>
