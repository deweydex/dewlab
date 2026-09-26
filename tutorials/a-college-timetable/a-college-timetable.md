---
title: "A college timetable: five tables and finding clashes"
year: "2026-2027"
version: 2026.09.26.1
covers:
  five-tables-for-one-timetable:
    covers: [DBM-LO9]
  building-it:
    covers: [DBM-LO10]
  asking-it-real-questions:
    touches: [DBM-LO5]
  finding-a-clash:
    covers: [DBM-LO5]
    touches: [DBM-LO9]
  the-same-idea-for-a-teacher:
    touches: [DBM-LO5]
  your-turn:
    touches: [DBM-LO10, DBM-LO11]
---

# A college timetable: five tables and finding clashes

A further education college runs on a timetable: which room, which
teacher, which module, on which date, between which two times. Every
earlier page in this series built a database with one or two tables. A
timetable needs more than that, and it needs to answer a question no
single table can: has anyone been booked into the same room, or asked to
teach in two places, at the same time.

This page designs and builds that database, then writes the query that
actually finds a clash. It is the longest page in this module on
purpose. A short example can show you the shape of a technique. A
problem this size is closer to the one a real college's admin office
actually has.

## Five tables for one timetable

Start with what the college needs to keep track of, before writing a
single `CREATE TABLE`.

A *programme* is a course a student enrols in, such as Software
Development, Business Studies or Culinary Arts. A programme has a name,
and nothing
else worth storing about it here.

A *module* belongs to one programme. Software Development includes
Database Methods and Web Authoring. Business Studies includes
Bookkeeping and Marketing Fundamentals. A module needs its own name, and
a column pointing back at the programme it belongs to.

A *teacher* has a name. Nothing here says which module a teacher
teaches. That fact belongs somewhere else, because the same teacher
can teach more than one module, and the same module could, in principle,
be taught by more than one teacher across different groups.

A *room* has a name and a capacity: how many people can sit in it at
once.

None of the four tables above says anything about *when*. A fifth table,
for *sessions*, does that. It has one row per class, naming which
module it is, which teacher is running it, which room it is in, what
date, and what time it starts and ends.

Each table gets a name in the course's usual way: `programme_tbl`,
`module_tbl`, `teacher_tbl`, `room_tbl` and `session_tbl`, each with a
key named after it, such as `room_id`. A column that points at another
table has that table's key name, and sits straight under its own key.
So `session_tbl` starts with `session_id`, then `module_id`,
`teacher_id` and `room_id`, then the date and times.

The date needs a design decision of its own. A weekday name, such as
`'Monday'` or `'Tuesday'`, reads well, but it sorts alphabetically. As
plain text, `'Friday'` comes before `'Monday'`, which would put the end
of the week at the top of every list this page builds. A calendar date,
written `'2026-09-14'`, sorts the same way whether the computer reads it
as text or as a date. So this page uses real dates instead.

![Five tables. programme_tbl, teacher_tbl and room_tbl stand on their own.
module_tbl points at programme_tbl, with a line from programme_id to
programme_id. session_tbl points at module_tbl, teacher_tbl and room_tbl,
so three lines arrive at it, each from a key to the column of the same
name, and none leave.](timetable-erd.svg)

Four tables describe things, and a fifth describes an event that ties
several of them together. You will meet this shape again outside this
course. If there is a clash, it is in `session_tbl`. The other tables
exist so a session can point at the right row
instead of repeating a teacher's name or a room's capacity on every row
that mentions them.

## Building it

