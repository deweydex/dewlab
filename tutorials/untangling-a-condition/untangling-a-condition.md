---
title: "Untangling a condition: De Morgan's laws"
year: "2026-2027"
version: 2026.09.25.1
covers:
  two-ways-to-grey-out-a-button:
    touches: [MIT-2.4]
  a-move-from-arithmetic:
    covers: [MIT-2.5]
  checking-every-row-with-one-function:
    touches: [MIT-2.4]
  de-morgans-laws:
    covers: [MIT-2.5]
  not-between:
    covers: [MIT-2.5]
    touches: [MIT-1.11]
  untangling-a-real-condition:
    covers: [MIT-2.5]
    touches: [PDP-LO4]
---

# Untangling a condition: De Morgan's laws

Sooner or later, you will open someone's program and find a line like
`not (not (a and not b) and c)`. Most people's eyes slide right off it.
If that happens to you, it is not a sign that logic is not for you. It is
a sign that the line was written badly, and this page is about how to
write it well.

Let's start small. A food-delivery app has an **Order** button. The
button is greyed out when the restaurant cannot take an order. One
programmer writes the test as `not (is_open and has_stock)`. Another
writes `not is_open or not has_stock`.

Do the two tests always agree? And why would `not (a and b)` mean the same
as `not a or not b`?

On this page we:

- compare two conditions row by row, with the truth tables from the last page
- write `same_rule`, a function that checks every row for us, and add it to
  the toolkit
- find the two laws that let us move a `not` inside brackets
- use them to untangle a hard condition from a real program, one checked
  step at a time

> **The space we're in.** Every input on this page is `True` or `False`,
> and nothing else. There are no "maybe" values and no numbers in between.
> The moves allowed are `not`, `and` and `or`. Python also gives us
> `between` and `truth_table` from earlier pages, because they are in your
> toolkit.

## Warm-up

```question
id: untangling-warm-up-1
type: multiple-choice
answer: 1

From [Choosing a path](tutorial:choosing-a-path): which condition is True
for exactly the temperatures that are *not* "80 and over"?

- `temperature < 80`
  - Everything below 80; 80 itself is "80 and over".
- `temperature <= 80`
  - This includes 80, which is "80 and over".
- `temperature > 80`
  - These are the temperatures over 80, not under.
- `temperature != 80`
  - This is True for 85, which is "80 and over".
```

```question
id: untangling-warm-up-2
type: fill-in-the-blank

From [True, false and every case](tutorial:true-false-and-every-case): a
rule with three True/False inputs has a truth table with {8} rows.
```

## Two ways to grey out a button

Let's give each programmer's test a name. Each one is a small function: two
True/False values go in, and one True/False value comes out. The result is
`True` when the button should be greyed out.

```python
def grey_out_a(is_open, has_stock):
    return not (is_open and has_stock)

def grey_out_b(is_open, has_stock):
    return not is_open or not has_stock
```

Before we run anything, think about the restaurant itself. It can take
an order only when it is open and it has stock.

```question
id: untangling-grey-out-rows
type: multiple-choice
answer: 3

There are four possible rows: open or closed, with stock or without. In how
many of the four rows should the button be greyed out?

- 1
  - One row leaves the button available: open and with stock.
- 2
  - Either reason, closed or no stock, is enough on its own to grey the button out.
- 3
  - The button works only when open and with stock; the other three rows grey it out.
- 4
  - The row that is open and with stock leaves the button available.
```

Now let's print both truth tables with `truth_table` from your toolkit. It
also gives back each result column, so the last line can compare the two
columns, the way we compared two rules on the last page. Run it to check
your answer.

```python exec
id: untangling-two-tests
def grey_out_a(is_open, has_stock):
    return not (is_open and has_stock)

def grey_out_b(is_open, has_stock):
    return not is_open or not has_stock

column_a = truth_table(grey_out_a, ["is_open", "has_stock"])
column_b = truth_table(grey_out_b, ["is_open", "has_stock"])
print(column_a == column_b)
```

The two tables match, row for row, and the last line says `True`. Each one is `True` in three rows. The
button is available in one row only, where the restaurant is open *and* has stock.
Every other row greys it out.

There is one detail in `grey_out_b` that is worth reading slowly. The last
page showed that brackets decide what happens first. But `grey_out_b` has no
brackets, so how does Python know what to do first? Python has an order for
these words, the same way arithmetic does multiplication before addition:
`not` first, then `and`, then `or`. So `not is_open or not has_stock` means
`(not is_open) or (not has_stock)`. In `grey_out_a`, the brackets change the
order: Python works out `is_open and has_stock` first, and then `not` flips
the result.

## A move from arithmetic

