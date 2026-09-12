---
title: "Updating and Deleting Rows"
slug: changing-what-is-in-it
module: database-methods
module_title: "Database Methods"
year: "2026-2027"
series: first-database
version: 2026.09.10.1
covers:
  update-changing-a-value:
    covers: [DBM-LO4]
  delete-removing-a-row:
    covers: [DBM-LO4]
---

# Updating and Deleting Rows

`INSERT` adds a row. Two more statements change the rows already there:
`UPDATE` changes values in existing rows, and `DELETE` removes rows
completely. Build the table again, then try both.

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

## UPDATE: changing a value

```sql exec
id: update-velociraptor-length
UPDATE dinosaurs SET length_meters = 2.5 WHERE name = 'Velociraptor';

SELECT name, length_meters FROM dinosaurs WHERE name = 'Velociraptor';
```

`SET` names the column and its new value. `WHERE` picks which rows
receive the new value. It works the same way it did on the last page.
Leave `WHERE` out, and every row in the table changes. Try running the
box again without it, and watch the whole table's lengths become 2.5.

## DELETE: removing a row

Run the first box again, to rebuild the table with six fresh rows. Then
run this:

```sql exec
id: delete-stegosaurus
DELETE FROM dinosaurs WHERE name = 'Stegosaurus';

SELECT name FROM dinosaurs;
```

`Stegosaurus` is gone from the list. Running `SELECT` again will not
bring the row back. `DELETE` needs a `WHERE` for the same reason
`UPDATE` does: leave it out, and every row in the table is removed.

## Why this happens

`UPDATE` and `DELETE` both act on whichever rows their `WHERE` matches,
and neither asks you to confirm first. A `WHERE` that matches more rows
than you expected — or none at all — is usually caused by a small
difference in spelling. Typing a name differently than it was inserted,
or writing a condition that matches no row, produces the same result.
Run a matching `SELECT` first, the way both boxes above do. It shows you
which rows a `WHERE` picks out, before you change or remove them.

## Your turn

Bring your table back from the last page. Paste in the `CREATE TABLE`
and `INSERT` statements you wrote there, then run them again to rebuild
it. If this is your first time in this series, write new `CREATE TABLE`
and `INSERT` statements of your own instead.

```sql exec
id: change-your-table
-- Paste the CREATE TABLE and INSERT statements you wrote for your own
-- table on an earlier page, then run them here to bring it back.
-- First time in this series? Write new CREATE TABLE and INSERT
-- statements of your own instead.
```

Try adding two more rows to it with `INSERT`. Then write one `UPDATE`
that changes a value in a row you choose, and one `DELETE` that removes
a row you no longer want. Check each one with a `SELECT` before and
after, the way the boxes above do. If something goes wrong, Reset
brings everything back.

## What you have now

- **UPDATE** changes a value in the rows a `WHERE` matches. Without a
  `WHERE`, every row changes.
- **DELETE** removes the rows a `WHERE` matches. Without a `WHERE`,
  every row is removed.
