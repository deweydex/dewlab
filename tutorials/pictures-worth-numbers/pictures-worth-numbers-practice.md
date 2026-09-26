---
title: "Charts: choosing the right chart for your data — Practice"
practice_for: pictures-worth-numbers
year: "2026-2027"
version: 2026.09.26.1
worlds:
  exoplanets: Planets around other stars, and the ways they were found.
  dinosaurs: Dinosaurs and their fossils, what has been found, where, and how old it is.
  book-characters: The people in six novels, chapter by chapter.
  games-of-chance: Dice, cards and coins, and the games people play with them.
datasets: [exoplanets, dinosaur-finds, book-characters]
---

# Charts: choosing the right chart for your data — Practice

Here are problems on choosing, reading and making charts, and three from
earlier pages. The plotting takes a few lines of code each time. The
skill is to choose well, and to notice what a chart makes you believe.

## Tools

`bars()` draws a labelled bar chart, and returns its axes, so you can
change the chart afterwards.

```python exec
id: tools-1
import matplotlib.pyplot as plt


def bars(labels, values, title="", ylabel=""):
    """Draw a labelled bar chart, and give back its axes."""
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(labels, values)
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.grid(axis="y", alpha=0.3)
    return ax


bars(["Mon", "Tue", "Wed", "Thu", "Fri"], [12, 19, 8, 22, 15],
     title="Support tickets", ylabel="tickets")
```

## Choosing a chart

```question
id: charts-which-chart
type: fill-in-the-blank

- Sales in each of six regions: a {bar chart|line chart|histogram|scatter plot}.
- Visits to a website on each day of a year: a {line chart|bar chart|histogram|scatter plot}.
- Height against weight for 200 people: a {scatter plot|line chart|bar chart|histogram}.
- The spread of exam marks in a class: a {histogram|bar chart|line chart|scatter plot}.
- The market share of four companies: a {bar chart|pie chart|line chart|histogram}.
```

**1.** Why a bar chart, not a pie chart, for the last one?

<details class="dl-answer"><summary>answer</summary>

A pie chart is the traditional answer, and it works less well. People
are good at comparing lengths and bad at comparing angles. Two slices of
23% and 27% look alike, but two bars of those heights are plainly
different.

</details>

**2.** When does a line chart not fit?

<details class="dl-answer"><summary>answer</summary>

When the x axis has no meaningful order. Join the sales of Leinster,
Munster and Connacht with a line, and it suggests that Munster lies
between the other two in some quantity. It does not. A line says "these
points are on a path". If there is no path, the chart is telling a lie.

</details>

**3.** What is the difference between a bar chart and a histogram, and
how can you tell them apart at a glance?

<details class="dl-answer"><summary>answer</summary>

A bar chart compares categories. A histogram shows how one measured
quantity is spread, in bins. The bars of a bar chart have gaps, because
the categories are separate. The bars of a histogram touch, because each
bin starts where the last one ends.

</details>

**4.** You have five years of monthly sales for three products. What do
you plot?

<details class="dl-answer"><summary>answer</summary>

Plot three lines on one pair of axes, with a legend. Three separate charts
would each be easy to read and useless for comparing, and comparing is
the point. If the products sell on very different scales, plot each
one's percentage change instead.

</details>

## Reading charts

**5.** A news graphic shows two planets as circles. One is labelled
"twice the size", and is drawn twice as wide. How much bigger does it
look?

<details class="dl-answer"><summary>answer</summary>

About four times, because twice as wide and twice as tall is four times
the area. The eye judges area. Drawn as spheres, it would suggest eight
times. Pictures sized by a number exaggerate it. A bar, which grows in
one direction only, does not.

</details>

**6.** Two variables have a correlation of 0. Can they still be related?
Here are the points on $y = x^2$, for $x$ from $-3$ to $3$.

```python exec
id: charts-zero-correlation
import statistics

xs = list(range(-3, 4))
ys = [x * x for x in xs]
print(ys)
print("correlation:", statistics.correlation(xs, ys))
```

```predict
type: number
tolerance: 0.05

What correlation will it print?
```

<details class="dl-answer"><summary>why</summary>

It prints 0.0, and yet $y$ is exactly $x^2$, a perfect relationship.
Correlation measures only a straight-line relationship, and this curve
goes down and then up by the same amount, so the straight-line parts
cancel. A quick plot answers what the number cannot.

</details>

## Making them

**7.** Can you plot $y = x^2$ and $y = 2^x$ on one pair of axes, for $x$
from 0 to 10, with a legend? Where do they cross?

```python exec
id: charts-two-curves
import matplotlib.pyplot as plt

xs = list(range(11))
```

```hint
Use `plt.plot(xs, [x ** 2 for x in xs], label="x squared")`, the same
for `2 ** x`, then `plt.legend()`.
```

