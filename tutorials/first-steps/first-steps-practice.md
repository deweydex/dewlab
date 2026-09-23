---
title: "Algorithms, pseudocode and your first Python — Practice"
practice_for: first-steps
year: "2026-2027"
version: 2026.08.23.1
---

# Algorithms, pseudocode and your first Python — Practice

On this page we practise the operators, `print()`, comments, algorithms
and pseudocode. Most of the problems are short. The aim is to use the
operators again and again, until you no longer need to stop and think
about them.

Each answer is folded away under its problem. Many problems ask you to
predict the result before you run anything. Try to predict first, and
wait before you run the cell. A wrong prediction, and finding out why it
was wrong, teaches you more than a right answer that came from running
the cell.

## Arithmetic

The cell below is a scratchpad for this section.

```python exec
id: arithmetic-1
# A scratchpad. Change anything, run it as often as you like.
print(7 + 3, 7 - 3, 7 * 3, 7 / 3)
print(7 // 3, 7 % 3, 7 ** 3)
```

**1.** Predict each result, then check.

- (a) `9 + 4 * 2`
- (b) `(9 + 4) * 2`
- (c) `20 - 6 / 3`
- (d) `(20 - 6) / 3`

<details class="dl-answer"><summary>answer</summary>

(a) 17. (b) 26. (c) 18.0. (d) 4.666…

There are two things to notice:

- Multiplication and division happen before addition and subtraction,
  unless brackets say otherwise.
- Division with `/` always gives a decimal number, even when the answer
  is whole. `6 / 3` is `2.0`, and not `2`.

</details>

**2.** How many seconds are there in a week? Write it as one calculation,
and not as a number you worked out somewhere else.

<details class="dl-answer"><summary>answer</summary>

```python
print(7 * 24 * 60 * 60)
```

604800. Anyone who reads `7 * 24 * 60 * 60` can see where the number
came from. It is also easy to change: with one edit, from 7 to 30, it
counts the seconds in a month.

</details>

**3.** A film is 143 minutes long. Print how many whole hours that is,
and how many minutes are left over.

<details class="dl-answer"><summary>answer</summary>

```python
print(143 // 60, "hours and", 143 % 60, "minutes")
```

2 hours and 23 minutes. This pair comes up all the time: `//` counts how
many whole ones there are, and `%` gives what is left over.

</details>

**4.** Predict each result, then check.

- (a) `17 // 5`
- (b) `17 % 5`
- (c) `5 // 17`
- (d) `5 % 17`

<details class="dl-answer"><summary>answer</summary>

(a) 3. (b) 2. (c) 0. (d) 5.

The last two surprise people. 17 does not go into 5 at all. So the whole
part is 0, and *all* of the 5 is left over.

</details>

**5.** What does `%` do with negative numbers? Predict `-7 % 3`, then
run it.

<details class="dl-answer"><summary>answer</summary>

2. Most people expect −1, so this is a surprise.

In Python, the result of `%` always has the same sign as the number on
the right, or is 0. Python defines `%` so that `(a // b) * b + (a % b)`
always gives back `a`. And `-7 // 3` is −3, not −2, because `//` rounds
down, and down from −2.33 is −3. So (−3 × 3) + 2 = −7.

Other programming languages do not all agree with Python about this. It
is worth knowing before you translate code from one language to another.

</details>

**6.** Predict each result, then check.

- (a) `2 ** 10`
- (b) `10 ** 2`
- (c) `2 ** 0.5`
- (d) `2 ** -1`

<details class="dl-answer"><summary>answer</summary>

(a) 1024. (b) 100. (c) 1.4142…, because a fractional power is a root:
the power 0.5 gives the square root. (d) 0.5, because a negative power
gives the reciprocal, one divided by the number.

The last two are the main ideas of
[Numbers and Their Families](tutorial:numbers-and-their-families),
arriving early.

</details>

## Print, and Comments

**7.** What is the difference between `print(5 + 3)` and
`print("5 + 3")`?

<details class="dl-answer"><summary>answer</summary>

The first prints 8. The second prints `5 + 3`.

Quotes mean "this is text, so do not work it out". Without quotes,
Python works out the calculation. With quotes, Python has a piece of
writing that happens to contain a plus sign.

</details>

**8.** Write one `print()` that displays `The answer is 42`. Let Python
calculate the 42, and do not type it in.

<details class="dl-answer"><summary>answer</summary>

```python
print("The answer is", 6 * 7)
```

A comma between the pieces inside `print()` puts a space between them in
the output.
[Variables, data types and text](tutorial:storing-and-computing) shows another
way to do this, which joins pieces of text with `+`.

</details>

**9.** What does this print, and why?

```python
# print("first")
print("second")  # print("third")
```

<details class="dl-answer"><summary>answer</summary>

Only `second`.

Python ignores everything after a `#` on a line, and that includes code.
The first line is all comment. The third `print()` sits inside the
comment at the end of the second line.

