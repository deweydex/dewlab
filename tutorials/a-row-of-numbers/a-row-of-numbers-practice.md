---
title: "A row of numbers: lists — Practice"
practice_for: a-row-of-numbers
year: "2026-2027"
version: 2026.09.25.1
datasets: [life-expectancy]
---

# A row of numbers: lists — Practice

Each answer is hidden until you open it. Where a problem asks you to
predict, the prediction is the exercise, so make one before you run
anything. A guess that turns out different from Python is the most
useful kind: it shows you exactly where to look.

Your toolkit is loaded on this page, so `largest`, `smallest` and
`count_if` are ready to use, and so are `total`, `between` and the rest.

## Warm-up

Use this cell for any of the warm-up problems.

```python exec
id: row-practice-scratch-1
playlist = ["Zombie", "Linger", "Dreams", "Salty Dog"]
print(playlist)
```

**1. Predict.** Using `playlist` from the cell above, what do these three
lines show?

```python
print(playlist[1])
print(playlist[-1])
print(len(playlist))
```

<details class="dl-answer"><summary>answer</summary>

`Linger`, then `Salty Dog`, then `4`.

Index 1 is the second song, because the first is at index 0. Index −1
is the last song, whatever the length of the list. And `len` counts
the songs: four.

</details>

**2. Predict.** A football team scored these goals in its last six
matches: `goals = [2, 0, 3, 1, 1, 4]`. What is `goals[2:5]`, and how many
values does it hold?

<details class="dl-answer"><summary>answer</summary>

`[3, 1, 1]`, three values.

```python
goals = [2, 0, 3, 1, 1, 4]
print(goals[2:5])    # [3, 1, 1]
```

The slice starts at index 2 and stops before index 5, so it holds
indexes 2, 3 and 4. It holds $5 - 2 = 3$ values.

</details>

**3. Make.** A folder holds these files, in this order:
`files = ["notes.txt", "photo.jpg", "draft.docx", "song.mp3"]`. Add
`"backup.zip"` at the end. Then the draft is finished, so change
`"draft.docx"` to `"final.docx"`. Print the list.

<details class="dl-answer"><summary>answer</summary>

```python
files = ["notes.txt", "photo.jpg", "draft.docx", "song.mp3"]
files.append("backup.zip")
files[2] = "final.docx"
print(files)    # ['notes.txt', 'photo.jpg', 'final.docx', 'song.mp3', 'backup.zip']
```

`append` adds at the end. `files[2] = "final.docx"` points position 2,
the third file, at a new value. Nothing else in the list moves.

</details>

**4. Explain.** A maths book writes a sequence as $a_1, a_2, a_3, \dots$.
In Python, the same values are in a list `a`. Which index gives $a_1$?
Which index gives $a_n$? Say why in a sentence.

<details class="dl-answer"><summary>answer</summary>

$a_1$ is `a[0]`, and $a_n$ is `a[n - 1]`.

The maths counts which value it is: first, second, third. Python counts
how many steps from the start: the first value is 0 steps along. So
every Python index is one less than the maths number. They are two
ways of counting, like the ground floor being 0 in a lift.

</details>

## Core

Use this cell for the core problems.

```python exec
id: row-practice-scratch-2
steps = [6200, 11400, 8100, 12900, 4500, 10300, 9900]
print(steps)
```

**5. Make.** The list `steps` above is one week of step counts from a
fitness watch, Monday to Sunday. How many days had more than 10,000
steps? Answer it with `count_if`. Then build a new list holding only
those step counts.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Write a test: a function that takes one step count and returns True
   when it is more than 10,000.
2. Hand the test to `count_if`, without brackets after its name.
3. For the new list, start with `[]`, and `append` inside an `if`.

**Think about:** how can you check the two answers against each other?

**Try this next:** which days of the week were they? You will need to go
through by index.

</details>

<details class="dl-answer"><summary>answer</summary>

One way through; yours may differ and work as well.

```python
def over_ten_thousand(count):
    """True when a day's step count is more than 10,000."""
    return count > 10000

print(count_if(steps, over_ten_thousand))    # 3

big_days = []
for count in steps:
    if over_ten_thousand(count):
        big_days.append(count)
print(big_days)          # [11400, 12900, 10300]
print(len(big_days))     # 3
```

Three days: Tuesday, Thursday and Saturday. The length of the new list
agrees with `count_if`, which is a good check.

</details>

**6. Fix.** A web server logs the moment each request arrives, in
milliseconds after it starts. The code should print the gap between each
request and the next. It prints four gaps, then stops with an error.
Find the line that does not do what its writer meant.

