---
title: "Statistics: averages, spread and frequency"
year: "2026-2027"
version: 2026.09.26.1
worlds:
  exoplanets: Planets around other stars, and the ways they were found.
  dinosaurs: Dinosaurs and their fossils, what has been found, where, and how old it is.
  book-characters: The people in six novels, chapter by chapter.
  games-of-chance: Dice, cards and coins, and the games people play with them.
datasets: [exoplanets, dinosaur-genera, book-chapters]
covers:
  measures-of-central-tendency:
    covers: [MIT-5.12]
  when-the-mean-misleads:
    covers: [MIT-5.13]
  measures-of-spread:
    covers: [MIT-5.12]
  data-types:
    covers: [MIT-5.9]
  frequency-distributions:
    covers: [MIT-5.11, MIT-5.10]
---

# Statistics: averages, spread and frequency

How big is a typical planet around another star? Astronomers have
confirmed more than six thousand of them, and NASA keeps a list. This
cell loads the list, as it stood on {{snapshot: exoplanets}}, and shows
its first five rows.

```python exec
id: data-first-look
planets = await load_csv("exoplanets.csv")
print(len(planets), "planets")
print(planets.head())
```

Each row is one planet. The columns say its name, the year it was
announced, how it was found, the days it takes to go round its star once
(`orbit_days`), its radius in Earth radii (`radius_earths`: 1 is the
size of the Earth, and Jupiter is about 11), and its distance from us in
light years.

A *dataset* is one collection of data that belongs together, like this
one. *Statistics* is the part of mathematics that summarises, describes
and explains data. This page asks what a typical planet looks like, how
much the planets differ, and what shape their sizes make. Before any of
that, it asks where the list came from.

## Where the data comes from

Every number in the file was measured by somebody, with some instrument,
and published in a paper. The NASA Exoplanet Archive gathers them. So the
file is not a list of the planets there are. It is a list of the planets
that our instruments have been able to find.

The Earth is about 1 Earth radius across, and takes 365 days to go round
the Sun. How many planets in the file are about the Earth's size, with a
year somewhere between 200 and 500 days?

```python exec
id: data-who-is-missing
earth_sized = planets[(planets.radius_earths >= 0.8) & (planets.radius_earths <= 1.25)]
earth_like_year = earth_sized[(earth_sized.orbit_days >= 200) & (earth_sized.orbit_days <= 500)]
print(len(earth_sized), "planets about the size of the Earth")
print(len(earth_like_year), "of them with a year of 200 to 500 days")
```

```predict
type: number

How many Earth-sized planets with a year of 200 to 500 days are in the
file? The last number printed is that count.
```

None. There are 507 planets the size of the Earth, but nearly all of
them go round their stars in a few days. That is not because planets
like the Earth are rare. Most of the planets in the file were found by
*transit*: a telescope watches a star, and sees it dim slightly when a
planet crosses in front of it. A small planet dims its star very little,
and a planet with a long year crosses only once a year, so a telescope
has to watch for years to see it twice. Small planets in long orbits are
the hardest kind to find.

That is the difference between a population and a sample. The
*population* is everything we want to know about: here, every planet
around every star. A *sample* is the part of it we have data on. When
the way a sample is taken makes some members more likely to be in it
than others, the sample has a *sampling bias*. Every dataset on this page
has one, and asking what it is comes before any average.

Three questions to ask of any dataset:

- Who collected it, and how?
- Who or what is missing from it, and why?
- Is it all of the population, or a sample? If a sample, how was it
  chosen?

## Measures of central tendency

A *measure of central tendency* is a single number that describes the
centre, or typical value, of a dataset. There are three common ones.

The *mean* is the ordinary average: add up all the values and divide by
how many there are. With $n$ values $x_1, x_2, \ldots, x_n$:

$$\bar{x} = \frac{1}{n}\sum_{i=1}^{n} x_i$$

We write the mean as $\bar{x}$ and say "x bar"; the $\sum$ sign means
"add up". The mean of 2, 4 and 9 is $\frac{15}{3} = 5$.

The *median* is the middle value when the data is sorted. The median of
2, 4 and 9 is 4. With an even number of values there are two in the
middle, and the median is their mean: the median of 2, 4, 9 and 11 is
6.5.

The *mode* is the value that appears most often. The mode of 3, 5, 5
and 8 is 5.

