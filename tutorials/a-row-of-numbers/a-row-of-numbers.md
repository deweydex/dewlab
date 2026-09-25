---
title: "A row of numbers: lists"
year: "2026-2027"
version: 2026.09.24.1
datasets: [life-expectancy]
covers:
  a-week-in-one-name:
    covers: [MIT-6.3]
  counting-from-0:
    covers: [MIT-6.3]
    touches: [MIT-6.4]
  counting-from-the-end:
    covers: [MIT-6.3]
  a-slice-of-the-week:
    covers: [MIT-6.3]
  changing-a-list:
    covers: [MIT-6.3]
  going-through-by-index:
    covers: [MIT-6.7]
  building-a-new-list-in-a-loop:
    covers: [MIT-6.5]
    touches: [PDP-LO6]
  adding-and-multiplying-lists:
    covers: [MIT-6.3, MIT-6.7]
  two-names-for-one-list:
    covers: [MIT-6.3]
  three-tools-for-your-toolkit:
    covers: [MIT-6.5]
    touches: [PDP-LO8, PDP-LO10]
  a-real-list-ireland-since-1950:
    covers: [MIT-6.5, MIT-6.7]
---

# A row of numbers: lists

A weather app shows the highest temperature for each day of the week.
That is seven numbers. How do we keep them in a program, so that we can
ask which day was warmest, or how much warmer Friday was than Thursday?
Seven names would work, for a week. For a year, we would need 365.

On this page we:

- keep many values under one name, in a list
- find one value by its position, counting from the front and from the
  back
- take a slice of a list, change a list, and make it longer
- go through a list by position, and build a new list in a loop
- see what `+` and `*` do to lists, and do the maths meaning ourselves
- see what happens when two names point at one list
- add `largest`, `smallest` and `count_if` to the toolkit, and use them
  on 67 years of real Irish data

> **The space we're in.** Lists of numbers, and now and then of words.
> We met lists on [Doing it again](tutorial:doing-it-again) as "a row of
> values", and used `len`, `append` and `[0]` in passing. This page is
> where we learn them properly. One thing usually goes unsaid: Python
> counts positions from 0, and maths usually counts from 1. Both are
> right, in their own space. Your toolkit is loaded, from `digit_at`
> to `close_enough`.

## Warm-up

