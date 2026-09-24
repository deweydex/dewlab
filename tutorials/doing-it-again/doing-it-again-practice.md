---
title: "Doing it again: loops, sums and products — Practice"
practice_for: doing-it-again
year: "2026-2027"
version: 2026.09.24.1
---

# Doing it again: loops, sums and products — Practice

Each answer is hidden until you open it. Where a problem asks you to
predict, the prediction is the exercise, so make one before you run
anything.

Your toolkit is loaded on this page, so `total` and `product` are ready
to use, and so are `split_bill`, `between` and the rest.

## Warm-up

Use this cell for any of the warm-up problems. Type a few lines, and run
them.

```python exec
id: doing-it-practice-scratch-1
for number in range(1, 4):
    print(number)
```

**1. Predict.** A playlist has three songs. How many lines does this
print, and what is the last one?

```python
playlist = ["Intro", "Chorus", "Outro"]
for song in playlist:
    print("Now playing:", song)
    print("---")
print("End of playlist")
```

<details class="dl-answer"><summary>answer</summary>

Seven lines, and the last is `End of playlist`.

The two pushed-in lines run once for each of the three songs, which
makes six lines. The last line is not pushed in, so it runs once, after
the loop has finished.

</details>

**2. Predict.** A bus route has stops numbered 1 to 9. Which stop numbers
does `range(3, 7)` give?

<details class="dl-answer"><summary>answer</summary>

3, 4, 5 and 6. The stop number, 7, is left out.

```python
for stop in range(3, 7):
    print(stop)
```

A handy check: `range(3, 7)` gives $7 - 3 = 4$ numbers.

</details>

**3. Make.** A fitness watch counted these steps over one week:
`[6200, 8100, 4500, 9900, 7300, 12000, 3000]`. Use `total` to find the
steps for the whole week, and then the average per day.

<details class="dl-answer"><summary>answer</summary>

```python
steps = [6200, 8100, 4500, 9900, 7300, 12000, 3000]
week_steps = total(steps)
print(week_steps)         # 51000
print(week_steps / 7)     # 7285.714285714285
```

The week has 51,000 steps, about 7,286 a day. The average is the total
shared out equally over the seven days.

</details>

**4. Explain.** In maths, $c = c + 1$ can never be true. Why is
`count = count + 1` a sensible line of Python?

<details class="dl-answer"><summary>answer</summary>

In Python, `=` is an instruction, not a claim that two sides are equal.
It happens in two steps. First Python works out the right-hand side,
`count + 1`, using the value `count` has now. Then it points the name
`count` at the answer. So if `count` was 4, it is now 5. The line means
"count is now one more than it was".

</details>

## Core

Use this cell for the core problems.

```python exec
id: doing-it-practice-scratch-2
rainfall = [148, 110, 115, 85, 80, 85, 90, 110, 120, 160, 150, 165]
print(total(rainfall))
```

**5. Make.** The list `rainfall` in the cell above is the rain, in mm,
for each month of one year at a weather station in the west of Ireland.
(The numbers are made up, but close to real ones.) Write a loop that
counts how many months had more than 150 mm.

<details class="dl-answer"><summary>answer</summary>

```python
wet_months = 0
for mm in rainfall:
    if mm > 150:
        wet_months = wet_months + 1
print(wet_months)     # 2
```

Two months, October (160 mm) and December (165 mm). November had
exactly 150 mm, which is not more than 150. A count is a running total
that adds 1 each time, and only when the `if` is True. The whole year
had 1,418 mm.

</details>

**6. Fix.** This code should add up the cost of the ingredients for a
pot of soup. It prints the wrong answer. Find the one mistake, and fix
it.

```python exec
id: doing-it-practice-fix-soup
ingredients = [1.20, 0.85, 2.40, 0.60]    # onions, carrots, stock, herbs

for cost in ingredients:
    basket = 0
    basket = basket + cost
print("The soup costs", basket)    # should be 5.05
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Follow `basket` through the loop by hand, one cost at a time.
2. What is `basket` just after the line `basket = 0`, every time round?
3. Which cost is the only one left at the end?

**Think about:** how many times should a running total be set to 0?

**Try this next:** what would the code print if the list had the herbs
first and the stock last?

</details>

<details class="dl-answer"><summary>answer</summary>

`basket = 0` is inside the loop, so the running total goes back to 0
every time round. At the end it holds only the last cost, 0.60. The
line must come before the loop, so that it runs only once:

```python
ingredients = [1.20, 0.85, 2.40, 0.60]

basket = 0
for cost in ingredients:
    basket = basket + cost
