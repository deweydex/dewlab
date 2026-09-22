---
title: "Changing the order of boxes on screen — Practice"
practice_for: order-on-screen
year: "2026-2027"
version: 2026.09.22.1
---

# Changing the order of boxes on screen — Practice

On this page we practise the `order` property, and the question that
goes with it: should this change be made in the CSS, or in the HTML?
There are three kinds of problem:

- a broken page, where we find the mistake and fix it
- a small layout to build from a description
- a change in your own site, which you commit

Each problem has a folded answer. Some also have a hint, folded before
the answer. Try the problem first. For some problems, you will need to
click in the preview and press Tab, to see where the keyboard goes.

## Fix the broken page

**1.** The shop wants its "Sale" link to come first in this row, on the
left. The author gave it `order: 1`. But it is still last.

```html site
id: order-practice-first-html
site: order-practice-first
<div class="row">
  <a href="#" class="item">New</a>
  <a href="#" class="item">Plushies</a>
  <a href="#" class="item sale">Sale</a>
</div>
```

```css site
id: order-practice-first-css
site: order-practice-first
.row {
  display: flex;
  gap: 12px;
}
.item {
  padding: 10px 14px;
  border: 1px solid #ccc;
  background: #f6f4f0;
  font-family: sans-serif;
}
.sale {
  order: 1;
}
```

Why does `order: 1` not bring the link to the front? Fix it.

<details class="dl-answer"><summary>answer</summary>

```css
.sale {
  order: -1;
}
```

Every item starts at `order: 0`. The browser lines the items up from
the smallest number to the largest, so `1` is bigger than the other
two, and it put the Sale link last. Any number smaller than `0` puts it
first. `-1` is the usual choice.

</details>

**2.** This row shows the three steps of buying a plushie. On screen,
the steps are in the right order. Now click an empty part of the
preview, below the row, and press Tab three times.

```html site
id: order-practice-steps-html
site: order-practice-steps
<div class="steps">
  <a href="#" class="step pay">3. Pay</a>
  <a href="#" class="step basket">1. Basket</a>
  <a href="#" class="step delivery">2. Delivery</a>
</div>
```

```css site
id: order-practice-steps-css
site: order-practice-steps
.steps {
  display: flex;
  gap: 12px;
}
.step {
  padding: 10px 14px;
  border: 1px solid #ccc;
  background: #f6f4f0;
  font-family: sans-serif;
}
.step:focus {
  outline: 3px solid #d9720c;
}
.basket { order: 1; }
.delivery { order: 2; }
.pay { order: 3; }
```

In what order does Tab visit the steps? Would a screen reader read them
in the right order? Fix the page so that the screen, the keyboard and a
screen reader all agree.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Read the HTML. In what order are the three links written?
2. Tab follows that order. Does `order` change it?
3. Where should the fix go, if we want Tab and a screen reader to
   follow the right order too?

**Think about:** here, does the order of the steps change their
meaning?

**Try this next:** once the HTML is right, are the three `order` rules
still needed?

</details>

<details class="dl-answer"><summary>answer</summary>

Change the source order in the HTML:

```html
<div class="steps">
  <a href="#" class="step basket">1. Basket</a>
  <a href="#" class="step delivery">2. Delivery</a>
  <a href="#" class="step pay">3. Pay</a>
</div>
```

Then delete the three `order` rules from the CSS. They have nothing
left to do.

In the broken page, Tab went to "3. Pay" first, because it comes first
in the HTML. A screen reader would read the steps in that order too.
The steps only make sense in one order, so the fix belongs in the HTML.
`order` is for changes of look, where the meaning stays the same.

</details>

## Make this

**3.** Here is a row of four plushies. On a narrow screen, it is fine as
it is. From `500px` wide and up, the shop wants the "New" plushie at
the far right end of the row.

```html site
id: order-practice-wide-html
site: order-practice-wide
<div class="row">
  <div class="item new">New: Octopus</div>
  <div class="item">Squid</div>
  <div class="item">Cuttlefish</div>
  <div class="item">Nautilus</div>
</div>
```

```css site
id: order-practice-wide-css
site: order-practice-wide
.row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.item {
  padding: 10px;
  border: 1px solid #ccc;
  background: #f6f4f0;
  font-family: sans-serif;
}
/* your rules here */
```

Use `order` inside a media query. Drag the slider across `500px` to
check.

<details class="dl-answer"><summary>answer</summary>

```css
@media (min-width: 500px) {
  .new {
    order: 1;
  }
}
```

From `500px` up, the "New" item has `order: 1`, and the others keep
`0`, so it goes last. Below `500px`, the media query is not true, and
the row follows the HTML again. This is a fair use of `order`: the
plushies are not steps, and either order makes sense to a reader.

</details>

**4.** Here are four boxes, A, B, C and D, in that order in the HTML.
Using only `order`, and no change to the HTML, make the row read
D, C, B, A on screen.

```html site
id: order-practice-reverse-html
site: order-practice-reverse
<div class="row">
  <div class="box a">A</div>
  <div class="box b">B</div>
  <div class="box c">C</div>
  <div class="box d">D</div>
</div>
```

```css site
id: order-practice-reverse-css
site: order-practice-reverse
.row {
  display: flex;
  gap: 8px;
}
.box {
  padding: 16px;
  border: 1px solid #ccc;
  background: #f6f4f0;
  font-family: sans-serif;
}
/* your rules here */
```

What is the fewest number of `order` rules you need?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Every box starts at `order: 0`. Which box can stay at `0`?
2. D must come first. What number puts it in front of a box at `0`?
3. Work along the row. What does C need, so that it comes after D and
   before the box at `0`?

**Think about:** when two boxes have the same number, which one comes
first?

**Try this next:** could you do it with positive numbers only?

</details>

<details class="dl-answer"><summary>answer</summary>

```css
.d { order: -3; }
.c { order: -2; }
.b { order: -1; }
```

A can stay at `0`, so three rules are enough. D has the smallest
number, so it comes first, then C, then B, then A. With positive
numbers, `.a { order: 3; }`, `.b { order: 2; }` and `.c { order: 1; }`
work too, with D staying at `0`.

</details>

## In your own site

**5.** On your About page, the section at the bottom has two buttons:
"View Portfolio", then "Contact Me". Suppose you want "Contact Me" to
come first. Where should that change go?

1. Open `about.html`, and find the `<div class="cta-buttons">` near the
   bottom.
2. Move the line with "Contact Me" above the line with "View
   Portfolio". Do not add any `order` to the CSS.
3. Save, and open `about.html` in your browser.
4. Refresh the page, and press Tab until the outline reaches these two
   buttons. Which one does it reach first?
5. Commit the change, with a message such as "Put Contact Me first on
   the About page".

Why is the HTML the right place for this change, and not `order`?

<details class="dl-answer"><summary>answer</summary>

The buttons swap places on screen, and Tab now reaches "Contact Me"
first. The screen order, the keyboard order and the order a screen
reader follows all match, because all three come from the HTML.

With `order`, the buttons would have swapped on screen, but Tab and a
screen reader would still meet "View Portfolio" first. When we want
one thing to come first for everyone, the source order is the place to
change it.

</details>
