---
title: "Doubling and halving: powers and logarithms at work — Practice"
practice_for: doubling-and-halving
year: "2026-2027"
version: 2026.09.24.1
datasets: [co2-emissions]
---

# Doubling and halving: powers and logarithms at work — Practice

Each problem says what kind it is. **Predict** means guess first, then
run. **Make** means write something new. **Fix** means find one mistake
in code that looks fine. **Explain** means answer in words. **Another
way** means reach the same place by a second route. The answers are
folded away until you open them.

Your toolkit is loaded on this page, including `halvings` from the
tutorial and `binary_search` from
[Finding things fast](tutorial:finding-things-fast). `math` is not: each
cell that needs it starts with `import math`.

## Warm-up

Use this cell for any of the warm-up problems.

```python exec
id: doubling-practice-warm-up
import math
# Try things here
```

**1. Predict.** What does this line print?

```python
print(2 ** 0, 2 ** 5, 2 ** -1)
```

<details class="dl-answer"><summary>answer</summary>

`1 32 0.5`.

$2^0$ is no doublings at all, which leaves 1. $2^5$ is five doublings:
2, 4, 8, 16, 32. $2^{-1}$ is one halving of 1, which is $\frac{1}{2}$,
and Python shows it as the float `0.5`.

</details>

**2. Predict.** What does each call to `halvings` give?

```python
print(halvings(64))
print(halvings(100))
print(halvings(1))
```

<details class="dl-answer"><summary>answer</summary>

`6`, `6` and `0`.

64 halves to 32, 16, 8, 4, 2, 1: six halvings. 100 halves to 50, 25,
12, 6, 3, 1, also six, because `//` drops the remainder each time.
$\log_2 100$ is about 6.64, and `halvings` rounds it down. And 1 is
already 1, so it needs no halvings.

</details>

**3. Make.** A sourdough starter roughly doubles in size every 4 hours
in a warm kitchen. You start with 50 g. How many hours until there is
800 g? Answer with a loop, or with `math.log2`.

<details class="dl-answer"><summary>answer</summary>

```python
starter = 50
hours = 0
while starter < 800:
    starter = starter * 2
    hours = hours + 4
print(hours, starter)

print(math.log2(800 / 50) * 4)
```

Both give 16 hours. $800 \div 50 = 16$, and $16 = 2^4$, so the starter
needs 4 doublings of 4 hours each. The loop adds 4 hours for each
doubling, where the tutorial's rumour added 1.

</details>

**4. Explain.** A friend says: "Prices rose by 5% a year for 10 years.
That is a rise of 50%." Is the rise 50%, more, or less? Why? Check your
answer with one line of Python.

<details class="dl-answer"><summary>answer</summary>

More. Each year's 5% is taken of a price that has already risen, so
each rise is a little bigger than the last. That is compound growth.
`1.05 ** 10` is about 1.629, a rise of about 62.9%.

