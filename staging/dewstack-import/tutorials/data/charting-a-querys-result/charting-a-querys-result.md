---
title: "Charting a query's result"
slug: charting-a-querys-result
module: data
module_title: "Data"
series: several-tables
version: 2026.09.06.1
---

# Charting a query's result

A table of numbers and a chart of the same numbers answer different
questions. The table says exactly what one row holds; the chart shows
what changed, and when, at a glance. This page turns a query's result
into a line chart, one line per country.

Load the income table again, the same way the last two pages did.

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

## From SELECT to DataFrame

`read_sql` runs a query against a SQL cell's own table and hands back a
DataFrame — `to_sql`'s opposite number, going from a table back to
Python rather than from Python into a table.

```py cell=income-share
import matplotlib.pyplot as plt

countries = ["Ireland", "Sweden", "United States", "Japan"]
placeholders = ", ".join(f"'{country}'" for country in countries)
result = read_sql(
    "income-share",
    f"SELECT country, year, share_extrapolated FROM income_share "
    f"WHERE country IN ({placeholders}) AND year >= 1980 ORDER BY country, year",
)
result.head()
```

## One line per country

```py cell=income-share
for country, rows in result.groupby("country"):
    plt.plot(rows["year"], rows["share_extrapolated"], label=country)

plt.xlabel("Year")
plt.ylabel("Top 1% share of pre-tax income")
plt.title("Income going to the richest 1%, by country")
plt.legend()
```

`result.groupby("country")` splits the DataFrame into one smaller table
per country. Each pass through the loop plots one line and labels it;
`plt.legend()` at the end reads back every label a `plt.plot` call gave
it. A cell's last line renders automatically here, the same as a
DataFrame does — no `plt.show()` needed.

## Reading the chart

Some countries climb steadily. Others sit fairly flat for decades, then
move. A chart like this raises a question more than it answers one. A
bend in a line might come from a bank crisis, a change in tax law, or a
data source that changed partway through — the chart alone cannot say
which.

## Your turn

Change the `countries` list to four countries of your own choosing —
check `SELECT DISTINCT country FROM income_share` first if you are not
sure a name is spelled the way the dataset expects. Run both cells
again. Look for the country whose line moves the most, and the one that
barely moves at all.

## What you have now

- **DataFrame to chart** — matplotlib reads columns straight out of a
  DataFrame; no separate conversion step.
- **`groupby`** — splits one table into a smaller table per group,
  ready for a loop that treats each group on its own.
- **A chart raises questions** — a bend in a line says something
  changed; a chart does not say what.
