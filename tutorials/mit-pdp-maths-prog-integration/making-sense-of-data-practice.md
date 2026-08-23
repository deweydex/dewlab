---
title: "Making Sense of Data — Practice"
slug: making-sense-of-data-practice
practice_for: making-sense-of-data
module: mit-pdp-maths-prog-integration
module_title: "Programming and Maths, Integrated"
year: "2026-2027"
series: maths-and-programming
version: 2026.08.23.1
---

# Making Sense of Data — Practice

Answers are folded. Compute the statistics by hand on the small sets — five numbers is quick, and doing it once is what makes the formulae stop being formulae.

Adapted in part from the statistics and probability worksheet in the Mathematics repository.

## Tools

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

## Central Tendency

**1.** For `[4, 8, 6, 5, 3, 8, 2]`, find the mean, median and mode.

<details class="dl-answer"><summary>answer</summary>

Mean 5.143, median 5, mode 8.

Sorted: 2, 3, 4, 5, 6, 8, 8. Seven values, so the median is the fourth.

</details>

**2.** For `[10, 12, 14, 16]`, find the median.

<details class="dl-answer"><summary>answer</summary>

13 — the mean of the two middle values.

An even-length list has no single middle, so the convention is to average the pair. The median need not be a value that occurs in the data.

</details>

**3.** Nine people in an office earn €30,000 and the director earns €500,000. Find the mean and median salary. Which describes the office better?

<details class="dl-answer"><summary>answer</summary>

Mean €77,000, median €30,000.

The median. Not a single person earns anything near the mean, and quoting it would be technically true and actively misleading.

The mean is dragged by outliers because every value contributes its full size. The median only cares about position, so one enormous value moves it by at most one place.

</details>

**4.** When is the mean the better summary?

<details class="dl-answer"><summary>answer</summary>

When the data is roughly symmetric with no extreme values, and when the total matters.

If you want to know how much the office costs in salary, the mean is exactly right — it is the total divided by the count. If you want to know what a typical person earns, it is not.

The right question is not which is better but which question is being asked.

</details>

**5.** Give a dataset where the mode is useless, and one where it is the only sensible measure.

<details class="dl-answer"><summary>answer</summary>

Useless: any set of measured values where every reading is distinct — heights to the millimetre, say. Every value occurs once and the "mode" is whichever happens to repeat by accident, or none.

Essential: categorical data. The mean of `["red", "blue", "red"]` does not exist, and the mode does — it is the most common category, and that is the only average available.

</details>

## Spread

**6.** For `[2, 4, 4, 4, 5, 5, 7, 9]`, compute the mean, then the population standard deviation by hand.

<details class="dl-answer"><summary>answer</summary>

Mean 5, standard deviation 2.

The deviations are −3, −1, −1, −1, 0, 0, 2, 4. Squared: 9, 1, 1, 1, 0, 0, 4, 16, which sum to 32. Divide by 8 to get the variance, 4, and take the square root.

This dataset is chosen so the numbers come out whole, which almost never happens with real data.

</details>

**7.** Why square the deviations rather than just adding them?

<details class="dl-answer"><summary>answer</summary>

Because they sum to zero, always. The mean is exactly the point where the positives and negatives cancel.

Squaring makes everything positive, and it also weights large deviations much more heavily — which is a choice, not a necessity. Taking absolute values instead gives the mean absolute deviation, which is a perfectly good measure and is harder to do algebra with.

</details>

**8.** Two classes both average 65%. One has a standard deviation of 3, the other 20. What does that tell you?

<details class="dl-answer"><summary>answer</summary>

The first class is uniform; the second has both strong and struggling students in it.

Same mean, completely different teaching problem. This is the argument for never reporting an average alone — a centre without a spread describes almost nothing.

</details>

**9.** What is the difference between dividing by n and by n − 1?

<details class="dl-answer"><summary>answer</summary>

Dividing by n gives the population standard deviation: the actual spread of the numbers you have.

Dividing by n − 1 gives the sample standard deviation: an estimate of the spread of a larger population that these numbers were drawn from.

The n − 1 is a correction. A sample's own mean sits closer to the sample than the true mean does, so the deviations come out slightly too small, and dividing by a slightly smaller number compensates.

For n = 100 the difference is half a percent. For n = 5 it is over 10%, which is exactly when people are most tempted to ignore it.

