---
title: "Laying out a page with grid areas — Practice"
practice_for: named-grid-areas
year: "2026-2027"
version: 2026.09.22.1
---

# Laying out a page with grid areas — Practice

On this page we practise grid maps: `grid-template-areas`, which draws
the map, and `grid-area`, which puts each element in its place. There
are three kinds of problem:

- a broken page, where we find the mistake and fix it
- a small layout to build from a description
- a change in your own site, which you commit

Each problem has a folded answer. Some also have a hint, folded before
the answer. Try the problem first. When a map goes wrong, it helps to
write the map out on paper as a small table, one row for each quoted
line.

## Fix the broken page

**1.** The author wanted a header across the top, a menu beside the
main area, and a footer across the bottom. Instead, all four boxes sit
on top of each other in one small corner.

```html site
id: grid-practice-short-html
site: grid-practice-short
<div class="page">
  <header>Header</header>
  <nav>Menu</nav>
  <main>Main</main>
  <footer>Footer</footer>
</div>
```

```css site
id: grid-practice-short-css
site: grid-practice-short
.page {
  display: grid;
  grid-template-areas:
    "header header"
    "nav main main"
    "footer footer";
  grid-template-columns: 120px 1fr;
  gap: 8px;
}
.page > * {
  padding: 12px;
  background: #f6f4f0;
  border: 1px solid #ccc;
  font-family: sans-serif;
}
header { grid-area: header; }
nav { grid-area: nav; }
main { grid-area: main; }
footer { grid-area: footer; }
```

Count the words in each quoted line. What is wrong with the map? Fix
it.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. How many words are in the first line? The second? The third?
2. The page has two columns, from `grid-template-columns`. How many
   words should each line have?
3. What happens to the whole map when one line breaks the rules?

**Think about:** why do all four boxes end up in the same place, and
not only the menu and the main area?

**Try this next:** what if we wanted three columns instead? What would
each line, and `grid-template-columns`, need then?

</details>

<details class="dl-answer"><summary>answer</summary>

```css
.page {
  display: grid;
  grid-template-areas:
    "header header"
    "nav main"
    "footer footer";
  grid-template-columns: 120px 1fr;
  gap: 8px;
}
```

The second line had three words, and the others had two. Every quoted
line must have the same number of words. When one does not, the
browser ignores the whole `grid-template-areas` declaration. Then no
area called `header`, `nav`, `main` or `footer` exists, so every
`grid-area` points at nothing, and the four boxes were piled into the
same spot. So the whole layout broke, and not only the second row.

</details>

**2.** This time the map is fine, but the menu has ended up in a narrow
column of its own, at the bottom right.

```html site
id: grid-practice-name-html
site: grid-practice-name
<div class="page">
  <header>Header</header>
  <nav>Menu</nav>
  <main>Main</main>
  <footer>Footer</footer>
</div>
```

```css site
id: grid-practice-name-css
site: grid-practice-name
.page {
  display: grid;
  grid-template-areas:
    "header header"
    "nav main"
    "footer footer";
  grid-template-columns: 120px 1fr;
  gap: 8px;
}
.page > * {
  padding: 12px;
  background: #f6f4f0;
  border: 1px solid #ccc;
  font-family: sans-serif;
}
header { grid-area: header; }
nav { grid-area: menu; }
main { grid-area: main; }
footer { grid-area: footer; }
```

Compare the names in the map with the names in the `grid-area` lines.
Fix it.

<details class="dl-answer"><summary>answer</summary>

```css
nav { grid-area: nav; }
```

The map names the area `nav`, but the rule asked for an area called
`menu`, which the map does not have. The browser had to find somewhere
else for the menu, so it added a new column and a new row at the edge
of the grid. The name in `grid-area` must match a word in the map
exactly. The text inside the element, "Menu", plays no part.

</details>

**3.** The author wanted the menu to run down the left-hand side, beside
both the main area and the footer. The header stays across the top.

```html site
id: grid-practice-shape-html
site: grid-practice-shape
<div class="page">
  <header>Header</header>
  <nav>Menu</nav>
  <main>Main</main>
  <footer>Footer</footer>
</div>
```

```css site
id: grid-practice-shape-css
site: grid-practice-shape
.page {
  display: grid;
  grid-template-areas:
    "header header"
    "nav main"
    "footer nav";
  grid-template-columns: 120px 1fr;
  gap: 8px;
}
.page > * {
  padding: 12px;
  background: #f6f4f0;
  border: 1px solid #ccc;
  font-family: sans-serif;
}
header { grid-area: header; }
nav { grid-area: nav; }
main { grid-area: main; }
footer { grid-area: footer; }
```

