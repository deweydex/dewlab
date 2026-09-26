---
title: "Mixed problems: running totals"
practice_across:
  - running-totals
  - where-the-total-starts
year: "2026-2027"
version: 2026.09.26.1
---

<!-- TEMPLATE: a mixed set. One per series, drawing on every page in it;
and one per course, cumulative, drawing on every series so far. Both are
listed under `mixed:` in the course file. The problems move between pages
on purpose, and do not say which page each comes from: choosing the tool is
part of the problem (#nothing-taught-once). -->

# Mixed problems: running totals

These problems use everything from this series, in no particular order.
Try each one before you open anything under it.

## 1. How many are wide?

How many of the rocky planets are more than 10,000 km wide? Can you make a
loop that counts them, rather than adds them?

```python exec
id: how-many-are-wide-1
widths = [4879, 12104, 12756, 6792]
```

```inputs
count
```

```solution
count = 0
for width in widths:
    if width > 10000:
        count = count + 1
print(count)
---
A count is a running total that adds 1 instead of the width, and only
sometimes. Two planets, Venus and the Earth, are that wide.
```

## 2. The average planet

What is the average width of the rocky planets? Guess first: nearer 5,000
km or nearer 10,000?

```python exec
id: the-average-planet-1
widths = [4879, 12104, 12756, 6792]
```

```predict
type: number
tolerance: 1000

Roughly, what is the average width?
```

```inputs
total / len(widths)
```

```solution
total = 0
for width in widths:
    total = total + width
print(total / len(widths))
---
The total is 36,531, and there are four planets, so the average is
9,132.75 km.
```

## 3. Two things at once

Can one loop find the total *and* the widest planet, going through the list
only once? What should `widest` start at?

```python exec
id: two-things-at-once-1
widths = [4879, 12104, 12756, 6792]
```

```inputs
total
widest
```

```solution
total = 0
widest = widths[0]
for width in widths:
    total = total + width
    if width > widest:
        widest = width
print(total, widest)
---
Starting `widest` at the first width means it always starts as a real
planet. Starting it at 0 works here too, but not for a list of numbers
that are all below 0.
```
