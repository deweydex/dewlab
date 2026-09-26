---
title: "Algorithms, pseudocode and your first Python — Practice"
practice_for: first-steps
year: "2026-2027"
version: 2026.09.26.1
worlds:
  secret-messages: Codes and hidden messages, the kind spies and puzzle-setters make.
  pixel-art: Pictures made of small squares, the way a screen draws them.
---

# Algorithms, pseudocode and your first Python — Practice

Problems on the operators, `print()`, algorithms and pseudocode. Most are
short. Try each one before you open anything under it. Say what you think
first, then run it.

## 1. Which comes first

```python exec
id: which-comes-first-1
print(20 - 6 / 3)
```

```predict
type: number
tolerance: 0.01

What will it print?
```

Now try `9 + 4 * 2`, `(9 + 4) * 2` and `(20 - 6) / 3` in the cell. What does
each give, and why?

<details class="dl-answer"><summary>answer</summary>

`20 - 6 / 3` is 18.0. The division happens first, 6 / 3 is 2.0, and 20 −
2.0 is 18.0. The others are 17, 26 and 4.666…

Multiplication and division happen before addition and subtraction, unless
brackets say otherwise. And division with `/` always gives a number with a
decimal point, even when the answer is whole.

</details>

## 2. Hours and minutes

A film is 143 minutes long. Can you print how many whole hours that is, and
how many minutes are left over?

```python exec
id: hours-and-minutes-1
# How many whole hours in 143 minutes, and how many minutes left over?

```

```hint
There are 60 minutes in an hour. Which operator counts the whole 60s, and
which gives what is left?
```

