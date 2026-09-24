---
title: "What is typical? Mean, median, mode and spread — Practice"
practice_for: what-is-typical
year: "2026-2027"
version: 2026.09.24.1
datasets: [life-expectancy]
---

# What is typical? Mean, median, mode and spread — Practice

Each answer is hidden until you open it. Where a problem asks you to
predict, the prediction is the exercise, so make one before you run
anything.

Your toolkit is loaded on this page, so `mean`, `median`, `mode` and
`std_dev` are ready to use, and so are `largest`, `smallest`, `total`
and the rest. One warning, from the tutorial: a cell that says
`mean = ...` hides the tool. Call the number something else.

## Warm-up

Use this cell for any of the warm-up problems.

```python exec
id: typical-practice-scratch-1
sleep_hours = [7, 8, 6, 8, 9]
print(sleep_hours)
```

**1. Predict.** Someone slept 7, 8, 6, 8 and 9 hours on five nights.
Work out the mean, the median and the mode by hand. Then check with
your toolkit.

<details class="dl-answer"><summary>answer</summary>

The total is 38 hours, and $38 \div 5 = 7.6$, so the mean is 7.6 hours.
In order, the nights are 6, 7, 8, 8, 9, and the middle one is 8, so the
median is 8. The mode is 8 too, because 8 appears twice.

```python
print(mean(sleep_hours), median(sleep_hours), mode(sleep_hours))    # 7.6 8 8
```

</details>

**2. Make.** A football team scored these goals in seven matches:
`[1, 0, 2, 4, 1, 1, 3]`. Find the mean, median and mode. Which one
would you give as "a typical match"?

<details class="dl-answer"><summary>answer</summary>

```python
goals = [1, 0, 2, 4, 1, 1, 3]
print(round(mean(goals), 2))    # 1.71
print(median(goals))            # 1
print(mode(goals))              # 1
```

The mean is about 1.71 goals, and the median and mode are both 1. No
match can have 1.71 goals, but the mean is still useful: over 70
matches, it says to expect about 120 goals. For "a typical match", 1
goal is a fair answer, because the median and the mode agree on it.

</details>

**3. Predict.** What is the median of `[10, 2, 7, 4]`? Put the values in
order first.

<details class="dl-answer"><summary>answer</summary>

In order, they are 2, 4, 7, 10. There are four values, an even count, so
there are two in the middle: 4 and 7. The median is halfway between
them, $(4 + 7) \div 2 = 5.5$.

```python
print(median([10, 2, 7, 4]))    # 5.5
```

</details>

**4. Explain.** A shoe shop keeps a list of the sizes it sold last
month, and wants to know which size to order most of. Which average
should it use, and why are the other two no help?

<details class="dl-answer"><summary>answer</summary>

The mode, the size sold most often. The mean size might be 7.4, which
is not a size anyone wears. The median is a real size, but it says
only that half the sales were smaller and half bigger, not which size
sold best. The mode answers the shop's question directly: this is the
size most people bought.

</details>

## Core

Use this cell for the core problems.

```python exec
id: typical-practice-scratch-2
coast = [12, 13, 12, 14, 13, 12, 13]
inland = [15, 24, 18, 27, 20, 16, 26]
print(coast, inland)
```

**5. Make.** The two lists above are made-up highest temperatures, in
degrees Celsius, for one week in two towns: one on the coast, and one
far inland. Find each town's mean, range and standard deviation. What
does the sea seem to do to the weather?

<details class="dl-answer"><summary>answer</summary>

```python
for town in [coast, inland]:
    print(round(mean(town), 1),
          largest(town) - smallest(town),
          round(std_dev(town), 2))
# 12.7 2 0.7
# 20.9 12 4.49
```

The inland town is warmer on average, 20.9 °C against 12.7 °C. It is
also far more spread out: a range of 12 degrees against 2, and a
standard deviation of about 4.5 against 0.7. In this made-up week, the
sea keeps the coast's temperature steady. Real coastal weather often
behaves the same way, because the sea warms and cools more slowly
than land.

