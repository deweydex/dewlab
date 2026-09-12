---
title: "The Library Loans Quiz"
slug: the-library-loans-quiz
module: database-methods
module_title: "Database Methods"
year: "2026-2027"
series: practice
version: 2026.09.12.1
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

# The Library Loans Quiz

You are building a database for a small library: which books it holds,
who wrote each one, who has borrowed what, and what is overdue. Six
tasks build it, one piece at a time. Nothing here is graded. Each task
has a check cell below it. Run that cell, and it tells you, instantly
and only in your own browser, whether the task's requirements are met.
Run it as often as you like.

This library's own books do not always have one author each — some are
written by two people together. That single fact is what makes this
database genuinely different from [a college
timetable](tutorial:a-college-timetable): every relationship there was
one thing pointing at one other thing. A book can point at *several*
authors, and an author can point at several books. Task 2 is where that
shows up.

Write your SQL in this box as you go. Your code is saved on this
device, the same as every cell on this site. After a reload, run this
box again to rebuild your tables. Use the hints if you need them.

```sql exec
id: library-quiz-workspace
-- Build the database here, one task at a time. Run this box after
-- every change, then use each task's check cell below.
```

## Task 1: authors and books

Create a table called `authors` with these columns:

- `id` is a whole number that identifies the row, filled in for you.
- `name` is text.

Create a second table called `books` with these columns:

- `id` is a whole number that identifies the row, filled in for you.
- `title` is text.
- `publication_year` is a whole number.

<details class="dl-hint"><summary>hint</summary>

Two separate `CREATE TABLE` statements, one for each table, the way
every table on the earlier pages in this module was built.

</details>

```python exec
id: check-authors-and-books-tables
author_columns = {row[1] for row in db.execute("PRAGMA table_info(authors)")}
book_columns = {row[1] for row in db.execute("PRAGMA table_info(books)")}
missing = set()
if not author_columns:
    print("There is no authors table yet.")
else:
    missing |= {"authors." + column for column in {"id", "name"} - author_columns}
if not book_columns:
    print("There is no books table yet.")
else:
    missing |= {"books." + column for column in {"id", "title", "publication_year"} - book_columns}
if missing:
    print("Missing:", ", ".join(sorted(missing)) + ".")
check(author_columns and book_columns and not missing, True, label="authors and books both exist, with the columns this task asks for")
```

## Task 2: a book can have more than one author

Neither `authors` nor `books` says which author wrote which book — a
third table does, since either one could point at several of the other.
Create a table called `book_authors` with these columns:

- `book_id` is a whole number naming a row in `books`.
- `author_id` is a whole number naming a row in `authors`.

No `id` column this time. One row of `book_authors` means "this book has
this author," and that pairing is what identifies the row — there is
nothing else for an `id` to add. Make `book_id` and `author_id` *together*
the table's primary key, with `PRIMARY KEY (book_id, author_id)` as a
line of its own inside the `CREATE TABLE`, after the two columns.

A table like this, joining two others many-to-many, is called a
*junction table* — junction, because every row is a single crossing
point between one book and one author.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Write the two columns first, `book_id INTEGER` and `author_id
   INTEGER`, the same way any other column is written.
2. After the last column, add one more line: `PRIMARY KEY (book_id,
   author_id)`. This line names two columns together as the primary
   key, rather than marking one column `PRIMARY KEY` on its own the way
   every earlier table in this module did.
3. Run `PRAGMA table_info(book_authors);` in the SQL box and look at its
   last column. A `0` means that column is not part of the primary key;
   any other number means it is, and shows its position within it.
   Both `book_id` and `author_id` should show a non-zero number.

**Think about:** why an ordinary single-column `id` would not actually
stop the same book being linked to the same author twice, the way the
composite key here does.

**Try this next:** [a college timetable](tutorial:a-college-timetable)
solved a different problem — finding two rows that clash — by comparing
a table to itself. This table solves a different problem again: letting
one row on each side connect to several rows on the other. Compare the
two designs once both are fresh in your mind.

</details>

```python exec
id: check-book-authors-table
columns = {row[1] for row in db.execute("PRAGMA table_info(book_authors)")}
required = {"book_id", "author_id"}
missing = required - columns
pk_columns = {row[1] for row in db.execute("PRAGMA table_info(book_authors)") if row[5] > 0}
if not columns:
    print("There is no book_authors table yet.")
elif missing:
    print("book_authors is missing:", ", ".join(sorted(missing)) + ".")
elif pk_columns != required:
    print("book_id and author_id both need to be part of the primary key, together.")
check(not missing and pk_columns == required, True, label="book_authors exists, with book_id and author_id together as its primary key")
```

## Task 3: members and loans

Create a table called `members` with these columns:

- `id` is a whole number that identifies the row, filled in for you.
- `name` is text.

Create a table called `loans` with these columns:

