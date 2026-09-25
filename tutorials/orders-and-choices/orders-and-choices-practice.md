---
title: "Orders and choices: factorials, permutations and combinations — Practice"
practice_for: orders-and-choices
year: "2026-2027"
version: 2026.09.25.1
---

# Orders and choices: factorials, permutations and combinations — Practice

Each problem says what kind it is. **Predict** means guess first, then
run. **Make** means write something new. **Fix** means find one mistake
in code that looks fine. **Explain** means answer in words. **Another
way** means reach the same place by a second route. The answers are
folded away until you open them, and each shows one good way: yours may
be different, and as good. The last few problems are meant to be
hard. If one feels like hard work, that is the right feeling.

Your toolkit is loaded on this page: `factorial`, `permutations` and
`combinations` from the tutorial, and `total`, `product` and `all_pairs`
from the two pages before it. If you have not written one of them
yourself, the reference version is used, so every problem works.

## Warm-up

Use this cell for any of the warm-up problems.

```python exec
id: orders-practice-warm-up
print(factorial(5))
```

**1. Predict.** Five programs are waiting to run on a computer, one
after another. In how many different orders can they run? Guess, then
run the cell above.

<details class="dl-answer"><summary>answer</summary>

120. Any of the 5 programs can go first, then any of the 4 left, and so on:
$5 \times 4 \times 3 \times 2 \times 1 = 5! = 120$.

</details>

**2. Make.** A podcast app will play 3 of your 10 saved episodes, one
after another. How many different running orders could it play? Decide
which toolkit function fits, and use it.

<details class="dl-answer"><summary>answer</summary>

```python
print(permutations(10, 3))
```

This prints `720`. The order matters, because the same three episodes in
a different order make a different evening, and none is played twice. So
it is $P(10, 3) = 10 \times 9 \times 8 = 720$.

</details>

**3. Explain.** $P(n, n)$ counts the ways to fill all $n$ places with $n$
things. Why is it always the same as $n!$? Which agreement from the
tutorial makes the formula $\frac{n!}{(n-n)!}$ give the right answer?

<details class="dl-answer"><summary>answer</summary>

Filling all $n$ places is the same as putting all $n$ things in order,
which is what $n!$ counts. In the formula, the bottom is $(n-n)! = 0!$.
Because we agreed that $0! = 1$, the formula gives $\frac{n!}{1} = n!$.
Without that agreement, the formula would break at exactly this point.

</details>

**4. Predict.** A weather balloon can carry sensors, and there are 6 to
choose from. What do `combinations(6, 1)` and `combinations(6, 6)` give?
Say in words what each one counts before you run them.

<details class="dl-answer"><summary>answer</summary>

```python
print(combinations(6, 1), combinations(6, 6))
```

This prints `6 1`. There are 6 ways to choose one sensor: one for each
sensor. There is only 1 way to choose all six: take everything.

</details>

## Core

Use this cell for any of the core problems.

```python exec
id: orders-practice-core
print(combinations(11, 4))
```

**5. Make.** A team for a group project needs 4 people, and 11 people in
your class would like to be on it. Nobody has a special role. How many
different teams are possible?

<details class="dl-answer"><summary>answer</summary>

```python
print(combinations(11, 4))
```

This prints `330`. The order does not matter, because a team is the same
team whoever joins first, and nobody can take two places. So it is
$C(11, 4) = \frac{11!}{4!\,7!} = 330$.

</details>

**6. Fix.** Schlomi, who is learning Python too, writes her own
combinations function. It should say there are 6 ways to fit 2 sensors
from 4. Run it and see what it says instead. Then find the one
mistake.

```python exec
id: orders-practice-fix-brackets
def my_combinations(n, r):
    """The ways to choose r things from n, when order does not matter."""
    return factorial(n) // factorial(r) * factorial(n - r)

print(my_combinations(4, 2))
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Work out the line by hand with $n = 4$ and $r = 2$: what are the three
   factorials?
2. `//` and `*` have the same rank in the order of operations. Which one
   does Python do first?
3. The formula has $r!\,(n-r)!$ together on the bottom of the fraction.

**Think about:** what the brackets in the formula
$\frac{n!}{r!\,(n-r)!}$ would look like if you wrote them on one line.

</details>

<details class="dl-answer"><summary>answer</summary>

