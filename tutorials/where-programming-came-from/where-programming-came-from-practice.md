---
title: "Where programming came from: from Lovelace to Python — Practice"
practice_for: where-programming-came-from
year: "2026-2027"
version: 2026.09.24.1
---

# Where programming came from: from Lovelace to Python — Practice

Each problem says what kind it is. **Predict** means guess first, then
run. **Make** means write something new. **Fix** means find why code
that looks fine does something else, and change it. **Explain** means
answer in words. **Another way** means reach the same place by a second
route. The answers are folded away until you open them, and each is one
way through: yours may go another way.

Your toolkit is loaded on this page, including `total` from
[Doing it again](tutorial:doing-it-again), `combinations` from
[Orders and choices](tutorial:orders-and-choices) and `insertion_sort`
from [Sorting a hand of cards](tutorial:sorting-a-hand-of-cards). The
tutorial's `bernoulli_numbers` is not a toolkit tool, so the Core
section starts with a cell that defines it again.

## Warm-up

Use this cell for any of the warm-up problems.

```python exec
id: where-prog-practice-warm-up
from fractions import Fraction
# Try things here
```

**1. Predict.** Run the warm-up cell first, so that `Fraction` is
there. What does each line print?

```python
print(Fraction(1, 4) + Fraction(1, 4))
print(Fraction(2, 6))
print(Fraction(1, 2) * Fraction(2, 3))
```

<details class="dl-answer"><summary>answer</summary>

`1/2`, `1/3` and `1/3`.

A quarter and a quarter make a half. `Fraction(2, 6)` is written in its
lowest terms, `1/3`, because a fraction keeps no memory of how it was
written. Half of two thirds is one third.

</details>

**2. Explain.** Babbage borrowed punched cards from Jacquard's weaving
loom. What did one card tell the loom to do, and what could one card
tell the Analytical Engine to do? Why was the same idea useful for both?

<details class="dl-answer"><summary>answer</summary>

One card told the loom which threads to lift for one row of the
pattern. One card could tell the engine which operation to do next,
such as add or divide. In both machines, a long job is broken into
small steps, and each step is written down in a form the machine can
read, in order. The cards are the program, and the order of the cards
is the sequence.

</details>

**3. Predict.** What is the first item of this sorted list?

```python
languages = [(1995, "JavaScript"), (1964, "BASIC"), (1991, "Python")]
print(sorted(languages)[0])
```

<details class="dl-answer"><summary>answer</summary>

`(1964, 'BASIC')`. `sorted` compares pairs by their first item, the
year, and 1964 is the smallest.

</details>

**4. Make.** How many years passed between Lovelace's notes (1843) and
ENIAC being shown to the public (1946)? And between BASIC at Dartmouth
(1964) and the BBC Micro (1981)? Work them out in the cell.

<details class="dl-answer"><summary>answer</summary>

```python
print(1946 - 1843)
print(1981 - 1964)
```

103 years, and 17 years. Programs had to wait a century for machines
that could run them. After that, change came much faster.

</details>

## Core

This cell defines the tutorial's `bernoulli_numbers` again, with the
names the problems below use. Run it first.

```python exec
id: where-prog-practice-core
from fractions import Fraction

def bernoulli_numbers(how_many):
    """Return the first how_many Bernoulli numbers, B0 onwards, as exact fractions."""
    numbers = [Fraction(1)]
    for m in range(1, how_many):
        weighted_sum = Fraction(0)
        for k in range(m):
            weighted_sum = weighted_sum + combinations(m + 1, k) * numbers[k]
        numbers.append(-weighted_sum / (m + 1))
    return numbers

timeline = [
    (1991, "Python 0.9.0"),
    (1843, "Lovelace's notes and Note G"),
    (1964, "BASIC at Dartmouth"),
    (1834, "Babbage begins the Analytical Engine"),
    (1995, "JavaScript"),
    (1946, "ENIAC shown to the public"),
    (1957, "FORTRAN"),
    (1952, "Hopper's A-0 compiler"),
    (1981, "BBC Micro"),
    (1959, "COBOL"),
]
print(bernoulli_numbers(5))
```

**5. Predict.** Lovelace called the numbers she kept $B_1, B_3, B_5,
B_7$. Which of today's Bernoulli numbers is her $B_5$, and what is its
value? Decide, then check with `bernoulli_numbers(7)`.

<details class="dl-answer"><summary>answer</summary>

Her $B_5$ is our $B_6$, which is $\frac{1}{42}$.

```python
print(bernoulli_numbers(7)[6])
```

She skipped the zeros in the odd places after $B_1$. Her 1, 3, 5, 7 are
our 2, 4, 6, 8: add 1 to her number to get ours.

</details>

**6. Fix.** This is the tutorial's function with one change. As in
the printed table of Note G, the two numbers of one division have been
swapped. Run it, compare the results with the tutorial's table, and
swap them back.

