---
title: "Collections without repeats: sets — Practice"
practice_for: collections-without-repeats
year: "2026-2027"
version: 2026.09.25.1
---

# Collections without repeats: sets — Practice

Each problem says what kind it is. **Predict** means guess first, then
run. **Make** means write something new. **Fix** means find why code
that looks fine does something else, and change it. **Explain** means
answer in words. **Another
way** means reach the same place by a second route. The answers are
folded away until you open them.

Your toolkit is loaded on this page: `frequency_table`, `all_pairs`,
`combinations`, `simulate`, `count_if` and the rest from earlier pages.
A set prints its elements in an order of its own, so the answers print
`sorted(...)` wherever the order matters to a reader.

## Warm-up

Use this cell for any of the warm-up problems.

```python exec
id: collections-practice-warm-up
print(len(set("banana")))
```

**1. Predict.** `set("banana")` makes a set from the letters of a word.
What will `len(set("banana"))` print? Guess, then run the cell.

<details class="dl-answer"><summary>answer</summary>

It prints `3`. The word has six letters, but only three different ones:
b, a and n. `set` reads a string letter by letter, the way a
`for` loop does, and keeps each letter once.

</details>

**2. Make.** A game uses two small pictures. Each list below is the
colour of every pixel in one picture, as a hex code from
[Everything is ones and zeros](tutorial:everything-is-ones-and-zeros).
How many different colours do the two pictures use between them? That
number is the size of the *palette*, the set of colours the game must
keep. Find it with sets.

```python exec
id: collections-practice-paints
first_picture = ["FF8800", "008080", "FFFFFF", "008080", "DC143C"]
second_picture = ["FFFFFF", "000000", "FF8800", "FFD700"]
```

<details class="dl-answer"><summary>answer</summary>

```python
palette = set(first_picture) | set(second_picture)
print(len(palette))
print(sorted(palette))
```

They use six colours. The union holds orange, `FF8800`, and white, `FFFFFF`,
once each, although both pictures use them, and teal, `008080`, once,
although the first picture has it twice. Real image formats such as GIF
keep a palette like this, with each colour once, and store each pixel as
a position in it.

</details>

**3. Predict.** What will each line print? Say all three before you run
them.

```python exec
id: collections-practice-three
print(sorted({1, 2, 3} & {2, 3, 4}))
print(sorted({1, 2, 3} | {2, 3, 4}))
print(sorted({1, 2, 3} - {2, 3, 4}))
```

<details class="dl-answer"><summary>answer</summary>

It prints `[2, 3]`, then `[1, 2, 3, 4]`, then `[1]`. The intersection keeps what
is in both, the union keeps what is in either, and the difference keeps
what is in the first set and not in the second.

</details>

**4. Explain.** A friend runs `print({"pear", "apple", "fig"})` and
sees the fruit in a different order from the one they typed. They run
it again, and the order changes again. Is something broken? How would
you print the fruit in alphabetical order?

<details class="dl-answer"><summary>answer</summary>

Nothing is broken. A set makes no promise about order. It only records
which values are in it. Python keeps the elements in an order of its
own, which can differ from run to run for words.
`sorted({"pear", "apple", "fig"})` gives a list in alphabetical order,
`['apple', 'fig', 'pear']`, every time.

</details>

## Core

**5. Make.** A recipe for pesto has these ingredients. A café must warn
customers about any of the allergens in the second set. Which allergens
are in the pesto? And is it free of every allergen, True or False?

```python exec
id: collections-practice-pesto
pesto = {"basil", "pine nuts", "parmesan", "garlic", "olive oil", "salt"}
allergens = {"milk", "egg", "peanuts", "tree nuts", "pine nuts", "gluten",
             "parmesan", "fish", "soya", "sesame"}
```

<details class="dl-answer"><summary>answer</summary>

```python
warnings = pesto & allergens
print(sorted(warnings))
print(warnings == set())
```

