---
title: "A form that writes a row"
slug: a-form-that-writes-a-row
module: data
module_title: "Data"
series: several-tables
version: 2026.09.06.1
---

# A form that writes a row

Every table on this arc has grown by running SQL directly — an
`INSERT` typed into a cell, or a DataFrame written in with `to_sql`.
Somebody using the finished thing rarely types SQL at all. They fill in
a form, and pressing submit is what turns their answers into a row.

[A form](tutorial:a-form) covers the HTML side of this: a label, an
input, a button, and what makes a form usable rather than merely
present. This page stays on the database side: the query a submission
like that would run, without wiring the two together yet. That wiring —
reading a form's own fields and writing what they held into a table —
is a later, full-stack page; the two pieces it would join already
exist, only the page that joins them does not yet.

## The row a submission would add

A form asking for a country, a year and a share would, once wired up,
run something close to this for every submission:

```sql cell=income-share
CREATE TABLE income_share (
    country TEXT,
    year INTEGER,
    share_extrapolated REAL
);

INSERT INTO income_share (country, year, share_extrapolated)
VALUES ('Ireland', 2024, 0.11);
```

`VALUES ('Ireland', 2024, 0.11)` is exactly what three form fields
become, in order, once their values are read. A form's job is
collecting them from a visitor; a database's job starts where a form's
ends.

## What still has to happen for this to be real

Three things, each already covered somewhere on this site, and none of
them wired together yet:

1. **Reading a form's values.** [A form](tutorial:a-form) builds the
   fields; JavaScript reads what a visitor typed into them.
2. **Turning those values into SQL.** The `INSERT` above, built with
   the values a form collected instead of typed directly.
3. **Running it against a real table.** Everything this arc has
   already done, `` ```sql cell= `` blocks included.

The page that puts these three together is the first of a later,
full-stack arc — a page small enough to still be one page, and the
natural next stop once you have both a form and a table on your own.

## Your turn

Go back to the two-table topic you designed on the first page of this
arc. Pick one table, and write the `INSERT` a form for it would need to
run — the column names in order, and a made-up row of values standing
in for what a visitor might type.

## What you have now

- **A form's `INSERT`** — the query a submission runs, with the form's
  own field values standing in for what was typed by hand elsewhere on
  this arc.
- **Three separate jobs** — reading a form, building a query from what
  it read, and running that query — each already familiar alone, not
  yet joined into one page.