print("The soup costs", round(basket, 2))    # 5.05
```

`round` tidies away a float's tiny rounding, so the answer shows as
5.05.

</details>

**7. Fix.** A savings jar gets 1 cent on day 1, 2 cents on day 2, and so
on. After 10 days it should hold 55 cents. This code says 45. Find the
mistake.

```python exec
id: doing-it-practice-fix-jar
jar = 0
for day in range(1, 10):
    jar = jar + day
print(jar)    # should be 55
```

<details class="dl-answer"><summary>answer</summary>

`range(1, 10)` stops at 9, because the stop number is left out. So day
10 is never added, and $55 - 10 = 45$. The range must go one past the
last day:

```python
jar = 0
for day in range(1, 11):
    jar = jar + day
print(jar)    # 55
```

Mistakes like this, off by one at the end, are among the most common in
all of programming. Asking "is the last one included?" catches them.

</details>

**8. Predict.** What is $\sum_{i=1}^{4} (2i - 1)$? Write out each term
first, then add them. Then check with a loop.

<details class="dl-answer"><summary>answer</summary>

The terms are $2(1) - 1 = 1$, $2(2) - 1 = 3$, $5$ and $7$. Their sum is
$1 + 3 + 5 + 7 = 16$.

```python
result = 0
for i in range(1, 5):
    result = result + (2 * i - 1)
print(result)    # 16
```

These are the first four odd numbers. Problem 14 comes back to them.

</details>

**9. Make.** On a phone, you enlarge a photo to 150%, then to 120% of
that, then shrink it to 80% of that. Use `product` to find how many
times bigger than the original the photo is now.

<details class="dl-answer"><summary>answer</summary>

150% is a scale of 1.5, 120% is 1.2, and 80% is 0.8.

```python
scales = [1.5, 1.2, 0.8]
print(product(scales))    # 1.44
```

The photo is 1.44 times as wide as the original. In pi notation that is
$\prod_{i=1}^{3} s_i$, where $s_i$ is the $i$th scale. Adding the
percentage changes, $+50 + 20 - 20 = 50$, would say 1.5, which is wrong:
scales multiply.

</details>

**10. Make.** A runner can run 5 km today. Each week, she runs 10% further
than the week before. After how many weeks can she first run more than a
half marathon, 21.1 km? Use a `while` loop.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Start with two names: the distance, 5, and the number of weeks, 0.
2. Go round again while the distance is not yet more than 21.1.
3. Each round, multiply the distance by 1.1 and add 1 to the weeks.

**Think about:** why is this a `while` loop, and not a `for` loop?

**Try this next:** how many weeks until she can run a full marathon,
42.2 km?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
distance = 5
weeks = 0
while distance <= 21.1:
    distance = distance * 1.1
    weeks = weeks + 1
print(weeks, round(distance, 1))    # 16 23.0
```

After 16 weeks she can run about 23 km. After 15 weeks it was about
20.9 km, not quite enough. We did not know the number of weeks at the
start, only when to stop. That is the job of a `while` loop.

</details>

**11. Another way.** A small stadium has 30 rows of seats. Row 1 has 20
seats, row 2 has 21, row 3 has 22, and each row has one more than the
row in front. How many seats are there? Find the answer two ways: with a
loop, and with the formula $\sum_{i=1}^{n} i = \frac{n(n+1)}{2}$.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Row $i$ has $19 + i$ seats. Check: row 1 has 20.
2. For the loop, add $19 + i$ for each $i$ from 1 to 30.
3. For the formula, split each row into 19 seats plus $i$ seats. Add
   the 19s and the $i$s separately.

**Think about:** how many 19s are there in all?

**Try this next:** what if the stadium had 40 rows?

</details>

<details class="dl-answer"><summary>answer</summary>

Row $i$ has $19 + i$ seats, so the stadium has $\sum_{i=1}^{30} (19 + i)$.

With a loop:

```python
seats = 0
for row in range(1, 31):
    seats = seats + (19 + row)
print(seats)    # 1035
```

With the formula, split each row into 19 seats plus `row` seats. There
are 30 lots of 19, and the rest is $1 + 2 + \dots + 30$:

$$30 \times 19 + \frac{30 \times 31}{2} = 570 + 465 = 1035$$

```python
print(30 * 19 + 30 * 31 // 2)    # 1035
```

Both routes give 1,035 seats.

</details>

**12. Explain.** For each job, would you use a `for` loop or a `while`
loop? Say why.

1. Print a line for every player in a squad of 15.
2. Keep rolling a die until you roll a 6.
3. Add up the cost of every item on a till receipt.
4. Keep heating a kettle until the water reaches 100 °C.

