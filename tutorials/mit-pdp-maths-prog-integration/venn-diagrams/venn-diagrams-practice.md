---
title: "Drawing Sets — Practice"
slug: venn-diagrams-practice
practice_for: venn-diagrams
module: mit-pdp-maths-prog-integration
module_title: "Programming and Maths, Integrated"
year: "2026-2027"
series: data-chance-and-logic
version: 2026.08.23.1
---

# Drawing Sets — Practice

Answers are folded. Where a question asks about three sets, sketch the diagram before you reason about it — that is what the diagram is for.

## Tools

```python exec
id: tools-1
everyone = {"Aoife", "Ben", "Cara", "Dara", "Eoin", "Fiona", "Gearoid", "Hannah", "Iarla"}
python = {"Aoife", "Ben", "Cara", "Dara", "Eoin", "Fiona"}
sql = {"Cara", "Dara", "Eoin", "Gearoid", "Hannah"}
javascript = {"Dara", "Eoin", "Fiona", "Hannah", "Iarla"}


def complement(s):
    return everyone - s


print("python & sql :", sorted(python & sql))
print("python - sql :", sorted(python - sql))
print("python | sql :", sorted(python | sql))
print("python ^ sql :", sorted(python ^ sql))
```

## Two Sets

**1.** Using the sets above, who knows Python but not SQL?

<details class="dl-answer"><summary>answer</summary>

`python - sql` = Aoife, Ben, Fiona.

</details>

**2.** Who knows exactly one of Python and SQL?

<details class="dl-answer"><summary>answer</summary>

`python ^ sql` = Aoife, Ben, Fiona, Gearoid, Hannah.

That is symmetric difference, which is XOR for sets — in one or the other but not both.

</details>

**3.** Who knows neither?

<details class="dl-answer"><summary>answer</summary>

`everyone - (python | sql)` = Iarla.

</details>

**4.** In a two-circle diagram, how many regions are there, counting the outside?

<details class="dl-answer"><summary>answer</summary>

Four: only left, only right, both, and neither.

The outside region is easy to forget and is often the one a question is about.

</details>

**5.** A class of 30 has 18 doing Maths and 15 doing Physics, and 7 doing both. How many do neither?

<details class="dl-answer"><summary>answer</summary>

Doing at least one: 18 + 15 − 7 = 26. So 4 do neither.

Subtracting the 7 is the whole trick — adding 18 and 15 counts the seven twice, once in each subject.

</details>

**6.** Why does `|A ∪ B| = |A| + |B| − |A ∩ B|` need that last term?

<details class="dl-answer"><summary>answer</summary>

Because anyone in both sets has been counted twice, once in each, so the overlap must be taken off once.

This is the inclusion-exclusion principle, and the diagram makes it obvious in a way the formula does not.

</details>

## Three Sets

**7.** How many regions does a three-circle diagram have, counting the outside?

<details class="dl-answer"><summary>answer</summary>

Eight. Each set is either in or out, so `2³`.

</details>

**8.** Who knows Python or SQL but not JavaScript?

<details class="dl-answer"><summary>answer</summary>

`(python | sql) - javascript` = Aoife, Ben, Cara, Gearoid.

</details>

**9.** Who knows all three?

<details class="dl-answer"><summary>answer</summary>

`python & sql & javascript` = Dara, Eoin.

</details>

**10.** Are `(python & sql) | (python & javascript)` and `python & (sql | javascript)` the same set?

<details class="dl-answer"><summary>answer</summary>

Yes. Both give Cara, Dara, Eoin, Fiona.

This is the distributive law, and it is exactly the same shape as `(a and b) or (a and c)` being the same as `a and (b or c)` in *Logic and Truth*.

</details>

**11.** Shade, on a three-circle diagram, the region for `A − (B ∪ C)`. Describe it in words.

<details class="dl-answer"><summary>answer</summary>

The part of A that overlaps neither of the others — the leftmost of the three outer petals.

In words: in A only.

</details>

**12.** A survey of 100 people: 60 use email, 45 use messaging, 30 use both. How many use at least one?

<details class="dl-answer"><summary>answer</summary>

60 + 45 − 30 = 75.

</details>

**13.** Same survey, with a third option: 60 email, 45 messaging, 40 phone, 30 email+messaging, 20 email+phone, 15 messaging+phone, 10 all three. How many use at least one?

<details class="dl-answer"><summary>answer</summary>

60 + 45 + 40 − 30 − 20 − 15 + 10 = 90.

Add the singles, subtract the pairs, add the triple back. The last step is there because the ten who use all three were added three times and then subtracted three times, leaving them at zero.

Doing this without a diagram is genuinely hard, which is the argument for the diagram.

</details>

## De Morgan on Sets

**14.** Is the complement of `A ∪ B` the same as the intersection of the complements?

<details class="dl-answer"><summary>answer</summary>

Yes. Being outside both circles is the same as being outside the first and outside the second.

Shade it and the two descriptions land on exactly the same region.

</details>

**15.** Is the complement of `A ∩ B` the same as the union of the complements?

<details class="dl-answer"><summary>answer</summary>

Yes. Being outside the overlap means missing at least one of the two, which is being outside the first or outside the second.

</details>

**16.** How does this proof differ from the truth-table one in *Logic and Truth*?

<details class="dl-answer"><summary>answer</summary>

The truth table checks four cases exhaustively and is complete for that reason.

The diagram convinces you by showing that two descriptions pick out the same region, which is a different kind of seeing.

Neither is better. They are the same claim in two notations, which is why the pairing is worth having — if one of them did not land, the other might.

</details>

## Where It Runs Out

**17.** Four sets would need how many regions? Can four circles produce them?

<details class="dl-answer"><summary>answer</summary>

Fifteen, plus the outside. And no — no arrangement of four circles in a plane gives all sixteen regions.

Diagrams for four sets exist, using ellipses or stranger shapes, and they stop being readable, which rather defeats the point.

</details>

**18.** What still works fine at four sets?

<details class="dl-answer"><summary>answer</summary>

The set operations. `A & B & C & D` is no harder to compute than `A & B`, and inclusion-exclusion generalises to any number of sets.

Every representation runs out somewhere, and knowing where is part of knowing it. A picture that helps enormously at three and not at all at four is still a good tool.

</details>

## One Longer One

**19.** A support team logs tickets by category: 120 hardware, 95 software, 60 network. 30 are both hardware and software, 25 hardware and network, 20 software and network, and 10 are all three. There are 250 tickets in total.

- (a) How many are in at least one category?
- (b) How many are in none?
- (c) How many are hardware only?

<details class="dl-answer"><summary>answer</summary>

(a) 120 + 95 + 60 − 30 − 25 − 20 + 10 = 210.

(b) 250 − 210 = 40.

(c) Start with 120, remove those also in software (30) and those also in network (25) — but that removed the ten in all three twice, so add ten back: 120 − 30 − 25 + 10 = 75.

Part (c) is where a diagram earns its place. The all-three region being subtracted twice is nearly impossible to keep track of without one, and nearly obvious with one.

</details>
