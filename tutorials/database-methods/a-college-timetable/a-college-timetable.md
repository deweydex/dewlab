---
title: "A College Timetable"
slug: a-college-timetable
module: database-methods
module_title: "Database Methods"
year: "2026-2027"
series: several-tables
version: 2026.09.12.1
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

# A College Timetable

A further education college runs on a timetable: which room, which
teacher, which module, on which date, between which two times. Every
earlier page in this series built a database with one or two tables. A
timetable needs more than that, and it needs to answer a question no
single table can: has anyone been booked into the same room, or asked to
teach in two places, at the same time.

This page designs and builds that database, then writes the query that
actually finds a clash. It is the longest page in this module on
purpose. A short example can show you the shape of a technique; a
problem this size is closer to the one a real college's admin office
actually has.

## Five tables for one timetable

Start with what the college needs to keep track of, before writing a
single `CREATE TABLE`.

A *programme* is a course a student enrols in — Software Development,
Business Studies, Culinary Arts. A programme has a name, and nothing
else worth storing about it here.

A *module* belongs to one programme. Software Development includes
Database Methods and Web Authoring; Business Studies includes
Bookkeeping and Marketing Fundamentals. A module needs its own name, and
a column pointing back at the programme it belongs to.

A *teacher* has a name. Nothing here says which module a teacher
teaches — that fact belongs somewhere else, because the same teacher
can teach more than one module, and the same module could, in principle,
be taught by more than one teacher across different groups.

A *room* has a name and a capacity: how many people can sit in it at
once.

None of the four tables above says anything about *when*. That is the
job of a fifth table, *sessions*: one row per class, naming which
module it is, which teacher is running it, which room it is in, what
date, and what time it starts and ends.

The date is worth a design decision of its own. Storing it as a weekday
name — `'Monday'`, `'Tuesday'` — reads well, but sorts alphabetically:
`'Friday'` comes before `'Monday'` as plain text, which would put the
end of the week at the top of every list this page builds. An actual
calendar date, written `'2026-09-14'`, sorts the same way whether the
computer reads it as text or as a date — the reason this page uses real
dates instead.

Four tables that describe things, and a fifth that describes an event
tying several of them together, is a shape you will meet again outside
this course. `sessions` is the table every clash lives or does not live
in — everything else exists so a session can point at the right row
instead of repeating a teacher's name or a room's capacity on every row
that mentions them.

## Building it

```sql exec
id: create-timetable-tables
CREATE TABLE programmes (
    id INTEGER PRIMARY KEY,
    name TEXT
);

CREATE TABLE teachers (
    id INTEGER PRIMARY KEY,
    name TEXT
);

CREATE TABLE rooms (
    id INTEGER PRIMARY KEY,
    name TEXT,
    capacity INTEGER
);

CREATE TABLE modules (
    id INTEGER PRIMARY KEY,
    name TEXT,
    programme_id INTEGER
);

CREATE TABLE sessions (
    id INTEGER PRIMARY KEY,
    module_id INTEGER,
    teacher_id INTEGER,
    room_id INTEGER,
    session_date TEXT,
    start_time TEXT,
    end_time TEXT
);

INSERT INTO programmes (name) VALUES
    ('Software Development'),
    ('Business Studies'),
    ('Culinary Arts');

INSERT INTO teachers (name) VALUES
    ('Aoife Byrne'),
    ('Cian Doyle'),
    ('Fatima Khan'),
    ('Liam O''Sullivan'),
    ('Priya Nair');

INSERT INTO rooms (name, capacity) VALUES
    ('Room 101', 25),
    ('Room 204', 20),
    ('IT Lab 1', 18),
    ('Kitchen 2', 12);

INSERT INTO modules (name, programme_id) VALUES
    ('Database Methods', 1),
    ('Web Authoring', 1),
    ('Bookkeeping', 2),
    ('Marketing Fundamentals', 2),
    ('Kitchen Skills', 3),
    ('Food Safety', 3);

INSERT INTO sessions (module_id, teacher_id, room_id, session_date, start_time, end_time) VALUES
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

SELECT COUNT(*) AS session_count FROM sessions;
```

