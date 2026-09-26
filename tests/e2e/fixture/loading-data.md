---
title: "Loading data"
year: "2026-2027"
version: 2026.09.26.1
datasets: [life-expectancy, the-time-machine]
---

# Loading data

A dataset with a live source, and one without.

```python exec
id: load-live
df = await load_csv("life-expectancy.csv")
print(len(df), "rows")
```

```python exec
id: load-saved
book = await load_text("the-time-machine.txt")
print(book.count("Time Traveller") > 0)
```