Two questions from earlier pages. The first is from
[Doing it again](tutorial:doing-it-again#counting-with-range), and the
second from
[What a function can see](tutorial:what-a-function-can-see#handing-over-a-list).

```question
id: row-warm-up-1
type: fill-in-the-blank

`range(2, 6)` gives the whole numbers 2, 3, 4 and 5. That is {4}
numbers, because the stop number is left out.
```

```question
id: row-warm-up-2
type: multiple-choice
correct: 2

`add_song(playlist, song)` puts a song at the end of `playlist` with
`append`. After `road_trip = ["Zombie", "Linger"]` and
`add_song(road_trip, "Galway Girl")`, what does `road_trip` hold?

- `["Zombie", "Linger"]`
- `["Zombie", "Linger", "Galway Girl"]`
- `None`
```

## A week in one name

Here is one week of highest temperatures in Dublin, in degrees Celsius,
from Monday to Sunday. The numbers are made up, but they are close to a
real week in April.

```python exec
id: row-week-1
week = [11, 13, 9, 12, 14, 10, 8]
print(week)
print(len(week))
```

A *list* is a row of values, kept in order, under one name. The square
brackets start and end it, and commas go between the values. `len()`
gives the length: how many values the list holds. Here it is 7.

This is the idea this unit leans on: naming. Seven values, and only one
name. The name `week` does not point at 11, or at 8. It points at the
whole row.

## Counting from 0

So how do we ask for Thursday's temperature? We write the list's name,
then a position in square brackets. Before you run it, guess: which day
will `week[3]` give?

```python exec
id: row-index-1
print(week[0])
print(week[3])
```

`week[0]` is 11, Monday's temperature, and `week[3]` is 12, which is
Thursday's. The number in square brackets is the *index*: the position
of a value in the list. Python's first index is 0, so a week goes from
`week[0]` to `week[6]`.

Why start at 0? Think of an index as "how many steps from the start".
Monday is at the start, 0 steps along. Thursday is 3 steps along. A
building in Ireland counts its floors the same way: the ground floor is
0, and the first floor is one flight of stairs up.

Maths usually counts from 1. On
[Doing it again](tutorial:doing-it-again#sigma-a-loop-written-by-mathematicians)
we wrote a list of numbers as $x_1, x_2, x_3$, and so on. Maths calls a
list of values in order a sequence. It is the word from our third
question, "what happens when?", because the values come one after
another. So the same week can be written two ways:

| Day | Mon | Tue | Wed | Thu | Fri | Sat | Sun |
|---|---|---|---|---|---|---|---|
| In maths | $x_1$ | $x_2$ | $x_3$ | $x_4$ | $x_5$ | $x_6$ | $x_7$ |
| In Python | `week[0]` | `week[1]` | `week[2]` | `week[3]` | `week[4]` | `week[5]` | `week[6]` |
| Value | 11 | 13 | 9 | 12 | 14 | 10 | 8 |

So $x_i$ in maths is `week[i - 1]` in Python. Neither way is wrong. They
are two spaces with two rules, and it helps to ask which one you are in.

Notice what `week[3]` is. It is a name made from a name and a number.
We can use it anywhere we could use a plain name. `week[4] - week[3]`
is how much warmer Friday was than Thursday.

What happens if we ask for `week[7]`? The cell below is meant to stop
with an error.

```python exec
id: row-index-2
print(week[7])
```

The last line says `IndexError: list index out of range`. An
*IndexError* means we asked for a position the list does not have. A
list of 7 values has indexes 0 to 6, so 7 is one past the end. It is
the same mistake as the `range` warm-up, seen from the other side.

## Counting from the end

Often we want the last value: today's reading, the newest price. We
could write `week[len(week) - 1]`, which is `week[6]`. Python has a
shorter way. What do you think `week[-1]` gives?

```python exec
id: row-end-1
print(week[-1])
print(week[-2])
print(week[len(week) - 1])
```

`week[-1]` is 8, Sunday, the last value. `week[-2]` is 10, the one
before it. A *negative index* counts from the end: `-1` is the last
value, `-2` is the one before the last, and so on. It works whatever
the length of the list, which is why it is so useful.

## A slice of the week

Now we want only the work days, Monday to Friday. A *slice* is a part
of a list, taken with two indexes and a colon between them:
`week[start:stop]`. Like `range`, the stop is left out. Before you run
the cell, which temperatures do you expect on each line?

```python exec
id: row-slice-1
print(week[0:5])
print(week[5:7])
print(week[:3])
print(week[5:])
```

`week[0:5]` is Monday to Friday: indexes 0, 1, 2, 3 and 4. A slice from
`start` to `stop` holds `stop - start` values, so this one holds 5. If
we leave out the start, the slice starts at the front. If we leave out
the stop, it goes to the end. So `week[5:]` is the weekend.

A slice is a new list. Taking it does not change `week`.

### Your turn

1. Print the middle three days, Tuesday to Thursday, with one slice.
2. Print the last three days with a slice that uses a negative index.
3. What does `week[3:3]` give? Guess, then try it.

```python exec
id: row-slice-your-turn
# Your slices here
```

## Changing a list

On Wednesday the thermometer was in the sun, and the real highest was
15 degrees, not 9. We can point one position at a new value, the way
we point a name at a new value. And when next Monday comes, we can add
a value at the end. What will the last line print?

```python exec
id: row-change-1
week[2] = 15
print(week)
week.append(12)
print(week)
print(len(week))
```

`week[2] = 15` changed one value. The list is still 7 long, and every
other value stayed where it was. `append` added 12 at the end, so the
list is now 8 long.

Look again at `week[2] = 15`. It is `=`, as always: the name on the
left, here `week[2]`, points at a new value. What is new is that the
name is made from a list and an index.

Let's set the week back to the way it was, for the rest of the page:

```python exec
id: row-change-2
week = [11, 13, 9, 12, 14, 10, 8]
```

## Going through by index

On [Doing it again](tutorial:doing-it-again#doing-it-for-each), a `for`
loop went through a list one value at a time. That works for "add them
all up". Now try this question: on which days was it warmer than the
day before? To answer it, each step needs two values, today's and
yesterday's. So we go through the positions instead of the values.

`range(len(week))` gives the indexes 0, 1, 2, and so on up to 6. Here
we start at 1, because Monday has no day before it in our list. We also
keep the day names in a second list, with the same order. What will the
cell print?

```python exec
id: row-by-index-1
days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

for i in range(1, len(week)):
    change = week[i] - week[i - 1]
    if change > 0:
        print(days[i], "was", change, "degrees warmer than", days[i - 1])
```

Tuesday, Thursday and Friday. Each time round, `i` is one index, so
`week[i]` is today and `week[i - 1]` is yesterday. And the same `i`
finds the day's name in `days`, because the two lists are in the same
order.

Going through a list by index means using the position as the loop
variable, and the list's name with `[i]` to reach each value. It is the
way to go when a step needs a value's neighbours, or a second list.

```question
id: row-by-index-2
type: multiple-choice
correct: 3

A cell loops `for i in range(len(week)):` and uses `week[i + 1]`. What
happens on the last time round?

- It gives the first value again.
- It gives the last value.
- It stops with an `IndexError`.
```

## Building a new list in a loop

A visitor from Boston wants the week in Fahrenheit. Your toolkit has
`celsius_to_fahrenheit` from
[Running a formula backwards](tutorial:running-a-formula-backwards).
We start with an empty list, `[]`, and `append` one converted value each
time round. How long will the new list be?

```python exec
id: row-build-1
week_fahrenheit = []
for celsius in week:
    week_fahrenheit.append(celsius_to_fahrenheit(celsius))
print(week_fahrenheit)
print(len(week_fahrenheit))
```

Seven values, one for each day, from 51.8 °F on Monday to 46.4 °F on
Sunday. This is a running total's shape again: start before the loop
with something empty, and add to it each time round. For a total, the
start is 0. For a list, the start is `[]`.

### Your turn

1. Build a list `cool_days` that holds only the temperatures below
   10. You will need an `if` inside the loop.
2. Before you run it, how many values will it hold?

```python exec
id: row-build-your-turn
cool_days = []
# Your loop here
print(cool_days)
```

## Adding and multiplying lists

A pub quiz has four teams, and two rounds. Here are each team's points
in round 1 and round 2, in the same team order. In maths, adding two
rows of numbers like these means adding each pair: the first team's two
scores, then the second's, and so on. What do you think Python's `+`
does? And `*`?

```python exec
id: row-add-1
round_one = [8, 6, 9, 5]
round_two = [7, 9, 4, 8]
print(round_one + round_two)
print(round_one * 2)
```

Python's `+` does not add the pairs. It joins the two lists into one
longer list, eight values long. And `* 2` repeats the list twice. This
is not a mistake in Python. In Python's space, a list is a row of any
values, words as well as numbers, and joining and repeating make sense
for any row. Adding pairs only makes sense for numbers.

So for the maths meaning, we go through by index, and add the pairs
ourselves:

```python exec
id: row-add-2
quiz_scores = []
for i in range(len(round_one)):
    quiz_scores.append(round_one[i] + round_two[i])
print(quiz_scores)
```

Each team's points: 15, 15, 13 and 13. Adding lists this way, pair by
pair, is called *adding element by element*. In maths, it only works
when the two lists are the same length.

Multiplying every value by one number is the other common move. A café
shows its prices without VAT, and needs to add 13.5%, which means
multiplying each price by 1.135. The cell below is meant to stop with
an error. Can you guess which kind?

```python exec
id: row-add-3
prices = [3.20, 4.50, 2.80]
print(prices * 1.135)
```

A `TypeError`, whose last line says we `can't multiply sequence by
non-int of type 'float'`. Repeating a list 1.135 times means nothing,
so Python refuses. The move we wanted belongs to a different space.

Python has that space too. *numpy*, which is on every page, has an
*array*: a row of numbers where `+` and `*` work element by element,
the maths way. What do you expect this time?

```python exec
id: row-add-4
import numpy as np

print(np.array(prices) * 1.135)
print(np.array(round_one) + np.array(round_two))
```

The same moves, in a space built for numbers, give the maths answer:
€3.63, €5.11 and €3.18 once rounded to the cent, and the same quiz
scores as before.
This unit works with lists, so that we can see every step. When you
meet an array later, you will know what it does for you.

## Two names for one list

Here is a puzzle about naming. We copy the week into a second name,
`forecast`, and change Sunday in the forecast to 16 degrees. What does
`week` hold now?

```python exec
id: row-two-names-1
week = [11, 13, 9, 12, 14, 10, 8]
forecast = week
forecast[6] = 16
print(week)
```

`week` changed too, and Sunday is 16 in both. Here is a picture in
words. The list is one box with seven values in it. A name is a label
on a string, tied to a box. `forecast = week` does not make a second
box. It ties a second label to the same box. So a change through one
label is a change to the only box there is, and both labels see it.

You met this on
[What a function can see](tutorial:what-a-function-can-see#handing-over-a-list),
where a function changed a playlist it was handed. It is the same
thing: one list, two names.

When we want a second box, we ask for one. `.copy()` makes a new list
with the same values in it. What will each line print now?

```python exec
id: row-two-names-2
week = [11, 13, 9, 12, 14, 10, 8]
forecast = week.copy()
forecast[6] = 16
print(week)
print(forecast)
```

Now `week` keeps its 8, and only `forecast` has 16. Two boxes, one label
each. A slice is also a new list, so `week[:]` would work too.

So there are two different moves. `forecast = week` points a name at a
list that already exists. `forecast[6] = 16` changes the list itself.
The first is renaming, and it changes nothing. The second changes the
value, and every name that points at it sees the change.

## Three tools for your toolkit

On [Does it work?](tutorial:does-it-work#a-walkthrough-by-hand) you
fixed a function called `warmest`, so that it starts from the first
reading. It finds the biggest value in any list of numbers, not only
temperatures. So in the toolkit it gets a name for any list: `largest`.
It is written for you below.

`smallest` is a stub. It has the same shape as `largest`, with one sign
turned round. `count_if` is a stub too. It is given a list and a test:
a function that returns True or False for one value. It counts the
values for which the test gives True. You handed a function to a
function on [How likely is it?](tutorial:how-likely-is-it#a-tool-that-runs-it-many-times),
when `simulate` was given a trial.

```python exec
id: row-toolkit
toolkit: yes
def largest(values):
    """Return the biggest number in values, a list of at least one number."""
    biggest_so_far = values[0]
    for value in values:
        if value > biggest_so_far:
            biggest_so_far = value
    return biggest_so_far


def smallest(values):
    """Return the smallest number in values, a list of at least one number."""
    ...


def count_if(values, test):
    """Return how many values in values make test(value) give True.

    test is a function that takes one value and returns True or False.
    """
    ...
```

```python toolkit-reference
for: row-toolkit
def largest(values):
    """Return the biggest number in values, a list of at least one number."""
    biggest_so_far = values[0]
    for value in values:
        if value > biggest_so_far:
            biggest_so_far = value
    return biggest_so_far


def smallest(values):
    """Return the smallest number in values, a list of at least one number."""
    smallest_so_far = values[0]
    for value in values:
        if value < smallest_so_far:
            smallest_so_far = value
    return smallest_so_far


def count_if(values, test):
    """Return how many values in values make test(value) give True.

    test is a function that takes one value and returns True or False.
    """
    count = 0
    for value in values:
        if test(value):
            count = count + 1
    return count
```

Run the toolkit cell, then the tests. Until both stubs are written,
this cell stops with an error. Why do you think one test uses a list
with only one value in it?

```python exec
id: row-toolkit-tests
def is_cold(celsius):
    """True when celsius is below 10 degrees."""
    return celsius < 10


assert largest([11, 13, 9, 12, 14, 10, 8]) == 14
assert largest([-3, -1, -4]) == -1
assert smallest([11, 13, 9, 12, 14, 10, 8]) == 8
assert smallest([5]) == 5
assert count_if([11, 13, 9, 12, 14, 10, 8], is_cold) == 2
assert count_if([], is_cold) == 0
print("largest, smallest and count_if keep their promises.")
```

```hint
Which test does the error point at? Try `print(smallest([4, 2, 7]))` on
its own. If it shows `None`, the function has no `return` yet.
```

```hint
after: 12 errors
title: some steps
1. `smallest` starts from `values[0]`, as `largest` does.
2. It goes through every value, and keeps the new one when it is
   smaller: `<` in place of `>`.
3. `count_if` starts a count at 0, and adds 1 each time `test(value)`
   gives True. It returns the count after the loop.

**Think about:** why does `count_if` write `test(value)`, with
brackets, when the test was handed over as `is_cold`, without them?
```

A list with one value is the edge of the promise, "at least one
number". Mistakes like to hide at the edges.

Python has its own `max()` and `min()`, which do what `largest` and
`smallest` do. Writing our own shows what happens inside. One warning
about names, as with `total`: a cell that says `largest = 14` hides
the tool on that page. Call the number `warmest_day` or `top_score`
instead.

## A real list: Ireland since 1950

Now a list too long to type. The file `life-expectancy.csv` holds life
expectancy at birth, in years, for many countries from 1950 to 2016.
Life expectancy is how long a baby born that year could expect to live.

The first line loads the file. `await` means "wait until the file has
arrived". The second line keeps the rows where the country is Ireland,
takes the `life_expectancy` column, and makes it a list. That is all we
need from the file. From there on, it is an ordinary list, and the
maths is ours.

```python exec
id: row-real-1
df = await load_csv("life-expectancy.csv")
ireland = df[df.country == "Ireland"]["life_expectancy"].tolist()

print(len(ireland))
print(ireland[0], ireland[-1])
print(ireland[-5:])
```

67 values, one for each year from 1950 to 2016. A baby born in Ireland
in 1950 could expect about 65.6 years, and one born in 2016 about 81.1.
The last line shows the last five years, with a negative index in a
slice.

The index tells us the year: index 0 is 1950, so index `i` is the year
`1950 + i`. Before you run the next cell, guess: in how many years was
life expectancy 80 or more? And what was the lowest value? The cell
uses your `smallest` and `count_if`. Until they are written, it prints
`None` where their answers should be.

```python exec
id: row-real-2
def eighty_or_more(years):
    """True when a life expectancy is 80 years or more."""
    return years >= 80


print(largest(ireland), smallest(ireland))
print(count_if(ireland, eighty_or_more), "years at 80 or more")
```

The lowest was 64.78 years, and 7 years were at 80 or more: 2010 to
2016. Now a question `count_if` cannot answer on its own, because each
step needs the year before. In which years did life expectancy go down?

```python exec
id: row-real-3
for i in range(1, len(ireland)):
    if ireland[i] < ireland[i - 1]:
        print(1950 + i, "fell from", ireland[i - 1], "to", ireland[i])
```

Ten years, and the last one was 1985. A single year can dip for many
reasons, such as a bad flu season. The long rise is the story.

### Your turn

1. Which year had the lowest life expectancy? Go through by index, and
   print the year where `ireland[i]` equals `smallest(ireland)`.
2. Find the biggest rise from one year to the next. Guess first: was it
   early or late in the list?
3. Pick another country, such as `"Spain"` or `"Nigeria"`, and make its
   list in the same way. How do its first and last values compare with
   Ireland's?

```python exec
id: row-real-your-turn
# Your loops here
```

<details class="dl-why"><summary>Why this way?</summary>

This page said a name is a label on a string, tied to a value. Many
courses picture a name as a box instead, with the value kept inside it.

The box is a good picture for numbers. It is simple, and for `x = 5`
it never gives a wrong answer. Many teachers start with it for that
reason.

We used the label because the box gives the wrong answer for lists.
If `forecast` were a box, `forecast = week` would copy the week into
it, and changing the forecast could never change the week. Python
does not work that way. With labels, one list with two names is
something you can picture. The same picture explains the playlist on
What a function can see, where a function was handed a list and
changed it.

</details>

## Four questions, looking back

| The question | On this page |
|---|---|
| What is named here? | a whole list under one name, `week`; a value by its position, `week[3]`, a name made from a name and a number; one list with two names |
| What is promised? | `len` gives the length; a slice gives a new list; `largest`, `smallest` and `count_if` keep the promises in their docstrings |
| What happens when? | a loop by index goes through positions in order, so each step can reach its neighbours; a new list grows by `append`, one value each time round |
| What does this space let us do? | Python counts from 0, maths from 1; in Python's list space `+` joins and `*` repeats; in numpy's array space they work element by element |

## What we have now

| Term or tool | What it means |
|---|---|
| list, `len()` | a row of values in order, under one name; how many values it holds |
| index, `week[i]` | a value's position, counting from 0 |
| sequence, $x_1, x_2, \dots$ | a list of values in order, in maths, counting from 1 |
| `IndexError` | we asked for a position the list does not have |
| negative index | counts from the end: `week[-1]` is the last value |
| slice, `week[start:stop]` | a new list from `start` up to `stop`, with `stop` left out |
| `week[2] = 15`, `append` | point one position at a new value; add a value at the end |
| going through by index | `for i in range(len(week)):`, using `week[i]` and its neighbours |
| building a list in a loop | start with `[]`, and `append` each time round |
| `+` and `*` on lists | join two lists; repeat a list |
| element by element | adding or multiplying each pair of values; numpy's arrays do it for us |
| two names for one list, `.copy()` | `b = a` ties a second name to the same list; `.copy()` makes a new one |
| `largest`, `smallest`, `count_if` | your three new toolkit tools |

The practice page is next. After it,
[What is typical?](tutorial:what-is-typical) asks what one number could
stand for a whole list, and finds three different answers.

For more on lists, the integrated course has
[Lists: keeping many values in order](tutorial:lists-and-sequences).
