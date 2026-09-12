---
title: "SQL practice"
slug: sql-practice
module: data
module_title: "Data"
series: practice
version: 2026.09.05.1
---

# SQL practice

Five short exercises, against a shared table of students and a shared
table of courses. None of this is graded; the hints and the solutions
at the bottom are there to use freely. Getting one wrong and reading why
is worth more than skipping the hint to avoid it.

Run this first, to build both tables.

```sql cell=practice
CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER,
    grade INTEGER
);

CREATE TABLE courses (
    id INTEGER PRIMARY KEY,
    name TEXT,
    instructor TEXT,
    credits INTEGER
);

INSERT INTO students (name, age, grade) VALUES
    ('Alice Johnson', 20, 88),
    ('Bob Smith', 19, 92),
    ('Carol Williams', 21, 76),
    ('David Brown', 20, 85),
    ('Eve Davis', 22, 91),
    ('Frank Miller', 19, 73),
    ('Grace Wilson', 21, 89),
    ('Henry Moore', 20, 94);

INSERT INTO courses (name, instructor, credits) VALUES
    ('Introduction to Programming', 'Dr. Smith', 4),
    ('Data Structures', 'Prof. Johnson', 3),
    ('Web Development', 'Dr. Lee', 3),
    ('Database Systems', 'Prof. Garcia', 4),
    ('Computer Networks', 'Dr. Martinez', 3);
```

## Exercise 1: naming columns

Try selecting only the `name` and `age` columns from `students`.

```sql cell=practice
-- Write your query here.
```

<details class="dl-hint"><summary>hint</summary>

Name the columns you want, separated by commas, in place of `*`.

</details>

## Exercise 2: WHERE

Try finding every student whose `grade` is less than 75.

```sql cell=practice
-- Write your query here.
```

<details class="dl-hint"><summary>hint</summary>

`WHERE grade < 75` goes after the table's name.

</details>

## Exercise 3: INSERT

Try adding yourself to `students`, with any age and grade you like.

```sql cell=practice
-- Write your query here.
```

<details class="dl-hint"><summary>hint</summary>

`INSERT INTO students (name, age, grade) VALUES ('Your Name', 20, 85);`

</details>

## Exercise 4: ORDER BY

Try showing every student, sorted by `name` in alphabetical order.

```sql cell=practice
-- Write your query here.
```

<details class="dl-hint"><summary>hint</summary>

`ORDER BY name ASC` sorts alphabetically; leaving `ASC` out does the
same thing.

</details>

## Exercise 5: COUNT

How many courses are in `courses`? Try writing a query that counts them.

```sql cell=practice
-- Write your query here.
```

<details class="dl-hint"><summary>hint</summary>

`SELECT COUNT(*) FROM courses;` counts every row.

</details>

## Solutions

<details class="dl-answer"><summary>exercise 1</summary>

```sql
SELECT name, age FROM students;
```

</details>

<details class="dl-answer"><summary>exercise 2</summary>

```sql
SELECT * FROM students WHERE grade < 75;
```

Carol Williams and Frank Miller are the two rows this matches, with the
seed data above.

</details>

<details class="dl-answer"><summary>exercise 3</summary>

```sql
INSERT INTO students (name, age, grade) VALUES ('Your Name', 20, 85);
```

Any name, age and grade work; `SELECT * FROM students;` afterward shows
your new row at the end.

</details>

<details class="dl-answer"><summary>exercise 4</summary>

```sql
SELECT * FROM students ORDER BY name ASC;
```

</details>

<details class="dl-answer"><summary>exercise 5</summary>

```sql
SELECT COUNT(*) FROM courses;
```

Five, with the seed data above.

</details>
