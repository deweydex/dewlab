---
title: "Circles that overlap: Venn diagrams — Practice"
practice_for: circles-that-overlap
year: "2026-2027"
version: 2026.09.25.1
---

# Circles that overlap: Venn diagrams — Practice

Each problem says what kind it is. **Predict** means guess first, then
run. **Make** means write something new. **Fix** means find why code
that looks fine does something else, and change it. **Explain** means
answer in words. **Another
way** means reach the same place by a second route. The answers are
folded away until you open them.

Your toolkit is loaded on this page, from every earlier page of the
course. Every survey and check here is made up, so that the numbers stay small
enough to check by eye. A pencil and a quick sketch of the circles help
with almost every problem.

## Warm-up

Use this cell for any of the warm-up problems.

```python exec
id: circles-practice-warm-up
# Try things here
```

**1. Predict.** A website runs on two servers. These users reached the
first server this morning, and these reached the second. What will the
cell print? Draw the two circles first.

```python
server_one = {"Mia", "Tom", "Ada", "Sean"}
server_two = {"Tom", "Sean", "Nora"}
print(len(server_one | server_two), len(server_one & server_two), len(server_one ^ server_two))
```

<details class="dl-answer"><summary>answer</summary>

It prints `5 2 3`.

Tom and Sean are in the overlap, so `server_one & server_two` has 2
names. The union
has everyone once: Mia, Tom, Ada, Sean and Nora, which makes 5. The
symmetric difference, `^`, is the two outer parts without the overlap:
Mia, Ada and Nora, which makes 3. Inclusion–exclusion agrees:
$4 + 3 - 2 = 5$.

</details>

**2. Make.** A café keeps its menu, and which dishes contain gluten and
which contain dairy, as sets. A customer can eat neither. Write one line
that gives the dishes they can have.

```python
menu = {"soup", "sandwich", "salad", "curry", "cake", "porridge", "fruit bowl"}
has_gluten = {"soup", "sandwich", "cake", "porridge"}
has_dairy = {"soup", "cake", "curry", "porridge"}
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Draw two circles, gluten and dairy, inside a box for the menu.
2. Which region holds the dishes with neither?
3. That region is the box, with both circles taken away.

**Think about:** what is the box here, and why does the answer need it?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
print(menu - (has_gluten | has_dairy))
```

This prints `{'salad', 'fruit bowl'}`, in some order. The dishes the
customer can eat are the complement of the union: everything on the
menu that is in neither circle. `(menu - has_gluten) & (menu - has_dairy)`
gives the same two dishes, by De Morgan's laws from
[Untangling a condition](tutorial:untangling-a-condition).

</details>

**3. Explain.** A tutor says, "Twelve people do not speak Polish." Why
does that sentence need a box to mean anything? What would the number be
if the box were the whole of Ireland?

<details class="dl-answer"><summary>answer</summary>

"Do not speak Polish" is a complement, and a complement is everything
*in the box* that is not in the circle. Without a box, there is no
"everything" to take the circle away from. The tutor means the box is
the class, and 12 people in the class do not speak Polish. If the box
were Ireland, the number would be millions.

</details>

**4. Predict.** An office has 30 computers. 18 are on the Wi-Fi, 15 are
plugged in with an Ethernet cable, and 7 use both. How many are on the
network at least one way? How many are on neither? Find it on
paper, then check it in the warm-up cell.

<details class="dl-answer"><summary>answer</summary>

The number on at least one is $18 + 15 - 7 = 26$. The 7 that use both were counted once
with the Wi-Fi and once with the cable, so they are taken away once.
The number on neither is $30 - 26 = 4$, perhaps switched off.

```python
print(18 + 15 - 7, 30 - (18 + 15 - 7))
```

</details>

## Core

Run this cell first. It gives the core and stretch problems the 20
laptops from the tutorial.

```python exec
id: circles-practice-laptops
updated = {"Aoife", "Hassan", "Ben", "Isla", "Rory", "Priya", "Wei",
           "Ciara", "Eoin", "Maeve"}
antivirus = {"Aoife", "Hassan", "Ben", "Isla", "Rory", "Priya", "Wei",
             "Dmitri", "Kate", "Fatima", "Liam"}
backed_up = {"Aoife", "Hassan", "Ciara", "Dmitri", "Kate", "Grainne",
             "Sadhbh", "Tomas"}
laptops = updated | antivirus | backed_up | {"Jakub", "Niamh", "Oisin"}
print(len(laptops), "laptops")
```

