---
title: "Solving equations: keeping it level"
year: "2026-2027"
version: 2026.09.27.2
worlds:
  numbers: Normal numbers, like 3 and 10.
  squiggles: Shapes like ♡ and △, which can stand for any number.
  letters: Letters like b and n, which can stand for any number.
---

# Solving equations: keeping it level

Here is the balance from the last page, written with signs:

$$\square + 3 = 7$$

The left pan holds a closed box and 3 beads. The right pan holds 7
beads. All the beads weigh the same, and the box weighs only what is
inside it. The bar is level: flat, and not tipped to one side. On the
last page, we found the box by guessing. This page finds it another
way.

```question
id: take-from-both-1
type: multiple-choice
answer: 1

We take 3 beads from the left pan. We take 3 beads from the right pan
too. What does the bar do?

- It stays level
  - Both pans lose the same weight. So they still weigh the same.
- The left pan goes down
  - The left pan lost 3 beads. So did the right pan.
- The right pan goes down
  - The right pan has more beads we can see. But both pans lost 3.
    The difference between them did not change.
```

## What is still on the pans

Here is the balance after we take 3 beads from each pan.

<img src="take-three.svg" alt="A balance with its bar level. The left pan holds one closed box, marked with a question mark, and no beads. The right pan holds 4 beads.">

```question
id: what-is-still-on-the-pans-1
type: fill-in-the-blank

The left pan now holds
{only the box|the box and 3 beads|nothing}.

The right pan now holds
{4|7|3}
beads.

So the box holds
{4|7|3}
beads.
```

We write what we did one line at a time:

$$\square + 3 = 7$$

$$\square = 4$$

This is the same answer as the guess on the last page. This time, we
did not need to guess.

## From one side only

What goes differently if we take beads from one side only? Start again
with □ + 3 = 7. This time, we take 3 beads from the left pan, and none
from the right pan.

```question
id: from-one-side-only-1
type: multiple-choice
answer: 1

What does the bar do?

- The right pan goes down
  - The left pan now holds only the box, which is 4 beads. The right
    pan still holds 7. The heavier pan goes down.
- It stays level
  - The left pan lost 3 beads, and the right pan lost none. Their
    weights are different now.
- The left pan goes down
  - The left pan got lighter. A lighter pan goes up.
```

Somebody took 3 beads from the left pan only. Then they read the pans:
the box on one side, 7 beads on the other. They wrote □ = 7. We can
check that. Put 7 in the box, and return to the first balance.

```question
id: from-one-side-only-2
type: fill-in-the-blank

With 7 in the box, the left pan of □ + 3 = 7 holds 7 + 3, which is
{10|7|4}
beads.

Is that the same as the 7 beads on the right pan?
{No|Yes}
```

The bar tipped, so the pans did not tell us the box any more.

## The same on both sides

Here is the idea of this page. Whatever we do to one pan, we do the
same to the other pan. Then the bar stays level. Choose numbers, shapes
or letters in the list under the title.

<div class="dl-world" data-world="numbers">

```question
id: the-same-on-both-sides-1--numbers
type: fill-in-the-blank

In ? + 5 = 11, we take
{5|11|6}
beads from both pans.

Then the ? holds
{6|16|5}.
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: the-same-on-both-sides-1--squiggles
type: fill-in-the-blank

In ♡ + 5 = 11, we take
{5|11|6}
beads from both pans.

Then the ♡ holds
{6|16|5}.
```

</div>

<div class="dl-world" data-world="letters">

```question
id: the-same-on-both-sides-1--letters
type: fill-in-the-blank

In x + 5 = 11, we take
{5|11|6}
beads from both pans.

Then x is
{6|16|5}.
```

</div>

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Draw the balance. The left pan has the box and 5 loose beads.
2. The loose beads on the left sit beside the box. We want the box on
   its own.
3. Take those beads from the left pan. Take the same number from the
   right pan.

**Think about:** what is still on the right pan after that.

**Try this next:** □ + 8 = 20.

</details>

## Taking away undoes adding

On [Subtracting fractions: taking slices away](tutorial:taking-slices-away),
we took slices from a plate. Start with 3/8 of a pizza. Add 2 slices,
and you have 5/8. Take the same 2 slices away, and you have
3/8 again. Taking away undoes adding.

The box was built in the same way. We started with the box, and added
3 beads. So we undo it by taking 3 beads away, from both pans.

```question
id: taking-away-undoes-adding-1
type: fill-in-the-blank

In □ + 9 = 15, 9 beads were added to the box. To undo that, we
{take away 9|add 9|take away 15}
beads from both pans.

Then the box holds
{6|24|9}.
```

To *solve*{.term} an equation is to find the unknown, the number in the box.
We solved □ + 9 = 15 without a single guess.

{{include: setup/zen-calm-check.md}}

## Sharing into equal groups

