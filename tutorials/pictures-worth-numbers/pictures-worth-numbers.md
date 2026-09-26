---
title: "Charts: choosing the right chart for your data"
year: "2026-2027"
version: 2026.09.26.1
worlds:
  exoplanets: Planets around other stars, and the ways they were found.
  dinosaurs: Dinosaurs and their fossils, what has been found, where, and how old it is.
  book-characters: The people in six novels, chapter by chapter.
  games-of-chance: Dice, cards and coins, and the games people play with them.
datasets: [exoplanets, dinosaur-genera, book-characters]
covers:
  why-draw-the-data:
    covers: [MIT-5.10]
  choosing-the-right-chart:
    covers: [MIT-5.10]
  writing-reusable-plotting-functions:
    covers: [PDP-LO8]
  how-a-chart-can-mislead:
    covers: [MIT-5.10]
  numbers-and-a-chart-together:
    covers: [MIT-5.12]
---

# Charts: choosing the right chart for your data

[Statistics](tutorial:making-sense-of-data) summed up the planets in a
few numbers, and drew one histogram, which showed two humps that no
average could. This page is about charts: which chart suits which
question, how to write plotting code once and use it again, and how a
chart can tell the truth about data, or not.

## Why draw the data?

Can four datasets have the same averages and the same spread, and still
look nothing like each other?

*Anscombe's quartet* is four small datasets made by the statistician
Francis Anscombe in 1973. Each is eleven points, an x and a y. The four
have nearly the same means, the same standard deviations, and the same
*correlation*: a number from $-1$ to $1$ that measures how closely the
points follow a straight line. Near 1, they lie close to a line going
up; near 0, there is no straight-line pattern. This cell prints the
means, and draws all four.

```python exec
id: why-visualise-1
import matplotlib.pyplot as plt

datasets = {
    "I":   {"x": [10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5],
            "y": [8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68]},
    "II":  {"x": [10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5],
            "y": [9.14, 8.14, 8.74, 8.77, 9.26, 8.10, 6.13, 3.10, 9.13, 7.26, 4.74]},
    "III": {"x": [10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5],
            "y": [7.46, 6.77, 12.74, 7.11, 7.81, 8.84, 6.08, 5.39, 8.15, 6.42, 5.73]},
    "IV":  {"x": [8, 8, 8, 8, 8, 8, 8, 19, 8, 8, 8],
            "y": [6.58, 5.76, 7.71, 8.84, 8.47, 7.04, 5.25, 12.50, 5.56, 7.91, 6.89]},
}

for name in datasets:
    xs = datasets[name]["x"]
    ys = datasets[name]["y"]
    print(name, " mean x", round(sum(xs) / len(xs), 2), " mean y", round(sum(ys) / len(ys), 2))

fig, axes = plt.subplots(2, 2, figsize=(9, 7))
for ax, name in zip(axes.flat, datasets):
    ax.scatter(datasets[name]["x"], datasets[name]["y"])
    ax.set_title("Dataset " + name)
    ax.set_xlim(3, 20)
    ax.set_ylim(2, 14)
plt.tight_layout()
```

The summaries agree, and the pictures do not. One is a loose cloud
around a line; one is a smooth curve; one is a neat line with a single
point far off it; and one is a column of points with one point far to
the right, which makes the whole "relationship" on its own.
`plt.subplots(2, 2)` makes a grid of four charts, called *axes*, and the
loop draws one set of points on each.

## Choosing the right chart

Each kind of chart answers its own kind of question:

| Chart | What it shows | A question it answers |
|---|---|---|
| Histogram | How one set of numbers is spread out | What sizes are planets? |
| *Bar chart* | Amounts compared across categories | How many planets did each method find? |
| *Line chart* | A trend along something ordered, often time | How many planets were found each year? |
| *Scatter plot* | How two sets of numbers relate | Do planets with longer years tend to be larger? |
| *Pie chart* | The parts of a whole | What share of planets did each method find? |

Use pie charts rarely. People compare the lengths of bars much more
easily than the sizes of slices, so a bar chart usually shows the same
thing more clearly.

### A bar chart

