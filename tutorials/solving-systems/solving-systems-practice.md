---
title: "Systems of equations: solving them with matrices — Practice"
practice_for: solving-systems
year: "2026-2027"
version: 2026.09.26.1
worlds:
  photos: Photographs, and the filters that change them.
  starships: Starships, and the structures they are built from.
  space-scenes: Stars, planets and the paths they take across the sky.
---

# Systems of equations: solving them with matrices — Practice

Here are problems on elimination, on systems with no single answer, and
three from earlier pages. Your own `eliminate`, `solve` and the
functions from the earlier pages are already loaded. Check every answer
against the original equations, not the ones after the row operations.

## From equations to a matrix

**1.** Write $3x - 2y = 5$ and $x + 4y = -3$ as an augmented matrix.
Then solve the system in whichever way you like: substitution, the
inverse, or elimination.

<details class="dl-answer"><summary>answer</summary>

The augmented matrix is $\left[\begin{array}{cc|c} 3 & -2 & 5 \\ 1 & 4 & -3
\end{array}\right]$, and the solution is $x = 1$, $y = -1$. Check it:
$3(1) - 2(-1) = 5$ and $1 + 4(-1) = -3$. `solve` gives
`[1.0000000000000002, -0.9999999999999998]`, which is the same answer
with rounding in the last decimal place.

</details>

## Elimination, from start to finish

**2.** Solve $x_1 + x_2 + x_3 = 6$, $2x_1 - x_2 + 3x_3 = 11$ and
$x_1 + 2x_2 - x_3 = 2$ by hand. Then check with `solve`.

```python exec
id: systems-by-hand
M = [[1, 1, 1, 6], [2, -1, 3, 11], [1, 2, -1, 2]]
print(solve(M))
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Use row 1 to clear $x_1$ from rows 2 and 3, as on the tutorial page.
2. Rows 2 and 3 are now a system in $x_2$ and $x_3$ only. Use row 2 to
   clear $x_2$ from row 3.
3. Row 3 now has one unknown. Solve for $x_3$.
4. Put $x_3$ into row 2 to find $x_2$. Then put both into row 1 to find
   $x_1$.

**Think about:** the answers are not whole numbers. Does that change
the method?

</details>

<details class="dl-answer"><summary>answer</summary>

$x_1 = \frac{11}{5} = 2.2$, $x_2 = \frac{6}{5} = 1.2$ and
$x_3 = \frac{13}{5} = 2.6$. After the first column, rows 2 and 3 are
$[0, -3, 1, -1]$ and $[0, 1, -2, -4]$. Three times row 3 plus row 2 is
$[0, 0, -5, -13]$, so $x_3 = 2.6$. `solve` prints `2.5999999999999996`
for $x_3$, which is 2.6 with a rounding error. The method is the same
for fractions as for whole numbers.

</details>

**3.** This system starts with a 0 where the staircase needs a number.

$$\begin{cases} 2y + z = 5 \\ x + y + z = 4 \\ 2x + y + 3z = 7 \end{cases}$$

What does `eliminate` do first, and what is the solution?

```python exec
id: systems-needs-a-swap
M = [[0, 2, 1, 5], [1, 1, 1, 4], [2, 1, 3, 7]]
for row in eliminate(M):
    print(row)
```

<details class="dl-answer"><summary>answer</summary>

It swaps the first two rows, because it cannot divide by the 0. The
staircase is `[1, 1, 1, 4]`, `[0.0, 2.0, 1.0, 5.0]` and
`[0.0, 0.0, 1.5, 1.5]`, so $z = 1$, then $y = 2$ and $x = 1$. Swapping
two equations does not change what they say, so the solution is the
same.

</details>

## No single answer

**4.** Run `eliminate` on these two systems. What does the last row say
in each?

$$\begin{cases} x + 2y = 3 \\ 2x + 4y = 6 \end{cases} \qquad
\begin{cases} x + 2y = 3 \\ 2x + 4y = 7 \end{cases}$$

```python exec
id: systems-last-row
print(eliminate([[1, 2, 3], [2, 4, 6]]))
print(eliminate([[1, 2, 3], [2, 4, 7]]))
```

<details class="dl-answer"><summary>answer</summary>

The first ends with `[0.0, 0.0, 0.0]`, which says $0 = 0$. That is
always true and tells us nothing new, so there is one equation for two
unknowns, and infinitely many solutions on the line $x + 2y = 3$.

The second ends with `[0.0, 0.0, 1.0]`, which says $0 = 1$. Nothing
makes that true, so there is no solution. The two lines are parallel.

In both, the coefficients $\begin{bmatrix} 1 & 2 \\ 2 & 4 \end{bmatrix}$
have determinant 0. The right-hand side decides which of the two cases
you get.

</details>

**5.** Can $x - y + z = 2$ and $2x - 2y + 2z = 5$ both be true? Decide
without solving.

<details class="dl-answer"><summary>answer</summary>

No. The second left-hand side is twice the first, so the second
right-hand side would need to be $2 \times 2 = 4$. It is 5. This is the
$0 = 1$ case again, with one more unknown.

</details>

## Checking your work

**6.** A friend says that $x_1 = 3$, $x_2 = 1$ and $x_3 = 2$ solve the
system in problem 2. Does their answer make all three equations true?

<details class="dl-answer"><summary>answer</summary>

It makes two of them true. $3 + 1 + 2 = 6$ and $2(3) - 1 + 3(2) = 11$.
But $3 + 2(1) - 2 = 3$, not 2. An answer has to make every equation
true, and checking only the first two would have missed this.

</details>

**7.** Write a system of three equations in three unknowns with a
whole-number solution. Choose the solution first, then choose the
left-hand sides, and find each right-hand side from your solution.

```python exec
id: systems-your-own
```

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Yours may be different and work too. Choose
$(2, -1, 3)$. The left-hand sides $x + y + z$, $x - y + z$ and
$2x + y - z$ give right-hand sides 4, 6 and 0.
`solve([[1, 1, 1, 4], [1, -1, 1, 6], [2, 1, -1, 0]])` gives
`[2.0, -1.0, 3.0]`. If one left-hand side can be made from the other
two, the determinant is 0, and `solve` raises its `ValueError`.

</details>

## Your world

**8.** A system from the world you chose.

<div class="dl-world" data-world="photos">

A greyscale filter turns every pixel into one grey. Each of red, green
and blue becomes $0.299r + 0.587g + 0.114b$. So all three rows of the
filter are the same. A pixel comes out as grey 120. Can `solve` find
the colour it was?

```python exec
id: systems-world--photos
grey = [0.299, 0.587, 0.114]
M = [grey + [120], grey + [120], grey + [120]]
```

```hint
Try `solve(M)`, then look at `eliminate(M)`.
```

```solution
{{include: setup/matrices/solve.py}}

