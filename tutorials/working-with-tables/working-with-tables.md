---
title: "A table in Python, with pandas"
year: "2026-2027"
version: 2026.09.22.1
covers:
  keeping-only-some-rows:
    touches: [DBM-LO5]
---

# A table in Python, with pandas

So far, every table we have made has lived in the database, and SQL has
asked it our questions. Real data often starts somewhere else. On the
next page, [Loading a Real Dataset](tutorial:loading-a-real-dataset), we
load a real file into Python, clean it up there, and only then put it
into the database.

To do that, Python needs a table of its own. *pandas* is a library for
working with tables of data in Python. A *library* is a collection of
ready-made code that we can load and use. A *DataFrame* is the table
that pandas holds in Python's memory. Like a database table, it has
named columns and one row for each record.

On this page we:

- build a small DataFrame, and look at it
- ask it a question, the way `WHERE` does in SQL
- check an answer with `check()`

## A Python cell

This page uses Python cells, not SQL boxes. A Python cell works in the
same way: press **Run**, or hold Ctrl and press Enter, and the result
appears under it. Reset brings back the code the page started with.

A Python cell shows two things under it: anything the code prints, and
the value of its last line.

## A small table of readings

The cell below makes a table of temperature readings, in degrees
Celsius, from four sites in Ireland. Each site has two readings: one in
the morning, and one in the evening. Run the cell, and the table
appears.

```python exec
id: setup
{{include: setup/load_readings.py}}
readings
```

Here is what each part of the cell does:

- `import pandas as pd` loads the pandas library, and gives it the short
  name `pd`.
- `readings = pd.DataFrame(...)` makes a DataFrame and gives it the name
  `readings`. Later cells use that name, in the same way that SQL uses a
  table's name after `FROM`.
- Inside, each line gives one column: its name in quotes, a colon, then
  the column's values in square brackets, one for each row, in order.
- The last line, `readings`, is the value the cell shows.

Did you notice the difference from `INSERT`? In SQL we wrote the table
one row at a time. Here we wrote it one column at a time. The table
that comes out has the same shape either way: four rows and three
columns.

The numbers down the left side, 0 to 3, are the row labels that pandas
adds. They count from 0, not from 1. They are not one of the table's
columns.

## Keeping only some rows

Which sites had an evening reading above 14 degrees? In SQL, we would
ask with `WHERE`:

```sql
SELECT * FROM readings WHERE evening > 14;
```

In pandas, we start from the column. `readings["evening"]` is the
`evening` column on its own. What do you think this cell shows? Run it
to check.

```python exec
id: compare-evening
readings["evening"] > 14
```

The cell shows one answer for each row: `True` where the evening
reading is above 14, and `False` where it is not. The comparison runs
on the whole column at once.

Now we can use those answers to keep only the rows marked `True`. We put
the comparison inside `readings[...]`:

```python exec
id: filter-evening
hint: Try readings["evening"] > 14 on its own first, to see the shape of the answer.
readings[readings["evening"] > 14]
```

Two sites are left, Cork and Wexford. This line does the same job as
the `WHERE` query above.

Here are some SQL questions you know, next to the pandas way of asking
them:

| In SQL | In pandas |
|---|---|
| `SELECT * FROM readings;` | `readings` |
| `SELECT * FROM readings WHERE evening > 14;` | `readings[readings["evening"] > 14]` |
| `SELECT * FROM readings ORDER BY evening;` | `readings.sort_values("evening")` |
| `SELECT COUNT(*) FROM readings;` | `len(readings)` |

## Your turn

Which sites had a morning reading of 10 degrees or more? Write the
pandas line in the cell below. `>=` means "greater than or equal to",
as it does in SQL.

```python exec
id: your-turn-filter-readings
hint: Start from the filter-evening cell. Change the column name, the comparison and the number.
# Your filter here
```

## Checking your own answer

Some cells can tell you whether you have found the right value. You met
`check()` in the quizzes earlier in this course. Here too, nothing is
recorded or graded: the answer is for you, and nobody else sees it.

`readings["morning"].mean()` works out the mean, or average, of the
`morning` column. Is it 10.85? Run the cell to check.

```python exec
id: check-mean
hint: The mean of a column is readings["morning"].mean().
check(readings["morning"].mean(), 10.85)
```

## What you have now

- **pandas** is a library for working with tables of data in Python.
- **A DataFrame** is a pandas table, with named columns and one row for
  each record.
- **`readings["evening"]`** picks out one column.
- **`readings[readings["evening"] > 14]`** keeps only the rows where the
  comparison is `True`, like `WHERE` in SQL.

Next, [Loading a Real Dataset](tutorial:loading-a-real-dataset) fills a
DataFrame from a real file, with thousands of rows, and then writes it
into the database so that SQL can query it.

## Where to Read More

Corey Schafer (2020). *Python Pandas Tutorial (Part 4): Filtering — Using
Conditionals to Filter Rows and Columns.*
<https://www.youtube.com/watch?v=Lw2rlcxScZY>. The exact operation this page
teaches — selecting rows with a comparison — worked through on a different
dataset.

pandas development team. *10 minutes to pandas.*
<https://pandas.pydata.org/docs/user_guide/10min.html>. The official quick
tour of the DataFrame, for the parts this page did not have room to cover.
