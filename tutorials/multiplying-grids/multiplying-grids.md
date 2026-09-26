---
title: "Matrix multiplication: rows times columns"
year: "2026-2027"
version: 2026.09.26.1
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

# Matrix multiplication: rows times columns

In [Matrices: adding, scaling and transposing a grid of
numbers](tutorial:grid-of-numbers), adding two matrices worked the way
you would guess. We paired up the entries and added them.

Multiplying two matrices does not work like that. Almost nobody guesses
the rule for matrix multiplication at the first try. So we will build it
slowly, from something smaller that you already know how to do.

On this page we:

- work out the dot product of two lists
- use the dot product to multiply two matrices
- find out whether the order of multiplication matters
- meet the matrix that changes nothing

## The dot product first

Here are two ordinary Python lists of the same length. What do you think
`zip` does with them? Run the cell to find out.

```python exec
id: the-dot-product-first-1
a = [1, 2, 3]
b = [4, 5, 6]

paired = list(zip(a, b))
print(paired)
```

`zip` pairs up the two lists, position by position: $1$ with $4$, $2$
with $5$, and $3$ with $6$. Each pair is printed in round brackets.

The *dot product* of `a` and `b` is the number we get when we multiply
each pair and then add up the results: $1(4) + 2(5) + 3(6)$. You met
the dot product in
[Lists: keeping many values in order](tutorial:lists-and-sequences).

### Your turn

How might you write `dot(a, b)`, so that it returns that one number?

You can use a loop, in about three lines. Or you can use a comprehension
over `zip(a, b)`, in one line.

```python exec
id: the-dot-product-first-2
hint: sum(x * y for x, y in zip(a, b)) — or the loop version of the same idea.
# Your dot(a, b)
```

Now try `dot(a, b)` with `a = [1, 2, 3]` and `b = [4, 5]`. The second
list is one shorter than the first. What happens?

```python exec
id: the-dot-product-first-3
```

Python raises no error, and that should make us suspicious. `zip` stops
at the end of the shorter list, without a word. So `dot` used only the
first two entries of `a` and ignored the third. There is no error and no
warning. The answer is wrong, but it looks exactly like a right one.

We can make this mistake loud. What if `dot` checked the lengths first,
with `if len(a) != len(b): raise ValueError(...)`? Write that version
below.

```python exec
id: the-dot-product-first-4
hint: One line before the sum — if len(a) != len(b): raise ValueError("lengths do not match").
# Your dot(a, b), with a length check
```

## Multiplying two grids

To multiply matrix $A$ by matrix $B$, we take the dot product of every
row of $A$ with every column of $B$. The entry at row $i$, column $j$ of
the result is the dot product of row $i$ of $A$ with column $j$ of $B$:

$$c_{ij} = \sum_{k} a_{ik} \, b_{kj}$$

![Matrix A times matrix B equals AB. The first row of A is shaded, the
first column of B is shaded, and the entry they produce in the top left of
AB is shaded. Below, the working: one times five plus two times one equals
seven.](row-times-column.svg)

One row and one column make one entry. The shaded row and the shaded
column pair up, term by term. The result goes in the place where that row
and that column meet. Every other entry of the answer is made in the
same way, with a different row and a different column.

The picture also shows why the shapes have to agree. A row and a column
can only pair up term by term if they have the same length.

That is the whole rule. The hard part is getting at the columns of $B$,
because a list of lists stores rows. But you have already written
something that turns columns into rows: `transpose`, from the last page.
No page starts with code from an earlier page, so here it is again,
exactly as before.

```python exec
id: multiplying-two-grids-1
def transpose(m):
    rows, cols = len(m), len(m[0])
    return [[m[r][c] for r in range(rows)] for c in range(cols)]
```

### Your turn

How might you write `multiply(a, b)`, with your own `dot` and
`transpose`?

1. Go through every row of `a`.
2. For each row, go through every column of `b`. The columns of `b` are
   the rows of `transpose(b)`.
3. The entry of the result for that row and column is `dot(row, column)`.

```python exec
id: multiplying-two-grids-2
hint: [[dot(row, col) for col in transpose(b)] for row in a] — one dot product per position in the result.
# Your multiply(a, b)
```

Try it on these two matrices. What shape is the result?

