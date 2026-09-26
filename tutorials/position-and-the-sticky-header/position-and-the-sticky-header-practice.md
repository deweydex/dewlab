---
title: "A header that stays in view as you scroll — Practice"
practice_for: position-and-the-sticky-header
year: "2026-2027"
version: 2026.09.22.1
---

# A header that stays in view as you scroll — Practice

On this page we practise `position`: how to keep something in view as a
page scrolls, and what goes wrong when it does not stay. There are three
kinds of problem:

- a broken page, where we find the mistake and fix it
- a small layout to build from a description
- a change in your own site, which you commit

Each problem has a folded answer. Some also have a hint, folded before
the answer. Scroll each preview before you change anything. Most of
these mistakes only show once the page moves.

## Fix the broken page

**1.** The author wanted this header bar to stay at the top of the
preview while the sections scroll past it.

```html site
id: position-practice-notop-html
site: position-practice-notop
<div class="header">Plushie Shop</div>
<p>Squishy Squid</p>
<p>Cuddly Cuttlefish</p>
<p>Sleepy Seal</p>
<p>Wobbly Walrus</p>
<p>Happy Hedgehog</p>
```

```css site
id: position-practice-notop-css
site: position-practice-notop
body { margin: 0; }
.header {
  position: sticky;
  background: #2c3e50;
  color: white;
  padding: 10px;
}
p { height: 100px; margin: 0; padding: 10px; border-bottom: 1px solid #ccc; }
```

Scroll the preview. Does the bar stay in view? What is missing? Fix it.

<details class="dl-answer"><summary>answer</summary>

```css
.header {
  position: sticky;
  top: 0;
  background: #2c3e50;
  color: white;
  padding: 10px;
}
```

`position: sticky` needs a point to stick at, and `top` names that
point. With no `top`, the bar has nowhere to stop, so it scrolls away
with the sections. `top: 0` makes it stop at the very top of the
preview.

</details>

**2.** This header has `position: sticky` and `top: 0`. It still scrolls
away. Scroll slowly, and watch the moment it leaves.

```html site
id: position-practice-parent-html
site: position-practice-parent
<div class="top">
  <div class="header">Plushie Shop</div>
  <p class="welcome">Welcome! Every plushie is handmade.</p>
</div>
<p>Squishy Squid</p>
<p>Cuddly Cuttlefish</p>
<p>Sleepy Seal</p>
<p>Wobbly Walrus</p>
<p>Happy Hedgehog</p>
```

```css site
id: position-practice-parent-css
site: position-practice-parent
body { margin: 0; }
.header {
  position: sticky;
  top: 0;
  background: #2c3e50;
  color: white;
  padding: 10px;
}
.welcome { background: #f6f4f0; }
p { height: 100px; margin: 0; padding: 10px; border-bottom: 1px solid #ccc; }
```

The CSS for the header is right. So the problem is in the HTML. What
is it, and how do we fix it?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Scroll slowly. Does the bar stick at all, even for a moment?
2. When does it leave? What else leaves the preview at the same moment?
3. Which element is the header's parent? How tall is that parent?

**Think about:** a sticky element can only stay in view while its
parent is on screen.

**Try this next:** what happens if we give `.top` a height of
`400px`? Scroll and see where the bar leaves now.

</details>

<details class="dl-answer"><summary>answer</summary>

```html
<div class="header">Plushie Shop</div>
<div class="top">
  <p class="welcome">Welcome! Every plushie is handmade.</p>
</div>
<p>Squishy Squid</p>
<p>Cuddly Cuttlefish</p>
<p>Sleepy Seal</p>
<p>Wobbly Walrus</p>
<p>Happy Hedgehog</p>
```

The header was inside the short `<div class="top">`. It stuck for a
moment, and then it scrolled away together with the welcome paragraph,
as soon as its parent left the preview. When we move the header out of
that wrapper, the body becomes its parent. The body holds the whole
page, so the
header stays in view all the way down.

</details>

**3.** Here the author used `position: fixed` for the header. Look at
the first section, before you scroll.

