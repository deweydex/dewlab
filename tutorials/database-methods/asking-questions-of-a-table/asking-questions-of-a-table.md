---
title: "Asking Questions of a Table"
slug: asking-questions-of-a-table
module: database-methods
module_title: "Database Methods"
year: "2026-2027"
series: first-database
version: 2026.09.10.1
covers:
  naming-columns:
    covers: [DBM-LO3]
  where-keeping-only-some-rows:
    covers: [DBM-LO5]
  order-by-choosing-an-order:
    touches: [DBM-LO5]
---

# Asking Questions of a Table

`SELECT *` shows every column. Most questions worth asking need only some
of the rows and some of their columns. This page builds the same
dinosaur table again, then asks it three different questions.

```sql exec
id: create-dinosaurs-table
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

```sql exec
id: select-name-and-length
SELECT name, length_meters FROM dinosaurs;
```

This asks for two columns instead of five. Name the columns you want,
separated by commas, in place of `*`.

## WHERE: keeping only some rows

```sql exec
id: query-carnivores
SELECT name, length_meters FROM dinosaurs WHERE diet = 'Carnivore';
```

`WHERE` keeps a row only if the condition after it is true for that row.
Text in a condition goes in single quotes, like `'Carnivore'` above. A
number needs no quotes: try changing the box to `WHERE length_meters >
10` and run it again.

```hint
for: query-carnivores
after: 2 empty results

Two runs in a row came back with no rows. Sometimes that means the
table has nothing that matches yet, and sometimes it means the text
after `=` is not written the way the table itself has it.

Look at the value after `WHERE diet =`. Does it match a value in the
`diet` column, letter for letter, including which letters are capital?
SQLite treats `'carnivore'` and `'Carnivore'` as two different pieces
of text, not the same word spelled two ways.
```

```hint
for: query-carnivores
after: 5 empty results
title: some steps

1. Run `SELECT DISTINCT diet FROM dinosaurs;` on its own, to see the
   exact spellings the table holds.
2. Compare that spelling, letter by letter, with the value after
   `WHERE diet =` in the box above.
3. Copy the spelling from that result into your query, rather than
   typing it again from memory.

**Think about:** why `'Carnivore'` and `'carnivore'` are different
pieces of text to SQLite, even though they read the same to you.

**Try this next:** change the condition to `WHERE length_meters > 10`
instead, and check whether that one brings back rows.
```

## ORDER BY: choosing an order

```sql exec
id: query-longest-first
SELECT name, length_meters, diet
FROM dinosaurs
WHERE length_meters > 5
ORDER BY length_meters DESC;
```

`ORDER BY` sorts the result by a column. `DESC` puts the largest value
first, and `ASC` puts the smallest value first. Leaving the word out
also gives you `ASC`. A query can combine `WHERE` and `ORDER BY`, in
that order, the way this one does.

## Why this happens

None of these statements changed the table. `SELECT` only reads.
Running the same one twice gives the same rows both times, unless
something else changes the table in between. That is worth knowing
before the next page, where some statements do change what a table
holds.

## Your turn

Bring your table back from the last page. Paste in the `CREATE TABLE`
and `INSERT` statements you wrote there, then run them again to rebuild
it. If this is your first time in this series, write a new `CREATE
TABLE` and some `INSERT` statements of your own instead.

```sql exec
id: query-your-table
-- Paste the CREATE TABLE and INSERT statements you wrote for your own
-- table on the last page, then run them here to bring the table back.
-- First time in this series? Write new CREATE TABLE and INSERT
-- statements of your own instead.
```

Try writing three queries against it in the box above:

- One that names only some of its columns.
- One with a `WHERE` that keeps only some rows.
- One with an `ORDER BY`.

Run each in turn and see what comes back. The code in this box is saved
automatically, like every cell on this site, so it is still here if you
come back to this exact page. Keep a copy of it — you will bring the
same table back again on the next page.

## What you have now

- **WHERE** keeps only the rows where a condition after the table's
  name is true.
- **ORDER BY** sorts a result by one of its columns, `ASC` (the
  default) for smallest first, `DESC` for largest first.
