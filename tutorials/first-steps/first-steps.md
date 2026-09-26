---
title: "Algorithms, pseudocode and your first Python"
year: "2026-2027"
version: 2026.09.26.1
worlds:
  secret-messages: Codes and hidden messages, the kind spies and puzzle-setters make.
  pixel-art: Pictures made of small squares, the way a screen draws them.
covers:
  what-is-an-algorithm:
    covers: [MIT-6.1, PDP-LO2]
  pseudocode-planning-before-coding:
    covers: [PDP-LO5, PDP-LO6]
  a-few-more-things-python-can-do:
    covers: [PDP-LO4]
---

# Algorithms, pseudocode and your first Python

Here is a line of Python. Before you run it, what do you think will appear
under it?

```python exec
id: hello-1
print("Hello, world!")
```

```predict
What will appear under the cell?

- Hello, world!
  - `print` shows the text inside the quotes.
- "Hello, world!"
  - The quotes tell Python where the text starts and ends. Are they part
    of the text?
- print("Hello, world!")
  - This is what you would see if Python showed the line instead of
    running it.
```

To run a cell, press its **Run** button, or hold Ctrl and press Enter. The
first run on a page takes a few seconds, while Python starts.

That one line is a complete program. A *program* is a set of clear steps,
written carefully enough for a computer to follow. `print()` is a
*function*: a named tool that does one job. The job of `print()` is to
display what is inside its brackets. The quotes mark where the text starts
and ends, so they are not shown.

This is the first programming page, and everyone starts here. You do not
need to know anything about computers or maths to begin. Over the coming
weeks we learn to program, and some maths along the way. The two are closer
than most people expect: a formula is also a set of steps, written for a
person instead of a computer.

## How this page works

Most of this page is reading. Between the paragraphs are *cells*: small
boxes of Python you can change and run. The result appears underneath. The
Python runs inside this browser tab, on the computer in front of you, and
nobody else can see what you type. You do not need to install anything.

The next cell has a few more lines. A line that starts with `#` is a
*comment*: a note for the people who read the code. Python ignores
everything on a line after the `#`.

```python exec
id: how-this-page-works-1
# Python can do arithmetic too.
print(2 + 3)
print(10 * 7)
print(100 / 4)
```

```predict
What will the last line show?

- 25
  - 100 shared into 4 is 25, a whole number.
- 25.0
  - Division in Python always gives a number with a decimal point.
- 100 / 4
  - Without quotes, Python works the sum out instead of showing it.
```

The numbers have no quotes around them. Python works with numbers
directly: text needs quotes, and numbers do not. And `100 / 4` gives
`25.0`, not `25`. Dividing with `/` always gives a number with a decimal
point, even when the answer is whole. The next page explains why Python
keeps two kinds of number.

## When a cell does not do what you expect

A cell can fail when nothing is wrong with the site. Here are three things
to try, in this order.

**Reset the cell.** The reset button next to Run brings back the code the
page started with. If the cell works again after that, the problem was in
an edit, not in the page.

**Run the cells above it.** A later cell often uses something an earlier
cell made. The cells on a page share their work, so the order you run them
in matters. The small **⋯** button beside Run opens "Run this cell and all
above". It runs every cell before this one, from the top of the page.

**Reload the page.** This starts Python again, fresh. It does not delete
anything you have saved. Your work is kept in this browser, on this device.

If none of these explains it, the small circle on a cell's bar opens a
report with your code and the cell's last output already in it, so there is
nothing to copy. The line at the bottom of every page does the same for the
whole page.

## A few more things Python can do

Python works through a calculation in a fixed order, the same one you may
know from school as BODMAS or PEMDAS: brackets first, then powers, then
multiplication and division, then addition and subtraction.

```python exec
id: order-of-operations-1
print(2 + 3 * 4)
```

```predict
type: number

What will it print?
```

It prints 14. Python multiplies first, 3 × 4 is 12, and then adds the 2.
To add first, put brackets round the part that comes first:
`(2 + 3) * 4` is 20.

Here are the rest of Python's arithmetic operators. Can you change the
numbers and see what each one does with them?

