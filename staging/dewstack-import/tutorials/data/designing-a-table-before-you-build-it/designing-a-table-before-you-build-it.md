---
title: "Designing a table before you build it"
slug: designing-a-table-before-you-build-it
module: data
module_title: "Data"
series: several-tables
version: 2026.09.05.1
---

# Designing a table before you build it

The dinosaurs table on the earlier pages was already designed before you
saw it: which columns it needed, and what kind of value belonged in
each. A database with more than one table needs that decision made on
paper first. A `CREATE TABLE` written before you know what you are
storing tends to need rewriting once you do.

## What goes in which table

One table per kind of thing. A shop's products are one kind of thing;
its sales are another. Put them in the same table, and every sale
repeats the product's name and price, and a price change means editing
every sale that mentions it. Two tables, joined by an id, means the
price lives in one place.

A rough test: if a column's value would repeat across many rows, that
value probably wants its own table.

## Naming a column and its type

Every column has a name and a kind of value. `price` is a number.
`product_name` is text. Deciding this before writing SQL is what
`CREATE TABLE` actually asks for: a list of columns, and for each one, a
name and a type.

`INTEGER PRIMARY KEY` names the column that gives each row its own
identity, the way `dinosaurs.id` did earlier. Every table wants one.

## One row can point at many

A product can appear in many sales; a sale points at exactly one
product. That is one-to-many. The id lives on the `sales` side, in a
column like `product_id`, holding the product it belongs to. [A second
table and a join](tutorial:a-second-table-and-a-join) already showed
the query side of this, with `sightings.dinosaur_id`.

## Your turn

Let's pick a topic for a database with at least two related tables — a
library's books and its borrowers, a gym's classes and its members, a
shop's products and its sales, or a topic of your own. On paper, or in
a text file next to your notes, try answering three questions for each
table:

- What is one row? (One book. One borrower. One sale.)
- What columns does that row need, and what kind of value goes in each?
- Which column, if any, points at a row in another table?

Do this before the next page opens a real dataset and asks the same
three questions of it. The database you design here is the one the rest
of this series builds, one page at a time.

## What you have now

- **One table per kind of thing** — repeating a value across many rows
  is the sign a table is doing two jobs.
- **Column, and its type** — every column needs a name and a kind of
  value, decided before `CREATE TABLE` is written.
- **One-to-many** — one row on one side can be pointed at by many rows
  on the other, through an id column on the "many" side.
