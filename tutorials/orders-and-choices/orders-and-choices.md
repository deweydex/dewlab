---
title: "Orders and choices: factorials, permutations and combinations"
year: "2026-2027"
version: 2026.09.24.1
covers:
  three-songs-in-a-row:
    covers: [MIT-5.3]
    touches: [MIT-5.2, PDP-LO6]
  factorial-a-product-that-counts-orders:
    covers: [MIT-5.3]
    touches: [MIT-6.4]
  only-the-first-few-places:
    covers: [MIT-5.4]
  when-order-does-not-matter:
    covers: [MIT-5.5]
  which-count-do-i-need:
    covers: [MIT-5.4, MIT-5.5]
    touches: [MIT-5.2]
---

# Orders and choices: factorials, permutations and combinations

Eight friends turn up for a game of five-a-side football, and only five
can play at a time. How many different teams could walk onto the pitch?
And if the five also have to agree who plays in goal, who defends and who
attacks, how many ways are there then?

The answers are 56 and 6,720. By the end of this page you will know where
each number comes from, and you will have three tools that find numbers
like these in one line.

On this page we:

- list every order of a few songs with a loop, and count them
- meet the factorial, a product that counts orders
- count the ways to fill the first few places: permutations
- count the ways to choose when order does not matter: combinations
- check every formula against a loop that lists every case
- add `factorial`, `permutations` and `combinations` to the toolkit

> **The space we're in.** Whole numbers, and groups of things that are
> all different from each other: eight different friends, three different
> songs. Nothing is picked twice unless we say so. One thing usually goes
> unsaid, so we will say it: we assume we can tell every item apart. Two
> identical red socks would change every count on this page. Your toolkit
> gives us `total`, `product` and `all_pairs` from the last two pages.

## Warm-up

The first question is from
[Counting every outfit: lists of outcomes](tutorial:counting-every-outfit),
and the second from
[Doing it again: loops, sums and products](tutorial:doing-it-again).

```question
id: orders-warm-up-1
type: fill-in-the-blank

A café offers 3 kinds of bread and 4 fillings. A sandwich is one bread
and one filling, so the café can make {12} different sandwiches.
```

```question
id: orders-warm-up-2
type: multiple-choice
correct: 3

What does `product([1, 2, 3, 4])` give?

- 10
- 4
- 24
- 1234
```

## Three songs in a row

You have three songs by The Cranberries for the start of a playlist:
"Zombie", "Linger" and "Dreams". In how many different orders can they
play? Try to list them all on paper before you read on.

One way to be sure we miss none is to fill one place at a time. The first
song can be any of the three. Once it is chosen, the second song can be
either of the two that are left. The last song is whichever one remains.

A loop can do the same listing for us. It tries every song in every
place, and keeps only the rows where no song appears twice. How many
orders do you expect it to print? Run it to check.

```python exec
id: orders-songs-1
songs = ["Zombie", "Linger", "Dreams"]
orders = 0
for first in songs:
    for second in songs:
        for third in songs:
            if first != second and first != third and second != third:
                print(first, "|", second, "|", third)
                orders = orders + 1
print(orders, "orders")
```

Six orders. The three loops try $3 \times 3 \times 3 = 27$ rows, the same
way the truth tables on
[True, false and every case](tutorial:true-false-and-every-case) did.
The `if` then throws away the 21 rows that use a song more than once.

An *arrangement* is one order of a group of things, from first to last.
The counting principle from the last page tells us how many there are
without listing them: 3 choices for the first place, then 2, then 1.

$$3 \times 2 \times 1 = 6$$

The choices shrink by one at each place, because a song that has already
played cannot play again.

### Your turn

1. Add a fourth song, "Ode to My Family", to the list in the cell above.
2. Before you change anything else, guess how many orders there will be
   now.
3. Add a fourth loop, `for fourth in songs:`, and make the `if` check
   that no two of the four songs are the same. It needs six checks, so
   it grows long. We will find a shorter way in the next section.
