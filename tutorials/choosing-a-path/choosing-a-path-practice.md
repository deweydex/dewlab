---
title: "Choosing a path: if, elif and else — Practice"
practice_for: choosing-a-path
year: "2026-2027"
version: 2026.09.24.1
---

# Choosing a path: if, elif and else — Practice

Each problem says what kind it is. **Predict** means guess first, then
run. **Make** means write something new. **Fix** means find one mistake
in code that looks fine. **Explain** means answer in words. **Another
way** means reach the same place by a second route. The answers are
folded away until you open them.

## Warm-up

Use this cell for any of the warm-up problems.

```python exec
id: choosing-practice-warm-up
# Try things here
```

**1. Predict.** Last night's lowest temperatures were $-1$ degrees in
Galway and $-4$ degrees in Mullingar. What does each line print?

```python
print(-1 < -4)
print(-1 != -4)
print(10 >= 10)
```

<details class="dl-answer"><summary>answer</summary>

`False`, `True`, `True`.

$-1$ is closer to zero than $-4$, so it sits to the right on the number
line: $-1$ is greater, and `-1 < -4` is False. The two numbers are
different, so `!=` gives True. And `10 >= 10` is True, because `>=`
includes the value itself.

</details>

**2. Make.** A playlist app puts a "short" label on any song under three
minutes. The length of a song is in `song_seconds`. Write the condition
that is True for a short song, and try it with 175 and with 180.

<details class="dl-answer"><summary>answer</summary>

```python
song_seconds = 175
print(song_seconds < 180)

song_seconds = 180
print(song_seconds < 180)
```

This prints `True`, then `False`. Three minutes is 180 seconds. "Under"
leaves 180 itself out, so the sign is `<`, not `<=`.

</details>

**3. Explain.** A match report program has these two lines. What does
each one do?

```python
home_score = 2
home_score == 2
```

<details class="dl-answer"><summary>answer</summary>

The first line names a value: from now on `home_score` stands for 2.

The second line asks a question: "is `home_score` equal to 2?" Its answer
is `True`. It changes nothing. One equals sign names; two equals signs
ask.

</details>

**4. Another way.** A fun-fair ride says "riders must be taller than
119 cm". One program checks `height > 119`. Another checks
`height >= 120`. Are they the same? Is there a space where they are, and
a space where they are not?

<details class="dl-answer"><summary>answer</summary>

If heights are measured in whole centimetres, the two are the same: the
only whole numbers above 119 are 120, 121 and so on.

If heights can have decimals, they are different. A child of 119.5 cm is
taller than 119 cm, so `height > 119` lets them on, but `height >= 120`
does not.

```python
height = 119.5
print(height > 119)
print(height >= 120)
```

This prints `True`, then `False`. Neither program is wrong. Each is right
in its own space, and the ride's sign should say which space it means.

</details>

## Core

A cell for checking your answers to problems 5 and 6.

```python exec
id: choosing-practice-core-checks
# Check your inequality answers here
```

**5. Make.** A music shop sells downloaded albums at €9 each. A streaming
service costs €11 a month. For how many albums a month is the streaming
service cheaper? Write the inequality, solve it, and check your answer
with code at the number of albums on either side.

<details class="dl-answer"><summary>answer</summary>

In words: streaming is cheaper when the albums would cost more than €11.
Let $a$ be the number of albums:

$$9a > 11$$

Divide both sides by 9:

$$a > 1.22\ldots$$

Albums are whole numbers, so streaming is cheaper from 2 albums a month.

```python
album_price = 9
streaming = 11

albums = 1
print(albums, album_price * albums > streaming)
albums = 2
print(albums, album_price * albums > streaming)
```

This prints `1 False`, then `2 True`.

</details>

**6. Make.** A runner starts with 750 ml of water and drinks about 60 ml
each kilometre. She wants at least 150 ml left for the end. For how many
kilometres $k$ is that true? Solve $750 - 60k \ge 150$, and check your
answer on both sides of it.