```python exec
id: where-prog-practice-fix-bernoulli
def bernoulli_swapped(how_many):
    """Return the first how_many Bernoulli numbers, B0 onwards, as exact fractions."""
    numbers = [Fraction(1)]
    for m in range(1, how_many):
        weighted_sum = Fraction(0)
        for k in range(m):
            weighted_sum = weighted_sum + combinations(m + 1, k) * numbers[k]
        numbers.append(-(m + 1) / weighted_sum)
    return numbers

print(bernoulli_swapped(5))
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The first number, $B_0 = 1$, matches the tutorial. Which is the
   first number that differs?
2. The tutorial's $B_1$ is $-\frac{1}{2}$, and here it is $-2$: upside
   down.
3. Which line makes each new number? Which two things does it divide?

**Think about:** why a single swap spoils every number after it, not
only one.

</details>

<details class="dl-answer"><summary>answer</summary>

The last line of the loop divides `m + 1` by `weighted_sum`. The
tutorial's version divides `weighted_sum` by `m + 1`:

```python
        numbers.append(-weighted_sum / (m + 1))
```

The swapped version gives $B_1 = -2$ in place of $-\frac{1}{2}$.
Every later number is built from the ones before it, so one number that
is off spoils all the rest. That is why the swap in Note G's
table matters: her $B_7$ comes out as $-\frac{25621}{630}$ in place of
$-\frac{1}{30}$.

</details>

**7. Make.** Write `lovelace_number(n)`, which takes Lovelace's number
for a Bernoulli number (1, 3, 5 or 7) and gives back its value. Check
that `lovelace_number(7)` is `Fraction(-1, 30)`.

<details class="dl-answer"><summary>answer</summary>

```python
def lovelace_number(n):
    """Return the Bernoulli number that Lovelace called B_n (n odd, 1 or more)."""
    return bernoulli_numbers(n + 2)[n + 1]

assert lovelace_number(1) == Fraction(1, 6)
assert lovelace_number(7) == Fraction(-1, 30)
print(lovelace_number(3), lovelace_number(5))
```

It prints `-1/30 1/42`. Her $B_n$ is our $B_{n+1}$, and to reach
position $n + 1$ the list needs $n + 2$ numbers, since it starts at 0.

</details>

**8. Explain.** Grace Hopper's A-0 was a program that put other programs
together. Why would that help a programmer in 1952? What does the same
kind of job for you each time you run a cell?

<details class="dl-answer"><summary>answer</summary>

In 1952 a program was a long list of numbers, written by hand, and one
wrong digit could break it. A-0 let a programmer name pieces of code
that were already written and tested, and the computer did the slow,
exact work of joining them. People made fewer mistakes, and wrote
programs faster.

Python does this kind of job for you. As
[When Python says no](tutorial:when-python-says-no#compilers-linkers-and-python)
showed, it compiles each cell before running it, and looks up each name
as it is used.

</details>

**9. Predict.** Here is a program in BASIC, to read. What does it print?

```basic
10 LET S = 1
20 FOR I = 1 TO 5
30 LET S = S * 2
40 NEXT I
50 PRINT S
60 END
```

<details class="dl-answer"><summary>answer</summary>

It prints 32. `S` starts at 1 and is doubled five times: 2, 4, 8, 16,
32. It is a running product, as on
[Doing it again](tutorial:doing-it-again#pi-multiplying-instead-of-adding),
and $2^5 = 32$. In Python:

```python
doubled = 1
for i in range(1, 6):
    doubled = doubled * 2
