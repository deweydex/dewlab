---
title: "Statistics: averages, spread and frequency — Practice"
practice_for: making-sense-of-data
year: "2026-2027"
version: 2026.09.26.1
worlds:
  exoplanets: Planets around other stars, and the ways they were found.
  dinosaurs: Dinosaurs and their fossils, what has been found, where, and how old it is.
  book-characters: The people in six novels, chapter by chapter.
  games-of-chance: Dice, cards and coins, and the games people play with them.
datasets: [exoplanets, dinosaur-finds, book-characters]
---

# Statistics: averages, spread and frequency — Practice

Problems on averages, spread and shape, and three from earlier pages. On
the small datasets, work the statistics out by hand before you check
them: five numbers do not take long, and doing it once by hand is what
makes a formula mean something.

## Tools

Python's `statistics` module has the tutorial's measures built in. Use it
to check your answers. `pstdev` is the standard deviation that divides
by $n$, as the tutorial's does, and `stdev` the one that divides by
$n - 1$.

```python exec
id: tools-1
import statistics

data = [12, 15, 15, 18, 22, 25, 25, 25, 30, 45]

print("mean    ", statistics.mean(data))
print("median  ", statistics.median(data))
print("mode    ", statistics.mode(data))
print("range   ", max(data) - min(data))
print("pstdev  ", round(statistics.pstdev(data), 4))
print("stdev   ", round(statistics.stdev(data), 4))
```

## The centre

**1.** What are the mean, median and mode of `[4, 8, 6, 5, 3, 8, 2]`?

<details class="dl-answer"><summary>answer</summary>

The mean is $\frac{36}{7} \approx 5.14$, the median 5, and the mode 8.
Sorted, the values are 2, 3, 4, 5, 6, 8, 8, and the fourth of seven is
the middle. The mode is the largest of the three here: the commonest
value need not be anywhere near the centre.

</details>

**2.** What is the median of `[10, 12, 14, 16]`?

<details class="dl-answer"><summary>answer</summary>

13, the mean of the two middle values. So the median need not be one of
the values in the data.

</details>

**3.** Nine people in an office earn €30,000 each, and the director earns
€500,000. What is the mean salary?

```python exec
id: data-office-salaries
import statistics

salaries = [30_000] * 9 + [500_000]
print("median", statistics.median(salaries))
print("mean  ", statistics.mean(salaries))
```

```predict
type: number

What will the mean salary be?
```

<details class="dl-answer"><summary>which describes the office</summary>

€77,000, against a median of €30,000. Nobody in the office earns
anything near the mean. Quoting it would be true, and would mislead. But
if the question is what the office costs in salaries, the mean is
exactly right: it is the total shared out. Which average is better
depends on the question.

</details>

**4.** Can you think of a dataset where the mode is useless? And one where
it is the only average that makes sense?

<details class="dl-answer"><summary>answer</summary>

Useless: measured values where every value is different, such as
heights to the millimetre. Then the mode is whichever value happens to
repeat, or there is none, which is why the tutorial's mode of the
planets' radii came from rounding.

The only sensible one: categorical data. `["red", "blue", "red"]` has
no mean and no median, but its mode is "red".

</details>

## Spread

**5.** For `[2, 4, 4, 4, 5, 5, 7, 9]`, can you work out the mean and the
standard deviation by hand?

<details class="dl-answer"><summary>answer</summary>

The mean is 5. The distances from it are −3, −1, −1, −1, 0, 0, 2 and 4;
their squares, 9, 1, 1, 1, 0, 0, 4 and 16, add up to 32, and $\frac{32}{8}
= 4$. That number, the mean of the squared distances, is the *variance*,
and its square root, 2, is the standard deviation. Real data almost
never comes out this neatly.

</details>

**6.** Why square the distances? What goes wrong if we add them up as
they are?

<details class="dl-answer"><summary>answer</summary>

They always add up to zero: the mean is exactly the point where the
distances above and below cancel. Squaring makes every distance positive,
and gives large distances more weight. Taking each distance without its
minus sign would work too, and gives the *mean absolute deviation*; it
is a perfectly good measure, and harder to work with in algebra.

</details>

**7.** Add 10 to every value in a dataset. What happens to the mean, the
median, the range and the standard deviation? Then multiply every value
by 3 instead.

