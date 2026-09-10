---
title: "The container: width and centring"
slug: the-container
module: web
module_title: "Web authoring"
series: first-site
version: 2026.09.04.1
---

# The container: width and centring

Drag the preview wide, then change `max-width` below from `300px` to
`100%`. The white box stops staying a fixed size and starts filling
whatever room it has.

```html site=container
<div class="container">
  <p>Content inside a container.</p>
</div>
```

```css site=container
body { margin: 0; background: #ddd; }
.container {
  max-width: 300px;
  margin: 0 auto;
  background: white;
  padding: 12px;
  border: 1px solid #2c3e50;
}
```

## Why this happens

`max-width` caps how wide an element is allowed to grow, but lets it stay
narrower when there is less room. That is different from `width`, which
sets one fixed size regardless of what is around it.

`margin: 0 auto` sets the top and bottom margin to `0` and the left and
right margin to `auto`. When an element's width is capped, as this one's
is, the two automatic margins split whatever space is left over evenly,
which centres the box.

## Your turn

Let's open your fork and find the `.container` rule in `styles.css`. It
sets `max-width: 1200px` and `margin: 0 auto`. Try `max-width: 600px`,
then `max-width: 100%`, and watch the page's content grow and shrink
between them. Then try removing `margin: 0 auto` for a moment and see
the container line up on the left instead of sitting in the middle.

## What you have now

A box that stays a sensible width and sits in the middle of the page,
however wide the screen is.

- **`max-width`** — the widest an element is allowed to grow.
- **Auto margin** — `margin: 0 auto`, which centres a width-capped
  element by splitting the leftover space evenly.
- **Container** — the element on a page whose width and centring most of
  the rest sits inside.
