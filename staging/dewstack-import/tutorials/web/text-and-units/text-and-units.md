---
title: "Text and units"
slug: text-and-units
module: web
module_title: "Web authoring"
series: first-site
version: 2026.09.04.1
---

# Text and units

Try changing `html { font-size: 20px; }` below to `40px`. One box's
spacing doubles. The other's stays exactly the same.

```html site=units
<div class="box-px">Measured in px</div>
<div class="box-rem">Measured in rem</div>
```

```css site=units
html { font-size: 20px; }
.box-px { padding: 16px; border: 1px solid #2c3e50; margin-bottom: 8px; }
.box-rem { padding: 1rem; border: 1px solid #2c3e50; }
```

## Why this happens

A **pixel** (`px`) is fixed: `16px` is always 16 pixels, whatever else on
the page changes.

A **rem** is relative to the root font size, the one set on `<html>`.
Browsers set this to 16px by default, so normally `1rem` equals `16px`.
Change the root, though, and every `rem` value follows it, as the box
above just did. Some people set their browser to a larger font size, a
common choice for people with visual impairments. Wherever `rem` is used,
their spacing and text scale to match. That is why the starter uses `rem`
for most spacing and font sizes.

A percentage (`%`) is relative to the parent element's own size rather
than the root, which is why it turns up most often for widths.

Text has its own property, `text-align`, with four common values: `left`,
`right`, `center` and `justify`. `justify` stretches each line to the same
width; it can read well for a narrow newspaper column and less well for a
wide one.

## Your turn

Let's open your fork and find the `.hero` rule in `styles.css`. It sets
`text-align: center`. Try `text-align: left`, then `text-align: right`,
and notice how differently the same words sit on the page.

## What you have now

Two units that hold their ground differently, and a property that moves
text sideways.

- **`px`** — a fixed unit.
- **`rem`** — relative to the root font size; scales with a reader's own
  settings.
- **`text-align`** — `left`, `right`, `center` or `justify`.
