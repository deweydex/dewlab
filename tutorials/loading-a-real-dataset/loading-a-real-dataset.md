---
title: "Loading a CSV dataset into a SQL table"
year: "2026-2027"
version: 2026.09.23.1
covers:
  fetching-a-csv-from-a-python-cell:
    covers: [DBM-LO8]
  querying-it-as-sql:
    touches: [DBM-LO5]
datasets: [income-share-top-1]
---

# Loading a CSV dataset into a SQL table

Real data almost never starts as a database table. It starts as a file, most
often a *CSV*. A CSV holds rows of plain text, one line per record, with each
value separated by a comma. Turning a CSV into a table you can query is where
this page starts.

The dataset below is real: how much of a country's income before tax goes to
the richest 1% of its people, by year. It comes from the [World Inequality
Database](https://ourworldindata.org/how-has-income-inequality-within-countries-evolved-over-the-past-century),
published through Our World in Data under a Creative Commons licence that
allows reuse with credit.

## Fetching a CSV from a Python cell

`load_csv` is already in every Python cell's own toolbox. Give it an address
and it returns a table you can work with.

```python exec
id: fetch-income-share
income_share = await load_csv(
    "https://ourworldindata.org/grapher/income-share-top-1-before-tax-wid-extrapolations.csv"
    "?v=1&csvType=full&useColumnShortNames=true"
)
income_share.head()
```

`load_csv` needs `await` in front of it, because fetching a file over the
network takes a moment, and Python waits for it rather than running ahead
with no data yet.

## Cleaning: names, and what is missing

The columns arrive with the dataset's own working names. Renaming them is
the first cleaning step, and a common one: a column's short code is fine for
the people who built the dataset, and confusing for anyone reading a query
later.

```python exec
id: rename-income-share-columns
income_share = income_share.rename(columns={
    "Entity": "country",
    "Code": "country_code",
    "Year": "year",
    "p99p100_share_pretax": "share",
    "p99p100_share_pretax_extrapolated": "share_extrapolated",
})
income_share[["country", "year", "share", "share_extrapolated"]].head()
```

The second cleaning step is checking what is missing, before building
anything on top of it.

```python exec
id: check-missing-values
income_share["share"].isna().sum(), income_share["share_extrapolated"].isna().sum()
```

`share` is missing for thousands of rows. The original survey data simply
does not reach every country in every year. `share_extrapolated` fills those
gaps with an estimate, worked out from related data, so it is missing far
less often. The rest of this series uses `share_extrapolated`, and says so
at each query, rather than treating an estimate as if it were the same thing
as a measurement.

## Into a table

A DataFrame becomes a database table only once you put it into one.
`pandas.DataFrame.to_sql` does that, writing into `db`, the same shared
connection a `` ```sql exec `` block on this page already uses.

Notice the two names. In Python, the DataFrame is still `income_share`.
The table it becomes is `income_share_tbl`, following the same naming
convention as `dinosaur_tbl`. The columns keep the names we gave them
while cleaning.

```python exec
id: income-share-to-sql
income_share.to_sql("income_share_tbl", db, if_exists="replace", index=False)
```

`if_exists="replace"` means running this cell again starts the table fresh,
rather than failing because it is already there. That's useful while you
are still working out what the table should hold.

## Querying it as SQL

You can query the table with `SELECT`, the same as any other table.

```sql exec
id: query-income-share-by-country
SELECT country, year, share_extrapolated
FROM income_share_tbl
WHERE country IN ('Ireland', 'Sweden', 'United States')
  AND year >= 1990
ORDER BY country, year
LIMIT 15;
```

## Your turn

Pick two or three countries of your own — a country you have lived in, one
you would like to visit, one that came up in another class. Change the
`country IN (...)` list above to yours, then run the query again. Look for a
country whose numbers move up and down sharply between years, next to one
that stays fairly steady. The next page joins this table to a second one;
keep your chosen countries in mind for that.

## What you have now

- **A CSV holds rows of data, separated by commas.** It's the plain-text
  shape most real datasets arrive in.
- **`load_csv`.** Fetches a CSV from a web address and returns it as a table
  you can work with in Python.
- **Cleaning renames columns to plain names, then checks what is missing.**
  Both happen before building a query on top of the data.
- **`to_sql`.** Writes a table built in Python into the page's shared
  database connection, so `SELECT` now works on the same data.

## Where to read more

Stand-up Maths (2020). *UK Government loses data because of Excel
mistake.* <https://www.youtube.com/watch?v=zUp8pkoeMss>. In 2020,
thousands of COVID-19 test results in England were missed because a file
format had no room for more rows. Matt Parker explains what is known.
About sixteen minutes.