This prints `['parmesan', 'pine nuts']`, then `False`. The pesto is not
free of allergens. The intersection is what the recipe and the list
share. An empty intersection would mean nothing to warn about. (Real
allergen rules count parmesan as milk. A real café would list what is
inside each ingredient, too.)

</details>

**6. Fix.** Two bus stops are served by these routes. Schlomo, who is
learning Python too, wants the routes that stop at both, so that he
could wait at either one. In English, "in both" is "A *and* B", so he
writes `and`. The cell prints four routes, and some of them do not stop
at the first stop. Run it, then find the line that does not do what
Schlomo meant.

```python exec
id: collections-practice-fix-buses
stop_a = {"4", "7", "46A", "145"}
stop_b = {"7", "39A", "145", "155"}

both_stops = stop_a and stop_b
print(sorted(both_stops))
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. What does the cell print? Compare it with `stop_b`.
2. On [True, false and every case](tutorial:true-false-and-every-case),
   what kind of values did `and` work on?
3. Which sign means "in both" for two sets?

**Think about:** why the word "and" and the sign `&` can mean different
things in Python, when in English they are the same word.

</details>

<details class="dl-answer"><summary>answer</summary>

Schlomo's reasoning matches the maths word. The
intersection is "A and B". But in Python, `and` is the word for True
and False. Given two sets, it does not make an intersection. It returns the second set whenever the first one is
not empty, so the cell printed all of `stop_b`. The sign for "in both"
is `&`:

```python
both_stops = stop_a & stop_b
print(sorted(both_stops))
```

Now it prints `['145', '7']`. (The order is alphabetical for text, so
"145" comes before "7", as "1" comes before "7".)

</details>

**7. Predict.** A five-a-side team played two matches. Before you run
the cell, say how many players are in each of the three answers.

```python exec
id: collections-practice-matches
first_match = {"Aoife", "Bríd", "Ciara", "Dara", "Eimear"}
second_match = {"Aoife", "Ciara", "Fiona", "Gráinne", "Eimear"}

print(sorted(first_match - second_match))
print(sorted(second_match - first_match))
print(len(first_match | second_match))
```

<details class="dl-answer"><summary>answer</summary>

The answers are two, two and seven. Bríd and Dara played only the first match. Fiona
and Gráinne played only the second. Seven different players took part
in all: the five from the first match, and the two new ones.

</details>

**8. Make.** Leinster has twelve counties. Make a set of the counties you
have visited, or make up a list, and print the Leinster counties you
have not visited yet. What is the universal set here?

```python exec
id: collections-practice-leinster
leinster = {"Carlow", "Dublin", "Kildare", "Kilkenny", "Laois", "Longford",
            "Louth", "Meath", "Offaly", "Westmeath", "Wexford", "Wicklow"}
visited = {"Dublin", "Wicklow", "Kildare", "Galway", "Kerry"}
```

<details class="dl-answer"><summary>answer</summary>

```python
not_yet = leinster - visited
print(len(not_yet))
print(sorted(not_yet))
```

With the counties above, it prints `9`, then the nine counties from
Carlow to Wexford that are not Dublin, Kildare or Wicklow. The
universal set is `leinster`. The complement is taken inside it, so
Galway and Kerry, which are not in Leinster, play no part. With all 32
counties of Ireland as the universal set, the answer would be different,
though `visited` is the same.

</details>

**9. Another way.** Two laptops have these programs installed. The
programs on only one of them are the symmetric difference, `^`. Find
the same set two more ways, with `|`, `&` and `-`, and check that all
three agree.

```python exec
id: collections-practice-games
maeve_laptop = {"Firefox", "Python", "VLC", "GIMP", "Zoom"}
tomas_laptop = {"GIMP", "Blender", "Python", "Audacity"}

print(sorted(maeve_laptop ^ tomas_laptop))
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The symmetric difference is everything in either set, except what is
   in both.
2. It is also what only Maeve's laptop has, together with what only
   Tomás's has.
3. Write each route as one line, and compare them with `==`.

