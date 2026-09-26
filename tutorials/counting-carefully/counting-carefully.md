---
title: "Counting: factorials, permutations and combinations"
year: "2026-2027"
version: 2026.09.26.1
worlds:
  games-of-chance: Dice, cards and coins, and the games people play with them.
  book-characters: The people in six novels, chapter by chapter.
covers:
  factorials-the-foundation:
    covers: [MIT-5.3]
  permutations-order-matters:
    covers: [MIT-5.4]
  combinations-order-does-not-matter:
    covers: [MIT-5.5]
  a-practical-application-password-strength:
    covers: [MIT-5.2]
---

# Counting: factorials, permutations and combinations

Five friends sit down to dinner at a round table. How many different
ways can they sit? Python can list every order they could sit in:

```python exec
id: counting-dinner-table
import itertools

guests = ["Ada", "Ben", "Cara", "Dev", "Eve"]
orders = list(itertools.permutations(guests))

print(orders[0])
print(orders[1])
print(len(orders), "orders")
```

```predict
type: number

How many different orders are there for five people?
```

That is how many ways to put five people in a row. A round table is a
different question: if everyone moves one seat to the left, has anything
changed? Remember that question. This page answers it at the end.

These are *counting problems*. They ask how many different ways
something can happen. They appear in probability, which is next, and in
security (how hard is a password to guess?), in games (how many
different hands of cards are there?), and in computing (how many
different inputs can a function get?).

This page counts the slow way first, by listing every case. Then it
finds a formula that does not need the list.

## Listing the cases

`itertools` is a module of tools for looping over collections. Three
of them list the three kinds of choice this page counts. Take four
people, A, B, C and D:

- `itertools.product("ABCD", repeat=2)`: two-letter codes, where a letter
  may be used again. AA is allowed.
- `itertools.permutations("ABCD", 2)`: a captain and a vice-captain, where
  the order matters but nobody is chosen twice. AB is not BA, and AA is
  not allowed.
- `itertools.combinations("ABCD", 2)`: teams of two, where the order does
  not matter either. AB is the same team as BA.

Each rule removes some choices, so each count is smaller than the one
before it.

```python exec
id: counting-three-kinds
import itertools

codes = list(itertools.product("ABCD", repeat=2))
captains = list(itertools.permutations("ABCD", 2))
teams = list(itertools.combinations("ABCD", 2))

print(len(codes), "codes")
print(len(captains), "captain pairs")
print(len(teams), "teams:", ["".join(t) for t in teams])
```

```predict
type: number

How many teams of two can be made from four people? The last line
prints it.
```

Listing always works, but it soon gets slow. Twelve people give 495
teams of four, and a deck of 52 cards gives 2,598,960 five-card hands.
That is too many to look at, and a bigger problem would have far too many
to list. The
rest of the page finds a formula for each kind of choice, and checks it
against the listing.

## Factorials: the foundation

How many orders are there for 1, 2, 3, 4 and 5 people? Listing them all
shows a pattern:

```python exec
id: counting-orders-pattern
import itertools

for n in range(1, 6):
    print(n, "people:", len(list(itertools.permutations(range(n)))), "orders")
```

Each count is the one before it times the new number of people: 1, 2, 6,
24, 120. With five people, there are 5 choices for the first place, then
4 for the second, then 3, 2 and 1. That product is a factorial, which
you met on [Repeating steps with loops](tutorial:repeating-yourself).
The factorial of a whole number $n$ multiplies every whole number from
$n$ down to 1. We write it $n!$ and say "n factorial":

$$n! = n \times (n-1) \times (n-2) \times \cdots \times 2 \times 1$$

A factorial counts the *arrangements* of $n$ different objects. And
$0! = 1$, because there is exactly one way to arrange nothing, which is
to do nothing. That also keeps every formula on this page working when a
number in it is 0.

A factorial needs exactly the product accumulator from
[Repeating steps with loops](tutorial:repeating-yourself). Can you write
`factorial(n)`?

```python exec
id: your-turn-1
def factorial(n):
    """Return n!, the number of ways to arrange n different objects."""
    # Your code here


print(factorial(5))
```

```inputs
factorial(0)
factorial(1)
factorial(5)
factorial(10)
```

```hint
Start a product at 1, and multiply it by every whole number from 1 to n.
What does the loop do when n is 0, and what should $0!$ be?
```

```solution
def factorial(n):
    """Return n!, the number of ways to arrange n different objects."""
    product = 1
    for i in range(1, n + 1):
        product = product * i
    return product


print(factorial(5))
---
Starting at 1 handles 0 on its own. `range(1, 1)` is empty, so the loop
never runs and the answer is 1, the value of $0!$. Python's
`math.factorial` does the same job.
```