In arithmetic, a minus sign in front of brackets goes onto each number
inside, and the plus stays a plus:

$$-(3 + 5) = -3 + (-5)$$

Both sides are $-8$. It is natural to try the same move with `not`: put it
on each part, and keep the joining word. That gives a third version.

```python
def grey_out_c(is_open, has_stock):
    return not is_open and not has_stock
```

Is `grey_out_c` the same rule as the other two? Make a guess before you run
the cell.

```python exec
id: untangling-arithmetic-move
def grey_out_c(is_open, has_stock):
    return not is_open and not has_stock

column_c = truth_table(grey_out_c, ["is_open", "has_stock"])
print(column_c == column_a)
```

This table is different, and the last line says `False`. It is `True` in one row only: closed *and* out of
stock. So a restaurant that is closed but has stock would show a working
Order button, and so would one that is open with nothing to sell.

If you guessed "the same", many people do. I think it is the most
natural guess in the whole unit, and the move has a reason behind it.
It works in arithmetic, the space of numbers,
where a minus sign goes onto each part and the plus stays. In the space of
True and False, `not` does a second job as well: it changes the joining
word. When `not` goes onto each part, `and` turns into `or`. That second
job is the whole secret of this page, and we will see it again.

## Checking every row with one function

Comparing result columns works well, but `truth_table` prints every row on
the way, and it stops at three inputs. A rule with ten inputs has 1,024 rows.
Let's write a function that compares two rules quietly, for any number of
inputs.

Two rules are *equivalent* when they give the same answer on every row of
their truth table. A function that tests this needs every row, so let's
start there. Python has a module called `itertools` that comes with it, and
one of its tools, `product`, makes every row of True/False values.

How many rows do you expect for `repeat=2`? And for `repeat=3`? Run it to
check, then change the 2 to a 3 and run it again.

```python exec
id: untangling-every-row
from itertools import product

for row in product([False, True], repeat=2):
    print(row)
```

The first line is an *import*: it brings `product` into our page's space,
because Python does not give it to us without asking. Then `product` makes
every row, and the loop does something for each one. Each row is a few
values in round brackets. Python calls that a *tuple*.

We need to hand a row to a rule. The rule wants two separate inputs, but a
row is one tuple. A star in front of the row, `*row`, spreads its values out,
one for each input:

```python exec
id: untangling-star-row
row = (True, False)
print(grey_out_a(*row))           # the same as the next line
print(grey_out_a(True, False))
```

Now we can write the function. Here is its promise. `same_rule(rule_a,
rule_b, count)` gives `True` when the two rules agree on every row of `count`
True/False inputs. It gives `False` if even one row is different.

This cell is a toolkit cell. What you keep in it goes into your toolkit, and
later pages can use it.

```python exec
id: untangling-toolkit
toolkit: yes
from itertools import product

def same_rule(rule_a, rule_b, count):
    """Return True when rule_a and rule_b give the same answer on every row
    of count True/False inputs. Return False as soon as one row differs."""
    for row in product([False, True], repeat=count):
        if rule_a(*row) != rule_b(*row):
            return False
    return True
```

Look at the order of the two `return` lines. The function can say "different"
the moment it finds one row that disagrees, and it stops there. It can only
say "the same" after the loop has checked every row. That is why
`return True` sits outside the loop, after it.

Every toolkit function gets tests. An `assert` line checks that something is
`True`. If it is, nothing happens. If it is not, Python stops with an
`AssertionError`. What do you expect this cell to print?

```python exec
id: untangling-toolkit-tests
assert same_rule(grey_out_a, grey_out_b, 2)
assert not same_rule(grey_out_a, grey_out_c, 2)
print("Both tests passed.")
```

### Your turn

1. In the cell below, write a rule `both(a, b)` that returns `a and b`.
2. Write a second rule `both_other_way(a, b)` that returns `b and a`.
3. Add `assert same_rule(both, both_other_way, 2)` and run the cell. Did it
   pass?
4. Add one more `assert` that you expect to fail, such as
   `assert same_rule(both, grey_out_a, 2)`. Run it, and read the last line of
   the error. The error here is the test doing its job.

```python exec
id: untangling-your-tests
# Your two rules and your asserts
```

```hint
Which line does the error point at? Is that the assert you expected to fail,
or a different one?
```

## De Morgan's laws

We have found one law. Here is a second situation, to find the other.

A small drone should stay on the ground if it is raining or if the wind
is strong. Most small drones are not waterproof, and a strong wind can
push them further than their motors can fight.

```python
def stay_grounded(is_raining, is_windy):
    return is_raining or is_windy
```

The drone can fly when `not (is_raining or is_windy)`. How would you write
that without the brackets? Here are two guesses. Which one do you think is
the same rule? Run the cell to check.

