---
title: "Logic: truth tables, XOR and De Morgan's laws"
year: "2026-2027"
version: 2026.09.26.1
worlds:
  games-of-chance: Dice, cards and coins, and the games people play with them.
  dinosaurs: Dinosaurs and their fossils, what has been found, where, and how old it is.
  exoplanets: Planets around other stars, and the ways they were found.
datasets: [exoplanets]
covers:
  every-possible-case:
    covers: [MIT-2.4]
  exclusive-or:
    covers: [MIT-2.4]
  de-morgans-laws:
    covers: [MIT-2.5]
  where-you-have-already-used-this:
    covers: [MIT-2.5]
  the-same-shapes-on-sets:
    covers: [MIT-2.5]
---

# Logic: truth tables, XOR and De Morgan's laws

Here is a game. Roll two dice. You win on a double, or when they add up
to 7. A friend writes the rule in code, and it works:

```python exec
id: logic-a-tangled-rule
def wins(first, second):
    return not (first != second and first + second != 7)


print(wins(3, 3), wins(2, 5), wins(1, 4))
```

It works, and it is hard to read: two `!=`, an `and`, and a `not` around
all of it. On this page we see why it gives the right answers, and how
to write it more simply.

You have been writing `and`, `or` and `not` since
[Making decisions](tutorial:making-decisions). On the last two pages,
[Sets](tutorial:sets-as-sorted-lists) and
[Venn diagrams](tutorial:venn-diagrams), union, intersection and
complement followed rules of their own. Here the same rules appear
again, with true and false.

## Every possible case

An `and` takes two values, each either `True` or `False`, and returns
one. Each input has only two possibilities, so there are only four
situations, few enough to list them all. A *truth table* lists every
combination of inputs, with the result for each:

```python exec
id: every-possible-case-1
print("   A        B      A and B")
for a in [True, False]:
    for b in [True, False]:
        print(f"{str(a):>6} {str(b):>7} {str(a and b):>10}")
```

A loop made the four rows. Nobody typed them. You get a truth table when
you try every input, so there is no need to memorise one. Here
are the tables for `or` and `not`:

```python exec
id: every-possible-case-2
print("   A        B      A or B")
for a in [True, False]:
    for b in [True, False]:
        print(f"{str(a):>6} {str(b):>7} {str(a or b):>10}")

print()
print("   A      not A")
for a in [True, False]:
    print(f"{str(a):>6} {str(not a):>10}")
```

Before you look at the first row of the `or` table, here is a question:

```python exec
id: logic-true-or-true
print(True or True)
```

```predict
What does `True or True` give?

- True
  - `or` is true when at least one side is true, and here both are.
- False
  - "Tea or coffee?" does not expect the answer "both".
```

The logical `or` includes "both". Everyday English usually does not. If
someone asks "tea or coffee?", they do not expect "both". This difference
confuses most people at least once.

### Your turn

What would the truth table for `A and (not B)` look like? Can you
predict the four rows, then write a loop that prints them?

```python exec
id: your-turn-1
# Your loop here
```

```inputs
[a and (not b) for a in [True, False] for b in [True, False]]
```

```hint
Copy the loop for `and`, and change what goes in the last column. Which
of the four rows do you expect to be `True`?
```

```solution
print("   A        B    A and (not B)")
for a in [True, False]:
    for b in [True, False]:
        print(f"{str(a):>6} {str(b):>7} {str(a and (not b)):>13}")
---
Only one row is `True`: A true and B false. The input shows the four
results in the loop's order, `[False, True, False, False]`. In sets, it
is the left circle without the overlap: A minus B.
```

## Exclusive or

The everyday "or", the one without "both", has a name too.
*Exclusive or*, or *XOR*, is true when exactly one of its two inputs is
true. You met it on the Venn page as `^` between sets. It means in one
circle or the other, not both.

Python has no `xor` keyword, so we build it, three ways. What do you
expect in the three columns?

```python exec
id: exclusive-or-1
def xor_written_out(a, b):
    return (a or b) and not (a and b)


print("   A        B     XOR    !=     ^")
for a in [True, False]:
    for b in [True, False]:
        print(f"{str(a):>6} {str(b):>7} {str(xor_written_out(a, b)):>7}"
              f" {str(a != b):>5} {str(a ^ b):>5}")
```

