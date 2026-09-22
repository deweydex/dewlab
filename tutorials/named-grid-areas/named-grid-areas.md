---
title: "Named grid areas"
year: "2026-2027"
version: 2026.09.11.1
covers:
  why-does-this-happen:
    covers: [WA-LO9]
  two-related-properties-order-and-auto-fill:
    touches: [WA-LO9]
  now-add-a-sidebar:
    touches: [WA-LO9]
---

# Named grid areas

How could we lay out a whole page at once: a header, a menu, a main
area and a footer? CSS grid can do it. With `grid-template-areas`, we
give each area a name, and the layout reads like a small map instead of
a row of column numbers. On this page we:

- change the width of a page and watch its layout change
- read the map that describes the layout
- meet two related properties, `order` and `auto-fill`
- add a new area to the map ourselves

## Let's try it

The HTML below is a small page with four parts. The CSS places each
part on a grid, and has a second map inside a media query.

```html site
id: layout-html
site: layout
<div class="page">
  <header class="area-header">Tentacular Plushies</header>
  <nav class="area-nav">Squid, Cuttlefish, Nautilus</nav>
  <main class="area-main">Soft things with too many arms.</main>
  <footer class="area-footer">Open all tentacles</footer>
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

1. Look at `grid-template-areas` at the top of the CSS. How many quoted
   lines does it have? How many words are in each line?
2. Drag the preview's width slider to the narrow end. Where does the menu
   (`nav`) sit?
3. Now drag slowly to the wide end. Where does the menu sit now?
4. Watch the pixel figure beside the slider. At what width does the
   layout change? Can you find that number in the CSS?
5. In the media query, what happens if we change `"nav main"` to
   `"main nav"`? Change it back afterwards.

## Why does this happen?

Now we can explain what we saw. At the narrow end, the menu sits above
the main area. Somewhere along the way, it moves beside the main area.
The two maps in the CSS are the reason.

`display: grid` on `.page` makes it a grid. Its children are placed in
rows and columns. `gap: 8px` sets the space between them, the same way
`gap` did for a flex row.

`grid-template-areas` is the map. It works like this:

- It takes one quoted line for each row of the grid.
- Each word in a line names one cell of that row.
- Repeating a name across several cells makes one area span all of
  them. So `"header header"` is one header area, two columns wide.

Then each element needs to know which area it fills. That is the job of
`grid-area`. The rule `header { grid-area: header; }` places the
`header` element in the area named `header`.

Now look at the two maps:

| Map | Rows | Columns | Where the menu sits |
|---|---|---|---|
| `"header"` `"nav"` `"main"` `"footer"` | 4 | 1 | above the main area |
| `"header header"` `"nav main"` `"footer footer"` | 3 | 2 | beside the main area |

The narrow map has four rows, with one area in each. The media query
`@media (min-width: 350px)` swaps in the wide map from 350 pixels up.
That is the number from step 4. The HTML never changes. Only the map
changes.

The wide map also sets `grid-template-columns: 150px 1fr`. This gives
the first column a width of 150 pixels. The unit `fr` means a share of
the space that is left over, so `1fr` gives the second column all the
rest. That is also why, in step 5, the main area was squeezed into 150
pixels: `"main nav"` puts `main` in the first column.

The drawing below shows the same two maps on one grid.

<div class="dl-drawn dl-gridmap-wrap">
<div class="dl-gm-control" hidden>
<label for="dl-gm-width">Map width</label>
<input type="range" id="dl-gm-width" min="170" max="520" step="1" value="260"
       list="dl-gm-ticks" data-dl-width-for="dl-gm-box">
<datalist id="dl-gm-ticks"><option value="350" label="350px"></option></datalist>
<output for="dl-gm-width">260px</output>
</div>
<div class="dl-gridmap" id="dl-gm-box">
<div class="dl-gm-frame">
<div class="dl-gm-strings dl-gm-narrow">
<code>"header"</code>
<code>"nav"</code>
<code>"main"</code>
<code>"footer"</code>
</div>
<div class="dl-gm-strings dl-gm-wide">
<code>"header header"</code>
<code>"nav main"</code>
<code>"footer footer"</code>
</div>
<div class="dl-gm-grid">
<div class="dl-gm-cell dl-gm-header">header</div>
<div class="dl-gm-cell dl-gm-nav dl-gm-moved">nav</div>
<div class="dl-gm-cell dl-gm-main">main</div>
<div class="dl-gm-cell dl-gm-footer">footer</div>
</div>
</div>
</div>
<p class="dl-gm-drag">One grid, under the tutorial's own two maps. Drag the width across
350px: the quoted lines change from four to three, and the shape changes
with them, because the lines are what makes the shape. <code>nav</code>
is marked in both, so you can see where it went.</p>
</div>

Sometimes we might edit a map and find that the whole layout falls
apart. Every quoted line must have the same number of words, and every
named area must make a rectangle. If either rule is broken, the browser
ignores the whole `grid-template-areas` declaration. A dot (`.`) in a
line names an empty cell, which is useful when a line needs a gap.

Chrome and Firefox can also show the grid for us, in the inspector we
met on [The browser inspector](tutorial:the-inspector). Select the
element with `display: grid`, and look for the grid options in the
**Layout** panel.
They draw the grid lines over the page, and can show the area names too.

## Two related properties: order and auto-fill

Two more properties are worth naming here, even without a live demo of
their own.

`order` changes a flex item's position on screen without changing where
it sits in the HTML. It works for grid items too. A screen reader still
follows the HTML order, and so does the Tab key. So a page that has been
reordered on screen can confuse someone who cannot see the new order,
or who moves through the page with a keyboard. For that reason, we use
`order` with care.

`auto-fill` is for a grid of many columns. It fits as many columns as
will hold, and so does `auto-fit`. The difference is in the spare
columns. `auto-fill` keeps any spare columns empty. `auto-fit` lets the
existing items grow to fill the row. [A grid
gallery](tutorial:a-grid-gallery), later in this course, covers
`auto-fit` itself.

## Now add a sidebar

The box above is ours to change. Can we give the wide layout a third
column, for a sidebar on the right?

1. In the media query's map, give the new area a name, such as
   `sidebar`. Each quoted line needs a third word, so that every line
   has the same number of words.
2. In the HTML, add an element for the sidebar, for example a `<div>`
   with the class `area-sidebar`.
3. In the CSS, give that element a matching `grid-area`, the way
   `header`, `nav`, `main` and `footer` have one.
4. You could also add a third width to `grid-template-columns`, such as
   `150px 1fr 150px`.
5. Drag the slider to the wide end again.

Does the new column appear on the right of the main area?

## What we have now

We can now describe a page-sized layout as a map, and make it redraw
itself at a width we choose.

| Word | Meaning | Example |
|---|---|---|
| `grid-template-areas` | Names each area of a grid as a small map, with one quoted line for each row | `"nav main"` |
| `grid-area` | Places an element in one of the named areas | `nav { grid-area: nav; }` |
| `fr` | A share of the space left over in a grid | `grid-template-columns: 150px 1fr;` |
| `auto-fill` | Fits as many grid columns as will hold, and keeps any spare columns empty, instead of growing the existing ones | used with `grid-template-columns` |
| `order` | Changes a flex item's position on screen without changing its position in the HTML | `order: 2;` |

## Where to Read More

Codepip. *Grid Garden*. <https://cssgridgarden.com/>. Twenty-eight levels
of watering carrots with `grid-column`, `grid-row` and `grid-template`.
It works in the column and row numbers this page avoided; having named
the areas first, the numbers underneath them are easier to meet.