The mean is one line. Can you write `median(data)`? Python's `sorted()`
gives back a new sorted list, and leaves the old one as it was.

```python exec
id: data-median
def mean(data):
    """The mean: add up the values, and share the total out equally."""
    return sum(data) / len(data)


def median(data):
    """The middle value once the data is sorted."""
    # Your code here


print(median([2, 4, 9]), median([2, 4, 9, 11]))
```

```inputs
median([2, 4, 9])
median([2, 4, 9, 11])
median([7])
median([3, 1, 2, 5])
```

```hint
Sort the data first. With `n` values, the middle position is `n // 2`.
When `n` is even, `n % 2` is 0, and the median is the mean of the values
at positions `n // 2 - 1` and `n // 2`.
```

```solution
def mean(data):
    """The mean: add up the values, and share the total out equally."""
    return sum(data) / len(data)


def median(data):
    """The middle value once the data is sorted."""
    ordered = sorted(data)
    n = len(ordered)
    middle = n // 2
    if n % 2 == 1:
        return ordered[middle]
    return (ordered[middle - 1] + ordered[middle]) / 2


print(median([2, 4, 9]), median([2, 4, 9, 11]))
---
`n // 2` is the middle position for an odd count: 1 for three values,
since positions start at 0. For an even count it is the second of the
two middle values, so the first is one before it.
```

And `mode(data)`? A dictionary from
[Looking things up by name](tutorial:looking-things-up-by-name) can count
how often each value appears.

```python exec
id: data-mode
def mode(data):
    """The value that appears most often. On a tie, the one seen first."""
    # Your code here


print(mode([3, 5, 5, 8]))
```

```inputs
mode([3, 5, 5, 8])
mode(["Transit", "Imaging", "Transit"])
mode([1, 2, 2, 1])
```

```hint
Count first: for each value, add 1 to `counts[value]`, starting it at 0
the first time. Then go through the counts, and keep the value with the
largest count so far.
```

```solution
def mode(data):
    """The value that appears most often. On a tie, the one seen first."""
    counts = {}
    for value in data:
        if value not in counts:
            counts[value] = 0
        counts[value] = counts[value] + 1
    best = data[0]
    for value in counts:
        if counts[value] > counts[best]:
            best = value
    return best


print(mode([3, 5, 5, 8]))
---
A dictionary keeps its keys in the order they were first added, so on a
tie the value seen first wins: `mode([1, 2, 2, 1])` is 1. A tie is worth
reporting, not hiding; `statistics.multimode` gives every value that
ties.
```

Now the three on the planets' radii. Fifty planets have no radius in the
file; `dropna()` leaves them out, and `tolist()` makes a plain list. The
missing fifty are part of the answer too.

```python exec
id: data-radius-averages
radii = planets.radius_earths.dropna().tolist()
print(len(radii), "radii")
print("mean  ", round(mean(radii), 2))
print("median", median(radii))
print("mode  ", mode(radii))
```

```predict
Which of the three will be largest?

- The mean
  - A few very large planets pull the total up.
- The median
  - The middle planet is a big one.
- The mode
  - The commonest size is the typical size.
```

The mean is 5.88 Earth radii, the median 2.87, and the mode 12.8. Three
"typical" sizes, and none of them agrees with another. The mode comes
from rounding: radii are given to two decimal places, and 59 planets
happen to share 12.8. For measured data, the most repeated rounded value
says little. The histogram, further down, shows why the mean and median
disagree.

## When the mean misleads

The planets' years are further apart still. This cell works out the
mean and median of `orbit_days`, and then again without the single
longest orbit.

```python exec
id: data-orbit-averages
orbits = planets.orbit_days.dropna().tolist()
print("mean  ", round(mean(orbits)), " median", median(orbits))

without_longest = sorted(orbits)[:-1]
print("mean  ", round(mean(without_longest)), " median", median(without_longest))
```

```predict
When one planet of 6,019 is taken away, which moves more?

- The mean
  - Every value adds its full size to the total.
- The median
  - The median is the middle, and the middle has changed.
- Neither much
  - One planet in six thousand cannot matter.
