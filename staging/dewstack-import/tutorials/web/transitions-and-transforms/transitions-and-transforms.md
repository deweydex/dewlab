---
title: "Transitions and transforms"
slug: transitions-and-transforms
module: web
module_title: "Web authoring"
series: first-site
version: 2026.09.04.1
---

# Transitions and transforms

Three boxes, three different `transform` values, none of them touching
the boxes next to it.

```html site=transforms
<div class="box move">translateY(-15px)</div>
<div class="box grow">scale(1.2)</div>
<div class="box turn">rotate(8deg)</div>
```

```css site=transforms
.box {
  display: inline-block;
  padding: 12px 16px;
  margin: 10px;
  background: #f6f4f0;
  border: 1px solid #2c3e50;
}
.move { transform: translateY(-15px); }
.grow { transform: scale(1.2); }
.turn { transform: rotate(8deg); }
```

## Why this happens

`transform` changes an element's position, size or shape without moving
anything else around it. `translateY()` shifts it up or down, `scale()`
resizes it, and `rotate()` turns it.

On its own, a transform jumps straight to its new state. `transition`
is what makes a change happen smoothly instead: `transition: transform
0.2s ease;` names the property to animate, how long it takes, and the
curve controlling its pacing. Defined on an element's base rule rather
than on `:hover`, a transition animates a change in both directions,
settling back as smoothly as it arrived.

## Your turn

Let's open your fork and find the `.card:hover` rule you added earlier.
Try `transform: scale(1.05)` instead of `translateY(-5px)`, so the card
grows rather than lifts. Then try changing `0.2s` to `1s` on the base
`.card` rule and hover again, to watch the same animation in slow motion.

## What you have now

Three ways to move an element, and the property that makes any of them
smooth.

- **`transform`** — changes an element's position, size or shape without
  affecting its neighbours.
- **`translateY()`** — shifts an element up or down.
- **`scale()`** — grows or shrinks an element.