Fourteen sessions, across five programmes' worth of modules, five
teachers and four rooms, running over one working week, Monday
2026-09-14 to Friday 2026-09-18. `start_time` and `end_time` are stored
as text, written the same way a clock shows them — `'09:00'`, `'13:00'`
— with a leading zero on any hour before ten. Written consistently like
that, ordinary text comparison already puts them in the right order:
`'09:00' < '11:00'` is true, the same way it would be for numbers. That
is what the rest of this page relies on.

The line for `Liam O''Sullivan` is worth a second look: two single
quotes in a row, inside a name that already has one. SQL uses a doubled
single quote to mean one literal quote inside a string — the same
problem an apostrophe in a name causes in most languages that quote
strings with `'`.

## Asking it real questions

A single `sessions` row is not very readable on its own — it is mostly
numbers pointing at other tables. Joining all five tables together turns
those numbers back into names.

```sql exec
id: everyones-full-timetable
SELECT
    teachers.name AS teacher,
    modules.name AS module,
    rooms.name AS room,
    sessions.session_date AS date,
    sessions.start_time AS starts,
    sessions.end_time AS ends
FROM sessions
JOIN modules ON sessions.module_id = modules.id
JOIN teachers ON sessions.teacher_id = teachers.id
JOIN rooms ON sessions.room_id = rooms.id
ORDER BY sessions.session_date, sessions.start_time;
```

Three `JOIN`s, one for each table `sessions` points at — the same idea
[a second table and a join](tutorial:a-second-table-and-a-join) covered
with two tables, extended to four. A `WHERE` narrows this to one
person's own week:

```sql exec
id: one-teachers-timetable
SELECT
    modules.name AS module,
    rooms.name AS room,
    sessions.session_date AS date,
    sessions.start_time AS starts,
    sessions.end_time AS ends
FROM sessions
JOIN modules ON sessions.module_id = modules.id
JOIN teachers ON sessions.teacher_id = teachers.id
JOIN rooms ON sessions.room_id = rooms.id
WHERE teachers.name = 'Aoife Byrne'
ORDER BY sessions.session_date, sessions.start_time;
```

Five rows for Aoife Byrne. Two of them share a date, 2026-09-14 —
Database Methods in IT Lab 1 from 09:00 to 11:00, and Bookkeeping in
Room 101 from 10:00 to 12:00. Read those two rows again, side by side.
Something about them does not add up — the next section is what
actually catches it.

## Finding a clash

Two sessions clash when they share a room (or a teacher) and their
times overlap. "Overlap" needs a precise test, because two sessions
back to back — one ending at 11:00, the next starting at 11:00 — are
not a clash. They only overlap if each one starts before the other
ends.

Try that rule on paper first, with two made-up sessions:

- Session A runs 10:00 to 12:00. Session B runs 11:00 to 13:00. Does A
  start before B ends? 10:00 is before 13:00 — yes. Does B start before
  A ends? 11:00 is before 12:00 — yes. Both hold, so they overlap,
  between 11:00 and 12:00.
- Session A runs 09:00 to 11:00. Session C runs 11:00 to 13:00. Does A
  start before C ends? 09:00 is before 13:00 — yes. Does C start before
  A ends? 11:00 is before 11:00 — no, 11:00 is not before itself. One
  condition fails, so A and C do not overlap. They are back to back.

That second check is the one that keeps a normal, fully booked day from
being reported as one long clash.

Turning that into SQL means comparing a `sessions` row against every
other `sessions` row — the same table, joined to itself. A *self-join*
gives each side of the comparison its own name, so `WHERE` can tell them
apart:

```sql exec
id: find-room-clashes
SELECT
    s1.id AS session_a,
    s2.id AS session_b,
    rooms.name AS room,
    s1.session_date AS date,
    s1.start_time AS a_starts,
    s1.end_time AS a_ends,
    s2.start_time AS b_starts,
    s2.end_time AS b_ends
FROM sessions AS s1
JOIN sessions AS s2
    ON s1.room_id = s2.room_id
    AND s1.session_date = s2.session_date
    AND s1.id < s2.id
JOIN rooms ON rooms.id = s1.room_id
WHERE s1.start_time < s2.end_time
  AND s2.start_time < s1.end_time;
```