```sql exec
id: create-timetable-tables
DROP TABLE IF EXISTS session_tbl;
DROP TABLE IF EXISTS module_tbl;
DROP TABLE IF EXISTS room_tbl;
DROP TABLE IF EXISTS teacher_tbl;
DROP TABLE IF EXISTS programme_tbl;

CREATE TABLE programme_tbl (
    programme_id INTEGER PRIMARY KEY,
    name TEXT
);

CREATE TABLE teacher_tbl (
    teacher_id INTEGER PRIMARY KEY,
    name TEXT
);

CREATE TABLE room_tbl (
    room_id INTEGER PRIMARY KEY,
    name TEXT,
    capacity INTEGER
);

CREATE TABLE module_tbl (
    module_id INTEGER PRIMARY KEY,
    programme_id INTEGER,
    name TEXT,
    FOREIGN KEY (programme_id) REFERENCES programme_tbl(programme_id)
);

CREATE TABLE session_tbl (
    session_id INTEGER PRIMARY KEY,
    module_id INTEGER,
    teacher_id INTEGER,
    room_id INTEGER,
    session_date TEXT,
    start_time TEXT,
    end_time TEXT,
    FOREIGN KEY (module_id) REFERENCES module_tbl(module_id),
    FOREIGN KEY (teacher_id) REFERENCES teacher_tbl(teacher_id),
    FOREIGN KEY (room_id) REFERENCES room_tbl(room_id)
);

INSERT INTO programme_tbl (name) VALUES
    ('Software Development'),
    ('Business Studies'),
    ('Culinary Arts');

INSERT INTO teacher_tbl (name) VALUES
    ('Aoife Byrne'),
    ('Cian Doyle'),
    ('Fatima Khan'),
    ('Liam O''Sullivan'),
    ('Priya Nair');

INSERT INTO room_tbl (name, capacity) VALUES
    ('Room 101', 25),
    ('Room 204', 20),
    ('IT Lab 1', 18),
    ('Kitchen 2', 12);

INSERT INTO module_tbl (programme_id, name) VALUES
    (1, 'Database Methods'),
    (1, 'Web Authoring'),
    (2, 'Bookkeeping'),
    (2, 'Marketing Fundamentals'),
    (3, 'Kitchen Skills'),
    (3, 'Food Safety');

INSERT INTO session_tbl (module_id, teacher_id, room_id, session_date, start_time, end_time) VALUES
    (1, 1, 3, '2026-09-14', '09:00', '11:00'),
    (2, 1, 3, '2026-09-15', '11:00', '13:00'),
    (1, 1, 3, '2026-09-16', '09:00', '11:00'),
    (2, 1, 3, '2026-09-17', '11:00', '13:00'),
    (3, 2, 2, '2026-09-14', '10:00', '12:00'),
    (4, 3, 2, '2026-09-14', '11:00', '13:00'),
    (3, 2, 2, '2026-09-16', '13:00', '15:00'),
    (4, 3, 1, '2026-09-15', '09:00', '11:00'),
    (4, 3, 1, '2026-09-17', '09:00', '11:00'),
    (5, 4, 4, '2026-09-15', '13:00', '15:00'),
    (5, 4, 4, '2026-09-18', '09:00', '11:00'),
    (6, 5, 4, '2026-09-14', '09:00', '11:00'),
    (6, 5, 4, '2026-09-16', '13:00', '15:00'),
    (3, 1, 1, '2026-09-14', '10:00', '12:00');

SELECT COUNT(*) AS session_count FROM session_tbl;
```

The box adds fourteen sessions, across three programmes' worth of
modules, five teachers and four rooms, over one working week, from
Monday 2026-09-14 to Friday 2026-09-18. `start_time` and `end_time` are
stored as text, the same way a clock shows them, such as `'09:00'` and
`'13:00'`, with a leading zero on any hour before ten. Written
consistently like
that, ordinary text comparison already puts them in the right order:
`'09:00' < '11:00'` is true, the same way it would be for numbers. The
rest of this page relies on this.

The five `DROP TABLE IF EXISTS` lines at the top delete any tables from
an earlier run, so the box builds the whole database from
nothing each time you run it. They go in the opposite order to the
`CREATE TABLE`s. `session_tbl` goes first, because its rows point into
three of the other tables, and `programme_tbl` goes last. Some databases
will not delete a table while another table still points into it.

The line for `Liam O''Sullivan` is worth a second look: two single
quotes in a row, inside a name that already has one. SQL uses a doubled
single quote to mean one quote inside a string. An apostrophe in a name
causes the same problem in most languages that quote strings with `'`.

## Asking it real questions

A single `session_tbl` row is not very readable on its own. It is mostly
numbers pointing at other tables. A join of all five tables turns those
numbers back into names.

