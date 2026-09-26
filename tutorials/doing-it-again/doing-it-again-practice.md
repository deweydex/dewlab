---
title: "Doing it again: loops, sums and products — Practice"
practice_for: doing-it-again
year: "2026-2027"
version: 2026.09.25.1
---

# Doing it again: loops, sums and products — Practice

Each answer is hidden until you open it. Where a problem asks you to
predict, the prediction is the exercise, so make one before you run
anything. The problems get harder as they go, on purpose. If one of the
stretch problems feels like hard work, open its hint if it has one, or
skip it and come back.

Your toolkit is loaded on this page, so `total` and `product` are ready
to use, and so are `digit_at`, `between` and the rest.

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

It prints seven lines, and the last is `End of playlist`.

The two pushed-in lines run once for each of the three songs, which
makes six lines. The last line is not pushed in, so it runs once, after
the loop has finished.

</details>

**2. Predict.** A game has levels numbered 1 to 9. Which level numbers
does `range(3, 7)` give?

<details class="dl-answer"><summary>answer</summary>

3, 4, 5 and 6. The stop number, 7, is not included.

```python
for level in range(3, 7):
    print(level)
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

The week has 51,000 steps, about 7,286 a day. The average is the total,
shared equally over the seven days.

</details>

**4. Explain.** Schlomi, who is learning Python too, reads
`count = count + 1` and says it can never be true, because in maths,
$c = c + 1$ is never true. Where does her idea work, and where does it stop working?

<details class="dl-answer"><summary>answer</summary>

Her idea works in maths, where $=$ says two sides are equal, and no
number is one more than itself. In Python, `=` is an instruction, not a
claim that two sides are equal.
It happens in two steps. First Python calculates the right-hand side,
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

**6. Fix.** Schlomo, who is learning Python too, wants the size of a
folder: the sizes of its four files, in megabytes (MB), added up. His
code prints a different number. Find why, and change it.

```python exec
id: doing-it-practice-fix-soup
file_sizes = [1.20, 0.85, 2.40, 0.60]    # sizes in MB

for size in file_sizes:
    folder = 0
    folder = folder + size
print("The folder holds", folder, "MB")    # should be 5.05
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Follow `folder` through the loop by hand, one size at a time.
2. What is `folder` just after the line `folder = 0`, every time round?
3. Which size is the only one left at the end?

**Think about:** how many times should a running total be set to 0?

**Try this next:** what would the code print if the list had the
0.60 MB file first and the 2.40 MB file last?

</details>

<details class="dl-answer"><summary>answer</summary>

`folder = 0` is inside the loop, so the running total returns to 0
every time round. At the end it holds only the last size, 0.60.
Schlomo's two lines both do their jobs. But the first one runs every
time. It must come before the loop, so that it runs only once.

```python
file_sizes = [1.20, 0.85, 2.40, 0.60]

folder = 0
for size in file_sizes:
    folder = folder + size
print("The folder holds", round(folder, 2), "MB")    # 5.05
```

`round` removes a float's tiny rounding error, so the answer shows as
5.05.

</details>

**7. Fix.** A savings jar gets 1 cent on day 1, 2 cents on day 2, and so
on. After 10 days it should hold 55 cents. This code says 45. Find
why.

```python exec
id: doing-it-practice-fix-jar
jar = 0
for day in range(1, 10):
    jar = jar + day
print(jar)    # should be 55
```

<details class="dl-answer"><summary>answer</summary>

`range(1, 10)` stops at 9, because the stop number is not included. So day
10 is never added, and $55 - 10 = 45$. The range must go one past the
last day:

```python
jar = 0
for day in range(1, 11):
    jar = jar + day
print(jar)    # 55
```

Mistakes like this, off by one at the end, are among the most common in
all of programming. If you ask "is the last one included?", you catch them.

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

These are the first four odd numbers. Problem 14 uses them again.

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
percentage changes, $+50 + 20 - 20 = 50$, would give 1.5. But scales
multiply, so adding does not work here.

</details>

**10. Make.** A new app has 5,000 users. Each week it has 10% more users
than the week before. After how many weeks does it first have more than
20,000? Use a `while` loop. (The app is made up. Real apps grow in less
tidy ways.)

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Start with two names: the users, 5000, and the number of weeks, 0.
2. Go round again while the users are not yet more than 20,000.
3. Each round, multiply the users by 1.1 and add 1 to the weeks.

**Think about:** why is this a `while` loop, and not a `for` loop?

**Try this next:** how many weeks until it has more than 40,000 users?

</details>

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Yours may be different and work too.

```python
users = 5000
weeks = 0
while users <= 20000:
    users = users * 1.1
    weeks = weeks + 1
print(weeks, round(users))    # 15 20886
```

After 15 weeks the app has about 20,886 users. After 14 weeks it had
about 18,987, not quite enough. We did not know the number of weeks at
the start, only when to stop. That is the job of a `while` loop.

</details>

**11. Another way.** A game draws a ramp in pixels, 30 rows tall. The top
row is 20 pixels wide, the next is 21, then 22, and each row is one
pixel wider than the row above. How many pixels is the ramp? Find the
answer two ways: with a loop, and with the formula
$\sum_{i=1}^{n} i = \frac{n(n+1)}{2}$.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Row $i$ has $19 + i$ pixels. Check: row 1 has 20.
2. For the loop, add $19 + i$ for each $i$ from 1 to 30.
3. For the formula, split each row into 19 pixels plus $i$ pixels. Add
   the 19s and the $i$s separately.

