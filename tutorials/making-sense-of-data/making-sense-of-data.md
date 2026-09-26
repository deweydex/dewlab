---
title: "Statistics: averages, spread and frequency"
year: "2026-2027"
version: 2026.08.23.1
covers:
  measures-of-central-tendency:
    covers: [MIT-5.12]
  measures-of-spread:
    covers: [MIT-5.12]
  data-types:
    covers: [MIT-5.9]
  frequency-distributions:
    covers: [MIT-5.11]
  visualization-with-matplotlib:
    covers: [MIT-5.10]
  a-note-on-limitations:
    covers: [MIT-5.13]
---

# Statistics: averages, spread and frequency

In the last three tutorials we counted possibilities and worked out probabilities. Now we turn to data. Data is a collection of numbers or labels that somebody has counted, measured or observed.

*Statistics* is the part of mathematics that summarises, describes and explains data. Every tool on this page can become a Python function that we write ourselves.

On this page we:

- find the "typical" value of a dataset in three ways: the mean, the median and the mode
- measure how spread out the data is
- sort data into kinds, and see which tools suit each kind
- count how often values appear, and draw the counts as a histogram
- look at how a summary can mislead

## A dataset to work with

A *dataset* is one collection of data that belongs together. Here is ours: the scores of 30 students on a programming quiz, marked out of 50. The scores are made up, and kept small enough that you can check any result on this page by hand.

```python exec
id: a-dataset-to-work-with-1
scores = [42, 38, 35, 47, 29, 41, 44, 33, 39, 48,
          31, 36, 43, 27, 45, 40, 37, 34, 46, 32,
          38, 41, 35, 43, 30, 39, 44, 36, 42, 28]

print("Number of students:", len(scores))
print("First few scores:", scores[:5])
```

A list of 30 numbers on its own does not tell us very much. We need to summarise it. The first question to ask is: what is a "typical" score?

## Measures of central tendency

A *measure of central tendency* is a single number that describes the centre, or typical value, of a dataset. There are three common ones.

The *mean* is the ordinary average. To find it, we add up all the values and divide by how many values there are. In symbols, with $n$ values $x_1, x_2, \ldots, x_n$:

$$\bar{x} = \frac{1}{n}\sum_{i=1}^{n} x_i$$

We write the mean as $\bar{x}$ and say "x bar". The $\sum$ sign means "add up". For example, the mean of 2, 4 and 9 is $\frac{2 + 4 + 9}{3} = \frac{15}{3} = 5$.

The *median* is the middle value when the data is sorted. The median of 2, 4 and 9 is 4. If there is an even number of values, there are two middle values, and the median is their average. The median of 2, 4, 9 and 11 is $\frac{4 + 9}{2} = 6.5$.

The *mode* is the value that appears most often. The mode of 3, 5, 5 and 8 is 5.

| Measure | How to find it | Example |
|---|---|---|
| Mean | Add up the values, then divide by how many there are | 2, 4, 9 gives 5 |
| Median | Sort the values, then take the middle one | 2, 4, 9 gives 4 |
| Mode | Find the value that appears most often | 3, 5, 5, 8 gives 5 |

Each one describes "typical" in a different way, and they can give quite different answers.

### Your turn

1. Write `mean(data)`. You wrote a `mean` function in
   [Designing and testing good functions](tutorial:building-reusable-tools),
   so you can copy it here or write it again.
2. Write `median(data)`. You need to sort the data first. Python's
   built-in `sorted()` gives back a new sorted list, and leaves the old
   list as it was. We wrote our own sorts in
   [Sorting a list: bubble, insertion and selection sort](tutorial:putting-things-in-order),
   so now we can use Python's.
3. Write `mode(data)`. For this, you need to count how many times each
   value appears.
4. Give each function a docstring.
5. Run the last cell, which uses all three on the scores.

A dictionary, from
[Dictionaries: looking things up by name](tutorial:looking-things-up-by-name),
is a good tool for counting. Here is a short reminder of how one works:

```python exec
id: your-turn-1
# Quick dictionary refresher if you have not used them before
counts = {}                    # empty dictionary
counts["apples"] = 5           # set a key-value pair
counts["bananas"] = 3
print(counts)
print(counts["apples"])

# Check if a key exists
if "oranges" in counts:
    print(counts["oranges"])
else:
    print("no oranges")
```

```python exec
id: your-turn-2
# Your mean function (with docstring)
```

```python exec
id: your-turn-3
# Your median function (with docstring)
```

```python exec
id: your-turn-4
# Your mode function (with docstring)
# Think about: what if there are multiple modes?
```

```python exec
id: your-turn-5
# Apply all three to the scores
print("Mean:", mean(scores))
print("Median:", median(scores))
print("Mode:", mode(scores))
```

### Interpreting the results

Do your three measures agree? Are they close together or far apart?

Look at your mode. Did your function find one mode, or several? What does that tell you about how useful the mode is for these scores?

When the three measures differ, what might that tell us about the shape of the data?

### When measures disagree

