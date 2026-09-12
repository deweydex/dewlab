---
title: "Exporting a query to a file"
slug: exporting-a-query-to-a-file
module: data
module_title: "Data"
series: several-tables
version: 2026.09.06.1
---

# Exporting a query to a file

Every table on this arc's pages lives only inside this browser tab. A
query's result leaving as a file of its own — something you could open
in a spreadsheet, attach to an email, or hand to a different program
entirely — needs one more step.

Load the income table again, the same way the earlier pages did.

```py cell=income-share
import sql_tools

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
connection = sql_tools.get_connection("income-share")
income_share.to_sql("income_share", connection, if_exists="replace", index=False)
```

## Building the file you want to keep

Run the query first, and look at what it returns, before saving it —
the file you export should be exactly the rows you meant to keep, not
a whole table's worth by accident.

```py cell=income-share
ireland = read_sql(
    "income-share",
    "SELECT year, share_extrapolated FROM income_share "
    "WHERE country = 'Ireland' ORDER BY year",
)
ireland.head()
```

## Saving it as a file

```py cell=income-share
download_csv(ireland, "ireland-income-share.csv")
```

Running this cell saves `ireland-income-share.csv` to this device the
same way clicking a download link anywhere else would. Open it in a
spreadsheet program afterwards, and the columns are exactly the ones
the query selected.

## Why this needs its own step

A SQL cell's own Download button, seen on earlier pages, saves the
cell's own text — the query itself, not what it returned.
`download_csv` saves the other half: the rows a query produced, ready
for something that is not this page at all.

## Your turn

Write a query of your own against `income_share` — a different country,
or every country in one particular year — and export it with
`download_csv`, under a filename that says what it holds.

## What you have now

- **`download_csv`** — saves a DataFrame as a CSV file on this device,
  the same way any other download does.
- **A query's result, not its text** — `download_csv` exports what a
  query returned; a SQL cell's own Download button exports the query
  itself. Different things, both useful, saved differently.
