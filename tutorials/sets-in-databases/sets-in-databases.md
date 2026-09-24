---
title: "Sets in databases"
context_for:
  - collections-without-repeats
  - circles-that-overlap
year: "2026-2027"
version: 2026.09.24.1
---

# Sets in databases

A music app keeps every playlist that anybody makes. When it tells you
that you and a friend share two songs, it asked its database, not
Python. How do you ask a database for an intersection? With
the same idea you already have, written in a different language.

On this page we:

- keep the two playlists from
  [Collections without repeats](tutorial:collections-without-repeats)
  as two tables
- ask for their union, intersection and difference in SQL
- see why a table can hold a repeat that a set cannot
- make every pair of rows from two tables, and then keep only the pairs
  that match, which is what a `JOIN` does

> **The space we're in.** A small database, which lives inside this page
> and is reached with SQL. Python is still here, but most cells on this
> page are SQL. One thing usually goes unsaid: a table is close to a set
> of rows, but not the same. A table can hold the same values twice, and
> SQL has words for when that matters.

## Two playlists, two tables

A *database* is a store of data, kept in tables. A *table* is a grid of
named columns, and each *row* is one record in it: here, one song on one
playlist. *SQL* is the language most databases use for questions, and a
question written in it is a *query*.

The cell below builds two tables, `my_song_tbl` and `your_song_tbl`,
with the same songs as the two playlists on
[Collections without repeats](tutorial:collections-without-repeats#two-playlists).
You do not need to follow every line. `DROP TABLE IF EXISTS` removes an
old copy of the table, so the cell can be run again. `CREATE TABLE`
names the columns, and `INSERT` puts in the rows. The Database Methods
page
[Tables in SQL: CREATE TABLE, INSERT and SELECT](tutorial:a-table-is-a-list-of-rows)
explains each of these.

```sql exec
id: sets-db-build
DROP TABLE IF EXISTS my_song_tbl;
DROP TABLE IF EXISTS your_song_tbl;

CREATE TABLE my_song_tbl (
    my_song_id INTEGER PRIMARY KEY,
    title TEXT
);
INSERT INTO my_song_tbl (title) VALUES
    ('Zombie'), ('Linger'), ('Galway Girl'), ('One'),
    ('Linger'), ('Chasing Cars'), ('Dreams');

CREATE TABLE your_song_tbl (
    your_song_id INTEGER PRIMARY KEY,
    title TEXT
);
INSERT INTO your_song_tbl (title) VALUES
    ('Take Me to Church'), ('Zombie'), ('Outnumbered'), ('Dreams'),
    ('Breakeven'), ('Zombie'), ('All I Want');
```

Each table has a column ending in `_id`. A *primary key* is a column
whose value is different on every row, so that each row can be named.
SQLite fills it in by itself, counting 1, 2, 3.

`SELECT my_song_id, title FROM my_song_tbl` asks for those two columns
of every row in `my_song_tbl`. "Linger" is on my playlist twice. How many rows do you think come
back: 6 or 7? Run it to check.

```sql exec
id: sets-db-select
SELECT my_song_id, title FROM my_song_tbl;
```

Seven. A Python set dropped the second "Linger", but the table keeps
it. The two "Linger" rows are different rows, because their keys, 2 and
5, are different. So a table is a set of rows, and the key is what
makes each row different. It is not a set of titles.

When we want the titles as a set, `SELECT DISTINCT` keeps each
different value once. It does for a column what `set()` did for a list.

```sql exec
id: sets-db-distinct
SELECT DISTINCT title FROM my_song_tbl;
```

Six titles, and "Linger" once.

## Union: UNION

How many different songs are there between you? On
[Collections without repeats](tutorial:collections-without-repeats#on-either-list-union)
the union, $A \cup B$, was `my_songs | your_songs`, and it held 10
songs.

In SQL, `UNION` goes between two queries. It takes the rows of both and
keeps each different row once. A query made of two queries joined like
this is called a *compound query*. The `ORDER BY title` at the end
sorts the whole result by title, because a table, like a set, makes no
promise about order. Do you expect 10 rows again?

```sql exec
id: sets-db-union
SELECT title FROM my_song_tbl
UNION
SELECT title FROM your_song_tbl
ORDER BY title;
```

The same 10 songs. `UNION` dropped the second "Linger", the two extra
"Zombie" rows and the shared "Dreams", as Python's `|` did.

Sometimes the repeats matter. A radio station might want every song
request, not every different song. `UNION ALL` keeps every row from both
sides. With 7 rows on each side, how many will that be?

```sql exec
id: sets-db-union-all
SELECT title FROM my_song_tbl
UNION ALL
SELECT title FROM your_song_tbl;
```

Fourteen rows: all 7 of mine, then all 7 of yours. `UNION ALL` is
closer to adding two lists with `+` than to a set operation.

### Rows must have the same shape

The next cell asks for two columns from my table and one from yours.
It will stop with an error, on purpose.

```sql exec
id: sets-db-union-error
SELECT my_song_id, title FROM my_song_tbl
UNION
SELECT title FROM your_song_tbl;
```

The message says that the `SELECT`s on the left and the right of
`UNION` "do not have the same number of result columns". In maths, you
may take the union of any two sets. In SQL, every row of a result has
the same columns, so both sides must give rows of the same shape. It is
the fourth question: this space allows a union only of rows that line
up column by column.

## Intersection and difference: INTERSECT and EXCEPT

Which songs are on both playlists? SQL's word for $A \cap B$ is
`INTERSECT`. Guess the rows before you run it.

```sql exec
id: sets-db-intersect
SELECT title FROM my_song_tbl
INTERSECT
SELECT title FROM your_song_tbl;
```

"Dreams" and "Zombie", as `&` gave on
[Collections without repeats](tutorial:collections-without-repeats#on-both-lists-intersection).
Each appears once, although "Zombie" is in your table twice. Like
`UNION`, `INTERSECT` keeps each different row once.

The difference $A \setminus B$ is `EXCEPT`: the rows of the first query
that are not in the second. Which songs are mine and not yours?

```sql exec
id: sets-db-except
SELECT title FROM my_song_tbl
EXCEPT
SELECT title FROM your_song_tbl;
```

Four songs: "Chasing Cars", "Galway Girl", "Linger" and "One". Here is
the same question in Python, with the lists from the build cell. Each
line should give the same songs as one of the SQL cells above.

```python exec
id: sets-db-in-python
mine = ["Zombie", "Linger", "Galway Girl", "One", "Linger", "Chasing Cars", "Dreams"]
yours = ["Take Me to Church", "Zombie", "Outnumbered", "Dreams", "Breakeven",
         "Zombie", "All I Want"]

print(sorted(set(mine) | set(yours)))
print(sorted(set(mine) & set(yours)))
print(sorted(set(mine) - set(yours)))
```

The three lines match `UNION`, `INTERSECT` and `EXCEPT`. The same three
ideas have three ways of being written:

| The idea | In maths | In Python | In SQL |
|---|---|---|---|
| in either, or both | $A \cup B$ | `a \| b` | `UNION` |
| in both | $A \cap B$ | `a & b` | `INTERSECT` |
| in the first, not the second | $A \setminus B$ | `a - b` | `EXCEPT` |
| every value, repeats and all | (no set symbol) | `list_a + list_b` | `UNION ALL` |
| each value once | a set | `set(values)` | `SELECT DISTINCT` |

SQL has no word for the complement, $A'$. A complement needs a universal
set, as
[Circles that overlap](tutorial:circles-that-overlap#two-circles-in-a-box)
drew with its box. In a database, the box must be a table of its own,
such as every song in the music library. Then "not on my playlist" is
`SELECT title FROM library_song_tbl EXCEPT SELECT title FROM my_song_tbl`.
The database cannot guess which space you mean, so you name it.

### Your turn

1. Swap the two tables in the `EXCEPT` cell. Before you run it, which
   four songs will come back?
2. Change `INTERSECT` to `UNION ALL` in its cell, and then back again.
   How many rows does each give, and why?
3. SQL has no word for the symmetric difference either. It is
   $(A \setminus B) \cup (B \setminus A)$: the songs on exactly one
   playlist. Try to write it in the empty cell below, using two
   `EXCEPT`s and a `UNION`. The answer is under the cell.

```sql exec
id: sets-db-your-turn
-- The songs on exactly one of the two playlists
```

<details class="dl-answer"><summary>Answer</summary>

A compound query can use another compound query as if it were a table,
once it is put in brackets after `FROM`:

    SELECT title FROM (
        SELECT title FROM my_song_tbl
        EXCEPT
        SELECT title FROM your_song_tbl
    )
    UNION
    SELECT title FROM (
        SELECT title FROM your_song_tbl
        EXCEPT
        SELECT title FROM my_song_tbl
    )
    ORDER BY title;

It gives eight songs, the same eight as `my_songs ^ your_songs`.

</details>

## Every pair: CROSS JOIN

The Cartesian product $A \times B$ is every pair $(a, b)$, with $a$
from $A$ and $b$ from $B$. On
[Counting every outfit](tutorial:counting-every-outfit#a-tool-that-lists-every-pair)
you built it with `all_pairs`. In SQL it is a `CROSS JOIN`, which pairs
every row of one table with every row of the other.

The result is too long to show, so this query only counts it. `COUNT(*)`
gives the number of rows in a result. Each playlist has 6 different
songs, and 7 rows. Will the count be 36 or 49?

```sql exec
id: sets-db-cross-join
SELECT COUNT(*) FROM my_song_tbl CROSS JOIN your_song_tbl;
```

It is 49, which is $7 \times 7$. The counting principle,
$|A \times B| = |A| \times |B|$, holds for tables too, as long as we
count rows and not titles: a `CROSS JOIN` pairs rows, and each "Linger"
row gets its own seven partners.

## A JOIN keeps the pairs that match

Most of those 49 pairs are of no use. What if we keep only the pairs where both rows have the same
title? `WHERE` keeps only the rows where its condition is true. When two
tables are in one query, `my_song_tbl.title` means "the `title` column
of `my_song_tbl`".

`INTERSECT` gave 2 rows. How many pairs do you think have the same
title on both sides?

```sql exec
id: sets-db-matching-pairs
SELECT my_song_id, your_song_id, my_song_tbl.title
FROM my_song_tbl CROSS JOIN your_song_tbl
WHERE my_song_tbl.title = your_song_tbl.title;
```

Three pairs. "Dreams" makes one pair. "Zombie" makes two, because my
one "Zombie" row matches each of your two "Zombie" rows, 2 and 6.

Keeping the matching pairs of a `CROSS JOIN` is so common that SQL has
a shorter way to write it. A `JOIN ... ON` pairs the rows of two tables
where the condition after `ON` is true. Will this give the same three
rows?

```sql exec
id: sets-db-join
SELECT my_song_id, your_song_id, my_song_tbl.title
FROM my_song_tbl
JOIN your_song_tbl ON my_song_tbl.title = your_song_tbl.title;
```

The same three rows. So a `JOIN` is the Cartesian product with a
condition: every pair, then only the pairs that match. The database does
not usually build all 49 pairs first. It finds the matches more directly,
often with a lookup that works a little like a set's hash. But the
answer is the one the long way promises, as the loop on
[Collections without repeats](tutorial:collections-without-repeats#on-both-lists-intersection)
was the proof of `&`.

On
[Collections without repeats](tutorial:collections-without-repeats#from-sets-to-databases),
we said that a `JOIN` keeps what two tables have in common, as an
intersection does. We can now say it more exactly. `INTERSECT` keeps
the values both sides have. A `JOIN` keeps the pairs of rows that
match, so a repeat on either side gives an extra pair. That is why
"Zombie" came back once from `INTERSECT` and twice from the `JOIN`.

In a real database, the condition after `ON` is almost always a key.
The Database Methods page
[Joining two tables: foreign keys and JOIN](tutorial:a-second-table-and-a-join)
joins fossil sites to dinosaurs on `dinosaur_id`, which names exactly
one dinosaur. And the rows that find no partner, like "Linger" and "One"
here, are left out of a `JOIN` without a word. Those rows are the ones
`EXCEPT` found. The page
[Joining real tables: the rows a JOIN drops](tutorial:joining-two-real-tables)
shows how to see them, with a `LEFT JOIN`.

## Where the idea came from

Databases were not always built on sets. In 1970, Edgar F. Codd, a
British computer scientist working at IBM, published a paper that
treated a table as a *relation*: a set of rows, all with the same
columns. Once a table is
a set, every move on sets becomes a move on tables, and a question can
say what it wants without saying how to find it. SQL grew out of
that idea at IBM in the years after. The databases built this way are
still called relational databases.

SQL did not follow Codd all the way. His relations held each row once,
and a SQL table may hold repeats. That is why SQL needs both `UNION`
and `UNION ALL`, and why `DISTINCT` exists at all.

## Where to read more

Codd, E. F. (1970). A relational model of data for large shared data
banks. *Communications of the ACM*, 13(6). The paper that started
relational databases. Its first pages explain the idea in words, before
the notation begins.

The Database Methods course builds real tables with SQL, starting with
[Tables in SQL: CREATE TABLE, INSERT and SELECT](tutorial:a-table-is-a-list-of-rows).
