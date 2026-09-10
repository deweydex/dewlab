---
title: "Flexible images"
slug: flexible-images
module: web
module_title: "Web authoring"
series: first-site
version: 2026.09.04.1
---

# Flexible images

Both images below are the same file, 500 pixels wide. Drag the preview
narrow. One of them spills past the edge; the other shrinks to fit.

```html site=responsive-img
<img class="plain" alt="A test image, 500 by 300"
     src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='500' height='300'%3E%3Crect width='500' height='300' fill='%232c3e50'/%3E%3Ctext x='50%25' y='50%25' fill='white' font-size='28' text-anchor='middle' dominant-baseline='middle'%3E500x300%3C/text%3E%3C/svg%3E">
<img class="responsive" alt="The same test image, made flexible"
     src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='500' height='300'%3E%3Crect width='500' height='300' fill='%232c3e50'/%3E%3Ctext x='50%25' y='50%25' fill='white' font-size='28' text-anchor='middle' dominant-baseline='middle'%3E500x300%3C/text%3E%3C/svg%3E">
```

```css site=responsive-img
img { display: block; margin-bottom: 8px; }
.responsive { max-width: 100%; height: auto; }
```

## Why this happens

An `<img>` normally renders at its file's own size, however wide its
container is. `max-width: 100%` caps it at its container's width instead,
so it shrinks on a narrow screen rather than spilling past the edge.

`height: auto` keeps the image's proportions as it shrinks, so a square
image stays square rather than being squashed. That relationship between
an image's width and its height is its **aspect ratio**.

## Your turn

Let's open your fork and find wherever you added an image earlier. Check
that it already has these two properties, either on the image itself or
through a rule that reaches it. Try narrowing your browser to a phone
width to confirm it never goes past the edge of the page.

## What you have now

An image that fits its container at any width, on any screen.

- **`max-width: 100%`** — caps an image at its container's width.
- **`height: auto`** — keeps an image's proportions as it shrinks.
- **Aspect ratio** — the relationship between an image's width and its
  height.
