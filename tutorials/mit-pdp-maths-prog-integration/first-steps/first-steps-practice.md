---
title: "First Steps — Practice"
slug: first-steps-practice
practice_for: first-steps
module: mit-pdp-maths-prog-integration
module_title: "Programming and Maths, Integrated"
year: "2026-2027"
series: maths-and-programming
version: 2026.08.23.1
---

# First Steps — Practice

Answers are folded. Most of these are short — the point is repetition on the operators until they stop needing thought.

Several ask you to predict before running. Predicting wrongly and finding out why is worth more than getting it right by executing the cell first, so resist.

## Arithmetic

```python exec
id: arithmetic-1
# A scratchpad. Change anything, run it as often as you like.
print(7 + 3, 7 - 3, 7 * 3, 7 / 3)
print(7 // 3, 7 % 3, 7 ** 3)
```

**1.** Predict each, then check.

- (a) `9 + 4 * 2`
- (b) `(9 + 4) * 2`
- (c) `20 - 6 / 3`
- (d) `(20 - 6) / 3`

<details class="dl-answer"><summary>answer</summary>

(a) 17. (b) 26. (c) 18.0. (d) 4.666…

Two things to notice. Multiplication and division happen before addition and subtraction unless brackets say otherwise, and any division produces a decimal even when it comes out even — `6 / 3` is `2.0`, not `2`.

</details>

**2.** How many seconds are there in a week? Write it as one expression rather than a number you worked out elsewhere.

<details class="dl-answer"><summary>answer</summary>

```python
print(7 * 24 * 60 * 60)
```

604800. Writing it as `7 * 24 * 60 * 60` rather than `604800` means anyone reading it can see where the number came from, and it is one edit away from being a month.

</details>

**3.** A film is 143 minutes long. Print how many whole hours and how many leftover minutes that is.

<details class="dl-answer"><summary>answer</summary>

```python
print(143 // 60, "hours and", 143 % 60, "minutes")
```

2 hours and 23 minutes. This pairing — `//` for how many whole ones, `%` for what is left over — comes up constantly.

</details>

**4.** Predict each, then check.

- (a) `17 // 5`
- (b) `17 % 5`
- (c) `5 // 17`
- (d) `5 % 17`

<details class="dl-answer"><summary>answer</summary>

(a) 3. (b) 2. (c) 0. (d) 5.

The last two catch people out. Seventeen does not go into five at all, so the whole part is 0 and *all* of the 5 is left over.

</details>

**5.** What does `%` do with negative numbers? Predict `-7 % 3` before running it.

<details class="dl-answer"><summary>answer</summary>

2, which surprises most people who expected −1.

Python's `%` always returns something with the same sign as the right-hand number. It is defined so that `(a // b) * b + (a % b)` comes back to `a`, and `-7 // 3` is −3 rather than −2. Other languages disagree with Python about this, which is worth knowing before you translate code between them.

</details>

**6.** Predict each, then check.

- (a) `2 ** 10`
- (b) `10 ** 2`
- (c) `2 ** 0.5`
- (d) `2 ** -1`

<details class="dl-answer"><summary>answer</summary>

(a) 1024. (b) 100. (c) 1.4142… — a fractional power is a root. (d) 0.5 — a negative power is a reciprocal.

The last two are the whole content of *Numbers and Their Families* arriving early.

</details>

## Print, and Comments

**7.** What is the difference between `print(5 + 3)` and `print("5 + 3")`?

<details class="dl-answer"><summary>answer</summary>

The first prints 8. The second prints `5 + 3`.

Quotes mean "this is text, do not work it out". Without them Python evaluates the expression; with them it has a piece of writing that happens to contain a plus sign.

</details>

**8.** Write one `print()` that displays `The answer is 42`, where the 42 is calculated rather than typed.

<details class="dl-answer"><summary>answer</summary>

```python
print("The answer is", 6 * 7)
```

Commas inside `print()` put a space between the pieces. There are neater ways to do this and you will meet them in *Storing and Computing*.

</details>

