---
title: "A grid gallery that chooses its own columns — Practice"
practice_for: a-grid-gallery
year: "2026-2027"
version: 2026.09.22.1
---

# A grid gallery that chooses its own columns — Practice

On this page we practise a grid that chooses its own number of columns:
`grid-template-columns: repeat(auto-fit, minmax(120px, 1fr))`. There are
three kinds of problem:

- a broken page, where we find the mistake and fix it
- a small gallery to build from a description
- a change in your own site, which you commit

Each problem has a folded answer. Some also have a hint, folded before
the answer. Try the problem first, and use the **Preview width** slider
as you go. Many of these mistakes only show at some widths.

## Fix the broken page

**1.** This gallery looks fine in a wide preview. Now drag the
**Preview width** slider all the way to narrow.

```html site
id: gallery-practice-fixed-html
site: gallery-practice-fixed
<div class="gallery">
  <div class="tile">1</div>
  <div class="tile">2</div>
  <div class="tile">3</div>
  <div class="tile">4</div>
</div>
```

```css site
id: gallery-practice-fixed-css
site: gallery-practice-fixed
.gallery {
  display: grid;
  grid-template-columns: repeat(4, 120px);
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

What goes wrong in a narrow preview? Fix it, so that the number of
columns suits the width.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. `repeat(4, 120px)` makes how many columns? Does that number ever
   change?
2. How wide is the grid when it has four columns of `120px` and three
   gaps of `10px`?
3. Which word, inside `repeat()`, lets the browser choose the number of
   columns? Which function lets a column grow and shrink?

**Think about:** a fixed number of fixed-width columns needs a fixed
amount of room. What happens when the room is not there?

**Try this next:** once it works, try `minmax(200px, 1fr)`. At what
width does the gallery drop to one column?

</details>

<details class="dl-answer"><summary>answer</summary>

```css
.gallery {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 10px;
}
```

`repeat(4, 120px)` always makes four columns of `120px`. With the three
gaps, the grid needs `510px`, whatever the width of the preview. In a
narrow preview, the tiles ran past the right-hand edge. With `auto-fit`
and `minmax()`, the browser fits as many columns of at least `120px` as
the width allows, and shares out any spare width between them.

</details>

**2.** This gallery has only two tiles. The author wanted them to fill
the row in a wide preview. Instead, they stay small on the left.

```html site
id: gallery-practice-fill-html
site: gallery-practice-fill
<div class="gallery">
  <div class="tile">1</div>
  <div class="tile">2</div>
</div>
```

```css site
id: gallery-practice-fill-css
site: gallery-practice-fill
.gallery {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
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

Change one word to fix it.

<details class="dl-answer"><summary>answer</summary>

```css
grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
```

In a wide preview there is room for more columns than there are tiles.
`auto-fill` keeps the spare columns, empty, so the two tiles stay in
the first two. `auto-fit` drops the empty columns, and the two tiles
grow to share the whole row. When there are more tiles than fit in one
row, the two words give the same result.

</details>

**3.** In this gallery, every tile sits in one column, however wide the
preview is.

```html site
id: gallery-practice-order-html
site: gallery-practice-order
<div class="gallery">
  <div class="tile">1</div>
  <div class="tile">2</div>
  <div class="tile">3</div>
  <div class="tile">4</div>
</div>
```

```css site
id: gallery-practice-order-css
site: gallery-practice-order
.gallery {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(1fr, 120px));
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

Compare the `minmax()` here with the one in the tutorial. What is
different?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. `minmax()` takes two values. Which one is the smallest size, and
   which is the largest?
2. Can a column's smallest size be "an equal share of the spare
   space"?
3. When a browser does not understand a declaration, it ignores the
   whole line. How many columns does a grid have with no
   `grid-template-columns` at all?

**Think about:** how could the inspector tell us that a line was
ignored?

**Try this next:** once it works, open the inspector on the preview.
Chrome and Firefox show a small **grid** label beside the gallery's
element. What does clicking it draw?

</details>

<details class="dl-answer"><summary>answer</summary>

```css
grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
```

`minmax()` takes the smallest size first, then the largest. Here they
were the wrong way round. A `fr` value is a share of the spare space,
and the browser does not accept it as a smallest size. So it ignored
the whole declaration, and a grid with no column sizes has one column.
The inspector shows an ignored declaration struck through, often with a
small warning sign beside it.

</details>

## Make this

**4.** Build a gallery of six tiles:

- every column at least `150px` wide
- as many columns as fit, sharing out any spare width
- a gap of `16px` between the tiles
- no media query

```html site
id: gallery-practice-six-html
site: gallery-practice-six
<div class="photos">
  <div class="tile">Sea</div>
  <div class="tile">Hill</div>
  <div class="tile">Town</div>
  <div class="tile">Lake</div>
  <div class="tile">Wood</div>
  <div class="tile">Road</div>
</div>
```

```css site
id: gallery-practice-six-css
site: gallery-practice-six
.tile {
  background: #f6f4f0;
  border: 1px solid #ccc;
  border-radius: 6px;
  padding: 20px;
  text-align: center;
}
/* your rules here */
```

At a preview width of about `500px`, how many columns do you get? How
many rows?

<details class="dl-answer"><summary>answer</summary>

```css
.photos {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 16px;
}
```

At about `500px`, three columns of `150px` and two gaps of `16px` need
`482px`, which fits, and a fourth column does not. So there are three
columns, and the six tiles make two rows. In a narrower preview, the
grid drops to two columns and three rows, then to one column.

</details>

## In your own site

**5.** In your fork of `project_wad`, the `.gallery` rule in `styles.css`
has `repeat(auto-fit, minmax(200px, 1fr))`. With the window as wide as
it goes, how many columns can your four images make? Choose a smallest
width so that the gallery shows **exactly three** columns in the widest
window.

1. Open `gallery.html` in your browser, with the window as wide as it
   goes. How many columns are there now?
2. Change `200px` to a value you think gives three columns. Save, and
   refresh.
3. Check it. Then narrow the window, slowly. Does it drop to two
   columns, then one?
4. Commit the change, with a message such as "Three columns in the
   gallery".

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Your `.container` is at most `1000px` wide, and has `1rem` of padding
   on each side. So the gallery is at most `968px` wide.
2. The gallery's gap is `var(--spacing-sm)`, which is `1rem`, or `16px`.
3. Four columns must *not* fit: four columns and three gaps must need
   more than `968px`. Three columns and two gaps must fit in `968px`.

**Think about:** what is the smallest width that stops a fourth column,
and the largest that still lets three fit?

**Try this next:** add two more `<figure>` elements to the gallery, so
it has six. How many rows are there in the widest window?

</details>

<details class="dl-answer"><summary>answer</summary>

With `200px`, four columns and three gaps need `848px`, which fits in
`968px`. So a wide window shows all four images in one row.

For exactly three columns, a fourth must not fit:
`4 × width + 3 × 16px` must be more than `968px`, so the width must be
more than `230px`. Three must still fit: `3 × width + 2 × 16px` must be
no more than `968px`, so the width can be at most `312px`. Any value
from `231px` to `312px` works. `250px` is a tidy choice:

```css
grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
```

</details>
