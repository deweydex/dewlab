---
title: "Venn diagrams: drawing sets and their overlaps — Practice"
practice_for: venn-diagrams
year: "2026-2027"
version: 2026.08.23.1
---

# Venn diagrams: drawing sets and their overlaps — Practice

Each answer is hidden until you open it. When a question is about three
sets, sketch the diagram first, and then find the answer. The diagram is
there to help you think.

## Tools

This cell creates the whole class, `everyone`, and the three sets of
students from the tutorial. It also defines `complement()`. Run it
before you try the problems, and use it to check your answers.

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

## Two sets

**1.** Using the sets above, who knows Python but not SQL?

<details class="dl-answer"><summary>answer</summary>

`python - sql` gives Aoife, Ben and Fiona.

</details>

**2.** Who knows exactly one of Python and SQL?

<details class="dl-answer"><summary>answer</summary>

`python ^ sql` gives Aoife, Ben, Fiona, Gearoid and Hannah.

This is the symmetric difference, which is XOR for sets: the people in
one set or the other, but not in both.

</details>

**3.** Who knows neither Python nor SQL?

<details class="dl-answer"><summary>answer</summary>

`everyone - (python | sql)` gives Iarla.

</details>

**4.** How many regions does a two-circle diagram have, if you count the outside?

<details class="dl-answer"><summary>answer</summary>

It has four: only in the left circle, only in the right circle, in both,
and in neither.

The outside region is easy to forget, and it is often the one a
question asks about.

</details>

**5.** In a class of 30, 18 students take Maths and 15 take Physics. 7 of them take both. How many take neither?

<details class="dl-answer"><summary>answer</summary>

The number taking at least one subject is $18 + 15 - 7 = 26$. So
$30 - 26 = 4$ take neither.

The key step is to take away the 7. When we add 18 and 15, we count
those seven students twice, once in each subject.

</details>

**6.** Why does $|A \cup B| = |A| + |B| - |A \cap B|$ need that last term?

<details class="dl-answer"><summary>answer</summary>

Anyone in both sets is counted twice in $|A| + |B|$, once in each set.
So we take the overlap away once.

This is the inclusion-exclusion principle. On the diagram you can see
why it works. The overlap sits inside both circles. The formula alone
does not show that.

</details>

## Three sets

**7.** How many regions does a three-circle diagram have, if you count the outside?

<details class="dl-answer"><summary>answer</summary>

It has eight. For each of the three sets, a person is either in it or
out of it. That gives $2 \times 2 \times 2 = 2^3 = 8$ combinations.

</details>

**8.** Who knows Python or SQL, but not JavaScript?

<details class="dl-answer"><summary>answer</summary>

`(python | sql) - javascript` gives Aoife, Ben, Cara and Gearoid.

</details>

**9.** Who knows all three?

<details class="dl-answer"><summary>answer</summary>

`python & sql & javascript` gives Dara and Eoin.

</details>

**10.** Are `(python & sql) | (python & javascript)` and `python & (sql | javascript)` the same set?

<details class="dl-answer"><summary>answer</summary>

Yes. Both give Cara, Dara, Eoin and Fiona.

This is the distributive law. You met it in problem 6 of
[Sets: building them from sorted lists — Practice](tutorial:sets-as-sorted-lists-practice).
It has the same shape as
a rule about `True` and `False`: `(a and b) or (a and c)` is the same as
`a and (b or c)`. You could check that rule with a loop over every case,
as in [Logic: truth tables, XOR and De Morgan's laws](tutorial:logic-and-truth).

</details>

**11.** On a three-circle diagram, shade the region for $A \setminus (B \cup C)$. Describe it in words.

<details class="dl-answer"><summary>answer</summary>

It is the part of circle A that does not overlap either of the other
circles. That is A's outer region, the one that belongs to A alone.

In words, it is the part in A only.

</details>

**12.** In a survey of 100 people, 60 use email, 45 use messaging, and 30 use both. How many use at least one?

<details class="dl-answer"><summary>answer</summary>

$60 + 45 - 30 = 75$ people use at least one.

</details>

**13.** The same survey adds a third option, the phone. Now 60 use email, 45 use messaging and 40 use the phone. 30 use email and messaging, 20 use email and the phone, and 15 use messaging and the phone. 10 use all three. How many use at least one?

<details class="dl-answer"><summary>answer</summary>

The answer is $60 + 45 + 40 - 30 - 20 - 15 + 10 = 90$.

There are three steps: add the single sets, take away the pairs, then
add the triple back. Why add the triple back? The ten people who use all
three were added three times, once for each single set. Then they were
taken away three times, once for each pair. That leaves them counted
zero times, so we add them back once.

This is hard to do without a diagram. That is a good reason to draw
one.

</details>

## De Morgan on sets

**14.** Is the complement of $A \cup B$ the same as the intersection of the two complements?

<details class="dl-answer"><summary>answer</summary>

Yes. A point outside both circles is outside the first circle and
outside the second.

Shade both descriptions on a diagram, and they cover exactly the same
region.

</details>

**15.** Is the complement of $A \cap B$ the same as the union of the two complements?

<details class="dl-answer"><summary>answer</summary>

Yes. A point outside the overlap misses at least one of the two
circles. So it is outside the first circle or outside the second.

</details>

**16.** How is this proof different from the truth-table proof in [Logic: truth tables, XOR and De Morgan's laws](tutorial:logic-and-truth)?

<details class="dl-answer"><summary>answer</summary>

The truth table checks all four cases. It is complete because there are
no other cases.

The diagram convinces you in a different way. It shows you that two
descriptions pick out the same region, so you see the answer.

Neither proof is better. They are the same claim in two notations, and
that is why it helps to have both. If one of them did not make sense to
you, the other might.

</details>

## Where it runs out

**17.** How many regions would four sets need? Can four circles make them?

<details class="dl-answer"><summary>answer</summary>

Four sets need fifteen regions, plus the outside, which makes sixteen.
And no arrangement of four circles on a flat page gives all sixteen
regions.

Diagrams for four sets do exist. They use ovals or stranger shapes, and
they get much harder to read, so they no longer help.

</details>

**18.** What still works well at four sets?

<details class="dl-answer"><summary>answer</summary>

The set operations still work well. `A & B & C & D` is no harder to compute than
`A & B`. Inclusion-exclusion also works for any number of sets.

Every way of showing an idea stops working at some point. A Venn
diagram helps a lot with three sets and not at all with four, and it is
still a good tool.

</details>

## One longer one

**19.** A support team sorts its tickets by category. There are 120 hardware tickets, 95 software tickets and 60 network tickets. 30 tickets are both hardware and software, 25 are hardware and network, and 20 are software and network. 10 are in all three categories. There are 250 tickets in total.

- (a) How many tickets are in at least one category?
- (b) How many are in none?
- (c) How many are hardware only?

<details class="dl-answer"><summary>answer</summary>

(a) $120 + 95 + 60 - 30 - 25 - 20 + 10 = 210$.

(b) $250 - 210 = 40$.

(c) Start with the 120 hardware tickets. Take away the ones that are
also software (30) and the ones that are also network (25). But that
takes away the ten tickets in all three categories twice, so add ten
back: $120 - 30 - 25 + 10 = 75$.

A diagram becomes useful in part (c). Without one, it is very hard
to notice that the all-three region was taken away twice. With one, it
is easy to see.

</details>
