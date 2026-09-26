---
title: "A row of numbers: lists"
year: "2026-2027"
version: 2026.09.26.1
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

Seven names would work, for a week. A year would need 365 names. A
phone that counts your steps every minute makes 525,600 numbers a year.
Nobody can write half a million names. By the end of this page, one
name will hold them all, and you will be asking questions of 74 years of
real Irish data with a few lines of code.

On this page we:

- keep many values under one name, in a list
- find one value by its position, counting from the front and from the
  back
- take a slice of a list, change a list, and make it longer
- loop over a list by position, and build a new list in a loop
- see what `+` and `*` do to lists, and do the maths meaning ourselves
- see what happens when two names point at one list
- add `largest`, `smallest` and `count_if` to the toolkit, and use them
  on 74 years of real Irish data

> **The space we're in.** We work with lists of numbers, and now and then of words.
> We met lists on [Doing it again](tutorial:doing-it-again) as "a row of
> values", and used `len`, `append` and `[0]` in passing. On this page
> we learn them properly. We usually do not say it, but Python counts
> positions from 0, and maths usually counts from 1. Each way
> works, in its own space. Your toolkit is loaded, from `digit_at`
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
answer: 2

`add_reading(readings, value)` puts a value at the end of `readings`
with `append`. After `today = [14.2, 14.8]` and
`add_reading(today, 15.1)`, what does `today` hold?

- `[14.2, 14.8]`
  - This is what you would see if the function worked on a copy of the list.
- `[14.2, 14.8, 15.1]`
  - `append` changes the list itself, and `today` names that same list.
- `None`
  - `None` is what `add_reading` gives back; the list it changed is still `today`.
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

This unit is about naming. Here we have seven values, and only one
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
Thursday's. If you guessed Wednesday, you counted the way people usually
do, and Python counts another way. The number in square brackets is the *index*: the position
of a value in the list. Python's first index is 0, so a week goes from
`week[0]` to `week[6]`.

Why start at 0? Think of an index as "how many steps from the start".
Monday is at the start, 0 steps along. Thursday is 3 steps along. A
building in Ireland counts its floors the same way: the ground floor is
0, and the first floor is one flight of stairs up.

<aside class="dl-note" id="row-note-zero">

**An argument about 0.** In 1982 the computer scientist Edsger Dijkstra
wrote a short note called "Why numbering should start at zero". His
reason was about ranges like `range(0, 7)`. When you count from 0 and
leave the end out, the length of a range is the end minus the start,
and nothing needs a "+ 1". Python chose his way. Some other languages,
such as MATLAB and Lua, count from 1.

</aside>

