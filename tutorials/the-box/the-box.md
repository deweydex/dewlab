---
title: "The box"
year: "2026-2027"
version: 2026.09.11.1
covers:
  why-this-happens:
    covers: [WA-LO9]
  your-turn:
    touches: [WA-LO9]
---

# The box

Here are two plushies from the shop, each sitting in a box of its own.
Let's change `padding` below to `0`, then to `4rem`. Each box changes
size and its border moves with it, but the words inside never move.

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

Now let's try `margin` instead. The boxes stay exactly the same size.
What changes is how far apart they sit, and how far they are from the
edge of the page.

Here is something worth watching for. Set `margin` to `4rem`, and the
gap between the two boxes is `4rem` — not `8rem`. When two margins meet,
they do not add up. The larger of the two sets the gap on its own.

## Why this happens

Every element on a page is a rectangular box, whatever it looks like on
screen. Each box has three layers around its content, from the inside
out.

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

*Padding* is space between the content and the border. It takes on the
box's own background colour, the way the space inside a picture frame
does.

*Border* is the edge of the box. It can be visible, with a colour and a
style, or invisible, with no width at all. `border-radius` rounds its
corners.

*Margin* is space outside the border. It is always transparent, and it
pushes neighbouring boxes away rather than changing this box's own size.

## Your turn

Let's open your fork and find the `.card` rule in `styles.css`. Try
padding of `0`, then `4rem`, then `1rem 3rem` for different
top-and-bottom versus left-and-right spacing. Then find `border-radius`
in the same rule. Try `0` for sharp corners, `20px` for rounded ones,
and `50%` to see what happens to a shape that is not a circle. Once you
have a feel for those, try adding a visible border with
`border: 2px solid var(--accent-color);`.

## What you have now

A box with three layers you can now name and change on purpose.

*Padding* is the space between content and border; it takes the box's
own background colour. *Border* is the box's edge, visible or not.
*Margin* is space outside the border, always transparent.