```python exec
id: more-operators-1
print(2 ** 3)      # a power: 2 to the power of 3
print(17 / 5)      # division
print(17 // 5)     # floor division: how many whole 5s fit into 17
print(17 % 5)      # remainder: what is left over
```

| Operator | What it does | Example | Result |
|---|---|---|---|
| `+` | addition | `17 + 5` | `22` |
| `-` | subtraction | `17 - 5` | `12` |
| `*` | multiplication | `17 * 5` | `85` |
| `/` | division | `17 / 5` | `3.4` |
| `//` | floor division: divides, then rounds down to a whole number | `17 // 5` | `3` |
| `%` | remainder, also called modulo | `17 % 5` | `2` |
| `**` | power | `2 ** 3` | `8` |

The last two work as a pair. Five goes into 17 three times, with 2 left
over: `17 // 5` counts the whole fives, and `17 % 5` gives what is left.
The remainder turns up more often than you might expect. A number is even
when its remainder after dividing by 2 is 0, and a clock goes back to 0
after 23 because of a remainder.

```python exec
id: remainder-1
print(100 % 7)
```

```predict
type: number

What will it print?
```

```hint
after: unsure
How many whole 7s fit into 100? Try `100 // 7` first. What is left once
those 7s are taken away?
```

Seven goes into 100 fourteen times, which uses up 98, so 2 is left over.

### Your turn

<div class="dl-world" data-world="secret-messages">

A spy sends a message by tapping a key: one tap for A, two for B, three for
C, and so on, up to 26 taps for Z. How many taps does the word CAB take?
And HELLO, where H is the 8th letter, E the 5th, L the 12th and O the 15th?

```python exec
id: your-turn-1--secret-messages
# How many taps for CAB?

```

```hint
C is the 3rd letter, A the 1st and B the 2nd. Can you add them in one
`print()`?
```

```solution
print(3 + 1 + 2)
print(8 + 5 + 12 + 12 + 15)
---
CAB takes 6 taps, and HELLO takes 52. Writing each letter's number in the
sum, rather than the total you worked out, shows where the answer came
from.
```

</div>

<div class="dl-world" data-world="pixel-art">

A screen draws a picture out of small squares called pixels. An old games
console had a screen 320 pixels wide and 240 tall. How many pixels is that?
A phone photo is 4000 by 3000 pixels: how many times more is that?

```python exec
id: your-turn-1--pixel-art
# How many pixels on the old screen?

