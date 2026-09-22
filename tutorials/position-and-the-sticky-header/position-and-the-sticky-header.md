---
title: "Position, and the sticky header"
year: "2026-2027"
version: 2026.09.11.1
covers:
  why-does-this-happen:
    covers: [WA-LO9]
  and-the-footer:
    covers: [WA-LO9]
  now-in-your-own-site:
    touches: [WA-LO9]
---

# Position, and the sticky header

On a long page, how do we keep the header in view while everything else
scrolls? On this page we:

- make a header bar stay at the top as we scroll
- compare the values of the `position` property
- keep a footer at the bottom of a short page

## Let's try it

The HTML has a header bar and five sections. The CSS gives the bar a
dark background, and gives each section a height of `100px`, so the
preview has something to scroll.

```html site
id: sticky-html
site: sticky
<div class="header">I stay in view</div>
<p>Section one. Scroll to see what happens.</p>
<p>Section two.</p>
<p>Section three.</p>
<p>Section four.</p>
<p>Section five.</p>
```

```css site
id: sticky-css
site: sticky
.header {
  position: sticky;
  top: 0;
  background: #2c3e50;
  color: white;
  padding: 10px;
  margin: 0;
}
p { height: 100px; margin: 0; padding: 10px; border-bottom: 1px solid #ccc; }
```

1. Scroll the preview down. What happens to the sections? What happens
   to the dark bar?
2. What happens if we delete the line `top: 0;` and scroll again?
3. Put the line back, and change it to `top: 20px;`. Where does the bar
   stop now?

## Why does this happen?

Now we can explain what we saw. Everything in the preview scrolled
except the dark bar at the top, which stayed where it was.

The `position` property sets how an element is placed as the page
scrolls. `position: sticky` with `top: 0` keeps an element in place once
scrolling would carry it past the top of the window. Until then, it
scrolls with everything else, the same as it would with no `position`
set at all. In our example, the preview plays the part of the window.

`top` names the point where the element sticks. `top: 0` is the very
top, and `top: 20px` is 20 pixels below it. In step 2, with
no `top` at all, the bar had no point to stick at, so it scrolled away
with the sections.

`sticky` is one of four values that are worth knowing:

| Value | What the element does as the page scrolls |
|---|---|
| `static` | It scrolls with the page. This is the default, when no `position` is set. |
| `relative` | It scrolls with the page, and on its own it looks the same as `static`. With `top` or `left`, it moves a little from where it would normally sit. |
| `sticky` | It scrolls with the page until it reaches the point set by `top`, then stays there. |
| `fixed` | It stays in the same place in the window all the time. It no longer takes up any space on the page, so the content after it moves up and can end up hidden behind it. |

Sometimes we might set `position: sticky` and find that nothing sticks.
Two things are worth checking. First, is there a `top` value? Second,
where does the element sit in the HTML? A sticky element can only stay
in view while its parent element is on screen. If a header sits inside a
short wrapper, it scrolls away as soon as the wrapper does.

Sticky headers are common on shops and news sites. The same idea works
on long tables too: `position: sticky` on a table's heading cells keeps
the heading row in view as we scroll down the rows.

## And the footer

The second example is a very short page: one paragraph, and a footer.

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

The page has almost no content, and yet the footer sits at the very
bottom of the preview, not right under the text. Three rules work
together to do this:

- `html, body { height: 100%; }` makes the page's body as tall as the
  preview. With `height: auto` in step 3, the body was only as tall as
  its content, so there was no empty space for the footer to move into.
- `body { display: flex; flex-direction: column; }` stacks the body's
  children from top to bottom, and lets them share out the space inside
  it. We meet `display: flex` properly in [Flexbox first
  steps](tutorial:flexbox-first-steps).
- `margin-top: auto` on the footer takes all the leftover space above
  it. However little content comes before the footer, this pushes the
  footer itself down to the bottom of the page. In step 2, without it,
  the footer moved up under the text.

This is a close relative of the auto margins on [Setting a page's width
and centring it](tutorial:the-container). There, auto margins shared
out the space beside a box. Here, one auto margin takes the space above
the footer. Oftentimes, when `margin-top: auto` seems to do nothing, the
parent element is missing `display: flex`. On an ordinary page, a top
margin set to `auto` counts as `0`.

## Now in your own site

In your fork, `styles.css` has a `header` rule. It sets
`position: sticky` and `top: 0`.

1. Open your page and scroll down. Does the header stay in view?
2. Change `position: sticky` to `position: fixed`. Save, refresh and
   scroll again.
3. Look at the content right below the header. Can you find a clue about
   what changed?
4. Now try `position: relative`. What does the header do as you scroll?
5. Set it back to `position: sticky`.
6. Find the `footer` rule. It has `margin-top: auto`. That is why the
   footer sits at the bottom of your page, even when there is little
   content above it.

Scroll your page one more time. Does the header stay in view again?

## What we have now

We can now keep a header in view as a page scrolls, and keep a footer
at the bottom of a short page.

| Word | Meaning | Example |
|---|---|---|
| `position: sticky` | Keeps an element in place once scrolling would carry it past a given point, set with `top` | `position: sticky; top: 0;` |
| `position: fixed` | Keeps an element in the same place in the window all the time. It no longer takes up space on the page. | `position: fixed;` |
| `position: static` | The default. The element scrolls with the page. | `position: static;` |
| `position: relative` | Looks the same as `static` on its own. With `top` or `left`, it moves the element a little from where it would normally sit. | `position: relative;` |
| `margin-top: auto` | On a child of a `display: flex` element, takes all the leftover space above it, pushing the element itself to the far side | `margin-top: auto;` |

## Where to Read More

Codepip. *Anchoreum*. <https://anchoreum.com/>. A puzzle game for CSS
anchor positioning, which pins one element to another rather than to the
page or to a scroll position. It is not on this course and it is newer
than most of what is — take it as a look at where `position` has gone
since.
