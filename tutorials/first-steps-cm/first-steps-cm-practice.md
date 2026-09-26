---
title: "Running Python in a cell — Practice"
practice_for: first-steps-cm
year: "2026-2027"
version: 2026.09.26.1
---

# Running Python in a cell — Practice

These short problems are about two things that confuse people in their first hour:
what a cell shows you, and the order cells run in. Try each one before you
open anything under it.

## 1. Two things under one cell

```python exec
id: what-a-cell-shows-1
print("printed")
"the value of the last line"
```

The cell shows two things. Where does each one come from? Delete the last
line and run it again. What changes?

<details class="dl-answer"><summary>answer</summary>

`printed` comes from the `print()`. The text in quotes comes from the last
line, because that line is an expression. A cell shows the value of its
last line, if the line has a value. Delete the last line, and only the
printed text is left. Delete the `print()` line, and only the value is
left.

</details>

## 2. Four cells

What does each of these cells show?

- (a) `2 + 3`
- (b) `print(2 + 3)`
- (c) `x = 2 + 3`
- (d) `x = 2 + 3`, then `x` on the next line

```python exec
id: four-cells-1
2 + 3
```

<details class="dl-answer"><summary>answer</summary>

(a) `5`. (b) `5`. (c) Nothing at all. (d) `5`.

Look closely at (c). A line with `=` is an instruction, so it has no value
to show. A cell that ends with an instruction looks as if it did nothing.
It did the work, but it has nothing to show you.

</details>

## 3. Printed, then shown

```python exec
id: printed-then-shown-1
print("one")
print("two")
3 + 4
```

```predict
What will the last line under the cell be?

- 7
  - The value of the last line comes after everything printed.
- two
  - Printed lines are what a cell shows.
- one
  - The first thing the cell does is the last thing it shows.
```

<details class="dl-answer"><summary>why</summary>

`one`, then `two`, then `7`. Printed lines appear in the order they
happen, and the value of the last line comes at the end. Python shows only
the value of the *last* line. `1 + 1` on the second line would show nothing.

</details>

## 4. Different every time

Run the trailer at the top of the tutorial page twice. Why are the numbers
different? Is either of them wrong?

<details class="dl-answer"><summary>answer</summary>

Each run throws different random darts, so each estimate is a little
different. Neither is wrong. Both are estimates, and with more darts, they
land closer together, and closer to 3.14159…. [Monte Carlo simulation](tutorial:counting-darts)
shows how close they get, and how fast.

</details>

## 5. Clear is not undo

Run a cell, change it, then press **Clear** (↻). What comes back?

<details class="dl-answer"><summary>answer</summary>

You get the code the page started with. The version you had a minute
ago is gone. If you want to keep something, copy it somewhere else
before you press Clear. **Reset** (↺) is different. It clears the
output and leaves your code alone.

</details>

## 6. Two cells in order

```python exec
id: two-cells-in-order-1
total = 10
```

```python exec
id: two-cells-in-order-2
total + 5
```

Does the second cell work? What if it runs before the first?

<details class="dl-answer"><summary>answer</summary>

It shows 15, if the first cell has been run. The cells on a page share one
workspace, so a name made in one can be used in every cell after it. If
the second runs first, it stops with a `NameError`. The order you *ran*
the cells in matters, not the order they appear on the page.

</details>

## 7. Which blocks run

How can you tell whether a block of code on a page can be run?

<details class="dl-answer"><summary>answer</summary>

It has a Run button. A block without one is an illustration, for reading.
Apart from that, the two look alike, on purpose. The code in an
illustration is real, and you are welcome to copy it into a cell to try
it.

</details>

## 8. An illustration, made to show something

Can you copy this illustration into the cell, and make it show the total?

```python
total = 0
for value in [1, 2, 3]:
    total = total + value
```

```python exec
id: reading-code-that-is-not-a-cell-1
# Your version here
```

```solution
total = 0
for value in [1, 2, 3]:
    total = total + value
total
---
`total` on its own as the last line shows 6, and so does `print(total)`.
Without one of them, the code runs correctly and shows nothing: problem
2 again.
```

## 9. Minutes in a week

Can you write a cell that shows how many minutes there are in a week?

```python exec
id: minutes-in-a-week-1

```

```solution
7 * 24 * 60
---
10080. Writing out the multiplication, and not only the answer, lets the
next reader see where the number came from.
```