```python exec
id: untangling-second-law
def can_fly(is_raining, is_windy):
    return not (is_raining or is_windy)

def guess_1(is_raining, is_windy):
    return not is_raining or not is_windy

def guess_2(is_raining, is_windy):
    return not is_raining and not is_windy

print("guess_1:", same_rule(can_fly, guess_1, 2))
print("guess_2:", same_rule(can_fly, guess_2, 2))
```

It is `guess_2`. The drone can fly when it is not raining *and* it is not
windy. The same thing happened as before: `not` went onto each part, and the
joining word changed, this time from `or` to `and`.

These two facts are called *De Morgan's laws*, after Augustus De Morgan, a
mathematician who wrote them in the language of algebra in the 1840s. Here
they are in words first:

- "Not both" means the same as "at least one is not".
- "Not either" means the same as "neither".

In the symbols from
[True, false and every case](tutorial:true-false-and-every-case), $\lnot$ is
not, $\land$ is and, and $\lor$ is or:

$$\lnot(A \land B) = \lnot A \lor \lnot B$$

$$\lnot(A \lor B) = \lnot A \land \lnot B$$

As a recipe, it is two steps. First, put a `not` on each part. Then swap
the joining word: `and` becomes `or`, and `or` becomes `and`.

The two laws are two promises, and `same_rule` is how we check a promise.
We have checked both on every row, so the laws hold for every possible pair
of inputs. A proof by checking every case is still a proof.

<aside class="dl-note" id="untangling-note-de-morgan">

**Augustus De Morgan** was born in India in 1806, and taught mathematics
in London. He was Ada Lovelace's maths tutor; we meet her in Unit 10. His
book *Formal Logic* came out in 1847, the same year as George Boole's
first book on logic. The laws are older than their name: logicians in
the Middle Ages, such as William of Ockham, stated them in words.

</aside>

### Your turn

1. Does the first law still hold with three parts? Write `not_all_three(a,
   b, c)` that returns `not (a and b and c)`.
2. Write `law_version(a, b, c)` using the recipe: a `not` on each part, and
   `or` in place of `and`.
3. Check them with `same_rule`. What should `count` be this time?
4. If you have time, do the same for `not (a or b or c)`.

```python exec
id: untangling-three-parts
# Your two rules for three inputs, and a same_rule check
```

```hint
How many inputs does each rule take? That number is the count, and it also
tells you how many rows `same_rule` will check.
```

## Not between

The laws are also hiding inside a function you already have. On
[Choosing a path](tutorial:choosing-a-path) we wrote `between(value, low,
high)`, which is true when `low <= value <= high`. Python reads that line
as two comparisons joined by `and`:

$$\text{low} \le \text{value} \;\text{ and }\; \text{value} \le \text{high}$$

That page met a real range: an iPhone is designed to work from 0 °C to
35 °C. Say a phone warns its owner outside that range. So "warn" is
`not between(temperature, 0, 35)`. Let's use the first law on it, one
step at a time:

1. Put a `not` on each part and swap `and` for `or`:
   `not (0 <= temperature) or not (temperature <= 35)`.
2. The warm-up showed that "not 80 and over" is `temperature < 80`. In the
   same way, a `not` in front of a comparison turns it round, and the end
   point changes sides: `not (0 <= temperature)` is `temperature < 0`, and
   `not (temperature <= 35)` is `temperature > 35`.
3. So "warn" is `temperature < 0 or temperature > 35`.

That matches the number line: the safe temperatures sit in one piece in
the middle, and "warn" is everything to the left of it *or* everything to
the right.

The inputs here are numbers, so `same_rule` cannot check it. A loop can.
`range(-20, 61)` gives the whole numbers from $-20$ up to 60 (the last
number, 61, is left out). Will this cell print any lines that say
"disagree"? Run it to check.

```python exec
id: untangling-not-between
for temperature in range(-20, 61):
    if (not between(temperature, 0, 35)) != (temperature < 0 or temperature > 35):
        print("They disagree at", temperature)
print("Checked every whole degree from -20 to 60.")
```

It prints no disagreements. The loop checked 81 temperatures, more than a
phone will meet. The law says more than the loop can: it holds for 35.5,
for $-100$ and for a million as well, because it only depends on each
comparison being True or False.

## Untangling a real condition

Here is a line of the kind people really find in programs. A swimming pool's
booking system refuses a booking with this rule:

```python
def refuse_booking(is_under_12, with_adult, has_paid):
    return not (not (is_under_12 and not with_adult) and has_paid)
```

Can you say, in one sentence, when a booking is refused? Pause and try
before you read on. Most people cannot, at first, and that is the point
of this section. Let's untangle it, one law at a time, and check each step with
`same_rule` before we take the next. Order matters here, so we work from the
outside in.

