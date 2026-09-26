---
title: "Counting: factorials, permutations and combinations — Practice"
practice_for: counting-carefully
year: "2026-2027"
version: 2026.09.26.1
worlds:
  games-of-chance: Dice, cards and coins, and the games people play with them.
  book-characters: The people in six novels, chapter by chapter.
datasets: [book-characters]
---

# Counting: factorials, permutations and combinations — Practice

Here are problems on counting, some on paper, some in code, and three
from earlier pages. Before you start each one, ask two questions:

1. Does the order matter?
2. Can the same thing be chosen more than once?

The two answers tell you which count to use. Choosing the count is the
hard part of these problems. The arithmetic after it is easy.

## Tools

Python's `math` module has the three counts built in: `math.factorial(n)`,
`math.perm(n, r)` and `math.comb(n, r)`. `itertools` lists the cases,
so you can check a formula on small numbers. Run this cell once
before you start.

```python exec
id: tools-1
import itertools
import math

print(math.factorial(5), math.perm(5, 3), math.comb(5, 3))
print(len(list(itertools.permutations(range(5), 3))))
```

## Factorials

**1.** What are $0!$, $1!$, $5!$ and $10!$?

<details class="dl-answer"><summary>answer</summary>

1, 1, 120 and 3,628,800.

$0! = 1$ is a definition. We agree on it. We do not calculate it. It is
the only value that keeps every formula on the page working, and it makes
sense too, because there is exactly one way to arrange nothing.

</details>

**2.** Can you simplify $\frac{10!}{8!}$ and $\frac{n!}{(n-2)!}$ without
calculating the factorials?

<details class="dl-answer"><summary>answer</summary>

90, and $n(n-1)$.

$\frac{10!}{8!} = 10 \times 9 = 90$. Every number from 8 down to 1 is on
both the top and the bottom, so they cancel. Because they cancel, a
permutation count for a large $n$ never needs a huge number.

</details>

**3.** Factorials grow fast. How many digits does $100!$ have?

```python exec
id: counting-hundred-factorial
import math

print("20! has", len(str(math.factorial(20))), "digits")
print("100! has", len(str(math.factorial(100))), "digits")
```

```predict
type: number
tolerance: 10

How many digits does $100!$ have? Your guess can be up to 10 away.
```

<details class="dl-answer"><summary>what the size means</summary>

158 digits. The number of atoms in the part of the universe we can
observe is thought to have about 81. Even $20!$ is
2,432,902,008,176,640,000. A program that tries every order of 20 things
will not finish.

</details>

## Arrangements

**4.** How many 4-letter arrangements can be made from the letters of
`COMPUTER`, with no letter used twice? Can you count them by listing,
then check with `math.perm`?

```python exec
id: counting-computer
import itertools
import math

arrangements = 0
```

```inputs
arrangements
```

```hint
`itertools.permutations("COMPUTER", 4)` lists them. How many letters are
there to choose from, and how many places?
```

```solution
import itertools
import math

arrangements = len(list(itertools.permutations("COMPUTER", 4)))
print(arrangements, math.perm(8, 4))
---
Both ways give 1,680, which is $8 \times 7 \times 6 \times 5$. The eight
letters of COMPUTER are all different, which keeps this one short. The
next problem has letters that repeat.
```

**5.** How many different arrangements are there of the letters of
`LETTER`? Listing gives $6! = 720$ orders, but some of them spell the
same word. Can you count the different words?

```python exec
id: counting-letter
import itertools

orders = list(itertools.permutations("LETTER"))
print(len(orders), "orders")
```

```inputs
len(set(orders))
```

```hint
Put the orders in a set. Two orders that spell the same word are the same
tuple, so the set keeps one of them.
```

```solution
import itertools
import math

orders = list(itertools.permutations("LETTER"))
print(len(orders), "orders")
print(len(set(orders)), "different words")
print(math.factorial(6) // (math.factorial(2) * math.factorial(2)))
---
There are 180 different words. Swapping the two Es gives the same word,
so every word is counted twice. The two Ts double it again. The formula
divides by $2!$ for each repeated letter:
$\frac{720}{2 \times 2} = 180$. In general, start with the factorial of
the number of letters, and divide by the factorial of each repeat count.
```

## Choices

**6.** In how many ways can you choose a committee of 3 from 8 people?
And how many ways to fill three different posts (chair, secretary and
treasurer) from the same 8?

<details class="dl-answer"><summary>answer</summary>

There are 56 committees, and 336 ways to fill the posts.

The posts are a permutation, $P(8, 3) = 8 \times 7 \times 6 = 336$. A
committee has no posts, so each committee of 3 was counted once for each
of its $3! = 6$ orders: $336 \div 6 = 56 = C(8, 3)$. The number of combinations
is the number of permutations divided by $r!$.

</details>

