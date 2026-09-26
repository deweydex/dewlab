---
title: "Tables in SQL: CREATE TABLE, INSERT and SELECT"
year: "2026-2027"
version: 2026.09.26.1
covers:
  where-databases-already-show-up:
    covers: [DBM-LO1]
  three-instructions-one-script:
    covers: [DBM-LO2]
---

# Tables in SQL: CREATE TABLE, INSERT and SELECT

![A shopping list drawn as a grid, with three columns headed item,
quantity and aisle, and four rows: Milk 2 1, Bread 1 3, Eggs 12 1, and
Apples 6 5. Labels name the parts. The header is the name at the top of
each column. The Eggs row is one row, or record: one thing on the list,
left to right. The quantity column is one column, or attribute: one kind
of value, top to bottom, the same for every row. The box holding 5, in
the Apples row, is one cell: one value.](parts-of-a-table.svg)

Here is a shopping list, drawn as a grid of small boxes. Look at it for a
moment before you continue. What does every line of the list have? And
what changes from one line to the next?

Every line has an item, a quantity and an aisle. The values in them
change: milk on one line, bread on the next.

A grid like this is a ***table***. A table is only boxes with values in
them, arranged in rows and columns. Things only get
interesting when we want particular values in particular boxes, by a rule
that everyone follows. The parts have names:

- Each small box is a ***cell***. It holds one value, such as `12` or
  `Milk`.
- A line of cells from left to right is a ***row***. One row describes
  one thing: one item on the list. A database calls a row a
  ***record***.
- A line of cells from top to bottom is a ***column***. Every value in a
  column is the same kind of thing: all quantities, or all aisles. A
  database calls a column an ***attribute***.
- The name at the top of a column is its ***header***.

One rule makes a grid into a table. Every row has the same columns. A
new line on the shopping list gets an item, a quantity
and an aisle, like every line before it. A database table follows the
same rule, and this page builds one.

Remember three things as you go:

- Every box of SQL on this page is yours to change. Change something, run
  it again, and see what happens.
- An error message tells you something about one line. It says nothing
  about you.
- A new word is in bold the first time it appears. The Reference panel
  has all of them.

## Where databases already show up

A ***database*** is a collection of tables, kept by a program that
stores them safely and answers questions about them. You already use
databases, even if nobody calls them that. The contacts list on a phone
is one, with one record per person. A shop's till checks stock and
prices against one during every sale. A school keeps its students, and
the classes they take, in one. Anywhere a list has to be searched,
sorted, or changed by more than one person, a database is usually
running underneath it.

A college timetable is one of the clearest examples: rooms, teachers,
programmes, and the sessions that connect them, all changing as a term
goes on. Later in this module, a page builds exactly that. Then it asks
a question a flat list could not easily answer: has anyone been booked
into the same room twice, at the same time?

Now let's build a real table. The box below makes a table of dinosaurs,
puts six rows into it, and then shows every row it holds.

Before you run it, look at the lines under `VALUES`. Each one gives a
dinosaur a name, a diet, a length and a period. None of them gives it a
`dinosaur_id`. What do you think Triceratops's `dinosaur_id` will be,
once the table is built? Write your guess down, or type it on the first
line of the box as `-- my guess: …`. A line that starts with two dashes
is a ***comment***. SQL does not run it.

Then click Run.

