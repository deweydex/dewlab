---
title: "Mixed problems: decisions and logic"
practice_across:
  - choosing-a-path
  - true-false-and-every-case
  - untangling-a-condition
  - bits-that-flip
year: "2026-2027"
version: 2026.09.24.1
---

# Mixed problems: decisions and logic

Each problem here draws on at least one page of Unit 2, and many draw on
two or more. None of them is harder than what those pages covered. The new
part is that nobody tells you which page a problem comes from. Choosing
the tool is part of the problem.

Your toolkit is loaded on this page: `between`, `truth_table`,
`same_rule` and `parity_bit` from this unit, and `to_binary` and `to_hex`
from Unit 1. Each answer is hidden until you open it. Where a problem asks
you to predict, make the prediction before you run anything. It is the
most useful part.

## Warm-up

Use this cell for any warm-up problem. Change the line, and run it.

```python exec
id: mixed-decisions-scratch-1
print(between(17.5, 12, 17))
```

**1. Predict.** A bus company's youth fare is for ages 12 to 17. A
program checks `between(age, 12, 17)`. What does it give for an age of
17.5?

<details class="dl-answer"><summary>answer</summary>

`False`, because 17.5 is more than 17.

A fare table usually assumes ages are whole numbers, and in that space
there is nothing between 17 and 18. In the space of decimals, 17.5 falls
into a gap: it is not "12 to 17", and it is not "18 and over" either. On
[Choosing a path](tutorial:choosing-a-path), that assumption was said out
loud in "the space we're in". This is why.

</details>

**2. Predict.** What does `True and not False or False` give? Say which
part Python works out first.

<details class="dl-answer"><summary>answer</summary>

`True`.

`not` goes first: `not False` is `True`. Then `and`: `True and True` is
`True`. Then `or`: `True or False` is `True`. With brackets, Python reads
it as `(True and (not False)) or False`.

</details>

**3. Make.** A swing in the playground is free when
`not (occupied or broken)`. Write it as a function, `swing_free`, and print
its truth table with `truth_table`. In how many rows is the swing free?

<details class="dl-answer"><summary>answer</summary>

```python
def swing_free(occupied, broken):
    return not (occupied or broken)

truth_table(swing_free, ["occupied", "broken"])
```

The swing is free in one row only: not occupied and not broken. That is
De Morgan's second law, from
[Untangling a condition](tutorial:untangling-a-condition):
`not (occupied or broken)` is `not occupied and not broken`.

</details>

**4. Predict.** What is `6 ^ 3`? Work it out in binary first.

<details class="dl-answer"><summary>answer</summary>

5.

6 is `110` and 3 is `011`. Column by column: 1 and 0 differ, so 1. 1 and
1 are the same, so 0. 0 and 1 differ, so 1. That gives `101`, which is 5.

</details>

**5. Explain.** A friend says that `age > 17` and `age >= 18` always mean
the same thing. When is your friend right, and when not?

<details class="dl-answer"><summary>answer</summary>

Your friend is right when ages are whole numbers. Then there is nothing
between 17 and 18, so "more than 17" and "18 or more" pick out the same
ages.

With decimals, they differ. An age of 17.5 is more than 17, but it is not
18 or more. So the friend's move is right in one space and wrong in the
other. Neither of you made a mistake, as long as you both say which space
you are in.

</details>

## Core

A scratch cell for the core problems.

```python exec
id: mixed-decisions-scratch-2
# Try things here
```

**6. Make.** A sports club charges a yearly fee by age. Under 5 is free.
Ages 5 to 17 pay €40. Ages 18 to 64 pay €120. Ages 65 and over pay €60.
Write `club_fee(age)` with `if`, `elif` and `else`, and test it with
`assert` at 4, 5, 17, 18, 64 and 65.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Start with the youngest group, and work up.
2. Each `elif` only runs if every check above it was False, so you do not
   need to check the low end of each group again.
3. The tests are at the edges of the groups, where a `<` in place of a
   `<=` would hide.

