---
title: "Charts: choosing the right chart for your data — Practice"
practice_for: pictures-worth-numbers
year: "2026-2027"
version: 2026.08.23.1
---

# Charts: choosing the right chart for your data — Practice

Each answer is hidden until you open it. Most of these problems ask you
to choose a chart and to explain your choice. The plotting takes only a
few lines of code. The real skill is the choosing.

## Tools

This cell holds a small helper, `bars()`, that draws a bar chart. It
also imports `plt`, which the answers below use.

```python exec
id: tools-1
import matplotlib.pyplot as plt

def bars(labels, values, title="", ylabel=""):
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

**1.** Which chart would you choose for each of these, and why?

- (a) Sales in each of six regions
- (b) Website visits each day for a year
- (c) Height against weight for 200 people
- (d) The distribution of exam marks in a class
- (e) Market share of four companies

<details class="dl-answer"><summary>answer</summary>

(a) A bar chart, because we are comparing separate categories.

(b) A line chart. The value changes over time, the days have a
meaningful order, and they are evenly spaced.

(c) A scatter plot. We have two measurements for each person, and we are
looking for a relationship between them.

(d) A histogram. There is one variable, and we want to see its shape.

(e) A bar chart. A pie chart is the traditional answer, but it works
less well. People are bad at comparing angles and good at comparing
lengths.

</details>

**2.** When is a line chart the wrong choice?

<details class="dl-answer"><summary>answer</summary>

A line chart is wrong when the x axis has no meaningful order, or no
meaningful spacing.

Suppose we join the sales of six regions with a line. Leinster, Munster
and Connacht are three of the provinces of Ireland. If the line goes
from Leinster to Munster to Connacht, it suggests that Munster lies
between the other two in some quantity. It does not. A line says "these
points are on a path". If there is no path, the chart is telling a lie.

</details>

**3.** What is the difference between a bar chart and a histogram?

<details class="dl-answer"><summary>answer</summary>

A bar chart compares categories. A histogram shows the distribution of
one continuous variable, grouped into bins.

You can tell them apart by the gaps. The bars of a bar chart have gaps
between them, because the categories are separate. The bars of a
histogram touch. Each bin is a range of values on one continuous scale,
and the next bin starts where the last one ends, so there is nothing
between them.

</details>

**4.** You have five years of monthly sales for three products. What do you plot?

<details class="dl-answer"><summary>answer</summary>

Plot three lines on one pair of axes, with a legend.

Three separate charts would each be easy to read, but they would be
useless for comparing the products, and comparing is the real point of
the question. With the three lines on one chart, a reader can see one
product overtake another.

This breaks down if the three products sell on very different scales.
Then the fix is to plot the percentage change for each product.
Another option is to add a second y axis, but a chart with two y axes
is nearly always harder to read than it looks.

</details>

## Reading charts

**5.** A bar chart's y axis starts at 95 instead of 0, and the bars run from 96 to 99. What is the effect?

<details class="dl-answer"><summary>answer</summary>

A difference of about 3% looks like a fourfold one.

The value 99 is only about 3% bigger than 96. But with the axis starting
at 95, the bar for 96 shows a height of 1 and the bar for 99 shows a
height of 4. So the tallest bar looks four times as big as the shortest.

This is the most common way a chart misleads, and it is usually not on
purpose. Plotting libraries often choose an axis range that fills the
frame.

Bar charts should start at zero, because the *length* of a bar is what
shows its value. Line charts do not have to start at zero, because the
*slope* of the line carries the meaning. If you force a line chart to
start at zero, you can flatten a real trend until it disappears.

</details>

**6.** A scatter plot shows a clear upward trend between ice cream sales and drownings. What does it mean?

<details class="dl-answer"><summary>answer</summary>

It means that both go up in hot weather.

Correlation tells us that two things move together. It does not tell us
which one causes the other. It also does not rule out a third thing
that causes both. Here that third thing is the temperature. A *confounder*
is a third thing that causes two others to move together.

The chart is not wrong. The sentence somebody writes underneath it
usually is.

</details>

**7.** Two variables have a correlation of 0. Can they still be related?

<details class="dl-answer"><summary>answer</summary>

Yes. Correlation measures only a *linear* relationship, one that
follows a straight line.

Take points on the curve $y = x^2$, for x from $-3$ to $3$. The curve is
symmetric, so the correlation is zero. But the
relationship is perfect: $y$ is exactly $x^2$. A quick plot answers the
question that the correlation number cannot.

</details>

## Making them

**8.** Plot support tickets per day for a week as a bar chart, with labels and a title.

<details class="dl-answer"><summary>answer</summary>

```python
import matplotlib.pyplot as plt