```python exec
id: row-practice-fix-bus
arrivals = [2, 14, 21, 35, 47]

for i in range(len(arrivals)):
    print("gap:", arrivals[i + 1] - arrivals[i], "ms")
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Read the last line of the error. Which kind is it?
2. How many requests are there? How many gaps between them?
3. On the last time round, what is `i`, and what is `i + 1`?

**Think about:** five fence posts have how many gaps between them?

**Try this next:** can you write it with `range(1, len(arrivals))`
and `i - 1` instead?

</details>

<details class="dl-answer"><summary>answer</summary>

On the last time round, `i` is 4, so `arrivals[i + 1]` asks for index
5. The list has indexes 0 to 4, so Python stops with an `IndexError`.
Five requests have only four gaps between them, so the loop should go
round four times:

```python
arrivals = [2, 14, 21, 35, 47]

for i in range(len(arrivals) - 1):
    print("gap:", arrivals[i + 1] - arrivals[i], "ms")
```

The gaps are 12, 7, 14 and 12 ms. A step that reaches a
neighbour needs one fewer time round than there are values.

</details>

**7. Fix.** Schlomo, who is learning Python too, is writing a photo
editor. One pixel's colour is a list of red, green and blue, from 0 to
255. He wants a brighter copy, with each part doubled, and he wants to
keep the original so that "undo" works. His idea: give the colour a
second name, and double through that name. After it runs, the original
has doubled too. What happened?

```python exec
id: row-practice-fix-pancakes
original = [100, 60, 20]
brighter = original
for i in range(len(brighter)):
    brighter[i] = brighter[i] * 2
print("original:", original)    # hoping for [100, 60, 20]
print("brighter:", brighter)    # hoping for [200, 120, 40]
```

<details class="dl-answer"><summary>answer</summary>

`brighter = original` does not make a second list. It ties a second
name to the same list. So doubling through `brighter` doubles the only
list there is, and `original` sees it too. Schlomo's idea of a second
name was half of a plan that works; the other half is a second list, from
`.copy()`:

```python
original = [100, 60, 20]
brighter = original.copy()
for i in range(len(brighter)):
    brighter[i] = brighter[i] * 2
print("original:", original)    # [100, 60, 20]
print("brighter:", brighter)    # [200, 120, 40]
```

That is one way through. Building a new list with `append` works too,
and then there is no question of which list is which. (A real editor would also stop each
part at 255, the largest value a part can hold.)

</details>

**8. Predict.** What does each line show?

```python
print([1, 2] + [3])
print([0] * 5)
print(["la"] * 3)
print(len([4, 5] + [6, 7]))
```

<details class="dl-answer"><summary>answer</summary>

```python
print([1, 2] + [3])          # [1, 2, 3]
print([0] * 5)               # [0, 0, 0, 0, 0]
print(["la"] * 3)            # ['la', 'la', 'la']
print(len([4, 5] + [6, 7]))  # 4
```

For lists, `+` joins and `*` repeats. `[0] * 5` is a handy way to start
a list of five zeros, for example to keep five running totals.

</details>

**9. Make.** A drone has two sensors that each report how full its
battery is, in percent, once a minute. They rarely agree exactly. To be
safe, the drone trusts the lower of the two readings each minute. Build
that list from `sensor_a = [98, 95, 91, 88, 86]` and
`sensor_b = [97, 96, 90, 89, 84]`, and find the lowest value the drone
trusted. (The readings are made up.)

<details class="dl-answer"><summary>answer</summary>

One way through; yours may differ and work as well.

```python
sensor_a = [98, 95, 91, 88, 86]
sensor_b = [97, 96, 90, 89, 84]

trusted = []
for i in range(len(sensor_a)):
    trusted.append(smallest([sensor_a[i], sensor_b[i]]))
print(trusted)              # [97, 95, 90, 88, 84]
print(smallest(trusted))    # 84
```

The drone trusted 97, 95, 90, 88 and 84, and the lowest was 84. Each
step needs the same position in two lists, so the loop goes through by
index. `smallest` works on any list, even one of two values made on the
spot.

</details>

**10. Another way.** Schlomi, who is learning Python too, says
`[1, 2] + [3, 4]` should give `[4, 6]`, not the `[1, 2, 3, 4]` that
Python gives. Where does her idea work, and where does it stop working?
Show it in a cell.

<details class="dl-answer"><summary>answer</summary>

It works in maths. There, two rows of numbers of the same length are often added
pair by pair, and numpy's arrays work that way:

```python
import numpy as np

print(np.array([1, 2]) + np.array([3, 4]))    # [4 6]
```

Schlomi is using the maths meaning of `+`, the one that mixes two
sounds. Python's lists use another meaning, joining, because a list can
hold words as well as numbers. Her move works in the array space, and
stops working in the list space.

</details>

**11. Explain.** `largest` starts with `biggest_so_far = values[0]`.
Schlomo thinks `biggest_so_far = 0` would be tidier: every list can
start from the same number. When does his idea work, and when does it
fail? Give a list for each.

<details class="dl-answer"><summary>answer</summary>

His idea works whenever at least one value is 0 or more, such as
`[11, 13, 9]`. But if every value is below 0, none of them is bigger
than 0, so a start of 0 would never change, and the function would give
back 0. For `[-3, -1, -4]`, three January nights, it would say 0 when
the biggest is −1. Starting from a real value in the list means the
answer is always one of the values. That is what
[Does it work?](tutorial:does-it-work#a-walkthrough-by-hand) found with
a trace table.

</details>

**12. Fix.** This code should count the cold days in a week. It stops
with an error. Find the line that does not do what its writer meant.

```python exec
id: row-practice-fix-test
week = [11, 13, 9, 12, 14, 10, 8]

