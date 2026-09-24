---
title: "True, false and every case: truth tables — Practice"
practice_for: true-false-and-every-case
year: "2026-2027"
version: 2026.09.24.1
---

# True, false and every case: truth tables — Practice

Each problem says what kind it is. **Predict** means guess first, then
run. **Make** means write something new. **Fix** means find one mistake
in code that looks fine. **Explain** means answer in words. **Another
way** means reach the same place by a second route. The answers are
folded away until you open them.

## Warm-up

Use this cell for any of the warm-up problems.

```python exec
id: true-false-practice-warm-up
# Try things here
```

**1. Predict.** What does this line print?

```python
print(True and False, True or False, not True)
```

<details class="dl-answer"><summary>answer</summary>

`False True False`.

`and` needs both sides True, and one is False. `or` needs at least one
True, and it has one. `not True` is the other value, False.

</details>

**2. Make.** A smoke alarm beeps when it senses smoke, or when its
battery is low. Name two Boolean values, `smoke` and `low_battery`, and
write the line that says whether it beeps. Try it with no smoke and a low
battery.

<details class="dl-answer"><summary>answer</summary>

```python
smoke = False
low_battery = True
beep = smoke or low_battery
print(beep)
```

This prints `True`. One reason to beep is enough, so the rule uses `or`.

</details>

**3. Explain.** A rule has four True/False inputs. Without writing the
table, how many rows does its truth table have, and why?

<details class="dl-answer"><summary>answer</summary>

16 rows. Each input can be False or True, and each new input doubles the
rows: every old row appears once with the new input False and once with
it True. So 2, 4, 8, 16, which is $2^4$.

</details>

**4. Another way.** A match goes ahead when it is not raining. One way
to write that is `not raining`. Write it another way, with `==`, and
check that the two agree in both rows.

<details class="dl-answer"><summary>answer</summary>

```python
for raining in [False, True]:
    print(raining, not raining, raining == False)
```

This prints:

```text
False True True
True False False
```

The last two columns agree in every row, so the two ways say the same
thing. `not raining` is shorter, and reads closer to the English.

</details>

## Core

This cell gives the page the reference `truth_table`, so every problem
below can use it. Run it first.

```python exec
id: true-false-practice-tools
def truth_table(rule, names):
    """Print every row of rule, for one, two or three True/False inputs.

    names holds the name of each input, in order. Give back the
    result column as a list, from the all-False row to the all-True row.
    """
    results = []
    if len(names) == 1:
        print(names[0], "result", sep="\t")
        for a in [False, True]:
            result = rule(a)
            print(a, result, sep="\t")
            results.append(result)
    elif len(names) == 2:
        print(names[0], names[1], "result", sep="\t")
        for a in [False, True]:
            for b in [False, True]:
                result = rule(a, b)
                print(a, b, result, sep="\t")
                results.append(result)
    elif len(names) == 3:
        print(names[0], names[1], names[2], "result", sep="\t")
        for a in [False, True]:
            for b in [False, True]:
                for c in [False, True]:
                    result = rule(a, b, c)
                    print(a, b, c, result, sep="\t")
                    results.append(result)
    else:
        print("truth_table works for one, two or three names.")
    return results

print("truth_table is ready.")
```

**5. Predict.** A pizza deal comes with garlic bread or wedges, but not
both. The shop's program checks an order like this. What does it print?

```python
garlic_bread = True
wedges = True
print(garlic_bread != wedges)
```

<details class="dl-answer"><summary>answer</summary>

`False`. For Boolean values, `!=` is XOR: True when exactly one input is
True. This order has both, so the deal does not allow it.

</details>

**6. Make.** A rail company gives a refund when a train is late or
cancelled, and you kept your ticket. Write `refund(late, cancelled,
kept_ticket)` and print its truth table with `truth_table`. In how many
rows is there a refund?

