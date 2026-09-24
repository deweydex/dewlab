---
title: "A row of numbers: lists — Practice"
practice_for: a-row-of-numbers
year: "2026-2027"
version: 2026.09.24.1
datasets: [life-expectancy]
---

# A row of numbers: lists — Practice

Each answer is hidden until you open it. Where a problem asks you to
predict, the prediction is the exercise, so make one before you run
anything.

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

**3. Make.** Here is a shopping list for a stew:
`shopping = ["onions", "carrots", "beef", "stock"]`. Add `"potatoes"` at
the end. Then the shop has no beef, so change `"beef"` to `"lentils"`.
Print the list.

<details class="dl-answer"><summary>answer</summary>

```python
shopping = ["onions", "carrots", "beef", "stock"]
shopping.append("potatoes")
shopping[2] = "lentils"
print(shopping)    # ['onions', 'carrots', 'lentils', 'stock', 'potatoes']
```

`append` adds at the end. `shopping[2] = "lentils"` points position 2,
the third item, at a new value. Nothing else in the list moves.

</details>

**4. Explain.** A maths book writes a sequence as $a_1, a_2, a_3, \dots$.
In Python, the same values are in a list `a`. Which index gives $a_1$?
Which index gives $a_n$? Say why in a sentence.

<details class="dl-answer"><summary>answer</summary>

$a_1$ is `a[0]`, and $a_n$ is `a[n - 1]`.

The maths counts which value it is: first, second, third. Python counts
how many steps from the start: the first value is 0 steps along. So
every Python index is one less than the maths number. Neither is wrong;
they are two ways of counting, like the ground floor being 0 in a lift.

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

**6. Fix.** A bus leaves the stop at these times, in minutes after 8:00.
The code should print the wait between each bus and the next. It prints
the right waits, then stops with an error. Find the mistake.

```python exec
id: row-practice-fix-bus
departures = [2, 14, 21, 35, 47]

for i in range(len(departures)):
    print("wait:", departures[i + 1] - departures[i], "minutes")
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Read the last line of the error. Which kind is it?
2. How many buses are there? How many waits between them?
3. On the last time round, what is `i`, and what is `i + 1`?

**Think about:** five fence posts have how many gaps between them?

**Try this next:** can you write it with `range(1, len(departures))`
and `i - 1` instead?

</details>

<details class="dl-answer"><summary>answer</summary>

On the last time round, `i` is 4, so `departures[i + 1]` asks for index
5. The list has indexes 0 to 4, so Python stops with an `IndexError`.
Five buses have only four waits between them, so the loop should go
round four times:

```python
departures = [2, 14, 21, 35, 47]

for i in range(len(departures) - 1):
    print("wait:", departures[i + 1] - departures[i], "minutes")
```

The waits are 12, 7, 14 and 12 minutes. A step that reaches a
neighbour needs one fewer time round than there are values.

</details>

**7. Fix.** A pancake recipe for two people is kept as a list of amounts:
flour in grams, milk in ml, and eggs. The code should make a recipe for
four people and keep the recipe for two. But after it runs, the recipe
for two has doubled too. Find the mistake.

```python exec
id: row-practice-fix-pancakes
for_two = [100, 250, 1]
for_four = for_two
for i in range(len(for_four)):
    for_four[i] = for_four[i] * 2
print("for two: ", for_two)     # should be [100, 250, 1]
print("for four:", for_four)    # should be [200, 500, 2]
```

<details class="dl-answer"><summary>answer</summary>

`for_four = for_two` does not make a second list. It ties a second name
to the same list. So doubling through `for_four` doubles the only list
there is, and `for_two` sees it too. Ask for a second list with
`.copy()`:

```python
for_two = [100, 250, 1]
for_four = for_two.copy()
for i in range(len(for_four)):
    for_four[i] = for_four[i] * 2
print("for two: ", for_two)     # [100, 250, 1]
print("for four:", for_four)    # [200, 500, 2]
```

Building a new list with `append` works too, and then there is no
question of which list is which.

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

**9. Make.** The same four things cost this much in two shops, in euro:
`shop_a = [2.49, 1.10, 3.75, 0.89]` and
`shop_b = [2.29, 1.25, 3.60, 0.95]`. Build a list of the cheaper price
for each thing, and find what the whole basket costs if you always buy
at the cheaper shop.

<details class="dl-answer"><summary>answer</summary>

```python
shop_a = [2.49, 1.10, 3.75, 0.89]
shop_b = [2.29, 1.25, 3.60, 0.95]

cheaper = []
for i in range(len(shop_a)):
    cheaper.append(smallest([shop_a[i], shop_b[i]]))
print(cheaper)                  # [2.29, 1.1, 3.6, 0.89]
print(round(total(cheaper), 2)) # 7.88
```

The basket costs €7.88 at the cheaper prices. Each step needs the same
position in two lists, so the loop goes through by index. `smallest`
works on any list, even one of two values made on the spot.

</details>

**10. Another way.** A friend says `[1, 2] + [3, 4]` should give
`[4, 6]`, and Python is wrong to give `[1, 2, 3, 4]`. Is there a space
where your friend is right? Show it in a cell.

<details class="dl-answer"><summary>answer</summary>

Yes. In maths, two rows of numbers of the same length are often added
pair by pair, and numpy's arrays work that way:

```python
import numpy as np

print(np.array([1, 2]) + np.array([3, 4]))    # [4 6]
```

Your friend is using the maths meaning of `+`. Python's lists use
another meaning, joining, because a list can hold words as well as
numbers. The move is fine; it belongs to the array space, not the list
space.

</details>

**11. Explain.** `largest` starts with `biggest_so_far = values[0]`. Why
not start with `biggest_so_far = 0`? Give a list where starting at 0
would give the wrong answer.

<details class="dl-answer"><summary>answer</summary>

If every value is below 0, none of them is bigger than 0, so a start of
0 would never change, and the function would give back 0. For
`[-3, -1, -4]`, three January nights, it would say 0 when the answer is
−1. Starting from a real value in the list means the answer is always
one of the values. That is what
[Does it work?](tutorial:does-it-work#a-walkthrough-by-hand) found with
a trace table.

</details>

**12. Fix.** This code should count the cold days in a week. It stops
with an error. Find the mistake.

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

**14. Make.** A savings account gets these amounts over six months, in
euro: `saved = [50, 20, 0, 75, 40, 60]`. Build a list of the running
total at the end of each month. Check that its last value equals
`total(saved)`.

<details class="dl-answer"><summary>answer</summary>

```python
saved = [50, 20, 0, 75, 40, 60]

so_far = 0
running = []
for amount in saved:
    so_far = so_far + amount
    running.append(so_far)
print(running)                        # [50, 70, 70, 145, 185, 245]
print(running[-1] == total(saved))    # True
```

The account holds €245 at the end. This joins two shapes from this
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
the quiz scores, used on colours.

</details>
