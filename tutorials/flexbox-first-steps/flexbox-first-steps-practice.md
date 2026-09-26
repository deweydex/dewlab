---
title: "Lining boxes up in a row with Flexbox — Practice"
practice_for: flexbox-first-steps
year: "2026-2027"
version: 2026.09.22.1
---

# Lining boxes up in a row with Flexbox — Practice

On this page we practise flex rows: `display: flex`, `flex-wrap`,
`gap`, and the `flex` line that decides when a row breaks. There are
three kinds of problem:

- a broken page, where we find the mistake and fix it
- a small layout to build from a description
- a change in your own site, which you commit

Each problem has a folded answer. Some also have a hint, folded before
the answer. Try the problem first, and drag the **Preview width** slider
as you go. A row that looks fine when wide can break when narrow.

## Fix the broken page

**1.** Here is a row of four tags. It looks fine in a wide preview. Now
drag the slider to about `320px`.

```html site
id: flex-practice-overflow-html
site: flex-practice-overflow
<div class="tags">
  <span class="tag">Squid</span>
  <span class="tag">Cuttlefish</span>
  <span class="tag">Nautilus</span>
  <span class="tag">Octopus</span>
</div>
```

```css site
id: flex-practice-overflow-css
site: flex-practice-overflow
body { margin: 0; }
.tags {
  display: flex;
  gap: 8px;
}
.tag {
  flex: 0 0 100px;
  padding: 8px;
  background: #f6f4f0;
  border: 1px solid #ccc;
  font-family: sans-serif;
  text-align: center;
}
```

What happens to the last tags on a narrow screen? Add one line so the
tags stay inside the preview at every width.

<details class="dl-answer"><summary>answer</summary>

```css
body { margin: 0; }
.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.tag {
  flex: 0 0 100px;
  padding: 8px;
  background: #f6f4f0;
  border: 1px solid #ccc;
  font-family: sans-serif;
  text-align: center;
}
```

Without `flex-wrap: wrap`, flex items stay in one line whatever
happens. These tags cannot shrink, because the second number in
`flex: 0 0 100px` is `0`. So the last tags ran past the right-hand
edge, and the preview could scroll sideways. With `flex-wrap: wrap`, a
tag that has no room starts a new line. On a phone, a missing
`flex-wrap` is often the first thing to check when a row runs off the
screen.

</details>

**2.** The author wanted these three cards side by side. They sit one
above the other instead.

```html site
id: flex-practice-parent-html
site: flex-practice-parent
<div class="row">
  <div class="card">Squishy Squid</div>
  <div class="card">Cuddly Cuttlefish</div>
  <div class="card">Nautical Nautilus</div>
</div>
```

```css site
id: flex-practice-parent-css
site: flex-practice-parent
.card {
  display: flex;
  flex-wrap: wrap;
  padding: 16px;
  border: 1px solid #ccc;
  background: #f6f4f0;
  font-family: sans-serif;
}
```

Which element should be the flex container? Fix the CSS.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. `display: flex` lays out the children of the element it is on. What
   are the children of each `.card`?
2. Which element has the three cards as its children?
3. Which lines belong on that element's rule?

**Think about:** is a card a flex container here, or a flex item?

**Try this next:** once the cards are in a row, what would `gap: 12px`
do, and on which rule would it go?

</details>

<details class="dl-answer"><summary>answer</summary>

```css
.row {
  display: flex;
  flex-wrap: wrap;
}
.card {
  padding: 16px;
  border: 1px solid #ccc;
  background: #f6f4f0;
  font-family: sans-serif;
}
```

`display: flex` goes on the parent, the flex container. Its children
become the flex items and line up in a row. In the broken page, each
card was a flex container, so it laid out its own text, and the cards
themselves stayed as ordinary block boxes, one above the other. The
cards now sit side by side, each as wide as its own text.

</details>

**3.** These three cards are in a row, but they touch. The author wanted
`12px` of space between them.

```html site
id: flex-practice-gap-html
site: flex-practice-gap
<div class="row">
  <div class="card">Squid</div>
  <div class="card">Cuttlefish</div>
  <div class="card">Nautilus</div>
</div>
```

