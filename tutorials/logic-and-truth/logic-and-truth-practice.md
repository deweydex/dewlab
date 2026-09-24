---
title: "Logic: truth tables, XOR and De Morgan's laws — Practice"
practice_for: logic-and-truth
year: "2026-2027"
version: 2026.08.23.1
---

# Logic: truth tables, XOR and De Morgan's laws — Practice

Each answer is hidden until you open it. Several of these problems ask
you to predict a truth table before you generate it. The prediction is
the real exercise, so try it first.

## Tools

This cell defines `table()`, which prints the truth table for any
operation on two inputs. The last line shows how to call it. There,
`lambda a, b: a and b` is a short way to write a small function with no
name: it takes `a` and `b`, and gives back `a and b`. To see another
table, change the part after the colon.

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

## Truth tables

**1.** Write down the truth table for `A and (not B)`. Then generate it, and compare.

<details class="dl-answer"><summary>answer</summary>

It is true only when A is true and B is false. That is one row out of
four.

</details>

**2.** How many rows does a truth table have for three inputs? For $n$ inputs?

<details class="dl-answer"><summary>answer</summary>

Three inputs give eight rows, and $n$ inputs give $2^n$ rows.

Each new input doubles the number of cases. That is why checking every
case stops being practical quite quickly. Twenty inputs give over a
million rows.

</details>

**3.** In how many of the four rows is `A or B` true? What about `A and B`?

<details class="dl-answer"><summary>answer</summary>

`A or B` is true in three rows, and `A and B` in one.

`or` is the generous one: it is false only when both inputs are false.
`and` is the strict one: it is true only when both inputs are true.

</details>

**4.** How is the logical `or` different from the everyday one?

<details class="dl-answer"><summary>answer</summary>

The logical `or` is true when both inputs are true. In everyday English,
"Tea or coffee?" usually means one or the other, and not both.

The everyday meaning is exclusive or. That is a different operation,
and Python has no keyword for it.

</details>

## Exclusive or

**5.** Write XOR using only `and`, `or` and `not`.

<details class="dl-answer"><summary>answer</summary>

`(a or b) and not (a and b)`. This says "at least one, but not both".

Another way is `(a and not b) or (b and not a)`. This one lists the two
rows where XOR is true.

</details>

**6.** Why does `a != b` do the same job for `True` and `False` values?

<details class="dl-answer"><summary>answer</summary>

When there are only two possible values, "exactly one is true" and "they
are different" are the same condition.

It is not a coincidence. It is one idea with two names, because people
came to it from different directions.

</details>

**7.** What is `a ^ a`, for either value of `a`? And what is `a ^ False`?

<details class="dl-answer"><summary>answer</summary>

`a ^ a` is `False`, and `a ^ False` is `a`.

Anything XOR itself is false, and XOR with false leaves a value
unchanged. Simple encryption uses both of these facts. XOR a message
with a key, then XOR the result again with the same key, and you get the
message back.

</details>

## De Morgan

**8.** Rewrite `not (A and B)` without the outer `not`.

<details class="dl-answer"><summary>answer</summary>

`(not A) or (not B)`.

Move the `not` inside the bracket, and the `and` becomes an `or`.

</details>

**9.** Rewrite `not (A or B)` without the outer `not`.

<details class="dl-answer"><summary>answer</summary>

`(not A) and (not B)`.

</details>

**10.** Simplify `not (not a or not b)`.

<details class="dl-answer"><summary>answer</summary>

`a and b`.

Use De Morgan's law on the whole expression. `not(not a or not b)` is
`not(not a) and not(not b)`. Two `not`s cancel each other, so this is
`a and b`.

</details>

**11.** Simplify `not (a and not b)`.

<details class="dl-answer"><summary>answer</summary>

`(not a) or b`.

</details>

**12.** Simplify `not (a or (b and not c))`.

<details class="dl-answer"><summary>answer</summary>

`(not a) and (not b or c)`.

