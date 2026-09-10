---
title: "A Table Is a List of Rows"
slug: a-table-is-a-list-of-rows
module: database-methods
module_title: "Database Methods"
year: "2026-2027"
series: first-database
version: 2026.09.10.1
---

# A Table Is a List of Rows

A table stores many records in one place, and every record is shaped the
same way. A line in a shopping list is a record. It has a name and a
quantity, even though the values differ from line to line. A database
table works the same way. Each row is one record, and every row has the
same columns.

This box creates a table of dinosaurs, adds six rows to it, then shows
every row it holds. Click Run and see what appears.

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

SELECT * FROM dinosaurs;
```

Six rows appear, one per dinosaur, each with the same five columns. There
is little you can do here that Reset cannot undo — it empties the table
so you can start again.

## Three instructions, one script

That box ran three separate instructions, called statements, each one
ending in a semicolon.

**CREATE TABLE** names the table and lists its columns. Each column has a
name and a type: `TEXT` for words, `REAL` for a number with a decimal
point, `INTEGER` for a whole number. `id INTEGER PRIMARY KEY` marks `id`
as the column that gives every row a unique number, filled in for you.

**INSERT INTO** adds rows. Each line inside `VALUES` is one row. Its
values follow the same order as the column names listed after the
table's name.

**SELECT \* FROM dinosaurs** asks for every column of every row in the
`dinosaurs` table. The word after `FROM` is always a table's name.

## Why this happens

A spreadsheet stores data in the same shape, one column per property and
one row per entry. The difference is how you change it. Anyone looking at
a spreadsheet can also type into any cell they see. A table's rows change
only through a statement that somebody runs on purpose, such as `INSERT`.
Several programs will read and write the same table at the same time
later in this course, and that rule is what keeps a table correct when
they do.

## Your turn

Try changing something in the box above: a different dinosaur name, a
seventh row, even a new column in the `CREATE TABLE` line. Run it again
and see what happens. Nothing here breaks anything that Reset cannot
fix.

Then let's build a table of your own, about something you know well:
books, a football squad, a music collection. Start with three columns
and four rows — you can always add more later.

```sql exec
id: create-your-table
-- Write your own CREATE TABLE and INSERT statements here, then run them.
```

Write your `CREATE TABLE` and `INSERT` statements in place of the
comment above, then run the box. This one is labelled "Your table"
instead of "SQL", to tell it apart from the dinosaur cells above.

The code you write here is saved automatically, the same as every cell
on this site — close this page and come back later, and it is still
here. Running it again rebuilds your table from scratch. You will bring
this same table back on each of the next few pages, so keep a copy of
your `CREATE TABLE` and `INSERT` statements somewhere of your own.
Settings also has ways to save a copy of the whole page, code included,
if you want one on another computer or to hand in.

## What you have now

- **Table** — rows of data, all shaped the same way, stored under one
  name.
- **Row** — one record in a table.
- **Column** — one property that every row in a table has.
- **Statement** — one instruction to the database, such as `CREATE
  TABLE`, `INSERT`, or `SELECT`.