**7.** Here is one line of choices: 5 things, choosing none of them, one,
two, and so on up to all five.

```python exec
id: counting-row-of-five
import math

row = [math.comb(5, r) for r in range(6)]
print(row)
print(sum(row))
```

```predict
type: number

What does the last line print, the total of the row?
```

<details class="dl-answer"><summary>what the row shows</summary>

The row is 1, 5, 10, 10, 5, 1, and the total is 32. The row is the same
forwards and backwards, because choosing 2 to keep is choosing 3 to
leave: $C(n, r) = C(n, n-r)$.

The total is $2^5$. Each of the five things is either in the choice or
out of it: two ways, five times. The row counts those same 32 choices,
sorted by size.

The row is also a row of *Pascal's triangle*, a triangle of numbers with
1 at each end of every row, where each number inside is the sum of the
two above it. Its rows start 1; then 1 1; then 1 2 1; then 1 3 3 1. The
same rows appear again in
[Polynomials: representing and combining them in Python](tutorial:expressions-come-alive),
when we expand $(x+1)^5$.

</details>

**8.** The Irish Lotto asks for 6 numbers from 47. How many different
tickets are there? And how many if the order of the numbers mattered?

<details class="dl-answer"><summary>answer</summary>

$C(47, 6) = 10{,}737{,}573$. With one ticket a week, a win would come
about once in 206,000 years.

If the order mattered, it would be $P(47, 6)$, about 7,700,000,000. That
is 720 times more, since each ticket's six numbers come in $6! = 720$
orders.

</details>

**9.** A pizza place has 10 toppings. How many pizzas have exactly 3
toppings? How many have any number of toppings, including none?

<details class="dl-answer"><summary>answer</summary>

120, and 1,024. Exactly 3 is $C(10, 3) = 120$. For any number, each
topping is on or off: 2 ways, ten times, so $2^{10} = 1{,}024$. It is
the question from problem 7 again, with 10 things in place of 5.

</details>

## Choosing the right tool

```question
id: counting-which-tool
type: fill-in-the-blank

- Choosing 3 books from 10 to take on holiday is a {combination|permutation|power}.
- Choosing a president, secretary and treasurer from 10 members is a {permutation|combination|power}.
- A 5-letter password from 26 letters, where letters may repeat, is a {power|permutation|combination}.
- Ranking your top 3 films from a list of 20 is a {permutation|combination|power}.
```

**10.** Can you calculate each of the four counts in the question above?

<details class="dl-answer"><summary>answer</summary>

$C(10, 3) = 120$ books; $P(10, 3) = 720$ ways to fill the posts, since
the three posts are different; $26^5 = 11{,}881{,}376$ passwords; and
$P(20, 3) = 6{,}840$ rankings. The same two questions decide every one:
does the order matter, and can a choice appear again?

</details>

## Your world

**11.** Here is a count from the world you chose.

<div class="dl-world" data-world="games-of-chance">

Roll four dice. How many of the $6^4$ outcomes show at least one six? Can
you count them by listing, then find a shorter way?

```python exec
id: counting-world--games-of-chance
import itertools

rolls = list(itertools.product(range(1, 7), repeat=4))
print(len(rolls), "outcomes")

at_least_one_six = 0
```

```inputs
at_least_one_six
```

```hint
`6 in roll` is `True` when a roll shows a six. For the shorter way, how
many outcomes show no six at all?
```

```solution
import itertools

rolls = list(itertools.product(range(1, 7), repeat=4))
print(len(rolls), "outcomes")

at_least_one_six = 0
for roll in rolls:
    if 6 in roll:
        at_least_one_six = at_least_one_six + 1
print(at_least_one_six, 6 ** 4 - 5 ** 4)
---
671 of the 1,296 outcomes show a six. The shorter way counts the rest:
$5^4 = 625$ outcomes have no six, so $1{,}296 - 625 = 671$ have at least
one. Counting the opposite is often easier than counting "at least one".
671 is just over half of 1,296, so a bet on a six in four rolls wins
slightly more often than it loses. In the 1650s, a French gambler, the
Chevalier de Méré, asked about bets like this one, and his questions
helped to start the study of probability. That is the next page.
```

</div>

<div class="dl-world" data-world="book-characters">

*The Time Machine* has seven people in the book's data. How many pairs of
them are there? How many of those pairs are ever named in the same
chapter, and which pairs never are?

```python exec
id: counting-world--book-characters
import itertools

characters = await load_csv("book-characters.csv")
book = characters[(characters.book == "the-time-machine") & (characters.mentions > 0)]
people = sorted(book.character.unique())
print(people)

met = set()
```

```inputs
len(met)
```

```hint
For each chapter, `itertools.combinations` of the sorted names in that
chapter gives the pairs named together. Add each to `met`.
`book.groupby("chapter")` gives the chapters one at a time.
```

