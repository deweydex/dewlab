---
title: "Untangling a condition: De Morgan's laws — Practice"
practice_for: untangling-a-condition
year: "2026-2027"
version: 2026.09.24.1
---

# Untangling a condition: De Morgan's laws — Practice

Each answer is hidden until you open it. Many problems ask you to guess
before you run anything. The guess is the real exercise, so make one
first, even if you are unsure.

`same_rule` and `truth_table` come from your toolkit, so every cell on
this page can use them.

## Warm-up

This cell sets up a few rules for the warm-up problems. Run it first.

```python exec
id: untangling-practice-tools-1
def can_jump(is_falling, is_stunned):
    return not (is_falling or is_stunned)

def both(a, b):
    return a and b

def either(a, b):
    return a or b
```

**1. Predict.** In a video game, a character can jump when
`not (is_falling or is_stunned)`. She is not falling, but she is stunned.
Can she jump? Say `True` or `False`, then check with
`can_jump(False, True)`.

<details class="dl-answer"><summary>answer</summary>

`False`. She cannot jump.

Inside the brackets, `False or True` is `True`: at least one thing is
stopping her. The `not` flips that to `False`.

With the second law, the rule is `not is_falling and not is_stunned`. She
needs both to be false, and one of them is true.

</details>

**2. Make.** A recipe app shows a "Quick meals" banner when
`not (has_time and has_oven)`. Write the same rule without brackets, using
the first law.

<details class="dl-answer"><summary>answer</summary>

`not has_time or not has_oven`.

Put a `not` on each part, then swap `and` for `or`. In words: show quick
meals if you are short of time, or if you have no oven. You can check it:

```python
def banner(has_time, has_oven):
    return not (has_time and has_oven)

def banner_no_brackets(has_time, has_oven):
    return not has_time or not has_oven

same_rule(banner, banner_no_brackets, 2)    # True
```

</details>

**3. Explain.** Python reads `not a or b` in one of these two ways. Which
one, and why? Find a row where the two ways give different answers.

- `(not a) or b`
- `not (a or b)`

<details class="dl-answer"><summary>answer</summary>

Python reads it as `(not a) or b`, because `not` goes first, then `and`,
then `or`.

They differ when `a` is `False` and `b` is `True`. Then `(not a) or b` is
`True or True`, which is `True`. But `not (a or b)` is `not True`, which is
`False`.

If you mean the second one, you need the brackets.

</details>

**4. Predict.** The tools cell defined `both(a, b)` as `a and b`, and
`either(a, b)` as `a or b`. What will `same_rule(both, either, 2)` give?
In how many rows do they disagree?

<details class="dl-answer"><summary>answer</summary>

`False`. They disagree in two rows: `(False, True)` and `(True, False)`.
There, `either` is `True` and `both` is `False`.

They agree when the two inputs are the same, because `True and True` and
`True or True` are both `True`, and the same goes for `False`.

</details>

## Core

These rules are for the core problems. Run this cell before you start.

```python exec
id: untangling-practice-tools-2
def grey_out_a(is_open, has_stock):
    return not (is_open and has_stock)

def grey_out_c(is_open, has_stock):
    return not is_open and not has_stock

def washing_out(is_raining, is_cold):
    return not (is_raining or is_cold)
```

**5. Make.** You can hang your washing outside when
`not (is_raining or is_cold)`. That rule is `washing_out` in the tools cell.
Write `washing_out_2`, the same rule without brackets, and check it with
`same_rule`.

```python exec
id: untangling-practice-washing
# Your washing_out_2, and a same_rule check
```

<details class="dl-answer"><summary>answer</summary>

```python
def washing_out_2(is_raining, is_cold):
    return not is_raining and not is_cold

print(same_rule(washing_out, washing_out_2, 2))    # True
```

This is the second law: "not raining or cold" means "not raining, and not
cold".

</details>

**6. Fix.** Someone wrote their own version of `same_rule`. It passes the
first test, but it says `grey_out_a` and `grey_out_c` are the same rule, and
we know they are not. Run it, find the one mistake, and fix it.