```css site
id: flex-practice-gap-css
site: flex-practice-gap
.row {
  display: flex;
  flex-wrap: wrap;
}
.card {
  gap: 12px;
  flex: 1 1 80px;
  padding: 16px;
  border: 1px solid #ccc;
  background: #f6f4f0;
  font-family: sans-serif;
}
```

The `gap` line is there. Why does it do nothing? Fix it.

<details class="dl-answer"><summary>answer</summary>

```css
.row {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}
.card {
  flex: 1 1 80px;
  padding: 16px;
  border: 1px solid #ccc;
  background: #f6f4f0;
  font-family: sans-serif;
}
```

`gap` sets the space between the items of a flex container, so it goes
on the container, `.row`. On `.card` it had nothing to space out,
because a card here is not a flex container.

</details>

## Make this

**4.** Build a row of four tags that wraps. Here is what it should do:

- the tags sit side by side, and wrap onto a new line when they no
  longer fit
- there is `8px` between the tags
- each tag starts from `60px` of content, can grow to share spare space,
  and can shrink
- each tag has `6px 10px` of padding and a `1px solid #ccc` border

Then, before you drag the slider: at what width will the fourth tag
move to a line of its own? Calculate it first, then check.

```html site
id: flex-practice-tags-html
site: flex-practice-tags
<div class="tags">
  <span class="tag">Soft</span>
  <span class="tag">Warm</span>
  <span class="tag">Small</span>
  <span class="tag">Blue</span>
</div>
```

```css site
id: flex-practice-tags-css
site: flex-practice-tags
body { margin: 0; }
.tags {
  /* your rules here */
}
.tag {
  /* your rules here */
  background: #f6f4f0;
  font-family: sans-serif;
}
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Which three lines go on `.tags`? The tutorial's `.row` rule had them.
2. On `.tag`, the `flex` line holds three settings: grow, shrink, and
   the starting width.
3. For the width: how wide is one tag in all, with its padding and its
   border on both sides? Then add four tags and three gaps.

**Think about:** the `60px` is the width of the content only. What sits
outside it?

**Try this next:** if the padding were `6px 20px`, where would the
fourth tag move?

</details>

<details class="dl-answer"><summary>answer</summary>

```css
body { margin: 0; }
.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.tag {
  flex: 1 1 60px;
  padding: 6px 10px;
  border: 1px solid #ccc;
  background: #f6f4f0;
  font-family: sans-serif;
}
```

One tag is 1 + 10 + 60 + 10 + 1 = `82px` wide in all. Four tags and
three `8px` gaps need 4 × 82 + 3 × 8 = `352px`. So at `352px` all four
still fit, and below that the fourth tag moves to a line of its own,
where it grows to fill the line.

</details>

## In your own site

**5.** Your About page has two buttons near the bottom, under "Want to
See My Work?". The `.cta-buttons` rule in `styles.css` lays them out
with `display: flex`, `flex-wrap: wrap`, and
`gap: var(--spacing-sm)`.

1. Open `about.html` in your browser, and open the inspector's device
   mode. Drag the page from wide to narrow. At about what width does
   the second button drop below the first?
2. In `styles.css`, change the `gap` in `.cta-buttons` to
   `var(--spacing-md)`.
3. Save, and refresh. Is the space between the buttons bigger?
4. Drag the width again. Does the second button drop sooner or later
   than before?
5. Commit the change, with a message such as "Wider gap between About
   page buttons".

Why did the width where the button drops change, when all we changed
was the gap?

<details class="dl-answer"><summary>answer</summary>

`--spacing-sm` is `1rem` and `--spacing-md` is `2rem`, so the gap
between the buttons doubled, from `16px` to `32px` with the browser's
default text size.

The second button now drops a little sooner, at a wider width. The two
buttons and the gap between them have to fit in one line. A bigger gap
means the line needs more room, so it runs out of room sooner as the
page gets narrower. This is the same sum as on the tutorial page:
items, plus the gaps between them.

</details>
