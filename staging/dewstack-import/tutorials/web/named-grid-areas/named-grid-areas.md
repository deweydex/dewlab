---
title: "Named grid areas"
slug: named-grid-areas
module: web
module_title: "Web authoring"
series: first-site
version: 2026.09.05.1
---

# Named grid areas

Grid can lay out a whole page at once: a header, a menu, a main area, a
footer. `grid-template-areas` names each of those areas, so the layout
reads like a small map instead of a row of column numbers.

Drag the preview width slider from narrow to wide. Somewhere along the
way, the menu moves from above the main area to beside it, and the map in
the CSS below is why.

```html site=layout
<div class="page">
  <header class="area-header">Header</header>
  <nav class="area-nav">Menu</nav>
  <main class="area-main">Main</main>
  <footer class="area-footer">Footer</footer>
</div>
```

```css site=layout
.page {
  display: grid;
  grid-template-areas:
    "header"
    "nav"
    "main"
    "footer";
  gap: 8px;
}
.area-header, .area-nav, .area-main, .area-footer {
  padding: 16px;
  background: #f6f4f0;
  border: 1px solid #ccc;
  text-align: center;
  font-family: sans-serif;
}
header { grid-area: header; }
nav { grid-area: nav; }
main { grid-area: main; }
footer { grid-area: footer; }

@media (min-width: 500px) {
  .page {
    grid-template-areas:
      "header header"
      "nav main"
      "footer footer";
    grid-template-columns: 150px 1fr;
  }
}
```

## Why this happens

`grid-template-areas` takes one quoted line per row of the grid. Each word
in that line names an area, and repeating a name across several cells
makes one area span all of them. `grid-area: header` on the `header`
element then says which named area it fills.

The narrow layout has four rows, one area each, so the menu sits above
the main area. The media query redraws the same map for a wider screen:
two columns, with the menu now beside the main area rather than above it.
Nothing about the HTML changes, only which map applies.

## Other properties from the same lesson

Two related properties from this part of the older course are worth
naming, even without a live demo of their own. `order` changes a flex
item's visual position without changing where it sits in the HTML. A
screen reader still follows the HTML order, not the visual one, so a
reordered page can confuse someone who cannot see the new order. Use
`order` carefully for that reason. `auto-fill`, alongside the `auto-fit`
already shown on [a grid gallery](tutorial:a-grid-gallery), fits as many
columns as `auto-fit` does. It keeps any leftover columns empty, though,
rather than letting the existing items grow to fill them.

## Your turn

Let's try adding a third column to the wide layout above, for a
right-hand sidebar. First, give the new area a name in the media query's
map. Then add an element for it in the HTML, and give that element a
matching `grid-area`. Drag the slider wide again once you are done, to
see the new column appear.

## What you have now

A page-sized layout that redraws itself at a chosen width, described as a
map rather than a set of column numbers.

- **`grid-template-areas`** — names each area of a grid as a small map,
  one quoted line per row.
- **`grid-area`** — assigns an element to one of those named areas.
- **`auto-fill`** — fits as many grid columns as `auto-fit`, but leaves
  any spare columns empty instead of growing the existing ones.
- **`order`** — changes a flex item's visual position without changing
  its position in the HTML.
