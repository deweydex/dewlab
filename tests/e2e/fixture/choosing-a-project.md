---
title: "Choosing a project"
year: "2026-2027"
version: 2026.09.27.1
projects:
  sums:
    title: Adding up
    question: How big does a running total get?
    make: a running total
    maths: repeated addition
    data: the numbers 1 to 10
  squares:
    title: Squaring
    question: How fast do squares grow?
    make: a table of squares
    maths: powers
    data: the numbers 1 to 5
  own:
    title: A project of your own
    question: What would you like to count?
    make: whatever you choose
    maths: your choice
    data: your choice
    own: true
---

# Choosing a project

A shared opening, before the projects.

```python exec
id: shared-opening
print("shared")
```

<div class="dl-project" data-project="sums">

## Adding up

```python exec
id: project-sums-1
total = 0
for n in range(1, 11):
    total = total + n
print("sum is", total)
```

</div>

<div class="dl-project" data-project="squares">

## Squaring

```python exec
id: project-squares-1
print("squares", [n * n for n in range(1, 6)])
```

</div>

<div class="dl-project" data-project="own">

## A project of your own

```python exec
id: project-own-1
# Yours here.
```

</div>

## After the projects

The page goes on.
