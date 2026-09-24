---
title: "Mixed problems: instructions for a machine"
practice_across:
  - four-questions
  - recipes-are-algorithms
  - numbers-a-computer-can-hold
  - everything-is-ones-and-zeros
  - when-python-says-no
year: "2026-2027"
version: 2026.09.24.1
---

# Mixed problems: instructions for a machine

These problems draw on every page of Unit 1, and none of them says which
page it needs. Working that out is part of the problem. When you are not
sure where to start, the four questions are always allowed: what is
named here, what is promised, what happens when, and what does this
space let us do?

Each problem says what kind it is: **Predict** (say what a cell will
print, then run it), **Make** (build something small), **Fix** (repair
one mistake), **Explain** (answer in words) or **Another way** (reach the
same answer by a second route, or find the space where a "wrong" answer
is right). Answers are in the folds.

## Your toolkit

Your toolkit from this unit is loaded on this page: `split_bill`,
`to_binary` and `to_hex`. Run this cell to check that all three are
there. If one of them gives a `NameError`, its page is where to build it.

```python exec
id: mixed-instructions-toolkit-check
print(split_bill(60, 4))
print(to_binary(13))
print(to_hex(255))
```

This cell is a scratchpad for any problem below. Change it as much as you
like.

```python exec
id: mixed-instructions-scratchpad
print(3 * "la ")
```

## Warm-up

**1. Predict.** What does each line print? Say all three answers, then
run them in the scratchpad.

```python
print(3 * "la ")
print(7 // 2)
print(7 / 2)
```

<details class="dl-answer"><summary>answer</summary>

`la la la `, then `3`, then `3.5`.

- `*` with a string writes it out that many times, as on
  [Four questions for any puzzle](tutorial:four-questions).
- `//` divides and keeps only the whole part, an int.
- `/` always gives a float, even when the answer could be whole.

</details>

**2. Another way.** In the counting numbers ℕ, $3 - 5$ has no answer.
Find a space where it does have one, and a place in daily life where you
would meet that answer.

<details class="dl-answer"><summary>answer</summary>

In the integers ℤ, which include the negative whole numbers,
$3 - 5 = -2$. The weather gives one place to meet it: it is 3 °C in the
evening, and by morning the temperature has fallen 5 degrees, to −2 °C.
Python's `print(3 - 5)` gives `-2` as well, because Python's ints are a
space with negative numbers in it.

</details>

**3. Make.** Use your toolkit to write the year 2026 in binary and in
hexadecimal.

<details class="dl-answer"><summary>answer</summary>

```python
print(to_binary(2026))
print(to_hex(2026))
```

This prints `11111101010` and `7EA`. The hex form is much shorter: 11
bits become 3 hex digits, since each hex digit stands for four bits.

</details>

**4. Fix.** This recipe card should print two steps and then `Enjoy!`.
It prints only `Enjoy!`, with no error. Find the mistake and fix it.

```python exec
id: mixed-instructions-pancakes
def make_pancakes(eggs):
    print("Whisk", eggs, "eggs with", eggs * 125, "ml of milk.")
    print("Cook in a hot pan.")


make_pancakes
print("Enjoy!")
```

<details class="dl-answer"><summary>answer</summary>

Line 6 names the function but does not call it. A call needs brackets,
with the value for `eggs` inside them:

```python
make_pancakes(2)
print("Enjoy!")
```

This prints `Whisk 2 eggs with 250 ml of milk.`, `Cook in a hot pan.`
and `Enjoy!`. There was no error, because naming a function without
calling it is allowed. It does nothing, the same way reading a recipe
card's title does not make any pancakes.

</details>

**5. Explain.** A robot is told: "Wash the pan until it is clean." Why is
this a poor step for a robot? Rewrite it as a better one.

<details class="dl-answer"><summary>answer</summary>

"Clean" has no single meaning. One person's clean pan is another
person's dirty one, so two robots could stop at different times, and
one might never stop at all. A good step has one meaning, and a
repeated step needs a clear end.

