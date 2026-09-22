---
title: "Making Decisions"
year: "2026-2027"
version: 2026.09.22.1
covers:
  comparisons-true-or-false:
    covers: [PDP-LO6]
  if-statements-choosing-a-path:
    covers: [PDP-LO6]
  if-else-two-paths:
    covers: [PDP-LO6]
  elif-multiple-paths:
    covers: [PDP-LO6]
  boolean-operators-combining-conditions:
    covers: [PDP-LO6]
    touches: [MIT-2.4]
  classifying-numbers-a-mathematical-application:
    covers: [MIT-1.1]
---

# Making Decisions

So far, our programs have run every line from top to bottom, every time.
Real algorithms need to make choices. "If the water has boiled, pour it.
Otherwise, keep waiting." "If the number is negative, deal with it in a
different way."

On this page, we learn how a program can choose a different path,
depending on a condition.

## Comparisons: True or False?

Before a program can make a decision, it needs to ask a question with a
True or False answer. Python has *comparison operators* for this. A
comparison operator is a symbol that compares two values and gives back
`True` or `False`.

Here are all six. Can you guess what each line prints before you run it?

```python exec
id: comparisons-true-or-false-1
# Comparison operators
print(5 > 3)        # greater than
print(5 < 3)        # less than
print(5 >= 5)       # greater than or equal to
print(5 <= 4)       # less than or equal to
print(5 == 5)       # equal to (note: two equals signs!)
print(5 != 3)       # not equal to
```

| Operator | Meaning |
|---|---|
| `>` | greater than |
| `<` | less than |
| `>=` | greater than or equal to |
| `<=` | less than or equal to |
| `==` | equal to |
| `!=` | not equal to |

Look closely at `==`. It has two equals signs.

- One equals sign, `=`, is *assignment*. It gives a name a value.
- Two equals signs, `==`, is *comparison*. It asks whether two things
  are equal.

Mixing up `=` and `==` is one of the most common mistakes in
programming. It trips up experienced programmers too.

Each comparison gives a Boolean value, `True` or `False`. Every decision
a program makes is built from values like these.

### Your turn

What do you think each comparison below will print? Write your guess
after `prediction:` on each line. Then run the cell to check.

```python exec
id: your-turn-1
# Predict first, then verify
print(10 > 10)        # prediction: 
print(10 >= 10)       # prediction: 
print("abc" == "abc") # prediction: 
print("abc" == "ABC") # prediction: 
print(1 == 1.0)       # prediction: 
print(0 == False)     # prediction: 
```

Did any of them surprise you? Look at the last one. In Python, `False`
counts as equal to `0`, and `True` counts as equal to `1`. This link
between logic and arithmetic goes back to George Boole's work in the
1850s. The word "Boolean" comes from his name.

## If Statements: Choosing a Path

An *if statement* is code that runs only when a condition is True. Here
is one. What do you think it prints?

```python exec
id: if-statements-choosing-a-path-1
temperature = 35

if temperature > 30:
    print("It's hot today!")
    print("Maybe stay indoors.")

print("This line always runs, regardless of the temperature.")
```

Look at the shape of the first line. It has three parts:

1. the keyword `if`
2. a condition, `temperature > 30`
3. a colon, `:`

The indented lines under it are the *body* of the if statement. The body
runs only when the condition is True. The last line is not indented, so
it is back in the normal flow. It runs every time.

Python uses indentation to know which lines belong inside the if
statement. So in Python, indentation is required. We use four spaces for
each level. Most editors put in four spaces for you when you press Tab.

### What happens when the condition is False?

What would happen if the temperature were 20? Change `35` to `20` in the
cell above, and run it again.

This time, Python skips the two indented lines. Only the last `print`
runs.

## If-Else: Two Paths

Often we want to do one thing when a condition is True, and something
different when it is False. An *if-else* statement does this.

```python exec
id: if-else-two-paths-1
number = 7

if number % 2 == 0:
    print(str(number) + " is even")
else:
    print(str(number) + " is odd")
```

