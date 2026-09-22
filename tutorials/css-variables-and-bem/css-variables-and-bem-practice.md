---
title: "Naming classes so they stay tidy (BEM) — Practice"
practice_for: css-variables-and-bem
year: "2026-2027"
version: 2026.09.22.1
---

# Naming classes so they stay tidy (BEM) — Practice

On this page we practise BEM: blocks, elements and modifiers, and the
class names that join them. There are three kinds of problem:

- a broken page, where we find the mistake and fix it
- a small layout to build from a description
- a change in your own site, which you commit

Each problem has a folded answer. Some also have a hint, folded before
the answer. Try the problem first. With BEM, most mistakes are in the
class names, so read the HTML and the CSS side by side.

## Fix the broken page

**1.** Two buttons, a blue one and a red one. The red one has lost its
padding and its rounded corners, and it is not red.

```html site
id: bem-practice-alone-html
site: bem-practice-alone
<button class="button">Save</button>
<button class="button--danger">Delete</button>
```

```css site
id: bem-practice-alone-css
site: bem-practice-alone
:root {
  --button-color: #2563eb;
}
.button {
  padding: 10px 18px;
  border: none;
  border-radius: 6px;
  color: white;
  font-weight: 600;
  background: var(--button-color);
}
.button--danger {
  --button-color: #dc2626;
}
```

The CSS is fine. What is wrong in the HTML?

<details class="dl-answer"><summary>answer</summary>

```html
<button class="button">Save</button>
<button class="button button--danger">Delete</button>
```

A modifier class always goes beside the block's own class. The block
class, `button`, brings the base rule: the padding, the corners, the
white text and the background. The modifier, `button--danger`, only
changes the colour. On its own, it set a colour that no rule read, so
the second button was a plain browser button.

</details>

**2.** Here the Delete button should be red. The author gave the
modifier its own `background`. But the button is blue.

```html site
id: bem-practice-order-html
site: bem-practice-order
<button class="button">Save</button>
<button class="button button--danger">Delete</button>
```

```css site
id: bem-practice-order-css
site: bem-practice-order
.button--danger {
  background: #dc2626;
}
.button {
  padding: 10px 18px;
  border: none;
  border-radius: 6px;
  color: white;
  font-weight: 600;
  background: #2563eb;
}
```

Both rules set a `background` on the second button. Which one wins, and
why? Fix it.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The second button has both classes. How many rules set its
   `background`?
2. Each selector is one class. When two rules like that disagree, which
   one wins?
3. Where should the modifier's rule be, compared with the block's rule?

**Think about:** the tutorial's modifier set a variable, not a
`background`. Would that version have had this problem?

**Try this next:** rewrite the two rules so the modifier sets
`--button-color` and the block reads it. Does the order of the rules
matter then?

</details>

<details class="dl-answer"><summary>answer</summary>

```css
.button {
  padding: 10px 18px;
  border: none;
  border-radius: 6px;
  color: white;
  font-weight: 600;
  background: #2563eb;
}
.button--danger {
  background: #dc2626;
}
```

Both selectors are one class each, so the rule further down the
stylesheet wins. The block's rule came last, so its blue won. A
modifier's rule belongs after its block's rule, so its change comes
last.

The version on the tutorial page has no such problem. There, the
modifier sets `--button-color`, and only the block sets `background`,
so the two rules never disagree about the same property.

</details>

**3.** This card should have a bold title in a larger size. The title
looks like ordinary text.

```html site
id: bem-practice-typo-html
site: bem-practice-typo
<div class="card">
  <p class="card_title">Squishy Squid</p>
  <p>Soft, washable, and very squishy.</p>
</div>
```

```css site
id: bem-practice-typo-css
site: bem-practice-typo
.card {
  padding: 16px;
  border: 1px solid #ccc;
  font-family: sans-serif;
}
.card__title {
  font-size: 20px;
  font-weight: bold;
}
```

Compare the class in the HTML with the selector in the CSS, letter by
letter. Fix the HTML.

