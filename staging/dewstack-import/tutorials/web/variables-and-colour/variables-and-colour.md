---
title: "Variables and colour"
slug: variables-and-colour
module: web
module_title: "Web authoring"
series: first-site
version: 2026.09.04.1
---

# Variables and colour

Change the one colour near the top below, and both boxes update, even
though neither box's own rule mentions a colour.

```html site=variables
<div class="header">Header</div>
<div class="button">Button</div>
```

```css site=variables
:root {
  --brand-color: #2c3e50;
}
.header, .button {
  background: var(--brand-color);
  color: white;
  padding: 12px;
  margin-bottom: 8px;
}
```

## Why this happens

`--brand-color` is a **CSS variable**, also called a custom property. The
`:root` selector defines it once, and `var(--brand-color)` reads it back
wherever it is used. Change the definition, and everywhere that reads it
changes too.

Without a variable, changing a colour used in ten places means editing ten
rules, and it is easy to miss one.

## Your turn

Let's open your fork's `styles.css` and find the `:root` section near
the top. Try changing `--primary-color` and `--accent-color` to colours
you like. Save and refresh: the header, the hero section, the footer
and the buttons all change at once, because they all read the same two
variables.

The starter's default colours were chosen so that text stays readable: a
contrast checker, such as the one at
[webaim.org](https://webaim.org/resources/contrastchecker/), confirms
this. Try checking whether your own choices still pass.

## What you have now

One value, defined once, read from several rules.

- **CSS variable** — a value defined once and reused; also called a
  custom property.
- **`:root`** — the selector usually holding a page's variable
  definitions.
- **`var()`** — reads a variable's value back into a declaration.