- `id` is a whole number that identifies the row, filled in for you.
- `book_id` is a whole number naming a row in `books`.
- `member_id` is a whole number naming a row in `members`.
- `borrowed_date` is text, in `'YYYY-MM-DD'` form.
- `due_date` is text, in the same form.
- `returned_date` is text, in the same form, and you can leave it blank.
  A blank `returned_date` means the book has not come back yet.

<details class="dl-hint"><summary>hint</summary>

`loans` has an ordinary `id INTEGER PRIMARY KEY`, unlike `book_authors`
— one loan is its own event, not a pairing that needs to stay unique.

</details>

```python exec
id: check-members-and-loans-tables
member_columns = {row[1] for row in db.execute("PRAGMA table_info(members)")}
loan_columns = {row[1] for row in db.execute("PRAGMA table_info(loans)")}
missing = set()
if not member_columns:
    print("There is no members table yet.")
else:
    missing |= {"members." + column for column in {"id", "name"} - member_columns}
if not loan_columns:
    print("There is no loans table yet.")
else:
    required_loan_columns = {"id", "book_id", "member_id", "borrowed_date", "due_date", "returned_date"}
    missing |= {"loans." + column for column in required_loan_columns - loan_columns}
if missing:
    print("Missing:", ", ".join(sorted(missing)) + ".")
check(member_columns and loan_columns and not missing, True, label="members and loans both exist, with the columns this task asks for")
```

## Task 4: add authors, books, and authorships

Insert at least four authors and at least five books. Then insert rows
into `book_authors` connecting them, so that:

- At least one book has two authors.
- At least one author has written two books.

<details class="dl-hint"><summary>hint</summary>

A real pair of co-written books works well here — *Good Omens*, written
together by two authors who also each wrote books of their own, is one
example. Insert both authors, then insert a `book_authors` row for each
of them against the same book's `id`.

</details>

```python exec
id: check-authors-books-authorships
authors_exist = bool(list(db.execute("PRAGMA table_info(authors)")))
books_exist = bool(list(db.execute("PRAGMA table_info(books)")))
book_authors_exist = bool(list(db.execute("PRAGMA table_info(book_authors)")))
if not (authors_exist and books_exist and book_authors_exist):
    print("authors, books and book_authors all need to exist before this check means anything.")
    author_count = book_count = shared_book = shared_author = 0
else:
    author_count = db.execute("SELECT COUNT(*) FROM authors").fetchone()[0]
    book_count = db.execute("SELECT COUNT(*) FROM books").fetchone()[0]
    print(f"{author_count} authors, {book_count} books.")
    shared_book = db.execute(
        "SELECT COUNT(*) FROM (SELECT book_id FROM book_authors GROUP BY book_id HAVING COUNT(*) >= 2)"
    ).fetchone()[0]
    shared_author = db.execute(
        "SELECT COUNT(*) FROM (SELECT author_id FROM book_authors GROUP BY author_id HAVING COUNT(*) >= 2)"
    ).fetchone()[0]
    if not shared_book:
        print("No book in book_authors has two or more authors yet.")
    if not shared_author:
        print("No author in book_authors has written two or more books yet.")
check(
    author_count >= 4 and book_count >= 5 and shared_book >= 1 and shared_author >= 1,
    True,
    label="at least four authors, five books, a book with two authors, and an author with two books",
)
```

```hint
for: check-authors-books-authorships
after: 2 failed checks

Read what the check printed: how many authors and books it counted, and
whether it found a shared book or a shared author yet.

A book with two authors needs two rows in `book_authors` that name the
same `book_id` with two different `author_id`s. An author with two
books needs the mirror image: two rows naming the same `author_id` with
two different `book_id`s. One well-chosen pair of `book_authors` rows,
covering a genuinely co-written book, can satisfy both counts at once.
```

## Task 5: add members and loans

Insert at least three members. Then insert at least four loans, each
naming a real `book_id` and `member_id`. At least one loan needs a
`returned_date` before `'2026-09-01'`, and at least one other loan needs
`returned_date` left blank, with a `due_date` before `'2026-09-01'` —
a book that is overdue right now.

<details class="dl-hint"><summary>hint</summary>

`INSERT INTO loans (book_id, member_id, borrowed_date, due_date,
returned_date) VALUES (1, 1, '2026-08-01', '2026-08-15', NULL)` leaves
`returned_date` blank with `NULL`. Leaving the column out of the
`INSERT` entirely, rather than writing `NULL`, works the same way.

</details>

```python exec
id: check-members-and-loans-rows
members_exist = bool(list(db.execute("PRAGMA table_info(members)")))
loans_exist = bool(list(db.execute("PRAGMA table_info(loans)")))
if not (members_exist and loans_exist):
    print("members and loans both need to exist before this check means anything.")
    member_count = loan_count = returned_before_cutoff = overdue_now = 0
else:
    member_count = db.execute("SELECT COUNT(*) FROM members").fetchone()[0]
    loan_count = db.execute("SELECT COUNT(*) FROM loans").fetchone()[0]
    print(f"{member_count} members, {loan_count} loans.")
    returned_before_cutoff = db.execute(
        "SELECT COUNT(*) FROM loans WHERE returned_date IS NOT NULL AND returned_date < '2026-09-01'"
    ).fetchone()[0]
    overdue_now = db.execute(
        "SELECT COUNT(*) FROM loans WHERE returned_date IS NULL AND due_date < '2026-09-01'"
    ).fetchone()[0]
    if not returned_before_cutoff:
        print("No loan has a returned_date before 2026-09-01 yet.")
    if not overdue_now:
        print("No loan is overdue yet — returned_date IS NULL with a due_date before 2026-09-01.")
check(
    member_count >= 3 and loan_count >= 4 and returned_before_cutoff >= 1 and overdue_now >= 1,
    True,
    label="at least three members, four loans, one already returned, and one overdue",
)
```

