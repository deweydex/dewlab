---
title: "A header that stays in view as you scroll"
year: "2026-2027"
version: 2026.09.22.1
covers:
  why-does-this-happen:
    covers: [WA-LO9]
  now-in-your-own-site:
    touches: [WA-LO9]
---

# A header that stays in view as you scroll

On a long page, how do we keep the header in view while everything else
scrolls? On this page we:

- make a header bar stay at the top as we scroll
- compare the values of the `position` property
- find the same header in your own site

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
except the dark bar at the top, which stayed where it was. Here is the
same page before and after we scroll:

![Two browser windows showing the same page. On the left, before scrolling, the dark bar "I stay in view" is at the top of the window, with sections one, two and three below it. Sections four and five are drawn dashed below the window, off screen. On the right, after scrolling down, the sections have moved up. The header's own place in the page and section one are now above the window, drawn dashed, off screen. Section two has slid under the dark bar, which is still at the top of the window. Sections three and four fill the window, and section five runs past its bottom edge.](sticky-header-scrolled.svg)

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

Scroll your page one more time. Does the header stay in view again?

## What we have now

We can now keep a header in view as a page scrolls, and say how the
other values of `position` behave.

| Word | Meaning | Example |
|---|---|---|
| `position: sticky` | Keeps an element in place once scrolling would carry it past a given point, set with `top` | `position: sticky; top: 0;` |
| `position: fixed` | Keeps an element in the same place in the window all the time. It no longer takes up space on the page. | `position: fixed;` |
| `position: static` | The default. The element scrolls with the page. | `position: static;` |
| `position: relative` | Looks the same as `static` on its own. With `top` or `left`, it moves the element a little from where it would normally sit. | `position: relative;` |

## Where to Read More

Codepip. *Anchoreum*. <https://anchoreum.com/>. A puzzle game for CSS
anchor positioning, which pins one element to another rather than to the
page or to a scroll position. It is not on this course and it is newer
than most of what is — take it as a look at where `position` has gone
since.