days = ["Mon", "Tue", "Wed", "Thu", "Fri"]
tickets = [12, 19, 8, 22, 15]

fig, ax = plt.subplots(figsize=(7, 4))
ax.bar(days, tickets)
ax.set_title("Support tickets by day")
ax.set_ylabel("tickets")
ax.grid(axis="y", alpha=0.3)
```

The grid has horizontal lines only, set by `axis="y"`. Horizontal grid
lines behind the bars help us read their heights. Vertical lines between
the categories would add nothing.

</details>

**9.** Plot two curves on one pair of axes, with a legend: $y = x^2$ and $y = 2^x$, for x from 0 to 10.

<details class="dl-answer"><summary>answer</summary>

```python
xs = list(range(11))
fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(xs, [x ** 2 for x in xs], label="x^2")
ax.plot(xs, [2 ** x for x in xs], label="2^x")
ax.legend()
ax.grid(alpha=0.3)
```

The curves cross twice, at $x = 2$ and at $x = 4$. After that, $2^x$
grows much faster. At $x = 10$ it is 1024, against 100 for $x^2$, and
the $x^2$ curve looks almost flat beside it.

A curve like $2^x$, where $x$ is the power, is called *exponential*.
[Number types, powers and logarithms](tutorial:numbers-and-their-families)
looks at powers more closely. For large $x$, the two curves are not
comparable at all. This is why an algorithm whose running time grows
exponentially is more than a slow algorithm: it quickly becomes
unusable.

</details>

**10.** Plot the same pair with a logarithmic y axis. What changes?

<details class="dl-answer"><summary>answer</summary>

On a *logarithmic scale*, each equal step up the axis multiplies the
value by the same amount: 1, 10, 100, 1000. One line of code changes the
axis:

```python
ax.set_yscale("log")
```

The $2^x$ curve becomes a straight line. The $x^2$ curve bends over and
flattens.

On a log scale, exponential growth is a straight line, and the
steepness of the line shows how fast it grows. That is the main reason
log scales exist. They turn multiplying into equal distances, so one
chart can show values from 1 to 1,000,000 and still be readable.

You will also see the $x^2$ line drop off the bottom of the chart at the
left. Its first value is $0$, and $0$ has no place on a log scale: each
step down divides by 10, and you never reach 0.

Always label a log axis clearly. A reader who does not notice it will
underestimate every difference on the chart.

</details>

**11.** Write a reusable `scatter(xs, ys, ...)` function with sensible defaults.

<details class="dl-answer"><summary>answer</summary>

```python
def scatter(xs, ys, title="", xlabel="", ylabel="", ax=None):
    """A labelled scatter plot. Pass ax to draw onto existing axes."""
    if ax is None:
        fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.scatter(xs, ys, alpha=0.6)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(alpha=0.3)
    return ax
```

The `ax=None` parameter is what makes the function reusable, and not
only shorter. With it, the function can draw a chart on its own, or draw
one panel of a larger figure. It returns `ax`, so the caller can keep
changing the chart afterwards.

</details>

**12.** Plot a histogram of 1,000 random numbers from `random.random()`. Then plot one of the *sum of three* such numbers. What is the difference?

<details class="dl-answer"><summary>answer</summary>

The first histogram is flat. The second is a hump with its centre at
1.5.

```python
import random
singles = [random.random() for _ in range(1000)]
triples = [sum(random.random() for _ in range(3)) for _ in range(1000)]
```

When we add three random numbers, middle-sized totals are far more
likely than very small or very large ones. It is the same reason a total
of 7 is more likely than a total of 12 on two dice. If you add together
enough independent random numbers, the histogram of the totals comes
close to a bell-shaped curve. This fact is called the *central limit
theorem*, and it is one of the most surprising results in mathematics.

</details>

## Combining with statistics

**13.** Plot a histogram of a dataset, with lines marking its mean and its median. When do the two lines separate?

<details class="dl-answer"><summary>answer</summary>

```python
import statistics

