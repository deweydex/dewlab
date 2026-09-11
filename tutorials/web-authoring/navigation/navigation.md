---
title: "Navigation"
slug: navigation
module: web-authoring
module_title: "Web Authoring"
year: "2026-2027"
series: first-site
version: 2026.09.11.1
covers:
  why-this-happens:
    covers: [WA-LO2]
  your-turn:
    touches: [WA-LO8]
---

# Navigation

Click the link below. The page jumps straight to the section further
down, without reloading.

```html site
id: nav-demo-html
site: nav-demo
<nav aria-label="Page">
  <ul>
    <li><a href="#one">Section one</a></li>
    <li><a href="#two">Section two</a></li>
  </ul>
</nav>
<section id="one">
  <h2>Section one</h2>
  <p>You started here.</p>
</section>
<section id="two" style="margin-top:400px">
  <h2>Section two</h2>
  <p>And now you are here.</p>
</section>
```

## Why this happens

`<nav>` wraps a set of links to other places, on this page or elsewhere.
Because it is a semantic tag, a screen reader can announce "navigation"
when it reaches one.

A link whose `href` starts with `#` instead of a filename is an *anchor
link*. `#two` points at whichever element on the same page has `id="two"`.
When you click it, the browser scrolls straight there instead of loading
a new page.

`aria-label="Page"` gives the `<nav>` a name a screen reader can read out,
such as "Page navigation" rather than only "navigation". This matters once
a page has more than one `<nav>` on it.

## Your turn

Let's open your fork and find the `<nav>` element in the header. Try
updating its links to point at your sections, reusing the `id`s you
already added:

```html
<nav class="main-nav" aria-label="Main">
    <ul>
        <li><a href="index.html">Home</a></li>
        <li><a href="about.html">About</a></li>
        <li><a href="#skills">Skills</a></li>
        <li><a href="#contact">Contact</a></li>
    </ul>
</nav>
```

Save and refresh, then try clicking the Skills link. The page should
scroll smoothly there. Look in `styles.css` for `scroll-behavior: smooth`,
which is what creates that. The links in this nav sit in a row rather than a
column; [Flexbox first steps](tutorial:flexbox-first-steps) explains why
once you reach it.

## What you have now

A working set of links inside a tag that says what it is.

`<nav>` is a semantic tag wrapping a set of links. An *anchor link* is an
`href` starting with `#`, jumping to a matching `id` on the same page.
`aria-label` names an element for a screen reader to read out.