The three columns are the same all the way down. Look at the middle one.
For `True` and `False`, "exclusive or" and "not equal to" are the *same
operation*. If exactly one of the two is true, the two are different.
The third column uses `^`, Python's *bitwise XOR*, which works on whole
numbers one binary digit at a time, and gives the right answer for
`True` and `False` too.

### Your turn

Can you write XOR a fourth way, using only `not` and `==`?

```python exec
id: your-turn-2
def xor_again(a, b):
    """Return True when exactly one of a and b is True."""
    # Your code here


print(xor_again(True, False), xor_again(True, True))
```

```inputs
xor_again(True, True)
xor_again(True, False)
xor_again(False, True)
xor_again(False, False)
```

```hint
The middle column above says XOR is "not equal". How do you say "not
equal" with `not` and `==`?
```

```solution
def xor_again(a, b):
    """Return True when exactly one of a and b is True."""
    return not (a == b)


print(xor_again(True, False), xor_again(True, True))
---
`not (a == b)` is `a != b`, the middle column, written with the two
pieces the task allowed. Four inputs is every case, so the table of
inputs is the whole proof.
```

## De Morgan's laws

Here is a question most people find hard, even after a month of writing
conditions: what is `not (A and B)` the same as? The cell checks two
possible answers against every case, and prints the one that matches.

```python exec
id: logic-which-one-matches
cases = [(a, b) for a in [True, False] for b in [True, False]]
or_version = all((not (a and b)) == ((not a) or (not b)) for a, b in cases)
and_version = all((not (a and b)) == ((not a) and (not b)) for a, b in cases)
if or_version:
    print("(not A) or (not B)")
if and_version:
    print("(not A) and (not B)")
```

```predict
Which one will it print?

- (not A) or (not B)
  - "Not both" means at least one of them is missing.
- (not A) and (not B)
  - The `not` goes inside the bracket, onto each part, and the `and` stays.
```

*De Morgan's laws* are two rules for moving a `not` inside a bracket:

> `not (A and B)` is the same as `(not A) or (not B)`
>
> `not (A or B)` is the same as `(not A) and (not B)`

When a `not` moves inside a bracket, each `and` becomes an `or`, and each
`or` becomes an `and`. The rules are easy to state and hard to believe,
so here is the whole table for each:

```python exec
id: de-morgans-laws-1
print("   A        B    not(A and B)   (not A) or (not B)")
for a in [True, False]:
    for b in [True, False]:
        left = not (a and b)
        right = (not a) or (not b)
        print(f"{str(a):>6} {str(b):>7} {str(left):>12} {str(right):>18}")
```

```python exec
id: de-morgans-laws-2
print("   A        B    not(A or B)   (not A) and (not B)")
for a in [True, False]:
    for b in [True, False]:
        left = not (a or b)
        right = (not a) and (not b)
        print(f"{str(a):>6} {str(b):>7} {str(left):>12} {str(right):>19}")
```

In both, the two columns match in every row. There are exactly four
cases, and the loop tried all four. So the loop is a proof, not just an
example.

That is unusual. "I tested it and it worked" is usually a weak argument,
since testing a few inputs cannot show that a program works for every
input. Here the argument is complete, because there are only four inputs,
and we tried every one. This only works when there are few enough cases
to check them all.

## Where you have already used this

De Morgan's laws turn conditions that are hard to read into conditions
that are easy to read. Here is the game from the top of the page again:

```python exec
id: where-you-have-already-used-this-1
def wins_readable(first, second):
    return first == second or first + second == 7


rolls = [(first, second) for first in range(1, 7) for second in range(1, 7)]
print("agree on every roll:", all(wins(f, s) == wins_readable(f, s) for f, s in rolls))
```

`all()` returns `True` when every value it gets is `True`. Here it gets
one comparison for each of the 36 rolls. The first version has a
`not` around an `and`. De Morgan turns it into an `or` of two `not`s, and
`not (first != second)` is `first == second`. That is the rule as the
game states it.

People rarely write the tangled version on purpose. It grows a little at
a time: someone adds a condition, later wraps the whole thing in a
`not`, then adds another. The laws let you untangle it afterwards.

### Your turn

Here are three conditions to simplify. Can you write a simpler version of
each, and check that it agrees with the original in every case?