ax.axvline(statistics.mean(data), color="tab:red", linestyle="--", label="mean")
ax.axvline(statistics.median(data), color="tab:green", linestyle=":", label="median")
ax.legend()
```

Here `statistics` is Python's own module of statistics functions. Your
`mean()` and `median()` from the statistics tutorial would work equally
well.

The two lines separate when the data is skewed. The mean usually moves away
from the median towards the long tail. When the distribution is
symmetric, the two lines land on top of each other.

Drawing both lines is a good habit. It costs two lines of code, and the
gap between them tells you about the shape of the data.

</details>

**14.** Plot Anscombe's Quartet: four datasets with the same mean, variance and correlation. Describe what each one looks like.

<details class="dl-answer"><summary>answer</summary>

```python
x = [10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5]
y1 = [8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68]
y2 = [9.14, 8.14, 8.74, 8.77, 9.26, 8.10, 6.13, 3.10, 9.13, 7.26, 4.74]
y3 = [7.46, 6.77, 12.74, 7.11, 7.81, 8.84, 6.08, 5.39, 8.15, 6.42, 5.73]
x4 = [8, 8, 8, 8, 8, 8, 8, 19, 8, 8, 8]
y4 = [6.58, 5.76, 7.71, 8.84, 8.47, 7.04, 5.25, 12.50, 5.56, 7.91, 6.89]
```

- The first is a straight-line relationship with some noise around it.
- The second is a clean curve, the shape of a parabola.
- The third is a perfect straight line, with one outlier that pulls the
  fitted line towards it.
- The fourth is a column of points at $x = 8$, plus one point far away.
  That single point creates the whole apparent relationship.

All four have a mean x of 9, a mean y of 7.5, the same variance and a
correlation of 0.816. Those summaries agree, but the pictures have
almost nothing in common. Other summaries do differ: the median of y,
for example, is 7.58 in the first dataset and 7.04 in the fourth.

</details>

## Good practice

**15.** List the things a chart needs before anyone else sees it.

<details class="dl-answer"><summary>answer</summary>

- A title that says what the chart shows.
- Labels on the axes, with units.
- A legend, if there is more than one series.
- A y axis that starts at zero, if the chart uses bars.
- A source, if the data came from somewhere.

The test is this: can the chart be understood without you beside it?
Charts get copied into slides and reports. Your chart will be read by
somebody who cannot ask you what an axis means.

</details>

**16.** What is wrong with a chart of "Sales" against "Month", with no units and a y axis from 3.4 to 3.6?

<details class="dl-answer"><summary>answer</summary>

Two things are wrong, and the second is worse.

First, the units are missing. The value 3.4 could mean 3.4 thousand,
3.4 million, or 3.4 units sold.

Second, the axis range makes a change of unknown size fill the whole
frame. Without units, the reader cannot even tell whether the ups and
downs matter. The chart is unreadable, and it also looks dramatic. That
is the worst possible combination.

</details>

**17.** You are asked to make a difference "look bigger" in a chart for a presentation. What do you do?

<details class="dl-answer"><summary>answer</summary>

Say what the difference is, and ask whether it is worth presenting.

There are several tricks that make a small difference look big:
cutting off the bottom of the axis, using area or volume to show an
amount that should be a length, or choosing a lucky date range. Every
one of them works by misleading the people who look at the chart. Later,
somebody may use that chart to make a decision, and the decision will
rest on the trick.

Sometimes the difference does matter and still looks small. Then the fix
is usually to plot the right thing: the change instead of the level, the
rate instead of the total, or the amount per person instead of the raw
number. That is not distortion. It often makes a real effect visible for
the first time.

</details>
