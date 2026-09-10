---
title: "A table is a list of rows"
slug: a-table-is-a-list-of-rows
module: data
module_title: "Data"
series: first-database
version: 2026.09.05.1
---

# A table is a list of rows

A table stores many records in one place, and every record is shaped the
same way. A line in a shopping list is a record. It has a name and a
quantity, even though the values differ from line to line. A database
table works the same way. Each row is one record, and every row has the
same columns.

This box creates a table of dinosaurs, adds six rows to it, then shows
every row it holds. Click Run and see what appears.

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

SELECT * FROM dinosaurs;
```

Six rows appear, one per dinosaur, each with the same five columns.
Nothing you do here can break anything; Reset empties the table so you
can start again.

## Three instructions, one script

That box ran three separate instructions, called statements, each one
ending in a semicolon.

**CREATE TABLE** names the table and lists its columns. Each column has a
name and a type: `TEXT` for words, `REAL` for a number with a decimal
point, `INTEGER` for a whole number. `id INTEGER PRIMARY KEY` marks `id`
as the column that gives every row a unique number, filled in for you.

**INSERT INTO** adds rows. Each line inside `VALUES` is one row, and its
values are in the same order as the columns named after the table.

**SELECT \* FROM dinosaurs** asks for every column of every row in the
`dinosaurs` table. The word after `FROM` is always a table's name.

## Why this happens

A spreadsheet stores data in the same shape, one column per property and
one row per entry. The difference is how you change it. Anyone looking at
a spreadsheet can also type into any cell they see. A table's rows only
change through a statement, run on purpose, such as `INSERT`. Later in
this course, several programs read and write the same table at once; that
rule is what keeps it correct while they do.

## Your turn

Try changing something in the box above — a different dinosaur name, a
seventh row, even a new column in the `CREATE TABLE` line. Run it again
and see what happens. Nothing here breaks anything that Reset cannot
fix.

Then let's build a table of your own, about something you know well:
books, a football squad, a music collection. Start with three columns
and four rows — you can always add more later.

```sql cell=my-table persist
-- Write your own CREATE TABLE and INSERT statements here, then run them.
```

Write your `CREATE TABLE` and `INSERT` statements in place of the comment
above, then run the box. This one is labelled "Your table", not "SQL". It
saves what you run here in this browser, so your table is already there
when you open the next page. Download still works if you want a copy of
your own, on a different computer or to hand in.

## What you have now

- **Table** — rows of data, all shaped the same way, stored under one
  name.
- **Row** — one record in a table.
- **Column** — one property that every row in a table has.
- **Statement** — one instruction to the database, such as `CREATE
  TABLE`, `INSERT`, or `SELECT`.
