---
title: "Pictures Worth Numbers — Practice"
slug: pictures-worth-numbers-practice
practice_for: pictures-worth-numbers
module: mit-pdp-maths-prog-integration
module_title: "Programming and Maths, Integrated"
year: "2026-2027"
series: maths-and-programming
version: 2026.08.23.1
---

# Pictures Worth Numbers — Practice

Answers are folded. Most of these ask you to choose a chart and defend the choice — the plotting is a few lines, and the choosing is the skill.

## Tools

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

## Choosing a Chart

**1.** Which chart for each, and why?

- (a) Sales in each of six regions
- (b) Website visits each day for a year
- (c) Height against weight for 200 people
- (d) The distribution of exam marks in a class
- (e) Market share of four companies

<details class="dl-answer"><summary>answer</summary>

(a) Bar chart — comparing separate categories.

(b) Line chart — a value changing over time, where the order is meaningful and the gaps are even.

(c) Scatter plot — two measurements per subject, looking for a relationship.

(d) Histogram — one variable, showing its shape.

(e) Bar chart. A pie chart is the traditional answer and is worse: people compare angles badly and lengths well.

</details>

**2.** When is a line chart wrong?

<details class="dl-answer"><summary>answer</summary>

When the x axis has no meaningful order or no meaningful spacing.

Joining the sales of six regions with a line implies that Munster is between Leinster and Connacht in some quantity, which it is not. The line says "these points are on a path", and if there is no path the chart is lying.

</details>

**3.** What is the difference between a bar chart and a histogram?

<details class="dl-answer"><summary>answer</summary>

A bar chart compares categories; a histogram shows the distribution of one continuous variable in bins.

The visual tell is the gaps. Bar chart bars are separated because the categories are separate. Histogram bars touch, because the bins are adjacent ranges of one continuous scale with nothing between them.

</details>

**4.** You have five years of monthly sales for three products. What do you plot?

<details class="dl-answer"><summary>answer</summary>

Three lines on one pair of axes, with a legend.

Three separate charts would be readable individually and useless for comparison, which is what the question is really about. Putting the lines together is what lets a reader see one product overtaking another.

If the three are on wildly different scales, that breaks down — and the fix is to plot the percentage change rather than adding a second y axis, which is nearly always harder to read than it looks.

</details>

## Reading Charts

**5.** A bar chart's y axis starts at 95 rather than 0, and the bars run from 96 to 99. What is the effect?

<details class="dl-answer"><summary>answer</summary>

A 3% difference looks like a threefold one.

This is the single most common way a chart misleads, and it is usually not deliberate — plotting libraries pick a range that fills the frame.

Bar charts should start at zero, because the bar's *length* is what encodes the value. Line charts need not, because the line's *slope* is what carries the meaning; forcing a line chart to zero can flatten a real trend into nothing.

</details>

**6.** A scatter plot shows a clear upward trend between ice cream sales and drownings. What does it mean?

<details class="dl-answer"><summary>answer</summary>

That both go up in hot weather.

Correlation says two things move together. It does not say which causes which, and it does not rule out a third thing causing both. Temperature here is a confounder.

The chart is not wrong. The sentence somebody writes underneath it usually is.

</details>

**7.** Two variables have a correlation of 0. Can they be related?

<details class="dl-answer"><summary>answer</summary>

Yes. Correlation measures *linear* relationship only.

Points on a symmetric parabola have a correlation of essentially zero and a perfect relationship: y is exactly x². Plotting it takes a second and settles the question that the correlation coefficient cannot answer.

</details>

## Making Them

**8.** Plot support tickets per day for a week as a bar chart, labelled and titled.

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

The grid on the y axis only. Gridlines behind bars help read heights; gridlines between the categories add nothing.

</details>

**9.** Plot two curves on one pair of axes with a legend: $y = x^2$ and $y = 2^x$ for x from 0 to 10.

<details class="dl-answer"><summary>answer</summary>

```python
xs = list(range(11))
fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(xs, [x ** 2 for x in xs], label="x^2")
ax.plot(xs, [2 ** x for x in xs], label="2^x")
ax.legend()
ax.grid(alpha=0.3)
```

They cross twice — at x = 2 and x = 4 — and after that the exponential runs away completely. At x = 10 it is 1024 against 100, and the squared curve is visually flat against it.

This is why the two are not comparable at large n and why an exponential algorithm is not merely a slow one.

</details>

**10.** Plot the same pair with a logarithmic y axis. What changes?