<details class="dl-answer"><summary>answer</summary>

$$750 - 60k \ge 150$$

Subtract 750 from both sides:

$$-60k \ge -600$$

Divide both sides by $-60$. Dividing by a negative number turns the sign
round:

$$k \le 10$$

```python
water = 750
per_km = 60

km = 10
print(km, water - per_km * km >= 150)
km = 11
print(km, water - per_km * km >= 150)
```

This prints `10 True`, then `11 False`. At 10 km she has exactly 150 ml,
and "at least" includes 150.

**Another route:** add $60k$ to both sides first: $750 \ge 150 + 60k$,
so $600 \ge 60k$, so $10 \ge k$. No negative number is needed.

</details>

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Move the 750 first: subtract it from both sides.
2. You now divide by a negative number. What does that do to $\ge$?
3. Check with $k = 10$ and $k = 11$ in the cell.

**Think about:** why $-3 > -5$, even though $3 < 5$.

**Try this next:** with 1,000 ml and the same 150 ml left over, how far
can she run?

</details>

**7. Predict.** QQI marks a component with these grades. What does the
cell print for a mark of 80? For 79.5? For 50? For 49?

```python
def grade_for(mark):
    """Return the QQI grade for a mark out of 100."""
    if mark >= 80:
        return "Distinction"
    elif mark >= 65:
        return "Merit"
    elif mark >= 50:
        return "Pass"
    else:
        return "Unsuccessful"

print(grade_for(80))
print(grade_for(79.5))
print(grade_for(50))
print(grade_for(49))
```

<details class="dl-answer"><summary>answer</summary>

`Distinction`, `Merit`, `Pass`, `Unsuccessful`.

80 passes the first check. 79.5 fails it and passes the second, even
though it is only half a mark away. 50 is the lowest Pass, because `>=`
includes 50. 49 fails every condition, so `else` catches it.

</details>

**8. Fix.** A weather app gives a wind warning from the strongest gust
it expects, in km/h. (The limits here are made up.) The app never shows
an orange or a red warning, even in a storm. Run it, then find and fix
the mistake.

```python exec
id: choosing-practice-fix-wind
def wind_warning(gust_kmh):
    """Return the warning colour for a gust speed in km/h."""
    if gust_kmh >= 65:
        return "yellow"
    elif gust_kmh >= 100:
        return "orange"
    elif gust_kmh >= 130:
        return "red"
    else:
        return "no warning"

print(wind_warning(50))
print(wind_warning(80))
print(wind_warning(110))
print(wind_warning(140))
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Take a gust of 140 km/h. Which condition does Python check first?
2. Is that condition True for 140?
3. What happens to every `elif` after the first True condition?

**Think about:** every gust that is 130 or more is also 65 or more.

**Try this next:** could you fix it by changing the signs instead of the
order?

</details>

<details class="dl-answer"><summary>answer</summary>

The checks are in the wrong order. Any gust of 100 or more is also 65 or
more, so the first condition catches it and the other two lines are
never reached. Put the biggest limit first:

```python
def wind_warning(gust_kmh):
    """Return the warning colour for a gust speed in km/h."""
    if gust_kmh >= 130:
        return "red"
    elif gust_kmh >= 100:
        return "orange"
    elif gust_kmh >= 65:
        return "yellow"
    else:
        return "no warning"
```

Now the four lines print `no warning`, `yellow`, `orange`, `red`.

</details>

**9. Make.** In a club's 400 m race, a time of 60 seconds or less wins
gold, 65 or less wins silver, 70 or less wins bronze, and anything slower
wins no medal. Write `medal_for(seconds)`, and test it with `assert` at
60, 60.5, 70 and 71.

```python exec
id: choosing-practice-medal
# Your medal_for, and its tests
```

<details class="dl-answer"><summary>answer</summary>

```python
def medal_for(seconds):
    """Return the medal for a 400 m time in seconds."""
    if seconds <= 60:
        return "gold"
    elif seconds <= 65:
        return "silver"
    elif seconds <= 70:
        return "bronze"
    else:
        return "no medal"