**5. Make.** An evening class has 12 adults. Here is who speaks Irish,
Polish and French.

```python
learners = {"Ana", "Bogdan", "Chloe", "Dara", "Emil", "Fiona", "Gosia",
            "Hugo", "Iris", "Jan", "Kasia", "Luke"}
irish = {"Chloe", "Dara", "Fiona", "Iris", "Luke"}
polish = {"Bogdan", "Emil", "Gosia", "Jan", "Kasia", "Luke"}
french = {"Ana", "Chloe", "Hugo", "Iris", "Kasia", "Luke"}
```

Find the size of all eight regions of the three-circle diagram, with
one set operation for each. Which regions are empty? How many learners
speak exactly two of the three languages?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Start with the middle: `irish & polish & french`.
2. A two-circle region is a pair's overlap, minus the third set:
   `(irish & polish) - french`.
3. A one-circle region is one set minus both of the others.
4. The outside is `learners` minus the union of all three.

**Think about:** do your eight numbers add to 12? If not, which region
has someone counted twice?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
print("all three:", len(irish & polish & french))
print("Irish and Polish only:", len((irish & polish) - french))
print("Irish and French only:", len((irish & french) - polish))
print("Polish and French only:", len((polish & french) - irish))
print("Irish only:", len(irish - polish - french))
print("Polish only:", len(polish - irish - french))
print("French only:", len(french - irish - polish))
print("none:", len(learners - (irish | polish | french)))
```

The counts are 1, 0, 2, 1, 2, 4, 2 and 0, which add to 12. Luke speaks
all three. Two regions are empty: nobody speaks Irish and Polish without
French, and everybody speaks at least one. An empty region is still a
region. The diagram draws it, and writes 0 in it. Three people,
$0 + 2 + 1$, speak exactly two: Chloe, Iris and Kasia.

</details>

**6. Fix.** Schlomi, who is learning Python too, wants a function that
finds "exactly two" from a report's totals. Her idea is to add the
three pairs, then take away the middle, because the middle is not "exactly
two". She tests it on the tutorial's laptops: their pairs are 7, 3 and
4, their middle is 2, and the tutorial found 8. The cell is meant to
stop with an `AssertionError` until you fix the function.

```python exec
id: circles-practice-fix-two
def exactly_two_from_totals(pair_1, pair_2, pair_3, all_three):
    """Return how many are in exactly two of three sets.

    pair_1, pair_2 and pair_3 are the sizes of the three overlaps of two
    sets. all_three is the size of the overlap of all three.
    """
    return pair_1 + pair_2 + pair_3 - all_three


assert exactly_two_from_totals(7, 3, 4, 2) == 8, "the laptops have 8"
print(exactly_two_from_totals(9, 2, 1, 1), "days in Galway")
```

Once it passes, the last line uses it on a made-up month of weather in
Galway: 9 days had rain and wind, 2 had rain and frost, 1 had wind and
frost, and 1 day had all three.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Draw three circles. Which regions does the pair "updates and
   antivirus", 7 laptops, include?
2. The middle is inside every pair. How many of the three pairs is it
   inside?
3. So how many times does the middle need to be taken away?

**Think about:** the table in the tutorial's section on inclusion–exclusion
for three sets. What does it say about a laptop in all three circles?

</details>

<details class="dl-answer"><summary>answer</summary>

Schlomi saw that the middle must go. But each pair's total
includes the middle. There are three pairs, so the middle is counted
three times, and it must be taken away three times:

```python
    return pair_1 + pair_2 + pair_3 - 3 * all_three
```

Now the laptops give $14 - 6 = 8$, and the test passes. Galway had
$12 - 3 = 9$ days with exactly two of rain, wind and frost.

</details>

**7. Another way.** The tutorial found that 14 laptops are updated or
have antivirus, with `len(updated | antivirus)`. Find the same number without
using `|` at all. There are two different ways. Can you find both?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. One way is a formula from the tutorial, using `len` and `&`.
2. For the other, think about the laptops with *neither*. Which are
   they, in terms of the complements `laptops - updated` and
   `laptops - antivirus`?
3. Every laptop that is not in "neither" has at least one of the two.

**Think about:** which law from Unit 2 turns "not (A or B)" into
"not A and not B"?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
print(len(updated) + len(antivirus) - len(updated & antivirus))

neither = (laptops - updated) & (laptops - antivirus)
print(len(laptops) - len(neither))
```

