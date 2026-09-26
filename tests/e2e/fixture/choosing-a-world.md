---
title: "Choosing a world"
year: "2026-2027"
version: 2026.09.26.1
worlds:
  planets: The planets of the solar system, measured by NASA.
  pixels: Pixel art on a grid three squares wide.
---

# Choosing a world

A cell every world shares.

```python exec
id: world-start
start = 10
print(start)
```

<div class="dl-world" data-world="planets">

How wide are the two largest planets, side by side?

```python exec
id: world-task--planets
widths = [142984, 120536]
print(sum(widths))
```

```predict
type: number

What will the last line print?
```

</div>

<div class="dl-world" data-world="pixels">

How many pixels are lit?

```python exec
id: world-task--pixels
sprite = ["#.#", ".#."]
print(sum(row.count("#") for row in sprite))
```

```predict
type: number

What will the last line print?
```

</div>

A cell after the task, shared again.

```python exec
id: world-end
print(start + 1)
```

<div class="dl-world" data-world="planets">

A task written for one world only shows in every world.

```python exec
id: one-world--planets
print("planets")
```

</div>