<details class="dl-answer"><summary>answer</summary>

1. `for`: we know the players, one for each.
2. `while`: we know when to stop (a 6), but not how many rolls it takes.
3. `for`: we know the items.
4. `while`: we know when to stop, but not how many seconds it takes.

The question to ask is: do I know the values, or how many times? Then
`for`. Do I only know when to stop? Then `while`.

</details>

## Stretch

Use this cell for the stretch problems.

```python exec
id: doing-it-practice-scratch-3
# Use this cell for the stretch problems
```

**13. Make.** Four friends go on a weekend trip. They spend €240 on a
hostel, €85.50 on train tickets, €60 on food and €34.50 on a museum.
They add 10% for small extras, and share the cost equally. Use `total`
and your `split_bill` from
[Numbers a computer can hold](tutorial:numbers-a-computer-can-hold) to
find each person's share.

<details class="dl-answer"><summary>answer</summary>

```python
costs = [240, 85.50, 60, 34.50]
trip = total(costs)
print(trip)                        # 420.0
print(split_bill(trip, 4, 10))     # 115.5
```

The trip cost €420, and with 10% added for extras, each friend pays
€115.50. `split_bill`'s "tip" works for any percentage added on. One
tool hands its answer to the next.

</details>

**14. Another way.** Problem 8 found $1 + 3 + 5 + 7 = 16$. Print the sum
of the first $n$ odd numbers, for each $n$ from 1 to 7. What do you
notice? Then find a picture that explains it.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The $i$th odd number is $2i - 1$.
2. Loop over $n$ from 1 to 7. For each $n$, add up $2i - 1$ for $i$ from
   1 to $n$. `total(range(1, 2 * n, 2))` does that too: `range` can take
   a third number, the step.
3. Look at the answers. Have you seen these numbers before?

**Think about:** draw 1 dot, then add 3 dots around it to make a square,
then 5 more. What shape do the dots make each time?

**Try this next:** what is the sum of the first 100 odd numbers?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
for n in range(1, 8):
    print(n, total(range(1, 2 * n, 2)))
```

The sums are 1, 4, 9, 16, 25, 36, 49. These are the square numbers:
$\sum_{i=1}^{n} (2i - 1) = n^2$.

The picture: a 1 by 1 square of dots is 1 dot. Add 3 dots along the
right side and the top, in an L shape, and you have a 2 by 2 square.
Add an L of 5 dots, and you have 3 by 3. Each new odd number is the L
that makes the square one bigger. So the first 100 odd numbers add up
to $100^2 = 10000$.

</details>

**15. Make.** A pizza of 1000 g is cut in half, and one half is given
away. Then what is left is cut in half, and one half is given away
again. How many times can you do this before less than 1 g is left?
Use a `while` loop. Then compare with `math.log2(1000)`.

<details class="dl-answer"><summary>answer</summary>

```python
import math

pizza = 1000
halvings = 0
while pizza >= 1:
    pizza = pizza / 2
    halvings = halvings + 1
print(halvings, pizza)       # 10 0.9765625
print(math.log2(1000))       # 9.965784284662087
```

After 10 halvings, less than 1 g is left. On
[Numbers a computer can hold](tutorial:numbers-a-computer-can-hold#powers-and-how-many-times),
a logarithm was "how many times do I multiply by 2?". Halving is the
same question run backwards: $\log_2 1000$ is about 9.97, so 9 halvings
are not quite enough and the 10th takes it under 1 g. The loop counts
the halvings one by one, and the logarithm gives the answer in one step.

</details>

**16. Predict.** Someone writes their own product function, and tests
it. What do the two `print` lines show? Explain the result, and fix the
function.

```python exec
id: doing-it-practice-predict-product
def product_draft(values):
    """Multiply every number in values together."""
    running = 0
    for value in values:
        running = running * value
    return running

print(product_draft([2, 3, 4]))    # hoping for 24
print(product_draft([]))           # hoping for 1
```

<details class="dl-answer"><summary>answer</summary>

Both lines show 0.

`running` starts at 0, and 0 multiplied by anything is 0. So the
answer is 0 whatever the list holds. With an empty list, the loop never
runs, and the function gives back the starting number, 0.

The fix is to start at 1, the number that changes nothing when you
multiply by it:

```python
def product_draft(values):
    running = 1
    for value in values:
        running = running * value
    return running

print(product_draft([2, 3, 4]))    # 24
print(product_draft([]))           # 1
```

The empty list shows why the starting number matters: it is the answer
when there is nothing to multiply.

</details>
