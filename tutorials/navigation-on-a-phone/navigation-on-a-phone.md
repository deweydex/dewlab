---
title: "A navigation that works on a phone"
year: "2026-2027"
version: 2026.09.11.1
covers:
  why-does-this-happen:
    touches: [WA-LO9, WA-LO10]
  now-in-your-own-site:
    touches: [WA-LO9, WA-LO10]
---

# A navigation that works on a phone

A row of links fits easily on a laptop. What happens to it on a phone?

## Let's try it

Here is a logo and three links. The CSS ends with a media query.

```html site
id: phone-nav-html
site: phone-nav
<nav aria-label="Main">
  <a href="#" class="logo">Site</a>
  <ul>
    <li><a href="#">Home</a></li>
    <li><a href="#">About</a></li>
    <li><a href="#">Contact</a></li>
  </ul>
</nav>
```

```css site
id: phone-nav-css
site: phone-nav
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

1. Drag the **Preview width** slider from wide to narrow. What
   happens to the links? Are they still in the same order?
2. What happens if we delete `flex-direction: column;` from the
   `nav ul` rule inside the media query?

## Why does this happen?

Now we can explain what we saw. At 350 pixels, the media query switches
on. The links drop out of the logo's row and stack into a column, in the
same order. Only the direction changes.

`flex-direction` sets the direction of a flex container. Its default
value is `row`, which lays items out side by side. `column` stacks them
from top to bottom. In step 2, without `column`, the list became a row
again.

Why not let the links wrap, as on [Lining boxes up in a row with Flexbox](tutorial:flexbox-first-steps)? Wrapping stops links
from squeezing sideways until they overlap, but it can leave a ragged
half-row, with one link alone on the next line. A whole menu stacked
into one column is easier to read.

## Now in your own site

1. In your fork of `project_wad`, open `styles.css`.
2. Find the `@media (max-width: 480px)` block. Can you find
   `flex-direction: column` inside it?
3. Open your site in device mode, as on [Changing the layout for phones: media queries](tutorial:media-queries), at a phone's width. Your navigation
   should already stack into a column.
4. If you changed page names while planning your site map, read the
   menu. Does it show the right links, in the right order?

## What we have now

We can now make a navigation that reads clearly at any width, without a
hidden menu or any JavaScript.

| Word | Meaning | Example |
|---|---|---|
| `flex-direction: column` | Stacks a flex container's items from top to bottom, often inside a media query. The default is `row`. | `nav ul { flex-direction: column; }` |
