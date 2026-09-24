---
title: "Statistics: averages, spread and frequency — Practice"
practice_for: making-sense-of-data
year: "2026-2027"
version: 2026.08.23.1
---

# Statistics: averages, spread and frequency — Practice

Each answer is hidden until you open it. On the small datasets, try working out the statistics by hand. Five numbers do not take long. Doing it by hand once helps a formula make sense, so that it feels like more than symbols.

Adapted in part from the statistics and probability worksheet in the Mathematics repository.

## Tools

This cell uses Python's `statistics` module, which has the measures from the tutorial built in. Run it to check your own functions against it. `pstdev` is the standard deviation that divides by $n$, and `stdev` is the one that divides by $n - 1$.

```python exec
id: tools-1
import statistics

data = [12, 15, 15, 18, 22, 25, 25, 25, 30, 45]

print("mean    ", statistics.mean(data))
print("median  ", statistics.median(data))
print("mode    ", statistics.mode(data))
print("range   ", max(data) - min(data))
print("pop sd  ", round(statistics.pstdev(data), 4))
print("samp sd ", round(statistics.stdev(data), 4))
```

## Central tendency

**1.** What are the mean, median and mode of `[4, 8, 6, 5, 3, 8, 2]`?

<details class="dl-answer"><summary>answer</summary>

The mean is about 5.143, the median is 5, and the mode is 8.

The values add up to 36, and there are 7 of them, so the mean is $\frac{36}{7} \approx 5.143$. Sorted, the values are 2, 3, 4, 5, 6, 8, 8. There are seven values, so the median is the fourth one.

</details>

**2.** What is the median of `[10, 12, 14, 16]`?

<details class="dl-answer"><summary>answer</summary>

13, which is the mean of the two middle values, 12 and 14.

A list with an even number of values has no single middle value, so we agree to take the average of the middle two. So the median does not have to be one of the values in the data.

</details>

**3.** Nine people in an office earn €30,000 each, and the director earns €500,000. What are the mean and median salaries? Which one describes the office better?

<details class="dl-answer"><summary>answer</summary>

The mean is €77,000, and the median is €30,000.

The median describes the office better. Nobody in the office earns anything near the mean. Quoting the mean would be true, but it would mislead people.

An outlier pulls the mean a long way, because every value adds its full size to the total. The median depends only on position, so one very large value moves it by at most one place.

</details>

**4.** When is the mean the better summary?

<details class="dl-answer"><summary>answer</summary>

The mean is the better summary when the data is roughly symmetric with no outliers. It is also the right choice when the total matters.

Say you want to know how much the office costs in salaries. Then the mean is exactly right, because it is the total divided by the count. But if you want to know what a typical person earns, the mean is the wrong choice.

So first ask which question you are trying to answer. That tells you which measure is better.

</details>

**5.** Can you think of a dataset where the mode is useless? And one where the mode is the only sensible measure?

<details class="dl-answer"><summary>answer</summary>

**Useless:** any set of measured values where every value is different, such as heights measured to the millimetre. Every value appears once. So the "mode" is whichever value happens to repeat by chance, or there is none.

**The only sensible measure:** categorical data. The list `["red", "blue", "red"]` has no mean. But it has a mode, "red", which is the most common category. It is the only average we can use.

</details>

## Spread

**6.** For `[2, 4, 4, 4, 5, 5, 7, 9]`, can you work out the mean by hand, and then the standard deviation that divides by $n$? (This is also called the population standard deviation.)

<details class="dl-answer"><summary>answer</summary>

The mean is 5, and the standard deviation is 2.

The distances from the mean, called deviations, are −3, −1, −1, −1, 0, 0, 2 and 4. Their squares are 9, 1, 1, 1, 0, 0, 4 and 16, which add up to 32. Divide by 8 to get 4. This number, the average of the squared deviations, is called the variance. Its square root is 2.

These numbers were chosen so that everything comes out whole. That almost never happens with real data.

</details>

**7.** Why do we square the deviations? What goes wrong if we add them up as they are?

<details class="dl-answer"><summary>answer</summary>

The deviations always add up to zero. The mean is exactly the point where the positive and negative deviations cancel out.

Squaring makes every deviation positive. It also gives large deviations much more weight. That is a choice, and other choices are possible. We could take the absolute value of each deviation instead, which means dropping its minus sign. That gives the mean absolute deviation. It is a perfectly good measure, but it is harder to work with in algebra.

</details>

**8.** Two classes both average 65%. One has a standard deviation of 3, the other 20. What does that tell you?

<details class="dl-answer"><summary>answer</summary>

In the first class, almost everyone scored close to 65%. The second class has both strong students and students who are struggling.

The mean is the same, but the two classes need very different teaching. This is why we should never report an average alone. A center without a spread tells us very little.

</details>

**9.** What is the difference between dividing by $n$ and dividing by $n - 1$?

<details class="dl-answer"><summary>answer</summary>

Dividing by $n$ gives the population standard deviation. It measures the spread of the numbers you have.

Dividing by $n - 1$ gives the sample standard deviation. Sometimes our numbers are a sample: a few values taken from a much larger group, called the population. The sample standard deviation is an estimate of the spread of that whole population.

The $n - 1$ is a correction. A sample's own mean is never further from the sample's values than the true population mean is. So the deviations come out a little too small. Dividing by a slightly smaller number makes up for that.

For $n = 100$, the two answers differ by about half a percent. For $n = 5$, they differ by more than 10%. Small samples are exactly when people are most tempted to ignore the difference.