```

The mean falls from 71,126 days to 4,338, and the median hardly moves
from 10.75. The longest orbit belongs to COCONUTS-2 b, a planet so far
from its star that one year there lasts about a million of ours:
402,000,000 days. That one value was most of the total.

An *outlier* is a value far away from the rest of the data. A measure is
*robust* when an outlier hardly changes it: the median is robust, and
the mean is not. Data is *skewed* when it has a long tail of values on
one side, as the orbits do: nearly half the planets go round in under 10
days, and a few take centuries or more. For skewed data, the median is
usually the better answer to "what is typical?". The mean answers a
different question, what each would get if the total were shared out
equally, and it is the right one when the total matters.

## Measures of spread

Two datasets can have the same centre and look very different: the
values in one close together, in the other far apart. A *measure of
spread* is a number that says how spread out the values are.

The *range* is the largest value minus the smallest. It is simple, and it
depends on only two values, both of them extremes.

The *standard deviation* measures how far the values are from the mean,
in a typical case. It takes four steps:

1. Find how far each value is from the mean.
2. Square each distance, which makes them all positive.
3. Find the mean of the squares.
4. Take the square root, to get back to the units of the data.

$$\sigma = \sqrt{\frac{1}{n}\sum_{i=1}^{n}(x_i - \bar{x})^2}$$

We write it $\sigma$, the Greek letter sigma. For 2, 4 and 9, whose
mean is 5, the distances are $-3$, $-1$ and $4$, the squares 9, 1 and 16,
their mean $\frac{26}{3} \approx 8.67$, and its square root about 2.94.
Some books divide by $n - 1$ in place of $n$; that is the *sample
standard deviation*, for when the data is a sample and the spread of
the whole population is what we want to estimate. This page divides by
$n$.

Can you write `std_dev(data)`?

```python exec
id: data-std-dev
def mean(data):
    """The mean: add up the values, and share the total out equally."""
    return sum(data) / len(data)


def std_dev(data):
    """How far the values are from their mean, in a typical case."""
    # Your code here


print(round(std_dev([2, 4, 9]), 2))
```

```inputs
round(std_dev([2, 4, 9]), 2)
round(std_dev([2, 4, 4, 4, 5, 5, 7, 9]), 2)
std_dev([5, 5, 5])
```

```hint
Work out the mean once, before the loop. Then add up
`(value - centre) ** 2` for every value, divide by how many there are,
and take the square root with `** 0.5`.
```

```solution
def mean(data):
    """The mean: add up the values, and share the total out equally."""
    return sum(data) / len(data)


def std_dev(data):
    """How far the values are from their mean, in a typical case."""
    centre = mean(data)
    total = 0
    for value in data:
        total = total + (value - centre) ** 2
    return (total / len(data)) ** 0.5


print(round(std_dev([2, 4, 9]), 2))
---
2.94, then 2.0 for the second list, and 0.0 when every value is the
same: no spread at all. Working out the mean inside the loop would give
the same answer, and do the same work once for every value.
```

```python exec
id: data-radius-spread
print("range  ", round(max(radii) - min(radii), 2))
print("std dev", round(std_dev(radii), 2))
```

The radii run from 0.31 to 87.21 Earth radii, a range of 86.9, set by
two unusual planets. The standard deviation, 5.43, uses every planet.
Beside a mean of 5.88, it says the sizes vary about as much as the mean
itself: these planets are nothing like one size.

## Data types

Data comes in kinds, and not every tool suits every kind. (These kinds
are not Python's types, such as `int` and `str`.)

- *Categorical* data, also called *nominal*, is labels with no order:
  the `method` column, or a planet's name.
- *Ordinal* data is labels with an order but unequal steps: a star
  rating, or small, medium and large.
- *Discrete* data is counted, so it comes in whole numbers: the number
  of planets found in a year.
- *Continuous* data is measured, and can be any value in a range:
  `radius_earths`, `orbit_days` and `distance_ly`.

| Kind of data | Example | Mode | Median | Mean |
|---|---|---|---|---|
| Categorical | how a planet was found | yes | no | no |
| Ordinal | a star rating | yes | yes | people disagree |
| Discrete | planets found in a year | yes | yes | yes |
| Continuous | a planet's radius | yes | yes | yes |

```question
id: data-kinds
type: fill-in-the-blank