```html site
id: position-practice-fixed-html
site: position-practice-fixed
<div class="header">The Plushie Shop, open every day</div>
<p>Squishy Squid</p>
<p>Cuddly Cuttlefish</p>
<p>Sleepy Seal</p>
<p>Wobbly Walrus</p>
<p>Happy Hedgehog</p>
```

```css site
id: position-practice-fixed-css
site: position-practice-fixed
body { margin: 0; }
.header {
  position: fixed;
  top: 0;
  background: #2c3e50;
  color: white;
  padding: 10px;
}
p { height: 100px; margin: 0; padding: 10px; border-bottom: 1px solid #ccc; }
```

Where are the words "Squishy Squid"? Change one word, so that the header
still stays in view and nothing is hidden.

<details class="dl-answer"><summary>answer</summary>

```css
.header {
  position: sticky;
  top: 0;
  background: #2c3e50;
  color: white;
  padding: 10px;
}
```

A `fixed` element no longer takes up any space on the page. So the first
section moved up, and its words are hidden behind the header. A `sticky`
element keeps its place on the page until it sticks, so the sections
start below it. You may also have noticed that the fixed header was only
as wide as its words. With `sticky`, it is full width again.

</details>

## Make this

**4.** A sticky element does not have to be at the top of the page. In
the cell below, a sale notice sits between the welcome text and the
list of plushies. Make it do this:

- at first, it scrolls up with the page
- when it reaches the top of the preview, it stops there, `10px` below
  the top edge
- the plushies then scroll past behind it

Can you also give it a background, so the words scrolling behind it do
not show through?

```html site
id: position-practice-notice-html
site: position-practice-notice
<p>Welcome to the Plushie Shop. Scroll down to see this week's plushies.</p>
<div class="sale">Sale ends Friday</div>
<p>Squishy Squid</p>
<p>Cuddly Cuttlefish</p>
<p>Sleepy Seal</p>
<p>Wobbly Walrus</p>
<p>Happy Hedgehog</p>
```

```css site
id: position-practice-notice-css
site: position-practice-notice
body { margin: 0; }
p { height: 100px; margin: 0; padding: 10px; border-bottom: 1px solid #ccc; }
.sale {
  padding: 10px;
  /* your rules here */
}
```

<details class="dl-answer"><summary>answer</summary>

```css
.sale {
  padding: 10px;
  position: sticky;
  top: 10px;
  background: #c0392b;
  color: white;
}
```

`position: sticky` lets the notice scroll with the page until it reaches
the point set by `top`. `top: 10px` sets that point `10px` below the top
of the preview. Any background colour works. Without one, the notice is
transparent, and the words of each section show through it as they
scroll past.

</details>

## In your own site

**5.** In your fork, `styles.css` has a `header` rule with
`position: sticky` and `top: 0`. In `index.html`, the `<header>` sits
directly inside `<body>`, so its parent is the whole page.

1. Open `index.html` in your browser, and scroll down. Check that the
   header stays in view.
2. In the `header` rule, change `top: 0` to `top: var(--spacing-sm)`.
   Save, refresh and scroll. What do you see above the header now?
3. Put `top: 0` back.
4. Above `position: sticky`, add a comment in your own words. Say which
   two things this header needs to stay in view. For example:
   `/* Sticks because it has a top value, and its parent, the body, is as tall as the page. */`
5. Save, and check the page still works.
6. Commit the change, with a message such as "Explain the sticky
   header".

Does the header on `about.html` stick too? Why?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Find the `header` rule. It is in the part of `styles.css` headed
   "Header & Navigation".
2. Look at the first practice problem on this page. What happened
   without `top`?
3. Look at the second practice problem. Why did the header leave?

**Think about:** those two problems show the two things a sticky header
needs.

**Try this next:** what would happen if you wrapped the `<header>` in
`index.html` inside a `<div>` with nothing else in it?

</details>

<details class="dl-answer"><summary>answer</summary>

With `top: var(--spacing-sm)`, the header stops a little below the top
of the window. The page scrolls past in the gap above it, so you see
bits of the content above the header.

The two things are a `top` value, which names the point where the header
sticks, and a parent tall enough to stay on screen. Here the parent is
the body, which holds the whole page.

The header on `about.html` sticks too. Both pages link to the same
`styles.css`, and on both pages the `<header>` sits directly inside the
body.

</details>