```python exec
id: multiplying-two-grids-3
A = [[1, 2], [3, 4]]
B = [[5, 0], [1, -1]]
multiply(A, B)
```

Now try a pair that should not work. `A3` is 2×3 and `E` is 2×2. The
number of columns in `A3` (3) does not match the number of rows in `E`
(2).

```python exec
id: multiplying-two-grids-4
A3 = [[1, 2, 3], [4, 5, 6]]
E = [[1, 0], [0, 1]]
multiply(A3, E)
```

What happened for you?

- If your `dot` checks the lengths, this raises a `ValueError`. Good:
  that is why we added the check.
- If your `dot` has no check, you get a 2×2 result, and the third column
  of `A3` has been thrown away without a word. This is the same silent
  mistake as in the dot-product section, one level up.

If you skipped the check, it is worth going back to add it now. A matrix
multiplication that fails loudly is much easier to fix than one that
gives a wrong answer that looks right.

This gives us the shape rule. To multiply an $m \times n$ matrix by an
$n \times p$ matrix, the inner numbers (the two $n$'s) have to match.
The result is $m \times p$: the two outer numbers, in the same order.

## Order matters

With ordinary numbers, $3 \times 5$ is the same as $5 \times 3$. Is
`multiply(A, B)` the same as `multiply(B, A)`? Make a guess, then run
the cell.

```python exec
id: order-matters-1
print("AB =", multiply(A, B))
print("BA =", multiply(B, A))
```

Both `A` and `B` are 2×2, so `AB` and `BA` both exist. But they are
different matrices. For matrix multiplication, the order matters. This
is one of the first places where multiplying matrices stops behaving
like multiplying numbers.

### Your turn

1. Pick any two 2×2 matrices of your own.
2. Multiply them in both orders. Does `multiply` ever give you the same
   answer both ways?
3. Try a pair where you think it might, before a pair where you are sure
   it will not.

```python exec
id: order-matters-2
# Two matrices of your own, and both orders of multiply
```

## The matrix that does nothing

When we multiply a number by 1, nothing changes. Is there a matrix that
does the same? When we multiply any matrix by it, does anything change?

### Your turn

1. Which 3×3 matrix `I3` do you think has this property? Build it in the
   first cell.
2. Choose a matrix `C` to test it on.
3. Does `multiply(C, I3)` equal `C`? Does `multiply(I3, C)`?

```python exec
id: the-matrix-that-does-nothing-1
hint: Ones down the main diagonal, zeros everywhere else.
# Your I3, and a C to test it on
```

```python exec
id: the-matrix-that-does-nothing-2
print(multiply(C, I3))
print(multiply(I3, C))
print(C)
```

This matrix is called the *identity matrix*. The identity matrix is a
square matrix with ones down its main diagonal and zeros everywhere
else. It is usually written $I$. Every square size has its own identity
matrix: $I_2$, $I_3$, and so on.

You will see the identity matrix often. Whenever a formula needs "no
change", the identity matrix is what "no change" looks like for a
matrix.

## Reflection

After two pages, you have built five operations from nothing but nested
Python lists: add, scale, transpose, the dot product, and now matrix
multiplication.

Most people do not find the multiplication rule obvious when they first
meet it. Building it from the dot product, one row and one column at a
time, is what makes it start to make sense.

Here are some questions to think about:

- Were you surprised that `AB` is not equal to `BA`? Or did you expect
  it, once you saw how the rule works?
- `transpose` gave us a way to get at the columns of `B`. Did that
  connection make sense to you? What made it clear, if it did?

## Where to Read More

Grant Sanderson (3Blue1Brown) (2016). *Essence of Linear Algebra, Chapter 3:
Linear Transformations and Matrices.*
<https://www.youtube.com/watch?v=kYB8IZa5AuE>. Where the row-times-column
rule in this tutorial comes from geometrically — essential watching before
the next tutorial, which is built entirely on this idea.

Grant Sanderson (3Blue1Brown) (2017). *But What Is a Neural Network? |
Deep Learning, Chapter 1.*
<https://www.youtube.com/watch?v=aircAruvnKk>. A forward pass through a
network is nothing but the matrix multiplication from this tutorial, applied
over and over.

Strang, G. (2016). *Introduction to Linear Algebra* (5th ed.).
Wellesley-Cambridge Press. The standard textbook treatment, for anyone who
wants the proofs behind why the rule works the way it does.
