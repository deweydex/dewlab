---
title: "Comparing with a solution"
year: "2026-2027"
version: 2026.09.26.1
---

# Comparing with a solution

## A function with a mistake in it

This `total_of` leaves out the last value, on purpose, so the comparison has
something to show.

```python exec
id: compare-total
def total_of(values):
    total = 0
    for value in values[:-1]:
        total = total + value
    return total
```

```inputs
guess: yes
total_of([1, 2, 3])
total_of([])     # an empty list
total_of([5])
```

```solution
def total_of(values):
    return sum(values)
---
Python's own `sum()` does it in one line.
```

```python exec
id: compare-total-tests
tests: compare-total
assert total_of([2, 2]) == 4
total_of([10])
```

## A task with no solution

```python exec
id: compare-own
def double(n):
    return n * 2
```

```inputs
double(4)
```