</details>

## Algorithms

**10.** Here is an algorithm for making toast. What is wrong with it?

```
1. Put bread in the toaster
2. Wait
3. Take out the toast
```

<details class="dl-answer"><summary>answer</summary>

Step 2 does not say how long to wait, or what to wait *for*.

A machine cannot follow "Wait". It can follow "While the toaster has not
popped, wait", because that step names the condition that ends the
waiting. Every loop needs a condition like this. A loop whose condition
never becomes true never stops.

Something else is missing too: nobody turns the toaster on.

</details>

**11.** Write an algorithm, as numbered steps, to find the largest number
in a list of numbers written on paper. You can look at only one number at
a time.

<details class="dl-answer"><summary>answer</summary>

```
1. Look at the first number and remember it as the largest so far
2. For each remaining number:
3.     If it is bigger than the largest so far, remember it instead
4. The largest so far is the answer
```

Because you can see only one number at a time, you have to carry
something with you as you go: the "largest so far". That is a variable,
which the next page explains. Python has a function, `max()`, that finds
the largest value for you, and inside, it follows this same algorithm.

</details>

**12.** Two algorithms both make tea. One boils the kettle, then gets a
cup. The other gets a cup, then boils the kettle. Are they the same
algorithm?

<details class="dl-answer"><summary>answer</summary>

No, even though they make the same tea.

The order of the steps is part of an algorithm, even when another order
gives the same result. Some steps cannot swap places: if the second step
depends on the first, swapping them breaks the whole thing. Part of
reading an algorithm is spotting which orders are forced and which are
free choices.

In real life, you would probably do something faster than either one:
turn the kettle on, then get the cup while the water boils. Doing two
things at the same time like this is called concurrency, and it is a
topic for later.

</details>

## Pseudocode

**13.** Turn this pseudocode into Python.

```
SET price to 40
SET vat rate to 0.23
MULTIPLY price by vat rate to get the vat
ADD the vat to the price to get the total
DISPLAY the total
```

<details class="dl-answer"><summary>answer</summary>

```python
price = 40
vat_rate = 0.23
vat = price * vat_rate
total = price + vat
print(total)
```

49.2. You could write `total = price * 1.23` on one line. It gives the
same answer, but it hides what the 1.23 means. That matters on the day
the VAT rate changes.

</details>

**14.** Write pseudocode to change a distance in miles to kilometres
(multiply by 1.60934). Then write the Python underneath.

<details class="dl-answer"><summary>answer</summary>

```
GET the distance in miles
MULTIPLY it by 1.60934
DISPLAY the result
```

```python
miles = 26.2
kilometres = miles * 1.60934
print(kilometres)
```

About 42.16 km, which is the length of a marathon.

</details>

**15.** Why write pseudocode at all, when you could write the Python
straight away?

<details class="dl-answer"><summary>answer</summary>

Because programming has two hard parts, and doing both at once is what
makes it feel impossible at the start.

- Working out *what* the steps are is thinking about the problem.
- Working out how to say them in Python is thinking about Python.

Pseudocode lets you finish the first part before you start the second.
Then, when the code fails, you know which of the two went wrong.

For a three-line program, pseudocode is more than you need. Keep the
habit anyway, because you will not notice the moment a problem stops
being three lines long.

</details>

## Putting It Together

**16.** A shop sells items at €7.50 each. Print three things:

1. the cost of 13 items
2. that cost with 23% VAT added
3. how many whole items you could buy with €100

<details class="dl-answer"><summary>answer</summary>

```python
price = 7.50
print(13 * price)
print(13 * price * 1.23)
print(100 // price)
```

97.5, then 119.925, then 13.0.

The last one uses `//` with a decimal number. It still gives a whole
number of items, but written as a decimal: `13.0`. If that bothers you,
`int(100 // price)` gives `13`.
[Variables, data types and text](tutorial:storing-and-computing) explains why
`13` and `13.0` are different kinds of value.

</details>

**17.** Without running it: is `2 ** 3 ** 2` equal to 64 or 512?

<details class="dl-answer"><summary>answer</summary>

512.

Powers group from the right, so Python reads this as `2 ** (3 ** 2)`,
which is `2 ** 9`. Almost every other operator in Python groups from the
left, and `**` is the exception. When you are not sure, add brackets.
Then nobody who reads your code needs to know this rule.

</details>

**18.** A number is even when its remainder after dividing by 2 is 0, so
when `n % 2` is 0. Print whether 1234567 is even, using only what the
tutorial has covered.

<details class="dl-answer"><summary>answer</summary>

```python
print(1234567 % 2)
```

1, so it is odd. You cannot yet make Python print the word "odd". That
needs a decision, and [Making decisions with if, elif and else](tutorial:making-decisions)
teaches decisions, two pages from now. Printing the remainder and
reading it yourself is a good place to stop.

</details>