A better version: "Scrub the pan for 30 seconds. Rinse it. If you can
still see food on it, repeat, at most 5 times." Now every part can be
checked, and the steps must end.

</details>

## Core

**6. Predict.** A taxi costs €4 to start, plus €2 for each kilometre.
What does each line print for a 6 km trip? Which one is the real fare?

```python
print(4 + 2 * 6)
print((4 + 2) * 6)
```

<details class="dl-answer"><summary>answer</summary>

`16`, then `36`.

Python multiplies before it adds, so the first line is
$4 + (2 \times 6) = 4 + 12 = 16$. That is the real fare: the €4 is paid
once, and the €2 six times. The brackets in the second line force the
adding to happen first, $6 \times 6 = 36$, which charges the €4 start
six times.

</details>

**7. Predict.** What does this print: 750 or 1250?

```python
water_ml = 250
cups = 3
total_ml = cups * water_ml
cups = 5
print(total_ml)
```

<details class="dl-answer"><summary>answer</summary>

`750`. On line 3, Python works out `3 * 250` and names the result
`total_ml`. Line 4 points `cups` at a new value, but `total_ml` was
worked out already, and nothing tells Python to work it out again. A
value is worked out when its line runs, not later.

</details>

**8. Make.** Four friends have a meal that costs €86.40, and they want
to leave a 10% tip. Use `split_bill` to find each share. Then check the
answer by hand, step by step.

<details class="dl-answer"><summary>answer</summary>

```python
print(split_bill(86.40, 4, 10))
```

By hand: the tip is 10% of €86.40, which is €8.64. The total with the
tip is $86.40 + 8.64 = 95.04$. Shared between 4, that is
$95.04 \div 4 = 23.76$. Each friend pays €23.76.

</details>

**9. Fix.** The total here came from a form, as text. Run the cell,
read the last line of the error, and fix the cell.

```python exec
id: mixed-instructions-form-total
total = "86.40"
print(split_bill(total, 4, 10))
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Read the last line. What kind of error is it?
2. Which kind of value does it name that should not be there?
3. Which line of *your* cell gave `split_bill` that value?
4. Which function turns text into a float?

**Think about:** the line that failed is inside `split_bill`. The line
responsible is in your cell.

**Try this next:** what happens if the form gives `"86,40"`, with a
comma, as it might in many countries?

</details>

<details class="dl-answer"><summary>answer</summary>

The last line is:

```text
TypeError: can't multiply sequence by non-int of type 'float'
```

This is the message from
[When Python says no](tutorial:when-python-says-no): a "sequence" here
is the string `"86.40"`, and `split_bill` tried to multiply it by a
float. The line that failed is inside `split_bill`, but the line
responsible is line 1 of this cell, which made `total` a string. Turn
it into a number first:

```python
total = float("86.40")
print(split_bill(total, 4, 10))
```

This prints `23.76`, as in problem 8.

</details>

**10. Another way.** Find 255 in hexadecimal two ways. First, use
`to_hex`. Then write 255 in binary, split the bits into groups of four,
and turn each group into one hex digit.

<details class="dl-answer"><summary>answer</summary>

`to_hex(255)` gives `FF`.

The second way: `to_binary(255)` gives `11111111`. In groups of four
that is `1111 1111`. Each group is $8 + 4 + 2 + 1 = 15$, which is the
hex digit F. So 255 is `FF` again. This is why hex is so handy for
colours: a byte always splits into exactly two hex digits.

</details>

**11. Explain.** A weather station's temperature sensor sends each
reading as a whole number from 0 to 1023. Why 1023, and not a round
number like 1000? How many bits does each reading use?

<details class="dl-answer"><summary>answer</summary>

The sensor uses 10 bits. Ten bits give $2^{10} = 1024$ different
patterns, and counting from 0, the largest is $1024 - 1 = 1023$. For a
computer, the round numbers are powers of 2, not powers of 10. Checking
with a logarithm: `math.log2(1024)` is `10.0`.

</details>

**12. Make.** Say an adult bus fare is €2.00 and a child fare is €0.65.
First, write the steps in pseudocode, as comments. Then write a function
`bus_fare(adults, children)` that gives the total fare for a group. Test
it with `assert`: 2 adults and 3 children should cost €5.95.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. In words: what do you do with the number of adults? With the number
   of children? What do you do with the two results?
2. Write those steps as `#` lines.
3. Under `def bus_fare(adults, children):`, write one pushed-in line
   that gives back the total with `return`.
