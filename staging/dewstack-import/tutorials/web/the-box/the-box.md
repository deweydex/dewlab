---
title: "The box"
slug: the-box
module: web
module_title: "Web authoring"
series: first-site
version: 2026.09.04.1
---

# The box

Try changing `padding` below to `0`, then to `4rem`. The box changes
size and the border moves with it, but the word inside never does.

```html site=box
<div class="box">Content</div>
```

```css site=box
.box {
  background: #f6f4f0;
  padding: 20px;
  border: 4px solid #2c3e50;
  margin: 20px;
  border-radius: 8px;
}
```

Now try changing `margin` instead. The box itself stays the same size,
but it moves away from whatever is around it.

## Why this happens

Every element on a page is a rectangular box, whatever it looks like on
screen. Each box has three layers around its content, from the inside
out.

**Padding** is space between the content and the border. It takes on the
box's own background colour, the way the space inside a picture frame
does.

**Border** is the edge of the box. It can be visible, with a colour and a
style, or invisible, with no width at all. `border-radius` rounds its
corners.

**Margin** is space outside the border. It is always transparent, and it
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

- **Padding** — space between content and border; takes the box's
  background colour.
- **Border** — the box's edge, visible or not.
- **Margin** — space outside the border, always transparent.
