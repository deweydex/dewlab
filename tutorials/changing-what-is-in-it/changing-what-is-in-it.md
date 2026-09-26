---
title: "Updating and deleting rows: UPDATE and DELETE"
year: "2026-2027"
version: 2026.09.26.1
covers:
  update-changing-a-value:
    covers: [DBM-LO4]
  delete-removing-a-row:
    covers: [DBM-LO4]
---

# Updating and deleting rows: UPDATE and DELETE

`INSERT` adds a row. Two more statements change the rows already there:
`UPDATE` changes values in rows, and `DELETE` removes rows completely.
Both are useful, and both can change far more than you meant them to.
So this page makes that mistake on purpose, twice, to see what it looks
like.

First, build the table again. The box reports `6 rows affected.` when
the six rows are in.

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

## UPDATE: changing a value

```sql exec
id: update-velociraptor-length
UPDATE dinosaur_tbl SET length_meters = 2.5 WHERE name = 'Velociraptor';

SELECT name, length_meters FROM dinosaur_tbl WHERE name = 'Velociraptor';
```

Velociraptor's length is now 2.5 metres. `SET` names the column and its
new value. `WHERE` picks which rows get the new value, the same way it
picked rows on the last page.

Now the mistake. Delete `WHERE name = 'Velociraptor'` from both lines
of the box, and keep the semicolons. The first line now has no
condition at all. Before you run it, how many rows do you think it will
change? Write your guess in a comment first, and then run it.

Every length in the table is now 2.5. Leave `WHERE` out, and `UPDATE`
changes every row in the table. The database does not ask whether you
are sure.

![Two copies of the same six-row table, each showing name and
length_meters after an UPDATE. On the left, with WHERE name =
'Velociraptor', only one cell has changed: Velociraptor, 2.0 to 2.5.
One row changed. On the right, without WHERE, every length has
changed to 2.5: Tyrannosaurus Rex 12.3 to 2.5, Triceratops 9.0 to 2.5,
and so on down the column. Six rows
changed.](update-with-and-without-where.svg)

To get the real lengths back, run the first box on this page again. Its
`DROP TABLE` line gives you a fresh table each time. Clear (↻) returns
the `UPDATE` box to its first version.

## DELETE: removing a row

Run the first box again, to rebuild the table with six fresh rows. Then
run this:

```sql exec
id: delete-stegosaurus
DELETE FROM dinosaur_tbl WHERE name = 'Stegosaurus';

SELECT name FROM dinosaur_tbl;
```

Stegosaurus is gone from the list, and running `SELECT` again will not
return it. `DELETE` needs a `WHERE` for the same reason `UPDATE` does.
Leave it out, and every row in the table is removed. The table itself
stays, with its columns and no rows. Removing the table itself is a
different statement, `DROP TABLE`, which the first box on this page
uses.

![Two copies of the same six-row table, each showing dinosaur_id and
name after a DELETE. On the left, DELETE with WHERE name =
'Stegosaurus': the Stegosaurus row, id 5, is struck through, and five
rows are left, with ids 1, 2, 3, 4 and 6. On the right, DELETE FROM
dinosaur_tbl with no WHERE: all six rows are struck through. No rows
are left, but the table and its columns
stay.](delete-with-and-without-where.svg)

Look at the `dinosaur_id` column on the left. After the delete, the ids
are 1, 2, 3, 4 and 6. Nobody renumbers the rows. Allosaurus keeps its 6,
because a primary key stays with its row. To see this in the box, change
its last line to `SELECT * FROM dinosaur_tbl;`.

## Why this happens

`UPDATE` and `DELETE` both act on whichever rows their `WHERE` matches,
and neither asks you to confirm first. A `WHERE` that matches more rows
than you expected, or none at all, usually comes from a small
difference: a name typed differently from the way it was inserted, or a
capital letter where the table has none.

So here is a habit worth having. Before an `UPDATE` or a `DELETE`, run
a `SELECT` with the same `WHERE`. It shows exactly which rows the
`WHERE` picks, before you change or remove any of them.

## Your turn

Bring your table back from the last page. Paste in the statements you
wrote there, starting with `DROP TABLE IF EXISTS`, then run them again
to rebuild it. If this is your first time in this series, write new
`CREATE TABLE` and `INSERT` statements of your own instead.

```sql exec
id: change-your-table
-- Paste the CREATE TABLE and INSERT statements you wrote for your own
-- table on an earlier page, then run them here to bring it back.
-- First time in this series? Write new CREATE TABLE and INSERT
-- statements of your own instead.
```

Then let's change it. One way to do it:

1. Add two more rows with `INSERT`.
2. Choose one row to change. Write a `SELECT` with a `WHERE` that finds
   only that row, and run the box to check it finds just the one.
3. Write an `UPDATE` with the same `WHERE`, and a `SELECT` after it to
   see the change.
4. Do the same with a `DELETE`, for a row you no longer want.

If something goes wrong, run the box again. Its `DROP TABLE` line
rebuilds your table from the start every time.

For more of a challenge: can you write one `UPDATE` that changes several
rows at once, on purpose? On the dinosaur table, that could be every
herbivore's `diet` changed to `'Plant eater'`. How many rows do you
expect it to change? When an `UPDATE` is the last statement in a box,
the box reports the number of rows it changed.

## What you have now

- **UPDATE** changes a value in the rows a `WHERE` matches. Without a
  `WHERE`, every row changes.
- **DELETE** removes the rows a `WHERE` matches. Without a `WHERE`,
  every row is removed, and the empty table stays.
- **DROP TABLE** removes a whole table, its columns as well as its rows.
