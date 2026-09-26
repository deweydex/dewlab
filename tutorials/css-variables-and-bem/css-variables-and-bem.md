---
title: "Naming classes so they stay tidy (BEM)"
year: "2026-2027"
version: 2026.09.11.1
covers:
  why-does-this-happen:
    covers: [WA-LO9]
  now-add-a-third-button:
    touches: [WA-LO9]
---

# Naming classes so they stay tidy (BEM)

As a stylesheet grows, it fills up with class names. Which rule styles
which part of the page? A good class name can tell us, before we open
the CSS. On this page we:

- read class names written in a pattern called BEM
- see how one extra class changes one button, and leaves the other alone
- add a third button of our own

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

1. Look at the HTML. Which class do both buttons have? Which class does
   only the second button have?
2. Look at the CSS. Which rule sets a `background`? What does the
   `.button--danger` rule set?
3. What if we delete `button--danger` from the second button's `class`
   in the HTML? Put it back afterwards.
4. What happens if we change the colour inside `.button--danger` to
   `#7c3aed`? Which button changes?
5. Now change the colour inside `:root` to `#16a34a`. Which button
   changes this time?

## Why does this happen?

Now we can explain what we saw. Both buttons have the class `button`,
so both get the padding, the rounded corners and the white text. The
second button also has `button--danger`, and only that button turns
red. Without that class, in step 3, it looked like the first one.

### Naming with BEM

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

### How the modifier changes the colour

The `.button--danger` rule sets no `background`. How does the button
turn red? It uses the CSS variable `--button-color`, which works
the way `--brand-color` did on [Colours, and naming them with
variables](tutorial:variables-and-colour). "Custom property" is its
official CSS name.

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

A variable passes down from an element to everything inside it. `:root`
holds the whole page, so every element can read the blue from `:root`.
But `.button--danger` sets `--button-color` again, on the second button
itself. So when the `.button` rule reads `var(--button-color)` on that
button, it finds the red first. This is a *scoped override*. A scoped
override sets a variable again on a more specific rule, and changes its
value for that element and the elements inside it only.

That explains steps 4 and 5. The purple in step 4 reached only the
second button. The green in step 5 reached only the first button,
because the second button has a value of its own.

Oftentimes a website keeps all its colours as variables on `:root`.
Then a modifier can change the colour for one part of the page, such
as one button, one card or a dark footer, and the block's own rule
stays the same.

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

Your own site has a block and a modifier too. In `index.html`, the
link styled as a button, under your main heading, has
`class="btn btn-primary"`. `btn` is
the block, and `btn-primary` is a variant of it, always used beside
`btn`. The idea is the same as BEM. Only the joining mark is different:
one hyphen, not two. The practice page renames it.

## What we have now

We can now give classes names that say what they are, and change one
variant of a block with a modifier class.

| Word | Meaning | Example |
|---|---|---|
| *BEM* | A naming pattern of block, element and modifier, joined with `__` and `--`, so that a class name says what it is for on its own | `button`, `button__icon`, `button--danger` |
| *block* | A self-contained piece, styled on its own | `button` |
| *element* (BEM) | A named part of a block, joined with `__` | `button__icon` |
| *modifier* | A variant of a block, joined with `--`, and always used beside the block's own class | `button--danger` |
| *scoped override* | A variable set again on a more specific rule, which changes its value for that element and the elements inside it only | `.button--danger { --button-color: #dc2626; }` |
