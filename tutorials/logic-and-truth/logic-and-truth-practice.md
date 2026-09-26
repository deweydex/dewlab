---
title: "Logic: truth tables, XOR and De Morgan's laws — Practice"
practice_for: logic-and-truth
year: "2026-2027"
version: 2026.09.26.1
worlds:
  games-of-chance: Dice, cards and coins, and the games people play with them.
  dinosaurs: Dinosaurs and their fossils, what has been found, where, and how old it is.
  exoplanets: Planets around other stars, and the ways they were found.
datasets: [dinosaur-finds, exoplanets]
---

# Logic: truth tables, XOR and De Morgan's laws — Practice

Here are problems on truth tables, exclusive or and De Morgan's laws,
and three from earlier pages. Several ask you to predict a table before
you make it. The prediction is the exercise, so try it first.

## Tools

This cell defines `table()`, which prints the truth table for any
function of two inputs. Give it the name of a function, without
brackets, and it calls the function for each of the four rows.

```python exec
id: tools-1
def table(rule, names=("A", "B")):
    """Print a truth table for a function of two True-or-False inputs."""
    print(f"{names[0]:>5}   {names[1]:>5}      result")
    for a in [True, False]:
        for b in [True, False]:
            print(f"{str(a):>5}   {str(b):>5}      {str(rule(a, b)):>5}")


def both(a, b):
    return a and b


table(both)
```

## Truth tables

**1.** How many rows does a truth table have for three inputs? For $n$
inputs?

<details class="dl-answer"><summary>answer</summary>

Eight, and $2^n$. Each new input doubles the number of cases. So checking
every case soon takes too long: twenty inputs give over a million rows.

</details>

```question
id: logic-how-many-rows-true
type: fill-in-the-blank

- `A or B` is true in {three|one|two|four} of the four rows.
- `A and B` is true in {one|three|two|four} of the four rows.
```

**2.** Logic has a rule it calls "if A then B", written `(not A) or B`.
Can you make its table with `table()`, and find the only row where it is
`False`?

```python exec
id: logic-if-then
def if_then(a, b):
    """True unless a is True and b is False."""
    # Your code here


table(if_then)
```

```inputs
[if_then(a, b) for a in [True, False] for b in [True, False]]
```

```hint
Write the rule exactly as given: `(not a) or b`. Then read down the table.
Which row has `False`?
```

```solution
def if_then(a, b):
    """True unless a is True and b is False."""
    return (not a) or b


table(if_then)
---
It is `False` in one row only: A true and B false. "If it rains, the
ground is wet" is only broken by rain on dry ground. When A is false, the
rule says nothing, so logic counts it as kept. "If it rains" makes no
promise about a dry day. Most people find this part strange, and the
four-card challenge on the tutorial page depends on it.
```

**3.** How is the logical `or` different from the everyday one?

<details class="dl-answer"><summary>answer</summary>

The logical `or` is true when both inputs are true. In everyday English,
"tea or coffee?" usually means one or the other, not both. The everyday
meaning is exclusive or, which Python has no keyword for.

</details>

## Exclusive or

**4.** Can you write XOR using only `and`, `or` and `not`?

<details class="dl-answer"><summary>answer</summary>

`(a or b) and not (a and b)`, which means "at least one, but not both".
Another way is `(a and not b) or (b and not a)`, which lists the two
rows where XOR is true.

</details>

**5.** `^` also works on whole numbers, one binary digit at a time, and
XOR with the same key twice undoes itself: `x ^ key ^ key` is `x` again.
Can you use that to scramble a message and unscramble it?

```python exec
id: logic-xor-secret
key = 42


def scramble(message, key):
    """Return a list of numbers: each character's code, XORed with key."""
    # Your code here


def unscramble(numbers, key):
    """Return the message that scramble made these numbers from."""
    # Your code here


hidden = scramble("MEET AT NOON", key)
print(hidden)
print(unscramble(hidden, key))
```

```inputs
scramble("HI", key)
unscramble(scramble("MEET AT NOON", key), key)
unscramble(scramble("MEET AT NOON", key), 7)
```

```hint
`ord(letter)` gives a character's code, and `chr(number)` changes a code
into a character. To scramble, use `ord(letter) ^ key` for each letter.
To unscramble, use the same XOR again, then `chr`.
```