**Think about:** which of the three routes you would rather read out
loud to someone, and why.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
route_one = maeve_laptop ^ tomas_laptop
route_two = (maeve_laptop | tomas_laptop) - (maeve_laptop & tomas_laptop)
route_three = (maeve_laptop - tomas_laptop) | (tomas_laptop - maeve_laptop)
print(route_one == route_two == route_three)
```

It prints `True`. All three give the same five programs: Audacity,
Blender, Firefox, VLC and Zoom. In symbols,
$A \triangle B = (A \cup B) \setminus (A \cap B) = (A \setminus B) \cup (B \setminus A)$.

</details>

**10. Explain.** Is the set of whole numbers from 1 to one billion
finite or infinite? Could Python hold it as a set? What could you use
instead, if all you want to know is whether a number is in it?

<details class="dl-answer"><summary>answer</summary>

It is finite. It has exactly 1,000,000,000 elements, which is a large
number, but a number. Python could try to make it, with
`set(range(1, 1_000_000_001))`, but a set of a billion numbers needs
tens of gigabytes of memory, more than most computers have. So in this
space, a finite set can still be too big to list.

A rule does the job, as for $\mathbb{N}$ on the tutorial page. A test
such as `1 <= number <= 1_000_000_000 and number == int(number)` answers
"is it in?" at once, without making the set.

</details>

<aside class="dl-note" id="collections-practice-note-cantor">

**Bigger infinities.** Some infinite sets can still be put in a list,
one after another. The whole numbers can: 1, 2, 3, and so on. In 1874,
Georg Cantor proved that the real numbers cannot. Whatever list you
make, some real number is missing from it. So one infinite set can be
bigger than another.

</aside>

**11. Fix.** Schlomi, who is learning Python too, wants the different
words in a line of a song. Maths writes a set with curly brackets, so
she starts an empty set with `{}`. The cell stops with an error. Run
it, read the last line of the error, then find the line that does not
do what Schlomi meant.

```python exec
id: collections-practice-fix-words
line = "row row row your boat gently down the stream"

different_words = {}
for word in line.split():
    different_words.add(word)
print(len(different_words))
```

<details class="dl-answer"><summary>answer</summary>

The last line of the error is
`AttributeError: 'dict' object has no attribute 'add'`. Schlomi's
brackets are the ones maths uses, but in Python `{}` is an empty
dictionary, not an empty set. A dictionary has no `.add`. Start with `set()`:

```python
different_words = set()
for word in line.split():
    different_words.add(word)
print(len(different_words))
```

It prints `7`. The line has nine words, and "row" is three of them.
`line.split()` cuts the line into a list of words at each space.

</details>

**12. Make.** A Python program needs three *packages*, collections of
extra code other people wrote: `numpy`, `pandas` and `matplotlib`.
Write a function `can_run(needed, installed)` that gives True when
everything needed is installed on a computer. Then print what is
missing from the second computer.

```python exec
id: collections-practice-gym
needed = {"numpy", "pandas", "matplotlib"}
first_computer = {"numpy", "matplotlib", "requests", "pandas", "flask"}
second_computer = {"numpy", "requests", "flask"}
```

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Yours may be different and work too.

```python
def can_run(needed, installed):
    """True when every package in needed is also in installed."""
    return needed <= installed

print(can_run(needed, first_computer))
print(can_run(needed, second_computer))
print(sorted(needed - second_computer))
```

It prints `True`, `False`, then `['matplotlib', 'pandas']`. The program can run
when `needed` is a subset of what is installed. The difference says
what to install. Tools like `pip`, which installs Python packages, ask
this question every time.

</details>

## Stretch

**13. Make.** Turn the colours cell from the tutorial into a function,
`power_set(values)`, that returns a list of every subset of `values`.
Then test its promise, $|\mathcal{P}(A)| = 2^n$, for sets of 0 to 6
elements with `assert`.

```python exec
id: collections-practice-power
def power_set(values):
    """Return a list of every subset of values, each subset a set.

    The list includes the empty set and a set of all the values.
    """
    ...
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Inside the function, the colours loop works with `lights` renamed to
   `values`, and `colours` renamed to `subsets`.
