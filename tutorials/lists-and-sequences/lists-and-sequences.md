---
title: "Lists: keeping many values in order"
year: "2026-2027"
version: 2026.09.22.1
covers:
  lists-ordered-collections:
    covers: [MIT-6.3]
  building-lists-with-loops:
    covers: [MIT-6.3, MIT-6.7]
  looping-over-lists:
    covers: [MIT-6.5, MIT-6.7]
  mathematical-sequences-as-functions:
    covers: [MIT-6.2]
  the-dot-product-lists-meet-arithmetic:
    covers: [MIT-6.3]
---

# Lists: keeping many values in order

So far, each variable has held one value: one number, or one string. Many
real problems need a group of values. Think of a set of test scores, a
week of temperatures, or the names of everyone in a class.

On this page we:

- keep many values together in a list, and pick out the ones we want
- build lists with a loop, and loop over them
- write functions that work with lists, and turn mathematical sequences
  into code

## Lists: Ordered Collections

A *list* is an ordered sequence of values, written inside square
brackets. Each value in a list is called an element.

```python exec
id: lists-ordered-collections-1
scores = [42, 38, 35, 47, 29, 41, 44, 33, 39, 48]
print(scores)
print("Number of scores:", len(scores))
```

Each element has a position, called its *index*. Python uses
*zero-based indexing*: it starts counting at 0, so the first element is
at index 0.

```python exec
id: lists-ordered-collections-2
print(scores[0])    # first element
print(scores[1])    # second element
print(scores[9])    # tenth (last) element
print(scores[-1])   # also the last element (negative indexing counts from the end)
```

A *slice* is a part of a list. We write it with two indexes and a colon
between them. Before you run the next cell, look at its first line,
`scores[2:5]`. How many scores do you think it prints? Run it to check.

```python exec
id: lists-ordered-collections-3
print(scores[2:5])    # from index 2 up to index 5: how many scores?
print(scores[:3])     # first three elements
print(scores[7:])     # from index 7 to the end
```

That first line surprises nearly everybody. From `2` to `5` looks like
four elements, but we get three. The rule is that the end index is left
out. The rule is easier to remember once we see where the two numbers
point.

In a slice, the two numbers do not point at elements. They point at the
gaps between elements.

![The ten scores in a row. Above each one is its index, 0 to 9. Below, along the boundaries between them, are the eleven cut positions, 0 to 10, offset from the indices above. Underneath, each of the three slices is drawn as a band running between the two cuts it names: 2 to 5 takes 35, 47 and 29; the start-to-3 slice takes 42, 38 and 35; and the 7-to-end slice takes 33, 39 and 48.](where-the-cuts-are.svg)

Ten elements have eleven places where we could cut. A slice names two of
those places and takes everything between them. So `scores[2:5]` means
"cut before 35, cut before 41, and keep the middle". That gives three
elements.

So the end index is not left out by a special rule. A cut is a gap, and
there is nothing in a gap to include.

The picture also shows why `scores[:3]` and `scores[3:]` fit back
together, with nothing missing and nothing repeated. Both slices meet at
the same cut.

We can change what is inside a list after we create it. A value we can
change like this is *mutable*, and lists are mutable.

```python exec
id: lists-ordered-collections-4
scores[0] = 45       # replace the first element
print(scores)

scores.append(50)    # add an element at the end
print(scores)
print("Now we have", len(scores), "scores")
```

### Your turn

1. Create a list called `temperatures`, with at least 7 temperature
   values in it.
2. Print the first temperature and the last temperature.
3. Print the middle three temperatures, using a slice.
4. Change one of the temperatures, and print the updated list.

```python exec
id: your-turn-1
# Your list work here
```

## Building Lists with Loops

A useful way to make a list is to start with an empty list, and then add
values to it one at a time in a loop.

```python exec
id: building-lists-with-loops-1
# Build a list of the first 10 square numbers
squares = []
for i in range(1, 11):
    squares.append(i ** 2)
print(squares)
```

Does this remind you of the accumulator pattern from
[Repeating steps with loops](tutorial:repeating-yourself)? It is the same idea.
There, we added each new value to a running total. Here, we add each new
value to a list.

### Your turn

The Fibonacci sequence starts with 1, 1. After that, each term is the sum
of the two terms before it. So the sequence begins 1, 1, 2, 3, 5, 8,
13, ...

Can you build a list that holds the first 15 terms of the Fibonacci
sequence? Before you write any Python, try writing the steps in
pseudocode, as comments at the top of the cell.

```python exec
id: your-turn-2
# Your Fibonacci list builder
```