- How a planet was found (`method`) is {categorical|ordinal|continuous} data.
- A planet's radius is {continuous|discrete|categorical} data.
- The number of planets found in one year is {discrete|continuous|ordinal} data.
- A planet's name is {categorical|ordinal|discrete} data, even though some names have numbers in them.
```

For categorical data, the mode is the only average there is: `mode` on
the `method` column gives Transit. A mean of the methods has no meaning,
and Python refuses to add up words. But give it numbers that are labels,
such as the numbers on football shirts, and it will work out their mean
without complaint: nothing in the data stops a meaningless average.

## Frequency distributions

The *frequency* of a value is how many times it appears. A *frequency
distribution* lists the values, or groups of values, with how often each
appears. For measured data, where hardly any two values are the same, we
split the range into equal groups called *bins*, and count the values in
each. A *histogram* draws the counts: one bar for each bin, as tall as
its count, with no gaps, since each bin starts where the last one ends.

matplotlib is a Python module for drawing charts. `import
matplotlib.pyplot as plt` loads it under the short name `plt`, and
`plt.hist` sorts the values into bins and draws the bars. Where do you
expect the tallest bars to be?

```python exec
id: data-radius-histogram
import matplotlib.pyplot as plt

small_enough = [r for r in radii if r <= 25]
plt.hist(small_enough, bins=50, edgecolor="black")
plt.axvline(mean(radii), color="red", linestyle="--", label="mean")
plt.axvline(median(radii), color="green", linestyle=":", label="median")
plt.xlabel("radius, in Earth radii")
plt.ylabel("planets")
plt.legend()
print(len(radii) - len(small_enough), "planets larger than 25 Earth radii are left off the chart")
```

```predict
What shape will the histogram have?

- One hump, around the mean
  - A mean is where the data gathers.
- Two humps, one of small planets and one of large
  - There might be two different kinds of planet.
- Tallest at the left, falling away to the right
  - Small things are usually commonest.
```

Two humps: a crowd of small planets, one to four times the Earth's
size, and a second crowd near Jupiter's size, about 11 to 14. The mean,
the red line, falls in the valley between them, where fewer than one
planet in twenty sits. It is a size hardly any planet has. A histogram
with one peak is *unimodal*; with two, *bimodal*. Two humps usually mean
two kinds of thing mixed together. Here they are small planets, rocky or
gassy, and giants like Jupiter.

A histogram is *symmetric* when its two halves are mirror images, and
skewed when one side has a long tail. When you look at one, ask: one
peak or more? Symmetric, or a long tail? Gaps, or outliers far away?

The number of bins changes the picture. Can you draw the same histogram
with 5 bins, and then with 200? With too few, what disappears? With too
many, what gets in the way?

```python exec
id: data-bins
import matplotlib.pyplot as plt

plt.hist(small_enough, bins=5, edgecolor="black")
plt.xlabel("radius, in Earth radii")
plt.ylabel("planets")
```

With 5 bins the two humps merge, and the valley vanishes. With 200, the
bars get so thin that chance bumps look like features. There is no
right number of bins; choosing one is a judgement, and trying several is
how to make it.

## Go further: percentiles and box plots

The median splits the data in half. *Percentiles* split it more finely:
the 25th percentile is the value a quarter of the data is below, and the
75th, the value three quarters is below. Those two are the *quartiles*,
and the distance between them, the *interquartile range*, is a measure
of spread that, like the median, ignores the extremes. For the radii, the
quartiles are 1.85 and 11.99.

A *box plot* draws them. The box runs from the 25th to the 75th
percentile, with a line at the median; the whiskers reach out to the
data that is not far from the box, and anything beyond them is drawn as
a dot. Box plots are good for comparing groups side by side. Here are
the planets' distances from us, for each of the four commonest ways of
finding them:

```python exec
id: data-box-plots
import matplotlib.pyplot as plt

methods = ["Radial Velocity", "Imaging", "Transit", "Microlensing"]
distances = []
for method in methods:
    found_this_way = planets[planets.method == method]
    distances.append(found_this_way.distance_ly.dropna().tolist())
    print(method, "median", median(distances[-1]), "light years")

plt.boxplot(distances)
plt.xticks([1, 2, 3, 4], methods)
plt.yscale("log")
plt.ylabel("distance from us, in light years")
```

Each method has its own reach. The wobble of a star (radial velocity)
and a direct photograph (imaging) work best on stars close by, a few
hundred light years away. Transits reach further. Microlensing, which sees a
distant star brighten as another star and its planet pass in front of it
and bend its light, finds planets at a median of about 20,000 light
years. The y axis is
a *logarithmic scale*: each step up multiplies by 10, so all four fit on
one chart.

## Go further: the binomial

Flip ten coins and count the heads. Do it 10,000 times, and draw how
often each count came up.

```python exec
id: data-binomial
import random
import matplotlib.pyplot as plt

