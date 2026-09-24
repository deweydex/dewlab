---
title: "Many languages, one idea — Practice"
practice_for: many-languages-one-idea
year: "2026-2027"
version: 2026.09.24.1
---

# Many languages, one idea — Practice

Each problem says what kind it is. **Predict** means guess first, then
run. **Make** means write something new. **Fix** means find one mistake
in code that looks fine. **Explain** means answer in words. **Another
way** means reach the same place by a second route. The answers are
folded away until you open them.

Python and SQL cells run on this page. JavaScript, BASIC and one other
language are shown to read: each answer says what they print, and each
was checked by running it outside this page. Your toolkit is loaded,
including `mean` from [What is typical?](tutorial:what-is-typical) and
`count_if` from [A row of numbers](tutorial:a-row-of-numbers).

This page's database starts empty. The first cell makes a small table
of songs for the SQL problems, a made-up playlist. Run it first.

```sql exec
id: many-lang-practice-songs
DROP TABLE IF EXISTS song_tbl;
CREATE TABLE song_tbl (
    song_id INTEGER PRIMARY KEY,
    title TEXT,
    minutes REAL,
    plays INTEGER
);
INSERT INTO song_tbl (title, minutes, plays) VALUES
    ('Rain on the Roof', 3.5, 120),
    ('Last Bus Home', 4.0, 45),
    ('Two Short Days', 2.5, 300),
    ('The Long Road West', 5.0, 80),
    ('Kettle Song', 3.0, 210);
```

## Warm-up

A Python cell and a SQL cell for the warm-up problems.

```python exec
id: many-lang-practice-warm-up
# Try things here
```

```sql exec
id: many-lang-practice-warm-up-sql
SELECT * FROM song_tbl;
```

**1. Predict.** What does each line of JavaScript print?

```js
console.log(10 / 4);
console.log("3" + 4);
```

<details class="dl-answer"><summary>answer</summary>

`2.5`, then `34`.

`/` divides, as in Python. `"3" + 4` joins a piece of text and a number,
so JavaScript turns the 4 into text and gives `"34"`. Python would stop
with a `TypeError` on the second line.

</details>

**2. Predict.** How many rows will this query count? Decide, then run
it in the SQL cell.

```sql
SELECT COUNT(*) FROM song_tbl WHERE plays > 100;
```

<details class="dl-answer"><summary>answer</summary>

3: 'Rain on the Roof' (120), 'Two Short Days' (300) and 'Kettle Song'
(210). `WHERE` keeps only the rows where the condition is true, and
`COUNT(*)` counts what is left.

</details>

**3. Make.** A football team scored 2, 0, 3, 1, 1 and 5 goals in six
matches. Find the average in Python with your toolkit's `mean`, and then
without it, with `sum` and `len`.

<details class="dl-answer"><summary>answer</summary>

```python
goals = [2, 0, 3, 1, 1, 5]
print(mean(goals))
print(sum(goals) / len(goals))
```

Both print `2.0`. Python's own `sum` does the job of the toolkit's
`total`.

</details>

**4. Explain.** In JavaScript, what do the curly brackets `{ }` do in a
loop? What does Python use for the same job?

<details class="dl-answer"><summary>answer</summary>

They mark where the loop's body starts and stops: every line between
`{` and `}` is repeated. Python marks the body by indentation: every
line indented under the `for` line is repeated. Both answer the same
question, "what happens when, and how many times?", in different
syntax.

</details>

## Core

A cell for the core Python problems. Use the SQL cell above for the SQL
ones.

```python exec
id: many-lang-practice-core
# Your working for problems 5 to 12
```

**5. Make.** Write a SQL query for the average length of a song, in
minutes. Then write one that lists the titles of the songs longer than
the average.

<details class="dl-answer"><summary>answer</summary>

```sql
SELECT AVG(minutes) FROM song_tbl;
```

```sql
SELECT title FROM song_tbl
WHERE minutes > (SELECT AVG(minutes) FROM song_tbl);
```

The average is 3.6 minutes. Two songs are longer: 'Last Bus Home' (4.0)
and 'The Long Road West' (5.0).

</details>

**6. Fix.** This query should list the songs played more often than the
average song. It stops with an error. Read the error, then repair the
query.

