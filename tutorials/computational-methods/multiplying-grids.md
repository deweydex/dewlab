---
title: "Multiplying Grids"
slug: multiplying-grids
module: computational-methods
module_title: "Computational Methods"
year: "2026-2027"
series: matrices
version: 2026.08.24.1
covers:
  the-dot-product-first:
    touches: [CMPS-LO4]
  multiplying-two-grids:
    touches: [CMPS-LO4]
  order-matters:
    touches: [CMPS-LO4]
  the-matrix-that-does-nothing:
    touches: [CMPS-LO4]
---

# Multiplying Grids

Adding two matrices, in *A Grid of Numbers*, turned out to be exactly what
you would guess — pair up the entries and add them. Multiplying two matrices
is not that. Almost nobody guesses the rule for matrix multiplication on the
first try, so today we build it slowly, out of something smaller that you
already know how to do.

## The Dot Product, First

Here are two ordinary Python lists of the same length.

```python exec
id: the-dot-product-first-1
a = [1, 2, 3]
b = [4, 5, 6]

paired = list(zip(a, b))
print(paired)
```

`zip` pairs up the two lists position by position: $1$ with $4$, $2$ with
$5$, $3$ with $6$. Multiply each pair and add up the three results —
$1(4) + 2(5) + 3(6)$ — and you have the *dot product* of `a` and `b`.

### Your turn

Write `dot(a, b)`, returning that single number. A comprehension over
`zip(a, b)` does it in one line, or a loop does it in three.

```python exec
id: the-dot-product-first-2
hint: sum(x * y for x, y in zip(a, b)) — or the loop version of the same idea.
# Your dot(a, b)
```

Try `dot(a, b)` where `a = [1, 2, 3]` and `b = [4, 5]` — one shorter than the
other. What happens?

```python exec
id: the-dot-product-first-3
```

Nothing raises, and that is worth being suspicious of. `zip` quietly stops at
the shorter list, so `dot` silently used only the first two entries of `a`
and ignored the third — no error, no warning, just a wrong-shaped answer that
looks exactly like a right one. Add a check at the top of `dot` — `if len(a) != len(b): raise ValueError(...)` — so that a length
mismatch is loud instead of silent.

```python exec
id: the-dot-product-first-4
hint: One line before the sum — if len(a) != len(b): raise ValueError("lengths do not match").
# Your dot(a, b), with a length check
```

## Multiplying Two Grids

To multiply matrix $A$ by matrix $B$, you take the dot product of every row
of $A$ with every column of $B$. Row $i$, column $j$ of the result is the dot
product of row $i$ of $A$ with column $j$ of $B$.

$$c_{ij} = \sum_{k} a_{ik} \, b_{kj}$$

That is the whole rule. The columns of $B$ are the awkward part to get at in
a plain list of lists — but you already wrote something that turns columns
into rows: `transpose`, from the last tutorial. Each page here starts fresh,
so here it is again, exactly as before.

```python exec
id: multiplying-two-grids-1
def transpose(m):
    rows, cols = len(m), len(m[0])
    return [[m[r][c] for r in range(rows)] for c in range(cols)]
```

### Your turn

Write `multiply(a, b)`, using your own `dot` and `transpose`. For every row
of `a`, and every column of `b` — which is every row of `transpose(b)` — the
entry of the result is `dot(row, column)`.

```python exec
id: multiplying-two-grids-2
hint: [[dot(row, col) for col in transpose(b)] for row in a] — one dot product per position in the result.
# Your multiply(a, b)
```

Try it on these two matrices, and check the shape of what comes back.

```python exec
id: multiplying-two-grids-3
A = [[1, 2], [3, 4]]
B = [[5, 0], [1, -1]]
multiply(A, B)
```

Now try a pair that should not work — $A$ is 2×3 and this $E$ is 2×2, so the
number of columns in $A$ does not match the number of rows in $E$.

```python exec
id: multiplying-two-grids-4
A3 = [[1, 2, 3], [4, 5, 6]]
E = [[1, 0], [0, 1]]
multiply(A3, E)
```

If your `dot` from the last section checks lengths, this raises a
`ValueError` — good, that is the point of having added the check. If it does
not raise anything and instead returns a $2\times2$ result that quietly threw
away the third column of `A3`, that is the exact silent failure from the
dot-product section, one level up. It is worth going back and adding the
check now if you skipped it, because a matrix multiplication that fails
loudly is vastly easier to debug than one that returns a plausible wrong
answer.

The rule this demonstrates: to multiply an $m \times n$ matrix by an
$n \times p$ matrix, the *inner* dimensions — the $n$'s — have to match. The
result is $m \times p$: the outer two numbers, in the order they appeared.

## Order Matters

```python exec
id: order-matters-1
print("AB =", multiply(A, B))
print("BA =", multiply(B, A))
```

`AB` and `BA` are both defined here — both matrices are 2×2 — and they are
not the same matrix. Order genuinely matters for matrix multiplication, which
is not true of multiplying ordinary numbers, and it is one of the first
places the analogy between "multiplication of numbers" and "multiplication
of matrices" breaks down.

### Your turn

Pick any two 2×2 matrices of your own and confirm the same thing — does
`multiply` ever give you the same answer both ways? Try a pair where you
suspect it might, before trying a pair where you are sure it will not.

```python exec
id: order-matters-2
# Two matrices of your own, and both orders of multiply
```

## The Matrix That Does Nothing

Is there a matrix that, multiplied by any other, changes nothing at all —
the matrix equivalent of multiplying a number by 1?

### Your turn

Construct a 3×3 matrix `I3` that you think should have this property, and
test it against some matrix `C` of your choosing: does `multiply(C, I3)`
equal `C`? Does `multiply(I3, C)`?

```python exec
id: the-matrix-that-does-nothing-1
hint: Ones down the main diagonal, zeros everywhere else.
# Your I3, and a C to test it on
```

```python exec
id: the-matrix-that-does-nothing-2
check(multiply(C, I3), C)
```

This matrix is called the *identity matrix*, usually written $I$, and every
square shape has its own: $I_2$, $I_3$, and so on. It comes up constantly —
whenever a formula needs "no change", the identity matrix is what "no
change" looks like for a matrix.

## Reflection

Two tutorials in, and you have built five operations — add, scale, transpose,
dot product, and now full matrix multiplication — out of nothing but nested
Python lists. The multiplication rule in particular is one that almost nobody
finds obvious on first meeting it, and building it out of the dot product,
one row-column pair at a time, is the only way it stops feeling arbitrary.

Was the non-commutativity — `AB` not equal to `BA` — surprising, or did you
expect it once you saw how the rule actually works? What made the connection
between transpose and "getting at the columns of B" click, if it did?

## Where to Read More

Grant Sanderson (3Blue1Brown) (2016). *Essence of Linear Algebra, Chapter 3:
Linear Transformations and Matrices.*
<https://www.youtube.com/watch?v=kYB8IZa5AuE>. Where the row-times-column
rule in this tutorial comes from geometrically — essential watching before
the next tutorial, which is built entirely on this idea.

Ben Eater and Grant Sanderson (2022). *But What Is a Neural Network?*
<https://www.youtube.com/watch?v=aircAruvnKk>. A forward pass through a
network is nothing but the matrix multiplication from this tutorial, applied
over and over.

Strang, G. (2016). *Introduction to Linear Algebra* (5th ed.).
Wellesley-Cambridge Press. The standard textbook treatment, for anyone who
wants the proofs behind why the rule works the way it does.
