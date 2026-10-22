---
title: "A window on a picture: convolution"
year: "2026-2027"
version: 2026.10.22.1
---

# A window on a picture: convolution

A **kernel** is a small canvas of weights, usually 3 by 3. Lay it over a
block of the picture of the same size, multiply each weight by the
square beneath it, and add up the products. That is a dot product, once
the block and the kernel are each laid out as one list. Slide the kernel
over every position of the picture, and the numbers you get make a new
picture. That is a **convolution**.

This page builds the window and the slide from the `dot` of the last
page: `get_patch`, `flatten`, `apply_kernel` and `convolve`.

## A block of the picture

How would you take a block out of a canvas, lay a grid of numbers out as
a single list, and put the two together? A slice, `numbers[2:5]`, takes
the items from position 2 up to but not including position 5.

```python exec
id: get-patch-1
toolkit: yes
expect: get_patch([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 1, 1, 2) == [[5, 6], [8, 9]]
def get_patch(canvas, row, column, size):
    """The size-by-size block of the canvas whose smallest row and column are row and column."""
    # Returns: a block, which is a list of lists. How many rows does it have?
    # How do you take size numbers from one row? (A slice takes the numbers from a up to, not including, b.)
    ...
```

```python toolkit-reference
for: get-patch-1
def get_patch(canvas, row, column, size):
    patch = []
    for r in range(row, row + size):
        patch.append(canvas[r][column:column + size])    # a slice takes size numbers from one row
    return patch
```

```hint
after: 3 errors
Print `get_patch(canvas, 1, 1, 2)` for a small canvas. Is the block 2
rows tall? Does each row have 2 numbers?
```

```solution
def get_patch(canvas, row, column, size):
    patch = []
    for r in range(row, row + size):
        patch.append(canvas[r][column:column + size])    # a slice takes size numbers from one row
    return patch
---
Here is one answer. Yours may be different and work too. `range(row, row
+ size)` visits the rows of the block, and the slice
`canvas[r][column:column + size]` takes `size` numbers from each.
```

```python exec
id: flatten-1
toolkit: yes
expect: flatten([[1, 2], [3, 4]]) == [1, 2, 3, 4] and flatten([]) == []
def flatten(grid):
    """One list holding the numbers of a list of lists, row after row."""
    # What do you start with? What does each row add?
    ...
```

```python toolkit-reference
for: flatten-1
def flatten(grid):
    flat = []
    for row in grid:
        for value in row:
            flat.append(value)
    return flat
```

```hint
after: 3 errors
Work through `flatten([[1, 2], [3, 4]])` by hand. What does the list
hold after the first row, and after the second?
```

```solution
def flatten(grid):
    flat = []
    for row in grid:
        for value in row:
            flat.append(value)
    return flat
---
Here is one answer. Yours may be different and work too. Two loops, one
inside the other, visit every number, and `append` adds it to the end of
one list.
```

```python exec
id: apply-kernel-1
toolkit: yes
expect: apply_kernel([[1, 2, 3], [4, 5, 6], [7, 8, 9]], [[0, 0], [0, 1]], 1, 1) == 9 and apply_kernel([[1, 2, 3], [4, 5, 6], [7, 8, 9]], [[1, 0], [0, 0]], 1, 1) == 5
def apply_kernel(canvas, kernel, row, column):
    """The dot product of the block that starts at (row, column) with the kernel."""
    # How big is the block? Which of your functions does each part of the job?
    ...
```

```python toolkit-reference
for: apply-kernel-1
def apply_kernel(canvas, kernel, row, column):
    patch = get_patch(canvas, row, column, len(kernel))
    return dot(flatten(patch), flatten(kernel))
```

```hint
after: 3 errors
The block has the same size as the kernel, and `len(kernel)` gives it.
Which two lists does `dot` need, and which function turns a block into a
list?
```

```solution
def apply_kernel(canvas, kernel, row, column):
    patch = get_patch(canvas, row, column, len(kernel))
    return dot(flatten(patch), flatten(kernel))
---
Here is one answer. Yours may be different and work too. The block and
the kernel are both grids, so `flatten` makes each one a list, and then
`dot` does the weighted sum. The window starts at `(row, column)` as its
smallest row and column, the same corner convention as `paint_square`.
```