Here is 3 × □ = 12 from the last page. The left pan holds three boxes,
all the same. The right pan holds 12 beads. The bar is level.

<img src="three-boxes.svg" alt="A level balance. The left pan holds three closed boxes, each marked with a question mark. The right pan holds 12 beads.">

$$3 \times \square = 12$$

The right pan has no box, so we cannot take a box from both pans. But
we can share. Share the left pan into 3 equal groups: each group is
one box. Share the right pan into 3 equal groups too. Now compare one
group from each pan. They still balance.

```question
id: sharing-into-equal-groups-1
type: fill-in-the-blank

12 beads, shared into 3 equal groups, make groups of
{4|9|36}
beads.

So the box holds
{4|9|36}.
```

Sharing into equal groups is *dividing*{.term}. Multiplying by 3 is undone by
dividing by 3.

```question
id: sharing-into-equal-groups-2
type: fill-in-the-blank

In 5 × □ = 30, we share both pans into
{5|30|6}
equal groups.

Then the box holds
{6|25|150}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The left pan holds 5 boxes, all the same.
2. Share it into 5 groups. How many boxes are in each group?
3. Share the 30 beads on the right into the same number of groups.

**Think about:** why the number of groups comes from the number of
boxes.

**Try this next:** 4 × □ = 28.

</details>

## Two boxes and a bead

Now the left pan holds two boxes and 1 loose bead. The right pan holds
9 beads.

<img src="two-boxes.svg" alt="A balance with its bar level. The left pan holds two closed boxes, each marked with a question mark, and 1 bead. The right pan holds 9 beads.">

$$2 \times \square + 1 = 9$$

```question
id: two-boxes-and-a-bead-1
type: multiple-choice
answer: 1

Which move helps first?

- Take 1 bead from each pan
  - Then the two boxes are on their own, against 8 beads.
- Share each pan into 2 equal groups
  - 9 beads do not share into 2 equal groups of whole beads. The loose
    bead on the left would need sharing too.
- Take 1 bead from the left pan only
  - Then the bar tips. A tipped bar does not tell us the box.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Try to share 9 beads into 2 equal groups. What happens to the last
   bead?
2. Now look at the loose bead on the left pan. Which move takes it
   away, and keeps the bar level?
3. After that move, what is on each pan?

**Think about:** which comes first: taking the loose bead away, or
sharing the two boxes.

**Try this next:** 2 × □ + 3 = 11.

</details>

## One move at a time

```question
id: one-move-at-a-time-1
type: fill-in-the-blank

After we take 1 bead from each pan, the left pan holds
{2 boxes|2 boxes and 1 bead|1 box}.

The right pan holds
{8|9|10}
beads.

We share both pans into 2 equal groups. One box balances
{4|8|3}
beads.
```

Here are the moves, one line at a time:

$$2 \times \square + 1 = 9$$

$$2 \times \square = 8$$

$$\square = 4$$

## The opposite order

Here is how the box was built, and how we undid it.

- **Building:** start with the box. Multiply by 2. Then add 1. We get 9.
- **Undoing:** start with 9. Take away 1. Then divide by 2. We get the
  box.

The undoing steps come in the opposite order. Adding 1 was the last
building step, so we undo it first.

```question
id: the-opposite-order-1
type: multiple-choice
answer: 1

A box is built in two steps. First multiply by 3. Then add 2. It
makes 17. Which undoing step comes first?

- Take away 2
  - Adding 2 was the last building step, so it is the first to undo.
- Divide by 3
  - Multiplying by 3 was the first building step. It is undone last.
- Add 2
  - Adding 2 again builds more. It does not undo.
```

<div class="dl-world" data-world="numbers">

```question
id: the-opposite-order-2--numbers
type: fill-in-the-blank

In 3 × ? + 2 = 17, we first take
{2|3|17}
from both sides.

That leaves 3 × ? =
{15|19|51}.

So the ? holds
{5|15|6}.
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: the-opposite-order-2--squiggles
type: fill-in-the-blank

In 3 × ♡ + 2 = 17, we first take
{2|3|17}
from both sides.

That leaves 3 × ♡ =
{15|19|51}.

So the ♡ holds
{5|15|6}.
```

</div>

<div class="dl-world" data-world="letters">

```question
id: the-opposite-order-2--letters
type: fill-in-the-blank

In 3 × n + 2 = 17, we first take
{2|3|17}
from both sides.

That leaves 3 × n =
{15|19|51}.

So n is
{5|15|6}.
```

</div>

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Picture the balance. The left pan has 3 boxes and 2 loose beads.
2. Take the loose beads from both pans first. What is on the right pan
   now?
3. Share both pans into 3 equal groups.

**Think about:** what "take away 2" does to the 17 on the right.

**Try this next:** 4 × □ + 1 = 21.

</details>

## A checking machine

