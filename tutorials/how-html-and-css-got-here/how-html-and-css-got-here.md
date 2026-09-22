---
title: "How HTML and CSS got here"
year: "2026-2027"
version: 2026.09.22.1
context_for: [conclusions-and-next-steps]
---

# How HTML and CSS got here

The HTML and CSS you wrote in this course are about thirty years old.
They did not arrive finished. They grew, one version at a time, and
some of what they once had is gone. This page tells that story. It is
background reading for [Where to go next: beyond HTML and
CSS](tutorial:conclusions-and-next-steps). You do not need it to finish
that page, but it explains why the languages look the way they do.

On this page we:

- see where HTML came from, and how its versions followed each other
- see why CSS was needed, and how it grew
- see why browsers still understand tags nobody should use any more
- find out how to check whether a browser supports something new

## The first web pages

In 1989, Tim Berners-Lee worked at CERN, a physics laboratory near
Geneva. He proposed a way for the scientists there to share documents
between computers, with links from one document to another. That idea
became the World Wide Web.

He described the first version of HTML in 1991. It had about eighteen
tags. Many of them are still with us: headings from `<h1>` to `<h6>`,
`<p>` for a paragraph, `<ul>` and `<li>` for a list, and `<a>` for a
link. A page was a document, with structure and links, and very little
say over how it looked.

In 1994, Berners-Lee founded the *W3C*, the World Wide Web Consortium.
The W3C is a group that writes and publishes the standards for the web.
A *standard*, here, is a document that says exactly how a language
works, so that every browser can follow the same rules.

Here is the timeline of both languages, which the rest of this page
walks through:

![A timeline from 1990 to 2020, with two rows. The HTML row: the first HTML in 1991, HTML 2.0 in 1995, HTML 3.2 in 1997, HTML 4.01 in 1999, browser makers start the WHATWG in 2004, the first public draft of HTML5 in 2008, HTML5 an official standard in 2014, and one living standard in 2019. The CSS row: CSS1 in 1996, CSS2 in 1998, CSS2.1 in 2011, and after that separate modules, with Grid in every major browser in 2017.](timeline.svg)

## Versions of HTML

HTML came out in numbered versions for most of the 1990s:

| Year | HTML |
|---|---|
| 1995 | HTML 2.0, the first version treated as a real standard |
| 1997 | HTML 3.2 |
| 1999 | HTML 4.01 |
| 2004 | Progress had stalled for years, so a group of browser makers broke away to keep improving HTML on their own |
| 2008 | Their work, HTML5, appears as a public draft |
| 2014 | HTML5 becomes an official standard |

Why did progress stall? After HTML 4.01, the W3C worked on a stricter
kind of HTML, called XHTML. A page in XHTML had to follow every rule
exactly, or a browser could refuse to show it. Browser makers worried
that this would break too many real pages. In 2004, people from Apple,
Mozilla and Opera started their own group, the *WHATWG*, the Web
Hypertext Application Technology Working Group. The WHATWG kept
improving HTML, and added what web pages needed: `<video>` and
`<audio>`, new kinds of form field, and elements such as `<header>`,
`<nav>`, `<section>` and `<footer>`, which you used on every page of
your site.

Their work became HTML5. For some years, the W3C and the WHATWG each
published a version of it. Since 2019, they have agreed on one: the
WHATWG's. It is a *living standard*: a document that is updated as the
web changes. There is no HTML6 waiting to happen. HTML5 keeps growing
instead.

## Why CSS was needed

The first HTML had almost no way to say how a page should look. In the
mid-1990s, browser makers competed to add ways, and they did it inside
HTML. `<font>` set a typeface, a size and a colour. `<center>` centred
whatever was inside it. Here is a heading written that way:

```html
<center>
  <font face="Georgia" size="6" color="#8b0000">Hill Walks</font>
</center>
```

This worked, but it had two problems. First, the look was mixed in
with the content. To change the colour of every heading on a site, you
had to edit every heading, on every page. Second, the page said less
about its own structure. `<font>` says how some text looks, and nothing
about what it is. A screen reader or a search engine learns nothing
from it.

