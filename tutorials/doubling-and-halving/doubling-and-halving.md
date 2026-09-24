---
title: "Doubling and halving: powers and logarithms at work"
year: "2026-2027"
version: 2026.09.24.1
datasets: [co2-emissions]
covers:
  a-rumour-that-doubles:
    covers: [MIT-1.1]
    touches: [PDP-LO6]
  grains-on-a-chessboard:
    covers: [MIT-1.1]
    touches: [MIT-6.4, MIT-1.4]
  doublings-add-up:
    covers: [MIT-1.1]
  how-long-to-double:
    covers: [MIT-1.1]
    touches: [MIT-6.5]
  halving-down-to-1:
    covers: [MIT-1.1]
    touches: [MIT-1.4, PDP-LO8]
  why-binary-search-is-so-quick:
    covers: [MIT-1.1]
    touches: [MIT-6.6, MIT-6.8]
---

# Doubling and halving: powers and logarithms at work

At nine o'clock one morning, you tell a friend a secret. An hour later,
each person who knows it has told one more person. The hour after that,
the same again. How long before the whole of Ireland knows?

And here is a second question that looks quite different. A phone keeps
five million names in order. Why does it find one of them in a moment?
By the end of this page, the two questions will turn out to have the
same answer.

On this page we:

- follow a rumour that doubles every hour, and count the hours
- put grains on a chessboard, and add them up
- see why doublings add, and use $2^{10} \approx 1000$ to estimate
- find how long money, or a country's emissions, takes to double
- count halvings down to 1, and add `halvings` to the toolkit
- see why binary search is so quick: $2^k = n$ and $k = \log_2 n$, from
  both ends