Python is a language for computers. It can put our answer back in the
box, and check that both pans match. Python cannot use □ as a name, so
the cell uses the word `box`. In Python, `*` means times, and `==` asks
"are these the same?"

```python exec
id: a-checking-machine-1
hint: Put 4 in the box. Is 2 × 4 + 1 the same as 9? Make a guess now, or run the cell and see.
box = 4
left_pan = 2 * box + 1
right_pan = 9

print(left_pan, right_pan)
print(left_pan == right_pan)
```

```predict
type: choice

Before you run it: what will the last line print?

- True
  - 2 × 4 is 8, and 8 + 1 is 9. Both pans hold 9.
- False
  - The cell builds the left pan from the box, so it can feel as if it
    will not match.
- 9 9
  - The line before it prints both pans. This line asks if they match.
```

It prints `9 9`, and then `True`. Now change `box = 4` to another
number, and run it again. Which numbers make it print `True`?

## One side only, checked

Somebody solved 2 × □ + 1 = 9 in another way. They took the 1 bead from
the left pan only. That left 2 × □ against 9 beads. Then they shared
both pans into 2 equal groups, and wrote □ = 4.5. We put 4.5 back in
the box to check. Python writes a half as `.5`.

```python exec
id: one-side-only-checked-1
hint: 2 × 4.5 is 9. What is 9 + 1? Make a guess now, or run the cell and see.
box = 4.5
print(2 * box + 1)
```

```predict
type: number

Before you run it: what will it print?
```

It prints `10.0`. The `.0` means Python worked with a decimal. 10 is not
9, so the two sides of 2 × □ + 1 = 9 do not match. The bead was taken
from one pan only, and the bar tipped. Every move after that started from
a tipped bar.

## Boxes on both pans

This one goes a step past the page. Now there are boxes on both pans:

$$3 \times \square + 2 = \square + 10$$

A box weighs the same wherever it is. So we can take one box from each
pan, and the bar stays level.

```question
id: boxes-on-both-pans-1
type: fill-in-the-blank

After we take one box from each pan, we have
{2 × □ + 2 = 10|3 × □ + 2 = 10|2 × □ + 2 = □ + 10}.

So the box holds
{4|6|12}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The left pan has 3 boxes and 2 beads. Take one box away. What is
   still there?
2. The right pan has 1 box and 10 beads. Take one box away. What is
   still there?
3. Now it is a balance like the one in *Two boxes and a bead*. Undo
   one step at a time.

**Think about:** why we may take a box from each pan, even though we
do not know what it holds.

**Try this next:** put your answer back in both sides of
3 × □ + 2 = □ + 10. Do they match?

</details>

{{include: setup/zen-calm-check.md}}

## Your rule, in your words

Before you read our version, say how to find the box in an equation
like 2 × □ + 1 = 9. Write it in the Notes panel or on paper, or say it
aloud.

<details class="dl-answer"><summary>one way to say it</summary>

An equation is a level balance. Whatever we do to one side, we do to
the other side, and it stays level. To get the box on its own, we undo
the steps that built it. We undo them one at a time, in the opposite
order: the last step first. Taking away undoes adding, and dividing
undoes multiplying. Then we put the answer back in, and check that
both sides match. Your way of saying it may be clearer than ours.

</details>

## Make your own

Can you make five equations of your own, and solve each one by keeping
it level? Here are some ideas:

- a box and some beads
- a few boxes the same, and no loose beads
- a few boxes and some loose beads
- boxes on both pans
- one that you build first: choose the number in the box, then build
  the other side from it

Check each answer by putting it back in.

## Looking back

Why must we do the same to both sides? What happened on this page when
we did something to one side only?

A challenge: the page [Rules with letters in them: expressions,
equations and identities](tutorial:rules-with-letters-in-them#a-rule-a-question-and-a-promise)
has a photo gallery on a web page. Its rows are 50 pixels tall, and
its header is 30 pixels tall. It asks how many rows make exactly 280
pixels:

$$50 \times \text{rows} + 30 = 280$$

Can you find the rows by keeping it level? The program below checks a
guess. Change it to check your answer.

```python challenge
# The photo gallery: 50 × rows + 30 = 280.
# Undo the steps in the opposite order. Then check your answer here.
rows = 1
print(50 * rows + 30)
print(50 * rows + 30 == 280)
```

## Read more

The page [Running a formula backwards: rearranging and
inverses](tutorial:running-a-formula-backwards#the-same-move-on-both-sides)
uses these moves on formulas about light and space. Its section
[Undoing, in reverse
order](tutorial:running-a-formula-backwards#undoing-in-reverse-order)
undoes a temperature formula, one step at a time, in the opposite
order.

Wikipedia's page on [equations](https://en.wikipedia.org/wiki/Equation)
compares an equation to a scale with grain in its pans. It says that
if we take grain from one pan, we must take the same amount from the
other pan.
