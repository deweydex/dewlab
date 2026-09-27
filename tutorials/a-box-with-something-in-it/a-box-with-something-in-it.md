---
title: "Unknowns: a box with something in it"
year: "2026-2027"
version: 2026.09.27.2
worlds:
  numbers: Normal numbers, like 3 and 10.
  squiggles: Shapes like ♡ and △, which can stand for any number.
  letters: Letters like b and n, which can stand for any number.
---

# Unknowns: a box with something in it

Here is a balance. A balance is a scale for weighing things. It has a
bar, and a pan hangs from each end of the bar. A pan is a small dish.

The left pan holds a closed box, marked ?, and 3 beads. A bead is a
small ball. The right pan holds 7 beads. All the beads weigh the same.
The box itself weighs almost nothing. Only the beads inside it count.

<img src="box-and-three.svg" alt="A balance with its bar level. The left pan holds one closed box, marked with a question mark, and 3 beads. The right pan holds 7 beads.">

```question
id: a-level-bar-1
type: multiple-choice
answer: 1

The bar is level. It is flat, and not tipped to one side. What does
that tell us?

- Both pans hold the same number of beads
  - The beads all weigh the same. A level bar means the two pans weigh
    the same, so they hold the same number of beads.
- The left pan holds more beads
  - A pan with more beads is heavier. The heavier pan goes down, and
    the bar tips.
- The box is empty
  - The left pan has only 3 beads we can see. The right pan has 7. If
    the box were empty, would the bar be level?
```

## Counting what we can see

```question
id: counting-what-we-can-see-1
type: fill-in-the-blank

On the left pan, we can see
{3|7|4}
beads.

On the right pan, we can see
{7|3|10}
beads.
```

We cannot see inside the box. But the bar is level. So the box and its
3 beads weigh the same as 7 beads.

## How many in the box?

```question
id: how-many-in-the-box-1
type: multiple-choice
answer: 2

How many beads are inside the box?

- 7
  - 7 beads are on the right pan. But the left pan has 3 beads outside
    the box too.
- 4
  - 4 in the box and 3 outside make 7, the same as the right pan.
- 10
  - 7 and 3 make 10. With 10 in the box, the left pan would hold 13
    beads.
- 3
  - 3 beads are outside the box. With 3 inside as well, the left pan
    holds 6.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The right pan holds 7 beads.
2. The left pan must hold 7 beads too, because the bar is level.
3. 3 of those 7 beads are outside the box.

**Think about:** how many more beads the 3 outside the box need, to
make 7.

**Try this next:** a box and 2 beads balance 7 beads. How many are in
the box?

</details>

## A guess, and a check

A guess is the first step. Put a number in the box, and count the
left pan again. Does it match the right pan?

```question
id: a-guess-and-a-check-1
type: fill-in-the-blank

Guess 5. Then the left pan holds 5 + 3, which is
{8|7|53}
beads.

That is
{more than 7|less than 7|the same as 7}.

So 5 is
{too many|too few|the number in the box}.
```

```question
id: a-guess-and-a-check-2
type: fill-in-the-blank

Guess 4. Then the left pan holds 4 + 3, which is
{7|8|43}
beads.

The bar is
{level|tipped}.
```

A guess that does not fit is still useful. Here, 5 was too many. So
the next guess is smaller.

## Writing it down

Drawing a balance every time is slow. So we write it with signs. We
write the box as □, and the beads as numbers:

$$\square + 3 = 7$$

The equals sign, =, says the bar is level. The two sides have the same
amount.

```question
id: writing-it-down-1
type: fill-in-the-blank

In □ + 3 = 7, the □ holds
{4|7|10}.

The = sign says both sides have
{the same amount|different amounts|no beads}.
```

## A heart in the box

The box does not have to be a square. We can use any shape. Here is a
heart:

$$\heartsuit + 3 = 7$$

```question
id: a-heart-in-the-box-1
type: fill-in-the-blank

In ♡ + 3 = 7, the ♡ holds
{4|7|3}.
```

The heart holds the same number as the square did. Only the shape of
the box changed.

## A letter in the box

Books usually write a letter in place of the box:

$$x + 3 = 7$$

```question
id: a-letter-in-the-box-1
type: multiple-choice
answer: 1

What is x in x + 3 = 7?

- 4
  - x is a box with a letter on it. It holds 4, as the square and the
    heart did.
