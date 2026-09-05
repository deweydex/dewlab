---
title: "Storing and Computing — Practice"
slug: storing-and-computing-practice
practice_for: storing-and-computing
module: mit-pdp-maths-prog-integration
module_title: "Programming and Maths, Integrated"
year: "2026-2027"
series: programming-foundations
version: 2026.08.23.1
---

# Storing and Computing — Practice

Answers are folded. The type questions are the ones worth slowing down on — nearly every confusing error in your first term will turn out to be a type you did not expect.

## Variables

```python exec
id: variables-1
# A scratchpad.
a = 3
b = 4
print(a, b, type(a), type(b))
```

**1.** Which of these are legal variable names in Python? For the illegal ones, say why.

`total`, `2nd_place`, `first name`, `_hidden`, `class`, `Total`, `total_2`, `my-name`

<details class="dl-answer"><summary>answer</summary>

Legal: `total`, `_hidden`, `Total`, `total_2`.

Illegal: `2nd_place` (cannot start with a digit), `first name` (no spaces — Python reads it as two things), `class` (a reserved word Python needs for itself), `my-name` (the hyphen is a minus sign, so Python reads `my - name`).

`Total` is legal and is a different variable from `total`, which is a good way to lose an afternoon.

</details>

**2.** After these lines, what is `x`?

```python
x = 5
y = x
x = 10
```

<details class="dl-answer"><summary>answer</summary>

`x` is 10, and `y` is 5.

The line `y = x` copied the value 5 into `y`. It did not tie `y` to `x` — assignment happens once, at the moment it runs. This is the difference between `=` in Python and `=` in mathematics: in an equation, `y = x` stays true; here it was a one-off instruction.

</details>

**3.** Swap the values of two variables so that `a` ends up with what `b` had and the other way round.

<details class="dl-answer"><summary>answer</summary>

```python
a, b = b, a
```

Python can do it in one line. Every other language needs a third variable, and it is worth knowing that version too because it shows what is actually happening:

```python
temp = a
a = b
b = temp
```

Without the `temp`, writing `a = b` first destroys the value you still needed.

</details>

**4.** Rewrite this so a person reading it can tell what it does.

```python
x = 4.5
y = 12
z = x * y
print(z)
```

<details class="dl-answer"><summary>answer</summary>

Something like:

```python
hourly_rate = 4.5
hours_worked = 12
pay = hourly_rate * hours_worked
print(pay)
```

The arithmetic is identical and the code is now readable. Names are the cheapest documentation there is, and the only kind that cannot fall out of date without the code changing too.

</details>

## Types

```python exec
id: types-1
for value in [7, 7.0, "7", True, 7 + 0.5]:
    print(f"{str(value):<6} is a {type(value).__name__}")
```

**5.** Give the type of each: `42`, `42.0`, `"42"`, `True`, `4 / 2`, `4 // 2`, `"4" + "2"`.

<details class="dl-answer"><summary>answer</summary>

`int`, `float`, `str`, `bool`, `float`, `int`, `str`.

`4 / 2` is the one people miss. Division always gives a float in Python, even when it comes out exactly — `2.0`, not `2`.

</details>

**6.** Predict each, then check.

- (a) `"5" + "3"`
- (b) `5 + 3`
- (c) `"5" * 3`
- (d) `5 * "3"`
- (e) `"5" + 3`

<details class="dl-answer"><summary>answer</summary>

(a) `53`. (b) `8`. (c) `555`. (d) `333`. (e) a `TypeError`.

`+` joins strings and adds numbers. `*` with a string and a whole number repeats it. `+` with one of each has no sensible meaning, so Python refuses rather than guessing — which is the behaviour you want, because guessing wrong silently is much worse than stopping.

</details>

**7.** Why does `int("3.7")` fail when `int(3.7)` works?

<details class="dl-answer"><summary>answer</summary>

`int(3.7)` takes a number and throws away the fractional part, giving 3.

`int("3.7")` takes a *string* and tries to read it as a whole number. It is not a whole number written down, so there is nothing to read. `float("3.7")` works, and `int(float("3.7"))` gets you to 3 by doing the two steps in order.

</details>

**8.** What does `int(-3.7)` give, and is that rounding?

<details class="dl-answer"><summary>answer</summary>

−3, and no, it is not rounding.

`int()` truncates — it cuts towards zero. Rounding would give −4. `round(-3.7)` does give −4. Two different operations that agree on positive numbers and part company on negative ones, which is exactly the kind of thing that hides in code for months.

</details>

**9.** Predict, then check: `bool(0)`, `bool(1)`, `bool(-5)`, `bool("")`, `bool("False")`.

<details class="dl-answer"><summary>answer</summary>

`False`, `True`, `True`, `False`, `True`.

Zero and empty things are false; everything else is true. `bool("False")` catching people out is the point of including it — it is a non-empty piece of text, and Python is not reading what the text says.

</details>