Paint a 3 by 3 square at row 1 and column 1 of a canvas that is 6 by 6,
and make a kernel in which all nine weights are $1/9$. Predict
`apply_kernel` at (0, 0), at (1, 1) and at (3, 3) before you run the
cell. Which position gives 1? Why? A decimal such as $1/9$ is stored
approximately, so a sum can be off by a tiny amount, such as
1.0000000000000002.

```python exec
id: apply-kernel-2
canvas = make_canvas(6, 6)
paint_square(canvas, 1, 1, 3)
average = [[1 / 9, 1 / 9, 1 / 9], [1 / 9, 1 / 9, 1 / 9], [1 / 9, 1 / 9, 1 / 9]]
print(apply_kernel(canvas, average, 0, 0))     # the window starts at a corner of the square
print(apply_kernel(canvas, average, 1, 1))     # the window is full of ink
print(apply_kernel(canvas, average, 3, 3))
```

```predict
type: number
tolerance: 0.01

What is the last number the cell prints, for the window at (3, 3)?
```

## Slide the window

Now slide the kernel over every position of the picture. At each
position, the dot product of the block under the kernel is one number of
a new picture. How big is the new canvas for a kernel of size 3? Why?

```python exec
id: convolve-1
toolkit: yes
expect: convolve([[1, 2, 3], [4, 5, 6], [7, 8, 9]], [[0, 0], [0, 1]]) == [[5, 6], [8, 9]]
def convolve(canvas, kernel):
    """A new canvas, where each square is apply_kernel at that position of the old one."""
    # How many rows and columns does the new canvas have, for a kernel of size 3? For size 5?
    # Which of your functions makes a blank canvas of that size?
    ...
```

```python toolkit-reference
for: convolve-1
def convolve(canvas, kernel):
    size = len(kernel)
    result = make_canvas(len(canvas) - size + 1, len(canvas[0]) - size + 1)
    for row in range(len(result)):
        for column in range(len(result[0])):
            result[row][column] = apply_kernel(canvas, kernel, row, column)
    return result
```

```hint
after: 3 errors
For a canvas of 3 rows and a kernel of size 2, the window can start at
row 0 and row 1, and no later, because it must stay on the canvas. How
many rows does the new canvas have? Does `make_canvas` get that size?
```

```solution
def convolve(canvas, kernel):
    size = len(kernel)
    result = make_canvas(len(canvas) - size + 1, len(canvas[0]) - size + 1)
    for row in range(len(result)):
        for column in range(len(result[0])):
            result[row][column] = apply_kernel(canvas, kernel, row, column)
    return result
---
Here is one answer. Yours may be different and work too. For a kernel of
size $k$, the new canvas has $k - 1$ fewer rows and columns, because the
window must stay on the canvas.
```

A kernel with a 1 in the middle and 0 everywhere else is called the
*identity*. What should a convolution with it do? Paint a 4 by 4 square
on a canvas of 8 by 8, convolve it with the identity kernel, and compare
the sizes of the two canvases. Show both pictures.

```python exec
id: convolve-2
canvas = make_canvas(8, 8)
paint_square(canvas, 2, 2, 4)
identity = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
same = convolve(canvas, identity)
print(len(same), len(same[0]))                  # smaller than the canvas
print(same[0] == canvas[1][1:7])                # the identity kernel keeps the picture, one square in
show_picture(canvas, darkest=1)
show_picture(same, darkest=1)
```

```predict
type: number

What is the last number the cell prints? It is the number of columns of
the new canvas, and a kernel of size 3 takes 2 away.
```

## Looking back

The operation we wrote slides the kernel without flipping it. Most
libraries, and neural networks, call this a convolution as well. A true
convolution flips the kernel first, and the two agree for a symmetric
kernel. Which of the kernels you know are symmetric?

A challenge: write `shrink(canvas)`, which makes a canvas with half as
many rows and columns, where each new square is the average of a 2 by 2
block. Which of your functions can you reuse?

```python challenge
# Half-size pictures. Your toolkit has get_patch, flatten and convolve.
canvas = make_canvas(8, 8)
paint_square(canvas, 2, 2, 4)
```

## Where to read more

Wikipedia. *Kernel (image processing).*
<https://en.wikipedia.org/wiki/Kernel_(image_processing)>. A gallery of
kernels, and what each does to a picture.
