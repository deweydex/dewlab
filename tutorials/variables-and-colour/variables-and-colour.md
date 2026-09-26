---
title: "Colours, and naming them with variables"
year: "2026-2027"
version: 2026.09.11.1
covers:
  why-does-this-happen:
    covers: [WA-LO9]
  now-in-your-own-site:
    touches: [WA-LO9]
---

# Colours, and naming them with variables

Suppose one colour appears in ten places on your site, and you want to
change it. Do you have to edit all ten? On this page we:

- change one colour value and watch what it reaches
- learn how a CSS variable stores a value once, for many rules to use
- choose new colours for your own site, and check they stay readable

## Let's try it

The HTML below has two boxes: a header and a button. The CSS under it
has two rules.

```html site
id: variables-html
site: variables
<div class="header">Header</div>
<div class="button">Button</div>
```

```css site
id: variables-css
site: variables
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

1. Near the top of the CSS, change `#2c3e50` to `firebrick`. What
   happens to the header? What happens to the button?
2. Look at the second rule. Does it name a colour for the background
   anywhere?
3. Try `darkgreen`, or a colour of your own. Where does the new colour
   come from?

## Why does this happen?

A few pieces of this CSS are new. Here they are, one at a time.

```css
:root {
  --brand-color: #2c3e50;           /* define the variable, once */
}
.header, .button {
  background: var(--brand-color);   /* read the variable back */
  ...
}
```

- `--brand-color` is a *CSS variable*, also called a custom property.
  A CSS variable is a value we define once and use again wherever we
  need it. Its name always starts with two dashes.
- `:root` is a selector. It matches the `<html>` element, the one that
  holds the whole page. A variable defined there can be read by every
  element on the page, so a page's variables usually live in `:root`.
- `var()` reads a variable's value back into a declaration.
  `var(--brand-color)` means "use whatever `--brand-color` holds".

Now we can explain what we saw. The header and the button do not name a
colour of their own. Both read `--brand-color`. When we change the
definition, everything that reads it changes too.

![On the left, the rule for :root holds one line, --brand-color: #2c3e50. Two arrows run from it to the right, one to a box labelled .header and one to a box labelled .button. Each box holds the line background: var(--brand-color). Both boxes are filled with the same solid colour.](one-variable-two-rules.svg)

Without a variable, changing a colour used in ten places means editing
ten rules, and it is easy to miss one. With a variable, we edit one
line.

The selector `.header, .button` is also new. `.header` matches the
element with `class="header"`, and the comma lets one rule style both
elements. [Choosing what to style: selectors and classes](tutorial:selectors-and-classes) looks
at selectors like these more closely. The `padding` and `margin-bottom`
lines add space around each box, which we explore in [The box model:
padding, border and margin](tutorial:the-box).

What about `#2c3e50`? That is a *hex colour*. It is a `#` followed by
three pairs of characters, for the amount of red, green and blue. Each
character is a digit from `0` to `9` or a letter from `a` to `f`, and
each pair goes from `00` (none) to `ff` (full). So `#000000` is black, and
`#ffffff` is white. Colour names like `firebrick` work too, but hex
colours can describe millions of shades.

## Now in your own site

Your fork's `styles.css` uses variables for its colours.

1. Open `styles.css` and find the `:root` section near the top.
2. Change `--primary-color` to a colour you like.
3. Change `--accent-color` too.
4. Save, and refresh. Which parts of the page changed?

The header, the hero section, the footer and the buttons all change at
once, because they all read the same two variables.

A new colour also has to keep the text on it readable. The starter's
default colours were chosen so that text stays readable, and a comment
in the `:root` section says so. A contrast checker, such as the one at
[webaim.org](https://webaim.org/resources/contrastchecker/), confirms
this. It compares the colour of the text with the colour behind it, and
gives a ratio. For ordinary text, a ratio of at least 4.5 to 1 passes
the common standard, WCAG AA.

5. Your header and your hero section show white text on
   `--primary-color`. Put `#ffffff` and your new `--primary-color` into
   the checker. Does it pass?
6. The main button shows white text on `--accent-color`. Does that pair
   pass too?
7. If both pass, commit the change, with a message such as "Choose my
   own site colours". If one fails, try a darker shade first.

## What we have now

We can now define a value once and read it from several rules.

| Word | Meaning | Example |
|---|---|---|
| *CSS variable* | A value defined once and reused. It is also called a custom property. | `--brand-color: #2c3e50;` |
| `:root` | The selector that matches `<html>`. A page's variables usually live there. | `:root { ... }` |
| `var()` | Reads a variable's value back into a declaration | `background: var(--brand-color);` |
| *hex colour* | A colour written as `#` and three pairs of characters, for red, green and blue | `#2c3e50` |

## Where to read more

Captain Disillusion (2020). *CD / Color.*
<https://www.youtube.com/watch?v=FTKP0Y9MVus>. Captain Disillusion
explains how a screen makes every colour from red, green and blue light.
Seven minutes.
