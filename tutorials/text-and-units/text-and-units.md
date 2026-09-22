---
title: "Text and units"
year: "2026-2027"
version: 2026.09.11.1
covers:
  why-does-this-happen:
    covers: [WA-LO9]
  now-in-your-own-site:
    touches: [WA-LO9]
---

# Text and units

When we write `16px` or `1rem` in CSS, what are we measuring in? On this
page we:

- compare two units, `px` and `rem`, side by side
- see why your site uses `rem` for most of its sizes
- move text to the left, the right and the centre with `text-align`

## Let's try it

The HTML below has two boxes. In the CSS, one box measures its padding
in `px`, and the other in `rem`. The first line sets the font size for
the whole page.

```html site
id: units-html
site: units
<div class="box-px">Measured in px</div>
<div class="box-rem">Measured in rem</div>
```

```css site
id: units-css
site: units
html { font-size: 20px; }
.box-px { padding: 16px; border: 1px solid #2c3e50; margin-bottom: 8px; }
.box-rem { padding: 1rem; border: 1px solid #2c3e50; }
```

1. Look at the space between the words and the border in each box. Is
   it the same in both?
2. On the first line, change `20px` to `40px`. What happens to the
   words in each box?
3. Now look at the space around the words. Which box's space grows,
   and which stays the same?
4. What if we change it to `16px`? How do the two boxes compare now?

## Why does this happen?

Each box uses a different unit for its padding. Now we can explain what
we saw.

| Unit | What it is measured against | `1` of it, by default |
|---|---|---|
| `px` | nothing: it is fixed | 1 pixel |
| `rem` | the root font size, set on `<html>` | 16 pixels |
| `%` | the parent element | depends on the parent |

- A *pixel* (`px`) is a fixed unit. `16px` is always 16 pixels,
  whatever else on the page changes. That is why the first box kept the
  same space.
- A *rem* is a unit measured against the *root font size*, the font
  size set on `<html>`. Browsers set this to `16px` by default, so
  normally `1rem` equals `16px`. When we changed the root to `40px`,
  `1rem` became `40px`, and the second box's space grew to match. At
  `16px`, the two boxes looked the same.
- A percentage (`%`) is measured against the parent element, the
  element this one sits inside. For a width, `50%` means half the
  parent's width. That is why percentages turn up most often for
  widths.

And why did the words grow in both boxes? The boxes do not set a font
size of their own, so their text takes the font size from `<html>`.

Why does this matter? Some people set their browser to a larger font
size. It is a common choice for people with visual impairments. Wherever
a page uses `rem`, its spacing and text grow to match that setting. That
is why the starter uses `rem` for most spacing and font sizes.

Sometimes we might zoom in on a page, with **Ctrl** and **+** (or
**Cmd** and **+** on a Mac), and see everything grow, `px` sizes too.
Zoom scales the whole page. The font size setting in the browser's
options is different: it changes the root font size, so `rem` sizes
follow it and `px` sizes do not. That makes it an easy way to test a
page. Change the font size setting, and see what stays small.

### Lining up text

Text has its own property, `text-align`. It sets where the lines of text
sit inside their element. It has four common values:

- `left` lines the text up on the left edge
- `right` lines it up on the right edge
- `center` puts each line in the middle
- `justify` stretches each line so both edges line up, except the last
  line of a paragraph

Newspapers often justify their columns. On the web, `justify` can leave
wide, uneven gaps between words, and these are worse in a narrow
column. Many readers, including many people with dyslexia, find those
gaps harder to read.

Oftentimes, when we put `text-align: center` on a box, we expect the box
itself to move to the middle. It does not. The box stays where it is,
and only the lines of text inside it move. Centring the box itself is a different job, which we meet in
[Setting a page's width and centring it](tutorial:the-container).

## Now in your own site

In your fork, open `styles.css`.

1. Find the `.hero` rule. It sets `text-align: center`.
2. Change it to `text-align: left`.
3. Save, and refresh.
4. Now try `text-align: right`.

How differently do the same words sit on the page each time? Which one
do you want to keep?

## What we have now

We can now choose between units that hold their size in different ways,
and move text sideways.

| Word | Meaning | Example |
|---|---|---|
| *pixel* (`px`) | A fixed unit | `padding: 16px;` |
| *rem* | A unit measured against the root font size. It grows with the reader's own font size setting. | `padding: 1rem;` |
| *root font size* | The font size set on `<html>`. It is `16px` by default. | `html { font-size: 20px; }` |
| `text-align` | A property that sets where lines of text sit: `left`, `right`, `center` or `justify` | `text-align: center;` |
