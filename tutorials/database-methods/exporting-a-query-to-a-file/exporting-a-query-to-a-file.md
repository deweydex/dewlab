---
title: "Exporting a Query to a File"
slug: exporting-a-query-to-a-file
module: database-methods
module_title: "Database Methods"
year: "2026-2027"
series: several-tables
version: 2026.09.10.1
covers:
  saving-it-as-a-file:
    covers: [DBM-LO7]
---

# Exporting a Query to a File

Every table on the pages in this series lives only inside this browser tab.
A query's result can also leave as a file of its own: something you could
open in a spreadsheet, attach to an email, or hand to a different program
entirely. That needs one more step.

Load the income table again, the same way the earlier pages did.

```python exec
id: rebuild-income-share
income_share = await load_csv(
    "https://ourworldindata.org/grapher/income-share-top-1-before-tax-wid-extrapolations.csv"
    "?v=1&csvType=full&useColumnShortNames=true"
)
income_share = income_share.rename(columns={
    "Entity": "country",
    "Code": "country_code",
    "Year": "year",
    "p99p100_share_pretax": "share",
    "p99p100_share_pretax_extrapolated": "share_extrapolated",
})
income_share.to_sql("income_share", db, if_exists="replace", index=False)
```

## Building the file you want to keep

Run the query first, and look at what it returns, before saving it. The
file you export should be exactly the rows you meant to keep, not a whole
table's worth by accident.

```sql exec
id: query-ireland-income-share
SELECT year, share_extrapolated FROM income_share
WHERE country = 'Ireland'
ORDER BY year;
```

## Pulling the result into Python

pandas can run that same query and return a DataFrame, ready to turn
into a file.

```python exec
id: ireland-income-share-as-dataframe
import pandas as pd

ireland = pd.read_sql(
    "SELECT year, share_extrapolated FROM income_share WHERE country = 'Ireland' ORDER BY year",
    db,
)
ireland.head()
```

## Saving it as a file

`to_csv` turns a DataFrame back into the same plain-text shape a CSV file
holds.

```python exec
id: ireland-income-share-as-csv
print(ireland.to_csv(index=False))
```

The lines above are exactly what a file named `ireland-income-share.csv`
would hold. Copy them into a new file in a text editor, then save it with a
`.csv` ending. A spreadsheet program then opens that file as a proper
table.

## Why this needs its own step

A query and the rows it returns are two different things. The SQL above is
a few lines of code; `ireland` is the table those lines produced. Saving
the code is not the same as saving the numbers. This page's whole point is
turning the numbers themselves into something you can keep, outside the
browser tab that ran the query.

## Your turn

Write a query of your own against `income_share`: perhaps a different
country, or every country in one particular year. Pull it into a DataFrame
the same way as above, then print its `to_csv()` text to see the file it
would become.

## What you have now

- **`to_csv`.** Turns a DataFrame back into the same plain-text shape a CSV
  file holds.
- **A query's result is not the same as its text.** The SQL that built a
  table and the rows it returned are two different things worth keeping
  separately; this page exports the second.
