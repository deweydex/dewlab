---
title: "Charting a Query's Result"
slug: charting-a-querys-result
module: database-methods
module_title: "Database Methods"
year: "2026-2027"
series: several-tables
version: 2026.09.10.1
covers:
  from-select-to-dataframe:
    touches: [DBM-LO5]
  one-line-per-country:
    touches: [DBM-LO7]
---

# Charting a Query's Result

A table of numbers and a chart of the same numbers answer different
questions. The table says exactly what one row holds; the chart shows what
changed, and when, at a glance. This page turns a query's result into a
line chart, one line per country.

Load the income table again, the same way the last two pages did.

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

## Checking what names the data uses

A query does not have to build anything to be useful. Before picking
countries to chart, this one simply asks what country names the dataset
already holds.

```sql exec
id: list-income-share-countries
SELECT DISTINCT country FROM income_share ORDER BY country;
```

## From SELECT to DataFrame

`pandas.read_sql` runs a query against the database and returns a
DataFrame. It does the opposite of `to_sql`: going from a table back into
Python, rather than from Python into a table.

```python exec
id: query-income-share-for-chart
import pandas as pd
import matplotlib.pyplot as plt

countries = ["Ireland", "Sweden", "United States", "Japan"]
# each name needs quotes of its own, so SQL reads it as text, not as code
placeholders = ", ".join(f"'{country}'" for country in countries)
result = pd.read_sql(
    f"SELECT country, year, share_extrapolated FROM income_share "
    f"WHERE country IN ({placeholders}) AND year >= 1980 ORDER BY country, year",
    db,
)
result.head()
```

## One line per country

```python exec
id: plot-income-share-by-country
for country, rows in result.groupby("country"):
    plt.plot(rows["year"], rows["share_extrapolated"], label=country)

plt.xlabel("Year")
plt.ylabel("Top 1% share of pre-tax income")
plt.title("Income going to the richest 1%, by country")
plt.legend()
```

`result.groupby("country")` splits the DataFrame into one smaller table per
country. Each pass through the loop plots one line and labels it;
`plt.legend()` at the end collects every label a `plt.plot` call gave it.
A cell's last line renders automatically here, the same as a DataFrame
does, so this cell needs no separate `plt.show()` call.

## Reading the chart

Some countries climb steadily. Others sit fairly flat for decades, then
move. A chart like this raises a question more than it answers one. A bend
in a line could come from a bank crisis, a change in tax law, or a data
source that changed partway through. The chart alone does not say which.

## Your turn

Change the `countries` list to four countries of your own choosing. Run the
query above again if you are not sure a name is spelled the way the dataset
expects. Look for the country whose line moves the most, and the one that
barely moves at all.

## What you have now

- **A DataFrame becomes a chart directly.** No separate conversion step:
  matplotlib reads columns straight out of a DataFrame.
- **`groupby`.** Splits one table into a smaller table per group, ready for
  a loop that treats each group on its own.
- **A chart raises questions.** A bend in a line says something changed; a
  chart does not say what.