```python exec
id: data-shift-and-stretch
import statistics

data = [3, 7, 7, 10, 13]
plus_ten = [value + 10 for value in data]
times_three = [value * 3 for value in data]

for name, values in [("data", data), ("plus 10", plus_ten), ("times 3", times_three)]:
    print(name, " mean", statistics.mean(values), " median", statistics.median(values),
          " range", max(values) - min(values), " sd", round(statistics.pstdev(values), 2))
```

<details class="dl-answer"><summary>what moves</summary>

Adding 10 moves the mean and median up by 10, and leaves the range and
standard deviation alone: every distance from the mean stays the same.
Multiplying by 3 multiplies all four by 3. Measures of centre move with
the data; measures of spread ignore a shift, and grow with a stretch.

</details>

**8.** What is the difference between dividing by $n$ and by $n - 1$?

<details class="dl-answer"><summary>answer</summary>

Dividing by $n$ measures the spread of the numbers you have. Dividing by
$n - 1$ estimates the spread of the population they are a sample from. A
sample's values sit a little closer to their own mean than to the
population's, so the distances come out slightly too small, and dividing
by a smaller number makes up for it. For $n = 100$ the two differ by
about half a percent; for $n = 5$, by more than ten.

</details>

## Kinds of data

Two more kinds split numerical data by what zero means. *Interval* data
has a zero that is a chosen point, not "none": temperature in Celsius.
*Ratio* data has a zero that means none of it: height.

```question
id: data-interval-or-ratio
type: fill-in-the-blank

- Eye colour is {nominal|ordinal|interval|ratio} data.
- An exam grade of Pass, Merit or Distinction is {ordinal|nominal|interval|ratio} data.
- Temperature in Celsius is {interval|ratio|nominal|ordinal} data.
- Height in centimetres is {ratio|interval|nominal|ordinal} data.
- The number on a football shirt is {nominal|ordinal|interval|ratio} data.
```

**9.** Why is 20 °C not twice as hot as 10 °C, when 20 cm is twice as
long as 10 cm?

<details class="dl-answer"><summary>answer</summary>

0 °C is where water freezes, a point somebody chose; it does not mean no
heat. 0 cm means no length. Ratios only make sense when zero means none.
And the shirt number is the trap of the question above: a program will
work out the mean of shirt numbers without a warning, and the answer
means nothing.

</details>

## Shape

**10.** Can you build a frequency table for
`[1, 2, 2, 3, 3, 3, 4, 4, 4, 4]`, and describe its shape?

```python exec
id: data-frequency-table
from collections import Counter

print(Counter([1, 2, 2, 3, 3, 3, 4, 4, 4, 4]))
```

<details class="dl-answer"><summary>answer</summary>

1 appears once, 2 twice, 3 three times and 4 four times. `Counter`,
from Python's `collections` module, counts for you. The shape rises to
the right, and its name is *skewed left*, which confuses many people:
the name describes the tail, the thin end, and here the tail is on the
left.

</details>

**11.** A right-skewed distribution has a long tail of large values. How
do its mean, median and mode usually compare?

<details class="dl-answer"><summary>answer</summary>

Mode < median < mean. The tail pulls the mean furthest, the median a
little, and the mode not at all. The number of rolls it takes to get a
six, from the tutorial's games world, has a mode of 1, a median of 4 and
a mean of 6.

</details>

**12.** Can you make a dataset whose mean and median are equal, but
which is not symmetric?

<details class="dl-answer"><summary>answer</summary>

`[2, 3, 6, 8, 11]` has a mean of 6 and a median of 6. Below 6, the values
are 3 and 4 away; above it, 2 and 5. Equal mean and median allow a
symmetric shape without proving one. Every summary loses something, and
the only sure way to see the shape is to draw it.

</details>

## Your world

**13.** A question from the world you chose.

<div class="dl-world" data-world="exoplanets">

Do the two commonest ways of finding planets find the same kind of
planet? Compare the median radius of the planets found by transit with
those found by radial velocity, the wobble of their star.

```python exec
id: data-world--exoplanets
import statistics

planets = await load_csv("exoplanets.csv")
transit = planets[planets.method == "Transit"].radius_earths.dropna()
wobble = planets[planets.method == "Radial Velocity"].radius_earths.dropna()
print(len(transit), "transit radii;", len(wobble), "wobble radii")
```

