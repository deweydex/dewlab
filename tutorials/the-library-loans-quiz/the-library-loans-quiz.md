---
title: "The library loans quiz: books, authors and loans"
year: "2026-2027"
version: 2026.09.26.2
covers:
  task-1-authors-and-books:
    touches: [DBM-LO2]
  task-2-a-book-can-have-more-than-one-author:
    covers: [DBM-LO9, DBM-LO11]
  task-3-members-and-loans:
    touches: [DBM-LO2]
  task-4-add-authors-books-and-authorships:
    covers: [DBM-LO10]
  task-5-add-members-and-loans:
    touches: [DBM-LO10]
  task-6-two-questions-for-your-database:
    touches: [DBM-LO5]
---

# The library loans quiz: books, authors and loans

You are building a database for a small library: which books it holds,
who wrote each one, who has borrowed what, and what is overdue. Six
tasks build it, one piece at a time. Nothing here is graded. Each task
has a check cell below it. Run that cell, and it tells you, instantly
and only in your own browser, whether the task's requirements are met.
Run it as often as you like.

This library's books do not always have one author each. Some are
written by two people together. This one fact makes this database
different from [a college timetable](tutorial:a-college-timetable).
Every relationship there was one thing pointing at one other thing. A
book can point at *several* authors, and an author can point at several
books. You meet this in Task 2.

Write your SQL in this box as you go. Your code is saved on this
device, the same as every cell on this site. After a reload, run this
box again to rebuild your tables. Use the hints if you need them.

The box starts with five `DROP TABLE IF EXISTS` lines. The page keeps
its database for as long as it is open, so each run finds the tables
from the run before. These lines delete those tables first. Without
them, the second run stops at your first `CREATE TABLE` with the error
`table author_tbl already exists`. The two tables whose rows point into
other tables, `loan_tbl` and `book_author_tbl`, are deleted first.

```sql exec
id: library-quiz-workspace
-- These delete the tables from the last run, so this box can build
-- them again. Keep them at the top.
DROP TABLE IF EXISTS loan_tbl;
DROP TABLE IF EXISTS book_author_tbl;
DROP TABLE IF EXISTS member_tbl;
DROP TABLE IF EXISTS book_tbl;
DROP TABLE IF EXISTS author_tbl;

-- Build the database here, one task at a time. Run this box after
-- every change, then use each task's check cell below.
```

## Task 1: authors and books

Create a table called `author_tbl` with these columns:

- `author_id` is a whole number that identifies the row, filled in for
  you.
- `name` is text.

Create a second table called `book_tbl` with these columns:

- `book_id` is a whole number that identifies the row, filled in for
  you.
- `title` is text.
- `publication_year` is a whole number.

<details class="dl-hint"><summary>hint</summary>

Two separate `CREATE TABLE` statements, one for each table, the way
every table on the earlier pages in this module was built.

</details>

```python exec
id: check-authors-and-books-tables
expect: bool(author_columns and book_columns) and not missing
author_columns = {row[1] for row in db.execute("PRAGMA table_info(author_tbl)")}
book_columns = {row[1] for row in db.execute("PRAGMA table_info(book_tbl)")}
missing = set()
if not author_columns:
    print("There is no author_tbl table yet.")
else:
    missing |= {"author_tbl." + column for column in {"author_id", "name"} - author_columns}
if not book_columns:
    print("There is no book_tbl table yet.")
else:
    missing |= {"book_tbl." + column for column in {"book_id", "title", "publication_year"} - book_columns}
if missing:
    print("Missing:", ", ".join(sorted(missing)) + ".")
if bool(author_columns and book_columns) and not missing:
    print("Found author_tbl and book_tbl, with every column this task names.")
```

## Task 2: a book can have more than one author

Neither `author_tbl` nor `book_tbl` says which author wrote which book.
A third table does, since either one could point at several of the
other. Create a table called `book_author_tbl` with these columns:

- `book_id` is a whole number naming a row in `book_tbl`.
- `author_id` is a whole number naming a row in `author_tbl`.