**Think about:** could you write it with `between` for each group
instead? Which version reads more like the fee table?

**Try this next:** add a student price of €60 for ages 18 to 22 with a
student card.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def club_fee(age):
    """Return the yearly fee in euro for a member of this age."""
    if age < 5:
        return 0
    elif age <= 17:
        return 40
    elif age <= 64:
        return 120
    else:
        return 60

assert club_fee(4) == 0
assert club_fee(5) == 40
assert club_fee(17) == 40
assert club_fee(18) == 120
assert club_fee(64) == 120
assert club_fee(65) == 60
print("All six tests pass.")
```

Each test sits at the edge of a group, because that is where mistakes
hide. You could also write `elif between(age, 5, 17):` and so on. That
checks both ends every time, which is a little longer, but reads the same
as the fee table.

</details>

**7. Fix.** A weather app gives a wind warning. It should say "orange" for
wind over 80 km/h, and "yellow" for wind over 50 km/h. For 90 km/h it says
"yellow". Find the mistake, and fix it.

```python exec
id: mixed-decisions-fix-wind
def wind_warning(speed):
    if speed > 50:
        return "yellow"
    elif speed > 80:
        return "orange"
    else:
        return "none"

print(wind_warning(90))    # should be orange
print(wind_warning(60))    # should be yellow
print(wind_warning(20))    # should be none
```

<details class="dl-answer"><summary>answer</summary>

The checks are in the wrong order. Any speed over 80 is also over 50, so
the first check catches it, and the `elif speed > 80` line can never be
reached. Put the stronger warning first:

```python
def wind_warning(speed):
    if speed > 80:
        return "orange"
    elif speed > 50:
        return "yellow"
    else:
        return "none"
```

Now the three lines print `orange`, `yellow` and `none`. Nothing crashed
before the fix, and no error appeared. This kind of mistake only shows
when you test with the right numbers.

</details>

**8. Another way.** An office air conditioner beeps when the temperature
is outside 18 to 24 degrees. One way to write that is
`not between(temperature, 18, 24)`. Write it a second way with no `not`
and no `between`. Then check that the two agree for every whole-number
temperature from 0 to 40.

```python exec
id: mixed-decisions-air-con
# Two ways to write "outside 18 to 24", and a loop that compares them
```

<details class="dl-answer"><summary>answer</summary>

`between` is `18 <= temperature and temperature <= 24`. De Morgan's first
law puts a `not` on each part and changes `and` to `or`. A `not` in front
of a comparison turns it round. So the second way is
`temperature < 18 or temperature > 24`.

```python
for temperature in range(0, 41):
    first = not between(temperature, 18, 24)
    second = temperature < 18 or temperature > 24
    if first != second:
        print("Different at", temperature)
print("Checked 0 to 40.")
```

Only the last line prints, so the two agree everywhere the loop looked.

</details>

**9. Predict.** A library has two versions of its borrowing rule. Will
`same_rule` say they are the same? Decide first, then run it.

```python
def can_borrow_1(has_card, owes_fines, card_expired):
    return has_card and not (owes_fines or card_expired)

def can_borrow_2(has_card, owes_fines, card_expired):
    return has_card and not owes_fines and not card_expired

print(same_rule(can_borrow_1, can_borrow_2, 3))
```

<details class="dl-answer"><summary>answer</summary>

`True`. They are the same rule.

De Morgan's second law turns `not (owes_fines or card_expired)` into
`not owes_fines and not card_expired`. The `has_card and` in front is the
same in both. `same_rule` checks all eight rows and finds no difference.

</details>

**10. Fix.** A game controller sends each button press as a row of bits,
with a parity bit at the end. The console checks each row. This check
rejects every good row and accepts the bad ones. Find the mistake.

```python exec
id: mixed-decisions-fix-controller
def row_ok(received):
    """True when the row, parity bit included, has an even number of 1s."""
    return parity_bit(received) == 1