How many planets did each method find? The methods are categories, so
this is a bar chart. With long labels, horizontal bars (`plt.barh`) keep
them readable.

```python exec
id: making-a-bar-chart-1
import matplotlib.pyplot as plt

planets = await load_csv("exoplanets.csv")
by_method = planets.method.value_counts()
top = by_method[:6]

plt.barh(top.index, top.values)
plt.gca().invert_yaxis()
plt.xlabel("planets found")
plt.title("How known planets were found")
```

`value_counts()` counts each method and puts the largest first;
`invert_yaxis()` keeps the largest at the top. Transit found about three
planets in four.

### A line chart

How many planets were announced each year? Years are in order and evenly
spaced, so a line joining them means something: it is a path through
time.

```python exec
id: making-a-line-chart-1
import matplotlib.pyplot as plt

per_year = planets.discovered.value_counts().sort_index()

plt.plot(per_year.index, per_year.values, marker="o")
plt.xlabel("year announced")
plt.ylabel("planets")
plt.title("Planets announced each year")
plt.grid(alpha=0.3)
```

Two spikes stand out: 2014, with 872 planets, and 2016, with 1,504. Both
are single announcements of planets found by the Kepler telescope,
checked in batches. The line shows how discoveries come: not steadily,
but in the lumps in which work is published.

### A scatter plot

Each point in a scatter plot is one planet: how long its year is, and how
big it is. Both go over huge ranges, so both axes are logarithmic. Before
you run it: which corner of the chart do you expect to be nearly empty?

```python exec
id: making-a-scatter-plot-1
import matplotlib.pyplot as plt

plt.scatter(planets.orbit_days, planets.radius_earths, s=4, alpha=0.3)
plt.xscale("log")
plt.yscale("log")
plt.xlabel("orbit, in days")
plt.ylabel("radius, in Earth radii")
plt.title("Year length against size")
```

```predict
Which corner will be nearly empty?

- Bottom right: small planets with long years
  - They are the hardest to find.
- Top left: large planets with short years
  - Giants that close to their stars seem unlikely.
- None of them
  - Planets come in every size at every distance.
```

The bottom right. There is a crowd of small planets with years of a few
days, and a clump of giants at the top left, the *hot Jupiters*, as big
as Jupiter and closer to their stars than Mercury is to the Sun. The
empty corner is the sampling bias from the last page, seen at a glance:
small planets with long years are there, but we can hardly find them.

One more thing is worth a second look: the flat line of points near 13
Earth radii, running out to years of thousands of days. A line that flat
is rarely nature. Most of those planets were found by the wobble of
their star, which gives a planet's mass but not its size, and the
archive estimated their radius from their mass. A chart shows how the
numbers were made, as well as what they measure.

```question
id: choosing-a-chart
type: fill-in-the-blank

- How your daily step count changed over a month: a {line chart|bar chart|histogram|scatter plot}.
- The number of bugs found in each of five parts of a program: a {bar chart|line chart|histogram|scatter plot}.
- How long a website takes to answer, over 10,000 requests: a {histogram|bar chart|line chart|scatter plot}.
- Whether people who drink more coffee sleep less: a {scatter plot|histogram|bar chart|line chart}.
```

## Writing reusable plotting functions

Every chart above needed the same few lines: draw, label the axes, add a
title. A function can hold them, so each new chart is one line. Can you
write `bar_chart(labels, values, title, xlabel)`, which draws a labelled
horizontal bar chart with the first label at the top?

```python exec
id: writing-reusable-plotting-functions-1
import matplotlib.pyplot as plt


def bar_chart(labels, values, title, xlabel):
    """Draw a labelled horizontal bar chart, first label at the top."""
    # Your code here


by_method = planets.method.value_counts()
bar_chart(by_method.index[:6], by_method.values[:6], "How known planets were found", "planets")
```

```hint
The bar chart earlier on this page has every line you need: `plt.barh`,
`plt.gca().invert_yaxis()`, `plt.xlabel` and `plt.title`. Use the
parameters in place of the fixed labels.
```