Both print 14. The first is inclusion–exclusion. The second counts the
laptops outside both circles, and takes them away from the box.
"Outside both" is "not updated and no antivirus", which is De Morgan's
law from [Untangling a condition](tutorial:untangling-a-condition#de-morgans-laws),
written with sets: $(U_p \cup A)' = U_p' \cap A'$.

</details>

**8. Make.** A games shop asked 40 customers what they play on: phone,
console or PC. 22 play on a phone, 18 on a console and 12 on a PC. 8 play
on a phone and a console, 5 on a phone and a PC, and 6 on a console and
a PC. 2 play on all three. Fill in all eight regions, from the middle
out, in Python. How many customers play on none of the three? Check your
answer with the three-set formula.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The middle is 2.
2. Each pair's region on its own is the pair's total minus the middle.
3. Each "only" region is the circle's total minus the three other
   regions inside that circle.
4. "None" is 40 minus everything inside the circles.

**Think about:** if any region comes out below 0, what would that say
about the shop's numbers?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
asked = 40
phone, console, pc = 22, 18, 12
all_three = 2
phone_console_only = 8 - all_three
phone_pc_only = 5 - all_three
console_pc_only = 6 - all_three
phone_only = phone - phone_console_only - phone_pc_only - all_three
console_only = console - phone_console_only - console_pc_only - all_three
pc_only = pc - phone_pc_only - console_pc_only - all_three

inside = (all_three + phone_console_only + phone_pc_only + console_pc_only
          + phone_only + console_only + pc_only)
print(phone_only, console_only, pc_only)
print(inside, asked - inside)
print(22 + 18 + 12 - 8 - 5 - 6 + 2)
```

The "only" regions are 11, 6 and 3, and the pairs on their own are 6, 3
and 4. That puts 35 customers inside the circles, so 5 play on none of
the three. The formula also gives $52 - 19 + 2 = 35$.

</details>

**9. Explain.** The tutorial started with the names of the laptops in
sets, and drew each diagram from them. Only at the end did it
give a survey's totals and ask for the regions. Many textbooks start the
other way round, with a puzzle of totals filled in from the middle out.
If you were teaching Venn diagrams to a friend, which would you start
with, and why?

<details class="dl-answer"><summary>answer</summary>

There is more than one good answer. Here are some things to weigh.

- **What your friend needs them for.** An exam question usually gives
  totals, so starting there practises the thing that will be asked. A
  person reading survey results also meets totals, not names.
- **What makes a region make sense.** With names, a region is a set of
  real laptops, and every number in it can be checked by counting. With
  totals alone, a region is a number calculated by rules, and a miscount
  is harder to see.
- **Your friend.** Someone who likes puzzles may enjoy the totals first.
  Someone who has been lost by rules before may want something to point
  at first.

One answer says which friend you are thinking of, and what would
tell you that your choice was not working for them.

</details>

**10. Explain.** A newspaper reports a survey of 100 people: "60 read
the news online, 50 read a paper, and 5 do both." Without any code, how
can you tell that these three numbers cannot all be true? What is the
smallest number that "both" could be?

<details class="dl-answer"><summary>answer</summary>

By inclusion–exclusion, the people who read at least one are
$60 + 50 - 5 = 105$. That is more than the 100 people who were asked,
and a region inside the box cannot hold more people than the box. So
the three numbers cannot all be true.

The union can be at most 100, so $110 - \text{both} \le 100$, which
means "both" is at least 10. With exactly 10, everyone reads the news
one way or the other, and nobody is outside both circles.

</details>

**11. Predict.** A health centre runs a flu clinic on Monday morning and
another on Thursday evening. Nobody needs two flu vaccines, so nobody
goes to both. What will this cell print?

```python
monday = {"Ann", "Brian", "Chidi", "Dolores"}
thursday = {"Eamon", "Fern", "Gus"}
print(monday & thursday)
print(len(monday | thursday), len(monday) + len(thursday))
```

<details class="dl-answer"><summary>answer</summary>

```text
set()
7 7
```

`set()` is how Python shows the empty set: a set with nothing in it.
The two circles do not overlap, so $|A \cap B| = 0$, and
inclusion–exclusion becomes plain adding: $4 + 3 - 0 = 7$. This is the
case of "and multiplies, or adds" on
[Counting every outfit](tutorial:counting-every-outfit#and-multiplies-or-adds),
where the two groups share nothing.

</details>

## Stretch

**12. Make.** Write a function `exactly(groups, everyone, k)`. `groups`
is a list of sets, and the function returns the set of values in
`everyone` that are in exactly `k` of the groups. Test it on the
laptops: `exactly([updated, antivirus, backed_up], laptops, 2)` should
have 8 names. Then use it to check that the sizes for `k` = 0, 1, 2 and 3 add
up to 20.

```python exec
id: circles-practice-exactly
def exactly(groups, everyone, k):
    """Return the set of values in everyone that are in exactly k of the sets in groups."""
    ...
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Start with an empty set for the answer: `found = set()`.
2. Loop over `everyone`. For each value, count how many of the groups
   it is in, with a loop over `groups`.
3. If the count is `k`, add the value to `found` with `found.add(value)`.
4. Return `found` after the loop.

**Think about:** the loop in the tutorial's section "Yes to exactly
two". What changes, and what stays the same?

</details>

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Yours may be different and work too.

```python
def exactly(groups, everyone, k):
    """Return the set of values in everyone that are in exactly k of the sets in groups."""
    found = set()
    for value in everyone:
        count = 0
        for group in groups:
            if value in group:
                count = count + 1
        if count == k:
            found.add(value)
    return found


checks = [updated, antivirus, backed_up]
assert len(exactly(checks, laptops, 2)) == 8
sizes = []
for k in range(4):
    sizes.append(len(exactly(checks, laptops, k)))
print(sizes, sum(sizes))
```

This prints `[3, 7, 8, 2] 20`. Every laptop passed 0, 1, 2 or 3
checks, and to only one of those numbers, so the four sets share no
one and cover the whole box. The function works for any number of
groups: try it on the language class from problem 5.

</details>

**13. Another way.** Pick one of the 20 laptops at random. What is the
chance that it has exactly two of the three? Find it by counting,
from the tutorial's answer. Then find it a second way, with `simulate`
from [How likely is it?](tutorial:how-likely-is-it#a-tool-that-runs-it-many-times).

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. By counting: 8 of the 20 laptops have exactly two, and each laptop
   is equally likely to be picked.
2. For `simulate`, you need a trial: a function with no inputs that
   picks one laptop with `random.choice` and returns True when it is in
   exactly two sets.
3. `random.choice` needs a list, and `sorted(laptops)` makes one.

**Think about:** why will the two answers differ a little?

</details>

<details class="dl-answer"><summary>answer</summary>

By counting, the chance is $\frac{8}{20} = 0.4$.

```python
import random

names = sorted(laptops)


def picks_exactly_two():
    """Pick one laptop at random. True when it has exactly two of the three checks."""
    name = random.choice(names)
    yes_answers = 0
    for group in [updated, antivirus, backed_up]:
        if name in group:
            yes_answers = yes_answers + 1
    return yes_answers == 2


print(simulate(picks_exactly_two, 10000))
```

The simulation gives something near 0.4, such as 0.4031. It differs a
little from 0.4 every run, for the reason on
[How likely is it?](tutorial:how-likely-is-it#why-the-two-answers-differ):
each pick is left to chance.

</details>

**14. Predict.** On the tutorial, `updated ^ antivirus` gave every
laptop in exactly one of the two circles. Schlomo, who is learning
Python too, reasons that `updated ^ antivirus ^ backed_up` must give the
laptops in exactly one of the three circles. What do you think? Guess
how many names, and which regions they come from. Then run it.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Python calculates `updated ^ antivirus` first, then `^ backed_up`.
2. Follow Aoife's laptop, which is in all three. Is it in
   `updated ^ antivirus`? Is it in the answer after `^ backed_up`?
3. Follow Ben's, which is updated and has antivirus but no backup, and
   Tomas's, which only has a backup.

**Think about:** [Bits that flip](tutorial:bits-that-flip#counting-the-1s-parity)
and what XOR says about how many 1s there are.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
odd_ones = updated ^ antivirus ^ backed_up
print(len(odd_ones), sorted(odd_ones))
```

It gives 9 names: the 7 laptops with exactly one of the three, and the
2 with all three. Most people make Schlomo's guess. It holds for two
sets. For three, it includes the middle as well. A name is in the
answer when it is in an odd number of the sets: 1 or 3. That is parity, as on
[Bits that flip](tutorial:bits-that-flip): XOR of several bits is 1 when
the number of 1s is odd. Aoife's laptop is in all three:
`updated ^ antivirus` drops it, and `^ backed_up` puts it back.

</details>
