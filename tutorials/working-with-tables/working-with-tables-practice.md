---
title: "A table in Python, with pandas — Practice"
practice_for: working-with-tables
year: "2026-2027"
version: 2026.09.26.1
---

# A table in Python, with pandas — Practice

The answers are hidden in folds under each problem. The table is the
same four rows as on the tutorial page. It is small enough that you can
check every answer by counting on your fingers, and that makes it a good
table to learn on.

## The Table

```python exec
id: the-table-1
{{include: setup/load_readings.py}}
readings
```

**1.** How many rows and columns does the table have? Can you find out
in two different ways?

<details class="dl-answer"><summary>answer</summary>

Four rows and three columns.

```python
print(readings.shape)      # (4, 3)
print(len(readings))       # 4: len counts rows
print(readings.columns)    # the column names
```

`shape` gives the number of rows, then the number of columns. `len()`
on a DataFrame gives the number of rows, not columns. That is worth
knowing before you rely on it.

</details>

**2.** Show only the `evening` column. What kind of thing is it?

<details class="dl-answer"><summary>answer</summary>

```python
readings["evening"]
```

It is a *Series*. A Series is one column, with the row labels down its
left side. A DataFrame is a group of Series that share the same row
labels. Most things you do to a single column give you a Series back.

</details>

**3.** Show the row for Sligo.

<details class="dl-answer"><summary>answer</summary>

```python
readings[readings["site"] == "Sligo"]
```

This gives a DataFrame with one row. It is like
`SELECT * FROM readings WHERE site = 'Sligo';`. Note the two equals
signs: in Python, `==` compares, and a single `=` gives a name to a
value.

To get Sligo's values on their own:

```python
readings.set_index("site").loc["Sligo"]
```

The first way is filtering. The second way is looking up a row by its
label. Both are useful, and they give back different shapes.

</details>

## Asking Questions

**4.** What does `readings["evening"] > 14` give on its own?

<details class="dl-answer"><summary>answer</summary>

Four True or False values, one for each row: True, False, False, True.

The comparison runs on the whole column at once. This is the key idea
in pandas: you write the condition once, and pandas tests it on every
row.

</details>

**5.** Find the sites where the evening reading was above 14. Then find
the sites where the morning reading was below 10.

<details class="dl-answer"><summary>answer</summary>

```python
readings[readings["evening"] > 14]        # Cork and Wexford
readings[readings["morning"] < 10]        # Sligo
```

The comparison goes inside the square brackets. pandas keeps the rows
where it is True.

</details>

**6.** Find the sites where the morning reading was above 10 *and* the
evening reading was above 14.

<details class="dl-answer"><summary>answer</summary>

```python
readings[(readings["morning"] > 10) & (readings["evening"] > 14)]
```

Cork and Wexford.

In SQL you would write `AND`. pandas is different in two ways. The
operator is `&`. And each condition needs its own round brackets.
Without them, Python works out `&` before `>`, and the line fails with
a confusing error message.

</details>

**7.** Find the sites where the temperature rose by more than 3 degrees
from morning to evening.

<details class="dl-answer"><summary>answer</summary>

```python
rise = readings["evening"] - readings["morning"]
readings[rise > 3]
```

Cork rose by 3.4, Galway by 3.5, Sligo by 2.3 and Wexford by 2.9. So
the answer is Cork and Galway.

Subtracting one column from another gives a new column: the difference
on each row. There is no loop anywhere.

</details>

**8.** Add the rise as a new column. Then show the table sorted by it,
largest first.

<details class="dl-answer"><summary>answer</summary>

```python
readings["rise"] = readings["evening"] - readings["morning"]
readings.sort_values("rise", ascending=False)
```

Galway, Cork, Wexford, Sligo.

`ascending=False` puts the largest first, like `ORDER BY rise DESC` in
SQL. `sort_values` gives back a new, sorted table, and leaves
`readings` in its old order. That is nearly always what you want.

</details>

## Summarising

**9.** Find the mean, the smallest value and the largest value of the
`morning` column.

<details class="dl-answer"><summary>answer</summary>

10.85, 9.7 and 12.2.

```python
readings["morning"].mean(), readings["morning"].min(), readings["morning"].max()
```

</details>

**10.** Can you get every summary number at once?

<details class="dl-answer"><summary>answer</summary>

```python
readings.describe()
```

For each column of numbers, this gives the count, the mean, the
standard deviation, the smallest value, the three quartiles and the
largest value. It leaves out the `site` column, because none of those
questions make sense for text.

</details>

**11.** Which site was warmest in the evening? Can you find out without
reading the table yourself?

<details class="dl-answer"><summary>answer</summary>

```python
readings.loc[readings["evening"].idxmax(), "site"]
```

Wexford, at 15.1.

`idxmax` gives the row label of the largest value, not the value
itself. With that label, we can look up something else in the same
row, here the site. `readings["evening"].max()` tells you 15.1, but not
which site it belongs to.

</details>

**12.** What does `readings["morning"].mean()` give if one reading is
missing?

<details class="dl-answer"><summary>answer</summary>

The mean of the values that are there. By default, pandas skips missing
values when it works out a mean.

That is handy, but it is a decision pandas makes for you. If three of
the four readings were missing, pandas would report the fourth one as
the mean, with no warning at all. `readings["morning"].count()` tells
you how many values went into it.

</details>

## Comparing Numbers

```python exec
id: checking-yourself-1
readings["evening"].mean()
```

**13.** What is the mean rise across all four sites? Can you work it out
in Python, and then compare it with the difference between the two
means?

<details class="dl-answer"><summary>answer</summary>

```python
rise = (readings["evening"] - readings["morning"]).mean()
print(rise)
```

The rises are 3.4, 3.5, 2.3 and 2.9, and their mean is 3.025.

Notice that this is the same as the difference between the two means:
13.875 − 10.85. That is true for any two columns. The mean of the
differences is always the difference of the means.

</details>

**14.** Python prints the mean rise as `3.0250000000000004`, and
`rise == 3.025` gives `False`. Why? How could you compare two numbers
like these?

<details class="dl-answer"><summary>answer</summary>

Computers store decimals in binary, so arithmetic on decimals does not
always land exactly where it should. The evening mean, on the other
hand, is exactly 13.875. Some results come out clean and some do not,
and there is no way to tell which in advance.

So compare within a small difference, a *tolerance*, rather than with an
exact `==`. After `import math`, `math.isclose(rise, 3.025)` allows a
tiny difference, and so does `round(rise, 3) == 3.025`.

</details>

**15.** How close is close enough? What does
`math.isclose(readings["morning"].mean(), 11, abs_tol=1)` say, and why is
that a problem?

<details class="dl-answer"><summary>answer</summary>

It gives `True`: 10.85 is within 1 of 11. So would 11.9. A tolerance
wide enough to hide a real difference says two numbers are the same when
they are not. Keep the tolerance as small as the arithmetic needs: big
enough for the tiny errors in decimals, and no bigger.

</details>
