---
title: "The box model: padding, border and margin"
year: "2026-2027"
version: 2026.09.11.1
covers:
  why-does-this-happen:
    covers: [WA-LO9]
  now-in-your-own-site:
    touches: [WA-LO9]
---

# The box model: padding, border and margin

Every element on a page is a rectangular box, whatever it looks like on
screen. On this page we find the three layers around that box, and learn
to change each one on purpose.

## Let's try it

Here are two plushies from the shop, each sitting in a box of its own.

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

**Padding first.** Let's change `padding` to `0`, then to `4rem`. What
happens to each box? What happens to its border? And do the words inside
move at all?

Each box changes size, and its border moves with it. The words inside
never move.

**Now margin.** With `padding` back at `20px`, what happens when we
change `margin` instead, to `0` and then to `4rem`? Does the box itself change size this time?

The boxes stay exactly the same size. What changes is how far apart they
sit, and how far they are from the edge of the page.

**Something worth watching for.** With `margin` at `4rem`, look at the
gap between the two boxes. The first box has `4rem` of margin
below it, and the second has `4rem` above it. So is the gap `8rem`? Look
closely: it is `4rem`. We will see why below.

## Why does this happen?

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

1. *Padding* is space between the content and the border. It takes on
   the box's own background colour, the way the space inside a picture
   frame does.
2. *Border* is the edge of the box. It can be visible, with a colour and
   a style, or invisible, with no width at all. `border-radius` rounds
   its corners.
3. *Margin* is space outside the border. It is always transparent, and
   it pushes neighbouring boxes away rather than changing this box's own
   size.

Now can we explain what we saw? Padding is inside the border, so more
padding makes the box bigger. Margin is outside the border, so more
margin only moves the boxes apart.

**And the gap that was not `8rem`?** When one box sits above another,
the bottom margin of the first meets the top margin of the second. They
do not add up. The larger of the two sets the gap on its own. This is
called *margin collapse*, and it happens with margins above and below a
box, not with margins at the sides. Here are two margins of different
sizes meeting in one gap:

<div class="dl-drawn dl-collapse" role="img" aria-label="Two boxes, one above the other, with a gap between them. The first box has a bottom margin of 4rem, drawn as a hatched band that fills the whole gap. The second box has a top margin of 2rem, drawn as a shorter hatched band that rises from the second box. The two bands overlap inside the same gap, side by side, instead of sitting end to end. So the gap is 4rem, the larger of the two margins, and not 6rem.">
<div class="dl-mc-box">first box</div>
<div class="dl-mc-gap">
<div class="dl-mc-margin dl-mc-bottom"><span class="dl-mc-label">margin-bottom: 4rem</span></div>
<div class="dl-mc-margin dl-mc-top"><span class="dl-mc-label">margin-top: 2rem</span></div>
</div>
<div class="dl-mc-box">second box</div>
<p class="dl-mc-said">The gap is 4rem, not 6rem.</p>
</div>

## Now in your own site

In your fork, `styles.css` has a `.card` rule. We can try the same
changes there.

1. Set `padding` to `0`, then `4rem`.
2. Now `1rem 3rem`. What changes? With two values, the first sets the
   top and bottom, and the second sets the left and right.
3. The same rule has a `border-radius`. What do `0` and `20px` do to
   the corners?
4. What happens with `50%`, on a shape that is not a circle?
5. Once you have a feel for those, you could add a visible border:
   `border: 2px solid var(--accent-color);`

After each change, save and refresh. Can you name which layer you
changed, just by looking at the result?

## What we have now

Every box has three layers, and we can now name each one and change it
on purpose.

- *Padding* is the space between content and border. It takes the box's
  own background colour.
- *Border* is the box's edge, visible or not.
- *Margin* is space outside the border, always transparent.
- When a bottom margin meets a top margin, the larger one sets the gap.
  This is *margin collapse*.
