---
title: "Several pages, one navigation"
slug: pages-and-navigation
module: web
module_title: "Web authoring"
series: several-pages
version: 2026.09.05.1
---

# Several pages, one navigation

Change which link below carries `aria-current="page"`. That link becomes
bold; the rest of the menu never changes.

```html site=nav
<nav aria-label="Main">
  <ul>
    <li><a href="index.html" aria-current="page">Home</a></li>
    <li><a href="about.html">About</a></li>
    <li><a href="gallery.html">Gallery</a></li>
  </ul>
</nav>
```

```css site=nav
nav ul { display: flex; gap: 16px; list-style: none; }
nav a[aria-current="page"] { font-weight: bold; text-decoration: underline; }
```

## Why this happens

`aria-current="page"` marks which link points at the page a visitor is
already on. A screen reader announces it; the CSS rule above just makes
it visible too, so a sighted visitor gets the same information.

Everything else about the menu — the links, their order, their wording —
stays exactly the same from page to page. That sameness is what
"consistent navigation" means: one menu, copied onto every page, with
only its current-page marker changing. A visitor who has found their way
around one page already knows where everything is on the next.

## Your turn

Let's open your fork of `project_wad` and compare the `<nav>` in all
five HTML files. The links should be identical and in the same order
everywhere, and only the current page's link should carry
`aria-current="page"`. If you renamed any file while planning your site
map, try updating every file's navigation to match — the same small
edit, five times, not once.

## What you have now

One menu that appears five times, and a marker that says which copy a
visitor is standing on.

- **`aria-current="page"`** — marks the link pointing at the current
  page.
- **Consistent navigation** — the same menu, in the same order, on every
  page of a site.
