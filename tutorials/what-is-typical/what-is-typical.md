---
title: "What is typical? Mean, median, mode and spread"
year: "2026-2027"
version: 2026.09.24.1
datasets: [life-expectancy]
covers:
  share-it-out-equally-the-mean:
    covers: [MIT-5.12]
    touches: [MIT-6.4]
  the-middle-one-in-the-line-the-median:
    covers: [MIT-5.12]
    touches: [MIT-6.7]
  the-most-common-the-mode:
    covers: [MIT-5.12]
  when-the-three-disagree:
    covers: [MIT-5.13]
  a-lopsided-world:
    covers: [MIT-5.13]
    touches: [MIT-6.5]
  how-spread-out-the-range:
    covers: [MIT-5.12]
  how-far-from-the-mean-on-average:
    covers: [MIT-5.12]
  the-standard-deviation:
    covers: [MIT-5.12]
    touches: [MIT-6.4]
---

# What is typical? Mean, median, mode and spread

A news report says the average rent for a flat in your town is €1,645 a
month. You and your friends pay about €1,250 to €1,400, and so does
nearly everyone you know. Is the report wrong? Is the average rent the
rent most people pay?

On this page we:

- find three different "typical" values for one list: the mean, the
  median and the mode
- add `mean`, `median` and `mode` to the toolkit
- see when the three disagree, and why, with rents and with real data
  from 226 places
- ask how spread out a list is: first the range, then "how far from the
  mean, on average", then the standard deviation
- add `std_dev` to the toolkit

> **The space we're in.** A list of numbers, and now and then a list of
> words. Every value in a list counts once. One thing usually goes
> unsaid: "the average" in a newspaper is almost always the mean, and
> the mean is only one of several ways to say what is typical. Your
> toolkit is loaded, with `total`, `largest`, `smallest` and `count_if`
> ready.

## Warm-up

