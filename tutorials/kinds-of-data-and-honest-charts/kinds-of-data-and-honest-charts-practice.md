---
title: "Kinds of data, and honest charts — Practice"
practice_for: kinds-of-data-and-honest-charts
year: "2026-2027"
version: 2026.09.25.1
datasets: [life-expectancy]
---

# Kinds of data, and honest charts — Practice

Each problem says what kind it is. **Predict** means guess first, then
run. **Make** means write something new. **Fix** means find why code
that looks fine does something else, and change it. **Explain** means
answer in words. **Another
way** means reach the same place by a second route. The answers are
folded away until you open them.

Your toolkit is loaded on this page: `frequency_table` from the
tutorial, and `largest`, `smallest`, `count_if`, `total`, `simulate` and
the rest from earlier pages. Every dataset on this page is made up,
except the life expectancy file.

## Warm-up

Use this cell for any of the warm-up problems.

```python exec
id: kinds-practice-warm-up
import matplotlib.pyplot as plt

chords = ["G", "C", "G", "D", "G", "C"]
print(frequency_table(chords))
```

**1. Predict.** A guitar song uses the chords in `chords` above, in
that order. What will `frequency_table(chords)` print? Say the keys in
the order they will appear, then run the cell.

<details class="dl-answer"><summary>answer</summary>

`{'G': 3, 'C': 2, 'D': 1}`. The keys come in the order each chord first
appears: G first, then C, then D. The three frequencies add up to 6,
the number of chords in the song.

</details>

**2. Explain.** What kind of data is each of these: nominal, ordinal,
discrete or continuous?

1. the county you were born in
2. a film's rating, from one star to five stars
3. the number of goals in a football match
4. the time a phone takes to download a film
5. an Eircode, such as D02 X285
6. a phone's Wi-Fi signal: weak, fair, good or excellent

<details class="dl-answer"><summary>answer</summary>

1. Nominal: a county is a name, with no order.
2. Ordinal: five stars is better than four, but the gap from one star
   to two is not a measured amount. (Many websites take a mean of star
   ratings anyway. That is a move from the numerical space, and people
   argue about whether it is fair.)
3. Discrete: goals are counted, in whole numbers.
4. Continuous: time is measured, and can be any value.
5. Nominal: it has digits in it, but it only names a place. Adding two
   Eircodes means nothing.
6. Ordinal: the levels have an order, weak before fair before good
   before excellent, but "good" is not a measured amount.

</details>

**3. Make.** In a survey of 40 people, 10 walk to work. How big an
angle does "walk" get in a pie chart? Work it out in Python, with names
for the numbers.

<details class="dl-answer"><summary>answer</summary>

```python
people = 40
walkers = 10
print(walkers / people * 360)
```

This prints `90.0`. A quarter of the people walk, so they get a quarter
of the circle: a right angle.

</details>

**4. Predict.** In a stem-and-leaf plot with the tens as stems, what are
the stem and the leaf of 47? Say them, then check with
`print(47 // 10, 47 % 10)`.

<details class="dl-answer"><summary>answer</summary>

The stem is 4 and the leaf is 7, and the cell prints `4 7`. `47 // 10`
is how many whole tens there are in 47, and `47 % 10` is what is left
over.

</details>

## Core

**5. Make.** Roll a fair die 60 times with `random.randint(1, 6)`, keep
the rolls in a list, and draw a bar chart of their frequency table. Put
the faces in order, 1 to 6, along the bottom. About how tall do you
expect each bar to be?

```python exec
id: kinds-practice-dice
import random

rolls = []
# Your loop here
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. A loop that runs 60 times appends `random.randint(1, 6)` to `rolls`.
2. `faces = frequency_table(rolls)` counts them.
3. A second loop over `range(1, 7)` builds the list of heights in the
   order 1 to 6.

**Think about:** what happens to `faces[4]` if, by chance, no 4 was
rolled at all.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
import random

rolls = []
for roll in range(60):
    rolls.append(random.randint(1, 6))

faces = frequency_table(rolls)
heights = []
for face in range(1, 7):
    heights.append(faces[face])

plt.bar(range(1, 7), heights)
plt.xlabel("face")
plt.ylabel("how many times")
```

