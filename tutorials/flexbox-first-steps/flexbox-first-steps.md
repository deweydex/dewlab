---
title: "Lining boxes up in a row with Flexbox"
year: "2026-2027"
version: 2026.09.11.1
covers:
  why-does-this-happen:
    covers: [WA-LO9]
  now-in-your-own-site:
    touches: [WA-LO9]
---

# Lining boxes up in a row with Flexbox

Here are three plushies from the shop, each on its own card, side by
side. What happens once the screen is too narrow for all three cards to
fit in one row? On this page we:

- narrow a row of cards and watch what the row does
- find the exact width where the row changes
- find the same kind of row in your own site

## Let's try it

The HTML puts three cards inside one `.row`. The CSS lays them out.
Try the steps below before reading on.

```html site
id: cards-html
site: cards
<div class="row">
  <div class="card">Squishy Squid</div>
  <div class="card">Cuddly Cuttlefish</div>
  <div class="card">Nautical Nautilus</div>
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

1. Drag the preview's width slider slowly toward the narrow end. What
   happens to the cards?
2. Which card moves first? Which one moves next?
3. Watch the pixel figure beside the slider while you drag. At roughly
   what width does the third card move?
4. Drag back up to the wide end. What do the cards do now? Did any of
   the code change?
5. What happens if we delete `flex-wrap: wrap;` and narrow the preview
   again? Put it back afterwards.

## Why does this happen?

Now we can explain what we saw. As the preview gets narrower, the
nautilus drops to a line of its own, and then the cuttlefish joins it.
When we drag back up, they return to one row. We never changed the
code. Only the width changed.

Three pieces of the CSS work together here.

**`display: flex` on `.row`.** This turns `.row` into a *flex
container*. A flex container is an element with `display: flex` on it.
Its three `div`s become *flex items*. A flex item is one direct child of
a flex container. By default, flex items line up side by side in a row.

**`flex-wrap: wrap` on `.row`.** This lets the row break.
Without it, items that no longer fit shrink to squeeze in, and after
that they spill past the edge of the page. Step 5 showed this.
With `flex-wrap: wrap`, an item that has run out of room starts a new
row.

**`flex: 1 1 80px` on `.card`.** This decides when the row breaks. It
holds three settings in one line:

- the first `1` lets a card grow, to share out any space left over
- the second `1` lets a card shrink, when there is not enough room
- `80px` is the width each card starts from

Each card starts from 80 pixels. Once every card has that much, the
cards grow to share any space left over. When the row is too narrow to
give all three their 80 pixels, one moves down.

### Where the number comes from

So did the third card move at 3 × 80 = 240 pixels? Most people expect
that. The slider shows a larger number.

The 80 pixels is the width of the card's content. It is not the width
of the whole card. The padding and the border sit outside the content,
as [The box model: padding, border and margin](tutorial:the-box)
showed. So each card takes 114 pixels in all. Three of those, with two
12-pixel gaps between them, need 366 pixels. Here is one card at its
real size:

<div class="dl-drawn dl-flexfit" role="img" aria-label="One card drawn at full size: an 80 pixel content box with 16 pixels of padding on each side and a 1 pixel border, 114 pixels in all. Three of those, with two 12 pixel gaps between them, come to 366 pixels — the width below which the third card moves to a row of its own.">
<div class="dl-fx-block">
<div class="dl-fx-card"><div class="dl-fx-content">80</div></div>
<div class="dl-fx-rule"></div>
</div>
<p class="dl-fx-sum">1 + 16 + 80 + 16 + 1 = 114px <span class="dl-fx-said">one card, border and padding included</span></p>
<p class="dl-fx-sum">114 + 12 + 114 + 12 + 114 = 366px <span class="dl-fx-said">three of them, and the two gaps between</span></p>
</div>

The 12-pixel gaps come from `gap: 12px` on `.row`. The `gap` property
sets the space between flex items. It adds no space around the outside
of the row.

Here are the three cards at three widths, with the width of each card:

![The three cards drawn at three widths. At 420 pixels there is room to spare: all three cards sit in one row, and each has grown to 132 pixels. At 366 pixels, three just fit: each card is 114 pixels, its starting width with padding and border, and there is no space left over. At 340 pixels, the row is too narrow for three: the squid and the cuttlefish share the first row at 164 pixels each, and the nautilus moves to a second row, where it grows to the full 340 pixels](flex-row-wraps.svg)

## Now in your own site

1. Open your fork of the starter, and find `styles.css`.
2. Find the `.cta-buttons` rule. It already sets `display: flex` and
   `flex-wrap: wrap`. It lays out the two buttons near the bottom of
   `about.html`, under the heading "Want to See My Work?".
3. Open `about.html` in your browser, and scroll down to those buttons.
   Open the inspector, and switch on device mode, as on [Changing the
   layout for phones: media queries](tutorial:media-queries). A desktop
   window cannot get narrow enough on its own.
4. Drag the page's width from wide to narrow, the way you dragged the
   preview above. Watch for the point where a button drops to its own
   line.
5. Now remove `flex-wrap: wrap` for a moment. Save, and refresh.
6. Narrow the page again. What does the row of buttons do without
   `flex-wrap`?
7. Put `flex-wrap: wrap` back, and save.

Do your buttons stay on the screen at every width now?

## What we have now

We can now build a row that responds to its own width instead of
breaking.

| Word | Meaning | Example |
|---|---|---|
| *flex container* | An element with `display: flex` on it | `.row { display: flex; }` |
| *flex item* | One direct child of a flex container | each `.card` |
| `flex-wrap` | The property that lets flex items move to a new row when they no longer fit, so they do not overflow or squeeze | `flex-wrap: wrap;` |

## Where to Read More

Codepip. *Flexbox Froggy*. <https://flexboxfroggy.com/>. Twenty-four
levels of moving frogs onto lily pads with `justify-content`,
`align-items` and the rest. It goes well past this page. Play it to
learn which flexbox property does what, without reading a reference.