Two questions from earlier pages. The first is from
[A row of numbers](tutorial:a-row-of-numbers#counting-from-the-end),
and the second from
[Doing it again](tutorial:doing-it-again#two-tools-for-your-toolkit).

```question
id: typical-warm-up-1
type: fill-in-the-blank

`goals = [2, 0, 3, 1]`. Then `goals[-1]` is {1}, and `goals[0]` is
{2}.
```

```question
id: typical-warm-up-2
type: multiple-choice
correct: 3

Your toolkit's `total` adds up a list. What is `total([3, 5, 10])`?

- 3
- 10
- 18
- 150
```

## Share it out equally: the mean

Here are the monthly rents of eleven flats in one town, in euro. The
numbers are made up, but the shape is like many Irish towns: most flats
cost about the same, and a few cost far more.

```python exec
id: typical-rents-1
rents = [1350, 1250, 3900, 1200, 1450, 1250, 1300, 2600, 1150, 1400, 1250]
print(len(rents), "flats")
print(total(rents), "euro a month, in all")
```

Picture this. All eleven tenants put their rent into one pot, €18,100,
and then share it out equally. Each one pays the same. How much is that?
Guess before you read on.

That shared-out amount is the *mean*: the total of the values, divided
by how many values there are. In words: add them all up, then divide by
the count. Maths writes the mean of $x_1$ to $x_n$ as $\bar{x}$, said
"x bar":

$$\bar{x} = \frac{1}{n}\sum_{i=1}^{n} x_i = \frac{x_1 + x_2 + \dots + x_n}{n}$$

The sigma is the running total from
[Doing it again](tutorial:doing-it-again#sigma-a-loop-written-by-mathematicians),
and $n$ is the length of the list. So the mean is one line of Python.
Can you write it? Your toolkit has `total`, and Python has `len`.

```python exec
id: typical-toolkit-mean
toolkit: yes
def mean(values):
    """Return the mean of values: their total shared out equally.

    values is a list of at least one number.
    """
    ...
```

```python toolkit-reference
for: typical-toolkit-mean
def mean(values):
    """Return the mean of values: their total shared out equally.

    values is a list of at least one number.
    """
    return total(values) / len(values)
```

The tests below check the "share it out" meaning. If everyone pays the
mean, the pot must hold the same total as before: the mean times the
count gives the total back. Until your `mean` is written, this cell
stops with an error, and the cells below that use `mean` stop too, or
show `None` where a number should be.

```python exec
id: typical-toolkit-mean-tests
assert mean([2, 4, 6]) == 4
assert mean([7]) == 7
assert close_enough(mean(rents) * len(rents), total(rents))
print("mean keeps its promise. The mean rent is", round(mean(rents), 2))
```

```hint
What does `print(mean([2, 4, 6]))` show? If it shows `None`, the
function has no `return` yet. The line to write starts with `return`.
```

The mean rent is €1,645.45, the number in the news report. Now look
back at the list. How many flats cost more than the mean?

```python exec
id: typical-rents-2
def above_the_mean(rent):
    """True when a rent is more than the mean rent."""
    return rent > mean(rents)


print(count_if(rents, above_the_mean), "of", len(rents))
```

Two flats out of eleven. The report was right about the mean, and the
mean is not the rent most people pay. So what else could "typical"
mean?

## The middle one in the line: the median

Picture the eleven tenants standing in a line, from the lowest rent to
the highest. The one in the middle has five people on each side. Their
rent is the *median*: the middle value, when the values are put in
order.

Python's `sorted()` gives back a new list, in order from smallest to
largest. The old list stays as it was, like a slice in
[A row of numbers](tutorial:a-row-of-numbers#a-slice-of-the-week).
With 11 values, the middle one is at index 5: 5 values before it, and 5
after. Before you run the cell, which rent do you think is in the
middle?

```python exec
id: typical-median-1
in_order = sorted(rents)
print(in_order)
print(in_order[5])
```

The median rent is €1,300. That is much closer to what you and your
friends pay.

With an even count, there is no single middle value. For six values,
indexes 0 to 5, the middle falls between index 2 and index 3. Then the
median is the mean of those two: halfway between them.

Here is `median` for your toolkit, written for you. Read it line by
line. `len(in_order) // 2` is the index of the middle, or of the second
of the two middle values. `% 2 == 1` asks whether the count is odd, as
on [Numbers a computer can hold](tutorial:numbers-a-computer-can-hold).

```python exec
id: typical-toolkit-median
toolkit: yes
def median(values):
    """Return the median of values: the middle one when they are in order.

    With an even count, return the mean of the two middle values.
    values is a list of at least one number. It is not changed.
    """
    in_order = sorted(values)
    middle = len(in_order) // 2
    if len(in_order) % 2 == 1:
        return in_order[middle]
    return (in_order[middle - 1] + in_order[middle]) / 2
```

Before you run the tests, work out the second one by hand. Which two
values are in the middle?

```python exec
id: typical-toolkit-median-tests
assert median([3, 1, 2]) == 2
assert median([4, 1, 3, 2]) == 2.5
assert median([7]) == 7
assert median(rents) == 1300
print("median keeps its promise.")
```

For `[4, 1, 3, 2]`, the values in order are 1, 2, 3 and 4. The two in
the middle are 2 and 3, and halfway between them is 2.5. A median does
not have to be one of the values.

## The most common: the mode

A third answer is the value that turns up most often. The *mode* is the
most common value in a list. A list's `.count()` says how many times
one value appears in it. What do you expect?

```python exec
id: typical-mode-1
print(rents.count(1250))
print(rents.count(1300))
```

Three flats cost €1,250, and only one costs €1,300. No rent appears
more than three times, so the mode is €1,250.

The mode has one power the other two lack: it works for words. There is
no mean of shoe sizes written as "UK 7", and no median of bus routes.
But there is a most common one.

Now write `mode` for your toolkit. Go through every value, and keep the
one whose count is highest so far. If two values are equally common,
the promise says to give back the one that comes first in the list.

```python exec
id: typical-toolkit-mode
toolkit: yes
def mode(values):
    """Return the most common value in values, a list of at least one value.

    If several values are equally common, return the one that comes first.
    The values can be numbers or words.
    """
    ...
```

```python toolkit-reference
for: typical-toolkit-mode
def mode(values):
    """Return the most common value in values, a list of at least one value.

    If several values are equally common, return the one that comes first.
    The values can be numbers or words.
    """
    most_common = values[0]
    for value in values:
        if values.count(value) > values.count(most_common):
            most_common = value
    return most_common
```

```hint
after: 8 errors
title: some steps
1. Start with the first value as the most common so far, as `largest`
   starts with the first value as the biggest so far.
2. Go through every value in the list.
3. When `values.count(value)` is bigger than the count of the most
   common so far, keep the new value.
4. After the loop, return the most common so far.

**Think about:** why must the test be `>`, and not `>=`, to keep the
promise about ties?
```

Until your `mode` is written, the tests stop with an error.

```python exec
id: typical-toolkit-mode-tests
assert mode(rents) == 1250
assert mode(["41", "42", "38", "42", "40"]) == "42"
assert mode([3, 5, 5, 3]) == 3
assert mode([9]) == 9
print("mode keeps its promise.")
```

The third test is the tie: 3 and 5 each appear twice, and 3 comes first.

## When the three disagree

Here are the three answers for the rents, side by side. You know them
already. Which one would you call typical?

```python exec
id: typical-disagree-1
print("mean:  ", round(mean(rents), 2))
print("median:", median(rents))
print("mode:  ", mode(rents))
```

The mean is €1,645, the median €1,300, and the mode €1,250. They
disagree because of the two expensive flats, at €2,600 and €3,900. Try
it: change the €3,900 in the first cell of this page to €1,500, and run
the cells again. The median does not move, and the mean falls by more
than €200.

A value far away from the rest is called an *outlier*. A list is
*skewed* when its values are bunched up on one side, with a long tail
of a few values stretching out to the other. The rents are skewed to
the right: bunched at the low end, with a tail of high rents.

Each average has its strengths and its limits:

| | Good at | Weak at |
|---|---|---|
| mean | uses every value; times the count, it gives the total back | a few outliers pull it towards the tail |
| median | outliers barely move it; says what the middle person pays | ignores how far away the other values are |
| mode | works for words too; says what is most common | may be a tie; measurements such as €1,243.50 rarely repeat |

So the report was not wrong. It answered "if the rent were shared out
equally, what would each flat pay?" You asked "what does a typical
tenant pay?", and for skewed data like rents, the median answers that
better. This is why reports on incomes and house prices often give the
median, or both. When you read "the average", it is worth asking which
average, and whether the data is skewed.

## A lopsided world

Skew can go the other way. The life expectancy file from
[A row of numbers](tutorial:a-row-of-numbers#a-real-list-ireland-since-1950)
has a row for each place and year. This line keeps the rows for 2016,
and takes the life expectancy column as a list. The rows are mostly
countries, with a few regions, such as Western Europe and the World as
a whole. For this question, that mix changes little.

Before you run it, guess: is the mean higher or lower than the median
this time?

```python exec
id: typical-world-1
df = await load_csv("life-expectancy.csv")
life_2016 = df[df.year == 2016]["life_expectancy"].tolist()

print(len(life_2016), "places")
print("mean:  ", round(mean(life_2016), 2))
print("median:", median(life_2016))
print("lowest:", smallest(life_2016), " highest:", largest(life_2016))
```

This time the mean, 72.4 years, is lower than the median, 73.6 years.
Four places in five are bunched between 65 and 84 years, and a tail of
places reaching down to about 50 years pulls the mean down. The list is skewed to the left. The median is not pulled, so it
stays with the bunch.

A rule of thumb follows from both examples. The mean moves towards the
tail. If the mean is well above the median, look for a few very high
values. If it is well below, look for a few very low ones.

## How spread out? The range

A typical value is half the story. Here are two bus routes, and how
many minutes late each bus was over one week. The numbers are made up.
Before you run it, look at the two lists. Which route would you rather
take to a job interview?

```python exec
id: typical-spread-1
route_a = [4, 5, 6, 5, 4, 6, 5]
route_b = [0, 10, 2, 5, 9, 1, 8]

print("mean:  ", mean(route_a), mean(route_b))
print("median:", median(route_a), median(route_b))
```

Both routes have a mean of 5 minutes late, and a median of 5. But route
A is always 4 to 6 minutes late, so you can plan for it. Route B might
be on time, or 10 minutes late. The typical values are the same, and
the routes are not. What differs is the *spread*: how far apart the
values are.

The simplest measure of spread is the *range*: the largest value minus
the smallest. The word has a second meaning here. On
[Machines that take a number](tutorial:machines-that-take-a-number#what-goes-in-and-what-comes-out),
a function's range was the outputs it can give. Your toolkit has both
parts of this one.

```python exec
id: typical-spread-2
print("range A:", largest(route_a) - smallest(route_a))
print("range B:", largest(route_b) - smallest(route_b))
```

Route A's range is 2 minutes, and route B's is 10. The range is quick,
and it has a weakness: it uses only two values. One very late bus, on
one day, would make route A's range huge, even if every other day was
the same. We would like a measure that uses every value.

## How far from the mean, on average

Here is one idea. For each bus, how far was it from the mean? Then find
the mean of those distances.

The difference between a value and the mean is its *deviation*. What do
you think the deviations add up to? Guess, then run it.

```python exec
id: typical-deviation-1
centre = mean(route_b)
deviations = []
for minutes in route_b:
    deviations.append(minutes - centre)
print(deviations)
print(total(deviations))
```

They add up to 0. They always do, for any list. The mean is the point
where the values balance: the amounts above it and below it cancel
out. So the mean of the deviations is always 0, and says nothing about
spread.

The fix is to ask how far, and not in which direction. On
[How likely is it?](tutorial:how-likely-is-it#why-the-two-answers-differ)
we met `abs()`, the size of a number without its sign. Before you run
the cell, which route will have the bigger answer?

```python exec
id: typical-deviation-2
def mean_distance(values):
    """Return how far the values are from their mean, on average."""
    centre = mean(values)
    distances = []
    for value in values:
        distances.append(abs(value - centre))
    return mean(distances)


print(round(mean_distance(route_a), 2))
print(round(mean_distance(route_b), 2))
```

Route A's buses are about 0.57 minutes from the mean, on average, and
route B's are about 3.43 minutes. Every bus counts this time, and the
answer says what we wanted: route B is about six times as spread out.
This measure is called the *mean absolute deviation*.

## The standard deviation

There is one more measure of spread, and it is the one you will meet
most often: on a calculator's σ button, in a science report, or in a
spreadsheet. It follows the same idea, with one change. Instead of
taking the size of each deviation with `abs()`, it squares it. A
square is never negative either.

Here it is in words:

1. Find the mean.
2. For each value, find its deviation from the mean, and square it.
3. Find the mean of those squares.
4. Take the square root.

The *standard deviation* is the result: the square root of the mean of
the squared deviations. The step 4 square root undoes the squaring, so
the answer is in minutes again, not minutes squared. Maths writes it
with the Greek letter σ, "sigma", in lower case:

$$\sigma = \sqrt{\frac{1}{n}\sum_{i=1}^{n} (x_i - \bar{x})^2}$$

Read it from the inside out, and you meet the four steps in order:
$\bar{x}$, then $(x_i - \bar{x})^2$, then $\frac{1}{n}\sum$, then
$\sqrt{\phantom{x}}$.

Now write it for your toolkit. `math.sqrt` from
[Machines that take a number](tutorial:machines-that-take-a-number#what-goes-in-and-what-comes-out)
is the square root, and your own `mean` can do step 3 as well as
step 1.

```python exec
id: typical-toolkit-std-dev
toolkit: yes
import math


def std_dev(values):
    """Return the standard deviation of values, a list of at least one number.

    It is the square root of the mean of the squared distances from the mean.
    """
    ...
```

```python toolkit-reference
for: typical-toolkit-std-dev
import math


def std_dev(values):
    """Return the standard deviation of values, a list of at least one number.

    It is the square root of the mean of the squared distances from the mean.
    """
    centre = mean(values)
    squares = []
    for value in values:
        squares.append((value - centre) ** 2)
    return math.sqrt(mean(squares))
```

```hint
after: 8 errors
title: some steps
1. Find the mean of `values` once, before the loop, and give it a name
   such as `centre`.
2. Build a list of squares: start with `[]`, and for each value append
   `(value - centre) ** 2`.
3. Return `math.sqrt(mean(squares))`.

**Think about:** how is this like `mean_distance` above, and which one
line is different?
```

Here are the tests. numpy has its own standard deviation, `np.std`, and
the last two tests check yours against it. Until your `std_dev` is
written, this cell stops with an error.

```python exec
id: typical-toolkit-std-dev-tests
import numpy as np

assert std_dev([5, 5, 5]) == 0
assert std_dev([2, 4, 4, 4, 5, 5, 7, 9]) == 2
assert close_enough(std_dev(route_b), np.std(route_b))
assert close_enough(std_dev(rents), np.std(rents))
print("std_dev keeps its promise.")
print(round(std_dev(route_a), 2), round(std_dev(route_b), 2))
```

Route A's standard deviation is about 0.76 minutes, and route B's about
3.78. They are a little bigger than the mean distances, 0.57 and 3.43,
because squaring makes big deviations count for more. The story is the
same: route B is about five times as spread out.

The first test is worth a look. When every value is the same, nothing
is spread out, and the standard deviation is 0.

One honest note. Some calculators and spreadsheets have a second
standard deviation, often written $s$, that divides by $n - 1$ instead
of $n$. It is used when the list is a sample from a bigger group. For a
long list the two are close. On this page, and in your toolkit, we
divide by $n$.

### Your turn

1. Find the mean and standard deviation of the rents. Is the standard
   deviation big or small compared with the mean? Which flats make it
   so big?
2. Take the two expensive flats out with a slice of `sorted(rents)`,
   and work out both again. Guess first: which one changes more?
3. Find the standard deviation of `life_2016`. Is life expectancy
   more spread out across the world, or across Ireland's years from
   1950 to 2016? Make Ireland's list the way
   [A row of numbers](tutorial:a-row-of-numbers#a-real-list-ireland-since-1950)
   did.

```python exec
id: typical-std-dev-your-turn
# Your spreads here
```

<details class="dl-why"><summary>Why this way?</summary>

This page reached the standard deviation in three steps: the range,
then the mean distance from the mean, then the standard deviation. Many
courses give the formula first, and then practise using it.

Giving the formula first is quicker, and it is what an exam or a
calculator asks for. A reader who only needs the number can get it
right away.

We took the longer road because the formula makes sense only as an
answer to a question. "How far from the mean, on average?" is a
question you can ask in words, and the mean distance answers it. The
standard deviation is the same answer with squares in place of `abs()`.
If you remember the question, you can rebuild the formula.

</details>

## Four questions, looking back

| The question | On this page |
|---|---|
| What is named here? | three typical values for one list, the mean $\bar{x}$, the median and the mode; spread, and the standard deviation $\sigma$ |
| What is promised? | the mean times the count gives the total back; `median`, `mode` and `std_dev` keep the promises in their docstrings, ties included |
| What happens when? | the median sorts first, then takes the middle; the standard deviation runs four steps in order, read from the inside of its formula out |
| What does this space let us do? | the mean and median need numbers, and the mode works for words too; in skewed data the averages disagree, and asking "which average?" is always allowed |

## What we have now

| Term or tool | What it means |
|---|---|
| mean, $\bar{x}$ | the total shared out equally: $\frac{1}{n}\sum x_i$ |
| median | the middle value when the values are in order; with an even count, halfway between the two middle ones |
| `sorted()` | a new list, in order from smallest to largest |
| mode, `.count()` | the most common value; how many times one value is in a list |
| outlier | a value far away from the rest |
| skewed | bunched on one side, with a tail stretching out on the other; the mean moves towards the tail |
| spread, range | how far apart the values are; the largest minus the smallest |
| deviation | a value minus the mean; the deviations always add up to 0 |
| mean absolute deviation | how far the values are from the mean, on average |
| standard deviation, $\sigma$ | the square root of the mean of the squared deviations |
| `mean`, `median`, `mode`, `std_dev` | your four new toolkit tools |

The practice page is next. After it,
[Kinds of data, and honest charts](tutorial:kinds-of-data-and-honest-charts)
draws these lists as pictures, and asks when a picture tells the truth.

For another route through the same ideas, the integrated course has
[Statistics: averages, spread and frequency](tutorial:making-sense-of-data).