**Step 1.** The outer `not` sits in front of `(something and has_paid)`. The
first law puts a `not` on each part and changes `and` to `or`:

```python exec
id: untangling-booking-step-1
def refuse_booking(is_under_12, with_adult, has_paid):
    return not (not (is_under_12 and not with_adult) and has_paid)

def step_1(is_under_12, with_adult, has_paid):
    return not not (is_under_12 and not with_adult) or not has_paid

print(same_rule(refuse_booking, step_1, 3))
```

**Step 2.** Now there is a `not not` at the front. Two nots cancel: flipping
True to False and then back again gives True. This is called *double
negation*. What do you expect `same_rule` to say this time?

```python exec
id: untangling-booking-step-2
def step_2(is_under_12, with_adult, has_paid):
    return (is_under_12 and not with_adult) or not has_paid

print(same_rule(refuse_booking, step_2, 3))
```

Both steps print `True`, so `step_2` is the same rule as the tangled one, on
all eight rows. And now it can be read aloud: a booking is refused if a child
under 12 comes without an adult, or if the booking has not been paid.

That is a strange and pleasing result: a line nobody could read turned
into a sentence anybody can, and a computer checked every step. That is
what untangling is for. The program does exactly what it did before.
What changed is how quickly a person can read it, and check it. A condition
that people can read is a condition that people can fix.

### Your turn

A music app decides when a listener may skip a song with this rule:

```python
def can_skip(liked, played_today, is_advert):
    return not (liked and not played_today) and not is_advert
```

1. Copy `can_skip` into the cell below.
2. Use the first law on `not (liked and not played_today)`, and write the
   result as a new function, `can_skip_step_1`.
3. Check it with `same_rule`. What should `count` be?
4. Remove any `not not` you find, and check again.
5. Say the rule aloud in one sentence. Who can skip, and when?

```python exec
id: untangling-your-condition
# Copy can_skip here, then untangle it one checked step at a time
```

```hint
In step 2, the two parts are `liked` and `not played_today`. What do you get
when you put a `not` in front of each of them?
```

```hint
after: 12 errors
title: some steps
1. The first law turns `not (A and B)` into `not A or not B`.
2. Here A is `liked` and B is `not played_today`.
3. So `not B` is `not not played_today`, which double negation turns into
   `played_today`.
4. The `and not is_advert` at the end is outside the brackets, so it stays
   as it is. You may want brackets around the `or` part, so that `and` does
   not go first.

**Think about:** what does Python do first, `and` or `or`?
```

<details class="dl-why"><summary>Why this way?</summary>

This page proved De Morgan's laws by checking every row with
`same_rule`. A maths book usually proves them another way: with Venn
diagrams, or with the rules of Boolean algebra, each line following from
the one before.

Those proofs are worth knowing. They show why the laws hold, and an
algebra proof still works when a rule has too many inputs to check row
by row.

We checked every row because it is a proof you can run, read and trust
without taking anyone's word for it. A promise that has been checked is
stronger than a promise that is believed. Checking also shows its own
limit: every extra input doubles the rows. The practice page asks where
that limit starts to matter.

</details>

## Four questions, looking back

| Question | On this page |
|---|---|
| What is named here? | Each condition got a function name, like `grey_out_a`, so we could hand the whole rule to another function. The two laws got a name too: De Morgan's laws. |
| What is promised? | `same_rule` promises `True` only when two rules agree on every row. Each law is a promise that two ways of writing a rule are equivalent. |
| What happens when? | `not` goes first, then `and`, then `or`, unless brackets say otherwise. We untangled from the outside in, one checked step at a time. |
| What does this space let us do? | In the space of True and False, `not` on each part swaps `and` with `or`. In arithmetic, a minus sign on each part leaves the plus alone. The same-looking move belongs to a different space. |

## What we have now

| Term or tool | What it means |
|---|---|
| equivalent rules | Two rules that give the same answer on every row of their truth table |
| De Morgan's first law | `not (a and b)` is the same as `not a or not b` |
| De Morgan's second law | `not (a or b)` is the same as `not a and not b` |
| double negation | `not not a` is the same as `a` |
| order of `not`, `and`, `or` | `not` first, then `and`, then `or`; brackets change the order |
| `product([False, True], repeat=n)` | Every row of `n` True/False values |
| `*row` | Spreads a tuple's values out, one for each input |
| `same_rule(rule_a, rule_b, count)` | Your toolkit function: `True` when two rules agree on every row |

For more on the same ideas, there is a longer page on the programming and
maths course: [Logic: truth tables, XOR and De Morgan's
laws](tutorial:logic-and-truth).
