---
title: "Many languages, one idea"
year: "2026-2027"
version: 2026.09.24.1
covers:
  one-job-in-python:
    covers: [PDP-LO3]
    touches: [MIT-5.12, PDP-LO6]
  the-same-job-in-sql:
    covers: [PDP-LO3]
    touches: [MIT-5.12]
  the-same-job-in-javascript:
    covers: [PDP-LO3]
    touches: [PDP-LO9]
  the-same-job-in-basic:
    covers: [PDP-LO3]
  what-changes-from-one-language-to-the-next:
    covers: [PDP-LO3]
  what-stays-the-same-the-four-questions:
    covers: [PDP-LO3]
    touches: [PDP-LO5]
---

# Many languages, one idea

Three people you might meet write code at work. One builds web pages in
JavaScript. One asks a company's database questions in SQL. One
remembers typing BASIC into a home computer in the 1980s. Are they
doing the same thing you do in Python, or something quite different?
Let's give all four languages the same small job, and find out.

On this page we:

- give one job to Python: the average rainfall of a week, and the days
  above it
- give the same job to SQL, and run it on this page
- read the same job in JavaScript and in BASIC
- sort out what changes from one language to the next: syntax, types,
  how a program is run, and where it runs
- see what stays the same: the four questions

> **The space we're in.** Python and SQL cells run here, in your
> browser. The SQL cells use a small database that lives inside this
> page and starts empty each time the page loads. JavaScript and BASIC
> are shown to read, not to run. One thing usually goes unsaid: a
> programming language is a set of agreements between people and a
> machine, and different people made different agreements.

## Warm-up

