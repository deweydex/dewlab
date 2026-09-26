---
title: "Filtering and sorting rows: WHERE and ORDER BY"
year: "2026-2027"
version: 2026.09.26.1
covers:
  naming-columns:
    covers: [DBM-LO3]
  where-keeping-only-some-rows:
    covers: [DBM-LO5]
  order-by-choosing-an-order:
    touches: [DBM-LO5]
---

# Filtering and sorting rows: WHERE and ORDER BY

`SELECT *` shows every column of every row: the `*` stands for all the
columns. Most questions worth asking need only some of the rows, and only
some of their columns. Which dinosaurs ate meat? Which one was the
longest? This page builds the same dinosaur table again, then asks it
three questions.

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
```

Run that box first. It builds the table, and reports `6 rows affected.`:
six rows went in. It shows no table, because no statement in it asks to
see one.

## Naming columns

```sql exec
id: select-name-and-length
SELECT name, length_meters FROM dinosaur_tbl;
```

This asks for two columns instead of five. Name the columns you want in
place of `*`, with a comma between each one. They appear in the order you
name them: try `SELECT length_meters, name` and see.

## WHERE: keeping only some rows

The next box keeps only the dinosaurs whose diet is `'Carnivore'`. Look again at the six rows. How many rows do you think will appear, and which
ones? Write your guess in a comment on the first line, `-- my guess: …`,
and then run the box.

```sql exec
id: query-carnivores
SELECT name, length_meters FROM dinosaur_tbl WHERE diet = 'Carnivore';
```

Three rows appear: Tyrannosaurus Rex, Velociraptor and Allosaurus.

`WHERE` keeps a row only if the ***condition*** after it is true for
that row. A condition compares a column with a value. `diet =
'Carnivore'` is true for three rows and false for the other three, so
three rows are kept. Text in a condition goes in single quotes, like
`'Carnivore'`. A number needs no quotes.

The picture shows the whole query at once. `SELECT` picks columns,
`WHERE` picks rows, and the result is only the cells that are in both.

![The six-row dinosaur table. The name and length_meters columns are
highlighted and marked SELECT. The Tyrannosaurus Rex, Velociraptor and
Allosaurus rows are highlighted and marked WHERE keeps. Where a picked
column and a kept row cross, the cell has a third colour. Under the
table is the query, SELECT name, length_meters FROM dinosaur_tbl WHERE
diet = 'Carnivore', and an arrow down to the result it gives: two
columns and three rows, Tyrannosaurus Rex 12.3, Velociraptor 2.0 and
Allosaurus 9.7. These are the cells that are in a picked column and in a
kept row.](columns-and-rows.svg)

`=` is one of six ways a condition can compare:

- `=` equal to, and `<>` not equal to
- `<` less than, and `>` greater than
- `<=` less than or equal to, and `>=` greater than or equal to

Try changing the box to `WHERE length_meters > 10` and run it again.
Which dinosaurs are left? What changes if you write `>= 12.3` instead?

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

1. Run `SELECT DISTINCT diet FROM dinosaur_tbl;` on its own, to see the
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

The next box keeps the dinosaurs longer than 5 metres, then sorts them,
longest first. Two of them, Triceratops and Stegosaurus, are both 9.0
metres long. Which of those two do you think will come first? Write
your guess down before you run the box.

```sql exec
id: query-longest-first
SELECT name, length_meters, diet
FROM dinosaur_tbl
WHERE length_meters > 5
ORDER BY length_meters DESC;
```

Brachiosaurus comes first, at 25.0 metres. Velociraptor is not there at
all. At 2.0 metres, it is not longer than 5. And Triceratops comes
before Stegosaurus.

`ORDER BY` sorts the result by a column. `DESC` puts the largest value
first, and `ASC` puts the smallest value first. Leaving the word out
also gives you `ASC`.

A query can use both `WHERE` and `ORDER BY`, the way this one does.
`WHERE` comes first in the query, and it happens first, too. The
database keeps the rows the condition allows, and then sorts only the
rows it kept.

![Two tables side by side. On the left, under the heading WHERE
length_meters > 5, the six dinosaurs with their lengths, and
Velociraptor, 2.0, struck through: five rows are kept and one is
dropped. An arrow points to the right-hand table, under the heading
ORDER BY length_meters DESC, which holds those five in order, longest
first: Brachiosaurus 25.0, Tyrannosaurus Rex 12.3, Allosaurus 9.7,
Triceratops 9.0, Stegosaurus 9.0.](where-then-order.svg)

So why did Triceratops come before Stegosaurus? Nothing in the query
decides between two equal lengths, so the database may put them in
either order. Here it kept the order they were added in, but a
different database, or a larger table, may not.

## Why this happens

None of these statements changed the table. `SELECT` only reads.
Running the same one twice gives the same rows both times, unless
something else changes the table in between. That is worth knowing
before the next page, where some statements do change what a table
holds.

## Your turn

Can you make the `ORDER BY` box decide between Triceratops and
Stegosaurus, so that Stegosaurus always comes first? A hint, if you want
one: `ORDER BY` can take more than one column, with a comma between them.
The second column only matters when the first one is equal.

Then bring your table back from the last page. Paste in the statements
you wrote there, starting with `DROP TABLE IF EXISTS`, and run them
again to rebuild it. If this is your first time in this series, write a
new `CREATE TABLE` and some `INSERT` statements of your own instead.

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

Only the last statement in a box shows its result, so run each query in
turn, with the one you want to see at the bottom. Before each run, can
you say how many rows it will show?

What you type in this box is saved on this device, like every box on
this site. Keep a copy of your statements too. You will bring the same
table back again on the next page.

## What you have now

- **`*`** stands for every column of a table.
- **Condition** compares a column with a value, such as `diet =
  'Carnivore'`, and is true or false for each row.
- **WHERE** keeps only the rows where a condition after the table's
  name is true.
- **ORDER BY** sorts a result by one of its columns, `ASC` (the
  default) for smallest first, `DESC` for largest first.

## Where to read more

Spanning Tree (2024). *Understanding B-Trees: The Data Structure Behind
Modern Databases.* <https://www.youtube.com/watch?v=K1a2Bk8NrYQ>. A
database can find the rows a WHERE asks for without reading every row,
because it keeps them in order in a B-tree. Brian Yu shows how that works.
About thirteen minutes.
