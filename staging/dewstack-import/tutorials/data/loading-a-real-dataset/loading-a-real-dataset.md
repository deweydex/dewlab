---
title: "Loading a real dataset"
slug: loading-a-real-dataset
module: data
module_title: "Data"
series: several-tables
version: 2026.09.06.1
---

# Loading a real dataset

Real data almost never starts as a database table. It starts as a file,
most often a CSV — rows of text separated by commas, one line per
record. Turning a CSV into a table you can query is where this page
starts.

The dataset below is real: how much of a country's income before tax
goes to the richest 1% of its people, by year. It comes from the
[World Inequality Database](https://ourworldindata.org/how-has-income-inequality-within-countries-evolved-over-the-past-century),
published through Our World in Data under a Creative Commons licence
that allows reuse with credit.

## Fetching a CSV from a Python cell

`load_csv` is already in every Python cell's own toolbox, next to
`read_sql`. Give it an address and it returns a table you can work with.

```py cell=income-share
income_share = await load_csv(
    "https://ourworldindata.org/grapher/income-share-top-1-before-tax-wid-extrapolations.csv"
    "?v=1&csvType=full&useColumnShortNames=true"
)
income_share.head()
```

`load_csv` needs `await` in front of it, because fetching a file over
the network takes a moment, and Python waits for it rather than running
ahead with no data yet.

## Cleaning: names, and what is missing

The columns arrive with the dataset's own working names. Renaming them
is the first cleaning step, and a common one: a column's short code is
fine for the people who built the dataset, and confusing for anyone
reading a query later.

```py cell=income-share
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

```py cell=income-share
income_share["share"].isna().sum(), income_share["share_extrapolated"].isna().sum()
```

`share` is missing for thousands of rows — the original survey data
simply does not reach every country in every year. `share_extrapolated`
fills those gaps with an estimate, worked out from related data, so it
is missing far less often. The rest of this arc uses
`share_extrapolated`, and says so at each query, rather than treating an
estimate as if it were the same thing as a measurement.

## Into a table

A DataFrame is not a database table until it is put into one.
`pandas.DataFrame.to_sql` does that, writing into the same named
connection a `` ```sql cell= `` block on this page would use.

```py cell=income-share
import sql_tools

connection = sql_tools.get_connection("income-share")
income_share.to_sql("income_share", connection, if_exists="replace", index=False)
```

`if_exists="replace"` means running this cell again starts the table
fresh, rather than failing because it is already there — useful while
you are still working out what the table should hold.

## Querying it as SQL

The table now answers to `SELECT`, the same as any other.

```sql cell=income-share
SELECT country, year, share_extrapolated
FROM income_share
WHERE country IN ('Ireland', 'Sweden', 'United States')
  AND year >= 1990
ORDER BY country, year
LIMIT 15;
```

## Your turn

Pick two or three countries of your own — a country you have lived in,
one you would like to visit, one that came up in another class. Change
the `country IN (...)` list above to yours, and run the query again.
Look for a country whose numbers jump around between years next to one
that stays fairly steady. The next page joins this table to a second
one; keep your chosen countries in mind for that.

## What you have now

- **CSV** — rows of data separated by commas, the plain-text shape most
  real datasets arrive in.
- **`load_csv`** — fetches a CSV from a web address and returns it as a
  table you can work with in Python.
- **Cleaning** — renaming columns to plain names, and checking what is
  missing, before building a query on top of either.
- **`to_sql`** — writes a table built in Python into a named SQL
  connection, so the same data answers to `SELECT`.
