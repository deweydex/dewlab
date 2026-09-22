---
title: "Cards in a row"
year: "2026-2027"
version: 2026.09.11.1
covers:
  why-does-this-happen:
    touches: [WA-LO9]
  now-in-your-own-site:
    touches: [WA-LO9]
---

# Cards in a row

In [Lining boxes up in a row with Flexbox](tutorial:flexbox-first-steps) we met
`flex: 1 1 80px`. What does each of its three parts do? On this page we
change them, then use them on your own cards.

## Let's try it

Here is a row of three cards, and the CSS that lays them out.

```html site
id: cards-html
site: cards
<div class="row">
  <div class="card">One</div>
  <div class="card">Two</div>
  <div class="card">Three</div>
</div>
```

```css site
id: cards-css
site: cards
.row { display: flex; flex-wrap: wrap; gap: 12px; }
.card {
  flex: 1 1 90px;
  padding: 16px;
  border: 1px solid #ccc;
  border-radius: 6px;
  background: #f6f4f0;
}
```

1. Change `flex: 1 1 90px` to `flex: 0 0 90px`. What happens to the
   cards? Where does the spare width go?
2. Put it back to `1 1 90px`. Now change `90px` to `200px`, and drag
   the width slider toward the narrow end. Do the cards move to new rows
   sooner or later than before?

## Why does this happen?

`flex` holds three values in one line: *flex-grow*, *flex-shrink* and
*flex-basis*, in that order.

- *flex-basis* is an item's starting size, before any growing or
  shrinking. Here it is 90 pixels of content, with the padding and
  border added outside it.
- *flex-grow* decides whether an item takes a share of the space left
  over once every item has its basis. `0` means "stay at the basis
  size". `1` means "share it evenly". An item with `2` takes twice the
  share of an item with `1`.
- *flex-shrink* is for when there is too little space. `1` lets an item
  shrink below its basis to fit. `0` holds it at its basis, even if it
  then spills out of the row.

Now we can explain what we saw. With `0 0 90px`, no card grows. Each
card stays at its basis, and the spare width stays empty at the end of
the row. With a basis of `200px`, each card needs more room, so fewer
cards fit on one line, and they wrap sooner.

Here is the same row twice, in a preview a little wider than the cards
need:

![Two rows of the three cards, One, Two and Three, each card labelled "basis 90px". In the top row, flex: 0 0 90px, the cards stay at their basis, and a dashed area at the end of the row is labelled "spare space, left empty". In the bottom row, flex: 1 1 90px, each card has a tinted part added on its right, labelled "+ share". The three shares are equal, and together they fill the same space that was empty in the top row.](spare-space-shared.svg)

## Now in your own site

Your `index.html` has three cards inside `.card-row`. In `styles.css`,
the `.card` rule has `flex: 1 1 200px`. Your stylesheet sets
`box-sizing: border-box`, so those 200 pixels include padding and
border.

1. In `styles.css`, change the `.card` rule to `flex: 0 0 200px`.
2. Save, and refresh the home page. Where does the spare space go?
3. Change it back to `flex: 1 1 200px`.
4. In `index.html`, give the first card a second class:
   `class="card card-wide"`.
5. In `styles.css`, directly after the `.card` rule, add
   `.card-wide { flex: 2 1 200px; }`. It comes later, so it wins.
6. Save, and refresh.

Does the first card take twice the spare space of each of the other two?

## What we have now

We can now describe a card's width with three separate numbers.

- *flex-grow* decides how big a share of the spare space an item takes.
- *flex-shrink* decides whether an item shrinks below its basis.
- *flex-basis* sets an item's starting size.
