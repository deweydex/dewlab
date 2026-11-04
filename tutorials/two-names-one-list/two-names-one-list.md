---
title: "Two names, one list: a closer look at copying"
year: "2026-2027"
version: 2026.11.04.3
---

# Two names, one list: a closer look at copying

In [Comprehensions, grids and aliasing](tutorial:comprehensions-and-grids#two-names-for-one-list),
`copy = row` did not copy anything, and a change to `copy` appeared in
`row`. Here are two ideas about what `=` does when the value on the right
already has a name. Both are reasonable, and they cannot both be true.

**Idea A.** `other = width` makes a copy. After it, `other` and `width` are
separate, and a change to one does not change the other.

**Idea B.** `other = width` gives the same value a second name. Nothing is
copied.

## An experiment

This cell does the same thing twice: once with a number, and once with a
*list*{.term}.

```python exec
id: an-experiment-1
width = 5
other = width
other = 7
print(width)

row = [5]
other_row = row
other_row[0] = 7
print(row)
```

Idea A says nothing changes: `width` is still 5, and `row` is still `[5]`.

Idea B says something different for each half. In the first half,
`other = 7` gives the name `other` a new value, so `width` still names 5.
In the second half, `row` and `other_row` are two names for one list, and
`other_row[0] = 7` changes that list. So `row` shows the change.

```predict
type: choice

What will the two lines print?

- 5, then [5]
  - This is what idea A predicts: two copies.
- 5, then [7]
  - This is what idea B predicts: one list with two names.
- 7, then [7]
```

Run it. It prints 5, then `[7]`, as idea B predicts. Look at what the
third line of each half does.

- `other = 7` gives the name `other` a new value. The name moves to 7.
  `width` still names 5.
- `other_row[0] = 7` does not give `other_row` a new value. It changes the
  list itself, in place, and `row` names that same list.

With numbers you never see the second name, because a number cannot be
changed in place. A list can change in place, so the second name shows
the change.

Can you change one line of the list half so that `row` stays `[5]`?

<details class="dl-answer"><summary>two changes that do it</summary>

`other_row = row[:]` makes a new list with the same items, so the change
goes to the new list. Or `other_row = [7]`, which, like `other = 7`, moves
the name to a new list and leaves `row` alone.

</details>

## What each idea counts

After `other_row = row`, the two ideas count different things.

Idea A counts two lists, `row` and `other_row`. Each holds `[5]`, and a
change to one list leaves the other as it was.

Idea B counts one list with two names. A change to that list shows under
both names.

For a number, the two ideas give the same result. A number cannot be
changed in place, so one number with two names looks the same as two
numbers. For a list, they differ. `other_row[0] = 7` changes the list in
place. Idea A says `row` is still `[5]`. Idea B says `row` is now `[7]`,
and that is what the experiment printed.

A shared document works in the same way. Two people hold the link to one
document. When one of them edits it, the other sees the edit, because
there is only one document.

## Where else it happens

A *grid*{.term} made with `*` has the same surprise. What will this print?

```python exec
id: where-else-it-happens-1
grid = [[0, 0]] * 2
grid[0][0] = 1
print(grid)
```

```predict
type: choice

What will it print?

- [[1, 0], [0, 0]]
- [[1, 0], [1, 0]]
```

It prints `[[1, 0], [1, 0]]`. `* 2` did not make two rows. It put one row
into the grid twice, with two names: `grid[0]` and `grid[1]`.

Let's change the number after `*`. The slider sets how many rows the grid
has. The last line uses `id()`, which gives each list its own number. Two
names for one list give the same number, so the last line counts how many
different lists the grid holds.

```python exec
id: where-else-it-happens-2
rows = slider("rows", 1, 6, step=1, value=2, id="rows").value

grid = [[0, 0]] * rows
grid[0][0] = 1
print(grid)
print("rows in the grid:", len(grid))
print("different lists in the grid:", len({id(line) for line in grid}))
```

Move the slider from 1 to 6. What happens to the first number as the grid
grows, and what happens to the second? Can you change the cell so that
only the first row shows a 1?

<details class="dl-answer"><summary>one change that does it</summary>

`grid = [[0, 0] for _ in range(rows)]` makes a new row each time round, so
the grid holds as many different lists as it has rows. Here is one answer.
Yours may be different and work too.

</details>

## Where to read more

Ned Batchelder's talk *Facts and Myths about Python Names and Values*
(PyCon 2015) explains names and values with pictures. It is
[on his website, with the slides](https://nedbatchelder.com/text/names1.html).
