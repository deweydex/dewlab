---
title: "Mixed problems: decisions and logic"
practice_across:
  - choosing-a-path
  - true-false-and-every-case
  - untangling-a-condition
  - bits-that-flip
year: "2026-2027"
version: 2026.09.25.1
---

# Mixed problems: decisions and logic

Each problem here draws on at least one page of Unit 2, and many draw on
two or more. None of them is harder than what those pages covered. The new
part is that nobody tells you which page a problem comes from. You
choose the tool as part of the problem.

Your toolkit is loaded on this page: `between`, `truth_table`,
`same_rule` and `parity_bit` from this unit, and `to_binary` and `to_hex`
from Unit 1. Each answer is hidden until you open it. Where a problem asks
you to predict, make the prediction before you run anything. It is the
most useful part.

If a problem feels hard, that is usually the feeling of choosing a tool,
which is the new skill here. Skip it, try another, and come back. The
answers show one answer to each. Yours may be different and work too.

## Warm-up

Use this cell for any warm-up problem. Change the line, and run it.

```python exec
id: mixed-decisions-scratch-1
print(between(35.5, 0, 35))
```

**1. Predict.** A phone is designed to work from 0 °C to 35 °C, and a
program checks `between(temperature, 0, 35)`. Another rule warns at "36
and over". What does `between` give for a reading of 35.5?

<details class="dl-answer"><summary>answer</summary>

`False`, because 35.5 is more than 35.

The two rules assume whole degrees, and in that space there is nothing
between 35 and 36. A sensor that reads tenths finds a gap. 35.5 is not
"0 to 35", and it is not "36 and over" either. On
[Choosing a path](tutorial:choosing-a-path), that assumption was stated in
"the space we're in". This problem shows why.

</details>

**2. Predict.** What does `True and not False or False` give? Say which
part Python does first.

<details class="dl-answer"><summary>answer</summary>

`True`.

`not` goes first, so `not False` is `True`. Then `and` gives
`True and True`, which is `True`. Then `or` gives `True or False`, which
is `True`. With brackets, Python reads
it as `(True and (not False)) or False`.

</details>

**3. Make.** An office printer can take a new job when
`not (busy or out_of_paper)`. Write it as a function, `printer_ready`, and
print its truth table with `truth_table`. In how many rows is the printer
ready?

<details class="dl-answer"><summary>answer</summary>

```python
def printer_ready(busy, out_of_paper):
    return not (busy or out_of_paper)

truth_table(printer_ready, ["busy", "out_of_paper"])
```

The printer is ready in one row only, when it is not busy and not out
of paper.
That is De Morgan's second law, from
[Untangling a condition](tutorial:untangling-a-condition):
`not (busy or out_of_paper)` is `not busy and not out_of_paper`.

</details>

**4. Predict.** What is `6 ^ 3`? Find it in binary first.

<details class="dl-answer"><summary>answer</summary>

5.

6 is `110` and 3 is `011`. Look at each column. 1 and 0 differ, so the
result is 1. 1 and 1 are the same, so it is 0. 0 and 1 differ, so it is
1. That gives `101`, which is 5.

</details>

**5. Explain.** Schlomi, who is learning Python too, says that
`temperature > 79` and `temperature >= 80` always mean the same thing, so
it does not matter which one the fan code uses. Where does her idea
work, and where does it stop working?

<details class="dl-answer"><summary>answer</summary>

Schlomi's idea works when the sensor gives whole degrees. Then there is
nothing between 79 and 80, so "more than 79" and "80 or more" pick out
the same readings.

With decimals, they differ. A reading of 79.5 is more than 79, but it is
not 80 or more. So Schlomi's move works in one space and not in the
other. It holds, as long as she says which space she is in.

</details>

## Core

A scratch cell for the core problems.

```python exec
id: mixed-decisions-scratch-2
# Try things here
```

**6. Make.** A phone draws its battery icon from the battery level, a
whole number from 0 to 100. From 0 to 10 it shows "empty". From 11 to 40
it shows "low". From 41 to 80 it shows "half". From 81 to 100 it shows
"full". Write `battery_icon(level)` with `if`, `elif` and `else`, and test
it with `assert` at 10, 11, 40, 41, 80 and 81.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Start with the lowest band, and work up.
2. Each `elif` only runs if every check above it was False, so you do not
   need to check the low end of each band again.
3. The tests are at the edges of the bands, where a `<` in place of a
   `<=` would hide.

**Think about:** could you write it with `between` for each band
instead? Which version reads more like the list of bands?

**Try this next:** add a "charging" icon that wins over all the others
when the phone is plugged in.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def battery_icon(level):
    """Return the icon for a battery level from 0 to 100."""
    if level <= 10:
        return "empty"
    elif level <= 40:
        return "low"
    elif level <= 80:
        return "half"
    else:
        return "full"

