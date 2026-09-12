---
title: "A navigation that works on a phone"
slug: navigation-on-a-phone
module: web
module_title: "Web authoring"
series: several-pages
version: 2026.09.05.1
---

# A navigation that works on a phone

Drag the preview narrow. The links below drop out of the logo's row and
stack into a column instead of squeezing sideways until they overlap.

```html site=phone-nav
<nav aria-label="Main">
  <a href="#" class="logo">Site</a>
  <ul>
    <li><a href="#">Home</a></li>
    <li><a href="#">About</a></li>
    <li><a href="#">Contact</a></li>
  </ul>
</nav>
```

```css site=phone-nav
nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
}
nav ul { display: flex; gap: 16px; list-style: none; }

@media (max-width: 350px) {
  nav { flex-direction: column; align-items: flex-start; }
  nav ul { flex-direction: column; gap: 8px; }
}
```

## Why this happens

A media query switches `flex-direction` from `row`, the default, to
`column` once the screen is narrow enough. The same nav, the same links,
in the same order: only the direction they lay out in changes.

A row of links that fits a desktop screen easily can run out of room on
a phone. Wrapping, the fix from earlier pages, still leaves a ragged
half-row. Stacking the whole menu into a column, all at once, reads more
clearly than a row that almost fits.

## Your turn

Let's open your fork of `project_wad` and find the
`@media (max-width: 480px)` block in `styles.css`. Try checking your
site at a phone width in your browser's device mode. The navigation
should already stack into a column. If you changed your page names while
planning your site map, confirm the stacked menu still shows the right
links in the right order.

## What you have now

A navigation that reads clearly at any width, without a hidden menu or
any JavaScript.

- **`flex-direction: column`** — switches a flex row to a flex column,
  usually inside a media query.
