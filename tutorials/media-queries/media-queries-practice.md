---
title: "Changing the layout for phones: media queries — Practice"
practice_for: media-queries
year: "2026-2027"
version: 2026.09.22.1
---

# Changing the layout for phones: media queries — Practice

On this page we practise media queries: CSS that applies only at some
widths. There are three kinds of problem:

- a broken page, where we find the mistake and fix it
- a small layout to build from a description
- a change in your own site, which you commit

Each problem has a folded answer. Some also have a hint, folded before
the answer. Try the problem first, and keep the **Preview width**
slider moving as you go. A media query only shows what it does when the
width crosses its breakpoint.

## Fix the broken page

**1.** The author wanted this notice to use smaller text on screens
`400px` wide or narrower.

```html site
id: mq-practice-brackets-html
site: mq-practice-brackets
<p class="note">Free delivery on orders over €30</p>
```

```css site
id: mq-practice-brackets-css
site: mq-practice-brackets
.note { background: #f6f4f0; padding: 12px; font-size: 20px; }
@media max-width: 400px {
  .note { font-size: 14px; }
}
```

Drag the slider all the way to narrow. Does the text ever get smaller?
Look closely at the `@media` line, and fix it.

<details class="dl-answer"><summary>answer</summary>

```css
.note { background: #f6f4f0; padding: 12px; font-size: 20px; }
@media (max-width: 400px) {
  .note { font-size: 14px; }
}
```

The condition needs its round brackets: `(max-width: 400px)`. Without
them, the browser cannot read the condition, so it skips the whole
`@media` block. It does not show an error. The rules inside do nothing
at any width, and the page looks as if the media query were not there.

</details>

**2.** This heading should get smaller in two steps: `24px` on a wide
screen, `18px` at `700px` or narrower, and `14px` at `400px` or
narrower.

```html site
id: mq-practice-order-html
site: mq-practice-order
<h2 class="title">Tentacular Plushies</h2>
```

```css site
id: mq-practice-order-css
site: mq-practice-order
.title { font-size: 24px; font-family: sans-serif; }
@media (max-width: 400px) {
  .title { font-size: 14px; }
}
@media (max-width: 700px) {
  .title { font-size: 18px; }
}
```

Drag the slider slowly from wide to narrow. How many times does the
heading change size? Which size never shows? Fix the CSS without
changing any of the numbers.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Set the preview to about `300px`. Which of the two media queries are
   true at that width?
2. Both of them set `font-size` on `.title`. When two rules with the
   same selector both apply, which one wins?
3. Which of the two blocks should win at `300px`? Where does it need to
   be in the stylesheet?

**Think about:** at a narrow width, a `max-width: 400px` query and a
`max-width: 700px` query are both true. Which should come last?

**Try this next:** what if the two queries used `min-width` instead?
Which order would they need then?

</details>

<details class="dl-answer"><summary>answer</summary>

```css
.title { font-size: 24px; font-family: sans-serif; }
@media (max-width: 700px) {
  .title { font-size: 18px; }
}
@media (max-width: 400px) {
  .title { font-size: 14px; }
}
```

At `300px`, both media queries are true, and both set the same property
on the same selector. The one further down the stylesheet wins. In the
broken page, that was the `700px` block, so the heading stayed at `18px`
and never reached `14px`. With `max-width` queries, the larger width
goes first, and the smaller width comes after it, so it can win on the
smallest screens.

</details>

**3.** On a wide screen, the shop wants its welcome line centred. On a
phone it should stay on the left. The author wanted the centring to
start at `600px`.

```html site
id: mq-practice-swap-html
site: mq-practice-swap
<p class="welcome">Welcome to the shop. Every plushie is made by hand.</p>
```

```css site
id: mq-practice-swap-css
site: mq-practice-swap
.welcome { font-family: sans-serif; background: #f6f4f0; padding: 12px; }
@media (max-width: 600px) {
  .welcome { text-align: center; }
}
```

Is the line centred on a wide preview? On a narrow one? Change one word
to fix it.

<details class="dl-answer"><summary>answer</summary>

