---
title: "Running Python in a cell — Practice"
practice_for: first-steps-cm
year: "2026-2027"
version: 2026.08.23.1
---

# Running Python in a cell — Practice

The answers are hidden in folds under each problem. The problems are
short. Most of them are about two things that confuse people in their
first hour: what a cell shows you, and what `range` produces.

## What a Cell Shows

```python exec
id: what-a-cell-shows-1
hint: Delete the last line and run it again. What changes?
print("printed")
"the value of the last line"
```

**1.** The cell above shows two things. Where does each one come from?

<details class="dl-answer"><summary>answer</summary>

`printed` comes from the `print()`. The text in quotes comes from the
last line, because that line is an expression. A cell shows the value
of its last line if that line has a value.

Delete the last line, and only the printed text is left. Delete the
`print()` line, and only the value is left.

</details>

**2.** What do you think each of these cells shows?

- (a) `2 + 3`
- (b) `print(2 + 3)`
- (c) `x = 2 + 3`
- (d) `x = 2 + 3`, then `x` on the next line

<details class="dl-answer"><summary>answer</summary>

(a) `5`. (b) `5`. (c) nothing at all. (d) `5`.

Look closely at (c). A line with `=` is an instruction, so it has no
value to show. A cell that ends with an instruction looks as if it did
nothing. It did the work. It has nothing to show you about it.

</details>

**3.** What does this cell show?

```python
print("one")
print("two")
3 + 4
```

<details class="dl-answer"><summary>answer</summary>

`one`, then `two`, then `7`.

Printed lines appear in the order they happen. The value of the last
line appears at the end. Only the *last* line's value is shown, so
`1 + 1` on the second line would show nothing.

</details>

## Running Things

**4.** Can you change the cell at the top of the tutorial page so it
prints the numbers 0 to 4? Then 1 to 5?

<details class="dl-answer"><summary>answer</summary>

```python
for step in range(5):
    print(step)
```

and

```python
for step in range(1, 6):
    print(step)
```

`range(5)` starts at 0, and stops before 5. To start somewhere else,
give it two numbers. The second number is still the stopping point, and
it is not included.

</details>

**5.** What does `range(3)` contain?

<details class="dl-answer"><summary>answer</summary>

0, 1 and 2. That is three values, and 3 is not one of them.

`list(range(3))` shows them. On its own, `range(3)` shows as
`range(0, 3)`, not as its contents. That is because a range makes its
numbers one at a time, when they are needed, and does not store them.

[Repeating steps with loops](tutorial:repeating-yourself) has more on
`range()`.

</details>

**6.** Run a cell, change it, then press reset. What comes back?

<details class="dl-answer"><summary>answer</summary>

The code the page started with. You do not get back the version you had
a minute ago.

Reset is not undo. If you want to keep something, copy it somewhere
else before you press reset.

</details>

**7.** Here are two cells, run in order:

```python
total = 10
```

```python
total + 5
```

Does the second one work?

<details class="dl-answer"><summary>answer</summary>

Yes, if the first cell has been run. The cells on a page share one
workspace. A name made in one cell can be used in every cell after it.

If the second cell runs first, it stops with a `NameError`. This is the
most common confusion on a page of cells. What matters is the order you
*ran* the cells in, not the order they appear on the page.

</details>

## Reading Code That Is Not a Cell

**8.** How can you tell whether a block of code on a page can be run?

<details class="dl-answer"><summary>answer</summary>

It has a Run button. A block without one is an illustration, for
reading.

Apart from that, the two look the same, on purpose. The code in an
illustration is real code, and you are welcome to copy it into a cell
to try it.

</details>

**9.** Copy this illustration into the cell below, and make it show the
total.

```python
total = 0
for value in [1, 2, 3]:
    total = total + value
```

```python exec
id: reading-code-that-is-not-a-cell-1
# Your version here
```

<details class="dl-answer"><summary>answer</summary>

Add `total` on its own as the last line, or `print(total)` at the end.
Either one shows 6.

Without one of those, the code runs correctly and shows nothing. That
is question 2 again.

</details>

## A Little Arithmetic

**10.** What do you think each of these gives? Check them in a cell:
`7 / 2`, `7 // 2`, `7 % 2`, `7 ** 2`.

<details class="dl-answer"><summary>answer</summary>

3.5, 3, 1 and 49.

`/` always gives a decimal. `//` rounds the result down to a whole
number. `%` gives what is left over. `**` is a power: 7 to the power of
2.

</details>

**11.** Can you write a cell that shows how many minutes there are in a
week?

<details class="dl-answer"><summary>answer</summary>

```python
7 * 24 * 60
```

The answer is 10080. If you write out the multiplication, and not only
the answer, the next reader can see where the number came from.

</details>

**12.** Can you change the cell at the top of the tutorial page so that
it shows the first five square numbers?

<details class="dl-answer"><summary>answer</summary>

```python
for n in range(1, 6):
    print(n ** 2)
```

1, 4, 9, 16, 25.

</details>
