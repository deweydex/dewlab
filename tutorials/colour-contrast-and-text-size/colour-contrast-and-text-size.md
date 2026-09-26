---
title: "Colour, contrast and text size"
year: "2026-2027"
version: 2026.09.22.1
context_for: [variables-and-colour, text-and-units]
---

# Colour, contrast and text size

Every reader sees a page a little differently. Some see colours less
clearly. Some make their text bigger. Two pages meet this question:
[Colours, and naming them with variables](tutorial:variables-and-colour)
and [Text size, units and alignment](tutorial:text-and-units). This
page looks at it more closely. It is background reading. You do not
need it to finish those pages, but it can help you choose colours and
sizes that work for everyone.

On this page we:

- see four ways to write the same colour
- learn to read a contrast ratio, and what counts as a pass
- see what happens when a reader makes the text bigger
- see how the way text lines up changes how easy it is to read

## Four ways to write a colour

So far we have met colour names, like `firebrick`, and hex colours,
like `#2c3e50`. CSS has other ways to write a colour too. Here are four
boxes. Each one writes its colour in a different way.

```html site
id: colour-formats-html
site: colour-formats
<div class="hex">#336699</div>
<div class="short">#369</div>
<div class="rgb">rgb(51 102 153)</div>
<div class="hsl">hsl(210 50% 40%)</div>
```

```css site
id: colour-formats-css
site: colour-formats
div { color: white; padding: 12px; margin-bottom: 4px; }
.hex { background: #336699; }
.short { background: #369; }
.rgb { background: rgb(51 102 153); }
.hsl { background: hsl(210 50% 40%); }
```

1. Do the four boxes look the same?
2. In the `.hsl` rule, change `40%` to `25%`, and then to `70%`. What
   changes? What stays the same?
3. Put `40%` back. Now change `210` to `0`, and then to `120`. What
   happens?
4. In the `.rgb` rule, change `153` to `51`. Which part of the colour
   did we remove?

Now we can explain what we saw. All four boxes are the same colour,
written four ways.

- **Hex**, `#336699`, is three pairs of characters, for red, green and
  blue. Each pair is a number written in base 16, where the digits go
  from `0` to `9` and then `a` to `f`. So `33` is 51, `66` is 102, and
  `99` is 153.
- **Short hex**, `#369`, works when both characters of every pair are
  the same. The browser doubles each one: `#369` means `#336699`, and
  `#fff` means `#ffffff`.
- **rgb()**, as in `rgb(51 102 153)`, writes the same three amounts
  as ordinary numbers, from `0` (none) to `255` (full). It is the same
  colour as `#336699`. In step 4, we removed most of the blue.
- **hsl()**, as in `hsl(210 50% 40%)`, describes a colour by its hue,
  its saturation and its lightness. The hue is an angle on a colour wheel, from `0` to `360`: `0` is red,
  `120` is green, and `240` is blue. Saturation says how strong the
  colour is, from `0%` (grey) to `100%`. Lightness goes from `0%`
  (black) to `100%` (white).

In step 2, only the lightness changed, so the box got darker or
lighter, and it stayed the same blue. That makes `hsl()` handy for a
set of colours that belong together: keep the hue, and change the
lightness. In step 3, the hue moved round the wheel, to red and then to
green.

Sometimes we might see a fourth value, after a slash: `rgb(0 0 0 / 0.1)`.
That fourth value is the *alpha*, how solid the colour is, from `0`
(fully see-through) to `1` (solid). Your starter's shadows use an older
way of writing the same thing, with commas: `rgba(0, 0, 0, 0.1)` is
black that is 90% see-through. Both ways work in every modern browser.

## Reading a contrast ratio

On the colours page, we put two colours into a contrast checker, and
it gave a ratio. What does that number mean?

A *contrast ratio* compares how light two colours are: the text colour
and the colour behind it. It goes from 1 to 1, for two colours that are
the same, up to 21 to 1, for black on white. The bigger the first
number, the easier the text is to read.

The common standard for this is *WCAG*, the Web Content Accessibility
Guidelines. It sets two levels:

| Level | Ordinary text | Large text |
|---|---|---|
| AA, the common standard | at least 4.5 to 1 | at least 3 to 1 |
| AAA, the stricter one | at least 7 to 1 | at least 4.5 to 1 |