2. Return `subsets` after the loop.
3. For the tests, loop over `n` in `range(7)`, and make a set of `n`
   elements with `set(range(n))`.

**Think about:** what `power_set([])` should give. How many subsets
does the empty set have?

</details>

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Yours may be different and work too.

```python
def power_set(values):
    """Return a list of every subset of values, each subset a set.

    The list includes the empty set and a set of all the values.
    """
    subsets = [set()]
    for value in values:
        with_value = []
        for subset in subsets:
            with_value.append(subset | {value})
        subsets = subsets + with_value
    return subsets

for n in range(7):
    assert len(power_set(set(range(n)))) == 2 ** n, n
print(power_set([]))
```

It prints `[set()]`. An `assert` prints nothing when its condition is
True. The empty set has one subset:
itself. That matches $2^0 = 1$, and it is why the loop starts from
`[set()]`, not from an empty list.

</details>

**14. Another way.** The tutorial counted 8 colours from 3 lights by
listing every subset. Count them another way, with `combinations` from
[Orders and choices](tutorial:orders-and-choices): the colours with 0
lights on, with 1, with 2 and with 3. Does it agree for 10 lights too?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The colours with exactly $k$ lights on, from $n$, are $C(n, k)$.
2. Add them up for every $k$ from 0 to $n$: `total` can help.
3. Compare with `2 ** n`.

**Think about:** why every colour is counted exactly once this way.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
for n in [3, 10]:
    counts = []
    for k in range(n + 1):
        counts.append(combinations(n, k))
    print(n, counts, total(counts), 2 ** n)
```

For 3 lights the counts are 1, 3, 3 and 1, which make 8: black; red,
green and blue; yellow, magenta and cyan; white. For 10 they make
1,024, which is $2^{10}$. Every subset has some number of elements,
from 0 to $n$, so it is counted in exactly one of the groups. In
symbols, $\sum_{k=0}^{n} C(n, k) = 2^n$.

</details>

**15. Make.** On
[Chances that combine](tutorial:chances-that-combine#the-birthday-problem),
two people in a class of 23 share a birthday about half the time. A set
gives a short way to check a class for a shared birthday. If the set of
birthdays is smaller than the class, two of them were the same. Write a
trial with that idea, and use `simulate` to check the tutorial's answer.

```python exec
id: collections-practice-birthdays
import random
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Make a list of 23 birthdays, each `random.randint(1, 365)`.
2. `set(birthdays)` keeps each day once.
3. Return True when `len(set(birthdays))` is less than 23.

**Think about:** what the difference `23 - len(set(birthdays))` tells
you.

</details>

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Yours may be different and work too.

```python
def shared_birthday():
    """Make a class of 23 random birthdays. True when two or more share a day."""
    birthdays = []
    for person in range(23):
        birthdays.append(random.randint(1, 365))
    return len(set(birthdays)) < 23

print(simulate(shared_birthday, 10000))
```

It prints something near 0.507, such as 0.5094, close to the exact
answer of about 0.507. The set checks in one step. Each
repeated birthday makes the set one element smaller than the list.

</details>

**16. Explain.** The tutorial said that a SQL `JOIN` is like an
intersection. In what way is it like one? In what way is it not?

<details class="dl-answer"><summary>answer</summary>

It is like an intersection because it keeps only what two tables have
in common. A row of one table is matched only with rows of the other
that share the same value in a column, such as a customer id. A
customer with no orders is left out, as a song on only one playlist is
left out of $A \cap B$.

It is not quite an intersection because the two tables' rows are
different kinds of thing, a customer and an order, so no row is "in
both". A JOIN compares one column, and then makes a new, wider row from
each matching pair. So it is closer to two steps. First make every pair,
as a `CROSS JOIN` or `all_pairs` does, then keep only the pairs whose ids
agree.

</details>
