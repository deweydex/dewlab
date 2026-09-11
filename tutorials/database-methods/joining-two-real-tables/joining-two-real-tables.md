---
title: "Joining Two Real Tables"
slug: joining-two-real-tables
module: database-methods
module_title: "Database Methods"
year: "2026-2027"
series: several-tables
version: 2026.09.10.1
---

# Joining Two Real Tables

[A second table and a join](tutorial:a-second-table-and-a-join) showed what
a `JOIN` does, on two tables built by hand, with no messy edges. Real tables
rarely match up that cleanly. This page joins the income dataset from the
last page to a second table, and one row in three goes missing. That happens
on purpose, so the reason is visible before it becomes a surprise somewhere
else.

Load the income table again, the same way the last page did.

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

## A second table, written by hand

A short table names which region each country belongs to. This one is small
enough to type directly as SQL, the same way `sightings` was on the earlier
page.

```sql exec
id: create-country-regions
CREATE TABLE country_regions (
    country TEXT PRIMARY KEY,
    region TEXT
);

INSERT INTO country_regions (country, region) VALUES
    ('Ireland', 'Europe'),
    ('Sweden', 'Europe'),
    ('France', 'Europe'),
    ('USA', 'North America'),
    ('Japan', 'Asia'),
    ('Brazil', 'South America'),
    ('South Africa', 'Africa');
```

## The join that loses a row

```sql exec
id: join-income-share-and-regions
SELECT income_share.country, income_share.year, income_share.share_extrapolated, country_regions.region
FROM income_share
JOIN country_regions ON income_share.country = country_regions.country
WHERE income_share.year = 2019
ORDER BY income_share.country;
```

Six countries went into `country_regions`. Run the query above and count
the countries that came back. One is missing. `income_share` spells that
country "United States"; `country_regions` spells it "USA". A `JOIN`
matches on exact text, not on what a person would recognise as the same
country, so two rows that mean the same thing with different spelling never
meet.

## Seeing what a JOIN drops

`LEFT JOIN` keeps every row from `income_share`, whether or not
`country_regions` has a matching one. Where it does not, `region` comes back
empty rather than the row disappearing.

```sql exec
id: left-join-income-share-and-regions
SELECT income_share.country, income_share.year, country_regions.region
FROM income_share
LEFT JOIN country_regions ON income_share.country = country_regions.country
WHERE income_share.year = 2019
  AND income_share.country IN ('Ireland', 'Japan', 'United States')
ORDER BY income_share.country;
```

United States now appears, with `region` blank. That blank is the mismatch,
made visible instead of silently dropped. Agreeing on one spelling is the
fix here, not a cleverer `JOIN`. Change `'USA'` to `'United States'` in the
`INSERT` above and re-run both cells; the first query then returns all six
countries.

## Your turn

Add one more country to `country_regions`, using the exact spelling
`income_share` uses for it (check with a quick `SELECT DISTINCT country
FROM income_share` first, if you are not sure). Then write a query that
joins the two tables and shows only that country's rows from the last five
years.

## What you have now

- **A join that drops a row.** This happens whenever the two tables spell
  the same thing differently, not because the data itself is wrong.
- **`LEFT JOIN`.** It keeps every row from the first table, filling in
  empty where the second table has no match, so a mismatch shows up
  instead of vanishing.
- **Fixing the spelling, not the query.** Agreeing on one name for the same
  thing is usually the real fix, once a `LEFT JOIN` shows where the gap is.