```sql exec
id: everyones-full-timetable
SELECT
    teacher_tbl.name AS teacher,
    module_tbl.name AS module,
    room_tbl.name AS room,
    session_tbl.session_date AS date,
    session_tbl.start_time AS starts,
    session_tbl.end_time AS ends
FROM session_tbl
JOIN module_tbl ON session_tbl.module_id = module_tbl.module_id
JOIN teacher_tbl ON session_tbl.teacher_id = teacher_tbl.teacher_id
JOIN room_tbl ON session_tbl.room_id = room_tbl.room_id
ORDER BY session_tbl.session_date, session_tbl.start_time;
```

The query has three `JOIN`s, one for each table `session_tbl` points at.
[A second table and a join](tutorial:a-second-table-and-a-join) used the
same idea with two tables. Here it joins four. A `WHERE` narrows this to
one
person's own week:

```sql exec
id: one-teachers-timetable
SELECT
    module_tbl.name AS module,
    room_tbl.name AS room,
    session_tbl.session_date AS date,
    session_tbl.start_time AS starts,
    session_tbl.end_time AS ends
FROM session_tbl
JOIN module_tbl ON session_tbl.module_id = module_tbl.module_id
JOIN teacher_tbl ON session_tbl.teacher_id = teacher_tbl.teacher_id
JOIN room_tbl ON session_tbl.room_id = room_tbl.room_id
WHERE teacher_tbl.name = 'Aoife Byrne'
ORDER BY session_tbl.session_date, session_tbl.start_time;
```

Aoife Byrne has five rows. Two of them share a date, 2026-09-14:
Database Methods in IT Lab 1 from 09:00 to 11:00, and Bookkeeping in
Room 101 from 10:00 to 12:00. Read those two rows again, side by side.
Something about them looks wrong. The next sections find it.

## Finding a clash

Two sessions clash when they share a room (or a teacher) and their
times overlap. "Overlap" needs a precise test, because two sessions back
to back, one ending at 11:00 and the next starting at 11:00, are not a
clash. They only overlap if each one starts before the other
ends.

Try that rule on paper first, with two made-up sessions:

- Session A runs 10:00 to 12:00. Session B runs 11:00 to 13:00. Does A
  start before B ends? 10:00 is before 13:00, so yes. Does B start before
  A ends? 11:00 is before 12:00, so yes. Both hold, so they overlap,
  between 11:00 and 12:00.
- Session A runs 09:00 to 11:00. Session C runs 11:00 to 13:00. Does A
  start before C ends? 09:00 is before 13:00, so yes. Does C start before
  A ends? No, because 11:00 is not before itself. One
  condition fails, so A and C do not overlap. They are back to back.

That second check stops a normal, fully booked day from being reported
as one long clash.

In SQL, we compare a `session_tbl` row against every other `session_tbl`
row. The same table is joined to itself. A *self-join*
gives each side of the comparison its own name, so `WHERE` can tell them
apart:

```sql exec
id: find-room-clashes
SELECT
    s1.session_id AS session_a,
    s2.session_id AS session_b,
    room_tbl.name AS room,
    s1.session_date AS date,
    s1.start_time AS a_starts,
    s1.end_time AS a_ends,
    s2.start_time AS b_starts,
    s2.end_time AS b_ends
FROM session_tbl AS s1
JOIN session_tbl AS s2
    ON s1.room_id = s2.room_id
    AND s1.session_date = s2.session_date
    AND s1.session_id < s2.session_id
JOIN room_tbl ON room_tbl.room_id = s1.room_id
WHERE s1.start_time < s2.end_time
  AND s2.start_time < s1.end_time;
```

`session_tbl AS s1` and `session_tbl AS s2` are the same table, given two
different names so a row can be compared against another row from the
very table it came from. `s1.room_id = s2.room_id AND s1.session_date =
s2.session_date` narrows the comparison to sessions that could clash, in
the same room on the same date, before the overlap test runs.
`s1.session_id < s2.session_id` rules out comparing a row with itself (which would
trivially "overlap" its own time) and stops each real pair from being
reported twice, once each way round. The last two lines are the rule we
tested on paper above.

One row comes back: the two Room 204 sessions from 2026-09-14,
overlapping between 11:00 and 12:00. Aoife Byrne's own two sessions on
that same date are not in this result. This query only checks rooms so
far, and her two sessions are in different rooms.

