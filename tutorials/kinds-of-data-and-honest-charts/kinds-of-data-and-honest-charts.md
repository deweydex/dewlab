---
title: "Kinds of data, and honest charts"
year: "2026-2027"
version: 2026.09.25.1
datasets: [life-expectancy]
covers:
  four-kinds-of-data:
    covers: [MIT-5.9]
  counting-a-frequency-table:
    covers: [MIT-5.11]
  a-tool-for-counting:
    covers: [MIT-5.11]
    touches: [PDP-LO8]
  bars-and-pies-for-categories:
    covers: [MIT-5.10]
  histograms-for-measured-numbers:
    covers: [MIT-5.10, MIT-5.11]
  stem-and-leaf-every-value-kept:
    covers: [MIT-5.10]
  lines-for-change-over-time:
    touches: [MIT-5.10]
  a-chart-that-tells-the-truth:
    covers: [MIT-5.10]
---

# Kinds of data, and honest charts

Picture an advert for a health drink. (The advert is made up; the
numbers in it are real.) It shows two bars: life expectancy in Ireland,
and in the UK. The Irish bar is more than three times as tall. Does an
Irish baby really expect to live three times as long?

No. And here is the part I find most surprising: every number on that
chart can be true. The trick is in one small choice about where the
picture starts. By the end of this page you will have drawn the
misleading chart yourself, and the honest one beside it.

On this page we:

- tell four kinds of data apart: nominal, ordinal, discrete and
  continuous
- count how often each value appears, in a frequency table, and add
  `frequency_table` to your toolkit
- draw a bar chart, a pie chart, a histogram, a stem-and-leaf plot and a
  line chart, each for the data it suits
- draw the misleading chart from the advert, and an honest one beside it

> **The space we're in.** Lists of values, from
> [A row of numbers](tutorial:a-row-of-numbers), and matplotlib, which
> draws charts once we write `import matplotlib.pyplot as plt`. One real
> dataset: life expectancy by country and year, from Our World in Data.
> One thing usually goes unsaid: a chart is not the data. It is a
> picture that somebody made from the data, and every picture involves
> choices, such as where an axis starts. An honest chart makes choices
> that let the reader see the data truly.

## Warm-up

The first question is from
[A row of numbers](tutorial:a-row-of-numbers), and the second from
[What is typical?](tutorial:what-is-typical).

```question
id: kinds-warm-up-1
type: fill-in-the-blank

`rain = [4, 0, 12, 7, 3]`. Then `rain[-1]` is {3}, and `len(rain)` is {5}.
```

```question
id: kinds-warm-up-2
type: multiple-choice
answer: 2

Seven friends' bus journeys take 12, 15, 15, 18, 20, 25 and 60 minutes.
What is the median journey?

- 15 minutes
  - 15 is the most common journey, the mode, not the middle one.
- 18 minutes
  - Seven journeys in order: the fourth is in the middle.
- 23.6 minutes
  - 23.6 is the mean, 165 ÷ 7, pulled up by the 60-minute journey.
- 60 minutes
  - 60 is the longest journey, not the middle one.
```

## Four kinds of data

A class of twenty fills in a short survey on the first day of a course.
It asks four questions:

1. How do you get to college: bus, car, walk, bike or train?
2. "I can learn maths." Strongly disagree, disagree, not sure, agree or
   strongly agree?
3. How many cups of coffee or tea did you have yesterday?
4. How many minutes did your journey take this morning?

The answers are all *data*: facts, collected so that we can learn from
them. They are not all the same kind of fact, and the kind decides
what we can do with them.

*Categorical data* is data where each answer is a group, or category,
such as "bus". There are two kinds.

- *Nominal data* is categorical data with no natural order. Bus, car,
  walk: no one of them comes first. The word comes from the Latin for
  "name": each answer is a name.
- *Ordinal data* is categorical data with an order. "Disagree" sits
  between "strongly disagree" and "not sure". We can put the answers in
  a line, but we cannot say how far apart they are.

*Numerical data* is data where each answer is a number that measures or
counts something. There are two kinds of those too.

- *Discrete data* is counted. Cups of coffee come in whole numbers: 0,
  1, 2, 3. Nobody had 2.7 cups, and between 2 and 3 there is nothing.
- *Continuous data* is measured. A journey can take 23 minutes, or 23.5,
  or 23.51. Between any two values there is always another one. We round
  when we write it down, but the thing itself can be any value.