</details>

**6. Fix.** A property website wants the median house price in a small
area. This code gives an answer, with no error, and the answer is
wrong. Find the mistake.

```python exec
id: typical-practice-fix-median
prices = [310000, 245000, 780000, 265000, 290000]


def middle_price(values):
    """Return the median of values, a list with an odd count."""
    return values[len(values) // 2]


print(middle_price(prices))    # should be 290000
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Which index does `len(values) // 2` give for five values?
2. Which price is at that index in `prices`?
3. Is that the middle price, if the five houses stood in a line from
   cheapest to dearest?

**Think about:** what must happen to the values before "the middle one"
means anything?

</details>

<details class="dl-answer"><summary>answer</summary>

The function takes the middle position of the list as it was given,
which is €780,000, the most expensive house. The median is the middle
one *in order*, so the values must be sorted first:

```python
def middle_price(values):
    """Return the median of values, a list with an odd count."""
    return sorted(values)[len(values) // 2]


print(middle_price(prices))    # 290000
```

A mistake like this is hard to spot, because the code runs, and gives a
real price from the list. A test with a list that is not already in
order catches it. Your toolkit's `median` does the same job, and works
for an even count too.

</details>

**7. Fix.** A student writes a function to report a week's spending. It
stops with an error. Read the last line of the error, then find the
mistake.

```python exec
id: typical-practice-fix-name
def spending_report(spends):
    """Print the mean and the largest of a list of amounts spent."""
    mean = mean(spends)
    print("typical day:", round(mean, 2))
    print("biggest day:", largest(spends))


spending_report([12.50, 4.00, 7.80, 31.20, 6.50])
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The error is an `UnboundLocalError`. Which name does it name?
2. Inside the function, `mean = ...` makes `mean` a local name. Where
   does Python look for `mean`, then, when the same line calls it?
3. What could the number be called instead?

**Think about:** [What a function can see](tutorial:what-a-function-can-see)
met this error. Why does one line both need the tool and hide it?

</details>

<details class="dl-answer"><summary>answer</summary>

The line `mean = mean(spends)` gives the name `mean` to a number inside
the function. That makes `mean` a local name for the whole function.
So when the right-hand side calls `mean(...)`, Python looks in the
call's own space, finds a local `mean` with no value yet, and stops
with an `UnboundLocalError`. Give the number its own name:

```python
def spending_report(spends):
    """Print the mean and the largest of a list of amounts spent."""
    typical_day = mean(spends)
    print("typical day:", round(typical_day, 2))
    print("biggest day:", largest(spends))