Draw the map as a small table on paper, and shade the cells called
`nav`. What shape do they make? Fix the map.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. In the second line, which column is `nav` in? In the third line?
2. Do those two cells touch, side by side or one above the other?
3. The menu should be in the left-hand column in both rows. Where does
   the footer go, then?

**Think about:** what shape must every named area make?

**Try this next:** can you make the footer run under both the menu and
the main area, with the menu beside the main area only?

</details>

<details class="dl-answer"><summary>answer</summary>

```css
.page {
  display: grid;
  grid-template-areas:
    "header header"
    "nav main"
    "nav footer";
  grid-template-columns: 120px 1fr;
  gap: 8px;
}
```

In the broken map, `nav` was on the left in one row, and on the right
in the next. Those two cells only touch at a corner, so they do not
make a rectangle. The browser ignored the whole map, and all four boxes
piled up in one spot. With `nav` on the left in both rows, the menu is
one rectangle, one column wide and two rows tall.

</details>

## Make this

**4.** Build this layout, with three columns:

- the header runs across all three columns
- below it: the menu on the left, the main area in the middle, and a
  box of extras on the right
- the footer sits under the main area only, with empty cells on either
  side of it
- the left and right columns are `100px` wide, and the middle column
  takes the rest

```html site
id: grid-practice-three-html
site: grid-practice-three
<div class="page">
  <header>Header</header>
  <nav>Menu</nav>
  <main>Main</main>
  <aside>Extras</aside>
  <footer>Footer</footer>
</div>
```

```css site
id: grid-practice-three-css
site: grid-practice-three
.page {
  display: grid;
  gap: 8px;
  /* your map and columns here */
}
.page > * {
  padding: 12px;
  background: #f6f4f0;
  border: 1px solid #ccc;
  font-family: sans-serif;
}
/* your grid-area rules here */
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. How many rows does the layout have? Write one quoted line for each.
2. Each line needs three words, one for each column.
3. How do we name an empty cell?
4. Each of the five elements needs a `grid-area` that matches a word in
   the map.

**Think about:** `<aside>` is new here. It is an element for content
that sits beside the main content. It needs a name in the map, like
the others.

**Try this next:** what changes if the footer should run under all
three columns instead?

</details>

<details class="dl-answer"><summary>answer</summary>

```css
.page {
  display: grid;
  gap: 8px;
  grid-template-areas:
    "header header header"
    "nav main aside"
    ". footer .";
  grid-template-columns: 100px 1fr 100px;
}
.page > * {
  padding: 12px;
  background: #f6f4f0;
  border: 1px solid #ccc;
  font-family: sans-serif;
}
header { grid-area: header; }
nav { grid-area: nav; }
main { grid-area: main; }
aside { grid-area: aside; }
footer { grid-area: footer; }
```

The dots in `". footer ."` name the two empty cells, so the last line
still has three words. The name `aside` is our choice. Any word works,
as long as the map and the `grid-area` line use the same one.

</details>

## In your own site

**5.** Your starter has no grid yet. Let's add a small one. On
`about.html`, the section at the bottom holds a heading, "Want to See
My Work?", a line of text, and the two buttons in `.cta-buttons`. On a
wide screen, we could put the buttons on the right, beside the heading
and the text.

1. In `styles.css`, find the `@media (max-width: 768px)` block near the
   bottom.
2. Just above it, add this new media query:

   ```css
   @media (min-width: 769px) {
       .cta-section .container {
           display: grid;
           grid-template-areas:
               "heading buttons"
               "text buttons";
           grid-template-columns: 1fr auto;
       }

       .cta-section h2 {
           grid-area: heading;
       }

       .cta-section p {
           grid-area: text;
       }

       .cta-buttons {
           grid-area: buttons;
           align-self: center;
       }
   }
   ```

   The last line, `align-self: center`, is new. Without it, the buttons
   would stretch to fill the whole height of their area. With it, they
   keep their own height, and sit in the middle of the area.

3. Save, and open `about.html` in a wide browser window. Where are the
   buttons now?
4. Make the window narrower than `769px`, or use device mode. What
   happens to the layout?
5. Commit the change, with a message such as "Put the About page
   buttons beside the heading on wide screens".

Why did we use `min-width: 769px`, and not `768px`?

<details class="dl-answer"><summary>answer</summary>

On a wide screen, the heading and the text sit in the left-hand column,
one above the other. The buttons sit in the right-hand column.
`buttons` is in both lines of the map, so their area is two rows tall,
and `align-self: center` keeps them in the middle of it. `auto` makes the right-hand column as wide as the buttons need,
and `1fr` gives the rest to the heading and the text.

Below `769px`, the media query is not true. The container is an ordinary
block again, and the heading, the text and the buttons stack, as
before.

Your stylesheet's other block starts at `max-width: 768px`. With
`min-width: 769px`, the two never overlap. At `768px` only the old
block applies, and at `769px` only the new one.

</details>
