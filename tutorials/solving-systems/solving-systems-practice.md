---
title: "Systems of equations: solving them with matrices — Practice"
practice_for: solving-systems
year: "2026-2027"
version: 2026.08.24.1
---

# Systems of equations: solving them with matrices — Practice

You can check every elimination problem on this page in the same way.
Put your answer back into the original equations, not the ones after the
row operations. If your answer does not make those true, there is an
arithmetic mistake somewhere in the middle.

## From equations to a matrix

**1.** Write $3x - 2y = 5$ and $x + 4y = -3$ as an augmented matrix. Then
solve the system. You can use substitution, elimination or the inverse,
whichever you prefer.

<details class="dl-answer"><summary>answer</summary>

$\left[\begin{array}{cc|c} 3 & -2 & 5 \\ 1 & 4 & -3 \end{array}\right]$,
and the solution is $x = 1$, $y = -1$.

Check against the original equations: $3(1) - 2(-1) = 5$ and
$1 + 4(-1) = -3$. Both are correct.

</details>

## Elimination, from start to finish

```python exec
id: elimination-1
def show(m):
    for row in m:
        print(row)
```

**2.** Solve $x_1 + x_2 + x_3 = 6$, $2x_1 - x_2 + 3x_3 = 11$,
$x_1 + 2x_2 - x_3 = 2$ by Gaussian elimination.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Write the augmented matrix.
2. Use row 1 to remove $x_1$ from rows 2 and 3, in the same way as the
   tutorial.
3. Rows 2 and 3 are now a $2\times2$ system, in $x_2$ and $x_3$ only. Use
   row 2 to remove $x_2$ from row 3.
4. Row 3 now has one unknown in it. Solve for $x_3$.
5. Work back up. Put $x_3$ into row 2 to find $x_2$. Then put both into
   row 1 to find $x_1$.

**Think about:** the answers here are not whole numbers. Does that make
the method any less trustworthy?

**Try this next:** put your answer, fractions and all, back into all
three original equations. Does each one balance exactly?

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

Row 3 says $-5x_3 = -13$, so $x_3 = 2.6$. Row 2 says $-3x_2 + x_3 = -1$,
so $x_2 = 1.2$. Row 1 then gives $x_1 = 2.2$.

Many systems in real use do not have whole-number answers. The method
works the same either way. Fractions are numbers too.

</details>

## Types of solutions

**3.** Solve $\begin{cases} x + 2y = 3 \\ 2x + 4y = 6 \end{cases}$, or say
why you cannot.

<details class="dl-answer"><summary>answer</summary>

There are infinitely many solutions. The second equation is exactly
twice the first: $2(x + 2y) = 2(3)$ is $2x + 4y = 6$. So it tells us
nothing new.

Any $(x, y)$ that makes the first equation true makes the second one
true as well. That leaves one equation with two unknowns. The solutions
form a whole line, not a single point.

</details>

**4.** Solve $\begin{cases} x + 2y = 3 \\ 2x + 4y = 7 \end{cases}$, or say
why you cannot.

<details class="dl-answer"><summary>answer</summary>

There is no solution. As in problem 3, the second left-hand side is
twice the first. But the right-hand sides do not follow: doubling the
first equation gives $6$ on the right, not $7$.

In a picture, these are two lines with the same slope that cross the
$y$-axis at different places. Such lines never meet. The two equations
have the same left-hand side, but they disagree about the answer.

</details>

**5.** Can we solve
$\begin{cases} x - y + z = 2 \\ 2x - 2y + 2z = 5 \end{cases}$? Decide
without solving it fully.

<details class="dl-answer"><summary>answer</summary>

No. The left-hand side of the second equation is exactly twice the first
one. So, for the two to agree, the right-hand side would need to be
$2 \times 2 = 4$. It is $5$. This is the same kind of disagreement as
in problem 4, with one more unknown.

</details>

## Checking your work

**6.** A friend says that $x_1 = 3, x_2 = 1, x_3 = 2$ solves
$x_1 + x_2 + x_3 = 6$, $2x_1 - x_2 + 3x_3 = 11$, $x_1 + 2x_2 - x_3 = 2$.
Are they right?

<details class="dl-answer"><summary>answer</summary>

No. The first equation works: $3 + 1 + 2 = 6$. The second works too:
$2(3) - 1 + 3(2) = 6 - 1 + 6 = 11$. But the third gives
$3 + 2(1) - 2 = 3$, not $2$. The third equation fails, so the answer is
wrong, even though it makes the first two true.

A solution has to make every equation true. If you check only some of
them, especially the ones that look easiest, a wrong answer can slip
through. (The real solution to this system is the one with fractions,
from problem 2.)

</details>

**7.** Write your own system of three equations in three unknowns, with a
whole-number solution.

1. Pick the answer first.
2. Work backwards to write three equations that it makes true.
3. Solve your system by elimination, to confirm it.

<details class="dl-answer"><summary>answer</summary>

Pick an answer, say $(2, -1, 3)$. Then choose left-hand sides, and work
out each right-hand side from your answer. For example:
$x + y + z = 4$, $x - y + z = 6$ and $2x + y - z = 0$.

Check them first: $2 - 1 + 3 = 4$, $2 + 1 + 3 = 6$ and $4 - 1 - 3 = 0$.
All three are true, because we built them that way. Elimination on this
system gives back $(2, -1, 3)$, because that is the only point where all
three equations agree.

Be careful when you choose the left-hand sides. If one equation is a
multiple of another, or the sum of multiples of the other two, you get
the problem from problem 3: infinitely many solutions, and elimination
cannot find a single answer. In the example above, no left-hand side
can be made from the other two, so the system is safe.

Working backwards like this is useful. Many textbook problems with tidy
answers are written in this way.

</details>
