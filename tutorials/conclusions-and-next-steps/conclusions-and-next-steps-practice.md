---
title: "Where to go next: beyond HTML and CSS — Practice"
practice_for: conclusions-and-next-steps
year: "2026-2027"
version: 2026.09.22.1
---

# Where to go next: beyond HTML and CSS — Practice

On this page we practise reading older HTML, and building by hand the
kind of page a template tool builds for us. There are three kinds of
problem:

- an old page, where we replace deprecated tags with CSS
- a small page to build from a description
- a check on your own site, which you commit

Each problem has a folded answer. Some also have a hint, folded before
the answer. Try the problem first.

## Fix the broken page

**1.** This page was written in the 1990s. It still works, but it uses
two deprecated tags: `<center>` and `<font>`. Rewrite it with no
deprecated tags, so that it looks the same.

```html site
id: next-practice-font-html
site: next-practice-font
<center>
  <font face="Georgia" color="#8b0000" size="6">Hill Walks</font>
  <p><font face="Arial" color="#555555">Short walks near Galway</font></p>
</center>
```

```css site
id: next-practice-font-css
site: next-practice-font
/* nothing here yet: in the 1990s, the HTML did all the styling */
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. What is "Hill Walks"? Which HTML element says that it is the page's
   main heading?
2. Which CSS property centres text? Which one sets a typeface? Which
   one sets a colour?
3. `size="6"` is the second-largest of the seven `<font>` sizes. In
   most browsers it is `2em`, twice the normal text size.

**Think about:** the old version says how the heading looks. What does
the new version say that the old one did not?

**Try this next:** add a second page's worth of headings to the HTML.
In which version would it be quicker to change the colour of every
heading?

</details>

<details class="dl-answer"><summary>answer</summary>

```html
<h1>Hill Walks</h1>
<p class="tagline">Short walks near Galway</p>
```

```css
h1, .tagline { text-align: center; }
h1 {
  font-family: Georgia, serif;
  font-weight: normal;
  font-size: 2em;
  color: #8b0000;
}
.tagline { font-family: Arial, sans-serif; color: #555555; }
```

`<center>` becomes `text-align: center`. Each `<font>` becomes CSS: its
`face` becomes `font-family`, its `color` becomes `color`, and its
`size` becomes `font-size`. The heading is now an `<h1>`, so the page
says what the text *is* as well as how it looks. An `<h1>` is bold by
default, and the old heading was not, so `font-weight: normal` keeps
the look the same. One small difference remains: an `<h1>` has a margin
above it, so the new heading sits a little lower. `margin-top: 0` on
the `h1` removes it.

</details>

**2.** This page shows a sale price, the old way. It uses two more tags
that are now obsolete: `<big>`, which made text bigger, and `<strike>`,
which drew a line through it.

```html site
id: next-practice-strike-html
site: next-practice-strike
<p>Walking boots: <strike>€90</strike> <big>€65</big></p>
```

```css site
id: next-practice-strike-css
site: next-practice-strike
p { font-family: Arial, sans-serif; }
```

Rewrite it with no obsolete tags. The old price should still have a
line through it, and the new price should still be bigger.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. HTML still has an element for text that is no longer accurate: `<s>`.
   A price that has changed is a good example.
2. For the new price, which element marks some text as important? We
   met it on [Headings, paragraphs and
   emphasis](tutorial:headings-and-emphasis).
3. Which CSS property makes the new price bigger?

**Think about:** `<big>` said how the price looks. What could the HTML
say about the new price instead?

**Try this next:** take the `<s>` out, and use a `<span>` with a class.
Which CSS property draws the line through the text?

</details>

<details class="dl-answer"><summary>answer</summary>

```html
<p>Walking boots: <s>€90</s> <strong class="price">€65</strong></p>
```

```css
p { font-family: Arial, sans-serif; }
.price { font-size: 1.2em; }
```

`<s>` is the current element for text that is no longer accurate, such
as an old price. It draws a line through the text by default. `<big>`
only made text bigger, and said nothing about why. `<strong>` says the
new price is important, and a class lets CSS set its size. The line
through the text is `text-decoration: line-through` in CSS, if you ever
need it without `<s>`.

</details>

## Make this

**3.** Carrd builds a one-page "business card" from a template. Build
one by hand:

- a white card, never wider than `320px`, in the middle of the grey
  page
- your name as the heading, and one line about you under it
- two links, side by side in the middle, with a gap between them
- everything in the card centred

```html site
id: next-practice-card-html
site: next-practice-card
<!-- your card here -->
```

```css site
id: next-practice-card-css
site: next-practice-card
body { background: #ddd; font-family: Arial, sans-serif; }
/* your rules here */
```

How long did it take? Could a template have done anything you could
not?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Start with the HTML: a `<div>` for the card, with a heading, a
   paragraph and two links inside it.
2. `max-width` and `margin: 0 auto` keep a box narrow and in the middle,
   as on [A readable width, centred on the
   page](tutorial:the-container).
3. Put the two links in their own `<div>`, and make it a flex
   container. `justify-content: center` puts the items of a flex row in
   the middle.

**Think about:** which parts of the card came from earlier pages in
this course?

**Try this next:** add a media query that makes the card fill the
whole width below `400px`.

</details>

<details class="dl-answer"><summary>answer</summary>

One way to build it:

```html
<div class="card">
  <h1>Ana Murphy</h1>
  <p>I build small websites for local clubs.</p>
  <div class="links">
    <a href="#">My work</a>
    <a href="#">Email me</a>
  </div>
</div>
```

```css
body { background: #ddd; font-family: Arial, sans-serif; }
.card {
  max-width: 320px;
  margin: 2rem auto;
  padding: 16px;
  background: white;
  border-radius: 6px;
  text-align: center;
}
.links { display: flex; justify-content: center; gap: 16px; }
```

Every part comes from an earlier page: a container with auto margins,
padding, a flex row with a gap, and `text-align`. A template would do
it faster. By hand, every spacing and colour is your choice, and
nothing is outside what you can change.

</details>

## In your own site

**4.** Check your own pages with the W3C's HTML checker. It reports
deprecated tags, and other mistakes too.

1. Open [validator.w3.org](https://validator.w3.org).
2. Choose **Validate by URI**, and paste in the address of one of your
   published pages. Press **Check**.
3. Read each error. The checker gives a line number for each one.
4. Fix the errors in your own copy of the page. Save, commit, and wait
   a minute for your site to update.
5. Check the page again. Then do the same for your other four pages.
6. In your README, under **Testing**, set **Validated with the W3C
   validators?** to "yes" for HTML.

Does every page now say "No errors or warnings to show"?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. If you have not published your site yet, choose **Validate by
   Direct Input** instead, and paste in the whole of one HTML file.
2. Fix the first error first. One mistake, such as a missing closing
   tag, can cause several errors further down.
3. An error that names an element as "obsolete" means a deprecated
   tag. The message says to use CSS instead.

**Think about:** what does each error tell you about the line it
points at?

**Try this next:** the W3C also has a CSS checker, at
[jigsaw.w3.org/css-validator](https://jigsaw.w3.org/css-validator/).
Check your `styles.css` there too.

</details>

<details class="dl-answer"><summary>answer</summary>

The starter's pages have no deprecated tags, so a page you have not
changed much may already pass. Common errors in a student's own pages
are a missing `alt` on an `<img>`, a closing tag that is missing or in
the wrong place, and an `id` used twice on one page. If you pasted in
an old snippet from the web, you may also see an element such as
`<center>` or `<font>` named as obsolete. Replace it with CSS, as in
problem 1.

</details>
