---
title: "A rule, and where it lives"
year: "2026-2027"
version: 2026.09.11.1
covers:
  how-it-works:
    covers: [WA-LO9]
    touches: [WA-LO2]
---

# A rule, and where it lives

HTML says what each part of a page *is*. CSS says how it should *look*.
On this page you:

- write a CSS rule and name its three parts
- find where the rules for your own site are kept

## Try it

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

1. In the CSS, change `darkslateblue` to `firebrick`. Both paragraphs
   change colour.
2. Look at the HTML again. Neither paragraph says anything about colour.
   So how did both of them change?

## How it works

The code in the CSS box is one *rule*. A rule has two parts:

```css
p {                      /* selector: which elements to style */
  color: darkslateblue;  /* declaration: property and value   */
}
```

- The *selector* comes first. It says which elements the rule styles.
  The selector `p` means "every paragraph".
- Inside the curly braces come one or more *declarations*. Each
  declaration is a property, a colon, a value, and a semicolon. Here the
  property is `color` and the value is `darkslateblue`.

This is the answer to the question above. The HTML does not mention
colour, because the CSS rule selects every `<p>` and colours all of them.
One rule can style many elements.

### Where rules live

On a real site, CSS rules are usually kept in their own file, called a
*stylesheet*. In your site, that file is `styles.css`.

The HTML page loads the stylesheet with a `<link>` tag in its `<head>`:

```html
<link rel="stylesheet" href="styles.css">
```

Every page that has this line uses the same rules. That is why
`index.html` and `about.html` look alike, even though the CSS is only
written once.

## In your own site

1. Open `index.html`. Find the `<link>` tag in the `<head>`.
2. Open `about.html`. Find the same `<link>` tag there.
3. Open `styles.css`. Scroll through it. The comments, between `/*` and
   `*/`, explain what each section does. You do not need to understand
   all of it yet.

## Summary

| Word | Meaning | Example |
|---|---|---|
| *rule* | A selector plus one or more declarations | `p { color: firebrick; }` |
| *selector* | Says which elements a rule styles | `p` |
| *declaration* | A property and a value, inside the braces | `color: firebrick;` |
| *stylesheet* | A file of CSS rules, loaded by a `<link>` tag | `styles.css` |
