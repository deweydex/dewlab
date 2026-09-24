---
title: "Choosing a path: if, elif and else"
year: "2026-2027"
version: 2026.09.24.1
covers:
  pictures-on-a-number-line:
    touches: [MIT-1.11]
  asking-python-a-question:
    covers: [PDP-LO4]
  solving-an-inequality:
    covers: [MIT-1.11]
  a-move-that-turns-the-sign-round:
    covers: [MIT-1.11]
  two-paths-if-and-else:
    covers: [PDP-LO6]
    touches: [PDP-LO4]
  more-than-two-paths-elif:
    covers: [PDP-LO6]
  a-tool-of-your-own-between:
    touches: [MIT-1.11, PDP-LO6]
---

# Choosing a path: if, elif and else

A ticket machine at a train station asks you two things: how old you
are, and whether you have a student card. A moment later it shows a
price. Nobody is inside the machine. So how does it know you get the
student price?

On this page we:

- draw "under 5" and "18 and over" as pictures on a number line
- ask Python questions that have the answer True or False
- solve an inequality: for how many journeys is a weekly pass cheaper?
- let a program choose a path with `if`, `elif` and `else`
- add our first decision tool to the toolkit: `between`

> **The space we're in.** We use the whole numbers and decimals from
> Unit 1, and Python's own ways of comparing them. Every question on this
> page has exactly two answers, True or False: there is no "maybe" here.
> Lines still run from top to bottom, but now some lines can be skipped.
> One thing a fare table never says out loud: it assumes every age is a
> whole number of years.

## Warm-up

Two questions from Unit 1. The first is from
[Numbers a computer can hold](tutorial:numbers-a-computer-can-hold), and
the second from
[When Python says no: reading error messages](tutorial:when-python-says-no).

```question
id: choosing-warm-up-1
type: multiple-choice
correct: 2

What does Python give for `7 // 2`?

- `3.5`
- `3`
- `4`
- `1`
```

```question
id: choosing-warm-up-2
type: multiple-choice
correct: 2

The last line of an error says `NameError: name 'totl' is not defined`.
What is the most likely cause?

- The number in `totl` is too big for Python to hold.
- The name was typed differently here from where it was made.
- Python cannot add the numbers in this cell.
- The cell has to be run a second time.
```

## Pictures on a number line

Here is the fare table on the machine's screen. The prices are made up,
but the shape is the same as on many real machines.

| Who | Fare for one journey |
|---|---|
| Under 5 | free |
| 5 to 17 | €1.00 |
| 18 and over, with a student card | €1.50 |
| 18 and over | €2.60 |

Let's draw the first and last rows. Picture a line of ages, from 0 on the
left to 30 on the right.

"Under 5" is every age to the left of 5. Is a person who is exactly 5
"under 5"? No. So on the picture, 5 gets an empty circle, which means
"up to here, but not this point". A thick line runs from the circle to
the left.

"18 and over" starts at 18 and runs to the right for ever. This time 18
is included, so it gets a filled circle.

An *inequality* is a statement that one amount is bigger or smaller than
another. Maths has four symbols for it:

| In words | Symbol | Example |
|---|---|---|
| less than | $<$ | $age < 5$ |
| less than or equal to | $\le$ | $age \le 17$ |
| greater than | $>$ | $age > 17$ |
| greater than or equal to | $\ge$ | $age \ge 18$ |

The small end of the symbol points at the smaller amount. An empty
circle on the number line goes with $<$ and $>$. A filled circle goes
with $\le$ and $\ge$.

```question
id: choosing-number-line-1
type: multiple-choice
correct: 2

Which of these is true for a person who is exactly 18?