Large text means text at least `24px` tall, or at least about `19px`
tall in bold. Most body text is smaller than that, so 4.5 to 1 is the
number to remember.

Here are some pairs, with their ratios:

| Text | Background | Ratio | AA, ordinary text? |
|---|---|---|---|
| black | white | 21 to 1 | passes |
| white | `#2c3e50`, your starter's `--primary-color` | 10.98 to 1 | passes |
| white | `#2672ad`, your starter's `--accent-color` | 5.13 to 1 | passes |
| `#5f6f73`, your `--text-light` | `#f8f9fa`, your `--light-gray` | 4.97 to 1 | passes |
| `#767676` | white | 4.54 to 1 | passes, just |
| `#777777` | white | 4.48 to 1 | fails, just |
| white | `#3498db` | 3.15 to 1 | fails, but passes for large text |

Two things in this table surprise most people. First, `#767676` and
`#777777` look the same to our eyes, but one passes and one fails. The
standard sets one exact number, and a checker is the only sure way to know
which side of it a colour is on. Second, a bright, strong colour like
`#3498db` can still fail with white text. How strong a colour is and
how light it is are two different things.

We do not always need a separate website to check. In Chrome and Edge,
select an element in the inspector, and click the small colour square
beside its `color` value in the **Styles** pane. The colour picker that
opens shows the contrast ratio against the background.

Contrast is one part of making colour work for everyone. Another is
never to use colour as the only clue. Say a form marks a mistake only
by turning a box red. A reader who cannot tell red from green, or who
uses a screen reader, misses the message. A word or an icon as well as
the colour reaches everyone.

## When a reader makes the text bigger

There are two ways to make a page bigger in a browser, and they work
differently.

- **Zoom**, with **Ctrl** and **+** (or **Cmd** and **+** on a Mac),
  scales the whole page. Everything grows, `px` sizes too.
- **The font size setting**, in the browser's settings, changes the
  root font size. Sizes in `rem` follow it, and sizes in `px` do not.

Some people with low vision set a bigger font size once, in their
browser's settings, and leave it there for every site. So the font
size setting is a good way to test a page. Change it, and look for
what stays small. A `px` size for text, or a `px` width that holds
text, is often the cause. The practice page for [Text size, units and
alignment](tutorial:text-and-units) finds one of those in your own
site.

You may also meet the *em* unit. `1em` is measured against a font size
too, but not the root one. For `font-size`, it is measured against the
parent element's font size, and for other properties, such as
`padding`, against the element's own font size. So `em` sizes can
change from one part of a page to another, and `rem` sizes cannot. That
is one reason why many stylesheets, like your starter, use `rem` for most sizes.

## Text that lines up well

`text-align` changes how easy text is to read, as well as how it looks.

Newspapers often justify their columns. On the web, `justify` can leave
wide, uneven gaps between words, and these are worse in a narrow
column. Many readers, including many people with dyslexia, find those
gaps harder to read.

Centred text works well for a few short lines, like a heading, or the
short welcome in your site's hero section. In a long paragraph, each
line starts in a different place, so the eye has to search for the
start of every line. So most body text on the web is lined up on the
left.

## What we have now

We can now write a colour in several ways, read a contrast ratio, and
test a page the way a reader with bigger text sees it.

| Word | Meaning | Example |
|---|---|---|
| `rgb()` | Writes a colour as three amounts, for red, green and blue, from `0` to `255` | `rgb(51 102 153)` |
| `hsl()` | Writes a colour as a hue, a saturation and a lightness | `hsl(210 50% 40%)` |
| *alpha* | How solid a colour is, from `0` (see-through) to `1` (solid) | `rgba(0, 0, 0, 0.1)` |
| *contrast ratio* | Compares how light the text and its background are, from 1 to 1 up to 21 to 1 | 4.5 to 1 |
| *WCAG* | The Web Content Accessibility Guidelines. Level AA asks for 4.5 to 1 for ordinary text. | WCAG AA |
| *em* | A unit measured against a font size nearby, not the root one | `padding: 1em;` |

## Where to read more

Answer in Progress (2024). *how dark mode killed good design.*
<https://www.youtube.com/watch?v=Ieq5sNEoc1E>. Is light text on a dark
page easier to read? Sabrina Cruz looks at what research says about dark
mode, reading and tired eyes. About thirteen minutes.