def is_cold(celsius):
    """True when celsius is below 10 degrees."""
    return celsius < 10

print(count_if(week, is_cold()))
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Read the last line of the error. Which function is missing an
   argument?
2. Where in the last line is `is_cold` being called?
3. Does `count_if` want the answer of a test, or the test itself?

**Think about:** what did `simulate(heads, 1000)` hand over, on How
likely is it?

</details>

<details class="dl-answer"><summary>answer</summary>

`is_cold()` with brackets calls the test straight away, with no
temperature, so Python stops with a `TypeError` saying a positional
argument is missing. `count_if` wants the test itself, so that it can
call it once for each value. Leave the brackets off:

```python
print(count_if(week, is_cold))    # 2
```

Two cold days: Wednesday (9) and Sunday (8).

</details>

## Stretch

Use this cell for the stretch problems.

```python exec
id: row-practice-scratch-3
df = await load_csv("life-expectancy.csv")
ireland = df[df.country == "Ireland"]["life_expectancy"].tolist()
spain = df[df.country == "Spain"]["life_expectancy"].tolist()
print(len(ireland), len(spain))
```

**13. Make.** The cell above makes two lists of life expectancy, for
Ireland and for Spain, each from 1950 to 2016. In how many of those
years was Spain's higher than Ireland's? And in which year did Spain
first pass Ireland?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Both lists are in year order, so the same index is the same year in
   both.
2. Go through by index, and count the years where `spain[i]` is bigger
   than `ireland[i]`.
3. The year for index `i` is `1950 + i`. A list of those years answers
   both questions.

**Think about:** why can `count_if` not answer this on its own?

</details>

<details class="dl-answer"><summary>answer</summary>

One way through; yours may differ and work as well.

```python
years_ahead = []
for i in range(len(ireland)):
    if spain[i] > ireland[i]:
        years_ahead.append(1950 + i)
print(len(years_ahead))    # 53
print(years_ahead[0])      # 1964
```

Spain was ahead in 53 of the 67 years, every year from 1964 to 2016.
Keeping the years in a list answers both questions: its length is the
count, and its first value is the first year. `count_if` looks at one
value at a time, and this question needs a value from each of two
lists, so the loop goes through by index.

</details>

**14. Make.** A rain gauge measured this much rain in each of six
months, in mm: `rain = [110, 80, 95, 60, 70, 75]`. (The numbers are made
up.) Build a list of the running total at the end of each month, the
rain so far this year. Check that its last value equals `total(rain)`.

<details class="dl-answer"><summary>answer</summary>

One way through; yours may differ and work as well.

```python
rain = [110, 80, 95, 60, 70, 75]

so_far = 0
running = []
for month_mm in rain:
    so_far = so_far + month_mm
    running.append(so_far)
print(running)                       # [110, 190, 285, 345, 415, 490]
print(running[-1] == total(rain))    # True
```

By the end of the sixth month, 490 mm of rain had fallen. This joins two shapes from this
unit and the last: a running total, and a list built in a loop. The
list keeps every step of the total, not only the last one.

</details>

**15. Predict.** What do the two `print` lines show? Think about names
and lists before you run it.

```python
first = [1, 2, 3]
second = first
second = second + [4]
print(first)
print(second)
```

<details class="dl-answer"><summary>answer</summary>

```python
first = [1, 2, 3]
second = first
second = second + [4]
print(first)     # [1, 2, 3]
print(second)    # [1, 2, 3, 4]
```

`first` is unchanged. After the second line, the two names point at one
list. But `second + [4]` makes a new, longer list, and `=` points
`second` at that new list. The old list was never changed, so `first`
still sees `[1, 2, 3]`. If the third line had been
`second.append(4)`, the one list would have changed, and both names
would show four values.

</details>

**16. Make.** A colour on a screen can be kept as a list of three
numbers from 0 to 255: red, green and blue, as on
[Everything is ones and zeros](tutorial:everything-is-ones-and-zeros#how-ff8800-makes-orange).
Orange is `[255, 136, 0]` and a sky blue is `[135, 206, 235]`. Mix them
half and half: each part of the mix is the two parts added, then halved
with `//`. What colour list do you get?

<details class="dl-answer"><summary>answer</summary>

One way through; yours may differ and work as well.

```python
orange = [255, 136, 0]
sky_blue = [135, 206, 235]

mixed = []
for i in range(3):
    mixed.append((orange[i] + sky_blue[i]) // 2)
print(mixed)    # [195, 171, 117]
```

The mix is `[195, 171, 117]`, a light brown, a little like sand. This
is adding element by element, then halving each value: the same move as
the two notes on the tutorial page, used on colours.

</details>
