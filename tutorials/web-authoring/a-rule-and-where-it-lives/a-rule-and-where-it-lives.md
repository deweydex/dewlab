---
title: "A rule, and where it lives"
slug: a-rule-and-where-it-lives
module: web-authoring
module_title: "Web Authoring"
year: "2026-2027"
series: first-site
version: 2026.09.11.1
---

# A rule, and where it lives

Try changing one line below and both paragraphs change colour, not just
one. Neither paragraph mentions colour at all.

```html site
id: rule-html
site: rule
<p>First paragraph.</p>
<p>Second paragraph.</p>
```

```css site
id: rule-css
site: rule
p {
  color: darkslateblue;
}
```

Try `firebrick` instead. Both change again, together.

## Why this happens

A CSS *rule* has two parts. A *selector* says which elements to style.
Inside curly braces after it come one or more *declarations*, each a
property and a value. `p { color: darkslateblue; }` is one rule: the
selector `p` matches every paragraph, and the declaration sets each one's
`color`.

A rule lives in `styles.css`, a separate file, not inside the HTML file it
styles. A `<link>` tag in the `<head>` connects the two:

```html
<link rel="stylesheet" href="styles.css">
```

One stylesheet can style many pages at once, which is why `index.html` and
`about.html` look consistent without repeating any CSS.

## Your turn

Let's open your fork and find that `<link>` tag in the `<head>` of both
`index.html` and `about.html`. Then try opening `styles.css` itself and
scrolling through it. It has many comments explaining what each section
does; browse them when you are curious.

## What you have now

A rule traced from the page it styles to the file it actually lives in.

A *selector* is the part of a rule saying which elements to style. A
*declaration* is a property and a value, inside a rule's braces. A
*rule* is a selector plus one or more declarations.