```python exec
id: untangling-practice-fix-same-rule
from itertools import product

def same_rule_draft(rule_a, rule_b, count):
    """True when the two rules agree on every row."""
    for row in product([False, True], repeat=count):
        if rule_a(*row) != rule_b(*row):
            return False
        return True

print(same_rule_draft(grey_out_a, grey_out_a, 2))   # should be True
print(same_rule_draft(grey_out_a, grey_out_c, 2))   # should be False
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Look at the first row the loop checks, `(False, False)`. Do the two
   rules agree there?
2. After that `if`, which line runs next?
3. How many rows has the loop looked at when the function returns?

**Think about:** when is it safe to say "these rules are the same"?

**Try this next:** add `print(row)` as the first line inside the loop, and
watch how many rows appear.

</details>

<details class="dl-answer"><summary>answer</summary>

`return True` is inside the loop. On the first row, `(False, False)`, both
rules give `True`, so they agree. Then the function reaches `return True`
and stops, after checking only one row.

Move `return True` out of the loop, so that it runs only after every row
has been checked:

```python
def same_rule_draft(rule_a, rule_b, count):
    for row in product([False, True], repeat=count):
        if rule_a(*row) != rule_b(*row):
            return False
    return True
```

Now the second line prints `False`. One space of indentation changed
what happens when, and so it changed the whole promise.

</details>

**7. Another way.** In arithmetic, $-(a + b) = -a + (-b)$. With `not`, the
same move gives `not a and not b`, which is not the same as
`not (a and b)`. But is it ever right? Find the rows where
`not (a and b)` and `not a and not b` do agree. What kind of space would
make the arithmetic move always right?

<details class="dl-answer"><summary>answer</summary>

Use `truth_table` on both, or write the four rows by hand:

| a | b | `not (a and b)` | `not a and not b` |
|---|---|---|---|
| False | False | True | True |
| False | True | True | False |
| True | False | True | False |
| True | True | False | False |

They agree in the rows where `a` and `b` are the same. So in a smaller
space, where the two inputs always come together (for example, a light
and its own switch, which are either both on or both off), the move is
always right. In the full space of True/False pairs, it is right only half
the time.

</details>

**8. Make.** A hotel has quiet hours from 23:00 until 07:00, so on a
24-hour clock the quiet hours are `hour >= 23 or hour < 7`. Write
`noise_allowed(hour)` using `between` from your toolkit. Then check it
against `not (hour >= 23 or hour < 7)` for every hour from 0 to 23.

```python exec
id: untangling-practice-quiet-hours
# Your noise_allowed(hour), and a loop that checks every hour
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Use the second law on `not (hour >= 23 or hour < 7)`.
2. `not (hour >= 23)` is `hour < 23`, and `not (hour < 7)` is `hour >= 7`.
3. For whole-number hours, `hour < 23` is the same as `hour <= 22`.

**Think about:** which hours are left when you take the quiet hours away?

**Try this next:** a shop is closed `hour < 9 or hour >= 18`. When is it
open?

</details>

<details class="dl-answer"><summary>answer</summary>

The second law gives `hour < 23 and hour >= 7`, which for whole hours is
7 to 22.

```python
def noise_allowed(hour):
    return between(hour, 7, 22)

for hour in range(0, 24):
    if noise_allowed(hour) != (not (hour >= 23 or hour < 7)):
        print("Different at", hour)
print("Checked all 24 hours.")
```

Nothing is printed except the last line, so the two agree at every hour.

</details>

**9. Explain.** On the tutorial page, `same_rule` checked De Morgan's law on
four rows, and we called that a proof. The loop over ages from 0 to 100 also
found no disagreement. Why is the first a proof about every possible input,
when the loop, on its own, is not?

<details class="dl-answer"><summary>answer</summary>

In the space of True and False, two inputs have exactly four possible
rows, and `same_rule` checked all four. There is nothing left to check.

Ages are numbers, and there are far more numbers than 0 to 100: 17.5, −3,
a million. The loop checked 101 of them and said nothing about the rest.
What makes the age rule hold everywhere is the law, because each
comparison is only ever True or False. The loop was a check on a few
cases, and the law is the reason it holds for all of them.

</details>

**10. Predict.** What is `not not not True`? Guess, then run it.

<details class="dl-answer"><summary>answer</summary>

`False`.

Each `not` flips the value. Two flips bring it back to where it started,
so `not not True` is `True`, and one more `not` makes it `False`. An odd
number of nots flips the value, and an even number leaves it alone.

</details>

**11. Fix.** A cinema shows a film to anyone aged 18 or over, or anyone who
comes with an adult. The original rule for turning people away was
`not (age >= 18 or with_adult)`. Someone removed the brackets and made a
mistake. A 20-year-old on their own is now turned away. Find the mistake
and fix it.

```python exec
id: untangling-practice-fix-cinema
def turn_away(age, with_adult):
    return not age >= 18 or not with_adult

print(turn_away(20, False))   # should be False: an adult on their own may go in
print(turn_away(15, True))    # should be False
print(turn_away(15, False))   # should be True
```

<details class="dl-answer"><summary>answer</summary>

