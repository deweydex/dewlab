---
title: "The dot product: multiply in pairs, then add"
year: "2026-2027"
version: 2026.10.22.1
---

# The dot product: multiply in pairs, then add

Take two lists of numbers of the same length. Multiply them in pairs and
add up the products. For `[1, 2, 3]` and `[4, 5, 6]` that is $1 \times 4
+ 2 \times 5 + 3 \times 6 = 32$. This is the **dot product**. It looks
small and it is everywhere: a lot of machine learning is dot products.

This page writes one function, `dot`, and asks what the numbers in the
first list do to the second list. The next page uses it to slide a
window over a picture.

## The function

How would you write the dot product as a function? What should the total
start at? What goes wrong when the lists have different lengths?

```python exec
id: dot-1
toolkit: yes
expect: dot([1, 2, 3], [4, 5, 6]) == 32 and dot([0.5, 0.5], [10, 20]) == 15 and dot([], []) == 0
def dot(first, second):
    """Multiply the two lists in pairs and add up the products."""
    # Inputs: two lists. What must be true about their lengths?
    # Returns: one number. What type is it?
    # What should the total start at?
    ...
```

```python toolkit-reference
for: dot-1
def dot(first, second):
    total = 0
    for index in range(len(first)):
        total = total + first[index] * second[index]
    return total
```

```hint
after: 3 errors
Work out `dot([1, 2], [3, 4])` on paper: $1 \times 3 + 2 \times 4$.
Which line of your function does each multiplication, and where does the
total collect them?
```

```solution
def dot(first, second):
    total = 0
    for index in range(len(first)):
        total = total + first[index] * second[index]
    return total
---
Here is one answer. Yours may be different and work too. The total
starts at 0 because adding 0 changes nothing. `first[index] *
second[index]` multiplies a pair, and the loop visits every position. If
the second list is shorter, `second[index]` runs off the end, and Python
raises an `IndexError`.
```

## What do the weights do?

Before you run the next cell, predict: what does the dot product of `[1,
1, 1]` with `[7, 8, 9]` give? What about `[1, 0, 0]` with the same list,
or `[0.5, 0.5]` with `[10, 20]`? What do the numbers in the first list
do to the second list?

```python exec
id: dot-2
print(dot([1, 2, 3], [4, 5, 6]))        # 4 + 10 + 18
print(dot([1, 0, 0], [7, 8, 9]))        # a 1 picks out one number
print(dot([1, 1, 1], [7, 8, 9]))        # all 1s add the numbers up
print(dot([0.5, 0.5], [10, 20]))        # weights that add to 1 give an average
```

```predict
type: number

What is the last number the cell prints? It is the dot product of `[0.5,
0.5]` with `[10, 20]`.
```

```predict
type: choice

What does the dot product of `[1, 0, 0]` with `[7, 8, 9]` give?

- 0
  - Zeros are in the list, so everything is cancelled.
- 7
  - A 1 picks out one number, and the 0s remove the rest.
- 24
```

The first list is a set of **weights**. With weights of 1 the dot
product adds the numbers up. With weights that add to 1 it takes an
average. With a single 1 it picks out one number. A dot product is a
weighted sum, and the weights decide what it finds.

## Looking back

Which weights would make the dot product the average of five numbers?
Which would make it the difference between the last number and the
first?

A challenge: write a function that gives the average of a list by using
`dot` and a list of weights that you build from the length of the list.

```python challenge
# An average, using dot.
numbers = [4, 8, 6, 2]
```

## Where to read more

Grant Sanderson (3Blue1Brown) (2016). *Essence of Linear Algebra,
Chapter 9: Dot products and duality.*
<https://www.youtube.com/watch?v=LyGKycYT2v0>. A picture of why
multiplying in pairs and adding is a natural thing to do.
