---
title: "Text size, units and alignment"
year: "2026-2027"
version: 2026.09.11.1
covers:
  why-does-this-happen:
    covers: [WA-LO9]
  now-in-your-own-site:
    touches: [WA-LO9]
---

# Text size, units and alignment

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

![Two panels, each with the same two boxes. In the left panel the root font size is 16px: the box measured in px has 16 pixels of padding, and the box measured in rem has 1rem, which is also 16 pixels, so the two look the same. In the right panel the root font size is 40px: the px box still has 16 pixels of padding, but the rem box now has 40 pixels. The text in both boxes is bigger, because both take their font size from the root.](px-and-rem.svg)

And why did the words grow in both boxes? The boxes do not set a font
size of their own, so their text takes the font size from `<html>`.

Why does this matter? Some people set their browser to a larger font
size. It is a common choice for people with visual impairments. Wherever
a page uses `rem`, its spacing and text grow to match that setting. That
is why the starter uses `rem` for most spacing and font sizes.

### Lining up text

Text has its own property, `text-align`. It sets where the lines of text
sit inside their element. It has four common values:

- `left` lines the text up on the left edge
- `right` lines it up on the right edge
- `center` puts each line in the middle
- `justify` stretches each line so both edges line up, except the last
  line of a paragraph

![Four copies of the same short paragraph, one for each value of text-align. Each word is drawn as a bar. With left, every line starts at the left edge and the right edge is ragged. With right, every line ends at the right edge. With center, each line sits in the middle, so both edges are ragged. With justify, every line but the last is stretched to touch both edges, and the last line starts at the left.](text-align-values.svg)

Oftentimes, when we put `text-align: center` on a box, we expect the box
itself to move to the middle. It does not. The box stays where it is,
and only the lines of text inside it move. Centring the box itself is a
different job, which we meet in [A readable width, centred on the
page](tutorial:the-container).

## Now in your own site

In your fork, open `styles.css`.

1. Find the `:root` section near the top. Under the colours is a group
   of spacing variables, from `--spacing-xs` to `--spacing-xl`. Which
   unit do they use? Read the comment just above them.
2. Now find the `.hero` rule. It sets `text-align: center`.
3. Change it to `text-align: left`.
4. Save, and refresh.
5. Now try `text-align: right`.

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

## Where to read more

Tantacrul (2021). *How I Designed a Free Music Font for 5 Million
Musicians (MuseScore 3.6).* <https://www.youtube.com/watch?v=XGo4PJd1lng>.
Martin Keary and an engraving expert design a font for music notation, and
explain the choices behind it. About twenty minutes.