```hint
`statistics.median` works on each; so does pandas's own `.median()`.
```

```solution
import statistics

planets = await load_csv("exoplanets.csv")
transit = planets[planets.method == "Transit"].radius_earths.dropna()
wobble = planets[planets.method == "Radial Velocity"].radius_earths.dropna()
print(len(transit), "transit radii;", len(wobble), "wobble radii")
print("median radius, transit:", statistics.median(transit))
print("median radius, wobble: ", statistics.median(wobble))
---
With the copy saved on {{snapshot: exoplanets}}: 2.46 Earth radii for
transit planets, and 12.6 for wobble planets, which is larger than
Jupiter. A heavy planet makes its star wobble more, so the wobble method
finds giants most easily. Each method has its own sampling bias, and the
two humps in the tutorial's histogram are partly the two methods'
different catches. (For most wobble planets, the archive estimates the
radius from the mass, since the wobble measures only the mass.)
```

</div>

<div class="dl-world" data-world="dinosaurs">

How many dinosaur finds does a typical country have? Count the finds in
each country, then work out the mean, median and mode of those counts.

```python exec
id: data-world--dinosaurs
import statistics

finds = await load_csv("dinosaur-finds.csv", keep_default_na=False)
per_country = finds.country_code.value_counts()
print(len(per_country), "countries")
print(per_country.head())
```

```hint
`per_country.tolist()` gives the counts as a plain list for the
`statistics` functions.
```

```solution
import statistics

finds = await load_csv("dinosaur-finds.csv", keep_default_na=False)
per_country = finds.country_code.value_counts()
print(len(per_country), "countries")
counts = per_country.tolist()
print("mean", round(statistics.mean(counts)), " median", statistics.median(counts),
      " mode", statistics.mode(counts))
---
With the copy saved on {{snapshot: dinosaur-finds}}: 63 countries, a
mean of about 105 finds, a median of 13 and a mode of 1. The United
States alone has 2,393. The counts are skewed far to the right, and the
mean describes no country. They also measure digging as much as
dinosaurs: where there is exposed rock of the right age, and where
people have looked and published.
```

</div>

<div class="dl-world" data-world="book-characters">

How often is Mr Darcy named in a typical chapter of *Pride and
Prejudice*? Work out the mean, median and mode of his mentions per
chapter, and do the same for Elizabeth.

```python exec
id: data-world--book-characters
import statistics

characters = await load_csv("book-characters.csv")
pride = characters[characters.book == "pride-and-prejudice"]
darcy = pride[pride.character == "Darcy"].mentions.tolist()
elizabeth = pride[pride.character == "Elizabeth"].mentions.tolist()
print(len(darcy), "chapters")
```

```hint
`statistics.mean`, `statistics.median` and `statistics.mode` on each list.
```

```solution
import statistics

characters = await load_csv("book-characters.csv")
pride = characters[characters.book == "pride-and-prejudice"]
darcy = pride[pride.character == "Darcy"].mentions.tolist()
elizabeth = pride[pride.character == "Elizabeth"].mentions.tolist()
print(len(darcy), "chapters")
for name, mentions in [("Darcy", darcy), ("Elizabeth", elizabeth)]:
    print(name, " mean", round(statistics.mean(mentions), 1),
          " median", statistics.median(mentions), " mode", statistics.multimode(mentions))
---
Darcy: a mean of 6.8, a median of 5 and a mode of 0, since he is not
named at all in 11 of the 61 chapters. Elizabeth is named in every
chapter: a mean of 12.3, a median of 11, and two modes, 10 and 14.
`statistics.mode` would give only the first of a tie, so `multimode`
shows both. Darcy's commonest count is none at all, and yet, of the
twelve people in the data, only Elizabeth is named more often: a mode
can say something true and unhelpful at once.
```

</div>

<div class="dl-world" data-world="games-of-chance">

Roll a die ten times and count the sixes. Do that 10,000 times. Which
number of sixes is commonest? Draw the counts, then compare them with
the binomial formula from the tutorial, with $p = \frac{1}{6}$.

