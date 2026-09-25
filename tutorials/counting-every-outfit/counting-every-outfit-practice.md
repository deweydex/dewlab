---
title: "Counting every outfit: lists of outcomes — Practice"
practice_for: counting-every-outfit
year: "2026-2027"
version: 2026.09.25.1
---

# Counting every outfit: lists of outcomes — Practice

Each answer is hidden until you open it. Where a problem asks you to
predict, the prediction is the exercise, so make one before you run
anything. An answer shows one good way. Yours may be different, and as
good.

Your toolkit is loaded on this page, so `all_pairs`, `total` and
`product` are ready to use, and so is everything from earlier pages.

## Warm-up

Use this cell for any of the warm-up problems.

```python exec
id: counting-every-practice-scratch-1
print(all_pairs(["light", "dark"], ["small", "large"]))
```

**1. Predict.** An app lets you choose a light or dark screen, and small
or large text. What does the cell above print? Say how many pairs there
are, and which one comes first and which last, before you run it.

<details class="dl-answer"><summary>answer</summary>

```text
[('light', 'small'), ('light', 'large'), ('dark', 'small'), ('dark', 'large')]
```

Four pairs, $2 \times 2$. The first is `('light', 'small')` and the
last is `('dark', 'large')`. Every pair with `"light"` comes first,
because the first list is the outer loop inside `all_pairs`.

</details>

**2. Make.** A board game has a spinner with three colours, red, green
and blue, and you also toss a coin. Write the sample space by hand,
then check it with `all_pairs`.

<details class="dl-answer"><summary>answer</summary>

By hand: red and H, red and T, green and H, green and T, blue and H,
blue and T. That is six outcomes.

```python
spinner = ["red", "green", "blue"]
coin = ["H", "T"]
outcomes = all_pairs(spinner, coin)
print(outcomes)
print(len(outcomes))    # 6
```

</details>

**3. Predict.** DNA, the code inside every living cell, is written with
four letters: A, C, G and T. A cell reads it three letters at a time,
and each group of three is called a codon. How many different codons
can there be?

<details class="dl-answer"><summary>answer</summary>

Each of the three places is a choice of 4 letters, so by the counting
principle there are $4 \times 4 \times 4 = 64$ codons.

```python
print(product([4, 4, 4]))    # 64
```

Living things use those 64 codons to stand for only 20 building blocks,
plus a few "stop" signals, so most building blocks have more than one
codon. Two letters would not have been enough: $4 \times 4 = 16$ is
fewer than 20.

</details>

**4. Explain.** You toss a 10c coin and a 20c coin. Why are
`("H", "T")` and `("T", "H")` two different outcomes?

<details class="dl-answer"><summary>answer</summary>

The first value in each pair is the 10c coin, and the second is the
20c coin. `("H", "T")` means the 10c shows heads and the 20c shows
tails. `("T", "H")` means the other way round. You could see the
difference on the table. A pair has a fixed order, so these are two
outcomes, and the sample space has four: HH, HT, TH, TT.

</details>

## Core

Use this cell for the core problems.

```python exec
id: counting-every-practice-scratch-2
die = [1, 2, 3, 4, 5, 6]
print(len(all_pairs(die, die)))
```

**5. Make.** A message goes from your laptop to a website in two hops.
First it passes through one of 3 routers, boxes that pass messages on,
called A, B and C. Then it passes through one of 2 more, X and Y. List
every route with `all_pairs`, and count them.

<details class="dl-answer"><summary>answer</summary>

```python
first_hop = ["A", "B", "C"]
second_hop = ["X", "Y"]
routes = all_pairs(first_hop, second_hop)
print(routes)
print(len(routes))    # 6
```

Six routes: AX, AY, BX, BY, CX, CY. Every first router can be followed
by either second one, so $3 \times 2 = 6$. The internet has many more
routers than this, and many more routes, which is one reason a message
still gets through when one router fails.

</details>

**6. Make.** Roll two dice. How many of the 36 outcomes have a total of
7? List them with a loop over `all_pairs(die, die)`. A `for` line can
take two names, as in `for first, second in all_pairs(die, die):`, one
for each value of the pair.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. `all_pairs(die, die)` gives all 36 pairs, like `(3, 4)`.
2. Loop over them with `for first, second in ...:`. Two names on the
   `for` line take the two values of each pair.
3. Keep a count that goes up by 1 when `first + second == 7`.

**Think about:** is `(3, 4)` the same outcome as `(4, 3)`?

**Try this next:** which total has the most outcomes?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
sevens = 0
for first, second in all_pairs(die, die):
    if first + second == 7:
        print(first, second)
        sevens = sevens + 1
