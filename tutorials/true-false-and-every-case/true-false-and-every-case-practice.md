---
title: "True, false and every case: truth tables — Practice"
practice_for: true-false-and-every-case
year: "2026-2027"
version: 2026.09.25.1
---

# True, false and every case: truth tables — Practice

Each problem says what kind it is. **Predict** means guess first, then
run. **Make** means write something new. **Fix** means find why code
that looks fine does something else, and change it. **Explain** means answer in words. **Another
way** means reach the same place by a second route. The answers are
folded away until you open them.

Guess before you open anything. A guess that misses is the most
useful kind. It shows you exactly which row you had not pictured.

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

It has 16 rows. Each input can be False or True, and each new input
doubles the rows. Every old row appears once with the new input False
and once with it True. So the counts are 2, 4, 8, 16, which is $2^4$.

</details>

**4. Another way.** A game pauses itself when its window is not in
focus, that is, when you have clicked on another window. One way to
write that is `not focused`. Write it another way, with `==`, and check
that the two agree in both rows.

<details class="dl-answer"><summary>answer</summary>

```python
for focused in [False, True]:
    print(focused, not focused, focused == False)
```

This prints:

```text
False True True
True False False
```

The last two columns agree in every row, so the two ways say the same
thing. `not focused` is shorter, and reads closer to the English.

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

**5. Predict.** Two motion sensors watch the same door. If exactly one
of them fires, one of the sensors may be broken, so the alarm system
logs a fault. Both fired just now. What does this print?

```python
sensor_1 = True
sensor_2 = True
print(sensor_1 != sensor_2)
```

<details class="dl-answer"><summary>answer</summary>

`False`. For Boolean values, `!=` is XOR, which is True when exactly one
input is True. Both sensors agree, so there is no fault to log. Somebody really
did walk through the door.

</details>

**6. Make.** A server sends an alert to the engineer on duty when its
disk is full or last night's backup failed, and alerts are switched on.
Write `alert(disk_full, backup_failed, alerts_on)` and print its truth
table with `truth_table`. In how many rows is there an alert?

```python exec
id: true-false-practice-alert
# Your alert rule and its table
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Which two inputs belong together, joined by `or`?
2. Put brackets round that part.
3. Join the bracket to `alerts_on` with `and`.

**Think about:** what the rule would mean without the brackets.

**Try this next:** change the rule so a failed backup sends an alert even
when alerts are switched off.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def alert(disk_full, backup_failed, alerts_on):
    """An alert when the disk is full or the backup failed, and alerts are on."""
    return (disk_full or backup_failed) and alerts_on

truth_table(alert, ["disk_full", "backup_failed", "alerts_on"])
```

The result column is `[False, False, False, True, False, True, False,
True]`. There is an alert in 3 of the 8 rows: disk full only, backup
failed only, and both. In each of them, `alerts_on` is True.

</details>

**7. Fix.** This loop should print the four rows of "wasting heat": the
heating is on and a window is open. It prints only two rows. Run it,
then find why.

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
once for each value of `heating_on`, which is two times. By then the inner loop
has finished, and `window_open` is always True. Push the `print` in one
more step, so it sits inside the inner loop:

```python
for heating_on in [False, True]:
    for window_open in [False, True]:
        wasting = heating_on and window_open
        print(heating_on, window_open, wasting)
```

Now it prints four rows, and only the last one says True. Nothing
crashed. The spaces at the start of a line changed what the program
means.

</details>

**8. Make.** In a quiz, a buzzer point counts only when exactly one of
the two teams buzzes. Write `point_counts(team_a, team_b)` and test it
with `assert`, checking its whole result column.

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Yours may be different and work too.

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

**9. Explain.** A weather station's program marks a temperature reading
as "suspect" when it is below $-50$ °C or above 60 °C. Is that "or"
inclusive or exclusive? Does it matter here?

<details class="dl-answer"><summary>answer</summary>

It does not matter. The two differ only in the row where both parts are
True, and no reading is below $-50$ and above 60 at once. That row can
never happen, so both kinds of "or" give the same answer for every
reading.

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

**11. Another way.** Schlomo, who is learning Python too, does not
trust `!=` as XOR. He wants the rule to say what the English says: "at
least one, but not both". Write his sentence with `or`, `and` and `not`,
as a function `xor_in_words(a, b)`. Then check whether his column is the
same as the column for `a != b`.

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

The last line prints `True`, because both columns are `[False, True, True,
False]`. Schlomo's way follows the English, and a reader can check it
against the sentence. The `!=` way is shorter, and it only works because
True and False are the only values here. Both ways work.