```sql exec
id: many-lang-practice-fix-sql
SELECT title FROM song_tbl WHERE plays > AVG(plays);
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The error says `misuse of aggregate function AVG()`. An aggregate is
   a function that turns a whole column into one value.
2. `WHERE` looks at one row at a time. Can one row know the average of
   the whole column?
3. In the tutorial, how did the rainfall query get the average into its
   `WHERE`?

**Think about:** which part has to happen first, and how SQL lets you
say so.

</details>

<details class="dl-answer"><summary>answer</summary>

`WHERE` checks one row at a time, so it cannot work out the average of
the whole column by itself. A query in brackets can, and it runs first:

```sql
SELECT title FROM song_tbl
WHERE plays > (SELECT AVG(plays) FROM song_tbl);
```

The average is 151 plays, and two songs beat it: 'Two Short Days' and
'Kettle Song'. The mistake is about sequence: the average must be known
before any row is compared with it.

</details>

**7. Predict.** Here is a BASIC program, to read. What does it print?

```basic
10 LET N$ = "ADA"
20 PRINT N$ + " LOVELACE"
30 FOR I = 10 TO 1 STEP -3
40 PRINT I
50 NEXT I
60 END
```

<details class="dl-answer"><summary>answer</summary>

```text
ADA LOVELACE
 10
 7
 4
 1
```

`N$` ends in `$`, so it holds text, and `+` joins two pieces of text.
`STEP -3` counts down by 3, like `range(10, 0, -3)` in Python. BASIC
prints a space before each positive number.

</details>

**8. Make.** Here is a JavaScript function that counts how many bus
waits, in minutes, were longer than a limit. Write it in Python as
`count_over(values, limit)`, and check that it gives 3 for the same
list.

```js
function countOver(values, limit) {
  let count = 0;
  for (const value of values) {
    if (value > limit) {
      count = count + 1;
    }
  }
  return count;
}
console.log(countOver([12, 3, 25, 8, 17], 10));
```

<details class="dl-answer"><summary>answer</summary>

```python
def count_over(values, limit):
    """Return how many of values are bigger than limit."""
    count = 0
    for value in values:
        if value > limit:
            count = count + 1
    return count

waits = [12, 3, 25, 8, 17]
print(count_over(waits, 10))

def over_ten(value):
    return value > 10

print(count_if(waits, over_ten))
```

Both print 3. `function` became `def`, the braces became indentation,
`let` went away, and `countOver` became `count_over`. Your toolkit's
`count_if` does the same job with any test you give it.

</details>

**9. Explain.** Python refuses `"5" + 1`. What would you write in Python
to get the number 6? And to get the text `"51"`?

<details class="dl-answer"><summary>answer</summary>

```python
print(int("5") + 1)
print("5" + str(1))
```

`int("5")` turns the text into a number, so the `+` adds. `str(1)` turns
the number into text, so the `+` joins. Python makes you say which one
you mean. JavaScript picks one for you, and it picks joining.

</details>

**10. Another way.** Find the average song length in SQL without
`AVG`. Which two other SQL functions share out a sum?

<details class="dl-answer"><summary>answer</summary>

```sql
SELECT SUM(minutes) / COUNT(*) FROM song_tbl;
```

It gives 3.6, the same as `AVG(minutes)`. `SUM` adds the column, and
`COUNT(*)` counts the rows: the mean is the sum shared out equally.
This is the promise from
[What is typical?](tutorial:what-is-typical#share-it-out-equally-the-mean),
kept by different tools.

</details>

**11. Fix.** Someone turned the tutorial's BASIC loop, `FOR I = 1 TO 7`,
into Python. The average should be 5.0, but the cell prints 4.4. Find
the one mistake.

```python exec
id: many-lang-practice-fix-range
readings = [4.2, 0.0, 12.6, 7.1, 0.8, 3.3, 7.0]
running_sum = 0
for i in range(1, 7):
    running_sum = running_sum + readings[i]
print(running_sum / 7)
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Print `i` inside the loop. Which positions does it visit?
2. Where does a Python list start counting?
3. Which reading is never added?

**Think about:** BASIC's `FOR I = 1 TO 7` includes 7. Does Python's
`range(1, 7)`?

</details>