print(doubled)
```

</details>

**10. Another way.** On the tutorial page, a loop found that
$1^2 + 2^2 + \dots + 10^2 = 385$. There is a formula for the same sum,
one of the formulas the Bernoulli numbers help to write:

$$1^2 + 2^2 + \dots + n^2 = \frac{n(n+1)(2n+1)}{6}$$

Check the formula against a loop for $n = 10$ and for $n = 1000$.

<details class="dl-answer"><summary>answer</summary>

```python
for n in [10, 1000]:
    squares = []
    for number in range(1, n + 1):
        squares.append(number ** 2)
    print(total(squares), n * (n + 1) * (2 * n + 1) // 6)
```

Both ways give 385, then 333,833,500. The loop does $n$ steps; the
formula does a few multiplications, however big $n$ is. That is why
Bernoulli wanted formulas like it.

</details>

**11. Explain.** Lovelace wrote that the engine might work on things
other than numbers, even music, if the rules could be written down.
Name one thing a computer does today that fits her idea, and say what
the "numbers" are in it.

<details class="dl-answer"><summary>answer</summary>

There are many answers. A music app keeps each note as numbers: a
pitch is a frequency, such as 440 for the A on
[Waves](tutorial:waves), and a length is a time. A photo is a grid of
colours, each three numbers, as on
[Everything is ones and zeros](tutorial:everything-is-ones-and-zeros).
Text is numbers too: each letter has a code. In each case the machine
still only does arithmetic. The meaning comes from the rule that joins
the numbers to the notes, colours or letters.

</details>

**12. Explain.** FORTRAN was made for scientists and COBOL for business
records. How might that change the way each language looks?

<details class="dl-answer"><summary>answer</summary>

A language shows the habits of the people it was made for. Scientists
write formulas, so FORTRAN's name means formula translating, and its
programs look like maths. Business staff work with records and words,
so COBOL, which drew on Hopper's FLOW-MATIC, used English words for its
instructions. The same job looks different in each, because each was
built to be read by different people.

</details>

## Stretch

A cell for the stretch problems.

```python exec
id: where-prog-practice-stretch
# Your working for problems 13 to 17
```

**13. Fix.** Schlomo, who is learning Python too, wants the gap in
years between each event in the timeline and the next one. His plan is
a fair one: go through every position, and subtract this year from the
next. The cell stops with an error. Read the last line of the error,
then change the loop.

```python exec
id: where-prog-practice-fix-gaps
in_order = sorted(timeline)
for position in range(len(in_order)):
    gap = in_order[position + 1][0] - in_order[position][0]
    print(in_order[position][1], "to", in_order[position + 1][1], ":", gap, "years")
```

<details class="dl-answer"><summary>answer</summary>

The error is an `IndexError: list index out of range`. On the last time
round, `position` is 9, the last place in the list, and there is no
place 10 after it. Ten events have only nine gaps between them, so the
loop needs to stop one place earlier:

```python
for position in range(len(in_order) - 1):
```

The longest gap is from Note G (1843) to ENIAC (1946), 103 years.

</details>

**14. Make.** Bernoulli's formula finds a sum of powers without adding
them one by one. With our $B_k$ (where $B_1 = -\frac{1}{2}$), it says:

$$1^p + 2^p + \dots + n^p = \frac{1}{p+1} \sum_{j=0}^{p} \binom{p+1}{j} B_j \, (n+1)^{p+1-j}$$

Write `sum_of_powers(n, power)` from the formula, and check it against
the tutorial's loop: the tenth powers from 1 to 1,000.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Get the Bernoulli numbers you need: `bernoulli_numbers(power + 1)`.
2. Start a running sum at 0, and loop `j` from 0 to `power`.
3. Add `combinations(power + 1, j) * b[j] * (n + 1) ** (power + 1 - j)`
   each time.
4. Divide the running sum by `power + 1` at the end.

**Think about:** which number in the formula plays the part of $\sum$,
and which plays the part of the loop's counter.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def sum_of_powers(n, power):
    """Return 1**power + 2**power + ... + n**power, from Bernoulli's formula."""
    b = bernoulli_numbers(power + 1)
    running = Fraction(0)
    for j in range(power + 1):
        running = running + combinations(power + 1, j) * b[j] * (n + 1) ** (power + 1 - j)
    return running / (power + 1)

tenth_powers = []
for number in range(1, 1001):
    tenth_powers.append(number ** 10)

print(sum_of_powers(1000, 10))
print(sum_of_powers(1000, 10) == total(tenth_powers))
print(sum_of_powers(10, 2))
```

It prints Bernoulli's 91409924241424243424241924242500, then `True`,
then `385`. The formula has 11 terms, while the loop has 1,000. Many
books write the formula with $n$ in place of $n + 1$; they use
$B_1 = +\frac{1}{2}$, and the two versions agree.

</details>

**15. Another way.** The tutorial put the timeline in order with
`sorted`. Put it in order with your own `insertion_sort` from the
toolkit, and check that the two ways agree.

<details class="dl-answer"><summary>answer</summary>

```python
print(insertion_sort(timeline) == sorted(timeline))
print(insertion_sort(timeline)[0])
```

It prints `True`, then `(1834, 'Babbage begins the Analytical Engine')`.
`insertion_sort` compares items with `>`, and Python compares pairs the
same way `sorted` does: by the first item, then by the second if the
first items are equal.

</details>

**16. Explain.** Schlomi, who is learning Python too, has been reading
about Note G. "Babbage gave her the formulas," she says, "so the program
was mostly his." Schlomo has read the same books. "The table and the
ideas in her notes were hers," he says. Historians have argued both
ways. What would you need to see to decide? Why might it matter who
wrote it?

<details class="dl-answer"><summary>answer</summary>

One way in is to look for evidence before taking a side. The letters
between Lovelace and Babbage show who sent what to whom, and who found
which mistakes. Drafts in each person's handwriting would help too.

It can matter for two reasons. People who are left out of a story can be
left out of a subject: the six ENIAC programmers were not invited to its
dedication in 1946. And a program is more than its formulas. Turning a
formula into an exact order of operations, with names for every stored
number, is the programming part, whoever did it. So Schlomi and Schlomo can each
be describing a real part: the formulas and the program are two different
things.

</details>

**17. Explain.** The tutorial told this history as a story of people and
the problems they met. Many courses teach it as a list of "generations":
machine code, then assembly, then high-level languages, and so on. Which
way would you have taught it, and why?

<details class="dl-answer"><summary>answer</summary>

There is more than one answer worth giving. Here are some things an
answer might weigh:

- A list of generations is short, it is tidy, and it is what many
  exam questions ask about. It shows the big steps at a glance.
- Stories of people explain why each step happened, which can help
  people remember it and use it. They take longer, and they leave out
  many people and languages.
- Who is learning, and what for? Someone preparing for an exam might
  want the list first. Someone who wonders why programming looks the
  way it does might want the stories.

You could also argue for both: the list as a map, and the stories as
the places on it.

</details>
