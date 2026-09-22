---
title: "A footer that sits at the bottom of a short page"
year: "2026-2027"
version: 2026.09.22.1
covers:
  why-does-this-happen:
    covers: [WA-LO9]
  now-in-your-own-site:
    touches: [WA-LO9]
---

# A footer that sits at the bottom of a short page

A page with very little on it leaves empty space in the window. Where
should its footer go: right under the text, or at the very bottom? On
this page we:

- keep a footer at the bottom of a short page
- see the three rules that work together to do it
- find the same rules in your own site

This page uses `display: flex`, which the course teaches properly later,
in [Lining boxes up in a row with Flexbox](tutorial:flexbox-first-steps).

## Let's try it

The example is a very short page: one paragraph, and a footer.

```html site
id: footer-push-html
site: footer-push
<p>Just a little content.</p>
<footer>Footer</footer>
```

```css site
id: footer-push-css
site: footer-push
html, body { height: 100%; margin: 0; }
body { display: flex; flex-direction: column; }
footer {
  margin-top: auto;
  background: #2c3e50;
  color: white;
  padding: 10px;
}
```

1. Where does the dark footer bar sit in the preview? Is it right under
   the text, or somewhere else?
2. What happens if we delete `margin-top: auto;` from the `footer` rule?
3. Put it back. Now change `height: 100%` to `height: auto` in the first
   rule. Where does the footer go this time?

## Why does this happen?

Now we can explain what we saw. The page has almost no content, and yet
the footer sits at the very bottom of the preview, not right under the
text. Here is the same short page, drawn twice:

![Two browser windows showing the same short page: one line of text, "Just a little content.", and a dark footer bar. On the left, without margin-top: auto, the footer sits right under the text, and the rest of the window below it is empty. On the right, with margin-top: auto, the footer sits at the bottom of the window, and the empty space between the text and the footer is shaded and labelled "margin-top: auto takes the leftover space".](footer-pushed-down.svg)

Three rules work together to do this:

- `html, body { height: 100%; }` makes the page's body as tall as the
  preview. With `height: auto` in step 3, the body was only as tall as
  its content, so there was no empty space for the footer to move into.
- `body { display: flex; flex-direction: column; }` stacks the body's
  children from top to bottom, and lets them share out the space inside
  it.
- `margin-top: auto` on the footer takes all the leftover space above
  it. However little content comes before the footer, this pushes the
  footer itself down to the bottom of the page. In step 2, without it,
  the footer moved up under the text.

This is a close relative of the auto margins on [A readable width,
centred on the page](tutorial:the-container). There, auto margins shared
out the space beside a box. Here, one auto margin takes the space above
the footer.

Oftentimes, when `margin-top: auto` seems to do nothing, the parent
element is missing `display: flex`. On an ordinary page, a top margin
set to `auto` counts as `0`.

## Now in your own site

Your own site uses the same idea, with one small difference. Your home
page has a lot of content, so to see the footer move we first make the
page short for a moment, in [Looking inside a page with the inspector](tutorial:the-inspector).

1. In your fork, open `styles.css` and find the `body` rule. It sets
   `display: flex` and `flex-direction: column`, the same as our
   example.
2. The same rule sets `min-height: 100vh` in place of `height: 100%`.
   `100vh` is the full height of the browser window. So the body is
   always at least as tall as the window, and it can still grow when
   there is more content.
3. Find the `footer` rule. It has `margin-top: auto`.
4. Open your home page in the browser, and open the inspector. In the
   **Elements** tab, click the line that starts `<main`, and press the
   **Delete** key. The page's main content disappears, in your browser
   only. Where does the footer sit now?
5. In `styles.css`, delete `margin-top: auto;` from the `footer` rule,
   and save.
6. Refresh the page. The refresh brings the main content back, so
   delete the `<main` line in the inspector again. Where is the footer
   this time?
7. Put `margin-top: auto;` back, and save.

Refresh, and delete the `<main` line one last time. Is your footer back
at the bottom of the window?

## What we have now

We can now keep a footer at the bottom of a page, however little content
sits above it.

| Word | Meaning | Example |
|---|---|---|
| `margin-top: auto` | On a child of a `display: flex` element, takes all the leftover space above it, pushing the element itself to the far side | `margin-top: auto;` |
| `vh` | A unit for heights. `100vh` is the full height of the browser window. | `min-height: 100vh;` |
