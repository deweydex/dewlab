---
title: "Asking questions of a table"
slug: asking-questions-of-a-table
module: data
module_title: "Data"
series: first-database
version: 2026.09.05.1
---

# Asking questions of a table

`SELECT *` shows every column. Most questions worth asking are smaller
than that: which rows, and which columns of them. This page builds the
same dinosaur table again, then asks it three different questions.

```sql cell=dinosaurs
CREATE TABLE dinosaurs (
    id INTEGER PRIMARY KEY,
    name TEXT,
    diet TEXT,
    length_meters REAL,
    period TEXT
);

INSERT INTO dinosaurs (name, diet, length_meters, period) VALUES
    ('Tyrannosaurus Rex', 'Carnivore', 12.3, 'Late Cretaceous'),
    ('Triceratops', 'Herbivore', 9.0, 'Late Cretaceous'),
    ('Velociraptor', 'Carnivore', 2.0, 'Late Cretaceous'),
    ('Brachiosaurus', 'Herbivore', 25.0, 'Late Jurassic'),
    ('Stegosaurus', 'Herbivore', 9.0, 'Late Jurassic'),
    ('Allosaurus', 'Carnivore', 9.7, 'Late Jurassic');
```

Run that box first; it only builds the table, so nothing appears yet.

## Naming columns

```sql cell=dinosaurs
SELECT name, length_meters FROM dinosaurs;
```

This asks for two columns instead of five. Name the columns you want,
separated by commas, in place of `*`.

## WHERE: keeping only some rows

```sql cell=dinosaurs
SELECT name, length_meters FROM dinosaurs WHERE diet = 'Carnivore';
```

`WHERE` keeps a row only if the condition after it is true for that row.
Text in a condition goes in single quotes, the way `'Carnivore'` does
above. A number needs no quotes: try changing the box to
`WHERE length_meters > 10` and run it again.

## ORDER BY: choosing an order

```sql cell=dinosaurs
SELECT name, length_meters, diet
FROM dinosaurs
WHERE length_meters > 5
ORDER BY length_meters DESC;
```

`ORDER BY` sorts the result by a column. `DESC` puts the largest value
first; `ASC` puts the smallest first, and is also what you get if you
leave the word out. A query can combine `WHERE` and `ORDER BY`, in that
order, the way this one does.

## Why this happens

None of these statements changed the table. `SELECT` only reads; running
the same one twice gives the same rows both times, unless something else
has changed the table in between. That is worth knowing before the next
page, where some statements do change what a table holds.

## Your turn

Your own table, from the last page, is already here.

```sql cell=my-table persist
-- If you built a table on the last page, it is already loaded above.
-- If this is your first time here, write a CREATE TABLE and some
-- INSERT statements of your own, then run them.
```

Try writing three queries against it in the box above:

- One that names only some of its columns.
- One with a `WHERE` that keeps only some rows.
- One with an `ORDER BY`.

Run each in turn and see what comes back. Each run saves what is in the
box, so the next page opens with whatever you last ran here.

## What you have now

- **WHERE** — a condition after a table's name that keeps only the rows
  where it is true.
- **ORDER BY** — sorts a result by one of its columns, `ASC` (the
  default) for smallest first, `DESC` for largest first.
