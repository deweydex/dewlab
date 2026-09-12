---
title: "Media queries"
slug: media-queries
module: web
module_title: "Web authoring"
series: first-site
version: 2026.09.04.1
---

# Media queries

Drag the preview width slider from wide to narrow. Somewhere along the
way, the message below changes colour, with nothing else on the page
touched.

```html site=media
<p class="msg">Watch me as the preview gets narrower.</p>
```

```css site=media
.msg { background: #f6f4f0; padding: 12px; font-weight: bold; }
@media (max-width: 350px) {
  .msg { background: #d9720c; color: white; }
}
```

## Why this happens

A **media query** wraps a block of CSS in a condition based on the
screen, most often its width. `@media (max-width: 350px) { ... }` applies
the rules inside it only when the screen is 350 pixels wide or narrower.
Outside that condition, the rules inside do nothing at all.

`min-width` works the other way, applying its rules only above a given
width rather than below it.

## Your turn

Let's open your browser's developer tools and switch to its device or
responsive mode, then resize to a narrow width, like a phone's. Now open
your fork and find the `@media (max-width: 768px)` block at the bottom
of `styles.css`. Try adding a second breakpoint for very small screens:

```css
@media (max-width: 480px) {
    .hero h1 {
        font-size: 1.75rem;
    }

    .container {
        padding: 0 1rem;
    }
}
```

Try changing `max-width: 480px` to `max-width: 800px` and notice when
the smaller heading starts to apply. Then try `min-width` in place of
`max-width`, and the rule applies above that width instead of below it.

## What you have now

CSS that only applies within a condition, rather than everywhere at once.

- **Media query** — a block of CSS that applies only when a condition,
  usually about screen width, is met.
- **`max-width` in a media query** — applies below a given width.
- **`min-width` in a media query** — applies above a given width.