</details>

## Stretch

**12. Make.** Some aircraft and spacecraft carry three computers that
calculate the same answer, and follow the majority. Then one broken
computer cannot steer the craft wrong. Each computer "votes" True or
False. Write `majority(computer_1, computer_2, computer_3)`, True when at
least two vote True, with `and` and `or`. Test its whole column with
`assert`.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. List the pairs of computers: 1 and 2, 1 and 3, 2 and 3.
2. The vote is True when any one pair both say True.
3. So join three `and` parts with `or`.

**Think about:** why all three saying True is already covered.

**Try this next:** with five computers, how many pairs would a rule like
this need? Is there a shorter way to count the True votes?

</details>

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Yours may be different and work too.

```python
def majority(computer_1, computer_2, computer_3):
    """True when at least two of the three computers vote True."""
    return (computer_1 and computer_2) or (computer_1 and computer_3) or (computer_2 and computer_3)

column = truth_table(majority, ["computer_1", "computer_2", "computer_3"])
assert column == [False, False, False, True, False, True, True, True]
print("majority keeps its promise.")
```

Four of the eight rows pass. They are the three rows with exactly two
True votes, and the row with three. Engineers call this *triple modular redundancy*.
The Space Shuttle went further. Four of its five flight computers ran
the same program and checked each other, and they could vote to ignore
a faulty one.

</details>

<aside class="dl-note" id="true-false-practice-note-saturn">

**Votes inside a rocket.** The computer that steered the Saturn V
rocket towards the Moon was built by IBM, and it voted inside itself.
It had three copies of its logic, and each job passed through seven
stages. At every stage, a vote kept the answer that at least two copies
gave. So one faulty part at any stage did not change the result.

</aside>

**13. Fix.** Schlomi, who is learning Python too, wrote this cell to
print the truth table of an umbrella rule. It stops with an error
instead. She had a reason. `umbrella` is a function, and functions
are called with brackets. Run it, read the last line of the error, and
fix it.

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

The brackets after `umbrella` call the function at once, with no
inputs, before `truth_table` even starts. `truth_table` wants the rule
itself, so it can call it once for each row. Remove the brackets:

```python
truth_table(umbrella, ["raining", "windy"])
```

The column is `[False, False, True, False]`. It says to take an
umbrella only when it is raining and calm.

</details>

**14. Predict.** Say a computer can check one million rows of a truth
table every second. About how long does it take to check every row of a
rule with 20 inputs? With 40 inputs? Guess first, then calculate it with
`**`.

<details class="dl-answer"><summary>answer</summary>

```python
rows_20 = 2 ** 20
rows_40 = 2 ** 40
print(rows_20, "rows:", rows_20 / 1000000, "seconds")
print(rows_40, "rows:", rows_40 / 1000000 / 60 / 60 / 24, "days")
```

20 inputs give 1,048,576 rows, which take about one second. 40 inputs
give 1,099,511,627,776 rows, which take about 12.7 days. Twenty more inputs make the
work about a million times bigger, because $2^{20}$ is about a million.
We can check every case for a small rule, but not when the cases
grow this fast.

</details>

**15. Another way.** On
[Choosing a path](tutorial:choosing-a-path) we chose with `if`, `elif`
and `else`. Write the login rule from the tutorial, a right password and
(at the office, or a right phone code), as a function `log_in_by_path`
that uses `if` and `else` with no `and` or `or` at all. Check that its
column matches `password_ok and (at_office or code_ok)`.

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Your path may ask its questions in another
order and work too.

```python
def log_in_by_path(password_ok, at_office, code_ok):
    """The login rule, as a path of questions."""
    if not password_ok:
        return False
    elif at_office:
        return True
    else:
        return code_ok

def log_in(password_ok, at_office, code_ok):
    """The login rule, with and and or."""
    return password_ok and (at_office or code_ok)

print(truth_table(log_in_by_path, ["password_ok", "at_office", "code_ok"])
      == truth_table(log_in, ["password_ok", "at_office", "code_ok"]))
```

The last line prints `True`. A path of questions and a line of `and`
and `or` can say the same rule. This path asks about the password first,
because without it nothing else matters.

</details>

## Where to read more

Steve Mould (2013). *Can you solve this 4 card puzzle?*
<https://www.youtube.com/watch?v=Hpwd_ns2Wjs>. A famous puzzle about an
"if" rule, which surprises most people. Write your answer down before the
end. Three minutes.