```sql exec
id: create-dinosaurs-table
DROP TABLE IF EXISTS dinosaur_tbl;

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
Triceratops has `dinosaur_id` 2. Nobody typed that 2. The database gave
each row the next number as it arrived: 1 for Tyrannosaurus Rex, 2 for
Triceratops, and so on down to 6. Did that match your guess?

## Three instructions, one script

That box ran four instructions, one after another. Each one is called a
***statement***, and each one ends with a semicolon, `;`. Three of them
do the main work, and the picture shows what each one does.

![Three steps, one under the other. Step 1: CREATE TABLE makes the
table, its name and its columns, with no rows yet. It is drawn as an empty
table with the headers dinosaur_id, name, diet, length_meters and period.
Step 2: INSERT INTO adds six rows, and the database gives each row its
dinosaur_id. The same table now has six rows, from 1, Tyrannosaurus Rex,
to 6, Allosaurus, with the dinosaur_id column highlighted. Step 3:
SELECT * FROM dinosaur_tbl reads every row back, and shows them under the
box. Reading changes nothing.](three-statements.svg)

Here is what each part of the box does:

- **CREATE TABLE** names the table and lists its columns. Each column has
  a name and a ***data type***: the kind of value it holds. `TEXT` is for
  words, `REAL` is for a number with a decimal point, and `INTEGER` is
  for a whole number.
- `dinosaur_id INTEGER PRIMARY KEY` makes `dinosaur_id` the table's
  ***primary key***. A primary key gives every row its own value,
  different from every other row's. When an `INSERT` leaves it out, the
  database gives the row the next number, which is what happened to
  Triceratops.
- **INSERT INTO** adds rows. Each line inside `VALUES` is one row. Its
  values go in the same order as the column names in the brackets after
  the table's name: first `name`, then `diet`, then `length_meters`, then
  `period`.
- **SELECT \* FROM dinosaur_tbl** asks for every column of every row in
  `dinosaur_tbl`. The word after `FROM` is always a table's name. A
  statement that asks a table for rows like this is called a
  ***query***.
- **DROP TABLE IF EXISTS dinosaur_tbl**, at the top, deletes any
  dinosaur table left from an earlier run. This line lets you run the
  box as often as you like. Each run starts from nothing.

Let's read one row by hand. The fourth line under `VALUES` is
`('Brachiosaurus', 'Herbivore', 25.0, 'Late Jurassic')`. Match it against
the column names, in order: `name` is Brachiosaurus, `diet` is
Herbivore, `length_meters` is 25.0 and `period` is Late Jurassic. It is
the fourth row to arrive, so its `dinosaur_id` is 4. Find it in the
result under the box.

Here is an experiment that is meant to go wrong. Put `--` at the start of
the `DROP TABLE` line, so that SQL skips it, and run the box again. This
time it stops with an error: `table dinosaur_tbl already exists`. The
table from your last run is still there, and a database will not make a
second table with a name it already has. Delete the `--` again, and the
box runs as often as you like.

## Names that say what they are

Why `dinosaur_tbl`, and not just `dinosaurs`? This course follows a
***naming convention***: a rule for choosing names that everyone on a
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
tables where `dinosaur_id` matches `dinosaur_id`. A diagram of those two
tables draws its line from `dinosaur_id` to `dinosaur_id`. The names
alone tell you what connects.

## Why this happens

A spreadsheet stores data in the same shape as a table: one column per
attribute, one row per record. The difference is how the data changes.
Anyone looking at a spreadsheet can type into any cell they see. A
table's rows change only through a statement that somebody runs on
purpose, such as `INSERT`. Later in this course, several programs will
read and change the same table at the same time. That rule keeps the
table correct when they do.

## Your turn

Try changing something in the dinosaur box: a different name, a seventh
row, or a new column in `CREATE TABLE`. Run it again and see what
happens. If you add a column, what else in the box has to change before
it runs? Clear (↻) returns the box to its first version, if you want
it.

Then let's build a table of your own, about something you know well:
books, a sports team, a music collection. One way to do it:

1. Choose a name that follows the convention, such as `book_tbl`, with a
   `book_id` key.
2. Start with `DROP TABLE IF EXISTS book_tbl;`, so the box can run more
   than once.
3. Write a `CREATE TABLE` with the key and three more columns. Choose a
   data type for each one.
4. Write an `INSERT INTO` with four rows.
5. End with `SELECT * FROM book_tbl;`, and run the box.

```sql exec
id: create-your-table
-- Write your own CREATE TABLE and INSERT statements here, then run them.
```

This box is labelled "Your table" instead of "SQL", to tell it apart from
the dinosaur box. What you type here is saved on this device, like every
box on this site: close the page, open it again later, and it is still
here. You will bring this same table back on each of the next few pages,
so keep a copy of your statements somewhere safe as well. Settings can
also save a copy of the whole page, code included, to use on another
computer or to hand in.

## What you have now

- **Table** stores rows of data, all shaped the same way, under one
  name.
- **Row**, or **record**, holds one thing in a table.
- **Column**, or **attribute**, holds one kind of value that every row
  in a table has.
- **Cell** holds one value: where one row and one column cross.
- **Statement** is one instruction to the database, such as `CREATE
  TABLE`, `INSERT`, or `SELECT`.
- **Query** is a statement that asks a table for rows, such as
  `SELECT`.
- **Primary key** gives every row its own value, such as
  `dinosaur_id`.
- **A naming convention** gives every table a singular name ending in
  `_tbl`, such as `dinosaur_tbl`, and a key named after it, such as
  `dinosaur_id`.
