---
title: "Undoing a square: the side of a square — Practice"
practice_for: the-side-of-a-square
year: "2026-2027"
version: 2026.09.27.1
worlds:
  numbers: Ordinary numbers, like 3 and 10.
  squiggles: Shapes like ♡ and △, which can stand for any number.
  letters: Letters like b and n, which can stand for any number.
---

# Undoing a square: the side of a square — Practice

These small problems are about one idea. side(…) starts with a square
of beads, and finds the number of beads along one side. edge(…) does
the same for a cube. Try each problem before you open anything under
it. Some problems come with numbers, shapes or letters. Choose the way
you like in the box under the title.

## 1. A square, or not?

```question
id: a-square-or-not-1
type: fill-in-the-blank

36 beads {make a square|do not make a square}.

40 beads {do not make a square|make a square}.

81 beads {make a square|do not make a square}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Try a square with 6 beads on a side. How many beads is that?
2. For 40, try 6 × 6 and 7 × 7. Is either of them 40?
3. For 81, try 9 × 9.

**Think about:** a square number is a number times itself.

**Try this next:** do 50 beads make a square?

</details>

## 2. Continue the pattern

Here are the square numbers, and the jump from each one to the next.

$$1 \xrightarrow{+3} 4 \xrightarrow{+5} 9 \xrightarrow{+7} 16 \xrightarrow{+9} 25$$

```question
id: continue-the-pattern-1
type: fill-in-the-blank

The next jump is {+11|+10|+9}.

So the next square number is {36|35|34}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Look at the jumps only: 3, 5, 7, 9.
2. How much bigger is each jump than the one before?
3. Add the next jump to 25.

**Think about:** to make the next square, you add one row and one
column of beads, and one bead in the corner.

**Try this next:** what is the jump from 36 to the next square number?

</details>

## 3. Three ways to say it

Here is one idea, said three ways: in beads, in symbols, and the long
way.

<div class="dl-world" data-world="numbers">

```question
id: three-ways-to-say-it-1--numbers
type: fill-in-the-blank

A square with 7 beads on each side has {49|14|28} beads.

In symbols, side({49|14|7}) = 7.

The long way, {7 × 7|7 + 7|7 × 2} = 49.
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: three-ways-to-say-it-1--squiggles
type: fill-in-the-blank

A square with ♡ beads on each side has {♡ × ♡|♡ + ♡|4 × ♡} beads.

In symbols, side({♡ × ♡|♡ + ♡|♡}) = ♡.

The long way, {♡ × ♡|♡ + ♡|♡ × 2} = ♡².
```

</div>

<div class="dl-world" data-world="letters">

```question
id: three-ways-to-say-it-1--letters
type: fill-in-the-blank

A square with k beads on each side has {k × k|k + k|4k} beads.

In symbols, side({k × k|k + k|k}) = k.

The long way, {k × k|k + k|k × 2} = k².
```

</div>

## 4. How much is it?

Only numbers here, since these ask for an amount.

```question
id: how-much-is-it-1
type: fill-in-the-blank

side(81) = {9|40.5|18}

side(144) = {12|72|14}

side(400) = {20|200|40}

side(1) = {1|0.5|0}
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. side(81) asks: which number, times itself, makes 81?
2. Try a number. Multiply it by itself. Too big, or too small?
3. Try a number one bigger or one smaller.

**Think about:** 400 is 4 × 100. What is the side of each?

**Try this next:** side(900).

</details>

You can check with this cell. Change `beads` and run it. It tries
every whole number, and prints any side or edge it finds.

```python exec
id: how-much-is-it-2
beads = 144

for side_length in range(1, beads + 1):
    if side_length * side_length == beads:
        print("side is", side_length)
    if side_length * side_length * side_length == beads:
        print("edge is", side_length)
```

## 5. Where on the line?

side(17) and side(24) are both between 4 and 5. Picture a line from 4
to 5.

```question
id: where-on-the-line-1
type: fill-in-the-blank

side(17) is closer to {4|5}.

side(24) is closer to {5|4}.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. 4 × 4 = 16, and 5 × 5 = 25.
2. Is 17 close to 16, or close to 25?
3. Is 24 close to 16, or close to 25?

**Think about:** a number of beads close to a square number has a side
close to that square's side.

**Try this next:** is side(99) closer to 9 or to 10?

</details>

## 6. What went differently here?

Somebody wanted side(16). They wrote $16 \div 2 = 8$, so side(16) = 8.
What happened?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Draw, or picture, a square with 8 beads on a side.
2. How many beads is that?
3. Is it 16?

**Think about:** halving and finding the side are different jobs.

**Try this next:** is there any number where halving and finding the
side give the same answer?

</details>

<details class="dl-answer"><summary>one way through it</summary>

A square with 8 beads on a side has $8 \times 8 = 64$ beads, not 16.
Dividing by 2 finds half, not the side. side(16) is 4, because
$4 \times 4 = 16$. For 4 beads, the two jobs give the same answer:
side(4) = 2, and half of 4 is 2 too. Here is one answer. Yours
may be different and work too.

</details>

## 7. Two paths, one answer

$36 = 4 \times 9$. Here are two ways to find side(36).

- Path one: $6 \times 6 = 36$, so side(36) = 6.
- Path two: side(4) × side(9) = 2 × 3.