```css
.welcome { font-family: sans-serif; background: #f6f4f0; padding: 12px; }
@media (min-width: 600px) {
  .welcome { text-align: center; }
}
```

`max-width: 600px` means "at `600px` or narrower", so the text was
centred on phones and not on wide screens. This is the opposite of the plan.
`min-width: 600px` means "at `600px` or wider".

</details>

## Make this

**4.** Build this card, written for a phone first. Here is what it
should do:

- on a narrow screen, it has `8px` of padding and a `#f6f4f0`
  background
- from `500px` wide and up, its padding grows to `32px`
- from `500px` wide and up, its text is also `20px`

Use one media query, with `min-width`.

```html site
id: mq-practice-card-html
site: mq-practice-card
<div class="card">Squishy Squid, €12. Soft, washable, and very squishy.</div>
```

```css site
id: mq-practice-card-css
site: mq-practice-card
.card {
  /* your rules here */
}
```

<details class="dl-answer"><summary>answer</summary>

```css
.card {
  padding: 8px;
  background: #f6f4f0;
}
@media (min-width: 500px) {
  .card {
    padding: 32px;
    font-size: 20px;
  }
}
```

The ordinary rule is for the phone. The media query adds to it from
`500px` up. The background is not in the media query, because it is
the same at every width. Only the things that change go inside.

</details>

**5.** Build a background that changes colour twice as the screen gets
wider:

- below `400px`: `#fde2e4`, a pink
- from `400px` to just under `700px`: `#e2ece9`, a green
- from `700px` up: `#dfe7fd`, a blue

Can you do it with one ordinary rule and two media queries?

```html site
id: mq-practice-bands-html
site: mq-practice-bands
<div class="band">What colour am I?</div>
```

```css site
id: mq-practice-bands-css
site: mq-practice-bands
.band {
  padding: 40px;
  font-family: sans-serif;
  /* your rules here */
}
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Start with the narrowest screen. Which colour goes in the ordinary
   `.band` rule?
2. Add a `min-width` media query for the next colour up.
3. Add one more for the widest screens. Which of the two queries must
   come last?

**Think about:** at `800px`, both `min-width` queries are true. Which
one should win?

**Try this next:** could you build the same thing with `max-width`
queries, starting from the widest screen?

</details>

<details class="dl-answer"><summary>answer</summary>

```css
.band {
  padding: 40px;
  font-family: sans-serif;
  background: #fde2e4;
}
@media (min-width: 400px) {
  .band { background: #e2ece9; }
}
@media (min-width: 700px) {
  .band { background: #dfe7fd; }
}
```

At `800px`, both media queries are true. The `700px` block comes last,
so its blue wins. With `min-width` queries, the smaller width goes
first. A version with `max-width` works too: blue in the ordinary rule,
then `(max-width: 699px)` for green, then `(max-width: 399px)` for pink,
in that order.

</details>

## In your own site

**6.** On [Changing the layout for phones: media
queries](tutorial:media-queries), you switched on the `480px` block at
the bottom of `styles.css`. Now let's add a rule of our own to it.

1. In `styles.css`, find the `.hero-text` rule. What `font-size` does
   it set?
2. Inside the `@media (max-width: 480px)` block, after the `.card`
   rule, add:

   ```css
   .hero-text {
       font-size: 1rem;
   }
   ```

3. Save, and open `index.html`. Open the inspector's device mode, and
   set a width of `400px`. Then try `600px`. Does the text under your
   main heading change size?
4. Commit the change, with a message such as "Smaller intro text on
   small phones".

Why does the new rule win over the `.hero-text` rule higher up, at
`400px`?

<details class="dl-answer"><summary>answer</summary>

The `.hero-text` rule sets `font-size: 1.25rem`. At `400px`, the new
rule makes the text `1rem`, a little smaller. At `600px`, the
`480px` block is not true, so the text is back to `1.25rem`.

At `400px`, both rules apply, and both set `font-size` on the same
selector, `.hero-text`. The media queries are at the bottom of
`styles.css`, so the new rule comes later, and it wins.

</details>