This table has no key of its own, so there is no `book_author_id`. One
row of `book_author_tbl` means "this book has this author," and that
pair identifies the row. A separate key would add nothing. Make
`book_id` and `author_id` *together* the table's primary key, with `PRIMARY KEY
(book_id, author_id)` as a line of its own inside the `CREATE TABLE`,
after the two columns. Each column keeps the name of the key it points
at, the same as any other foreign key.

A table like this, joining two others many-to-many, is called a
*junction table*. Each row is one point where one book and one author
meet, like a junction where two roads meet.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Write the two columns first, `book_id INTEGER` and `author_id
   INTEGER`, the same way any other column is written.
2. After the last column, add one more line: `PRIMARY KEY (book_id,
   author_id)`. This line names two columns together as the primary
   key, rather than marking one column `PRIMARY KEY` on its own the way
   every earlier table in this module did.
3. Run `PRAGMA table_info(book_author_tbl);` in the SQL box and look at its
   last column. A `0` means that column is not part of the primary key.
   Any other number means it is, and shows its position within it.
   Both `book_id` and `author_id` should show a non-zero number.

**Think about:** why would an ordinary single-column key, such as a
`book_author_id`, not stop the same book being linked to the same author
twice? The composite key here does stop it.

**Try this next:** [a college timetable](tutorial:a-college-timetable)
solved a different problem. It found two rows that clash by comparing a
table to itself. This table solves a different problem again: letting
one row on each side connect to several rows on the other. Compare the
two designs while you remember both.

</details>

```python exec
id: check-book-authors-table
expect: not missing and pk_columns == required
columns = {row[1] for row in db.execute("PRAGMA table_info(book_author_tbl)")}
required = {"book_id", "author_id"}
missing = required - columns
pk_columns = {row[1] for row in db.execute("PRAGMA table_info(book_author_tbl)") if row[5] > 0}
if not columns:
    print("There is no book_author_tbl table yet.")
elif missing:
    print("book_author_tbl is missing:", ", ".join(sorted(missing)) + ".")
elif pk_columns != required:
    print("book_id and author_id both need to be part of the primary key, together.")
if not missing and pk_columns == required:
    print("Found book_author_tbl, with book_id and author_id together as its primary key.")
```

## Task 3: members and loans

Create a table called `member_tbl` with these columns:

- `member_id` is a whole number that identifies the row, filled in for
  you.
- `name` is text.

Create a table called `loan_tbl` with these columns:

- `loan_id` is a whole number that identifies the row, filled in for
  you.
- `book_id` is a whole number naming a row in `book_tbl`.
- `member_id` is a whole number naming a row in `member_tbl`.
- `borrowed_date` is text, in `'YYYY-MM-DD'` form.
- `due_date` is text, in the same form.
- `returned_date` is text, in the same form, and you can leave it blank.
  A blank `returned_date` means the book has not come back yet.

<details class="dl-hint"><summary>hint</summary>

`loan_tbl` has an ordinary `loan_id INTEGER PRIMARY KEY`, unlike
`book_author_tbl`. One loan is its own event, not a pairing that needs
to stay unique. Its two foreign keys, `book_id` and `member_id`, go
directly under `loan_id`, before the dates.

</details>

```python exec
id: check-members-and-loans-tables
expect: bool(member_columns and loan_columns) and not missing
member_columns = {row[1] for row in db.execute("PRAGMA table_info(member_tbl)")}
loan_columns = {row[1] for row in db.execute("PRAGMA table_info(loan_tbl)")}
missing = set()
if not member_columns:
    print("There is no member_tbl table yet.")
else:
    missing |= {"member_tbl." + column for column in {"member_id", "name"} - member_columns}
if not loan_columns:
    print("There is no loan_tbl table yet.")
else:
    required_loan_columns = {"loan_id", "book_id", "member_id", "borrowed_date", "due_date", "returned_date"}
    missing |= {"loan_tbl." + column for column in required_loan_columns - loan_columns}
if missing:
    print("Missing:", ", ".join(sorted(missing)) + ".")
if bool(member_columns and loan_columns) and not missing:
    print("Found member_tbl and loan_tbl, with every column this task names.")
```

## Task 4: add authors, books, and authorships

Insert at least four authors and at least five books. Then insert rows
into `book_author_tbl` connecting them, so that:

- At least one book has two authors.
- At least one author has written two books.

<details class="dl-hint"><summary>hint</summary>

A real pair of co-written books works well here. *Good Omens* is one
example. Its two authors also each wrote books of their own. Insert both
authors, then insert a `book_author_tbl` row for
each of them against the same book's `book_id`.

</details>

```python exec
id: check-authors-books-authorships
expect: author_count >= 4 and book_count >= 5 and shared_book >= 1 and shared_author >= 1
authors_exist = bool(list(db.execute("PRAGMA table_info(author_tbl)")))
books_exist = bool(list(db.execute("PRAGMA table_info(book_tbl)")))
book_authors_exist = bool(list(db.execute("PRAGMA table_info(book_author_tbl)")))
if not (authors_exist and books_exist and book_authors_exist):
    print("author_tbl, book_tbl and book_author_tbl all need to exist before this check means anything.")
    author_count = book_count = shared_book = shared_author = 0
