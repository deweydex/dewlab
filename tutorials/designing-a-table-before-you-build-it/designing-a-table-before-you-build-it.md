---
title: "Designing tables: columns, types and one-to-many links"
year: "2026-2027"
version: 2026.09.10.1
covers:
  what-goes-in-which-table:
    covers: [DBM-LO9]
  naming-a-column-and-its-type:
    covers: [DBM-LO2]
  one-row-can-point-at-many:
    covers: [DBM-LO9]
---

# Designing tables: columns, types and one-to-many links

`dinosaur_tbl`, on the earlier pages, was already designed before you saw
it: which columns it needed, and what kind of value belonged in each. A
database with more than one table needs that decision made on paper first. A
`CREATE TABLE` written before you know what you are storing tends to need
rewriting once you do.

## What goes in which table

Each table holds one kind of thing. A shop's products are one kind of
thing. Its sales are another. Put them in the same table, and every sale
repeats the
product's name and price. A price change then means editing every sale that
mentions it. Two tables joined by a key keep the price in one place.

Here is a rough test. If a column's value would repeat across many rows,
that value probably belongs in its own table.

## Naming a column and its type

Every column has a name and a kind of value. `price` is a number.
`product_name` is text. `CREATE TABLE` asks you to decide this before
you write it. It needs a list of columns, and for each one, a name and a
type.

`INTEGER PRIMARY KEY` names the column that gives each row its own identity,
the way `dinosaur_tbl.dinosaur_id` did earlier. Every table needs one, and
we name it after its table: `product_id` in `product_tbl`, `sale_id` in
`sale_tbl`.

## One row can point at many

A product can appear in many sales. A sale points at exactly one
product. This is called *one-to-many*. The link lives on the `sale_tbl`
side, in a
`product_id` column holding the product it belongs to. [A second table and
a join](tutorial:a-second-table-and-a-join) already showed the query side
of this, with `sighting_tbl.dinosaur_id`.

Why is that column called `product_id`, the same as the key in
`product_tbl`? A foreign key takes the name of the key it points at, so
anyone reading `sale_tbl` can see where it leads. It also sits directly
under `sale_id`, before `sold_on` and `quantity`. Put every foreign key
there, and every table in your design has the same shape: its own key
first, then its links, then everything else.

![One product_tbl row is reached by many sale_tbl rows. The product_id
column in product_tbl carries PK for primary key; the product_id column in
sale_tbl, directly under sale_id, carries FK for foreign key. The line runs
from one product_id to the other and ends in three prongs on the sale_tbl
side, meaning many.](products-sales-erd.svg)

That picture is an *entity relationship diagram*. Each box is a table, with
its columns listed under its name. `PK` marks the column that gives a row
its own identity, and `FK` marks a column holding a row's key from another
table. The line joins those two columns, `product_id` to `product_id`, and
its ends say how many: a single bar for one, and three prongs, called a
crow's foot, for many. So one product has many sales.

## Your turn

Let's pick a topic for a database with at least two related tables — a
library's books and its borrowers, a gym's classes and its members, a shop's
products and its sales, or a topic of your own. On paper, or in a text file
next to your notes, try answering three questions for each table:

- What is one row? (One book, one borrower, one sale.)
- What columns does that row need, and what kind of value goes in each?
- Which column, if any, points at a row in another table? Give it the
  same name as the key it points at, and list it straight after the
  table's own key.

Do this before the next page opens a real dataset and asks the same three
questions of it. The database you design here is the one the rest of this
series builds, one page at a time.

## What you have now

- **Each table holds one kind of thing.** A value that repeats across
  many rows is a sign that a table is doing two jobs.
- **Every column needs a name and a type.** `CREATE TABLE` asks you to
  decide both before you write it.
- **One-to-many** is a relationship where a key column, such as `product_id`,
  links one row in one table to many rows in another.
- **A foreign key keeps the name of the key it points at**, and sits
  directly under its own table's key.

## Where to read more

Stand-up Maths (2022). *How Roman numerals broke the official dog
database.* <https://www.youtube.com/watch?v=jMxoGqsmk5Y>. A kennel club
gives dogs that share a name a Roman numeral, and found that it could only
count so high. Matt Parker looks at what went wrong, and at better ways to
number things. About fifteen minutes.