assert medal_for(60) == "gold"
assert medal_for(60.5) == "silver"
assert medal_for(70) == "bronze"
assert medal_for(71) == "no medal"
print("All tests pass.")
```

Here a smaller number is better, so the smallest limit goes first. The
tests sit at the ends of the ranges, where a `<` in place of `<=` would
show up.

</details>

**10. Explain.** A student writes the grade rules with three separate
`if` lines instead of `if` and `elif`. What does this print, and why?

```python
mark = 90
if mark >= 80:
    print("Distinction")
if mark >= 65:
    print("Merit")
if mark >= 50:
    print("Pass")
```

<details class="dl-answer"><summary>answer</summary>

It prints all three: `Distinction`, `Merit` and `Pass`.

Each `if` starts a new question, and Python asks every one of them. 90
is more than 80, more than 65 and more than 50, so every answer is True.
With `elif`, the three checks belong to one question, and Python stops at
the first True answer. That is the difference between three separate
choices and one choice with three paths.

</details>

**11. Fix.** A home heating app says a room is comfortable from 18 to 22
degrees, both included. The tests stop with an error. Run the cell, read
the last line of the error, and fix the function.

```python exec
id: choosing-practice-fix-comfort
def comfortable(temperature):
    """Return True when the temperature is from 18 to 22 degrees, both included."""
    return 18 < temperature < 22

assert comfortable(20) == True
assert comfortable(18) == True
assert comfortable(22) == True
assert comfortable(17.5) == False
assert comfortable(23) == False
print("All tests pass.")
```

<details class="dl-answer"><summary>answer</summary>

The error is an `AssertionError` on the line `assert comfortable(18) ==
True`. The promise says 18 is included, but `18 < 18` is False. Use
`<=` on both sides:

```python
def comfortable(temperature):
    """Return True when the temperature is from 18 to 22 degrees, both included."""
    return 18 <= temperature <= 22
```

Now every test passes. The mistake only showed up because two tests sit
exactly on the ends.

</details>

## Stretch

This cell gives the page `between` from the tutorial, so the stretch
problems can use it. Run it first.

```python exec
id: choosing-practice-stretch-tools
def between(value, low, high):
    """Return True when low <= value <= high, with both ends included."""
    return low <= value <= high

print("between is ready.")
```

**12. Predict.** One colour byte can be from 0 to 255, and a dice roll
from 1 to 6. What does each line print? The last one is a puzzle.

```python
print(between(255, 0, 255))
print(between(256, 0, 255))
print(between(0, 1, 6))
print(between(5, 10, 1))
```

<details class="dl-answer"><summary>answer</summary>

`True`, `False`, `False`, `False`.

255 is the top end, and the ends count. 256 is one past it: too big for
one byte. 0 is not a dice roll.

The last line gives False because `low` is 10 and `high` is 1. No number
is both 10 or more and 1 or less, so this `between` is False for every
value. The function keeps its promise; the promise assumes `low` is not
bigger than `high`.

</details>

**13. Make.** Some restaurants add a 12.5% service charge for a group of
6 or more. Use `split_bill` from your toolkit to write
`share_for(total, people)`: each person's share, with 12.5% added for a
group of 6 or more, and nothing added for a smaller group. A bill of
€180 for 6 people should give 33.75 each. A bill of €120 for 4 people
should give 30.0 each.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Look at the promise of `split_bill`. Its third input is a percentage
   to add.
2. Which condition says "6 or more"?
3. One branch calls `split_bill` with 12.5 as the third input. The other
   calls it without one.

**Think about:** why 6 people get the charge but 5 do not. Which sign
makes that true?

**Try this next:** add a third path: groups of 10 or more pay 15%.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def share_for(total, people):
    """Each person's share, with 12.5% added for a group of 6 or more."""
    if people >= 6:
        return split_bill(total, people, 12.5)
    else:
        return split_bill(total, people)

print(share_for(180, 6))
print(share_for(120, 4))
```