## Task 6: two questions for your database

Try writing and running each of these two queries:

- Every author of one specific book you chose in task 4, joining
  `book_authors` to `authors`.
- Every loan that is overdue right now: `returned_date IS NULL` and
  `due_date` before `'2026-09-01'`, joining `loans` to `books` and
  `members` so the result shows a title and a borrower's name rather
  than bare ids.

<details class="dl-hint"><summary>hint</summary>

`SELECT authors.name FROM book_authors JOIN authors ON
book_authors.author_id = authors.id WHERE book_authors.book_id = 1;` is
the shape of the first query, once you know which book's `id` you want.

</details>

This check looks at whether your data can answer both questions, not at
the queries themselves. There is more than one correct way to write a
`SELECT`.

```python exec
id: check-quiz-queries
book_authors_exist = bool(list(db.execute("PRAGMA table_info(book_authors)")))
loans_exist = bool(list(db.execute("PRAGMA table_info(loans)")))
if not (book_authors_exist and loans_exist):
    print("book_authors and loans both need to exist before this check means anything.")
    book_with_two_authors = None
    overdue_count = 0
else:
    book_with_two_authors = db.execute(
        "SELECT book_id FROM book_authors GROUP BY book_id HAVING COUNT(*) >= 2 LIMIT 1"
    ).fetchone()
    overdue_count = db.execute(
        "SELECT COUNT(*) FROM loans WHERE returned_date IS NULL AND due_date < '2026-09-01'"
    ).fetchone()[0]
    if not book_with_two_authors:
        print("Task 4's book with two authors needs to exist before the first query means anything.")
    if not overdue_count:
        print("Task 5's overdue loan needs to exist before the second query means anything.")
check(bool(book_with_two_authors) and overdue_count > 0, True, label="your data can answer both queries")
```

## One way to do it

Every check passing means your own database already meets the tasks.
This is one complete solution, not the only one. Compare it with your
own to see a full example.

<details class="dl-answer"><summary>a worked solution</summary>

```sql
CREATE TABLE authors (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE books (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    publication_year INTEGER
);

CREATE TABLE book_authors (
    book_id INTEGER NOT NULL,
    author_id INTEGER NOT NULL,
    PRIMARY KEY (book_id, author_id)
);

CREATE TABLE members (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE loans (
    id INTEGER PRIMARY KEY,
    book_id INTEGER NOT NULL,
    member_id INTEGER NOT NULL,
    borrowed_date TEXT NOT NULL,
    due_date TEXT NOT NULL,
    returned_date TEXT
);

INSERT INTO authors (name) VALUES
    ('Terry Pratchett'),
    ('Neil Gaiman'),
    ('Ursula K. Le Guin'),
    ('Ann Leckie');

INSERT INTO books (title, publication_year) VALUES
    ('Good Omens', 1990),
    ('Mort', 1987),
    ('American Gods', 2001),
    ('The Left Hand of Darkness', 1969),
    ('Ancillary Justice', 2013);

INSERT INTO book_authors (book_id, author_id) VALUES
    (1, 1),
    (1, 2),
    (2, 1),
    (3, 2),
    (4, 3),
    (5, 4);

INSERT INTO members (name) VALUES
    ('Grace Lin'),
    ('Omar Farouk'),
    ('Beatriz Silva');

INSERT INTO loans (book_id, member_id, borrowed_date, due_date, returned_date) VALUES
    (1, 1, '2026-08-01', '2026-08-15', NULL),
    (2, 2, '2026-08-10', '2026-08-24', '2026-08-20'),
    (4, 3, '2026-09-01', '2026-09-15', NULL),
    (3, 1, '2026-07-01', '2026-07-15', '2026-07-10');

SELECT authors.name
FROM book_authors
JOIN authors ON book_authors.author_id = authors.id
WHERE book_authors.book_id = 1;

SELECT books.title, members.name, loans.due_date
FROM loans
JOIN books ON loans.book_id = books.id
JOIN members ON loans.member_id = members.id
WHERE loans.returned_date IS NULL AND loans.due_date < '2026-09-01';
```

`Good Omens`, `book_id` 1, has two rows in `book_authors` — one for
Terry Pratchett, one for Neil Gaiman. Running the first `SELECT` on its
own returns both names. The second returns one row: `Good Omens`,
borrowed by Grace Lin, due back before the cutoff and never returned.

</details>
