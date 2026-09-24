---
title: "Doing it again: loops, sums and products"
year: "2026-2027"
version: 2026.09.24.1
covers:
  a-coffee-a-day:
    touches: [PDP-LO6]
  doing-it-for-each:
    covers: [PDP-LO6]
  a-running-total:
    covers: [PDP-LO6]
  counting-with-range:
    covers: [PDP-LO6]
  sigma-a-loop-written-by-mathematicians:
    covers: [MIT-6.4]
  pi-multiplying-instead-of-adding:
    covers: [MIT-6.4]
  until-something-is-true-while:
    covers: [PDP-LO6]
  two-tools-for-your-toolkit:
    touches: [MIT-6.4, PDP-LO6]
---

# Doing it again: loops, sums and products

You buy a coffee most mornings. It is only a few euro each time. How
much does it come to over a whole year? And what if the price is
different from day to day, or goes up every year?

On this page we:

- repeat some lines once for each value in a row of values, with `for`
- keep a running total, and see why where each line sits matters
- count through days with `range()`, and choose inside a loop
- read sigma, $\sum$, and pi, $\prod$: loops, written by mathematicians
- repeat until something is true, with `while`
- add `total` and `product` to your toolkit

> **The space we're in.** Numbers, and lines of Python that run from the
> top down, one after another. New on this page: a few lines can run
> again and again, and Python decides how many times from what we give
> it. One thing usually goes unsaid: a loop runs very fast. A loop that
> runs a million times is over in about a second, and it never gets
> bored or loses count.

## Warm-up

Two questions from earlier pages. The first is from
[Numbers a computer can hold](tutorial:numbers-a-computer-can-hold), and
the second from
[True, false and every case](tutorial:true-false-and-every-case).

```question
id: doing-it-warm-up-1
type: fill-in-the-blank

A year starts on a Monday, day 1. Day 15 is also a Monday. `15 % 7`, the
remainder after taking out whole weeks, is {1}.
```

```question
id: doing-it-warm-up-2
type: multiple-choice
correct: 3

A loop over `[False, True]` sits inside another loop over
`[False, True]`. The inner loop prints one line each time round. How
many lines are printed in all?

- 2
- 3
- 4
- 8
```

## A coffee a day

Say a coffee costs €3.20, and you buy one every day. Before you run the
cell, guess the cost of a year of coffee. Any guess will do.

```python exec
id: doing-it-coffee-1
price = 3.20
print(price * 5)
print(price * 365)
```

Five work days cost €16, and a year costs €1,168. When every day costs the
same, one multiplication answers the question.

But a real week is not like that. On Monday you have a flat white at
€3.20. On Tuesday you skip it. On Wednesday you have a large one at
€3.50. Now there is no single price to multiply by, and we need to add
up seven different numbers. For a year, it would be 365.