```solution
key = 42


def scramble(message, key):
    """Return a list of numbers: each character's code, XORed with key."""
    numbers = []
    for letter in message:
        numbers.append(ord(letter) ^ key)
    return numbers


def unscramble(numbers, key):
    """Return the message that scramble made these numbers from."""
    message = ""
    for number in numbers:
        message = message + chr(number ^ key)
    return message


hidden = scramble("MEET AT NOON", key)
print(hidden)
print(unscramble(hidden, key))
---
The same operation works both ways. XOR with the key hides a letter,
and XOR with the key again undoes it. With the wrong key, in the last
input, the message is nonsense. Real encryption is far stronger, but
much of it still uses XOR.
```

## De Morgan

```question
id: logic-de-morgan-rewrites
type: fill-in-the-blank

- `not (A and B)` is the same as {(not A) or (not B)|(not A) and (not B)}.
- `not (A or B)` is the same as {(not A) and (not B)|(not A) or (not B)}.
- `not (not a or not b)` is the same as {a and b|a or b}.
```

**6.** Why is a loop over four rows a *proof* here, when "I tested it and
it worked" usually is not?

<details class="dl-answer"><summary>answer</summary>

There are exactly four possible inputs, and the loop tried all of them.
For almost anything else, such as a function that takes whole numbers,
the inputs never end, and a test can only fail to find a problem. A
loop over every case proves a rule only when there are few enough cases
to check them all.

</details>

## Readability

**7.** A system logs an error when `not (status == "ok" and errors == 0)`.
Can you rewrite it so a reader sees what causes a log entry?

<details class="dl-answer"><summary>answer</summary>

`status != "ok" or errors != 0`. The status is not "ok", or there are
errors.

</details>

**8.** Can you rewrite `not (age >= 18 and has_id)`?

<details class="dl-answer"><summary>answer</summary>

`age < 18 or not has_id`. `not (age >= 18)` is `age < 18`, not
`age <= 18`. A boundary that is wrong by one is an *off-by-one error*,
one of the most common slips in conditions.

</details>

**9.** Here is De Morgan in real data. A pandas filter uses `&` for and,
`|` for or, and `~` for not, each on a whole column at once.

<div class="dl-world" data-world="exoplanets">

`~(big | far)` keeps the planets that are not (more than 2 Earths across
or 100 light-years or more away). Can you set `rewritten` to the same
filter with `<=` and `<`, and no `~` at all, and compare the counts?

```python exec
id: logic-pandas--exoplanets
planets = await load_csv("exoplanets.csv")
big = planets.radius_earths > 2
far = planets.distance_ly >= 100
print(len(planets[~(big | far)]), "planets kept by ~(big | far)")

rewritten = planets[planets.radius_earths > 0]   # change this line
print(len(rewritten), "planets kept by the rewrite")
```

```inputs
len(rewritten)
```

```solution
planets = await load_csv("exoplanets.csv")
big = planets.radius_earths > 2
far = planets.distance_ly >= 100
print(len(planets[~(big | far)]), "planets kept by ~(big | far)")

rewritten = planets[(planets.radius_earths <= 2) & (planets.distance_ly < 100)]
print(len(rewritten), "planets kept by the rewrite")
---
The counts are 196 and 164, with the copy saved on
{{snapshot: exoplanets}}. De Morgan's law still holds. `~big & ~far`
keeps 196 too. The difference comes from changing `~big` into
`radius_earths <= 2`. A planet with no radius in the file has
`nan`, and `nan > 2` and `nan <= 2` are both `False`, so `~big` is `True`
for it and `<= 2` is `False`. The two filters disagree on 32 planets,
each with a missing radius or distance. With missing values, "not bigger
than 2" and "at most 2" are different questions.
```

</div>

<div class="dl-world" data-world="dinosaurs">

`~(from_us | older)` keeps the finds that are neither from the United
States nor from rock older than 150 million years. Can you set
`rewritten` to the same filter with De Morgan's law, and check that the
counts match?

```python exec
id: logic-pandas--dinosaurs
finds = await load_csv("dinosaur-finds.csv", keep_default_na=False)
from_us = finds.country_code == "US"
older = finds.oldest_mya > 150
print(len(finds[~(from_us | older)]), "finds kept by ~(from_us | older)")

rewritten = finds[from_us]   # change this line
print(len(rewritten), "finds kept by the rewrite")
```

```inputs
len(rewritten)
```