Maths usually counts from 1. On
[Doing it again](tutorial:doing-it-again#sigma-a-loop-written-by-mathematicians)
we wrote a list of numbers as $x_1, x_2, x_3$, and so on. Maths calls a
list of values in order a sequence, because the values come one after
another. So the same week can be written two ways:

| Day | Mon | Tue | Wed | Thu | Fri | Sat | Sun |
|---|---|---|---|---|---|---|---|
| In maths | $x_1$ | $x_2$ | $x_3$ | $x_4$ | $x_5$ | $x_6$ | $x_7$ |
| In Python | `week[0]` | `week[1]` | `week[2]` | `week[3]` | `week[4]` | `week[5]` | `week[6]` |
| Value | 11 | 13 | 9 | 12 | 14 | 10 | 8 |

So $x_i$ in maths is `week[i - 1]` in Python. They are two spaces with
two rules, and it helps to ask which one you are in.

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
list of 7 values has indexes 0 to 6, so 7 is one past the end. The
`range` warm-up had the same edge.

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
the length of the list, so the same line finds the newest reading in a
week of data or in a year of it.

<img src="indexes-both-ways.svg" alt="The list week drawn as seven boxes holding 11, 13, 9, 12, 14, 10 and 8, for Monday to Sunday. Above each box is its index, from [0] for Monday to [6] for Sunday. Below each box is its negative index, from [−7] for Monday to [−1] for Sunday.">

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

Let's set the week back to the way it was, for the rest of the page:

```python exec
id: row-change-2
week = [11, 13, 9, 12, 14, 10, 8]
```

## Going through by index

On [Doing it again](tutorial:doing-it-again#doing-it-for-each), a `for`
loop took the values of a list one at a time. That works for "add them
all up". Now try this question: on which days was it warmer than the
day before? To answer it, each step needs two values, today's and
yesterday's. So we loop over the positions instead of the values.

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

It prints Tuesday, Thursday and Friday. Each time round, `i` is one index, so
`week[i]` is today and `week[i - 1]` is yesterday. And the same `i`
finds the day's name in `days`, because the two lists are in the same
order.

Use a loop by index when a step needs a value's neighbours, or a
second list.

```question
id: row-by-index-2
type: multiple-choice
answer: 3

A cell loops `for i in range(len(week)):` and uses `week[i + 1]`. What
happens on the last time round?

- It gives the first value again.
  - This is what you would see if the positions went round in a circle, as some languages allow.
- It gives the last value.
  - `week[i + 1]` looks one place ahead, so on the last time round it looks past the end.
- It stops with an `IndexError`.
  - On the last time round, `i + 1` is one past the last position, and nothing is there.
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

The new list has seven values, from 51.8 °F on Monday to 46.4 °F on
Sunday. This is the shape of a running total again. We start before
the loop with something empty, and add to it each time round. For a total, the
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

A sound on a computer is a list of numbers. A microphone measures the
push of the air many times a second, and each measurement is a
*sample*. A music CD keeps 44,100 samples every second, for each
speaker. Here are eight samples from each of two short sounds, a low
note and a high note. They are made up, and much shorter than a real
sound.

To play both notes at once, a computer adds the two lists pair by pair:
the first sample of one to the first sample of the other, and so on.
In maths, adding two rows of numbers usually means that too. What do you
think Python's `+` does? And `*`? Pause here and guess. I'll wait.

```python exec
id: row-add-1
low_note = [0, 5, 8, 5, 0, -5, -8, -5]
high_note = [0, 4, 0, -4, 0, 4, 0, -4]
print(low_note + high_note)
print(low_note * 2)
```

Python's `+` does not add the pairs. It joins the two lists into one
longer list, sixteen values long: the low note, and then the high note
after it. And `* 2` plays the low note twice. Python is keeping a
promise of its own here. In Python's space, a list is a row of any values,
words as well as numbers, and joining and repeating make sense for any
row. Adding pairs only makes sense for numbers.

So for the maths meaning, we go through by index, and add the pairs
ourselves:

```python exec
id: row-add-2
both_notes = []
for i in range(len(low_note)):
    both_notes.append(low_note[i] + high_note[i])
print(both_notes)
```

The mixed sound is `[0, 9, 8, 1, 0, -1, -8, -9]`. Adding lists this way,
pair by pair, is called *adding element by element*. In maths, it only
works when the two lists are the same length.

<img src="adding-two-notes.svg" alt="Three rows of samples, with one stem for each index from 0 to 7. low_note is 0, 5, 8, 5, 0, −5, −8, −5. high_note is 0, 4, 0, −4, 0, 4, 0, −4. both_notes, their sum index by index, is 0, 9, 8, 1, 0, −1, −8, −9. A dashed line follows index 1 down the three rows: 5 plus 4 is 9.">

Multiplying every value by one number is the other common move: every
sample times 0.5 makes the sound quieter. The cell below is meant to
stop with an error. Can you guess which kind?

```python exec
id: row-add-3
print(low_note * 0.5)
```

It stops with a `TypeError`, whose last line says we `can't multiply sequence by
non-int of type 'float'`. Repeating a list half a time means nothing,
so Python refuses. The move we wanted belongs to a different space.

Python has that space too. *numpy*, which is on every page, has an
*array*: a row of numbers where `+` and `*` work element by element,
the maths way. What do you expect this time?

```python exec
id: row-add-4
import numpy as np

print(np.array(low_note) * 0.5)
print(np.array(low_note) + np.array(high_note))
```

The same moves, in a space built for numbers, give the maths answer.
Programs that work with real sound use arrays, because a song is
millions of samples. This unit works with lists, so that we can see
every step.

<aside class="dl-note" id="row-note-cd">

**Why 44,100?** People hear sounds up to about 20,000 vibrations a
second. To keep a sound, a computer must take more than two samples
for each vibration, so more than 40,000 samples a second. The makers of
the CD, Sony and Philips, chose 44,100 in the early 1980s.

</aside>

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

`week` changed too, and Sunday is 16 in both. Nobody touched `week`,
and still it changed. That surprises almost everyone the first time.
Here is a picture in words. The list is one box with seven values in it. A name is a label
on a string, tied to a box. `forecast = week` does not make a second
box. It ties a second label to the same box. So a change through one
label is a change to the only box there is, and both labels see it.

You met this on
[What a function can see](tutorial:what-a-function-can-see#handing-over-a-list),
where a function changed a playlist it was handed. It is the same
thing. There is one list with two names.

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

Now `week` keeps its 8, and only `forecast` has 16. There are two boxes now,
with one label each. A slice is also a new list, so `week[:]` would work too.

<img src="two-labels-one-box.svg" alt="Two pictures. On the left, after forecast = week, the labels week and forecast both point at one list, 11, 13, 9, 12, 14, 10, 16, so both names see the 16. On the right, after forecast = week.copy(), week points at a list that ends in 8, and forecast points at a second list that ends in 16.">

So there are two different moves. `forecast = week` is renaming, and it
changes nothing. `forecast[6] = 16` changes the list itself, and every
name that points at it sees the change.

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

Here is a test to hand to `count_if`. It gives True for a cold day,
below 10 degrees. Run it before the toolkit cell, because the table
under the toolkit uses it.

```python exec
id: row-is-cold
def is_cold(celsius):
    """True when celsius is below 10 degrees."""
    return celsius < 10
```

Now the toolkit cell.

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

Run the toolkit cell. How do your `smallest` and `count_if` compare
with one way to write them? The table below runs the same calls on your
tools and on a solution, side by side. Where a row is different, try
that call on its own. Why do you think one row uses a list with only one
value in it?

```inputs
for: row-toolkit
largest([11, 13, 9, 12, 14, 10, 8])
largest([-3, -1, -4])
smallest([11, 13, 9, 12, 14, 10, 8])
smallest([5])
count_if([11, 13, 9, 12, 14, 10, 8], is_cold)
count_if([], is_cold)
```

```solution
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

```hint
for: row-toolkit
after: 3 runs
Which row is different? Try `print(smallest([4, 2, 7]))` on its own. If
it shows `None`, the function has no `return` yet.
```

```hint
for: row-toolkit
after: 8 runs
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
number". Bugs like to hide at the edges. If the stubs are hard to
write, copy `largest` and change one thing at a time. After a few tries,
a fold under the table offers the steps, and you can come back to
`count_if` after the next section.

Python has its own `max()` and `min()`, which do the same jobs. One
warning about names, as with `total`: a cell that says `largest = 14`
hides the tool on that page. Call the number `warmest_day` instead.

## A real list: Ireland since 1950

Now a list too long to type. The file `life-expectancy.csv` holds life
expectancy at birth, in years, for many countries from 1950 to 2023.
Life expectancy is how long a baby born that year could expect to live.

The numbers on this page come from the copy of the file saved on
{{snapshot: life-expectancy}}. When the cell loads the file, a line under
it says whether it got that copy or a newer one from Our World in Data.
With a newer one, a few of your numbers may be a little different from
ours.

The first line loads the file. `await` means "wait until the file has
arrived". The second line keeps Ireland's rows, takes the
`life_expectancy` column, and makes it a list. From there on, it is an
ordinary list, and we do the maths ourselves.

```python exec
id: row-real-1
df = await load_csv("life-expectancy.csv")
ireland = df[df.country == "Ireland"]["life_expectancy"].tolist()

print(len(ireland))
print(ireland[0], ireland[-1])
print(ireland[-5:])
```

The list has 74 values, one for each year from 1950 to 2023. A baby born in Ireland
in 1950 could expect about 65.6 years, and one born in 2023 about 82.4.
The last line shows the last five years, with a negative index in a
slice. They are not all rising. Keep that in mind for a few minutes.

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

The lowest was 64.75 years, and 15 years were at 80 or more: 2009 to
2023. Now a question `count_if` cannot answer on its own, because each
step needs the year before. In which years did life expectancy go down?

```python exec
id: row-real-3
for i in range(1, len(ireland)):
    if ireland[i] < ireland[i - 1]:
        print(1950 + i, "fell from", ireland[i - 1], "to", ireland[i])
```

Life expectancy went down in fifteen of the years. The last two, 2020 and 2021, are the years of the
COVID-19 pandemic. A single year can dip for many reasons, such as a bad
flu season, but the long rise is still the main pattern.

### Your turn

1. Which year had the lowest life expectancy? Loop by index, and
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

The box works well as a picture for numbers. It is simple, and for
`x = 5` it always matches what Python does. Many teachers start with it for that
reason.

We used the label because the box does not match what Python does
with lists.
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
| What happens when? | a loop by index visits positions in order, so each step can use its neighbours; a new list grows by `append`, one value each time round |
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
[Lists and looping over them](tutorial:lists-and-sequences).

## Where to read more

CrashCourse (2017). *Data Structures: Crash Course Computer Science #14.*
<https://www.youtube.com/watch?v=DuDz6B4cqVc>. How a computer keeps a list
in its memory, and why some jobs need a different shape of data, such as a
queue or a tree. Ten minutes.