The `else` part catches every case that the `if` condition does not.
Between them, the two paths cover every possibility.

What is the `%` doing here? We met `%`, the remainder (or modulo)
operator, in [First Steps](tutorial:first-steps). When a number divided
by 2 leaves a remainder of 0, the number is even. Otherwise, it is odd.
We will use `% 2 == 0` to test for "even" many more times in this
course.

### Your turn

Can you write a program that looks at a variable `year` and prints
whether it is a leap year? For now, we use a short rule: a year is a
leap year if it can be divided by 4. (The full rule has more detail about
centuries. We come back to it further down this page.)

1. In the cell below, write your pseudocode as comments, one step per
   line.
2. Under each comment, write the Python for that step.
3. Run it.

```python exec
id: your-turn-2
# Your leap year checker
year = 2024
```

## Elif: Multiple Paths

Sometimes there are more than two possible cases. The keyword `elif` is
short for "else if". It adds another condition to an if statement, so a
program can have as many paths as it needs.

```python exec
id: elif-multiple-paths-1
score = 72

if score >= 80:
    grade = "Distinction"
elif score >= 65:
    grade = "Merit"
elif score >= 50:
    grade = "Pass"
else:
    grade = "Unsuccessful"

print("Score: " + str(score) + " -> " + grade)
```

Python checks each condition in turn, from top to bottom. It runs the
body of the first condition that is True, and skips all the rest.

So does the order of the conditions matter? Imagine we checked
`score >= 50` first. What grade would a score of 90 get?

It would get "Pass". The number 90 is greater than 50, and that
condition comes first, so Python never reaches the check for
"Distinction". The order matters.

### Your turn

1. Change `score` in the cell above, and run it a few times. Try at
   least one score in each grade.
2. Now try the boundary values: 50, 65 and 80. Does each one get the
   grade you expect?

Bugs often hide at the boundaries, so they are worth testing every time.

Next, you could write a classifier of your own.

3. Plan it as pseudocode, in the comment lines at the top of the cell
   below.
4. Write a program that looks at `number` and prints whether it is
   positive, negative or zero.

```python exec
id: your-turn-3
# Pseudocode:
#
#

# Your number classifier
number = -5
```

## Boolean Operators: Combining Conditions

Sometimes one comparison is not enough. A *Boolean operator* is a word
that combines True and False values, or changes one. Python has three:
`and`, `or` and `not`.

**`and`** is True only when *both* conditions are True.

```python exec
id: boolean-operators-combining-conditions-1
age = 25
has_licence = True

if age >= 17 and has_licence:
    print("Can drive")
else:
    print("Cannot drive")
```

**`or`** is True when *at least one* condition is True.

```python exec
id: boolean-operators-combining-conditions-2
day = "Saturday"

if day == "Saturday" or day == "Sunday":
    print("It's the weekend!")
else:
    print("It's a weekday.")
```

**`not`** turns True into False, and False into True.

```python exec
id: boolean-operators-combining-conditions-3
is_raining = False

if not is_raining:
    print("No umbrella needed")
```

| Operator | True when… |
|---|---|
| `a and b` | `a` and `b` are both True |
| `a or b` | at least one of `a` and `b` is True |
| `not a` | `a` is False |

What changes if you set `age` to 16, `day` to `"Monday"`, or
`is_raining` to `True`? Can you predict each result before you run it?

When one line uses more than one of these operators, Python works them
out in a fixed order: `not` first, then `and`, then `or`. If you are not
sure how Python will read a line, add brackets, `( )`, to make your
meaning clear.

### Your turn

Let's go back to the leap year problem, this time with the full rule:

- A year is a leap year if it can be divided by 4,
- *except* that a year that can be divided by 100 is not a leap year,
- *unless* it can also be divided by 400.

So 2024 is a leap year, because it can be divided by 4. 1900 is not,
because it can be divided by 100 but not by 400. 2000 is a leap year,
because it can be divided by 400.

