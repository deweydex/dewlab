---
title: "A grid gallery"
year: "2026-2027"
version: 2026.09.11.1
covers:
  why-does-this-happen:
    touches: [WA-LO9]
  now-in-your-own-site:
    touches: [WA-LO9]
---

# A grid gallery

Can a grid choose its own number of columns, to suit the screen? On this
page we try a gallery grid, then change the one in your own site.

## Let's try it

Here is a gallery of four tiles, and its CSS.

```html site
id: gallery-html
site: gallery
<div class="gallery">
  <div class="tile">1</div>
  <div class="tile">2</div>
  <div class="tile">3</div>
  <div class="tile">4</div>
</div>
```

```css site
id: gallery-css
site: gallery
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

1. Drag the width slider slowly toward the narrow end. What happens to
   the number of columns?
2. Look through the CSS. Can you find a media query?

## Why does this happen?

Now we can explain what we saw. The number of columns drops as the
preview gets narrower, and the CSS has no media query at all.

`display: grid` turns `.gallery` into a grid. `grid-template-columns`
says how many columns it has, and how wide each one is. Its value here
has three parts:

- `repeat(...)` repeats one column size many times.
- *auto-fit* means "as many columns as fit". The browser adds or removes
  a column as the container grows or shrinks.
- *minmax()* sets a column's smallest and largest size.
  `minmax(120px, 1fr)` means at least 120 pixels, and an equal share
  (`1fr`) of any wider space.

Together, `repeat(auto-fit, minmax(120px, 1fr))` makes a grid that
resizes itself.

`auto-fit` has a close relative, *auto-fill*. It also fits as many
columns as will hold. The two differ when there is room for more
columns than there are tiles. `auto-fit` lets the four
tiles grow to fill the row. `auto-fill` keeps the spare columns empty.
Here is the difference with two tiles, in a grid with room for four
columns:

![Two grids, each as wide as four columns of at least 120 pixels. The top one uses repeat(auto-fill, minmax(120px, 1fr)): tiles 1 and 2 fill the first two columns, and the other two columns are drawn dashed and labelled "empty column". The bottom one uses repeat(auto-fit, minmax(120px, 1fr)): the empty columns are gone, and tiles 1 and 2 each stretch across half of the row.](auto-fit-and-auto-fill.svg)

## Now in your own site

1. Open your copy of `project_wad`, and find the `.gallery` rule in
   `styles.css`. It already uses this pattern, with `200px`.
2. Change `200px` to `300px`. Save.
3. Open your gallery page, and narrow the window to about a phone's
   width.

Do fewer, wider columns fit now? At what width is there only one?

## What we have now

We now have a gallery that rearranges its own columns, with no CSS
written for any particular screen size.

- `display: grid` turns a container into a grid.
- *auto-fit*, inside `repeat()`, fits as many columns as the width
  allows.
- *minmax()* sets a column's smallest and largest allowed size.