## Looping Over Lists

A `for` loop can go through the elements of a list directly, one at a
time.

```python exec
id: looping-over-lists-1
names = ["Ada", "Grace", "Alan", "Margaret"]

for name in names:
    print("Hello, " + name)
```

Sometimes we need both the index and the value. We could loop over
`range(len(names))` and look up each index. Python has a neater way,
`enumerate()`, which gives us the index and the value together.

```python exec
id: looping-over-lists-2
for index, name in enumerate(names):
    print(str(index) + ": " + name)
```

### Your turn: Summing a list

Can you add up all the elements in the `scores` list, using a `for` loop
and the accumulator pattern? Python has a built-in `sum()` function, but
please leave it aside this time, and write the loop yourself.

```python exec
id: your-turn-summing-a-list-1
# Sum the scores using a loop
scores = [42, 38, 35, 47, 29, 41, 44, 33, 39, 48]
```

## Mathematical Sequences as Functions

In mathematics, a *sequence* is a list of numbers made by a rule. The
rule is a function: it takes a position, $n$, and gives back the value
at that position.

For example, the square numbers $1, 4, 9, 16, 25, ...$ come from the
rule $f(n) = n^2$.

The triangular numbers $1, 3, 6, 10, 15, ...$ come from the rule
$f(n) = \frac{n(n+1)}{2}$. This is the same as $\sum_{i=1}^{n} i$, the
sum of the whole numbers from 1 to $n$.

We wrote functions like these in
[Writing your own functions](tutorial:writing-your-own-functions): a
parameter goes in, and `return` sends the answer back. Let's write a
Python function for each of these rules.

```python exec
id: mathematical-sequences-as-functions-1
def square_number(n):
    return n ** 2

def triangular_number(n):
    return n * (n + 1) // 2

# Generate the first 8 terms of each
for i in range(1, 9):
    print("n=" + str(i) + ":  square=" + str(square_number(i)) + 
          "  triangular=" + str(triangular_number(i)))
```

### Your turn

Here, a function takes *another function* as its input. Passing a
function to a function can seem strange at first. It is also a very
useful idea.

1. Write a function `generate_sequence(func, n)`. Its first argument,
   `func`, is a function. Its second argument, `n`, is a whole number.
2. Make it return a list of the first `n` terms of the sequence that
   `func` makes.
3. In the second cell, try it with `square_number` and with
   `triangular_number`.

```python exec
id: your-turn-5
# Your generate_sequence function
```

```python exec
id: your-turn-6
# Test it
# generate_sequence(square_number, 5) should give [1, 4, 9, 16, 25]
```

## The Dot Product: Lists Meet Arithmetic

When two lists have the same length, we can combine them element by
element. The *dot product* of two lists is the sum we get when we
multiply each pair of matching elements and add up the results.

$$\vec{a} \cdot \vec{b} = \sum_{i=0}^{n-1} a_i \times b_i$$

For example, $[1, 2, 3] \cdot [4, 5, 6] = 1 \times 4 + 2 \times 5 + 3 \times 6 = 32$.

The dot product is used everywhere in machine learning, in physics, and
in many other fields.

### Your turn

1. Write a function `dot_product(a, b)` that returns the dot product of
   two lists. You can plan it in pseudocode first, as comments at the top
   of the cell.
2. Think about lists of different lengths. What should your function do
   then? Decide, and make it do that on purpose, so that it does not
   crash with an error you did not plan for.
3. Test it in the second cell.

```python exec
id: your-turn-7
# Your dot_product function
```

```python exec
id: your-turn-8
# Test cases
# dot_product([1, 2, 3], [4, 5, 6]) should be 32
# What should dot_product([1, 2], [3, 4, 5]) return?
```

## Reflection

On this page we met lists. We created them, read elements by index, took
slices, and changed them. We built lists with loops, and we looped over
them. Then we saw how mathematical sequences and the dot product turn
straight into code, as functions that take lists in and give lists or
numbers back.

What links do you see between the ideas from mathematics and the
patterns in the code?

## Where to Read More

Grant Sanderson (3Blue1Brown) (2016). *Essence of Linear Algebra, Chapter 9:
Dot Products and Duality.* <https://www.youtube.com/watch?v=LyGKycYT2v0>.
The dot product this page introduces algebraically, seen geometrically
instead — worth watching before the matrices strand builds on it further.

Python Software Foundation. *The Python Tutorial — Data Structures.*
<https://docs.python.org/3/tutorial/datastructures.html>. The official
reference for everything a list can do, including the methods this page
does not cover.