4. Floats can be a tiny bit off, so round the total to 2 places before
   comparing it.

**Think about:** which is the promise here, and which are the steps?

**Try this next:** what should `bus_fare(0, 0)` give?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
# SET adult_cost TO adults times 2.00
# SET child_cost TO children times 0.65
# GIVE BACK adult_cost plus child_cost

def bus_fare(adults, children):
    """The total bus fare, in euro, for a group of adults and children."""
    return adults * 2.00 + children * 0.65


assert round(bus_fare(2, 3), 2) == 5.95
assert bus_fare(0, 0) == 0
print(bus_fare(2, 3))
```

This prints `5.95`. Python multiplies before it adds, so the line needs
no brackets. The `round` in the test is there because floats are binary
fractions, and 0.65 has no exact binary form.

</details>

**13. Fix.** In Gaelic football, a goal is worth 3 points. A score of
2 goals and 11 points, written 2-11, is worth 17 points. This function
should give that total. Run it, read the message, and fix it.

```python exec
id: mixed-instructions-gaa
def total_points(goals, points):
    return goal * 3 + points


print(total_points(2, 11))
```

<details class="dl-answer"><summary>answer</summary>

```text
NameError: name 'goal' is not defined. Did you mean: 'goals'?
```

The parameter is named `goals`, with an s, but line 2 uses `goal`. The
fix is `return goals * 3 + points`, and then the cell prints `17`. The
traceback names two places: line 5, where the call was made, and line
2, inside the function, where the name was missing. Here the line that
failed is also the line to fix.

</details>

## Stretch

**14. Predict.** `to_binary` and `to_hex` promise to work with whole
numbers of 0 or more. What happens if we step outside that space? Say
what you expect, then run each line on its own.

```python
print(to_binary(-5))
print(to_hex(2.5))
```

<details class="dl-answer"><summary>answer</summary>

The first line prints `-101`, with no error. The second stops with:

```text
ValueError: Unknown format code 'X' for object of type 'float'
```

So one broken promise gives an error, and the other gives an answer we
never agreed on. `-101` is a sensible way to write −5, but it is not the
string of 0s and 1s that `to_binary` promised, and a program that trusts
the promise could go wrong later, with no message at all. A promise
holds only inside its space. Outside it, anything may happen, and an
error is the better of the two outcomes.

</details>

**15. Another way.** Three friends share a €100 bill. Run
`split_bill(100, 3)`. What does each person pay? Add up the three
shares. What went missing? Then find another way, in whole cents with
`//` and `%`, that shares out every cent.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. €100 is 10,000 cents.
2. `10000 // 3` is what everyone pays at least.
3. `10000 % 3` is how many cents are left over after that.
4. Who pays the leftover cents?

**Think about:** why whole cents never go missing, and rounded euro can.

**Try this next:** share €50 between 7 people the same way.

</details>

<details class="dl-answer"><summary>answer</summary>

`split_bill(100, 3)` gives `33.33`. Three shares of €33.33 add up to
€99.99, so one cent is missing: rounding each share to the cent threw
away a third of a cent three times.

In whole cents:

```python
total_cents = 10000
people = 3
each = total_cents // people
left_over = total_cents % people
print(each, left_over)
```

This prints `3333 1`. Everyone pays 3,333 cents, and 1 cent is left, so
one person pays €33.34 and the other two pay €33.33. Now
$3334 + 3333 + 3333 = 10000$, every cent. The unit's two number spaces
meet here: whole numbers share exactly, and floats round.

</details>