print(row_ok("10111"))    # message 1011, parity bit 1: should be True
print(row_ok("10011"))    # one bit flipped on the way: should be False
```

<details class="dl-answer"><summary>answer</summary>

The check compares with the wrong bit. The sender chose the parity bit to
make the count of 1s even. So a good row has an even count, and
`parity_bit` of an even count is 0, not 1:

```python
def row_ok(received):
    return parity_bit(received) == 0

print(row_ok("10111"))    # True: four 1s
print(row_ok("10011"))    # False: three 1s, so something flipped
```

The mistake turned every answer round, which is a clue in itself. When a
check is wrong every single time, look for a `0` that should be a `1`, or
a `==` that should be a `!=`.

</details>

**11. Explain.** A cinema uses this rule to let people in:

```python
def let_in(over_18, with_adult, has_ticket):
    return over_18 or with_adult and has_ticket
```

An adult with no ticket gets in. Why? What should the rule be?

<details class="dl-answer"><summary>answer</summary>

Python works out `and` before `or`. So the rule means
`over_18 or (with_adult and has_ticket)`. Anyone over 18 gets in, ticket
or not.

The rule should have brackets around the `or`:

```python
def let_in_fixed(over_18, with_adult, has_ticket):
    return (over_18 or with_adult) and has_ticket

print(same_rule(let_in, let_in_fixed, 3))    # False: they are different rules
print(let_in(True, False, False), let_in_fixed(True, False, False))
```

The last line prints `True False`: the first rule lets in an adult with no
ticket, and the fixed one does not.

</details>

**12. Make.** A fitness app calls a day "good" when the steps are from
8,000 to 30,000 and the hours of sleep are from 7 to 9. Write
`good_day(steps, sleep_hours)` using `between`, and test it with at least
three `assert` lines, one of them at an edge.

<details class="dl-answer"><summary>answer</summary>

```python
def good_day(steps, sleep_hours):
    """True when both steps and sleep are in their healthy ranges."""
    return between(steps, 8000, 30000) and between(sleep_hours, 7, 9)

assert good_day(10000, 8) == True
assert good_day(8000, 7) == True       # both edges count
assert good_day(12000, 6.5) == False   # too little sleep
assert good_day(5000, 8) == False      # too few steps
print("good_day keeps its promise.")
```

</details>

**13. Another way.** Find a shorter way to write `not (a ^ b)`, and check
it with `same_rule`.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. `a ^ b` is True when `a` and `b` are different.
2. So `not (a ^ b)` is True when they are ... what?
3. Python has a comparison that asks exactly that.

**Think about:** on [True, false and every case](tutorial:true-false-and-every-case),
which comparison did XOR turn out to be?

**Try this next:** what is `not (a == b)` the same as?

</details>

<details class="dl-answer"><summary>answer</summary>

`a == b`. XOR asks "are they different?", so `not` of it asks "are they
the same?".

```python
def not_xor(a, b):
    return not (a ^ b)

def same(a, b):
    return a == b

print(same_rule(not_xor, same, 2))    # True
```

</details>

## Stretch

A scratch cell for the stretch problems.

```python exec
id: mixed-decisions-scratch-3
# Try things here
```

**14. Make.** This unit's product is a quiz that marks answers and says
why. Write `mark_binary(number, answer)`. It takes a whole number and a
reader's answer, as a string of bits, and gives back a message:

- "Right." when the answer is `to_binary(number)`
- "Right number, but leave out the zeros at the front." when the answer is
  the right bits with zeros in front to make eight digits
- otherwise, a message that uses `parity_bit` to say whether an odd or an
  even number of bits are wrong, when the answer has the right length

Try it on 13, with the answers `"1101"`, `"00001101"`, `"1100"` and
`"1011"`.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Work out `right = to_binary(number)` first.
2. Use `if`, `elif` and `else`, from the most exact match to the least.
3. When two rows of bits of the same length differ in one bit, their
   parity bits differ. When they differ in two bits, their parity bits are
   the same.

**Think about:** why does the check for the right length have to come
before the parity message?

**Try this next:** add a branch for an answer that has the wrong number
of bits.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def mark_binary(number, answer):
    """Mark a reader's binary for number, and say why."""
    right = to_binary(number)
    if answer == right:
        return "Right."
    elif answer == format(number, "08b"):
        return "Right number, but leave out the zeros at the front."
    elif len(answer) != len(right):
        return "Not yet: " + right + " has " + str(len(right)) + " bits."
    elif parity_bit(answer) != parity_bit(right):
        return "Not yet: an odd number of bits are wrong. Check each column."
    else:
        return "Not yet: an even number of bits are wrong. Check each column."

print(mark_binary(13, "1101"))
print(mark_binary(13, "00001101"))
print(mark_binary(13, "1100"))
print(mark_binary(13, "1011"))
```