CSS was the answer. Håkon Wium Lie proposed it in 1994, while he was
also working at CERN. The idea is the one you have used all through
this course: HTML says what each part of a page *is*, and CSS says how
it *looks*, from one separate file. The same heading, the way you would
write it now:

```html
<h1>Hill Walks</h1>
```

```css
h1 {
  text-align: center;
  font-family: Georgia, serif;
  color: #8b0000;
}
```

One rule in `styles.css` now styles every `<h1>` on every page. That is
why your five pages share one stylesheet.

## Versions of CSS

CSS has a shorter, steadier history:

| Year | CSS |
|---|---|
| 1996 | CSS1: colours, fonts and basic backgrounds |
| 1998 | CSS2 adds positioning, the same `position` property we met on [A header that stays in view as you scroll](tutorial:position-and-the-sticky-header) |
| 2011 | CSS2.1 tidies up differences between browsers |

After CSS2.1, CSS stopped coming out as one single specification. CSS3
split into many separate *modules*, each developed, tested and released
on its own schedule. Flexbox and grid are two of them. Colours,
selectors, media queries and animations are others.

Why split it up? A single, huge standard can only be finished when
every part of it is finished. With modules, a small, ready part does
not have to wait for a large, difficult one. So "CSS3" was never one
single thing. Each module moves at its own pace. Grid, for example, took many years of work. It arrived in all the
major browsers in 2017, and since then it has been safe to use on a
real site.

## Old tags that still work

A *deprecated* tag or property is one that browsers still understand,
but the standard no longer recommends. Usually CSS took over its job.
`<center>` and `<font>` are the best-known examples. The current HTML
standard calls them *obsolete*, and says that authors must not use
them.

So why do they still work? Millions of old pages use them, and many of
those pages are still online. If browsers stopped showing them, those
pages would break, and nobody would fix them. So the standard does two
things at once. It tells authors not to use these tags, and it tells
browsers exactly how to show them anyway.

Sometimes we might open an old page's source and see `<font>`,
`<center>`, or a `bgcolor` attribute on the `<body>`. Now we know what
we are looking at: a page from before CSS took over. The W3C's HTML
checker, at [validator.w3.org](https://validator.w3.org), reports these
tags as errors, and says to use CSS instead.

## Is it safe to use yet?

New CSS arrives all the time, one module at a time. How do we know
whether our visitors' browsers understand it? Two places answer that
question:

- **MDN Web Docs**, at
  [developer.mozilla.org](https://developer.mozilla.org), has a page for
  every HTML element and CSS property. Near the end of each page, a
  table shows which browsers support it, and from which version.
- **Can I use**, at [caniuse.com](https://caniuse.com), shows the same
  kind of information as a chart, and says roughly what share of people
  use a browser that supports it.

*Browser compatibility* is whether a feature works the same way in
every browser a site's visitors use. Everything in this course, Flexbox
and grid included, works in every current major browser. With something
newer, it is worth a look at one of these two sites before we rely on
it.

## What we have now

We can now tell the story of HTML and CSS: where each began, how their
versions followed each other, and why some old tags still work.

| Word | Meaning | Example |
|---|---|---|
| *W3C* | The World Wide Web Consortium: a group that writes and publishes web standards | the CSS standards |
| *standard* | A document that says exactly how a language works, so every browser can follow the same rules | HTML 4.01 |
| *WHATWG* | A group started by browser makers in 2004. It now looks after the HTML standard. | the HTML living standard |
| *living standard* | A standard that is updated as the web changes, with no new numbered version | HTML5 |
| *module* | One separate part of CSS, released on its own schedule | Flexbox, grid |
| *deprecated* | Still understood by browsers, but no longer recommended, usually because CSS replaced it | `<center>`, `<font>` |
| *browser compatibility* | Whether a feature works the same way in every browser a site's visitors use | checking Grid on caniuse.com |