## Permutations: order matters

A *permutation* is an arrangement of $r$ objects chosen from $n$
different objects, where order matters. Eight runners finish a race. In
how many ways can they take 1st, 2nd and 3rd? There are 8 choices for
1st, then 7 left for 2nd, then 6 for 3rd: $8 \times 7 \times 6 = 336$.

That is the start of $8!$, stopped after three numbers. Dividing $8!$ by
the rest of it, $5!$, says the same thing. We write the count as
$P(n, r)$:

$$P(n, r) = \frac{n!}{(n-r)!} \qquad P(8, 3) = \frac{40320}{120} = 336$$

Can you write `permutations(n, r)` with your `factorial`, and check it
against a listing?

```python exec
id: your-turn-3
def permutations(n, r):
    """Return P(n, r), the number of ordered choices of r from n."""
    # Your code here


print(permutations(8, 3))
print(len(list(itertools.permutations(range(8), 3))))
```

```inputs
permutations(8, 3)
permutations(5, 5)
permutations(5, 0)
permutations(5, 1)
```

```hint
The formula is $n!$ divided by $(n - r)!$. Use `//` for the division, so
the answer stays a whole number.
```

```solution
def factorial(n):
    product = 1
    for i in range(1, n + 1):
        product = product * i
    return product


def permutations(n, r):
    """Return P(n, r), the number of ordered choices of r from n."""
    return factorial(n) // factorial(n - r)


print(permutations(8, 3))
print(len(list(itertools.permutations(range(8), 3))))
---
Both ways give 336. The division always gives a whole number, since
$(n-r)!$ is the last part of $n!$. `//` keeps the answer an `int` rather
than a float. With $r > n$ there is no way to choose, and `factorial` of a
negative number gives 1 here, which would be wrong. A careful version
returns 0 when `r > n`.
```

## Combinations: order does not matter

A *combination* is a choice of $r$ objects from $n$, where order does not
matter: $\{A, B, C\}$ is the same combination as $\{C, A, B\}$.

Look at the listing again. Four people gave 12 captain pairs and 6
teams. Each team, such as AB, appears twice among the captain pairs, as
AB and BA. In general, the $r$ objects in one combination can be
arranged in $r!$ orders, so the permutation count lists each combination
$r!$ times. Dividing by $r!$ counts each one once:

$$C(n, r) = \binom{n}{r} = \frac{n!}{r! \cdot (n-r)!}$$

We read $\binom{n}{r}$ as "n choose r". For the teams, $C(4, 2) = 12 / 2 = 6$.
For five-card hands from 52 cards, $C(52, 5) = 2{,}598{,}960$.

```question
id: permutation-or-combination
type: multiple-choice
answer: 2

A raffle draws 3 winning numbers from a barrel, one at a time. Every
winner gets the same prize, whatever order their number came out in.
Which counts this situation?

- A permutation, because the numbers come out one at a time.
  - Drawing one at a time is how it happens, but the prize does not depend on the order.
- A combination, because the prize does not depend on the order the numbers came out in.
  - Only which numbers win matters, not the order they came out in.
- A count with repeats allowed, because a number could be drawn more than once.
  - Once drawn, a number is out of the barrel, so it cannot come out again.
```

Can you write `combinations(n, r)` the same way?

```python exec
id: your-turn-5
def combinations(n, r):
    """Return C(n, r), the number of unordered choices of r from n."""
    # Your code here


print(combinations(4, 2))
print(len(list(itertools.combinations(range(4), 2))))
```

```inputs
combinations(52, 5)
combinations(10, 3)
combinations(5, 0)
combinations(5, 5)
combinations(10, 7)
```

```hint
Start from the permutation count, $n!$ divided by $(n - r)!$, and divide
once more by $r!$, the orders each choice was counted in.
```

```solution
def factorial(n):
    product = 1
    for i in range(1, n + 1):
        product = product * i
    return product


def combinations(n, r):
    """Return C(n, r), the number of unordered choices of r from n."""
    return factorial(n) // (factorial(r) * factorial(n - r))


print(combinations(4, 2))
print(len(list(itertools.combinations(range(4), 2))))
---
Both ways give 6. `combinations(10, 3)` and `combinations(10, 7)` are
both 120, because choosing the 3 to take is the same as choosing the 7
to leave. Python has both counts built in, as `math.perm` and
`math.comb`.
```

### Choosing the tool

For each question, ask first: does the order matter? Can the same thing
be chosen again?

1. A committee of 4 is chosen from 12 people.
2. A 4-letter sequence uses the letters A to Z, and a letter may be used
   again.
3. A PIN is 4 digits, each from 0 to 9.
4. A class of 20 chooses a president, a vice-president and a treasurer.
5. A pizza shop offers 15 toppings. How many 3-topping pizzas can it
   make?

```python exec
id: applying-the-counting-tools-1
import math