**16. Make.** Write a function `hex_colour(red, green, blue)` that
gives the colour code, like `"#FF8800"`, for three brightnesses from 0
to 255. Test it with `assert`, including a colour with a 0 in it.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Each light needs exactly two hex digits.
2. `to_hex(0)` gives `"0"`, only one digit. `format(0, "02X")` gives
   `"00"`.
3. Join `"#"` and the three pairs with `+`.
4. Test with `(255, 136, 0)`, which should give `"#FF8800"`.

**Think about:** why the test with a 0 in it matters more than the
others.

**Try this next:** what should `hex_colour(256, 0, 0)` give, and what
does yours give?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def hex_colour(red, green, blue):
    """The #RRGGBB code for three brightnesses from 0 to 255."""
    return "#" + format(red, "02X") + format(green, "02X") + format(blue, "02X")


assert hex_colour(255, 136, 0) == "#FF8800"
assert hex_colour(0, 0, 0) == "#000000"
assert hex_colour(255, 255, 255) == "#FFFFFF"
print(hex_colour(22, 155, 98))
```

This prints `#169B62`. The test with 0 in it is the one that catches a
version built with `to_hex`, which would give `#FF880`, a code a
browser cannot read.

</details>

**17. Explain.** A friend says: "Python is broken. `1 + 2 == 3` is
`True`, but `0.1 + 0.2 == 0.3` is `False`." Using what this unit taught
about the spaces numbers live in, explain what is happening, and whether
anything is broken.

<details class="dl-answer"><summary>answer</summary>

Nothing is broken. The two sums live in different spaces.

`1`, `2` and `3` are ints. Python keeps whole numbers exactly, in
binary, so `1 + 2` is exactly `3`.

`0.1`, `0.2` and `0.3` are floats. A float is a binary fraction, built
from halves, quarters, eighths and so on, and a tenth cannot be made
exactly from those. So Python keeps a number very close to 0.1, and the
tiny differences show up in the sum: `0.30000000000000004`.

In the space of fractions, ℚ, `0.1 + 0.2 == 0.3` is true. In the space
of floats, the question to ask is "close enough?", for example
`round(0.1 + 0.2, 10) == 0.3`.

</details>

**18. Fix.** A game controller sends the state of four buttons as four
bits. This function should turn them back into a number, so `1, 1, 0, 1`
should give 13. The test fails. Find the mistake and fix it.

```python exec
id: mixed-instructions-bits
def from_bits(bit_8, bit_4, bit_2, bit_1):
    """The number made by four bits, worth 8, 4, 2 and 1."""
    return bit_8 * 2 ** 3 + bit_4 * 2 ** 2 + bit_2 * 2 + bit_1 * 2 ** 1


print(from_bits(1, 1, 0, 1))
assert from_bits(1, 1, 0, 1) == 13
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The cell prints 14, one too many. Which bit is 1 here, and worth 1?
2. Work out each of the four parts of the sum on its own.
3. What is $2^1$? What should the last bit be worth?

**Think about:** the names promise worths of 8, 4, 2 and 1. Does the
code keep that promise?

**Try this next:** add a test that uses only the last bit,
`from_bits(0, 0, 0, 1)`. Would it have caught the mistake alone?

</details>

<details class="dl-answer"><summary>answer</summary>

The last part is `bit_1 * 2 ** 1`, which is worth 2, not 1. The ones
column is $2^0 = 1$:

```python
def from_bits(bit_8, bit_4, bit_2, bit_1):
    """The number made by four bits, worth 8, 4, 2 and 1."""
    return bit_8 * 2 ** 3 + bit_4 * 2 ** 2 + bit_2 * 2 ** 1 + bit_1 * 2 ** 0


print(from_bits(1, 1, 0, 1))
assert from_bits(1, 1, 0, 1) == 13
assert from_bits(0, 0, 0, 1) == 1
assert from_bits(1, 1, 1, 1) == 15
```

This prints `13`, and every test passes. Python saw nothing wrong with
the first version: only the test noticed. Without the test, 14 would have
looked like a fine answer. That is what a test is for.

</details>
