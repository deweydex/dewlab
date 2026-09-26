---
title: "Joining real tables: the rows a JOIN drops"
year: "2026-2027"
version: 2026.09.26.1
covers:
  a-second-table-written-by-hand:
    touches: [DBM-LO9]
  the-join-that-loses-a-row:
    covers: [DBM-LO5]
datasets: [income-share-top-1]
---

# Joining real tables: the rows a JOIN drops

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
income_share.to_sql("income_share_tbl", db, if_exists="replace", index=False)
```

## A second table, written by hand

A short table names which region each country belongs to. This one is small
enough to type directly as SQL, the same way `sighting_tbl` was on the
earlier page.

Its key is `country`, not a `country_region_id`. Why? The join matches on
the country's name, and the income table already calls that column
`country`, the name we gave it while cleaning. A foreign key and the key
it points at share one name, so the key here takes the name the data
already uses.

The box starts with `DROP TABLE IF EXISTS`, which deletes the table if an
earlier run left one behind. That lets you change a row and run the box
again, which you will do further down this page.

```sql exec
id: create-country-regions
DROP TABLE IF EXISTS country_region_tbl;

CREATE TABLE country_region_tbl (
    country TEXT PRIMARY KEY,
    region TEXT
);

INSERT INTO country_region_tbl (country, region) VALUES
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
SELECT income_share_tbl.country, income_share_tbl.year,
       income_share_tbl.share_extrapolated, country_region_tbl.region
FROM income_share_tbl
JOIN country_region_tbl ON income_share_tbl.country = country_region_tbl.country
WHERE income_share_tbl.year = 2019
ORDER BY income_share_tbl.country;
```

Seven countries went into `country_region_tbl`. Run the query above and
count the countries that came back. One is missing. `income_share_tbl` spells that
country "United States"; `country_region_tbl` spells it "USA". A `JOIN`
matches on exact text, not on what a person would recognise as the same
country, so two rows that mean the same thing with different spelling never
meet.

## Seeing what a JOIN drops

`LEFT JOIN` keeps every row from `income_share_tbl`, whether or not
`country_region_tbl` has a matching one. Where it does not, `region` comes back
empty rather than the row disappearing.

```sql exec
id: left-join-income-share-and-regions
SELECT income_share_tbl.country, income_share_tbl.year, country_region_tbl.region
FROM income_share_tbl
LEFT JOIN country_region_tbl ON income_share_tbl.country = country_region_tbl.country
WHERE income_share_tbl.year = 2019
  AND income_share_tbl.country IN ('Ireland', 'Japan', 'United States')
ORDER BY income_share_tbl.country;
```

United States now appears, with `region` blank. That blank is the mismatch,
made visible instead of silently dropped. Agreeing on one spelling is the
fix here, not a cleverer `JOIN`. Change `'USA'` to `'United States'` in the
`INSERT` above, then re-run both cells; the first query now returns all
seven countries.

## Your turn

Add one more country to `country_region_tbl`, using the exact spelling
`income_share_tbl` uses for it (check with a quick `SELECT DISTINCT country
FROM income_share_tbl` first, if you are not sure). Then write a query that
joins the two tables and shows only that country's rows from the last five
years.

## What you have now

- **A join can drop a row.** This happens whenever the two tables spell
  the same thing differently, not because the data itself is wrong.
- **`LEFT JOIN` keeps every row from the first table.** It fills in
  empty where the second table has no match, so a mismatch shows up
  instead of vanishing.
- **Fixing the spelling is usually the real fix, not a cleverer query.**
  That works once a `LEFT JOIN` shows where the gap is.