</details>

**10.** Suppose we add 10 to every value in a dataset. What happens to the mean, the median, the range and the standard deviation?

<details class="dl-answer"><summary>answer</summary>

The mean and median both go up by 10. The range and standard deviation do not change at all.

Measures of center move with the data. Measures of spread do not move, because every distance from the mean stays the same.

What if we multiply every value by 3 instead? Then all four measures are multiplied by 3. The spread measures do not move when we add, but they do grow when we multiply.

</details>

## Data types

**11.** This question uses two new words. They split numerical data into two kinds, by what zero means:

- Interval data is numbers where zero is a chosen point, not "none". Temperature in Celsius is an example.
- Ratio data is numbers where zero means "none of it". Height is an example.

Is each of these nominal, ordinal, interval or ratio?

- (a) Eye color
- (b) Exam grade (Pass, Merit, Distinction)
- (c) Temperature in Celsius
- (d) Height in centimetres
- (e) Shirt number on a football kit

<details class="dl-answer"><summary>answer</summary>

(a) Nominal. (b) Ordinal. (c) Interval. (d) Ratio. (e) Nominal, even though it is a number.

(c) and (d) differ in whether zero means "none". 20 °C is not twice as hot as 10 °C, because 0 °C is a chosen point. It does not mean there is no heat. But 20 cm is twice 10 cm, because 0 cm really means no height.

(e) is the trap. We can work out the average of shirt numbers, but the answer means nothing. A program will do it without any warning.

</details>

**12.** Which averages make sense for each kind of data in question 11?

<details class="dl-answer"><summary>answer</summary>

- Nominal: the mode only.
- Ordinal: the mode and the median. We can put the values in order, so there is a middle.
- Interval and ratio: all three.

The measure has to fit what the numbers mean. Nothing in the data itself will stop you from choosing the wrong one.

</details>

## Frequency and shape

**13.** Can you build a frequency table for `[1, 2, 2, 3, 3, 3, 4, 4, 4, 4]`? How would you describe its shape?

<details class="dl-answer"><summary>answer</summary>

1 appears once, 2 appears twice, 3 appears three times, and 4 appears four times.

Python's `collections` module has a `Counter` that makes the table for you:

```python
from collections import Counter
print(Counter([1, 2, 2, 3, 3, 3, 4, 4, 4, 4]))
```

The shape rises steadily to the right. Its name is "skewed left", which confuses many people. The name describes the *tail*, the thin end of the shape, and here the tail is on the left. The name does not describe where most of the data is.

</details>

**14.** A right-skewed distribution has a long tail of large values. How do its mean, median and mode compare?

<details class="dl-answer"><summary>answer</summary>

Mode < median < mean.

The tail pulls the mean furthest, the median a little, and the mode not at all. Incomes are the usual example. That is why the mean income and the typical income are different numbers in every country.

</details>

**15.** Can you make a dataset where the mean and the median are equal, but the data is not symmetric?

<details class="dl-answer"><summary>answer</summary>

Any dataset with tails of different shapes that balance each other will do. `[2, 3, 6, 8, 11]` has a mean of 6 and a median of 6. It is not symmetric: below 6 the values are 3 and 4 away, and above 6 they are 2 and 5 away.

When the mean and the median are equal, the data might be symmetric, but it does not have to be. Every summary number loses some information. The only sure way to know the shape is to look at it.

</details>

## Putting it together

**16.** Here are ten exam marks: `[45, 52, 68, 71, 71, 74, 78, 82, 89, 95]`. Can you work out a full summary, and describe the class?

<details class="dl-answer"><summary>answer</summary>

The mean is 72.5, the median is 72.5, the mode is 71, the range is 50, and the population standard deviation is 14.5.

The mean and median are equal, which suggests the marks are spread fairly evenly on both sides. The mean is about 72 and the standard deviation about 14, so most marks should be between about 58 and 87. The data agrees: 6 of the 10 marks are in that range.

The range of 50 tells us the least. It depends on only two students, the highest and the lowest.

</details>

**17.** Now add a mark of 12 to that list. What changes most?

<details class="dl-answer"><summary>answer</summary>

The mean drops to 67, the median drops only to 71, and the standard deviation jumps to about 22.2.

One value out of eleven moved the mean by 5.5 marks and the median by 1.5. The standard deviation grew by half. Why so much? The new mark is 55 below the new mean, and that deviation is squared: $55^2 = 3025$.

So the standard deviation is even more sensitive to outliers than the mean. Remember this before you use it to decide anything.

</details>

**18.** Two datasets have the same mean, median, standard deviation and correlation. Can they look different?

(Correlation is a number that measures how closely pairs of values lie along a straight line. We meet it properly in the next tutorial, [Charts: choosing the right chart for your data](tutorial:pictures-worth-numbers).)

<details class="dl-answer"><summary>answer</summary>

Yes. They can look completely different.

Anscombe's quartet is a famous example that comes very close. It is four datasets of points with the same means, standard deviations and correlation, to about two decimal places. (Their medians differ a little, but the lesson is the same.) When we plot them, one is a clean line, one is a curve, one is a line with a single outlier, and one is a vertical stack with one point far away. The Datasaurus dozen takes the same idea further: one of its datasets draws a dinosaur.

This is the best reason for the next tutorial. **Plot the data.** Summary numbers answer the questions you thought to ask. A picture answers the question you did not think of.

</details>