Here is a small dataset of salaries, in thousands of euro: 30, 32, 33, 35, 35, 36, 38, 40 and 250.

One of these values is very different from the others. An *outlier* is a value that is far away from the rest of the data. Here, 250 is an outlier.

What do you think the outlier will do to the mean? What will it do to the median? Make a guess, then run the cell.

```python exec
id: when-measures-disagree-1
# Demonstrate the effect of an outlier
salaries = [30, 32, 33, 35, 35, 36, 38, 40, 250]
print("Mean:", mean(salaries))
print("Median:", median(salaries))
print("Mode:", mode(salaries))
# Which one best represents a "typical" salary?
```

The outlier pulls the mean up a long way, to nearly 59. The median is 35, and the outlier hardly changes it. The median only depends on which value is in the middle, so one very large value moves it by at most one place.

A measure is *robust* when an outlier hardly changes it. The median is robust, and the mean is not. Data is *skewed* when it has a long tail of values on one side. Incomes are skewed: most people earn a middle amount, and a few earn very large amounts. This is why people often use the median for skewed data such as incomes.

## Measures of spread

The centre tells us only part of what we want to know. Two datasets can have the same mean but look very different. In one, the values might be close together. In the other, they might be spread far apart.

A *measure of spread* is a number that describes how spread out the values are. We look at two.

The *range* is the largest value minus the smallest value. It is the simplest measure of spread. The range of 2, 4 and 9 is $9 - 2 = 7$.

We met the standard deviation in [Designing and testing good functions](tutorial:building-reusable-tools), where we wrote a function for it. It measures how far the values are from the mean, on average. Here is the idea again, in four steps:

1. Find how far each value is from the mean.
2. Square each of those distances. This makes them all positive.
3. Find the average of the squares.
4. Take the square root. This brings the answer back to the same units as the data.

The formula writes those four steps in symbols:

$$\sigma = \sqrt{\frac{1}{n}\sum_{i=1}^{n}(x_i - \bar{x})^2}$$

We write the standard deviation as $\sigma$, the Greek letter sigma.

Let's try it on 2, 4 and 9, whose mean is 5. The distances from the mean are $-3$, $-1$ and $4$. Their squares are 9, 1 and 16. The average of the squares is $\frac{9 + 1 + 16}{3} = \frac{26}{3} \approx 8.67$. The square root of 8.67 is about 2.94, so the standard deviation is about 2.94.

Some books and calculators divide by $n - 1$ in place of $n$. That version is called the *sample standard deviation*, and it gives a slightly larger answer. On this page we divide by $n$, as the formula shows.

### Your turn

1. Write `data_range(data)`.
2. Write `std_dev(data)`. Use your `mean` function inside it.
3. Run the third cell to use both on the scores.

Here are the steps for `std_dev`, in pseudocode:
```
COMPUTE the mean of the data
FOR each value:
    COMPUTE (value - mean) squared
    ADD it to a running total
DIVIDE the total by the number of values
RETURN the square root of the result
```

```python exec
id: your-turn-6
# Your data_range function
```

```python exec
id: your-turn-7
# Your std_dev function (use your mean function!)
```

```python exec
id: your-turn-8
# Apply to the scores
print("Range:", data_range(scores))
print("Standard deviation:", round(std_dev(scores), 2))
```

What does your standard deviation tell you? The scores have a mean of about 38 and a standard deviation of about 5.7. One standard deviation either side of the mean runs from about 32.4 to 43.8, and 18 of the 30 scores fall inside it.

If the standard deviation were 15, the scores would be much more spread out. If it were 1, they would all be very close to the mean.

### Your turn

Can you make up two datasets that have the same mean, but very different standard deviations? Use your functions to check.

```python exec
id: your-turn-9
# Two datasets with the same mean but different spreads
```

## Data types