spending_report([12.50, 4.00, 7.80, 31.20, 6.50])
# typical day: 12.4
# biggest day: 31.2
```

Outside a function, the same line would work once, and then hide the
tool for the rest of the page. Either way, a tool's name is best left
to the tool.

</details>

**8. Predict.** A five-a-side team's ages are 20, 22, 21, 23 and 24.
Their coach, aged 64, joins the list. Which changes more, the mean or
the median? Guess, then check.

<details class="dl-answer"><summary>answer</summary>

```python
ages = [20, 22, 21, 23, 24]
print(mean(ages), median(ages))                  # 22.0 22
print(mean(ages + [64]), median(ages + [64]))    # 29.0 22.5
```

The mean jumps from 22 to 29, older than everyone but the coach. The
median moves only from 22 to 22.5. The coach is an outlier, and the
mean moves towards the tail, as it did with the rents. Notice
`ages + [64]`: from
[A row of numbers](tutorial:a-row-of-numbers#adding-and-multiplying-lists),
`+` joins two lists.

</details>

**9. Explain.** For any list, the deviations from the mean add up to 0.
Why? Try to say it without a formula first, using the idea of
sharing out.

<details class="dl-answer"><summary>answer</summary>

The mean is what each value would be if the total were shared out
equally. The values above the mean have more than their share, and the
values below it have less. Sharing out moves exactly the extra from the
first group to the second, so the amounts above and below must be
equal. The positive deviations and the negative ones cancel out.

With a formula: the deviations add up to
$\sum x_i - n\bar{x}$, and $n\bar{x}$ is the total, so the answer is
the total minus the total, which is 0.

</details>

**10. Another way.** Here is another way to find a median, by hand or
in code. Put the values in order. Then take away the smallest and the
largest, again and again, until one or two values are left. Write it
with a `while` loop and a slice, and check it against your toolkit's
`median` on the rents from the tutorial.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Start with `in_line = sorted(values)`.
2. `in_line[1:-1]` is the list without its first and last values.
3. Keep doing that while more than two values are left.
4. At the end, one value is left, or two. If two, take their mean.

**Think about:** why does this give the same answer as picking the
middle index?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def median_by_trimming(values):
    """Return the median by taking away both ends until one or two are left."""
    in_line = sorted(values)
    while len(in_line) > 2:
        in_line = in_line[1:-1]
    return mean(in_line)


rents = [1350, 1250, 3900, 1200, 1450, 1250, 1300, 2600, 1150, 1400, 1250]
print(median_by_trimming(rents), median(rents))    # 1300.0 1300
print(median_by_trimming([10, 2, 7, 4]))           # 5.5
```

Both ways give €1,300. The mean of one value is that value, so
`mean(in_line)` works whether one or two are left. Each trim takes one
value from each side, so the middle is never touched. That is why the
median ignores outliers: they are the first things trimmed away.

</details>

**11. Make.** A bus company asked 12 passengers which route they took
this morning. Their answers are below. Which route is most used, and
by how many of the 12?

```python
routes = ["46A", "15", "46A", "39A", "15", "46A",
          "145", "46A", "15", "39A", "46A", "145"]
```

<details class="dl-answer"><summary>answer</summary>

```python
routes = ["46A", "15", "46A", "39A", "15", "46A",
          "145", "46A", "15", "39A", "46A", "145"]
print(mode(routes), routes.count(mode(routes)))    # 46A 5
```

The 46A, with 5 of the 12 passengers. The mode is the only one of the
three averages that works here, because route names are words, not
amounts. "46A" is a name, even though it has a number in it.

</details>

**12. Explain.** The tutorial built the standard deviation in steps: the
range, then the mean distance from the mean, then the standard
deviation, with the formula at the end. Many courses give the formula
first, and then practise with it. If you were teaching this to a
friend, which way would you choose, and why?

<details class="dl-answer"><summary>answer</summary>

There is no single right answer. A good answer weighs a few things:

- **Time and exams.** The formula first is quicker, and an exam or a
  calculator often wants only the number.