The four lines print "Right.", then the message about zeros, then "an odd
number" (one bit is wrong in `1100`), then "an even number" (two bits are
wrong in `1011`).

The order of the checks matters. The length check comes before the parity
checks, because the parity trick only makes sense for rows of the same
length.

</details>

**15. Explain.** On [Untangling a condition](tutorial:untangling-a-condition),
`same_rule` showed that `a and b` is the same rule as `b and a`. But these
two lines are not the same in a program. The second one raises an error on
purpose. Run it, read the last line of the error, and explain why the order
matters here.

```python exec
id: mixed-decisions-order-of-and
count = 0
total = 0
print(count != 0 and total / count > 5)
print(total / count > 5 and count != 0)
```

<details class="dl-answer"><summary>answer</summary>

The first line prints `False`. The second stops with
`ZeroDivisionError: division by zero`, the error from
[When Python says no](tutorial:when-python-says-no).

Python works out `and` from left to right, and it stops as soon as it
knows the answer. In the first line, `count != 0` is `False`, and
`False and` anything is `False`, so Python never does the division. In
the second line, the division comes first, and dividing by zero is not
allowed.

As rules on True and False, the two orders are the same: `same_rule` was
right. But a program is more than a rule. What happens when is part of
it, and the left part of an `and` can protect the right part.

</details>

**16. Make.** A band chooses songs by a vote of three members. A song is
in when at least two of the three vote yes. Write `majority(a, b, c)`
using `and` and `or`, print its truth table, and check with `same_rule`
that it is the same rule as `a + b + c >= 2`.

<details class="dl-answer"><summary>answer</summary>

At least two means one of the three pairs is both yes:

```python
def majority(a, b, c):
    return (a and b) or (a and c) or (b and c)

def majority_by_counting(a, b, c):
    return a + b + c >= 2

truth_table(majority, ["a", "b", "c"])
print(same_rule(majority, majority_by_counting, 3))    # True
```

The counting version works because Python treats `True` as 1 and `False`
as 0 when it adds them. It is another way to reach the same rule: one
reads as logic, the other as arithmetic.

</details>

**17. Another way.** A light is toggled with `light = not light`. Write a
second version that uses `^`, and check with `same_rule` (with a `count`
of 1) that the two are the same rule.

<details class="dl-answer"><summary>answer</summary>

XOR with `True` flips a value, the same way XOR with 1 flips a bit:

```python
def toggle_with_not(light):
    return not light

def toggle_with_xor(light):
    return light ^ True

print(same_rule(toggle_with_not, toggle_with_xor, 1))    # True
```

A rule with one input has only two rows, and `same_rule` checks both.

</details>

**18. Predict.** Using your toolkit from both units, what do these two
lines print? Work each one out by hand first.

```python
print(parity_bit(to_binary(255)))
print(to_hex(0x0F ^ 0xFF))
```

<details class="dl-answer"><summary>answer</summary>

`0` and then `F0`.

255 is `11111111`, eight 1s. Eight is even, so the parity bit is 0.

`0x0F` is `00001111` and `0xFF` is `11111111`. XOR with all 1s flips every
bit, so the result is `11110000`, which is `F0` in hex.

</details>