<details class="dl-answer"><summary>answer</summary>

The loop visits positions 1 to 6, so it never adds `readings[0]`, the
4.2 on Monday. The BASIC program counted from 1 because its array was
filled from 1. A Python list starts at 0, and `range` stops before its
second number. The fix is:

```python
for i in range(0, 7):
```

or, better, `for reading in readings:`, which cannot miss one. This is
a naming mistake: `R(1)` in BASIC and `readings[1]` in Python are not
the same reading.

</details>

**12. Explain.** A friend says, "SQL is not a real programming language:
it has no loops." What would you say back?

<details class="dl-answer"><summary>answer</summary>

A good answer might say: SQL is a different style, not a lesser one. It
is declarative, so a query says what result it wants, and the database
decides the steps. The loops are still there, inside the database, where
you do not have to write them. For questions about tables, that is
often the clearer way to write it.

You could also agree with part of what your friend says. SQL is made
for one kind of job, questions about data in tables, while Python is
made for almost any job. Most programs that use a database are written
in two languages: SQL for the questions, and another language for
everything else.

</details>

## Stretch

A cell for the stretch problems.

```python exec
id: many-lang-practice-stretch
# Your working for problems 13 to 15
```

**13. Predict.** In Python, `"5" + 1` is an error. What do these two
lines do, one in each language?

```python
print("5" * 3)
```

```js
console.log("5" * 3);
```

<details class="dl-answer"><summary>answer</summary>

Python prints `555`, and JavaScript prints `15`.

In Python, a piece of text times a whole number repeats the text. In
JavaScript, `*` only works on numbers, so it turns `"5"` into the number
5 first. So Python refuses `+` here and allows `*`, and JavaScript
changes its guess depending on the operator. The same symbols mean
different moves in different spaces, as on
[Four questions for any puzzle](tutorial:four-questions#the-same-move-in-a-different-space).

</details>

**14. Explain.** Here is a language you have probably never seen, Ruby.
Ask the four questions of it. What is named, what is promised, what
happens when, and what does its space do? It prints `15`. Why not
15.25?

```ruby
temps = [14, 17, 11, 19]
sum = 0
temps.each do |t|
  sum = sum + t
end
puts sum / temps.length
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Find the list, and the name that holds the running sum.
2. `each do |t| ... end` is Ruby's "for each": which Python line does
   the same job?
3. The sum is 61, and there are 4 temperatures. Which Python operator
   gives 15 from 61 and 4?

**Think about:** on
[Numbers a computer can hold](tutorial:numbers-a-computer-can-hold),
why does `7 // 2` give 3?

</details>

<details class="dl-answer"><summary>answer</summary>

- **Named:** `temps`, a list of four temperatures; `sum`, a running
  total; `t`, each temperature in turn.
- **Promised:** `puts` promises to print; `.length` promises the number
  of items.
- **What happens when:** `sum` starts at 0, each temperature is added in
  turn, and the division comes after the loop.
- **The space:** in Ruby, a whole number divided by a whole number gives
  a whole number, rounded down, like Python's `//`. So $61 \div 4$ gives
  15. To get 15.25, Ruby needs one of the numbers to be a decimal, such
  as `sum.to_f / temps.length`.

You read a program in a language you had never seen, by asking four
questions. That is the idea of the tutorial.

</details>

**15. Make.** Write a Python function `days_above_average(values)` that
gives back how many values are bigger than their own mean. Test it with
`assert` on the tutorial's rainfall (3) and on the song plays from
problem 6 (2).

<details class="dl-answer"><summary>answer</summary>

```python
def days_above_average(values):
    """Return how many of values are bigger than the mean of values."""
    average = mean(values)
    above = 0
    for value in values:
        if value > average:
            above = above + 1
    return above

assert days_above_average([4.2, 0.0, 12.6, 7.1, 0.8, 3.3, 7.0]) == 3
assert days_above_average([120, 45, 300, 80, 210]) == 2
assert days_above_average([5, 5, 5]) == 0, "nothing is above itself"
print("days_above_average keeps its promise.")
```

The function does in Python what the tutorial's SQL did with a query
inside a query: first find the average, then compare every value with
it. The last test checks an edge: when every value is the same, none is
above the average.

</details>