else:
    author_count = db.execute("SELECT COUNT(*) FROM author_tbl").fetchone()[0]
    book_count = db.execute("SELECT COUNT(*) FROM book_tbl").fetchone()[0]
    print(f"{author_count} authors, {book_count} books.")
    shared_book = db.execute(
        "SELECT COUNT(*) FROM (SELECT book_id FROM book_author_tbl GROUP BY book_id HAVING COUNT(*) >= 2)"
    ).fetchone()[0]
    shared_author = db.execute(
        "SELECT COUNT(*) FROM (SELECT author_id FROM book_author_tbl GROUP BY author_id HAVING COUNT(*) >= 2)"
    ).fetchone()[0]
    if not shared_book:
        print("No book in book_author_tbl has two or more authors yet.")
    if not shared_author:
        print("No author in book_author_tbl has written two or more books yet.")
if author_count >= 4 and book_count >= 5 and shared_book >= 1 and shared_author >= 1:
    print("Found at least four authors, five books, a book with two authors, and an author with two books.")
```

```hint
for: check-authors-books-authorships
after: 2 runs

Read what the check printed: how many authors and books it counted, and
whether it found a shared book or a shared author yet.

A book with two authors needs two rows in `book_author_tbl` that name the
same `book_id` with two different `author_id`s. An author with two
books needs the mirror image: two rows naming the same `author_id` with
two different `book_id`s. One well-chosen pair of `book_author_tbl` rows,
covering a genuinely co-written book, can satisfy both counts at once.
```

## Task 5: add members and loans

Insert at least three members. Then insert at least four loans, each
naming a real `book_id` and `member_id`. At least one loan needs a
`returned_date` before `'2026-09-01'`, and at least one other loan needs
`returned_date` left blank, with a `due_date` before `'2026-09-01'`.
That book is overdue right now.

<details class="dl-hint"><summary>hint</summary>

`INSERT INTO loan_tbl (book_id, member_id, borrowed_date, due_date,
returned_date) VALUES (1, 1, '2026-08-01', '2026-08-15', NULL)` leaves
`returned_date` blank with `NULL`. Leaving the column out of the
`INSERT` entirely, rather than writing `NULL`, works the same way.

</details>

```python exec
id: check-members-and-loans-rows
expect: member_count >= 3 and loan_count >= 4 and returned_before_cutoff >= 1 and overdue_now >= 1
members_exist = bool(list(db.execute("PRAGMA table_info(member_tbl)")))
loans_exist = bool(list(db.execute("PRAGMA table_info(loan_tbl)")))
if not (members_exist and loans_exist):
    print("member_tbl and loan_tbl both need to exist before this check means anything.")
    member_count = loan_count = returned_before_cutoff = overdue_now = 0
else:
    member_count = db.execute("SELECT COUNT(*) FROM member_tbl").fetchone()[0]
    loan_count = db.execute("SELECT COUNT(*) FROM loan_tbl").fetchone()[0]
    print(f"{member_count} members, {loan_count} loans.")
    returned_before_cutoff = db.execute(
        "SELECT COUNT(*) FROM loan_tbl WHERE returned_date IS NOT NULL AND returned_date < '2026-09-01'"
    ).fetchone()[0]
    overdue_now = db.execute(
        "SELECT COUNT(*) FROM loan_tbl WHERE returned_date IS NULL AND due_date < '2026-09-01'"
    ).fetchone()[0]
    if not returned_before_cutoff:
        print("No loan has a returned_date before 2026-09-01 yet.")
    if not overdue_now:
        print("No loan is overdue yet — returned_date IS NULL with a due_date before 2026-09-01.")
if member_count >= 3 and loan_count >= 4 and returned_before_cutoff >= 1 and overdue_now >= 1:
    print("Found at least three members, four loans, one loan already returned, and one overdue.")
```

## Task 6: two questions for your database

Try writing and running each of these two queries:

- Every author of one specific book you chose in task 4, joining
  `book_author_tbl` to `author_tbl`.
- Every loan that is overdue right now: `returned_date IS NULL` and
  `due_date` before `'2026-09-01'`, joining `loan_tbl` to `book_tbl` and
  `member_tbl` so the result shows a title and a borrower's name rather
  than bare ids.

<details class="dl-hint"><summary>hint</summary>

`SELECT author_tbl.name FROM book_author_tbl JOIN author_tbl ON
book_author_tbl.author_id = author_tbl.author_id WHERE
book_author_tbl.book_id = 1;` is the shape of the first query, once you
know which book's `book_id` you want.

</details>

This check looks at whether your data can answer both questions, not at
the queries themselves. There is more than one correct way to write a
`SELECT`.

```python exec
id: check-quiz-queries
expect: bool(book_with_two_authors) and overdue_count > 0
book_authors_exist = bool(list(db.execute("PRAGMA table_info(book_author_tbl)")))
loans_exist = bool(list(db.execute("PRAGMA table_info(loan_tbl)")))
if not (book_authors_exist and loans_exist):
    print("book_author_tbl and loan_tbl both need to exist before this check means anything.")
    book_with_two_authors = None
    overdue_count = 0