What we want is a way to say "do this again, once for each day". Every
recipe already has a way to say it. On
[Recipes are algorithms](tutorial:recipes-are-algorithms#steps-that-repeat-and-steps-that-choose)
it was repetition: "for each cup, pour the tea".

## Doing it for each

Here is the plan for a week, first in pseudocode:

```text
SET week TO the seven prices, Monday to Sunday
REPEAT for each price in week:
    SHOW the price
SAY that was the whole week
```

And here it is in Python. The first line keeps the seven prices under
one name, `week`. The square brackets make a *list*: a row of values,
kept in order. A list can hold as many values as we like. That is all we
need from lists for now; Unit 5 is where we learn them properly.

How many lines do you think the cell will print? Count before you run
it.

```python exec
id: doing-it-for-1
week = [3.20, 0, 3.50, 3.20, 2.90, 4.10, 0]

for price in week:
    print(price)
print("That was the whole week.")
```

Eight lines: one for each of the seven prices, then one more. Here is
what happened, in order.

1. The `for` line pointed the name `price` at the first value, 3.2.
2. Python ran the pushed-in line, which printed 3.2.
3. Python went back to the `for` line. It pointed `price` at the next
   value, 0, and ran the pushed-in line again.
4. It did the same for every value in the list, in order.
5. When the list ran out, Python went on to the first line that is not
   pushed in, and printed "That was the whole week."

A loop is a group of lines that Python runs again and again. A `for`
loop runs them once for each value in a row of values. You met one on
[True, false and every case](tutorial:true-false-and-every-case), going
through `[False, True]`, and it works the same way for seven prices or a
thousand. The pushed-in lines are the *loop body*. The name on the
`for` line, here `price`, is the *loop variable*: each time round, it
points at the next value.

### Your turn

1. Change the prices in `week` to a week of your own. Put in as many
   days as you like, and run the cell.
2. Put four spaces in front of the last line, so that it is pushed in
   like `print(price)`. Before you run it, how many times do you think
   it will print "That was the whole week."?
3. Take the four spaces out again.

## A running total

Printing each price is a start. We wanted the whole week added up. Here
is how you might do it on paper, one day at a time:

| Day | Price | Spent so far |
|---|---|---|
| (start) | | 0 |
| Monday | 3.20 | 3.20 |
| Tuesday | 0 | 3.20 |
| Wednesday | 3.50 | 6.70 |
| Thursday | 3.20 | 9.90 |

Each row does the same thing: take what was spent so far, and add the
new price. That is a job for a loop. A *running total* is a name that
holds the total so far, and grows each time round the loop.

Before you run the cell, what do you think the last line will print?

```python exec
id: doing-it-running-1
week = [3.20, 0, 3.50, 3.20, 2.90, 4.10, 0]

spent = 0
for price in week:
    spent = spent + price
    print("so far:", spent)
print("The week cost", spent)
```

The week cost €16.90. Look at the line `spent = spent + price`. In maths,
"spent equals spent plus price" would be false, unless the price was 0.
In Python, `=` is not a claim that two things are equal. It is an
instruction, and it happens in two steps. First, Python works out the
right-hand side, `spent + price`, using the old value of `spent`. Then
it points the name `spent` at the answer. So the line means "spent is
now what it was, plus this price".

You may also see `spent += price`, which is short for the same line.
This page uses the longer one, because it says what happens.

Where each line sits matters too.

```question
id: doing-it-running-2
type: multiple-choice
correct: 2

Someone moves `spent = 0` inside the loop, just above
`spent = spent + price`. What does the last line print now?

- The week cost 16.9
- The week cost 0
- The week cost 3.2
- An error, because `spent` is made twice
```

Each time round, the loop would set `spent` back to 0, then add one
price. So at the end, `spent` holds only the last price, Sunday's 0. A
running total must start before the loop, so that it is set to 0 only once.
Try it in the cell above, if you like, and then put the line back.

## Counting with range()

A year has 365 days. Nobody wants to type 365 prices. When the loop
should count, `range()` gives the numbers for us. You met it on
[Untangling a condition](tutorial:untangling-a-condition#not-between).
`range(1, 8)` gives the whole numbers from 1 up to 7. The last number,
8, is left out.

What will this print? Run it to check.

```python exec
id: doing-it-range-1
for day in range(1, 8):
    print("day", day)
```

Now a year of coffee at €3.20 a day, added up one day at a time. We
already know the answer from the first cell: €1,168. Will the loop agree
exactly? Guess, then run it.

```python exec
id: doing-it-range-2
spent = 0
for day in range(1, 366):
    spent = spent + 3.20
print(spent)
print(3.20 * 365)
```

Python actually prints `1168.000000000008` for the loop. That is not a
mistake in the loop. A float is very close to 3.20, but not exactly
3.20, as
[Everything is ones and zeros](tutorial:everything-is-ones-and-zeros#why-01-02-is-not-03)
showed. Each addition rounds a tiny amount, and 365 additions add up
365 tiny amounts. `round(spent, 2)` gives 1168.0, to the nearest cent.

### Choosing inside a loop

Most people buy coffee on work days only. Our year starts on a Monday,
day 1. So a day is Monday to Friday when `day % 7` is 1, 2, 3, 4 or 5.
Saturday gives 6, and Sunday gives 0. Your toolkit already has the right
tool for "1 to 5":
[`between`](tutorial:choosing-a-path#a-tool-of-your-own-between).

How many work-day coffees are there in the year? Guess before you run
it.

```python exec
id: doing-it-range-3
spent = 0
coffees = 0
for day in range(1, 366):
    if between(day % 7, 1, 5):    # day 1 is a Monday
        spent = spent + 3.20
        coffees = coffees + 1
print(coffees, "coffees")
print(round(spent, 2))
```

That is 261 coffees and €835.20. There are 52 whole weeks of five work
days, which makes 260, and the 365th day is a Monday again.

Look at what this small program uses. It keeps values under names
(`spent`, `coffees`): that is *storage*. It chooses with `if`: that is
selection. It repeats with `for`: that is iteration. Those are the three
shapes of step from
[Recipes are algorithms](tutorial:recipes-are-algorithms), and between
them they can build any program. Planning a program from those shapes is
called *structured design*.

### Your turn

1. Change 3.20 to the price of a coffee, or tea, or bus fare, that you
   pay. Run the cell again.
2. Change the cell to count weekend days only. Saturday and Sunday give
   `day % 7` of 6 and 0. Before you run it, how many weekend days do
   you think a year has?

## Sigma: a loop written by mathematicians

Here is a savings plan some people try. On day 1 of the year, put 1 cent
in a jar. On day 2, put in 2 cents. On day 3, 3 cents, and so on, until
day 365, when you put in 365 cents. How much is in the jar at the end?
Guess in euro first.

Maths has a short way to write a list of numbers like these. We call
them $x_1, x_2, x_3$ and so on, up to $x_{365}$. The small number is the
*index*: it says which one we mean. So $x_3$ is the amount on day 3,
and $x_i$ is the amount on day $i$, whichever day $i$ is. Here $x_i = i$.

Adding up all of them is written with a Greek capital S, called sigma:

$$\sum_{i=1}^{365} i$$

This is *sigma notation*: a way to write "add up every value, for each
index from here to there". Say it as "the sum of $i$, for $i$ from 1 to
365". It is a loop, written by mathematicians. Every part of it has a
place in a `for` loop:

| In the sigma | What it says | In Python |
|---|---|---|
| $i = 1$, underneath | start the index at 1 | `for i in range(1, ...)` |
| $365$, on top | stop after 365, and include it | `range(..., 366)`, one past the end |
| $i$, after the sigma | what to add each time | `jar = jar + i` |
| $\sum$ itself | add them all up | a running total that starts at 0 |

Here is the sigma, as a loop. Run it and compare with your guess.

```python exec
id: doing-it-sigma-1
jar = 0
for i in range(1, 366):
    jar = jar + i
print(jar, "cents")
```

66,795 cents is €667.95, from a few cents a day.

There is a shortcut. A story says that a young Carl Friedrich Gauss was
asked to add 1 to 100 at school, and found the answer in a moment. Here
is the idea. Write the numbers forwards, and under them write them
backwards:

| forwards | 1 | 2 | 3 | … | 364 | 365 |
|---|---|---|---|---|---|---|
| backwards | 365 | 364 | 363 | … | 2 | 1 |
| added | 366 | 366 | 366 | … | 366 | 366 |

Every column adds to 366, and there are 365 columns. So the two rows
together make $365 \times 366$, and that is the sum twice. The sum is
half of it. In words: the sum of 1 to $n$ is $n$ times $n + 1$, halved.
In symbols:

$$\sum_{i=1}^{n} i = \frac{n(n+1)}{2}$$

A formula like this is a promise, so let's check it. Python has a
built-in `sum()`, which adds up a row of values for us. Will the two
columns agree for every $n$? Run it to check.

```python exec
id: doing-it-sigma-2
for n in [1, 2, 3, 10, 100, 365]:
    print(n, sum(range(1, n + 1)), n * (n + 1) // 2)
```

They agree every time. The formula is much faster, and the loop is the
proof we can follow step by step, so we check the formula against the
loop.

Sigma works for any list, not only 1, 2, 3. If $x_1$ to $x_7$ are the
week's coffee prices, then the week's cost is $\sum_{i=1}^{7} x_i$. That
is the running total from earlier, with a new name.

### Your turn

1. What is $\sum_{i=1}^{5} i^2$? That means $1^2 + 2^2 + 3^2 + 4^2 + 5^2$.
   Work it out on paper first.
2. Change the loop in the cell below so that it adds $i^2$ each time,
   and check your answer. (In Python, $i^2$ is `i ** 2`.)
3. Try $\sum_{i=1}^{10} 2i$. What do you notice about the answer?

```python exec
id: doing-it-sigma-your-turn
result = 0
for i in range(1, 6):
    result = result + i
print(result)
```

## Pi: multiplying instead of adding

Prices do not stay still. Say a coffee cost €3.20 four years ago. Then
prices rose by 2% in the first year, 8% in the second, 6% in the third
and 2% in the fourth. That is roughly what Irish prices did from 2021 to
2024. What does the coffee cost now?

A rise of 8% means the price is multiplied by 1.08. So the four years
multiply the price by 1.02, then 1.08, then 1.06, then 1.02. We need a
running product: a number that is multiplied, not added, each time
round.

```question
id: doing-it-pi-1
type: multiple-choice
correct: 2

A running total starts at 0. What should a running product start at?

- 0
- 1
- The first value in the list
```

It starts at 1. Adding 0 changes nothing, so a total starts at 0.
Multiplying by 1 changes nothing, so a product starts at 1. If it
started at 0, every multiplication would give 0 again. Each move has
its own starting number that changes nothing.

Before you run the cell, guess: did prices rise by more or less than
$2 + 8 + 6 + 2 = 18$%?

```python exec
id: doing-it-pi-2
rises = [1.02, 1.08, 1.06, 1.02]

grown = 1
for rise in rises:
    grown = grown * rise
print(round(grown, 4))
print(round(3.20 * grown, 2))
```

The four rises multiply to 1.191, a rise of about 19.1%, and the
coffee now costs €3.81. That is more than 18%, because each rise
applies to a price that has already risen. Adding the percentages is
not a foolish move: for small rises it comes close. But rises multiply,
and multiplying is the space they live in.

Maths writes a product of many values with a Greek capital P, called pi:

$$\prod_{i=1}^{4} r_i = r_1 \times r_2 \times r_3 \times r_4$$

where $r_i$ is the rise in year $i$. This is *pi notation*: the same as
sigma, with multiplying in place of adding. (It is the same Greek letter
as the $\pi$ in circles, written large. The two have nothing else to do
with each other.) You have met one product already. A power, like
$2^{10}$ on
[Numbers a computer can hold](tutorial:numbers-a-computer-can-hold#powers-and-how-many-times),
is $\prod_{i=1}^{10} 2$: ten 2s, multiplied.

## Until something is true: while

Back to the savings jar. On which day does it first hold €100, which is
10,000 cents? This time we do not know how many times to go round. We
know when to stop.

A *while loop* runs its body again and again, for as long as a
condition is True. Before each round, it checks the condition. As soon
as the condition is False, the loop ends.

Guess the day before you run it.

```python exec
id: doing-it-while-1
jar = 0
day = 0
while jar < 10000:
    day = day + 1
    jar = jar + day
print("On day", day, "the jar holds", jar, "cents.")
```

On day 141 the jar passes €100, with 10,011 cents. Here is what happens
when, for the first few rounds:

| Round | `jar < 10000`? | `day` | `jar` |
|---|---|---|---|
| before | | 0 | 0 |
| 1 | True | 1 | 1 |
| 2 | True | 2 | 3 |
| 3 | True | 3 | 6 |
| … | … | … | … |
| 141 | True | 141 | 10011 |
| (check) | False: stop | | |

The two lines inside have an order, and the order matters. Swap them,
and on day 1 the jar gets 0 cents, the old value of `day`.

On Recipes are algorithms we asked of every repeat: what makes it end?
A while loop ends only when its condition becomes False. This one does,
because `jar` grows every round. Here is one that never would:

```python
jar = 0
while jar < 10000:
    jar = jar - 1    # the jar only gets emptier
```

The jar goes 0, −1, −2, and so on for ever, always less than 10,000.
If a loop like this ever runs in a cell, the cell's **Run** button turns
into **Stop** while it runs. Press it, and Python stops.

So which loop do you reach for?

| Use | When you know | Example |
|---|---|---|
| `for` | the values, or how many times | every day of a year |
| `while` | when to stop, but not how many times | until the jar holds €100 |

### Your turn

A coffee costs €3.20 today, and its price rises by 2% every year.

1. Before you write anything, guess how many years until it costs more
   than €5.
2. Change the cell below so that it counts the years. Each round, the
   price is multiplied by 1.02 and `years` goes up by 1.
3. What is the condition for going round again?

```python exec
id: doing-it-while-your-turn
coffee = 3.20
years = 0
# Your while loop here
print(years, "years, and the coffee costs", round(coffee, 2))
```

## Two tools for your toolkit

We have added up lists and multiplied them together several times now.
Let's make each one a tool, so that later pages can use them in one
line.

The first, `total`, has one gap. The line inside the loop adds `0`
where it should add each value. Change that `0`. The second, `product`,
is a stub: only its promise is written. Write its body yourself, in the
same shape as `total`. Remember where a product starts.

```python exec
id: doing-it-toolkit
toolkit: yes
def total(values):
    """Add up every number in values, and return the sum.

    values can be a list, or a range. total([3.20, 0, 3.50]) is 6.7.
    With no values at all, the sum is 0.
    """
    running = 0
    for value in values:
        running = running + 0    # change this 0 so the line adds each value
    return running


def product(values):
    """Multiply every number in values together, and return the result.

    values can be a list, or a range. product([2, 3, 4]) is 24.
    With no values at all, the product is 1.
    """
    ...
```

```python toolkit-reference
for: doing-it-toolkit
def total(values):
    """Add up every number in values, and return the sum.

    values can be a list, or a range. total([3.20, 0, 3.50]) is 6.7.
    With no values at all, the sum is 0.
    """
    running = 0
    for value in values:
        running = running + value
    return running


def product(values):
    """Multiply every number in values together, and return the result.

    values can be a list, or a range. product([2, 3, 4]) is 24.
    With no values at all, the product is 1.
    """
    running = 1
    for value in values:
        running = running * value
    return running
```

Run the toolkit cell, then run the tests. Until both tools are written,
expect the first test to stop with an `AssertionError`. That is the test
telling you which promise is not kept yet.

```python exec
id: doing-it-toolkit-tests
assert total([3.20, 0, 3.50]) == 6.7
assert total(range(1, 366)) == 66795          # the savings jar
assert total([]) == 0
assert product([2, 3, 4]) == 24
assert round(product([1.02, 1.08, 1.06, 1.02]), 4) == 1.191
assert product([]) == 1                       # nothing multiplied changes nothing
print("total and product keep their promises.")
```

```hint
Which test does the error point at? Print `total([3.20, 0, 3.50])` or
`product([2, 3, 4])` on its own, and compare it with what the test
expects.
```

```hint
after: 12 errors
title: some steps
1. In `total`, the loop points `value` at each number in turn. The line
   inside should add `value`, not `0`.
2. `product` has the same shape as `total`: a starting number, a loop,
   and a `return` after the loop.
3. A product starts at 1, and multiplies with `*`.

**Think about:** why must `return running` sit outside the loop, and
not inside it?
```

Python has both tools already: `sum()`, and `math.prod()` in the
`math` module. Writing our own shows what they do inside.

One thing about names. `total` is now the name of a function. If a cell
on a later page says `total = 0`, the name `total` points at 0 instead,
and the tool is gone from that page. That is why the loops on this page
used names like `spent`, `jar` and `grown` for the numbers they built
up.

<details class="dl-why"><summary>Why this way?</summary>

This page had you write `total` and `product` yourself. Python already
has `sum()`, and `math.prod()` in its `math` module, and they do the same
jobs.

Using Python's own tools is what most programmers do, for good reasons:
they are tested, they are fast, and every Python reader knows them. A
course could show `sum()` and move on.

We wrote our own because a running total is the idea this page teaches,
and `sum()` hides it. Writing `total` shows what happens inside: a
starting value, a loop, and one line that runs again and again. It also
shows why a product starts at 1. Once you have written one, `sum()` is
not a mystery, and you can choose either.

</details>

## Four questions, looking back

| The question | On this page |
|---|---|
| What is named here? | a list of prices, `week`; a loop variable, `price`, that points at each value in turn; running totals like `spent` and `jar`; the index $i$ in $x_i$ |
| What is promised? | a `for` loop promises one round for each value; `total` and `product` promise the sum and the product of any list; the Gauss formula promises the same answer as the loop |
| What happens when? | the loop body runs again and again; a running total starts before the loop and grows inside it; a `while` loop checks its condition before every round |
| What does this space let us do? | Python repeats without getting tired; a total starts at 0 and a product at 1; rises multiply, they do not add |

## What we have now

| Term or tool | What it means |
|---|---|
| list | a row of values in square brackets, kept in order (Unit 5 has much more) |
| `for x in values:` | a loop: run the pushed-in lines once for each value |
| loop body, loop variable | the pushed-in lines; the name that points at each value in turn |
| running total | a name that holds the total so far: start at 0, add each time round |
| `+=` | `spent += price` is short for `spent = spent + price` |
| `range(start, stop)` | the whole numbers from `start` up to `stop`, with `stop` left out |
| storage, selection, iteration | names, `if` and loops: the shapes of structured design |
| index, $x_i$ | the small number that says which value we mean |
| $\sum_{i=1}^{n} x_i$ | sigma: add up $x_i$ for every $i$ from 1 to $n$ |
| $\prod_{i=1}^{n} x_i$ | pi: multiply $x_i$ together for every $i$ from 1 to $n$ |
| $\sum_{i=1}^{n} i = \frac{n(n+1)}{2}$ | the sum of 1 to $n$, found by pairing the ends |
| `sum()` | Python's own way to add up a row of values |
| `while condition:` | a loop that runs for as long as the condition is True |
| `total(values)`, `product(values)` | your two new toolkit tools |

The practice page is next. After it,
[Counting every outfit](tutorial:counting-every-outfit) puts one loop
inside another, and uses them to count.

For more on loops, the integrated course has
[Repeating steps with loops](tutorial:repeating-yourself).