```solution
import matplotlib.pyplot as plt


def bar_chart(labels, values, title, xlabel):
    """Draw a labelled horizontal bar chart, first label at the top."""
    plt.figure()
    plt.barh(labels, values)
    plt.gca().invert_yaxis()
    plt.xlabel(xlabel)
    plt.title(title)


planets = await load_csv("exoplanets.csv")
by_method = planets.method.value_counts()
bar_chart(by_method.index[:6], by_method.values[:6], "How known planets were found", "planets")
---
`plt.figure()` starts a new chart each time, so two calls in one cell
draw two charts rather than piling bars on top of each other. The
decisions about how a bar chart should look now live in one place:
change them there, and every chart that uses the function changes too.
```

## How a chart can mislead

A chart can be made from true numbers and still leave a false picture.
The commonest ways are few, and once you know them, you see them
everywhere.

### A bar that does not start at zero

The file has 260 planets announced in 2024 and 245 in 2025. Here they
are twice: on the left with the axis starting at zero, and on the right
with it starting at 240. `plt.subplots(1, 2)` makes two charts side by
side.

```python exec
id: mislead-truncated-axis
import matplotlib.pyplot as plt

years = ["2024", "2025"]
counts = [260, 245]

fig, (left, right) = plt.subplots(1, 2, figsize=(9, 4))
left.bar(years, counts)
left.set_title("Axis from 0")
right.bar(years, counts)
right.set_ylim(240, 262)
right.set_title("Axis from 240")

print("The real ratio:", round(260 / 245, 2))
print("On the right, 2024's bar is drawn", (260 - 240) / (245 - 240), "times as tall")
```

```predict
type: number

On the right, how many times as tall as 2025's bar will 2024's bar be
drawn?
```

Four times as tall, for a difference of 6%. The length of a bar is what
shows its value, so a bar chart must start at zero. A line chart need
not: how steeply it rises and falls carries the meaning, and forcing it
to zero can flatten a real change until it disappears. Plotting libraries often choose the
axis that fills the frame, so the truncated chart is the one you get if
you do nothing.

### A window chosen to tell a story

"Planet discoveries collapse by 87%!" Here are the years that headline
might use, and the whole record beside them.

```python exec
id: mislead-chosen-window
import matplotlib.pyplot as plt

per_year = planets.discovered.value_counts().sort_index()
window = per_year.loc[2016:2019]

fig, (left, right) = plt.subplots(1, 2, figsize=(10, 4))
left.plot(window.index, window.values, marker="o")
left.set_title("2016 to 2019")
right.plot(per_year.index, per_year.values, marker="o")
right.set_title("Every year")
print("2016:", per_year[2016], " 2019:", per_year[2019])
```

From 1,504 to 194 is a fall of 87%, and every number is true. But 2016
was the year of Kepler's great batch, and the whole record shows no
collapse at all. Starting a window at a peak, or ending it at a dip, is
the easiest way to make a trend. A last period that is not over yet does
the same: this year's count, compared with whole years, always looks like
a fall.

### Three more

- **Area for length.** A picture of a planet twice as wide looks four
  times as big, because its area is four times as big. Pictures sized by
  a number exaggerate it.
- **A logarithmic axis nobody mentions.** On a log scale, equal steps
  multiply. A reader who does not notice will misjudge every difference.
- **Correlation read as cause.** Ice cream sales and drownings rise
  together, because both rise in hot weather. A *confounder* is a third
  thing that makes two others move together. The chart is not wrong; the
  sentence written under it often is.

## Numbers and a chart together

A summary and a chart each catch what the other misses. Can you write
`summarise(data, title)`, which prints the mean, median and standard
deviation, and draws a histogram with dashed lines at the mean and the
median? The cell starts with `mean`, `median` and `std_dev`, the
functions from the Statistics page, so you can use them.

```python exec
id: combining-statistics-and-visualisation-1
{{include: setup/data/functions.py}}

import matplotlib.pyplot as plt


def summarise(data, title):
    """Print the centre and spread of data, and draw its histogram."""
    # Your code here


distances = planets.distance_ly.dropna().tolist()
summarise(distances, "Distance from us, in light years")
```

