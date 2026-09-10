---
title: "A Second Table and a Join"
slug: a-second-table-and-a-join
module: database-methods
module_title: "Database Methods"
year: "2026-2027"
series: first-database
version: 2026.09.10.1
---

# A Second Table and a Join

Real data rarely fits in one table. A dinosaur is one record. Where its
fossils were found is a different kind of record, and one dinosaur can
have several fossil sites. Splitting the two into separate tables avoids
repeating a dinosaur's name, diet and length once per fossil site. A
`JOIN` is how a query brings the two tables back together.

Let's build the dinosaurs table again, then a second table for fossil
sites.

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

```sql exec
id: create-sightings-table
CREATE TABLE sightings (
    id INTEGER PRIMARY KEY,
    dinosaur_id INTEGER,
    location TEXT,
    year INTEGER
);

INSERT INTO sightings (dinosaur_id, location, year) VALUES
    (1, 'Montana, USA', 1902),
    (1, 'Saskatchewan, Canada', 1981),
    (2, 'Wyoming, USA', 1888),
    (3, 'Mongolia', 1971),
    (5, 'Colorado, USA', 1877);
```

`sightings.dinosaur_id` holds a value that also appears in
`dinosaurs.id`. That shared value is what connects one table's row to
the other's.

## JOIN: querying across both tables

```sql exec
id: join-dinosaurs-and-sightings
SELECT dinosaurs.name, sightings.location, sightings.year
FROM sightings
JOIN dinosaurs ON sightings.dinosaur_id = dinosaurs.id
ORDER BY sightings.year;
```

`JOIN dinosaurs ON sightings.dinosaur_id = dinosaurs.id` tells the query
which column in each table holds the shared value. For every row in
`sightings`, it finds the `dinosaurs` row whose `id` matches, and the
result carries columns from both. `table.column` names a column when two
tables in the same query might otherwise share a name.

## Why this happens

Storing a dinosaur's name on every one of its sighting rows would work.
A misspelling in one row would then disagree with the others, and
nothing would flag it. Storing the name once, in `dinosaurs`, and
referring to it by `id` everywhere else means it can only be spelled one
way. `JOIN` is the cost of that — the two tables are re-combined at
query time, on the column that connects them, rather than kept together
all along.

## Your turn

Bring your table back from the earlier pages. Paste in the `CREATE
TABLE` and `INSERT` statements you have written so far, then run them
again to rebuild it. If this is your first time in this series, write a
new `CREATE TABLE` and some `INSERT` statements of your own instead.

```sql exec
id: join-your-tables
-- Paste the CREATE TABLE and INSERT statements you have written so far
-- for your own table, then run them here to bring it back.
-- First time in this series? Write a new CREATE TABLE and some INSERT
-- statements of your own instead.
```

In the same box, below what is already there, try adding a `CREATE
TABLE` for a second table that relates to it. If your table lists films,
a second table might hold one row per actor, with a column naming which
film's `id` they belong to. If your table lists books, it might hold one
row per author. Give the second table's linking column the same kind of
values as the first table's `id` column. Insert a few rows, then try
writing a `JOIN` that brings a row from each table together. Run it
here, in this one box.

This is the last page of the series. The code in this box is saved
automatically, like every cell on this site, so you can always come back
and run it again. If you want a copy of your own, to keep or to hand in,
Settings has a few ways to save the whole page, code included.

## What you have now

- **Foreign key** — a column in one table naming a row in another table,
  the way `sightings.dinosaur_id` names a row in `dinosaurs`.
- **JOIN** — combines rows from two tables in one query, matched on a
  column they share.