print(sevens)    # 6
```

Six outcomes: (1, 6), (2, 5), (3, 4), (4, 3), (5, 2) and (6, 1). No
other total has as many, which is why 7 matters so much in dice games.
Listing the outcomes and then counting the ones we want is the start of
probability, on
[How likely is it?](tutorial:how-likely-is-it).

</details>

**7. Fix.** Schlomo, who is learning Python too, writes a function to
list every text style a small editor offers: one font and one size. It
gives only some of them. Find the one mistake, and fix it.

```python exec
id: counting-every-practice-fix-styles
def every_style(fonts, sizes):
    """Every (font, size) pair."""
    styles = []
    for font in fonts:
        for size in sizes:
            styles.append((font, size))
        return styles

fonts = ["serif", "sans"]
sizes = [10, 12, 14]
print(len(every_style(fonts, sizes)))    # should be 6
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Which styles does the function give back? Print the list, not only
   its length.
2. Which loop is the `return` line inside?
3. What happens to a function when it reaches `return`?

**Think about:** how far along the `return` line must be, to run only
once both loops have finished?

**Try this next:** what would happen if `return` were pushed in one
level further, inside the inner loop?

</details>

<details class="dl-answer"><summary>answer</summary>

The `return` line is pushed in under the outer loop. So after the first
font, serif, has met every size, the function returns, and sans is never
used. It gives 3 styles, not 6. Schlomo's loops were right; one line was
four spaces too far in.

`return` must sit outside both loops, level with `for font`:

```python
def every_style(fonts, sizes):
    styles = []
    for font in fonts:
        for size in sizes:
            styles.append((font, size))
    return styles

print(len(every_style(fonts, sizes)))    # 6
```

</details>

**8. Fix.** A laptop comes with one of 4 screens and one of 3 amounts of
memory. This code counts the different laptops, and gets the wrong
answer. Fix it.

```python exec
id: counting-every-practice-fix-laptops
screens = ["13 inch", "14 inch", "15 inch", "16 inch"]
memory = ["8 GB", "16 GB", "32 GB"]

laptops = len(screens) + len(memory)
print(laptops)    # should be 12
```

<details class="dl-answer"><summary>answer</summary>

A laptop has a screen and an amount of memory, one choice then another,
so the counts multiply:

```python
laptops = len(screens) * len(memory)
print(laptops)    # 12
```

`+` would be right for "a new screen or more memory, not both": 7
choices. And multiplies, or adds.

</details>

**9. Predict.** You toss three coins, a 10c, a 20c and a 50c. How many
outcomes are there? Then run this to list them. What does the first
outcome look like?

```python
coin = ["H", "T"]
three = all_pairs(all_pairs(coin, coin), coin)
print(len(three))
print(three[0])
```

<details class="dl-answer"><summary>answer</summary>

$2 \times 2 \times 2 = 8$ outcomes. The first is `(('H', 'H'), 'H')`:
the pair for the first two coins, then the third coin.

This is the same count as a truth table with three inputs, $2^3 = 8$
rows. Heads and tails, like True and False, are a choice of two.

</details>

**10. Explain.** A game has 8 heads and 12 bodies for your robot. Its
advert says "Choose a head and a body: over 100 different robots!" Is
that true? What could the game add to make it true?

<details class="dl-answer"><summary>answer</summary>

It is not true. By the counting principle there are $8 \times 12 = 96$
robots, which is fewer than 100.

Adding one head gives $9 \times 12 = 108$. Adding one body gives
$8 \times 13 = 104$. Either would make the claim true. So would
allowing "a body with no head": that adds 12 more, for 108. That is one
good answer, and you may have found others.

</details>

**11. Another way.** Schlomi, who is learning Python too, says that two
dice have 21 outcomes, not 36. In which space is she right?