> **The space we're in.** Whole numbers that double, and whole numbers
> that are halved with `//`, which drops any remainder. Python's whole
> numbers never run out of room, however big they get. We met powers and
> logarithms on
> [Numbers a computer can hold](tutorial:numbers-a-computer-can-hold#powers-and-how-many-times),
> and binary search on
> [Finding things fast](tutorial:finding-things-fast). One thing usually
> goes unsaid: a rule like "everyone tells one more person" is a model.
> It is true of the maths. It is only roughly true of people, and only
> for a while.

## Warm-up

The first question is from
[A function that calls itself](tutorial:a-function-that-calls-itself#where-the-promise-stops-the-base-case),
and the second from
[Finding things fast](tutorial:finding-things-fast#only-in-a-sorted-list).

```question
id: doubling-warm-up-1
type: fill-in-the-blank

A function that calls itself on a smaller problem needs a
{base case|loop|docstring}: an input small enough to answer straight
away, where the calls stop.
```

```question
id: doubling-warm-up-2
type: multiple-choice
correct: 2

Binary search looks at the middle of a list and throws away the half
where the target cannot be. What must be true of the list first?

- It must hold numbers, not words.
- It must be sorted.
- It must have an even number of values.
- It must be shorter than 1,000 values.
```

## A rumour that doubles

At the start, one person knows the rumour: you. After one hour, you have
told one friend, so two people know. After two hours, each of those two
has told someone new, so four people know. Every hour, the number who
know doubles.

The population of Ireland at the 2022 census was 5,149,139. Before you
run the cell, guess how many hours the rumour needs to reach that many
people. A day? A week? A month?

```python exec
id: doubling-rumour-1
population = 5149139

people_who_know = 1
hours = 0
while people_who_know < population:
    people_who_know = people_who_know * 2
    hours = hours + 1

print(hours, "hours, and", people_who_know, "people could know")
```

It takes 23 hours. After 22 hours, 4,194,304 people know, which is
about four people in every five. One more doubling passes the whole population. (The
rumour runs out of new people before the last hour ends, so 8,388,608
is what the rule would give, not what could happen.)

The loop has a counter, `hours`, and the counter is the answer. It
counts doublings. Here is a picture of the same 23 hours. Before you
run it, what shape do you expect?

```python exec
id: doubling-rumour-2
import matplotlib.pyplot as plt

hour_list = []
people_list = []
knowing = 1
for hour in range(24):
    hour_list.append(hour)
    people_list.append(knowing)
    knowing = knowing * 2

plt.plot(hour_list, people_list, marker="o")
plt.axhline(population, color="grey", linestyle="--")
plt.xlabel("hours since you told one friend")
plt.ylabel("people who know")
```

For most of the day the line lies flat along the bottom. After 13 hours,
only 8,192 people know, and the country has not noticed. Then the line
rises very steeply. By the rule, more people hear the rumour in each
hour than in all the hours before it put together.

Growth like this, where a number is multiplied by the same amount each
step, is called *exponential growth*. The name comes from the exponent:
after $k$ hours, $2^k$ people know. So the question "how many hours?"
asks for the $k$ that makes $2^k$ reach 5,149,139. That is a logarithm,
as on
[Numbers a computer can hold](tutorial:numbers-a-computer-can-hold#powers-and-how-many-times):

$$2^k = n \quad \text{means} \quad k = \log_2 n$$

`math.log2(5149139)` is about 22.3. A rumour cannot spend 0.3 of an
hour being told in this model, so we round up to the next whole number,
with `math.ceil` from
[Measuring rooms and tins](tutorial:measuring-rooms-and-tins). What do
you expect?

```python exec
id: doubling-rumour-3
import math

print(math.log2(population))
print(math.ceil(math.log2(population)))
```

The loop and the logarithm agree: 23. The loop counts one doubling at
a time. The logarithm gives the count in one step.

### Your turn

1. Change `population` in the first cell to the population of the world,
   about 8,000,000,000. Before you run it, guess how many more hours
   that takes than Ireland did.
2. Now say each person tells *two* new people every hour, so the number
   who know triples. Change `* 2` to `* 3`. How many hours for Ireland?
3. Check your answer to step 2 with `math.log(population, 3)`, which
   asks "how many times do I multiply by 3?" Round it up.

## Grains on a chessboard

There is an old story about the game of chess. The king asked the man
who invented it to name his reward. The man asked for one grain of rice
on the first square of the board, two on the second, four on the third,
and so on, doubling each time, across all 64 squares. The king laughed
at such a small reward.

You met the start of this on
[Numbers a computer can hold](tutorial:numbers-a-computer-can-hold#powers-and-how-many-times),
with cents. Now let's fill the whole board. Square 1 has $2^0 = 1$ grain,
square 2 has $2^1 = 2$, and square $k$ has $2^{k-1}$. The power is one
less than the square's number, because the first square has had no
doublings yet. Multiplying no 2s at all leaves 1, in the same way that
a running product started at 1 on
[Doing it again](tutorial:doing-it-again#pi-multiplying-instead-of-adding).
So $2^0 = 1$.

The cell builds a list of the grains on each square, then adds it up
with your toolkit's `total`. Guess the number of digits in the answer
before you run it.

```python exec
id: doubling-chess-1
grains = []
for square in range(1, 65):
    grains.append(2 ** (square - 1))

print(grains[:8])
print(grains[-1])
print(total(grains))
```

The last square alone has 9,223,372,036,854,775,808 grains, and the
whole board holds 18,446,744,073,709,551,615. If a grain of rice weighs
about 0.02 grams, that is about 369 billion tonnes of rice: hundreds of
times what the whole world grows in a year.

Look at the running total for the first few squares: 1, then 3, then 7,
then 15, then 31. Each is one less than a power of 2. Can you say why
before you run the check?

```python exec
id: doubling-chess-2
for squares in [1, 2, 3, 4, 5, 64]:
    print(squares, total(grains[:squares]), 2 ** squares - 1)
```

The two columns agree every time. Each square holds one more grain than
all the squares before it put together. That is the rumour's last hour
again. In sigma notation:

$$\sum_{k=1}^{64} 2^{k-1} = 2^{64} - 1$$

That number may look familiar. On
[Everything is ones and zeros](tutorial:everything-is-ones-and-zeros#how-many-bits-is-enough),
each extra bit doubled the number of values a byte could hold. A number
kept in 64 bits can be anything from 0 to $2^{64} - 1$. The king's debt
fits in 64 bits exactly, with no room to spare.

### Your turn

1. Which square is the first to hold more than a million grains? Guess,
   then find it with a loop or with `math.log2`.
2. Print `len(str(total(grains)))`. It counts the digits of the total.
   Was your guess close?

## Doublings add up

Double 10 times, then double 5 more times. How many doublings is that?
Fifteen. In powers, that says:

$$2^{10} \times 2^{5} = 2^{15}$$

In words: to multiply two powers of the same base, add the exponents.
This is a *law of powers*: $2^a \times 2^b = 2^{a+b}$. Let's check it,
and try one other thing. What do you notice about `2 ** 10`?

```python exec
id: doubling-add-1
print(2 ** 10 * 2 ** 5, 2 ** 15)
print(2 ** 10)
print(2 ** 20)
print(2 ** 30)
```

$2^{10}$ is 1,024, which is close to a thousand. So 20 doublings is a
thousand times a thousand, about a million, and 30 doublings is about a
billion. That gives a quick way to estimate a logarithm in your head:
$\log_2$ of a million is about 20, and $\log_2$ of a billion is about 30.

Logarithms count doublings, so they add up too. To reach $a \times b$,
double enough times to reach $a$, then enough more to reach $b$ times
that:

$$\log_2(a \times b) = \log_2 a + \log_2 b$$

This is the *law of logarithms* for a product. Will it hold for numbers
that are not powers of 2? Predict, then run it.

```python exec
id: doubling-add-2
print(math.log2(8 * 32), math.log2(8) + math.log2(32))
print(math.log2(1000 * 1000), math.log2(1000) + math.log2(1000))
print(math.log2(1000000))
```

Both lines agree, and $\log_2$ of a million is 19.93, very close to the
estimate of 20.

```question
id: doubling-add-3
type: multiple-choice
correct: 3

About how many doublings take 1 to a trillion, which is a thousand
billion?

- about 13
- about 30
- about 40
- about 1,000
```

## How long to double?

Money in a savings account at 4% a year grows the way prices did on
[Doing it again](tutorial:doing-it-again#pi-multiplying-instead-of-adding):
each year it is multiplied by 1.04. Growth where each step's increase is
added in, and earns its own increase the next time, is called *compound
growth*. It is exponential growth with a base of 1.04 in place of 2.

How many years until €1,000 becomes €2,000? The time it takes a growing
amount to double is its *doubling time*. Guess first. The cell counts
the years, the way the rumour counted hours.

```python exec
id: doubling-money-1
def years_to_double(start, rate_percent):
    """Return how many whole years start takes to double, growing by rate_percent a year."""
    amount = start
    years = 0
    while amount < 2 * start:
        amount = amount * (1 + rate_percent / 100)
        years = years + 1
    return years

print(years_to_double(1000, 4))
print(years_to_double(50, 4))
print(years_to_double(1000, 8))
```

At 4%, it takes 18 years. The start does not matter: €50 also takes 18
years. Only the rate does. At 8% it takes 10 years, a little over half
as long.

Savers have a shortcut for this, the *rule of 72*: divide 72 by the rate
in percent, and you get the doubling time, roughly. $72 \div 4 = 18$,
and $72 \div 8 = 9$. It is a rough rule, close for rates from about 2%
to 10%, and not exact.

The exact question is: which $k$ makes $1.04^k = 2$? That is a
logarithm with base 1.04, written $\log_{1.04} 2$. A logarithm can have
any base, not only 2 or 10. Python's `math.log(x, base)` takes the base
as its second input. What will it give?

```python exec
id: doubling-money-2
print(math.log(2, 1.04))
print(math.log(2, 1.08))
```

About 17.7 years and 9.0 years. The loop counted whole years, so it
rounded up. At 8%, after 9 years, €1,000 has grown to €1,999.00: one
euro short of doubling, so the loop needed a tenth year.

### Doubling in real data

Rules like "4% every year" are steady. Real numbers are not. Here are
Ireland's carbon dioxide emissions from burning fuel and making cement,
in millions of tonnes a year, from 1950 to 2023. The cell loads a file
of every country's emissions, keeps Ireland's rows, and takes two
columns out as lists. Then our own loop finds the first year that
emissions reached 2 times, then 4 times, the 1950 level.

```python exec
id: doubling-co2-1
df = await load_csv("co2-emissions.csv")
ireland = df[df.country == "Ireland"]
years = ireland["year"].tolist()
emissions = ireland["co2"].tolist()

start = emissions[0]
target = 2 * start
for position in range(len(years)):
    if emissions[position] >= target:
        print(years[position], "reached", round(target, 1), "million tonnes")
        target = 2 * target

plt.plot(years, emissions)
for level in [start, 2 * start, 4 * start]:
    plt.axhline(level, color="grey", linestyle="--")
plt.xlabel("year")
plt.ylabel("CO2, millions of tonnes")
```

Emissions doubled by 1971, 21 years after 1950, and doubled again by
1998, 27 years later. The third doubling, to about 78 million tonnes,
never came: emissions stopped growing in the 2000s and have fallen
since. A doubling time describes growth while it lasts. It does not
promise that the growth will go on. The rumour's space assumed an
endless supply of people who have not heard yet; the real world has no
such promise.

### Your turn

1. Try `years_to_double(1000, 2)` and `72 / 2`. How close is the rule of
   72 at 2%? Try 20% too.
2. Change the cell so that it looks for the year Ireland's emissions
   first reached 3 times the 1950 level.

## Halving down to 1

Now the other end. A tennis tournament like Wimbledon starts with 128
players in each singles draw. Every match knocks one player out, so each
round halves the field. How many rounds until one champion is left?

```python exec
id: doubling-halve-1
players = 128
rounds = 0
while players > 1:
    players = players // 2
    rounds = rounds + 1
print(rounds, "rounds")
```

Seven rounds, because $2^7 = 128$. Halving 128 down to 1 takes the same
number of steps as doubling 1 up to 128.

What if the number is not a power of 2? On
[Finding things fast](tutorial:finding-things-fast#how-many-halvings),
1,000 names halved down to 1 in 9 halvings, with `// 2` dropping the
remainder each time, while $\log_2 1000$ is about 9.97. So counting
halvings gives the logarithm rounded down: the number of whole halvings
that fit.

We have now counted halvings several times, so it is time for a tool.
It is the last tool of this unit. Here is its promise, and its body is
yours to write. It is the tennis cell, with `n` in place of `players`.

```python exec
id: doubling-toolkit
toolkit: yes
def halvings(n):
    """Return how many times the whole number n (1 or more) can be halved,
    rounding down each time, before it reaches 1.

    halvings(128) is 7, halvings(1000) is 9 and halvings(1) is 0.
    It is log2(n), rounded down.
    """
    ...
```

```python toolkit-reference
for: doubling-toolkit
def halvings(n):
    """Return how many times the whole number n (1 or more) can be halved,
    rounding down each time, before it reaches 1.

    halvings(128) is 7, halvings(1000) is 9 and halvings(1) is 0.
    It is log2(n), rounded down.
    """
    count = 0
    while n > 1:
        n = n // 2
        count = count + 1
    return count
```

Run the toolkit cell, then the tests. Until `halvings` is written, the
first test stops with an `AssertionError`, because `...` gives back
`None`. The last test checks the promise against `math.log2` for every
whole number up to 10,000.

```python exec
id: doubling-toolkit-tests
assert halvings(128) == 7, "seven rounds of tennis"
assert halvings(1000) == 9, "500, 250, 125, 62, 31, 15, 7, 3, 1"
assert halvings(1) == 0, "1 is already 1"
assert halvings(2) == 1
assert halvings(population) == 22, "one fewer than the rumour's hours"
for n in range(1, 10001):
    assert halvings(n) == math.floor(math.log2(n)), n
print("halvings keeps its promise.")
```

```hint
Try `print(halvings(8))` on its own. What did you expect, and what came
back? Which name in the function should change each time round the loop?
```

```hint
after: 10 errors
title: some steps
1. Start a counter at 0.
2. While `n` is bigger than 1, halve `n` with `// 2` and add 1 to the
   counter.
3. After the loop, give back the counter.

**Think about:** why the loop's condition is `n > 1` and not `n > 0`.
What would `halvings(8)` give with `n > 0`?
```

`math.floor` rounds down, the partner of `math.ceil`. The fifth test says
something worth a second look. 5,149,139 halves 22 times to reach 1,
while the rumour needed 23 doublings to pass it. Halvings round
down and doublings round up, because 5,149,139 sits between $2^{22}$ and
$2^{23}$.

There is one more way to see `halvings`. On
[Everything is ones and zeros](tutorial:everything-is-ones-and-zeros#from-a-number-to-its-bits),
the recipe for binary halved a number again and again. Each `// 2`
drops the last binary digit of a number, so the halvings of $n$ are one
fewer than its number of binary digits. What do you expect `to_binary(1000)` to look
like, and how long?

```python exec
id: doubling-halve-2
print(to_binary(1000), len(to_binary(1000)), halvings(1000))
```

Ten binary digits, and 9 halvings.

Halving with `//` stays in the whole numbers, so it stops at 1. In the
space of fractions it need not stop: $1 \div 2 = \frac{1}{2}$, then
$\frac{1}{4}$, then $\frac{1}{8}$, for ever. Mathematicians write these
as powers too, with a negative exponent: $2^{-1} = \frac{1}{2}$ and
$2^{-3} = \frac{1}{8}$. A *negative exponent* counts halvings, in the
same way a positive one counts doublings. Try `2 ** -3` in any cell.

## Why binary search is so quick

On [Finding things fast](tutorial:finding-things-fast#watching-the-steps-grow),
binary search needed about $\log_2 n$ looks, "one or two more at most".
Now `halvings` lets us say exactly how many. Every look halves what is
left. So the most looks a search can need is the number of halvings that
take $n$ values down to 1, plus one last look at the value that is left:
`halvings(n) + 1`.

Is that promise true for every target, not only the one past the end?
Here is `binary_looks` from that page again. It gives back how many
items a binary search looked at. The cell tries every target in lists
of 10 up to 10,000 numbers, and keeps the largest count. It uses your
`halvings`, so write that first. Before you run it, use `halvings` to
predict the last column.

```python exec
id: doubling-search-1
def binary_looks(sorted_values, target):
    """Binary search sorted_values for target. Return how many items were looked at."""
    low = 0
    high = len(sorted_values) - 1
    looks = 0
    while low <= high:
        middle = (low + high) // 2
        looks = looks + 1
        if sorted_values[middle] == target:
            return looks
        if sorted_values[middle] < target:
            low = middle + 1
        else:
            high = middle - 1
    return looks

for size in [10, 100, 1000, 10000]:
    numbers = list(range(size))
    most = 0
    for target in range(-1, size + 1):
        most = max(most, binary_looks(numbers, target))
    print(size, halvings(size) + 1, most)
```

The last two columns agree. A list of 10,000 values never needs more than 14
looks. A linear search could need all 10,000.

Now put the two ends side by side. The rumour needed 23 doublings to
reach five million people. A phone book of five million names needs at
most 23 looks, which is `halvings(5149139) + 1`. That is the same
number, found from opposite ends:

| | Doubling | Halving |
|---|---|---|
| starts at | 1 | $n$ |
| each step | multiply by 2 | divide by 2, rounding down |
| stops at | $n$ or more | 1 |
| number of steps | $\log_2 n$, rounded up | $\log_2 n$, rounded down |
| where we met it | the rumour, the chessboard | tennis, binary search |

Doubling makes numbers huge fast. Halving makes them small just as fast.
That is why the logarithmic growth of binary search is so slow. Ten
times as many names adds only 3 or 4 looks, because
$\log_2 10 \approx 3.3$. A million times as many adds about 20.

A picture shows the two ends at once. The cell draws the points
$(k, 2^k)$ for doubling and $(2^k, k)$ for halving. What do you think
the grey line $y = x$ is doing between them?

```python exec
id: doubling-search-2
steps = list(range(6))
sizes = []
for k in steps:
    sizes.append(2 ** k)

plt.plot(steps, sizes, marker="o", label="doubling: 2 to the k")
plt.plot(sizes, steps, marker="o", label="halving: log2 of n")
plt.plot([0, 32], [0, 32], color="grey", linestyle="--")
plt.legend()
```

Each curve is the other one reflected in the line $y = x$. On
[Machines that take a number](tutorial:machines-that-take-a-number#running-it-backwards-the-inverse)
we met the inverse of a function: the function that undoes it. Powers of
2 and $\log_2$ are inverses. Put 5 into one, and 32 comes out. Put 32
into the other, and 5 comes back.

### Your turn

1. Without running anything, how many looks can a binary search need in
   a list of 1,000,000 names? Use $2^{10} \approx 1000$.
2. Check your answer with `halvings(1000000) + 1`.
3. A sorted list doubles in size, from 50,000 to 100,000. How many more
   looks can binary search need? How many more for linear search?

<details class="dl-why"><summary>Why this way?</summary>

This page found every logarithm by counting first: hours of a rumour,
rounds of tennis, looks of a search. The logarithm came in afterwards,
as a quick way to get the same count.

Most textbooks go the other way. They define $\log_b x$ as the power
of $b$ that makes $x$, and then practise its laws as algebra:
products, powers and changing the base. That route is quicker to write
down, it makes exam questions on logarithms fast to solve, and it is
what later maths, such as calculus, builds on.

We counted because a count is something you can check with a loop, and
because the count is what connects logarithms to algorithms. The cost is
that this page showed only one law of logarithms, and a logarithm like
9.97 is harder to picture as a count than 10 is.

</details>

## Four questions, looking back

| The question | On this page |
|---|---|
| What is named here? | a counter like `hours` or `rounds`, which turns out to be a logarithm; a base, 2 or 1.04; $k$ in $2^k = n$ |
| What is promised? | `halvings(n)` promises $\log_2 n$ rounded down; $2^a \times 2^b = 2^{a+b}$; $\log_2(ab) = \log_2 a + \log_2 b$ |
| What happens when? | each doubling or halving happens after the one before; the last doubling adds more than all the ones before it |
| What does this space let us do? | Python's whole numbers hold $2^{64} - 1$ exactly; `//` stops halving at 1, while fractions halve for ever; a model of a rumour doubles for ever, and people do not |

## What we have now

| Term or tool | What it means |
|---|---|
| exponential growth | multiplying by the same amount at every step, as $2^k$ does |
| $2^0 = 1$ | no doublings yet: nothing multiplied gives 1 |
| $2^a \times 2^b = 2^{a+b}$ | a law of powers: doublings add |
| $2^{10} \approx 1000$ | a way to estimate: 20 doublings is about a million |
| $\log_2(ab) = \log_2 a + \log_2 b$ | a law of logarithms: the counts add |
| compound growth | growth where each step's increase earns its own increase next time |
| doubling time, rule of 72 | how long a growing amount takes to double; roughly 72 divided by the rate in percent |
| `math.log(x, base)` | a logarithm with any base: how many times do I multiply by `base`? |
| `math.floor(x)` | $x$ rounded down to a whole number |
| `halvings(n)` | your toolkit tool: how many times $n$ halves down to 1, which is $\log_2 n$ rounded down |
| negative exponent, $2^{-k}$ | $k$ halvings of 1: $2^{-3} = \frac{1}{8}$ |
| $2^k = n$ and $k = \log_2 n$ | one fact from two ends: doublings up from 1, halvings down from $n$ |

The practice page is next, and then the mixed problems for this unit,
where a phone book of 100,000 names is searched three ways.
