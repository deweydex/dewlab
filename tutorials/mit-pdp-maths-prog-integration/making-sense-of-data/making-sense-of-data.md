---
title: "Making Sense of Data"
slug: making-sense-of-data
module: mit-pdp-maths-prog-integration
module_title: "Programming and Maths, Integrated"
year: "2026-2027"
series: data-chance-and-logic
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
  visualisation-with-matplotlib:
    covers: [MIT-5.10]
  a-note-on-limitations:
    covers: [MIT-5.13]
---

# Making Sense of Data

**Programming Design Principles / Maths for IT**

We have learned to count possibilities and calculate probabilities. Now we turn to actual data: numbers that have been collected, measured, or observed. Statistics gives us tools to summarise, describe, and interpret data -- and every one of those tools translates into a function we can write.

## A Dataset to Work With

Let's start with something concrete. Here are the scores of 30 students on a programming quiz, marked out of 50:

```python exec
id: a-dataset-to-work-with-1
scores = [42, 38, 35, 47, 29, 41, 44, 33, 39, 48,
          31, 36, 43, 27, 45, 40, 37, 34, 46, 32,
          38, 41, 35, 43, 30, 39, 44, 36, 42, 28]

print("Number of students:", len(scores))
print("First few scores:", scores[:5])
```

Looking at a raw list of 30 numbers does not tell us very much. We need to summarise. The most fundamental question is: what is a "typical" value?

## Measures of Central Tendency

There are three classic ways to define the "centre" of a dataset.

**Mean** (arithmetic average): add everything up and divide by the count.

$$\bar{x} = \frac{1}{n}\sum_{i=1}^{n} x_i$$

**Median**: the middle value when the data is sorted. If there is an even number of values, take the average of the two middle ones.

**Mode**: the value that appears most frequently.

Each captures a different notion of "typical," and they can give quite different answers.

### Your turn

Let's write three functions: `mean(data)`, `median(data)`, and `mode(data)`.

For `mean`, you have already written this -- bring it forward or rewrite it. For `median`, you will need to sort the data first (use Python's built-in `sorted()` -- we earned that right after building our own sorts). For `mode`, think about how to count how many times each value appears. A dictionary is a natural tool here:

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

Do your three measures agree? Are they close together or far apart? When they differ, what does that tell us about the shape of the data?

What's your interpretation?

### When measures disagree

Consider this dataset of salaries (in thousands): [30, 32, 33, 35, 35, 36, 38, 40, 250].

The mean will be pulled up dramatically by the outlier (250). The median will barely notice it. This is why the median is often preferred for skewed data like income distributions -- it is *robust* to outliers.

```python exec
id: when-measures-disagree-1
# Demonstrate the effect of an outlier
salaries = [30, 32, 33, 35, 35, 36, 38, 40, 250]
print("Mean:", mean(salaries))
print("Median:", median(salaries))
print("Mode:", mode(salaries))
# Which one best represents a "typical" salary?
```

## Measures of Spread

Knowing the centre is only half the story. Two datasets can have the same mean but very different shapes: one might be tightly clustered, the other wildly spread out.

**Range**: the simplest measure of spread. Maximum minus minimum.

**Standard deviation**: measures how far, on average, each data point is from the mean.

$$\sigma = \sqrt{\frac{1}{N}\sum_{i=1}^{N}(x_i - \bar{x})^2}$$

The formula looks complicated, but the idea is straightforward: find each value's distance from the mean, square those distances (to make them all positive), average them, and take the square root to get back to the original units.

### Your turn

Let's write `data_range(data)` and `std_dev(data)`. For `std_dev`, break the calculation into steps:

**Pseudocode:**
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

A standard deviation of about 5-6 on data with a mean around 38 tells us that most scores are within 5-6 points of the mean. If the standard deviation were 15, the scores would be much more spread out. If it were 1, they would be tightly clustered.

### Your turn

See if you can create two artificial datasets with the same mean but very different standard deviations, then verify using your functions.

```python exec
id: your-turn-9
# Two datasets with the same mean but different spreads
```

## Data Types

Not all data is the same. Before applying statistical tools, we need to know what kind of data we are working with:

**Categorical (nominal)**: labels with no inherent order. Favourite programming language, colour of car, type of pet. You can count the mode but the mean is meaningless.

**Ordinal**: categories with a natural order but no consistent spacing. Skill level (beginner, intermediate, advanced), satisfaction rating (1-5 stars). The median makes sense but the mean is debatable.

**Discrete numerical**: countable values. Number of bugs in a program, number of students in a class. All our statistical tools work.

**Continuous numerical**: values that can take any real number in a range. Temperature, time, weight. All our statistical tools work.

### Your turn

For each of the following, what data type is it, and which measures of central tendency (mean, median, mode) would be appropriate?

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

## Frequency Distributions

A frequency distribution shows how often each value (or range of values) occurs. This is often more informative than any single summary number.

For discrete data with few unique values, we can count each one directly. For continuous data or discrete data with many unique values, we group the data into *bins* (ranges) and count how many values fall in each bin.

### Your turn

How might you write a function `frequency_table(data, num_bins)` that divides the range of the data into `num_bins` equal-width bins and counts how many values fall in each? Return the result as a list of tuples, where each tuple contains the bin range and the count.

**Pseudocode:**
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

## Visualisation with matplotlib

Numbers are good but pictures can reveal patterns that are hard to see otherwise. Let's make a histogram of our scores:

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

The `hist()` function does the binning and plotting for us. The `edgecolor` makes the bars distinct, and `alpha` controls transparency.

### Your turn

What happens when you create a histogram with different numbers of bins (try 3, 5, 8, and 12)? Too few bins hides detail; too many bins creates noise. Finding the right balance is part of the art of data analysis.

```python exec
id: your-turn-13
# Experiment with different numbers of bins
```

### Interpreting the shape

When you look at a histogram, consider:
- Is it roughly symmetric, or is it skewed to one side?
- Is there a single peak (unimodal) or multiple peaks?
- Are there gaps or outliers?

What do you observe about the score distribution?

## A note on limitations

Statistical summaries are powerful but they can also mislead. The mean of [0, 0, 0, 0, 100] is 20, but 20 is not "typical" of anything in that dataset. A histogram can look very different depending on the bin width. Always look at the data from multiple angles, and be honest about what the numbers do and do not tell you.

This critical awareness -- knowing when a statistical tool is appropriate and when it might mislead -- is as important as knowing how to compute the statistic in the first place.

## Reflection

We have built a complete set of descriptive statistics tools: mean, median, mode, range, standard deviation, frequency distributions, and histograms. Each one is a function we wrote and tested ourselves.

The progression matters: we started with individual numbers (central tendency), then measured spread, then looked at the full distribution. Each level gives us more information. Together they give us a rich picture of a dataset.

You now have everything you need to build these tools yourself, from nothing, and turn them on real probability and data analysis problems.

What surprised you about working with data?

## Where to Read More

Josh Starmer (StatQuest) (2019). *Calculating the Mean, Variance and
Standard Deviation, Clearly Explained!!!*
<https://www.youtube.com/watch?v=SzZ6GpcfoQY>. The same three measures
this page builds as functions, worked through by hand first.