Do the two paths give the same answer?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Find 2 × 3.
2. Compare it with path one.
3. Picture a 6 by 6 square. Can you cut it into 2 by 2 blocks of 9
   beads each?

**Think about:** a square of squares is still a square.

**Try this next:** side(100), with $100 = 4 \times 25$.

</details>

<details class="dl-answer"><summary>one way through it</summary>

Yes. $2 \times 3 = 6$, the same as path one. A 6 by 6 square cuts into
4 blocks, 2 by 2. Each block is a square of 9 beads, 3 by 3. For
side(100): side(4) × side(25) = 2 × 5 = 10, and $10 \times 10 = 100$.

</details>

## 8. Undoing a cube

<div class="dl-world" data-world="numbers">

```question
id: undoing-a-cube-1--numbers
type: fill-in-the-blank

edge(64) = {4|8|16}

edge(125) = {5|25|41}
```

</div>

<div class="dl-world" data-world="squiggles">

```question
id: undoing-a-cube-1--squiggles
type: fill-in-the-blank

edge(★ × ★ × ★) = {★|★ × ★|3 × ★}

edge(△ × △ × △) × edge(△ × △ × △) = {△ × △|△|6 × △}
```

</div>

<div class="dl-world" data-world="letters">

```question
id: undoing-a-cube-1--letters
type: fill-in-the-blank

edge(m × m × m) = {m|m × m|3m}

edge(p × p × p) × edge(p × p × p) = {p × p|p|6p}
```

</div>

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. A cube of beads is the same number wide, high and deep.
2. edge(…) asks how many beads are along one edge.
3. For the second one, find the first edge. Then multiply it by
   itself.

**Think about:** edge(…) undoes a cube, the way side(…) undoes a
square.

**Try this next:** edge(1000 × 1000 × 1000).

</details>

## 9. Looks scary, is simple

<div class="dl-world" data-world="numbers">

What is side(10 × 10 × 10 × 10)?

</div>

<div class="dl-world" data-world="squiggles">

What is side(♡ × ♡ × ♡ × ♡)?

</div>

<div class="dl-world" data-world="letters">

What is side(b × b × b × b)?

</div>

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. side(…) asks: what, times itself, makes this?
2. Split the four in the brackets into two equal groups.
3. Each group is one side.

**Think about:** a group of two, times a group of two, is four.

**Try this next:** side of six of them multiplied together.

</details>

<details class="dl-answer"><summary>one way through it</summary>

Split the four into two groups of two:
$(10 \times 10) \times (10 \times 10)$. So side(10 × 10 × 10 × 10) is
$10 \times 10 = 100$. Check: $100 \times 100 = 10000$, which is
$10 \times 10 \times 10 \times 10$. With shapes it is the same:
side(♡ × ♡ × ♡ × ♡) = ♡ × ♡. With letters, side(b × b × b × b) = b × b,
or $b^2$.

</details>

## 10. A stretch: a square and a cube

1 bead is a square and a cube. So is 64: 8 by 8, and 4 by 4 by 4. There
is one more number like this below 1000. Can you find it? The cell in
problem 4 can help: it prints both a side and an edge when it finds
them.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Write the cubes below 1000: 1, 8, 27, 64, 125, …
2. For each cube, ask: is it also a square number?
3. Use the cell to check each one.

**Think about:** the cubes are further apart than the squares, so there
are fewer to check.

**Try this next:** is there one bigger than 1000?

</details>

<details class="dl-answer"><summary>answer</summary>

729. It is $27 \times 27$, so side(729) = 27. It is also
$9 \times 9 \times 9$, so edge(729) = 9.

</details>

## 11. From earlier: the long way

From *Powers: the long way and the short way*. Write $5^3$ the long
way, and find how much it is. Then find the edge of a cube with that
many beads.

<details class="dl-answer"><summary>answer</summary>

$5^3 = 5 \times 5 \times 5 = 125$, and edge(125) = 5. The edge undoes
the power 3.

</details>

## 12. From earlier: the simplest name

From *Equivalent fractions: the same amount, different names*. What is
the simplest name for $\frac{16}{64}$?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Find a number that divides 16 and 64 with nothing left over.
2. Divide the top and the bottom by it.
3. Look again. Can you divide again?

**Think about:** 16 goes into 64 exactly.

**Try this next:** the simplest name for $\frac{9}{36}$.

</details>

<details class="dl-answer"><summary>answer</summary>

$\frac{1}{4}$: divide the top and the bottom by 16.

</details>

## 13. The usual way to write it

The tutorial showed the signs people usually write. $\sqrt{49}$ is the
*square root* of 49, and means side(49). $\sqrt[3]{27}$ is the *cube
root* of 27, and means edge(27). Use whichever feels calmer.

```question
id: the-usual-way-to-write-it-1
type: fill-in-the-blank

√81 = {9|40.5|18}

√400 = {20|200|40}

∛125 = {5|25|41}
```

## 14. Five of your own

Can you make five problems of your own, and find each answer? Here are
some ideas:

- side(…) of a square number bigger than 10,000
- edge(…) of a cube bigger than 10,000
- a number whose side is between 20 and 21
- side(…) with a shape or a letter in the brackets

Which of your problems looks scary, but is simple?
