---
title: "Cards in a row: grow, shrink and basis in Flexbox — Practice"
practice_for: cards-in-a-row
year: "2026-2027"
version: 2026.09.22.1
---

# Cards in a row: grow, shrink and basis in Flexbox — Practice

On this page we practise the three parts of `flex`: *flex-grow*,
*flex-shrink* and *flex-basis*, in that order. There are three kinds of
problem:

- a broken page, where we find the mistake and fix it
- a small layout to build from a description
- a change in your own site, which you commit

Each problem has a folded answer. Some also have a hint, folded before
the answer. Try the problem first, and use the **Preview width** slider
as you go. Many of these mistakes only show at some widths.

## Fix the broken page

**1.** The author wanted three cards that share the width of the row
between them. Instead, the cards sit bunched together on the left.

```html site
id: cards-practice-wrongbox-html
site: cards-practice-wrongbox
<div class="row">
  <div class="card">Tea</div>
  <div class="card">Coffee</div>
  <div class="card">Juice</div>
</div>
```

```css site
id: cards-practice-wrongbox-css
site: cards-practice-wrongbox
.row { display: flex; flex-wrap: wrap; gap: 12px; flex: 1 1 90px; }
.card {
  padding: 16px;
  border: 1px solid #ccc;
  border-radius: 6px;
  background: #f6f4f0;
}
```

The `flex` value is right. What is wrong with where it is? Fix it.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Which element is the flex container here? Which elements are its
   items?
2. `flex: 1 1 90px` tells an item how to grow and shrink inside its
   container. Which element has it now?
3. Which elements should grow to share the width?

**Think about:** does `display: flex` go on the parent or on the
children? And `flex`?

**Try this next:** once it works, drag the slider to narrow. At what
width does the third card move to a new row?

</details>

<details class="dl-answer"><summary>answer</summary>

```css
.row { display: flex; flex-wrap: wrap; gap: 12px; }
.card {
  flex: 1 1 90px;
  padding: 16px;
  border: 1px solid #ccc;
  border-radius: 6px;
  background: #f6f4f0;
}
```

`display: flex` goes on the container, the `.row`. `flex` goes on the
items, the cards, because it says how each item grows and shrinks. On
the `.row`, it did nothing for the cards, so each card stayed as wide as
its own text.

</details>

**2.** These cards should move to a new row when the preview gets
narrow. Drag the **Preview width** slider all the way to narrow.

```html site
id: cards-practice-nowrap-html
site: cards-practice-nowrap
<div class="row">
  <div class="card">Tea</div>
  <div class="card">Coffee</div>
  <div class="card">Juice</div>
</div>
```

```css site
id: cards-practice-nowrap-css
site: cards-practice-nowrap
.row { display: flex; gap: 12px; }
.card {
  flex: 1 1 90px;
  padding: 16px;
  border: 1px solid #ccc;
  border-radius: 6px;
  background: #f6f4f0;
}
```

What do the cards do instead of moving to a new row? Fix it.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. In a narrow preview, how wide is each card? Is it more or less than
   its basis of `90px`?
2. Which part of `flex: 1 1 90px` lets a card get smaller than its
   basis?
3. Which property of the row lets its items move onto a new line? We
   met it on [Lining boxes up in a row with
   Flexbox](tutorial:flexbox-first-steps).

**Think about:** when there is too little room, a flex item can shrink
or it can wrap. Which one happens when the row cannot wrap?

**Try this next:** put the row back the way it was, and change the
cards to `flex: 1 0 90px`. What happens in a narrow preview now?

</details>

<details class="dl-answer"><summary>answer</summary>

```css
.row { display: flex; flex-wrap: wrap; gap: 12px; }
```

Without `flex-wrap: wrap`, a flex container keeps all its items on one
line. When the line is too short, `flex-shrink: 1` lets each card shrink
below its `90px` basis to fit, so the cards got squeezed. With
`flex-wrap: wrap`, a card that does not fit at its basis moves to the
next line.

</details>

## Make this

**3.** Make the first card greedy. When there is spare space in the row,
the first card should take twice as big a share of it as each of the
other two. Change the CSS only.

```html site
id: cards-practice-greedy-html
site: cards-practice-greedy
<div class="row">
  <div class="card first">Tea</div>
  <div class="card">Coffee</div>
  <div class="card">Juice</div>
</div>
```

