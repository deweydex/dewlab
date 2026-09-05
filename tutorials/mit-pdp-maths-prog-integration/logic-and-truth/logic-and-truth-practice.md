---
title: "Logic and Truth — Practice"
slug: logic-and-truth-practice
practice_for: logic-and-truth
module: mit-pdp-maths-prog-integration
module_title: "Programming and Maths, Integrated"
year: "2026-2027"
series: data-chance-and-logic
version: 2026.08.23.1
---

# Logic and Truth — Practice

Answers are folded. Several of these ask you to predict a table before generating it — the prediction is the exercise.

## Tools

```python exec
id: tools-1
def table(expression, names=("A", "B")):
    """Print a truth table for a function of two booleans."""
    header = "   ".join(f"{n:>5}" for n in names)
    print(f"{header}      result")
    for a in [True, False]:
        for b in [True, False]:
            print(f"{str(a):>5}   {str(b):>5}      {str(expression(a, b)):>5}")


table(lambda a, b: a and b)
```

## Truth Tables

**1.** Write the table for `A and (not B)` before generating it.

<details class="dl-answer"><summary>answer</summary>

True only when A is true and B is false — one row out of four.

</details>

**2.** How many rows does a truth table have for three inputs? For n?

<details class="dl-answer"><summary>answer</summary>

Eight, and `2ⁿ`.

Each input doubles the number of cases, which is why exhaustive checking stops being practical quite quickly — twenty inputs is over a million rows.

</details>

**3.** `A or B` is true in how many of the four rows? And `A and B`?

<details class="dl-answer"><summary>answer</summary>

Three and one.

`or` is the generous one — it only fails when both fail. `and` is the strict one.

</details>

**4.** How does the logical `or` differ from the everyday one?

<details class="dl-answer"><summary>answer</summary>

The logical `or` is true when both are true. "Tea or coffee?" usually means one or the other and not both.

The everyday meaning is exclusive or, which is a different operation and does not have a keyword in Python.

</details>

## Exclusive Or

**5.** Write XOR using only `and`, `or` and `not`.

<details class="dl-answer"><summary>answer</summary>

`(a or b) and not (a and b)` — at least one, but not both.

Or equivalently `(a and not b) or (b and not a)`, which lists the two true rows directly.

</details>

**6.** Why does `a != b` do the same job for booleans?

<details class="dl-answer"><summary>answer</summary>

Because "exactly one is true" and "they are different" are the same condition when there are only two possible values.

That is not a coincidence — it is one idea named twice by people who came at it from different directions.

</details>

**7.** What is `a ^ a` for any boolean a? And `a ^ False`?

<details class="dl-answer"><summary>answer</summary>

False, and a.

Anything XOR itself is false, and XOR with false leaves things alone. Both of those get used in simple encryption: XOR a message with a key and then XOR again with the same key, and you get the message back.

</details>

## De Morgan

**8.** Rewrite `not (A and B)` without the outer `not`.

<details class="dl-answer"><summary>answer</summary>

`(not A) or (not B)`.

Push the `not` inside and the `and` becomes an `or`.

</details>

**9.** Rewrite `not (A or B)` without the outer `not`.

<details class="dl-answer"><summary>answer</summary>

`(not A) and (not B)`.

</details>

**10.** Simplify `not (not a or not b)`.

<details class="dl-answer"><summary>answer</summary>

`a and b`.

Apply De Morgan to the inside: `not(not a or not b)` is `not(not a) and not(not b)`, which is `a and b`.

</details>

**11.** Simplify `not (a and not b)`.

<details class="dl-answer"><summary>answer</summary>

`(not a) or b`.

</details>

**12.** Simplify `not (a or (b and not c))`.

<details class="dl-answer"><summary>answer</summary>

`(not a) and (not b or c)`.

Push the outer `not` in: `not a and not(b and not c)`. Then push the inner one: `not b or c`.

Two steps, working outwards in. Check it by looping over all eight combinations.

</details>

**13.** Why is looping over four rows a *proof* here, when "I tested it and it worked" usually is not?

<details class="dl-answer"><summary>answer</summary>

Because the space of possible inputs has exactly four things in it and the loop visited all of them. There is nothing left untested.

For almost anything else — a function of integers, say — the space is unbounded and a test can only fail to find a problem. Exhaustive checking is a proof when the space is small enough to exhaust, and almost never otherwise.

</details>

## Readability

**14.** Simplify `not (not attended or not submitted)`.

<details class="dl-answer"><summary>answer</summary>

`attended and submitted`.

Nobody writes the first version deliberately. They arrive at it by adding a condition, negating the whole thing later, and adding another — the tangle grows a bit at a time, which is why knowing the rule matters.

</details>

**15.** A system logs an error when `not (status == "ok" and errors == 0)`. Rewrite it so a reader can see what triggers a log.

<details class="dl-answer"><summary>answer</summary>

`status != "ok" or errors != 0`.

Now it reads as what it is: something is wrong with the status, or there are errors.

</details>

**16.** `not (age >= 18 and has_id)` — rewrite it.

<details class="dl-answer"><summary>answer</summary>

`age < 18 or not has_id`.

Note that `not (age >= 18)` becomes `age < 18` rather than `age <= 18`. Getting the boundary wrong here is the single most common off-by-one in condition logic.

</details>

## Sets

**17.** Given `everyone = {1..8}`, `A = {1,2,3,4}` and `B = {3,4,5,6}`, compute the complement of `A ∪ B`, and the intersection of the two complements.

<details class="dl-answer"><summary>answer</summary>

`A ∪ B = {1,2,3,4,5,6}`, so its complement is `{7,8}`.

`complement(A) = {5,6,7,8}` and `complement(B) = {1,2,7,8}`, and their intersection is `{7,8}`.

The same, which is De Morgan on sets.

</details>

**18.** Which set operation corresponds to `and`? To `or`? To `not`?

<details class="dl-answer"><summary>answer</summary>

Intersection, union, and complement.

An item being in a set and a statement being true are the same question asked about different things, which is why the same two laws hold for both.

</details>

**19.** What is the set equivalent of XOR?

<details class="dl-answer"><summary>answer</summary>

Symmetric difference — everything in exactly one of the two sets. Python spells it `A ^ B`, using the same operator as for booleans, and for the same reason.

</details>

## One Longer One

**20.** A door unlocks when: the card is valid, AND it is either during working hours or the person is a manager, AND the door is not in lockdown.

- (a) Write it as a Python expression.
- (b) A colleague writes the "does not unlock" case as `not valid or not (hours or manager) or lockdown`. Is that right?
- (c) Simplify their middle term.

<details class="dl-answer"><summary>answer</summary>

(a) `valid and (hours or manager) and not lockdown`.

(b) Yes. De Morgan on a three-way `and` gives a three-way `or` of the negations, and `not (not lockdown)` is `lockdown`.

(c) `not (hours or manager)` becomes `not hours and not manager` — outside working hours and not a manager.

So the whole thing reads: it fails to unlock if the card is invalid, or it is out of hours and you are not a manager, or the door is locked down. Which is a sentence somebody could check against the actual policy — and that is the point of the rewriting.

</details>