- $age < 18$
- $age \ge 18$
- $age > 18$
```

Notice that $age > 17$ and $age \ge 18$ draw the same picture, as long
as ages are whole numbers. If ages could be 17.5, they would not. That is
the space we are in deciding the answer.

## Asking Python a question

Python writes $\le$ as `<=` and $\ge$ as `>=`, because a keyboard has no
key for either. What do you think each line below will print? Make a
guess for all three, then run it to check.

```python exec
id: choosing-asking-1
age = 17
print(age < 5)
print(age >= 18)
print(age <= 17)
```

Python answers each question with `True` or `False`. A *condition* is a
question with exactly two possible answers, True or False. `True` and
`False` are values in Python, the same way `17` is a value. They are
written with a capital letter.

Asking whether two things are equal needs two equals signs. One equals
sign already has a job: it names a value. So `age = 18` means "let `age`
stand for 18", and `age == 18` asks "is `age` 18?". The sign `!=` asks
"is it different?".

```python exec
id: choosing-asking-2
age = 18
print(age == 18)
print(age != 18)

is_adult = age >= 18
print(is_adult)
```

The last two lines show something useful. A condition's answer is a
value, so we can give it a name, like any other value.

### Your turn

1. In the first cell above, change `age = 17` to `age = 4`. Before you
   run it, guess the three answers.
2. In the cell below, set `age` to your own age, or any age you like.
3. Write a line that prints True when `age` is 66 or more.

```python exec
id: choosing-your-turn-1
# Your age, and a question about it
```

## Solving an inequality

Many travellers have a choice. They can pay €2.00 for each single
journey, or buy a weekly pass for €25.00. For how many journeys in a week
is the pass the cheaper choice?

Let's say it in words first. The pass is cheaper when the singles would
cost more than €25.

Now in symbols. Maths likes a short letter here, so let $j$ stand for the
number of journeys. The singles cost $2j$ euro, and we want

$$2j > 25$$

We solve an inequality with the same moves as an equation. We can add or
subtract the same amount on both sides. We can multiply or divide both
sides by the same positive number. Dividing both sides by 2 gives

$$j > 12.5$$

What does $j > 12.5$ mean for a real week? Journeys are whole numbers:
nobody takes half a bus. So the pass is cheaper for 13 journeys or more.

Before you run the cell, which line do you expect to say True? Run it to
check.

```python exec
id: choosing-solving-1
single_fare = 2.00
weekly_pass = 25.00

journeys = 12
print(journeys, "journeys:", single_fare * journeys, "euro. Pass cheaper?", single_fare * journeys > weekly_pass)

journeys = 13
print(journeys, "journeys:", single_fare * journeys, "euro. Pass cheaper?", single_fare * journeys > weekly_pass)
```

At 12 journeys the singles cost €24, so the pass is not cheaper yet. At
13 they cost €26, and the pass wins. The algebra and the code agree.

We checked two values by writing the same line twice. In Unit 3 we will
meet a way to check every value from 1 to 20 with a few lines.

### Your turn

A gym charges €6 for each visit, or €40 for a month. For how many visits
is the monthly price cheaper?

1. Write the inequality in words, then with a letter.
2. Solve it on paper.
3. Check your answer in the cell below, with one visit fewer and one
   visit more than your answer.

```python exec
id: choosing-your-turn-2
# Check your gym answer here
```

## A move that turns the sign round

A phone battery is at 80%, and a video call uses 5% of it each hour. For
how many hours $h$ does the battery stay above 20%?

In symbols: $80 - 5h > 20$.

Subtract 80 from both sides: $-5h > -60$.

Now divide both sides by $-5$. It looks like the answer is $h > 12$. But
look at 13 hours: $80 - 5 \times 13 = 15$, and 15 is not above 20.
Something went wrong. Before you run the next cell, can you guess which
of these three lines print True?

```python exec
id: choosing-sign-1
print(3 < 5)
print(-3 < -5)
print(-3 > -5)
```

Three is less than five. But $-3$ is greater than $-5$. It is closer to
zero, so it sits further to the right on the number line. Multiplying or
dividing by a negative number turns the whole number line round, so the
order of any two numbers turns round too.

So in the space of inequalities, dividing by a negative number is
allowed, with one extra rule: the sign turns round. $-5h > -60$ becomes

$$h < 12$$

Let's check that on both sides of 12.

```python exec
id: choosing-sign-2
battery_now = 80
use_per_hour = 5

