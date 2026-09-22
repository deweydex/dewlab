---
title: "The box model: padding, border and margin — Practice"
practice_for: the-box
year: "2026-2027"
version: 2026.09.22.1
---

# The box model: padding, border and margin — Practice

On this page we practise the three layers around every box: padding,
border and margin. There are three kinds of problem:

- a broken page, where we find the mistake and fix it
- a small layout to build from a description
- a change in your own site, which you commit

Each problem has a folded answer. Some also have a hint, folded before
the answer. Try the problem first. Being wrong, and then finding out
why, teaches more than reading the answer.

## Fix the broken page

**1.** A designer asked for a gap of `60px` between these two notices.
The author gave the first box `30px` of margin below it, and the second
box `30px` of margin above it. Under the notices is a grey square,
`60px` tall, so we can compare.

```html site
id: box-practice-gap-html
site: box-practice-gap
<div class="first">Free delivery this week</div>
<div class="second">New plushies every Friday</div>
<div class="ruler">60px</div>
```

```css site
id: box-practice-gap-css
site: box-practice-gap
.first {
  background: #f6f4f0;
  border: 2px solid #2c3e50;
  padding: 10px;
  margin-bottom: 30px;
}
.second {
  background: #f6f4f0;
  border: 2px solid #2c3e50;
  padding: 10px;
  margin-top: 30px;
}
.ruler {
  width: 60px;
  height: 60px;
  margin-top: 40px;
  background: #ccc;
  font-size: 12px;
}
```

Is the gap between the two notices as tall as the grey square? Why not?
Change the CSS so the gap is `60px`.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Look at the gap. Is it closer to `30px` or to `60px`?
2. Where do the two margins meet? One is below the first box, and one
   is above the second.
3. Remember what happens when a bottom margin meets a top margin. Do
   they add up?

**Think about:** which margin sets the gap, when two margins meet?

**Try this next:** what gap do we get with `margin-bottom: 50px` on the
first box and `margin-top: 20px` on the second?

</details>

<details class="dl-answer"><summary>answer</summary>

The gap is `30px`, half the height of the grey square. This is *margin
collapse*: the bottom margin of the first box meets the top margin of the
second, and they do not add up. The larger of the two sets the gap, and
here both are `30px`.

One fix is to give one margin the whole gap, and remove the other:

```css
.first {
  background: #f6f4f0;
  border: 2px solid #2c3e50;
  padding: 10px;
  margin-bottom: 60px;
}
.second {
  background: #f6f4f0;
  border: 2px solid #2c3e50;
  padding: 10px;
}
```

Setting `margin-top: 60px` on the second box works too. Either way, the
larger margin is now `60px`, so the gap is `60px`.

</details>

**2.** This banner should fill the width of the preview, with its border
showing on all four sides. Look at its right-hand edge.

```html site
id: box-practice-overflow-html
site: box-practice-overflow
<div class="banner">Free delivery on orders over €30</div>
```

```css site
id: box-practice-overflow-css
site: box-practice-overflow
body { margin: 0; }
.banner {
  width: 100%;
  padding: 20px;
  border: 4px solid #2c3e50;
  background: #f6f4f0;
}
```

Where is the right-hand border? Can you scroll the preview sideways? Fix
the banner so that it fits, and keep its padding and border.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. `width: 100%` makes something as wide as the preview. But which part
   of the box does `width` measure, by default?
2. Add up the parts: the width, then the padding on both sides, then the
   border on both sides. How much wider than the preview is that?
3. The box model page named one property that changes what `width`
   measures.

**Think about:** by default, are the padding and the border inside the
width, or added on outside it?

**Try this next:** with the default, how wide is a box with
`width: 200px`, `padding: 10px` and `border: 5px solid`?

</details>

<details class="dl-answer"><summary>answer</summary>

```css
body { margin: 0; }
.banner {
  width: 100%;
  padding: 20px;
  border: 4px solid #2c3e50;
  background: #f6f4f0;
  box-sizing: border-box;
}
```

By default, `width` sets the width of the content only. The padding and
the border are added on outside it: `20px` and `4px` on each side, so the
banner was `48px` wider than the preview. Its right-hand padding and
border ran off the edge. `box-sizing: border-box` makes `width` include
the padding and the border, so the whole banner is now as wide as the
preview.

</details>

**3.** This card has a background and a border, but the words sit right
up against the border. The author wanted `20px` of space between the
words and the border.