grey = [0.299, 0.587, 0.114]
M = [grey + [120], grey + [120], grey + [120]]
for row in eliminate(M):
    print(row)
---
The last two rows are all zeros, so this is the $0 = 0$ case.
`solve` raises its `ValueError`. Every colour with
$0.299r + 0.587g + 0.114b = 120$ becomes this grey, and there are
infinitely many of them. That is why no editor can turn a greyscale
photo back into its colours.
```

</div>

<div class="dl-world" data-world="starships">

A cheaper ship has three thrusters, but the second points the same way
as the first and is twice as strong:

- thruster 1: sideways 2, forward 0, spin 1
- thruster 2: sideways 4, forward 0, spin 2
- thruster 3: sideways 0, forward 3, spin 0

Can the pilot get a change of sideways 4, forward 3 and spin 1? And
sideways 4, forward 3 and spin 2?

```python exec
id: systems-world--starships
thrusters = [(2, 0, 1), (4, 0, 2), (0, 3, 0)]
```

```hint
Build the augmented matrix as on the tutorial page, with each thruster
as a column, and look at the last row of `eliminate`.
```

```solution
{{include: setup/matrices/solve.py}}

thrusters = [(2, 0, 1), (4, 0, 2), (0, 3, 0)]
for wanted in ([4, 3, 1], [4, 3, 2]):
    M = [[t[i] for t in thrusters] + [wanted[i]] for i in range(3)]
    print(eliminate(M)[-1])
---
The first ends with `[0.0, 0.0, 0.0, -1.0]`, which says $0 = -1$, so
no firing times work. The second ends with zeros, so infinitely many
do. Thrusters 1 and 2 always give twice as much sideways as spin, so
the ship can only get changes where that holds. Spin 2 fits, and spin 1
does not.
```

</div>

<div class="dl-world" data-world="space-scenes">

Two probes travel in straight lines across a star chart. One follows
$y = 0.5x + 1$, and the other $y = -x + 7$. Where do their paths cross?

```python exec
id: systems-world--space-scenes
```

```hint
Move the $x$ terms to the left: $-0.5x + y = 1$ and $x + y = 7$.
```

```solution
{{include: setup/matrices/solve.py}}

print(solve([[-0.5, 1, 1], [1, 1, 7]]))
---
It prints `[4.0, 3.0]`, so the paths cross at $(4, 3)$. The probes
only meet there if they arrive at the same time. The system says where
the paths cross, not when each probe gets there.
```

</div>

## From earlier

**9.** From *Comprehensions, grids and aliasing*. `eliminate` starts
with `rows = [list(row) for row in M]`. What would change if it started
with `rows = M`?

<details class="dl-answer"><summary>answer</summary>

`rows` and `M` would be two names for one list, so every row operation
would change the caller's `M` too. After
`eliminate([[1, 1, 1, 6], [2, -1, 1, 3], [1, 2, -1, 2]])`, anyone who
kept that list would find it half eliminated. `list(row)` copies each
row, so `M` stays as it was.

</details>

**10.** From *Matrix multiplication*. How can `multiply` check the
answer to problem 2 in one line?

<details class="dl-answer"><summary>answer</summary>

Multiply the coefficients by the answer written as a column:
`multiply([[1, 1, 1], [2, -1, 3], [1, 2, -1]], [[2.2], [1.2], [2.6]])`.
It gives the right-hand sides, 6, 11 and 2, as a column, up to rounding.

</details>

**11.** From *Inverse matrices*. Without solving problem 1, how could
you know it has exactly one solution?

<details class="dl-answer"><summary>answer</summary>

Its coefficients have determinant $3(4) - (-2)(1) = 14$. That is not
0, so the matrix can be undone, and exactly one point lands on
$(5, -3)$.

</details>
