---
title: "Mixed problems: many values"
practice_across:
  - a-row-of-numbers
  - what-is-typical
  - kinds-of-data-and-honest-charts
  - collections-without-repeats
  - circles-that-overlap
year: "2026-2027"
version: 2026.09.25.1
datasets: [life-expectancy]
---

# Mixed problems: many values

Each problem here draws on at least one page of Unit 5, and many draw on
two or more. None of them is harder than what those pages covered. The
new part is that nobody tells you which page a problem comes from.
Choosing the tool is part of the problem, and if you are unsure which
tool fits, open the hint: it names the page to look back at.

Along the way, the problems build this unit's product: a one-page
report on real data. It gives typical values, the spread, a frequency
table and one honest chart, for life expectancy in Ireland and in one
other country that you choose. Problems 5, 6, 8, 10, 13 and 15 are the
report's parts, and they build on each other, so do those in order.

Your toolkit is loaded on this page: `largest`, `smallest`, `count_if`,
`mean`, `median`, `mode`, `std_dev` and `frequency_table` from this
unit, and every tool from Units 1 to 4. One warning, from
[Doing it again](tutorial:doing-it-again#two-tools-for-your-toolkit):
a cell that says `mean = ...` or `mode = ...` hides that tool for the
rest of the page. Give your numbers names like `ireland_mean`. Each
answer is hidden until you open it. Where a problem asks you to predict,
make the prediction before you run anything. It is the most useful part.

## Warm-up

Use this cell for any warm-up problem. Paste in the code, and run it.

```python exec
id: mixed-many-scratch-1
# Try things here
```

**1. Predict.** Here are the highest temperatures in Cork on six days
in May. What does the last line show? Work out all four values before
you run it.

```python
temps = [12, 14, 12, 15, 14, 12]
print(len(temps), len(set(temps)), mode(temps), temps[-2:])
```

<details class="dl-answer"><summary>answer</summary>

`6 3 12 [14, 12]`.

The list has six values. The set keeps each value once, so it holds 12,
14 and 15: three values. The mode is 12, which appears three times.
`temps[-2:]` is a slice from the second-last value to the end: the
last two days, 14 and 12. Slices are on
[A row of numbers](tutorial:a-row-of-numbers#a-slice-of-the-week).

</details>

**2. Make.** A smart meter records how much electricity a home uses,
in kilowatt-hours (kWh). Here are seven weeks of one home's readings.
They are made up. In one week a cold snap came, and an electric heater
ran every evening. Find the mean and the median. Which one would you
give as a typical week, and why?

```python
kwh = [78, 72, 81, 75, 160, 77, 74]
```

<details class="dl-answer"><summary>answer</summary>

```python
print(round(mean(kwh), 2), median(kwh))
```

This prints `88.14 77`. The mean is pulled up by the cold week, an
outlier, and it is higher than six of the seven weeks. The median,
77 kWh, is the better answer to "what does a typical week use?". The
mean answers a different question: shared out equally, how much went on
each week? As on
[What is typical?](tutorial:what-is-typical#when-the-three-disagree),
the mean moves towards the tail.

</details>

**3. Explain.** The IT team on
[Circles that overlap](tutorial:circles-that-overlap) asked three
questions of each laptop: "Is it updated?", "Does it have antivirus?"
and "Is it backed up?". What kind of data is the answer to each
question? Could you find the mean answer to "Is it updated?" What could
you say about it instead?

<details class="dl-answer"><summary>answer</summary>

Each answer is yes or no, so it is categorical data, and nominal: yes
and no have no order that means anything here. There is no mean of
"yes" and "no". What we can do is count: a frequency table of the
answers, or the fraction that said yes. The team found 10 updated
laptops in 20, so half said yes. The mode, the most common answer, makes sense too.
The Venn diagram is a picture of those counts, for three questions at
once.

(If you write yes as 1 and no as 0, the mean of the 1s and 0s is the
fraction who said yes. That is a useful trick, and it works because
those numbers count something, not because "yes" is a number.)

</details>

**4. Predict.** A radio station keeps the kind of each song it played in
one hour. What will each line show?

```python
kinds = ["pop", "rock", "pop", "trad", "pop", "rock"]
print(frequency_table(kinds))
print(mode(kinds), len(set(kinds)))
```

<details class="dl-answer"><summary>answer</summary>

```text
{'pop': 3, 'rock': 2, 'trad': 1}
pop 3
```

`frequency_table` keeps its keys in the order it first met them. The
mode is the key with the biggest frequency. And the number of keys is
the number of different values, which is what `len(set(kinds))` counts
too.

</details>

## Core

Run this cell first. It loads the life expectancy file from
[A row of numbers](tutorial:a-row-of-numbers#a-real-list-ireland-since-1950),
and takes out two lists: Ireland's values, one for each year from 1950
to 2016, and another country's. Change `other_country` to the country
you want to compare, such as `"Poland"`, `"Nigeria"` or `"Brazil"`. The
name must be spelled as it is in the file. The answers below use Spain,
so your numbers will differ from them if you choose another country.

```python exec
id: mixed-many-data
df = await load_csv("life-expectancy.csv")
other_country = "Spain"

years = df[df.country == "Ireland"]["year"].tolist()
ireland = df[df.country == "Ireland"]["life_expectancy"].tolist()
other = df[df.country == other_country]["life_expectancy"].tolist()

print(len(ireland), "years for Ireland,", len(other), "for", other_country)
```

If the second number is 0, the name is not in the file: check its
spelling and its capital letters. The problems below expect both lists
to have 67 values, one for each year.

A scratch cell for the core problems:

```python exec
id: mixed-many-scratch-2
# Your work, problem by problem
```

**5. Make.** The report's first line says where each list starts and
ends. For each country, print the first value, the last value, and how
much life expectancy rose between them. Then use slices to find the
mean of the first 10 years and of the last 10 years.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The first value is at index 0, and the last at index −1.
2. The first 10 values are `ireland[:10]`. What slice gives the last 10?
3. `mean` works on any list, so it works on a slice.

**Think about:** which of the four numbers would you put in the
report's first sentence?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
for name, values in [("Ireland", ireland), (other_country, other)]:
    rise = values[-1] - values[0]
    print(name, values[0], values[-1], round(rise, 2))
    print("  first 10 years:", round(mean(values[:10]), 2),
          " last 10 years:", round(mean(values[-10:]), 2))
```

```text
Ireland 65.61 81.14 15.53
  first 10 years: 67.86  last 10 years: 80.54
Spain 61.87 82.97 21.1
  first 10 years: 65.9  last 10 years: 82.19
```

Spain started about 4 years behind Ireland, and ended almost 2 years
ahead. The loop goes through a list of pairs, and takes each pair apart
into `name` and `values`, as on
[How likely is it?](tutorial:how-likely-is-it#counting-equally-likely-outcomes).

</details>

**6. Make.** Now the typical values. Find the mean and the median of
each whole list. For the mode, first make a new list with every value
rounded to a whole year, with a loop and `append`, and take the mode of
that.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. `mean(ireland)` and `median(ireland)` need nothing new.
2. Start a list with `[]`. Go through `ireland`, and `append`
   `round(value)` each time round.
3. Take `mode` of the new list.

**Think about:** why would `mode(ireland)`, without rounding, tell you
almost nothing?

</details>

<details class="dl-answer"><summary>answer</summary>

One way through; yours may differ and work as well.

```python
def whole_years(values):
    """Return a new list with every value rounded to a whole number."""
    rounded = []
    for value in values:
        rounded.append(round(value))
    return rounded


for name, values in [("Ireland", ireland), (other_country, other)]:
    print(name, round(mean(values), 2), median(values), mode(whole_years(values)))
```

```text
Ireland 73.79 73.26 71
Spain 75.03 76.3 76
```

Life expectancy is continuous, so almost no two values are exactly the
same, and every value would be "most common" once. Rounding makes the
values repeat. Even so, the mode here is the most common whole number
of years, which is not the most useful fact in the report. The mean and
median say more. For Spain the median is well above the mean, because
Spain's low early years form a tail to the left.

</details>

**7. Explain.** Ireland's standard deviation over these 67 years is
about 4.2 years. On
[What is typical?](tutorial:what-is-typical#the-standard-deviation) the
standard deviation measured how spread out a list is. What is spread out
here? Is it how long people in Ireland live?

<details class="dl-answer"><summary>answer</summary>

No. Each value is one year's life expectancy for the whole country, so
the list has one value per year, not one per person. The spread is
across time: it says how much the yearly figure changed over 67 years.
A list that rises steadily has a large spread even if every single year
was very predictable. How long individual people live varies far more
than 4.2 years, and this file cannot tell us about that. A report
should say what one value in its list stands for, so that a reader does
not read the spread as something else.

</details>

**8. Make.** The spread, for the report. For each country, find the
range and the standard deviation. Which country's life expectancy
changed more over the years?

<details class="dl-answer"><summary>answer</summary>

```python
for name, values in [("Ireland", ireland), (other_country, other)]:
    spread = largest(values) - smallest(values)
    print(name, "range:", round(spread, 2), " std dev:", round(std_dev(values), 2))
```

```text
Ireland range: 16.36  std dev: 4.18
Spain range: 21.45  std dev: 5.39
```

Spain's values are more spread out by both measures, because Spain rose
further: from about 61.5 years to about 83. Notice that the range uses
`largest` and `smallest`, not the first and last values. They are
nearly the same here, because both lists mostly rise, and in a list that
went up and down they would not be.

</details>

**9. Fix.** Schlomo, who is learning Python too, writes the typical
values into his report like this. He names the number `mean` because
that is what it is. The first line runs. The cell is meant to stop with
an error on the second. Read the last line of the error, then find the
line that does not do what Schlomo meant.

```python exec
id: mixed-many-fix-hidden
mean = mean(ireland)
other_mean = mean(other)
print(round(mean, 2), round(other_mean, 2))
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The last line of the error is `TypeError: 'float' object is not
   callable`. Which thing on that line is being called?
2. After the first line runs, what does the name `mean` point at?
3. On [What a function can see](tutorial:what-a-function-can-see), and
   in the note at the top of this page, what happens when a cell reuses
   a toolkit function's name?

**Think about:** renaming a number changes nothing for Python. What
does repointing a name change?

</details>

<details class="dl-answer"><summary>answer</summary>

Schlomo's name is honest, and that is the trouble. The first line
points the name `mean` at a number, 73.79…, and the function is gone
from this page. On the second line, `mean(other)`
tries to call that number, and a number cannot be called. Give the
number its own name:

```python
ireland_mean = mean(ireland)
other_mean = mean(other)
print(round(ireland_mean, 2), round(other_mean, 2))
```

To get the tool back after the broken cell has run, run
`del mean` in the scratch cell. That removes the page's name, so
`mean` means the toolkit's function again. (Reloading the page does the
same.)

</details>

**10. Make.** The frequency table, for the report. Put each country's
values into bins 5 years wide, as on
[Kinds of data, and honest charts](tutorial:kinds-of-data-and-honest-charts#histograms-for-measured-numbers),
and count them with `frequency_table`. Print each table in order, from
the lowest bin up.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. `int(age // 5 * 5)` gives the start of the bin that `age` is in.
2. Build a list of bin starts with a loop, then give it to
   `frequency_table`.
3. `sorted(table)` gives the keys of a dictionary in order.

**Think about:** do the frequencies in each table add up to 67?

</details>

<details class="dl-answer"><summary>answer</summary>

One way through; yours may differ and work as well.

```python
def five_year_bins(values):
    """Return a frequency table of values in bins 5 wide, keyed by where each bin starts."""
    starts = []
    for value in values:
        starts.append(int(value // 5 * 5))
    return frequency_table(starts)


for name, values in [("Ireland", ireland), (other_country, other)]:
    table = five_year_bins(values)
    print(name)
    for start in sorted(table):
        print(" ", start, "to", start + 5, "years:", table[start])
```

For Ireland, the bins from 60 up hold 1, 11, 29, 19 and 7 years. For
Spain they hold 3, 11, 15, 25 and 13. Each adds up to 67. Ireland spent
the most years in the 70 to 75 bin, and Spain in the 75 to 80 bin.

</details>

**11. Predict.** In how many of the 67 years was life expectancy 75 or
more, in each country? Guess from the frequency tables in problem 10,
then check with `count_if`.

<details class="dl-answer"><summary>answer</summary>

```python
def seventy_five_or_more(years_expected):
    """True when a life expectancy is 75 years or more."""
    return years_expected >= 75


print(count_if(ireland, seventy_five_or_more), count_if(other, seventy_five_or_more))
```

This prints `26 38`. The frequency tables give the same answer without
a new count: the bins from 75 up hold $19 + 7 = 26$ years for Ireland,
and $25 + 13 = 38$ for Spain.

</details>

**12. Another way.** Which years had Ireland at 75 or more, which had
the other country at 75 or more, and which had both? Make two sets of
years, draw the two circles in your head, and find the size of each
region. Then check that inclusion–exclusion from
[Circles that overlap](tutorial:circles-that-overlap#counting-either-inclusion-exclusion)
agrees with the union.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Go through the lists by index, `for i in range(len(years)):`, and
   `.add(years[i])` to a set when the value at `i` is 75 or more.
2. The overlap is `&`. Each "only" region is a difference.
3. The box is every year, `set(years)`. What is outside both circles?

**Think about:** what does it mean that one region is empty?

</details>

<details class="dl-answer"><summary>answer</summary>

One way through; yours may differ and work as well.

```python
ireland_high = set()
other_high = set()
for i in range(len(years)):
    if ireland[i] >= 75:
        ireland_high.add(years[i])
    if other[i] >= 75:
        other_high.add(years[i])

print("both:", len(ireland_high & other_high))
print("Ireland only:", len(ireland_high - other_high))
print("other only:", len(other_high - ireland_high))
print("neither:", len(set(years) - (ireland_high | other_high)))
print(len(ireland_high | other_high),
      len(ireland_high) + len(other_high) - len(ireland_high & other_high))
```

With Spain: 26 years in both, 0 for Ireland only, 12 for Spain only,
and 29 in neither. The union has 38 years, and $26 + 38 - 26 = 38$.

The empty region says that Ireland's circle sits inside Spain's: every
year Ireland was at 75 or more, Spain was too. In the language of
[Collections without repeats](tutorial:collections-without-repeats#sets-too-big-to-list),
`ireland_high <= other_high` is `True`. Spain reached 75 in 1979, and
Ireland only in 1991.

</details>

**13. Make.** The report's chart. Draw one line chart with both
countries on it, over the years. Give it labelled axes, with units, a
legend, a title and the source of the data. Should the vertical axis
start at 0?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. `plt.plot(years, ireland, label="Ireland")` draws one line. A second
   `plt.plot` adds the other country to the same chart.
2. `plt.legend()` shows the labels.
3. `plt.xlabel`, `plt.ylabel` and `plt.title` add the words.

**Think about:** on
[Kinds of data, and honest charts](tutorial:kinds-of-data-and-honest-charts#a-chart-that-tells-the-truth),
which kind of chart may zoom in, and which may not?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
import matplotlib.pyplot as plt

plt.plot(years, ireland, label="Ireland")
plt.plot(years, other, label=other_country)
plt.xlabel("year")
plt.ylabel("life expectancy at birth, in years")
plt.title("Life expectancy, 1950 to 2016 (Our World in Data)")
plt.legend()
```

The lines cross in the mid-1960s, when Spain overtook Ireland, and the
gap widens until about 1980. A line chart suits it: the order of the
years means something, and each point comes after the one before.

The axis does not need to start at 0. A line shows change, and the
numbers on the axis say where it starts. A bar chart of the two means
would be different: a bar's length is read as its amount, so its axis
must start at 0.

</details>

**14. Explain.** Schlomi, who is learning Python too, wants her report
to make it plain that Spain's mean is higher. Her bar chart of the two
means shows 73.8 for Ireland and 75.0 for Spain, with the vertical axis
from 73 to 75.5, so Spain's bar is more than twice as tall as Ireland's. Every
number on the axis is true. What is dishonest about the chart, and what
would you change so that it still makes her point?

<details class="dl-answer"><summary>answer</summary>

Her point is a fair one, and the chart overstates it. The bars'
lengths are not the values. Ireland's bar is $73.8 - 73 = 0.8$
long, and Spain's is $75.0 - 73 = 2.0$, so Spain looks two and a half
times as high, for a difference of about a year. A reader compares the
lengths, not the axis labels. The honest fix is to start the axis at 0,
so that the bars are almost the same, because the numbers are. If the
one-year difference is the story, say it in words, or show the change
over time with a line chart, which may zoom in.

</details>

## Stretch

**15. Make.** The report itself. Write a procedure, `report(name,
values, first_year)`, that prints a one-page report for one country:
the first and last years with their values, the mean, the median, the
range, the standard deviation, and the frequency table in 5-year bins.
Use the functions you wrote in problems 6 and 10 if you like. Call it
for Ireland and for your country, then draw the chart from problem 13
under them. End with two sentences of your own that say what the
report shows.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The last year is `first_year + len(values) - 1`, because the index
   counts from 0.
2. Inside the procedure, every name should be a new one, such as
   `typical` or `spread`, and never a toolkit function's name.
3. A procedure prints, and gives back `None`, as on
   [Machines that take a number](tutorial:machines-that-take-a-number#functions-that-give-back-and-procedures-that-do).

**Think about:** what would a reader who never saw your code need to be
told, in the report's own words, to trust the numbers?

</details>

<details class="dl-answer"><summary>answer</summary>

One way through; yours may differ and work as well.

```python
def report(name, values, first_year):
    """Print a one-page report on a list of yearly life expectancies for one country."""
    last_year = first_year + len(values) - 1
    print("Life expectancy at birth in", name, "(Our World in Data)")
    print(" ", first_year, ":", values[0], "years   ", last_year, ":", values[-1], "years")
    print("  mean:", round(mean(values), 2), "  median:", median(values))
    print("  range:", round(largest(values) - smallest(values), 2),
          "  standard deviation:", round(std_dev(values), 2))
    table = five_year_bins(values)
    for start in sorted(table):
        print("  ", start, "to", start + 5, "years:", table[start])
    print()


report("Ireland", ireland, years[0])
report(other_country, other, years[0])
```

The report for Ireland begins:

```text
Life expectancy at birth in Ireland (Our World in Data)
  1950 : 65.61 years    2016 : 81.14 years
  mean: 73.79   median: 73.26
  range: 16.36   standard deviation: 4.18
   60 to 65 years: 1
   65 to 70 years: 11
   ...
```

Your two sentences will be your own. For Spain, one pair might be:
"Life expectancy rose in both countries between 1950 and 2016, by
about 15.5 years in Ireland and about 21 years in Spain. Spain started
lower, passed Ireland in the mid-1960s, and has stayed ahead, though
by 2016 the gap was under two years."

</details>

**16. Another way.** In problem 6 you took the mode of the rounded
values. Here is another use of the same rounded list: find its mean from
its frequency table alone, without `mean`. Each value counts as many
times as its frequency. Check your answer against `mean` of the rounded
list.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. `table = frequency_table(whole_years(ireland))`.
2. For each key, multiply the key by its frequency, and keep a running
   total of those products.
3. Divide by the total of the frequencies, which is the number of
   values.

**Think about:** why does this give exactly the same answer as adding
up all 67 rounded values?

</details>

<details class="dl-answer"><summary>answer</summary>

One way through; yours may differ and work as well.

```python
table = frequency_table(whole_years(ireland))
weighted = 0
for value in table:
    weighted = weighted + value * table[value]
from_table = weighted / total(table.values())

print(from_table, mean(whole_years(ireland)))
```

Both give 73.8208…. That is a little different from the mean of the
raw values, 73.79, because rounding moved each value a little. Adding 71 eight times is the same as
adding $71 \times 8$ once, so a frequency table holds everything a mean
needs. In symbols, with $f$ for each value's frequency:
$\bar{x} = \frac{\sum f x}{\sum f}$. This is how a mean is found when a
survey gives only a table, not the raw list.

</details>

**17. Explain.** Your report compares two countries over 67 years with
a few numbers and a chart. Name two things the report cannot tell a
reader, however carefully it is made, and one sentence you would add to
the report so that nobody reads more into it than it holds.

<details class="dl-answer"><summary>answer</summary>

There are many answers worth giving. Here is one way through:

- **What one value is.** Each value is a whole country's life
  expectancy at birth for one year, an estimate. It says nothing about
  how long any one person lives, or about the differences between
  people in the same country.
- **Why.** The report shows that Spain rose faster. It cannot say why:
  health care, diet, income, or something else. A chart shows *that*,
  and rarely *why*.
- **After 2016.** The file stops in 2016, so the report cannot say what
  happened since, and a mean over all 67 years mixes 1950 with 2016.

A sentence worth adding: "Each value is the life expectancy of a baby
born in that year, as estimated by Our World in Data; the figures
describe countries, not people, and end in 2016." Saying where the data
came from, and what it stands for, is part of an honest report, as it
is part of an honest chart.

</details>