Each face is expected about $\frac{60}{6} = 10$ times, and your bars
will wobble around 10: perhaps 7 for one face and 13 for another. That
is the wobble from
[How likely is it?](tutorial:how-likely-is-it#why-the-two-answers-differ).
If one face never came up, `faces[face]` stops with a `KeyError`, since
that key was never made. With 60 rolls that almost never happens.

</details>

**6. Fix.** Schlomi, who is learning Python too, is writing the part of
a music app that counts how many times each song was played. She wrote
the loop from memory, and every count comes out as 1. Run it, then find
what went missing.

```python exec
id: kinds-practice-fix-plays
plays = ["Zombie", "Linger", "Zombie", "Dreams", "Zombie", "Linger"]

counts = {}
for song in plays:
    if song in counts:
        counts[song] = counts[song] + 1
    counts[song] = 1
print(counts)
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Follow "Zombie" the second time it comes round. What does the `if`
   line do?
2. Which line runs next, straight after that?
3. Should that line run every time, or only the first time?

**Think about:** what word is missing, compared with the loop on the
tutorial page.

</details>

<details class="dl-answer"><summary>answer</summary>

The line `counts[song] = 1` runs every time, since it is not inside an
`else`. So when a song is seen again, the count goes up by 1, then goes
straight back to 1. Schlomi remembered both lines; only the `else`
that keeps them apart went missing. Put it back:

```python
counts = {}
for song in plays:
    if song in counts:
        counts[song] = counts[song] + 1
    else:
        counts[song] = 1
print(counts)
```

Now it prints `{'Zombie': 3, 'Linger': 2, 'Dreams': 1}`, the same as
`frequency_table(plays)`.

</details>

**7. Make.** Here are the resting heart rates of twenty people, in
beats per minute. Make a grouped frequency table with bins of width 10,
starting at 50, and then draw a histogram with the same bins. Which bin
is the busiest?

```python exec
id: kinds-practice-heart
heart_rates = [62, 71, 58, 80, 66, 74, 69, 90, 55, 63,
               77, 68, 72, 85, 60, 64, 70, 75, 67, 59]
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. For each rate, `rate // 10 * 10` gives the start of its bin: 62
   gives 60.
2. Append each bin start to a list, and give the list to
   `frequency_table`.
3. For the histogram, the edges of the bins are `range(50, 110, 10)`.

**Think about:** which bin a rate of exactly 70 goes into, and whether
the histogram agrees.

</details>

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Yours may be different and work too.

```python
bins = []
for rate in heart_rates:
    bins.append(rate // 10 * 10)
grouped = frequency_table(bins)
for start in sorted(grouped):
    print(start, "to", start + 10, ":", grouped[start])

plt.hist(heart_rates, bins=range(50, 110, 10), edgecolor="white")
plt.xlabel("resting heart rate, beats per minute")
plt.ylabel("number of people")
```

The table is 50 to 60: 3, 60 to 70: 8, 70 to 80: 6, 80 to 90: 2 and
90 to 100: 1. The busiest bin is 60 to 70. A rate of 70 goes into the
70 to 80 bin in both, because each bin starts at its left edge and stops
just before its right one.

</details>

**8. Fix.** Ten phones in a library report their Wi-Fi signal, and a
program draws a bar chart of the answers. Every number matches the
data, and yet the chart is hard to read. Run it, then find the line that
does not do what its writer meant.

```python exec
id: kinds-practice-fix-sizes
signals = ["good", "fair", "weak", "good", "excellent", "good", "weak",
           "fair", "good", "fair"]

reports = frequency_table(signals)
plt.bar(list(reports.keys()), list(reports.values()))
plt.title("Wi-Fi signal on ten phones")
```

<details class="dl-answer"><summary>answer</summary>

The bars come in the order each level first appeared: good, fair, weak,
excellent. Signal strength is ordinal data, and its bars should follow
its own order. Give that order as a list:

```python
reports = frequency_table(signals)
order = ["weak", "fair", "good", "excellent"]
heights = []
for level in order:
    heights.append(reports[level])
plt.bar(order, heights)
plt.title("Wi-Fi signal on ten phones")
```

Now the chart reads from weak to excellent, and the shape means
something: most phones had a fair or good signal.

</details>

**9. Explain.** A news website shows a line chart of Irish unemployment
over two years. Its vertical axis runs from 4% to 6%, and the line
climbs steeply. Schlomo, who is learning Python too, has read the
tutorial, and says the chart is dishonest: its axis does not start at
0. Is the chart dishonest in the way the advert's bar chart was?

<details class="dl-answer"><summary>answer</summary>

Not in the same way. Schlomo is using the rule for bar charts, and it
works there. A line chart shows change, and a reader reads its
height against the numbers on the axis, not as a length from 0. Zooming
in shows a change that matters: a rise from 4.2% to 5.1% is a real
story for thousands of people. So it can be honest, if the axis has
labels a reader can find and read.

It can still mislead a hasty reader, who sees "steep" and thinks
"huge". A careful chart says the numbers in its title, or marks the
axis with large numbers, so that nobody has to guess. A bar chart with the same
axis would be dishonest, because a bar's length is its value.

</details>

**10. Another way.** On the tutorial page, `frequency_table(journeys)`
said 7 people came by bus. Find the same 7 another way, with `count_if`
from [A row of numbers](tutorial:a-row-of-numbers#three-tools-for-your-toolkit).

```python exec
id: kinds-practice-another-bus
journeys = ["bus", "car", "walk", "bus", "bike", "car", "bus", "train",
            "car", "bus", "walk", "car", "bus", "bike", "bus", "car",
            "walk", "bus", "car", "train"]
```

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Yours may be different and work too.

```python
def by_bus(way):
    """True when the way to travel is the bus."""
    return way == "bus"

print(count_if(journeys, by_bus))
print(frequency_table(journeys)["bus"])
```

Both print 7. `count_if` answers one question, "how many buses?", and
`frequency_table` answers it for every value at once. When you need
only one count, `count_if` is enough. A third route is the list's own
`.count()`, from [What is typical?](tutorial:what-is-typical):
`journeys.count("bus")` gives 7 too.

</details>

**11. Make.** Draw a line chart of life expectancy in Ireland from 1950
to 2023, and on the same chart, a line for another country of your
choice. Label both lines, and say where the data comes from.

```python exec
id: kinds-practice-two-lines
df = await load_csv("life-expectancy.csv")
ireland_df = df[df.country == "Ireland"]
years = ireland_df["year"].tolist()
ireland = ireland_df["life_expectancy"].tolist()
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Take out the other country's list the same way as `ireland`.
2. Call `plt.plot` twice, once for each list, with `label="Ireland"`
   and a label for the other.
3. `plt.legend()` shows the labels on the chart.

**Think about:** both countries need a row for every year from 1950 to
2023, or the two lists will be different lengths. Check with `len`.

</details>

<details class="dl-answer"><summary>answer</summary>

With Spain:

```python
spain = df[df.country == "Spain"]["life_expectancy"].tolist()
print(len(ireland), len(spain))

plt.plot(years, ireland, label="Ireland")
plt.plot(years, spain, label="Spain")
plt.legend()
plt.xlabel("year")
plt.ylabel("life expectancy at birth, in years")
plt.title("Life expectancy since 1950 (Our World in Data)")
```

Both lists have 74 values. Spain starts lower than Ireland, at about
61.8 years in 1950, and passes Ireland in 1964. It stays ahead in
every year after that except 2020, the first year of COVID-19. In 2023
Spain is at about 83.7 years, and Ireland at 82.4. (These are the
numbers in the copy saved on {{snapshot: life-expectancy}}.)

</details>

**12. Predict.** Here are the highest temperatures in Dublin on twenty
days in June. How many leaves will the stem 1 have in a stem-and-leaf
plot? Guess, then run it.

```python exec
id: kinds-practice-june
june = [17, 19, 21, 18, 16, 22, 24, 19, 18, 20,
        23, 25, 19, 17, 18, 21, 20, 26, 22, 19]

for stem in range(1, 3):
    leaves = []
    for temperature in sorted(june):
        if temperature // 10 == stem:
            leaves.append(temperature % 10)
    print(stem, "|", *leaves)
```

<details class="dl-answer"><summary>answer</summary>

Stem 1 has 10 leaves, one for each day below 20 degrees:

```text
1 | 6 7 7 8 8 8 9 9 9 9
2 | 0 0 1 1 2 2 3 4 5 6
```

Those are 16, 17, 17, 18, 18, 18, 19, 19, 19 and 19. Half the days
were below 20 degrees, and half were 20 or more. Counting leaves by eye
is slow, and a miscount is common, so `len(leaves)` inside the loop is
a good check.

</details>

## Stretch

**13. Make.** The stem-and-leaf loop on the tutorial page went from
stem 1 to stem 4, because we looked at the data first. Write a function
`stem_and_leaf(values)` that prints the plot for any list of whole
numbers from 0 to 99, working out the first and last stems for itself.
Test it on the journey times and on the June temperatures.

```python exec
id: kinds-practice-stem-tool
times = [24, 31, 19, 27, 45, 22, 28, 33, 26, 38,
         21, 29, 35, 24, 30, 27, 41, 25, 23, 32]


def stem_and_leaf(values):
    """Print a stem-and-leaf plot of values, whole numbers from 0 to 99."""
    ...
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The first stem is `smallest(values) // 10`, and the last is
   `largest(values) // 10`.
2. Loop over `range(first, last + 1)`: the `+ 1` includes the last
   stem.
3. Inside, build the leaves as on the tutorial page.

**Think about:** what your plot shows for a stem with no values, such
as stem 3 in `[12, 15, 41]`. Is an empty row useful?

</details>

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Yours may be different and work too.

```python
def stem_and_leaf(values):
    """Print a stem-and-leaf plot of values, whole numbers from 0 to 99."""
    first = smallest(values) // 10
    last = largest(values) // 10
    for stem in range(first, last + 1):
        leaves = []
        for value in sorted(values):
            if value // 10 == stem:
                leaves.append(value % 10)
        print(stem, "|", *leaves)

stem_and_leaf(times)
stem_and_leaf(june)
stem_and_leaf([12, 15, 41])
```

The journey plot is the same as on the tutorial page, and the June plot
has the two rows from problem 12. For `[12, 15, 41]` it prints the
rows `2 |` and `3 |` with nothing after them. Keep them: an empty row
is a gap in the data, and a gap is part of its shape, as a gap would be
in a histogram.

</details>

**14. Another way.** The mode is the most common value. Find the mode of
`journeys` from its frequency table, with a loop that keeps the key
with the biggest frequency so far. Then check your answer with `mode`
from [What is typical?](tutorial:what-is-typical).

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. `travel = frequency_table(journeys)`.
2. Start with `best = None` and `best_count = 0`.
3. Loop over the keys. When `travel[way]` is bigger than `best_count`,
   point both names at the new way and its count.

**Think about:** this loop has the same shape as `largest`. What is
different about it?

</details>

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Yours may be different and work too.

```python
travel = frequency_table(journeys)
best = None
best_count = 0
for way in travel:
    if travel[way] > best_count:
        best = way
        best_count = travel[way]
print(best, best_count)
print(mode(journeys))
```

Both give `bus`, with 7. The loop is `largest` again, with one change:
it compares the frequencies, but it keeps the key. A `for` loop over a
dictionary goes through its keys, the same as `.keys()`.

</details>

**15. Explain.** The tutorial taught the four kinds of data first, and
the charts after. Another way would start with the charts: draw a bar
chart, a line chart and a pie of the same data, see which ones go wrong,
and only then name the kinds of data that explain why. Which order would
you have chosen, for a class like yours, and why?

<details class="dl-answer"><summary>answer</summary>

There is more than one good answer. Here are some things to weigh.

Names first gives a reader words to think with before the pictures
arrive, and a clear table of which moves each kind allows. That suits a
reader who likes to know the rules before playing. But the names can
feel empty until they are needed, and four new words at once is a lot.

Charts first gives a surprise, such as a line joining "walk" to "car",
and then the name arrives as the answer to a question the reader
already has. That usually makes a name stick better. But it takes
longer, and a reader who is unsure may read a broken chart as their own
mistake.

An answer can also say who the class is: what they already know, and
what they find hard.

</details>

**16. Explain.** A survey asks 50 people which streaming services they
use, and they may tick more than one. A pie chart of the answers has
slices for four services, adding up to 85 ticks. What is wrong with
using a pie chart here, and what would you draw instead?

<details class="dl-answer"><summary>answer</summary>

A pie promises that its slices make up one whole, and that each person
is in exactly one slice. Here many people are in two or three slices,
so the whole is 85 ticks, not 50 people. The pie would suggest, for
example, that a service ticked by 30 people has about a third of the
viewers, when in fact 30 of 50 people, 60%, use it.

One answer is a bar chart: one bar per service, each bar's height the
number of people who ticked it, and a title that says people could tick
more than one. People who use two services at once belong to two sets
at once, and that overlap is the subject of
[Collections without repeats](tutorial:collections-without-repeats).

</details>
