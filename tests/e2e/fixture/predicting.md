---
title: "Guessing before running"
year: "2026-2027"
version: 2026.09.26.1
---

# Guessing before running

## A loop that starts again

```python exec
id: predict-spending
spent = 0
for day in [3, 4, 5]:
    spent = 0
    spent = spent + day
print(spent)
```

```predict
What will the last line print?

- 12
  The total starts once, before the loop, and every day adds to it.
- 5
  This is what you would see if the total started again each time round.
```

```hint
after: unsure
Which lines run every time round the loop?
```

```hint
after: guess differed
title: another way in
Try printing `spent` inside the loop, and watch it change.
```

## A number

```python exec
id: predict-number
print(2 ** 10)
```

```predict
type: number
tolerance: 0

What will it print?
```

## A word

```python exec
id: predict-word
print("sea".upper())
```

```predict
What will it print?
```