## The same idea, for a teacher

A teacher booked into two sessions at once is the same problem, with
`teacher_id` in place of `room_id`. Try writing that query yourself
before opening the fold below. Everything it needs is in the query
above, with one join and one column changed.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Start from `find-room-clashes` and copy its whole shape: the two
   `session_tbl AS s1`/`s2` aliases, the `s1.session_id < s2.session_id`
   line, and both
   `start_time`/`end_time` comparisons unchanged.
2. `ON s1.room_id = s2.room_id` becomes `ON s1.teacher_id =
   s2.teacher_id`. A teacher clash means the same teacher, not the
   same room.
3. `JOIN room_tbl ON room_tbl.room_id = s1.room_id` becomes a join to
   `teacher_tbl` instead, so the result can show a name rather than a
   `teacher_id`.

**Think about:** why does `s1.session_date = s2.session_date` still
belong in the `ON` clause, even though nothing about it changed?

**Try this next:** a version that finds a teacher double-booked, *or* a
room double-booked, in one query. `OR` between the two `ON` conditions
gets partway there. What would need to change about the columns the
query selects, once a room clash and a teacher clash can both appear in
the same row?

</details>

<details class="dl-answer"><summary>answer</summary>

```sql
SELECT
    s1.session_id AS session_a,
    s2.session_id AS session_b,
    teacher_tbl.name AS teacher,
    s1.session_date AS date,
    s1.start_time AS a_starts,
    s1.end_time AS a_ends,
    s2.start_time AS b_starts,
    s2.end_time AS b_ends
FROM session_tbl AS s1
JOIN session_tbl AS s2
    ON s1.teacher_id = s2.teacher_id
    AND s1.session_date = s2.session_date
    AND s1.session_id < s2.session_id
JOIN teacher_tbl ON teacher_tbl.teacher_id = s1.teacher_id
WHERE s1.start_time < s2.end_time
  AND s2.start_time < s1.end_time;
```

Run against the data on this page, one row comes back: Aoife Byrne,
2026-09-14, one session from 09:00 to 11:00 and the cover session added
later at 10:00 to 12:00. `one-teachers-timetable` already showed the two
rows of this clash.

</details>

```sql exec
id: find-teacher-clashes
-- Write your own version of the teacher-clash query here, then run it.
-- The hint above walks through adapting find-room-clashes, and the
-- answer fold has a full worked version if you want to check your own.
```

## Your turn

Scroll back up to `create-timetable-tables` and add one more row to
`session_tbl`: a module, teacher, room, date and time of your own
choosing, using the keys already in `module_tbl`, `teacher_tbl` and
`room_tbl`. Run that box
again to rebuild the whole database with your row included.

Then run `find-room-clashes` and `find-teacher-clashes` again. If either
one now returns a row it did not before, your new session clashes with
something already on the timetable. Change its room, or its time, and
run both boxes again until neither reports it. If neither query changes
at all, you picked a free slot on the first try. To check, choose a room
and time you can already see is busy in `everyones-full-timetable`, and
see whether the clash queries catch it.

## What you have now

- **A five-table design for one real problem.** Four tables describe
  things (`programme_tbl`, `teacher_tbl`, `room_tbl`, `module_tbl`), and
  one describes an event that ties several of them together
  (`session_tbl`). You will see this shape outside this course too.
- **A real date sorts correctly. A weekday name does not.** `'Friday'`
  comes before `'Monday'` as plain text. `'2026-09-18'` comes after
  `'2026-09-14'`, both as text and on a calendar.
- **Self-join.** A self-join joins a table to itself, under two
  different names, to compare one of its rows against another.
- **The overlap test.** Two time ranges overlap only if each one starts
  before the other ends. Both conditions must be true, not just one.
- **`s1.session_id < s2.session_id`.** This line stops a self-join from
  matching a row with itself, and from reporting the same pair
  twice.

## Where to read more

Stand-up Maths (2018). *How many calendars are there?*
<https://www.youtube.com/watch?v=mrgN-tvg53I>. Every year's calendar is
one of only a few possible layouts, set by the day of the week it starts
on and whether it is a leap year. Matt Parker counts them. About eleven
minutes.
