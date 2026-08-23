---
title: "First Steps — Practice"
slug: first-steps-practice
practice_for: first-steps
module: computational-methods
module_title: "Computational Methods"
year: "2026-2027"
series: python-fundamentals
version: 2026.08.23.1
---

# First Steps — Practice

Answers are folded. These are short, and they are mostly about the two things that trip people up in the first hour: what a cell shows you, and what `range` actually produces.

## What a Cell Shows

```python exec
id: what-a-cell-shows-1
hint: Delete the last line and run it again. What changes?
print("printed")
"the value of the last line"
```

**1.** The cell above shows two things. Where does each come from?

<details class="dl-answer"><summary>answer</summary>

`printed` came from the `print`. The quoted string came from the last line being an expression — a cell shows the value of its final line if that line has a value.

Delete the last line and only the printed text remains. Delete the `print` and only the value remains.

</details>

**2.** Predict what each of these cells shows.

- (a) `2 + 3`
- (b) `print(2 + 3)`
- (c) `x = 2 + 3`
- (d) `x = 2 + 3` then `x` on the next line

<details class="dl-answer"><summary>answer</summary>

(a) `5`. (b) `5`. (c) nothing at all. (d) `5`.

(c) is the one to notice. An assignment is an instruction rather than an expression, so it has no value to show. A cell that ends in an assignment looks like it did nothing, and it did the work — it just has nothing to say about it.

</details>

**3.** What does this cell show?

```python
print("one")
print("two")
3 + 4
```

<details class="dl-answer"><summary>answer</summary>

`one`, then `two`, then `7`.

Prints appear in the order they happen; the final value appears at the end. Only the *last* line's value is shown, so putting `1 + 1` on the second line would produce nothing.

</details>

## Running Things

**4.** Change the cell at the top of this page so it prints the numbers 0 to 4. Then 1 to 5.

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

`range(5)` starts at 0 and stops before 5. To start elsewhere, give it two numbers — and the second is still the stopping point rather than the last value.

</details>

**5.** What does `range(3)` actually contain?

<details class="dl-answer"><summary>answer</summary>

0, 1, 2. Three values, and 3 is not one of them.

`list(range(3))` shows them. On its own, `range(3)` displays as `range(0, 3)` rather than as its contents, because it generates the numbers as they are needed rather than storing them.

</details>

**6.** Run a cell, edit it, then press reset. What comes back?

<details class="dl-answer"><summary>answer</summary>

The version the author wrote, not the version you had a minute ago.

Reset is not undo. Anything you want to keep, copy out before pressing it.

</details>

**7.** Two cells, run in order:

```python
total = 10
```

```python
total + 5
```

Does the second one work?

<details class="dl-answer"><summary>answer</summary>

Yes, if the first has been run. Cells share one workspace, and a name defined in one is available in every cell afterwards.

If the second is run first, it raises a `NameError`. That is the most common confusion on a page of cells: the order you *ran* them matters, not the order they appear in.

</details>

## Reading Code That Is Not a Cell

**8.** How can you tell whether a block of code on a page can be run?

<details class="dl-answer"><summary>answer</summary>

It has a Run button. Blocks without one are illustrations to read.

Both are shown the same way otherwise, deliberately: the code in an illustration is real code, and copying it into a cell to try it out is encouraged.

</details>

**9.** Copy this illustration into the cell below and make it show the total.

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

Add `total` on its own as the last line, or `print(total)` at the end. Either shows 6.

Without one of those it runs correctly and displays nothing, which is question 2 all over again.

</details>

## A Little Arithmetic

**10.** Predict, then check: `7 / 2`, `7 // 2`, `7 % 2`, `7 ** 2`.

<details class="dl-answer"><summary>answer</summary>

3.5, 3, 1, 49.

`/` always gives a decimal. `//` gives the whole number of times it goes in, and `%` gives what is left over.

</details>

**11.** Write a cell that shows how many minutes there are in a week.

<details class="dl-answer"><summary>answer</summary>

```python
7 * 24 * 60
```

10080. Writing the multiplication out rather than the answer means the next reader can see where it came from.

</details>

**12.** Write a loop that shows the first five square numbers.

<details class="dl-answer"><summary>answer</summary>

```python
for n in range(1, 6):
    print(n ** 2)
```

1, 4, 9, 16, 25.

</details>
