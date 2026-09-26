---
title: "Charts: choosing the right chart for your data"
year: "2026-2027"
version: 2026.08.23.1
covers:
  why-visualize:
    covers: [MIT-5.10]
  choosing-the-right-chart:
    covers: [MIT-5.10]
  writing-reusable-plotting-functions:
    covers: [PDP-LO8]
  combining-statistics-and-visualization:
    covers: [MIT-5.12]
  good-practices-for-visualization:
    covers: [MIT-5.10]
---

# Charts: choosing the right chart for your data

In [Statistics: averages, spread and frequency](tutorial:making-sense-of-data)
we wrote functions for the mean, the median, the mode and the standard
deviation. We also drew our first histogram. On this page we look more
closely at charts. A good chart does more than make a report look nice.
It helps us understand the data.

On this page we:

- see how summary numbers can hide what a dataset looks like
- match five kinds of chart to the jobs they do well
- wrap plotting code in functions we can use again
- put summary numbers and a chart side by side
- collect a few rules that make any chart easier to read

Along the way we practise writing clean code, in small functions that
each do one job.

## Why visualize?

Can four datasets have the same averages and the same spread, and still
look nothing like each other?

*Anscombe's Quartet* is a set of four small datasets, made by the
statistician Francis Anscombe in 1973. The four datasets have nearly
the same mean and the same standard deviation. They also have the same
correlation. *Correlation* is a number between $-1$ and $1$ that
measures how closely two lists of numbers follow a straight line. A
correlation near $1$ means the points lie close to a line that goes up;
a correlation near $0$ means there is no straight-line pattern. We will
not calculate it on this page.

For the four datasets, every one of those numbers is about the same. So
the numbers cannot tell the datasets apart. What happens when we plot
them? Run the cell to see.

```python exec
id: why-visualise-1
import matplotlib.pyplot as plt

# Anscombe's Quartet
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

fig, axes = plt.subplots(2, 2, figsize=(10, 8))
for ax, (name, data) in zip(axes.flat, datasets.items()):
    ax.scatter(data["x"], data["y"])
    ax.set_title("Dataset " + name)
    ax.set_xlim(3, 20)
    ax.set_ylim(2, 14)
plt.tight_layout()
plt.show()
```

The four summaries are the same, but the four pictures tell very
different stories. One is a loose cloud around a line. One is a smooth
curve. One is a neat line with a single point far away from it. One is
a column of points with one point far off to the right. This is why
charts matter: they show us what the numbers alone cannot.

## Choosing the right chart

Different kinds of data need different kinds of chart. Each chart type
answers its own kind of question:

| Chart | What it shows | A question it answers |
|---|---|---|
| **Histogram** | How the values of one numerical variable are spread out | How often does each range of values occur? |
| **Bar chart** | Amounts compared across categories | How many students prefer each programming language? |
| **Line chart** | A trend over time, or along some other ordered sequence | How did the temperature change during the day? |
| **Scatter plot** | The relationship between two numerical variables | Do students who study for more hours get higher test scores? |
| **Pie chart** | The parts of a whole | What fraction of students passed, got a merit, or got a distinction? |

Use pie charts rarely. A bar chart usually shows the same information
more clearly, because people compare the lengths of bars more easily
than the sizes of slices.

We made a histogram on the statistics page. Here are the other three
most useful types.

### Making a bar chart

Suppose we asked a class of students for their favourite programming
language, and counted the answers:

```python exec
id: making-a-bar-chart-1
languages = ["Python", "JavaScript", "Java", "C++", "Other"]
counts = [15, 8, 5, 3, 4]

plt.figure(figsize=(8, 5))
plt.bar(languages, counts, color='steelblue', edgecolor='black')
plt.xlabel('Language')
plt.ylabel('Number of Students')
plt.title('Favourite Programming Language')
plt.show()
```

### Making a line chart

This chart shows the temperature at each hour of one day, from midnight
(hour 0) to the next midnight (hour 24). The hours are in order, so a
line joining them makes sense.

```python exec
id: making-a-line-chart-1
hours = list(range(0, 25))
temperatures = [8, 7, 6, 6, 5, 5, 6, 7, 9, 11, 13, 15, 
                16, 17, 17, 16, 15, 14, 12, 11, 10, 9, 9, 8, 8]

plt.figure(figsize=(10, 5))
plt.plot(hours, temperatures, marker='o', linewidth=2, markersize=4)
plt.xlabel('Hour of Day')
plt.ylabel('Temperature (C)')
plt.title('Temperature Throughout the Day')
plt.grid(True, alpha=0.3)
plt.show()
```

### Making a scatter plot

Each point in a scatter plot is one student: how many hours they studied,
and the score they got. The cell makes up data for 20 students, using
`random` as we did in
[Probability: simple, compound and conditional](tutorial:what-are-the-chances).
Before you run it, what shape do you expect the points to make?

```python exec
id: making-a-scatter-plot-1
# Study hours vs test scores for 20 students
import random
random.seed(42)

study_hours = [random.uniform(1, 10) for _ in range(20)]
test_scores = [min(100, max(20, hours * 8 + random.uniform(-10, 10) + 15)) 
               for hours in study_hours]

plt.figure(figsize=(8, 6))
plt.scatter(study_hours, test_scores, color='coral', edgecolor='black', s=60)
plt.xlabel('Hours Studied')
plt.ylabel('Test Score')
plt.title('Study Hours vs Test Score')
plt.grid(True, alpha=0.3)
plt.show()
```

### Your turn

Here are five situations:

- (a) Showing how your daily step count changed over a month
- (b) Comparing the number of bugs found in five different modules of a
  program