```python exec
id: counting-every-practice-another-dice
count = 0
for first, second in all_pairs(die, die):
    if first <= second:
        count = count + 1
print(count)
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Run the cell. Which pairs does `first <= second` keep?
2. Which pair does it keep out of `(3, 4)` and `(4, 3)`?
3. When would you not be able to tell `(3, 4)` from `(4, 3)`?

**Think about:** two dice of the same colour, rolled into a cup. What
can you see?

**Try this next:** how many of the 21 have both dice the same?

</details>

<details class="dl-answer"><summary>answer</summary>

The cell prints 21. It keeps one pair out of each two that are the same
numbers in a different order, such as `(3, 4)` and `(4, 3)`, and it
keeps all six doubles.

Schlomi is right when the two dice look the same and only the two
numbers matter, not which die showed which. Then "a 3 and a 4" is one
outcome. The count of 36 is right when the dice can be told apart, such
as a red die and a blue one.

Both are real sample spaces. But the 21 are not equally likely: a 3 and
a 4 can happen two ways, and a double 3 only one. That matters on
[How likely is it?](tutorial:how-likely-is-it). Counting where order
does not matter is what
[Orders and choices](tutorial:orders-and-choices) is about.

</details>

**12. Make.** A music app plays either one of 5 rock songs or one of 4
jazz songs to wake you up. How many choices of alarm are there? And how
many if it plays one rock song and then one jazz song? Check the second
with `all_pairs`.

<details class="dl-answer"><summary>answer</summary>

One song, from rock or jazz: $5 + 4 = 9$ choices.

A rock song and then a jazz song: $5 \times 4 = 20$ choices.

```python
rock = ["R1", "R2", "R3", "R4", "R5"]
jazz = ["J1", "J2", "J3", "J4"]
print(len(rock) + len(jazz))              # 9
print(len(all_pairs(rock, jazz)))         # 20
```

</details>

## Stretch

Use this cell for the stretch problems.

```python exec
id: counting-every-practice-scratch-3
# Use this cell for the stretch problems
```

**13. Make.** A website lets you make a password of 1, 2, 3 or 4 small
letters. How many passwords is that in all? Write it in sigma notation,
then work it out with a loop and `total`.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. With 1 letter there are $26$ passwords. With 2 there are $26^2$.
2. So the whole count is $\sum_{n=1}^{4} 26^n$.
3. Build a list of the four counts with a loop and `append`, then use
   `total`.

**Think about:** which length gives most of the passwords?

**Try this next:** how many passwords of 1 to 8 letters are there?

</details>

<details class="dl-answer"><summary>answer</summary>

$$\sum_{n=1}^{4} 26^n = 26 + 676 + 17576 + 456976 = 475254$$

```python
counts = []
for length in range(1, 5):
    counts.append(26 ** length)
print(counts)           # [26, 676, 17576, 456976]
print(total(counts))    # 475254
```

The passwords of 4 letters are about 96% of the whole count. The
longest length always gives most of the passwords, because each extra
letter multiplies the count by 26. Allowing short passwords adds very
little.

</details>

**14. Make.** Here is a start on the unit's password checker. Write
`password_strength(choices, length)`. It works out how many passwords
there are with `choices` characters for each of `length` places. Then
it gives back `"weak"` for fewer than a million, `"fair"` for fewer than
a million million ($10^{12}$), and `"strong"` otherwise. Test it on a
four-digit PIN, 8 small letters, and 12 small letters.

<details class="dl-answer"><summary>answer</summary>

```python
def password_strength(choices, length):
    """Say how hard it is to try every password of this kind."""
    count = choices ** length
    if count < 10 ** 6:
        return "weak"
    elif count < 10 ** 12:
        return "fair"
    else:
        return "strong"

assert password_strength(10, 4) == "weak"      # 10,000 PINs
assert password_strength(26, 8) == "fair"      # about 209 thousand million
assert password_strength(26, 12) == "strong"
print("password_strength keeps its promise.")
```

The counting principle gives the count, and `if` and `elif` from
[Choosing a path](tutorial:choosing-a-path) turn it into a word. The
order of the checks matters: the smallest limit is checked first.

</details>

**15. Predict.** What does this print? Think about what each part
counts, from the inside out.

```python
switches = [False, True]
print(len(all_pairs(switches, all_pairs(switches, switches))))
```

<details class="dl-answer"><summary>answer</summary>

It prints 8.

The inside, `all_pairs(switches, switches)`, has $2 \times 2 = 4$
pairs. Pairing each of the 2 values with each of those 4 gives
$2 \times 4 = 8$. These are the 8 rows of a truth table with three
inputs. A truth table is the sample space of its inputs.

</details>

**16. Explain.** On the tutorial page, the loop came first and
the formula $m \times n$ came second. Schlomo says: "Listing all the
outfits was a waste of time. Tell me to multiply, and I'll multiply." What
would you say to him? Is there a kind of problem where he is right?

<details class="dl-answer"><summary>answer</summary>

There is no single right answer. A good answer agrees with Schlomo
where he is right, and also says what the list is for.

- **Where Schlomo is right.** When the choices do not change each
  other, and there are too many to list, the formula is the only way. No
  loop will list $26^{12}$ passwords. In an exam, multiplying is faster
  too.
- **What the list gives.** The list is how we know the formula can be
  trusted. It also catches a problem the formula cannot see. If the
  choices do change each other, $m \times n$ gives the wrong count, and
  only a list, or careful thought, will show it. Three songs in a
  playlist are an example: $3 \times 3 \times 3$ is 27, but only 6
  orders play each song once, as the next page,
  [Orders and choices](tutorial:orders-and-choices), shows.

A strong answer might say: multiply when you are sure the choices do not
change each other, and list a small case when you are not sure.

</details>