`sessions AS s1` and `sessions AS s2` are the same table, given two
different names so a row can be compared against another row from the
very table it came from. `s1.room_id = s2.room_id AND s1.session_date =
s2.session_date` narrows the comparison to sessions that could possibly
clash — same room, same date — before the overlap test even runs.
`s1.id < s2.id` rules out comparing a row with itself (which would
trivially "overlap" its own time) and stops each real pair from being
reported twice, once each way round. The last two lines are exactly the
rule worked out on paper above.

One row comes back: the two Room 204 sessions from 2026-09-14,
overlapping between 11:00 and 12:00. Aoife Byrne's own two sessions on
that same date are not in this result — this query only checks rooms so
far, and her two sessions are in different rooms.

## The same idea, for a teacher

A teacher booked into two sessions at once is the same problem, with
`teacher_id` in place of `room_id`. Try writing that query yourself
before opening the fold below — everything it needs is in the query
above, with one join and one column changed.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Start from `find-room-clashes` and copy its whole shape: the two
   `sessions AS s1`/`s2` aliases, the `s1.id < s2.id` line, and both
   `start_time`/`end_time` comparisons unchanged.
2. `ON s1.room_id = s2.room_id` becomes `ON s1.teacher_id =
   s2.teacher_id` — a teacher clash means the same teacher, not the
   same room.
3. `JOIN rooms ON rooms.id = s1.room_id` becomes a join to `teachers`
   instead, so the result can show a name rather than an id.

**Think about:** why `s1.session_date = s2.session_date` still belongs
in the `ON` clause even though nothing else changed about it.

**Try this next:** a version that finds a teacher double-booked, *or* a
room double-booked, in one query. `OR` between the two `ON` conditions
gets partway there — what would need to change about the columns the
query selects, once a room clash and a teacher clash can both appear in
the same row?

</details>

<details class="dl-answer"><summary>answer</summary>

```sql
SELECT
    s1.id AS session_a,
    s2.id AS session_b,
    teachers.name AS teacher,
    s1.session_date AS date,
    s1.start_time AS a_starts,
    s1.end_time AS a_ends,
    s2.start_time AS b_starts,
    s2.end_time AS b_ends
FROM sessions AS s1
JOIN sessions AS s2
    ON s1.teacher_id = s2.teacher_id
    AND s1.session_date = s2.session_date
    AND s1.id < s2.id
JOIN teachers ON teachers.id = s1.teacher_id
WHERE s1.start_time < s2.end_time
  AND s2.start_time < s1.end_time;
```

Run against the data on this page, one row comes back: Aoife Byrne,
2026-09-14, one session from 09:00 to 11:00 and the cover session added
later at 10:00 to 12:00 — the same clash `one-teachers-timetable`
already showed the raw ingredients of.

</details>

```sql exec
id: find-teacher-clashes
-- Write your own version of the teacher-clash query here, then run it.
-- The hint above walks through adapting find-room-clashes, and the
-- answer fold has a full worked version if you want to check your own.
```

## Your turn

Scroll back up to `create-timetable-tables` and add one more row to
`sessions`: a module, teacher, room, date and time of your own choosing,
using the ids already in `modules`, `teachers` and `rooms`. Run that box
again to rebuild the whole database with your row included.

Then run `find-room-clashes` and `find-teacher-clashes` again. If either
one now returns a row it did not before, your new session clashes with
something already on the timetable. Change its room, or its time, and
run both boxes again until neither reports it. If neither query changes
at all, you picked a genuinely free slot on the first try — check by
choosing a room and time you can already see is busy in
`everyones-full-timetable`, and confirm the clash queries actually catch
it.

## What you have now

- **A five-table design for one real problem.** Four tables describing
  things (`programmes`, `teachers`, `rooms`, `modules`) and one
  describing an event that ties several of them together
  (`sessions`) — a shape worth recognising outside this course, not
  just inside it.
- **A real date sorts correctly; a weekday name does not.** `'Friday'`
  comes before `'Monday'` as plain text. `'2026-09-18'` comes after
  `'2026-09-14'`, both as text and on a calendar.
- **Self-join.** Joining a table to itself, under two different names,
  to compare one of its rows against another.
- **The overlap test.** Two time ranges overlap only if each one starts
  before the other ends — both conditions, not just one.
- **`s1.id < s2.id`.** The line that keeps a self-join from matching a
  row with itself, and from reporting the same pair twice.