else:
    book_with_two_authors = db.execute(
        "SELECT book_id FROM book_author_tbl GROUP BY book_id HAVING COUNT(*) >= 2 LIMIT 1"
    ).fetchone()
    overdue_count = db.execute(
        "SELECT COUNT(*) FROM loan_tbl WHERE returned_date IS NULL AND due_date < '2026-09-01'"
    ).fetchone()[0]
    if not book_with_two_authors:
        print("Task 4's book with two authors needs to exist before the first query means anything.")
    if not overdue_count:
        print("Task 5's overdue loan needs to exist before the second query means anything.")
if bool(book_with_two_authors) and overdue_count > 0:
    print("Your data has a book with two authors and an overdue loan, so both queries have something to find.")
```

## One way to do it

If every check passes, your own database already meets the tasks.
This is one complete solution, not the only one. Compare it with your
own to see a full example.

<details class="dl-answer"><summary>a worked solution</summary>

![Five tables. book_author_tbl sits between book_tbl and author_tbl. A line runs from book_id in book_tbl to book_id in book_author_tbl, and another from author_id in author_tbl to author_id in book_author_tbl. Both of its columns are marked PK, so one row of it is one book paired with one author. loan_tbl points at book_tbl through book_id and at member_tbl through member_id.](library-erd.svg)

```sql
DROP TABLE IF EXISTS loan_tbl;
DROP TABLE IF EXISTS book_author_tbl;
DROP TABLE IF EXISTS member_tbl;
DROP TABLE IF EXISTS book_tbl;
DROP TABLE IF EXISTS author_tbl;

CREATE TABLE author_tbl (
    author_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE book_tbl (
    book_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    publication_year INTEGER
);

CREATE TABLE book_author_tbl (
    book_id INTEGER NOT NULL,
    author_id INTEGER NOT NULL,
    PRIMARY KEY (book_id, author_id),
    FOREIGN KEY (book_id) REFERENCES book_tbl(book_id),
    FOREIGN KEY (author_id) REFERENCES author_tbl(author_id)
);

CREATE TABLE member_tbl (
    member_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE loan_tbl (
    loan_id INTEGER PRIMARY KEY,
    book_id INTEGER NOT NULL,
    member_id INTEGER NOT NULL,
    borrowed_date TEXT NOT NULL,
    due_date TEXT NOT NULL,
    returned_date TEXT,
    FOREIGN KEY (book_id) REFERENCES book_tbl(book_id),
    FOREIGN KEY (member_id) REFERENCES member_tbl(member_id)
);

INSERT INTO author_tbl (name) VALUES
    ('Terry Pratchett'),
    ('Neil Gaiman'),
    ('Ursula K. Le Guin'),
    ('Ann Leckie');

INSERT INTO book_tbl (title, publication_year) VALUES
    ('Good Omens', 1990),
    ('Mort', 1987),
    ('American Gods', 2001),
    ('The Left Hand of Darkness', 1969),
    ('Ancillary Justice', 2013);

INSERT INTO book_author_tbl (book_id, author_id) VALUES
    (1, 1),
    (1, 2),
    (2, 1),
    (3, 2),
    (4, 3),
    (5, 4);

INSERT INTO member_tbl (name) VALUES
    ('Grace Lin'),
    ('Omar Farouk'),
    ('Beatriz Silva');

INSERT INTO loan_tbl (book_id, member_id, borrowed_date, due_date, returned_date) VALUES
    (1, 1, '2026-08-01', '2026-08-15', NULL),
    (2, 2, '2026-08-10', '2026-08-24', '2026-08-20'),
    (4, 3, '2026-09-01', '2026-09-15', NULL),
    (3, 1, '2026-07-01', '2026-07-15', '2026-07-10');

SELECT author_tbl.name
FROM book_author_tbl
JOIN author_tbl ON book_author_tbl.author_id = author_tbl.author_id
WHERE book_author_tbl.book_id = 1;

SELECT book_tbl.title, member_tbl.name, loan_tbl.due_date
FROM loan_tbl
JOIN book_tbl ON loan_tbl.book_id = book_tbl.book_id
JOIN member_tbl ON loan_tbl.member_id = member_tbl.member_id
WHERE loan_tbl.returned_date IS NULL AND loan_tbl.due_date < '2026-09-01';
```

`Good Omens`, `book_id` 1, has two rows in `book_author_tbl`: one for
Terry Pratchett, one for Neil Gaiman. Running the first `SELECT` on its
own returns both names. The second returns one row: `Good Omens`,
borrowed by Grace Lin, due back before the cutoff and never returned.

</details>
