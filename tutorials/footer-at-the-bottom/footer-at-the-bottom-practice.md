---
title: "A footer that sits at the bottom of a short page — Practice"
practice_for: footer-at-the-bottom
year: "2026-2027"
version: 2026.09.22.1
---

# A footer that sits at the bottom of a short page — Practice

On this page we practise keeping a footer at the bottom of a short page.
Every problem here uses the same three rules:

- `body { min-height: 100vh; }` makes the body at least as tall as the
  window. `100vh` is the full height of the window, and in these cells
  the preview plays the part of the window. On a long page, the body
  grows taller to fit.
- `body { display: flex; flex-direction: column; }` stacks the body's
  children from top to bottom, and lets them share out the space inside
  it.
- `footer { margin-top: auto; }` gives the footer all the leftover space
  above it, which pushes the footer down to the bottom.

There are three kinds of problem:

- a broken page, where we find the mistake and fix it
- a small layout to build from a description
- a change in your own site, which you commit

Each problem has a folded answer. Some also have a hint, folded before
the answer. When a footer is in the wrong place, check the three rules
one at a time. Which one is missing?

## Fix the broken page

**1.** This footer should sit at the very bottom of the preview. It sits
right under the text instead.

```html site
id: footer-practice-noflex-html
site: footer-practice-noflex
<p>Our shop is open from 10 to 6.</p>
<footer>© Plushie Shop</footer>
```

```css site
id: footer-practice-noflex-css
site: footer-practice-noflex
body { margin: 0; min-height: 100vh; }
footer {
  margin-top: auto;
  background: #2c3e50;
  color: white;
  padding: 10px;
}
```

The footer has `margin-top: auto`, and the body is as tall as the
preview. So what is missing? Fix it.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Check the three rules at the top of this page. Which ones are
   here?
2. `margin-top: auto` only pushes the footer down when its parent has
   one particular setting. What is that?
3. On an ordinary page, what does a top margin of `auto` count as?

**Think about:** which element needs to change: the footer, or its
parent?

**Try this next:** once it works, delete `flex-direction: column;`
only. What happens to the paragraph and the footer?

</details>

<details class="dl-answer"><summary>answer</summary>

```css
body {
  margin: 0;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
footer {
  margin-top: auto;
  background: #2c3e50;
  color: white;
  padding: 10px;
}
```

On an ordinary page, a top margin set to `auto` counts as `0`. So the
footer sat right under the text. The body needs `display: flex` and
`flex-direction: column`. Then its children share out the space inside
it, and the footer's auto margin takes all the leftover space.

</details>

**2.** This time the body is a flex column, and the footer has
`margin-top: auto`. The footer still sits right under the text.

```html site
id: footer-practice-noheight-html
site: footer-practice-noheight
<p>Our shop is open from 10 to 6.</p>
<footer>© Plushie Shop</footer>
```

```css site
id: footer-practice-noheight-css
site: footer-practice-noheight
body { margin: 0; display: flex; flex-direction: column; }
footer {
  margin-top: auto;
  background: #2c3e50;
  color: white;
  padding: 10px;
}
```

How tall is the body here? Fix it.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Check the three rules at the top of this page. Which one is
   missing now?
2. Without a height of its own, a body is only as tall as its content.
   How much leftover space is there inside it?
3. What would make the body at least as tall as the preview?

**Think about:** `margin-top: auto` takes the leftover space. What if
there is none?

**Try this next:** once it works, add ten more paragraphs above the
footer. Does the body grow to fit them, and does the footer stay under
the last one?

</details>

<details class="dl-answer"><summary>answer</summary>

```css
body {
  margin: 0;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
```

Without a height of its own, the body was only as tall as the paragraph
and the footer. There was no leftover space for the auto margin to
take. `min-height: 100vh` makes the body at least as tall as the
preview, so there is space above the footer for the auto margin to
fill.

</details>

**3.** This page has a header, a main part and a footer. The footer is at
the bottom, but there is a large empty gap between the header and the
main part.

```html site
id: footer-practice-wrong-html
site: footer-practice-wrong
<header>Plushie Shop</header>
<main>
  <p>New plushies every Friday.</p>
</main>
<footer>© Plushie Shop</footer>
```