```python exec
id: your-turn-3
def one(a, b):
    return not (a and not b)


def two(a, b):
    return not (not a and not b)


def three(a, b, c):
    return not (a or (b and not c))


def one_simple(a, b):
    """The same as one(a, b), with no not outside a bracket."""


def two_simple(a, b):
    """The same as two(a, b), with no not at all."""


def three_simple(a, b, c):
    """The same as three(a, b, c), with no not outside a bracket."""
```

```inputs
[one_simple(a, b) for a in [True, False] for b in [True, False]]
[two_simple(a, b) for a in [True, False] for b in [True, False]]
[three_simple(a, b, c) for a in [True, False] for b in [True, False] for c in [True, False]]
```

```hint
Move the outside `not` inside, one law at a time, and let two `not`s
cancel: `not (not b)` is `b`. For `three`, the `not` meets an `or` first,
then the `and` inside it.
```

```solution
def one(a, b):
    return not (a and not b)


def two(a, b):
    return not (not a and not b)


def three(a, b, c):
    return not (a or (b and not c))


def one_simple(a, b):
    """The same as one(a, b), with no not outside a bracket."""
    return (not a) or b


def two_simple(a, b):
    """The same as two(a, b), with no not at all."""
    return a or b


def three_simple(a, b, c):
    """The same as three(a, b, c), with no not outside a bracket."""
    return (not a) and ((not b) or c)
---
`one` becomes `(not a) or b`, since `not (not b)` is `b`. `two` becomes
`a or b`, because "not neither" is "at least one". `three` uses the laws
twice,
once for the `or` and once for the `and` inside it. The inputs are every
case, so if yours match the solution's there, they match everywhere.
```

### A condition from your world

<div class="dl-world" data-world="games-of-chance">

A card game lets you play a card unless it is neither a heart nor higher
than 10. The rule is written as `not (not heart and not high)`. Can you
write `can_play_simple` with no `not`, and check it on all 52 cards?

```python exec
id: logic-your-world--games-of-chance
def can_play(heart, high):
    return not (not heart and not high)


def can_play_simple(heart, high):
    """The same rule as can_play, with no not."""


deck = [(rank, suit) for suit in ["clubs", "diamonds", "hearts", "spades"] for rank in range(2, 15)]
print(all(can_play(s == "hearts", r > 10) == can_play_simple(s == "hearts", r > 10) for r, s in deck))
```

```inputs
[can_play_simple(heart, high) for heart in [True, False] for high in [True, False]]
```

```solution
def can_play(heart, high):
    return not (not heart and not high)


def can_play_simple(heart, high):
    """The same rule as can_play, with no not."""
    return heart or high


deck = [(rank, suit) for suit in ["clubs", "diamonds", "hearts", "spades"] for rank in range(2, 15)]
print(all(can_play(s == "hearts", r > 10) == can_play_simple(s == "hearts", r > 10) for r, s in deck))
---
It is `heart or high`, because "not neither" is "at least one". Ranks
run from 2 to 14 here, with 11 to 14 for jack, queen, king and ace, so
"higher than 10" is a picture card or an ace. The 52 cards are 52 cases,
but the four cases of the rule are the proof. The cards only show it on
a real deck.
```

</div>

<div class="dl-world" data-world="dinosaurs">

A museum puts a fossil on display unless it is incomplete or not yet
described in a paper. The rule is written as `not (not complete or not
described)`. Can you write `on_display_simple` with no `not`, and check
it on every case?

```python exec
id: logic-your-world--dinosaurs
def on_display(complete, described):
    return not (not complete or not described)


def on_display_simple(complete, described):
    """The same rule as on_display, with no not."""


cases = [(c, d) for c in [True, False] for d in [True, False]]
print(all(on_display(c, d) == on_display_simple(c, d) for c, d in cases))
```

```inputs
[on_display_simple(c, d) for c in [True, False] for d in [True, False]]
```

```solution
def on_display(complete, described):
    return not (not complete or not described)


def on_display_simple(complete, described):
    """The same rule as on_display, with no not."""
    return complete and described


cases = [(c, d) for c in [True, False] for d in [True, False]]
print(all(on_display(c, d) == on_display_simple(c, d) for c, d in cases))
---
`complete and described`. The `not` moves inside the bracket, turns the
`or` into an `and`, and meets the two `not`s already there, which cancel.
The written rule said "unless", and "unless" means "if not". Most
tangled conditions start as a sentence with "unless" in it.
```

</div>

<div class="dl-world" data-world="exoplanets">

