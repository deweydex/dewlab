---
title: "Naming classes so they stay tidy (BEM)"
year: "2026-2027"
version: 2026.09.11.1
covers:
  why-does-this-happen:
    covers: [WA-LO9]
  naming-with-bem:
    touches: [WA-LO9]
  now-add-a-third-button:
    touches: [WA-LO9]
---

# Naming classes so they stay tidy (BEM)

On [Colours, and naming them with variables](tutorial:variables-and-colour) we stored a
colour in a CSS variable and read it back in several rules. This page
goes one step further. Can one rule give two buttons two different
colours? On this page we:

- change a variable in two places, and see which button follows
- learn to set a variable again for one element only
- meet BEM, a way of naming classes so that each name explains itself

## Let's try it

Here are two buttons. The CSS has one rule, `.button`, for both of them,
and one small rule for the second button.

```html site
id: buttons-html
site: buttons
<button class="button button--primary">Save</button>
<button class="button button--danger">Delete</button>
```

```css site
id: buttons-css
site: buttons
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

1. Look at the CSS. Which rule sets a `background`? What does the
   `.button--danger` rule set?
2. What happens if we change the colour inside `:root` to `#16a34a`?
   Which button changes?
3. Now change the colour inside `.button--danger` instead. Which button
   changes this time?
4. What if we delete `button--danger` from the second button's `class`
   in the HTML? Put it back afterwards.

## Why does this happen?

Now we can explain what we saw. The first button follows the value on
`:root`. The second button follows the value in `.button--danger`. Yet
only `.button` sets a `background`.

The variable `--button-color` is a *CSS custom property*. A CSS custom
property is a value declared once, most often on `:root`, and read back
anywhere with `var()`. "Custom property" is the official CSS name for
what we have been calling a CSS variable.

Here is the path the value takes:

```css
:root {
  --button-color: #2563eb;       /* 1. declared once, for the whole page */
}
.button {
  background: var(--button-color); /* 2. read back here */
}
.button--danger {
  --button-color: #dc2626;       /* 3. set again, for this button only */
}
```

- `:root` declares `--button-color` once. `:root` selects the `<html>`
  element, which holds every other element on the page. A custom
  property passes down from an element to everything inside it, so
  every element on the page can read this value.
- `var(--button-color)` in `.button` reads the value back.
- `.button--danger` sets no `background` of its own. It sets
  `--button-color` again, for itself and its children. So when
  `.button`'s rule reads `var(--button-color)` on the second button, it
  gets the new value, not the one on `:root`.

This is a *scoped override*. A scoped override sets a custom property
again on a more specific rule, and changes its value for that rule and
its children only. One value is read in two places, and changed in one.

That explains step 4 too. Without the class `button--danger`, the second
button has no value of its own, so it reads the one on `:root`, like
the first button.

Oftentimes, a website keeps all its colours as custom properties on
`:root`. A scoped override then changes the colour for one part of the
page, such as one button, one card or a dark footer, and the main rules
stay the same.

## Naming with BEM

The class names `button` and `button--danger` follow a naming pattern
called *BEM*. BEM is short for Block, Element, Modifier. It is a way of
naming classes so that a class name says on its own which block it
belongs to, and which variant it is.

| Part | What it is | How it is joined | Example |
|---|---|---|---|
| *block* | A self-contained piece, styled on its own | the name on its own | `button` |
| *element* | A named part of a block | two underscores, `__` | `button__icon`, for an icon inside a button |
| *modifier* | A variant that changes how the block looks, without replacing its base rule | two hyphens, `--` | `button--danger` |

Note that "element" here means BEM's element, a named part of a block.
It is a different thing from an HTML element.

Each BEM class works on its own in the CSS. We write `.button__icon`
as the selector. We do not need a selector that puts one class inside
another, like `.button .icon`.

A modifier class always goes beside the block's own class. It is never
used alone. So we write `class="button button--danger"`. We do not write
`class="button--danger"` by itself. The block class brings the base
rule, and the modifier class adds the change.

Written this way, a class name tells a reader which block it belongs to
and which variant it is. The reader does not have to trace back through
the CSS to find out.

## Now add a third button

Can we add a green button, the same way the red one works?

1. In the HTML box, add a third button with the class
   `button button--success`.
2. In the CSS box, add a `.button--success` rule.
3. Inside it, set `--button-color` to a green of your choosing, the
   same way `.button--danger` does.
4. Look at the preview.

Does the new button pick up its own colour, with no change to the
`.button` rule?

## What we have now

We can now store a value once and read it in more than one place, and
we can give classes names that say what they are, with no CSS to check.

| Word | Meaning | Example |
|---|---|---|
| *CSS custom property* | A value declared once, most often on `:root`, and read back anywhere with `var()` | `--button-color: #2563eb;` |
| *scoped override* | A custom property set again on a more specific rule, which changes its value for that rule and its children only | `.button--danger { --button-color: #dc2626; }` |
| *BEM* | A naming pattern of block, element and modifier, joined with `__` and `--`, so that a class name says what it is for on its own | `button`, `button__icon`, `button--danger` |