First, move the outer `not` in. That gives `not a and not(b and not c)`.
Then move the inner `not` in. `not(b and not c)` becomes `not b or c`.

That is two steps, working from the outside in. With three inputs there
are eight combinations, so check your answer with a loop over all
eight.

</details>

**13.** Why is a loop over four rows a *proof* here, when "I tested it and it worked" usually is not?

<details class="dl-answer"><summary>answer</summary>

There are exactly four possible inputs, and the loop tried all of them.
Nothing is left untested.

For almost anything else, such as a function that takes whole numbers,
the possible inputs never run out. A test can then only fail to find a
problem. Checking every case is a proof when there are few enough cases
to check them all, and almost never otherwise.

</details>

## Readability

**14.** Simplify `not (not attended or not submitted)`.

<details class="dl-answer"><summary>answer</summary>

`attended and submitted`.

People rarely write the first version on purpose. It grows a little at a
time: someone adds a condition, later puts a `not` around the whole
thing, then adds another condition. That is why knowing the rule
matters.

</details>

**15.** A system logs an error when `not (status == "ok" and errors == 0)`. Rewrite the condition so that a reader can see what causes a log entry.

<details class="dl-answer"><summary>answer</summary>

`status != "ok" or errors != 0`.

Now it reads as what it means: either something is wrong with the
status, or there are errors.

</details>

**16.** Rewrite `not (age >= 18 and has_id)`.

<details class="dl-answer"><summary>answer</summary>

`age < 18 or not has_id`.

Look at the first part. `not (age >= 18)` becomes `age < 18`, and not
`age <= 18`. Getting a boundary wrong by one, like this, is called an
*off-by-one error*. It is one of the most common mistakes in
conditions.

</details>

## Sets

**17.** Take everyone $= \{1, 2, 3, 4, 5, 6, 7, 8\}$, $A = \{1, 2, 3, 4\}$ and $B = \{3, 4, 5, 6\}$. Find the complement of $A \cup B$. Then find the intersection of the two complements, of $A$ and of $B$.

<details class="dl-answer"><summary>answer</summary>

$A \cup B = \{1, 2, 3, 4, 5, 6\}$, so its complement is $\{7, 8\}$.

The complement of $A$ is $\{5, 6, 7, 8\}$, and the complement of $B$ is
$\{1, 2, 7, 8\}$. Their intersection is $\{7, 8\}$.

The two answers are the same. This is De Morgan's law, on sets.

</details>

**18.** Which set operation matches `and`? Which matches `or`? Which matches `not`?

<details class="dl-answer"><summary>answer</summary>

Intersection matches `and`, union matches `or`, and complement matches
`not`.

"Is this item in the set?" and "Is this statement true?" are the same
kind of question, asked about different things. That is why the same two
laws hold for both.

</details>

**19.** What is the set version of XOR?

<details class="dl-answer"><summary>answer</summary>

The symmetric difference: everything that is in exactly one of the two
sets. Python writes it `A ^ B`. It uses the same operator as XOR on
`True` and `False`, for the same reason.

</details>

## One longer one

**20.** A door unlocks when all three of these hold: the card is valid; it is during working hours, or the person is a manager; and the door is not in lockdown.

- (a) Write this as a Python expression.
- (b) A colleague writes the "does not unlock" case as `not valid or not (hours or manager) or lockdown`. Is that right?
- (c) Simplify the middle part of their expression.

<details class="dl-answer"><summary>answer</summary>

(a) `valid and (hours or manager) and not lockdown`.

(b) Yes. De Morgan's law turns a `not` around three things joined by
`and` into three `not`s joined by `or`. And `not (not lockdown)` is
`lockdown`.

(c) `not (hours or manager)` becomes `not hours and not manager`. In
words: outside working hours, and not a manager.

So the whole expression reads: the door does not unlock if the card is
invalid, or it is outside working hours and the person is not a
manager, or the door is in lockdown. Somebody could check that sentence
against the real rules for the door, and that is the point of
rewriting it.

</details>