# One line for each question, with math.comb, math.perm, or **
```

```solution
import math

print(1, math.comb(12, 4))
print(2, 26 ** 4)
print(3, 10 ** 4)
print(4, math.perm(20, 3))
print(5, math.comb(15, 3))
---
The five lines print 495, 456,976, 10,000, 6,840 and 455. The committee
and the pizza are combinations, because the order does not matter. The
officers are a permutation, because who gets which job matters.
Questions 2 and 3 are different from the rest. A letter or a digit can
appear again, which permutations and combinations never allow.
```

Those two use the *multiplication principle*. With $k$ choices at each
of $r$ steps, there are $k^r$ outcomes. `itertools.product` listed
exactly these. Four letters from 26 give $26^4 = 456{,}976$.

## A practical application: password strength

An attacker who tries every possible password must try them all, so
the more there are, the stronger a password is. With only
lowercase letters, 8 characters give $26^8$ passwords. With upper case
too there are 52 choices a character, with digits 62, and with 10
special characters such as `!` and `#`, 72.

```python exec
id: counting-length-or-variety
print("12 lowercase letters:      ", 26 ** 12)
print("8 characters of any of 72: ", 72 ** 8)
print("Twelve lowercase letters win:", 26 ** 12 > 72 ** 8)
```

```predict
The last line asks which gives more passwords: 12 lowercase letters, or
8 characters from all 72?

- Twelve lowercase letters win: True
  - Length is the power. Four more characters multiply the count by 26 four times.
- Twelve lowercase letters win: False
  - 72 choices a character is nearly three times 26.
```

Length wins, because the length is the power in $k^r$. Adding to the
power makes a number grow faster than adding to the base. That is why
password advice asks for length first.

Suppose a computer tests a billion ($10^9$) passwords a second. Can you
write `crack_time(possibilities, per_second)`, which says how long trying
them all takes, in the most sensible unit?

```python exec
id: your-turn-9
def crack_time(possibilities, per_second):
    """Return how long trying every possibility takes, as text with a unit."""
    # Your code here


print(crack_time(26 ** 8, 10 ** 9))
print(crack_time(72 ** 12, 10 ** 9))
```

```inputs
crack_time(26 ** 8, 10 ** 9)
crack_time(72 ** 8, 10 ** 9)
crack_time(26 ** 12, 10 ** 9)
crack_time(72 ** 12, 10 ** 9)
```

```hint
Divide to get seconds. Then compare with a minute (60), an hour (3,600),
a day (86,400) and a year (about 31,557,600 seconds), and divide by the
largest unit the time is at least one of.
```

```solution
def crack_time(possibilities, per_second):
    """Return how long trying every possibility takes, as text with a unit."""
    seconds = possibilities / per_second
    units = [("years", 31557600), ("days", 86400), ("hours", 3600), ("minutes", 60)]
    for name, size in units:
        if seconds >= size:
            return f"{seconds / size:,.1f} {name}"
    return f"{seconds:,.1f} seconds"


print(crack_time(26 ** 8, 10 ** 9))
print(crack_time(72 ** 12, 10 ** 9))
---
Eight lowercase letters take 3.5 minutes. Eight characters from 72
take 8.4 days. Twelve lowercase letters take 3.0 years, and twelve from
72 take over 600,000 years. The biggest jump on the list is length, not
variety.
```

## The dinner table, answered

Here is the round table again. Five people give 120 orders in a row. At
a round table, a seating and the same seating moved one place round are
the same seating, because nobody's neighbours have changed. So fix one
person's seat, say Ada's, and count the orders of everyone else around
her:

```python exec
id: counting-round-table
import itertools

guests = ["Ada", "Ben", "Cara", "Dev", "Eve"]


def turned_to_ada(order):
    """The same seating, turned so that Ada is first."""
    place = order.index("Ada")
    return order[place:] + order[:place]


different = set()
for order in itertools.permutations(guests):
    different.add(turned_to_ada(order))
print(len(different), "different seatings at a round table")
```

The 120 orders form groups of 5, one group for each seating, so there
are $120 / 5 = 24$ seatings. This is $(5-1)!$, because with Ada's seat
fixed, the other four can sit in $4!$ ways. If a seating and its mirror
image count as the same, since everyone has the same two neighbours,
there are 12.

### Your turn

<div class="dl-world" data-world="book-characters">

The Bennet family of *Pride and Prejudice* sits down to dinner at a
round table: Mr and Mrs Bennet and their five daughters, Jane,
Elizabeth, Mary, Kitty and Lydia. How many different seatings are there?
And how many if Mr and Mrs Bennet must sit side by side? Can you count
both by listing, then check with a formula?

