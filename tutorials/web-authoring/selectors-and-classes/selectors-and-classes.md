---
title: "Selectors and classes"
slug: selectors-and-classes
module: web-authoring
module_title: "Web Authoring"
year: "2026-2027"
series: first-site
version: 2026.09.11.1
covers:
  why-this-happens:
    covers: [WA-LO9]
  your-turn:
    touches: [WA-LO9]
---

# Selectors and classes

Both paragraphs below say almost the same thing. Only one of them turns
red.

```html site
id: selectors-html
site: selectors
<div class="highlight">
  <p>Inside the highlighted box.</p>
</div>
<p>Outside it.</p>
```

```css site
id: selectors-css
site: selectors
.highlight p {
  color: firebrick;
  font-weight: bold;
}
```

## Why this happens

`.highlight` is a *class selector*: it matches any element carrying
`class="highlight"`, wherever it sits on the page.

`.highlight p` is a *descendant selector*: two selectors joined by a
space. It matches a `<p>` only when it sits somewhere inside an element
matching `.highlight`, at any depth, not only as a direct child. That is
why the paragraph outside the highlighted box stays untouched.

## Your turn

Let's open your fork and find the skills section you added earlier. Try
adding this to `styles.css`, near the bottom, before any `@media` rules:

```css
.skills-section {
    background-color: var(--light-gray);
}

.skills-section .card {
    border-left: 4px solid var(--accent-color);
}
```

Save and refresh. The border shows up only on cards inside the skills
section, because `.skills-section .card` is a descendant selector. Try
changing it to plain `.card` for a moment and see which other cards on
the page pick up the same border.

## What you have now

A way to style one part of a page without touching the rest of it.

A *class selector* matches every element carrying a given class. A
*descendant selector* is two selectors joined by a space, matching an
element nested inside another.
