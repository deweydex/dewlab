---
title: "Updating and deleting rows"
slug: changing-what-is-in-it
module: data
module_title: "Data"
series: first-database
version: 2026.09.05.1
---

# Updating and deleting rows

`INSERT` adds a row. Two more statements change the rows already there:
`UPDATE` changes values in existing rows, and `DELETE` removes rows
completely. Build the table again, then try both.

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

## UPDATE: changing a value

```sql cell=dinosaurs
UPDATE dinosaurs SET length_meters = 2.5 WHERE name = 'Velociraptor';

SELECT name, length_meters FROM dinosaurs WHERE name = 'Velociraptor';
```

`SET` names the column and its new value. `WHERE` picks which rows get
it, the same `WHERE` from the last page. Leave `WHERE` out, and every row
in the table changes: run the box again without it and see the whole
table's lengths become 2.5.

## DELETE: removing a row

Run the first box again, to rebuild the table with six fresh rows. Then
run this:

```sql cell=dinosaurs
DELETE FROM dinosaurs WHERE name = 'Stegosaurus';

SELECT name FROM dinosaurs;
```

`Stegosaurus` is gone from the list, and the row cannot be recovered by
running a `SELECT`. `DELETE` needs a `WHERE` for the same reason
`UPDATE` does: leave it out, and every row in the table is removed.

## Why this happens

`UPDATE` and `DELETE` both act on whichever rows their `WHERE` matches,
and neither asks you to confirm first. A `WHERE` that matches more rows
than you expected, or none at all, is usually a spelling difference. A
name typed differently than it was inserted, or a condition true for no
row, both look this way. Run a matching `SELECT` first, the way both
boxes above do, to see which rows a `WHERE` picks out before you change
or remove them.

## Your turn

Your own table is already here, carried over from the last page.

```sql cell=my-table persist
-- If you built a table on an earlier page, it is already loaded above.
-- If this is your first time here, write a CREATE TABLE and some
-- INSERT statements of your own, then run them.
```

Try adding two more rows to it with `INSERT`. Then write one `UPDATE`
that changes a value in a row you choose, and one `DELETE` that removes
a row you no longer want. Check each one with a `SELECT` before and
after, the way the boxes above do. If something goes wrong, Reset
brings everything back.

## What you have now

- **UPDATE** — changes a value in the rows a `WHERE` matches. Without a
  `WHERE`, every row changes.
- **DELETE** — removes the rows a `WHERE` matches. Without a `WHERE`,
  every row is removed.