```python exec
id: data-world--games-of-chance
import math
import random
import matplotlib.pyplot as plt

counts = [0] * 11
for trial in range(10_000):
    sixes = 0
    for roll in range(10):
        if random.randint(1, 6) == 6:
            sixes = sixes + 1
    counts[sixes] = counts[sixes] + 1

plt.bar(range(11), counts)
plt.xlabel("sixes in ten rolls")
plt.ylabel("times in 10,000 trials")
```

```hint
The chance of exactly `k` sixes is `math.comb(10, k) * (1/6) ** k * (5/6) ** (10 - k)`.
Multiply it by 10,000 to compare with a bar.
```

```solution
import math
import random
import matplotlib.pyplot as plt

counts = [0] * 11
for trial in range(10_000):
    sixes = 0
    for roll in range(10):
        if random.randint(1, 6) == 6:
            sixes = sixes + 1
    counts[sixes] = counts[sixes] + 1

plt.bar(range(11), counts)
plt.xlabel("sixes in ten rolls")
plt.ylabel("times in 10,000 trials")

for k in range(5):
    expected = 10_000 * math.comb(10, k) * (1 / 6) ** k * (5 / 6) ** (10 - k)
    print(k, "sixes:", counts[k], "rolled,", round(expected), "expected")
---
One six is commonest, about 3,230 times in 10,000, then two, then none.
The shape is lopsided, unlike the coins' symmetric hump, because $p$ is
not a half: with ten rolls and a chance of $\frac{1}{6}$, the counts
bunch near $10 \times \frac{1}{6} \approx 1.7$ and trail off to the
right. Seven or more sixes in ten rolls comes up only two or three times
in 10,000.
```

</div>

## Putting it together

**14.** Ten exam marks: `[45, 52, 68, 71, 71, 74, 78, 82, 89, 95]`. Can
you work out the mean, median, mode, range and standard deviation, and
say what they tell you about the class?

<details class="dl-answer"><summary>answer</summary>

The mean and the median are both 72.5, the mode 71, the range 50, and the
standard deviation 14.5. The mean and median agree, which suggests the
marks are spread fairly evenly either side. The range tells us least: it
depends on two students.

</details>

**15.** Now add a mark of 12. What changes most?

```python exec
id: data-one-low-mark
import statistics

marks = [45, 52, 68, 71, 71, 74, 78, 82, 89, 95, 12]
print("mean  ", round(statistics.mean(marks), 1))
print("median", statistics.median(marks))
print("sd    ", round(statistics.pstdev(marks), 1))
```

```predict
Which of the three moves most, for its size?

- The mean
  - Every mark adds its full size to the total.
- The median
  - A new mark changes which one is in the middle.
- The standard deviation
  - The new mark is very far from the rest, and distances are squared.
```

<details class="dl-answer"><summary>why</summary>

The mean falls from 72.5 to 67, and the median only to 71. The standard
deviation jumps from 14.5 to about 22.2, by half. The new mark is 55
below the new mean, and that distance is squared: $55^2 = 3{,}025$. The
standard deviation is even more sensitive to an outlier than the mean.

</details>

## From earlier

**16.** From *Probability*. What is the mean of the six faces of a die?
Can a die ever show it?

<details class="dl-answer"><summary>answer</summary>

$\frac{1 + 2 + 3 + 4 + 5 + 6}{6} = 3.5$, which no roll can show. The mean
of many rolls comes close to 3.5, by the law of large numbers, but a
mean need not be a possible value, like the planets' mean radius, which
hardly any planet has.

</details>

**17.** From *Venn diagrams*. The tutorial found 507 Earth-sized
planets, and none of them has a year of 200 to 500 days. The file has
235 planets with a year of 200 to 500 days. How many planets are
Earth-sized, or have an Earth-like year?

<details class="dl-answer"><summary>answer</summary>

$507 + 235 - 0 = 742$. The overlap is empty, so the two sets are
mutually exclusive, and inclusion-exclusion takes nothing away. In the
population of all planets, the overlap is surely not empty. In this
sample, it is.

</details>

**18.** From *Counting*. How many different samples of 5 planets could
be chosen from the file's 6,372?

<details class="dl-answer"><summary>answer</summary>

$C(6{,}372, 5)$, about $8.7 \times 10^{16}$: `math.comb(6372, 5)`. Each
sample would give its own mean radius, some far from the whole file's.
How far a sample's mean can wander from the population's is where the
next page's "go further" sections lead.

</details>