```css site
id: cards-practice-greedy-css
site: cards-practice-greedy
.row { display: flex; flex-wrap: wrap; gap: 12px; }
.card {
  flex: 1 1 90px;
  padding: 16px;
  border: 1px solid #ccc;
  border-radius: 6px;
  background: #f6f4f0;
}
/* your rules here */
```

When it works, is the first card twice as wide as the others?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Which of the three parts of `flex` decides the share of spare space?
2. The first card has a second class, `first`. Write a rule for it.
3. The new rule must come after the `.card` rule, so that it wins.

**Think about:** each card starts at its basis. Which part of its width
does `flex-grow` change: the basis, or the spare space on top of it?

**Try this next:** what happens if we give the first card
`flex: 2 1 0`, and the other two `flex: 1 1 0`?

</details>

<details class="dl-answer"><summary>answer</summary>

```css
.first { flex-grow: 2; }
```

`flex: 2 1 90px` on `.first` does the same job. Each card starts at its
basis, `90px` of content plus padding and border. Then the spare space
is shared out: two parts to the first card, and one part to each of the
others.

So the first card is wider, but it is not twice as wide. Only the
*spare* space is shared two to one. The basis, the padding and the
border stay the same for every card. In a preview `500px` wide, for
example, the first card is about `168px` wide and the others about
`146px`.

</details>

**4.** Build a page with a sidebar and a main area, side by side:

- the sidebar has a basis of `120px`. It never grows and never
  shrinks.
- the main area starts at `200px`, and takes all the spare space
- in a narrow preview, the main area moves under the sidebar

```html site
id: cards-practice-sidebar-html
site: cards-practice-sidebar
<div class="row">
  <aside class="side">Menu</aside>
  <main class="content">Today's news</main>
</div>
```

```css site
id: cards-practice-sidebar-css
site: cards-practice-sidebar
.row { display: flex; flex-wrap: wrap; gap: 12px; }
.side, .content { padding: 16px; border: 1px solid #ccc; background: #f6f4f0; }
/* your rules here */
```

<details class="dl-answer"><summary>answer</summary>

```css
.side { flex: 0 0 120px; }
.content { flex: 1 1 200px; }
```

`0 0 120px` means "start at `120px`, do not grow, do not shrink", so
the sidebar keeps its size. `1 1 200px` lets the main area grow into all
the spare space. When the row is too short for `120px` and `200px` side
by side, `flex-wrap: wrap` moves the main area to the next line. There
it grows to fill the whole width.

</details>

## In your own site

**5.** In your fork of `project_wad`, the `.card` rule in `styles.css`
has `flex: 1 1 200px`. The basis decides how narrow the window can get
before a card moves to a new row. Choose a basis that suits your own
cards.

1. Open your home page, with the window as wide as it goes.
2. Change the basis in the `.card` rule to `320px`. Save, and refresh.
   How many cards fit in the first row now?
3. Try `250px`. Then make the window narrower, slowly. When does the
   third card move to a new row?
4. Choose the basis that looks best with your own text in the cards.
5. Commit the change, with a message such as "Choose a width for the
   cards".

Does a card ever get so narrow that its heading breaks across two lines?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Your `.container` is at most `1000px` wide, and has `1rem` of padding
   on each side. So the row inside it is at most `968px` wide.
2. `.card-row` has a gap of `var(--spacing-sm)`, which is `1rem`, or
   `16px`. Three cards in a row have two gaps between them.
3. Your stylesheet sets `box-sizing: border-box`, so the basis includes
   each card's padding and border.

**Think about:** how much width do three cards of `320px` and two gaps
need? Is it more or less than `968px`?

**Try this next:** add a fourth card to `index.html`. With your basis,
how many cards sit in the first row?

</details>

<details class="dl-answer"><summary>answer</summary>

Three cards of `320px` need `3 × 320 = 960px`, and the two gaps add
`32px`, so `992px` in all. That is more than the `968px` the row has,
so the third card moves to a new row even in the widest window.

With `250px`, the three cards and two gaps need `782px`, so they fit in
one row in a wide window. As the window narrows below that, the third
card moves to a new row. There is no single right basis. A good one
lets each card's heading and text sit comfortably, without breaking the
heading across lines.

</details>