- **Meaning.** Steps from a question ("how far from the mean, on
  average?") give a reason for each part of the formula, which helps
  when you forget it, or have to explain a result.
- **Who the friend is.** Someone who has met the formula before might
  only need the steps named. Someone who is nervous of formulas might
  need the question first.
- **What goes wrong.** With the formula first, a common mistake is to
  forget the square root, or square the wrong thing. With the steps
  first, a common problem is a lesson that runs long.

Whichever you choose, say what it costs. That is the question the
tutorial's "Why this way?" fold asks of itself.

</details>

## Stretch

Use this cell for the stretch problems.

```python exec
id: typical-practice-scratch-3
df = await load_csv("life-expectancy.csv")
ireland = df[df.country == "Ireland"]["life_expectancy"].tolist()
print(len(ireland))
```

**13. Make.** The cell above makes Ireland's list of life expectancy
from 1950 to 2016. Find its mean, median and standard deviation. Then
make the same list for another country, such as `"Spain"` or
`"Nigeria"`, and compare.

<details class="dl-answer"><summary>answer</summary>

```python
for country in ["Ireland", "Spain", "Nigeria"]:
    years = df[df.country == country]["life_expectancy"].tolist()
    print(country, round(mean(years), 2), median(years), round(std_dev(years), 2))
# Ireland 73.79 73.26 4.18
# Spain 75.03 76.3 5.39
# Nigeria 47.01 46.15 9.79
```

Over these 67 years, Spain's typical value is a little higher than
Ireland's, and its standard deviation is bigger: Spain started lower in
1950 and rose further. Nigeria's typical value is far lower, and its
spread is the biggest of the three. A standard deviation across years
measures how much a country changed, not how far apart its people are.

</details>

**14. Another way.** Python's own `statistics` module has two standard
deviations: `statistics.pstdev`, which divides by $n$, and
`statistics.stdev`, which divides by $n - 1$. Find both for the rents,
and compare them with your `std_dev`. Which one matches yours?

<details class="dl-answer"><summary>answer</summary>

```python
import statistics

rents = [1350, 1250, 3900, 1200, 1450, 1250, 1300, 2600, 1150, 1400, 1250]
print(round(std_dev(rents), 2))              # 809.73
print(round(statistics.pstdev(rents), 2))    # 809.73
print(round(statistics.stdev(rents), 2))     # 849.25
```

`pstdev` matches yours, because both divide by $n$. The `p` stands for
population: the list is the whole group we care about. `stdev`
divides by $n - 1 = 10$ instead of 11, so its answer is a little
bigger. It is meant for a sample, a few values picked from a bigger
group, where dividing by $n$ would tend to give too small an answer.
With 11 values the two differ by about 5%. With 1,000 values, they
would be almost the same.

</details>

**15. Make.** Roll two dice 1,000 times with `random.randint`, and keep
each total in a list. Find the mean, the mode and the standard
deviation of the totals. What do you expect the mode to be, from
[How likely is it?](tutorial:how-likely-is-it#counting-equally-likely-outcomes)

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. `import random`, and start with an empty list.
2. Loop 1,000 times. Each time, append
   `random.randint(1, 6) + random.randint(1, 6)`.
3. Hand the list to `mean`, `mode` and `std_dev`.

**Think about:** which total has the most pairs of dice that make it?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
import random

dice_totals = []
for roll in range(1000):
    dice_totals.append(random.randint(1, 6) + random.randint(1, 6))

print(round(mean(dice_totals), 2))
print(mode(dice_totals))
print(round(std_dev(dice_totals), 2))
```

Your numbers will differ a little each run. The mean is close to 7, and
the mode is almost always 7, because six of the 36 pairs add up to 7,
more than any other total. The standard deviation is close to 2.4. If
the mode ever comes out as 6 or 8, that is the simulation's wobble,
and a run of 100,000 rolls would settle it.

</details>

**16. Predict.** Every flat in the rents list goes up by €50 a month.
What happens to the mean, the median and the standard deviation? What
if instead every rent went up by 10%? Predict first, then check.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Build a new list with 50 added to each rent, and another with each
   rent multiplied by 1.1.
2. Find the three numbers for each list, and compare with the old ones.

**Think about:** when every value moves up by €50, do the values get
any further apart?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
rents = [1350, 1250, 3900, 1200, 1450, 1250, 1300, 2600, 1150, 1400, 1250]

plus_fifty = []
plus_ten_percent = []
for rent in rents:
    plus_fifty.append(rent + 50)
    plus_ten_percent.append(rent * 1.1)

for rent_list in [rents, plus_fifty, plus_ten_percent]:
    print(round(mean(rent_list), 2), round(median(rent_list), 2), round(std_dev(rent_list), 2))
# 1645.45 1300 809.73
# 1695.45 1350 809.73
# 1810.0 1430.0 890.7
```

Adding €50 to every rent adds €50 to the mean and to the median, and
leaves the standard deviation exactly where it was. Every value moves
the same distance, so none of them gets further from the others.
Adding 10% multiplies all three by 1.1, the spread included, because
the big rents go up by more euro than the small ones.

</details>