**9.** What does this print, and why?

```python
# print("first")
print("second")  # print("third")
```

<details class="dl-answer"><summary>answer</summary>

Just `second`.

Everything after a `#` on a line is ignored, including code. The first line is entirely a comment; the third print is inside a comment on the second line.

</details>

## Algorithms

**10.** Here is an algorithm for making toast. What is wrong with it?

```
1. Put bread in the toaster
2. Wait
3. Take out the toast
```

<details class="dl-answer"><summary>answer</summary>

Step 2 does not say how long, or what to wait *for*.

"Wait" is not an instruction a machine can follow. "While the toaster has not popped, wait" is, because it names the condition that ends the waiting. Every loop needs one of those, and a loop whose condition never becomes true never stops.

Also missing: turning the toaster on.

</details>

**11.** Write an algorithm, as numbered steps, for finding the largest number in a list of numbers written on paper. Assume you can only look at one number at a time.

<details class="dl-answer"><summary>answer</summary>

```
1. Look at the first number and remember it as the largest so far
2. For each remaining number:
3.     If it is bigger than the largest so far, remember it instead
4. The largest so far is the answer
```

The constraint — one number at a time — is what forces you to carry something with you as you go. That "largest so far" is a variable, and this algorithm is what `max()` does internally.

</details>

**12.** Two algorithms both make tea. One boils the kettle then gets a cup; the other gets a cup then boils the kettle. Are they the same algorithm?

<details class="dl-answer"><summary>answer</summary>

No, though they give the same tea.

Order matters in an algorithm even when it does not matter to the outcome, because the two are not always interchangeable: swap two steps where the second depends on the first and the whole thing breaks. Part of reading an algorithm is spotting which of its orderings are forced and which are arbitrary.

The second one is faster in real life, because you can get the cup while the kettle boils. That is concurrency, and it is a topic for later.

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

49.2. Writing `total = price * 1.23` in one line gives the same answer and hides what the 1.23 is, which matters the day the rate changes.

</details>

**14.** Write pseudocode for converting a distance in miles to kilometres (multiply by 1.60934), then write the Python underneath.

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

About 42.16 km, which is a marathon.

</details>

**15.** Why write pseudocode at all, when you could write the Python directly?

<details class="dl-answer"><summary>answer</summary>

Because the two hard parts are separate, and doing them at once is what makes programming feel impossible at the start.

Working out *what* the steps are is thinking about the problem. Working out how to say them in Python is thinking about Python. Pseudocode lets you finish the first before starting the second, and when the code then fails you know which of the two went wrong.

For a three-line program it is overkill. Keep the habit anyway, because you will not notice the moment a problem stops being three lines.

</details>

## Putting It Together

**16.** A shop sells items at €7.50 each. Print the cost of 13 items, the cost with 23% VAT added, and how many whole items you could buy with €100.

<details class="dl-answer"><summary>answer</summary>

```python
price = 7.50
print(13 * price)
print(13 * price * 1.23)
print(100 // price)
```

97.5, then 119.925, then 13.0.

That last one is `//` on decimals, which still gives a whole number of items but as a float — `13.0`. If that bothers you, `int(100 // price)` is the fix, and *Storing and Computing* explains why the two are different kinds of thing at all.

</details>

**17.** Without running it: is `2 ** 3 ** 2` equal to 64 or 512?

<details class="dl-answer"><summary>answer</summary>

512.

Powers group from the right, so this is `2 ** (3 ** 2)`, which is `2 ** 9`. Nearly every other operator in Python groups from the left, and this is the exception. When in doubt, bracket it — the reader should not have to know this rule to read your code.

</details>

**18.** A number is even when `n % 2` is 0. Print whether 1234567 is even, using only what this tutorial has covered.

<details class="dl-answer"><summary>answer</summary>

```python
print(1234567 % 2)
```

1, so it is odd. You cannot yet make Python print the word "odd" — that needs a decision, which is two tutorials away. Printing the remainder and reading it yourself is a perfectly good stopping point.

</details>