Adding the percentages is not a foolish move. It comes close for one or
two small rises. But over many years the rises multiply, as they did on
[Doing it again](tutorial:doing-it-again#pi-multiplying-instead-of-adding),
and the gap grows.

</details>

## Core

A cell for the core problems.

```python exec
id: doubling-practice-core
import math
# Your working for problems 5 to 12
```

**5. Predict.** What does the last line print? Make a guess for both
numbers before you run it.

```python
amount = 1
days = 0
while amount < 1000:
    amount = amount * 2
    days = days + 1
print(days, amount)
```

<details class="dl-answer"><summary>answer</summary>

`10 1024`.

After 9 doublings, `amount` is 512, which is still less than 1000, so
the loop runs once more. After 10 it is 1024, and the check
`1024 < 1000` is False. This is $2^{10} \approx 1000$ from the
tutorial.

</details>

**6. Make.** Food safety advice says that bacteria on food left in a
warm room can double about every 20 minutes. A plate of rice starts with
10 bacteria. How long until there are more than a million? Give the
answer in hours and minutes.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Start `bacteria` at 10 and `minutes` at 0.
2. While `bacteria` is less than 1,000,000, double it and add 20 to
   `minutes`.
3. Turn the minutes into hours with `//` and `%`, as on
   [Numbers a computer can hold](tutorial:numbers-a-computer-can-hold).

**Think about:** how many doublings take 10 to a million? That is the
same as the doublings that take 1 to 100,000.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
bacteria = 10
minutes = 0
while bacteria < 1000000:
    bacteria = bacteria * 2
    minutes = minutes + 20
print(minutes, "minutes, which is", minutes // 60, "hours and", minutes % 60, "minutes")
print(bacteria)
```

340 minutes, which is 5 hours and 40 minutes, with 1,310,720 bacteria.
That took 17 doublings. As a check, `math.log2(100000)` is about 16.6,
which rounds up to 17. An afternoon on the counter is enough, which is
why the advice is to put cooked rice in the fridge soon.

</details>

**7. Fix.** Here is someone's version of `halvings`, with two tests.
Run it, see which test fails, and fix the function.

```python exec
id: doubling-practice-fix-halve
def halvings_again(n):
    """Return how many times the whole number n can be halved, rounding down, before it reaches 1."""
    count = 0
    while n > 1:
        n = n / 2
        count = count + 1
    return count

assert halvings_again(8) == 3, "8, 4, 2, 1"
assert halvings_again(1000) == 9, "500, 250, 125, 62, 31, 15, 7, 3, 1"
print("halvings_again keeps its promise.")
```

<details class="dl-answer"><summary>answer</summary>

The second test fails: `halvings_again(1000)` gives 10. The function
halves with `/`, which keeps the fraction, so 125 becomes 62.5, then
31.25, and so on, down to 1.953125. That is still more than 1, so the
loop halves once more, to about 0.98. The promise says "rounding down",
which is `//`:

```python
        n = n // 2
```

The first test passed because 8 is a power of 2, and halving it never
leaves a remainder. A test on a power of 2 alone would never have found
this bug.

</details>

**8. Fix.** This cell is meant to add up the grains on all 64 squares
of the chessboard. Its answer is not $2^{64} - 1$. Find the mistake.

```python exec
id: doubling-practice-fix-chess
grains_on_board = 0
for square in range(1, 64):
    grains_on_board = grains_on_board + 2 ** (square - 1)
print(grains_on_board)
print(grains_on_board == 2 ** 64 - 1)
```

<details class="dl-answer"><summary>answer</summary>

It prints `9223372036854775807` and `False`. `range(1, 64)` stops before
64, so the loop covers only squares 1 to 63. The answer is $2^{63} - 1$,
about half the right total, because the last square alone holds more
than all the others together. The fix is `range(1, 65)`.

</details>

**9. Another way.** A hex colour like `#FF8800`, from
[Everything is ones and zeros](tutorial:everything-is-ones-and-zeros#how-ff8800-makes-orange),
can be any one of 16,777,216 colours. How many doublings of 1 reach
16,777,216? Find it three ways: with a loop, with `math.log2`, and with
`halvings`.

<details class="dl-answer"><summary>answer</summary>

```python
doubled = 1
doublings = 0
while doubled < 16777216:
    doubled = doubled * 2
    doublings = doublings + 1
print(doublings)

print(math.log2(16777216))
print(halvings(16777216))
```

All three give 24 (the logarithm as `24.0`). 16,777,216 is exactly
$2^{24}$, so doubling up and halving down take the same number of steps,
with no rounding. It is also the number of bits in a colour: 8 bits
each for red, green and blue.

</details>

**10. Explain.** The tutorial counted doublings and halvings with loops
first, and named the logarithm afterwards, as a quick way to get the
count. Many textbooks start the other way: they define $\log_b x$ as
the power of $b$ that makes $x$, and then practise its laws as algebra.
Which way would you have wanted to learn it, and why? There is no one
right answer.

<details class="dl-answer"><summary>answer</summary>

A good answer weighs a few things, and can land on either side.

- **What you can check.** A count from a loop can be checked by
  running it, or on paper. A law learned as algebra is checked by
  following rules.
- **Speed.** The textbook route is faster to write down, and exam
  questions are often written for it.
- **What comes next.** Logarithms as counts connect to algorithms, such
  as binary search. Logarithms as algebra connect to later maths, such
  as solving equations like $1.04^k = 2$ by hand, and calculus.
- **Awkward cases.** A count is harder to picture when the answer is
  9.97. The algebra has no trouble with that.
- **You.** Some people trust a rule more once they have seen it work
  on numbers. Others find the numbers a slow way round.

It is also fair to want both, in one order or the other.

</details>

**11. Make.** A store card charges 24% interest a year on any money
still owed. Someone owes €1,000 and pays nothing back. Use the rule of
72 to estimate how long until the debt doubles. Then find the exact
answer with `math.log`, and the number of whole years with a loop.

<details class="dl-answer"><summary>answer</summary>

```python
print(72 / 24)
print(math.log(2, 1.24))

owed = 1000
years = 0
while owed < 2000:
    owed = owed * 1.24
    years = years + 1
print(years, round(owed, 2))
```

The rule of 72 says 3 years. The exact doubling time is about 3.22
years. After 3 whole years the debt is €1,906.62, so it passes €2,000
during the fourth year, and the loop gives 4 years and €2,364.21. The
rule of 72 is least close at high rates like this one.

</details>

**12. Predict.** What do these three lines print?

```python
print(math.log2(64 * 1024))
print(math.log2(64) + math.log2(1024))
print(math.log10(1000 * 100))
```

<details class="dl-answer"><summary>answer</summary>

`16.0`, `16.0` and `5.0`.

64 is 6 doublings and 1024 is 10, so $64 \times 1024$ is 16 doublings.
The law of logarithms works in any base: `math.log10` counts
multiplications by 10, and $1000 \times 100$ is 3 of them and then 2
more.

</details>

## Stretch

A cell for the stretch problems.

```python exec
id: doubling-practice-stretch
import math
# Your working for problems 13 to 17
```

**13. Make.** A cup competition has 40 teams. Every match knocks one
team out. When a round has an odd number of teams, or a number that
will not halve down evenly, some teams get a *bye*: they go through to
the next round without playing. Write `rounds_needed(teams)`, which
gives how many rounds it takes to get down to one winner. Test it on
128, 40, 2 and 3 teams. Is it `halvings(teams)`?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. 128 teams need 7 rounds. How many rounds would 129 teams need?
2. A round can at most halve the teams, rounding up: 3 teams leave at
   least 2.
3. So the rounds needed is the number of doublings of 1 that reach
   `teams`, or more. The rumour counted that.

**Think about:** does `halvings` round the logarithm up or down? Which
one do you need here?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def rounds_needed(teams):
    """Return how many knockout rounds it takes to get from teams down to one winner."""
    winners_possible = 1
    rounds = 0
    while winners_possible < teams:
        winners_possible = winners_possible * 2
        rounds = rounds + 1
    return rounds

for teams in [128, 40, 2, 3]:
    print(teams, rounds_needed(teams), halvings(teams), math.ceil(math.log2(teams)))
```

128 teams need 7 rounds, 40 need 6, 2 need 1 and 3 need 2. So it is
not `halvings`: `halvings(40)` is 5, one round short. Halvings round the
logarithm down, and a competition needs it rounded up, because the
last team with a bye still has to play. `math.ceil(math.log2(teams))`
gives the same answers. So does `halvings(teams - 1) + 1`, for 2 teams
or more.

</details>

**14. Another way.** On
[A function that calls itself](tutorial:a-function-that-calls-itself#a-promise-that-uses-itself),
a promise used itself on a smaller problem. Write
`halvings_by_calls(n)` with no loop. It uses itself on `n // 2`. What
is its base case? Test it against `halvings` for every number from 1 to
1,000.

<details class="dl-answer"><summary>answer</summary>

```python
def halvings_by_calls(n):
    """Return how many times n can be halved, rounding down, before it reaches 1."""
    if n == 1:
        return 0                            # the base case: nothing to halve
    return 1 + halvings_by_calls(n // 2)    # one halving, then the rest

for n in range(1, 1001):
    assert halvings_by_calls(n) == halvings(n), n
print("The two versions agree.")
```

It prints `The two versions agree.` The base case is 1, which needs no
halvings. For anything bigger, the number of halvings is one halving,
plus the halvings of what is left. Each call waits for a number about
half the size, so even `halvings_by_calls(1000000)` makes only 20
calls, far from Python's limit.

</details>

**15. Make.** The file from the tutorial also has a `gdp` column: the
value of everything a country produced in a year, in dollars adjusted
so that years can be compared. Find each year in which Ireland's GDP
first reached 2, 4, 8 and 16 times its 1950 value. How many years did
each doubling take? The first lines are written for you.

```python exec
id: doubling-practice-gdp
df = await load_csv("co2-emissions.csv")
ireland = df[df.country == "Ireland"]
years = ireland["year"].tolist()
gdp = ireland["gdp"].tolist()
print(years[0], gdp[0])
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The tutorial's emissions cell has the shape you need. Change
   `emissions` to `gdp`.
2. Keep a `target`, which starts at twice the 1950 value and doubles
   each time it is reached.
3. Print the year each time a target is reached.

**Think about:** the last value in `gdp` is `nan`, which means "no
number here". Is `nan >= target` True or False?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
target = 2 * gdp[0]
for position in range(len(years)):
    if gdp[position] >= target:
        print(years[position])
        target = 2 * target
```

It prints 1973, 1990, 1999 and 2017. The doublings took 23, 17, 9 and
18 years. The fast one, in the 1990s, was the years people called the
Celtic Tiger. For 2023 the file has no value, and a comparison with
`nan` is always False, so the loop passes it by.

One honest note: Ireland's GDP includes large profits that foreign
companies record here, so it grew faster than most people's incomes
did.

</details>

**16. Explain.** In the game Twenty Questions, one player thinks of
something, and the other may ask up to 20 questions that are answered
"yes" or "no". A good player can pick out one thing from about a
million. Why a million? What does this have to do with binary search?

<details class="dl-answer"><summary>answer</summary>

A good question splits the things still possible into two halves:
"yes" keeps one half and "no" keeps the other. That is a binary
search, and each answer is one halving. Twenty halvings can bring
$2^{20} = 1{,}048{,}576$ things down to one, and $2^{20}$ is about a
million, since $2^{10} \approx 1000$.

A question that splits the things unevenly, like "Is it a
hedgehog?", usually throws away far less than half. That is why a good
player asks "Is it alive?" first.

</details>

**17. Fix.** A savings app has a function for the doubling time, and a
test that compares it with the rule of 72. The test fails. Find the
mistake.

```python exec
id: doubling-practice-fix-rate
def years_until_double(start, rate_percent):
    """Return how many whole years start takes to double, growing by rate_percent a year."""
    amount = start
    years = 0
    while amount < 2 * start:
        amount = amount * (1 + rate_percent)
        years = years + 1
    return years

print(years_until_double(1000, 4))
assert abs(years_until_double(1000, 4) - 72 / 4) <= 1, "the rule of 72 says about 18"
print("years_until_double agrees with the rule of 72.")
```

<details class="dl-answer"><summary>answer</summary>

It prints `1`, and then the test fails. `1 + rate_percent` is 5, so the
money is multiplied by 5 in the first year: a 400% rise, not 4%. A rate
in percent has to be divided by 100 first:

```python
        amount = amount * (1 + rate_percent / 100)
```

Now it gives 18, and the test passes. The rule of 72 made a good test
here, because it is a second route to an answer we can trust roughly,
as on [Does it work?](tutorial:does-it-work#code-that-runs-and-code-that-works).

</details>
