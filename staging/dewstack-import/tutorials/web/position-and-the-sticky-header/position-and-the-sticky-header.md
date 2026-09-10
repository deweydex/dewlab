---
title: "Position, and the sticky header"
slug: position-and-the-sticky-header
module: web
module_title: "Web authoring"
series: first-site
version: 2026.09.04.1
---

# Position, and the sticky header

Scroll the preview below. Everything moves except the dark bar at the
top, which stays exactly where it is.

```html site=sticky
<div class="header">I stay in view</div>
<p>Section one. Scroll to see what happens.</p>
<p>Section two.</p>
<p>Section three.</p>
<p>Section four.</p>
<p>Section five.</p>
```

```css site=sticky
.header {
  position: sticky;
  top: 0;
  background: #2c3e50;
  color: white;
  padding: 10px;
  margin: 0;
}
p { height: 100px; margin: 0; padding: 10px; border-bottom: 1px solid #ccc; }
```

## Why this happens

`position: sticky` with `top: 0` keeps an element in place once scrolling
would otherwise carry it past that point. Until then, it scrolls with
everything else, the same as it would with no `position` set at all.

## And the footer

The page below has almost no content. Yet the dark bar still sits at the
very bottom of the preview, not right under the text.

```html site=footer-push
<p>Just a little content.</p>
<footer>Footer</footer>
```

```css site=footer-push
html, body { height: 100%; margin: 0; }
body { display: flex; flex-direction: column; }
footer {
  margin-top: auto;
  background: #2c3e50;
  color: white;
  padding: 10px;
}
```

`body` here is `display: flex` with `flex-direction: column`, stacking its
children top to bottom. `margin-top: auto` on the footer pulls all the
leftover space above it. However little content comes before the footer,
that pushes the footer itself down to the bottom of the page.

## Your turn

Let's open your fork and find the `header` rule in `styles.css`. It sets
`position: sticky` and `top: 0`. Scroll your page and watch the header
stay in view. Then try changing `position: sticky` to `position: fixed`
and scroll again; look at the content behind the header for a clue about
what changed. Try `position: relative`, the default, and the header
scrolls away with everything else. Set it back to `sticky` when you are
done.

Then find the `footer` rule. It has `margin-top: auto`, which is why the
footer sits at the bottom of your page even when there is little content
above it.

## What you have now

A header that stays put, and a footer that never floats up into empty
space.

- **`position: sticky`** — keeps an element in place once scrolling would
  carry it past a given point.
- **`margin-top: auto`** — on a flex child, pulls the leftover space
  above it, pushing the element itself to the far side.
