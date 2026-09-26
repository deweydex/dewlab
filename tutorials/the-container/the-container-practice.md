---
title: "A readable width, centred on the page — Practice"
practice_for: the-container
year: "2026-2027"
version: 2026.09.22.1
---

# A readable width, centred on the page — Practice

On this page we practise `max-width` and auto margins: how to stop a box
from growing too wide, and how to keep it in the middle. There are three
kinds of problem:

- a broken page, where we find the mistake and fix it
- a small layout to build from a description
- a change in your own site, which you commit

Each problem has a folded answer. Some also have a hint, folded before
the answer. Try the problem first, and use the **Preview width** slider
as you go. Many of these mistakes only show at some widths.

## Fix the broken page

**1.** The author wanted a white column, `300px` wide at most, in the
middle of the grey page. The CSS has `margin: 0 auto`, but the column is
not in the middle.

```html site
id: container-practice-full-html
site: container-practice-full
<div class="container">
  <p>Opening hours: 10 to 6, Monday to Saturday.</p>
</div>
```

```css site
id: container-practice-full-css
site: container-practice-full
body { margin: 0; background: #ddd; }
.container {
  margin: 0 auto;
  background: white;
  padding: 12px;
  border: 1px solid #2c3e50;
}
```

How wide is the white box? Why does `margin: 0 auto` do nothing here? Fix
it.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Drag the **Preview width** slider. Does the white box ever leave any
   space beside it?
2. Auto margins share out the leftover space beside a box. How much
   space is left over here?
3. What would make the box narrower than the page, so that there is
   some space left over?

**Think about:** what do auto margins need before they can centre
anything?

**Try this next:** what happens if we set `max-width: 100%` instead?
Is there any leftover space then?

</details>

<details class="dl-answer"><summary>answer</summary>

```css
body { margin: 0; background: #ddd; }
.container {
  max-width: 300px;
  margin: 0 auto;
  background: white;
  padding: 12px;
  border: 1px solid #2c3e50;
}
```

Without a `max-width` or a `width`, the box fills the whole width of the
page. There is no leftover space beside it, so the auto margins have
nothing to share out. With `max-width: 300px`, the box stops growing at
`300px`, and the auto margins split the space left over on either side.

</details>

**2.** This column looks fine in a wide preview. Now drag the **Preview
width** slider all the way to narrow.

```html site
id: container-practice-fixed-html
site: container-practice-fixed
<div class="container">
  <p>Every plushie is washable at 30 degrees.</p>
</div>
```

```css site
id: container-practice-fixed-css
site: container-practice-fixed
body { margin: 0; background: #ddd; }
.container {
  width: 400px;
  margin: 0 auto;
  background: white;
  padding: 12px;
  border: 1px solid #2c3e50;
}
```

What goes wrong in a narrow preview? Change one word so the column
works at every width.

<details class="dl-answer"><summary>answer</summary>

```css
.container {
  max-width: 400px;
  margin: 0 auto;
  background: white;
  padding: 12px;
  border: 1px solid #2c3e50;
}
```

`width: 400px` sets one size, and the box keeps it whatever is around
it. In a preview narrower than the box, the box runs past the right-hand
edge. `max-width: 400px` sets the widest the box may grow, so in a narrow
preview it shrinks to fit. On a phone, this means we can read the page
without scrolling sideways.

</details>

**3.** This column has a `max-width`, and the author meant to centre it.
But it sits on the left.

```html site
id: container-practice-swap-html
site: container-practice-swap
<div class="container">
  <p>Gift wrapping is free.</p>
</div>
```

```css site
id: container-practice-swap-css
site: container-practice-swap
body { margin: 0; background: #ddd; }
.container {
  max-width: 300px;
  margin: auto 0;
  background: white;
  padding: 12px;
  border: 1px solid #2c3e50;
}
```

Look closely at the `margin` line. What is wrong with it?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. `margin` has two values here. Which sides does the first value set?
2. Which sides does the second value set?
3. Which sides need to be `auto` to centre a box?

**Think about:** when `margin` has two values, which one is for the
left and right?

**Try this next:** how would we centre the box and also leave `20px`
of space above and below it?

</details>

<details class="dl-answer"><summary>answer</summary>

```css
.container {
  max-width: 300px;
  margin: 0 auto;
  background: white;
  padding: 12px;
  border: 1px solid #2c3e50;
}
```

With two values, the first sets the top and bottom margins, and the
second sets the left and right. `margin: auto 0` put `auto` on the top
and bottom, and `0` on the left and right, so nothing shared out the
space beside the box. `margin: 0 auto` puts the auto margins on the left
and right, where they centre the box.

</details>

## Make this

**4.** Build this notice in the cell below:

- a white box on the grey page, with a thin `#2c3e50` border
- never wider than `320px`, and narrower when the preview is narrower
- in the middle of the page, from left to right
- `2rem` of space between the top of the page and the box

Can you do the centring and the space above with one `margin`
declaration?

```html site
id: container-practice-notice-html
site: container-practice-notice
<div class="notice">
  <p>The shop is closed on Sunday.</p>
</div>
```

```css site
id: container-practice-notice-css
site: container-practice-notice
body { margin: 0; background: #ddd; }
.notice {
  background: white;
  padding: 12px;
  /* your rules here */
}
```

<details class="dl-answer"><summary>answer</summary>

```css
body { margin: 0; background: #ddd; }
.notice {
  background: white;
  padding: 12px;
  border: 1px solid #2c3e50;
  max-width: 320px;
  margin: 2rem auto;
}
```

`max-width: 320px` caps the box, and lets it shrink in a narrow preview.
In `margin: 2rem auto`, the first value sets the top and bottom margins
to `2rem`. The second sets the left and right margins to `auto`, which
centres the box. Drag the slider to check both.

</details>

## In your own site

**5.** In your fork, `styles.css` has an `.about-content` rule. It sets
`max-width: 800px` and `margin: 0 auto`. On `about.html`, the
`<article class="about-content">` sits inside a `<div class="container">`.
So it is a narrow container inside a wider one.

1. Open `about.html` in your browser, with the window as wide as it
   goes.
2. Change the `max-width` in `.about-content` to `600px`. Save, and
   refresh.
3. Which parts of the page get narrower? Does the header, with the
   logo and the links, change?
4. Try `700px` too. Keep the width that you find easiest to read.
5. Commit the change, with a message such as "Narrower text column on
   the About page".

Can you see the two auto margins in the inspector, as two equal bands on
either side of the article?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Find the `.about-content` rule. It is in the part of `styles.css`
   headed "About Page".
2. Look at `about.html`. Which elements have the class `about-content`,
   and which have the class `container`?
3. A rule only changes the elements its selector matches.

**Think about:** which class does the header use?

**Try this next:** what would change if we set `max-width: 600px` in
the `.container` rule instead?

</details>

<details class="dl-answer"><summary>answer</summary>

Only the article gets narrower: the headings, the paragraphs and the
card inside it. It stays in the middle, because `margin: 0 auto` still
splits the leftover space on either side.

The header does not change. Its content sits in an element with the
class `container`, and the `.container` rule still says
`max-width: 1200px`. The article has its own, narrower limit, inside
that wider container.

</details>
