---
title: "The box"
year: "2026-2027"
version: 2026.09.11.1
covers:
  how-it-works:
    covers: [WA-LO9]
  in-your-own-site:
    touches: [WA-LO9]
---

# The box

Every element on a web page sits in a rectangular box, whatever shape it
looks like. On this page you learn the three layers around that box:
*padding*, *border* and *margin*. Once you can name them, you can control
the space on your page.

## Try it

Here are two plushies from the shop, each in a box of its own.

```html site
id: box-html
site: box
<div class="box">Squishy Squid</div>
<div class="box">Cuddly Cuttlefish</div>
```

```css site
id: box-css
site: box
.box {
  background: #f6f4f0;
  padding: 20px;
  border: 4px solid #2c3e50;
  margin: 20px;
  border-radius: 8px;
}
```

**Padding.** Change `padding` to `0`, then to `4rem`.
The boxes grow and shrink, and the border moves with them. The space
inside the border has the same background colour as the words.

**Margin.** Put `padding` back to `20px`. Now change `margin` to `0`,
then to `4rem`. The boxes stay the same size. What changes is the space
*around* them: the gap between the two boxes, and the gap to the edge of
the preview.

**A surprise.** With `margin` at `4rem`, look at the gap *between* the
two boxes. The first box has `4rem` of margin below it. The second box
has `4rem` of margin above it. You might expect a gap of `8rem`, but the
gap is only `4rem`.

## How it works

Each box has three layers around its content. From the inside out:

<div class="dl-drawn dl-boxmodel" role="img" aria-label="Four regions, one inside the next. Innermost, a content box outlined with a dashed line. Around it, padding, on the same tinted background as the content. Around that, the border, a thick solid line. Outside the border, the margin, an empty band outlined with a dashed line, with the page showing through it.">
  <div class="dl-bm-margin">
    <span class="dl-bm-tag">margin</span>
    <div class="dl-bm-border">
      <span class="dl-bm-tag dl-bm-tag-line">border</span>
      <div class="dl-bm-padding">
        <span class="dl-bm-tag">padding</span>
        <div class="dl-bm-content">content</div>
      </div>
    </div>
  </div>
</div>

| Layer | Where it is | What it looks like |
|---|---|---|
| *Padding* | Between the content and the border | The box's own background colour |
| *Border* | The edge of the box | Any colour and style, or none at all |
| *Margin* | Outside the border | Always transparent: the page shows through |

Padding makes the box bigger. Margin does not change the box. It pushes
the boxes next to it further away.

`border-radius` rounds the corners of the border.

**About the surprise.** When one box sits above another, the bottom
margin of the first box and the top margin of the second box meet. They
do not add up. The larger of the two margins sets the gap. This is called
*margin collapse*. It only happens to margins above and below a box, not
to margins at the left and right.

## In your own site

Open `styles.css` in your fork and find the `.card` rule.

1. Change its `padding` to `0`, then `4rem`. Then try `1rem 3rem`. With
   two values, the first sets top and bottom and the second sets left and
   right.
2. Find `border-radius` in the same rule. Try `0` for sharp corners and
   `20px` for round ones. Then try `50%`: the card is not a square, so
   it becomes an oval.
3. Add a visible border: `border: 2px solid var(--accent-color);`.

**Check:** after each change, save and refresh. Can you say which layer
you changed by looking at the result?

## Summary

- *Padding* is the space between the content and the border. It has the
  box's background colour and makes the box bigger.
- *Border* is the edge of the box.
- *Margin* is the space outside the border. It is transparent and pushes
  other boxes away.
- When a top margin and a bottom margin meet, the larger one wins. This
  is *margin collapse*.
