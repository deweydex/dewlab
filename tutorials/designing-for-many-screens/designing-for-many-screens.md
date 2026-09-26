---
title: "Designing for many screens"
year: "2026-2027"
version: 2026.09.22.1
context_for: [media-queries, flexible-images]
---

# Designing for many screens

The same page may be read on a phone, a tablet, a laptop and a very wide
monitor. Two pages each show one tool for this: [Changing the layout for
phones: media queries](tutorial:media-queries) and [Images that shrink
to fit the screen](tutorial:flexible-images). This page looks at the
bigger picture. It is background reading. You do not need it to finish
those pages, but it can help you plan your own.

On this page we:

- see why a phone needs one line in the `<head>` before media queries work
- compare two ways to plan a stylesheet: small screens first, or large
  screens first
- think about where to put a breakpoint
- see why so many websites have a rule for every image

## The line that tells a phone its own width

Sometimes we might see a media query work in a desktop browser, and yet
never switch on for a real phone. Often the page is missing this
line in its `<head>`:

```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

This is the *viewport meta tag*. It tells a phone to lay the page out
at the phone's own width. Without it, a phone lays the page out as if
its screen were much wider, often about 980 pixels, then shrinks the
whole page to fit. The text looks tiny. And a `max-width` media query
for phones never switches on, because as far as the page can tell, the
viewport is 980 pixels wide.

![Two phones showing the same page. On the left, without the viewport line, the page is laid out about 980 pixels wide and then shrunk: three narrow columns of tiny text fill the screen. On the right, with the line, the page is laid out at the phone's own width: one column, with a header and text at a readable size.](viewport-meta.svg)

Why do phones do this? The first phone browsers met a web full of pages
made only for desktop screens. Laying those pages out wide and shrinking
them was the best they could do. A page that is made to fit a phone
says so with this line.

Your starter already has it. Near the top of both `index.html` and
`about.html`, the `<head>` holds a `<meta name="viewport" ...>` line,
with a comment beside it: "Without it, phones would display your site as
a tiny zoomed-out desktop page." Any new page you add needs the same
line.

## Small screens first, or large screens first?

There are two common ways to plan a stylesheet for many screens.

- *Desktop-first*: the ordinary rules are written for a wide screen.
  Media queries with `max-width` then change things for narrower
  screens.
- *Mobile-first*: the ordinary rules are written for a phone. Media
  queries with `min-width` then add to them for wider screens.

Your starter is desktop-first. Its ordinary rules are for a wide
screen, and at the bottom of `styles.css` there is a
`@media (max-width: 768px)` block, and then the `480px` one from
Exercise 24.

Here is a small page written mobile-first. The ordinary rules are for a
phone. Each media query adds a little more, from a wider width up.

```html site
id: mobile-first-html
site: mobile-first
<div class="page">
  <h1>Tentacular Plushies</h1>
  <p>Soft things with too many arms.</p>
</div>
```

```css site
id: mobile-first-css
site: mobile-first
.page { background: #f6f4f0; padding: 8px; font-family: sans-serif; }
h1 { font-size: 24px; }
@media (min-width: 400px) {
  .page { padding: 24px; }
  h1 { font-size: 32px; }
}
@media (min-width: 600px) {
  .page { max-width: 500px; margin: 0 auto; }
  h1 { font-size: 40px; }
}
```

1. Drag the **Preview width** slider from narrow to wide. How many
   times does the page change?
2. At 700 pixels, both media queries are true. Which heading size do we
   see?
3. What happens if we move the whole `600px` block above the `400px`
   block?

Now we can explain what we saw. The page changed twice, at 400 and at
600 pixels. At 700 pixels, both media queries match, and both set the
heading's `font-size`. The rule further down the stylesheet wins, so we
see `40px`. In step 3, the `400px` block came last, so its `32px` won
at every width from 400 pixels up, and the `40px` heading never showed.

So the order of media queries matters.

- In a mobile-first stylesheet, the `min-width` queries go from the
  smallest width to the largest.
- In a desktop-first stylesheet, the `max-width` queries go from the
  largest width to the smallest. That is why your starter's `768px`
  block comes before its `480px` block.

Which way is better? Many sites use each. Mobile-first has one
advantage. The phone's CSS is the simplest, and everything else is
added on top. Many websites now get
more visits from phones than from computers, so their designers often
start with the phone.

## Where to put a breakpoint

Where should a breakpoint go? A good way to decide is to watch the
content. Make the page narrow, then widen it slowly, the way we drag the
**Preview width** slider. When the page starts to look wrong, such as
lines of text that grow too long, or a row with too much empty space,
that width is a good place for a breakpoint.

It is tempting to pick breakpoints from a list of phones and tablets.
But screens come in many widths, and new ones arrive every year, so no
list stays complete. Round numbers such as `768px` and `480px`, the
ones in your starter, are common starting points. `768px` is about the
width of a tablet held upright, and `480px` is wider than most phones.
They are a starting point, not a rule.

Inside the inspector, device mode lets us try many widths quickly. It
has a list of sizes for well-known phones and tablets, and we can also
drag the page's edge to any width. When we select an element in the
**Elements** tab, most browsers show each rule that applies to it. A
rule that comes from a media query has its `@media` condition shown
right above it. That helps us see which media query is in use at the
width we are looking at.

Device mode is a good imitation of a phone, but it is not a phone. Once
your site is published, as on [Publishing your site with GitHub
Pages](tutorial:publish-it), it is worth opening it on a real phone too.

## Images on a narrow screen

A phone screen is often narrower than the photos we put on a page.
Without the two declarations from [Images that shrink to fit the
screen](tutorial:flexible-images), such a photo spills past the edge,
and the whole page can scroll sideways on a phone. So `max-width: 100%`
and `height: auto` appear on a great many websites, often in one rule
for every `img` on the page:

```css
img {
  max-width: 100%;
  height: auto;
}
```

A shrunk image still costs the same to download, though. The phone
fetches the whole file, then shows it small. [Images and file
size](tutorial:images-and-file-size) looks at how to keep image files
small.

## What we have now

We can now explain why a phone needs the viewport line, choose between
two ways to plan a stylesheet, and choose breakpoints by watching the
content.

| Word | Meaning | Example |
|---|---|---|
| *viewport meta tag* | A line in the `<head>` that tells a phone to lay the page out at its own width | `<meta name="viewport" content="width=device-width, initial-scale=1">` |
| *desktop-first* | Ordinary rules for a wide screen, then `max-width` media queries for narrower ones | your starter's `styles.css` |
| *mobile-first* | Ordinary rules for a phone, then `min-width` media queries that add to them for wider screens | `@media (min-width: 400px) { ... }` |

## Where to read more

Captain Disillusion (2019). *CD / Aspect Ratio.*
<https://www.youtube.com/watch?v=g5ZgUIobSj0>. Captain Disillusion
explains aspect ratio, the shape of a screen or a picture, and what
happens when the two do not match. Three minutes.