```css site
id: footer-practice-wrong-css
site: footer-practice-wrong
body {
  margin: 0;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
header, footer { background: #2c3e50; color: white; padding: 10px; }
main { margin-top: auto; padding: 10px; }
```

Why is the main part down at the bottom, next to the footer? Fix it, so
the main part sits under the header and the footer stays at the bottom.

<details class="dl-answer"><summary>answer</summary>

```css
header, footer { background: #2c3e50; color: white; padding: 10px; }
main { padding: 10px; }
footer { margin-top: auto; }
```

`margin-top: auto` was on `main`, so `main` took all the leftover space
above it. That pushed `main` down, and the footer came down with it,
because the footer comes after `main`. The auto margin belongs on the
footer. Then the leftover space goes between `main` and the footer.

</details>

## Make this

**4.** Build this page in the cell below:

- a dark header bar at the top
- a main part with one short paragraph, right under the header
- a dark footer bar at the very bottom of the preview
- when the page gets longer, the footer stays under the content

The HTML is ready. Write the CSS.

```html site
id: footer-practice-build-html
site: footer-practice-build
<header>Plushie Shop</header>
<main>
  <p>Every plushie is handmade.</p>
</main>
<footer>© Plushie Shop</footer>
```

```css site
id: footer-practice-build-css
site: footer-practice-build
body { margin: 0; }
header, footer { background: #2c3e50; color: white; padding: 10px; }
main { padding: 10px; }
/* your rules here */
```

To test the last point, copy the paragraph ten times. Does the footer
stay under the last one?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Which element holds the header, the main part and the footer? That
   element needs two of the three rules.
2. Which element should be pushed to the bottom? That one needs the
   third rule.
3. Why `min-height`, and not `height`? Think about what should happen
   when the page gets long.

**Think about:** `min-height` sets the smallest the body can be. What
does it allow the body to do?

**Try this next:** can you add a sticky header too, from
[A header that stays in view as you scroll](tutorial:position-and-the-sticky-header)?

</details>

<details class="dl-answer"><summary>answer</summary>

```css
body {
  margin: 0;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
header, footer { background: #2c3e50; color: white; padding: 10px; }
main { padding: 10px; }
footer { margin-top: auto; }
```

The body is at least as tall as the preview, and stacks its children
from top to bottom. The footer's auto margin takes the leftover space
above it. With ten paragraphs, the content is taller than the preview.
`min-height` lets the body grow to fit, and there is no leftover space,
so the footer sits right under the last paragraph.

</details>

## In your own site

**5.** In your fork, `styles.css` has a `body` rule with
`min-height: 100vh`, `display: flex` and `flex-direction: column`. It
also has a `footer` rule with `margin-top: auto`. These are the same
three rules as on this page.

1. Open `index.html` in your browser. Zoom out with **Ctrl** and **-**
   (**Cmd** and **-** on a Mac) until the whole page fits in the window
   with space to spare. Where is the footer?
2. In the `footer` rule, put `/*` before `margin-top: auto;` and `*/`
   after it. This turns the line into a comment, so the browser ignores
   it. Save, and refresh. Where is the footer now?
3. Take the comment marks away again. Save, refresh, and check the
   footer is back at the bottom.
4. The footer says `&copy; 2025 My Portfolio. All rights reserved.` in
   `index.html`. Change the year to this year, and the name to your
   name or your site's name.
5. Make the same change in the footer of `about.html`.
6. Zoom back in with **Ctrl** and **0** (**Cmd** and **0** on a Mac).
7. Commit the change, with a message such as "Update the footer".

Do both pages show your new footer, at the bottom of the window?

<details class="dl-answer"><summary>answer</summary>

Zoomed out, the page is shorter than the window, and the footer sits at
the bottom of the window. With `margin-top: auto` turned into a comment,
the footer moves up to sit right under the content, with empty space
below it. Without the auto margin, nothing takes the leftover space
above the footer, so that space is below it.

Each page has its own copy of the footer, so you change the text in both
`index.html` and `about.html`. `&copy;` shows as the © sign.

</details>