<details class="dl-answer"><summary>answer</summary>

```python
ax.set_yscale("log")
```

The exponential becomes a straight line, and the quadratic becomes a gentle curve.

On a log scale, exponential growth is straight and its slope is the growth rate. That is the whole reason log scales exist: they turn multiplication into distance, so a graph can hold six orders of magnitude and still be readable.

Always label a log axis clearly. A reader who misses it will underestimate every difference on the chart.

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

The `ax=None` parameter is what makes it reusable rather than merely shorter: with it, the function can draw a single chart or contribute one panel to a larger figure. Returning `ax` lets the caller keep adjusting.

</details>

**12.** Plot a histogram of 1,000 random numbers from `random.random()`, then of the *sum of three* such numbers. What is the difference?

<details class="dl-answer"><summary>answer</summary>

The first is flat. The second is a hump centred on 1.5.

```python
import random
singles = [random.random() for _ in range(1000)]
triples = [sum(random.random() for _ in range(3)) for _ in range(1000)]
```

Adding three uniform numbers makes middling totals far more likely than extreme ones, for the same reason a total of 7 beats a total of 12 on two dice. Add enough of anything together and you get a bell curve, which is the central limit theorem and one of the more surprising facts in mathematics.

</details>

## Combining With Statistics

**13.** Plot a dataset with its mean and median marked. When do the two lines separate?

<details class="dl-answer"><summary>answer</summary>

```python
ax.axvline(statistics.mean(data), color="tab:red", linestyle="--", label="mean")
ax.axvline(statistics.median(data), color="tab:green", linestyle=":", label="median")
ax.legend()
```

They separate when the data is skewed, and the gap between them points towards the tail. On a symmetric distribution the two lines land on top of each other.

Drawing both is a habit worth acquiring: the gap is a free diagnostic that costs two lines of code.

</details>

**14.** Plot Anscombe's quartet — four datasets with the same mean, variance and correlation — and describe what each looks like.

<details class="dl-answer"><summary>answer</summary>

```python
x = [10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5]
y1 = [8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68]
y2 = [9.14, 8.14, 8.74, 8.77, 9.26, 8.10, 6.13, 3.10, 9.13, 7.26, 4.74]
y3 = [7.46, 6.77, 12.74, 7.11, 7.81, 8.84, 6.08, 5.39, 8.15, 6.42, 5.73]
x4 = [8, 8, 8, 8, 8, 8, 8, 19, 8, 8, 8]
y4 = [6.58, 5.76, 7.71, 8.84, 8.47, 7.04, 5.25, 12.50, 5.56, 7.91, 6.89]
```

The first is a genuine noisy linear relationship. The second is a clean parabola. The third is a perfect line with one outlier dragging the fit. The fourth is a vertical stack at x = 8 plus one distant point, which alone creates the entire apparent relationship.

All four have a mean x of 9, a mean y of 7.5, and a correlation of 0.816. Any summary you compute will agree; nothing about them is the same.

</details>

## Good Practice

**15.** List the things a chart needs before anyone else sees it.

<details class="dl-answer"><summary>answer</summary>

A title saying what it shows. Labelled axes with units. A legend if there is more than one series. A y axis starting at zero if the marks are bars. A source, if the data came from somewhere.

The test is whether it survives being separated from you. Charts get copied into slides and reports, and yours will be read by somebody who cannot ask what the axis means.

</details>

**16.** What is wrong with a chart of "Sales" against "Month" with no units and a y axis from 3.4 to 3.6?

<details class="dl-answer"><summary>answer</summary>

Two things, and the second is worse.

The units are missing, so 3.4 could be thousands, millions, or units sold.

And the axis range makes an unknown-sized variation fill the whole frame. Without units the reader cannot even tell whether the wobble matters — the chart is unreadable and looks dramatic, which is the worst possible combination.

</details>

**17.** You are asked to make a difference "look bigger" in a chart for a presentation. What do you do?

<details class="dl-answer"><summary>answer</summary>

Say what the difference actually is, and ask whether it is worth presenting.

Every technique that makes a small difference look big — truncating the axis, using area or volume for a linear quantity, choosing a lucky date range — works by misleading, and works on the presenter too. The chart ends up in a decision.

If the difference genuinely matters and looks small, the fix is usually to plot the right thing: the change rather than the level, the rate rather than the total, or the per-person figure rather than the raw one. That is not distortion, and it often makes a real effect visible for the first time.

</details>