- x is not a number
  - A letter can feel strange in a sum. But x is a box, and a box holds
    a number.
- 24
  - x is the 24th letter of the alphabet. In maths, the letter's place
    in the alphabet does not count.
```

A letter is a box. It holds a number we cannot see yet. The box, the
heart and the letter could each hold any number at all. The level bar
tells us which number it is.

{{include: setup/zen-calm-check.md}}

## Try some

Choose numbers, shapes or letters in the list under the title. With
numbers, the box is a ?, as in the picture.

<div class="dl-world" data-world="numbers">

```question
id: try-some-1--numbers
type: fill-in-the-blank

In ? + 6 = 10, the ? holds
{4|16|6}.

In 9 = ? + 2, the ? holds
{7|11|9}.
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: try-some-1--squiggles
type: fill-in-the-blank

In △ + 6 = 10, the △ holds
{4|16|6}.

In 9 = ★ + 2, the ★ holds
{7|11|9}.
```

</div>

<div class="dl-world" data-world="letters">

```question
id: try-some-1--letters
type: fill-in-the-blank

In n + 6 = 10, the n holds
{4|16|6}.

In 9 = b + 2, the b holds
{7|11|9}.
```

</div>

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Draw the balance. Put the box and its beads on one pan.
2. Put the other number of beads on the other pan.
3. In 9 = ? + 2, the box is on the right pan. It does not matter which
   pan the box is on.

**Think about:** how many beads the box needs, so both pans hold the
same number.

**Try this next:** 12 = ? + 5.

</details>

## Names for what we did

Now that we have used the box, here are the usual names.

- The number in the box is called the *unknown*. It is a number we do
  not know yet.
- A sentence like □ + 3 = 7, with an = sign between two sides, is
  called an *equation*.
- To *solve* an equation is to find the number in the box.

```question
id: names-for-what-we-did-1
type: fill-in-the-blank

In n + 6 = 10, the unknown is
{n|6|10}.

To solve n + 6 = 10, we find that n is
{4|16|10}.
```

## Three boxes the same

Now the left pan holds three boxes and no loose beads. The three boxes
have the same sign on them, so they hold the same number of beads. The
right pan holds 12 beads. The bar is level.

<img src="three-boxes.svg" alt="A level balance. The left pan holds three closed boxes, each marked with a question mark. The right pan holds 12 beads.">

$$\square + \square + \square = 12$$

```question
id: three-boxes-the-same-1
type: multiple-choice
answer: 3

How many beads are in each box?

- 12
  - 12 beads are on the right pan. They are shared among three boxes.
- 9
  - 12 − 3 = 9. But there are no loose beads to take away here. The 3
    counts the boxes.
- 4
  - 4 + 4 + 4 = 12. Three boxes of 4 balance 12 beads.
- 36
  - 12 × 3 = 36. That is three pans of 12 beads, not one.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Guess a number for one box. Try 2.
2. All three boxes hold that number. So add it three times: 2 + 2 + 2.
3. Is that 12? If it is too few, guess a bigger number.

**Think about:** why all three boxes must hold the same number.

**Try this next:** □ + □ = 12.

</details>

Three boxes, all the same, is three times one box. So we can write it
with a times sign:

$$3 \times \square = 12$$

## Times a box

<div class="dl-world" data-world="numbers">

```question
id: times-a-box-1--numbers
type: fill-in-the-blank

In 5 × ? = 20, the ? holds
{4|15|100}.

In 2 × ? = 14, the ? holds
{7|12|28}.
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: times-a-box-1--squiggles
type: fill-in-the-blank

In 5 × ♡ = 20, the ♡ holds
{4|15|100}.

In 2 × △ = 14, the △ holds
{7|12|28}.
```

</div>

<div class="dl-world" data-world="letters">

```question
id: times-a-box-1--letters
type: fill-in-the-blank

In 5 × n = 20, the n holds
{4|15|100}.

In 2 × b = 14, the b holds
{7|12|28}.
```

</div>

Books often write 5 × n as 5n, with no sign between the 5 and the
letter. It means the same: five boxes, each holding n.

## A checking machine

Python is a language for computers. It can check a guess for us.
Python cannot use □ as a name, so the cell uses the word `box`. The
sign `==` asks a question: are the two sides the same? Python answers
`True` or `False`.