counts = [0] * 11
for trial in range(10_000):
    heads = 0
    for flip in range(10):
        if random.random() < 0.5:
            heads = heads + 1
    counts[heads] = counts[heads] + 1

plt.bar(range(11), counts)
plt.xlabel("heads in ten flips")
plt.ylabel("times in 10,000 trials")

commonest = 0
for heads in range(11):
    if counts[heads] > counts[commonest]:
        commonest = heads
print("The commonest count is", commonest)
```

```predict
type: number

Which number of heads will come up most often?
```

Five heads, about a quarter of the time, and the counts fall away on
both sides. [Counting](tutorial:counting-carefully) says why: there are
$2^{10} = 1{,}024$ equally likely ways ten flips can land, and $C(10, 5)
= 252$ of them have five heads, so the chance is $\frac{252}{1{,}024}
\approx 0.246$. Ten heads is $\frac{1}{1{,}024}$.

This is the *binomial distribution*: the number of successes in $n$
independent trials, each with the same chance $p$. The chance of exactly
$k$ successes is

$$P(k) = C(n, k) \, p^k (1-p)^{n-k}$$

$C(n, k)$ counts the ways, and $p^k (1-p)^{n-k}$ is the chance of any one
of them, by the multiplication rule for independent events. For the
coins, $p = \frac{1}{2}$, so every way has chance $\frac{1}{2^{10}}$.

## Your world

A question from the world you chose, with the tools from this page.

<div class="dl-world" data-world="exoplanets">

The years in which planets were announced: what are the mean, median and
mode of the `discovered` column? What does the mode year say, and which
average would you quote for "when was a typical planet found"?

```python exec
id: data-your-world--exoplanets
years = planets.discovered.tolist()
print(min(years), "to", max(years))
```

```hint
The functions `mean`, `median` and `mode` from above work on any list.
```

```solution
{{include: setup/data/functions.py}}

planets = await load_csv("exoplanets.csv")
years = planets.discovered.tolist()
print(min(years), "to", max(years))
print("mean", round(mean(years), 1), " median", median(years), " mode", mode(years))
---
With the copy saved on {{snapshot: exoplanets}}: the mean is about
2017.3, the median 2016, and the mode 2016, when more than 1,500
planets were announced, 1,284 of them from the Kepler telescope on one
day in May. The years are skewed: a long tail back to 1992, the first
year in the file, and a crowd in the last ten years. The median is the
fairer "typical year", and the mode here is not typical at all: it marks
one announcement.
```

</div>

<div class="dl-world" data-world="dinosaurs">

The file `dinosaur-genera.csv` has one row for each named dinosaur genus,
and `named_by` says who named it and when, such as "Osborn 1905". A few
are in brackets, such as "(Stromer 1931)", which means the animal was
first described under another name; `strip("()")` takes the brackets off
the ends. When was a typical genus named? Work out the mean and the median year. What
do they say about where this data comes from?

```python exec
id: data-your-world--dinosaurs
genera = await load_csv("dinosaur-genera.csv")
years = []
for name in genera.named_by:
    years.append(int(name.strip("()")[-4:]))
print(len(years), "genera, named from", min(years), "to", max(years))
```

```hint
`name.strip("()")[-4:]` is the last four characters of the text, once
the brackets are off: the year. `mean`
and `median` from above work on the list.
```

```solution
{{include: setup/data/functions.py}}

genera = await load_csv("dinosaur-genera.csv")
years = []
for name in genera.named_by:
    years.append(int(name.strip("()")[-4:]))