Each kind is a space with its own allowed moves:

| Kind | Example | Can we put it in order? | Can we add it up, or take a mean? |
|---|---|---|---|
| nominal | how you travel | no | no |
| ordinal | "I can learn maths" | yes | no |
| discrete | cups of coffee | yes | yes |
| continuous | journey time | yes | yes |

A mean journey time makes sense. A "mean way to travel" does not. The
move is the same, and the space is different.

```question
id: kinds-four-kinds-1
type: multiple-choice
answer: 1

A football team's shirts have numbers on the back: 1, 7, 9, 10 and so
on. What kind of data is a shirt number?

- nominal: the number is a name, and adding two of them means nothing
  - A 10 is not more of anything than a 7: the number names a player, the way a word would.
- ordinal: a 10 is higher than a 7
  - The numbers can be put in order, but a 10 on a shirt is not ahead of a 7 in anything.
- discrete: it is a whole number
  - It is a whole number, but nothing is being counted with it.
- continuous: it is a number
  - It is written in digits, but nothing is being measured with it.
```

A number is not always numerical data. A shirt number, a phone number
or a bus route, such as the 46A, only names something. Ask whether
adding two of them would mean anything. If not, the data is categorical,
whatever it looks like.

## Counting: a frequency table

Here are the twenty answers to the first question, as a list. The
survey is made up, but it is the kind of answer a real class gives.
Which way to travel do you think is the most common? How would your own
class answer?

