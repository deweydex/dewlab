---
title: "CSS variables and BEM names"
slug: css-variables-and-bem
module: web
module_title: "Web authoring"
series: first-site
version: 2026.09.05.1
---

# CSS variables and BEM names

Two buttons below share one rule for padding, shape and colour. Only the
second one looks different, and its own rule sets nothing but a colour.

```html site=buttons
<button class="button button--primary">Save</button>
<button class="button button--danger">Delete</button>
```

```css site=buttons
:root {
  --button-color: #2563eb;
}
.button {
  padding: 10px 18px;
  border: none;
  border-radius: 6px;
  color: white;
  font-weight: 600;
  background: var(--button-color);
}
.button--danger {
  --button-color: #dc2626;
}
```

## Why this happens

`:root` declares `--button-color` once, and `var(--button-color)` in
`.button` reads it back. `.button--danger` does not set a `background` of
its own. It resets `--button-color` for itself and its children, and
`.button`'s own rule reads that new value through `var()` instead of the
one on `:root`. One value, read in two places, changed once.

## Naming with BEM

`button` and `button--danger` follow a naming pattern called **BEM**,
short for Block, Element, Modifier. `button` is the **block**: a
self-contained piece, styled on its own. `button--danger` is a
**modifier**, joined to the block's name with two hyphens. It changes
how the block looks, without replacing its base rule. A block can also
have an **element**, a named part of it, joined with two underscores
instead. `button__icon`, for an icon inside a button, is one example.
None of the three ever nests a class inside another class's name.

A modifier class is always added beside the block's own class, never
used alone: `class="button button--danger"`, not
`class="button--danger"` by itself. Written this way, a class name says
on its own which block it belongs to and which variant it is. A reader
does not have to trace back through the CSS to find out.

## Your turn

Let's try adding a third button to the HTML above, with a class of
`button button--success`. Give `.button--success` its own rule that sets
`--button-color` to a green of your choosing, the same way
`.button--danger` does. Run it and check that the new button picks up
its own colour without any change to `.button`'s own rule.

## What you have now

One value, stored once and read in more than one place. Class names that
say what they are on their own, with no CSS to check.

- **CSS custom property** — a value declared once, most often on
  `:root`, and read back anywhere with `var()`.
- **Scoped override** — setting a custom property again on a more
  specific rule, changing its value for that rule and its children only.
- **BEM** — a naming pattern of block, element and modifier, joined with
  `__` and `--`. A class name says what it is for on its own.
