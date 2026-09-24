---
title: "Counting every outfit: lists of outcomes — Practice"
practice_for: counting-every-outfit
year: "2026-2027"
version: 2026.09.24.1
---

# Counting every outfit: lists of outcomes — Practice

Each answer is hidden until you open it. Where a problem asks you to
predict, the prediction is the exercise, so make one before you run
anything.

Your toolkit is loaded on this page, so `all_pairs`, `total` and
`product` are ready to use, and so is everything from earlier pages.

## Warm-up

Use this cell for any of the warm-up problems.

```python exec
id: counting-every-practice-scratch-1
print(all_pairs(["tea", "coffee"], ["small", "large"]))
```

**1. Predict.** What does the cell above print? Say how many pairs there
are, and which one comes first and which last, before you run it.

<details class="dl-answer"><summary>answer</summary>

```text
[('tea', 'small'), ('tea', 'large'), ('coffee', 'small'), ('coffee', 'large')]
```

Four pairs, $2 \times 2$. The first is `('tea', 'small')` and the last
is `('coffee', 'large')`. Every pair with `"tea"` comes first, because
the first list is the outer loop inside `all_pairs`.

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

**3. Predict.** A football club has 3 jerseys, 2 pairs of shorts and 4
pairs of socks. A kit is one of each. How many different kits are
there?

<details class="dl-answer"><summary>answer</summary>

By the counting principle, $3 \times 2 \times 4 = 24$ kits.

```python
print(product([3, 2, 4]))    # 24
```

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

**5. Make.** You are driving from Galway to Dublin through Athlone.
There are 3 roads you could take from Galway to Athlone, call them A, B
and C, and 2 from Athlone to Dublin, call them X and Y. List every
route with `all_pairs`, and count them.

<details class="dl-answer"><summary>answer</summary>

```python
to_athlone = ["A", "B", "C"]
to_dublin = ["X", "Y"]
routes = all_pairs(to_athlone, to_dublin)
print(routes)
print(len(routes))    # 6
```

Six routes: AX, AY, BX, BY, CX, CY. Every road to Athlone can be
followed by either road to Dublin, so $3 \times 2 = 6$.

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

**7. Fix.** This function is meant to list every pizza you can make from
one base and one topping. It gives only some of them. Find the one
mistake, and fix it.

```python exec
id: counting-every-practice-fix-pizza
def every_pizza(bases, toppings):
    """Every (base, topping) pair."""
    pizzas = []
    for base in bases:
        for topping in toppings:
            pizzas.append((base, topping))
        return pizzas

bases = ["thin", "deep"]
toppings = ["cheese", "mushroom", "pepperoni"]
print(len(every_pizza(bases, toppings)))    # should be 6
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Which pizzas does the function give back? Print the list, not only
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
base, the thin one, has met every topping, the function returns, and
the deep base is never used. It gives 3 pizzas, not 6.

`return` must sit outside both loops, level with `for base`:

```python
def every_pizza(bases, toppings):
    pizzas = []
    for base in bases:
        for topping in toppings:
            pizzas.append((base, topping))
    return pizzas

print(len(every_pizza(bases, toppings)))    # 6
```

</details>

**8. Fix.** A lunch deal is one sandwich and one drink. This code counts
the lunch deals, and gets the wrong answer. Fix it.

```python exec
id: counting-every-practice-fix-lunch
sandwiches = ["ham", "cheese", "egg", "falafel"]
drinks = ["water", "juice", "tea"]

meal_deals = len(sandwiches) + len(drinks)
print(meal_deals)    # should be 12
```

<details class="dl-answer"><summary>answer</summary>

A deal is a sandwich and a drink, one choice then another, so the counts
multiply:

```python
meal_deals = len(sandwiches) * len(drinks)
print(meal_deals)    # 12
```

`+` would be right for "a sandwich or a drink, not both": 7 choices.
And multiplies, or adds.

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

**10. Explain.** A restaurant has 8 starters and 12 main courses. Its
menu says "Choose a starter and a main: over 100 different dinners!" Is
that true? What could the restaurant add to make it true?

<details class="dl-answer"><summary>answer</summary>

It is not true. By the counting principle there are $8 \times 12 = 96$
dinners, which is fewer than 100.

Adding one starter gives $9 \times 12 = 108$. Adding one main gives
$8 \times 13 = 104$. Either would make the claim true. So would
counting "a main on its own" as a dinner too: that adds 12 more, for
108.

</details>

**11. Another way.** A friend says that two dice have 21 outcomes, not
36. In which space is your friend right?

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

Your friend is right when the two dice look the same and only the two
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
