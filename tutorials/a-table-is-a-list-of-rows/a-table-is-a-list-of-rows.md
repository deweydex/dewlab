---
title: "A Table Is a List of Rows"
year: "2026-2027"
version: 2026.09.23.1
covers:
  where-databases-already-show-up:
    covers: [DBM-LO1]
  three-instructions-one-script:
    covers: [DBM-LO2]
---

# A Table Is a List of Rows

A `table is a load of boxes that have stuff in them... honestly its as simple as that. Where things get complicated is when we want specific stuff to be in specific boxes according to rules or conventions. The boxes form a grid, and we tend to talk about not just one box in that grid, but whole lines: row if we are talking about boxes (or "cells") left to right (horizontal), and columns if we refer to to a bunch of cells up and down (vertical). Each of those rows we call a record, columns refer to a specific "attribute" which we put at the top of the column as a header. So we call that box of values a table, and a table stores many records in one place, and every record is shaped the
same way: with the same attributes. For example, a line in a shopping list is a record. It has a name and a
quantity, and of course we want the item name to likely be different from line to line. A database table works the same way. Each row is one record, and every row has the same columns.

## Where databases already show up

A database is already part of things you use, whether or not anyone ever
calls it that. The contacts list on a phone is one, one record per
person. A shop's till checks stock and prices against one as a sale
happens. A school keeps its students and the classes they take in one.
Anywhere a list has to be searched, sorted, or updated by more than one
person, a database is usually already running underneath it.

A college timetable is one of the clearer examples: rooms, teachers,
programmes and the sessions that tie them together, all changing as a
term goes on. Later in this module, a page builds exactly that, and asks
a question a flat list could not easily answer: has anyone been booked
into the same room twice, at the same time.

This box creates a table of dinosaurs, adds six rows to it, then shows
every row it holds. Click Run and see what appears.

```sql exec
id: create-dinosaurs-table
CREATE TABLE dinosaur_tbl (
    dinosaur_id INTEGER PRIMARY KEY,
    name TEXT,
    diet TEXT,
    length_meters REAL,
    period TEXT
);

INSERT INTO dinosaur_tbl (name, diet, length_meters, period) VALUES
    ('Tyrannosaurus Rex', 'Carnivore', 12.3, 'Late Cretaceous'),
    ('Triceratops', 'Herbivore', 9.0, 'Late Cretaceous'),
    ('Velociraptor', 'Carnivore', 2.0, 'Late Cretaceous'),
    ('Brachiosaurus', 'Herbivore', 25.0, 'Late Jurassic'),
    ('Stegosaurus', 'Herbivore', 9.0, 'Late Jurassic'),
    ('Allosaurus', 'Carnivore', 9.7, 'Late Jurassic');

SELECT * FROM dinosaur_tbl;
```

Six rows appear, one per dinosaur, each with the same five columns.
Reset can undo almost anything you do here — it empties the table, so
you can start again.

## Three instructions, one script

That box ran three separate instructions, called statements, each one
ending in a semicolon.

**CREATE TABLE** names the table and lists its columns. Each column has a
name and a type: `TEXT` for words, `REAL` for a number with a decimal
point, `INTEGER` for a whole number. `dinosaur_id INTEGER PRIMARY KEY`
marks `dinosaur_id` as the column that gives every row a unique number,
filled in for you.

**INSERT INTO** adds rows. Each line inside `VALUES` is one row. Its
values follow the same order as the column names listed after the
table's name.

**SELECT \* FROM dinosaur_tbl** asks for every column of every row in the
`dinosaur_tbl` table. The word after `FROM` is always a table's name.

## Names that say what they are

Why `dinosaur_tbl`, and not just `dinosaurs`? This course follows a
*naming convention*: a rule for choosing names that everyone on a
project agrees to use. Ours has two parts.

A table's name is one row's thing, in the singular, with `_tbl` on the
end. One row is one dinosaur, so the table is `dinosaur_tbl`. The
`_tbl` tells a reader that the name belongs to a table. A query mixes
table names, column names and values together, so that clue is useful.

The key column takes its table's name too: `dinosaur_id`, not a bare
`id`. Why? Soon we will have several tables, and each one has a key. If
every key were called `id`, which table would a given `id` belong to?
`dinosaur_id` says so in its own name. On a later page, a second table
holds a `dinosaur_id` column of its own, and a query joins the two
tables where `dinosaur_id` matches `dinosaur_id`. A diagram of the two
tables draws its line from `dinosaur_id` to `dinosaur_id`. The names
alone tell you what connects.

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
and see what happens. Reset can fix anything you break here.

Then let's build a table of your own, about something you know well:
books, a sports team, a music collection. Start with three columns
and four rows — you can always add more later. Try naming it the same
way: `book_tbl`, with a `book_id` key.

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
your `CREATE TABLE` and `INSERT` statements somewhere safe. Settings
also has ways to save a copy of the whole page, code included, if you
want one on another computer or to hand in.

## What you have now

- **Table** stores rows of data, all shaped the same way, under one
  name.
- **Row** holds one record in a table.
- **Column** holds one property that every row in a table has.
- **Statement** is one instruction to the database, such as `CREATE
  TABLE`, `INSERT`, or `SELECT`.
- **A naming convention** gives every table a singular name ending in
  `_tbl`, such as `dinosaur_tbl`, and a key named after it, such as
  `dinosaur_id`.
