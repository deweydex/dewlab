---
title: "CSS rules and stylesheets"
year: "2026-2027"
version: 2026.09.11.1
covers:
  why-does-this-happen:
    covers: [WA-LO9]
    touches: [WA-LO2]
---

# CSS rules and stylesheets

HTML says what each part of a page *is*. CSS says how it should *look*.
On this page we:

- change one line of CSS, and see what it reaches
- name the parts of a CSS rule
- find where the rules for your own site are kept

## Let's try it

The HTML below has two paragraphs. The CSS under it has one rule.

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

1. What happens if we change `darkslateblue` to `firebrick`? How many
   paragraphs change colour?
2. Look at the HTML again. Does either paragraph mention colour at
   all?

So how did both of them change, together, from one line?

## Why does this happen?

The code in the CSS box is one *rule*. Let's label its parts:

```css
p {                      /* selector: which elements to style */
  color: darkslateblue;  /* declaration: a property and a value */
}
```

- A *selector* says which elements to style. The selector `p` matches
  every paragraph.
- Inside the curly braces after it come one or more *declarations*.
  Each declaration is a property and a value. Here the property is
  `color` and the value is `darkslateblue`.

That answers our question. The HTML never mentions colour, because the
rule selects every `<p>` and sets the `color` of each one.

### Where rules live

A rule usually lives in its own file, not inside the HTML file it
styles. In your site that file is `styles.css`. A file of CSS rules like
this is called a *stylesheet*. A `<link>` tag in the `<head>` of the
page connects the two:

```html
<link rel="stylesheet" href="styles.css">
```

The `href` names the file to load. `rel="stylesheet"` tells the browser
that the file holds CSS rules.

Why keep the rules in a file of their own? One stylesheet can style many
pages at once. That is why `index.html` and `about.html` look consistent
without repeating any CSS.

![Two page files, index.html and about.html, side by side. Each has a link tag in its head, and an arrow runs from each link tag down to one shared file, styles.css. Inside styles.css is the rule p with color darkslateblue, so this one rule styles the paragraphs on both pages.](one-stylesheet-two-pages.svg)

## Now in your own site

1. In your fork, open `index.html`. Can you find the `<link>` tag in
   its `<head>`?
2. Can you find the same tag in `about.html`?
3. Now we can open `styles.css` itself and scroll through it. It has many
   comments, between `/*` and `*/`, explaining what each section does.
   Browse them whenever you are curious.

## What we have now

We can now follow a rule from the page it styles to the file it lives
in.

| Word | Meaning | Example |
|---|---|---|
| *rule* | A selector plus one or more declarations | `p { color: firebrick; }` |
| *selector* | The part of a rule saying which elements to style | `p` |
| *declaration* | A property and a value, inside a rule's braces | `color: firebrick;` |
| *stylesheet* | A file of CSS rules, linked from the `<head>` | `styles.css` |