print(len(years), "genera, named from", min(years), "to", max(years))
print("mean", round(mean(years)), " median", median(years))
recent = [year for year in years if year >= 2000]
print(len(recent), "named in 2000 or later")
---
With the copy saved on {{snapshot: dinosaur-genera}}: the mean is about
1990 and the median 2007. Half of all the genera in the file were named
since 2007, and 1,014 of the 1,615 since 2000. The oldest,
*Megalosaurus*, dates from 1822. The years are skewed, with a long tail
back to the 1800s, which pulls the mean nearly twenty years earlier than
the median. This data is not a fixed list of dinosaurs: it is what
people have found and named so far, and it grows every year.
```

</div>

<div class="dl-world" data-world="book-characters">

The file `book-chapters.csv` counts the words in every chapter of six
novels. Which book has the most even chapters, by standard deviation?
Does the answer change if you compare each book's standard deviation
with its mean?

```python exec
id: data-your-world--book-characters
chapters = await load_csv("book-chapters.csv")
for book in chapters.book.unique():
    words = chapters[chapters.book == book].words.tolist()
    print(book, len(words), "chapters")
```

```hint
For each book, `std_dev(words)` and `mean(words)`. Dividing the first by
the second gives the spread as a share of the mean.
```

```solution
{{include: setup/data/functions.py}}

chapters = await load_csv("book-chapters.csv")
for book in chapters.book.unique():
    words = chapters[chapters.book == book].words.tolist()
    spread = std_dev(words)
    print(book, " mean", round(mean(words)), " sd", round(spread),
          " sd / mean", round(spread / mean(words), 2))
---
*A Princess of Mars* has the most even chapters both ways: a standard
deviation of 771 words, 0.33 of its mean. *The Lost World* has the
largest standard deviation, 1,614, but its chapters are also the longest,
nearly 4,800 words on average; as a share of the mean, 0.34, it is
nearly as even as *A Princess of Mars*. The least even, as a share, is
*The War of the Worlds*, at 0.53. A spread means more beside the size of
the values it is spread around.
```

</div>

<div class="dl-world" data-world="games-of-chance">

A game starts when you roll a six. How many rolls does it take? This
cell plays it for 10,000 players. What are the mean, median and mode of
the number of rolls, and which would you tell a new player to expect?

```python exec
id: data-your-world--games-of-chance
import random


def rolls_until_six():
    """Roll a die until it shows a six, and say how many rolls it took."""
    rolls = 1
    while random.randint(1, 6) != 6:
        rolls = rolls + 1
    return rolls


waits = []
for player in range(10_000):
    waits.append(rolls_until_six())
print("The longest wait:", max(waits), "rolls")
```

```hint
The functions `mean`, `median` and `mode` from above work on `waits`.
```

```solution
{{include: setup/data/functions.py}}

import random


def rolls_until_six():
    """Roll a die until it shows a six, and say how many rolls it took."""
    rolls = 1
    while random.randint(1, 6) != 6:
        rolls = rolls + 1
    return rolls


waits = []
for player in range(10_000):
    waits.append(rolls_until_six())
print("The longest wait:", max(waits), "rolls")
print("mean", round(mean(waits), 2), " median", median(waits), " mode", mode(waits))
---
The mean is about 6, the median 4, and the mode 1. The commonest wait
is one roll, and yet the typical player waits several, and a few wait
thirty or more. The waits are skewed, with a long tail of unlucky
players. "Six rolls on average" is true, and "most players start within
six rolls" is true too, about two players in three, but a player who is
told only the mean will think a four-roll wait is lucky.
```

</div>

## Looking back

On this page, the mean of the planets' radii was a size almost no
planet has, and the mean orbit was set by one planet in six thousand.
Before you quote an average of anything, can you say which of the three
you would choose for the planets' orbits, and the one sentence you would
put beside it?

The next page, [Charts](tutorial:pictures-worth-numbers), draws data in
more ways, and shows how a chart can tell the truth about it, or not.

## Where to read more

Josh Starmer (StatQuest) (2019). *Calculating the Mean, Variance and
Standard Deviation, Clearly Explained!!!*
<https://www.youtube.com/watch?v=SzZ6GpcfoQY>. The same measures this
page builds as functions, worked through by hand first.

CrashCourse (2018). *Measures of Spread: Crash Course Statistics #4.*
<https://www.youtube.com/watch?v=R4yfNi_8Kqw>. The range, the standard
deviation and other measures of spread, and what they tell us that the
mean does not. About eleven minutes.

NASA Exoplanet Archive. *Exoplanet and Candidate Statistics.*
<https://exoplanetarchive.ipac.caltech.edu/docs/counts_detail.html>.
The archive's own running counts, by method and by year: the same data
this page summarises, kept up to date.