```html site
id: box-practice-tight-html
site: box-practice-tight
<div class="card">Squishy Squid, €12</div>
<div class="card">Cuddly Cuttlefish, €15</div>
```

```css site
id: box-practice-tight-css
site: box-practice-tight
.card {
  background: #f6f4f0;
  border: 3px solid #2c3e50;
  margin: 20px;
}
```

The author did write `20px`. So why do the words still touch the border?
Fix it.

<details class="dl-answer"><summary>answer</summary>

```css
.card {
  background: #f6f4f0;
  border: 3px solid #2c3e50;
  margin: 20px;
  padding: 20px;
}
```

`margin` is space outside the border, so it moved the cards away from
each other and from the edge. Space between the words and the border is
*padding*, which sits inside the border. Notice that the padding takes
the card's own background colour too.

</details>

## Make this

**4.** Build this price tag in the cell below. Here is what it should
look like:

- the text sits on a `#f6f4f0` background
- there is `10px` of space above and below the text, inside the border,
  and `30px` to the left and right of it
- the border is `3px`, solid and `#2c3e50`
- the corners are rounded by `12px`
- the tag sits `40px` away from everything around it

Can you set the padding with one declaration, using two values?

```html site
id: box-practice-tag-html
site: box-practice-tag
<div class="tag">Sleepy Seal, €18</div>
```

```css site
id: box-practice-tag-css
site: box-practice-tag
.tag {
  /* your rules here */
}
```

<details class="dl-answer"><summary>answer</summary>

```css
.tag {
  background: #f6f4f0;
  padding: 10px 30px;
  border: 3px solid #2c3e50;
  border-radius: 12px;
  margin: 40px;
}
```

With two values, the first sets the top and bottom padding, and the
second sets the left and right. The space around the tag is outside the
border, so it is `margin`. The tag stretches across the whole preview.
That is expected: we set its layers, and not its width.

</details>

## In your own site

**5.** In your fork, `styles.css` has a `.card` rule. It sets
`padding: var(--spacing-md)` and `border-radius: var(--radius-md)`. It
has a shadow, and no border.

1. Change the padding to two values:
   `padding: var(--spacing-sm) var(--spacing-lg);`
2. Add a border: `border: 2px solid var(--accent-color);`
3. Save, and refresh `index.html`. Look at the card under "A Little
   About Me". Which sides have less space now, and which have more?
4. Keep the values you like best. You could try other spacing
   variables from the top of `styles.css`, such as `--spacing-xs` or
   `--spacing-md`.
5. Commit the change, with a message that says what you changed, such
   as "Give cards a border and wider side padding".

Does the card on `about.html` change too? Why?

<details class="dl-answer"><summary>answer</summary>

With `padding: var(--spacing-sm) var(--spacing-lg)`, the top and bottom
padding get smaller and the left and right padding get bigger. The first
value sets the top and bottom, and the second sets the left and right.
The border appears outside the padding, and follows the rounded corners.

The card on `about.html` changes too. Both pages link to the same
`styles.css`, and both use the class `card`, so one rule styles both
cards.

</details>

**6.** Now let's find margin collapse in your own site. Open `about.html`
in your browser, and open the inspector.

1. Select the heading "Why Web Development?". In `styles.css`, the rule
   `.about-content h2` gives it `margin-top: var(--spacing-lg)`.
2. Select the paragraph just above that heading. The `p` rule gives
   it `margin-bottom: var(--spacing-sm)`.
3. Look at each one in the inspector's box model panel. It shows the
   margins in pixels.

Is the gap between the paragraph and the heading the two margins added
together? Which margin sets the gap?

4. Say we want more space above each heading on this page. Which margin
   should we make bigger: the paragraph's bottom margin, or the
   heading's top margin? Decide before you try it.
5. Change the `.about-content h2` rule to
   `margin-top: var(--spacing-xl);`. Save, refresh, and check the gap
   in the inspector again.
6. Commit the change, with a message such as "More space above About
   page headings".

<details class="dl-answer"><summary>answer</summary>

The gap is not the two margins added together. The heading's top margin
is the larger of the two, so it sets the gap on its own. With the
browser's default text size, the panel shows `48` for the heading's top
margin and `16` for the paragraph's bottom margin, and the gap is `48`
pixels, not `64`.

So the heading's margin is the one to change. Making the paragraph's
bottom margin bigger would change nothing here, until it grew larger than
the heading's. With `margin-top: var(--spacing-xl)`, the panel shows
`64`, and the gap is `64` pixels.

</details>