```hint
Print the three numbers first. Then `plt.hist(data, bins=50)`, and
`plt.axvline(value, linestyle="--", label="mean")` for each line, with
`plt.legend()` to name them.
```

```solution
{{include: setup/data/functions.py}}

import matplotlib.pyplot as plt


def summarise(data, title):
    """Print the centre and spread of data, and draw its histogram."""
    print(title)
    print("  mean   ", round(mean(data), 1))
    print("  median ", round(median(data), 1))
    print("  sd     ", round(std_dev(data), 1))
    plt.figure()
    plt.hist(data, bins=50)
    plt.axvline(mean(data), color="red", linestyle="--", label="mean")
    plt.axvline(median(data), color="green", linestyle="--", label="median")
    plt.title(title)
    plt.legend()


planets = await load_csv("exoplanets.csv")
distances = planets.distance_ly.dropna().tolist()
summarise(distances, "Distance from us, in light years")
---
A mean of about 2,322 light years, a median of 1,172, and a standard
deviation of 4,031, larger than the mean itself. The histogram shows
why: a tall crowd near us and a long tail out past 20,000 light years,
the microlensing planets. The two lines apart is the skew, in one glance.
```

## Go further: the central limit theorem

Roll one die many times, and the histogram is flat: every face equally
often. Add two dice, and it is a triangle, as on the
[Probability](tutorial:what-are-the-chances) page. What happens with
ten?

```python exec
id: clt-dice
import random
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 3, figsize=(11, 3.5))
for ax, dice in zip(axes, [1, 2, 10]):
    totals = []
    for trial in range(10_000):
        total = 0
        for die in range(dice):
            total = total + random.randint(1, 6)
        totals.append(total)
    ax.hist(totals, bins=range(dice, 6 * dice + 2))
    ax.set_title(str(dice) + " dice")
plt.tight_layout()
```

With ten dice, the totals make a smooth hump, highest in the middle and
falling away evenly on both sides: a bell. The same happens with
anything added up from many independent random parts, whatever shape
each part has. That is the *central limit theorem*.

It is most useful for means. The planets' radii have two humps. Take a
random sample of 50 planets, and work out its mean radius; do that 2,000
times, and draw the means.

```python exec
id: clt-sample-means
import random
import matplotlib.pyplot as plt

radii = planets.radius_earths.dropna().tolist()
sample_means = []
for trial in range(2000):
    sample = random.sample(radii, 50)
    sample_means.append(sum(sample) / 50)

plt.hist(sample_means, bins=40)
plt.xlabel("mean radius of 50 planets")
plt.ylabel("samples")
print("The mean of all the radii:", round(sum(radii) / len(radii), 2))
```

A single bell, centred on the mean of all the radii, 5.88, though no
single planet's radius is anywhere near a bell. Each sample's mean
misses the true one, some by more than a whole Earth radius, and the
bell says how likely each size of miss is. That is what lets a survey of
a thousand people say something about a million.

## Go further: the 68–95–99.7 rule

A bell shape like that is called a *normal distribution*. For data that
is close to normal, about 68% of values are within one standard deviation
of the mean, about 95% within two, and about 99.7% within three: the
*68–95–99.7 rule*. Does it hold for the sample means? And for the
planets' orbits?

```python exec
id: rule-68-95-99
{{include: setup/data/functions.py}}


def share_within(data, how_many_sds):
    """The share of values within how_many_sds standard deviations of the mean."""
    centre = mean(data)
    spread = std_dev(data)
    inside = [value for value in data if abs(value - centre) < how_many_sds * spread]
    return len(inside) / len(data)


orbits = planets.orbit_days.dropna().tolist()
for k in [1, 2, 3]:
    print(k, "sd:  sample means", round(share_within(sample_means, k), 3),
          "  orbits", round(share_within(orbits, k), 4))
```

The sample means follow the rule closely: about 0.68, 0.95 and 0.99.
The orbits do not: 99.9% of them are within one standard deviation,
not 68%.
One enormous orbit made the standard deviation over five million days,
so almost everything is "close" by that measure. The rule belongs to
bell-shaped data. On skewed data, a statement like "three standard
deviations from the mean" can mean almost nothing.