The `or` should have become an `and`. The second law turns
`not (A or B)` into `not A and not B`:

```python
def turn_away(age, with_adult):
    return not age >= 18 and not with_adult
```

Now the three lines print `False`, `False` and `True`. You could also
write `age < 18 and not with_adult`, which reads well aloud: turn someone
away if they are under 18 and have no adult with them.

</details>

## Stretch

**12. Make.** When `same_rule` says `False`, you want to know which row
is different. Write `first_difference(rule_a, rule_b, count)`. It returns
the first row where the two rules disagree, or `None` if they agree on
every row. Test it on `grey_out_a` and `grey_out_c`.

```python exec
id: untangling-practice-first-difference
# Your first_difference
```

<details class="dl-answer"><summary>answer</summary>

It has the same shape as `same_rule`. The only change is what it gives
back:

```python
from itertools import product

def first_difference(rule_a, rule_b, count):
    """Return the first row where the rules disagree, or None if none does."""
    for row in product([False, True], repeat=count):
        if rule_a(*row) != rule_b(*row):
            return row
    return None

print(first_difference(grey_out_a, grey_out_c, 2))   # (False, True)
print(first_difference(grey_out_a, grey_out_a, 2))   # None
```

`(False, True)` means a café that is closed but has stock. `grey_out_a`
greys the button out there, and `grey_out_c` does not.

</details>

**13. Make.** A home heating system uses this rule:

```python
def heating_on(is_warm, someone_home, window_open):
    return not (is_warm or not someone_home) and not window_open
```

Untangle it one law at a time, checking each step with `same_rule`. Then
say the rule in one sentence.

```python exec
id: untangling-practice-heating
def heating_on(is_warm, someone_home, window_open):
    return not (is_warm or not someone_home) and not window_open

# Your untangled steps, each checked with same_rule
```

<details class="dl-answer"><summary>answer</summary>

Step 1, the second law on the brackets:
`not is_warm and not not someone_home and not window_open`.

Step 2, double negation:
`not is_warm and someone_home and not window_open`.

```python
def heating_step_1(is_warm, someone_home, window_open):
    return not is_warm and not not someone_home and not window_open

def heating_step_2(is_warm, someone_home, window_open):
    return not is_warm and someone_home and not window_open

print(same_rule(heating_on, heating_step_1, 3))   # True
print(same_rule(heating_on, heating_step_2, 3))   # True
```

In words: the heating comes on when it is not warm, someone is at home,
and no window is open.

</details>

**14. Another way.** On [Numbers a computer can
hold](tutorial:numbers-a-computer-can-hold) we worked with whole numbers.
Write True as 1 and False as 0. Then `a and b` is the same as `a * b`, and
`not a` is the same as `1 - a`. Use this to write both sides of the first
law as arithmetic, and check them for every pair of 0s and 1s. You will
need `a or b`, which is `a + b - a * b`.

```python exec
id: untangling-practice-arithmetic
# Both sides of the first law, as arithmetic on 0 and 1
```

<details class="dl-answer"><summary>answer</summary>

The left side, `not (a and b)`, is `1 - a * b`.

The right side, `not a or not b`, uses the `or` formula with `1 - a` and
`1 - b` in place of `a` and `b`:
$(1 - a) + (1 - b) - (1 - a)(1 - b)$.

```python
for a in [0, 1]:
    for b in [0, 1]:
        left = 1 - a * b
        right = (1 - a) + (1 - b) - (1 - a) * (1 - b)
        print(a, b, left, right)
```

The two columns match on all four rows. You can also multiply out the
right side by hand: $(1 - a)(1 - b) = 1 - a - b + ab$, so the right side is
$2 - a - b - 1 + a + b - ab$, which is $1 - ab$. That is the left side. The
same law, proved in the space of numbers.

</details>

**15. Explain.** `same_rule` with `count` inputs checks $2^{\text{count}}$
rows. A rule with 30 inputs has how many rows? If a computer checks
10 million rows a second, about how long does that take? What does this
tell you about checking every row as a way to prove things?

<details class="dl-answer"><summary>answer</summary>

$2^{30} = 1{,}073{,}741{,}824$, a little over a billion rows. At
10,000,000 rows a second, that is about 107 seconds, a little under two
minutes.

```python
rows = 2 ** 30
print(rows, rows / 10_000_000)    # 1073741824 107.3741824
```

Each extra input doubles the time, so 40 inputs would take over 30 hours,
and 50 inputs over three and a half years. Checking every row is a real
proof, but it stops being practical fast. That is why laws like De
Morgan's matter: they let us prove two rules are the same without
checking every row.

</details>