```solution
import matplotlib.pyplot as plt

xs = list(range(11))
plt.plot(xs, [x ** 2 for x in xs], label="x squared")
plt.plot(xs, [2 ** x for x in xs], label="2 to the power x")
plt.legend()
plt.grid(alpha=0.3)
---
They cross at $x = 2$ and $x = 4$, and after that $2^x$ grows much
faster than $x^2$: 1,024 against 100 at $x = 10$. A curve where $x$ is
the power is *exponential*. An algorithm whose running time grows like
that soon stops being usable at all.
```

**8.** Now add `plt.yscale("log")` to the same chart. What changes?

<details class="dl-answer"><summary>answer</summary>

$2^x$ becomes a straight line, and $x^2$ bends and flattens. On a
log scale, exponential growth is a straight line, and its steepness says
how fast it grows. The $x^2$ line also loses its first point. 0 has
no place on a log scale, since each step down divides by 10 and never
reaches 0. Label a log axis clearly, or every difference on it will be
misread.

</details>

**9.** Can you write `scatter(xs, ys, title, xlabel, ylabel, ax=None)`,
which draws a labelled scatter plot on its own, or onto an existing
chart when it is given one?

```python exec
id: charts-scatter-function
import matplotlib.pyplot as plt


def scatter(xs, ys, title="", xlabel="", ylabel="", ax=None):
    """A labelled scatter plot. Pass ax to draw onto an existing chart."""
    # Your code here


fig, (left, right) = plt.subplots(1, 2, figsize=(9, 4))
scatter([1, 2, 3], [2, 4, 5], title="Left", ax=left)
scatter([1, 2, 3], [5, 3, 1], title="Right", ax=right)
```

```hint
When `ax` is `None`, make one with `fig, ax = plt.subplots()`. Then use
`ax.scatter`, `ax.set_title`, `ax.set_xlabel` and `ax.set_ylabel`, and
return `ax`.
```

```solution
import matplotlib.pyplot as plt


def scatter(xs, ys, title="", xlabel="", ylabel="", ax=None):
    """A labelled scatter plot. Pass ax to draw onto an existing chart."""
    if ax is None:
        fig, ax = plt.subplots()
    ax.scatter(xs, ys)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    return ax


fig, (left, right) = plt.subplots(1, 2, figsize=(9, 4))
scatter([1, 2, 3], [2, 4, 5], title="Left", ax=left)
scatter([1, 2, 3], [5, 3, 1], title="Right", ax=right)
---
`ax=None` makes the function reusable, not only shorter. It can draw a
chart of its own, or one panel of a larger figure.
Returning `ax` lets whoever called it keep changing the chart.
```

## Your world

**10.** Each world asks a question that a chart can answer.

<div class="dl-world" data-world="exoplanets">

What share of each year's new planets was found by transit? Draw it as a
line chart, from 1995 on.

```python exec
id: charts-world--exoplanets
import matplotlib.pyplot as plt

planets = await load_csv("exoplanets.csv")
recent = planets[planets.discovered >= 1995]
transit_share = (recent.method == "Transit").groupby(recent.discovered).mean()
print(transit_share.loc[2014:2018].round(2))
```

```hint
`transit_share.index` is the years and `transit_share.values` the
shares. `plt.plot` joins them.
```

```solution
import matplotlib.pyplot as plt

planets = await load_csv("exoplanets.csv")
recent = planets[planets.discovered >= 1995]
transit_share = (recent.method == "Transit").groupby(recent.discovered).mean()
print(transit_share.loc[2014:2018].round(2))

plt.plot(transit_share.index, transit_share.values, marker="o")
plt.ylim(0, 1)
plt.xlabel("year announced")
plt.ylabel("share found by transit")
---
Almost no planets were found by transit before 2004. Then the share
climbs unevenly to more than 0.9 in 2014 and 2016, Kepler's years, and
has been between about 0.5 and 0.8 since. The y axis runs from 0 to 1
because a share can only be in that range. If the library chose, it
would stretch the wiggles after 2016 to fill the frame.
```

</div>

<div class="dl-world" data-world="dinosaurs">

Where on Earth are dinosaur fossils found? Draw a histogram of the finds'
latitudes, from the South Pole at −90 to the North Pole at 90. What share
are north of the equator?

```python exec
id: charts-world--dinosaurs
import matplotlib.pyplot as plt

finds = await load_csv("dinosaur-finds.csv", keep_default_na=False)
print(len(finds), "finds")
```

```hint
`plt.hist(finds.lat, bins=36, range=(-90, 90))` gives bins five degrees
wide. `(finds.lat > 0).mean()` is the share north of the equator.
```

```solution
import matplotlib.pyplot as plt

finds = await load_csv("dinosaur-finds.csv", keep_default_na=False)
print(len(finds), "finds")
print("north of the equator:", round((finds.lat > 0).mean(), 2))

plt.hist(finds.lat, bins=36, range=(-90, 90))
plt.xlabel("latitude, degrees")
plt.ylabel("finds")
---
With the copy saved on {{snapshot: dinosaur-finds}}, 0.88 of the finds
are north of the equator, most of them between about 30° and 55° north,
the latitudes of the United States, Canada, Europe, Mongolia and northern
China. Dinosaurs lived all over the world. The histogram shows where the
right rock is exposed, and where palaeontologists have worked longest.
The continents have also moved since, so a find's latitude today is not
where the animal lived.
```

