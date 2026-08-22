---
title: "Working With a Table"
slug: working-with-tables
module: computational-methods
module_title: "Computational Methods"
year: "2026-2027"
series: python-fundamentals
version: 1
---

# Working With a Table

A single number is rarely what you are working with. This tutorial introduces
the *DataFrame* — a table of rows and columns, which is how pandas, a library
for handling tabular data, holds a dataset in memory.

## The shared table

Several tutorials in this series use the same small set of temperature
readings, so it lives in one file and is pulled into whichever tutorial needs
it. Run the cell to load it.

```python exec
id: setup
{{include: setup/load_readings.py}}
readings
```

A DataFrame renders as a table rather than as text, which makes it much easier
to see what you have.

## Asking a question of the table

How might you find the sites where the evening reading rose above fourteen
degrees? A comparison applies to a whole column at once, giving one answer per
row, and that result can be used to select the rows you want.

```python exec
id: filter-evening
hint: Try printing readings["evening"] > 14 on its own first, to see the shape of the answer.
readings[readings["evening"] > 14]
```

## Checking your own answer

Some cells can tell you whether you have arrived at the right value. Nothing is
recorded and nothing is graded — the feedback is there for you, not for anyone
else.

```python exec
id: check-mean
hint: The mean of a column is readings["morning"].mean().
check(readings["morning"].mean(), 10.85)
```

If you would rather go back to where this series started, the
[first tutorial](tutorial:first-steps) is still there.