```solution
import itertools
import math

characters = await load_csv("book-characters.csv")
book = characters[(characters.book == "the-time-machine") & (characters.mentions > 0)]
people = sorted(book.character.unique())
print(len(people), "people,", math.comb(len(people), 2), "pairs")

met = set()
for chapter, rows in book.groupby("chapter"):
    for pair in itertools.combinations(sorted(rows.character), 2):
        met.add(pair)
print(len(met), "pairs meet")
for pair in itertools.combinations(people, 2):
    if pair not in met:
        print(pair)
---
There are 21 pairs, and 14 of them are named in the same chapter. Each
of the seven that never are puts one of the Time Traveller's dinner
guests (Filby, the Medical Man, the Psychologist) beside someone from
the year 802,701: Weena, the Eloi or the Morlocks. The count shows the
book's two times without reading a page of it. Only Weena crosses
between them. In chapter 16, the Medical Man examines the flowers she
put in the Time Traveller's pocket.
```

</div>

## Passwords

**12.** Which is stronger: a 10-character password from 72 characters,
or four words chosen at random from a list of 10,000? Can you count both
before you open the answer?

<details class="dl-answer"><summary>answer</summary>

The characters are stronger, by this count.
$72^{10} \approx 3.7 \times 10^{18}$, against $10{,}000^4 = 10^{16}$,
about 370 times fewer. From a list of 50,000 words, four give
$6.25 \times 10^{18}$, slightly more than the characters.

The count does not tell you everything. People can remember four words.
Ten random characters get written on a note, and then the password is only
as safe as the note.

</details>

**13.** A company asks for "at least one capital letter, one digit and
one symbol". Does the rule make passwords stronger?

<details class="dl-answer"><summary>answer</summary>

It makes the number of possible passwords smaller. It removes every
password without a capital, a digit and a symbol, and adds none.

It does stop the weakest choices, which helps against an attacker who
tries lowercase words first. But it also produces `Password1!` again and
again, because people follow a rule in the easiest way they can. Counting
the possible passwords is easy. Guessing which ones people choose is the
hard problem, and counting cannot answer it.

</details>

## One longer one

**14.** Choose six numbers from 47, where a number may be chosen more
than once and the order does not matter. How many choices are there? The
count for $r$ choices from $n$ with repeats is $C(n + r - 1, r)$. Can
you check the formula on small numbers first, with
`itertools.combinations_with_replacement`?

```python exec
id: counting-with-repeats
import itertools
import math

n = 5
r = 3
listed = len(list(itertools.combinations_with_replacement(range(n), r)))
print(listed)
```

```inputs
listed
```

```solution
import itertools
import math

n = 5
r = 3
listed = len(list(itertools.combinations_with_replacement(range(n), r)))
print(listed, math.comb(n + r - 1, r))
print(math.comb(47 + 6 - 1, 6))
---
Both ways give 35 for 3 from 5. The lottery with repeats has
$C(52, 6) = 20{,}358{,}520$, about twice the real one. Here is why the
formula works. Picture $r$ dots and $n - 1$ bars in one row, $n + r - 1$
places in all. The bars split the row into $n$ groups, one for each
number, and the dots in a group say how many times that number was
chosen. Each choice is one way to pick which $r$ of the places hold
dots.
```

## From earlier

**15.** From *Repeating steps with loops*. This loop should calculate
$5!$, but starts its product in the wrong place. What does it print?

```python exec
id: counting-from-earlier-product
product = 0
for i in range(1, 6):
    product = product * i
print(product)
```

```predict
type: number

What will it print?
```

<details class="dl-answer"><summary>why</summary>

0. Zero times anything is zero, so the product never leaves 0. A sum
starts at 0, because adding 0 changes nothing. A product starts at 1,
because multiplying by 1 changes nothing.

</details>

**16.** From *Venn diagrams*. How many whole numbers from 1 to 100 divide
by 2 or by 3? Can you count them with inclusion-exclusion first, and then
check?

```python exec
id: counting-from-earlier-two-or-three
count = 0
for n in range(1, 101):
    if n % 2 == 0 or n % 3 == 0:
        count = count + 1
print(count)
```

<details class="dl-answer"><summary>answer</summary>

67. 50 divide by 2 and 33 by 3, but the 16 that divide by 6 were counted
twice: $50 + 33 - 16 = 67$.

</details>

**17.** From *Logic and truth*. A truth table for two inputs has four
rows. How many
different truth tables are there for two inputs? That is, how many
different ways could an operator like `and` or `or` behave?

<details class="dl-answer"><summary>answer</summary>

16. Each of the four rows gives `True` or `False`: two choices, four
times, so $2^4 = 16$. `and`, `or` and XOR are three of the 16. The
multiplication principle counted them. `itertools.product([False, True],
repeat=4)` would list them.

</details>