<details class="dl-answer"><summary>answer</summary>

```html
<p class="card__title">Squishy Squid</p>
```

A BEM element is joined to its block with two underscores, `__`. The
HTML had only one, so `card_title` and `card__title` were two different
names, and the rule matched nothing. The same goes for modifiers: they
need two hyphens, `--`.

</details>

## Make this

**4.** Build two product cards, named with BEM. Here is what they
should look like:

- each card is a block called `card`, with `16px` of padding and a
  `2px` solid border
- inside each card, the name is an element called `card__name`, in
  bold
- inside each card, the price is an element called `card__price`
- the border and the price share one colour, `#2c3e50`, kept in a
  variable called `--card-color`
- the second card is on sale. A modifier called `card--sale` turns its
  border and its price `#dc2626`, and changes nothing else

Add the classes to the HTML, then write the CSS.

```html site
id: bem-practice-cards-html
site: bem-practice-cards
<div>
  <p>Squishy Squid</p>
  <p>€12</p>
</div>
<div>
  <p>Cuddly Cuttlefish</p>
  <p>€9, was €15</p>
</div>
```

```css site
id: bem-practice-cards-css
site: bem-practice-cards
/* your rules here */
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Give both `div`s the block class. Which of them also needs the
   modifier class?
2. Give each `p` an element class.
3. Set `--card-color` on `:root`, and read it with `var()` in the
   `.card` border. In `.card__price`, read it again for the colour.
4. In `.card--sale`, set `--card-color` again, and nothing else.

**Think about:** why does the sale price turn red, when `.card--sale`
never mentions the price?

**Try this next:** add a third card with a modifier `card--new`, in a
green of your choosing.

</details>

<details class="dl-answer"><summary>answer</summary>

```html
<div class="card">
  <p class="card__name">Squishy Squid</p>
  <p class="card__price">€12</p>
</div>
<div class="card card--sale">
  <p class="card__name">Cuddly Cuttlefish</p>
  <p class="card__price">€9, was €15</p>
</div>
```

```css
:root {
  --card-color: #2c3e50;
}
.card {
  padding: 16px;
  border: 2px solid var(--card-color);
  margin-bottom: 12px;
}
.card__name {
  font-weight: bold;
}
.card__price {
  color: var(--card-color);
}
.card--sale {
  --card-color: #dc2626;
}
```

The modifier sets `--card-color` again on the second card. The price
sits inside that card, so it reads the new value too. That is a scoped
override: one change on the block, and every part inside it follows.
The `margin-bottom` is only there to keep the two cards apart.

We set `--card-color` on `:root`, as the tutorial did. Setting it on
`.card` works too, but then `.card` and `.card--sale` both set the
variable on the same element, so `.card--sale` must come after `.card`
to win.

</details>

## In your own site

**5.** In your starter, the main buttons have `class="btn btn-primary"`.
`btn` is the block, and `btn-primary` is a variant of it: a modifier,
with one hyphen. Let's rename it the BEM way, to `btn--primary`.

1. In `styles.css`, find every selector that says `.btn-primary`. There
   are two: the rule itself, and its `:hover` rule. Change each one to
   `.btn--primary`.
2. In `index.html`, find `btn-primary`, and change it to
   `btn--primary`.
3. Do the same in `about.html`.
4. Save all three files. Open both pages. Do the filled blue buttons
   look the same as before?
5. Commit the change, with a message such as "Rename btn-primary to
   the BEM modifier btn--primary".

What would you see if you forgot one of the three files?

<details class="dl-answer"><summary>answer</summary>

When all three files agree, nothing changes on screen: the same rules
match the same buttons, under a new name. The filled button is "Learn
More About Me" on `index.html`, and "View Portfolio" on `about.html`.

If `styles.css` still said `.btn-primary`, no button would match it,
and both filled buttons would look like the plain outlined ones. If only
one HTML file were missed, that page's button would still have the old
class, which no rule matches any more, so it would lose its fill. A
search for `btn-primary` in all three files is a good way to check
nothing was missed.

</details>