**10.** Someone types their age into `input()` and the program adds 1. It prints `251` instead of `26`. What happened?

<details class="dl-answer"><summary>answer</summary>

`input()` always returns a string, so `"25" + "1"` joined two pieces of text.

The fix is `int(input(...))`, converting the moment it arrives rather than remembering to convert everywhere it is used.

</details>

## Floating Point

```python exec
id: floating-point-1
print(0.1 + 0.2)
print(0.1 + 0.2 == 0.3)
print(abs((0.1 + 0.2) - 0.3) < 1e-9)
```

**11.** Why is `0.1 + 0.2 == 0.3` false?

<details class="dl-answer"><summary>answer</summary>

Because 0.1 and 0.2 cannot be stored exactly in binary, any more than a third can be written exactly in decimal. Each is stored as the nearest number the machine can represent, and the two small errors do not cancel.

The result is 0.30000000000000004 — wrong in the seventeenth decimal place, which does not matter, and unequal to 0.3, which does if you test for equality.

</details>

**12.** How should you compare two floats, then?

<details class="dl-answer"><summary>answer</summary>

By asking whether they are close enough:

```python
abs(a - b) < 1e-9
```

How close is close enough depends on what the numbers are. Money in cents wants a different tolerance from astronomical distances, and there is no universal right answer — which is why Python does not pick one for you.

</details>

**13.** Which of these are exact in binary floating point? `0.5`, `0.25`, `0.1`, `0.75`, `0.3`

<details class="dl-answer"><summary>answer</summary>

`0.5`, `0.25` and `0.75` are exact. `0.1` and `0.3` are not.

A number is exact in binary when it is a sum of halves, quarters, eighths and so on. A tenth is not, for the same reason a third is not exact in decimal — 10 has a factor of 5 and binary only has 2s to work with.

</details>

## Binary and Hexadecimal

```python exec
id: binary-and-hexadecimal-1
n = 42
print(n, bin(n), hex(n), oct(n))
print(int("101010", 2), int("2A", 16))
```

**14.** Convert to decimal by hand, then check: binary `1101`, `10000`, `11111`, `10101010`.

<details class="dl-answer"><summary>answer</summary>

13, 16, 31, 170.

`11111` being 31 rather than 32 is worth holding on to: a run of n ones is one less than the next power of two. That is why a byte holds 0 to 255 and not 0 to 256.

</details>

**15.** Convert to binary by hand, then check: 6, 12, 100, 255.

<details class="dl-answer"><summary>answer</summary>

110, 1100, 1100100, 11111111.

Notice 12 is 6 shifted one place left. Multiplying by two in binary is exactly what multiplying by ten is in decimal — add a zero on the end.

</details>

**16.** Convert to hexadecimal: 15, 16, 255, 256, 4095.

<details class="dl-answer"><summary>answer</summary>

F, 10, FF, 100, FFF.

Each hex digit is exactly four binary digits, so FF is eight bits — one byte. That correspondence is the entire reason hexadecimal is used: it is a shorthand for binary that a person can read.

</details>

**17.** A colour on the web is written `#1E90FF`. What are its red, green and blue values in decimal?

<details class="dl-answer"><summary>answer</summary>

30, 144, 255.

```python
print(int("1E", 16), int("90", 16), int("FF", 16))
```

Two hex digits per channel, each 0 to 255. This is dodger blue, and the notation is hexadecimal precisely because three bytes write as six digits with no ambiguity.

</details>

**18.** Write a program that takes a hex string like `"2A"` and prints its decimal value, without using `int(x, 16)`.

<details class="dl-answer"><summary>answer</summary>

```python
digits = "0123456789ABCDEF"
text = "2A"
total = 0
for character in text.upper():
    total = total * 16 + digits.index(character)
print(total)
```

42. The `total = total * 16 + digit` step is the general method for reading any base: shift everything you have up one place, then add the new digit. Change the 16 and the digit list and it reads binary, or base 7.

</details>

## Putting It Together

**19.** Write a converter that turns a number of minutes into hours and minutes, with clear names and a labelled output.

<details class="dl-answer"><summary>answer</summary>

```python
total_minutes = 500
hours = total_minutes // 60
minutes = total_minutes % 60
print(f"{total_minutes} minutes is {hours} hours and {minutes} minutes")
```

8 hours and 20 minutes.

</details>

**20.** A shop's till stores prices in euro as floats. Adding fifty items at €0.10 gives €4.999999999999998. What should it store instead?

<details class="dl-answer"><summary>answer</summary>

Whole cents, as integers. Fifty lots of 10 cents is exactly 500, and you divide by 100 only when displaying it.

This is what real payment systems do. The general rule: when a quantity is fundamentally whole units of something small, store the whole units. Floating point is for measurements, not for counting.

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

`10101010101010101010`, then `50`, then `105`, then `15`.

Four different answers from the same two values, decided entirely by types. That is the tutorial's point in one cell.

</details>