hours = 11
print(hours, "hours:", battery_now - use_per_hour * hours > 20)
hours = 12
print(hours, "hours:", battery_now - use_per_hour * hours > 20)
hours = 13
print(hours, "hours:", battery_now - use_per_hour * hours > 20)
```

After 12 hours the battery is at exactly 20%, and 20 is not above 20.
So the battery stays above 20% for any time less than 12 hours.

There is another way that never divides by a negative. Add $5h$ to both
sides of $80 - 5h > 20$ to get $80 > 20 + 5h$. Subtract 20: $60 > 5h$.
Divide by 5: $12 > h$. That is the same answer, read from the other side.

## Two paths: if and else

Back to the ticket machine. Here is a machine that knows two fares.
Guess what it prints for `age = 20`. Then run it to check.

```python exec
id: choosing-if-else-1
age = 20

if age >= 18:
    print("Adult fare: €2.60")
else:
    print("Child fare: €1.00")

print("Have a good journey.")
```

Now change `age` to 12 and run it again.

The word `if` starts a question. After it comes a condition, then a
colon. The lines pushed in under it run only when the condition is True.
Under `else` are the lines that run when it is False. Each of these
groups of pushed-in lines is a *branch*, and the program takes exactly
one of them. The last line is not pushed in, so it runs every time.

The spaces at the start of a line are how Python knows which lines
belong to a branch. On
[When Python says no](tutorial:when-python-says-no) we met the
`IndentationError`: now we can see why Python cares so much about those
spaces.

On [Recipes are algorithms](tutorial:recipes-are-algorithms), a robot
making tea chose a path with "if they take milk, add milk". That shape
was called selection. Here is the same shape, with Python doing the
choosing.

A condition does not have to be a comparison. Any True or False value
will do, including one we named:

```python exec
id: choosing-if-else-2
has_student_card = True

if has_student_card:
    print("Student fare: €1.50")
else:
    print("Adult fare: €2.60")
```

## More than two paths: elif

The real table has four rows, so the machine needs four paths. The word
`elif` is short for "else if". It adds another condition. Python checks
the conditions from the top, one after another. It takes the first path
whose condition is True, and skips every path after it.

Here is the whole table as a function, which gives back a fare.

```python exec
id: choosing-elif-1
def fare_for(age, has_student_card):
    """Return the fare in euro for one journey."""
    if age < 5:
        return 0.00
    elif age < 18:
        return 1.00
    elif has_student_card:
        return 1.50
    else:
        return 2.60

print(fare_for(3, False))
print(fare_for(12, False))
print(fare_for(19, True))
print(fare_for(40, False))
```

Look at the second condition, `age < 18`. The table says "5 to 17", but
the code never checks that the age is 5 or more. It does not need to. We
only reach that line when `age < 5` was False. The order of the checks
carries information. What happens when is part of the meaning.

```question
id: choosing-elif-2
type: multiple-choice
correct: 1

A 16-year-old has a student card. What does `fare_for(16, True)` give?

- `1.0`, because `age < 18` is checked before the student card
- `1.5`, because they have a student card
- `2.6`, because no condition fits
```

Now let's put the same checks in a different order. This cell has a
mistake in it on purpose. Before you run it, what do you think a
3-year-old will pay?

```python exec
id: choosing-elif-3
def fare_in_wrong_order(age, has_student_card):
    """The same four fares, checked in a different order."""
    if age < 18:
        return 1.00
    elif age < 5:
        return 0.00
    elif has_student_card:
        return 1.50
    else:
        return 2.60

print(fare_in_wrong_order(3, False))
```

The 3-year-old pays €1.00. Python did exactly what it was told. Every
age under 5 is also under 18, so the first condition catches it, and
the line `elif age < 5` can never be reached. Nothing crashed, and no
error message appeared. This kind of mistake only shows up when we test
the program with the right ages.

### Your turn

In Ireland, people aged 66 and over can travel free on most public
transport.

1. Copy `fare_for` into the cell below.
2. Add a branch so that anyone 66 or over pays 0.00. Think about where
   in the order it has to go.
3. Test it: `print(fare_for(70, True))` should print `0.0`, and
   `print(fare_for(19, True))` should still print `1.5`.

```python exec
id: choosing-your-turn-3
# Your fare_for, with free travel at 66 and over
```

## A tool of your own: between

Many everyday questions have the shape "is this value between two
others?". Is a child's age from 5 to 17? Is a heart rate during a run
from 120 to 150 beats a minute? Is the oven from 180 to 200 degrees?

Maths writes it as one line with two signs: $120 \le rate \le 150$.
Python lets us write it the same way. What do you expect each line to
print? Run it to check.

```python exec
id: choosing-between-1
heart_rate = 135
print(120 <= heart_rate <= 150)

