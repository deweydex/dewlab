---
title: "Working With a Table — Practice"
slug: working-with-tables-practice
practice_for: working-with-tables
module: computational-methods
module_title: "Computational Methods"
year: "2026-2027"
series: python-fundamentals
version: 2026.08.23.1
---

# Working With a Table — Practice

Answers are folded. The table is the same four rows the tutorial uses, so every answer here can be checked by counting on your fingers — which is exactly why it is a good table to learn on.

## The Table

```python exec
id: the-table-1
{{include: setup/load_readings.py}}
readings
```

**1.** How many rows and columns does the table have? Find out two ways.

<details class="dl-answer"><summary>answer</summary>

Four rows and three columns.

```python
print(readings.shape)      # (4, 3)
print(len(readings))       # 4 — len counts rows
print(readings.columns)    # the column names
```

`len` on a DataFrame gives rows rather than columns, which is worth knowing before you rely on it.

</details>

**2.** Show just the `evening` column. What kind of thing is it?

<details class="dl-answer"><summary>answer</summary>

```python
readings["evening"]
```

A Series — one column with its index attached. A DataFrame is a collection of Series sharing an index, and most single-column operations give a Series back.

</details>

**3.** Show the row for Sligo.

<details class="dl-answer"><summary>answer</summary>

```python
readings[readings["site"] == "Sligo"]
```

That returns a one-row DataFrame. To get the values themselves:

```python
readings.set_index("site").loc["Sligo"]
```

The first is filtering, the second is looking up. Both are useful and they return different shapes.

</details>

## Asking Questions

**4.** What does `readings["evening"] > 14` produce on its own?

<details class="dl-answer"><summary>answer</summary>

Four True/False values, one per row: True, False, False, True.

The comparison applies to the whole column at once. That is the key idea in pandas — you write the condition once and it is evaluated for every row.

</details>

**5.** Find the sites where the evening reading was above 14. Then where the morning reading was below 10.

<details class="dl-answer"><summary>answer</summary>

```python
readings[readings["evening"] > 14]        # Cork and Wexford
readings[readings["morning"] < 10]        # Sligo
```

The mask goes inside the square brackets and keeps the rows where it is True.

</details>

**6.** Find the sites where the morning reading was above 10 *and* the evening above 14.

<details class="dl-answer"><summary>answer</summary>

```python
readings[(readings["morning"] > 10) & (readings["evening"] > 14)]
```

Cork and Wexford.

Two things differ from ordinary Python. The operator is `&` rather than `and`, and each condition needs its own brackets — without them, `&` binds tighter than `>` and the whole thing fails with a confusing message about ambiguous truth values.

</details>

**7.** Find the sites where the temperature rose by more than 3 degrees.

<details class="dl-answer"><summary>answer</summary>

```python
rise = readings["evening"] - readings["morning"]
readings[rise > 3]
```

Cork rose 3.4, Galway 3.5, Sligo 2.3, Wexford 2.9 — so Cork and Galway.

Subtracting two columns gives a new column of the row-by-row differences. No loop anywhere.

</details>

**8.** Add the rise as a new column, then show the table sorted by it.

<details class="dl-answer"><summary>answer</summary>

```python
readings["rise"] = readings["evening"] - readings["morning"]
readings.sort_values("rise", ascending=False)
```

Galway, Cork, Wexford, Sligo.

`sort_values` returns a new table and leaves the original order alone, which is nearly always what you want.

</details>

## Summarising

**9.** Find the mean, minimum and maximum of the morning column.

<details class="dl-answer"><summary>answer</summary>

10.85, 9.7, and 12.2.

```python
readings["morning"].mean(), readings["morning"].min(), readings["morning"].max()
```

</details>

**10.** Get every summary statistic at once.

<details class="dl-answer"><summary>answer</summary>

```python
readings.describe()
```

Count, mean, standard deviation, minimum, the three quartiles and the maximum, for each numeric column. It skips the `site` column, because none of those questions mean anything for text.

</details>

**11.** Which site was warmest in the evening? Answer without reading the table.

<details class="dl-answer"><summary>answer</summary>

```python
readings.loc[readings["evening"].idxmax(), "site"]
```

Wexford, at 15.1.

`idxmax` gives the index of the largest value rather than the value itself, which is what lets you look up something else in the same row. Asking for `readings["evening"].max()` tells you 15.1 and not whose it is.

</details>

**12.** What does `readings["morning"].mean()` give if one reading is missing?

<details class="dl-answer"><summary>answer</summary>

The mean of the values that are present. pandas skips missing values by default rather than propagating them.

That is convenient and it is a decision made on your behalf. If three of four readings are missing, the mean of the fourth is reported with no warning at all, and `readings["morning"].count()` is how you find out how many went into it.

</details>

## Checking Yourself

```python exec
id: checking-yourself-1
check(readings["evening"].mean(), 13.875)
```

**13.** Use `check` to confirm the mean rise across all four sites.

<details class="dl-answer"><summary>answer</summary>

```python
check((readings["evening"] - readings["morning"]).mean(), 3.025)
```

The rises are 3.4, 3.5, 2.3 and 2.9, averaging 3.025.

Note this equals the difference of the two means — 13.875 − 10.85. Averaging is linear, so the mean of the differences is the difference of the means, and that is true for any two columns.

</details>

**14.** `check` compares with a tolerance rather than exactly. Why does that matter here?

<details class="dl-answer"><summary>answer</summary>

Because decimals are stored in binary, and arithmetic on them does not always land exactly where it should.

The mean rise in the previous question is a live example. It comes out as `3.0250000000000004`, so `== 3.025` is `False` and the correct answer would be marked wrong. The evening mean, by contrast, is exactly 13.875 — some of these come out clean and some do not, and there is no way to tell which in advance.

That is the argument for a tolerance rather than an equals sign on anything measured.

</details>

**15.** Write a check that would pass for a wrong answer, and say why that is a problem.

<details class="dl-answer"><summary>answer</summary>

A tolerance wide enough to swallow the mistake:

```python
check(readings["morning"].mean(), 11, tolerance=1)
```

10.85 passes, and so would 11.9.

A check with a loose tolerance is worse than no check, because it reports success. The tolerance should be as small as the arithmetic allows — big enough for floating point, and no bigger.

</details>