```solution
finds = await load_csv("dinosaur-finds.csv", keep_default_na=False)
from_us = finds.country_code == "US"
older = finds.oldest_mya > 150
print(len(finds[~(from_us | older)]), "finds kept by ~(from_us | older)")

rewritten = finds[~from_us & ~older]
print(len(rewritten), "finds kept by the rewrite")
---
Both counts are 3,385, with the copy saved on {{snapshot: dinosaur-finds}}.
In pandas, `&` and `|` bind more tightly than `==` or `>`. So the cell
builds `from_us` and `older` first, as columns of `True` and
`False`. Written in one line, each comparison needs its own brackets.
```

</div>

<div class="dl-world" data-world="games-of-chance">

A dice game pays you unless the roll is a double or adds up to more than
9. Can you count the paying rolls a second way, with De Morgan's law,
and check the counts agree?

```python exec
id: logic-pandas--games-of-chance
rolls = [(a, b) for a in range(1, 7) for b in range(1, 7)]

as_written = 0
rewritten = 0
for a, b in rolls:
    if not (a == b or a + b > 9):
        as_written = as_written + 1
    # Add one to rewritten here, with no "not" outside a bracket

print(as_written, rewritten)
```

```inputs
rewritten
```

```solution
rolls = [(a, b) for a in range(1, 7) for b in range(1, 7)]

as_written = 0
rewritten = 0
for a, b in rolls:
    if not (a == b or a + b > 9):
        as_written = as_written + 1
    if a != b and a + b <= 9:
        rewritten = rewritten + 1

print(as_written, rewritten)
---
Both ways give 26. 6 doubles and 6 rolls over 9 would be 12, but (5, 5)
and (6, 6) are both, so 10 rolls do not pay, and 36 - 10 = 26 pay.
`not (a + b > 9)` is `a + b <= 9`, never `< 9`, as in problem 8.
```

</div>

## One longer one

**10.** A door unlocks when all three of these are true: the card is valid;
it is during working hours, or the person is a manager; and the door is
not in lockdown.

- (a) Can you write it as a Python expression?
- (b) A colleague writes the "does not unlock" case as
  `not valid or not (hours or manager) or lockdown`. Does it match?
- (c) Can you simplify the middle part of their expression?

<details class="dl-answer"><summary>answer</summary>

(a) `valid and (hours or manager) and not lockdown`.

(b) Yes. De Morgan's law turns a `not` around three things joined by
`and` into three `not`s joined by `or`, and `not (not lockdown)` is
`lockdown`.

(c) `not (hours or manager)` becomes `not hours and not manager`,
which means outside working hours, and not a manager. We rewrite it so
that somebody can check the whole sentence against the real rules for
the door.

</details>

## From earlier

**11.** From *Venn diagrams*. With everyone $= \{1, 2, 3, 4, 5, 6, 7, 8\}$,
$A = \{1, 2, 3, 4\}$ and $B = \{3, 4, 5, 6\}$, what is the complement of
$A \cup B$, and what is the intersection of the two complements?

<details class="dl-answer"><summary>answer</summary>

Both are $\{7, 8\}$. $A \cup B = \{1, 2, 3, 4, 5, 6\}$, and its
complement is what is left. The complements are $\{5, 6, 7, 8\}$ and
$\{1, 2, 7, 8\}$, and they share $\{7, 8\}$. This is De Morgan's law, on
sets.

</details>

**12.** From *Sets*. What is the set version of XOR, and how does Python
write it?

<details class="dl-answer"><summary>answer</summary>

It is the symmetric difference, everything in exactly one of the two
sets. Python writes it `A ^ B`, the same operator as XOR on `True` and
`False`, for the same reason.

</details>

**13.** From *Making decisions*. When is `x > 5 and x < 3` true?

```python exec
id: logic-never-true
for x in range(-10, 11):
    if x > 5 and x < 3:
        print(x)
print("done")
```

```predict
What will it print before "done"?

- Nothing
  - No number is both more than 5 and less than 3.
- The numbers 4 and 5
  - The numbers between the two limits.
- Every number except 3, 4 and 5
  - The numbers outside the two limits.
```

<details class="dl-answer"><summary>why</summary>

Nothing. No number is both more than 5 and less than 3, so the condition
is never true. Somebody who wrote it probably meant `or`, for the numbers
outside the gap. A condition with no `True` row in its table is a slip
worth looking for.

</details>

## Where to read more

Up and Atom (2018). *Can You Guess Who's Lying? 3 Logic Riddles to Train
Your Problem Solving Skills.*
<https://www.youtube.com/watch?v=xjSjxVAbhJ8>. Three puzzles about people
who always tell the truth and people who always lie. A truth table can
solve each one. Try before Jade Tan-Holmes gives her answers. About twelve
minutes.