## Your world

A chart that answers one question in the world you chose.

<div class="dl-world" data-world="exoplanets">

Has the typical distance of newly found planets changed over the years?
Draw the median distance of each year's planets as a line chart, with a
log scale on the y axis.

```python exec
id: charts-your-world--exoplanets
import matplotlib.pyplot as plt

planets = await load_csv("exoplanets.csv")
median_distance = planets.groupby("discovered").distance_ly.median()
print(median_distance.loc[2014:2019])
```

```hint
`median_distance.index` is the years and `median_distance.values` the
medians. `plt.yscale("log")` after `plt.plot`.
```

```solution
import matplotlib.pyplot as plt

planets = await load_csv("exoplanets.csv")
median_distance = planets.groupby("discovered").distance_ly.median()
print(median_distance.loc[2014:2019])

plt.plot(median_distance.index, median_distance.values, marker="o")
plt.yscale("log")
plt.xlabel("year announced")
plt.ylabel("median distance, light years")
---
With the copy saved on {{snapshot: exoplanets}}: from about 50 light
years in the late 1990s to over 2,000 in Kepler's big years, 2014 and
2016, then back to a few hundred. Kepler stared at one patch of sky, deep
into it. TESS, launched in 2018, watches bright stars all over the sky,
and bright stars are mostly near. The planets did not move: the
telescopes changed, and the sample changed with them.
```

</div>

<div class="dl-world" data-world="dinosaurs">

How many dinosaur genera were named in each decade? Draw a bar for each
decade. Then look hard at the last bar before you say what the chart
shows.

```python exec
id: charts-your-world--dinosaurs
import matplotlib.pyplot as plt

genera = await load_csv("dinosaur-genera.csv")
decades = {}
for name in genera.named_by:
    year = int(name.strip("()")[-4:])
    decade = year // 10 * 10
    if decade not in decades:
        decades[decade] = 0
    decades[decade] = decades[decade] + 1
print(sorted(decades.items())[-4:])
```

```hint
`plt.bar(list(decades.keys()), list(decades.values()), width=8)`: the
width of 8 years leaves a gap between the ten-year bars.
```

```solution
import matplotlib.pyplot as plt

genera = await load_csv("dinosaur-genera.csv")
decades = {}
for name in genera.named_by:
    year = int(name.strip("()")[-4:])
    decade = year // 10 * 10
    if decade not in decades:
        decades[decade] = 0
    decades[decade] = decades[decade] + 1
print(sorted(decades.items())[-4:])

plt.bar(list(decades.keys()), list(decades.values()), width=8)
plt.xlabel("decade named")
plt.ylabel("genera")
---
With the copy saved on {{snapshot: dinosaur-genera}}: a bump in the
1870s, the "Bone Wars" between two American collectors racing to name
new animals; a dip in the 1940s, during the Second World War; and a
climb from the 1970s to 457 in the 2010s. The last bar, 254, looks like a
fall, and mostly it is not: the 2020s are not yet seven years old, and
at that pace the decade would end near 380, not 254. An unfinished last period is one of the
easiest ways for a chart to mislead.
```

</div>

<div class="dl-world" data-world="book-characters">

When are Mr Darcy and Mr Wickham on stage in *Pride and Prejudice*? Draw
each one's mentions, chapter by chapter, as two lines on one chart, with
a legend.

```python exec
id: charts-your-world--book-characters
import matplotlib.pyplot as plt

characters = await load_csv("book-characters.csv")
pride = characters[characters.book == "pride-and-prejudice"]
darcy = pride[pride.character == "Darcy"]
wickham = pride[pride.character == "Wickham"]
print(len(darcy), "chapters")
```

```hint
`plt.plot(darcy.chapter, darcy.mentions, label="Darcy")`, the same for
Wickham, then `plt.legend()`.
```