This prints `33.75`, then `30.0`. For 6 people: €180 plus 12.5% is
€202.50, and €202.50 shared by 6 is €33.75.

</details>

**14. Another way.** The tutorial's `between` used two comparisons in one
line. Write `between_again(value, low, high)` that keeps the same promise
using `if`, `elif` and `else` instead, with one comparison on each line.
Then check that it agrees with `between` for the values 0, 1, 5, 6 and 7,
with `low` 1 and `high` 6.

<details class="dl-answer"><summary>answer</summary>

```python
def between_again(value, low, high):
    """Return True when low <= value <= high, with both ends included."""
    if value < low:
        return False
    elif value > high:
        return False
    else:
        return True

assert between_again(0, 1, 6) == between(0, 1, 6)
assert between_again(1, 1, 6) == between(1, 1, 6)
assert between_again(5, 1, 6) == between(5, 1, 6)
assert between_again(6, 1, 6) == between(6, 1, 6)
assert between_again(7, 1, 6) == between(7, 1, 6)
print("They agree.")
```

It prints `They agree.` The value is outside when it is too small or too
big. Every other value is inside. Two different routes, one promise.

</details>

**15. Make.** On
[Everything is ones and zeros](tutorial:everything-is-ones-and-zeros)
we saw that one byte holds $2^8 = 256$ different values. Two bytes hold
$2^{16}$, three hold $2^{24}$ and four hold $2^{32}$. Write
`bytes_needed(count)`, which gives the fewest bytes (1 to 4) that can
give every one of `count` things its own number. The 2022 census counted
5,149,139 people in Ireland. How many bytes would give each person a
number?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Start with the smallest: if `count <= 2 ** 8`, one byte is enough.
2. Each `elif` tries one more byte.
3. The order matters: which check has to come first?

**Think about:** why the check is `<=` and not `<`. How many different
values does one byte hold?

**Try this next:** how many bytes for every person on Earth, about 8
billion?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def bytes_needed(count):
    """Return the fewest bytes, from 1 to 4, that give count things a number each."""
    if count <= 2 ** 8:
        return 1
    elif count <= 2 ** 16:
        return 2
    elif count <= 2 ** 24:
        return 3
    else:
        return 4

print(bytes_needed(256))
print(bytes_needed(257))
print(bytes_needed(5149139))
```

This prints `1`, `2` and `3`. $2^{16}$ is 65,536, far too few for
Ireland. $2^{24}$ is 16,777,216, which is enough. Four bytes hold
4,294,967,296 values, so 8 billion people would need more than this
function allows: the promise only covers up to four bytes.

</details>

**16. Explain.** The tutorial page taught solving an inequality and
choosing a path with `if` on one page. In many schools they would belong to
two subjects. Think of one person: someone who likes maths and not
computers, or someone who likes computers and not maths. It can be you. For
that person, would one page with both, or two separate pages, work better?
Why?

<details class="dl-answer"><summary>answer</summary>

There is no one right answer, and your own experience counts as
evidence here. A good answer weighs a few things.

- **One page with both.** Each side explains the other: the number line
  makes sense of `<=`, and the code checks the algebra. The cost: two new
  things arrive at once, and the page is longer. Someone who dislikes one
  side meets it anyway.
- **Two separate pages.** Each one can go at its own speed, and a reader
  who is nervous about one subject can take it on its own. The cost: the
  link between the two may never be made, and one of them can feel like a
  topic with no use.

For the maths lover, the code may be a way to check their work. For the
computer lover, the maths may be the reason `elif` needs its order. A
strong answer says which of these fits the person you chose.

</details>
