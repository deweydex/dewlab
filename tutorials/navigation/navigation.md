---
title: "Navigation"
year: "2026-2027"
version: 2026.09.11.1
covers:
  why-does-this-happen:
    covers: [WA-LO2]
  now-in-your-own-site:
    touches: [WA-LO8]
---

# Navigation

On the last page, a link took us to another page, or to another site.
Can a link also take us to a place further down the same page? On this
page we:

- try a menu whose links jump within one page
- learn what `<nav>`, `href="#..."` and `aria-label` each do
- point the menu in your own site at your own sections

## Let's try it

The box below has a small menu with two links, and two sections under
it. The second section starts a long way down.

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

1. Look at the `href` on each link. How is it different from the links
   on the last page?
2. Click **Section two** in the preview. Where does it take you? Does
   the page reload?
3. Can you find `two` anywhere else in the code?

## Why does this happen?

Now we can explain what we saw.

- An *anchor link* is a link whose `href` starts with `#`, in place of a
  filename. `#two` points at the element on the same page that has
  `id="two"`. When we click it, the browser scrolls straight there. It
  does not load a new page.
- `<nav>` is a semantic tag. It wraps a set of links to other places, on
  this page or elsewhere. Because it names what it holds, a screen
  reader can announce "navigation" when it reaches one.
- `aria-label` is an attribute that gives an element a name for a screen
  reader to read out. With `aria-label="Page"`, a screen reader can say
  "Page navigation", not only "navigation". This matters once a page has
  more than one `<nav>` on it.
- Inside the `<nav>`, the links sit in a list. `<ul>` is a list, and
  each `<li>` is one item in it. Most menus on the web are built this
  way.

Here are the two halves of an anchor link side by side:

```html
<a href="#two">Section two</a>   <!-- the link: # and a name -->
<section id="two">...</section>  <!-- the target: the same name in id -->
```

Oftentimes, when an anchor link does nothing, the two names do not
match. `#Two` and `id="two"` are different names, because the match is
exact, capital letters included. An `id` must also appear only once on a
page, so the browser knows which element to scroll to.

Sometimes we might notice that, after clicking an anchor link, the web
address in the browser's address bar ends with the `#` part, such as
`#contact`. We can copy that full address and share it. Whoever opens
it lands on that same section.

## Now in your own site

The `id`s you added on earlier pages now get used: `id="skills"` on
your skills section, and `id="contact"` on your contact section.

1. In your fork, open `index.html`.
2. Find the `<nav>` element in the header.
3. Update its links so they point at your sections:

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

4. Save, and refresh.
5. Click the **Skills** link. What does the page do?

The page should scroll smoothly down to your skills section. The smooth
movement comes from `scroll-behavior: smooth` in `styles.css`. Can you
find it there?

You might also notice that the links in this menu sit in a row, not in a
column. [Flexbox first steps](tutorial:flexbox-first-steps) explains why,
once you reach it.

## What we have now

We can now build a set of links inside a tag that says what it is, and
jump to any part of a page.

| Word | Meaning | Example |
|---|---|---|
| `<nav>` | A semantic tag that wraps a set of links | `<nav aria-label="Main">` |
| *anchor link* | A link whose `href` starts with `#`. It jumps to the element with the matching `id` on the same page. | `<a href="#skills">` |
| `aria-label` | An attribute that names an element for a screen reader to read out | `aria-label="Main"` |
