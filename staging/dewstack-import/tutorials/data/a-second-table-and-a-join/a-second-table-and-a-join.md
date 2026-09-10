---
title: "A second table and a join"
slug: a-second-table-and-a-join
module: data
module_title: "Data"
series: first-database
version: 2026.09.05.1
---

# A second table and a join

Real data rarely fits in one table. A dinosaur is one record; where its
fossils were found is a different kind of record, and a dinosaur can have
several. Splitting the two into separate tables avoids repeating a
dinosaur's name, diet and length once per fossil site. A `JOIN` is how a
query brings the two tables back together.

Let's build the dinosaurs table again, then a second table for fossil sites.

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

```sql cell=dinosaurs
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

`sightings.dinosaur_id` holds a value that also appears in `dinosaurs.id`.
That shared value is what connects one table's row to the other's.

## JOIN: querying across both tables

```sql cell=dinosaurs
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
way. `JOIN` is the cost of that. The two tables are re-combined at query
time, on the column that connects them, rather than kept together all
along.

## Your turn

Your own table is already here, carried over from the earlier pages.

```sql cell=my-table persist
-- If you built a table on an earlier page, it is already loaded above.
-- If this is your first time here, write a CREATE TABLE and some
-- INSERT statements of your own, then run them.
```

In the same box, below what is already there, try adding a `CREATE
TABLE` for a second table that relates to it. If your table lists films,
a second table might hold one row per actor, with a column naming which
film's `id` they belong to. If your table lists books, it might hold one
row per author. Give the second table's linking column the same kind of
values as the first table's `id` column. Insert a few rows, then try
writing a `JOIN` that brings a row from each table together. Run it
here, in this one box. This is the last page of the series, but the
table stays saved in your browser. Download is still there if you want a
copy of your own.

## What you have now

- **Foreign key** — a column in one table naming a row in another table,
  the way `sightings.dinosaur_id` names a row in `dinosaurs`.
- **JOIN** — combines rows from two tables in one query, matched on a
  column they share.
