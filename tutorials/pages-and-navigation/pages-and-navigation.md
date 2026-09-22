---
title: "One navigation bar across several pages"
year: "2026-2027"
version: 2026.09.11.1
covers:
  why-does-this-happen:
    touches: [WA-LO2, WA-LO4]
  now-in-your-own-site:
    touches: [WA-LO8]
---

# One navigation bar across several pages

Every page of a site has the same menu. So how does a visitor know which
page they are on? On this page we move a marker in a menu, then check
your own site's menus.

## Let's try it

Here is a small menu, with its CSS.

```html site
id: nav-html
site: nav
<nav aria-label="Main">
  <ul>
    <li><a href="index.html" aria-current="page">Home</a></li>
    <li><a href="about.html">About</a></li>
    <li><a href="gallery.html">Gallery</a></li>
  </ul>
</nav>
```

```css site
id: nav-css
site: nav
nav ul { display: flex; gap: 16px; list-style: none; }
nav a[aria-current="page"] { font-weight: bold; text-decoration: underline; }
```

1. Which link looks different from the others?
2. Move `aria-current="page"` to the **About** link. What changes?
3. What stays the same?

## Why does this happen?

`aria-current="page"` marks the link that points at the page a visitor
is already on. A screen reader announces it. The second CSS rule makes
it visible too, so a sighted visitor gets the same information.

That rule uses an *attribute selector*. An attribute selector is an
attribute in square brackets. It matches elements that carry that
attribute and value. When we moved the attribute, the bold style moved
too. (In the first rule, `list-style: none` removes the list's
bullet points.)

Everything else stayed the same: the links, their order and their
wording. This is *consistent navigation*: one menu, copied onto every
page, with only the current-page marker changing. A visitor who knows
their way around one page already knows where everything is on the
next.

Oftentimes, when we copy a menu onto a new page, we forget to move the
marker. Then the new page says that **Home** is the current page. It is
an easy mistake to miss, because only one word looks different.

## Now in your own site

1. Open your copy of `project_wad`.
2. Compare the `<nav>` in all five HTML files. Are the links the same,
   and in the same order?
3. Does only the current page's link carry `aria-current="page"`?
4. Did you rename a file while planning your site map? Then update the
   navigation in every file to match: the same small edit, five times.

Does each page mark itself, and only itself, as the current page?

## What we have now

We now have one menu on five pages, and a marker that says which page a
visitor is on.

- `aria-current="page"` marks the link pointing at the current page.
- An *attribute selector*, like `a[aria-current="page"]`, matches
  elements that carry that attribute.
- *Consistent navigation* is the same menu, in the same order, on every
  page of a site.
