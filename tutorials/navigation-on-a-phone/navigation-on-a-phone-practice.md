---
title: "A navigation that works on a phone — Practice"
practice_for: navigation-on-a-phone
year: "2026-2027"
version: 2026.09.22.1
---

# A navigation that works on a phone — Practice

On this page we practise a menu that stacks into a column on a narrow
screen, with `flex-direction: column` inside a media query. There are
three kinds of problem:

- a broken page, where we find the mistake and fix it
- a small layout to build from a description
- a change in your own site, which you commit

Each problem has a folded answer. Some also have a hint, folded before
the answer. Try the problem first, and use the **Preview width** slider
as you go. Every problem on this page changes with the width.

## Fix the broken page

**1.** This menu has five links, and no media query yet. Drag the
**Preview width** slider slowly from wide to narrow, and watch the
links.

```html site
id: phone-nav-practice-ragged-html
site: phone-nav-practice-ragged
<nav aria-label="Main">
  <a href="#" class="logo">Plushie Shop</a>
  <ul>
    <li><a href="#">Home</a></li>
    <li><a href="#">About</a></li>
    <li><a href="#">Gallery</a></li>
    <li><a href="#">Contact</a></li>
    <li><a href="#">Resources</a></li>
  </ul>
</nav>
```

```css site
id: phone-nav-practice-ragged-css
site: phone-nav-practice-ragged
nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
}
nav ul { display: flex; flex-wrap: wrap; gap: 16px; list-style: none; padding: 0; }
```

At some widths, the menu looks untidy. What happens to the links? Add a
media query so that, below `400px`, the logo sits on top and the links
stack in one column under it.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. At what widths does one link sit alone on a second line?
2. A media query that starts `@media (max-width: 400px)` holds rules
   for narrow previews only. Where in the CSS does it go?
3. Two elements need `flex-direction: column` inside it. Which two?

**Think about:** why is a whole column easier to read than a row with
one link left over?

**Try this next:** once it works, is `400px` the best breakpoint? Find
the widest width where a link still sits alone, and use that instead.

</details>

<details class="dl-answer"><summary>answer</summary>

```css
nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
}
nav ul { display: flex; flex-wrap: wrap; gap: 16px; list-style: none; padding: 0; }

@media (max-width: 400px) {
  nav { flex-direction: column; align-items: flex-start; }
  nav ul { flex-direction: column; gap: 8px; }
}
```

Without a media query, the links wrap. At some narrow widths, the last
link drops onto a second line on its own, and the menu has a ragged
half-row. Inside
the media query, `nav` stacks the logo above the list, and `nav ul`
stacks the links in one column, in the same order.

</details>

**2.** The author wanted this menu to stack into a column in narrow
previews only. Drag the slider from wide to narrow.

```html site
id: phone-nav-practice-minmax-html
site: phone-nav-practice-minmax
<nav aria-label="Main">
  <a href="#" class="logo">Site</a>
  <ul>
    <li><a href="#">Home</a></li>
    <li><a href="#">About</a></li>
    <li><a href="#">Contact</a></li>
  </ul>
</nav>
```

```css site
id: phone-nav-practice-minmax-css
site: phone-nav-practice-minmax
nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
}
nav ul { display: flex; gap: 16px; list-style: none; }

@media (min-width: 350px) {
  nav { flex-direction: column; align-items: flex-start; }
  nav ul { flex-direction: column; gap: 8px; }
}
```

When is the menu a column, and when is it a row? Fix the media query.

<details class="dl-answer"><summary>answer</summary>

```css
@media (max-width: 350px) {
  nav { flex-direction: column; align-items: flex-start; }
  nav ul { flex-direction: column; gap: 8px; }
}
```

`min-width: 350px` means "when the preview is at least `350px` wide", so
the menu stacked in every wide preview and made a row only in a very
narrow one. That is the wrong way round. `max-width: 350px` means "when
the preview is at most `350px` wide".

</details>

**3.** In a narrow preview, these links stack into a column, as the
author wanted. But the column sits to the right of the logo, not under
it.