assert battery_icon(10) == "empty"
assert battery_icon(11) == "low"
assert battery_icon(40) == "low"
assert battery_icon(41) == "half"
assert battery_icon(80) == "half"
assert battery_icon(81) == "full"
print("All six tests pass.")
```

Each test sits at the edge of a band, because mistakes
hide there. You could also write `elif between(level, 11, 40):` and so on. That
checks both ends every time, which is a little longer, but reads the same
as the list of bands.

</details>

**7. Fix.** A weather app gives a wind warning. It should say "orange" for
wind over 80 km/h, and "yellow" for wind over 50 km/h. (The limits here
are invented.) For 90 km/h it says "yellow". Find why, and change it.

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

<aside class="dl-note" id="mixed-decisions-note-eowyn">

**Red for every county.** Met Éireann's warnings go from yellow to
orange to red. For 24 January 2025, the day of Storm Éowyn, it gave a
red warning for the whole country. A gust of 184 km/h was measured at
Mace Head in County Galway, the strongest gust ever recorded in
Ireland. The old record, 182 km/h at Foynes in 1945, had stood for 80
years.

</aside>

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
rejects every good row and accepts the bad ones. Find why.

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

**11. Explain.** A web forum lets you post if you are a member or you
have a guest code, and you are not banned. Its rule is:

```python
def can_post(is_member, has_code, not_banned):
    return is_member or has_code and not_banned
```

A banned member can still post. Why? What should the rule be?

<details class="dl-answer"><summary>answer</summary>

Python does `and` before `or`. So the rule means
`is_member or (has_code and not_banned)`. Any member can post, banned or
not.

The rule should have brackets around the `or`:

```python
def can_post_fixed(is_member, has_code, not_banned):
    return (is_member or has_code) and not_banned

print(same_rule(can_post, can_post_fixed, 3))    # False: they are different rules
print(can_post(True, False, False), can_post_fixed(True, False, False))
```

The last line prints `True False`. The first rule lets a banned member
post, and the fixed one does not.

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
which comparison was XOR the same as?

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

**14. Make.** This unit's product is a quiz that compares an answer with
`to_binary` and says how the two differ, without marking anyone. Write
`compare_binary(number, answer)`. It takes a whole number and a reader's
answer, as a string of bits, and returns a message:

- "The same bits as to_binary." when the answer is `to_binary(number)`
- "The same number, with zeros in front; to_binary leaves them out." when
  the answer is those bits with zeros in front to make eight digits
- when the answer has a different length, a message saying how many bits
  `to_binary` gives
- otherwise, a message that uses `parity_bit` to say whether an odd or an
  even number of bits differ

Try it on 13, with the answers `"1101"`, `"00001101"`, `"1100"` and
`"1011"`.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Set `bits = to_binary(number)` first.
2. Use `if`, `elif` and `else`, from the most exact match to the least.
3. When two rows of bits of the same length differ in one bit, their
   parity bits differ. When they differ in two bits, their parity bits are
   the same.

**Think about:** why does the check for the right length have to come
before the parity message?

**Try this next:** say which columns differ, not only how many.

</details>

<details class="dl-answer"><summary>one answer</summary>

```python
def compare_binary(number, answer):
    """Say how a reader's binary for number differs from to_binary's."""
    bits = to_binary(number)
    if answer == bits:
        return "The same bits as to_binary."
    elif answer == format(number, "08b"):
        return "The same number, with zeros in front; to_binary leaves them out."
    elif len(answer) != len(bits):
        return "A different length: to_binary gives " + str(len(bits)) + " bits, " + bits + "."
    elif parity_bit(answer) != parity_bit(bits):
        return "The same length; an odd number of bits differ. Compare each column."
    else:
        return "The same length; an even number of bits differ. Compare each column."

print(compare_binary(13, "1101"))
print(compare_binary(13, "00001101"))
print(compare_binary(13, "1100"))
print(compare_binary(13, "1011"))
```

The four lines print "The same bits as to_binary.", then the message about
zeros, then "an odd number" (one bit differs in `1100`), then "an even
number" (two bits differ in `1011`). Yours may word the messages another
way and work as well.

The order of the checks matters. The length check comes before the parity
checks, because the parity trick only makes sense for rows of the same
length.

</details>

**15. Explain.** On [Untangling a condition](tutorial:untangling-a-condition),
`same_rule` showed that `a and b` is the same rule as `b and a`. So
Schlomo, who is learning Python too, says the order inside an `and` never
matters. But these two lines
are not the same in a program. The second one raises an error on
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

Python reads `and` from left to right, and it stops as soon as it
knows the answer. In the first line, `count != 0` is `False`, and
`False and` anything is `False`, so Python never does the division. In
the second line, the division comes first, and Python cannot divide by
zero.

As rules on True and False, the two orders are the same. What
`same_rule` showed is true in that space, and so is Schlomo's idea. But a program is more than a
rule. What happens when is part of
it, and the left part of an `and` can protect the right part.

</details>

**16. Make.** A satellite has three temperature sensors on one panel.
Each says True when it reads "too hot". So that one broken sensor cannot
fool it, the satellite believes "too hot" when at least two of the three
say so. Write `majority(a, b, c)` using `and` and `or`, print its truth
table, and check with `same_rule` that it is the same rule as
`a + b + c >= 2`.

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
as 0 when it adds them. It is another way to reach the same rule. One
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
lines print? Find each one by hand first.

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
