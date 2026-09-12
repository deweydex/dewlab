---
title: "A grid gallery"
slug: a-grid-gallery
module: web
module_title: "Web authoring"
series: several-pages
version: 2026.09.05.1
---

# A grid gallery

Drag the preview narrower. The number of columns drops on its own,
without a single media query in the CSS below.

```html site=gallery
<div class="gallery">
  <div class="tile">1</div>
  <div class="tile">2</div>
  <div class="tile">3</div>
  <div class="tile">4</div>
</div>
```

```css site=gallery
.gallery {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 10px;
}
.tile {
  background: #f6f4f0;
  border: 1px solid #ccc;
  border-radius: 6px;
  padding: 20px;
  text-align: center;
}
```

## Why this happens

`display: grid` turns a container into a grid; `grid-template-columns`
says how many columns it has and how wide each one is.

`repeat(auto-fit, ...)` does not name a fixed number of columns. It fits
as many as the current width allows, adding or removing a column as the
container grows or shrinks.

`minmax(120px, 1fr)` sets each column's range: at least 120 pixels, but
sharing any wider space evenly once every column has that much. Together,
`repeat(auto-fit, minmax(120px, 1fr))` is a grid that resizes itself.

## Your turn

Let's open your fork of `project_wad` and find the `.gallery` rule in
`styles.css`. It already uses this pattern. Try changing `120px` to
`300px`, then check your gallery page at a phone width. Fewer, wider
columns fit, and at a narrow enough width, just one.

## What you have now

A gallery that rearranges its own columns, with nothing written for any
particular screen size.

- **`display: grid`** — turns a container into a grid.
- **`repeat(auto-fit, …)`** — fits as many columns as the current width
  allows.
- **`minmax()`** — a column's smallest and largest allowed size.
