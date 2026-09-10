---
title: "Cards in a row"
slug: cards-in-a-row
module: web
module_title: "Web authoring"
series: several-pages
version: 2026.09.05.1
---

# Cards in a row

Try changing `flex: 1 1 200px` below to `flex: 0 0 200px`. The three
cards stop sharing the leftover width evenly; instead each one stays
exactly 200 pixels, with a gap of empty space beside them.

```html site=cards
<div class="row">
  <div class="card">One</div>
  <div class="card">Two</div>
  <div class="card">Three</div>
</div>
```

```css site=cards
.row { display: flex; flex-wrap: wrap; gap: 12px; }
.card {
  flex: 1 1 200px;
  padding: 16px;
  border: 1px solid #ccc;
  border-radius: 6px;
  background: #f6f4f0;
}
```

## Why this happens

`flex` combines three numbers into one line: **flex-grow**,
**flex-shrink**, and **flex-basis**, in that order.

**flex-basis** is a card's starting size, 200 pixels here, before any
growing or shrinking happens.

**flex-grow** decides whether a card claims a share of any space left
over once every card has its basis. `1` means yes, share it evenly with
the other cards; `0` means stay at the basis size and leave the rest
empty.

**flex-shrink** works the other way, for when there is too little space
rather than too much. `1` lets a card shrink below its basis to fit;
`0` holds it at the basis size even if that means overflowing.

## Your turn

Let's open your fork of `project_wad` and find the `.card` rule in
`styles.css`. It already uses `flex: 1 1 200px` on the card row from
your planning page. Try `flex: 0 0 200px` and watch the gap appear.
Then try `flex: 2 1 200px` on just one card, and watch it take twice
the leftover space of the other two.

## What you have now

A row of cards whose width you can now describe in three separate
numbers, not just one setting.

- **flex-grow** — whether an item claims leftover space, and how much
  relative to its neighbours.
- **flex-shrink** — whether an item shrinks below its basis when space
  is short.
- **flex-basis** — an item's starting size, before any growing or
  shrinking.