```python exec
id: true-false-practice-refund
# Your refund rule and its table
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Which two inputs belong together, joined by `or`?
2. Put brackets round that part.
3. Join the bracket to `kept_ticket` with `and`.

**Think about:** what the rule would mean without the brackets.

**Try this next:** change the rule so a cancelled train gives a refund
even without the ticket.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def refund(late, cancelled, kept_ticket):
    """A refund when the train was late or cancelled, and you kept your ticket."""
    return (late or cancelled) and kept_ticket

truth_table(refund, ["late", "cancelled", "kept_ticket"])
```

The result column is `[False, False, False, True, False, True, False,
True]`. There is a refund in 3 of the 8 rows: late only, cancelled only,
and both. In each of them, `kept_ticket` is True.

</details>

**7. Fix.** This loop should print the four rows of "wasting heat": the
heating is on and a window is open. It prints only two rows. Run it,
then find the mistake.

```python exec
id: true-false-practice-fix-rows
for heating_on in [False, True]:
    for window_open in [False, True]:
        wasting = heating_on and window_open
    print(heating_on, window_open, wasting)
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Which lines are pushed in under the inner `for`?
2. Is the `print` line one of them?
3. How many times does a line under the outer loop only run?

**Think about:** which value of `window_open` the two printed rows show.

</details>

<details class="dl-answer"><summary>answer</summary>

The `print` line is pushed in only as far as the outer loop, so it runs
once for each value of `heating_on`: two times. By then the inner loop
has finished, and `window_open` is always True. Push the `print` in one
more step, so it sits inside the inner loop:

```python
for heating_on in [False, True]:
    for window_open in [False, True]:
        wasting = heating_on and window_open
        print(heating_on, window_open, wasting)
```

Now it prints four rows, and only the last one says True. Nothing
crashed: the spaces at the start of a line changed what the program
means.

</details>

**8. Make.** In a quiz, a buzzer point counts only when exactly one of
the two teams buzzes. Write `point_counts(team_a, team_b)` and test it
with `assert`, checking its whole result column.

<details class="dl-answer"><summary>answer</summary>

```python
def point_counts(team_a, team_b):
    """True when exactly one team buzzed."""
    return team_a != team_b

assert truth_table(point_counts, ["team_a", "team_b"]) == [False, True, True, False]
print("point_counts keeps its promise.")
```

This is XOR. Neither team buzzing gives no point, and both buzzing at
once gives no point either.

</details>

**9. Explain.** A gallery's sign says "free entry for children under 5
or adults over 65". Is that "or" inclusive or exclusive? Does it matter
here?

<details class="dl-answer"><summary>answer</summary>

It does not matter. The two differ only in the row where both parts are
True, and nobody is under 5 and over 65 at once. That row can never
happen, so both kinds of "or" give the same answer for every real
visitor.

This happens often in real rules. When two conditions cannot both be
True, the difference between inclusive and exclusive "or" disappears.

</details>

**10. Predict.** In a three-input truth table, the rows count up in
binary from 000 to 111, with False as 0 and True as 1. Counting the
first row as row 0, which row is `True, False, True`? Check with
`to_binary` from your toolkit.

<details class="dl-answer"><summary>answer</summary>

Row 5. `True, False, True` is 101 in binary, which is $4 + 0 + 1 = 5$.

```python
print(to_binary(5))
```

This prints `101`. Counting from row 0, row 5 is the sixth row printed.

</details>

**11. Another way.** XOR means "at least one, but not both". Write that
sentence with `or`, `and` and `not`, as a function `xor_in_words(a, b)`.
Then check that its column is the same as the column for `a != b`.

<details class="dl-answer"><summary>answer</summary>

```python
def xor_in_words(a, b):
    """At least one is True, but not both."""
    return (a or b) and not (a and b)

def xor_by_difference(a, b):
    """The two values are different."""
    return a != b