4. Run it, and compare the count with your guess.

## Factorial: a product that counts orders

Four songs have $4 \times 3 \times 2 \times 1 = 24$ orders. For any
number of songs, the pattern is the same: one choice fewer at each place,
down to 1. This product has its own name and its own sign.

The *factorial* of a whole number $n$ is the product of every whole
number from 1 up to $n$. We write it $n!$ and say "n factorial". It
counts the arrangements of $n$ different things.

$$n! = n \times (n-1) \times \dots \times 2 \times 1 = \prod_{k=1}^{n} k$$

The $\prod$ is the pi notation from
[Doing it again](tutorial:doing-it-again#pi-multiplying-instead-of-adding), a
loop written by mathematicians: multiply $k$, for every $k$ from 1 to
$n$. So your `product` tool can find a factorial already.

How fast do you think factorials grow? Before you run the cell, guess
$10!$. Is it nearer 100, 10,000 or 1,000,000?

```python exec
id: orders-factorial-1
arrangements = 1
for songs_so_far in range(1, 11):
    arrangements = arrangements * songs_so_far
    print(songs_so_far, "->", arrangements)

print(product(range(1, 11)))
```

Each row shows a number of songs, then the number of orders they can
play in. Ten songs can play in 3,628,800 different orders. Each new song
multiplies the count by the new number of songs, so the count grows
faster and faster. `range(1, 11)` gives the numbers 1 to 10, because it
stops just before its second number. The last line finds the same $10!$
with `product`, in one step.

A deck of 52 playing cards has $52!$ orders, a number with 68 digits.
If you shuffle a deck well, it is very likely that no deck in history
has ever been in that exact order before.

### What is 0!?

Here is a question about the space we are in. What should $0!$ be? There
are no numbers from 1 up to 0 to multiply.

Look at the loop above with `range(1, 1)` in place of `range(1, 11)`. It
runs zero times, so `arrangements` stays at 1. Mathematicians agree:

$$0! = 1$$

There is exactly one way to arrange nothing, which is to play no songs
at all. This can feel strange, and that is fine. It is an agreement,
made because it keeps every formula later on this page working.

```question
id: orders-factorial-2
type: multiple-choice
correct: 2

A queue of 6 people forms at a bus stop. How many different orders
could they stand in?

- 21, which is 6 + 5 + 4 + 3 + 2 + 1
- 720, which is 6!
- 36, which is 6 × 6
```

### Your turn: factorial in your toolkit

The cell below is the start of `factorial`, a new function for your
toolkit. Replace the `...` with a loop that multiplies every whole
number from 1 up to `n`, the way the cell `orders-factorial-1` did, and
return the result.

```python exec
id: orders-toolkit-factorial
toolkit: yes
def factorial(n):
    """Return n!, the number of orders of n different things.

    n is a whole number, 0 or more. factorial(0) is 1.
    """
    ...
```

```python toolkit-reference
for: orders-toolkit-factorial
def factorial(n):
    """Return n!, the number of orders of n different things.

    n is a whole number, 0 or more. factorial(0) is 1.
    """
    result = 1
    for number in range(1, n + 1):
        result = result * number
    return result
```

Now test it. Until your `factorial` is written, this cell stops with an
error, which is the test doing its job. The last test compares yours
with Python's own `math.factorial`, which is another way to the same
number.

```python exec
id: orders-factorial-tests
import math

assert factorial(3) == 6
assert factorial(4) == 24
assert factorial(0) == 1
assert factorial(10) == 3628800
assert factorial(20) == math.factorial(20)
print("factorial keeps its promise.")
```

```hint
What does `print(factorial(4))` show on its own? If it shows `None`, the
function reached its end without a `return`.
```

## Only the first few places

At a club race, eight runners are close together in the last 200 metres.
Prizes go to the first three: gold, silver and bronze. How many
different top threes are possible?

Fill one place at a time again. Any of the 8 can win. Then any of the 7
left can come second, and any of the 6 left can come third. After that
we stop, because the other five runners do not change who is on the
podium.

$$8 \times 7 \times 6 = 336$$

A *permutation* is an arrangement of some of a group of things, where
the order matters. The number of permutations of $r$ things chosen from
$n$ is written $P(n, r)$. Some books write it $^{n}P_{r}$. So the club race
question asks for $P(8, 3)$.

The loop below tries every runner in every place, and counts the rows
with no runner twice. It counts, rather than printing 336 rows. Does it
agree with $8 \times 7 \times 6$?

```python exec
id: orders-podium-1
runners = ["Aoife", "Bea", "Cian", "Dara", "Eoin", "Fionn", "Grace", "Hana"]
podiums = 0
for gold in runners:
    for silver in runners:
        for bronze in runners:
            if gold != silver and gold != bronze and silver != bronze:
                podiums = podiums + 1

print(podiums)
print(8 * 7 * 6)
```

Both lines show 336. Now we want a formula for any $n$ and $r$. Look at
$8 \times 7 \times 6$. It is the start of $8!$, with the end,
$5 \times 4 \times 3 \times 2 \times 1$, missing. That end is $5!$, the
orders of the five runners who win nothing. Dividing $8!$ by $5!$ cuts
it off.

In words: the orders of all $n$ things, divided by the orders of the
$n - r$ things we do not care about.

$$P(n, r) = n \times (n-1) \times \dots \times (n - r + 1) = \frac{n!}{(n-r)!}$$

Here it is in Python, with your `factorial`. We use `//`, from
[Numbers a computer can hold](tutorial:numbers-a-computer-can-hold),
because this division always comes out whole, and `//` keeps the answer
an int. This cell needs your `factorial` from the last section. If it is
not written yet, the cell stops with a `TypeError`, because a function
with no `return` gives back `None`, and Python cannot divide `None`.

```python exec
id: orders-podium-2
print(factorial(8) // factorial(5))
print(factorial(8) // factorial(3))
```

The first line is the podium, 336. The second line divides by $3!$
instead, and gives 6,720. That is $P(8, 5)$: the ways to put five of
the eight friends into five named positions on the pitch. It answers the
second question at the top of the page.

### Your turn: permutations in your toolkit

1. Fill in the body of `permutations` below, using `factorial` and `//`.
2. Run the cell, then run the tests under it.

```python exec
id: orders-toolkit-permutations
toolkit: yes
def permutations(n, r):
    """Return P(n, r): the orders of r things chosen from n different things.

    n and r are whole numbers, with r from 0 up to n.
    """
    ...
```

```python toolkit-reference
for: orders-toolkit-permutations
def permutations(n, r):
    """Return P(n, r): the orders of r things chosen from n different things.

    n and r are whole numbers, with r from 0 up to n.
    """
    return factorial(n) // factorial(n - r)
```

Until your `permutations` is written, these tests stop with an error.

```python exec
id: orders-permutations-tests
assert permutations(8, 3) == 336
assert permutations(8, 5) == 6720
assert permutations(3, 3) == factorial(3)
assert permutations(10, 1) == 10
assert permutations(5, 0) == 1
print("permutations keeps its promise.")
```

The last test is $P(5, 0)$: the ways to fill no places at all. It is 1,
and it only comes out as 1 because $0! = 1$.

## When order does not matter

Back to five-a-side, with no positions this time. Aoife, Bea, Cian, Dara
and Eoin are one team. Eoin, Dara, Cian, Bea and Aoife are the same team,
listed in a different order. So $P(8, 5)$ counts every team many times
over.

Let's look at a smaller question first. A pizza comes with two toppings
from four: ham, pineapple, mushroom and olive. In order, there are
$4 \times 3 = 12$ ways to pick two. But "ham and olive" is the same
pizza as "olive and ham", so every pizza is counted twice.

To list each pizza once, we let the second loop start just after the
first one. How many pizzas do you expect? Run it to check.

```python exec
id: orders-pizza-1
toppings = ["ham", "pineapple", "mushroom", "olive"]
pizzas = 0
for first in range(4):
    for second in range(first + 1, 4):
        print(toppings[first], "and", toppings[second])
        pizzas = pizzas + 1
print(pizzas, "pizzas")
```

Six pizzas: $12 \div 2$. The loops count positions in the list, from 0.
Because `second` always starts after `first`, each pair of toppings
appears once, in one order only.

A *combination* is a choice of some things from a group, where the order
does not matter. The number of combinations of $r$ things chosen from $n$
is written $C(n, r)$, or $\binom{n}{r}$, and said "n choose r".

Every choice of $r$ things can be put in order in $r!$ ways. So the
permutations count each combination $r!$ times, and we divide that out:

$$C(n, r) = \frac{P(n, r)}{r!} = \frac{n!}{r!\,(n-r)!}$$

For the pizza, that is $12 \div 2! = 6$. For the team, it is
$6720 \div 5! = 6720 \div 120 = 56$.

### Checking with a list of every team

Five loops, one inside another, would list the teams, but that is a lot
of typing. Python has a module that does the listing for us:
`itertools`, which we met on
[Untangling a condition](tutorial:untangling-a-condition). Its
`combinations` lists every choice, and its `permutations` lists every
order.

Notice that we write `itertools.combinations`, with the module's name in
front. Your toolkit is about to have its own `combinations`, which
counts. The name `combinations` points at two different things in two
different spaces, and the `itertools.` in front says which space we
mean. `list()` turns what `itertools` makes into a list, so `len` can
count it.

```python exec
id: orders-team-1
import itertools

players = ["Aoife", "Bea", "Cian", "Dara", "Eoin", "Fionn", "Grace", "Hana"]
teams = list(itertools.combinations(players, 5))
print(teams[0])
print(teams[1])
print(len(teams), "teams")

lineups = list(itertools.permutations(players, 5))
print(len(lineups), "line-ups with positions")
```

Every team of five, listed and counted: 56. Every line-up with
positions: 6,720. The formula is the fast way, and the list is the
proof.

### Your turn: combinations in your toolkit

1. Fill in the body of `combinations`, using `factorial` or
   `permutations`.
2. Run it, then run the tests.
3. Look at the fourth test. Why should choosing 3 friends from 8 give
   the same count as choosing 5? (Think about who sits out.)

```python exec
id: orders-toolkit-combinations
toolkit: yes
def combinations(n, r):
    """Return C(n, r): the ways to choose r things from n different things,
    when the order does not matter.

    n and r are whole numbers, with r from 0 up to n.
    """
    ...
```

```python toolkit-reference
for: orders-toolkit-combinations
def combinations(n, r):
    """Return C(n, r): the ways to choose r things from n different things,
    when the order does not matter.

    n and r are whole numbers, with r from 0 up to n.
    """
    return factorial(n) // (factorial(r) * factorial(n - r))
```

Until your `combinations` is written, these tests stop with an error.

```python exec
id: orders-combinations-tests
assert combinations(4, 2) == 6
assert combinations(8, 5) == 56
assert combinations(8, 5) == len(list(itertools.combinations(players, 5)))
assert combinations(8, 3) == combinations(8, 5)
assert combinations(5, 0) == 1
assert combinations(5, 5) == 1
print("combinations keeps its promise.")
```

## Which count do I need?

Most counting questions come down to two smaller questions. Does the
order matter? And can the same thing be picked more than once?

| | Order matters | Order does not matter |
|---|---|---|
| **Repeats allowed** | $n^r$, the counting principle: a 4-digit PIN has $10^4$ | a rarer case, which we leave for now |
| **No repeats** | $P(n, r)$: a podium, a team with positions | $C(n, r)$: a team, a pizza, a lottery ticket |

The Irish Lotto draws 6 numbers from 1 to 47. A ticket wins the jackpot
when its six numbers match, in any order. So the order does not matter,
and no number can come up twice.

Our unit is building towards a password-strength checker. The last
page counted $26^8$ passwords of 8 small letters, where the order
matters and a letter can appear again. The third line counts them with
one more rule: no letter used twice. What do you expect it to show: more
passwords, or fewer? Run it to check. This cell uses your
`combinations` and `permutations`, so it shows `None` for any of them
you have not written yet.

```python exec
id: orders-which-1
print(combinations(47, 6), "Lotto tickets")
print(26 ** 8, "passwords of 8 small letters")
print(permutations(26, 8), "passwords with no letter used twice")
```

There are 10,737,573 different Lotto tickets, so one ticket has about a
one in ten million chance of the jackpot. The next page,
[How likely is it?](tutorial:how-likely-is-it), turns counts like this
into chances.

The passwords are a surprise for some people. A rule that says "no
letter twice" sounds strict, but it leaves fewer passwords to guess:
about 63 billion instead of about 209 billion. A rule makes a password
stronger only when it makes the space of possible passwords bigger.

```question
id: orders-which-2
type: multiple-choice
correct: 3

A school choir of 20 needs 4 singers to go to a competition. Which count
gives the number of different groups that could go?

- $20^4$
- $P(20, 4)$
- $C(20, 4)$
- $4!$
```

### Your turn

1. A café's meal deal lets you choose 3 different sides from 7. Decide
   first: does the order matter, and can a side repeat?
2. Work out the number of meal deals in the cell below.
3. A bet on a horse race names the first and second horse, in order,
   from 12 runners. Decide which count it needs, and work it out too.

```python exec
id: orders-which-your-turn
# The meal deal, then the horse race
```

<details class="dl-why"><summary>Why this way?</summary>

This page told you the answers, 56 and 6,720, in its second paragraph,
before you had worked anything out. Most pages in this course ask you to
guess first.

Asking for a guess is usually the better choice. A guess gives you
something to compare with, and a wrong guess shows you where your
thinking went.

Here we gave the answers away on purpose. Counting teams and line-ups is
a long road, with three formulas on the way. Knowing where it ends lets
you check each step as you go: when $P(8, 5)$ comes out as 6,720, you
know that part is right. An answer named at the start is a promise, and
the rest of the page keeps it.

</details>

## Four questions, looking back

| The question | On this page |
|---|---|
| What is named here? | $n!$, $P(n, r)$ and $C(n, r)$; the toolkit functions `factorial`, `permutations` and `combinations`; one name, `combinations`, in two spaces |
| What is promised? | `factorial(n)` promises the orders of $n$ things; `permutations` and `combinations` promise their counts, and the tests check each promise against a list of every case |
| What happens when? | Places are filled one at a time, with one choice fewer each time. `factorial` must work before `permutations` and `combinations`, which are built from it. |
| What does this space let us do? | Things we can tell apart, picked at most once. Here $0! = 1$ is an agreement that keeps the formulas working. |

## What we have now

| Term or move | What it means |
|---|---|
| arrangement | one order of a group of things, from first to last |
| factorial, $n!$ | $n \times (n-1) \times \dots \times 1$: the arrangements of $n$ things; $0! = 1$ |
| permutation, $P(n, r)$ | an arrangement of $r$ things from $n$, where order matters: $\frac{n!}{(n-r)!}$ |
| combination, $C(n, r)$, $\binom{n}{r}$ | a choice of $r$ things from $n$, where order does not matter: $\frac{n!}{r!\,(n-r)!}$ |
| `itertools.combinations`, `itertools.permutations` | Python's tools that list every choice, or every order |
| `factorial(n)`, `permutations(n, r)`, `combinations(n, r)` | your three new toolkit functions |

For another route through the same counts, the integrated course has
[Counting: factorials, permutations and combinations](tutorial:counting-carefully).