An astronomer shortlists a planet for a closer look unless it is more
than 2 Earths across or 100 light-years or more away. The rule is
written as `not (not radius <= 2 or not distance < 100)`. Can you write
`shortlist_simple` with no `not`, and check that it picks the same
planets from the real file?

```python exec
id: logic-your-world--exoplanets
planets = await load_csv("exoplanets.csv")


def shortlist(radius, distance):
    return not (not radius <= 2 or not distance < 100)


def shortlist_simple(radius, distance):
    """The same rule as shortlist, with no not."""


pairs = list(zip(planets["radius_earths"], planets["distance_ly"]))
print(all(shortlist(r, d) == shortlist_simple(r, d) for r, d in pairs))
```

```inputs
sum(1 for r, d in pairs if shortlist_simple(r, d))
```

```solution
planets = await load_csv("exoplanets.csv")


def shortlist(radius, distance):
    return not (not radius <= 2 or not distance < 100)


def shortlist_simple(radius, distance):
    """The same rule as shortlist, with no not."""
    return radius <= 2 and distance < 100


pairs = list(zip(planets["radius_earths"], planets["distance_ly"]))
print(all(shortlist(r, d) == shortlist_simple(r, d) for r, d in pairs))
---
It is `radius <= 2 and distance < 100`, which shortlists 164 planets in
the copy saved on {{snapshot: exoplanets}}. The nearest of them is around
Proxima Centauri, 4.2 light-years away. A planet with no radius in the
file has `nan` there, and `<=` and `<` with `nan` are always `False`,
so neither version picks it. The two versions agree on 6,372 real
planets, but the four-row truth table is the proof.
```

</div>

## The same shapes, on sets

On [Venn diagrams](tutorial:venn-diagrams) the same two laws appeared on
sets, with union for `or`, intersection for `and`, and complement for
`not`. The complement of a set is everything in the *universal set*,
the set of everything we are talking about, that is not in it.

```python exec
id: the-same-shapes-on-sets-1
everyone = {1, 2, 3, 4, 5, 6, 7, 8}
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}


def complement(s):
    return everyone - s


print("not (A or B):        ", sorted(complement(a | b)))
print("(not A) and (not B): ", sorted(complement(a) & complement(b)))
print()
print("not (A and B):       ", sorted(complement(a & b)))
print("(not A) or (not B):  ", sorted(complement(a) | complement(b)))
```

A statement is true or false. An element is in a set or out of it. They
are the same kind of question, asked about different things, and so a law
proved in one place holds in the other. The Venn page showed it with a
picture. This page proved it by trying every row.

## Looking back

The game's rule, `not (first != second and first + second != 7)`, is
true on 12 of the 36 rolls. Can you say which 12, from the readable
version, without running anything?

A challenge: four cards lie on a table, showing `A`, `K`, `4` and `7`.
Each has a letter on one side and a number on the other. The rule says: "if a
card has a vowel on one side, it has an even number on the other." Which
cards must you turn over to check the rule? The most common choice is the A
and the 4. Can you write a program that tries every possible hidden side, to check?

```python challenge
cards_showing = ["A", "K", "4", "7"]


def breaks_rule(letter, number):
    """True if this card breaks: a vowel on one side, an odd number on the other."""
    return letter in "AEIOU" and number % 2 == 1


# For each card, try every hidden side it could have.
# A card needs turning over if some hidden side could break the rule.
```

The next page, [Counting carefully](tutorial:counting-carefully), counts
outcomes without listing them all. Probability starts there.

## Where to read more

Everything here is covered elsewhere too, often in a form that will suit you
better than this one.

Khan Academy. *Equivalent Compound Booleans.*
<https://www.khanacademy.org/computing/ap-computer-science-principles/programming-101/x2d2f703b37b450a3:logical-equivalence/a/equivalent-compound-booleans>.
De Morgan's laws from the programming side, with the same two rules this
page proves by looping over four rows.

Steve Mould (2013). *Can you solve this 4 card puzzle?*
<https://www.youtube.com/watch?v=Hpwd_ns2Wjs>. The puzzle in the
challenge above, and why an "if" does not mean what most people expect.
Three minutes. Try the challenge first.

CrashCourse (2017). *Boolean Logic & Logic Gates: Crash Course Computer
Science #3.* <https://www.youtube.com/watch?v=gI-qXk7XojA>. AND, OR, NOT
and XOR as switches inside a computer, each with its truth table. About
ten minutes.
