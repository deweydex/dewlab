---
title: "Flexbox first steps"
slug: flexbox-first-steps
module: web
module_title: "Web authoring"
series: first-site
version: 2026.09.04.1
---

# Flexbox first steps

Three cards, side by side. What happens once the screen is too narrow for
all three to fit in one row? Try it below before reading on.

```html site=cards
<div class="row">
  <div class="card">One</div>
  <div class="card">Two</div>
  <div class="card">Three</div>
</div>
```

```css site=cards
.row {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}
.card {
  flex: 1 1 100px;
  padding: 16px;
  border: 1px solid #ccc;
  border-radius: 6px;
  background: #f6f4f0;
  text-align: center;
  font-family: sans-serif;
}
```

Drag the preview width slider down, toward the narrow end. At some point
the third card drops to a line of its own, then the second joins it. Drag
back up, and they return to one row. Nothing you typed changed; only the
width did.

## Why this happens

Setting `display: flex` on `.row` turns it into a flex container. Its
three `div`s become flex items, and by default they line up in a row.

`flex-wrap: wrap` is what lets that row break. Without it, three items
that no longer fit would either shrink to squeeze in or spill past the
edge of the page. With it, an item that has run out of room starts a new
row instead.

The `flex: 1 1 100px` on `.card` decides when that happens. Each card
asks for at least 100 pixels, then grows to share any space left over
once every card has that much. Once the row is too narrow to give all
three their minimum, one moves down.

## Your turn

Let's open your fork of the starter and find `styles.css`. Its
`.cta-buttons` rule already sets `display: flex` and `flex-wrap: wrap`,
on the buttons below the introduction. Try narrowing your browser window
the way you just narrowed the preview above, and watch for the point
where a button drops to its own line. Then try removing `flex-wrap: wrap`
for a moment and narrowing the window again, to see what the row does
without it.

## What you have now

A row that responds to its own width instead of breaking. Three names
for what you just did:

- **Flex container** — the element with `display: flex` on it.
- **Flex item** — one of that container's direct children.
- **`flex-wrap`** — the property that lets items move to a new row
  rather than overflow or squeeze.