Data comes in different kinds. Before we use a statistical tool, we need to know what kind of data we have, because not every tool suits every kind. (These kinds are different from Python's data types, such as `int` and `str`, from [Variables, data types and text](tutorial:storing-and-computing).)

*Categorical* data, also called *nominal* data, is made of labels with no natural order. Examples are a favourite programming language, the colour of a car, or a type of pet. We can find the mode, but a mean has no meaning.

*Ordinal* data is made of labels that have a natural order, but the steps between them are not equal. Examples are a skill level (beginner, intermediate, advanced) or a satisfaction rating from 1 to 5 stars. The median makes sense. People disagree about whether the mean does.

*Discrete* numerical data is made of values we count, so they are whole numbers. Examples are the number of bugs in a program, or the number of students in a class. All our tools work.

*Continuous* numerical data is made of values we measure, and they can be any number in a range. Examples are temperature, time and weight. All our tools work.

| Kind of data | Example | Mode | Median | Mean |
|---|---|---|---|---|
| Categorical (nominal) | colour of a car | yes | no | no |
| Ordinal | star rating | yes | yes | people disagree |
| Discrete numerical | number of bugs | yes | yes | yes |
| Continuous numerical | temperature | yes | yes | yes |

### Your turn

What kind of data is each of these? Which measures of central tendency (mean, median, mode) make sense for it? Write your answers as comments in the cell.

1. The brands of laptops in a classroom
2. Student satisfaction ratings (1 to 5)
3. The number of commits each developer made this week
4. The time (in seconds) each student took to complete a quiz

```python exec
id: your-turn-10
# Your answers (in comments)
# 1. Laptop brands:
# 2. Satisfaction ratings:
# 3. Number of commits:
# 4. Time to complete:
```

## Frequency distributions

The *frequency* of a value is how many times it appears in the data. A *frequency distribution* is a list of the values, or groups of values, with how often each one appears. It often tells us more than any single summary number.

Some data has only a few different values, such as a dice score from 1 to 6. Then we can count each value on its own.

Other data has many different values, such as our quiz scores or any continuous data. Then we split the range of the data into equal groups. A *bin* is one of those groups, such as the scores from 27 to 31. We count how many values fall in each bin.

### Your turn

How might you write a function `frequency_table(data, num_bins)`?

1. Split the range of the data into `num_bins` bins of equal width.
2. Count how many values fall in each bin.
3. Return a list with one pair for each bin. Each pair holds the bin's range and its count, such as `((27, 31.2), 5)`. A pair in round brackets like this is a tuple, as in
   [Probability: simple, compound and conditional](tutorial:what-are-the-chances).

Here are the steps in pseudocode. The notation `[lower, upper)` means "from `lower` up to `upper`, including `lower` but not `upper`".
```
FIND the minimum and maximum of the data
COMPUTE bin_width = (max - min) / num_bins
FOR each bin:
    SET lower = min + bin_number * bin_width
    SET upper = lower + bin_width
    COUNT how many values fall in [lower, upper)
    (for the last bin, include values equal to max)
RETURN the list of (range, count) pairs
```

```python exec
id: your-turn-11
# Your frequency_table function
```

```python exec
id: your-turn-12
# Test it with the scores
table = frequency_table(scores, 5)
for bin_range, count in table:
    print(bin_range, ":", count)
```

## Visualization with matplotlib

Numbers are useful, but a picture can show patterns that are hard to see in numbers. A *histogram* is a chart of a frequency distribution. It has one bar for each bin, and the height of the bar is the count.

To draw one, we use matplotlib, a Python module for drawing charts. The line `import matplotlib.pyplot as plt` loads it, and lets us call it by the short name `plt`. Run the cell to draw a histogram of our scores.

```python exec
id: visualisation-with-matplotlib-1
import matplotlib.pyplot as plt

plt.figure(figsize=(8, 5))
plt.hist(scores, bins=5, edgecolor='black', alpha=0.7)
plt.xlabel('Score')
plt.ylabel('Frequency')
plt.title('Distribution of Quiz Scores')
plt.show()
```

The `hist()` function splits the data into bins and draws the bars for us. `edgecolor='black'` draws a black line around each bar, so we can see where one bar ends and the next begins. `alpha` sets how see-through the bars are, from 0 (invisible) to 1 (solid).

### Your turn

What happens when you draw the histogram with a different number of bins? Try 3, 5, 8 and 12.

Which number of bins shows the shape of the scores best? With too few bins, what do you lose? With too many, what gets in the way? Choosing the number of bins is a judgement, and part of the skill of working with data.

```python exec
id: your-turn-13
# Experiment with different numbers of bins
```

### Interpreting the shape

A histogram is *symmetric* when its left half and right half are roughly mirror images of each other. A histogram with one peak is called *unimodal*.

When you look at a histogram, ask yourself:

- Is it roughly symmetric, or is it skewed to one side?
- Does it have a single peak, or several peaks?
- Are there gaps or outliers?

What do you observe about the score distribution?

## A note on limitations

Summaries are useful, but they can also mislead. The mean of 0, 0, 0, 0 and 100 is 20. But 20 is not typical of anything in that dataset.

A histogram can also look very different when the bin width changes. So it helps to look at the data in several ways, and to be clear about what the numbers tell you and what they do not.

Knowing when a tool suits the data, and when it might mislead, is as important as knowing how to work it out.

## Reflection

We have built a full set of tools that describe data: mean, median, mode, range, standard deviation, frequency tables and histograms. We wrote and tested each of the functions ourselves.

The order matters. First we found a single typical value (central tendency). Then we measured the spread. Then we looked at the whole distribution. Each step gives us more information, and together they give us a full picture of a dataset.

You can now build these tools yourself, starting from nothing, and use them on real problems in probability and data analysis. In the next tutorial,
[Charts: choosing the right chart for your data](tutorial:pictures-worth-numbers),
we look at more ways to draw data.

What surprised you about working with data?

## Where to Read More

Josh Starmer (StatQuest) (2019). *Calculating the Mean, Variance and
Standard Deviation, Clearly Explained!!!*
<https://www.youtube.com/watch?v=SzZ6GpcfoQY>. The same three measures
this page builds as functions, worked through by hand first.
