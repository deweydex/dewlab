---
title: "Headings, paragraphs and emphasis"
slug: headings-and-emphasis
module: web
module_title: "Web authoring"
series: first-site
version: 2026.09.04.1
---

# Headings, paragraphs and emphasis

A page's main heading and a heading over one small section are not the
same size, and they should not be. Try the page below, then change the
`<h2>` to an `<h1>` and see what shifts.

```html site=headings
<h1>My Portfolio</h1>
<p>Welcome. I am a <strong>developer</strong> and I love
<em>learning</em> new things.</p>
<h2>What I'm Learning</h2>
<p>A smaller heading for a smaller section.</p>
```

## Why this happens

`<h1>` through `<h6>` are heading levels. `<h1>` marks a page's one main
heading. `<h2>` marks a heading for a section beneath it, and so on down
the levels. Browsers usually make each level smaller than the one before
it, though CSS can change how they look.

`<p>` marks a paragraph of ordinary text.

Inside a paragraph, two tags mark words that matter more than the rest.
`<strong>` marks something important; `<em>` marks something emphasised.
Browsers usually show these as bold and italic, but the tags carry a
meaning beyond how they look. `<b>` and `<i>` often look the same as
`<strong>` and `<em>`, but they mean nothing extra to a screen reader or a
search engine. `<strong>` and `<em>` do.

## Your turn

Let's open your fork and find the paragraph below your `<h1>`, marked
with `class="hero-text"`. Try rewriting it in your own words: who you
are, what you are working on, what interests you. A few sentences is
enough.

Then try wrapping one important word or phrase in `<strong>` tags, and
something you want to emphasise in `<em>` tags. Save and refresh to see
them appear on the page.

## What you have now

Text broken into headings at the right level, paragraphs, and words marked
as important or emphasised.

- **Heading level** — `<h1>` for a page's main heading, `<h2>` and below
  for the sections under it.
- **`<strong>`** — marks text as important.
- **`<em>`** — marks text as emphasised.