```html site
id: phone-nav-practice-half-html
site: phone-nav-practice-half
<nav aria-label="Main">
  <a href="#" class="logo">Site</a>
  <ul>
    <li><a href="#">Home</a></li>
    <li><a href="#">About</a></li>
    <li><a href="#">Contact</a></li>
  </ul>
</nav>
```

```css site
id: phone-nav-practice-half-css
site: phone-nav-practice-half
nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
}
nav ul { display: flex; gap: 16px; list-style: none; }

@media (max-width: 350px) {
  nav ul { flex-direction: column; gap: 8px; }
}
```

Which flex container is still a row? Fix it.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. There are two flex containers here. One holds the logo and the list.
   The other holds the links.
2. Which of the two does the media query change?
3. What does the other one need, so that the logo and the list stack?

**Think about:** `flex-direction` changes only the container it is set
on. Does it change the containers inside it?

**Try this next:** once it works, take out `align-items: flex-start`.
Where do the logo and the list sit then?

</details>

<details class="dl-answer"><summary>answer</summary>

```css
@media (max-width: 350px) {
  nav { flex-direction: column; align-items: flex-start; }
  nav ul { flex-direction: column; gap: 8px; }
}
```

There are two flex containers. `nav` holds the logo and the list, and
`nav ul` holds the links. The media query stacked the links, inside the
list, but `nav` was still a row, so the list stayed beside the logo.
`flex-direction: column` on `nav` puts the list under the logo, and
`align-items: flex-start` lines both up on the left.

</details>

## Make this

**4.** Build a footer menu. In a wide preview, its three links sit in a
row, in the middle. Below `400px`, they stack in a column, still in the
middle, with `6px` between them.

```html site
id: phone-nav-practice-footer-html
site: phone-nav-practice-footer
<footer>
  <ul>
    <li><a href="#">Privacy</a></li>
    <li><a href="#">Delivery</a></li>
    <li><a href="#">Returns</a></li>
  </ul>
</footer>
```

```css site
id: phone-nav-practice-footer-css
site: phone-nav-practice-footer
footer { background: #2c3e50; padding: 12px; }
footer a { color: white; }
footer ul { list-style: none; padding: 0; margin: 0; }
/* your rules here */
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Make `footer ul` a flex container, with a gap between the links.
2. `justify-content: center` puts the items of a flex row in the middle
   of the row.
3. In a column, the main direction runs from top to bottom, so
   `justify-content` now works from top to bottom. `align-items: center`
   puts the items in the middle from side to side.

**Think about:** when a flex container turns into a column,
`justify-content` works from top to bottom. What works from side to
side?

**Try this next:** what happens in the column if we leave out
`align-items: center`?

</details>

<details class="dl-answer"><summary>answer</summary>

```css
footer ul { display: flex; justify-content: center; gap: 24px; }

@media (max-width: 400px) {
  footer ul { flex-direction: column; align-items: center; gap: 6px; }
}
```

Any gap works in the wide row. In the row, `justify-content: center`
puts the links in the middle. In the column, the main direction runs
from top to bottom, so `justify-content` no longer centres them from
side to side. `align-items: center` does that job across a column.

</details>

## In your own site

**5.** In your fork of `project_wad`, the `@media (max-width: 480px)`
block in `styles.css` stacks your menu. But your own link names may be
longer than the starter's. Your menu might wrap untidily at a width
*above* `480px`, before the media query switches on.

1. Open your home page in device mode, as on [Changing the layout for
   phones: media queries](tutorial:media-queries).
2. Start at about `800px` wide, and make the width smaller, slowly.
   Watch your menu.
3. Does a link drop onto a second line before the width reaches
   `480px`? Note the width where that first happens.
4. If it does, change `480px` in the media query to that width. Save,
   and check again.
5. Commit the change, with a message such as "Stack the menu before it
   wraps".

Is there any width now where your menu has one link sitting alone?

<details class="dl-answer"><summary>answer</summary>

It depends on your own link names, and on your logo. If your menu never
wraps above `480px`, the starter's breakpoint already suits it, and you
can leave it. If it wraps at, say, `560px`, change the media query to
`@media (max-width: 560px)`. Both rules inside it, for `.header-inner`
and `.main-nav ul`, then switch on before the menu has a chance to wrap.

</details>