The next cell counts them with a new kind of collection. A *dictionary*
is a collection of names, each pointing at a value. The names are
called *keys*. We write one with curly brackets, a key, a colon and its
value: `{"bus": 7, "car": 6}`. Then `counts["bus"]` is 7. On
[A row of numbers](tutorial:a-row-of-numbers#counting-from-0),
`week[3]` found a value by its position, a number. `counts["bus"]`
finds a value by its key, a word. The key is a name for the value.

Read the loop before you run it. What happens the first time it meets
"walk", and what happens the second time?

```python exec
id: kinds-count-1
journeys = ["bus", "car", "walk", "bus", "bike", "car", "bus", "train",
            "car", "bus", "walk", "car", "bus", "bike", "bus", "car",
            "walk", "bus", "car", "train"]

counts = {}
for way in journeys:
    if way in counts:
        counts[way] = counts[way] + 1    # seen before: one more
    else:
        counts[way] = 1                  # the first one
print(counts)
print(counts["bus"])
```

The dictionary starts empty. The first time the loop meets a way to
travel, `way in counts` is False, so the loop makes a new key with the
value 1. After that, `way in counts` is True, and the loop adds 1 to
what is there. At the end, `counts` is

`{'bus': 7, 'car': 6, 'walk': 3, 'bike': 2, 'train': 2}`.

That is a *frequency table*: a list of each value, with how often it
appears. How often a value appears is its *frequency*. The frequencies
add up to 20, the number of answers. On a page, a frequency table is
usually written with a row for each value:

| How you travel | Frequency |
|---|---|
| bus | 7 |
| car | 6 |
| walk | 3 |
| bike | 2 |
| train | 2 |

On What is typical?, `journeys.count("bus")` would have counted one
value. A frequency table counts every value at once, in one pass
through the list. The most common value is the mode, from
[What is typical?](tutorial:what-is-typical). A frequency table shows
it at a glance: the bus. And each frequency divided by 20 is a relative
frequency, as on
[How likely is it?](tutorial:how-likely-is-it#letting-python-toss-the-coin):
7 of 20, or 35%, came by bus.

### Your turn

1. Add your own answer to the end of `journeys`, and run the cell again.
   Which number changed?
2. Add an answer nobody else gave, such as "tram". What does the loop do
   with it?
3. Try `print(counts["boat"])`. Before you run it, what do you think
   Python will say: 0, or an error? If it is an error, its last line
   names the kind, a `KeyError`, and the key that is not in the
   dictionary.

## A tool for counting

We will count values on many pages to come. So let's make the loop a
tool. `frequency_table(values)` promises a dictionary with each value as
a key and its frequency as the value. The cell below is a stub: only its
promise is written. The loop in the last section has the shape you need.

```python exec
id: kinds-toolkit
toolkit: yes
def frequency_table(values):
    """Return a dictionary from each value in values to how often it appears.

    The keys come in the order each value first appears.
    frequency_table(["bus", "car", "bus"]) is {"bus": 2, "car": 1}.
    With no values at all, the result is an empty dictionary, {}.
    """
    ...
```

```python toolkit-reference
for: kinds-toolkit
def frequency_table(values):
    """Return a dictionary from each value in values to how often it appears.

    The keys come in the order each value first appears.
    frequency_table(["bus", "car", "bus"]) is {"bus": 2, "car": 1}.
    With no values at all, the result is an empty dictionary, {}.
    """
    table = {}
    for value in values:
        if value in table:
            table[value] = table[value] + 1
        else:
            table[value] = 1
    return table
```

Run the toolkit cell, then the tests. Until the body is written,
`frequency_table` gives back `None`, so expect the first test to stop
with an `AssertionError`.

```python exec
id: kinds-toolkit-tests
assert frequency_table(["bus", "car", "bus"]) == {"bus": 2, "car": 1}
assert frequency_table([3, 0, 3, 3]) == {3: 3, 0: 1}
assert frequency_table([]) == {}
assert total(frequency_table(journeys).values()) == len(journeys)
print("frequency_table keeps its promise.")
```

```hint
Which test does the error point at? Try
`print(frequency_table(["bus", "car", "bus"]))` on its own. What does
your version give?
```

The last test says something true of every frequency table: the
frequencies add up to the number of values. `.values()` gives the
values of a dictionary without their keys, and `total` from
[Doing it again](tutorial:doing-it-again) adds them up. `.keys()` gives
the keys without their values.

Python has the same tool already, as `Counter` in its `collections`
module. Writing our own shows what it does inside.

## Bars and pies, for categories

A frequency table is a list of numbers. A chart turns it into a picture.
For categorical data, the usual picture is a *bar chart*: one bar for
each category, with its height showing the frequency. The bars stand
apart, with gaps between them, because the categories are separate
things.

Which bar will be the tallest? Run it to check. This cell, and every
cell after it on the page that counts, needs your `frequency_table`.
Until that is written, they stop with an error, because `None` has no
keys to draw.

```python exec
id: kinds-bars-1
import matplotlib.pyplot as plt

travel = frequency_table(journeys)
plt.bar(list(travel.keys()), list(travel.values()))
plt.xlabel("how you travel")
plt.ylabel("number of people")
plt.title("How 20 people get to college (made-up survey)")
```

`plt.bar` takes two lists: the labels along the bottom, and the height
of each bar. `list(...)` turns the keys and the values into ordinary
lists.

A *pie chart* shows the same frequencies as slices of a circle. Each
slice's angle is its share of 360°: the bus's slice is
$\frac{7}{20} \times 360° = 126°$.

```python exec
id: kinds-bars-2
plt.pie(list(travel.values()), labels=list(travel.keys()))
plt.title("How 20 people get to college (made-up survey)")
```

Which chart makes it easier to see that the bus beats the car? Most
people find the bars easier, because our eyes compare lengths better
than angles. A pie chart works best when there are only a few slices,
and the question is "what share of the whole?". The pie also needs the
parts to make up a whole: every person is in exactly one slice.

For ordinal data, the order of the bars matters. A frequency table
keeps its keys in the order it first met them, which for the maths
question is not the order of the scale. So we give the order ourselves,
as a list.

```python exec
id: kinds-bars-3
feelings = ["not sure", "agree", "disagree", "not sure", "agree",
            "strongly agree", "not sure", "disagree", "agree",
            "strongly disagree", "agree", "not sure", "agree", "disagree",
            "strongly agree", "agree", "not sure", "agree", "disagree", "agree"]
scale = ["strongly disagree", "disagree", "not sure", "agree", "strongly agree"]

feeling_counts = frequency_table(feelings)
heights = []
for level in scale:
    heights.append(feeling_counts[level])

plt.bar(scale, heights)
plt.xticks(rotation=20)
plt.title('"I can learn maths" (made-up survey)')
```

Eight of the twenty agree, and two strongly agree. `plt.xticks(rotation=20)`
tilts the labels so that they do not run into each other.

### Your turn

1. In the last cell, change `plt.bar(scale, heights)` to
   `plt.bar(list(feeling_counts.keys()), list(feeling_counts.values()))`.
   What goes wrong with the picture, even though every number is right?
2. Put it back. Would a pie chart suit the `feelings` data? What would
   it hide?

## Histograms, for measured numbers

Now numerical data, and real data: the life expectancy file from
[A row of numbers](tutorial:a-row-of-numbers#a-real-list-ireland-since-1950).
It has a row for each country and year. This time the cell keeps the
rows for the year 2016, from every country, and takes out the
`life_expectancy` column as a list. As before, that is all we ask of
the file: the maths is done on the list.

```python exec
id: kinds-hist-1
df = await load_csv("life-expectancy.csv")
ages = df[df.year == 2016]["life_expectancy"].tolist()

print(len(ages))
print(ages[:5])
print(smallest(ages), largest(ages))
```

There are 226 rows for 2016. Most are countries, and a few are regions,
such as "Western Europe" and "World". The values run from 50.16 to
83.94 years.

Can we make a frequency table of these? We can, but it would not help.
Life expectancy is continuous, so almost every value is different, and
nearly every frequency would be 1. Instead, we put the values into
groups of equal width, such as 50 to 55, 55 to 60, and so on. Each
group is a *class interval*, or *bin*. A frequency table of bins is a
*grouped frequency table*.

For each age, `age // 5 * 5` rounds it down to the start of its bin:
72.4 // 5 is 14, and 14 × 5 is 70. How many bins will there be, from
50 to 83.94?

```python exec
id: kinds-hist-2
bins = []
for age in ages:
    bins.append(int(age // 5 * 5))

grouped = frequency_table(bins)
for start in sorted(grouped):
    print(start, "to", start + 5, ":", grouped[start])
```

Seven bins, from 50 up to 85. `sorted(grouped)` gives the keys in
order, from the smallest bin up. The busiest bin is 75 to 80 years, with
62 rows.

A *histogram* is the chart of a grouped frequency table. It looks like a
bar chart, with two differences. The bottom axis is a number line, not a
row of names. And the bars touch, because the bins meet: one ends where
the next begins. `plt.hist` does the grouping for us, when we give it
the edges of the bins.

```python exec
id: kinds-hist-3
plt.hist(ages, bins=range(50, 90, 5), edgecolor="white")
plt.xlabel("life expectancy at birth, in years")
plt.ylabel("number of rows")
plt.title("Life expectancy in 2016 (Our World in Data)")
```

Compare the heights with the table you just printed. They are the same
seven numbers. The histogram shows the shape of the data: most places
are in the 70s, and the bars get shorter towards 50. A table of 226
numbers would never show that at a glance.

### Your turn

1. Change the bins to `range(50, 90, 10)`, then to `range(50, 90, 2)`.
   How does the shape change?
2. Which width tells the story best, in your opinion? Several answers
   are good ones: too few bins hide the shape, and too many make it
   ragged.

## Stem-and-leaf: every value kept

A histogram hides the values inside each bar. A *stem-and-leaf plot*
keeps them. Here are the twenty answers to the survey's fourth
question: how many minutes the journey took this morning, rounded to
whole minutes. Like the rest of the survey, they are made up.

Each time is split in two. The tens digit is the *stem*, and the units
digit is the *leaf*: 27 has stem 2 and leaf 7. On
[Numbers a computer can hold](tutorial:numbers-a-computer-can-hold),
`//` and `%` split a division into how many times, and what is left
over. So `27 // 10` is 2, the stem, and `27 % 10` is 7, the leaf.

What will the row for stem 2 look like? Guess, then run it.

```python exec
id: kinds-stem-1
journey_minutes = [24, 31, 19, 27, 45, 22, 28, 33, 26, 38,
                   21, 29, 35, 24, 30, 27, 41, 25, 23, 32]

for stem in range(1, 5):
    leaves = []
    for minutes in sorted(journey_minutes):
        if minutes // 10 == stem:
            leaves.append(minutes % 10)
    print(stem, "|", *leaves)
```

```text
1 | 9
2 | 1 2 3 4 4 5 6 7 7 8 9
3 | 0 1 2 3 5 8
4 | 1 5
```

`sorted(journey_minutes)`, from [What is typical?](tutorial:what-is-typical),
puts the times in order first, so each row's leaves come out smallest
first. Read the row `3 | 0 1 2 3 5 8` as the times 30, 31, 32, 33, 35 and 38.
Turn your head to the left, and the rows become bars: a histogram, with
every value still readable. The `*leaves` hands `print` each leaf on its
own, as `*row` did on
[Untangling a condition](tutorial:untangling-a-condition).

A stem-and-leaf plot suits a
small set of numbers, up to about fifty,
where you want the shape and the values both. For the 226 life
expectancies, it would be a wall of digits.

```question
id: kinds-stem-2
type: fill-in-the-blank

Twenty times have no single middle one, so the median is halfway between
the 10th and the 11th. Counting along the leaves in the plot above, the
10th time is {27} minutes and the 11th is {28} minutes.
```

## Lines, for change over time

On A row of numbers we took out Ireland's 67 years as a list, and
looked at the numbers. Now we draw them, with the years along the
bottom. What shape do you expect? Sketch a guess in the air with your
finger, then run the cell.

```python exec
id: kinds-line-1
ireland_df = df[df.country == "Ireland"]
years = ireland_df["year"].tolist()
ireland = ireland_df["life_expectancy"].tolist()

plt.plot(years, ireland)
plt.xlabel("year")
plt.ylabel("life expectancy at birth, in years")
plt.title("Ireland, 1950 to 2016 (Our World in Data)")
print(ireland[0], ireland[-1])
```

It rose from 65.61 years in 1950 to 81.14 in 2016, with a few small dips.
A *line chart* joins points in order, so it suits data where the order
means something, usually time. The line says "and then": each point
comes after the one before it. Joining the bars of the travel survey
with a line would suggest that "walk" comes after "car", which means
nothing.

Look at the left side of the chart. The axis starts near 65, not at 0.
For a line chart, that is usually fine, because the line's job is to
show change, and the numbers on the axis say where it starts. Keep that
in mind for the next section, where the same choice becomes a trick.

## A chart that tells the truth

Back to the advert. Ireland's life expectancy in 2016 was 81.14 years,
and the UK's was 80.90. The advert's chart is drawn below on the left,
and an honest one on the right. The two charts use the same two numbers.
What do you think is different about them? Pause here and guess before
you run it.

```python exec
id: kinds-honest-1
uk = df[df.country == "United Kingdom"]["life_expectancy"].tolist()
places = ["Ireland", "UK"]
values_2016 = [ireland[-1], uk[-1]]

figure, (advert, honest) = plt.subplots(1, 2, figsize=(9, 4))
advert.bar(places, values_2016, color=["green", "grey"])
advert.set_ylim(80.8, 81.2)
advert.set_title("The advert's chart")
honest.bar(places, values_2016, color=["green", "grey"])
honest.set_ylim(0, 90)
honest.set_title("An honest chart")
print(values_2016)
```

`plt.subplots(1, 2)` makes one figure with two charts side by side, and
names them `advert` and `honest`. `set_ylim` sets where each vertical
axis starts and ends.

On the left, the axis starts at 80.8. The Irish bar is
$81.14 - 80.8 = 0.34$ tall, and the UK bar is $80.90 - 80.8 = 0.10$.
So the Irish bar is 3.4 times as tall, for a difference of about a
quarter of a year. On the right, the axis starts at 0, and the bars are
almost the same, because the numbers are almost the same.

Here is the rule underneath. In a bar chart, the reader reads the
length of each bar as its value. If the axis does not start at 0, the
lengths are wrong, even when every number on the axis is right. That is
why a line chart may zoom in and a bar chart may not: a line shows
change, and a bar shows an amount.

The second trick is the three-dimensional pie. Here is the travel
survey again, flat on the left, and tilted as if it were a real pie on
the right. You do not need to read how the tilted one is drawn: it
stacks many flat pies on top of each other, squashed. Which way to
travel looks the most common in each?

```python exec
id: kinds-honest-2
from matplotlib.patches import Wedge

ways = ["bus", "car", "walk", "bike", "train"]
people = []
for way in ways:
    people.append(travel[way])
colours = ["C0", "C1", "C2", "C3", "C4"]

figure, (flat, tilted) = plt.subplots(1, 2, figsize=(9, 4))
flat.pie(people, labels=ways, colors=colours, startangle=45, counterclock=False)
flat.set_title("Flat")
for layer in range(12, -1, -1):          # the bottom layer first, the top last
    angle = 45
    for position in range(len(ways)):
        sweep = 360 * people[position] / sum(people)
        tilted.add_patch(Wedge((0, -0.02 * layer), 1, angle - sweep, angle,
                               color=colours[position], alpha=1 if layer == 0 else 0.6))
        angle = angle - sweep
tilted.set_xlim(-1.1, 1.1)
tilted.set_ylim(-1.4, 1.1)
tilted.set_aspect(0.45)
tilted.axis("off")
tilted.set_title("Tilted")
```

In the flat pie, the bus's slice is a little bigger than the car's, as
7 is a little more than 6. In the tilted pie, the car sits at the
front. Its slice looks wider, and it shows its thick side as well as its
top, so it covers more of the page than the bus. The numbers did not
change. The picture changed which slice looks biggest.

<aside class="dl-note" id="kinds-note-playfair">

**Who drew the first bar chart?** The Scottish engineer William
Playfair published the first bar charts and line charts of economic
data in 1786, in his *Commercial and Political Atlas*, and the first
pie chart in 1801. He wanted readers to see trade figures at a glance,
the same job these charts do today.

</aside>

So an honest chart, in short:

- a bar chart's axis starts at 0;
- a pie is flat, with few slices, and its slices make a whole;
- the axes have labels, with units, and the chart says where its data
  came from, and whether it is made up;
- the kind of chart suits the kind of data.

### Your turn

1. In the first cell of this section, pick one other country from the
   file, such as `"Spain"` or `"Nigeria"`, and add it to `places` and
   `values_2016`. Take its list out the same way as `uk`.
2. Change `advert.set_ylim(80.8, 81.2)` so that the advert's chart makes
   the UK look far ahead of Ireland. Which numbers would you choose?
3. Now say, in one sentence, what an honest chart of the same three
   countries shows.

<details class="dl-why"><summary>Why this way?</summary>

This page had you draw the misleading charts yourself, with your own
code. Another way is to collect real misleading charts from news
reports and adverts, and study them.

Real examples have real value. They show that the tricks happen, and
where, and a reader learns to recognise them in the wild.

We drew them ourselves because making the trick shows how small it is:
one number in `set_ylim`. A reader who has made a chart lie knows that
every chart is a set of choices, and can ask which choices were made.
That is the larger idea here. Data does not speak for itself. A person
chooses how it is shown, and you can now be that person.

</details>

## Four questions, looking back

| The question | On this page |
|---|---|
| What is named here? | four kinds of data; a dictionary, where each key is a name for a count, such as `counts["bus"]`; bins, stems and leaves |
| What is promised? | `frequency_table` promises each value with its frequency, and the frequencies add up to the number of values; a bar's length promises its value |
| What happens when? | a frequency table meets each value in turn, and makes a new key the first time; a line chart joins points in order, so its order must mean something |
| What does this space let us do? | each kind of data allows different moves: a mean for numbers, an order for ordinal data, only counting for nominal data; a chart is a picture with choices in it |

## What we have now

| Term or tool | What it means |
|---|---|
| data | facts collected so that we can learn from them |
| nominal, ordinal | categorical data: groups with no order; groups with an order |
| discrete, continuous | numerical data: counted in whole steps; measured, any value in between |
| dictionary, key | `{"bus": 7}`: a collection of names (keys), each pointing at a value |
| `.keys()`, `.values()` | a dictionary's keys; its values |
| frequency, frequency table | how often a value appears; each value with its frequency |
| class interval, bin; grouped frequency table | a group of equal width; a frequency table of groups |
| `frequency_table(values)` | your new toolkit tool |
| bar chart, pie chart | bars for categories, with gaps; slices of a whole |
| histogram | touching bars for bins of numerical data, on a number line |
| stem-and-leaf plot | each value split into stem and leaf, so the shape shows and every value is kept |
| line chart | points joined in order, usually over time |
| honest chart | a bar axis from 0, a flat pie, labelled axes, the right chart for the data |

The practice page is next. After it,
[Collections without repeats](tutorial:collections-without-repeats)
asks which songs are on two playlists at once.

For more on choosing charts, the integrated course has
[Charts: choosing the right chart for your data](tutorial:pictures-worth-numbers).

## Where to read more

CrashCourse (2019). *Data & Infographics: Crash Course Navigating Digital
Information #8.* <https://www.youtube.com/watch?v=OiND50qfCek>. How a
number or a chart can help us understand something, or fool us, and what
to ask before we trust one. Thirteen minutes.
