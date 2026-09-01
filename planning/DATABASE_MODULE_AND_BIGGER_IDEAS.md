# Notes toward a database module

`tutorials/database-methods/` is an empty folder. Nothing here is built or
agreed. These are the findings worth keeping from a longer argument, each of
which holds whether or not a database module is ever built the way this
document imagines.

---

## The distinction the module would rest on

A notebook models values. You run a cell, something comes back, and you look
at it. The whole interface is built around that loop.

A database is a different kind of thing. It is state that outlives any cell
and that no cell fully shows you. A DataFrame of twenty rows is a photograph
of one corner of it, taken at a moment, and a notebook then treats the
photograph as though it were the thing.

This matters more than it sounds, because a notebook already has one source
of hidden state. Cells run in the order you press Run rather than from the
top, so a namespace can hold names whose origin is invisible. A database file
adds a second source, and a worse one, because it survives the restart that
clears the first. A student restarts Python and the `.db` on disk still
carries whatever a since-deleted cell did to it three sessions ago.

---

## Three findings from reading the repository

**The maths module has already laid the groundwork.**
`planning/curriculum/topics.yaml` names the database application of five MIT
topics: joins as set intersection at 2.2, logic rewriting as `WHERE` at 2.5,
schema design at 5.9, collections at 6.3, and index cost at 6.8. A database
module's `needs:` edges can therefore point at topics that already exist, and
the level bands will band its terms correctly with no extra work.

**`run_query` commits every query, which forecloses transactions.** Its
docstring is explicit that every query commits, and calls that the friendlier
default. That is right for a data-analysis tutorial and wrong twice over for a
database module, where transactions are core content and a student
experimenting with `DELETE` has no way back.

**No database learning outcomes exist yet.** This is the better case rather
than the worse one, because the tooling can be designed against the teaching
instead of retrofitted to it. It also means any argument about the order this
work should happen in is provisional until those outcomes are written.

---

## What SQLite offers, checked rather than assumed

Savepoints recovered a table after every row had been deleted.
`set_authorizer` classifies a statement as reading or writing before it runs.
`EXPLAIN QUERY PLAN` distinguishes a scan from a search, which is MIT-6.8's
lesson in machine-readable form. `backup()` and `iterdump()` give
deterministic reseeding.

Those were run on CPython 3.11 in an authoring sandbox, and Pyodide runs 3.13.
Each needs confirming there before anything is built on it.
