---
title: "Running totals: adding up as you go — Practice"
practice_for: running-totals
year: "2026-2027"
version: 2026.09.26.1
---

<!-- TEMPLATE: a practice page. The mix of problem kinds is yours to choose.
The kinds below are ideas, not a quota: predict, make, fix, explain, another
way, open-ended. Two or three problems come from earlier pages
(#nothing-taught-once). Code problems carry blocks; a problem done by hand
gets a "one way through it" fold. -->

# Running totals: adding up as you go — Practice

Problems on running totals, and two from earlier pages. Try each one before
you open anything under it.

## 1. A total that multiplies

<!-- Predict. -->

This loop multiplies instead of adding. What will it print?

```python exec
id: a-total-that-multiplies-1
product = 1
for number in [2, 3, 4]:
    product = product * number
print(product)
```

```predict
type: number

What will the last line print?
```

Why does `product` start at 1, not 0? What would it print if it started at
0?

<details class="dl-answer"><summary>answer</summary>

It prints 24: 1 × 2 × 3 × 4. Starting at 0 would print 0, because 0 times
anything is 0. An accumulator starts at the number that changes nothing:
0 for adding, 1 for multiplying.

</details>

## 2. A tool for any list

<!-- Make. A solution block and an inputs block replace a hand-written
answer. The author lists inputs only; what the solution gives comes from
running it. Two solutions make two tiers; the comparison uses the first. -->

Can you make a function, `line_up(widths)`, that gives back the total of
any list of widths?

```python exec
id: a-tool-for-any-list-1
def line_up(widths):
    ...
```

```solution
title: with what you've met so far
def line_up(widths):
    total = 0
    for width in widths:
        total = total + width
    return total
```

```solution
title: a shorter way you'll meet later
def line_up(widths):
    return sum(widths)
---
Python's own `sum()` is an accumulator somebody else wrote.
```

```inputs
line_up([4879, 12104, 12756, 6792])
line_up([])          # an empty list
line_up([-3, 3])     # a negative width makes no sense, but what happens?
```

## 3. One planet short

<!-- Fix. -->

Somebody wrote this loop to add up the rocky planets. It gives 29,739.
Which planet is missing, and why?

```python exec
id: one-planet-short-1
widths = [4879, 12104, 12756, 6792]
total = 0
for index in range(len(widths) - 1):
    total = total + widths[index]
print(total)
```

```solution
widths = [4879, 12104, 12756, 6792]
total = 0
for index in range(len(widths)):
    total = total + widths[index]
print(total)
---
`range(len(widths) - 1)` gives 0, 1 and 2, so the last width, Mars, is
never added. `range(len(widths))` gives all four indexes. A loop straight
over the list, `for width in widths:`, cannot miss one at all.
```

```inputs
total
```

```hint
Can you print `index` inside the loop? Which indexes does it visit?
```

## 4. Not an equation

<!-- Explain. An answer fold, since there is no code to compare. -->

In mathematics, $t = t + w$ has no answer unless $w$ is 0. In Python,
`total = total + width` works every time round the loop. What is different
about the `=` sign?

<details class="dl-answer"><summary>one good answer</summary>

In mathematics, `=` says two things are equal, always. In Python, `=` is an
action: find the value of the right-hand side, then give that value the name
on the left. So `total = total + width` means "the new total is the old total plus
this width". Your own way of saying it may be clearer than this one.

</details>

## 5. Adding up to a hundred

<!-- By-hand mathematics, with a "one way through it" fold rather than a
solution block. -->

Without a loop, and without a calculator, can you find
$1 + 2 + 3 + \dots + 100$?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Write the sum forwards, and underneath it, backwards.
2. Add each pair of numbers that sit one above the other.
3. How many pairs are there, and what does each come to?

**Think about:** why that gives twice the sum, not the sum.

**Try this next:** $1 + 2 + \dots + 1000$.

</details>

<details class="dl-answer"><summary>one way through it</summary>

Forwards, $1 + 2 + \dots + 100$. Backwards, $100 + 99 + \dots + 1$. Each of
the 100 pairs adds to 101, so the two rows together make
$100 \times 101 = 10100$. That is the sum twice, so the sum is 5050.

A loop gets the same answer, and you can check it:

    total = 0
    for number in range(1, 101):
        total = total + number
    print(total)

</details>

## 6. From earlier: the first and the last

<!-- From earlier. Two or three problems from earlier pages, named as
such, so the reader meets an idea again a week later. -->

From *Lists and sequences*. With `widths = [4879, 12104, 12756, 6792]`, what
do `widths[0]` and `widths[-1]` give?

<details class="dl-answer"><summary>answer</summary>

`widths[0]` is 4879, the first width (Mercury). `widths[-1]` is 6792, the
last one (Mars). A negative index counts from the end.

</details>

## 7. From earlier: a name that is not there

From *Reading an error message*. A cell prints `NameError: name 'totl' is
not defined`. What is the first thing you would look for?

<details class="dl-answer"><summary>answer</summary>

A name typed differently here from where it was made: `totl` here, `total`
where the value was given.

</details>

## 8. Your own list

<!-- Open-ended: a first step anyone can take, and no top
(#low-floor-high-ceiling). -->

Find a list of numbers you would like to add up: the goals in a season,
the pages of the books on a shelf, the heights of the mountains you can see
from home. What else could the loop find as it goes? The biggest number in
the list, as well as the total?
