---
title: "One navigation bar across several pages — Practice"
practice_for: pages-and-navigation
year: "2026-2027"
version: 2026.09.22.1
---

# One navigation bar across several pages — Practice

On this page we practise the current-page marker: `aria-current="page"`
in the HTML, and an attribute selector in the CSS that makes it visible.
There are three kinds of problem:

- a broken page, where we find the mistake and fix it
- a small menu to build from a description
- a change in your own site, which you commit

Each problem has a folded answer. Some also have a hint, folded before
the answer. Try the problem first.

## Fix the broken page

**1.** This is the menu from a site's Gallery page. The author copied it
from the home page. Look at the heading under the menu, then look at
the menu.

```html site
id: nav-practice-copied-html
site: nav-practice-copied
<nav aria-label="Main">
  <ul>
    <li><a href="index.html" aria-current="page">Home</a></li>
    <li><a href="about.html">About</a></li>
    <li><a href="gallery.html">Gallery</a></li>
  </ul>
</nav>
<h1>Gallery</h1>
```

```css site
id: nav-practice-copied-css
site: nav-practice-copied
nav ul { display: flex; gap: 16px; list-style: none; }
nav a[aria-current="page"] { font-weight: bold; text-decoration: underline; }
```

Which page does the menu say we are on? Fix it.

<details class="dl-answer"><summary>answer</summary>

```html
<nav aria-label="Main">
  <ul>
    <li><a href="index.html">Home</a></li>
    <li><a href="about.html">About</a></li>
    <li><a href="gallery.html" aria-current="page">Gallery</a></li>
  </ul>
</nav>
<h1>Gallery</h1>
```

The menu said **Home**, because the marker was still on the Home link.
A screen reader would announce Home as the current page too. The marker
belongs on the link to the page we are on, so it moves to **Gallery**.
When we copy a menu onto a new page, this is the one edit it needs.

</details>

**2.** Here the marker is on the right link, but no link looks
different. The author wanted the current page's link in bold.

```html site
id: nav-practice-space-html
site: nav-practice-space
<nav aria-label="Main">
  <ul>
    <li><a href="index.html">Home</a></li>
    <li><a href="about.html" aria-current="page">About</a></li>
    <li><a href="gallery.html">Gallery</a></li>
  </ul>
</nav>
```

```css site
id: nav-practice-space-css
site: nav-practice-space
nav ul { display: flex; gap: 16px; list-style: none; }
nav a [aria-current="page"] { font-weight: bold; }
```

Look closely at the selector in the second rule. What is wrong with it?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Read the selector aloud, one part at a time. There are three parts,
   with a space between each.
2. On [Choosing what to style: selectors and
   classes](tutorial:selectors-and-classes) we met the descendant
   selector. A space between two parts means "inside". What does this
   selector look for inside each link?
3. Is there any element inside the About link? Or is the attribute on
   the link itself?

**Think about:** what is the difference between `a [aria-current]` and
`a[aria-current]`?

**Try this next:** once it works, what happens if we write
`nav [aria-current="page"]`, with no `a` at all?

</details>

<details class="dl-answer"><summary>answer</summary>

```css
nav a[aria-current="page"] { font-weight: bold; }
```

There was a space between `a` and `[aria-current="page"]`. A space in a
selector means "inside", so the rule looked for an element with the
attribute *inside* a link. There is none, so nothing matched. With no
space, the selector matches a link that has the attribute itself.

</details>

**3.** This menu comes from a Contact page. Two links look like the
current page.

```html site
id: nav-practice-two-html
site: nav-practice-two
<nav aria-label="Main">
  <ul>
    <li><a href="index.html" aria-current="page">Home</a></li>
    <li><a href="about.html">About</a></li>
    <li><a href="contact.html" aria-current="page">Contact</a></li>
  </ul>
</nav>
<h1>Contact</h1>
```

```css site
id: nav-practice-two-css
site: nav-practice-two
nav ul { display: flex; gap: 16px; list-style: none; }
nav a[aria-current="page"] { font-weight: bold; text-decoration: underline; }
```

How did this happen, do you think? Fix it.

<details class="dl-answer"><summary>answer</summary>

```html
<nav aria-label="Main">
  <ul>
    <li><a href="index.html">Home</a></li>
    <li><a href="about.html">About</a></li>
    <li><a href="contact.html" aria-current="page">Contact</a></li>
  </ul>
</nav>
<h1>Contact</h1>
```

The author copied the menu from the home page, then added the marker to
**Contact**, but did not take it off **Home**. To move the marker, we
make two edits: take it off one link, and put it on another. Only one
link on a
page should carry `aria-current="page"`.

</details>

## Make this

**4.** Style the current page's link in this menu:

- a `3px` solid line under it, in the colour `#0066cc`
- `4px` of space between the word and the line
- no underline on any link

Use an attribute selector, so the style follows the marker if it moves.

```html site
id: nav-practice-line-html
site: nav-practice-line
<nav aria-label="Main">
  <ul>
    <li><a href="index.html">Home</a></li>
    <li><a href="about.html" aria-current="page">About</a></li>
    <li><a href="gallery.html">Gallery</a></li>
  </ul>
</nav>
```

```css site
id: nav-practice-line-css
site: nav-practice-line
nav ul { display: flex; gap: 16px; list-style: none; }
/* your rules here */
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Which rule takes the underline off every link in the menu? Its
   selector is `nav a`.
2. Which rule adds the line under the current link only? Its selector
   is the attribute selector from the tutorial.
3. A line under a box is a bottom border. The space between the word
   and the border is bottom padding.

**Think about:** why is a border easier to control here than
`text-decoration: underline`?

**Try this next:** move `aria-current="page"` to **Gallery**. Does the
line move with it?

</details>

<details class="dl-answer"><summary>answer</summary>

```css
nav ul { display: flex; gap: 16px; list-style: none; }
nav a { text-decoration: none; }
nav a[aria-current="page"] {
  border-bottom: 3px solid #0066cc;
  padding-bottom: 4px;
}
```

`nav a` takes the underline off every link. The attribute selector then
adds a bottom border to the link that carries the marker, and the
padding sets the space above the line. A border lets us choose its
thickness, colour and distance from the text, which an underline does
not.

</details>

## In your own site

**5.** In your fork of `project_wad`, the `.main-nav a[aria-current="page"]`
rule in `styles.css` makes the current page's link bold. Bold alone can
be hard to see. Make the current page stand out more.

1. Find the rule. It is near the end of the part of `styles.css` headed
   "Header and navigation".
2. Add a bottom border to it, as in problem 4. You could use your
   accent colour: `var(--accent-color)`.
3. Save, and open each of your five pages in turn.
4. Commit the change, with a message such as "Underline the current
   page in the menu".

Does each page underline its own link, and only its own?

<details class="dl-answer"><summary>answer</summary>

One way to write it:

```css
.main-nav a[aria-current="page"] {
    font-weight: bold;
    border-bottom: 2px solid var(--accent-color);
    padding-bottom: 2px;
}
```

Every page links to the same `styles.css`, so this one rule styles the
marker on all five pages. If one page shows a line under the wrong link,
or under two links, the mistake is in that page's HTML. The marker is on
the wrong link, as in problems 1 and 3.

</details>
