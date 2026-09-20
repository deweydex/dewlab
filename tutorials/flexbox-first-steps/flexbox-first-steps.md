---
title: "Flexbox first steps"
year: "2026-2027"
version: 2026.09.11.1
covers:
  why-this-happens:
    covers: [WA-LO9]
  your-turn:
    touches: [WA-LO9]
---

# Flexbox first steps

Three cards, side by side. What happens once the screen is too narrow for
all three to fit in one row? Try it below before reading on.

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
body {
  margin: 0;
}
.row {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}
.card {
  flex: 1 1 80px;
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

Watch the pixel figure beside the slider while you drag, and find roughly
where the third card gives up. The rest of this page is about where that
number comes from.

## Why this happens

Setting `display: flex` on `.row` turns it into a flex container. Its
three `div`s become flex items, and by default they line up in a row.

`flex-wrap: wrap` is what lets that row break. Without it, three items
that no longer fit would either shrink to squeeze in or spill past the
edge of the page. With it, an item that has run out of room starts a new
row instead.

The `flex: 1 1 80px` on `.card` decides when that happens. Each card
asks for at least 80 pixels, then grows to share any space left over
once every card has that much. Once the row is too narrow to give all
three their minimum, one moves down.

But 80 pixels is the width of the card's content, not the width of the
card. The padding and the border sit outside it, the way [the
box](tutorial:the-box) showed, so each card takes 114 pixels in all —
and three of those, with two 12-pixel gaps between them, need 366. Here
is one card at its real size:

<div class="dl-drawn dl-flexfit" role="img" aria-label="One card drawn at full size: an 80 pixel content box with 16 pixels of padding on each side and a 1 pixel border, 114 pixels in all. Three of those, with two 12 pixel gaps between them, come to 366 pixels — the width below which the third card moves to a row of its own.">
<div class="dl-fx-block">
<div class="dl-fx-card"><div class="dl-fx-content">80</div></div>
<div class="dl-fx-rule"></div>
</div>
<p class="dl-fx-sum">1 + 16 + 80 + 16 + 1 = 114px <span class="dl-fx-said">one card, border and padding included</span></p>
<p class="dl-fx-sum">114 + 12 + 114 + 12 + 114 = 366px <span class="dl-fx-said">three of them, and the two gaps between</span></p>
</div>

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
for what you just did.

A *flex container* is the element with `display: flex` on it. A *flex
item* is one of that container's direct children. `flex-wrap` is the
property that lets items move to a new row rather than overflow or
squeeze.

## Where to Read More

Codepip. *Flexbox Froggy*. <https://flexboxfroggy.com/>. Twenty-four
levels of moving frogs onto lily pads with `justify-content`,
`align-items` and the rest. It reaches well past this page, and playing
it is the cheapest way to find out which flexbox property does what
without reading a reference.