```python exec
id: counting-your-world--book-characters
import itertools

family = ["Mr Bennet", "Mrs Bennet", "Jane", "Elizabeth", "Mary", "Kitty", "Lydia"]


def turned(order):
    """The same seating, turned so that Mr Bennet is first."""
    place = order.index("Mr Bennet")
    return order[place:] + order[:place]


seatings = set()
side_by_side = 0
```

```inputs
len(seatings)
side_by_side
```

```hint
Add `turned(order)` to `seatings` for every order `itertools.permutations`
gives. With Mr Bennet first, Mrs Bennet is beside him when she is second
or last.
```

```solution
import itertools

family = ["Mr Bennet", "Mrs Bennet", "Jane", "Elizabeth", "Mary", "Kitty", "Lydia"]


def turned(order):
    """The same seating, turned so that Mr Bennet is first."""
    place = order.index("Mr Bennet")
    return order[place:] + order[:place]


seatings = set()
for order in itertools.permutations(family):
    seatings.add(turned(order))
side_by_side = 0
for seating in seatings:
    if seating[1] == "Mrs Bennet" or seating[-1] == "Mrs Bennet":
        side_by_side = side_by_side + 1
print(len(seatings), side_by_side)
---
There are 720 seatings, which is $(7-1)! = 6!$, and 240 with the parents
side by side. For the second, treat the couple as one person. Then six
sit round the table in $(6-1)! = 120$ ways, and the couple can sit two
ways round, so $120 \times 2 = 240$. That is a third of all seatings,
because with Mr Bennet fixed, 2 of the 6 other seats are beside him.
```

</div>

<div class="dl-world" data-world="games-of-chance">

Roll three dice. How many of the outcomes show three different numbers?
Can you count them by listing, with `itertools.product`, then check with
`permutations` from above?

```python exec
id: counting-your-world--games-of-chance
import itertools

rolls = list(itertools.product(range(1, 7), repeat=3))
print(len(rolls), "outcomes")

all_different = 0
```

```inputs
all_different
```

```hint
A roll shows three different numbers when `len(set(roll))` is 3. Which
kind of choice is it? Does order matter, and can a number appear again?
```

```solution
import itertools

rolls = list(itertools.product(range(1, 7), repeat=3))
print(len(rolls), "outcomes")

all_different = 0
for roll in rolls:
    if len(set(roll)) == 3:
        all_different = all_different + 1
print(all_different)
---
120 of the 216 outcomes show three different numbers. It is
$P(6, 3) = 6 \times 5 \times 4$: six numbers for the first die, five
left for the second, four for the third, and the dice are different
dice, so order matters. As a chance, 120 out of 216 is a little over a
half. The next page asks about chances like this.
```

</div>

## Looking back

The table on this page has three rows. Can you say, for each of them,
which `itertools` tool lists its cases?

| The question | The tool | The count |
|---|---|---|
| Order matters, no repeats | Permutation | $P(n, r) = \frac{n!}{(n-r)!}$ |
| Order does not matter, no repeats | Combination | $C(n, r) = \frac{n!}{r! \cdot (n-r)!}$ |
| The same thing can be chosen again | Multiplication principle | $k^r$ |

A challenge: 23 people are in a room. How many ways can they have 23
different birthdays, out of 365 days? And how many ways can they have
birthdays at all? The first divided by the second is the chance that
nobody shares. Most people expect it to be nearly certain.

```python challenge
import math

people = 23
days = 365
# Ways to have all different birthdays: an ordered choice, with no repeats.
# Ways to have birthdays at all: a choice with repeats allowed.
# Their ratio is the chance that nobody in the room shares a birthday.
```

The next page, [Probability](tutorial:what-are-the-chances),
turns these counts into probabilities, and plays the games before it
counts them.

## Where to read more

Everything here is covered elsewhere too, often in a form that will suit you
better than this one.

Khan Academy. *The Fundamental Principle of Counting.*
<https://www.youtube.com/watch?v=HDLBCv4yyIs>. The multiplication
principle this page uses for PINs and letter sequences, built up from
first principles.

Mike Pound (Computerphile) (2016). *Password Cracking.*
<https://www.youtube.com/watch?v=7U-RbOKanYs>. What the numbers this page
computes mean in practice: how fast a real machine gets through them.

Stand-up Maths (2015). *Matt Explains: Binomial Coefficients.*
<https://www.youtube.com/watch?v=Pcgvv6T_bD8>. Matt Parker explains "n
choose r" on a whiteboard, and shows where the same numbers appear in
Pascal's triangle. Twelve minutes.
