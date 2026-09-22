---
title: "Choosing what to style: selectors and classes"
year: "2026-2027"
version: 2026.09.11.1
covers:
  why-does-this-happen:
    covers: [WA-LO9]
  now-in-your-own-site:
    touches: [WA-LO9]
---

# Choosing what to style: selectors and classes

So far, a selector like `p` has styled every paragraph on a page. What
if we want to style only some of them? On this page we:

- style one part of a page and leave the rest alone
- learn two kinds of selector: the class selector and the descendant
  selector
- give the skills section in your own site a style of its own

## Let's try it

The HTML below has two paragraphs. One sits inside a `<div>` with
`class="highlight"`, and one sits outside it. The CSS has one rule.

```html site
id: selectors-html
site: selectors
<div class="highlight">
  <p>Inside the highlighted box.</p>
</div>
<p>Outside it.</p>
```

```css site
id: selectors-css
site: selectors
.highlight p {
  color: firebrick;
  font-weight: bold;
}
```

1. Both paragraphs are `<p>` elements. Do both of them turn red?
2. Move `<p>Outside it.</p>` up, so it sits inside the `<div>`, just
   after the first paragraph. What happens to it?
3. Put it back. Now change the selector from `.highlight p` to plain
   `p`. Which paragraphs are styled now?

## Why does this happen?

The selector `.highlight p` has two parts, joined by a space.

```css
.highlight p {    /* a <p> that is somewhere inside class="highlight" */
  color: firebrick;
}
```

- `.highlight` is a *class selector*. A class selector is a dot and a
  class name. It matches every element that carries that class, such as
  `class="highlight"`, wherever it sits on the page.
- `.highlight p` is a *descendant selector*. A descendant selector is
  two selectors joined by a space. It matches an element only when it
  sits somewhere inside an element that matches the first selector.

Now we can explain what we saw. The paragraph inside the box sits inside
an element with `class="highlight"`, so the rule matches it. The
paragraph outside the box has no such element around it, so it stays
untouched. When we moved it inside, it matched too. With plain `p`, the
rule matched every paragraph.

![The HTML of the example drawn as a tree. At the top is body. Under it are two branches: a div with class highlight, and a p that says Outside it. Under the div is a p that says Inside the highlighted box. That inner p is shaded and marked as matched by .highlight p, because the highlight div is above it. The outer p is not shaded, because no element with class highlight is above it.](descendant-tree.svg)

"Somewhere inside" means at any depth. The `<p>` does not have to sit
directly inside the `.highlight` element. It could be inside a
`<section>` that is inside it, and it would still match.

An element can also carry more than one class, with spaces between the
names. You have met this already: your skills section has
`class="section skills-section"`. That element matches both `.section`
and `.skills-section`.

## Now in your own site

On an earlier page you added a skills section to your fork. Now we can
style that section on its own. The starter already holds two rules for
it, inside a comment, so they do nothing yet.

1. Open `styles.css`, and find section 7, Sections & Cards.
2. Find the comment that starts `/* → Exercise 18`. Under it are these
   two rules:

```css
.skills-section {
    background-color: var(--light-gray);
}

.skills-section .card {
    border-left: 4px solid var(--accent-color);
}
```

3. Delete the comment's first line, the one that starts
   `/* → Exercise 18`. Then delete the `*/` line just after the two
   rules. Now the two rules are no longer inside a comment.
4. Save, and refresh. Which cards have a border on the left?

The border shows up only on cards inside the skills section, because
`.skills-section .card` is a descendant selector.

5. For a moment, change `.skills-section .card` to plain `.card`. Which
   other cards on the page pick up the same border?
6. Change it back when you have looked.

## What we have now

We can now style one part of a page without touching the rest of it.

| Word | Meaning | Example |
|---|---|---|
| *class selector* | A dot and a class name. It matches every element that carries that class. | `.highlight` |
| *descendant selector* | Two selectors joined by a space. It matches an element nested anywhere inside another. | `.highlight p` |
