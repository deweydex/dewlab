---
title: "Solving Systems — Practice"
slug: solving-systems-practice
practice_for: solving-systems
module: computational-methods
module_title: "Computational Methods"
year: "2026-2027"
series: matrices
version: 2026.08.24.1
---

# Solving Systems — Practice

Every elimination problem here can be checked the same way: substitute your
answer back into the *original* equations, not the row-reduced ones. If it
does not satisfy those, an arithmetic slip happened somewhere in the middle.

## From Equations to a Matrix

**1.** Write $3x - 2y = 5$ and $x + 4y = -3$ as an augmented matrix, then
solve it — by substitution, elimination, or the inverse, whichever you
prefer.

<details class="dl-answer"><summary>answer</summary>

$\left[\begin{array}{cc|c} 3 & -2 & 5 \\ 1 & 4 & -3 \end{array}\right]$,
and the solution is $x = 1$, $y = -1$.

Checking against the originals: $3(1) - 2(-1) = 5$ and $1 + 4(-1) = -3$ —
both correct.

</details>

## Elimination, Start to Finish

```python exec
id: elimination-1
def show(m):
    for row in m:
        print(row)
```

**2.** Solve $x_1 + x_2 + x_3 = 6$, $2x_1 - x_2 + 3x_3 = 11$,
$x_1 + 2x_2 - x_3 = 2$ by Gaussian elimination.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Write the augmented matrix, and clear $x_1$ out of rows 2 and 3 using row
   1, the same way the tutorial cleared it.
2. That leaves a $2\times2$ system in rows 2 and 3, in $x_2$ and $x_3$ only —
   clear $x_2$ out of row 3 using row 2.
3. Row 3 now has one unknown in it. Solve for $x_3$.
4. Work back up: substitute into row 2 for $x_2$, then into row 1 for $x_1$.

**Think about:** the numbers here do not come out to whole numbers. Does
that make the method any less trustworthy?

**Try this next:** substitute your fractional answer back into all three
original equations and confirm each one balances exactly.

</details>

<details class="dl-answer"><summary>answer</summary>

$x_1 = \frac{11}{5} = 2.2$, $x_2 = \frac{6}{5} = 1.2$, $x_3 = \frac{13}{5} = 2.6$.

```python
M = [[1, 1, 1, 6], [2, -1, 3, 11], [1, 2, -1, 2]]
M[1] = [M[1][k] - 2 * M[0][k] for k in range(4)]   # [0, -3, 1, -1]
M[2] = [M[2][k] - 1 * M[0][k] for k in range(4)]   # [0, 1, -2, -4]
M[2] = [3 * v for v in M[2]]                        # [0, 3, -6, -12]
M[2] = [M[2][k] + M[1][k] for k in range(4)]        # [0, 0, -5, -13]
```

Row 3 says $-5x_3 = -13$, so $x_3 = 2.6$. Row 2 says $-3x_2 + x_3 = -1$, so
$x_2 = 1.2$. Row 1 gives $x_1 = 2.2$. Not every system in real use has
whole-number answers, and the method does not care either way — fractions
are just numbers.

</details>

## Types of Solutions

**3.** $\begin{cases} x + 2y = 3 \\ 2x + 4y = 6 \end{cases}$ — solve it, or
say why you cannot.

<details class="dl-answer"><summary>answer</summary>

Infinitely many solutions. The second equation is exactly twice the first —
$2(x + 2y) = 2(3)$ is $2x + 4y = 6$ — so it carries no new information at
all. Any $(x, y)$ satisfying the first equation satisfies the second
automatically, which leaves one equation and two unknowns: a whole line of
solutions, not a single point.

</details>

**4.** $\begin{cases} x + 2y = 3 \\ 2x + 4y = 7 \end{cases}$ — solve it, or
say why you cannot.

<details class="dl-answer"><summary>answer</summary>

No solution. The left-hand sides are proportional exactly as in problem 3 —
but the right-hand sides are not: doubling the first equation's left side
gives $6$, not $7$. Two lines with the same slope and different intercepts
never meet, and that is exactly what "the same equation, twice, disagreeing
about the answer" describes.

</details>

**5.** Without fully solving it, is
$\begin{cases} x - y + z = 2 \\ 2x - 2y + 2z = 5 \end{cases}$ solvable?

<details class="dl-answer"><summary>answer</summary>

No. The second equation's left side is exactly twice the first's, so a
consistent system would need its right side to be $2 \times 2 = 4$ — and it
says $5$ instead. Same shape of contradiction as problem 4, one dimension up.

</details>

## Checking Your Work

**6.** A friend claims $x_1 = 3, x_2 = 1, x_3 = 2$ solves
$x_1 + x_2 + x_3 = 6$, $2x_1 - x_2 + 3x_3 = 11$, $x_1 + 2x_2 - x_3 = 2$.
Are they right?

<details class="dl-answer"><summary>answer</summary>

No. $3 + 1 + 2 = 6$ checks out, but $2(3) - 1 + 3(2) = 6 - 1 + 6 = 11$ also
checks — and $3 + 2(1) - 2 = 3$, not $2$. The third equation fails, so the
claimed answer is wrong, even though it happens to satisfy the first two.

This is worth sitting with: a solution has to satisfy *every* equation, and
checking only some of them — especially the ones that look easiest — is
exactly how a wrong answer gets past a quick check. (The actual solution to
this system is the fractional one from problem 2.)

</details>

**7.** Write your own three-equation, three-unknown system with a whole
number solution, by picking the answer first and working backward. Then
solve it by elimination to confirm.

<details class="dl-answer"><summary>answer</summary>

Pick an answer, say $(2, -1, 3)$, and any three equations it happens to
satisfy — for instance $x + y + z = 4$, $x - y + z = 6$, $2x + y - z = 0$.
Check the pick first: $2 - 1 + 3 = 4$, $2 + 1 + 3 = 6$, $4 - 1 - 3 = 0$ — all
correct by construction, and elimination on the resulting matrix has to
recover $(2, -1, 3)$, because that is the only point where all three
equations agree.

Working backward like this is a genuinely useful trick — it is how a lot of
textbook problems with clean answers get written in the first place.

</details>