It prints `24`. Python does `//` and `*` from left to right, so it works
out $24 \div 2 = 12$ first, and then multiplies by $2! = 2$ to get 24.
The whole bottom of the fraction needs brackets, so that it is worked
out first:

```python
def my_combinations(n, r):
    """The ways to choose r things from n, when order does not matter."""
    return factorial(n) // (factorial(r) * factorial(n - r))

print(my_combinations(4, 2))
```

Now it prints `6`. Schlomi had the formula right; the line said
something else. This is the order of operations from
[Numbers a computer can hold](tutorial:numbers-a-computer-can-hold#which-comes-first),
in a new place.

</details>

**7. Predict.** Five computers in a lab are joined so that every pair
has its own cable. The loop below counts the cables. How many will it
count? Guess first, then paste it into the core cell and run it.

```python
computers = 5
cables = 0
for first in range(computers):
    for second in range(first + 1, computers):
        cables = cables + 1
print(cables)
```

<details class="dl-answer"><summary>answer</summary>

10. The second loop always starts after the first, so each pair of
computers is counted once. The first computer needs 4 cables, the
second 3 new ones, then 2, then 1: $4 + 3 + 2 + 1 = 10$. A cable joins a
choice of 2 computers where the order does not matter, so it is also
$C(5, 2) = 10$. With 50 computers it would be $C(50, 2) = 1225$ cables,
which is why real networks join computers through a switch instead.

</details>

**8. Another way.** In the tutorial, the first three of eight jobs were
$P(8, 3) = 336$, found with `factorial`. Find the same 336 a second way,
with `product` from
[Doing it again](tutorial:doing-it-again).

<details class="dl-answer"><summary>answer</summary>

```python
print(product([8, 7, 6]))
print(product(range(6, 9)))
```

Both print `336`. The first writes out the three choices, 8, 7 and 6.
The second lets `range(6, 9)` make them: 6, 7 and 8. The order of the
numbers does not change a product. This route never works out $8!$ at
all, so it does less work than the factorial formula.

</details>

**9. Explain.** Schlomo, who is learning Python too, has a bike lock
with 4 wheels, each with the digits 0 to 9. He calls it a "combination
lock", so he works out `combinations(10, 4)` and gets 210 settings. Is
the number of settings a combination, in the sense of this page? What
is the right count?

<details class="dl-answer"><summary>answer</summary>

No, though the name of the lock makes his move a reasonable one. The
order matters: 1234 and 4321 open different locks. A digit can
also repeat, as in 0077. So neither $C(n, r)$ nor $P(n, r)$ fits. It is
the counting principle from
[Counting every outfit](tutorial:counting-every-outfit): 10 choices for
each of 4 wheels, $10^4 = 10{,}000$ settings.

A mathematician might call it a "permutation lock with repeats". The
everyday name is fine for a shop, but it is not the maths name.

</details>

**10. Fix.** A flag has three stripes, each a different colour, from
green, white and orange. This loop should count the different flags. It
counts 12. Run it, then find the mistake.

```python exec
id: orders-practice-fix-flags
colours = ["green", "white", "orange"]
flags = 0
for left in colours:
    for middle in colours:
        for right in colours:
            if left != middle and middle != right:
                flags = flags + 1
print(flags)
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. There are three stripes. How many pairs of stripes must be different?
2. The `if` checks two pairs. Which pair does it miss?
3. Add one print line inside the `if` to see the rows it keeps.

**Think about:** which kept rows would not be a flag of three different
colours.

</details>

<details class="dl-answer"><summary>answer</summary>

The `if` never checks `left` against `right`, so it keeps flags such as
green, white, green. Three stripes make three pairs, and all three must
differ:

```python
if left != middle and middle != right and left != right:
```

Now it counts 6, which is $3!$. The mistake is a realistic one: with
more loops, the number of pairs to check grows quickly, and anyone can
miss one. That is one reason to reach for a formula, or
for `itertools`.

</details>

**11. Make.** Two questions about music and cards. For each, decide
first whether the order matters, then work it out.

1. A running playlist uses 4 different songs from a list of 12, in
   order.
2. A poker hand is 5 cards dealt from a deck of 52.

<details class="dl-answer"><summary>answer</summary>

```python
print(permutations(12, 4))
print(combinations(52, 5))
```

The playlist is ordered, so it is $P(12, 4) = 11{,}880$. A hand of cards
is the same hand in any order you pick it up, so it is
$C(52, 5) = 2{,}598{,}960$.

</details>

## Stretch

Use this cell for any of the stretch problems.

```python exec
id: orders-practice-stretch
for lit in range(0, 8):
    print(lit, combinations(7, lit))
```

**12. Make.** A seven-segment display has seven bars of light. The cell
above prints $C(7, r)$ for every $r$ from 0 to 7: the number of
patterns with exactly $r$ segments lit. Put those eight numbers in a
list and add them up with `total`. What do you get, and where have you
seen that number before?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Start with an empty list, and `append` each count inside the loop.
2. Call `total` on the list after the loop.
3. Compare the answer with $2^7$.

**Think about:** a truth table with 7 inputs, one for each segment. How
many of its rows have exactly 2 inputs True?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
counts = []
for lit in range(0, 8):
    counts.append(combinations(7, lit))
print(counts)
print(total(counts), 2 ** 7)
```

The counts are `[1, 7, 21, 35, 35, 21, 7, 1]`, and they add up to 128,
which is $2^7$: the 128 patterns from
[Numbers a computer can hold](tutorial:numbers-a-computer-can-hold#powers-and-how-many-times).
Each pattern is a choice of which segments are lit. So $C(7, 2) = 21$
patterns light exactly two, and all the choices together are all the
patterns. The digit 1 is one of those 21: it lights two segments.

</details>

**13. Another way.** In the tutorial, the ways to fit two sensors from
four were counted with two loops. Count them another way, with
`all_pairs` from
[Counting every outfit](tutorial:counting-every-outfit). Make every pair
of positions, then keep only the pairs where the first position is
smaller.

<details class="dl-answer"><summary>answer</summary>

```python
sensors = ["camera", "thermometer", "microphone", "location"]
fittings = 0
for first, second in all_pairs(range(4), range(4)):
    if first < second:
        print(sensors[first], "and", sensors[second])
        fittings = fittings + 1
print(fittings)
```

This prints the same six pairs of sensors, and `6`. The line
`for first, second in` takes each pair apart into its two values.
`all_pairs` makes all 16
pairs of positions. Four of them use a sensor twice, and of the other
12, each choice appears twice, once in each order. Keeping `first <
second` keeps each choice once: $16 - 4 = 12$, and $12 \div 2 = 6$.

</details>

**14. Make.** A EuroMillions ticket picks 5 main numbers from 1 to 50,
and 2 "lucky star" numbers from 1 to 12. Order does not matter in either
part. How many different tickets are there?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Count the ways to choose the 5 main numbers.
2. Count the ways to choose the 2 lucky stars.
3. Each choice of main numbers can go with each choice of stars. Which
   rule from the last page joins two counts like that?

**Think about:** why we multiply here, and do not add.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
main_numbers = combinations(50, 5)
lucky_stars = combinations(12, 2)
print(main_numbers, lucky_stars, main_numbers * lucky_stars)
```

There are 2,118,760 ways to choose the main numbers and 66 ways to
choose the stars. By the counting principle, every choice of one goes
with every choice of the other, so there are
$2{,}118{,}760 \times 66 = 139{,}838{,}160$ tickets, about 13 times as
many as the Irish Lotto.

</details>

**15. Predict.** How many digits does $100!$ have? Guess first: 10, 50,
150 or 1,000? Then find out with `str()`, from
[When Python says no](tutorial:when-python-says-no), and `len()`.

<details class="dl-answer"><summary>answer</summary>

```python
print(len(str(factorial(100))))
```

It has 158 digits. `str()` turns the number into text, and `len()`
counts its characters. Python's ints never run out of room, as
[Numbers a computer can hold](tutorial:numbers-a-computer-can-hold)
promised, so every one of those digits is exact.

</details>

**16. Explain.** A phone app only allows 4-digit PINs whose digits go
up from left to right, with no repeats, like 1357 or 0289. How many PINs
are left? Explain why this is a combination, even though order matters
in a PIN.

<details class="dl-answer"><summary>answer</summary>

```python
print(combinations(10, 4))
```

There are 210 such PINs. Choose any 4 different digits, and there is
exactly one way to write them in increasing order. So each choice of
digits gives one PIN, and the count is $C(10, 4) = 210$. Order matters
in a PIN, but here the rule has already fixed the order for us. That
leaves only the choice.

Compare that with $10^4 = 10{,}000$ PINs with no rule. This rule makes
a PIN about 48 times easier to guess.

</details>
