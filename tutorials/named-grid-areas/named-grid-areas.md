---
title: "Named grid areas"
year: "2026-2027"
version: 2026.09.11.1
covers:
  why-this-happens:
    covers: [WA-LO9]
  other-properties-from-the-same-lesson:
    touches: [WA-LO9]
  your-turn:
    touches: [WA-LO9]
---

# Named grid areas

Grid can lay out a whole page at once: a header, a menu, a main area, a
footer. `grid-template-areas` names each of those areas, so the layout
reads like a small map instead of a row of column numbers.

Drag the preview width slider from narrow to wide. Somewhere along the
way, the menu moves from above the main area to beside it, and the map in
the CSS below is why.

```html site
id: layout-html
site: layout
<div class="page">
  <header class="area-header">Header</header>
  <nav class="area-nav">Menu</nav>
  <main class="area-main">Main</main>
  <footer class="area-footer">Footer</footer>
</div>
```

```css site
id: layout-css
site: layout
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

@media (min-width: 350px) {
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

<div class="dl-drawn dl-gridmap" role="img" aria-label="The same four areas under two maps, each shown as its quoted lines of grid-template-areas and as the shape those lines make. Under 350 pixels: four quoted lines, so one column and four rows, in the order header, nav, main, footer. At 350 pixels and wider: three quoted lines of two words each, so two columns and three rows, with header spanning both columns on the top row, nav and main side by side on the middle row, and footer spanning both columns on the bottom.">
<div class="dl-gm-case dl-gm-narrow-case">
<p class="dl-gm-when">under 350px</p>
<div class="dl-gm-strings">
<code>"header"</code>
<code>"nav"</code>
<code>"main"</code>
<code>"footer"</code>
</div>
<div class="dl-gm-grid dl-gm-narrow">
<div class="dl-gm-cell dl-gm-header">header</div>
<div class="dl-gm-cell dl-gm-nav dl-gm-moved">nav</div>
<div class="dl-gm-cell dl-gm-main">main</div>
<div class="dl-gm-cell dl-gm-footer">footer</div>
</div>
</div>
<div class="dl-gm-case dl-gm-wide-case">
<p class="dl-gm-when">350px and wider</p>
<div class="dl-gm-strings">
<code>"header header"</code>
<code>"nav main"</code>
<code>"footer footer"</code>
</div>
<div class="dl-gm-grid dl-gm-wide">
<div class="dl-gm-cell dl-gm-header">header</div>
<div class="dl-gm-cell dl-gm-nav dl-gm-moved">nav</div>
<div class="dl-gm-cell dl-gm-main">main</div>
<div class="dl-gm-cell dl-gm-footer">footer</div>
</div>
</div>
</div>

## Other properties from the same lesson

Two related properties are worth naming here, even without a live demo
of their own. `order` changes a flex
item's visual position without changing where it sits in the HTML. A
screen reader still follows the HTML order, not the visual one, so a
reordered page can confuse someone who cannot see the new order. Use
`order` carefully for that reason. `auto-fill` fits as many columns as
`auto-fit` does, but keeps any leftover columns empty rather than
letting the existing items grow to fill them. [A grid
gallery](tutorial:a-grid-gallery), later in this course, covers
`auto-fit` itself.

## Your turn

Let's try adding a third column to the wide layout above, for a
right-hand sidebar. First, give the new area a name in the media query's
map. Then add an element for it in the HTML, and give that element a
matching `grid-area`. Drag the slider wide again once you are done, to
see the new column appear.

## What you have now

A page-sized layout that redraws itself at a chosen width, described as a
map rather than a set of column numbers.

`grid-template-areas` names each area of a grid as a small map, one
quoted line per row. `grid-area` assigns an element to one of those
named areas. `auto-fill` fits as many grid columns as `auto-fit`, but
leaves any spare columns empty instead of growing the existing ones.
`order` changes a flex item's visual position without changing its
position in the HTML.