```solution
print(143 // 60, "hours and", 143 % 60, "minutes")
---
2 hours and 23 minutes. This pair comes up all the time: `//` counts how
many whole ones there are, and `%` gives what is left over. A comma between
the pieces inside `print()` puts a space between them.
```

## 3. When it does not fit at all

```python exec
id: when-it-does-not-fit-1
print(5 // 17)
```

```predict
type: number

What will it print?
```

And `5 % 17`? Try it once you have a guess.

<details class="dl-answer"><summary>answer</summary>

`5 // 17` is 0, and `5 % 17` is 5. Seventeen does not go into 5 at all, so
the whole part is 0, and *all* of the 5 is left over.

</details>

## 4. A remainder below zero

```python exec
id: a-remainder-below-zero-1
print(-7 % 3)
```

```predict
type: number

What will it print?
```

<details class="dl-answer"><summary>why</summary>

It prints 2, and most people expect −1.

In Python, the result of `%` always has the same sign as the number on the
right, or is 0. Python makes `(a // b) * b + (a % b)` always equal `a`.
And `-7 // 3` is −3, not −2, because `//` rounds down, and down from −2.33
is −3. So (−3 × 3) + 2 = −7.

Other programming languages do not all agree with Python about this. It is
worth knowing before you move code from one language to another.

</details>

## 5. Powers

Say what each of these gives, then try them in the cell: `2 ** 10`,
`10 ** 2`, `2 ** 0.5` and `2 ** -1`.

```python exec
id: powers-1
print(2 ** 10)
```

<details class="dl-answer"><summary>answer</summary>

They give 1024, 100, 1.4142… and 0.5. A power of 0.5 is a square root,
and a negative power is one divided by the number. Both are main ideas of
[Number types, powers and logarithms](tutorial:numbers-and-their-families),
and you meet them early here.

</details>

## 6. Powers of powers

```python exec
id: powers-of-powers-1
print(2 ** 3 ** 2)
```

```predict
Will it print 64 or 512?

- 64
  - This works out `2 ** 3` first, then squares it.
- 512
  - This works out `3 ** 2` first, then raises 2 to that.
```

<details class="dl-answer"><summary>why</summary>

Powers group from the right, so Python reads this as `2 ** (3 ** 2)`, which
is `2 ** 9`. Almost every other operator in Python groups from the left,
and `**` is the one that does not. When you are not sure, add brackets.
Then nobody who reads your code needs to know this rule.

</details>

## 7. Text, or a sum

```python exec
id: text-or-a-sum-1
print("5 + 3")
```

```predict
What will it print?

- 8
  - Python works out a sum when it sees one without quotes.
- 5 + 3
  - Inside quotes, the plus sign is just a character in the text.
```

<details class="dl-answer"><summary>why</summary>

Quotes mean "this is text, so do not calculate it". Without quotes,
`print(5 + 3)` prints 8. With them, Python has a piece of writing that
happens to contain a plus sign.

</details>

## 8. Let Python work it out

Can you write one `print()` that displays `The answer is 42`, with Python
calculating the 42 from `6 * 7` rather than you typing it?

```python exec
id: let-python-work-it-out-1

```

```solution
print("The answer is", 6 * 7)
---
A comma between the pieces inside `print()` puts a space between them in
the output.
[Variables, data types and text](tutorial:storing-and-computing) shows
another way, which joins pieces of text with `+`.
```

## 9. Hidden lines

```python exec
id: hidden-lines-1
# print("first")
print("second")  # print("third")
```

```predict
What will it print?

- first, second and third
  - Each of the three prints runs.
- second and third
  - The first line starts with #, so it does not run.
- second
  - Everything after a # on a line is a comment, even code.
```

## 10. A toast algorithm

Here is an algorithm for making toast. Where would a machine get stuck
following it?

```
1. Put bread in the toaster
2. Wait
3. Take out the toast
```

<details class="dl-answer"><summary>one good answer</summary>

Step 2 does not say how long to wait, or what to wait *for*. A machine
cannot follow "Wait". It can follow "While the toaster has not popped,
wait", because that step names what ends the waiting. Every loop needs
something like this.

Something else is missing too: nobody switches the toaster on.

</details>

## 11. The largest number

Can you write an algorithm, as numbered steps, to find the largest number
in a list written on paper? You can look at only one number at a time.

<details class="dl-answer"><summary>one good answer</summary>

```
1. Look at the first number and remember it as the largest so far
2. For each number after it:
3.     If it is bigger than the largest so far, remember it instead
4. The largest so far is the answer
```

Because you can see only one number at a time, you have to remember one
number as you go, the "largest so far". That is a variable, which the
next page explains. Python's own `max()` finds the largest value for you,
and inside, it follows this same algorithm.

</details>

## 12. Two ways to make tea

Two algorithms both make tea. One boils the kettle, then gets a cup. The
other gets a cup, then boils the kettle. Are they the same algorithm?

<details class="dl-answer"><summary>one good answer</summary>

No, even though they make the same tea. The order of the steps is part of
an algorithm. Some steps cannot swap places. If the second step needs the
first, the algorithm breaks when you swap them. When you read an algorithm,
look for the steps whose order matters, and the steps whose order does not.

In real life you would probably do something faster than either: switch the
kettle on, then get the cup while the water boils. When you do two things
at the same time like this, it is called concurrency. It is a topic for
later.

</details>

## 13. From a plan to Python

Can you turn this plan into Python, one line for each step?

<div class="dl-world" data-world="secret-messages">

Number the letters from 0: A is 0, B is 1, and so on, up to Z, which is 25.
This plan moves a letter five places along the alphabet, going back to A
after Z. It is the main step of a secret code called a Caesar shift.

```
SET the letter to 23, which is X
ADD 5 to move it along
FIND the remainder after dividing by 26, so it goes back round after Z
DISPLAY the new letter's number
```

```python exec
id: from-a-plan-to-python-1--secret-messages
# One line of Python under each step of the plan

```

```solution
letter = 23
moved = letter + 5
moved = moved % 26
print(moved)
---
It prints 2, which is C: X moves on to Y, Z, then round to A, B and C. The
remainder is what makes the alphabet go round like a clock.
```

</div>

<div class="dl-world" data-world="pixel-art">

A small picture is 64 pixels wide and 48 tall. Each pixel takes three bytes
of memory: one for red, one for green and one for blue. This plan calculates
how much memory the picture takes.

```
SET the width to 64
SET the height to 48
MULTIPLY them to get the number of pixels
MULTIPLY by 3 to get the number of bytes
DISPLAY the bytes
```

```python exec
id: from-a-plan-to-python-1--pixel-art
# One line of Python under each step of the plan

```

```solution
width = 64
height = 48
pixels = width * height
bytes_needed = pixels * 3
print(bytes_needed)
---
3,072 pixels, and 9,216 bytes. You could write `64 * 48 * 3` on one line.
It gives the same answer, but it hides what each number means.
```

</div>

## 14. Why plan at all

Why write pseudocode at all, when you could write the Python straight
away?

<details class="dl-answer"><summary>one good answer</summary>

Programming has two hard parts. If you do both at once, it can feel
impossible at the start. When you decide *what* the steps are, you think
about the problem. When you decide how to say them in Python, you think
about Python. Pseudocode lets you finish the first before you start the
second. Then, when the code does something you did not expect,
you know which of the two to look at.

For a three-line program, pseudocode is more than you need. Keep the habit
anyway. You will not notice the moment a problem grows past three lines.

</details>

## 15. Even or odd

A number is even when its remainder after dividing by 2 is 0. Can you check
whether 1234567 is even, using only what the tutorial covered?

```python exec
id: even-or-odd-1

```

```solution
print(1234567 % 2)
---
It prints 1, so the number is odd. Making Python print the word "odd" needs
a decision, and
[Making decisions with if, elif and else](tutorial:making-decisions)
teaches decisions, two pages from now.
```