</div>

<div class="dl-world" data-world="book-characters">

Choose one of the six books. Who is named most often in it? Draw a
horizontal bar chart of each person's total mentions, largest at the top.
Is the most named person the main character?

```python exec
id: charts-world--book-characters
import matplotlib.pyplot as plt

characters = await load_csv("book-characters.csv")
print(list(characters.book.unique()))
book = characters[characters.book == "frankenstein"]
```

```hint
`book.groupby("character").mentions.sum().sort_values()` gives the
totals, smallest first. `plt.barh` draws the first at the bottom, so the
largest is at the top.
```

```solution
import matplotlib.pyplot as plt

characters = await load_csv("book-characters.csv")
print(list(characters.book.unique()))
book = characters[characters.book == "frankenstein"]
totals = book.groupby("character").mentions.sum().sort_values()
print(totals)

plt.barh(totals.index, totals.values)
plt.xlabel("times named")
---
In *Frankenstein*, Elizabeth is named most, 92 times, then Clerval and
Justine. Victor Frankenstein, who tells most of the story, is named only
28 times. A narrator says "I", which the count does not see. The
creature has no name at all, so he has no row. In
*The War of the Worlds* the narrator has no name either. A chart of
names measures who is named, not who matters. That difference is a fact
about the data, not the book.
```

</div>

<div class="dl-world" data-world="games-of-chance">

Roll two dice 1,000 times. On one chart, draw a bar for the counted
chance of each total, and a dot for the share of the 1,000 rolls that
made it. Where do the dots miss the bars most?

```python exec
id: charts-world--games-of-chance
import itertools
import random
import matplotlib.pyplot as plt

outcomes = list(itertools.product(range(1, 7), repeat=2))
totals = list(range(2, 13))
counted = [len([roll for roll in outcomes if sum(roll) == total]) / 36 for total in totals]

rolled = {}
for total in totals:
    rolled[total] = 0
for roll in range(1000):
    total = random.randint(1, 6) + random.randint(1, 6)
    rolled[total] = rolled[total] + 1
```

```hint
Use `plt.bar(totals, counted)` for the bars, then
`plt.plot(totals, [rolled[t] / 1000 for t in totals], "o", color="black")`
for the dots, with `"o"` meaning dots and no line.
```

```solution
import itertools
import random
import matplotlib.pyplot as plt

outcomes = list(itertools.product(range(1, 7), repeat=2))
totals = list(range(2, 13))
counted = [len([roll for roll in outcomes if sum(roll) == total]) / 36 for total in totals]

rolled = {}
for total in totals:
    rolled[total] = 0
for roll in range(1000):
    total = random.randint(1, 6) + random.randint(1, 6)
    rolled[total] = rolled[total] + 1

plt.bar(totals, counted, label="counted")
plt.plot(totals, [rolled[t] / 1000 for t in totals], "o", color="black", label="rolled")
plt.xlabel("total of two dice")
plt.ylabel("share")
plt.legend()
---
The dots sit close to the bars, and miss most, in shares, near the
middle, where the bars are tallest. For the rare totals, 2 and 12, a
miss of a few rolls is a large miss as a fraction of the bar. Run it
again and the misses move. With 100,000 rolls they would nearly vanish.
That is the law of large numbers, in a picture.
```

</div>

## From earlier

**11.** From *Statistics*. On a histogram of a right-skewed dataset, you
draw a line at the mean and a line at the median. Which is further
right?

<details class="dl-answer"><summary>answer</summary>

The mean. The long tail of large values pulls the mean towards it, and
the median, which depends only on the middle, hardly moves. The gap
between the two lines shows the skew at a glance.

</details>

**12.** From *Probability*. Draw the million people from the medical
test as a bar chart of four groups: sick and positive (99), sick and
negative (1), well and positive (9,999), well and negative (989,901).
Why is the chart nearly useless, and what would fix it?

<details class="dl-answer"><summary>answer</summary>

The well-and-negative bar is so tall that the other three are
invisible, and they are what matters. There are two fixes. One is a
log scale, which shows all four, clearly labelled. The other is to remove
the 989,901 people who tested negative and did not need to, and draw only
the positives, 99 against 9,999. Deciding what a chart does not show is
part of making it, as long as you say so.

</details>

**13.** From *Counting*. Draw a bar chart of $C(10, k)$ for $k$ from 0 to
10. What shape is it, and where have you seen it before?

<details class="dl-answer"><summary>answer</summary>

It is a symmetric hump, from 1 up to 252 at $k = 5$ and back to 1. It is the
row of Pascal's triangle for 10, and the shape of the binomial
distribution of heads in ten coin flips, from the Statistics page. Each
count divided by $2^{10}$ is the chance of that many heads.

</details>