**Think about:** how many 19s are there in all?

**Try this next:** what if the ramp had 40 rows?

</details>

<details class="dl-answer"><summary>answer</summary>

Row $i$ has $19 + i$ pixels, so the ramp has $\sum_{i=1}^{30} (19 + i)$.

With a loop:

```python
pixels = 0
for row in range(1, 31):
    pixels = pixels + (19 + row)
print(pixels)    # 1035
```

With the formula, split each row into 19 pixels plus `row` pixels. There
are 30 groups of 19, and the rest is $1 + 2 + \dots + 30$:

$$30 \times 19 + \frac{30 \times 31}{2} = 570 + 465 = 1035$$

```python
print(30 * 19 + 30 * 31 // 2)    # 1035
```

Both ways give 1,035 pixels. You might have found another
way, such as pairing the top row with the bottom
row, as Gauss did.

</details>

**12. Explain.** For each job, would you use a `for` loop or a `while`
loop? Say why.

1. Print a line for every file in a folder of 15 files.
2. Keep rolling a die until you roll a 6.
3. Add up the brightness of every pixel in a row of an image.
4. Keep dropping a ball until a bounce is under 1 cm.

<details class="dl-answer"><summary>answer</summary>

1. `for`: we know the files, one for each.
2. `while`: we know when to stop (a 6), but not how many rolls it takes.
3. `for`: we know the pixels.
4. `while`: we know when to stop, but not how many bounces it takes.
   (The tutorial found it: 21, for a ball that keeps 80%.)

The question to ask is: do I know the values, or how many times? Then
`for`. Do I only know when to stop? Then `while`.

</details>

## Stretch

Use this cell for the stretch problems.

```python exec
id: doing-it-practice-scratch-3
# Use this cell for the stretch problems
```

**13. Make.** A game adds up your points from four rounds: 480, 1250,
95 and 700. Its score display lights one digit at a time, from the
thousands down. Use `total` to find the score. Then use a `for` loop
and your `digit_at` from
[Numbers a computer can hold](tutorial:numbers-a-computer-can-hold) to
print the four digits the display lights, from left to right.

<details class="dl-answer"><summary>answer</summary>

```python
rounds = [480, 1250, 95, 700]
score = total(rounds)
print(score)                        # 2525
for place in [3, 2, 1, 0]:
    print(digit_at(score, place))   # 2, then 5, then 2, then 5
```

The score is 2525, and the loop prints 2, 5, 2 and 5. In Unit 1, the
display needed one line for each digit. The loop does the same job for
any number of places. Here the answer from `total` goes into `digit_at`.

</details>

**14. Another way.** Problem 8 found $1 + 3 + 5 + 7 = 16$. Print the sum
of the first $n$ odd numbers, for each $n$ from 1 to 7. What do you
notice? Then find a picture that explains it.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The $i$th odd number is $2i - 1$.
2. Loop over $n$ from 1 to 7. For each $n$, add up $2i - 1$ for $i$ from
   1 to $n$. `total(range(1, 2 * n, 2))` does that too. `range` can take
   a third number, the step.
3. Look at the answers. Have you seen these numbers before?

**Think about:** draw 1 dot, then add 3 dots around it to make a square,
then 5 more. What shape do the dots make each time?

**Try this next:** what is the sum of the first 100 odd numbers?

</details>

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Yours may be different and work too.

```python
for n in range(1, 8):
    print(n, total(range(1, 2 * n, 2)))
```

The sums are 1, 4, 9, 16, 25, 36, 49. These are the square numbers:
$\sum_{i=1}^{n} (2i - 1) = n^2$.

Here is the picture. A 1 by 1 square of dots is 1 dot. Add 3 dots along the
right side and the top, in an L shape, and you have a 2 by 2 square.
Add an L of 5 dots, and you have 3 by 3. Each new odd number is the L
that makes the square one bigger. So the first 100 odd numbers add up
to $100^2 = 10000$.

</details>

**15. Make.** A game has a picture 1000 pixels wide. To draw it far
away, it makes a copy half as wide, then a copy half as wide as that,
and so on. How many halvings until a copy is less than 1 pixel wide?
Use a `while` loop. Then compare with `math.log2(1000)`.

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Yours may be different and work too.

```python
import math

width = 1000
halvings = 0
while width >= 1:
    width = width / 2
    halvings = halvings + 1
print(halvings, width)       # 10 0.9765625
print(math.log2(1000))       # 9.965784284662087
```

After 10 halvings, the copy is less than 1 pixel wide. Games really do
this. The smaller copies of a picture are called "mipmaps", and each
one is half the width of the one before. On
[Numbers a computer can hold](tutorial:numbers-a-computer-can-hold#powers-and-how-many-times),
a logarithm was "how many times do I multiply by 2?". Halving asks the
same question backwards. $\log_2 1000$ is about 9.97, so 9 halvings
are not quite enough and the 10th takes it under 1 pixel. The loop counts
the halvings one by one, and the logarithm gives the answer in one step.

</details>

**16. Predict.** Schlomi writes her own product function, and tests
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
runs, and the function returns the starting number, 0.

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

The empty list shows why the starting number matters. It is the answer
when there is nothing to multiply.

</details>