1. Write your pseudocode in the comment lines of the first cell below.
2. Write the Python under it.
3. Use the second cell to test your checker with several years: 2024,
   1900, 2000, 2023 and 1600. Which of them should be leap years?

```python exec
id: your-turn-4
# Pseudocode:
#
#
#

# Full leap year checker
year = 2000
```

```python exec
id: your-turn-5
# Test with several years: 2024, 1900, 2000, 2023, 1600
```

## Classifying Numbers: A Mathematical Application

Now we can use our new tools on a problem from mathematics: sorting
numbers into families. Mathematicians sort numbers into four families,
and each one sits inside the next.

| Family | Symbol | What it holds | Examples |
|---|---|---|---|
| natural numbers | N | whole numbers from 0 upwards | 0, 1, 7 |
| integers | Z | whole numbers, positive, negative or zero | -3, 0, 7 |
| rational numbers | Q | numbers we can write as one integer divided by another | 1/2, -3.5, 7 |
| real numbers | R | every number on the number line | π, 1/2, 7 |

Each family contains the one before it. Every natural number is also an
integer. Every integer is also a rational number, and every rational
number is also a real number. The families fit together like a set of
Russian dolls, one inside the next.

(Some books start the natural numbers at 1. On this page, and in the
code below, 0 counts as a natural number.)

The program below looks at a value and tells us which families it
belongs to. What do you think it will say about -3.5?

```python exec
id: classifying-numbers-a-mathematical-application-1
# Which number families does a value belong to?
value = -3.5

is_real = True                           # everything we can store is real (approximately)
is_rational = True                       # for our purposes, all Python numbers are rational
is_integer = (value == int(value))       # is it a whole number?
is_natural = is_integer and (value >= 0) # is it a non-negative whole number?

print("Value: " + str(value))
print("Natural (N): " + str(is_natural))
print("Integer (Z): " + str(is_integer))
print("Rational (Q): " + str(is_rational))
print("Real (R): " + str(is_real))
```

### Your turn

1. Change `value` to each of these in turn: 7, -3, 0.5, 0, 3.14159. How
   does the answer change each time?
2. In the cell below, plan a new version as pseudocode. It should use
   `if`, `elif` and `else`.
3. Write it so that it prints one clear summary, such as "7 is a natural
   number (and therefore also an integer, rational, and real)."

**Pseudocode first, then the code:**

```python exec
id: your-turn-6
# Pseudocode:
#
#
#

# Your number classifier
value = 7
```

## Reflection

On this page, our programs learned to choose between paths. We used
`if`, `else` and `elif`, and the Boolean operators `and`, `or` and
`not`. These are *selection structures*: code that chooses which lines
to run.

Before this page, our programs used only *sequential* execution, which
means running every line from top to bottom, every time. Sequence and
selection are two of the three basic building blocks of programming. The
third is *iteration*, which means repetition. We meet it in
[Repeating Yourself](tutorial:repeating-yourself), after a page on what
to do [When It Goes Wrong](tutorial:when-it-goes-wrong).

We also saw that sorting a number into its mathematical families needs
exactly this kind of decision. The mathematics and the programming are
the same activity, seen from two sides.

What did you find most interesting on this page? What did you find
hardest?

## Where to Read More

Khan Academy. *If Statements.*
<https://www.khanacademy.org/computing/intro-to-python-fundamentals/x5279a44ae0ab15d6:designing-algorithms-with-conditionals/x5279a44ae0ab15d6:boolean-conditions/v/if-statements>.
A second walk through the same idea — a program choosing between paths —
with its own examples.

Khan Academy. *Evaluating Compound Boolean Expressions.*
<https://www.khanacademy.org/computing/intro-to-python-fundamentals/x5279a44ae0ab15d6:designing-algorithms-with-conditionals/x5279a44ae0ab15d6:compound-boolean-conditions/v/evaluating-compound-boolean-expressions>.
Traces through `and`, `or` and `not` step by step, which is worth watching
once before trusting your own head to do it.