```

```hint
A picture 320 wide and 240 tall is 240 rows of 320. How do you work out
240 lots of 320?
```

```solution
print(320 * 240)
print(4000 * 3000 / (320 * 240))
---
The old screen has 76,800 pixels, and the photo has 12 million, about 156
times more. The brackets make Python work out the old screen's pixels
first, before it divides.
```

</div>

## What is an algorithm?

An *algorithm* is a list of clear steps that complete a task. Each step has
only one meaning. We follow algorithms every day without thinking about
them. Here is one for making a cup of tea:

1. Fill the kettle with water.
2. Switch the kettle on.
3. While the water has not boiled, wait.
4. Pour the water into a cup with a tea bag in it.
5. Wait three minutes.
6. Take the tea bag out.

It starts from a known point: a kettle, water, a cup and a tea bag. The
steps come in a clear order. And it finishes: at the end, there is a cup of
tea.

Step 3 is different from the others. "While the water has not boiled, wait"
repeats the waiting until the water boils. This is a *loop*: a step, or a
group of steps, that repeats until something is true. We write loops in
Python in [Repeating steps with loops](tutorial:repeating-yourself).

Programming is writing algorithms carefully enough for a computer to follow
them. A computer is very fast, but it cannot guess what you meant. It does
exactly what you tell it, and nothing more.

Think of something you do most days: making breakfast, getting to college,
logging in to a computer. Can you write it as numbered steps? How much
detail would somebody need who had never done it before? You could write
the steps on paper, or in **Your notes**, in the **Notes** panel at the top
right of the page.

## Pseudocode: planning before coding

Before we write Python, it helps to plan the steps in plain English.
*Pseudocode* is a plan for a program, written in plain English, sometimes
with a little code-like structure. No computer runs it. Writing pseudocode
first is one of the most useful habits you can build.

Here is a plan for finding the middle of a screen 320 pixels wide and 240
tall:

```
GET the width and the height of the screen
DIVIDE the width by 2, to find the middle across
DIVIDE the height by 2, to find the middle down
DISPLAY both
```

And here is the same plan in Python. It keeps the numbers under the names
`width` and `height`. The next page,
[Variables, data types and text](tutorial:storing-and-computing), explains
how names like these work.

```python exec
id: pseudocode-planning-before-coding-1
# Find the middle of a screen
width = 320
height = 240
print(width // 2, height // 2)
```

This is the way of working we use all through these pages:

1. Think about what you want to do.
2. Write it as pseudocode.
3. Turn the pseudocode into Python.

For a small problem, the pseudocode can feel like extra work. As problems
get bigger, it is what keeps you from getting lost.

### Your turn

Can you write the plan first this time? In the cell, write your pseudocode
as comments, one line of plain English for each step, each starting with
`#`. Then write the Python for each step under its comment.

<div class="dl-world" data-world="secret-messages">

Spies used to send messages in blocks of five letters, so nobody listening
could count the words. A message has 47 letters. How many full blocks of
five does it make, and how many letters are left over for the last one?

```python exec
id: your-turn-2--secret-messages
# Plan first, as comments. Then the Python.

```

```hint
Which operator counts how many whole fives fit, and which one gives what is
left over? Both are in the table above.
```

```solution
# GET the number of letters
# DIVIDE by 5, keeping only the whole blocks
# FIND the remainder, the letters left over
letters = 47
print(letters // 5)
print(letters % 5)
---
Nine full blocks, and two letters left over for a short last block.
```

</div>

<div class="dl-world" data-world="pixel-art">

A row of a picture is 50 pixels wide. You want to fill it with tiles 8
pixels wide. How many whole tiles fit, and how many pixels are left over at
the end?

```python exec
id: your-turn-2--pixel-art
# Plan first, as comments. Then the Python.

```

```hint
Which operator counts how many whole 8s fit into 50, and which one gives
what is left over? Both are in the table above.
```

```solution
# GET the width of the row
# DIVIDE by the width of a tile, keeping only the whole tiles
# FIND the remainder, the pixels left over
row = 50
print(row // 8)
print(row % 8)
---
Six whole tiles, and two pixels left over at the end.
```

</div>

## Looking back

`/` and `//` both divide. When would you want each one? Think of a
question on this page where only one of them gives an answer that makes
sense.

A challenge: a clock shows 22:00. What time will it show 5 hours later? And
40 hours later? Can you make Python go back to 0 after 23, the way a clock
does? One of the operators on this page does it in one step.

```python challenge
# It is 22:00. What time will it be 5 hours later?
# Can one operator make the hours go back to 0 after 23?
now = 22
later = now + 5
print(later)
```

The next page, [Variables, data types and text](tutorial:storing-and-computing),
gives values names, and meets text as something Python can take apart.

## Where to read more

Everything here is covered elsewhere too, often in a form that will suit you
better than this one. These are worth your time.

Downey, A. B. (2015). *Think Python: How to Think Like a Computer Scientist*
(2nd ed.). Green Tea Press. Free at <https://greenteapress.com/wp/think-python-2e/>.
Chapters 1 and 2 cover this tutorial's ground at greater length, and the book is
written for exactly this audience.

Python Software Foundation. *The Python Tutorial*, sections 3.1 and 3.1.1.
<https://docs.python.org/3/tutorial/introduction.html>. The official reference
for the arithmetic operators, including the exact behaviour of `//` and `%`.

Computerphile (2017). *What on Earth is an Algorithm?*
<https://www.youtube.com/watch?v=X0HHUlAiA4E>. Nine minutes on what does and
does not count as an algorithm, which is a harder question than it first looks.

Khan Academy. *Intro to algorithms*.
<https://www.khanacademy.org/computing/computer-science/algorithms>. Worked
through slowly, with exercises, if the pace here was too quick.