heart_rate = 150
print(120 <= heart_rate <= 150)

heart_rate = 151
print(120 <= heart_rate <= 150)
```

A value exactly at an end counts, because the signs are `<=`, the
filled circles on the number line.

Now it is your turn to make a tool from this. The cell below is a
toolkit cell, like the one where you finished `to_hex` on
[Everything is ones and zeros](tutorial:everything-is-ones-and-zeros).
What you write here goes into your own toolkit, and later pages can use
it. The first line of the function and its promise are written for you.
Replace the comment with one `return` line that keeps the promise.

```python exec
id: choosing-between-toolkit
toolkit: yes
def between(value, low, high):
    """Return True when low <= value <= high, with both ends included.

    between(135, 120, 150) is True. between(151, 120, 150) is False.
    """
    # Replace this comment with one return line.
```

```python toolkit-reference
for: choosing-between-toolkit
def between(value, low, high):
    """Return True when low <= value <= high, with both ends included.

    between(135, 120, 150) is True. between(151, 120, 150) is False.
    """
    return low <= value <= high
```

Run your cell, then run the tests below. Each `assert` checks one part
of the promise, and stays quiet when it holds. We write `== True` and
`== False` so that a function which gives back nothing at all fails the
test, instead of slipping through. Until your `return` line is written,
expect the first test to stop with an `AssertionError`: the promise is
not kept yet.

```python exec
id: choosing-between-2
assert between(135, 120, 150) == True
assert between(120, 120, 150) == True   # the low end counts
assert between(150, 120, 150) == True   # so does the high end
assert between(119, 120, 150) == False
assert between(151, 120, 150) == False
print("All five tests pass.")
```

Look at which values the tests use. Two are the ends themselves, and two
are one step outside. The ends are where a mistake like `<` in place of
`<=` would hide.

### Your turn

A weather warning for ice goes out when the temperature is from $-2$ to
2 degrees.

1. Set `temperature = 1` in the cell below.
2. Write an `if` and `else` that uses `between` to print either "Risk of
   ice" or "No ice warning".
3. Try `temperature` at $-3$, $-2$ and 2, and check each answer against
   the number line in your head.

```python exec
id: choosing-your-turn-4
# Your ice warning
```

## Four questions, looking back

| Question | On this page |
|---|---|
| What is named here? | Ages, fares and journeys. A condition's answer too: `is_adult = age >= 18`. `=` names, `==` asks. |
| What is promised? | `fare_for` promises a fare for any age. `between` promises True exactly when the value is from `low` to `high`. The asserts check the promise. |
| What happens when? | Conditions are checked from the top. The first True one wins, and the rest are skipped, so the order of the `elif` checks changes the answer. |
| What does this space let us do? | Inequalities allow the same moves as equations, but dividing by a negative turns the sign round. Whole-number ages make $age > 17$ and $age \ge 18$ the same. |

## What we have now

| Term or move | What it means |
|---|---|
| inequality | A statement that one amount is bigger or smaller than another: $<$, $\le$, $>$, $\ge$ |
| `<`, `<=`, `>`, `>=`, `==`, `!=` | Python's comparisons. Each gives `True` or `False`. |
| condition | A question whose answer is True or False |
| solving an inequality | The same moves as an equation. Dividing or multiplying by a negative number turns the sign round. |
| `if`, `elif`, `else` | Choose one branch. Checked from the top; the first True condition wins. |
| branch | The lines pushed in under `if`, `elif` or `else` |
| `low <= value <= high` | Two comparisons in one line, the way maths writes "between" |
| `between(value, low, high)` | Your first decision tool, now in your toolkit |

For more examples of `if`, `elif` and `else`, the integrated course has
[Making decisions with if, elif and else](tutorial:making-decisions).