- (c) Showing the distribution of response times for a web server
- (d) Looking for a relationship between how much coffee people drink
  and how much work they get done
- (e) Showing what percentage of a project's budget went to each
  department

1. For each situation, choose the chart type you think fits best.
2. Write down why, as a comment in the cell.
3. Pick one of the five, and build its chart with matplotlib. You can
   make up the data.

```python exec
id: your-turn-1
# Your chart type choices (in comments) and one implementation
```

## Writing reusable plotting functions

On the statistics page we wrapped each calculation in a function. We can
do the same with plotting code that we keep writing again. Here is a
function that draws a labelled histogram:

```python exec
id: writing-reusable-plotting-functions-1
def plot_histogram(data, title, xlabel, num_bins=10, colour='steelblue'):
    """Create a labelled histogram from a list of numerical data."""
    plt.figure(figsize=(8, 5))
    plt.hist(data, bins=num_bins, color=colour, edgecolor='black', alpha=0.7)
    plt.xlabel(xlabel)
    plt.ylabel('Frequency')
    plt.title(title)
    plt.show()

# Now we can create histograms with one line
scores = [42, 38, 35, 47, 29, 41, 44, 33, 39, 48,
          31, 36, 43, 27, 45, 40, 37, 34, 46, 32,
          38, 41, 35, 43, 30, 39, 44, 36, 42, 28]

plot_histogram(scores, 'Quiz Score Distribution', 'Score', num_bins=6)
```

The last line draws a whole labelled chart. The details, like the colour
and the axis labels, live inside the function. `num_bins` and `colour`
have default values, so we only give them when we want something
different.

### Your turn

1. Write a function `plot_bar_chart(categories, values, title, xlabel, ylabel)`
   that draws a labelled bar chart. Give it a docstring.
2. Write a function `plot_scatter(x, y, title, xlabel, ylabel)` that
   draws a labelled scatter plot. Give it a docstring too.
3. Test both functions with data from earlier on this page: the
   favourite languages, and the study hours and test scores.

```python exec
id: your-turn-2
# Your plot_bar_chart function
```

```python exec
id: your-turn-3
# Your plot_scatter function
```

```python exec
id: your-turn-4
# Test them
```

## Combining statistics and visualization

We learn the most about a dataset when we look at summary numbers and a
chart together. Here is the start of a function that does both. It
prints a few numbers, and then it draws a histogram with our
`plot_histogram()` function.

```python exec
id: combining-statistics-and-visualisation-1
def analyse_dataset(data, title):
    """Print summary statistics and show a histogram for a dataset."""
    # We are using our functions from *Statistics: averages, spread and frequency*
    # (you may need to redefine mean, median, mode, std_dev here
    #  or copy them from your previous work)
    
    print("=== " + title + " ===")
    print("Count:    ", len(data))
    print("Min:      ", min(data))
    print("Max:      ", max(data))
    # Add calls to mean, median, mode, std_dev here
    print()
    
    plot_histogram(data, title, 'Value')
```

### Your turn

The function is not finished yet. How might you complete it?

1. Bring in your `mean()`, `median()`, `mode()` and `std_dev()`
   functions from
   [Statistics: averages, spread and frequency](tutorial:making-sense-of-data).
   You can copy them from your earlier work, or write them again.
2. Add calls to them inside `analyse_dataset()`, where the comment says.
3. Run `analyse_dataset()` on the quiz scores.
4. If you want a challenge, make a second dataset of your own. Analyse
   both, and compare the two results side by side. What does each chart
   show that its numbers do not?

```python exec
id: your-turn-5
# Your completed analyse_dataset function
```

```python exec
id: your-turn-6
# Apply it
```

## Good practices for visualization

Here are a few rules that help with almost any chart:

- **Title and labels.** Give every chart a clear title, and label both
  axes. Imagine someone sees the chart with no text around it. They
  should still understand what it shows.
- **Colour.** Choose colours to make the chart clearer, not to decorate
  it. For separate categories, use colours that are easy to tell apart.
  For a quantity that changes smoothly, use a *gradient*: one colour
  that goes smoothly from light to dark.
- **No chart junk.** *Chart junk* is anything on a chart that is only
  decoration and carries no information. A simple chart is easier to
  understand.
- **The same scale.** When you compare groups in separate charts, use
  the same scale on each one. Different scales can make a difference
  look bigger or smaller than it is.

### Your turn

Can you find a chart online, in a news article, a textbook or a website,
that communicates well? Can you find one that communicates badly? What
makes each one work, or fail?

## Reflection

Drawing charts and calculating statistics are two parts of the same
job: understanding data. A good analyst moves between numbers and
pictures all the time, and uses each one to check the other.

We now have a complete set of tools for exploring a dataset: counting,
probability, summary statistics and charts. From here on, we use them
together.

What is the most important thing you have learned about presenting
data?

## Where to Read More

Anscombe, F. J. (1973). *Graphs in Statistical Analysis.* The American
Statistician, 27(1), 17–21. The original paper behind the quartet this
page opens with — four datasets, one lesson.

Matplotlib development team. *Pyplot Tutorial.*
<https://matplotlib.org/stable/tutorials/pyplot.html>. The official
reference for everything this page's charts do, and the many options it
does not have room to cover.

CrashCourse (2018). *Charts Are Like Pasta: Data Visualization Part 1:
Crash Course Statistics #5.*
<https://www.youtube.com/watch?v=hEWY6kkBdpo>. Which chart suits which
kind of data, starting with bar charts and pie charts for categories.
About ten minutes.