first = truth_table(xor_in_words, ["a", "b"])
second = truth_table(xor_by_difference, ["a", "b"])
print(first == second)
```

The last line prints `True`: both columns are `[False, True, True,
False]`. The first way follows the English. The second way is shorter,
and it only works because True and False are the only values here.

</details>

## Stretch

**12. Make.** Three judges each vote yes or no, and a dive passes when at
least two of them vote yes. Write `majority(judge_1, judge_2, judge_3)`
with `and` and `or`. Test its whole column with `assert`.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. List the pairs of judges: 1 and 2, 1 and 3, 2 and 3.
2. The dive passes when any one pair both say yes.
3. So join three `and` parts with `or`.

**Think about:** why all three saying yes is already covered.

**Try this next:** with five judges, how many pairs would a rule like
this need? Is there a shorter way to count yes votes?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def majority(judge_1, judge_2, judge_3):
    """True when at least two of the three judges vote yes."""
    return (judge_1 and judge_2) or (judge_1 and judge_3) or (judge_2 and judge_3)

column = truth_table(majority, ["judge_1", "judge_2", "judge_3"])
assert column == [False, False, False, True, False, True, True, True]
print("majority keeps its promise.")
```

Four of the eight rows pass: the three rows with exactly two yes votes,
and the row with three.

</details>

**13. Fix.** This cell should print the truth table of an umbrella rule.
It stops with an error instead. Run it, read the last line of the error,
and fix it.

```python exec
id: true-false-practice-fix-umbrella
def umbrella(raining, windy):
    """Take an umbrella when it is raining and not windy."""
    return raining and not windy

truth_table(umbrella(), ["raining", "windy"])
```

<details class="dl-answer"><summary>answer</summary>

The last line of the error is:

```text
TypeError: umbrella() missing 2 required positional arguments: 'raining' and 'windy'
```

The brackets after `umbrella` call the function straight away, with no
inputs, before `truth_table` even starts. `truth_table` wants the rule
itself, so it can call it once for each row. Take the brackets away:

```python
truth_table(umbrella, ["raining", "windy"])
```

The column is `[False, False, True, False]`: an umbrella only when it is
raining and calm.

</details>

**14. Predict.** Say a computer can check one million rows of a truth
table every second. About how long does it take to check every row of a
rule with 20 inputs? With 40 inputs? Guess first, then work it out with
`**`.

<details class="dl-answer"><summary>answer</summary>

```python
rows_20 = 2 ** 20
rows_40 = 2 ** 40
print(rows_20, "rows:", rows_20 / 1000000, "seconds")
print(rows_40, "rows:", rows_40 / 1000000 / 60 / 60 / 24, "days")
```

20 inputs give 1,048,576 rows: about one second. 40 inputs give
1,099,511,627,776 rows: about 12.7 days. Twenty more inputs make the
work about a million times bigger, because $2^{20}$ is about a million.
Checking every case is a great method, until the number of cases grows
this fast.

</details>

**15. Another way.** On
[Choosing a path](tutorial:choosing-a-path) we chose with `if`, `elif`
and `else`. Write the festival rule, a ticket and (18 or over, or with
an adult), as a function `let_in_by_path` that uses `if` and `else` with
no `and` or `or` at all. Check that its column matches
`has_ticket and (over_18 or with_adult)`.

<details class="dl-answer"><summary>answer</summary>

```python
def let_in_by_path(has_ticket, over_18, with_adult):
    """The festival rule, as a path of questions."""
    if not has_ticket:
        return False
    elif over_18:
        return True
    else:
        return with_adult

def let_in(has_ticket, over_18, with_adult):
    """The festival rule, with and and or."""
    return has_ticket and (over_18 or with_adult)

print(truth_table(let_in_by_path, ["has_ticket", "over_18", "with_adult"])
      == truth_table(let_in, ["has_ticket", "over_18", "with_adult"]))
```

The last line prints `True`. A path of questions and a line of `and`
and `or` can say the same rule. The path asks about the ticket first,
because without one nothing else matters.

</details>
