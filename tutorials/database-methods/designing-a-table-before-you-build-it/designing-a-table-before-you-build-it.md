---
title: "Designing a Table Before You Build It"
slug: designing-a-table-before-you-build-it
module: database-methods
module_title: "Database Methods"
year: "2026-2027"
series: several-tables
version: 2026.09.10.1
covers:
  what-goes-in-which-table:
    covers: [DBM-LO9]
  naming-a-column-and-its-type:
    covers: [DBM-LO2]
  one-row-can-point-at-many:
    covers: [DBM-LO9]
---

# Designing a Table Before You Build It

The dinosaurs table on the earlier pages was already designed before you saw
it: which columns it needed, and what kind of value belonged in each. A
database with more than one table needs that decision made on paper first. A
`CREATE TABLE` written before you know what you are storing tends to need
rewriting once you do.

## What goes in which table

Each table holds one kind of thing. A shop's products are one kind of thing;
its sales are another. Put them in the same table, and every sale repeats the
product's name and price. A price change then means editing every sale that
mentions it. Two tables joined by an id keep the price in one place.

A rough test: if a column's value would repeat across many rows, that value
probably belongs in its own table.

## Naming a column and its type

Every column has a name and a kind of value. `price` is a number.
`product_name` is text. Deciding this before writing SQL is what
`CREATE TABLE` actually asks for: a list of columns, and for each one, a name
and a type.

`INTEGER PRIMARY KEY` names the column that gives each row its own identity,
the way `dinosaurs.id` did earlier. Every table needs one.

## One row can point at many

A product can appear in many sales; a sale points at exactly one product.
That is *one-to-many*. The id lives on the `sales` side, in a column like
`product_id`, holding the product it belongs to. [A second table and a
join](tutorial:a-second-table-and-a-join) already showed the query side of
this, with `sightings.dinosaur_id`.

## Your turn

Let's pick a topic for a database with at least two related tables — a
library's books and its borrowers, a gym's classes and its members, a shop's
products and its sales, or a topic of your own. On paper, or in a text file
next to your notes, try answering three questions for each table:

- What is one row? (One book, one borrower, one sale.)
- What columns does that row need, and what kind of value goes in each?
- Which column, if any, points at a row in another table?

Do this before the next page opens a real dataset and asks the same three
questions of it. The database you design here is the one the rest of this
series builds, one page at a time.

## What you have now

- **Each table holds one kind of thing.** Repeating a value across many rows
  is the sign a table is doing two jobs.
- **Every column needs a name and a type.** Deciding both, before writing
  `CREATE TABLE`, is what `CREATE TABLE` actually asks for.
- **One-to-many** is a relationship where an id column, such as `product_id`,
  links one row in one table to many rows in another.