```solution
import matplotlib.pyplot as plt

characters = await load_csv("book-characters.csv")
pride = characters[characters.book == "pride-and-prejudice"]
darcy = pride[pride.character == "Darcy"]
wickham = pride[pride.character == "Wickham"]
print(len(darcy), "chapters")

plt.plot(darcy.chapter, darcy.mentions, label="Darcy")
plt.plot(wickham.chapter, wickham.mentions, label="Wickham")
plt.xlabel("chapter")
plt.ylabel("times named")
plt.legend()
---
Darcy peaks at chapter 18, the Netherfield ball, named 41 times; Wickham
at chapter 16, where he tells Elizabeth his story about Darcy. Wickham
comes and goes in bursts, and Darcy is named in most chapters, even the
ones he is not in, because the others talk about him. Chapters are in
order, so a line chart fits: the x axis is the book's own time.
```

</div>

<div class="dl-world" data-world="games-of-chance">

Roll three dice and add them. Count every one of the $6^3 = 216$
outcomes, with no simulation at all, and draw a bar for each total.
Which totals are commonest?

```python exec
id: charts-your-world--games-of-chance
import itertools
import matplotlib.pyplot as plt

totals = {}
for roll in itertools.product(range(1, 7), repeat=3):
    total = sum(roll)
    if total not in totals:
        totals[total] = 0
    totals[total] = totals[total] + 1
print(len(totals), "different totals")
```

```hint
`plt.bar(list(totals.keys()), list(totals.values()))`, then look for the
tallest bars.
```

```solution
import itertools
import matplotlib.pyplot as plt

totals = {}
for roll in itertools.product(range(1, 7), repeat=3):
    total = sum(roll)
    if total not in totals:
        totals[total] = 0
    totals[total] = totals[total] + 1
print(len(totals), "different totals")
print(totals[10], totals[11], totals[3])

plt.bar(list(totals.keys()), list(totals.values()))
plt.xlabel("total of three dice")
plt.ylabel("outcomes, of 216")
---
10 and 11, with 27 outcomes each; 3 and 18 have one each. Two dice made
a triangle; three already make a rounded hump, the start of the bell in
the central limit theorem, and this time counted exactly rather than
simulated.
```

</div>

## Good practice

A checklist for any chart that someone else will see:

- **A title, and labels with units** on both axes. The chart should make
  sense with no text around it, because it will be copied into places
  where there is none.
- **Bars start at zero.** Line charts may not, and should say so.
- **The same scale** for charts meant to be compared.
- **Say where the data came from**, and when.
- **No chart junk.** *Chart junk* is decoration that carries no
  information. Colour should separate things, not decorate them.

## Looking back

This page drew the same planets many ways, and made one pair of true
numbers look like a fourfold difference. If you had to make a chart of
the planets that misled without a single false number, which of the
tricks on this page would you use, and what would give it away?

A challenge: the central limit theorem for something far from a bell.
The wait for a six, from the Statistics page, is skewed: mostly short,
sometimes very long. Take the mean wait of a sample of players, many
times, and draw the means. How big must a sample be before the bell
appears?

```python challenge
import random
import matplotlib.pyplot as plt


def rolls_until_six():
    rolls = 1
    while random.randint(1, 6) != 6:
        rolls = rolls + 1
    return rolls


# For samples of 2, 10 and 50 players: work out 2,000 sample means,
# and draw a histogram of each.
```

The last page of the series asks you to make exactly that: one chart
that tells the truth about your world's data, and one that does not.

## Where to read more

Anscombe, F. J. (1973). *Graphs in Statistical Analysis.* The American
Statistician, 27(1), 17–21. The paper behind the quartet this page opens
with.

Stand-up Maths (2020). *The Datasaurus Dozen.*
<https://www.youtube.com/watch?v=iwzzv1biHv8>. Twelve sets of points with
the same means and spread, which look nothing alike when drawn, and one
of them is a dinosaur. Eight minutes.

Matplotlib development team. *Pyplot Tutorial.*
<https://matplotlib.org/stable/tutorials/pyplot.html>. The official
reference for everything this page's charts do.

CrashCourse (2018). *Charts Are Like Pasta: Data Visualization Part 1:
Crash Course Statistics #5.*
<https://www.youtube.com/watch?v=hEWY6kkBdpo>. Which chart suits which
kind of data, starting with bar charts and pie charts for categories.
About ten minutes.