</details>

**10.** Add 10 to every value in a dataset. What happens to the mean, the median, the range and the standard deviation?

<details class="dl-answer"><summary>answer</summary>

The mean and median both go up by 10. The range and standard deviation do not change at all.

Measures of centre shift with the data; measures of spread do not, because every deviation from the mean is the same as it was.

Multiply everything by 3 instead and all four triple — the spread measures scale even though they do not shift.

</details>

## Data Types

**11.** Classify each as nominal, ordinal, interval or ratio.

- (a) Eye colour
- (b) Exam grade (Pass, Merit, Distinction)
- (c) Temperature in Celsius
- (d) Height in centimetres
- (e) Shirt number on a football kit

<details class="dl-answer"><summary>answer</summary>

(a) Nominal. (b) Ordinal. (c) Interval. (d) Ratio. (e) Nominal, despite being a number.

(c) and (d) differ over whether zero means "none". 20 °C is not twice as hot as 10 °C, because 0 °C is a chosen point rather than an absence of heat. 20 cm genuinely is twice 10 cm.

(e) is the trap. Averaging shirt numbers is arithmetically possible and meaningless, and a program will do it without complaint.

</details>

**12.** Which averages make sense for each type?

<details class="dl-answer"><summary>answer</summary>

Nominal: mode only. Ordinal: mode and median — you can put them in order, so a middle exists. Interval and ratio: all three.

The measure has to respect what the numbers actually mean, and there is nothing in the data itself that will stop you.

</details>

## Frequency and Shape

**13.** Build a frequency table for `[1, 2, 2, 3, 3, 3, 4, 4, 4, 4]`, and describe the shape.

<details class="dl-answer"><summary>answer</summary>

1 appears once, 2 twice, 3 three times, 4 four times.

```python
from collections import Counter
print(Counter(data))
```

The shape rises steadily to the right — skewed left, in the standard and confusing terminology, because the *tail* is on the left. The name refers to the tail, not to where the bulk sits.

</details>

**14.** For a right-skewed distribution — a long tail of large values — how do the mean, median and mode compare?

<details class="dl-answer"><summary>answer</summary>

Mode < median < mean.

The tail pulls the mean furthest, the median a little, the mode not at all. Income distributions are the standard example, and it is why "average income" and "typical income" are different numbers in every country.

</details>

**15.** Sketch a distribution where the mean and median are equal but the data is not symmetric.

<details class="dl-answer"><summary>answer</summary>

Any distribution with balanced tails of different shapes will do. `[1, 5, 6, 7, 11]` has mean and median both 6, and is not symmetric.

Equal mean and median is a hint of symmetry, not a proof of it. Every summary statistic loses information, and the only reliable way to know the shape is to look at it.

</details>

## Putting It Together

**16.** Ten exam marks: `[45, 52, 68, 71, 71, 74, 78, 82, 89, 95]`. Compute a full summary and describe the class.

<details class="dl-answer"><summary>answer</summary>

Mean 72.5, median 72.5, mode 71, range 50, population standard deviation about 14.5.

The mean and median agreeing suggests a fairly symmetric spread. A standard deviation of 14 on a mean of 72 means most marks fall roughly between 58 and 87, which the data bears out.

The range of 50 is the least informative number here: it depends entirely on two students.

</details>

**17.** Add a mark of 12 to that list. What changes most?

<details class="dl-answer"><summary>answer</summary>

Mean drops to 67, median only to 71, and the standard deviation jumps to about 22.2.

One value in eleven moved the mean by 5.5 marks and the median by 1.5. The standard deviation rose by half, because the deviation is squared and 55 squared is a large number.

Standard deviation is even more outlier-sensitive than the mean, which is worth remembering before using it to decide anything.

</details>

**18.** Two datasets have the same mean, median, standard deviation and correlation. Can they look different?

<details class="dl-answer"><summary>answer</summary>

Completely.

Anscombe's quartet is four datasets agreeing on all of those to two decimal places: one is a clean line, one is a curve, one is a line with a single outlier, and one is a vertical stack with one point far off. The Datasaurus dozen extends the trick to a picture of a dinosaur.

This is the strongest available argument for the next tutorial. **Plot the data.** Summary statistics answer the questions you thought to ask, and a picture answers the one you did not.

</details>