The first question is from
[Where programming came from](tutorial:where-programming-came-from#basic-a-language-for-beginners),
and the second from
[What is typical?](tutorial:what-is-typical#share-it-out-equally-the-mean)

```question
id: many-lang-warm-up-1
type: fill-in-the-blank

BASIC was made at Dartmouth College in 1964 so that
{beginners|scientists|banks} could write programs.
```

```question
id: many-lang-warm-up-2
type: multiple-choice
correct: 2

What is the mean of 2, 4 and 9?

- 4
- 5
- 9
- 15
```

## One job in Python

Here is a week of rainfall, in millimetres, for a town in the west of
Ireland. The numbers are made up, to keep the sums tidy. The job has
two parts: find the average, then count the days that were wetter than
the average.

Before any code, let's ask the four questions of the job itself. What is
named? Seven readings, and an average. What is promised? The average is
the sum shared out equally over the days. What happens when? We must
add up before we divide, and we must know the average before we can
compare a day with it. What does the space let us do? Numbers with
decimals, and a way to go through them one at a time.

Guess the average before you run the cell. Will it be closer to 0 or to
12.6?

```python exec
id: many-lang-python
rainfall_mm = [4.2, 0.0, 12.6, 7.1, 0.8, 3.3, 7.0]

running_sum = 0
for reading in rainfall_mm:
    running_sum = running_sum + reading
average = running_sum / len(rainfall_mm)
print("average:", average)

wet_days = 0
for reading in rainfall_mm:
    if reading > average:
        wet_days = wet_days + 1
print("days above it:", wet_days)

print("with the toolkit:", mean(rainfall_mm))
```

The average is 5.0 mm, and three days were above it: 12.6, 7.1 and 7.0.
Your toolkit's `mean` from
[What is typical?](tutorial:what-is-typical#share-it-out-equally-the-mean)
agrees. Keep this cell in mind. Every version below does these same
steps, or asks for these same answers.

## The same job in SQL

*SQL* is a language for asking a database questions. It grew out of
SEQUEL, a language that Donald Chamberlin and Raymond Boyce described
at IBM in 1974. A database keeps its data in tables, so first we make a
table, with one row for each day. Run this cell. It reports how many
rows it added.

```sql exec
id: many-lang-sql-table
DROP TABLE IF EXISTS rain_tbl;
CREATE TABLE rain_tbl (
    rain_id INTEGER PRIMARY KEY,
    day TEXT,
    rainfall_mm REAL
);
INSERT INTO rain_tbl (day, rainfall_mm) VALUES
    ('Mon', 4.2), ('Tue', 0.0), ('Wed', 12.6), ('Thu', 7.1),
    ('Fri', 0.8), ('Sat', 3.3), ('Sun', 7.0);
```

The first line removes the table if it is already there, so the cell
can run twice without an error. Notice `REAL` and `TEXT`: each column
is given a type when the table is made. Most databases hold every value
to its column's type. SQLite, the database on this page, is more relaxed
about it.

Now the average. How many lines of SQL do you think it will take?

```sql exec
id: many-lang-sql-average
SELECT AVG(rainfall_mm) FROM rain_tbl;
```

One line, and no loop. `AVG` is a function that SQL gives us, the way
Python gives us `len`. Now the second part: the days above the average.

```sql exec
id: many-lang-sql-above
SELECT COUNT(*) FROM rain_tbl
WHERE rainfall_mm > (SELECT AVG(rainfall_mm) FROM rain_tbl);
```

The answer is 3 again. The query in brackets runs first and gives 5.0.
Then the outer query counts the rows whose rainfall is bigger than that.

SQL is *declarative*: a program says what result it wants, and the
database decides the steps. Python is step by step: the program says
each step, in order. In SQL we never wrote "start at 0, add each
reading". Somewhere inside the database a loop still runs, but it is
the database's loop, not ours.

### Your turn

1. Change `COUNT(*)` to `day` in the last cell. Which three days come
   back?
2. Write a query that finds the wettest reading, with `MAX(rainfall_mm)`
   in place of `AVG(rainfall_mm)`.

## The same job in JavaScript

JavaScript is the language that web browsers run, as we saw on
[the last page](tutorial:where-programming-came-from#the-web-javascript-and-python). Here is the same job. It is to read, not to run, so read it
slowly beside the Python cell. Which parts can you match up?

```js
const rainfallMm = [4.2, 0.0, 12.6, 7.1, 0.8, 3.3, 7.0];

let runningSum = 0;
for (const reading of rainfallMm) {
  runningSum = runningSum + reading;
}
const average = runningSum / rainfallMm.length;
console.log("average:", average);

let wetDays = 0;
for (const reading of rainfallMm) {
  if (reading > average) {
    wetDays = wetDays + 1;
  }
}
console.log("days above it:", wetDays);
```

Almost every line has a partner in the Python. The differences are in
the syntax, the grammar a language's code must follow (we met the
word on
[When Python says no](tutorial:when-python-says-no#mistakes-python-finds-before-it-starts)):

- Curly brackets `{ }` mark where a loop or an `if` starts and stops.
  Python uses indentation for the same job.
- A new name starts with `let` or `const`. `const` promises that the
  name will never point at anything else.
- Names are written `rainfallMm`, with a capital in the middle, where
  Python programmers write `rainfall_mm`. This is a habit of each
  language's programmers, not a rule of either language.
- `.length` does the job of `len`, and `console.log` does the job of
  `print`.

Run in a browser, this prints `average: 5`, not `5.0`. JavaScript uses
one type of number for both whole numbers and decimals, so it has no
reason to show the `.0`.

### Two ways to answer "5" + 1

The bigger differences hide in what a language allows. In JavaScript,
`"5" + 1` gives `"51"`: a piece of text, 5 and 1 joined. What do you
expect Python to do with the same line? This cell raises an error on
purpose.

```python exec
id: many-lang-text-plus-number
print("5" + 1)
```

Python stops with a `TypeError`, as on
[When Python says no](tutorial:when-python-says-no#the-last-line-first).
It will not guess whether you meant a number or a piece of text.
JavaScript guesses, and it chooses text. Neither is foolish. They are
two spaces with different rules. JavaScript's rule lets a page join
text and numbers with no extra step, but it can hide a mistake: you may
have wanted 6. Python's rule costs an extra step, `int("5") + 1`, and
it catches the mistake on the line where it happens.

## The same job in BASIC

BASIC is the language from 1964 that was later built into home
computers, as on
[the last page](tutorial:where-programming-came-from#basic-a-language-for-beginners). Here is the same job, in the style of the 1980s. Again, it
is to read, not to run:

```basic
10 REM A WET WEEK: THE AVERAGE, AND DAYS ABOVE IT
20 DIM R(7)
30 LET T = 0
40 FOR I = 1 TO 7
50 READ R(I)
60 LET T = T + R(I)
70 NEXT I
80 LET A = T / 7
90 PRINT "AVERAGE"; A
100 LET C = 0
110 FOR I = 1 TO 7
120 IF R(I) > A THEN LET C = C + 1
130 NEXT I
140 PRINT "DAYS ABOVE IT"; C
150 DATA 4.2, 0, 12.6, 7.1, 0.8, 3.3, 7
160 END
```

It prints `AVERAGE 5` and `DAYS ABOVE IT 3`. Every line has a number,
and the numbers set the order. `REM` starts a comment, like `#` in
Python. `DIM R(7)` makes room for seven numbers, like a list. The
readings sit in a `DATA` line at the end, and `READ` takes them one at a
time.

The names are single letters, and that was not only a habit. On the
Commodore 64, only the first two letters of a name counted, so
`RAINFALL` and `RAINY` would have been the same name. Programmers kept
names short because the machine could not tell long ones apart. In
most home-computer BASICs, a name that ends in `$`, such as `N$`, holds
text. There, the name itself says the type.

## What changes from one language to the next

A computer's hardware runs only its own machine instructions, so every
language needs a program that translates or carries out its code. You
met the compiler, which translates a whole program first, on
[When Python says no](tutorial:when-python-says-no#compilers-linkers-and-python).
An *interpreter* is a program that reads another program and carries out
its instructions as it goes. Is a language compiled or interpreted? That
is really a question about the tool, not the language. The first BASIC
at Dartmouth was compiled, but the BASICs built into home computers such
as the Spectrum and the Commodore 64 were interpreters. Python first compiles your cell into simpler instructions,
then interprets those. Chrome's JavaScript engine, for example, starts
a program with an interpreter, and compiles the parts that run most
often into machine instructions while the page is running.

Here are the differences we found, side by side:

| | Python | SQL | JavaScript | BASIC, 1980s |
|---|---|---|---|---|
| **Syntax** | indentation marks a block | one statement, in clauses like `SELECT` and `WHERE` | `{ }` marks a block | line numbers set the order |
| **Types** | a value carries its type; `"5" + 1` is an error | each column's type is given when the table is made | a value carries its type; `"5" + 1` becomes text | a name ending in `$` holds text |
| **How it runs** | compiled to simpler instructions, then interpreted | the database plans the steps itself | interpreted, and compiled while it runs | interpreted, line by line |
| **Where it runs** | on almost any computer, and here in your browser | inside a database | in every web browser | built into a home computer |
| **Style** | step by step | declarative | step by step | step by step |
| **Made for** | readable, general programs | questions about tables of data | making web pages do things | beginners |

These rows are what people mean by the *characteristics* of a
programming language: its syntax, how it treats types, how it is
translated and run, where it runs, whether it is step by step or
declarative, and what it was made for. Two languages can differ in one
row and agree in the next. JavaScript looks different from Python on
the page, but it runs in much the same step-by-step way.

```question
id: many-lang-characteristics
type: multiple-choice
correct: 3

A friend says, "BASIC is an interpreted language." What is the most
careful reply?

- Yes, every BASIC is interpreted.
- No, BASIC is always compiled.
- The home-computer BASICs were interpreted, but the first one at
  Dartmouth was compiled: it depends on the tool.
- BASIC is not a real programming language.
```

## What stays the same: the four questions

Now let's ask the four questions of all four programs at once.

| The question | Python | SQL | JavaScript | BASIC |
|---|---|---|---|---|
| What is named here? | `rainfall_mm`, `average` | `rain_tbl`, `rainfall_mm` | `rainfallMm`, `average` | `R`, `A` |
| What is promised? | `mean` shares the sum out | `AVG` shares the sum out | the same sum, divided by `.length` | `T / 7` |
| What happens when? | add, then divide, then compare | the query in brackets first, then the count | add, then divide, then compare | the order of the line numbers |
| What does this space let us do? | `len`, lists, a `TypeError` | tables, `AVG`, `COUNT` | `console.log`, joining text to numbers | `DATA`, `READ`, two-letter names |

The answers change from column to column, and the questions never do.
That is the idea in this page's title. Every language names things,
keeps promises, puts steps in an order, and works inside a space with
its own rules. A programmer who asks the four questions can start to
read a language they have never seen before.

### Your turn

1. Look back at the JavaScript. Find one line whose job is naming, one
   whose job is a promise, and one where the order matters.
2. In the BASIC program, what would go wrong if line 80 came before line
   40? Which question is that?

<details class="dl-why"><summary>Why this way?</summary>

This page gave one small job to four languages and compared the
results. Another way is a tour: one page for each language, each with
its own history and its own features.

A tour goes deeper into each language. It shows what each one is best
at, such as SQL joining tables, and a reader who wants to work in
JavaScript would learn more of it.

We chose one job because a comparison needs something to hold still.
With the job fixed, every difference you saw belonged to the languages,
not to the task. The cost is that the job was small. It did not show
what makes each language worth learning for its own sake.

</details>

## Four questions, looking back

| The question | On this page |
|---|---|
| What is named here? | the same week of rain, named four ways; a table's columns; two-letter names on the Commodore 64 |
| What is promised? | the average as the sum shared out, kept by `mean`, `AVG` and a loop; a query that says what, not how |
| What happens when? | add before dividing; the query in brackets before the outer query; line numbers in BASIC |
| What does this space let us do? | JavaScript joins `"5"` and `1`; Python refuses; SQL gives `AVG` for free; each language gives its own tools |

## What we have now

| Term or tool | What it means |
|---|---|
| SQL | a declarative language for asking a database questions |
| `AVG(column)`, `COUNT(*)` | SQL's average of a column, and its count of rows |
| a query in brackets | a query inside a query; it runs first, and the outer query uses its answer |
| declarative | a style where a program says what result it wants, not the steps to get it |
| interpreter | a program that reads another program and carries out its instructions as it goes |
| characteristics of a language | its syntax, its types, how it runs, where it runs, its style, and what it was made for |
| `"5" + 1` | an error in Python; the text `"51"` in JavaScript |

## Where to read more

The Database Methods course teaches SQL properly. Its first SQL page is
[Tables in SQL: CREATE TABLE, INSERT and SELECT](tutorial:a-table-is-a-list-of-rows).

[How programming languages came to be](tutorial:how-we-got-here#the-same-problem-four-ways)
has another comparison, of a different kind: one job done four ways in
Python, each in a different style of programming.