```python exec
id: a-checking-machine-1
hint: Put 4 in the box. Is 4 + 3 the same as 7? Make a guess now, or run the cell and see.
box = 4
print(box + 3)
print(box + 3 == 7)
```

```predict
type: choice

Before you run it: what will the last line print?

- True
  - 4 + 3 is 7, so the two sides are the same.
- False
  - The box is a guess, so it can feel as if the check must fail.
- 7
  - The line before it prints 7. This line asks a question about it.
```

The first line prints 7, and the second prints `True`. Now change
`box = 4` to `box = 5`, and run it again. What does the check say now?

## A guessing machine

Guessing one number at a time is slow. This cell guesses every whole
number from 0 to 10, and checks each one. It prints only the guesses
that make the bar level.

```python exec
id: a-guessing-machine-1
hint: Which guesses from 0 to 10 make guess + 3 equal to 7? Make a guess now, or run the cell and see.
for guess in range(0, 11):
    if guess + 3 == 7:
        print("The box holds", guess)
```

```predict
type: choice

Before you run it: what will it print?

- The box holds 4
  - Only one guess makes the two sides the same.
- Eleven lines, one for each guess
  - The cell tries eleven guesses. It prints only when the check says
    yes.
- Nothing at all
  - If no guess fits, nothing prints. Does one fit here?
```

It prints one line, "The box holds 4". Now change the check to
`3 * guess == 12`, and run it again. In Python, `*` means times.

<details class="dl-answer"><summary>What each line does</summary>

- `for guess in range(0, 11):` is a loop. It runs the lines under it
  again and again. The first time, `guess` is 0. Then it is 1, then 2,
  and so on, up to 10.
- `if guess + 3 == 7:` checks one guess.
- `print(...)` runs only when the check says yes.

</details>

## An empty box

This one goes a step past the page.

$$\square + 3 = 3$$

```question
id: an-empty-box-1
type: multiple-choice
answer: 1

What does the box hold?

- 0
  - The 3 loose beads already balance the 3 beads on the right. The box
    holds nothing.
- 3
  - With 3 in the box, the left pan holds 6 beads.
- No number works
  - An empty box can feel like "no answer". But 0 is a number, and
    0 + 3 = 3.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Guess 1. Then the left pan holds 1 + 3 beads. Is that 3?
2. The guess was too many. Is there a smaller whole number to try?
3. Try the smallest whole number of all.

**Think about:** can a box be closed and still hold nothing?

**Try this next:** □ + 10 = 10.

</details>

{{include: setup/zen-calm-check.md}}

## Your rule, in your words

Before you read our version, say what the box means in a sentence like
□ + 3 = 7. How can you find what it holds? Write it in the Notes panel
or on paper, or say it aloud.

<details class="dl-answer"><summary>one way to say it</summary>

A box, a shape or a letter holds a number we cannot see yet. The =
sign says the two sides are level: they have the same amount. So only
one number fits in the box. To find it, guess a number, put it in the
box, and check that both sides match. Your way of saying it may be
clearer than ours.

</details>

## Make your own

Can you make five balance problems of your own? Draw each balance, or
write it with signs. Find what each box holds. Here are some ideas:

- a box and some beads, as on this page
- a heart, or a letter, in place of the box
- the box on the right side of the = sign
- three boxes the same, with no loose beads
- a box that holds 0

## Looking back

On this page, □ + 3 = 7 and x + 3 = 7 had the same answer. What is the
same about them? What is different?

A challenge: the guessing machine below finds the box in box + 3 = 7.
Can you make it find the box in 4 × box + 3 = 31? Can you make an
equation where the machine prints nothing at all? Why does it print
nothing?

```python challenge
# A guessing machine. It tries every whole number from 0 to 20.
for guess in range(0, 21):
    if guess + 3 == 7:
        print("The box holds", guess)
```

## Read more

The next page, [Solving equations: keeping it level](tutorial:keeping-it-level),
finds the box without guessing. After it, the page [Rules with letters
in them: expressions, equations and
identities](tutorial:rules-with-letters-in-them#a-rule-a-question-and-a-promise)
goes further. It asks about photos on a web page, with the equation
$50n + 30 = 280$. The $n$ there is a box, like the ones on this page.

Wikipedia's page on equations has [a picture of a
balance](https://en.wikipedia.org/wiki/Equation#Analogous_illustration)
with letters on its weights. It uses more signs than this page, but
the idea is the same.
